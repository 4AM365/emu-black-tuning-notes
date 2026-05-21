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

Before deep analysis, scan these three things:

1. **ECU State** — 1 = idle/cranking, 3 = running. State drops back to 1 at stall.
2. **Trigger error count** — any non-zero value = crank/cam signal issue.
3. **Engine protection code** and **Check engine code** — non-zero = active fault.
4. **Lambda is valid** — 1 = WBO sensor warmed and validated; 0 = open-loop, no trim.

```python
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
| `Idle state` | 0=off, 2=active PID, 4=recovery mode |
| `Idle air %` | requested airflow; if maxed and RPM still low = not enough base air |
| `DBW Out. DC` | throttle drive %; negative = closing, positive = opening |
| `DBW target` | requested throttle % |
| `Idle PID air % correction` | PID output; large correction = system fighting hard |
| `Idle ignition correction` | timing bump for idle recovery |
| `Idle effective DC` | final output to IAC/throttle |

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
| `VVT CAM1 status` | 0=OK, non-zero = error (cam not following target) |

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

### Boost overshoot

Signature: `Boost` spikes above `Boost Target`; `Boost out of margin` = 1.

Check: `Boost PID correction` — high values mean the PID gains are too aggressive. Also check if `Boost DC` is saturating (0% or 100%) before the spike.

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
| `Idle state` | 0 | Idle control off |
| `Idle state` | 2 | PID active |
| `Idle state` | 4 | Recovery/forced open loop |
| `Lambda is valid` | 0 | WBO not ready (no trim) |
| `Lambda is valid` | 1 | WBO validated (trim active) |
| `Overrun status` | 1 | Overrun condition met (check `Overrun fuel corr.` for actual cut) |


