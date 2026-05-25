# FFIM Fuel Distribution

Note that front-feed intake manifolds (FFIMs) are terrible for airflow distribution. It's essentially equal at idle, but as soon as you get some air mass inertia going, the distribution will become severely uneven. Common inline-6 FFIMs typically need around 10% more fuel on the rearmost cylinder. Notice that your rear EGTs are always hotter and the rear cylinder knocks first — this is why. The max fuel trim will be needed in the cruise region, and you can taper off to about half of that under boost since airflow becomes dominated by boost forcing air into the cylinder rather than resonant effects even though they're still present.

---

## Acceleration Enrichment

### When Accel Enrichment Is NOT the Right Tool

- Gentle throttle transitions at idle/low RPM happen slowly enough that the VE table handles them. Wall-wetting occurs gradually, fuel vaporizes with time. Over-enriching here causes a bog, not a cure.
- Accel enrichment is for **transient spikes**, not gradual transitions.

### Table Structure (EMU Black)

- Table 1: Accel enrichment % (axes: TPS rate of change vs. RPM) — how much enrichment to add.
- Table 2: Enrichment correction % (often load/MAP-based) — when to reduce it.
- Higher TPS rate of change = more enrichment. Lower RPM at the same rate = more enrichment needed (worse wall wetting at low port velocity).

### Test Cases for Logging

1. Gentle snap from idle (rolling, ~1000 RPM, vacuum)
2. Part-throttle snap at cruise (2000–3000 RPM, light load)
3. Throttle snap mid-range (3500 RPM, atmospheric)
4. Post-DFCO throttle spike (high RPM, vacuum → boost)
5. Rolling into boost (high RPM, already in boost)