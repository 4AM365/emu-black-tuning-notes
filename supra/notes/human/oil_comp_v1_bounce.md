# Oil comp v1 — why it bounced (digest)

Digest of [`../oil_comp_v1_bounce.md`](../oil_comp_v1_bounce.md). Canonical note wins.

## What this covers

The first on-car run of the oil-pressure idle airflow correction (`idle bounce.csv`,
2026-08-06). One engine run, cold start to 103 °C, with the correction live.

## The rules

- **Oil pressure is an RPM sensor, not a viscosity sensor, on any timescale under ~10 s.**
  Measured: OP tracks RPM at **zero lag** (r = 0.81 at lag 0). Viscosity moves on minutes;
  `P ∝ μ·N` and N wins every transient.
- So a correction table indexed on OP (and on RPM) is a **second feedback loop** around the
  idle controller — zero lag, huge gain, untuned, in front of a plant with 750 ms of airflow
  lag. That oscillates.
- Its sign flips across the surface. High RPM / high pressure → it yanks air out (limit
  cycle). Low pressure during a sag → it *also* yanks air out (near-stall). Both happened.
- **A correction fitted from held-idle data must not act during a transient.**
- It is additive on a base table that already schedules cold-oil drag through CLT. Don't
  tune the correction until the base is re-leveled.

## Key numbers

- Correction span **−22 … +44 %** airflow. PID authority is only **−15 … +20**.
- Bounce: RPM 1073 ↔ 2055 at **0.55 Hz**, air 32 ↔ 89 %; PID pinned on its −15 rail 43 % of
  the time; the driver is a 19-point cliff between the 5.5 and 6.0 bar columns.
- Near-stall: 1215 → 772 rpm while the correction went **+19 → −13** (pulled 32 points of air
  out of a dying engine). Repeats twice more; the engine finally quits with it at −22.
- RPM off target by >100 for **22 %** of idle-active time.

## Part 2 — the base-table rework (`idle bounce 2.csv`, same run)

- Correction is **indexed at 3 bar** (its 3.00 column is zero on every row). So the base table
  means "airflow required at 3 bar," and the rework follows from one identity:
  **new base cell = old cell + steady PID + 13·fan.** Observed oil pressure drops out.
- **A +13 term enters `Idle air %` between CLT 68 and 92 and the PID cancels it exactly** —
  engine air requirement is identical with it and without (26.1 vs 25.0 at CLT 86–94). It
  matches `idleCoolantFanCorr = 13`, which conflicts with the 06-13 note saying that adder is
  a DBW DC offset invisible in `Idle air %`. **The reworked cells require it set to 0** — it
  switches on and off *inside* one CLT interval of the base table, so no cell value can cover
  both states. Will's call; flagged, not decided.
- Reworked cells: 1500/30 62→68 (weak), 1500/45 53.5→55.5, **1375/60 44→34.5**,
  **1375/75 39→29.5**, 1200/60 36→30 (inferred), **1200/75 31→25.5**, **1200/96 24→27** (and
  105 the same). 1000/1100 rows and CLT 0/15 untouched — never visited. Replay error RMS 1.2 %.
- **The target ramp-down is a wrong-way step.** At 6 bar the correction reads +4/+16/+35 at
  1500/1375/1200 rpm. Walking the target 1500→1200 adds +31 of correction while the base only
  sheds ~11 — asking for a *lower* idle adds ~20 points of air. That is the CLT 66–90 rail.
- Carrying the higher target longer helps but is palliative. Re-referencing the zero column
  nearer **5 bar** would put the whole warm-up near zero correction; the base would then have
  to be re-levelled as the 5-bar requirement.

## When to care

Before re-enabling the correction: filter the pressure axis (5–10 s), clamp authority to
about **±6**, flatten or drop the RPM axis, and freeze it whenever RPM is >50 off target or
idle isn't ACTIVE. Re-level `idleActiveAirflow` first. And export a current tune XML — the
table's real axes and clamps have never been read, only inferred from the log.
