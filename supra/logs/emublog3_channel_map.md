# EMU Black `.emublog3` channel map (Supra)

Running decode of the raw internal log channels EMU Black writes to `.emublog3`.
Built up gradually — add a row whenever a channel's identity is confirmed.

## Channel index (from EMU "Select logged parameters" decoder)

The CSV export header renames these to friendly labels, but the firmware channel
indices are:

Log "Analog N" maps directly to ECU **Analog input N**. Identities below are
**confirmed from the EMU "Inputs assignment" screen** (2026-06-04).

| Channel | Export header | EMU input | Identity (confirmed) |
|---------|---------------|-----------|----------------------|
| #0 | RPM       | —              | Engine RPM |
| #1 | Gear      | —              | Calculated gear |
| #2 | TPS       | —              | Throttle position (%), EMU-calibrated |
| #3 | Analog 1  | Analog input 1 | **Unassigned** (reads ~4.98 V pulled-up) |
| #4 | Analog 2  | Analog input 2 | **TPS main signal** (throttle voltage; corr +0.999). NB: the ECU's dedicated TPS pin carries **PPS** (pedal), so the throttle's main signal lives here on Analog 2 |
| #5 | Analog 3  | Analog input 3 | **Unassigned** (reads ~4.98 V pulled-up) |
| #6 | Analog 4  | Analog input 4 | Assigned to logic **Fn 3, Fn 5, Fn 6** (reads 4.980 V flat) |
| #7 | Analog 5  | Analog input 5 | **Fuel pressure sensor** (not MAP — tracks TPS via load/MAP-referenced rail pressure) |
| #8 | Analog 6  | Analog input 6 | **Unassigned** (reads 0.000 V) |

CAN analog inputs (not in this 6-analog export, but assigned in the ECU):
CAN 3 = custom temp 1, CAN 4 = pre-throttle boost, CAN 5 = oil pressure,
CAN 6 = back pressure; CAN 1–2 and 7–12 unassigned.

Free local analog inputs for new sensors: **Analog input 1, 3, and 6.**

## TPS-corollary analysis (`analog_signals.csv`, export of `test-run.emublog3`)

Question: is the Lexus DBW throttle's secondary opposing-direction half-voltage
confirmation signal still wired to an analog input?

**Finding: no opposing-direction confirmation signal is present in this log.**
Nothing tracks *inversely* with TPS — every moving channel rises with throttle.
The redundant sub-TPS appears to have been removed or repurposed (consistent with
the input being borrowed for something else).

Two channels move with TPS; the transient test distinguishes them:

| Channel | corr vs TPS | Range (this log) | Extrap. full-travel | Transient behavior | Verdict |
|---------|-------------|------------------|---------------------|--------------------|---------|
| Analog 2 | **+0.999** | 0.843–1.255 V | ~0.68 V @0% → ~4.3 V @100% (≈3.63 V span) | snaps *instantly* with each TPS step | **Throttle position voltage** (raw VTA, main — full-swing, same direction) |
| Analog 5 | +0.974 | 1.745–1.980 V | ~1.69 V @0% → ~3.35 V @100% (≈1.66 V span) | only ~12 quantization steps over whole log | **Fuel pressure sensor** (confirmed from pinout) — correlates with TPS because rail pressure follows load/MAP, not a throttle sensor |

So Analog 2 is the only throttle-position analog in the log: **same-direction,
full-swing** main throttle voltage (0.68–4.3 V). Analog 5's correlation was a
load artifact — fuel pressure rising with manifold pressure as throttle opens.

Bottom line: the opposing-direction secondary TPS safety signal is **not currently
wired**. Three local analog inputs are free for it — **Analog input 1, 3, and 6**
(plus many free CAN analog inputs). No need to reclaim anything.

## Plan: swap to a Bosch DBW throttle body for redundant TPS

EcuMaster EMU Black does not accept the Lexus/Toyota secondary throttle sensor
(VTA2 is a same-direction *offset* signal, not the mirrored pair EMU's TPS2
plausibility check expects). Plan is to fit a **Bosch DBW throttle body**, whose
two sensors are mirrored/opposing (TPS1 rises ~0.5→4.5 V, TPS2 falls ~4.5→0.5 V) —
the relationship EMU Black natively validates — to get the secondary as a real
safety/limp input.
