# What an idle log can and cannot tell you about the plant

A structural limit on log-based analysis of the EMU two-PID idle architecture
([P2](idle.md#p2-the-emu-black-two-pid-idle-architecture)), found while building
a trajectory simulator of the cascade
(`../emu-idle-sim`, see its `docs/MODEL.md`). It explains a discrepancy that has
been sitting in these notes and sets a rule for future log work.

## The rule

**You cannot identify the plant from closed-loop idle data by regression.** The
controller makes the input a function of the output, so ordinary least squares
recovers the *inverse controller* rather than the engine. Every naive fit on an
idle log is measuring the ECU, not the motor.

The failure is not subtle. Fitting `dN/dt` against airflow, RPM and ignition
correction over hot ACTIVE samples returns a **negative** coefficient on
ignition — advance slowing the engine. Restricting to desaturation events, where
delivered air is frozen, still returns negative. Restricting to the first 0.4 s
after activation, before the air lag can deliver anything, returns negative and
nine times larger. The magnitudes are the *controller's* gain being read back,
not noise.

## Why ignition specifically is unrecoverable

With a proportional inner loop,

```
ign_corr = -idleIgnitionKP * (RPM - target)
```

is an **exact linear function of the state**. Spark torque is therefore
perfectly collinear with the speed error, and no amount of data separates it
from the hold curve. Measured collinearity on the reference build: r = −0.93
between `d(Idle ignition correction)` and `d(RPM)` even in the pre-air-lag
window.

The only genuinely exogenous spark in a normal log is **at the rails**, where the
output is the clamp and has stopped responding to RPM. That is why railed
stretches are the analytically valuable ones — but separating spark from air
needs *two* rail levels to difference against. A typical hot drive log has
minutes at the retard rail and a handful of samples at the advance rail, so
there is one level and no separation.

**Consequence for these notes:** any figure for "how much torque a degree of
idle timing is worth", derived from a normal log, is an inference and not a
measurement. Two such figures live in this repo — the ignition rail absorbing
about 10 airflow points over its 17° range, and a ~7° desaturation producing a
~95 rpm step — and they disagree by about a factor of nine. Neither is wrong as
an observation; they are simply not measurements of the same thing, and this
data cannot arbitrate.

## The test that settles it

Ten seconds of open-loop data closes what three regressions cannot. At stable
warm idle, in neutral, A/C off:

1. Zero `idleIgnitionKP`, `idleIgnitionKI`, `idleIgnitionKD` so the inner loop
   cannot respond.
2. Step the idle ignition target by ±3°.
3. Log RPM.

Spark authority is the initial slope of the RPM response divided by the step
size. Do it before trusting any conclusion that rests on ignition authority —
including how much of the entry dip the ignition channel could ever arrest.

The same test also settles the **hold curve slope** (airflow required per rpm),
because the two trade off directly: an assumed spark authority and a fitted hold
curve move together, and the notes' creep-phase figure and the simulator's
free-run fit differ by about 2× for exactly this reason.

## What *is* identifiable from a normal log

- **Every controller constant**, and they should be *read* from the tune XML and
  then cross-checked against the log's own monitor channels rather than fitted.
  On the reference build every cross-check agreed: `Monitored P term` divided by
  `Idle ignition correction` returns `idleAirFlowKP` exactly; `Monitored I term`
  and the total correction reveal which of the integral limit and the output
  limit is actually binding; `median(Ignition Angle − Idle ignition correction)`
  returns the idle ignition target; the absolute angle range returns the
  min/max-torque-angle clamps.
- **The air path** (gain, hold curve, total lag) by **output error** — replaying
  logged inputs and free-running the speed state over multi-second windows,
  scoring the trajectory rather than one-step residuals. This is consistent under
  feedback where equation-error regression is not.
- **The total air lag**, but *not* its split between transport delay and plenum
  fill: hundreds of `(delay, tau)` pairs fit equally well. Quote the sum.

## Correction this produced

`idleIgnitionKP` is quoted in these notes both as 0.0432 and 0.0498 °/rpm, read
off different logs. The low figures are **rail-contaminated**: regressing the
correction on RPM error over a wide error window includes samples where the
output is pinned to the min/max-torque-angle clamp and no longer follows the
gain, which flattens the slope. Restricted to the unrailed band (|error| below
about 80 rpm) the regression converges on the tune's decoded value. This is not
two calibrations — it is one gain measured two ways, one of them biased.

**Method worth reusing:** before regressing any PID gain out of a log, mask out
every sample where that loop's output is on a clamp.

## Related notes

- [idle.md](idle.md) — P2 architecture, the hang/step/creep anatomy
- [return_to_idle_bog.md](return_to_idle_bog.md) — the failure this modelling served
- [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md) — integral limits vs output limits
