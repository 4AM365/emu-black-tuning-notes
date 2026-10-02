---
name: emu-black-idle-pid-gain
description: >
  Identify the idle **airflow** PID's stability margin from a logged oscillation and
  prescribe `idleAirFlowKP`. Use whenever an EMU Black log shows idle hunting, ringing
  after start, a decaying RPM/airflow swing, or a persistent low-level "walking around"
  at idle — and whenever the question is "what should kP actually be?". Measures the
  live kP straight out of the log, fits the plant, returns ultimate gain Ku, ultimate
  period Tu, current gain margin, and a decay-ratio-vs-kP table. Trigger on "idle
  oscillation", "idle hunt", "airflow PID gain", "kP too high", "how much should I drop
  kP", "idle rings after start". Distinct from emu-black-idle-stability (which scores
  RPM quality) and emu-black-idle-drift (which attributes slow hot drift).
---

# Idle airflow-PID gain identification

Turns a logged idle oscillation into a number for `idleAirFlowKP`. Everything below is
measured from the log — the only tune value you need is confirmation of the *current*
kP, and the script measures that too.

## Run it

```bash
python skills/emu-black-idle-pid-gain/scripts/idle_pid_gain.py LOG.csv --fit 8.0 13.0 --regress 6 30 --settled 45 70
```

- `--fit T0 T1` — the clean decaying cycles. **Want ≥3 full cycles**; the script prints
  the individual per-cycle decay ratios, and they should agree within ~0.05. If it
  reports `n=1`, widen the window.
- `--regress T0 T1` — window for measuring kP. Wider is fine.
- `--settled T0 T1` — residual-wander stats. Keep it **short (≈25 s)**: base airflow is
  CLT-scheduled, so over a long warm-up its drift inflates `sd(air%)` and corrupts the
  `sd(air%)/sd(ign)` check.
- `--auto` picks a fit window by largest ignition swing. Always eyeball the result.

Required channels: `TIME`, `RPM`, `MAP`, `Idle air %`, `Ignition Angle`. Only numpy.

## Why this works

In the EMU v3 cascade the airflow PID's error is **(Ignition Angle − Target ignition
angle)**, not RPM error ([`notes/idle.md` → P2](../../notes/idle.md)). So:

**1. kP falls out of a regression.** Regress `Idle air %` on `Ignition Angle`. The slope
*is* kP in %/deg. Base airflow only moves the intercept, and it drifts on the CLT
timescale — far slower than the oscillation — so it doesn't bias the slope. A high R²
also *proves* the loop is P-dominated, which is what licenses the pure-gain analysis
below. Check it: with `idleAirFlowKI` around 0.2 %/(°·s) and kP around 2, the P/I
crossover sits at KI/kP ≈ 0.1 rad/s — a 60 s period. Integral action is invisible at a
1.5 s oscillation.

**2. The decay gives the closed-loop pole.** From decay ratio `r` per cycle and period
`T`: log decrement `δ = ln(1/r)`, `ζ = δ/√(4π²+δ²)`, `ω_d = 2π/T`, `σ = −ln(r)/T`.

**3. The pole gives the plant.** Solve `(τs + 1) + K·e^(−Ls) = 0` at `s = −σ + jω_d`
for `(K, L)`, for several assumed `τ`. Then `Ku` from the phase crossover
`atan(ωτ) + ωL = π`.

**The τ-insensitivity is the whole trick.** Near the stability boundary the observed pole
pins down `kP/Ku` almost independently of how you split lag between `τ` and `L`. The
script prints the spread; under 0.05 means trust it. You do not need to know the plant
to know how close to the edge you are.

## Napkin version (no script)

Needs only the cycle count and a rough sense of how far it fell:

```
δ = ln(1/f) / n         f = fraction of amplitude left after n cycles
ζ = δ / 2π
kP/Ku ≈ 1 − δ/π         valid near the boundary only (ζ ≲ 0.15)
```

"Six cycles to die down into the noise" ⇒ f ≈ 0.25, n = 6 ⇒ δ = 0.231 ⇒ kP/Ku = 0.926.
The full solve on the same log gave 0.914. Good to ~1%.

Answering the common question directly: a **sustained** oscillation needs no amplitude —
that is Ziegler–Nichols, and kP *is* Ku. A **decaying** one does need amplitude, but
cycles-to-settle already encodes it, so counting cycles is enough.

## Choosing kP

The script prints decay ratio, period and ζ for a sweep of kP. Pick against the loop's
job, not against a textbook default:

