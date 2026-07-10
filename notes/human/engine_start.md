# Cranking and cold-start

> Digest of [engine_start.md](../engine_start.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** getting the engine lit and through the first 5–10 seconds — cranking airflow and enrichment, the handoff into the idle system, and why post-start stumbles are almost never fuel.

**The rules:**

- A post-start flare, sag, or stumble is an air/timing problem until proven otherwise. Do not reach for ASE — the restart runs open-loop (wideband blind ~25–33 s), so a "lean sag" can't even be measured during the event.
- `idleCrankingDC` is an airflow % (same unit as the active table; the "DC" name is historical) and it is **held open-loop through catch** — the idle PID stays gated for `idleControlAfterstartDelay`. Whatever you put in the hot bins is the airflow the engine flares on.
- Flare-fix lever order: hot cranking bins down (sets the level), afterstart delay down (held shorter), ignition lock time/restore down (frees the fast retard lever), then a small `idleAirFlowKD` for the residual swing. Kill the flare and the undershoot shrinks with it.
- Set each cranking CLT bin to the active-airflow % at the RPM you actually catch into — idle target **plus** the afterstart bump — with a small margin so the first correction is a gentle pull-down. That makes the 400 rpm handoff stepless.
- The post-start throttle slam (cranking TPS → lower idle TPS) creates an air deficit ASE cannot cover. Fix it with an elevated idle target for 5–10 s after start, not more fuel.
- Cranking enrichment pays the wall-film tax, not air starvation — big positive cold, small hot. Configure ASE as CLT × post-start **revolutions** (not time).
- Target ~60–80 kPa MAP while cranking; on big cams don't restrict the throttle to build MAP — defer to the airflow targets.

**Key numbers:** handoff at **400 rpm**; afterstart delay 5 ≈ 480 ms open-loop; ignition lock ×0.04 s/count; wideband blind ~25–33 s. Idle timing starting ranges: pump/stock 10–12°, pump/cammed 13–16°, ethanol/cammed 16–19°, ethanol/big cams 19–22° (base below MBT for reserve).

**When to care:** any start complaint — hard start, flare-then-sag, post-start stall — and whenever you set cranking airflow, ASE, or the afterstart ignition lock.
