# Airflow / Idle DBW — live calibration reference

Current state of the Airflow-Actuator + idle DBW system. Keep this updated when values change.
Full table data lives in the `.emubt` files and in `supra export 05222026 (2.4-8.0 range).xml.emub3`
(that XML is a reference snapshot only — actual changes are made in EMU).

- **Last updated:** 2026-09-19 (throttle body cleaned; window re-cut — see [`tb_clean_2026-09-19.md`](tb_clean_2026-09-19.md). Airflow tables below are STALE — read the current XML)
- **Actuator range:** **`[1.5%, 6.5%]` TPS** per `supra export 09192026 post-tb-clean.xml.emub3` (`idleDBWTargetMin`/`Max` raw 15/65), live in the log from ≈1040 s on 09-19. History: `[2.0, 8.0]` (09-19 morning), `[2.4, 8.0]` (05-22 → 09-15), `[3.5, 8.0]`, original `[2.0, 6.4]`. `dbwMinDC` is now **−100** (was −35 / −40).
- **Change history:** see `cranking_and_idle.md` → Change log.

> **Measured hot-idle airflow requirement vs oil temperature:**
> [oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md) — cold-oil/hot-coolant needs
> 51–58 airflow %, hot-oil 28–31 %; sizes the oil-temp table replacing `idleCustomCorrection`.
> That note also independently confirms the **2.4 / 8.0** window below, recovered by regressing
> logged `TPS` on `Idle air %` in every log from 2026-05-24 to 07-30.

## Actuator range (the airflow→TPS mapping)

`TPS% = floor + airflow% / 100 × (ceiling − floor)`

| symbol | raw | scale | = | meaning |
|---|---|---|---|---|
| `idleDBWTargetMin` | 24 | 0.1 | **2.4%** | range floor |
| `idleDBWTargetMax` | 80 | 0.1 | **8.0%** | range ceiling |

Width = 8.0 − 2.4 = **5.6**. (Old width 3.5→8.0 = 4.5.)

## Airflow-% encoding

- ubyte airflow-% tables: **0.5/count** (raw = 2 × displayed %). e.g. raw 130 = 65.0%.
- `idleDBWTargetMin/Max`: word, **0.1/count** (TPS %).
- `idleCustomCorrection`: sbyte, **1:1**, signed, **additive** (mode is configurable in EMU; currently additive).

## Airflow-% tables (displayed %, current = post 2.4–8.0 rescale)

### Active state air flow `idleActiveAirflow` — X=Coolant °C, Y=Idle RPM
| RPM\CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 82.5 | 76.5 | 69.5 | 67.5 | 66.0 | 65.0 | 65.0 |
| 1375 | 86.0 | 81.0 | 71.0 | 61.0 | 61.0 | 61.0 | 60.0 | 60.0 |
| 1200 | 81.0 | 75.0 | 63.5 | 52.0 | 50.0 | 50.0 | 49.5 | 49.5 |
| 1100 | 74.5 | 69.0 | 56.0 | 40.0 | 37.5 | 36.0 | 37.5 | 37.5 |
| 1000 | 65.0 | 60.0 | 50.0 | 35.5 | 32.5 | 31.5 | 31.5 | 31.5 |

### Armed state air flow `idleArmedAirFlow` — vs RPM (8 bins)
`39.0  45.0  50.5  54.5  58.0  60.0  62.5  63.0`

### Cranking airflow `idleCrankingDC` — X=Coolant °C 0/33/67/100 (cold→hot)
`13.0  12.5  12.0  11.5`  (cold cell = 3.13% TPS — the cold-crank vacuum anchor)

### Custom air flow correction `idleCustomCorrection` (additive %) — X=IAT °C, Y=Idle RPM
| RPM\IAT | 20 | 30 | 40 | 60 | 70 |
|---|---|---|---|---|---|
| 1500 | 1 | 0 | -3 | -10 | -14 |
| 1375 | 2 | 0 | -5 | -15 | -20 |
| 1200 | 2 | 0 | -7 | -22 | -30 |
| 1100 | 2 | 0 | -9 | -26 | -35 |
| 1000 | 2 | 0 | -10 | -31 | -40 |

## Airflow PID (output is airflow %, scales with range width)

**Live values verified 2026-07-17** against the EMU `Idle → Airflow → Airflow PID` dialog and the
June 29 XML. Raw = tune-file storage; displayed = what EMU shows.

| symbol | raw | EMU displays | note |
|---|---|---|---|
| `idleAirFlowKP` | 2048 | **2 %/°** | scale **raw/1024** |
| `idleAirFlowKI` | 205 | **0.2002 %/(°·s)** | scale **raw/1024** |
| `idleAirFlowKD` | 0 | **0 %/(°/s)** | no derivative brake — see caveat below |
| `idleAirFlowIntegralLimitMin` | -4 | **-4 %** | direct (1:1) |
| `idleAirFlowIntegralLimitMax` | 12 | **12 %** | direct |
| `idleAirPIDOutMin` | -6 | **-6 %** | direct |
| `idleAirPIDOutMax` | 15 → **25** | **25 %** | **raised 2026-07-17** (was 15) |

**Gain scale = raw/1024, verified empirically on two independent values** (2048/1024 = 2 exactly;
205/1024 = 0.20019… = displayed 0.2002). Limits and output clamps are direct 1:1 with %.

**The gains are dt-normalized — read the units.** `%/°`, `%/(°·s)`, `%/(°/s)`: I and D carry explicit
time units, so EMU integrates `e·dt` and differentiates `Δe/dt` in real time.

**⚠ `idlePIDUpdateInterval` (=200) is inert — not a lever.** The idle airflow PID measurably runs
**~40 ms**, not 200 (hold-length histogram of `Idle PID air % correction` in the July 17 logs peaked
at 1 sample with no spike at 5). The symbol is a v2 relic or unexposed internal: undocumented in all
23 v3 help pages, absent from the Airflow PID dialog, frozen at 200 across every tune export, orphaned
in the XML at line 433 beside `starterOutput`/`enableBuzzerOnStartup`. **The only real delay in this
loop is the ~160 ms DBW actuator lag.** Full evidence:
[idle_drive_wobble.md](idle_drive_wobble.md) §2026-07-17.

**⚠ The range-rescale of the gains was never applied.** When the actuator range widened 4.5 → 5.6 %
span, this file previously carried proposed rescaled gains (KP 2048→1646, KI 205→165, ×4.5/5.6).
The tune shows **KP still 2048 / KI still 205** — the proposal was never written to the ECU. Because
PID output is airflow-% and a wider range makes each airflow-% worth more throttle, the effective
loop gain is running **~1.24× (1 ÷ 0.8036) hotter than the pre-rescale calibration intended**. Worth
weighing against the observed limit-cycle hunting; not yet changed either way.

**⚠ `KD` = 0** with the ~160 ms DBW lag leaves no derivative brake on large transients — the known
under-damped-single-swing caveat in [`notes/idle.md` → Airflow PID](../../notes/idle.md).

### Measured loop stability margin — 2026-08-24

