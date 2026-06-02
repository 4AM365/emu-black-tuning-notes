# Return-to-Idle Bogging

Bog/stumble (and sometimes stall) as the engine drops back toward idle after lift-off — coming off throttle at speed, neutral coast-down, or a clutch-in roll to a stop. This page is the consolidated entry point; the full diagnostic trees live in [idle_stall.md](idle_stall.md) sections [A] and [H], which this note links into rather than duplicates.

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

Return-to-idle bog on this build is almost always one (or both) of:

### 1. Airflow falls out from under the idle controller

- **Overrun (§A):** armed-state airflow resolves too low (0–4%) at decel RPM bins, so the DBW plate fights its return spring with no useful air column. Fuel cut exits into near-zero air → rich spike → bog. Fix: populate the armed-state airflow table with **60–80% at 1800–2200 RPM (PPS=0)**, tapering to your idle airflow (~38%) at 1100–1300 RPM, no step at the bottom.
- **Rolling wobble (§H):** the +13% `idleCoolantFanCorr` is VSS-gated **off above ~56 km/h**, so a return from speed runs the bare ~26.5% base airflow instead of ~39%, and the airflow PID (clamped +12) can't hold the depth. Fix without adding idle variation: more PID authority (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`) and a faster `idlePIDUpdateInterval` (200 ms → ~50 ms). Leave the fan +13% — it's correct load-comp.

### 2. Low-RPM VE over-fuels into the dip

As RPM craters and MAP rises toward 60+ kPa (low-rpm pumping loss), speed-density over-fuels. Rich misfire → erratic torque → the dip deepens and oscillates.

- The **500-rpm VE row** governs fueling *exactly when RPM craters into a dip*. If it's a verbatim copy of the 842 row it's ~17% too rich there — lean it toward λ0.93. Richness should **increase as RPM drops**, so the lean deepens 1184 → 842 → 500.
- **Set VE from measured lambda, not from the trims.** The lambda trim is deliberately slow/low-authority (~±2–3%) so it won't reveal the true VE requirement and can't catch a fast dip. Use `VE_new = VE_old × (Lambda 1 / Lambda target)`, apply ~80% of the computed lean first, then re-verify. Lean **both** `veTable` (pump) and `veTable2` (ethanol) by the same ratio.

> **⚠ Re-measure at the fuel you actually run.** The −17–19% rich figure is from pre-correction E25 logs. After the v2 global −18% pump / +10% ethanol correction, the residual is fuel-dependent (~−18% rich still at E60, only ~−9% at E25). A lean computed from an E25 log over-leans by ~9% at E25 and risks a lean stumble. See [idle_stall.md §H](idle_stall.md) for the full blend math.

---

## What does NOT work (return-to-idle specific dead ends)

- **Raising the Active airflow table's 1000/1100 rows.** `idleActiveAirflow` is indexed by idle *target*, which floors at 1200, so those rows are never read. The VE table **is** indexed by actual rpm × MAP, so its 500-rpm row *is* the live lever when RPM craters.
- **VSS-scheduled idle-target bump** (`idleIncreaseTargetAboveVSS`): would mechanically work but adds a target step — rejected to keep low-speed heat-soak idle clean.
- **Big overrun exit enrichment.** A +20–25% pulse fired into a barely-cracked throttle makes the stumble worse. Prefer raising the exit RPM threshold (~2500) or a stepped exit.
- **Decel fuel correction firing during recovery.** The decelerate-fuel-correction table can trim fuel the wrong way at low RPM during the return — raise its RPM floor so it doesn't activate in idle recovery. See [throttle_feel.md](throttle_feel.md).

---

## Calibration discipline

Size feed-forward airflow corrections **conservatively** — apply ~half what the engine needs and let the PID ease in the rest. Under-correcting costs a brief high-idle blip the PID resolves; over-correcting can hit the actuator floor and stall. Full rationale and the sizing procedure: [idle_stall.md "Design principle: feed-forward should be conservative"](idle_stall.md).

Before touching calibration, run the [Universal Pre-Diagnosis Checklist](idle_stall.md) (wideband valid, brake switch 0, trigger/VVT/protection codes clean, battery 13.8–14.4 V, idle state = 2).

## Related notes

- [idle_stall.md](idle_stall.md) — full diagnostic trees (this page's source for §A and §H)
- [throttle_feel.md](throttle_feel.md) — DBW blend point, decel fuel correction, tip-in feel
- [cranking_and_idle.md](cranking_and_idle.md) — cold-start and post-start idle
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — PID integrator windup on slow hot droop
