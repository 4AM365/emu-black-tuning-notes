# Oil temperature versus coolant temperature as an idle-airflow reference

## Decision

**Do not substitute oil temperature for coolant temperature.** Keep coolant temperature as
the reference for cold-engine combustion, port/wall temperature and throttle-body thermal state;
add oil temperature as an independent, smooth *idle-airflow correction* (or, if firmware forces
it, a post-start-time proxy).  A coolant-to-oil heat exchanger can shorten the time for which
that oil correction is large, but cannot make the two inputs interchangeable.

This is specifically about idle / DBW airflow feed-forward. It is not an argument for using
either fluid temperature to calculate inducted-air density: speed-density mass is set by MAP and
the temperature of the inducted charge, `m_air = MAP * V_d * VE / (R_air * T_charge)`.

## Why two inputs are identifiable on the Supra

The active-airflow base table is natively indexed by CLT (`cltBins8 = 0/15/30/45/60/75/96/105 C`).
The usable correction path is the active-only custom-airflow table.  The last readable export
checked (`supra/exports/ind deadtime rescale.xml.emub3`) has an unassigned oil-temperature input
(`oilTempInput = 0`) and an unsafe-for-air-subtraction fail-safe (`oilTempFailSafe = 100 C`).

The measured requirement is non-single-valued versus either temperature alone:

| Same stated condition | Required total idle air | TPS, using 2.4–8.0% actuator range |
|---|---:|---:|
| CLT = 96 C, oil still cold | 51–58% | 5.2–5.6% |
| CLT = 96 C, oil hot | 28–31% | 3.9–4.1% |
| Missing feed-forward if CLT alone selects hot-oil value | +20 to +29% | +1.1 to +1.6% |

`TPS = 2.4 + 0.056 * airflow_percent`, so a representative 25-airflow-point oil-state
error is **1.40% TPS**.  That is too large to delegate to a delayed idle loop during a
return-to-idle event.

Conversely, oil cannot stand in for CLT. At cold start oil and coolant begin near the same
temperature, but the coolant-indexed base has a genuine cold-engine term (cold port/wall fuel
behavior and quick throttle-body/metal changes). The measured cold-CLT base excess is about +27
airflow points at <=35 C, +16 at 35–55 C, +6.5 at 55–80 C and about zero above 80 C. Replacing
the CLT axis with oil would erase or mis-time that term.

The usable form is therefore additive decomposition, calibrated from steady holds:

`air_ff(RPM, CLT, T_oil) = base(RPM, CLT) + oil_correction(RPM, T_oil) + accessory_corrections`

Do not use raw oil pressure as a substitute for a temperature axis across a multi-RPM armed
range: pressure contains pump-speed and relief-valve effects as well as viscosity. It can be a
fixed-idle-RPM empirical trim only when its pressure/temperature relation has been logged.

## Heat exchanger: what it changes

For a liquid-liquid exchanger, the instantaneous transferred heat is approximately

`Qdot_hx = epsilon * C_min * (T_hot - T_cold)`,

where `C = mdot * cp`; equivalently it is `UA * LMTD` for a steady exchanger. The coupled fluid
energy balances contain opposite signs:

`C_oil dT_oil/dt = Qdot_oil_sources + Qdot_hx - Qdot_oil_rejection`

`C_clt dT_clt/dt = Qdot_combustion - Qdot_radiator - Qdot_hx`.

During a normal cold start, coolant/head metal normally warm faster than bulk oil, so
`T_clt > T_oil`, `Qdot_hx > 0` into the oil, and the exchanger reduces the large cold-oil airflow
adder sooner. At sustained high load, oil can be hotter than coolant, reversing the sign; then
the exchanger is valuable as an oil cooler. This sign reversal is why an exchanger **narrows**
the temperature difference but cannot guarantee equality or justify deleting either ECU input.

Control implication: a thermostatic/bypassed oil-to-coolant exchanger is preferable to a
permanently-maximal coupling.  It should pass heat into oil during a genuine coolant-hot/oil-cold
condition, retain enough oil-temperature margin for load, and preserve high-load oil rejection.
Whether to bypass during early warmup is system-specific: if coolant is colder than oil or the
radiator path is already removing heat, coupling can cool the oil instead of helping it.

## Implementation and safety

1. Add a calibrated oil-temperature sensor at a repeatable, relevant location (gallery feed or
   post-exchanger oil outlet; record the exact location). Do not infer temperature from pressure.
2. Retain the CLT-indexed base table. Use the existing custom correction path only if its axis can
   be assigned to oil temperature; otherwise use a CLT + elapsed-running-time decay as the
   conservative proxy.
3. Make the oil correction monotonic and rate-limited: more air cold, tapering toward zero at the
   measured fully-hot oil temperature. Leave the base with enough cold-oil air for ARMED/non-active
   states, because the custom correction is active-only.
4. If the oil correction subtracts air as oil warms, set the ECU's oil-temperature fail-safe to
   the **cold** side/below the first bin, not the currently configured 100 C. A missing sensor must
   command extra air, not maximum subtraction and a stall.
5. Log CLT, actual oil temperature, oil pressure, IAT/charge temperature, fan, A/C, target RPM,
   idle state, base/custom/PID airflow and TPS through (a) cold start, (b) 15+ minute idle, (c)
   hot restart, and (d) a high-load cool-down. Refit only from stable, same-calibration segments.

## 2026-08-30 decision and current graphing rule

The owner retired oil-pressure compensation because the control variable is circular/confounded by
oil-pump speed, relief behavior, and the control response it is meant to correct. The replacement
is an actual oil-temperature sensor and oil-temperature-indexed correction; oil pressure remains a
protection/diagnostic channel only.

Until that sensor is installed, an oil-temperature trace may be shown only as an explicitly
**inferred** visualization axis. For the 08:47 `latestdrivevischan.csv` warm-up chart, the
inference is `T_oil(t) = 112 - 75 exp(-t / 6.16 min)` C: it starts at the observed 37 C cold
condition and tends to the previous hot-oil 112 C estimate. It is a historical time model, not a
measurement and not a calibration input. The plotted 96-C excess is median
`Idle airflow custom corr. + Idle PID air % correction` from ACTIVE,
target-1025-rpm, CLT-95.5–97.5 C windows; fan correction is explicitly 0. The plot marks the
in-log removal of the old pressure correction at about 20.25 minutes; do not fit one continuous
thermal curve across that calibration change.

## Sources

- Local primary working evidence: `supra/notes/oil_viscosity_idle_airflow.md`, esp. Evidence base
  and Results 1/8; `supra/notes/oil_pressure_airflow.md`; `supra/notes/idle_drive_wobble.md`.
- Heywood local extract: `corpus/ice_fundamentals.md`, pp. 1237–1239 (oil lags coolant during
  warm-up) and pp. 1311–1313 (friction is strongly oil-temperature dependent).
- Banish local extract: `corpus/engine_management_advanced_tuning.md`, temperature-sensor and
  speed-density sections (charge temperature is the density input; coolant is a thermal/engine-state
  signal).
- Andrews et al., SAE 2007-01-2067, coolant/lube-oil exchanger during cold start.
- Di Battista et al., *Applied Energy* 162 (2016) 570–580, doi:10.1016/j.apenergy.2015.10.127.
