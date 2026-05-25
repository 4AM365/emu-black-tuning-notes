##Nitrous

The **Nitrous strategy **allows for the control of nitrous oxide injection. The following injection types are supported:

* **Dry** -  nitrous oxide is injected **without additional fuel**. Control is performed via an **On/Off** solenoid. Additional fuel is provided by the ECU based on the user-defined **NFR** (Nitrous to Fuel Ratio).

* **Dry progressive** - nitrous oxide is injected **without additional fuel**. Control is performed via a **PWM** solenoid, allowing for smooth power delivery. Additional fuel is provided by the ECU based on the user-defined **NFR** (Nitrous to Fuel Ratio). !!⚠This mode requires a solenoid designed for PWM operation.

* **Wet** - nitrous oxide is injected together with additional fuel (through a separate fuel nozzle). Control is performed via an **On/Off** solenoid. The **Nitrous to Fuel Ratio** is determined by selecting the appropriate **nitrous and fuel jets and applying additional user-defined dose (or dose reduction) through the primary injectors.

* **Wet progressive** - nitrous oxide is injected together with additional fuel (through a separate fuel nozzle). Control is performed via a **PWM** solenoid. The **Nitrous to Fuel Ratio** is determined by selecting the appropriate nitrous and fuel jets and applying additional user-defined dose (or dose reduction) through the primary injectors. !!⚠This mode requires solenoids designed for PWM operation.


**Calculated fuel dose for all modes takes into consideration fuel pressure and fuel ethanol content**

**!!⚠IMPORTANT: The vehicle's fuel system (fuel pump and injectors) must be capable of delivering additional fuel when the Nitrous system is activated.

**!!⚠IMPORTANT: Additional fuel can be provided only by primary injectors.Additional fuel can be provided only by primary injectors.

!!**⚠MPORTANT: When the rev limiter is active, the solenoid is turned off, and the additional fuel dose is set to 0.

The EMU supports a two-stage Nitrous system, which can be activated sequentially (e.g., the second stage activates after a predefined time during a 1/4-mile run).
Additionally, Stage 1 can be used during Launch Control.

Each stage has its own state (Nitrous Stage X State logging channel):

* **__Inactive**__ - The stage is inactive (activation conditions not met).
* **__Active delay**__ - The stage is active and counting down before solenoid activation. The delay time is defined in the stage parameters.
* **Active timer** - The stage is active, the solenoid output is engaged, and the following parameters are applied:  **__Timer__** (__Nitrous stage X time__), **__Ignition timing correction**__ (__Nitrous Ign. Mod.__),  ** __ Additional fuel injection__** (__Nitrous fuel adder__)
* **Active LC** - The stage is active during Launch contro,, the solenoid output is engaged, and the following parameters are applied:  **__Timer__** (__Nitrous stage X time__), **__Ignition timing correction**__ (__Nitrous Ign. Mod.__),  ** __ Additional fuel injection__** (__Nitrous fuel adder__)
* **Finished**  - The nitrous procedure has ended (time elapsed) or has been interrupted (e.g., throttle pedal released). To return to the **__Inactive state**__, the stage activation conditions must be met again.
* **Post active** - If ignition or fuel corrections remain active after the solenoid is turned off (__**Fuel Off Delay > 0**__ or Ign. __**Corr. Off Delay**__ > 0), the strategy transitions into the **Post active** state. Once the correction hold time expires, the strategy transitions to the **Finished** state.


**Below is a wiring diagram for a Dry and Wet system using a Solid-State Relay (SSR).
__The solid-state relay can be replaced with a standard mechanical relay.

![Nitrous/nitrousWiringDiagram.png](Images/Nitrous/nitrousWiringDiagram.png)

**Below is a wiring diagram for a Dry and Wet progressive system using a Solid-State Relay (SSR).

!!⚠**__The solid-state relay cannot be replaced with a standard mechanical relay.

![Nitrous/nitrousWiringDiagramPWM.png](Images/Nitrous/nitrousWiringDiagramPWM.png)


