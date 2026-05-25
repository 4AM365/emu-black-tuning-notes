##Fueling

!!**⚠Before starting tuning, it is essential to correctly set the following parameters:

* **Engine displacement** ({1})
* **Injector size** ({2})
* **Fuel pressure regulator type** and **base fuel pressure** ({3})
* **Fuel composition** (Flex Fuel sensor or fixed fuel ethanol content) ({4})
* **Injector dead time calibration**. {5}
* **IAT and CLT** sensors {6}
* **Lambda target** {7}


The EMU fuel model uses engine volumetric efficiency (**VE**) and the **Speed density** algorithm.

* **Volumetric Efficiency (VE)** - volumetric efficiency is a measure of the effectiveness with which the engine fills its cylinders with air during the intake process. It is expressed as a percentage, representing the actual volume of air inducted into the cylinders versus the theoretical maximum volume.


* **Speed Density Algorithm** - the speed density algorithm calculates the air mass entering the engine based on intake manifold pressure, intake air temperature, and engine speed. This method allows for accurate fuel delivery calculations without relying on a mass air flow sensor, making it particularly suitable for performance and forced induction applications.


In the case of an engine where the **speed density** algorithm cannot be applied (e.g., naturally aspirated engines where the camshaft profile causes issues with vacuum readings), the **Alpha-N** algorithm can be used instead.

* **Alpha-N** - the Alpha-N algorithm is a fuel calculation method used primarily in engines where intake manifold pressure (**MAP**) readings are unreliable, such as those with aggressive camshafts that cause fluctuating vacuum levels. Instead of using **MAP*, the **Alpha-N** method relies on throttle position (**Alpha*) and engine **RPM** (**N**) to determine the amount of fuel to inject. This approach is particularly suited for naturally aspirated, high-performance engines, where stable **MAP** readings are challenging to obtain.


Based on the calculated amount of air (using **VE, IAT**, and **MAP** values), the desired **Lambda target** value, the **ethanol content** in the fuel (either a fixed value or a value read from the Flex Fuel sensor), the **injectors size**, **engine displacement** and the type and pressure of the **fuel regulator**, and other corrections, the device calculates the required injector opening time (in ms)

The engine tuning process involves building a  {8} tableso that the actual **Lambda** value matches the {9} value.

!!**⚠An incorrect lambda value of the fuel-air mixture can lead to engine damage!

**Logging channels:

* __   **Lambda 1, 2**__ - current Lambda value of the fuel-air mixture.
* __   **Lambda target**__ - expected Lambda value with all corrections applied.
* __   **Lambda target from table**__ - expected Lambda value read from the Lambda target table.
* __   **Lambda error mult**__ - The theoretical value by which the **VE** value should be adjusted to achieve the desired **__Lambda target__**. It should be emphasized that this value is only accurate when the engine is operating steadily, i.e., there is no spark or fuel cut and no transient conditions are present.
* __   **Injectors PW**__ - current injector pulse width (opening time).
* __   **Injectors cal. time**__ - current injector dead time added to the Injectors PW value.
* __   **Injectors DC**__ - injector duty cycle, which should not exceed 90%.
* __   **Injection angle**__ - current injection angle.
* __   **VE**__ - volumetric efficiency value of the engine read from the VE table.
* __   **Charge temp**__ - intake air temperature calculated from IAT and CLT values using the Charge temp table.
* __   **FF Blend VE**__ - when the option for VE table blending based on ethanol content is selected, this value indicates the current interpolation percentage between VE tables 1 and 2. 100% means only the value from VE table 1.
* __   **Fuel pressure**__ - current fuel pressure from the fuel pressure sensor.
* __   **Effective fuel pressure**__ - effective fuel pressure depending on the type of pressure regulator, fuel pressure, barometric pressure, and manifold pressure.
* __   **Fuel pressure error**__ - difference between the expected fuel pressure and the actual effective fuel pressure.
* __   **Fuel cut**__ - indicates injector shutdown (e.g., in case of excessive RPM).
* __   **Fuel cut percent**__ - for strategies that reduce torque by cutting fuel injectors, this parameter indicates the percentage of fuel cut.
* __   **Secondary inj. PW**__ - current pulse width of secondary injectors.
* __   **Secondary inj. DC**__ - duty cycle of secondary injectors, which should not exceed 90%.
* __   **Secondary inj. split**__ - defines the percentage split of the fuel dose between the primary and secondary injectors. **0%** means that all the fuel should be delivered by the primary injectors, while **100%** means that the entire fuel dose should be delivered by the secondary injectors.  If the activation conditions for the secondary injectors (**RPM, TPS, MAP**) are not met, the inj. split value is **0%**.
* __   **Fuel used**__ - fuel consumed since engine start.
* __   **Fuel usage**__ - current fuel consumption.
* __   **Short term trim**__ - current short-term fuel trim adjustment based on Lambda sensor readings.
* __   **Acc. enrichment %**__ - percentage correction of the fuel mixture; positive values indicate enrichment, negative values indicate leaning. 
* __   **Acc. enrich. async PW**__ - asynchronous enrichment pulse width.
* __   **Warmup enrichment**__ - enrichment during the engine warm-up phase.
* __   **Afterstart enrichment**__ - mixture enrichment after engine start defined in the  {10} table.
* __   **Fuel pressure correction**__ - current fuel dose correction due to the difference between effective fuel pressure and expected fuel pressure.
* __   **Fuel temp correction**__ - fuel dose correction based on current fuel temperature.
* __   **IAT user correction**__ - fuel dose correction based on user adjustment.
* __   **BARO correction**__ - fuel dose correction based on barometric correction.
* __   **Cranking correction**__ - fuel dose correction during cranking.
* __   **ALS fuel correction**__ - fuel dose correction introduced by the ALS strategy.
* __   **LC fuel enrichment**__ - fuel dose correction introduced by the LC strategy.
* __   **Timer fuel corr.**__ - fuel dose correction introduced by timer strategies.
* __   **Fuel custom correction 1, 2, 3**__ - custom fuel correction values.


