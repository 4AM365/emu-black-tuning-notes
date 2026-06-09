# Idle — EMU Black settings and the principles behind them

> **Software page:** *Idle*. Full symbol catalog: [tune_feature_tree.md → Idle](tune_feature_tree.md). Cranking/post-start is on [engine_start.md](engine_start.md); the overrun return is on [overrun.md](overrun.md).

The dedicated idle document. It is organized along two axes:

- **Part 1 — Settings**: one block per EMU Black idle/DBW table — what it is, what it
  controls, how to set it, how it fails, and where it lives. Each settings block links to
  the principle that justifies it and to the build's live values.
- **Part 2 — Principles**: the physics and control-architecture facts that make the
  calibration choices read as consequences rather than rules. These are car-agnostic and
  stable; they rarely change.

> **Car-specific values live in the build working docs**, not here. For the reference build
> see [`supra/notes/`](../supra/notes/) — esp. [`airflow_actuator.md`](../supra/notes/airflow_actuator.md)
> (live tables + actuator range), [`idle_session_05242026.md`](../supra/notes/idle_session_05242026.md)
> and [`my_car.md`](../supra/notes/my_car.md). This document tells you which table to set and
> which direction; the literal numbers for any one build live in those docs.

> **Diagnosing a specific failure?** The symptom-first decision trees live in
> [idle_stall.md](idle_stall.md) (stalls) and [return_to_idle_bog.md](return_to_idle_bog.md)
> (return-to-idle bog). This document is the table-by-table reference; those are the
> troubleshooting flow. Each settings block below links to the relevant section.

---

# Part 1 — Settings (one block per EMU Black table)

### Airflow% ↔ TPS% encoding (read this once)

Idle air is expressed as **Airflow%** (relative to the actuator range), not raw TPS:

```
TPS% = floor + (Airflow% / 100) × (ceiling − floor)
```

where `floor`/`ceiling` are `idleDBWTargetMin`/`idleDBWTargetMax`. Encoding of the raw tune
values (per [airflow_actuator.md](../supra/notes/airflow_actuator.md)):

- ubyte Airflow% tables (`idleActiveAirflow`, `idleArmedAirFlow`, `idleCrankingDC`): **0.5 / count** (raw = 2 × displayed %)
- `idleDBWTargetMin/Max`: word, **0.1 / count** (TPS %)
- `idleCustomCorrection`: sbyte, **1:1**, signed, **additive**

When the actuator range changes, every Airflow% table must be rescaled to preserve actual TPS —
the rescale rules live in [airflow_actuator.md](../supra/notes/airflow_actuator.md) and the
`emu-black-actuator-rescale` skill. **Never guess the conversion** — do per-cell math and verify
one cell empirically first.

---

### Actuator range — `idleDBWTargetMin` / `idleDBWTargetMax`

- **What it is.** The two scalars that map Airflow% (0–100) onto a physical TPS window. Floor =
  `idleDBWTargetMin`, ceiling = `idleDBWTargetMax`; width = ceiling − floor. Everything in the
  Airflow% tables resolves through this window.
- **How to set it.** Cold-start: override idle airflow and find the TPS it takes to idle at the
  **top** of your RPM range (cold post-start + A/C + cold-idle increases all stacked) — that's
  the ceiling. Hot: find the TPS to run just **below** ideal hot idle — that's near the floor.
  Set the floor **just below steady hot-idle TPS**, and set DBW min position DC% just below it
  too, so a light throttle tap can't drop you into a no-support gap. Wider range = less
  resolution; keep it only as wide as the cold ceiling demands.
