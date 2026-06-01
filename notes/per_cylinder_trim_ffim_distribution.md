# Per-cylinder fuel trim distribution on the 2JZ FFIM (4 tables, 6 cylinders)

## EMU mechanism
- 4 trim tables: `fuelTrim1..4Table`, each **sbyte 5x5** (% direct), axes `fuelTrimRPM`
  [1000,2000,4000,6000,8000] x `fuelTrimLoad` [20,75,130,185,240] kPa.
- Assignment scalars `fuelCylNTrimTableIdx`: 0 = no table (0% / reference), 1..4 = that
  table. One table can serve multiple cylinders (set two cyls to the same idx).
- Supra uses 6 injector channels (injCyl1..6 = 1..6).

## Distribution model (front-feed intake manifold)
Throttle body at the FRONT (cyl1 end); air travels down the log plenum, so front cylinders
fill richest and the lean trend accelerates toward the rear (cyl 5/6). Literature: per-cyl
spread ~15% richest-to-leanest typical; mid-rear (4,5) often HOTTEST (~100C, 920-950C), not
always 6. EGT also moved by ignition trims + sensor placement, so read EGT as a guide not gospel.

Anchoring with only cyl3 + cyl6 EGT (no EGT-to-CAN module yet to multiplex the other probes):
- cyl1 = 0% (richest, reference; matches existing convention of trimming UP to the rich cyls)
- cyl3 = measured anchor
- cyl6 = cyl3 + 10% (Will's requirement for equal charge temp between 3 and 6)
- cyls 2,4,5 = extrapolated along the front-to-rear curve, **biasing 4 & 5 RICH** because
  (a) they're unmeasured and (b) literature flags them as the hottest. Treat cyl5 ~= cyl6.

Worked profile (2026-05-31): cyl1 0, cyl2 0, cyl3 +2, cyl4 +7, cyl5 +12, cyl6 +12.
The +10% cyl6-vs-cyl3 relationship holds at EVERY load cell because all tables share one
load shape.

## Load shape (per table)
`M + [-1,+1,0,0,-1]` across load = small **cruise bump** (peak at 75 kPa), tapering -1 at
idle (20) and full boost (240). Rationale: FFIM maldistribution is worst at cruise (inertia/
resonance dominated) and eases under boost (boost forces even filling). Kept mild (+/-1) and
RPM-flat to match existing tables. Future refinement: add RPM dependence (maldistribution
worsens with airflow) once more EGT data exists.

## Output / assignment
File `cyl_trim_FFIM_extrapolated.emubt` (4 symbols). **No idx changes needed** - keep
cyl1,2 -> idx0; cyl3->1, cyl4->2, cyl5->3, cyl6->4. Only the table VALUES change:
- fuelTrim1Table (cyl3): [1,3,2,2,1]
- fuelTrim2Table (cyl4): [6,8,7,7,6]
- fuelTrim3Table (cyl5): [11,13,12,12,11]
- fuelTrim4Table (cyl6): [11,13,12,12,11]   (cyl5 & cyl6 identical now; kept separate tables
  so cyl5 can be split off once it has its own EGT)

## CURRENT STATE = NEAR PARITY (test-run-2.csv, post-trim, the truth)
With Will's 2% cyl3 / 9% cyl6 trim ACTIVE, cyl6-cyl3 (EGT2-EGT1) per region:
idle -7, light -3, cruise -14, transition -10, boost(130-176, n=316) -20 C. All within
+/-20C and cyl6 now slightly COLDER (mildly over-trimmed, most at boost ~ -1%). **Will's
2%/9% choice is validated.** => The rich-biased export (cyl6 +13 cruise, cyl4/5 +7/+12) is
TOO RICH; revert cyl6 to ~9% (his [7,9,8,8,7], maybe shave boost cell -1) and use
proportionate cyl4/5 (~+5/+7, at most +1 safety bias), NOT +7/+12.

## PRE-TRIM reference (drive_home_today.csv) - historical, NOT current
Before the cyl6 trim, EGT delta was load-dependent, shrinking as load rises:
light/cruise +44C -> cruise +32 -> transition +19 -> boost(130-160) +12C. This validates
the cruise-peaked / boost-tapered load shape: FFIM maldistribution is inertia/resonance
driven (worst light load) and boost forces even filling (gap closes). 
**Key inference: because the delta SHRINKS with load instead of staying flat, most of it is
real airflow maldistribution, NOT a fixed sensor offset** (an offset would be load-constant).
Caveats: boost segment was ~2s/36 samples = thermally unsettled (EGT lag), so boost parity
is unconfirmed - needs a sustained pull; idle/overrun includes fuel-cut decel artifacts.
Residual ~+30-44C at cruise = either cyl6 still slightly lean (9% a hair light) OR ~15-20C
probe offset; a one-time 3<->6 probe swap is the only way to separate them. Could NOT read
active trim % from the log (Injector N trim channel = 100 = flow scaling, not cyl-trim output).

## Caveat / next step
cyls 2,4,5 are EXTRAPOLATED, not measured. The biggest risk is cyl4/cyl5 running leaner than
estimated (lit. says they can be the hottest) with no EGT to catch it. **Priority: get the
EGT-to-CAN module so probes on 4 and 5 can be read; then replace the extrapolated mid-rear
values with measured trims.** Per-cyl trims correct distribution so the GLOBAL lambda/VE
target must NOT be over-enriched for the lean cylinder (see project_supra_per_cylinder_trim).
