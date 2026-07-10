# Valve timing and dynamic compression

> Digest of [valve_timing_dynamic_compression.md](../valve_timing_dynamic_compression.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the equations that turn intake cam advance into IVC, overlap, dynamic compression, and low-rpm filling — model a cam change instead of eyeballing it.

**The rules:**

- Advancing the intake cam A crank degrees opens it earlier (overlap +A) and closes it earlier (IVC −A). Earlier IVC pushes less charge back out at low rpm — more bottom-end. At high rpm ram filling reverses it, so advance trades top-end for bottom-end.
- Unit trap: EMU cam tables are in crank degrees. A spec quoted in cam degrees doubles — 19 cam° = 38 crank°, usually far too much overlap.
- IVC sets dynamic compression: DCR = cylinder volume at IVC over clearance volume. Streetable band is 7.5–8.5.
- Overlap is the cost of advance. It hurts idle (worse when idle is spark-only, no air trim) and high-boost VE on a restrictive exhaust, where pre-turbine pressure above MAP drives reversion.
- Big advance is a mid-load/mid-rpm target (cruise, spool) — schedule it with VVT and park or retard it at idle and high boost, never run it globally.
- Worked 1JZ + 272 cam case: 19 crank° of advance took DCR 6.82 → 7.82 (+15%), low-rpm trapped charge +14.6%, overlap 44° → 63°, cranking pressure ~164 → 198 psi. Robust across plausible LSAs.

**Key numbers:** streetable DCR 7.5–8.5; crank degrees = 2 × cam degrees.

**When to care:** before moving `cam1AdvTbl` or degreeing a cam, and when explaining low-end torque, idle quality, or cranking-pressure shifts after a cam change.
