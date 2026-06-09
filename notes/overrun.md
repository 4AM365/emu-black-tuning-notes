# Overrun — EMU Black settings and the principles behind them

> **Software page:** *Overrun*. Full symbol catalog: [tune_feature_tree.md → Overrun](tune_feature_tree.md). The return-to-idle *recovery* (armed airflow, idle PID re-entry) is on [idle.md](idle.md); the symptom-first trees are [return_to_idle_bog.md](return_to_idle_bog.md) and [idle_stall.md](idle_stall.md).

Organized like [idle.md](idle.md): settings first, then principles.

> **Car-specific values live in the build working docs**, not here — esp.
> [`supra/notes/airflow_actuator.md`](../supra/notes/airflow_actuator.md).

---

# Part 1 — Settings

### Overrun fuel cut — `overrunFuel` / `overrunFuel2`, `overrunRPMActive` / `overrunRPMInactive`, `overrunPPSOn` / `overrunPPSOff`

- **What it is.** Deceleration fuel cut (DFCO): fuel is cut on a closed-pedal, above-RPM overrun and
  restored at a lower RPM. Enter/exit are gated on PPS (`overrunPPSOn/Off`) and RPM
  (`overrunRPMActive/Inactive`), with hysteresis between enter and exit.
- **How to set it.** For cammed / high-compression builds, allow DE (decel enleanment / cut) only
  **above a relatively high RPM**; the larger the overlap, the bigger the gap between idle and the
  DE-exit threshold. Restore fuel at a lower RPM with a small RPM hysteresis. Alternative to a hard
  threshold raise: a **stepped exit** — partial cut at an intermediate band, full fuel at the lower
  bound (gentler for sensitive setups).
- **Failure modes.** Exit RPM too low → fuel returns into a near-zero air column at the bottom of the
  decel → rich spike → the overrun-to-idle stall ([idle_stall.md §A](idle_stall.md)). The *cause* of
  that stall is usually airflow (armed table), not the cut — see K-principles below.
- **Live values:** build doc.

### Overrun exit enrichment — `overrunExitEnrich`, `overrunExitDecayRate`

- **What it is.** A fuel pulse as the cut exits, to re-wet the ports.
- **How to set it.** Keep it **small**. A large pulse fired into a barely-cracked throttle causes a
  rich stumble that defeats idle recovery. Decay it out (`overrunExitDecayRate`).
- **Failure mode.** Over-sized exit enrichment → rich stumble on every return to idle.
- **Live values:** build doc.

### Overrun ignition — `overrunIgnition` / `overrunIgnition2`, `overrunSparkCut`, `overrunIgnEnterRate` / `overrunIgnExitRate`

- **What it is.** Timing retard (and optional spark cut) during overrun, with separate enter/exit
  ramp rates.
- **How to set it.** Use **asymmetric** rates — **fast enter** (cut/retard fast), **slow exit**
  (restore advance slowly) so the advance step doesn't stack with the re-fuel event and force the
  airflow PID to chase it. Retard also softens the off-throttle "parachute."
- **Live values:** build doc.

### Overrun throttle — `overrunDBW` / `overrunDBW2`, `overrunDBWOverride`

- **What it is.** The DBW target held during overrun (distinct from the armed-state idle airflow).
- **How to set it.** Hold enough plate to keep an air column under the engine through the transition;
  for boosted builds this also keeps the turbine fed (see [boost.md → B3](boost.md), spool retention,
  which holds ~10–15% TPS with fuel cut). Don't let it drive to the spring stop.
- **Live values:** build doc.

### Lean-cruise / lift gating — `lg*`

- **What it is.** A conditional lean/fuel-correction function (`lgEnable`, `lgMinRPM/MaxRPM`,
  `lgMinMAP`, `lgMinTPS/MaxTPS`, `lgLeantime`, `lgFuelCorrection`) gated by RPM/MAP/TPS/CLT.
- **How to set it.** Gate it well clear of idle and the return-to-idle band so it can't trim fuel the
  wrong way during recovery. See the decel-fuel-correction caution below.
- **Live values:** build doc.

---

# Part 2 — Principles

## O1. The rich spike at overrun exit is a symptom — fix airflow first

Stalls/bogs on the return to idle look like a fuelling problem (lambda spikes rich just before the
engine dies) but the **cause is usually airflow**: `idleArmedAirFlow` resolves too low at the decel
RPM bins, the DBW plate fights its return spring with no useful air column, and the cut exits into
near-zero air → rich spike → deeper RPM drop → feedback loop. Fix the **armed airflow table**
([idle.md → Armed state airflow](idle.md)) and the rich spike disappears with the stall. Raising the
overrun-exit RPM or stepping the exit are *secondary* helpers, not the primary lever. Full tree:
[idle_stall.md §A](idle_stall.md), [return_to_idle_bog.md](return_to_idle_bog.md).

## O2. Asymmetric transitions — cut fast, restore slow

Both the fuel restore and the ignition re-advance, if fast, stack a torque step onto whatever the
pedal is doing and force the airflow PID to chase it. Fast-enter / slow-exit ramps keep the recovery
smooth. Small RPM hysteresis between enter and exit thresholds prevents chatter at the boundary.

## O3. Lift-off rod protection lives here

Overrun fuel cut is also the **rod-protection** event: at high-RPM lift-off the drivetrain drives the
engine and the power-stroke rods load in tension. The direct mitigations are **overrun fuel-cut
strategy** (minimum-RPM threshold, hysteresis, partial reduction) and **ignition cut instead of fuel
cut** — a slower throttle closure only helps indirectly ([dbw.md → T2](dbw.md)).

## O4. Decel fuel correction can fire the wrong way

The decelerate-fuel-correction table (and `lg*`) can fire **negative accel enrichment during a
return-to-idle recovery**, trimming fuel the wrong way at low RPM and worsening a bog. Raise its RPM
floor so it doesn't activate in idle recovery ([fueling.md → Decel fuel correction](fueling.md)).

---

## Related documents

- [idle.md](idle.md) — armed-state airflow (the real overrun-stall lever) + idle re-entry
- [return_to_idle_bog.md](return_to_idle_bog.md) / [idle_stall.md](idle_stall.md) — symptom-first decision trees
- [dbw.md](dbw.md) — lift-off rod protection, throttle closure rate
- [boost.md](boost.md) — spool retention (fuel cut + plate held open turns the engine into an air pump)
- [fueling.md](fueling.md) — decel fuel correction RPM floor
