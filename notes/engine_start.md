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

`idleCrankingDC` is an independent open-loop table active in the Cranking state and held through the
afterstart delay; the active airflow table only applies once the ECU has left Cranking
(`crankingThreshold`) and the delay has run. They are separate control paths with a hard handoff. Pre-position the throttle during cranking so the handoff is **stepless**.

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

### Where to put `crankingThreshold` — designed meaning: "the engine has started" (revised 2026-09-29)

**Rule (Will, 2026-09-29):** `crankingThreshold` defines the transition to the Afterstart state, so its
designed meaning is *the engine has started*. Set it where the engine is running on its own, not where
a cranking pulse can reach. Don't lengthen `idleControlAfterstartDelay` or bend another parameter to
cover an early exit ([[feedback-designed-behavior-not-bandaids]]).

**Evidence (post-TB-clean, `allchannels_smoothclt.csv`, cold start CLT 26, threshold 500):** the cranking
tables carried the engine to ~300 rpm (logged). The exit fired on a single ≥500 pulse (586 logged), and
fuel switched there from the cranking dose to VE × ASE × warmup. The engine then **bogged at 455–586 rpm
for ~0.5 s** with vbat still starter-depressed. 0.32 s into the bog (`idleControlAfterstartDelay`) the
idle controller went ACTIVE against 1677 (error −1146), and both PIDs wound up. The engine pulled itself
out at 85.20: that was 0.12–0.16 s after the plate first moved, inside the ~750 ms air lag, so not the
PID's air (inference). The still-winding PID (+23 air-%) then drove the overshoot to 1815 and the trough
to 1155. Phase table: [log note §1](../supra/notes/log_2026-09-29_allchannels_smoothclt.md). `Engine runtime` counts from the exit, so the ASE and afterstart-RPM-increase
runtime axes also start there. Full analysis: [log note §1d](../supra/notes/log_2026-09-29_allchannels_smoothclt.md).

**Setting chosen for the Supra: 750 rpm, afterstart delay 4 (Will, 2026-09-29; not yet in an XML export —
re-read the live values from the newest export before relying on them).** Rule (Will): the threshold sits
**above everything the engine does before it has caught and below the lowest running stumble you can
expect.** In the 09-29 log that window is 586 (highest pre-catch RPM: cranking + bog) to 832 (lowest
running RPM after the start, a return-to-idle at 455.8 s). 750 leaves 164 above and 82 below. 1025 was
considered and rejected: hot idle targets 1025 and dips below it all the time (388 samples < 1000 in this
log), and whether the ECU re-enters Cranking on a sustained dip below the threshold is unverified. The
only evidence is 455 < 500 for ~0.3 s after the 09-29 exit without re-entry.
On this start a 750 exit lands at 85.255 s, 4.5 revs after the old exit. RPM crosses the decaying
afterstart target 0.39 s later (3.7 counts at ≈0.107 s/count). Delay 3 → ACTIVE at 1507 vs 1678 (−171);
**delay 4 → 1719 vs 1672 (+47)**; delay 5 → 1796 vs 1665 (+131, at the peak → trough risk). Lock time ≥
delay: 11 (0.44 s). From 750 up, the run-up stays on the 24° lock + ASE, as it did on this start.

**What `idleControlAfterstartDelay` is for (Will, 2026-09-29):** it covers the run-up from the cranking
threshold to the target RPM, so the idle PIDs start at target instead of chasing a climbing engine. Set it
to the measured time from the exit to the moment RPM crosses the afterstart-elevated `Idle target` (the
target the PIDs actually use). 09-29, CLT 26, 750 exit: **0.39 s** (85.255 → 85.647 s, 1674 rpm). To the
1500 base target it's 0.32 s. At ≈0.107 s/count (3 = 0.32 s measured, ±1 sample) that is 3.7 counts → 4.
The PID air added from 85.04 on the real start reached the cylinders only after ~0.75 s (≈85.8), so it did
not drive this 750 → target climb; the interval reflects the engine on 24° lock + ASE. It is one cold start:
hot and colder starts will climb at different rates, so re-measure on each new start type.
**Measured across start types (2026-10-02, Supra):** exit-to-target is ≈ 1.5 s cold (CLT 29, hover) and ≈ 0.1–0.25 s
warm/hot (CLT 82–98). The flare peak comes ≈ 0.65 s after exit. A 1.5 s hold engaged ACTIVE cleanly cold. At CLT 82 (held airflow
below the steady need) it engaged on the falling edge (≈ 800 rpm/s): spark railed at the max torque angle, trough 615,
late-air overshoot 1430. The flare pumps the manifold down, and its lagged refill carries the decay past the held plate's
equilibrium. Both hot cases (CLT 96–98) had the A/C clutch engage during the hold with no A/C feed-forward (the custom
airflow correction applies only in ACTIVE), so the hot behaviour of the long hold is untested.
Evidence: `supra/notes/log_2026-10-02_restartbounce.md`.

**What the design requires once the threshold marks a real start:**
- **The cranking tables must carry the engine up to the threshold.** Fuel: at today's exit, running
  fuel / cranking fuel = ×1.36 per kPa of MAP (net PW 1.864 ms at MAP 88, cranking corr +4 % → 2.395 ms at
  MAP 83, ASE +40 %). So the dose steps unless the `crankingCorrTbl` rev tail near the exit (~5–7 revs past
  the old exit) matches ASE runtime-0, or ASE runtime-0 comes down to meet the tail. Which one is a mixture
  question; the WBO is blind until ~30–40 s. Spark: `crankingIgnAnlge` now runs the hover and run-up.
  Air: `idleCrankingDC` is now the run-up air.
- **Re-entry below the threshold is unverified, so keep the threshold below running dips.** `engineStallRevs`
  (a direct RPM, UI max 250, not an adder) declares a stall. Whether a running engine that dips below
  `crankingThreshold` but stays above the stall limit re-enters Cranking has only one data point: 455 rpm
  < 500 for ~0.3 s right after the 09-29 exit, no re-entry. Don't rely on it for sustained dips.
- **`engineStallRevs` must sit below the lowest cranking speed** (Will, 2026-09-29). Otherwise a normal crank
  reads as a stall. Cranking speed on 09-29 was 158–222 rpm at 10.5–11 V, and a weak battery cranks slower
  (175 rpm at 10.2 V, 07-29). The engine has recovered from dips to ~580 rpm, so the stall limit only needs
  to catch a real stop. Will lowered it below 60 on 2026-09-29 (new value not recorded here) to shorten the
  time from starter engagement to first fuel: below the stall limit the ECU treats the engine as stopped.
  Effect not yet measured; the 09-29 crank start is inside a `Data changing` gap.
