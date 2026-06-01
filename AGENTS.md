# Codex working rules for emu-black-tuning-notes

## Skills and scripts

**Before generating any table, script, or file from scratch, check `skills/INDEX.md`.**
A skill or script for the task likely already exists. If it does, use it — do not
reimplement it inline. If a script is referenced in a skill, its path in this repo is
`skills/<skill-name>/scripts/<script>.py`, not `scripts/<script>.py`.

Skill pairing quick-reference:
- Tune file (read/decode/edit) → `emu-black-tune`
- Write a table as `.emubt` → `emu-black-emubt-export` + `skills/emu-black-emubt-export/scripts/export_emubt.py`
- Actuator range change → `emu-black-actuator-rescale` + `skills/emu-black-actuator-rescale/scripts/rescale.py`
- CSV log diagnosis → `emu-black-log`
- Binary `.emublog3` log → `emu-black-log-emublog3`
- Full tune audit → `emu-black-tune-review`
- VVT-i street sweep → `emu-black-vvti-street-tune`

## Tune files

- XML exports are the readable format: filename contains `.xml.emub3`.
- Binary `.emub3` files start with `PK` — not grep-able, skip them.
- Canonical files live in `supra/tunes/` and `supra/exports/`.
- The EMU OneDrive folder (`EMU_BLACK_V3\Supra`) is the source for files not in the repo.

## Table math rules

- **Never guess on table conversion.** Do per-cell math and show the full back-calc first.
- Always read `idleDBWTargetMin` and `idleDBWTargetMax` from the tune file before computing
  any airflow rescale — never assume values from history.
- Verify scale empirically (one cell: `raw × scale` vs EMU display) before trusting any
  scale constant.
- When displaying MAP/RPM tables, show RPM increasing on the Y axis and MAP increasing
  on the X axis. Put RPM labels on the left and MAP labels at the bottom.

## Notes and documentation

- When a first-principles derivation or tuning principle surfaces, write it to `notes/`
  before the conversation ends.
- Capture thermal, density, or torque derivations to `notes/` — they are expensive to redo.

## Theory / RAG rule

- For theoretical engine, combustion, controls, fuel, or tuning questions, bias hard toward
  repo-local retrieval before answering from model memory. Check `README.md`'s Academic
  sources list, then search `corpus/` and `notes/` for the relevant text.
- Prefer direct references to indexed/extracted texts such as
  `corpus/ice_fundamentals.md` (Heywood), `corpus/engine_management_advanced_tuning.md`
  (Banish), `corpus/how_to_tune.md` (Hartman), Bosch, Bell, and Kiencke/Nielsen.
- If the answer is not grounded in retrieved local text, say that explicitly and label it
  as model knowledge or a hypothesis. Do not present theory from embedding memory as
  book-backed fact.
- If detailed theory is required, directly retrieve the relevant page/section from the
  reference text before answering. If the source is not yet text-searchable, create or
  use a quickly accessible `.txt`/`.md`/corpus extract in `corpus/` (source PDFs/EPUBs
  live in the shared `../../agentic-library/engine-dynamics/` repo) so future turns can
  quote/check it directly. Keep quotes short and cite the local source path/page marker
  when available.
