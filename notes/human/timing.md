# Ignition timing — the deep reference

> Digest of [timing.md](../timing.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** what timing is trying to do (CA50 at MBT), how cams, fuel, and load move the target, and the working method for cruise, boost, and the flex blend.

**The rules:**

- The whole game is putting CA50 (half the fuel burned) at ~8° ATDC — that's MBT. Too advanced and peak pressure fights the piston: torque falls, EGT rises.
- Keep two fuel properties separate: octane sets knock resistance; burn rate sets how much advance MBT needs. Ethanol wants ~3–8° more timing, and it barely knocks — there the limit is torque, not detonation. Peak anti-knock is ~E60.
- More cam overlap dilutes the charge with exhaust, so idle/low-load cells need more advance: 10–12° pump/stock up to 19–22° ethanol/big cams.
- Find cruise MBT experimentally with an EGT sensor — lower EGT means closer. MAP rising at constant pedal confirms a gain; lambda hunting means you went too far. Then flatten the cruise MAP band into a ~1° plateau so MAP wander doesn't become torque roughness.
- Table shape: lose ~2° per 30 kPa across MAP (peak near 20 kPa), add timing up the RPM axis. Boost MBT on a 4-valve DOHC I6 sits in the low-20s° BTDC.
- Never reshape the flex blend table to dial in timing — advance Table 2 instead, and remember the blend fraction (<1 at partial ethanol) scales what actually reaches the wheel.
- Lock cam advance per cell before pulling for MBT, and re-verify ignition anywhere you change cam advance — the tables are coupled.
- Cruise lambda target is 1.0. Lean of stoich on a cammed port-injected engine risks instability for no real economy gain.

**Key numbers:** the theoretical MBT tables (238°/264°/272° cams, E0 + E100) are for *shape only* — subtract knock retard before running them. Walk boost timing up in 1° steps on per-cylinder knock + EGT. Blend curve: ~14%/86% at E62.5, 0% Table 1 by ~E75.

**When to care:** any time you set or move an ignition cell — idle, cruise, boost walk-up — or after a cam, fuel, or boost change.
