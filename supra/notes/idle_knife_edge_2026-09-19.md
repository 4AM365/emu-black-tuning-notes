# Idle knife edge, 2026-09-19 — hungry cold, hanging hot, "riding the negative DBW stop"

**Logs:** `EMU_BLACK_V3\Supra\LogAutosave\whencold.csv` (morning cold start, 602 s, CLT 32→107) and
`EMU_BLACK_V3\Supra\losingit.csv` (afternoon hot session, 509 s, CLT 91–118, IAT 56–63).
**Tune:** `EMU_BLACK_V3\Supra\fucquedup.xml.emub3`, exported 12:09 — *after* both logs, and the
losingit log carries **44 `Data changing` events** (edits at t = 11, 22, 56–72, 107–125, 203–243,
308–413, 430–494 s). Where a value mattered it was **derived from the log**, per the
match-the-log-to-the-calibration rule; the export is cited only for what did not change.
Baseline for comparison: `misc log csv\omg.csv` (2026-08-24, all channels) and
`goodlogwithclutch.csv` (2026-09-09).
Figures + running dataset: [`op_vs_dbw_1000rpm/`](op_vs_dbw_1000rpm/) — `losingit_timeline.png`,
`whencold_timeline.png`, `scatter.png`, `table.md`. Related: [`airflow_actuator.md`](airflow_actuator.md)
(the 09-08 duty→position floor work), [`oil_viscosity_idle_airflow.md`](oil_viscosity_idle_airflow.md)
R13–R15 (pressure axis is a clock, not a mechanism), [`op_vs_dbw_1000rpm.md`](op_vs_dbw_1000rpm.md).

## 1. Cylinder-out check — negative

Will's first question before chasing anything: is the map richer everywhere / is a cylinder out?
Compared `losingit` and `whencold` against `omg` (08-24) over `Lambda is valid`==1, CLT>80, no accel
enrichment, binned by region:

| region | log | n | λ meas | λ tgt | λ/tgt | STFT | EGT1 (cyl 3) | EGT2 (cyl 6) | MAP×RPM/k |
|---|---|---|---|---|---|---|---|---|---|
| idle | omg 08-24 | 8231 | 0.896 | 0.901 | 0.994 | +0.1 | 448 | 475 | 37.1 |
| idle | whencold | 2481 | 0.867 | 0.901 | 0.962 | −2.2 | 437 | 472 | 38.6 |
| idle | losingit | 5774 | 0.936 | 0.901 | 1.038 | +1.8 | 503 | 521 | 38.3 |
| light 1.5–2.5k, MAP 30–60 | omg | 1070 | 1.019 | 0.972 | 1.057 | +0.2 | 546 | 577 | — |
| light | whencold | 355 | 0.961 | 0.976 | 0.989 | −0.1 | 494 | 512 | — |
| light | losingit | 4624 | 1.005 | 0.953 | 1.056 | +5.1 | 600 | 612 | — |
| cruise 60–100 kPa | omg | 366 | 0.970 | 0.956 | 1.020 | +0.1 | 534 | 542 | — |
| cruise | whencold | 425 | 0.947 | 0.961 | 0.997 | −0.1 | 485 | 490 | — |
| cruise | losingit | 99 | 1.039 | 0.954 | 1.091 | +0.9 | 542 | 562 | — |

- **Per-cylinder knock-window voltage, idle, ratio to the six-cylinder mean** (a dead cylinder reads
  far below its usual share): omg `0.82 1.31 0.93 0.82 1.36 0.76`, whencold `0.76 1.28 0.99 0.87 1.22
  0.87`, losingit `0.84 1.23 0.95 0.84 1.35 0.79`. Same fingerprint, all three logs. Same at cruise.
- Idle RPM roughness (sd of 1-s-detrended RPM): 8.8 / 10.6 / 9.0. A dead cylinder is tens of rpm.
- Air the engine took at idle (MAP×RPM — the throttle is choked at idle MAP, so this is the mass-flow
  proxy) is **+3–4 % over the 08-24 baseline**, not the ~+20 % a dead cylinder costs.
- EGT on cylinders 3 and 6 both up ~55 °C in losingit — matches its 2.5° less idle advance and the hot
  day, and the 3↔6 delta is unchanged. `Trigger error` 0, `Knock count` 0, `Lambda 2` not fitted (0).

Mixture is not richer everywhere: losingit runs **~4–6 % lean of target** at idle/light load with STFT
adding +2…+5 %, whencold ~3 % rich at idle. Both are ordinary trims (fuel temp 39 vs 46 °C, ethanol 14 %
both). **No cylinder is out. Nothing here to chase.**

## 2. The engine's air demand is normal and repeatable — the numbers that moved are position numbers

