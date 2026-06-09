---
name: emu-black-charge-temp-analysis
description: >-
  Summarizes intake-air / charge temperature behavior from EMU Black CSV logs —
  IAT, Pre-IC (pre-intercooler) temperature, Charge temp, and CLT distributions over
  running no-boost samples, plus the Pre-IC sensor dropout rate and an idle subset.
  Use whenever the user wants to "check my charge temps", "how hot is my intake air",
  "pre-IC vs post-IC", "is my IAT sensor dropping out", "charge temp distribution",
  "intake temps at idle", or is investigating heat-soak / intercooler efficiency from
  a log. Takes one or more log files as arguments (not vehicle-specific). Pairs with
  emu-black-intercooler-heatsoak (cross-log ambient-normalized comparison) and
  emu-black-temp-sensor-recal (fix a mis-calibrated temp sensor).
---

# EMU Black charge-temp distribution

Over **running, no-boost** samples (`RPM > 400`, `MAP < 100 kPa`), reports
min / p05 / median / mean / p95 / max for **IAT**, **Pre-IC temperature**,
**Charge temp**, and **CLT**, the **Pre-IC sensor dropout rate** (≤ 2 °C, a common
fault signature), and an **idle subset** (`RPM < 1500`, `MAP < 60`).

## Usage

```bash
python scripts/charge_temp_distribution.py LOG.csv [LOG2.csv ...] [--ambient C]
```

- One or more EMU semicolon-delimited CSV exports.
- `--ambient` is for the printed label only.
- Standard library only (no pandas).

## Interpreting

- **Pre-IC near ambient at no-boost** is the clean heat-soak signal (compressor-bay
  air rise above ambient). A large Pre-IC − ambient at idle = under-hood/compressor
  heat soak.
- **Charge − Pre-IC** is the pickup from compressor outlet to the throttle body.
- A high **dropout rate** (Pre-IC ≤ 2 °C) points to a sensor/wiring fault, not real
  temperature — exclude dropouts before trusting the distribution. If the sensor
  reads systematically wrong (offset), it's a *calibration* problem →
  `emu-black-temp-sensor-recal`.

## Related

- `emu-black-intercooler-heatsoak` — compare charge-temp / IC performance **across**
  logs, normalized to ambient (e.g. hood-on vs hood-off, hot day vs cool).
- Build-specific charge-temp derivations and results live in
  `notes/hood_removal_charge_temps.md` and `supra/notes/`.
