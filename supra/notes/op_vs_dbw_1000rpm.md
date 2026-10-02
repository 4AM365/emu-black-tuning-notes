# Running dataset — oil pressure vs DBW output duty at ~1000 rpm (ign 17–19°)

**Ask (Will, 2026-09-19):** a running file of everything we know about oil pressure at 1000 rpm against
`DBW Out. DC`, with the scatter, restricted to ignition 17–19° (i.e. the idle ignition PID at rest so the
airflow side is doing the work), and a big table.

**Where it lives:** [`op_vs_dbw_1000rpm/`](op_vs_dbw_1000rpm/)

| file | what |
|---|---|
| `running_op_vs_dbw.py` | the whole pipeline. Scans every `.csv` in `EMU_BLACK_V3\Supra`, `…\misc log csv`, `…\LogAutosave`, `supra/logs`, `supra/tunes`; keeps logs that carry `Engine oil pressure`, `DBW Out. DC`, `Ignition Angle`, `Idle state`, `Idle air %`, `TPS`, `MAP`. Re-run it and any new log is in. |
| `samples.csv` | every gated sample, tagged with log name and file date |
| `table.md` | the big table: pooled by 0.25-bar OP bin, then per log × OP bin, then a DC histogram per OP bin |
| `scatter.png` | four panels vs OP: `DBW Out. DC`, `Idle air %`, `TPS`, `MAP×RPM` |
| `session_timeline.py` | one-log timeline figure (RPM/target/state, TPS vs `DBW target` vs duty, air vs PID vs ignition, OP/MAP/CLT/PPS, tune-edit ticks) |

**Gate:** `Idle state`==2, |RPM−1000| ≤ 50, 17 ≤ `Ignition Angle` ≤ 19, `Engine oil pressure status`==1
where present, OP ≥ 0.5 bar, MAP < 60, `AC Clutch`==0 where present. First run: 5,829 samples, 13 logs,
2026-04-08 … 2026-09-19. Many of the August oil-study logs are absent because they do not carry
`DBW Out. DC` (`bighotidle`, `goodrun*`, the 08-04 sweep) — they were exported with narrower channel sets.

## What the first run says

- **`DBW Out. DC` has no structure against oil pressure.** Every OP bin from 1.25 to 5.25 bar spans
  duty −40 → 0; medians bounce −8 / −34 / −13 between adjacent bins because each bin is dominated by a
  different log and a different `dbwMinDC`. Duty is a property of the servo's moment-to-moment stall
  torque and the configured clamp, not of the engine (see
  [`idle_knife_edge_2026-09-19.md`](idle_knife_edge_2026-09-19.md) §2b).
- **`Idle air %` clusters by tune era, not by oil pressure** — 24–29 (08-24), 35–43 (May/June), 46–55
  (09-19 hot), 58–68 (09-19 cold oil). It is a position command through `idleDBWTargetMin/Max`, and both
  the range and the tables have been re-cut several times.
- **`TPS` (the plate) does organise by OP within a day** — 09-19: 4.5–5.4 at 1.5–2.0 bar, 5.6–6.2 at
  3.3–5.2 bar — but the whole cloud shifts ~1.5 % TPS between April and September at the same OP.
- **`MAP×RPM` (the air the engine actually took) is the only panel that is flat and repeatable:**
  35–40 k in every log since April, with a gentle rise from ~36 k at 1.5–2 bar to ~38–39 k at 3.5–5 bar.
  That ~7 % is the entire cold-oil friction term at 1000 rpm. Everything else in the other three panels is
  actuator and calibration.

So the running file answers the question it was built for by showing there is nothing there: oil
pressure at 1000 rpm does not predict the DBW duty, and it barely moves the engine's air. What it does
move is the *plate position* that delivers that air (~1 % TPS across the oil-temperature clock), which
is the useful number and is what the `TPS` panel and `table.md`'s TPS column carry.

## Maintenance

- New log with the channels → drop it in one of the scanned folders, re-run
  `python supra/notes/op_vs_dbw_1000rpm/running_op_vs_dbw.py`. Takes ~1 min (it reads the 90 MB logs).
- Change the RPM centre / tolerance / ignition window at the top of the script (`RPM_C`, `RPM_TOL`,
  `IGN_LO`, `IGN_HI`). The ignition window assumes the idle ignition target is ~18° at hot idle
  (`idleIgnitionTargetTbl` hot rows) — if that target moves, move the window with it or the gate empties.
- Log date = file mtime. OneDrive re-syncs can reset it; if a log's date looks wrong, that is why.
