# Knock baseline grumble = cylinder uniformity

> Digest of [knock_sensor_baseline_vs_cylinder_uniformity.md](../knock_sensor_baseline_vs_cylinder_uniformity.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why the knock channel's baseline wander — not its spikes — tells you whether all cylinders are burning alike, and why per-cylinder trims flatten it.

**The rules:**

- Two signals live in the knock channel: spikes (true/incipient knock) and baseline wander — the variance of the per-event noise floor. The mean can look fine while the spread scatters.
- Lean cylinders burn faster and hotter (sharper pressure rise, more high-frequency energy into the block) and sit near the autoignition edge — intermittent trace knock lifts the floor without ever crossing the spike threshold.
- A fixed cylinder-to-cylinder offset plus the higher cycle-to-cycle COV of lean mixtures makes the windowed energy oscillate. That "walk" is real maldistribution information, not sensor noise.
- Equalizing per-cylinder lambda flattens it three ways: uniform per-event band energy, no cylinder near the edge, lower COV. On this build the channel went dead-smooth after per-cylinder trims — even with more timing.
- A flat, smooth baseline at max power is the acoustic fingerprint of health. Watch variance as a uniformity metric — it flags a cylinder near the edge before any spike appears.

**When to care:** after changing per-cylinder fuel trims, and whenever the knock baseline starts walking at high load — chase fuel distribution before blaming the sensor or pulling timing.
