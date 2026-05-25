##DBW

**  !! ⚠ Please note! The electronic throttle control strategy is not intended for use on public roads!

The electronic throttle control strategy (drive by wire) allows for control of electronic throttles using a direct current motor. In a typical application, the throttle opening is commanded by an accelerator pedal, which has two built-in position sensors. One sensor is responsible for reading the current position of the pedal (PPS), while the second one is used to verify the correct operation of the first sensor.
A similar solution is found in the electronic throttle.

** !!⚠ For safety reasons, it is recommended to connect both sensors in both the throttle and the accelerator pedal.

In the EMU BLACK 2.xxx software versions, the accelerator pedal sensor was connected to the TPS input, while the throttle position sensor was connected to analog inputs 1 to 6.
In the 3.xxx versions, the throttle position sensor should be connected to the TPS input. To avoid the need for changes in the engine's electrical harness, it is possible to define analog inputs for the PPS and TPS sensors.

The diagram below shows a typical connection of the accelerator pedal and the electronic throttle.

![dbwWiringDiagram.png](Images/dbwWiringDiagram.png)


** Defining and calibrating sensors

Firstly, you need to configure the throttle position sensors and the accelerator pedal sensors.

The configuration of the PPS and TPS sensors can be found in the options menu under 
{1} and {2}

** !!⚠ Attention! In the event of any TPS or PPS sensor error, the electronic throttle strategy enters a fail-safe mode where the throttle motor power is cut off, resulting in the throttle being set to a position known as "limp mode."

** Throttle calibration

After properly connecting the EMU BLACK throttle, automatic throttle calibration is possible. To do this, go to the Tools menu and select the option "Automatic DBW calibration." Once the calibration is completed without any errors, the throttle should be ready for use.
--

**Throttle Calibration Step-by-Step Guide:

1. Connect the electronic throttle to the H-Bridge 1A and 1B outputs as per the diagram.

2. Connect the main throttle position sensor to the TPS input according to the diagram provided. It is crucial that the throttle position sensor voltage increases with the throttle angle.

3. If you want to use a control sensor (TPS check signal), connect it to an unused analog input.

4. Connect the accelerator pedal position sensor to a free analog input.

5. If you want to use a control sensor (PPS check signal), connect it to an unused analog input.

6. To configure the throttle position sensor, go to the Sensor Setup/TPS, PPS/TPS settings and select the analog input to which the main throttle position sensor (TPS main) is connected. If you followed the suggested diagram, the input should be TPS. Leave the other values at their default settings as they will be determined during the auto-calibration process.

7. To configure the throttle position sensor, go to the Sensor Setup/TPS, PPS/PPS settings. Select "Pedal" as the PPS function and assign the analog input to which the main accelerator pedal position sensor is connected (Main signal input). To calibrate the accelerator pedal, read the voltage value of the channel for the selected analog input when the pedal is not pressed and when it is fully pressed. Enter these voltages in the "Voltage for 0%" and "Voltage for 100%" fields, respectively. Then, fill in the "Main valid voltage min" and "Main valid voltage max" fields accordingly. For example, "Main valid voltage min" should be half the value of "Voltage for 0%", and "Main valid voltage max" should be half the sum of "Voltage for 100%" and 5V. If the voltage goes outside this range, it indicates a sensor error (short circuit, open circuit), and the DBW strategy will go into emergency mode.

8. In the DBW/Parameters options, select "Enable" and, if necessary, change the frequency of the throttle control signal.

9. Proceed to the Tools/DBW calibration tool menu and run the tool. If everything is properly connected, the calibration will be completed within a few seconds, and the throttle will respond to accelerator pedal inputs according to the values entered in the DBW characteristic table. To get more information about autocalibration refer to {3}

