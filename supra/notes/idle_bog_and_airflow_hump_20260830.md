# 2026-08-30 — return-to-idle bog anatomy + the "airflow requirement hump" resolved

Status: **bog mechanism closed and fixed; hump attributed to the oil-pressure correction table
fighting the airflow PID.** Adversarial verification did NOT run (3 verify agents died on a spend
limit), so everything here is single-pass measurement — solid arithmetic, unreviewed conclusions.

Logs: `latestdrivevischan.csv` (2026-08-30, 2170 s, 17 channels), `bogevent.csv` (same drive,
t 1383.7–1392.1, all 564 channels), `omg.csv` (2026-08-24, 565 ch), `added features.csv`
(2026-08-27). Tune: `newtune.xml.emub3` (post-drive) — **live edits happened mid-log**, so every
threshold below is derived from the log, not read from a file.

## 1. The bog is four subtractions stacked on one descent

Anatomy of the t≈1387 event (rolling ~30 km/h, neutral, pedal lift at 1816 rpm):

| # | subtraction | measured |
|---|---|---|
| 1 | **clutch-release target cliff** | target 1902→1697 (−205) at clutch 1→0; PID +5.38→−1.50, ign +7.0→−3.0, command **52.5→43.5** |
| 2 | **A/C-disengage target cliff** | target 1662→1472 (−190); PID +5.44→+0.63, command **47.5→38.0** |
| 3 | **`Idle force open loop` chatter** | 20 edges / 4.5 s, ten wipes; each pins air to base and ignition to 18° |
| 4 | **DBW close-floor lag** | `DBW Out. DC` held −35 for ~0.5 s past the point TPS crossed below target; plate undershot to 2.8 % |

Target arithmetic confirmed exactly against `newtune.xml.emub3`: entry 1957 = base **1225** + ramp
**347** + `idleClutchTrgtRPMIncrease` **200** + `idleACRPMIncrease` **185**; after clutch release
1225+287+185 = **1697**; after A/C drop 1225+247 = **1472**.

**The clutch cliff is dishonest, the A/C cliff is honest.** At the clutch release the fall rate went
**−158 → −683 rpm/s** while MAP (37→27) and `Estimated airflow` (9.8→6.1) declined smoothly through
it — no load event. At the A/C drop the fall rate barely moved (−920 → −857). In neutral the clutch
was already decoupled, so releasing it changes nothing the engine feels; the ECU deletes 200 rpm of
setpoint and ~9 points of air anyway. Corroborated by [clutch_idle_load.md](clutch_idle_load.md)
(clutch load ≈ 1/15 of A/C).

Across the whole drive: **51 hot-ACTIVE target drops >50 rpm, every one of them 175–205** (36 clutch,
15 A/C). Median subsequent RPM drop **361**; 10 of 51 went under 680; the worst (t=639.7, −205 at
1577 rpm) **is the log's one true stall**.

## 2. Two independent wipe paths, both confirmed

- **VSS gate.** Above threshold the ratio-based gear estimator is *structurally* blind to neutral:
  in a decoupled coast RPM free-falls while VSS holds, so `Gear speed to RPM ratio` sweeps
  0.366→0.878 in one second and marches 2→3→4→5. VSS was **clean** in that slice (max 7.8 km/h/s,
  zero glitches) — this is not a signal problem and cleaning VSS will not fix it. Discriminating
  test on `omg.csv` (ACTIVE, >46 km/h, clutch out): true neutral → force cleared **10/10**; a real
  gear → force asserted **183/194**; gear *unknown* → cleared **198/203**. So the ECU treats
  "can't determine gear" as neutral, and `Neutral enables closed loop` is the flicker path.
- **Any exit from `Idle state` 2.** Unambiguous case with `Idle force open loop` = 0 throughout —
  t=519.76: 807 rpm vs a 1025 target, PID **+22.94**, ign +15.5, angle 34°. A **0.24 s** pedal tap
  → state 2→4 → on re-entry PID restarts at **+7.56**, ign correction **0.0**, angle collapses
  **34°→18°**, RPM falls to **343**. A rescue blip is itself a wipe.

## 3. Derived control constants (from the log — re-derive, don't carry forward)

- `idleAirFlowKP` = 717/1024 = **0.7002**; verified exactly: `Monitored P term` = 0.7002 × `Idle
  ignition correction`, so P rails at 0.7002 × 17 = **11.902** (the ignition rail sets the airflow
  P rail).
- Integral recovered as I = correction − 0.7002×ignCorr: range **−4.19 … +12.17** over the drive,
  pinning `idleAirFlowIntegralLimitMin`/`Max` at **−4 / +12 airflow %**. `idleAirPIDOutMax` (25) is
  never reached — the true ceiling is P_max + I_max = **23.9**.
- Airflow→TPS actuator map, regressed over settled samples: **TPS = 2.4 + 5.6 × (airflow %/100)**
  (residual mean +0.04, sd 0.46, n=128 with `DBW Target source` = Idle). So a wipe from airflow 46
  → 32 costs **0.8 %TPS out of a 5.6-point band = 14 % of total idle authority, instantly.**
