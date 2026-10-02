# Idle airflow requirement binned by oil pressure — measured RPM × CLT tables (2026-08-05)

**Question.** For each oil-pressure bin {2, 3, 4, 5, 6} bar, how much idle airflow % was
actually sustaining the engine at a given RPM and coolant temperature?

**Relation to the rest of the oil work.** This is the *raw measurement layer* under
[oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md) — no model, no correction
subtracted, no base-table decomposition. Every number here is a logged total. The fitted
`corr(N,P)` tables and the `idleActiveAirflow` v2 proposal live in that note; this one only
says what the car did. Sensor cal and the RPM×CLT pressure baseline:
[`../../notes/oil_pressure.md`](../../notes/oil_pressure.md).

Reproduce: `supra/notes/oil_pressure_airflow/build_tables_v2.py` →
`tables.md`, `cells.csv`, `cells_by_idle_target.csv`, `pooled_samples.csv` in that folder.

---

## Method

**Log window.** CSVs with mtime 2026-06-05 … 2026-08-05 (the requested two months) in
`C:\Users\WTCra\Desktop`, `EMU_BLACK_V3\Supra`, `…\LogAutosave`, `supra/logs/`, `supra/tunes/`.
**Logs without an `Engine oil pressure` column are not read at all.**

| log | rows | usable | note |
|---|---|---|---|
| `Cold oil reference` (08-02) | 13,419 | **7,125** | CLT 28→102 cold start, 9.3 min |
| `oil compensation test with hot restart and varied hot idle targets` (08-04) | 16,706 | **3,142** | **the idle-target sweep** — targets 900→2000, CLT 27→103, OP 1.88–7.50. Fills the 1000 and 1500 rows |
| `oil data after 25 minutes` (08-02) | 11,935 | **2,770** | deep-soak hold, OP 1.81–2.44 — the 2-bar anchor |
| `20260613_1141` (06-13) | 17,298 | **1,520** | cold start + drive + hot restart |
| `cold idle dip again 3 all channels` (06-26) | 1,120 | **81** | CLT 75–99, 45 s |
| `died_hot_return_to_idle_again`, `cold idle dip again`, `crank_fail_0729` | — | 0 | no sustained idle-active / engine never ran |
| `key_data` (08-02) | 17,199 | **dropped** | bit-identical column subset of `20260613_1141` |
| `oil compensation test`, `…with hot restart` (08-04) | 16,354 / 16,706 | **dropped** | same session as the varied-target log, which is the 12-column superset (the only one carrying `Idle target`) |
| `oil temp data` (08-02) | — | not read | no oil-pressure column |

**Pooled: 14,638 gated samples from 5 logs = 9.8 min of held idle; 14,409 land in the tables** (229 fall outside the RPM axis span — see *Binning* below).

**Sample gate** — each surviving sample is one observation of "this much air is holding this
RPM at this CLT and this oil pressure":

- `Idle state == 2` (ACTIVE). Only here does the idle controller own the throttle and
  `Idle air %` equal the full commanded airflow.
- `MAP < 60` kPa, `Engine oil pressure status == 1`, `AC Clutch == 0`, `RPM > 400` (the last
  two only where logged).
- Entry age > 15 s into the current uninterrupted idle-active run.
- **`|RPM − Idle target| ≤ 50`** — Will's envelope, 2026-08-05. See the envelope section below
  for what this costs versus the σ(RPM) criterion it replaced.

**Cell value = median total `Idle air %`** = `idleActiveAirflow(CLT,target) + 13·fan +
idleCustomCorrection + PID`. **This composition is exact, verified on 11,496 samples**: the
residual `air − base − custom − PID` is **+0.15 with the fan off and +13.19 with it on**
(§ *Implied base cell*). Scalars from `supra/tunes/supra 06132026.xml.emub3`:
`idleCoolantFanCorr = 13`, `idleDBWTargetMin/Max = 2.4 / 8.0 %`,
`idleAirPIDOutMin/Max = −6 / +15` (the August logs rail at **−10**, so the floor was widened
after that export).

