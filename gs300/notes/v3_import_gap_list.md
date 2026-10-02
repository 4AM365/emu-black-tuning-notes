# v2 → v3 import gap list — Napier GS300

Established 2026-09-15. What the EMU Black v2→v3 import tool carried, what it broke, what is
still blank, and which of those blanks Will has said may be filled from the Supra tune.

**Cross-reference exception (stated by Will, 2026-09-15):** the blanket "never carry a value from the
Supra" rule in [`my_car.md`](my_car.md) is relaxed for three categories only — **lambda target
tables, ignition maps, and PID settings**. Everything else in this list stays car-specific.

## Files compared

| Role | File | Notes |
|---|---|---|
| v2 source (what Josh was running) | `gs300/tunes/Napier_post_rebuild v2.175 source 09142026.emub` | `project version="2.175"`, 1535 symbols. Copied from `EMU_BLACK\Napier_GS300\Napier_post_rebuild.emub` (mtime 2026-09-14) |
| v3 import result | `gs300/tunes/Napier_GS300 v3 import 09152026.xml.emub3` | `project version="3.059"`, 1771 symbols. From `EMU_BLACK_V3\Napier_GS300\Napier_GS300.xml.emub3` (2026-09-15 16:05) |
| Supra donor | `supra/tunes/supra export 09152026.xml.emub3` | `3.059`, same 1771 symbols. From `EMU_BLACK_V3\Supra\Supra.xml.emub3` (2026-09-15 16:05) |

Method: parsed every `<symbol>` in all three; classified each v3 symbol as *carried from v2
unchanged*, *altered by the tool*, or *new in v3* (no v2 ancestor). Headline counts:

- 658 symbols carried from v2 byte-identical.
- 134 symbols altered by the tool (unit rescales, re-binned tables, a few resets).
- 979 symbols new in v3. **757 of those are byte-identical to the Supra** — firmware defaults
  neither car has touched. Not blanks; ignore them.
- 222 new-in-v3 symbols differ from the Supra — this is where the real gaps live.
- ~600 v2 symbols have no v3 name (retired or renamed). The renamed ones are where the tool
  silently dropped Josh's values (idle PID, boost PID, VVT PID, launch control, overrun).

Re-run: the parse/diff script is trivial (regex over `<symbol name= value=|data=>`); nothing in
this note should be trusted past the next export — re-read the XML.

## 1. Carried over correctly — no action

Confirmed byte-identical to v2 (or converted with the right unit change):

