# Cranking and Idle

## Migration from v2

- The idle system changed significantly from v2 to v3. Most settings will need to be redefined.
- Import your v2 setup, then run the throttle body self-learn.
- Next, override the DBW duty cycle and note the throttle angle vs. DC relationship. This is used for both cranking and idle maps.

## Cranking

- Target roughly 60–80 kPa MAP during cranking. A cold engine benefits from lower MAP (more vacuum) to reduce the fuel boiling point and aid vaporization; a hot engine relies on heat to do the same job.
- Try 25% enrichment (125 in the table) when cold, and 5% hot.

## Establishing Sync Quickly

- EMU has a setting to infer position from the cam sensor state (high or low) when it first encounters the missing tooth gap, which you can also define.
- A smaller missing-tooth gap threshold is more aggressive and has less noise rejection. 90% might work here; 100% is the default.
- Set up the sensors correctly first — scope the signal during cranking and assess noise. If the sensors are shielded and close to the wheel, skipping the noise filter is reasonable; it will give faster sync and eliminate the filter's processing delay. The filter is most likely a rolling average, so it needs to fill its buffer before it can function.
- Check the cam sensitivity table — you can plot VR sensor voltage vs. RPM.

## Idle

- Once the car is started, define the actuator range. The larger the range, the less resolution you have.
- On cold start, override the idle airflow and note how much throttle angle / DC it takes to idle at the top of your RPM range. For me that's around 1500 RPM once you add post-start RPM increase, A/C RPM increase, and cold idle increase — I needed 8% throttle angle, which becomes my max actuator value.
- Oil thins out gradually until roughly 70 °C. The idle ref table should be fairly flat between 70 °C and 90 °C, then rise exponentially below 70 °C to overcome oil drag.
- Once the engine is hot, find the override % required to run just below your ideal hot idle RPM. For me that's 4.2% throttle angle. So 3.5% and 8.0% becomes my actuator range.
- The override target maps to the active-state airflow. Adjust the value to achieve your desired RPM in a given situation, then populate the active-state airflow % with that value. Mine ranges from 18.5% at minimum (hot, low RPM) to 98% cold high RPM. This is what opens the throttle body slightly on idle re-entry to cushion the RPM drop when coming off higher RPM.

## Idle Entry

- Idle DBW blend point is the PPS at which the idle ref value equals the DBW characteristic value. Set this just above idle so you have some range for adjustment. Mine is 8% hot and 12% cold.

- Armed State Air Flow is what the throttle body does when you enter the idle armed state and meet all criteria to enter the RPM defined by idle target + ramp-down max offset.

## Idle Ref Table

Oil is substantially warmed up by 71 °C, so the idle ref table becomes linear there. Below 71 °C it is exponential due to oil viscosity.

The custom correction table handles A/C clutch compensation well, but the engagement time range should be around 900 ms for a 2JZ — much faster than the airflow correction.

Noisy VVT-i values and noisy CLT will push idle all over the place. Lock these down first.

Get your fuel trims right. My FFIM needs about 9% more fuel on cylinder 6 at idle. The effect diminishes with boost — the manifold does a better job of distribution under pressure. Get EGT probes; they're essential.

## Long-Duration Camshafts

- Longer-duration cams have more overlap even if they share a lobe separation angle with stock cams.
- On a turbo engine with overlap, exhaust pressure is always higher than intake pressure due to the turbine restriction, so exhaust gas blows back into the intake. The RPM you idle at determines how much intake air momentum fights the exhaust reversion.
- You will need more ignition timing at idle because exhaust gas dilutes the charge, slowing flame-front velocity (think CA50).

- Idle stability becomes marginal when you combine high intake temps with aggressive cams. Raise your idle RPM target to build intake air momentum against exhaust reversion and store more energy in the flywheel to ride through misfires. I use 1100 RPM in winter and 1200 RPM in summer.

- Ignition timing does less work per degree at idle on a cammed engine. Tune the idle PID more aggressively and trim with ignition timing — sweep timing while running with the airflow override active.

| Fuel | Cams | Idle timing range |
|------|------|-------------------|
| Pump gas | Stock | 10–12° |
| Pump gas | Cammed | 13–16° |
| Ethanol | Stock | 13–16° |
| Ethanol | Cammed | 16–19° |
| Ethanol | Big cams | 19–22° |

## Extreme Charge Temps at Idle

Ultra-high charge temps reduce air density but improve fuel vaporization and effectively advance timing by increasing flame-front velocity, making peak cylinder pressure easier to achieve. I find I need about 30% less airflow when going from 30 °C to 65 °C charge temps. I repurposed the idle airflow compensation table for this correction.

Look at your hot-idle TPS. You never need significantly less than that angle. Set your actuator floor just below it, and set your DBW min position DC% just below it too. Sometimes there is a gap between exiting idle airflow control and the blend values being sufficient to support the engine, causing a stall on a light throttle tap. If you're blending between a worst-case-survival DBW value and a known-good idle ref, you'll be fine.

## PID Tuning

Be careful here — it's easy to make things worse. Keep the integrator limits lower than the proportional limits: the proportional term responds immediately, but the integrator accumulates over time and can trap you in a low-airflow state just long enough to stall the engine.

Set the airflow PID integrator so that corrections take about 5 seconds to reach steady state.
