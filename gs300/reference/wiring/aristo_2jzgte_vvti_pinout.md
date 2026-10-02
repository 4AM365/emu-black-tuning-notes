# 2JZ-GTE VVT-i (JZS161 Aristo) — ECU & loom pinout

Source: wilbo666 PBworks, *2JZ-GTE VVTi JZS161 Aristo Engine Wiring* —
<http://wilbo666.pbworks.com/w/page/42173082/2JZ-GTE%20VVTi%20JZS161%20Aristo%20Engine%20Wiring>
Retrieved 2026-09-08. Full per-pin What / Why / How prose is preserved verbatim in
`wilbo666_2jzgte_vvti_jzs161_aristo_engine_wiring.txt` (same folder).

## Engine ECU part numbers

| Toyota P/N | Dates | Transmission | Note |
|---|---|---|---|
| 89661-3A470 | 08/1997 – 06/2000 | Automatic | no inbuilt immobiliser |
| 89666-30180 | 07/2000 – 12/2004 | Automatic | engine immobiliser built into the ECU |

## Engine ECU Pinout

Plugs: **B1** (31 pins), **B2** (24 pins), **B3** (17 pins), **F59** (28 pins), **F60** (22 pins), **F84** (26 pins)

| Plug | Pin | Symbol | Definition | I/O |
|---|---:|---|---|---|
| B1 | 1 | #30 | No. 3 Injector | Output |
| B1 | 2 | #40 | Cyl 4 Injector Driver | Output |
| B1 | 3 | #50 | Cyl 5 Injector Driver | Output |
| B1 | 4 | #60 | Cyl 6 Injector Driver | Output |
| B1 | 5 | VSV1 | Intake Air Bypass Valve Vacuum Switching Valve | Output |
| B1 | 6 | MOL | Main Oil Level Switch | Input |
| B1 | 7 | M- | ETCS-i  Motor | Output |
| B1 | 8 | M+ | ETCS-i  Motor | Output |
| B1 | 9 | ME01 | ETCS-i Ground | Input |
| B1 | 10 | G2 | Intake Camshaft Position Sensor | Input |
| B1 | 11 | IGT | Ignition Trigger Cyl 1 & Cyl 6 | Output |
| B1 | 12 | IGT2 | Ignition Trigger Cyl 5 & Cyl 2 | Output |
| B1 | 13 | IGT3 | Ignition Trigger Cyl 3 & Cyl 4 | Output |
| B1 | 14 | — | *not used* |  |
| B1 | 15 | PMC | Pressure Modulation Control (Wastegate) Vacuum Switching Valve | Output |
| B1 | 16 | — | *not used* |  |
| B1 | 17 | OCV- | VVTi Solenoid | Output |
| B1 | 18 | OCV+ | VVTi Solenoid | Output |
| B1 | 19 | CL- | ETCS-i  Clutch | Output |
| B1 | 20 | CL+ | ETCS-i  Clutch | Output |
| B1 | 21 | E01 | ECU Ground | Input |
| B1 | 22 | NE- | Crankshaft & Intake Camshaft Position Sensor Ground | Input |
| B1 | 23 | NE+ | Crankshaft Position Sensor | Input |
| B1 | 24 | — | *not used* |  |
| B1 | 25 | IGF | Igniter Verification Signal | Input |
| B1 | 26 | RL | Alternator Charge Light Output (L) | Input |
| B1 | 27 | KNK2 | No.2 Knock Sensor (Rear) | Input |
| B1 | 28 | KNK1 | No.1 Knock Sensor (Front) | Input |
| B1 | 29 | LCKI | Airconditioning Compressor Lock Sensor | Input |
| B1 | 30 | GEO1 | ETCS-i Motor Shielding | Output |
| B1 | 31 | E02 | ECU Ground | Input |
| B2 | 1 | — | *not used* |  |
| B2 | 2 | VC | Sensor Power | Output |
| B2 | 3 | VSV2 | Exhaust Gas Control Valve Vacuum Switching Valve | Output |
| B2 | 4 | HT | Oxygen Sensor Heater | Output |
| B2 | 5 | #10 | Cyl 1 Injector Driver | Output |
| B2 | 6 | #20 | Cyl 2 Injector Driver | Output |
| B2 | 7 | PRG | Evaporative Emission Control Vacuum Switching Valve | Output |
| B2 | 8 | MOPS | Main Oil Pressure Switch | Input |
| B2 | 9 | PIM | Pressure Intake Manifold (MAP Sensor) | Input |
| B2 | 10 | VG | Engine Airflow | Input |
| B2 | 11 | — | *not used* |  |
| B2 | 12 | OX | Oxygen Sensor | Input |
| B2 | 13 | N | Automatic Transmission Neutral Gear Position Indicator | Input |
| B2 | 14 | THW | Water Temperature Sensor | Input |
| B2 | 15 | VPA | Accelerator Pedal Position Sensor | Input |
| B2 | 16 | VPA2 | Accelerator Sensor (Demand Position Sensor) | Input |
| B2 | 17 | E1 | ECU Ground | Input |
| B2 | 18 | E2 | Sensor Ground | Output |
| B2 | 19 | EVG | Airflow Meter Ground | Input |
| B2 | 20 | 2 | Automatic Transmission 2nd Gear Position Indicator | Input |
| B2 | 21 | L | Automatic Transmission 1st Gear Position Indicator | Input |
| B2 | 22 | THA | Air Temperature Sensor | Input |
| B2 | 23 | VTA | Throttle Position Sensor |  |
| B2 | 24 | VTA2 | Throttle Position Sensor (Actual Throttle Position Sensor) | Input |
| B3 | 1 | S1 | Automatic Transmission No.1 Shift Solenoid | Output |
| B3 | 2 | S2 | Automatic Transmission No.2 Shift Solenoid | Output |
| B3 | 3 | SD | Automatic Transmission Shift Solenoid | Output |
| B3 | 4 | NCO+ | Automatic Transmission Over Drive Direct Clutch Speed Sensor | Input |
| B3 | 5 | SP2+ | Speed Sensor | Input |
| B3 | 6 | S4 | Automatic Transmission Shift Solenoid | Output |
| B3 | 7 | SLU+ | Automatic Transmission Lock Up Solenoid | Output |
| B3 | 8 | SLN+ | Automatic Transmission Accumulator Back Pressure Solenoid | Output |
| B3 | 9 | SLT+ | Automatic Transmission Line Pressure Control Solenoid | Output |
| B3 | 10 | NCO- | Automatic Transmission Over Drive Direct Clutch Speed Sensor | Input |
| B3 | 11 | SP2- | Speed Sensor | Input |
| B3 | 12 | VSV3 | Exhaust Bypass Valve Vacuum Switching Valve | Output |
| B3 | 13 | SLU- | Automatic Transmission Lock Up Solenoid | Output |
| B3 | 14 | SLN- | Automatic Transmission Accumulator Back Pressure Solenoid | Output |
| B3 | 15 | SLT- | Automatic Transmission Line Pressure Control Solenoid | Output |
| B3 | 16 | FPU | Fuel Pressure Up Vacuum Switching Valve | Output |
| B3 | 17 | OIL | Automatic Transmission Oil Temperature Sensor | Input |
| F59 | 1 | — | *not used* |  |
| F59 | 2 | STA | Starter Signal | Input |
| F59 | 3 | FCUT | Fuel Cut | Output? |
| F59 | 4 | SFTU | Automatic Transmission Shift Up | Input |
| F59 | 5 | TC | Test Connector | Input |
| F59 | 6 | STP | Stop Light Switch | Input |
| F59 | 7 | 3 | Automatic Transmission M (Manual) Gear Position Indicator | Input |
| F59 | 8 | — | *not used* |  |
| F59 | 9 | — | *not used* |  |
| F59 | 10 | TAM | Ambient Air Temperature Sensor | Input |
| F59 | 11 | ST1- | Brake Signal Switch | Input |
| F59 | 12 | PRE2 | AC Pressure Switch 2 | Input |
| F59 | 13 | ACMG | AC Magnetic Clutch Relay Trigger | Output |
| F59 | 14 | SFTD | Automatic Transmission Shift Down | Input |
| F59 | 15 | — | *not used* |  |
| F59 | 16 | R | Automatic Transmission Reverse Gear Position Indicator | Input |
| F59 | 17 | D | Automatic Transmission Drive Gear Position Indicator | Input |
| F59 | 18 | TH+ | Engine Coolant Temperature Sensor | Input |
| F59 | 19 | — | *not used* |  |
| F59 | 20 | TACH | Tachometer | Output |
| F59 | 21 | PRE | AC Pressure Switch | Input |
| F59 | 22 | TH- | Engine Coolant Temperature Sensor | Input |
| F59 | 23 | CCS | Cruise Control Switch | Input |
| F59 | 24 | — | *not used* |  |
| F59 | 25 | REC | Fan Control | Output |
| F59 | 26 | P | Automatic Transmission Park Gear Position Indicator | Input |
| F59 | 27 | MPX2 | Multiplex Communications to AC ECU | Output |
| F59 | 28 | MPX1 | Multiplex Communications to Multiplex Network Body Computer No.1 | Input |
| F60 | 1 | BATT | Battery Power | Input |
| F60 | 2 | — | *not used* |  |
| F60 | 3 | — | *not used* |  |
| F60 | 4 | DI | Diagnostic Indication (Fuel Pump Control) | Input |
| F60 | 5 | FPC | Fuel Pump Control | Output |
| F60 | 6 | W | Engine Warning Light (Check Engine Light) | Output |
| F60 | 7 | +BM | ETCS-i Power | Input |
| F60 | 8 | +B2 | EFI Main Relay Switched Power | Input |
| F60 | 9 | IGSW | Ignition Switch | Input |
| F60 | 10 | M-REL | EFI Main Relay Trigger | Output |
| F60 | 11 | SIL | OBDII | Output |
| F60 | 12 | — | *not used* |  |
| F60 | 13 | TRC+ | ABS & TRC & VSC ECU Serial Data | Input |
| F60 | 14 | ENG+ | ABS & TRC & VSC ECU Serial Data | Output |
| F60 | 15 | NEO | Slave Engine Speed Sensor | Output |
| F60 | 16 | +B | Switched Battery Power | Input |
| F60 | 17 | — | *not used* |  |
| F60 | 18 | REC2 | Fan Control | Output |
| F60 | 19 | — | *not used* |  |
| F60 | 20 | TRC- | ABS & TRC & VSC ECU Serial Data | Output |
| F60 | 21 | ENG- | ABS & TRC & VSC ECU Serial Data | Input |
| F60 | 22 | EC | PRE and PRE2 Switches Ground | Input |
| F84 | 1 | — | *not used* |  |
| F84 | 2 | — | *not used* |  |
| F84 | 3 | — | *not used* |  |
| F84 | 4 | — | *not used* |  |
| F84 | 5 | — | *not used* |  |
| F84 | 6 | — | *not used* |  |
| F84 | 7 | — | *not used* |  |
| F84 | 8 | — | *not used* |  |
| F84 | 9 | EOM | GND | Input |
| F84 | 10 | KSW | Key Inserted | Input |
| F84 | 11 | — | *not used* |  |
| F84 | 12 | — | *not used* |  |
| F84 | 13 | — | *not used* |  |
| F84 | 14 | — | *not used* |  |
| F84 | 15 | — | *not used* |  |
| F84 | 16 | — | *not used* |  |
| F84 | 17 | — | *not used* |  |
| F84 | 18 | — | *not used* |  |
| F84 | 19 | — | *not used* |  |
| F84 | 20 | IMLD | Immobilizer LED | Output |
| F84 | 21 | TXCT | Key Amplifier | Output |
| F84 | 22 | RXCK | Key Amplifier | Input |
| F84 | 23 | CODE | Key Amplifier | Input |
| F84 | 24 | — | *not used* |  |
| F84 | 25 | — | *not used* |  |
| F84 | 26 | — | *not used* |  |

