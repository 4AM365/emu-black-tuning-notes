##Boost

The **Boost** strategy is used to control boost pressure in engines equipped with a turbocharger. Boost pressure control can be achieved by using a PWM-controlled solenoid (both internal and external wastegate valves) or by using an electronic wastegate (controlled by an electric motor). It should be emphasized that in the case of an electronic EWG, we connect the control of the electric motor to the **HBRIDGE 2** output. 

!!**⚠The current draw by the motor must not exceed 8A.

To properly configure boost pressure control, the first step is to fill in the {1}, where the desired DC solenoid/position EWG should be set according to the required boost. The better this table is set, the more precise the boost control will be.

The next step is to configure the {2} table, which defines the desired boost depending on the throttle position and RPM. Additionally, limits can be set to restrict boost based on parameters such as CLT (Coolant Temperature), IAT (Intake Air Temperature), Oil Temperature, etc.

**It should also be emphasized that the Boost controller does not operate on absolute MAP pressure but on pressure relative to atmospheric pressure (Boost). To protect the engine from excessive boost (e.g., a broken hose controlling the wastegate), {3}  is available. **


**Logging channels:

* __   **Boost target**__ - current desired boost pressure
* __   **Boost target from table**__ - current desired boost pressure read from the Boost Target table
* __   **Boost DC**__ - current DC of the solenoid
* __   **Boost DC from table**__ - current DC of the solenoid read from the {4} table
* __   **Boost target limit**__ - the lowest value limiting the boost pressure from the {5} tables
* __   **Boost target correction**__ - boost pressure correction from the {6} tables
* __   **Boost output disabled**__ - information whether the solenoid control is disabled because the current MAP pressure is lower than the __Disable Output Under MAP__ parameter or __Disable solenoid func.__ is equal to true.
* __   **Boost out of margin**__ - information whether the current boost pressure is within the range defined in the {7} parameters
* __   **Boost source**__ - information whether Boost is calculated from the MAP sensor or from the pre-throttle pressure sensor
* __   **Boost lambda guard corr.**__ - boost pressure correction applied by the {8} engine protection strategy
* __   **Boost tables blend**__ - percentage value of blending between Boost Target 1 and Boost Target 2 tables
* __   **EWG position**__ - current position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG target**__ - current desired position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG output DC**__ - current DC controlling the electric motor of the wastegate, ranging from -100 to 100, where 0 means no current is driving the motor


The diagram below shows a typical way of connecting a PWM solenoid.
![boost/boost_pwm_schematic.png](Images/boost/boost_pwm_schematic.png)

The diagram below shows a typical way of connecting a electric wastgate.
![boost/boost_ewg_schematic.png](Images/boost/boost_ewg_schematic.png)














---

