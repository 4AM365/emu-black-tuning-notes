# CAN, Serial — settings reference

> **Software page:** *CAN, Serial*. Full symbol catalog: [tune_feature_tree.md → CAN, Serial](tune_feature_tree.md).

CAN bus, serial, and dash communication — the EMU stream, OEM CAN integrations (vehicle presets), and CAN switch panels / keypads (sp/csb/scb/pmu).

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Switch panels / keypads (CAN)** (112) — `csbEnable`, `csbEnableAin1`, `csbEnableAin2`, `csbEnableAinX1`, `csbEnableAinX2` …
- **CAN / dash / OEM integration** (32) — `userCANStream`, `canBoschABS`, `canBusDashType`, `canBusSendEMUDataOverCAN`, `canBusSpeed` …
