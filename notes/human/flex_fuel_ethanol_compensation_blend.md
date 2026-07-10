# Flex-fuel blend curves

> Digest of [flex_fuel_ethanol_compensation_blend.md](../flex_fuel_ethanol_compensation_blend.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how to shape the table-switching blend curves when `ethanolFuelScale` already handles the stoich fuel-mass change, plus lambda endpoints and cold-start blends.

**The rules:**

- Derive the blend curve from the fuel-scale table itself: `table1_weight(E) = 1 − ethanolFuelScale(E)/ethanolFuelScale(100)`. It's nonlinear — table-1 weight falls faster than ethanol % rises. Never draw a straight line by intuition.
- Keep VE tables as airflow models. Correct VE only from measured lambda error (`VE_new = VE_old × measured/target`). A leaner Lambda Target 2 is a target-table choice, not a reason to cut 2% from VE2.
- Set two full-boost lambda endpoints — E0 and E100 — and let the blend interpolate. The ethanol endpoint can sit leaner: ethanol brings knock resistance and charge cooling that pump gas lacks.
- Don't jump the boost-entry columns (80–100 kPa) straight to full-boost richness. Shape the transition for smooth torque, then verify 130–200 kPa in steady high-load logs.
- Cold-start blends aren't stoich compensators — they only pace the move between E0 and E100 extra-enrichment. Ethanol-forwardness ranks Cranking > ASE > Warmup, so at the same ethanol %: warmup table-1 weight ≥ ASE ≥ cranking. One shared linear blend for all three is wrong.
- Don't assume E100 wants a leaner idle target just because it runs leaner under load. Idle on ethanol is limited by mixture prep (vaporization, wall film, overlap dilution) — tune idle for measured stability, not chemistry.

**Key numbers:** blend tables resolve to 0.5% (ubyte). Gasoline WOT best-torque band λ ~0.78–0.90 (Hartman); Banish's forced-induction mapping start is λ 0.77.

**When to care:** setting `tblsFFLambdaBlend` or `tblsVEBlend`, the cranking/ASE/warmup blend curves, or the E0/E100 full-boost lambda endpoints.
