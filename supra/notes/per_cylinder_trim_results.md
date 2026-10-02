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

**Test register (scientific-method pass, Will 2026-10-02).** Each test: hypothesis → prediction → assumptions challenged → verdict. 95 % CIs on the after/before rate ratio resample whole drives (`tests_bootstrap.py`, `egt_bootstrap.py`, `assumption_checks.py`); "same fuel" = Apr 20 – May 10 (E57 both sides, idle λ target 0.931 both sides).

| Test | Before → after | After ÷ before (95 % CI) | Verdict |
|---|---|---|---|
| T1 idle knock peaks, cyl 6 (> 2× own normal) | 192 → 23 events, ~4.3 h idle each side; same fuel 164 → 4 | 0.12 (0.04–0.31); same fuel 0.04 (0–0.19) | Drop is real. Cause not isolated: untrimmed cyl 1 fell by the same factor (0.12, 0–0.52) and idle peaks mostly hit several channels at once |
| T2 boost knock peaks, cyl 6 | 17 → 6 in 2.2 / 0.8 min shared cells | 1.0 (0.3–4.5) | Inconclusive (too little comparable boost after) |
| T3 cruise knock peaks, cyl 6 | same fuel 150 → 76 in 153 / 64 min | 1.2 (0.7–2.0); all data 6.4 (3.9–10.3) | No change on the same fuel; the all-data rise comes with +6° cruise timing and lower ethanol, not a trim test |
| T4 idle misfire, rich λ blips > 0.02 | 8 → 6 in 149 / 229 min | 0.49 (0.13–1.9); same fuel 0.70 (0–3.7) | Not established (too few events) |
| T5 cyl6 − cyl3 EGT gap | light +47 → +12 °C; same fuel +40 → +12 | change −35 °C (−41…−29); same fuel −29 (−39…−16); idle −26 (−30…−21); cruise −34 (−42…−27) | Supported |

Assumptions that failed or only partly held: T1 control (cyl 1 not independent at idle); T1 idle conditions (ignition +1°, measured λ 0.934 → 0.913 at the same 0.931 target, IAT +2 °C); T2 data volume; T3 conditions (timing, ethanol, cruise target 0.961 → 0.973); T4 event count, and 20 % of blips sit within 0.5 s of a lambda-target change (3–7 % of idle time does), with larger closed-loop trim steps at blips; T4 counting — a per-idle-stretch rolling median created blips at stretch edges and produced the earlier −53 % / −64 % claims (replaced with a whole-log median). Lambda target answer: idle 0.931 / 0.931 (0.901 part of the time from Aug 22), cruise same cells 0.961 / 0.973, boost 0.884 / 0.869.

**Superseded by the register above:** the knock-peak and misfire tables below were the working numbers before the drive-level challenge; keep them for the definitions, use the register for conclusions.

**Comparison is binary (Will, 2026-10-02):** before = every sample with logged `Injector 6 trim` = 100 (Mar 1 → May 4 17:25, ~15 h running, 57 drives incl. 20 pump-fuel drives in March); after = every sample with trim > 100 (May 4 17:38 → Sep 29, ~10 h, 42 drives). Fuel differs: before = pump fuel then E57; after = E57 (May 4–10), E25, then E14 from Aug 22. Lower ethanol after works against the knock result.

**Knock peaks, `Knock voltage peak cyl 6`.** Definition of normal (Will asked, 2026-10-02): the median of that cylinder's knock voltage in its cell (region × RPM 250 × MAP 10 kPa) **during the same period**; only cells both periods visited for ≥ 200 samples (8 s) count. Peak = sample above 1.5× / 2× normal. Control for baseline shift (`peak_normalization.py`): in the shared cells each cylinder's median and noise spread (MAD) match before vs after within one 0.02 V channel step, and pooled-median, own-median and own-MAD (z > 10) definitions agree at idle and cruise. Idle = `Idle state` 2, CLT ≥ 80; cruise = MAP 30–95, 1500–4000 rpm; boost = MAP 105–175, 3500–6000 rpm. Shared-cell coverage before / after: idle 4.4 / 4.2 h, cruise 6.9 / 3.1 h, boost 2.2 / 0.8 min.

| cyl 6, % of samples | before | after |
|---|---|---|
| idle > 1.5× / > 2× own normal | 0.35 / 0.049 | 0.074 / 0.006 |
| idle > 10 MAD | 0.122 | 0.020 |
| cruise > 1.5× / > 2× | 0.93 / 0.056 | 1.61 / 0.354 |
| boost > 1.5× / > 2× | 5.10 / 0.522 | 4.68 / 0.530 |