**Fan imputation.** The three 08-04 `oil compensation test` exports omit `Coolant fan`. It is
imputed only where the logs that carry it leave no doubt — measured engage share is **0.000 at
CLT ≤ 75** (n=4,326) and **0.999 at CLT ≥ 95** (n=6,172). The 75–95 band is genuinely mixed
(0.09 → 0.75) and stays NaN, dropping out of the fan-removed table rather than being guessed.
The tune says `coolantFanActTemp = 70` / `coolantFanHyst = 7`, but the observed switch sits
nearer 80 — trust the measurement.

**Binning: nearest bin on all three axes.** RPM outside [950, 1562.5] is dropped, not clamped —
229 samples, all from the target sweep's 900 rpm and >1600 rpm excursions.

---

## The tables

Cell = median total commanded airflow %, RPM = **actual RPM held**.
**†** = the airflow PID sat on its negative rail for > 20 % of the cell: the loop wanted *less*
air and had no authority left, so that cell is an **upper bound**.

### 2 bar — actual OP 1.81–2.50, median 2.12 — n = 3,271

| RPM ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | — | — | — | — | — | — | — | — |
| **1375** | — | — | — | — | — | — | — | — |
| **1200** | — | — | — | — | — | — | **28.5†** | 28.0† |
| **1100** | — | — | — | — | — | — | 24.5 | 26.5† |
| **1000** | — | — | — | — | — | — | **21.5** | 21.0 |

n = 2,593 / 302 / 143 / 3 / **229** / 1. The deep-soak column, and the one that reproduces
oil_viscosity_idle_airflow Result 7 exactly (26.5–28.5 total at 2.06–2.12 bar).

### 3 bar — actual OP 2.56–3.50, median 3.06 — n = 1,275

| RPM ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | — | — | — | — | — | — | 47.5 | — |
| **1375** | — | — | — | — | — | — | 43.0 | — |
| **1200** | — | — | — | — | — | 44.0 | 38.8 | 33.0 |
| **1100** | — | — | — | — | — | — | 25.0 | — |
| **1000** | — | — | — | — | — | — | — | — |

n = 67 / 375 / 7 / 792 / 5 / 29. The 1200/96 IQR is wide (34.0–43.5) — it mixes the 06/13
post-restart with the soak tail.

### 4 bar — actual OP 3.62–4.50, median 4.25 — n = 2,107

| RPM ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | — | — | — | — | — | — | — | — |
| **1375** | — | — | — | — | — | — | — | — |
| **1200** | — | — | — | — | — | 66.2 ⚠n=2 | **37.0†** | 36.5† |
| **1100** | — | — | — | — | — | — | 34.0† ⚠n=6 | — |
| **1000** | — | — | — | — | — | — | — | — |

n = 2 / 2,093 / 6 / 6. Only 1200/96 is real; 72 % PID-railed.

### 5 bar — actual OP 4.62–5.50, median 4.88 — n = 2,035

| RPM ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | — | — | — | — | — | — | — | — |
| **1375** | — | — | — | — | — | — | — | — |
| **1200** | — | — | — | — | — | 32.5 | **37.0†** | — |
| **1100** | — | — | — | — | — | 29.0 ⚠n=2 | 31.0† | — |
| **1000** | — | — | — | — | — | — | — | — |

n = 207 / 1,788 / 2 / 38.

### 6 bar — actual OP 5.62–**7.62**, median **6.88** — n = 5,721

| RPM ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | — | — | **77.5** | **72.5** | 61.0 | — | — | — |
| **1375** | — | — | 58.0† | 49.5† | — | — | — | — |
| **1200** | — | — | — | 41.5† | 34.5 | 30.5 | 34.0 | — |
| **1100** | — | — | — | — | — | 29.0 ⚠n=8 | — | — |
| **1000** | — | — | — | — | — | — | — | — |

n = 118 / 787 / 25 / 947 / 717 / 505 / 1,054 / 1,433 / 127 / 8. The 1500 row is new — it comes
entirely from the 08-04 target sweep driving an elevated target during warm-up.

⚠ **Nearest-bin lumping puts everything ≥ 5.5 bar in this column.** Its true centre is
**6.88 bar** and it reaches 7.62 — cold-start pressure, not 6 bar.

### Fan removed (−13 where the fan is on) — engine-only requirement

| RPM ＼ CLT (2 bar) | 96 | 105 |
|---|---|---|
| **1200** | 15.5† | 15.0† |
| **1100** | 11.5 | 13.5† |
| **1000** | **8.5** | 8.0 |

