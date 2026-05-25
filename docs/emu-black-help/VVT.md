##VVT

The EMU device allows for variable valve timing (VVT) control for two camshafts, with position sensors connected to the **__CAM1**__ and/or **__CAM2**__ inputs. There is also support for **__BMW DUAL VANOS**__ variable valve timing, using built-in **__H-Bridges**__, an external module that converts low side outputs (**__AXU**__, **__INJ**__) to high side outputs, or by changing the solenoid wiring and removing the protective diodes, allowing solenoid control via low side signals.

!!⚠In engines with two camshafts with variable timing, do not connect both solenoids to a single **__H-Bridge**__. In this situation, use low side outputs (**__INJ**__, **__AUX**__) or connect one solenoid to **__H-Bridge 1**__ and the other to **__H-Bridge 2**__. Connecting both solenoids to the same **__H-Bridge**__ will cause interference. Note that **__INJ**__ and **__AUX1/AUX2**__ outputs do not have built-in flyback diodes. If these outputs are to be used for variable valve timing control, external flyback diodes must be used.

The diagrams below show example connections of **__VVTI**__ solenoids to **__AUX5**__ and **__AUX6**__ outputs.

![VVT/twoCams_Aux5_Aux6.png](Images/VVT/twoCams_Aux5_Aux6.png)

The diagrams below show example connections of **__VVTI**__ solenoids to **__INJ5**__ and **__INJ6**__ outputs with external flyback diodes.

![VVT/twoCams_Inj5_inj6_flyback.png](Images/VVT/twoCams_Inj5_inj6_flyback.png)

The diagram below shows an example connection of a **__Dual vanos**__ solenoids to **__H-Bridge 2**__ output.

![VVT/dualVanos_hbridge.png](Images/VVT/dualVanos_hbridge.png)


In the VVT options, there is also a strategy available for controlling {1}  variable valve lift (on/off).
The diagram below shows an example connection of a VTEC control solenoid (high side).

![VVT/vtect_hbridge2_a.png](Images/VVT/vtect_hbridge2_a.png)

--
**Configuration 

The first step in configuring variable valve timing is to correctly configure the patterns for the **__CAM1**__ and **__CAM2**__ camshafts. More information on this can be found in the {2} of the help documentation.

After starting the engine, you can read the camshaft offsets for camshaft 1 and 2 using the scope, as shown in the diagram below.

![VVT/scope_with_cams_offset.png](Images/VVT/scope_with_cams_offset.png)

These values should match the values of the **__VVT CAM 1**__ and **__CAM 2 angle**__ log channels. Enter these values in the {3} options for the corresponding camshaft in the **__CAM offset**__ field. This should zero out the **__VVT CAM 1**__ and **__CAM 2 angle**__ log values.

!!Ensure that the solenoids are not controlled (powered) at this stage of the configuration.

The next step is to configure the **__Steady pos DC**__ parameters and determine how changing the DC affects the camshaft angle. To do this, select the **__Override DC**__ option in the {4} of the corresponding camshaft and, by changing this value, find the DC value at which the camshaft changes direction (observed on the **__VVT CAM 1**__ or **__VVT CAM 2 angle**__ channel). This value will be our **__Steady pos DC**__ value.

Additionally, if increasing the DC increases the camshaft angle, select "**__increase CAM angle**__" in the **__Higher DC**__ field; otherwise, select "**__decrease CAM angle**__".
It is also recommended to check at this stage whether the indicated angle is correct for the full range of camshaft angles and that there are no ignition problems, which could indicate incorrect trigger configuration for the camshaft position sensor.

!!**WARNING:** Changing the camshaft position affects engine operation, which can cause the engine to stall, especially at low RPMs. Therefore, during camshaft configuration, maintain sufficiently high RPMs.

The **__VVT CAM 1**__ and **__CAM 2 status**__ log channels show the current state of the control strategy and can be very useful during configuration.

If the above configuration was successful, set the {5} controller parameters, which will allow the strategy to maintain the desired camshaft position (CAM angle tables).
Most VVT systems rely mainly on the proportional component. During PID configuration, maintain RPMs above 2000 to ensure proper oil pressure used by the VVT actuators.

**Logging channels:

* __ **VVT CAM 1 / 2 angle**__  - current angle of the respective camshaft relative to the crankshaft
* __ **VVT CAM 1 / 2 angle target **__ - desired angle of the respective camshaft relative to the crankshaft 
* __ **VVT CAM 1 / 2 status**__ - status of the camshaft position control strategy 
* __ **VVT CAM 1 / 2 solenoid DC**__ - current DC signal of the camshaft solenoid
* __ **VVT CAM 1 / 2 table index**__ - current CAM angle table for the respective camshaft
* __ **VTEC active**__ - VTEC solenoid control output is active


**Meaning of VVT CAM statuses:

* __ **Disabled**__ - the camshaft position control strategy is not enabled.
* __ **Inactive - start delay**__ - the strategy is inactive because the start delay time defined by the Start delay parameter has not elapsed.
* __ **Inactive - below RPM**__ - the strategy is inactive because the engine RPM is below the defined threshold.
* __ **Inactive - below CLT**__ - the strategy is inactive because the engine coolant temperature is below the defined threshold.
* __ **Active - DC override**__ - the strategy is active, and the input DC signal is defined by the DC override parameter.
* __ **Active**__ - the strategy is active, and the PID controller is attempting to maintain the target camshaft position by adjusting the DC signal.


---

[Auto](help://VVT/VVT) 
##VTEC Control

The **__VTEC control**__ strategy allows for the definition of two sets of parameters, upon the fulfillment of which the VTEC valve control output will be active. The output is active when all conditions in one of the parameter sets are met.

When the VTEC solenoid is activated, it is possible to switch VE/Ignition tables using the {1} strategy.

{#1}


---

[Auto](help://VVT/VVT) 
##CAM 1

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM1) 
##Parameters

{#1}


---

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM1) 
##PID

The PID controller modifies the __**Steady pos DC__** value to achieve the desired camshaft position angle.

{#1}


---

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM1) 
##CAM1 angle 1

A table defining the desired camshaft position angle.


---

[Auto](help://VVT/VVT) 
##VVT

**Logging channels:

{#1}

**Meaning of VVT CAM statuses:

* __ **Disabled**__ - the camshaft position control strategy is not enabled.
* __ **Inactive - start delay**__ - the strategy is inactive because the start delay time defined by the Start delay parameter has not elapsed.
* __ **Inactive - below RPM**__ - the strategy is inactive because the engine RPM is below the defined threshold.
* __ **Inactive - below CLT**__ - the strategy is inactive because the engine coolant temperature is below the defined threshold.
* __ **Active - DC override**__ - the strategy is active, and the input DC signal is defined by the DC override parameter.
* __ **Active**__ - the strategy is active, and the PID controller is attempting to maintain the target camshaft position by adjusting the DC signal.


---

[Auto](help://VVT/VVT) 
##CAM #1

Each group contains specific information related to its respective area


---

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM_1) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM_1) 
##PID

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://VVT/VVT) [Auto](help://VVT/CAM_1) 
##CAM1 angle #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

