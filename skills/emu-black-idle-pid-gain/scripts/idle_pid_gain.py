#!/usr/bin/env python3
"""
Identify the EMU Black idle *airflow* PID loop gain margin from a logged oscillation,
and prescribe a kP.

Method (see ../SKILL.md for the derivation and the caveats):

  1. Confirm the loop is P-dominated by regressing `Idle air %` on `Ignition Angle`.
     In the v3 cascade the airflow PID's error IS (Ignition Angle - Target ign angle),
     so the regression slope recovers `idleAirFlowKP` in %/deg straight out of the log.
  2. Extract the closed-loop pole from the decaying oscillation: decay ratio r per
     cycle and period T  ->  log decrement d = ln(1/r),  zeta = d/sqrt(4pi^2+d^2).
  3. Fit a first-order-plus-deadtime plant by solving the characteristic equation
     (tau*s + 1) + K*exp(-L*s) = 0  at the observed pole, for a range of assumed tau.
     Near the stability boundary the resulting kP/Ku is nearly tau-independent, which
     is what makes this trustworthy without knowing the plant.
  4. Sweep kP and report decay ratio / period / damping for each.

Usage:
  python idle_pid_gain.py LOG.csv --fit 8.9 12.1 [--regress 6 30] [--settled 20 100]
  python idle_pid_gain.py LOG.csv --auto          # pick the fit window automatically

Only numpy is required.
"""
import argparse, csv, sys
import numpy as np

AIR, IGN, RPM, TIME = 'Idle air %', 'Ignition Angle', 'RPM', 'TIME'


# ---------------------------------------------------------------- solvers (no scipy)
def bisect(f, a, b, tol=1e-13, it=400):
    fa = f(a)
    for _ in range(it):
        m = 0.5 * (a + b)
        if f(m) * fa <= 0:
            b = m
        else:
            a, fa = m, f(m)
        if b - a < tol:
            break
    return 0.5 * (a + b)


def newton2(F, x0, args=(), it=400):
    """Damped Newton for a 2-eq/2-unknown real system. Returns (x, converged)."""
    x = np.array(x0, float)
    for _ in range(it):
        f = np.array(F(x, *args), float)
        if np.max(np.abs(f)) < 1e-13:
            break
        J = np.zeros((len(x), len(x)))
        for j in range(len(x)):
            h = 1e-7 * max(abs(x[j]), 1e-4)
            xp = x.copy(); xp[j] += h
            J[:, j] = (np.array(F(xp, *args), float) - f) / h
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, False
        n = np.linalg.norm(dx)
        if n > 0.5:
            dx *= 0.5 / n
        x = x + dx
    return x, np.max(np.abs(np.array(F(x, *args), float))) < 1e-7


# ---------------------------------------------------------------- log loading
def load(path):
    with open(path, newline='') as fh:
        rows = list(csv.reader(fh, delimiter=';'))
    hdr = [h for h in rows[0] if h]
    need = {TIME, AIR, IGN, RPM} - set(hdr)
    if need:
        sys.exit("log is missing required channel(s): %s" % ", ".join(sorted(need)))
    data = np.array([[float(x) for x in r[:len(hdr)]]
                     for r in rows[1:] if len(r) >= len(hdr) and r[0].strip()])
    return {h: data[:, i] for i, h in enumerate(hdr)}


# ---------------------------------------------------------------- steps
def regress_kp(t, air, ign, lo, hi):
    m = (t >= lo) & (t <= hi)
    a, g = air[m], ign[m]
    A = np.vstack([g, np.ones_like(g)]).T
    (slope, icept), *_ = np.linalg.lstsq(A, a, rcond=None)
    r2 = 1 - ((a - A @ [slope, icept]) ** 2).sum() / ((a - a.mean()) ** 2).sum()
    return slope, icept, r2


def turning_points(x, y, lo, hi, minsep):
    m = (x >= lo) & (x <= hi)
    xx, yy = x[m], y[m]
    out = []
    for i in range(2, len(yy) - 2):
        up = yy[i] >= yy[i - 1] and yy[i] >= yy[i + 1] and yy[i] > yy[i - 2] and yy[i] > yy[i + 2]
        dn = yy[i] <= yy[i - 1] and yy[i] <= yy[i + 1] and yy[i] < yy[i - 2] and yy[i] < yy[i + 2]
        if not (up or dn):
            continue
        kind = 'P' if up else 'T'
        if out and out[-1][2] == kind and i - out[-1][0] < minsep:
            if (up and yy[i] > out[-1][3]) or (dn and yy[i] < out[-1][3]):
                out[-1] = (i, xx[i], kind, yy[i])
        elif not out or i - out[-1][0] >= minsep:
            out.append((i, xx[i], kind, yy[i]))
    return out