6 bar is fan-off throughout the cold columns, so that table is unchanged except 1200/96
(34.0 → 27.5) and 1200/75 (30.5, 9 % fan). Full set in `tables.md`.

---

## Implied `idleActiveAirflow` cell — what the base table should have read

Because the composition is exact, the base-table cell the engine actually wanted can be
back-solved per sample: **`implied = Idle air % − 13·fan − custom − PID`**. Validated first on
the logs that carry `Coolant fan` (residual +0.15 fan-off, +13.19 fan-on — the model closes to
±0.2), which also confirms `idleCoolantFanCorr = 13` empirically.

Against the shipped table decoded from `supra 06132026.xml.emub3` (bilinear on CLT × target):

| bin | rpm | CLT | n | total air | **implied** | IQR | shipped | Δ |
|---|---|---|---|---|---|---|---|---|
| 2 | **1000** | 96 | 229 | 21.5 | **19.2** | 19.0–19.5 | 16.5 | **+2.8** |
| 2 | 1100 | 96 | 143 | 24.5 | 22.4 | 21.9–22.8 | 21.5 | +0.9 |
| 2 | 1200 | 96 | 2,593 | 28.5 | **26.5** | 26.5–27.0 | 26.5 | **0.0** |
| 2 | 1200 | 105 | 302 | 28.0 | 26.5 | 26.5–27.0 | 26.5 | 0.0 |
| 3 | 1200 | 96 | 792 | 38.8 | 26.9 | 26.4–27.8 | 26.5 | +0.4 |
| 3 | 1375 | 96 | 375 | 43.0 | 34.5 | 31.9–35.0 | 36.0 | −1.5 |
| 3 | 1500 | 96 | 67 | 47.5 | 37.5 | 37.1–37.9 | 40.0 | −2.5 |
| 4 | 1200 | 96 | 2,059 | 37.0 | 33.5 | 27.0–34.0 | 26.5 | +7.0 |
| 5 | 1200 | 96 | 1,474 | 34.0 | 26.2 | 25.9–28.1 | 26.5 | −0.2 |
| 6 | 1200 | 45 | 505 | 41.5 | 46.1 | 45.8–46.6 | 44.9 | +1.2 |
| 6 | 1200 | 60 | 1,054 | 34.5 | 34.4 | 33.5–40.6 | 36.4 | −2.0 |
| 6 | 1200 | 75 | 1,433 | 30.5 | 32.0 | 31.8–32.2 | 32.0 | **0.0** |
| 6 | 1375 | 30 | 947 | 58.0 | 68.0 | 61.5–70.0 | 56.6 | +11.4 |
| 6 | 1375 | 45 | 717 | 49.5 | 52.6 | 51.6–58.0 | 52.1 | +0.4 |
| 6 | 1500 | 30 | 118 | 77.5 | 49.3 | 48.9–49.8 | 57.3 | −8.1 |
| 6 | 1500 | 45 | 787 | 72.5 | 45.8 | 44.4–47.1 | 53.2 | −7.4 |
| 6 | 1500 | 60 | 25 | 61.0 | 40.2 | 39.5–40.8 | 48.0 | −7.8 |

Readings:

- **The hot 1200 cell is dead-on** — implied 26.5 vs shipped 26.5, IQR 0.5 wide, n=2,593.
  Nothing to change there.
- **1000 rpm / 96 °C implies 19.2 (IQR 19.0–19.5), against a shipped 16.5.** Will's independent
  figure of **18 %** lands inside 1.2 points of the measurement and on the same side of the
  shipped value. The row wants roughly **+2.8**.
- **The 1500 row is 7–8 below the shipped cold cells** across three CLT columns with consistent
  sign and tight IQRs — the first measured evidence on that row, previously pure extrapolation.
- **1375 / 30 implies +11.4**, but that cell is 62 % PID-railed (the loop was on its −10 floor
  with the integral still draining), so it reads high — consistent with the
  oil_viscosity_idle_airflow Result 8 §6 warning about the cold anchor.
- **4 bar / 1200 / 96 implies +7.0 with a bimodal IQR (27.0–34.0)** — the path-dependence again,
  not a single-valued cell.

