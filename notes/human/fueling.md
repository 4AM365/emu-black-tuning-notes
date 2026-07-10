# Fueling

> Digest of [fueling.md](../fueling.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how the EMU fuel model actually works (VE is the dose, lambda target is not a multiplier), how to correct VE from logs, and the flex-blend, per-cylinder-trim, and fuel-pressure rules.

**The rules:**

- `veTable` is the fuel dose and carries mixture itself; `lambdaTable` is only a tuning reference and the closed-loop STFT target. Changing the lambda target alone changes nothing open-loop — real mixture moves happen in VE, enrichment added by hand.
- Correct steady closed-loop cells from `Short term trim` (the wideband already tracks target); correct open-loop/accel cells from lambda error directly, filtered to rising-RPM, TPS > 10% samples. Apply the same factor to both VE tables.
- STFT is slow (~3 s to saturate) — never read needed enrichment from it during transients. The wideband λ/λ_target already carries the full open-loop deficit there.
- Since 2026-06-29 the car runs a **pure VE map**: injectors characterized, fuel-pressure comp active. `veTable2` should now converge toward `veTable` — the old "ethanol table lower is expected" reasoning no longer holds here.
- Don't over-enrich the global target to protect the lean rear cylinders — per-cylinder trim owns maldistribution. Global WOT richness is purely an EGT-margin choice. An EGT delta that shrinks with load is real maldistribution; a load-constant delta is sensor offset.
- Base fuel pressure is the **engine-off, pump-primed** differential, and it forms a matched pair with `injectorsSize` (flow scales √ΔP). Never edit one without the other; enabling active pressure correction shifts the whole map's fueling — re-verify STFT before driving.
- When smoothing VE, preserve the idle knee: smooth the *correction* (delta overlay), never the absolute surface — a global polynomial rounds off a real nonlinearity and invites idle surge.
- Accel enrichment is for transient spikes only, never a patch for steady-state VE error. The decel fuel correction can fire during return-to-idle recovery and trim fuel the wrong way — raise its RPM floor.

**Key numbers:** `veTable` is u12, scale 0.1; boost lambda rolloff is ~linear in MAP, so spend bins at the MBT→protection knee (~130 kPa); high-boost pump λ ~0.72–0.80; knock benefit of richness saturates ~λ 0.76–0.78; clamp log corrections ±15% per pass.

**When to care:** before any VE, lambda-target, blend, trim, or fuel-pressure edit — and after any injector or regulator change, which re-anchors the whole model.
