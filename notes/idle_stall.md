# Idle Stall Troubleshooting

Idle stalls on EMU Black builds nearly always have a specific, diagnosable root cause. Log the stall, identify which pattern matches, and fix that one thing. Do not tune blind.

---

## Step 0: Get a Log

Every diagnosis starts with a log that captures the stall. Before changing anything:

```python
import pandas as pd
df = pd.read_csv('log.csv', sep=';')
df.columns = df.columns.str.strip()

# Find all stall events
stalls = df[(df['RPM'] == 0) & (df['RPM'].shift(1) > 200)]
for i, row in stalls.iterrows():
    window = df.loc[max(0, i-100):i+20]
    print(f"\n--- Stall at t={row['TIME']:.2f}s ---")
    print(window[['TIME','RPM','MAP','TPS','Lambda is valid',
                  'Short term trim','Idle air %','DBW Out. DC',
                  'Idle state','Fuel Cut','ECU State']].to_string())
```

Look at the 4 seconds **before** the stall, not just the moment it dies.

---

## When Does It Stall? (Quick Sort)

| Symptom | Most likely cause | Section |
|---|---|---|
| Coming off throttle at speed | Armed state airflow too low | [A] |
| Right after cold start | Post-start throttle slam / ASE | [B] |
| Warm idle, no obvious trigger | VE error or fuel trim | [C] |
| Tapping the throttle lightly | DBW floor / blend gap | [D] |
| Idle hunts then dies | Noisy VVT-i or CLT sensor | [E] |
| Idle PID never engages | Brake switch stuck active | [F] |
| Idle slowly falls, integrator can't recover | PID integrator windup | [G] |
| RPM craters then wobbles on a rolling return to idle | Rich low-RPM VE bog + fan-off airflow loss | [H] |

---

## [A] Overrun-to-Idle Stall

**The most common stall on a tuned car.** Happens after lift-off from high RPM or boost.

### What you'll see in the log

- RPM drops from 2000–3000 toward idle
- `DBW Out. DC` goes to −80% or worse — throttle is fighting its return spring
- `Fuel Cut` exits (fuel returns) into a near-zero air column
- Lambda spikes rich — ECU commands fuel based on MAP/RPM but actual airflow is nearly zero
- Rich stumble → RPM drops further → more closed throttle → feedback loop → stall

**The rich spike is a symptom. The cause is the armed state airflow table.**

### Root cause

Armed state airflow resolves too low (0–4% Airflow) at the decel RPM bins. Below 2.0% Airflow the DBW motor is actively working against the return spring with no useful airflow result.

### Fix

Populate the armed state airflow table with **60–80% Airflow at 1800–2200 RPM** (PPS = 0). Taper down to match your idle airflow value (~38%) at the 1100–1300 RPM bins. Do not create a step at the bottom — the transition into idle PID should be seamless.

The rich spike and stall both disappear once the throttle stops fighting itself.

### Secondary check

If overrun fuel cut exits harshly, consider:
- Raising the exit RPM threshold to 2500 RPM (gives idle controller a running start)
- Stepped exit: −50% fuel at 2500 RPM, full fuel at ~1800 RPM
- Reducing overrun exit enrichment — a large pulse (+20–25%) fired into a barely-cracked throttle makes the stumble worse, not better

---

## [B] Cold Start / Post-Start Stall

### Pattern 1: Throttle slams shut after cranking

The throttle body is at cranking position (~14% TPS) during crank, then snaps to idle position (~3% TPS) as soon as the engine fires. This air deficit is too large for ASE to compensate.

**Fix:** Use a post-start idle RPM target that stays elevated for 5–10 seconds after start, then tapers. This keeps the throttle open long enough for the transition to be smooth. Do not reduce ASE to compensate — ASE is not the cause.

### Pattern 2: ASE decays too fast

If ASE drops to zero before the wideband validates (Lambda is valid = 0), the ECU runs open-loop with no trim correction. If base VE is even slightly lean, the engine stalls as wall-wetting fuel evaporates and ASE runs out simultaneously.

**Fix:** Configure ASE as a 2D table: CLT vs. **engine revolutions** (not time). The revolution axis tracks wall-wetting decay better than time. Reference values:

| CLT | Revolutions | ASE % |
|-----|-------------|-------|
| −10°C | 1 | ~60% |
| 20°C | 5 | ~30% |
| 60°C | 10 | ~10% |
| 110°C | 20 | 0% |

