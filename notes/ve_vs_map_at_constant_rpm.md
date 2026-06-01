# VE vs MAP at constant RPM, and copying RPM shape across boost columns

## Principle: cam-resonance VE peak is an RPM phenomenon, copy it across all MAP columns
The 1FZ... (Supra 2JZ) cams make the engine resonate at ~5500 rpm — peak cylinder
filling. Evidence: at constant ignition timing and boost, knock first appears at 5500
(max trapped mass → max end-gas compression/heating → knock-prone). Because resonance
is set by RPM (cam/runner tuning), the **VE-vs-RPM contour shape does not move with
manifold pressure**. So stamping a known-good column's RPM shape (e.g. the well-mapped
167 kPa column, peak at 5289–5632 bins) onto an unmapped high-boost column (240 kPa) is
methodologically correct — better than interpolating *through* the resonance peak.

## Principle: VE at higher MAP (same RPM) trends flat-to-DOWN, not up
"The compressor loves pressure ratio" describes the **compressor's** flow/efficiency —
it is decoupled from cylinder VE by the plenum. VE is normalized to manifold density, so
once air is in the plenum at 240 kPa, cylinder filling is governed by:
- **Exhaust backpressure** (turbo): higher at 240 kPa → worse scavenging → lowers trapped VE.
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

## Fuel-model confirmation (2026-05-31)
`lambdaTable` on this build is **only a tuning reference + closed-loop STFT target** — it
is NOT a fuel-equation multiplier (see `notes/fueling.md`). So `veTable` IS the dose and
must carry enrichment by hand. Verdict for high-boost columns: the dose offset between
two MAP columns SHOULD be added (no double-count risk), and its correct size =
(air-VE ratio 240/167) × (target-λ enrichment 167→240). Measured at 5000 rpm: lambda
0.79 @160 → 0.77 @200 (table tops out at 200 kPa, flat to 240) = +2.6% enrichment. With
air VE flat-to-down, the honest dose offset is ≈ +2.6% (≈ +2.0 display units on ~78),
NOT the +4.5% (+3.5 units) applied in ve1_copied_boost.emubt — roughly 2× too rich.

## Working correction model (used on ve2, 2026-05-31)
To rebuild a high-boost column from a known-good anchor column (here 167 kPa) so it is
consistent with target lambda AND engine efficiency, with NO log data:

    dose(m,rpm) = dose(anchor,rpm) * enrich(m,rpm) * VEeff(m,rpm)

- `enrich = lambda_target(anchor)/lambda_target(m)` — from `lambdaTable2` (ethanol),
  bilinear, with the boost slope **linearly extended above 200 kPa** (table tops out at
  200; intended target keeps richening). Richer m -> enrich > 1.
- `VEeff = 1 - k(rpm)/100 * (m-anchor)/100` — theoretical air-VE roll-off into boost.
  `k` is %/100 kPa, RPM-weighted because EMAP/charge-heat hurt most at high rpm:
  `k(rpm)=clip(0.5 + (rpm-2500)/4500*2.5, 0.5, 3.0)` -> 0.5 %/100kPa at <=2500 rpm,
  ~1.9 at 5000, 3.0 at 7000. VEeff <= 1.

Net behavior (the whole point): at LOW rpm enrich dominates (offset stays ~+4%); at HIGH
rpm VEeff cancels enrich (offset -> ~0, dose returns to the anchor). This pulls down the
high-rpm/high-boost corner where an eyeballed flat offset is always too rich. Finish with
a light [.25,.5,.25] RPM smooth on the rebuilt cols and enforce non-decreasing across MAP.
Output: `ve2_corrected_boost.emubt` (symbol veTable2). The k-schedule is a theoretical
placeholder — replace VEeff with measured air VE (EMAP log or wideband back-out) when
available.

## Verification method: veTable × λ_target = air-VE proxy (must be smooth)
Because `lambdaTable` is a reference/STFT target, NOT a fuel multiplier, the dose
veTable must carry 1/λ enrichment by hand. The cheap whole-table check:
`air_VE_proxy(m,rpm) = veTable(m,rpm) × λ_target(m,rpm)`. Interpolate the λ table onto
the VE grid and form the product across MAP at each RPM. A correct VE shape yields a
**smooth** surface: rises out of the idle/vacuum region, peaks near the torque-MAP band
(~80–110 kPa), then tapers gently into boost (EMAP/charge-heat roll-off). A **dip or
step at the boost knee** (where λ_target starts dropping ~100 kPa) means the veTable did
NOT receive the extra fuel the (newly expanded) λ targets demand — i.e. shape mismatch.
Script: `supra/scripts/verify_ve_vs_lambda.py`.

## Case (2026-05-31): 05312026 supra v2 — expanded-lambda VE shape PASSES
Ran the product test on the v2 export against the expanded lambdaTable/lambdaTable2.
All three checks (VE1×λ1 pump endpoint, VE1×λ_E60 blend, VE2×λ2 ethanol endpoint)
produce a clean monotone-rise-then-gentle-taper air-VE proxy with NO kink at the boost
enrichment onset. So the dose VE rose as ~1/λ through the boost columns — the VE table
shape DOES track the new lambda targets; enrichment is baked into veTable, no double
count, no gap. Boost confirmed referenced to pedal/TPS: `boostTarget1/2` X axis =
`ppsBoostBins` (0→98 %), col0 (closed throttle)=0 boost, monotone rise with pedal, flat
3500–5500 then slightly higher 6000–7000; E60 blend (52% t1 / 48% t2) tops ~102–111 kPa.

## Case (2026-05-31): ve1_copied_boost.emubt
Copied 167 kPa column shape → 167–240 kPa columns; ~+3.5 display-unit offset (≈+4.5%
relative) in the 4600–5600 band, flaring to +4 at the rpm extremes. Shape copy: correct.
Offset direction: not physics-justified, but safe. Trim down to target lambda once logged.
