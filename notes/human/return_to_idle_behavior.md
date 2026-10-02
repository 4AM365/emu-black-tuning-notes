# RPM Bounce on re-entry without dip below target
- If RPM bounces up, look at idle air % during the re-entry log.
- Typically there will be a step function, your job is to find the source of the step function (step function is sudden increase in duty cycle)
- Most likely candidate is coolant fan DC Corr. Solve this by activating the coolant fan much earlier if it is a significant drag, or switching to a gradual PWM control strategy that does not outrun the PID's ability to correct for it.

# RPM dip then bounce
- Something is driving the RPM below the target. The dip is the engine failing to correct for it, and the recovery is the engine recovering too late.
- The recovery strategy works, it's just too slow.
- First, something is causing a dip! Check for a sudden change when the handoff from idle armed to idle active state occurs, or look for a narrow window where the TPS tracks PPS - sometimes the DBW output can escape the idle strategy and default to the DBW Characteristic map.
- My characteristic maps have the 0% PPS column set close to the idle TPS value as a result
- Sometimes the rpm decay rate is incorrect, so that when the RPM crosses the idle control strategy threshold (sum of idle target RPM plus decay rate target offset), then the idle PID will begin to pull the RPM down and will overshoot the target, resulting in RPM below target.

# RPM catch above target, then slow decay
- Caused by excessive active state airflow. The active state table should be tuned well above target. In my case, it spans 1000 to 2000 RPM for a 1000 RPM target idle.
- Idle strategy transitions from armed state airflow amount to active state and the engine gets a bolus of air, and then PID is responsible for dragging RPM down.

# Slow correction or long settling time
- Often a consequence of insufficient PID ignition control authority. Because the airflow PID acts on the ignition target error, ignition must be set first.
- A reasonable range for the idle ignition min and max torque on a cammed 10:1 engine is from 10 degrees to 35 degrees. Test this by doing manual overrides at idle for airflow and ignition.
- Remember that armed state can be used to control the rate of descent. The rate of RPM loss is typically non-linear, but can be forced linear so that the RPM decay rate can be set correctly. The RPM decay rate is responsible for telling the PID not to wind up and what to expect first.

# General Principle
- An engine does not need PID to return to idle consistently and reliably. This is governed by physics - the engine wants to reach equilibrium between pumping force (combustion) and pumping resistance (energy required to create vacuum in intake manifold). As you approach the idle airflow amount, the difference between what the vacuum takes and the combustion provides reduces, meaning less force is available to slow the engine RPM, so it settles more gently. It creeps up to the target.
- The purpose of idle air control is really to restrict intake air as the engine becomes more efficient when hot.
- An engine will need about half of the idle airflow when it goes from cold coolant to fully heated, but it will also need significantly less air to idle when the oil heats up fully. These behaviors are independent.