## The RPM envelope, and why the 1000 rpm row cannot be filled (2026-08-05, Will's challenge)

Directive: *"your envelope for acceptable RPM is too small — open it up to ±50 of target."*
Implemented as `gate(mode=...)`; all three variants are on disk
(`tables.md` / `tables_target50.md` / `tables_either.md`).

**The original gate never had a target-proximity test at all.** It required RPM to be *not
moving* (rolling σ < 25 rpm over ±1 s) — a torque-balance criterion — and binned on actual RPM,
so a steady 1150 with a 1200 target was a legitimate observation of the 1100 cell. Adding
`|RPM − Idle target| ≤ 50` therefore **narrows** the set, it does not open it:

**With the 08-04 target-sweep log in the set** (n per bin 2/3/4/5/6 bar):

| envelope | binned n | cells | n<1050 rpm | 2 bar | 3 bar | 4 bar | 5 bar | 6 bar |
|---|---|---|---|---|---|---|---|---|
| σ < 25 (physics) | 16,815 | **40** | 339 | 28.0 | 42.0 | 37.0 | 34.5 | 37.5 |
| **\|RPM−tgt\| ≤ 50 (shipped)** | **14,409** | **30** | **229** | **28.0** | **42.5** | **37.0** | **37.0** | **41.5** |
| either (widest) | 18,427 | **40** | 360 | 28.0 | 42.0 | 37.0 | 34.5 | 37.5 |

The ±50 envelope still costs **10 of 40 cells** and moves the 5- and 6-bar medians up 2.5–4
points (it drops the steady-but-below-target samples, which are the low-airflow ones). It is
shipped because it is what was asked for; `tables.md` is built with it, and the σ variant is
one environment flag away (`ENVELOPE=steady`).

Before that log arrived (2026-08-05 first pass, 3 logs, no held sub-1050 data anywhere):

| envelope | pooled n | cells with data | 2 bar | 3 bar | 4 bar | 5 bar | 6 bar |
|---|---|---|---|---|---|---|---|
| σ < 25 (physics) | 10,314 | **25** | 36.0 | 43.0 | 37.0 | 31.0 | 36.0 |
| \|RPM−tgt\| ≤ 50 (control) | 8,726 | 18 | 36.0 | 43.0 | 37.0 | 32.5 | 36.5 |
| either (widest) | 11,381 | 25 | 36.0 | 43.0 | 37.0 | 31.0 | 35.5 |

`±50 of target` costs seven cells — (2,1100,96), (3,1375,96), (3,1375,105), (5,1375,96),
(6,1100,60), (6,1100,96) and **(6,1200,30)**, the coldest 1200-row cell — because during a cold
warmup the target is elevated and RPM legitimately sits more than 50 below it while the loop
catches up. The union adds ~1,000 samples but **no new cells**. No cell value moves more than
1.5 points under any of the three. The envelope was never the binding constraint.

**In the ordinary logs, no envelope produces a single sample below 1050 rpm** — all 347
idle-ACTIVE samples under 1050 rpm there are **sags, not holds**:

| log | n < 1050 | how far below target | σ<25 | \|dev\|≤50 | entry age >15 s | airflow % |
|---|---|---|---|---|---|---|
| `20260613_1141` | 271 | −151 … −574 (med −232) | 37 | **0** | **0** | 39.5–50.5 |
| `cold idle dip again 3` | 24 | −224 … −562 | 0 | **0** | 0 | 47.5–56.0 |
| `died_hot_return` | 25 | −212 … −791 | 0 | **0** | 0 | 46.5–54.5 |
| `Cold oil reference` | 27 | −153 … −273 | 0 | **0** | 27 | 32.5–41.0 |

In those logs the idle target never goes below 1200, so the engine only *visits* 1000 rpm on
the way into a dip with the PID shoving 32–56 % airflow in to recover — anti-stall air, roughly
2.5× the requirement. **The rows were structurally unmeasurable from normal driving and needed a
deliberate idle-target sweep. That sweep is `oil compensation test with hot restart and varied
hot idle targets` (2026-08-04, targets 900 → 2000), which is exactly what fills the 1000 and
1500 rows above with held data at PID −7.4 (free, floor −10) rather than recovery transients.**
Note the sweep's own held 1000-rpm samples pass the ±50 envelope easily — median |RPM − target|
is under 10 — so the envelope was never what excluded them; the absence of a 1000 rpm *target*
was.

