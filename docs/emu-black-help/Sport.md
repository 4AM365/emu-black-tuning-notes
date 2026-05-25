##Sport

The Sports category contains a list of strategies used in motorsport.


---

[Auto](help://Sport/Sport) 
##Flat shift

The __Flat shift__ strategy is used when shifting gears upwards with the accelerator pedal fully pressed. When the clutch is depressed (the clutch switch should activate the __Flat shift__ function), the strategy activates, aiming to maintain the engine revs at a predetermined level despite the accelerator pedal being fully depressed.

**Logging channels:

* __   **Flat shift active** __ - flag indicating whether the flat shift strategy is active
* __   **Flat shift cut %** __ -  the value of ignition or injection events currently being cut (depending on the strategy configuration)


{#1}


---

[Auto](help://Sport/Sport) 
##Rev matching

The Rev Matching strategy is designed to increase engine RPM when downshifting using a manual transmission with an H-pattern. This allows for setting higher RPM during gear changes, improving the car's balance and reducing wear on the drivetrain.

**Note: To utilize this strategy, an electronic throttle is required.

To implement the strategy, connect the clutch and brake pedal sensors to the Engine Management Unit (EMU). The strategy detects the situation where the driver presses the brake pedal during a gear reduction (PPS must be lower than 2.5% to activate strategy) and activates after releasing the clutch pedal. 

If you want to downshift multiple gears, press the clutch pedal again after each shift. The strategy operates in two modes:


**Fixed RPM target** - regardless of the gear, the same RPM is set during gear changes.

**Calculated RPM target** - based on the Gear to Speed ratio values from the VSS configuration, the strategy calculates the expected engine RPM following a gear reduction. This allows optimal adjustment of the engine speed and is the recommended mode.

**Calculated RPM target forced** - rev matching is activated immediately upon strategy activation (i.e., when the function assigned to the __Enable Input__ parameter evaluates to 1), regardless of the __Clutch__ and __Brake switch__ channel values. RPM target calculation is identical to the __Calculated RPM Target__ mode. This mode can be used, for example, to execute rev matching from an external gearbox controller.

**Log Channels:

* **__Rev. match active__** - indicates whether the strategy is active and attempting to set the desired RPM.
* **__Rev. match RPM target__** - the desired RPM that the strategy aims to set.
* **__Rev. match Gear target__** - the expected gear after the reduction.
* **__Rev. match armed__** - indicates whether the strategy is armed (brake pedal pressed) and waiting for activation.


Additionally, monitor the state of the electronic throttle channel DBW Target Source to check when Rev Matching is controlling the throttle.

{#1}



---

[Auto](help://Sport/Sport) 
##Rolling start

The Rolling start strategy is the equivalent of Launch Control, which can be activated while the vehicle is in motion. When the strategy is activated, the engine speed is read and maintained.

This allows for driving at a constant speed with the accelerator pedal depressed and building up boost pressure. When the strategy is deactivated, the ignition advance is smoothly restored, and fuel / ignition cut-off is terminated, allowing for a smooth increase in torque, reducing wheel slip, and decreasing the load on the drivetrain.

The current operating state of the strategy can be observed in the ** __Rolling start state log__** channel.

* ** Inactive ** - the strategy is inactive (either the activation input is not defined or the switch is not active)

* **Conditions not met ** - the switch is active, but other conditions are not met (e.g., coolant temperature too low, vehicle speed too low, or EGT too high)

* **Active** - the strategy is active

* **Exit** - the strategy is in exit mode, where the ignition advance angle is restored 


**Logging channels:

* __** Rolling start state**__ - a channel indicating whether the rolling start strategy is active.
* __** Rolling start target**__ - engine RPM that the rolling start strategy will maintain.
* __** Rolling start fuel corr**__ - current fuel dose correction.
* __**Rolling start ign. corr.**__ - current ignition advance angle correction.

---

[Auto](help://Sport/Sport) 
##Shift light

The shift light strategy enables the implementation of a visual gear change indicator using, for example, an LED. It allows defining the engine RPM at which the indicator will illuminate for each gear. It's important to consider the rate of RPM increase for each gear and activate the LED with the appropriate lead time to give the driver time to react.

**Logging channels:

* __   **Shift light** __ - flag indicating whether the shift lighe output is active


{#1}



---

[Auto](help://Sport/Sport) 
##ALS

The aim of the Anti-Lag strategy in turbocharged engines is to maintain the rotational speed of the turbocharger when the throttle is closed (for example, during gear changes or deceleration into a corner).

During throttle closure, the strategy takes control over it (in the case of DBW) or activates a so-called throttle kicker, which opens the throttle (or an additional solenoid valve supplying extra air to the engine), or a mechanical throttle is partially opened (in such a case, idle speed control should utilize cycling idle or fuel/ignition cut strategies), resulting in the delivery of extra air to the engine.

By retarding ignition and cutting fuel/ignition, we can induce late combustion of the mixture, enabling the turbocharger to be powered. It should be noted that ALS (Anti-Lag System) can cause a "dragging" effect on the vehicle during braking and can also negatively affect the lifespan of the turbocharger/exhaust valves.

It's also worth emphasizing that the air pressure (boost) behind the throttle on a partially open throttle will be significantly lower than the pressure before the throttle. For this reason, it is preferred to use a pre-throttle boost sensor or set the strategy very cautiously to keep the boost pressure as low as possible.

Key to setting the parameters of the ALS (Anti-Lag System) strategy is monitoring the ALS state parameter, which represents the current state of the strategy. Below is a list of states along with their descriptions:

* **Disable** - the strategy is not activated by the user switch
* **Not armed** - the strategy is activated but not armed. To transition to the active state, it must first be armed. For this to occur, the engine RPM must exceed the __Armed above RPM__ value, and the accelerator pedal position must exceed the __Arming above PPS__ value.
* **Armed** - the strategy is ready to transition to the active mode when the accelerator pedal position is lower than the __Activate below PPS__ value.
* **Active** - the strategy is active. It will exit this state if the accelerator pedal position exceeds the __Activation below PPS__ + __Activation PPS hysteresis__ value, or when the maximum duration is reached, or if the cooling liquid temperature or exhaust gas temperature (EGT) exceeds their respective thresholds.
* **Exit** - after exiting the active state, the strategy enters the exit state, where it gradually restores ignition advance angle and cuts off ignition/fuel to smoothly restore torque. From this state, the strategy transitions to the __Not armed__ state.


Additionally, there are conditions where the strategy remains inactive:

* **Inactive above CLT** - If the cooling liquid temperature exceeds the __Max CLT__ value, the strategy will not activate, or if already active, it will immediately exit.
* **Inactive below CLT** -If the cooling liquid temperature is below the __Min CLT__ value, the strategy will not activate, or if already active, it will immediately exit.
* **Inactive above EGT** -If the Exhaust Gas Temperature (maximum value from all connected EGT sensors) exceeds the _Max EGT__ value, the strategy will not activate, or if already active, it will immediately exit.
* **Inactive below VSS** - If the vehicle speed is lower than the __Min VSS__ value, the strategy will not activate, or if already active, it will immediately exit.


**Logging channels:

* __** ALS fuel correction**__ - actual fuel dose correction caused by ALS strategy.
* __** ALS cut**__   - the percentage of ignition events or fuel injections being cut off by ALS strategy.
* __**ALS state**__ - actual state of ALS strategy. States are described in the text above.
* __**ALS ingition angle**__ - actual ALS ignition angle correction (or absolute value depends on ALS settings)


---

[Auto](help://Sport/Sport) 
##Diff control

The differential control strategy allows for the management of active differentials.

Differentials controlled by PWM signals (e.g., EVO X, Haldex 2nd gen) are supported. For Haldex, however, it's necessary to modify the module and directly connect the EMU to the internal solenoid valve.

To define the output to which the solenoid controlling the differential is connected, you need to navigate to the settings for {1} . From there, select the function for PWM output 1 or PWM output 2 and configure the output as well as the frequency of the control signal.

Control is based on vehicle speed and throttle position. There are three sets of tables available for selection (e.g., gravel, tarmac, snow) separately for braking and acceleration (DC Brk, DC Acc).

In addition to controlling the differential mechanism solenoid, there is the option to control the oil pump. For Haldex mechanisms, the pump control is continuous, with the pump itself controlled via PWM modulation to limit the flowing current.

For pumps where pressure is regulated using a pressure sensor, the control is On/Off with hysteresis. The pump is activated when pressure drops below the minimum and deactivated when it exceeds the defined maximum value.

**Logging channels:

* **__Diff ctrl. active__** – status of differential control strategy activity
* __**Diff ctrl. oil pump active__** – status of differential oil pump control activity
* __**Diff ctrl. active table__** – currently active differential control table
* __**PWM 1 or 2 DC__** – depending on the selected PWM channel, indicates the current duty cycle of the solenoid valve controlling the differential

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##Parameters

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##DC Acc 1

The table defining the duty cycle (DC) of the solenoid control signal for the differential when the vehicle is accelerating.








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##DC Brk 1

The table defining the duty cycle (DC) of the solenoid control signal for the differential when the vehicle is braking.


---

[Auto](help://Sport/Sport) 
##Gear Cut

Each group contains specific information related to its respective area


---

[Auto](help://Sport/Sport) 
##Launch ctrl.

The launch control strategy enables maintaining the desired engine rotational speed during launch, building up boost, and achieving rapid vehicle acceleration through smooth torque delivery.

Engine rotational speed control is accomplished using a PID controller by manipulating ignition timing advance and cutting ignition events or fuel injection. It's important to emphasize that in vehicles equipped with a catalytic converter, cutting ignition events can lead to its damage due to fuel-air mixture combustion within it.

To ensure smooth torque transfer to the wheels when releasing the clutch, parameters such as the ignition timing advance rate, injection/spark timing, and, in the case of electronic throttle control, throttle opening rate can be defined.

The strategy can be activated whenever the vehicle is stationary (VSS is equal to 0) and the throttle is open above a specified value (e.g., 90%) or may require additional activation via a switch. Depending on this configuration, the Activation input parameter should be set as __Always active__ or assigned to an appropriate switch.

The strategy allows for limitations to prevent activation when the engine temperature is too low or too high. If the strategy is active but any of the operational conditions are not met (e.g., coolant temperature too high or exhaust gas temperature too high), the strategy will be halted and transition to the __Wait for exit state__.

The strategy includes an additional state called **__Prestage**__, which allows for setting different parameters, such as the target boost pressure (Boost Target), engine RPM, ignition cut percentage (Cut %), and others. The **__Prestage**__ state (when enabled) is activated as the first phase of Launch Control. During this state, the system maintains the configured parameters until one of the following conditions is met:
* The boost pressure reaches the value defined by the Boost Target parameter.
* A predefined time duration elapses.

Once either condition is satisfied, the strategy transitions to the **__Active state**__. 

The current operating state of the strategy can be monitored in the **__LC state__** log channel:

* **Inactive** - the strategy is inactive.
* **Wait for activation** - upon strategy activation, it transitions to this state for the defined __Activation delay__ period.
* **Active prestage** - the strategy is in prestage active state. 
* **Active** - the strategy is active.
* **Wait for exit** - upon strategy deactivation, it transitions to this state for the defined __Deactivation delay__ period.
* **Exit** - the state in which the ignition timing advance is restored, ignition cut is disabled, and in the case of electronic throttle control, the throttle is opened to a position determined by the current accelerator pedal position.


**Logging channels:

* **__LC RPM target__** -  the target RPM towards which the strategy is currently working.
* **__LC boost target__** -  the boost target resulting from the operation of the launch control strategy.
* **__LC cut__** -  flag indicates ignition or fuel cut.
* **__LC fuel enrichment__** -  the percentage fuel-air mixture enrichment.
* **__LC ignition angle__** -  the ignition timing advance angle resulting from the operation of the launch control strategy.
* **__LC state__** - the current state of the strategy, as described above.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Parameters

The **Launch Control** strategy offers two methods of maintaining the desired engine RPM, defined by the **Cut type** parameter:

- **Spark cut** – cuts ignition events to hold the target RPM.  
- **Fuel cut** – cuts injection events to control engine RPM.  

Additionally, it is possible to retard ignition and adjust the throttle position (when DBW is used).

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Cut PID

The PID controller controlling ignition/fuel cut operates differently depending on the selected control type in {1}

If the control type is set to "cut," this controller operates independently, relying on the error between the engine RPM and the launch control target RPM.

If the control type is set to "cut and ignition retard," this controller functions as a secondary PID controller, relying on the error between the ignition timing advance angle from the {2} table and the angle calculated by the {3}.

It should be emphasized that the Cut PID modifies the base ignition/fuel cut (feed forward) from the {4}.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Ignition PID

In he case of selecting control type ({1})  __Cut and igntion retard__,  ignition PID modifies the base ignition timing advance angle from the  {2} depending on the error between the target RPM and the current engine RPM. 

The second PID controller cuts ignition/fuel depending  on the the error betwwen  current ignition timing and the base ignition timing advance angle from the {3}
. 
This solution results in both PID controllers "cooperating" with each other.

It should be emphasized that the Ignition PID modifies the base ignition/fuel cut (feed forward) from the {4}

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Strategy exit

When deactivating the launch control strategy, it transitions from the **__Active state__** to the __**Wait for exit__** state, and then, after the defined time specified by the __Deactivation delay__ parameter ({1}), it transitions to the Exit state.

In the **__Exit state__**, the ignition timing advance is restored, ignition cut is disabled, and in the case of electronic throttle control, the throttle is opened to a position determined by the current accelerator pedal position.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Boost target

The boost target during the operation of the strategy. It overrides the boost target calculated by the boost control strategy. 
Changing the target is done using a rotary switch defined in the {1}. If the rotary switch is not assigned, then the value from the first column is taken.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Cylinder cut

The table defines the base ignition/fuel cut for a given RPM target. This value is modified by the Cut PID controller.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Fuel enrichment

The table defines the enrichment/lean-out of the fuel-air mixture depending on the Target RPM.




---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Ignition angle

The table defines the base ignition/fuel ignition advance for a given RPM target. 

In the case of selecting control type {1} __Cut and igntion retard__, this value is modified by the Ignition PID controller.





---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##RPM target

The RPM target towards which the Launch control strategy will strive.

Changing the target is done using a rotary switch defined in the {1}. If the rotary switch is not assigned, then the value from the first column is taken.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##DBW target

In the case of a vehicle equipped with an electronic throttle, this table determines the throttle position depending on the RPM target and boost target.







---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Launch control

**Logging channels:

* **__LC ignition angle__** -  the ignition timing advance angle resulting from the operation of the launch control strategy.
* **__LC fuel enrichment__** -  the percentage fuel-air mixture enrichment.
* **__LC cut__** -  the percentage of ignition or fuel cut.
* **__LC RPM target__** -  the target RPM towards which the strategy is currently working.
* **__RPM__** -  engine RPM
* **__LC boost target__** -  the boost target resulting from the operation of the launch control strategy.
* **__Boost__** -  actual boost pressure





{#1}

**Meaning of Nitrous stage state

* **Inactive** - the strategy is inactive.
* **Wait for activation** - upon strategy activation, it transitions to this state for the defined __Activation delay__ period.
* **Active prestage** - the strategy is in prestage active state. 
* **Active** - the strategy is active.
* **Wait for exit** - upon strategy deactivation, it transitions to this state for the defined __Deactivation delay__ period.
* **Exit** - the state in which the ignition timing advance is restored, ignition cut is disabled, and in the case of electronic throttle control, the throttle is opened to a position determined by the current accelerator pedal position.


---

[Auto](help://Sport/Sport) 
##Pit limiter

The pit limiter is a strategy used to limit the speed of a vehicle to a set value, particularly useful in racing, where there are speed restrictions in the pit lane. Due to the fact that different racing tracks have different speed limits, the pit limiter strategy allows for the definition of multiple speeds and selection through a rotary switch.

The pit limiter strategy utilizes cutting off ignition events or fuel injections to limit the engine's speed in order to achieve the desired vehicle speed. In the case of using an electronic throttle, there is the possibility of limiting torque by partially limiting the throttle position while the pit limiter strategy is active.

**Logging channels:

* __** Pit limiter state**__ - a channel indicating whether the pit limiter strategy is active.
* __** Pit limiter cut**__ - the percentage of ignition events or fuel injections being cut off.
* __** Pit limiter target speed**__ - the speed that the pit limiter strategy will strive to maintain.




---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Parameters

A set of parameters enabling the configuration of the pit limiter strategy

{#1}



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Pit limiter torq. reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##DC Acc #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##DC Brk #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) 
##ALSX

Each group contains specific information related to its respective area


---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Parameters

A set of parameters enabling the configuration of the ALS strategy

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##DWB target

This table defines throttle openings when the ALS strategy is in the __Active__ state, depending on the engine RPM.








---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Cut

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Fuel correction

This table defines fuel dose corrections when the ALS strategy is in the active state.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Ignition correction

This table defines the ignition angle (or ignition angle correction depending on the value of the parameter __Ignition control method__ in {1}/).




---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Cylidner cut

This table defines the percentage of ignition events/injections cut (depending on the value of the parameter __cut type__ in {1}/).








---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Strategy exit

When the ALS strategy transitions to the **__Exit__**  state, the parameters of **__strategy exit__** determine how the ignition timing angle will be restored and how all ignition events/injections will be restored.
The ALS strategy will transition from the **__Exit__** state to the **__Not armed__** state as soon as the ignition timing angle is restored and the spark/fuel cut reaches a value of 0%.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Pit limiter speed target

__Pit limiter speed target__ table defines the desired speed of the pit limiter strategy, depending on the position of the rotary switch. In case the rotary switch is not assigned, the speed target for the strategy is defined in cell 0 of the table
.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Pit limiter DBW limit

__Pit limiter DWB limit__ table defines the desired limit of the throttle position, depending on the position of the rotary switch. In case the rotary switch is not assigned, the throttle limit is defined in cell 0 of the table. 


---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Launch control

The help content will cover essential details about channels in this particular group.
{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Pit limiter cut

__Pit limiter cut__ table defines the percentage of ignition/fuel cut based on the error between the desired and actual vehicle speed. The smoothness of vehicle speed regulation depends on the settings of this table.







---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##ALS

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Speed target

__Pit limiter speed target__ table defines the desired speed of the pit limiter strategy, depending on the position of the rotary switch. In case the rotary switch is not assigned, the speed target for the strategy is defined in cell 0 of the table.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##DBW limit

__Pit limiter DWB limit__ table defines the desired limit of the throttle position, depending on the position of the rotary switch. In case the rotary switch is not assigned, the throttle limit is defined in cell 0 of the table. 

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Cylinder cut

__Pit limiter cylinder cut__ table defines the percentage of ignition/fuel cut based on the error between the desired and actual vehicle speed. The smoothness of vehicle speed regulation depends on the settings of this table.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##Parameters

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##Boost target

Boost target table defines the desired boost depending on the vehicle speed. This requires settings in the parameters of the Override boost target option.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##DBW target

DBW target table specifies the desired throttle position depending on the vehicle speed. This requires settings in the parameters of the Override DBW option.



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##Fuel correction

Fuel correction table determines the fuel dose correction depending on the vehicle speed.



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##Ignition correction

Ignition correction table specifies the ignition advance angle correction depending on the vehicle speed.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Rollingstart) 
##Rolling start

{#1}


---

[Auto](help://Sport/Sport) 
##Gearbox

Each group contains specific information related to its respective area


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearbox) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearbox) 
##Up shift - cut

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearbox) 
##Down shift - blip

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) 
##Gearbox shifts

Each group contains specific information related to its respective area


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) 
##Up shift - cut

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) 
##Down shift - blip

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) 
##Torque reduction

Each group contains specific information related to its respective area


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Torquereduction) 
##Cut

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Torquereduction) 
##Igntion corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Upshift timeout

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Torquereduction) 
##DWB target corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Upshift torque reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Torquereduction) 
##Torque recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Torque recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Downshift blip level

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Downshift timeout

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Downshift post-shift torq. reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Downshift post-shift recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Post down shift torq. reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Post down shift recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Timeout

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Upshift_cut) 
##Torque reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Timeout

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Blip level

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Torque reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Torque recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Post shift torque reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearboxshifts) [Auto](help://Sport/Gearboxshifts/Downshift_blip) 
##Post shift torque recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) 
##Gear shifts

The **__Gear Shift**__ strategy is used to control the throttle and limit torque with use of sequential gearboxes. It implements the gear cut strategy (limiting torque during upshifts) and the Blip strategy (increasing engine revs during downshifts). To initialize the strategy, a load cell or switches installed in the gearshift lever are utilized, or an external control unit transmitting gear cut/blip commands to the EMU, or an internal paddle shift strategy. The configuration of the gear lever is found in {1}. Depending on the gear lever position, it sets **__Gear Lever Action**__ log channel to __Upshift Request__, or__ Downshift Request__. 
  
The implementation of the strategy can be based on fixed timing for each gear (open-loop), gear position sensor (closed-loop), or an external controller where cut or blip activity is externally controlled. The sensor and voltage defining a specific gear are configured in {2}. Since analog inputs are logged at various frequencies, it is recommended to connect the gear position sensor to analog input 4, which logs at 250Hz, facilitating strategy configuration. It should be noted that all analog inputs are sampled at a minimum frequency of 500Hz.

**Open Loop
In the Open Loop strategy, the duration of gear-upshift cut or blip is fixed (defined in Timeout tables) for each gear separately.

![sport/gearcutOpenLoop.png](Images/sport/gearcutOpenLoop.png)


**Closed Loop
In the Closed Loop strategy, the duration of Gear Upshift Cut or Blip ends as soon as the gear physically changes (target gear engaged), determined based on the gearbox sensor voltage. The strategy will also end after a timeout if no gear change occurs during this time, or if the sensor voltage indicates an undefined gear or malfunction. The Closed Loop strategy enables the fastest gear changes and is the preferred strategy.

For proper operation of the strategy, accurate calibration of the {3} Min and Max values for each gear is mandatory!

![sport/gearcutClosedLoop.png](Images/sport/gearcutClosedLoop.png)

**External Controller:
For an external controller, two inputs are defined (e.g., physical switch inputs or switches controlled via the CAN bus) to activate shift-up cut or blip. The duration of cut or blip is controlled by the external controller signal but cannot exceed the defined Timeout. In such a case, the strategy is interrupted and 
enters a recovery state.

![sport/gearcutExternalController.png](Images/sport/gearcutExternalController.png)


**Logging channels:

* __   **Gear shift state** __ - the current state of the gear shift strategy
* __   **Gear shift state torque reduction** __ - actual value of the torque reduction during up shift..


**Meaning of gear shift  state

* __   **Disabled** __ - the controller is disabled 
* __   **Not active** __ - the controller is enabled but doesnt perform any operation
* __   **Rejected - clutch engaged** __ - the strategy was not activated because the clutch pedal was pressed.
* __   **Rejected - gearbox sensor error** __ - - the strategy was not activated because there is an error connected to the gear box sensor.  
* __   **Rejected - leaver sensor errorr** __ - the strategy was not activated because there is an error connected to the gear lever sensor.    
* __   **Rejected - upshift low RPM ** __ - the strategy was not activated because the RPMs are too low for the up shift .
* __   **Rejected - downshift high RPM ** __ - the strategy was not activated because the RPMs are too high for the down shift .
* __   **Rejected - gear unknown ** __ - the strategy was not activated because the current gear is unknown. 
* __   **Rejected - gear neutral ** __ - the strategy was not activated because the gear is neutral.
* __   **Rejected - gear reverse** __ - the strategy was not activated because the gear is reverse
* __   **Rejected - VSS too low** __ - the strategy was not activated because the vehicle speed is too low. 
* __   **Rejected - upshift tps too low** __ - The attempt to upshift failed because the throttle position was below the defined **__Min TPS to cut**__ value in the {4}.
* __   **Rejected - downshift tps too high** __ - The attempt to downshift failed because the throttle position was above the defined **__Max TPS to blip**__ value in the {5}.

* __   **Upshift - shift** __ - the strategy performs the up shift torque redcution (cut, ignition corr, DBW target corr).
* __   **Upshift - recovery** __ - the strategy performs recovery from the torque redcution stage.
* __   **Downshift - shift** __ - the strategy performs the down shift blip.
* __   **Downshift - recovery** __ - the strategy performs recovery from the blip stage.		
* __   **Rearm** __ - the strategy is rearm state.			
		

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) 
##Torque reduction

During the execution of the upshift strategy, torque reduction is applied (in the Torque reduction table). Depending on the desired torque reduction value (ranging from 0 to 100%), it is possible to set fuel or ignition cut, modify the ignition advance angle, and adjust throttle position.








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Torquereduction) 
##Cut

This table defines the percentage of cut (fuel/ignition) depending on the desired torque reduction.



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Torquereduction) 
##Igntion corr.

This table defines the ignition angle correction depending on the desired torque reduction.



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Torquereduction) 
##DWB target corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) 
##Up shift - cut

In the event that the gear shift strategy receives an upshift request from the **__Gear Lever Action__** channel or the request comes from an external controller, the upshift procedure will be executed. Its task is to momentarily decrease the torque, which facilitates shifting to a higher gear.

If the clutch is pressed, there is a problem with the gear sensor, or any other issue arises, the gear upshift strategy will not be activated, and the cause will be indicated in the __**Gear Shift State__** logging channel.

For __**Open loop__** control type, the duration of torque reduction is defined in the  {1} table.

In the __**Closed loop__** strategy, torque reduction continues until the gear is changed or until the {2} value is reached if the gear change does not occur sooner.

The following diagram illustrates the voltage curve from the gear position sensor and the behavior of the closed-loop gear upshift strategy.

![sport/gearShiftUp.png](Images/sport/gearShiftUp.png)


For __**External controller__** strategy, torque reduction continues as long as the signal from the external controller is active, or until the {3} value is reached if the gear change does not occur by then.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Upshift_cut) 
##Timeout

