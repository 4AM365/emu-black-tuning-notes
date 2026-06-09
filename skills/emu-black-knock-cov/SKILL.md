---
name: emu-black-knock-cov
description: >-
  Estimates combustion stability (a CoV-of-IMEP proxy) from knock-sensor voltage
  scatter in an EMU Black log — a way to rank fuel/ignition maps without a
  cylinder-pressure transducer. Use whenever the user wants to "is combustion
  stable", "compare map smoothness", "combustion CoV from knock", "which map burns
  more consistently", "knock voltage scatter", or is A/B-testing map generations in
  boost. Uses `Knock voltage peak cyl N` cycle-to-cycle scatter on NO-KNOCK cycles,
  with the two required corrections: detrend within fine RPM×MAP cells (the mean rises
  deterministically with load) and restrict to positive transients (smoothness only
  bites while interpolating across cells). Takes logs or named --group sets; choose
  the cylinder with --channel. Boost-region tool — at idle use emu-black-idle-stability
  (RPM CoV) instead.
---

# EMU Black knock-voltage combustion-CoV proxy

`Knock voltage peak cyl N` (per-firing band-pass peak) has cycle-to-cycle scatter
that, **on no-knock cycles**, proxies combustion CoV. Two corrections are mandatory:

1. **Operating-point detrend** — the channel mean rises steeply with RPM/load, so a
   naive std/mean is dominated by that trend (a log that just roams more of the boost
   map looks noisier). Detrend within fine RPM×MAP cells:
   `resid = (peak − cell_mean)/cell_mean`, then `corrected CoV = std(resid)·100`.
2. **Transition gate** — map smoothness only bites while interpolating across cells, so
   keep only positive transients (accel through RPM **or** ramp into boost).

No-knock cycles only (`Knocking cylinders == 0` and the cylinder's knock-retard == 0).
Reported overall and by RPM bin. Lower corrected CoV = more stable combustion.

## Usage

```bash
# single map
python scripts/knock_chatter_cov.py LOG1.csv LOG2.csv [--channel "Knock voltage peak cyl 6"]

# A/B map comparison, with plot
python scripts/knock_chatter_cov.py \
    --group "hand=a.csv,b.csv" --group "machine=c.csv" --plot out.png
```

- `--channel` / `--retard` pick the cylinder's voltage and knock-retard channels.
- `--map-min` boost floor (default 130 kPa). `--plot` needs matplotlib; tables always print.

## Caveats

- It's a **qualitative ranking** tool, not a calibrated COV-of-IMEP — compare maps on
  like-for-like logs (ethanol blend and other run-to-run variables shift the level).
- **Idle:** knock ring-down is buried in mechanical noise → use `emu-black-idle-stability`
  (RPM CoV) at idle instead.

## Related

- `emu-black-lambda-tracking` (tracking companion), `emu-black-ve-smooth`.
- Method: `ai-analysis-skills/knock_voltage_cov_combustion_stability.md`,
  `notes/knock_sensors.md`.
