# Bypassing the OEM Aristo ECU — dependency map

> ## ⛔ THIS IS NOT THE SUPRA. DO NOT CROSS-REFERENCE.
>
> This repository's main subject is a **MKIV Supra**. **This car has nothing to do with it.**
> It is Josh Napier's **2000 Lexus GS300 (JZS160)** with a **JDM Aristo (JZS161) 2JZ-GTE VVT-i**
> and a **CD009** gearbox. Different chassis, different body electronics, different engine
> variant, different throttle body, different pedal, different gearbox, different owner.
>
> **Rules for anyone — human or agent — working in this folder:**
>
> 1. **Never** carry a value, table, calibration constant, pin, sensor trace, hardware part or
>    conclusion from the Supra notes (`../../supra/`, `../../notes/`) into this car, and never
>    the other way. Not as a starting point, not as a sanity check, not "for reference."
> 2. **Never** load the `supra-specs` skill for a question about this car.
> 3. The two share an engine *family* and an ECU *brand*. That is the entire overlap, and
>    same-family is not same-part. Every conclusion here must stand on the GS300 / Aristo
>    documents in [`../reference/`](../reference/README.md) alone.
> 4. If a fact cannot be sourced from this folder's documents or from Josh, it is **unverified**.
>    Say so. Do not reach across for it.


Josh Napier's GS300 ([`my_car.md`](my_car.md)). Established 2026-09-08.

**Where the car is now.** An ECUMaster EMU Black piggyback harness is installed, **v3 firmware**.
The OEM Aristo ECU still owns the drive-by-wire throttle and idle air, the instrument cluster,
the HVAC, and — until the swap — the automatic transmission. The gearbox is now a **CD009**
(Nissan 350Z/G35 6-speed).

**Where it is going.** Repin the ECUMaster harness so the stock ECU comes out completely. The
immobiliser goes with it and is not to be preserved.

Every row below is read off the factory documents in [`../reference/`](../reference/README.md) —
**EWD356U** (GS300 body) and wilbo666's JZS161 pinout (Aristo engine ECU) — with page or pin
cited. Signal character comes from wilbo666's per-pin notes, not from inference. Where something
about *this particular car* is not yet established, the row says so.

---

## 1. The one structural problem: the multiplex bus

The Aristo ECU is not only an engine controller. It is a **node on the Toyota body multiplex
network (BEAN)** — `MPX1` (F59-28, in) and `MPX2` (F59-27, out). The GS300 is built the same way:
EWD356U p. 246 draws the bus with the Engine Control Module on it alongside the combination
meter, the A/C control assembly, both body ECUs, the multi-display and the tilt ECU. p. 247 lists
27 systems riding it.

wilbo666 states what the engine ECU puts on that bus: *"the engine ECU sends the water
temperature signal to the dash, the automatic transmission shifter position signals, etc via the
Multiplex network."*

**The EMU Black cannot join it.** BEAN is not CAN. The only Toyota entry in the EMU's OEM
vehicle-CAN list is the GT86/BRZ (`docs/emu-black-help/CANSerial.md`:876), which is a CAN car.

So the multiplex-fed cluster functions have **no wire to repin** — they simply stop. That is the
part of this job that needs a decision rather than a crimp, and it is worth settling before
touching a pin.

---

## 2. Instrument cluster