Also confirm `Lambda is valid` goes to 1 before ASE reaches 0. If the wideband validates after ASE runs out, you have no safety net.

---

## [C] Warm Idle Stall (No Obvious Trigger)

### Check order

**1. Is the wideband valid?**
`Lambda is valid` = 0 throughout means `Short term trim` = 0. The ECU is running open-loop. Base VE must be exactly right. If it's even 5% lean at idle MAP/RPM, the engine will slowly starve.

Fix: get the wideband hot and validated before diagnosing anything else. If it takes too long to validate, check the heater circuit.

**2. Is ASE masking a lean VE table?**
`Afterstart Enrichment` decaying toward 0 while RPM is slowly falling is the signature. The engine is fine on ASE, then runs out and stalls.

Fix: add fuel to idle VE cells (MAP 30–40 kPa, RPM 800–1200) at the operating CLT.

**3. Is the idle PID even active?**
Check `Idle state`. A value of 0 throughout means the idle PID is completely disabled. See **[F]** (brake switch).

**4. Is the DBW floor too low?**
Look at hot-idle TPS. You never need significantly less throttle than you use at steady hot idle. If your actuator floor is set below that, there is a range where the throttle is commanded partially closed but not enough to support the engine.

Fix: set the actuator floor just below steady hot-idle TPS. Set DBW min position DC% just below this too.

**5. Fuel trim maldistribution (front-feed intake manifolds)**
Front-feed intake manifolds distribute fuel unevenly under air mass inertia. The rearmost cylinder consistently runs lean at cruise — visible as rear EGT hotter than the others, and that cylinder knocking first. At idle this is less severe, but a poorly trimmed FFIM can cause a cylinder to misfire, dropping RPM enough to stall.

Fix: add ~9–10% fuel trim to the lean cylinder at idle MAP/RPM. Taper to ~5% under boost (manifold distribution improves with pressure).

---

## [D] Tip-In Stall (Light Throttle Touch Kills It)

### Signature

Engine is idling stably. A small, gentle throttle input — not a blip, just a light touch — causes RPM to drop and the engine dies.

### Root cause

A gap exists between the idle airflow control exit point and the blend values taking over. When you tap the throttle:
1. Idle airflow control hands off to driver demand
2. DBW targets a small opening based on the characteristic map
3. The small commanded opening is less than idle required — throttle is effectively closing

### Fix

- Set actuator floor and DBW min position DC% just below hot-idle TPS (same fix as C4 above)
- Check the blend point: it should be just above your idle PPS, giving you a smooth ramp from idle control into driver demand
- If you're running an armed-state margin, confirm it doesn't resolve below idle at low RPM

---

## [E] Idle Hunts Then Stalls (Sensor Noise)

### VVT-i noise

Noisy VVT cam angle readings cause the ECU to see false position changes, which affects cam angle targets and therefore breathing. VVT instability shows up as erratic MAP and RPM oscillation at idle.

Fix: check `VVT CAM1 angle` in the log. If it's oscillating ±5° or more at stable idle, the solenoid, oil pressure, or feedback circuit needs attention before idle can be stable. Lock VVT to a fixed value temporarily to confirm.

### CLT sensor noise

A noisy CLT makes the idle ref table, warmup enrichment, and ASE all oscillate simultaneously. Three feedback loops all fighting each other.

Fix: check `CLT` for rapid small fluctuations (1–2°C jitter at stable temperature). This points to a wiring or sensor issue, not a calibration issue.

### Front-feed manifold maldistribution at idle

At idle with cams, misfires on one cylinder are enough to cause RPM oscillation. If a rear cylinder is consistently lean, every few cycles it misfires, RPM dips, the idle PID opens the throttle, the misfire stops, RPM rises, PID closes, misfire recurs — oscillation.

Fix: EGT probes on each cylinder. If a rear EGT runs 30–50°C hotter at idle, fuel trim that cylinder.

---

## [F] Idle PID Disabled (Brake Switch)

### Signature

`Idle state` = 0 throughout the entire log, even during a clean stable idle. The engine manages to idle, but there is no PID authority. Any disturbance — A/C clutch, fan cycling, load change — causes a stumble with no recovery.

### Root cause

A continuously active brake switch signal tells the ECU to hold idle control in open-loop mode permanently. Common cause: brake switch adjustment, wiring short, or a switch that closes under vibration.

### Diagnosis

