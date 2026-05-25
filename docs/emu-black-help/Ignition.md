##Ignition

--

##** Troubleshooting**

**Trigger Errors**

During normal engine operation, the Trigger Error parameter should display **NO ERROR**.
Any other value indicates an issue that must be resolved.

* **TOOTH OUT OF RANGE** - the expected missing or extra tooth was not detected when it should have been. Check sensor wiring and shielding. Verify trigger edge settings.
* **UNEXPECTED MISSING TOOTH**  - An unexpected missing or extra tooth was detected. This may indicate a trigger wheel concentricity issue. When a __**VR sensor**__ is used for the __**Primary trigger**__, and an unexpected missing tooth error occurs, a 4.7k&#x3a9;-20k&#x3a9; resistor can be connected in series between the sensor output and the primary trigger input. Additionally, enabling the puld-down resistor may help stabilize the signal.
* **FALSE PRIMARY TRIGGER FILTERED** - The primary trigger decoder detected an unexpected pulse that was ignored.
* **FALSE SECONDARY TRIGGER FILTERED** - The camshaft trigger decoder detected an unexpected pulse that was ignored.
* **FALSE CAM2 TRIGGER FILTERED** - The CAM 2 decoder detected an unexpected pulse that was ignored.



**CAM sync trigger tooth

The CAM sync trigger tooth log channel indicates the index of crankshaft  tooth associated with ignition synchronization.

* When using a Multitooth trigger wheel, the parameter value must be constant and equal to the number of teeth on the trigger wheel. Any fluctuation in the CAM Ssync trigger tooth value can cause changes in the base ignition angle, potentially leading to engine malfunction. Please check the cam signal trigger edge.

* When using a missing/additional tooth trigger wheel, the CAM sync trigger tooth value may vary. This is because the camshaft signal is used only to determine the engine stroke, not the base ignition angle. 

If errors related to camshaft signal interference occur, the sensor connection and shielding should be checked.

** Dwell error

The **Dwell error** log channel is a useful indicator of trigger signal issues.

If the engine does not run correctly within a specific RPM range and, at the same time, the Dwell error log channel shows significant fluctuations in coil charging time, this may indicate problems with the trigger signal.



---

[Auto](help://Ignition/Ignition) 
##Trigger wizard

The **Trigger Wizard** enables automatic configuration of trigger parameters, firing order, ignition coil assignments, and injectors.



---

[Auto](help://Ignition/Ignition) 
##Firing order

The firing order defines the sequence of engine ignition events. A typical firing order for four-cylinder engines is **1-3-4-2**, meaning that the air-fuel mixture is ignited first in cylinder 1 (counting from the timing belt/chain), then in cylinder 3, followed by 4 and 2.

In the case of EMU, the sequence of ignition and fuel injection events is based on the firing order.

{#1}


---

[Auto](help://Ignition/Ignition) 
##Coils

EMU has built-in output stages that support both passive coils (ground-triggered, without active electronics) and active coils (positive voltage-triggered).

Incorrect coil type selection in Coils / Ignition Outputs may result in no spark, even if the trigger is correctly configured.

The correct connection and configuration of ignition coils can also be tested using Tools / Test Outputs. 
This tool generates pulses to the ignition outputs, allowing a visual inspection of the spark.

**__Passive Coil Wiring diagram

![ignition/coilsPassive.png](Images/ignition/coilsPassive.png)

**!!⚠Never connect two passive coils to a single EMU output!


**__Active coils or coils with external ignition modules wiring diagram

![ignition/coilsActive.png](Images/ignition/coilsActive.png)


For active coils, it is possible to connect two coils to a single ignition output.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Coils) 
##Coils dwell wizard

A tool used to automatically generate values in the Coil Dwell Table for a selected ignition coil.

!!**⚠It should be emphasized that the Coil Dwell Wizard only generates the table and does not store any information about the selected ignition coil. As a result, each time the wizard is run, the desired coil must be selected again.










---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Coils) 
##Ignition outputs

The ignition output options are used for configuring ignition coils and how they are assigned to the ignition outputs (IGN) of the device.

{#1}

**Coils with built-in amplifier**
Coils with built-in ignition modules or external ignition modules. Coil charging starts on the rising edge of the control signal, and the spark is triggered on the falling edge.
![ignition/coilType_active_coils.png](Images/ignition/coilType_active_coils.png)

**Coils without amplifier**
Coils without an ignition module. Coil charging is controlled by the low state of the ignition output. Due to the high possible current draw (up to 15A), this type of coil should not be paired with another coil on the same output.
![ignition/coiltype_passive_coils.png](Images/ignition/coiltype_passive_coils.png)

**CDI pulse, spark at falling**
Control method designed for CDI modules. The spark occurs on the falling edge, followed by charging the CDI module's capacitor.
![ignition/coiltype_CDI_falling.png](Images/ignition/coiltype_CDI_falling.png)

**CDI pulse, spark at rising**
Control method designed for CDI modules. The spark occurs on the rising edge, followed by charging the CDI module's capacitor.
![ignition/coiltype_CDI_rising.png](Images/ignition/coiltype_CDI_rising.png)



---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Coils) 
##Coil dwell time

The **Coil dwell time** table defines how long the ignition coil remains energized as a function of battery voltage. Lower battery voltage requires a longer dwell time to ensure proper coil charging.

Short dwell times may cause a weak spark and misfires and excessively long dwell times may lead to coil overheating.

To create the **Coil dwell time** table, it is recommended to use the {1} or refer to the ignition coil manufacturer's datasheet.


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Coils) 
##Dwell RPM corr.

The **Coil dwell RPM correction** Table adjusts coil dwell time as a function of **RPM**. It is common to increase dwell time at low RPM to improve combustion efficiency. Due to the low engine speed, the thermal stress on the coil does not increase significantly.

!!**⚠A value of 0 means no correction; positive values increase the dwell time, while negative values decrease the coil dwell time.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Coils) 
##Dwell MAP corr.

