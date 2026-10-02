# CAN breakout node — passenger footwell

3D-printed enclosure carrying parallel DTM connectors, splitting one CAN bus (and switched
power) from the EMU Black to four peripherals. Five DTM positions, four used.
Designed 2026-08-23; **not yet built.** General topology rules and the termination
arithmetic live in [notes/can_serial.md](../../notes/can_serial.md) — this page is the
vehicle-specific application only.

## Nodes and runs

| Node | Run from box | Role |
|---|---|---|
| EMU Black | short — same footwell | trunk end, terminated internally (`canBusTerminator`) |
| TPMS module | 10 cm | stub |
| EDL-1 | 10 cm | stub |
| EGT-to-CAN | 30 cm | stub — **at the stated limit**, trim if convenient |
| CAN Switchboard | undecided | stub or trunk end — see below |
| 5th DTM | — | spare, left open; a zero-length stub, no action needed |

The EMU occupies one trunk end because its 120 Ω is inside the ECU, so exactly one
peripheral can be promoted to the other end.

## Two viable layouts

Both use exactly two 120 Ω (60 Ω measured). The choice hinges only on where the
Switchboard ends up mounted.

**A — Switchboard within 30 cm.** Trunk = EMU → box. Second 120 Ω soldered across the
CAN-H/CAN-L bus junction inside the enclosure. All four peripherals are stubs. One
resistor location, four identical short pigtails, nothing to remember at a remote module.
Preferred if the Switchboard's sensor wiring reaches from the footwell.

**B — Switchboard remote.** Trunk = EMU → box → Switchboard, second 120 Ω at the
Switchboard (its own terminator if it has one, otherwise soldered into the DTM shell). The
box becomes a mid-bus junction with three stubs. Frees the Switchboard's placement
entirely, since that leg is trunk and the 30 cm cap does not apply to it.

A second remote peripheral is not available under either layout without daisy-chaining the
trunk through an existing node.

## The A-vs-B trade

Layout A does not remove length from the system, it moves it from CAN to analog. The
Switchboard's 0–5 V and thermistor runs lengthen instead. That is normally the better
trade — CAN has a hard 30 cm number while analog sensor runs tolerate several meters,
provided each sensor returns to the Switchboard's own sensor ground and the runs are routed
clear of coil and injector wiring. Decide from where the Switchboard's sensors physically
sit, not from the CAN constraint.

## Open items

- **Onboard terminators on the Switchboard, EDL-1, TPMS, and EGT-to-CAN: unverified.**
  Check each manual; disable all of them. Confirm empirically with the 60 Ω measurement
  before first power-up.
- Switchboard mounting location undecided — this selects layout A or B.
- Confirm `canBusTerminator` is set in the *live* tune, not just in an export.
- All five nodes must run the same bus speed (`canBusSpeed`).
