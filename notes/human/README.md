# Human digests — index

Tight half-page versions of the dense notes in [`notes/`](../README.md). Each digest is a
derived view: **the canonical note always wins**, and edits happen there first. Format:
What this covers / The rules / Key numbers / When to care.

## EMU software pages

- [Sensors and inputs](sensors_and_inputs.md) — fix sensors before maps; how the VR trigger's adaptive threshold really works
- [Cranking and cold-start](engine_start.md) — post-start stumbles are air/timing, not fuel; cranking airflow sets the flare
- [Fueling](fueling.md) — VE is the dose, lambda target isn't a multiplier; correcting fuel from logs
- [Ignition — EMU settings hub](ignition.md) — which EMU ignition table owns each job, five principles behind them
- [Overrun](overrun.md) — return-to-idle stalls are airflow, not fuel; cut fast, restore slow
- [Knock sensors](knock_sensors.md) — detection setup, retard, and reading knock voltage as combustion quality
- [Idle](idle.md) — which of the two idle PIDs and airflow tables fixes which idle problem
- [Boost control](boost.md) — feed-forward WGDC first, pedal-shaped torque targets, and the v2/v3 absolute-vs-gauge table trap
- [DBW / throttle](dbw.md) — throttle feel levers, rod protection, brake-boost-safe stuck-throttle logic
- [VVT (VVT-i)](vvt.md) — cam advance moves MBT; lock cam per cell before ignition, tune fully hot
- [Sport (launch control / 2-step)](sport.md) — launch-control gating, V2 vs V3 symbols, why Andrew's 2-step arms intermittently
- [Tables switching (flex-fuel blend)](tables_switching.md) — derive the blend curve from fuel scale; tune endpoints, never the blend
- [Engine protection](engine_protection.md) — PPS-referenced layers first, permissive brake box — this car brake-boosts
- [CAN, Serial — topology and termination](can_serial.md) — two 120 Ω total, 30 cm stubs, and the 60 Ω check that catches every mistake

## Principles, diagnostics, and hardware

- [Ignition timing — the deep reference](timing.md) — CA50 at MBT, and how cams, fuel, and load move the target
- [EMAP/MAP ratio and cam overlap](emap_map_ratio_cam_overlap.md) — the pressure ratio decides whether overlap helps; VVT scheduling from it
- [Valve timing and dynamic compression](valve_timing_dynamic_compression.md) — what advancing the intake cam does to IVC, DCR, and overlap
- [Piston-to-valve clearance and cam advance](piston_valve_clearance_cam_advance.md) — how much cam advance before the valve kisses the piston
- [Intake runner resonance and the VE table](intake_runner_resonance.md) — why you can't read runner length off a smoothed VE table
- [Knock frequency — bore sets the band](knock_frequency.md) — bore alone sets the filter band; nothing else moves it enough
- [Knock baseline grumble = cylinder uniformity](knock_sensor_baseline_vs_cylinder_uniformity.md) — baseline wander reveals maldistribution before any knock spike
- [Idle stall troubleshooting](idle_stall.md) — eight stall patterns, log-first triage, and the one fix each needs
- [Why cammed builds idle badly](cammed_idle_instability.md) — overlap dilution physics and the levers that pull idle back from misfire
- [Return-to-idle bogging](return_to_idle_bog.md) — four root causes of the coast-down bog, sync loss checked first
- [Hot-idle drift and the two-PID windup fix](idle_hot_drift_pid_windup.md) — ignition owns the fast knockdown; cap the airflow integral independently
- [Throttle response tuning](throttle_feel.md) — characteristic map beats rate limit; fixing creep, lift-off, and the handoff bump
- [Stuck-throttle protection vs. brake boosting](stuck_throttle_protection_brake_boost.md) — pedal-referenced layers protect; the brake box stays permissive
- [Exhaust note tuning](exhaust_noise_tuning.md) — source vs filter decides which part moves pitch, drone, and rasp
- [Flex-fuel blend curves](flex_fuel_ethanol_compensation_blend.md) — derive blend weights from the fuel-scale table, never a straight line
- [Injector dead-time calibration](injector_deadtime_calibration.md) — manufacturer data onto the voltage-pressure grid; extrapolate edges, verify row order
- [Per-cylinder trim on the front-feed manifold](per_cylinder_trim_ffim_distribution.md) — constant front-to-rear bias, RPM-axis resonance
- [Lambda target vs load](lambda_target_vs_load.md) — flat then linear rolloff; spend bins on the knee, not the straight
- [VE tables are fuel-dose, not air physics](ve_ethanol_table_charge_cooling.md) — lower ethanol VE is expected; the stoich lives in ethanolFuelScale
- [Spark delta for the cam + compression change](spark_delta_cam_cr_change.md) — both changes add advance, +4° light-load corner tapering to +2°
- [Throttle body thermal growth](throttle_body_thermal_growth.md) — how much hot-idle correction TB expansion physics actually justifies
- [Denso / Toyota coil reference](denso-coils.md) — coil part numbers, dwell limits, and connectors for standalone builds
- [Functions](functions.md) — user functions as virtual inputs (Fn n = 19 + n in the XML), empty operators use slots, False delay as a debounce, XML byte layout
- [Tune feature tree](tune_feature_tree.md) — every tunable symbol filed under the software's 23 pages (catalog pointer)

## Already tight — read the original

These canonical notes are under ~25 lines and need no digest:
[hood_removal_charge_temps](../hood_removal_charge_temps.md) ·
[log](../log.md) · [other](../other.md) ·
[outputs](../outputs.md) ·
[traction_control](../traction_control.md) · [timers](../timers.md) ·
[nitrous](../nitrous.md) · [gauges](../gauges.md) · [dsg_gearbox](../dsg_gearbox.md)

Car-specific digests: [`../../supra/notes/human/`](../../supra/notes/human/README.md)
