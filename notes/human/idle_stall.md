# Idle stall troubleshooting

> Digest of [idle_stall.md](../idle_stall.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the eight idle-stall patterns, how to sort a log into one, and the single fix each pattern needs.

**The rules:**

- Log the stall first and read the 4 seconds *before* it dies, not the moment of death. No log, no calibration change.
- Overrun-to-idle stall (the most common): `idleArmedAirFlow` resolves too low at the decel RPM bins, so the plate fights its return spring and fuel-cut exit lands in dead air. The rich lambda spike is the symptom, not the cause. Fill the table so it holds the plate open, tapering smoothly into steady idle airflow — no step at the bottom.
- Post-start stall: the throttle slams from cranking position to idle position at catch. Hold the post-start idle target elevated 5–10 s; ASE is not the cause, don't cut it. Run ASE on engine revolutions (not time), and confirm the wideband validates before ASE reaches zero.
- Warm stall check order: wideband valid → ASE masking lean idle VE → `Idle state` (0 throughout = brake switch holding the PID off) → DBW floor. Set the actuator floor just below hot-idle TPS; the same fix cures tip-in stalls from the blend gap.
- Idle hunts then dies: sensor/hardware, not calibration. VVT angle wobbling ±5° or CLT jittering 1–2 °C, or a lean rear cylinder on a front-feed manifold (trim it, watch rear EGT).
- Windup: keep the integrator limit *below* the proportional limit and size it for ~5 s to steady state. P recovers the engine; a wound-up I lags behind and loses.
- Rolling wobble at speed is two faults: rich bottom VE row (lean it toward the idle lambda target — set VE from measured lambda, never from the slow low-authority trims) plus fan-corr airflow gated off above a speed threshold (fix with more PID authority, not more scheduled air). Sub-idle `idleActiveAirflow` rows are dead — the table indexes by idle *target*, which floors at the setpoint.
- Size every feed-forward air correction at about *half* the measured need and let the PID close the rest. Under-correction is a brief high-idle blip; over-correction hits the actuator floor and stalls.

**Key numbers:** `Idle state` 2 = PID active, 0 = disabled. Battery 13.8–14.4 V running. Integrator ~5 s to steady state.

**When to care:** any time the engine dies at idle or coming to a stop — run the pre-diagnosis checklist (wideband, brake switch, trigger, VVT, battery) before touching a table.
