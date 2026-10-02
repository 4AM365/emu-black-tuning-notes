# Oil-pressure idle compensation v1 — why it bounced (log `idle bounce.csv`, 2026-08-06)

First on-car implementation of the oil-pressure idle airflow correction, logged as
`C:\Users\WTCra\Desktop\idle bounce.csv` (33,204 rows, 22.5 min wall, one engine run
t = 34–458 s, CLT 24 → 103 °C, OP 0.06 → 7.56 bar). Channel set is the reduced 10-column
oil-comp set: RPM, MAP, `Idle air %`, `Idle PID air % correction`,
**`Idle airflow custom corr.`**, `Idle state`, `Engine oil pressure`, CLT, `Idle target`.

Measurement layer this sits on: [oil_pressure_airflow.md](oil_pressure_airflow.md).
Model layer: [oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md).

## The correction surface, as actually executed

Median `Idle airflow custom corr.` over the 8,518 idle-ACTIVE samples, binned by actual
RPM (rows) × logged oil pressure (0.5 bar columns). This is the table *as the ECU read it*,
not as authored:

| RPM ＼ bar | 1.0 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1600** | — | — | — | — | — | — | 21 | 23 | 28 | 4 | 4 | 4 | 4 |
| **1500** | — | — | — | — | — | 15 | 19 | 23 | 23 | 8 | 4 | 5 | 4 |
| **1400** | — | — | — | — | 8 | 15 | 18 | 23 | 15 | 16 | 14 | 13 | 11 |
| **1300** | — | — | — | — | 8 | 13 | 21 | 23 | 23 | 24 | 20 | 20 | — |
| **1200** | — | — | — | 7 | 6 | 14 | 14 | 18 | 22 | 33 | 31 | — | — |
| **1100** | −6 | −6 | — | 0 | 8 | 8 | 13 | 24 | 34 | 37 | 39 | — | — |
| **1000** | — | −17 | −7 | 3 | 6 | 4 | 26 | 33 | 40 | — | — | — | — |
| **900** | — | −17 | −14 | 0 | −5 | −1 | 30 | — | — | — | — | — | — |
| **800** | −22 | −20 | −9 | −13 | −10 | — | — | — | — | — | — | — | — |

Observed span **−22 … +44** (5th/50th/95th pct = +4 / +13 / +31). For scale, the whole
airflow-PID authority band in this tune is **−15 … +20** (both rails observed: 790 samples
on −15, one on +20.4 — note this is *wider* than the −6/+15 in `supra 06132026.xml.emub3`
and the −10 the August logs railed at, so the PID limits were widened again; read the
current XML before quoting them). **The open-loop correction swings ~1.8× the closed-loop
controller's entire range.**

## Failure mode: oil pressure is an instantaneous RPM sensor

Cross-correlation of RPM against `Engine oil pressure` across the bounce (t = 163–200 s):
peak **r = 0.81 at lag 0.00 s**, first sign change at ±0.85 s. Oil pressure tracks RPM with
no measurable delay at 25 Hz. `P ∝ μ·N` — the `N` term dominates any transient; `μ` only
moves on a thermal timescale.

Consequence: **both axes of the correction table move with RPM in-cycle.** The table stops
being a viscosity schedule and becomes a second proportional feedback path around the idle
loop — one with no lag on its input, no integral, no gain tuning, and a sign that flips
depending on where you sit on the surface. Airflow → RPM has ~750 ms of lag
(`supra_idle_airflow_lag`). A high-gain, zero-lag feedback path in front of a 750 ms plant
is an oscillator.

Both signs appear in this one log:

**(a) RPM-axis dominant → limit cycle.** t = 165–200 s, CLT 66–75 °C, target ~1300.
RPM 1073 ↔ 2055, σ = 157 rpm, **period ≈ 1.8 s (0.55 Hz)**. `Idle air %` 32.5 ↔ 89.0.
corr(RPM, custom corr) = **−0.63**, corr(RPM, `Idle air %`) = **−0.76** — the commanded air
is in antiphase with RPM, so the correction is doing the driving, not responding. Mechanism:
an RPM overshoot moves the row index up into the 1500–1600 / ≥6 bar corner where corr
collapses 23 → 4 (a **19-point cliff between the 5.5 and 6.0 bar columns**), air is yanked
out, RPM falls back into the 1100–1200 / 5.5–6.5 bar corner where corr is 34–39, air is
slammed back in. The PID sat on its −15 rail **43 % of that window** — it had no authority
left to oppose any of it.

