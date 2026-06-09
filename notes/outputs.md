# Outputs — settings reference

> **Software page:** *Outputs*. Full symbol catalog: [tune_feature_tree.md → Outputs](tune_feature_tree.md).

Physical and logical output drivers — PWM tables, gauge/GP outputs (tacho, shift light, relays), and electrical/cooling aux (alternator, electric water pump).

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Electrical / cooling aux** (24) — `altCtrlTargetVoltage`, `ewpTable`, `ewpTableBin`, `altCtrlBaseDC`, `altCtrlDCOutputMax` …
- **PWM tables** (21) — `pwm2XAxis`, `pwm2YAxis`, `pwmTable`, `pwmTable2`, `pwmXAxis` …
- **GP / aux outputs** (16) — `freqCustomXAxis`, `frequencyOutputTbl`, `buzzerFunction`, `dtoEnable`, `dtoMinTime` …