The table specifying the maximum duration of the cut phase during the gears upshift strategy.

During a gear change from 2 to 3, the time is taken from column 2; from 3 to 4, it's taken from column 3, and so on.








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Upshift_cut) 
##Torque reduction

This table defines the value of torque reduction depending on the current gear and MAP.

During a gear change from 2 to 3, the torque reduction is taken from column 2; from 3 to 4, it's taken from column 3, and so on.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Upshift_cut) 
##Torque recovery time

After the torque reduction phase, the controller transitions to the recovery phase, during which torque is restored.  The **__Torque recovery time**__ table specifies the time for each gear during which torque is restored.

During a gear change from 2 to 3, the time is taken from column 2; from 3 to 4, it's taken from column 3, and so on.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) 
##Down shift - blip

In the event that the gear shift strategy receives an downshift request from the **__Gear Lever Action__** channel or the request comes from an external controller, the downshift procedure will be executed. Its task is to increase the engine torque usnig throttle blip, which facilitates shifting to a lower gear.

If the clutch is pressed, there is a problem with the gear sensor, or any other issue arises, the gear upshift strategy will not be activated, and the cause will be indicated in the __**Gear Shift State__** logging channel.

For __**Open loop__** control type, the duration of throttle blip is defined in the {1}  table.

In the __**Closed loop__** strategy, the throttle blip continues until the gear is changed or until the {2} value is reached if the gear change does not occur sooner.

