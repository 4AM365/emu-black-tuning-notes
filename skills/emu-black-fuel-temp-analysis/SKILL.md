---
name: emu-black-fuel-temp-analysis
description: >-
  Summarizes the Fuel Temperature channel from EMU Black CSV logs — start / min /
  mean / max / end per log. Use whenever the user wants to "check fuel temp", "how
  hot is my fuel", "fuel rail heat-soak", "fuel temperature rise", "use fuel temp as
  an ambient proxy", or is sizing fuel-temperature density / vapor-pressure
  compensation. The start-of-log value is the best cold anchor (≈ tank/ambient before
  pump + bay heat); the rise to end shows heat-soak. Takes any number of logs as
  arguments (not vehicle-specific).
---

# EMU Black fuel-temperature analysis

Reads the **Fuel Temperature** channel and reports start / min / mean / max / end
(°C and °F for the start anchor) per log, skipping sensor-fault rows (≤ −30 °C).

## Usage

```bash
python scripts/fuel_temp.py LOG1.csv [LOG2.csv ...]
```

Standard library only.

## Why it's useful

- **Cold anchor:** the first valid sample ≈ tank/ambient temperature before the pump
  and engine bay warm the rail — a handy **ambient proxy** when a log lacks an Ambient
  channel (e.g. for `emu-black-intercooler-heatsoak`).
- **Heat-soak:** the start→end rise quantifies how much the rail heat-soaks during the
  drive — relevant to **fuel density** (mass per injector ms) and **vapor pressure**
  (hot-restart / cranking). If the rail runs hot, fuel-temp density compensation and
  hot-start enrichment matter more.

## Related

- `emu-black-charge-temp-analysis` / `emu-black-intercooler-heatsoak` — air-side temps.
- `emu-black-temp-sensor-recal` — if the fuel-temp sensor reads systematically wrong.
