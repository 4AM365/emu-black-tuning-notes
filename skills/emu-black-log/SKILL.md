---
name: emu-black-log
description: >
  Reads, parses, and diagnoses EMU Black ECU data logs exported as CSV.
  Use this skill whenever the user uploads or references a .csv file from
  an EMU Black ECU — identifiable by semicolon delimiters, a TIME column
  in seconds, and channels like RPM, MAP, TPS, CLT, Lambda is valid, ECU
  State, etc. Covers idle stalls, lean/rich conditions, boost control
  faults, knock events, cold-start issues, and general channel
  interpretation. Also applies to logs from EMU Classic (same format).
  Trigger on phrases like "ECU log", "EMU log", "data log", "diagnose my
  idle", "why did it stall", or any uploaded CSV that contains EMU Black
  channel names.
---

# EMU Black log analysis

## ⚠ RULE: gate every lambda diagnosis behind `Lambda is valid == 1`

EMU Black runs a conservative WBO heater warmup to avoid thermal shock cracking
the Bosch LSU 4.9 ceramic. During warmup (typically the first **30–60 seconds
post-start**, sometimes longer on a hot restart), the firmware:

- Holds `Lambda 1` at the placeholder value **1.000**
- Holds `Lambda 2` at its placeholder
- Disables closed-loop trim → `Short term trim` stays at 0
- Forces `Lambda is valid = 0`

**Any diagnosis that uses `Lambda 1`, `Lambda 2`, `AFR`, or `Short term trim`
during this period is meaningless — the numbers are placeholders, not measurements.**

Common mistake: looking at the first 30 seconds of a log, seeing lambda pinned
at 1.000 with STFT = 0, and concluding "fueling is perfect." It's not — there
is no feedback at all. The base fuel calculation could be 10% off in either
direction and the log would look identical.

Always start log analysis by computing the first time `Lambda is valid == 1`,
and discard or flag every lambda-based observation before that point:

```python
valid = df[df['Lambda is valid'] == 1]
if valid.empty:
    t_valid = None  # WBO never validated — entire log is open-loop
else:
    t_valid = valid.iloc[0]['TIME']
    print(f"WBO validated at t={t_valid:.1f}s ({t_valid - df['TIME'].iloc[0]:.1f}s into log)")

# Use this mask for anything lambda/STFT/AFR-related:
trustable = df['Lambda is valid'] == 1
```

This also constrains street-tuning protocols: any test that uses lambda or
STFT as feedback (closed-loop VE correction, STFT-as-VE-correctness signal in
VVT sweeps, lean-cruise tuning) must wait until the WBO is valid. EGT, MAP,
RPM, ignition retard, knock data are all valid immediately and don't need this
gate.

## File format

- **Delimiter**: semicolons (`;`), NOT commas
- **Sample rate**: typically 25 Hz (0.04 s intervals); can vary per log config
- **TIME column**: absolute ECU uptime in seconds (not wall-clock)
- **~500 columns** in a full log; most are zero or static — triage first

```python
import pandas as pd
df = pd.read_csv('log.csv', sep=';')
df.columns = df.columns.str.strip()
df = df.dropna(axis=1, how='all')  # drop empty trailing columns
```

## First-pass triage

Before deep analysis, scan these four things — **in this order**:

1. **Lambda is valid** — find the first `t` where it transitions 0→1.
   Every lambda/STFT/AFR claim must be qualified by this gate.
2. **ECU State** — 1 = idle/cranking, 3 = running. State drops back to 1 at stall.
3. **Trigger error count** — any non-zero value = crank/cam signal issue.
4. **Engine protection code** and **Check engine code** — non-zero = active fault.

```python
# Lambda validity timing — do this FIRST
valid = df[df['Lambda is valid'] == 1]
t_valid = valid.iloc[0]['TIME'] if not valid.empty else None

# Standard state checks
stall_rows = df[df['ECU State'] == 1]
trigger_faults = df[df['Trigger error count'] > 0]
protection = df[df['Engine protection code'] != 0]
```

## Channel reference — diagnostic tiers

### Tier 1: always check first

