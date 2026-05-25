##Overrun

__Overrun__ is a state in which we release the accelerator pedal and begin decelerating the engine using engine braking. In this state, there is no need for fuel injection.

It is possible to create two separate configurations for the overrun strategy (e.g., one gentle and one aggressive with pops and bangs) that can be switched by the user. This is achieved using tables with **__index #1**__ and **__#2**__. The method for switching between overrun settings is defined in the {1} options .

The Overrun strategy has the following states (the current state is represented in the __Overrun status__ log channel):

**Disabled** - The strategy is not enabled in the software.

**Inactive - Conditions not met** - The strategy is enabled, but it is inactive because the Overrun conditions (Pedal position and RPM) are not met.

**Enter ignition ramp** - In this state, the conditions for the overrun strategy are met, and there is a change in the ignition angle to the value defined in the {2}  table. If the {3}  option is selected, the throttle target is taken from the **__DBW override**__ table. Fuel injection is determined based on the VE tables.

**Active** - In this state, the ignition angle is read from the {4}  table, fuel injection correction is made based on the  {5} table, and if the **__Override DBW**__ option is selected, the throttle target is taken from the {6} table. In the {7} table, -100% means complete injector shutoff (Fuel cut), 0% means no fuel correction, and 100% means double the fuel dose.

**Exit ignition ramp** - A state of exiting the overrun strategy in which the ignition angle is changed from the value in the {8}  to a value calculated from current maps. Fuel injection correction is turned off, and fuel mixture enrichment is activated based on the parameters Exit fuel enrichment and Exit fuel enrichment decay rate.

**Logging channels:

* __   **Overrun status** __ - the state of the overrun strategy. 
* __   **Overrun fuel corr.** __ - the current fuel correction applied by the overrun strategy (0% - no correction).
* __   **Overrun tables index** __ - the currently selected overrun strategy configuration. 


**Meaning of Overrun statuses:

* __**Disabled**__- the overrun strategy is not activated in the software
* __**Inactive - conditions not met**__-  the strategy is not active because the activation conditions are not met
* __**Enter ignition ramp**__- overrun is in the ignition ramp state, advancing/retarding to the specified ignition timing defined in the overrun ignition table. In this state, the fuel correction is not applied.
* __**Active**__- the strategy is active, the ignition timing is defined in the overrun ignition table, and the fuel correction is taken from the overrun fuel corr. table
* __**Exit ignition ramp**__- the strategy has been interrupted, and the ignition timing and fuel delivery are being restored.
* __**Blocked by Idle**__- the Idle strategy interrupts the operation of the overrun strategy.
* __**Blocked by ALS**__- the ALS strategy interrupts the operation of the overrun strategy.
* __**Blocked by Blip**__- the Blip strategy interrupts the operation of the overrun strategy.
* __**Blocked by CC**__ - the Cruise Control strategy interrupts the operation of the overrun strategy.
* __**Blocked by rev match. **__ - the Rev matching strategy interrupts the operation of the overrun strategy.
* __**Blocked by DBW CAN control**__ - the Rev matching strategy interrupts the operation of the overrun strategy.


---

[Auto](help://Overrun/Overrun) 
##Parameters

{#1}


---

[Auto](help://Overrun/Overrun) 
##Ignition angle 1

This table defines the ignition timing during the overrun function. Significant ignition retard enables achieving the pops and bangs effect.

---

[Auto](help://Overrun/Overrun) 
##Fuel corr. 1

This table defines the fuel adjustment during the overrun strategy (in the Active state). 0% means no correction, -100% means complete fuel cut-off, and 100% means doubling the fuel amount.


---

[Auto](help://Overrun/Overrun) 
##Spark cut 1

This table defines the percentage of ignition events cut during the overrun strategy.

---

[Auto](help://Overrun/Overrun) 
##DBW override 1

In the case where the Override DBW option is selected in the parameters, during the operation of the overrun strategy, the DBW (drive-by-wire) position will be taken from this table.


---

[Auto](help://Overrun/Overrun) 
##Ignition angle #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Overrun/Overrun) 
##Fuel corr. #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Overrun/Overrun) 
##Spark cut #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Overrun/Overrun) 
##DBW override #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