- **Ignition lock ≤ afterstart delay, fast restore.** With the exit at running speed the lock no longer
  protects a hover. Held longer, it pins the lock angle through the flare while the airflow PID reads the
  undelivered ignition demand.

*Superseded (kept for the record):* the 2026-08-24 verdict below said to leave the threshold at 400. Its
reason 2 (holding cranking timing and air through the pull-away starves the engine) is now a sizing
requirement on the cranking tables, not a reason to exit early. Its reason 4 (latched exit) is explained
by `engineStallRevs`.

#### 2026-08-24 analysis (superseded verdict)

`crankingThreshold` is a **plain RPM comparison**, and it gates four things at once: cranking fuel
(`crankingCorrTbl`) vs VE + ASE, `crankingIgnAnlge` vs `afterstartIgnitionLockAngle`, `idleCrankingDC`
vs the idle regime, and `crankingLambdaTarget` vs the lambda table. Moving it moves all four together.

**Verdict: leave it where it is. It is not the lever for a bad start.** Four reasons, all checked
against `cranking_channels_recent_run.csv` (2026-08-24) and the 2026-08-22 XML:

1. **RPM *is* the all-cylinders-fired detector** (Will, 2026-08-24 — the earlier framing here was
   wrong to call it merely an RPM compare). Rise above cranking speed is the physical evidence that
   cylinders are contributing, so choosing the threshold *is* choosing how much combustion evidence
   you demand before committing. On this engine cranking speed is 183–237 rpm, so 400 rpm already
   requires ~1.7–2.2× cranking speed = sustained multi-cylinder firing; a single fire gives a blip.
2. **Demanding more evidence costs timing and air during the pull-away.** The six sequential
   first-fires span two crank revolutions — ~0.6 s at 200 rpm. Holding `crankingIgnAnlge` (13°) and
   `idleCrankingDC` through that window starves the engine of both exactly when it needs them.
3. **Lowering it widens an already-extrapolated band.** `rpmBins` (the VE-table RPM axis) starts at
   **500 rpm**. A 400 rpm threshold is *already* below the bottom row, so 400–500 rpm runs on a
   clamped VE row. Drop the threshold to 300 and that uncalibrated band doubles. `crankingCorrTbl`'s
   rev-indexed schedule exists precisely because the VE model is not valid at 200–400 rpm — exiting
   early hands a marginal start to a model that was never calibrated there, on a build with a
   documented cold-plug fouling failure ([[project-supra-ignition-hardware]]).
4. **There is no chatter argument in either direction — the exit is latched.** Measured: RPM fell
   back to 391/386 (below the 400 threshold) from t 4.88 to 5.20 and the ECU did **not** re-enter
   cranking — `Cranking correction` stayed 0 and `Idle state` went 5 → 2 through the dip. So you do
   not need headroom above the post-catch sag.

The one honest argument for *raising* it is aligning the running-fuel handoff with `rpmBins[0]` = 500
so the VE model is on its calibrated axis at handoff. It loses to reason 2: on a healthy catch the
engine crosses 400→500 rpm in ~0.1 s, and buying that costs a longer hold of cranking timing and air.

### The binding constraint: the threshold must sit *below* the cranking-air RPM ceiling

> **2026-09-29:** with the threshold now meaning "started" (750 on the Supra, set 2026-09-29), this constraint is a
> sizing requirement on all three cranking tables (air, fuel, spark), not a reason to keep the threshold
> low. The 08-24 plateau below was on a fouled TB (pre-09-19 airflow frame).

**`crankingThreshold` must be below the RPM that `idleCrankingDC` alone can sustain — otherwise the
exit condition is unreachable.** The idle regime's air is gated *behind* the exit, so if the engine
cannot reach the threshold on cranking air, you have gated the escape behind the escape.

Measured on the 2026-08-24 log: on 36 % cranking airflow the engine held a **stable plateau at
386–425 rpm for 0.56 s** (t 4.72–5.28) and topped out at **425**. It broke out only when the idle
PID's air arrived. A 450 rpm threshold sits *above* that measured ceiling — it would have held the
engine in cranking on the same 36 % air with no path out. **Do not raise the threshold without first
raising `idleCrankingDC` at that CLT bin so the ceiling moves above the new threshold.** Order:
airflow first, threshold second, never the reverse.

### Why 36 % airflow sustains 425 rpm here and flared 1728 rpm on 06-13 — the low-branch trap

The same cranking airflow can sag *or* flare because a fixed plate position has **two stable
equilibria**, and which one you land on depends on how hard the engine catches. Airflow % is a plate
*position*, not a mass flow, and the mass it passes collapses as MAP rises toward barometric:

| branch | RPM | MAP | throttle ΔP | air the plate passes |
|---|---|---|---|---|
| low | ~400 | ~83 kPa | small | ≈4.5 g/s — enough to idle at 400, not to climb |
| high | ~1330 | ~40 kPa | large (near-choked) | ≈8.4 g/s |

(3.0 L, VE ≈0.5 / 0.6, ρ from MAP·(RT)⁻¹.) Land on the low branch and the loop is
self-holding — low RPM → high MAP → less mass through the plate → stays at low RPM. It needs a
*kick* in plate area to jump branches, which is exactly what the PID supplied.

**Consequence for calibration:** there is no single `idleCrankingDC` value that is simultaneously
right for both branches — 37.5 % flared 06-13 to 1728 and sagged 08-24 to 386. So do **not** chase a
perfect cranking airflow. Get the closed loop authority *early* instead (short
`idleControlAfterstartDelay`), so whichever branch you land on gets corrected before it sets.

**What is actually wrong is the handoff, not its trigger point.** At catch three things step and one
is late (same log, catch at t 4.72):

| At catch | Commanded | Observed |
|---|---|---|
| Ignition | 13° → 24 ° (`afterstartIgnitionLockAngle` ×0.5), held `afterstartIgnitionLockTime` ×0.04 = 1.0 s | steps immediately ✓ |
| Fuel | lean-of-VE cranking dose → VE + `aseTbl` (**+20 %** at ~70 °C, runtime 0) + `warmupTbl` (~+3.5 %) | `Injectors PW` 2.47 → 3.24 ms ✓ |
| Airflow | idle regime | **held at cranking 37.5 % for another 0.28 s**, then jumps to 62 % |

`Idle state` = 5 for exactly that 0.28 s window, then 2 — i.e. `idleControlAfterstartDelay` = 3 at
**≈93 ms/count**, consistent with the ~480 ms measured at delay 5.

> **Correction (2026-08-24):** an earlier revision of this section read the 36 → 62 % airflow jump as
> a *table* mismatch at the handoff. It is not. `idleActiveAirflow` at CLT ≈70 °C interpolated to the
> afterstart target (idle target 1200 + `idleAfterstartRPMincrease` ≈131 → ~1331 rpm) is **≈35.6 %** —
> which matches the 36–37.5 % cranking value almost exactly, so the "stepless handoff" rule is
> *already* satisfied at the base-table level. The extra ~26 points are **PID output**: the loop
> engaged at t 5.00, saw RPM 386 against a ~1330 target, and commanded air accordingly. The lever is
> therefore the *delay* and the PID's authority window, not the cranking airflow level.

