# EMU Black tuning notes

Practitioner notes and analysis tooling for tuning engines with the ECUMaster EMU Black ECU. Designed to be useful as standalone reference and as RAG/context source for code/tuning assistants.

## Layout

```
.
├── notes/        Generic tuning principles — cranking, idle, boost, timing, etc.
│                  Reusable across any EMU Black build. No vehicle-specific values.
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

## Tooling

- **`emu-black-tune` skill** — reads/decodes/edits EMU Black `.emub3` XML project exports
- **`emu-black-emubt-export` skill** — writes `.emubt` single-table imports that EMU Black accepts
- **`emu-black-log` skill** — analyses EMU Black CSV data logs

## Academic sources (in `corpus/`)

Synthesised throughout the notes:
- Hartman, *How to Tune and Modify Engine Management Systems*
- Banish, *Engine Management: Advanced Tuning*
- Heywood, *Internal Combustion Engine Fundamentals*
- Bell (Graham), *Four-Stroke Performance Tuning*
- Bell (Corky), *Maximum Boost*
