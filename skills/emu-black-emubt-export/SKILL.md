---
name: emu-black-emubt-export
description: >-
  Exports EMU Black ECU tables to importable .emubt files. Use this whenever you
  produce or modify a tune table — rescaled airflow maps, new idle/cranking/armed
  targets, fuel or ignition tables, custom corrections — and need it written out
  as a single-table .emubt the user can import into EMU Black. Trigger on phrases
  like "export this table", "make an .emubt", "write these values out for EMU",
  "give me an importable table", "save the rescaled airflow table", or any time
  the deliverable is a table file EMU can read back. Also covers the CSV
  round-trip tooling in the emubt_breakout repo for editing existing tables.
  Pairs with emu-black-tune (which decodes/scales values) — use THIS skill for
  the write-out step. Reach for it proactively after computing new table values.
---

# EMU Black .emubt Exporter

`.emubt` is EMU Black's single-(or multi-)table export: a minimal XML project
that holds one or more `<symbol>` table elements. EMU imports it into the
matching table by symbol name. Use this skill to write tables we generate into
that format correctly — the encoding has a few traps that silently produce a
file EMU rejects or imports wrong.

For *reading*/decoding tables and the scaling conventions, use the
**emu-black-tune** skill. This skill is the write-out half.

## File shape

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="1.0">
  <tables>
    <symbol name="idleActiveAirflow" storage="ubyte" width="8" height="5" data="71 65 4B ... 71 "/>
  </tables>
</project>
```

- `version="1.0"` (a single-table export; the full tune is `version="3.059"`).
- One `<symbol>` per table; multiple symbols are allowed under `<tables>`.
- **Filename = EMU's exact table title**, including category prefix and unit
  suffix, e.g. `Airflow - Active state air flow [%].emubt`,
  `Cranking - Cranking airflow [%].emubt`. EMU shows/uses these titles; matching
  the filename keeps things unambiguous for the user.

## Encoding traps (why the bundled script exists)

1. **`data` is space-separated UPPERCASE hex**, no `0x`: `108 → 6C`, `0 → 0`.
2. **Signed types (`sbyte`/`sword`) use sign + hex magnitude, NOT two's
   complement**: `-13 → -D`, `-50 → -32`.
3. **The XML declaration must use double quotes.** Python's `ElementTree`
   defaults to single quotes (`<?xml version='1.0' …?>`) which the ECU rejects.
4. **Storage type must be explicit and exact** (`ubyte`, `sbyte`, `word`,
   `sword`, `u12`). Do not let a tool *infer* it — see the round-trip note below.

## Primary path: `scripts/export_emubt.py`

Writes a correct `.emubt` from values we compute. Handles all four traps and
validates count and per-type range. Verified to reproduce real EMU exports
byte-for-byte (unsigned-with-scale and signed).

**Single table, raw integer values:**
```bash
python scripts/export_emubt.py --name idleArmedAirFlow --storage ubyte \
  --width 8 --height 1 --values "48 63 77 87 95 101 107 108" \
  --out "Airflow - Armed state air flow [%].emubt"
```

**Single table, DISPLAY values + `--scale`** (raw = round(display/scale)). Airflow-%
ubyte tables display at 0.5/count, so pass `--scale 0.5` and give the percentages
EMU shows:
```bash
python scripts/export_emubt.py --name idleActiveAirflow --storage ubyte \
  --width 8 --height 5 --scale 0.5 \
  --values "56.5 50.5 37.5 19.5 16 14.5 14.5 14.5  68.5 61.5 45 25.5 ..." \
  --out "Airflow - Active state air flow [%].emubt"
```

**Multiple tables / structured input — JSON spec** (`values` may be flat or 2D rows):
```bash
python scripts/export_emubt.py --json spec.json
```
```json
{
  "out": "Airflow - Active state air flow [%].emubt",
  "symbols": [
    {"name": "idleActiveAirflow", "storage": "ubyte", "width": 8, "height": 5,
     "scale": 0.5,
     "values": [[56.5,50.5,37.5,19.5,16,14.5,14.5,14.5], [68.5,61.5,45,25.5,22,20.5,22.5,22.5]]}
  ]
}
```

**Value order is row-major and matches EMU's storage order.** For the idle/airflow
tables that means rows run **low → high** on the Y axis (e.g. `idleActiveAirflow`
row 0 = lowest idle-target RPM). Decode the original first (emu-black-tune) to
confirm orientation before writing a replacement.

## Alternative: CSV round-trip for EXISTING tables (`emubt_breakout` repo)

Located at `C:\Code\car-projects\emubt_breakout`. Use this when the user wants to
edit tables that already exist as `.emubt`, working in a spreadsheet:

- `emubt_to_csv.py <folder>` — explodes every `.emubt` table into a per-symbol
  CSV grid named `<emubt_stem>__<symbol>.csv`, in **decimal RAW** units (no scale
  applied — `idleActiveAirflow` cell shows `113`, not `56.5`). Originals untouched.
- `csv_to_emubt.py <folder>` — re-ingests edited CSVs back, matching the
  `__<symbol>` suffix to the symbol inside the **template** `.emubt`, and writes
  `altered_<original>.emubt`, **preserving the template's storage type**.

**Prefer the template path.** `csv_to_emubt.py`'s fresh-create branch (CSV with no
matching `.emubt` template) infers storage as `u8/u16` — not `ubyte/sbyte` — and
cannot tag signed tables, so it is lossy for anything signed. For brand-new tables
use `export_emubt.py` (explicit storage) instead.

## Workflow for tables we generate

1. Decode the source table and confirm storage, width/height, axis orientation,
   and scale (emu-black-tune skill).
2. Compute new values (e.g. an actuator-range rescale). Keep them in display
   units if convenient and let `--scale` convert.
3. Export with `export_emubt.py` to a file named after EMU's table title.
4. Have the user import the single table in EMU and spot-check a few cells
   against the values you reported before running the engine.

## Verifying export correctness (proven on this build)

Because a single-table `.emubt` and the full `.emub3` project store the **same raw
hex** for the same symbol, you can prove the encoding is faithful by comparing them:
extract `storage`/`width`/`height`/`data` for a symbol from both and diff. On this
build that check returned **identical raw bytes** for `idleActiveAirflow`,
`idleArmedAirFlow`, and the signed `idleCustomCorrection`, with matching storage and
dims — confirming `export_emubt.py` writes exactly what EMU reads (including the
sign-magnitude `-D` format for `sbyte`). Only `idleCrankingDC` differed, and that was
a *content* edit (the `.emubt` was newer than the export), not an encoding error.

**Takeaway:** a value mismatch between a fresh `.emubt` and an older project export
is usually baseline drift, not a scaling bug — confirm which file is current truth
(file mtimes) before rescaling off it. Verify encoding by round-tripping one known
table, not by assuming.

## Safety

- A single-table `.emubt` import touches only that table — lower blast radius
  than editing the whole project export. Prefer it for targeted changes.
- Always tell the user the resulting display values (not just raw hex) so they
  can verify against EMU after import.
- Confirm the scale empirically (one cell: `raw × scale` vs EMU display) before
  trusting a `--scale` conversion; a wrong scale silently corrupts every cell.
- This is a real engine — for cranking/idle/DBW tables, confirm intent and
  re-verify post-import before start.
