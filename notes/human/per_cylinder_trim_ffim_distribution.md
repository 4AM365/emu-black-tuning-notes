# Per-cylinder trim on the front-feed manifold

> Digest of [per_cylinder_trim_ffim_distribution.md](../per_cylinder_trim_ffim_distribution.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** building the four `fuelTrimNTable`s to correct front-to-rear FFIM maldistribution, which axis the variation actually lives on, and how to validate with EGT.

**The rules:**

- Front cylinders fill richest; the lean trend accelerates toward the rear (~15% richest-to-leanest typical). Mid-rear cylinders are often the HOTTEST — bias unmeasured mid-rears rich.
- Front cylinder = 0% reference. Anchor each EGT-probed cylinder from its measurement; extrapolate the rest along the front-to-rear curve.
- The DC bias (mean front-to-rear split) is roughly RPM- and MAP-independent — hold it constant across the whole table.
- The modulation on top is intake acoustic resonance, so it lives on the RPM axis, not load. Encoding it on MAP smears it across unrelated RPMs once boost decouples MAP from RPM. Until the resonant hump is located empirically, RPM-flat (DC only) is the honest default.
- Pre-trim: an EGT delta that shrinks as load rises is real maldistribution, not probe offset (an offset would be load-constant). A residual constant cruise delta needs a one-time probe swap to separate lean cylinder from probe error.
- Post-trim: rear-minus-front EGT inside ~±20 °C is good; trimmed cylinder slightly colder means over-trimmed — back off toward measured values.
- The `Injector N trim` log channel reports flow scaling, not trim output — you can't read active trim % back from it.
- Never over-enrich the global lambda/VE target to protect a lean cylinder — the trims already correct distribution.

**Key numbers:** 4 tables, sbyte 5×5 in direct %, assigned via `fuelCylNTrimTableIdx` (0 = reference). Keep two rear cylinders on separate tables even if identical, so one can split off when it gets a probe.

**When to care:** setting up or revising per-cylinder trims, reading EGT spreads, or whenever tempted to fix a lean rear cylinder with global enrichment.