**Logging channels:

* __ **Nitrous active**__  -  shows if any of nitrous  stage is active
* __ **Nitrous stage state**__  -  shows current statet of the stage.
* __ **Nitrous ign. mod.**__  -  shows current ignition correction from all active nitrous stages..
* __ **Nitrous fuel adder **__  -  shows current fuel correction added / substracted to the primary injectors PW.
* __ **Nitrous stage time **__  -  shows current stage time when active
* __ **Nitrous stage DC **__  -  shows stage current output DC (for progressive systems)
* __ **Nitrous stage output **__  -  shows stage output state. Can be used for controlling PMU outputs.


.







---

[Auto](help://Nitrous/Nitrous) 
##Parameters

This configuration defines the global settings for the __**Nitrous system**__ activation, protection against low nitrous pressure, and the __**NFR**__ (Nitrous to Fuel Ratio) for __**DRY**__ systems.

{#1}


---

[Auto](help://Nitrous/Nitrous) 
##Fuel add.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Ignition mod.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Fuel scale

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Torque Correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Stage 1

Stage configuration


---

[Auto](help://Nitrous/Nitrous) [Auto](help://Nitrous/Stage1) 
##Parameters

{#1}














---

[Auto](help://Nitrous/Nitrous) [Auto](help://Nitrous/Stage1) 
##Launch control

For Stage 1, additional activation during the {1} procedure is possible to spool the turbocharger. After the launch procedure is completed, Stage 1 can be activated and used in the standard way.


{#1}


---

[Auto](help://Nitrous/Nitrous) 
##Nitrous S1 fuel

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Nitrous S1 ignition

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Nitrous S1 DC

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Stage 1 fuel

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Stage 1 ignition

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) 
##Stage 1 DC

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Nitrous/Nitrous) [Auto](help://Nitrous/Stage1) 
##Stage 1 fuel

In the case of the **DRY** or **DRY progressive** nitrous system, the ECU calculates the required additional fuel dose based on the defined horsepower (**HP**) increase from the injected nitrous oxide and the expected **Nitrous to Fuel Ratio (NFR)**. In this case, the **Stage fuel** table defines the correction for the calculated additional fuel dose.

For the **WET** or **WET Progressive** system, the **Stage fuel **table defines the additional fuel flow (or fuel flow reduction) expressed in **g/min**. For reference, **100 lb/h** equals **755.99 g/min**.

In progressive systems (**PWM**), the **X-axis **represents the current solenoid duty cycle (**DC**). In **On/Off** systems, the** X-axis** represents engine **RPM.**


**Calculated fuel dose takes into consideration fuel pressure and fuel ethanol content**

**!!⚠IMPORTANT: Additional fuel can be provided only by primary injectors.Additional fuel can be provided only by primary injectors.





---

[Auto](help://Nitrous/Nitrous) [Auto](help://Nitrous/Stage1) 
##Stage 1 ignition

The **Stage Iignition** table defines the ignition timing correction during the __**Nitrous strategy**__ operation. Both negative values (for ignition retard) and positive values (for ignition advance) are allowed. Advancing ignition can be beneficial when using the Nitro strategy for Methanol injection.

In progressive systems (**PWM**), the **X-axis **represents the current solenoid duty cycle (**DC**). In **On/Off** systems, the** X-axis** represents engine **RPM.**



---

[Auto](help://Nitrous/Nitrous) [Auto](help://Nitrous/Stage1) 
##Stage 1 DC

In the case of a **PWM-controlled** solenoid system (**Dry progressive** and **Wet progressive**), the **Stage DC** table defines the solenoid duty cycle (**DC**) as a function of the nitrous strategy runtime.

The table defines the !!**effective duty cycle**!!, which depends on the __**Solenoid min DC**__ and __**Solenoid max DC**__ defined in {1}.  **0%** represents the **__Solenoid Min DC**__, while **100%** represents the **__Solenoid Max DC**__.


---

