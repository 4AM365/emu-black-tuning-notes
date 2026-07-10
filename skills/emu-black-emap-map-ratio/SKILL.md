---
name: emu-black-emap-map-ratio
description: >-
  Builds an EMAP/MAP pressure-ratio table from EMU Black CSV logs, binned
  into the tune's veTable grid (mapBins x rpmBins). Use when the user asks
  to compare exhaust backpressure to MAP/boost, map reversion margin,
  check turbine backpressure ("EMAP vs MAP", "backpressure ratio",
  "crossover"), or decide where cam overlap helps vs hurts. Gates on
  sensor liveness — a flat Back pressure channel is reported as a dead
  sensor, never binned as data. Pairs with notes/emap_map_ratio_cam_overlap.md
  for the interpretation (reversion, VVT scheduling, dynamic compression).
---

# EMAP/MAP ratio table from logs

## Why this ratio

EMAP/MAP (both absolute) at each operating point decides which way gas moves
during valve overlap:

- **ratio > 1** — exhaust backflows into the cylinder/intake during overlap
  (reversion): internal EGR, hot residuals, charge heating. Overlap hurts.
- **ratio < 1** ("crossover", Bell) — fresh charge scavenges residuals out the
  exhaust: cooler chamber, denser charge. Overlap helps.

Bell (`corpus/maximum_boost.md`): street turbos generally run EMAP somewhat
*above* boost; judging turbine A/R "by the numbers" requires measuring turbine
inlet pressure and comparing with boost.

## Requirements

- Logs must contain `Back pressure`, `MAP`, `RPM`, `TIME` (`Baro` optional;
  defaults to 100 kPa when absent). Reduced logs missing the channel are
  skipped with a message.
- **Unit trap:** on this build the `Back pressure` channel logs in **bar
  gauge**, quantized 1/32 bar (~3.1 kPa/count), while MAP is kPa. Read in kPa
  it looks dead-flat (a 110 kPa-gauge pull reads "1.1") — this misdiagnosed a
  live sensor as dead once. The script autodetects (max ≤ 6 ⇒ bar) and
  requires corr(EMAP, MAP) > 0.3 on logs that span boost, so a genuinely
  immobile or non-tracking channel is excluded and reported, and a
  quantized-bar channel is converted, not discarded.

## Run

```bash
python skills/emu-black-emap-map-ratio/scripts/emap_map_ratio.py \
  --tune "supra/exports/<latest>.xml.emub3" \
  --out supra/exports/emap_ratio \
  <log1.csv> <log2.csv> ...
```

Outputs:
- `<out>_points.csv` — every running sample: TIME, RPM, MAP, smoothed absolute
  EMAP, ratio, source log, bin indices.
- `<out>_table.md` / `.csv` — per-cell median ratio on the veTable grid,
  RPM increasing upward, MAP left→right (repo display convention). Cells with
  n < 20 stay blank.

`--self-test` feeds MAP in as EMAP — every populated cell must print 1.00.
Use it after touching the script.

## Method (and why)

1. **Liveness gate** before anything else (see Requirements).
2. **Gauge/absolute autodetect** — median Back pressure with engine off (or at
   idle): ~0 → gauge (adds Baro), ~100 → already absolute.
3. **Despike + smooth**: 5-sample rolling median kills single-sample spikes,
   then zero-phase Savitzky-Golay (poly 2). Window is sized from the measured
   high-frequency noise sigma (MAD of successive differences) so the smoothed
   channel lands near ±0.5 kPa; clamped 7–31 samples (0.28–1.24 s at 25 Hz).
   Rationale: exhaust pressure pulsates at firing frequency (3×RPM/60 on an
   I6 = 50–350 Hz), far above the 12.5 Hz log Nyquist — the pulsation aliases
   into broadband noise and only the cycle-mean is recoverable, which is the
   quantity the ratio needs. Zero-phase filtering on both EMAP and MAP keeps
   them time-aligned (no lag mismatch corrupting the ratio in transients).
4. **Binning**: nearest veTable bin (`mapBins` 16 × `rpmBins` 20 from the tune
   XML); per-cell median (robust to remaining transients) with a minimum
   sample count.

## Interpretation

Send the table to `notes/emap_map_ratio_cam_overlap.md`: ratio bands → where
intake cam advance (overlap) pays vs costs, VE consequences, dynamic
compression / knock implications.
