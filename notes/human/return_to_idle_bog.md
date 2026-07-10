# Return-to-idle bogging

> Digest of [return_to_idle_bog.md](../return_to_idle_bog.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** bog, stumble, or stall as RPM falls back to idle — how to identify which of four root causes you have before touching a table.

**The rules:**

- Rule out cam-sync loss first. `Trigger error count` = 0 proves nothing — read `Trigger sync status` (2 = synced, 0 = lost). The tell is a cluster of running-gated flags (idle state, idle air, lambda valid, fan) all dropping to 0 on the same sample. No calibration change fixes a sync-initiated bog.
- Don't mistake the recovery for the cause: a sync-tooth excursion (57→21→57) and garbage VVT angles mid-dip are the re-acquire signature, not a phase flip. The cause is whatever dropped sync one sample earlier.
- Usual trigger culprit: the VVT sync cam commanded off 0° at idle hunts off its lock pin and its sync edge wanders. Command 0° at idle so it parks. Crank-side noise: fit the 1K pulldown on a VR primary before touching input filters. Never lower `disableCamSyncOver` on a VVT engine.
- Airflow cause A: `idleArmedAirFlow` too low at the decel bins — the plate fights its spring and fuel-cut exit lands in dead air. Fill and taper it, no step at the bottom.
- Airflow cause B: the MAP-activation gate (`idleMinMapToActivate`) locks idle control out during engine braking, so the plate just follows the released pedal until near-stall. Lower the gate to just above worst-case engine-braking MAP and well below idle MAP — read both bands off a log.
- Fuel cause: the bottom VE row over-fuels the dip. Lean it from measured lambda (`VE_new = VE_old × Lambda/target`), apply most-not-all, lean `veTable` and `veTable2` by the same ratio — and re-measure on the fuel you actually run before trusting an old dip log.
- Dead ends: sub-idle `idleActiveAirflow` rows (never read), a VSS idle-target bump, big overrun-exit enrichment, and decel fuel correction firing during recovery (raise its RPM floor instead).

**Key numbers:** reference-build MAP gate fix 25 → 18 kPa moved the catch from 582 to ~1060 rpm. A sync loss costs ~80 ms of spark+fuel cut plus ~160 ms re-acquire.

**When to care:** any stumble coming off throttle, neutral coast-down, or clutch-in roll to a stop — especially one that repeats at the same spot every drive.
