##Traction control

**Traction control** allows for the reduction of engine torque when wheel slip is detected. The EMU supports two algorithms for detecting wheel slip:

* **RPM based** - This algorithm is based on the increase in engine RPM and is used when it is not possible to measure the speed of the **Driven** and **Non-driven** axles.


* **Speed based** - This algorithm is based on the difference in speed between the **Driven** and **Non-driven** axles. It requires axle speed sensors or information from the ABS system regarding the speed of individual wheels.


More information about the operation of these algorithms can be found in the corresponding Help categories.


**Logging channels:
 	
* __** TC status**__ - the current status of the Traction control strategy.

* __** TC intervention**__ - the Traction control strategy is reducing engine torque.

* __** TC dRPM Raw**__ - the change in engine RPM over a unit of time defined by the Sensitivity parameter.

* __** TC dRPM**__ - the change in engine RPM corrected by all adjustments.

* __** TC user rotary pos**__ - the position of the rotary switch defined in General/Rotary switch.

* __** Driven axle speed**__ - the speed of the vehicle's driven axle (defined in {1}).

* __** Undriven axle speed**__ - the speed of the vehicle's undriven axle  (defined in {2}).

* __** TC slip**__ - the slip between the axles.

* __** TC slip target**__ - the maximum allowable slip between the axles.

* **__TC torq. reduction**__ - the current torque reduction request.



**Meaning of  TC statuses:

* **__Disabled__** - the strategy is not activated in the device configuration.

* **__Inactive - switch off__** - the strategy is turned off by the user.

* **__Inactive - below RPM__** - the engine speed is below the minimum RPM defined in the strategy settings.

* **__Inactive - below VSS__** - the vehicle speed is below the minimum speed defined in the strategy settings.

* **__Inactive - gear shift__** - the strategy is inactive due to the activity of the Gear Shift strategy.

* **__Inactive - ESP__** - The strategy is inactive because there is no torque limitation request from the ESP system.

* **__Active - differential__** - the strategy is active in Diff mode.

* **__Active - percent__** - the strategy is active in Percent mode.

* **__Active - RPM based__** - the strategy is active in RPM based mode.
* **__Active - ESP__** - the strategy is active, The strategy is active; the ESP system has issued a request to reduce torque.
<br>




---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##General

