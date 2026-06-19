# Cranking and cold-start

Getting the engine lit and through the first 5–10 seconds. **Steady-idle table mechanics
(actuator range, idle target/ref, active & armed airflow, custom/fan correction, blend point,
airflow PID, idle ignition) now live in [idle.md](idle.md)** — this note covers only what is
unique to cranking and the cold-start transition. The two are a pair: cranking pre-positions the
throttle so the handoff *into* the idle system is stepless.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`idle_session_05242026.md`](../supra/notes/idle_session_05242026.md),
> [`airflow_actuator.md`](../supra/notes/airflow_actuator.md), and [`my_car.md`](../supra/notes/my_car.md).

## Migration from v2

- The idle system changed significantly from v2 to v3. Most settings will need to be redefined.
- Import your v2 setup, then run the throttle body self-learn.
- Next, override the DBW duty cycle and note the throttle angle vs. DC relationship. This is used
  for both cranking and idle maps.
- v3 flips the primary/secondary actuator roles: **airflow PID is the primary RPM controller**,
  ignition timing is fast-path fine-tuning only. This is the opposite of v2. (Full architecture:
  [idle.md → P2](idle.md), [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md).)

## Cranking

- Target roughly 60–80 kPa MAP during cranking. A cold engine benefits from lower MAP (more
  vacuum) to reduce the fuel boiling point and aid vaporization; a hot engine relies on heat to do
  the same job.
- With extended-duration cams you will have a harder time developing MAP during cranking. Don't
  restrict the throttle arbitrarily to help out — defer to the airflow targets.
- Run more cranking enrichment cold than hot (cold needs a large positive enrichment for
  wall-film, hot needs only a small one). The cranking fuel enrichment bridges "engine spinning
  slowly with poor mixture formation" to "engine running and metering its own charge" — it pays
  the wall-film tax until surfaces warm up. It is **NOT** compensating for air starvation. See the
  build's working doc for this car's cranking enrichment values.

### Cranking-airflow handoff (the one airflow fact that belongs here)

`idleCrankingDC` is an independent open-loop table active **below 400 rpm** (`crankingThreshold`);
the active airflow table only applies once RPM crosses 400. They are separate control paths with a
hard handoff. Pre-position the throttle during cranking so the handoff is **stepless**.

**Units — confirmed on fw v59 (06-13 log): `idleCrankingDC` is an airflow %, not a duty cycle.**
The EMU UI titles it "Cranking airflow [%]"; it decodes ubyte ×0.5 and shows up *directly* in the
`Idle air %` log channel during cranking (raw `74` → 37.0% = the 37.5% the plate held at catch on
the hot restart). So it is the **same unit as the active airflow table** — the handoff is a direct
airflow-% match, no DC back-calc needed. (The "DC" in the symbol name is historical from the
PWM-IAC era; ignore it. An earlier version of this note called it a duty cycle — that was wrong.)
You can still translate to TPS to sanity-check the plate angle:
`TPS% = idleDBWTargetMin + airflow%/100 × (idleDBWTargetMax − idleDBWTargetMin)`.

Set each CLT bin to the **active-airflow % at the RPM you actually catch into — the idle target
*plus* the afterstart RPM increase** (the engine fires into the *elevated* afterstart state, not
steady idle; the active table is indexed by idle **target**). Cold bins → cold target + larger
afterstart bump (top of the active range, e.g. 1500 rpm); hot bins → hot target + its smaller bump.
Add a small margin so the first idle correction is a gentle **pull-down** (the stable direction).
Full method and the manifold-time-constant rationale: [idle.md → Cranking airflow / P5](idle.md).

