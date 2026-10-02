# Clutch load at idle — human digest

*View of `../clutch_idle_load.md`. If they disagree, the canonical note wins.*

## What this covers

Whether the clutch disturbs idle enough to justify feeding air forward, measured from
`omg.csv` (2026-08-24).

## The rules

- **Don't feed the clutch forward.** The predictable part is too small; the big part
  (drag in gear) isn't predictable — it varies with gear, oil temperature, and wear.
- **Separate neutral from in-gear clutch events.** They're different loads, ~5× apart.
  Pooling them gives a meaningless average.
- `idleClutchEnablesClosedLoop` already forces closed-loop idle on pedal-down. That is
  the correct mechanism and it's free.
- A clutch **target** bump is inert while the active-airflow target axis floors above
  the commanded hot target — the lookup clamps to the same row.
- Judge any idle feed-forward by **airflow points of PID response**, not rpm alone.
- Check settled time in each state before building a table. The pedal is almost never
  held down at idle, so there's nothing to calibrate against.

## Key numbers

- Settled idle: **530 s** clutch up vs **1.4 s** clutch down. No steady-state comparison
  is possible.
- Neutral, hot: press unloads **15–45 rpm**, release loads **25–35 rpm**. PID answers
  with **under 1 point** of ±25 authority.
- In gear, dragging (one confounded observation): **+5.4 airflow points, +4.2° ignition**,
  still 50 rpm under target.
- For scale: A/C is **12–14 airflow points** and **~350 rpm**. Clutch is ~1/15th of that.

## Gotchas when re-running this

- `PPS` has a non-zero closed-pedal floor (~1.8 p99, spikes to 3). A `PPS == 0` gate
  drops nearly everything — use `PPS < 1`.
- `Vehicle Speed` glitches to 25–158 km/h for single samples at idle. A `VSS.max()`
  gate over a window rejects good events; use a median.

## When to care

Any time idle feed-forward comes up. A/C is the load worth feeding forward; the clutch
is not.
