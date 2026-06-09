# Cranking and cold-start

Getting the engine lit and through the first 5–10 seconds. **Steady-idle table mechanics
(actuator range, idle target/ref, active & armed airflow, custom/fan correction, blend point,
airflow PID, idle ignition) now live in [idle.md](idle.md)** — this note covers only what is
unique to cranking and the cold-start transition. The two are a pair: cranking pre-positions the
throttle so the handoff *into* the idle system is stepless.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`idle_session_05242026.md`](../supra/notes/idle_session_05242026.md),
> [`airflow_actuator.md`](../supra/notes/airflow_actuator.md), and [`my_car.md`](../supra/notes/my_car.md).

## Migration from v2

- The idle system changed significantly from v2 to v3. Most settings will need to be redefined.
- Import your v2 setup, then run the throttle body self-learn.
- Next, override the DBW duty cycle and note the throttle angle vs. DC relationship. This is used
  for both cranking and idle maps.
- v3 flips the primary/secondary actuator roles: **airflow PID is the primary RPM controller**,
  ignition timing is fast-path fine-tuning only. This is the opposite of v2. (Full architecture:
  [idle.md → P2](idle.md), [idle_hot_drift_pid_windup.md](idle_hot_drift_pid_windup.md).)

## Cranking

- Target roughly 60–80 kPa MAP during cranking. A cold engine benefits from lower MAP (more
  vacuum) to reduce the fuel boiling point and aid vaporization; a hot engine relies on heat to do
  the same job.
- With extended-duration cams you will have a harder time developing MAP during cranking. Don't
  restrict the throttle arbitrarily to help out — defer to the airflow targets.
- Run more cranking enrichment cold than hot (cold needs a large positive enrichment for
  wall-film, hot needs only a small one). The cranking fuel enrichment bridges "engine spinning
  slowly with poor mixture formation" to "engine running and metering its own charge" — it pays
  the wall-film tax until surfaces warm up. It is **NOT** compensating for air starvation. See the
  build's working doc for this car's cranking enrichment values.

### Cranking-airflow handoff (the one airflow fact that belongs here)

`idleCrankingDC` is an independent open-loop table active **below 400 rpm**; the active airflow
table only applies once RPM crosses 400 rpm. They are separate control paths with a hard handoff.
Pre-position the throttle during cranking so the handoff is **stepless** — set `idleCrankingDC`
for each CLT bin to the active airflow value the engine will want just above 400 rpm at that CLT,
biased a few percent **above** it so the first idle correction is a gentle pull-down. Full method
and the manifold-time-constant rationale: [idle.md → Cranking airflow / P5](idle.md).

## Establishing Sync Quickly

- EMU has a setting to infer position from the cam sensor state (high or low) when it first
  encounters the missing tooth gap, which you can also define.
- A smaller missing-tooth gap threshold is more aggressive and has less noise rejection. 90% might
  work here; 100% is the default.
- Set up the sensors correctly first — scope the signal during cranking and assess noise. If the
  sensors are shielded and close to the wheel, skipping the noise filter is reasonable; it will
  give faster sync and eliminate the filter's processing delay. The filter is most likely a rolling
  average, so it needs to fill its buffer before it can function.
- Check the cam sensitivity table — you can plot VR sensor voltage vs. RPM.

## Afterstart Enrichment (ASE)

- Rapid throttle closure from the (higher) cranking TPS to the (lower) idle TPS creates a large
  air deficit that ASE alone cannot compensate.
- The fix is not to reduce ASE — it is to prevent the throttle from slamming shut post-start. Use
  a higher idle RPM target for 5–10 seconds after start, then taper down. (Stall version of this
  failure: [idle_stall.md §B](idle_stall.md).)
- Configure ASE as a 2D table: coolant temperature vs. post-start engine **revolutions** (not just
  time). The revolution axis correlates better to wall-wetting decay rate.
- Shape: large positive enrichment at cold/low-revolution cells, decaying to zero as the engine
  warms and the revolution count climbs. See the build's working doc for this car's ASE values.

## Idle ignition by fuel and cam (reference table)

Idle base advance is set **below MBT** to leave the controller recovery authority (reserve of
torque — Banish/Hartman). A diluted charge (cams, ethanol) burns slowly, so peak pressure needs
the burn to start earlier; cammed/ethanol builds therefore idle with more advance. Full setup
(target table, swing limits, flat-base rule) is in [idle.md → Idle ignition](idle.md); this is the
starting-range reference:

| Fuel | Cams | Idle timing range |
|------|------|-------------------|
| Pump gas | Stock | 10–12° |
| Pump gas | Cammed | 13–16° |
| Ethanol | Stock | 13–16° |
| Ethanol | Cammed | 16–19° |
| Ethanol | Big cams | 19–22° |

## Related notes

- [idle.md](idle.md) — steady-idle settings + principles hub (everything not unique to cranking)
- [idle_stall.md §B](idle_stall.md) — cold-start / post-start stall decision tree
- [cammed_idle_instability.md](cammed_idle_instability.md) — why a diluted idle charge is unstable
- [supra/notes/airflow_actuator.md](../supra/notes/airflow_actuator.md) — live cranking/active airflow values
