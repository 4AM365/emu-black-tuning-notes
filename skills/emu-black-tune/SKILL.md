---
name: emu-black-tune
description: >-
  Reads, interprets, and edits EMU Black ECU tune files exported as XML
  (.emub3 / .xml). Use this whenever the user references, opens, or wants to
  change a tune/calibration FILE (not a data log) — symbols, scalars, tables,
  axis bins, DBW/airflow targets, idle, cranking, ignition, fuel, boost, VVT.
  Trigger on phrases like "tune file", "calibration", ".emub3", "xml export of
  my tune", "armed airflow table", "rescale the airflow values", "what does
  symbol X mean", "change the actuator range", or any request to read or modify
  values inside an EMU Black project export. Distinct from emu-black-log (which
  reads CSV data logs) and supra-specs (the vehicle build reference) — reach for
  THIS skill when the artifact is the tune itself. Always read this before
  hand-editing an .emub3 so the hex encoding and scaling are applied correctly.
---

# EMU Black Tune File Interpreter

EMU Black (and EMU Classic) stores a tune as an XML project export, usually named
`*.emub3` or `*.xml`. This skill explains the file format, the per-symbol
scaling conventions (the part that bites people), and how to read or rewrite
values safely — including the DBW airflow→TPS calibration and how to rescale
airflow tables when the actuator range changes.

## When to use vs. sibling skills

- **This skill** — the artifact is the *tune/calibration file* (.emub3/.xml). Reading symbols, decoding tables, editing values, rescaling.
- **emu-black-log** — the artifact is a *data log* CSV (semicolon-delimited, TIME column, live channels).
- **supra-specs / fj80-specs** — the *vehicle build reference* (hardware, targets, history). Read those for build context; read this for file mechanics.

For a build-specific edit you will often use this skill **with** the matching specs skill.

## File anatomy

```xml
<project version="3.059">
  <variables>
    <symbol name="..." value="..."  storage="word"  type="value"/>     <!-- scalar -->
    <symbol name="..." storage="ubyte" width="8" height="5" data="..."/> <!-- table  -->
  </variables>
  <tables>
    <symbol name="..." storage="word" width="16" height="1" data="..."/> <!-- axis bins / tables -->
  </tables>
</project>
```

- **Scalars** carry a `value` attribute. **Tables** carry `width`, `height`, and a `data` attribute.
- **`data` is space-separated HEX**, no `0x` prefix. `data="30 3F 4D"` = decimal 48, 63, 77.
- Tables are **row-major**: `width` = columns (usually the X axis), `height` = rows (usually the Y axis). A `width=8 height=5` table is 40 values, first 8 = row 0, next 8 = row 1, etc.
- The matching axis bins are separate symbols (e.g. `rpmBins`, `mapBins`, `cltBins8`, `tpsBins`). Bins are also hex and also scaled.
- Two checksums live near the top: `variablesChecksum` and `tablesChecksum`. **Editing `data`/`value` makes these stale** — see Safety below.

## Storage types

| storage | bytes | signed | raw range |
|---------|-------|--------|-----------|
| `ubyte` | 1 | no  | 0..255 |
| `sbyte` | 1 | yes | -128..127 |
| `word`  | 2 | no  | 0..65535 |
| `sword` | 2 | yes | -32768..32767 |
| `u12`   | — | no  | 12-bit packed value |

Signed values appear in hex with a leading `-` in the export (e.g. `sbyte` `-4B` = -75). Storage size constrains what a rescaled value may be (a `ubyte` cannot exceed 255).

## Scaling conventions (READ THIS BEFORE EDITING)

**Scaling is defined by EMU Black firmware, not by the XML.** The raw integer in `data` is *not* the displayed number. The conventions below are derived from this platform's exports and cross-checked against documented behavior, but **the authoritative check is always: open the cell in EMU software and compare the displayed value to `raw × scale`.** If they disagree, trust EMU and back out the real scale before writing anything.

