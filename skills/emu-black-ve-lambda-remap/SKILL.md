---
name: emu-black-ve-lambda-remap
description: >-
  Builds one EMU Black VE table from another by applying the lambda-target delta between
  two lambda tables — e.g. derive veTable2 (ethanol) from veTable (pump) when the only
  intended difference is the lambda target. Use whenever the user wants to "make VE2 from
  VE1 with the lambda difference", "remap my ethanol VE from the pump VE", "apply the
  lambda target delta to the VE table", "derive one fuel table from another", or is
  seeding a second flex table. Uses VE2 = VE1 × (1 − (lambdaTable2 − lambdaTable)) (the
  rough rule +0.01 λ leaner ≈ −1% VE), bilinear-interpolating the lambda tables onto the
  VE grid. Reads the VE source from an .emubt and the lambda tables/axes from a tune XML;
  writes a JSON spec for emu-black-emubt-export plus a markdown back-calc report. Pairs
  with emu-black-emubt-export and emu-black-ve-smooth.
---

# EMU Black VE lambda-delta remap

When two fuel VE tables should differ **only** by their lambda target (the rest of the
dose being identical), derive one from the other instead of hand-editing:

```
lambda_delta(map, rpm) = lambdaTable2 − lambdaTable      (bilinear onto the VE grid)
VE2 = VE1 × (1 − lambda_delta)
```

following the local rule **+0.01 λ leaner ≈ −1% VE/fuel**. The lambda tables usually sit
on a coarser axis (`mapBinsL8` × `rpmBins10`) than the VE grid (`mapBins` × `rpmBins`), so
the delta is bilinear-interpolated onto each VE cell.

## Usage

```bash
python scripts/remap_ve_for_lambda_delta.py \
    --tune project.xml.emub3 \
    --ve1 "VE Table 1.emubt" \
    --out-emubt "VE Table 2 remap.emubt" \
    [--out-json spec.json] [--out-report backcalc.md] \
    [--src-symbol veTable] [--dst-symbol veTable2] \
    [--map-bins mapBins --rpm-bins rpmBins \
     --lambda-map-bins mapBinsL8 --lambda-rpm-bins rpmBins10]
```

Outputs a JSON spec (feed to `emu-black-emubt-export` to write the `.emubt`) and a markdown
back-calc report (lambda delta, multiplier, VE1, remapped VE2 grids) for review.

## Notes

- This is a **seed**, not a final tune — verify VE2 against measured lambda on the target
  fuel. The 1%/0.01 λ rule is approximate.
- Confirm the lambda-axis symbol names for your tune with `emu-black-tune` (they vary).

## Related

- `emu-black-emubt-export` (write the spec out as `.emubt`), `emu-black-tune` (decode
  symbols/axes), `emu-black-ve-lambda-verify` (check the result tracks its targets),
  `emu-black-ve-smooth`.