Sequence, then: catch → 0.32 s of gated PID on the low branch (386–425 rpm, ~950 rpm under target) →
PID engages and commands +26 points → DBW plate + manifold deliver it ~0.2 s later (t ≈5.20) → engine
jumps to the high branch and overshoots to **1810** with the integral wound up, the plate lagging, and
`afterstartIgnitionLockAngle` pinning ignition at 24° so the *fast* retard lever is unavailable.

Consequence worth noting: because the engine could not pull away from the threshold, it spent ~0.5 s
between 386 and 425 rpm — half a second on a VE row it was never calibrated on. Fix the airflow
handoff and that window collapses to ~0.1 s on its own. Levers in priority order:
**[Hot-restart flare → sag](#hot-restart-flare--sag-root-cause--levers)**.

> **Log-channel note (this build, 2026-08-24):** `Idle state` **3 = CRANKING**, **5 = AFTERSTART
> DELAY** (held for `idleControlAfterstartDelay`), **2 = ACTIVE**. This resolves the
> "AFTERSTART DELAY *or* CRANKING — verify per build" ambiguity in the `emu-black-log` enum table;
> state 5 is *not* cycling idle on this build.

> **Unverified:** this crank layout has no `CLT`, `Lambda`, or `Battery voltage` channel, so the fuel
> side above is tune arithmetic, not measurement. It closes consistently (VE ≈64.8 % at MAP 83 on the
> clamped 500-rpm row × +24 % ≈ 1.71 ms effective, + ~1.5 ms cranking-voltage deadtime ≈ 3.2 ms vs
> 3.24 ms logged) but that is corroboration, not proof. Add those three channels.

## Cranking fuel equation (fw v59 — decoded 2026-07-29, log-verified)

The cranking dose is **not** a standalone PW table. Per EMU help ([Enginestart](../docs/emu-black-help/Enginestart.md))
and confirmed by per-sample decomposition of the 07-29 crank log:

```
PW = deadtime(vbatt, ΔP)
   + [VE-equation base dose, λ target = crankingLambdaTarget]   ← main VE table, NOT the 3D λ table
   × (1 + crankingCorrTbl%)     ← "Cranking fuel", CLT × crank-revolutions, FF-blended
   × (1 + TPSScaleTbl%)         ← anti-flood pedal scale
   × fprDeltaCorrection          ← fuel-pressure compensation
```

- **`crankingCorrTbl` / `crankingCorrTbl2`** (u12, 8×5, 1%/count): X = `cltBinsCranking`
  (sword, °C: 0/17/34/51/69/86/103/120), Y = `crankRevCntBins` (ubyte revs: 1/3/7/13/20).
  0% = no change, 100% = double dose. FF blend via `tblsFFCrankingBlend` (ubyte ×0.5%,
  9 bins over 0–100% ethanol; E25 → 83% table 1).
- **`TPSScaleTbl`** (6×1 at `tpsCrankingBins` ×0.1 %, cells 1 %/count; read the current values
  from the export — the Supra's changed between the June and 09-15 exports). −100% = designed
  clear-flood (zero fuel). Corollary: *any* pedal input while cranking cuts the dose — never crank
  with your foot in it unless you're deliberately drying the cylinders.
  **It also bites with no pedal at all (found 2026-10-02).** On DBW the idle controller opens the
  throttle to the cranking airflow position, and the table reads that TPS. With the first breakpoint
  at TPS 0 and a non-zero second bin, every cranking position lands on the cut slope. Supra 10-02:
  TPS 5.4 (cold) → −16 %, TPS 2.9–3.1 (hot) → −9 %, the whole crank, with the pedal untouched. The
  logged `Cranking correction` is the product, (1 + table)(1 + TPSScaleTbl) − 1 — verified on three
  starts. Designed meaning: the scale is 0 up to just above the highest cranking-airflow TPS
  (`idleCrankingDC` coldest bin through the DBW idle window), then cuts. Re-scale `tpsCrankingBins`.
  **Indexed by TPS, not PPS** (log-proven 07-29: PPS 100 / TPS 69.5 → −77%, not −100%). On a
  DBW characteristic that caps WOT below 90% throttle (e.g. a boost-TPS strategy), **the −100%
  bin is unreachable from the pedal** and clear-flood silently keeps injecting. Re-anchor the
  −100% bin below the achievable WOT-crank TPS.
- **`fprDeltaCorrection`** (12 bins at `fprDelta` 70→650 kPa, ×0.01): the table is exactly
  √(400/ΔP) normalized at the 400 kPa base — the orifice equation. **It clamps at 2.39× below
  70 kPa ΔP**, so compensation cannot rescue a rail that hasn't filled yet; the first revs on an
  empty rail deliver ~nothing no matter what PW is commanded.
- **`crankingLambdaTarget`** (ubyte ×0.01, this build 1.00): replaces the λ-target table while in
  Cranking state. Lowering it enriches every cranking cell uniformly (0.90 ≈ +11%).
- `injectorsSize` (word, cc/min) is flow **at the 400 kPa base ΔP** (1230 = ID1050X 1065@3 bar ✓).
- `primePulseTable` (ubyte 8×1 vs CLT): extra simultaneous dose at first trigger impulses;
  **invisible on the Injector PW channel** (scope only). `engineStartDelay` (ubyte 8×1, revs vs
  CLT) and `startDelay` exist as XML symbols, but **Will reports no start-delay setting in the
  EMU software — treat them as non-functional/hidden, not a usable lever** (2026-07-29).

### The VE basis is the silent multiplier on every cranking % (2026-08-06)

> **Will, 2026-09-30:** the VE table's RPM axis stops at 500 rpm and clamps. Cranking reads the
> high-MAP (WOT) end of that row, which does not reflect cranking fuel demand, so every cranking %
> is a correction to that cell. Read the VE cells actually looked up (500 rpm row at cranking MAP;
> the 500 rpm row and the next row up at the falling MAP through the run-up) before judging any cranking
> cell. This is now a standing rule in the repo `AGENTS.md`/`CLAUDE.md`.

**Option: move B into a sub-500 VE row (worked 2026-09-30, Supra 09-29 log).** The VE table's 20 rows are
fixed, but `rpmBins` is an editable scale: an even 500 → 7000 on the 09-19 export, and it can start at 200
(e.g. 200 → 7000) or use any spacing. Re-scaling moves every bin, so the VE values get re-mapped onto the new
bins. With a bin at ~200 rpm holding B × (the VE at 500 rpm), the lookup below 500 blends the two. With B 0.79 and the 09-29 cells (VE 63 at
cranking MAP): 200 rpm −21 %, 303 −14 %, 381 −8 %, bog 455–586 −3…0 %, ≥ 500 unchanged.
- **Paired with the cranking table lifted ×1/B:** the cranking-speed dose is unchanged, and the
  speed-dependent error now fades with RPM through the bog/run-up by itself. The cranking table then
  carries only the wall-film term (CLT × rev) and can decay monotonically to ASE runtime-0 at the exit:
  no rising tail.
- **Without the ×1/B:** B is applied twice, so cranking runs 21 % lean and first fires 8–14 % lean.
- **Limit:** B 0.79 compares the 500 rpm / ~90 kPa cell with the 1184 rpm / 35 kPa idle cell. True VE at
  200 rpm / 90 kPa is unmeasured, and every cranking % rescales with that row.
- **Rejected (Will, 2026-09-30):** the 500 rpm bin is Will's deliberate bog-rescue row, and it has worked. On 09-29
  the 455–586 bog ran on VE 59.3–61.7 at MAP 77–83 and pulled out. An even 200 → 7000 re-scale moves the
  low bins to 200 and ~558, so the bog would blend with the cranking-speed bin (≈ −8 % at 455 rpm). B stays in
  the cranking table (CLT × rev), which can't touch a running bog.

Because the cranking dose runs **through** the main VE table, the cranking correction's
percentages are enrichment over *the VE table's belief about trapped air*, not over real
stoich. Define

```
B(CLT) = VE_true / VE_table_at_the_cranking_cell
λ_liquid_true = B / (1 + corr)      →      (1 + corr) = B × (1 + E over true stoich)
```

**If B < 1, a cell reading 0 % is not "no enrichment" — it is an overfuel of (1/B − 1).**
Cranking clamps to the *lowest* RPM row of `veTable`/`veTable2`, which is the one row a
wideband can never autotune (WBO invalid ~25–33 s after start — [[supra-wbo-blind-after-start]]),
so it is an extrapolation corner by construction. Every build should expect B ≠ 1 there and
measure it rather than assume.

Why VE_true < VE_table at cranking speed, both terms real:
- **Geometric/reversion (temperature-independent).** Late IVC + no intake ram at ~180 rpm ⇒ the
  rising piston pushes charge back out the open intake valve. Trapped-volume geometry alone
  gives ≈0.80 of ideal on a late-IVC cam; low-speed backflow takes more.
- **Charge heating (grows with CLT).** The ECU sizes air density from IAT; on a hot restart the
  ports and valves downstream of that sensor heat the charge further. Absent on a cold start,
  worst on a hot restart — so B should be scheduled down with coolant temp, not held flat.

**Storage note: the cranking correction tables accept negative cells** even though their storage
is named `u12` — EMU writes them sign+magnitude (`-7 -D -10`). Verified 2026-08-06 against an
EMU-written export. So the basis correction can live in the table itself; there is no need to
push it into `crankingLambdaTarget` (which would work — dose ∝ 1/λ_target — but disguises a
calibration error as a lean λ target and will be misread later).

**Do not re-anchor U to the old working tables when rebuilding.** Back-solving the evaporated
fraction from tables that already sat on a wrong basis reproduces those tables exactly — the B
term cancels and the "rebuild" is the original. This is the same circularity retracted in
[crank_fail_0729.md](../supra/notes/crank_fail_0729.md); it bites a second time here. Choose
E₁ and N from the wall-film physics and *state them as chosen parameters*.

Rebuild form used 2026-08-06 (car-specific values + method:
[supra/notes/cranking_ve_basis.md](../supra/notes/cranking_ve_basis.md)):

```
corr(CLT, rev) = B(CLT) × [1 + E₁(CLT) · e^−(rev−1)/N(CLT)] − 1
```
E₁ = rev-1 enrichment over *true* stoich (wall-film tax), N = film-charging revs. The ethanol
table carries only the **vaporization** penalty — the stoich difference between E0 and E100 is
already in the base fuel equation, so table 2 > table 1 is not double-counting AFR.

**v2 → v3 relevance (hypothesis, unverified).** v3 computes cranking through the VE equation
(decoded above). If v2 fueled cranking from a standalone dose, the low-RPM VE row was simply
not in the cranking path before migration — which would make "cranking got worse after the v3
import" a basis-exposure story, not a lost setting. Confirm against v2 docs before relying on it.

### When the threshold means "started", the rev tail fuels a running engine (2026-09-29)

With `crankingThreshold` at the start point (750 on the Supra, set 2026-09-29) rather than just above
cranking speed, the late rows of `crankingCorrTbl` stop being "long crank, not catching" cells. They
fuel the hover and run-up of a catching engine. On the 09-29 cold start the old 500 exit landed around
rev 9–10 (`Cranking correction` +4 % at CLT 26, between the rev-7 and rev-13 rows). Measured (RPM integral, cross-checked
against the spark rate at 6 sparks/rev wasted-spark while cranking/hovering and 3/rev running): 3.3 revs
from the first post-gap crank sample to the old exit, then **5.9–6.2 revs from the old exit to 1000 rpm**
(4.0 hover, 2.0 run-up); 9.2–9.5 revs from 83.96 s to 1000, plus whatever turned inside the `Data changing`
gap before it. In the ECU's own rev count (the `crankingCorrTbl` Y axis, inverted from the logged
correction through the 09-22 table, blend 91.5 % table 1) the old exit sat at ≈10, and the count advanced
~5.5 while the crank turned ~3.0. So either the counter runs ~1.8× physical revs, or the live table differed
from the export (data was being changed right before the crank). A 750 exit (the Supra setting) comes 4.5 physical revs after the old exit: count ≈14.5 at 1:1, ≈18
at 1.8× (the 1000-rpm point would be ≈16 / ≈21, past the last bin). Unresolved.

The tail was built as `B(CLT) × [1 + film(rev)] − 1`. B, the VE-basis correction, belongs to cranking
speed, where the lookup clamps to the 500 rpm VE row and true VE is lower (late IVC, no ram). At
500–750 rpm and above the lookup is on real VE rows, so B no longer applies; the wall-film term still does. A
tail that goes negative (CLT 22/33: rev 13 = 0/−9 %, rev 20 = −7/−12 % in the 09-22 XML) is right for a
200 rpm crank and wrong for a 900 rpm run-up at the same rev count. The table can't see RPM, so the rev
axis has to carry the difference.

**Target: stepless fuel at the exit.** Cranking dose at the exit revolution ≈ running dose right after it
(VE eq × ASE runtime-0 × warmup). Measured at the 09-29 500-rpm exit: net PW 1.864 ms at MAP 88 (corr +4 %)
→ 2.395 ms at MAP 83 (ASE 40 %) = ×1.36 per kPa, i.e. ≈ +40 % cranking correction at CLT 26. That is
the dose this start ran through its hover and run-up. Step size at that exit: PW +16 %, net PW +28 %,
≈ +36 % per unit air. That is well inside the ~3:1 ignitable window, and Will judged it not severe (2026-09-30).
Continuity is a refinement here, not a fix. Whether +40 % is right, or ASE runtime-0 should
come down to meet a lower tail, is a mixture question the start can't answer: WBO invalid until 122.8 s,
first reading λ 0.73 vs 0.91 target (hints rich). Other CLT columns need their own starts. A hot catch
reaches the threshold in fewer revs and exits on earlier rows. With `crankRevCntBins` at 1/3/7/13/20, two
rows now span the whole run-up and slow catches pass rev 20 onto the clamped last row.

**Shape that follows if ASE stays (Supra proposal, 2026-09-29; the alternative is to keep the cranking table and lower ASE runtime-0 to meet it — undecided):** keep the cranking-speed rows (1/3/7). Set the exit
row (13 for a cold 750 exit, ~12–15 revs) equal to ASE runtime-0 per CLT and per table. The linear 7 → 13
rise then unwinds the cranking-speed VE-basis error as RPM climbs; in true-mixture terms enrichment still
decays, as the help file intends. Leave the last row (20) low: a crank that hasn't exited by then isn't
catching, and the rev axis can't tell that from a run-up. Warm/hot columns need their own exit revolution
(fewer revs). Values: [log note §1e](../supra/notes/log_2026-09-29_allchannels_smoothclt.md). Source:
[log note §1d](../supra/notes/log_2026-09-29_allchannels_smoothclt.md).

### The rev-axis exhaustion trap

`crankRevCntBins` counts from the first crank rotation **whether or not fuel is being
delivered**. If the rail is empty (or the pedal is down) for the first N revs, the rich early
rows of the cranking table are consumed injecting into an unfueled engine, and real fueling
starts on the decayed tail → lean no-start that "more cranking fuel" barely touches. With no
usable start-delay setting (see above), the only real fix is **making the key-on prime actually
pump** so the rail is full at rev 1; √ΔP compensation clamps at 2.39× (70 kPa) and cannot cover
an empty rail.

### Enrichment decay per revolution — the wall-film (Aquino x-τ) basis

Why cranking enrichment decays over *revolutions* (the `crankingCorrTbl` Y-axis), not seconds:
injected fuel doesn't all reach the cylinder — a fraction impacts the port/cylinder walls as a
liquid **film** ("puddle"), and only airflow past it carries part into the charge (Banish's τ model,
`corpus/engine_management_advanced_tuning.md` §transient fueling; **Aquino 1981, SAE 810494** — the
foundational first-order wall-film model: per-cycle impaction fraction *x* + evaporation time
constant τ). At the **first crank the walls are dry**, so a large fraction of every injection sticks
and never burns → a big rev-1 overfuel is needed just to vapor-charge the first fires. As cycles
accumulate the film fills toward its (temperature-set) equilibrium; less of each shot sticks; the
enrichment decays.

- **Revs is the physically correct axis** — the film charges per intake event = per cycle; time
  drifts with cranking speed. Grounds the repo's standing "ASE as revs, not time" rule (Heywood
  Ch.7 Mixture Preparation; Aquino).
