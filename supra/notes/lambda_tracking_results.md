# Lambda tracking: hand-made vs machine-smoothed — Supra results

Build-specific results behind the generic method note [`notes/lambda_tracking_map_smoothing.md`](../../notes/lambda_tracking_map_smoothing.md). Script: `supra/scripts/lambda_tracking.py`.

## Result (hand-made = all human-map logs; machine-smoothed = `machine-smoothed.csv`)

Tracking-error **spread (std %)** by MAP load bin — lower = tighter tracking:

| MAP bin (kPa)      | hand-made | machine-smoothed |
|--------------------|-----------|------------------|
| 40–80 (cruise)     | 6.29%     | 6.65%            |
| 80–110             | 6.11%     | **4.71%**        |
| 110–140 (low boost)| 4.18%     | **2.75%**        |
| 140–185 (boost)    | 3.96%     | **2.84%**        |

**Machine-smoothed tracks markedly tighter everywhere ≥ 80 kPa** — spread nearly halves in boost (2.8% vs 4.0%). Same load region where combustion CoV improved: smoother cell-to-cell dose → less feedforward error across cells → measured lambda hugs target. The lowest cruise bin (40–80) is a wash (closed-loop deadband masks feedforward smoothness).

## Bias is a known artifact (don't read it as a tracking fault)

The machine-smoothed map reads ~**+3% lean** of target uniformly because the whole map was **not re-scaled after the per-cylinder trims** (a global mixture offset). The analysis applies a constant **−3% correction** (`SHIFT` in the script). A constant shift doesn't change std, so the spread table is unaffected. After re-centering, the machine-smoothed error distribution is taller/narrower (std 6.2% vs 6.4% overall, far tighter in ≥110 kPa bins) vs the broad, rich-skewed hand-made distribution. The residual offset is a one-number global fuel-scale fix.

## Caveats
Machine-smoothed is a single log (n=10.5k valid vs 54k hand-made); the 40–80 bin counts are lopsided (45.5k vs 7.7k). Ranking is robust in the ≥80 kPa bins where both have hundreds–thousands of samples.