```python
# Check idle state throughout the log
print(df['Idle state'].value_counts())
# If only 0 appears, idle PID never activated
```

Fix: check brake switch input in real-time while the engine is running. Should be 0 (inactive) when foot is off brake. Adjust or replace the switch.

---

## [G] PID Integrator Windup

### Signature

RPM slowly drifts down over 5–10 seconds. The PID tries to recover but each correction is too slow. By the time it opens the throttle enough, the engine is already below the recovery threshold and stalls.

### Root cause

Integrator accumulates error over time but its limit is set too high. It chases a large accumulated error instead of responding to the current error. The proportional term could have recovered the engine; the integrator is lagging behind.

### Fix

- Keep integrator limits **lower than proportional limits**. The proportional term responds instantly; the integrator is slow by design.
- Set the integrator so corrections take ~5 seconds to reach steady state — fast enough to eliminate steady-state error, slow enough not to fight the proportional term.
- Starting baseline: P: 3.0 | I: 1.0 | D: 0.2. Tune P-only first, add I to eliminate droop, add D only if overshoot is a problem.

---

## [H] Rolling Return-to-Idle Wobble ("drive wobble")

**Distinct from [A]:** this is a *recoverable* oscillation, not a clean stall. RPM craters well below idle target (observed: ~1800 → **525 rpm** at a 1200 target) then limit-cycles (525↔1390) during a **neutral coast-down to idle while the car is still rolling**. The driver always neutral-shifts toward a stop, so the engine is decoupled and free-falls toward idle (confirmed: RPM/VSS ratio swings 8×, impossible in a fixed gear). Two compounding faults — both must be addressed.

### 1. Fuel: rich bog at low RPM (the violent part)

As RPM craters and MAP rises toward 60+ kPa (low-rpm pumping loss), the speed-density fuel calc over-fuels. Measured `Lambda 1` dives to **0.68 (AFR 9.9)** against a 0.93 target — the low-rpm VE is **~17–19% rich** at MAP 35–64 kPa. Rich misfire → erratic torque → the dip goes deep and oscillates. This is exactly the "unstable lambda the airflow PID cannot compensate for" case the EMU idle help warns about.

> **⚠ Baseline caveat — do not lean off these numbers blindly.** The −17–19 % figure is from the *pre-correction* logs, recorded at **E25** (not the usual E60). A global **−18 % pump (`veTable`) / +10 % ethanol (`veTable2`)** correction was applied afterward (the v2 export). Because the correction is split by fuel and blended through `tblsVEBlend`, its net effect is **fuel-dependent**: ~**0 %** at E60 (~38 % pump weight — the −18/+10 nearly cancels) but ~**−11 %** at E25 (73.5 % pump). So on the v2 calibration the dip residual is *still ~−18 % rich at E60* but only ~**−9 %** at E25. A lean computed from the E25 log is roughly right **only** for E60; at E25 it over-leans by ~9 % and risks a lean stumble. **Always re-measure lambda on a v2-calibration dip log at the fuel you actually run before leaning the 500/842 rows.**

> **⚠ The 500 rpm VE channel must be tuned for dips.** `rpmBins` now starts at 500 (`1F4`), and the 500-rpm VE row governs fueling *precisely when RPM craters into a dip*. If it is left as a verbatim copy of the 842 row (its initial state) it is ~17% too rich there and bogs the engine. Lean it toward λ0.93. The 842 row and the 1184 idle row (~9% rich at steady idle, λ0.844) want the same treatment — **richness increases as RPM drops**, so the lean deepens toward the 500 row.

**Fuel is closed-loop down here — but do NOT tune VE from the trims.** The lambda trim is intentionally **slow and low-authority** (`Short term trim` clamped to ~±2–3 %, slow integration) so it does not jerk idle around. It therefore (a) cannot correct a fast dip in real time, and (b) will never reveal the true VE requirement. Set VE from **measured lambda error** — `VE_new = VE_old × (Lambda 1 / Lambda target)` — as a deliberate, gentle change, then verify on the next drive. Account for WBO transport lag: during a fast dip the reading trails the actual rpm/MAP, so treat per-cell numbers as a starting point and iterate. Per the conservative feed-forward principle below, apply ~80 % of the computed lean first. Lean **both** `veTable` (pump) and `veTable2` (ethanol) by the same ratio — the E60 blend uses both.

### 2. Airflow: fan-gated air drops out at speed (the depth)

