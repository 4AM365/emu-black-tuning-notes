# Knock-voltage scatter as a combustion-stability (CoV) proxy

Method for reading combustion quality from knock-sensor "chatter," and the result
comparing three fuel-map generations. Script: `supra/scripts/knock_chatter_cov.py`.

## The metric

`Knock voltage peak cyl N` = per-combustion-event peak of the band-pass-filtered
knock-sensor signal in that cylinder's window, one value per firing. Its cycle-to-cycle
scatter, on **no-knock** cycles, proxies combustion CoV (the structural analogue of
CoV-of-IMEP). Express scatter as a Coefficient of Variation (std/mean, %) — NOT raw std,
because the signal is heteroscedastic (swing scales with mean).

## The two methodological traps (both must be handled)

1. **Operating-point mixing (the big one).** The MEAN of this channel rises steeply and
   deterministically with RPM and load (mechanical engine noise). A naive std/mean over a
   coarse window (e.g. 1000 rpm × 50 kPa) is then dominated by that deterministic trend, so
   a log that merely *roams more of the boost map* looks noisier — a pure artifact. This
   inverted the first cut of this analysis.
   **Fix:** detrend within fine cells. Bin RPM 250 × MAP 10 kPa, subtract each cell's local
   mean, normalize: `resid_norm = (peak − mean_cell)/mean_cell`. Then `corrected CoV =
   std(resid_norm)·100`. This isolates scatter *around* the local operating point and also
   cancels any absolute-level offset between groups.

2. **Where you measure.** Map smoothness only bites while *interpolating across cells* —
   i.e. on transitions: accelerating through RPM (dRPM/dt > 0) or ramping into boost
   (dMAP/dt > 0). At steady state you sit in one cell and rough-vs-smooth washes out. So
   restrict to positive transients before measuring. (Empirically on this car, MAP > 130 kPa
   is *already* almost entirely transitional — ~98% of boost samples pass the gate — because
   steady cruise rarely exceeds 130 kPa. So on this dataset the transition gate barely
   changes the set; the operating-point detrend is what actually mattered.)

Also: no-knock cycles only (`Knocking cylinders == 0` AND cyl-N retard == 0). It's a
qualitative proxy, not a calibrated CoV-of-IMEP — use it to rank tunes, not as an absolute.

## Result: hand-made vs machine-smoothed (MAP > 130 kPa, transitions, detrended)

Two map generations (handmade and hand-smoothed are the SAME map — pooled as "hand-made"):
- **hand-made** — `20260524_1301`, `hood-removed`, `hood 0506`, `hand-smoothed-1/2/3`
- **machine-smoothed** — newest, algorithm/autotune-smoothed (`machine-smoothed.csv`, full log)

Operating-point-corrected CoV (lower = more stable combustion):

| RPM bin  | hand-made | machine-smoothed |
|----------|-----------|------------------|
| 3.5–4k   | 30.8%     | **11.5%**        |
| 4–4.5k   | 24.1%     | **17.2%**        |
| 4.5–5k   | 24.7%     | **21.3%**        |
| 5–5.5k   | 28.9%     | **16.4%**        |
| overall  | 25.9%     | **19.0%**        |

**Machine-smoothed is tighter in every overlapping RPM bin** — a clean, consistent
confirmation that the algorithm-smoothed map runs with less knock-sensor chatter / more
repeatable combustion than the hand-built map.

Caveats: machine-smoothed is one log (363 transition samples, RPM 3.7–5.9k, no >6k coverage);
5.5–6k has too few machine samples to plot. Per [[project_supra_flex_fuel]], ethanol blend
can vary between logs and is not controlled here.
