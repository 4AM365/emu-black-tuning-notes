# EMU Black tune — feature tree (software-aligned)

All tunable symbols in the project, filed under the **EMU Black software’s own feature tree** (the 23 top-level pages of the tuning software). This is the authoritative organization; each H2 below is a software page, each H3 a sub-node. Tables marked **▸** with `width×height`; scalars listed compactly.

> **Source:** `supra/tunes/supra xml v3 05292026.xml.emub3` (v3.059). **1771 symbols** (428 tables, 1343 scalars). Software-page assignment is derived from symbol names; a few niche symbols may sit one node off from the software’s exact placement.

## Page index → notes coverage

Each of the 23 software pages has its own notes page (rich tuning pages where we have material, concise config references elsewhere):

- **Sensors and inputs** (397) — [sensors_and_inputs.md](sensors_and_inputs.md)
- **Engine start** (39) — [engine_start.md](engine_start.md)
- **Fueling** (149) — [fueling.md](fueling.md)
- **Ignition** (47) — [ignition.md](ignition.md) · [timing.md](timing.md)
- **Overrun** (36) — [overrun.md](overrun.md)
- **Knock sensors** (35) — [knock_sensors.md](knock_sensors.md)
- **Idle** (92) — [idle.md](idle.md)
- **Functions** (83) — [functions.md](functions.md)
- **Outputs** (61) — [outputs.md](outputs.md)
- **Boost** (131) — [boost.md](boost.md)
- **DBW** (55) — [dbw.md](dbw.md)
- **Traction control** (44) — [traction_control.md](traction_control.md)
- **VVT** (88) — [vvt.md](vvt.md)
- **Sport** (148) — [sport.md](sport.md)
- **Nitrous** (49) — [nitrous.md](nitrous.md)
- **Tables switching** (27) — [tables_switching.md](tables_switching.md)
- **Engine protection** (44) — [engine_protection.md](engine_protection.md)
- **Timers** (6) — [timers.md](timers.md)
- **DSG Gearbox** (41) — [dsg_gearbox.md](dsg_gearbox.md)
- **Other** (43) — [other.md](other.md)
- **CAN, Serial** (144) — [can_serial.md](can_serial.md)
- **Log** (12) — [log.md](log.md)
- **Gauges** (0) — [gauges.md](gauges.md)


## Sensors and inputs  ·  397


### VSS and Gearbox  (94)

- **▸ `boostDCGearCorrection`** (8×1)
- **▸ `boostGearCorr`** (8×1)
- **▸ `boostGearLimit`** (8×1)
- **▸ `dbwSpeedOpeningScale`** (8×1)
- **▸ `dsgBlipGear`** (6×1)
- **▸ `gearBins`** (8×1)
- **▸ `gearBinsPS`** (7×1)
- **▸ `gearSensorBins`** (10×1)
- **▸ `gearSensorCalLower`** (10×1)
- **▸ `gearSensorCalUpper`** (10×1)
- **▸ `gearShiftDownSensorV`** (10×1)
- **▸ `gearShiftTqRedCut`** (10×1)
- **▸ `gearShiftTqRedDBWCorr`** (10×1)
- **▸ `gearShiftTqRedIgnCorr`** (10×1)
- **▸ `gearShiftUpSensorV`** (10×1)
- **▸ `tcDiffSlipGearMulitplier`** (8×1)
- **▸ `tcGearPercent`** (8×1)
- **▸ `tcPercSlipGearMulitplier`** (8×1)
- **▸ `tckPDiffGearScale`** (8×1)
- **▸ `tckPPercGearScale`** (8×1)
- **▸ `vssBins`** (16×1)
- `VSSInputFilter`, `VSSPullup`, `VSSSensorType`, `VSSTrigerEdge`, `drivenAxleBias`, `drivenAxleDivider`, `drivenAxleFilter`, `drivenAxleRatio`, `drivenAxleSource`, `dsgGearboxCode`, `dsgSelectorGear1`, `dsgSelectorGear2`, `dsgSelectorGear3`, `dsgSelectorGear4`, `dsgSelectorGear5`, `dsgSelectorGear6`, `fiat500ReverseGear`, `gearBoxEnable`, `gearBoxRejectIfClutchPressed`, `gearBoxRejectIfGearUnknown`, `gearBoxShiftBlipControlType`, `gearBoxShiftControl`, `gearBoxShiftMinRPM`, `gearBoxShiftMinVSS`, `gearBoxShiftThrottleKickerOutput`, `gearCutUseTPS`, `gearDelay`, `gearDetectionType`, `gearRatio1`, `gearRatio2`, `gearRatio3`, `gearRatio4`, `gearRatio5`, `gearRatio6`, `gearRatio7`, `gearRatio8`, `gearRatioR`, `gearRatioTolerance`, `gearSensorInput`, `gearSensorLeverTimeout`, `gearShiftArmingTime`, `gearShiftExternalControllerDown`, `gearShiftExternalControllerUp`, `gearShiftMaxTPSToCut`, `gearShiftMinTPSToCut`, `gearShiftTorqueCutType`, `gearboxSensorDetectionTime`, `gearboxSensorFailSafeMax`, `gearboxSensorFailSafeMin`, `gearsLayout`, `nonDrivenAxleBias`, `nonDrivenAxleDivider`, `nonDrivenAxleFilter`, `nonDrivenAxleRatio`, `nonDrivenAxleSource`, `numGears`, `psFirstMaxVehicleSpeed`, `psNeutralMaxVehicleSpeed`, `psReverseMaxVehicleSpeed`, `revMatchMinGear`, `shiftLightGear1RPM`, `shiftLightGear2RPM`, `shiftLightGear3RPM`, `shiftLightGear4RPM`, `shiftLightGear5RPM`, `shiftLightGear6RPM`, `speedRatio`, `speedoMultiplier`, `speedoOutput`, `tcGearDisableTime`, `vssFilter`, `vssSource`, `wheelSpeedSource`

### TPS, PPS  (47)

- **▸ `TPSScaleTbl`** (6×1)
- **▸ `eTqMapBins8`** (16×1)
- **▸ `eTqRpmBins8`** (12×1)
- **▸ `ppPlausibilityBins`** (8×1)
- **▸ `ppsBoostBins`** (8×1)
- **▸ `ppsPlausibilityTable`** (8×1)
- **▸ `preThrottleBoostCal`** (2×1)
- **▸ `preThrottleBoostCalBins`** (2×1)
- **▸ `tpsBins`** (16×1)
- **▸ `tpsBins7TC`** (7×1)
- **▸ `tpsBins8`** (12×1)
- **▸ `tpsBins8B`** (8×1)
- **▸ `tpsBinsAirCharge`** (8×1)
- **▸ `tpsBinsDSG`** (16×1)
- **▸ `tpsBinsL8`** (8×1)
- **▸ `tpsBinsTC`** (8×1)
- **▸ `tpsPlausibilityBins`** (8×1)
- **▸ `tpsPlausibilityTable`** (8×1)
- **▸ `tpsRateAsyncBins`** (5×1)
- **▸ `tpsRateBins`** (9×1)
- `brakePedalInput`, `clutchPedalInput`, `downshiftPostshiftMaxAccPedalPos`, `flatShiftOverrideThrottle`, `ppsCheckFailSafeMax`, `ppsCheckFailSafeMin`, `ppsCheckMaxError`, `ppsFunction`, `ppsInputCheck`, `ppsInputMain`, `ppsMainFailSafeMax`, `ppsMainFailSafeMin`, `ppsMax`, `ppsMin`, `prethrottleBoostFailSafe`, `prethrottleBoostInput`, `revLimit1OverrideThrottle`, `revLimit2OverrideThrottle`, `tpsCheckFailSafeMax`, `tpsCheckFailSafeMin`, `tpsCheckMaxError`, `tpsInputCheck`, `tpsInputMain`, `tpsMainFailSafeMax`, `tpsMainFailSafeMin`, `tpsMax`, `tpsMin`

### Triggers (crank / cam)  (46)

- **▸ `cam2Sensitivity`** (12×1)
- **▸ `secTriggerSensitivity`** (12×1)
- `cam1ToothMax`, `cam1ToothMin`, `cam2ToothRangeMax`, `cam2ToothRangeMin`, `camSequenceInRange1Max`, `camSequenceInRange1Min`, `camSequenceInRange2Max`, `camSequenceInRange2Min`, `disableCamSyncOver`, `dragRaceTrigger`, `firstTriggerTooth`, `fuelCustomCorrTrigger`, `fuelCustomCorrTrigger2`, `fuelCustomCorrTrigger3`, `ignCAMToothMax`, `ignCAMToothMin`, `ignCustomCorrTrigger`, `ignCustomCorrTrigger2`, `ignCustomCorrTrigger3`, `nissanCamSyncWindowWidth`, `numTeeth`, `primTrigAdaptive`, `primTrigEdge`, `primTrigInputDelay`, `primTrigInputFilter`, `primTrigLevelSync`, `primTrigPullup`, `primTrigSensorType`, `primTrigerType`, `primTriggerScopeTraceError`, `pwm2Trigger`, `pwmTrigger`, `scopeTakeSkippedEdges`, `secTrigInputFilter`, `secTrigPullup`, `secTrigSensorType`, `secTrigerEdge`, `secTrigerPattern`, `tcSensitivity`, `timer1Trigger`, `timer2Trigger`, `triggerAngle`, `vvtCam1TriggerOffset`, `vvtCam2TriggerOffset`

