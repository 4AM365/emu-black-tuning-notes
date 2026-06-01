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

## Table rendering convention (when displaying tables in chat)

When you render a 2D tune table in markdown for the user to read, the **presentation orientation** is independent of the raw byte order in storage:

- **Y-axis high values at the top.** Highest RPM (or whatever Y-axis quantity) is the first data row in the markdown table, lowest at the bottom. Matches the EMU software UI and standard chart convention. The underlying `data` byte order (row 0 = lowest Y bin) is for editing the file, not for display.
- **Multiplicative / scalar correction tables**: present cells as percent deltas (`+2%`, `0%`, `-8%`) the way EMU shows them in scalar mode. Do not render the raw multiplier (`1.02`, `0.92`) in chat.
- **Additive correction tables**: present cells in their native displayed unit (e.g. `+1.0 %`, `-5.0 %` of airflow), not the raw signed byte.

Internal calculations may keep the natural raw orientation; flip before printing the final table.

## Ingesting a table from a screenshot (paste-a-map workflow)

The user can **paste a screenshot of a map** straight from the EMU software instead of
(or before) sending the tune file. Read the grid directly from the image and, critically,
**read the little tabs in the bottom-right corner of the table editor** — those tabs
identify *which table* the screenshot is (the table-set / table selector, e.g. VE table 1
vs VE table 2, or table Set 1/2/3). Recognizing them is what lets you map the picture to
the correct tune **symbol** and edit the right thing.

Workflow:

