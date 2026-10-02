# Crank-fail 2026-07-29 — no-fire diagnosis + orifice-equation dose model

## ★ RESOLUTION (Will's root-cause, end of session) — read this first

**Root cause of the whole saga: over-fueling during cranking fouled the plugs, then every
subsequent lever chased a plug problem.** Will added cranking fuel to light off faster → wet/
fouled plugs (all six, #6 wettest from its +8 % per-cyl cranking trim) → the "long crank" pattern
is drowning it and waiting for a spark to punch through a wet plug. Every no-catch after that
(including the throttle-restriction/vacuum attempts) is a **fouled-plug no-fire**, so those
experiments are *inconclusive, not disproven* — they were never testable through wet plugs.

**Forward plan (agreed):**
1. Clean/replace all six plugs — the actual blocker.
2. **Way less cranking fuel** — undo the additions; err lean, the flammability window is wide.
3. **Crank at the post-start landing airflow (no vacuum, "crank where it lands"), foot OFF.**
   Landing = Active airflow **1500 rpm (afterstart) row**: [87.5, 75, 62, 52, 47.5, 45, 45, 45] %
   at CLT [0,15,30,45,60,75,96,105]. Cranking airflow is already [86,63,38,30] at CLT[0,33,67,100]
   → cold end (86 ≈ 87.5 %) already lands there. Cold crank TPS ≈ 7.3 % → MAP ~98 kPa, and that is
   fine (vacuum was never the blocker; the car starts here with plugs that arc).
4. `idleDBWTargetMin` back to 2.4 % (idle anti-stall floor); prime rail to 4 bar before cranking.
5. Foot OFF while cranking — pedal/TPS >33 % triggers the anti-flood cut (that's flood-clear, not
   a start).

Everything below is the investigation that led here; the vacuum/vapor analysis is sound physics
but was aimed at a problem the car doesn't have once the plugs can spark.

---


Log: `crank_fail_0729.csv` (OneDrive Supra). One crank window t=8.44–13.16 s, 131–212 RPM,
CLT 36 °C, IAT 33 °C, ethanol 25%, battery 10.3 V under crank. Never a single fire event.
Context: **new start strategy** — fuel-pressure-compensated dosing, cranking begins while the
rail is still filling (old procedure waited for full rail pressure before cranking), TB parked
at idle-landing position (MAP goal ~98 kPa), cranking tables recently changed. Old working
tables backed up in `QuickSave\working_cranking_fuel_old_1.emubt` (`crankingCorrTbl`) and
`working_cranking_fuel_old.emubt` (`crankingCorrTbl2`).

## ⚠ RETRACTION (2026-07-29, later pass): the re-derived tables below are NOT a fix

Blended at the actual failing cell (CLT 36, E25 83/17), the re-derived tables land within
**5–6 percentage points of the tables already in the car and failing**:

| rev | current (0728) | re-derived | λ_cmd current | λ_cmd new |
|---|---|---|---|---|
| 1 | +71.4% | +76.5% | 0.584 | 0.567 |
| 3 | +64.2% | +69.3% | 0.609 | 0.591 |
| 7 | +51.6% | +58.0% | 0.660 | 0.633 |
| 13 | +39.5% | +45.9% | 0.717 | 0.686 |
| 20 | +34.1% | +38.6% | 0.746 | 0.721 |

A ~3% fuel change inside a 3:1-wide flammability window is noise — **they would have failed
identically.** The error was methodological: U was anchored to the working tables from *before*
the high-MAP crank strategy, so the model reproduced them by construction. The one term that
actually changed — MAP → U — was absent from the model. Circular calibration; don't repeat it.
Theory now in [engine_start.md → Cranking MAP sets the vaporization budget](../../notes/engine_start.md).

## Zero heat release — this is not a lean-mixture signature

| evidence | value | reading |
|---|---|---|
| `EGT 1` / `EGT 2` | **47 °C flat, span 0** across 61 sparks | not one combustion event |
| `RPM` (post spin-up) | 174–179, σ 7.6, no bumps | no partial fires |
| `Executed sparks count` | 0→61, 4.6/rev | sparks commanded at expected rate |
| `Dwell Time` | 5.3–6.1 ms vs `dwellTime` table 6.2 ms @10 V, `Overdwell`=0 | dwell correct, coils saturating |
| `CAM1 signal present` | 1 on all 117 crank samples | cam signal solid |
| `VVT CAM1 angle` | 0.0, target 0.0 | cam parked correctly for start |
| `MAP` | oscillating 94↔98 | engine pumping |

A merely-lean mixture *pops* — sporadic fires bump RPM 20–50 and tick EGT. Flat EGT + flat RPM
means the charge never ignited at all: either outside the flammability band or **no effective arc
(fouled/fuel-wetted plugs)**. Both are invisible to the fuel tables. Dry or replace the plugs
before any fuel calibration is testable. If dry plugs + correct enrichment still give flat EGT,
compression-test it (175 RPM @ 10.2 V is slow/weak cranking — also worth its own look).

## Why cutting (or doubling) the cranking tables can't light it — vapor-λ accounting

The cranking tables set **liquid** λ; the spark sees **vapor** λ = λ_liquid / U. Current tables at
CLT 36 command corr +71% → **liquid λ 0.585** (this is the "smells rich" number — all injected
fuel counted). At 98 kPa/36 °C/E25 the evaporated fraction U is ~0.10–0.20, so:

| dose | corr | liquid λ | vapor λ (U=0.12) | result |
|---|---|---|---|---|
| **cut 41%** (Will's proposal) | +42% | 0.705 | **5.9** | leaner vapor — worse |
| current tables | +71% | 0.585 | 4.9 | too lean to light |
| double fuel (tried) | +242% | 0.292 | 2.4 | still lean, plugs wetter |

**Every liquid-quantity option is vapor-lean.** To reach ignitable vapor (λ_v ≈ 0.95) at U 0.12
needs corr +780% = **8.8× stoich liquid** — which floods the plugs long before it lights. So the
engine is *simultaneously* vapor-lean and plug-flooding: adding fuel wets the plugs, cutting fuel
leans the vapor, and neither reaches the window. This is why baseline foot-off **and** double-fuel
both failed — they bracket the quantity axis and the window isn't on it.

Will's instinct that it's over-fueled is right in **liquid** terms (the 98-kPa VE cell 65 is
~41% above the 35-kPa cell 46, and the 500-rpm VE row is an untuned extrapolation that likely
overstates true cranking VE) — but cutting liquid moves vapor λ the *wrong way*. A cut only helps
by drying already-fouled plugs; it is not a path to ignition.

**The only lever that opens the window is U**, and U is set by cranking MAP:

| MAP | U (est) | vapor λ at current dose |
|---|---|---|
| 98 (now) | ~0.12 | 4.9 |
| 50 | ~0.28 | 2.1 |
| 35 | ~0.36 | 1.6 → near ignitable |

Drop cranking MAP and the *same* dose walks into the flammable band. That is why the engine
started under the old vacuum-crank strategy and stopped under crank-at-98-kPa: the strategy change
collapsed U. (U values are physics estimates, not measured — the direction is robust, the exact
crossover MAP is not.) Fix U (vacuum, heat, or more volatile fuel), not the fuel quantity.

## DBW authority + cranking/idle airflow mapping (confirmed from tune + EMU screenshot 07-29)

`idleDBWTargetMin`/`Max` = 24/80 → **TPS authority band 2.4 %–8.0 %** (span 5.6). Idle-airflow %
(0–100, the table value) maps linearly onto it: **TPS = 2.4 + af% × 0.056**. So "% airflow" and
"% of DBW authority" are the same number.

**Cranking airflow [%]** (`idleCrankingDC`, ×0.5) vs CLT [0, 33, 67, 100 °C] = **[86, 63, 38, 30]%**
→ TPS [7.2, 5.9, 4.5, 4.1]%. At this attempt's CLT 36 → **63 % → TPS 5.8 %**, and MAP measured
**98 kPa** — the model anchors exactly to the log here.

**Active airflow [%]** (idle target RPM × CLT), cold column (0 °C): 1500 rpm row = **87.5 %**,
1000 rpm = 65 %. So the cold **afterstart landing (1500 rpm) = 87.5 % ≈ the 86 % cold cranking
cell by design** — the throttle is deliberately parked where it will idle at catch, zero handoff
step. Warm idle (1100 rpm @ 96 °C) = 21.5 % → TPS 3.6 %.

**The identity, now numeric.** Same TPS makes idle vacuum at idle rpm but not at cranking rpm.
Orifice model anchored to (TPS 5.8 → MAP 98 @ 178 rpm), swept down to the 2.4 % floor:

| cranking TPS | authority | MAP @178 rpm (plate ~sealed) | MAP @178 rpm (plate leaks) |
|---|---|---|---|
| 7.2 % (cold land) | 86 % | 99 | 100 |
| 5.8 % (CLT36 now) | 61 % | 98 | 98 |
| 3.6 % (warm-idle pos) | 21 % | 92 | 81 |
| 2.4 % (floor) | 0 % | 84 | 28 |

**The whole vacuum question collapses to one unknown: how well the plate seals at the 2.4 % floor.**
If it seals, cranking at the floor pulls MAP to ~28–40 kPa (real vaporization, and the ECU also
injects only ~0.25× the liquid — see VE-cell row below). If it leaks, the floor still reads ~84 kPa
and vacuum-cranking is off the table. The model cannot resolve this from the tune — **one test
does:** set the cold cranking cell toward 0 % (clamps to the floor), crank, watch MAP.
- **Absolute liquid dose scales with MAP×VE-cell:** MAP 98 → 1.00×, MAP 55 → 0.46×, MAP 35 → 0.25×.
  High-MAP cranking is the ECU's *maximum* liquid dose at a given λ — Will's "mega rich" read is
  right in the way that matters (pooling), even though commanded λ is unchanged.

**PID windup concern (cranking closed then opening at catch):** the idle *airflow* PID is gated
off during crank and for `idleControlAfterstartDelay` (=3) after catch; the log shows idle state
never = 2 (PID-active) during the crank. Cranking closed does **not** wind the integrator — the
crank→afterstart airflow move is *feedforward*. Any catch "weirdness" is the feedforward airflow
step (2.4 %→87.5 %), managed by ramping the cranking cell up to the landing value, not a PID fight.

## `varied_cranking_airflow.csv` (07-29) — 4 attempts, settles it

Long log (170 s), 4 cranking attempts alternating with throttle-open flood-clears (A2 @ t43 has
DBW DC +26, PW 0.03 ms, CrankCorr −100 % = deliberate clear). Real attempts A1/A3/A4 drove the
throttle closed. **Three facts, all repeated:**

1. **MAP floor = 88 kPa, confirmed.** Across every attempt, even with DBW DC driven to −35 %
   (hard closed), MAP bottomed at 88 and mostly sat 91–96. The plate cannot pull below ~88 at
   cranking speed. Vacuum path dead — 4× confirmed, not a one-off.
2. **The rail read low at the start of each crank in this session** (0.0–0.7 bar → 4.0 bar after
   ~0.4–0.6 s of cranking; `Fuel pressure correction` maxed +139 %, PW 8+ ms, but at 0.1–1.2 bar
   almost nothing flows). **Rail hardware is fine** — Will confirms it holds pressure and the car
   runs smooth; the low reading is the **key-on prime not firing before the starter**, so after
   the car sat/repeated cranks the rail was down at each attempt. Fix is procedural: get 4 bar up
   (prime) before cranking, not a hardware repair. Minor vs finding 3.
3. **Full rail + rich mixture + spark → still zero catch.** After the rail fills (~rev 2), A1 ran
   ~40 more sparks at 3.9–4.0 bar, PW ~4.0 ms (liquid λ ≈ 0.5, genuinely rich), CrankCorr 51→33 %,
   trigger synced — and never fired. A rich, well-fuelled, well-sparked charge that won't light
   after this many flooded attempts is **wet/fouled plugs**. The visible flood-clear cranks
   confirm Will is fighting standing flood; a few seconds of throttle-open cranking doesn't dry
   soaked plugs. This is the current blocker, not mixture or air.

**Verdict:** the no-start is fuel-delivery + fouled-plugs, not MAP and not the cranking tables.
The old "wait for full rail pressure before cranking" habit was silently covering finding 2.

**Confirmed 07-29 (Will pulled the plugs): all fouled, #6 wet.** Direct proof of finding 3 — clean
or replace all six before any further test. **#6 wet is expected, not a fault:** the per-cylinder
cranking trim biases #6 **+8 %** (rear-cylinder lean compensation, see [[project-supra-per-cylinder-trim]]),
so #6 is the richest during cranking and the first to wet when flooding. Not an injector leak.

**`idleDBWTargetMin` = 2.4 % is a deliberate idle anti-stall floor, NOT free to lower.** Will set
it there because the idle PID was closing the throttle far enough to stall the engine; 2.4 % is
the guard that fixed it. Cranking airflow 0 % maps to that same min, so pulling more cranking
vacuum (Will got MAP 88→78 by lowering it) directly reopens the idle stall it prevents. Since
vacuum is not the blocker (finding 3), **restore it to 2.4 %** — don't trade a working idle for
~10 kPa on a non-issue. Cranking is floored at ~88 kPa by the idle requirement, and that's fine.

**Hypothesis — wet #6 + rail-won't-hold may be one fault: a leaking #6 injector.** Finding 2 (rail
bleeds to 0 between attempts) and the wet #6 plug have a common explanation: a #6 injector that
seeps under rail pressure would both drain the rail *and* pool fuel in #6. Test: pressurize rail,
key off, watch the gauge for bleed-down; if it leaks, pull injectors and find the dribbler (or if
#6 is repeatedly the wettest, suspect it). Alternative is the pump check valve (rail won't hold
but no single cylinder floods worse). Either way the rail must hold 4 bar before cranking.

## Dwell / coil energy at cranking (checked 2026-07-29) — well-set, not the weak link

`dwellTime` vs `vbattVBins` (axis confirmed raw/37 = clean **6–17 V** integer columns; **×0.05
ms/count**, verified against logged dwell): 14 V→4.05 ms, 12 V→5.1 ms, **10 V→6.2 ms**, 8 V→7.8 ms,
6 V→10.8 ms. Proper voltage compensation. Cranking modifiers checked: **`dwellRPMCorr` = 0 at
cranking-speed cells** (only cuts −2…−16 at the top RPM end), **`dwellMAPCorr` = all 0**. So the
coil receives the full 6.2 ms at cranking, log-confirmed (5.3–6.1 ms at 10.2–11.6 V, `Overdwell`=0).
`coilsType = 0` (inductive). **Coils confirmed 2026-07-29: GM/Delphi D585 (LS truck COP), factory
deadtime cal.** D585s are current-limited smart coils saturating ~4–5 ms even at cranking voltage,
so **6.2 ms at 10 V fully saturates them with margin** (log's `Overdwell`=0 = at the limit, not
past). Spark energy at cranking is *not* a limiter — question closed. **Plugs: NGK BKR7EIX (iridium,
heat range 7 = cold) at 0.028″ gap** — tight gap + D585 = a spark that fires *through* rich mixture
(fires at lower V, blow-out-resistant). Consequence: with this ignition, "40 sparks, zero catch"
almost has to be a **shorted (wet) plug**, not weak spark or mere lean — and the cold heat-range-7
plug is fouling-prone at cranking, so sustained richness fouls it. Reinforces: cut fuel; a cold
plug makes modest cranking fuel matter double.

**Cranking voltage is the soft number, not the dwell.** RPM 50–500 in `crank_fail_0729.csv`:
median **10.38 V**, min 10.22, p10 10.30 — workable but not strong (a healthy setup holds 11+).
Raising it helps three ways at once: faster cranking (→ compression, cam note), stronger spark,
and less dwell needed. Battery state-of-charge / grounds / starter draw. **Refinement, not the
fix** — clean plugs + right fuel remains the fix.

## Cranking vacuum IS available (~78 kPa) — held in reserve (2026-07-29)

Will reached **MAP 78 kPa** by driving the throttle hard shut (requires lowering `idleDBWTargetMin`
below 2.4 %). So vacuum-cranking is a real lever if ever wanted (vaporization margin on a genuinely
cold start / difficult fuel) — but it **costs the idle anti-stall floor** ([[project-supra-dbw-min-idle-antistall]]),
so it's a deliberate trade, not a default. Not needed for the current fix; noted as a tool in the box.

## Ruled OUT (all verified in log)

- **Trigger/sync:** `Trigger sync status` 2 throughout crank, `CAM sync trigger tooth` locked 57
  by t=9.04, one momentary `Trigger error` 32 during re-acquire (count 2→3), then clean.
- **Spark commanded:** `Executed sparks count` 0→62, dwell 5.9–6.0 ms, `Wasted spark`=1
  (by-design cranking mode), ign fixed 10° BTDC (`crankingIgnAnlge`=20 × 0.5°).
- **Cuts/protections:** all zero. DBW tracking fine. MAP/CLT/IAT/FP sensors status OK.

## Root cause: the fuel dose collapsed, in three stacked ways

Decomposition of logged `Injectors PW` (all numbers close within ~2%):
`PW = deadtime(≈1.6 ms @10.3 V) + 1.72 ms(λ=1 base) × (1+crankingCorr) × (1+TPSScale) × fprComp`

| Phase | t [s] | revs | Rail ΔP | Pedal/TPS | PW | Effective dose |
|---|---|---|---|---|---|---|
| 1 | 8.44–9.0 | ~1–4 | 0→200 kPa | floored / 69.5% | 2.2–3.1 ms | ≈ nothing — no pressure to flow |
| 2 | 9.0–10.0 | ~4–9 | 400 kPa | floored / 69.5% | 2.16 ms | 0.56 ms eff → **λ ≈ 3.1** |
| 3 | 10.0–13.16 | ~9–23 | 400 kPa | released / 5.8% | 4.0–4.2 ms | 2.4–2.6 ms eff → λ ≈ 0.66–0.72 nominal |

1. **Empty rail at crank start — the key-on prime never pumped.** TIME in this log is ECU
   uptime and starts at 2.0 s (cf. other logs starting at 0.000 = boot, or 2744 = 45 min up),
   so the logged span *covers* the post-key-on ~5 s prime window — and rail pressure sat at
   **0.000 bar flat** through it. Measured bleed rate (~0.4 bar/s post-crank) rules out
   "primed then leaked before logging": any prime would have left >1 bar at t=2. The pump
   itself is healthy: pressure moved 0.12 s after first rotation and hit the 4.00 bar target in
   ~0.85 s, then held ±6 kPa all crank. Leading hypothesis: **EMU primes once per ECU power-up;
   if the ECU wakes on USB before key-on 12 V reaches the pump-relay feed, the prime window
   burns with an unpowered pump** and the pump next runs only on trigger pulses (cranking).
   No `fuelPumpPrime*` duration symbol exists in the XML — prime length is firmware-fixed, so
   the fix is procedural (key-on before/with laptop; no start-delay setting exists). Discriminating
   test: cold key-on with no USB attached, watch the rail gauge; or force `fuelPumpTestOutput`.
   Meanwhile `fprDeltaCorrection` = √(400/ΔP) **clamps at 2.39× (70 kPa bin)** — compensation
   cannot rescue a near-empty rail.
2. **Anti-flood cut — and it can't reach −100% on this car.** The pedal-down phase was a
   *deliberate* flood clear (clearing prior attempts), but `TPSScaleTbl` is indexed by **TPS,
   not PPS** (log-proven: PPS 100 / TPS 69.5 gave PW 2.16 ms = 1.6 deadtime + 0.56 eff; a
   PPS-indexed −100% would have left deadtime-only pulses). Table:
   [0,−21,−31,−37,−100,−100]% at TPS [0,19.2,27.5,33.3,90,99.6]%. The boost-TPS DBW
   characteristic caps full pedal at **TPS ~69.5% → only −77%**, so "flood clearing" still
   injects ~23% of the dose every rev. The −100% bin at 90% TPS is **unreachable**.
3. **Rev-axis exhaustion.** `crankingCorrTbl` Y-axis is crank revolutions [1,3,7,13,20] and it
   counts from the first rotation *whether or not fuel is being delivered*. By the time rail +
   pedal allowed a real dose (rev ~9), the table had decayed to its +35–40% tail → nominal
   λ ≈ 0.7, vapor fraction at 36 °C maybe ~50% → vapor mixture ~1.3–1.4, too lean to light at
   180 RPM. The rich early rows were spent injecting into an unfueled engine.

**Why "doubling the cranking fuel" didn't fix it:** doubling the tail still fights items 1–2 if
the pedal is down, and by then repeated soaked cranks had wet the plugs — a wet plug quenches
spark, so more fuel only adds odor. Note also the rail bleeds 4.0→2.25 bar in ~4.5 s after the
pump stops; if that bleed path is through injector seats into hot ports, every failed attempt
pre-loads more unmetered fuel (progressive self-flooding between attempts). Verify bleed path.

## Orifice-equation dose model (parameters verified in `0728 commute tune.xml.emub3` — latest export; identical in `supra way more sauce.xml.emub3`)

- Injector: `injectorsSize` = 1230 cc/min at ΔP 400 kPa (= ID1050X 1065 cc @ 3 bar × √(4/3) ✓).
  Flow(ΔP) = 20.5 cc/s × √(ΔP/400). Deadtime ≈ 1.6 ms @ 10.3 V (log-derived; matches ID data).
- Air/event: m = MAP·V·VE/(R·T) = 96000×0.0005×0.64/(287×306) = **0.350 g** (ECU basis VE 64).
- E25: AFR_st ≈ 13.2, ρ ≈ 0.752 g/cc → λ=1 dose = 0.0265 g = 0.0352 cc → **1.72 ms effective**.
- Required first-fire schedule (vapor-fraction reasoning, 36 °C): command λ ~0.55 at rev 1
  decaying to ~0.85 by rev 20 → crankingCorr = 1/λ − 1 = **[+82, +67, +49, +33, +18]%** at revs
  [1,3,7,13,20]. Total PW at rev 1, full rail: 1.6 + 1.72×1.82 ≈ **4.7 ms**.
- **Cross-check: the old working backup at CLT 34 °C, E25-blended (83% tbl1), reads
  [+77, +69, +55, +43, +37]%** — the first-principles model reproduces the known-good table.
  Old tables are **model-validation data only** (they encode the old strategy); the fix is the
  re-derived tables below, not a restore.

## Re-derived tables (utilization model, 2026-07-29)

`corr(CLT,rev) = D(rev) × [1/(0.95·U₁(CLT)) − 1]`, λ_vapor target 0.95, decay
D = [1.00, 0.90, 0.75, 0.60, 0.50] over revs [1,3,7,13,20]. U₁ anchored to the back-solved
working tables + hot-end physics; E100 keeps meaningful enrichment through the 51–103 °C band
(ethanol Tboil 78 °C — the 0728 tables under-fuel this region):

- U₁(E0)   = [0.45, 0.52, 0.60, 0.70, 0.80, 0.90, 1.00, 1.04] over CLT [0…120 °C]
- U₁(E100) = [0.37, 0.43, 0.52, 0.62, 0.72, 0.84, 0.95, 1.02]

Exported (u12, raw = %, rev-1 row first):
`supra/exports/Cranking - Cranking fuel 1 [%] (orifice model 20260729).emubt`,
`… fuel 2 … .emubt`.
Verification at E25/CLT 36/MAP 96/10.3 V: rev 1 blend → corr +76.5%, λ_cmd 0.567,
PW 4.63 ms, vapor λ ≈ 0.97; rev 20 → +38.6%, PW 3.98 ms (= the logged working-chain tail ✓).

**VE basis (audited 07-29):** base dose uses the ECU's own lookup — logged `VE` channel
63.9–64.7 at MAP 94–98 / RPM≤212 reproduces exactly from the 0728 XML: RPM clamps to the
500-RPM row, mapBins cols 93/108 → veTable 64.0/66.9, veTable2 62.8/65.9, E25 blend (83/17)
at MAP 98 → **64.78 vs logged 64.7 ✓** (scale 0.1, orientation, and blend all confirmed).
That 500-RPM row is an untuned extrapolation corner (WBO blind, no autotune possible at
crank), but the working-table anchor ran the **same airflow path and same VE cells**, so any
physical error in the cell cancels between anchor and re-derived tables. Runup path after
catch (500→842 RPM rows, MAP 98→40) is smooth — no VE cliffs to kill a catch.

## Implementation (software levers, in order)

**The lever is air, not fuel — and fuel self-corrects when you move air.** Dropping cranking MAP
lowers the ECU's MAP×VE base dose proportionally (same corr %, so liquid λ unchanged at 0.585)
while raising U — vapor λ 4.9→~1.6 with *zero* fuel-table edits. Do not re-dose; restrict air.

0. **Dry/replace the plugs first.** Every flooded attempt fouls them further; a wet plug quenches
   spark, so any air/fuel test through fouled plugs reads as no-fire regardless. Non-negotiable
   pre-step to all below.
1. ~~Restrict cranking air to make vacuum.~~ **DEAD — measured 07-29: 0 % airflow (2.4 % TPS floor)
   → MAP 88 kPa.** The 73 mm plate can't seal enough to make useful vacuum at 178 rpm; no throttle
   position reaches 50 kPa. Matches the "plate leaks" (area ∝ TPS, ~zero offset) model (predicted
   84). The whole air-restriction path is off the table.
   **Reassessment (own it): the vacuum angle was over-weighted.** The throttle never could make
   vacuum, yet the car *normally starts* — so it has always cranked at ~88–98 kPa and high MAP is
   **not** the regression. The U≈0.12 vapor estimate was too pessimistic; empirically U at ~90 kPa
   + cold enrichment is adequate (the car lights there daily). Vaporization physics is real but is
   not the blocker. Real regression is upstream of MAP → items 2–3 below.
2. **Watch the catch flare when you lower cranking air.** `idleCrankingDC` may be held through
   catch as the flare setpoint (see [[supra-cranking-airflow-is-flare-setpoint]]); if lowering it
   makes the catch sag/stall, the flare was coming from that cell and the cold **Active airflow**
   cell (1500 rpm/0 °C = 87.5 %) + a fast ramp must supply it instead. Restrict *crank* air,
   don't starve the *catch*.
3. **Foot off the pedal while cranking** — the anti-flood cut is deliberate flood-clear, not a
   start mode. (Flood-clear table already fixed 07-29 to reach −100 % from 33 % TPS.)
4. **Fuel is a trim, applied last, only after vacuum exists.** Once air is restricted and U rises,
   if vapor λ still reads lean (model puts MAP 35/U 0.36 at vapor λ ~1.6, slightly lean), a small
   bump *then* centers it. Not before — with no vacuum, fuel is the wrong axis (proven above).
5. **Fix the key-on prime** (no start-delay setting exists — `engineStartDelay` is an XML-only
   symbol). Rail must be full at rev 1: prime never ran this cycle (finding 1); test cold key-on
   without USB attached, or `fuelPumpTestOutput`. Independent of the air work, still required.
6. Chase the ~0.4 bar/s rail bleed-down (injector seat vs pump check valve) — progressive
   self-flooding between attempts.

Full equation decode + scalings: [engine_start.md → Cranking fuel equation](../../notes/engine_start.md).