Engine-side air at ~1000–1030 rpm, `Idle state`==2, ignition 17–19°, MAP 35–38 (all choked):

| when | OP [bar] | CLT | IAT | MAP×RPM/k | TPS holding it | `Idle air %` | `DBW Out. DC` |
|---|---|---|---|---|---|---|---|
| omg 08-24, hot | 2.0–2.5 | 96 | — | **36.4–36.6** | 3.7 | 24 | −34 |
| whencold, CLT 96 / oil still warming (t 331–364) | 3.6–4.1 | 96 | 31 | **38.2** | **5.9–6.1** | 62–67 (PID +8…+13) | −4…−28 |
| whencold, after a 2-min drive (t 422–495) | 1.69 | 101–104 | 35 | **35–36** | **4.8–5.0** | 46–51 (PID −7…+3) | −4…−35 |
| losingit C (t 119–138) | 1.88 | 98 | 62 | **37.0** | **4.5** (target 4.0, unreachable) | 30 (PID −25 railed) | −30/−35 pinned |
| losingit G/H (t 420–500) | 1.69 | 102–103 | 60 | **36.0–36.1** | **4.8–5.1** | 48–51 (PID −0.1…+2.6) | −10…−26 |

Read across: the engine took **36–38.5 k** in every hot row on three different days, and the cold-oil
rows (3.6–4.1 bar) took only **~7 % more** than the hot-soaked rows (1.7 bar). That is the whole
oil-viscosity friction term at this RPM and it is modest. Meanwhile the **plate position** delivering
that air ran 3.7 → 4.5 → 5.0 → 6.0 depending on the day and the hour, and `Idle air %` ran 24 → 67.

So: *"super hungry for airflow"* and *"needs even less air than I've ever seen"* are both true **of the
position command** (`Idle air %` is a position through `idleDBWTargetMin/Max`; `Idle effective DC` is the
same number) and both false of the air. The engine consumed the same air. Two other things moved.

### 2a. The sustaining position tracks the oil-temperature clock, ~1 % TPS per day

Same 1025 target, same coolant column (CLT ≥ 96 → `idleActiveAirflow` is flat by construction):

| OP [bar] | sustaining TPS | in the 2.0–8.0 airflow frame |
|---|---|---|
| 3.6–4.1 (morning, oil not yet hot) | **5.9–6.1** | 65–68 % |
| 1.7 (both logs, oil hot) | **4.8–5.0** | 47–50 % |

Roughly **1.0 % TPS ≈ 17 airflow-%** between "coolant on the stat, oil still warming" and "everything
soaked". The engine-side air explains ~0.35–0.4 % TPS of that (7 % more flow at TPS ≈ 5); the remainder
is the plate passing more air per % TPS as the throttle body heats (bore outgrows plate — the direction
[`throttle_body_thermal_growth.md`](throttle_body_thermal_growth.md) predicts). Whether the split is
40/60 or 60/40 does not matter for tuning: **the CLT axis cannot see any of it**, because CLT pins at 96
minutes before the oil and the throttle body finish heating. That is the knife edge Will described:
a cold value that idles is ~1 % TPS above the hot value that hangs, on the same CLT column. The
oil-pressure custom correction was built for exactly this and is disabled (`Idle airflow custom corr.`
logs 0; see memory *project_supra_oil_viscosity_idle_adder*).

Oil pressure being "lower than usual" (1.5–1.9 bar at hot idle vs 2.0–2.5 on 08-24) is thinner oil on a
hot day, and it *reduced* the air the engine needed (36.1 vs 36.5 k). It is not the oil pump.

### 2b. The DBW servo cannot reliably reach positions below ~5.5 % TPS — and the stall point wanders

`DBW Out. DC` pinned at the clamp (`dbwMinDC`, edited live during the session: −35 → −30 at t≈125,
−35 at t=373.5, −40 at t=377.7) with the plate parked above the commanded position:

| losingit t [s] | clamp | plate parked at (TPS p10/med) | commanded | RPM | MAP×RPM/k | note |
|---|---|---|---|---|---|---|
| 120–125 | −35 | 4.40 / 4.50 | 4.00 | 1002 | 37.0 | on target by luck — this is the sustaining position |
| 125–138 | −30 | 4.40 / 4.50 | 4.00 | 998 | 36.4 | clamp raised, plate stayed (hysteresis) |
| 168–215 | −30 | 8.2 / 8.3–8.6 | 6.0–6.2 | 2000–2500 | 64–68 | coast / return to idle, plate 2 % above command |
| 217–258 | −30 | 5.40 / 5.60 | **3.50** | 1044 | 39.3 | RPM hangs 20–40 over target with 5° retard; PID railed −25 |
| 295–373 | −30 | **7.40 / 7.50** | 3.9 → 2.4 | 1848 | 60 | 78 s: armed, pedal off, target walked down to 2.4 by live edits — plate never moved |
| 373.8–377.4 | −35 | 7.20 / 7.40 | 3.6 | 1847 | 60 | −35 bought 0.1 % |
| 377.9–379.0 | **−40** | **3.60** | 3.6 | 1791 → **396** | — | plate released, reached the command in 0.8 s; engine choked; PPS rescue at 379.9 |
| 469–496 | −26…−35 | 4.80 | 4.7–4.8 | 1027 | 36.0 | tracking again, holding 4.8 on −26…−35 |

