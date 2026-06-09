# Hot-idle drift, the two-PID idle architecture, and the windup/purge/stall fix

A hot-soak idle drift pattern and the EMU two-PID architecture that explains the right fix for it.

> **Car-specific values live in the build working docs**, not here. For the reference build's measured hot-drift attribution and the specific PID/integral/ignition clamp values, see [`supra/notes/idle_hot_drift.md`](../supra/notes/idle_hot_drift.md) (and [`airflow_actuator.md`](../supra/notes/airflow_actuator.md) for the PID limit/custom-correction tables). This note is intentionally car-agnostic.

## Observed behaviour

On a hot stop the engine enters idle high (some tens of RPM over target) and walks down to
target over roughly half a minute. Attribution over the stretch:

| term | trend | reads |
|------|-------|-------|
| RPM | high → target | walks down over ~30 s |
| Idle air % (total) | falling | **bleeding off** |
| Idle air % = base − PID; **PID corr** | **pinned at its negative clamp** | contributes nothing dynamic for most of hot idle |
| Charge temp / IAT | rising | heat soak |
| Lambda 1 | leaning toward stoich | secondary torque loss |

**The walk-down is done by the feed-forward charge-temp air bleed, NOT the PID.** The
airflow PID is saturated against its negative clamp the whole time and contributes
nothing dynamic. (See the build's working doc for this car's measured PID range and clamp.)

## Why the FF is deliberately restricted (design intent — do NOT "fix" by adding FF)

The charge-temp idle-air FF is **intentionally limited** because **throttle-body metal temp
lags CLT significantly**. An aggressive FF would pull air out on the CLT/charge-temp schedule
*before the TB has actually heat-soaked*, sagging idle prematurely. So FF stays gentle and the
PID is meant to own the late walk-down. The earlier "add more FF / reduce it" reads were both
wrong: keep FF restricted.

## The EMU two-PID idle architecture (the key to the right lever)

EMU runs **two cooperating idle PIDs** (Idle help, ~line 181-183):
1. **Ignition PID** — fast RPM lever; trims torque via timing within Min/Max torque ign angle.
2. **Airflow PID** — does **not** act on RPM error; it acts on the error between *current
   ignition angle and the Target ignition angle*, slowly trimming air to re-center the ignition
   PID so the two "cooperate" instead of fighting.

Consequence: the **stall-safe** way to knock down a high hot idle is **ignition retard**, not
air. Timing is reversible in one combustion cycle — no air purge, no throttle closing, no
fill-lag. If logged idle ign correction is using only part of its allowed swing, there is likely
headroom in the **Min torque ign. angle** table to let ignition do more of the fast knockdown.

## The windup/purge/stall failure mode and the fix

**Failure (observed historically):** negative airflow **integral** winds up → ECU purges a lot
of (hot) charge air → DBW forced toward shut → the next load step / required air-return can't
happen fast enough → **stall**.

**Fix (EMU allows an independent integral limit):**
- **Cap the integral independently**, tight. P and D are windup-free (functions of current
  error, self-clearing the instant RPM returns), so they're safe to give room; the integral is
  the part that accumulates, lags, and leaves the throttle shut. Capping it bounds worst-case
  stuck-shut to the current level.
- **Widen the total negative correction** beyond the integral cap so P/D can spike transiently
  for a fast knockdown of the high entry, then self-clear.
- **Critical condition:** the integral cap must be *independent* of the total-output clamp. If
  only the output is clamped, the integrator can still wind all the way to the output limit and
  the windup returns. EMU supports a separate integral limit (`idleAirFlowIntegralLimitMin/Max`),
  so this is directly configurable. See the build's working doc for this car's chosen limit values.

## Recommended division of labour (all consistent with the TB-lag constraint)

1. **FF stays restricted** — no premature sag.
2. **Ignition PID = fast knockdown** of the high entry (use Min torque ign-angle headroom) —
   stall-safe because it's reversible and never shuts the throttle.
3. **Airflow PID = slow trim only**, integral capped tight (anti-windup), total negative output
   wider than the integral cap for transient P/D headroom.

This gives the term we rely on (closed loop) the authority to own the late walk-down without
reintroducing the purge-stall risk, and shifts the fast work onto the safest actuator (timing).