| Channel | Units | Notes |
|---|---|---|
| `RPM` | RPM | Stall = drops to 0; crank = 50–300 |
| `MAP` | kPa | Idle ~33–40; WOT near baro; after stall creeps to atmospheric |
| `TPS` | % | 0–100; should match driver intent |
| `CLT` | °C | Cold start <40°C; normal >85°C |
| `IAT` / `Charge temp` | °C | Charge air temperature; use whichever channel is populated |
| `Battery voltage` | V | Running: 13.8–14.4 V; stall/off: 12.5–12.9 V |
| `ECU State` | enum | 1=stopped, 3=running |
| `Lambda is valid` | 0/1 | 0 = open-loop; no STFT possible |
| `Short term trim` | % | 0 when WBO invalid; ±5% normal; ±15%+ = VE error |

### Tier 2: fueling & enrichment

| Channel | Notes |
|---|---|
| `Injectors PW` | ms; should rise on accel, fall on decel |
| `Injectors DC` | % duty cycle; >85% at WOT may indicate injector sizing limit |
| `VE` | volumetric efficiency % from table lookup |
| `Afterstart Enrichment` (ASE) | % extra fuel post-crank; decays over time/RPM |
| `Warmup enrichment` | % extra fuel by CLT |
| `Acc. enrichment %` | transient enrichment on throttle opening |
| `Fuel pressure` | bar; watch for drop under load (weak pump or regulator) |
| `Fuel pressure error` | non-zero = FPR deviation from target |
| `Fuel Cut` | 1 = fuel cut active |
| `Overrun status` | 1 = overrun condition; `Overrun fuel corr.` shows actual correction |

### Tier 3: ignition & timing

| Channel | Notes |
|---|---|
| `Ignition Angle` | degrees BTDC; sudden advance = idle recovery attempt |
| `Ignition From Table` | base table value; compare to `Ignition Angle` to see corrections |
| `I.Idle` | idle ignition correction; ECU retards/advances to hold target RPM |
| `Knock Level Peak` | V; compare against `Knock Engine Noise` to assess S/N |
| `Knock ign retard cyl 1–8` | per-cylinder retard in degrees; non-zero = knock detected |
| `Knock count` | cumulative; rising = knock protection active |
| `Spark cut percent` | non-zero = active spark cut (rev limiter, TC, etc.) |

### Tier 4: idle control (DBW builds)

| Channel | Notes |
|---|---|
| `Idle target` | RPM target |
| `Idle state` | enum (0=INACTIVE/driver, 1=ARMED, 2=ACTIVE/PID, 4=DBW BLEND — see enumerations) |
| `Idle air %` | final commanded airflow %; in `ACTIVE` = base + custom corr + PID; in `BLEND`/`ARMED` = base only (custom corr is logged but not applied per EMU help) |
| `Idle airflow custom corr.` | CAT-based feedforward correction value from `idleCustomCorrection` table; per EMU help only **applied** in `ACTIVE` state |
| `DBW Out. DC` | motor drive %; negative = closing actuator force, positive = opening (NOT throttle position) |
| `DBW target` | requested throttle position % |
| `DBW Target source` | who is commanding the throttle — see enumerations |
| `Idle PID air % correction` | PID output; **operates on idle-ignition-angle error, not RPM error** (per EMU help) — coupled to ignition PID |
| `Idle ignition correction` | idle ignition PID/table output relative to `Target ign. angle` |
| `Idle effective DC` | final output to actuator (stepper/PWM); not used on DBW builds |

### Tier 5: boost

| Channel | Notes |
|---|---|
| `Boost` | kPa gauge (MAP − Baro) |
| `Boost Target` | requested boost from table |
| `Boost DC` | wastegate solenoid duty cycle |
| `Boost out of margin` | 1 = over/under boost protection triggered |
| `Boost PID correction` | PID output; large = boost control hunting |

### Tier 6: VVT

| Channel | Notes |
|---|---|
| `VVT CAM1 angle` | intake cam position degrees |
| `VVT CAM1 angle target` | requested position |
| `VVT CAM1 solenoid DC` | oil pressure solenoid duty cycle |
| `VVT CAM1 status` | 0=OK, 1=error (cam not reaching target), 2=moving wrong direction, 3=disabled/locked out |

### Tier 7: sensor validation (status channels)

Most sensor channels have a paired `*status` field: 0 = OK, 1 = fault.
Check: `CLT status`, `IAT status`, `MAP status`, `Fuel press. status`,
`Engine oil pressure status`, `TPS main status`, `PPS main status`.

---

## Common diagnostic patterns

### Idle stall (warm engine, no fault codes)

Signature: RPM declines slowly then collapses; ECU State 3→1; no cuts active.

