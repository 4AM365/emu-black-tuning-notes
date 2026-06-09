# Throttle body thermal growth — airflow correction sanity check

A first-principles way to bound how much of a hot-idle airflow correction (`idleCustomCorrection`) is justified by throttle-body thermal expansion alone, vs. other warm-engine effects. The method is car-agnostic; plug in your TB's bore diameter, materials, and idle TPS.

> **Car-specific values live in the build working docs**, not here. For the reference build's geometry, per-RPM operating points, and the comparison against the implemented `idleCustomCorrection` table, see [`supra/notes/throttle_body_thermal_growth.md`](../supra/notes/throttle_body_thermal_growth.md). This note is intentionally car-agnostic.

## Material reference (CTE of common butterfly parts)

| Part | Material | α (×10⁻⁶ /°C) |
|---|---|---|
| Housing/bore | A356 cast aluminum | ~21.5 |
| Plate | 304 stainless steel | ~17.0 |
| Plate | C200 brass | ~20 |
| Plate | C76100 nickel silver | ~16.2 |

Differential α = α_bore − α_plate is what drives clearance change:
- **Brass plate × Al bore** → small differential (~1.5 ppm/°C) → gap nearly constant with heat.
- **Stainless / nickel-silver plate × Al bore** → large differential (~4.5–5.3 ppm/°C) → gap **opens monotonically as the assembly heats** (bore outruns blade).

### Reference: Bosch DV-E blade (Porsche Cayenne etc.) — nickel silver C76100

Identified from a physical blade stamped **"761"** = CDA **C76100 nickel silver** (Cu 59–63%, Ni 7–9%, bal. Zn). Non-magnetic (rules out stainless), silvery-white (the Ni bleaches the brass yellow — looks aluminum-ish). α ≈ 16.2 ×10⁻⁶/°C, thermal conductivity ~40 W/m·K (~¼ of aluminum). Differential vs A356 Al bore ≈ 5.3 ppm/°C — Bosch deliberately uses a lower-CTE blade so clearance **always grows, never binds** (anti-seize by design), at the cost of a temperature-varying leak path. Its low conductivity makes the **blade thermally lag the bore** during warmup → transient gap overshoot on top of the steady-state delta.

**Implication:** on the common (SS/nickel-silver plate × Al bore) pairing, closed-plate **leakage rises when hot** → compensate idle/closed-throttle airflow as a CLT/IAT-indexed offset, not a fixed DBW floor.

## Butterfly flow area formula

For a plate of diameter `d_p` in a bore of diameter `D`, at angle φ from fully closed:

```
A(φ) = (π/4) × ( D² − d_p² × cos(φ) )
```

Bounds:
- φ = 0 (fully closed): `A = (π/4)(D² − d_p²) ≈ π × D × c`, where c = radial clearance
- φ = 90° (fully open): `A = πD²/4` (full bore)

At small idle φ (~3–5°), cos(φ) ≈ 0.997–0.998 — the plate still blocks nearly all of its disc area, so the open area is **mostly the radial clearance widened slightly by plate tilt**. **The dominant idle flow path is the differential clearance around the plate edge**, not the tilt gap (tilt only dominates at much larger φ, in the full-open regime).

## Thermal expansion math (differential)

```
D_hot   = D   × (1 + α_bore  × ΔT)
d_p_hot = d_p × (1 + α_plate × ΔT)
```

`ΔT` is the **TB body temp swing from the temperature at which the active-airflow table was calibrated** — not necessarily the CAT/IAT reading directly. CAT is a sensor proxy that may lead or lag TB body during transients. For a butterfly of diameter ~D over ΔT, diametral clearance grows by ≈ `D × (α_bore − α_plate) × ΔT`.

Idle MAP is below the choke threshold (MAP < 0.528 × P_atm), so flow is choked across the gap and **mass flow ∝ flow area** — `ΔA / A` is the fractional mass-flow increase at the same upstream conditions.

## Why the correction is RPM-dependent (the key principle)

At lower idle-target RPM the base airflow command is smaller → idle TPS is smaller → φ is smaller → the open area is dominated by radial clearance. A fixed *absolute* differential-clearance growth is then a larger *fractional* increase. **So the thermal-growth correction must be more negative at lower idle RPM** — the RPM dependence emerges purely from geometry, not from a separate effect. Any implemented `idleCustomCorrection` table should show this monotonic trend; if it does, that's evidence it's physically grounded rather than arbitrarily hand-fit.

## How to use this as a sanity check

1. Compute the predicted `ΔA/A` at each idle-target row for a representative hot-soak ΔT, using your TB's `D`, `d_p`, materials, and the idle TPS your active table commands at warm CLT.
2. Compare against the implemented `idleCustomCorrection` magnitudes. A close match at the **upper** RPM rows with a growing residual at the **lower** rows is the typical signature — the residual is either TB body running hotter than the temp sensor suggests, or other warm effects (oil-temp drag, VE shift at hot intake, lambda effects).
3. Treat the pure-physics prediction as a **defensible starting point and an upper bound** on what's justifiable without log evidence. Corrections well beyond the physics prediction need a specific logged reason, not extrapolation.

## Validity / known limitations

- Assumes full DBW sweep = 90°; a different mechanical sweep shifts φ and the predicted Δ by ~10%.
- Assumes a radial clearance value; within ±50% of the assumed clearance the qualitative conclusion (TB growth explains the bulk of the correction) holds.
- Assumes the temp-sensor → TB-body ΔT mapping; real TB body equilibrates closer to coolant at idle, so hot-soak ΔT may be larger than the sensor suggests and the prediction scales up.
- Choked-flow proportionality (area ∝ mass flow) holds at idle MAP; at higher MAP density effects re-enter.
- Plate thickness ignored (sub-percent at small φ).
- **A brass-plated TB** drops the differential α by ~3× → the whole correction shrinks proportionally; a table tuned for a stainless/nickel-silver blade would over-correct on brass. Re-derive if the TB changes.
- A **higher actuator floor** shrinks the radial-clearance contribution → the low-RPM magnitudes shrink too. A lowered floor is what makes the correction strongly RPM-dependent.
