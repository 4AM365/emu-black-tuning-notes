# Per-cylinder fuel trim distribution on a front-feed intake manifold (FFIM)

> **Car-specific values live in the build working docs**, not here. For the reference build's measured trim profiles, EGT anchors, and table values see [`supra/notes/per_cylinder_trim_results.md`](../supra/notes/per_cylinder_trim_results.md). This note is intentionally car-agnostic.

## EMU mechanism
- 4 trim tables: `fuelTrim1..4Table`, each **sbyte 5x5** (% direct), with `fuelTrimRPM` ×
  `fuelTrimLoad` (kPa) axes. Set the axis bins to bracket this engine's idle/cruise/boost.
- Assignment scalars `fuelCylNTrimTableIdx`: 0 = no table (0% / reference), 1..4 = that
  table. One table can serve multiple cylinders (set two cyls to the same idx).
- Use one injector channel (`injCylN`) per cylinder.

## Distribution model (front-feed intake manifold)
With the throttle body at the FRONT, air travels down the log plenum, so front cylinders
fill richest and the lean trend accelerates toward the rear. Literature: per-cyl spread
~15% richest-to-leanest typical; the mid-rear cylinders are often the HOTTEST (not always
the last one). EGT is also moved by ignition trims + sensor placement, so read EGT as a
guide not gospel.

Anchoring method when only a subset of cylinders has EGT probes:
- Front cylinder = 0% (richest, reference; trim UP toward the rich cyl convention).
- Each measured cylinder = its own anchor from EGT.
- Hold a fixed charge-temp delta between a front measured cyl and a rear measured cyl
  (the build's chosen target delta) and let it set the rear trim.
- Unmeasured cylinders = extrapolated along the front-to-rear curve, **biasing the
  unmeasured mid-rear cyls RICH** because (a) they're unmeasured and (b) literature flags
  them as the hottest.

A constant front-to-rear trim delta holds at EVERY load cell because all tables share one
load shape. This build's actual per-cylinder trim percentages and worked profile are in
`supra/notes/`.

## Load shape (per table)
Apply a per-table load shape of the form `M + [-1,+1,0,0,-1]`: a small **cruise bump**
(peak at the cruise load bin), tapering -1 at idle and at full boost. Rationale: FFIM
maldistribution is worst at cruise (inertia/resonance dominated) and eases under boost
(boost forces even filling). Keep it mild (+/-1) and RPM-flat unless data supports more.
Future refinement: add RPM dependence (maldistribution worsens with airflow) once more EGT
data exists.

## Output / assignment
Export one `.emubt` with the 4 `fuelTrimNTable` symbols. Assign each cylinder to a table
index via `fuelCylNTrimTableIdx`; only the table VALUES change between revisions, not the
index map. Keep two rear cyls on separate tables (even if identical values) so one can be
split off once it gets its own EGT probe.

## Validating against post-trim EGT
After applying trims, log EGT and compute the rear-minus-front EGT delta per load region. A
result inside a tight band (e.g. ±20 °C) with the trimmed cyl slightly COLDER means mildly
over-trimmed — back the rich bias off toward the measured-correct values rather than the
safety-biased extrapolation. The build's actual measured deltas live in `supra/notes/`.

## Diagnosing offset vs real maldistribution (pre-trim)
Before trimming, if the front-to-rear EGT delta is **load-dependent and shrinks as load
rises**, most of it is real airflow maldistribution, NOT a fixed sensor offset (an offset
would be load-constant). This also validates the cruise-peaked / boost-tapered load shape.
Caveats: short boost segments are thermally unsettled (EGT lag) so boost parity needs a
sustained pull; idle/overrun includes fuel-cut decel artifacts. A residual constant delta at
cruise is either a still-slightly-lean rear cyl OR a probe offset; a one-time probe swap is
the only way to separate them. Note the `Injector N trim` channel reports flow scaling, not
cyl-trim output, so it can't be used to read back active trim %.

## Caveat / next step
Unmeasured cylinders are EXTRAPOLATED, not measured. The biggest risk is an unmeasured
mid-rear cyl running leaner than estimated (lit. says they can be the hottest) with no EGT
to catch it. **Priority: get enough EGT channels (e.g. an EGT-to-CAN module) to read every
mid-rear cyl, then replace the extrapolated values with measured trims.** Per-cyl trims
correct distribution, so the GLOBAL lambda/VE target must NOT be over-enriched for the lean
cylinder.
