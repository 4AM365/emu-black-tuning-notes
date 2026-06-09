---
name: emu-black-intercooler-heatsoak
description: >-
  Compares charge-air / intercooler heat-soak ACROSS multiple EMU Black logs,
  normalized to ambient — so different days, ambient temps, or configurations are
  directly comparable. Use whenever the user wants to "compare intercooler
  performance", "hood on vs hood off", "is my intercooler heat-soaking", "charge
  temps across these logs", "compressor-bay heat rise", "did the vent/duct help", or
  is A/B-testing a cooling change. For each log it reports the ambient-normalized
  deltas PreIC-amb (compressor-bay rise), Chg-amb (total charge rise), and Chg-PreIC
  (post-compressor pickup), sorted by ambient. Takes any number of logs as arguments
  (not vehicle-specific). For a single log's raw distribution use
  emu-black-charge-temp-analysis instead.
---

# EMU Black intercooler heat-soak comparison

Absolute charge temps aren't comparable across logs taken on different days — a hot
day looks "worse" even if the cooling system performs identically. This normalizes
to **ambient**, so the deltas reflect the *system*, not the weather.

## What it reports (per log, running no-boost)

| Metric | Meaning |
|--------|---------|
| `PreIC − amb` | compressor-bay air rise above ambient — the cleanest heat-soak signal |
| `Chg − amb`   | total charge-air rise above ambient at the throttle body |
| `Chg − PreIC` | pickup from compressor outlet to the throttle body |

Logs are sorted by ambient so a cool→hot sweep (or hood-on vs hood-off) reads top to
bottom.

## Usage

```bash
python scripts/intercooler_heatsoak.py LOG1.csv LOG2.csv ... [--ambient C]
```

- Ambient comes from the logged `Ambient temperature` channel; `--ambient` supplies a
  fallback for reduced logs that don't carry it.
- Standard library only.

## Interpreting

- A **rising `PreIC − amb`** on hotter days or after a config change = the compressor
  bay is heat-soaking the inlet; address ducting/venting/heat-shielding.
- `Chg − PreIC` isolates the **core/piping** pickup downstream of the compressor.
- Drop Pre-IC dropouts (≤ 2 °C) — they're sensor faults, handled here automatically.

## Related

- `emu-black-charge-temp-analysis` — single-log charge-temp distribution.
- Worked example + the Supra hood-removal study: `notes/hood_removal_charge_temps.md`,
  `supra/notes/`.
