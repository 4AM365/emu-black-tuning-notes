##Engine start

During the operation of the EMU device, we can distinguish the following device states:

* **INACTIVE** - the device is turned on, there is no signal from the position sensor / crankshaft, fuel is not supplied, and no spark is generated.
* **CRANKING** - this is the state in which the engine revolutions usually oscillate around 200 rotations, and the controller tries to start the engine by dosing fuel and generating sparks. The transition to the next state occurs when the engine speed exceeds the Cranking threshold.
* **AFTERSTART** - this is the state after starting the engine in which the Afterstart fuel correction is active.
* **RUNNING** - proper engine operation.


The set of parameters and tables in the __Engine start__ category is responsible for starting the engine, especially for fuel dosing during startup.
The basic fuel dose is calculated in the same way as in normal engine operation (using the VE table value and fuel dose corrections), with the difference that we can scale the fuel dose using the {1} table.
This table is responsible for fuel dosing during startup (__Cranking__ state). It is preferred to decrease the fuel dose (decrease the values in the table) with subsequent engine revolutions. Additionally, the lower the coolant temperature (CLT), the more fuel is needed due to its poorer evaporation.
Additionally, in the Cranking state, the device takes the Lambda target value from the Cranking parameters rather than from the 3D Fueling/Lambda target table.

To ensure the fastest engine startup, a so-called prime pulse can be applied ({2}), which is an additional fuel dose injected when the first impulses from the crankshaft or camshaft reluctor ring appear. This facilitates startup because when the ignition system is synchronized and the first spark appears, vaporized mixture will be available. In the case of __Prime pulse__, all injectors deliver a simultaneously defined amount of fuel (dependent on the coolant temperature).

Additionally, to speed up engine startup, (in the case of triggers with missing or additional teeth) you can select in the ignition outputs configuration ({3})) options the engine startup mode in "wasted spark" mode, which causes the coils to be activated in pairs during startup, and the controller does not have to wait for synchronization with the crankshaft reluctor sensor.



---

[Auto](help://Enginestart/Enginestart) 
##Afterstart

The __Afterstart enrichment__ is an increase in the fuel dose that is active when the engine speed exceeds the __Cranking threshold__. The __Afterstart enrichment__ lasts until the enrichment value reaches 0% or until the maximum time defined on the X-axis of the __Engine runtime__ table elapses. At that point, the device transitions from the __Afterstart state__ to the __Running state__.







---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Afterstart) 
##ASE table 1

The table defines the percentage enrichment of the fuel dose expressed in percentages (0% indicating no enrichment) during the __Afterstart state__.  A value of 0% or an engine runtime greater than the maximum time defined on the X-axis results in a transition of the device state from **__Afterstart**__ to **__Running**__.

In the case of using fuel with variable ethanol content and utilizing the Flex Fuel Ethanol Content Sensor, it is possible to create two tables, **__ASE#1**__ and **__ASE#2**__, for pump gas and fuels such as E85/E100, respectively. Then, their values can be blended depending on the percentage of ethanol in the fuel.
To achieve this, the Flex Fuel sensor must be activated, and the blending map ASE ({1}) in __Tables switching_ options must be configured.

---

