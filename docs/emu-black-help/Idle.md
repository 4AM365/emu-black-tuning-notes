##Idle

The idle strategy is responsible for controlling the engine at idle speed. To achieve this, the strategy uses ignition timing control and airflow control (via an actuator such as electronic throttle, stepper motor, or PWM solenoid) to maintain the desired idle RPM (Idle Target RPM).

The Idle strategy has the following states (**__Idle state__** log channel):

* **INACTIVE** - in this state, the strategy is inactive and does not affect engine operation. It occurs when the conditions for activating Idle are not met (PPS above activation threshold), or the engine is not running.  In the case where the EMU device is in **__Inactive**__ state (no engine rotation) and the selected actuator is other than DBW, the **__Airflow %**__ value is set to 0%. If the EMU is in a **__Running**__ state, the **__Airflow**__ value in this state is taken from the **__Armed state airflow**__ table. In the case of using electronic throttle, it is not controlled by the Idle controller in this state.


* **CRANKING** - the idle strategy transitions to the Cranking state when the device changes from Inactive to Cranking and attempts to start the engine. During this state, the Idle strategy controls the airflow into the engine using the defined actuator (e.g., DBW, stepper motor, etc.). If the accelerator pedal position exceeds __**Idle Off if pps over__**, the controller will be in an __**INACTIVE__** state, and the __**Idle air %__** value will be taken from the __**Armed state airflow__** table. In the case of an electronic throttle, this will be the value from the __**DBW Characteristic__** table.


* **AFTERSTART DELAY** - this state occurs after exiting the Cranking state for a time defined in the Idle/Activation/Afterstart delay parameter. A short delay in controller operation immediately after startup can have a beneficial effect on the initial phase of engine operation. In this state, the **__Airflow %**__ values are calculated identically as in the Cranking state.


* **ACTIVE** - the idle strategy is active and controls the engine RPM. This is achieved through ignition timing (Idle/Ignition) and airflow control. It's important to note that PID airflow control operates based on the error of the ignition timing controller rather than the error between target and actual engine RPM. This approach ensures good cooperation between the PID ignition timing controller and PID airflow controller. The current desired idle RPM is defined in the {1} table. In the **__Active**__ state, the ignition timing is determined by the idle ignition control strategy ({2}).  **__Airflow %**__ values are taken from the {3} table. In the case where the vehicle is moving and its speed is greater than the value of the {4} parameter, all PID controllers are disabled and the strategy operates in __**Open loop**__ mode. When the clutch is pressed ({5}) or when the current gear is neutral ({6}), the idle strategy switches back to **__Closed loop**__ mode.


* **ARMED** - the armed state occurs when the PPS is below the activation threshold, but the engine RPM is above the Idle target RPM + Ramp down offset. The Ramp down offset parameter is crucial for smooth and controlled engine deceleration when releasing the accelerator pedal. When the driver releases the accelerator pedal and the engine RPM starts to decrease below Idle target RPM + Ramp down offset, the Ramp down offset parameter begins to ramp down according to the Ramp down decay rate (RPM/s). This parameter is chosen experimentally for each engine to achieve the desired rate at which the controller transitions to idle speed. This concept is illustrated in the diagram below.  In the Armed state, the ignition timing is equal to the Target ign angle unless the Overrun strategy is active, in which case the ignition timing is taken from the Overrun strategy. The **__Airflow %**__ values are taken from the {7} table.

![rampdownOffset.png](Images/rampdownOffset.png)

* **DBW BLEND** - the DBW Blend state is a state in which there is a smooth transition between the throttle angle required to maintain the desired RPM and the throttle angle commanded by the driver through pressing the accelerator pedal. To give the driver the sensation that the engine responds to the accelerator pedal, a blend is introduced between the current throttle position, the commanded throttle position, and the Actuator/DBW blend point parameter. The operation principle of DBW Blend is illustrated in the diagram below:

![idleDBWBlend.png](Images/idleDBWBlend.png)

* **CYCLING IDLE** - the  cycling idle state is active if an alternative strategy for controlling idle speed called "cycling idle" ({8}) is activated. It allows for cyclic increases in engine RPM to enhance the efficiency of the water pump and thus improve the cooling of the motor.


* **DC overriden** - in this state, the Idle controller engages when the {9}  option is selected. Regardless of the selected actuator type and the state of the idle controller, it sets the airflow value to the Override airflow DC value. ** !!⚠Note! In the case of an electronic throttle, throttle control is unconditionally taken over by the idle controller, so this function should not be activated when the vehicle is in motion!