### Switches  (41)

- **▸ `diffCtrlRotarySwitchBins`** (4×1)
- **▸ `rotarySwitchBins`** (10×1)
- **▸ `rotarySwitchCal1`** (10×1)
- **▸ `rotarySwitchCal2`** (10×1)
- **▸ `rotarySwitchCal3`** (10×1)
- **▸ `rotarySwitchCal4`** (10×1)
- **▸ `rotarySwitchCal5`** (10×1)
- `invertSw1`, `invertSw2`, `invertSw3`, `invertSw4`, `invertSw5`, `invertSw6`, `invertSw7`, `invertSw8`, `latchingSwitchDefaultState`, `latchingSwitchInput`, `latchingSwitchMinPressTime`, `latchingSwitchNumStates`, `muxSw1Invert`, `muxSw2Invert`, `muxSw3Invert`, `muxSwitchEnable`, `muxSwitchInput`, `pitLimitRotaryInput`, `rotarySwitch1Input`, `rotarySwitch2Input`, `rotarySwitch3Input`, `rotarySwitch4Input`, `rotarySwitch5Input`, `sw1Invert`, `sw2Invert`, `sw3Invert`, `switchInput1`, `switchInput2`, `switchInput3`, `switchInput4`, `switchInput5`, `switchInput6`, `switchInput7`, `switchInput8`

### Pressure  (40)

- **▸ `acPressureCal`** (2×1)
- **▸ `acPressureCalBins`** (2×1)
- **▸ `backPressureCal`** (2×1)
- **▸ `backPressureCalBins`** (2×1)
- **▸ `coolantPressureCal`** (2×1)
- **▸ `coolantPressureCalBins`** (2×1)
- **▸ `crankCasePressureCal`** (2×1)
- **▸ `crankCasePressureCalBins`** (2×1)
- **▸ `diffPressureCal`** (2×1)
- **▸ `diffPressureCalBins`** (2×1)
- **▸ `effectiveFuelPressureBins`** (4×1)
- **▸ `fuelPressureCal`** (2×1)
- **▸ `fuelPressureCalBins`** (2×1)
- **▸ `nitrousPressureCal`** (2×1)
- **▸ `nitrousPressureCalBins`** (2×1)
- **▸ `oilPressureCal`** (2×1)
- **▸ `oilPressureCalBins`** (2×1)
- **▸ `oilPressureCutTbl`** (12×1)
- **▸ `wastegateDomePressureCal`** (2×1)
- **▸ `wastegateDomePressureCalBins`** (2×1)
- `backPressureFailSafe`, `backpressureInput`, `coolantPressureFailSafe`, `coolantPressureInput`, `crankCasePressureFailSafe`, `crankCasePressureInput`, `diffPressureFailSafe`, `diffPressureInput`, `genericPressSensorCal`, `minOilPressureToDeliverFuel`, `nitrousNitrousPressure`, `nitrousPressureFailSafe`, `nitrousPressureInput`, `oilPressCutDisableWhenOilpSensorFails`, `oilPressureCutDelay`, `oilPressureCutEnable`, `oilPressureCutRestartTime`, `oilPressureFailSafe`, `oilPressureInput`, `oilPressureStartDelay`

### Temperature  (37)

- **▸ `boostOilTempLimit`** (5×1)
- **▸ `customTemp1Cal`** (10×1)
- **▸ `customTemp1CalBins`** (10×1)
- **▸ `customTemp2Cal`** (10×1)
- **▸ `customTemp2CalBins`** (10×1)
- **▸ `customTemp3Cal`** (10×1)
- **▸ `customTemp3CalBins`** (10×1)
- **▸ `customTemp4Cal`** (10×1)
- **▸ `customTemp4CalBins`** (10×1)
- **▸ `cylinderHeadCalBins`** (10×1)
- **▸ `cylinderHeadTempCal`** (10×1)
- **▸ `fuelTemperatureCal`** (10×1)
- **▸ `fuelTemperatureCalBins`** (10×1)
- **▸ `oilTempBoostBins`** (5×1)
- **▸ `oilTempCal`** (10×1)
- **▸ `oilTempCalBins`** (10×1)
- `customTemperature1`, `customTemperature2`, `customTemperature3`, `customTemperature4`, `customTemperatureFailSafe1`, `customTemperatureFailSafe2`, `customTemperatureFailSafe3`, `customTemperatureFailSafe4`, `customTemperatureInput1`, `customTemperatureInput2`, `customTemperatureInput3`, `customTemperatureInput4`, `cylHeadTempInput1`, `cylHeadTempInput2`, `diffControlMaxOilTemp`, `genericTempSensorCal`, `oilTempFailSafe`, `oilTempInput`, `vtecMinOilTemp`, `vvtCam1MinOilTemp`, `vvtCam2MinOilTemp`

### IAT, CLT  (22)

- **▸ `chargeTempTbl`** (8×12)
- **▸ `cltBins`** (16×1)
- **▸ `cltBins4`** (4×1)
- **▸ `cltBins8`** (8×1)
- **▸ `cltBoostBins`** (5×1)
- **▸ `cltTbl`** (14×1)
- **▸ `iatBins`** (16×1)
- **▸ `iatBoostBins`** (5×1)
- **▸ `iatTbl`** (14×1)
- `cltFanACMinDC`, `cltFanPWMCtrl`, `cltFanPWMMax`, `cltFanPWMMin`, `cltFanPWMPropGain`, `cltPullup`, `cltSensorCal`, `cltSensorType`, `iatPullup`, `iatSensorCal`, `iatSensorType`, `vvtCam1MinCoolantTemp`, `vvtCam2MinCoolantTemp`

### Oxygen Sensor  (19)

- **▸ `wboIPNormTable`** (20×1)
- **▸ `wboLambdaTable`** (20×1)
- `oxygenSensorType`, `useWBOHeaterForNBOSensor`, `wbo2AFRAt0V`, `wbo2AFRAt5V`, `wbo2Enable`, `wbo2ExtCtrlInput`, `wboAFRAt0V`, `wboAFRAt5V`, `wboExtCtrlInput`, `wboFuelType`, `wboHeaterKD`, `wboHeaterKI`, `wboHeaterKP`, `wboHeaterMode`, `wboPumpKD`, `wboPumpKI`, `wboPumpKP`

### Analog inputs  (15)

- **▸ `vbattVBins`** (12×1)
- **▸ `voltage5VCLTBin`** (14×1)
- **▸ `voltage5VIATBin`** (14×1)
- `an1DigitalFilter`, `an1Pullup`, `an2DigitalFilter`, `an2Pullup`, `an3DigitalFilter`, `an3Pullup`, `an4DigitalFilter`, `an4Pullup`, `an5DigitalFilter`, `an5Pullup`, `an6DigitalFilter`, `an6Pullup`

### MAP, BARO  (15)

- **▸ `baro5VBins`** (2×1)
- **▸ `baroBins`** (8×1)
- **▸ `baroCorrection`** (8×1)
- **▸ `baroSensorCal`** (2×1)
- **▸ `map5VBins`** (2×1)
- **▸ `mapSensorCal`** (2×1)
- `baroAnalogInput`, `baroOption`, `builtInMAPOffset`, `enableBaro`, `mapAnalogIn`, `mapDigitalFilter`, `mapValidVoltageMax`, `mapValidVoltageMin`, `useBuiltInMap`

### Digital inputs  (1)

- `cam2Pullup`

### Other sensors  (20)

- **▸ `egtBins`** (8×1)
- **▸ `egtFuelCorrection`** (8×1)
- `cam2SensorType`, `cyl1EGTProbe`, `cyl2EGTProbe`, `cyl3EGTProbe`, `cyl4EGTProbe`, `cyl5EGTProbe`, `cyl6EGTProbe`, `cyl7EGTProbe`, `cyl8EGTProbe`, `egtAlarmInvOutput`, `egtAlarmOutput`, `egtAlarmTemperature`, `egtAlarmTemperatureALSLC`, `egtAlarmType`, `loadCellSensorFailSafeMax`, `loadCellSensorFailSafeMin`, `loadCellSensorInput`, `pressureSensorType`

## Engine start  ·  39


### Cranking / ASE / warmup  (29)

