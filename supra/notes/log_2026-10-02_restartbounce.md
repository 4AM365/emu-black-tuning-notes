# Log `restartbounce.csv` (2026-10-02): A/C relay cycle after a hot restart

Source: `EMU_BLACK_V3\Supra\restartbounce.csv` (0–2801 s). Key cycle at 1947.8–1954.4 (`ECU Reset`), restart 1955.5,
CLT 98. A/C request (`Switch 1`) was on at key-on. 27 `Data changing` spans. Airflow PID gains recovered from
`Monitored P term` ÷ `Idle ignition correction` and dI/dt ÷ ign: **KP 1.0 / KI 0.5 through ~2110, KI 1.0 from 2110,
KP 0.5 / KI 0.5 from ~2440–2449.** The restart ran KP 1.0 / KI 0.5, so the later edit changed only KP for this case.

## Restart (1955–1976)

1. Afterstart flare to 1862 on the held cranking airflow (same as `log_2026-10-02_cold_hot_start.md` §3). `Switch 1`
   returned at 1957.44; the clutch engaged `acTimeToEngage` later (1958.00) while still in Afterstart (`Idle state` 5,
   PIDs off), RPM falling ~1000 rpm/s through 1338. ACTIVE took over at 997, still falling. Trough 530.
2. Relay cycle, period ~1.7 s, 4 cycles: the RPM gate (`acMinRPM`, log-derived ≈ 800, no hysteresis) drops the clutch
   **and** the A/C custom airflow correction (+16) together at the trough → the gate re-arms ≈ 0.1–1 s later and the +16
   returns → the clutch follows `acTimeToEngage` (0.56 s) later, landing on the overshoot (1290–1620) with ignition on
   its retard limit (angle ≈ 10°, −7…−8) and the P term pulling ~8 air → RPM falls ~800 in 0.7 s back through the gate.
   Ignition sat flat at +17 / −8 in the troughs/peaks — both ends at their limits.
3. It ended when `Monitored I term` had climbed +3 → +9.6: troughs 530, 755, 758, 798, then 870 (above the gate).
   Clutch held; on target by ~1976.

## Fresh A/C engagements at steady hot idle (target 1025, PPS 0)

The custom correction enters with the request; the clutch follows `acTimeToEngage` later. In that gap RPM rises
~100–140, ignition retards ~6° and the P term removes ~5 of the +16, so the load lands on ≈ +11. Then one dip and one
overshoot, on target in 1.5–2.6 s.

| gains | engagements | trough | overshoot |
|---|---|---|---|
| KP 1.0 (KI 0.5 or 1.0) | 1576, 1698, 2288, 2343, 2418 | 802–832 | 1157–1292 |
| KP 0.5 / KI 0.5 | 2459, 2476, 2779 | 835–898 | 1165–1180 |

n = 3 for KP 0.5. Every steady trough lands within 0–100 rpm of the gate; one at KP 1.0 bottomed at 802.
Disengagement flare 1180–1280. No A/C-on restart exists at KP 0.5, so its effect on the restart case is untested.

## Gate trips (the whole log)

12 trips (clutch off with request on). Logged RPM at the trip is 800–840 (channel latency), so the effective trip is
≈ 815–840. Besides the 4 at the restart: 5 at standing idle, each on a fresh engagement that dipped straight through the
gate (494, 1253, 1486, 1575, 1722), and 3 on clutch-pedal return-to-idle (214, 224, 264). Re-engage 0.64–1.0 s later;
outside the restart the second engagement held. The post-trip bottom was 734–798. A trip sheds the +16 with the load, so
it is a transient relief only (net ≈ −1.8 air at steady state, from the 10-01 +14.2 need). There is no compressor-on
data below the gate. Lowest recoveries without A/C: 530 here, 455–586 on 09-29. `acMinRPM` has no hysteresis
symbol in the XML (only `acPressHyst`). Proposed to Will 2026-10-02: lower it to ≈ 650; raising it is useful only above
the idle target (= no A/C at idle). Any value from ≈ 900 up to the target trips nearly every engagement.

## After-start A/C inhibit (Will's proposal, 2026-10-02)

Will proposed gating A/C on ASE to make an after-start delay so that `acMinRPM` can stay put. `Engine runtime` is a
direct clock: whole seconds since the engine started, reset at a stall-and-restart with no key cycle (`newhotstart.csv`
1351 → 0). A function `Switch 1 is True AND Engine runtime > N` avoids coupling A/C timing to `aseTbl` (whose decay
moves with every ASE edit) and adds no fuel. Gate the **request** (`acActivation` → the function), not the clutch
output. The custom airflow correction follows the EMU's A/C state, so an output-side gate would add the +16 during the
inhibit with no compressor load. Unverified: whether `acActivation`'s list offers functions (the brake input uses one).
N: the hot start without A/C settled within ±60 of target at runtime 7 → N ≈ 8. The inhibit fixes the restart trigger
only; the standing-idle and return-to-idle trips at the current gate are unaffected.

