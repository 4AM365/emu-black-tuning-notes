# 4000 rpm idle after the CD009 swap

> **⛔ NOT THE SUPRA.** Josh Napier's GS300 (JZS160) / JDM Aristo (JZS161) 2JZ-GTE VVT-i / CD009.
> Never carry values, pins, hardware or conclusions between this car and the Supra notes in either
> direction, and never load `supra-specs` for it. Full caveat in [`my_car.md`](my_car.md).

Written 2026-09-08. **Symptom:** with the automatic gone and the CD009 in, the car settles at
~4000 rpm immediately after start. Idle control is faulting.

---

## Bottom line

**Don't tune around it.** This is the OEM Aristo ECU's idle controller failing because the inputs
it needs were bolted to the gearbox that left the car. That ECU is scheduled for deletion and the
EMU is taking DBW. Time spent making the Aristo ECU idle nicely is time spent on a component
you are removing.

**But do three things now, in this order:**

1. **Stop driving it.** §4.
2. **Pull the OEM diagnostic trouble codes.** §5. They name exactly which inputs the ECU is
   unhappy about, and that information is destroyed the moment the ECU comes out.
3. **Look at the instrument cluster while it is faulted.** §6. The car is running the experiment
   from [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md) §5
   for free, right now.

---

## 1. What idle control lost when the automatic left

Every one of these was a live input to the Aristo ECU and is now open circuit:

| Signal | Pin | Why idle cared |
|---|---|---|
| **Vehicle speed** `SP2+` / `SP2-` | B3-5 / B3-11 | wilbo666, verbatim: *"Vehicle speed is used in **idle control**, automatic transmission shift control, cruise control, speed limiting etc."* This is a direct, documented idle input, and it is gone |
| **Neutral** `N` | B2-13 | on a Toyota automatic the neutral/park state is a first-class idle input — the ECU schedules a different idle for in-gear versus out-of-gear |
| Gear position `P` `R` `D` `2` `L` `3` | F59-26, F59-16, F59-17, B2-20, B2-21, F59-7 | same family of information; all now open |
| OD direct clutch speed `NCO±` | B3-4 / B3-10 | a second driveline speed reference |
| ATF temperature `OIL` | B3-17 | load and drag estimation |
| Shift and pressure solenoids `S1` `S2` `S4` `SD` `SLU±` `SLN±` `SLT±` | B3-1, 2, 6, 3, 7/13, 8/14, 9/15 | **all open circuit.** The ECU's own actuator self-tests now fail on every one |

The Aristo ECU is a combined engine **and** ECT controller — there is no separate transmission
computer. So this is not a peripheral losing a signal. Roughly half of what that ECU was built to
supervise has vanished, and it is finding out about it on every power-up.

## 2. Why it goes *high* rather than low

This is the part worth thinking about, because a confused idle controller usually stalls.

### Correction — the "opener" evidence was the wrong engine's throttle body

An earlier draft of this section built Hypothesis 1 on RM718U pp. 841–843, describing a mechanical
default ("opener," ~3.5°) with matching TPS values. **Those pages are headed `SFI (2JZ-GE)`** —
they are the GS300's own factory throttle body, on the naturally-aspirated engine no longer in the
car. That evidence does not describe hardware installed on this vehicle and the specific angle and
TPS numbers below should not be trusted. The section is corrected here.

**Hypothesis 1 — the ECU has lost authority over the blade and it has gone to some default position.**
Whether that default is a spring-loaded mechanical stop and what angle it sits at is **not
established for the Aristo throttle body** — nothing in wilbo666's notes or the pinout text
describes one. What is established: wilbo666 on `CL+` B1-20: *"The ETCS-i clutch must be engaged
for the electric motor to be able to open or close the throttle."* Losing that clutch means the
motor cannot hold or move the blade, and whatever the blade does next is spring and geometry, not
ECU command.

*Prediction if true:* the blade does not respond to the pedal, `CL+`/`CL-` is unpowered, and `VTA`
sits at some fixed value regardless of pedal input.

**Hypothesis 2 — the ECU is genuinely commanding a high airflow.** Some fault path lands on a
default or maximum airflow rather than a minimum.
*Prediction if true:* the blade still tracks the pedal, `VTA` follows what the ECU commands, clutch
energised.

**Hypothesis 3 — the rpm is real but the air is not coming through the blade.** An intake or vacuum
leak introduced during the swap work — a disturbed hose, a brake booster line, something moved when
the trans came out.
*Prediction if true:* `VTA`/`VTA2` read near-closed while the engine sits at 4000.

