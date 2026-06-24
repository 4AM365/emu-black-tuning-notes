# Sport — settings reference

> **Software page:** *Sport*. Full symbol catalog: [tune_feature_tree.md → Sport](tune_feature_tree.md).

Motorsport features: launch control, rolling launch, pit limiter, flat-shift / sequential / paddle-shift control, trans-brake, and drag-race timing. Mostly unused on this build.

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Sequential / flat-shift** (95) — `downshiftBlipLevel`, `downshiftBlipRPMBin`, `downshiftTimeout`, `psDownShiftLimits`, `psDownShiftPreload` …
- **Launch control** (25) — `lcDBWTargetRPMBins`, `lcDBWTargetTable`, `lcFuelEnrichment`, `lcRPMTarget`, `lcActivateOverPPS` …
- **Pit limiter** (10) — `pitLimitError`, `pitLimitTorqReduction`, `pitLimiterSpeedTarget`, `pitLimitEnabled`, `pitLimitInput` …
- **Rolling launch** (10) — `ralDBWTarget`, `ralFuelCorr`, `ralVSSBins`, `ralCutType`, `ralInput` …
- **Trans-brake / line-lock** (7) — `tBrakeActivationSwitch`, `tBrakeBumpbutton`, `tBrakeBumptime`, `tBrakeCreepDC`, `tBrakeCreepFrequency` …
- **Drag race** (1) — `dragRaceTimerActSwitch`

## Launch control / "2-step" — how it works (and the V2 vs V3 symbol split)

The EMU Black "2-step" is the **Launch control** strategy (Sport → Launch ctrl.). It is a
second, lower rev limiter that holds engine RPM while the car is stationary so you can build
boost against the converter/clutch, then releases to full power on launch. It holds RPM by
**cutting ignition (or fuel) and optionally retarding timing** in a soft→hard band.

**Activation gating** (ALL must be true to engage):
1. **Activation input** active — `lcInput` (the boolean source selected in EMU). `0` = not used.
   A non-zero value means LC is gated on an assigned switch/CAN-switch. There is **no separate
   `lcEnable`** — assigning the activation input is what turns the feature on.
2. **VSS ≤ `lcVssLimit`** (km/h) — must be ~stationary. This is what *releases* the limiter on
   launch (VSS climbs past the limit → LC exits → full power).
3. **TPS ≥ `lcActivationTPS`** (%) — throttle threshold to arm.
4. RPM rises into the band: soft cut begins at **`lcActivationRPM`** (the launch RPM you hold),
   hard cut at **`lcHardCutRPM`**. `lcCutType` 0 = spark cut. `lcTimeToActivate` = arm delay.

**Two parameter sets** (`…1` / `…2`) selectable via `lcTableSwitch`; `lcIgnRestoreRate` /
`lcSparkRestoreRate` govern how smoothly torque comes back on exit. `LC state` and the
`FLAGS1` bit 2 (`LC`) in the EMU CAN stream report live state.

### V2 (firmware ~2.x) vs V3 symbol families — they are different
- **V2 (e.g. project v2.175):** simple soft/hard limiter — `lcInput`, `lcActivationRPM{1,2}`,
  `lcHardCutRPM{1,2}`, `lcActivationTPS{1,2}`, `lcVssLimit{1,2}`, `lcCutType`, `lcTimeToActivate`,
  plus 7×7 `lcSparkCutTbl{1,2}` / `lcIgnRetardTbl{1,2}` / `lcFuelEnrichTbl{1,2}` / `lcWGOverrideTbl{1,2}`.
  **No prestage, no DBW target table.**
- **V3:** richer — `lcRPMTarget`, `lcDBWTargetTable`, `lcActivateOverPPS`, prestage, boost target, PID.
  The `notes/sport.md` sub-node list above is V3 names; do **not** expect them in a V2 tune.

### Intermittent 2-step — root-cause order (verify by logging `LC state` + each gate)
1. **Activation input flaky** (`lcInput`). The #1 cause. Read its *name* in EMU (Sport → Launch
   ctrl. → Activation input) — a bad switch/wire, or a **CAN switch** whose source device drops
   off the bus, makes the arm signal intermittent. If sourced from a CAN device, suspect bus
   health (baud/termination/errors).
2. **`lcVssLimit` too tight** (e.g. 1 km/h). VSS noise or the car rocking pushes VSS ≥ limit and
   drops LC out. Watch VSS at standstill; ~3–5 km/h gives margin and still releases on launch.
3. **TPS/RPM window** — if `lcActivationTPS` isn't consistently exceeded, or the soft→hard band is
   narrow, the hold feels inconsistent. The cut/retard tables only have authority in their
   populated cells.
4. **Clutch interlock** — if `clutchPedalInput` is assigned, a marginal clutch switch gates it too;
   if `0`, there is no clutch gate (arming is input+VSS+TPS+RPM only).

### Andrew's car (V1 `EMU_BLACK\andrew`, project v2.175) — as-found 2-step config
`lcInput=34` = **CAN switch #2** (confirmed in EMU). The 2-step is therefore armed by a *virtual*
CAN switch, which is OFF unless a bus device transmits its state. **As-found, nothing in the tune
drives CAN switch #2:** `userCANStream` is all-zero (no user-defined RX frame) and
`pmuKeyboardEnable=0`. So the arm bit is essentially unsourced — the most likely cause of the
intermittent/non-working launch. CAN switches are fed one of three ways: (a) ECUMaster **ECM switch
board / keyboard** predefined receiver (this is what the BTI gauge claims to *emulate* — but the
gauge manual only documents its 3 buttons for screen nav, so confirm it actually outputs a
switch-board key before relying on it); (b) a **User-defined CAN** RX frame with a bit mapped to
"CAN switch #2"; (c) not at all — **hardwire** a momentary to EMU Switch #1/#2/#3 (pins 10/23/36)
and point `lcInput` there, which removes the bus from a launch-critical trigger (recommended fix).
`lcTableSwitch=0` → set 1 active. Set 1: `lcActivationRPM1=4000`, `lcHardCutRPM1=5000`,
`lcActivationTPS1=40` (%), `lcVssLimit1=1` km/h (**very tight**), `lcTimeToActivate=0`, `lcCutType=0`
(spark). `clutchPedalInput=0` (no clutch gate). Ign-retard/spark-cut tables populated only in the
upper RPM/load band (`lcSparkCutTbl1` 0x5F=95% in high cells). CAN side matches the **BTI CAN gauge**
manual requirements: `extPortDeviceID=0` (CAN-Bus), `canBusSpeed=0` (1 Mbps), `canBusSendEMUDataOverCAN=1`,
`canBusTerminator=1`, base ID 0x600 — so EMU + gauge form a correctly terminated 2-node bus (EMU
terminator on, gauge jumper on = 120 Ω each end). The BTI gauge is a receive/display device (3 nav
buttons); it can emulate the "ECU switch board" to send button presses, so **if `lcInput=34` resolves
to a CAN switch, the gauge/CAN path is directly in the 2-step trigger chain.**
