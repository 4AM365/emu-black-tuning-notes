# `gs300/reference/` — source documents

> **⛔ NOT THE SUPRA.** Every document here describes the GS300 (JZS160) or the JDM Aristo
> (JZS161). None of it applies to this repo's Supra, and no Supra document applies here.

Everything here was retrieved 2026-09-08 for Josh Napier's 2000 GS300 (JZS160) running a
JDM Aristo (JZS161) 2JZ-GTE VVT-i engine + factory Aristo ECU. See `../notes/my_car.md`.

| File | What it is | Pages | Text-searchable? |
|---|---|---:|---|
| `manuals/Lexus_GS300_JZS160_Workshop_Manual_1998-2005.pdf` | Toyota/Lexus factory repair manual **RM718U**, *2000 LEXUS GS300/GS400*. Chassis + body + **2JZ-GE** engine. | 1111 | yes (embedded text, some glyphs mangled) |
| `wiring/Lexus_1999_GS400_GS300_EWD356U.pdf` | Factory **Electrical Wiring Diagram EWD356U**, 1999 GS400/GS300 — body-side wiring bible. | 491 | yes |
| `wiring/JZS16x_Electrical_Wiring_Diagram_Book_6748505.pdf` | JDM Toyota **Aristo JZS16x** electrical wiring diagram book, part 6748505. | 129 | **no** — scanned images only |
| `wiring/SAE970297_Toyota_BEAN.pdf` | **SAE 970297**, *Toyota Body Electronics Area Network (BEAN)* — the protocol paper for the body multiplex bus the stock ECU sits on. Physical layer, frame format, arbitration. | 9 | yes (`sae970297_bean_text.txt`, OCR-grade — readable but scruffy) |
| `wiring/aristo_ecu_pinout_bee-mfg.pdf` | Aristo 2JZ-GTE VVT-i ECU pinout hand-out. **Verified to be a print of the same wilbo666 page** — convenient, but not independent corroboration. | 37 | yes |
| `wiring/aristo_2jzgte_vvti_pinout.md` | **Derived** — clean pinout tables for all six Aristo ECU plugs + the three engine↔body loom plugs. | — | — |
| `wiring/wilbo666_..._engine_wiring.txt` | Verbatim capture of wilbo666's Aristo wiring page, incl. per-pin What/Why/How prose. | — | yes |
| `*_text.txt` | Extracted plain text of the searchable PDFs, page-tagged `===== [name p.N] =====` for grepping. (No text file for the JZS16x book — it has none.) | — | — |

## Provenance