- **▸ `aseCltBins`** (6×1)
- **▸ `aseRuntimeBin`** (6×1)
- **▸ `aseTbl`** (6×6)
- **▸ `aseTbl2`** (6×6)
- **▸ `cltBinsCranking`** (8×1)
- **▸ `cltBinsWarmup`** (10×1)
- **▸ `crankRevCntBins`** (5×1)
- **▸ `crankingCorrTbl`** (8×5)
- **▸ `crankingCorrTbl2`** (8×5)
- **▸ `idleAfterstartRPMincrease`** (4×4)
- **▸ `idleCrankingDC`** (4×1)
- **▸ `mapBinsWarmup`** (4×1)
- **▸ `primePulseTable`** (8×1)
- **▸ `tpsBinsWarmup`** (4×1)
- **▸ `tpsCrankingBins`** (6×1)
- **▸ `warmupTbl`** (10×4)
- **▸ `warmupTbl2`** (10×4)
- **▸ `warmupTblLambdaCorrTbl`** (10×4)
- **▸ `warmupTblLambdaCorrTbl2`** (10×4)
- `afterstartEnableIgnLock`, `afterstartIgnRestoreRate`, `afterstartIgnitionLockAngle`, `afterstartIgnitionLockTime`, `coolantFanOffDuringCranking`, `crankingIgnAnlge`, `crankingLambdaTarget`, `crankingThreshold`, `gapDetectionScaleCranking`, `idleControlAfterstartDelay`

### Start / stop control  (10)

- **▸ `engineStartDelay`** (8×1)
- `autoStartTime`, `engineStallRevs`, `startDelay`, `startInput`, `startSwitchEnable`, `starterOutput`, `stopInput`, `stopSwitchEnable`, `stopSwitchTimeout`

## Fueling  ·  149


### Per-cylinder trim  (30)

- **▸ `fuelTrim1Table`** (5×5)
- **▸ `fuelTrim2Table`** (5×5)
- **▸ `fuelTrim3Table`** (5×5)
- **▸ `fuelTrim4Table`** (5×5)
- **▸ `fuelTrimLoad`** (5×1)
- **▸ `fuelTrimRPM`** (5×1)
- `fuelCyl1TrimTableIdx`, `fuelCyl2TrimTableIdx`, `fuelCyl3TrimTableIdx`, `fuelCyl4TrimTableIdx`, `fuelCyl5TrimTableIdx`, `fuelCyl6TrimTableIdx`, `fuelCyl7TrimTableIdx`, `fuelCyl8TrimTableIdx`, `fuelTrim1`, `fuelTrim2`, `fuelTrim3`, `fuelTrim4`, `fuelTrim5`, `fuelTrim6`, `fuelTrim7`, `fuelTrim8`, `injCyl1`, `injCyl2`, `injCyl3`, `injCyl4`, `injCyl5`, `injCyl6`, `injCyl7`, `injCyl8`

### Lambda / closed-loop  (26)

- **▸ `lambdaDelay`** (4×1)
- **▸ `lambdaTable`** (8×10)
- **▸ `lambdaTable2`** (8×10)
- **▸ `shortTermLeanLimit`** (4×1)
- **▸ `shortTermRichLimit`** (4×1)
- **▸ `shortTrimKIScale`** (4×1)
- **▸ `shortTrimKPScale`** (4×1)
- `lambdaTrimIntegralLimitMax`, `lambdaTrimIntegralLimitMin`, `lambdaTrimKD`, `lambdaTrimKI`, `lambdaTrimKP`, `nitrousShortTermTrimCorrModer`, `shortTermDelay`, `shortTermDisableSwitch`, `shortTermEnable`, `shortTermLockDuringAccEnrch`, `shortTermMaxLambda`, `shortTermMaxMAP`, `shortTermMaxRPM`, `shortTermMaxTPS`, `shortTermMinClt`, `shortTermMinLambda`, `shortTermMinMAP`, `shortTermMinRPM`, `shortTrimTransientDelay`

### Acceleration enrichment  (25)

- **▸ `accAsyncCLTFactor`** (16×1)
- **▸ `accCLTFactor`** (16×1)
- **▸ `accEnrichAsyncRPMBins`** (4×1)
- **▸ `accEnrichCustomCorr`** (5×5)
- **▸ `accEnrichCustomCorrXBin`** (5×1)
- **▸ `accEnrichCustomCorrYBin`** (5×1)
- **▸ `accEnrichRPMBins`** (6×1)
- **▸ `accEnrichment`** (6×9)
- **▸ `accEnrichmentAsync`** (4×5)
- `acClutchInvert`, `acClutchOutput`, `accAsyncHoldOffCycles`, `accAsyncMaxRPM`, `accAsyncMinTPSRate`, `accDecayRate`, `accEnableAsync`, `accEnrichCorXAxisT`, `accEnrichCorYAxisT`, `accEnrichType`, `accHoldCycles`, `accMAPThreshold`, `accThrottleThreshold`, `dtpsFilter`, `dtpsIntervalBase`, `dtpsUseDBWTarget`

### VE / fuel tables  (22)

- **▸ `fuelIATCorr`** (16×1)
- **▸ `fuelTempBin`** (9×1)
- **▸ `fuelTempCorr`** (9×1)
- **▸ `mapBinsAirCharge`** (8×1)
- **▸ `mapBinsL8`** (8×1)
- **▸ `veTable`** (16×20)
- **▸ `veTable2`** (16×20)
- `fuelComposition`, `fuelCorrTimer`, `fuelCustomCorrXAxisType`, `fuelCustomCorrXAxisType2`, `fuelCustomCorrXAxisType3`, `fuelCustomCorrYAxisType`, `fuelCustomCorrYAxisType2`, `fuelCustomCorrYAxisType3`, `fuelCutAbovePressure`, `fuelCutAbovePressureDelay`, `fuelRailBasepressure`, `fuelRailType`, `fuelTempFailSafe`, `fuelTempInput`, `fuelingType`

### Fuel pump / pressure  (21)

- **▸ `fprDelta`** (12×1)
- **▸ `fprDeltaCorrection`** (12×1)
- **▸ `fuelLevelCal`** (10×1)
- **▸ `fuelLevelCalBins`** (10×1)
- **▸ `fuelPumpAirflowBins`** (5×1)
- **▸ `fuelPumpDC`** (5×1)
- `fprDelay`, `fprFailSafeEnable`, `fprLimitRPM`, `fprMaxError`, `fprMinError`, `fprRPM`, `fuelLevel`, `fuelLevelFilterUpdateRate`, `fuelPressureFailSafe`, `fuelPressureInput`, `fuelPumpASActivity`, `fuelPumpControlType`, `fuelPumpInvertOutput`, `fuelPumpOutput`, `fuelPumpTestOutput`

### Secondary / staged injectors  (11)

- **▸ `stagedInjSplit`** (12×12)
- **▸ `stagedInjectorsCal`** (12×1)
- `secInjBank1`, `secInjBank2`, `secInjInjectorsSize`, `secInjMinInjTime`, `secInjMinMAP`, `secInjMinRPM`, `secInjMinTPS`, `secInjNumInjectors`, `secInjType`

### Custom fuel corrections  (8)

- **▸ `customFuelCorrection`** (8×8)
- **▸ `customFuelCorrection2`** (8×8)
- **▸ `customFuelCorrection3`** (8×8)
- `customFuelCorrection2Modify`, `customFuelCorrection3Modify`, `customFuelCorrectionModify`, `customIATCorrectionModify`, `disableFuelDelivery`

### Injectors & fuel model  (6)

- **▸ `injOpeningTimeTbl`** (12×4)
- **▸ `injectionAngle`** (8×8)
- `alphaNUseMAPForAFR`, `fireInjectorTwicePerCycle`, `injAngleCtrl`, `injectorsSize`

## Ignition  ·  47


### Ignition tables  (43)

- **▸ `customIgnitionCorrection`** (8×8)
- **▸ `customIgnitionCorrection2`** (8×8)
- **▸ `customIgnitionCorrection3`** (8×8)
- **▸ `ignTable`** (16×20)
- **▸ `ignTable2`** (16×20)
- **▸ `lcIgnitionAngleTable`** (5×1)
- **▸ `nitrousS1Ignition`** (6×1)
- **▸ `nitrousS2Ignition`** (6×1)
- **▸ `ralIgnitionCorr`** (6×1)
- **▸ `tcTRIgnitionRetard`** (10×1)
- `disSparkWhenCrankDelay`, `ignCorrTimer`, `ignCustomCorrXAxisType`, `ignCustomCorrXAxisType2`, `ignCustomCorrXAxisType3`, `ignCustomCorrYAxisType`, `ignCustomCorrYAxisType2`, `ignCustomCorrYAxisType3`, `ignCyl1`, `ignCyl2`, `ignCyl3`, `ignCyl4`, `ignCyl5`, `ignCyl6`, `ignCyl7`, `ignCyl8`, `ignInvertPhase`, `ignOutputsMode`, `ignSyncCrankWithCam`, `ignitionTrim1`, `ignitionTrim2`, `ignitionTrim3`, `ignitionTrim4`, `ignitionTrim5`, `ignitionTrim6`, `ignitionTrim7`, `ignitionTrim8`, `lockIgnition`, `lockIgnitionAngle`, `nitrousS1IgnitionOnDelay`, `nitrousS2IgnitionOnDelay`, `pitLimitIgnition`, `sparkDistribution`

