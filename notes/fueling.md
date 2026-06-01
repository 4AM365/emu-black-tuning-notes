# Fuel model: veTable is the dose, lambdaTable is NOT a multiplier

On this Supra build, the fuel equation does **not** divide the dose by the lambda
target. `lambdaTable` is **only a tuning reference and the target for the closed-loop
STFT** (short-term fuel trim) — the firmware does not multiply `veTable` by
(stoich/target) to hit it open-loop.

**Consequences:**
- `veTable` is the actual **fuel dose** and must carry mixture itself — it is air-VE ×
  whatever enrichment you want (this is why veTable2 reads leaner/lower for ethanol, and
  why the dose can legitimately rise into boost while pure air VE rolls off).
- When you copy a column's shape across MAP, you must **add the desired lambda
  enrichment by hand** — it does not come for free from `lambdaTable`. The correct
  offset = (air-VE ratio) × (target-λ enrichment between the two MAP columns).
- Changing `lambdaTable` alone only moves the STFT target; it does not reflux fuel
  open-loop. Real mixture changes are made in `veTable`.

---

# FFIM Fuel Distribution

Note that front-feed intake manifolds (FFIMs) are terrible for airflow distribution. It's essentially equal at idle, but as soon as you get some air mass inertia going, the distribution will become severely uneven. Common inline-6 FFIMs typically need around 10% more fuel on the rearmost cylinder. Notice that your rear EGTs are always hotter and the rear cylinder knocks first — this is why. The max fuel trim will be needed in the cruise region, and you can taper off to about half of that under boost since airflow becomes dominated by boost forcing air into the cylinder rather than resonant effects even though they're still present.

**This car corrects FFIM maldistribution with per-cylinder 3D fuel trim tables** — each
cylinder (including the lean/hot rears) is trimmed to target individually. Consequence:
do NOT over-enrich the GLOBAL lambda/VE target to protect the leanest cylinder; that's
already handled per-cylinder. Global enrichment choices (e.g. full-boost lambda) should be
sized for a well-distributed charge, not for the worst cylinder.

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