`cranking_channels_recent_run.csv`, post-start idle t = 5–137 s, idle state 2 throughout.
Method + tooling: [`notes/idle.md` → Setting `idleAirFlowKP` from a logged
oscillation](../../notes/idle.md) and
[emu-black-idle-pid-gain](../../skills/emu-black-idle-pid-gain/SKILL.md).

| quantity | measured |
|---|---|
| `idleAirFlowKP`, **from the log** | `Idle air % = 11.97 + 1.976 × Ignition Angle`, R² = 0.816 → **1.98 %/°** |
| closed-loop pole | decay ratio **0.800**/cycle (n=3: 0.80/0.80/0.82), period **1.58 s**, ζ = **0.0355** |
| total loop deadtime L | **0.42–0.51 s** across τ = 0.40–1.10 s |
| **kP/Ku** | **0.907–0.918** — near-invariant across τ, so the margin is trustworthy without knowing the plant |
| ultimate gain / period | **Ku ≈ 2.16 %/°**, **Tu ≈ 1.50 s** |
| **gain margin** | **1.09 = 0.8 dB** |

**The airflow PID is running at ~91% of ultimate gain.** That is a stability-margin problem,
not a comfort one — 0.8 dB is consumed by any condition that raises plant gain.

Three readings that fall out of the same log:

- **The regression independently confirms KP = 2048 raw is live** on this date, so the
  never-applied range-rescale above is still not applied. Had it been (KP → 1646 = 1.607 %/°),
  the loop would sit at **0.74·Ku** — decay ratio ~0.46, ζ ≈ 0.12. Still hot, but not on the
  edge. The missing rescale is a direct contributor to the observed limit-cycle hunting.
- **The cascade itself is healthy.** Settled `Ignition Angle` = **17.99° ± 1.31** against
  `idleIgnitionTargetTbl` = 18.0° warm — the airflow loop is holding target to a hundredth of
  a degree. Only the gain is wrong.
- **The residual idle wander is the P term, not combustion.** In a short settled window
  `sd(air%)/sd(ign)` = **2.57** ≈ kP: the P term is converting normal ignition-PID jitter into
  ±3.4% of continuous throttle motion. It scales linearly with kP.

The fitted **L is total loop deadtime** — DBW travel + manifold transport + induction-to-torque
+ the ignition PID's own response — *not* DBW actuator lag alone, so it does not contradict the
~160 ms DBW figure above.

**Transient spanned `Idle air %` 34 → 67 = 33 points**, against a structural ceiling of 34.4
(P 22.4 + I 12) from the sizing section below. The loop was using essentially its entire output
range, and that ceiling was sized around kP = 2 — **re-derive it if kP changes.**

**Proposed (not applied — Will enters tune changes):** kP ≈ **0.6 %/°** (raw 614), ≈ 0.28·Ku →
decay ratio 0.013–0.031/cycle, ζ ≈ 0.48–0.62, one small overshoot, settling ~2 s instead of
20+, residual throttle dither cut to 0.30×. ZN's 0.5·Ku (≈ 1.08) is the textbook number but
targets quarter-amplitude decay, which is too hot for the *outer* half of a mid-ranging pair.
KI needs no compensating change — cutting kP raises the P/I crossover, so relative integral
authority increases. `KI`/`KD`/limits above are **2026-07-17 readings and unverified on this
date** — re-read them from the current XML before changing anything.

### Sizing `idleAirPIDOutMax` — size it against the window, not as a round airflow-%

The clamp is in **airflow %**, so its throttle value is set entirely by the actuator window width.
With the current `[2.4, 8.0]` range:

```
gearing   = 5.6 % TPS / 100 airflow%  =  0.056 % TPS per airflow-%
hot base  = 4.4 % TPS  =  (4.4 − 2.4)/5.6 × 100  =  35.7 airflow%
clamp +15 → 4.4 + 15×0.056 = 5.24 % TPS   (matches randomlydied.csv, logged 5.3)
clamp +25 → 4.4 + 25×0.056 = 5.80 % TPS
clamp +50 → 4.4 + 50×0.056 = 7.20 % TPS
```

**Superseded — do not size against the window ceiling.** An earlier revision of this note recommended
a clamp of 50–55 on the reasoning "reach 80–90 % of the window." That is the wrong constraint: the
airflow PID's own P and I terms bound the output well below the window, so a clamp above ~35 is inert
decoration. Correct sizing is the structural-ceiling derivation below.

### The structural ceiling — why `idleAirPIDOutMax` above ~35 does nothing

**The airflow PID cannot see RPM.** Its error signal is ignition-angle error,
`(current angle − idleIgnitionTargetTbl)` — `docs/emu-black-help/Idle.md:271`, and `Idle.md:197`
explains the intent (the two loops cooperate instead of fighting). The RPM-error loop is the *ignition*
PID; airflow is its slave. So maximum airflow output is set by how many degrees the ignition PID can
present, not by the actuator window:

```
warm ign target @1000 rpm   18.0°   idleIgnitionTargetTbl, CLT 96/130 rows
max torque angle @1000 rpm  ~29.2°  idleIgnitionMaxTorqueAngleTbl, interp 30.0@800 / 29.0@1067
max presentable error       11.2°
P = idleAirFlowKP 2 %/° × 11.2°  = 22.4 airflow%
I = idleAirFlowIntegralLimitMax  = 12   airflow%
──────────────────────────────────────────────
structural ceiling               34.4 airflow%
```

**Therefore `idleAirPIDOutMax` = 35.** Anything higher is unreachable unless KP or the integral cap
moves first. (15 and 25 both clip well under the ceiling — 25 wastes 9.4 airflow% of available authority.)

**⚠ Unverified assumption in the 22.4 P-term:** this assumes the ignition PID can actually drive the
angle all the way to `idleIgnitionMaxTorqueAngleTbl`. But it has its own clamps — `idleIgnitionKP` = 10,
`idleIgnitionKI` = 1, `idleIgnitionIntegralLimitMin/Max` = −5/+5 — and the scaling of KP and of that
±5 (degrees? counts?) is **not yet established**. If the ignition PID's own P+I ceiling lands short of
the max-torque table, the presentable angle error is smaller than 11.2° and the whole structural
ceiling drops proportionally. **Verify before trusting the 34.4 number**: log `Idle ignition correction`
(or the ign-angle channel) during a hot return-to-idle sag and read the peak angle actually reached
against the 29.2° table value. Until then treat 34.4 as an upper bound, not a measurement.

### CLT-sensor-failure redundancy — the case that sets the requirement

`failSafeCLTValue` = **105 °C** (`supra/exports/ind deadtime rescale.xml.emub3:84`; was 80, changed
some time before the 05-26 export). Note: **not 96 °C** — 96 is a `cltBins8` axis bin, easy to conflate.
On CLT failure the ECU limp-substitutes a temperature *hotter* than normal operating temp, so a
genuinely cold engine gets fully-hot feedforward. The airflow PID is the only thing left to rescue it:

```
needs (idleActiveAirflow, 1000 rpm row, CLT 0 cell)    65.0 airflow%
gets  (same row, CLT 105 cell)                         31.5 airflow%
deficit                                                33.5 airflow%   → +1.88 % TPS (4.28 → 6.15)
```