The **Coil dwell MAP correction** table adjusts coil dwell time based on manifold absolute pressure (**MAP**). It is common to increase dwell time at high **MAP** values (boosted applications) to improve combustion efficiency.

!!**⚠A value of 0 means no correction; positive values increase the dwell time, while negative values decrease the coil dwell time.

---

[Auto](help://Ignition/Ignition) 
##Corrections

Corrections allow for adjusting the ignition angle based on various engine operating parameters.

**Logging channels:

* **__I.Idle__** - the Idle control strategy controls the ignition timing.
* **__I.KS Correction__** - ignition correction is active due to the Knock Sensor Strategy.
* **__I.Soft Rev Limiter Correction__** - ignition correction is active due to the Rev Limiter Strategy.
* **__I.Custom Correction 1, 2, 3__** - a custom ignition correction is active.
* **__I.LC Correction__** - ignition correction is active due to the Launch Control Strategy.
* **__I.Nitrous Correction__** - ignition correction is active due to the Nitrous Strategy.
* **__I.Pit Limiter Correction__** -  ignition correction is active due to the Pit Limiter Strategy.
* **__I.Rolling LC Correction__** -  ignition correction is active due to the Rolling Launch Control Strategy.
* **__I.Ignition Angle Lock__** - the ignition angle is locked by the Ignition Angle Lock function.
* **__I.ALS Correction__** -  ignition correction is active due to the Anti-Lag System (ALS) Strategy.
* **__I.TC Correction__** -  ignition correction is active due to the Traction Control Strategy.
* **__I.FS Correction__** -  ignition correction is active due to the Flat Shift Strategy.
* **__I.Timer Correction__** - ignition correction is active due to the Timers Strategy.
* **__I.Lambda Guard__** -  ignition correction is active due to the Lambda Guard Strategy.
* **__I.DSG Correction__** -  ignition correction is active due to the DSG Gearbox Control Strategy.
* **__I.Rev Matching__** -  ignition correction is active due to the Rev Matching Strategy.
* **__I.User Function Corr__** -  ignition correction is active due to a User-Defined Function.


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Corrections) 
##Custom corrections

{#1}


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Corrections) 
##Cylinders trim

The Cylinder trim parameters  define ignition angle correction for each cylinder.
Negative values indicate ignition retard, positive values indicate ignition advance.

**!!⚠Warning! The Cylinder Trim function works only when the camshaft signal is used for full synchronization of the engine cycle.


{#1}


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Corrections) 
##Custom corr. 1

The **Custom correction** table is used to adjust the ignition timing advance based on user-selected logging channels. The correction becomes active when the conditions defined in the {1} configuration are met.
Negative values indicate ignition retard, positive values indicate ignition advance.









---

[Auto](help://Ignition/Ignition) 
##Ign. tables

**__Ignition tables**__ define the base ignition timing as a function of engine load and RPM.

The load axis depends on the parameter set in {1}

* **Speed Density** - the X-axis is represented by MAP.
* **Alpha N** - the X-axis is represented by TPS.
* **Alpha N with MAP multiplication** - the X-axis is represented by TPS.
* **Alpha N with MAP-based ignition** - the X-axis is represented by MAP.
* **Alpha N with MAP multiplication and MAP-based ignition** - the X-axis is represented by MAP.


!!⚠It is important to emphasize that this is the base ignition timing, and its final value may differ due to currently active strategies!

It is possible to define two independent base ignition timing tables. These tables can be switched depending on the fuel type, ethanol content in the fuel, or, for example, VTEC activation. The ignition table switching is configured in {2}.

!!**⚠IMPORTANT!** The values in the Ignition angle table are valid only when the base ignition angles ({3} and {4}) are correctly configured!

The resolution of this table is 0.5 degrees. Positive values indicate a spark before TDC (Top Dead Center) and negative values indicate a spark after TDC.






---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Ign_tables) 
##Ign. table 1

A value of **0** degrees means the spark will occur exactly at **TDC**. Positive values indicate the spark will occur before TDC, while negative values indicate the spark will occur after **TDC**.

---

