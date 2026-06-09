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
