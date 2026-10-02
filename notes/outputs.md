# Outputs — settings reference

> **Software page:** *Outputs*. Full symbol catalog: [tune_feature_tree.md → Outputs](tune_feature_tree.md).

Physical and logical output drivers — PWM tables, gauge/GP outputs (tacho, shift light, relays), and electrical/cooling aux (alternator, electric water pump).

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Electrical / cooling aux** (24) — `altCtrlTargetVoltage`, `ewpTable`, `ewpTableBin`, `altCtrlBaseDC`, `altCtrlDCOutputMax` …
- **PWM tables** (21) — `pwm2XAxis`, `pwm2YAxis`, `pwmTable`, `pwmTable2`, `pwmXAxis` …
- **GP / aux outputs** (16) — `freqCustomXAxis`, `frequencyOutputTbl`, `buzzerFunction`, `dtoEnable`, `dtoMinTime` …

## AC clutch — gating logic as observed in a log

Source: `fullchannels.csv` (Supra, 2026-09-19, 1943 s, 25 Hz), tune `Supra.xml.emub3` exported
2026-09-19 19:05 (the export immediately preceding the log). Channels: `Switch 1` = HVAC
compressor request (input selected by `acActivation`), `AC Clutch` = ECU output. Values below are
the readings from that export — re-read the XML before relying on them.

- **Clutch never engages without the request.** `AC Clutch`=1 with `Switch 1`=0 only for one
  40 ms sample at each request drop. Request off → clutch off within one sample: no off-delay.
- **RPM window = `acMinRPM` … `acMaxRPM`** (1800 / 5000 on that export). Min RPM with clutch on
  1801; every drop with the request still on straddles 1800 (prior sample ≥1803); drops at
  logged 5006/5009 rpm with TPS ≈56 (below `acMaxTPS`) then re-engage under 5000. **No
  hysteresis** on either edge — re-engagement starts the moment RPM is back inside the window.
- **`acTimeToEngage` is a delay from *gates satisfied*, not from the request edge.** All 43
  engagements came 0.88–0.92 s (22–23 samples) after RPM entered the window with the request
  on — the 900 ms setting — including one where the request had been on for 42 s. The timer
  restarts on every gate loss: no gate-true run shorter than 0.88 s ever engaged (36 such
  runs, longest 0.84 s), so a request that hovers around `acMinRPM` never gets a compressor.
- **Untested by this log:** `acMaxTPS` (TPS peaked 63.5 with request on), `acMaxCLT` (CLT ≤105),
  and pressure/evap limits — `acPressure`/`acEvapTemp` are set to none, `AC Pressure`,
  `AC EVAP temp.` and both status channels log flat 0, so those gates are inert.
- Consequence for idle: with `acMinRPM` above the idle target the compressor is never on during
  idle control, so `idleACRPMIncrease` (0) and any A/C idle-up are inert (see
  [idle.md](idle.md)). The HVAC side cycles the request on its own (evap thermostat), which is
  why `Switch 1` toggles every few seconds at cruise.