**(b) OP-axis dominant → near-stall.** t = 352–365 s, CLT 96 °C, target 1200. RPM decays
1215 → 772. OP follows 4.44 → 2.44. The correction follows the OP axis **down**:
**+19 → −13, i.e. it removed 32 points of airflow from a dying engine.** Total `Idle air %`
fell 42 → 28 while the PID could only find +11. Idle state flipped to 4 (recovery) at 765 rpm.
Same event repeats at t = 370 (515 rpm) and t = 458, where the engine finally quits with the
correction sitting at **−22**.

The positive-slope region below ~4.5 bar is the dangerous half: in a sag, dropping OP
subtracts air, which deepens the sag, which drops OP further. Nothing in the loop breaks
that except the recovery state.

## Over-airing, quantified

- Warm-up hold t = 36–165 s (target 1500 → 1300, CLT 37 → 66): correction +4 → +27 on top of
  a base table that the `oil_pressure_airflow.md` implied-cell work already found correct at
  the hot 1200 anchor. The PID walked steadily from +6 to its −15 floor absorbing it, hitting
  ≤ −9.5 for 9 % of the window. That is the "main active state not adjusted yet" the
  correction was authored against — it is *additive on top of* a base table that already
  carries the same cold-oil drag in its CLT axis. **Double-count.**
- Whole log: `|RPM − Idle target| > 100` for **22 % of idle-active time.**

## What the log says to change

1. **Filter the oil-pressure input, hard.** The viscosity signal lives on a 10s-of-seconds
   timescale; everything faster is an RPM echo. A 5–10 s time constant (or slew limit) on the
   correction's pressure axis removes both failure modes at once — the 1.8 s limit cycle and
   the 3 s sag are both inside the stopband. Verify against the current XML whether the axis
   channel can be a filtered/user-defined channel; if EMU can only index raw
   `Engine oil pressure`, this becomes a gating problem instead (item 4).
2. **Cap the authority.** ±44 points against a ±15/+20 PID is inverted. Until the surface is
   proven, clamp the correction to roughly **±6** — smaller than the PID's negative rail, so
   the closed loop can always overrule it.
3. **Drop or flatten the RPM axis.** It duplicates the base table's target/CLT axes and it is
   the source of the 19-point cliff that drove the limit cycle. Any RPM dependence wanted here
   should be monotone and shallow.
4. **Gate on steady idle.** Freeze the correction at its last value whenever
   `|RPM − Idle target| > 50`, `Idle state ≠ 2`, or entry age < 15 s — the same gate the
   measurement tables in `oil_pressure_airflow.md` are built on. A correction derived from
   held-idle data has no business acting during a transient, and item (b) above is exactly the
   cost of letting it.
5. **Re-level the base table first.** The correction cannot be evaluated while it is stacked
   on a base that already compensates cold oil through CLT. Zero the correction, re-log, level
   `idleActiveAirflow`, then re-enable at reduced authority.

---

# Part 2 — `idle bounce 2.csv` and the base-table rework (same session)

`idle bounce 2.csv` is the same engine run, re-exported idle-active-only with `Injectors PW`
and `VE` added (t = 20–323 s, 7,343 rows, RPM correlation 0.99 against log 1). Will supplied
screenshots of **both live tables**, so the calibration is now known, not inferred.

## The tables as they stand (screenshot, 2026-08-06 — "the tune as-is")

`idleActiveAirflow` — rows = Idle target, cols = CLT °C:

| tgt ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 75.0 | 62.0 | 53.5 | 47.5 | 43.0 | 34.5 | 34.5 |
| 1375 | 86.0 | 73.5 | 59.0 | 50.5 | 44.0 | 39.0 | 30.0 | 30.0 |
| 1200 | 81.0 | 68.5 | 52.5 | 42.5 | 36.0 | 31.0 | 24.0 | 24.0 |
| 1100 | 74.5 | 62.0 | 46.0 | 35.5 | 30.5 | 25.5 | 21.0 | 21.0 |
| 1000 | 65.0 | 54.0 | 40.0 | 28.5 | 24.5 | 20.0 | 18.5 | 18.5 |

