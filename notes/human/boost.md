# Boost control

> Digest of [boost.md](../boost.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** feed-forward wastegate control, pedal-referenced boost targets shaped as a torque curve, and keeping the turbo lit through shifts.

**The rules:**

- Build the base WGDC table open-loop first: override duty, pull, write the duty that made each boost into its MAP/RPM cell. PID on top of an unmapped base just fights bad feed-forward.
- The boost target is pedal-referenced: zero at closed throttle, rising monotonically to a top-right peak. Power should be asked-for, not a hammer on every throttle breath.
- v2 and v3 firmware read the Boost Target table differently — v2 is absolute kPa (floor 100), v3 is gauge kPa (floor 0). Never copy the table between generations as-is; shift every cell by 100.
- PID hunting (oscillating `Boost PID correction`) and margin triggering (`Boost out of margin` = 1) are different faults with different fixes. Margin protection is a safety limiter, not a control loop — widen its thresholds (±8–10 kPa) for street use.
- Shape boost as a torque curve: ~100% WGDC where the turbo isn't lit, trim the midrange for a flat curve near MBT, build boost again above peak-torque RPM out to redline.
- Spool retention: put a non-zero target (~60–80 kPa) in the 0% PPS / high-RPM cells so the gate stays shut through a shift — but gate that behind VSS or you spike boost at low speed.
- Anti-lag retard (15–25° on clutch + RPM/VSS/recent-TPS gates, ≤1 s with a taper) keeps the turbine spinning but raises EGT hard — never run it ungated.

**Key numbers:** v2↔v3 table conversion = ±100 kPa per cell. kPa × 0.145038 = psi. Spool-retention target 60–80 kPa; anti-lag 15–25° retard, 500–1000 ms max.

**When to care:** before mapping WGDC or enabling boost PID, when copying a boost table between firmware generations, and when diagnosing boost oscillation, shift dropout, or false margin cuts.