**Hypothesis 4 — the EMU piggyback is contributing.** The EMU is in the loop today. Whether it is
touching anything that feeds idle is unknown until the Phase 0.4 inventory in
[`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) §10 is done.

**What we cannot look up:** RM718U is missing its **DIAGNOSTICS** section — the SFI chapter's ECM
inspection points at page DI-20 and that page is not in our copy — and EWD356U documents fail-safe
behaviour only for the moon roof and the ABS/TRAC/VSC ECU, never for the throttle. So the actual
ETCS-i fail-safe response on a JZS161 is **not established from anything we hold.** Hypotheses 1
and 2 are reasoned from the clutch requirement and the symptom timing, not read out of a book.
Treat them as hypotheses and let the measurements below decide.

## 3. The measurements that separate them — about twenty minutes

| # | Test | Reading | Points to |
|---|---|---|---|
| 1 | Key on, engine off. Watch the throttle blade | does it perform the ETCS self-sweep? | no sweep → motor or clutch has no authority → **H1** |
| 2 | Key on, engine off. Press the pedal slowly | does the blade follow? | no movement → **H1**. Follows → **H2** or **H3** |
| 3 | Engine at the 4000 rpm idle: read `VTA` B2-23 and `VTA2` B2-24 | is the blade actually open? | open → **H1** or **H2**. Near closed → **H3**, go leak-hunting |
| 4 | Measure across `CL+` B1-20 / `CL-` B1-19 while running | energised? | de-energised → **H1** confirmed |
| 5 | Compare ECU-commanded position against actual `VTA` | do they agree? | disagreement with the clutch dropped → **H1**. Agreement at a high value → **H2** |

Do 1 and 2 first. They need no meter and they split the field in half.

## 4. Safety — this matters more than the diagnosis

A 4000 rpm no-load idle in a car with a **manual gearbox** is a different problem from the same
symptom in an automatic. Engaging a clutch at 4000 rpm is how driveline parts and people get hurt.

If Hypothesis 1 is right, **the throttle is not under anyone's control** — not the Aristo ECU's,
and, on the documentation we hold, not yours either: every Aristo-specific source describes `VPA`/
`VPA2` as a pedal position **sensor** feeding the ECU, with no accelerator cable mentioned anywhere.
If that holds on the physical car, lifting off does nothing because the pedal was never mechanically
connected to the plate. **This is now disputed — see §9** — confirm which is true before assuming
either way.

- Do not drive the car.
- Do not assume the pedal can bring the revs down.
- Have a way to kill it that does not depend on the throttle — ignition, or a fuel pump relay you
  can reach without leaning over the engine.
- Run it only long enough to take the §3 readings.

## 5. Capture the DTCs now — this is on a clock

The Aristo ECU has been logging exactly which inputs it lost, in its own words. Read the codes
through `SIL` F60-11 at the diagnostic connector **before the ECU is removed**. Once it is out,
that information does not exist anywhere.

This joins the BEAN capture as an unrecoverable Phase 1 item in
[`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) §10. Do them in the same
session. The codes are also the cheapest possible confirmation of §1 — if the ECU is throwing
speed-sensor, gear-position and solenoid-circuit faults, the diagnosis is closed.

## 6. The car is running a useful experiment for free

