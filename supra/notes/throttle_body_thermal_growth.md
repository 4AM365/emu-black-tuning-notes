# Throttle body thermal growth — Supra worked example (GS430 TB)

Build-specific worked numbers behind the airflow-correction sanity check. The car-agnostic method, formulas, and material reference live in [`notes/throttle_body_thermal_growth.md`](../../notes/throttle_body_thermal_growth.md). This file holds **this build's** geometry, the per-RPM operating points, and the comparison against the implemented `idleCustomCorrection` table.

## Material assumptions (this build's GS430 TB)

| Part | Material | α (×10⁻⁶ /°C) |
|---|---|---|
| Bore | A356 cast aluminum | **21.5** |
| Plate | 304 stainless steel | **17.0** |
| Differential | (bore − plate) | **4.5** |

(If the actual GS430 blade turns out to be nickel-silver like the Bosch DV-E reference in the generic note, the differential is ~5.3 instead of 4.5 — slightly stronger, same direction.)

## Geometry (this TB)

- Bore diameter D = **73 mm**
- Plate diameter d_p ≈ 72.9 mm (radial clearance 0.05 mm per side; typical butterfly throttle)
- Plate thickness t ≈ 1–2 mm (negligible at small φ)
- Full DBW sweep assumed = 90°; idle TPS angle φ = TPS%/100 × 90°
- Actuator floor: TPS 2.4 % (`idleDBWTargetMin`), hardware-limited effective floor ~3.0 % TPS (per [supra DBW DC floor memory](C:\Users\WTCra\.claude\projects\C--Code-car-projects-emu-black-tuning-notes\memory\project_supra_dbw_dc_floor.md))

## Thermal expansion math (differential)

```
D_hot   = D   × (1 + α_bore  × ΔT) = 73   × (1 + 21.5e-6 × ΔT)
d_p_hot = d_p × (1 + α_plate × ΔT) = 72.9 × (1 + 17.0e-6 × ΔT)
```

ΔT = TB body temp swing from the temperature at which `idleActiveAirflow` was calibrated (not necessarily CAT directly — CAT leads/lags TB body during transients).

| ΔT | D_hot (mm) | d_p_hot (mm) | Δ diametral clearance |
|---:|:---:|:---:|:---:|
| 0 | 73.000 | 72.900 | 0 |
| 30 °C | 73.047 | 72.937 | 9.9 μm |
| 50 °C | 73.078 | 72.962 | 16.4 μm |
| 80 °C | 73.126 | 72.999 | 26.3 μm |
| 100 °C | 73.157 | 73.024 | 32.9 μm |

## Per-RPM operating point at warm CLT (96 °C col of `idleActiveAirflow`)

| Idle target RPM | warm `Idle air %` | TPS % | φ (deg) |
|---:|:---:|:---:|:---:|
| 1500 | 45.0 | 4.92 | 4.43° |
| 1375 | 40.0 | 4.64 | 4.18° |
| 1200 | 26.5 | 3.88 | 3.49° |
| 1100 | 18.5 | 3.44 | 3.10° |
| 1000 | 16.5 | 3.32 | 2.99° |

## Cold flow area at each idle TPS

```
A_cold(φ) = (π/4) × ( 73² − 72.9² × cos(φ) )
```

| Idle target RPM | A_cold (mm²) |
|---:|:---:|
| 1500 | 23.95 |
| 1375 | 22.57 |
| 1200 | 19.18 |
| 1100 | 17.55 |
| 1000 | 17.12 |

## Hot flow area & area increase at ΔT = 50 °C (≈ CAT 70 from CAT 20 reference)

| Idle target RPM | A_hot (mm²) | **ΔA / A_cold** |
|---:|:---:|:---:|
| 1500 | 25.86 | **+8.0 %** |
| 1375 | 24.49 | **+8.5 %** |
| 1200 | 21.11 | **+10.1 %** |
| 1100 | 19.48 | **+11.0 %** |
| 1000 | 19.05 | **+11.3 %** |