### Dwell / coils  (4)

- **▸ `dwellMAPCorr`** (16×1)
- **▸ `dwellRPMCorr`** (20×1)
- **▸ `dwellTime`** (12×1)
- `coilsType`

## Overrun  ·  36


### Overrun / decel cut  (36)

- **▸ `overrunDBW`** (8×1)
- **▸ `overrunDBW2`** (8×1)
- **▸ `overrunFuel`** (8×1)
- **▸ `overrunFuel2`** (8×1)
- **▸ `overrunIgnition`** (8×1)
- **▸ `overrunIgnition2`** (8×1)
- **▸ `overrunRPMBins`** (8×1)
- **▸ `overrunSparkCut`** (8×1)
- **▸ `overrunSparkCut2`** (8×1)
- `lgBoostCorr`, `lgEnable`, `lgFuelCorrection0Based`, `lgFuelCutDelay`, `lgGearCutDelay`, `lgIgnitionRetard`, `lgLeantime`, `lgMaxLambdaLean`, `lgMaxMAP`, `lgMaxRPM`, `lgMaxTPS`, `lgMinClt`, `lgMinMAP`, `lgMinRPM`, `lgMinTPS`, `lgTransientDelay`, `overrunDBWOverride`, `overrunDisableSwitch`, `overrunEnable`, `overrunExitDecayRate`, `overrunExitEnrich`, `overrunIgnEnterRate`, `overrunIgnExitRate`, `overrunPPSOff`, `overrunPPSOn`, `overrunRPMActive`, `overrunRPMInactive`

## Knock sensors  ·  35


### Knock control  (35)

- **▸ `knockGainScaleByGear`** (10×1)
- **▸ `knockNoiseTable`** (8×6)
- **▸ `mapKnockBin`** (6×1)
- **▸ `rpmBinsKnock`** (8×1)
- `failReportKnocking`, `knockActionActive`, `knockActionMaxRPM`, `knockActionMinRPM`, `knockActionMinTps`, `knockFrequency`, `knockIgnRetardRate`, `knockIgnitionRetardControlType`, `knockIntegrator`, `knockMaxIgnRetard`, `knockNoiseUseTPS`, `knockRestoreRate`, `knockSensorGainCyl1`, `knockSensorGainCyl2`, `knockSensorGainCyl3`, `knockSensorGainCyl4`, `knockSensorGainCyl5`, `knockSensorGainCyl6`, `knockSensorGainCyl7`, `knockSensorGainCyl8`, `knockWindowDurationEx`, `knockWindowStart`, `ksInputCylinder1`, `ksInputCylinder2`, `ksInputCylinder3`, `ksInputCylinder4`, `ksInputCylinder5`, `ksInputCylinder6`, `ksInputCylinder7`, `ksInputCylinder8`, `kscutDelay`

## Idle  ·  92


### Idle  (92)

- **▸ `idleActiveAirflow`** (8×5)
- **▸ `idleArmedAirFlow`** (8×1)
- **▸ `idleCustomCorrX`** (5×1)
- **▸ `idleCustomCorrY`** (5×1)
- **▸ `idleCustomCorrection`** (5×5)
- **▸ `idleDBWBlendPointTbl`** (4×1)
- **▸ `idleDBWBlendXAxix`** (4×1)
- **▸ `idleDCBin`** (8×1)
- **▸ `idleDCVECorrection`** (8×4)
- **▸ `idleDCVERPM`** (4×1)
- **▸ `idleDSGTorqueCorr`** (6×1)
- **▸ `idleDSGTorqueLosesBin`** (6×1)
- **▸ `idleErrBins`** (8×1)
- **▸ `idleIgnAngleCorrection`** (8×1)
- **▸ `idleIgnitionMaxTorqueAngleTbl`** (4×1)
- **▸ `idleIgnitionMinTorqueAngleTbl`** (4×1)
- **▸ `idleIgnitionRPMTargetBin`** (4×1)
- **▸ `idleIgnitionTargetCLTBins`** (4×1)
- **▸ `idleIgnitionTargetTbl`** (4×4)
- **▸ `idleInactiveAirFlow`** (8×1)
- **▸ `idlePWMBattCorr`** (12×1)
- **▸ `idleRPM`** (16×1)
- **▸ `idleRPMBins`** (8×1)
- **▸ `idleRPMIncreaseCltBin`** (4×1)
- **▸ `idleRPMIncreaseRuntimeBin`** (4×1)
- **▸ `idleTargetBins`** (5×1)
- `cyclingIdleActivationInput`, `cyclingIdleAirflow`, `cyclingIdleAirflowApplyToDBW`, `cyclingIdleFuelCutOfs`, `cyclingIdleFuelEnrichment`, `cyclingIdleIgnitionAngle`, `cyclingIdleMode`, `cyclingIdleRPMCut`, `cyclingIdleRPMResume`, `idleACRPMIncrease`, `idleAboveVSSTargetIncrease`, `idleAirDCOverrided`, `idleAirFlowIntegralLimitMax`, `idleAirFlowIntegralLimitMin`, `idleAirFlowKD`, `idleAirFlowKI`, `idleAirFlowKP`, `idleAirPIDOutMax`, `idleAirPIDOutMin`, `idleClutchEnablesClosedLoop`, `idleClutchTrgtRPMIncrease`, `idleCoolantFanCorr`, `idleCutCutType`, `idleCutIntegralLimitMax`, `idleCutIntegralLimitMin`, `idleCutKI`, `idleCutKP`, `idleDBWBlendPoint`, `idleDBWTargetMax`, `idleDBWTargetMin`, `idleDCCorrActivationInput`, `idleDCCorrBehaviour`, `idleDCCorrXAxisType`, `idleDCCorrYAxisType`, `idleEnterMode`, `idleEnterModeFunction`, `idleFrequency`, `idleIgnitionControlType`, `idleIgnitionIntegralLimitMax`, `idleIgnitionIntegralLimitMin`, `idleIgnitionKD`, `idleIgnitionKI`, `idleIgnitionKP`, `idleIncreaseTargetAboveVSS`, `idleInvertOutput`, `idleKD`, `idleKeepSteperPowerdOverMAPValue`, `idleMaxCutPercent`, `idleMinMapToActivate`, `idleNeutralEnablesClosedLoop`, `idleOffIfTPSOver`, `idleOnIfTPSBelow`, `idleOpenLoopOverVss`, `idleOverrideAirDC`, `idlePIDUpdateInterval`, `idlePWMOutput`, `idlePWMOutput2`, `idleRAMPDownDecayRate`, `idleRAMPDownOffset`, `idleReverse`, `idleStepperNumSteps`, `idleTargetRampDelay`, `idleUseV3OutToActivatePID`, `idleValveMaxDC`, `idleValveMinDC`, `idleValveType`

## Functions  ·  83


### Diff control  (26)

- **▸ `diffCtrlDCTbl1Acc`** (8×5)
- **▸ `diffCtrlDCTbl1Brk`** (8×5)
- **▸ `diffCtrlDCTbl2Acc`** (8×5)
- **▸ `diffCtrlDCTbl2Brk`** (8×5)
- **▸ `diffCtrlDCTbl3Acc`** (8×5)
- **▸ `diffCtrlDCTbl3Brk`** (8×5)
- **▸ `diffCtrlTPSBin`** (5×1)
- **▸ `diffCtrlVSSBin`** (8×1)
- `diffControlType`, `diffControlXAxis`, `diffControlYAxis`, `diffCtrlCtrlInput`, `diffCtrlDCFor0`, `diffCtrlDCFor100`, `diffCtrlDisableHandBrakeWhenBrakes`, `diffCtrlEnableInput`, `diffCtrlHandbrakeInput`, `diffCtrlLCEnableFixedDC`, `diffCtrlLCFixedDC`, `diffCtrlLCFixedDCSustain`, `diffCtrlOilPumpCtrlType`, `diffCtrlOilPumpOutput`, `diffCtrlOilPumpPressMax`, `diffCtrlOilPumpPressMin`, `diffCtrlOilPumpTimeout`, `diffCtrlWhenTableZero`

### Fan / AC / water-meth  (26)

