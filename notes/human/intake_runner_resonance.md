# Intake runner resonance and the VE table

> Digest of [intake_runner_resonance.md](../intake_runner_resonance.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** whether you can back-calculate runner length from a VE-table peak, and how much runner physics should shape a VE table copied between engines.

**The rules:**

- Only fit physics to measured tables. Bradley's veTable is a seeded guess — its peak is not data. The earlier cross-car "ratio test" fit a model to a fabricated table and is retracted.
- Two engines with matching VE tables is the fingerprint of a copied calibration, not corroborating physics.
- The Supra's real autotuned table peaks broadly at ~5300–5600 rpm; a Helmholtz back-calc gives ~8.9 in against the measured 8. Consistent but soft — order-of-magnitude only, since the peak is probably dominated by cam/port/exhaust breathing anyway.
- Going 2JZ → 1JZ, runner physics predicts only about a −10% intake-tuning shift — second order. The dominant differences (stroke, cam, turbo, head) can't be derived from the tune.
- So seed the 1JZ table with the Supra's measured shape, run safe-rich, and build the real table from logs/autotune. Don't pre-bake a resonance reshape bigger than that ~10%.
- To measure for real: compute air-VE from a log at fixed NA load with VVT locked, un-smoothed — the true peak and ripple appear and length inverts cleanly.

**Key numbers:** runner length Supra ≈ 8 in, Bradley ≈ 12 in; Supra VE peak ≈ 5300–5600 rpm; cross-engine tuning shift ≈ −10%.

**When to care:** seeding one car's `veTable` from another's, or whenever you're tempted to read intake physics out of a smoothed VE table.
