# Knock-chatter CoV — Supra results (hand-made vs machine-smoothed map)

Build-specific results behind the generic method note [`notes/knock_voltage_cov_combustion_stability.md`](../../notes/knock_voltage_cov_combustion_stability.md). Script: `supra/scripts/knock_chatter_cov.py`.

## This dataset's transition-gate note

Empirically on this car, MAP > 130 kPa is *already* almost entirely transitional — ~98% of boost samples pass the dRPM/dt or dMAP/dt gate — because steady cruise rarely exceeds 130 kPa. So on this dataset the transition gate barely changes the set; the **operating-point detrend** (RPM 250 × MAP 10 kPa cells, normalized residuals) is what actually mattered.

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

**Machine-smoothed is tighter in every overlapping RPM bin** — a clean, consistent confirmation that the algorithm-smoothed map runs with less knock-sensor chatter / more repeatable combustion than the hand-built map.

Caveats: machine-smoothed is one log (363 transition samples, RPM 3.7–5.9k, no >6k coverage); 5.5–6k has too few machine samples to plot. Per [[project_supra_flex_fuel]], ethanol blend can vary between logs and is not controlled here.