- **▸ `acEvapCal`** (10×1)
- **▸ `acEvapCalBins`** (10×1)
- `acActivation`, `acEvapMinTemp`, `acEvapTemp`, `acFanInvertOutput`, `acFanOutput`, `acMaxCLT`, `acMaxPressure`, `acMaxRPM`, `acMaxTPS`, `acMinPressure`, `acMinRPM`, `acPressHyst`, `acPressure`, `acTimeToEngage`, `coolantFanActTemp`, `coolantFanDisableWhenNoRPM`, `coolantFanForceOnInput`, `coolantFanHyst`, `coolantFanInvOutput`, `coolantFanOutput`, `coolantFanTimeToEngage`, `coolantFanTurnOnWhenAC`, `coolantFanVSSOff`, `coolantFanWhenCLTFail`

### Cruise control  (18)

- **▸ `ccTargetSpeedBin`** (6×1)
- `ccDeadband`, `ccIntegralLimitMax`, `ccIntegralLimitMaxRate`, `ccIntegralLimitMin`, `ccKD`, `ccKI`, `ccKP`, `ccOutputMax`, `ccOutputMin`, `cruiseControlChangeStep`, `cruiseControlEnable`, `cruiseControlMarginBelowTarget`, `cruiseControlMinSpeed`, `cruiseControlResumeInput`, `cruiseControlSetInput`, `cruiseControlSpeedMinusInput`, `cruiseControlSpeedPlusInput`

### Custom functions / maps  (12)

- **▸ `customFX2Bins8`** (8×1)
- **▸ `customFX3Bins8`** (8×1)
- **▸ `customFXBins8`** (8×1)
- **▸ `customFY2Bins8`** (8×1)
- **▸ `customFY3Bins8`** (8×1)
- **▸ `customFYBins8`** (8×1)
- **▸ `customIX2Bins8`** (8×1)
- **▸ `customIX3Bins8`** (8×1)
- **▸ `customIXBins8`** (8×1)
- **▸ `customIY2Bins8`** (8×1)
- **▸ `customIY3Bins8`** (8×1)
- **▸ `customIYBins8`** (8×1)

### Math / logic  (1)

- **▸ `userFunctions`** (380×1)

## Outputs  ·  61


### Electrical / cooling aux  (24)

- **▸ `altCtrlTargetVoltage`** (8×8)
- **▸ `ewpTable`** (6×1)
- **▸ `ewpTableBin`** (6×1)
- `altCtrlBaseDC`, `altCtrlDCOutputMax`, `altCtrlDCOutputMin`, `altCtrlEnable`, `altCtrlIntegralLimitMax`, `altCtrlIntegralLimitMin`, `altCtrlInvert`, `altCtrlKD`, `altCtrlKI`, `altCtrlKP`, `altCtrlOutputMax`, `altCtrlOutputMin`, `ewpCLTPoint1`, `ewpCLTPoint1OffTime`, `ewpCLTPoint1OnTime`, `ewpCLTPoint1PWMDC`, `ewpCLTPoint2`, `ewpCLTPoint2OffTime`, `ewpCLTPoint2OnTime`, `ewpCLTPoint2PWMDC`, `ewpEnable`

### PWM tables  (21)

- **▸ `pwm2XAxis`** (8×1)
- **▸ `pwm2YAxis`** (8×1)
- **▸ `pwmTable`** (8×8)
- **▸ `pwmTable2`** (8×8)
- **▸ `pwmXAxis`** (8×1)
- **▸ `pwmYAxis`** (8×1)
- `pwm1Function`, `pwm2Function`, `pwm2TableDCWhenInactive`, `pwm2TableDisableOutputIfNoRPM`, `pwm2TableFrequency`, `pwm2TableOutput`, `pwm2TableXAxisType`, `pwm2TableYAxisType`, `pwmMinDCWhenACActive`, `pwmTableDCWhenInactive`, `pwmTableDisableOutputIfNoRPM`, `pwmTableFrequency`, `pwmTableOutput`, `pwmTableXAxisType`, `pwmTableYAxisType`

### GP / aux outputs  (16)

- **▸ `freqCustomXAxis`** (8×1)
- **▸ `frequencyOutputTbl`** (8×1)
- `buzzerFunction`, `dtoEnable`, `dtoMinTime`, `dtoTurnOffCondition`, `enableBuzzerOnMkPerm`, `enableBuzzerOnStartup`, `freqOutput`, `freqTableAxis`, `mainRelayControlOutput`, `mainRelayInvertOutput`, `shiftLightHysteresis`, `shiftLightInvertOutput`, `shiftLightOutput`, `tachoOutput`

## Boost  ·  131


### Boost target / control  (61)

- **▸ `boostCLTCorr`** (5×1)
- **▸ `boostCLTLimit`** (5×1)
- **▸ `boostDCCCBins`** (8×1)
- **▸ `boostDCCorrection`** (8×1)
- **▸ `boostEGTBins`** (6×1)
- **▸ `boostEGTCorrection`** (6×1)
- **▸ `boostEGTLimit`** (6×1)
- **▸ `boostEthanoCorr`** (9×1)
- **▸ `boostIATCorr`** (5×1)
- **▸ `boostIATLimit`** (5×1)
- **▸ `boostRotaryBlend`** (10×1)
- **▸ `boostTarget1`** (8×8)
- **▸ `boostTarget2`** (8×8)
- **▸ `boostVSSBins`** (6×1)
- **▸ `boostVSSCorrection`** (6×1)
- **▸ `boostVSSLimit`** (6×1)
- **▸ `dbwBoostTargetLimit`** (6×1)
- **▸ `dbwBoostTargetLimitBin`** (6×1)
- **▸ `dcBoostRef1`** (8×8)
- **▸ `lcBoostTarget`** (10×1)
- **▸ `lcDBWBoostBins`** (4×1)
- **▸ `ralBoostTarget`** (6×1)
- **▸ `rpmBoostBins`** (8×1)
- **▸ `targetMapBoostBins`** (8×1)
- **▸ `timerBoostCorrection`** (10×1)
- `boostBlendTargetSource`, `boostControlType`, `boostCorrTimer`, `boostCutEnable`, `boostCutOverboostCutTime`, `boostCutOverboostDuration`, `boostCutOverboostLimit`, `boostDCBelowMargin`, `boostDCCCXAxis`, `boostDisableSolenoidUnderMap`, `boostDisiableSolenoidFunc`, `boostIntegralLimitMax`, `boostIntegralLimitMaxRate`, `boostIntegralLimitMin`, `boostInvertOutput`, `boostKD`, `boostKI`, `boostKP`, `boostMinRPM`, `boostOverrideDC`, `boostOverridenDC`, `boostPressureFilter`, `boostResetPIDOutOfMargin`, `boostResponseDelay`, `boostSource`, `boostSwitch`, `boostSwitchMode`, `boostUseUndrivenSpeedAsVss`, `boostValveFrequency`, `boostValveMaxDC`, `boostValveMinDC`, `boostXAxis`, `lcBoostTargetSelector`, `lcPrestageBoostTarget`, `machZBoostOnDashUnit`, `ralOverrideBoost`

### Anti-lag (ALS)  (34)

- **▸ `alsBoostBins`** (4×1)
- **▸ `alsCut`** (4×6)
- **▸ `alsCut2`** (4×6)
- **▸ `alsDBWTarget`** (6×4)
- **▸ `alsDBWTarget2`** (6×4)
- **▸ `alsFuelCorr`** (6×1)
- **▸ `alsFuelCorr2`** (6×1)
- **▸ `alsIgnAngle`** (4×6)
- **▸ `alsIgnAngle2`** (4×6)
- **▸ `alsRPMBins`** (6×1)
- **▸ `alsTPSBins`** (4×1)
- `alsActivationInput`, `alsActivationPPS`, `alsActuatorOuptut`, `alsActuatorType`, `alsArmingPPS`, `alsArmingRPM`, `alsBostTarget`, `alsCutType`, `alsDeactivationPPSHyst`, `alsExitCutPercent`, `alsExitCutRestoreRate`, `alsExitIgnAngle`, `alsExitIgnRestoreRate`, `alsIgnAngleMode`, `alsMaxCLT`, `alsMaxDurationTime`, `alsMaxEGT`, `alsMinCLT`, `alsMinRPM`, `alsMinVSS`, `alsOverrideBostTarget`, `alsTblSwitch`, `alsUsePPSAsXAxis`

### Wastegate  (29)

- **▸ `ewgFeedForwardDC`** (5×5)
- **▸ `ewgTargetBins5`** (5×1)
- `ewgCANControlID`, `ewgControlFrequency`, `ewgEnableControl`, `ewgFeedbackInput`, `ewgInputMain`, `ewgIntegralLimitMax`, `ewgIntegralLimitMin`, `ewgInvertInput`, `ewgKD`, `ewgKI`, `ewgKP`, `ewgMainFailSafeMax`, `ewgMainFailSafeMin`, `ewgMax`, `ewgMin`, `ewgOutput`, `ewgOverrideDC`, `ewgOverrideTarget`, `ewgOverridenDC`, `ewgOverridenTarget`, `ewgType`, `turboShaftNumBlades`, `turboShaftSensorDivider`, `turboShaftSensorInput`, `turboShaftSensorSignalEdge`, `wastegateDomePressureFailSafe`, `wastegateDomePressureInput`

