# Idle RPM stability results

> Digest of [idle_rpm_stability_results.md](../idle_rpm_stability_results.md) — the dense note is canonical; if they disagree, it wins.

**Finding (log `idle_log_v3_tune`, 25 Hz, 268 s of steady idle):** average tracking is good — bias +1 rpm at the 1200 target — but scatter is ~3× OEM: std 43 rpm vs an OEM 10–15, with only 79% of samples inside ±50 rpm. Nearly all of it is a **0.59 Hz hunt**; fast combustion jitter is only 0.68%.

**So-what:** the fix is the idle PID limit cycle, not fueling or combustion. Killing the ~0.6 Hz hunt should pull std to ~10–15 rpm and ±50 coverage to ~95% — OEM territory — without touching fuel.

**Also:** a real −36 rpm steady bias at the 1250 warmup target, distinct from the hunt — feedforward/PID authority falls short at elevated targets. And the log wasn't thermally hot (charge temp 30–62 °C, no CLT channel).

**Data flags:** `more_idle_returns`' "steady" span sits +186 rpm above target — post-return hang, not controlled idle; `drive_wobble` has no steady idle at all. 100 Hz exports would sharpen the hunt PSD but still can't give per-cycle combustion CoV.