- **Failure modes.** Floor set below hot-idle TPS → tip-in / warm stalls ([idle_stall.md §C4, §D](idle_stall.md)).
- **Live values:** [airflow_actuator.md → Actuator range](../supra/notes/airflow_actuator.md).
- **Principle:** [P5](#p5-cranking--active-handoff-the-manifold-time-constant) (handoff), [P1](#p1-idle-is-a-30-egr-engine-cams-push-it-over-the-stability-cliff).

### Idle target / ref table — `idleRPM`

- **What it is.** The commanded idle RPM vs CLT. It is the setpoint the whole idle system tracks,
  and it also **indexes the active airflow table** (see below).
- **How to set it.** Flat between ~70 °C and ~90 °C (oil is warmed up, drag is constant), rising
  **exponentially below ~71 °C** to overcome oil viscosity. On a cammed/turbo build, bias the
  warm target **up** — more intake momentum to fight reversion, more flywheel energy (∝ RPM²) to
  ride through weak cycles. A slightly higher summer target than winter is common. Keep extra
  scheduled variation out of it (heat-soak target steps add idle variation; fix idle by
  tightening the PID instead).
- **Failure modes.** Target too low on a cammed build → marginal stability, stalls under any load
  step. Noisy CLT makes the ref table oscillate ([idle_stall.md §E](idle_stall.md)).
- **Live values:** build doc (seasonal targets).
- **Principle:** [P1](#p1-idle-is-a-30-egr-engine-cams-push-it-over-the-stability-cliff).

### Active state airflow — `idleActiveAirflow`

- **What it is.** The feed-forward base airflow the idle PID runs **on top of**, active once RPM
  crosses 400 rpm. Indexed **X = Coolant °C, Y = Idle target RPM**. This is what opens the plate
  slightly on idle re-entry to cushion the RPM drop coming off higher RPM.
- **How to set it.** Must be calibrated from logged data — not optional. For each CLT/target cell,
  command the override airflow that holds the desired RPM, then write that Airflow% in. Spans from
  low (hot, low RPM) to high (cold, high RPM). The **highest-target row** is in play during the
  clutch-in cruise-decel handoff; if it's over-prescribed the PID winds negative each transit and
  dumps that correction when idle exits, producing a tip-in bump. Validate by logging `Idle PID
  air % correction` while sweeping the high-target band — PID should sit within a few % of zero,
  not pegged.
- **Failure modes.** **Indexed by target, which floors at the idle setpoint** — so its sub-idle
  rows are *never read* and **raising them does nothing** for a return-to-idle dip (the VE table
  owns that; see [return_to_idle_bog.md](return_to_idle_bog.md) / [idle_stall.md §H](idle_stall.md)).
  Over-prescribed high-target row → idle-handoff bump ([throttle_feel.md](throttle_feel.md)).
- **Live values:** [airflow_actuator.md → Active state air flow](../supra/notes/airflow_actuator.md).
- **Principle:** [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest), [P5](#p5-cranking--active-handoff-the-manifold-time-constant).

### Armed state airflow — `idleArmedAirFlow`

- **What it is.** Airflow vs RPM (8 bins) commanded when **PPS < ~2% but RPM has not yet dropped
  into the idle-PID engagement window** — i.e. the overrun glide down toward idle. Feed-forward
  guidance only; the idle PID is not yet in charge.
- **How to set it.** Higher decel-approach RPM bins: command **more** air than steady idle so the
  engine breathes through the transition (bias well open). Idle-approach bins: **match the active
  idle airflow value** for a seamless PID handoff — **no step at the bottom**. The whole table
  must stay **above the minimum useful airflow** at all times; below that the DBW motor just
  fights the return spring with no air benefit. The transition is transient (a second or two), so
  high values at high RPM never persist to steady idle. It should sit a small, tight margin above
  hot-idle airflow so the plate is held off its spring on re-entry.
- **Failure modes.** Resolves too low at the decel bins → DBW drives to its mechanical stop → fuel
  cut exits into a near-zero air column → rich spike → stumble → deeper RPM drop → feedback loop →
  **overrun-to-idle stall**. *The rich spike is the symptom, not the cause — fix the table and it
  disappears.* It is also the **off-throttle "parachute" lever**: hold higher airflow at high RPM
  / PPS=0 to prevent an instant torque drop to zero (trade-off: less engine braking).
  Full tree: [idle_stall.md §A](idle_stall.md), [return_to_idle_bog.md](return_to_idle_bog.md);
  parachute feel: [throttle_feel.md](throttle_feel.md).
- **Live values:** [airflow_actuator.md → Armed state air flow](../supra/notes/airflow_actuator.md).
- **Principle:** [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest).

### Cranking airflow — `idleCrankingDC`

- **What it is.** An independent open-loop DC table, active **below 400 rpm** (cranking state),
  indexed by CLT (cold → hot). No relationship to the active table — separate control path.
- **How to set it.** Pre-position the throttle for a **stepless handoff** at 400 rpm: for each CLT
  bin, set it to the active-airflow value the engine will want just above 400 rpm at that CLT/post-
  start target, then bias it a few percent **above** that matched value so the first idle
  correction is a gentle *pull-down* (the stable direction). Target ~60–80 kPa MAP during cranking;
  cold wants lower MAP (more vacuum → lower fuel boiling point, better vaporization). Don't restrict
  the throttle to build MAP on a big cam — defer to the airflow targets. Cranking *fuel* enrichment
  is a separate wall-film tax, **not** an air-starvation compensator.
- **Failure modes.** A step at the 400 rpm handoff → multi-time-constant RPM disturbance after
  start. Throttle slamming from cranking TPS to a lower idle TPS post-start → air deficit ASE can't
  cover → post-start stall ([idle_stall.md §B](idle_stall.md)); fix with an elevated post-start
  target, not by reducing ASE.
- **Live values:** [airflow_actuator.md → Cranking airflow](../supra/notes/airflow_actuator.md).
- **Principle:** [P5](#p5-cranking--active-handoff-the-manifold-time-constant).

### Custom airflow correction — `idleCustomCorrection`

- **What it is.** A signed, **additive** Airflow% correction on top of the active base, indexed
  **X = IAT °C, Y = Idle RPM**. Repurposed here as the **charge-temp air bleed**: a heat-soaked
  engine needs *less* air at the same RPM (hotter charge vaporizes fuel better and effectively
  advances timing), so this table pulls air out as charge temp climbs. Also the natural home for
  A/C-clutch comp (engagement time ~900 ms on an I6 — much faster than the airflow PID).
- **How to set it.** Size it **conservatively** — roughly half the steady-state correction the PID
  converges on — and let the closed loop ease in the rest (P3). It is deliberately gentle because
  **throttle-body metal temp lags CLT**: an aggressive bleed on the CLT/charge-temp schedule pulls
  air *before* the TB has actually heat-soaked and sags idle prematurely. The PID is meant to own
  the late hot-soak walk-down, not this table.
- **Failure modes.** Sized near "full" compensation → the airflow PID sits saturated against its
  negative clamp with TPS just above the floor → no headroom, stall risk if any load drops off.
  Halve it to restore two-way PID authority and grow the stall margin
  ([idle_stall.md → feed-forward conservative](idle_stall.md), [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md)).
- **Live values:** [airflow_actuator.md → Custom air flow correction](../supra/notes/airflow_actuator.md).
- **Principle:** [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest).

### Coolant-fan airflow correction — `idleCoolantFanCorr`

- **What it is.** A positive idle-air bump applied while the cooling fan loads the engine. It is
  **VSS-gated off above a speed threshold** (the fan's drag is negligible relative to road load at
  speed).
- **How to set it.** It is correct load-comp — **leave it.** Engagement strategy on the reference
  build: fan kicks on at CLT 70 °C if VSS is under threshold, which removes the fan-kick idle dip.
- **Failure modes.** On a return-to-idle *from above the speed gate*, the bump is off, so the base
  airflow is the bare table value and a clamped-too-low PID can't hold the depth → **rolling
  return-to-idle wobble**. The fix is **not** to change this table — it's more airflow-PID authority
  (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`) and a faster `idlePIDUpdateInterval`. Full
  tree: [idle_stall.md §H](idle_stall.md), [return_to_idle_bog.md](return_to_idle_bog.md).
- **Live values:** build doc (`idleCoolantFanCorr=13`, speed gate).
- **Principle:** [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest).

### DBW blend point — `idleDBWBlendPointTbl`

- **What it is.** The TPS/PPS at which the idle strategy is **fully exited** — the upper end of the
  idle-to-characteristic blend region (the PPS where the idle ref value equals the DBW
  characteristic value). Per-CLT table.
- **How to set it.** Set it **just above idle PPS** so there's a smooth ramp from idle control into
  driver demand. For consistent feel across temperature, track the idle table plus a fixed offset:
  `blend_point[CLT] ≈ idle_TPS_at_CLT + Δ`, where `idle_TPS_at_CLT` is the TPS the idle controller
  actually commands at that CLT (from `idleActiveAirflow` mapped through the actuator range) and **Δ
  is a fixed driver-preference offset** (a few % TPS) setting the perceived blend-window width. A
  flat value slightly above idle PPS works for a stable setup; run it a touch higher cold than hot
  if needed. **If `idleActiveAirflow` is rescaled, re-derive this table off the new values** or the
  blend window silently grows/shrinks at the cells you changed.
- **Failure modes.** Too low / gap between idle-exit and characteristic support → **tip-in stall**
  on a light throttle tap ([idle_stall.md §D](idle_stall.md)). At the exit, the airflow PID I-term,
  the idle ignition correction, and the source switch all release at once — a wound-negative PID
  dumps a TPS + timing step (the idle-handoff bump). Full discussion: [throttle_feel.md](throttle_feel.md).
- **Live values:** build doc (blend point + Δ, per-CLT idle TPS).
- **Principle:** [P2](#p2-the-emu-black-two-pid-idle-architecture) (what releases at exit).

### Airflow PID — `idleAirFlowKP` / `KI` / `KD` + limits

- **What it is.** The slow, air-trimming idle PID (P2). Output is **Airflow%**, so the gains and
  limits **scale with the actuator-range width** — widen the range and you must shrink them by the
  width ratio. Key symbols: `idleAirFlowKP/KI/KD`, integral clamp
  `idleAirFlowIntegralLimitMin/Max`, output clamp `idleAirPIDOutMin/Max`, and
  `idlePIDUpdateInterval`.
- **How to set it.** Tune **P-only first** (zero I and D), layer **I** to kill steady-state droop,
  add **D** sparingly only if overshoot appears. Size the integrator so corrections take ~5 s to
  reach steady state. **Keep the integral limit lower than the proportional limit** — P responds
  instantly and self-clears; the integrator accumulates, lags, and can trap the throttle shut.
  Critically, EMU exposes an **independent integral clamp**: cap the integral tight (anti-windup)
  but keep the **total** negative output wider, so P/D can spike transiently for a fast knockdown
  and then self-clear. If you only clamp the output, the integrator winds all the way to the output
  limit and windup returns.
- **Failure modes.** Integral limit too high → **windup**: integrator purges hot charge air, DBW
  forced shut, next load step can't refill fast enough → stall (hot-soak version:
  [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md); slow-droop version:
  [idle_stall.md §G](idle_stall.md)). PID clamped too low → can't hold a return-to-idle dip
  ([idle_stall.md §H](idle_stall.md)). Remember the PID **cannot** fix combustion instability
  (P1) — unstable λ reads as RPM noise no airflow authority can smooth.
- **Live values:** [airflow_actuator.md → Airflow PID](../supra/notes/airflow_actuator.md).
- **Principle:** [P2](#p2-the-emu-black-two-pid-idle-architecture), [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest).

### Idle ignition — `idleIgnitionTargetTbl` + `idleIgnitionMinTorqueAngleTbl` / `idleIgnitionMaxTorqueAngleTbl`

- **What it is.** The **fast** idle lever (P2). `ignTable`/`ignTable2` (ethanol-blended) set the
  **base** advance at the operating cell; `idleIgnitionTargetTbl` (0.5°/count, sbyte) is the
  **target** the idle controller drives toward at steady state; the Min/Max torque-angle tables set
  the **swing range** the controller may use around that target.
- **How to set it.** Set base idle advance **below MBT** so the controller has advance authority to
  recover dips (Banish/Hartman reserve-of-torque). Cammed builds idle with more advance than stock
  because the diluted charge burns slowly (peak pressure must still land near MBT) — see the
  fuel/cam idle-timing table in [engine_start.md](engine_start.md). Keep base **flat**
  across CLT/RPM and the PID window **narrow** (a few degrees each side) — varying timing with temp
  or RPM creates a competing feedback loop; let airflow own the mean. On a big cam the engine
  responds little per degree at idle, so lean on the airflow PID and trim with timing. To knock down
  a high hot idle, **use ignition retard (reversible), not an air purge** (stall-safe, P2) — if
  logged idle-ign correction uses only part of its swing, there's headroom in the Min-torque-angle
  table to let timing do more of the fast work.
- **Failure modes.** >10° of routine swing usually means a load-measurement or speed-pickup
  accuracy issue, not a timing-table problem (Banish). No reserve (base at MBT) → no recovery
  authority on a dip.
- **Live values:** build doc (base idle advance, target, swing limits).
- **Principle:** [P2](#p2-the-emu-black-two-pid-idle-architecture), [P1](#p1-idle-is-a-30-egr-engine-cams-push-it-over-the-stability-cliff).

---

# Part 2 — Principles

## P1. Idle is a ~30%-EGR engine; cams push it over the stability cliff

On *any* throttled SI engine the residual-gas fraction at idle is **~30%** (Heywood §6.4):
the throttle is nearly shut, manifold pressure is deep vacuum, and burned gas blows back into
the cylinder and intake during overlap, then gets re-inducted. That already puts a stock
engine near the **~20% "poor stability" threshold** (Heywood §9.4.3). Cams widen the overlap
window, so more burned gas reverts at low MAP — and a turbo's exhaust backpressure (turbine
restriction → EMAP > IMAP across idle) makes the reversion worse still. The diluted charge
burns slowly and erratically; erratic combustion → erratic torque → crank speed wanders → the
controllers chase it forever.

The levers the tuner actually pulls — **raise the idle RPM target**, **run idle λ slightly
rich**, **more base timing at idle**, **nail per-cylinder fuel trim first** — don't *cure*
instability; they move the operating point back from the misfire cliff so the controllers only
have to manage drift, not combustion. Two consequences that bound what the airflow loop can do:

- **The PID cannot fix combustion instability.** A charge that occasionally misfires produces
  RPM noise faster than the airflow loop (manifold time constant ~740 ms) can respond. The
  controllers hold the mean; the cycle-to-cycle scatter is combustion's, reduced only by
  reducing dilution.
- **The mass-flow estimator lies at idle.** Reverted flow reads as airflow even though most of
  it is exhaust — the channel can overstate true combustion airflow by ~10× at idle. Don't
  validate idle VE against it (see [supra/notes/mass_flow_estimator_quirk.md](../supra/notes/mass_flow_estimator_quirk.md)).

Full derivation (the dilution → slow-burn → partial-burn → misfire ladder, and every lever and
why it works): [cammed_idle_instability.md](cammed_idle_instability.md).

## P2. The EMU Black two-PID idle architecture

EMU v3 runs **two cooperating idle PIDs**, and which one owns what determines the right lever
for every idle problem:

1. **Ignition PID** — the **fast** RPM lever. Trims torque via timing within the Min/Max
   torque-angle swing. Reversible in one combustion cycle: no air purge, no throttle move, no
   fill lag.
2. **Airflow PID** — the **slow** lever. It does **not** act on RPM error directly; it acts on
   the error between the *current ignition angle and the Target ignition angle*, slowly
   trimming air to re-center the ignition PID so the two cooperate instead of fight.

This is the **opposite of v2** (where ignition was primary). Two consequences used throughout
Part 2:

- The **stall-safe way to knock down a high idle is ignition retard, not air** — timing
  reverses instantly; an air purge leaves the throttle shut and can't refill fast enough for
  the next load step.
- Keep the **ignition PID window narrow** (a few degrees each side). It is a fast transient
  corrector, not a primary RPM controller. Let airflow own the mean RPM.

Full architecture + the windup/purge/stall failure mode it explains:
[idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md).

## P3. Feed-forward should be conservative; the PID does the rest

When calibrating any open-loop / feed-forward idle-air correction (`idleCustomCorrection`,
fan/AC comp, charge-temp bleed, creep correction), bias toward **under-correction** — a useful
default is **apply roughly half the airflow change the engine actually needs** and let the
closed loop ease in the rest. The asymmetry is the reason:

| Failure mode | Cause | Severity |
|---|---|---|
| FF **under-corrects** | Engine briefly idles a little high while PID trims down | **Safe** — PID has full negative authority |
| FF **over-corrects** | Engine commanded less air than it needs; with transient lags it can hit the actuator floor before PID recovers | **Stall** — restart required |

Sizing: log the steady-state correction the PID converges on with no FF, halve it for the
table, verify PID's residual is now ~half and not saturated, then grow toward (never past) the
steady-state value — and never aggressively at sensor edges / extrapolated cells. Full rationale
and procedure: [idle_stall.md → "feed-forward should be conservative"](idle_stall.md).

## P4. Measure idle quality as RPM fluctuation, not knock voltage

Knock voltage is a **boost-region** tool. At idle the ring-down energy is tiny and the knock
packet is buried in mechanical noise, so CoV-of-knock at idle measures noise repeatability, not
combustion. The classic idle proxy is **crankshaft-speed fluctuation** (how OBD-II misfire
detection works). Two caveats:

- Primary metric is **error vs commanded `Idle target`** (bias, RMS, % within ±25/±50 rpm), per
  setpoint, in both thermal regimes — not CoV-around-own-mean, which forgives a steady offset.
- **True per-cycle combustion CoV is not recoverable from logged RPM.** Firing frequency at
  ~1000 rpm (6-cyl) is ~50 Hz; a 25 Hz autosave (Nyquist 12.5 Hz) aliases per-firing content
  down into the hunting band. Even 100 Hz only just touches the fundamental. RPM-hold CoV = idle
  *quality* (valid, use it); it is not a COV-of-IMEP number.

Full method, metric definitions, and the sample-rate wall: [idle_rpm_cov_stability.md](idle_rpm_cov_stability.md).

## P5. Cranking → active handoff: the manifold time constant

`idleCrankingDC` (cranking state, < 400 rpm) and `idleActiveAirflow` (running state, ≥ 400 rpm)
are **separate control paths with a hard handoff at 400 rpm**. The manifold time constant at
idle is ~740 ms (Kiencke & Nielsen §3.2.6), so a *step* in commanded air at the handoff takes
multiple time constants to settle and shows up as an RPM disturbance. The fix is to pre-position
the throttle during cranking so the handoff is **stepless** — set `idleCrankingDC` to the active
airflow the engine will want just above 400 rpm at that CLT. See the cranking and active-airflow
settings blocks below.

---

## Related documents

- [cammed_idle_instability.md](cammed_idle_instability.md) — full dilution/combustion physics (P1)
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — two-PID architecture + windup fix (P2)
- [idle_rpm_cov_stability.md](idle_rpm_cov_stability.md) — RPM-CoV metric and method (P4)
- [idle_stall.md](idle_stall.md) — symptom-first stall decision trees (§A–§H)
- [return_to_idle_bog.md](return_to_idle_bog.md) — consolidated return-to-idle entry point
- [engine_start.md](engine_start.md) — cold-start, cranking, ASE, idle-timing-by-fuel table
- [throttle_feel.md](throttle_feel.md) — DBW characteristic, blend point, tip-in/parachute feel
- [supra/notes/airflow_actuator.md](../supra/notes/airflow_actuator.md) — **live** tables, actuator range, rescale rules
