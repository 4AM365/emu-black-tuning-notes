# What an idle log can and cannot tell you about the plant

> Digest of [idle_pid_identifiability.md](../idle_pid_identifiability.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why you cannot measure the engine from a closed-loop idle log by regression, which idle quantities *are* recoverable, and the one test that fixes the gap.

**The rules:**

- **Regression on a closed-loop idle log measures the ECU, not the engine.** The controller sets the input from the output, so least squares returns the inverse controller. The tell is a **negative** ignition coefficient — advance slowing the motor. Three different windows all produced one.
- **Ignition authority is structurally unrecoverable.** With a proportional inner loop the correction is an exact linear function of RPM error (measured r = −0.93), so spark torque is perfectly aliased onto the hold curve.
- **The rails are the only exogenous spark in a normal log** — there the output is the clamp and has stopped answering RPM. But separating spark from air needs *two* rail levels, and a typical log has minutes at the retard rail and a handful of samples at the advance rail.
- **Both repo figures for "torque per degree of idle timing" are inferences, not measurements**, and they disagree by ~9×. Don't build a decision on either.
- **Read controller constants from the tune, then cross-check against the log's monitor channels** — never fit them. `Monitored P term` ÷ `Idle ignition correction` returns `idleAirFlowKP` exactly; the I-term and total-correction ranges reveal whether the integral limit or the output limit is the one actually binding.
- **Fit the air path by output error**, not one-step residuals: replay logged inputs, free-run the speed state over multi-second windows, score the trajectory. That stays consistent under feedback.
- **Quote the total air lag, never the split.** Hundreds of (delay, fill) pairs fit equally well.
- **Mask clamped samples before regressing any PID gain.** This is what resolved `idleIgnitionKP` reading 0.0432 on some logs and 0.0498 on others — the low ones included railed samples, where output is the clamp and no longer tracks the gain. One gain, measured two ways, one biased.

**The test that settles it:** warm idle, neutral, A/C off — zero `idleIgnitionKP`/`KI`/`KD` so the inner loop can't respond, step the idle ignition target ±3°, log RPM. Spark authority is the initial RPM slope ÷ the step. Ten seconds of open-loop data closes what three regressions could not, and it settles the hold-curve slope at the same time (the two trade off directly).

**When to care:** before trusting any log-derived claim about how much of an entry dip the ignition channel could arrest, before quoting airflow-required-per-rpm, and any time a fit returns a coefficient whose *sign* is impossible — that is feedback, not noise.
