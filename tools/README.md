# tools

Standalone utilities and apps that support the EMU Black tuning work, consolidated here
on 2026-06-12 so they live next to the notes and skills they serve. Nesting is
organizational only — both are git-ignored by this repo (see `../.gitignore`), not merged.

- `emubt_breakout/` — converts EMU Black `.emubt` XML tables to/from CSV for editing and
  re-import (decimal/hex, sign-magnitude encoding). Keeps its own git history and remote
  (`github.com/4AM365/emubt_breakout`); it stays an independent repo nested here. See its README.
- `emub_analysis/` — local Flask web UI that diagnoses EMU Black CSV data logs across seven
  tiers (trigger, lambda, knock, idle, boost, VVT, sensors), with optional Ollama LLM
  root-cause ranking. Local-only. Run `python app.py` (serves on localhost).
