# Tables switching (flex-fuel blend)

> Digest of [tables_switching.md](../tables_switching.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how the dual pump/ethanol table sets (VE, ignition, cam, cold-start) blend by ethanol content, and how to work on them without fighting the blend.

**The rules:**

- Derive the blend curve from EMU's ethanol fuel scale, never by eye: table-1 weight = 1 − `ethanolFuelScale`(E) / `ethanolFuelScale`(100), in raw counts. The curve is nonlinear — a straight line mistimes the handoff.
- Tune the endpoints, not the blend. To change mixture or timing at a given ethanol content, edit table 2 (the E100 endpoint) and let the blend interpolate. Reshaping the blend curve to "get more timing" is the classic mistake.
- The blend scalar is below 1 at any partial content, so an endpoint delta delivers proportionally less at the wheel — account for the fraction when stepping values.
- Identical endpoints mean the blend does nothing. VE2 below VE1 at high load is the point of the blend (ethanol runs leaner fuel-dose values), not a bug.
- Cold-enrichment blends are not stoichiometric compensators — they only pace the E0→E100 extra-enrichment handoff. The wall-film tax is most ethanol-forward at cranking: table-1 weight runs Warmup ≥ ASE ≥ Cranking at the same content.
- Confirm each domain's blend mode before editing values — additive vs scalar vs blended changes what the stored bytes mean.
- Any ethanol reading 0–100% is valid on this build (fill-ups vary); only flag a flex-sensor dropout, never an unusual content value.

**Key numbers:** blend curves are stored ubyte at 0.5% resolution.

**When to care:** editing VE2 / ignition table 2 / cold-enrichment tables, touching any blend curve, or diagnosing mixture or timing drift that tracks ethanol content.
