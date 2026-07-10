# Spark delta for the cam + compression change

> Digest of [spark_delta_cam_cr_change.md](../spark_delta_cam_cr_change.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how much advance to add to the E100 ignition table (`ignTable2`) for the 264°→272° intake cam and CR 10→9 change, and where on the map it lands.

**The rules:**

- Both changes want MORE advance. The bigger cam adds it at low-rpm/light-load (overlap dilution slows the burn) and fades to ~0 at high-rpm WOT. The CR drop adds +1 to +2° everywhere via slower flame, biggest at heavy load.
- Combined delta: +4° in the low-rpm/light-load corner tapering to +2° at high-rpm/heavy-load. Cam dominates the upper-left, CR dominates the right.
- Signs are solid (every cell ≥ 0); magnitudes are ±1–2° ballparks — confirm on dyno, knock-ear, and EGT before trusting them.
- E100 only. On the pump table the same CR drop ALSO buys knock relief in the heavy-load/low-rpm corner — don't reuse these numbers there.
- timing.md's numeric duration tables give the opposite sign at light load — treat their light-load trend as inverted/unreliable. The prose (and Hartman/Heywood) say bigger cam = more cruise advance; that's the view to trust.
- At partial ethanol the flex blend delivers only a fraction of any `ignTable2` step — a full delta there shows up diluted in the car.
- Assumes VVT-i scheduling comparable to today. Parking the 272 retarded at idle/light load cuts overlap and shrinks the upper-left adds.

**Key numbers:** `ignTable2` is sbyte ×0.5°/count. Rule of thumb ~1° advance per CR point (practitioner rule, not a book coefficient).

**When to care:** after the cam/compression swap lands and before touching `ignTable2`, or whenever timing.md's duration-delta tables are about to be cited.
