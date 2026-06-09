# Rolling return-to-idle wobble ("drive wobble") — Supra measured specifics

Build-specific numbers behind [`notes/idle_stall.md`](../../notes/idle_stall.md) §H and the consolidated [`notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md). The generic notes hold the mechanism; this file holds the measured values for this car.

## Observed event

- RPM craters well below idle target: **~1800 → 525 rpm at a 1200 target**, then limit-cycles **525 ↔ 1390** during a neutral coast-down to idle while the car is still rolling.
- Confirmed decoupled: RPM/VSS ratio swings 8× (impossible in a fixed gear) — the driver neutral-shifts toward a stop, engine free-falls toward idle.

## Fault 1 — rich low-RPM VE bog

- As RPM craters and MAP rises toward **60+ kPa**, speed-density over-fuels. Measured `Lambda 1` dives to **0.68 (AFR 9.9)** against a **0.93** target — low-rpm VE is **~17–19% rich** at MAP **35–64 kPa**.
- **Baseline caveat:** the −17–19% figure is from *pre-correction* logs at **E25** (not the usual E60). A global **−18% pump (`veTable`) / +10% ethanol (`veTable2`)** correction was applied afterward (v2 export). Net effect is fuel-dependent through `tblsVEBlend`: ~**0%** at E60 (~38% pump weight — the −18/+10 nearly cancel) but ~**−11%** at E25 (73.5% pump). So on v2 the dip residual is still **~−18% rich at E60** but only **~−9% at E25**. A lean computed from the E25 log is right only for E60; at E25 it over-leans ~9% → lean-stumble risk. **Always re-measure lambda on a v2-calibration dip log at the fuel you actually run before leaning the 500/842 rows.**
- **`rpmBins` starts at 500 (`1F4`).** The 500-rpm VE row governs fueling precisely when RPM craters into a dip; left as a verbatim copy of the 842 row it is ~17% too rich. Lean toward λ0.93. The 842 row and the 1184 idle row (~9% rich at steady idle, **λ0.844**) want the same treatment — richness increases as RPM drops, so the lean deepens toward the 500 row.
- `Short term trim` is clamped ~**±2–3%** with slow integration (intentional), so it can't correct a fast dip and won't reveal true VE. Set VE from measured lambda error, apply ~80% first, lean both `veTable` and `veTable2` by the same ratio.

## Fault 2 — fan-gated airflow drops out at speed

- The **+13% `idleCoolantFanCorr`** is VSS-gated **off above ~56 km/h**. On a return from above ~56 km/h base idle airflow is the bare **~26.5%** table value instead of **~39%** (fan-on), and the airflow PID is clamped at **+12** — not enough to hold. Below ~56 km/h the fan is on and returns catch cleanly.
- Fixes that don't add idle variation: more airflow-PID authority (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`) and a faster `idlePIDUpdateInterval` (**200 ms → ~50 ms**). Leave the fan +13% — correct load-comp.

## Dead ends (this build)

- Raising `idleActiveAirflow` 1000/1100 rows: indexed by idle **target**, which floors at 1200 (`idleRPM` bottoms at 1200), so those rows are never read. The VE table is indexed by actual rpm×MAP, so its 500-rpm row is the live lever.
- `idleIncreaseTargetAboveVSS`: would work but adds a target step — rejected to keep low-speed heat-soak idle clean.

## Feed-forward sizing worked point (this build)

Before the "halve the feed-forward" principle was applied, `idleCustomCorrection` was sized near full steady-state comp at the operating CAT band. PID sat at **−9.75% (saturated negative)** at the worst log point (**t=178.64, `supra/logs/20260526_1644.csv`**) with TPS only **1.1%** above the actuator floor. After converting to scalar mode and halving the corrections, PID has authority both directions and worst-case stall margin grows.
