# CAN, Serial — settings reference

> **Software page:** *CAN, Serial*. Full symbol catalog: [tune_feature_tree.md → CAN, Serial](tune_feature_tree.md).

CAN bus, serial, and dash communication — the EMU stream, OEM CAN integrations (vehicle presets), and CAN switch panels / keypads (sp/csb/scb/pmu).

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Switch panels / keypads (CAN)** (112) — `csbEnable`, `csbEnableAin1`, `csbEnableAin2`, `csbEnableAinX1`, `csbEnableAinX2` …
- **CAN / dash / OEM integration** (32) — `userCANStream`, `canBoschABS`, `canBusDashType`, `canBusSendEMUDataOverCAN`, `canBusSpeed` …

---

## Bus topology and termination

**The invariant is 60 Ω differential across the whole bus** — exactly two 120 Ω resistors,
one at each end of the trunk, never one per device. Each extra terminator lowers the load
the transceivers drive against (3 → 40 Ω, 4 → 30 Ω, 5 → 24 Ω) until dominant bits stop
resolving. ECUMaster states the both-ends requirement and the twisted-pair requirement at
[CANSerial.md:25](../docs/emu-black-help/CANSerial.md).

**Trunk vs. stub.** The trunk is the backbone, end terminator to end terminator; a stub
(drop) is anything hanging off it. The stub limit is **< 30 cm, and it does not relax with
bit rate** — the same 30 cm applies at 1 Mbps and 500 kbps
([CANSerial.md:13](../docs/emu-black-help/CANSerial.md),
[:20](../docs/emu-black-help/CANSerial.md)). What *does* scale with rate is total bus
length: 40 m at 1 Mbps, 100 m at 500 kbps; 30 nodes either way.

**The rule runs one direction only.** Anything longer than 30 cm *must* be trunk. The
converse is false: a trunk has no minimum length, need not be the longest run, and can be
shorter than a stub. The only hard constraint is the 30 cm cap on drops.

**A trunk has exactly two ends** — so at most two devices can sit far from a junction box.
Terminating a device promotes its run from stub to trunk and frees it from the 30 cm cap,
but only for that one node per end. A further remote device requires chaining the trunk
*through* an existing node (CAN-in / CAN-out at that device), not a second star leg.

**EMU end.** The EMU Black's terminator is internal and software-switchable via the
`canBusTerminator` bool. It lives in the tune, so it travels inside the `.emub3` —
restoring an older tune or loading another car's base map can silently clear it, and the
symptom is `BUS ERROR` (listed among the CANBUS State faults at
[CANSerial.md:46](../docs/emu-black-help/CANSerial.md)). Check the symbol before suspecting
a wiring fault. Because the resistor is inside the ECU, the EMU is necessarily an end node:
the trunk cannot pass through it.

**Peripheral terminators are the usual failure mode.** ECUMaster CAN modules vary — some
carry an onboard 120 Ω (fixed, jumper, or software-selected). *Unverified per device;*
confirm each peripheral's manual and disable every one except the two you intend.

**Verification — do this before first power-up.** Fully wired, everything plugged in,
ignition off, meter across CAN-H / CAN-L at any connector:

| Reading | Terminators present |
|---|---|
| 120 Ω | 1 — one is missing |
| **60 Ω** | **2 — correct** |
| 40 Ω | 3 |
| 30 Ω | 4 |
| 24 Ω | 5 |

With a software-switchable end this isolates in two steps without pulling connectors:
`canBusTerminator` off → expect 120 Ω (proves the far resistor exists *and* that no
peripheral is terminated); on → expect 60 Ω.

**Build rules.** Solder the terminator across the CAN-H/CAN-L bus junction, never onto a
connector pin — unplugging a module must not be able to un-terminate the bus. Twisted pair
on the trunk and on every stub. All nodes on one bus must share the same speed
(`canBusSpeed`).

Vehicle application: [supra/notes/can_breakout_node.md](../supra/notes/can_breakout_node.md).
