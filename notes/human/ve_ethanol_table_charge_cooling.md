# VE tables are fuel-dose, not air physics

> Digest of [ve_ethanol_table_charge_cooling.md](../ve_ethanol_table_charge_cooling.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why the EMU VE table is a fuel-dose value rather than true volumetric efficiency, and why the pump-vs-ethanol table gap is a dosing choice, not a charge-cooling signature.

**The rules:**

- EMU's VE table computes fuel dose; it's only a rough proxy of physical VE. So the difference between the pump and ethanol maps is set by mixture intent and measured lambda, not air physics.
- `veTable2` reading LOWER than `veTable` at high load is expected — leaner ethanol targets mean lower values. It is not a physics violation; don't "fix" it.
- The big ethanol fuel increase (~+57% at E100, ~+44% at E85) is applied automatically by `ethanolFuelScale` (indexed by `ethanol10Bins`), separate from VE. VE2 carries only the residual dosing trim.
- V2 firmware has no table — the scalar `ethanolScaleFactor` does the job (e.g. raw 16400 ≈ 1.64×). Read the displayed value: ~1.6 = active and VE2≈VE1 is correct; ~1.0 = effectively off, and VE2 must carry the stoich itself.
- Never bulk-add ~50% to `veTable2` while the ethanol scale is active — it double-counts and runs dangerously rich.
- Air-VE physics still shapes each map (the load-axis knee, the RPM hump are real); it just doesn't dictate the offset between the two flex tables.
- If your logs were captured at low ethanol content, high-load `veTable2` is unverified — the blend gave it no authority. Confirm against delivered lambda on a high-ethanol boost pull.

**Key numbers:** E100 stoich fuel increase ≈ +57%, E85 ≈ +44%. Supra V3 `ethanolFuelScale` verified: E100 raw 0xE3 = 227 at ×0.25 scale ≈ +57%.

**When to care:** comparing `veTable` vs `veTable2`, tuning after a high-ethanol fill-up, or any time a "charge cooling should raise ethanol VE" argument surfaces.
