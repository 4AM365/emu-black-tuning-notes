# DBW — EMU Black settings and the principles behind them

> **Software page:** *DBW*. Full symbol catalog: [tune_feature_tree.md → DBW](tune_feature_tree.md). Related software pages: TPS/PPS *sensor* setup is on [sensors_and_inputs.md](sensors_and_inputs.md); stuck-throttle cut is on [engine_protection.md](engine_protection.md).

The dedicated drive-by-wire / throttle document, organized like [idle.md](idle.md):

- **Part 1 — Settings**: one block per EMU Black DBW/throttle table — what it is, how to set it,
  how it fails, where the deep-dive + live values live.
- **Part 2 — Principles**: what governs throttle feel, lift-off protection, stuck-throttle safety,
  and throttle-body thermal behavior.

> **Idle owns the closed-throttle domain.** When PPS is at/near zero the throttle target comes
> from the idle system (armed airflow → idle PID), not the driver characteristic. Actuator range,
> idle blend point, armed airflow, and the `idleCustomCorrection` air bleed are all in
> [idle.md](idle.md); this document picks up where the pedal takes over.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md),
> [`airflow_actuator.md`](../supra/notes/airflow_actuator.md), and
> [`throttle_body_thermal_growth.md`](../supra/notes/throttle_body_thermal_growth.md).

---

# Part 1 — Settings (one block per EMU Black DBW/throttle table)

### DBW characteristic (PPS → TPS map)

- **What it is.** The pedal-to-throttle mapping — the biggest feel lever. No VSS or gear input;
  the RPM axis gives implicit partial gear awareness (first-gear creep lives in the low-PPS/low-RPM
  quadrant).
- **How to set it.** **Linear at high RPM** for predictable closing feel. **Scoop the
  low-PPS/low-RPM quadrant** to kill parking-lot/creep jerkiness, while **bumping the upper-PPS
  region** so throttle blips stay effective for downshifts. To run the "ready to launch" strategy,
  blow the plate open early and meter power via WGDC on PPS (T1). You can reference the
  characteristic on **MAP instead of RPM**, but watch the circular-logic trap (a gentle low-MAP map
  never builds MAP).
- **Failure modes.** Too aggressive low-PPS quadrant → creep jerkiness; MAP-referenced gentle map →
  can't build boost it's gated on.
- **Live values / deep-dive:** [throttle_feel.md](throttle_feel.md), [supra/notes/my_car.md](../supra/notes/my_car.md).

### TPS rate limit

- **What it is.** Limits how fast the plate opens/closes — controls low-speed "bucking." Range
  0–1300°/sec with a +125°/sec RPM-referenced adjustment on top.
- **How to set it.** A **moderate universal limit**, actually **reduced at high speed** so lift-off
  is gentler under high power, works best. Don't set the universal limit so low it fights the idle
  controller's own plate movements at idle. It governs **transient rate**, not steady-state target —
  it affects blip response, so **asymmetric open/close rates** are preferable if available (fast
  open, gentler close). A slower closure also delays lift-off MAP drop (secondary rod-protection
  help, T2).
- **Failure mode.** Limit low enough to "feel" → interferes with DBW idle operation.
- **Live values:** build doc.

### Boost-vs-PPS mapping / pre-throttle boost reference

- **What it is.** How power demand maps to wastegate duty (PPS-based) and where boost is referenced
  (pre-throttle vs plenum MAP).
- **How to set it.** Run **WGDC off pedal position** so power is commanded by the pedal with the
  plate already open (T1), and reference boost **pre-throttle** so the pressure is "ready to go" in
  the charge pipes per power demand. Boost target X-axis on `ppsBoostBins` with the closed-throttle
  column at zero boost, rising monotonically with pedal (cross-check: [ve_vs_map_at_constant_rpm.md](../ai-analysis-skills/ve_vs_map_at_constant_rpm.md)).
- **Live values / boost detail:** [boost.md](boost.md), build doc.

### Stuck-throttle protection → moved to Engine protection

The DBW stuck-throttle defense (dual-TPS plausibility, DBW position-error monitor, the brake-based
"Stuck throttle" box, and the fuel/RPM limp cap) is the EMU **Engine protection** page, so it now
lives in **[engine_protection.md → Stuck-throttle](engine_protection.md)**. Short version: PPS is the
correct discriminator (T3), lean on the sensor-referenced layers, keep the brake-based box permissive
because this build brake-boosts.

### Creep / low-speed handoff

