# Idle airflow by oil-pressure bin — measured tables

Digest of [`../oil_pressure_airflow.md`](../oil_pressure_airflow.md). Canonical note wins.

## What this covers

Five tables — one per oil-pressure bin (2/3/4/5/6 bar) — of the airflow % that was actually
holding idle, on the EMU RPM × CLT axes. Pure measurement, nothing modelled. Built from every
CSV in the two months to 2026-08-05 that logs oil pressure, including the Desktop exports.

## The rules

- **Five logs contribute, 14,409 binned samples, 9.8 min of held idle.** The 08-04
  **idle-target sweep** (targets 900 → 2000) is what fills the 1000 and 1500 rpm rows; without
  it those rows are unmeasurable, because normal driving never *holds* those speeds.
- Duplicates dropped: `key_data.csv` (identical subset of `20260613_1141`) and two shorter
  exports of the same 08-04 session.
- Gate: idle ACTIVE, MAP < 60, A/C off, 15 s past handoff, **|RPM − target| ≤ 50**.
  Cell = median total `Idle air %`.
- **† = upper bound** — the airflow PID was pinned on its −10 rail.
- The **6-bar column centres on 6.88 bar** and reaches 7.6; everything ≥ 5.5 lands there.

## Key numbers

| bin | cell | airflow % | n |
|---|---|---|---|
| 2 bar | 1200 / 96 | 28.5† | 2,593 |
| 2 bar | **1000 / 96** | **21.5** | 229 |
| 3 bar | 1200 / 96 · 1375 / 96 · 1500 / 96 | 38.8 · 43.0 · 47.5 | 792 · 375 · 67 |
| 4 bar | 1200 / 96 | 37.0† | 2,093 |
| 5 bar | 1200 / 96 | 37.0† | 1,788 |
| 6 bar | 1500 / 30 · 45 | 77.5 · 72.5 | 118 · 787 |
| 6 bar | 1200 / 45 · 60 · 75 | 41.5† · 34.5 · 30.5 | 505 · 1,054 · 1,433 |

30 of 200 cells hold data. The 0/15 °C columns stay empty — nothing colder than 27 °C exists.

## The composition closes exactly

`Idle air % = base(CLT,target) + 13·fan + custom + PID` — residual **+0.15 fan-off, +13.19
fan-on** over 11,496 samples. That lets the base cell be back-solved: at **2 bar / 1000 rpm /
96 °C the table should read 19.2** (IQR 19.0–19.5) against a shipped 16.5. The hot 1200 cell
back-solves to 26.5 against a shipped 26.5 — dead on. The whole **1500 row back-solves 7–8
below** the shipped cold cells.

## When to care

Don't read these as a correction surface: at hot coolant the requirement is two-valued by
thermal history above ~3.5 bar (bulk oil viscosity ≠ bearing-film viscosity), and the
high-pressure hot cells are rail-censored. The ±50-of-target envelope costs 10 of 40 cells
versus an "RPM is steady" criterion and biases the 5/6-bar medians up 2.5–4 points; both
variants are built (`ENVELOPE=steady`).
