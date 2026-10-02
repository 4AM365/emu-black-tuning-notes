# Fuel-mixture parameter inventory (Supra, EMU Black V3)

Built 2026-09-29 from `EMU_BLACK_V3\Supra\Supra.xml.emub3` (09-22 14:30) and a symbol-level diff against
`supra/tunes/supra export 09192026 post-tb-clean.xml.emub3` (the calibration under the on-target 09-19 `fullchannels.csv`).
Values are deliberately not copied here — read them from the current XML at analysis time. The binary `.emub3`/QuickSave
after 09-22 cannot be read; **anything edited after 09-22 is invisible to this inventory** (ask Will for a fresh XML export).

**Diff result:** between the 09-19 post-clean export and 09-22 only `cltSensorCal`, `idleActiveAirflow` (2 cells) and checksums
differ. **No fuel-relevant symbol changed.** The rich shift therefore did not come from a tune edit made by 09-22.

## 1. Base dose (what sets pulse width at a cell)
- `veTable`, `veTable2` (16 × 20, MAP × RPM), blended by `tblsVEBlend` on ethanol content (`FF Blend VE` in the log)
- `mapBins`, `rpmBins`, `rpmBins2` — axes
- `injectorsSize`, `injOpeningTimeTbl` (dead time, 12 voltage × 4 rows), `fprDelta` + `fprDeltaCorrection` (√ΔP model), `fuelPressureInput`, `fuelPressureCal(Bins)`, `fprDelay`, `fprMinError/MaxError`, `fprFailSafeEnable`
- Per-cylinder trims: `fuelTrim1..8` (which table each cylinder uses), `fuelTrim1..4Table`, `fuelTrimLoad`, `fuelTrimRPM` (log: `Injector n trim`)
- `injectionAngle`, `injAngleCtrl` (timing only)

## 2. Fuel type / ethanol
- `ethanol10Bins` + `ethanolFuelScale` (log `Ethanol correction`), `ffEnableFFSensor`, `ffEthanolContentIfError`, `ethanolContentPercent`, `ffEnableCustomCal`, `ffMaxTPS`
- Blends by ethanol: `tblsVEBlend`, `tblsFFLambdaBlend`, `tblsFFIgnBlend`, `tblsFFASEBlend`, `tblsFFWarmupBlend`, `tblsFFCrankingBlend`; twin tables `lambdaTable2`, `warmupTbl2`, `aseTbl2`, `crankingCorrTbl2`
- `wboFuelType` (WBO lambda→AFR display; the `AFR` channel is not E-corrected)

## 3. Temperature and density
- `chargeTempTbl` (8 MAP × TPS; weight of CLT in `Charge temp`), `mapBinsAirCharge`, `tpsBinsAirCharge`
- Sensor conversion: `iatTbl` + `voltage5VIATBin`, `cltTbl` + `voltage5VCLTBin`, `iatSensorType/Cal`, `cltSensorType/Cal`; failsafes `failSafeIATValue/CLTValue`, `failReportIAT/CLT`
- `fuelTempCorr` + `fuelTempBin` (dose vs fuel temp), `fuelTemperatureCal(Bins)`, `fuelTempFailSafe`, `fuelTempInput`
- `baroCorrection`, `baroBins`, `enableBaro`/`baroOption` (baro is fixed in these logs → correction inert)
- `failSafeMAPValue`, internal MAP (`useBuiltInMap`)

## 4. Enrichment (inert at hot steady idle, matter cold/transient)
- Warm-up: `warmupTbl(2)`, `mapBinsWarmup`, `tpsBinsWarmup`, `warmupTblLambdaCorrTbl(2)`
- After-start: `aseTbl(2)`, `aseCltBins`, `aseRuntimeBin`
- Cranking: `crankingCorrTbl(2)`, `crankingLambdaTarget`, `primePulseTable`
- Accel/decel: `accEnrichType`, `accEnrichment`, `accEnrichRPMBins`, `accCLTFactor`, `accThrottleThreshold`, `accMAPThreshold`, `accDecayRate`, `accHoldCycles`, `accEnableAsync`, `accEnrichmentAsync` (+ bins/factor), `accEnrichCustomCorr*`
- Overrun: `overrunFuel(2)`, `overrunExitEnrich`, `overrunExitDecayRate`, `overrunEnable`, `overrunPPSOn/Off`, `overrunRPMActive/Inactive`
- Custom: `fuelCustomCorr*` (three, axis/trigger symbols present; log channels `Fuel custom correction 1–3` are 0)
- Timer/AC/fan: `fuelCorrTimer`, `idleCoolantFanCorr` (airflow, not fuel)

## 5. Closed loop (moves the *delivered* mixture toward `lambdaTable`)
- Targets: `lambdaTable(2)`, `lambdaDelay`, `crankingLambdaTarget`
- STFT enable/gates: `shortTermEnable`, `shortTermMinClt`, `shortTermMinRPM/MaxRPM`, `shortTermMinMAP/MaxMAP`, `shortTermMaxTPS`, `shortTermDelay`, `shortTermDisableSwitch`, `shortTermLockDuringAccEnrch`, `shortTrimTransientDelay`
- **`shortTermMinLambda` / `shortTermMaxLambda`** — raw ÷ 128 gives the λ window in which STFT runs. Raw 102 → **0.797**, matching the observed switch-off (flag off below ~0.795 in the 09-29 log, n = 1865 vs all-on above 0.80). This is the traced mechanism for "STFT never engages at 0.78"; Max raw 154 → 1.203.
- PID: `lambdaTrimKP/KI/KD`, **`lambdaTrimIntegralLimitMin/Max`** (Min binds: log floor −8.06), `shortTrimKPScale`, `shortTrimKIScale` (airflow-indexed gain scalers — both negative at the low-airflow bins, i.e. STFT is deliberately slowest at idle), `shortTermRichLimit`, `shortTermLeanLimit` (airflow-indexed)
- WBO conversion (measurement side): `wboLambdaTable`, `wboIPNormTable`, `wboPumpKP/KI/KD`, `wboHeaterKP/KI/KD`, `wboHeaterMode`, `wbo2Enable`, `wboAFRAt0V/5V`

## 6. Not fuel but changes what the fuel equation sees
- Idle airflow/DBW tables (change MAP at a given RPM, not the dose per MAP)
- Cam: `cam1AdvTbl`/VVT (residual gas, real air per cycle); ignition tables (EGT, not λ)
- `voltage5VCLTBin`/`cltTbl` dead band (CLT-keyed items see a flat 96)

## 7. Log channels that show each term
`VE`, `FF Blend VE`, `Ethanol correction`, `Charge temp`, `IAT`, `Fuel Temp Correction`, `Effective fuel pressure`, `Fuel pressure error`, `Fuel pressure correction`, `Injectors cal. time`, `Injectors PW`, `Injector n trim`, `Warmup enrichment`, `Afterstart Enrichment`, `Acc. enrichment %`, `F.*` flags (1 = that correction is active), `Lambda target`, `Lambda target from table`, `Lambda error mult.`, `Short term trim`, `F.Short term trim`, `Estimated airflow`, `Lambda 1`, `WBO IP Meas.`, `WBO RI`.