- **What it is.** Behavior in the zone between idle control and driver demand at very low speed.
- **How to set it.** Soften the low-PPS/low-RPM characteristic quadrant (primary creep tool), and
  consider **raising the idle closed-loop cutoff** so the idle PID stays active into the creeping
  range rather than operating in a hand-off no-man's-land. The idle→characteristic blend point
  itself is [idle.md → DBW blend point](idle.md); the decel-fuel-correction RPM floor (which can
  mis-fire during a return) is [fueling.md → Decel fuel correction](fueling.md).
- **Live values:** build doc.

---

# Part 2 — Principles

## T1. Throttle feel = three levers, and a "ready to launch" philosophy

Throttle response is set by three things: **TPS rate limit** (how fast the plate moves),
**DBW characteristic** (the PPS→TPS map, the biggest lever), and **boost-vs-PPS mapping** (where
power actually comes from). The build's chosen philosophy: **blow the throttle open early** for
system efficiency and control power by **wastegate duty cycle on pedal position**, so the car
feels "ready to launch" — MAP up early, TPS applying power. That implies a **pre-throttle boost
reference** (pressure ready in the charge pipes per power demand). Caveat: a MAP-referenced
characteristic risks circular logic (a gentle map at low MAP never builds the MAP it's gated on),
so prefer RPM/PPS referencing for the characteristic. Full feel methodology:
[throttle_feel.md](throttle_feel.md).

## T2. Lift-off rod protection — the real mitigations are fuel/ignition, not throttle rate

On a high-boost engine, lifting off at high RPM is a rod-failure risk: MAP drops, overrun fuel cut
activates, and the drivetrain now **drives** the engine — every power-stroke piston is *pulled*
down with no combustion pressure behind it, loading the rod in **tension** (which rods tolerate far
worse than compression). The direct mitigations are **overrun fuel-cut strategy** (minimum-RPM
threshold, hysteresis, partial reduction instead of a hard cut) and **ignition cut instead of fuel
cut**. A slower throttle-closure rate delays MAP drop and thus fuel-cut onset, so it helps
*indirectly* — it is not the primary lever.

## T3. PPS is the correct stuck-throttle discriminator (and brake-boost is safe by it)

The dangerous case (throttle open, **pedal released**) and the intentional case (brake-boost:
throttle open, **pedal commanding it**) separate cleanly by **PPS**. Any protection that watches
**PPS-vs-TPS** is inherently brake-boost-safe — it can't trip while the driver is commanding
throttle. EMU's built-in **brake-based "Stuck throttle" box looks at brake + TPS only, blind to
PPS**, so it cannot tell a brake-boost from a stuck throttle and will cut a brake-boost at tight
settings. Therefore lean on the **pedal/sensor-referenced** layers as primary defense (dual-TPS
plausibility + DBW position error) and keep the brake-based box **permissive**. *This build
brake-boosts — never tighten the brake-based box or add a brake-gated cut.* Full strategy + config:
[stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md).

## T4. Throttle-body thermal growth — closed-plate leakage rises when hot

On the common **stainless / nickel-silver plate × aluminum bore** pairing, the differential CTE
(~4.5–5.3 ppm/°C) means the bore outruns the blade as the assembly heats → the radial clearance
**opens monotonically when hot** (Bosch does this deliberately so the plate never binds). At small
idle angles the dominant flow path **is** that radial clearance, so hot closed-plate leakage rises —
compensate it as a **CLT/IAT-indexed offset** (`idleCustomCorrection`), not a fixed DBW floor. The
correction is **more negative at lower idle RPM**: smaller idle TPS → smaller angle → open area is
clearance-dominated → a fixed absolute clearance growth is a larger *fractional* flow increase.
That RPM-dependence emerges purely from geometry, which makes it a **physics sanity check** on the
`idleCustomCorrection` table (and an upper bound on what's justifiable without log evidence). Full
derivation + the flow-area math: [throttle_body_thermal_growth.md](throttle_body_thermal_growth.md);
the table it bounds lives in [idle.md → Custom airflow correction](idle.md).

---

## Related documents

- [throttle_feel.md](throttle_feel.md) — full feel methodology: rate limit, characteristic, boost-vs-PPS (T1, T2)
- [stuck_throttle_protection_brake_boost.md](stuck_throttle_protection_brake_boost.md) — layered stuck-throttle defense + config (T3)
- [throttle_body_thermal_growth.md](throttle_body_thermal_growth.md) — TB thermal-growth physics + flow-area math (T4)
- [idle.md](idle.md) — closed-throttle domain: actuator range, armed airflow, blend point, custom correction
- [boost.md](boost.md) — wastegate / boost control (PPS-referenced)
