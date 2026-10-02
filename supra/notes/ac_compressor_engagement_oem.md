# OEM A/C compressor engagement criteria — JZA80 (JDM 1994 SZ)

Source: `C:\_\Projects\vehicles\supra\Supra Manuals\` —
`Air Conditioning.pdf` (AC section, US RM502U-era, pp. AC-17…AC-65),
`AC Manual.pdf` (AC-9 idle-up spec), `Diagnostics-Engine.pdf` p. DI-313
(A/C cut control), `JDM.Electrical.English.pdf` pp. 89-91 (JDM "Auto air
conditioner" circuit). Read 2026-08-25.

## Architecture (JDM diagram confirms same as US)

A/C amplifier ("AIR CONDITIONING COMPUTER") owns the request. It does **not**
drive the clutch directly:

    A/C amp  --MGC-->  ECM (AC1 in / ACMG out)  -->  MG clutch relay (R/B No.2)  -->  magnetic clutch

So the engine ECU holds veto authority over every A/C request. Voltages:
- A/C amp `MGC`: clutch ON <1 V, OFF 4–6 V (AC-64)
- ECM `AC1` (A/C switch state from amp): ON 0–1.5 V, OFF 7.5–14 V (DI-314)
- ECM `ACMG`: clutch ON ~1.3 V, OFF battery voltage (AC-65)
- Amp `A/C IN` (clutch feedback): ON 10–14 V, OFF <1 V (AC-63)

## Conditions that must ALL hold for clutch engagement

Amplifier side:
1. IG ON, engine running, A/C switch ON (or AUTO calling for cooling).
2. Blower running — ACMG check at AC-65 is made with the fan dial at Lo/Med/Hi.
3. Refrigerant pressure inside the window. Dual pressure switch (JDM diagram
   shows both a high/low air-side switch and an in-pressure-side switch).
   Amp cuts and logs code 7 outside **196 kPa (2.0 kgf/cm², 28 psi)** low or
   **3,140 kPa (32.0 kgf/cm², 455 psi)** high (AC-40).
4. Evaporator temp sensor (`TE`–`SG`) above the frost threshold. Sensor is an
   NTC thermistor: 4.5–5.2 kΩ @ 0 °C, 2.0–2.7 kΩ @ 15 °C; amp pin 2.0–2.4 V
   @ 0 °C, 1.4–1.8 V @ 15 °C (AC-33). *The manual gives the sensor curve, not
   the cut-in/cut-out setpoint* — the usual Toyota ~3 °C off / ~4 °C on is
   model knowledge, unverified here.
5. Compressor lock sensor healthy. Sensor sends 1 pulse/engine rev; if
   compressor/engine speed ratio deviates ≥20 % from normal for ≥3 s with
   engine ≥450 rpm, the amp turns the compressor OFF and blinks the A/C
   indicator at ~1 Hz (AC-38/39). Sensor resistance 160–210 Ω @ 20 °C.
6. Engine coolant temp sensor (amp's own, separate from ECM CLT) feeds
   warm-up control only — it gates blower/air-mix when cold, not documented
   as a compressor inhibit (AC-34).

ECM side (veto):
7. **A/C cut control** — during acceleration with vehicle speed ≤25 km/h
   (16 mph), engine speed ≤1,200 rpm, and throttle angle ≥60°, the ECM drops
   the magnet switch for several seconds (DI-313).
8. ECM also drops the clutch on the amp's pressure-switch fault signal (AC-40).

## Load compensation
OEM idle-up on clutch engagement (AC-9 / AC-77, warm, neutral):
2JZ-GE M/T 700 → 900 rpm; GE A/T 700 → 800; GTE 650 → 800.

## Diagnostics
A/C amp has its own panel self-diagnosis (IG ON while holding AUTO + REC;
LED blink codes 0–11). Code 6 = compressor lock, 7 = pressure abnormal,
3 = evaporator sensor. Memory hold times listed on AC-21 (15 s for the
lock/pressure codes, 8.5 min for the temp sensors).

## Inputs the A/C amplifier (JDM "AIR CONDITIONING COMPUTER") needs

Terminal names from the US AC troubleshooting section (AC-28…AC-61); presence on
the JDM SZ confirmed against `JDM.Electrical.English.pdf` pp. 89-91.

Power / reference
- `+B` — constant battery via ECU-B fuse (J/B No. 1). Holds diagnostic memory
  and set mode with IG off. Lose it and the mode clears at every key-off.
- `IG` — ignition-on supply. `ACC` — accessory supply. `GND` — body ground.
- Panel illumination / dimming circuit (JDM p. 90).

Operator command
- A/C control switch assembly (A/C, AUTO, blower speed, temp set, mode, REC/FRESH,
  DEF). Separate assembly from the computer on JZA80; also the diagnosis entry path.

Climate sensors
- `TR` room temperature (aspirated) · `TAM` ambient temperature · `S5` solar
- `TE` (ref `SG`) evaporator / "after evaporation" temperature — frost cut
- `TW` engine coolant temperature — the amp's OWN water temp sensor, separate from
  the engine ECU's CLT. Used for cold warm-up control (blower/air mix).

Position feedback
- `TP` air mix damper position sensor · `TPM` air outlet (mode) damper position sensor

Compressor interlocks
- `PSW` pressure switch — voltage varies with refrigerant pressure; cut outside
  196 kPa / 3,140 kPa. JDM circuit carries TWO switches: the high-or-low
  air-side switch and the A/C-in-pressure-side switch (the latter drives the
  condenser/cooling fan motors alongside the condenser-fan water temp switch,
  i.e. fan control is NOT routed through the computer).
- Compressor lock / revolution detecting sensor (160-210 Ω @ 20 °C, on compressor)
- Engine speed reference from the **magnetic clutch igniter** (JDM p. 89) — the
  denominator in the compressor/engine ratio test.
- `A/C IN` — magnetic clutch engagement feedback (10-14 V engaged, <1 V off)
- Engine control computer leg (`AC1`) — the request handshake / veto.

Not present: no vehicle-speed input to the A/C computer on this circuit.

Outputs for contrast: `MGC` (request to ECM), `HR` heater relay, `BLW` blower,
air mix / mode / air inlet servo motors, panel indicator.

Diagnosis: TDCL / diagnosis connector (JDM p. 91) plus the panel self-diagnosis
(IG ON holding AUTO + REC).

> **See also:** `ac_request_input_noise.md` — the EMU-side `Switch 1` request line
> chatters at ~7 Hz whenever the clutch pedal switch is closed, and that noise (not
> `acMinRPM`) causes most logged compressor drop-outs. Rule the wiring fault out
> before pursuing any amplifier-side cause below.

## Why the amplifier withholds the request at a stop (hot day)

Symptom shape: no request at idle, request present while moving. Amp-side causes,
most likely first:
1. **High-pressure cut.** No ram air at a stop, so the condenser depends entirely
   on the fan leg — which is switched by the A/C-in pressure switch and the
   condenser-fan water temp switch, NOT by the A/C computer. Fan leg down → head
   pressure past 3,140 kPa in seconds at hot idle → request withdrawn; returns
   with ram air.
2. **Compressor lock protection.** Belt slip is worst at idle (lowest belt speed,
   highest compressor torque under high head pressure). ≥20 % ratio deviation for
   ≥3 s at ≥450 rpm → compressor off, A/C indicator blinks ~1 Hz. The blink is the
   unique tell separating this from the pressure cut.
3. **Evaporator freeze cut** on a drifted or genuinely iced `TE` sensor.
4. **Engine speed reference** from the igniter marginal at idle frequency.

Test order: read panel self-diagnosis codes (6 lock / 7 pressure / 3 evaporator;
both 6 and 7 store after 15 s, so an idle-only fault survives to the read) →
manifold gauges at hot idle → confirm the condenser fan actually runs on request.

## EMU-side gate: the clutch output is held off below 1800 rpm (2026-09-08)

> **2026-10-01 update:** Will tested A/C at idle with `acMinRPM` ≈ 800 and an A/C-activated
> custom airflow correction (`new_cranking_rules.csv`; the 10-01 export reads 1800 again).
> Measured idle A/C air need, the request-glitch limit cycle, and the correction-table physics:
> [log_2026-10-01_new_cranking_rules.md](log_2026-10-01_new_cranking_rules.md) §2. The section
> below holds only while `acMinRPM` is above the idle target.

**The A/C clutch output in this tune is gated at 1800 rpm**, well above any idle
target — so the compressor **cannot be engaged while the idle controller is
running**. Everything in the OEM sections above describes the amplifier's request;
this gate is the EMU output condition sitting downstream of it.

Confirmed in `goodlog.csv` (2026-09-08, merged with `idle_log_running_fine.csv`
for the `AC Clutch` channel):

| | |
|---|---|
| `AC Clutch` = 1 samples | 2118 (37 % of the log) |
| minimum RPM with clutch engaged | **1804** |
| samples below 1800 rpm with clutch engaged | **0** |
| RPM at the 1→0 transitions on the way down | 1773, 1810, 1821, 1913 … |
| `Idle state` while engaged | 0 / 1 / 4 only — **never 2 (ACTIVE)** |

Consequences that keep getting re-derived wrongly:

- **There is no A/C load step onto an idling engine on this car.** Do not model
  one, do not size idle airflow authority or PID anti-windup against one, and do
  not read a clutch engagement in a log as an idle disturbance.
- **`idleACRPMIncrease` never fires.** The target increase is applied only while
  the clutch is engaged, which by construction never coincides with idle control.
  It is inert until the 1800 rpm gate changes.
- A log can show heavy clutch cycling and still be a clean idle log — the two
  regimes do not overlap. The drop-outs to watch for are the `Switch 1` request
  chatter documented in `ac_request_input_noise.md`, not the gate.
