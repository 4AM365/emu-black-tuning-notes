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

## Before/after from decoded autosaves (analysis 2026-10-02)

Source: 119 LogAutosave `.emublog3` files, 2026-03-01 → 09-29 (~25 h running), decoded with `skills/emu-black-log-emublog3/scripts/supra_decode_504.py`; 20 duplicate/empty autosaves dropped. Charts, data, scripts: [`supra/reports/2026-10-02_cyl6_trim_knock_boost/`](../reports/2026-10-02_cyl6_trim_knock_boost/).

**When the trim went in:** logged `Injector N trim` carries the trim-table output (100 = none). It is 100 on every cylinder through `20260504_1725_09` and 109 (cyl6) / 102 (cyl3) from `20260504_1738_14`: **2026-05-04 between 17:25 and 17:38**. Values moved 102–109 during May 4–11 while Will iterated, then settled.

**Periods (assigned per sample from `Injector 6 trim` and `Ethanol content`):** before E57 = Mar 29 → May 4 (631 min, 57 files); after E57 = May 4 → 10 (174 min, 10 files); after later = May 11 → Sep 29 (416 min, 32 files, E25 then E14); pump fuel Mar 1–29 (290 min) for EGT/boost context only. Ethanol was 56–57 % on both sides of the switch, so before E57 vs after E57 is a same-fuel comparison.

**Knock spikes, `Knock voltage peak cyl 6`** (Will's observation 2026-10-02: "the spikes went away"; the median-based first pass missed it). Spike = sample above 1.5× / 2× the median of its 250 rpm × 10 kPa cell, cell median pooled over all three periods. Idle = `Idle state` 2, CLT ≥ 80; cruise = MAP 30–95, 1500–4000 rpm; boost = MAP 105–175, 3500–6000 rpm.

| cyl 6, % of samples | before E57 | after E57 | after later |
|---|---|---|---|
| idle > 1.5× / > 2× | 0.43 / 0.082 | 0.13 / 0.005 | 0.13 / 0.018 |
| cruise > 1.5× / > 2× | 0.98 / 0.056 | 1.73 / 0.117 | 2.21 / 0.557 |
| boost > 1.5× / > 2× | 6.00 / 0.773 | 5.64 / 0.289 | 2.20 / 0.170 |

- Idle: cyl 6 and cyl 4 (the two most-trimmed) dropped (cyl 4 0.23 → 0.04 % at 1.5×); untrimmed cyl 1 rose (0.63 → 1.37 %). The pattern follows the trim. Per drive, the spiky idle stretch was Apr 20 – May 1 (up to 2.2 % / 0.9 %); early April was quiet; no drive after May 4 went above 0.61 % / 0.12 %.
- Boost: the drop is engine-wide (cyl 1 > 2× 1.38 → 0.72 → 0.14 %, cyl 3 0.64 → 0.15 → 0 %), the same-fuel after set is only 32 s of boost, and boost overshoot stopped at the same time (below). Not attributable to the trim alone.
- Cruise: spikes went up after the trim, cyl 6 at the same fuel (0.98 → 1.73 %) and every cylinder later (lower ethanol). Unexplained.
- Median knock voltage vs boost barely moved; the 99th percentile came down (4000–5500 rpm: before 1.55–1.98 V, after later 1.38–1.55 V).
- Knock-voltage CoV (`emu-black-knock-cov` method, no-knock gate unavailable in the binary): MAP > 100 kPa 25.1 → 20.4 → 21.2 %; MAP > 130 kPa 23.4 → 20.4 → 20.1 %.
- Knock counts in the CSV exports: two all year, both after the trim, both flagged on cyl 1 (and cyl 5), cyl 6 under 1 V.

**Idle quality** (`emu-black-idle-stability` method; steady segments gated on `Idle state` 2, closed TPS, slew < 300 rpm/s, CLT ≥ 80; 25 Hz so quality, not COV-of-IMEP):

| | before E57 | after E57 | after later |
|---|---|---|---|
| steady idle, min | 125 | 63 | 180 |
| RPM jitter (1 s detrended) % | 1.025 | 0.951 | 0.868 |
| `Lambda 1` jitter % | 0.786 | 0.587 | 0.360 |
| hold CoV % (includes PID hunt) | 9.74 | 11.43 | 11.20 |

Will reported idle felt better after the trim; the fast components agree (RPM jitter −7 %, lambda jitter −25 % at the same fuel). The slow hunt didn't improve; that is the airflow PID.

**Idle misfire proxies** (no misfire channel; `questions.py` in the report folder). Same steady-idle gate. RPM sag = run of samples below a centred 7-sample (0.28 s) rolling median by more than d rpm; the short window passes a lost-firing sag but not the ~1 Hz idle hunt (a 1 s window counted hunt troughs, first attempt discarded). Lean blip = `Lambda 1` above a centred 15-sample (0.6 s) median by more than x while lambda is valid. Events per minute of steady idle, before E57 → after E57 → after later:
- sags > 10 / 15 / 20 / 25 rpm: 3.43 → 1.99 → 3.51; 1.12 → 0.55 → 0.96; 0.51 → 0.24 → 0.47; 0.20 → 0.13 → 0.25. Sags > 30 rpm are rare in every period (< 0.15 /min).
- lean blips > 0.015 / 0.02 / 0.03 λ: 0.78 → 0.52 → 0.34; 0.48 → 0.32 → 0.10; 0.28 → 0.15 → 0.02.
- Reading: on the same fuel both proxies fell (sags −37…−54 %, lean blips −33…−48 %). From May 11 the sags returned to about the pre-trim rate while lean blips kept falling; ethanol and idle settings changed in that period.

**EGT, cyl6 − cyl3 (`EGT 2` − `EGT 1`), °C**, MAP held in band 2 s, overrun excluded (bands as above: idle MAP<45 & RPM<1400; light 25–60; cruise 60–95; transition 95–130):

| | pump fuel Mar | before E57 | after E57 | after later |
|---|---|---|---|---|
| idle | +43 | +42 | +24 | +16 |
| light | +56 | +38 | +4 | +11 |
| cruise | +41 | +27 | +1 | −2 |
| transition | +25 | +15 | −6 | −16 |

**Boost** (logged `Boost`, kPa gauge; pulls = Boost > 20 kPa for ≥ 0.5 s): before the trim pulls regularly overshot target, peaks to 105 kPa on E57 and 136 kPa on pump fuel in March (Mar 16 and 28) against `Boost Target` maxima of 100–116. After the trim, peaks sit at or under target: max 89 kPa (target 99) on E57, 81 kPa later. Median pull peak 51 → 66 → 52 kPa (most pulls are short and spool-limited). So boost came down at the top end around the trim; what changed in boost control is not in any export (no pre-trim XML; boost PID disabled in every export since 05-22).

**Superseded first pass (CSV exports only, same day):** concluded the boost ceiling rose after the trim, idle CoV was unchanged and cyl 6 knock was unchanged. All three came from too little pre-trim data (two Apr 8 drives, 15 s of idle, 5 short pulls) and from comparing knock medians instead of spikes. The EGT direction held.

## Next step
cyls 2,4,5 are EXTRAPOLATED, not measured. Biggest risk: cyl4/5 leaner than estimated with no EGT to catch it. Priority: get the EGT-to-CAN module so probes on 4 and 5 can be read, then replace the extrapolated mid-rear values with measured trims.