- `veTable`, `ignTable`, `lambdaTable`, `rpmBins`, `mapBins` — the core maps.
- `dwellTime`, `injOpeningTimeTbl` (GS300's own coils/injectors — do not touch from Supra).
- `tpsMin`/`tpsMax`, trigger block (`primTrig*`, `secTrig*`, `firstTriggerTooth`, `triggerAngle`,
  `secTriggerSensitivity`).
- `idleValveType`, `idlePWMOutput`, `idleFrequency`, `idleValveMaxDC` — GS300 idles on a **PWM
  valve**, not DBW (`idleValveType` = 2 vs Supra 6). `idleActiveAirflow` = v2 `idleDCREF` ×2
  (ubyte 0.5/count) — faithful.
- `boostTarget1` — v2 raw was absolute kPa at 2 kPa/count; v3 is gauge kPa. Conversion checks
  out (v2 raw 105 → 210 abs → v3 110 gauge). `boostOutput` carried.
- `warmupTbl`, `aseTbl` values converted from v2 "100 = neutral" to v3 "0 = neutral" correctly
  (but see §2 — their CLT axes are garbage).
- `fuelTrim1..6` converted 100/101/102 → 0/+1/+2.
- `idleOnIfTPSBelow`/`idleOffIfTPSOver` 2/3 → 20/30 (1 % → 0.1 % units, same meaning).
- `firingOrder1..6` = 1,2,3,1,2,3 = v2 `ignitionEvent1..6`. That is a **3-output wasted-spark
  layout** and `ignOutputsMode` = 0. Consistent with v2, so not an import error — but it is
  worth Josh confirming that is how the coils are actually wired before first fire on v3.
- Parametric outputs: v2 `po1..po8` were all unconfigured (output 0), so the empty v3
  `userFunctions` loses nothing. `coolantFanOutput`/`coolantFanActTemp`/`coolantFanHyst` carried.

## 2. Broken or blanked by the import — must be rebuilt (car-specific)

| Area | Symbols | What happened |
|---|---|---|
| **Idle PID** | `idleAirFlowKP/KI/KD` = 0, `idleIgnitionKP/KI/KD` = 0 | v2 `idleP`=10 `idleI`=12 `idleD`=0 `idleIntWindup`=80/`idleIntWindupMinus`=160, `idleIgnMaxAdvance`=7 `idleIgnMaxRetard`=10 `idleAngleChangeRate`=20 were all dropped. **Idle closed loop is dead until these are set.** See §3 for what the Supra can lend. |
| Idle ignition target | `idleIgnitionTargetTbl` flat 12°, `idleIgnitionMaxTorqueAngleTbl` 30, `idleIgnitionMinTorqueAngleTbl` −10, `idleIgnAngleCorrection` all 0 (v2 had 19,16,10,3,0,−7,−13,−20) | v3 idle-ignition scheme is new; tool filled defaults. |
| Idle bins | `idleRPMBins` = 500,729,959,1163,1367,1571,1851,**6975** ; `idleErrBins` re-binned ±250 | Nonsense last bin; `idleArmedAirFlow` (87→51 % descending) rides on it. Re-bin. |
| Idle gates | `idleOpenLoopOverVss` 10 (1 km/h), `idleClutchEnablesClosedLoop`/`idleNeutralEnablesClosedLoop` 0, `idleMinMapToActivate` 0, `idleControlAfterstartDelay` 5, `idleRAMPDownOffset` 100 / `idleRAMPDownDecayRate` 50, `idleAirPIDOutMin/Max` ±50 | Defaults. v2 `idleControlMaxRPM`=1600 has no v3 home. |
| `idleCrankingDC` | flat 20 → 10 % ×4 | v2 scalar 20 became 4-cell table at 0x14 = 10 % (0.5/count). **Halved** — either the tool mis-scaled or v2 was also 0.5/count; check what EMU displays. |
| **Cranking fuel** | `crankingCorrTbl` **all 0**, `crankingCorrTbl2` all 0, `cltBinsCranking` = −40,106,106,107,108,108,109,109 | v2 `crankingTbl` (16×5, 78 % cold → 17 % hot) was not mapped; the CLT axis is corrupt. |
| **ASE axis** | `aseCltBins` = −40,107,108,108,109,109 ; `aseRuntimeBin` 0,3,7,12,17,22 | Values in `aseTbl` converted but the CLT axis is corrupt → the table is unusable as-is. |
| Accel enrichment | `accEnrichment` all 0, `accEnrichType` 0, `accCLTFactor` all 0, `tpsRateBins` default | v2 `accDTPSRate`/`accTPSFactor`/`accRPMFactor`/`accCLTFactor`/`accEnrichLimit`=120/`accEnrichSustainRate`=160 all dropped. No transient fuel. |
| **Boost control** | `dcBoostRef1` **all 0** (v2 had a full 10×10 WG base-DC map 10–110 %), `boostKP/KI/KD` = 400/4000/11 (defaults; v2 Kp 2 / Ki 64 / Kd 0 dropped), `boostControlType` 0→1, `boostMinRPM` 2000→500, `rpmBoostBins` re-binned, `boostGearLimit` flat 1000 | Target survived, everything that delivers it did not. |
| **VVT PID** | `vvtCam1KP/KI/KD` = 768/4096/0, `vvtCam1IntegralLimitMin/Max` ±3, `vvtCam1tOutputMin/OutputMax` ±15 | v2 `vvtCam1PTerm`=30 `ITerm`=2 `DTerm`=1 `IntegralLimit`=3 dropped. `cam1AdvTbl` was re-sampled (values shifted) — check it in EMU. `vvt1MinDC/MaxDC` 10/90 = v2, OK. |
| **Launch control** | `lcActivationInput` 0, `lcRPMTarget` flat 4000, `lcMaxVSS` 1, `lcRPMActivationDelta` 2000 | v2 `lcInput`=60, `lcActivationRPM1`=3800, `lcActivationTPS1`=50, `lcHardCutRPM1`=4500, `lcHardCutType1`=1 dropped. Josh used LC (see v2 filename `lowerLCVSS`). |
| **Overrun** | `overrunRPMActive` 7000 / `overrunRPMInactive` 2000, `overrunPPSOn/Off` 50/60, `overrunIgnition` flat −10 | Fuel cut effectively never engages. v2 `overrunCutRate`=20 dropped. v2 had **no** overrun-ignition table — the −30° decel retard was baked into `ignTable`'s 20 kPa column above 3900 rpm. v3 has `overrunIgnition`; move it there and clean the ign map (§3). |
| Rev limiter | `revLimit1*` defaults | v2 `enableSoftRevLimiter`=1, `controlRange`=300, `softLimiterIgnRetard`=30, `softLimiterCurSparkPercent`=95. v3 defaults happen to be 300 / 90 % / 30° so it's close, but confirm `revLimit1CutType`. |
| Closed-loop fuel | `shortTermEnable` 0 (was 0 in v2 too), `lambdaTrimKP/KI` 1024/2560 → 128/512 (inconsistent ÷8, ÷5 rescale), `shortTermMinClt` 80→50, `shortTermMinRPM` 600→900, `shortTrimTransientDelay` 500→100, `shortTermMinLambda` 0.77 | Tool changed Josh's gates. Off anyway; set deliberately when enabling. |
| Knock | `knockSensorGainCyl1..6` 38 (= v2 `knockSensorGain`), `ksInputCylinder1..6` all 1, `rpmBinsKnock`/`mapKnockBin` re-binned, `knockNoiseTable` partly re-filled | Single sensor input assumed. Aristo has two knock sensors — set `ksInputCylinder2/4/6` if the second is wired. Noise table needs a fresh sweep regardless. |
| Sensor cals | `cltSensorCal` 0→5 and `cltTbl` rewritten; `iatTbl` rewritten; `oilTempCal`/`oilTempCalBins` rewritten; `mapSensorCal` 4→2 points; `fuelLevelCal`, `fprDelta`/`fprDeltaCorrection` re-binned | The tool swapped a custom CLT curve for preset 5. Verify CLT/IAT readings against a known temperature before trusting warm-up or idle tables. |
| Misc resets | `checkEngineLightOutput` 2→0, `failReportWBO/IAT/CLT/MAP/Knocking` 1→0, `rpmMultiplier` 300→100, `canBusDashType` 100→0, `extPortDeviceID` 4→0, `acMaxCLT` 120→110, `idlePIDUpdateInterval` 25→200, `TPSScaleTbl` reshaped, `primePulseTable` 20→24 | Small, but each was a Josh setting the tool overwrote. |
| DBW | `dbwMode` 0, `ppsFunction` 0, `tpsInputMain`/`ppsInputMain` 0, `dbwCharacteristic1/2` default, DBW PIDs default | Not configured — expected; the DBW-vs-cable+IACV decision in [`high_idle_after_cd009_swap.md`](high_idle_after_cd009_swap.md) §9 is still open. Nothing here to do until that is settled. If DBW: `idleValveType` must change and the entire idle-airflow block re-scales to `idleDBWTargetMin/Max`. |

## 3. What the Supra can lend (Will's three categories)

### Lambda target — already identical
`lambdaTable` is **byte-for-byte the same** in both cars (max |Δλ| = 0.00 over all 80 cells).
`lambdaTable2` differs but GS300 is not flex (`fuelComposition` 0, `tblsLambda` 0) so it is unused.
Nothing to copy.

### Ignition map — same lineage, three real differences
`ignTable` (16×20) on both cars descends from the same base map: rows ≥ 2895 rpm agree within
±2° except for the 20 kPa column. Differences worth a decision:

1. **20 kPa column, ≥ 3921 rpm: GS300 = −30°, Supra = 51–66°.** That is Josh's v2 decel retard
   living in the ign map. In v3 the Supra does this with `overrunIgnition` (rows 20,20,20,20,20,
   14,−30,−30 on `overrunRPMBins` 1000…7000) — cleaner, gated by pedal/RPM instead of a MAP
   column. Recommend: copy Supra `overrunIgnition` + `overrunRPMBins` + `overrunIgnEnterRate`/
   `overrunIgnExitRate`, then fill the GS300's −30 column from the adjacent 35 kPa column.
2. **1526–2553 rpm, 20–79 kPa: GS300 runs 4–20° more advance** (e.g. 2211/49 kPa: GS 75 vs Supra
   63). Supra pulled this region down during idle/drive-wobble work. Josh's fuel and cams differ;
   this is a tuning choice, not a blank.
3. Below 1184 rpm the Supra is flat 36°, GS300 32° — idle-region timing, tied to the idle
   ignition PID's base angle. Set together with the idle PID.

Supra `ignTable2` is the ethanol map — irrelevant to a non-flex car.

### PID settings — what transfers and what does not

| PID | Supra values (`supra export 09152026`) | Transfer? |
|---|---|---|
| Idle ignition (`idleIgnitionKP/KI/KD`, `idleIgnitionIntegralLimitMin/Max`) | 51 / 5 / 0, ±5 | **Yes.** RPM-error → ignition-angle loop; the plant (2JZ inertia, torque-per-degree at idle) is the same engine family. Also take `idleIgnitionMaxTorqueAngleTbl` (70) / `idleIgnitionMinTorqueAngleTbl` (26…20) / `idleIgnitionTargetTbl` / `idleIgnAngleCorrection` as the starting shape. |
| Idle airflow (`idleAirFlowKP/KI/KD`, `idleAirFlowIntegralLimitMin/Max`, `idleAirPIDOutMin/Max`) | 1024 / 1024 / 0, −25/+15, ±25 | **No, not directly.** Supra's loop drives a DBW blade through a 2.4–8.0 % TPS authority window; GS300 drives a PWM valve 0–90 % DC. 1 % of output moves very different amounts of air. Use Supra gains only as an order-of-magnitude sanity check; start from the v2 `idleP`/`idleI` ratio (10:12) and retune on the car. |
| VVT cam 1 (`vvtCam1KP/KI/KD`, `IntegralLimitMin/Max`, `tOutputMin/OutputMax`) | 1434 / 5 / 3, ±20, ±20 | **Yes.** Same OCV/phaser hardware on both 2JZ-GTE VVT-i heads. Supra `vvtCam1OutputFrequency` 200 Hz vs GS300 600 Hz and `vvtCam1SteadyPosDC` 44 vs 45 — keep GS300's own frequency unless it hunts. `vvtCam1MinCoolantTemp` 88 (Supra) vs 10 (GS300) — Josh's choice. |
| Boost (`boostKP/KI/KD`, `boostOutputMin/Max`, `boostMargin*`) | 4096 / 1536 / 51, ±15, −35/+15/7 | **Gains yes as a starting point; base map no.** Same control structure (PID on top of `dcBoostRef1` feed-forward). GS300's wastegate/turbo differ so `dcBoostRef1` must come from v2's map (10×10 → re-sample onto v3 8×8 `rpmBoostBins`×`ppsBoostBins`), not the Supra's. |
| Lambda STFT (`lambdaTrimKP/KI/KD`, `lambdaTrimIntegralLimitMin/Max`, `shortTrimKPScale/KIScale`, `shortTermRichLimit/LeanLimit`) | 32 / 160 / 0, −8/+10, KP scale −76/−26/0/0 | **Yes** if/when `shortTermEnable` is turned on — the loop acts on injector PW, plant is the same. |
| DBW motor PIDs (`dbwOverLimp*`, `dbwUnderLimp*`, `dbwIntegratorResetThreshold`) | 1024/13002/58 fric 28 ; 860/13002/58 fric 23 | **No.** Supra is on a Lexus DBW body with a Bosch swap planned; GS300 throttle is Aristo ETCS-i (and may end up cable). Run the DBW calibration tool on the car if DBW is chosen. |
| WBO heater/pump PIDs | identical already | — |

### Other Supra items that are *not* in Will's three categories but are structurally car-agnostic
Listed only so they are not forgotten; Will decides.
- `overrunIgnition`/`overrunRPMBins`/`overrunIgnEnterRate`/`overrunIgnExitRate` (see ignition §1).
- `accEnrichment` + `accEnrichType` 1 + `accDecayRate` 35 — a shape to start from; magnitudes
  depend on injectors/manifold.
- `idleAfterstartRPMincrease`, `idleRAMPDownOffset` 200 / `idleRAMPDownDecayRate` 100,
  `idleControlAfterstartDelay` 3 — idle-entry behaviour that was tuned on the Supra
  (`supra/notes/idle_drive_wobble.md`).

## 4. Verify-before-trusting list (import artifacts, not blanks)

Things the tool changed that look plausible but were not Josh's numbers:

- `cltSensorCal`/`cltTbl`, `iatTbl` — sensor curves (see §2).
- `idleCrankingDC` halved (20 → 10 %).
- `cam1AdvTbl` re-sampled; `vvtiRpmBins10` differs by 1 rpm in places (harmless).
- `lambdaTrimKP/KI` rescaled inconsistently (÷8 vs ÷5).
- `shortTermMinClt`/`shortTermMinRPM`/`shortTrimTransientDelay` changed.
- `failReport*` all zeroed — no sensor-failure CEL.
- `rpmMultiplier` 300 → 100 (tacho output scaling).
- `flatShiftTPSLimit` 0 → 90, `flatShiftCutOffRPM` 5500 carried, `flatShiftInput` 0 (off).

## Related
- [`my_car.md`](my_car.md) — identity card; the cross-reference rule and its 2026-09-15 exception.
- [`high_idle_after_cd009_swap.md`](high_idle_after_cd009_swap.md) — DBW vs cable+IACV decision.
- `../../notes/tune_feature_tree.md` — where each v3 symbol lives in the software tree.
- `../../supra/notes/idle_drive_wobble.md` — provenance of the Supra idle PID values.