[Auto](help://Boost/Boost) 
##Parameters

{#1}


---

[Auto](help://Boost/Boost) 
##Boost PID

The basic configuration of the boost controller involves setting the {1}  table and the desired boost pressure as a function of RPM and throttle position ({2} tables). The PID controller allows for additional correction of the solenoid DC or the EWG position to ensure the controller can maintain the desired boost under all engine load conditions, intake air temperatures, ignition timing, etc.

The PID controller takes the value from the {3}  table and then modifies it within the range defined by the PID **__Output Min**__ and **__Output Max**__ parameters to minimize the error between the desired target and the actual boost pressure.

It should also be emphasized that the PID controller operates only when the actual **__Boost pressure**__ falls within the **__Boost Target**__ range defined by the {4} parameters.

If the PID is disabled, the strategy operates in what is known as **__Open Loop mode**__. The PID controller also has an option for linear extrapolation of future boost pressure, enabling a faster response from the PID controller. This is achieved using the Response Delay parameter. The diagram below graphically illustrates the function of the Response Delay parameter.

![boost/Boost_response_delay.png](Images/boost/Boost_response_delay.png)




{#1}


---

[Auto](help://Boost/Boost) 
##Margins

Margins define the area above and below the target within which the strategy controls DC to maintain the desired boost target. The diagram below illustrates the principle of margins.

![boost/boost_margins.png](Images/boost/boost_margins.png)


{#1}


---

[Auto](help://Boost/Boost) 
##Overboost protection

The overboost protection function protects the engine from the effects of excessively high boost pressure. The cause of excessive boost pressure can be incorrect EMU configuration or a mechanical failure of the wastegate or control system (solenoid, hose, etc.).


{#1}


---

[Auto](help://Boost/Boost) 
##Target limits

Target limits define the maximum allowable **__Boost target**__ depending on parameters such as **__CLT**__ (Coolant Temperature), **__IAT**__ (Intake Air Temperature), **__VSS**__ (Vehicle Speed), etc.




---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##CLT limit

The **__CLT limit**__ tablespecifies the maximum **__Boost target**__ value for a given temperature. If the **__Boost target**__ pressure exceeds the value from the **__CLT limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##Oil temp limit

The **__Oil temperture**__ limit table specifies the maximum **__Boost target**__ value for a given oil pressure. If the **__Boost target**__  pressure exceeds the value from the **__Oil temperature**__ limit table, it will be limited. Due to the fact that there are multiple maps limiting Boost target, the lowest value will always be selected.


---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##IAT limit

The **__IAT limit**__ tablespecifies the maximum **__Boost target**__ value for a given temperature. If the **__Boost target**__ pressure exceeds the value from the **__IAT limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##VSS limit

The **__VSS limit**__ tablespecifies the maximum **__Boost target**__ value for a given speed. If the **__Boost target**__ pressure exceeds the value from the **__VSS limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##EGT limit

The **__EGT limit**__ tablespecifies the maximum **__Boost target**__ value for a given temperature. If the **__Boost target**__ pressure exceeds the value from the **__EGT limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##Gear limit

The **__Gear limit**__ tablespecifies the maximum **__Boost target**__ value for a given gear. If the **__Boost target**__ pressure exceeds the value from the **__Gear limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetlimits) 
##Ethanol limit

The **__Ethanol limit**__ tablespecifies the maximum **__Boost target**__ value for a given ethanol content. If the **__Boost target**__ pressure exceeds the value from the **__Ethanol limit**__ table, it will be limited. Due to the fact that there are multiple maps limiting Boost, the lowest value will always be selected.

---

[Auto](help://Boost/Boost) 
##Target correction

Target corrections define the **__Boost target**__ scaling depending on parameters such as **__CLT**__ (Coolant Temperature), **__IAT**__ (Intake Air Temperature), **__VSS**__
 (Vehicle Speed), etc.




---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##CLT correction

The **__CLT correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current coolant temperature. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##IAT correction

The **__IAT correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current intake air temperature. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##VSS correction

The **__VSS correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current vehicle speed. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##EGT correction

The **__EGT correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current EGT. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##Gear correction

The **__Gear correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current gear. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetcorrection) 
##Ethanol correction

The **__Ethanol correction**__ table is responsible for the percentage correction of the **__Boost target**__ depending on the current ethanol content. A value of 0 means no correction, negative values decrease the boost (e.g., -50 means reducing the **__Boost target**__ by 50%), and positive values increase the **__Boost target**__. Due to the fact that there are multiple boost correction tables, the Boost target value is scaled by all of them.









---

[Auto](help://Boost/Boost) 
##Target blending

**__Target blending**__ allows control of boost depending on the position of a rotary switch or the value from an ethanol content sensor (Flex Fuel). This enables adjustment of the boost level according to the driver's needs.









---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetblending) 
##Rotary switch blend

To activate Rotary switch target blending, in the {1} options, select __Rotary Switch__ as the blend source. 

**__Blending%**__ = Rotary switch blend[Rotary pos] 
**__Final boost target**__ = Boost target 1 x  Blending% + Boost target 2 x  (100% - Blending%)




---

[Auto](help://Boost/Boost) [Auto](help://Boost/Targetblending) 
##Ethanol content blend

**__Ethanol content**__ blending allows blending between **__Boost Target 1**__ and **__Boost Target 2**__ tables depending on the ethanol content in the fuel.
To activate ethanol target blending, in the {1} options, select __Ethanol content__ as the blend source. 

**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final boost target**__ = Boost target 1 x  Blending% + Boost target 2 x  (100% - Blending%)




---

[Auto](help://Boost/Boost) 
##EWG

To control the boost using the electronic wastegate, connect its motor to the **HBRIDGE 2** output and its position sensor to the device's analog input. 
Then, configure the {1}. If the sensor status is anything other than OK, the **__HBRIDGE 2**__ output will be inactive. To maintain the concept that **100% Boost  DC** gives maximum boost and **0% Boost DC** gives minimum boost, the position sensor must be configured so that at 0% the **EWG** is fully open (exhaust gases bypass the turbocharger) and at 100% it is fully closed (all exhaust gases flow through the turbocharger).
Thanks to this approach, the configuration of the boost control is analogous to systems controlled using **PWM** solenoids.

The control of the **EWG** position is carried out using a PID controller. The **EWG DC** (Electronic Wastegate Duty Cycle) output ranges from **-100%** to **100%**, where **0%** signifies no movement of the actuator. Negative values command movement in one direction, while positive values command movement in the opposite direction.

{#1}

The diagram below shows a typical way of connecting a electric wastgate to EMU **BLACK HBRIDGE 2**.
![boost/boost_ewg_schematic.png](Images/boost/boost_ewg_schematic.png)

The diagram below shows a typical way of connecting a electric wastgate to Ecuamster Dual H-Bridge module.

![boost/boost_ewg_dual_hbridge_schematic.png](Images/boost/boost_ewg_dual_hbridge_schematic.png)

**Dual H-Bridge** configuration (configured via Light Client)

![boost/dual_HBridge_configuration.png](Images/boost/dual_HBridge_configuration.png)







---

[Auto](help://Boost/Boost) 
##Duty cycle feedback

The **__Duty cycle feedback**__ table is the primary map used to define the DC signal for the boost control solenoid (or the position of the electronic wastegate) for the desired **__Boost target**__ and **__RPM**__. The better this table is configured, the more stable and precise the boost control will be.









---

[Auto](help://Boost/Boost) 
##Boost target 1

The **__Boost target**__ tables define the desired boost pressure for different throttle positions (the smaller the throttle opening, the lower the boost should be) and engine **__RPM**__.

!!**⚠It should be emphasized that the values in the table represent Boost (ressure relative to atmospheric pressure), not MAP!
















---

[Auto](help://Boost/Boost) 
##Duty cyclce feedback

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Boost/Boost) 
##Boost target #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Boost/Boost) 
##Boost

{#1}


---

[Auto](help://Boost/Boost) 
##EWG PID

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Boost/Boost) [Auto](help://Boost/EWG) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Boost/Boost) [Auto](help://Boost/EWG) 
##EWG base DC.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Boost/Boost) 
##CO2

CO2 based boost control is a sophisticated system used in motorsport and high-performance applications to control turbocharger boost pressure with great precision. It uses compressed CO2 as an actuation medium, providing highly consistent and responsive control over the wastegate actuator. 

Below is a diagram for connecting a typical boost control system utilizing compressed CO2 as the control medium. This system consists of two solenoids and a wastegate dome pressure sensor.

![boost/co2.png](Images/boost/co2.png)


**!!⚠In the event that the wastegate dome pressure sensor is not connected or the EMU detects a malfunction in its operation (the Wastegate Dome Pressure Sensor State is different from "OK"), the device automatically sets the CO2 output duty cycle (CO2 Output DC) to -50%. This action causes the wastegate dome pressure to drop completely to 0 kPa gauge pressure, protecting the engine from potential damage.

When using the CO2-based control strategy, the target wastegate dome pressure is defined in the Boost Target table. Additionally, this strategy allows for the use of the Overboost Protection feature, which is based on monitoring the boost pressure.

Moreover, when the engine is not running, the CO2 Output Duty Cycle is automatically set to 0%, preventing unnecessary activation of the control system.

**Logging channels:

* __   **Boost target**__ - current desired wastegate dome pressure 
* __   **Boost target from table**__ - current desired wastegate dome pressure read from the Boost Target table
* __   **CO2 output DC**__ - the current duty cycle controlling the solenoids that regulate the pressure in the wastegate. A value of 0 indicates that both solenoids are closed. Negative values mean that the vent solenoid, which reduces the pressure, is open, while positive values indicate that only the pressure source solenoid is open.



{#1}


---

[Auto](help://Boost/Boost) 
##DC corrections

Each group contains specific information related to its respective area


---

[Auto](help://Boost/Boost) [Auto](help://Boost/DCcorrections) 
##Gear correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Boost/Boost) [Auto](help://Boost/DCcorrections) 
##Custom correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Boost/Boost) 
##Duty cycle corrections

The **Duty cycle corrections** section allows adjustment of the DC value read from the {1} table. In certain conditions (e.g. varying engine load depending on gear, or different boost behavior depending on IAT), correcting the DC value can significantly improve the performance of the boost controller.


---

[Auto](help://Boost/Boost) [Auto](help://Boost/Dutycyclecorrections) 
##Parameters

{#1}


---

[Auto](help://Boost/Boost) [Auto](help://Boost/Dutycyclecorrections) 
##Custom correction

This table allows correction of the DC value read from the {1}  table as a function of a user-defined log channel on the X-axis. This channel can be configured in the {2} section.



---

[Auto](help://Boost/Boost) [Auto](help://Boost/Dutycyclecorrections) 
##Gear correction

This table allows correction of the DC value from the {1} table based on the current gear.



---

[Auto](help://Boost/Boost) 
##EWG feedforward

In the case of an **EWG** with a return spring, this map defines the base value of the control current driving the wastegate actuator. A value of **–100%** corresponds to the full closing current of the **EWG**, while a value of **100%** corresponds to the full opening current of the wastegate. These values are defined as a function of EWG target and engine airflow. It can be assumed that the engine airflow is proportional to the exhaust gas mass (airflow + fuel mass), where the fuel mass plays only a minor role in the total exhaust mass.

---

