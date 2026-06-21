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

## Load/RPM shape — the harmonic (acoustic) reinterpretation
The per-cylinder modulation (the small **bump** on top of the geometric DC bias) is an
intake **acoustic resonance** effect, and resonance lives on the **RPM axis**, not the load
axis. Grounding: Heywood (VE is set by intake gas dynamics, `corpus/ice_fundamentals.md`
§2.10/6.2); Bell runner-length-vs-speed + symmetry→equal distribution
(`maximum-boost/chapter-06-intake-manifold.md` L67–82); Bell wave/inertia tuning is
RPM-tuned and sharp near resonance (`corpus/four_stroke_performance.md` L4602–4612). The
per-cylinder *synthesis* below is reasoned from those blocks (model knowledge), not quoted.

Two gas-dynamic mechanisms make VE — and the cylinder-to-cylinder SPREAD — speed-dependent:
- **Inertial ram:** broadband, grows with port velocity; rams charge past the valve after BDC.
- **Acoustic / Helmholtz tuning:** narrowband, RPM-selective. The runner+plenum resonator
  returns a pressure wave to the valve near IVC, peaking VE at a discrete resonance RPM
  (`f ≈ a/4L` organ-pipe; `f_H = (a/2π)√(A/(V·L))` Helmholtz). One intake event per cyl per
  two crank revs sets the engine-order link from acoustic frequency to RPM.

On a **shared-plenum inline-6** (central throttle, log plenum — the FFIM case) each runner
taps the plenum at a different axial station, so each intake valve sees a different
phase/amplitude of the plenum standing wave at IVC → different trapped mass per cylinder.
That difference IS the maldistribution; it **peaks at the plenum/runner resonance RPM** and
can change sign across resonances. End cylinders sit near pressure antinodes, center near nodes.

Consequences for the trim tables:
- **Geometric DC bias** (mean front-to-rear split, fuel fall-out, heat) is ~RPM- and
  ~MAP-independent → hold it CONSTANT across the whole table.
- **Modulation** is RPM-resonant: it belongs **down the RPM axis**, peaking in the resonant
  band and tapering above it — NOT spread across the load axis, and NOT a monotonic
  "worsens with airflow" ramp (this supersedes the earlier future-refinement guess).
- **~Flat across MAP at fixed RPM:** resonance RPM is set by geometry and sound speed
  `a=√(γRT)` — by charge *temperature*, not manifold *pressure*. Higher MAP raises wave
  amplitude slightly (stronger effect) but barely moves the resonance RPM; charge-temp
  (heat-soak, un-intercooled boost) nudges it UP a little (∝√T).
- **Load is the wrong axis for it, especially in boost:** above ~4500 rpm a turbo can hold
  any MAP at any RPM, so MAP stops proxying RPM. A resonance encoded on the load axis smears
  across unrelated RPMs. Encode it on RPM.

Net: the genuinely-3D-correct table is approximately the **transpose** of a load-swept
build — near-constant in MAP, varying down RPM with a resonant hump. **Locate the hump
empirically** from per-cylinder lambda (or EGT) spread vs RPM in a steady log; do not infer
it from where a load-line build happened to place the bump. Until then, RPM-flat (DC only)
is the honest default — a wrong-axis ramp is worse than none.

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