(Hot columns are lower than the `supra 06132026.xml.emub3` decode in
[oil_pressure_airflow.md](oil_pressure_airflow.md) — 1500/96 40.0 → 34.5, 1200/96 26.5 → 24.0,
1000/96 16.5 → 18.5. The live table is newer than that export.)

`Airflow – Custom air flow correction [%]` — rows = **Engine RPM**, cols = **oil pressure, bar**:

| RPM ＼ bar | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 |
|---|---|---|---|---|---|
| 1500 | −3 | **0** | 0 | 3 | 4 |
| 1375 | −3 | **0** | 2 | 10 | 16 |
| 1200 | −6 | **0** | 9 | 26 | 35 |
| 1100 | −5 | **0** | 12 | 31 | 42 |
| 1000 | −6 | **0** | 16 | 39 | 51 |

**The 3.00 bar column is zero on every row — the correction is indexed at 3 bar** (Will,
2026-08-06). That fixes the meaning of the base table: `idleActiveAirflow` must be the
airflow requirement **at 3 bar oil pressure**, and the correction supplies the deviation.

## The identity that makes the rework trivial

`Idle air % = idleActiveAirflow(tgt,CLT) + corr(RPM,OP) + 13·fan + PID`, verified on this log
to **±0.3 %** (median residual −0.08 to +0.44 across every fan-off bin, exactly +12.7…+13.2 in
every fan-on bin). Since `corr(·, 3 bar) ≡ 0`:

> **R₃(tgt,CLT) = idleActiveAirflow(tgt,CLT) + PID_steady + 13·fan**

The 3-bar-indexed requirement is the current base cell **plus the steady PID output**. The
observed oil pressure drops out entirely — no OP surface, no P_typ assumption, no
back-solving the correction. The correction is presumed correct and the PID reports the
residual base error directly.

Steady PID is taken as `δ = PID − (RPM − Idle target)·0.046`, the 0.046 %-airflow/rpm being
the local slope of the base table itself (≈ 8 points per 175 rpm across the 1200–1375 rows).

## Finding 1 — `idleCoolantFanCorr = 13` is fully cancelled by the PID

Fan state is recoverable from the residual even though neither export carries `Coolant fan`.
It engages at **CLT ≈ 68** and drops out again by **CLT ≈ 92** (engage share 0.00 → 0.94 →
0.13 across those bins; the drop-out is unexplained — no VSS channel in this export).

That gives a near-controlled comparison in the CLT 86–94 band, same 1200 target:

| fan | n | CLT | OP | corr | PID | `Idle air %` | required total | requirement − corr |
|---|---|---|---|---|---|---|---|---|
| off | 353 | 92 | 4.62 | 13 | −1.2 | 37.0 | 39.1 | **26.1** |
| on | 408 | 90 | 5.31 | 20 | **−14.1** | 45.5 | 45.0 | **25.0** |

**The engine's air requirement is the same with the fan running as without it.** With the fan
on, the +13 is added and the PID takes 13.0 straight back out — and still overshoots target.
Every fan-on bin in the log shows the same thing.

Consequence for the rework: `δ` must have `13·fan` added back before it is written into the
base table, otherwise the CLT 60–90 cells absorb an adder that does not belong to them. With
that done the required base becomes monotone in CLT; without it, it reads 12 at CLT 80 and 27
at CLT 94 — a 13-point discontinuity sitting exactly on the fan transition.

**Two standing positions conflict with this, and both need Will's call rather than an edit.**

1. `supra_fan_engagement_strategy` records (validated 2026-05-29, Will, twice) that
   `idleCoolantFanCorr = 13` is a true load-comp and must not be cut to rebalance the base
   table. This log does not re-open that on theory — it just reports that the PID removed
   13.0 of it, at 1,900+ samples, with RPM still above target.
2. The same note records (06-13) that the +13 is applied as a **DBW DC offset and does not
   appear in `Idle air %`**. This log contradicts that directly: a term worth exactly
   +12.7…+13.2 enters the `Idle air %` sum between CLT 68 and 92 and is absent outside it.

