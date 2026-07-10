# Overrun

> Digest of [overrun.md](../overrun.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the deceleration fuel cut, its exit behavior, overrun ignition and throttle, and why return-to-idle stalls are usually airflow problems.

**The rules:**

- The rich spike at cut exit is a symptom. The cause is usually `idleArmedAirFlow` resolving too low at decel RPM — fuel returns into a near-zero air column. Fix the armed airflow table first; raising the exit RPM or stepping the exit are secondary helpers.
- Cut fast, restore slow. Asymmetric enter/exit ramps for both fuel and ignition keep the re-fuel and re-advance steps from stacking into a torque hit the idle PID has to chase. Small RPM hysteresis prevents chatter at the boundary.
- Keep exit enrichment small. A large pulse into a barely-cracked throttle gives a rich stumble on every return to idle; decay it out.
- Cammed / high-compression builds: allow the cut only above a relatively high RPM — the bigger the overlap, the bigger the gap between idle and the exit threshold. A stepped exit (partial cut, then full fuel lower down) is the gentler alternative.
- Overrun DBW should hold enough plate to keep an air column under the engine — and on boost, feed the turbine (~10–15% TPS with fuel cut). Don't let it drive to the spring stop.
- This is also the rod-protection event: high-RPM lift-off loads power-stroke rods in tension. Mitigate with the minimum-RPM threshold, hysteresis, partial reduction, or ignition cut instead of fuel cut.
- Decel fuel correction and lean-cruise gating can trim fuel the wrong way during recovery — raise the RPM floor / gate them well clear of the return-to-idle band.

**When to care:** return-to-idle bogs or stalls, harsh off-throttle "parachute" feel, and high-RPM lift-off on a boosted engine.
