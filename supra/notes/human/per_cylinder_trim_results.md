# Per-cylinder trim results

> Digest of [per_cylinder_trim_results.md](../per_cylinder_trim_results.md) — the dense note is canonical; if they disagree, it wins.

**Finding (post-trim log `test-run-2.csv`; trim profile worked 2026-05-31):** with 2% cyl3 / 9% cyl6 trims active, the cyl6−cyl3 EGT delta is within ±20 °C in every load region, and cyl6 now runs slightly colder — **the 2%/9% choice is validated**, with cyl6 mildly over-trimmed at boost (~−1%).

**So-what:** the rich-biased export (cyl6 +13 cruise, cyl4/5 +7/+12) is too rich. Revert cyl6 to ~9% ([7,9,8,8,7], maybe shave the boost cell −1) and scale cyl4/5 proportionately (~+5/+7, at most +1 safety bias).

**Pre-trim context:** the EGT delta shrank as load rose (+44 °C cruise → +12 °C boost) — that load-dependence means real FFIM airflow maldistribution, not a fixed sensor offset. A one-time probe swap between 3 and 6 is the only way to separate any residual probe offset.

**Before/after (2026-10-02, 119 decoded autosaves):** trim went live **May 4 2026, 17:25–17:38**; ethanol was 57 % on both sides, so the 5 weeks before vs 6 days after is a same-fuel test.
- Idle: cyl 6 knock spikes (> 2× normal) 0.082 → 0.005 % of samples; cyl 4 also fell, untrimmed cyl 1 didn't. Spiky idle drives (Apr 20 – May 1) stopped on May 4. RPM jitter 1.03 → 0.95 %, lambda jitter 0.79 → 0.59 %. Misfire proxies (same fuel): sharp RPM sags 10–25 rpm −37…−54 %, lean lambda blips −33…−48 %; sags drifted back up after May 11, lean blips kept falling.
- Boost: cyl 6 spikes 0.77 → 0.29 → 0.17 %, but every cylinder fell and boost overshoot (peaks to 105–136 kPa before) stopped at the same time, so not the trim alone. Cruise spikes went up.
- EGT cyl6 − cyl3: light +38 → +4 °C, cruise +27 → +1 °C, idle +42 → +24 °C.
- The earlier CSV-only pass (boost ceiling up, no idle or knock change) was wrong: too little pre-trim data, medians instead of spikes.
Charts: `supra/reports/2026-10-02_cyl6_trim_knock_boost/report.html`.

**Risk / next step:** cyls 2, 4, 5 are extrapolated, not measured — cyl4/5 could be leaner than estimated with nothing to catch it. Priority is the EGT-to-CAN module so 4 and 5 get measured trims.