def pole_from_window(t, y, lo, hi, minsep):
    """decay ratio per full cycle + period, from alternating turning points."""
    tp = turning_points(t, y, lo, hi, minsep)
    amps, times = [], []
    for i in range(len(tp) - 1):
        if tp[i][2] != tp[i + 1][2]:
            amps.append(abs(tp[i + 1][3] - tp[i][3]))
            times.append(0.5 * (tp[i][1] + tp[i + 1][1]))
    rs, Ts = [], []
    for i in range(len(amps) - 2):
        if amps[i] > 1e-6 and amps[i + 2] > 0:
            rs.append(amps[i + 2] / amps[i])
            Ts.append(times[i + 2] - times[i])
    return tp, amps, times, rs, Ts


def fit_fopdt(sigma, wd, taus):
    """Solve (tau s+1)+K e^{-Ls}=0 at s=-sigma+j wd for (K, L). Return per-tau results."""
    def resid(p, tau):
        K, L = p
        s = complex(-sigma, wd)
        z = (tau * s + 1) + K * np.exp(-L * s)
        return [z.real, z.imag]

    out = []
    for tau in taus:
        (K, L), ok = newton2(resid, [3.0, 0.25], args=(tau,))
        if not ok or K <= 0 or L <= 0:
            continue
        wu = bisect(lambda w: np.arctan(w * tau) + w * L - np.pi, 1e-9, 500.0 / L)
        Ku = np.sqrt(1 + (wu * tau) ** 2)          # |1/G(j wu)| with plant gain folded into K
        out.append(dict(tau=tau, K=K, L=L, Ku=Ku, wu=wu, ratio=K / Ku, Tu=2 * np.pi / wu))
    return out


def pole_at(Kn, L, tau, seed):
    def eq(v):
        s = complex(v[0], v[1])
        z = (tau * s + 1) + Kn * np.exp(-L * s)
        return [z.real, z.imag]
    x, ok = newton2(eq, seed)
    return complex(x[0], x[1]), ok


