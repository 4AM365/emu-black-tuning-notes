# Position paper — keep the Aristo ECU as a cluster driver, give DBW to the EMU?

> **⛔ NOT THE SUPRA.** Josh Napier's GS300 (JZS160) / JDM Aristo (JZS161) 2JZ-GTE VVT-i / CD009.
> Never carry values, pins, hardware or conclusions between this car and the Supra notes in either
> direction, and never load `supra-specs` for it. Full caveat in [`my_car.md`](my_car.md).

Written 2026-09-08. Companion to [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md).

**The proposal.** Leave the OEM Aristo ECU in the car so the instrument cluster and HVAC keep
their multiplex data. Move drive-by-wire control to the EMU Black. Wire the throttle and pedal
position sensors to **both** ECUs so each can see throttle state.

---

## Position, up front

**The idea is half right, and the good half is very good.**

Keeping the Aristo ECU as a BEAN node solves the hardest problem in
[`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) §8 for free. That section's
blocker is not the protocol — it is the **message dictionary**: which `DST-ID`/`MES-ID` carries
coolant temperature, which bit is the charge lamp. Toyota never published it and it is per-model.
The Aristo ECU already knows it. Using Toyota's own hardware as the gateway sidesteps a
reverse-engineering project entirely. That is a genuinely good instinct.

**The sensor-sharing half buys nothing and costs plenty, and it is separable from the good half.**
Drop it.

---

## 1. The Aristo ECU will fault whatever you do with the sensors

This is the part that undoes the sharing rationale.

ETCS-i is a **closed-loop position controller**. The ECU drives `M+`/`M-` (B1-8/7) as a PWM
H-bridge, energises the `CL+`/`CL-` clutch (B1-20/19) — wilbo666 is explicit that *"the ETCS-i
clutch must be engaged for the electric motor to be able to open or close the throttle"* — and
watches `VTA`/`VTA2` to confirm the blade went where it was told.

Take the motor and clutch away and the ECU is in fault the moment it powers up. It sees an open
circuit on its motor driver. Then it sees the blade moving to positions it never commanded. Both
are unambiguous ETCS-i faults on any Toyota of this era.

So: **sharing the position sensors does not prevent the fault.** It gives a faulted ECU higher
quality data about a throttle it cannot move. That is the whole return on the sharing work.

*Unverified, and it matters:* what a JZS161 ECU actually does in that state is **not documented in
anything we hold**. RM718U is missing its DIAGNOSTICS section — the ECM inspection procedure points
at page DI-20 and that page is not in our copy — and EWD356U describes fail-safe behaviour only
for the moon roof and the ABS/TRAC/VSC ECU, never for the throttle. Do not assume benign
degradation. Test it (§5).

## 2. What sensor sharing actually costs

| Problem | Why it bites |
|---|---|
| **Two 5 V supplies, one sensor** | `VC` B2-2 is the Aristo's regulated 5 V, and wilbo666 says it feeds *"the throttle position sensor, accelerator pedal position sensor and the MAP sensor."* The EMU has its own 5 V rail. You cannot parallel two regulators onto one sensor — so one ECU must supply and the other must simply listen |
| **…which forces a shared ground reference** | the listening ECU has to reference the supplying ECU's `E2` sensor ground. Any offset between the two ECUs' grounds appears directly as a throttle-position error on whichever one is listening. That error lands on **safety-critical DBW feedback** |
| **Input bias networks** | a Toyota ECU biases its analog inputs so it can detect opens and shorts. Those networks sit in parallel with the EMU's input and shift the voltage the EMU reads. The shift is not guaranteed constant across the sweep, so it is not a single calibration offset you can dial out |
| **A faulted ECU wired to your throttle feedback** | this is the real objection. A browning-out, resetting or fault-latching Aristo ECU now has an electrical path into the sensors the EMU's DBW safety logic depends on. You have coupled an unpredictable device to the one subsystem that must never behave unpredictably |

None of these is exotic. All of them are avoidable, because **none of them is necessary** (§4).

## 3. What the prize actually is

Yes — the only reason to keep it is the cluster and HVAC. So it is worth being precise about how
much that is worth. From [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md)
§§2–3, everything the Aristo ECU puts on the bus:

| Lost without it | Can it be replaced discretely? |
|---|---|
| **Water temperature gauge** | **No.** There is no temperature sender in the car and no analog input behind the needle |
| **Charge / alternator light** | **No.** The alternator `L` terminal goes to the ECM, not to the lamp (EWD356U p. 82) |
| **Low oil pressure light** | **No.** Switch to ECM, lamp behind the meter CPU |
| **Oil level light** | **No.** Same |
| Oil temperature | no, and nobody will miss it |
| A/T gear position indicator | already dead — the car is a CD009 |
| **HVAC engine data** | no. Degraded auto mode. The compressor clutch is a discrete `ACMG` line, so A/C still *works* |

**Correction to an earlier draft of this section.** The first version of the dependency note said
the three warning lamps were "one wire each." **That was wrong.** The GS300 combination meter has
its **own CPU** (labelled on EWD356U pp. 90 and 92) and paints those lamps and the temperature gauge
from BEAN messages. There are no terminals behind them — see
[`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) §2a.