- Idle: extreme peaks (> 2×) fell on every channel (cyl 4 0.043 → 0.009, cyl 2 0.029 → 0.002, cyl 1 0.016 → 0.002 %); at 1.5× the trimmed cylinders fell while untrimmed cyl 1 rose (0.82 → 1.18 %). Spiky idle drives clustered Apr 20 – May 1.
- Boost: in shared cells cyl 6 did not change; cyl 1 (0.61 → 0.18 %) and cyl 3 (0.46 → 0 %) fell. Only 0.8 min of comparable boost after the trim. An earlier pooled, all-cells version showed cyl 6 −67 %; that came partly from cells only the before period visited (superseded).
- Cruise: peaks rose on every cylinder (see the follow-up below: +6° cruise timing, lower ethanol).
- Knock-voltage CoV (`emu-black-knock-cov` method, no-knock gate unavailable in binary): MAP > 100 kPa 24.1 → 21.5 %; > 130 kPa 24.1 → 21.0 %.
- Knock counts in the CSV exports: two all year, both after the trim, both flagged on cyl 1.

**Idle misfire proxy — rich lambda blips** (no misfire channel; `questions.py`). Corrections from Will, 2026-10-02: **a misfire reads RICH on this wideband** (an earlier version counted lean blips — wrong); **idle RPM (sags, jitter) is not a usable misfire metric** over this period because the throttle-body problems dominate it; and **restart minutes must be excluded** (the first trace shown sat right after a restart). Rich blip = `Lambda 1` below a centred 15-sample (0.6 s) rolling median by more than x while lambda is valid; steady warm idle gate as `emu-black-idle-stability` (`Idle state` 2, closed TPS, slew < 300 rpm/s, CLT ≥ 80) **and ≥ 2 min after engine start**; 147 / 231 min of steady idle. Per minute, before → after:
- rich blips > 0.005 / 0.01 / 0.015 / 0.02 / 0.03 / 0.04 / 0.06 λ: 10.89 → 11.84; 1.14 → 1.14; 0.329 → 0.209; 0.144 → 0.052; 0.089 → 0.017; 0.068 → 0.013; 0.055 → 0.013.
- Without the restart gate the drop is smaller (> 0.02 λ 0.158 → 0.075), so restart minutes diluted the result rather than creating it.
- Reading: blips ≤ 0.01 λ (sensor-noise scale) unchanged; from 0.015 λ up the rate fell 36–81 %. Will reported idle felt better.
- Example traces in the report use a 30 s window ≥ 5 min after start (furthest qualifying window), lambda valid throughout, constant idle target.

**EGT, cyl6 − cyl3 (`EGT 2` − `EGT 1`), °C**, MAP held in band 2 s, overrun excluded (idle MAP<45 & RPM<1400; light 25–60; cruise 60–95; transition 95–130; boost > 130): idle +42 → +18, light +44 → +9, cruise +31 → −1, transition +21 → −14, boost +12 → −26.

**Boost levels** are not compared: boost control is the product of other factors, so a before/after boost comparison says nothing about the trim (Will, 2026-10-02).

## Per-cylinder knock and dwell follow-up (2026-10-02)

