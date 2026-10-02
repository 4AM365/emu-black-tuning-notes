# Per-cylinder trim results

> Digest of [per_cylinder_trim_results.md](../per_cylinder_trim_results.md) — the dense note is canonical; if they disagree, it wins.

**Finding (post-trim log `test-run-2.csv`; trim profile worked 2026-05-31):** with 2% cyl3 / 9% cyl6 trims active, the cyl6−cyl3 EGT delta is within ±20 °C in every load region, and cyl6 now runs slightly colder — **the 2%/9% choice is validated**, with cyl6 mildly over-trimmed at boost (~−1%).

**So-what:** the rich-biased export (cyl6 +13 cruise, cyl4/5 +7/+12) is too rich. Revert cyl6 to ~9% ([7,9,8,8,7], maybe shave the boost cell −1) and scale cyl4/5 proportionately (~+5/+7, at most +1 safety bias).

**Pre-trim context:** the EGT delta shrank as load rose (+44 °C cruise → +12 °C boost) — that load-dependence means real FFIM airflow maldistribution, not a fixed sensor offset. A one-time probe swap between 3 and 6 is the only way to separate any residual probe offset.

**Before/after (2026-10-02, 119 decoded autosaves, binary split at the trim):** trim went live **May 4 2026, 17:25–17:38**. Before = Mar 1 → May 4, after = May 4 → Sep 29.
- Knock peaks, cyl 6 > 2× normal: idle 0.066 → 0.015 % (cyl 4 fell too, untrimmed cyl 1 rose); boost 0.58 → 0.19 % (every cylinder fell); cruise 0.048 → 0.42 % (rose).
- Idle misfire proxy (a misfire reads RICH; idle RPM unusable because of the TB issues): rich lambda blips > 0.02 λ 0.158 → 0.075 /min (−53 %), > 0.03 λ −69 %.
- EGT cyl6 − cyl3: light +44 → +9 °C, cruise +31 → −1 °C, idle +42 → +18 °C.
- The earlier CSV-only pass (no idle or knock change) was wrong. Boost levels aren't compared: boost control depends on other factors.
Charts: `supra/reports/2026-10-02_cyl6_trim_knock_boost/report.html`.

**Follow-up (2026-10-02):** knock voltage can't rank cylinders (each window has its own noise floor). Boost peaks are single-cylinder and sit at +2° more timing with λ on target; cruise peaks rose with +6° cruise timing after May 4 and with lower ethanol, as multi-cylinder bursts; cruise already runs rich of target. So the data point at timing, not whole-map enrichment. EGT (cyl 6 vs 3 only) says cyl 6 still wants ≈ +5–6 % at idle and 4000 rpm / 20 kPa, ≈ −3 % at 4000 / 130; the trim tables are RPM-flat but the residual isn't. Dwell was unchanged before/after; its within-cell wiggle is battery voltage tracking heat soak. Knock window is 10–60 °ATDC: the next cylinder's spark always lands after it; the next coil's charge start sits inside it at cruise in both periods.

**Risk / next step:** cyls 2, 4, 5 are extrapolated, not measured — cyl4/5 could be leaner than estimated with nothing to catch it. Priority is the EGT-to-CAN module so 4 and 5 get measured trims.