- **Shape ≈ first-order (exponential)** from the rev-1 peak toward the warm-running requirement;
  `crankRevCntBins` [1,3,7,13,20] matches the ~10–20-cycle film-filling timescale.
- **CLT axis does real work:** colder = bigger film + slower evaporation → higher peak AND a longer
  (more-revs) decay; warmer = small film, fast collapse. Hot cells (112 °F ambient) should peak
  lower and reach ~0 enrichment by ~rev 7–13, not drag to 20.
- **Ethanol nuance (flex):** ethanol's high heat of vaporization makes the film stickier/slower to
  clear cold → the ethanol side wants a *slower* cold rev-decay (ethanol wall-wetting paper, J.
  Zhejiang Univ. A `jzus.A1200068`). `crankingCorrTbl2` decaying slower than Tbl1 at cold cells is
  physically correct, not a bug.

Temporal companion to the orifice dose model below: that sizes the *rev-1 peak*; the wall-film model
sizes the *decay* from it.

**What 0% enrichment costs — the self-priming revs (derivation 2026-07-29).** At 0% cranking
enrichment you inject only the base stoich dose, but the dry wall film steals a fraction *x* per
cycle, so the cylinder sees φ(n) = 1 − x·(1−γ)^(n−1) (γ ≈ 1/N). It fires when φ crosses the lean
limit φ_fire, so **n_fire ≈ 1 + N·ln(x/(1−φ_fire))** (=1 if x ≤ 1−φ_fire, i.e. base dose already
flammable). The deposit fraction comes free from the calibrated rev-1 enrichment: a table that fires
on rev 1 overfuels by exactly the wall loss → **x = E₁/(1+E₁)**. Using this build's E25-blend rev-1
values, N ~16→8 cold→warm, φ_fire ≈ 0.7:

