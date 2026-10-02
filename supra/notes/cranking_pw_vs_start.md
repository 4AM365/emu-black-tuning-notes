# Cranking injector PW vs time to start — running record

Every cranking event in the Supra CSV logs (`EMU_BLACK_V3\Supra`, incl. `misc log csv`, `LogAutosave`), regenerated
by [`cranking_pw_vs_start/scan_crank_events.py`](cranking_pw_vs_start/scan_crank_events.py) (raw rows in
`cranking_pw_vs_start/crank_events.csv`). Append new starts by re-running it. Chart:
[`pw_vs_start_by_clt.png`](cranking_pw_vs_start/pw_vs_start_by_clt.png) from `plot_pw_vs_start.py` — average PW
(mean of the first-1 s and last-0.5 s values; cranking PW falls roughly linearly, Will 2026-10-02) vs time to
start, one panel per CLT bin, cranks after the 06-29 injector deadtime update only.

Logging gaps: a lone pre-gap sample followed by a > 1 s gap means the crank began after the gap, so the clock
starts there (fixed 2026-10-02; it had inflated 08-06, 08-16 @ 596, 08-24, 09-19 and 09-29).

**Definitions.** Crank = `ECU State` 2 span (logs without that channel: RPM > 0 after ≥ 1 s at 0, until 450). All
times from the **first injector pulse** (excludes sync and pump-start delay). *Start* = first fuel → RPM ≥ 750, the
current `crankingThreshold`; older starts exited Cranking earlier (400 through 06-29, 500 on 09-15…09-29) and ran
the rest on ASE, so their time includes some afterstart. PW in ms; (net) = PW − `Injectors cal. time`. "End" = last
0.5 s of the crank. Fuel per cycle follows net PW (rail 3.8–4.0 bar in every row that logs it). Duplicate logs
(`50hz log wont_idle`, `goodrunwithvoltage`) dropped. n/l = not logged.

| Date | Log @ t (s) | CLT | E % | PW first 1 s (net) | PW end (net) | Cranking corr. first → end | First fuel → 750 | Notes |
|---|---|---|---|---|---|---|---|---|
| 05-31 | all-channels-reduced-idlaircorr @ 91 | 29 | 25 | 4.55 (3.11) | 3.90 (2.53) | +59 → +40 | 2.40 | |
| 05-31 | hood on 0509 @ 80 | 96 | 56 | 3.52 (2.08) | 3.52 (2.08) | 0 → 0 | 0.44 | |
| 05-31 | hood on 0509 @ 1871 | 96 | 56 | 3.62 (2.19) | 3.62 (2.19) | 0 → 0 | 0.60 | |
| 05-31 | hood on 0509 @ 1896 | 96 | 56 | 3.39 (1.99) | 3.30 (1.93) | −1 → −2 | 2.16 | |
| 06-13 | 20260613_1141 @ 306 | 91 | 25 | 3.05 (1.62) | 3.05 (1.62) | +1 | 0.60 | |
| 06-28 | died_hot_return_to_idle_again @ 2791 | 96 | 25 | 2.95 (1.56) | 2.95 (1.56) | −2 | 0.28 | |
| 07-29 | crank_fail_0729 @ 9 | 36 | 25 | 2.58 (1.22) | 3.85 (2.43) | −62 → +28 | no start | pedal in (TPS 25) |
| 07-30 | hotcranx @ 531 / 550 / 598 | n/l | n/l | 2.82–2.84 | 2.45–2.75 | −11 | no start | cranks of 2.4 / 4.5 / 7.4 s |
| 07-30 | hotcranx @ 779 | n/l | n/l | 2.94 | 2.94 | −9 | 0.44 | |
| 07-30 | varied_cranking_airflow @ 10 / 78 / 104 | n/l | n/l | 4.44–5.18 | 3.55–3.65 | +51…+59 → +30…+41 | no start | 2.0–3.4 s cranks |
| 08-06 | 0806 rich cranks × 6 | n/l | n/l | 2.65–2.98 (1.27–1.57) | 2.46–2.60 (1.18–1.25) | n/l | no start | 0.8–10.6 s cranks; one with pedal |
| 08-06 | idle bounce 2 @ 32 | 35 | n/l | 3.17 | 3.96 | n/l | 1.80 | |
| 08-12 | wont_idle @ 139 | 92 | n/l | 2.63 | 2.59 | n/l | 1.16 | |
| 08-12 | wont_idle @ 202 | 91 | n/l | 2.51 | 2.17 | n/l | no start | 10 s crank |
| 08-12 | wont_idle @ 474 / 543 / 565 / 572 / 598 | 92–95 | n/l | 2.12–4.72 | 2.09–4.81 | n/l | 0.64–0.84 or none | pedal in — mask |
| 08-12 | wont_idle @ 701 | 95 | n/l | 2.76 | 2.76 | n/l | 0.40 | |
| 08-16 | goodrun @ 33 | 34 | n/l | 3.33 | 3.19 | n/l | 2.16 | |
| 08-16 | goodrun @ 596 | 35 | n/l | 3.25 | 3.25 | n/l | 0.52 | |
| 08-24 | cranking_channels_recent_run @ 3 | n/l | n/l | 2.92 | 3.24 | −9 → 0 | 2.12 | |
| 08-24 | omg @ 76 | 38 | 14 | 2.84 (1.49) | 2.39 (1.14) | −13 → −26 | 3.68 | |
| 09-19 | fullchannels @ 715 | 51 | 14 | 2.49 (1.23) | 2.45 (1.20) | −24 → −23 | 1.12 | |
| 09-29 | allchannels_smoothclt @ 83 | 26 | 14 | 3.52 (2.13) | 3.38 (2.01) | +11 → +8 | 1.32 | exit at 500 |
| 10-01 | new_cranking_rules @ 4 | 27 | 14 | 3.15 (1.77) | 2.33 (0.98) | −4 → −47 | no start | hovered 300–480; pedal at the end |
| 10-01 | new_cranking_rules @ 99 | 27 | 14 | 3.38 (1.98) | 3.38 (1.98) | +11 | **0.40** | ports wet from the attempt before |
| 10-02 | newcoldstart @ 1117 | 29 | 14 | 3.47 (2.04) | 2.17 (1.12) | +10 → −17 | **7.48** | 5.6 s lean hover |
| 10-02 | newhotstart @ 2476 | 96 | 14 | 2.81 (1.41) | 2.71 (1.35) | −9 → −8 | 1.08 | all of the −9 is anti-flood |
| *proposed* | 10-02 cold, same MAP/voltage | 29 | 14 | 3.90 (2.47) | 2.81 (1.75) | +36 → +30 | — | anti-flood fixed + floor tables |
| *proposed* | 10-02 hot, same MAP/voltage | 96 | 14 | 3.12 (1.72) | 2.99 (1.63) | +10.5 | — | |