| Function | Aristo pin | Signal type | Electrical detail | After bypass |
|---|---|---|---|---|
| **Speedometer** | — | — | ABS & TRC & VSC ECU drives `SP1` to the meter directly | **survives.** EWD356U pp. 90, 393, 461. wilbo666 on `SP2+`: *"The speed signal for the dash is NOT received via the Multiplex… The dash speed signal comes from the ABS ECU (SP1)."* Nothing to do |
| **Tachometer** | `TACH` F59-20 → BF3-2 | **digital square wave** | 0 V ↔ battery voltage, frequency proportional to RPM | **repin** to an EMU frequency/RPM output — *if* the Aristo cluster is fitted. If it is the GS300 cluster, tach comes off the **igniter** `TAC` terminal instead (EWD356U p. 360) and survives untouched. See §9 |
| **Water temperature gauge** | `THW` B2-14 | thermistor in, **BEAN serial** out | one coolant sensor (`E8`), to the ECM only (EWD356U p. 161) | **lost, and not re-wirable.** There is **no water-temperature sender or receiver gauge anywhere in EWD356U** — the only `WATER TEMP. SW` (W3) is the radiator-fan switch (p. 318), and the only `SENDER` in the book is the fuel sender. The needle is painted by the meter's own CPU from bus data. See §2a |
| **Charge / alternator light** | `RL` B1-26 | switch-to-ground in, **BEAN** out | alternator regulator pulls it low when not charging | **lost, and not re-wirable.** EWD356U p. 82 draws the generator's IC-regulator `L` terminal going **to the ECM**, with the CHARGE lamp driven by the meter `CPU` and `MPX1`/`MPX2` between the two. There is no alternator-to-lamp wire to restore. See §2a |
| **Low oil pressure light** | `MOPS` B2-8 | switch-to-ground in, **BEAN** out | switch grounded through the block; closes below ~20 kPa (EWD356U p. 94) | **lost, and not re-wirable** — the switch goes to the ECM and the lamp is CPU-driven (EWD356U p. 92). The switch itself is still a perfectly good EMU input. See §2a |
| **Oil level light** | `MOL` B1-6 | switch in, **BEAN** out | float switch, temperature-qualified (EWD356U p. 94) | **lost, and not re-wirable** — same architecture. See §2a |
| **Oil temperature** | via the `MOL`/`MOPS` group | **BEAN** | EWD356U p. 92 | **lost.** Delete, or re-sense on the EMU |
| **Check engine / MIL** | `W` F60-6 | **low-side switch** | ECU grounds it; lamp's other side on switched 12 V. ON = fault | **repin** to an EMU low-side output |
| **A/T gear position indicator** | `P` F59-26, `R` F59-16, `D` F59-17, `3` F59-7, `2` B2-20, `L` B2-21, `N` B2-13 | switch in, **BEAN** out | | **gone regardless** — manual car, §6 |
| **Fuel gauge** | — | resistive sender | `F15`, ~2.0 Ω full / 48.7 Ω empty (EWD356U p. 94) | **survives.** Nothing to do |
| **ABS / VSC / SLIP / BRAKE lights** | — | discrete from the ABS ECU | | survive the ECU deletion — but see §7 |

### 2a. The cluster is a computer, not a bundle of gauges — correction

**This corrects earlier advice in this note.** An initial reading suggested the lost lamps and the
temperature gauge could simply be re-wired to their senders. **They cannot.**

The GS300 combination meter carries its **own CPU** — labelled as `CPU` inside the meter block on
EWD356U pp. 90 and 92 — and it is a BEAN node on `MPX1`/`MPX2`. The ECM-sourced gauges and warning
lamps are *rendered by that CPU from bus messages*. There are no analog terminals behind them.

Three pieces of evidence, all from EWD356U:

- **No sender exists.** Searching the entire book, the only `WATER TEMP.` part is the radiator-fan
  switch `W3` (p. 318) and the only `SENDER` is the fuel sender `F15`. There is no water-temp
  sender and no receiver gauge in the car.
- **The charging circuit proves the pattern** (p. 82): the generator's IC regulator `L` terminal
  runs **to the ECM**, not to the lamp. The CHARGE lamp sits behind the meter `CPU`, with
  `MPX1`/`MPX2` joining meter and ECM.
- **Oil pressure and oil level** follow the same path (p. 92) — switches to the ECM, lamps behind
  the CPU.

**What this changes.** For water temperature, charge, oil pressure and oil level there is nothing
to wire to. The only routes to a live factory cluster are:

1. **Keep the Aristo ECU transmitting** — [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md)
2. **Build a BEAN gateway** — §8 option B
3. **Go around the instrument entirely** — separate aftermarket gauges, or drive the movements
   inside the cluster directly, which is a different and far more invasive job

The switches and senders themselves are unaffected and remain good EMU inputs. What is lost is the
factory *display* of them.

**What still survives:** the **speedometer** (the ABS ECU drives `SP1` straight to the meter) and
the **fuel gauge** (`F15` is a resistive sender wired directly). Those two are analog, and they are
the exceptions that make the rest of the architecture obvious.

## 3. HVAC and cooling