The finding is stated **mechanism-agnostically**: whatever that +13 term is, it is observably
inside the logged airflow sum and the PID cancels it, so it is added back before the residual
is written into the base table.

**But the reworked table below requires that term to be zero — it is not optional.** The
reason is not the magnitude, it is the *shape*. The term switches on at CLT ≈ 68 and off again
at CLT ≈ 92, i.e. it lives entirely inside one CLT interval of the base table (the 75 node,
spanning 60–96). A base cell cannot encode "13 lower between 68 and 92 and correct outside
it." Keeping the adder at 13 forces the 60/75-column cells 13 below the fan-off requirement,
which is then wrong for every fan-off sample above 92 — exactly the 13-point discontinuity
observed. So: **`idleCoolantFanCorr` → 0 and use the cells as published**, or leave the adder
alone and accept that the CLT 60–96 span cannot be levelled. What is not viable is the present
arrangement, where the PID spends its entire negative authority cancelling the adder and has
nothing left for the oil correction stacked on top.

## Finding 2 — the required base along the warm-up path

Fan adder removed, `R₃ = base + δ + 13·fan`, binned every 4 °C (n = 321–1,148 per bin):

| CLT | tgt | OP | fan | base | corr | δ | **R₃** | R₃ − base |
|---|---|---|---|---|---|---|---|---|
| 38 | 1500 | 7.2 | off | 57.5 | 5 | +6.5 | **63.7** | +6.2 |
| 42 | 1495 | 7.1 | off | 55.0 | 4 | +4.1 | **58.9** | +3.9 |
| 46 | 1485 | 7.1 | off | 52.7 | 5 | +1.8 | **54.3** | +1.6 |
| 50 | 1475 | 6.9 | off | 50.6 | 7 | −0.6 | **50.1** | −0.5 |
| 54 | 1430 | 6.9 | off | 47.6 | 12 | −4.2 | **43.6** | −4.0 |
| 58 | 1394 | 6.8 | off | 45.2 | 14 | −6.8 | **38.1** | −7.1 |
| 62 | 1357 | 6.7 | off | 42.2 | 17 | −8.8 | **33.7** | −8.5 |
| 66 | 1330 | 6.6 | 0.4 | 39.9 | 20 | −9.9 | **31.1** | −8.8 |
| 74 | 1255 | 6.2 | 0.8 | 33.8 | 20 | −15.8 | **28.1** | −5.7 |
| 78 | 1209 | 5.8 | 0.9 | 30.4 | 20 | −18.0 | **25.1** | −5.3 |
| 82 | 1200 | 5.4 | 1.0 | 28.7 | 20 | −17.1 | **24.5** | −4.2 |
| 86 | 1200 | 5.2 | 0.9 | 27.3 | 19 | −15.5 | **24.5** | −2.8 |
| 90 | 1200 | 5.0 | 0.5 | 25.7 | 18 | −11.9 | **25.1** | −0.6 |
| 94 | 1200 | 4.6 | 0.1 | 24.0 | 13 | +2.6 | **26.9** | +2.9 |

R₃ falls monotonically 63.7 → 24.5 and flattens at ~25–27 from CLT 82 up. The PID sits on its
**−15 rail continuously from CLT 76 to 90** with RPM still 24–65 above target, so those bins
are lower bounds on the error, not equalities — the true requirement there is at or below the
listed R₃.

## The reworked `idleActiveAirflow`

Only the cells the warm-up schedule actually visits are changed. The 1000 and 1100 rows and
the CLT 0/15 columns were never entered and are left alone.

| tgt ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 75.0 | **68.0** | **55.5** | 47.5 | 43.0 | 34.5 | 34.5 |
| 1375 | 86.0 | 73.5 | 59.0 | 50.5 | **34.5** | **29.5** | 30.0 | 30.0 |
| 1200 | 81.0 | 68.5 | 52.5 | 42.5 | **30.0** | **25.5** | **27.0** | **27.0** |
| 1100 | 74.5 | 62.0 | 46.0 | 35.5 | 30.5 | 25.5 | 21.0 | 21.0 |
| 1000 | 65.0 | 54.0 | 40.0 | 28.5 | 24.5 | 20.0 | 18.5 | 18.5 |