## Engagement PID response: kP vs KD (2026-10-02)

At kP 0.5 the airflow P term adds +7 over the dip and removes 5–8 on the recovery, all through the air lag; that late
air is the overshoot. The ignition correction carries the fast part (−6.5 → +8.5). In 2779 the engine was already 80 rpm
above target on the feed-forward when the clutch landed, and it still dipped 270. So the engagement torque transient
(compressor spin-up and initial pumping) exceeds the steady +14.2 need; a static custom correction can't cover it.
Settled idle RPM sd is 11–15 at both kP 1.0 and 0.5, so steady wander no longer depends on kP. For the KD option and its
SNR at this transient, see `notes/idle.md` → Airflow PID (exception paragraph).

**Decision (Will, 2026-10-02):** a function gates A/C for the first 10 s of `Engine runtime`; `acMinRPM` → 750 (not 650,
out of concern for engagement while cranking). From this log the crank can't engage at either value: cranking RPM is
150–300, and `Switch 1` itself drops while the starter runs (0 from 1955.5 to 1957.4). `Engine runtime` stays 0 through
the crank, so the gate ends ≈ 11–12 s after the crank begins. At 750 (effective ≈ 765–790 logged) the steady troughs
clear it by ≈ 45–130; some of the standing-idle dives that tripped at 800 likely still trip. Confirmed in the 13:54 export: Fn 7
"AC Delay" = `Engine runtime` > 10 AND `Switch 1` Is True, Virtual, and `acActivation` = Fn 7 (encoding: `notes/functions.md`).
Same export: airflow kP 0.5 / kI 0.5, `idleAirFlowKD` raw 102 (≈ 0.1 if raw/1024, unverified), `acTimeToEngage` 740. Next log: count clutch-off
events with `Switch 1` on at idle.

## Afterstart hold 1.5 s (Will's experiment, `idleControlAfterstartDelay` 4 → 15, 0.1 s/ct)

Start 1 (48.8 s, CLT 82, OP ≈ 4 bar at 1150, no A/C) is the clean case. Exit at 750 (49.96), crosses target 1129 rising at
≈ +0.25 s, peaks 1734 at +0.65 s on the 22° lock (`afterstartIgnitionLockTime` 25 = 1.0 s) and the held cranking airflow 41
(MAP pumped down to 27). After the lock ends: 18°, decay ≈ 1000 rpm/s. ACTIVE at +1.5 s at 1109, on target but still falling
≈ 800 rpm/s with MAP 33 (38–40 at steady target). Spark at the max torque angle (35°) and the airflow PID at its +25 limit
within 0.6 s; trough 615 at 52.24. The late air gives overshoot 1430 (spark at the 10.5° retard limit), then 937, then
settled ≈ 1150 by 56 s. The held 41 was below the steady need at target (45–47 incl. PID), so its equilibrium is ≈ 1025
(air ∝ RPM). The pumped-down manifold refills with a lag, so the decay overshoots even that. Restart (CLT 98): same shape,
flare 1862, ACTIVE at 997 falling ≈ 1500 rpm/s, but the A/C clutch engaged at 1958.0 (trough 530 confounded).
Tally for the 1.5 s hold: 10-02 cold (CLT 29) ACTIVE at 1334 rising, clean. This log CLT 82 (no A/C): 615 / 1430.
**Both hot dips had the A/C clutch engage during the hold** (correction, 2026-10-02): `newhotstart.csv` clutch at 2478.00
(`Switch 1` back at 2477.36), ACTIVE at 2478.20; restart here, clutch at 1958.00, ACTIVE at 1958.28. The A/C custom airflow
correction appears only from ACTIVE (2478.20 / 1958.24), so the compressor load hit during the hold with no feed-forward.
The decay steepened from ≈ 700 to ≈ 1200 rpm/s at the clutch, and the 800 gate then relay-cycled it (2478.64 off, 2479.68 on).
So no clean hot sample exists for the 1.5 s hold. Will's held-plate model predicts the over-aired hot case settles above
target; untested. The CLT 82 start is the under-aired branch (held 41 below the 45–47 need). With 0.4 s on 10-01 cold: engaged at the flare peak, −150
undershoot, with the lock longer than the delay at the time. Exit-to-target time (the delay's design definition): ≈ 1.5 s cold
(hover), ≈ 0.1–0.25 s warm/hot. Delays between ≈ 0.4 and 1.2 s land at the warm flare peak.
In the 13:54 export, `aseTbl` hot runtime-0 = 10 %, not the ≈ 3 % issued earlier on 10-02. Start 1 ran ≈ 3 at CLT 82
and the restart ran 10 at CLT 98: Will was experimenting with ASE mid-log, so don't read either value as final.
