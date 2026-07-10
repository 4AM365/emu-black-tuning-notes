# Hot-idle drift and the two-PID windup fix

> Digest of [idle_hot_drift_pid_windup.md](../idle_hot_drift_pid_windup.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why a hot-soaked idle enters high and walks down slowly, how EMU's two-PID idle actually divides the work, and the anti-windup fix that removes the purge-then-stall risk.

**The rules:**

- On a hot stop the ~30 s walk-down to target is done by the feed-forward charge-temp air bleed. The airflow PID sits pinned on its negative clamp the whole time, contributing nothing dynamic.
- Don't add feed-forward to speed it up. FF is deliberately gentle because throttle-body metal lags CLT — an aggressive FF pulls air on the sensor's schedule before the body has actually soaked, and sags idle early.
- EMU runs two cooperating idle PIDs: ignition is the fast RPM lever; the airflow PID doesn't watch RPM at all — it trims air to re-center the ignition angle on its target so the two don't fight.
- So the stall-safe way to knock down a high hot idle is ignition retard, not air. Timing reverses in one combustion cycle — no air purge, no shut throttle, no manifold fill lag. If logged idle ignition correction isn't using its full swing, open up the Min torque ign angle table.
- The failure mode to avoid: the negative airflow integral winds up, purges the charge air, forces the DBW toward shut — and the next load step can't get air back fast enough. Stall.
- The fix: cap the integral independently and tight (`idleAirFlowIntegralLimitMin/Max`), then widen the total negative clamp beyond it so P and D can spike transiently and self-clear.
- The integral cap must be separate from the output clamp. Clamp only the output and the integrator still winds to that limit — the windup comes straight back.

**When to care:** hot idle enters high and droops to target, or the engine stalls on a load step after a long hot idle — before touching FF tables or overall PID gains.
