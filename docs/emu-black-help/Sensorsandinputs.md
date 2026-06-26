##Sensors setup

The Sensors setup group is used to configure analog inputs, digital inputs, and sensors that may occur in the electrical installation of a vehicle.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Analog inputs

In the configuration of analog inputs, we can set up the behavior of analog inputs, specifically the input filter and enable the internal pull-up resistor (used for NTC temperature sensors). For voltage sensors (e.g., MAP sensor), a 1M ohm pull-down should be selected. 
**__Analog input 4**__ is logged at a frequency of **250Hz** and, in the case of using the __ closed loop gear cut strategy __, this input should be used for connecting the gear position sensor. Other analog channels are logged at a frequency of **100Hz**. 

Filtering should be used for sensors with slowly changing values or exceptionally noisy signals (e.g., oil pressure or fuel pressure sensor). For sensors like throttle position or gear position sensor, filtering should not be applied as any digital filter introduces a delay that would negatively affect the strategy's performance.
It should be emphasized that the analog inputs measure voltages from **0-5V** but are resistant to voltages up to **20V.

For analog inputs, the built-in pull-up / pull-down resistors have a value of 4.7k, while for the CLT and IAT inputs, the value is **2.2K**.  This **2.2K** value is considered optimal for typical temperature sensors.

In the case of the CLT and IAT inputs, it is possible to disable the internal pull-up resistor to use an external one if the provided value is not suitable for the specific temperature sensor used, or if the CLT / IAT signal is shared with the original ECU (Engine Control Unit).

When connecting a switch to an analog input, you should enable the internal pull-up resistor and wire the switch according to the following diagram:

 ![switchToGnd.png](Images/switchToGnd.png)

**Logging channels:

* __** Analog 1 - Analog 6**__ - the voltage of the given analog inputs
* __** CAN Analog 1 - CAN Analog 8**__ the voltage of the given analog input set by CAN BUS (eg. can switch board or user defined CAN)



