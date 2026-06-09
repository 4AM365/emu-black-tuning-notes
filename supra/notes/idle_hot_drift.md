# Hot-idle drift (windup/purge/stall) — Supra measured specifics

Build-specific numbers behind [`notes/idle_hot_drift_pid_windup.md`](../../notes/idle_hot_drift_pid_windup.md). The generic note holds the two-PID architecture and the windup/purge/stall mechanism; this file holds the measured values. Diagnosed on `new_fuel_strategy` (machine-smoothed / v3), hot idle CLT ≥ 95 °C. Scripts: `supra/scripts/idle_drift_attribution.py`, `supra/scripts/idle_tracking.py`.

## Observed behaviour

On a hot stop the engine enters idle high (**~+90 RPM over a 1200 target**) and walks down to target over ~30 s.

| term | start → end | reads |
|------|-------------|-------|
| RPM | 1289 → ~1200 | walks down ~30 s |
| Idle air % (total) | 32.0 → 29.5% | bleeding off |
| Idle air % = base − PID; **PID corr** | **−4.0 → −4.0** | pinned at its −4% clamp, 91% of hot idle |
| Charge temp / IAT | +4.7 / +4.8 °C | rising (heat soak) |
| Lambda 1 | 0.90 → 1.00 | leans (secondary torque loss) |

The walk-down is done by the feed-forward charge-temp air bleed, NOT the PID. The airflow PID is saturated against its **−4% negative clamp** the whole time (full-log range **−4.0 … +2.19**, so −4.0 is the hard floor).

## Fix values (this build)

- **Cap the airflow integral independently at ~−4%** (anti-windup). P and D are windup-free, safe to give room.
- **Widen total negative correction to ~−10%** so P/D can spike transiently for a fast knockdown, then self-clear.
- The integral cap must be **independent** of the total-output clamp (EMU supports a separate integral limit).
- Logged idle ignition correction only reached **~−4 to −7.5°**, so there is likely headroom in the **Min torque ign. angle** table to let ignition do more of the fast knockdown (stall-safe — reversible, never shuts the throttle).
