# Did the per-cylinder trim cut knock peaks and idle misfire? (2026-10-02)

Open `report.html` in a browser (self-contained, data embedded). Published copy:
https://claude.ai/artifact/3zSN8dgNbZogYhKRjPzkKr (private to Will's account).

Canonical findings live in [`supra/notes/per_cylinder_trim_results.md`](../../notes/per_cylinder_trim_results.md)
§ "Before/after from decoded autosaves". This folder is the evidence: charts, data and the scripts that made them.

## Data
- 119 LogAutosave `.emublog3` files, 2026-03-01 → 09-29, decoded directly with
  `skills/emu-black-log-emublog3/scripts/supra_decode_504.py` (layout pinned 2026-10-02, exact match against two CSV exports).
  20 duplicate or empty autosaves dropped (block-hash dedupe in `decode_autosaves.py`).
- Each sample's period comes from its logged `Injector 6 trim` (100 = no trim) and `Ethanol content`:
  before E57 = Mar 29 → May 4 17:25; after E57 = May 4 17:38 → May 10; after later = May 11 → Sep 29 (E25 then E14);
  pump fuel Mar 1 → 29 is kept for the EGT and boost tables only.

## What it compares
Cyl 6 knock-voltage spikes (above 1.5× / 2× the pooled 250 rpm × 10 kPa cell median) at idle, cruise and boost, all six
cylinders, per drive; knock vs boost scatter and the 99th-percentile tail; matched full-pedal pulls; idle RPM and lambda jitter
(`emu-black-idle-stability` method, gated on `Idle state` 2); cyl6 − cyl3 EGT by load band; boost peaks vs target;
knock-voltage CoV (`emu-black-knock-cov` method, no-knock gate unavailable in the binary).

## Rebuild
```
python scripts/decode_autosaves.py   # LogAutosave -> data/eb_all.pkl (gitignored, ~1 GB in memory)
python scripts/analyse.py            # -> data/report_data.json (EGT, boost, scatter, pulls, idle jitter)
python scripts/questions.py          # -> data/questions.json (knock-peak exceedance, idle misfire proxies, traces)
python scripts/build_html.py         # -> report.html
```
