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
Wiring per ECUMaster's diagram: two-terminal sensors, signals to **B5** (CLT) and **B32** (IAT),
both second terminals **commoned to B29 Sensor GND** — never engine or chassis ground. Fixed
internal **2K2** pull-up, enabled by a bool (`cltPullup`/`iatPullup`); no value selector and no
digital filter on these two inputs. Noise diagnosis method: P5.

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

### Primary / cam trigger — VR adaptive threshold (how it works)
The EMU VR input is an **adaptive-peak-threshold + zero-crossing** conditioner (MAX9924–27 class;
ECUMaster help: "adaptively adjusts sensitivity, *from 50 mV*"). It does **two separate jobs** — keep
them separate or the settings won't make sense. Verbatim help text: [docs/emu-black-help/Sensorsandinputs.md](../docs/emu-black-help/Sensorsandinputs.md) (Primary trigger).

- **Zero-crossing = the *timing*.** The edge is taken where the waveform crosses BIAS midpoint —
  **amplitude-independent**, so timing doesn't drift with signal strength or RPM. (All thresholds are
  referenced to BIAS.)
- **Adaptive peak threshold = the *arming gate*.** A zero-crossing is only accepted as a real tooth if
  the signal first cleared an arming level that **tracks a fraction of the recent peak**: high RPM → big
  signal → high gate (rejects noise); low RPM → small signal → gate tracks **down** to a **~50 mV
  floor**. Below the floor, nothing arms → no detection.
- **`primTrigAdaptive` "strength" Low/High = the gate *level* (fraction of peak), NOT adaptation speed.**
  High = more noise margin but a sagging tooth (eccentric/non-concentric wheel, or the weak tooth after
  the gap) can fall below it → **"unexpected missing tooth."** Low = catches weak/varying teeth, less
  noise margin. ECUMaster: change it "when the signal varies (non-centric trigger wheel)."
- **Pulldown ↔ adaptive threshold interaction (validated):** a pulldown lowers input impedance →
  rejects noise **and** attenuates the signal; the adaptive gate **tracks the smaller peak down and
  self-compensates** the attenuation, while zero-crossing keeps timing intact. The **only** limit is the
  50 mV floor — too strong a pulldown attenuates the weakest (cranking) signal below it → no sync. That
  is exactly ECUMaster's "**1K pulldown, 4K7 if no signal during cranking with 1K**."
- **Pulldown value axis:** lower R (1K) = **more** noise rejection but more loading; higher R (4K7) =
  gentler load / safer cranking but **less** rejection. (So "4K7 = less interference" is true only for
  *loading*, not for *rejection* — 1K rejects more.) The generic "never pull a VR, it biases the
  waveform" rule is for **fixed-threshold** inputs; it doesn't apply to this BIAS-referenced
  zero-crossing input, which is why ECUMaster recommends the pulldown.
- **Input filter is last resort:** rolling-average low-pass, adds latency; "the lower the better." A
  series ~10K resistor is the documented fix for low-RPM *logged* unexpected-missing-tooth errors.

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
([fueling.md](fueling.md), [lambda_tracking_map_smoothing.md](../ai-analysis-skills/lambda_tracking_map_smoothing.md)).

## P4. EGT is the cheap truth sensor

EGT is the primary proxy for MBT at cruise (lower EGT → closer to MBT) and for cylinder-to-cylinder
distribution (rear-vs-front delta on a front-feed manifold). A $20 k-type probe ~1 inch from the head
on each runner is the single highest-value sensor add for a self-tuner ([ignition.md](ignition.md),
[fueling.md → F4](fueling.md), [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md)).

## P5. An NTC's noise gain is worst exactly where you care — diagnose in volts, not degrees

A thermistor divider loses volts-per-degree as it gets hot (resistance collapses toward zero while
the pull-up stays fixed), so a *constant* electrical disturbance produces a small temperature error
cold and a large one at operating temperature. Never judge temp-sensor noise in °C — log the
`* Voltage` channel and work the residual there, then convert through the calibration at the end.

Three diagnostics that cost nothing and localize the fault:

1. **Key on, engine off.** A clean flat voltage here clears the ADC, the reference, and the sensor;
   anything that appears the instant the engine fires is pickup.
2. **The temperature dependence tells you the coupling.** With `V/5 = R_th/(R_pu+R_th)`, a series
   disturbance in the sensor leg (ground offset, or magnetic pickup in the signal/return loop)
   reaches the ADC scaled by `1 − V/5`, so it is **worse hot**. Current injected onto the wire
   (capacitive pickup) or noise on the 5 V pull-up rail scales by `V/5` — **worse cold**. The two
   predictions differ by ~4× across a normal warm-up and are easy to separate in one log.
