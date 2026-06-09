# Engine protection — EMU Black settings and the principles behind them

> **Software page:** *Engine protection*. Full symbol catalog: [tune_feature_tree.md → Engine protection](tune_feature_tree.md). Full stuck-throttle config + history: [stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md).

Organized like [idle.md](idle.md): settings first, then principles.

> **Car-specific values live in the build working docs.** This build **brake-boosts** — the
> stuck-throttle box is deliberately permissive; never tighten it (see P1).

---

# Part 1 — Settings

### Stuck-throttle protection — `stEnable`, `stTPSLevel`, `stBrakeTimeout`, `stMinRPM`

- **What it is.** A layered defense against an uncommanded-open throttle: (1) **dual-TPS
  plausibility** (`Check signal input` — catches a lying sensor; brake-independent), (2) **closed-loop
  DBW position-error** monitor (actual TPS doesn't follow target → limp; brake-independent), (3) the
  **brake-based "Stuck throttle" box** (`st*` — brake + TPS, blind to PPS), (4) a **fuel/RPM limp cap**.
- **How to set it.** Make layers **1 and 2 primary** (PPS/sensor-referenced; never interfere with
  brake-boost). Keep the brake-based box **permissive** — raise **`stTPSLevel`** first (keeps a fast
  cut for a high/WOT-stuck blade while ignoring partial-throttle-while-braking), then **`stBrakeTimeout`**;
  set `stTPSLevel` just above a logged real brake-boost peak. Pair the throttle limp with a **fuel-cut
  RPM cap** because the DBW spring-home angle sits *above* the zero-airflow point and can still flow
  enough air to run RPM up.
- **Failure modes.** Tight brake-based box cuts brake-boosts (post-stall code 16384 = the plausibility
  fault, a different mechanism). `Check signal input = None` leaves dual-TPS plausibility (and its
  error tolerance) inert.
- **Live values:** interim `stTPSLevel` 70 / `stBrakeTimeout` 1500 ms; Bosch TB swap makes dual-TPS
  live. Full config: [stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md).

### Rev limiter — `revLimit1*` / `revLimit2*`

- **What it is.** Two-stage limiter; each stage has a control range, cut type (fuel/ignition/both),
  cut percent, and ignition retard.
- **How to set it.** Prefer **ignition-based** (or partial) cut for a softer limiter that doesn't dump
  raw fuel; set the control range so it tapers in rather than hard-walls. Stage 1 as the working
  limiter, stage 2 as a hard backstop.
- **Live values:** build doc (`rpmLimit`, per-stage cut type/percent/retard).

### Protection limits & fault reporting — `fuelCutAbovePressure`, protection thresholds, `failReport*`, `egtAlarm*`, `checkEngineLight*`

- **What it is.** Hard limits (e.g. fuel cut above a MAP/pressure ceiling, over-temp/over-boost
  protection) plus the fault-reporting channels and CEL/alarm outputs.
- **How to set it.** Set ceilings with margin above the intended operating envelope; route faults to
  the CEL and (for EGT) an `egtAlarm` output. Confirm a fault actually limps/reports in a log before
  relying on it.
- **Live values:** build doc.

---

# Part 2 — Principles

## P1. PPS is the correct stuck-throttle discriminator (and brake-boost is safe by it)

The dangerous case (throttle open, **pedal released**) and the intentional brake-boost case (throttle
open, **pedal commanding it**) separate cleanly by **PPS**. Any protection that watches **PPS-vs-TPS**
is inherently brake-boost-safe — it can't trip while the driver is commanding throttle. EMU's
brake-based box looks at **brake + TPS only, blind to PPS**, so it cannot tell a brake-boost from a
stuck throttle and will cut a brake-boost at tight settings. Lean on the sensor-referenced layers as
primary defense and keep the brake-based box permissive. **This build brake-boosts — never tighten the
brake-based box or add a brake-gated cut.** Full rationale: [dbw.md → T3](dbw.md),
[stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md).

## P2. Limp must bound airflow, not just throttle angle

The DBW mechanical spring-home angle sits **above** the zero-airflow TPS point, so a fault that drops
to spring-home can still flow meaningful air. A throttle-angle limp alone can let spring-home airflow
run RPM up — pair it with a **fuel-cut RPM cap** so the failure is bounded regardless of plate position.

## P3. Soft limiters beat hard walls

A fuel-only hard cut dumps raw fuel and bangs the limiter; an ignition (or partial) cut with a taper
control range protects with less drivetrain shock and no raw-fuel wash. Same logic as the overrun
cut ([overrun.md → O2](overrun.md)) — protect firmly, transition gently.

---

## Related documents

- [stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md) — full layered defense + this build's config/history
- [dbw.md](dbw.md) — throttle control the protection guards
- [overrun.md](overrun.md) — overrun fuel/ignition cut (rod protection)
- [boost.md](boost.md) — boost margin protection (a different limiter)
