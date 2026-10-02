# Human digests — Supra-specific notes

Tight half-page versions of the dense notes in [`supra/notes/`](../). Derived views —
**the canonical note always wins**, and edits happen there first.

- [The car — build sheet and constants](my_car.md) — hardware list, calibration constants, and the 5500 rpm resonance caution zone
- [Sensor and switch inventory](sensor_inventory.md) — every input with type, 5/12 V supply and ground requirement; which ones must be on sensor ground
- [Timing targets (10:1 CR, E60)](timing_targets.md) — WOT timing by boost level, boost ceilings, and the cost of retard
- [Airflow / idle DBW calibration reference](airflow_actuator.md) — live actuator range, airflow tables, PID gains, and rescale rules
- [Throttle body thermal growth (ES330 TB)](throttle_body_thermal_growth.md) — bore outgrows plate when hot; physics validates the idle correction table's shape
- [Hood removal vs charge temps](hood_removal_charge_temps.md) — hoodless drops charge temp 5–8 °C; sensor cal fixes needed before reading logs
- [Rolling return-to-idle wobble](idle_drive_wobble.md) — three measured faults behind coast-down RPM craters: rich VE, fan gate, MAP lockout
- [Oil-viscosity idle-airflow compensation](oil_viscosity_idle_airflow.md) — cold oil under hot coolant needs ~1.8× the idle airflow; the measured adder is ≈ +25 airflow %
- [Idle airflow by oil-pressure bin](oil_pressure_airflow.md) — the raw RPM × CLT measurement under that note; only 25 of 200 cells are reachable
- [Mass-flow estimator quirk at idle](mass_flow_estimator_quirk.md) — cam reversion makes the idle mass-flow channel read ten times too high
- [Idle session — 2026-05-24](idle_session_05242026.md) — saturated PID means fix the base airflow table, not the limits
- [Idle RPM stability results](idle_rpm_stability_results.md) — idle scatter is a 0.59 Hz PID hunt, not combustion; fix the loop
- [Per-cylinder trim results](per_cylinder_trim_results.md) — 2%/9% trims validated within ±20 °C; rich-biased export needs reverting
- [Knock-chatter CoV results](knock_chatter_cov_results.md) — machine-smoothed map beats hand-made in every RPM bin for combustion stability
- [CAN breakout node (footwell)](can_breakout_node.md) — DTM junction box plan; which device earns the second 120 Ω and why
- [Clutch load at idle](clutch_idle_load.md) — measured at ~1/15th of the A/C load and mostly unpredictable; don't feed it forward
- [A/C request input noise](ac_request_input_noise.md) — the request line chatters only while the owner-installed clutch switch is energized and the compressor is off; it is cycling the compressor
- [Speed-signal integrity](vss_signal_integrity.md) — the VSS input glitches to 80 km/h at a standstill; that noise is what makes the idle open-loop gate chatter and wipe both PID integrals
- [Idle bog + airflow hump (2026-08-30)](idle_bog_and_airflow_hump_20260830.md) — the bog is four subtractions on one descent; the airflow "hump" is the oil-pressure table and the PID cancelling each other
- [Idle knife edge — 2026-09-19](idle_knife_edge_2026-09-19.md) — no cylinder out; engine air demand unchanged; the sustaining plate position moves ~1 % TPS on the oil/TB clock and the DBW servo's stall point wanders 4 % — the PID rails are saturation, not gain
- [Throttle-body cleaning — 2026-09-19](tb_clean_2026-09-19.md) — the wandering servo was carbon: hot sustaining position 5.9 → 2.9/2.4 % TPS (plus a −1.09 relearn frame shift), plate-stuck time 20 % → 1.5 %; engine air unchanged and ∝ RPM; duty sweep (break-away closed −28…−31, rest 6.3–6.6); derived Active/Armed starting tables for the 1.5–6.5 window (rows must fan out with RPM on a clean TB)
- [Running dataset — OP vs DBW duty at 1000 rpm](op_vs_dbw_1000rpm.md) — re-runnable file; DBW duty has no relationship to oil pressure, MAP×RPM is the only repeatable panel
- [CLT signal noise](clt_signal_noise.md) — coil-synchronous ground offset on the CLT run; ECUMaster's diagram returns CLT+IAT to B29 Sensor GND, and their glitches being *uncorrelated* says they aren't sharing it. Amplified by one broken `cltTbl` cell that reads 96 °C over a 9 °C-wide dead band. Fix the cell, count the sensor's pins, then the wiring
- [Log 2026-09-29 — afterstart dip, rich idle, sensor noise](log_2026-09-29_allchannels_smoothclt.md) — the dip is a limit cycle (airflow PID fed a spark demand the afterstart lock never delivers), not a kP fault; hot idle and the whole map run 6–13 % rich and IAT/charge temp does not explain it (wrong sign); the CLT/IAT rewire took voltage noise from 1.58 to 0.12 quanta
- [Log 2026-10-01 — fw 3.071, A/C at idle, cold start](log_2026-10-01_new_cranking_rules.md) — load warnings are new-feature defaults (but WBO cal tables and rev-limit cut percent were replaced); A/C idle cycling is request-line blips restarting the engage timer; measured A/C need +14.2 air-% at 1025; IAT is not ambient at idle; post-start wiggle = PID engaging at the overshoot peak
- [Starts 2026-10-02 — cranking dose vs need](log_2026-10-02_cold_hot_start.md) — anti-flood TPS scale cut cranking fuel 16 % cold / 9 % hot with no pedal; cold hovered lean on −17 % until the +68 % afterstart step; stepless target ≈ +40 % at ~29 °C; rail bleeds to 0 in 5 s; long hold good cold, hot handover mid-fall → 715 dip (A/C clutch engaged mid-hold — confounded)
- [Restart bounce with A/C on — 2026-10-02](log_2026-10-02_restartbounce.md) — relay loop between the no-hysteresis `acMinRPM` gate (drops clutch + custom corr together) and the re-engage timer; kP 0.5 helps the dip, not the relay; gate trips 12× in the log, lower it (~650) rather than raise
- [Cranking PW vs time to start](cranking_pw_vs_start.md) — running record of every logged crank: PW first second and at the end, cranking correction, first fuel → 750 rpm; the end-of-crank dose decides the time; regenerate with the scan script
- [Fuel-mixture parameter inventory](fuel_mixture_parameter_inventory.md) — every XML symbol that moves the mixture, by group; no fuel symbol changed between the on-target 09-19 export and 09-22; STFT's λ window is `shortTermMinLambda` ÷ 128 = 0.797
- [Idle airflow back-projected to cold](idle_cold_backprojection.md) — oil pressure is relief-capped below ~65 °C oil; cold requirement bounded L…H; the 6.5 ceiling binds below CLT ~45 at 1500 rpm on any cold start

## Already tight — read the original

[idle_hot_drift](../idle_hot_drift.md) · [lambda_tracking_results](../lambda_tracking_results.md)
