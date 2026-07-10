# Human digests — Supra-specific notes

Tight half-page versions of the dense notes in [`supra/notes/`](../). Derived views —
**the canonical note always wins**, and edits happen there first.

- [The car — build sheet and constants](my_car.md) — hardware list, calibration constants, and the 5500 rpm resonance caution zone
- [Timing targets (10:1 CR, E60)](timing_targets.md) — WOT timing by boost level, boost ceilings, and the cost of retard
- [Airflow / idle DBW calibration reference](airflow_actuator.md) — live actuator range, airflow tables, PID gains, and rescale rules
- [Throttle body thermal growth (GS430 TB)](throttle_body_thermal_growth.md) — bore outgrows plate when hot; physics validates the idle correction table's shape
- [Hood removal vs charge temps](hood_removal_charge_temps.md) — hoodless drops charge temp 5–8 °C; sensor cal fixes needed before reading logs
- [Rolling return-to-idle wobble](idle_drive_wobble.md) — three measured faults behind coast-down RPM craters: rich VE, fan gate, MAP lockout
- [Mass-flow estimator quirk at idle](mass_flow_estimator_quirk.md) — cam reversion makes the idle mass-flow channel read ten times too high
- [Idle session — 2026-05-24](idle_session_05242026.md) — saturated PID means fix the base airflow table, not the limits
- [Idle RPM stability results](idle_rpm_stability_results.md) — idle scatter is a 0.59 Hz PID hunt, not combustion; fix the loop
- [Per-cylinder trim results](per_cylinder_trim_results.md) — 2%/9% trims validated within ±20 °C; rich-biased export needs reverting
- [Knock-chatter CoV results](knock_chatter_cov_results.md) — machine-smoothed map beats hand-made in every RPM bin for combustion stability

## Already tight — read the original

[idle_hot_drift](../idle_hot_drift.md) · [lambda_tracking_results](../lambda_tracking_results.md)