10. If you plan to use a throttle position check sensor, go back to the Sensor Setup/TPS, PPS/TPS settings and assign the appropriate analog input to the Check signal input field. Then, move the throttle and read the voltage values of the TPS check sensor analog input for various throttle positions. Enter these values in the TPS check tolerance map. For most throttles, reading values for the closed (0%) and fully open (100%) positions and entering them in the corresponding cells of the TPS check tolerance map, followed by interpolation, should be sufficient. During throttle operation, the strategy checks if the difference between the actual voltage and the voltage from the TPS check tolerance map falls within the Error tolerance parameter. Initially, we suggest setting this value to 5V and then checking the TPS check error channel in the log to determine the appropriate value for Error tolerance. If everything is calibrated correctly, this value should not exceed a few tenths of a volt.

11. If you plan to use an accelerator pedal position check sensor, follow the same steps as in point 10 but in the Sensor Setup/TPS, PPS/PPS settings.

!!**⚠ In most cases, throttle operation issues result either from problems with connecting the throttle motor and sensors or from the configuration of the throttle position sensors or pedal position sensors. If an error code for DBW (Drive-By-Wire) is visible in the __Check engine__ log channel, verify the statuses of the sensors: __TPS main status, TPS check status, TPS check error , PPS main status, PPS check status__, and __TPS check error__.


** Note: Ensure that all connections are properly made and double-check the wiring diagram before proceeding with the throttle calibration.
--
**Logging channels:

* __ **DBW target**__  - the current target that the throttle will aim to achieve. 
* __ **PPS**__ - the current position of the accelerator pedal.
* __ **TPS**__ - the current position of the throttle.
* __ **DBW targte blend percent**__ - the percentage value of blending between two characteristic maps. 0% means the value is taken from the DBW characteristic 1 table, 100% means the value is taken from the DBW characteristic 2 table.
* __ **DBW friction corr.**__ - the current DC correction resulting from the Friction characteristic table.
* __ **DBW Out. DC**__ - the duty cycle of the signal controlling the throttle electric motor.
* __ **DBW Target source**__ - status indicating the current strategy controlling the throttle.
* __ **DBW Delta error**__ - the current error between the throttle position (TPS) and the desired target (DBW target).
* __ **DBW characteristic #2**__ - the channel indicating which characteristic map is being used. In the case of blending between tables, this value is 1 if the blend value is greater than 50%.
* __ **DBW Override **__ - when the override DC or override target option is selected, this status indicates the current override.

* __ **TPS voltage**__ - the current voltage from the TPS sensor.
* __ **TPS main status**__ - status of the TPS main sensor.
* __ **TPS check status**__ - status of the TPS check sensor.
* __ **TPS check error**__ - error between the expected and actual voltage of the check sensor.

* __ **PPS Voltage**__ - the current voltage from the accelerator pedal sensor.
* __ **PPS main status**__ - status of the main PPS sensor.
* __ **PPS check status**__ -status of the PPS check sensor.
* __ **PPS check error**__ - error between the expected and actual voltage of the check sensor.



**Meaning of DBW target source status:

* **Target table
* **Override
* **Idle
* **Idle blend
* **DSG blip
* **CAN control
* **Launch control
* **Cruise control
* **Rev limiter
* **Overrun
* **Flat shift
* **Rev matching
* **Pit limiter
* **ALS
* **Rolling start
* **Gear shift

--

**DBW target priority

* **Override** (used by DBW overriden options)
* **Rev limiters** 
* **Gear cut**  (cut and blip)
* **CAN control**  
* **Rev matching**
* **DSG Blip** 
* **Overrun (disable when the cruise control is active)
* **Launch control**
* **ALS**
* **Cruise control**
* **Rolling launch control**
* **Flat shift**
* **Idle**
* **Idle blend**
* **Target table**


**Cruise control**
 If the target value from the table is higher than the target value from the cruise control (CC), the cruise control is suspended, allowing the user to accelerate. When the user releases the throttle (bringing the target below the CC control TPS position), the cruise control is resumed.



---

