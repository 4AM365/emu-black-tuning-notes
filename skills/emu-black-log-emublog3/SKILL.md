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
python scripts/inspect_emublog3.py path/to/log.emublog3
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

### Empirical finding (2026-05-31, Supra test-run pair, 565-channel CSV)

Full-channel bootstrap attempted (test-run.emublog3 vs all-channel-reference.csv, 16025 records,
record = **504 bytes, data starts at byte 0** — the ~12 trailing bytes are pad, NOT a leading
header). Read before trusting `discover_schema` at scale:

- "matched 505/565" is **massively inflated**: only ~**55 unique byte offsets** exist in a 504-byte
  record, so ~450 "matches" are aliases (constant/zero columns + derived channels on the same
  offsets). **~480 of 565 CSV columns are constant/zero export padding — nothing to decode.**
- The tool's `correlation` is **scale-invariant** — high corr only means the field tracks the
  channel's shape; scale/offset are fit separately and are often wrong (EGT 2 fit as `i16 × 0.0039`,
  which can't reach 742 °C). **Always linear-refit `y=a*raw+b` vs CSV and check R²; never trust the
  reported scale.**
- **Fast, high-dynamic-range channels decode reliably** (~30–40: RPM, MAP, TPS, PPS, Boost, Boost
  Target, Vehicle Speed, Ignition Angle, VE, Injectors PW, Short term trim …).
- **Slow/monotonic channels do NOT reliably auto-decode from one log — including EGT 1 and EGT 2**
  (and IAT, Charge temp, Battery). They track the warmup/time ramp, so the search latches onto a
  monotonic timer field. Proof: brute force placed EGT1/EGT2 at *overlapping* u32 offsets both
  sharing the **TIME scale** (1.52e-05); the field at off=104 is 84% monotonic (a runtime counter),
  not EGT. **Do not trust binary-decoded EGT — use the CSV.**
- A correctly-gated re-discovery (dynamic-only, R²>0.9995) swung between 1 and 11 channels depending
  on thresholds — that instability shows single-log value-correlation is not a sound basis for a
  full schema.

**Takeaway:** format is structurally solved and fast channels are easy; a *complete, safe* schema
(esp. EGT/temps) needs the **deterministic** route — read channel order/type/scale from the EMU
project's logger config — not value-correlation. No auto-schema is committed because none was
trustworthy enough.

### Deterministic route WORKS — EGT pinned via channel order (2026-05-31)

The EMU **"Select logged parameters"** dialog gives the logger channel ORDER (Channel #0..#N).
For test-run: #0 RPM, #1 MAP, #2 Boost, #3 Boost Target, #4 Boost DC, #5 PPS, #6 Vehicle Speed,
#7 Knock voltage peak cyl 6, #8 Back pressure, #9 Turboshaft speed, #10 Estimated airflow,
#11 (blank), **#12 EGT 1, #13 EGT 2**, ...

Using the **adjacency constraint** (EGT1 immediately followed by EGT2, same dtype, sensible shared
scale, non-monotonic) the EGT pair was pinned **deterministically** where correlation had failed:
**EGT 1 @ offset 106 u16, EGT 2 @ offset 108 u16, scale = 1.0 (raw u16 = degC direct)**, R²=0.9995/
0.9998, decoded values match the CSV exactly. This is the proof that the logger-config ORDER + a
per-channel CSV fit (for width/scale) cracks the channels that single-log value-correlation can't.
**To finish the full schema: capture the COMPLETE ordered channel list from that dialog** (the
504-byte record holds ~55 real channels, far more than the 16 first visible), then walk them in
order assigning offsets and fitting width/scale against the CSV. EGT stored as u16 degC, scale 1.

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