Check in order:
1. `Lambda is valid` — is WBO heating up? If 0 throughout, `Short term trim` = 0 and base VE must be correct.
2. `Afterstart Enrichment` — if decaying toward 0 while RPM is falling, ASE is masking lean VE table.
3. `Idle air %` and `DBW Out. DC` — if DBW is already pegged open and still losing RPM, insufficient base idle air.
4. `Battery voltage` — drops as engine stumbles (consequence), recovers after stall (not cause).
5. `Ignition Angle` — ECU will advance timing aggressively as RPM falls (last-ditch recovery); if this is happening, fueling is the root cause.

Fix: add fuel to idle VE cells (MAP 30–40 kPa, RPM 800–1200) at the operating CLT. Verify ASE decay rate isn't faster than WBO validation time.

Also check `Idle state` — a persistent value of 0 throughout means idle PID is disabled. Check brake switch state; a continuously active brake switch locks idle control into permanent open-loop mode and prevents all ignition correction and airflow recovery.

### Overrun-to-idle stall

Signature: stall occurs after lift-off from high RPM/boost; RPM drops toward idle, stumbles, then dies. A rich lambda spike is often visible just before the stall.

Check in order:
1. `Idle air %` / armed state airflow at the transition RPM (1800–2200 RPM) — resolving near 0% is the root cause.
2. `DBW Out. DC` at the transition — if it is −80% or worse, the throttle is fighting its return spring and supplying no air.
3. `Overrun status` and `Fuel Cut` — when does fuel return? Returning into near-zero airflow makes a rich stumble unavoidable.
4. `Short term trim` / `Lambda` immediately after fuel cut exit — a large positive lambda spike (lean) confirms fuel returned into too little air.
5. `Idle state` — if it stays at 0 through the transition, idle PID never engaged; check brake switch.

Fix: populate armed state airflow at 60–80% for the 1800–2200 RPM bins. The rich spike and stall will both disappear.

### Cold-start stall (CLT < 50°C)

Same as warm stall but also check:
- `Warmup enrichment` — should be 20–40% at 20°C
- `Cranking correction` — adequate pulse width for cold fuel atomization
- `Afterstart Enrichment` at 100% = start of ASE decay; ensure decay is slow enough

### Lean surge at cruise

Signature: AFR oscillates above lambda target; `Short term trim` chasing positive.

Check: VE table cells at cruise MAP/RPM. Also `Fuel pressure error` — lean can be FPR failing to track at vacuum.

### Knock event

```python
knock = df[df['Knock count'].diff() > 0]
```

Check: `Knock Level Peak` vs `Knock Engine Noise` (S/N ratio). If noise floor is high, may be false detection. Check `Knock ign retard cyl N` for per-cylinder distribution. A single cylinder repeating = possible detonation hot-spot.

### Boost overshoot / control fault

Signature: `Boost` spikes above `Boost Target`; `Boost out of margin` = 1.

Distinguish the two failure modes before adjusting anything:
- **Margin protection triggered** (`Boost out of margin` = 1, `Boost PID correction` stable): thresholds are too tight or base WGDC table is wrong. Widen margins and verify open-loop WGDC from ramp-run data.
- **PID hunting** (`Boost PID correction` oscillating, boost overshooting and undershooting): gains are too aggressive. Reduce P, then I.

Also check `Boost DC` saturation (0% or 100%) before the spike — a saturated duty cycle means the feed-forward table is miscalibrated, not a PID issue.

### VVT fault

Signature: `VVT CAM1 angle` deviates from `VVT CAM1 angle target` and does not recover.

- Large persistent error (>5°): oil pressure or solenoid issue. Check oil pressure at idle; VVT authority is limited below ~1.5 bar.
- Small oscillation (±2–3°): normal PID hunting — not a fault.
- `VVT CAM1 status` non-zero: ECU has flagged an error condition.
- Cold-engine deviation is expected if VVT is intentionally disabled below a CLT threshold.

---

## Python analysis templates

### Find stall events
```python
stalls = df[(df['RPM'] == 0) & (df['RPM'].shift(1) > 200)]
for i, row in stalls.iterrows():
    window = df.loc[max(0,i-50):i+20]
    print(f"Stall at t={row['TIME']:.2f}s")
    print(window[['TIME','RPM','MAP','Fuel Cut','Spark cut percent',
                   'Engine protection code','Lambda is valid']].to_string())
```

