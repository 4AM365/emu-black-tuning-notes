# Car identity — Josh Napier's GS300

> ## ⛔ THIS IS NOT THE SUPRA. DO NOT CROSS-REFERENCE.
>
> This repository's main subject is a **MKIV Supra**. **This car has nothing to do with it.**
> This is Josh Napier's **2000 Lexus GS300 (JZS160)** with a **JDM Aristo (JZS161) 2JZ-GTE VVT-i**
> and a **CD009** gearbox. Different chassis, different body electronics, different engine
> variant, different throttle body, different pedal, different gearbox, different owner.
>
> Never carry a value, table, calibration constant, pin, sensor trace, hardware part or conclusion
> between this car and the Supra notes (`../../supra/`, `../../notes/`) in **either** direction —
> not as a starting point, not as a sanity check, not "for reference." Never load the
> `supra-specs` skill for a question about this car. They share an engine *family* and an ECU
> *brand*; that is the entire overlap, and same-family is not same-part. If a fact cannot be
> sourced from [`../reference/`](../reference/README.md) or from Josh, it is **unverified** — say
> so rather than reaching across.
>
> **Exception (Will, 2026-09-15, for the v3 import):** three categories may be seeded from the
> Supra tune — **lambda target tables, ignition maps, PID settings** — because they describe the
> shared 2JZ-GTE VVT-i plant rather than this car's hardware. Which specific symbols qualify, and
> which PIDs do *not* (idle-airflow, DBW motor), is worked out in
> [`v3_import_gap_list.md`](v3_import_gap_list.md). Everything else stays under the rule above.


Established 2026-09-08. This is the identity card for the `gs300` / `napier` vehicle in this
repo. Everything below is either **stated by Will**, **read out of a source document in
`../reference/`**, or explicitly marked **unverified**. Nothing here is assumed from a
generic build.

## Stated

| | |
|---|---|
| Owner | Josh Napier |
| Vehicle | 2000 Lexus GS300 |
| Engine | 2JZ-GTE VVT-i, JDM Aristo |
| Engine ECU | factory JDM Aristo ECU (being removed) |
| Aftermarket ECU | ECUMaster EMU Black, **v3 firmware**, currently piggyback |
| Transmission | **CD009** (Nissan 350Z/G35 6-speed manual) — swapped from the factory automatic |

## What that resolves to

**Chassis — Lexus GS300, 2nd gen (1998–2005).** Toyota chassis code **JZS160**; the V8
GS400 sibling is UZS160/161. Factory engine for this chassis is the **2JZ-GE** (NA,
non-VVT-i on early cars, VVT-i on 2JZ-GE from 1998). The factory service manual for the
exact model year is in hand: **RM718U, *2000 LEXUS GS300/GS400***, 1111 pages.

**Engine — 2JZ-GTE VVT-i out of a JDM Toyota Aristo.** Chassis code **JZS161** (the
1997–2004 twin-turbo Aristo; the earlier 1991–1997 Aristo is JZS147 with the non-VVT-i
2JZ-GTE, and that is a *different* engine and a *different* loom — do not mix the two
sources up). JZS161 is the JDM twin of the GS300's own body, so a lot of the chassis
hardware lines up even though the engine and its electronics do not.

**Engine ECU.** Two Toyota part numbers exist for the JZS161 automatic:

| Toyota P/N | Fitted | Immobiliser |
|---|---|---|
| 89661-3A470 | 08/1997 – 06/2000 | none in the ECU |
| 89666-30180 | 07/2000 – 12/2004 | **engine immobiliser built into the ECU** |

Which one Josh has is **unverified** and it matters: the later ECU will not run without its
matched transponder/immobiliser, and the GS300 has its own separate immobiliser system
(EWD356U pdf pp. 166–173). Read the number off the ECU case before planning any start-up
wiring.

## The wiring problem, stated plainly

Two looms and two ECUs that were never meant to meet:

- The **Aristo engine ECU** expects a JZS161 body — it wants A/T control, ABS/TRC/VSC
  differential serial (`TRC+`/`TRC-`, `ENG+`/`ENG-`), a tach output, an A/C request and
  amplifier, starter and EFI-relay control, and an immobiliser handshake on plug F84.
  Full pin-by-pin in [`../reference/wiring/aristo_2jzgte_vvti_pinout.md`](../reference/wiring/aristo_2jzgte_vvti_pinout.md).
- The **GS300 body** offers the JZS160 versions of those same services, on different pins,
  through different connectors, to a 2JZ-GE ECM. Its side is documented in EWD356U.

Six Aristo ECU plugs, 147 pins total:

