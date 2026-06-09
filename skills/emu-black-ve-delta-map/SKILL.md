---
name: emu-black-ve-delta-map
description: >-
  Renders the 3D delta surface between two EMU Black table .emubt exports (before vs
  after) so you can see exactly where a VE/fuel correction moved the map and by how
  much. Use whenever the user wants to "show what the autotune changed", "diff my two
  VE tables", "where did the correction land", "before vs after VE map", "delta
  surface", or wants to visualize a table edit. Reads both .emubt exports, takes the
  axis bins from a tune XML (the .emubt omits them), prints delta min/max/mean/RMS and
  writes a colored 3D surface (MAP→x, RPM→y). Works on any table symbol (default
  veTable) — pass the symbol and axis-bin symbols. Pairs with emu-black-ve-smooth and
  emu-black-emubt-export.
---

# EMU Black table delta-map

Visualizes `after − before` between two `.emubt` exports of the same table — the
clearest way to see which cells a log-based VE correction (or any edit) actually
touched and how far.

## Usage

```bash
python scripts/ve1_delta_map.py \
    --before before.emubt --after after.emubt \
    --tune project.xml.emub3 \
    [--symbol veTable] [--x-bins mapBins] [--y-bins rpmBins] \
    [--scale 0.1] [--out delta.png]
```

- `--tune` is the full project XML; `.emubt` exports omit the axis bins, so the bins
  come from there.
- `--symbol` defaults to `veTable` (u12, scale 0.1); pass another symbol + its axis-bin
  symbols to diff any table.
- Requires `numpy` + `matplotlib`. Prints delta stats and writes the 3D PNG.

## Convention

X = MAP (kPa) low→high left→right; Y = RPM low→high bottom→top; row 0 of the raw data
is the lowest Y bin (matches the repo's plot orientation).

## Related

- `emu-black-ve-smooth` (produce the corrected table), `emu-black-emubt-export` (write
  it out), `emu-black-tune` (decode symbols/axes).