Target RPM also derives from CLT, so the failure keeps you in the hot-target row — the deficit is a
clean column-to-column read, and 6.15 % TPS is comfortably inside the 8.0 ceiling. The *window* is not
the limit here; the PID terms are.

**34.4 available vs 33.5 required is a 0.9 airflow% coincidence, not a margin.** To make the redundancy
real the binding term is the integral cap, not the output clamp — a sustained deficit is carried by I,
not P. Proposed: **`idleAirFlowIntegralLimitMax` 12 → 20**, ceiling 42.4, ~9 airflow% headroom. With
`idleAirPIDOutMax` = 35 that still leaves 15 of P-only space above the integral, preserving the
anti-windup separation.

**Scope limit on the redundancy argument:** a 105 °C failsafe also suppresses warm-up *fuel*
enrichment. A cold engine on a failed CLT is likely a no-start or a no-catch before airflow authority
is ever exercised. This buys a limp-home once running (at ~29° idle advance, rough by design) — it does
not make a failed CLT a non-event.

Failure asymmetry still favors the generous side: over-clamped saturates and stalls silently
(`randomlydied.csv`), over-authorized flares to ~1500–2000 rpm — recoverable and self-announcing.

Keep `idleAirFlowIntegralLimitMax` (12) well under the output clamp so only P and D reach the top of
the range; that separation is what keeps a catch from becoming a hang. (Independent-integral-cap rule,
[`notes/idle.md`](../../notes/idle.md).)

**Order of operations:** rescale KP/KI for the widened window *first* (see the ⚠ above — effective gain
is ~1.24× hot), *then* open the clamp. Widening authority under hot gain enlarges the limit cycle seen
in `armedstatebogjuly17.csv` (~330 ↔ 2000 rpm, ~1.2 s period) rather than damping it.

Typical-for-a-normal-TB reference (engineering judgment, not corpus-retrieved): window width 4–6 % TPS,
hot base sitting ~⅓ into the window, PID able to reach ~⅞ of it. The `[2.4, 8.0]` window and the
4.4 % base are both normal; only the clamp was mis-sized.

## 2026-07-19 — `idle0719.csv`: limits now correctly sized, but the loop runs a standing offset

Hot log, 944 s, 25 Hz. Config at end of log: `idleAirPIDOutMax` = 25, `idleAirPIDOutMin` = **−15**
(raised from −6 during this log). Observed PID range −11.0 … +8.56 — **neither clamp binding.**

**The old −6 was provably a clamp, not a resting value.** Consecutive-hold analysis:

| held value | consecutive samples | duration | start t |
|---|---|---|---|
| −6.000 | 1054 | **42.2 s** | 277.8 s |
| −9.000 | 586 | 23.4 s | 607.1 s |
| −8.000 | 156 | 6.2 s | 321.8 s |

Bit-exact holds at round numbers for tens of seconds = clamp signature. The −6/−8/−9 sequence is the
limit being walked open live mid-log; the PID ran to each new wall immediately. Method is reusable:
`(series != series.shift()).cumsum()` run-length on `Idle PID air % correction`.

### Gearing and PID decomposition — confirmed empirically

Regression over 7885 settled hot samples (state 2, TPS<6, target 1200, CLT 95–97):

```
DBW target = 0.05368 × (PID + custom corr) + 4.5572     r = 0.982
  measured gearing 0.0537 %TPS/airflow%   vs 0.0560 derived — model confirmed
  implied base feedforward = (4.5572 − 2.4)/0.056 = 38.5 airflow%
  PID −5.23 = P(2 %/° × −1.75°) −3.50  +  I −1.73     (I not at its −4 clamp)
```

`Idle ignition correction` vs airflow PID correlate at **0.803** — the two loops are coupled exactly
as `docs/emu-black-help/Idle.md:197` describes.

### ❌ RETRACTED: "standing negative offset costs positive authority" — this was wrong

An earlier revision of this note claimed the hot feedforward was ~5–6 airflow% too high, that a decel
event "must climb 6–9 airflow% to reach neutral before adding air," and recommended lowering the
`idleActiveAirflow` hot cells to recenter the PID. **All of that is wrong. Do not do it.**

**The airflow PID is zeroed whenever idle state ≠ 2**, so it never carries an offset into a
return-to-idle. Measured in `idle0719.csv`:

| idle state | samples | PID nonzero |
|---|---|---|
| 0 | 7935 | **0** |
| 1 | 4965 | **0** |
| 4 | 1223 | **0** |
| 2 | 9494 | 9287 |