Same servo on 09-09 (`goodlogwithclutch`): −35 parked the plate at 4.5–5.4 at ~1010 rpm, target 4.3–4.6.
Same servo on 09-08 ([`airflow_actuator.md`](airflow_actuator.md)): −35 → floor 4.80, holding 6.0 cost −7.

So the closing duty the plate needs is **not a function of position**: today −30 held 5.6 at one moment
and could not get below 7.5 twenty minutes later; on 09-08 −7 held 6.0. The stall point ranged **4.5 →
8.6 % TPS at the same duty inside one 8-minute window.** The log cannot say whether that is motor torque
(winding temperature: copper ≈ +0.4 %/°C resistance, so a hot motor gives less torque per duty),
gear-train / shaft friction, or plate aerodynamics at high vacuum (the 7.5–8.6 stalls are all at
MAP 33 and 1850–2500 rpm; the 4.5–5.6 stalls at MAP 37–38 and ~1000 rpm — flow-correlated, but the
09-09 log had −35 reaching 4.8 at 1768 rpm, so flow alone does not explain it). **Hypothesis, not
measured.** What is measured: TPS voltage → TPS % is a fixed linear cal (resid 0.15 %), `DBW HW state`
constant 4, `TPS check error` 0, ECU 42–44 °C, Vbat 13.2–13.4 — no fault flag, no sensor drift.

**The hot-soaked sustaining position (4.8–5.0) sits inside the band where this servo is unreliable.**
That is why a clamp at −30 hangs the idle (plate stuck open at 5.6–7.5, RPM +20…+800, ignition PID
retarding 5°, airflow PID wound to its rail) and a clamp at −40 chokes it (plate slams to whatever the
wound-down command says). No `dbwMinDC` value is right for a mechanism whose stiction wanders 25 duty
points — the 09-08 conclusion, reconfirmed with the choke as the counter-example.

## 3. Why the PID "winds up" — actuator-saturation windup, bounded at the integral clamp

The airflow PID commands a position; it does not know the servo is saturated. Whenever the plate is
parked above the command and RPM stays above target, the integral keeps accumulating toward
`idleAirFlowIntegralLimitMin` and the output sits at `idleAirPIDOutMin` (both read −25 in the export;
the log confirms −25 as the rail at t 122–138 and 220–258). −25 airflow-% is ~1.5 % TPS in the current
frame. It is *not* the PID being mis-gained — the plant stopped responding, and the loop did the only
thing an integrator can do. The dangerous part is what happens when the servo suddenly *does* respond
(t=377.7): the wound-down command is already ~1.5 % below the parked position, so the plate goes
straight through the sustaining position. That was the first death (RPM 396 at t=379.9; recovered
on the pedal — the log does not show an engine stop).

The cold side is the mirror image. `whencold` t 37–172 (CLT 33–66, OP 7.25–6.7, target 1500): RPM held
**1417–1480, 20–80 short of target**, `Idle air %` 87 → 75 with the PID at **+24 → +18**, and the
**I term parked at +15 = `idleAirFlowIntegralLimitMax`** for the whole 135 s (P supplied the rest,
+9 → +3). The plate was at 7.0–7.2 and tracking (duty −13…−27, not pinned), so this one is a genuine
shortfall. Base = `Idle air %` − PID ≈ 63 at CLT 33–37, which matches the 1500 row of the **09-15
export** (raw `92 8C 80 7A …` → 73/70/64/61 at CLT 0/15/30/45), so that table was live; the cold engine
wanted ≥ 87 and was still 20–80 rpm short, so the cell was **≥ 24 airflow-% low** and the positive integral
clamp bit first. `fucquedup.xml.emub3` carries that row raised +4…+7 (raw `9A 94 8E 88 …` → 77/74/71/68) —
Will's morning edit — still ~15–20 short of the +18…+24 the PID was carrying.

Both rails are the same lesson: the ±25 output window and the −25/+15 integral window are about 1 %
TPS of authority each way, and the day-to-day span of the sustaining position at the hot column alone
is ~1 % TPS (§2a), before any cold-cell error or servo stall.

