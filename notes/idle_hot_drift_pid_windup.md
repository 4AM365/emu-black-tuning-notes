# Hot-idle drift, the two-PID idle architecture, and the windup/purge/stall fix

Diagnosed on `new_fuel_strategy` (machine-smoothed / v3), hot idle CLT ≥ 95 °C.
Scripts: `supra/scripts/idle_drift_attribution.py`, `supra/scripts/idle_tracking.py`.

## Observed behaviour

On a hot stop the engine enters idle high (~+90 RPM over a 1200 target) and walks down to
target over ~30 s. Attribution over the stretch:

| term | start → end | reads |
|------|-------------|-------|
| RPM | 1289 → ~1200 | walks down ~30 s |
| Idle air % (total) | 32.0 → 29.5% | **bleeding off** |
| Idle air % = base − PID; **PID corr** | **−4.0 → −4.0** | **pinned at its −4% clamp, 91% of hot idle** |
| Charge temp / IAT | +4.7 / +4.8 °C | rising (heat soak) |
| Lambda 1 | 0.90 → 1.00 | leans (secondary torque loss) |

**The walk-down is done by the feed-forward charge-temp air bleed, NOT the PID.** The
airflow PID is saturated against its −4% negative clamp the whole time and contributes
nothing dynamic. (PID full-log range −4.0 … +2.19, so −4.0 is the hard floor.)

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
fill-lag. Logged idle ign correction only reached ~−4 to −7.5°, so there is likely headroom in
the **Min torque ign. angle** table to let ignition do more of the fast knockdown.

## The windup/purge/stall failure mode and the fix

**Failure (observed historically):** negative airflow **integral** winds up → ECU purges a lot
of (hot) charge air → DBW forced toward shut → the next load step / required air-return can't
happen fast enough → **stall**.

**Fix (confirmed implementable — EMU allows an independent integral limit):**
- **Cap the integral independently at ~−4%.** P and D are windup-free (functions of current
  error, self-clearing the instant RPM returns), so they're safe to give room; the integral is
  the part that accumulates, lags, and leaves the throttle shut. Capping it bounds worst-case
  stuck-shut to today's level.
- **Widen total negative correction to ~−10%** so P/D can spike transiently for a fast
  knockdown of the high entry, then self-clear.
- **Critical condition:** the integral cap must be *independent* of the total-output clamp. If
  only the output is clamped, the integrator can still wind to −10% and the windup returns.
  (Will confirmed EMU supports a separate integral limit, so this is directly configurable.)

## Recommended division of labour (all consistent with the TB-lag constraint)

1. **FF stays restricted** — no premature sag.
2. **Ignition PID = fast knockdown** of the high entry (use Min torque ign-angle headroom) —
   stall-safe because it's reversible and never shuts the throttle.
3. **Airflow PID = slow trim only**, integral capped ~−4% (anti-windup), total ~−10% for
   transient P/D headroom.

This gives the term we rely on (closed loop) the authority to own the late walk-down without
reintroducing the purge-stall risk, and shifts the fast work onto the safest actuator (timing).
