# Log `allchannels_smoothclt.csv` (2026-09-29) — afterstart dip, rich idle, post-rewire sensor noise

Source: `EMU_BLACK_V3\Supra\allchannels_smoothclt.csv` (binary twin `LogAutosave` 20260929_1332_15.emublog3).
31 557 samples @ 25 Hz, 1263 s: key-on 0–83 s, cold start at **t = 84.1 s** (CLT 26, IAT 26), warm idle to ~495 s, drive
495–1225 s, hot idle to the end. E14 the whole log (`FF sensor frequency` 63/64 Hz; `FF Blend VE` 91).

**Calibration caveat.** Newest XML is `Supra.xml.emub3` (09-22); the binary `.emub3` and QuickSave are newer and
unreadable. The log contains live edits (`Data changing` at 30.4, 82.9–84.1, 119.3–119.6, 122.7, 125.1,
152.7, 155.6, 159, 246.6, **479.96**; `Making permanent` at 126.7, 161, 481.1–481.7). Two are identifiable from the
log itself and are used below: **kP halved at 479.96 s**, **cold base airflow +~20 air-% at 119.4 s**. Symbol values
quoted as "09-22 XML" are that export's; log-derived quantities are authoritative for this log.

---

## 1. Afterstart RPM dip

**How the 500 threshold actually ran this start (this log only; Will's reading, confirmed 2026-09-29).** The cranking tables carried the engine to ~300 rpm logged. The exit to Afterstart fired on a single ≥500 pulse, and fuel switched from the cranking dose to VE × ASE at that moment. The engine then **bogged at 455–586 rpm for ~0.5 s** with the starter still loading the battery. 0.32 s into that bog the idle controller went ACTIVE and both PIDs wound up against a −1146 rpm error. The engine pulled itself out: the lift-off at 85.20 came only 0.12–0.16 s after the plate first moved (TPS 4.7 → 5.0 at 85.08), far inside the ~750 ms idle-air lag ([[supra_idle_airflow_lag]]), so the added air cannot have caused it. That is an inference from the lag, not a direct measurement. The PID kept winding through the run-up (+23 air-% at 85.48), and the result was the overshoot to 1815 and the trough at 1155. Nothing in this sequence is the software's designed start: the threshold was below the engine's own bog speed. Fixed by `crankingThreshold` → 750 with afterstart delay 4 (Will, 2026-09-29).

| Phase | t (s) | RPM | State | Fuel | Spark | Air |
|---|---|---|---|---|---|---|
| Crank | → 84.68 | 158–222, first fires 381 at 84.48, 303 at 84.68 | Cranking (`ECU State` 2, `Idle state` 3) | cranking dose, `Cranking correction` 17 → 4 % (rev-decaying) | 13° | cranking 67.5 % (TPS 4.7) |
| Exit | 84.72 | exit on a ≥500 pulse (586 logged next sample) | Afterstart (3 / 5) | switches to VE eq × ASE 40 % × warmup 12 %; PW 3.14 → 3.65 ms | 24° lock | still cranking 67.5 % (held through the afterstart delay) |
| **Bog** | 84.72–85.20 | **455–586**, vbat 11.5–11.8 (starter still loaded) | Afterstart delay | VE + ASE | 24° lock | 67.5 % |
| Idle ACTIVE | 85.04 (+0.32 s) | 531 vs target 1677 (−1146) | `Idle state` 2 | unchanged (VE + ASE) | 24° lock; ignition demand +14.5 (ceiling), not delivered | airflow PID +15 in one sample → air 71.5; TPS 5.0 at 85.08 |
| Lift-off | 85.20–85.36 | 455 → 685 → 856 → 994, vbat 12.4 → 14.1 | ACTIVE | VE + ASE | 24° lock | PID still winding: +17.4 → +20.4 |
| Overshoot | 85.36–85.84 | 1000 at 85.36, **peak 1815** at 85.84 vs 1627 | ACTIVE | VE + ASE | 24° lock → restore | PID peaks +23.2 (air 79.5, TPS 5.4), then dumps to −2 |
| Trough | 86.9 | **1155** vs 1567 | ACTIVE | VE + ASE | restore slew | air trough 53.5 at 85.84 arrives ~1 s later |

### 1a. What happened (40 ms resolution, t = 84.7–88)

| t (s) | event |
|---|---|
| 84.72 | `Idle state` 3 → 5 (AFTERSTART DELAY); `Ign. afterstart lock` = 1, `Ignition Angle` 24° (matches 09-22 `afterstartIgnitionLockAngle`/`Time`) |
| 85.04 | → 2 (ACTIVE) at **RPM 531** against target 1677 (`Idle target` = table + Afterstart RPM increase, decaying). ignition PID demand `Idle ignition correction` **+14.5** (its ceiling), airflow P = **+14.5** in one sample, I term ramps ≈ 15 %/s. Air 67.5 (cranking) → 71.5 → **78.5** at 85.44 |
| 85.84 | **RPM peak 1815** (target 1627, +190). ignition demand hits its retard floor **−8.5**; P = −8.5, I = +6.4 → PID −2.1; `Idle air %` 53.5 (= base), `DBW Out. DC` −24…−30 |
| 85.76→86.24 | lock hold ends, restore slew begins (flag stays 1 until 87.52); executed angle falls 24 → 21° (≈ 7°/s) though demand was 18.5 − 8.5 = 10° |
| 86.4–86.56 | RPM through target on the way down; demand swings to **+15.5**, PID rails **+25** (`idleAirPIDOutMax`), air 80.5 |
| **86.9–87.0** | **RPM minimum 1155** (target 1567, **−410**). Air-command trough was 85.9 → **≈1.0 s of air lag** (TPS bottom 4.6 at 86.2) |
| 86.24→87.5 | executed angle climbs back at ≈ 5°/s, reaching only +8° over `Idle ignition target` when demand is +15.5 |
| 87.52 | lock flag clears; RPM smooth from here (1400–1440), no second cycle |
| 88–119 | RPM sits ~70–100 under target, `Idle ignition correction` +6…+8, **I term parked at its ceiling (15.0) for 30 s**, PID +21, base airflow 54 |

**Tuned flare vs delivered (09-22 XML `idleAfterstartRPMincrease`, 4 × 4 u12 = rpm, CLT bins −40/0/40/90 °C × `idleRPMIncreaseRuntimeBin` 0/1/2/4 s; interpolated at CLT 26 → +198 / +137 / +75 / 0 rpm on the `idleRPM` 1500 target).** The logged `Idle target` follows that table exactly (1698 at fire, 1633 at 1.0 s, 1572 at 2.0 s, 1500 at 4 s; continuous in runtime). Delivered, seconds since fire: 0.3 s 531 · 1.1 s **1815** (+188 vs target, +117 vs the 1698 start value) · 2.0 s **1171 (−401)** · 3.0 s 1433 (−101) · 4–8 s 1396–1411 (−89…−104); first sustained ±60 rpm of target only at 14.4 s, mean −56 rpm over 5–30 s. So the peak height is in the tuned range, but the shape is not a decay from ~1700 to 1500: RPM sat *above* the tuned path for ~0.4 s and *below* it from 1.5 s to ~14 s. Cranking airflow (`idleCrankingDC`, 86/63/37.5/30 % at its four CLT bins) reads 67.5 % at CLT 26 and is held only 0.32 s into the afterstart delay; the peak was made under Active-state air (71 → 78.5 %).

**Start sequence across four logged starts (revised 2026-09-29 after Will pointed out the state flip is premature).** The `Idle state` 3 → 5 / `ECU State` 2 → 3 flip fires on a cranking-speed pulse, not on a sustained catch. 09-29: flip at 84.72 s on a 586 rpm pulse; then RPM sits 455–531 for ~0.45 s with `Battery voltage` still starter-depressed (11.5–12.1 V), and only rises to 12.8 → 14.35 V at 85.28–85.40 as RPM takes off (856 → 1085). Same in 08-24 (flip at logged 465, vbat 11.5–11.9, RPM 404–519 for 0.35 s, then vbat 12.3 → 13.2 and RPM 946), and 09-19 second start (flip at 543, vbat 11.9, then 13.0 and 839). So the ECU switches spark (13° → 24° lock), cranking fuel correction (→ 0), ASE (+40 %) and idle control (ACTIVE 0.32 s later) about 0.3–0.5 s before the engine is self-sustaining. Cranking-state pulse peaks seen: 586 (09-29), 465–519 (08-24), 543 (09-19), 425 (08-22 hot); the real catch then climbs at 2000–5000 rpm/s. Threshold history in the exports: 400 through 06-29, 500 by 09-15. Throttle position in cranking and in the afterstart delay comes from `idleCrankingDC` (67.5 % → TPS 4.8 at CLT 26; same value through state 5), so a later flip keeps that TB position until the catch is real.

*Retracted (earlier in this session):* (a) that a higher `crankingThreshold` could leave the state machine unreleased because the ~450–590 hover was what the engine sustains on cranking air — the hover was starter-driven (vbat depressed); (b) that ACTIVE's airflow step launches the run-up — the lift-off coincides with the vbat recovery, and these logs cannot separate real catch from the airflow step; (c) that more base air would raise the peak (unsupported either way: peak 1796–1815 for +9/+11/+26-point steps).

Handoff error by threshold (estimate: first logged RPM ≥ N minus 0.04 s log lag, ACTIVE +0.32 s as measured, 09-29 run-up): 500 → RPM 531 at ACTIVE (−1146 vs target); 600 → 1329 (−319); 700/800 → 1441 (−205); 900 → 1666 (+25); 1000 → 1716 (+77). Window constraints from the logs: above the cranking pulse peak (586 here), below the lowest running dip seen (832 at 455.8 s, kP 1.0 return-to-idle; 925–931 in two drives) and hot idle 1025.

### 1b. Mechanism (four parts; each measured, not inferred)

1. **The airflow PID is fed the ignition PID's *demand*, not the executed angle.** `Monitored P term` ÷
   `Idle ignition correction` = 1.00 ± 0.04 through the whole lock/restore window, when executed angle and demand differ
   by up to 8°. (Outside the lock the two coincide, which is why the help-file wording "ignition angle error" looks right.)
2. **The afterstart lock + restore slew disables the fast loop for 2.8 s** (84.72 → 87.52) — precisely across the flare
   and the dip. Executed angle barely moved on the retard side (−3°) and recovered at ~5°/s on the advance side. What is
   left is the slow loop (air, ~1 s lag) driven at full gain by a demand spark never delivered → one full limit-cycle.
3. **Base airflow at CLT 26 is short.** Steady state after the transient needed PID +21 (I at ceiling + P +7) to hold
   1430 rpm. When the PID unwinds to ≈ 0 at the trough the engine is on base alone ≈ 20 air-% short — that sets the
   *depth*. Corroboration: Will's +20 base edit at 119.4 s dropped P to ≈ 0 and RPM rose to 1600 (over target) before
   the PID trimmed back.
4. **Handoff is early.** ACTIVE begins 0.32 s after AFTERSTART DELAY (`idleControlAfterstartDelay`) while RPM is still
   climbing 531 → 1815, so the first thing the PIDs see is a −1150 rpm error.

### 1b-ii. `idleActiveAirflow` edit history (from the XML exports; axes X = CLT, inferred `idleDCBin` 0–84 °C in 12 steps, Y = `idleTargetBins`)
Exports are ordered by name/date; several May files share one copy timestamp. Displayed % = raw / 2.
- **05-22 → 05-31:** whole table rescaled and re-worked around the 2.4–8.0 actuator range (40 → 35 → 24 → 14 → 6 cells changed between successive files), settling on the 06-03 "smoothed" export (±2 on 14 cells).
- **09-15:** all 40 cells rewritten. Warm/hot columns raised by ~20–33 points (1000-rpm row: CLT 36 from 28.5 → 55.5, CLT 84 from 16.5 → 49.0) — the fouled-TB / oil-viscosity period.
- **09-19 12:09:** all 40 cells +4…+7. **09-19 19:29 (post TB clean):** all 40 cells −16…−28 (1000 rpm, CLT 84: 53 → 28).
- **09-22:** 4 cells, CLT-84 column × four rows, −1.5 each.
- **09-29 (in this log, t = 119.4):** base at CLT 30 jumps 53 → 73; CLT 30–52 sit +22 → +16 above the 09-22 table (log base 73.3/68.8/62.8/59.8 at CLT 30/36/48/52 vs table 51.5/49.5/45.5/43.8), hot end untouched (base 28 at CLT 96 both sides). Before the edit the log base matched the 09-22 table within 1.6 points, so the table at log start ≈ 09-22. The new cold end lands near the 09-19 12:09 (pre-clean) table (69.5 at CLT 30, 64.2 at 52) and near where the PID had settled (base 54 + PID 21 ≈ 75 total). So the edit undid, for the cold columns, the 09-19 post-clean reduction.

### 1c. Was halving kP the wrong call?

kP measured from the log: **1.00 before 479.96 s, 0.50 after** (`Monitored P term` / correction, per 10 s: 0.90–1.10 → 0.45–0.55; edit flagged `Data changing` at 479.96). kI not checked separately (I-slope ÷ correction is noisy: 0.63 before, 0.82 after); the replay below uses kI = 1.0, which reproduces the logged kP = 1.0 trace.

- **The dip was recorded at kP = 1.0**, so the halving cannot have caused it, and it would not have cured it. Open-loop replay
  of the logged demand through `P = kP·corr`, `I = ∫ 1.0·corr dt` clamped [−25, 15], out [−25, 25]:

  | kP | air-PID at 85.44 / 85.84 / 86.56 | swing |
  |---|---|---|
  | 1.0 (validates: log 22.1 / −2.1 / 25.0) | 22.0 / −2.3 / 25.0 | 27.7 |
  | 0.5 | 14.2 / +1.9 / 17.3 | 22.8 (−18 %) |

  First-order only — demand is held as logged, not re-closed through the engine. The integral carries most of the swing.
- **Hot-idle evidence after the change is neutral-to-better.** Settled band: RPM sd 7–13 both sides, `Idle air %` high-pass sd
  0.44 both sides (sd(air)/sd(ign) 1.11 → 0.81, not the 2× drop kP alone would give — the wander is not mostly P). Returns to
  the 1025 target, stationary: **kP 1.0, t = 454.2** → 193 rpm under, ignition to 30°, ringing; **kP 0.5, t = 507.6 / 840.3 /
  1229.8** → 65 / 66 / 26 rpm under, ignition ≤ 21°, no ring. n = 1 vs 3 with different entry histories — suggestive.
- **What kP cannot fix:** parts 2–4 above. The cost of lower kP is a slower recovery from a large positive demand (replay: +17 vs +25 at 86.56 s), ~0.4 s.
- **Gain grid (same replay, open-loop; swing = max − min of PID output):** kP/kI 1.0/1.0 → 27.7; 0.5/1.0 → 22.8; 0.5/0.5 → 19.6; 0.5/0.25 → 15.4; 0.25/0.25 → 10.2. Cutting kI alone at kP 1.0 makes it *worse* (30.6) — the integral's windup is what cancels the P swing. Handoff totals: old base 55.6 + PID → 70.7 at handoff, 77.6 at the peak, trough 53.5; with base ≈ 73 (after the 119 s edit) the same PID trace gives 88 / 95 / 71 — the trough (dip) mostly disappears, the flare gets more air.
- **Other levers, unverified (options only):** `idleControlAfterstartDelay` (hold cranking air until RPM nears target; but the 09-hot-restart finding wants it *shorter* — one scalar, opposing needs); `afterstartIgnitionLockTime` / `afterstartIgnRestoreRate` / `afterstartIgnitionLockAngle` (shrink the window in which demand and executed spark differ; lock angle sits ~4–5° above the idle ignition target through the flare); `idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax` (cap the handoff push now that base carries the load). Fuel in the first 38 s is unobserved: the WBO heater is 0 % until the engine fires (heater DC 0 → 2 → 16 → 55 % over 0–110 s; valid at 122.8 s), so an air dip and a fuel hole cannot be told apart from this log.
- `skills/emu-black-idle-pid-gain` on the 454–466 s ring returns n = 1 cycle, R² 0.39 — outside the method's validity; no Ku quoted.


### 1d. Start/afterstart parameter review — this log only (2026-09-29, post-TB-clean frame)

Scope: this log only. Every earlier start is from before the 09-19 TB clean (different airflow frame), so none of them is used here. This log has **one** start (cold, CLT 26) and **no hot restart**, so every hot-side statement below is untested. Symbol values are from the 09-22 XML. `Data changing` at 82.9–84.1, just before the crank, means the live start parameters are only as good as what the log shows.

**Scalings measured in this log.** `idleControlAfterstartDelay` 3 → state 5 lasted 84.72–85.04 = 0.32 s (≈0.1 s/count). Both idle PIDs are off in state 5 (`Idle ignition correction` logs 0.0). `afterstartIgnitionLockTime` 25 → 24° flat 84.72–85.76 = 1.04 s (0.04 s/count ✓). `afterstartIgnRestoreRate` 4 (if live) → executed angle slewed −3.5° over 6.3 engine cycles (85.76–86.20), then +6.0° over 12.9 cycles (86.24–87.48) = **0.47–0.56 °/cycle ≈ 0.125 °/cycle per count**. That is half the "0.125 °/rev per count" previously in `notes/engine_start.md`. The restore chases the idle-ignition demand in both directions, and `Ign. afterstart lock` clears when executed meets demand (87.52, both 27.5°). Air %→TPS: `TPS ≈ 1.5 + air%·5/100` (`idleDBWTargetMin/Max` 15/65) → 67.5 % = 4.9 (logged 4.7), 80 % = 5.5 (logged 5.2–5.4).

**Sustaining total `Idle air %` (base + PID), this log.** 6-s means, idle state 2, PPS 0, after the 119.4 s base edit unless noted:

| CLT | `Idle target` | RPM | total air | PID | base |
|---|---|---|---|---|---|
| 26–29 (pre-edit) | 1500 | 1417–1483 | 75.4–77.0 | +21…+23 | 54 |
| 32–36 | 1500 | 1491–1504 | 76.0–78.6 | +4…+9 | 69–71 |
| 40–45 | 1500 | 1480–1502 | 70.8–73.8 | +2…+7 | 64–69 |
| 49–52 | 1488–1500 | 1489–1496 | 71.3–74.6 | +11…+13 | 59–63 |
| 60 | 1450 | 1431 | 64.8 | +12 | 53 |
| 67 | 1348 | 1328 | 54.4 | +8 | 47 |
| 72 | 1270 | 1249 | 47.4 | +5 | 42 |
| 75 | 1225–1229 | 1232 | 40.0–43.0 | +1…+3 | 39–40 |
| 90–93 (just warmed, 395–497 s) | 1030–1041 | 1024–1041 | 26.7–28.2 | −2…−4 | 30 |
| 96 (heat-soaked, 1234–1263 s) | 1033 | 1036 | 14.8 | −13.7 | 28 |

The need at hot idle roughly halved between the just-warmed and heat-soaked segments at the same CLT and target. This log can't separate oil temperature from other soak effects; oil temp is not logged (channel reads 0).

**Start sequence recap (40 ms).** Crank 158–222 rpm at MAP 88–94 on 67.5 % (TPS 4.7). `Idle state` 3→5 on a 586 pulse at 84.72, with the cranking correction decayed to 4 %. At the flip the PW went 3.14 → 3.64 ms (ASE 40 %). Hover 455–531 at the 24° lock, vbat 11.5–11.8. ACTIVE at 85.04, 531 rpm vs 1677: the airflow PID goes +15 → +23 (air 71.5 → 79.5, TPS 4.7 → 5.4), and the ignition demand goes to +14.5…+16 (ceiling, not delivered). RPM ≥ 800 at 85.28 (0.56 s after the flip), 994 at 0.64 s, 1210 at 0.72 s, peak 1815 at 1.12 s against 1627. At the peak the ignition demand was 10° against 23–24° executed, and the air command was 53.5. Trough 1155 at 2.2 s.

**Per parameter:**

- **`crankingThreshold` (500): too low — it fired on a cranking pulse, so the exit did not mean "started".** *(Revised 2026-09-29 after Will's objection. An earlier line here kept 500 and lengthened the afterstart delay to compensate, which patches one parameter's misplacement with another.)* In this log the engine is caught once RPM climbs monotonically: 685 (85.24) → 856 → 994 → 1085 (85.40), with vbat recovering over the same samples. Every sample before that is starter-carried pulses and hover (≤ 586). Exit timeline, delay unchanged at 3 (+0.32 s): threshold 700 → exit ≈ 85.24, ACTIVE ≈ 85.56–85.60 at ~1440–1605 vs target ~1678; threshold 1000 → exit ≈ 85.36–85.40, ACTIVE ≈ 85.72 at ~1754 vs ~1678. Either one hands the PIDs a small error instead of −1146. On this start, 700 and 1000 differ by only ~0.15 s.
  - **Decision (Will, 2026-09-29): `crankingThreshold` → 750, `idleControlAfterstartDelay` → 4.** Placement rule: above everything before the catch and below the lowest running stumble. Window in this log: 586 (pre-catch max) to 832 (lowest running RPM after 88 s; 0 samples < 800, 9 < 850, 14 < 900). A 750 exit lands at 85.255 s, 4.5 revs after the old exit. Physical revs from the first post-gap crank sample (83.96): 3.3 to the old exit, 9.2–9.5 to 1000 rpm. The ECU rev counter behind `crankingCorrTbl` read ≈10 at the old exit and may run ~1.8× physical (see `notes/engine_start.md`). RPM crosses the afterstart target 0.39 s after the exit (85.255 → 85.647, 1674 rpm; 0.32 s to the 1500 base target), i.e. 3.7 counts at ≈0.107 s/count. The delay's job is this 750 → target interval (Will). Delay 3 → −171, **delay 4 → +47**, delay 5 → +131 (at the peak). Lock time 11 (0.44 s, ≥ delay). `Engine runtime` counts from the exit, so ASE and the afterstart RPM increase start there too. *(1025 was chosen first, then rejected: hot idle targets 1025, running RPM was < 1000 in 388 samples, and re-entry below the threshold is unverified.)*
  - **Re-entry below the threshold — unverified.** The only evidence is 455 < 500 for ~0.3 s after the old exit, without re-entering Cranking. Keeping the threshold under the lowest running dip makes the question moot.
  - **`engineStallRevs` must sit below the lowest cranking speed** (Will, 2026-09-29). This log cranked at 158–222 rpm (10.5–11 V), so 250 would read a normal crank as a stall. It is 60 in the 09-22 XML, unchanged in every export since May. Will lowered it below 60 on 2026-09-29 (value not recorded here) to shorten crank-start → first fuel. The effect can't be checked here: the crank start is inside the `Data changing` gap.
  - **Companion change the design needs: stepless fuel at the exit.** The cranking tables must now carry the hover and run-up. Measured at today's flip: net PW 1.864 ms at MAP 88 on cranking fuel (`Cranking correction` 4 %) → 2.395 ms at MAP 83 on running fuel (ASE 40 %, warmup 12 % on both sides). That is ×1.36 per kPa, so the cranking correction equivalent to the running dose is ≈ +41 %, i.e. ASE(CLT 26, runtime 0). A later exit lands ~5–7 revs after today's flip (today's flip sat between the rev-7 and rev-13 rows at CLT 26). Those rev-7…20 cells at CLT 22–33 are now 7/−3/−9 %, so without a change the hover and run-up get ~25–35 % less fuel than this start did. Either the tail rises toward the ASE runtime-0 value (non-monotonic against the wall-film decay the table was built on), or ASE runtime-0 comes down to meet the tail. Which is right is a mixture question; the WBO was invalid until 122.8 s.
  - **Spark:** `crankingIgnAnlge` (13°, chosen for kickback at starter speed) would run the hover and run-up instead of the 24° lock. Less torque, so the run-up is probably slower and the flare smaller. Not observed.
- **`idleControlAfterstartDelay` (3 ≈ 0.32 s): keep 3 once the threshold marks the catch.** The "short delay after startup" in the help file is its design role. The earlier suggestion of 6–7 was compensating for the early exit; withdrawn.
- **`afterstartIgnitionLockTime` (25 = 1.04 s) + restore (4 ≈ 0.5 °/cycle): the locked window is 2.8 s, and 1.8 s of it is restore tail.** The airflow PID reads the undelivered demand for the whole window (P/corr = 1.00). Suggested: end the lock when ACTIVE starts (lock count ≈ delay seconds / 0.04, i.e. 8 ≈ 0.32 s with delay 3). Keep lock ≥ delay, because this log doesn't show what spark state 5 runs without the lock. Make the restore fast enough to close the ~14° gap seen at the peak in a couple of cycles (~7 °/cycle, ~55 counts at the measured scale; check the UI units first, given the 2× scaling discrepancy).
- **`afterstartIgnitionLockAngle` (24°): no change supported.** With the lock ending at ACTIVE, it only acts in the hover, and this start caught at 24° (cold idle-ignition target 18.5–20.5). Its cost at the flare (demand 10° vs 23–24° executed) came from the lock *duration*.
- **`idleCrankingDC` (86/63/37.5/30 at `cltBins4` 0/33/67/96).** Method (`notes/engine_start.md`): each bin = the air the engine needs at idle target + afterstart increase.
  - **33 bin ≈ 78–80** (now 63). This log needs 76–79 at 1500 for CLT 32–36. The afterstart increase at 1 s is +130 at CLT 33, and the active table's row spacing is +1.2…+1.4 air-% per 100 rpm (09-22 XML; a tune value, not a measurement). At CLT 26 the table gave 67.5 against 75–77 total held at 1417–1483.
  - **67 bin ≈ 55–56** (now 37.5), from the warm-up segment (54.4 at 1348, +97 increase). A warm restart at CLT 67 (warmer oil) would need less; this log doesn't measure that.
  - **96 bin: keep 30.** *(Corrected 2026-09-29 after Will's objection; an earlier line here said ≈16, sized to the heat-soaked case.)* A hot restart does not imply heat-saturated oil. The cranking bin is open-loop, like the active base ([[idle_base_airflow_is_open_loop_guarantee]]), so it has to carry the worst hot case. In this log the unsaturated hot case (CLT 90–94, `Engine oil pressure` 3.8–4.1 bar) needed 26.7 at 1024 rpm, 28.2 at 1041 and 34.5 at 1177. Interpolated to the hot afterstart target (~1100–1125), that is ≈ 30–31, which is the current value. Heat-soaked (CLT 96, 1.8–2.1 bar) needed 14.8 at 1036 and 19.8 at 1091, so the soaked restart is over-aired by ~11–15 points at 30. That surplus can't be removed from a CLT-only table without starving the unsaturated case.
  - **0 bin:** no data below CLT 26.
  - **What separates the two hot cases in this log: oil pressure,** 3.8–4.1 bar (need 27–28) vs 1.8–2.1 bar (need 15–20) at ~1030–1090 rpm and CLT 90–96. The PID sat at −2…−4 unsaturated and −9.7…−13.7 soaked, matching the held soak-valley design (−11.5 at ≤ 2.5 bar, `oil_viscosity_idle_airflow.md`). Two limits for starts: (1) `Engine oil pressure` read 0.06 bar until 1.5 s after the flip, ≥ 1 bar at 2.1 s and ≥ 4 bar at 2.3 s (cold start; hot build-up not in this log). (2) The custom correction is active-state only. So an OP-indexed trim can't act during cranking or the afterstart delay, or through the flare. During the first ~2 s its low-P column would apply to *every* start, cold and unsaturated included, because OP hasn't built yet. Through the flare itself, the only lever that can tell the two cases apart is ignition (lock ≈ delay, fast restore).
- **`idleAfterstartRPMincrease`: no change supported yet.** The logged `Idle target` follows the table exactly (1698 → 1500 over 4 s at CLT 26). RPM was +188 at the peak and −401 at 2.0 s. After the transient it sat ~100 under a flat 1500 for 30 s, so the shortfall was base air (fixed at 119.4 s), not the decay rate. The flare the table would be sized against includes the premature PID push (air 67.5 → 79.5). Re-read RPM − target at the peak and at ~2 s on the next cold start after the delay/lock changes. The 90 °C row is untested here.


### 1e. Cranking fuel rebuild for the 750 exit (proposal 2026-09-29; Will enters values himself)

**Status: undecided (Will, 2026-09-30: "maybe our cranking tables are good — they're VE-based and taper to 0").** The alternative is to keep the tables and bring ASE runtime-0 down to meet the tail, ≈ 0 cold (ASE is `ubyte`, so it can't go below 0). Against it: the cold tail is negative (rev 13/20 at CLT 22–33 = 0/−9, −7/−12), which carries the cranking-speed VE error; at 500–750 rpm the lookup is on the VE table's own rows (not measured either). This start caught and ran on ASE +40 from the exit, and nothing in the log says 40 % less is safe. Either way the two sides must meet at the exit; which one is right is a mixture question the WBO can't answer in the first ~38 s.

**Step size (Will, 2026-09-30: "not really severe" — agreed).** At the 84.72 exit: PW +16 % (3.14 → 3.65 ms, back to 3.16 within 0.5 s as MAP fell), net PW +28 % (1.86 → 2.40 ms), per unit air ≈ +36 % (MAP 88 → 83). That is well inside the ~3:1 ignitable window (`notes/engine_start.md`), and the engine caught through it. The bog/overshoot came from the idle PIDs engaging in the bog, not from this step. With the current tables and a 750 exit (rev 12–13, CLT 26: tail −0.4…−2 % vs ASE 40.5 %) the step is +41…+44 %, about the same size. So keeping the tables is defensible, and the rebuild above is a refinement, not a fix.

Source values: `crankingCorrTbl`/`crankingCorrTbl2`, `aseTbl`/`aseTbl2`, `tblsFFCrankingBlend`, `tblsFFASEBlend` from the 09-22 XML (read this session) and the 09-19 post-clean export (identical on all of these). The 09-22 XML was overwritten by a binary save at 2026-09-29 20:30, so the live tune needs a fresh XML export before these are entered.

**Exit continuity, derived and checked in this log.** Cranking dose = VE eq × (1 + `Cranking correction`); running dose = VE eq × (1 + ASE); warmup is on both sides. At the 84.72 exit: ×1.36 per kPa at corr +4 % → corr-equivalent +41 % vs logged ASE 40 (blend check: ASE1 37.7 × 0.885 + ASE2 62.3 × 0.115 = 40.5). So a stepless exit needs **corr(exit rev, CLT) = ASE(CLT, runtime 0)**, table 1 ↔ table 1 and table 2 ↔ table 2. The two FF blend curves differ by ≤ 11 points of weight (E75), leaving ≤ ~3 points of residual step. At E14 the residual is 0.7.

**Exit revolution.** Will's estimate is 12–13 on the ECU count. The log brackets it at 12–15: 4.1 inverted from the first post-gap sample + 3.3 + 4.5 physical revs = 11.9; ≈10.3 at the old exit + 4.5 = 14.8. So `crankRevCntBins` row 13 is the exit row for a cold start.

**Rows:**
- Rev 1/3/7: unchanged. They are the cranking-speed cells (B ≈ 0.79, VE lookup clamped to the 500 rpm row), and this start first fired at count ~7–8 on them.
- Rev 13 = ASE runtime-0 interpolated to `cltBinsCranking`: T1 48/44/39/35/29/25/21/17, T2 79/72/65/58/52/45/38/32 at CLT 0/11/22/33/45/56/67/78. The linear 7 → 13 rise is not extra enrichment in true terms: it unwinds B as RPM leaves cranking speed (true enrichment ≈ (1+corr)/B − 1: rev 1 at CLT 22 ≈ +65 % at B 0.79; exit ≈ +39 % if B ≈ 1 at 750).
- Rev 20: unchanged (anti-flood). A crank still short of 750 by rev 20 isn't catching, and the rev axis can't tell a stalled 200 rpm crank from a 700 rpm run-up. At B 0.79 the new rev-13 cell is ≈ +76 % true for a non-catching crank (λ ≈ 0.57, CLT 22 T1), against +23 % before. Holding rev 20 at its old value limits how long that lasts. Cost: an exit at rev 15 meets 26 against ASE 39 (×1.10).
- Blended at CLT 26, E14: rev 7 8.7 → rev 13 39.6 against ASE 40.5.

**Scope.** Columns 0–33 are covered by this start (CLT 26). For 45–78 the continuity rule is applied without a measured exit revolution. A warm/hot catch reaches 750 in fewer revs, so it exits on the 7 → 13 slope below the ASE value; at CLT 78 T1, an exit at rev 8 meets −15 against +17. A non-catching hot crank also gets richer. Take those columns after a warm/hot start log.

---

## 2. Rich hot idle (λ 0.78–0.85 vs 0.90)

### 2a. Measured
- Hot idle (CLT ≥ 92, PPS 0, 900–1400 rpm, MAP < 42; 214 s): λ mean 0.819, **`Lambda target` 0.90** (table) → −7…−13 %; `Lambda error mult.` −8…−13.
- Not idle-only. Steady driving, λ_open-loop vs `Lambda target`: median **−6 %** (IQR −8.1…−3.9); by MAP: 20–30 kPa −13.6 %, 30–36 −9.6, 36–45 −9.3, 45–60 −6.1, 60–80 −6.2, 80–100 −5.4, 100–120 −6.2, >120 −8.0. Boost pulls: λ medians 0.78–0.84 (min 0.73) vs target 0.84–0.88 (rich = safe side).
- **The trim cannot correct it, three separate ways:** (i) STFT floor — `Short term trim` bottoms at **−8.06** (t = 419.1, 883 samples ≤ −7.5; = `lambdaTrimIntegralLimitMin`, 09-22 XML), λ then still 0.87 ≈ open-loop 0.80; (ii) integration rate ≈ 0.09–0.12 %/s, run lengths median 3.5 s, and it resets to 0 on every excursion; (iii) **the STFT flag is off whenever λ < ~0.795** (error worse than ~−12 %): idle samples with flag 0 have mean λ 0.78 (n = 1865), flag 1 all have λ ≥ 0.80 — so at 0.78 it can never engage. Also gated below CLT 80 (`shortTermMinClt`; first active 349.6 s). Mechanism of (iii) traced: `shortTermMinLambda` raw ÷ 128 = 0.797 (09-22 XML), matching the observed switch-off; `shortTrimKPScale`/`shortTrimKIScale` are also cut at the low-airflow bins, which is why it is so slow at idle. See [fuel_mixture_parameter_inventory.md](fuel_mixture_parameter_inventory.md).

### 2b. Charge-temperature hypothesis (map tuned at higher IAT)

> **Correction 2026-09-29 (later, after checking the earlier all-channel logs).** The first pass below concluded "not supported". That was too strong. Hot-idle λ_open-loop vs target across logs, all E14: **08-24 `omg.csv`** IAT 47.6 → −0.4 % (cruise +0.8); **09-19 `losingit.csv`** IAT 60.4 → **+6.4 %** lean (cruise +8.6); **09-19 `fullchannels.csv`** IAT 48.3 → −0.1 % (cruise +1.2); **09-29** IAT 29.6 → **−10.8 %** (cruise −6.3). It has *not* always run rich: on target at every hot idle through 09-19 afternoon; today's IAT is the lowest of any log checked. Monotonic in IAT, ≈ 0.5 %/K at both idle and cruise. Within `fullchannels.csv` (IAT 31–57) idle λ_ol rises **0.31 %/K of charge temp** (R² 0.5, holds with MAP in the model; 0.85 at IAT 31 vs 0.92 at 55) — one full ideal-gas density term. `omg.csv` (IAT 38–57) shows no trend (0.08 %/K). The ECU dose does follow ~1/T within every log (exponent −0.71…−1.10), so the pattern fits "dose follows modelled charge temp, real cylinder air at idle doesn't follow it as much" — but that accounts for ~−4 % of the −11 % at idle, and the cross-log dose ratio (×1.003) is unexplained. So: IAT is the best-supported correlate, mechanism and full size unsettled, EGT still disagrees on direction. The sign argument in point 1 below assumes real air tracks the model; it does not survive this.

**Pulse-width test (17 cell-matched cells, 09-19 pm vs 09-29, net PW 0.29–1.28 ms):** shift = **0.66 %/K × ΔIAT** (rmse 1.9 %); adding an additive 1/PW (dead-time) term changes nothing (coefficient −0.19). So the shift is proportional to IAT and does not grow at small pulses — injector dead time is rejected as the cause. Same-day pair on one sensor and tune: 09-19 morning IAT 60 → +6.4 %, afternoon IAT 48 → −0.1 % (≈ 0.55 %/K), which also argues against a pure sensor-drift explanation. Parameter inventory: [fuel_mixture_parameter_inventory.md](fuel_mixture_parameter_inventory.md); no fuel symbol differs between the 09-19 post-clean export and the 09-22 XML. Key-on MAP is 98 kPa / 1.137 V in both logs (no MAP-sensor drift); E14 in all four logs.

*First-pass analysis (kept for the numbers):*
`chargeTempTbl` (09-22 XML): weight on CLT of **17.5 %** at idle cells (raw ×0.5 %), falling to 0 above ~54 kPa / TPS ≥ 30. Log-verified: hot idle `(Charge temp − IAT)/(CLT − IAT)` = 16.8 %. So `Charge temp` = IAT at cruise/boost; the table only touches idle/light load.

Natural experiment vs `fullchannels.csv` (2026-09-19), hot idle, same fuel (E14), VE-table cell, MAP, RPM, ignition, cam:

| | 09-19 | 09-29 |
|---|---|---|
| `VE` / MAP / RPM | 48.4 / 36.0 / 1020 | 48.2 / 35.6 / 1026 |
| PW net (PW − `Injectors cal. time`) | 0.480 ms | 0.474 ms |
| dose ÷ (VE·MAP) | — | ×1.003 |
| IAT / `Charge temp` / `Fuel Temperature` | 48.8 / 56.2 / 45.9 | 32.5 / 42.5 / 38.3 |
| `Estimated airflow` | 4.82 | 5.07 g/s (+5 %) |
| λ open-loop (λ·(1+STFT/100)) | 0.902 | **0.802** |
| EGT 1 / EGT 2 | 466 / 485 | 505 / 529 |
| WBO `RI`, `VS`, sensor temp | 0.739, 2.735, 777.7 | identical |
| free-air Ip (fuel cut, n ≥ 60 samples) | 2.22–2.26 | 2.15–2.20 |

Ten cell-matched cruise cells (MAP 40–80 × RPM 1500–2500, IAT 46→31): dose per VE·MAP **+2.1 %** (ideal-gas +4.5 %, less the removed fuel-temp adder), **λ −7.5 %** (−4…−14), EGT **+39 °C** in every cell.

Why it does not close:
1. **Sign.** Cooler charge = denser air = *leaner* at fixed dose. The ECU adds ~2 % of the +4.5 %. Net expected shift is slightly lean; measured is 7–11 % rich.
2. **Size at idle.** ±10 K of `Charge temp` = ±3.2 % dose. An 11 % change needs +34 K, i.e. table weight ~66 % rather than 17.5 % — and the cruise cells (weight 0) are also −6 %.
3. **Within this log** IAT climbed 26 → 37 and the mixture did not follow: idle open-loop λ slope +0.2 ± 0.1 %/K unadjusted (its sign flips when MAP and time are added — not resolvable; cross-log needs ~0.7 %/K); steady cruise IAT 28.7 → 31.8 gave −5.7, −6.9, −4.4, −6.2 % (flat).
4. **EGT** rose ~40 °C at cooler intake while the WBO says 7–11 % richer — the two observables disagree on direction.

Unresolved. The −7…−11 % shift between 09-19 and 09-29 is on the air/fuel/measurement side, not in the ECU's dose model. WBO gain is unchanged at the free-air end (rules out a plain electronic offset); not ruled out: fuel-side (injector dead time — net pulse is only 0.48 ms of 1.5 ms, so 0.03 ms = 6 %; supply pressure; fuel batch) or a real air-side change. Discriminators: hot-soak the car in one session and watch idle λ vs IAT at fixed cell; WBO free-air check with key-on engine-off; a second fuel-cut Ip series.

### 2c. Tolerability
Mechanically safe: rich, never lean at load (worst tip-in 1.08–1.10 for 4 samples at 728 s; the 1.89 samples are WBO tail after fuel cut). Costs are fuel, plug fouling (BKR7EIX, cold range), oil dilution at long idles; idle stability is helped by λ < 1 (Idle help). At boost λ medians 0.78–0.84 vs 0.84–0.88 target (rich by ~0.05), EGT peak 648/664 °C, no knock. Not a reason to touch `chargeTempTbl`.

---

## 3. General behavior
- **Start:** cranking 84.1, fires 84.7, no stall. Battery low 10.5 V at crank. WBO valid at **122.8 s** (38 s blind; STFT gated until CLT 80 at 349.6 s). Cold λ 0.73 vs 0.91 target with ASE/warm-up enrichment (10–12 % + 13 %) — intentional.
- **Warm-up:** target 1500 at CLT 26 → 1025 at CLT ≥ 90; fan on from t = 286 (CLT ≈ 70) and stays on 77 % of the log, no visible step in RPM.
- **Hot idle:** RPM 1016 ± 13 on 1025; ignition 17.8° on 18.5° target; airflow I term −14 (base too high, PID trims), not at −25 limit; TPS 2.1 ± 0.05.
- **Drive:** 6058 rpm, 62 kPa boost (target 52 → +10 at 1013 s, boost DC 90 %), boost under target on the short bursts; no knock retard, `Knock count` 0, no protection/check-engine codes, no spark/idle cuts, one `Trigger error` (code 32, 1 sample, RPM 2305, t = 716.48). Fuel cut: 30 short events (~3000–3450 rpm in the ones inspected).
- **Return-to-idle at speed:** `Idle target` steps 1025 → 1225 → 1425 while moving (origin not traced) and undershoots of 200–360 rpm below the *elevated* target occur with clutch-in; ignition to 36° (authority limit). Not analysed further here.
- **CLT reads 96.0 for 10.6 min:** voltage 0.529–0.569 all map to 96; 0.588 V → 94–96. The 09-22 note's Steinhart–Hart fit puts 0.549 V near 90 °C, so this is table saturation (dead band), not thermostat regulation — every CLT-keyed table (idle target, WUE, fan, charge weight) sees a flat 96.

## 4. Sensor noise — post-rewire re-scan (method: `clt_signal_noise.md` §6)
CLT/IAT returned to sensor ground on 09-28; this is the hot re-log that note asked for.

| channel | amp running (quanta) | p99.9 (V) | spikes ≥ 3 LSB | before (09-19) |
|---|---|---|---|---|
| `CLT Voltage` | **0.12** | **0.020** | **0.00 %** | 1.58 / 0.177 V / 1–4 % hot |
| `IAT Voltage` | **0.15** | **0.020** | 0.00 % | 1.65 / 0.098 V |
| CLT ↔ IAT residual r | 0.05 | | | 0.07 |
| `CAN Analog 5` (oil pressure) | 2.68 | 0.314 | 26.6 % | 2.69 — **unchanged** |
| `Battery voltage` | 1.56 | 0.189 | 3.0 % | 2.59 |

Hot-window mean |CLT residual| 0.0003 V (was 0.0218). Engine-off amp 0.00. **The CLT noise is gone; it was the return.** What remains is 1-LSB code-boundary dither (1.4 % of samples on CLT, 2.3 % on IAT) — 324 CLT-voltage flips but only 92 CLT-degree flips in the hot window.

**What the rewire changed for fueling.** Engine-start voltage step (15 s before vs 6–21 s after first fire, physical temp unchanged): 09-19 `CLT Voltage` −0.114 V (≈ +3 °C hot bias while running), `IAT Voltage` −0.030 V (≈ +0.6 °C); 09-29 CLT −0.006 V, IAT +0.038 V (within a code or two). IAT noise sd 0.033 V (~0.7 °C, p99.9 ~2.3 °C) → 0.003 V. At the ECU's ~0.3 %/K density sensitivity that is ≈ +0.2 % dose from removing the IAT bias (≈ +0.15 % more via the 17.5 % CLT weight in `Charge temp` at idle) and ±0.2 % of jitter that averaged to zero before. **The rewire moved mixture by ~0.3 %, not ~10 %.** The same-day 09-19 pair (IAT 60 vs 48, +6.4 % vs −0.1 %) was entirely before the rewire.

**Did the old IAT/CLT noise reach VE or pulse width?** Hot idle, 09-19 (noisy) vs 09-29: `VE` high-pass sd 0.35 (0.72 %) vs 0.42 (0.87 %) — VE is a MAP × RPM lookup, so IAT/CLT noise cannot enter it; its jitter is MAP/RPM. `Charge temp` was **not filtered** (steps on ~76 % of hot-idle samples, sd 0.99 °C vs 0.50 °C now, the latter just 1-LSB dither). `Injectors PW` high-pass sd 1.07 % vs 0.99 %; regression of PW % on charge-temp residual −0.18 %/°C (r −0.17; ideal −0.3) → ≈ 0.18 % rms, ~3 % of PW variance. A ±1 °C charge step moved PW 0.04–0.09 %. CLT excursions ≥ 3 °C occupied 8.4 % of hot-idle samples and moved PW by −0.06 % on average. Cold-side (warm-up/ASE keyed to CLT) not examined; spike rate was ~0 in the first 3 minutes.

Other channels at hot idle (23 s): `MAP` 1 kPa quantum, 2-value flicker, sd 0.9 kPa (≈ 2.6 % of 34 kPa — coarse, but PW jitter is only ~1 %, so the ECU filters); `TPS` 0.1 quantum, sd 0.05; `Lambda 1` hp sd 0.006; EGT hp sd 0.6 °C; `Fuel pressure` sd 0.003 bar; `Pre IC temperature` integer, sd 1.0. Knock peaks: per-cylinder idle baseline 0.22–0.25 V (cyl 1/3/4/6) vs 0.35–0.36 (cyl 2/5); one pinned 4.96 V on cyl 1 during the start (84.72–84.92, six samples, cranking); 1.5–2.7 V at 4200–6000 rpm; `Knock Engine Noise` constant 5.0 (dead). Unused/clamped: `Post IC`/`Ambient` −40, `Baro` 100 (fixed), `Engine oil temperature` 0. **Open item: oil-pressure jitter (`CAN Analog 5`) untouched by the rewire — its cause is still unresolved (see `clt_signal_noise.md` §6b).**