> ⚠️ **The margin is not free — it is held open-loop and becomes the flare setpoint.** The cranking
> airflow does **not** dump to a lower value when the engine catches: the idle PID is gated off for
> `idleControlAfterstartDelay` after catch (~480 ms at delay=5), so the cranking airflow % is
> **held through the entire catch and flare** with no closed-loop trim. On the 06-13 hot restart the
> 37.5% cranking airflow was held flat from 228→1602 rpm and flared the engine to 1728 before the
> PID engaged. An over-generous *hot* cranking bin doesn't just seed the idle — it *is* the airflow
> the engine flares on. See **[Hot-restart flare → sag](#hot-restart-flare--sag-root-cause--levers)**.

## Establishing Sync Quickly

- EMU has a setting to infer position from the cam sensor state (high or low) when it first
  encounters the missing tooth gap, which you can also define.
- A smaller missing-tooth gap threshold is more aggressive and has less noise rejection. 90% might
  work here; 100% is the default.
- Set up the sensors correctly first — scope the signal during cranking and assess noise. If the
  sensors are shielded and close to the wheel, skipping the noise filter is reasonable; it will
  give faster sync and eliminate the filter's processing delay. The filter is most likely a rolling
  average, so it needs to fill its buffer before it can function.
- Check the cam sensitivity table — you can plot VR sensor voltage vs. RPM.

## Afterstart Enrichment (ASE)

> **Rule: ASE is not the post-start RPM lever.** A flare, sag, or stumble in the first seconds is
> an airflow/timing problem (see [Hot-restart flare → sag](#hot-restart-flare--sag-root-cause--levers)).
> ASE only changes mixture, and the restart is open-loop (no wideband for ~25–33 s), so it can't even
> be measured during the event. Touch fuel only if the open-loop mixture proxy actually shows lean.

- Rapid throttle closure from the (higher) cranking TPS to the (lower) idle TPS creates a large
  air deficit that ASE alone cannot compensate.
- The fix is not to reduce ASE — it is to prevent the throttle from slamming shut post-start. Use
  a higher idle RPM target for 5–10 seconds after start, then taper down. (Stall version of this
  failure: [idle_stall.md §B](idle_stall.md).)
- Configure ASE as a 2D table: coolant temperature vs. post-start engine **revolutions** (not just
  time). The revolution axis correlates better to wall-wetting decay rate.
- Shape: large positive enrichment at cold/low-revolution cells, decaying to zero as the engine
  warms and the revolution count climbs. See the build's working doc for this car's ASE values.

## Hot-restart flare → sag (root cause + levers)

> **Lesson (06-13): a post-start RPM "stumble/slight misfire" is an air/timing flare-then-undershoot
> until proven otherwise — not a fueling problem. Root-cause the air/timing path *first*; do not
> reach for ASE.** (This session initially proposed adding ASE to a hot-restart sag; the data
> refuted it. The fix is upstream of fuel.)

Sequence on a hot key-off restart (06-13 log, CLT ~92–96 °C):

1. **Catch → flare.** Engine fires into the *held* open-loop cranking airflow (37.5%, more than a
   hot engine needs) with ignition **locked** at the afterstart angle (24°, ~5° above the ~19° warm
   idle runs) and the airflow PID gated off for `idleControlAfterstartDelay`. RPM flares to **1728**
   over a ~1289 target.
2. **Flare → undershoot.** The PID engages and correctly *cuts* air, but the only idle-air actuator
   is the DBW plate, which lags **~750–840 ms** (no stepper IAC). Its corrective air arrives ~0.88 s
   late — *after* RPM has already collapsed to **669**. With `idleAirFlowKD`=0 there is no
   derivative brake, so it is one large under-damped swing before it settles.

**The whole swing is seeded by the flare** — kill the flare and the undershoot + hunt shrink with
it. Fix the airflow the engine catches on, not the aftermath.

### Levers, priority order (all CLT-indexed or afterstart-only → won't disturb steady idle)

1. **`idleCrankingDC` hot bins** — the airflow the engine flares on (held open-loop through catch;
   see [handoff](#cranking-airflow-handoff-the-one-airflow-fact-that-belongs-here)). Lower the hot
   bins to lower the flare directly. Keep enough for a crisp hot catch — trim moderately, re-log
   catch quality. **Biggest single lever; it sets the level.**
2. **`idleControlAfterstartDelay`** — how *long* the cranking airflow is held before the PID can
   trim it (5 ≈ 480 ms open-loop window). Lower it so the PID cuts *before* the flare peaks.
   Compounds with #1 (lower level, held shorter).
3. **`afterstartIgnitionLockTime` + `afterstartIgnRestoreRate`** — frees the *fast* lever
   (idle-ignition retard) to knock the flare down. The lock's harm is **at the flare** (controller
   wanted ~10° of retard but the lock pinned 24°). It is **NOT** harmful at the trough — there the
   locked angle was *more* advanced than the controller wanted, so unlocking there would retard
   timing and *deepen* the sag. Shorten both; the restore tail is part of the locked window (the
   controller doesn't regain authority until restore completes).
4. **`idleAirFlowKD`** (0 → small) — derivative damping on the residual swing.

### Why ASE is NOT the lever (open-loop caveat)

A hot restart runs **open-loop**: the wideband is invalid for **~25–33 s after every start**
(conservative heater warm-up — `Lambda 1` pins to 1.000, `Lambda is valid`=0), so there is no STFT
and AFR cannot be read during the event. Every fueling signal refuted a lean sag: injector PW
*rose* into the trough as airflow fell, ASE was flat while RPM collapsed (no enrichment-fade tell),
the trough ran richer than steady idle, and the **cold** start — which idles fine — carries a far
larger fuel stack (ASE ~25–30% + warmup) at the same MAP. There is no mechanism by which a ~13% hot
stack is "too lean" when ~35% cold is stable. If anything, hot ASE should **stay or trim down**
(hot, low-wall-film engine needs minimal enrichment — Bosch). This restates the [ASE rule](#afterstart-enrichment-ase)
above.

### Secondary: the cooling fan as a load disturbance

On a hot restart the fan re-engages at `catch + coolantFanTimeToEngage` (~750 ms) — landing
mid-recovery and adding an alternator load step (≈ −0.5 V battery, ~50–100 rpm of extra sag depth).
Its feedforward `idleCoolantFanCorr` (+13%) is applied as a **DBW DC offset** (motor-drive level —
it does *not* show in `Idle air %`/`DBW target`) and was effectively absent during the afterstart
transient. Curing the flare shrinks the swing the fan can disturb, so treat the fan as secondary;
confirm whether `coolantFanTimeToEngage` is a pre-activation air lead or a plain engage delay before
changing it. (See [outputs.md](outputs.md) / [idle.md](idle.md) for the fan idle-up feedforward.)

### Parameter scalings (fw v59 — decoded + empirically anchored)

| Symbol | Raw → display | Note |
|--------|---------------|------|
| `idleCrankingDC` | ubyte ×0.5 = **airflow %** | UI "Cranking airflow [%]"; `cltBins4` = 0/33/67/100 °C |
| `idleControlAfterstartDelay` | 5 ≈ **480 ms** open-loop window | empirical: catch → `Idle control active` 0→1 |
| `afterstartIgnitionLockAngle` | sbyte ×0.5 = ° | 48 → **24.0°** |
| `afterstartIgnitionLockTime` | **×0.04 s/count** | 100 → 4.0 s flat (+ restore tail ≈ 5.5 s total locked) |
| `afterstartIgnRestoreRate` | **×0.125 °/rev per count** | 2 → 0.25 °/rev (runs *after* the flat time) |
| `coolantFanTimeToEngage` | ms | 750 → fan re-engages 0.75 s after catch |
| `idleCoolantFanCorr` | direct % airflow, applied as **DBW DC offset** | 13 → +13% |

## Idle ignition by fuel and cam (reference table)

Idle base advance is set **below MBT** to leave the controller recovery authority (reserve of
torque — Banish/Hartman). A diluted charge (cams, ethanol) burns slowly, so peak pressure needs
the burn to start earlier; cammed/ethanol builds therefore idle with more advance. Full setup
(target table, swing limits, flat-base rule) is in [idle.md → Idle ignition](idle.md); this is the
starting-range reference:

| Fuel | Cams | Idle timing range |
|------|------|-------------------|
| Pump gas | Stock | 10–12° |
| Pump gas | Cammed | 13–16° |
| Ethanol | Stock | 13–16° |
| Ethanol | Cammed | 16–19° |
| Ethanol | Big cams | 19–22° |

## Related notes

- [idle.md](idle.md) — steady-idle settings + principles hub (airflow PID, KD, DBW lag, idle ignition)
- [ignition.md](ignition.md) / [timing.md](timing.md) — afterstart ignition lock behavior
- [dbw.md](dbw.md) — DBW airflow transport lag (~750 ms), the reason air is the slow recovery lever
- [idle_stall.md §B](idle_stall.md) — cold-start / post-start stall decision tree
- [cammed_idle_instability.md](cammed_idle_instability.md) — why a diluted idle charge is unstable
- [supra/notes/airflow_actuator.md](../supra/notes/airflow_actuator.md) — live cranking/active airflow values