Per-cell provenance:

| cell | old | new | Δ | held-idle coverage | confidence |
|---|---|---|---|---|---|
| 1500 / 30 | 62.0 | 68.0 | **+6.0** | 10 s at CLT 37–40, extrapolated to the 30 node | **weak** — coldest datum is 37 °C |
| 1500 / 45 | 53.5 | 55.5 | +2.0 | 44 s | good |
| 1375 / 60 | 44.0 | 34.5 | **−9.5** | 41 s | good |
| 1375 / 75 | 39.0 | 29.5 | **−9.5** | 21 s | fair |
| 1200 / 60 | 36.0 | 30.0 | −6.0 | 7 s | inferred to close the CLT-66 diagonal |
| 1200 / 75 | 31.0 | 25.5 | **−5.5** | 52 s | good (rail-censored → may want less still) |
| 1200 / 96 | 24.0 | 27.0 | **+3.0** | 102 s | good |
| 1200 / 105 | 24.0 | 27.0 | +3.0 | none | mirrors 96, as the table already does |

Replaying the whole warm-up through the reworked table reproduces the measured requirement to
**RMS 1.2 %, worst cell 2.4 %** — inside the PID's authority everywhere, versus the −15 rail
it lived on before. Two cells (1200/60, 1500/30) are inference, not measurement; both are
flagged above.

Note the shape change: the table used to fall smoothly with CLT; the reworked one has a
**step down at the 1375→1200 rows in the CLT 60–75 block**, which is the base table absorbing
the correction's large low-RPM/high-pressure values so the total stays flat.

## Finding 3 — the target ramp-down is a wrong-way step against the correction's RPM axis

At a fixed 6 bar, the correction reads +4 at 1500 rpm, +16 at 1375, **+35 at 1200**. Walking
the idle target down 1500 → 1200 during warm-up therefore *adds* **+31** of correction, while
the base table only removes ~11 across the same rows (47.5 → 36.0 at CLT 60). **Net effect of
asking for a lower idle speed at constant oil pressure: about 20 points more airflow.** That
is the whole mechanism behind the CLT 66–90 rail.

Measured against Will's observation (2026-08-06): the target reaches **1200 at CLT ≈ 80 with
OP still 5.4 bar**, and OP is still 5.0 at CLT 90 — it does not fall to the 4.6 bar where the
loop recovers until CLT ≈ 94.

Two independent levers, both real:

- **Carry the higher target further into the warm-up.** Delays entry into the steep corner and
  buys margin, but it is palliative — the corner is still there at any CLT.
- **Move the index pressure.** With the zero column at 3 bar, hot idle at 1200 rpm sits at
  4.4–4.75 bar in this warm-up and ~2.2–2.4 bar deep-soaked
  ([`../../notes/oil_pressure.md`](../../notes/oil_pressure.md)) — the operating band straddles
  the reference on both sides and the +9/+26/+35 columns do all the work. Re-referencing the
  zero column nearer **5 bar** would put the whole warm-up close to zero correction and leave
  only the deep-soak hot end negative, i.e. small excursions from a base table already trusted.
  The base table would then have to be re-levelled as the 5-bar requirement.

The reworked table above is built for the **3 bar** index as it stands today. Re-index and it
must be rebuilt — the arithmetic is the same, `R_ref = base + PID_steady + 13·fan` with the
reference column zeroed wherever it is put.

## Still open

- The 1000 and 1100 rows and the CLT 0/15 columns are unvisited in every log to date. A cold
  morning start and a deliberate low-target hold remain the only way to fill them.
- CLT 76–90 is rail-censored; re-log after this rework so the PID regulates freely and those
  cells become measurements rather than bounds.
- Why the fan drops out above CLT 92 is unexplained — log `Coolant fan` and a speed channel
  next time rather than inferring the state from a residual.
- The correction's own slope has not been validated against a deep soak. The one cross-check
  available (2 bar / 1200 / 96 in [oil_pressure_airflow.md](oil_pressure_airflow.md)) is itself
  PID-rail-censored, so it cannot confirm or refute the −6 at 2 bar.
