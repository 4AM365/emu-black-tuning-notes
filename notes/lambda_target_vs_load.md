# Lambda target vs load: why the boost rolloff is ~linear, and where it isn't

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`timing_targets.md`](../supra/notes/timing_targets.md) (boost/lambda targets). This note is intentionally car-agnostic.

## Two regimes
1. **Best-torque (MBT) mixture** — phi ~1.05-1.1 (lambda ~0.90-0.95), essentially
   **load- and speed-independent** for a given engine (Heywood, SI mixture requirements).
   In light boost you're near best-torque already; the target is flat, not sloped.
2. **Protection enrichment** (above MBT) — fuel added purely to cap a temperature: EGT
   (turbine/valves) or end-gas temp (knock), via evaporative + lower-flame-temp cooling.
   This is what grows with load.

## Why protection enrichment is ~linear in MAP
- Ideal gas at const VE, RPM: charge mass proportional to MAP (PV=mRT).
- Const phi + efficiency: **BMEP proportional to trapped fuel proportional to MAP** -> BMEP linear in MAP.
- Stoich-baseline EGT rises ~with load; rich-side adiabatic flame temp falls ~linearly
  with phi (1.0->1.3), so each increment of fuel buys ~constant deltaT. Holding a fixed
  EGT cap with baseline ~linear in MAP + constant deltaT/fuel => **required enrichment
  ~linear in MAP.** So 160->240 kPa can be a straight lambda rolloff (interp endpoints);
  dense bins there are wasted.
- Pedantic: it's fuel fraction phi that's linear; lambda=1/phi, but over lambda 0.84->0.80
  the 1/x curvature is negligible.

## Where linearity breaks (needs bins / attention)
1. **MBT->protection knee** (early boost, ~120-160 kPa): the SLOPE changes here (flat
   best-torque -> sloped protection). Genuine kink -> this is why **130 kPa needs its own
   bin**; bracket it with 100/130/160.
2. **Knock wall:** retarding timing to survive spikes EGT -> enrichment demand accelerates
   (superlinear).
3. **Compressor/turbine limits:** out of the efficiency island IAT climbs nonlinearly; a
   choking turbine raises EMAP nonlinearly. Both steepen the top of the curve.
A well-intercooled, not-heavily-retarded engine at the top of its MAP axis is likely still
linear up top -> coarse bins above the knee, dense bins at the knee.

## How rich to go at full boost (pump): enrichment benefits saturate
- Best-torque mixture ~phi 1.1 (lambda ~0.90), load-independent. Everything richer is
  protection, not power.
- Typical high-boost pump targets sit in the lambda ~0.72-0.80 band; the rich/conservative
  end of that band is supported, not exotic. Pick this car's actual WOT target from the
  build doc (`supra/notes/my_car.md`).
- **Charge-cooling AND knock-suppression benefit saturate ~lambda 0.76-0.78.** Below that
  you add fuel for little extra knock margin. What KEEPS paying past 0.78 is **EGT
  reduction** (turbine/valve protection). So choosing the richer vs leaner end of the band
  is mostly an EGT/safety-margin buy, costing a little power + BSFC, with bore-wash/fouling/
  instability risk if sustained.
- Engine-specific reason to bias the pump table rich vs E: **pump gas has no ethanol
  evaporative cooling**, so it leans on fuel quantity for charge cooling -> the pump table
  should sit richer than the ethanol table.
- **NOT a reason: FFIM maldistribution.** When a build runs **per-cylinder 3D fuel trim
  tables**, each cylinder (incl. the lean/hot rears) is trimmed to target individually.
  The GLOBAL lambda target therefore does NOT need to be over-enriched to protect the
  leanest cylinder - distribution is already corrected per-cylinder. So the WOT richness is
  purely an EGT/safety-margin choice; on a per-cyl-trimmed charge, a slightly leaner target
  holds knock as well with more power. (Earlier note claiming FFIM justifies the rich bias
  was wrong - corrected.)

## Resulting MAP bin recommendation (fixed 8-column lambda axis)
Spend bins where the curve bends, not where it's straight. On the fixed 8-column lambda
axis a good distribution is: idle/cruise points where the target is flat, a dense cluster
bracketing the MBT->protection knee, and a few coarse points spanning the linear rolloff up
to the veTable MAP boundary.
- Put a bin ON the knee and bracket it on both sides (the MBT->protection transition).
- Only ~3 points are needed across the linear rolloff; top bin lands on the veTable MAP
  boundary.
- Idle/cruise bins cover the region where target is flat.
(This build's actual MAP axis values are in `supra/notes/`.)
(Earlier I suggested using an empty 9th slot — there is no 9th column; the axis is fixed
at 8. Note corrected.)
