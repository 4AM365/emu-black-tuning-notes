# Why cammed builds idle badly

> Digest of [cammed_idle_instability.md](../cammed_idle_instability.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the physics chain from cam overlap to idle wobble, and which levers actually move a cammed idle back from the misfire cliff.

**The rules:**

- Any throttled engine idles on ~30% re-inducted exhaust — already at the ~20% dilution threshold where combustion goes unstable. Some idle shake is physics; the tune manages it, it cannot delete it.
- Past the threshold, bad cycles multiply fast, not gradually: slow burn → partial burn → misfire, each one a torque hole that jerks the crank.
- Cams widen the overlap window, so more burned gas backflows into the intake at idle vacuum. Turbo backpressure drives that backflow harder. The breathing advantage at 6000 rpm is the liability at 800.
- The levers, in order: per-cylinder fuel trim first (kill the chronic-misfire cylinder), then raise the idle target (intake momentum fights reversion; flywheel energy goes with RPM²), idle slightly rich (wider misfire margin), more base timing (recenters the slow burn).
- Dilution demands more base advance *and* shrinks the reserve — ignition is the fast stability lever, and advance spent on a clean burn is swing headroom you no longer have.
- The airflow PID cannot fix combustion instability. The disturbance is inside the cylinder and faster than the ~740 ms manifold loop; the PID holds the mean, dilution owns the scatter. Stable lambda above all.
- Don't validate idle VE against the mass-flow channel — reverted flow through the throttle can overstate true combustion airflow ~10× at idle.
- Measure idle quality as crank-speed fluctuation (RPM CoV), not knock voltage.

**Key numbers:** ~30% residual fraction at idle, stock; instability threshold ~20% dilution; airflow loop time constant ~740 ms; flywheel ride-through energy ∝ RPM².

**When to care:** deciding whether a cammed idle is broken or as-good-as-physics, and before reaching for PID gains to chase RPM wobble.
