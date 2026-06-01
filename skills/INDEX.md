# Skills & Scripts Index

All skills live under `skills/<name>/SKILL.md`. Scripts are under `skills/<name>/scripts/`.
The canonical copy of each skill is **this repo** — the Claude skills directory
(`~/.claude/skills/`) is a deployment target, not the source of truth.

## Skills

| Skill | Purpose | Scripts |
|-------|---------|---------|
| [emu-black-tune](emu-black-tune/SKILL.md) | Read, decode, and edit EMU Black XML tune exports (.emub3 / .xml). Scaling conventions, symbol glossary, DBW airflow↔TPS math, cold-start tables. Use for any tune *file* work. | — |
| [emu-black-emubt-export](emu-black-emubt-export/SKILL.md) | Write computed tables back out as importable `.emubt` files. Handles all encoding traps (hex format, signed sign-magnitude, double-quote XML declaration). Use after computing new table values. | [export_emubt.py](emu-black-emubt-export/scripts/export_emubt.py) |
| [emu-black-actuator-rescale](emu-black-actuator-rescale/SKILL.md) | Rescale every airflow-% table when the idle DBW actuator range `[floor, ceiling]` changes. Outputs a folder of `.emubt` files + per-cell report. | [rescale.py](emu-black-actuator-rescale/scripts/rescale.py) |
| [emu-black-log](emu-black-log/SKILL.md) | Parse and diagnose EMU Black CSV data logs (semicolon-delimited, TIME column). Covers stalls, lambda, boost, knock, cold-start. | — |
| [emu-black-log-emublog3](emu-black-log-emublog3/SKILL.md) | Parse EMU Black binary `.emublog3` logs directly, skipping the CSV export step. Requires one-time schema bootstrap from a matching CSV. | [parse_emublog3.py](emu-black-log-emublog3/scripts/parse_emublog3.py) · [discover_schema.py](emu-black-log-emublog3/scripts/discover_schema.py) · [inspect.py](emu-black-log-emublog3/scripts/inspect.py) |
| [emu-black-tune-review](emu-black-tune-review/SKILL.md) | Comprehensive tune audit against Banish/Hartman/Heywood references and EMU conventions. Outputs Validated / Worth-discussing / Verification-gap findings. | [review.py](emu-black-tune-review/scripts/review.py) |
| [emu-black-vvti-street-tune](emu-black-vvti-street-tune/SKILL.md) | Street-tune the VVT-i cam advance table without a dyno, using MAP-at-fixed-TPS as torque proxy. Generates sweep plans, analyzes logs, proposes smoothed cam tables. | [plan_sweep.py](emu-black-vvti-street-tune/scripts/plan_sweep.py) · [analyze_sweep.py](emu-black-vvti-street-tune/scripts/analyze_sweep.py) · [propose_table.py](emu-black-vvti-street-tune/scripts/propose_table.py) |
| [emu-black-ve-smooth](emu-black-ve-smooth/SKILL.md) | Anchor-weighted polynomial smoothing of a VE / fuel-dose table — trusted autotune cells stay pinned, ragged neighbours get pulled onto a low-order curve. Use after a log-based VE correction. | [smooth_ve.py](emu-black-ve-smooth/scripts/smooth_ve.py) |

## Skill pairing guide

```
tune file work:   emu-black-tune  →  emu-black-emubt-export
range change:     emu-black-tune  →  emu-black-actuator-rescale  →  emu-black-emubt-export
log diagnosis:    emu-black-log  (CSV)  |  emu-black-log-emublog3  (binary)
tune audit:       emu-black-tune-review  (reads tune, cites literature)
VVT-i sweep:      emu-black-vvti-street-tune  +  emu-black-log  +  emu-black-tune
VE smoothing:     emu-black-log  (corrections)  →  emu-black-ve-smooth  →  emu-black-emubt-export
```

## Other repo resources

| Path | What it is |
|------|-----------|
| `supra/tunes/` | XML tune exports (`.xml.emub3`) and generated `.emubt` table files |
| `supra/exports/` | Post-drive XML exports |
| `supra/tunes/*.csv` | Log snapshots associated with a tune session |
| `notes/` | First-principles derivations, tuning principles, build observations |
| `supra/notes/` | Supra-specific notes (mass-flow estimator quirks, etc.) |
| `scripts/` | Standalone repo-level utility scripts (OCR, corpus cleanup, etc.) |
| `C:\Code\car-projects\emubt_breakout\` | CSV round-trip tools for editing existing `.emubt` files in a spreadsheet |