| CLT | E₁ | x | revs @ 0% |
|---|---|---|---|
| 0 | ~81% | 0.45 | ~7 |
| 17 | ~62% | 0.38 | ~4 |
| 34 | ~46% | 0.31 | ~1–2 |
| 51+ | ~30% | 0.23 | ~1 (base already flammable) |

Correct table fires in ~1 rev throughout. So **0% self-primes in ~5–15 revs cold, ~1–3 warm** (order
of magnitude — swings with φ_fire; at φ_fire 0.85 cold stretches to ~15–20, and a deep-cold regime
exists where a charged film still can't vaporize to the limit → enrichment mandatory, not optional).
**Revs saved by the table ≈ the table's decay length** — the table decays over ~N revs because
that's the film-fill time; the [1,3,7,13,20] axis IS the self-priming clock. Corollary: enrichment
earns its keep **cold** (prevents a no-start); **warm** the base dose is ~1–2 revs from firing, so
extra cranking fuel just wets a plug you didn't need to wet — the 112 °F fouling story exactly.
**But the floor is a catch-margin, NOT zero:** the ~1–2 revs is the *first fire*, not a clean
pull-up to idle, and near the flammability limit ignition is probabilistic — so warm cells want a
small margin (~10–15%) for a robust rev-1 light + catch across real variation (voltage, ethanol
content, soak temp, plug condition), not 0%. Trim warm toward that floor; keep cold rich.

**Current tables read off the EMU screenshots (2026-07-29):** both `crankingCorrTbl` (gasoline) and
`crankingCorrTbl2` (ethanol) decay ~50% from rev 1→20 with a near-identical *normalized* shape in
every CLT column — built by scaling one master curve ≈ **[1.00, 0.88, 0.72, 0.60, 0.49]** at revs
[1,3,7,13,20]. Correctly concave (steep early, flat late) = the model's exponential. Two
model-based refinements, both second-order (the rev-1 peak/level is the first-order knob):
1. **Temperature-schedule the decay *rate*** — currently uniform. Warm columns should collapse
   faster (small film, fast evaporation, earlier catch → near-floor by rev 7–13); cold columns
   legitimately drag to rev 20 (big film, low cranking airflow, slow evaporation). Steepen warm,
   keep cold shallow.
2. **Ethanol table (2) should decay slightly slower cold** than table 1 (higher HoV → film persists).
Clean rebuild form: `E(n) = E_ss(CLT) + [E_1(CLT) − E_ss(CLT)]·exp(−(n−1)/N(CLT))`, E_1 = rev-1
peak, E_ss = warmup-enrichment floor, N = film-charging revs (~15–20 cold, ~4–6 warm). Note rev
13/20 rows are only *reached* on a hard start still cranking that long; a normal catch by rev 5–10
means the rev 1→7 region governs real starts.

## Starting ignition timing across conditions

Two phases: **cranking timing** (`crankingIgnAngle`, a fixed value applied through the Cranking
state, pre-catch) and **afterstart timing** (the lock/ramp from the cranking value into the idle
table at catch).

**Cranking timing — the kickback ceiling sets the max, flame-completion sets the min.**
- Too much advance → the cylinder fires well before TDC → peak pressure at/before TDC → negative
  torque that fights the starter (**kickback**: labored/slow cranking, a buck, worst case a broken
  starter). Too little → weak, late combustion → won't catch, or catches without pulling up.
- **The kickback ceiling is set by *cranking (dynamic)* compression, not static CR — and the cam
  raises it.** Tuning-literature consensus: an ~8:1 engine tolerates 0–20° cranking advance without
  kickback; 10:1 less; 12–13:1 much less. This build is SCR 10 but **cranking DCR ≈ 8.2** (late IVC,
  VVT parked — [emap_map_ratio_cam_overlap.md](../supra/notes/emap_map_ratio_cam_overlap.md) §6), so
  for kickback it behaves like an ~8:1 engine and can safely carry more cranking advance than its
  static ratio implies. Programmable-ECU default is ~15° (up to 20° small/fast-cranking, down to 10°
  slow-cranking).
- **This build:** `crankingIgnAngle` = 10° BTDC is conservative for a cranking-DCR-8.2 cammed engine
  with a slow cold flame. **12–15° is a reasonable A-B target**; the low cranking compression both
  *needs* more advance (slow burn) and *permits* it (low pre-TDC pressure). Watch for kickback.

| condition | vs. base | why |
|---|---|---|
| colder CLT | slightly more | slower cold flame needs more time to peak after TDC (don't overdo — cold also cranks slower, widening the kickback window) |
| big cam / low cranking DCR | more | slow dilute low-compression charge burns slowly; low pressure raises the kickback ceiling |
| ethanol / flex | slightly more (cold) | cold ethanol charge is slow to light (poor vaporization dominates) |
| high static CR / small cam (high cranking DCR) | less | kickback ceiling is low |
| very slow cranking (weak battery) | less | more crank-angle time per degree → kickback risk ↑ (another reason to fix cranking voltage) |

**Caveat (well-supported):** cold-start difficulty is far more often *fuel* than spark timing —
size the fuel/vaporization first; timing is the secondary lever. One tuner even found removing a
large factory cold-*retard* and running full advance gave a smoother start, so don't reflexively
retard cold.

**Afterstart timing (catch → idle):** EMU holds `afterstartIgnitionLockAngle` for
`afterstartIgnitionLockTime`, then restores to the idle table at `afterstartIgnRestoreRate`. This is
the fast flare-control lever (ignition is cycle-fast; airflow lags) — retard here to knock down a
catch flare. See the hot-restart flare section.

Sources: cranking-advance + kickback-vs-CR consensus and "cold start is usually fuel not timing"
(tuning literature, web, cited in-session); cranking DCR from `emap_map_ratio_cam_overlap.md` §6.

### First-fire dose sizing (orifice model)

λ=1 effective PW = m_air / (AFR_st × ρ_fuel × flow) with m_air = MAP·V_cyl·VE/(R·T) using the
**ECU's VE-table value** (the tables sit on top of that basis — don't "correct" the basis).
Command λ ≈ 0.55 at rev 1 decaying to ~0.85 by rev 20 (wall-film tax; richer cold, leaner hot);
crankingCorr = 1/λ − 1. Worked example + cross-validation against the known-good table (model
reproduces it within a few %): [supra/notes/crank_fail_0729.md](../supra/notes/crank_fail_0729.md).
### Cranking MAP sets the vaporization budget — and it, not fuel quantity, holds the margin

> **⚠ Scope caveat (academic check, 2026-07-29).** The U-vs-MAP physics below is sound, but the
> mainstream literature does **not** treat cranking manifold vacuum as a usable lever. Cranking is
> a near-barometric regime by design (the engine can't pump the manifold down at ~180 rpm; a cam
> raises it further — Hartman), so ECUs (a) use the key-on MAP reading to *learn baro*, not as a
> load signal, and (b) fuel cranking from a dedicated temp/rev enrichment, not the MAP-based VE
> model. Bosch's stated fix for cold-start poor vaporization is **fuel quantity** ("fuel
> precipitates on the cold wall… provide an increased fuel quantity," *Gasoline Engine Mgmt*
> p.108), never manifold pressure; Bell's "high vacuum keeps fuel vaporised" is a *running*-
> condition statement whose corollary is that low-vacuum regimes wet the walls and need
> enrichment. So the section below explains **why** cranking is vaporization-marginal; it does
> **not** license chasing cranking vacuum as the fix. Established levers: enrichment (bounded by
> plug-wetting), heat, compression, spark. Full treatment: response of 2026-07-29 + `corpus/`
> Bosch/Bell/Hartman/Heywood.

