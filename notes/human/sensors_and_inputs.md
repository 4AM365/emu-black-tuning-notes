# Sensors and inputs

> Digest of [sensors_and_inputs.md](../sensors_and_inputs.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the sensor-setup discipline the whole tune depends on, plus how the EMU's VR trigger input actually conditions the signal.

**The rules:**

- Lock the sensors before tuning anything. Noisy CLT oscillates the idle target, warmup, ASE, and fan logic all at once; that's a wiring/hardware problem — chasing it in the maps never converges.
- The mass-flow estimator lies at idle: reverted flow through the throttle reads as airflow and can overstate real combustion air ~10×. Never validate idle VE against it.
- `lambdaDelay` realigns logged lambda to the cell that produced it, so measured-vs-target attribution is trustworthy even under acceleration.
- EGT is the cheap truth sensor — a k-type probe ~1 inch from the head on each runner is the single highest-value add. Lower EGT at cruise means closer to MBT; front-vs-rear delta reads maldistribution.
- The VR trigger does two separate jobs: the **zero-crossing** sets tooth timing (amplitude-independent, never drifts), and the **adaptive peak threshold** is only an arming gate that tracks the recent peak down to a ~50 mV floor.
- `primTrigAdaptive` Low/High is the gate *level*, not adaptation speed. High buys noise margin but a sagging tooth (non-concentric wheel) can drop below it → "unexpected missing tooth." Low catches weak teeth.
- A pulldown resistor is fine here — the adaptive gate self-compensates the attenuation and zero-crossing keeps timing intact. 1K rejects the most noise; go 4K7 only if cranking loses signal. The "never pull a VR" rule is for fixed-threshold inputs, not this one.
- The input filter is a last resort (rolling average, adds latency — "the lower the better"). A series ~10K resistor is the documented fix for low-RPM unexpected-missing-tooth errors.
- **Diagnose temp-sensor noise in volts, not degrees.** An NTC loses volts-per-degree as it heats, so the same electrical disturbance is harmless cold and brutal at operating temperature. Key-on/engine-off is the free zero reference; anything appearing when the engine fires is pickup.
- **The temperature dependence names the coupling.** A series disturbance in the sensor leg (ground offset, magnetic pickup in the signal/return loop) scales by `1 − V/5` — worse hot. Capacitive pickup on the wire, or 5 V-rail noise, scales by `V/5` — worse cold. ~4× apart across a warm-up, so one log separates them.
- **CLT and IAT are wired to a common Sensor GND (B29) per ECUMaster's diagram** — signals B5 and B32. Same-sample glitches mean a real disturbance on that shared return or the 5 V rail. **Independent glitches mean they are not on it**, i.e. each is bonded locally to the engine — which is a distributed conductor, not a node, so locally-grounded sensors glitch independently by construction. Correlation returning after a rewire is the confirmation.
- **Separate coil from injector.** Dwell is near-constant, injector duty swings with load. Normalize glitch rate by spark rate: flat per spark while duty multiplies ⇒ coil current, so move the coil grounds and harness.
- **Audit the two downstream multipliers before touching hardware:** the calibration table (8-bit voltage bins — a coarse or duplicated cell near the operating point makes a dead band on one side and a slope cliff on the other; a real NTC fits Steinhart-Hart to well under 1 °C RMS, so a point that won't fit is a bad cell) and the pull-up (`cltPullup`/`iatPullup` are bools on a fixed internal 2K2, not selectors — an external resistor plus a regenerated table is the only way to change it).
- **Sensor ground isn't isolated, it's kept out of the high-current path** (model knowledge; no ECUMaster schematic). It's a separate net joined to power ground at one star point, so coil/injector current never flows through the copper the ADC measures against. Landing a sensor on the block puts that current's `I·R` in the signal; bonding sensor ground to the block makes a ground loop. With the ECU plugged in it always beeps to the block — unplug to test.
- Sensitivity peaks when the pull-up matches the thermistor at the temperature you care about; lowering it also lowers node impedance and the ground-offset transfer ratio, paid for in cold-end range. It scales the symptom, never the source.

**Key numbers:** adaptive-gate floor ~50 mV; pulldowns 1K (default) / 4K7 (cranking fallback); idle airflow channel overstates ~10×; fix anything past 1–2 °C CLT jitter or ±5° VVT oscillation at steady idle. Internal pull-ups: 2K2 on CLT/IAT, 4K7 on analog inputs 1–6.

**When to care:** before tuning anything new, when a trigger/sync error appears in the log, and whenever idle wanders with no calibration explanation.
