# Mass-flow estimator quirk at idle

> Digest of [mass_flow_estimator_quirk.md](../mass_flow_estimator_quirk.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why the `Estimated mass airflow` channel is wildly wrong at idle on this cammed engine, and when you can trust it.

**The rules:**

- The channel reports **gross throttle flow, not net cylinder fill**. With 264° cams, overlap reversion at idle means most of what passes the throttle goes right back out — reported idle flow can be ~10× real combustion airflow (~60 g/s reported vs ~6 g/s true at 1200 rpm).
- Trust it at WOT / high load — validated against measured mass. Cruise is likely within ~5–10%. At idle, low load, or closed-throttle decel: never use it for fuel-mass math or VE validation.
- For idle physics, compute mass flow first-principles from MAP, charge temp, displacement, and the VE cell: ≈ **5.9 g/s** at 1200 rpm / MAP 35 kPa / VE 0.55. That's the anchor for TB-growth, pump-headroom, and injector minimum-PW checks.
- The idle VE cells are already calibrated for net effective fill on this cam — don't "correct" them from the estimator.
- Don't compare the idle channel value against compressor maps or MAF ranges either; those expect net flow.

**Key numbers:** ~5.9 g/s true idle mass flow vs ~60 g/s reported.

**When to care:** any idle-region math that needs a mass-flow number, or when the log channel looks impossibly high at idle — it's model output, ignore it there.
