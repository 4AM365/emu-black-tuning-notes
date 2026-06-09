---
name: emu-black-ve-from-log
description: >-
  Corrects an EMU Black VE table (veTable / veTable2) from a closed-loop CSV log and
  writes a corrected copy of the tune. Use whenever the user wants to "autotune my VE
  from a log", "correct my fuel map from this drive", "apply STFT corrections to the VE
  table", "fix my VE from closed-loop data", "log-based VE correction", or has a steady
  log and wants the resulting per-cell VE corrections baked into the tune. Computes
  F = (1 + STFT/100) × (lambda_actual / lambda_target) over steady closed-loop samples
  only, accumulates bilinearly into the VE grid, clamps per-pass, applies to both flex
  tables, and writes a new XML with stale checksums (EMU recomputes on import). Prints a
  per-cell correction map + before→after. Pairs with emu-black-ve-smooth (clean up the
  result) and emu-black-emubt-export.
---

# EMU Black VE correction from a closed-loop log

Reads `veTable`/`veTable2` + axes from a tune XML, derives per-cell corrections from a
log, and writes a corrected tune.

## Method

- **Per-cell factor:** `F = (1 + STFT/100) × (λ_actual / λ_target)` — folds in the trim the
  ECU is already applying *plus* any residual the loop hasn't caught. In settled closed loop
  λ_actual ≈ λ_target, so F ≈ `(1 + STFT/100)`.
- **Steady closed-loop only:** `Lambda is valid==1 & F.Short term trim==1 & Fuel Cut==0 &
  Overrun status<2 & ASE==0 & Warmup==0 & |Acc. enrichment|≤1`. Open-loop/decel samples are
  transient-contaminated and excluded (they produce spurious corner corrections).
- **Bilinear accumulate + gate:** each sample spreads across its 4 surrounding cells by
  weight; a cell is corrected only once its accumulated weight ≥ threshold (~1 s @ 25 Hz).
  Clamp ±15 %/pass.
- **Both tables:** the same factor is applied to `veTable` and `veTable2` — a dose error
  measured at one ethanol content corrects the *blended* result, so distributing it keeps
  both in play (and preserves their offset). The EMU VE table is a fuel-**dose** proxy, not
  pure air VE; this is a first cut — verify each on its own fuel.

## Usage

```bash
python scripts/ve_correct.py --tune TUNE.xml.emub3 --log LOG.csv --out CORRECTED.xml.emub3 \
    [--clamp 0.15] [--weight-threshold 25] [--acc-tol 1.0]
```

Requires `pandas` + `numpy`. Output checksums are stale; EMU recomputes on import.

## Related

- `emu-black-ve-smooth` — smooth the corrected (patchy) table afterward.
- `emu-black-ve-lambda-verify` / `emu-black-ve-delta-map` — sanity-check the result.
- Method note: `ai-analysis-skills/ve_correction_from_log.md` /
  `ve_correctness_from_log_method.md`.
