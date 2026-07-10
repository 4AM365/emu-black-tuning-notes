# Knock-chatter CoV results

> Digest of [knock_chatter_cov_results.md](../knock_chatter_cov_results.md) — the dense note is canonical; if they disagree, it wins.

**Finding (May 2026 logs, e.g. `20260524_1301`; machine-smoothed log is the newest):** after operating-point detrending, the machine-smoothed VE map runs tighter combustion than the hand-made map in **every** overlapping RPM bin — overall knock-chatter CoV 19.0% vs 25.9%, best bin 11.5% vs 30.8% at 3.5–4k rpm.

**So-what:** clean, consistent confirmation that the autotune/machine-smoothed map is the more stable calibration. Keep it as the base; don't fall back to the hand-built one.

**Method note:** on this car MAP > 130 kPa is ~98% transitional anyway, so the transition gate barely filtered anything — the operating-point detrend (RPM 250 × MAP 10 kPa cells) is what made the comparison valid.

**Caveats:** machine-smoothed evidence is one log (363 transition samples, 3.7–5.9k rpm, nothing above 6k), and ethanol blend was not controlled between logs.