## 4. What was live vs what the export says

Derived from the logs (authoritative for those instants), against `fucquedup.xml.emub3`:

| parameter | log-derived | export | note |
|---|---|---|---|
| `idleDBWTargetMin` | 2.4 until t≈345 (losingit), then 2.0, then **0.0** at t 370–380, then 2.0 from t≈418 | 2.0 (raw 20) | fit of `DBW target` vs `Idle air %` per segment: 2.60/2.08/2.40/2.03/1.99 intercepts, slope ≈ 0.055–0.059 |
| `idleDBWTargetMax` | 7.7–7.9 | 8.0 | same fits |
| `dbwMinDC` | −35 → −30 (t≈125) → −35 (373.5) → −40 (377.7) | −40 | pinned-duty value per episode |
| `idleRAMPDownOffset` | 200 → 100 → 10 → 200 | 200 | `Idle ramp down offset` channel |
| `idleAirPIDOutMin` / `IntegralLimitMin` | −25 | −25 / −25 | rail value |
| `idleAirFlowIntegralLimitMax` | +15 | +15 | I-term plateau in whencold |
| `idleActiveAirflow` 1000-row CLT-96 cell | base ≈ 55 at t 8–138, ≈ 45 at t 220–258, ≈ 48–52 at t 420+ | 53.0 (raw 6A) | `Idle air %` − PID in settled windows; Will was editing it |

The 1000-row hot cell has been ~49–55 airflow-% (≈ 5.1–5.5 % TPS) across the 09-15 export, this
export and the live edits — i.e. it has been sitting right on the hot-soaked sustaining position (4.8–5.0
at 1.7 bar) minus a few tenths, which is why the hot idle needs −5…−25 of PID and why lowering it any
further starves the morning. The table's CLT axis has nothing to offer here; see §2a.

## 5. What this log cannot resolve, and the one measurement that would

- Whether the servo's variable stall torque is thermal (motor), mechanical (gear train, shaft, plate
  edge) or aerodynamic. A **duty sweep at hot idle** — EMU's DBW test, or stepping `dbwMinDC` in 2-point
  steps with the engine hot and the target held far below the plate — gives the duty→position curve
  directly; repeating it cold and after a 20-minute soak separates thermal from not. The 09-08 note
  asked for the same sweep.
- Whether `Idle air %`-vs-OP slope in §2a is plate leakage or MAP×RPM under-reading the flow change.
  Irrelevant to the tuning conclusion (the CLT axis sees neither), relevant to the TB-swap decision.
- The Bosch TB swap already on the list (memory *project_supra_bosch_tb_swap*) replaces the mechanism
  this note is describing; it would also invalidate every duty and position number here.

## 6. Bottom line

1. **No cylinder out; mixture ordinary.** Stop looking there.
2. **The engine's idle air demand is normal** (36–38.5 k MAP×RPM at ~1000 rpm on every day measured).
   Hungry/starved/hanging are position-domain symptoms.
3. **Two independent things move the sustaining plate position** on the CLT-96 column: the oil/TB
   temperature clock (~1 % TPS between "coolant on stat" and "soaked") and the DBW servo's wandering
   stall point (up to 4 % TPS at a fixed duty). The airflow PID has ~1 % TPS of authority each way. The
   knife edge is structural, not a wrong number in a table.
4. **The PID winds to its rail because the plate does not follow its command** — bounded windup, and
   the choke at t=379 is what the wound-down command does when the servo finally lets go.
5. Anything done in the tune (tables, clamps, `dbwMinDC`) moves the problem between the morning and
   the afternoon. The mechanism-level fixes are outside the tune: the servo (sweep it, or swap the TB)
   and an open-loop term that can see the oil/TB clock (the disabled oil-pressure correction, gated so it
   never fires on a warm restart — [`oil_viscosity_idle_airflow.md`](oil_viscosity_idle_airflow.md) §15.5).

## Postscript, same evening — resolved

The wandering stall point (§2b) and the open mechanism question (§5) were **carbon fouling of the throttle body**. Will
cleaned it that afternoon; the plate then followed its command (stuck-above-command time 20 % → 1.5 %, zero
duty-pinned episodes) and the hot sustaining position fell 5.9 → 2.9/2.4 % TPS (new frame — a DBW relearn the same afternoon shifted TPS by −1.09). The engine-off duty sweep asked for in §5
was also run: break-away closed at −28…−31 % duty, rest 6.3–6.6. Full analysis and the re-cut 1.5–6.5 window:
[`tb_clean_2026-09-19.md`](tb_clean_2026-09-19.md). §2a (the oil/TB clock, ~1 % TPS per hot soak) **stands** — it
reappeared unchanged on the clean TB.
