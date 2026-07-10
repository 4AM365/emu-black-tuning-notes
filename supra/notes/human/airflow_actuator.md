# Airflow / idle DBW calibration reference

> Digest of [airflow_actuator.md](../airflow_actuator.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the live state of the idle DBW system — actuator range, airflow tables, PID gains — and the rescale rules to reapply whenever the range changes.

**The rules:**

- Actuator range is **[2.4%, 8.0%] TPS** (width 5.6): `TPS% = 2.4 + airflow%/100 × 5.6`. Was 3.5–8.0; original 2.0–6.4.
- Encodings: ubyte airflow tables are 0.5%/count (raw = 2× displayed); `idleDBWTargetMin/Max` are 0.1/count; `idleCustomCorrection` is signed 1:1 and currently **additive**.
- When the range changes again: absolute tables (Active, Armed) get the offset+ratio formula to preserve real TPS; additive corrections and PID gains/limits just scale by width ratio; cranking is set fresh to the target TPS, keeping the taper shape.
- PID gains were scaled ×4.5/5.6 for the wider range (`idleAirFlowKP` 1646, `idleAirFlowKI` 165). They're starting points — hunts means trim down, sluggish recovery means nudge up.
- Cold-crank cell = 13.0% airflow = 3.13% TPS — the cold-crank vacuum anchor.
- The XML export is a reference snapshot only; make actual changes in EMU.

**Key numbers:** warm (96 °C) active airflow 31.5–65% across 1000–1500 rpm targets; integral limits −6/+8; PID output −8/+10; `idleCustomCorrection` reaches −40% at IAT 70 / 1000 rpm.

**When to care:** any time you touch the actuator range, idle airflow tables, or the airflow PID. Last updated 2026-05-22 — keep it current.
