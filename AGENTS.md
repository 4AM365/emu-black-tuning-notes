# Agent working rules for emu-black-tuning-notes

<!-- AGENTS.md and CLAUDE.md are kept as essentially identical duplicates. Edit both. -->

## Skills and scripts

**Before generating any table, script, or file from scratch, check `skills/INDEX.md`.**
A skill or script for the task likely already exists. If it does, use it — do not
reimplement it inline. If a script is referenced in a skill, its path in this repo is
`skills/<skill-name>/scripts/<script>.py`, not `scripts/<script>.py`.

Skill pairing quick-reference:
- Tune file (read/decode/edit) → `emu-black-tune`
- Write a table as `.emubt` → `emu-black-emubt-export` + `skills/emu-black-emubt-export/scripts/export_emubt.py`
- Pull scalar parameters as `.emubp` (cam/VVT/overrun/PID settings, e.g. "pull the cam settings from land cruiser to emubp") → `emu-black-emubp-export` + `skills/emu-black-emubp-export/scripts/pull_emubp.py`
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

## Source folders

- A repo/vehicle name resolves to its EMU source folder via `EMU_SOURCE_INDEX.md`.
  Rule: **`<reponame>` → `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\<reponame>`**
  (default to the V3 tree; fall back to the older `EMU_BLACK` V1 path only when noted).
- Quick map: `supra` → `EMU_BLACK_V3\Supra` (+ `LogAutosave`), `bradley` →
  `EMU_BLACK_V3\bradley` (1JZ; V1 `EMU_BLACK\bradley-1jz`), `land cruiser`/`fj80` →
  `EMU_BLACK_V3\Land Cruiser`, `napier`/`gs300` → V1 `EMU_BLACK\Napier_GS300` only.
- Access rules (per global CLAUDE.md): normal/local access only for `supra`; for every
  other folder, open only the specific file named — no broad OneDrive traversal.
- **Maintenance:** whenever a tune repo/vehicle is mentioned that isn't already in
  `EMU_SOURCE_INDEX.md`, check for `EMU_BLACK_V3\<name>` (shallow, directory-only — no
  recursion). If it exists, add a row to `EMU_SOURCE_INDEX.md` and the quick map above.
  If only an older `EMU_BLACK\<name>` (V1) folder exists, note it as V1-only. If neither
  exists, say so and don't add a row.

## Verify the system in the tune before reasoning about it

- **Before speculating about any vehicle system or subsystem, read that car's tune XML
  to confirm the system exists, is enabled, and how it is configured.** Ground the
  reasoning in the actual calibration, not in assumptions about what a generic build has.
- This is general — it applies to every subsystem, e.g.:
  - *Idle airflow control* → does the car run DBW, an idle solenoid/PWM valve, or no idle
    air control at all? Read `idleActiveAirflow`/`idleArmedAirFlow`/`idleCrankingDC`/
    `idleDBWTargetMin/Max` and the relevant enable flags before discussing idle behavior.
  - *Ignition stability* → number of coils/outputs, dwell strategy, cranking/idle ignition
    tables, knock setup — read them before reasoning about timing or misfire.
  - *Fueling* → injector setup, VE vs lambda role, flex-fuel blend tables, per-cylinder trim.
  - *Boost / VVT / launch / overrun* → confirm the feature is wired and enabled (its
    tables/flags are present and non-default) before assuming it is active.
- Resolve the right tune via `EMU_SOURCE_INDEX.md` for the car named, and use the
  `emu-black-tune` skill to decode symbols/scaling correctly.
- If a relevant symbol/flag can't be found or read, **say the configuration is unverified**
  and label any conclusion as a hypothesis — do not present generic-build assumptions as
  facts about this car.

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
- **Hard notes are the source of truth — not agent memory.** For this subject, rely on the
  repo's `notes/`, `skills/`, and `corpus/`, not on remembered facts. Memory may index or
  point to a note, but the note is authoritative; if memory and a note conflict, the note
  wins. Anything worth keeping goes into a file here, not only into memory.

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

## Model with equations — don't hand-wave a quantitative claim

- **Any claim about how one quantity affects another — a Δ, a "shifts up/down", a "roughly
  X%", a trend vs RPM/load/temp — must be backed by the governing equation(s) and an actual
  computation, not an adjective.** "Advancing the cam helps low end" is not an answer;
  "IVC 70°→51° ABDC ⇒ DCR 6.82→7.82 via `DCR=V(θ_IVC)/V_c`" is.
- For **each point** you consider, work it:
  1. **Seek the equation** — retrieve it from `corpus/`/`notes/` first (per the Theory/RAG
     rule); if it is standard and not in-corpus, state it from model knowledge and label it.
  2. **State inputs and assumptions explicitly**, pulling the real values from the tune
     (per "verify the system in the tune") instead of assuming them.
  3. **Compute and show the number.** For a relationship, **sweep** the variable and present
     the table/trend, not a single point.
  4. **Sensitivity:** vary the uncertain inputs (assumed LSA, scale, charge temp, …) and
     report the range, so the conclusion's robustness is visible.
- Prefer a short script over hand arithmetic for any multi-cell/multi-point relationship
  (keep it out of the repo unless reusable); still show the equations in the writeup.
- **Capture the derivation + worked numbers to `notes/`** so they're reusable. Cite the
  corpus path when retrieved; label model-knowledge equations as such.
- If you can't find or justify an equation for an effect, **say so and mark the claim a
  hypothesis** — do not present a guess as a modeled result.
