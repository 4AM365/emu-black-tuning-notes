# Return-to-Idle Bogging

Bog/stumble (and sometimes stall) as the engine drops back toward idle after lift-off — coming off throttle at speed, neutral coast-down, or a clutch-in roll to a stop. This page is the consolidated entry point; the full diagnostic trees live in [idle_stall.md](idle_stall.md) sections [A] and [H], which this note links into rather than duplicates.

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`airflow_actuator.md`](../supra/notes/airflow_actuator.md) and [`idle_session_05242026.md`](../supra/notes/idle_session_05242026.md). This note is intentionally car-agnostic.

---

## First: which return-to-idle failure is it?

| What you feel / see | Pattern | Where to fix |
|---|---|---|
| Lift-off from high RPM/boost, rich stumble → dies cleanly | **Overrun-to-idle stall** | [idle_stall.md §A](idle_stall.md) |
| Neutral/clutch-in coast while still rolling; RPM craters below target then limit-cycles (recoverable, doesn't always die) | **Rolling return-to-idle wobble** ("drive wobble") | [idle_stall.md §H](idle_stall.md) |
| Light throttle blip from idle stumbles | DBW floor / blend gap | [idle_stall.md §D](idle_stall.md), [throttle_feel.md](throttle_feel.md) |

Always start from a log that captures the event (see [idle_stall.md Step 0](idle_stall.md)). Look at the ~4 s **before** the bog, not just the moment it happens.

---

## Rule it out FIRST: a cam-sync (phase) loss masquerading as an airflow bog

Before reaching for any airflow/VE lever below, confirm the engine **held cam-to-crank sync through the dip**. A momentary loss of sync produces a bog that is *visually identical* to an airflow stall — RPM craters to a low floor then over-recovers — but no calibration change can fix it.

**`Trigger error count` = 0 does NOT mean sync was held**, and the loss is usually **not** the crank teeth dropping out. `Trigger sync status` is the **cam↔crank sync** state (2 = full sync, 0 = lost), not "are the crank teeth present." On a VVT engine the most likely cause is an **unstable VVT sync cam**: the intake cam (which is also the sync cam) is held off its lock pin at idle and hunts, so its sync edge wanders — and on the decel into idle that wandering edge misses its expected primary tooth and the ECU dumps full sync.

**Do not mis-read the recovery as the cause.** After a full sync loss the ECU drops into cranking-mode re-acquisition: it batch-fires, **locks to the first sync it sees** (a provisional tooth — e.g. 21), then once RPM passes `crankingThreshold` it **resolves the true tooth and pops over** (e.g. to 57). So a `CAM sync trigger tooth` excursion like 57→21→57 (and the `VVT CAM angle` reading garbage such as the `vvtCam1TriggerOffset` constant, 417°, mid-recovery) is the **re-acquire signature, not a causal phase flip**. The cause is whatever dropped full sync one sample earlier.

Signature of the loss + recovery (downstream cascade is identical regardless of trigger cause):

- `Trigger sync status` 2 → **0**; `Engine runtime` resets large→**0**; `ECU State` 3/4 → **1**; `Executed sparks count`→0, `Injectors PW`→0 (spark+fuel cut while fully unsynced, ~80 ms).
- Then the cranking-style re-acquire (~160 ms): provisional-tooth lock → promote to true tooth past the cranking threshold. RPM keeps sagging through this.
- A **cluster of running-gated flags drop to 0 on the same sample** and recover together: `Idle state` 2→0, `Idle control active` 1→0, `Idle air %`→0, `Coolant fan`, `AC Clutch`, `Lambda is valid`. That synchronized multi-flag drop is the tell — idle logic alone never does it. Idle control gating off is what yanks the air and drives the DBW closed; recovery overshoots.

**Why it shows up on the decel into idle, every drive — the VVT sync-cam mechanism:** the cam-sync tooth-deviation tolerance **must be 0 on a multitooth primary**, so there is *zero* slack for the sync cam edge to move off its expected tooth. If the VVT intake cam (the sync cam) is commanded to a small non-zero angle at idle, it sits **off its lock pin** on marginal low-RPM/low-oil-pressure control and hunts several degrees (look for `VVT CAM angle` with a wide min–max band and the solenoid DC thrashing at a flat target). On the fast coast-down — tooth periods stretching, cam edge wandering, oil pressure sagging — the cam pulse lands off its tooth → full sync loss → the re-acquire above → idle-control-off cascade → bog.

**Separate the cam side from the crank side before picking a lever.** First confirm the cam: is `CAM sync trigger tooth` stable in normal running (not counting the re-acquire excursion) and is `vvtCam1TriggerOffset` correct? If yes, the cam phase is **not** the cause — and the loss fingerprint (`RPM`→0, `Engine runtime` reset) confirms it's the **primary/crank decode** that dropped, not the cam. Two independent, non-conflicting levers:

- **Crank side (the loss itself) — front-end first, filter last:** ECUMaster *strongly recommends a 1K pulldown* on a VR primary trigger (the build was running None). Lowering the input impedance dumps induced interference at the analog front end with **no added latency** — the right first move for a crank-side noise loss. Verify cranking still syncs after (1K loads the sensor most at the lowest-amplitude cranking RPM; step to **4K7** if cranking signal drops). Pair with shielded cable, shield grounded **one end only**. Only if noise persists, probe `primTrigInputFilter` none→low→medium — it adds delay and only rejects *added* edges, so it's diagnostic (kills the loss ⇒ interference; no effect ⇒ a true *dropped* edge = VR amplitude/air-gap, which neither pulldown nor filter recovers) and risks high-RPM misfire (verify on a redline pull: `Trigger error count` stays 0, `Trigger sync status` stays 2). A ~10K **series** resistor is the documented remedy for low-RPM unexpected-missing-tooth VR errors specifically.
- **Cam side (idle stability, worth doing regardless):** if the VVT sync cam is commanded off 0° at idle it sits off its lock pin and hunts (wide `VVT CAM angle` min–max, solenoid DC thrashing at a flat target). Command **0° at idle** so it parks on the lock pin — steadier idle (0° overlap) and a dead-stable sync edge. Removes a perturbation even if the tooth wasn't visibly fluctuating.

**Never lower `disableCamSyncOver` on a VVT engine.** Disabling cam sync stops the **cam-angle calculation** (cam sync runs every revolution to compute it), so it must stay enabled — it is not a lever here. The adaptive threshold (a crank-amplitude knob) is also not it. The airflow/VE levers below smooth the *recovery* but will not prevent a sync-initiated bog.

> Confirmed instance: `cold idle dip again 3 all channels.csv`, log-rel t≈26.2 s — full sync loss (`Trigger sync status` 2→0, `Engine runtime` 402→0, sparks+fuel zeroed), then the cranking re-acquire signature `CAM sync trigger tooth` 57→21→57 and `VVT CAM1 angle`→417/362 garbage (recovery artifacts, **not** the cause); idle air 42%→0; floor 720 RPM; over-recovery to 1513. Same 720/1513 fingerprint as the lower-channel `cold idle dip again 2.csv` export (same physical event), recurring most drives at this decel-to-idle region. **Root cause traced to the VVT sync cam:** commanded 2.5° at idle, held off its lock pin, hunting −0.5°→+4.5° (std 1.47°) with solenoid DC thrashing 2–48% at a flat target — the wandering sync edge misses its tooth on the oil-pressure-sagging decel. Owner's fix: command 0° cam at idle so it parks on the lock pin.

---

## The two root causes, in one place

Return-to-idle bog is almost always one (or both) of:

### 1. Airflow falls out from under the idle controller

- **Overrun (§A):** `idleArmedAirFlow` resolves too low at the decel RPM bins, so the DBW plate fights its return spring with no useful air column. Fuel cut exits into near-zero air → rich spike → bog. Fix: populate `idleArmedAirFlow` with enough air across the higher decel RPM bins (PPS=0) to hold the plate off its spring, tapering smoothly into your steady idle airflow at the idle-approach bins, no step at the bottom.
- **Rolling wobble (§H):** `idleCoolantFanCorr` (a positive idle-air bump while the fan loads the engine) is VSS-gated **off above a speed threshold**, so a return from speed runs the bare base airflow instead of the higher fan-on value, and the airflow PID is clamped too low to hold the depth. Fix without adding idle variation: more PID authority (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`) and a faster `idlePIDUpdateInterval`. Leave the fan correction — it's correct load-comp.

### 2. Low-RPM VE over-fuels into the dip

As RPM craters and MAP rises toward the low-RPM pumping-loss region, speed-density over-fuels. Rich misfire → erratic torque → the dip deepens and oscillates.

- The **lowest-RPM VE row** (the dip row, the bottom of `rpmBins`) governs fueling *exactly when RPM craters into a dip*. If it's a verbatim copy of the row above it it's too rich there — lean it toward the idle lambda target. Richness should **increase as RPM drops**, so the lean deepens from the idle row down toward the dip row.
- **Set VE from measured lambda, not from the trims.** The lambda trim is deliberately slow/low-authority (a few percent) so it won't reveal the true VE requirement and can't catch a fast dip. Use `VE_new = VE_old × (Lambda 1 / Lambda target)`, apply most (not all) of the computed lean first, then re-verify. Lean **both** `veTable` (pump) and `veTable2` (ethanol) by the same ratio.

> **⚠ Re-measure at the fuel you actually run.** If a global pump/ethanol VE correction has been applied since the dip was logged, the residual richness is fuel-dependent (the pump and ethanol corrections can nearly cancel at one ethanol blend and not at another), so a lean computed at one fuel can over-lean at another and risk a lean stumble. See [idle_stall.md §H](idle_stall.md) and the build's working doc for the full blend math.

---

## What does NOT work (return-to-idle specific dead ends)

- **Raising the Active airflow table's sub-idle rows.** `idleActiveAirflow` is indexed by idle *target*, which floors at the idle setpoint, so rows below it are never read. The VE table **is** indexed by actual rpm × MAP, so its dip-RPM row *is* the live lever when RPM craters.
- **VSS-scheduled idle-target bump** (`idleIncreaseTargetAboveVSS`): would mechanically work but adds a target step — rejected to keep low-speed heat-soak idle clean.
- **Big overrun exit enrichment.** A large pulse fired into a barely-cracked throttle makes the stumble worse. Prefer raising the overrun-exit RPM threshold or a stepped exit.
- **Decel fuel correction firing during recovery.** The decelerate-fuel-correction table can trim fuel the wrong way at low RPM during the return — raise its RPM floor so it doesn't activate in idle recovery. See [throttle_feel.md](throttle_feel.md).

---

## Calibration discipline

Size feed-forward airflow corrections **conservatively** — apply ~half what the engine needs and let the PID ease in the rest. Under-correcting costs a brief high-idle blip the PID resolves; over-correcting can hit the actuator floor and stall. Full rationale and the sizing procedure: [idle_stall.md "Design principle: feed-forward should be conservative"](idle_stall.md).

Before touching calibration, run the [Universal Pre-Diagnosis Checklist](idle_stall.md) (wideband valid, brake switch 0, trigger/VVT/protection codes clean, battery 13.8–14.4 V, idle state = 2).

## Related notes

- [idle_stall.md](idle_stall.md) — full diagnostic trees (this page's source for §A and §H)
- [throttle_feel.md](throttle_feel.md) — DBW blend point, decel fuel correction, tip-in feel
- [engine_start.md](engine_start.md) — cold-start and post-start idle
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — PID integrator windup on slow hot droop