### 1000 rpm / 2 bar / 96 °C — now measured

`idleActiveAirflow` decoded from `supra 06132026.xml.emub3` — `storage="ubyte" width="8"
height="5"`, **scale 0.5, rows stored low-RPM-first**, bytes
`82 6C 50 39 31 28 21 21 | 95 7C 5C 47 3D 33 2B 2B | A2 89 69 55 48 3E 35 35 | AC 8C 76 65 58 4E 46 46 | AF 96 7C 68 5F 57 50 50`:

| tgt ＼ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 75.0 | 62.0 | 52.0 | 47.5 | 43.5 | 40.0 | 40.0 |
| 1375 | 86.0 | 70.0 | 59.0 | 50.5 | 44.0 | 39.0 | 35.0 | 35.0 |
| 1200 | 81.0 | 68.5 | 52.5 | 42.5 | 36.0 | 31.0 | 26.5 | 26.5 |
| 1100 | 74.5 | 62.0 | 46.0 | 35.5 | 30.5 | 25.5 | 21.5 | 21.5 |
| 1000 | 65.0 | 54.0 | 40.0 | 28.5 | 24.5 | 20.0 | 16.5 | 16.5 |

(Matches Will's on-screen table in every cell except 1500/75 — 43.5 here vs 45.5 on screen — so
**the live table is newer than this export**; get a current XML before programming from it.)

Shipped row delta 1200 → 1000 at CLT 96 is **−10.0**. Applying it to the nearest measurement
(2 bar / 1200 / 96, n=28, fan on: **36.0 total / 23.0 fan-removed**) extrapolates to
**≈26 total / ≈13 fan-removed** at 1000 rpm. Will's stated 18 % sits between those two, so the
fan convention decides whether it is high or low — a 13-point question, larger than the
disagreement itself. The deep-soak anchor in oil_viscosity_idle_airflow Result 7 (26.5–28.5
total at 2.06–2.12 bar, fan on → 13.5–15.5 fan-removed at 1200) extrapolates lower still.
**None of this is a measurement**: the 2-bar column is 1.1 s of data and the row shape is
inherited from the shipped table, not observed. A held 1000 rpm target at soak settles it.

## Gaps and what closes them

- **2-bar bin (n=31).** The deep-soak anchor log named in Result 7 —
  `oil data after 25 minutes.csv`, 8.1 min of post-drive idle hold at 1.69–2.44 bar, n≈3,935 —
  is **not in `EMU_BLACK_V3\Supra`, `…\LogAutosave`, or `supra/logs/`**. It is the single
  highest-value addition to this analysis; ask Will where it went rather than re-deriving.
- **Widening the window past two months** adds seven more oil-pressure-bearing logs, all with
  `Idle state`, `Idle air %` and `Coolant fan`: `20260524_1301`, `drivehome`,
  `new_fuel_strategy`, `drive_wobble` (05-24…05-30), `all-channels-reduced-idlaircorr`,
  `all-channel-reference` (05-31), `hood on 0509 terrible day` (05-31, 86 MB). Those carry the
  hot-soak idle that the 2-bar column needs. Note they predate the `idleAirPIDOutMin`
  −6 → −10 change and several base-table revisions.
- **0 / 15 °C columns** need a genuinely cold morning start; nothing colder than 28 °C exists.
- **1000 / 1500 rpm rows** need a deliberate idle-target sweep, since normal operation never
  holds those speeds.
- **Rail-censored cells (†)** need a re-log after the base table is re-leveled, so the PID is
  regulating freely and the reading is a demand rather than a ceiling.

## Supersedes

`oil_pressure_airflow/oil_press_*bar_{table,n}.md` + `oil_press_points.csv` /
`oil_press_log_summary.csv` (earlier same-day pass). Its values agree closely where they
overlap, but it **included `key_data.csv` alongside `20260613_1141`**, double-weighting that
session — visible as roughly doubled n in the 6-bar 1375 row (2,135 vs 1,084) — and its
proxy-mode gate for that column-reduced file admitted samples with no `Idle state` check,
which is where its otherwise-unsupported 3-bar 1000/1100/1500 rpm rows come from.