Choked flow at idle (MAP ~35 kPa < 0.528 × P_atm), so mass flow ∝ flow area; ΔA/A is the fractional mass-flow increase at same upstream conditions.

## Comparison to implemented `idleCustomCorrection` at CAT 70 (assuming ≈ ΔT 50 °C)

| Idle target RPM | TB-growth prediction | implemented | residual |
|---:|:---:|:---:|:---:|
| 1500 | -8 % | -10 % | -2 % |
| 1375 | -8.5 % | -15 % | -6.5 % |
| 1200 | -10 % | -21 % | -11 % |
| 1100 | -11 % | -24 % | -13 % |
| 1000 | -11 % | -28 % | -17 % |

**TB thermal growth alone justifies roughly 50–100 % of the implemented correction depending on the cell.** Tight match at high idle target (1500–1375); growing residual at low idle target. Either the TB body is hotter than CAT alone suggests (ΔT may be 70–80 °C at hot soak, giving +14–16 % growth that fully covers the implemented values), or other effects contribute the rest (oil temp lagging CLT, VE shift at hot intake, lambda effects at high CAT).

## Worst-case at actuator floor (φ = 2.16°, TPS = 2.4 %)

| ΔT | A (mm²) | ΔA / A_cold |
|---:|:---:|:---:|
| 0 | 14.42 | — |
| 30 °C | 15.57 | +8.0 % |
| 50 °C | 16.34 | +13.3 % |
| 80 °C | 17.49 | +21.3 % |
| 100 °C | 18.27 | +26.7 % |

Implemented `idleCustomCorrection` at CAT 70 / idle target 1000 RPM = -28 %, which matches the **actuator-floor + extreme-soak (ΔT ≈ 80 °C)** prediction nearly exactly — the table is right-sized for the worst-case hot-soak stall-margin point.

## CAT 50 column (ΔT ≈ 25–30 °C from baseline)

| Idle target RPM | predicted at ΔT=25 | implemented |
|---:|:---:|:---:|
| 1500 | -4 % | -3 % |
| 1375 | -4.3 % | -4 % |
| 1200 | -5 % | -6 % |
| 1100 | -5.5 % | -7 % |
| 1000 | -5.7 % | -8 % |

Closer match than at CAT 70 → reference temp for the active table is ~CAT 25–30 °C; at moderate CAT excursions the correction is almost purely TB-growth driven.

## Reference physics-pure scalar table (this build)

Baseline at CAT 30 °C (correction = 0), CAT axis as direct proxy for TB body temp:

| Idle target (RPM) \ IAT (°C) | 20 | 30 | 40 | 50 | 70 |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1500 | +2 | 0 | -2 | -3 | -6 |
| 1375 | +2 | 0 | -2 | -3 | -6 |
| 1200 | +2 | 0 | -2 | -4 | -7 |
| 1100 | +2 | 0 | -2 | -4 | -8 |
| 1000 | +2 | 0 | -2 | -4 | -8 |

At CAT 70 cap under various TB-body-soak assumptions:

| Idle target (RPM) \ ΔT_body at CAT 70 | 40 °C (CAT = body) | 60 °C (body hotter) | 80 °C (coolant-soaked) |
|---:|:---:|:---:|:---:|
| 1500 | -6 | -9 | -12 |
| 1375 | -6 | -10 | -13 |
| 1200 | -7 | -11 | -14 |
| 1100 | -8 | -12 | -15 |
| 1000 | -8 | -12 | -16 |

Anything beyond ~-16 % at CAT 70 needs a specific reason from logging, not extrapolation.

## Build-specific design implications

1. The implemented table is reasonably calibrated against the physics at the upper RPM rows; lower rows may be slightly aggressive or correctly reflect TB body running hotter than CAT.
2. **If swapped to a brass-plated throttle**, differential α drops 4.5 → ~1.5 ppm/°C (×3 reduction); predicted CAT-70 correction would be ~-3 % instead of ~-10 %, so the current values would over-correct. (Doesn't apply unless the TB changes.)
3. The lowered actuator floor on this build is what makes the TB-growth correction so RPM-dependent — a higher floor would shrink the low-RPM magnitudes.