{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Momentary switch

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##MUX Switch

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Oxygen Sensor PID

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Oxygen Sensor

The EMU Black supports __Bosch LSU 4.9__ and __Bosch LSU 4.2__ sensors. These sensors can measure the value of the air-fuel ratio in exhaust gases and can be used for both exhaust gas monitoring and controlling fuel injection in the feedback loop __**Fueling/Short term trim.

There is an option to calibrate the internal oxygen sensor controller, which can improve the sensor readings around Lambda=1 (especially for PCB revisions older than O). To calibrate, disconnect the sensor plug from the EMU device, then from the **Tools** menu, select the __**Calibrate WBO circuit**__ function. The current calibration value can be found in the Logbook (__**Tool/Logbook/**__) and is independent of the loaded project/firmware.

!!**⚠To ensure the long-term operation of the lambda sensor, it should be installed following the manufacturer's guidelines, and it should not be exposed to vibrations or excessively high temperatures from exhaust gases and external air.

* The sensor installation position and the sensor functionality in the full system must be assured sufficiently by the customer through appropriate vehicle tests under realistic conditions of use. 
* Installation in the exhaust system must be at a position ensuring representative exhaust gas composition whilst also satisfying the specified temperature limits. Installation points in exhaust systems of passenger cars with compression ignition engine meeting all following boundary conditions:  downstream turbo charger and upstream oxidation catalyst and relating positions in systems without turbo charger (normally aspirated engine).


!! **⚠Installation positions other than mentioned above must be verified individually at own risk.

* Contamination entering the exhaust gas through the intake air or as a result of fuel, oil, sealing materials etc., might reach the sensor and lead to damage. The influence of this contamination is application specific and has to be determined by customer tests.

* The sensor installation position design must be selected in a way to minimize exhaust side stress of the sensor with exhaust gas condensate.

* The maximum continuous operating temperature for the sensor is 930°C, and the maximum short-term temperature is 1030°C.
* Motosport features like Launch Control and ALS may contribute to a shorter sensor life.
* Every sensor is factory-calibrated using a laser trim resistor, which is located in the lambda sensor connector. Never cut the connector or connect the sensor without this resistor, as the sensor readings will be incorrect.


** Design measures:
* Locate sensor as close to the engine as possible, respecting the maximum allowed temperature range.
* The exhaust pipe in front of the sensor must not contain any pockets, projections, protrusions, edges, flex-tubes etc. to avoid accumulation of exhaust gas condensate. A downwards slope of the pipe is recommended.
* Make sure that the front hole of the protection tube does not point against exhaust gas stream.
* Also make sure, that no accumulated water can flow back from locations downstream of the sensor (catalyst, muffler), e.g. when decelerating or downhill parking.
* Attempt to achieve rapid heating-up of the exhaust pipes in the area in front of the sensor and of the complete sensor thread boss area to avoid exhaust gas condensate.
* The sensor thread boss has to be designed as shown in figure  below to allow a rapid heat up of the sensor protection tube area. Make sure that the protection tube is fully reaching into the exhaust gas stream.
* Installation angle should be aimed perpendicular (90°); at least it must be inclined 10° towards horizontal. Thus, the accumulation of condensate between sensor housing and sensing element is prevented. The tilt angle against the exhaust gas stream should be 90°, maximum inclination 90° - 30° (protection tube entry hole in direction of exhaust gas flow to avoid cooling of the sensing element). !!⚠A slope of the sensor axis towards the exhaust-gas flow is not allowed.

![LsuSensorInstallation1.PNG](Images/LsuSensorInstallation1.PNG)
![LsuSensorInstallation2.PNG](Images/LsuSensorInstallation2.PNG)
![LsuSensorInstallation3.PNG](Images/LsuSensorInstallation3.PNG)

* The sensor must not be exposed to strong mechanical shocks (e.g. while the sensor is installed). Otherwise the sensing element may crack without visible damage to the sensor housing. Avoid excessive heating up of sensor cable grommet, particularly when the engine has been switched off after running under max. load conditions.
* The sensor should not be exposed to continuous, one-sided dripping of water, e.g. by the air conditioning condensation water outlet. The thermal load could lead to mechanical damage of the sensor. Underfloor installation of the sensor at a distance from the engine requires an additional check of the following points: positioning of the sensor with respect to stone impact hazard and [ositioning and fixing of cable and connector with respect to mechanical damage and thermal load.
* The PTFE formed hose is part of the reference air volume of the sensor and must be kept sealed and undamaged. The first fixing point for the cable to the car body should be 200 mm to 400 mm after the end of the PTFE formed hose, depending on movement of the exhaust system. For installation, the minimum bending radius of the hose must be 20 mm (for long PTFE hose) resp. 12 mm (for short hose). Keep the PTFE forme hose away from sharp edges and avoid contact/friction with frame/engine assembly.


The above information and drawings are provided with the consent of Robert Bosch GmbH.

**Logging channels:

* __   **Lambda** __ - actual Lambda value 
* __  **Lambda is valid** __ - It indicates whether the sensor is functioning correctly and displaying accurate lambda values. In the case where the sensor is heating up or is damaged, the value of this channel is 'No'
* __   **AFR** __ - Air to fuel ratio for given Lambda and fuel type 
* __   **Lambda 2__** - actual Lambda value 2nd sensor (using external controller) 
* __   **AFR 2**  __ - Air to fuel ratio for given Lambda 2 and fuel type 
* __   **WBO IP ADC** __ - internal ADC value for IP measure
* __   **WBO RI** __  - the value of measurerd voltage of sensor RI 
* __   **WBO Heater DC** __  - the lambda sensor heater DC 
* __   **WBO VS** __  - the value of sensor VS
* __   **WBO IP Meas. ** __ - the value of normalized value of sensor IP
* __   **WBO sensor temperature** __ - the temperature of the sensor is estimated based on the Nernst cell resistance (Ri). The minimum displayed temperature is approximately 620°C. If the temperature is 0°C, it indicates that the sensor is not sufficiently heated or is malfunctioning.
* __   **WBO is calibrating** __  - during the calibration process this channel is equal to Yes


** Connection:

Below are the connection diagrams for LSU 4.9 and LSU 4.2 sensors to the EMU Black computer.

![lsu42.png](Images/lsu42.png)
![lsu49.png](Images/lsu49.png)

!!⚠If you are installing an LSU 4.9 sensor in an EMU BLACK device with a PCB revision below "O", a 150KOhm resistor must be installed between the WBO Vs signal and +5V. 
!!To check the main board revision, connect to the EMU device and then select the "About" option from the Help menu.

!!**⚠All devices with a USB-C or Micro USB port with a main board revision of "O" do not require this resistor.


![lsu49_resistor.PNG](Images/lsu49_resistor.PNG)




---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##WBO Lambda table

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Digital inputs

The digital inputs category allows for the configuration of device inputs that handle rapidly changing electrical signals from sensors, such as the crankshaft position sensor, camshaft position sensor, or vehicle speed sensor. The Engine Management Unit (EMU) has 4 inputs of this type, of which 3 are dedicated to the trigger system, handling signals from the crankshaft position sensor and camshaft position sensors, and one input dedicated to vehicle speed measurement. CAM#1 (secondary trigger), CAM#2, and VSS inputs can also be utilized as inputs for switches.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##Primary trigger

Primary trigger options are responsible for configuring the main sensor directing the ignition system and base ignition advance. The signal source (sensor) can be located on the crankshaft as well as on the camshaft. After each change of parameters, the ignition angle should be checked with a timing light.

!! **⚠ Proper configuration of the ignition system is essential for safe operation of the engine!

The device supports two types of sensors: VR sensors and Hall/Optical sensors. When using a VR sensor, it should be noted that it is sensitive to electromagnetic interference and, therefore, must be connected to the EMU device using shielded wires. It is also important to connect the screen to the ground on only one side of the wires. It is recommended to include a pulldown resistor to lower the input impedance.

For Hall/Optical sensors, they are typically of the open-drain or open-collector type, meaning they require the inclusion of a pullup resistor in the device. We recommend a value of 1K. In contrast to VR sensors, Hall sensors are much more resistant to interference and do not require the use of shielded wires. However, they do require power, which depending on the sensor type, can be either +5V or +12V.

In the case of the VR sensor, the input circuit adaptively adjusts sensitivity (from 50mV) to ensure the highest immunity of the input circuit to interference.

To check if the sensor is connected correctly, you can use the Scope function in the EMU.

**In case of issues with the VR sensor signal (e.g., trigger errors like unexpected missing tooth for patterns with a missing tooth) occurring at rotations below the expected RPM limit, one can try connecting in series with the sensor signal a resistor with a resistance of approximately 10K.

{#1} — Primary trigger parameter table (captured from the in-software help):

| Name | Description |
|---|---|
| **Sensor type** | VR sensor — select when your sensor is inductive. HALL sensor — select when your sensor is hall or optical. |
| **Adaptive threshold** | In the case of VR sensors it is possible to change the strength of the adaptive threshold. When the signal varies (e.g. a non-centric trigger wheel) changing this setting can help. |
| **Pullup/Pulldown** | For VR sensor we **strongly recommend 1K pulldown** (4K7 if there is no signal during cranking with 1K). For Hall sensor pullup 1K is advised. |
| **Input filter** | Enables low-pass filter. For the Hall sensor, we recommend not using any filter. For VR sensors, use the filter **only when there are signal noise issues**. The lower the filter setting, the better, as it introduces delay in the processed signal. |

**VR SENSOR

VR (Variable Reluctance) sensors utilize a coil wound around a permanent magnet to generate voltage as they pass by a ferrous target tooth. The induced voltage is directly proportional to the sensor's distance from the trigger wheel and its rotational speed. An important characteristic of VR sensors is their polarity. It is crucial to determine the polarity when connecting a VR sensor to the Engine Management Unit (EMU) so that the correct trigger edge can be selected. Signals from such sensors, particularly at low speeds, where their amplitude only reaches several hundred millivolts, are highly susceptible to interference. Consequently, they must always be connected using shielded cables. It is also important to note that the shield covering the cable should be grounded on only one side of the wire.

The scope trace of VR sensor signal 
![vrSensor.png](Images/vrSensor.png)

!! ** ⚠The VR sensors are very sensitive to noise. Due to this fact only shielded wire should be used to connect VR sensors and the shield should be connected to ground only at one end

Sample Wiring Diagram for Connecting a VR Sensor to the EMU Device (Primary Trigger). The polarity of the sensor signal is not critical (however the falling edge in the trigger configuration is preffered) because the trigger edge can be selected in the trigger input options. 

![ignition/vr_sensor_wiring.png](Images/ignition/vr_sensor_wiring.png)


**HALL SENSOR 

This sensor employs Hall's phenomenon to gauge the position and speed of a ferromagnetic trigger wheel. Unlike the variable reluctance sensor, it necessitates external power. Typically, these sensors feature "open collector" outputs and mandate the use of a pull-up resistor (with the Engine Management Unit or EMU, a 2K pull-up to +5V can be activated in the software menu by selecting the enable pull-up option). Hall sensors require a power supply in the range of 5-12V but exhibit greater immunity to interference when compared to magneto-inductive sensors. 

The scope trace of Hall sensor signal
![hallSensor.png](Images/hallSensor.png)


HALL and optical sensors require either +5V or +12V. Prior to installation, verify the sensor's power requirements, as supplying an incorrect voltage may result in sensor damage!
Here is a sample wiring diagram illustrating the connection of a Hall sensor to an Engine Management Unit (EMU) device. Both Hall and optical sensors typically feature open collector outputs and mandate a pull-up resistor (activate the pull-up option in the trigger input configuration).

![ignition/hall_sensor_wiring.png](Images/ignition/hall_sensor_wiring.png)








---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM 1

CAM options are responsible for configuring the engine phase sensor (CAM 1) as well sensors used for detecting camshafts position (VVTi).  Additionally, CAM 1 and CAM 2 inputs can be used as inputs for switches and CAM 2 input can be used as driven / nondriven axle speed source. 

!! **⚠Proper configuration of the ignition system is essential for safe operation of the engine!

The device supports two types of sensors: VR sensors and Hall/Optical sensors. When using a VE sensor, it should be noted that it is sensitive to electromagnetic interference and, therefore, must be connected to the EMU device using shielded wires. It is also important to connect the screen to the ground on only one side of the wires. It is recommended to include a pulldown resistor to lower the input impedance.

For Hall/Optical sensors, they are typically of the open-drain or open-collector type, meaning they require the inclusion of a pullup resistor in the device. We recommend a value of 1K. In contrast to VR sensors, Hall sensors are much more resistant to interference and do not require the use of shielded wires. However, they do require power, which depending on the sensor type, can be either +5V or +12V.

There is a possibility to check in the log whether the device reads the electrical waveform from the input (CAM signal present channels). In the case of using the CAM input as a "switch" channel, the CAM signal level indicates the current signal level at the input (low, high).

In the case of an inductive sensor, we have the option to choose a default reference voltage curve (where the signal changes from 0 to 1) at a level of 0.2V@0RPM to 2V@7000 and above. Alternatively, we can define such voltage based on rotational functions (the higher the rotational speed, the higher the voltage from the sensor) using the 2D CAM sensitivity table.

{#1}

**VR SENSOR

VR (Variable Reluctance) sensors utilize a coil wound around a permanent magnet to generate voltage as they pass by a ferrous target tooth. The induced voltage is directly proportional to the sensor's distance from the trigger wheel and its rotational speed. An important characteristic of VR sensors is their polarity. It is crucial to determine the polarity when connecting a VR sensor to the Engine Management Unit (EMU) so that the correct trigger edge can be selected. Signals from such sensors, particularly at low speeds, where their amplitude only reaches several hundred millivolts, are highly susceptible to interference. Consequently, they must always be connected using shielded cables. It is also important to note that the shield covering the cable should be grounded on only one side of the wire.

The scope trace of VR sensor signal 
![vrSensor.png](Images/vrSensor.png)

!! ** ⚠The VR sensors are very sensitive to noise. Due to this fact only shielded wire should be used to connect VR sensors and the shield should be connected to ground only at one end

Sample Wiring Diagram for Connecting a VR Sensor to the EMU Device (Primary Trigger). The polarity of the sensor signal is not critical (however the falling edge in the trigger configuration is preffered) because the trigger edge can be selected in the trigger input options. 

![ignition/vr_sensor_wiring.png](Images/ignition/vr_sensor_wiring.png)


**HALL SENSOR 

This sensor employs Hall's phenomenon to gauge the position and speed of a ferromagnetic trigger wheel. Unlike the variable reluctance sensor, it necessitates external power. Typically, these sensors feature "open collector" outputs and mandate the use of a pull-up resistor (with the Engine Management Unit or EMU, a 2K pull-up to +5V can be activated in the software menu by selecting the enable pull-up option). Hall sensors require a power supply in the range of 5-12V but exhibit greater immunity to interference when compared to magneto-inductive sensors. 

The scope trace of Hall sensor signal
![hallSensor.png](Images/hallSensor.png)


HALL and optical sensors require either +5V or +12V. Prior to installation, verify the sensor's power requirements, as supplying an incorrect voltage may result in sensor damage!
Here is a sample wiring diagram illustrating the connection of a Hall sensor to an Engine Management Unit (EMU) device. Both Hall and optical sensors typically feature open collector outputs and mandate a pull-up resistor (activate the pull-up option in the trigger input configuration).

![ignition/hall_sensor_wiring.png](Images/ignition/hall_sensor_wiring.png)


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##VSS

The VSS (Vehicle Speed Sensor) input configuration allows you to define the type of sensor connected to the VSS input of the device as a speed sensor. The VSS input can also be utilized as an input for a switch.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM sensitivity

The CAM sensitivity table defines the reference voltage for an inductive sensor connected to the CAM input when selecting the__ ** VR sensor sensitivity table type.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##TPS, PPS

The **TPS** and **PPS** configuration is used to define the correct position of the throttle position sensor (__TPS__) and the accelerator pedal position (__PPS__). In the case of a vehicle with a mechanical throttle, the throttle position is identical to the accelerator pedal position, and only the TPS is configured. In the case of an electronic throttle, both the TPS and PPS need to be configured separately. In such applications, the throttle position and accelerator pedal position sensors have a secondary measurement system (__check__), which allows the detection of irregularities in the operation of the primary (__main__) sensors. For safety reasons, it is recommended to connect and properly configure the check sensors.

To activate the error-checking function between the __main sensor__ and the __check sensor__, it is necessary to assign an analog input for the __check sensor__ in the __TPS/PPS__ configuration. Next, a 2D check tolerance table should be defined. In this table, for a given position of the __main sensor__ (in %), the expected voltage from the __check sensor__ is specified. If this voltage differs from the actual voltage by more than the value specified in the __error tolerance paramete__, the ECU will detect an error and deactivate the throttle power supply.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##TPS

TPS sensor calibration is necessary to ensure accurate readings and proper functioning of the throttle position sensor, whether it is used in a mechanical or electronic throttle system. 

{#1}

For the TPS sensor, 2D check tolerance table is defined. For given throttle position (main TPS) values, you need to define the check sensor voltage values. These voltages should be read from the log.

** !!Note: In case of any TPS sensor error, the electronic throttle strategy enters a fail-safe mode, cutting off power to the throttle motor, which should result in setting it to the limp mode position.

**Logging channels:

* __**TPS**__ - Current throttle position (0-100%)
* __**TPS voltage**__ - Analog input voltage defined for the TPS sensor
* __**TPS check error**__ - Error between the expected and actual voltage of the check sensor
* __**TPS main status**__ - Status of the main TPS sensor
* __**TPS check status**__ - Status of the TPS check sensor
* __**TPS rate__** - refers to the rate of change of the throttle position in percentage per second (%/s). During the opening of the throttle, this parameter takes positive values, while during closure, it takes negative values.


**Meaning of TPS statuses:

* __**OK**__ - Sensor is functioning correctly
* __**Unassigned**__ - Sensor is not assigned
* __**Short to ground**__ - Voltage from the sensor is below the valid voltage min or missing +5V.
* __**Short to 5V**__ - Voltage from the sensor is above the valid voltage max or missing sensor ground.
* __**Check error**__ - The error between the expected and actual voltage of the check sensor is greater than the error tolerance.



---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##PPS

The accelerator pedal position sensor is utilized when an electronic throttle is employed. Its purpose is to communicate the expected position of the electronic throttle to the ECU. In the case of engines with a mechanical throttle, the value of the accelerator pedal position sensor (PPS) is always equal to the throttle position sensor (TPS) value, and no configuration adjustments are made in the PPS configuration.

{#1}

**Logging channels:

* __**PPS**__ - Current throttle position (0-100%)
* __**PPS voltage**__ - Analog input voltage defined for the TPS sensor
* __**PPS check error**__ - Error between the expected and actual voltage of the check sensor
* __**PPS main status**__ - Status of the main TPS sensor
* __**PPS check status**__ - Status of the TPS check sensor


**Meaning of PPS statuses:

* __**OK**__ - Sensor is functioning correctly
* __**Unassigned**__ - Sensor is not assigned
* __**Short to ground**__ - Voltage from the sensor is below the valid voltage min
* __**Short to 5V**__ - Voltage from the sensor is above the valid voltage max
* __**Check error**__ - The error between the expected and actual voltage of the check sensor is greater than the error tolerance.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##PPS check tolerance

A table defining the expected voltage from the __check sensor__ for a given pedal position expressed in %.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##TPS check tolerance

A table defining the expected voltage from the __check sensor__ for a given throttle position expressed in %.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Rotary switches

Each group contains specific information related to its respective area


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Rotaryswitches) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##IAT, CLT

The Intake Air Temperature (IAT) sensor and the Coolant Temperature (CLT) sensor are crucial sensors utilized by the Engine Control Unit (ECU). Based on the intake air temperature, the computer adjusts the fuel injection rate. The coolant temperature is used to determine the enrichment of the mixture in the case of a cold engine and to control the radiator fans.

** !!⚠Both sensors must be connected to the EMU and properly configured for the device to operate correctly!

The EMU Black device has a built-in 2K2 pull-up resistor on the IAT and CLT sensor inputs, which, along with the variable resistance of the sensor, forms a voltage divider. In rare cases where the internal pull-up resistor may not be optimal for the specific sensor used, there is an option to disable the internal pull-up (__{1}__) and use an external resistor instead.

The diagram below illustrate the method of connecting IAT and CLT sensors to the EMU device.

![iatClt.png](Images/iatClt.png)




---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/IATCLT) 
##IAT calibration

The IAT calibration table defines the sensor temperature based on the input voltage. It is recommended to use the IAT sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/IATCLT) 
##CLT calibration

The CLT calibration table defines the sensor temperature based on the input voltage. It is recommended to use the CLT sensor wizard to populate this table.



---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##MAP, BARO

The Manifold Absolute Pressure (__**MAP__**) sensor is a fundamental sensor in the Speed Density algorithm, used to calculate the fuel dosage. It also enables boost control. The EMU is equipped with a built-in MAP sensor with a measurement range of 400 kPa.

In situations where the installation location of the EMU makes it challenging to connect the hose to the intake manifold pressure, or if a sensor with a different measurement range is preferred, it can be connected to any analog input of the device. The hose length between the device and the intake manifold should be kept as short as possible, and the hose should be rigid.

The Barometric Pressure (__**Baro**__) sensor is mainly used in vehicles employing the Alpha-N fuel dosage strategy. It allows for fuel dosage compensation with changes in atmospheric pressure, which correlates with changes in air density.

The device does not have an internal Baro sensor. However, in Alpha-N strategies, an internal pressure sensor can be utilized.

The scheme below illustrates the way of connecting an external MAP sensor to the EMU. The external BARO sensor is connected in the same manner.
![map.png](Images/map.png)


**Logging channels:

* __   **MAP** __ - actual MAP value 
* __   **MAP status** __ - actual MAP sensor status
* __   **MAP rate** __ - rate of change of MAP sensor. Can be used for acceleration enrichment
* __   **BARO** __ - actual BARO value 


**Meaning of MAP and BARO statuses:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input






---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/MAPBARO) 
##Parameters

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/MAPBARO) 
##BARO calibration

In the case of connecting an external BARO sensor, this table defines the relationship between pressure in kPa and the voltage from the analog input.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/MAPBARO) 
##MAP calibration

In the case of connecting an external MAP sensor, this table defines the relationship between pressure in kPa and the voltage from the analog input.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Pressure

The device allows for the configuration of a wide range of pressure sensors that may be present in a race car. To simplify the sensor configuration, a wizard can be utilized to generate appropriate calibration tables. Additionally, there are many popular sensors available in the list for easy selection.

In the Parameters options, sensors can be activated by assigning analog inputs to which they are connected and defining failsafe values. These failsafe values will be used if the sensor voltage is lower than 0.1V or higher than 0.9V.

For each sensor, a logging channel is created, along with its status channel containing information about whether the sensor is operating correctly or the cause of its malfunction.

Pressure sensors are, in most cases, voltage-based sensors (and only such sensors can be utilized here). They should be powered according to the manufacturer's guidelines, typically with +5V, and their outputs connected to available analog inputs.


**Logging channels:

* __   **Engine oil pressure** __ - actual egnine oil pressure value 
* __   **Engine oil pressure status** __ - actual engine oil sensor status
* __   **Fuel pressure** __ - actual fuel pressure value 
* __   **Fuel pressure status** __ - actual fuel pressure sensor status
* __   **Back pressure** __ - actual back pressure value 
* __   **Back pressure status** __ - actual back pressure sensor status
* __   **Differentail oil pressure** __ - actual differential oil pressure value 
* __   **Differentail oil pressure status** __ - differential oil pressure sensor status
* __   **Coolant pressure** __ - actual coolant pressure value 
* __   **Coolant  pressure status** __ - actual coolant pressue sensor status
* __   **Crankcase pressure** __ - actual crankcase pressure value 
* __   **Crankcase pressure status** __ - actual MAP sensor status
* __   **AC  pressure** __ - actual airconditioning pressure value 
* __   **AC pressure status** __ - actual airconditioning sensor status
* __   **Pre throttle boost pressure** __ - actual boost pressure from the pre throttle installed sensor 
* __   **Pre throttle boost sensor status** __ - pre throttle boost sensor status
* __   **Wastegate dome pressure**__ -  wastegate dome pressure for the wastgate installed sensor
* __   **Wastegate dome pressure sensor status** __ - wastegate dome pressure sensor status


**Meaning of statuses:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input
* __   **CAN-BUS** __ -  the sensor value is overridden by user-defined CAN stream

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Parameters

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##AC pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Back pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Coolant pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Crankcase pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Diff. pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Fuel pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Oil pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Temperature

The device allows for the configuration of a wide range of pressure sensors that may be present in a race car. To simplify the sensor configuration, a wizard can be utilized to generate appropriate calibration tables. Additionally, there are many popular sensors available in the list for easy selection.

In the Parameters options, sensors can be activated by assigning analog inputs to which they are connected and defining failsafe values. These failsafe values will be used if the sensor voltage is lower than 0.1V or higher than 0.9V.

The temperature sensors in EMU can be divided into two groups. The first group consists of sensors that have their own calibration tables (e.g., Engine oil temp cal., Fuel temp. cal., etc.) and are named Standard sensors. The second group includes Custom sensors, which have only 4 calibration tables, limiting the choice to 4 sensors from this group. All temperature sensors have their logging channels and status channels.

In the case of temperature sensors that are resistive sensors (NTC, PTC), a pull-up resistor to +5V is required, which will form a voltage divider with the sensor. For analog inputs, a 4700-ohm resistor can be activated  in analog inputs configuration  (__{1}__). If it isn't an optimal value for a specific sensor, an external pull-up resistor to +5V with the appropriate resistance should be used.




---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##AC evap temp cal.

The calibration table defines the sensor temperature based on the input voltage. It is recommended to use the temperature sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Diff. oil temp cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Fuel temp cal.

The calibration table defines the sensor temperature based on the input voltage. It is recommended to use the temperature sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Gearbox oil temp cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Pre IC air temp cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Power steer. temp cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Oil temp. cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Other sensors

Sensors in the __Other sensors__ category are sensors that could not be assigned to the pressure or temperature categories.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Othersensors) 
##Parameters

The fuel level sensor requires special filtering due to the fact that its level in the tank can change rapidly while the vehicle is in motion on the road.

The fuel level filtering strategy reads its level at regular intervals (fuel level filter rate) and then adjusts the current reading by a maximum of 0.25% if it differs from the current level. In case the engine is not running, the fuel level takes the value from the calibration table without any filtering.

Fuel level sensors are most commonly resistive sensors and require a low-resistance pull-up (100-200 Ohms).

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Othersensors) 
##Fuel level cal.

Table defining the relationship between the fuel level and voltage from the sensor at the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##VSS and Gearbox

Available vehicle speeds can be divided into:

1. {1}
2. {2}
3. {3}
4. {4}

__Vehicle speed__ is the most important source of speed used by most strategies. 
__Driven axle__ and __Non-driven__ axle speeds are used in traction control strategy.

__Wheels speed__ allows reading the speeds of individual wheels from the CAN bus.

Depending on the vehicle and requirements, you can configure only __Vehicle speed__ or all speeds.

In the case of detecting the current gear, it is possible to read from an analog gear position sensor or calculate the gear based on the ratio of vehicle speed to engine speed.

!!**⚠When using User Defined CAN, the following is the format of the channels describing speeds:

* **__Wheel speeds**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__GPS speed**__ - 2 km/h per bit, e.g., 100 = 200 km/h.
* **__Driven speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__Undriven speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__Vehicle speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.



**Logging channels:

* **__Vehicle speed**__ – Estimated vehicle speed based on selected speed source (e.g., driven axle, GPS, etc.).
* __**Gear**__ – current calculated gear .
* __**Driven axle speed**__ – rotational speed of the driven axle (in RPM), derived from the input frequency.
* __**Undriven axle speed**__ – rotational speed of the undriven axle (in RPM), derived from the input frequency.
* __**Wheel speed FL / FR / RL / RR**__ – individual wheel speeds: Front Left, Front Right, Rear Left, and Rear Right (typically read via CAN from ABS or traction control system).
* __**GPS speed**__ – vehicle speed calculated from the GPS module data.
* __**Driven axle input frequency**__ – Raw frequency signal from the driven axle speed sensor.
* __**Undriven axle input frequency**__ – Raw frequency signal from the undriven axle speed sensor.
* __**Gear speed to RPM ratio**__ – calculated ratio between vehicle speed and engine RPM, used for gear estimation. Can be dirietly used to fill the {5} speed to RPM ratios.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gearbox

EMU Black can detect the current gear using three strategies:

1. Reading the voltage from the gearbox's current gear sensor.
2. Calculating the gear based on the ratio of vehicle speed to engine speed.
3. Reading the gearbox from the DSG gearbox. 

In the first case, you should check the voltage range for each gear on the analog input to which the sensor is connected and then enter them into the __Gear-in lower voltage__ and __Gear-in upper voltage__ tables. A value of -1 in the table indicates reverse gear.

For the method of calculating the gear, you should perform a test drive in each gear and read the ratio for each gear from the log (channel __Gear speed to RPM ratio__), and then enter these values for the parameters of individual gears.

It is worth emphasizing that when the clutch is pressed, there is no possibility of correctly calculating the current gear. In such a case, we recommend connecting the clutch pedal sensor to EMU, and its state will be taken into account in the calculations.


**The gear ratio formula:
__Gear ratio = (16 x Vehicle speed) / RPM

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Vehicle speed

Vehicle speed configuration is used to define the method by which the vehicle speed  (VSS) is calculated. It also enables the introduction of speed correction (Speed ratio) and signal filtering.

{#1}



---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Wheels setup

Wheel setup configuration defines how the speed of individual wheels is calculated. Since EMU BLACK lacks an adequate number of digital inputs for reading speed from four wheel speed sensors, the only option for configuring wheel speeds is through the CAN BUS streams.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Driven axle

The driven axle configuration allows for the setup of the speed source for the driven axle. In the case of traction control, the speed difference between the driven and non-driven axles is taken into account. 

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Non-driven axle

The driven axle configuration allows for the setup of the speed source for the driven axle. In the case of traction control, the speed difference between the driven and non-driven axles is taken into account. If you do not plan to use traction control, the non-driven axle does not need to be configured.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear sensor. cal.

The __Gear sensor calibration__ table defines the voltage from the gear position sensor for each specific gear. The number of gears is defined in the Gearbox parameters. The strategy for calculating the gear based on the gear position sensor selects the gear whose defined voltage is closest to the voltage from the sensor.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Vss and gears

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) 
##Switches

 Switches enable the activation of strategies and control of their parameters. The user has the following switch categories to choose from:

* Built-in Switches
* User switches
* Latching switch
* Rotary switches
* MUX switch
* Clutch, brake switch


**Built-in switches:
These are switches directly integrated into the EMU BLACK device. They are buttons controlled by ground. In the hardware revision P or newer, each input operates independently, and positive voltage can be applied to them (although they activate on ground). In the case of older versions, only ground (sensor ground) can be applied to their input; otherwise, the measurement from other inputs may be disturbed. The device has 3 switch-type inputs.

**User Switches:
User switches are defined by the user, and their input signal sources can be analog inputs, CAN analog inputs, and digital inputs such as CAM 1, CAM 2, VSS Input. The user can define up to 8 user switches.

**Latching Switch:
A latching switch has up to 4 positions that can be cyclically changed using an external button. The device allows the management of 4 latching switches that can be controlled via the CAN keypad. The user can define parameters for 1 latching switch using the device's inputs.

**Rotary Switches:
Rotary switches are a type of rotary switch that can have up to 10 positions. The main signal sources for rotary switches are analog inputs and CAN analog inputs. Latching switches can also serve as inputs (then the maximum number of positions for the rotary switch is 4), as well as regular switches and user switches (then the maximum number of positions for the rotary switch is 2). Rotary switches are used wherever the user can change strategy parameters in real-time (e.g., RPM in Launch Control or traction control sensitivity). There are 5 rotary switches defined in the device and 4 rotary switches set via the CAN bus.

**MUX Switch:
MUX switch allows the use of an analog input or CAN analog input to connect 3 switches controlled by ground.

**Clutch, Brake Switch:
This is a separate switch category related to crucial pedals used by safety-related strategies (e.g., stucked throttle protection, cruise control, DSG support, etc.). These switches can be controlled either by EMU inputs or via the CAN bus.

**Rx  Switch:
Unlike other inputs, the **Rx switch** is activated by a high state (+5V or +12V). It uses the RS232 Rx input. Normally, it stays low (0V), and switches to a high state when connected to 5V or 12V




---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##User switches

The user switch is a switch defined by the user utilizing analog inputs, CAN analog inputs, as well as CAM 1 input, CAM 2 input, and Vss input. In the case of analog inputs, it is typical to use switches connected to ground. In such a case, it is necessary to activate the internal pull-up of the EMU in the Analog Inputs configuration.

For CAM 1, CAM 2, and Vss inputs, in the Digital Input configuration, the Sensor type should be selected as HALL, and the pull-up should be activated.

The **__Flex fuel**__ input has a built-in 10k pull-up resistor permanently connected to +5V. The value of the **__FF input state**__ channel is 1 when the circuit is open and 0 when the input is grounded. Therefore, the **__Invert switch**__ option must be selected.

Below are examples of how switches can be connected to an analog input and the VSS input or Flex Fuel input:

**Analog Input Connection (typical switch to ground):
* Connect one side of the switch to the analog input.
* Connect the other side of the switch to the ground.
* Ensure that the internal pull-up of the EMU is activated in the Analog Inputs configuration.


**VSS Input Connection (HALL sensor type with pull-up):
* Connect the switch to the VSS input.
* Configure the VSS input in the Digital Inputs settings:
* Select Sensor type as HALL.
* Activate the pull-up.


The diagram below illustrates how the switches should be connected

![switchToGnd.png](Images/switchToGnd.png) 
![switchInput.png](Images/switchInput.png) 
![switchOnCam.png](Images/switchOnCam.png)

{#1}

**Logging channels:

* __ ** User swtich 1 __ **  - the state of User switch 1
* __ ** User swtich 2 __ ** - the state of User switch 2
* __ ** User swtich 3 __ ** - the state of User switch 3
* __ ** User swtich 4 __ ** - the state of User switch 4
* __ ** User swtich 5 __ ** - the state of User switch 5
* __ ** User swtich 6 __ ** - the state of User switch 6
* __ ** User swtich 7 __ ** - the state of User switch 7
* __ ** User swtich 8 __ ** - the state of User switch 8

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##MUX Switch

The MUX switch strategy allows for connecting 3 ground-controlled switches to a single analog input. It is crucial that these switches are activated using sensor ground.

The diagram below illustrates how the switches should be connected to the resistor voltage divider. We recommend using resistors with a tolerance of 1%.

![muxSwitch.png](Images/muxSwitch.png)


{#1}
**Logging channels:

* __** Mux switch voltage raw __** - the raw voltage of mux switch analog input
* __** Mux switch 1 __** - the state of Mux switch 1
* __** Mux switch 2 __** - the state of Mux switch 2
* __** Mux switch 3 __** - the state of Mux switch 3


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##Momentary switch

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##Rotary switches

Rotary switches are a type of rotary switch that can have up to 10 positions. The main signal sources for rotary switches are analog inputs and CAN analog inputs. 

Latching switches can also serve as inputs (then the maximum number of positions for the rotary switch is 4), as well as regular switches and user switches (then the maximum number of positions for the rotary switch is 2). 

Rotary switches are used wherever the user can change strategy parameters in real-time (e.g., RPM in Launch Control or traction control sensitivity). 

There are 5 rotary switches defined in the device and 4 rotary switches set via the CAN bus.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) [Auto](help://Sensorsandinputs/Switches/Rotaryswitches) 
##Parameters

The rotary switch utilizes a multi-position rotary selector connected to a voltage divider and linked to the analog input of the EMU. Each unique position of the selector should have a distinct voltage, which we define in tables specific to each rotary switch.

When assigned as the input for a switch (On/Off) or a 4-state latching switch, the values for the rotary switch correspond to 0 and 1, or 0, 1, 2, 3 respectively.

In addition to the 5 rotary switches, it is possible to utilize an extra 4 CAN rotary switches, whose values can be set through the CAN bus.

{#1}

**Logging channels:

* __ ** Rotary switch 1 __ ** - the current position of the rotary switch
* __ ** Rotary switch 2 __ ** - the current position of the rotary switch
* __ ** Rotary switch 3 __ ** - the current position of the rotary switch
* __ ** Rotary switch 4 __ ** - the current position of the rotary switch
* __ ** Rotary switch 5 __ ** - the current position of the rotary switch
* __ ** Rotary switch CAN 1 __ ** - the current position of the rotary switch
* __ ** Rotary switch CAN 2 __ ** - the current position of the rotary switch
* __ ** Rotary switch CAN 3 __ ** - the current position of the rotary switch
* __ ** Rotary switch CAN 4 __ ** - the current position of the rotary switch





---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) [Auto](help://Sensorsandinputs/Switches/Rotaryswitches) 
##Rotary switch cal.

Table defining unique voltages for each position of the rotary switch. In cases where the rotary switch input is not an analog input, calibration tables are not utilized.



---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/OxygenSensor) 
##Parameters

The oxygen sensor configuration options allow the configuration of an external sensor/controller connected to the EMU device.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/OxygenSensor) 
##Oxygen Sensor PID

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/OxygenSensor) 
##WBO Lambda table

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/IATCLT) 
##Failsafe

In case of sensor issues (voltage at the device input less than 0.1V or greater than 4.9V), a failsafe value is adopted for the sensor to ensure continued engine operation.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/IATCLT) 
##IAT sensor wizard

The temperature sensor wizard is a tool designed to generate calibration tables for a given sensor. The applied algorithm allows generating an optimal calibration table from three known resistance/temperature points (the values defining the X-axis are optimized to minimize the quantization error of the sensor voltage to the 2D table).

The tool includes a set of predefined popular sensors. After selecting a sensor, resistance and temperature values are automatically populated. In the case of using an external pull-up resistor, its value can be entered in the Rx value field (2200 ohms by default).

If the used sensor is not on the list, you should enter 3 resistance values along with their corresponding temperatures. The greater the difference between the temperature values, the better the approximation of the sensor characteristic curve. If the entered data is incorrect and does not match the sensor's characteristics, the tool will be unable to generate a calibration table.

![iatWizard.png](Images/iatWizard.png)

After accepting the selected parameters, a window will appear where you can define the range of temperatures and voltages within which you want to generate the calibration map. In the case of a poorly chosen pull-up resistor for the sensor characteristic, it may turn out that the full expected temperature range cannot be achieved within the 0-5V range. In such a situation, you should calculate the correct pull-up resistor or, by adjusting the pull-up resistance Rx in the wizard, select a value that allows obtaining the full range of temperatures of interest.

![iatWizard2ndScreen.png](Images/iatWizard2ndScreen.png)

The image below shows an example calibration table for a Bosch 0280130039 sensor.

![iatCalibration.png](Images/iatCalibration.png)

!!**It should be emphasized that the IAT sensor wizard only generates the table and does not store any information about the selected temperature sensor. As a result, each time the wizard is run, the desired sensor must be selected again.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/IATCLT) 
##CLT sensor wizard

The temperature sensor wizard is a tool designed to generate calibration tables for a given sensor. The applied algorithm allows generating an optimal calibration table from three known resistance/temperature points (the values defining the X-axis are optimized to minimize the quantization error of the sensor voltage to the 2D table).

The tool includes a set of predefined popular sensors. After selecting a sensor, resistance and temperature values are automatically populated. In the case of using an external pull-up resistor, its value can be entered in the Rx value field (2200 ohms by default).

If the used sensor is not on the list, you should enter 3 resistance values along with their corresponding temperatures. The greater the difference between the temperature values, the better the approximation of the sensor characteristic curve. If the entered data is incorrect and does not match the sensor's characteristics, the tool will be unable to generate a calibration table.

![iatWizard.png](Images/iatWizard.png)

 After accepting the selected parameters, a window will appear where you can define the range of temperatures and voltages within which you want to generate the calibration map. In the case of a poorly chosen pull-up resistor for the sensor characteristic, it may turn out that the full expected temperature range cannot be achieved within the 0-5V range. In such a situation, you should calculate the correct pull-up resistor or, by adjusting the pull-up resistance Rx in the wizard, select a value that allows obtaining the full range of temperatures of interest.

![iatWizard2ndScreen.png](Images/iatWizard2ndScreen.png)

The image below shows an example calibration table for a Bosch 0280130039 sensor.

![iatCalibration.png](Images/iatCalibration.png)


!!**It should be emphasized that the CLT sensor wizard only generates the table and does not store any information about the selected temperature sensor. As a result, each time the wizard is run, the desired sensor must be selected again.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Sensor wizard

The pressure sensor wizard is a tool that facilitates the generation of calibration characteristics for pressure sensors. The tool includes a set of predefined popular sensors and also allows the input of two voltage-pressure pairs, based on which it generates and saves the calibration in the appropriate table (xxxx pressure cal.).

![pressureSensorWizard.png](Images/pressureSensorWizard.png)

To select a predefined sensor, choose it from the Predefined sensor list, and in the Sensor cal. table option, select the table for which you want to generate the calibration. If the sensor is not on the list, provide two voltages and their corresponding pressures in bars. After pressing the OK button, the table will be generated.


!!**⚠It should be emphasized that the Pressure sensor wizard only generates the table and does not store any information about the selected pressure  sensor. As a result, each time the wizard is run, the desired sensor must be selected again.





---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Sensor wizard

The temperature sensor wizard is a tool designed to generate calibration tables for a given sensor. The applied algorithm allows generating an optimal calibration table from three known resistance/temperature points (the values defining the X-axis are optimized to minimize the quantization error of the sensor voltage to the 2D table).

The tool includes a set of predefined popular sensors. After selecting a sensor, resistance and temperature values are automatically populated. In the case of using an external pull-up resistor, its value can be entered in the Rx value field (2200 ohms by default).

If the used sensor is not on the list, you should enter 3 resistance values along with their corresponding temperatures. The greater the difference between the temperature values, the better the approximation of the sensor characteristic curve. If the entered data is incorrect and does not match the sensor's characteristics, the tool will be unable to generate a calibration table.

To choose the calibration table for which data is to be generated, select it in the __Sensor cal. table__ field.

![tempsensorwizard.png](Images/tempsensorwizard.png)

After accepting the selected parameters, a window will appear where you can define the range of temperatures and voltages within which you want to generate the calibration map. In the case of a poorly chosen pull-up resistor for the sensor characteristic, it may turn out that the full expected temperature range cannot be achieved within the 0-5V range. In such a situation, you should calculate the correct pull-up resistor or, by adjusting the pull-up resistance Rx in the wizard, select a value that allows obtaining the full range of temperatures of interest.

![iatWizard2ndScreen.png](Images/iatWizard2ndScreen.png)



---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Cylinder head temp. cal.

The calibration table defines the sensor temperature based on the input voltage. It is recommended to use the temperature sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Standard sensors

Standard sensors have their own calibration tables.

**Logging channels:

* __   **Engine oil temperature** __ - actual engine oil temperature value 
* __   **Engine oil temp. status** __ - actual engine oil temperature sensor status
* __   **Fuel temperature** __ - actual fuel temperature value 
* __   **Fuel temperature status** __ - actual fuel temperature sensor status 
* __   **AC EVAP temperature** __ - actual AC evaporator temperature value 
* __   **AC  EVAP status** __ - actual AC evaporator temperature sensor status
* __   **Cylinder head temp. 1** __ - actual cylinder head temperature 1 value 
* __   **Cylinder head temp. 1 status** __ - actual cylinder head temperature sensor 1 status
* __   **Cylinder head temp. 2** __ - actual cylinder head temperature 2 value 
* __   **Cylinder head temp. 2 status** __ - actual cylinder head temperature sensor 2 status


**Meaning of statuses:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input
* __   **CAN-BUS** __ -  the sensor value is overridden by user-defined CAN stream


{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Custom sensors

Custom sensors have 4 calibration tables that can be assigned to specific sensor types.

**Logging channels:

* __   **Ambient temperature** __ - actual ambinet temperature value 
* __   **Ambient  temp. status** __ - actual mbinet temperature sensor status
* __   **Pre IC  temperature** __ - actual pre intercooler  temperature value 
* __   **Pre IC temp. status** __ - actual pre intercooler temperature sensor status 
* __   **Post IC temperature** __ - actual post intercooler temperature value 
* __   **Post IC temp. status** __ - actual post intercooler temperature sensor status
* __   **Power steering temperature** __ - actual power steering  temperature value 
* __   **Power steering fluid temp. status** __ - actual power steering temperature sensor status
* __   **Differential oil temperature** __ - actual differential oil temperature value 
* __   **Diffteerential oil temp. status** __ - actual differential oil temperature status
* __   **Brake fluid temperature** __ - actual brake fluid temperature value 
* __   **Brake fluid temp. status** __ - actual brake fluid temperature status
* __   **Gearbox oil temperature ** __ - actual gearbox oil temperature 
* __   **Gearbox oil temp. status** __ - actual gearbox oil temperature status


**Meaning of statuses:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input
* __   **CAN-BUS** __ -  the sensor value is overridden by user-defined CAN stream


{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Custom temp. cal

The calibration table defines the sensor temperature based on the input voltage. It is recommended to use the temperature sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Engine oil temp. cal.

The calibration table defines the sensor temperature based on the input voltage. It is recommended to use the temperature sensor wizard to populate this table.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##Clutch, brake

Brake and clutch switches are  used by safety-related strategies (e.g., stucked throttle protection, cruise control, DSG support, etc.). These switches can be controlled either by EMU inputs or via the CAN bus.

{#1}
**Logging channels:

* __** Brake pedal switch **__ - the state of the brake pedal
* __** Clutch pedal switch**__ - the state of the clutch pedal

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##Latching switch

Latching switches are switches that can assume up to 3 states (LSW_A, LSW_B, LSW_C). The state change occurs when the defined input changes from 1 to 0.

For example, if we define the input as Switch 1, pressing the button connected to the Switch 1 input will set its state to 1 (ON), releasing it will set the state to 0 (OFF), and the Latching switch will change its state from LSW_A to LSW_D.

You can define Latching switch 1 that uses switch inputs. Additionally, by utilizing the CAN keypad function, you can use Latching switches from 1 to 4.

Latching switches can be employed to activate functions or used in Rotary switch functions to obtain 3 different values.

{#1}
**Logging channels:

* __** Latching SW 1__**  - the state of latching switch 1 (LLSW_A, LSW_B, LSW_C, LSW_D)
* __** Latching SW 2__**  - the state of latching switch 2 (LSW_A, LSW_B, LSW_C, LSW_D)
* __** Latching SW 3__**  - the state of latching switch 3 (LSW_A, LSW_B, LSW_C, LSW_D) 
* __** Latching SW 4__**  - the state of latching switch 4 (LSW_A, LSW_B, LSW_C, LSW_D)


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##Built-in switches

EMU Black has 3 built-in switches available on terminals 10, 23, and 36 of the black plug. These inputs are controlled by switching to ground. In the hardware revision "P" (you can check hardware revision in about window) or newer, each input operates independently, and positive voltage can be applied to them (although they activate when switched to  ground). In the case of older versions, only sensor ground can be applied to their input; otherwise, the measurement from other inputs may be disturbed. The device has 3 switch-type inputs.

Example of switch connection:

![switchInput.png](Images/switchInput.png)

{#1}
**Logging channels:

* __ ** Switch 1__ ** - the state of the Switch 1 
* __ ** Switch 2__ ** - the state of the Switch 2
* __ ** Switch 3__ ** - the state of the Switch 3

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM 2

CAM options are responsible for configuring the engine phase sensor (CAM 1) as well sensors used for detecting camshafts position (VVTi).  Additionally, CAM 1 and CAM 2 inputs can be used as inputs for switches and CAM 2 input can be used as driven / nondriven axle speed source. 

!! **Proper configuration of the ignition system is essential for safe operation of the engine!

The device supports two types of sensors: VR sensors and Hall/Optical sensors. When using a VE sensor, it should be noted that it is sensitive to electromagnetic interference and, therefore, must be connected to the EMU device using shielded wires. It is also important to connect the screen to the ground on only one side of the wires. It is recommended to include a pulldown resistor to lower the input impedance.

For Hall/Optical sensors, they are typically of the open-drain or open-collector type, meaning they require the inclusion of a pullup resistor in the device. We recommend a value of 1K. In contrast to VR sensors, Hall sensors are much more resistant to interference and do not require the use of shielded wires. However, they do require power, which depending on the sensor type, can be either +5V or +12V.

There is a possibility to check in the log whether the device reads the electrical waveform from the input (CAM signal present channels). In the case of using the CAM input as a "switch" channel, the CAM signal level indicates the current signal level at the input (low, high).

In the case of an inductive sensor, we have the option to choose a default reference voltage curve (where the signal changes from 0 to 1) at a level of 0.2V@0RPM to 2V@7000 and above. Alternatively, we can define such voltage based on rotational functions (the higher the rotational speed, the higher the voltage from the sensor) using the 2D CAM sensitivity table.

{#1}

**VR SENSOR

VR (Variable Reluctance) sensors utilize a coil wound around a permanent magnet to generate voltage as they pass by a ferrous target tooth. The induced voltage is directly proportional to the sensor's distance from the trigger wheel and its rotational speed. An important characteristic of VR sensors is their polarity. It is crucial to determine the polarity when connecting a VR sensor to the Engine Management Unit (EMU) so that the correct trigger edge can be selected. Signals from such sensors, particularly at low speeds, where their amplitude only reaches several hundred millivolts, are highly susceptible to interference. Consequently, they must always be connected using shielded cables. It is also important to note that the shield covering the cable should be grounded on only one side of the wire.

The scope trace of VR sensor signal 
![vrSensor.png](Images/vrSensor.png)

!! ** The VR sensors are very sensitive to noise. Due to this fact only shielded wire should be used to connect VR sensors and the shield should be connected to ground only at one end

Sample Wiring Diagram for Connecting a VR Sensor to the EMU Device (Primary Trigger). The polarity of the sensor signal is not critical (however the falling edge in the trigger configuration is preffered) because the trigger edge can be selected in the trigger input options. 

![ignition/vr_sensor_wiring.png](Images/ignition/vr_sensor_wiring.png)


**HALL SENSOR 

This sensor employs Hall's phenomenon to gauge the position and speed of a ferromagnetic trigger wheel. Unlike the variable reluctance sensor, it necessitates external power. Typically, these sensors feature "open collector" outputs and mandate the use of a pull-up resistor (with the Engine Management Unit or EMU, a 2K pull-up to +5V can be activated in the software menu by selecting the enable pull-up option). Hall sensors require a power supply in the range of 5-12V but exhibit greater immunity to interference when compared to magneto-inductive sensors. 

The scope trace of Hall sensor signal
![hallSensor.png](Images/hallSensor.png)


HALL and optical sensors require either +5V or +12V. Prior to installation, verify the sensor's power requirements, as supplying an incorrect voltage may result in sensor damage!
Here is a sample wiring diagram illustrating the connection of a Hall sensor to an Engine Management Unit (EMU) device. Both Hall and optical sensors typically feature open collector outputs and mandate a pull-up resistor (activate the pull-up option in the trigger input configuration).

![ignition/hall_sensor_wiring.png](Images/ignition/hall_sensor_wiring.png)


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Custom temp. cal 1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM 2

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Custom temp. cal 2

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM #1

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Digitalinputs) 
##CAM#1 sensitivity

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) [Auto](help://Sensorsandinputs/Switches/Rotaryswitches) 
##Rotary switch #1 cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Temperature) 
##Custom temp. cal #1

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Switches) 
##CAN-Bus stream

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Pre throttle boost cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear-in lower voltage

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear-in upper voltage

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear position sensor

The gear position sensor configuration allows for defining sensor parameters as well as defining voltage ranges for individual gears. It should be emphasized that in the case of using the sensor for sequential gear shift control, it should be connected to ** __Analog input #4__ **, which is logged at a rate of 250Hz (reading of all analog sensors is done at a frequency of 500Hz), which is necessary during the configuration of the gear shift strategy.

**Logging channels:

* __   **Gear** __ - actual gear
* __   **Gear sensor status ** __ - actual status of the gear position sensor
* __   **Gear unknown** __ - this channel indicates whether the voltage from the sensor is within the voltage ranges defined for the gears.


**Meaning of gear sensor status

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearpositionsensor) 
##Sensor parameters

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearpositionsensor) 
##Gear-in lower voltage

This table defines the minimum voltage from the gear position sensor for each gear. The correct voltage for a given gear must fall within the range of **__Gear-in lower voltage__** and **__Gear-in upper voltage__**. 
If the voltage from the sensor is not within the defined ranges for any gear, the **__Gear unknown**__ logging channel is equal to 1. This indicates a gear change or incorrectly defined values for the Gear-in lower voltage and Gear-in upper voltage tables.

The diagram below shows a plot defining gears 1 and 2.

![sport/gearDefinition.png](Images/sport/gearDefinition.png)


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearpositionsensor) 
##Gear-in upper voltage

This table defines the maximum voltage from the gear position sensor for each gear. The correct voltage for a given gear must fall within the range of **__Gear-in lower voltage__** and **__Gear-in upper voltage__**. 
If the voltage from the sensor is not within the defined ranges for any gear, the **__Gear unknown**__ logging channel is equal to 1. This indicates a gear change or incorrectly defined values for the Gear-in lower voltage and Gear-in upper voltage tables.

The diagram below shows a plot defining gears 1 and 2.

![sport/gearDefinition.png](Images/sport/gearDefinition.png)


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear leaver load cell

Each group contains specific information related to its respective area


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearleaverloadcell) 
##Sensor parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear lever load cell

Each group contains specific information related to its respective area


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearleverloadcell) 
##Sensor parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Gear lever

The gear level parameters allow for defining the behavior of load cells or switches installed on the gear lever, which are used in the gear shift strategy for sequential gearboxes.

**Logging channels:

* __   **Gear lever load cell voltage** __ - the gear lever load cell voltage.  Channel used only when leaver uses load cell sensor.
* __   **Gear lever load cell sensor status ** __ - actual status of the gear position sensor. Channel used only when leaver uses load cell sensor.
* __   **Gear lever action** __ - this channel specifies the desired action that the gear shift strategy is supposed to execute.
* __   **Gear lever shift up** __ - this channel specifies if the shift up request switch is pressed. Channel used only when leaver uses switches.
* __   **Gear lever shift down** __ - this channel specifies if the shift down request switch is pressed. Channel used only when leaver uses switches.



**Meaning of gear leaver action

* __   **No action** __ -  no gear shift action request
* __   **Up shift request __**   -  up shift shift action request
* __   **Down shift request**  __ -  down shift shift action request
* __   **Error ** __ -  load cell sensor error
* __   **Unassigned ** __ -  load cell sensor analog input not assigned



**Meaning of gear sensor status

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input








---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearlever) 
##Sensor parameters

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##PPS check voltage vs pedal pos.

A table defining the expected voltage from the __**PPS check sensor**__ for a given pedal position expressed in %


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##TPC check voltage vs throtlte pos.

A table defining the expected voltage from the __tps check sensor__ for a given pedal position expressed in %

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/TPSPPS) 
##TPS check voltage vs throtlte pos.

A table defining the expected voltage from the **__TPS check sensor**__ for a given throttle position expressed in %.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Othersensors) 
##EWG position sensor

The **__EWG position sensor**__ must be configured first in order to use the boost control strategy with the electronic wastegate. If the sensor status is anything other than OK, the EWG control signal (HBRIDGE 2) will be disabled.

**Logging channels:

* __   **EWG position** __ - actual electric wastegate position. 0% means fully open (the minimum boost), 100% means fully closed (the maximum boost)
* __  **EWG pos sensor status** __ -actual EWG position sensor status


**Meaning of EWG pos sensor status:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input


{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Othersensors) 
##Turbooshaft speed

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Othersensors) 
##Turboshaft speed

The turbocharger speed sensor can be connected to the **__VSS**__ or **__CAM 2**__ input. The input signal is measured and expressed in **__kRPM**__ (thousands of revolutions per minute). This value is available in the **__Turboshaft speed**__ logging channel.

{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) 
##Paddle shifters

Paddle shifters allow for defined paddles and additional buttons used in paddle shift strategy.

**Logging channels:

* __   **Paddle up** __ - actual egnine oil pressure value 
* __   **Paddle down** __ - state of the switch used to shift down
* __   **N switch** __ - state of the switch that can be used to engage **__Neutral**__ gear
* __   **R switch** __ - state of the switch that can be used to engage **__ Reverse**__  gear
* __   **Paddle hold switches** __ - state of the switches in the ** __Hold** __ state


{#1}


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Wastegate dome pressure cal.

The table defining the relationship between the pressure of the sensor and the voltage from the analog input of the device.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/Pressure) 
##Nitrous pressure cal.

The table defining the relationship between the pressure of the 
sensor and the voltage from the analog input of the device.


---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearlever) 
##Gear shift up threshold

When using a **gear position sensor** in the gearbox **to activate the gear shift strategy**, it is necessary to define, for each gear, the voltage above which a cut request will be sent to the gear shift strategy. This table is used exclusively when the **__Gear lever type**__ is set to **__Gear sensor**__.

**Important!
The voltage value for a given gear must be lower than the {1} for the next gear in the gearbox position sensor calibration.

---

[Auto](help://Sensorsandinputs/Sensorsandinputs) [Auto](help://Sensorsandinputs/VSSandGearbox) [Auto](help://Sensorsandinputs/VSSandGearbox/Gearlever) 
##Gear shift down threshold

When using a **gear position sensor** in the gearbox **to activate the gear shift strategy**, it is necessary to define, for each gear, the voltage below which a blip request will be sent to the gear shift strategy. This table is used exclusively when the **__Gear lever type**__ is set to **__Gear sensor**__.

**Important!
The voltage value for a given gear must be higher than the {1} for the previous gear in the gearbox position sensor calibration.

---