{#1}


---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##Speed based

This strategy is based on reducing torque by measuring the difference in speed between the front and rear axles of the vehicle. It is the preferred method as it yields better results compared to the **RPM-based** method. It requires axle speed information, which can come from separate sensors or from the ABS system (individual wheel speeds).

To use this strategy, the parameters for **Driven** and **Non-driven** axle must be properly defined in the {1} configuration.

Depending on the vehicle's speed, one of two methods is used to calculate the current slip between the axles. 

At low speeds, the difference in speed between the axles is calculated as follows (**Diff method**):

** Slip[km/h] = Driven axle speed - Non drived axle speed

At higher speeds (e.g., above 10 km/h), the percentage method is preferred, and slip is calculated as follows (**Perc method**):  

**Slip[%] = Driven axle speed / Non drived axle speed \* 100

Then, using the values from the appropriate table for the method, Slip target, the error is calculated, which is used by the **PID controller** to reduce torque (if **Slip > Slip target**).

The coefficients for the **PID controller** are 2D tables that allow for different coefficients to be applied depending on the current gear. Additionally, for the proportional term of the **PID controller**, a correction based on the current throttle position can be applied using the {2} table.

The result of the **PID controller** is the **Torque reduction** value, which is used to limit torque: 

**Torque reduction = PID result \* (User torque reduction[Rotary Pos] + 100) / 100 

The calculated value of **Torque reduction** is used to limit engine torque. The amount of spark or fuel cut, as well as the ignition retard angle required for the desired **Torque reduction**, can be found in the {3} and {4} tables, respectively.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##Parameters

{#1}


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##PID parameters

{#1}


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##Diff

Each group contains specific information related to its respective area


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##Diff slip target

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##User slip scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##Gear sclale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kP

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kP gear scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kP tps scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kI

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kD

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##Perc.

Each group contains specific information related to its respective area


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##Perc. slip target

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##User slip scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##Gear scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kP

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kP gear scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kP tps scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kI

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kD

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##RPM based

**RPM Based** traction control uses the change in engine RPM as an indication of wheel spin. This strategy requires a **VSS** (Vehicle Speed Sensor) or gear sensor because the information about the current gear is essential for proper operation. In addition to gear detection, a rotary switch should be installed, which is used to control the sensitivity of traction control.

The main variable used in this traction control strategy is the value of **TC Delta RPM**. This value represents the current corrected change in engine **RPM**. When the **TC Delta RPM** is too high for a given gear, it indicates wheel slip, and torque reduction should be performed. Torque reduction is executed by cutting spark or injection events. The {1}  table is used to define different torque reductions for each gear.

Additionally, the sensitivity of traction control can be adjusted by a rotary switch or potentiometer, defined by the {2} 

Torque reduction is defined in the {3} 3D table. 

The Y-axis value (**TC Delta RPM**) is calculated as follows: 

**TC delta  RPM = TC dRPM RAW  \* (Gear scale[Current gear] + 100) / 100 \* (User correction[Rotary switch pos] + 100) / 100

Torque reduction is then calculated as follows: 

**Torque reduction = Torque reduction target[TPS][TC DELTA RPM] \* (User torque reduction[Rotary switch Pos] + 100) / 100

The calculated value of **Torque reduction** is used to limit engine torque. The amount of spark or fuel cut, as well as the ignition retard angle required for the desired **Torque reduction**, can be found in the {4} and {5} tables, respectively.




---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Parameters

{#1}


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Gear scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Adj. scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Torq. reduction target

This table defines the desired torque reduction based on **TPS** and **TC Delta RPM**. This value is then used in the {1} and {2} tables to calculate the ignition retard value and the percentage of ignition or fuel cut.


---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##User trq. red. scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##Ignition retard

This table defines how much the ignition timing will be retarded based on the **Torque reduction** value.

---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##Cut

This table defines the percentage of spark or fuel cut based on the **Torque reduction** value.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##Gear scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##User slip correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##Gear correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kP gear correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff) 
##kP tps correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##User slip correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##Gear correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kP gear correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_) 
##kP tps correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Gear correction

Depending on the current gear, it is possible to scale the value of TC dRPM Raw, resulting in the TC Delta RPM value. The formula for calculating TC Delta RPM is shown below:

**TC delta RPM = TC dRPM RAW \* (Gear scale[Current gear] + 100) / 100 \* (User correction[Rotary switch pos]+ 100) / 100


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##Adj. correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##User torque reduction

The table that defines the correction of the **Torque reduction** value based on the Rotary switch defined in {1}. The **Torque reduction** value is used in the  {2} and {3} tables to calculate the ignition retard value and the percentage of ignition or fuel cut.



---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##User slip correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##Diff. mode

At low vehicle speeds, even a small difference in speed between the axles would result in a very large percentage difference. In such cases, the **Diff. mode** strategy should be applied, where the **Slip target** is defined by the difference in speeds between the **Driven** and **Non-driven** axles. The speed below which the **Diff. mode** should be used is defined by the parameter {1}.










---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##Diff slip target

The table specifying the allowable difference in wheel speeds (**Driven axle speed - Non-driven axle speed**) above which torque reduction will occur.



---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##User slip correction

The table that allows scaling of the **Diff slip target** value depending on the position of the rotary switch defined in the parameters {1} 

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##Gear correction

The table that allows scaling of the **Diff slip target** value depending on the current gear.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##kP

The table defining the gain of the proportional term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##kP gear correction

The table defining the correction of the gain of the proportional term of the PID controller depending on the current gear.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##kP tps correction

The table defining the correction of the gain of the proportional term of the PID controller depending on the throttle position.


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##kI

The table defining the gain of the integral term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Diff_mode) 
##kD

The table defining the gain of the derivative term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) 
##Perc. mode

When the vehicle speed exceeds 10-15 km/h, the Perc. mode strategy should be applied, where the Slip target is defined by the ratio between the Driven and Non-driven axles.
The speed above which the **Diff. mode** should be used is defined by the parameter {1}.








---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##Perc. slip target

The table specifying the allowable percentage difference in wheel speeds (**Driven axle speed / Non-driven axle speed \* 100**) above which torque reduction will occur.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##User slip correction

The table that allows scaling of the **Diff slip target** value depending on the position of the rotary switch defined in the parameters {1} 

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##Gear correction

The table that allows scaling of the **Diff slip target** value depending on the current gear.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##kP

The table defining the gain of the proportional term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##kP gear correction

The table defining the correction of the gain of the proportional term of the PID controller depending on the current gear.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##kP tps correction

The table defining the correction of the gain of the proportional term of the PID controller depending on the throttle position.


---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##kI

The table defining the gain of the integral term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/Speedbased) [Auto](help://Tractioncontrol/Speedbased/Perc_mode) 
##kD

The table defining the gain of the derivative term of the PID controller depending on the engine speed.

---

[Auto](help://Tractioncontrol/Tractioncontrol) [Auto](help://Tractioncontrol/RPMbased) 
##User correction

Depending on the position of the Rotary switch defined in {1}, it is possible to scale the value of **TC dRPM Raw**, resulting in the **TC Delta RPM value**. The formula for calculating **TC Delta RPM** is shown below:

**TC delta RPM = TC dRPM RAW \* (Gear scale[Current gear] + 100) / 100 \* (User correction[Rotary switch pos]+ 100) / 100


---

[Auto](help://Tractioncontrol/Tractioncontrol) 
##Traction control

{#1}


---