## 90980-11531 Engine Loom to Body Loom Plug (White)

Plugs: **BF1** (12 pins)

| Plug | Pin | Symbol | Definition | I/O |
|---|---:|---|---|---|
| BF1 | 1 | — | *not used* |  |
| BF1 | 2 | Engine ECU: E2 | Ambient Temperature Sensor Ground | Output |
| BF1 | 3 | Engine Mounted Diagnostic Connector: AB | SRS Airbag Power | Input |
| BF1 | 4 | — | *not used* |  |
| BF1 | 5 | Engine Mounted Diagnostic Connector: TS |  |  |
| BF1 | 6 | Engine ECU: R | Reverse Gear Automatic Transmission Position Switch Indicator | Output |
| BF1 | 7 | — | Alternator Battery Voltage Sense | Input |
| BF1 | 8 | Proportional Power Steering ECU: SOL+ | Proportional Power Steering Solenoid | Input |
| BF1 | 9 | Proportional Power Steering ECU: SOL- | Proportional Power Steering Solenoid | Input |
| BF1 | 10 | Engine Mounted Diagnostic Connector: WA |  |  |
| BF1 | 11 | Engine Mounted Diagnostic Connector: WB |  |  |
| BF1 | 12 | Engine Mounted Diagnostic Connector: TC |  |  |