The +13 % `idleCoolantFanCorr` is VSS-gated **off above ~56 km/h**. On a return from above ~56 km/h the base idle airflow is the bare ~26.5 % table value instead of ~39 % (fan-on), and the airflow PID is clamped at +12 — not enough to hold. Below ~56 km/h the fan is on and returns catch cleanly. Fixes that do **not** add idle variation: more airflow-PID authority (`idleAirPIDOutMax`/`idleAirFlowIntegralLimitMax`) and a faster `idlePIDUpdateInterval` (200 ms → ~50 ms). The fan +13 % itself is correct load-comp — leave it.

### What does NOT work

- **Raising the Active airflow table's 1000/1100 rows.** `idleActiveAirflow` is indexed by idle **target**, and the target floors at 1200 (`idleRPM` bottoms at 1200), so those rows are never read regardless of actual RPM. *Contrast:* the VE table **is** indexed by actual rpm × MAP, so its 500-rpm row **is** used when RPM craters — that is why the VE 500 channel is the right lever and the airflow 1100 row is dead.
- **VSS-scheduled idle-target bump** (`idleIncreaseTargetAboveVSS`): mechanically would work, but it adds a target step — rejected to keep low-speed heat-soak idle free of extra variables.

---

## Design principle: feed-forward should be conservative, PID does the rest

When calibrating any open-loop / feed-forward idle-air correction — `idleCustomCorrection`, fan/AC compensation, DSG creep correction, custom-output feed-forward — bias toward **under-correction**, not full correction. A useful default is to **apply roughly half the airflow change the engine actually needs** at the operating point and let the closed-loop PID ease in the rest.

**Why the asymmetry matters:**

| Failure mode | Cause | Severity |
|---|---|---|
| Feed-forward **under-corrects** | Engine briefly runs higher RPM than target while PID trims back down | Safe — PID has full negative authority, no combustion risk |
| Feed-forward **over-corrects** | Engine commanded toward less air than it needs; combined with transient lags (manifold fill, wall film, sensor lead/lag) can hit the actuator floor before PID can recover | Stall — engine off, restart required |

The cost of being too small is a temporary high-idle blip the closed-loop quickly resolves. The cost of being too aggressive is a stall — which interrupts driving, may strand the vehicle, and on a build with idle ignition retard can produce a hot-side cough.

**When this principle especially applies:**

- Feed-forwards keyed on **sensor proxies for the real physical state** (e.g. CAT used as proxy for throttle-body body temp — the sensor lags the body during transients; aggressive correction based on the sensor will over-correct during the lag window)
- Loads that arrive as **step changes** with their own time lag (cooling fan engagement, AC clutch, alternator step) — the airflow change must trail the load by less than the lag of the load's effect, or you over-compensate before the load is felt
- Any correction that crosses **stall margin**: at idle the throttle is already near the actuator floor; any feed-forward that closes the plate further has limited headroom before the floor

**Practical guideline for sizing:**

1. Determine the steady-state correction needed (from logging — what trim does PID converge on with no feed-forward?).
2. Halve it for the feed-forward table.
3. Verify in a log that PID's residual is now ~half of what it was, and not saturated.
4. Iterate: if PID still works hard in one direction, the feed-forward can grow toward the steady-state value — but never past it, and never aggressively at sensor edges (e.g. extrapolated cells).

**Where this changes calibration behavior:**

Before this principle was applied on this build, the `idleCustomCorrection` table was sized close to "full" steady-state compensation at the operating CAT band. PID sat at -9.75 % (saturated negative) at the worst log point (t=178.64, [supra/logs/20260526_1644.csv](../supra/logs/20260526_1644.csv)) with TPS only 1.1 % above the actuator floor. After converting to scalar mode and halving the corrections at the operating points, PID will have authority both directions and the worst-case stall margin grows.

---

## Universal Pre-Diagnosis Checklist

Before touching calibration, confirm:

- [ ] Wideband heats up and `Lambda is valid` goes to 1 within 30 seconds of start
- [ ] `Brake switch` channel reads 0 at idle with foot off brake
- [ ] `Trigger error count` = 0 (crank/cam signal issues destabilize idle)
- [ ] `VVT CAM1 status` = 0 (VVT fault causes breathing instability)
- [ ] `Engine protection code` and `Check engine code` = 0
- [ ] `Battery voltage` is 13.8–14.4 V running (a bad alternator load-dumps into idle)
- [ ] `Idle state` is 2 (PID active) during steady idle, not 0
