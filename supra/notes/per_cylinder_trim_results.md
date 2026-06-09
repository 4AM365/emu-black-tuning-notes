# Per-cylinder fuel trim — Supra worked values (2JZ FFIM)

Build-specific values, anchors, and measured EGT deltas behind the generic method note [`notes/per_cylinder_trim_ffim_distribution.md`](../../notes/per_cylinder_trim_ffim_distribution.md). The generic note holds the EMU mechanism and the front-feed distribution model; this file holds this car's numbers.

## Setup
- 6 injector channels (injCyl1..6 = 1..6). 4 trim tables `fuelTrim1..4Table`, sbyte 5×5, axes `fuelTrimRPM` [1000,2000,4000,6000,8000] × `fuelTrimLoad` [20,75,130,185,240] kPa.
- Assignment: cyl1,2 → idx0 (0%/reference); cyl3→1, cyl4→2, cyl5→3, cyl6→4.

## Anchoring (only cyl3 + cyl6 EGT available; no EGT-to-CAN module yet)
- cyl1 = 0% (richest, reference) ; cyl3 = measured anchor ; cyl6 = cyl3 + 10% (Will's requirement for equal charge temp between 3 and 6).
- cyls 2,4,5 = extrapolated along the front-to-rear curve, biasing 4 & 5 RICH (unmeasured + literature flags them hottest). cyl5 ≈ cyl6.
- Worked profile (2026-05-31): cyl1 0, cyl2 0, cyl3 +2, cyl4 +7, cyl5 +12, cyl6 +12. The +10% cyl6-vs-cyl3 relationship holds at every load cell (shared load shape).

## Load shape (per table)
`M + [-1,+1,0,0,-1]` across load = small cruise bump (peak at 75 kPa), tapering −1 at idle (20) and full boost (240). FFIM maldistribution worst at cruise, eases under boost. Kept mild (±1), RPM-flat.

## Output (`cyl_trim_FFIM_extrapolated.emubt`, 4 symbols — values only, no idx changes)
- fuelTrim1Table (cyl3): [1,3,2,2,1]
- fuelTrim2Table (cyl4): [6,8,7,7,6]
- fuelTrim3Table (cyl5): [11,13,12,12,11]
- fuelTrim4Table (cyl6): [11,13,12,12,11] (cyl5/6 identical; kept separate so cyl5 can split off once it has its own EGT)

## CURRENT STATE = near parity (test-run-2.csv, post-trim — the truth)
With Will's 2% cyl3 / 9% cyl6 trim ACTIVE, cyl6−cyl3 (EGT2−EGT1) per region: idle −7, light −3, cruise −14, transition −10, boost(130–176, n=316) −20 °C. All within ±20 °C, cyl6 now slightly COLDER (mildly over-trimmed at boost ~−1%). **Will's 2%/9% choice is validated.** ⇒ the rich-biased export (cyl6 +13 cruise, cyl4/5 +7/+12) is TOO RICH; revert cyl6 to ~9% ([7,9,8,8,7], maybe shave boost cell −1) and use proportionate cyl4/5 (~+5/+7, at most +1 safety bias), NOT +7/+12.

## PRE-TRIM reference (drive_home_today.csv) — historical, NOT current
Before the cyl6 trim, EGT delta was load-dependent, shrinking as load rises: light/cruise +44 °C → cruise +32 → transition +19 → boost(130–160) +12 °C. **Because the delta SHRINKS with load instead of staying flat, most of it is real airflow maldistribution, NOT a fixed sensor offset.** Caveats: boost segment ~2 s/36 samples (EGT lag, parity unconfirmed); idle/overrun includes fuel-cut decel artifacts. Residual ~+30–44 °C at cruise = either cyl6 still slightly lean OR ~15–20 °C probe offset; a one-time 3↔6 probe swap is the only way to separate them.

## Next step
cyls 2,4,5 are EXTRAPOLATED, not measured. Biggest risk: cyl4/5 leaner than estimated with no EGT to catch it. Priority: get the EGT-to-CAN module so probes on 4 and 5 can be read, then replace the extrapolated mid-rear values with measured trims.
