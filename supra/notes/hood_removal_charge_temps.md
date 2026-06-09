# Hood removal vs charge/intake temps — Supra worked example

Build-specific results behind the generic note [`notes/hood_removal_charge_temps.md`](../../notes/hood_removal_charge_temps.md). Validated May 2026 by comparing labeled hood-on logs against the single hood-off log (`hood-removed.csv`). Phoenix/Gilbert ambient from Open-Meteo hourly archive.

## Channel interpretation (IMPORTANT — corrects earlier assumptions)
- **`Charge temp` == `IAT`**, exactly, row-for-row in the full-channel logs
  (drive_home, more_tip_in both show Charge med = IAT med). So in this config
  `Charge temp` is just the **physical manifold/throttle-body intake-air sensor**,
  NOT a coolant-blended model. Treat it as real intake-air temp. The reduced-channel
  logs (0506/0514/hood-removed) drop IAT and keep only `Charge temp` — same sensor.
- **`Pre IC temperature` was logged with the WRONG calibration curve** ("Custom temp
  cal 1") instead of the real IAT sensor curve — it's the same sensor type. This made
  it read ~30 °C too COLD (e.g. logged 17 °C → true 45 °C; logged 31 °C → true 56 °C).
  To correct a logged value: invert the wrong curve (T→V), then apply the correct IAT
  curve (V→T). Script: `correct_preic.py` (curves embedded).
  - WRONG curve V→T: 0.00→92, 0.55→55, 0.57→54, 1.67→15, 2.22→3, 2.76→-5, 3.31→-15,
    3.88→-24, 4.43→-33, 4.98→-40
  - CORRECT (IAT) V→T: 0.00→121, 0.24→115, 0.31→104, 0.45→91, 0.78→71, 1.00→62,
    1.45→49, 1.73→42, 2.47→27, 2.96→18, 3.63→6, 4.10→-5, 4.63→-22, 4.98→-39
  - **Corrected, Pre-IC is the HOTTEST point in the tract** (~50–58 °C at hot idle),
    sitting off the turbo — NOT cool inlet air as the bad cal made it look. The IC then
    cools it before the manifold (Charge/IAT). Recovered voltage cross-checks vs raw
    `Analog 2` in direction (colder→higher V) but not 1:1 (logging divider) — trust the
    curve inversion, which is exact given the wrong curve.
- `Ambient temperature` and `Post IC temperature` channels are **not wired** — they
  read a flat −40 °C (EMU open-circuit default). Do not use; pull ambient from weather.

## Headline result (matched ambient, the cleanest comparison)
0514 hood-ON @ 99 °F (Phoenix) vs hood-OFF @ 97 °F — only ~2 °F apart, MAP<100:

| condition | metric | hood ON | hood OFF | delta |
|---|---|---|---|---|
| idle | Charge/IAT | 53.1 °C (128 °F) | 45–48 °C | **−5 to −8 °C** |
| idle | Pre-IC (corrected) | 50.8 °C (123 °F) | 44.6 °C (112 °F) | **−6.2 °C** |
| all no-boost | Pre-IC (corrected) | 52.0 °C | 49.2 °C | **−2.8 °C** |

**Removing the hood drops intake charge temp ~5–8 °C (10–15 °F) at matched ambient**,
biggest at idle. Corrected Pre-IC (turbo-side) and Charge (manifold) agree.
Corrected Pre-IC also orders cleanly by heat load: 0509 @104 °F = 58 °C idle,
0514 @99 °F = 51 °C, hood-off @97 °F = 45 °C.

## Physical picture: where the heat lives
Charge − Pre-IC gap (heating from turbo inlet to manifold), idle:
- 0514 hood-on: +28 °C   hood-off: +28 °C   (Apr-8 moving logs: ~+16–18 °C ≈ just the sensor offset)
- The hot-idle gap = ~17 °C sensor offset + ~11 °C REAL manifold soak.
- That ~11 °C real soak is the SAME hood-on vs hood-off → **the hood does not fix
  manifold/plenum conduction from the hot head.** Hood removal lowers the *level* of
  air entering (inlet/Pre-IC) and the manifold temp tracks down with it, but the
  conduction-driven rise across the plenum is unchanged.

## Confounds to respect
1. **Drive composition dominates manifold temp.** Same night/ambient, drive_home
   (moving) IAT 35 °C vs more_tip_in (idling/blips) IAT 47 °C — 12 °C apart from soak
   time alone. 0509 (hottest day, 104 °F) shows LOW charge (38 °C) because it was a
   highway drive. **Always compare like-for-like: idle-vs-idle is the control.**
2. **n=1 on hood-off.** Need a hot-day hood-off log (heat-soaked idle) to firm up.
3. Hood-off Pre-IC has ~10% dropouts to 0 °C — filter `>2 °C`.

## Method notes
- Precise ambient = file CreationTime → weekday-workhours = Phoenix 85004, else =
  Gilbert 85233 → Open-Meteo hourly. **BUT** re-saving/exporting logs through OneDrive
  resets CreationTime (all May logs got stamped 5/31). Only intact stamps survived on
  drive_home/more_tip_in (Apr 8). To keep this method usable, preserve original file
  timestamps or name logs `YYYYMMDD_HHMM`.
- Scripts: `analyze_hood_hot.py` (matched hot-day compare), `analyze_apr8.py`
  (channel-identity + Pre-IC offset check).