For __**External controller__** strategy, the throttle blip continues as long as the signal from the external controller is active, or until the {3} value is reached if the gear change does not occur by then.

After completing the throttle blip phase, the controller enters the post-shift cut phase, during which we can reduce torque instantly after engeging target gear using fuel/ignition cut. This allows us to avoid the effect of pushing the vehicle during downshifts.








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Parameters

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Timeout

The table specifying the maximum duration of the blip phase during the gears downshift strategy.

During a gear change from 3 to 2, the time is taken from column 3; from 2 to 1, it's taken from column 2, and so on.









---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Blip level

This table defines the value of throttle position change depending on the current gear. Value of blip level is added to current dbw target (if DBW Control type is chosen).

During a gear change from 3 to 2, the throttle position correction is taken from column 3; from 2 to 1, it's taken from column 2, and so on.

This table is not usable in the case of using the throttle kicker.


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Post shift torque reduction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Post shift torque recovery time

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##DBW target

While the **ALS** strategy is active, the **DBW target** table determines the electronic throttle position based on engine **RPM** and **Boost** pressure.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Torquereduction) 
##Parameters

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Torquereduction) 
##DBW target corr.

This table defines the throttle position correction depending on the desired torque reduction.




---

[Auto](help://Sport/Sport) [Auto](help://Sport/Gearshifts) [Auto](help://Sport/Gearshifts/Downshift_blip) 
##Post shift cut

After completing the throttle blip phase, the controller enters the post-shift cut phase, during which we can reduce torque through fuel/ignition cut. This allows us to avoid the effect of pushing the vehicle during downshifts.

{#1}


---

[Auto](help://Sport/Sport) 
##Paddle shift

The **__Paddle shift**__ strategy is used to operate sequential gearboxes using paddle shifts. This strategy is responsible for controlling the solenoids of the gear shift system, as well as managing the **__Gear shift**__ strategy.

For shifting from **__Neutral**__ to **__1st**__ or **__Reverse**__, from **__1st**__ to **__Neutral**__, and from **__Reverse**__ to **__Neutral**__, additional buttons **__N switch**__ and **__R switch**__ can be used.
The configuration of paddle shift switches and **__N**__ and **__R**__ switches can be found in the configuration  {1}.

!!**⚠It should be noted that some logging channels are recorded at a frequency of 25Hz, which may make it difficult to analyze times shorter than 40ms. The Paddle shift strategy and gearshift operate at a frequency of 500Hz (2ms).
--
**Upshift

When the paddle responsible for shifting up is pressed and conditions such as minimum engine RPM, vehicle speed, and clutch state (for gears N, R) are met, the solenoid responsible for shifting up is engaged.

The engagement time of the solenoid for shifts from 1 to 2 and higher gears is defined in the {2} table. The {3}  table defines the time after which the __**Gear shift__** strategy is activated, which will execute the torque reduction required for a proper gear change.

If the gear is changed in a time shorter than the timeout, the solenoid will be immediately disengaged. Otherwise, it will disengage after the timeout period.

For upshifting from __**Reverse__** and __**Neutral__**, the timeout time is taken from the {4} and {5} configuration. The gear shift strategy is not activated in these cases.

![sport/paddleUp.png](Images/sport/paddleUp.png)

--
**Downshift

When the paddle responsible for shifting down is pressed and conditions such as minimum engine RPM, vehicle speed, and clutch state (for gears 1, N) are met, the solenoid responsible for shifting down is engaged.

The engagement time of the solenoid for shifts from 2 and higher gears to lower gears is defined in the {6}. The {7} table defines the time after the solenoid is engaged at which the **__Gear shift**__ strategy is activated, performing the throttle blip required for a proper gear change.

If the gear is changed in a time shorter than the timeout, the solenoid will be immediately disengaged. Otherwise, it will disengage after the timeout period.

For downshifting from **__1st**__ and **__Neutral**__, the timeout time is taken from the {8} and {9} configuration. In these cases, the throttle blip strategy is not activated.

If the engine RPM for a given gear is higher than the RPM defined in the {10} table, the paddle shift strategy will not execute the request to shift to a lower gear.

--
**Logging channels:

* __ **Paddle shift status**__  - status of the **__Paddle shift**__ strategy
* __ **Paddle shift states**__  - states of the **__Paddle shift**__ strategy logged @ 100hz
* __ **Performing downshift**__  - the **__Paddle shift**__ strategy is executing a downshift
* __ **Performing upshift**__  - the **__Paddle shift**__ strategy is executing an upshift


**Meaning of Paddle shift  statuses:

* __**OK**__ - no errors
* __**Rejected - RPM**__ - RPM are too low or too high to perform paddle shift 
* __**Rejected - VSS**__ - vehicle speed is too high to perform paddle shift 
* __**Rejected - clutch**__ - the clutch pedal is not pressed to perform paddle shift 
* __**Rejected - gear out of range**__ - attempt to shift to a gear lower than Reverse or higher than the maximum number of gears


**Meaning of Paddle shift  states:

* __**Inactive**__ - the paddle shift strategy is inactive
* __**Performing downshift**__ - the paddle shift strategy performs downshift
* __**Performing upshift**__ - the paddle shift strategy performs upshift
* __**Solenoid down**__ - the state of downshift solenoid
* __**Solenoid up**__ - the state of upshift solenoid
* __**Preload**_ - paddle shift strategy perfomrs preload phase






 


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Parameters

{#1}



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Neutral selection

When the current gear is **__Reverse**__ or **__1st**__, shifting gears occurs without activating the **__Gear shift**__ strategy, and the solenoid engagement time is equal to the **__Pulse time.**__

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##First gear selection

When the current gear is **__Neutral**__ shifting up occurs without activating the **__Gear shift**__ strategy, and the solenoid engagement time is equal to the **__Pulse time.**__


Selection of the method for changing the gear from __**Neutral__** to __**Reverse**__: <br> <br>

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Reverse gear selection

When the current gear is **__Neutral**__ shifting down occurs without activating the **__Gear shift**__ strategy, and the solenoid engagement time is equal to the **__Pulse time.**__

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Down shift timeout

The maximum time the shift solenoid will be powered. If the gear change occurs earlier, the solenoid will be immediately turned off.

In the case of shifting from 4th to 3rd gear, the time is taken from the column for the 4th gear (and similarly for other gears).


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Dwon shift RPM limits

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Up shift preload

The **__Up shift preload**__ table defines the time after the solenoid for upshifting is powered when the **__Gear shift**__ strategy will be activated.

In the case of shifting from 2nd to 3rd gear (and subsequent gears), the time is taken from the column for the second gear (and subsequent gears).








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Up shift timeout

The maximum time the shift solenoid will be powered. If the gear change occurs earlier, the solenoid will be immediately turned off.

In the case of shifting from 2nd to 3rd gear (and subsequent gears), the time is taken from the column for the second gear (and subsequent gears).








---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Down shift RPM limits

This table defines the maximum RPM below which a downshift can occur. This protects the engine from exceeding maximum RPM during a downshift.

In the case of shifting from 4th to 3rd gear, the RPM limit is taken from the column for the 4th gear (and similarly for other gears).



---

[Auto](help://Sport/Sport) [Auto](help://Sport/Paddleshift) 
##Down shift preload

The **__Downshift preload**__ table defines the time after the solenoid for downshifting is powered when the **__Gear shift**__ strategy will be activated.

In the case of shifting from 4th to 3rd gear, the time is taken from the column for the 4th gear (and similarly for other gears).














---

[Auto](help://Sport/Sport) [Auto](help://Sport/Diffcontrol) 
##Diff control

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Launchctrl_) 
##Prestage

Activating the **__Prestage**__ state allows the configuration of distinct parameters tailored to the specific requirements of the initial phase of **__Launch control**__. 

These parameters include:
* Target boost pressure (Boost Target),
* Engine RPM,
* Ignition angle,
* Fuel enrichment,

The **__Prestage**__ state is the first stage of the **__Launch control**__ process. The system remains in this state, maintaining the set parameters until one of the following conditions is met:

* Boost pressure reaches the value defined in the Boost Target parameter.
* A predefined waiting time (Timeout) elapses.


Once either of these conditions is fulfilled, the strategy automatically transitions to the next state, called **__Active**__, continuing the **__Launch control**__ procedure.

{#1}


---

[Auto](help://Sport/Sport) 
##Trans brake

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sport/Sport) 
##Trans-brake

A trans-brake (short for transmission brake) is a crucial component in drag racing that allows a car to launch with maximum acceleration and minimal drivetrain shock.  This locks the transmission by simultaneously engaging both first gear and reverse gear, preventing the car from moving.

**Bump** staging is a technique where the car moves forward slightly with a quick pulse of the trans-brake release. 

**Creep** staging  is a technique that allows the car to slowly roll forward. Slow vehicle movement is achieved by controlling the trans-brake solenoid using PWM.



The diagram below shows the method of connecting the trans-brake to the device.

![transBrakeWiring.png](Images/transBrakeWiring.png)


**Logging channels:
* **__Trans-brake state__** - current status of the trans-brake strategy.


**Possible states:
* **__Inactive__** - strategy is inactive
* **__Active__** - startegy is active and transbrake is locked (100% DC)
* **__Active bump__** - startegy is active and performs **bump.**
* **__Active creep__** - startegy is active and performs **creep**.



{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/Pitlimiter) 
##Pit limiter

{#1}


---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Fuel correction 2

This table defines fuel dose corrections when the ALS strategy is in the active state.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##DBW target 2

While the **ALS** strategy is active, the **DBW target** table determines the electronic throttle position based on engine **RPM** and **Boost** pressure.

---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Cylidner cut 2

This table defines the percentage of ignition events/injections cut (depending on the value of the parameter __cut type__ in {1}/).








---

[Auto](help://Sport/Sport) [Auto](help://Sport/ALS) 
##Ignition correction 2

This table defines the ignition angle (or ignition angle correction depending on the value of the parameter __Ignition control method__ in {1}/).




---