3. **Cross-check CLT against IAT — and know which answer means what.** ECUMaster's own diagram
   (`Sensorsandinputs.md` → `Images/iatClt.png`) returns *both* sensors to a **common Sensor GND
   pin** (B29; CLT signal B5, IAT B32), so wired to spec they share one conductor. Glitching on the
   same samples therefore means a real disturbance on that shared return or on the 5 V rail.
   Glitching **independently means they are not on it** — each is referenced to something local.
   That is positive evidence for engine/chassis grounding, not evidence against a ground problem:
   engine ground is a distributed conductor carrying coil, starter and alternator return current,
   and two points on a block differ by tens of millivolts during a switching impulse, so two
   locally-bonded sensors glitch independently by construction. After a correct rewire the two
   channels should become *correlated* — that is the confirmation, not a new fault.
4. **Separate coil from injector.** Dwell is usually near-constant, so coil energy per event is
   fixed while injector duty swings with load. Normalize the glitch rate by spark rate: flat per
   spark while injector duty multiplies ⇒ coil current is the source, and the coil grounds and coil
   harness are what to move.

Two multipliers sit downstream of the raw noise and are worth auditing before touching hardware:

- **The calibration table.** EMU's `voltage5VCLTBin` is 8-bit and the wizard's point placement is
  yours to choose; a coarse or duplicated cell near the operating point creates a dead band on one
  side and a slope cliff on the other, turning a small voltage glitch into a large reading. Fit
  Steinhart-Hart to the table's own points — a real NTC fits to well under 1 °C RMS, so any point
  that refuses to fit is a bad cell, not a sensor characteristic.
- **The pull-up.** `cltPullup`/`iatPullup` are **bools** on a fixed internal 2K2 (analog inputs get
  4K7 and a 3-way selector); the only way to change the value is to clear the bool, fit an external
  resistor to +5 V, and regenerate the table with the wizard's `Rx` set to match. Sensitivity peaks
  when `R_pu ≈ R_th` at the temperature you care about, and lowering `R_pu` also lowers node
  impedance *and* the ground-offset transfer ratio — it wins on all three axes, paid for in cold-end
  range. It scales the symptom; it does not remove the source.

Worked example with all of this measured on a real log:
[supra/notes/clt_signal_noise.md](../supra/notes/clt_signal_noise.md).

## P6. Sensor ground is separated from power ground by current path, not by isolation

*Model knowledge, not ECUMaster text (2026-09-25).* ECUMaster publishes no EMU Black schematic;
the pinout only says sensor grounds (29/38/39) are "not connected to the engine" and power grounds
(17/24/27/28) are. The standard ECU design this describes:

- **Not galvanically isolated.** Sensor ground (AGND) is its own copper net joined to power ground
  (PGND) at **one point** — a star point, usually at the ground pins or under the ADC/5 V regulator,
  sometimes through a 0 Ω link, ferrite bead or small resistor. The ADC and the 5 V reference sit on
  AGND, so they share one reference with every sensor return.
- **What the separation buys is that big currents never flow through AGND copper.** Coil primaries,
  injectors, the DBW H-bridge and the ECU's own supply return on PGND. Any trace or wire has
  resistance, so `V = I·R`: 10 A of coil current across 5 mΩ of shared copper is 50 mV, which an
  ADC reading an NTC at operating temperature sees as degrees. Sensor currents are milliamps, so the
  AGND path stays at one potential.
- **Why the harness must keep the rule.** Land a sensor return on the block and its reference now
  runs block → straps → ECU power-ground wire, all carrying engine current, so that `I·R` appears in
  series with the signal. Bond the AGND net to the block anywhere and you create a second path in
  parallel with the internal star point — a ground loop — and a share of engine current flows through
  AGND copper inside the ECU, corrupting every input referenced to it. On pre-"P" hardware that is the
  documented switch-input cross-talk ([supra/notes/ac_request_input_noise.md](../supra/notes/ac_request_input_noise.md)).
  A corroded power ground makes this worse: the ECU's own return current then looks for a way home
  through any sensor bonded to the block.
- **Consequence for testing:** with the ECU plugged in, the sensor-ground net beeps to the block
  through the star point whatever the harness does. Unplug the ECU to test harness routing. On the
  unplugged ECU, ohms from a sensor-ground pin to a power-ground pin shows the internal tie — a direct
  link reads ≈0 Ω, a protective resistor reads a few ohms or more (unmeasured on this unit).

---

## Related documents

- [dbw.md](dbw.md) — TPS/PPS *map* (the characteristic) and DBW motor
- [../supra/notes/clt_signal_noise.md](../supra/notes/clt_signal_noise.md) — CLT pickup, cal-table dead band, pull-up trade study
- [engine_protection.md](engine_protection.md) — dual-TPS plausibility, oil-pressure protection
- [fueling.md](fueling.md) — wideband closed-loop logic, `lambdaDelay`, per-cylinder EGT trim
- [supra/notes/mass_flow_estimator_quirk.md](../supra/notes/mass_flow_estimator_quirk.md) — why idle airflow reads ~10× high
- [supra/notes/throttle_body_thermal_growth.md](../supra/notes/throttle_body_thermal_growth.md) — TB temp vs sensor temp lag