| Plug | Pins | What lives there |
|---|---:|---|
| B1 | 31 | injector drivers `#10`–`#60`, `IGT` ignition triggers, crank `NE+`, cam position |
| B2 | 24 | `PIM` MAP, `THW` coolant temp, `VTA` TPS, knock, O2, sensor supplies |
| B3 | 17 | **automatic transmission** — shift solenoids `S1` `S2` `S4` `SD`, linear solenoids `SLU±` `SLN±` `SLT±`, `NCO±` OD direct-clutch speed, `SP2±` speed, `OIL` ATF temp; plus `VSV3` exhaust bypass and `FPU` fuel-pressure-up VSV |
| F59 | 28 | **body interface** — `STA` starter, `STP` stop light, `ST1-` brake, `ACMG` A/C clutch relay, `PRE`/`PRE2` A/C pressure, `CCS` cruise, `TACH`, `TAM` ambient temp, `REC` fan, `P`/`R`/`D`/`3` gear-position indicators, `SFTU`/`SFTD` shift up/down, `TC` test connector, `MPX1`/`MPX2` multiplex to body computer and A/C ECU |
| F60 | 22 | `BATT`, `IGSW`, `M-REL` EFI main relay, `+B`, `SIL` (ISO 9141-2 K-line OBDII), `TRC±`/`ENG±` ABS-TRC-VSC serial, `NEO` slave engine-speed out |
| F84 | 26 | **immobiliser only**, 5 live pins — `EOM` ground, `KSW` key inserted, `IMLD` LED, `TXCT`/`RXCK`/`CODE` to the key amplifier. Everything else on this plug is unused. |

Worth saying out loud: **the Aristo ECU is a combined engine + ECT controller.** Plug B3 is
nothing but automatic-transmission actuators and sensors — it drives the shift solenoids
and the line-pressure/lock-up linear solenoids directly. There is no separate A/T ECU on
the Aristo side. That makes the transmission question below structural, not a detail.

Engine loom to body loom crosses three white Toyota connectors:
**90980-11531** (BF1, 12-pin), **90980-11527** (BF2, 10-pin), **90980-11710** (BF3, 9-pin).

## Unverified / to confirm with Josh

1. **Which cluster and body harness are fitted** — GS300 (JZS160) or Aristo (JZS161)?
   Decides where the tachometer signal comes from and which multiplex node map applies.
2. **What the EMU Black already owns on the piggyback** — injectors, coils, crank/cam,
   knock, MAP, wideband? Knowing the current split avoids repinning anything twice. Note the
   EMU source folder for this car is V1-only (`EMU_BLACK\Napier_GS300`, checked
   2026-09-08) while the car runs **v3 firmware**, so that folder is historical.
3. **Sequential turbo state** — still sequential, true-twin, or single-turbo? Determines how
   many of the factory boost-control VSVs the EMU needs to drive.
4. **Which harness is physically in the car** — Aristo engine loom spliced to GS300 body
   loom, a fully rewired standalone, or something in between.

The immobiliser is **not** an open question: it is being deleted with the stock ECU.

## See also

- [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) — full map of what the
  stock ECU provides, signal by signal, and what happens to each when it comes out.

## Sources

All in [`../reference/`](../reference/), with per-page indexes in
[`../reference/README.md`](../reference/README.md):

| Side | Document | Note |
|---|---|---|
| Chassis | `manuals/Lexus_GS300_JZS160_Workshop_Manual_1998-2005.pdf` (RM718U) | 2JZ-GE only, and **missing the DIAGNOSTICS (DI) section** — so the ECM terminal-voltage table it points at (DI-20) is not in this copy |
| Chassis | `wiring/Lexus_1999_GS400_GS300_EWD356U.pdf` | factory EWD, text-searchable. 2JZ-GE engine control = pdf pp. 152–165; immobiliser 166–173; starting 355–362; theft deterrent 373–386 |
| Engine | `wiring/aristo_2jzgte_vvti_pinout.md` | derived clean tables |
| Engine | `wiring/wilbo666_2jzgte_vvti_jzs161_aristo_engine_wiring.txt` | verbatim, with per-pin What/Why/How prose |
| Engine | `wiring/JZS16x_Electrical_Wiring_Diagram_Book_6748505.pdf` | JDM Aristo factory diagram book — **scanned images, not searchable** |
| Engine | `wiring/aristo_ecu_pinout_bee-mfg.pdf` | second-source pinout hand-out |

EMU source folder for this car, per `../../EMU_SOURCE_INDEX.md`:
`C:\Users\WTCra\OneDrive\Documents\EMU_BLACK\Napier_GS300` (V1 tree only — there is no
`EMU_BLACK_V3\Napier_GS300`).
