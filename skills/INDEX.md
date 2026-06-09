# Skills & Scripts Index

All skills live under `skills/<name>/SKILL.md`. Scripts are under `skills/<name>/scripts/`.
The canonical copy of each skill is **this repo** — the Claude skills directory
(`~/.claude/skills/`) is a deployment target, not the source of truth.

## Skills

| Skill | Purpose | Scripts |
|-------|---------|---------|
| [emu-black-tune](emu-black-tune/SKILL.md) | Read, decode, and edit EMU Black XML tune exports (.emub3 / .xml). Scaling conventions, symbol glossary, DBW airflow↔TPS math, cold-start tables. Use for any tune *file* work. | [inventory_tune.py](emu-black-tune/scripts/inventory_tune.py) · [decode_tables.py](emu-black-tune/scripts/decode_tables.py) |
| [emu-black-emubt-export](emu-black-emubt-export/SKILL.md) | Write computed tables back out as importable `.emubt` files. Handles all encoding traps (hex format, signed sign-magnitude, double-quote XML declaration). Use after computing new table values. | [export_emubt.py](emu-black-emubt-export/scripts/export_emubt.py) |
| [emu-black-actuator-rescale](emu-black-actuator-rescale/SKILL.md) | Rescale every airflow-% table when the idle DBW actuator range `[floor, ceiling]` changes. Outputs a folder of `.emubt` files + per-cell report. | [rescale.py](emu-black-actuator-rescale/scripts/rescale.py) |
| [emu-black-log](emu-black-log/SKILL.md) | Parse and diagnose EMU Black CSV data logs (semicolon-delimited, TIME column). Covers stalls, lambda, boost, knock, cold-start. | — |
| [emu-black-log-emublog3](emu-black-log-emublog3/SKILL.md) | Parse EMU Black binary `.emublog3` logs directly, skipping the CSV export step. Requires one-time schema bootstrap from a matching CSV. | [parse_emublog3.py](emu-black-log-emublog3/scripts/parse_emublog3.py) · [discover_schema.py](emu-black-log-emublog3/scripts/discover_schema.py) · [inspect_emublog3.py](emu-black-log-emublog3/scripts/inspect_emublog3.py) |
| [emu-black-tune-review](emu-black-tune-review/SKILL.md) | Comprehensive tune audit against Banish/Hartman/Heywood references and EMU conventions. Outputs Validated / Worth-discussing / Verification-gap findings. | [review.py](emu-black-tune-review/scripts/review.py) |
| [emu-black-vvti-street-tune](emu-black-vvti-street-tune/SKILL.md) | Street-tune the VVT-i cam advance table without a dyno, using MAP-at-fixed-TPS as torque proxy. Generates sweep plans, analyzes logs, proposes smoothed cam tables. | [plan_sweep.py](emu-black-vvti-street-tune/scripts/plan_sweep.py) · [analyze_sweep.py](emu-black-vvti-street-tune/scripts/analyze_sweep.py) · [propose_table.py](emu-black-vvti-street-tune/scripts/propose_table.py) |
| [emu-black-ve-smooth](emu-black-ve-smooth/SKILL.md) | Anchor-weighted polynomial smoothing of a VE / fuel-dose table — trusted autotune cells stay pinned, ragged neighbours get pulled onto a low-order curve. Use after a log-based VE correction. | [smooth_ve.py](emu-black-ve-smooth/scripts/smooth_ve.py) |

### Log-analysis skills (generalized from build-specific scripts)

