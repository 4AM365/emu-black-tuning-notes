# Josh's GS300 — the short version

> **⛔ NOT THE SUPRA.** GS300 / Aristo / CD009 — a different car from this repo's main
> subject. Never carry values, pins, hardware or conclusions between the two in either
> direction, and never load `supra-specs` for it. One exception since 2026-09-15: lambda
> targets, ignition maps and PID settings may be seeded from the Supra — see
> [`v3_import_gap_list.md`](v3_import_gap_list.md).

**What this covers.** Who the car is and what it's made of, so nobody has to re-derive it.
Canonical note: [`../my_car.md`](../my_car.md) — that one wins if these disagree.

**The car.** Josh Napier's 2000 Lexus GS300, chassis **JZS160**, now running a **2JZ-GTE
VVT-i out of a JDM Toyota Aristo (JZS161)** with the Aristo's own factory ECU.

**The rules.**
- JZS161 Aristo, not JZS147. The older Aristo is non-VVT-i and a different loom entirely.
- The GS300's factory manual (RM718U) is **2JZ-GE only**. For anything engine-side, use the
  Aristo sources, never the GS300 book.
- The Aristo ECU **also runs the automatic transmission** — plug B3 is all shift and
  line-pressure solenoids. There's no separate A/T ECU on that side.
- Don't state an ECU part number, transmission model, or immobiliser status until Josh
  confirms it. None of that is established yet.

**Key numbers.**
- 6 ECU plugs, 147 pins: B1 31, B2 24, B3 17, F59 28, F60 22, F84 26.
- Engine loom ↔ body loom: three white plugs, 90980-11531 (12p), -11527 (10p), -11710 (9p).
- Two possible ECUs: 89661-3A470 (to 06/2000, no immobiliser) or 89666-30180 (07/2000 on,
  immobiliser inside the ECU).

**When to care.** Any wiring, start-up, immobiliser or transmission question on this car.
Everything is in `gs300/reference/` with page indexes in its README — the GS300 EWD and the
workshop manual are both text-searchable; the JDM Aristo diagram book is scans only.

**Still open.** ECU part number · transmission plan · immobiliser strategy · whether EMU
Black is in this car now or historical · what harness is physically installed.
