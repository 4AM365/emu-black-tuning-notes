---
name: emu-black-lambda-tracking
description: >-
  Scores how tightly an EMU Black fuel map tracks its lambda target from a CSV log,
  and compares map versions (e.g. hand-built vs machine/autotune-smoothed). Use
  whenever the user wants to "how well does my fuel map track", "lambda tracking
  error", "is my AFR on target", "compare these two maps", "did the autotune improve
  tracking", "tracking spread by load". Metric is percent off target,
  err% = (Lambda1/Lambda_target − 1)·100 (so an error at a rich 0.80 target is
  comparable to one at 0.98); reports bias (mean) and spread (std/RMS) overall and by
  MAP load bin. err% is commanded-vs-measured, so it's fuel-agnostic — flex-fuel
  ethanol variation between logs does NOT confound it. Takes logs as arguments, or
  named --group sets for A/B; optional plot. Pairs with emu-black-ve-smooth.
---

# EMU Black lambda-tracking quality

`err% = (Lambda1 / Lambda_target − 1) · 100`, over valid windows (target 0.70–1.02,
measured 0.60–1.30, RPM > 1200, MAP ≥ 40 — drops DFCO/overrun sentinels). Reports:

- **bias** (mean err%) = calibration centering — separately trimmable, *not* a
  smoothness signal.
- **spread** (std / RMS err%) = tracking tightness — **this** is what map smoothness
  affects.

…overall and **by MAP load bin**. Map quality shows in the **high-MAP / boost** bins,
where closed-loop STFT is typically off so tracking error is pure feed-forward (map)
quality; low-load cruise tracks tightly regardless of smoothness.

## Usage

```bash
# single map (one or more logs pooled)
python scripts/lambda_tracking.py LOG1.csv LOG2.csv [--plot out.png]

# A/B comparison of two map generations
python scripts/lambda_tracking.py \
    --group "hand=a.csv,b.csv" --group "machine=c.csv" \
    [--shift "machine=-3"] [--plot out.png]
```

- `--group NAME=p1,p2,...` named log sets for comparison.
- `--shift NAME=pct` removes a known **constant** mixture offset (e.g. a map not
  re-scaled after per-cylinder trims reads uniformly lean) so you compare *shape*; a
  constant shift doesn't change std, so the spread comparison is unaffected.
- `--meas` / `--target` override channel names. `--plot` needs matplotlib; tables
  always print.

## Related

- `emu-black-ve-smooth` (smoother maps track tighter), `emu-black-knock-cov`
  (combustion-CoV companion). Method: `ai-analysis-skills/lambda_tracking_map_smoothing.md`.