**The spark sees vapor, the table commands liquid.** λ_vapor = λ_cmd / U, where U = evaporated
fraction. MAP cancels out of that ratio (the ECU already scales m_inj with m_air), so **the only
way cranking MAP matters is through U** — but it dominates U completely.

*Flammability window (handbook values, not corpus-retrieved):* gasoline vapor burns from ~1.4 to
~7.6 vol% in air; stoichiometric vapor is ~1.70 vol% (mole-fraction calc, MW 114/29). So the
ignitable band is **λ_vapor ≈ 0.22 (rich) to ≈ 1.2 (lean)** — roughly 3:1, wide. Precision is
*not* required. The commanded window is that same 3:1 band divided by U, so **U is the entire
calibration problem**, and a ±10% table change is noise inside it.

*Why U collapses at high MAP* — Clausius–Clapeyron boiling point vs manifold pressure
(1/T = 1/T_b − (R/ΔH_vap)·ln(P/P₀)):

| species | BP @98 kPa | @60 kPa | @35 kPa |
|---|---|---|---|
| isopentane | 26.7 °C | 12.6 °C | −1.5 °C |
| n-pentane | 35.0 °C | 20.7 °C | 6.4 °C |
| n-hexane | **67.6 °C** | 52.0 °C | **36.3 °C** |
| n-heptane | 97.3 °C | 80.4 °C | 63.6 °C |
| ethanol | **77.4 °C** | 64.8 °C | 52.1 °C |

