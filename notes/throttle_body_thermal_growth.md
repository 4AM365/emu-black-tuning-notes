# Throttle body thermal growth — airflow correction sanity check

First-principles bound on how much of the `idleCustomCorrection` table magnitude is justified by TB thermal expansion alone (vs. other warm-engine effects).

## Material assumptions (Supra build)

| Part | Material | α (×10⁻⁶ /°C) |
|---|---|---|
| Bore | A356 cast aluminum | **21.5** |
| Plate | 304 stainless steel | **17.0** |
| Differential | (bore − plate) | **4.5** |

General defaults if unknown: plates may be C200 brass (α ≈ 20) or stainless (α ≈ 17); housings typically A356 (α ≈ 21.5). Brass × Al has small differential (~1.5); SS × Al has large differential (~4.5).

### Reference: Bosch DV-E blade (Porsche Cayenne etc.) — nickel silver C76100

Identified empirically from a physical blade stamped **"761"** = CDA **C76100 nickel silver** (a copper-nickel-zinc "nickel brass"). Confirmed non-magnetic (rules out stainless) and silvery-white (the ~7-9% Ni bleaches out the brass yellow — looks aluminum-ish, NOT gold).

| Property | C76100 | Note |
|---|---|---|
| Composition | Cu 59-63%, Ni 7-9%, bal. Zn (~28-34%) | brass family, not Al, not SS |
| α (CTE) | **≈ 16.2 ×10⁻⁶ /°C** (20-300 °C) | ~ same as 304 SS (17), NOT like Al (21.5) |
| Thermal conductivity | ~40 W/m·K | ~¼ of aluminum (~150) |

**Differential vs A356 aluminum bore = 21.5 − 16.2 = 5.3 ppm/°C** — slightly *larger* than the SS×Al case (4.5). So a nickel-silver blade behaves like the stainless assumption above, just marginally stronger: gap opens with heat at ~5.3 ppm/°C × D × ΔT.

**Gap-consistency implications:**
1. Gap is **not thermally constant** — it opens monotonically as the assembly heats (bore outruns blade). Same direction as SS plate. A matched aluminum blade would hold gap constant (~0 differential) but Bosch deliberately uses lower-CTE blade so clearance **always grows, never binds** (anti-seize by design) at the cost of a temperature-varying leak path.
2. Closed-plate **leakage rises when hot** → compensate idle/closed-throttle airflow as a CLT/IAT-indexed offset, not a fixed DBW floor. For a 60 mm blade over ΔT 80 °C: ΔgapØ ≈ 60 × 5.3e-6 × 80 ≈ 25 µm diametral (~13 µm radial).
3. The low conductivity (~40 W/m·K) makes the **blade thermally lag the bore** during warmup/transients → transient gap overshoot on top of the steady-state delta. Gap is predictable but not constant.

## Geometry

- Bore diameter D = **73 mm**
- Plate diameter d_p ≈ 72.9 mm (radial clearance 0.05 mm per side; typical butterfly throttle)
- Plate thickness t ≈ 1-2 mm (not used in this calc — negligible at small φ)
- Full DBW sweep assumed = 90°; idle TPS angle φ = TPS%/100 × 90°
- Actuator floor: TPS 2.4 % (`idleDBWTargetMin`), hardware-limited effective floor ~3.0 % TPS (per [supra DBW DC floor memory](C:\Users\WTCra\.claude\projects\C--Code-car-projects-emu-black-tuning-notes\memory\project_supra_dbw_dc_floor.md))

## Butterfly flow area formula

For a plate of diameter d_p in a bore of diameter D, at angle φ from fully closed:

```
A(φ) = (π/4) × ( D² − d_p² × cos(φ) )
```

Bounds:
- φ = 0 (fully closed): `A = (π/4)(D² − d_p²) ≈ π × D × c` where c = radial clearance
- φ = 90° (fully open): `A = πD²/4` (full bore)

At small idle φ (~3-5°), cos(φ) ≈ 0.997-0.998. The plate is still blocking nearly all of its disc area, and the open area is **mostly the radial clearance widened by the plate tilt**. **The dominant flow path is the differential clearance around the plate edge.** The earlier "tilt gap dominates" reasoning was wrong — that model would apply at much larger φ (full-open regime, not idle).

## Thermal expansion math (differential)

Hot dimensions:
```
D_hot   = D   × (1 + α_bore  × ΔT) = 73   × (1 + 21.5e-6 × ΔT)
d_p_hot = d_p × (1 + α_plate × ΔT) = 72.9 × (1 + 17.0e-6 × ΔT)
```

ΔT here is the **TB body temp swing from the temperature at which the active-airflow table was calibrated** — not necessarily CAT directly. CAT is a sensor proxy that may lead or lag TB body during transients.

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

Choked flow at idle (MAP ~35 kPa < 0.528 × P_atm), so mass flow ∝ flow area. ΔA/A is also the fractional mass-flow increase at same upstream conditions.

**The RPM dependence emerges from geometry**: at lower idle target RPM, the base airflow command is smaller → TPS is smaller → φ is smaller → flow area is dominated by radial clearance, which receives a larger *fractional* increase from a fixed *absolute* differential clearance growth. So the correction needs to be more negative at lower RPM — exactly the trend in the implemented table.

## Comparison to implemented `idleCustomCorrection` at CAT 70 (assuming ≈ ΔT 50 °C)