| Quantity | storage | scale (display = raw × …) | notes |
|----------|---------|---------------------------|-------|
| TPS / pedal % | word | 0.1 | `tpsBins` 0x3E8=1000 → 100.0% |
| Airflow % axis (bins) | word | 0.1 | `airflowBins4` 0x44C=1100 → 110.0% |
| **Airflow-% target tables** | **ubyte** | **0.5** | idle/armed/cranking DBW targets. `idleActiveAirflow` 0x5A=90 → 45% (matches ~45% warm idle) |
| RPM | word | 1 | `rpmBins` 0x3E8=1000 → 1000 rpm |
| MAP / boost (kPa) | word | 1 | `mapBins` 0x14=20 → 20 kPa |
| Coolant/IAT (°C) | sword | 1 | `cltBins8` may be offset; verify |
| Mass airflow (g/s) | word | 0.1 | `fuelPumpAirflowBins` 0xBB8=3000 → 300 g/s — **mass, not %** |
| Ignition (°) | sbyte | 1 | crank advance |
| Lambda | ubyte | /100 or table-specific | verify against EMU |

**The single biggest trap:** the word "airflow" is used for two unrelated things —
(1) **DBW airflow %** (a throttle-plate target, 0–~110%) and
(2) **mass airflow g/s** (sensor/fuel-pump axes). They scale differently and must never be mixed. Check the symbol's role before assuming `%`.

When a value exceeds 100 as a raw byte (e.g. an airflow-% table maxing at 0xA9=169), that is a strong signal the scale is **not** 1:1 — here 169 × 0.5 = 84.5%.

**Verified:** the ubyte airflow-% scale of 0.5/count (raw = 2 × displayed %) was confirmed two ways on this build — (1) decoding `idleActiveAirflow` row-by-row matched the EMU screenshot exactly (`71 65 4B 27 …` ×0.5 = `56.5 50.5 37.5 19.5 …`, the 1000-rpm row), and (2) the cross-check below.

### Cross-checking encoding against the tune file (do this before trusting a scale)

A single-table `.emubt` and the full `.emub3` project store the **same raw hex** for
the same symbol. So the cheapest way to confirm your decode is anchored to reality:
extract a symbol's `storage`/`width`/`height`/`data` from both files and compare.

- **Identical raw `data` + matching `storage`/dims** → the `.emubt` faithfully
  represents the tune, and whatever scale reproduces the EMU display is correct for both.
- **Same dims but different `data`** → a *content* difference, not an encoding one.
  A `.emubt` is often a **newer edit** than a given project export (check file mtimes),
  so confirm which baseline is current before computing a rescale off it.

On this build the cross-check showed `idleActiveAirflow`, `idleArmedAirFlow`, and
`idleCustomCorrection` byte-identical between `.emubt` and `.emub3`; only
`idleCrankingDC` differed (tune `25 25 25 25` = flat 18.5%, vs a later tapered
`.emubt` `28 27 26 25` = 20.0/19.5/19.0/18.5%).

## Reading a value — worked example

`idleArmedAirFlow`, `storage="ubyte"`, `data="30 3F 4D 57 5F 65 6B 6C"`:

1. Hex → dec: 48, 63, 77, 87, 95, 101, 107, 108
2. Apply ubyte airflow-% scale (×0.5): 24%, 31.5%, 38.5%, 43.5%, 47.5%, 50.5%, 53.5%, 54%
3. These are DBW airflow targets across the armed-state RPM bins.

To go from a displayed % back to the byte you'd write: `raw = round(display% / 0.5)`.

## DBW airflow ↔ TPS calibration

On a DBW EMU Black setup, the airflow-% target is converted to an actual throttle
position through a linear **actuator control range** `[floor, ceiling]` expressed in TPS %:

```
TPS%     = floor + (airflow% / 100) × (ceiling − floor)
airflow% = (TPS% − floor) / (ceiling − floor) × 100
```

