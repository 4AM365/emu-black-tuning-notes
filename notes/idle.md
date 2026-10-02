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

### Actuator range — **DBW Target min / DBW target max** (`idleDBWTargetMin` / `idleDBWTargetMax`)

- **Where it lives in the software:** *Idle → Actuator*, alongside the actuator-type selection —
  the same box that offers **Min DC / Max DC** for a PWM solenoid and **Stepper step range** for a
  stepper. Use the display names when talking about it; the `idleDBWTarget*` symbols are the XML
  storage names only. ECUMaster's own setup instruction names this pair as the anti-stall knob:
  *"Make sure the actuator can provide sufficient airflow for maximum idle RPM during cold start,
  and that it does not allow the engine to stall at minimum airflow (adjust DBW Target Min/Max or
  Solenoid Min/Max DC accordingly)"* — [`docs/emu-black-help/Idle.md`](../docs/emu-black-help/Idle.md).
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

### Afterstart RPM increase — `idleAfterstartRPMincrease`

- **What it is.** An adder on the idle target vs CLT × `idleRPMIncreaseRuntimeBin` (seconds since
  start), decaying to 0 (help: *Idle → Afterstart RPM increase*; the help gives no rationale).
  Bosch TDI (corpus `gasoline_engine_management_bosch.md`, p. 235) is the OEM form: the setpoint is
  raised above nominal in the post-start phase so the air path commands a torque reserve.
- **Its time axis says what it can be for.** The runtime bins span seconds, so it can only serve
  causes that are *transient over seconds after catch*. Anything lasting minutes (cold friction,
  cold combustion, catalyst heating) belongs to `idleRPM` vs CLT, which already carries it.
- **Causes that fit the window (why the post-start engine needs more torque reserve than the same
  engine a minute later at the same CLT):**
  1. *Wall-film building* — cold-start fuel precipitates on cold walls and does not burn at once
     (Bosch p. 108, "stable engine revving-up"); the first tens of cycles run erratic mixture. More
     RPM = more flywheel energy (∝ N²) per weak cycle and less time per cycle for heat loss
     (Heywood). Worse with overlap/residual dilution (cams: P1).
  2. *Unlubricated friction* — oil reaches the tap only after ~45–55 crank revs from a soak
     ([oil_pressure.md §Start-up oil fill](oil_pressure.md)); friction is highest and least
     predictable until then.
  3. *Electrical load* — alternator recharging the starter draw (model knowledge; vbat reaches
     charge voltage within ~0.2 s of catch in the Supra logs).
  4. *Controller handoff* — the loop starts from an open-loop cranking state with ~0.74–1 s of air
     lag (P5); a raised target keeps an undershoot above the stall zone.
- **Not a cause: oil priming.** The oil fill is volume-limited (fixed in revs), and cold pressure
  goes straight to the relief — RPM changes neither the revs turned dry nor the delivery after.
  No hydraulic lifters to pump up on shim/shimless-bucket heads. The common "high idle warms the
  oil faster" claim (web, 2026-09-29: torque.com.sg, sunautoservice.com) is a minutes-scale warm-up
  argument for `idleRPM`, not for a seconds-long bump. If anything, oil runs the other way: revs
  turned before pressure arrives are unlubricated, and the turbo is fed from the same gallery.
- **OEM practice (web, 2026-09-29).** Toyota's ISC runs open-loop for a period after start, then
  closed-loop, with fast idle scheduled on coolant temperature; a stock 2JZ-GTE with a working ISC
  catches around 1200 rpm and settles to ~700 over ~60 s (Link forum). That is a warm-up schedule
  (`idleRPM` vs CLT) plus a start-up air opening, not a seconds-long target flare. OEM cold idle is
  also raised for catalyst light-off (Kiencke §3.2.7 pairs it with ignition retard), which is
  minutes-scale and only matters with a cat fitted.
- **Engine-dependent weight.** Every cause above is a stall-margin argument, so the right size
  scales with how close the engine sits to the stability limit right after catch: more overlap,
  fewer cylinders, lighter rotating mass → more needed. An inline-6 (even 120° firing, heavy
  crank) needs less than a 4-cyl; big cams need more.
- **Coupled to `idleCrankingDC`.** Cranking airflow is sized to the active airflow at *target +
  bump* (see Cranking airflow below). Changing or zeroing the bump means re-deriving the cranking
  cells at the new landing target, or the held cranking air lands the catch high.
- **Supra evidence (09-29 log, CLT 26).** The engine ran steadily at 1396–1433 rpm from 3 s after
  catch while the film was still forming, and recovered from 1155 at 2 s. The catch flare
  (1782–2071 in three soaked starts) comes from cranking air + afterstart enrichment, not from the
  target bump.
- **Cost.** A decaying target is itself a disturbance the idle loop must follow; the bump's size
  and decay should be no larger than the margin the causes above require.

### Activation gates — `idleOnIfPPSBelow` / `idleOffIfPPSOver` / `idleMinMapToActivate` / `idleOpenLoopOverVss` (+ clutch/neutral enables)

These live on the EMU **Idle ▸ Activation** page and decide *when the idle controller is allowed
to close the loop at all*. Until every gate is satisfied the idle PID does not run, and on a DBW
car the plate simply follows the released pedal (shut) — so no airflow table matters until idle
activates. Order of importance for return-to-idle:

- **PPS gates (`Idle On if PPS below` / `Idle Off if PPS over`).** Pedal-based, with hysteresis
  (e.g. on <3 %, off >4 %). This is the "is the driver off the throttle" test. On a DBW build it is
  **PPS** (pedal), not TPS.
- **`Idle On if MAP over` (`idleMinMapToActivate`) — the one that traps people.** Idle activates
  only when MAP is **above** this value. It reads backwards until you realise **idle is not the
  lowest-MAP state — engine braking is.** A genuine idle cracks the plate for idle air and settles
  at moderate vacuum; a closed-throttle decel seals the plate while the engine pumps hard and pulls
  *deeper* vacuum (lower kPa). The three regimes line up as:

  ```
  deep vacuum ◄──────────────────────────────────► toward atmospheric
     engine braking      │  gate  │     idle            cruise / load
       ~13–17 kPa                       ~30–40 kPa        50–100 kPa
     (throttle SHUT,                  (throttle cracked
      pumping hard)                    for idle air)
  ```

  So the gate sits in the **valley between engine-braking vacuum and idle vacuum**. "MAP **over** X"
  = "we're at idle-or-higher pressure, i.e. genuinely idling — not in the deeper engine-braking
  vacuum, so it's safe to close the loop." If it were "MAP **under** X" it would do the opposite:
  wake idle *during* engine braking (and fight it) and stay off at a real idle. The PPS gate already
  knows the pedal is up; this gate exists purely to **disambiguate "pedal-up coasting in gear" from
  "pedal-up genuinely idling,"** since both have a closed throttle and only MAP separates them.
