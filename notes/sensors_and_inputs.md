# Sensors and inputs — EMU Black settings and the principles behind them

> **Software page:** *Sensors and inputs* (the largest page — 397 symbols). Full symbol catalog: [tune_feature_tree.md → Sensors and inputs](tune_feature_tree.md). Most entries are hardware calibration/config; this page captures the **setup discipline and the tuning principles that depend on good sensor data**, organized by the software's sub-nodes.

> **Car-specific values live in the build working docs.** Sensor cal is hardware-specific — read it
> from the live export, don't assume.

---

# Part 1 — Settings (by software sub-node)

### TPS, PPS
The throttle/pedal sensors. Main + check (redundant) signal inputs, 0%/100% voltages, valid range,
and error tolerance. The **dual-TPS plausibility** check (`Check signal input`) is the highest-value
safety upgrade — see [engine_protection.md](engine_protection.md). The PPS→TPS *map* (DBW
characteristic) is on [dbw.md](dbw.md), not here.

### IAT, CLT
Charge-air and coolant temperature. **Lock these down before chasing idle** (P1). CLT feeds the idle
ref table, warmup enrichment, ASE, and fan logic simultaneously, so CLT noise oscillates all of them.

### MAP, BARO
Manifold and barometric pressure. Built-in vs external MAP, 5 V cal, baro source. The load axis for
fuel/ignition; the idle mass-flow estimator built on it **lies at idle** (P2).

### Oxygen Sensor
Wideband (`wbo*`) and optional second wideband hardware config: AFR-at-0V/5V, fuel type, heater PID,
pump PID, external controller input. The closed-loop *logic* (lambda target, STFT) is on
[fueling.md](fueling.md); this sub-node is the **sensor hardware**. `lambdaDelay` alignment is P3.

### Pressure
Oil, fuel, coolant, crankcase, diff, back-pressure, pre-throttle boost, wastegate-dome pressure cals.
Oil/fuel pressure feed protection limits ([engine_protection.md](engine_protection.md)).

### Temperature
Oil temp, cylinder-head temp, fuel temp, and the custom temp-sensor calibrations
(`customTemp1..4CalBins`). Re-cal whenever a sensor is swapped.

### Other sensors / EGT
EGT inputs and probe assignment (`cyl1..8EGTProbe`). **Put a k-type probe ~1 inch from the head**;
EGT is the primary MBT/distribution proxy (P4). Load-cell (shift) and generic sensors also land here.

### VSS and Gearbox
Vehicle speed and gear detection (`gearBins`, `vssBins`, driven/non-driven axle config). Feeds gear
correction, traction reference, and the VSS gates used by spool retention / fan correction.

### Analog inputs / Digital inputs / Switches
Raw input plumbing: `an1..6` pull-ups and digital filters, digital-input config, and switch
assignment (`invertSw*`, latching/mux switches). Set the switch polarity and debounce here; the
*functions* they trigger live on their own pages. **CAN keypads** (switch panels) are on
[can_serial.md](can_serial.md), not here.

---

# Part 2 — Principles

## P1. Lock the sensors before tuning idle (and everything else)

Noisy CLT or VVT feedback pushes idle "all over the place" — CLT noise makes the idle ref table,
warmup, ASE, and fan logic oscillate together; VVT angle noise corrupts breathing. A noisy sensor is
a **wiring/hardware issue, not a calibration one** — chasing it in the maps never converges. Check for
1–2 °C CLT jitter or ±5° VVT oscillation at steady idle and fix the signal first
([idle_stall.md §E](idle_stall.md)).

## P2. The mass-flow estimator lies at idle

At idle the high reverted flow through the throttle reads as airflow even though most of it is exhaust
going back out — the channel can overstate true combustion airflow by ~10×. **Don't validate idle VE
against it.** See [supra/notes/mass_flow_estimator_quirk.md](../supra/notes/mass_flow_estimator_quirk.md),
[cammed_idle_instability.md](cammed_idle_instability.md).

## P3. Time-align the wideband before trusting cell attribution

`lambdaDelay` models the transport/measurement lag so the logged Lambda is realigned to the cell that
produced it. With it active, same-row measured-vs-target is valid even under acceleration — which is
what makes accel-bin VE attribution and lambda-tracking analysis trustworthy
([fueling.md](fueling.md), [lambda_tracking_map_smoothing.md](lambda_tracking_map_smoothing.md)).

## P4. EGT is the cheap truth sensor

EGT is the primary proxy for MBT at cruise (lower EGT → closer to MBT) and for cylinder-to-cylinder
distribution (rear-vs-front delta on a front-feed manifold). A $20 k-type probe ~1 inch from the head
on each runner is the single highest-value sensor add for a self-tuner ([ignition.md](ignition.md),
[fueling.md → F4](fueling.md), [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md)).

---

## Related documents

- [dbw.md](dbw.md) — TPS/PPS *map* (the characteristic) and DBW motor
- [engine_protection.md](engine_protection.md) — dual-TPS plausibility, oil-pressure protection
- [fueling.md](fueling.md) — wideband closed-loop logic, `lambdaDelay`, per-cylinder EGT trim
- [supra/notes/mass_flow_estimator_quirk.md](../supra/notes/mass_flow_estimator_quirk.md) — why idle airflow reads ~10× high
- [supra/notes/throttle_body_thermal_growth.md](../supra/notes/throttle_body_thermal_growth.md) — TB temp vs sensor temp lag