**What the record shows (2026-10-02).**
- Time to start follows the **end-of-crank** dose, not the first second. Cold (26–38 °C): end net ≈ 2.0–2.5 ms →
  0.4–2.4 s; end net ≈ 1.1 ms → 3.7–7.5 s (08-24, 10-02) or no start (10-01 #1). First-second net was ~2 ms in both
  groups.
- Hot (91–96 °C): net 1.56–2.19 → 0.28–0.60 s; 10-02 at 1.41 → 1.08 s. Ethanol differs (E14–E56); E25 vs E14 needs
  only ~3 % more fuel for stoich, so it does not explain the gap.
- The proposed end dose, 1.75 ms net at the 10-02 hover MAP (74 kPa), is ≈ 2.1 ms at 90 kPa — inside the fast
  cold group. Proposed hot (1.72) sits above the fast hot group's floor.
- Rich is not fast: the July `varied_cranking_airflow` cranks ran +51…+59 % and did not start, and `0806 rich
  cranks` failed six times. Too much is as bad as too little; see `notes/engine_start.md` on plug fouling.
- Confounds: VE basis and injector deadtime changed over the summer (06-29 deadtime rescale, 06-30 VE ×1.1547,
  10-01 VE −5 points), CLT is not logged in the July/August rows, and older starts exited Cranking below 750.

## Fouling-era doses (added 2026-10-02)

Pressure-corrected net PW per injection (× √(rail/4 bar)) and liquid fuel per crank (3 injections/rev, 1230 cc/min,
0.75 g/cc). The cranks that first fouled the plugs (07-28) are not logged; the logged ones below ran on plugs
already wet, so they show the dose that kept them drowned, with zero fires.

| Crank | Net PW / injection | Cranking corr. | Fuel per crank | Fires |
|---|---|---|---|---|
| 07-29 crank_fail (CLT 36) | 2.47 ms | ≈ +30 % (table +71 % at rev 1) | 1.3 g in 4.6 s | none (EGT flat) |
| 07-29/30 varied_cranking_airflow × 3 | 2.63–2.77 ms | +40…+53 % | 0.8–1.25 g each | none |
| 08-06 rich cranks × 7 | 1.2–1.5 ms | (base only) | ≈ 3.6 g total | none — plugs already fouled |
| clean cold catches 09-29, 10-01 #2 | 2.03–2.08 ms | +10 % | 0.2–0.4 g | caught |
| 10-02 cold (7.4 s hover) | 2.04 → 1.12 ms | +10 → −17 % | 3.1 g | firing (EGT +51 °C) |

The 10-02 hover put in more fuel than any fouling crank but burned it. Fouling is fuel in while nothing fires.
The first draft of the 10-02 floor tables would have put 2.47 ms into the first second of a cold crank, the 07-29
level; the revision keeps rows 1/3/7 at the dose that caught cleanly (see `log_2026-10-02_cold_hot_start.md`).

## Delivered fuel per injection (mg) — the comparison that matters (Will, 2026-10-02)

Tables are not comparable across VE, deadtime, voltage and rail pressure; delivered fuel is. mg = (PW − `Injectors
cal. time`) × 1230 cc/min × √(ΔP/400 kPa) × density (E-blended). Now a column in `crank_events.csv`.

| Group | mg / injection | Result |
|---|---|---|
| Cold clean catches: 10-01 #2 (27 °C), 09-29 (26 °C) | 30.8, 33.0 | 0.4 s, 1.3 s |
| 05-31 (29 °C, pre-deadtime-update) | 43.8 → 35.7 | 2.4 s — more fuel, not faster |
| 10-02 cold (29 °C) | 31.8 first second → 17.1 at the end | 7.5 s hover |
| 08-24 (38 °C), 10-01 #1 (27 °C) | 22.8 → 17.3; 27.5 → 15.2 | 3.7 s; no start |
| Fouled-plug cranks 07-29/30, 08-06 | ≈ 38–43; 20–24 | no fires (plugs already wet) |
| Hot restarts 06-13, 06-28 (E25), 05-31 (E56) | 22.8, 23.9; 28.5–31.4 | 0.3–0.6 s |
| 10-02 hot (E14, −9 % anti-flood) | 21.9 | 1.08 s |

Cold light-off dose ≈ 31–33 mg/injection at cranking MAP; ~44 mg did not light faster; a tail that decays to
~15–17 mg hovers or fails. Hot: ≈ 23–24 mg (E14-equivalent) restarts in under 0.6 s; with the anti-flood fix the
10-02 hot crank at 0 % would get ≈ 24 mg.