Across all **19 entries into state 2**, PID at entry = **mean +0.145** (18 of 19 within ±0.7; the lone
outlier is the log's first sample, already mid-idle). It then develops its negative trim *after*
settling — median **0.36 s** to pass −3.

**So the standing −6 is a settled-state trim, not a starting handicap.** Every catch begins at PID 0
with the full feedforward already commanded. The error was importing a steady-state statistic
("a centered loop averages ~0") into a transient problem.

### The governing principle: the base table is the open-loop guarantee at the catch

`idleActiveAirflow` is the air the engine gets **immediately on idle activation, before the PID has
done anything**. Keep it high. The risk is asymmetric and the asymmetry is not close:

- **Too much base air** → the ignition PID absorbs it by retarding (here a standing −1.75°, min −4.0
  against its −5 integral clamp; RPM sits 1227 vs 1200 target). Modest, self-correcting, harmless.
- **Too little base air** → nothing to absorb. The engine dies on a decel, potentially in traffic.

A negative steady-state PID average is therefore **expected and desirable**, not a calibration defect.
Do not trim the base table to make that average look centered — that removes air from precisely the
instant the engine is most likely to die, to improve a cosmetic statistic. The standing ignition retard
is the *designed absorption mechanism* for surplus air (`Idle.md:197` — the two loops cooperate), not a
fault to be tuned out.

**What the negative limit is actually for:** `idleAirPIDOutMin` must be deep enough for the loop to
remove the surplus at settled idle, or RPM parks above target. The old −6 was binding (42.2 s bit-exact
pin); −15 is correctly sized. That part of the analysis stands.

### ⚠ The airflow tables above are STALE

This note tabulates `idleActiveAirflow` 1200 rpm / 96 °C = **49.5**; `idle0719.csv` implies a live base
of **38.5**. Changes are made in EMU and no export has captured them. **Read the live table before
trimming — do not act on the cell values in this note.** Also: hot idle target is **1200 rpm** (log
floor), not 1000; the CLT-failsafe deficit derivation above used the 1000 row and needs re-deriving
against live values.

### Open

- Idle still wanders: sd 88 rpm, range 874–1589 against a 1200 target.
- Logged channel set still lacks **MAP, PPS, Lambda, clutch** — same gap as `randomlydied.csv`.
  Without MAP, load steps cannot be separated from control error. Add before the next idle log.
- Ignition-PID reach to `idleIgnitionMaxTorqueAngleTbl` still unverified (see ⚠ above); this log shows
  idle ign correction spanning only −4.0 … +3.5, nowhere near the ~+11° the structural ceiling assumes.

## External references for idle authority sizing (2026-07-20)

**Provenance warning:** these are ECU *vendor documentation*, not engineering literature. Real-world
calibration guidance, empirically validated by vendors, but not derived from anything. The repo corpus
(8 books incl. Heywood, Banish, Bosch, Kiencke & Nielsen) contains **no** actuator-authority sizing
figure — verified by targeted grep 2026-07-20. US Patent 4,572,127 describes this exact architecture
(spark fast / throttle slow, integrator in the throttle path) and **contains no numeric authority
values at all.** Treat everything below as convention, not theory.

### MaxxECU — documents the same parameter (closest comparable)

Relative-to-open-loop PID clamp, official example:
> "Min PID Range: -10%, Max PID Range 20%. This allows the system to only be able to remove 10%, but add 20%"

Asymmetric ~2:1 toward adding air. **Supra runs −15/+25 = 1.67:1 — same shape, slightly wider.**
The safety asymmetry (surplus air is cheap, deficit kills) is the shipped vendor default, not a
local invention. See the retraction section above.

Actuator window examples, and where the Supra sits:

| source | window | width |
|---|---|---|
| MaxxECU ex. 1 | 2 → 10 % TPS | 8.0 |
| MaxxECU ex. 2 | 7 → 22 % TPS | 15.0 |
| **Supra** | 2.4 → 8.0 % TPS | **5.6** |

**The Supra window is narrower than both vendor examples.** This is the root of the whole clamp
sensitivity: at 5.6 % width each airflow-% buys only 0.054 % throttle (measured, r=0.982). Widening
`idleDBWTargetMax` would make every airflow-% worth more at the cost of resolution. **Not a
recommendation** — the 5.6 % window demonstrably holds idle; logged behavior outranks a vendor example.

Floor placement rule:
> "it is good to have the min value right below the normal opening position"

Supra: normal idle 4.2 % TPS, floor 2.4 % → satisfied, 1.8 % margin below.

Ignition authority example: "0% idle control = 4 deg ignition advance, 100% = 36 deg" (32° span).
Supra `idleIgnitionMin/MaxTorqueAngleTbl` spans 13→30° = 17° — about half MaxxECU's example.

### rusEFI — base position rule

> "adjust the throttle stop so that when the engine is idling fully warmed up at its lowest RPM
> (i.e. lowest airflow requirements) the Idle Air Control (IAC) is between 20% and 40% duty"

**Supra measured base = 38.5 airflow% — top of that band. Current calibration validated.** Note the
rule governs where the *base* sits, which is the load-bearing quantity (see the retraction above).
rusEFI on priority: "the open loop base table tuning is the most important thing to do, do not skip";
for ETB idle, "the PID values are pretty low, cause big changes is not what you need."

### Still unsourced

No source found — vendor or academic — for the **CLT-failsafe cold-rescue** case, i.e. how much
authority is needed to hold idle on a cold engine when the ECU believes it is hot. That requirement
remains derived from this car's own `idleActiveAirflow` cold-vs-hot column delta and nothing else.
The earlier "authority should be able to double idle airflow" heuristic was **unsourced invention and
is withdrawn** — it is not in the corpus and not in any vendor doc.

Sources: MaxxECU idle control settings (`maxxecu.com/webhelp/settings-idle_control-settings.html`),
rusEFI Idle Control wiki (`wiki.rusefi.com/Idle-Control/` — quotes via search index, page 403s to
direct fetch), US Patent 4,572,127 (`patents.google.com/patent/US4572127A/en`).

## Rescale rules (when the range changes again)

`f,c` = floor, ceiling. width = c − f.
- **Absolute airflow-% tables** (Active, Armed) — preserve actual TPS:
  `new% = (f_old − f_new)/(c_new − f_new)×100 + (c_old − f_old)/(c_new − f_new) × old%`
- **Additive correction** (delta, no offset): `new = old × (c_old − f_old)/(c_new − f_new)`
- **Airflow PID gains & limits** (delta output): same width-ratio scale as the correction.
- **Cranking**: not preserved — set the cold cell to the target TPS directly,
  `new% = (TPS_target − f_new)/(c_new − f_new)×100`, keep the taper shape.

See the `emu-black-tune` skill for full methodology and the `emu-black-emubt-export` skill for writing tables back out.

## 2026-09-08 — `goodlog.csv`: the idle floor is a DC clamp, and it sits *below* the sustaining position

229 s, 25 Hz, hot (CLT 96–115, oil 1.4–2.4 bar), mixed drive + six returns to idle.
`idle_log_running_fine.csv` (18:49) is the **same drive re-exported with a different channel set** —
identical TIME/RPM/CLT/airflow series — so the two merge sample-for-sample and give MAP, Ignition
Angle, A/C clutch and Gear alongside the DBW channels. Comparison log: `more_pid.csv` +
`more_pid_all_channels.csv` (2026-08-30), whose matching XML export is `more_pid.xml.emub3`.
The 09-08 configuration below was **first derived from the log itself** and has since been
**confirmed against the XML export `updatedarmedstate.xml.emub3`** (exported 09-09) — see the config
read at the end of this section. Where the two are compared, both agree.

### Live configuration recovered from the log

| quantity | method | 09-08 | 08-30 (XML) |
|---|---|---|---|
| actuator window | regress `DBW target` on `Idle air %`, idle-owned samples, cmd < 12 | slope 0.0568, floor **2.40**, ceiling **8.01** (n=3117) | `idleDBWTargetMin/Max` = 2.4 / 8.0 |
| ramp down offset | peak `Idle target` − hot base (base = `idleRPM` hot bin, 1025) | **200 rpm** | `idleRAMPDownOffset` = 350 |
| ramp decay rate | Δ`Idle target`/Δt while falling — dead flat, no exponential | **100 rpm/s** | `idleRAMPDownDecayRate` = 125 (⇒ 1 rpm/s per count) |
| ramp duration | offset ÷ rate | **2.0 s** | 2.8 s |
| airflow `kI` | slope of PID output over constant-`Idle ignition correction` holds ÷ e | **≈0.95 %/(°·s)** | 0.31 measured / `idleAirFlowKI` 410 |
| airflow `kP` | output jump at each error step, kI term removed | **≈0.59 %/°** | 0.13 measured / `idleAirFlowKP` 307 |

Both gain estimates are attenuated by 1° quantization of the error channel, so read the **ratio**, not
the absolute: the 09-08 tune runs the airflow PID roughly **3–4× hotter** than 08-30. The ramp-offset
change was not made alone.

### The position floor is set by `dbwMinDC`, and it does not guarantee anything

`DBW Out. DC` pins at **−35 %** on every deep close. **That is the configured minimum DBW output
(`dbwMinDC`), a tune value — not a mechanical end-stop.** With it in force the plate stops descending
at **4.80 % TPS**: DC held at −35 for **13.6 s continuously** with the command below 4.3 and TPS never
went under 4.80; across every settled saturated-close sample in the log (61.8 s) p10 = 4.80. Raise the
clamp and the plate goes lower — this is a calibration floor wearing a hardware costume.

Holding duty vs commanded position (samples where TPS tracks target within 0.15):

| TPS held | 8.5–9.0 | 6.0 | 5.5 | 5.0 | 4.5 |
|---|---|---|---|---|---|
| median `DBW Out. DC` | −3 | −7 | −32 | −33 | −35 (saturated) |

Zero holding duty at **8.5–9 % TPS** is the spring rest / limp-home position. Below ~6 % the force
demand knees up steeply — the plate is being driven past the limp-home detent onto the strong spring —
so **relaxing `dbwMinDC` buys progressively less closure per unit of duty**. How much less is not
derivable from this log; it needs a deliberate sweep (see below).

**The floor lands below the position that sustains idle.** Binning d(RPM)/dt against TPS over
idle-ACTIVE samples at the 1025 target:

| TPS | 4.5 | 4.7 | 4.8 | 5.0 | 5.1 | 5.2 |
|---|---|---|---|---|---|---|
| median d(RPM)/dt | −4 | −19 | **−10** | −6 | **+10** | +2 |

Zero crossing at **5.0–5.1 % TPS** — hot, heat-soaked, no A/C. The clamp-limited floor (4.80) is
*under* that: parked on the floor the engine bleeds ~10 rpm/s. The log's last seven seconds show
exactly this — 1012–1055 rpm against a 1025 target, plate at 4.8–5.0, DC pinned, `Idle PID air %
correction` at −19 and still integrating down.

**So the −35 % clamp is not an anti-stall safeguard, and did not act as one.** Confirmed by Will:
**two stalls after a start run with an under-supplied `idleArmedAirFlow`.** A position floor beneath
the sustaining position bounds nothing — it only bounds how fast you starve. The open-loop survival
guarantee is the **armed / active airflow tables**, not the actuator window minimum
([`notes/idle.md`](../../notes/idle.md), and the memory rule *idle base airflow is the open-loop
guarantee*). That is the mechanism that bit him, and no floor value would have covered it.

**Two different floors, two different scopes:**

- `idleDBWTargetMin` bounds only what the **idle strategy** can ask for. Raising it constrains the
  idle PID and nothing else.
- `dbwMinDC` bounds what the **servo will drive to from any source** — idle, characteristic, cranking.
  In principle it is also closing-rate authority — but **measurably it is not, on this car.** Of the
  70.7 s this log spends on the −35 rail (31 % of the log), **70.4 s is at TPS ≤ 10 and 96 % of that is
  idle-owned; only 0.32 s occurs above TPS 10.** The seven big closures (TPS > 20 → < 10, including two
  at 110–115 %/s) touch the rail for a **median 0.04 s** out of ~2.2 s. So `dbwMinDC` is in practice an
  idle-region parameter here, and moving it costs essentially nothing in driveability. *(An earlier
  revision of this section claimed tightening it "slows every throttle closure in the car" — withdrawn,
  the log does not support it.)*

### `dbwMinDC` → position floor, as far as this log can resolve it

| `dbwMinDC` | resulting floor (TPS) | basis |
|---|---|---|
| 0 | **8.5–9.0** | zero holding duty = spring rest / limp-home |
| −3 | **5.8** | settled holding duty, n=24 |
| −6 | **5.6** | settled holding duty, n=47 (p10 −13) |
| −33 | **5.2** | settled holding duty, n=257 |
| −35 (current) | **4.80** | saturated equilibrium, 13.6 s continuous |

**The map is violently nonlinear right where the floor wants to live:** 27 points of duty (−6 → −33)
buy 0.4 % TPS, then 2 points (−33 → −35) buy another 0.4. Note also the hysteresis — the plate will
*hold* 5.6 on −3 to −6 % once it has arrived, but the final approach of a closing move to 4.7 shows a
median −34 %. Reaching a position costs more duty than holding it, so size against the approach figure.

**Which is why duty is the wrong unit for a safeguard.** Motor force ∝ duty × battery voltage: 12.0 →
14.4 V is ~20 % more force at the same commanded duty, and on a map this steep that moves the floor by
more than the entire −33…−35 band. Cranking (~10 V) is the worst case, and the cranking airflow table
shares this same actuator. A duty clamp is a floor that drifts with the alternator; `idleDBWTargetMin`
is a floor that does not. **Use `dbwMinDC` for authority and `idleDBWTargetMin` for the guarantee.**

### The TPS frame moved ~+1.1 % between 08-30 and 09-08

Same engine, same hot idle, same target, no A/C in either:

| | 08-30 | 09-08 |
|---|---|---|
| settled idle RPM / MAP | 1014 / 37 kPa | 1020 / 37 kPa |
| TPS holding it | **4.0** | **5.2** |
| plate floor at `dbwMinDC` | **3.9–4.0** | **4.8** |
| `Idle PID air % correction`, settled | **−22.6 median, pinned on the −25 clamp** | −1.3 median, clamps not touched |
| implied base feedforward (air% − PID) | **≈48.6** | **≈49.1** |

Same RPM at the same MAP is the same mass flow, so the airflow did not change — the **position that
delivers it** did, by about +1.1 % TPS, and the clamp-limited floor moved with it by the same amount.
The base airflow feedforward is unchanged. Independent check from a flow fit: on 08-30, `MAP × RPM`
against TPS over steady idle-region samples (RPM 1007→1524) is linear with **R² = 0.954** and
extrapolates to zero flow at TPS = **−0.34**; feeding 09-08's idle flow into that line predicts an
08-30-frame TPS of 4.11 against the 5.2 actually read.

**What fixed idle on 09-08 was not the ramp offset.** The frame shift is what put the (unchanged) base
airflow table on the money: the same table that pinned the PID against its −25 clamp all through 08-30
now settles within a couple of airflow % of neutral. The short ramp and the 3× PID are survivable
*because* the feedforward is finally correct.

**Resolved 2026-09-19:** it was **carbon fouling of the throttle body**. Cleaning it dropped the hot sustaining
position 5.9 → 2.5 % TPS in one step, and the plate-stuck-above-command behaviour with the duty pinned went from
20 % of idle time to nil — [`tb_clean_2026-09-19.md`](tb_clean_2026-09-19.md). The +1.1 here was one step on that
fouling curve, so every TPS number in this note describes a fouled TB at some stage — and in the **old TPS frame**: the
09-19 DBW relearn moved the zero by 0.040 V, so `TPS_new ≈ TPS_old − 1.09` for everything logged after it.

### Ramp-down offset A/B — the approach works, quantified

Return-to-idle events, entry into idle ACTIVE, window held to samples where idle owns the DBW target
(source 2) throughout, measured **after** the target ramp reaches base so the ramp itself is not scored:

| | 08-30 (offset 350 / decay 125) | 09-08 (offset 200 / decay 100) |
|---|---|---|
| events scored | 10 | 3 |
| ramp duration | 2.76 s | 1.92 s |
| RPM overshoot above base target, median | **+202** | **+50** |
| peak-to-peak RPM | 254 | 88 |
| time to settle inside ±40 rpm | **7.8 s** (up to 11.1) | **0.12 s** (worst 1.0) |
| PID excursion above its settled value | +16.4 airflow% | +9.7 |
| worst RPM undershoot | −73 | −47 |

The mechanism is the one already written up in [`notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md):
RPM decays toward idle negative-exponentially while the ramp falls at a fixed rate, so the two agree at
exactly one point and the PID integrates the difference everywhere else. Halving the offset and slowing
the decay rate cuts the ramp 2.8 s → 2.0 s, and the accrued error with it.

**How far this can be taken.** The offset must stay above the largest RPM error the engine genuinely
presents at idle entry, or the PID is switched on inside the natural error band and starts saturated.
Worst post-entry error in this log was **+189 rpm** against the 200 offset — the offset now sits
essentially *at* the observed error band, which is the right target, with nothing spare. **~150 is the
floor**; below that it starts truncating real error. *(Retired by the clutch filter below: the
+189 figure comes from the t=214.6 throttle-blip re-entry, which happens **clutch-in**, so it is not
a ramp-down event at all. On genuine clutch-out return-to-idle events the worst post-entry excursion
is +138 — about 62 rpm of margin under the cap, not zero.)*


#### Per-event scoring of the 200 offset (all six ACTIVE entries in `goodlog.csv`)

Every entry into `Idle state` = 2, scored from the log alone. Base target 1025 (hot `idleRPM` bin),
ARMED cap 1225 in every event — the cap is the handover threshold, so **the offset alone sets where
the loop closes**. Ramp rate measured 100 rpm/s flat on all six.

| t (s) | entry RPM | d(RPM)/dt at handover | worst RPM *below* the ramping target | peak PID air % / ign corr. | RPM peak after ramp ends | settle to ±25 | min RPM |
|---|---|---|---|---|---|---|---|
| 57.28 | 1253 | −528 | −96 | +7.9 / +5.0° | 1067 (+42) | 0.56 s | 1012 |
| 82.16 | 1239 | −412 | −116 | +12.4 / +6.0° | 1051 (+26) | 1.36 s | 962 |
| 157.72 | 1254 | −123 | −26 | +1.3 / +1.5° | 1094 | left ACTIVE at 1.44 s | 1094 |
| 174.92 | 1230 | −480 | −108 | +8.9 / +5.5° | 1163 (+138) | 2.48 s | 996 |
| 201.32 | 1226 | −137 | **−1** | +0.2 / +1.5° | 1065 (+40) | 0.20 s | 979 |
| 214.56 | 1103 | +183 (blip re-entry, not a ramp-down) | +1 | −0.2 / +1.5° | 1214 | 1.08 s | 985 |

**The split is entirely by arrival rate, not by the offset.** The two events that arrive at the
threshold at −123/−137 rpm/s track the 100 rpm/s ramp to within 1–26 rpm and never wake the PID
(+0.2 and +1.3 airflow %). The three that arrive at −412…−528 rpm/s outrun the ramp by 96–116 rpm,
drive the PID to +8…+12 airflow % and +5…+6° of idle ignition, and pay for it with a +26…+138 rpm
rebound once the ramp lands. **Engine fall rate at the handover point spans 4:1 across events, so no
single `Ramp down decay rate` can be in sync with all of them** — the mechanism already written up in
[`notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md), here measured directly.

**Why moving 350 → 200 helped anyway: it moved the handover into a slower part of the decay.**
Fall rate as the same six decels cross each candidate threshold:

| threshold | offset it corresponds to | d(RPM)/dt at crossing, six events |
|---|---|---|
| 1375 | 350 | −207, −402, −450, −607, −715, −805 (median −528) |
| 1275 | 250 | −167, −207, −475, −507, −570, −862 |
| 1225 | **200 (current)** | **−123, −137, −412, −480, −528, −790 (median −446)** |

The slowest arrival improves 207 → 123 rpm/s, which is what converts two of the six events from
"PID fights the ramp" to "PID never engages." The offset also sets the exposure window directly —
duration = offset ÷ decay rate, 3.5 s at 350/100 vs **2.0 s** at 200/100 — so it cuts both the rate
mismatch and the time spent accruing it.

**No re-arming, and margin above the worst excursion.** Zero ACTIVE→ARMED reversions in the log;
the largest RPM the controller reached while ACTIVE was 1254 (at handover) and the largest post-ramp
excursion was 1214 on the throttle-blip re-entry — **11 rpm under the 1225 cap.** On genuine ramp-down
events the worst is 1163, i.e. ~62 rpm of margin. No stall, no dip below ~962 (−63 under base).

**Where the residual error now lives: the decay rate, not the offset.** On the fast events the ramp is
a phantom target sitting ~100 rpm above the real engine for roughly a second. Shortening that further
means raising `Ramp down decay rate` (200 rpm/s ⇒ 1.0 s exposure at the same 200 offset), which flips
the gentle events to the RPM-*above*-ramp side — the benign polarity (PID commands *less* air) but the
one that can pull the bottom of the entry down. Untested here; would need a deliberate sweep.


#### Clutch filter — `goodlogwithclutch.csv`, and the clutch idle-up is not applying

`goodlogwithclutch.csv` (09-09 export) is the **same drive re-exported with `Clutch pedal switch`
added** — all 5722 samples match `goodlog.csv` on TIME/RPM/`Idle target`/`Idle state` exactly, so
every number above transfers. Clutch pressed for **39.92 s of 228.88 (17.4 %), 18 presses.**

**The clutch does not move the idle target in this tune.** ARMED `Idle target` cap = **1225 whether
the pedal is pressed or released** (n = 1020 released / 197 pressed, no spread); settled ACTIVE target
= 1025 in both. If the *Clutch pressed increase* = 200 from the 2026-08-27 screenshot were live, the
cap would read 1425 and the settled target 1225 while pressed. It does not. **Confirmed in the XML:
`idleClutchTrgtRPMIncrease` = 0** (`updatedarmedstate.xml.emub3`) — the increase is zeroed, not
unassigned; `idleClutchEnablesClosedLoop` is still 1, so the pedal still forces closed loop. The
clutch cannot shift the handover threshold, so it never confounded the offset study through the
target.

**Where the clutch actually lands in the six events:** never during the ramp itself on any of the five
genuine ramp-downs — only in the approach and in the settle tail.

| event | clutch in decel / ramp / settle | verdict |
|---|---|---|
| 57.28 | 0.00 / 0.00 / 0.00 | **clean** |
| 82.16 | 3.84 / 0.00 / 1.48 | excluded (strict) |
| 157.72 | 0.00 / 0.00 / 0.00 | **clean** |
| 174.92 | 0.48 / 0.00 / 0.72 | excluded (strict) |
| 201.32 | 0.52 / 0.00 / 0.00 | excluded (strict) |
| 214.56 | 0.00 / **0.80** / 1.12 | **dropped outright — clutch in through the ramp** |

**This retires the "+189 rpm, 11 rpm of margin" figure.** That excursion was the t = 214.56
throttle-blip re-entry, which happens **clutch-in**. On genuine clutch-out ramp-downs the worst
post-entry excursion is **1163 (+138)**, i.e. ~62 rpm under the 1225 cap. The offset has more headroom
than the unfiltered read suggested.

**The conclusion survives the strict filter, on n = 2.** Only 57.28 and 157.72 are clutch-free end to
end, and they are the two poles of the same pattern: arrival at −528 rpm/s → 96 rpm below the ramp,
PID +7.9 %; arrival at −123 rpm/s → 26 below, PID +1.3 %. Arrival rate, not the offset, sets the cost.

**Clutch-in coastdown is ~3× faster and is the untested stress case.** ARMED decel rate over
RPM 1225–2500:

| clutch | n | p10 | median | p90 |
|---|---|---|---|---|
| released | 660 | −405 | **−161** | −55 |
| pressed | 53 | −1392 | **−472** | −87 |

Disconnecting the driveline drops the decelerating inertia to the engine alone. **Every genuine
handover in this log happened clutch-out**, so the 200 offset has never been scored against a
clutch-in coastdown arriving at the cap — the case where a 100 rpm/s ramp is furthest out of sync.
That is the gap to fill before trusting the current numbers as worst-case. It also means the fast
arrivals (−412…−528) were all *in gear* — the fast/slow split is not a clutch artifact.

**Withdrawn before it propagated:** settled `Idle PID air % correction` at first appears
clutch-dependent (median −1.75 released vs −9.75 pressed), which would read as a clutch load step at
idle. It is **time drift, not the clutch** — the settled PID walks +2.5 (t≈1–8 s) to −17.7 (t≈224–229)
across the log as it heat-soaks, and each clutch-pressed window matches the clutch-released window
immediately beside it to within ~2 points (74.40 −9.94 vs 68.76 −8.88; 210.48 −12.06 vs 207.36
−10.28). No clutch load step at idle is detectable in this log.


### 2026-09-08 config read from XML — `updatedarmedstate.xml.emub3` (exported 09-09)

The 09-08 calibration is no longer binary-only. **Everything derived from the log above is confirmed
by the tune**, and three things the log could not show are now readable.

| quantity | symbol | log-derived | XML | |
|---|---|---|---|---|
| actuator window | `idleDBWTargetMin` / `Max` | floor 2.40, ceiling 8.01 (regression) | 24 / 80 → **2.4 / 8.0** | ✔ |
| ramp down offset | `idleRAMPDownOffset` | 200 rpm | **200** | ✔ |
| ramp decay rate | `idleRAMPDownDecayRate` | 100 rpm/s | **100** (1 rpm/s per count) | ✔ |
| ramp delay | `idleTargetRampDelay` | — | **0 ms** | |
| duty floor | `dbwMinDC` | −35 % | **−35** | ✔ |
| hot idle target | `idleRPM` @ `cltBins` | 1025 | **1025 flat from 90 °C up** | ✔ |
| hot base feedforward | `idleActiveAirflow` | 48.81–49.25 airflow % | **49.25** interpolated at CLT 96 / target 1025 | ✔ |
| clutch idle-up | `idleClutchTrgtRPMIncrease` | inferred 0 from the log | **0** | ✔ |
| airflow PID | `idleAirFlowKP` / `KI` / `KD` | "3–4× hotter than 08-30" | **1024 / 1024 / 0** = KP 1.00, KI 1.00 vs 08-30's 307/410 → **3.3× / 2.5×** | ✔ |

The airflow-% decode chain is now anchored end to end: `idleActiveAirflow` raw 0x62 = 98 → 49.0 % at
CLT 96 / 1000 rpm, interpolating to **49.25 %** at the 1025 target, which maps to
`2.4 + 49.25/100 × 5.6` = **5.158 % TPS** — and the log's `Idle air %` minus `Idle PID air %
correction` reads 48.8–49.25 across every settled window. Same for the commanded position: the last
block's 32.5 airflow % predicts 4.22 % TPS against a logged `DBW target` of 4.20.

#### The base airflow table is flat above 96 °C — that is why the drift had nowhere to go but the PID

`cltBins8` = 0/15/30/45/60/75/**96/105**, and in `idleActiveAirflow` **columns 96 and 105 are
identical in every row** (1000-rpm row: 49.0 / 49.0). The log ran CLT 95–115 °C the whole time. So
across the entire drive the open-loop feedforward was a constant 49.25 airflow % **by construction** —
it is not that the table was well-centred and drifted, it is that above 96 °C the table has no slope
left to give. Everything the engine's changing air demand did over those four minutes landed on the
integrator. Combined with the oil-pressure custom correction being off (`Idle airflow custom corr.`
logs 0 throughout), **nothing in the open loop can see heat soak once coolant is on the stat.**

#### The PID clamps were not the wall — `dbwMinDC` was

`idleAirPIDOutMin/Max` = −25 / +25 and `idleAirFlowIntegralLimitMin/Max` = −25 / +15. The PID
finished the log around −17 and still integrating, so it had **7–8 points of clamp left**. What
actually stopped it is the actuator: it was commanding `DBW target` 4.20 % TPS with `DBW Out. DC`
pinned on the −35 rail and the plate parked at ~5.0. **The closing authority ran out in hardware
terms, not in strategy terms** — which is the same conclusion the `dbwMinDC` section reaches from the
other direction, now confirmed from both ends.

#### Every scheduled idle adder is now zero

`idleACRPMIncrease` 0, `idleClutchTrgtRPMIncrease` 0, `idleAboveVSSTargetIncrease` 0 (**re-enabled at 200 / 5 km/h in the 2026-09-19 19:05 export** — rolling entries now arrive at 1425),
`idleDSGTorqueCorr` all-zero, and **`idleCoolantFanCorr` 0** — the last one is a change from the
value this repo previously recorded, so the fan-kick airflow compensation is no longer armed
(see [`supra/notes/`](.) fan strategy). The only scheduled variable left acting on the idle target is
the ramp-down offset. That is consistent with the stated intent to minimise scheduled idle variables,
but it means the fan engaging at CLT 70 now lands as an uncompensated load step.

Ignition side for completeness: `idleIgnitionKP` 51 / `KI` 5 (÷1024 → 0.050 / 0.005),
integral limit ±5°, `idleIgnitionTargetTbl` on `idleIgnitionTargetCLTBins` 0/43/96/130 °C.

### `idleMinMapToActivate` — re-evaluated, not binding, and no room to raise it

The gate blocks ACTIVE while MAP is *below* it, to keep idle out of engine braking
([`docs/emu-black-help/Idle.md` → Activation](../../docs/emu-black-help/Idle.md): *"Idle On if MAP
over"*). Two direct tests on this log:

1. **Did it ever delay a handover?** Count ARMED samples where the RPM condition for ACTIVE was
   already satisfied (RPM ≤ the logged ramped target) — i.e. idle waiting on something else.
   **Zero samples, 0.00 s.** Every ARMED→ACTIVE handover fired on the RPM crossing, immediately.
2. **What is the margin?** MAP at the five handovers: **29, 30, 30, 30, 33 kPa**.

| band | MAP |
|---|---|
| idle ACTIVE | min 29, p1 32, p10 35, med 37 |
| coast at the handover neighbourhood (1150–1350 rpm, closed pedal) | min 27, p10 29, med 30 |
| deep engine braking (> 2500 rpm, closed pedal) | 14–19 |

Valid window is therefore roughly **19 → 26 kPa**: above the deep-braking band you want excluded,
below the 27 kPa floor of the coast band where handovers actually happen. `idleMinMapToActivate` = 18
(08-30 XML, unverified on 09-08) sits just under that window — unbinding by design, 4 kPa clear of the
deepest braking MAP seen. **Leave it.** Raising it toward 27+ re-creates the 2026-07 lockout stall;
there is no benefit on the other side to pay for that.

### Conditions this log does *not* cover

- **A/C at idle: cannot happen.** The clutch output is gated at 1800 rpm, and the log confirms it —
  `AC Clutch` = 1 has **minimum RPM 1804, zero samples below 1800**, and drops out at 1773–1821 on the
  way down. There is no A/C load step onto an idling engine, so `idleACRPMIncrease` never fires on this
  car. (An earlier revision of this note flagged an A/C-at-idle sag risk — **withdrawn, it is not
  reachable.**)
- **Cold.** Every sample is CLT ≥ 95. A cold return-to-idle rides the armed-state table longer and
  arrives on a much higher base; a short ramp puts more of the burden on that table being right — which
  is precisely the table that produced the two stalls.
- **Cold, dense intake air.** IAT on 08-30 was 51–63 °C at idle. Idle runs MAP/baro ≈ 0.37, well under
  0.528, so the throttle is choked and flow ∝ A·P/√T: the winter case needs roughly **12 % less area**
  than the hot-soak case measured here, i.e. a sustaining position near **4.5–4.65 %** — *below* the
  4.80 the current `dbwMinDC` allows. Expect idle to sit high on genuinely cold-air days with the plate
  pinned and ignition retard as the only remaining authority.
- **`Idle airflow custom corr.` reads exactly 0** for all 5722 samples here and all 12418 on 08-30.
  **This is deliberate — Will disabled the oil-pressure custom correction.** Not a fault; just don't
  credit it in any airflow sum. See [`oil_viscosity_idle_airflow.md`](oil_viscosity_idle_airflow.md).

### Raising `idleDBWTargetMin` — what it does and does not buy

Under the current `dbwMinDC`, 2.4 → 4.8 % TPS is unreachable, so raising the floor into that band costs
no behaviour and buys resolution: window 5.6 → 3.6 % TPS makes each airflow-% worth 0.036 instead of
0.056 % TPS, **1.56× finer** over the range that actually exists. For `f_new` = 4.4, ceiling unchanged:

```
absolute tables (Active, Armed):   new% = 1.5556 × old% − 55.56      (clip at 0)
   49  (hot idle base)  → 20.7      87.5 (cold 1500 rpm) → 80.6
   30  (log's lowest command) → clips to 0        cranking cells (11.5–13) → clip to 0
additive corrections, PID gains, PID clamps, integral limits:   × 1.5556
   e.g. idleAirPIDOutMin/Max −25/+25 → −39/+39 to hold the same throttle authority
```

**But it is not the stall fix, and no value of it is** (Will, 2026-09-09). The sustaining position is
not a constant — it moves with friction, and it moves *further than the whole band under discussion*.
From this repo's own oil dataset ([`oil_viscosity_idle_airflow.md`](oil_viscosity_idle_airflow.md)
table at line 132), both rows at **the same 96 °C coolant**:

| condition | airflow % to hold idle |
|---|---|
| hot coolant, **cold oil** | **51–58** |
| hot coolant, **hot oil** | **28–31** |

That is a **~25 airflow-% swing on oil temperature alone**. The entire dead band this section is about
— base feedforward ≈ 49 down to the `dbwMinDC` floor at 42.9 — is **~6 airflow %**. The thing that
varies is four times wider than the thing being clamped. Will's framing of it: *a cold-oil engine can
stall at −20 % DBW DC, while a hot-oil engine needs less air than −35 % delivers.* The duty→position
table above puts −20 % at ~5.6–5.8 % TPS ≈ 57–61 airflow %, sitting right on top of the measured
51–58 cold-oil demand — his number and the oil dataset agree independently.

**So no constant floor — in duty or in position — is a stall guarantee.** Set it for cold oil and the
hot engine idles high with no authority; set it for hot oil and it is under the cold-oil requirement
and guarantees nothing. **The only floor in the idle system that tracks the condition is
`idleAirPIDOutMin`**, because it is measured in airflow % *relative to the Active-state table*, and
that table moves with the operating point. Absolute floors (`DBW Target min`, `dbwMinDC`) can only ever
say "don't command somewhere useless"; the survival limit has to ride the feedforward.

Two things follow for this build:

- **`idleAirPIDOutMin` and `idleAirFlowIntegralLimitMin` were both −25** on the 08-30 XML, so the
  integral alone can reach the whole negative clamp — no separation between the fast and slow paths,
  against the independent-integral-cap rule in [`notes/idle.md`](../../notes/idle.md). Measured
  hot-soak surplus (base 49 − sustaining ≈ 47.3) is under **2 airflow %**, yet the loop settled −10 to
  −18 chasing a command the actuator could not deliver.
- **A relative floor is only as good as the feedforward under it.** With the custom correction
  deliberately off, the Active table is indexed on coolant — and coolant does not see oil viscosity,
  which is the entire reason the oil-pressure correction exists. Until something in the feedforward
  tracks friction, there is **no condition-following stall guarantee available on this car at all**.
  That gap, not the floor value, is the thing standing between here and a guarantee.

Cells that clip to 0 were all asking for positions the plate cannot currently reach; the loss is inside
the dead zone. **The cranking clip is the one to watch** — `idleCrankingDC` asks for ~3.0–3.1 % TPS and
would be pinned at 4.4. Free while `dbwMinDC` = −35, real the moment that changes.

### The measurement that would settle the floor

**Done 2026-09-19, engine off, clean TB** — [`tb_clean_2026-09-19.md`](tb_clean_2026-09-19.md) §3: rest 6.3–6.6 % TPS
at zero duty, break-away open +25…+28, **break-away closed −28…−31** then straight to the 0.0 hard stop; no stable
position between 0 and ~6 % without the position loop. The idle band sits entirely in that bistable zone, which is why
the running holding duty is ~−25…−33 at every idle position and why a fouled plate parked itself against a −35/−40 clamp.

Everything above was bounded by one unknown: **where the plate actually stops as a function of allowed
closing duty.** Sweep `dbwMinDC` (or command the DBW down in EMU's throttle test) at hot idle and at
key-on-engine-off, logging `DBW target`, `TPS`, `DBW Out. DC` and battery voltage. That gives the
duty→position curve past the limp-home detent, separates the calibration floor from the real mechanical
stop, and tells you whether any of this window is recoverable at all.

**Not applied — Will enters tune changes.** See the rescale rules section above and the
[emu-black-actuator-rescale](../../skills/emu-black-actuator-rescale/SKILL.md) skill.