## 90980-11527 Engine Loom to Body Loom Plug (White)

Plugs: **BF2** (10 pins)

| Plug | Pin | Symbol | Definition | I/O |
|---|---:|---|---|---|
| BF2 | 1 | Engine ECU: ACMG | AC Magnetic Clutch Relay Trigger Signal | Output |
| BF2 | 2 | Engine ECU: P | Park Gear Automatic Transmission Position Switch Indicator | Output |
| BF2 | 3 | — | *not used* |  |
| BF2 | 4 | — | *not used* |  |
| BF2 | 5 | — | *not used* |  |
| BF2 | 6 | — | Power to Coils and Igniter | Input |
| BF2 | 7 | — | Power to Fuel Injectors | Input |
| BF2 | 8 | — | Starter Motor Relay Switched Power | Input |
| BF2 | 9 | Engine ECU: +B, +B2 | Main EFI Relay Switched Power | Input |
| BF2 | 10 | — | *not used* |  |

## 90980-11710 Engine Loom to Body Loom Plug (White)

Plugs: **BF3** (9 pins)

| Plug | Pin | Symbol | Definition | I/O |
|---|---:|---|---|---|
| BF3 | 1 | — | *not used* |  |
| BF3 | 2 | Engine ECU: TACH |  |  |
| BF3 | 3 | Engine ECU: D | Drive Gear Automatic Transmission Position Switch Indicator | Output |
| BF3 | 4 | Engine ECU: STA | Starter Motor Relay Trigger Signal | Output |
| BF3 | 5 | — | Starter Signal | Input |
| BF3 | 6 | — | *not used* |  |
| BF3 | 7 | Engine ECU: E1 | Ground | Output |
| BF3 | 8 | — | *not used* |  |
| BF3 | 9 | — | Ignition Switched Power | Input |