So `airflow%` is literally "percent of the control range." Changing `floor` or
`ceiling` reinterprets **every** stored airflow-% value against the new range —
the plate moves even though the tables are untouched. To keep the engine behaving
the same after a range change, you must **rescale** the airflow-% tables.

### Rescaling procedure when the range changes

Given old range `[f_old, c]` → new range `[f_new, c]` (ceiling usually unchanged):

To **preserve the actual TPS** of every cell, convert each airflow-% value:

```
new% = ( f_old − f_new + old% × (c − f_old)/100 ) / (c − f_new) × 100
```

This is linear: `new% = A + B × old%`, where
`B = (c − f_old)/(c − f_new)` and `A = (f_old − f_new)/(c − f_new) × 100`.

In **raw bytes** (ubyte airflow tables, scale 0.5), the slope `B` is unchanged and
the offset becomes `A/0.5`: `new_raw = A/0.5 + B × old_raw`.

**A value you deliberately want at a specific TPS** (e.g. cranking) is *not*
preserved — set it directly: `new% = (TPS_target − f_new)/(c − f_new) × 100`.

**Additive / delta tables scale differently — no offset.** An *additive* airflow-%
correction (e.g. `idleCustomCorrection`, "Custom air flow correction [%]") is added
to the target before the airflow→TPS conversion, so its real effect is
`ΔTPS = correction% /100 × width`. Only the **width ratio** matters; the floor shift
cancels for a difference. To preserve a correction's effect:
`new = old × (c_old−f_old)/(c_new−f_new)` — slope `B`, **offset zero**. Widening the
range without this scaling would multiply every correction's effect. (If you instead
convert the table to a multiplicative/scalar mode in EMU, do NOT width-scale — a
multiplier is dimensionless and range-independent. Pick one, never both.)

### Worked example (this build's actuator-range change)

**Read the CURRENT range from `idleDBWTargetMin/Max`, do not infer it from history.**
On this build the original range was `[2.0, 6.4]`, but by the time of the change the
range was already `[3.5, 8.0]` (`idleDBWTargetMin=35`, `idleDBWTargetMax=80`) — the
ceiling had been raised to 8.0 during idle setup. The change moved only the floor:
`[3.5, 8.0] → [2.4, 8.0]`. So `f_old=3.5, c_old=8.0, f_new=2.4, c_new=8.0`, width
4.5 → 5.6.
- `B = (c_old−f_old)/(c_new−f_new) = 4.5/5.6 = 0.803571`
- `A% = (f_old−f_new)/(c_new−f_new)×100 = 1.1/5.6×100 = 19.6429`
- Preserve-TPS rule (display %): **`new% = 19.6429 + 0.803571 × old%`**
- In raw ubyte (×0.5): **`new_raw = 39.2857 + 0.803571 × old_raw`**, round, clamp 0–255.
- Sanity: old 0% → 19.64% (still 3.5% TPS); old at 8.0% TPS → still 8.0% TPS. ✓
- **Cranking exception** — not preserve-TPS. Reproduce the original `[2.0,6.4]`
  cold-crank taper 25.5→24.0% (= TPS 3.122→3.056), then express in the NEW range:
  `new% = (TPS−f_new)/(c_new−f_new)×100`. Cold `(3.122−2.4)/5.6×100 = 12.89%`
  → raw 26 (0.5/count). Result `26 25 24 23` = 13.0/12.5/12.0/11.5%.

**Cautionary tale:** the first pass here assumed the ceiling was still the *original*
6.4 and got slope 0.5179 — wrong by ~0.4% TPS at idle (a stall risk). The current
ceiling lives in `idleDBWTargetMax`; always read it before computing. Recompute
`A`/`B` for the actual ranges every time; never reuse stale constants.

## Symbol glossary (DBW / idle / cranking / airflow domain)

Names are stable across exports. `*Bins` = axis for the table of the same root.

