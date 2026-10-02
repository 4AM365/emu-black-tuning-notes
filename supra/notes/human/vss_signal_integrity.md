# Speed signal integrity — digest

*Digest of [`../vss_signal_integrity.md`](../vss_signal_integrity.md). The canonical note wins.*

**09-19 re-check (2026-09-28):** still faulty. It drops to 0 in one sample from up to 117 km/h (8×) and has a 270 Hz phantom. Those are step functions, which points at the wiring.

## What this covers

The Supra's VSS input is noisy, and that noise — not any idle tuning decision — is what makes
`Idle force open loop` flicker on and off while driving. Confirmed from `omg.csv` (2026-08-24),
the first log carrying both a speed channel and the `Idle force open loop` flag.

## Status 2026-08-30 — NOT fixed by the ground rewire
The clutch switch was moved from chassis ground to sensor ground 2026-08-29, but the speed signal
**still glitches** (owner, 2026-08-30 drive). The VSS pin is a *digital* input, not one of the
pre-"P" switch inputs, so that mechanism never covered it. The clutch-circuit gating stands
(**12.9/min pressed vs 1.0/min released, 13×**, state-gated not edge-gated) — the coupling path
into the VSS input is still open. Interim: `idleOpenLoopOverVss` = 400 km/h (force disabled so
noise can't wipe the PIDs); VSS idle-up kept above ~5 km/h. Low-threshold decoupling gate resumes
once the channel is clean.

**You cannot filter it away.** The artifact is a coherent 0.5–0.7 s burst that ramps and decays
like real acceleration (0.25 → 81.75 → 5 km/h, parked), not a spike: a 5-sample median filter
removes **zero** samples. Any window long enough to swallow it delays every real crossing by the
same 0.7 s. It's a pin fix, not a software fix.

## The rules

- **Fix the speed sensor before tuning anything gated on speed.** The idle open-loop gate, the
  VSS idle-target increase, the gear estimator, the fan VSS cutoff, rev-match, flat-shift and
  launch all read the same input. Filtering is already configured and does not catch it.
- **The gate is cleared by `Gear unknown`, not by a real neutral.** The ratio-based gear estimator
  loses lock constantly, and "unknown" satisfies *Neutral enables closed loop* — so the gate
  toggles at the estimator's flicker rate instead of at road-speed crossings.
- **Every toggle wipes both idle PID integrals** (EMU help: the force resets integral terms), so
  the loop restarts from zero and re-pays the travel-debt each time.
- **Don't read A/C idle-up from `omg.xml.emub3` for this log** — the log shows a live +500 the
  export's `idleACRPMIncrease` doesn't. And the first 788 s contain live tune edits; use t > 839 s.

## Key numbers

36 impossible speed steps (>200 km/h/s); phantom **81.75** and **46.25 km/h** at a dead stop.
`Gear unknown` asserts **214×**, median **0.20 s**. `Idle force open loop` asserts **23× / 35.2 s**,
median **0.20 s**, 17 of them under 0.5 s. Above the threshold with the clutch out, gear-unknown
samples have the force cleared **480 of 488** times. **15 of 23** assertions hit while idle was
ACTIVE, discarding a median **−3.0°** of ignition correction (range −8.0 … +17.0°) and **−3.06 %**
of air correction (−5.69 … +10.56 %). Three assertions happened at a genuine standstill.

## When to care

Any time idle behaves oddly while rolling — a hang on decel, a bump at 45–60 km/h, timing that
steps rather than glides — or when a stopped idle sags for no visible reason. Also before trusting
any measurement conditioned on speed or gear.
