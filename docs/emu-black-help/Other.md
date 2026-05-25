##Other

The __**Other**__ category contains strategies that could not be assigned to any other category.










---

[Auto](help://Other/Other) 
##Debug functions

Each group contains specific information related to its respective area


---

[Auto](help://Other/Other) [Auto](help://Other/Debugfunctions) 
##PID

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Other/Other) [Auto](help://Other/Debugfunctions) 
##Debug variables

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Other/Other) 
##Cruise control

The **__Cruise control**__ strategy is used to maintain the desired vehicle speed without user intervention. To use this strategy, a brake switch must be connected and configured.

* !!**⚠During the operation of the Cruise Control strategy, pressing the brake pedal or clutch pedal immediately interrupts speed control.


* **!!⚠After activating the __Cruise control__ strategy, the brake pedal must be pressed during engine startup; otherwise, the fuel supply will be cut off.

* !!**⚠The Cruise Control strategy only works with engines equipped with an electronic throttle.


The strategy uses predefined throttle opening values for the desired speed, which are then modified using a PID controller. Therefore, the first step is to create a  {1}  table, where for a given gear and target speed, the throttle setting is adjusted to achieve the closest possible speed.

!!**⚠The values in the {2}  table should be set on a flat section of the road with the vehicle stationary.

When the **__Cruise control**__ strategy is active, the **__DBW target source**__ channel assumes the value **__Cruise control**__.

**Logging channels:

* __ **Cruise control state**__ - current state of the startegy
* __ **Cruise control target**__  - desired target speed
* __ **Cruise control PID corr.**__  - current PID correction 
* __ **Cruise control is in range**__  - indicates whether the difference between the current speed and the Cruise Control target speed is less than the Margin Below Target value, which activates the PID controller


**Meaning of control statue:

* __**Disabled**__ - the **__Cruise control__** strategy is disabled
* __**Inactive under vss**__ - the **__Cruise control__** strategy is inactive due to vehicle speed lower than  **__Minimum speed to activate
* __**Inactive**__ - the **__Cruise control__** strategy is inactive waiting for user activation
* __**Suspended**__ - the **__Cruise control__** strategy is suspended. This situation occurs when, during the operation of the **__Cruise control**__ strategy, the driver increases the vehicle speed (the requested throttle opening is greater than the throttle opening calculated by the strategy). When the driver decreases the throttle angle, the **__Cruise control__** strategy will be restored.
* __**Active**__ - the strategy is active and controls vehicle speed suing the electronic throttle



---

[Auto](help://Other/Other) [Auto](help://Other/Cruisecontrol) 
##Parameters

* !!**⚠ the operation of the Cruise Control strategy, pressing the brake pedal or clutch pedal immediately interrupts speed control. 


* !!**⚠After activating the Cruise control strategy, the brake pedal must be pressed during engine startup; otherwise, the fuel supply will be cut off. 


* !!**⚠The Cruise Control strategy only works with engines equipped with an electronic throttle. 


{#1}


---

[Auto](help://Other/Other) [Auto](help://Other/Cruisecontrol) 
##PID

The PID controller in the **__Cruise control**__ strategy modifies the feed-forward value from the {1} table to maintain the desired vehicle speed. 

The PID controller starts operating when the difference between the current speed and the **__Cruise control target speed**__ is less than the **__Margin below target**__ value. This prevents the PID controller from becoming excessively saturated if the current vehicle speed is much lower than the desired speed.

{#1}


---

[Auto](help://Other/Other) [Auto](help://Other/Cruisecontrol) 
##Throttle target

The strategy uses predefined throttle opening values for the desired speed, which are then modified using a PID controller. Therefore, the first step is to create this table, where for a given gear and target speed, the throttle setting is adjusted to achieve the closest possible speed.

!!**⚠The values in the table should be set on a flat section of the road with the vehicle stationary.


---

[Auto](help://Other/Other) [Auto](help://Other/Cruisecontrol) 
##Cruise control

{#1}

**Meaning of control statue:

* __**Disabled**__ - the **__Cruise control__** strategy is disabled
* __**Inactive under vss**__ - the **__Cruise control__** strategy is inactive due to vehicle speed lower than  **__Minimum speed to activate
* __**Inactive**__ - the **__Cruise control__** strategy is inactive waiting for user activation
* __**Suspended**__ - the **__Cruise control__** strategy is suspended. This situation occurs when, during the operation of the **__Cruise control**__ strategy, the driver increases the vehicle speed (the requested throttle opening is greater than the throttle opening calculated by the strategy). When the driver decreases the throttle angle, the **__Cruise control__** strategy will be restored.
* __**Active**__ - the strategy is active and controls vehicle speed suing the electronic throttle



---

[Auto](help://Other/Other) 
##Delayed turn off

The **__Delayed turn off**__ strategy allows maintaining ECU power after the ignition is turned off. This enables continued power supply to the electric water pump relay or the coolant fan. Additionally, the strategy has a safeguard against low voltage in the electrical system, and if the voltage drops below 10V, it will disable the power maintenance. 

!!**⚠For this function to work correctly, the EMU Battery +12V terminal must be connected directly to the battery, and the Ignition +12V to the ignition switch.

{#1}


---

[Auto](help://Other/Other) 
##Dyno

The EMU software contains a built-in dyno feature that allows users to generate a power and torque graph based on a road test. This function is useful when a chassis dynamometer is not available.

**How it works

1. Define the vehicle parameters 
2. Perform a full-throttle acceleration run on a flat road, using one selected gear (typically 3rd or 4th).
3. Record the log.
4. In the log window, select the region where the engine speed increases steadily (no wheelspin, clutch slip, or gearshift).
5. Right-click the selection and choose “Create dyno graph.”
6. The program will generate a separate Dyno window with calculated power and torque curves.

Optionally, you can overlay additional logged channels such as Lambda, Boost, or Intake Air Temperature (IAT).

**Notes

!!* Always perform tests on a safe, closed, and flat road.

* Use a single gear without shifting during the measurement.
* Ensure there is no wheel slip for accurate results.
* The accuracy of the dyno graph depends strongly on correct vehicle parameters and environmental conditions (wind, slope, tire pressure).


!!**This function is intended for tuning and comparison purposes. For certified measurements, use a professional chassis dynamometer.

{#1}


---

[Auto](help://Other/Other) 
##Internal buzzer

The EMU device has a built-in buzzer, which is activated when power is supplied and/or when maps are permanently saved in the device (F2). 

{#1}


---

[Auto](help://Other/Other) 
##Start/Stop switch

The **__Start/Stop**__ strategy allows starting and stopping the engine using a switch. To use this strategy, connect the starter relay to the EMU output and assign a button or buttons. If only the button is assigned to the **__Start switch input**__, pressing it again will activate the engine stop function (by cutting off the injectors).
Assigning only the **__Stop button**__ will activate the engine stop function.

{#1}


---

[Auto](help://Other/Other) 
##Tables switching

Each group contains specific information related to its respective area


---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##FF Ign blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##FF Lambda target blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##FF Crank. fuel blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##FF ASE blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##FF Warmup blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Other/Other) [Auto](help://Other/Tablesswitching) 
##Tables

The help content will cover essential details about channels in this particular group.
{#1}


---

[Auto](help://Other/Other) 
##Debug variables

!!**⚠Debug variables are only for developers. Please do not modify.

{#1}


---

[Auto](help://Other/Other) 
##PID monitor

The operation of each PID controller used in the strategies can be monitored using the **__Monitored P term**__, **__Monitored I term**__, and **__Monitored D term**__ log channels. These parameters indicate the current values of the P, I, and D components.

To monitor a particular PID controller, you need to select it from the PID controller list beforehand.

{#1}


---

[Auto](help://Other/Other) 
##Project comment

The comment is saved in the device memory and the project, allowing for comparisons between projects. 

!!**⚠The comment is limited to 64 characters.

---