| Function | Aristo pin | Signal type | Electrical detail | After bypass |
|---|---|---|---|---|
| A/C compressor clutch | `ACMG` F59-13 → BF2-1 | **low-side switch** | ECU grounds the relay coil; coil's other side on switched 12 V | **repin** to an EMU low-side output. ECU control is what drops A/C under load — keep that behaviour in the EMU |
| A/C pressure switches | `PRE` F59-21, `PRE2` F59-12, ground `EC` F60-22 | **digital switch inputs** | referenced to `EC`, not chassis ground | **repin** to EMU switch inputs, gating the clutch output |
| A/C compressor lock sensor | `LCKI` B1-29 | **frequency / speed pulse** | compressor speed pickup, other side grounded; protects against a seized compressor | **repin to a frequency input, or delete** |
| Ambient air temperature | `TAM` F59-10, ground BF1-2 | analog thermistor | | **lost to the HVAC** — the climate controller receives it via the ECU/multiplex. It will need its own source or will fault |
| **A/C control assembly ↔ engine data** | `MPX1`/`MPX2` | **BEAN serial** | coolant temp, RPM, load | **lost.** Expect faults or degraded auto mode |
| Radiator fan speed | `REC` F59-25 **+** `REC2` F60-18 | **PWM pair** | wilbo666: *"The REC and REC2 pins are triggered by the engine ECU in a PWM fashion"* into the fan controller | **repin — two coordinated PWM outputs.** A single on/off output will not reproduce this |
| Fan temperature input | `TH+` F59-18 / `TH-` F59-22 | **analog thermistor, differential** | a **second** coolant thermistor, in the **radiator lower tank**, wired between `TH+` and `TH-` — not to chassis ground, and not the same sensor as `THW` | **repin** to an EMU analog input with its own ground reference. Fan speed is scheduled off *this* sensor, not off engine-out temp |

## 4. Throttle, idle, cruise — the big lift

**There is no idle air control valve on this engine.** No `ISC` / `ISCV` / `IACV` pin exists
anywhere in the Aristo pinout, and none in the GS300 EWD either — both cars are ETCS-i. Idle air
is the throttle plate. wilbo666 on the throttle motor: *"Having the throttle controlled by the
engine ECU allows idle speed control, traction control, cruise control, etc to be built directly
into the engine ECU."* This contradicts "IACV" in the brief — see §8.

| Function | Aristo pin | Signal type | Electrical detail |
|---|---|---|---|
| Throttle motor | `M+` B1-8, `M-` B1-7 | **PWM, H-bridge** | wilbo666: *"The M+ and M- pins are triggered by the engine ECU in a PWM fashion"* |
| Throttle motor power | `+BM` F60-7 | permanent 12 V | via the **15 A ETCS fuse** — separate from the EFI feed |
| ETCS-i clutch | `CL+` B1-20, `CL-` B1-19 | **DC coil output** | *"The ETCS-i clutch must be engaged for the electric motor to be able to open or close the throttle"* — the blade cannot be driven with the clutch de-energised |
| ETCS-i ground / shield | `ME01` B1-9, `GEO1` B1-30 | ground + motor shield | keep the shield |
| Throttle position | `VTA` B2-23, `VTA2` B2-24 | **analog 0–5 V ×2** | two outputs *"with different responses"* — main + check |
| Pedal position | `VPA` B2-15, `VPA2` B2-16 | **analog 0–5 V ×2** | same arrangement at the pedal |
| Sensor supply | `VC` B2-2 | **regulated +5 V out** | feeds TPS, pedal **and** MAP |
| Sensor ground | `E2` B2-18 | sensor ground | |
| **Cruise control** | switch on `CCS` F59-23 | digital switch in | cruise is implemented *through* ETCS by the ECM (EWD356U p. 107) — there is no separate actuator. **Lost** unless the EMU is set up to do it |

### Correction — the check sensors are almost certainly fine

An earlier draft of this note warned that `VTA2` and `VPA2` might not be usable as EMU check
inputs because they are Toyota diagnostic pairs *"with different responses"* rather than matched
mirrors. **Reading ECUMaster's own DBW documentation, that concern was overstated.**

The EMU does not assume a mirrored sensor. It uses a **`TPS check tolerance map`**: you move the
throttle, read the check sensor's voltage at various positions, enter those into the map, and the
strategy then verifies that the live voltage sits within `Error tolerance` of the mapped value
(`docs/emu-black-help/DBW.md` step 10). An offset second sensor with a different slope is exactly
what that map exists to accommodate. ECUMaster suggests starting with `Error tolerance` at 5 V,
watching the `TPS check error` log channel, and tightening — *"If everything is calibrated
correctly, this value should not exceed a few tenths of a volt."*

So the requirement on `VTA2` / `VPA2` is that they be **repeatable and monotonic**, not that they
mirror. Still scope all four traces — but to *fill the map*, not to decide whether the sensors can
be used at all. ECUMaster's standing advice: *"For safety reasons, it is recommended to connect
both sensors in both the throttle and the accelerator pedal."*

### v3 wiring — this is the opposite of v2, and it is easy to get wrong

This car is on **v3 firmware**, and ECUMaster changed the convention:

> *"In the EMU BLACK 2.xxx software versions, the accelerator pedal sensor was connected to the TPS
> input, while the throttle position sensor was connected to analog inputs 1 to 6. In the 3.xxx
> versions, the throttle position sensor should be connected to the TPS input."*
> — `docs/emu-black-help/DBW.md`

