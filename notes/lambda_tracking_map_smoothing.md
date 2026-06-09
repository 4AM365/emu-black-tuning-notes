# Lambda tracking: hand-made vs machine-smoothed map

> **Car-specific values live in the build working docs**, not here. For the reference build's measured tracking-spread tables see [`supra/notes/lambda_tracking_results.md`](../supra/notes/lambda_tracking_results.md). This note is intentionally car-agnostic.

Companion to `notes/knock_voltage_cov_combustion_stability.md`. Does the AI/machine-smoothed
fuel map track its lambda target better than the hand-built map? Script:
`supra/scripts/lambda_tracking.py`.

## Metric

Tracking error as **percent off target**: `err% = (Lambda 1 / Lambda target − 1)·100`.
Percent (not raw lambda) so an error at a rich target (0.80) is comparable to one near 0.98.
Separate two things:
- **bias** (mean err%) = calibration centering — separately trimmable, NOT a smoothness signal.
- **spread** (std err%) = tracking tightness — THIS is what map smoothness affects.

Filters: valid windows only (target 0.70–1.02, measured 0.60–1.30), RPM > 1200, MAP ≥ 40 kPa
(drops decel/overrun fuel-cut sentinels where target→0 and the WBO rails lean). err% is
commanded-vs-measured so it is **fuel-agnostic** — flex-fuel ethanol variation between logs
does not confound it (unlike absolute VE). lambdaDelay is active and logged Lambda is already
time-aligned to its cell, so same-row measured-vs-target is valid.

Where it shows: in boost / higher load, closed-loop STFT is typically off, so tracking error
there is pure feedforward (map) quality. Low-load cruise is closed-loop and tracks tightly
regardless of map smoothness — read the high-MAP bins for the map-quality signal.

## Result (hand-made = all human-map logs; machine-smoothed = the smoothed-map log)

Compare tracking-error **spread (std %)** by MAP load bin — lower = tighter tracking. For
this build's measured spread-by-bin numbers see `supra/notes/`. The qualitative finding:

**Machine-smoothed tracks markedly tighter everywhere in and above the boost-entry region** —
spread nearly halves in boost. Same load region where combustion CoV improved: smoother
cell-to-cell dose → less feedforward error as you interpolate across cells → measured lambda
hugs target. The lowest cruise bin is a wash / marginally wider for machine — expected, since
that's closed-loop deadband where the map's feedforward smoothness is masked.

**Bias is a known artifact — remove it and compare shape.** The machine-smoothed map can read
uniformly lean of target if the whole map was **not re-scaled after the per-cylinder trims**
(a global mixture offset, not a tracking fault). The analysis applies a constant percent
correction to the machine-smoothed errors (`SHIFT` in the script). A constant shift does not
change std, so the spread comparison is unaffected — it already measures pure shape. After
re-centering, the distributions overlay near zero and the point is plain: the machine-smoothed
error distribution is **taller and narrower** (and far tighter in the boost bins), while the
hand-made distribution is broad and skewed rich. The whole *shape* is tighter; the residual
offset is a one-number global fuel-scale fix.

Caveats: machine-smoothed is typically a single log vs many hand-made logs, and the cruise-bin
sample counts are lopsided. Ranking is robust in the higher-MAP bins where both maps have
hundreds–thousands of samples.
