# Idle combustion stability: use RPM fluctuation, not knock voltage

> **Car-specific values live in the build working docs**, not here. For the reference build's measured idle-stability results (the tracking/hunt result tables) see [`supra/notes/idle_rpm_stability_results.md`](../supra/notes/idle_rpm_stability_results.md). This note is intentionally car-agnostic: the metric definitions and method are universal; the specific log results live in the build doc.

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
- A **25 Hz** log (a common autosave default, dt=0.040 s) has Nyquist **12.5 Hz**. Per-firing
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

## Metric definitions
Detect steady idle segments first, then measure inside:
- steady := TPS ≤ closed-throttle TPS + 1.5%  (auto-detect the closed-TPS value per log — it is
  usually **not 0** because of the TPS offset)  AND  VSS ≤ 2 (if logged)  AND  **|dRPM/dt| ≤ 300 rpm/s** (slew-rate gate keeps
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

## How to read a result (illustrative pattern)
Run the metrics above on a steady-idle log and interpret the split between *tracking* and
*scatter*, and within scatter between *hunt* and *jitter*. A common diagnostic pattern:
- **Average tracking good, scatter several× OEM, dominated by a sub-Hz hunt** (jitter small).
  This is an idle-PID limit cycle, **not** combustion — fix the controller, not fueling.
  Killing the hunt should pull std and ±50-rpm coverage back toward OEM territory without
  touching fuel.
- **A steady bias (sits below target) that appears only at an elevated warmup setpoint**, distinct
  from the hunt — points to idle-air feedforward/PID authority falling short at the higher target.

For the reference build's actual measured numbers (bias, RMS, std, hunt frequency per setpoint)
see [`supra/notes/idle_session_05242026.md`](../supra/notes/idle_session_05242026.md).

## Data-quality flags / next steps
- A "steady" segment that sits well *above* target with high RMS is a post-return hang, not
  controlled idle — exclude it and capture sustained-idle logs instead.
- A pure driving log has no steady idle to measure even if it logs CLT.
- **100 Hz exports** sharpen the hunting PSD (Nyquist 50 Hz); still won't give per-cycle
  combustion CoV. Use them for a clean warm-vs-warmup, tune-to-tune comparison.
