# Engine protection

> Digest of [engine_protection.md](../engine_protection.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the layered stuck-throttle defense (and why it must stay brake-boost-safe), rev limiter setup, and hard limits / fault reporting.

**The rules:**

- Stuck-throttle defense has four layers: dual-TPS plausibility, DBW position-error monitor, the brake-based "Stuck throttle" box, and a fuel/RPM limp cap. Make the first two primary — they're PPS/sensor-referenced and brake-independent.
- PPS separates the dangerous case (throttle open, pedal released) from an intentional brake-boost (pedal commanding it). The brake-based box is blind to PPS, so at tight settings it cuts brake-boosts. This build brake-boosts — never tighten that box or add a brake-gated cut.
- If the brake box needs loosening, raise `stTPSLevel` first (set it just above a logged real brake-boost peak — you keep a fast cut for a WOT-stuck blade), then `stBrakeTimeout`.
- A limp must bound airflow, not just plate angle: the DBW spring-home angle sits above the zero-airflow point and can still run RPM up. Pair the throttle limp with a fuel-cut RPM cap.
- Soft limiters beat hard walls. Prefer ignition or partial cut with a taper control range; stage 1 is the working limiter, stage 2 the hard backstop. A fuel-only hard cut dumps raw fuel and bangs the driveline.
- `Check signal input = None` leaves dual-TPS plausibility inert. Post-stall code 16384 is the plausibility fault — a different mechanism than the brake box.
- Set protection ceilings (fuel cut above pressure, over-temp, over-boost) with margin above the operating envelope, route faults to the CEL/EGT alarm, and confirm in a log that a fault actually limps and reports before relying on it.

**Key numbers:** interim brake-box settings `stTPSLevel` 70 / `stBrakeTimeout` 1500 ms; the Bosch TB swap makes dual-TPS plausibility live.

**When to care:** any protection change, after the Bosch throttle-body swap, and whenever a cut fires during a brake-boost or a limp fails to hold RPM down.
