# Hood removal vs charge temps

> Digest of [hood_removal_charge_temps.md](../hood_removal_charge_temps.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** what removing the hood actually did to intake temps (validated May 2026), plus the sensor-channel corrections you need before reading any temperature out of these logs.

**The rules:**

- Removing the hood drops intake charge temp **~5–8 °C (10–15 °F)** at matched ambient, biggest at idle.
- `Charge temp` == IAT, row-for-row — it's the physical manifold sensor, not a coolant-blended model. Treat it as real intake-air temp.
- `Pre IC temperature` was logged on the wrong cal curve and reads ~30 °C too cold. Corrected, Pre-IC is the **hottest point in the tract** (~50–58 °C at hot idle), not cool inlet air. Fix via `emu-black-temp-sensor-recal`.
- `Ambient temperature` and `Post IC temperature` are unwired (flat −40 °C). Pull ambient from weather archives instead.
- The hood does not fix manifold soak: the ~11 °C real conduction rise across the plenum is identical hood-on and hood-off. Hood removal only lowers the level of the air coming in.
- Drive composition dominates manifold temp — 12 °C swing from soak time alone at the same ambient. Compare idle-vs-idle, always.
- OneDrive re-saves reset file CreationTime and break the ambient-lookup method — name logs `YYYYMMDD_HHMM`.

**Key numbers:** idle Charge/IAT −5 to −8 °C hood-off; corrected Pre-IC −6.2 °C at idle; hood-off data is n=1 (a hot-day hood-off idle log would firm it up).

**When to care:** reading any charge/IAT/Pre-IC value from a log, or weighing whether hood venting is worth the trouble.