### Boost PID / margin  (7)

- `boostMarginAboveTarget`, `boostMarginBelowTarget`, `boostMarginHysteresis`, `boostOutput`, `boostOutputMax`, `boostOutputMin`, `boostPIDEnable`

## DBW  ·  55


### DBW motor / limits  (14)

- **▸ `dbwCLTLimitBins`** (5×1)
- **▸ `dbwCLTLimitTable`** (5×1)
- **▸ `dbwMAPBins`** (8×1)
- **▸ `dbwPPSBins`** (10×1)
- **▸ `dbwRPMBins`** (8×1)
- **▸ `frictionCharacteristic`** (3×1)
- **▸ `frictionCharacteristicBin`** (3×1)
- **▸ `pitLimiterDBWLimit`** (10×1)
- **▸ `springDCBin`** (5×1)
- **▸ `springDCRef`** (5×1)
- `dbwMaxCurrent`, `dbwMaxDC`, `dbwMinDC`, `dbwPIDTuning`

### DBW characteristic  (3)

- **▸ `dbwCharacteristic1`** (10×8)
- **▸ `dbwCharacteristic2`** (10×8)
- `dbwCharacteristicSwitchType`

### DBW misc  (38)

- **▸ `ccThrottleTarget`** (8×6)
- **▸ `dbwRotaryBlend`** (10×1)
- **▸ `dbwSpeedClosingScale`** (8×1)
- `FlatShiftThrottlePos`, `dbwBMWITBOutput`, `dbwBlendCharactSrc`, `dbwCANControlID`, `dbwCANTimeout`, `dbwDeadband`, `dbwDisableIfNoRPM`, `dbwDisableOutputFn`, `dbwFreqency`, `dbwIntegratorResetThreshold`, `dbwInvertMotor`, `dbwLimpPosVoltage`, `dbwMode`, `dbwMovementTest`, `dbwOverLimpFrictionFactor`, `dbwOverLimpkD`, `dbwOverLimpkI`, `dbwOverLimpkP`, `dbwOverrideDC`, `dbwOverrideTarget`, `dbwOverridedDC`, `dbwOverridedTarget`, `dbwSwtichInput`, `dbwThrottleSpeedLimit`, `dbwUnderLimpFrictionFactor`, `dbwUnderLimpkD`, `dbwUnderLimpkI`, `dbwUnderLimpkP`, `dbwUseMAPAsYAxis`, `lcThrottleSpeedLimit`, `nitrousS1ThrottleReleasedBehaviour`, `nitrousS2ThrottleReleasedBehaviour`, `revLimit1MinThrottlePos`, `revLimit2MinThrottlePos`, `revMatchThrottleBlipRefLvl`

## Traction control  ·  44


### Traction control  (44)

- **▸ `binSpeedTCDiff`** (7×1)
- **▸ `binSpeedTCPerc`** (10×1)
- **▸ `binTCTrqRed`** (10×1)
- **▸ `dsgTorqueReductionIgn`** (5×4)
- **▸ `tcAdjPosPercent`** (10×1)
- **▸ `tcAdjustBins`** (10×1)
- **▸ `tcMaxDiffSlip`** (7×7)
- **▸ `tcMaxPercSlip`** (7×10)
- **▸ `tcTRCut`** (10×1)
- **▸ `tcTorqReductionTbl`** (8×8)
- **▸ `tcUserSlipDiff`** (10×1)
- **▸ `tcUserSlipPerc`** (10×1)
- **▸ `tcUserTorqRedScle`** (10×1)
- **▸ `tcdRPM`** (8×1)
- **▸ `tckDDiff`** (8×1)
- **▸ `tckDPerc`** (8×1)
- **▸ `tckIDiff`** (8×1)
- **▸ `tckIPerc`** (8×1)
- **▸ `tckPDiff`** (8×1)
- **▸ `tckPDiffTpsScale`** (7×1)
- **▸ `tckPPerc`** (8×1)
- **▸ `tckPPercTpsScale`** (7×1)
- **▸ `torqueReductionLoadBin`** (4×1)
- **▸ `torqueReductionRequestBin`** (5×1)
- **▸ `upshiftTorqueReduction`** (8×4)
- `dsgTrqRedMaxIgnReatrd`, `pitLimitTorqueReductionMode`, `tcActivateTCOutputWhenTCDisabled`, `tcActivationSwitch`, `tcActiveOutput`, `tcCutType`, `tcDecayRate`, `tcDiffModeSpeed`, `tcDisableAdjPotPos`, `tcEnable`, `tcIntegralLimitMax`, `tcIntegralLimitMin`, `tcInvertTCActiveOutput`, `tcMinRPM`, `tcMinSpeed`, `tcPidIntegralResetMinus`, `tcTorqueScaleSource`, `tcType`, `tcUserScaleSource`

## VVT  ·  88


### VVT / cam  (88)

- **▸ `cam1AdvTbl`** (10×10)
- **▸ `cam1AdvTblB`** (10×10)
- **▸ `cam2AdvTbl`** (10×10)
- **▸ `cam2AdvTblB`** (10×10)
- **▸ `vvtiMapBins10`** (10×1)
- **▸ `vvtiRpmBins10`** (10×1)
- **▸ `vvtiRpmBins10_2`** (10×1)
- **▸ `vvtiTPSBins10`** (10×1)
- `cam2Edge`, `cam2InputFilter`, `cam2Pattern`, `camLongerFactor`, `camShorterFactor`, `vtecInvertOutput`, `vtecMAPHist1`, `vtecMAPHist2`, `vtecMAPMax1`, `vtecMAPMax2`, `vtecMAPMin1`, `vtecMAPMin2`, `vtecOffDelay`, `vtecOutput`, `vtecRPMAboveVTECAlwaysOn`, `vtecRPMHist1`, `vtecRPMHist2`, `vtecRPMMax1`, `vtecRPMMax2`, `vtecRPMMin1`, `vtecRPMMin2`, `vtecTPSHist1`, `vtecTPSHist2`, `vtecTPSMax1`, `vtecTPSMax2`, `vtecTPSMin1`, `vtecTPSMin2`, `vtecVSSHist1`, `vtecVSSHist2`, `vtecVSSMin1`, `vtecVSSMin2`, `vvt1MaxDC`, `vvt1MinDC`, `vvt2MaxDC`, `vvt2MinDC`, `vvtCAM1CtrlDelay`, `vvtCAM2CtrlDelay`, `vvtCam1ControlType`, `vvtCam1DCOverridedDC`, `vvtCam1DCOverridedTarget`, `vvtCam1Deadband`, `vvtCam1IntegralLimitMax`, `vvtCam1IntegralLimitMin`, `vvtCam1InvertOutput`, `vvtCam1KD`, `vvtCam1KI`, `vvtCam1KP`, `vvtCam1MaxAdvance`, `vvtCam1MinRPM`, `vvtCam1Output1`, `vvtCam1Output2`, `vvtCam1OutputFrequency`, `vvtCam1OutputMax`, `vvtCam1Override`, `vvtCam1OverrideTarget`, `vvtCam1SteadyPosDC`, `vvtCam1direction`, `vvtCam1tOutputMin`, `vvtCam2ControlType`, `vvtCam2DCOverridedDC`, `vvtCam2DCOverridedTarget`, `vvtCam2Deadband`, `vvtCam2IntegralLimitMax`, `vvtCam2IntegralLimitMin`, `vvtCam2InvertOutput`, `vvtCam2KD`, `vvtCam2KI`, `vvtCam2KP`, `vvtCam2MaxAdvance`, `vvtCam2MinRPM`, `vvtCam2Output1`, `vvtCam2Output2`, `vvtCam2OutputFrequency`, `vvtCam2OutputMax`, `vvtCam2Override`, `vvtCam2OverrideTarget`, `vvtCam2SteadyPosDC`, `vvtCam2direction`, `vvtCam2tOutputMin`, `vvtiUseTableFromCAM1`

## Sport  ·  148


### Sequential / flat-shift  (95)