- GS300 workshop manual: Google Drive link posted by user *Thornton234* (2025-05-26) in the ClubLexus
  thread [GS300 Workshop Manual Link Here!](https://www.clublexus.com/forums/gs-2nd-gen-1998-2005/1040013-gs300-workshop-manual-link-here.html).
  That thread contains exactly one link; nothing else was posted there.
- EWD356U and the JZS16x diagram book: [wilbo666 PBworks](http://wilbo666.pbworks.com/).
- Aristo pinout text: [wilbo666 — 2JZ-GTE VVTi JZS161 Aristo Engine Wiring](http://wilbo666.pbworks.com/w/page/42173082/2JZ-GTE%20VVTi%20JZS161%20Aristo%20Engine%20Wiring),
  Plug/pin counts cross-checked against [shoarmateam](https://www.shoarmateam.nl/content/jzs161-engine-wiring/)
  and match exactly (B1 31, B2 24, F59 28, F60 22, F84 26; BF1 12, BF2 10, BF3 9).

### Known gaps

- RM718U here has **no DIAGNOSTICS (DI) section**. The ECM terminal-voltage table the SFI section
  points at ("INSPECT ECM, see page DI-20") is therefore **not in this copy** — still to be sourced.
- RM718U covers **2JZ-GE only**. It has zero 2JZ-GTE content; use the Aristo sources for the engine side.
- The JZS16x diagram book is image-only. Anything needed from it must be read off the page by eye.
- EWD356U is the **1999** book against a **2000** car — expect small year-to-year deltas.

## RM718U — section code → PDF page

| Code | Section | PDF pages | Book pages | Count |
|---|---|---|---|---:|
| `AC` | AIR CONDITIONING / AIR CONDITIONING SYSTEM | 1–96 | 1–96 | 95 |
| `AT` | AUTOMATIC TRANSMISSION / AUTOMATIC TRANSMISSION SYSTEM | 97–135 | 1–39 | 39 |
| `BE` | BODY ELECTRICAL / BODY ELECTRICAL SYSTEM | 136–386 | 1–251 | 231 |
| `BR` | BRAKE / BRAKE SYSTEM | 387–447 | 1–62 | 59 |
| `CH` | CHARGING (2JZ–GE) / CHARGING SYSTEM | 448–463 | 1–16 | 16 |
| `CO` | COOLING (2JZ–GE) / COOLANT | 464–497 | 1–34 | 34 |
| `EC` | EMISSION CONTROL (2JZ–GE) / EMISSION CONTROL SYSTEM | 498–512 | 1–15 | 15 |
| `EM` | ENGINE MECHANICAL (2JZ–GE) / CO/HC | 513–609 | 1–97 | 94 |
| `IN` | INTRODUCTION / HOW TO USE THIS MANUAL | 610–652 | 1–43 | 38 |
| `LU` | LUBRICATION (2JZ–GE) / OIL AND FILTER | 653–667 | 1–15 | 15 |
| `MA` | MAINTENANCE / OUTSIDE VEHICLE | 668–676 | 1–9 | 9 |
| `PP` | PREPARATION / MAINTENANCE | 677–748 | 1–104 | 67 |
| `PR` | PROPELLER SHAFT / TROUBLESHOOTING | 749–761 | 1–13 | 13 |
| `SS` | SERVICE SPECIFICATIONS / STANDARD BOLT | 762–809 | 1–67 | 42 |
| `SF` | SFI (2JZ–GE) / SFI SYSTEM | 810–881 | 1–72 | 70 |
| `ST` | STARTING (2JZ–GE) / STARTING SYSTEM | 882–898 | 1–17 | 17 |
| `SR` | STEERING / STEERING SYSTEM | 899–943 | 1–58 | 45 |
| `RS` | SUPPLEMENTAL RESTRAINT SYSTEM / SRS AIRBAG | 944–1013 | 1–70 | 68 |
| `SA` | SUSPENSION AND AXLE / TROUBLESHOOTING | 1014–1111 | 1–105 | 97 |

## EWD356U — PDF page map

Page titles as printed at the top of each sheet. Blank rows are continuation diagram sheets.

| PDF pages | Sheet title |
|---|---|
| 1 | NOTICE |
| 2 | A  INTRODUCTION |
| 3 | HOW TO USE THIS MANUAL  B |
| 7 | Pins used in the system circuit. |
| 8 | B  HOW TO USE THIS MANUAL |
| 10–11 | To Ignition SW |
| 14 | Retainer at |
| 15 | ∗ The titles given inside the components are the names of the terminals (termi |
| 16 | E  GLOSSARY OF TERMS AND SYMBOLS |
| 18–34 | F  RELAY LOCATIONS |
| 36–56 | G  ELECTRICAL WIRING ROUTING |
| 58 | AUTO ANTENNA |
| 59 | A35  AUTO ANTENNA CONTROL RELAY AND MOTOR |
| 60–66 | AUTOMATIC AIR CONDITIONING |
| 65–423 | : PARTS LOCATION |
| 67–425 | A A A |
| 68 | AUTOMATIC GLARE–RESISTANT EC MIRROR |
| 69 | I23  INNER MIRROR |
| 70–72 | AUTOMATIC LIGHT CONTROL |
| 73–370 | : GROUND POINTS |
| 74–76 | BACK–UP LIGHT |
| 75 | P1  BACK–UP LIGHT SW [PARK/NEUTRAL POSITION SW] |
| 78–80 | CELLULAR MOBILE TELEPHONE |
| 79 | TELEPHONE TRANSCEIVER AND SPEAKER RELAY |
| 82–84 | CHARGING |
| 83 | G1 (A), G2 (B)  GENERATOR |
| 86 | CIGARETTE LIGHTER AND POWER OUTLET |
| 87 | C10  CIGARETTE LIGHTER |
| 88 | CLOCK |
| 89 | C11  CLOCK |
| 90–96 | COMBINATION METER |
| 91 | * 1 : W/ DAYTIME RUNNING LIGHT |
| 93 | * 3 : 1UZ–FE |
| 95–398 | : CONNECTOR JOINING WIRE HARNESS AND WIRE HARNESS |
| 98–104 | CRUISE CONTROL (1UZ–FE) |
| 101–109 | The cruise control system is a constant vehicle speed controller in which cont |
| 106–112 | CRUISE CONTROL (2JZ–GE) |
| 114 | ELECTRIC TENSION REDUCER |
| 115 | B7  BUCKLE SW LH |
| 116–134 | ELECTRONICALLY CONTROLLED TRANSMISSION |
| 117–123 | AND A/T INDICATOR (1UZ–FE) |
| 127–133 | AND A/T INDICATOR (2JZ–GE) |
| 136–150 | ENGINE CONTROL (1UZ–FE) |
| 139 | (SHIELDED) |
| 145 | 2. CONTROL SYSTEM |
| 152–164 | ENGINE CONTROL (2JZ–GE) |
| 159 | The engine control system utilizes a microcomputer and maintains overall contr |
| 161–171 | EFI RELAY |
| 166–168 | ENGINE IMMOBILISER SYSTEM (1UZ–FE) |
| 170–172 | ENGINE IMMOBILISER SYSTEM (2JZ–GE) |
| 174 | FOG LIGHT |
| 175 | FOG RELAY |
| 176 | FUEL LID OPENER |
| 177 | F8  FUEL LID OPENER SW |
| 178 | GARAGE DOOR OPENER |
| 179 | G5  GARAGE DOOR OPENER |
| 180–184 | HEADLIGHT (w/ DAYTIME RUNNING LIGHT) |
| 183 | 1. DAYTIME RUNNING LIGHT OPERATION |
| 186–188 | HEADLIGHT (w/o DAYTIME RUNNING LIGHT) |
| 187 | 10A H–LP R UPR |
| 190–192 | HEADLIGHT BEAM LEVEL CONTROL |
| 194–196 | HEADLIGHT CLEANER |
| 199 | HORN RELAY |
| 200–204 | ILLUMINATION |
| 203 | TAIL RELAY |
| 206–216 | INTERIOR LIGHT |
| 213–382 | : RELAY BLOCKS |
| 218–222 | KEY REMINDER AND SEAT BELT WARNING |
| 221 | 1. SEAT BELT WARNING SYSTEM |
| 224–226 | LEXUS NAVIGATION SYSTEM |
| 227–309 | : SPLICE POINTS |
| 228–236 | LIGHT AUTO TURN OFF |
| 233 | This system automatically turns off the taillights and/or headlights when the  |
| 238 | LUGGAGE COMPARTMENT DOOR OPENER |
| 239 | L1  LUGGAGE COMPARTMENT DOOR OPENER SW |
| 240–244 | MOON ROOF |
| 243 | 6. KEY OFF MOON ROOF OPERATION |
| 246 | MULTIPLEX COMMUNICATION SYSTEM (COMMUNICATION BUS) |
| 247 | MULTIPLEX COMMUNICATION SYSTEM INCLUDES FOLLOWING SYSTEMS |
| 248–270 | MULTIPLEX COMMUNICATION SYSTEM |
| 263 | 1. COMMUNICATION OUTLINE |
| 265–415 | : JUNCTION BLOCK AND WIRE HARNESS CONNECTOR |
| 272–282 | POWER SEAT (DRIVER’S SEAT w/ DRIVING POSITION MEMORY) |
| 279 | P18 (A), P19 (B)  POWER SEAT ECU |
| 284 | POWER SEAT (DRIVER’S SEAT w/o DRIVING POSITION MEMORY) |
| 285 | P16  POWER SEAT CONTROL SW (DRIVER’S SEAT) |
| 286 | POWER SEAT (FRONT PASSENGER’S SEAT) |
| 287 | P17  POWER SEAT CONTROL SW (FRONT PASSENGER’S SEAT) |
| 288–290 | POWER SOURCE |
| 292–296 | POWER TILT AND POWER TELESCOPIC |
| 295 | This system provides the automatic tilt and telescopic mechanisms using the mo |
| 298–310 | POWER WINDOW |
| 307 | B6  BODY ECU NO.2 |
| 313 | PPS ECU (Flow rate control system) controls the solenoid valves mounted in the |
| 316–318 | RADIATOR FAN AND CONDENSER FAN |
| 320–322 | RADIO AND PLAYER (EXCEPT NAKAMICHI) |
| 324–326 | RADIO AND PLAYER (NAKAMICHI) |
| 325 | D/A CONVERTER |
| 327 | 1 2 X |
| 328–330 | REAR WINDOW DEFOGGER AND MIRROR HEATER |
| 332–338 | REMOTE CONTROL MIRROR |
| 340–342 | SEAT HEATER |
| 341 | S3  SEAT HEATER SW |
| 344–346 | SHIFT LOCK |
| 345 | 1. SHIFT LOCK MECHANISM |
| 355–357 | STARTING AND IGNITION (1UZ–FE) |
| 359–361 | STARTING AND IGNITION (2JZ–GE) |
| 363–365 | STOP LIGHT |
| 367–371 | TAILLIGHT |
| 373–385 | THEFT DETERRENT AND DOOR LOCK CONTROL |
| 380 | 1. MANUAL UNLOCK OPERATION |
| 387–389 | TURN SIGNAL AND HAZARD WARNING LIGHT |
| 388 | T7  TURN SIGNAL FLASHER |
| 394 | FROM POWER SOURCE SYSTEM (SEE PAGE 60) |
| 396 | 1. ABS OPERATION |
| 400 |     C C |
| 402–404 | WIPER AND WASHER |
| 403 | With the ignition SW turned on, the current flows to TERMINAL 17 of the front  |
| 406–416 | WIRELESS DOOR LOCK CONTROL |
| 413 | In this system, the wireless door lock ECU receives weak radio wave transmitte |
| 417 | X X X    X  |
| 418–424 | I  GROUND POINT |
| 419 | FRONT TURN SIGNAL |
| 421 | HIGH MOUNTED |
| 426–478 | J  OVERALL ELECTRICAL WIRING DIAGRAM |
| 428 | SYSTEM INDEX |
| 480–486 | K  POWER SOURCE (Current Flow Chart) |
| 488–490 | L  PART NUMBER OF CONNECTORS |
