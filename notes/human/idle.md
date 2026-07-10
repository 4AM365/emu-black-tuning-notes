# Idle

> Digest of [idle.md](../idle.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** every EMU Black idle table — what it does, which direction to move it, and the two-PID architecture that decides which lever fixes which idle problem.

**The rules:**

- Two PIDs: ignition is the fast lever, airflow the slow one (it re-centers the ignition angle, not RPM). Knock down a high idle with retard, never an air purge — retard reverses in one cycle; a purge leaves the throttle shut for the next load step.
- Idle runs ~30% residual gas; cams and turbo backpressure push it toward the misfire cliff. No PID authority fixes combustion instability — raise the target, run slightly rich, add base timing, nail per-cylinder trim first.
- Feed-forward corrections (`idleCustomCorrection`, fan/AC comp) get roughly **half** the airflow change the engine needs; the PID eases in the rest. Under-correcting idles briefly high; over-correcting stalls.
- The MAP activation gate (`idleMinMapToActivate`) reads backwards until you see that engine braking pulls *deeper* vacuum than idle. Idle activates when MAP is **above** the gate. Set it just above worst-case engine-braking MAP and well below the idle-MAP floor (check cold fast-idle too). Too high → return-to-idle stall.
- `idleActiveAirflow` is indexed by idle **target**, which floors at the setpoint — its sub-idle rows are never read. Raising them does nothing for a return-to-idle dip; the VE table owns that.
- `idleArmedAirFlow` (the overrun glide) must stay above minimum useful airflow and match the active value at the bottom bin. Too low at the decel bins → overrun-to-idle stall; the rich spike in the log is the symptom, not the cause.
- `idleCrankingDC` is an airflow % (not a duty cycle) held open-loop through catch — it is the flare setpoint. Match it to the active-airflow value at target + afterstart bump, plus a small margin.
- Clamp the airflow-PID integral tighter than its total output, or windup returns. `KD`=0 plus the ~750 ms DBW lag gives one big under-damped swing on any large transient — a small KD is the brake.

**Key numbers:** cranking→active handoff at **400 rpm**; manifold time constant ~740 ms; DBW lag ~750 ms; engine braking ~13–17 kPa vs idle ~30–40 kPa; Airflow% ubyte tables decode ×0.5.

**When to care:** any idle complaint — stall, hunt, hot drift, return-to-idle bog — and before touching any idle airflow table, PID gain, or the actuator range (rescale everything together).