---

[Auto](help://Fueling/Fueling) 
##General

**Fuel Pressure Regulator

Depending on the fuel pressure regulator used and the presence of a fuel pressure sensor, the appropriate type of regulator should be selected. The use of a fuel pressure sensor allows for active correction of the fuel dose when the measured fuel pressure differs from the theoretically calculated value. In the absence of a sensor or if the sensor returns a status other than OK, the fuel dose correction is not active.


**Log Channels connected to the fueling type

* **__Effective fuel pressure**__ - in the absence of a pressure sensor or if it is malfunctioning, this value is calculated based on the base pressure and the MAP pressure. <br>
* **__Fuel pressure error**__ - When using a fuel pressure sensor, this represents the difference between the actual fuel pressure and the calculated value. Negative values indicate that the actual pressure is lower than expected.


* **__Fuel pressure correction__** - the current fuel dose correction resulting from the type of fuel rail and the effective fuel pressure.



{#1}


---

[Auto](help://Fueling/Fueling) 
##Fuel cut

The **Fuel Cut** setting in the fueling configuration specifies the engine **RPM** (over-rev) or intake manifold pressure limit above which the injectors will be turned off, which can help prevent engine damage.

For precise control of maximum engine **RPM** (Rev Limiter), it is recommended to use the {1}  strategy. 

**The maximum RPM value for Fuel Cut should be set lower than the value specified in the Rev Limiter strategy.**

{#1}


---

[Auto](help://Fueling/Fueling) 
##Lambda guard

The **__Lambda guard**__ strategy is used to protect the engine if the &#x3bb; value remains above the __Lambda target__ for a specified period. In such cases, it allows for additional adjustments to be applied, such as correction of the ignition timing, fuel dose, or reduction of boost pressure.
The strategy is deactivated whenever the spark or fuel is cut.

**Logging channels:

* __   **Lambda guard status__** - status of the strategy.
* __   **F. Lambda guard**__   - lambda guard fuel correction active.
* __   **I. Lambda guard**__ - lambda guard ignition  correction active.
* __   **Boost lambda guard corr.**__ - lambda guard boost target correction active


**Meaning of Lambda guard statuses:	

* __   **Disabled**__ - the strategy is disabled.
* __   **Active**__ - the strategy is active due to a lean condition.
* __   **Lean cond. waiting**__ - the lambda guard strategy is pending activation. Waiting for __Max limit time__ to elapse.
* __   **RPM not in range**__ - engine RPM is outside the defined range.
* __   **MAP not in range**__  - MAP sensor value  is outside the defined range.
* __   **TPS not in range**__ - TPS sensor value  is outside the defined range.
* __   **WBO sensor not valid**__ - Wideband oxygen sensor value is not valid (eg. sensor warmup, sensor error).
* __   **CLT too low**__ - CLT sensor value  is below defined value.
* __   **Transient fuel**__ - transient condition like gearshift, acceleration enrichemnt, fuel or ignition cut, etc.



{#1}



---

[Auto](help://Fueling/Fueling) 
##Acceleration

Acceleration enrichment refers to the process of temporarily increasing the amount of fuel delivered to an engine when there is a rapid increase in throttle position. This is necessary to ensure smooth acceleration and to prevent hesitation or stalling when the driver demands more power.

Deceleration enrichment is a opposite process that temporarily adjust the fuel mixture when the throttle is rapidly closed.

The implemented strategy allows for enriching and leaning the fuel mixture depending on the rate of change of the throttle position ({1}). The greater the change in throttle position, the stronger the enrichment or leaning of the mixture needed. There are two available enrichment methods: **__synchronous**__, which proportionally increases the injection time that decreases with each engine cycle, and **__asynchronous**__, which allows for an additional fuel injection  during a sudden change in throttle position, especially at low engine speeds. These two enrichment methods complement each other, enabling a quick engine response to throttle input. 

It is also important to select the smallest possible {2} in the TPS configuration to minimize the delay in response to the accelerator pedal input.

To achieve the best engine response to pressing the accelerator pedal, the injection timing must be correctly set.

**Logging channels:

* __   **TPS rate  ** __  - change in the throttle position in %/s
* __   **MAP rate  ** __ -  change in intake manifold pressure in kPa/s. Used when acceleration enrichment is based on the MAP sensor instead of the TPS
* __   **Acc.  enrichment %  ** __ - percentage correction of the fuel mixture. Positive values indicate enrichment, while negative values indicate leaning.
* __   **Acc.  enrich. async PW  ** __ - asynchronous enrichment pulse widh 
* __   **Acc. enrichment correction**__ - total value of acceleration enrichment corrections from the {3} and {4}








 









---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Acc. enrichment

The **__Acc. enrichment**__ table defines the amount of enrichment (positive values) or leaning (negative values) of the mixture to be applied based on the TPS rate and engine RPM. The higher the TPS rate, the greater the enrichment of the fuel mixture.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Acc. CLT Factor

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) 
##Corrections

Corrections allow for adjusting the fuel dose depending on the values of various engine operating parameters. It is worth noting that for each correction, it is possible to change both the percentage of the fuel dose and to adjust the **__Lambda target__**. When using the {1} film function, the lambda target should be modified, as a direct fuel dose correction will be compensated by the **__Short fuel trim__**. 
Currently active corrections can be read from the log.

**Log Channels:

* **__BARO correction**__ - value of barometric correction. 0% means no correction.
* **__Ethanol correction**__ - value of ethanol conent based correction. 0% means no correction.
* **__IAT user correction**__ - value of user IAT correction. 0% means no correction.
* **__Fuel temperature correction**__ - value of fuel temperature based correction. 0% means no correction.
* **__Fuel custom correction 1, 2, 3**__ - value of custom correction 1,2 and 3


* **__F.EGT correction**__ -  EGT fuel dose correction active.
* **__F.IAT user correction**__ - user IAT based correction active. 
* **__F.BARO user correction**__ - barometric correction active.
* **__F.Custom correction 1,2,3**__ - custom correction 1,2 and 3 active.
* **__F.Fuel temp. correction__** - fuel temperature based correction active.
* **__F.FPR correction__** - fuel pressure correction active.

 

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##General

General options allow configuring fuel corrections. Here, it is possible to define the axes for the **__Custom corr. 1, 2, and 3__** tables, as well as specify which corrections modify the fuel dose or the **__Lambda target__**.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##EGT correction

This function allows for fuel dose correction per cylinder based on the EGT temperature for each cylinder. It is essential to correctly assign the EGT sensors to the respective cylinders.

The injection time correction value is defined in the {1} table.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Barometric corr.

The __**Barometric correction table**__ adjusts the fuel dose based on changes in barometric pressure, ensuring stable engine performance across varying altitudes and atmospheric conditions. Since barometric pressure affects air density, this table helps maintain optimal air-fuel ratios regardless of environmental changes.

!!**⚠Ensure the barometric (BARO) sensor is properly configured and calibrated to provide accurate pressure readings to the system.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##IAT correction

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##DFPR corr.

Read-only table, automatically generated based on the configuration of the fuel rail and the base fuel pressure ({1}).
.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##EGT corr

A table defining fuel dose correction based on EGT probes.

These corrections need to be activated, and the EGT probes must be assigned to the cylinders in the {1} options.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Fuel temp. corr.

The **__Fuel temperature correction**__ table adjusts the fuel dose based on the fuel temperature. As fuel temperature changes, its density and combustion characteristics also vary, potentially impacting engine performance. This table allows you to apply corrections to ensure optimal fuel delivery across a range of fuel temperatures.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Charge temp.

Charge defines the contents of the cylinder after all valves have closed, consisting of the fresh mixture and residual gases. The simplest way to estimate air density is by using IAT. However, this approach doesn't account for the effect of air heating from the intake manifold and engine components. At lower air flows, air heating becomes more significant. To address this phenomenon, the **__Charge temperature estimation**__ table was introduced. This table defines the influence of **__IAT__** and **__CLT__** on charge temperature. A value of 0% means the charge temperature is equal to the IAT sensor reading, while 100% means the charge temperature is equal to the CLT sensor reading.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Custom corr. 1

The Custom correction tables allow for flexible adjustments to either the fuel dose or the **__Lambda target**__, depending on specific engine operating conditions. This table is highly customizable and can be tailored to meet unique tuning requirements ({1}).

---

[Auto](help://Fueling/Fueling) 
##Short term trim

Short Term Trim (STT) is an adaptive correction mechanism used to adjust fuel delivery based on real-time feedback from the engine. 
The strategy utilizes a PID controller that corrects the error between the desired Lambda target and the current readings of the probe. It also takes into account the fact that the readings of the WBO probe are delayed due to both the sensor's reaction time and the time it takes for exhaust gases to reach the probe from the cylinders.

Therefore, an **__Air flow__** channel has been introduced, which calculates the amount of air sucked in by the engine per second based on engine parameters.

The short term trim is deactivated during fuel cut overrun. However, for this to occur, the {1} strategy must be active.

**Logging channels:

* **__Estimated airflow__** -  estimated airflow through the engine in g/s.
* **__Short term trim__** -   fuel dose correction introduced by the Short term trim strategy.
* **__Lambda target from table__** -  target lambda to which the PID controller aims.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##Parameters

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##PID

The configuration of the PID controller is crucial for the correct operation of the short term trim strategy. Excessive values of the **kP** and **kI** coefficients will cause oscillations, while too small values will result in slow controller response. 
It is crucial to note that different **kP** and **kI** coefficients (smaller) are required for low engine loads compared to high exhaust gas flows. This can be compensated for by using {1} and {2} tables so that, under higher engine load, these values are increased to provide a faster controller response.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##Lambda delay

The Lambda delay table defines the delay between the change in lambda mixture value and the reading of this change by the lambda sensor. This change results from the sensor's reaction time, the distance of the lambda sensor from the cylinder head, as well as the amount of exhaust gases flowing. The greater the amount of gases, the faster the exhaust gases reach the sensor, and the shorter the delay in reading by the sensor.
In summary, the largest delay will be at low engine speeds, and the smallest at full engine load at high speeds.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##PID kP scale

Depending on the engine load (amount of exhaust gases), to achieve the fastest possible fuel dose correction, the PID table **kP** scale allows for correction of the **kP** coefficient of the PID controller. In practice, the smallest values of the **kP** and **kI** coefficients occur at low exhaust gas flow rates. For higher flow rates, larger values of the coefficients can be applied.

!!**⚠A value of 0% indicates no correction, 100% indicates twice the amount of kP, -50% indicates half of the kP, and so on.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##PID kI scale

Depending on the engine load (amount of exhaust gases), to achieve the fastest possible fuel dose correction, the PID table **kI** scale allows for correction of the kP coefficient of the PID controller. In practice, the smallest values of the **kP** and **kI** coefficients occur at low exhaust gas flow rates. For higher flow rates, larger values of the coefficients can be applied.

!!**⚠A value of 0% indicates no correction, 100% indicates twice the amount of kI, -50% indicates half of the kI, and so on.



---

[Auto](help://Fueling/Fueling) 
##Fuel tables

Fuel tables are a key component in determining the fuel dose. Engine tuning involves setting the desired **Lambda target** values for specific RPM and load conditions in the {1} table and building the engine's volumetric efficiency  {2} table.

**Volumetric efficiency** is a measure of how effectively an engine fills its cylinders with air (or air-fuel mixture) during the intake stroke compared to its maximum theoretical capacity. It is typically expressed as a percentage and plays a crucial role in determining the engine's performance and efficiency.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Fueltables) 
##VE table 1

The VE table is used to establish the engine's volumetric efficiency. After completing the {1} table, the next step in the tuning process is to adjust the **VE table** values so that the actual **Lambda** matches the **Lambda target**. It is essential to avoid overly lean mixtures under load, as this can lead to engine damage. The **VE table** can also be refined using the {2} tool, which analyzes log data to suggest modifications to the existing **VE** map.




---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Fueltables) 
##Lambda trgt. 1

The **Lambda target** table is used to define the desired Lambda value for different engine RPMs and loads. If all parameters are set correctly (injectors calibration, *VE table, etc.), changing the **Lambda target** value should adjust the fuel dose so that the actual **Lambda value** matches the **Lambda target**.

!!⚠The **Lambda target** is a component of the fuel model, and changes in this table directly affect the fuel dose, independently of the {1} strategy.


---

[Auto](help://Fueling/Fueling) 
##Flex fuel

A **__Flex Fuel__** sensor, also known as an ethanol content sensor or fuel composition sensor, is a device used in vehicles to detect the ethanol content in the fuel and fuel temperature. 

The operating frequency of the Flex Fuel sensor ranges from 50 to 150Hz, and any frequency outside of this range is interpreted by the ECU as a sensor error. In such a case, the ethanol content defaults to the value defined by the Flex fuel fail-safe ethanol content parameter.

The sensor also allows for reading the temperature of the flowing fuel (based on the PWM signal from the sensor, ranging from 1ms to 5ms). To enable the EMU to read the fuel temperature from the sensor, in the temperature sensor configuration ( {1} ), the parameter Fuel temperature sensor input must be set to Flex Fuel sensor.

The ethanol content is one of the parameters of the EMU's fuel model. In the {2} parameters, there is an option to select whether the ethanol content should be read from the Flex Fuel sensor or if the ECU should assume a constant value (the Fuel composition parameter).

The diagram below shows the sensor connection scheme for EMU BLACK.

![flexFuelSensor.png](Images/flexFuelSensor.png)

**Logging channels:

* __   **FF Sensor frequency** __ - the current frequency from the Flex Fuel sensor.
* __   **Ethanol content** __ - the current ethanol content in the fuel.
* __   **Fuel Temperature** __ - the current fuel temperature.
* __ **FF status**__ – current status of the Flex Fuel sensor
* __ **Fuel temperature correction**__ – current fuel dose correction based on fuel temperature
* __ **Ethanol correction**__ – current fuel dose correction based on ethanol content in the fuel
* __ **FF input state**__ – when using the FF input as a switch input, this channel shows the input state (0 – grounded, 1 – open circuit). 


**Meaning of FF status:

* __**Disabled__** – sensor support not activated in EMU
* __**OK**__ – sensor is active and working properly
* __**Sensor error**__ – the sensor is enabled but not functioning correctly and is reporting an error. This condition may be caused by fuel contamination, the presence of an alcohol type other than ethanol, or air bubbles.
* __**Connection error**__ – no signal is being received from the sensor. Please verify the wiring connections.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Flexfuel) 
##Parameters

{#1}


---

[Auto](help://Fueling/Fueling) 
##Injectors

Injector configuration is crucial for accurate fuel dose calculation ({1}) and for maintaining smooth engine operation ({2}).









---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Injectors wizard

The software includes predefined calibration characteristics for selected injectors. The wizard allows for easy selection of an injector and then generates corresponding values in the {1} table for the chosen injector model.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Injectors phase

The **Injector phase** configuration window assigns fuel injector outputs to physical cylinder. 
There are three methods of injector timing control:

* When injection angle control is set to **Start at ignition event**, injection begins **N** degrees before Top Dead Center (**TDC**) of the cylinder associated with the injector. **N** corresponds to the **Trigger angle** value from the {1} configuration.


* When injection angle control is set to **End of injection**, the injectors close at the angle specified in the {2} table. !!⚠__This option functions only when the engine operates in full sequential fuel injection mode (with camshaft synchronization).


* When injection angle control is set to **Start of injection**, the injectors open at the angle defined in the {3} table.!!⚠__This option functions only when the engine operates in full sequential fuel injection mode (with camshaft synchronization).


It is also possible to assign **AUX1** and **AUX2** as **injectors 7** and **8**. Note that these outputs lack a flyback circuit, which is necessary for proper injector control.

It is recommended to assign injectors according to the cylinder sequence, meaning the injector for cylinder #1 is assigned to output INJ 1, the injector for cylinder #2 to output INJ 2, and so on.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Injectors trim

The **Injectors trim** configuration is used to adjust the fuel dose for individual cylinders, making it useful for fine-tuning fuel delivery on a per-cylinder basis.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Injectors cal.

The **Injectors calibration** table is used to calibrate injector dead time as a function of **supply voltage** and **effective fuel pressure**. For every fuel injector, there is a delay between when current is applied and when fuel is actually injected; this is known as the latency or dead time. This delay increases at lower **supply voltages** and higher **effective fuel pressure** and can vary significantly between different injector models. 

For many popular injector models, the {1} can be used to configure dead time settings.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Second injectors cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Injectors) 
##Injection angle

The **Injection angle** table defines the injection timing (either the start or end of injection, as specified in {1} configuration). Injection timing is specified in degrees before top dead center (**TDC**) during the compression stroke.

Injector phase must be defined accurately. The angle range is from 0 to 1440 degrees to ensure a smooth transition at 0/720 degrees. For example, 800 degrees is equivalent to 80 degrees, 0 degrees is equivalent to 720 degrees, and so forth.


---

[Auto](help://Fueling/Fueling) 
##Second fuel rail

Each group contains specific information related to its respective area


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondfuelrail) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondfuelrail) 
##Staged inj. split

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Custom corr. #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Fueltables) 
##VE table #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Fueltables) 
##Lambda trgt. #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Acc. CLT correction

The **__Acc. CLT correction**__ table defines the correction of acceleration enrichment based on the engine temperature. In the case of a cold engine, the level of acceleration enrichment should be higher than for an engine warmed up to operating temperature.

---

[Auto](help://Fueling/Fueling) 
##Ethanol correction

The Ethanol correction table defines the injection timing correction depending on the ethanol content in the fuel. In the case of using a FlexFuel sensor, the ethanol content is taken from the sensor readings; otherwise, the value defined in the Fueling/General/Ethanol content options is considered.

It should be emphasized that in most countries, fuels available at gas stations contain ethanol additives (e.g., within the European Union, this can be up to 10%).

This table contains the correct fuel correction for gasoline density of 0.723 g/cm3 and standard ethanol density of 0.789 g/cm3. Depending on the manufacturer, gasoline density may vary, and the values in this table may require correction. 

For example, for a gasoline density of 0.770 g/cm3, the correction table will look as follows:

![ethanolContent.png](Images/ethanolContent.png)


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##Ethanol correction

The Ethanol correction table defines the injection timing correction depending on the ethanol content in the fuel. In the case of using a FlexFuel sensor, the ethanol content is taken from the sensor readings; otherwise, the value defined in the Fueling/General/Ethanol content options is considered.

It should be emphasized that in most countries, fuels available at gas stations contain ethanol additives (e.g., within the European Union, this can be up to 10%).

This table contains the correct fuel correction for gasoline density of 0.723 g/cm3 and standard ethanol density of 0.789 g/cm3. Depending on the manufacturer, gasoline density may vary, and the values in this table may require correction. 

For example, for a gasoline density of 0.770 g/cm3, the correction table will look as follows:

![ethanolContent.png](Images/ethanolContent.png)


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Acc. async. enrich.

The **__Acc. async. enrich.**__ table defines the percentage of the current injection time that will be injected asynchronously to achieve the quickest possible formation of an additional fuel film during rapid acceleration.
The value of 0% means that the current injection time will be applied, the value of -100% disables the additional fuel injection, and the value of 100% doubles the current injection time for async. injection.. 









---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Enrichment correctiom

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Enrichment correction

The **__Enrichment correction**__ table allows for the correction of acceleration enrichment based on a user-defined function (**__TPS, MAP**__ for the X-axis, and **__RPM**__ or **__TPS rate**__ for the Y-axis). 0% means  correction.








---

[Auto](help://Fueling/Fueling) 
##Autotune

The **Autotune** function is a tool used to analyze gathered log data and assist in building an accurate **VE** (Volumetric Efficiency) table. The process involves three main steps:

* Gathering Data (Making Logs)
* Processing Data
* Analyzing Data and Applying VE Changes


**1. Gathering Data

Gathering data is the most critical part of the autotune process. To ensure accurate results, it is essential to maintain the engine in a steady state across as many load and RPM setpoints as possible. Data collected during transient conditions (e.g., acceleration) will be ignored.

**Key Considerations:

* Engine Temperature -the engine coolant should be at normal operating temperature during data collection.
* EGO Correction -  using **Short term trim** correction is allowed during data collection.
* Variety of Driving Conditions - collect data using different gears and varying throttle positions to cover as much of the **VE** table as possible.
* Lambda target table: Ensure that a **Lambda target** table is built before starting the autotune process.

--
**2. Processing Data

Once data has been gathered, the next step is to process it.

**Steps for Processing Data:

 * Calibration - ensure that the calibration used during data logging is loaded (or that the EMU with the calibration is connected) and that the appropriate datalog is present.
* Opening the Autotune Tool -  access the **Autotune tool**  through **Menu / Tools / Autotune** or by clicking Autotune icon in the main tree view. 


**Autotune Parameters Description

![autotuneWnd.png](Images/autotuneWnd.png)

* **Min./ Max. RPM** - the RPM range for valid data samples.
* ** Min./ Max. TPS** - the TPS (Throttle Position Sensor) range for valid data samples.
* ** Min./ Max. MAP** - the MAP (Manifold Absolute Pressure) range for valid data samples.
* ** Transients delay**  - the time after a transient condition (e.g., fuel resume, acceleration/deceleration enrichment) during which all collected data will be ignored.
* **VE table** - the table that will be modified. It is important that this table must be the same as the table used during data collection.


After pressing the OK button, the data will be processed, and the Autotune window will appear. This window is also accessible from the left tree view under Log / Autotune.
--
** 3. Analyzing Data and Applying VE Changes

The final step is analyzing the data and applying changes to the VE table.

![autotune.png](Images/autotune.png)


** Analyzing and Applying VE Changes:

* **Proposed VE Table** - the base view shows the proposed VE table. Cells calculated from the log are clear, while cells not calculated are masked (hatched). When selecting any cells in the **Autotune table**, the corresponding cells in the VE table will also be selected. To apply changes from selected cells to the VE table, right-click to show the context menu and select **Apply selection 100%** or **Apply selection 50%**. Alternatively, press **S** to apply selection 100% and **ALT+S** to apply selection 50%. Applying 100% copies the proposed VE values to the VE table, while applying 50% averages the VE table and proposed VE values.

* **Actual lambda view** - displays the measured Lambda during data collection.

* **Number of collected samples view** -  Shows the number of data samples used for calculating the proposed VE table the more samples, the better proposed VE values.

* **Actual lambda difference view** - displays the difference between the Lambda/AFR target and the measured Lambda. A larger difference indicates that a larger VE change is required.

* **Actual VE difference view** - shows the difference between the proposed VE values and the current VE table.

--
** Step-by-Step Autotune Procedure

* Prepare a VE table that allows the engine to run and ensures that the mixture is rich at high engine loads.
* Prepare the Lambda target table.
* Drive the car under various load and RPM conditions.
* Run the Autotune tool.
* Apply changes to the desired VE cells.
* Manually correct unmodified VE table cells (those not visited during the test drive) to match the autotuned ones. You can use the Equalize function (E button on selected cells).
* Clear the log.
* Repeat the procedure from step 3.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Corrections) 
##IAT user correction

A table defining fuel dose correction based on intake air temperature.

!!**⚠It should be emphasized that IAT is already considered in the mathematical model used to calculate the fuel dose (air density). This function can be used for additional enrichment, for example, in cases of very high intake air temperatures.

---

[Auto](help://Fueling/Fueling) 
##Secondondary injectors

Each group contains specific information related to its respective area


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondondaryinjectors) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondondaryinjectors) 
##Second injectors cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondondaryinjectors) 
##Staged inj. split

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Fueling/Fueling) 
##Secondary injectors

Staged injection refers to a fuel injection strategy where multiple injectors per cylinder are used, and they operate at different stages to optimize performance. The main goal of staged injection is to improve power output, fuel efficiency, throttle response, and control over the air-fuel mixture across a wide range of engine speeds and loads.

Here's how it typically works:

**Low RPM/Light Load Conditions** - at lower engine speeds and light loads, only one set of injectors (typically called the primary injectors) operates. This ensures precise fuel delivery and efficient combustion for normal driving or lower performance requirements.

**High RPM/Heavy Load Conditions** - as engine speed and load increase, the secondary injectors are activated to supply additional fuel. This secondary injection stage ensures that the engine gets enough fuel to match the increased air intake, thus maximizing power and performance during high-demand situations, such as during acceleration or racing conditions.

The EMU allows injectors to be connected to two injector outputs, which deliver fuel simultaneously, twice during the engine's operating cycle. Typically, up to four high-impedance injectors (> 12 Ohm) can be connected to one output. If there are more injectors or if they have lower impedance, both outputs should be used to avoid damaging the output transistor.

The {1} table allows you to define what percentage of the calculated fuel dose should be delivered by the primary injectors and what percentage by the additional secondary injectors.

**Logging channels:

* __   **Secondary inj. PW ** __ - pulse width of  secodnary injectors. Since the secondary injectors deliver fuel twice during the cycle, the injection time is half as long as it would be if the fuel were delivered once per cycle.
* __   **Secondary inj. DC ** __ - duty cycle of secondary injectors. The duty cycle should not exceed 90%.
* __   **Secondary inj. split ** __ - defines the percentage split of the fuel dose between the primary and secondary injectors. 0% means that all the fuel should be delivered by the primary injectors, while 100% means that the entire fuel dose should be delivered by the secondary injectors. **If the activation conditions for the secondary injectors (RPM, TPS, MAP) are not met, the inj. split value is 0%.







 






---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondaryinjectors) 
##Parameters

{#1}




---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondaryinjectors) 
##Second injectors cal.

Injectors dead time calibration refers to the process of accounting for the delay between when an injector is commanded to open and when it actually begins delivering fuel. This delay, known as "dead time" or "latency," is caused by the time it takes for the electrical signal to open the injector and for the fuel to start flowing.

Dead time can vary based on factors such as battery voltage, injector type, and fuel pressure. Accurately calibrating this delay is crucial for precise fuel delivery, especially at low pulse widths, where the dead time can significantly affect the amount of fuel injected. If not properly calibrated, it can lead to inconsistent fueling, affecting performance, idle stability, and overall drivability.

The **Secondary injectors calibration** table defines the latency for the secondary injectors depending on the vehicle's electrical system voltage. The lower the voltage, the greater the latency.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Secondaryinjectors) 
##Staged inj. split

This table allows you to define what percentage of the calculated fuel dose should be delivered by the primary injectors and what percentage by the additional secondary injectors. 
**0%** means that all the fuel should be delivered by the primary injectors, while **100%** means that the entire fuel dose should be delivered by the secondary injectors.

**If the activation conditions for the secondary injectors (RPM, TPS, MAP) are not met, the inj. split value is 0%.












---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Flexfuel) 
##Custom cal.

The Flex fuel custom calibration table allows creating a custom sensor characteristic. To activate this function, the Enable custom calibration option must be enabled in the {1} settings.



---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##Rich limit

**Rich limit **table defines the maximum allowable fuel enrichment (Short term trim correction > 0%) as a function of airflow through the engine.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##Lean limit

**Rich limit **table defines the maximum allowable fuel leaning (Short term trim correction < 0%) as a function of airflow through the engine.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Acceleration) 
##Async acc. CLT correction

The **__Async acc. CLT correction**__ table defines the correction of asynchronous acceleration enrichment based on the engine temperature. 


---

[Auto](help://Fueling/Fueling) 
##Cylinders trim

Cylinder trim allows for adjusting the fuel dose on an individual engine cylinder. For each cylinder, you can input a fixed correction ({1}) and assign one of the four 3D fuel trim maps to adjust the dose based on load and RPM.








---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Cylinderstrim) 
##Trim tables assignemet

These parameters allow assigning the {1} correction table to a specific engine cylinder. The value from the 3D fuel trim table is summed with the {2} value defined for the respective cylinder.

The value **__Do not use corr. table**__ means that no 3D correction will be applied to the specific cylinder. The value **__Use fuel trim table**__ assigns the selected 3D table to the respective cylinder.


---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Cylinderstrim) 
##Trim

The injectors trim configuration is used to adjust the fuel dose for individual cylinders, making it useful for fine-tuning fuel delivery on a per-cylinder basis.  Positive values indicate an increase in the fuel dose, while negative values indicate a decrease.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Cylinderstrim) 
##Fuel trim 1

This table defines the fuel dose correction based on engine load and RPM. It can be assigned to any cylinder.
 Positive values indicate an increase in the fuel dose, while negative values indicate a decrease.

---

[Auto](help://Fueling/Fueling) [Auto](help://Fueling/Shorttermtrim) 
##Short term

{#1}


---

