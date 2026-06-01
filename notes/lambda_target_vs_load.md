# Lambda target vs load: why the boost rolloff is ~linear, and where it isn't

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
A well-intercooled, not-heavily-retarded 2J at 240 kPa is likely still linear up top ->
coarse bins above the knee, dense bins at the knee.

## How rich to go at full boost (pump): enrichment benefits saturate
- Best-torque mixture ~phi 1.1 (lambda ~0.90), load-independent. Everything richer is
  protection, not power.
- Typical high-boost pump targets: lambda 0.72-0.80. 0.73 (AFR ~10.7, phi 1.37) is the
  rich/conservative end - supported, not exotic.
- **Charge-cooling AND knock-suppression benefit saturate ~lambda 0.76-0.78.** Below that
  you add fuel for little extra knock margin. What KEEPS paying past 0.78 is **EGT
  reduction** (turbine/valve protection). So 0.73 vs 0.77 is mostly an EGT/safety-margin
  buy, costing a little power + BSFC, with bore-wash/fouling/instability risk if sustained.
- Engine-specific reason to bias the pump table rich vs E: **pump gas has no ethanol
  evaporative cooling**, so it leans on fuel quantity for charge cooling -> pump table
  should sit richer than the E table (0.73 vs ~0.81).
- **NOT a reason: FFIM maldistribution.** This car runs **per-cylinder 3D fuel trim
  tables**, so each cylinder (incl. the lean/hot rears) is trimmed to target individually.
  The GLOBAL lambda target therefore does NOT need to be over-enriched to protect the
  leanest cylinder - distribution is already corrected per-cylinder. So 0.73 is purely an
  EGT/safety-margin choice; on a per-cyl-trimmed charge, 0.75-0.76 would hold knock as well
  with more power. (Earlier note claiming FFIM justifies the rich bias was wrong - corrected.)

## Resulting MAP bin recommendation (fixed 8-column lambda axis)
`20, 50, 80, 100, 130, 160, 200, 240`
- 130 = the knee (kept); 100/130/160 bracket the MBT->protection transition.
- 160/200/240 = 3 points for the linear rolloff, top bin on the veTable MAP boundary (240).
- 20/50/80 = idle/cruise where target is flat.
(Earlier I suggested using an empty 9th slot — there is no 9th column; the axis is fixed
at 8. Note corrected.)
