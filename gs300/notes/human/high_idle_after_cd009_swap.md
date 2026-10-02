# 4000 rpm idle after the CD009 swap — the short version

> **⛔ NOT THE SUPRA.** GS300 / Aristo / CD009. Never carry values, pins or conclusions between
> this car and the Supra notes in either direction; never load `supra-specs` for it.

**What this covers.** Why the car sits at ~4000 rpm right after start now that the automatic is
gone. Canonical note: [`../high_idle_after_cd009_swap.md`](../high_idle_after_cd009_swap.md) — that one wins.

**The rules.**
- **Don't tune around it.** It's the Aristo ECU's idle controller failing on inputs that left with
  the gearbox, and that ECU is being deleted. Fixing it means the EMU taking the throttle.
- **Don't drive it.** 4000 rpm no-load with a manual gearbox. If the throttle clutch has dropped,
  the pedal will not bring the revs down — nothing is holding the blade closed.
- **The likely mechanism is lost authority, not a high command.** The ETCS-i clutch must be
  energised for the motor to move the blade at all. Drop the clutch after the post-start warm-up
  airflow is already commanded, and the ECU can't take it back.
- Two things are on a clock and die with the ECU: **the OEM trouble codes** and **a BEAN capture**.

**Key numbers.**
- Idle inputs now open circuit: `SP2±` B3-5/11 vehicle speed (wilbo666 says outright it feeds idle
  control), `N` B2-13, the six other gear-position pins, `NCO±`, `OIL`, and every shift and
  pressure solenoid on plug B3.
- Not lookup-able: RM718U has **no DIAGNOSTICS section**, so the real ETCS-i fail-safe behaviour
  isn't in anything we hold. The hypotheses are reasoned, not sourced.

**The twenty-minute test.** Key on, engine off — does the throttle self-sweep? Does the blade
follow the pedal? Then at the high idle, read `VTA`/`VTA2` and check whether `CL+`/`CL-` is
energised. Those four readings split the field.

**Free bonus.** The car is currently a faulted Aristo ECU, which is exactly the experiment in
[`../position_keep_aristo_ecu_for_cluster.md`](../position_keep_aristo_ecu_for_cluster.md) §5.
**Look at the dash now** — temp gauge reading? charge/oil lamps sane? HVAC in auto? That answers
the whole cluster strategy for the cost of one look.

**When to care.** Right now, and before anything else on the car changes.

**The decision (2026-09-08).** Move DBW to the EMU now — but **unplug the throttle from the OEM
ECU, don't remove the ECU**. Same work, and the cluster question stays open, the BEAN capture stays
available, and it doubles as the disconnection test. Three preconditions: the EMU needs its **own
main relay and permanent 12 V** (don't hang the throttle controller off `M-REL`), the EMU must
drive `CL+`/`CL-` with `+BM` on its 15 A fuse (no clutch = no throttle, same symptom, new ECU), and
Phase 0.4 must confirm what the EMU already owns. Wire per **v3**: `VTA` → TPS input, `VPA` → free
analog input. Full reasoning in §8 of the canonical note.

**Cable + IACV instead of DBW?** Corrected 2026-09-08 — the "opener" evidence in an earlier
version of this note was from the **wrong engine's throttle body** (GS300 2JZ-GE, not the Aristo
unit actually in the car) and has been struck.

On its own footing: every **Aristo-specific** document describes `VPA`/`VPA2` as a pedal position
**sensor**, feeding the ECU, with the blade moved by the `M+`/`M-` motor through the `CL+`/`CL-`
clutch. No cable is mentioned anywhere in wilbo666's notes or the pinout text — the standard
signature of a pure fly-by-wire throttle. Will says the physical part has a cable with the motor
as an electric "adder." **Those two don't agree — check by eye before wiring anything:** motor and
ECU both unplugged, work the pedal/cable by hand, watch the throttle shaft. Moves → cable is real,
wire the two-wire IACV per §9 (EMU idle strategy set to PWM solenoid, not DBW — simpler, no DBW
calibration, no check-sensor tolerance map). Doesn't move → the earlier §8 plan stands: EMU drives
the existing motor and clutch.
