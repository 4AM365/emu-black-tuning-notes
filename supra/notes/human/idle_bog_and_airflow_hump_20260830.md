# Idle bog + airflow hump, 2026-08-30 — digest

*Digest of [`../idle_bog_and_airflow_hump_20260830.md`](../idle_bog_and_airflow_hump_20260830.md).
The canonical note wins. Adversarial verification never ran — single-pass measurement.*

## What this covers

Why the car still bogged on return-to-idle, and why the settled hot-idle airflow requirement
appeared to "walk up then settle back down."

## The rules

- **The bog is subtraction, not deficit.** Four things pull air out during one descent: the
  clutch-release target cliff (−200), the A/C-disengage cliff (−185), `Idle force open loop`
  chatter, and the DBW plate held on its close floor ~0.5 s too long.
- **The clutch cliff is dishonest.** In neutral the driveline was already decoupled, so releasing
  the pedal changes no engine load — but the ECU deletes 200 rpm of setpoint and ~9 airflow points
  anyway. The fall rate quadruples at that instant while MAP and estimated airflow slide smoothly
  through it. The A/C cliff *is* honest (the compressor really unloaded).
- **Gear detection cannot see neutral, and never will.** It is ratio-based, so a decoupled coast
  sweeps the ratio through every gear. Cleaning the speed signal does not fix this.
- **Any exit from `Idle state` 2 zeroes both PIDs** — a force-open-loop blip *or* a pedal tap. So
  rescuing a bog with a throttle blip makes the next dip worse.
- **The "hump" is the oil-pressure table fighting the PID.** The engine's requirement is flat
  against oil pressure; the table removes ~3.9 points/bar and the PID puts back ~3.9. The hump you
  see lives in the PID channel, not in the engine.
- **The old 5.45 %/bar oil slope is not reproduced.** In a single warm-up drive every candidate is
  monotone in time (r ≈ −0.99), so no oil coefficient is identifiable — it flips sign depending on
  what you condition on.
- **The real requirement declines slowly with time-hot**, ~0.2–0.4 %/min, with discrete ±5–7 point
  excursions. No single base value covers that swing; let the PID absorb it.

## Key numbers

Target arithmetic: entry 1957 = base 1225 + ramp 347 + clutch 200 + A/C 185. Fall rate at clutch
release **−158 → −683 rpm/s**. **51** target drops in the drive, all 175–205, median RPM drop
**361**, worst one is the stall. Oil-table vs PID slopes: **+3.88 / −3.91 %/bar → net +0.01**.
`idleAirFlowKP` = 717/1024 = **0.7002**; integral limits recovered as **−4 / +12**; PID ceiling is
P+I = **23.9**, not `idleAirPIDOutMax`. Airflow→TPS: **TPS = 2.4 + 5.6 × airflow%/100**. After the
final edits: min ACTIVE RPM **835**, zero sub-800 — versus min **298** before.

## When to care

Any return-to-idle complaint, any time you are tempted to raise base airflow to cure a dip, and
before trusting an oil-pressure-indexed idle correction. Also read before adding any target
increase — every one of them is a cliff on the way back down.