[Auto](help://DBW/DBW) ##Parameters

{#1}

--

**CAN control frame format

Freqency 100Hz

|ID|DLC|Byte0|Byte1|Byte2|Byte3|Byte4|Byte5|Byte6|Byte7|
|Any|8|Target H|Targt L|Gear|0|0|0|0|0|

* **__ID**__ - the message ID should be set in CAN ID field
* **__Target**__ - 0-1000, uint16 big endian
* **__Gear**__ - when the Gear sensor input is set to CAN, the current gear can be set via this message.

--
**Connecting the BMW S54 throttle to the EMU using the ECUMASTER DUAL H-BRIDGE CAN module.

!! ** ⚠ Important!

!! The **__DWB Out. DC__** at fully open throttle (**TPS 100%**) should be close to the value for the **80%-90%** position. If it is significantly higher, it may result from a too high voltage defined for the **TPS 100%** position or the throttle may require adjustment. Also, for the **TPS 0%**, DC should be close to the DC value for the **10–20% TPS** position.

!!**⚠ Excessively high DC will cause the throttle motor to overheat, which may lead to damage!


![DBW/dualHbridgeWiringDiagram.png](Images/DBW/dualHbridgeWiringDiagram.png)

!!** ⚠ The DUAL H-BRIDGE module must have firmware version 12.1 or higher.

For BMW S54 ITB the TPS is: PIN 1 - GND, PIN2 - Otput signal, PIN3 - Sensor ground
Below is the required DUAL H-BRIDGE configuration.


![DBW/dualHBridge.png](Images/DBW/dualHBridge.png)

To perform throttle auto-calibration, select __**BMW S54 ITB**__  from the __Throttle type__ dropdown list in the calibration tool window.

The EMU sends control information to the DUAL H-BRIDGE module via CAN using **ID 0x774**.
--

**Connecting the BMW S54 throttle to the EMU using the simple transistor circut.

It is possible to connect the BMW S54 ITB throttle using a simple control circuit built with a transistor and Schottky diodes. The schematic of the module is shown below.

!!** ⚠ Important!

!! The **__DWB Out. DC__** at fully open throttle (**TPS 100%**) should be close to the value for the **80%-90%** position. If it is significantly higher, it may result from a too high voltage defined for the **TPS 100%** position or the throttle may require adjustment. 

!!** ⚠ Excessively high DC will cause the throttle motor to overheat, which may lead to damage!

![DBW/DBW-direct.png](Images/DBW/DBW-direct.png)
For BMW S54 ITB the TPS is: PIN 1 - GND, PIN2 - Otput signal, PIN3 - Sensor ground


!!** ⚠ The module above should be connected to any H-Bridge output.














---

[Auto](help://DBW/DBW) 
##PID above limp position

PID above limp position enables the definition of PID controller coefficients within the electronic throttle's operating range from the Limp position to full throttle opening. Within this range, a spring provides resistance during throttle opening and allows for automatic return to the Limp position in the event of power loss.

{#1}

** Throttle control strategy

The throttle control strategy is based on a model that utilizes the Friction Characteristic and Spring DC Reference maps, as well as a PID controller. The PID controller parameters are defined separately for throttle movement from the neutral position (limp position) to full open (PID above limp position) and from the neutral position to full closed (PID below limp position).

If you want to accelerate the response of the throttle after auto-calibration, you can increase the Proportional Gain coefficient. However, setting it too high may result in overshooting the desired value or even causing throttle oscillation. If the throttle rapidly reaches the desired position, you can increase the Derivative Gain coefficient. Setting this coefficient too high may lead to throttle position oscillations.

The diagrams below illustrate the example operation of the throttle and the PID coefficients.

![](DBW/dbw_kp2_kd005.png 100% x 100%)
__Based on the coefficients provided above (kP=2, kI=50, kd=0.05), it is evident that the throttle is experiencing difficulty in reaching the desired target position.

![DBW/dbw_kp3_kd005.png](Images/DBW/dbw_kp3_kd005.png)
__Increasing the Proportional Gain coefficient to 3.0 has accelerated the throttle's ability to reach the target position from 400ms to 280ms.

![DBW/dbw_kp4_kd005.png](Images/DBW/dbw_kp4_kd005.png)
__ Increasing the Proportional Gain coefficient to 4.0 has accelerated the throttle's ability to reach the target position from 280ms to 110ms.

![DBW/dbw_kp5_kd005.png](Images/DBW/dbw_kp5_kd005.png)
__As seen above, further increasing the Proportional Gain coefficient to 5.0 has shortened the time to reach the target position to 90ms. However, this leads to overshooting the desired position.

![DBW/dbw_kp45_kd008.png](Images/DBW/dbw_kp45_kd008.png)
__Reducing the Proportional Gain coefficient and increasing the Derivative Gain coefficient has mitigated the issue of overshooting the target while still maintaining a short time required to reach it.


---

[Auto](help://DBW/DBW) 
##PID below limp position

PID below limp position enables the definition of PID controller coefficients within the electronic throttle's operating range from full closed position to the Limp position. Within this range, a spring provides resistance during throttle closing and allows for automatic return to the Limp position in the event of power loss.

{#1}

** Throttle control strategy

The throttle control strategy is based on a model that utilizes the Friction Characteristic and Spring DC Reference maps, as well as a PID controller. The PID controller parameters are defined separately for throttle movement from the neutral position (limp position) to full open (PID above limp position) and from the neutral position to full closed (PID below limp position).

If you want to accelerate the response of the throttle after auto-calibration, you can increase the Proportional Gain coefficient. However, setting it too high may result in overshooting the desired value or even causing throttle oscillation. If the throttle rapidly reaches the desired position, you can increase the Derivative Gain coefficient. Setting this coefficient too high may lead to throttle position oscillations.

The diagrams below illustrate the example operation of the throttle and the PID coefficients.

![](DBW/dbw_kp2_kd005.png 100% x 100%)
__Based on the coefficients provided above (kP=2, kI=50, kd=0.05), it is evident that the throttle is experiencing difficulty in reaching the desired target position.

![DBW/dbw_kp3_kd005.png](Images/DBW/dbw_kp3_kd005.png)
__Increasing the Proportional Gain coefficient to 3.0 has accelerated the throttle's ability to reach the target position from 400ms to 280ms.

![DBW/dbw_kp4_kd005.png](Images/DBW/dbw_kp4_kd005.png)
__ Increasing the Proportional Gain coefficient to 4.0 has accelerated the throttle's ability to reach the target position from 280ms to 110ms.

![DBW/dbw_kp5_kd005.png](Images/DBW/dbw_kp5_kd005.png)
__As seen above, further increasing the Proportional Gain coefficient to 5.0 has shortened the time to reach the target position to 90ms. However, this leads to overshooting the desired position.

![DBW/dbw_kp45_kd008.png](Images/DBW/dbw_kp45_kd008.png)
__Reducing the Proportional Gain coefficient and increasing the Derivative Gain coefficient has mitigated the issue of overshooting the target while still maintaining a short time required to reach it.


---

[Auto](help://DBW/DBW) 
##Overrides

These options allow manual setting of the throttle motor's DC, manual setting of the target, and enabling the **__Movement test**__ option, which moves the throttle from 0% to 100% and back to 0%. The **__PID tuning**__ option is used by the DBW autotune function. 

{#1}


---

[Auto](help://DBW/DBW) 
##CLT Limit table

This table defines the maximum throttle opening limit depending on the engine temperature (CLT). It allows limiting the engine power in case of very low temperatures.



---

[Auto](help://DBW/DBW) 
##Friction characteristic

This table defines the value added to the DC signal controlling the throttle motor when the throttle is not moving to overcome static friction. Additionally, this table is scaled by the Friction factor parameter from the **__PID above/below limp position**__ options.



---

[Auto](help://DBW/DBW) 
##Spring DC reference

This table defines the throttle motor duty cycle that neutralizes the resistance from the throttle's internal springs.



---

[Auto](help://DBW/DBW) 
##DBW Characteristic

The DBW characteristic table defines how the position of the accelerator pedal translates into the position of the throttle. This characteristic is very important from the perspective of driveability. Additionally, for low engine speeds, throttle opening can be limited in case of aggressive accelerator pedal input.




---

[Auto](help://DBW/DBW) 
##DBW wizard

A wizard guides users through the process of configuring parameters, simplifying complex setups


---

[Auto](help://DBW/DBW) 
##DBW autotune

The DWB autotune is used for automatic throttle calibration. Before starting the calibration, ensure that the throttle and its position sensor are correctly connected. We suggest setting 
{1} and {2} to **__None**__ during the calibration process. This allows the calibration to proceed even if the TPS or PPS check tolerance table is improperly calibrated.

Additionally, enable the strategy by selecting the **__Enable**__ option in **__DBW Parameters**__ and choose the **__PWM signal frequency**__ for the throttle motor (found under **__DBW Parameters / Output Frequency**__). If the frequency is not known, we recommend leaving the default value at 4000Hz.

To verify the throttle connection, use the {3} function. By activating the **__Override DC**__ option, you can directly control the throttle motor. Entering values in the **__DC Value**__ field should cause the throttle to move, which should be visible in the **__TPS channel**__. If changes in the DC value correspond with changes in the TPS position, the throttle is connected correctly.

In the __**DBW calibration tool**__, there is a dropdown list for selecting the throttle type, which optimizes the tool's operation. For typical throttles connected directly to the H-Bridge in the EMU, the default setting **__Standard throttle**__ should be used. When using the **__BMW S54 ITB**__ throttle, the **__BMW S54 ITB**__ option must be selected.

If everything is connected properly, the auto-calibration should proceed without major issues.
--
**Errors Signaled During Calibration

**Make sure the engine is not running
This message appears when engine rotation is detected during the throttle calibration attempt. Calibration can only be performed with the engine off.

**The position of the throttle doesn't move. Please check if the position sensor and electric motor are connected correctly
During the attempt to power the throttle motor, no voltage changes were noted on the throttle position sensor. Please check the motor connection and the configuration of the throttle position sensor (e.g., incorrectly assigned analog input).

**Please correct the setting for the PPS check signal as it causes a DBW error!
An error was detected in the accelerator pedal's "check" sensor. You can check the problem in the PPS check status log channel. We also suggest setting the PPS Check sensor input to None during calibration.

**Please correct the settings for the PPS main signal as it causes a DBW error!
An error was detected in the accelerator pedal's "main" sensor. You can check the problem in the PPS main status log channel.

**Please correct the settings for the TPS check signal as it is shorted to the ground
The TPS check sensor voltage was detected below the Check valid voltage min value. Please check the TPS check sensor settings, its connection, or set the TPS check sensor input to None during calibration.

**Please correct the settings for the TPS check signal as it is shorted to +5V.
The TPS check sensor voltage was detected above the Check valid voltage max value. Please check the TPS check sensor settings, its connection, or set the TPS check sensor input to None during calibration.

**Please correct the settings for the TPS main and check signal as it reports an error.
The defined difference in position between the TPS main and TPS check sensors exceeds the TPS voltage tolerance value. Please check the TPS voltage tolerance configuration and the TPS check tolerance table, or set the TPS check signal input to None during calibration.

**Please correct the settings for the TPS main signal as it is UNASSIGNED
No input has been defined for the TPS main sensor. Please configure the TPS main sensor correctly.

**Please correct the settings for the TPS main signal as it is shorted to the ground
The TPS main sensor voltage was detected below the Main valid voltage min value. Please check the TPS main sensor settings or its connection.

**Please correct the settings for the TPS main signal as it is shorted to +5V.
The TPS main sensor voltage was detected above the Main valid voltage max value. Please check the TPS main sensor settings or its connection.

**The throttle doesn't move from the limp position
The ECU does not detect throttle movement from the limp position. During the calibration attempt, no voltage changes were noted on the throttle position sensor. Please check the motor connection and the configuration of the throttle position sensor (e.g., incorrectly assigned analog input).

**The throttle doesn't move from 10% to 90%
During the calibration attempt, no voltage changes were noted on the throttle position sensor. Please check the motor connection and the configuration of the throttle position sensor (e.g., incorrectly assigned analog input).
--

**Variables Modified by the DBW Wizard

**__DBW / Parameters / Enable
**__DBW / Parameters / Disable when no RPM
**__DBW / Parameters / TPS limp postion voltage
**__DBW / Parameters / Integrator reset threshold
**__DBW / Parameters / Throttle plate speed limit
**__DBW / Parameters / Invert motor direction

**__Sensors and inputs / TPS,PPS/ Voltage for 0% 
**__Sensors and inputs / TPS,PPS/ Voltage for 100% 

**__DBW / __PID above limp position / Proportional gain
**__DBW / __PID above limp position / Integral gain
**__DBW / __PID above limp position / Derivative gain
**__DBW / __PID above limp position / Friction factor

**__DBW / __PID below limp position / Proportional gain
**__DBW / __PID below limp position / Integral gain
**__DBW / __PID below limp position / Derivative gain
**__DBW / __PID below limp position / Friction factor
--

**Tables Modified by the DBW Wizard

**__DBW / Spring DC reference
**__DBW / Friction characteristic



---

[Auto](help://DBW/DBW) 
##DBW blend

This table defines how the blending occurs between the **__DBW Characteristic 1**__ and **__DBW Characteristic 2**__ tables when using a rotary switch.
100 means that the value is taken from the **__DBW Characteristic 2**__ table, 0 means that the value is taken from the **__DBW Characteristic 1**__ table.

**DBW Target = (DBWCharacteristic1 x blend + DBWCharacteristic2 x (100 - blend)) / 100

---

[Auto](help://DBW/DBW) 
##DBW Characteristic #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://DBW/DBW) 
##DBW

{#1}

**Meaning of DBW target source statuses:

* **Target table** - the DBW target is taken from {1} table.
* **Override** - the DBW target is defined by {2} parameters.
* **Idle** - the  {3} strategy is controlling DBW target.
* **Idle blend** -the DBW target is controlled by {4} srategy.
* **DSG blip** - the DBW target is controlled by {5} strategy. 
* **CAN control** - the DBW target is controlled by CAN message.
* **Launch control** - the DBW target is controlled by {6} strategy.
* **Cruise control** - the DBW target is controlled by {7} strategy.
* **Rev limiter** - the DBW target is controlled by {8} strategy.
* **Overrun** - the DBW target is controlled by {9} strategy.
* **Flat shift** - the DBW target is controlled by {10} strategy.
* **Rev matching** - the DBW target is controlled by  {11} strategy.
* **Pit limiter** 0 the DBW target is controlled by {12} strategy.
* **ALS** - the DBW target is controlled by {13} strategy.
* **Rolling start** - the DBW target is controlled by {14} strategy.
* **Gear shift** - the DBW target is controlled by {15} strategy.

--

**DBW target priority

* **Override** (used by DBW overriden options)
* **Rev limiters** 
* **Gear cut**  (cut and blip)
* **CAN control**  
* **Rev matching**
* **DSG Blip** 
* **Overrun (disable when the cruise control is active)
* **Launch control**
* **ALS**
* **Cruise control**
* **Rolling launch control**
* **Flat shift**
* **Idle**
* **Idle blend**
* **Target table**


**Cruise control**

 If the target value from the table is higher than the target value from the cruise control (CC), the cruise control is suspended, allowing the user to accelerate. When the user releases the throttle (bringing the target below the CC control TPS position), the cruise control is resumed.



---

[Auto](help://DBW/DBW) 
##Opening speed scale

The **Throttle speed limit**, defined by the {1}  can be modified using the settings of this table. If the **Throttle speed limit** value is different from **No limit**, the values from this table affect the throttle opening speed as a function of engine RPM. 

This is particularly useful at low engine RPM, where limiting the throttle opening speed has a positive effect on maintaining the proper fuel film. The values from this table influence the throttle opening speed only when the **DBW target** is taken from the **DBW Characteristic table.**

---

[Auto](help://DBW/DBW) 
##Closing speed scale

The **Throttle speed limit**, defined by the {1}  can be modified using the settings of this table. If the **Throttle speed limit** value is different from **No limit**, the values from this table affect the throttle closing speed as a function of engine RPM. 

The values from this table influence the throttle opening speed only when the **DBW target** is taken from the **DBW Characteristic table.**

---

[Auto](help://DBW/DBW) 
##Boost target Limit

The table defines the maximum throttle opening as a function of boost. This allows limiting the throttle opening in case of excessive boost caused by the phenomenon known as boost creep.


---

