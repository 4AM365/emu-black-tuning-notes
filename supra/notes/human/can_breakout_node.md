# CAN breakout node — passenger footwell

## What this covers
The planned 3D-printed DTM junction box in the passenger footwell that splits one CAN bus
from the EMU to the TPMS module, EDL-1, EGT-to-CAN, and CAN Switchboard. Not built yet.
Canonical: [`../can_breakout_node.md`](../can_breakout_node.md). General CAN rules:
[`notes/can_serial.md`](../../../notes/can_serial.md).

## The rules
- The EMU takes one end of the trunk — its 120 Ω is inside the ECU, so the bus can't pass
  through it. That leaves exactly one end for a peripheral.
- **Layout A** — Switchboard within 30 cm: trunk is EMU → box, second 120 Ω soldered inside
  the enclosure, all four devices are stubs. Simplest; preferred if the sensors reach.
- **Layout B** — Switchboard remote: trunk is EMU → box → Switchboard with the 120 Ω out at
  the Switchboard. Its run becomes trunk, so no length limit on it.
- Only one peripheral can be remote. A second would need daisy-chaining.
- Layout A doesn't delete length, it moves it to the Switchboard's analog sensor runs.
  That's usually the right trade — analog tolerates meters, CAN doesn't.

## Key numbers
- Stub lengths: TPMS 10 cm, EDL-1 10 cm, EGT-to-CAN 30 cm, Switchboard TBD.
- The EGT run at 30 cm is **at** the limit, not under it. Trim it if it's free to do so.
- Five DTM positions, four used; the spare stays open and needs nothing.
- Target 60 Ω across CAN-H/CAN-L with everything plugged in and the key off.

## When to care
Before cutting wire, and again before first power-up. The open questions are where the
Switchboard mounts and whether any of the four modules has its own 120 Ω hiding in it —
both unverified.
