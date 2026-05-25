---
name: emu-black-log-emublog3
description: >-
  Parses EMU Black's binary log format (.emublog3) directly, removing the
  manual CSV-export step. Use this whenever the user has a .emublog3 file
  to analyze, says "look at my log" with a binary log present, or wants
  to skip the EMU Black UI's "Export to CSV" round-trip. Pairs with
  emu-black-log (which assumes CSV input) — once parsed, the output is
  the same channel set / DataFrame that emu-black-log knows how to
  diagnose. **Requires a one-time schema bootstrap** — pair a known
  .emublog3 with its matching CSV export to lock the binary layout, then
  reuse the schema for all future logs from that ECU configuration.
---

# EMU Black .emublog3 parser

EMU Black stores binary data logs as `.emublog3` files: a gzip-compressed
record stream with **no embedded channel schema**. Channel order, count,
and per-channel scaling live in the ECU's log configuration, not in the
file. So parsing requires the schema to be known externally — either by
pairing a `.emublog3` with its matching CSV export (one-time bootstrap)
or by reading the EMU project's logger setup.

## What we know about the format

- **Outer envelope**: standard gzip (magic `1F 8B 08 ...`).
- **Decompression ratio**: ~4.5× (a 2.26 MB file expands to ~10.5 MB).
- **Inner structure**: fixed-size records, contiguous. Record size = (number of
  configured log channels) × (bytes per value). Common per-value sizes are 1, 2,
  or 4 bytes depending on channel data type.
- **No textual headers** — no channel names, no record-size marker. The first
  ~16 bytes might be a small file header (we've observed structured bytes that
  could be a count + timestamp), but contents aren't yet decoded.
- **Sample rate** matches the CSV `TIME` increment for the same recording
  session — typically 25 Hz (0.04 s/record) but configurable.

## Bootstrap workflow (one-time per ECU configuration)

If you only have `.emublog3` files and no matching CSV, **first ask the user
to export one as CSV via EMU Black** (File → Export to CSV). With both files
in hand:

```bash
python scripts/discover_schema.py \
  --emublog3 path/to/sample.emublog3 \
  --csv     path/to/matching_export.csv \
  --out-schema schemas/<descriptive_name>.json
```

The discovery tool:
1. Gunzips the `.emublog3`
2. Reads channel count and sample count from the CSV
3. Searches for the record size by trying common per-value widths (1/2/4 bytes)
   and looking for a monotonically increasing time-like channel near offset 0
4. For each candidate record size, attempts to assign byte positions and types
   to each CSV channel by correlating decoded binary values against the CSV
5. Reports its confidence and writes the schema JSON

The schema is small (channel name → byte offset, type, scale) and reusable
for any log from the same ECU log config. **Re-run schema discovery if the
user changes the logger setup in EMU Black** (added/removed channels, changed
sample rate).

## Parse workflow (after schema is locked)

```bash
python scripts/parse_emublog3.py \
  --emublog3 path/to/log.emublog3 \
  --schema   schemas/<descriptive_name>.json \
  --out-csv  path/to/log.csv
```

or programmatically:

```python
from parse_emublog3 import read_emublog3
df = read_emublog3('log.emublog3', schema='schemas/supra_v1.json')
# df is a pandas DataFrame, same shape as EMU's CSV export
# Hand off to emu-black-log workflows
```

## Inspect tool (no schema required)

For unknown files where you want to see what's there before bootstrapping:

```bash
python scripts/inspect.py path/to/log.emublog3
```

Prints decompressed size, first 256 bytes hex, and reports any obvious
candidate record sizes based on simple periodicity tests.

## Honest status

- **Working today**: gzip envelope, inspect tool, schema discovery framework, parse-with-schema execution.
- **Requires bootstrap**: the schema discovery tool is heuristic — when it works it produces a reusable
  schema, but it has not been validated against many ECU log configurations. Expect to iterate on a few
  pairs the first time you use it for a particular EMU setup.
- **Not done**: directly decoding the leading file header to extract the schema without a CSV pair.
  If/when that's reverse-engineered, the bootstrap step becomes optional.

## Safety / caveats

- The discovery tool can produce false positives if channels happen to correlate by coincidence over a
  short window. Always verify a few cells visually in EMU after parsing.
- Channel order in the `.emublog3` does NOT have to match the CSV column order — EMU may sort them
  differently. The schema records the binary order explicitly.
- Different EMU firmware versions or ECU log configurations produce different binary layouts. Always
  associate a schema with its source ECU/firmware in the filename.

## Related skills

- **`emu-black-log`** — once parsed to a DataFrame, all the channel reference, triage flow, and
  diagnostic patterns there apply directly.
- **`emu-black-tune`** — for the calibration side of the build.