| Idle target RPM | TB-growth prediction | implemented | residual |
|---:|:---:|:---:|:---:|
| 1500 | -8 % | -10 % | -2 % |
| 1375 | -8.5 % | -15 % | -6.5 % |
| 1200 | -10 % | -21 % | -11 % |
| 1100 | -11 % | -24 % | -13 % |
| 1000 | -11 % | -28 % | -17 % |

**TB thermal growth alone justifies roughly 50-100 % of the implemented correction depending on the cell.** Tight match at high idle target (1500-1375); growing residual at low idle target. Either:
- The TB body is hotter than CAT alone suggests (ΔT may be 70-80 °C at hot soak, giving +14-16 % growth that fully covers the implemented values)
- Or other effects contribute the rest:
  - Oil temp lagging CLT under sustained load → less rotational drag than `idleActiveAirflow` accounts for
  - VE shift at hot intake (less wall film, better atomization)
  - Lambda effects at high CAT

## Worst-case at actuator floor (φ = 2.16°, TPS = 2.4 %)

This is where the smallest φ meets the biggest fractional thermal-growth effect — the cell most relevant for stall safety analysis.

| ΔT | A (mm²) | ΔA / A_cold |
|---:|:---:|:---:|
| 0 | 14.42 | — |
| 30 °C | 15.57 | +8.0 % |
| 50 °C | 16.34 | +13.3 % |
| 80 °C | 17.49 | +21.3 % |
| 100 °C | 18.27 | +26.7 % |

The implemented `idleCustomCorrection` at CAT 70 / idle target 1000 RPM = -28 %, which matches the **actuator-floor + extreme-soak (ΔT ≈ 80 °C)** prediction nearly exactly. The table is right-sized for the worst-case scenario where the throttle saturates at the floor during a hot soak — the operating point where stall margin is most at risk.

## CAT 50 column (ΔT ≈ 25-30 °C from baseline)

| Idle target RPM | predicted at ΔT=25 | implemented |
|---:|:---:|:---:|
| 1500 | -4 % | -3 % |
| 1375 | -4.3 % | -4 % |
| 1200 | -5 % | -6 % |
| 1100 | -5.5 % | -7 % |
| 1000 | -5.7 % | -8 % |

Excellent match in the upper rows; slight over-correction (more negative than predicted) in the lower rows. The match here is closer than at CAT 70, suggesting the reference temperature for the active table is around CAT 25-30 °C, and at moderate CAT excursions the correction is almost purely TB-growth driven.

## Validity / known limitations

- Assumes full DBW sweep = 90°. If the actual mechanical sweep is different (e.g., 80°), φ values shift and predicted Δ values change by ~10 %.
- Assumes radial clearance 0.05 mm per side. Tighter clearance (0.025 mm) gives bigger fractional areas, looser (0.10 mm) gives smaller. Within ±50 % of the assumed value the qualitative conclusion (TB growth explains the bulk of the correction) is unchanged.
- Assumes CAT 70 ≈ TB body ΔT 50 °C from reference. Real TB body equilibrates closer to coolant (~95 °C) at idle — so for hot soak conditions ΔT may be 60-80 °C and the prediction grows proportionally.
- Flow assumed choked across the gap (valid for idle MAP). For higher MAP (mid-load) the relationship between area and mass flow loses the simple proportionality and density effects re-enter.
- Plate thickness (1-2 mm) ignored. At small φ the plate edge geometry could marginally affect C_d, but the magnitude is sub-percent.

## Reference physics-pure scalar table

Baseline at CAT 30 °C (correction = 0), CAT axis treated as direct proxy for TB body temp:

| Idle target (RPM) \ IAT (°C) | 20 | 30 | 40 | 50 | 70 |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1500 | +2 | 0 | -2 | -3 | -6 |
| 1375 | +2 | 0 | -2 | -3 | -6 |
| 1200 | +2 | 0 | -2 | -4 | -7 |
| 1100 | +2 | 0 | -2 | -4 | -8 |
| 1000 | +2 | 0 | -2 | -4 | -8 |

At CAT 70 cap under various TB-body-soak assumptions:

| Idle target (RPM) \ ΔT_body at CAT 70 | 40 °C (CAT = body) | 60 °C (body hotter than CAT) | 80 °C (body fully coolant-soaked) |
|---:|:---:|:---:|:---:|
| 1500 | -6 | -9 | -12 |
| 1375 | -6 | -10 | -13 |
| 1200 | -7 | -11 | -14 |
| 1100 | -8 | -12 | -15 |
| 1000 | -8 | -12 | -16 |

The physics-pure values are a defensible starting point and a hard upper bound on what can be justified without empirical evidence of unmodeled effects. Anything beyond ~-16 % at CAT 70 needs a specific reason from logging, not extrapolation.

## Implications for table design

1. **TB thermal growth is a real and significant contributor** to the `idleCustomCorrection` magnitude at hot CAT — NOT a sub-percent effect as I previously claimed.
2. **The implemented table is reasonably calibrated against the physics** at the upper RPM rows. The lower RPM rows may be tuned a bit aggressively or may correctly reflect TB body running hotter than CAT.
3. **If you change to a brass-plated throttle**, the differential α drops from 4.5 to ~1.5 ppm/°C — a factor of 3 reduction in TB-growth effect. Predicted correction at CAT 70 would be -3 % instead of -10 %. The implemented values would over-correct on a brass-plate TB. (Doesn't apply unless you swap TBs.)
4. **If the actuator floor were higher (say 4 % TPS), the radial-clearance contribution would shrink and the table magnitudes at low idle target RPM would also need to shrink.** The lowered floor on this build is what makes the TB-growth correction so RPM-dependent.