- **▸ `downshiftBlipLevel`** (8×3)
- **▸ `downshiftBlipRPMBin`** (3×1)
- **▸ `downshiftTimeout`** (8×1)
- **▸ `psDownShiftLimits`** (7×1)
- **▸ `psDownShiftPreload`** (7×1)
- **▸ `psDownShiftTimeout`** (7×1)
- **▸ `psLoad`** (3×1)
- **▸ `psPower`** (6×1)
- **▸ `psUpShiftPreload`** (7×3)
- **▸ `psUpShiftTimeout`** (7×1)
- **▸ `psVSSBins`** (6×1)
- **▸ `upshiftRecoveryTime`** (8×1)
- **▸ `upshiftTimeout`** (8×1)
- **▸ `upshiftTorqRedMAPBins`** (4×1)
- `co2Deadband`, `co2Frequency`, `co2IntegralLimitMax`, `co2IntegralLimitMin`, `co2KD`, `co2KI`, `co2KP`, `co2MaxDC`, `co2MinDC`, `co2OverrideDC`, `co2OverridenDC`, `co2PIDOutputMax`, `co2PIDOutputMin`, `co2PressureSrcOutput`, `co2VentSrcOutput`, `csbPaddleShiftIn1`, `csbPaddleShiftIn2`, `downshiftPostshiftCutMinRPM`, `downshiftPostshiftCutPercent`, `downshiftPostshiftCutType`, `downshiftPostshiftRecoveryCutTime`, `downshiftPostshiftRecoveryTime`, `dsgEnablePaddleShift`, `dsgRevMatchMinDBWPos`, `dsgUpshiftTqRedStrategy`, `flatShiftControlRange`, `flatShiftCutOffRPM`, `flatShiftCutPercent`, `flatShiftCutType`, `flatShiftDeactivationDelay`, `flatShiftFuelCorrection`, `flatShiftIgnRetard`, `flatShiftInput`, `flatShiftTPSLimit`, `flatShiftVssLimit`, `loadCellInvertVoltage`, `loadCellShiftDownActivation`, `loadCellShiftUpActivation`, `loadCellSwitchDown`, `loadCellSwitchUp`, `paddleShiftDebounceTime`, `paddleShiftDownInput`, `paddleShiftNInput`, `paddleShiftRInput`, `paddleShiftUpInput`, `psDownActuatorOutput`, `psEnable`, `psFirstMaxRPM`, `psFirstPulseTime`, `psFirstRejectClutchIfInactive`, `psFirstRequestMode`, `psMinRPMForUpshift`, `psNeutralMaxRPM`, `psNeutralNumPulses`, `psNeutralPulseOffTime`, `psNeutralPulseStartTime`, `psNeutralPulseStep`, `psNeutralPulseTime`, `psNeutralRejectClutchIfInactive`, `psNeutralRequestMode`, `psNeutralShiftMethod`, `psOutputType`, `psPreloadYAxis`, `psReverseMaxRPM`, `psReversePulseTime`, `psReverseRejectClutchIfInactive`, `psReverseRequestMode`, `psSwitchesHoldTime`, `psType`, `psUpActuatorOutput`, `psXAPHighPower`, `revMatchDelayToActivate`, `revMatchDelayToDeactivate`, `revMatchEnableInput`, `revMatchFuelCorrection`, `revMatchMaxBlipDuration`, `revMatchMaxIgnRetard`, `revMatchMaxRPM`, `revMatchMinVSS`, `revMatchTargetRPM`, `revMatchType`

### Launch control  (25)

- **▸ `lcDBWTargetRPMBins`** (5×1)
- **▸ `lcDBWTargetTable`** (5×4)
- **▸ `lcFuelEnrichment`** (5×1)
- **▸ `lcRPMTarget`** (10×1)
- `lcActivateOverPPS`, `lcActivateUnderPPS`, `lcActivationDelay`, `lcActivationInput`, `lcCutType`, `lcDeactivationDelay`, `lcExitIgnRestoreRate`, `lcMaxCLT`, `lcMaxEGT`, `lcMaxVSS`, `lcMinCLT`, `lcPrestageCylCut`, `lcPrestageDBWTarget`, `lcPrestageEnable`, `lcPrestageFuelEnrich`, `lcPrestageIgnAngle`, `lcPrestageRPM`, `lcPrestageTimeout`, `lcRPMActivationDelta`, `lcRPMTargetSelector`, `lcUseClutchSwitchToDeactivate`

### Pit limiter  (10)

- **▸ `pitLimitError`** (8×1)
- **▸ `pitLimitTorqReduction`** (8×1)
- **▸ `pitLimiterSpeedTarget`** (10×1)
- `pitLimitEnabled`, `pitLimitInput`, `pitLimitMaxSpeed`, `pitLimitMinSpeed`, `pitLimitRestoreRate`, `pitLimitRotary0DisableLimiter`, `pitLimiterOverrideDBW`

### Rolling launch  (10)

- **▸ `ralDBWTarget`** (6×1)
- **▸ `ralFuelCorr`** (6×1)
- **▸ `ralVSSBins`** (6×1)
- `ralCutType`, `ralInput`, `ralMaxEGT`, `ralMinCLT`, `ralMinVSS`, `ralOverrideDBW`, `ralRestoreIgnRate`

### Trans-brake / line-lock  (7)

- `tBrakeActivationSwitch`, `tBrakeBumpbutton`, `tBrakeBumptime`, `tBrakeCreepDC`, `tBrakeCreepFrequency`, `tBrakeCreepbutton`, `tBrakeOutput`

### Drag race  (1)

- `dragRaceTimerActSwitch`

## Nitrous  ·  49


### Nitrous  (49)

- **▸ `nitrousS1DC`** (6×1)
- **▸ `nitrousS1Fuel`** (6×1)
- **▸ `nitrousS1TimeXaxis`** (6×1)
- **▸ `nitrousS1Xaxis`** (6×1)
- **▸ `nitrousS2DC`** (6×1)
- **▸ `nitrousS2Fuel`** (6×1)
- **▸ `nitrousS2TimeXaxis`** (6×1)
- **▸ `nitrousS2Xaxis`** (6×1)
- `nitrousActivationFn`, `nitrousLambdaTarget`, `nitrousS1Activation`, `nitrousS1ActivationFn`, `nitrousS1Delay`, `nitrousS1Frequency`, `nitrousS1FuelOffDelay`, `nitrousS1FuelOnDelay`, `nitrousS1IgntionDelay`, `nitrousS1LCActive`, `nitrousS1LCMaxDuration`, `nitrousS1MaxActiveTime`, `nitrousS1MaxDC`, `nitrousS1MaxMAP`, `nitrousS1MinDC`, `nitrousS1MinMAP`, `nitrousS1MinRPM`, `nitrousS1MinTPS`, `nitrousS1MinVSS`, `nitrousS1Output`, `nitrousS1TotalHP`, `nitrousS1Type`, `nitrousS2Activation`, `nitrousS2ActivationFn`, `nitrousS2Delay`, `nitrousS2Frequency`, `nitrousS2FuelOffDelay`, `nitrousS2FuelOnDelay`, `nitrousS2IgntionDelay`, `nitrousS2MaxActiveTime`, `nitrousS2MaxDC`, `nitrousS2MaxMAP`, `nitrousS2MinDC`, `nitrousS2MinMAP`, `nitrousS2MinRPM`, `nitrousS2MinTPS`, `nitrousS2MinVSS`, `nitrousS2Output`, `nitrousS2TotalHP`, `nitrousS2Type`, `nitrousToFuelRatio`

## Tables switching  ·  27


### Table-set / flex blend selectors  (15)

- **▸ `tblsFFASEBlend`** (9×1)
- **▸ `tblsFFCrankingBlend`** (9×1)
- **▸ `tblsFFIgnBlend`** (9×1)
- **▸ `tblsFFLambdaBlend`** (9×1)
- **▸ `tblsFFWarmupBlend`** (9×1)
- **▸ `tblsVEBlend`** (9×1)
- `tblsASE`, `tblsCAM1`, `tblsCAM2`, `tblsCranking`, `tblsIGN`, `tblsLambda`, `tblsOverrun`, `tblsVE`, `tblsWarmup`

### Flex fuel blend  (12)

- **▸ `boostEthanoLimit`** (9×1)
- **▸ `boostEthanolBlend`** (9×1)
- **▸ `ethanol10Bins`** (11×1)
- **▸ `ethanolFuelScale`** (11×1)
- **▸ `flexFuelEthanolContentBins`** (9×1)
- **▸ `flexFuelSensorBins`** (6×1)
- **▸ `flexFuelSensorCal`** (6×1)
- `ethanolContentPercent`, `ffEnableCustomCal`, `ffEnableFFSensor`, `ffEthanolContentIfError`, `ffMaxTPS`

## Engine protection  ·  44


### Rev limiter  (21)

- **▸ `revLimiterCLTTarget`** (5×1)
- **▸ `revLimiterCLTTargetBins`** (5×1)
- **▸ `revLimiterCustomTarget`** (10×1)
- **▸ `revLimiterEthTarget`** (4×1)
- **▸ `revLimiterEthTargetBins`** (4×1)
- **▸ `revLimiterIATTarget`** (4×1)
- **▸ `revLimiterIATTargetBins`** (4×1)
- **▸ `revLimiterOILTarget`** (5×1)
- **▸ `revLimiterOILTargetBins`** (5×1)
- `customRevLimitInput`, `revLimit1ControlRange`, `revLimit1CutPercent`, `revLimit1CutType`, `revLimit1IgnRetard`, `revLimit2ControlRange`, `revLimit2CutPercent`, `revLimit2CutType`, `revLimit2IgnRetard`, `revLimitCanBusControlCondition`, `revLimitersSwitchInputs`, `rpmLimit`