At a 33–36 °C charge and MAP 98 kPa only the C4–C5 light ends (~10–12% of gasoline mass) can
flash — and **every bit of the ethanol fraction stays liquid** (BP 77 °C). Drop MAP to ~35 kPa
and the whole C6 fraction joins in (hexane boils at 36.3 °C, i.e. at charge temp), roughly
tripling U. Bell states the principle directly, with the altitude analogy
(`corpus/four_stroke_performance.md:1462` — lower pressure, easier vaporization); Banish gives
the cold-start corollary (`corpus/engine_management_advanced_tuning.md:3178-3184`): add total
quantity because only a portion evaporates, targeting air-to-**vapor** ratio.

**Corollary — the wet-plug ceiling.** You cannot buy your way out of a low U by multiplying
liquid: at U ≈ 0.1, reaching λ_vapor 0.95 needs λ_cmd ≈ 0.10 (corr ≈ +900%), and the 90% that
doesn't evaporate pools on the plugs and shorts them first. A choke works because it does *both*
halves — the plate makes vacuum (raises U) **and** enriches. Enrichment without vacuum is half a
choke and hits the wetting wall.

### The crank-MAP / idle-TB-position identity (DBW, no idle bypass valve)

Cranking airflow demand is tiny: at 178 RPM, 3.0 L, VE 0.6 → ~3.1 g/s. Choked-flow area needed
to hold MAP 35 kPa is **~17 mm² — 0.4% of a 73 mm bore's 4185 mm²**, i.e. a nearly shut plate.
The same opening at idle (800 RPM) passes **4.5× more flow**. Therefore the TB position that
yields 33–40 kPa at idle necessarily yields **~98 kPa at cranking speed**:

> "Crank with the TB where it lands at idle" and "crank with manifold vacuum" are the same
> hardware statement with opposite signs. They cannot both be had — it is an identity, not a
> tuning trade-off.

Resolution: the TB does not need to be *parked* at the idle-landing position during crank, only
to **arrive** there at catch — which the cranking-airflow → `idleControlAfterstartDelay` handoff
already does. Crank at the DBW closing floor (~3% TPS on this build) for whatever vacuum the
hardware can make, then let airflow ramp.

**Cranking speed is a third term.** Slow cranking (this attempt: 175 RPM at 10.2–10.4 V) gives
the compression stroke ~40% longer to dump heat into cold walls than 250 RPM would, lowering
peak charge temperature and with it the in-cylinder share of U. A weak battery is a
vaporization problem, not just a starter problem.

### Zero-heat-release vs lean: read EGT and RPM texture, not fuel

A mixture that is *merely* lean still pops: sporadic fires bump RPM 20–50 and tick EGT up. **Flat
EGT plus flat RPM across dozens of sparks means zero combustion events** — you are outside the
flammability band or have no effective arc (fouled/wetted plugs), and no fuel-table change
addresses either. Check this before touching the cranking tables. Worked case:
[supra/notes/crank_fail_0729.md](../supra/notes/crank_fail_0729.md).

## Cranking a cammed engine (BC0311 264° — why this build cranks the way it does)

Build: Brian Crower BC0311 (264° adv, 218° @0.050″, LSA 114, base ICL 110), VVT-i intake phaser.
Full event math: [emap_map_ratio_cam_overlap.md](../supra/notes/emap_map_ratio_cam_overlap.md) §3/§6.
A cam changes cranking through three mechanisms — ranked by impact on this build:

1. **Late IVC → low cranking compression (the dominant term).** Parked at 0 advance, IVC = 62°
   ABDC advertised / 39° @0.050″ → **DCR ≈ 8.2** (vs SCR 10.0). At ~178 rpm there is no intake
   ram, so the rising piston pushes charge back out the still-open intake valve; effective
   compression — and with it compression *temperature* — falls. Cooler charge → less fuel flashes
   to vapor → harder first fire. Patent/tuning lit: a big cam sheds ~10 psi of cranking pressure;
   late IVC took one design DCR 9.49 → 7.70.
2. **VVT can't help at cranking.** Advancing IVC toward BDC raises cranking compression and is a
   known cold-start aid — but VVT-i needs oil pressure it doesn't have while cranking, so the cam
   sits at its parked (latest-IVC, lowest-DCR) position on every start. You always crank at the
   worst compression the cam offers. (Log: `VVT CAM1 angle` 0 through crank; parks ≈ −2° cold.)
3. **The cam raises cranking MAP / kills vacuum.** Hartman: "at lower rpm, a cam with more
   duration and overlap results in higher manifold pressures (less vacuum)." So the high cranking
   MAP (88–98) and the throttle's inability to pull it down are **partly the cam**, not only low
   airflow demand — independent reinforcement that chasing cranking vacuum is a dead end here.

Overlap/residual dilution is the *classic* big-cam idle problem (Heywood: residual ~30% at idle,
worse at cranking; Bell: overlap → reversion, weak low-speed fuel signal). **But this build's
effective overlap is mild at the parked position** (10° gap at 0.050″ lift — note §3), so cranking
dilution is moderate and idle is stable. Late IVC, not overlap, is the dominant cam term here.

