# v3 import gap list — the short version

**What this covers.** What the EMU v2→v3 import tool did to Josh's tune (2026-09-15), what is
still blank, and which blanks the Supra may fill. Canonical note:
[`../v3_import_gap_list.md`](../v3_import_gap_list.md) — that one wins if these disagree.

**The rules.**
- Core maps (VE, ignition, lambda, bins), coils/injector cals, trigger and idle-valve setup
  came across intact. Lambda target is already byte-identical to the Supra's.
- Every renamed PID block was silently reset to defaults: **idle airflow + idle ignition,
  boost, VVT, lambda STFT.** Launch control and overrun were dropped too. Idle closed loop is
  dead until the idle gains are entered.
- Cranking fuel is zeroed and its CLT axis (and the ASE CLT axis) is corrupt. Accel enrichment
  is empty. Wastegate base-DC map is zeroed. All car-specific — rebuild from the v2 file.
- From the Supra, take: idle **ignition** PID + torque-angle tables, VVT cam-1 PID, lambda STFT
  PID, boost PID gains (not the base map), and `overrunIgnition` in place of the −30° decel
  column baked into the GS300 ignition map.
- Do **not** take idle-airflow gains (PWM valve vs DBW blade) or DBW motor PIDs.
- The tool also rewrote the CLT/IAT sensor curves, halved `idleCrankingDC`, and zeroed the
  sensor-failure CEL flags — verify before trusting warm-up or idle tables.

**When to care.** Before first fire on v3 firmware, and any time a v3 symbol on this car
looks "default" — check whether it had a v2 ancestor before assuming Josh set it.
