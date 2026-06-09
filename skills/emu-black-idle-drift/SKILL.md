---
name: emu-black-idle-drift
description: >-
  Attributes a slow hot-soak idle RPM drift in an EMU Black log to its cause — airflow
  PID winding out an excess vs an exogenous charge-temp/IAT torque drift the PID chases.
  Use whenever the user says "my idle drifts down after a hot stop", "idle walks to
  target over 30 seconds", "why does hot idle sag", "is the PID or heat-soak driving my
  idle drift", or wants to decompose a hot-idle decay. Takes the longest hot, parked,
  idle-active stretch, splits idle air into PID vs base (total − PID), overlays charge
  temp / IAT / idle ignition correction / lambda, and prints each channel's trend
  (slope/s) and correlation with RPM so cause (leads, exogenous) separates from response
  (PID). Writes a 3-panel timeline plot. Takes the log as an argument (not
  vehicle-specific). Pairs with emu-black-idle-stability.
---

# EMU Black hot-idle drift attribution

A hot stop often enters idle high and decays to target over ~25–30 s. This separates
**cause from response**: take the longest hot (`CLT ≥ 95 °C`), parked, idle-active
stretch (no settle-drop, so the entry is visible), split idle air into **PID vs base**
(`base = Idle air % − Idle PID air % correction`), and overlay charge temp, IAT, idle
ignition correction, and lambda.

For each channel it prints **start → end**, **slope/s**, and **correlation with RPM**:

- If the **feed-forward base air** (charge-temp bleed) carries the decay while the PID
  sits pinned at its clamp → the walk-down is the FF, not the PID (the classic hot-soak
  windup/purge pattern — fix with the independent integral cap, not more FF).
- If charge temp/IAT **lead** RPM → an exogenous torque drift the PID is chasing.

## Usage

```bash
python scripts/idle_drift_attribution.py LOG.csv [out.png] [hot_clt]
```

- Requires `pandas`, `numpy`, `matplotlib`. Defaults: out `idle_drift_attribution.png`,
  hot CLT 95 °C.

## Related

- `emu-black-idle-stability` — steady idle tracking/CoV.
- Background: `notes/idle.md` (P2 two-PID architecture; `idle_hot_drift_pid_windup.md`).
