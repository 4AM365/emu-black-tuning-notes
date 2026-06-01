# Knock-sensor baseline "grumble" is a proxy for cylinder-to-cylinder combustion uniformity

## Observation that prompted this
After improving per-cylinder fuel trims (FFIM maldistribution correction) on the Supra,
the knock-sensor signal went "dead smooth" under full boost — even with more timing.
There were never knock *spikes* before or after; what changed was that the baseline
noise level stopped "walking around." This is expected and is a sign of health.

## What the sensor measures
A knock sensor is a band-pass piezo accelerometer. The ECU windows around each
combustion event and measures **energy in the knock frequency band**, then compares it
to a rolling baseline. Two distinct things live in that channel:
- **Spikes** = single events above baseline (true/incipient knock).
- **Baseline wander / "grumble"** = the *variance* of the per-event noise floor.
  Mean can be fine while the spread scatters. This is what was "walking."

## Why maldistribution makes the baseline walk
Knock-band energy per event is driven by pressure-rise rate (dP/dθ), which is a strong
function of mixture:
- Leaner cylinders (the rear cyls before trim) burn **faster and hotter** → sharper
  dP/dθ, higher peak pressure, more HF content into the block → those events sit higher
  in the band.
- Lean cylinders sit closer to the **end-gas autoignition edge** → intermittent *trace*
  knock that never crosses the spike threshold but lifts and jitters the noise floor.
- A **fixed cylinder-to-cylinder offset** (5/6 hotter every cycle) combined with the
  **higher COV of IMEP** of lean mixtures (less repeatable cycle-to-cycle) makes the
  windowed energy oscillate = the "walk."

So pre-trim knock-channel wander was real combustion non-uniformity bleeding through —
information, not sensor noise.

## Why equalizing AFR flattens it
Matched per-cylinder lambda produces:
1. **Uniform per-event band energy** — all cylinders present the same dP/dθ, so the
   windowed measurement repeats instead of sawtoothing.
2. **No cylinder near the edge** — pulling lean cyls back removes the trace-knock
   contribution lifting the floor.
3. **Lower COV** — well-fueled cylinders burn more repeatably, collapsing the spread.

Added timing + tighter fuel control reinforce this: consistent charge cooling and flame
speed → consistent phasing → consistent acoustic signature.

## Tuning takeaway
A flat, smooth knock-band baseline at max power is the acoustic fingerprint of all
cylinders doing the same thing every cycle. Watch knock-channel **variance**, not just
spike count, as a uniformity/health metric — it can reveal maldistribution or a
cylinder near the edge before any spike appears.

Related: [[project_supra_per_cylinder_trim]], [[emu_ve_table_is_fuel_dose_proxy]]
