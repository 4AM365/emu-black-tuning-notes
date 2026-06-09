---
name: emu-black-egt-analysis
description: >-
  Analyzes per-cylinder EGT (exhaust gas temperature) evenness and health from an
  EMU Black CSV data log. Use whenever the user wants to "check my EGTs", "are my
  cylinders even", "which cylinder is running hot/lean", "EGT spread", "compare
  exhaust temps", "is the rear cylinder hot", or is diagnosing cylinder-to-cylinder
  fuel/air distribution (front-feed manifolds run the rear cylinders lean and hot).
  Detects active EGT channels (CAN EGT 1..8, EGT 1/2), filters to warm running rows
  where every probe is firing, and reports per-cylinder mean/median/p95 plus the
  mean-to-mean spread and the hottest cylinder; also reads back active per-injector
  trims. Works on any multi-cylinder EGT-instrumented EMU Black (or EMU Classic)
  build — not vehicle-specific. Pairs with emu-black-log (general CSV diagnosis) and
  feeds per-cylinder fuel-trim decisions.
---

# EMU Black EGT evenness analysis

Reads an EMU Black CSV log and quantifies **cylinder-to-cylinder EGT distribution** —
the cheapest proxy for per-cylinder mixture (and the primary signal for front-feed
intake-manifold maldistribution, where the rear cylinders run lean and hot).

## What it measures

1. **Active EGT channels** — `CAN EGT 1..8`, `EGT 1`, `EGT 2`; a channel counts as
   active if it has > ~100 non-zero samples.
2. **Per-cylinder evenness** — over **warm running** rows (`ECU State == 3`, `CLT >
   70 °C`) where **all** active probes are firing (`> 300 °C`), the per-cylinder
   mean / median / p95 and the **mean-to-mean spread** (and which cylinder is
   hottest). A tight spread = uniform combustion; a high outlier = a lean/hot
   cylinder.
3. **Per-injector trims** — reads back any active `Injector N trim` channels so you
   can see what correction is already applied. (Note: this channel reports flow
   scaling, not the per-cylinder fuel-trim *table* output.)

## Usage

```bash
python scripts/egt_analysis.py LOG.csv [--clt 70] [--firing 300] [--state 3]
```

- `LOG.csv` — EMU semicolon-delimited CSV export (any build).
- `--clt` warm threshold, `--firing` EGT-firing threshold, `--state` running ECU State.
- Requires `pandas` + `numpy`.

## Interpreting the result

- **Spread within ~20–30 °C** at load → cylinders are well matched.
- **One cylinder consistently hotter** → likely lean; add per-cylinder fuel trim at
  that cylinder (front-feed manifolds typically need 5–10 % extra on the rearmost),
  tapering under boost where manifold pressure dominates distribution.
- A delta that **shrinks as load rises** is real airflow maldistribution; a
  **load-constant** delta is more likely a probe offset.
- EGT is also the primary **MBT proxy at cruise** (lower EGT → closer to MBT) — see
  the ignition/timing notes.

## Related

- Background + the per-cylinder-trim method live in the repo notes
  (`notes/fueling.md`, `notes/knock_sensors.md`, the per-cylinder-trim distribution
  note, and `ai-analysis-skills/`). Build-specific measured EGT results live under
  `supra/notes/`.
- Pairs with `emu-black-log` (general CSV diagnosis) and `emu-black-emubt-export`
  (write per-cylinder trim tables back out).