So on this car: **throttle position (`VTA`) → the TPS input. Pedal (`VPA`) → a free analog input.**
Check sensors go to further free analog inputs. Any older guide will have this backwards.

Setup order, from the same page: configure TPS main → configure PPS main with its 0 % / 100 %
voltages and valid-range limits → enable DBW and set the control frequency → run
**Tools → DBW calibration tool** → *then* add the check sensors and their tolerance maps.

## 5. Power, start, fuel pump

The immobiliser (`KSW` F84-10, `TXCT` F84-21, `RXCK` F84-22, `CODE` F84-23, `IMLD` F84-20,
`EOM` F84-9) is **deleted outright** — plug F84 has no other live pins and does not get repinned.
The transponder amplifier, key coil and security indicator all go dead, which is the intent.

| Function | Aristo pin | Signal type | Electrical detail | After bypass |
|---|---|---|---|---|
| Permanent battery | `BATT` F60-1 | 12 V permanent | via the **25 A EFI fuse** | EMU permanent 12 V |
| Ignition sense | `IGSW` F60-9 | 12 V digital in | battery voltage in **RUN and CRANK** | EMU key-on input |
| Main relay trigger | `M-REL` F60-10 | **high-side output** | the ECU **sources battery voltage** to the relay coil; coil's other side to ground. Holds for a few seconds after key-off | **EMU main relay output.** Note the polarity — this is not a ground-switched relay. Keep an equivalent post-run hold so the throttle parks |
| Switched power | `+B` F60-16, `+B2` F60-8 → BF2-9 | 12 V switched | from the main relay | EMU switched feed |
| Fuel pump | `FPC` F60-5 | **PWM 0–5 V** | wilbo666: *"outputs a 0V to 5V Pulse Width Modulated (PWM) signal which is connected to the Fuel Pump ECU to control fuel pump speed"* — **not** a relay drive | EMU PWM output into the fuel pump ECU, or replace the pump ECU with a straight relay |
| Fuel pump feedback | `DI` F60-4 | plausibility input | **only wired on 07/2000-on cars** | drop |
| Crank signal in | `STA` F59-2 ← BF3-5 | 12 V digital in | battery voltage when the ignition switch is in CRANK | EMU crank input |
| Brake pressed | `STP` F59-6 | 12 V digital in | battery voltage **when pressed**, open when not | EMU switch input |
| Brake released | `ST1-` F59-11 | 12 V digital in, **inverted** | battery voltage when **not** pressed — the complement of `STP`. The pair is a plausibility check | EMU switch input, or drop one |
| OBDII K-line | `SIL` F60-11 | **ISO 9141-2 serial** | | **lost.** Factory scan tools stop working; the EMU has its own link |
| Test connector | `TC` F59-5 | digital in | | drop |

## 6. The CD009 swap — what changes on the transmission side

Plug **B3 is almost entirely the automatic transmission**. The Aristo ECU *is* the ECT
controller; there is no separate A/T ECU. All of this is now dead and does not get repinned:

`S1` B3-1 · `S2` B3-2 · `SD` B3-3 · `S4` B3-6 (shift solenoids) · `SLU±` B3-7/13 (lock-up) ·
`SLN±` B3-8/14 (accumulator back pressure) · `SLT±` B3-9/15 (line pressure) · `NCO±` B3-4/10
(OD direct-clutch speed) · `OIL` B3-17 (ATF temperature) · `SFTU` F59-4 / `SFTD` F59-14
(shift up/down) · the seven gear-position inputs in §2.

Two pins on B3 are **not** transmission and must be kept: `VSV3` B3-12 (exhaust bypass VSV) and
`FPU` B3-16 (fuel pressure up VSV).

### What the CD009 actually has