**Strategy implications:**
- Cammed + cold genuinely wants a rich cranking charge (Hartman: "at cranking as rich as 1.5 to
  1" because cold vaporization wastes most of the fuel) — the enrichment instinct isn't wrong. The
  ceiling is plug-wetting: too much liquid on a cool low-DCR charge pools and fouls (exactly the
  2026-07-29 saga). Tune the window, don't max it.
- A few degrees more **cranking advance** can pay (low DCR + slow cold flame; cammed low-CR
  engines like more initial timing — lit cites 15–18° for big-cam/low-CR idle). `crankingIgnAngle`
  10° BTDC is modest; a bump is worth an A-B.
- **Faster cranking helps disproportionately** — less time for the late intake to bleed
  compression, less heat loss to cold walls. On a cam car a strong battery/starter is a *starting
  tune lever*, not just maintenance (the 07-29 log cranked at 10.2 V / 178 rpm — marginal).

Sources: Hartman `corpus/how_to_tune.md:1255-1266,1232-1234`; Heywood `corpus/ice_fundamentals.md:6123`;
Bell `corpus/four_stroke_performance.md`; cam math `supra/notes/emap_map_ratio_cam_overlap.md` §3/§6;
web (late-IVC-startability + big-cam cold-start consensus, cited in-session).

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
| `idleCrankingDC` | ubyte ×0.5 = **airflow %** | UI "Cranking airflow [%]"; `cltBins4` = 0/33/67/96 °C (09-22 XML) |
| `crankingThreshold` | word, rpm | exit Cranking → Afterstart = "engine started"; one-way until a stall |
| `engineStallRevs` | ubyte, **direct rpm** (UI max 250) | stall declared below it; must sit below the lowest cranking speed |
| `idleControlAfterstartDelay` | ≈**0.1 s/count** (5 ≈ 480 ms; 3 = 0.32 s on 2026-09-29) | catch → `Idle control active` 0→1; both idle PIDs off in state 5 |
| `afterstartIgnitionLockAngle` | sbyte ×0.5 = ° | 48 → **24.0°** |
| `afterstartIgnitionLockTime` | **×0.04 s/count** | 100 → 4.0 s flat (+ restore tail ≈ 5.5 s total locked) |
| `afterstartIgnRestoreRate` | **≈0.125 °/engine cycle per count** (measured 2026-09-29: count 4 → 0.47–0.56 °/cycle; the earlier "0.125 °/rev per count" is 2× high) | runs *after* the flat time; slews toward the idle-ignition demand both ways; lock flag clears when executed = demand — [log note §1d](../supra/notes/log_2026-09-29_allchannels_smoothclt.md) |
| `coolantFanTimeToEngage` | ms | 750 → fan re-engages 0.75 s after catch |
| `idleCoolantFanCorr` | direct % airflow, applied as **DBW DC offset** | 13 → +13% |

## What the O2 sensor reads during warm-up (injected ≠ measured) — 2026-08-02

The cranking identity `λ_vapor = λ_cmd / U` keeps working after the catch: warm-up enrichment
feeds the port/valve **wall films** (the U < 1 tax), and the WBO reads only the **burned-gas**
result — the stored fraction is invisible to it. Consequences:

- **This build's calibration says so explicitly** (`supra 06132026.xml.emub3`): idle-row warmup
  enrichment at CLT 32/42 °C = +12/+9 % (pump `warmupTbl`) and +29/+23 % (ethanol `warmupTbl2`)
  → ≈ **+23/+18 % injected at E60** — while `warmupTblLambdaCorrTbl(2)` are **all zero**: the
  λ *target* is unchanged during warm-up. Intent: burned mixture at the normal target, enrichment
  covers film storage only.
- Heywood: cold, inject "substantial additional fuel beyond that required if fully vaporized"
  (corpus/ice_fundamentals.md:13593–13595) since "only a moderate fraction of the fuel injected
  will vaporize" (13596–13597); then as surfaces warm, "succeeding injections must be reduced
  below the nominal stoichiometric requirement" to burn off the stored excess (13601–13603).
- **What the gauge should show:** first ~25–33 s — nothing (WBO heater, `Lambda is valid`=0,
  pins 1.00). After validation: **near target with a mild rich bias** (a few % for the first
  minutes) from film burn-off returning unmetered fuel plus cold-wall partial-burn HC/CO reading
  rich on a wideband. **Sustained severe rich (λ ≤ ~0.85 for minutes) is over-delivery, not a
  cold-engine requirement** — the burned charge doesn't want 0.8 (slower, less stable cold burn),
  and the surplus is bore wash / oil dilution / plug fouling (heat-range-7 BKR7EIX is the
  documented fouling victim).
- **Reading rule:** measured λ during warm-up is the *check* on enrichment sizing precisely
  because the stored fraction never reaches the sensor. "Injected very rich" and "measured near
  target" is the correct pairing; "measured very rich" means the film tax was overpaid.

### Rich reading + lean stumble when pulled — the fork (2026-08-02, observed on this car)

Both at once is a signature, not a contradiction; a uniform pull is the wrong lever. Ranked:

1. **Cold-amplified per-cylinder maldistribution (prime suspect — documented FFIM behavior).**
   The WBO reads the 6-cyl average; wall-film behavior is port-specific and the warm-tuned
   per-cyl trims don't know the cold pattern. Average rich while the leanest cylinder rides the
   misfire limit → pulling global enrichment stumbles the lean cylinder while the average still
   reads rich. Self-confirming: a stumbling cylinder's partial-burn HC/CO pushes the reading
   *richer*. Diagnostic: per-cyl EGT spread cold vs warm (egt-analysis skill); ID the laggard.
2. **E60 preferential evaporation → two-phase schedule error.** Below ~50–60 °C port temp the
   ethanol fraction (BP 77 °C — see the Clausius–Clapeyron table above) barely vaporizes: early
   charge vapor is gasoline light-ends (lean-fragile → the stumble edge lives here), and the
   stored ethanol pays back as a **delayed rich slug** as ports warm through ~50–77 °C — minutes
   1–5, the observed rich window. Signature: λ *humps* mid-warm-up rather than sitting uniformly
   rich. Fix is the CLT **schedule**, not the level: hold/raise the coldest cells, taper the
   40–60 °C cells faster (mostly on `warmupTbl2`).
3. **The burned mixture may legitimately need to be rich cold — command it.** Slow cold burn +
   cam dilution + the spread from (1) want stability margin (burned λ ~0.90–0.95; OEM-standard
   practice, not corpus-retrieved). With `warmupTblLambdaCorrTbl(2)` zeroed, that need can only
   exist as uncommanded open-loop surplus that reads as error. Populating the warm-up λ-target
   correction makes the richness commanded, STFT-consistent, and sizes enrichment against a
   truthful target. Secondary lever: +2–4° cold idle ignition target (room exists under the
   27–30° max-torque band) — slower lean cold vapor wants more advance; costs recovery reserve.

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

- [prime_pulse.md](prime_pulse.md) — key-on/first-sync prime injection: sizing (front-loads the rev-1 wall film) + the coupled cranking-fuel cut
- [idle.md](idle.md) — steady-idle settings + principles hub (airflow PID, KD, DBW lag, idle ignition)
- [ignition.md](ignition.md) / [timing.md](timing.md) — afterstart ignition lock behavior
- [dbw.md](dbw.md) — DBW airflow transport lag (~750 ms), the reason air is the slow recovery lever
- [idle_stall.md §B](idle_stall.md) — cold-start / post-start stall decision tree
- [cammed_idle_instability.md](cammed_idle_instability.md) — why a diluted idle charge is unstable
- [supra/notes/airflow_actuator.md](../supra/notes/airflow_actuator.md) — live cranking/active airflow values
