# CAN bus — topology and termination

## What this covers
How to wire a CAN bus with more than two devices on it: where the terminating resistors
go, how long each branch can be, and how to prove it's right with a multimeter before you
power anything up. Canonical: [`../can_serial.md`](../can_serial.md).

## The rules
- **Two 120 Ω resistors. Total. Ever.** One at each end of the trunk — not one per device.
  Extra terminators drop the bus resistance until the transceivers can't drive it.
- **Trunk vs. stub.** The trunk is the backbone, resistor to resistor. A stub is any branch
  hanging off it. Stubs are capped at 30 cm; the trunk has no length rule that matters here.
- The rule only runs one way: anything over 30 cm **must** be trunk. A trunk is allowed to
  be short — even shorter than a stub.
- **A trunk has two ends,** so only two devices can be far away. Everything else lives
  within 30 cm of a junction, or you daisy-chain the trunk through a device.
- The EMU's own terminator is a tune setting (`canBusTerminator`), so it rides in the
  `.emub3`. Loading an old tune can switch it off and it looks exactly like a wiring fault.
- Terminators get soldered to the bus junction, never to a connector pin. Unplugging a
  module must not un-terminate the bus.
- Peripheral modules often have their own hidden 120 Ω. Find them and turn them off.

## Key numbers
- **60 Ω** across CAN-H/CAN-L, power off = correct. 120 Ω = one missing. 40/30/24 Ω = three,
  four, five terminators.
- **30 cm** max stub — same at 1 Mbps and 500 kbps; it does not relax at lower speed.
- Total bus length: 40 m at 1 Mbps, 100 m at 500 kbps. 30 nodes max either way.

## When to care
Any time you add a device to the bus, build a junction box, or see `BUS ERROR`. Measure the
60 Ω before first power-up — it catches every termination mistake in one reading.
