# Supra sensor and switch inventory — inputs, supply, ground

Inventory 2026-09-28. Config from `EMU_BLACK_V3\Supra\Supra.xml.emub3` (09-22, newest XML).
Channel identities proved on `EMU_BLACK_V3\Supra\fullchannels.csv` (09-19 19:38, 48 064 samples
@ 25 Hz, all 564 channels) by correlation, not from index decoding alone. Re-read the symbols named
here before acting; assignments can change on any edit.

ECU is hardware rev F / CPU G, which is pre-"P" (see [my_car.md](my_car.md)). On that hardware the three built-in
switch inputs (black plug 10/23/36) accept **sensor ground only**. Anything else on one corrupts
the others (`docs/emu-black-help/Sensorsandinputs.md` :862, :1273). Ground theory: [notes/sensors_and_inputs.md → P6](../../notes/sensors_and_inputs.md).

## Input index decode (proved)

- 200-series pressure/temperature input indices = `CAN Analog (n − 199)`: `oilPressureInput` → `CAN Analog 5`
  (r 0.999), `backpressureInput` → `CAN Analog 6` (r 0.977 on pressurised samples),
  `prethrottleBoostInput` → `CAN Analog 4` (r −0.99, the negative r comes from the failsafe), `customTemperatureInput1` → `CAN Analog 3` (r −0.995).
- `fuelPressureInput` → ECU `Analog 5` (r 0.9996, [clt_signal_noise.md](clt_signal_noise.md) §6).
- Switch function inputs: `acActivation` → `Switch 1`, brake → `Switch 2`, `clutchPedalInput` →
  `Switch 3` (r 0.994) ([ac_request_input_noise.md](ac_request_input_noise.md) §1). Function channels
  have logic applied: `Brake pedal switch` = NOT(`Switch 2`) on 99.5 % of samples. That is
  configured inversion, not a fault.
- `TPS voltage` = ECU `Analog 2`. `PPS Voltage` matches no logged `Analog 1–6`; `ppsInputMain` pin unverified.
- ECU `Analog 1/3/4` rail at 4.96–4.98 V (pull-up, nothing connected); `Analog 6` reads 0.000 V (unused).
  The 09-19 "EMAP dead on Analog 6" call read this unused pin (corrected in
  [emap_map_ratio_cam_overlap.md](../../notes/emap_map_ratio_cam_overlap.md)).

## How status was judged

- **Drop to zero:** compare the step into zero against the fastest the physical quantity can move
  (and against the channel's own p99.9 sample-to-sample slew). A one-sample step far past that is a
  **step function → wiring/connection**. A zero reached at a physical rate, or a zero that is the
  quantity's true value (gauge pressure at atmosphere, engine off, standstill, below a speed sensor's
  floor), is normal.
- **Noise:** residual against a 1 s running median, in quanta `q` of the channel, plus the
  sign-reversal rate of sample-to-sample changes (white noise ≈ 0.67, a smooth signal ≪ 0.35).
  Oscillation around a clean mean is flagged.

## Inventory