**This raises the prize substantially.** It is not "one gauge you could replace anyway." It is
**the temperature gauge and three warning lamps, none of which can be restored by any amount of
wiring**, plus HVAC auto mode. The alternatives are separate aftermarket gauges, or opening the
cluster. That makes keeping the Aristo ECU — or building a gateway — the *only* route to a
factory-looking dash, and it moves this from a curiosity to the main event.

## 4. What keeping it costs, before any sensor sharing

- **The immobiliser stays in the car.** Will's stated goal is to delete it. If the ECU is the
  **89666-30180** the immobiliser is *inside* the ECU and gates the EFI main relay through `M-REL`
  — EWD356U p. 170 shows the identical scheme on the GS300 side. Keeping the ECU means keeping the
  key amplifier, coil and transponder satisfied, or finding out the hard way whether a
  immobiliser-blocked ECU still transmits.
- **Permanent MIL.** `W` F60-6 is grounded by the ECU on fault. It will be on forever unless that
  wire is cut — at which point you have no check-engine lamp for the EMU either, so it needs
  rehoming to an EMU output regardless.
- **Outputs that must be severed.** The Aristo ECU must not keep driving `M-REL` F60-10, `FPC`
  F60-5, `ACMG` F59-13, `REC`/`REC2` F59-25/F60-18. **Give the EMU its own main relay** — do not
  let a faulted ECU hold the power supply for the running engine.
- **A second ECU to power, ground and live with**, forever, in a car that is otherwise standalone.

## 5. The assumption nobody has tested — and it is half an hour of work

The entire plan rests on one unproven claim: **a faulted Aristo ECU still transmits valid BEAN
gauge frames.** If that is false, every cost above is paid for nothing.

One reason for cautious optimism: from the factory, the temperature gauge reads at **key on, engine
off**. The ECU populates the cluster without the engine running at all, which suggests the gauge
path does not depend on the engine-control side being healthy. That is an argument, not evidence.

**Test it now, on the car as it sits, before any wiring changes.** Escalate one connector at a time,
key on, watching the cluster and the HVAC each time:

| Step | Disconnect | Watch for |
|---|---|---|
| 1 | throttle **motor** only | temp gauge still reads? lamps behave? MIL on? does the ECU hold the main relay? |
| 2 | motor **+ throttle position sensors** | same |
| 3 | motor + sensors **+ pedal** | same |
| 4 | also injectors and coils | does it still populate the cluster with the engine unable to run? |

If the cluster dies at step 1, the idea is finished and you have lost an afternoon rather than a
harness. If it survives step 4, you have the answer and — importantly — **you never needed to share
a sensor to get it.**

## 6. Recommendation

**Tier 1 — do this first.** Run the §5 disconnection test. It costs nothing, it is reversible, and
it decides everything. Also run [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md)
§10 Phase 1 while the ECU is still live, because a BEAN capture is unrecoverable afterwards and it
is your fallback if the ECU-as-gateway plan fails.

**Tier 2 — if the test passes, keep it *isolated*, not shared.** Wire the Aristo ECU as a dumb BEAN
transmitter and nothing else:

- **Give it:** permanent and switched power, ground, `THW` B2-14, `RL` B1-26, `MOPS` B2-8,
  `MOL` B1-6, `MPX1` F59-28 / `MPX2` F59-27. If the test shows it needs to believe the engine is
  turning, a synthetic `NE+` B1-23.
- **Do not give it:** throttle motor, throttle clutch, `VTA`/`VTA2`, `VPA`/`VPA2`, `VC`, or any
  shared sensor ground. Injectors, coils, `M-REL`, `FPC`, `ACMG`, `REC`/`REC2` all severed.
- Shared sensors only where a sensor is genuinely dual-ported and can be **buffered** — and even
  then, only for gauge signals, **never** for anything in the DBW loop.

This gets the whole prize with none of §2's coupling. It is strictly better than the sharing
proposal on every axis, which is why the sharing half should simply be dropped.

**Tier 3 — if the test fails**, the fallback is no longer "rewire the lamps," because that is not
possible (§3). It is: delete the ECU, accept a dark temperature gauge and three dark lamps, and put
coolant temperature and oil pressure on **separate gauges** or on a dash off the EMU. Everything is
still monitored — just not in the factory instrument. Speedometer, tachometer and fuel gauge are
unaffected.

Which means: **if the Tier 1 test passes, take it.** The alternative is meaningfully worse than it
looked a day ago.

## 7. The one-line answers

- **Will sharing the TPS cause Aristo ECU issues?** The ECU will fault regardless, because you took
  its motor. Sharing does not change that.
- **Does that matter?** Only in three ways, and the first two are what §5 tests: does it stop
  transmitting, does it do something harmful (drop the main relay, hold the MIL, disturb the bus),
  and — only if you share sensors — does it corrupt the EMU's throttle feedback. The third is
  entirely avoidable by not sharing.
- **Are we only keeping it for the cluster?** Yes. And the cluster prize is one temperature gauge
  and HVAC auto mode.