- **It's referenced to engine-braking vacuum, NOT idle vacuum.** This catches people on cammed
  builds: idle vacuum is *weak* (high MAP) because overlap/reversion kill low-RPM pumping, so a gate
  down in the high-teens *looks* absurdly deep "for an idle." But the gate's job is to clear
  **engine braking**, which is a *high-RPM, throttle-sealed* condition that pulls deep vacuum
  (commonly 13–17 kPa) **regardless of cam** — at 2500–3000 rpm pumping rate dominates and overlap
  barely matters. The cam actually *helps* here: it raises the idle-MAP floor and widens the gap the
  gate sits in. Judge the value against the braking band, not against where idle runs.
- **How to set `idleMinMapToActivate`.** Put it **just above the worst-case engine-braking MAP**
  (so it still excludes coasting) and **well below the idle-MAP floor** (so it never blocks real
  idle) — and confirm the floor across *all* idle conditions, including **cold fast-idle**, not just
  warm idle. Too high → on a fast return-to-idle MAP doesn't climb back over the gate until the engine
  is nearly stalled, so idle activates too late and stalls (see
  [return_to_idle_bog.md §3](return_to_idle_bog.md)). Too low → idle wakes during high-RPM coasting;
  benign-ish (at RPM ≫ target the airflow PID drives toward its minimum and actually preserves
  engine braking) but not the design intent. Read both bands off a log of the actual car
  (closed-throttle decel MAP-vs-RPM, and stable-idle MAP) and split the difference.
- **`Open loop over VSS` (`idleOpenLoopOverVss`) + clutch/neutral enables.** Above this road speed
  all PID is forced off and **the integral terms are reset** (log channel **`Idle force open loop`
  = Yes**). *Clutch enables closed loop* and *Neutral enables closed loop* let a clutch press or
  neutral cancel that force. **Before blaming VSS for a late activation, read `Idle force open
  loop`** — if it's No (e.g. a clutch press cleared it), VSS is not the gate; check MAP instead.
- **It is a DECOUPLING gate, not a high-speed safety cutoff — this determines how to set it.**
  The three parameters together express one rule: *close the idle loop only when crank speed is
  the throttle's responsibility.* Pedal up and rolling **in gear**, RPM is a driveline
  observable — grade, gear and vehicle inertia set it, not idle air. The loop still sees the
  difference as error and winds against it, and it has no authority to fix it. The accrued
  posture then survives until the driveline lets go, at which point it lands on an engine that
  no longer has the disturbance it was fighting: **RPM dips if the loop had wound negative (RPM
  was being held above target), flares if it had wound positive.** Sign depends on the last few
  seconds of grade and gear, so the same clutch-in feels different every time — that
  inconsistency is the diagnostic signature.
- **Therefore a LOW threshold (single-digit km/h) is the defensible setting, not a high one.**
  "Moving at all in gear" → open loop; the clutch and neutral escapes hand the loop back the
  instant the crank decouples. Clutch-slip creep keeps the loop closed via the clutch escape,
  which is the one rolling case where added air is genuinely wanted. A high threshold leaves a
  wide band of coupled rolling inside the closed loop, which is pure windup exposure.
