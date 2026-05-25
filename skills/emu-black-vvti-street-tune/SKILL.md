---
name: emu-black-vvti-street-tune
description: >-
  Optimizes the VVT-i intake cam advance table on the street, without a
  dyno, using MAP-at-fixed-TPS as the primary torque proxy and EGT as a
  corroborating signal. Use this whenever the user asks to "tune VVT",
  "optimize cam advance", "find the best cam position", "tune cams
  without a dyno", or wants to populate / refine cam1AdvTbl entries.
  Provides: (1) a sweep plan generator that orders cells by which to test
  first, (2) a log analyzer that identifies steady-state cam-override
  windows in a recorded sweep and ranks cam positions by MAP, (3) a
  table-proposer that smooths a new cam1AdvTbl from multiple cell
  results. Pairs with emu-black-log (gates lambda/STFT signals behind
  WBO valid) and emu-black-tune (writes the resulting cam table).
---

# EMU Black VVT-i street tune

A dyno gives direct torque feedback per Banish (p.4552). On the street you have
to use proxies. The good news: with the right protocol, the proxies are good
enough for the cells you actually live in (cruise + light boost), and they
agree well enough with dyno results to be confidence-inspiring.

This skill provides the protocol, the analysis, and the table-write-back.

## When to invoke

- "Tune my VVT", "optimize the cam advance table", "find the best cam position"
- "Tune cams without a dyno"
- After populating an initial `cam1AdvTbl` from OEM defaults, to refine it
- After other significant tune changes that affect breathing (cams, manifold,
  intercooler) and you want to re-verify VVT optima

Do NOT invoke for:
- WOT-only cam tuning — torque accuracy and knock margin under boost still
  benefit from dyno. Use this skill for cruise and light-load cells; flag the
  high-boost cells as dyno-verification gaps.

## The torque proxies (street vs dyno)

| Signal | What it represents | When it's reliable |
|---|---|---|
| **MAP at fixed TPS** | Cylinder filling at a fixed throttle restriction. Higher MAP at the same TPS = more air per cycle = more torque potential. | Steady-state cruise: flat road, constant speed, no wind gusts. Use cruise control or a long highway stretch. |
| **EGT at fixed everything** | Combustion efficiency. Lower EGT at the same lambda + commanded ignition = more energy extracted as work. | Steady-state, after thermal soak (~30s at the operating point). |
| **Per-cylinder EGT spread** | Charge distribution uniformity. Tighter spread = cam position not biasing one cylinder. | Requires per-cylinder probes. Use as tiebreaker between close cam positions. |
| **STFT shift after cam change** | The VE table is now wrong at that cell — needs recorrection. | **Only valid after `Lambda is valid == 1`** (30–60s post-start). Don't try STFT-based VE work until you see the transition. |

**Commanded ignition is constant during a cam sweep at fixed (MAP, RPM)** —
the ignition table indexed cell doesn't change. MBT itself changes with cam
position, but you're not changing the commanded value. So "is ignition
optimized" is a property of the ignition table you already have, not a
confound in the sweep. The sweep finds the best cam for the current ignition
table; if you later re-optimize ignition, re-verify cam (second iteration).

**MBT shifts with cam position because residual gas fraction shifts.** The
direction depends on load:
- **At light load (vacuum)**: more cam advance → more overlap → exhaust gas
  blows back into the intake (because exhaust pressure > intake pressure) →
  more in-cylinder dilution → slower flame propagation → MBT shifts toward
  MORE advance.
- **Under boost**: more cam advance → more overlap → boost scavenges residuals
  out the exhaust during overlap (intake pressure > exhaust pressure) → less
  dilution → faster burn → MBT shifts toward LESS advance.
- At low RPM (any load), advancing the intake cam also closes IVC earlier
  which raises effective compression → faster burn → MBT toward LESS advance.

This means **the same cam-table cell can need opposite-direction ignition
re-tuning depending on whether it's a cruise cell or a boost cell.** When
following up a cam sweep with ignition optimization, treat cruise and boost
cells as separate problems. See `notes/vvti.md` for full mechanism.

## Cell priority (which to test first)

Test in this order — earlier cells give more drivability gain per session:

1. **Light cruise band**: MAP 40–80 kPa, RPM 2000–3500. This is where you spend
   most of the miles. Wins here = real fuel economy + smoother part-throttle.
2. **Off-idle / tip-in band**: MAP 30–60 kPa, RPM 1200–2000. Affects how
   quickly the engine "wakes up" off the line.
3. **Low-boost band**: MAP 100–140 kPa, RPM 3000–5000. Spool and mid-range
   acceleration.
