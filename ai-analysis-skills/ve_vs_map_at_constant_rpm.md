# VE vs MAP at constant RPM, and copying RPM shape across boost columns

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`mass_flow_estimator_quirk.md`](../supra/notes/mass_flow_estimator_quirk.md). This note is intentionally car-agnostic.

## Principle: cam-resonance VE peak is an RPM phenomenon, copy it across all MAP columns
Cam/runner tuning makes an engine resonate at some peak-filling RPM. Evidence on a
given build: at constant ignition timing and boost, knock first appears at that
resonance RPM (max trapped mass → max end-gas compression/heating → knock-prone).
Because resonance is set by RPM (cam/runner tuning), the **VE-vs-RPM contour shape
does not move with manifold pressure**. So stamping a known-good, well-mapped MAP
column's RPM shape onto an unmapped high-boost column (top of `mapBins`) is
methodologically correct — better than interpolating *through* the resonance peak.

## Principle: VE at higher MAP (same RPM) trends flat-to-DOWN, not up
"The compressor loves pressure ratio" describes the **compressor's** flow/efficiency —
it is decoupled from cylinder VE by the plenum. VE is normalized to manifold density, so
once air is in the plenum at high MAP, cylinder filling is governed by:
- **Exhaust backpressure** (turbo): higher at high MAP → worse scavenging → lowers trapped VE.
- **Charge heating** at higher pressure ratio: lower density for the same MAP → lowers
  mass-based VE unless IAT/charge-temp correction fully compensates.

Both push true air-VE at higher MAP to **equal-or-slightly-lower** vs a lower-MAP column
at the same RPM. An *upward* offset when copying a low-MAP column up to high MAP is NOT
supported by filling physics.

## Practical: an upward VE offset into unproven boost is the SAFE direction
Erring VE high = more fuel = richer = safer on knock/EGT in an unproven high-boost zone.
Fine as a **placeholder to log against**, but it is a safety bias, not a derived value.
Because the RPM shape is copied correctly, wideband trims converge as a near-uniform
scalar (expect a small pull-DOWN). Let measured lambda set the final magnitude.

## Fuel-model confirmation
`lambdaTable` is **only a tuning reference + closed-loop STFT target** — it
is NOT a fuel-equation multiplier (see `notes/fueling.md`). So `veTable` IS the dose and
must carry enrichment by hand. Verdict for high-boost columns: the dose offset between
two MAP columns SHOULD be added (no double-count risk), and its correct size =
(air-VE ratio between the two columns) × (target-λ enrichment between them). Back the
enrichment factor out of measured lambda at the two columns (richer target at higher
MAP → enrich > 1). With air VE flat-to-down, the honest dose offset is roughly the
λ-enrichment alone — an eyeballed flat offset copied up the MAP axis is typically
too rich.

## Working correction model
To rebuild a high-boost column from a known-good anchor column so it is
consistent with target lambda AND engine efficiency, with NO log data:

    dose(m,rpm) = dose(anchor,rpm) * enrich(m,rpm) * VEeff(m,rpm)

- `enrich = lambda_target(anchor)/lambda_target(m)` — from the relevant `lambdaTable`
  (use `lambdaTable2` for the ethanol map), bilinear, with the boost slope **linearly
  extended above the table's top MAP bin** if the intended target keeps richening past
  where the table tops out. Richer m -> enrich > 1.
- `VEeff = 1 - k(rpm)/100 * (m-anchor)/100` — theoretical air-VE roll-off into boost.
  `k` is %/100 kPa, RPM-weighted because EMAP/charge-heat hurt most at high rpm:
  schedule `k` low at low RPM and rising toward redline (e.g.
  `k(rpm)=clip(0.5 + (rpm-2500)/4500*2.5, 0.5, 3.0)`). VEeff <= 1.

Net behavior (the whole point): at LOW rpm enrich dominates (offset stays positive); at
HIGH rpm VEeff cancels enrich (offset -> ~0, dose returns to the anchor). This pulls down
the high-rpm/high-boost corner where an eyeballed flat offset is always too rich. Finish
with a light [.25,.5,.25] RPM smooth on the rebuilt cols and enforce non-decreasing
across MAP. The k-schedule is a theoretical placeholder — replace VEeff with measured
air VE (EMAP log or wideband back-out) when available.

## Verification method: veTable × λ_target = air-VE proxy (must be smooth)
Because `lambdaTable` is a reference/STFT target, NOT a fuel multiplier, the dose
veTable must carry 1/λ enrichment by hand. The cheap whole-table check:
`air_VE_proxy(m,rpm) = veTable(m,rpm) × λ_target(m,rpm)`. Interpolate the λ table onto
the VE grid and form the product across MAP at each RPM. A correct VE shape yields a
**smooth** surface: rises out of the idle/vacuum region, peaks near the torque-MAP band
(roughly atmospheric load), then tapers gently into boost (EMAP/charge-heat roll-off).
A **dip or step at the boost knee** (where λ_target starts dropping near the
boost-onset MAP) means the veTable did NOT receive the extra fuel the (newly expanded)
λ targets demand — i.e. shape mismatch.

## Worked example: a PASS
Run the product test on an export against its expanded `lambdaTable`/`lambdaTable2`.
A pass looks like: all checks (VE1×λ1 pump endpoint, VE1×blend, VE2×λ2 ethanol
endpoint) produce a clean monotone-rise-then-gentle-taper air-VE proxy with NO kink at
the boost enrichment onset. That means the dose VE rose as ~1/λ through the boost
columns — the VE table shape DOES track the lambda targets; enrichment is baked into
veTable, no double count, no gap. Also confirm boost is referenced to pedal/TPS:
`boostTarget1/2` X axis = `ppsBoostBins`, with the closed-throttle column at zero boost
and a monotone rise with pedal.

## Worked example: a copied-column placeholder
Copying a known-good MAP column's shape up into the unmapped boost columns with a flat
positive display-unit offset gets the **shape** right but the **offset direction** is
not physics-justified (only safe — biased rich). Trim the offset down to target lambda
once the columns are logged under load.