- **How low: clear the speed channel's standstill noise floor, and no lower.** The error is
  asymmetric. Too high costs windup exposure (bounded, and only felt at the next clutch-in).
  **Too low is dangerous** — a speed glitch at a genuine stopped idle asserts the force and
  **wipes both integrals** while the engine is relying on them, which is a stall shape. Read the
  channel's max during a settled stopped idle from a log and set the threshold several times
  that. Inside the threshold band itself the gate has no hysteresis and will toggle while
  crawling at that speed with the clutch out — benign, because a reset there is exactly the
  intent (don't accrue while coupled); the wipe only hurts at a true stopped idle.
- **Prerequisite: a clean speed signal.** Every argument above assumes the channel is
  trustworthy near zero. Validate it before lowering the threshold — see
  [../supra/notes/vss_signal_integrity.md](../supra/notes/vss_signal_integrity.md) for a case
  where a mis-grounded switch made it read 81 km/h at a standstill.
- **Live values:** build doc.
- **Principle:** [P5](#p5-cranking--active-handoff-the-manifold-time-constant); diagnosis flow in
  [return_to_idle_bog.md](return_to_idle_bog.md).

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
- **The Y value is the *ramp-inflated* target, not the base setpoint.** The logged `Idle target`
  — and the value that indexes this table — is `idleRPM` **plus the remaining ramp-down offset**
  (`idleRAMPDownOffset`, decaying at `idleRAMPDownDecayRate`). So the axis must span
  *base target + offset*, not just the setpoint range, or every idle **entry** clamps to the top
  row and under-supplies air through the handoff. Corollary: **whenever `idleRPM` or
  `idleRAMPDownOffset` changes, re-check that `idleTargetBins` still brackets the range** — the
  axis silently goes stale, and the bottom bin is the one that bites (see below).
- **Verifying the axis empirically** (do this rather than assuming — target and RPM are collinear
  over most of a closed-loop idle log, so a whole-log fit cannot tell them apart). Reconstruct
  `base = Idle air % − Idle airflow custom corr. − Idle PID air % correction` over ACTIVE samples,
  then compare a table lookup on `Idle target` against one on actual `RPM` **restricted to samples
  where the two differ by >150 rpm** — the catch transient and any load sag. On the 2026-08-24
  Supra log this gave residual sd **0.59** (target) vs **4.29** (RPM): decisive. Catch is the
  cleanest single case (RPM 404 against target 1662).
- **Failure modes.** **Indexed by target, which floors at the lowest axis bin** — so if the bottom
  bin sits *above* the commanded hot setpoint, two operating points share one row and it cannot
  serve both. On the Supra (2026-08-24) a bottom bin above the hot target left one cell owing
  ~20 airflow % across a 200 rpm span: the lower point ran a standing **negative** PID (surplus,
  benign — the open-loop guarantee) while the higher one ran a standing **positive** PID with the
  integrator pinned at `idleAirFlowIntegralLimitMax` a third of the time. **The fix is the axis,
  not the values** — trimming the shared cell helps one point and worsens the other. Sub-idle rows
  below the floor are never read, so raising them does nothing for a return-to-idle dip (the VE
  table owns that; see [return_to_idle_bog.md](return_to_idle_bog.md) /
  [idle_stall.md §H](idle_stall.md)). Over-prescribed high-target row → idle-handoff bump
  ([throttle_feel.md](throttle_feel.md)).
- **Re-siting the axis is not a one-field edit.** Changing `idleTargetBins` **re-labels the
  existing rows without moving the cell data** — every row inherits a calibration made for a
  different target. Resample the existing surface onto the new bins and re-enter every row.
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

- **What it is.** An independent open-loop table active **below 400 rpm** (cranking state), indexed
  by CLT (cold → hot). **Units: airflow %, NOT a duty cycle** — confirmed on fw v59 (decodes ubyte
  ×0.5; UI title "Cranking airflow [%]"; shows up directly in the `Idle air %` log channel during
  cranking, e.g. raw 74 → 37.0%). The "DC" in the symbol name is historical. *(An earlier version of
  this note called it a duty cycle and described a TPS→DC back-calc — that was wrong; it's the same
  unit as the active table.)*
- **How to set it.** Pre-position for a **stepless handoff** at 400 rpm: per CLT bin, set it to the
  `idleActiveAirflow` % at the RPM you actually catch into — the **idle target *plus* the afterstart
  RPM increase** at that temperature (the engine fires into the afterstart-elevated state, not steady
  idle): a hot start → hot idle target + its small afterstart bump; a cold start → cold idle target +
  afterstart bump (the **top of the active range**, e.g. 1500 rpm). Add a **small margin** so the
  first idle correction is a gentle *pull-down* (the stable direction). It's a **direct airflow-%
  match** — no DC back-calc — though you can translate to TPS
  (`TPS% = idleDBWTargetMin + airflow%/100 × (idleDBWTargetMax − idleDBWTargetMin)`) to sanity-check
  the plate angle. Target ~60–80 kPa MAP during cranking; cold wants lower MAP (more vacuum → lower
  fuel boiling point, better vaporization). Don't restrict the throttle to build MAP on a big cam —
  defer to the airflow targets. Cranking *fuel* enrichment is a separate wall-film tax, **not** an
  air-starvation compensator.
- **Failure modes.** A step at the 400 rpm handoff → multi-time-constant RPM disturbance after start.
  Two opposite ways the cranking-airflow setting bites post-start, both fixed *here*, not with ASE:
  - **Too low / throttle slams to a lower idle TPS** → air deficit ASE can't cover → post-start
    **stall** ([idle_stall.md §B](idle_stall.md)); fix with an elevated post-start target.
  - **Too high (esp. hot)** → because the cranking airflow is **held open-loop through catch** (the
    PID is gated off for `idleControlAfterstartDelay`), it becomes the **flare setpoint** and the
    engine over-revs then under-damps into a sag. Lower the hot bins. Full root cause + lever order:
    [engine_start.md → Hot-restart flare → sag](engine_start.md#hot-restart-flare--sag-root-cause--levers).
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
  return-to-idle wobble**. The fix is **not** to change this table — it's more airflow-PID **output
  authority** (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`). If the PID is pinned on its clamp
  during the dip, that clamp is the only lever. Full tree:
  [idle_stall.md §H](idle_stall.md), [return_to_idle_bog.md](return_to_idle_bog.md).
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
  `idleAirFlowIntegralLimitMin/Max`, output clamp `idleAirPIDOutMin/Max`.
- **UI group (verified by screenshot):** `Idle → Airflow → Airflow PID` holds exactly seven fields —
  Proportional / Integral / Derivative gain, Integral term limit min/max, Output min/max. That is the
  whole group.
- **⚠ `idlePIDUpdateInterval` is not a tunable — treat it as vestigial.** It is absent from that dialog,
  undocumented across all 23 help pages, frozen at 200 in every tune export, and orphaned in the XML
  next to `starterOutput` / `enableBuzzerOnStartup` / `canBusTerminator`, ~350 lines from the idle PID
  block. Its only link to idle is the `idle*` name prefix. **Measured loop rate is ~40 ms, not 200** —
  so it is a v2 relic or an unexposed internal, and there is no sampling lag to tune away.
  **Method to verify on any build:** histogram the hold lengths of the PID-output channel in a log. A
  genuine 5 Hz loop gives 5-sample treads at 25 Hz; this one peaked at 1 sample (~54 %) with no spike
  at 5. Do this before believing any interval symbol.
- **Gain encoding & units.** Gains are stored raw and displayed **raw/1024** (verified: 2048 → 2.0,
  205 → 0.2002). Displayed units are **`%/°` (P), `%/(°·s)` (I), `%/(°/s)` (D)** — the error signal is
  *ignition-angle degrees*, not RPM (P2), and I/D carry **explicit time**, so the loop is
  **dt-normalized**. Consequence (now academic, since the interval isn't adjustable — see above):
  an update interval would multiply **no** gain, not P and not integral windup. A faster loop never
  *gives* more gain; it removes dead time, which *permits* more gain.
- **Saturation ≠ slowness.** When the PID pins on `idleAirPIDOutMax`, gains and loop rate are both
  irrelevant — only the clamp moves the ceiling. Size it from the actuator mapping:
  `throttle % per airflow % = (idleDBWTargetMax − idleDBWTargetMin)/100`.
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
  ([idle_stall.md §H](idle_stall.md)). **`KD`=0 + the ~750 ms DBW lag → an under-damped single swing
  on any large transient** (e.g. the post-start flare→sag:
  [engine_start.md → Hot-restart flare → sag](engine_start.md#hot-restart-flare--sag-root-cause--levers));
  a small KD is the derivative brake **in principle — but measure the derivative's SNR before
  reaching for it.** On this platform the outer loop's error (`Idle ignition correction`) is
  quantised at **0.5°**, so one LSB per ~40 ms tick is **12.5 °/s** of apparent dε/dt. Measured at
  settled idle: sd(dε/dt) = **6.0–6.8 °/s**, p95 = 12.5 °/s (i.e. pure quantisation). Measured
  during the desaturation transient the D term exists to catch: **1.0–3.6 °/s**. **Signal-to-noise
  ≈ 0.3** — a KD sized to compensate the 0.75 s lag (Td = τ_lag ⇒ KD = kP × 0.75 = 0.225 at
  kP 0.30) would inject ~1.4 airflow points of continuous idle jitter (~18 rpm) to buy ~0.45 points
  of anticipation. **Keep KD = 0 and buy the anticipation with kP instead** (see the P/I split
  below). Note also that KD's raw scaling cannot be verified from a log while it is 0.
  **Exception — load steps (A/C engagement), measured 2026-10-02** (`restartbounce.csv`, see
  [log_2026-10-02_restartbounce.md](../supra/notes/log_2026-10-02_restartbounce.md)): the ignition
  correction swings ~15° in under a second, peaks |dε/dt| 40–60 °/s against settled sd 2.8–4.6 °/s,
  SNR ≈ 10. The 0.3 SNR above is for the slow desaturation transient and still holds there. Per
  engagement at kP 0.5 the P term adds +7 air over the dip and removes 5–8 on the recovery, all through
  the air lag, and that late air is the overshoot. A KD of 0.1 %/(°/s) would add +1.4–1.8 mean (+3.3
  peak) over the dip and −0.9…−1.6 on the recovery, about 0.2 s earlier than P, for settled jitter about
  equal to the kP 0.5 P term's. Unverified until `Monitored D term` is logged with KD ≠ 0.
  Remember the PID **cannot** fix combustion instability
  (P1) — unstable λ reads as RPM noise no airflow authority can smooth.
- **Live values:** [airflow_actuator.md → Airflow PID](../supra/notes/airflow_actuator.md).
- **Principle:** [P2](#p2-the-emu-black-two-pid-idle-architecture), [P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest).

#### Setting `idleAirFlowKP` from a logged oscillation

Any decaying idle oscillation contains everything needed to compute the gain margin — no
step test, no tune reading. Tooling:
[emu-black-idle-pid-gain](../skills/emu-black-idle-pid-gain/SKILL.md).

**Measure kP from the log.** Regress `Idle air %` on `Ignition Angle`. Because the airflow
PID's error *is* (Ignition Angle − Target ignition angle) (P2), **the slope is kP in %/deg**.
Base airflow only shifts the intercept and drifts on the CLT timescale, so it can't bias the
slope. A high R² simultaneously proves the loop is P-dominated — which is the usual case:
with KI around 0.2 %/(°·s) against a kP of order 1, the P/I crossover is ~0.1 rad/s, a 60 s
period, invisible at a 1.5 s oscillation.

**Napkin gain margin — count cycles, don't measure amplitude.**

```
δ = ln(1/f)/n        f = fraction of amplitude left after n cycles
ζ = δ/2π             kP/Ku ≈ 1 − δ/π      (near the boundary only, ζ ≲ 0.15)
```

A *sustained* oscillation needs no amplitude at all — that's Ziegler–Nichols, kP = Ku. A
decaying one does, but cycles-to-settle already encodes it. Verified to ~1% against the full
solve.

**Full solve.** Take the pole (`δ`, `T`) → `σ`, `ω_d`, then fit `(τs+1) + K·e^(−Ls) = 0` at
that pole for a range of assumed τ. **Near the stability boundary `kP/Ku` comes out almost
τ-independent** — that is what makes the answer trustworthy without knowing the plant. Ku
then follows from the phase crossover `atan(ωτ) + ωL = π`.

**Where to land.** ZN's 0.5·Ku targets quarter-amplitude decay, a disturbance-rejection
criterion for a *primary* controller. This isn't one — it's the outer half of a mid-ranging
pair that should be boring, so aim **0.25–0.30·Ku** (one small overshoot, ζ ≈ 0.5–0.6).
Three consequences that repeatedly surprise:

- **Lower gain settles faster.** Near Ku the loop rings for tens of seconds; at 0.3·Ku it's
  done in ~2 s.
- **Residual "walking around" at idle is the same gain, not a second fault.** The P term
  multiplies the ignition PID's cycle-to-cycle jitter into continuous throttle motion, which
  stirs RPM, which feeds the ignition PID. Diagnostic: if `sd(air%)/sd(ign)` ≈ kP in a short
  settled window, the wander *is* the P term, and it falls linearly with kP.
- **KI needs no compensating change.** Cutting kP raises the P/I crossover, so relative
  integral authority goes *up*; the extra phase lag at crossover is a few degrees.

Two cross-checks before applying: settled `Ignition Angle` should sit on
`idleIgnitionTargetTbl` (if it does, the cascade is healthy and only the gain is wrong), and
the output ceiling (`kP × max presentable error` + `idleAirFlowIntegralLimitMax`) was sized
around the *old* kP — re-check it after the change.

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

### Why the outer loop targets ignition angle, not RPM (and what it actually buys)

The airflow PID is a **mid-ranging** (valve-position) controller: its process variable is the
*inner loop's control effort*, not the plant output. Standard where two actuators share one job
and neither is both fast and wide —

| Actuator | Response | Range |
|---|---|---|
| Ignition angle | < 1 combustion cycle | narrow — ~±5° effective, ~50–80 RPM of authority ([K&N](../corpus/automotive_control_systems_kiencke_nielsen.md)) |
| Airflow | ~740 ms manifold lag | effectively unbounded |

So spark holds RPM; air chases spark back toward `Target ignition angle` so the fast lever keeps
authority in **both** directions.

**No airflow PID is required for the engine to run.** Pre-electronic engines idled on *droop*:
the engine's own torque-speed slope is negative through the idle region (pumping + friction rise
with N faster than the airflow gain), which is a proportional term built into the plant. It
yields a stable equilibrium, not a chosen one — every load offset moves the point and leaves it
moved. The historical fixes were all open-loop schedules that map 1:1 onto EMU tables: choke
fast-idle cam → CLT base airflow, A/C idle-up solenoid → fan/AC comp, vacuum advance → idle
ignition schedule. The driver's throttle blip was the only closed loop.

**What the airflow PID buys is therefore not "running" — it's not having to enumerate the
disturbances.** With no integral term, any base-table vs. true-demand gap becomes a permanent
offset that the ignition PID absorbs by parking off-center, and an off-center ignition PID is an
asymmetric one:

- pinned toward **Max torque ign. angle** → no advance reserve left; the next load step drops RPM
  and nothing catches it (this is the P1/stall path);
- pinned toward **Min torque ign. angle** → burning fuel into the exhaust to hold a setpoint that
  cheaper air would have held.

The PID's product is **symmetric ignition authority at every operating point**, obtained without
individually scheduling oil viscosity, TB heat soak, alternator field, fan, A/C and gear
engagement. Trading it away for an open-loop table (as the oil-viscosity trim deliberately does,
[oil_viscosity_idle_airflow.md](../supra/notes/oil_viscosity_idle_airflow.md)) is legitimate — it
just moves the burden onto the schedule.

**Empirical confirmation on this car:** the airflow PID is already gated off during afterstart
delay, under `Idle force open loop`, and across the cranking flare. Idle in those windows is pure
base table and holds. Which is exactly why **base airflow is the open-loop guarantee** and why a
steady negative PID average is diagnostic, not a cue to trim the table
([P3](#p3-feed-forward-should-be-conservative-the-pid-does-the-rest)).

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

Full method, metric definitions, and the sample-rate wall: [idle_rpm_cov_stability.md](../ai-analysis-skills/idle_rpm_cov_stability.md).

## P5. Cranking → active handoff: the manifold time constant

`idleCrankingDC` (cranking state, < 400 rpm) and `idleActiveAirflow` (running state, ≥ 400 rpm)
are **separate control paths with a hard handoff at 400 rpm**. The manifold time constant at
idle is ~740 ms (Kiencke & Nielsen §3.2.6), so a *step* in commanded air at the handoff takes
multiple time constants to settle and shows up as an RPM disturbance. The fix is to pre-position
the throttle during cranking so the handoff is **stepless** — match the **TPS the idle controller
will land on for that start**. The engine catches into the **afterstart-elevated** RPM, not steady
idle, so set `idleCrankingDC` to the active-airflow % at `idle target + afterstart RPM increase`
for that temperature (hot start → hot idle target + small bump; cold start → cold idle target +
bump, the top of the active-airflow range, e.g. 1500 rpm), plus a small margin so the first idle
correction is a gentle pull-down. `idleCrankingDC` is itself an **airflow %** (same unit as the
active table — confirmed fw v59; the "DC" name is historical), so it's a **direct match**, no
TPS/duty back-calc. **Caveat:** that margin is *held open-loop* through catch (PID gated for
`idleControlAfterstartDelay`), so an over-high hot value becomes the flare setpoint — see
[engine_start.md → Hot-restart flare → sag](engine_start.md#hot-restart-flare--sag-root-cause--levers).
See the cranking and active-airflow settings blocks below.

---

## P6. Ramp-down entry: the two-step is inner-loop desaturation, not a gain fault

**Symptom.** On every return to idle the RPM falls, *hangs* at an arbitrary value well above
target, then drops in a distinct step, then creeps the rest of the way. Two steps inside one
ramp. Measured on `more_pid_all_channels.csv` (2026-08-30), 8 entries, hot (CLT 98–101 °C):

| phase | what is happening | measured |
|---|---|---|
| hang | `Idle ignition correction` pinned at the `idleIgnitionMinTorqueAngleTbl` rail | plateau 1143–1246 rpm, rail held 3.2–6.1 s |
| step | ignition desaturates, advance returns toward `Idle ignition target` | RPM drops 39–126 rpm (median ~95) in <1 s |
| creep | airflow PID finally in its linear region, integral walks the remainder | 1063–1103 → target over a further 6–60 s |
| converged | | within ±25 rpm at **9–14 s** after ACTIVE entry |

**Mechanism.** The airflow PID's error is the *ignition* PID's angle error (P2), so when the
ignition PID saturates against its min-torque-angle rail, the outer loop is handed a **clipped,
constant** error. It then winds at a fixed open-loop rate — `KI × rail depth` — and nothing about
the RPM error modulates it. RPM does not fall during this phase because the excess air and the
retard cancel. When enough air has been removed that full retard is no longer needed, the angle
recovers several degrees in well under a second; idle torque is steep in timing at 11–18°, so
that recovery *is* the step. Everything after it is the normal linear settle.

**The rail is structural once the excess outgrows what retard can mask.** Measured masking
capacity: the ignition rail absorbs roughly **10 airflow points** (ignition unrails at 33–38.5 %
commanded against a ~49 % base). Wherever along the ramp `base − required` passes ~10 points, the
inner loop rails and the two-step is guaranteed from there down. **The excess is not constant along
the ramp** — see the target-binned table below: it is ≈0 at the top and ~24 points at the held
target (base 48.7 % vs converged requirement 24–26 % at 1025 rpm, CLT 100, oil hot), crossing the
masking capacity around 1200–1250 rpm, which is exactly where the measured plateau sits.

**Corollaries — what does and does not change the step**

- **Airflow gains change the durations, not the step height.** Identified from the log
  (gains decode raw/1024): kP 0.300 → 0.200 %/°, KI 0.30 → 0.49 %/(°·s) partway through the
  same log. Time to ±25 rpm improved 12.3 s → 9.1 s; step height was 96 vs 95 rpm — unchanged.
  Step height is set by the retard depth (here a hard −7.0°, absolute 11°), not by the outer loop.
- **The ramp-down offset is not shaping the descent.** `idleRAMPDownOffset` decays at exactly
  `idleRAMPDownDecayRate` (125 rpm/s measured = raw 125, scale 1) and reaches zero in **2.8 s**,
  while the engine needs **9–14 s**. When the offset hits zero the RPM is still **+177 to +284**
  above target on every entry. A target that finishes four times faster than the plant is a step
  wearing a ramp's clothes: it guarantees a large sustained inner-loop error, hence the rail.
- **That overrun is also the bog mechanism.** While the target leads, the outer integral winds at
  its full railed rate for the *whole* lead time and can only stop once the angle desaturates —
  which is inherently late. The accumulated surplus of negative airflow shows up as an undershoot
  below target on arrival (988–1007 rpm against a 1025 target; sags to 956–982 with the integral
  pinned). Longer lead ⇒ more accumulation ⇒ deeper bog. This is the ECUMaster help's own warning:
  tune the decay rate so RPM falls **in sync with** the offset, "to prevent PID saturation and a
  RPM dip below target".
- **The engine tracks about half the commanded decay, and rails before the ramp ends.** Across
  the ramp window (offset 350 → 0): tracking error grows from **+5 to +16 rpm at the start** to
  **+132 to +282 rpm at the end**; engine slope is **−64 rpm/s median against −125 commanded
  (52 %)**; the ignition PID reaches its rail at **1.7–2.5 s into a 2.8 s ramp**, i.e. before the
  offset has finished decaying, on 8 of 9 entries. So the ramp is not "nearly right" — it is
  outrunning the plant from the first half-second.
- **The knee at the handoff is on the engine side, not the target side.** Incoming ARMED
  deceleration is **−35 to −515 rpm/s** (median ≈ −105 over the last second); within 0.5 s of
  ACTIVE entry it collapses to **−29 to −137 rpm/s**. Nothing in fuelling explains it —
  `Fuel cut percent` is 0 for the whole log, `Overrun fuel corr.` is 0 either side, injector PW is
  unchanged to 0.02 ms, and `Ignition Angle` moves ≤0.5°. What changes is base airflow. Raising
  `idleRAMPDownDecayRate` to match the *arrival* slope therefore has the sign backwards: it makes
  the setpoint C1-continuous at the boundary while widening the gap to what the loop delivers.
  Two continuity conditions conflict — setpoint-slope-matches-arrival (~200 rpm/s) versus
  trackability (~64 rpm/s) — and they only converge once the airflow discontinuity below is gone.
- **ARMED → ACTIVE hands the engine *more* air.** At the crossover (target + offset) the base
  switches from `idleArmedAirFlow` to `idleActiveAirflow`, and on this calibration that is a
  **+3.9 to +5.7 airflow-point step upward** on 8 of 10 entries — applied at the instant the
  engine is supposed to be decelerating. Match the two tables at the crossover RPM/target.
- **A linear ramp cannot be exponential.** `idleRAMPDownDecayRate` is rpm/s; the only shaping
  parameters are that rate and `idleTargetRampDelay` (a pre-delay, not a curve). A first-order
  approach comes from letting the *plant* do the shaping: keep the target's lead small enough that
  neither PID rails, then the closed loop's own dominant time constant produces the exponential
  tail. Measured lead at which the ignition desaturates: RPM within roughly **50–90 rpm** of target.
- **Measured achievable descent** (pooled, hot, this calibration): 70 rpm/s from 1300→1200,
  31 rpm/s 1200→1100, 20 rpm/s 1100→1050, 7 rpm/s 1050→1030. A decay rate near the low end of that
  band tracks the plant instead of outrunning it. It lengthens the between-shift hang, which the
  same offset governs — that trade is real and belongs to the driver, not the note.

**The retard floor is the min-torque-angle clamp, not the ignition integral limit.** These are
different mechanisms and it is easy to conflate them. `idleIgnitionIntegralLimitMin/Max` (±5°)
bound only the **I component**; the PID's *total* output is then clamped to
`idleIgnitionMinTorqueAngleTbl` / `idleIgnitionMaxTorqueAngleTbl` in **absolute** degrees. With
`idleIgnitionKP` = 0.0498 °/rpm, P alone reaches −7° at a 140 rpm error and −8.7° at 175 rpm — the
integral never has to contribute anything to saturate the output. Measured floor of the absolute
`Ignition Angle` by RPM bin (target flat 18°): 12.0° at 1000–1100, 11.0° at 1100–1300, 10.5° at
1300–1400 — matching the min-torque table's 13/12/11/10° range, so the correction floor is simply
*(min torque angle − 18)*. **Note also that `Monitored P/I/D term` is the AIRFLOW PID's monitor
(its P saturates at kP × rail = −2.40), not the ignition PID's — the ignition loop has no monitor
channel.**

**Trackability of the ramp — the governing arithmetic.** Measured on the creep phase by partial
regression `air ~ a·RPM + b·ign` (6 segments, R² 0.64–0.96): the airflow requirement is
**a ≈ 0.092 %/rpm** (range 0.069–0.107). The base table's own target-axis slope at CLT 100 is
**0.013 %/rpm** — so the feed-forward supplies only **14 %** of the needed reduction and the
integrator must supply the other 86 %. Hence

> `D_trackable  =  KI × |ignition error| / (0.092 − 0.013)`

| KI %/(°·s) | never rails (3.5°) | at the rail (7°) | in-flight over-subtraction at desat (× 0.75 s lag) |
|---|---|---|---|
| 0.30 (raw 307) | 13 rpm/s | 27 rpm/s | 0.8 / 1.6 pts |
| 0.49 (raw ~500) | 22 rpm/s | 44 rpm/s | 1.3 / 2.6 pts |
| 1.00 (raw 1024) | 45 rpm/s | 89 rpm/s | 2.6 / 5.2 pts |

So at present gains the trackable decay rate is **≈20 rpm/s**, against 125 commanded. Raising KI
buys rate linearly but buys overshoot linearly too — the in-flight column is the airflow already
commanded but not yet in the cylinder when the inner loop desaturates, and it is the bog.

**The excess is not constant along the ramp — it is ~0 at the top and ~24 points at the bottom.**
Anchor the requirement line at the *measured* held-idle requirement (24–26 % at 1025), not at the
table's own value there. Then `idleActiveAirflow` is over-aired by ~24 points at 1025 and sits
**at equilibrium** near the top of the ramp; arithmetic crossover ~1330 rpm. Measured directly —
ACTIVE ramp samples binned by commanded target, `Idle ignition correction`:

| commanded target | 1350–1400 | 1300–1350 | 1250–1300 | 1200–1250 | 1150–1200 | 1100–1150 | 1050–1100 | 1000–1050 |
|---|---|---|---|---|---|---|---|---|
| mean ign corr | **+0.19** | +0.61 | +0.56 | −0.79 | −2.50 | −5.18 | −6.37 | −6.24 |
| base % | 52.7 | 52.1 | 51.2 | 50.7 | 50.2 | 49.8 | 49.3 | 48.9 |

The inner loop needs no retard at the top of the ramp and is on the rail by the bottom. Entry
samples say the same thing: at target ≈1340 the ignition correction across 9 entries runs −1.73 to
+1.85, averaging ≈0, with the airflow PID still at 0. **So the top rows are right and the bottom
row carries the whole cold-oil allowance** — do not "correct" the upper rows upward from a slope
extrapolation anchored on the 1025 cell (an earlier revision of this note did exactly that and was
wrong). `Airflow %` is a throttle-*position* command on a strongly nonlinear near-closed throttle;
never extrapolate a locally-measured slope across the axis.

**Reconciling the ARMED glide rate with the ACTIVE approach.** ARMED falls fast (−35 to −515 rpm/s,
median ≈ −105 over the last second) because `idleArmedAirFlow` sits *below* the equilibrium
requirement — a deliberate torque deficit. At the handoff the base becomes the Active table's top
row, which is *at* equilibrium (ign corr ≈ 0, above). **The deficit goes to zero, so the
deceleration stops — that is the knee.** ACTIVE must then *manufacture* a new deficit by winding
the integrator, at no more than `KI × |ign error|` points/s. Hence a hard floor on ramp duration:

> `t_ramp,min = excess_at_held_target / (KI × rail depth)` → 24 / (0.49 × 7) = **7.0 s**
> ⇒ `idleRAMPDownDecayRate ≤ 350 / 7.0 ≈ 50 rpm/s` (and ≈25 rpm/s if the loop must never rail)

**Sizing `idleRAMPDownOffset`: the crossover must sit above where the ARMED table alone would
settle the engine.** If it doesn't, RPM stops falling and the controller never leaves ARMED — the
failure ECUMaster's help names directly ("if RPMs are not dropping as expected and the idle
controller remains in Armed state, reduce values in the Armed state airflow table"). Measure it,
don't compute it: bin ARMED samples (pedal up) by RPM and read the smoothed dN/dt.

| ARMED RPM band | 1300–1400 | 1400–1500 | 1500–1600 | 1600–1700 | 1700–1900 | 2000+ |
|---|---|---|---|---|---|---|
| median dN/dt (rpm/s) | −92 | **−44** | **−46** | −281 | −516 to −556 | −188 to −356 |

The engine is **still descending at the 1375 crossover**, so today's offset clears the hang point —
but the glide has already slowed to **~45 rpm/s through 1400–1600**, and that is the engine's free
deceleration with no PID at all. Note this also caps ambition: a 200 rpm/s commanded decay is 4.4×
the engine's *own* rate in the band just above the crossover. A straight-line requirement
extrapolation puts the ARMED equilibrium near ~1300 rpm; the measured profile shows the requirement
curve is **concave** (airflow % is a throttle *position* on a nonlinear near-closed throttle), so
treat ~1300 as a soft floor for the crossover, i.e. **offset ≥ ~300 at a 1025 target**.

**Hard ceiling: `idleTargetBins` must span `idleRPM + offset`.** Top bin 2000, hot `idleRPM` 1025
⇒ any offset above **975** silently clamps the base-airflow lookup to the 2000 row and the
feed-forward stops responding to the ramp at all.

**A bigger `idleRAMPDownOffset` does not buy runway.** `idleArmedAirFlow` and `idleActiveAirflow`
are **near-parallel** — decoded at CLT 100, the handoff step is +6.8 pts at 1000, +5.6 at 1200,
+5.3 at 1375, +5.4 at 1500, +5.7 at 1625, +5.7 at 1800. (Cross-check: predicted armed 47.8 /
active 53.2 at the 1375 crossover against measured 47.0–48.3 / 52.1–52.8.) So **the knee is the
same size wherever on the axis you enter** — moving the entry point up changes nothing about it.
Worse, the integrator only winds where there is excess, and there is none at the top: measured
`Idle PID air % correction` by commanded-target bin runs **+0.04 / +0.20 / +0.31** at 1350–1400 /
1300–1350 / 1250–1300 — it winds the *wrong way* up there. A larger offset extends that wrong-way
region, lengthens the integrator's journey, and adds elevated-idle time. Same knee, slower result.

**The mirror of "give ACTIVE a deficit" is "take the deficit out of ARMED."** Raising the armed
cells to meet the active table (~+5.4 pts at 1375) removes the step by removing the glide: the
engine arrives at the crossover already decelerating slowly, so there is nothing to reconcile.
It costs coastdown feel on a manual — the lift will hang.

Observed convergence is 9–14 s, consistent. Commanding 200 rpm/s would require 24 points in 1.75 s
= 13.7 points/s = KI ≈ 2.0 railed or ≈3.9 unrailed (4–8× current), leaving 10–22 airflow points in
flight at desaturation — a bog generator. The three honest ways to close the gap: put the Active
table's **hot** upper cells slightly *below* equilibrium so ACTIVE inherits the glide (removes the
knee, gives the integrator a head start — at the cost of a sub-equilibrium base if ACTIVE is
entered low); enlarge `idleRAMPDownOffset` so ACTIVE starts earlier and has more runway; or slow
the decay to what the loop delivers. **Acceptance test for any of them:** re-bin `Idle ignition
correction` by commanded target as above — if it stays within ±2° across the whole ramp, the ramp
is trackable.

**The ignition PID is not the lever.** Identified from the same log: `idleIgnitionKP` = 51/1024 =
**0.0498 °/rpm** — confirmed at the settled point (a −12 rpm error produced exactly −0.6° of
correction). It therefore rails at ~140 rpm of error, which is the right place: not twitchy on
small errors, not lazy on large ones. `idleIgnitionKI` = 5/1024 = 0.0049 °/(rpm·s) is deliberately
glacial and should stay that way — in a mid-ranging pair the **outer** (airflow) loop supplies the
integral action, and giving the inner loop real integral makes the two fight. `KD` = 0 is correct
on a lever that acts within one combustion event. The only ignition parameter that touches the
step is the rail depth, `idleIgnitionMinTorqueAngleTbl`, and it is a strict trade: raising it
shrinks the step but raises and lengthens the hang and spends the flare knock-down authority;
lowering it deepens the step and idles a ~30 %-residual engine at 8–9°, which is where combustion
stability goes. Leave both tables alone and remove the saturation instead — then the min-torque
table reverts to stall/flare insurance, which is what it was doing when the +17° reserve caught
the 454 rpm event.

**If the decay rate is a fixed requirement, the ramp must be carried by feed-forward, not gain.**
A 200 rpm/s decay is a 1.75 s ramp. The integrator can travel `KI × 7 × 1.75` = 3.4 points in that
window at KI 0.49; it needs 24. Closing that by gain alone wants **KI ≈ 2.0 %/(°·s)**, which parks
`KI × err × 0.75 s` ≈ **10 airflow points in flight** when the inner loop desaturates — ~110 rpm of
undershoot at 0.092 %/rpm. Feedback cannot close a 24-point gap in 1.75 s at any sane gain.

The trajectory is *known*, so it belongs to feed-forward. Two **measured** anchors bracket the ramp
span: requirement(1025) = 25 % (converged, hot) and requirement(1375) = 52.7 % (base at entry with
`Idle ignition correction` ≈ 0). The chord between them is **0.079 %/rpm** — independent of, and
close to, the 0.092 %/rpm creep-phase partial. The table's own Y slope over that span is
**0.0117 %/rpm**, i.e. **6.8× too shallow**. For the base alone to carry a 200 rpm/s ramp it would
have to follow `25 + 0.079·(target − 1025) + margin`.

**But that only relocates the hang, it does not remove it.** With the margin carried up the axis
(constant, as a friction term should be) the excess is ~24 at *every* target: the inner loop rails
at entry, the engine hangs high for `24 / (KI × 7)` ≈ 7 s, and only then descends — cleanly, at
200 rpm/s. Today's shape (margin at the bottom row only) gives the opposite: a smooth entry and the
two-step later. **24 points of cold-oil insurance cannot be hidden anywhere inside a 1.75 s ramp.**
The margin is the constraint, and it goes away only when the oil-temperature correction replaces
it — at which point base ≈ requirement, integrator travel ≈ 0, and a fast ramp tracks with no hang
at all. That, not gain tuning, is what unlocks a fast decay rate.

**Shift authority from I to P — P is the right lever for trajectory following.** P responds
instantly to the error, is bounded by the output clamp, and — critically — **releases itself the
moment the error clears, so it contributes nothing to the in-flight overshoot.** I is the term that
must be unwound, and unwinding through a 0.75 s lag *is* the bog. Today's loop is badly P-starved
for a trajectory task: at the −7° rail, P contributes only −2.1 points of a 24-point job (9 %).

Sizing, for "P+I reaches the −25 clamp within the ramp window T", with the in-flight balance at
desaturation (`KI × 7 × 0.75` committed by I, against `kP × 7` released by P):

| kP %/° (raw) | P at rail | share | KI for T=1.75 s (raw) | I in flight | P releases | **net** |
|---|---|---|---|---|---|---|
| 0.30 (307) | −2.1 | 9 % | 1.87 (1914) | 9.8 | 2.1 | **+7.7 (bog)** |
| 0.50 (512) | −3.5 | 15 % | 1.76 (1797) | 9.2 | 3.5 | +5.7 |
| **1.00 (1024)** | **−7.0** | **29 %** | **1.47 (1505)** | 7.7 | 7.0 | **+0.7 (cancels)** |
| 1.50 (1536) | −10.5 | 44 % | 1.18 (1212) | 6.2 | 10.5 | −4.3 (flare) |

The near-cancellation at kP ≈ 1.0–1.1 is the point: **raising kP does not just add authority, it
buys back most of the overshoot that the higher KI creates.** Noise cost is small in practice —
added airflow jitter is `kP × sd(ε)` = 1.0 × 0.8 = 0.8 points, which lands in quadrature on an
already-2.2-point sd(air) (+6 %) and takes sd(RPM) from ~19 to ~21.5.

Caveats: **Ku was not identified** (no sustained oscillation in the source log), so a 3–5× kP
increase is unbounded against the stability margin — step it and re-run
[emu-black-idle-pid-gain](../skills/emu-black-idle-pid-gain/SKILL.md) on the next log. And note
`idleAirFlowIntegralLimitMin` **cannot** be clamped tighter than the total output while the base
carries a large margin: at convergence ε → 0 so P → 0 and the steady-state correction is *all*
integral — clamping I above the margin means idling high by `(margin − |I_limit|) / 0.079` rpm.

**Do not "fix" this by flattening the hot end of `idleActiveAirflow`.** The base excess is
deliberate: it is sized for a **hot-coolant / cold-oil** idle, which shares a CLT cell with
hot-coolant / hot-oil and therefore cannot be separated on the base table's own axis. See
[oil_temp_vs_coolant_airflow_reference.md](oil_temp_vs_coolant_airflow_reference.md) — the
correct home for that term is an oil-temperature-indexed custom correction, and the base must
stay tall until that sensor exists because the custom correction is ACTIVE-only. The over-air
also buys real protection: in this log a clutch-drop catch from **454 rpm** recovered past 1000 rpm
in 0.45 s, because base airflow was already ~49 % and the ignition PID had its full +17° reserve —
there was no throttle lag to wait through.

---

## Related documents

- [cammed_idle_instability.md](cammed_idle_instability.md) — full dilution/combustion physics (P1)
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — two-PID architecture + windup fix (P2)
- [idle_rpm_cov_stability.md](../ai-analysis-skills/idle_rpm_cov_stability.md) — RPM-CoV metric and method (P4)
- [idle_stall.md](idle_stall.md) — symptom-first stall decision trees (§A–§H)
- [return_to_idle_bog.md](return_to_idle_bog.md) — consolidated return-to-idle entry point
- [engine_start.md](engine_start.md) — cold-start, cranking, ASE, idle-timing-by-fuel table
- [throttle_feel.md](throttle_feel.md) — DBW characteristic, blend point, tip-in/parachute feel
- [supra/notes/airflow_actuator.md](../supra/notes/airflow_actuator.md) — **live** tables, actuator range, rescale rules