The CD009 carries **one switch and nothing else**. It has no speed sensor and no neutral switch —
on the 350Z the speedometer is driven from the ABS ECU and the start interlock is a clutch-pedal
switch. This is well established in the swap community and is why vendors sell external speed
pickups ([LOJ Conversions](https://lojkits.com/products/copy-of-350z-lsx-swap-transmission-mount),
[MY350Z](https://my350z.com/forum/engine-and-drivetrain/619407-transmission-speed-sensor.html)).
One swap write-up ([SVK Works](https://svkworks.com/blog-sc400-cd009-swap-wiring.html)) describes
a reluctor VSS on the CD009; the Nissan-side sources and the existence of the aftermarket pickups
contradict it. **Confirm by eye on Josh's actual case before planning around either.**

| Item | On the CD009? | Signal type | Electrical detail | What to do |
|---|---|---|---|---|
| **Reverse light switch** | **yes** | **SPST, normally open**, closes in reverse | 2-wire, **non-polarised** — it is a bare switch, not a sensor. Connector sold as the [CD009/CD00A reverse switch connector](https://fischracingtech.com/products/cd009-cd00a-reverse-switch-connector) | wire into the GS300 back-up lamp circuit. On the GS300 that circuit ran through the A/T `PARK/NEUTRAL POSITION SW` (P1), terminals **4–8 closed in R** (EWD356U pp. 74, 75) — take over that pair |
| **Neutral / range switch** | **no** | — | the 350Z has no trans-mounted neutral safety switch | use a **clutch pedal interlock switch** (SPST). On the GS300 the interlock is in the **starter circuit itself**, not in the ECU: ignition `ST2` → P/N switch `P`/`N` terminals → starter relay (EWD356U p. 359). Put the clutch switch in that path. Feed it to an EMU input too if you want clutch state for idle or launch |
| **Vehicle speed sensor** | **no** | — | | see below |

### Vehicle speed — pick a source

The **speedometer** does not need this (§2, ABS-driven). What needs it is the **EMU**: speed is
used for idle control, cruise, speed limiting and any traction strategy. The old source was
`SP2+`/`SP2-` B3-5/11 — a **VR/reluctor pair, 12 pulses per automatic output-shaft revolution**,
from the sensor on the left rear of the A650E. That sensor is gone with the gearbox.

| Option | Signal type | Notes |
|---|---|---|
| Tap an **ABS wheel speed sensor** | **VR — differential sine**, amplitude and frequency both rising with speed | the EMU wants a clean square wave; a VR→Hall conditioner is the usual answer. Do not load the ABS ECU's input |
| **Hall pickup + trigger wheel** on the CD009 output shaft | **digital square, 0–5 V or 0–12 V**, PPR set by the wheel | cleanest for the EMU. Choose PPR knowingly — it sets the resolution at low speed |
| **Driveshaft flange pickup** (LOJ-type) | **Hall, 10 PPR at the driveshaft** | matches Z32 / S13 / S14 signal style, which are 4 PPR — so calibration is not interchangeable between them |

Also gone with the automatic: the shift-lock control ECU (EWD356U p. 344), the A/T indicator
lamp, and the A/T shift main switch.

## 7. ABS, traction and stability

| Function | Aristo pin | Signal type | After bypass |
|---|---|---|---|
| Engine speed copy to ABS/TRC/VSC | `NEO` F60-15 | **digital pulse train** | reproducible — EMU frequency output into the ABS ECU's `NEO` pin |
| **ABS/TRC/VSC ↔ engine serial** | `TRC+` F60-13, `TRC-` F60-20, `ENG+` F60-14, `ENG-` F60-21 | **differential serial, two pairs** | **lost.** Undocumented protocol; nothing on the EMU speaks it |

The stability ECU uses that link to request torque reduction. With the OEM ECU gone it loses its
counterpart — expect TRC/VSC to fault and light the dash. Whether ABS braking itself still
functions is **unverified**; ABS is normally independent of engine torque requests, but confirm
before relying on it. The speedometer feed `SP1` is a separate output from that same ECU and is
not at risk.

## 8. BEAN — can the multiplex be re-created?

Primary source, now held locally: **SAE 970297, *Toyota Body Electronics Area Network (BEAN)***
(Honda, Sakai, Akatsuka) — [`../reference/wiring/SAE970297_Toyota_BEAN.pdf`](../reference/wiring/SAE970297_Toyota_BEAN.pdf),
9 pp., text extracted to `../reference/sae970297_bean_text.txt`. Everything in the table below is
quoted or read directly from that paper, not inferred.

| Property | Value |
|---|---|
| Medium | **single non-shielded wire**, 12 V |
| Rate | **10 kbps** |
| Encoding | **NRZ** |
| Line driver | current-control type — current is ramped onto the bus deliberately, to keep radiated noise down |
| Bus access | **CSMA/CD with bitwise arbitration** |
| Error check | **8-bit CRC** |
| Response | **ACK / NAK** |
| Frame | `SOF`(1b) · `PRI`(4b) · `ML`(4b) · `DST-ID`(8b) · `MES-ID`(8b) · `DATA` 1–11 bytes · `CRC`(8b) · `EOM` · `RSP`(2b) · `EOF`(6b) · `IDL` |
| `PRI` | priority, up to 16 levels |
| `ML` | message length — byte count of `[ID + DATA]`, range 3–13 |
| `DST-ID` | destination. **`0xFF` = broadcast**, anything else is point-to-point |
| Bit stuffing | an inverted bit is inserted after 5 consecutive identical bits, from `SOF` through `CRC` |
| Network size | **20+ nodes, ~200 possible messages** |
| Implementation | designed to be small enough for a **general-purpose 8-bit MCU** |
| Sleep | power-saving mode when the ignition is off |
| Diagnostics | carried as variable-length frames through a gateway ECU |

### What exists in the wild

| Project | What it does | State |
|---|---|---|
| [**BeanMPX**](https://github.com/fiztech-code/BeanMPX) (fiztech-code) | Arduino library that bit-bangs BEAN on two configurable pins using Timer1 or Timer2. **Transmits and receives.** Builds `DST-ID` / `MES-ID` / `ML` / `CRC` / `EOM` for you, acknowledges nominated destination IDs, and retries 3× when no ACK comes back | archived read-only 2026-03-03 — usable, unmaintained |
| [GVRET](https://github.com/collin80/GVRET) | general vehicle reverse-engineering firmware (Arduino Due) | active, generic — not BEAN-specific |
| [ToyotaLib](https://github.com/b3bb0/ToyotaLib) | Toyota OBD-I Arduino library | tangential |

### The honest assessment

**The protocol is not the hard part.** 10 kbps NRZ on one wire with an 8-bit CRC is a solved
problem, and BeanMPX already solves it.

**The message dictionary is the hard part.** Which `DST-ID` / `MES-ID` carries coolant temperature,
and which bit inside it is the charge lamp, is not in SAE 970297 and Toyota never published it.
It is per-model. There is exactly one place to get it: **sniff this car's own bus while the OEM
ECU is still fitted and working.**

That creates a hard ordering constraint. **Once the stock ECU comes out, the traffic is gone and
cannot be recovered.** If there is any chance of wanting the gauges back, capture the bus first.

Two secondary unknowns, both hardware:

- **Transceiver.** The paper describes a purpose-built current-control driver. BeanMPX's published
  circuit does not name a transceiver part, and its optional MCP2515 is on the CAN side, not the
  BEAN side. Sourcing or building a BEAN-compatible line interface is an open item the library
  does not solve.
- **Node behaviour on the real bus.** BEAN nodes arbitrate and ACK. A gateway that transmits badly
  can disturb traffic the cluster and body ECUs depend on. Bench it against a captured log before
  it goes near the car.

### Three ways to play it

| | Approach | Effort | What you get | What it costs |
|---|---|---|---|---|
| **A** | **Don't re-create it.** Accept the dark gauges; put coolant temperature, oil pressure and oil level on **separate aftermarket gauges** or on a phone/laptop dash off the EMU | low | speedo, tach and fuel keep working; you still see every value, just not in the factory instrument | the factory temperature gauge and three warning lamps stay dead — **they cannot be re-wired** (§2a); HVAC auto mode stays degraded |
| **B** | **BEAN gateway.** An MCU listening to the EMU (CAN or serial) and transmitting the frames the cluster and A/C ECU expect | high, and front-loaded by the capture work | gauges and HVAC behave as factory | needs the dictionary sniffed first, a transceiver solved, and bench validation. A weekend of wiring becomes a project |
| **C** | **Leave the OEM ECU powered as a bus node**, engine outputs unused | low, if it works at all | everything keeps working, *and* it sidesteps the dictionary problem entirely — the Aristo ECU already knows the dictionary | drags the immobiliser back in, holds the MIL on, and rests on an untested assumption. **Worth testing before rejecting** — see [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md) |

**A is the default. C is the cheap long shot and should be tested first**, because it costs an
afternoon and, if it works, delivers B's result without the reverse engineering — the argument and
the test procedure are in [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md).
B is worth funding only if C fails and Josh still wants a factory-looking dash. Either way the
capture has to happen **before** the ECU comes out, so the decision cannot be deferred.

## 9. Open questions, in the order they block work

1. **"IACV" — there isn't one.** Neither car has an idle air control valve; both idle on the
   throttle plate. Either an aftermarket IACV has been fitted, or the term stands in for idle via
   DBW. This changes §4 materially.
2. **Which cluster and body harness** — GS300 (JZS160) or Aristo (JZS161)? Decides the tachometer
   (ECU pin vs igniter terminal) and which multiplex node map applies. The architecture is the
   same either way, so the conclusions hold; the pin numbers do not.
3. **Sequential turbo state** — `VSV1` B1-5, `VSV2` B2-3, `VSV3` B3-12 and `PMC` B1-15 are the
   factory sequential twin-turbo and wastegate controls. Still sequential, true-twin, or single
   determines how many of those the EMU needs to drive.
4. **What the EMU already owns on the piggyback** — injectors, coils, crank/cam, knock, MAP,
   wideband. Knowing the current split avoids repinning something twice.
5. **Fuel pump ECU** — still fitted? `FPC` is a PWM speed command, not a relay drive, so the
   answer changes what that output has to be.

---

## 10. What needs to be done

Ordered. Phases 0 and 1 happen **while the stock ECU is still in the car and running** — some of
what they capture cannot be recovered afterwards.

### Phase 0 — establish the facts (no tools down)

| # | Task | Why it's here | Done when |
|---|---|---|---|
| 0.1 | Read the **ECU part number** off the case | tells you which harness revision you have; `DI` F60-4 is only wired on 07/2000-on cars | number written down |
| 0.2 | Identify the **cluster and body harness** — GS300 (JZS160) or Aristo (JZS161) | decides whether the tachometer comes from the ECU pin or the igniter, and which node map applies | confirmed by connector count / part number at the cluster |
| 0.3 | Resolve **"IACV"** — find it, or confirm idle is the throttle plate | there is no idle-air pin on either car's ECU. If a valve exists it was added, and it needs an output | valve found and identified, or confirmed absent |
| 0.4 | Inventory **what the EMU already drives** on the piggyback | avoids repinning the same circuit twice | a list: injectors, coils, crank, cam, knock, MAP, wideband, boost |
| 0.5 | Confirm the **turbo configuration** — sequential, true-twin, or single | sets how many of `VSV1` B1-5, `VSV2` B2-3, `VSV3` B3-12, `PMC` B1-15 the EMU must drive | plumbing traced |
| 0.6 | Confirm the **fuel pump ECU** is still fitted | `FPC` F60-5 is a PWM speed command, not a relay drive | found, or confirmed removed |
| 0.7 | Inspect the **CD009 case** for a speed sensor boss | sources disagree; settle it by eye | photographed |

### Phase 1 — capture what removal destroys ⏳ **order-critical**

| # | Task | Why it's here | Done when |
|---|---|---|---|
| 1.1 | **Sniff the BEAN bus** with the stock ECU live — key on, engine running, cold and warm, A/C on and off, oil pressure lamp cycling | the message dictionary exists nowhere else. Once the ECU is out this is unrecoverable (§8) | logs captured and archived to `../reference/` |
| 1.2 | **Scope `VTA` / `VTA2` and `VPA` / `VPA2`** through a full sweep, closed to wide open | decides whether the EMU can use the check sensors at all, which decides the DBW safety plan (§4) | four voltage-vs-position traces recorded |
| 1.3 | **Scope `REC` / `REC2`** across a fan ramp | it is a PWM pair into a fan controller; you need the duty relationship to reproduce it (§3) | duty-vs-fan-speed captured |
| 1.4 | **Scope `TACH`** (and, if the GS300 cluster is fitted, the igniter `TAC` terminal) | confirms pulses per revolution before you try to drive the gauge | frequency-vs-RPM confirmed |
| 1.5 | **Measure `FPC`** duty across the operating range | tells you what the pump ECU expects | duty range recorded |
| 1.8 | **Read the OEM diagnostic trouble codes** through `SIL` F60-11 at the diagnostic connector | the ECU has logged exactly which inputs it lost with the automatic. Destroyed when the ECU comes out | codes recorded — see [`high_idle_after_cd009_swap.md`](high_idle_after_cd009_swap.md) §5 |
| 1.7 | **Disconnection test** — pull the throttle motor, then the throttle sensors, then the pedal, then injectors and coils; key on each time and watch the cluster and HVAC | decides whether the Aristo ECU can stay as a BEAN gateway (option C). ~30 minutes, fully reversible | each step recorded as gauges-live or gauges-dead — procedure in [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md) §5 |
| 1.6 | Record **resting voltages and states** on every pin in §§2–7 | your only reference for "was it like that before?" | table filled in |

### Phase 2 — decide

| # | Decision | Options | Consequence |
|---|---|---|---|
| 2.1 | **BEAN: re-create it or not** | §8 option A (discrete rewire) or B (gateway). C is rejected | gates 1.1's value and the whole cluster plan. **Decide before the ECU comes out** |
| 2.2 | **Temperature gauge** | EMU output · separate sender · dead gauge | drives whether a sender and a port are needed |
| 2.3 | **Vehicle speed source for the EMU** | ABS tap through a VR→Hall conditioner · Hall pickup and trigger wheel on the CD009 output shaft · driveshaft flange pickup | sets PPR, which sets the EMU calibration |
| 2.4 | **Cruise control** | implement on the EMU · delete | it ran through ETCS; there is no separate actuator |
| 2.5 | **A/C compressor lock sensor** | keep on a frequency input · delete | protection vs. one less input |
| 2.6 | **TRC / VSC** | accept the dash lights · disable the system properly | the serial link cannot be reproduced (§7) |

### Phase 3 — repin the EMU harness

| # | Task | Detail |
|---|---|---|
| 3.1 | **Power and relay** | `BATT` F60-1 (25 A EFI fuse), `IGSW` F60-9, `+B`/`+B2`, and `M-REL` F60-10 — remember it **sources 12 V** to the coil. Keep a post-key-off hold so the throttle parks |
| 3.2 | **DBW** | `M+`/`M-` B1-8/7 to the EMU H-bridge; `CL+`/`CL-` B1-20/19; `ME01` B1-9 and the `GEO1` B1-30 shield; `+BM` F60-7 on its own 15 A ETCS fuse; `VC` B2-2 and `E2` B2-18; `VTA`/`VTA2`, `VPA`/`VPA2` per the 1.2 result |
| 3.3 | **Engine sensors and actuators** | whatever 0.4 shows the EMU does not already own — `THW` B2-14, `THA` B2-22, `PIM` B2-9, `VG` B2-10, knock `KNK1`/`KNK2`, `OX` B2-12 + `HT` B2-4, `OCV±` B1-17/18, plus the turbo VSVs from 0.5 |
| 3.4 | **Outputs** | `W` F60-6 (low side), `ACMG` F59-13 (low side), `FPC` F60-5 (PWM), `REC` F59-25 + `REC2` F60-18 (PWM pair), `TACH` F59-20 if 0.2 says the cluster needs it |
| 3.5 | **Inputs** | `STA` F59-2, `STP` F59-6, `ST1-` F59-11 (inverted — pick one or wire both), `PRE` F59-21 / `PRE2` F59-12 with ground `EC` F60-22, `TH+`/`TH-` F59-18/22 as a differential pair, `LCKI` B1-29 if kept |
| 3.6 | **Delete** | all of plug **F84** (immobiliser) · plug **B3** except `VSV3` B3-12 and `FPU` B3-16 · the seven gear-position inputs · `SFTU` F59-4 / `SFTD` F59-14 · `SIL` F60-11 · `TC` F59-5 · `TRC±`/`ENG±` F60-13/20/14/21 · `MPX1`/`MPX2` F59-28/27 unless 2.1 chose the gateway |
| 3.7 | **Label and document** | every repinned wire recorded against this table | a marked-up copy lives in `../reference/` |

### Phase 4 — chassis and CD009

| # | Task | Detail |
|---|---|---|
| 4.1 | **Clutch interlock switch** | into the starter path where the A/T `PARK/NEUTRAL POSITION SW` P1 `P`/`N` terminals were, between ignition `ST2` and the starter relay (EWD356U p. 359). Feed it to an EMU input as well if you want clutch state |
| 4.2 | **Reverse lamps** | CD009 reverse switch — SPST, normally open, 2-wire, non-polarised — onto the terminals P1 4–8 used to close (EWD356U pp. 74–75) |
| 4.3 | **Speed pickup** | fit whatever 2.3 chose; set the EMU's pulses-per-revolution to match, and verify against GPS |
| 4.4 | **Cluster rewire** | per 2.1/2.2 — alternator L to the charge lamp, `MOPS` and `MOL` switches to their lamps, temperature gauge source |
| 4.5 | **Remove the dead hardware** | transponder key amplifier and coil, security indicator, shift-lock control ECU, A/T indicator, A/T shift main switch |

### Phase 5 — commission

| # | Task | Pass criterion |
|---|---|---|
| 5.1 | **DBW calibration and limp test** | throttle sweeps cleanly; deliberately unplug each position sensor and confirm the EMU limps rather than runs away |
| 5.2 | **Crank, no start** | main relay picks up and drops correctly; fuel pump commanded; no crank with the clutch up |
| 5.3 | **First start and idle** | idle held on the throttle plate across a cold-to-hot cycle |
| 5.4 | **Fans** | both PWM stages step with the radiator-tank sensor, not with engine-out temperature |
| 5.5 | **A/C** | clutch engages, drops out under load, pressure switches cut it |
| 5.6 | **Dash audit** | tach, speedo, fuel, temperature, charge, oil pressure, MIL — each checked and recorded as working, rewired, or deliberately dead |
| 5.7 | **Road test** | speed calibration against GPS; note which TRC/VSC lights are on and confirm ABS still functions |