def decay_at(kP, kP_now, fit, seed):
    s, ok = pole_at(fit['K'] * kP / kP_now, fit['L'], fit['tau'], seed)
    if not ok or s.imag < 1e-3:
        return None
    T = 2 * np.pi / s.imag
    r = float(np.exp(s.real * T))
    d = np.log(1 / max(r, 1e-12))
    return dict(T=T, r=r, zeta=d / np.sqrt(4 * np.pi ** 2 + d ** 2))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('log')
    ap.add_argument('--fit', nargs=2, type=float, metavar=('T0', 'T1'),
                    help='window holding the clean decaying cycles')
    ap.add_argument('--regress', nargs=2, type=float, metavar=('T0', 'T1'),
                    help='window for the kP regression (default: --fit widened 4x)')
    ap.add_argument('--settled', nargs=2, type=float, metavar=('T0', 'T1'),
                    help='window for residual-dither stats')
    ap.add_argument('--auto', action='store_true',
                    help='auto-pick the fit window: largest sustained ignition swing')
    ap.add_argument('--taus', type=float, nargs='+',
                    default=[0.40, 0.55, 0.74, 0.90, 1.10],
                    help='plant time constants to test (s); the answer should be insensitive')
    ap.add_argument('--sweep', type=float, nargs='+',
                    default=[2.0, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3],
                    help='kP values to report')
    ap.add_argument('--minsep', type=int, default=8,
                    help='min samples between turning points (default 8 = 0.32 s @25 Hz)')
    a = ap.parse_args()

    C = load(a.log)
    t, air, ign, rpm = C[TIME], C[AIR], C[IGN], C[RPM]
    dt = float(np.median(np.diff(t)))
    print("log: %s   %d samples @ %.0f Hz   t = %.1f .. %.1f s"
          % (a.log, len(t), 1 / dt, t[0], t[-1]))

    if a.auto and not a.fit:
        best, run = None, None
        idx = np.flatnonzero(rpm > 400)
        for lo in np.arange(t[idx[0]], t[idx[0]] + 40, 1.0):
            hi = lo + 4.0
            m = (t >= lo) & (t <= hi)
            if m.sum() < 40:
                continue
            sw = np.ptp(ign[m])
            if best is None or sw > best:
                best, run = sw, (lo, hi)
        a.fit = list(run)
        print("auto fit window: %.1f .. %.1f s (ignition swing %.1f deg)" % (a.fit[0], a.fit[1], best))
    if not a.fit:
        sys.exit("give --fit T0 T1 (or --auto)")

    reg = a.regress or [a.fit[0] - 1.5 * (a.fit[1] - a.fit[0]),
                        a.fit[1] + 4.0 * (a.fit[1] - a.fit[0])]

    # 1 --------------------------------------------------------------- kP from the log
    slope, icept, r2 = regress_kp(t, air, ign, *reg)
    print("\n[1] airflow output vs ignition angle,  t = %.1f..%.1f s" % (reg[0], reg[1]))
    print("    Idle air %% = %.2f + %.3f * Ignition Angle      R^2 = %.3f" % (icept, slope, r2))
    print("    -> measured idleAirFlowKP = %.2f %%/deg" % slope)
    if r2 < 0.5:
        print("    !! low R^2: the loop is NOT P-dominated in this window; the")
        print("       identification below assumes pure proportional control.")
    kP_now = slope

    # 2 --------------------------------------------------------------- closed-loop pole
    tp, amps, times, rs, Ts = pole_from_window(t, ign, a.fit[0], a.fit[1], a.minsep)
    if len(rs) < 1:
        sys.exit("no full cycle found in --fit window; widen it or lower --minsep")
    r_m, T_m = float(np.median(rs)), float(np.median(Ts))
    d = np.log(1 / r_m)
    zeta = d / np.sqrt(4 * np.pi ** 2 + d ** 2)
    wd, sigma = 2 * np.pi / T_m, -np.log(r_m) / T_m
    print("\n[2] closed-loop pole from t = %.1f..%.1f s" % (a.fit[0], a.fit[1]))
    print("    half-cycle p-p amplitudes (deg): " + " ".join("%.1f" % x for x in amps))
    print("    decay ratio/cycle r = %.3f  (n=%d: %s)" % (r_m, len(rs), " ".join("%.2f" % x for x in rs)))
    print("    period T = %.2f s          log decrement = %.4f" % (T_m, d))
    print("    zeta = %.4f   wd = %.3f rad/s   sigma = %.4f 1/s" % (zeta, wd, sigma))
    print("    cycles to 5%% of initial amplitude = %.1f" % (np.log(0.05) / np.log(r_m)))
    print("    napkin check  kP/Ku ~ 1 - ln(1/f)/(pi*n) = %.3f" % (1 - d / np.pi))

    # 3 --------------------------------------------------------------- plant + Ku
    fits = fit_fopdt(sigma, wd, a.taus)
    if not fits:
        sys.exit("FOPDT fit failed for every tau; check the fit window")
    print("\n[3] FOPDT fit   (tau s + 1) + K exp(-L s) = 0   at the observed pole")
    print("    tau[s]   loop K   deadtime L[s]   kP/Ku    Ku[%/deg]   Tu[s]")
    for f in fits:
        print("    %5.2f   %7.3f   %11.3f   %6.3f   %9.2f   %5.2f"
              % (f['tau'], f['K'], f['L'], f['ratio'], kP_now / f['ratio'], f['Tu']))
    ratios = [f['ratio'] for f in fits]
    print("    kP/Ku spread across tau: %.3f .. %.3f  %s"
          % (min(ratios), max(ratios),
             "(tau-insensitive - trust it)" if max(ratios) - min(ratios) < 0.05
             else "(tau-SENSITIVE - treat Ku as approximate)"))
    mid = fits[len(fits) // 2]
    Ku = kP_now / mid['ratio']
    print("    -> Ku = %.2f %%/deg,  Tu = %.2f s;  current kP = %.2f is %.0f%% of ultimate"
          % (Ku, mid['Tu'], kP_now, 100 * mid['ratio']))
    print("       gain margin = %.2f  (%.1f dB)" % (1 / mid['ratio'], -20 * np.log10(mid['ratio'])))
    print("    Ziegler-Nichols anchors:  P-only 0.50*Ku = %.2f   PI 0.45*Ku = %.2f   quiet 0.20*Ku = %.2f"
          % (0.50 * Ku, 0.45 * Ku, 0.20 * Ku))

    # 4 --------------------------------------------------------------- sweep
    print("\n[4] predicted behaviour vs kP   (columns = assumed tau, %s s)"
          % "/".join("%.2f" % f['tau'] for f in fits))
    print("    kP     " + "".join("  r/cyc  T[s]  zeta " for _ in fits) + "  dither")
    for kp in a.sweep:
        line = "    %.2f   " % kp
        for f in fits:
            g = decay_at(kp, kP_now, f, [-sigma, wd])
            line += "  ---    ---   ---  " if g is None else "  %.3f  %.2f  %.3f " % (g['r'], g['T'], g['zeta'])
        print(line + "   %.2fx" % (kp / kP_now))
    print("    'dither' = residual throttle motion vs today: the P term multiplies the")
    print("    ignition PID's cycle-to-cycle jitter, so it scales linearly with kP.")

    # 5 --------------------------------------------------------------- settled residual
    if a.settled:
        m = (t >= a.settled[0]) & (t <= a.settled[1])
        print("\n[5] settled band %.0f..%.0f s" % tuple(a.settled))
        print("    RPM  %6.0f +- %-5.1f (p-p %3.0f)" % (rpm[m].mean(), rpm[m].std(), np.ptp(rpm[m])))
        print("    air%% %6.1f +- %-5.2f (p-p %4.1f)" % (air[m].mean(), air[m].std(), np.ptp(air[m])))
        print("    ign  %6.2f +- %-5.2f (p-p %4.1f)   <- should sit on idleIgnitionTargetTbl"
              % (ign[m].mean(), ign[m].std(), np.ptp(ign[m])))
        print("    sd(air%%)/sd(ign) = %.2f   vs kP = %.2f  %s"
              % (air[m].std() / ign[m].std(), kP_now,
                 "-> residual wander IS the P term amplifying ignition jitter"
                 if abs(air[m].std() / ign[m].std() - kP_now) < 0.5 * kP_now else ""))


if __name__ == '__main__':
    main()
