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
- **Never attempt to unzip, decode, or decrypt binary tune/QuickSave files** (their
  contents are `.crypted` — it's a dead end and wasted compute). If a needed value
  exists only in a binary file, **stop and ask Will to export it** (XML or .emubt),
  then continue. Ask-don't-chase applies to any unreadable artifact here.
- Canonical files live in `supra/tunes/` and `supra/exports/`.
- The EMU OneDrive folder (`EMU_BLACK_V3\Supra`) is the source for files not in the repo.

## Source folders

- A repo/vehicle name resolves to its EMU source folder via `EMU_SOURCE_INDEX.md`.
  Rule: **`<reponame>` → `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\<reponame>`**
  (default to the V3 tree; fall back to the older `EMU_BLACK` V1 path only when noted).
- Quick map: `supra` → `EMU_BLACK_V3\Supra` (+ `LogAutosave`), `bradley` →
  `EMU_BLACK_V3\bradley` (1JZ; V1 `EMU_BLACK\bradley-1jz`), `land cruiser`/`fj80` →
  `EMU_BLACK_V3\Land Cruiser`, `napier`/`gs300` → `EMU_BLACK_V3\Napier_GS300` (v3 import 2026-09-15; v2 sources in V1 `EMU_BLACK\Napier_GS300`).
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

## Match the log to the calibration that was live

When the question is about a log — especially an old one — establish what the ECU was actually
running at that moment, in this order:

1. **Derive it from the log first.** If the parameter is recoverable from logged channels, do that
   and stop: it is authoritative for that instant and cannot go stale. Examples — idle target
   arithmetic (base + `Idle ramp down offset` + the A/C / VSS / clutch increases) recovers each
   increase; a threshold shows up as the value at which a state flips (`Idle state`,
   `Idle force open loop`, `Idle control active`); open-loop base airflow = `Idle air %` minus
   `Idle PID air % correction` minus `Idle airflow custom corr.`.
2. **Otherwise use the tune export immediately preceding that log, by date — not the newest one.**
   Check `supra/tunes/`, then `supra/exports/`, then the EMU source folder; many logs have a
   same-named export beside them. A later export describes edits made after the drive.
3. **If only a binary `.emub3` exists for that date, stop and ask Will to export the XML.** Never
   decode the binary. Name the file and the parameter you need, then carry on with everything that
   does not depend on it.
4. **Check `Data changing` / `Making permanent` before pooling any statistic.** Segment the log at
   the last edit and state which segment each result came from.
5. **When a derived value and an export disagree, the log wins for that log.** Say so plainly and
   ask which was in force — do not report it as a firmware or scaling anomaly.

## Table math rules

- **Never guess on table conversion.** Do per-cell math and show the full back-calc first.
- Always read `idleDBWTargetMin` and `idleDBWTargetMax` from the tune file before computing
  any airflow rescale — never assume values from history.
- Verify scale empirically (one cell: `raw × scale` vs EMU display) before trusting any
  scale constant.
- **EMU table axes are editable scales; only the cell count is fixed.** A table's size (e.g. `veTable`
  16 × 20) is set by firmware, but its axis bins (`rpmBins`, `mapBins`, …) are whatever values Will enters.
  The Supra's `rpmBins` is currently an even 500 → 7000 spread across the fixed 20 bins (09-19 export), and
  can just as well be 200 → 7000 or any spacing. **When Will says "add a row", he means re-scale the
  axis so a bin lands where it's needed.** Never describe it as shifting rows, dropping a row, or making the
  table bigger (Will, 2026-09-30, after repeated misstatements). Re-scaling moves every bin, so cell values
  have to be re-mapped to the new bins. Do the per-cell math (rule above).
- When displaying MAP/RPM tables, show RPM increasing on the Y axis and MAP increasing
  on the X axis. Put RPM labels on the left and MAP labels at the bottom.

## Cranking tables are VE-relative — read the VE cells first

Whenever a cranking table (`crankingCorrTbl`/`crankingCorrTbl2`, and by extension ASE) is discussed or changed:

- **The cranking dose is the VE fuel equation × (1 + cranking %)**, not a standalone fuel demand
  (`notes/engine_start.md` → Cranking fuel equation). A cranking % is a correction to the VE cell
  being looked up, and it means nothing without that cell.
- **The VE table's RPM axis bottoms out at 500 rpm and clamps there.** Cranking runs at ~150–250 rpm and
  near-atmospheric MAP, so it reads the high-MAP (WOT) end of the 500 rpm row. Will added that 500 rpm bin
  so a **running** engine that bogs to ~500 rpm gets rescued, and it works (2026-09-30). Its cells describe
  a bogging running engine, **not cranking fuel demand**. The cranking table corrects that mismatch
  (B = VE_true/VE_table), and the correction stays there: don't move the VE axis down to a cranking speed,
  because the bog band would then blend with a cranking-speed bin.
- **Before reasoning about any cranking cell, read from the current export the VE cells the crank and
  run-up actually look up:** the 500 rpm row at the logged cranking MAP, and the cells between the
  500 rpm row and the next row up at the falling MAP through the run-up to `crankingThreshold`. Reason
  in absolute dose (VE × MAP × (1 + %)) or true enrichment ((1 + %)/B − 1), not in table %.
- Corollaries: any edit to the low-RPM, high-MAP VE cells silently rescales every cranking cell. A
  cranking % and an ASE % can be compared directly only at the same instant (same VE cell), e.g. at
  the Cranking → Afterstart exit.

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