| symbol | meaning |
|--------|---------|
| `idleActiveAirflow` | EMU "Airflow - Active state air flow [%]". Closed-loop idle airflow target, ubyte 8×5 = CLT (X) × idle-target RPM (Y); data rows run **low→high RPM** (row 0 = lowest) |
| `idleArmedAirFlow` | EMU "Airflow - Armed state air flow [%]". Armed-state airflow target (pedal released, pre-PID), ubyte 8×1 vs RPM |
| `idleCustomCorrection` | EMU "Airflow - Custom air flow correction [%]". sbyte 5×5 (signed). Was an **additive** correction on this build; being converted to a scalar/multiplier — confirm its mode before rescaling |
| `idleCrankingDC` | EMU title "Cranking airflow [%]". Airflow-% target vs CLT, 4 bins on `cltBins4` = `0/33/67/100 °C`, so **bin 0 = coldest**. (Despite "DC" in the name it is airflow-%, not a duty cycle, on a DBW setup.) |
| `cyclingIdleAirflow` | airflow target during cycling-idle (anti-stall) mode |
| `idleDBWTargetMin/Max` | **the Airflow-Actuator range** (TPS %, word @ 0.1/count). `idleDBWTargetMin=35`→3.5% floor, `idleDBWTargetMax=80`→8.0% ceiling. This is the `[floor, ceiling]` that all airflow-% values map into — the symbols to read to learn the CURRENT range, and to edit when changing it (floor 2.4% = `24`). Do **not** assume the ceiling from history; read it here. |
| `idleDBWBlendPoint`, `idleDBWBlendPointTbl` | PID/feed-forward blend |
| `overrunDBW`, `overrunDBW2` | decel/overrun throttle target |
| `lcDBWTargetTable`, `lcPrestageDBWTarget` | launch-control airflow targets |
| `alsDBWTarget`, `alsDBWTarget2` | anti-lag throttle targets |
| `ralDBWTarget`, `pitLimiterDBWLimit`, `dbwBoostTargetLimit` | rolling-AL / pit-limiter / boost-limited throttle |
| `dbwCharacteristic1/2` | pedal→target maps (PPS × something) |
| `dbwMinDC`/`dbwMaxDC`/`dbwMaxCurrent` | motor drive limits (not airflow %) |
| `tpsMin`/`tpsMax` | TPS *sensor* ADC calibration (closed/WOT), **not** the airflow range |
| `crankingCorrTbl`, `crankingCorrTbl2` | cranking fuel correction (CLT × TPS) |
| `tblsFFCrankingBlend` | flex-fuel blend for cranking tables |

When asked "which symbols are airflow %", the core start/idle group is
`idleActiveAirflow`, `idleArmedAirFlow`, `idleCrankingDC`, `cyclingIdleAirflow`;
the next ring out adds `overrunDBW`/`overrunDBW2`; the broadest set adds the
launch/ALS/pit/rolling-AL/boost-limit DBW targets. Confirm scope with the user —
limit tables (e.g. `dbwBoostTargetLimit`, `dbwCLTLimitTable`) are caps, not idle
targets, and may not want the same remap.

## Safety before any edit

1. **Confirm the scale empirically.** Pick one cell, compute `raw × scale`, and
   ask the user what EMU shows. One mismatch means every offset you write is wrong.
2. **Checksums go stale.** `variablesChecksum`/`tablesChecksum` will no longer
   match after you edit `data`. EMU Black normally recomputes on import, but
   confirm the user's workflow accepts a hand-edited file rather than rejecting it.
3. **Respect storage limits.** Clamp/round results to the type's range; never let
   a `ubyte` exceed 255 or write a fraction where the type is integer.
4. **Work on a copy**, keep the original export, and have the user re-verify a few
   representative cells in EMU after import before the engine is started.
5. **This is a real engine.** Cranking, idle, and DBW limits affect start and
   runaway behavior. Get explicit confirmation of scope and scale before rewriting.

## Editing mechanics

Edit the `data` string in place (it's plain hex in the XML). Convert
display → raw, format as uppercase hex without `0x`, preserve the count and order
(row-major). Keep the trailing space style consistent with the surrounding file.
