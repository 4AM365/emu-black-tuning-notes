# Throttle body thermal growth

> Digest of [throttle_body_thermal_growth.md](../throttle_body_thermal_growth.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** a physics bound on how much hot-idle airflow correction throttle-body expansion alone justifies — the sanity check for `idleCustomCorrection`. Car-agnostic; plug in your bore, plate material, and idle TPS.

**The rules:**

- Idle air flows through the radial clearance around the plate edge, not the tilt gap — at 3–5° throttle the plate still blocks nearly its whole disc.
- Stainless or nickel-silver plate in an aluminum bore: the gap opens as it heats (bore outruns blade), so closed-throttle leakage rises hot. Compensate as a temperature-indexed offset, not a fixed DBW floor.
- Idle flow is choked, so mass flow scales directly with area — fractional area growth is the airflow increase.
- The correction must be more negative at lower idle RPM: smaller idle TPS means clearance dominates, so the same absolute growth is a bigger fraction. That monotonic trend is the fingerprint of a physically grounded table.
- The physics prediction is a starting point and an upper bound. Corrections beyond it need a specific logged reason, not extrapolation.
- ΔT is the TB body's swing from the temp the airflow table was calibrated at — not the CAT reading, which leads or lags the body. At idle the body runs closer to coolant temp, so real ΔT may exceed what the sensor suggests.
- A brass plate cuts the differential ~3× — a table tuned for a stainless blade over-corrects on brass. Re-derive if the TB or blade changes.

**Key numbers:** differential CTE vs aluminum bore — stainless/nickel-silver ~4.5–5.3 ppm/°C, brass ~1.5 ppm/°C; flow is choked below MAP ≈ 0.528 × atmospheric.

**When to care:** tuning or auditing hot-idle corrections, and after any throttle-body swap or blade-material change.
