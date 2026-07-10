# DBW / throttle

> Digest of [dbw.md](../dbw.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** what sets throttle feel, the "ready to launch" boost-on-pedal philosophy, lift-off rod protection, stuck-throttle safety, and hot throttle-body leakage. Idle owns the closed-throttle domain — this picks up where the pedal takes over.

**The rules:**

- The DBW characteristic (PPS→TPS map) is the biggest feel lever. Linear at high RPM for predictable closing, scoop the low-PPS/low-RPM quadrant to kill creep jerkiness, bump upper PPS so downshift blips stay effective.
- Don't reference the characteristic on MAP — a gentle low-MAP map never builds the MAP it's gated on. Use RPM/PPS.
- The build's philosophy: blow the plate open early, meter power via WGDC on pedal position, reference boost pre-throttle so pressure is ready in the charge pipes.
- The TPS rate limit governs transient rate only. Reduce it at high speed for gentler lift-off, prefer fast-open / slow-close, and never set it low enough to fight the idle controller's own plate movements.
- Lift-off rod protection is fuel/ignition work — overrun cut minimum RPM, hysteresis, partial or ignition cut. Slower throttle closure only helps indirectly; it is not the primary lever.
- PPS is the stuck-throttle discriminator. The brake-based box is blind to PPS and will cut a brake-boost — keep it permissive; this car brake-boosts. Config lives on the Engine protection page.
- Hot closed-plate leakage rises (aluminum bore outruns the stainless plate). Compensate as a CLT/IAT-indexed `idleCustomCorrection`, more negative at lower idle RPM — not a fixed DBW floor.
- For the creep zone, consider raising the idle closed-loop cutoff so the idle PID stays active into creeping speed instead of a hand-off no-man's-land.

**Key numbers:** TPS rate limit range 0–1300°/sec, plus a +125°/sec RPM-referenced adjustment.

**When to care:** throttle-feel or creep-jerkiness complaints, high-RPM lift-off on boost, hot-idle drift, and before touching the characteristic, rate limit, or stuck-throttle settings.