| # | Sensor / switch | EMU input (log channel) | Sensor type | Supply | Ground | Status (09-19 log) |
|---|---|---|---|---|---|---|
| 1 | Crank position | Primary trigger | VR, 2-wire (`primTrigSensorType`) | none (self-generating) | SGND for VR−; shield to ground at one end | OK, synced |
| 2 | Intake cam / VVT-i | Secondary trigger = CAM1 | VR (`secTrigSensorType`) | none | SGND for VR−; shield at one end | OK |
| 3 | Turbo speed | CAM2 digital (`turboShaftSensorInput`) | active speed sensor, part unverified; `cam2SensorType` = VR mode | unverified (5 or 12 V per datasheet) | SGND recommended | **Noisy**: at steady RPM+MAP, 1 s CV 17 %, reversal 0.62. Zeros are low-speed floor (entry steps within normal slew), normal |
| 4 | Vehicle speed (R155) | VSS digital → `Driven axle input frequency` | Hall per `VSSSensorType`; part unverified | unverified (Hall needs 5 or 12 V) | SGND recommended | **Step functions → wiring.** 8 one-sample drops to 0 from 27–117 km/h (0.26 Hz/sample ≈ 1 g is the physical limit; these are 5–22 Hz), none near a live edit; one 270 Hz (≈1460 km/h) phantom held 0.56 s at t 1635.6. Drops below ~4 Hz (~22 km/h) are normal stop timeouts. Continuous signal is smooth (1.45 q, rev 0.25) |
| 5–6 | Knock ×2 | Knock 1 / Knock 2 (`ksInputCylinder*` alternate) | **Bosch donut** piezo, 2-wire, body isolated from the block (Will, 2026-09-28) | none | SGND + shield | OK (zeros only engine-off) |
| 7 | TPS (ES330 DBW TB) | `Analog 2` / `TPS voltage` | ratiometric 0–5 V; TPS2 track not assigned (`tpsInputCheck`) | 5 V | SGND | Borderline: 1.70 q, rev 0.59. The plate is servoed and moves, so part of this is real motion |
| 8 | PPS (GS430 pedal) | `PPS Voltage` | ratiometric 0–5 V; check track not assigned (`ppsInputCheck`) | 5 V | SGND | OK (1.22 q, rev 0.38, smooth) |
| 9 | MAP | internal (`useBuiltInMap`) | on-board, hose | internal | n/a | 1.33 q, rev 0.78; bursts ≥ 3 samples = aliased manifold pulsation (clt_signal_noise §6) |
| 10 | IAT | B32 / `IAT Voltage` | 2-wire NTC, internal 2K2 pull-up | 5 V (pull-up) | SGND, B29 per ECUMaster diagram | **Noisy** (1.74 q, rev 0.82). Was on block ground; **being rewired to SGND (Will, 2026-09-28)** |
| 11 | CLT | B5 / `CLT Voltage` | NTC, internal 2K2 pull-up | 5 V (pull-up) | SGND, B29 | **Noisy** (1.66 q, rev 0.70, p99.9 0.18 V). Was on block ground; **being rewired to SGND (Will, 2026-09-28)** |
| 12 | Fuel pressure | `Analog 5` | 3-wire 0.5–4.5 V | 5 V | SGND | OK (0.57 q). Zeros engine-off only |
| 13 | Oil pressure | `CAN Analog 5` (Switchboard) | 3-wire 0.5–4.5 V | 5 V (Switchboard) | Switchboard SGND (Will, 09-22) | **Noisy**: 2.83 q, rev 0.75, p99.9 0.39 V around a clean mean. Zeros engine-off only |
| 14 | Exhaust back pressure | `CAN Analog 6` | 3-wire 0.5–4.5 V | 5 V | Switchboard SGND | OK (0.12 q). Channel zeros are atmospheric gauge rounding, normal |
| 15 | Pre-throttle boost | `CAN Analog 4` | 3-wire 0.5–4.5 V | 5 V | Switchboard SGND | **Step → connection event.** Exactly 0.000 V from log start (incl. running) to t 602.36, then a one-sample step to 0.51 V with the **engine off**; clean after (0.25 q). No live edit at that instant (nearest `Data changing` 590.5 s) |
| 16 | Pre-IC temperature | `CAN Analog 3` | NTC | 5 V (pull-up) | Switchboard SGND | **Step at the same sample as #15:** 1.39 → 1.84 V in 40 ms, impossible for a thermistor. So something common to An3 and An4 (connector, 5 V or ground) changed at 602 s. Clean otherwise (0.14 q) |
| 17 | (unassigned) | `CAN Analog 2` | unidentified; 0.47 V idle → 0.78 V in boost, r 0.76 vs back pressure | ? | Switchboard SGND if a Switchboard sensor | clean, no function assigned |
| 18 | (unassigned) | `CAN Analog 1` | unidentified; 0.43–0.45 V near-flat | ? | ? | clean, no function assigned |
| 19 | Flex fuel (ethanol + fuel temp) | FF input (10k internal pull-up) | frequency + pulse-width | 12 V | general OK (digital edges) | OK |
| 20 | Wideband LSU 4.9 | internal controller (`oxygenSensorType`) | 5-wire planar | heater 12 V; cells on dedicated WBO pins | n/a (dedicated pins; heater low-side in EMU) | OK |
| 21–22 | EGT ×2 | built-in EGT 1 / EGT 2 | K-type thermocouple | none | n/a (differential) | OK (0.3–0.4 q) |
| 23 | A/C request | `Switch 1` | HVAC amplifier output; drive circuit unverified | from amplifier | **SGND only (pre-P)** | **Chatter cleared** by the 08-29 clutch-ground fix: 6.8 edges/min with the clutch pressed vs 416/min on 08-24. A 3× pressed/released bias remains (2.3/min released) |
| 24 | Brake pedal | `Switch 2` → `Brake pedal switch` (inverted by config) | switch | none | **SGND only (pre-P)** | OK (88 edges, 2 short runs) |
| 25 | Clutch pedal | `Switch 3` | owner-installed switch | none | **SGND only (pre-P)** | OK. Moved chassis → SGND 2026-08-29 |

Battery voltage (internal): 2.58 q, rev 0.61. Alternator ripple around a clean mean, flagged for
completeness. ECU temperature internal. Baro is disabled (`enableBaro`). No CAN Switchboard
switches, MUX, rotary or user switches are in use (all channels flat 0).
`latchingSwitchInput`, `lcActivationInput` and `ralInput` are set but have no separate hardware in
evidence.

## Observation — `Mux switch voltage raw` follows the brake

MUX is not enabled, but its raw channel reads 3.33 V (median) with the brake released and 5.0 V
with it pressed, r 0.91 against `Brake pedal switch`, minimum 1.82 V. *Hypothesis (model
knowledge):* on pre-"P" hardware the three switch inputs share one resistor-ladder ADC node, and this
channel is showing that node. That would explain why the documented cross-talk exists at all:
a foreign ground on one switch shifts the shared node that all three switches are read from. Unverified; no schematic.