- `DBW Target source` enum (help, `docs/emu-black-help/DBW.md`): 0 Target table, 1 Override,
  **2 Idle**, 3 Idle blend, 4 DSG blip, …

## 4. The airflow-requirement "hump" is the oil-pressure table fighting the PID

`omg.csv`, settled hot idle, `Idle target` = 1200, CLT ≥ 94, t 300–520 s, base flat 27.6–27.8
(n = 4000 samples), regressed against `Engine oil pressure` over 3.3–4.6 bar:

| term | slope vs oil P |
|---|---:|
| `Idle airflow custom corr.` (the oil table) | **+3.88 %/bar** |
| `Idle PID air % correction` | **−3.91 %/bar** |
| base (`Idle air %` − PID − corr) | +0.04 |
| **total `Idle air %` (the actual requirement)** | **+0.01 %/bar** |

**The engine's requirement is flat against oil pressure in this band. The table removes ~3.9
points per bar and the PID puts back ~3.9.** Perfect cancellation, no net effect on the engine —
except that the PID trace now carries the table's decay curve inverted. Binned: PID walks
**+5.29 → +11.09 (t≈420) → +9.47**, then eases as oil pressure falls under the table's knee and the
table output goes to zero. **That walk-up-then-settle-back IS the hump.** It lives in the PID
channel, not in the engine.

Live table shape recovered independently from `added features.csv`:
**corr ≈ clip(4.3·(P − 2.03), 0, 13)** — and hot idle oil pressure sits at **1.75–2.25 bar**, right
on the zero knee, so the table has no authority in the band where the real drift happens.

### ⚠ This corrects [oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md)

The **5.45 %/bar** slope in that note is **not reproduced** and is contradicted here. Cause: in a
single warm-up-to-hot drive every candidate is monotone in time — measured
r(oilP, runtime) = **−0.99**, r(oilP, charge temp) = −0.99, r(oilP, Vbatt) = +0.97, full-model
**VIF 150** — so nothing is identified and the fitted oil coefficient flips sign depending on what
you condition on (−1.11 %/bar at target 1200, +4.18 at target 1000). The earlier slope attributed a
**time-decay** to oil pressure. Corroborating: over the window where the table output was
identically zero, oil P moved only −0.157 bar (worth −0.55 points) while the requirement fell
**−5.4 to −5.7** — ~90 % of the late fall is not oil pressure.

## 5. What the requirement actually does

Not a hump — a **slow monotone decline** with time-hot plus discrete step excursions:
−0.43 %air/min over 22 min (`added features.csv`, R² 0.56, quadratic rejected: vertex is a
*minimum* at 56 min) and −0.24 %/min (`latestdrivevischan.csv`), with **+5 to +7 point** excursions
riding on it (t≈622–637 sustained 27 s; t≈1637–1677). Total swing ~6–8 points; no single base value
covers it. Eliminated as drivers: CLT (plateaus at 96, R² 0.010), coolant fan (constant on through
every settled run), charge temp (wrong sign, and collinear with elapsed time), MAP (nearly flat,
inverts on one episode), ignition loop (absorbs none of it, ±0.55° across a 7.5-point airflow swing),
alternator/battery (voltage falls monotonically with no recharge-taper knee).

Ranked candidates for the residual (theory pass, all citing repo notes): bulk-oil + structure soak
(largest measured amplitude, **reset by driving** — which is exactly why interleaved drive/idle
*looks* like a hump); TB differential thermal growth (**0.23 airflow %/°C** of casting temp,
Al bore outruns SS plate); charge-temp density (the only rise-signed term). Discriminator already
logged: **MAP at fixed RPM** separates demand-side terms (MAP moves with the command) from
throttle-gain terms (MAP stays put).

**Single channel that would settle it: throttle-body casting metal temperature.** No proxy exists —
CLT pins at 96, charge temp is air not metal, oil pressure is 91 % RPM at hot idle, and
`Engine oil temperature` is **dead (identically zero — no sensor configured)**. Free runners-up:
`Back pressure` (EMAP, already wired, the only way to test residual-dilution at idle) and
`AC Clutch`.

## 6. Fixes, in the order the evidence supports

1. **`idleOpenLoopOverVss` = 400** (done) — stops the wipes. Measured: min ACTIVE RPM **835** and
   zero sub-800 samples after t=1679, vs min **298** and 345 sub-680 before.
2. **`idleClutchTrgtRPMIncrease` → 0.** Removes the dishonest cliff; costs almost nothing.
3. **Trim `idleActiveAirflow` rows 1000/1250 by ~5 points** (41.5→~36, 43.0→~38); leave rows
   1500/1750/2000 alone — those are the catch. Evidence for over-airing: at base 41 the integral
   sits on its −4 rail **31 %** of settled hot time and the ignition parks **1.5° retarded**
   (angle 16.5 vs target 18.0). At base 30–33 the ignition was dead-centred and RPM sd was **28.4**,
   the best in the log.
4. **Leave `idleCustomCorrection` (oil) at zero.** Measured net effect on the engine: +0.01 %/bar.
   Re-introduce only from a dedicated hot-coolant/cold-oil restart case, shaped from that case alone.
5. **Don't rescue a bog with a pedal blip** — it wipes both loops (§2).