--

##How to properly set up idle control?

Properly configured idle settings should maintain the desired idle RPM under standard conditions without the need for PID controllers. 

!!⚠PID controllers are used to correct idle speed under varying conditions such as coolant temperature changes or engine load (e.g. when the rear window defroster or radiator fan is activated).

**Step 1**
Configure the {10} parameters. Ensure that __**Idle On if PPS below__**  is set lower than __**On if PPS above__**. For initial setup, the default values can be used.

**Step 2**
Configure the desired idle target based on coolant temperatur. This is done in the {11} table.
The colder the engine, the higher the idle RPM should be. If the engine is equipped with aggressive camshafts, oversized injectors, or a lightweight flywheel, the **__Idle target__** should be set higher than in a stock engine. Also configure the {12} table. This table defines how much the idle **__RPM**__ should be increased after engine startup. The colder the coolant, the more the **__RPM**__ should be raised during startup.

**Step 3** 
Configure the {13} table. Set ignition timing so that advancing or retarding timing affects engine speed in a predictable and symmetrical way. This is typically a few degrees before TDC. At this point, set all PID parameters (**__kP, kI, and kD__**) to 0.

**Step 4** 
Configure the airflow control method ({14}). This step is critical for proper idle control. In the {15} settings, choose the correct method of airflow control (e.g. DBW, PWM valve, etc.). Make sure the actuator can provide sufficient airflow for maximum idle RPM during cold start, and that it does not allow the engine to stall at minimum airflow (adjust **__DBW Target Min/Max**__ or **__Solenoid Min/Max DC**__ accordingly).

**Step 5**
Use the {16} airflow feature, start the engine and log engine **__RPM**__ at various coolant temperatures and airflow percentages. These values will help you fill in the {17} table. 

!!**⚠This table is essential for the correct operation of idle control!

**Important note**
If the engine speed is unstable with a constant airflow setting, it likely indicates problems such as incorrect fueling, wrong injection timing, oversized injectors, or idle RPM set too low to be stable. PID controllers cannot compensate for such issues. Ensure a stable lambda for each airflow value. Lambda < 1 usually results in more stable idle.


**Step 6**
 Fill in the {18} table. Use the logged data. Interpolate missing values from surrounding cells. At this point, changing the {19} should result in actual engine **__RPM**__ closely following the target. If not, adjust airflow values for the relevant temperature.

**Step 7**
 If idle is still unstable improve the fuel map in the idle region, use a lower {20}, or increase the {21} (a higher target usually results in better idle stability).

**Step 8** 
Tune the {22} table. If RPMs are not dropping as expected and the idle controller remains in **Armed** state , reduce values in the {23} table. This table controls how quickly RPM drops after throttle closure. Too high of a value will prevent **__RPM**__ from dropping effectively.

**Step 9**
Once stable idle has been achieved for all combinations of **__CLT**__ and idle targets, configure idle behavior when **__RPMs**__ are dropping in **__Neutral**__ gear. Briefly tap the throttle and observe how **__RPM**__ falls compared to the fall of the idle target affected by the **__Ramp fown Offset**__. Tune **__Ramp down decay rate**__ and **__Ramp fown delay**__ so that engine **__RPM**__ decreases in sync with the ramp down offset. This prevents PID saturation and ensures a smooth transition to idle without **__RPM**__ dipping below the target.

**Step 10** 
Configure the PID controller for ignition (Ignition PID) This should help minimize idle RPM deviation from the target.
The default values are a good starting point.

--

**Logging channels:
 	
* __** Idle control active**__  - when the idle state is Inactive, the idle control active log channel value is Yes.
* __** Idle state**__  - current state of the idle controller.
* __** Idle target**__  - current desired idle RPM.
* __** Idle ramp down offset**__  - current value of the Idle ramp down offset parameter (more information about this parameter can be found in the help section for Idle).
* __** Idle air %**__  - current desired airflow value.
* __** Idle effective DC %**__  - effective DC of a PWM solenoid control signal
* __** Idle motor step**__  - for a stepper motor actuator, this value specifies the current position of the stepper motor in steps.
* __** Idle Ignition target **__ - the expected ignition timing value the idle controller will aim for.
* __** Idle PID airflow % correction**__ - current correction of the airflow by the PID controller.
* __** Idle ignition correction**__  - current correction of the ignition timing by the PID controller or table.
* __** Idle airflow custom corr.**__ - User-defined air flow correction specified in the {24} table.
* __** Idle airflow custom corr. active**__ - Indicates whether the custom air flow correction is active.
* __** Idle cut percent **__ - current percentage value of cut events for spark/fuel cut based idle.
* __** Idle force open loop**__ - all PIDs are disabled, integral terms are reseted.




