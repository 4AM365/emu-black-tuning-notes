"""Idle target-tracking + stability from RPM — the right combustion-stability proxy AT IDLE.

GOAL: idle should TRACK TARGET tightly EVERYWHERE (cold high-idle through warm), so we
measure error vs the commanded `Idle target`, per setpoint, in both thermal regimes.

WHY RPM, NOT KNOCK, AT IDLE
---------------------------
At idle, cylinder pressure is low, so knock ring-down energy is tiny and buried in
injector/valvetrain noise — knock CoV at idle measures mechanical noise, not combustion.
Crank-speed fluctuation is the classic idle combustion-stability proxy (OBD-II misfire
detection works this way): each cylinder's torque impulse accelerates the crank.

TWO METRIC FAMILIES
-------------------
  TRACKING (vs target)            STABILITY (scatter)
  - bias   = mean(RPM - target)   - hold_CoV  = std(RPM)/mean      (hunting + jitter)
  - RMS err= sqrt(mean(e^2))      - jitter_CoV= std(RPM-trend)/mean (fast only)
  - %within +/-25, +/-50 rpm      - hunt_Hz   = dominant RPM-PSD peak (hunting limit cycle)
  CoV-around-own-mean forgives a steady offset from target; RMS error does NOT. Report both.

OEM YARDSTICK
-------------
Steady warm idle holds ~+/-20-50 rpm of target (std ~10-15 rpm, CoV ~1.5-2%, COV-of-IMEP
<5%). >10% COV-of-IMEP is the perceived-roughness limit. Transients (AC, gear engage) get a
bigger momentary excursion but should settle in ~1-2 s without hunting.

SAMPLE-RATE WALL
----------------
Idle firing freq (6-cyl 4-stroke @ ~1000 rpm) ~= 50 Hz. A 25 Hz log (Nyquist 12.5 Hz)
aliases per-firing content into the low band, so hold/jitter CoV = idle QUALITY, NOT a
COV-of-IMEP number. 100 Hz exports (Nyquist 50 Hz) sharpen the hunting PSD but still can't
give honest per-cycle combustion CoV.

THERMAL REGIME
--------------
warm vs warmup is decided by CLT when logged (>= WARM_CLT), else by `Idle target` relative
to the log's lowest steady target (high target == cold). Both regimes are reported; nothing
is thrown away. Per-target-band table shows tracking AT EACH commanded setpoint.

STEADINESS GATE: by RPM slew rate (not closeness to target), so a steady-but-OFFSET idle is
kept (it's a tracking miss we want to see) while returns/flares are excluded.

Run:    python supra/scripts/idle_stability.py
Output: per-target-band + per-regime tables, and supra/scripts/idle_stability.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- config -------------------------------------------------------------------
OD = r"C:/Users/WTCra/OneDrive/Documents/EMU_BLACK_V3/Supra"
ODL = OD + "/LogAutosave"

LOGS = [
    ("idle_v3_tune",      "supra/logs/idle_log_v3_tune.csv"),
    ("more_idle_returns", "supra/logs/more_idle_returns.csv"),
    ("drive_wobble",      "supra/logs/drive_wobble.csv"),
]

TPS_MARGIN     = 1.5    # %  above auto-detected closed-throttle TPS still "closed"
TPS_CLOSED_PCT = 2.0    # percentile estimating closed-throttle TPS
VSS_MAX        = 2.0    # <= this is stationary
RPM_LO, RPM_HI = 550, 2000   # absolute idle/high-idle sanity window
RATE_MAX       = 300.0  # rpm/s; |dRPM/dt| above this = transient (return/flare) -> excluded
RATE_K         = 3      # samples for the rate estimate (~0.12 s @ 25 Hz)
MIN_SEG_S      = 4.0    # minimum steady stretch
GAP_BRIDGE_S   = 0.5    # bridge sub-blip breaks
TREND_S        = 1.0    # rolling-mean window defining "slow drift" for jitter
WARM_CLT       = 80.0   # degC; CLT >= this == warm (when CLT logged)
TGT_WARM_MARGIN= 100.0  # rpm; target <= min_steady_target + this == warm (CLT fallback)
WARN_RATE_HZ   = 40.0

NUMCOLS = ["TIME", "RPM", "Idle target", "TPS", "Vehicle Speed", "CLT", "Charge temp"]


def load(path):
    df = pd.read_csv(path, sep=";", decimal=".", low_memory=False)
    for c in NUMCOLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def sample_rate(df):
    dt = np.median(np.diff(df["TIME"].values))
    return (1.0 / dt if dt > 0 else np.nan), dt


def steady_mask(df, tps_closed, dt):
    m = pd.Series(True, index=df.index)
    if "TPS" in df:
        m &= df["TPS"] <= tps_closed + TPS_MARGIN
    if "Vehicle Speed" in df:
        m &= df["Vehicle Speed"].fillna(0).abs() <= VSS_MAX
    m &= df["RPM"].between(RPM_LO, RPM_HI)
    if "Idle target" in df:
        m &= df["Idle target"].notna()
    # slew-rate gate: settled, not mid-transient
    tdt = df["TIME"].diff(RATE_K)
    slew = (df["RPM"].diff(RATE_K) / tdt.where(tdt > 0)).abs()
    m &= slew.fillna(0) <= RATE_MAX
    return m.fillna(False)


def runs(mask, dt):
    bridge = max(1, int(round(GAP_BRIDGE_S / dt)))
    idx = np.where(mask.values)[0]
    if len(idx) == 0:
        return []
    out, s, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev <= bridge:
            prev = i
        else:
            out.append((s, prev)); s = prev = i
    out.append((s, prev))
    minlen = int(round(MIN_SEG_S / dt))
    return [(a, b) for a, b in out if (b - a + 1) >= minlen]


def welch_psd(x, fs, nperseg=None):
    x = np.asarray(x, float); x = x - x.mean(); n = len(x)
    if n < 16:
        return np.array([]), np.array([])
    nperseg = int(min(256, n) if nperseg is None else nperseg)
    step = max(1, nperseg // 2); win = np.hanning(nperseg)
    scale = 1.0 / (fs * (win ** 2).sum())
    starts = list(range(0, n - nperseg + 1, step)) or [0]
    acc = None
    for st in starts:
        seg = x[st:st + nperseg] * win
        if len(seg) < nperseg:
            seg = np.pad(seg, (0, nperseg - len(seg)))
        p = np.abs(np.fft.rfft(seg)) ** 2 * scale
        acc = p if acc is None else acc + p
    return np.fft.rfftfreq(nperseg, 1.0 / fs), acc / len(starts)


def dom_freq(x, fs):
    f, p = welch_psd(x, fs)
    if len(f) == 0:
        return np.nan, f, p
    band = (f >= 0.1) & (f <= fs / 2)
    if not band.any():
        return np.nan, f, p
    return f[band][int(np.argmax(p[band]))], f, p


def metrics(e, rpm):
    e = np.asarray(e, float); rpm = np.asarray(rpm, float)
    mu = np.nanmean(rpm)
    return dict(n=len(e), mean_rpm=mu,
                bias=np.nanmean(e), rms=np.sqrt(np.nanmean(e ** 2)),
                std=np.nanstd(rpm),
                p25=100 * np.nanmean(np.abs(e) <= 25),
                p50=100 * np.nanmean(np.abs(e) <= 50),
                cov=100 * np.nanstd(rpm) / mu if mu else np.nan)


def analyse(label, path):
    if not os.path.exists(path):
        print(f"  {label}: missing"); return None
    df = load(path)
    if "RPM" not in df or "Idle target" not in df:
        print(f"  {label}: missing RPM/Idle target"); return None
    fs, dt = sample_rate(df)
    tps_closed = (np.nanpercentile(df["TPS"], TPS_CLOSED_PCT)
                  if "TPS" in df and df["TPS"].notna().any() else 0.0)
    segs = runs(steady_mask(df, tps_closed, dt), dt)
    if not segs:
        print(f"  {label}: no steady idle segments (fs={fs:.0f}Hz, closedTPS~{tps_closed:.1f}%)")
        return None

    has_clt = "CLT" in df and df["CLT"].notna().any()
    min_tgt = min(df["Idle target"].iloc[a:b + 1].median() for a, b in segs)

    rows, trend_win = [], max(3, int(round(TREND_S / dt)) | 1)
    longest = {"warm": None, "warmup": None}
    for (a, b) in segs:
        seg = df.iloc[a:b + 1]
        rpm = seg["RPM"].astype(float).values
        tgt = seg["Idle target"].astype(float).values
        if len(rpm) < trend_win:
            continue
        clt = float(np.nanmedian(seg["CLT"])) if has_clt else np.nan
        warm = (clt >= WARM_CLT) if has_clt else (np.nanmedian(tgt) <= min_tgt + TGT_WARM_MARGIN)
        regime = "warm" if warm else "warmup"
        e = rpm - tgt
        trend = pd.Series(rpm).rolling(trend_win, center=True, min_periods=1).mean().values
        dur = seg["TIME"].iloc[-1] - seg["TIME"].iloc[0]
        rows.append(dict(regime=regime, dur=dur, clt=clt,
                         tgt_band=int(round(np.nanmedian(tgt) / 50.0) * 50),
                         rpm=rpm, tgt=tgt, e=e, resid=rpm - trend, mean_rpm=np.nanmean(rpm)))
        if longest[regime] is None or dur > longest[regime]["dur"]:
            longest[regime] = dict(dur=dur, resid=rpm - trend)
    return dict(label=label, fs=fs, has_clt=has_clt, rows=rows, longest=longest)


def pool(rows, key=None, val=None):
    sel = [r for r in rows if (key is None or r[key] == val)]
    if not sel:
        return None
    e = np.concatenate([r["e"] for r in sel])
    rpm = np.concatenate([r["rpm"] for r in sel])
    m = metrics(e, rpm)
    m["dur"] = sum(r["dur"] for r in sel)
    clts = [r["clt"] for r in sel if not np.isnan(r["clt"])]
    m["clt"] = np.mean(clts) if clts else np.nan
    # jitter (fast) CoV from residuals
    resid = np.concatenate([r["resid"] for r in sel])
    m["jit"] = 100 * np.nanstd(resid) / m["mean_rpm"] if m["mean_rpm"] else np.nan
    return m


def main():
    print("Idle target-tracking + stability (RPM)\n")
    results = [r for r in (analyse(l, p) for l, p in LOGS) if r and r["rows"]]
    if not results:
        print("No usable steady idle segments."); return

    for r in results:
        print(f"\n#### {r['label']}   (fs={r['fs']:.0f} Hz"
              f"{', CLT logged' if r['has_clt'] else ', no CLT -> target-based regime'})")
        # per thermal regime
        print(f"  {'regime':8s}{'time_s':>8s}{'meanCLT':>8s}{'mean_rpm':>9s}"
              f"{'bias':>7s}{'RMSerr':>8s}{'std':>6s}{'±25%':>7s}{'±50%':>7s}{'jitCoV':>8s}{'hunt_Hz':>9s}")
        for reg in ("warmup", "warm"):
            m = pool(r["rows"], "regime", reg)
            if not m:
                continue
            lg = r["longest"][reg]
            hz = dom_freq(lg["resid"], r["fs"])[0] if lg else np.nan
            clt = f"{m['clt']:.0f}" if not np.isnan(m['clt']) else "  --"
            print(f"  {reg:8s}{m['dur']:8.1f}{clt:>8s}{m['mean_rpm']:9.0f}"
                  f"{m['bias']:+7.0f}{m['rms']:8.1f}{m['std']:6.1f}"
                  f"{m['p25']:6.0f}%{m['p50']:6.0f}%{m['jit']:7.2f}%{hz:9.2f}")
        # per commanded target band
        bands = sorted({r2["tgt_band"] for r2 in r["rows"]})
        print(f"  {'target':>8s}{'time_s':>8s}{'mean_rpm':>9s}{'bias':>7s}{'RMSerr':>8s}{'±25%':>7s}{'±50%':>7s}")
        for tb in bands:
            m = pool(r["rows"], "tgt_band", tb)
            print(f"  {tb:8d}{m['dur']:8.1f}{m['mean_rpm']:9.0f}{m['bias']:+7.0f}"
                  f"{m['rms']:8.1f}{m['p25']:6.0f}%{m['p50']:6.0f}%")

    if any(r["fs"] < WARN_RATE_HZ for r in results):
        print(f"\n* fs < {WARN_RATE_HZ:.0f} Hz: idle firing ~50 Hz aliases below Nyquist. "
              f"CoV/jitter = idle QUALITY, not COV-of-IMEP. Export 100 Hz to sharpen hunt PSD.")

    # ---- plot: per-target RMS error + PSD ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.4))
    for r in results:
        bands = sorted({x["tgt_band"] for x in r["rows"]})
        rms = [pool(r["rows"], "tgt_band", tb)["rms"] for tb in bands]
        ax1.plot(bands, rms, "o-", label=r["label"])
    ax1.axhspan(0, 25, color="green", alpha=.08); ax1.axhspan(25, 50, color="gold", alpha=.08)
    ax1.set_xlabel("Commanded idle target (rpm)"); ax1.set_ylabel("RMS tracking error (rpm)")
    ax1.set_title("Target-tracking error per setpoint (green <±25, gold ±25–50)")
    ax1.legend(fontsize=8); ax1.grid(alpha=.3)
    for r in results:
        for reg in ("warmup", "warm"):
            lg = r["longest"][reg]
            if lg:
                hz, f, p = dom_freq(lg["resid"], r["fs"])
                if len(f):
                    ax2.semilogy(f, p, label=f"{r['label']}/{reg} ({hz:.2f}Hz)")
    ax2.set_xlim(0, min(15, max(r["fs"] for r in results) / 2))
    ax2.set_xlabel("Frequency (Hz)"); ax2.set_ylabel("RPM PSD (rpm^2/Hz)")
    ax2.set_title("Idle RPM spectrum — peak = hunting frequency")
    ax2.legend(fontsize=7); ax2.grid(alpha=.3)
    fig.tight_layout()
    out = "supra/scripts/idle_stability.png"
    fig.savefig(out, dpi=130)
    print(f"\nplot -> {out}")


if __name__ == "__main__":
    main()