1. **Read the bottom-right tabs** to identify the table and its set. That tells you the
   target symbol (e.g. `veTable` vs `veTable2`, or which table set's instance) — do not
   guess from the values alone; the tabs are the ground truth for *which* table this is.
2. **OCR the grid** into a 2D array, plus the axis bins (RPM along one edge, load/MAP along
   the other). Confirm orientation against the rendering convention above (Y-axis high at
   top in the EMU UI; remember `data` byte order is row 0 = lowest Y bin when you write back).
3. **Map to the symbol** and apply the scaling for that table family (see the scaling table
   below) before computing any edit.
4. **Edit the tune to fit** — alter that symbol's `data`, fix the checksums, and export.

This is the same recognition step that previously let a pasted VE-map screenshot (identified
by its bottom-right tabs) be matched to the right symbol and written back into the tune. For
*smoothing* a pasted map rather than transcribing it, hand off to **emu-black-ve-smooth**
(which also accepts a pasted/screenshotted grid).

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
| **Airflow-% scalar corrections** (single value, not table) | **ubyte** | **1** (direct %) | `idleCoolantFanCorr` raw 13 → +13 % airflow when fan output active. Despite being in the airflow domain, single-value scalars often use scale=1 rather than the 0.5/count convention of the multi-cell target tables. **Verify per symbol — do not assume 0.5 just because the symbol is in the airflow %  family.** |
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

### Converting an additive correction table to a multiplicative (scalar) one

**RULE: NO GUESSING.** When the user asks you to convert a table from additive to scalar (or any other table transformation that requires per-cell math), do the per-cell calculation explicitly and show the back-calculated table FIRST before proposing any trim or simplification. Do not anchor the multiplier to a single reference base and eyeball the rest of the rows. The right output is two tables: (1) the faithful back-calculation, (2) optionally the trimmed/safer version with the trim shown as a deliberate edit on top of the faithful values.

### Custom correction — what the scalar actually scales (per EMU help)

EMU's help for the "Custom correction" `Correction type` parameter:
> **Scale** — The value from the Custom air flow correction table scales the **calculated DC value**.
> **Add** — The value from the Custom air flow correction table is added to the calculated DC value.

"Calculated DC value" = the **already-summed open-loop airflow command** before PID. This includes the base airflow PLUS any other additive corrections that have been folded in (fan compensation, DSG torque comp, etc.) — not just the base. On a DBW build, the EMU vocabulary "DC" is historical (from PWM solenoid days); on DBW it's the airflow-% command that then maps to a TPS target via the actuator floor/ceiling.

The full effective formula on a DBW build in scalar mode:

```
Idle air %  =  ( idleActiveAirflow[CLT, idle_target]
                + idleCoolantFanCorr  (when fan output active)
                + idleDSGTorqueCorr[load]
                + ... other open-loop corrections
              )  × idleCustomCorrection_mult[X, Y]
              + idleAirFlowPID
```

**Practical consequence:** the custom-corr scalar shrinks (or grows) every layered open-loop correction at the same proportion as the base. A fan correction of +6.5 % airflow at a CAT 70 / mult-0.72 cell delivers only +4.7 % effective. If you size additive corrections (like `idleCoolantFanCorr`) without remembering they'll be scaled by the custom-corr multiplier, you'll under-deliver at the cells where the multiplier is most negative.

**Lesson learned (2026-05-26):** initial reading missed this — I assumed the scalar only multiplied the base and that fan was added after. The EMU help "scales the calculated DC value" makes it clear the scalar applies to the sum. Re-read EMU help precisely before assuming a calculation order.

When EMU's custom correction table is switched from additive (sbyte, direct % delta) to scalar (multiplier displayed as % delta from 1.00), the **storage scaling changes**. Do not assume the raw bytes carry the same meaning across modes. To convert faithfully:

1. **Look up the base airflow** at each correction cell. For `idleCustomCorrection` the base is `idleActiveAirflow[CLT_warm, idle_target_RPM]` — the warm-CLT row of the active-airflow table at the idle-target-RPM that the correction cell is keyed to. **Use a single reference CLT (typically the operating CLT, e.g. 96 °C)** so the conversion is well-defined.
2. **Apply the additive correction** to get effective absolute airflow: `effective = base + additive_corr_%`.
3. **Back-calculate the multiplier**: `mult = effective / base`. Express as % delta for the EMU UI: `mult_%_delta = (mult − 1) × 100`.
4. **Verify the corner cells make physical sense.** If a multiplier comes out near 0 (or negative), the original additive table was already commanding stall conditions in that cell; the new scalar should be sized for safety (e.g. floor at -50 % delta = mult 0.5), not faithfully reproduced. Note the change.
5. **Then apply any intentional trim** (e.g. halve depth per the [conservative feed-forward principle](C:\Code\car-projects\emu-black-tuning-notes\notes\idle_stall.md)) on top of the faithful conversion, not in place of it.

**Why this matters:** the conversion is non-linear across the table because each cell's reference base is different. A -10 % additive correction means a *-22 % multiplier* at a 45 % base row (1500 rpm warm CLT) but a *-61 % multiplier* at a 16.5 % base row (1000 rpm warm CLT). Designing the scalar table by eye against a single reference base — instead of cell-by-cell — silently flattens the correction curve and misses the stall-margin cells.

**Lesson learned (2026-05-26 conversion of `idleCustomCorrection`)**: the first-pass scalar proposal was anchored to one reference RPM and the other rows were eyeballed. The faithful back-calc showed the original additive table was commanding ≤0 % absolute airflow in two low-RPM × high-CAT cells (idle target 1000-1100 rpm × CAT 70). The scalar conversion is the right opportunity to fix that, but only if you run the per-cell math first and *then* decide how aggressively to trim.

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
| `idleActiveAirflow` | EMU "Airflow - Active state air flow [%]". Closed-loop idle airflow target. **8 cols × 5 rows = 40 cells**. X = "Coolant Temp. (°C)" (`cltBins8` = 0/15/30/45/60/75/96/105 on this build). Y = "Idle target (RPM)" (1000/1100/1200/1375/1500 on this build) — keyed on idle TARGET, not actual engine RPM. ubyte ×0.5/count. Raw `data` rows run low→high RPM (row 0 = 1000 rpm); EMU UI shows high RPM at top — flip when rendering. |
| `idleArmedAirFlow` | EMU "Airflow - Armed state air flow [%]". Armed-state airflow target (pedal released, pre-PID), ubyte 8×1 vs RPM |
| `idleCustomCorrection` | EMU "Airflow - Custom air flow correction [%]". **5 cols × 5 rows = 25 cells**. **X axis is IAT/CAT (charge-air temp), NOT CLT** — `idleCustomCorrX` bins on this build are 20/30/40/50/70 °C — used for heat-soak airflow compensation. **Y axis is "Idle target (RPM)"** (`idleCustomCorrY` = 1000/1100/1200/1375/1500 rpm) — lookup is on the current idle-target value, NOT actual engine RPM. As of 05/26/2026 build was switched from **additive** (sbyte direct %) to **scalar/multiplicative** mode (displayed as % delta in EMU UI; +2 % = mult 1.02, -28 % = mult 0.72). Confirm mode before rescaling — additive and scalar use different storage scales. |
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

## Cold start fuel parameters

### File format gotcha: binary vs. XML `.emub3`

`.emub3` files come in two flavours. Check before grepping:
- **Binary (ZIP)** — starts with `PK` bytes. Not human-readable. These are the EMU software project files (e.g. `Supra Tune 05242026.emub3`, `supra ai corrected 05242026.emub3`).
- **XML export** — readable text. Filename usually contains `.xml.emub3` (e.g. `supra tune export 05242026.xml.emub3`). Use these for grepping.

Always check modification timestamps to identify the most recent XML export before extracting values.

### Grep pattern to extract cold start symbols

```bash
grep -i "cranking\|afterStart\|warmUp\|postStart\|startEnrich\|cltBins4\|aseTbl\|aseRev\|aseClt" tune.xml.emub3
```

This captures all fuel enrichment tables and their axis bins in one pass. Key symbols returned:

| Symbol | Storage | Dims | Axes | Scale | Description |
|--------|---------|------|------|-------|-------------|
| `crankingCorrTbl` | u12 | 8 CLT × 5 TPS | `cltBinsCranking` × `tpsCrankingBins` | 1 (direct %) | Cranking fuel correction, pump gas |
| `crankingCorrTbl2` | u12 | 8 CLT × 5 TPS | same | 1 (direct %) | Cranking fuel correction, ethanol |
| `tblsFFCrankingBlend` | ubyte | 9×1 | ethanol content % | **0.5** | Pump gas weight in cranking blend (100%=E0, 0%=E100) |
| `aseTbl` | ubyte | 6 rev × 6 CLT | `aseCltBins` (rows) × revolutions (cols, bins not in XML) | 1 (direct %) | Afterstart enrichment, pump gas |
| `aseTbl2` | ubyte | 6 rev × 6 CLT | same | 1 (direct %) | Afterstart enrichment, ethanol |
| `warmupTbl` | ubyte | 10 CLT × 4 MAP | `cltBinsWarmup` × `mapBinsWarmup` | 1 (direct %) | Ongoing warmup enrichment, pump gas |
| `warmupTbl2` | ubyte | 10 CLT × 4 MAP | same | 1 (direct %) | Ongoing warmup enrichment, ethanol |
| `tblsFFWarmupBlend` | ubyte | 9×1 | ethanol content % | **0.5** | Pump gas weight in warmup blend |
| `cltBinsCranking` | sword | 8×1 | — | 1 (°C) | CLT axis for crankingCorrTbl |
| `tpsCrankingBins` | word | 6×1 | — | 0.1 (%) | TPS axis for crankingCorrTbl (note: 6 bins for 5-row table — may have one unused entry) |
| `aseCltBins` | sword | 6×1 | — | 1 (°C) | CLT axis for aseTbl |
| `cltBinsWarmup` | sword | 10×1 | — | 1 (°C) | CLT axis for warmupTbl |
| `mapBinsWarmup` | word | 4×1 | — | 1 (kPa) | MAP axis for warmupTbl |

**Scale note:** Fuel correction tables (`crankingCorrTbl`, `aseTbl`, `warmupTbl`) use scale=1 (raw = displayed %). This is **different** from airflow-% tables (ubyte, scale=0.5). Do not mix the two.

### Table layout

**`crankingCorrTbl` / `crankingCorrTbl2`** — `height=5` rows are TPS bins (closed throttle = row 0, WOT = row 4). `width=8` columns are CLT bins (cold = col 0). Active during cranking state only (< `crankingThreshold` RPM, typically 400 RPM). Values = % extra fuel on top of base pulse width.

**`aseTbl` / `aseTbl2`** — `height=6` rows are CLT bins (`aseCltBins`). `width=6` columns are revolution counts since start (bins not stored in XML — hardcoded in firmware). Values decay left→right to 0 over the first N revolutions. Active immediately after engine fires until all values reach 0.

**`warmupTbl` / `warmupTbl2`** — `height=4` rows are MAP bins, `width=10` columns are CLT bins. Ongoing correction applied until engine reaches operating temperature. Values = % extra fuel.

### Flex-fuel blending

At any ethanol content, the effective cranking correction is:
```
effective% = crankingCorrTbl[clt][tps] × (blend/100) + crankingCorrTbl2[clt][tps] × (1 − blend/100)
```
where `blend` is the pump-gas weight from `tblsFFCrankingBlend` for the current ethanol content (scale 0.5, so raw 0x6C=108 → 54% pump gas weight).

At E60 on this build, the pump gas weight is approximately 37%, giving ~63% weight to the ethanol table.

### Scalars related to cold start

| Symbol | Scale | Description |
|--------|-------|-------------|
| `crankingThreshold` | word, 1 RPM | RPM below which cranking state is active (400 on this build) |
| `crankingIgnAngle` | sbyte, 1° | Fixed ignition advance during cranking |
| `crankingLambdaTarget` | ubyte, /100 | Lambda target during cranking (100 = λ1.00) |
| `afterstartIgnitionLockAngle` | sbyte, 1° | Ignition angle held for post-start lock period |
| `afterstartIgnitionLockTime` | ubyte, 1 (units TBD) | Duration of post-start ignition lock |
| `afterstartIgnRestoreRate` | sbyte, 1°/cycle | Rate at which timing restores to base after lock |
| `afterstartEnableIgnLock` | ubyte, bool | 1 = post-start ignition lock active |
| `idleControlAfterstartDelay` | ubyte, 1 (cycles?) | Idle PID engagement delay after start |
| `idleAfterstartRPMincrease` | u12, 4×4 | Post-start RPM elevation table (CLT × time/rev bins) |

### Benchmark reference (port injection, pump gas)

From HP Academy and Banish (*Engine Management: Advanced Tuning*):
- **ASE at 20°C, first revolution**: ~39% (HP Academy empirical)
- **ASE at −10°C, first revolution**: ~60% (Banish)
- **Cranking correction at 0°C, closed throttle**: ~100–150% for port injection (first principles: ~50–60% of injected fuel lost to wall film at 0°C)

On this build (`supra tune export 05242026.xml.emub3`): ASE 39% at 23°C (exact HP Academy match), cranking correction 88% at 0°C pump gas / 158% ethanol / ~132% effective at E60. Hot ASE (92°C) is 12% first revolution — slightly high for a hot soak restart where wall film is minimal; 2–5% would be more appropriate.

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