4. **High-load WOT** — *flag for dyno*. Street protocol gives MAP as a torque
   proxy but knock margin and EGT ceiling matter more here than peak torque
   optimization.

## Protocol per cell

### Setup

- Engine fully warm (CLT > 80°C, charge temp stable).
- WBO has validated (`Lambda is valid == 1`) — wait at least 60s of driving
  before starting the sweep. *No exceptions* — STFT data before the gate is
  meaningless.
- Open-loop fuel is OK during the sweep (no closed-loop trim chasing). If
  your build runs closed-loop at the cell of interest, briefly disable it for
  the sweep.
- Per-cylinder EGT probes plugged in if you have them. Otherwise single bank
  EGT works.

### Execution

1. Get to the cell: cruise control on a flat highway is the cleanest approach.
   Lock to a speed that lands the engine at the target RPM and MAP in the
   gear you want to test.
2. Use EMU Black's VVT advance override to lock the cam at the first sweep
   position (e.g. 0°).
3. Hold for 15+ seconds. Log everything.
4. Step the override to the next position (+5°). Wait for MAP to settle (a
   couple seconds), then hold 15+ more seconds.
5. Continue through your sweep range (typically 0° to 40° in 5° steps for
   intake VVT-i).
6. **Repeat the first position at the end** as a drift check — if MAP at the
   re-test of position 0 differs from the initial position 0 by more than
   ~2 kPa, conditions changed (grade, headwind, etc.) and the sweep is
   contaminated. Re-do.

### After the drive

```bash
python scripts/analyze_sweep.py \
  --log path/to/sweep.csv \
  --cell-rpm 3000 --cell-map 70 \
  --cell-tolerance 200 5
```

The script identifies each cam-override hold, computes mean MAP and EGT per
hold, and ranks cam positions. Output:

```
Cell (MAP=70 ±5 kPa, RPM=3000 ±200):
  Cam   0°: MAP 68.2 kPa  EGT 712 °C  n=287 samples  std(MAP)=0.4
  Cam   5°: MAP 70.1 kPa  EGT 706 °C  n=304
  Cam  10°: MAP 72.4 kPa  EGT 698 °C  n=298
  Cam  15°: MAP 73.6 kPa  EGT 695 °C  n=311
  Cam  20°: MAP 73.2 kPa  EGT 696 °C  n=302
  Cam  25°: MAP 71.5 kPa  EGT 702 °C  n=295
  → Best cam position: 15° (MAP peak, EGT minimum agrees)
  → Drift check: cam 0° retest within 0.3 kPa of initial — sweep valid.
```

## Building the cam1AdvTbl from multiple cell sweeps

Repeat the protocol at 5–10 cells across the cruise band. Once you have a set
of (MAP, RPM, best_cam) tuples:

```bash
python scripts/propose_table.py \
  --sweeps cell1.json cell2.json cell3.json ... \
  --tune path/to/tune.emub3 \
  --out exports/cam1AdvTbl-refined.emubt
```

The script:
1. Reads `cam1AdvTbl` axis bins from the tune (`vvtiMapBins10`, `vvtiRpmBins10`)
2. Places each measured optimum into its nearest cell
3. Bilinearly interpolates between measured cells to fill the table
4. Smooths to prevent step discontinuities (Banish: VVT table should be
   visually smooth — sharp deltas suggest bad sweep data)
5. Holds out cells far from any measurement (typically WOT) and emits them
   unchanged with a "verification-gap" flag

## Constraints and caveats

- **Cruise control is your friend.** Without it, holding fixed throttle for
  60+ seconds across multiple cam positions is hard.
- **Repeat the sweep.** Once is data, twice is confirmation, three times tells
  you the noise floor.
- **STFT-based VE recorrection is a separate step.** After changing the cam
  table, the VE table at the changed cells will be wrong (different air mass
  trapped per cycle). Drive normally with closed-loop active (and Lambda
  valid) and let STFT show you which cells need VE adjustment. That's a job
  for `emu-black-log`'s VE-trim workflow, not this skill.
- **WOT verification still wants dyno.** Knock margin and EGT ceiling at peak
  load matter more than peak torque optimization. Don't optimize WOT cells
  via this method without a tow.

## Related skills

- **`emu-black-log`** — gates lambda/STFT signals correctly; provides the
  follow-on VE-recorrection workflow.
- **`emu-black-tune`** — for reading/writing the cam advance table.
- **`emu-black-emubt-export`** — used by `propose_table.py` to write the
  output .emubt.
- **`emu-black-tune-review`** — previously flagged VVT as a dyno-only
  verification gap. After this skill is run, the cruise cells of the VVT
  table become "validated on the street, see emu-black-vvti-street-tune
  output for sweep data."
