---
name: emu-black-idle-stability
description: >-
  Measures idle quality from an EMU Black CSV log using crank-speed (RPM) — the
  correct combustion-stability proxy at idle (knock is useless at idle). Use whenever
  the user wants to "check my idle stability", "is my idle hunting", "how well does
  idle hold target", "idle RPM CoV", "idle quality", "is my idle good", or is
  comparing idle before/after a change. Auto-detects steady idle segments (closed
  throttle, stationary, low slew-rate), then reports tracking (bias, RMS error vs
  Idle target, % within ±25/±50 rpm) and stability (hold/jitter CoV, hunting
  frequency from the RPM PSD), split by thermal regime and by commanded target
  setpoint. Takes any log(s) as arguments (not vehicle-specific); optional PSD/RMS
  plot. Pairs with emu-black-idle-drift (hot-soak drift attribution).
---

# EMU Black idle stability / target-tracking

At idle, cylinder pressure is low so knock ring-down is buried in mechanical noise —
**crank-speed fluctuation** is the right combustion-stability proxy (it's how OBD-II
misfire detection works). This auto-detects steady idle and reports two metric
families:

- **Tracking** (vs commanded `Idle target`): `bias`, `RMS error`, `% within ±25/±50 rpm`
- **Stability** (scatter): `hold CoV`, `jitter CoV` (fast residual), `hunt_Hz` (dominant
  RPM-PSD peak = the hunting limit cycle)

Reported per **thermal regime** (warm vs warmup, by CLT or by target) and per
**commanded target setpoint** — so a steady-but-offset idle (a tracking miss) is kept,
while returns/flares are excluded by a slew-rate gate.

## Usage

```bash
python scripts/idle_stability.py LOG.csv [LOG2.csv ...] [--plot out.png]
```

- Requires `pandas` + `numpy`; `--plot` additionally needs `matplotlib`.

## Reading the result

- **OEM yardstick:** steady warm idle holds ±20–50 rpm (std ~10–15 rpm, CoV ~1.5–2 %).
- **Good average tracking but high scatter dominated by a sub-Hz hunt** (jitter small)
  = an idle-**PID limit cycle**, not combustion — fix the controller, not fueling.
- **A steady bias only at an elevated warmup setpoint** = idle-air feed-forward/PID
  authority falling short at the higher target.
- **Sample-rate wall:** idle firing ≈ 50 Hz; a 25 Hz log (Nyquist 12.5 Hz) aliases
  per-firing content down, so hold/jitter CoV = idle *quality*, **not** COV-of-IMEP.
  Export 100 Hz to sharpen the hunt PSD.

## Related

- `emu-black-idle-drift` — attribute a slow hot-soak idle drift to PID vs charge-temp.
- Method background: `notes/idle.md`, `ai-analysis-skills/idle_rpm_cov_stability.md`.