| Target | kP | Behaviour |
|---|---|---|
| Ziegler–Nichols P-only | 0.50·Ku | quarter-amplitude decay; still visibly rings 2–3 cycles |
| Ziegler–Nichols PI | 0.45·Ku | as above, slightly softer |
| **Recommended for this loop** | **0.25–0.30·Ku** | one small overshoot, ζ ≈ 0.5–0.6 |
| Deadbeat | 0.20·Ku | no visible overshoot; slow to re-centre |

**ZN is too hot here.** Quarter-amplitude decay is a disturbance-rejection criterion for
a *primary* controller. The airflow PID is the outer half of a mid-ranging pair — its job
is slow re-centring of the ignition PID, and it should be boring. The fast lever already
exists.

Three things worth saying to whoever is applying the change:

- **Lower gain often settles *faster*.** At 91% of Ku the loop rings for 20+ s; at 0.3·Ku
  it is done in ~2 s.
- **Residual "walking around" is the same gain, not a separate fault.** The P term
  multiplies the ignition PID's normal cycle-to-cycle jitter into continuous throttle
  motion, which stirs RPM, which feeds the ignition PID. Check `sd(air%)/sd(ign)` in the
  settled band — if it ≈ kP, the wander *is* the P term, and it falls linearly with kP.
- **KI usually needs no change.** Cutting kP *raises* the P/I crossover, so relative
  integral authority goes up. The added phase lag at crossover is a few degrees —
  negligible against the gain removed.

## Cross-checks before recommending a number

- **Settled `Ignition Angle` should sit on `idleIgnitionTargetTbl`.** If it does, the
  cascade is working and only the gain is wrong. If it doesn't, something else is broken
  — fix that first.
- **Check the output ceiling.** Structural ceiling = `kP × max presentable ignition
  error` + `idleAirFlowIntegralLimitMax`. If the logged `Idle air %` swing approached it,
  the transient was clipping (the analysis window should avoid clipped cycles), and the
  ceiling was sized around the *old* kP — re-check it after the change. See
  [`supra/notes/airflow_actuator.md` → sizing `idleAirPIDOutMax`](../../supra/notes/airflow_actuator.md).
- **Re-read the live gains.** kP is verified by the log itself, but KI/KD/limits are not.
  Per repo convention, read them from the current XML rather than a remembered value —
  and if the newest binary postdates the newest XML, ask which was live.

## Failure modes

| Symptom | Meaning |
|---|---|
| Low R² in step [1] | Loop isn't P-dominated in that window — pure-gain analysis invalid. Check for a clipped/saturated transient, a state change, or a genuinely large KI. |
| `n=1` decay ratio | Too few cycles; widen `--fit` or lower `--minsep`. |
| Per-cycle ratios scattered | Window straddles a nonlinearity (output clipping, ignition hitting Min/Max torque angle) or a load disturbance. Move to smaller-amplitude cycles, which are more linear. |
| `kP/Ku` spread across τ > 0.05 | Not near the stability boundary; Ku is approximate. The method is weakest when the loop is already well damped — which is fine, because then you don't need it. |
| Period lengthens as amplitude decays | Amplitude-dependent gain — clipping or actuator rate limiting. Fit the *small* cycles. |

## Worked result — Supra, `cranking_channels_recent_run.csv` (2026-08-24)

Post-start idle, t = 5–137 s, idle state 2 throughout.

```
kP measured:  Idle air % = 11.97 + 1.976 × Ignition Angle,  R² = 0.816   -> kP = 1.98 %/deg
pole:         r = 0.800/cycle (n=3: 0.80 0.80 0.82),  T = 1.58 s,  ζ = 0.0355
FOPDT:        L ≈ 0.42–0.51 s;  kP/Ku = 0.907..0.918 across τ = 0.40..1.10 s
              -> Ku = 2.16 %/deg,  Tu = 1.50 s,  gain margin 0.8 dB
settled:      ign 17.99° ± 1.31 vs idleIgnitionTargetTbl 18.0°  (cascade healthy)
              sd(air%)/sd(ign) = 2.57 ≈ kP  (wander is the P term)
```

Conclusion: kP was at **91% of ultimate gain**. Not a comfort problem — a margin problem.
Recommendation was 0.6 %/deg (0.28·Ku): decay 0.013–0.031/cycle, ζ ≈ 0.48–0.62, one small
overshoot, and residual throttle dither cut to 0.30×.
