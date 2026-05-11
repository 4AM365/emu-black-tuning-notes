# Migration
- The idle system is very different from v2 to v3. You will need to redefine most things.
- Import your setup from v2 and then self-learn the throttle body.
- Next, override the DBW DC value and take notes of the throttle angle vs DC. This will be used for cranking as well as idle maps.

# Cranking
- Pick values that get you roughly 60-80kPa MAP under cranking. A cold engine needs lower MAP to lower the fuel boiling point and vaporize it, while a hot engine can add heat to vaporize the fuel.
- Try 25% enrichment (125 in the table) when cold, and 5% hot.

# Establishing sync fast
- EMU has a setting where you can infer position based on the status of the cam (high or low) when it encounters the first missing tooth gap, which you can also define.
- A smaller missing tooth gap is more aggressive and has less noise rejection. 90% might be a value here. 100% is default.
- Setting up the sensors correctly first is ideal - look at the scope during cranking and see how noisy the signal is if at all. If the sensors are shielded and close to the wheel, it's probably good to avoid using a noise filter and have a low adaptive threshold to get faster sync and eliminate the processing time associated with the filter. The filter is most likely a rolling average, so it eneds to fill the rolling average buffer before it can work.
- Check out the new cam sensitivity table - you can look at VR sensor voltage vs RPM!

# Idle
- Once the car is started, you'll want to define the actuator range. The larger the range, the less resolution you have.
- On cold start, override the airflow amount for idle and see how much throttle angle / DC it takes to idle at the absolute top of your range. For me, that's around 1500RPM once you add in post-start RPM increase, A/C RPM increase, and cold idle increase. I needed 8% angle, which becomes my max actuator value.
- Oil thins out gradually out until you reach roughly 70C. The idle ref table should look pretty flat between 70C and 90C, and increase exponentially under 70C to overcome oil resistance.
- Once the engine is hot, figure out the override % required to go just below your ideal hot idle. For me, that's 4.2% throttle angle. So 3.5% and 8.0% becomes my Airflow - Actuator range.
- The override target maps to the active state air flow. Change the value to achieve your desired RPM in a particular situation, and then populate the active state air flow % with that value. Super important to set this right. Mine goes from 18.5% at minimum (hot, low RPM) to 98% cold high RPM. This is what opens the throttle body a little when you re-enter idle to create a soft landing for your engine speed when you idle down from higher RPM.

# Idle entry
- Idle DBW blend point is the PPS at which the idle ref value becomes equal to the DBW characteristic value. You want this just above your idle point to give you some 'range' in which to adjust. For me it's 8% hot and 12% cold.

- Armed State Air Flow is what your TB does when you enter the idle armed state and you meet all criteria for idle and enter the RPM defined by idle target value + ramp down max offset.

# Idle Ref Table

Oil is pretty much warmed up by 71C, so the idle ref table gets linear there. Below 71C it's exponential due to oil viscosity.

The custom correction table does a good job of AC clutch compensation, but the range of time-to-engage for AC clutch should be around 900ms for a 2jz. It's a lot faster than the airflow correction.

Noisy vvt-i values and noisy CLT will push idle all over the place. Lock these down.

Get your fuel trims right! My FFIM needs another 9% fuel on cylinder 6 at idle. The effect actually lessens with boost; the manifold does a better job when it's under pressure. Get some EGT probes, they're essential.

# Special considerations for long-duration camshafts.

- On a cammed engine, there's charge dilution due to overlap so your flame front velocity drops along with your dynamic compression ratio. This means you need more timing at idle and cruise.

- Idle stability becomes marginal when you combine high intake temps with cams. Your idle RPM target needs to increase so you get some intake air momentum fighting the exhaust reversion and you store more energy in the flywheel to overcome misfires. For me this is an 1100rpm target in winter, but 1200 target in summer.





Look at your hot idle TPS. You never need significantly less than this TPS. Put your actuator floor just below this, and put your DBW min position DC % just below this. Sometimes there can be a gap where you're exiting idle air flow but the blend values aren't enough to support the engine, so the engine can die when you tap the throttle. If it's blending between a worst-case-the-engine-lives DBW value and a known-good-idle-ref, you're going to be OK.

Ignition timing just doesn't do as much work per degree at idle with cams. Tune your idle PID to be more aggressive and trim with the ignition. Try it out - sweep ignition timing while running and airflow override.

The active state airflow is mostly overcoming oil resistance. Oil resistance is exponential - more with colder oil.

Ultra high charge temps / IAT will cause superior fuel vaporization and thus cause the airflow PID to pull down airflow, so that the integrator winds up and then after a short movement, you'll choke the engine out and it will die. Combat this by running near-MBT ignition timing and then pulling timing as the charge temp heats up in order to maintain a stable airflow position.

Set the airflow PID integrator so that changes take about 5 seconds to ready steady state.