[`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md) §5 proposes an
afternoon of disconnection testing to answer one question: **does a faulted Aristo ECU still
transmit valid gauge data over BEAN?**

The car is currently a faulted Aristo ECU. So look at the cluster, right now, while it sits at
4000 rpm:

- Does the **water temperature gauge** read and rise as the engine warms?
- Are the **charge**, **oil pressure** and **oil level** lamps behaving sanely — off when they
  should be off?
- Is the **check engine** lamp lit? (Expected — `W` F60-6.)
- Does the **HVAC** still run in auto mode?

If the gauges are alive, the Tier 2 plan in that paper is validated by observation rather than by
argument, and you have saved the afternoon. If the cluster is dead or frozen, that is equally
decisive and the fallback applies.

**This costs one look at the dash.** Do it before anything else changes.

## 7. What this changes in the plan

- **The car is not usable as it stands**, so there is no cost to pulling it off the road and doing
  [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md) §10 Phases 0 and 1 now.
  The schedule pressure that would normally argue for a quick fix has evaporated.
- **Do not spend effort making the Aristo ECU idle correctly.** Even if you found the fault path
  and satisfied it — a speed signal spoofed onto `SP2±`, a neutral signal onto `N` — you would be
  calibrating a controller you are about to remove, and you would be doing it on the very inputs
  the EMU is going to own.
- **The one exception:** if the §6 cluster check says the gauges survive, then keeping the Aristo
  ECU as a bus node becomes the plan, and at that point it is worth knowing whether it can be kept
  in a *quiet* fault state rather than a noisy one. That is a question for after the DBW handover,
  not before it.
- **This is now the reason to move on the DBW work.** Idle on this engine is the throttle plate —
  there is no idle air valve on either car. The 4000 rpm idle does not get fixed by a setting; it
  gets fixed by the EMU taking `M+`/`M-`, `CL+`/`CL-`, `VTA`/`VTA2` and `VPA`/`VPA2` and running
  the blade itself.

---

## 8. Decision — move DBW to the EMU now, but unplug the throttle rather than the ECU

**Superseded pending §9.** This section assumes the throttle is motor-driven-only, per every
Aristo document we hold. If the §9 physical check instead confirms a live cable, skip this section
and go straight to §9’s IACV path — it is simpler and there is no reason to wire DBW if the
mechanical path already works. Left in place in case the check goes the other way.

**Will's argument, 2026-09-08:** the EMU cannot control idle because the OEM ECU owns DBW; the OEM
ECU is faulted and cannot control DBW either; therefore nobody has the throttle, and moving DBW to
the EMU can only be an improvement, codes be damned.

**That is correct.** The OEM ECU's ownership of the throttle currently has *negative* value — it is
not regulating the blade, it is holding it open. Any state in which the EMU owns the throttle is
strictly better than the present one, because the present one is *nobody owns the throttle*. There
is no configuration to protect and nothing to lose.

**One refinement makes it materially better: take the throttle off the OEM ECU, do not remove the
OEM ECU.** Leave it powered and on the bus. Same work, and you get:

- idle control back, and the car safe again;
- the ECU still transmitting on BEAN, so the cluster question stays open rather than being decided
  by demolition — and §2a of [`stock_ecu_bypass_dependencies.md`](stock_ecu_bypass_dependencies.md)
  says those gauges cannot be recovered any other way;
- **this move *is* steps 1–2 of the disconnection test** in
  [`position_keep_aristo_ecu_for_cluster.md`](position_keep_aristo_ecu_for_cluster.md) §5. You get
  the answer for free, as a side effect of work you were doing anyway;
- the BEAN capture still available afterwards — nothing irreversible happens;
- no sensor sharing. The OEM ECU simply loses `VTA`/`VTA2`/`VPA`/`VPA2`, which is the isolation the
  position paper argued for. It does not need them to transmit gauge data.

### Three things that must be true first

| # | Requirement | Why |
|---|---|---|
| 1 | **The EMU gets its own main relay and its own permanent 12 V** | do not leave the ECU that now controls your throttle hanging off a relay the faulted OEM ECU drives through `M-REL` F60-10. If the OEM ECU faults harder and drops that relay, it takes the throttle controller with it. **This is the trap in the whole plan** |
| 2 | **The EMU must drive `CL+` / `CL-` B1-20/19, and `+BM` F60-7 must feed the EMU's DBW stage** | wilbo666: *"The ETCS-i clutch must be engaged for the electric motor to be able to open or close the throttle."* An unenergised clutch means the EMU cannot move the blade either — you would reproduce the exact present symptom with a different ECU in charge. `+BM` is on its own 15 A ETCS fuse |
| 3 | **Know what the EMU already owns** — Phase 0.4 | if the OEM ECU is still doing fuel or ignition, giving the EMU the air alone leaves two controllers pulling against each other. Air is the dominant idle lever, so it will still improve things, but the split needs to be known before it is called finished |

### Do this in the same session

- **Read the OEM DTCs first** (§5) — before the throttle comes off it, while the codes describe the
  transmission fault rather than the fault you are about to add.
- **Photograph the dash** before and after. Before: faulted ECU with throttle. After: faulted ECU
  without throttle. If the gauges survive both, Tier 2 of the position paper is proven.
- **Wire per v3, not v2** — throttle `VTA` to the **TPS input**, pedal `VPA` to a free analog input.
  This is reversed from 2.xxx and it is the easiest thing to get wrong.
- Run **Tools → DBW calibration tool** with the blade genuinely free — the OEM ECU must be fully off
  the motor and clutch, not partially.
- Add the check sensors and their tolerance maps **after** calibration, per
  `docs/emu-black-help/DBW.md` steps 10–11.

### What this does not fix

The OEM ECU will throw more codes, not fewer, and the MIL stays on. Cruise control is gone either
way. The stability-control serial link is unaffected today and dies later. None of that is a reason
to wait.

---

## 9. Cable throttle + IACV instead of DBW — assessed

**Will's proposal, 2026-09-08:** the throttle body is cable-operated, with the ETCS-i motor as an
electric "adder" on top of a mechanical cable connection. If so, unplugging the motor leaves a
working mechanical throttle, and idle can be handled with a simple two-wire IACV instead of DBW.

### This contradicts what our Aristo documents show, and needs a look at the part

**Correction to an earlier version of this note:** the "mechanical opener" evidence previously cited
here (RM718U pp. 841–843) is the **GS300's own 2JZ-GE throttle body**, not the Aristo unit installed
in the car. That was a documentation mix-up on this note's part and has been struck from §2.

Separately, and on its own footing: **every Aristo-specific document we hold describes a pedal
position *sensor*, not a cable.** wilbo666's pin-by-pin notes and the Aristo pinout text both
describe `VPA` / `VPA2` as *"the variable voltage from one of the outputs from the position sensor
that measures how depressed the accelerator pedal is"* — an electrical sensor, feeding the ECU,
with the ECU then driving the blade through the `M+`/`M-` motor and `CL+`/`CL-` clutch. **Neither
document mentions a cable anywhere.** That is the standard signature of a pure fly-by-wire
throttle, and it is consistent with why this specific throttle body is sought after for swaps in
the first place — as a cable-eliminating DBW unit, distinct from a cable-throttle VVT-i head.

**That is not proof the physical part in this car matches the documentation** — throttle bodies get
swapped, modified, and mismatched to their documentation more often than any other component in a
build like this. But it is enough of a discrepancy from "cable operated, motor as an adder" that it
is worth confirming by eye before any wiring is cut, because the two paths lead to different jobs:

| If confirmed | The job is |
|---|---|
| **Cable pulley on the throttle shaft, motor/clutch genuinely an add-on** | § below — straightforward. Unplug the motor, fit an IACV, done |
| **No cable path — pedal sensor only, blade is motor-driven-only** | the earlier plan stands: EMU takes `M+`/`M-`/`CL+`/`CL-` and drives the existing motor (§8). A cable throttle body would have to be sourced and fitted, which is a different and larger job than an IACV alone |

**The check:** with the ECU and motor connector both disconnected, work the accelerator pedal (or
the cable end, if one is visible) by hand and watch the throttle shaft. If it rotates the blade,
the cable path is real and the table above resolves in your favor. If nothing on the throttle body
moves, the ECU's pedal sensor was never mechanically linked to the plate, and the swap needs a
different throttle body, not just a repin.

### If the cable path is confirmed — how to wire the IACV

Assuming the check above confirms a live mechanical path, this is materially simpler than DBW and
the EMU supports it natively:

- **Idle actuator type:** in the EMU's Idle strategy, select **PWM solenoid** rather than DBW.
  ECUMaster's own framing: *"The amount of airflow entering the engine is a fundamental parameter
  … The airflow quantity can be controlled using an electronic throttle … or, in the case of
  mechanical throttles, etc., using additional actuators such as PWM valves, stepper motors, etc."*
  (`docs/emu-black-help/Idle.md`).
- **Range:** set `Solenoid Min DC` / `Solenoid Max DC` to bound the valve's authority — *"Make sure
  the actuator can provide sufficient airflow for maximum idle RPM during cold start, and that it
  does not allow the engine to stall at minimum airflow."*
- **Battery compensation:** the `PWM Batt. corr.` table exists specifically because *"this table
  adjusts the … duty cycle, compensating for voltage changes in the system"* — fill it in, cranking
  voltage sag otherwise moves idle airflow underneath you.
- **Fuel-load correction — check this one carefully.** ECUMaster's own caveat: *"In the case of
  engines using the Alpha-N strategy for fuel injection calculation along with an additional
  solenoid controlling airflow during idle, any changes in airflow will not directly affect the
  engine load… use the Airflow VE Correction map."* This engine reads `PIM` (MAP) — confirmed by
  the Aristo pinout, B2-9 — so it is very likely speed-density rather than Alpha-N, in which case
  bypass air shows up as a MAP change and this correction is less critical. **Confirm the fuel
  strategy on the EMU side (Phase 0.4) before assuming it can be skipped.**
- **What still needs the EMU regardless of this decision:** the throttle's own position sensors
  (`VTA`/`VTA2`) remain useful as a plausibility check even on a cable throttle — confirming the
  blade is actually where the cable says it should be. Not required, but cheap insurance given
  they're already wired to the connector.
- **What this removes from the DBW section (§4) if the cable path is confirmed:** the entire
  `M+`/`M-`/`CL+`/`CL-` H-bridge and clutch drive, the DBW calibration tool step, and the check-
  sensor tolerance-map work in §8's correction. All of that was written for the motor-driven-blade
  case and does not apply if the cable is live.

### Recommendation

**Do the thirty-second check first.** Nothing below is worth planning around until it's settled.

If it confirms a cable: this is the better plan. Fewer failure modes than DBW, no calibration tool,
no check-sensor tolerance mapping, and the throttle becomes purely mechanical — one less
safety-critical system for the EMU to own. Proceed with the IACV per the wiring notes above.

If it does not: the earlier §8 plan (EMU drives the existing motor and clutch) is the one to
execute, and a cable-operated throttle body would need to be sourced separately if that path is
still wanted later.
