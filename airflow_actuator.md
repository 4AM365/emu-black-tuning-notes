# Airflow / Idle DBW — live calibration reference

Current state of the Airflow-Actuator + idle DBW system. Keep this updated when values change.
Full table data lives in the `.emubt` files and in `supra export 05222026 (2.4-8.0 range).xml.emub3`
(that XML is a reference snapshot only — actual changes are made in EMU).

- **Last updated:** 2026-05-22
- **Actuator range:** `[2.4%, 8.0%]` TPS (was `[3.5%, 8.0%]`; original `[2.0%, 6.4%]`)
- **Change history:** see `cranking_and_idle.md` → Change log.

## Actuator range (the airflow→TPS mapping)

`TPS% = floor + airflow% / 100 × (ceiling − floor)`

| symbol | raw | scale | = | meaning |
|---|---|---|---|---|
| `idleDBWTargetMin` | 24 | 0.1 | **2.4%** | range floor |
| `idleDBWTargetMax` | 80 | 0.1 | **8.0%** | range ceiling |

Width = 8.0 − 2.4 = **5.6**. (Old width 3.5→8.0 = 4.5.)

## Airflow-% encoding

- ubyte airflow-% tables: **0.5/count** (raw = 2 × displayed %). e.g. raw 130 = 65.0%.
- `idleDBWTargetMin/Max`: word, **0.1/count** (TPS %).
- `idleCustomCorrection`: sbyte, **1:1**, signed, **additive** (mode is configurable in EMU; currently additive).

## Airflow-% tables (displayed %, current = post 2.4–8.0 rescale)

### Active state air flow `idleActiveAirflow` — X=Coolant °C, Y=Idle RPM
| RPM\CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 82.5 | 76.5 | 69.5 | 67.5 | 66.0 | 65.0 | 65.0 |
| 1375 | 86.0 | 81.0 | 71.0 | 61.0 | 61.0 | 61.0 | 60.0 | 60.0 |
| 1200 | 81.0 | 75.0 | 63.5 | 52.0 | 50.0 | 50.0 | 49.5 | 49.5 |
| 1100 | 74.5 | 69.0 | 56.0 | 40.0 | 37.5 | 36.0 | 37.5 | 37.5 |
| 1000 | 65.0 | 60.0 | 50.0 | 35.5 | 32.5 | 31.5 | 31.5 | 31.5 |

### Armed state air flow `idleArmedAirFlow` — vs RPM (8 bins)
`39.0  45.0  50.5  54.5  58.0  60.0  62.5  63.0`

### Cranking airflow `idleCrankingDC` — X=Coolant °C 0/33/67/100 (cold→hot)
`13.0  12.5  12.0  11.5`  (cold cell = 3.13% TPS — the cold-crank vacuum anchor)

### Custom air flow correction `idleCustomCorrection` (additive %) — X=IAT °C, Y=Idle RPM
| RPM\IAT | 20 | 30 | 40 | 60 | 70 |
|---|---|---|---|---|---|
| 1500 | 1 | 0 | -3 | -10 | -14 |
| 1375 | 2 | 0 | -5 | -15 | -20 |
| 1200 | 2 | 0 | -7 | -22 | -30 |
| 1100 | 2 | 0 | -9 | -26 | -35 |
| 1000 | 2 | 0 | -10 | -31 | -40 |

## Airflow PID (output is airflow %, scales with range width)

| symbol | old | current | note |
|---|---|---|---|
| `idleAirFlowKP` | 2048 | **1646** | ×4.5/5.6 (range widened) |
| `idleAirFlowKI` | 205 | **165** | ×4.5/5.6 |
| `idleAirFlowKD` | 0 | 0 | — |
| `idleAirFlowIntegralLimitMin` | -8 | **-6** | airflow-% authority clamp |
| `idleAirFlowIntegralLimitMax` | 10 | **8** | |
| `idleAirPIDOutMin` | -10 | **-8** | |
| `idleAirPIDOutMax` | 12 | **10** | |

Starting points after the range change — confirm by feel (hunts → trim down; sluggish recovery → nudge up).

## Rescale rules (when the range changes again)

`f,c` = floor, ceiling. width = c − f.
- **Absolute airflow-% tables** (Active, Armed) — preserve actual TPS:
  `new% = (f_old − f_new)/(c_new − f_new)×100 + (c_old − f_old)/(c_new − f_new) × old%`
- **Additive correction** (delta, no offset): `new = old × (c_old − f_old)/(c_new − f_new)`
- **Airflow PID gains & limits** (delta output): same width-ratio scale as the correction.
- **Cranking**: not preserved — set the cold cell to the target TPS directly,
  `new% = (TPS_target − f_new)/(c_new − f_new)×100`, keep the taper shape.

See the `emu-black-tune` skill for full methodology and the `emu-black-emubt-export` skill for writing tables back out.
