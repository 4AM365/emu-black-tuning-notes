# Throttle response tuning

> Digest of [throttle_feel.md](../throttle_feel.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** what actually sets throttle feel — pedal-to-plate mapping, rate limit, boost reference — plus the trouble spots: creep, lift-off, and the idle-to-driving handoff.

**The rules:**

- The DBW characteristic map matters more than the rate limit. Parking-lot jerkiness: scoop the low-pedal region and bump the upper region so downshift blips still land. Creep behavior lives in the low-PPS/low-RPM quadrant — the RPM axis gives implicit gear awareness.
- Rate limit: a moderate universal value, *reduced* at high speed for gentler lift-off. Setting it low enough to feel at low speed fights the idle controller's own plate movements — that path is a dead end.
- Lift-off at high RPM loads rods in tension (fuel cut, crank dragging pistons down). The real mitigations are overrun strategy — minimum RPM, hysteresis, partial cut, or ignition cut instead of fuel cut. A slower closing rate only delays the onset.
- Prefer boost reference measured pre-throttle vs MAP: build plenum pressure early, meter power with the plate. A MAP-based characteristic risks circular logic — a gentle map at low MAP never opens enough to build MAP.
- Parachute lift-off feel: hold armed-state airflow at high RPM with the pedal released, trading away some engine braking. EMU has no PPS-rate-aware closing rates, so armed state is the workaround; decel ignition retard is the secondary softener.
- Decel fuel correction can trim fuel the wrong way at low RPM during idle recovery — raise its RPM floor so it can't fire there.
- At idle exit, the airflow PID I-term, the idle ignition correction, and the source switch all release at once — a wound-negative PID dumps a TPS-plus-timing step (the tip-in bump). Keep the high-target `idleActiveAirflow` rows accurate and re-derive the blend point whenever you rescale that table.

**Key numbers:** rate limit range 0–1300°/s, plus a 125°/s RPM-referenced adder on top.

**When to care:** parking-lot bucking, harsh lift-off, a bump on tip-in from idle, or any rework of the DBW characteristic or blend point.
