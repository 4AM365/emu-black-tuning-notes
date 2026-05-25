##Outputs

Outputs groups all strategies for controlling the device outputs, such as the main relay or the fuel pump.

---

[Auto](help://Outputs/Outputs) 
##PWM outputs

The EMU BLACK device has 2 dedicated PWM outputs that can be used for control via PWM tables. Additionally, the **__Alternator control**__ and **__Differential control**__ strategies utilize PWM outputs.

{#1}


---

[Auto](help://Outputs/Outputs) 
##AC clutch

The AC clutch strategy allows for the management of the clutch that engages the air conditioning compressor.

**Logging channels:

* __  **AC clutch** __ - Indicates whether the AC compressor clutch is engaged. 


{#1}


---

[Auto](help://Outputs/Outputs) 
##CLT Freq. output

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Coolant fan

**Logging channels:

* __  **Coolant fan** __ - Indicates whether the coolant fan is engaged. 
* __  **Coolant fan DC** __ - In the case of a radiator fan controlled by a PWM signal, this channel indicates the current duty cycle (DC) of the control signal.


{#1}



---

[Auto](help://Outputs/Outputs) 
##Fuel pump

The fuel pump strategy is used to control the fuel pump relay. Upon turning on the ignition, it activates the fuel pump for a specified time to build pressure in the fuel system, and then re-engages the pump when engine RPM is detected. When the engine stops, the fuel pump will automatically turn off.

**BMW EKP Fuel Pump Control

The **Fuel Pump strategy** also supports BMW fuel pumps controlled via the EKP module (e.g. M2, M3).  
To enable this mode, set the **Control type** option to **BMW E9x EKP**.  

The fuel pump duty cycle is defined in the **EKP Pump DC table**.  
As a rule of thumb, the higher the engine airflow, the higher the duty cycle should be.  

When this control type is selected, the EMU will transmit a CAN frame to control the EKP module.  
For this reason, the EKP module must be connected to the EMU CAN bus.  

EKP control is also supported when the **BMW E90 CAN stream** is selected in the CAN configuration.



---

[Auto](help://Outputs/Outputs) 
##Honda CLT Dash

This strategy enables sending a digital signal to control the coolant temperature gauge on the dashboard of a Honda S2000.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Main relay

This function enables the main relay to be activated when the EMU device is powered on.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Speedometer output

This function enables generating a square wave signal to control the speedometer gauge on the dashboard. The frequency of the generated signal is proportional to the vehicle's speed.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Tacho output

This function enables generating a square wave signal to control the tachometer gauge on the dashboard. The frequency of the generated signal is proportional to the engine's RPM.
In the case of a low-voltage signal (when the original tachometer was controlled by the ECU), a pull-up resistor is usually required for the Low Side output (**__Injectors**__, **__Aux**__). In this case, **__Aux 4**__ output, which has a built-in pull-up to +12V, or the **__H-Bridge**__ output should be selected.

The frequency of the output signal can be modified using the **__RPM multipliers__** parameters. If no switch is assigned to the **__Multiplier switch__** parameter, or the assigned switch is not active, the **__RPM multiplier 1__** parameter is always used. If the selected switch is active, the value of the **__RPM multiplier 2__** parameter is applied.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Alternator

Some alternators require control via a PWM signal, which allows us to regulate the battery charging voltage.

This control is performed in a feedback loop using a PID controller.

To use the battery charging control strategy, you need to assign the Alternator Control function in the  {1}  configuration. to PWM 1 or 2 output.

**Logging channels:

* __  **Battery voltage target** __ - the target voltage for the __**Alternator control__** strategy to aim for
* __  **Battery voltage** __ - the current voltage in the electrical system
* __  **PWM 1 or PWM 2 DC** __ - the duty cycle of the alternator control signal depending on which PWM output the __**Alternator control__** strategy has been assigned to.



.

 


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Alternator) 
##Parameters

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Alternator) 
##Batt. voltage trgt

The table defines the desired voltage in the vehicle's electrical system as a function of load and RPM.



---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Alternator) 
##Alternator

The help content will cover essential details about channels in this particular group.
{#1}


---

[Auto](help://Outputs/Outputs) 
##Oil metering pump

Each group contains specific information related to its respective area


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Oilmeteringpump) 
##OMP Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Oilmeteringpump) 
##Position target

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Outputs/Outputs) 
##PWM

In cases where {1} have the PWM table function assigned, the PWM section allows controlling the duty cycle of the output signal

** The signal frequency and device output must be defined in the {2}t options.


**Logging channels:

* __  **PWM 1 DC** __ - duty cycle of PWM 1 output
* __  **PWM 2 DC** __ - duty cycle of PWM 2 output



---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/PWM) 
##PWM 1 Parameters

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/PWM) 
##CLT Freq output

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/PWM) 
##PWM 1 table

A table defining the duty cycle of the output signal.



---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/PWM) 
##PWM

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/PWM) 
##PWM #1 table

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Outputs/Outputs) 
##Frequency output

The **__Frequency output**__ strategy allows generating frequencies in the range of 1 to 120 Hz, defined in the Frequency table. This function enables, for example, the generation of a control signal for the coolant gauge in some dashboards.

** The signal frequency and device output must be defined in the {1}t options.

**Logging channels:

* __  **Frequency output** __ - current output signal frequency




---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Frequencyoutput) 
##Freq. output

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Frequencyoutput) 
##Freqency tbl.

A table defining the desired output frequency.


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Frequencyoutput) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) 
##Electric water pump

The EWP strategy is used to control the electric water pump.


**Logging channels:

* __  **EWP active** __ - indicates if the EWP is active 

---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Electricwaterpump) 
##Parameters

The control strategy for the electric water pump enables its cyclic operation when the engine is cold (allowing it to warm up faster) and smooth flow regulation within the operating temperature range. The water pump should be connected using a solid-state relay controlled by the EMU output.

The EMU output, **__PWM signal frequency__**, and the **__PWM function**__ (Electric water pump) should be defined in the {1}  section for the **__PWM1**__ or **__PWM2**__  function.

The diagram below illustrates the wiring of an electric pump using a solid-state relay.

![ewpWiringDiagram.png](Images/ewpWiringDiagram.png)

The diagram below illustrates the operating principle of the strategy. For temperatures below **__Set point 1**__ and **__Set point 2**__, the pump operates cyclically. Above the temperature of **__Set point 2**__, the pump operates continuously with the duty cycle value of the control signal defined in the {2}.

![ewpStrategy.png](Images/ewpStrategy.png)

 

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Electricwaterpump) 
##EWP DC table

When the coolant temperature exceeds the value defined by the **__Set point 2**__ parameter ({1}), the duty cycle of the control signal for the pump is defined in this table.


---

[Auto](help://Outputs/Outputs) 
##Power steering

Handling power steering pumps controlled via the CAN bus.









---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Powersteering) 
##Parameters

{#1}



---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Powersteering) 
##Power

Power steering assistance level from 0 to 100%, where 0% represents the minimum assistance force, and 100% represents the maximum assistance force.










---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Frequencyoutput) 
##Param block

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Frequencyoutput) 
##EKP pump DC

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Fuelpump) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Outputs/Outputs) [Auto](help://Outputs/Fuelpump) 
##EKP pump DC

The **EKP Pump DC** table defines the fuel pump duty cycle as a function of **Airflow**.  
As airflow increases, the engine fuel demand also rises, which requires a higher duty cycle.

---

