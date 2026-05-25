# EMU Black tuning notes

Practitioner notes and analysis tooling for tuning engines with the ECUMaster EMU Black ECU. Designed to be useful as standalone reference and as RAG/context source for code/tuning assistants.

## Layout

```
.
├── notes/        Generic tuning principles — cranking, idle, boost, timing, etc.
│                  Reusable across any EMU Black build. No vehicle-specific values.
├── skills/       Claude Code skills for EMU Black workflows (deployable).
│                  Symlink or copy into ~/.claude/skills/ to use them.
├── scripts/      Generic analysis utilities (corpus prep, etc.).
├── corpus/       Extracted text from academic engine-tuning books (gitignored).
├── books/        Source PDFs / EPUBs of those books (gitignored).
└── supra/        Build-specific data and notes for one particular car
                   (1994 MKIV Supra, 2JZ-GE + VVT-i, 10:1, 264° cams, BorgWarner 61.44).
                   Excluded if you want only generic context.
    ├── notes/
    ├── tunes/    .emub3 project exports
    ├── exports/  .emubt single-table imports
    ├── logs/     CSV log exports (gitignored)
    └── scripts/  Scripts that hardcode this build's data paths
```

## For RAG / context retrieval

- **Generic context only:** include `notes/`, `scripts/`, optionally `corpus/`. Exclude `supra/`.
- **Build-specific work:** include everything, or specifically `supra/` plus the relevant generic notes.

The `notes/` directory is deliberately scrubbed of vehicle-specific values, calibration snapshots, and per-build calibration targets. Cross-cutting principles (e.g. "set idle base ignition below MBT for reserve-of-torque headroom") live there; specific numbers ("this car runs 16.5° base at warm idle") live in `supra/notes/`.

## Skills (`skills/`)

All six live in `skills/` as deployable Claude Code skills with proper YAML frontmatter. Copy or symlink into `~/.claude/skills/` to use.

**Core tooling:**

- **`emu-black-tune`** — reads/decodes/edits EMU Black `.emub3` XML project exports. Knows storage types, sign-magnitude hex, axis bin conventions, the airflow-% encoding (0.5/count, the common trap), the DBW actuator-range rescale formulas, and the symbol glossary for the idle/cranking/airflow domain.
- **`emu-black-emubt-export`** — writes `.emubt` single-table imports that EMU Black accepts. Bundles `scripts/export_emubt.py` which handles encoding traps (uppercase hex, sign-magnitude, no XML single-quote declarations) and validates per-storage-type ranges.
- **`emu-black-log`** — analyses EMU Black CSV data logs. Triage flow, channel reference by diagnostic tier, common diagnostic patterns (idle stall, lean surge, knock event, boost overshoot), and ready-to-run Python templates for the common analyses.

**Workflow automation:**

- **`emu-black-actuator-rescale`** — rescales every airflow-% table in a tune when the DBW actuator range changes, preserving the actual throttle position at each cell. Handles preserve-TPS, additive (slope-only), and PID width-scaling rules; emits a folder of importable `.emubt` files plus a per-cell summary report with clamp warnings.
- **`emu-black-log-emublog3`** — parses EMU Black's binary `.emublog3` log format directly (skipping the manual CSV export). Includes a schema-discovery tool that bootstraps the binary layout from a paired CSV one time, and a parser that uses the saved schema for all future logs from the same ECU configuration.
- **`emu-black-tune-review`** — runs a structured review of a tune against codified checks derived from Banish, Hartman, Heywood, and EMU Black architecture conventions. Categorises findings as Validated / Worth-discussing / Verification-gap with citations and suggested actions.

## Academic sources (in `corpus/`)

Synthesised throughout the notes:
- Hartman, *How to Tune and Modify Engine Management Systems*
- Banish, *Engine Management: Advanced Tuning*
- Heywood, *Internal Combustion Engine Fundamentals*
- Bell (Graham), *Four-Stroke Performance Tuning*
- Bell (Corky), *Maximum Boost*
