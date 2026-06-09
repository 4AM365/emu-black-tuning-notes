# Idle RPM-hold stability — Supra measured results

Build-specific results behind [`notes/idle_rpm_cov_stability.md`](../../ai-analysis-skills/idle_rpm_cov_stability.md). The generic note holds the method (use RPM fluctuation not knock voltage; the sample-rate wall; metric definitions). Script: `supra/scripts/idle_stability.py`.

## Detection thresholds used here

- steady := TPS ≤ closed-throttle TPS + 1.5% (closed TPS auto-detected ≈ **4.5%**, NOT 0 — TPS offset) AND VSS ≤ 2 (if logged) AND |dRPM/dt| ≤ 300 rpm/s. Contiguous runs ≥ 4 s.
- Regime split: warm vs warmup by CLT (≥ 80 °C) when logged, else by `Idle target` vs the log's lowest steady target. `idle_v3` & `more_idle_returns` log only Charge temp (no CLT); `drive_wobble` logs CLT.

## Result (idle_log_v3_tune, 25 Hz, 268 s steady; targets 1200 & 1250 — "warmest-in-log", not thermally hot: no CLT, charge temp only 30→62 °C)

| view | bias | RMS err | std | ±25 % | ±50 % | jitter | hunt |
|------|------|---------|-----|-------|-------|--------|------|
| overall | −7 | 40 rpm | 43 | 37 % | 79 % | 0.68 % | 0.59 Hz |
| @1200 tgt | +1 | 38 rpm | — | 39 % | 82 % | — | — |
| @1250 tgt | **−36** | 46 rpm | — | 30 % | 69 % | — | — |

**Read:**
- Average tracking is good (bias +1 at 1200) but scatter is ~3× OEM: std 43 vs OEM 10–15, only 79% within ±50 (OEM ~95%+). Almost all of it is the **0.59 Hz hunt** — jitter (fast/combustion) is only 0.68%. Fix = idle PID limit cycle, NOT combustion.
- At 1250 there's a **−36 rpm steady bias** (sits below target) — a real tracking offset at the higher setpoint, distinct from the hunt. Suggests idle-air feedforward/PID authority falls short at elevated warmup targets.
- Expected payoff: killing the 0.6 Hz hunt should pull std 43 → ~10–15 and ±50 coverage 79% → ~95%, into OEM territory without touching fueling.

## OEM yardstick (general, kept in the generic note too)

Steady warm idle holds ±20–50 rpm of target (std ~10–15 rpm, CoV ~1.5–2%, ~95%+ within ±50). COV-of-IMEP < 5% smooth, > 10% = perceived-roughness limit.

## Data-quality flags / next steps

- `more_idle_returns`: the "steady" 19.6 s sits **+186 rpm above target** (RMS 205) — post-return hangs, not controlled idle.
- `drive_wobble`: no steady idle (driving log) despite logging CLT.
- 100 Hz exports sharpen the hunting PSD (Nyquist 50 Hz); still won't give per-cycle combustion CoV.
