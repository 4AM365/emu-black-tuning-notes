# Per-cylinder trim results

> Digest of [per_cylinder_trim_results.md](../per_cylinder_trim_results.md) — the dense note is canonical; if they disagree, it wins.

**Finding (post-trim log `test-run-2.csv`; trim profile worked 2026-05-31):** with 2% cyl3 / 9% cyl6 trims active, the cyl6−cyl3 EGT delta is within ±20 °C in every load region, and cyl6 now runs slightly colder — **the 2%/9% choice is validated**, with cyl6 mildly over-trimmed at boost (~−1%).

**So-what:** the rich-biased export (cyl6 +13 cruise, cyl4/5 +7/+12) is too rich. Revert cyl6 to ~9% ([7,9,8,8,7], maybe shave the boost cell −1) and scale cyl4/5 proportionately (~+5/+7, at most +1 safety bias).

**Pre-trim context:** the EGT delta shrank as load rose (+44 °C cruise → +12 °C boost) — that load-dependence means real FFIM airflow maldistribution, not a fixed sensor offset. A one-time probe swap between 3 and 6 is the only way to separate any residual probe offset.

**Risk / next step:** cyls 2, 4, 5 are extrapolated, not measured — cyl4/5 could be leaner than estimated with nothing to catch it. Priority is the EGT-to-CAN module so 4 and 5 get measured trims.
