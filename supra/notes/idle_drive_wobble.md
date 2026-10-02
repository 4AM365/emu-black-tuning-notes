# Rolling return-to-idle wobble ("drive wobble") — Supra measured specifics

Build-specific numbers behind [`notes/idle_stall.md`](../../notes/idle_stall.md) §H and the consolidated [`notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md). The generic notes hold the mechanism; this file holds the measured values for this car.

## Observed event

- RPM craters well below idle target: **~1800 → 525 rpm at a 1200 target**, then limit-cycles **525 ↔ 1390** during a neutral coast-down to idle while the car is still rolling.
- Confirmed decoupled: RPM/VSS ratio swings 8× (impossible in a fixed gear) — the driver neutral-shifts toward a stop, engine free-falls toward idle.

## Fault 1 — rich low-RPM VE bog

- As RPM craters and MAP rises toward **60+ kPa**, speed-density over-fuels. Measured `Lambda 1` dives to **0.68 (AFR 9.9)** against a **0.93** target — low-rpm VE is **~17–19% rich** at MAP **35–64 kPa**.
- **Baseline caveat:** the −17–19% figure is from *pre-correction* logs at **E25** (not the usual E60). A global **−18% pump (`veTable`) / +10% ethanol (`veTable2`)** correction was applied afterward (v2 export). Net effect is fuel-dependent through `tblsVEBlend`: ~**0%** at E60 (~38% pump weight — the −18/+10 nearly cancel) but ~**−11%** at E25 (73.5% pump). So on v2 the dip residual is still **~−18% rich at E60** but only **~−9% at E25**. A lean computed from the E25 log is right only for E60; at E25 it over-leans ~9% → lean-stumble risk. **Always re-measure lambda on a v2-calibration dip log at the fuel you actually run before leaning the 500/842 rows.**
- **`rpmBins` starts at 500 (`1F4`).** The 500-rpm VE row governs fueling precisely when RPM craters into a dip; left as a verbatim copy of the 842 row it is ~17% too rich. Lean toward λ0.93. The 842 row and the 1184 idle row (~9% rich at steady idle, **λ0.844**) want the same treatment — richness increases as RPM drops, so the lean deepens toward the 500 row.
- `Short term trim` is clamped ~**±2–3%** with slow integration (intentional), so it can't correct a fast dip and won't reveal true VE. Set VE from measured lambda error, apply ~80% first, lean both `veTable` and `veTable2` by the same ratio.

## Fault 2 — fan-gated airflow drops out at speed

- The **+13% `idleCoolantFanCorr`** is VSS-gated **off above ~56 km/h**. On a return from above ~56 km/h base idle airflow is the bare **~26.5%** table value instead of **~39%** (fan-on), and the airflow PID is clamped at **+12** — not enough to hold. Below ~56 km/h the fan is on and returns catch cleanly.
- Fixes that don't add idle variation: more airflow-PID authority (`idleAirPIDOutMax` / `idleAirFlowIntegralLimitMax`). Leave the fan +13% — correct load-comp.
- **`idlePIDUpdateInterval` is not a lever (established 2026-07-17):** the symbol reads 200 but the loop measurably runs ~40 ms — it is vestigial or unexposed, and there is no sampling lag to remove. Authority (`idleAirPIDOutMax`) is what relieves a saturated catch. See §2026-07-17 for the measurement.

## Fault 3 — idle locked out by the MAP-activation gate (`idleMinMapToActivate`)

Source log: `died_hot_return_to_idle_again.csv` (hot, CLT ~96 °C), closed-throttle rolling decel, PPS=0. The car stalled returning to idle and the binding gate was **`Idle On if MAP over` = 25 kPa**, not VSS (`Idle force open loop` = 0 the whole coast — the clutch press had cleared the VSS force). Mechanism + generic write-up: [`notes/return_to_idle_bog.md §3`](../../notes/return_to_idle_bog.md).

**The three MAP bands measured on this car** (the inputs you need to set the gate):

| Regime | MAP (this log) |
|---|---|
| Closed-throttle engine braking, high RPM (1700–3000) | **13–14 kPa** (lift transient touched **16–17**) |
| Stable warm idle (state 2, stopped, ~1000–1260 rpm) | **32–58 kPa** (median 37, floor **32**) |
| Current gate `idleMinMapToActivate` | **25 kPa** |

MAP rises as RPM falls on the closed-throttle descent, so the gate value maps directly to the RPM where idle is *allowed* to grab:

| Gate (kPa) | Idle catches at ≈ | Verdict |
|---|---|---|
| **25 (current)** | **582 rpm** | too late — engine already gone, stalls |
| 22 | ~728 rpm | still marginal |
| **18 (recommended)** | **~1060 rpm** | recoverable within the ~160 ms DBW lag |
| <17 | >1300 rpm, risks tripping on the 16–17 high-RPM braking transient | too low |

**Recommended: `idleMinMapToActivate` 25 → 18 kPa.** That's the bottom of the valid window
**(17, 32)** — just above the worst engine-braking MAP seen (17, so coasting is still excluded)
and far below the 32 idle floor (so it never blocks real idle). It moves the idle catch from
582 rpm up to ~1060 rpm, giving the airflow PID + idle ignition time to arrest the drop before the
DBW actuator lag would otherwise lose it. Re-verify a few closed-throttle coast-downs after the
change (idle should not wake at high RPM during sustained braking; overrun fuel/throttle unchanged).

## 2026-07-17 follow-up — gate fix is live; the *secondary* lever is now the binding one

Two logs, hot (CLT 96 °C), 14-channel idle/DBW capture (RPM, idle target, TPS, DBW Out DC,
DBW target, DBW Target source, Idle state, custom corr, PID air %, idle ign corr/target, CLT,
pre-IC T — **no MAP/PPS/clutch/electrical-load channels**): `armedstatebogjuly17.csv` (707 s
drive, repeated return-to-idle hunts) and `randomlydied.csv` (61 s, one clean stall).
Figure: [`july17_idle_dbw_hunt.png`](july17_idle_dbw_hunt.png).

**Fault 3 fix is applied and working.** Today's tune reads `idleMinMapToActivate` = **18** (was 25).
The MAP-activation lockout is gone: idle now stays **active (`Idle state` = 2)** all the way down
through the sag — in `randomlydied` it held state 2 from 1180 rpm down to ~324 rpm before the engine
died. No state-4 lockout coast like `died_hot_return_to_idle_again.csv`. The gate is no longer the killer.

**What killed it = the airflow PID's output clamp** (`idleAirPIDOutMax` = **15** at the time of these
logs; raised to 25 later the same day — see below). When a load disturbance drops RPM off a stable
~1180 idle, the air PID pegs at **+15 (saturated)** and idle ignition at its **~+8.5° cap**, yet the
DBW **target only rises 4.4 → ~5.3 %** and TPS ~0.8 % — nowhere near enough air. Note the loop was
**pinned on its clamp**, so this is an *authority* failure, not a speed failure: while saturated,
no gain and no update rate can add another cubic inch of air. The loop itself was **fast** (measured
~40 ms, see below) — the only real actuator delay is the ~160 ms DBW lag. Two outcomes seen:
- **`randomlydied`** — no rescue: RPM 1180 → 324 → 0, a clean **saturated death**. `DBW Out DC ≈ 0`
  through the fatal sag (**not** on the close rail) — the plate simply was never commanded open enough.
- **`armedstatebog`** — rescued each cycle by a throttle blip (`DBW Target source` flips 2→3/0,
  TPS 11–22 %), RPM over-recovers to ~1600–2000, idle re-grabs and slams the plate shut, RPM craters
  again → a **~1.2 s limit-cycle** swinging RPM ~330 ↔ 2000 for seconds at a time. Recoverable, no stall
  in this log (the lone `RPM=0` at t=579.12 is a **single-sample trigger dropout** at ~2085 rpm, not a death).

**The −35 "negative rail" the driver noticed is a symptom of the rescue-hunt, not the cause.**
At idle the DBW motor holds a **steady negative bias** (~−4 to −13 %) because the throttle's limp-home
rest sits above the idle position — negative is normal there. It only slams to the **−35 close rail**
when idle re-takes control right after a rescue blip opened the plate to 10–22 % and yanks it back to
~5 % (top panel). In the clean death DC never approached −35. So the rail = the position servo pulling
the plate back down after each over-recovery; the actual failure is the throttle **not opening** (air
authority), not the motor holding it closed.

**Idle DBW throttle authority window:** `idleDBWTargetMin`/`Max` = **24 / 80 = 2.4 % / 8.0 %** throttle
(matches the repo `supra export 05222026 (2.4-8.0 range)`). Note the saturated death topped out at
**~5.3 % — below the 8.0 % ceiling** — so the binding limit is the **+15 air-PID clamp × airflow→throttle
mapping**, not the mechanical 8 % ceiling. That means the primary lever is **PID output authority**;
the 8 % ceiling still has headroom to absorb a bigger PID output. (Loop speed is *not* a lever here —
see the interval note below.)

**⚠ `idlePIDUpdateInterval` is NOT connected to this loop — do not treat it as a lever.**
The symbol exists in the tune (`value="200"`, flat word), but the idle airflow PID **demonstrably does
not run at 200 ms**. Measured from the July 17 logs (25 Hz sampling): the hold-length distribution of
`Idle PID air % correction` while `Idle state`=2 is

| hold | 1 smp (40 ms) | 2 (80) | 3 (120) | **5 (200)** |
|---|---|---|---|---|
| `randomlydied` | 54.1 % | 28.3 % | 11.3 % | **1.4 %** |
| `armedstatebog` | 53.7 % | 25.2 % | 11.4 % | **2.3 %** |

**Median hold = 1 sample = 40 ms, with no spike whatsoever at 5 samples.** A true 5 Hz loop would
produce an unmistakable staircase with 5-sample treads; instead the decay is smooth and geometric —
the signature of a value updating at or faster than the log rate, occasionally re-quantizing to the
same number (the channel is 1/16-quantized). **The loop is running ≥25 Hz, not 5 Hz.**

Corroborating evidence that the symbol is vestigial (a v2 relic) or live-but-unexposed:
- **Never documented** in any of the 23 v3 help pages (`docs/emu-black-help/`).
- **Not in the `Idle → Airflow → Airflow PID` dialog** (screenshot: that dialog holds exactly the three
  gains, two integral limits, two output clamps — seven fields, no interval).
- **Frozen at 200 across all 14 repo tune exports** spanning months — never varies.
- **Orphaned in the XML at line 433**, ~350 lines from every other idle PID symbol (784–808), sitting
  among `starterOutput` / `autoStartTime` / `enableBuzzerOnStartup` / `canBusTerminator`.
- Its only association with "Idle" was the `idle*` **name prefix**, via
  [`notes/tune_feature_tree.md`](../../notes/tune_feature_tree.md), which explicitly warns its
  page assignment is *"derived from symbol names"* and may sit a node off.

Relic vs. unexposed-but-live can't be separated from the tune file, and it doesn't matter: either way
**there is no 200 ms sampling lag in this loop and no interval to tune.** *(This supersedes earlier
text in these notes that treated 200 ms as a tuned, validated setting and blamed loop-rate lag for the
sag — both were wrong. The only real actuator delay here is the ~160 ms DBW lag.)*

> Aside, now academic: EMU's gains are dt-normalized anyway — units are `%/°`, `%/(°·s)`, `%/(°/s)`,
> so I and D carry explicit time. Even if the interval were adjustable it would scale **no** gain;
> a faster loop never *gives* more gain, it only removes dead time (which *permits* more gain).

**The ceiling is the output clamp, and only the output clamp moves it.** Measured mapping:
the 2.4–8.0 % actuator window spans **5.6 % throttle over 0–100 % Airflow%**, so **1 % airflow
≈ 0.056 % throttle**. Hot idle base ~4.4 % throttle ≈ **35.7 % airflow**; the `idleAirPIDOutMax`
= +15 clamp therefore buys only **+0.84 % throttle** (4.4 → 5.24 %) — which is exactly the **5.3 %**
ceiling logged in `randomlydied`. Neither the gains nor the interval change that number. Headroom is
large: reaching the 8.0 % mechanical stop from a 35.7 % base would take ~+64 % airflow, so the clamp
can rise a long way before the actuator range binds.

**Change applied 2026-07-17: `idleAirPIDOutMax` 15 → 25.** Confirmed live in the Airflow PID dialog;
it is the *only* value changed in that group (KP 2048, KI 205, KD 0, integral limits −4/12, OutMin −6
all unchanged from the June 29 XML). Expected effect by the mapping above: the PID's ceiling moves from
**+0.84 % → +1.40 % throttle** (4.4 → ~5.8 % at a 35.7 % airflow base), i.e. ~⅔ more air available to
arrest a sag. Still well inside the 8.0 % mechanical stop. **Next step is to re-log a hot
return-to-idle and confirm the PID no longer pins at its clamp** — if it still saturates at 25, the
clamp can go higher before the actuator range binds.

**Remaining levers (author's call on which/whether):**
- `idleAirFlowIntegralLimitMax` (12) — keep the integral cap **below** the output cap (25) per the
  independent-clamp / anti-windup rule; the gap just widened, which is the desired direction.
- **The un-applied gain rescale** — KP/KI were never scaled down for the 4.5 → 5.6 % range widening,
  so loop gain sits ~1.24× hotter than the pre-rescale calibration intended. A candidate contributor
  to the limit-cycle hunting, and it interacts with the clamp change; see
  [airflow_actuator.md → Airflow PID](airflow_actuator.md).
- ~~`idlePIDUpdateInterval`~~ — **struck: not a lever.** Measured loop rate is ~40 ms, not 200; the
  symbol is vestigial or unexposed. Sampling lag is therefore *not* an available explanation for the
  hunting, which pushes the remaining candidates toward the gain rescale above, the clamp, and the
  real ~160 ms DBW actuator lag.
- If PID output is raised, confirm `idleDBWTargetMax` (8.0 %) covers the worst hot-load idle-air demand;
  nudge up only if the PID starts pinning against 8 %.
- `Idle airflow custom corr.` sat **−2/−3 %** at hot idle in `randomlydied` — it's trimming air *out* and
  narrowing an already-tight margin; revisit whether that hot-CLT custom cell should be less negative.
- **Identify the disturbance:** these 14-channel logs can't show *what* pulled RPM off stable idle
  (A/C, PS, alternator, clutch/driveline, MAP). Add MAP/PPS/`Idle force open loop`/electrical-load
  channels to the next capture so the trigger — not just the controller's failure to answer it — is visible.

## 2026-07-30 follow-up — clamp fix confirmed working; the fault moved off the clamp

Source log: `ahfuck less data.csv` (Supra, hot **CLT 96 °C**, 18 s, same 14/15-channel idle/DBW
capture — RPM, idle target, TPS, DBW Out DC / target / source, Idle state, custom corr, PID air %,
idle ign corr/target, CLT, pre-IC T; **no MAP/PPS/fuel/lambda/ignition-total/ECU-state**). This is the
re-log §2026-07-17 asked for. Its full-channel companion `ahfuck.csv` arrived **truncated** (exactly
8192 bytes, zero newlines, cut off mid-header — no data rows), so MAP/fuel/spark **could not be
cross-checked for this event**; mixture/spark contribution is assumed-consistent-with-priors, not proven.

**The `idleAirPIDOutMax` 15 → 25 change is confirmed live and working.** On the fatal sag the air PID
reached **+18.25 with clear headroom to 25 — it did NOT saturate**, and airflow reached **74 % ≈ 6.5 %
throttle** (vs July 17's pinned +15 / 5.3 %). So the raised clamp *did* buy more air, exactly as the
mapping predicted. **Per §2026-07-17's own test, an unsaturated PID means the clamp is no longer the
binding lever** — and the engine stalled anyway. The fault has moved.

**What killed it this time = time + torque, not the gate and not the clamp.** Sequence (t = s into log):

| t (s) | RPM | Idle state | Idle air % | PID | Idle ign corr | note |
|---|---|---|---|---|---|---|
| 6.2–9.0 | 2477→1771 | **1 (armed/approach)** | **40.5 (open-loop, fixed)** | 0 | 0 | starved: 40.5 vs 54.5 base |
| 9.08 | 1771 | **1→2 (closed loop engages)** | 59.5 | −0.6 | −0.5 | engages late, RPM already sinking fast |
| 9.1→10.0 | 1771→647 | 2 | ramps to **74** | to **+18.25** | to **+9.0** | PID not saturated; airflow lag can't catch |
| 10.16 | 505 | **2→4 (handoff)** | **74 → 36.5 (air dumped)** | 0 | 0 | air pulled at the worst moment |
| 10.20–10.36 | 342 | 0 | (throttle blip TPS→19 %) | — | — | too late |
| **10.40** | **0** | — | — | — | — | **stall** |
| 13.2–15.7 | 157–226 | 3 | 31 | — | — | restart cranks, never catches → 0 |

Collapse rate **1771 → 0 in ~1.3 s**.

**⚠ Correction to the first-pass read (Will, same day).** My initial "armed airflow **too low**, raise
it" was **wrong — backwards.** The armed value is intentionally ~5 % **too high**. Confirmed in the tune
(`cranking_silliness.xml.emub3`, 2026-07-30): `idleArmedAirFlow` = `40 46 4C 50 51 51 51 51` →
**32.0, 35.0, 38.0, 40.0, 40.5, 40.5, 40.5, 40.5 %**. The decel bins the coast sits on are the **40.5 %**
cells, vs a warm-idle need of **~35.7 %** — a deliberate **+~5 % cold-oil margin** (high oil viscosity on a
cold-oil / hot-CLT start needs more air or idle bogs). Comparing 40.5 to the "54.5" state-0 value was the
error: 54.5 is not the warm-idle base. **Do NOT raise the armed bins; if anything they're the windup
*source*, not a starve.** And there is no way to schedule the margin away: **`oilTempInput = 0`** — no
oil-temp sensor feeds EMU, so a flat table margin is the only available tool. Any real fix is
controller-side, not table-scheduling.

**Windup hypothesis (Will's) — plausible + documented, but the reduced log argues partly against it.**
Mechanism: the +5 % armed/active air makes a warm-oil engine idle high, so the airflow integrator winds
to its `idleAirFlowIntegralLimitMin` = **−4** floor to pull air out; on a load drop it must climb −4 → +12
before delivering air → delayed catch → stall. Coherent, and it's the [idle_hot_drift_pid_windup]
mode. **But** three log facts don't fit *this* event: (1) at re-engagement (1771 rpm) total PID output was
**−0.56 %**, not parked at −4 — no deep negative hole at hand-off; (2) the integral never saturated
positive either (cap +12; total reached +18, so P supplied the rest — I-term had room); (3) **no
steady-idle dwell in this window** for the integrator to wind up during — the engine went driving →
coast → stall, never settling at idle. Windup could still fit only if the integrator **carried** a
negative charge across the drive from the prior idle, and the −0.56 argues against a deep carry.
**Cannot be settled without the `Monitored I term` channel — absent from this reduced log.**

**The signature: both loops had authority left and still lost it.** Airflow PID reached **+18 of 25**;
idle ignition reached **+9° of a ~+12° `idleIgnAngleCorrection` ceiling** (`18 13 F 0 0 -7 -D -14` sbyte).
*Neither hit its clamp*, yet RPM fell 1771→0 in 1.3 s. So this is a **speed** failure, not an authority
failure — something robbed torque faster than air+spark could replace it.

**Root cause = cold-oil friction (owner-identified, 2026-07-30; consistent with all log evidence).** Just
prior to this event the engine was stumbling from airflow starvation due to oil viscosity (cold oil,
hot CLT — coolant warms in minutes, oil in 10–20). Mechanism, Heywood §13.3-grounded: hydrodynamic engine
friction depends on lubricant **viscosity**, and cold oil is several× more viscous → **FMEP elevated
across the board** → the thin idle torque margin is eaten. When RPM sagged toward the stop there was no
surplus torque to arrest it, and the margin only worsened on the way down → the 1.3 s collapse. This
*explains the paradox* of unsaturated loops: the **air lever had authority but is too slow** (Bosch p.224:
"the air channel only permits gradual changes in torque"; ~750 ms throttle transport lag) to answer a
1.3 s friction-driven sag, and the **ignition lever is fast but small** (Kiencke §5.2: idle stabilized by
low-RPM spark advance) — a few % of torque, asked to cover a large friction load alone, and it couldn't.
The state 2→4 hand-off dumping air 74→36.5 % at 505 rpm was the last shove.

**Windup is ruled out** (supersedes the hypothesis above): PID output was −0.56 % at re-engagement, never
near the −4 floor, never saturated — it was out-torqued by friction, not held down by a wound integrator.
The only thing still unprovable without MAP/lambda is a *secondary* brief lean on the way down; cold-oil
friction alone accounts for the stall, so the full log is now confirmatory, not load-bearing, for cause.

Remaining findings (unchanged): closed loop engages at 1771 (reasonable); the state **2→4 hand-off dumps
air 74 → 36.5 %** at 505 rpm into a late blip (`DBW Target source`→0) — pulls air at the worst instant;
ceiling check holds (74 % air = ~6.5 % throttle vs the 8.0 % `idleDBWTargetMax` stop — room left, ran out
of *time*).

**Proposed fix (owner, 2026-07-30): an oil-temp-based idle-airflow modifier.** Physically correct — it
targets the friction directly. Two constraints: (1) **no oil-temp signal exists** — `oilTempInput=0`, and
EMU won't model it (the `oilTempCal` tables are sensor transfer functions, not an estimator; with no input,
oil temp = 100 °C failsafe), so a true modifier needs an **added oil-temp sensor**. (2) It **reduces** net
idle variation: today the flat **+5 % armed margin is permanent** for a condition true only the first
~15 min; an oil-temp (or runtime-decay) add lets the flat table drop to warm-idle-correct and adds air
**only when oil is cold** — fewer hot-idle surprises, and it removes the windup concern. **OEM practice**
(corpus): idle-up is scheduled on **coolant temp + a post-start time decay** (Bosch p.235), *not* oil
temp — the time decay is the industry's cheap proxy for "oil lags coolant." A **sensor-free runtime-decay**
idle-air add (gated on cold start) captures the normal warmup gap for zero hardware; it misses the edge
cases a real sensor catches (short hot restart with cooled oil, cold-ambient soak).

The truncated full-channel `ahfuck.csv` would still confirm a secondary lean and show the `Monitored I
term`, but is no longer needed to establish cause.

**Two real warmup effects, separated by timescale — NOT one dismissing the other.** The "DBW area-growth
lag" is TWO physical effects on different clocks; an earlier draft wrongly minimized the TB one to hand
the whole thing to oil. Corrected:

- **TB bore thermal expansion — ~20% of idle air, FAST (owner-confirmed magnitude).** Stainless plate
  α 17 vs aluminum bore α 21.5 ppm/°C, 73 mm bore ([project_supra_throttle_body_materials]). Cold-start
  math (ΔT≈70 °C): radial gap growth = 36.5 mm × (21.5−17)e-6 × 70 ≈ **0.0115 mm**; added leak area =
  π·73 × 0.0115 ≈ **2.6 mm²**. Against an idle **effective** area of only ~13 mm² (choked, ~35 kPa MAP,
  few g/s) that is **~20%** (→ ~30% on a very cold start / low-α plate). *Not small.* As the TB metal
  heats, the bore opens faster than the plate → effective area grows ~20% → ECU **closes** the DBW to
  hold idle — this IS the "area growth." Scales with ΔT: biggest on a cold start, ~0 on a hot restart.
  Tracks TB metal ≈ coolant/underhood, so it **settles when CLT does (minutes).**
- **Oil-temp friction — large, SLOW tail.** Separate clock (10–20 min). The decay that persists *after*
  CLT and the TB metal have both settled.

Both push DBW opening the same direction over warmup, so they can't be split by sign — only by **when
they stop**: the fast ~20% chunk that settles with coolant is the bore; the tail that outlives coolant is
the oil. (Prior "TB is the wrong suspect / small" framing was the error — it was sycophantic
minimization to fit the oil narrative. TB is real and ~20%; the distinction is timescale, not size.) **Practical:** idle `DBW target`/`Idle air %` vs engine runtime,
masked to stable idle from CLT-hot outward, *is* both the oil-warming signature and the shape of the
sensor-free runtime-decay idle-air table — measure it off a from-cold warmup log to calibrate the fix.

> **Measured, 2026-08-01 — [oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md).** That
> measurement is now done, across 11 logs from 2026-05-24 → 07-30. Hot coolant + cold oil needs
> **51–58 airflow % (5.2–5.6 % TPS)**; hot coolant + hot oil needs **28–31 % (3.9–4.1 % TPS)** —
> an adder of **≈ +25 airflow %**, ~1.8×. Demand peaks **90–180 s *after*** CLT reaches 96 and
> settles 8–12 min later. Oil pressure normalized for pump speed falls a further **44 %** with CLT
> flat at 96, while charge temp *rises* — so it is friction, not coolant and not charge density.

**Symptom fingerprint (owner-confirmed, long-standing):** idle **struggles for the first few minutes
after CLT peaks, then is fine the rest of the drive** = oil lagging coolant. CLT reaches target in
minutes; oil (the true friction variable) takes 10–20 min, so friction stays high past CLT-flat and idle
fights it until the oil catches up, then it's fine until the engine cools. If you see this shape, it's
the oil-lag window — not a tune fault.

**Plan (2026-07-30):** (1) **interim** — raise base idle airflow in the *actual idle region* (the live
`idleActiveAirflow` target rows ≥ floor), **not** the approach/armed cells, and let the PID trim it down.
Sound for the speed failure: it **pre-positions air at the catch** so the engine enters idle with it
instead of waiting ~750 ms on the slow PID; leaving the approach lean avoids a hang/drive-wobble on the
descent. Caveat: at warm idle the extra base sits with the PID trimming negative (the mild negative-trim
posture) — keep the uplift modest; bounded by the current negative airflow limits. (2) **permanent** —
**oil-temp sensor on order** → oil-temp-scheduled idle air.

**Permanent design (owner, 2026-07-30) — armed table cold-oil-rich, oil-temp subtracts:** calibrate
`idleArmedAirFlow` adequate for the **hot-CLT / cold-oil pocket** (max friction), then as the oil-temp
sensor reads warmer, **subtract** armed airflow in that region back to warm-correct. Fixes the actual
stall mechanism (pre-positioned cold-oil air beats the slow-PID wind-up), and **resolves the windup
concern**: the subtraction removes the excess when warm, so the integrator never parks negative trimming
a permanent margin (cold oil → high air the engine needs, PID not fighting; warm oil → correct base,
nothing to trim). **Only an oil-temp input can do this** — a CLT-indexed table applies the same hot-CLT
cell to both cold-oil-early and warm-oil-later, which is the blind spot. Cost of excess air in-pocket =
tach settles slowly / bounces down (benign; beats a stall).

**⚠ CRITICAL — the fail-safe direction is defeated by `oilTempFailSafe` as currently set.** Intent: dead
sensor → land on the too-much-air (cold-oil) cal. But the tune has **`oilTempFailSafe = 100`** (°C, hot);
on sensor fault EMU substitutes 100 °C → the subtraction map applies **max** subtraction → **least** air
→ a stall on the exact failure being designed against. **Fix: set `oilTempFailSafe` to the cold end
(−40, or below the coldest bin)** so a fault → zero subtraction → max air. Fail-to-cold, not fail-to-100.
This one scalar is what makes the fail-safe hold. (Also confirm the sensor's own failure mode reads
low/open, not a mid-scale short.)

**Oil-pressure as a viscosity proxy (owner floated it) — real but confounded.** Cold thick oil = high
pressure, and the sensor already exists ([oil_pressure]). But pressure **rises with RPM/pump speed**, so
across the armed table's ~1500–2500 rpm span raw oil pressure misreads viscosity (adds air from RPM, not
cold oil); and at idle it's low, often relief-capped cold, and worst-accuracy — the cold-vs-hot idle
*spread* may be too small to meter. Use **oil temp as the primary index** for the multi-RPM armed region;
use oil pressure only as a **fixed-idle-RPM** real-time trim (RPM confound removed), and only after
logging idle oil pressure cold vs hot to confirm the delta is usable.

**EMU implementation check:** confirm the firmware can index idle/armed airflow on oil temp (it may need
the `Idle airflow custom corr.` path rather than a native oil-temp axis); keep the subtraction smooth and
monotonic in oil temp so the air "slips down" cleanly with no steps.

**Cranking side (separate issue — the failed hot *restart*, not the stall).** After this event Will cut
the hot-start extra air+fuel to prevent flooding. Confirmed in the tune: `idleCrankingDC` = `AC 7E 3E 00`
→ **86, 63, 31, 0 %** by CLT — hot bin now **0 %** (no flare → no flare→sag, no flood), cold bins keep
**86 %**. Good gradient; verify a genuinely-cold start still catches on the 86 %. Consistent with
[project_supra_hot_restart_flare_sag] (hot restart stumble is air/timing/flooding, not lean).

## 2026-08-22 follow-up — with the gate and clamp fixes live, the residual is the activation hand-off itself (entry dip → ramp-masked PIDs → high, glacial settle)

Source log: `moviedrive.csv` (2026-08-22, 19.6 min stop-and-go, hot: CLT jitters 96–109 °C
sample-to-sample; oil warm — `Engine oil pressure` 2.4–3.2 bar at idle. 15-channel idle capture:
RPM, MAP, TPS, CLT, oil pressure, idle state/target/air %/PID air/custom corr/ign corr/ign target,
ignition angle, clutch). Tune readings below are from **`supra way more sauce.xml.emub3` (2026-08-16
export)**; ⚠ the binary project was re-saved 2026-08-21, so later edits (if any) are not in that XML.
Figure: [`idle_entry_dip_20260822.png`](idle_entry_dip_20260822.png).

**Reference event (log t 845.5–872, twin at 828.3):** pedal released at 2232 rpm → armed (state 1)
→ activation at **1557** → dip to **1327** (+0.44 s) → overshoot to **1620** (+1.44 s) → then a 25+ s
creep that parks at ~1250 and never reaches the 1200 target in the observation window. The twin
entered at −763 rpm/s (clutch-in free decel) and double-dipped to **1155**. **Neither prior fault
fired:** MAP sat 24–29 kPa > `idleMinMapToActivate` (18, Aug-16 XML) the whole coast — no state-4
lockout; the air PID never touched its output clamps (`idleAirPIDOutMin/Max` = **−15/+25** in the
Aug-16 XML — OutMin has been widened from the −6 documented on 07-17). State sequence 0→1→2 clean,
no sync-loss flag cascade (trigger channels not logged, but the fingerprint is absent).

**Phase-by-phase mechanism:**

1. **Armed coast (state 1).** Activation cannot happen above **idle target + `idleRAMPDownOffset`**
   (350, Aug-16 XML → threshold 1550 at the warm 1200 target; the pre-activation `Idle target`
   channel displays the threshold, and entries across the whole log cluster at 1530–1560).
   Until then the engine free-decays on the open-loop armed airflow (`idleArmedAirFlow` decel bins,
   40.5 % — unchanged since the 07-30 read) at −500…−760 rpm/s, MAP 24–29 kPa. Corroboration of the
   threshold arithmetic: two entries in this log activated at ~1770 while rolling faster — the VSS
   target increase (`idleAboveVSSTargetIncrease` = 200 above `idleIncreaseTargetAboveVSS` = 50)
   moves the threshold by the same amount.
2. **Activation step + air-torque lag = the dip.** At state 2 the airflow command **steps to
   ≈ armed + 20 %** (60.5 / 60.0 here, 59.5 in the 07-30 log — see open items). TPS follows in
   ~0.3 s (4.3 → 5.5 %), but torque arrives on the ~750 ms air lag, so RPM keeps falling ~0.45 s
   past activation. **Dip depth ≈ entry decel rate × air lag:** −658 rpm/s entry → floor 230 below
   the threshold. The catch is done by this open-loop step, not by the loops — because:
3. **The ramp masks the dip from both PIDs.** The target ramps from the threshold toward base at a
   **measured 250 rpm/s** (`idleRAMPDownDecayRate`, 1:1 RPM/s — the Aug-16 XML's 700 was stale;
   owner confirms the live revision at log date carried 250. Stale-export lesson in Open items).
   RPM falls at ~−520 vs the ramp's −250, so tracking error at the floor is only ~−100 rpm: the
   ignition correction peaks at just **+1.0–1.5°** and the air PID at **+2.6 %**. That is exactly
   what the gains dictate — ign Kp = 10 raw/1024 ≈ 0.01 °/rpm → ~+1° at −100; the loops are
   answering the error they are shown, and the ramp shows them almost none.
4. **Recovery crosses the still-falling ramp → negative accrual.** First negative air-PID sample
   at **+0.64 s** (RPM 1369 vs ramped target 1380). When the ramp bottoms at 1200 (+1.36 s) RPM is
   1608 → error +400: the ignition integral pegs its clamp (−4.5…−5.0; `idleIgnitionIntegralLimitMin/Max`
   = ±5; the twin hit −5.0 exactly), angle drops 18.5 → 13.5°, and the air PID grinds to −9…−10.
   **The retard is what turns the 1620 peak down** — RPM falls ~330 while `Idle air %` barely moves
   (40 → 36.5). Air-PID output fits **2 %/° × (angle − 18°) + integral** in both polarities
   (`idleAirFlowKP` = 2048 raw/1024 = 2 %/°), re-confirming the slave-on-ignition-angle-error
   architecture from the log alone. In the twin, the pegged negative pair then drove a **second,
   deeper dip** (1662 → 1155, 45 below target) before recovering — the underdamped version of the
   same phase.
5. **The settle is structurally high and glacial.** Warm open-loop base =
   `idleActiveAirflow`[1200 target, hot col] 27 % + `idleCoolantFanCorr` 13 + custom corr ~+3
   ≈ **43 %**, vs the measured hot-oil warm-idle need of ~28–33 %
   ([oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md)) — the deliberate open-loop-
   guarantee margin. The PID must hold **−10…−12** continuously; with `idleAirFlowIntegralLimitMin`
   = −4 the P-term (2 %/° on angle error) must supply the remainder, which **requires a standing
   angle error**: equilibrium lands at angle ~14–15.5° (not the 18° `idleIgnitionTargetTbl` hot
   value), ign corr −2.5…−4, and **RPM +30…+90 above target** (the ign PID only holds retard while
   RPM error is positive). Whole-log steady stats (346 s of state-2 / target-1200 samples): median
   RPM **1231**, air PID **−8.0** (p10 −12.75), ign corr **−2.5**, angle 15.5°, `Idle air %` 36,
   MAP 37. Model closes: (15.5−18)×2 + (−4) ≈ −9; at the −12 extreme, (14−18)×2 + (−4) = −12. ✓
   Every idle entry restarts this travel from 0 (the PID zeroes outside state 2), so the posture
   re-accrues on every single return to idle.

**Chronicity:** ~40 decel entries into state 2 this drive. Ordinary hot decels floor at 1100–1330;
harder decels (−900…−1700 rpm/s) or low entries floored at 570–1150. Entry PID excursions to −9…−11
within 6 s are the norm, and settle-above-target is the norm (median +31 rpm).

**Open items / unverified:**
- ~~The entry-airflow ledger does not close against the Aug-16 XML~~ — **resolved (owner, same
  day): the live `idleActiveAirflow` 1500-target row (hot) read 43**, an un-exported Aug-21 edit
  (Aug-16 XML had 34.5). Ledger closes exactly: 43 + fan 13 + custom ~4 ≈ 60 ✓ observed 60.5.
  No enter-mode kick exists. **Owner edit applied in response: 1500 row 43 → 37**, sized from the
  measured hold at 1500 hot ≈ 50 % *total* (37 + 13 = 50); entry total becomes ~54, flip step
  +20 → ~+13.5 before any armed shaping. Check the 1375 row too — the settle back-calc (base ≈ 30
  vs Aug-16's 27) hints the traverse rows below 1500 were also nudged in the Aug-21 edits; keep the
  1500→1375→1200 walk-down monotone toward hold values (the 1200-region margin stays, per the
  standing cold-oil rule).
- ~~`idleRAMPDownDecayRate` display scale~~ — **resolved (owner, same day):** the live revision at
  log date carried **250 rpm/s**; the Aug-16 XML's 700 was stale (changed in a later revision — the
  Aug-21 binary postdates the export). Delivered = configured, 1:1 RPM/s. **Lesson: never benchmark
  a symbol against an export older than the log — confirm the revision in force at log time first.**
  Also strengthens the Aug-21-edits explanation for the entry-airflow ledger gap (at least one idle
  parameter demonstrably changed in that window).
- CLT jitters 96↔109 °C sample-to-sample all drive (~13 °C ADC/sensor noise). Benign here —
  `cltBins8` cols 96/105 hold identical idle values — but worth an eye.
- The err-indexed `idleIgnAngleCorrection` table (+12° at −200 err) demonstrably does **not** apply
  in this config (`idleIgnitionControlType` = 0): at −103 rpm error the correction was +1…+1.5°,
  matching the target-angle PID, not the table. (Supersedes 07-30's use of that table as the
  "ignition ceiling" — the live ceiling is the ±5 integral clamp around the 18° target.)

### Lever evaluation (2026-08-22, same day) — goal: fall to target and hold, no catch-bounce-settle

Frame it as a **rendezvous problem**: three things must arrive at the target together — the falling
RPM, the ramping target, and the air *torque* (command + ~750 ms lag). Today all three miss: the ramp
delivers 250 rpm/s against an engine falling 650–760, the air arrives ~0.75 s after the step, and it
is sized ~1.8–2× the steady need (entry ~60 % vs ~31–33 % hold). The bounce is the surplus air
integrating into speed while the withdrawal runs at ramp/integral speed; the negative PID accrual is
a *symptom* of the bounce, not a cause of the dip (during the drop itself the loops correctly saw
almost no error and added only +1°/+2.6 %).

- **ECUMaster's own doctrine matches the owner's instinct** — help Idle Step 9
  ([docs/emu-black-help/Idle.md](../../docs/emu-black-help/Idle.md)): tune `Ramp down decay rate` +
  `Ramp down delay` so RPM falls **in sync** with the offset ramp; "prevents PID saturation and
  ensures a smooth transition to idle without RPM dipping below the target." **[Corrected same day
  — owner:]** the live revision at log date had the rate at **250 rpm/s**; the Aug-16 XML's 700 was
  stale (700 dates from several revisions ago, originally set to the measured free-rev fall).
  Delivered = configured, 1:1 RPM/s as documented — no anomaly. The consequence stands and
  sharpens: the current 250 runs **~2.6× slower than the engine's measured fall** (650–760 rpm/s
  in this log), which is what delays the pull-down ~0.9 s and lets the bounce grow to 1620.
  **Raising the rate back to ≈ the measured fall (owner proposal: 650, just under the −658/−763
  band) is the Step-9 sync move and the first tune change to make** — descent error ≈ 0 both ways,
  and the retard/air-pull engage at the turn instead of ~0.9 s late. Err on ramp ≤ fall: a ramp
  faster than the fall dives below RPM and retards while the engine is still falling.
- **Raising `idleRAMPDownOffset` alone does not fix the shape — measured.** The two VSS-bumped
  entries in this log activated at ~1770 and still bounced (floors 1415/1370 → peaks 1566/1547).
  The offset's principled role is **lead time**: lead = offset / fall-rate, and it should ≈ the
  ~750 ms air lag so torque arrives as RPM reaches target (at −658 rpm/s, current 350 gives 0.53 s —
  ~0.2 s short, which is the 230-rpm dip). A fixed offset cannot be right for every decel rate
  (lead shrinks as the fall steepens); size for the typical case, accept residual dip at extremes,
  or shape the approach with armed airflow (help: armed values "induce a decrease… not too rapidly…
  enabling a smooth transition"; cost = slower fall on every lift + too-high armed can block entry).
- **Entry airflow magnitude is the bounce's energy source and its origin is the open ledger item.**
  Back-calc: closing it needs `idleActiveAirflow`[top target row, hot col] ≈ 43.5 vs the Aug-16
  XML's 34.5 — check the live table on screen / export current XML. If the row was raised chasing
  the dip, it's boomeranging (more catch air ⇒ bigger bounce). Size the catch near steady need +
  modest margin per the conservative-FF principle; let lead time, not magnitude, close the dip.
- **Bolus anatomy (owner-identified, same day): the big kicker is the fan adder joining at the
  flip.** Of the observed +20 step, only ~+3 is armed-vs-active table difference; **+13 is
  `idleCoolantFanCorr` and ~+4 the custom correction — both active-state-only, so they arrive as a
  step at activation** (armed displayed exactly the table 40.5, confirming neither applies in
  armed). The fan air is compensating a *real* load that is already present during the armed coast
  (fan on at hot CLT) — armed runs uncompensated against it, steepening the fall AND setting up the
  step. **Fix direction (owner): shape the armed table to feather that air in before the flip** —
  the OEM dashpot pattern, and K&N §5.2.2's pre-position-the-feedforward heuristic. Mechanics:
  `idleArmedAirFlow` is firmware-fixed 8×1 on `idleRPMBins` — bins can be **re-spaced, not added**
  (e.g. cluster ~1500–2200, top bin raised so a 2200+ let-off doesn't clamp; keep 1–2 low-RPM
  anchor bins as the gate-blocked-descent safety net; `idleInactiveAirFlow` shares the axis but is
  inert on DBW). Taper lands just below the active-entry total. **Hang rule:** armed at the
  threshold-adjacent bin must stay clearly below the hold-torque airflow at that RPM (hot hold at
  ~1500 ≈ 51–52 % incl. fan) or RPM hangs above the threshold and idle never activates (explicit
  help-file warning); the gentle-vs-hang gap is only a few %, so step in and watch. Consistent with
  07-30's rules: decel bins not lowered (cold-oil margin intact), and the raise is bounded +
  near-threshold only. **Coupling/sequence:** shaping the approach lowers the arrival fall rate, so
  re-tune in this order — shape armed → re-measure the fall from a log → set ramp ≈ new fall →
  size offset as lead time. Sizing the ramp to the unshaped −658/−763 and then shaping armed leaves
  the ramp faster than the fall (retards during descent). And the taper's top end depends on the
  entry total — confirm the active-table cell / current XML first.
- **Deficit sizing (owner + same-day math): do NOT close the armed→entry gap to zero.** Armed =
  entry ≈ hold at the threshold RPM means zero torque deficit → RPM hangs above the threshold and
  idle never activates. The deficit IS the descent-rate knob: from this log, a ~10–12-point deficit
  produced −658 rpm/s, so ≈ **55–65 rpm/s per point of deficit** near the threshold (linearized —
  refine with a two-point measurement on the next log). Worked sizing at hold(1500) = 50 total
  (owner-measured), entry ≈ 54: armed(threshold bin) ≈ **47–48** → fall ≈ 250 rpm/s, flip step ≈ +6
  (mostly fan comp for an already-present load); armed ≥ 50 → crawl/hang (the cliff is 2–3 points
  away — step in). A flat raised value across the upper bins **self-tapers**: hold grows with RPM,
  so the same armed value gives a bigger deficit at 2200 (brisk fall) shrinking toward 1600 (gentle
  arrival). **Convergence:** at a ~250 rpm/s approach the existing ramp rate (250) already satisfies
  Step-9 sync with no change, and lead = offset/rate = 350/250 = 1.4 s > the ~0.75 s air lag — the
  offset likely needs no change either. The two table edits (1500 row 43→37 + armed taper) may be
  the entire geometry fix. Size the deficit against the custom correction's high side (+1…+6) so
  rich-corr entries don't tip into hang.
- **Custom correction identity (owner-confirmed, same day): it is now the oil-pressure-indexed
  correction** — the viscosity adder's v2 home (the May CAT heat-soak axis was re-purposed;
  `idleCustomCorrX` bins decode to an oil-pressure axis). It is active-state-only, so it joins at
  the flip. **Offset benefit #3 (owner):** a larger `idleRAMPDownOffset` brings this correction
  in-loop earlier, compensating the cold-vs-hot-oil descent difference before the landing zone —
  with the documented caveat that at 1700–2200 rpm the pressure signal is pump-speed-inflated
  (P ∝ μ·N), so the corr's descent-phase *value* mostly tracks falling RPM (a small deterministic
  air-withdrawal on every approach, absorbed by the ramp/deficit cal); the true viscosity
  information is the cold-vs-hot offset between pressure curves at equal RPM.
- **Offset moved 350 → 500 (owner, same day): threshold 1700 hot (~1900 rolling with the VSS +200
  bump; ~2000 cold at the 1500 cold target). This relocates — not repeals — the hang rule.** Hang
  is an *open-loop* failure (zero deficit in armed, nothing else to push RPM down), so it now
  applies only to bins **above 1700** — the 1714 bin is the critical one (stay a few points under
  hold there). Below 1700 the armed table is no longer consulted in normal operation, so armed
  values meeting hold at ~1500 are safe — and as safety-net values for gate-blocked descents
  they're a bonus (survivable air where `died_hot` had none). New numbers: fall through the 1700s
  at a 3–4-pt deficit ≈ 200–250 rpm/s → lead = 500/~225 ≈ **2.2 s vs the 0.75 s air lag**;
  glide 1700→1200 at the matched ~250 rpm/s ≈ 2.0 s/stop.
  **Watch-items for the verification log:** (1) the 1700→1500 stretch runs on the clamped 1500
  target row (base ≈ 37 + fan + oil-corr ≈ 53–57 vs hold 52–54 there — near-zero open-loop
  margin): if the *natural* fall stalls there, the ramp pulls ahead of the engine and retard
  drifts in — that drift is the **mismatch signature, not a control strategy**; remedy is air-side
  (trim the 1500 row / adders so open-loop air stays slightly under hold through the window), then
  re-measure and re-match the ramp; (2) rolling lifts now flip active almost immediately
  (threshold ~1900) — source of any early-grab feel. Prediction: flip ~1700, step ≤ +8, no
  sub-1200 undershoot, RPM and ramp descending together with the loops near zero (retard beyond
  ~−1° through the glide = mismatch); settle still parks +30–90 high (structural, oil-temp
  plan's job).
- **The ramp is a MODEL of the engine's natural fall, not a command trajectory (owner, same day —
  design principle).** Its sole job is holding PID error ≈ 0 through entry so neither loop
  accumulates. The descent rate is set by the *air physics* — armed deficit above the threshold,
  base-vs-hold margin along the in-range walk-down — and the ramp is then **re-matched to the
  measured fall** after any air change. Never set the ramp faster than the natural fall to
  "command" a quicker glide: the loops chase it with retard/air-pull, accumulating exactly the
  negative state the sync exists to prevent, and land in the droop posture. Mismatch charges the
  PIDs in either direction (slower ramp → the moviedrive bounce-cross accrual; faster ramp →
  retard-chased descent, negative integrals at touchdown). If the descent is wrong somewhere, fix
  the air, re-measure, re-match. *(Supersedes the same-day "ramp rate is the knob for glide feel /
  a closed loop can track a faster ramp" lines — that framing was backwards.)*
  **Why the active table is target-indexed — the walk-down is self-following:** with rows
  calibrated at hold(T) (the help's own Step-5/6 procedure), base = hold(ramped target) while
  RPM > target, and since hold rises with RPM the engine carries a deficit ∝ (RPM − T)
  automatically — the in-range descent motor, loops quiet, no extra margin needed. It breaks only
  where the *total* (row + fan + oil-corr, the latter pump-speed-inflated during descent) exceeds
  hold(RPM) — e.g. the clamped 1500-row window — and retard drift is the signature.
- **Size armed against HOLD, not against the entry total or the "gap" — the flip step is a
  residue, not the control variable.** Live example (owner, same day): a "cover the 22-point gap,
  −6 from the base cell, +10 to armed" plan lands armed at 50.5 — *above* the owner-measured hold
  (50 at 1500) → deficit ~0–1.5 → the crawl/hang being avoided. (The 22 also counted +2.5 of PID
  transient in the log's 62 peak; the command step was 20.) Hold-anchored sizing: armed(threshold
  bin) = hold − 2…4 points; the entry−armed step then falls out (~6.5 here). Approach the cliff
  from below, one point at a time.
- **The armed table owns the throttle plate at ALL RPM on this car** — `overrunDBWOverride` = 0
  (Aug-16 XML), so the overrun strategy's `overrunDBW/2` tables are disabled and overrun takes only
  fuel + ignition above `overrunRPMActive`; the plate follows armed on every closed-pedal decel.
  Above the top `idleRPMBins` bin the lookup **clamps to the top-bin value**, which therefore serves
  every higher-RPM lift. ⇒ Apply the dashpot raise as a taper in the approach bins only and keep
  the top bin at the engine-braking value — a global raise would soften engine braking at every
  RPM. (Axis-span convention on other builds unverifiable: FJ80/bradley folders hold only binary
  `.emub3` — would need XML exports to compare.)
- **Ignition attack is the damper, second in order.** K&N §5.2: the D-channel belongs on ignition
  (<1 cycle response; ~50–80 rpm per cycle authority; ~±5° effective range — exactly the
  `idleIgnitionIntegralLimitMin/Max` clamp). Today's attack: Kp 10 raw ≈ 0.01 °/rpm peaked −4.5°
  late in the bounce. Options: raise ign Kp; add ign Kd (engages at the turn, before error grows);
  or `idleIgnitionControlType` → correction-table mode = scheduled high-gain P (±10–12° via
  `idleErrBins`/`idleIgnAngleCorrection`, clamped by the min/max torque tables; integral action then
  lives in the air slave, so it still centers). Mind the coupling: every 1° of correction moves the
  air P by 2 %/° (`idleAirFlowKP` 2048/1024), and air gains already run ~1.24× hot from the
  never-applied range rescale — sharpen ignition only after the trajectory/feedforward geometry is
  fixed (help doctrine: base tables carry idle *without* PIDs; PIDs are for disturbances).
- **Do NOT widen `idleAirFlowIntegralLimitMin` to fix the +30–90 high park.** Arithmetic: the air
  P-term is bounded ±10 % (2 %/° × the ±5° angle-error window), so with the integral parked at −12
  a fresh sag could command at most 10 − 12 = **−2 % net** until the integral unwinds at
  ~KI-limited rate (0.2 %/(°·s)) — reinstating the windup-purge-stall the −4 floor was set to
  prevent. The standing −10…−12 must shrink **at the source** instead: the oil-temp-scheduled base
  plan (§2026-07-30, sensor on order) drops warm base to ~need, the standing trim falls inside the
  −4 floor, and idle centers at 1200 with catch authority intact. Until then the high park is the
  price of the cold-oil margin.
- Benchmarks for "what good looks like" (corpus): K&N §5.2 — a well-tuned idle loop dips
  ~100–150 rpm on a load step and recovers in 2–3 s via air; Bosch p.224 — air channel is the
  gradual/integral path, ignition the fast one. Nothing online will supply per-engine PID numbers;
  the sync procedure (Step 9) + measured plant constants (fall rate, ~750 ms lag, 2 %/° coupling)
  *are* the benchmark method.

## 2026-08-22b — `variousbjjdrive.csv`: the ignition advance-at-dip is the bounce motor; armed taper hangs at 1750–1850; every ramp tried outruns the in-range fall

Source log: `variousbjjdrive.csv` (2026-08-22 11:20, 26.4 min, 16-ch incl. **Gear**; CLT 40→122,
oil pressure 7.7→2.8 bar across the drive — a full cold→warm-oil sweep). **No XML export post-dates
the edits; all config below is log-inferred.** The log contains mid-drive config churn (owner,
non-systematic): threshold mostly **1700** (offset 500 ✓), one era displaying 1900/2000 (VSS-bump
/ elevated-target entries); measured ramp eras ≈ **−350** (t≈170–1180), then **−650 / −250 / −450 /
−650**; the **ignition-PID change (max-torque 35°, Kp/Ki ×10) lands mid-log ≈ t 1000–1084** — ign
corr range jumps from ±2.5 to **+17/−8** (= 35/10° torque-table clamps around the 18° target) and
the air PID starts railing **−20…+25** (+25 = OutMax clamp, −20 = 2 %/° × −8 angle err + integral).

**H1 cascade — CONFIRMED.** The loops are master/slave: ign PID (RPM err → angle), air PID
(angle err → air, 2 %/°). The ×10 ignition gains therefore multiplied the *whole* RPM→air chain
~×10 without touching an air gain; the air channel now slams rail-to-rail (−20 fits 2×(−8)+I
exactly). The perceived "PID updating faster" is cascade slew — the loop *rate* is unchanged
(~40 ms, per the 07-17 measurement).

**H5 bounce driver — CONFIRMED, and it survived the era change.** Across warm entries,
**corr(bounce, advance-at-dip) = 0.78 (old ign) / 0.77 (new ign)** — the strongest predictor in
both eras; corr with gross ramp mismatch ≈ 0.1. The ×10 gains scaled the same mechanism:
**median bounce 29 rpm (old) → 128 rpm (new)**; advance-pegged entries (+13…+17° kicks at the
floor) median 170. The dip-bottom advance is a torque bolus fired exactly at the turn — the air
bolus was traded for an ignition bolus.

**H3 armed-deficit map — the requested table (state 1, neutral, t>400; fall = median dRPM/dt;
armed table may have been edited mid-log — treat cold-oil rows as an earlier revision):**

| RPM bin | armed Air % | fall (rpm/s) | MAP | n | |
|---|---|---|---|---|---|
| 2200 | 49.5 | −738 | 27 | 28 | warm oil (<4 bar) |
| 2100 | 49.5 | −663 | 25 | 32 | |
| 2000 | 49.5 | −600 | 27 | 35 | |
| 1900 | 54.0 | −363 | 29 | 64 | |
| **1800** | **57.0** | **0** | 33 | **345** | **hang** |
| **1700** | **54.0** | **−25** | 33 | **737** | **hang/dribble** |
| 1500 | 48.0 | 0 | 33 | 381 | sub-threshold (armed only when gate-blocked) |
| cold oil ≥4 bar: 2400 49.5/−375 · 2300 51.5/−500 · 2200 55.5/−288 · 1700 64.5/−25 | | | | | |

⇒ **hold(1750–1850, neutral, warm) ≈ 54–57 armed-% — the taper peak equals hold ~100 rpm above
the 1700 gate.** "Armed can't come up any more" is quantified: margin is already ZERO at
1750–1850; the engine dwells there (n=345/737 samples) and dribbles across at −25 rpm/s.
**The hang zone is also an inconsistency machine:** gentle approaches stall above the gate and
enter with ~no error (nice re-entries); hard decels punch through with a large error → advance
kick → bounce. Lever: **reduce the Armed state air flow values at the 1700–1850 bins** — this is
help Step 8 verbatim ("If RPMs are not dropping as expected and the idle controller remains in
Armed state, reduce values in the Armed state airflow table").

> **⚠ RETRACTED same day — "or raise the activation point above the stuck band" is refuted by this
> log.** Measured armed fall by band (warm, neutral): **1650–1750 = −25 rpm/s, 1850–1950 = −250,
> 1950–2100 = −375.** So a higher activation point moves entry into a *faster-falling* region:
> entries at ≥1900 have median bounce **153** and advance-at-dip **+3.5°**, vs **62** and **−1.0°**
> at ~1700 (n=6 vs 36; within the new-gain era, 294 vs 127). The slow band is what *delivers the
> engine to the activation point gently* — which is precisely the Armed table's documented purpose
> ("induce a decrease in engine speed, but not too rapidly… enabling a smooth transition to idle").
> **The real trade: reducing those bins buys a faster drop and costs a harsher entry — so it must
> be paired with an Ignition PID gain reduction, or the arriving speed is converted straight into
> advance and bounce.**

**The VSS idle-target increase (`idleIncreaseTargetAboveVSS` 50 / `idleAboveVSSTargetIncrease`
200) — data cannot convict it; n=3.** Only 3 entries in the log had the increase live (identified
by the ramp settling at 1400 rather than 1200): bounces 74 / 127 / 462. The other elevated-
threshold entries came from the owner's *offset* experiments (settle 1200 with 700 and 800 gaps),
so the two effects are confounded. It governs a settled idle for only **14.4 s of 887 s** of ACTIVE
time — its real footprint is a second activation point, not a raised cruising idle. Verdict:
removing it eliminates one source of entry-to-entry variation and matches the standing
fewer-scheduled-variables preference, **but it is not the fix, and today it is mildly protective**
(it lifts those entries over the stuck band). Remove it *together with* the Armed-table reduction,
not before.

**H4 in-range fall — every ramp tried outruns it.** During state-2 descent (target >1215):
ramp−350/old-ign era: ign corr med −1.0, RPM−target med **+99**; ramp−250/new: corr med −7.5
(pegged −8), air PID −15.8, RPM−target +90; ramp−450/new: corr rail-to-rail [−8,+4.3], med 0.
**RPM rides ~+90–100 above the ramping target in every era — the in-range natural fall is slower
than every decay rate tried, so retard powers the descent** (the exact ramp-outruns-fall failure).
Cause per the walk-down model: the in-range *total* (row + fan 13 + pump-inflated oil-corr) sits
at/above hold(RPM), so the natural fall ≈ 0 and any ramp pulls ahead. Air-side fix territory, plus
a slower ramp than the armed-phase fall for the in-range portion — the two phases now have very
different natural rates (armed −600 up high vs ≈0 in-range), which a single linear ramp cannot
model; landing the in-range total slightly under hold is what makes a single rate feasible.

**H2 inconsistency — answered.** What is changing between re-entries: (1) the dip-bottom error —
set by entry decel × that era's ramp × whether the approach stalled in the hang zone — which sets
the advance kick (r≈0.78 → bounce); (2) the mid-log config churn itself (ign era, four ramp eras,
threshold era); (3) gear: in-gear descents (Gear ≥1) bounce least (driveline damping, old era
bounces 0–29); neutral hard-decels bounce most. Best landing of the log: t=1222.8 — fall −732 vs
ramp −650 (matched), advance never fired (corr ≤ −1), **bounce 13 rpm** — the geometry thesis
working even with hot gains.

Cold-oil note: early-era falls are much faster at equal armed air (−806…−1129 at entry) — cold-oil
FMEP adds deficit; the hang zone is a warm-oil phenomenon (cold oil provides its own margin).

### Armed state air flow — measured properly (2026-08-22c, corrected)

> **⚠ The first pass at this section was wrong and is struck.** It read "the Armed state air flow
> table" as the median `Idle air %` per RPM bin pooled over the whole log — but **the owner was
> editing the table live throughout the drive**, so those medians blended table versions. Retracted:
> the claimed table shape (a hump peaking 57 @1800), the hold points (48/54.5/57), the ~45 rpm/s
> sensitivity, and the proposed flat-52 table built on them. **Rule: `Idle air %` in ARMED is a
> faithful record of what was *commanded*, but it is only evidence of *table contents* within a
> window where the table did not change — verify stationarity before reading a table out of a log.**

**Live-edit history, read from `Idle air %` in ARMED per window** (bin-centred ±60 rpm; the owner's
screenshot of the final table is the last row):

| window | 1571 | 1714 | 1857 | 2000 |
|---|---|---|---|---|
| t0–200 | . | . | 49.5 | 50.0 |
| t200–400 | . | 54.5 | 54.5 | 55.0 |
| t400–600 | . | 59.5 | 59.5 | 60.0 |
| t600–800 | . | 64.5 | 62.2 | 60.5 |
| t800–1000 | . | 53.0 | 57.0 | 54.0 |
| t1000–1200 | . | 48.5 | 50.5 | 51.0 |
| t1200–1400 | 48.0 | 48.5 | 48.5 | 49.0 |
| t1400–1583 | . | 53.5 | 53.5 | 54.0 |
| **owner screenshot (final)** | **48.5** | **48.5** | **49.0** | **49.5** |

**Corrections apply in ACTIVE only — the coolant-fan adder is NOT in ARMED (measured).**
`moviedrive.csv`, ARMED at RPM ≥ 1600 across CLT 41–116 (fan certainly on for part of that):
commanded `Idle air %` = **40.5, min 40.0 / max 40.5** — exactly the Aug-16 Armed table's 40.5 with
**zero** spread. Meanwhile ACTIVE at a settled 1200 target: open-loop base (`Idle air %` minus
`Idle PID air % correction`) = **44.0** against an Active state air flow hot cell of **27.0** — a
17-point gap that accommodates `idleCoolantFanCorr` 13 + Custom ~1. ⇒ **the fan correction is the
handoff step**, and it cannot be cancelled from the ARMED side (see the trap below).

**Fall rate vs commanded Airflow %, RPM 1600–1800, warm, ARMED** — pooling both logs spans the
range because the old table ran much lower:

| commanded Airflow % | measured fall (rpm/s) | source |
|---|---|---|
| 40 | **−259** | `moviedrive` (n=184) |
| 48 | −17 | `variousbjj` neutral (n=71) |
| 53 / 54 / 57 / 58 / 60 / 64 | +5 / −5 / −9 / +2 / −11 / +2 | `variousbjj` neutral (n=17–222 each) |

⇒ **hold(1600–1800) ≈ 47.5** and **sensitivity ≈ 30 rpm/s per Airflow % point**. Self-consistent:
the model predicts 40 → −(47.5−40)×30 = −225 against −259 measured. Above ~50 the curve is flat —
extra air buys nothing but hang, which is exactly the owner's "can't come up any more."

**Consequence — the owner's table is ~1 point above hold at the activation point, so it parks.**
To choose an arrival rate at the gate: `Airflow % = 47.5 − (desired fall)/30`.
−100 rpm/s → **44**; −150 → **42.5**; −250 → **40** (what the old table delivered).

**⚠ The trap that produced this:** raising Armed values to shrink the ARMED→ACTIVE step can never
work, because the step is the fan + Custom corrections joining, and Armed hits hold before it can
reach them. **Close the step from the ACTIVE side** — set Active state air flow so
`cell + fan + Custom ≈ hold at that target RPM`. Hold reference points: **hold(1231) ≈ 36 total**
(settled `Idle air %`, `moviedrive`) and **hold(1600–1800) ≈ 47.5** ⇒ ≈ **+2.45 points per 100 rpm**,
so **hold(1500) ≈ 42.5 total**, i.e. a 1500-target cell of roughly `42.5 − 13 − Custom`. The owner's
working figure of 50 total to hold 1500 (hence a cell of 37) looks ~7 points high by this
measurement — worth re-checking on the car before trusting either number.

**Design rule — flatten the approach, don't feather it.** Two constraints force this:
1. **The lag makes shaped tapers unreliable.** Airflow changes take ~0.75 s to become torque; at
   −600 rpm/s that is 450 rpm of lead, so a value set at 1800 governs behavior far below the
   activation point. **A flat command through the approach has nothing to lag behind** — the plate
   is already where it needs to be when RPM arrives.
2. **No bin between the activation point and ~2000 may exceed hold at the *activation point***
   (not hold at its own RPM), because lag leaks high-RPM values downward. Ceiling ≈ hold(1700)
   − margin.
A flat value self-tapers: hold rises ~3.5/100 rpm, so the deficit grows on its own with RPM —
brisk fall up high, gentle at the gate, no shape to get wrong.

**Proposed table** (8 bins, warm; `idleRPMBins` re-spaced — count is firmware-fixed). Values follow
`47.5 − fall/30` at the gate; the 1857/2000 bins are left near the owner's current numbers because
the 1800–2000 measurement is confounded (fall there varies strongly with position inside the band):

| bin (rpm) | Airflow % | basis | expected fall |
|---|---|---|---|
| 1200 | 34 | ~hold(1200) 36 − 2 — drifts down slowly rather than dying if activation is ever blocked | ~ −60 |
| 1450 | 40 | ~hold(1450) 42 − 2 | ~ −60 |
| 1700 | 44 | measured hold 47.5 − 3.5 | **≈ −105** |
| 1850 | 44 | flat — a constant command has no change for the ~0.75 s air lag to trail | ≈ −180 |
| 2000 | 45 | | ≈ −300 |
| 2200 | 47 | | brisk |
| 2500 | 49.5 | unchanged from owner's table | strong |
| 3000 | 49.5 | top bin — clamps for all higher lifts | strong |

Verification: one neutral coast; check fall at 1900/1800/1700 ≈ −450/−225/−110. Still parking near
1700 ⇒ drop the flat value 1–2 points; arriving hard ⇒ raise 1. **Must be paired with the Ignition
PID kP reduction** (owner: 0.1 → 0.05 °/rpm) or a faster arrival converts to advance and overshoot.
No CLT axis on this table — cold falls faster at equal Airflow % (early-log cold entries −806…−1129
vs −600 warm), and a cold Idle target moves the activation point, so cold behavior differs by design.

**"The 40→60 jump was just a blip" — confirmed, median across entries:**

| | before ×10 (`moviedrive`) | after ×10 (`variousbjj`) |
|---|---|---|
| peak Idle air % above the ARMED value | **+18** | **+5** |
| time to fall back below the ARMED value | **1.08 s** | **0.40 s** |
| Idle PID airflow % correction trough (3 s) | −7.6 | **−16.0** |

The Active-state base still steps up at handoff; the Airflow PID now cancels it in ~0.4 s because
the ignition angle swings ten times further off Target ign. angle for the same RPM error.

### Deleting `idleCoolantFanCorr` — endorsed (owner proposal 2026-08-22c), and it fixes the standing-error posture

Owner: *"I can also just get rid of the coolant fan correction and let PID handle it. Coolant fan is
basically always on, and the failure mode is being over-aired. Which is fine."* Correct on all three
counts, and the integral-limit arithmetic makes it the **primary** fix for idle settling above target
with retard held.

**The asymmetric integral limits are the key.** `idleAirFlowIntegralLimitMin` = **−4**,
`idleAirFlowIntegralLimitMax` = **+12** (Aug-16 XML). The loop can therefore carry a large *positive*
standing correction inside its integrator, but only −4 of negative. **So the open-loop base must be
set slightly LOW, never high.** Measured today (settled 1200 target, hot, `moviedrive`): open-loop
base **44.0** (= Active cell 27 + fan 13 + Custom ~4) against a measured need of **36** ⇒ standing
correction **−8**. That exceeds the −4 integral floor, so the P-term must supply the rest — and since
the Airflow PID's P-term acts on *ignition-angle error* (2 %/°), a standing −4 of P demands a
standing −2° of angle, which the Ignition PID only holds while RPM is **above** target. **That chain
is why idle parks +30–90 rpm high with a few degrees pulled: it is a base-too-high artifact, not a
tuning defect in either PID.**

Delete the fan adder and base becomes **31** against a need of **36** ⇒ standing correction **+5**,
which fits inside the +12 integral cap with room to spare. The integrator carries it, P goes to ~0,
angle error → 0, ignition correction → 0, and **RPM can sit on target**.

Secondary benefit: the ARMED→ACTIVE step largely disappears. ACTIVE at handoff becomes
(1500-row cell + Custom) ≈ 41 against an Armed value of ~44 at 1700 — a step of about **−3**, so the
engine keeps decelerating into ACTIVE instead of receiving a surplus. The step that started this
whole investigation was the fan adder joining, and this removes it at the source.

**Doctrinally supported:** the EMU help's own example of what the idle PIDs are for is
"engine load (e.g. when the rear window defroster or **radiator fan** is activated)."

**⚠ The one real cost — the fan-kick transient, and it reverses a prior decision.** The correction's
genuine job is the *moment the fan engages* (CLT crossing `coolantFanActTemp` 70, or VSS falling back
under `coolantFanVSSOff` 80), where ~13 points of load arrive in one step with no feed-forward to
meet them; the loops must now cover it, and the Ignition PID (fast, ±5° of integral authority) is
what absorbs the first second. This supersedes the earlier "keep `idleCoolantFanCorr` = 13 to
eliminate the fan-kick dip" position — the trade is now judged worthwhile because the standing-error
cost is continuous while the kick is once per drive. **Watch a warmup log through the CLT-70
crossing** and confirm the dip is acceptable; if not, the middle path is to keep a *smaller* adder
(enough to blunt the kick, small enough to leave the standing correction positive).

Cold behavior is unaffected: below CLT 70 the fan output is off, so the correction was never applied
there and the cold columns of Active state air flow already stand alone.

### ⚠ The Armed table and the Ramp down offset are coupled through the settling RPM (2026-08-22c)

With a flat-ish Armed value the engine **coasts down onto the RPM where hold equals the command**
and stops there. Call that the settling RPM. Two consequences:

- **The settling RPM must sit meaningfully below the activation point**, or the engine asymptotes
  onto the gate and parks (never entering ACTIVE) — the same failure as commanding at hold, arrived
  at from a different direction. Rule of thumb: **settling RPM ≈ 150 rpm below the gate.**
- **Changing the offset therefore forces a rescale of the Armed table.** Owner moved the offset
  **500 → 350** (gate 1200 + 350 = **1550** warm), keeping the decay rate at 650. The table proposed
  for the 1700 gate (flat ~44, settling ~1557) would settle *exactly on* the new gate. Every
  approach-region value must drop ~3.5–4 points: **flat ~40, settling ≈ 1394.**

Approach dynamics under a flat command: `fall ≈ 0.735 × (RPM − settling RPM)` (from the measured
30 rpm/s per point × 2.45 points per 100 rpm), an exponential approach with **τ ≈ 1.36 s**.

**Revised table for the 1550 gate** (same method, `Airflow % = hold − fall/30`):

| bin (rpm) | Airflow % | predicted fall |
|---|---|---|
| 1100 | 32.0 | ~0 (at hold — parks, won't die if activation is blocked) |
| 1300 | 37.0 | ~0 |
| 1500 | 40.0 | −78 |
| 1700 | 40.0 | −225 |
| 1900 | 40.5 | −357 |
| 2200 | 42.0 | −533 |
| 2600 | 45.0 | −735 |
| 3000 | 47.0 | −972 |

At the 1550 gate this interpolates to 40.0, arriving ≈ **−114 rpm/s**. Note this lands very close to
the **pre-raise table** (`moviedrive` ran flat 40.5 above 1571 at a 350 offset) — that table was
correctly sized for this offset; raising it was what produced the parking.

**⚠ Model accuracy falls off above ~1800.** Measured falls at 2000–2600 run **1.8–2.4× faster** than
this model predicts (the engine passes through quickly there, so those samples are transient, not
settled). Real entries will arrive at the gate faster than tabulated — treat the top four bins as
shape, not prediction, and read the actual arrival off a log.

**Decay rate 650 vs the natural fall — expect the PIDs to lead, not track.** Near idle the
airflow-driven descent is bounded by the relation above: at the gate it is ~110 rpm/s, and even with
the Active cells set ~5 under hold (the positive-standing-correction posture) the natural rate is
only ~150–250 rpm/s in the 1500–1700 region. A 650 rpm/s ramp therefore **outruns the engine**: the
target reaches 1200 in ~0.5 s while RPM needs 2–3 s, so the Ignition PID retards and the Airflow PID
pulls to drive the descent — the ramp-faster-than-fall case. **Upside:** with the target already
parked at the floor, RPM approaches 1200 from above and never crosses the ramp, so the
crossing-and-whipsaw mechanism behind the overshoot is eliminated. **Risk:** arriving with a
wound-down correction (bounded by `idleAirFlowIntegralLimitMin` −4) and retard held through the
whole glide. **Read it off the log:** if `Idle ignition correction` sits at several degrees of retard
the entire way down, the ramp is outrunning the engine; matching it to the measured fall
(~150–250 in this region) is the Step-9 fix, at the cost of a longer glide.

### ⚠⚠ CORRECTION — the hold curve below 1600 was wrong; owner's fan test wins (2026-08-22c)

Owner challenged "Active state air flow needs no increase" against his own **fan-activation tests
measuring the fan load at right on 13 % airflow**. He is right; my hold curve was unsound.

**Why my ARMED-derived hold(1600–1800) ≈ 47.5 is not a hold measurement.** The fall-vs-airflow
table showed 53 → +5, 57 → −9, 60 → −11, **64 → +2** — i.e. no trend at all from 53 to 64. If hold
really were 47.5, a command of 64 is a 16-point surplus and the engine would accelerate ~+500 rpm/s;
it did not. **Those samples are a mixture of conditions each sitting at its own equilibrium** (fan
on/off — `coolantFanVSSOff` 80 gates it out at speed — plus oil temp and accessory load), so pooling
them produced a fictitious flat region and an artificially low hold. The 40 → −259 and 48 → −17
points are real, but they pin hold **for those samples only**.

**The decisive measurement — settled, hot, ACTIVE, RPM on target (delivered `Idle air %` = hold):**

| RPM | delivered | dwell | source |
|---|---|---|---|
| 1214 | **34.0** | 183 s | moviedrive |
| 1221 | **32.0** | 431 s | variousbjj |
| 1406 | 50.5 | 3.8 s | variousbjj |
| 1418 | 47.5 | 3.3 s | moviedrive |
| 1480 | 56.0 | 3.6 s | moviedrive |
| 1528 | 54.0 | 3.9 s | variousbjj |
| 1673 | 54.0 | 3.7 s | variousbjj |

The 1200-region points are rock solid (hundreds of seconds). The 1400–1700 points are thin (~4 s
each) but four independent ones cluster **47–56**, which **corroborates the owner's bench figure of
~50 to hold 1500** and refutes my interpolated 42.6. Hold therefore rises **~6–8 points per 100 rpm**
between 1200 and 1500, not 2.45 — the curve is steep down low and flattens above ~1500.

**Consequence 1 — the Active table IS over-set, by ~11 at the 1200 row.** Settled: base **44**,
requirement **33** ⇒ the standing −11 correction seen in both logs. `base = cell + Custom + fan 13`
⇒ `cell + Custom` = 31 where it should be 20.

**Consequence 2 — FINAL (owner, 2026-08-22c): delete `idleCoolantFanCorr`, fold the air into the
Active table.** Owner: *"The fan kicks back on WELL ABOVE the idle re-entry region — we're talking
3000 rpm. It's a constant. We don't need to worry about kick-on."* That settles the only remaining
objection: the fan re-engages (VSS falling under `coolantFanVSSOff`) at ~3000 rpm, hundreds of rpm
above any activation point, so it is already on and stable through the entire idle envelope — the
feed-forward has nothing left to feed forward, and the VSS-gated dropout that was **Fault 2** in the
2026-05 write-up never occurs in the idle region either. A "correction" that is always applied is
just a hidden constant; moving it into the table makes all idle air visible in one place.

**⚠ Deleting it does NOT reduce the ARMED→ACTIVE step** (verified twice): the step is
`ACTIVE total − ARMED total`, and ACTIVE total is fixed by what holds the RPM, so relocating 13
points between the correction and the table leaves it unchanged. **The step *is* the armed deficit** —
ARMED sits below hold so the engine descends, ACTIVE sits at hold so it can hold the target — and
driving it to zero means driving the descent to zero (the parking failure). The observed +20 was
pathological only because the 1200 row is ~11 over; corrected, it is ~+12 and harmless. Residual
cost of deleting: on a long high-speed neutral coast with idle ACTIVE the fan is genuinely off, so
the folded-in air over-airs by 13 (owner: acceptable direction).

*(Struck: the previous recommendation to keep the correction and cut the 1200 row — its arithmetic
holds, but the fan-kick and VSS-dropout justifications for keeping it are void per the above.)*

**Superseded reasoning follows.**
Deleting it works at a 1200 target (base 31 vs need 33 ⇒ PID +2) but at an elevated target it fails:
at 1500, base becomes `cell 37 + Custom 4` = 41 against a need of **50–54**, requiring **+9…+13** of
PID — at or past `idleAirFlowIntegralLimitMax` (+12). It also throws away the fan-engagement
feed-forward for no gain. **Recommended instead: keep the fan correction at 13, and lower the hot
cells of the 1200 target row by ~11–13** (leaving a small positive standing correction, which the
asymmetric −4/+12 integral limits want). Then both fan states are correct — fan on: base = need;
fan off: base − 13 = need − 13 — and the standing angle/RPM error goes away, which was the whole
point. *(This supersedes the "Deleting `idleCoolantFanCorr` — endorsed" section above; the
integral-limit reasoning there stands, the arithmetic behind it does not.)*

### FINAL recommended values, 2026-08-22c (supersedes both earlier proposed tables)

Gate-independent by design: one flat Armed value whose settling RPM (**1394**) sits below the lowest
activation point that can occur, so the same table works at every `Idle target + Ramp down offset`
combination (warm 1550/1700, VSS-bumped 1900, cold 2000) — arrival is automatically gentler at low
gates and brisker at high ones.

**Armed state air flow** — bins `1000 1200 1400 1600 1800 2100 2500 3000`,
values **`28.0 33.0 37.0 42.0 42.0 42.0 42.0 42.0`**

Anchored on the two *directly measured* ARMED points at 1600–1800 (**40 → −259 rpm/s**,
**48 → −17**, sensitivity **30 rpm/s per point**) rather than on the discredited hold line: 42 sits
6 under the 48 that parks, giving ≈ **−180 rpm/s** through that band — gentler than the old flat
40.5 (which measured −259 and always crossed) and still nowhere near parking. The two bottom bins
sit at the measured hold (~33 at 1200) as the blocked-activation safety net.

Because 42 is defined against *measured falls* and not an extrapolated hold curve, it is
gate-independent in the way that matters: at every activation point in use (1550 / 1700 / 1900 /
2000) the engine is still descending when it crosses. **Keep `idleRAMPDownOffset` ≥ 350;**
500 recommended.

Companion settings: `idleRAMPDownDecayRate` **650** (owner's; outruns the natural fall, so RPM
approaches the target from above and never crosses the ramp — the overshoot mechanism is removed,
at the cost of retard held through the glide); **`idleCoolantFanCorr` stays 13**; Ignition PID kP
**0.05 °/rpm** (owner's); **Active state air flow — lower the hot cells of the 1200 target row by
~11–13** (measured base 44 vs requirement 33). Rows above 1200 are unmeasured here; the thin
1400–1500 settled points suggest they are roughly correct, so change them only on evidence.

Verification on one neutral coast: RPM keeps falling through the activation point with no plateau
above it, and once settled at 1200 `Idle ignition correction` sits near zero rather than holding
retard, with `Idle PID air % correction` small and positive instead of −11.

## 2026-08-22d — `majorimprovement.csv` + `.xml.emub3`: the structural fix is confirmed working

First log with a **matching same-day tune export** (15:41/15:42), so every value below is read, not
inferred. Applied: `idleCoolantFanCorr` **0**, `idleAboveVSSTargetIncrease` **0**,
`idleIgnitionKP` **51** (= 0.0498 °/rpm), `idleIgnitionKI` **5**, `idleAirPIDOutMin/Max` **±25**,
`idleTargetBins` **1200/1400/1600/1800/2000**, `idleRPMBins` **1000/1200/1600/1800/2000/2300/2600/3000**,
`idleArmedAirFlow` **28/38/44/44/44/44/44/44**, `idleIgnitionMaxTorqueAngleTbl` flat **35°**.
`idleCustomCorrection` is now **oil-pressure indexed** (owner-confirmed, ACTIVE-only): X =
`20 2C 38 44 50` decodes at **1/16 bar per count** → **2.0 / 2.75 / 3.5 / 4.25 / 5.0 bar**,
corrections **0 / +4 / +7 / +10 / +13 %**. At warm idle (oil 2.4–4.3 bar, median 3.38) it runs
**+6**, which is now a load-bearing part of the base.

**Steady warm idle — the standing-error posture is gone.** 155 s of settled samples at a 1200 target:

| | before (moviedrive) | now |
|---|---|---|
| RPM (target 1200) | 1231 (+31) | **1197 (−3)** |
| `Idle PID air % correction` | −8 to −12 | **−0.94** |
| `Idle ignition correction` | −2.5 | **0.00** |
| `Ignition Angle` | 14–15.5 | **18.00 = Target ign. angle** |
| handoff step | +20 | **−1.5** |
| bounce (median) | 128 | **85** |

Base arithmetic closes exactly: Active cell at 1200/hot **27.5** + Custom **+6** + fan **0** = **33.5**
against the measured hold of **33** ⇒ PID ≈ 0. The engine now sits on target with timing at the
target angle and both loops idle — which is the definition of a correctly calibrated open loop.

**Owner's framing, now measurable:** *"the engine WANTS to return to idle normally and in a calm
manner — it's the PID that can screw it up."* ARMED approach with flat 44: fall **−133 / −129 / −121
rpm/s** across 1700–1900 / 1900–2100 / 2100–2400 — essentially **constant −125 rpm/s** the whole way
down, with zero PID involvement. The glide is free; the loops only start fighting in ACTIVE.

**Fault A — the idle limit cycle ("PID wiggle"). Cause: air-loop gain, via the cascade.**
Settled RPM swings p10 1155 / p90 1290 with a **1–2 s period**; **82 %** of the deep-negative air-PID
excursions happen at settled target, not during the descent. The cascade is confirmed numerically:
`airPID = 2.06 × ignCorr − 0.63` (r = 0.984), matching `idleAirFlowKP` 2048/1024 = **2.00 %/°**.
`ignCorr` is anti-correlated with RPM at **zero lag** (r = −0.953) — clean, fast P action, correctly
damping. The destabiliser is the *air* copy of that same signal arriving **~0.75 s late**: an
integrator-like plant with delay T oscillates when loop gain exceeds ~π/2T, and the period predicted
(~3 s) is the right order for the ~1–2 s observed. **Fix = cut `idleAirFlowKP`, not the ignition
gain** — ignition action is fast and stabilising, air action is delayed and destabilising. Suggested
**2048 → 1024 (2.0 → 1.0 %/°)**. Supporting: the gains were never rescaled when the actuator window
widened 4.5 → 5.6 %, so they still run ~1.24× hot (see [airflow_actuator.md](airflow_actuator.md)).

**Fault B — the ACTIVE descent is PID-forced, and that is what remains of the undershoot.**
`idleRAMPDownDecayRate` **650** against a natural fall of **~125–150 rpm/s** — about **5× too fast**.
Consequences measured over the descent phase: RPM − target median **+64** (p90 +264), `ignCorr`
median **−3.0** with p10 **−8.0** *sitting on the min-torque floor*, **34 % of the descent at ≥6° of
retard**, actual fall **−317 rpm/s** (i.e. retard is supplying roughly half the deceleration). That
retard then has to unwind at the bottom, which is exactly the residual undershoot — entry floors
median **1133** against a 1200 target. **Fix = Step 9: slow the ramp toward the natural fall.**
Measured trade ≈ **55 rpm/s of extra deceleration per degree of retard**, so **650 → 250** needs only
~1.5–2° instead of the floor, and drops the 1700→1200 glide to ~2 s. Going all the way to ~150
(fully natural) would take ~4–5 s and is probably slower than wanted.

## Dead ends (this build)

- Raising `idleActiveAirflow` 1000/1100 rows: indexed by idle **target**, which floors at 1200 (`idleRPM` bottoms at 1200), so those rows are never read. The VE table is indexed by actual rpm×MAP, so its 500-rpm row is the live lever.
- `idleIncreaseTargetAboveVSS`: would work but adds a target step — rejected to keep low-speed heat-soak idle clean.

## Feed-forward sizing worked point (this build)

Before the "halve the feed-forward" principle was applied, `idleCustomCorrection` was sized near full steady-state comp at the operating CAT band. PID sat at **−9.75% (saturated negative)** at the worst log point (**t=178.64, `supra/logs/20260526_1644.csv`**) with TPS only **1.1%** above the actuator floor. After converting to scalar mode and halving the corrections, PID has authority both directions and worst-case stall margin grows.


## 2026-08-27 `added features.csv` — geometry fixes confirmed; residual disturbance is the **A/C idle-up releasing**

Source log: `added features.csv` (2026-08-27, 27.5 min, cold start to hot; CLT 29 to 96–113;
17-channel idle capture: RPM, MAP, TPS, CLT, `Engine oil pressure`, `Idle state/target/air %/PID
air %/custom corr/ignition correction/ignition target`, `Ignition Angle`, `Gear`, `AC Clutch`.
No VSS, PPS, clutch-switch or lambda channels). **Idle → Target parameters in force (owner
screenshot, same day):** AC idle increase **500 rpm**; Ramp down max. offset **350**; Ramp down
decay rate **125 rpm/s**; Ramp down delay **0 ms**; Increase target above VSS **3 km/h**; Above VSS
target increase **200**; Clutch pressed target increase **200**; DSG creep 200 / max 1300.

Three owner changes went in around this drive: `idleActiveAirflow` hot 1000-target cell 24.5 → 27;
the **VSS target increase (+200)**; and the **clutch-pressed target increase (+200)**. Per the owner,
the dipping was observed *early* in the drive and the two +200 increases were added in response and
**stopped it** — the timeline below agrees.

### The 08-22d fixes are confirmed live and working

| Item | 08-22d recommendation | Measured here | Status |
|---|---|---|---|
| `idleAirFlowKP` 2048 → 1024 | halve the slave gain | regression `airPID = 0.82 × ignCorr` (r 0.70) over 15 640 hot ACTIVE samples — was **2.06** | applied |
| `idleRAMPDownDecayRate` 650 → 250 | slow the ramp toward the natural fall | dialog reads **125 rpm/s**; measured target ramp **−125 rpm/s** (p25 = p75, n = 2891) | applied, taken past the recommendation |
| natural ARMED fall | ~125–150 rpm/s | **−125** (1500–1800), −150 (1200–1500), −175…−250 (1800–2500); armed air 39.5–44.5 | ramp now ≈ fall — Step-9 sync achieved |
| fan correction removed | 0 | open-loop base reconstructs without it (below) | confirmed |
| Custom corr = oil-pressure indexed | 2.0 bar→0 … 5.0 bar→+13 | log confirms exactly: oilP 2.0 → 0, 3.25 → 5–6, 4.0 → 8, 6.4 → 13 | confirmed |

**The airflow edit is visible in the log.** With fan = 0, open-loop base = `Idle air %` −
`Idle PID air % correction` − `Idle airflow custom corr.`. On stopped hot idle it reads a rock-steady
**24.9–25.6 through t ≈ 930 s, then 26.8–27.1 from t ≈ 960 s on** — the 24.5 → 27 edit, applied
mid-drive. (Standing rule confirmed again: this log contains live tune edits — segment before
pooling.) Effect on the *hold*: none — RPM error stayed ~0 and the airflow PID moved from ≈ 0 to
**−4.7** to trim the extra back out, angle parking ~16.5° against an 18° target. That is the
open-loop guarantee doing its job ([idle_base_airflow_is_open_loop_guarantee]); the +2.5 points buys
catch margin, not idle speed. Do not undo it, and do not expect it to move the tach.

**`Idle air %` is a usable DBW-target proxy (owner's tip, validated here).** Mapping the 2.4–8.0 %
idle authority window onto the 0–100 % airflow command — `DBW ≈ 2.4 + air% × 0.056` — reproduces the
measured plate position: hot ACTIVE implied median **4.11 %** vs logged TPS median **4.00 %**
(p1 3.58 vs 3.50, p99 5.28 vs 6.30). So a reduced log without `DBW target` still shows the commanded
throttle. Two consequences: at settled idle a 3-point airflow move is ≈ 0.17 % throttle — under TPS
log resolution — and TPS drops below the 2.4 % `idleDBWTargetMin` floor on only **14 samples in the
whole drive**, all inside the worst target-step slams (min 1.30 %).

### The dip: the 500-rpm A/C idle-up dropping out mid-ramp

The three deep events in the log are one mechanism, not three. Each begins with the target losing
**exactly ~510 rpm in a single 40 ms sample** while `Idle state` stays 2 — the **AC idle increase
(500)** being withdrawn while the ramp-down is still running:

| t (s) | RPM at the step | target | `AC Clutch` | ign corr | Ignition Angle | `Idle air %` | TPS | floor reached |
|---|---|---|---|---|---|---|---|---|
| 321.80 | 1699 | 1710 → **1200** | **1 → 0** | 0 → **−8.0** | 18 → **10.0** | 49.0 → 35.5 | 6.8 → 5.0 | **558** |
| 419.12 | 1704 | 1825 → **1315** | already 0 | −0.5 → **−8.0** | 23.5 → **10.0** | 52.0 → 36.5 | 7.1 → 5.9 | **616** |
| 577.36 | 1745 | 1843 → **1343** | **1 → 0** | +4.5 → **−8.0** | 22.5 → **10.0** | 49.5 → 34.5 | 6.4 → **1.4** | **682** |

Sequence in every case: instant −510 setpoint step → the Ignition PID (proportional on RPM error,
authority **+17°/−8°** = Max torque 35 − Target 18, Target − Min torque 10) rails to **min torque,
angle 10°** → airflow command drops 13–15 points → torque floor → RPM falls **~500 below target** in
~1.3 s → both loops rail the other way (+17°, angle 35°, airflow PID +12…+14) → recovery overshoot →
1–2 s limit cycle. **Air authority was never the limit** — this is a commanded torque cut answering a
commanded setpoint step, not the old cold-oil/authority failure.

**Attribution:** two of the three coincide exactly with a logged `AC Clutch` 1 → 0 edge. The third
(419.12) has the clutch output already off — EMU applies the idle-up on the A/C **request**, which is
a different signal from the clutch output and is not logged here, so the request can fall away with
the output already low. Nothing else in the Target dialog is worth 500 rpm.

**The A/C compressor short-cycles, so this is a repeating square-wave disturbance.** 86 on-periods in
27 min: median **1.5 s on / 2.1 s off** (p10 on-time 0.1 s), 29 clutch edges landing while
`Idle state` = 2. Across the drive there are **80 in-ACTIVE target steps in the ±500 family**, median
**0.08 s** (two samples) between consecutive flips — 85 % within 0.5 s. Median RPM peak-to-peak in
the 2 s after one: **502 rpm**.

> **Owner, 2026-08-27:** the A/C request can now occur at idle, and it has been **gated in the EMU so
> this disturbance is removed**. Untested at the time of writing — verify on the next drive that a
> compressor cycle at idle produces no target step and no ±500 excursion.

### The +200 increases are the mitigation, not the fault

Timeline of activation floors confirms the owner's account. Before ~t 600 the entry undershoots run
**−492 / −524 / −568** (floors 558 / 616 / 682). After the +200s are in, the same kind of entry
floors at **1063–1614**, median undershoot **−15**, worst −166 excluding the t = 902.8 restart. The
mechanism is direct: the increases raise the *landing* target so the post-step collapse starts from
and ends on a higher number, and the residual error the Ignition PID sees is smaller.

Feedforward keeps up with the raise: open-loop base rises 26.9 → **28.5–29.3** at target 1225/1250
and → 30.2 at 1330, with airflow-PID medians −2 … +2. `idleActiveAirflow` *is* indexed on the raised
target, so the bump is properly fed. **Keep both +200s.**

**Second-order cost, worth knowing:** the ±200 family also steps un-ramped, 129 events, and **87 %
occur with `Gear` = 0** — at or below the speed where the gear calculation gives up. With
`Increase target above VSS` = **3 km/h** the threshold sits inside the speed signal's noise band at
rest, so it toggles at a standstill. Median gap between consecutive flips **0.60 s**.

**Worked example — stationary car, no driver input (t = 984–996, `Gear` 0, TPS pinned 3.7 %).**
Dead-stable 1010–1018 rpm on a 1025 target, ign corr −0.5, airflow PID −3.5. Then:

| t (s) | target | ign corr | Ignition Angle | RPM |
|---|---|---|---|---|
| 985.56 | 1025 | 0.0 | 17.5 | 1014 |
| 985.68 | **1225** (+200) | **+9.5** | **27.5** | 1016 |
| 986.16 | **1025** (−200) | **−3.5** | **15.5** | 1072 |
| 987.36 | **1225** (+200) | **+12.5** | **31.5** | 953 |
| 988.08 | 1225 | +4.5 | 22.0 | 1149 |
| 989.5–990.2 | 1225 | **+17.0 (rail)** | **35.0** | **849 → 883** |
| 990.96 | 1225 | +2.0 | 21.5 | 1200 |

A parked car, **1149 → 849 → 1200** — 350 rpm p2p from two 0.5 s VSS-gate flickers. Median RPM p2p
in the 2 s after a ±200 step is **218** vs **502** for ±500, i.e. roughly linear in step size.

**Fix without giving up the benefit: raise `Increase target above VSS` clear of the standstill noise**
(the increase is wanted for steering effort while rolling, not at 3 km/h), and add hysteresis if the
firmware allows separate rise/fall thresholds. The clutch +200 shows no equivalent chatter in this
log.

### Steady idle is otherwise good

Stopped hot idle, no target step: RPM within ±10 of target, p2p **42–97 rpm**, sd 13–33, period ~1 s,
airflow PID −2 … −5, angle 14.5–18°. TPS pinned flat at 3.6–3.7 % while `Idle air %` moves 3 points —
below plate resolution — so the residual ±25 rpm is **the ignition loop working alone**. Noise floor,
not a fault.


### What a target step actually does — decomposed (owner's framing, measured)

A target increase is primarily **an increase in feedforward airflow**, not a commanded RPM. The
target indexes `idleActiveAirflow`, so raising it raises the open-loop duty; the tach only follows
because the loops then close on the new number. Both halves are real, on different timescales:

- **Steady state, the loops do land RPM on the raised target:** settled hot medians — target 1025 →
  RPM 1027 (FF base 26.7); 1050 → 1051 (25.3); 1225 → 1209 (28.4); 1250 → 1186 (28.6).
- **Transiently, the feedforward move is small and the ignition move is large.** Decomposing the two
  clean −500 A/C steps (`base` = `Idle air %` − PID − custom):

| t (s) | target | FF base | as throttle | airflow PID | ign corr |
|---|---|---|---|---|---|
| 419.12 | 1820 → 1315 | 37.5 → 30.2 (**−7.2 pts**) | **−0.41 %** | +3.5 → −4.8 | **+5.5 → −8.0 (−13.5°)** |
| 577.36 | 1848 → 1343 | 38.8 → 30.2 (**−8.6 pts**) | **−0.48 %** | +3.2 → −4.7 | **+5.0 → −8.0 (−13.0°)** |

At ~30 rpm/s of fall per airflow point (measured ARMED) the feedforward loss is worth ~215–260 rpm/s
and arrives on the ~750 ms air lag; at ~55 rpm/s per degree of retard the ignition swing is worth
~700 rpm/s and arrives immediately. **So the fast, dominant half of the dip is the ignition PID
retarding on the sudden positive RPM error, not the lost feedforward air.** That is why the fix is to
shrink the step, not to add base air.

### A/C: the trigger is the 1700 rpm clutch cut-out, not the refrigerant charge

**Owner-confirmed 2026-08-27: the A/C clutch RPM cut-off is 1700.** The log shows it independently
and unambiguously:

- The clutch is **never engaged below 1669 rpm** anywhere in the drive; lowest RPM with A/C on = 1702;
  **zero seconds of A/C-on time below 1300 rpm.**
- 86 disengage edges: RPM p10 **1713**, median 2435 (the higher ones are wide-open decels blowing
  straight through). 86 engage edges: RPM min **1719**.
- The −500 target steps cluster on the same number: n = 57, p10 **1693**, median **1719**, **67 %
  between 1650 and 1800**. The +500 re-applications: median **1716**.

So the mechanism is complete: in stop-and-go traffic RPM crosses 1700 constantly, and **there is
essentially no hysteresis** (cut at ~1700, re-engage from 1719) — hence 86 cycles in 27 minutes at a
median **1.5 s on / 2.1 s off**, and ±500 target flips a median **0.08 s** apart. Every crossing
withdraws the 500-rpm idle-up, the Ignition PID answers a sudden +500 error by railing to min torque
(angle 10°), and the engine dips. The three deep events are simply the crossings that happened while
the ramp-down was already running.

**⚠ Retraction:** an earlier draft of this section blamed the short-cycling on low refrigerant charge
(low-pressure switch at 196 kPa, [ac_compressor_engagement_oem.md](ac_compressor_engagement_oem.md)).
The RPM evidence rules that out — the cut-outs sit on a sharp 1700 rpm edge, not on a pressure clock.
The charge is genuinely low (owner) and worth topping up, but it is **not** the cause of this
disturbance.

**Fix (owner's, and it is the right one): drop the A/C clutch minimum RPM 1700 → 850.** It removes
the transition rather than shrinking it — at a 1025 target the engine never approaches 850, so the
compressor simply stays engaged through the return to idle and there is no step to answer. It also
deletes the threshold chatter, which is most of the 86 cycles. Three conditions to pair with it:

1. **Give the re-engage hysteresis** (e.g. cut at 850, re-engage at ~1000). Otherwise the new floor
   chatters exactly the way 1700 does today — the present cut/re-engage gap is ~50 rpm, which is
   inside the idle wobble band (p2p 42–97).
2. **Keep an idle-up, but size it to OEM.** With the compressor now running *at* idle the load
   compensation actually matters; the factory 2JZ-GTE figure is 650 → 800 = **+150** (AC-9 / AC-77).
   500 was 3.3× that, and as a standing offset rather than a step it no longer needs to be large.
3. **Watch for the amp taking over the cut.** Compressor-at-idle is the worst case for head pressure
   (no ram air) and for belt slip / compressor-lock detection — both amp-side protections that would
   reintroduce a drop-out at a different trigger. **Log the A/C request input alongside `AC Clutch`
   output** on the verification drive: request high while output goes low = ECU-side; request itself
   dropping = amp protection, and then the pressure/lock/charge side needs attention before the tune
   does. Confirm the condenser fan is on at idle (it is, per the CLT-70/VSS fan strategy).

Sizing check on the 850 floor: it sits ~175 rpm under the hot 1025 target, well outside the measured
steady wobble (p2p 42–97), so it will not nuisance-trip; and it still fires before a genuine sag
becomes a stall.

### Residual exposure: the HVAC amp can still withdraw the request mid-decel

Lowering the ECU's clutch RPM floor fixes the trigger that fired **86 of 86** cut-outs in this log,
but it gives no protection when the *amp* drops the request on its own (high-pressure cut, evaporator
freeze, compressor-lock detection). That event lands the same −500 step at the same bad moment. The
only lever that bounds it regardless of cause is **the size of the step itself**, and the log gives a
hard sizing rule.

**Measured ignition proportional slope: −0.043 °/rpm** (17 123 hot ACTIVE samples, r = −0.88;
consistent with `Ignition PID kP` 51 raw ≈ 0.05 °/rpm). With the authority window +17° / −8°:

| rail | reached at RPM error |
|---|---|
| **−8° min torque (the dip-maker)** | **≈ 185 rpm** — observed p5 of |err| at the rail = 211 |
| +17° max torque | ≈ 393 rpm — observed p5 = 312 |

**So any idle-up larger than ~185 rpm saturates the retard rail the instant it is withdrawn**, and
the engine then gets the full 8° of retard for as long as the error persists — which is the entire
dip mechanism. Below ~185 the loop stays proportional and self-limits.

- 500 → **11.6× over the rail threshold**: full retard, held ~1–2 s, floors 558–682.
- 200 → still rails (the ±200 family does exactly this — see the parked-car example).
- **150 (the OEM 2JZ-GTE figure) → 6.5° of the 8 available: under the rail, with margin.**

That is the principled reason to size the A/C idle-up at ~150 *in addition to* dropping the RPM
floor: the floor change removes the common trigger, the sizing bounds the uncommon one. Neither alone
covers both.

**If full immunity is wanted**, the compensation has to stop going through the *target* at all — an
A/C-gated **airflow** adder produces no RPM error when it is withdrawn, only a slow, small air change.
The Target dialog exposes no such field and the Custom correction is already spent on oil pressure,
so this needs a check of what else EMU exposes (user-defined output / table on the A/C input) before
it can be called available. Do not reach for narrowing `Min torque ign. angle` instead — that damps
every step but also spends the authority needed to catch a genuine sag.

### The A/C idle-up also inflates the activation threshold — and that decides whether a 2000 rpm cut works

**Decoded and confirmed from this log:** in ARMED the displayed `Idle target` is
`min(RPM, base target + Ramp down max. offset)`, i.e. it tracks RPM until RPM exceeds the cap, then
sits on the cap — and **that cap is the activation point.** Every clamp value observed in the drive
resolves exactly on `offset = 350`:

| observed cap | = base target + 350 |
|---|---|
| 1350 / 1400 | 1000 / 1050 (hot base) |
| 1580 / 1600 | 1225 / 1250 (base + VSS 200) |
| 1780 | 1425 (base + VSS + clutch) |
| **2080 / 2100** | **1225 / 1250 + A/C 500** |
| **2280** | **1425 + A/C 500** |

Consequence, measured directly: **activation RPM with the A/C engaged in the prior second — min 1731,
median 2078, max 2300 (n = 32); with A/C off — min 1055, median 1419, max 1967 (n = 21).** The
idle-up drags the whole idle entry ~650 rpm higher. So with A/C on, idle is already **ACTIVE** by
~2075, which is precisely why a clutch cut at 1700 lands inside the closed loop.

**Owner's fallback (2026-08-27): raise the A/C cut to 2000 rpm to get it clear of idle.** Whether that
works is pure arithmetic against the cap — the cut must sit **above** `base target + A/C increase +
350`, so the step lands while the PIDs are still zeroed in ARMED:

| configuration | activation threshold | 2000 rpm cut lands… |
|---|---|---|
| today (VSS +200, A/C +500) | 1225 + 500 + 350 = **2075** | **below it — still ACTIVE. Does not help.** |
| VSS cancelled, A/C +500 | 1025 + 500 + 350 = **1875** | above it — ARMED, no PID output. Works. |
| VSS cancelled, A/C +150 | 1025 + 150 + 350 = **1525** | above it by 475. Works with margin. |

So the fallback is viable, but **only in combination with cancelling the VSS increase** — at today's
settings 2000 is 75 rpm short of the threshold and buys nothing. Two costs to weigh against the 850
direction: RPM crosses 2000 more often than 1700 in traffic, so cycling gets *worse* unless hysteresis
is added; and it guarantees no cooling at a stop, which is the opposite of what the 850 change is for.

### Would more kP help? No — the event is authority-limited, not gain-limited (measured)

Decomposing the t = 321.6 event against the measured proportional slope (−0.0432 °/rpm), residual =
actual `Idle ignition correction` − clipped P term:

| t (s) | RPM | target | error | P term demanded | ign corr delivered | residual (I + D) |
|---|---|---|---|---|---|---|
| 321.76 | 1711 | 1205 | **+506** | **−21.9°** | **−8.0 (rail)** | **0.00** |
| 322.08 | 1562 | 1165 | +397 | −17.2° | −8.0 (rail) | **0.00** |
| 322.24 | 1351 | 1145 | +206 | −8.9° | −7.0 | 1.00 |
| 322.80 | 836 | 1075 | −239 | +10.3° | +15.0 | 4.68 |
| 323.12 | 635 | 1050 | −415 | +17.9° | **+17.0 (rail)** | **0.00** |
| 323.76 | 558 | 1050 | **−492** | **+21.3°** | **+17.0 (rail)** | **0.00** |

**The whole excursion ran on the proportional term, pinned to one rail then the other. Residual is
0.00 through both saturated stretches — the integral contributed nothing where it mattered** (it
shows up only as +3…+4.7 mid-recovery, where the loop was briefly linear). *(Owner's first read had
"−5.38° ign and −8 % airflow" — the values are right but swapped: at t = 322.08 the ignition
correction is **−8.0°** on its clamp and the airflow PID is **−5.38 %**, its slaved copy. It is the
clamp, not accumulated integral.)*

**Consequences for the gain question:**

1. **More ignition kP does literally nothing on this event.** The loop asked for **−21.9° and got 8** —
   2.7× past saturation — then asked for **+21.3° and got 17**. While clamped, output is the clamp;
   multiplying kP changes no sample. This transient is **authority-limited**.
2. **And yes, more kP would choke it out faster everywhere else** — the owner's own worry is correct
   and quantified. The retard rail is reached at only **~185 rpm** of error today. Raising kP shrinks
   that proportional band, so a larger share of ordinary disturbances get converted into a
   **full-authority torque cut** instead of a proportional nudge. Higher kP buys nothing at the rail
   and buys more time *at* the rail.
3. **Airflow kP is already convicted — do not raise it.** 08-22d measured the idle limit cycle as the
   delayed air copy of the ignition action (`airPID = 2.06 × ignCorr`, r 0.984) and halving
   `idleAirFlowKP` to ~1 %/° fixed it; this log measures 0.82 and the settled wobble is down to
   p2p 42–97. Re-raising it puts the delayed energy back.

### Why the air channel really is slow at idle — it is filling, not acoustics

The owner's point that a pressure wave crosses a short-runner plenum at sonic speed is correct and
irrelevant: what sets the lag is **mass-filling a plenum from a trickle of flow**, and that is at its
worst precisely at idle. Book-backed —
[Kiencke & Nielsen §3.2.6, pp. 65–68](../../corpus/automotive_control_systems_kiencke_nielsen.md):

> at minimum power (e.g. idling), p_m,0 = 0.35 bar and ṁ_a,0 = 6 kg/h gives **T_m = 740 ms**

against **20–25 ms at WOT** — the manifold time constant is **~35× longer at idle**, because
τ ≈ m_plenum / ṁ and ṁ is at its minimum. Kiencke states the consequence directly: "the dynamic
behavior of the intake manifold has an impact on engine dynamics especially at low power such as
idling." The repo's measured ~750 ms end-to-end air lag on this car (DBW travel ~160 ms + fill +
induction-to-torque) sits right on that figure. So the air channel is not slow because of wave
propagation — it is slow because at 35 kPa and idle flow there is almost nothing moving to fill it
with. **The lag is real and is not shortened by gain.**

### What would actually soak up the transient

- **Reduce the step** (owner's own answer, and the first one). Below ~185 rpm of error the ignition
  loop stays linear and every other lever starts working. Above it, nothing does.
- **Derivative on the ignition channel — the one gain increase that is indicated.** D responds to RPM
  *rate*, so it acts while the error is still inside the proportional band, before P saturates: it
  anticipates rather than amplifies. On this event D would have opposed the slam (error large and
  falling → D commands advance against P's retard). Airflow KD is 0 in the record; **read the live
  ignition kD before assuming.** ⚠ Two cautions: (a) if EMU differentiates *error* rather than
  *measurement*, a −500 setpoint step produces a one-sample derivative **kick** of extra retard,
  which is worse than no D at all — step in small and watch the first sample after a step; (b) D
  amplifies RPM noise, though this build's idle is clean (p2p 42–97).
- **Feedforward, not feedback.** The A/C load and its idle-up are a *known* event with a known sign
  and size. No feedback gain beats knowing it is coming. This is the same conclusion the armed-table
  work reached from the other direction.
- **Rate-limit the setpoint** if EMU exposes a slew on the increases — it converts the step into a
  ramp the loop can track inside its linear band, which is the general form of "reduce the step."

### ⚠ Correction: ~150/185 is a controller bound, NOT a load requirement — and the target is a weak feedforward channel

Owner's objection (2026-08-27) is correct and this supersedes the sizing advice above. Two different
questions were run together:

1. **How much airflow does the compressor load actually need?** — a torque question, answered by the
   engine.
2. **What target step keeps the Ignition PID out of its rails?** — a controller question, answered by
   `kP` and the torque-angle window. **This is what ~185 rpm is.** It is a *constraint on what the
   controller tolerates*, not a *specification of what the load needs*. Sizing a load compensation by
   it is backwards.

**Measured exchange rate — the target is a poor air lever on this build.** Open-loop feedforward
(`Idle air %` − PID − custom) against idle target, hot ACTIVE, after the mid-log airflow edit:

| idle target | feedforward base | n |
|---|---|---|
| 1020 | 26.81 | 3976 |
| 1220 | 28.44 | 3221 |
| 1420 | 31.62 | 153 |

**Supply slope = 1.20 airflow points per 100 rpm of target** (r = 0.983). Therefore:

- the current **500-rpm** A/C increase supplies only **~6.0 airflow points** of feedforward;
- a **185-rpm** increase supplies **~2.2 points**;
- matching the oil correction's **13 points** would take a **~1080 rpm** target increase.

So a target increase is mostly *setpoint move*, not *feedforward*: the small air bump arrives first
and the PID is left to find the rest through the 740 ms manifold lag. **If the compressor's real air
requirement is anywhere near the oil correction's 13 points, the target channel is the wrong
instrument by roughly 6×, and neither 185 nor 500 is a load-based number.**

**Channel allocation — why oil correctly stays on the custom correction.** The two disturbances are
not interchangeable:

| | oil viscosity | A/C compressor |
|---|---|---|
| speed | slow (10–20 min) | step, on/off |
| size | **13 airflow points** (owner: ≈ 1000 → 2000 rpm on a free engine, so ~77 free-rpm per point) | unmeasured |
| should idle **speed** change with it? | **No** — idle RPM must not track oil temperature | **Yes** — OEM raises 650 → 800 with A/C on |

The target channel moves the setpoint by construction, so **oil cannot go there** — it would make idle
speed a function of oil temperature, against the standing preference for fewer scheduled idle
variables. The custom (airflow-only) channel is the right home for it and should stay. A/C is the one
case where a speed raise is legitimate — but the *air* half still has to come from somewhere, and at
1.2 points per 100 rpm the target barely supplies it.

**Measure the load before choosing the number.** This is now possible for the first time — the log
cannot answer it (the compressor was never engaged below 1669 rpm, and every A/C-off sample in the
1650–1900 overlap is mid-collapse on the min-torque rail, not an equilibrium). With the clutch floor
at 850:

1. Hot idle, stable, PID settled, A/C off. Record `Idle air %` **and** `Idle PID air % correction`.
2. Engage the compressor. Wait ≥ 5 s for RPM to return to target and the PID to settle (740 ms
   manifold τ plus integral).
3. **The change in settled `Idle air %` is the required feedforward, in airflow points** — directly
   comparable to the oil correction's 13.
4. Repeat at a couple of ambient / head-pressure conditions; compressor torque scales with head
   pressure, so one reading is not the whole table.

Set the A/C idle-up to a small value (or 0) for the measurement so the number is not contaminated by
the target's own air contribution; the resulting dip is exactly the disturbance being characterised,
and the 850 floor is the backstop.

**Then allocate:** if the measured need is small (≲ 3 points), the target increase can carry it and
the ~185 rpm rail constraint is the binding limit. If it is large, the air must come from an
airflow-only channel — **check whether EMU allows a second correction, or whether the custom
correction's axis can be assigned to the A/C input** (its axis is demonstrably re-assignable: it was
a CAT axis before it was an oil-pressure axis). If only one correction exists and oil owns it, the
remaining options are: accept PID action with the 740 ms lag, or use a larger target increase and
accept the rail on withdrawal.

**Conditional alternative worth considering:** with the compressor now engaged from 850 rpm up, A/C
at idle becomes a persistent state rather than an intermittent one. If it is on for most of the
driving that matters, the base `idleActiveAirflow` rows can simply be calibrated **with the
compressor running**, and the PID trims *down* on the rarer A/C-off case — the safe direction, and no
step at all. Cost: it re-creates the standing negative-trim / retarded-angle posture that the 08-22d
work removed, whenever A/C is off. Only worth it if A/C-at-idle is the dominant case.

### The loop now has the authority to absorb the A/C load — measured headroom (owner's framing, 2026-08-28)

Owner's read is correct and this is the right way round: **the target increase mostly biases the
loop; the PID does the work.** That only became viable once the ignition PID was un-restricted —
previously the ignition correction was tightly limited, and because the airflow PID is *slaved to
ignition angle error* (~1 %/° after the KP halving) a restricted ignition loop meant a near-inert air
loop, so the engine bogged long before compensation arrived. Both loops now have range. Measured in
this log:

| quantity | measured | clamp |
|---|---|---|
| airflow PID excursion | **−8.81 … +19.50** | −15 / **+25** |
| samples above +20 | **0.00 %** | — |
| headroom from settled idle to the +25 clamp | **28.9 points** | — |
| sustained airflow-PID slew (real recovery, t 322.4–324.1) | **8.9 points/s** | — |
| ignition angle at settled idle | 17.0° | Target 18, Max torque 35 |
| usable advance reserve | **+17°** (correction clamp) | — |

**So a step A/C load is inside the envelope.** For a 10-point requirement the PID travels from its
settled −3.9 to about +6 — 10 points at 8.9 points/s ≈ **1.1 s**, plus the ~740 ms manifold lag, so
air is substantially there in **~2 s**, with 19 points of clamp still unused. Even a 13-point load
(matching the oil correction) lands at +9 in ~1.5 s and leaves 16 points spare. During that window
the **+17° ignition reserve is the fast lever**, applied within one ~40 ms loop pass — the standard
fast-spark / slow-air split (Kiencke §5.2; the 740 ms manifold τ is §3.2.6).

**The binding constraint has moved from authority to time.** Two time costs worth naming:

- **~740 ms of manifold lag**, irreducible by gain (see the filling section above).
- **~0.45 s of "travel debt"** — the PID sits at a settled **−3.94** because the base airflow carries
  the deliberate open-loop-guarantee surplus, so it must climb ~4 points just to reach net-zero
  before it starts *adding* air. That is a genuine cost of the guarantee, **not** a reason to trim
  the base ([idle_base_airflow_is_open_loop_guarantee]) — just a term in the response budget.

**What to watch on the first A/C-at-idle test:** the *engagement* transient is the new one (load step
down, ignition advances first, air follows) and it is the direction the reserve is designed for.
Disengagement is still the one that produced the 558/616/682 dips, but with the increase at 185 its
withdrawal is worth only ~2.2 airflow points and 185 rpm of error — inside the ~185 rpm retard rail,
so no full-authority torque cut. Log `Idle air %`, `Idle PID air % correction`, `Idle ignition
correction`, `Ignition Angle` and the A/C request; the settled `Idle air %` delta across an
engagement is simultaneously the load measurement asked for above.

### Is the ignition correction too slow? Measured: no — it is in phase. The limits are gain and rail depth

Owner's question, 2026-08-28. Answered from `added features.csv` directly.

**1. There is no dead time in the ignition path.** Cross-correlation of `Idle ignition correction`
against RPM error peaks at **lag 0** and falls off symmetrically both ways — whole hot ACTIVE data
set (n = 17 283): r = −0.822 at −40 ms, **−0.878 at 0**, −0.829 at +40 ms. Restricted to settled
stopped idle only (5 runs > 15 s, 115 s): −0.802 at −40 ms, **−0.807 at 0**, −0.779 at +40 ms.
A phase-shifted self-oscillation would peak at ~90° of the 1 s wobble period (≈ −6 samples); it does
not. **The residual idle wobble is proportional tracking of a disturbance, not a limit cycle** — so
there is gain margin. (Residual: RPM error sd **21.5**, p5…p95 **−28…+45**.)

**2. It is not rate-limited either.** Through the 558-rpm dip it walked the error proportionally and
reached the advance rail in **0.60 s**: err −108 → +8.0°, err −254 → +15.0°, err −336 → **+17.0
(rail, angle 35°)** — then held maximum advance for 0.6 s more while RPM fell 724 → 558. At that
moment it was an **authority** failure, not a speed failure.

**3. What actually limits it is gain and, more importantly, rail asymmetry.**
Unrailed regression over 17 283 hot ACTIVE samples: `ignCorr = −0.0424 × (RPM − target) + 0.18`
(r = −0.889). So **0.042 °/rpm**, and the two rails are reached at very different errors:

| direction | clamp | rails at |
|---|---|---|
| advance (anti-stall) | **+17°** | **401 rpm** of error |
| retard (over-speed) | **−8°** | **189 rpm** of error |

The retard side is **2.1× more sensitive**, and −8° at idle is a large torque cut — that clamp depth,
not any lag, is what turned the target steps into craters (a 500 step rails retard at 38 % of the
error; a 200 step at 95 %).

**4. Why raising ignition kP alone is the wrong move** (and the owner's own worry — "wouldn't that
choke the engine out faster?" — is correct). Doubling kP to 0.084 °/rpm would rail **retard at 95 rpm**
of error, against a settled-idle p95 error of **+45** — normal idle wander would start touching the
torque cut. And because the airflow PID is *slaved to ignition angle error*, doubling ignition kP
doubles the **delayed** air action too, which is the documented destabiliser (08-22d: the air copy
arrives ~740 ms late).

**5. The move that is free in the stability sense: change the ignition:air ratio, not the total.**
`airPID = idleAirFlowKP × ignCorr` — so raising ignition kP by a factor *k* while dividing
`idleAirFlowKP` by the same *k* leaves the delayed path's loop gain **exactly unchanged** while the
fast, zero-lag spark action gets *k* times stronger. Worked at k = 1.5: ignition kP ×1.5 (→ ~0.063
°/rpm; advance rails at 267 rpm, retard at 126), `idleAirFlowKP` **1024 → ~683**. Net delayed-path
gain identical to today. This is the right shape because the ignition path has zero measured lag
(stabilising) and the air path has 740 ms (destabilising) — moving authority from air to spark buys
speed and stability together.

**6. Pair it with shrinking the retard *depth*, not the retard trigger.** Railing early is harmless if
the rail is benign; the crater came from depth. Raise `Min torque ign. angle` (≈ 10° → ≈ 14°) so the
negative clamp goes −8 → −4: worst-case commanded torque cut halves, over-speed simply takes a little
longer to come down, and air still pulls it. Keep the +17° advance side intact — a momentary high
idle is benign, a stall is not, so the authority *should* be asymmetric in the advance direction.

**Cost to weigh:** this shifts idle-holding work from air onto spark, so the engine sits further from
MBT more of the time (slightly worse idle efficiency / higher EGT) and spends more of the torque
reserve. Minor at idle, but it is the trade being made.

### ⚠ Retracted: reducing retard authority. And an OEM benchmark of both channels (2026-08-28)

**Retraction — the retard-clamp suggestion was symptom-level, not an engineering need.** Owner asked
whether it addressed a real requirement. Tested directly, it does not. Splitting hot ACTIVE samples by
whether a ≥150 rpm target step occurred in the prior 3 s:

| | on the −8 floor | ≤ −6° | ≤ −4° | p1 |
|---|---|---|---|---|
| **within 3 s of a step** (209 s) | **12.03 %** | 21.00 % | 28.86 % | −8.0 |
| **clean, no step** (520 s) | **0.14 %** | 0.73 % | 2.21 % | −5.0 |

The floor is reached **~86× more often** when a spurious step is present. And on the clean ACTIVE
descent — the phase the 08-22d work was about — `ignCorr` median is now **0.00**, p10 **−4.5**, only
**2.44 %** on the floor and 6.17 % at ≤ −6°, against the 08-22d baseline of median −3.0, p10 −8.0,
**34 % of the descent at ≥ 6° retard**. RPM − target on descent: median **+19**, p90 +104.

**Conclusion: the `idleRAMPDownDecayRate` 650 → 125 change already took the descent off the retard
floor. The only thing still driving ignition to −8 is the spurious target steps. Remove the steps and
the clamp is never reached — do not touch it.** The owner's framing is the correct one: the big fix is
eliminating the drops and letting the PID work.

**OEM / academic benchmark of both channels** (corpus: Kiencke & Nielsen §5.2, Bosch p. 224/235):

| | this build, measured | K&N / Bosch reference |
|---|---|---|
| actuator split | air = slow integral, ignition = fast | Bosch p. 224 — identical split ✔ |
| ignition role | **proportional** (0.042 °/rpm), airflow slaved to angle error | K&N §5.2.3: the **D portion** shifts ignition "due to the smaller delays" — *structurally different* |
| ignition dead time | **0 samples (< 40 ms)**, correlation peaks at lag 0 | "< 1 engine cycle" |
| ignition range | **+17° / −8°** | "limited range (**~±5° effectively**)" |
| ignition authority | ~400 rpm of error at the advance rail | "recover **~50–80 rpm** within one engine cycle" |
| air recovery time | **~2 s** for a 10-point step (1.1 s PID travel + 740 ms lag) | "**~2–3 seconds** via the air channel" |
| A/C engagement dip | **not yet measurable** (never engaged below 1669 rpm) | "**~100–150 rpm** with a well-tuned controller" |

**What the benchmark says:**

1. **The air channel is already at OEM speed** — ~2 s against K&N's 2–3 s. There is nothing to gain
   there, and the 740 ms manifold τ is the physical floor regardless of gain.
2. **The ignition channel is already ~3.4× the reference range** (+17/−8 vs ±5) and responds with no
   measurable dead time. By this benchmark it is neither slow nor weak — it is well beyond typical
   OEM authority. (The larger range is *justified* here: EMU runs ignition as a P channel, where K&N
   describes it as the D channel, so it needs more range to do more of the work.)
3. **Therefore: leave both gains alone.** Nothing in the measured behaviour or the benchmark supports
   raising ignition kP, lowering `idleAirFlowKP`, or narrowing the retard clamp. The k-ratio trade
   proposed above is sound arithmetic but solves a problem this build does not have.

**Pass/fail criterion for the first A/C-at-idle test, from the same source:** a well-tuned OEM
controller dips **100–150 rpm** on compressor engagement and recovers in **2–3 s**. That is the number
to judge the result against — not zero dip.

**Owner's mechanism read is confirmed by the numbers.** At the step the airflow PID sat at **−4.9**
and had to travel to **+14.4** — 19.3 points at the measured 8.9 points/s ≈ **2.2 s**, plus the 740 ms
lag. RPM bottomed **1.9 s** after the step. The unwind time and the floor coincide, so the negative
starting position (the open-loop-guarantee surplus being trimmed out) is a real term in the recovery
budget — as noted above, a cost of the guarantee to be aware of, not a reason to remove it.

**Related theory for the feedforward instinct** (K&N §5.2.2, p. 126): the documented handling for a
*known* disturbance is to interrupt integration and hand the transition to a precomputed feedforward
value rather than leaving it to the PID — which is exactly the argument for compensating a
commanded A/C engagement on an airflow channel rather than through the loop.

### VSS increase: the flicker is real but rare — cancelling it is defensible

**Owner, 2026-08-27: the logged speed flickers to as much as 63 km/h at a standstill.** No value of
`Increase target above VSS` is safe against that, so the earlier "raise the threshold" advice does
not hold — the choice is cancel the increase or clean up the speed signal.

Frequency, measured: of the 125 in-ACTIVE ±200 steps, only **8 (6 %)** fired from a genuinely settled
stopped idle (state 2, `Gear` 0, |RPM − target| < 60 for the prior 2 s) — 8 bursts in 27 minutes. The
other 117 are legitimate crossings during creep. Excursions from those 8, restricted to samples with
no driver input: **p2p 16 / 120 / 132 / 178 / 303 / 324 rpm** (two unmeasurable, driver pulled away).
So the owner's read is right — uncommon, and not dangerous.

Cancelling costs the steering-effort benefit only while rolling **in gear** (clutch out); the
`Clutch pressed target increase` = 200 still covers the return-to-idle case that actually stopped the
dips, since those all happen with the clutch in. Consistent with the standing preference for fewer
scheduled idle variables. **The wider point stands regardless of what is done with the idle target:
the same noisy speed input gates other VSS-conditioned logic in the ECU, so a 63 km/h spike at rest
is worth fixing at the sensor even if the idle increase is removed.**

### 2026-08-29 — the VSS gate is a decoupling gate; measured windup while coupled

Source: `omg.csv` (2026-08-24), segment t > 839 s (post-`Making permanent`). Owner's framing,
which the data supports: `idleOpenLoopOverVss` is not a high-speed safety cutoff — with the
clutch/neutral escapes it decides *whether crank speed is the throttle's responsibility at all*.
Rolling in gear with the pedal up, it is not, and the loop winds against a driveline disturbance
it cannot correct. Generic write-up in [notes/idle.md → Activation gates](../../notes/idle.md).

Measured on this car:

| quantity | value |
|---|---|
| corr(RPM error just before a rolling clutch press, accrued `Idle PID air % correction`) | **−0.813** (n = 7) |
| idle ACTIVE while rolling > 2 km/h | **142.4 s = 20 %** of all ACTIVE time |
| accrued air correction over that exposure | p5 **−7.31**, p95 **+12.0**, mean +0.18 |
| RPM error over that exposure | mean **+22**, **58 %** above target |

So the posture carried into a clutch press is proportional to how hard the driveline was holding
RPM off target, and it goes **both ways** — which is why the same clutch-in sometimes dips and
sometimes flares. The single clean coast-in press in this log (no throttle for 3 s after,
t = 981.2 s, ~20 km/h) went from **+92 rpm above target with −7.5 % of air wound out** to **−24
below**: a 116 rpm swing. n = 1, so treat it as consistent with the mechanism, not proof of it;
the other six presses were followed by throttle and are unreadable. **A cleaner test is cheap:**
log a few coast-to-stop clutch-ins with no throttle, at varied grade, and correlate accrued
correction at the press against the excursion after.

Earlier in this note (2026-08-29 first pass) the t = 886–889 s walk of the air correction from
−3.9 to −6.5 while coasting ~45 km/h in 5th was described as the loop behaving sanely. **That was
the wrong reading** — it is 6.5 airflow points pulled out to fight the driveline, waiting to land
on the next clutch press.

**Setting it:** low, not high — but bounded below by the speed channel's standstill noise floor,
because the force wipes both integrals and a glitch at a stopped idle is a stall shape. The
mis-grounded clutch switch that made this channel read 81 km/h at a standstill was found and fixed
2026-08-29 ([vss_signal_integrity.md](vss_signal_integrity.md)); re-log and read the settled
stopped-idle maximum off the clean channel before choosing the number.

### Open items

- **A frozen-PID mode.** 4.3 % of hot ACTIVE samples have `Idle PID air % correction` **and**
  `Idle ignition correction` at exactly 0 with the angle exactly at target; five runs exceed 2 s (max
  8.5 s), all rolling (`Gear` 3–5) with RPM 50–150 *above* target and MAP 30–33. Example t = 1455–1463:
  RPM 1300–1370 on a 1225 target with both loops output-zero for 8 s. Cause unidentified.
  **CLOSED 2026-08-29 — it is the VSS open-loop gate. Confirmed in `omg.csv`, which carries both a
  speed channel and `Idle force open loop`: same signature, flag asserted. See
  [vss_signal_integrity.md](vss_signal_integrity.md) for the mechanism (the gear estimator's
  `Gear unknown` flicker is what toggles it) and the measured cost.** Original reasoning: `Open loop over VSS`
  (`idleOpenLoopOverVss`) forces *all* idle PIDs off and **resets the integral terms** — help,
  `docs/emu-black-help/Idle.md` — which is exactly this signature (both outputs exactly 0, angle
  exactly at target). Every one of these runs is rolling in gear, and `idleClutchEnablesClosedLoop` /
  `idleNeutralEnablesClosedLoop` are both on, so the force only survives with the clutch out — again
  matching. No VSS channel in this log, so it stays a hypothesis; log **`Idle force open loop`** plus
  a real speed channel to close it. If confirmed, the cost is not just the frozen window: the integral
  reset means PID posture is discarded at every crossing and re-accrues from zero on the next entry
  (the "travel debt" term above).
- **Channels to add:** the A/C **request** (not just `AC Clutch` output), PPS, the clutch switch, and
  a real speed channel. Every attribution above that concerns A/C, VSS or clutch rests on the target
  arithmetic (base 1025/1050 CLT-scheduled, +200 VSS, +200 clutch, +500 A/C) rather than on the input
  itself. `DBW target` is *not* needed — infer it from `Idle air %` per the mapping above.
- CLT still jitters (96 ↔ 113 here) sample-to-sample.
