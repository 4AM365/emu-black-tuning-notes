# Keep the Aristo ECU for the cluster? — the short version

> **⛔ NOT THE SUPRA.** GS300 / Aristo / CD009. Never carry values, pins or conclusions between
> this car and the Supra notes in either direction; never load `supra-specs` for it.

**What this covers.** Whether to leave the OEM Aristo ECU in the car as a gauge driver while the
EMU takes drive-by-wire, and whether to share the throttle/pedal sensors between both.
Canonical note: [`../position_keep_aristo_ecu_for_cluster.md`](../position_keep_aristo_ecu_for_cluster.md) — that one wins.

**The verdict.** Keeping the ECU: promising, test it. Sharing the sensors: **no.**

**The rules.**
- Keeping it is clever for one specific reason — the Aristo ECU already knows the **BEAN message
  dictionary** that nobody has reverse-engineered. Toyota's own hardware as the gateway.
- Sharing the position sensors buys nothing. The ECU **faults regardless**, because you took its
  motor away. ETCS-i is closed-loop: open motor driver, plus a blade moving to positions it never
  commanded. Better sensor data doesn't fix either.
- Sharing costs real things: two 5 V rails can't feed one sensor, so you end up sharing a **ground
  reference** between two ECUs, and that offset lands on safety-critical throttle feedback. Toyota
  input bias networks also shift what the EMU reads.
- **If you keep it, isolate it.** Power, ground, `THW`, `RL`, `MOPS`, `MOL`, `MPX1`/`MPX2`, and
  nothing else. Never anything in the DBW loop.
- Give the EMU its **own main relay**. Don't let a faulted ECU hold power for a running engine.

**Key numbers.**
- The prize is **bigger than first thought**: the temperature gauge **and** the charge, oil
  pressure and oil level lamps — **none of which can be re-wired**, because the cluster has its own
  CPU and paints them from bus data. Plus HVAC auto mode. Gear position is already dead (CD009).
- The costs: the immobiliser stays (it's inside the ECU on the 89666-30180 and gates `M-REL`),
  permanent MIL on `W` F60-6, and four outputs that must be severed.
- Untested assumption: that a faulted ECU still transmits valid gauge frames. Not documented
  anywhere we hold — RM718U is missing its DIAGNOSTICS section.

**When to care.** Before any repin. The disconnection test is ~30 minutes and decides the whole
cluster strategy: pull the throttle motor, then sensors, then pedal, then injectors and coils —
key on each time, watch the gauges. Do the BEAN capture in the same session; it's unrecoverable
once the ECU is out.