### Protection / fault reporting  (19)

- `acEvapTempFailSafe`, `acPressureFailSafe`, `checkEngineLightInvOutput`, `checkEngineLightOutput`, `cylHeadTempFailSafe`, `ewpFailSafeDC`, `failReportCLT`, `failReportDBW`, `failReportEGT1`, `failReportEGT2`, `failReportEGTAlarm`, `failReportFFSensor`, `failReportFPR`, `failReportIAT`, `failReportMAP`, `failReportWBO`, `failSafeCLTValue`, `failSafeIATValue`, `failSafeMAPValue`

### Stuck-throttle  (4)

- `stBrakeTimeout`, `stEnable`, `stMinRPM`, `stTPSLevel`

## Timers  ·  6


### Timers  (6)

- **▸ `timer1Bins`** (10×1)
- **▸ `timer2Bins`** (10×1)
- **▸ `timer3Bins`** (10×1)
- **▸ `timerFuelCorrection`** (10×1)
- **▸ `timerIgnCorrection`** (10×1)
- `customTimerCorrectionModify`

## DSG Gearbox  ·  41


### DSG / transmission  (41)

- **▸ `dsgBlipLevel`** (5×6)
- **▸ `dsgBlipRPMError`** (5×1)
- **▸ `dsgBlipRPMTarget`** (5×1)
- **▸ `dsgCombinedLoad`** (8×5)
- **▸ `dsgCombinedLoadBin`** (16×1)
- **▸ `dsgCombinedLoadMAPBin5`** (5×1)
- **▸ `dsgCombinedLoadTPSBin8`** (8×1)
- **▸ `dsgCutReduction`** (5×4)
- **▸ `dsgPostBlipLevel`** (5×1)
- **▸ `dsgTorqueLosses`** (4×5)
- **▸ `dsgTorqueLossesCLTBins`** (4×1)
- **▸ `dsgTorqueLossesRPMBins`** (5×1)
- `dsgAutoNmodeEnable`, `dsgBlipFuelEnrichment`, `dsgBlipMaxIgnRetard`, `dsgBlipTime`, `dsgCCCanVer`, `dsgCCMotCode`, `dsgEmulationABSESP`, `dsgEmulationAirbag`, `dsgEmulationDisableABS2`, `dsgEmulationEPS`, `dsgEmulationGateway`, `dsgEnable`, `dsgEnableSelectorEmulation`, `dsgFuelEnrichSusatainRate`, `dsgFuelEnrichment`, `dsgIdleTargetCreepIncrease`, `dsgIdleTargetCreepMaxTarget`, `dsgKickdownEnable`, `dsgKickdownLimit`, `dsgMDNorm`, `dsgMaxEngineTorque`, `dsgNumCutIgnEvents`, `dsgPsDownInput`, `dsgPsUpInput`, `dsgReverseOutput`, `dsgSelectorRotary`, `dsgSportCutMinRPM`, `dsgSportCutMinTPS`, `dsgUseCombinedLoad`

## Other  ·  43


### Engine / base setup  (18)

- **▸ `engineTorqueNm`** (16×12)
- `engineDisplacement`, `firingOrder1`, `firingOrder2`, `firingOrder3`, `firingOrder4`, `firingOrder5`, `firingOrder6`, `firingOrder7`, `firingOrder8`, `initMask`, `maxEngineTrqNmINV`, `maxVeRpm`, `numCylinders`, `rpmMultiplier`, `rpmMultiplier2`, `rpmMultiplierSwitch`, `toBeRemoved`

### Checksums  (2)

- `tablesChecksum`, `variablesChecksum`

### Base config / misc  (13)

- **▸ `autotuneDirtyFlags`** (40×1)
- **▸ `commentData`** (64×1)
- `calToolState`, `debugSwitch1`, `debugSwitch2`, `debugValue1`, `debugValue2`, `enableDBWCANControl`, `enableEGTCorrection`, `enableLogWhenProtected`, `leaverType`, `pidDebug`, `useEGT1asCLT`

### Shared axis bins  (10)

- **▸ `airflowBins4`** (4×1)
- **▸ `airflowBins5`** (5×1)
- **▸ `mapBins`** (16×1)
- **▸ `mapBins8`** (12×1)
- **▸ `mapBins8B`** (8×1)
- **▸ `rpmBins`** (20×1)
- **▸ `rpmBins10`** (10×1)
- **▸ `rpmBins2`** (20×1)
- **▸ `rpmBins8`** (12×1)
- **▸ `rpmBins8B`** (8×1)

## CAN, Serial  ·  144


### Switch panels / keypads (CAN)  (112)

- `csbEnable`, `csbEnableAin1`, `csbEnableAin2`, `csbEnableAinX1`, `csbEnableAinX2`, `csbEnableAinX3`, `csbEnableAinX4`, `csbEnableAinX5`, `csbEnableAinX6`, `csbEnableAinX7`, `csbEnableAinX8`, `csbEnableDebounce`, `csbEnableRSCAN1`, `csbEnableRSCAN2`, `csbEnableRSCAN3`, `csbEnableRSCAN4`, `csbOutput1Control`, `csbOutput2Control`, `csbOutput3Control`, `csbOutput4Control`, `csbSW1Led`, `csbSW1Type`, `csbSW2Led`, `csbSW2Type`, `csbSW3Led`, `csbSW3Type`, `csbSW4Led`, `csbSW4Type`, `csbSW5Led`, `csbSW5Type`, `csbSW6Led`, `csbSW6Type`, `csbSW7Led`, `csbSW7Type`, `csbSW8Led`, `csbSW8Type`, `csbType`, `keypadBacklightColor`, `keypadBrightnessSwitch`, `pmuAnalogImport`, `pmuKey1`, `pmuKey10`, `pmuKey11`, `pmuKey12`, `pmuKey2`, `pmuKey3`, `pmuKey4`, `pmuKey5`, `pmuKey6`, `pmuKey7`, `pmuKey8`, `pmuKey9`, `pmuKeyboardEnable`, `scbSW1Id`, `scbSW2Id`, `scbSW3Id`, `scbSW4Id`, `scbSW5Id`, `scbSW6Id`, `scbSW7Id`, `scbSW8Id`, `spBacklight`, `spBacklight2`, `spEnable`, `spEnableOpenCeremony`, `spKey10DefState`, `spKey10Id`, `spKey10Type`, `spKey11DefState`, `spKey11Id`, `spKey11Type`, `spKey12DefState`, `spKey12Id`, `spKey12Type`, `spKey13DefState`, `spKey13Id`, `spKey13Type`, `spKey14DefState`, `spKey14Id`, `spKey14Type`, `spKey15DefState`, `spKey15Id`, `spKey15Type`, `spKey1DefState`, `spKey1Id`, `spKey1Type`, `spKey2DefState`, `spKey2Id`, `spKey2Type`, `spKey3DefState`, `spKey3Id`, `spKey3Type`, `spKey4DefState`, `spKey4Id`, `spKey4Type`, `spKey5DefState`, `spKey5Id`, `spKey5Type`, `spKey6DefState`, `spKey6Id`, `spKey6Type`, `spKey7DefState`, `spKey7Id`, `spKey7Type`, `spKey8DefState`, `spKey8Id`, `spKey8Type`, `spKey9DefState`, `spKey9Id`, `spKey9Type`, `spKeyBright`, `spKeypadType`

### CAN / dash / OEM integration  (32)

- **▸ `userCANStream`** (315×1)
- `canBoschABS`, `canBusDashType`, `canBusSendEMUDataOverCAN`, `canBusSpeed`, `canBusTerminator`, `canFrame600`, `canLotusEliseSportMode`, `canLotusExigeSportRotary`, `canOBD2Support`, `canRX8ABSModel`, `emuClassicSerialCompatibility`, `espEmulationEnable`, `evoXICSprayIdnicator`, `extPortDeviceID`, `fiat500Version`, `fordFocusType`, `hondaS2000DashClt`, `hondaS2000DashCltOutput`, `machZType`, `mavericProductionYear`, `mqbEnableRPMSignal`, `rx8EmulatePowerSteering`, `rzr4WDSwitch`, `rzrFrontDiffLock`, `rzrModeInput`, `sendClio3ImmoMessage`, `sendEcumasterDataToBTModule`, `sendExigeStreamWhenVW`, `steeringWheelSensorOffset`, `vwCANVersion`, `vwEngineCode`

## Log  ·  12


### Logging / virtual dyno  (12)

- `dynoCarMass`, `dynoCoefOfDrag`, `dynoDriveTrainEff`, `dynoFrontalArea`, `dynoMaxRPM`, `dynoMinRPM`, `dynoShowIAT`, `dynoShowMixture`, `dynoShowPressure`, `dynoVSSAt3000`, `dynoVSSType`, `loggingLevel`

## Gauges  ·  0