[Auto](help://Enginestart/Enginestart) 
##Cranking

The parameters in the Cranking group are directly responsible for engine startup. The proper settings of these parameters determine the smooth startup of the egnie in all weather conditions.






---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Parameters

The Cranking parameters window allows for defining basic parameters enabling engine startup.

{#1}


---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Cranking fuel 1

The __Cranking fuel__ table defines the scale by which the calculated fuel dose should be changed based on the coolant temperature and engine revolutions. It is important to emphasize that a value of 0% means no change to the calculated dose, while 100% represents a doubling of the calculated fuel dose, and so on.

**__The main VE table is used for calculating the base fuel dose in cranking state! 

The fuel dose at startup also depends on the Lambda target parameter in the Cranking/Parameters menu. The smaller the Lambda target value, the larger the fuel dose will be delivered.

In the case of using fuel with a variable ethanol content, it is possible to create two Cranking fuel tables, one for pump gas and one for the maximum predictable ethanol content, and then blend them depending on the reading from the Flex Fuel sensor.
This allows for optimal starting on both pump gas and E85 or even E100 fuel.
To achieve this, the Flex Fuel sensor must be activated, and the blending map FF Crank. fuel ({1}) in Tables switching options must be configured. 

![crankingFuel.png](Images/crankingFuel.png)


---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Idle air flow

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Fuel TPS scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Prime pulse

This table defines an additional fuel dose that is injected when the first impulses from the crankshaft or camshaft reluctor ring appear. This facilitates startup because when the ignition system is synchronized and the first spark appears, vaporized mixture will be available. In the case of Prime pulse, all injectors simultaneously deliver a predefined amount of fuel (dependent on the coolant temperature).

**The prime pulse is not visible on the Injector PW log channel! It can only be observed using the internal Scope.**










---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Start delay

The start delay table defines by how many crankshaft revolutions to delay the engine start based on the coolant temperature. This feature can be used to build oil pressure before starting the engine.





---

[Auto](help://Enginestart/Enginestart) 
##Warmup

In order to ensure proper operation of a "cold engine" (when the coolant temperature has not reached the operating temperature), it is necessary to apply warm-up enrichment. This allows for compensating for the fact that fuel evaporation is significantly worse at low temperatures compared to operating temperatures, and the increased amount of fuel delivered aims to compensate for this phenomenon. Additionally, modifying the lambda target (enrichment) for a cold engine enables correct operation even when using _Short term trim_ strategy (closed-loop fuel control).

In the case of using fuel with variable ethanol content and utilizing the Flex Fuel Ethanol Content Sensor, it is possible to create two Warmup tables ({1}), one for pump gas and one for fuels such as E85/E100, respectively. Then, their values can be blended depending on the percentage of ethanol in the fuel.

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Warmup) 
##Warmup 1

The __Warmup__ table allows for enriching the fuel mixture depending on the coolant temperature and load. The lower the coolant temperature, the greater the enrichment, aiming to compensate for poorer fuel evaporation at lower temperatures.

A value of 0% indicates no correction, 100% indicates twice the amount of fuel, -50% indicates 50% of the calculated dose, and so on.

In the case of using fuel with variable ethanol content and utilizing the Flex Fuel Ethanol Content Sensor, it is possible to create two Warmup tables, one for pump gas and one for fuels such as E85/E100, respectively. Then, their values can be blended depending on the percentage of ethanol in the fuel.






---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Warmup) 
##λ target corr. 1

The __Lambda  target correction__ table allows for adjusting the Lambda target values of the fuel mixture based on the coolant temperature and load.





---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Afterstart) 
##ASE table#1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Cranking fuel #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Warmup) 
##Warmup #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Warmup) 
##λ target corr. #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Fuel TPS correction

This table allows for the implementation of the so-called Anti-flood strategy, which involves the device suspending fuel delivery in the event of an open throttle. This action clears the combustion chamber and cylinder walls of excess fuel.


---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Cranking) 
##Cranking airflow

This table defines the throttle angle (in the case of DBW) or the position of the stepper motor or DC solenoid controlling the airflow during the __Cranking__ state.

A higher value corresponds to more airflow being delivered to the engine during startup.
It should be noted that in the case of electronic throttle, a value of 0% indicates opening the throttle to the Idle/Airflow/Actuator/DBW target min value, and a value of 100% indicates the Idle/Airflow/Actuator/DBW target max value ({1})

In the case of an electronic throttle, the **__cranking air flow %**__ affects the throttle position within the range from **__DBW Target min**__ to **__DBW target max**__. For PWM solenoids, it ranges from **__Min DC**__ to **__Max DC**__, and for stepper motors, it falls within the **__Stepper step range**__.


---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Warmup) 
##Lambda target corr. 1

The __Lambda  target correction__ table allows for adjusting the Lambda target values of the fuel mixture based on the coolant temperature and load. It is an adder. The negative values make the Lambda target richer. 
 

---

[Auto](help://Enginestart/Enginestart) [Auto](help://Enginestart/Afterstart) 
##Ignition lock

Ignition lock during engine start enforces a fixed ignition advance angle for a defined time after exiting the cranking state. For some engines, this improves engine smoothness immediately after startup.

**Logging channels:
* __  **Ign. afterstart lock**__ - Indicates whether the ignition afterstart lock is active..


{#1}


---

