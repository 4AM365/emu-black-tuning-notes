# Restart bounce with A/C on — 2026-10-02 (digest)

Canonical: [../log_2026-10-02_restartbounce.md](../log_2026-10-02_restartbounce.md).

**What this covers.** The idle hunt after a hot restart with the A/C requested from key-on, and how A/C engagement behaves at steady hot idle.

**The rules**
- The bounce was a relay loop, not PID instability. `acMinRPM` has no hysteresis, and when it trips it drops the clutch and the A/C custom airflow correction together. Both re-arm, and the clutch lands `acTimeToEngage` later on the overshoot, which drags RPM back through the gate.
- It was triggered by the clutch engaging during the Afterstart fall (PIDs off). It ended only when the airflow integral had built up enough to lift a trough above the gate.
- The kP 1.0 → 0.5 edit was the only gain change compared with the restart. kI was already 0.5 then. It makes the troughs shallower but doesn't remove the relay.
- The dip at a normal engagement is inherent: the torque arrives faster than the air. The feed-forward goes in before the clutch, so the controllers take back about 5 of the +16 before the load lands.
- The gate sits inside the normal engagement dip: 12 trips in this log, 5 of them on fresh engagements at standing idle. Raising it only helps above the idle target (no A/C at idle). Proposed: lower it to about 650.
- After-start inhibit: use a function, `Switch 1 is True AND Engine runtime > N` (N ≈ 8 s), as the A/C request, not ASE (ASE timing moves with every ASE edit and adds fuel). Gate the request rather than the clutch output, or the +16 custom correction comes in with no load. It fixes the restart trigger only.
- Engagement response: the airflow P term's late air is the overshoot. The engagement torque transient is bigger than the steady load, so the custom correction can't cover the dip. The derivative signal is clean at this transient (SNR ≈ 10), so a small KD is a fair test.

**Key numbers.** Restart troughs 530 / 755 / 758 / 798, then 870, which held. Steady engagements bottomed at 802–832 with kP 1.0 and 835–898 with kP 0.5 (n = 3), back on target in 1.5–2.6 s. Effective trip ≈ 815–840 logged RPM.

**When to care.** Any A/C-at-idle tuning, restarts with A/C on, or any change to `acMinRPM` / `acTimeToEngage` / the A/C custom airflow correction.