---

[Auto](help://Idle/Idle) 
##Activation

Activation parameters determine when the idle controller will be activated.
This depends on the position of the accelerator pedal.

{#1}


---

[Auto](help://Idle/Idle) 
##Cycling idle

The cycling idle strategy can be activated at any time (e.g., through the use of user functions and conditions such as CLT being greater than 103°C). It is used to cyclically increase the engine speed to the __Cut RPM level__, and then completely shut off the injectors / spark until the __Resume RPM__ is reached. By increasing the engine speed, we achieve a higher flow of coolant (higher water pump speeds) and in the case of using spark cut, the unburnt fuel flow can cool down the combustion chamber.

Activating this function overrides the basic Idle configuration, and the idle controller state changes to the __Cycling Idle__ state.

{#1}

The diagram below illustrates the operation principle of the algorithm in **Cut fuel** mode.

![cyclingIdleFuelCut.png](Images/cyclingIdleFuelCut.png)

The diagram below illustrates the operation principle of the algorithm in **Spark cut** mode.

![cyclingIdleSparkCut.png](Images/cyclingIdleSparkCut.png)


---

[Auto](help://Idle/Idle) 
##Target

The Target configuration allows defining the desired idle speed level depending on the engine temperature and enables increasing the idle speed level after the engine is started.



---

[Auto](help://Idle/Idle) [Auto](help://Idle/Target) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}

The following diagram illustrates the concept of the Ramp down offset.

![rampdownOffset.png](Images/rampdownOffset.png)





---

[Auto](help://Idle/Idle) [Auto](help://Idle/Target) 
##Idle Target RPM

The Idle target RPM table defines the desired idle speed level based on the coolant temperature (CLT). Lower coolant temperatures should correspond to higher desired idle speeds. The lowest possible stable idle speeds depend on various factors such as injectors, camshaft profiles, injection timing, lambda, etc.




---

[Auto](help://Idle/Idle) [Auto](help://Idle/Target) 
##Afterstart RPM increase

This table allows for adjusting the desired idle speed after engine startup. On the X-axis, we have the time since engine startup, and on the Y-axis, we have the coolant temperature. Increasing the idle speed after engine startup should be higher for lower coolant temperatures, and it should decrease to 0 as the engine runtime progresses.


---

[Auto](help://Idle/Idle) 
##Ignition

Controlling idle speed by changing the ignition timing angle is highly effective and responsive in terms of engine reaction. For this reason, it is the primary method of idle speed control based on a PID controller. Depending on the error between the current RPM and the desired RPM (target RPM), this controller adjusts the ignition timing angle within the range defined in the Min/Max torque ignition angle tables.

It is crucial that the PID controller controlling Airflow % does not rely on RPM error but rather on the error between the current ignition timing angle and the angle defined in the Target ignition angle table. Thanks to this approach, the ignition PID controller and the airflow PID controller "cooperate" rather than "fighting" against each other.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Ignition PID

Parameters of the PID controller controlling ignition timing angle in the idle strategy:

When all coefficients are set to 0, the controller is disabled, and the ignition timing angle is taken solely from the Target ignition angle table.

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Max torque ign. angle

This table defines the maximum ignition timing advance angle depending on the Target RPM that the PID controller can set. It is assumed that this angle represents the maximum torque angle for the idle strategy and the desired RPM.

For each cell, this angle should be greater than the angle from the {1} table.

!!** ⚠ The max torque ignition angle must always be higher  than the values from the__ {2} angle map.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Min torque ign. angle

This table defines the minimum ignition timing advance angle depending on the Target RPM that the PID controller can set. It is assumed that this angle represents the minimum torque angle for the idle strategy and the desired RPM.

For each cell, this angle should be smaller than the angle from the  {1} table.

!!** ⚠ The min torque ignition angle must always be lower than the values from the__ {2} angle map.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Target ign. angle

The desired ignition timing advance angle that the airflow PID controller will aim for. This angle serves as the base angle for the idle controller, which is modified by the ignition PID controller. It is important for this angle to be in the middle of the min/max torque ignition angle range. This ensures optimal engine response to ignition timing changes.

!!** ⚠ The target ignition angle value must always be lower than the max torque ignition angle and higher than the min torque ignition angle!




---

[Auto](help://Idle/Idle) 
##Airflow

The amount of airflow entering the engine is a fundamental parameter (alongside ignition timing and lambda) determining engine speed during idle strategy operation. The airflow quantity can be controlled using an electronic throttle (in which case, during idle, control over the throttle is assumed by the idle controller) or, in the case of mechanical throttles, etc., using additional actuators such as PWM valves, stepper motors, etc.

The key to the correct operation of the engine at idle is the proper configuration of the actuator, correct definition of the Active state airflow and Armed state airflow tables. It is also important to ensure that the VE (Volumetric Efficiency) map in the full idle range is properly defined and that the lambda value in this range is stable (lambda instability will cause RPM fluctuations).

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Actuator

Actuator options allow for the selection of the appropriate actuator and its configuration:

{#1}

In the case of an electronic throttle, the Air flow % affects the throttle position within the range from **__DBW Target min**__ to **__DBW target max**__. For PWM solenoids, it ranges from **__Min DC**__ to **__Max DC**__, and for stepper motors, it falls within the **__Stepper step range**__.


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Airflow PID

The Airflow PID enables the control of the intake airflow using a feedback loop with a PID controller. It is crucial to note that this controller operates on the error between the desired ignition timing angle and the current angle. Therefore, to ensure the proper functioning of the Airflow PID controller, it is necessary to activate and configure the Ignition PID controller or ignition correction table as well. Additionally, it should be remembered that changes in engine speed through adjustments in the intake airflow are relatively slow, and overly aggressive PID controller settings may lead to significant RPM oscillations.

!!**⚠Always start tuning idle control by setting up the ignition control parameters first, and only then proceed to adjust the airflow PID.

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Active state air flow

The __**Active State Airflow**__ table defines the **__Airflow %**__ depending on the desired **__Target RPM**__ and engine temperature **__CLT**__. As the engine temperature (**__CLT**__) decreases, a higher **__Airflow %**__ is needed to achieve the desired RPM. To set up this table, you should start the engine when it's cold and, for each engine temperature, adjust the RPM target (preferably to values defined on the Y-axis) while setting the **__Airflow %**__ to achieve RPM as close as possible to the expected values. It is recommended to disable the **__Ignition PID**__ (by setting all coefficients to 0) or adjust the airflow to ensure that the ignition angle is as close as possible to the target ignition angle during this setup process.

During the setup of this table, it is essential to monitor the Lambda value and ensure that it is stable and within the expected range. Any changes in the Lambda value will affect the engine RPM.

In the case of an electronic throttle, the Air flow % affects the throttle position within the range from **__DBW Target min**__ to **__DBW target max**__. For PWM solenoids, it ranges from **__Min DC**__ to **__Max DC**__, and for stepper motors, it falls within the **__Stepper step range**__.

!! **⚠This table is crucial for the proper functioning of idle control. It should be correctly set for a wide range of RPM and coolant temperatures, as it will enable the correct operation of the strategy during the idle target ramp.

To configure this table, the engine should be warmed up to operating temperature. Then, by setting various idle targets, both the value in this table and the VE map should be adjusted to achieve the desired lambda value. After cooling down the engine, this table should be built for different temperatures.

!!**⚠A stable lambda value during idle operation is crucial for maintaining idle stability.
















---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##DC VE correction

In the case of engines using the Alpha-N strategy for fuel injection calculation along with an additional solenoid controlling airflow during idle, any changes in airflow will not directly affect the engine load. However, this issue can be compensated for using the Airflow VE Correction map. This map adjusts the Volumetric Efficiency (VE) based on the Airflow %. By adjusting the VE, the fuel injection calculation can be appropriately compensated to reflect changes in airflow, ensuring proper fuel delivery and engine performance. 

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##DSG DC correction

In the case of a DSG transmission, it transmits current torque losses to the controller (e.g., during creeping). This enables the compensation of increased engine load by increasing airflow.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Armed state air flow

When the activation condition for Idle is met (PPS < Idle On if PPS below), but the RPM is higher than __ Target RPM + Ramp Down Offset, the idle controller transitions to the ARMED state. In this state, the Airflow % is defined in this table.

Values should be chosen to induce a decrease in engine speed, but not too rapidly (especially within the desired RPM range), enabling a smooth transition to idle RPM.

** Excessively high values in the Armed state airflow table may prevent the engine from reducing RPM and entering the Active state.

In the case of an electronic throttle, the Air flow % affects the throttle position within the range from **__DBW Target min**__ to **__DBW target max**__. For PWM solenoids, it ranges from **__Min DC**__ to **__Max DC**__, and for stepper motors, it falls within the **__Stepper step range**__.


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##PWM Batt. corr.

In the case of PWM solenoids, this table adjusts the pulse width modulation (PWM) duty cycle, compensating for voltage changes in the system.


---

[Auto](help://Idle/Idle) 
##Spark / Fuel cut

In high-performance engines, there isn't always the possibility to install a solenoid controlling additional air. In such cases, one can set a minimal opening of the mechanical throttle (or electronic throttle if someone wants to have idle speed control of this type) allowing to achieve higher RPMs than expected.

The RPM control to reach the RPM target is achieved by cutting off fuel or ignition, utilizing a PID controller.

It's important to remember that cutting off ignition leaves unburned fuel, which can lead to fouling of the spark plugs.

@@!!⚠ Please note! The Spark / Fuel Cut function disables idle speed control via the actuator. The Idle Air % value is set to 0%.


---

[Auto](help://Idle/Idle) [Auto](help://Idle/SparkFuelcut) 
##Cut parameters

Parameters under "Cut" define how the fuel or spark cut is implemented in the idle control strategy:

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/SparkFuelcut) 
##Cut PID

The Cut PID defines the parameters of the PID controller controlling the cutting of ignition events or fuel injections to maintain the desired idle RPM.

These parameters collectively determine how aggressively the fuel or spark cuts are applied to maintain the target idle RPM.

{#1}


---

[Auto](help://Idle/Idle) 
##Idle

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Airflow VE correction

In the case of engines using the Alpha-N strategy for fuel injection calculation along with an additional solenoid controlling airflow during idle, any changes in airflow will not directly affect the engine load. However, this issue can be compensated for using the Airflow VE Correction map. This map adjusts the Volumetric Efficiency (VE) based on the Airflow %. By adjusting the VE, the fuel injection calculation can be appropriately compensated to reflect changes in airflow, ensuring proper fuel delivery and engine performance. 


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##DSG airflow correction

In the case of a DSG gearbox, it sends information about the torque losses within the transmission (for example, these increase during creeping). This table allows for an increase in airflow when the load on the gearbox rises, which helps maintain the set engine speed.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Override

If we want to test different **__Airflow %**__ values regardless of the current state of the idle controller (for example, if we want to test a PWM valve or a stepper motor), we can activate this option. 

!! **⚠Note! In the case of an electronic throttle, throttle control is unconditionally taken over by the idle controller, so this function should not be activated when the vehicle is in motion!

!! **⚠For PWM-controlled solenoids, an Airflow % value of 0 means that the Duty Cycle (DC) will be equal to the Solenoid minimum DC, and a value of 100% means that the DC will be equal to the Solenoid maximum DC.

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Custom air flow correction

This table allows for airflow correction based on user-defined conditions ({1}). A value of 0 means no correction.

!! **⚠Note! Custom correction is used only in **Idle Active** state.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Custom correction

Custom correction allows for additional adjustment of Airflow % using a 3D table with defined axes. An example application is increasing airflow when the AC compressor is activated.

!! **⚠Note! Custom correction is used only in **Idle Active** state.

{#1}


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Target) 
##DSG target correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Target) 
##DSG target increase

In the case of a DSG transmission, it sends information regarding the torque losses within the gearbox (for example, these increase during creeping). This table allows for an increase in idle speed when the load on the transmission rises, which enables a smooth start from a standstill.


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##DBW blend point

This table defines the throttle position value at which the idle strategy is exited. The operation principle of DBW Blend is illustrated in the diagram below:
![idleDBWBlend.png](Images/idleDBWBlend.png)


---

[Auto](help://Idle/Idle) [Auto](help://Idle/Airflow) 
##Inactive state air flow

The **__Inactive airflow table__** defines the stepper motor opening or the DC value for PWM-controlled solenoids when the **Idle control** is in the **inactive state**. This table has no effect on the operation of the electronic throttle.

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Ignition corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Ignition correctopm

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Idle/Idle) [Auto](help://Idle/Ignition) 
##Ignition correction

The **__Idle ignition correction**__ map is used when the **Control type** parameter in the {1} settings is set to **__Use correction table**__. Depending on the current error (**__RPM - Idle RPM target**__), the table defines the correction of the ignition advance angle relative to the value defined in the {2}  table. The final ignition advance angle is clamped to the values defined in the {3} and {4} tables. This correction is only active when the engine is in the idle active state.

For error values greater than zero, the correction values should be negative (to reduce torque), while for negative error values, the correction should be positive (to increase torque).












---

