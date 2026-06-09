# EMU Black tuning notes — index

These notes are organized to mirror the **EMU Black tuning software's own feature tree**: one page
per top-level software node. Each page leads with **Settings** (the EMU tables for that page) and
closes with the **Principles** behind them, where we have them. The exhaustive, every-symbol catalog
is [tune_feature_tree.md](tune_feature_tree.md).

## Pages (software tree order)

1. [Sensors and inputs](sensors_and_inputs.md) — TPS/PPS, MAP/BARO, IAT/CLT, O₂, EGT, pressure, VSS, switches
2. [Engine start](engine_start.md) — cranking, sync, ASE
3. [Fueling](fueling.md) — VE, lambda, flex, per-cylinder trim, accel enrichment
4. [Ignition](ignition.md) — timing tables, dwell, flex blend _(deep reference: [timing.md](timing.md))_
5. [Overrun](overrun.md) — DFCO, exit enrichment, overrun ignition/throttle
6. [Knock sensors](knock_sensors.md) — detection, retard, CoV/uniformity reading
7. [Idle](idle.md) — airflow tables, DBW range/blend, idle PID, idle ignition
8. [Functions](functions.md) — cruise, fan/AC, custom functions
9. [Outputs](outputs.md) — PWM, GP outputs, electrical aux
10. [Boost](boost.md) — WGDC, boost target, PID, anti-lag
11. [DBW](dbw.md) — characteristic, rate limit, motor/limits
12. [Traction control](traction_control.md)
13. [VVT](vvt.md) — cam target, PID, setpoint
14. [Sport](sport.md) — launch, flat-shift, pit limiter
15. [Nitrous](nitrous.md)
16. [Tables switching](tables_switching.md) — flex blend selectors
17. [Engine protection](engine_protection.md) — stuck-throttle, rev limiter, protection limits
18. [Timers](timers.md)
19. [DSG Gearbox](dsg_gearbox.md)
20. [Other](other.md) — engine setup, start/stop, base config, axis bins
21. [CAN, Serial](can_serial.md) — CAN stream, OEM integration, keypads
22. [Log](log.md) — logging config, virtual dyno
23. [Gauges](gauges.md)

## AI / data-analysis skills → [`../ai-analysis-skills/`](../ai-analysis-skills/)

The log/data-analysis *methods* (VE-from-log correction, delta-overlay smoothing, VE-vs-MAP
shaping, lambda-tracking scoring, knock-CoV and idle-RPM-CoV) live in their own sibling folder,
[`../ai-analysis-skills/`](../ai-analysis-skills/). They're techniques, not EMU software pages.

## Cross-cutting reference notes

Physics/principle deep-dives the pages link into (not software pages):

- [cammed_idle_instability.md](cammed_idle_instability.md) — why a diluted idle charge is unstable
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — two-PID idle architecture + windup fix
- [idle_stall.md](idle_stall.md) · [return_to_idle_bog.md](return_to_idle_bog.md) — idle diagnostics
- [timing.md](timing.md) — MBT tables + cruise/boost/VVT methodology
- [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md) — knock variance as a uniformity proxy
- [lambda_target_vs_load.md](lambda_target_vs_load.md) · [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md) · [ve_ethanol_table_charge_cooling.md](ve_ethanol_table_charge_cooling.md) · [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md)
- [throttle_feel.md](throttle_feel.md) · [throttle_body_thermal_growth.md](throttle_body_thermal_growth.md) · [stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md)
- [hood_removal_charge_temps.md](hood_removal_charge_temps.md) · [denso-coils.md](denso-coils.md)

Car-specific live values live in [`../supra/notes/`](../supra/notes/).
