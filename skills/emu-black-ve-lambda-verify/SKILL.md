---
name: emu-black-ve-lambda-verify
description: >-
  Verifies that an EMU Black VE table carries the lambda enrichment correctly, using the
  veTable x lambda_target product test. Use whenever the user wants to "check my VE map
  has the boost enrichment", "did the VE table get the extra fuel for my lambda targets",
  "is there a kink at the boost knee", "verify VE vs lambda", or after expanding/editing
  lambda targets. In a fuel model where lambdaTable is only a reference / closed-loop
  target (not a fuel multiplier), the veTable IS the dose and must carry enrichment by
  hand; the product veTable x lambda_target should be a smooth air-VE surface — a dip at
  the boost-enrichment knee means the VE didn't receive the fuel the targets demand.
  Reads the tables straight from a tune XML export. Pairs with emu-black-tune.
---

# EMU Black VE-vs-lambda shape check

When `lambdaTable` is a **reference / closed-loop target only** (the firmware does not
divide the dose by it), the **`veTable` is the dose** and must carry the 1/λ enrichment
by hand. The cheap whole-table check:

```
air_VE_proxy(map, rpm) = veTable(map, rpm) × lambda_target(map, rpm)
```

A correct VE shape yields a **smooth** surface across MAP at each RPM — rises out of the
idle/vacuum region, peaks near the torque-MAP band, tapers gently into boost. A **dip or
step at the boost knee** (where `lambda_target` starts dropping at boost onset) means the
`veTable` did **not** get the extra fuel the (expanded) lambda targets demand → shape
mismatch; the VE needs the boost enrichment added.

## Usage

```bash
python scripts/verify_ve_vs_lambda.py TUNE.xml.emub3 \
    [--ve veTable] [--lambda lambdaTable] \
    [--map-bins mapBins] [--rpm-bins rpmBins] \
    [--lambda-map-bins mapBinsL8] [--lambda-rpm-bins rpmBins10] \
    [--ve-scale 0.1] [--lambda-scale 0.01]
```

Run once per fuel: pump `--ve veTable --lambda lambdaTable`, ethanol
`--ve veTable2 --lambda lambdaTable2`. Standard library only. Confirm the lambda axis
symbol names for your tune with `emu-black-tune` (they vary by project).

## Related

- `emu-black-tune` (decode tables/axes/scales), `emu-black-ve-smooth`,
  `ai-analysis-skills/ve_vs_map_at_constant_rpm.md` (the dose-vs-MAP method this checks).
