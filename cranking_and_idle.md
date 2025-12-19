# Migration
- The idle system is very different from v2 to v3. You will need to redefine most things.
- Import your setup from v2 and then self-learn the throttle body.
- Next, override the DBW DC value and take notes of the throttle angle vs DC. This will be used for cranking as well as idle maps.

# Cranking
- Shoot for 45% TPS at cold start and 15% on hot start. You'll know what DC values to put into the sheet from the last step.
- Try 25% enrichment (125 in the table) when cold, and 5% hot.

# Establishing sync fast
- EMU has a setting where you can infer position based on the status of the cam (high or low) when it encounters the first missing tooth gap, which you can also define.
- A smaller missing tooth gap is more aggressive and has less noise rejection. 90% might be a value here. 100% is default.
- Setting up the sensors correctly first is ideal - look at the scope during cranking and see how noisy the signal is if at all. If the sensors are shielded and close to the wheel, it's probably good to avoid using a noise filter and have a low adaptive threshold to get faster sync and eliminate the processing time associated with the filter. The filter is most likely a rolling average, so it eneds to fill the rolling average buffer before it can work.
- Check out the new cam sensitivity table - you can look at VR sensor voltage vs RPM!

# Idle
- Once the car is started, you'll want to define the actuator range. The larger the range, the less resolution you have.
- On cold start, override the airflow amount for idle and see how much throttle angle / DC it takes to idle at the absolute top of your range. For me, that's around 1500RPM once you add in post-start RPM increase, A/C RPM increase, and cold idle increase. I needed 6.2% angle, which becomes my max actuator value.
- Once the engine is hot, figure out the override % required to go just below your ideal hot idle. For me, that's 3.0% throttle angle. So 3.0 and 6.2% becomes my Airflow - Actuator range.
- The override target maps to the active state air flow. Change the value to achieve your desired RPM in a particular situation, and then populate the active state air flow % with that value. Super important to set this right. Mine goes from 18.5% at minimum (hot, low RPM) to 98% cold high RPM. This is what opens the throttle body a little when you re-enter idle to create a soft landing for your engine speed when you idle down from higher RPM.

# Idle entry
- Idle DBW blend point is the TPS at which you go from the DBW characteristic table to the active state air flow table. You want this just above your idle point to give you some 'range' in which to adjust. For me it's 5% hot and 10% cold.

- Armed State Air Flow is what your TB does when your foot is off the gas. I like this to be a little high to keep the turbo spooled between gears, but just low enough that the engine will drop RPM. Mine drops quickly because it's 10:1 with a reasonably sized TB.

