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

**Key numbers:** adaptive-gate floor ~50 mV; pulldowns 1K (default) / 4K7 (cranking fallback); idle airflow channel overstates ~10×; fix anything past 1–2 °C CLT jitter or ±5° VVT oscillation at steady idle.

**When to care:** before tuning anything new, when a trigger/sync error appears in the log, and whenever idle wanders with no calibration explanation.
