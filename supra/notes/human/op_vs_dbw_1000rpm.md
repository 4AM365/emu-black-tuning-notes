# Running dataset — oil pressure vs DBW duty at ~1000 rpm

> Digest of [op_vs_dbw_1000rpm.md](../op_vs_dbw_1000rpm.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the re-runnable file Will asked for on 2026-09-19 — every log with oil pressure + `DBW Out. DC`, gated to idle-active, ~1000 rpm, ignition 17–19°, binned by oil pressure. Script, samples, big table and a four-panel scatter live in `supra/notes/op_vs_dbw_1000rpm/`.

**The rules:**

- Re-run `running_op_vs_dbw.py` after dropping a new log in `EMU_BLACK_V3\Supra`, `misc log csv`, `LogAutosave`, `supra/logs` or `supra/tunes`. Logs without `DBW Out. DC` are skipped (most of the August oil-study exports).
- **`DBW Out. DC` has no relationship to oil pressure.** Every OP bin spans −40 → 0; the medians are whichever log and `dbwMinDC` dominate that bin.
- **`Idle air %` clusters by tune era**, not by OP — it is a position command through a range that has been re-cut several times.
- **`TPS` organises by OP within a day** (~1 % TPS between 1.7 and 3.8 bar) but shifts ~1.5 % between April and September.
- **`MAP×RPM` — the air the engine actually took — is flat and repeatable:** 35–40 k in every log since April, ~7 % higher with cold oil. That is the whole friction term; everything else is actuator and calibration.
- The ignition window assumes the hot idle ignition target is ~18°; if that target moves, move the window.

**Key numbers:** first run 5,829 samples, 13 logs, 2026-04-08 … 2026-09-19.

**When to care:** any time oil pressure is proposed as an axis for a duty or airflow correction — this file shows what it does and does not predict.
