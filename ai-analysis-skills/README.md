# AI / data-analysis skills

Methods for analyzing EMU Black logs and tune tables with scripts / machine techniques — the
"how to read the data" companions to the feature pages in [`../notes/`](../notes/). These are
**techniques**, not EMU software pages: how to derive a correction from a log, how to smooth a
table without destroying real features, and how to score one map against another.

## Methods

| Note | What it does |
|------|--------------|
| [ve_correction_from_log.md](ve_correction_from_log.md) | Correct `veTable`/`veTable2` from a closed-loop log: `new_VE = old_VE × (1+STFT/100) × (λ_act/λ_tgt)`, steady-closed-loop mask, bilinear accumulate, apply to both flex tables. |
| [ve_correctness_from_log_method.md](ve_correctness_from_log_method.md) | Judge whether the fuel tables are right: STFT in steady cells, lambda error in accel cells, coverage map for what's unverified. |
| [ve_idle_region_nonlinearity.md](ve_idle_region_nonlinearity.md) | **Delta-overlay** smoothing — smooth the correction, not absolute VE — so the idle knee, cam inflection, and high-load plateau survive. |
| [ve_vs_map_at_constant_rpm.md](ve_vs_map_at_constant_rpm.md) | Shape unmapped boost columns: copy the RPM resonance shape across MAP, roll VE flat-to-down into boost, verify with the `veTable × λ_target` air-VE proxy. |
| [lambda_tracking_map_smoothing.md](lambda_tracking_map_smoothing.md) | Score a map by lambda-tracking spread (machine-smoothed vs hand-built); bias is a global offset, spread is the smoothness signal. |
| [knock_voltage_cov_combustion_stability.md](knock_voltage_cov_combustion_stability.md) | Combustion-CoV proxy from knock-voltage scatter on no-knock cycles — detrend within fine cells, restrict to transients. |
| [idle_rpm_cov_stability.md](idle_rpm_cov_stability.md) | Idle quality from crank-speed fluctuation (tracking vs target + hunt/jitter); the sample-rate wall that blocks true per-cycle CoV. |

## Related scripts & skills (not moved here)

The executable implementations live with the tooling, not in this notes folder:

- Skill [`emu-black-ve-smooth`](../skills/emu-black-ve-smooth/SKILL.md) — anchor-weighted VE smoothing
- Skill [`emu-black-tune-review`](../skills/emu-black-tune-review/SKILL.md) — literature-cited tune audit
- Skill [`emu-black-vvti-street-tune`](../skills/emu-black-vvti-street-tune/SKILL.md) — MAP-proxy VVT sweep analysis
- Reference-build pipelines: `../supra/scripts/` and `../supra/tunes/ve_*.py`

Car-specific measured results live in [`../supra/notes/`](../supra/notes/) (e.g. `lambda_tracking_results.md`, `knock_chatter_cov_results.md`, `idle_rpm_stability_results.md`).
