---
name: emu-black-tune-review
description: >-
  Performs a comprehensive review of an EMU Black tune file (.emub3 / .xml)
  against best-practice references (Banish, Hartman, Heywood) and EMU Black's
  own architecture conventions. Use this whenever the user asks to "review my
  tune", "audit the calibration", "what could be improved", "look over the
  whole tune", or wants a sanity check across all functional areas of their
  build. Produces a structured report categorising findings as
  Validated / Worth-discussing / Verification-gap, with citations and
  prioritised action items. Pairs with emu-black-tune for the decoding side.
---

# EMU Black tune review

Reviews a tune against codified checks derived from the academic and
practitioner literature, plus EMU Black architecture conventions.

## When to invoke

- "Review my tune", "audit the calibration", "look it over"
- "What could be improved on this tune?"
- "Sanity check my settings"
- After importing a fresh tune export, before making changes

Do NOT invoke for:
- Single-table edits (use `emu-black-tune` + `emu-black-emubt-export`)
- Active troubleshooting of a specific symptom (use `emu-black-log` for log analysis)

## What the review covers

The skill walks through these categories. Each produces 0+ findings.

### Idle / cranking

- **PID limit asymmetry / saturation risk** — does `idleAirPIDOutMin/Max` give symmetric authority?
  Is `idleAirFlowIntegralLimitMin/Max` narrower than the PID output limit (which Banish recommends)?
- **Idle ignition reserve** — is `idleIgnitionTargetTbl` set above the base ignition cells at idle MAP/RPM
  (per Hartman/Banish reserve-of-torque principle)?
- **Cranking airflow vs idle airflow** — is cranking airflow within 1.0–1.75× of idle airflow demand
  (per RusEFI / general practitioner guidance)? Bigger gaps suggest a step in the handoff.
- **Armed-state airflow ramp** — does it taper smoothly from high-RPM bins toward idle airflow at the
  low-RPM bins?
- **Cold-CLT enrichment shape** — does `crankingCorrTbl` decay to zero by typical warm CLT?
  Are warm-bin values modest (typical 10–30% at 17–34°C)?
- **Brake-switch lockout risk** — if a brake input is always-on or noisy, idle PID gets stuck in
  open-loop. Hard to detect from tune alone; flag for log review.

### Lambda targets

- **Cruise zone (40–80 kPa, 2500–4000 RPM)** — Banish (p.1605) recommends λ ≈ 1.0–1.05 for economy.
  Flag if cells in this zone read < 0.95 (leaving fuel economy on the table) or > 1.07 (lean misfire risk).
- **Idle zone (< 50 kPa, < 1500 RPM)** — Banish (p.3062): λ 0.85–1.0 is typical, slightly rich gives
  stability for cammed engines. Flag if < 0.85 (bore wash risk) or > 1.05 (unstable on big cams).
- **WOT / boost zone (> 100 kPa)** — λ 0.78–0.86 typical for E0 turbo. Richer on E25/E60 not always
  needed since ethanol's cooling already lowers cylinder temp.
- **Lambda blend curve shape (`tblsFFLambdaBlend`)** — should be smoothly monotonic from 100% at E0
  to 0% at E100. Discontinuities suggest a hand-edit that wasn't smoothed.
- **Warmup lambda correction** — if `warmupTblLambdaCorrTbl` is all zeros, warmup enrichment relies
  purely on VE enrichment which closed-loop trim may unwind once WBO comes online. Hartman recommends
  commanding richer lambda during cold operation explicitly.

### Ignition

- **Base idle ignition** — should be in the 8–20° BTDC range (Hartman p.17885), modest for the reserve.
- **Knock action min TPS** (`knockActionMinTps`) — if > 30%, part-throttle detonation isn't protected.
  Hartman/Banish recommend ≤ 25% (knock signal threshold prevents false trips at light load anyway).
- **Knock retard rate / restore** — typical 3–6°/cycle retard, 4–8°/cycle restore (your fast cut, slow
  restore principle).
- **Knock per-cylinder gains** — should match for active cylinders (cyl 1–6 on inline-6) and be 0 for
  disabled cylinder slots.
- **Ignition flex blend curve** — should be smooth, similar shape to the lambda blend curve.

### Boost

- **Boost PID enabled** — `boostPIDEnable`. If 0 with `boostControlType > 0`, the user is running
  open-loop boost (DC table only). Flag explicitly since this is often unintentional.
- **Boost PID gains plausibility** — KP/KI/KD all zero with PID enabled = nothing happens.
- **Overboost protection** — `boostCutOverboostLimit` and duration. Conservative: +15–25 kPa over
  target, 200–500 ms. Flag if disabled (limit = 0 or off).
- **Wastegate solenoid frequency** — typical 33 Hz or 25 Hz for standard MAC valves. Out-of-range
  frequency causes erratic boost control.

### Acceleration / transient enrichment

- **`accEnrichment` table shape** — should grow with TPS rate-of-change, fall toward zero at high RPM.
- **`accEnrichmentAsync`** — if all −100, async branch is disabled (intentional or vestigial).
- **`accEnrichCustomCorr`** — if all zeros, no MAP/load-based correction applied.

### Sensors / safety

- **`rpmLimit`** — should match the engine's mechanical limit, not above it.
- **`fuelPressureFailSafe`** — if very low (< 30 psi-equivalent), the engine could run on low rail
  pressure during a pump fault.
- **`mapValidVoltageMin`** — too low and a failing MAP sensor goes unnoticed.
- **Injector opening time table row variance** — if all 4 rows are identical, only one dimension
  (battery voltage) of dead-time compensation is active. Vacuum-referenced regulators benefit from a
  second dimension (rail pressure or differential).

### VVT (when configured)

- **Cam1 advance table** — should be smooth, not have any cell deltas > 10° between adjacent cells
  (suggests hand-edits that weren't smoothed). Without dyno data, flag the whole table as
  "verification gap" rather than prescribing values.

## Workflow

```bash
python scripts/review.py --tune <file.emub3> [--out-md <path>]
```

Produces a markdown report categorised by:
- **Validated as solid** — passes the check
- **Worth discussing** — fails a soft check, may be intentional, flag for user judgement
- **Verification gap** — requires dyno data or log data to validate (skill can't decide alone)

Each finding has:
- The symbol(s) involved
- The current value(s)
- The check that triggered
- The reference (Banish p.X, Hartman p.Y, Heywood ch.Z, or "EMU Black architecture")
- A suggested action (with explicit recommended values where appropriate)

## Output style

The report deliberately does NOT prescribe a single "correct" tune. It flags things that diverge
from documented best practice and explains the trade-off. The user makes the call.

When the tune is clean (most checks pass), the report should be short — that's a positive sign.

## Limitations

- **No log data** — many checks would benefit from a log to confirm whether a setting is causing
  symptoms. Pair with `emu-black-log` if a log is available.
- **No dyno data** — VE, ignition advance, and lambda WOT targets are inherently dyno-dependent.
  The skill flags ranges, not optimal values.
- **Reference values evolve** — the codified thresholds reflect 2024–2026 practitioner consensus.
  Re-check the source citations if anomalous findings surface.

## Related skills

- **`emu-black-tune`** — decoding side (this skill calls into it conceptually for parsing).
- **`emu-black-log`** — if a log is available, cross-correlate findings.
- **`emu-black-actuator-rescale`** — if the review flags PID limits and an actuator range change is
  the underlying cause, that skill handles the rescale.