Will asked: do the per-cylinder knock data say to trim cylinders differently, or to enrich the whole map, and how much did coil dwell matter? Scripts: `explore_cyl_dwell.py`, `explore_checks.py` in the report folder; binary split at the trim. Tune facts read from `Supra.xml.emub3` (2026-10-02) and the 05-22 export (identical here): `ksInputCylinder1..6` = 1,2,1,2,1,2 (sensor 1 hears cyl 1/3/5, sensor 2 hears 2/4/6); `knockSensorGainCyl1..6` equal; `ignitionTrim1..6` all 0; knock window **10–60 °ATDC** (`knockWindowStart` 20 and `knockWindowDurationEx` 100, both ×0.5 °; confirmed from Will's EMU screenshot 2026-10-02); knock frequency 6.64 kHz, integrator 160 µs, gain 0.286 all cylinders; knock action only above 50 % TPS, all-cylinder retard.

**Cylinders can't be ranked against each other from knock voltage.** Median level per cylinder differs a lot and doesn't move with the trim (boost: cyl 2 ≈ 1.00 V and cyl 5 ≈ 0.96 V vs cyl 3 ≈ 0.77 V), so each window has its own noise floor; cyl 2 and 5 show the fewest peaks because their floor is highest, not because they burn best. Before/after changes within one cylinder are valid; cross-cylinder rankings are not. The knock data alone can't say which cylinder needs more trim.

**Boost peaks are single-cylinder events tied to timing, not mixture.** 82–90 % of boost peaks hit one cylinder alone in the sample (combustion-like, not a common electrical/mechanical burst). Against same-cell samples, boost peaks (before group) sit at +1.6…+2.7° more `Ignition Angle`, +10…+16 % ethanol, −2.5…−5 °C IAT, and λ error within ±0.014 of the cell (`Lambda 1` − `Lambda target`). By fuel: before E57 cyl 6 0.80 %, before E9 0.32 %, after E57 0.29 %, after E25/E14 0.15–0.21 % (> 2×). The worst boost peaks were the E57 pre-trim drives, which run the ethanol-blend timing.

**Cruise peaks follow timing and ethanol, and arrive as multi-cylinder bursts.** After the trim, cruise cells run +6.2° `Ignition From Table` (+5.8° `Ignition Angle`) vs the same cells before (2000–2500 rpm: before E57 28.5–31°, after E57 35.5–39°, after E25 33–37°, after E14 31.5–35.5°; before E9 20.5–23°). Cruise peaks: before E9 0.03 %, before E57 0.06 %, after E57 0.11 %, after E25 0.38 %, after E14 0.77 % (cyl 6, > 2×), concentrated at 2000–2500 rpm. Only 36–66 % are single-cylinder; the rest co-occur on cyl 1/3/4/6 in the same sample. Against same-cell samples they sit at +6…+8 °C IAT, −9…−12 % ethanol, MAP falling 17–23 kPa/s (cyl 1/3/4), λ +0.01…+0.02 of the cell. The whole cruise region already runs ~0.05 richer than before in the same cells while `Lambda target` rose 0.012 (λ − target median −0.032 after).

**Enrich the whole map?** The data don't point at fuel: boost peaks occur at on-target λ, cruise already runs rich of target, and both peak types line up with ignition advance (and lower ethanol / hotter IAT at cruise). The lever the data point to is timing: the cruise table in the 2000–2500 rpm band and how the ethanol blend pulls it back on low ethanol, plus IAT ignition correction. Will owns that call.

**Trim differently?** The only measured pair is cyl 6 vs cyl 3 EGT. Per trim-table cell (`fuelTrimRPM` × `fuelTrimLoad`, nearest cell, MAP held 2 s), cyl6 − cyl3 °C before → after: 1000/20 +41.6 → +18.0; 1000/75 +36.8 → +13.3; 2000/20 +38.0 → +4.1; 2000/75 +33.3 → +0.8; 4000/20 +56.5 → +25.0; 4000/75 +45.4 → +9.0; 4000/130 +20.4 → −16.4 (no data at 185/240 kPa held 2 s). The trim-difference change between the groups was ~7 % (20 and 75 kPa columns) and ~6.5 % (130 kPa), giving 3.4–5.7 °C per % of trim. Residual / sensitivity = cyl 6 relative to cyl 3: ≈ +5 % at 1000/20 (idle), ≈ +1 % at 2000/20–75, ≈ +6 % at 4000/20, ≈ +2 % at 4000/75, ≈ −3 % at 4000/130. The trim tables are RPM-flat (same row at every `fuelTrimRPM`), but the residual has an RPM shape (at 20 kPa: +18 / +4 / +25 °C at 1000 / 2000 / 4000 rpm). Caveats: idle EGT is low and slow; a fixed probe offset can't be separated without a one-time 3↔6 probe swap; cyl 2/4/5 remain unmeasured.

**Coil dwell.** `Dwell Time` was the same before and after (4.25 ms up to 4000 rpm, 4.05 at 5000, 3.70 → 3.85 at 6000), battery voltage identical (median 13.57 V both), `Overdwell` 0 in the CSV pairs. So dwell can't explain the before/after change. Within a cell dwell moves only ±0.1 ms and is the dwell table following battery voltage (within-cell r = −0.98 with battery V, +0.72 with IAT). Cruise peaks are more frequent in the longest-dwell third (cyl 6 0.69 % vs 0.22 %), but that third is the low-voltage, heat-soaked third; IAT is the more plausible driver. Boost shows no consistent dwell relation. Coil events vs the 10–60 °ATDC window: the next cylinder's spark fires at 120° − advance = 81–92 °ATDC at cruise and ~100–105° in boost, always after the window closes, so spark noise can't enter it. The next coil's charge start (spark minus dwell in degrees) lands at ~17–40 °ATDC at 2000–2500 rpm cruise, inside the window, both before and after the trim (the extra cruise timing moves it a few degrees, still inside). In boost at 5000 rpm it falls before TDC, outside. So coil switching is a constant at cruise and can't explain the before/after change; whether the charge-start edge contributes to the cruise multi-cylinder bursts is unverified.

**Superseded first pass (CSV exports only, same day):** concluded the boost ceiling rose after the trim, idle CoV was unchanged and cyl 6 knock was unchanged. All three came from too little pre-trim data (two Apr 8 drives, 15 s of idle, 5 short pulls) and from comparing knock medians instead of spikes. The EGT direction held.

## Next step
cyls 2,4,5 are EXTRAPOLATED, not measured. Biggest risk: cyl4/5 leaner than estimated with no EGT to catch it. Priority: get the EGT-to-CAN module so probes on 4 and 5 can be read, then replace the extrapolated mid-rear values with measured trims.
