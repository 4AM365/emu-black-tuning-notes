---
name: emu-black-actuator-rescale
description: >-
  Rescales every airflow-% table in an EMU Black tune when the idle DBW
  actuator range [floor, ceiling] changes, preserving the actual throttle
  position at each cell. Use this whenever the user changes
  idleDBWTargetMin or idleDBWTargetMax (e.g. floor 3.5%→2.4% or back),
  or asks to "rescale the airflow tables" / "move the actuator floor" /
  "preserve TPS after widening the range". Outputs a folder of
  importable .emubt files plus a per-cell summary report. Knows which
  symbols use preserve-TPS rule, additive (slope-only) rule, or PID
  width-scaling — and which to flag (overrun, ALS, launch, pit limiter)
  because their behavior depends on whether the feature is actually used.
  Pairs with emu-black-tune (decode side) and emu-black-emubt-export
  (write side).
---

# EMU Black Actuator Rescale

The idle DBW actuator range `[idleDBWTargetMin, idleDBWTargetMax]` defines the
TPS band into which every airflow-% value is mapped:

```
TPS%     = floor + (airflow% / 100) × (ceiling − floor)
airflow% = (TPS% − floor) / (ceiling − floor) × 100
```

Changing the floor or ceiling reinterprets every stored airflow-% value
against the new range — the plate moves even though the tables are untouched.
This skill rescales the tables so behavior is preserved at every cell.

## When to invoke

- User says "rescale the airflow tables to a new range"
- User changes `idleDBWTargetMin` and/or `idleDBWTargetMax`
- User mentions floor or ceiling values in % (e.g. "move the floor from 3.5 to 2.4")
- User asks "what happens to my airflow tables if I widen the range?"

Do NOT invoke for:
- Changes to individual cells of one table (use `emu-black-emubt-export` directly)
- Changes to PID gains alone (this skill scales them as a side-effect, but it's not
  the primary use case)

## Rescale rules

Given old range `[f_old, c_old]` and new range `[f_new, c_new]`:

```python
B = (c_old - f_old) / (c_new - f_new)        # slope (width ratio)
A_pct = (f_old - f_new) / (c_new - f_new) * 100   # offset in display %
```

Per-symbol formula selection:

| Symbol class | Examples | Rule | Math |
|---|---|---|---|
| **Absolute airflow-% target** | `idleActiveAirflow`, `idleArmedAirFlow`, `overrunDBW`, `lcDBWTargetTable`, `alsDBWTarget`, `ralDBWTarget`, `pitLimiterDBWLimit`, `cyclingIdleAirflow` | preserve-TPS | `new% = A_pct + B × old%` |
| **Cranking airflow** | `idleCrankingDC` | preserve-TPS by default (or set directly to a desired TPS) | same as above |
| **Additive correction** (delta in airflow-%) | `idleCustomCorrection` (when in additive mode) | width-ratio only | `new = old × B` |
| **PID output (delta in airflow-%)** | `idleAirFlowKP`, `idleAirFlowKI`, `idleAirFlowKD`, `idleAirFlowIntegralLimitMin/Max`, `idleAirPIDOutMin/Max` | width-ratio scaling | `new = old × B` (gain) or `old × B` (limits) |
| **Range floor/ceiling scalars** | `idleDBWTargetMin`, `idleDBWTargetMax` | direct write | `new = TPS_new_floor × 10` (word @ 0.1/count) |

Cells that would map to TPS below `f_new` get clamped to 0% airflow.
Always report clamping events so the user can decide whether to override.

## Cautions / non-rescaled

These symbols are NOT rescaled by this skill — they need user judgement:

- **`idleCustomCorrection` in multiplicative/scalar mode** — a multiplier is
  dimensionless and range-independent. Skip width-scaling. The skill cannot
  detect mode automatically; ask the user or default to additive and flag.
- **Cells that would clamp under the new floor** — flag with a warning. The
  user may want to override (e.g. ALS targets want throttle nearly closed;
  raising the floor breaks them).
- **`dbwBoostTargetLimit`, `dbwCLTLimitTable`** — units unclear (could be
  airflow-% or raw TPS%). Confirm before rescaling.
- **`tpsCrankingBins`** — TPS-axis, scale 0.1, not airflow-% — do not rescale.

## Workflow

```bash
python scripts/rescale.py \
  --tune "supra/tunes/supra tune export 05242026.xml.emub3" \
  --old-range 2.4 8.0 \
  --new-range 3.5 8.0 \
  --out-dir "supra/exports/rescaled_3.5_8.0"
```

The script:
1. Reads the tune and decodes every airflow-% symbol
2. Applies the right rule per symbol class
3. Writes one `.emubt` per symbol into `--out-dir` (filenames match EMU's display titles)
4. Writes `summary.md` with per-cell old → new tables and clamp warnings
5. Updates `idleDBWTargetMin/Max` in a separate `range_scalars.emubt`

To selectively skip motorsport-mode targets that would all clamp:
```bash
python scripts/rescale.py ... --skip-symbols alsDBWTarget,alsDBWTarget2,lcDBWTargetTable,ralDBWTarget,pitLimiterDBWLimit
```

To preserve cranking at specific TPS targets rather than rescale:
```bash
python scripts/rescale.py ... --crank-tps "5.0 4.5 4.0 3.7"
```
(TPS targets for `cltBins4` order: 0/33/67/100°C)

## Verification

After import, log a few seconds of stable hot idle and check:
- `Idle air %` should be a different number than before, but
- Actual `TPS` should be the same as before (preservation of behavior)
- `Idle PID air % correction` should be similar magnitude (PID gain was width-scaled)

A 1–2% TPS drift is normal (rounding in the rescale + closed-loop reacquisition).
Larger drift means a symbol class was misidentified.

## Safety

- **Worktree-equivalent practice**: rescale into a separate `--out-dir`, don't
  overwrite previous exports.
- **Verify scalars first.** Importing the rescaled `idleActiveAirflow` without
  also updating `idleDBWTargetMin` produces wrong behavior — the airflow values
  map into the OLD range, putting the throttle in the wrong physical position.
  Always import the range scalars together with the table changes (or use the
  combined `.emubt` if EMU's importer supports multi-symbol files).
- **Re-verify a representative cell** in EMU after import: pick the hot idle
  cell, multiply `raw × 0.5` to get display %, compute `TPS = f_new + display%/100 × (c_new − f_new)`,
  and compare to the previous-range TPS at the same cell. They must match within
  rounding (±0.05% TPS).