[Auto](help://Ignition/Ignition) 
##Rev limiters

The **Rev limiters** strategy allows setting the rev limiter based on parameters such as CLT, engine oil temperature, ethanol content, etc. It also defines the method by which torque limitation will be implemented (fuel, ignition, throttle closure).

The primary safeguard for the engine against excessive RPM is the **RPM limit** parameter within the {1}. When the **RPM limit** is exceeded, fuel will be completely cut off to protect the engine from damage.

The rev limit set by the **Rev limiters** should always be configured below the RPM limit defined in {2}.

It is possible to define two different parameterizations of the rev limiter (**Rev Limiter 1** and **Rev Limiter 2**). Depending on the needs, one limiter can be a "soft limiter," and the other, for example, a loud limiter with pops and bangs.

In addition to the limiters defined in the **CLT limit**, **Ethanol limit**, **IAT limit**, **Oil temp limit**, and **Custom rev limit** tables, it is possible to set the rev limit using {3}.

The strategy compares the requested rev limit from the above tables and functions and always selects the lowest value!

!!**  ⚠ Please note!  Launch control and Rolling start strategies use the rev limiter mechanism to maintain the target RPM. When these strategies are active, the rev limiter parameters are taken from the Launch control or Rolling start settings. In this case, the __Rev limiter target source__  is set to either __Launch control__ or __Rolling start__.

**Logging channels:

* **__Rev limiter target__** - the desired RPM for the rev limiter.
* **__Rev limiter target source__** - when the rev limiter is active, this channel shows which table/function is responsible for the rev limiter's target RPM.
* **__Active rev limiter__** - the type of active limiter.
* **__Rev limiter target CAN BUS__** - the target RPM received from the CAN BUS.



**Meaning of  Rev limiter target source statuses:

* **__None__** - no active rev limiter.
* **__CLT__** - rev limiter RPM defined in the CLT table.
* **__IAT__** - rev limiter RPM defined in the IAT table.
* **__Oil temp.__** - rev limiter RPM defined in the Engine oil temp. table.
* **__Custom__** - rev limiter RPM defined in the Custom table.
* **__Ethanol__** - rev limiter RPM defined in the Ethanol content table.
* **__Function__** - rev limiter RPM set by a function.
* **__CAN BUS__** - rev limiter RPM set by the CAN BUS.
* **__Fuel pressure prot.__** - rev limiter RPM set by the Fuel pressure protection strategy.
* **__Launch control__** - rev limiter RPM set by Launch control strategy
* **__Rolling start__** - rev limiter RPM set by Roling start strategy



**Meaning of  Active rev limiter statuses:

* **__None__** - The rev limiter is not active.
* **__Limiter 1__** - Active rev limiter defined by the Rev limiter 1 parameters.
* **__Limiter 2__** - Active rev limiter defined by the Rev limiter 2 parameters.
* **__RPM Fuel cut__** - Complete fuel cut-off for the RPM defined in the Fueling/Fuelcut.



---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##General

{#1}


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##Rev Limiter 1

The **Rev limiter** parameters define how the engine should behave during RPM limiting (how torque should be limited).

To achieve the smoothest RPM limitation, you should use fuel cutting (**Cut type Fuel** or **Per cylinder fuel cut**), slight ignition retardation, and, if using an electronic throttle, override the DBW (Drive-By-Wire) position and set the throttle opening to the smallest value that allows maintaining the cutoff RPM.

To achieve the "pops and bangs" effect, you should use ignition cutting (**Cut type Spark**) and significantly retard the ignition timing.

!!**⚠If the vehicle has a catalytic converter, ignition cutting should not be used, as unburnt fuel igniting in the catalytic converter will lead to its rapid destruction!


{#1}


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##CLT limit

The maximum engine RPM depending on the coolant temperature.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##Ethanol limit

The maximum engine RPM depending on the ethanol content in the fuel.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##IAT limit

The maximum engine RPM depending on the intake air temperature.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##Oil temp. limit

The maximum engine RPM depending on the engine oil temperature.

---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##Custom rev limit

A limiter defined using the rotary switch. Depending on its position, the driver can set different RPM values. The selection of the rotary switch is located in the {1} options.


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Revlimiters) 
##Rev limiters

{#1}


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Triggers) 
##Primary trigger

The configuration of the connected sensor type and the active signal edge can be found in {1}.

The **Primary trigger** options are responsible for configuring the ignition system and the base ignition advance. The signal source (sensor) can be located on either the crankshaft or the camshaft.

**!!⚠After any modification to the ignition system parameters, it is necessary to verify the ignition timing advance using a timing light.

**!!⚠Proper configuration of the ignition system is essential for the safe operation of the engine!

{#1}

**Trigger phase synchronization with camshaft sensor signal level

In many engines, the camshaft sensor provides a **high** level during one missing-tooth gap and a **low** level during the other.  EMU Black can read the camshaft signal state directly after the missing teeth are detected and uses this information to determine the correct phase of the engine cycle.

This allows the ECU to:
- Identify the engine phase **immediately** after detecting the first missing-tooth gap.  
- Start **fuel injection** and **ignition** without waiting for a camshaft edge.  
- Achieve **faster and more reliable engine starts**.  

In the built-in oscilloscope:
- A **circle marker** is displayed at the first tooth after the missing gap.  
- **Circle in the middle** → camshaft signal was **low**.  
- **Circle at the top** → camshaft signal was **high**.  

**Limitations: 
- Available only for crank triggers with **1, 2, or 3 missing teeth**.  
- Requires a **stable and correctly aligned camshaft position sensor signal**.  
- If the camshaft signal is noisy, misaligned, or inconsistent, phase synchronization may fall back to standard edge detection.  
- Proper configuration of the trigger system is essential for reliable operation.  
--
** AUDI TRIGGER 135 TEETH

This system, also known as the "Audi trigger", consists of 3 sensors (2 VR sensors on the crankshaft and 1 Hall sensor located on the camshaft). The crankshaft sensors read the signal from a toothed ring consisting of 135 evenly spaced teeth (connect to primary trigger) and a single pin (connect to cam sync input). Due to the fact that in one engine cycle a single tooth generates an impulse twice, it cannot be used directly as a synchronizing signal for the ignition system. 
The Hall sensor installed on the camshaft reads the signal from a single tooth. This signal masks 1 of the 2 impulses from CAM sensor 1. To configure the Audi 135 Teeth trigger, you should select "Audi trigger home" as CAM 1 type and "Audi trigger CAM" as CAM 2. 

**!!⚠In the case of the Audi trigger, only __Injection Angle Control Start at ignition event__ can be used.

The EMU processes the signal into 60 equal pulses per crankshaft revolution. 
We suggest changing the ignition system to the 60-2 system using the original rear main seal crank trigger kit (WV 036105189C).

The diagram below shows the EMU oscilloscope trace for the Audi trigger signal.

![ignition/audiTriggerScope.png](Images/ignition/audiTriggerScope.png)
--
**BMW E30 M3 116 TEETH

This trigger pattern is specific to the 4-cylinder BMW E30 M3 2.0L 4 cylinder engine.
It is characterized by the fact that the synchronization tooth (1 pin) is located on the crankshaft. Therefore, this system can be used for wasted spark or distributor ignition operation.
The EMU converts this signal to 4 teeth per revolution of the crankshaft, synchronizing the engine operation to every other occurrence of the synchronizing signal with the crankshaft.
This synchronisation sensor should be connected to the CAM#1 input and the pattern selected: 1 tooth on the crankshaft.

!!⚠Due to limitations of such solutions, we strongly recommend the use of an aftermarket 60-2 toothed wheel, which guarantees the highest precision in controlling the ignition advance angle.
--
**CAM TOOTHED WHEEL WITH ADDITIONAL TOOTH

The trigger pattern occurring on the camshaft consists of evenly spaced teeth along with an additional tooth used for synchronization. Due to the fact that this trigger pattern occurs on the camshaft, it enables operation in a full sequence of injection and ignition. The **__Num teeth__** parameter must be half the number of teeth on the camshaft gear excluding the additional tooth. For example, for a camshaft gear of 24+1 teeth, the **__Num teeth**__ parameter should be set to **12**.

!!⚠Full cycle synchronization is performed automatically, and the secondary trigger should be set to __**Do not use**__
--
**CAM TOOTHED WHEEL WITH MISSING TOOTH

The trigger pattern occurring on the camshaft consists of evenly spaced teeth along with one missing tooth used for synchronization. Due to the fact that this trigger pattern occurs on the camshaft, it enables operation in a full sequence of injection and ignition. The**__Num teeth__** parameter must be half the number of teeth on the camshaft gear including the missing tooth. For example, for a camshaft gear of 24-1 teeth, the **__Num teeth__** parameter should be set to **12**.

!!⚠Full cycle synchronization is performed automatically, and the secondary trigger should be set to __**Do not use**__
--
**CAM TOOTHED WHEEL WITH 2 MISSING TEETH

The trigger pattern occurring on the camshaft consists of evenly spaced teeth along with two missing teeth used for synchronization. Due to the fact that this trigger pattern occurs on the camshaft, it enables operation in a full sequence of injection and ignition. The **__Num teeth__** parameter must be half the number of teeth on the camshaft gear including the missing teeth. For example, for a camshaft gear of 48-2 teeth, the **__Num teeth**__ parameter should be set to **24**.

!!⚠Full cycle synchronization is performed automatically, and the secondary trigger should be set to __**Do not use**__
--
**NISSAN 

The Nissan trigger is a standard triggering mechanism employed in Nissan engines such as RB20, CA18DET, RB30DET, etc.. It relies on a disc and two optical sensors installed on the camshaft. One sensor detects 360 evenly spaced falling-edge pulses (every 2 degrees of crankshaft rotation), while the other, known as the home signal, consists of slots equal to the engine's cylinder count. Each slot has a width corresponding to a multiple of pulses from the first sensor (e.g., 4, 8, 12, etc.).
The EMU processes the signal into 60 equal pulses per crankshaft revolution, and synchronization occurs by identifying the slot with a unique number of pulses from the first sensor. To configure, connect sensor 1 (360 pulses) to the primary trigger input and sensor 2 to the CAM#1 input (Secondary trigger). Both sensors are optical sensors (select Hall) and should have a enable pull-up of 820 ohms.
Choose a falling edge for both the primary trigger and CAM#1 input. Do not activate any filtering! 
On the built-in oscilloscope, identify a unique window (occurring only once per cycle). In the camshaft configuration, select the number of pulses visible on the camshaft signal graph.

![ignition/nissanTrigger.png](Images/ignition/nissanTrigger.png)

Due to the design, potential mechanical wear, and the fact that sensors are installed on the camshaft, ignition timing accuracy is limited. Hence, we recommend using an aftermarket trigger kit installed on the engine's crankshaft.

!!**⚠In the case of the Nissan trigger, only __Injection Angle Control Start at ignition event__  can be used.
--
**NISSAN VQ35

For the VQ35 engine, the crankshaft trigger wheel is divided into three groups of 10 teeth, separated by two gaps. This pattern makes it impossible to start the engine without determining the current cylinder position using the camshaft position sensor signal.

Decoding the camshaft signal is performed using the Factors Sequence decoder with the following parameters:

In range 1 min: **1.7
In range 1 max: **2.6
In range 2 min: **0.297
In range 2 max: **0.7

**!!⚠For the camshaft sensors in the VQ35 engine, the __falling edge__ must always be used.

Depending on which camshaft sensor is connected to the CAM #1 input, the Invert phase parameter must be set in the Ignition / Firing Order settings.
The crankshaft signal is converted to a pattern of 12 equally spaced teeth (multitooth 12).

**Automatic configuration of the trigger can be performed using the Trigger Wizard preset (Nissan VQ35).
--
**PORSCHE 132 TEETH 

This trigger pattern is specific to the 4-cylinder Porsche Porsche 944 engine.
It is characterized by the fact that the synchronization tooth (1 pin) is located on the crankshaft. Therefore, this system can be used for wasted spark or distributor ignition operation.
The EMU converts this signal to 4 teeth per revolution of the crankshaft, synchronizing the engine operation to every other occurrence of the synchronizing signal with the crankshaft.
This synchronisation sensor should be connected to the CAM#1 input and the pattern selected: 1 tooth on the crankshaft.

!!⚠Due to limitations of such solutions, we strongly recommend the use of an aftermarket 60-2 toothed wheel, which guarantees the highest precision in controlling the ignition advance angle.
--
**PORSCHE 129 TEETH 
This trigger pattern is specific to the 6-cylinders 3.2L Porsche 911 engine.
It is characterized by the fact that the synchronization tooth (1 pin) is located on the crankshaft. Therefore, this system can be used for wasted spark or distributor ignition operation.
The EMU converts this signal to 3 teeth per revolution of the crankshaft, synchronizing the engine operation to every other occurrence of the synchronizing signal with the crankshaft.
This synchronisation sensor should be connected to the CAM#1 input and the pattern selected: 1 tooth on the crankshaft.


!!⚠Due to limitations of such solutions, we strongly recommend the use of an aftermarket 60-2 toothed wheel, which guarantees the highest precision in controlling the ignition advance angle.
--
**RENAULT  CLIO WILLIAMS  44-2-2, RENIX, 4 cylidners

This trigger is converted to two teeth on the crankshaft. It requires a distributor ignition system, as there is no synchronization with the camshaft sensor.
--
**RENAULT  CLIO WILLIAMS  66-2-2-2, RENIX, 6 cylidners

This trigger is converted to three teeth on the crankshaft. It requires a distributor ignition system, as there is no synchronization with the camshaft sensor.
--
**TFI

TFI is an ignition system used by Ford in the 1980s and 1990s. To utilize this system with the EMU device, connect the PIP signal from the TFI module (pin 6) to the primary trigger input and select the HALL sensor type. Connect the EMU ignition output directly to the ignition coil. Due to the operation principle of the TFI module, it ensures full synchronization with the engine's operation cycle, enabling the engine to operate in a full ignition and fuel injection sequence. The current implementation of TFI module support in EMU allows operation for 6-cylinder engines. For a different number of cylinders, please contact tech support (tech@ecumaster.com).


---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Triggers) 
##Secondary trigger

The configuration of the connected sensor type and the active signal edge can be found in {1}.

{#1}

**Engine Synchronization with Camshaft Signal

To enable the engine to operate in full sequential ignition and fuel modes, synchronization of the crankshaft position within the engine's operating cycle is required.
When the primary trigger signal is derived from a crankshaft position sensor, it is not possible to determine the crankshaft's position within the 720-degree engine cycle. Certain patterns, such as 60-2, allow determining the position within a single revolution (360 degrees), enabling the engine to start in wasted spark mode, where ignition coils fire twice per cycle for each cylinder. However, other patterns, like multitooth, do not allow crankshaft position determination, making engine start impossible without synchronization with the camshaft.

**Camshaft Signal Patterns

Camshaft signal patterns vary widely, from a single tooth to multiple teeth at varying intervals. Depending on the selected signal edge (rising or falling), the pattern appearance may differ. For example:

**Falling edge**: Four evenly spaced teeth may render decoding ambiguous.
**Rising edge**: Teeth may be unevenly spaced, allowing effective decoding.

**Determining the start of the cycle

The method of defining tooth 0 after synchronization depends on the trigger pattern:
* Non-unique crankshaft triggers (e.g., multitooth): Tooth 0 is the first crankshaft tooth read after synchronization. **Example:** A multitooth 12 pattern on the crankshaft and one tooth on the camshaft.
* Unique crankshaft triggers (e.g., 60-2): Tooth 0 is the first tooth after synchronization, typically the first tooth following the gap in a missing-tooth pattern. **Example:** A 60-2 pattern on the crankshaft and one tooth on the camshaft.


**Signal Edge Selection

Edge configurations for crankshaft and camshaft signals should maximize the separation between their corresponding teeth. If the signals overlap, chain or belt slack may cause the camshaft signal to be read after what was previously tooth 0, resulting in a one-tooth timing shift and affecting ignition timing. 
For unique crankshaft patterns like 60-2, the camshaft synchronization signal position is less critical. The system can tolerate signal shifts relative to the crankshaft as long as they do not exceed the position of the first tooth after the gap. This flexibility ensures proper operation in systems with variable valve timing, where the camshaft position relative to the crankshaft changes dynamically.

**Wasted Spark Capability

If the trigger supports wasted spark mode, the engine can start in wasted spark mode before camshaft synchronization. Additional details on this functionality are available in the {2} section.
The table below summarizes all supported trigger patterns, indicating whether engine start without a camshaft sensor signal is possible and how synchronization with the camshaft occurs (e.g., on the next crankshaft tooth or a characteristic point like a missing tooth gap).
This setup allows flexibility for various configurations and ensures reliable synchronization for optimal engine operation.

| Trigger | Start in <br> wasted <br>spark | Cam sync <br> required |Tooth 0| Comment |
| 18-2-18-2 Nissan QR25DE<br> Wrangler <br>Hemi, Dodge | No | Yes  | After gap | |
| Toothed wheel with<br> 1,2 and 3 missing teeth | Yes | No | After gap  ||
| Toothed wheel with<br> additional tooth | Yes | No | After <br>additional <br> tooth ||
|CAM toothed wheel <br>with additional tooth | No | No | After cam<br>addition<br>tooth | In the case of this trigger, synchronization occurs automatically, and for the **Secondary Trigger**, the option **Do Not Use** should be selected. Tooth number 0 is defined as the next tooth following the additional tooth.|
| Multitooth | No | Yes | Next tooth after cam sync ||
| Audi trigger 5 cyl <br> Audi trigger V8| No | Yes | Next tooth after cam sync |This system requires the connection of three signals: **Primary Trigger, CAM1 (Home)**, and **CAM2**. For more information, refer to the {3} section in the help documentation.|
| BMW E30 M3 116 teeth | No | No | N/A |Requires distributor|
|Honda J35A8| Yes(?) | No | Next tooth after 2nd gap ||
|Mazda NB| No | Yes | ????? ||
|Mitsubischi Colt 1.5CZ| | | ||
|Lancer EVO X | Yes | No | Next after XX gap  ||
|Nissan trigger | No | Yes  |   ||
|Nissan 350Z (VQ35) | No | Yes  | Next tooth after gap | Always use falling edge for CAM  signal!|
|Porsche 129 teeth<br>Porsche 132 teeth|No|Yes|N/A |It requires a distributor or a wasted spark configuration. Synchronization is achieved using a single tooth on the crankshaft, but full cycle synchronization is not possible.|
|Renault Renix | No | No  | N/A  | Requires distributor |
|Rover 18-1-18-1| No | Yes | Next tooth after gap ||
|Rover 13-1-2-1-14-1-3-1 | || ||
|Subaru 36-2-2-2 | Yes |||Some models use 3 cam sensors (1 with fixed position and 2 for VVTi) |
|Subaru 6 teeth |No |Yes|N/A ||
|Suzuki 36-2-2 |Yes |No|Next tooth after gap ||
|TFI | |No|N/A |Synchronisation based on TFI PIP signal|

** Decoders

When the camshaft gear has more than one tooth, the appropriate decoder must be selected to uniquely identify the tooth used for synchronization. In most cases, detection relies on identifying a unique **__Factor**__, which represents the timing ratio between consecutive teeth.
The **__Factor**__ value is displayed on an oscilloscope as the ratio of times between consecutive teeth. The figure below illustrates how the **__Factor**__ value is determined between camshaft teeth.

![ignition/scope_factors.png](Images/ignition/scope_factors.png)
In the diagram above, you can see the Factors (0.6, 0.4, 2.3). These values result from the ratio of time between the teeth. For example, the value 0.4 comes from 14.93/33.86, and the value 2.3 comes from 33.77/14.93.

For the above example, the unique value (in this case, the shortest one) is 0.4, and the **Shorter Than Factor** decoder can be applied with a threshold of 0.5. It is important to always leave a margin of error, as the angular velocity of the crankshaft is variable (especially during cranking), and Factor values may fluctuate.
Decoders such as **N-1, N+1, N+1 60%**, and **VW 1.8T** use internal **Longer Than Factor** and **Shorter Than Factor** logic.
In the case of the **Factor Sequence** decoder, you can specify a condition where two consecutive **__Factor**__ values must fall within defined ranges.

More information about specific decoders can be found later in the text.

In some ignition systems (e.g., **Nissan SR20DET** or **2JZ VVTi**, where the spacing between teeth is constant), such solutions cannot be used, and specific algorithms have been implemented to handle these cases. 
If the camshaft position sensor signal is lost during engine operation, the engine will continue running based on the last synchronization. Otherwise, synchronization with the camshaft occurs every engine cycle.

** Available decoders

**Do not use
No synchronization with the camshaft position sensor. This option can be used for engines with a distributor ignition system or when the trigger pattern allows unambiguous determination of the crankshaft position relative to the cylinders (e.g., 60-2).

**1 tooth
The camshaft gear has only one tooth, which is used for synchronization. This trigger is also used for engine synchronization via a MAP sensor. In the CAM1 configuration, select VR sensor sensitivity table as the sensor and adjust the MAP voltage during cranking to achieve synchronization on cylinder 1. Additionally, set the Disable camsync above RPM parameter to a value slightly higher than the cranking threshold.

**1 tooth on crankshaft
A specific decoder for systems with a primary trigger using a starter ring gear (e.g., Porsche 129) and a single tooth (pin) on the crankshaft for synchronization within 360 degrees. This system requires a distributor ignition or wasted spark coils and cannot operate in full sequential fuel mode.

**N-1
Decoder for a missing-tooth gear, using an internal **__Longer Than Factor 1.5**__ threshold.
(Include example scope illustration)

**N+1
Decoder for a gear with an additional tooth, using an internal **__Shorter Than Factor 0.5**__ threshold.

**N+1 60%
Decoder for a gear with an additional tooth, using an internal **__Shorter Than Factor 0.6**__ threshold.

**Longer than factor
Synchronization occurs if the **__Factor**__ exceeds the defined parameter.
On the scope below, the factor is defined as 1.5. When the factor on the scope reaches 2.0, the condition is met, and the next tooth becomes the sync tooth (marked with a circle).

![ignition/scope_longer_than_factor.png](Images/ignition/scope_longer_than_factor.png)

**Shorter than factor
Synchronization occurs if the **__Factor**__ is below the defined parameter.

**Factor sequence
Synchronization occurs when:

**__Factor Sequence 1**__ falls within the defined **__In Range 1 Min/Max parameters**__.
**__Factor Sequence 2**__ falls within the defined **__In Range 2 Min/Max parameters**__.

In the example below, factor **sequence 1** has a minimum value of **0.2** and a maximum of **0.5**. **Factor sequence 2** has a minimum value of **1.5** and a maximum of **2.5**. The only teeth that meet these conditions are those with factors of **0.3** and **2.0**. These parameters enable unambiguous identification of the synchronization tooth in the engine cycle.

![ignition/scope_factors_sequence.png](Images/ignition/scope_factors_sequence.png)


**Primary tooth window
Defines the range for valid crankshaft teeth during synchronization.

**VW 1.8T
A decoder for a missing-tooth gear, using an internal **__Longer Than Factor 1.66**__ threshold.

**Nissan trigger
Specific decoder for **__Nissan**__ systems with 360 slots on the camshaft. The camshaft sensor signal includes slots with lengths corresponding to 4, 8, or 12 primary trigger slots (depending on the engine model). A unique value must be selected to enable unambiguous ignition system synchronization.

**2JZ VVTi
A specific decoder for 2JZ VVTi engines, designed to handle constant tooth spacing on the camshaft.







---

[Auto](help://Ignition/Ignition) [Auto](help://Ignition/Triggers) 
##CAM 2

**CAM 2** is used to connect a camshaft position sensor for the second camshaft (not used for synchronization), in order to determine its position for variable valve timing (**VVT**) systems.
In engines such as the Toyota **1JZ/2JZ** (non-VVTi) or **Honda F20C**, it also allows for faster synchronization.

{#1}

** Available Patterns:

*  **Audi Trigger CAM** – a decoder specific to Audi engines equipped with two crankshaft position sensors (e.g., 135/136, 1) and one camshaft sensor. More information about configuring this trigger can be found in the {1} documentation.


* **Primary teeth window** – a universal decoder that allows defining a range (expressed as primary trigger tooth numbers) from which the pulse will be taken to calculate camshaft position. At the moment of changing the camshaft position angle, the tooth for which we defined the range with the **Primary trigger** must not move beyond it, nor may any other tooth enter that range.


![Scope/cam2ToothRange.png](Images/Scope/cam2ToothRange.png)

The example above shows a sample oscilloscope capture where the **primary trigger** is **60-2**, and the second camshaft (**CAM 2**) has 4 evenly spaced teeth. When the camshaft moves, it shifts toward tooth 0 of the primary trigger. The designated tooth range is **1** to **13**, which ensures the full operating range of the camshaft.


* **Mazda MX-5 (3 Teeth)** – a pattern specific to the Mazda MX-5 camshaft signal system.


* **Honda F20C – Second CAM** – utilizes the signal from the second camshaft to enable faster engine synchronization. The signal from **CAM 2** is used only for the first synchronization. After that, only **CAM 1** is used.


* **1JZ / 2JZ – Second CAM (Non-VVTi only)** – utilizes the signal from the second camshaft to enable faster engine synchronization. The signal from **CAM 2** is used only for the first synchronization. After that, only **CAM 1** is used.

---

[Auto](help://Ignition/Ignition) 
##Triggers

**Trigger Sync Status

When the ignition system is correctly configured, the __**Trigger sync status**__ should change from **SYNCHRONIZING** to **SYNCHRONIZED** during cranking.

If the status does not change, there is a trigger synchronization issue. Possible causes:

* Incorrect Primary Trigger type selected (crankshaft).
* Incorrect Primary Trigger Edge selected.
* Incorrect Secondary Trigger type selected (camshaft).
* No signal from the camshaft sensor.
* Poor ground wire routing.


The **Scope tool** in the EMU software is the primary diagnostic tool for troubleshooting trigger type and edge selection issues. You can find more about troubleshooting in {1} section.

--
**Setting up primary trigger

1. Set the engine to top dead center (**TDC**) on cylinder number **1**. In most inline engines, cylinder number 1 is the cylinder closest to the timing belt/chain. In the case of V-engines, refer to the manufacturer's manual to accurately identify cylinder 1.

![](triggersetup/img1.png )

2. Make a mark on the timing belt/chain cover and the crankshaft pulley with the engine set
at **TDC**. Use white paint or a corrector to create reflective marks for the timing light. If the
engine is equipped with factory marks, ensure they match each other and use paint to make
them more visible.

3. Connect the timing light to the high tension (HT) leads that connect the ignition coil to
the spark plug in cylinder number one. If the engine is equipped with coil-on-plug ignition
and there are no HT leads, remove the coil from cylinder number one and extend it with a
spare HT lead to the spark plug. Secure the connection between the coil and HT lead with
insulating tape.

!!**⚠Attention:** Do not connect the timing light inductive probe to the loop on the ignition signal wire to the coil. This mistake will lead to incorrect ignition timing settings.


4. Open the EMU Black V3 software and, from the Tree View, choose {2}. Select spark distribution and the appropriate coil type. If the engine is equipped with passive coils, select **__Coils without amplifier**__. If the engine is equipped with active coils or an ignition module, select **__Coils with built-in amplifier**__.

5. Navigate to menu **__Tools / Output Test**__. Select: **__Output / Ignition Out 1**__ and press the **Test button.** If the coil type is selected correctly, the strobe lamp should flash when the trigger is pressed and a spark is generated. If the strobe lamp does not flash, remove the spark plug from the cylinder head, ground the spark plug electrode, and run the test again. Observe the spark.

6. With the timing light flashing when a spark is generated, setup the trigger inputs. First, you need to configure the input parameters for the {3} and {4}. In our case, the crankshaft signal is provided by a VR (variable reluctance) sensor, and the camshaft position sensor is a Hall effect sensor.

![triggersetup/img2.png](Images/triggersetup/img2.png)

Next select the proper trigger patterns ({5} and {6}). In our case it is 60-2 for primary trigger and 1 tooth as a CAM 1.

![triggersetup/img2b.png](Images/triggersetup/img2b.png)

7. From the Tree View, open Log / Scope Window.
Press the blue arrow and tart to crank the engine. If the triggers are set correctly, lines from the decoded wheels should appear.

![triggersetup/img3.png](Images/triggersetup/img3.png)

8. To configure the base timing, you need to set the **__First trigger tooth**__ and **__trigger Angle**__ parameters correctly ({7}).

The **__First trigger tooth**__ setting determines which tooth after the secondary trigger synchronisation (in the case of missing tooth pattern the tooth 0 is the first tooth after the gap. On the scope it is marked with wider red line) will start the new engine cycle. The trigger angle defines how much the crankshaft must rotate afterthe **__First trigger tooth**__  appears to get the **__TDC**__ of the **__cylinder**__. The maximum ignition advance cannot exceed the trigger angle.
The engine rotates 360 degrees every half cycle. In this example, the trigger wheel divides
360 degrees into 60 equal parts, so each tooth represents 6 degrees of rotation.
If the ignition advance is set to 0 and **__First trigger tooth**__ is set to 3 with a Trigger Angle of 60&#xb0;, the spark will occur at **__TDC**__ on cylinder 1. The maximum possible advance in this setup is 60 degrees.

In the following example, **__First trigger tooth**__ is defined as the 9th tooth, located 60 degrees before the engine's first cylinder __**TDC__**, which is at the 19th tooth. The next ignition event is located on the 39th tooth (in a 4c ylinder engine, ignition events are spaced by 180 degrees). The trigger tooth for any ignition event must not overlap with the missing tooth (or teeth) on the trigger wheel! 

![triggerWheel.png](Images/triggerWheel.png)

9. Open the graph log from the Tree View and select the following channels:

- RPM
- MAP
- Trigger Sync Status
- Trigger Error
- Cam Sync Trigger Tooth

During cranking, the parameters on the graph will change. When the settings for the primary and secondary triggers are correct, the **__Trigger sync status**__ will change from **__No sync__** to **__Synchronized**__. Once the ECU is in a synchronized state, spark and injector pulses are generated.

![triggersetup/img5.png](Images/triggersetup/img5.png)

10. To define the firing order and assign coil outputs to cylinders, you need to set up the {8} table and {9}.

In our case In our case, the firing order is 1-3-4-2, and the ignition outputs are connected to the ignition coils corresponding to each cylinder (**__IGN OUT 1**__ to the coil on cylinder 1, **__IGN OUT 2**__ to the coil on cylinder 2, and so forth). The coils are passive coils without built-in ignition modules.

![triggersetup/img6.png](Images/triggersetup/img6.png)

11. Open the {10} window and select **__the Ignition Angle Lock**__ option. Set the **__Locked angle__** to 0 degrees.  Set the **__Trigger angle__** to 60 degrees. These settings are theoretical and will be adjusted during testing with a timing light.

![triggersetup/img7.png](Images/triggersetup/img7.png)

12. Aim the timing light at the TDC mark you created on the timing belt/chain cover. Crank the engine and observe if the crankshaft pulley mark aligns closely with the mark on the timing cover. If the mark on the pulley is not present and the timing light is flashing, increase the **__First trigger tooth__** (it will change the spark position by 6 degrees) and repeat the test with the timing light.
Continue adjusting the First trigger tooth until the crankshaft pulley mark is as close
as possible to the mark on the timing cover. Each trigger tooth adjustment changes the
ignition angle by 6 degrees (for example for 12 multitooth patter, one tooth changes the ignition advance by 30 degrees (360/12) ). Increasing the trigger tooth value will retard the ignition, while
decreasing it will advance the ignition.

13. For fine-tuning the primary trigger settings, use the **__Trigger angle__** option. Crank the engine and adjust the **__Trigger angle__** value to align the marks on the pulley and the timing cover. Increasing the angle will retard the ignition, while decreasing the angle will advance the ignition.

14. The crankshaft in a 4 - stroke engine completes two rotations for the entire engine cycle. This means that the piston reaches the top dead center (TDC) twice per cycle. It's possible for the spark to be triggered when the cylinder is in the intake stroke, in which case the engine won't start. Common symptoms of this issue include backfires in the exhaust or intake system, or the engine stalling during cranking.  To reverse the engine phase, enable the **__Invert phase__** setting in {11}.




---

