# Idle combustion stability: use RPM fluctuation, not knock voltage

## Why RPM, not knock, AT IDLE
Knock voltage is a boost-region tool. At idle, cylinder pressure is low → ring-down energy
is tiny → the knock packet is buried in injector/valvetrain/mechanical noise. CoV of knock
voltage at idle measures mechanical-noise repeatability, not combustion. The classic idle
combustion-stability proxy is **crankshaft-speed fluctuation** (it's how OBD-II misfire
detection works): each cylinder's torque impulse accelerates the crank, so cycle-to-cycle
RPM scatter tracks cycle-to-cycle work output. Flip the tool at idle.

## Two different "CoV at idle" — and the sample-rate wall
1. **Idle-hold quality / hunting** (sub-Hz .. ~12 Hz) — reachable, actionable for PID.
2. **True per-cycle combustion CoV** (COV-of-IMEP analogue) — NOT reachable from logged RPM.

Firing frequency, 6-cyl 4-stroke @ ~1000 rpm = **~50 Hz** (3 firings/rev × 16.7 rev/s).
- A **25 Hz** log (our autosave default, dt=0.040 s) has Nyquist **12.5 Hz**. Per-firing
  content is ABOVE Nyquist and **aliases down** into the low band, masquerading as slow
  hunting. Per-cycle combustion CoV is unrecoverable at 25 Hz.
- A **100 Hz** export (Nyquist 50 Hz) only just touches the firing fundamental — enough to
  clean up the hunting PSD, **not** enough for honest per-cycle combustion CoV.
- Crank-angle-resolved instantaneous crank speed (per-firing Δω) would be needed for true
  per-cycle / per-cylinder idle balance — EMU computes it internally but does NOT log it.

So RPM-hold CoV = idle QUALITY (valid, use it). It is NOT a COV-of-IMEP number.

## Goal: track target tightly EVERYWHERE (cold high-idle through warm)
Primary metric is **error vs commanded `Idle target`**, per setpoint, in both thermal regimes
— NOT CoV-around-own-mean (which forgives a steady offset from target).

## Metric definitions (script: `supra/scripts/idle_stability.py`)
Detect steady idle segments first, then measure inside:
- steady := TPS ≤ closed-throttle TPS + 1.5%  (closed TPS auto-detected ≈ **4.5%**, NOT 0 —
  TPS offset)  AND  VSS ≤ 2 (if logged)  AND  **|dRPM/dt| ≤ 300 rpm/s** (slew-rate gate keeps
  a steady-but-OFFSET idle, excludes returns/flares). Contiguous runs ≥ 4 s.
- TRACKING: `bias = mean(RPM − target)`, `RMS_err = sqrt(mean(e²))`, `%within ±25/±50 rpm`.
- STABILITY: `hold_CoV = std(RPM)/mean`, `jitter_CoV = std(RPM − 1 s trend)/mean`,
  `hunt_Hz` = dominant Welch-PSD peak (the hunting limit cycle).
- Regime: warm vs warmup by **CLT** when logged (≥ 80 °C), else by `Idle target` vs the log's
  lowest steady target. Both regimes reported; nothing dropped. `idle_v3` & `more_idle_returns`
  do NOT log CLT (only Charge temp); `drive_wobble` does.

## OEM yardstick
Steady warm idle holds **±20–50 rpm** of target (std ~10–15 rpm, CoV ~1.5–2 %, ~95 %+ within
±50). COV-of-IMEP < 5 % smooth, > 10 % = perceived-roughness limit.

## Result (idle_log_v3_tune, 25 Hz, 268 s steady; targets 1200 & 1250 — "warmest-in-log",
## not thermally hot: no CLT, charge temp only 30→62 °C)
| view | bias | RMS err | std | ±25 % | ±50 % | jitter | hunt |
|------|------|---------|-----|-------|-------|--------|------|
| overall | −7 | 40 rpm | 43 | 37 % | 79 % | 0.68 % | 0.59 Hz |
| @1200 tgt | +1 | 38 rpm | — | 39 % | 82 % | — | — |
| @1250 tgt | **−36** | 46 rpm | — | 30 % | 69 % | — | — |

**Read:**
- **Average tracking is good** (bias +1 at 1200) but **scatter is ~3× OEM**: std 43 vs OEM
  10–15, only 79 % within ±50 (OEM ~95 %+). Almost all of it is the **0.59 Hz hunt** —
  jitter (fast/combustion) is only 0.68 %. Fix = idle PID limit cycle, NOT combustion.
- **At 1250 there's a −36 rpm steady bias** (sits *below* target) — a real tracking offset at
  the higher setpoint, distinct from the hunt. Suggests idle-air feedforward/PID authority
  falls short at elevated warmup targets. Worth a look.
- Expected payoff: killing the 0.6 Hz hunt should pull std 43 → ~10–15 and ±50 coverage
  79 % → ~95 %, landing in OEM territory without touching fueling.

## Data-quality flags / next steps
- `more_idle_returns`: the "steady" 19.6 s sits **+186 rpm above target** (RMS 205) — post-return
  hangs, not controlled idle. Needs sustained-idle logs.
- `drive_wobble`: no steady idle (driving log) despite logging CLT.
- **100 Hz exports** sharpen the hunting PSD (Nyquist 50 Hz); still won't give per-cycle
  combustion CoV. Drop them in `LOGS` for a clean warm-vs-warmup, tune-to-tune comparison.