### Check WBO validation timing
```python
valid = df[df['Lambda is valid'] == 1]
if valid.empty:
    print("WBO never validated in this log")
else:
    first_valid = valid.iloc[0]['TIME']
    start_t = df.iloc[0]['TIME']
    print(f"WBO validated at t={first_valid:.1f}s ({first_valid-start_t:.1f}s after log start)")
```

### ASE decay profile
```python
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df['TIME'], df['RPM'], color='#378ADD', label='RPM')
ax2.plot(df['TIME'], df['Afterstart Enrichment'], color='#D85A30',
         linestyle='--', label='ASE %')
ax2.plot(df['TIME'], df['WBO Heater DC'], color='gray',
         linestyle=':', label='WBO heater DC')
plt.title('ASE decay vs RPM')
plt.tight_layout(); plt.show()
```

### Knock summary
```python
knock_cols = [c for c in df.columns if 'Knock ign retard cyl' in c]
knock_summary = df[knock_cols].abs().max()
print(knock_summary[knock_summary > 0])
```

---

## Key EMU Black state enumerations

| Channel | Value | Meaning |
|---|---|---|
| `ECU State` | 1 | Stopped / pre-start |
| `ECU State` | 3 | Running |
| `Idle state` | 0 | INACTIVE — PPS above activation threshold (driver in control) or engine off. Airflow = Armed-state table (engine running) or 0 (engine off) |
| `Idle state` | 1 | ARMED — PPS released, RPM above `Target + Ramp down offset`. Airflow taken from `idleArmedAirFlow` table. PID disabled, custom corr NOT applied. Ramp-down-offset decays toward 0 at `Ramp down decay rate` |
| `Idle state` | 2 | ACTIVE — closed-loop PID idle. Airflow = `idleActiveAirflow` + custom corr + PID. Airflow PID tracks ignition-angle error (not RPM error) |
| `Idle state` | 3 | AFTERSTART DELAY or CRANKING (verify per build — Idle help lists both as discrete states between INACTIVE and ACTIVE) |
| `Idle state` | 4 | DBW BLEND — blending between idle-commanded TPS and driver-commanded TPS via `idleDBWBlendPoint` (single value) or `idleDBWBlendPointTbl` (RPM-indexed). Custom corr NOT applied |
| `Idle state` | 5 | CYCLING IDLE — cyclic RPM increase for cooling (alternative strategy) |
| `Idle state` | 6 | DC OVERRIDDEN — diagnostic override (do not use while vehicle is moving) |
| `Lambda is valid` | 0 | WBO not ready (no trim) |
| `Lambda is valid` | 1 | WBO validated (trim active) |
| `Overrun status` | 1 | Overrun condition met (check `Overrun fuel corr.` for actual cut) |
| `DBW Target source` | 0 | **Target table** — driver pedal via `dbwCharacteristic1/2` (paired with Idle state 0) |
| `DBW Target source` | 1 | **Override** — diagnostic override DC/target (do not use while moving) |
| `DBW Target source` | 2 | **Idle** — idle controller commanding throttle (paired with Idle state 1, 2, or 5) |
| `DBW Target source` | 3 | **Idle blend** — DBW Blend state (paired with Idle state 4) |
| `DBW Target source` | 4 | **DSG blip** |
| `DBW Target source` | 5 | **CAN control** — via CAN message |
| `DBW Target source` | 6 | **Launch control** |
| `DBW Target source` | 7 | **Cruise control** |
| `DBW Target source` | 8 | **Rev limiter** |
| `DBW Target source` | 9 | **Overrun** |
| `DBW Target source` | 10 | **Flat shift** |
| `DBW Target source` | 11 | **Rev matching** |
| `DBW Target source` | 12 | **Pit limiter** |
| `DBW Target source` | 13 | **ALS** |
| `DBW Target source` | 14 | **Rolling start** |
| `DBW Target source` | 15 | **Gear shift** |
| `VVT CAM1 status` | 0 | OK |
| `VVT CAM1 status` | 1 | Error — cam not reaching target |
| `VVT CAM1 status` | 2 | Error — cam moving in wrong direction |
| `VVT CAM1 status` | 3 | Disabled / locked out |
| `Engine protection code` | 0 | No fault |
| `Engine protection code` | non-zero | Protection active; bitmask — use EMU Software live diagnostics to decode |
| `Check engine code` | 0 | No fault |
| `Check engine code` | non-zero | Sensor/system fault logged; use EMU Software to decode |