| Skill | Purpose | Scripts |
|-------|---------|---------|
| [emu-black-egt-analysis](emu-black-egt-analysis/SKILL.md) | Per-cylinder EGT evenness/health from a log — active channels, mean/median/p95, mean-to-mean spread + hottest cylinder, injector trims. | [egt_analysis.py](emu-black-egt-analysis/scripts/egt_analysis.py) |
| [emu-black-charge-temp-analysis](emu-black-charge-temp-analysis/SKILL.md) | IAT / Pre-IC / charge-temp / CLT distribution over no-boost samples + Pre-IC dropout rate (single log). | [charge_temp_distribution.py](emu-black-charge-temp-analysis/scripts/charge_temp_distribution.py) |
| [emu-black-intercooler-heatsoak](emu-black-intercooler-heatsoak/SKILL.md) | Ambient-normalized charge-temp / intercooler comparison **across** logs (hood on/off, hot vs cool). | [intercooler_heatsoak.py](emu-black-intercooler-heatsoak/scripts/intercooler_heatsoak.py) |
| [emu-black-fuel-temp-analysis](emu-black-fuel-temp-analysis/SKILL.md) | Fuel-temperature summary (start cold anchor → heat-soak rise) across logs. | [fuel_temp.py](emu-black-fuel-temp-analysis/scripts/fuel_temp.py) |
| [emu-black-temp-sensor-recal](emu-black-temp-sensor-recal/SKILL.md) | Rebuild a mis-curved custom temp sensor by resampling a known-good curve → corrected `.emubt`. | [temp_sensor_recal.py](emu-black-temp-sensor-recal/scripts/temp_sensor_recal.py) |
| [emu-black-idle-stability](emu-black-idle-stability/SKILL.md) | Idle target-tracking + stability from RPM (bias/RMS, CoV, hunt frequency), per regime/setpoint. | [idle_stability.py](emu-black-idle-stability/scripts/idle_stability.py) |
| [emu-black-idle-drift](emu-black-idle-drift/SKILL.md) | Attribute a hot-soak idle drift to PID vs charge-temp (airflow split + per-channel trend/correlation). | [idle_drift_attribution.py](emu-black-idle-drift/scripts/idle_drift_attribution.py) |
| [emu-black-lambda-tracking](emu-black-lambda-tracking/SKILL.md) | Lambda tracking quality (measured vs target %), bias + spread by MAP bin; A/B map comparison. | [lambda_tracking.py](emu-black-lambda-tracking/scripts/lambda_tracking.py) |
| [emu-black-knock-cov](emu-black-knock-cov/SKILL.md) | Combustion-CoV proxy from knock-voltage scatter (detrended, transitions only); A/B map comparison. | [knock_chatter_cov.py](emu-black-knock-cov/scripts/knock_chatter_cov.py) |
| [emu-black-ve-lambda-verify](emu-black-ve-lambda-verify/SKILL.md) | veTable × lambda_target product test — confirms the VE dose carries the lambda enrichment (no boost-knee dip). | [verify_ve_vs_lambda.py](emu-black-ve-lambda-verify/scripts/verify_ve_vs_lambda.py) |
| [emu-black-ve-delta-map](emu-black-ve-delta-map/SKILL.md) | 3D delta surface between two table `.emubt` exports (before vs after). | [ve1_delta_map.py](emu-black-ve-delta-map/scripts/ve1_delta_map.py) |
| [emu-black-ve-lambda-remap](emu-black-ve-lambda-remap/SKILL.md) | Build one VE table from another via the lambda-target delta (VE2 = VE1 × (1 − Δλ)); emits a JSON spec + back-calc report. | [remap_ve_for_lambda_delta.py](emu-black-ve-lambda-remap/scripts/remap_ve_for_lambda_delta.py) |
| [emu-black-ve-from-log](emu-black-ve-from-log/SKILL.md) | Correct veTable/veTable2 from a closed-loop log (F = (1+STFT/100)×λ_act/λ_tgt, steady samples, bilinear accumulate) and write a corrected tune. | [ve_correct.py](emu-black-ve-from-log/scripts/ve_correct.py) |

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
| `scripts/` | Standalone repo-level utility scripts (OCR, corpus cleanup, etc.) — NOT tune/log analysis |
| `supra/scripts/` | (now empty) — the former Supra analysis scripts were **generalized into the log-analysis skills above**. New reusable analyses should be a skill, not a script here; truly one-off Supra-only scratch can still live here. |
| `C:\Code\car-projects\emubt_breakout\` | CSV round-trip tools for editing existing `.emubt` files in a spreadsheet |
