
This text was automatically translated and may contain minor inaccuracies.
	

---

##ALS

**Logging channels:

* __** ALS fuel correction**__ - actual fuel dose correction caused by ALS strategy.
* __** ALS cut**__   - the percentage of ignition events or fuel injections being cut off by ALS strategy.
* __**ALS state**__ - actual state of ALS strategy. States are described in the text above.
* __**ALS ingition angle**__ - actual ALS ignition angle correction (or absolute value depends on ALS settings)

---

##Alternator

**Logging channels:

* __  **Battery voltage target** __ - the target voltage for the __**Alternator control__** strategy to aim for
* __  **Battery voltage** __ - the current voltage in the electrical system
* __  **PWM 1 or PWM 2 DC** __ - the duty cycle of the alternator control signal depending on which PWM output the __**Alternator control__** strategy has been assigned to.



---

##Analog inputs

**Logging channels:

* __** Analog 1 - Analog 6**__ - the voltage of the given analog inputs
* __**TPS voltage**__ - Analog input voltage given for the TPS sensor
* __**TPS check error**__ - Error between the expected and actual voltage of the check sensor
* __**PPS voltage**__ - Analog input voltage defined for the TPS sensor
* __**PPS check error**__ - Error between the expected and actual voltage of the check sensorr
* __**IAT voltage**__ - Analog input voltage given for the IAT sensor
* __**CLT voltage**__ - Analog input voltage given for the CLT sensor


---

##Basic

* RPM
* MAP
* Engine runtime
* BARO
* Boost
* Estimated airflow
* PPS
* TPS
* IAT
* CLT
* Battery voltage
* Fuel level
* ECU State
* ECU Reset
* Tables set
* Engine actual torque


---

##Boost

**Logging channels:

* __   **Boost target**__ - current desired boost pressure
* __   **Boost target from table**__ - current desired boost pressure read from the Boost Target table
* __   **Boost DC**__ - current DC of the solenoid
* __   **Boost DC from table**__ - current DC of the solenoid read from the {1} table
* __   **Boost target limit**__ - the lowest value limiting the boost pressure from the {2} tables
* __   **Boost target correction**__ - boost pressure correction from the {3} tables
* __   **Boost output disabled**__ - information whether the solenoid control is disabled because the current MAP pressure is lower than the __Disable Output Under MAP__ parameter or __Disable solenoid func.__ is equal to true.
* __   **Boost out of margin**__ - information whether the current boost pressure is within the range defined in the {4} parameters
* __   **Boost source**__ - information whether Boost is calculated from the MAP sensor or from the pre-throttle pressure sensor
* __   **Boost lambda guard corr.**__ - boost pressure correction applied by the {5} engine protection strategy
* __   **Boost tables blend**__ - percentage value of blending between Boost Target 1 and Boost Target 2 tables
* __   **EWG position**__ - current position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG target**__ - current desired position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG output DC**__ - current DC controlling the electric motor of the wastegate, ranging from -100 to 100, where 0 means no current is driving the motor


---

##Cruise control

**Logging channels:

* __ **Cruise control state**__ - current state of the startegy
* __ **Cruise control target**__  - desired target speed
* __ **Cruise control PID corr.**__  - current PID correction 
* __ **Cruise control is in range**__  - indicates whether the difference between the current speed and the Cruise Control target speed is less than the Margin Below Target value, which activates the PID controller


**Meaning of control statue:

* __**Disabled**__ - the **__Cruise control__** strategy is disabled
* __**Inactive under vss**__ - the **__Cruise control__** strategy is inactive due to vehicle speed lower than  **__Minimum speed to activate
* __**Inactive**__ - the **__Cruise control__** strategy is inactive waiting for user activation
* __**Suspended**__ - the **__Cruise control__** strategy is suspended. This situation occurs when, during the operation of the **__Cruise control**__ strategy, the driver increases the vehicle speed (the requested throttle opening is greater than the throttle opening calculated by the strategy). When the driver decreases the throttle angle, the **__Cruise control__** strategy will be restored.
* __**Active**__ - the strategy is active and controls vehicle speed suing the electronic throttle



---

##DBW

**Logging channels:

* __ **DBW target**__  - the current target that the throttle will aim to achieve. 
* __ **PPS**__ - the current position of the accelerator pedal.
* __ **TPS**__ - the current position of the throttle.
* __ **DBW targte blend percent**__ - the percentage value of blending between two characteristic maps. 0% means the value is taken from the DBW characteristic 1 table, 100% means the value is taken from the DBW characteristic 2 table.
* __ **DBW friction corr.**__ - the current DC correction resulting from the Friction characteristic table.
* __ **DBW Out. DC**__ - the duty cycle of the signal controlling the throttle electric motor.
* __ **DBW target source**__ - status indicating the current strategy controlling the throttle.
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


---

##Diff control

**Logging channels:

* **__Diff ctrl. active__** – status of differential control strategy activity
* __**Diff ctrl. oil pump active__** – status of differential oil pump control activity
* __**Diff ctrl. active table__** – currently active differential control table
* __**PWM 1 or 2 DC__** – depending on the selected PWM channel, indicates the current duty cycle of the solenoid valve controlling the differential

---

##DSG

**Logging channels:

* __**Engine torque**__ - current engine torque (with corrections) in %
* __**Engine actual torque**__ - current engine torque (with corrections) in Nm
* __**Engine torque losses**__  current engine torque losses in %
* __**DSG  torque losses**__  - current DSG gearbox torque losses reported by the gearbox
* __**DSG  combined  load**__ - current value of comined load % from {1} table
* __**DSG  gearbox torqe red. reqest**__  - current torque reduction request (in %) send by DSG gearbox
* __**DSG  blip RPM target**__  - required RPM (during downshift) requested by DSG gearbox
* __**DSG  mode**__  - current DSG mode (P, R, N, D, S, M)
* __**DSG  emulated selector pos**__  - in the case of gear selector emulation, this value represents the desired gearbox operating mode
* __**DSG  next gear**__  - indicates the next gear to which the gear shift will occur (reported by DSG)
* __**DSG  clutch**__ - state of DSG clutch (reported by DSG)
* __**DSG  clutch error**__  - indicates clutch fault (reported by DSG)
* __**DSG  blip**__  - a flag indicating that the ECU is performing a blip
* __**DSG  torque reduction**__ - a flag indicating the ECU is performing torque reduction 
* __**DSG  LC**__  - a flag indicating the DSG gearbox is in __Launch control__ mode
* __**DSG  fault**__ - a flag indicating the DSG gearbox fault 
* __**DSG  shift up**__ - a flag indicating an upshift is in progress
* __**DSG  shift down**__  - a flag indicating an downshift is in progress
* __**DSG  block engine start**__ -a flag indicating that the engine start conditions have not been met and the EMU is blocking fuel delivery (e.g., brake pedal not pressed, gearbox not in the P position, etc.)


---

##EGT

**Logging channels:

* **__EGT 1 and 2__**  – values of EGT sensors connected to the built-in inputs
* **__CAN EGT 1 to 8__** – values of EGT sensors read from the CAN bus (e.g., using EGT2CAN module)


---

##Enrichments

* Acc. Enrichment
* TPS Rate
* MAP rate
* Afterstart Enrichment
* Warmup enrichment


---

##FC reason

* Rev limiter
* Overrun fuel cut
* Cycling idle fuel cut
* Stuck throttle protection
* Fuel pressure protection
* Oil press. protection
* Pit limiter
* Flat shift
* Overboost
* Gear cut
* Idle
* Per injector FC
* Launch control
* Start/Stop
* Over pressure


---

##Flex Fuel

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

##FS

* Paddle up
* Clutch pedal switch
* Paddle down
* Flat Shift Fuel Cut
* Rolling start active
* Gear cut active
* Flat Shift Ign. Cut
* Rolling start ign. retard
* Rolling start target
* Flat Shift Active


---

##Fuel active corr.

* F.ASE correction
* F.Warmup correction
* F.IAT correction
* F.EGT correction
* Unused
* F.BARO correction
* F.FPR correction
* F.Fuel temp. correction
* F.ALS correction
* F.Knock correction
* F.LC correction
* F.Decelerate correction
* F.Accelerate correction
* F.Fuel cut
* F.Short term trim
* F.Flat shift correction
* F.Timer correction
* F.Custom correction #3
* F.Custom correction #2
* F. Lambda guard
* F.Nitrous correction
* F.AT correction
* F.Custom correction #1


---

##Fueling

* Fuel Cut
* Injectors PW
* Injectors DC
* Injectors cal. time
* VE
* Short term trim
* Lambda target
* Lambda target from table
* BARO Correction
* IAT Correction
* Per injector FC
* Fuel pressure
* Charge temp
* Differential fuel pressure
* Fuel pressure correction
* Fuel custom correction #1
* Fuel custom correction #2
* Fuel custom correction #3
* Injector 1 trim
* Injector 2 trim
* Injector 3 trim
* Injector 4 trim
* Injector 5 trim
* Injector 6 trim
* Secondary inj. PW
* Secondary inj. DC
* Secondary injectors split
* Lambda guard active
* Lambda error mult.
* Fuel Temp Correction
* Injection angle
* Fuel cut percent
* Fuel usage
* Fuel used
* Ethanol correction


---

##Gear cut

* Paddle up
* Clutch pedal switch
* Paddle down
* Flat Shift Fuel Cut
* Rolling start active
* Gear cut active
* Flat Shift Ign. Cut
* Rolling start ign. retard
* Rolling start target
* Flat Shift Active


---

##Idle

**Logging channels:
 	
* __** Idle control active**__  - when the idle state is Inactive, the idle control active log channel value is Yes.
* __** Idle state**__  - current state of the idle controller. Idle states are described in {1} help.
* __** Idle target**__  - current desired idle RPM.
* __** Idle ramp down offset**__  - current value of the Idle ramp down offset parameter (more information about this parameter can be found in the help section for Idle).
* __** Idle effective DC %**__  - effective DC of a PWM solenoid control signal
* __** Idle air %**__  - current desired airflow value.
* __** Idle motor step**__  - for a stepper motor actuator, this value specifies the current position of the stepper motor in steps. If the motor step is > 255, the log channel is equal to 255.
* __** Idle PID airflow % correction**__ - current correction of the airflow by the PID controller.
* __** Idle airflow custom corr.**__ - User-defined air flow correction specified in the {2} table.
* __** Idle airflow custom corr. active**__ - Indicates whether the custom air flow correction is active.
* __** Idle Ignition target **__ - the expected ignition timing value the idle controller will aim for.
* __** Idle ignition correction**__  - current correction of the ignition timing by the PID controller.
* __** Idle cut percent **__ - current percentage value of cut events for spark/fuel cut based idle.
* __** Idle force open loop**__ - all PIDs are disabled, integral terms are reseted.


---

##Knock Sensing

**Logging channels:

* __  **Knock level peak** __ - the maximum registered knock peak (**__Engine noise**__ - **__Knock voltage peak cyl**__) since the last sample in the log. A value of 0 indicates no knock, while values greater than zero indicate knock. The higher the value, the more severe the knock
* __  **Knock actions status __ **  - the current status of the knock sensor action strategy.
* __  **Knock engine noise__** - the reference voltage for which combustion proceeds correctly (no knock). If the **__Knock voltage peak cyl**__ exceeds this value, the ECU recognizes that knock has been detected.

* __  **Knocking cylinders**__ -  A list of cylinders where knock was detected since the last sample in the log.

* __  **Knock voltage peak cyl #1 - #8__ ** - the integrated voltage from the knock sensor for each respective cylinder.
* __  **Knock count__ ** - the number of engine cycles in which knock was detected. If this channel reaches the value of 65535, it will no longer increment.
* __  **Knock ign retard cyl #1-#8__** - these channels show the current ignition correction for each specific cylinder.


**Meaning of Knock action statuses:

* __   **Disabled__** -  the knock sensor action strategy is not enabled.
* __   **Inactive - condition not met __** The necessary conditions for the strategy (e.g., too low RPM) have not been met.
* __   **Inactive no knock__** - the conditions for the action strategy have been met, but no knock has been detected.
* __   **Active__** - knock has been detected, and the action strategy is active.


---

##Launch control

**Logging channels:

* **__LC state__** - the current state of the strategy, as described below.
* **__LC ignition angle__** -  the ignition timing advance angle resulting from the operation of the launch control strategy.
* **__LC fuel enrichment__** -  the percentage fuel-air mixture enrichment.
* **__LC cut__** -  flag indicates ignition or fuel cut.
* **__LC RPM target__** -  the target RPM towards which the strategy is currently working.
* **__RPM__** -  engine RPM
* **__LC boost target__** -  the boost target resulting from the operation of the launch control strategy.
* **__Boost__** -  actual boost pressure



**Meaning of Nitrous stage state

* **Inactive** - the strategy is inactive.
* **Wait for activation** - upon strategy activation, it transitions to this state for the defined __Activation delay__ period.
* **Active prestage** - the strategy is in prestage active state. 
* **Active** - the strategy is active.
* **Wait for exit** - upon strategy deactivation, it transitions to this state for the defined __Deactivation delay__ period.
* **Exit** - the state in which the ignition timing advance is restored, ignition cut is disabled, and in the case of electronic throttle control, the throttle is opened to a position determined by the current accelerator pedal position.



---

##Nitrous

**Logging channels:

* __ **Nitrous active**__  -  shows if any of nitrous  stage is active
* __ **Nitrous stage state**__  -  shows current statet of the stage.
* __ **Nitrous ign. mod.**__  -  shows current ignition correction from all active nitrous stages..
* __ **Nitrous fuel adder **__  -  shows current fuel correction added / substracted to the primary injectors PW.
* __ **Nitrous stage time **__  -  shows current stage time when active
* __ **Nitrous stage DC **__  -  shows stage current output DC (for progressive systems)
* __ **Nitrous stage output **__  -  shows stage output state. Can be used for controlling PMU outputs.


**Meaning of Nitrous stage state

* **__Inactive**__ - The stage is inactive (activation conditions not met).
* **__Active delay**__ - The stage is active and counting down before solenoid activation. The delay time is defined in the stage parameters.
* **Active timer** - The stage is active, the solenoid output is engaged, and the following parameters are applied:  **__Timer__** (__Nitrous stage X time__), **__Ignition timing correction**__ (__Nitrous Ign. Mod.__),  ** __ Additional fuel injection__** (__Nitrous fuel adder__)
* **Active LC** - The stage is active during Launch contro,, the solenoid output is engaged, and the following parameters are applied:  **__Timer__** (__Nitrous stage X time__), **__Ignition timing correction**__ (__Nitrous Ign. Mod.__),  ** __ Additional fuel injection__** (__Nitrous fuel adder__)
* **Finished**  - The nitrous procedure has ended (time elapsed) or has been interrupted (e.g., throttle pedal released). To return to the **__Inactive state**__, the stage activation conditions must be met again.
* **Post active** - If ignition or fuel corrections remain active after the solenoid is turned off (__**Fuel Off Delay > 0**__ or Ign. __**Corr. Off Delay**__ > 0), the strategy transitions into the **Post active** state. Once the correction hold time expires, the strategy transitions to the **Finished** state.




---

##Other

**Logging channels:

* __   **Log fw version**__ - firmware version used during log acquisition. Firmware version is 3.xx, with 'xx' representing the value recorded in the logging channel.
* __   **Check engine code**__ - the check engine code reflects faults detected by the EMU. A complete list of error codes is provided at the end of this description.
* __   **Tables CRC**__ - the CRC16 of EMU tables
* __   **Variables CRC**__ - the CRC16 of EMU variables
* __   **Monitored P term**__ -  indicate the current values of the PID P component. To monitor a particular PID controller, you need to select it from the PID controller list beforehand (from {1} settings).
* __   **Monitored I term**__ -   indicate the current values of the PID I component. To monitor a particular PID controller, you need to select it from the PID controller list beforehand (from {2} settings).
* __   **Monitored D term**__ -  indicate the current values of the PID D component. To monitor a particular PID controller, you need to select it from the PID controller list beforehand (from {3} settings).
* __   **Steering wheel angle**__ - steering wheel angle in degrees. This channel is used by the following CAN streams: Lancer EVO X, Subaru STI.
* __   **Yaw rate**__ - vehicle yaw rate. This channel is used by the following CAN streams: Lancer EVO X.
* __   **Lateral G**__ - vehicle lateral G force. This channel is used by the following CAN streams: Lancer EVO X.
* __   **Frequency output**__ - current output signal frequency (strategy {4})
* __   **Cruise control engine start block**__ - engine start inhibited by cruise control strategy – awaiting brake pedal input.
* __   **DSG block engine start**__ - engine start inhibited by DSG control strategy – awaiting brake pedal input.



**Meaning of check engine codes:
* __**CLT__** - coolant temperature sensors error
* __**IAT__** - intake manifold temperature sensor error
* __**MAP__** - intake manifold pressure sensor error
* __**WBO__** - wideband oxygen sensor error
* __**EGT1__** - EGT sesnor 1 error
* __**EGT2__** -EGT sesnor 2  error
* __**KNOCK__** - knocking detected
* __**FF SENSOR__** - flex fuel sensor error
* __**DBW__** - drive by wire error
* __**FPR__** - fuel pressure error (reported by {5} strategy)
* __**DIFF CTRL__** - differential control error (oil pressure pump issue)
* __**EWG__** - electronic wastegate error (position sensor issue)
* __**OILP__** - low oil pressure 			
			


---

##Outputs

**Logging channels:

* __  **PWM 1 DC** __ - duty cycle of PWM 1 output
* __  **PWM 2 DC** __ - duty cycle of PWM 2 output
* __   **INJ outputs** __ - information about the currently active INJ outputs (1–6). It should be noted that the channel is logged at 25 Hz, and the information about PWM signals may be inaccurate due to the low sampling frequency.
* __   **AUX outputs** __ -  information about the currently active AUX outputs (1–6). It should be noted that the channel is logged at 25 Hz, and the information about PWM signals may be inaccurate due to the low sampling frequency.
* __  **Coolant fan** __ - Indicates whether the coolant fan is engaged. 
* __  **Coolant fan DC** __ - In the case of a radiator fan controlled by a PWM signal, this channel indicates the current duty cycle (DC) of the control signal.
* __   **Fuel pump state** __ - the state of fuel pump output.
* __   **Shift light** __ - the state of shift light output.
* __   **AC clutch** __ - the state of AC clutch otuput.
* __   **EWP active** __ - the state of  EWP otuput. 
* __   **Output test state** __ - indicates whether the **__Output Test__** tool is active.


---

##Overrun

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

##Pressure

**Logging channels:

* __   **MAP** __ - actual mainfold absolute pressure value 
* __   **Baro** __ - actual barometricpressure value 
* __   **Boost** __ - actual boost pressure value 
* __   **Engine oil pressure** __ - actual egnine oil pressure value 
* __   **Fuel pressure** __ - actual fuel pressure value 
* __   **AC  pressure** __ - actual airconditioning pressure value 
* __   **Back pressure** __ - actual back pressure value 
* __   **Differentail oil pressure** __ - actual differential oil pressure value 
* __   **Coolant pressure** __ - actual coolant pressure value 
* __   **Crankcase pressure** __ - actual crankcase pressure value 
* __   **Differential oil pressure** __ - actual differential pressure value 
* __   **Nitrous pressure** __ - actual Nitrous bootle pressure value 
* __   **Pre throttle boost pressure** __ - actual boost pressure from the pre throttle installed sensor 
* __   **Wastegate dome pressure**__ -  wastegate dome pressure for the wastgate installed sensor


---

##PWM

* PWM#1 DC
* PWM#2 DC


---

##Rev limiters

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
* **__RPM Fuel cut__** - Complete fuel cut-off for the RPM defined in the Fueling/Fuelcut
* **__Launch control__** - Active rev limiter defined by Launch control strategy
* **__Rolling start__** - Active rev limiter defined by Rolling start strategy




---

##Rev matching

**Log Channels:

* **__Rev. match active__** - indicates whether the strategy is active and attempting to set the desired RPM.
* **__Rev. match RPM target__** - the desired RPM that the strategy aims to set.
* **__Rev. match Gear target__** - the expected gear after the reduction.
* **__Rev. match armed__** - indicates whether the strategy is armed (brake pedal pressed) and waiting for activation.



---

##Sensors

* AC evap status
* CLT status
* Diff. oil temp. status
* Fuel temp. status
* Gearbox oil temp. status
* IAT status
* Engine oil temp. status
* Power steering fluid temp. status
* Pre IC temp. status
* Brake fluid temp. status
* Post IC temp. status
* Ambient temp. status
* Diff. oil press. status
* BARO status
* AC press. status
* MAP status
* Engine oil pressure status
* Coolant fluid press. status
* Fuel press. status
* Crankcase press. status
* Back press. status
* TPS main status
* TPS check status
* PPS main status
* PPS check status
* Cyl. head temp. #2 status
* Cyl. head temp. #1 status


---

##Short term

**Logging channels:

* __  **Lambda target**__ - target lambda to which the PID controller aims.
* __  **Lambda 1**__ - current Lambda value of the fuel-air mixture.
* __ **Short term trim **__ - fuel dose correction introduced by the **Short term trim** strategy.
* __  **Estimated airflow **__ - estimated airflow through the engine in g/s.
* __  **Lambda target from table**__ - expected **Lambda** value read from the {1} table.
* __  **Lambda error mult.**__ - theoretical percentage value by which the **VE** table cell can be multiplied to achieve the **Lambda target**.
* __  **F.Short term trim**__ - indicates that {2}  correction is active and currently modifying the injected fuel amount.

---

##Statuses

* Knock action status
* VVT CAM 2 status
* VVT CAM1 status
* Trigger sync status
* Cruise control state
* Overrun status


---

##Switches

**Logging channels:

* __ ** Switch 1__ ** - the state of the built-in Switch 1 
* __ ** Switch 2__ ** - the state of the built-in Switch 2
* __ ** Switch 3__ ** - the state of the built-in Switch 3
* __** Brake pedal switch **__ - the state of the brake pedal
* __** Clutch pedal switch**__ - the state of the clutch pedal
* __** CAM1 signal level**__ - the state of the CAM1 input pin
* __** CAM2 signal level**__ - the state of the CAM2 input pin
* __** Rx switch**__ - the state of the RS232 Rx input pin. This switch is activated by high level (+5 or +12V) 





---

##Switches CAN

CAN Switches represent various types of switches controlled via the CAN bus. They can be set using a CAN switch board, a vehicle-specific CAN stream, or a User-defined CAN stream.


**Logging channels:

* __   ** CAN Switch #1 to #20** - state of the corresponding CAN switch.

---

##Switches latching

**Logging channels:

* __** Latching SW 1__**  - the state of latching switch 1 (LLSW_A, LSW_B, LSW_C, LSW_D)
* __** Latching SW 2__**  - the state of latching switch 2 (LSW_A, LSW_B, LSW_C, LSW_D)
* __** Latching SW 3__**  - the state of latching switch 3 (LSW_A, LSW_B, LSW_C, LSW_D) 
* __** Latching SW 4__**  - the state of latching switch 4 (LSW_A, LSW_B, LSW_C, LSW_D)


---

##Switches MUX

**Logging channels:

* __** Mux switch voltage raw __** - the raw voltage of mux switch analog input
* __** Mux switch 1 __** - the state of Mux switch 1
* __** Mux switch 2 __** - the state of Mux switch 2
* __** Mux switch 3 __** - the state of Mux switch 3


---

##Switches rotary

**Logging channels:

* __ ** Rotary switch 1 __ ** - the current position of the rotary switch
* __ ** Rotary switch 2 __ ** - the current position of the rotary switch
* __ ** Rotary switch 3 __ ** - the current position of the rotary switch
* __ ** Rotary switch 4 __ ** - the current position of the rotary switch
* __ ** Rotary switch 5 __ ** - the current position of the rotary switch
* __ ** Rotary switch CAN 1 __ ** - the current position of the rotary switch received by CAN
* __ ** Rotary switch CAN 2 __ ** - the current position of the rotary switch received by CAN
* __ ** Rotary switch CAN 3 __ ** - the current position of the rotary switch received by CAN
* __ ** Rotary switch CAN 4 __ ** - the current position of the rotary switch received by CAN
* __ ** Rotary switch BT 1 __ ** - the current position of the rotary switch received from eDash PRO 
* __ ** Rotary switch BT 2 __ ** - the current position of the rotary switch received from eDash PRO 
* __ ** Rotary switch BT 3__ ** - the current position of the rotary switch received from eDash PRO 
* __ ** Rotary switch BT 4 __ ** - the current position of the rotary switch received from eDash PRO 

---

##Switches user

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

##Tables

**Logging channels:

* __ **FF blend ign**__ - the current blend percentage between the **__Ignition angle**__ tables. A value of 100% means that the ignition timing value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Ignition angle **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend lambda**__ - the current blend percentage between the **__Lambda target**__ tables. A value of 100% means that the **__Lambda target**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Lambda target **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend cranking fuel**__ - the current blend percentage between the **__Cranking fuel**__ tables. A value of 100% means that the **__Cranking fuel**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Cranking fuel**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend warmup**__ - the current blend percentage between the **__Warmup enrichment**__ tables. A value of 100% means that the **__Warmup enrichment**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Warmup enrichment**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.

* __ **FF blend ASE**__ - the current blend percentage between the **__ASE**__ tables. A value of 100% means that the **__ASE__** value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__ASE**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.

* __ **FF blend VE**__ - the current blend percentage between the **__VE**__ tables. A value of 100% means that the VE value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__VE **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **Overrun tables index**__ - index of the currently used **__Overrun**__ tables.
* __ **VE table index**__ - index of the currently used VE table.
* __ **VVT CAM1 table index**__ - index of the currently used **__VVT CAM1**__ table.
* __ **VVT CAM2 table index**__ - index of the currently used **__VVT CAM2**__ table.


---

##TC

* TC status, Statuses
* I.Wasted spart
* TC intervention
* TC dRPM Raw
* TC adjust pos
* TC dRPM
* Driven axle speed
* Undriven axle speed
* TC slip
* TC slip target
* TC Torq. Reduction req.


---

##Temperature

**Logging channels:

* __   **IAT** __ -intake manifold temeperature value
* __   **CLT** __ -coolant temperature value  
* __   **Engine oil temperature** __ - actual engine oil temperature value 
* __   **Fuel temperature** __ - actual fuel temperature value 
* __   **AC EVAP temperature** __ - actual AC evaporator temperature value 
* __   **Pre IC  temperature** __ - actual pre intercooler  temperature value 
* __   **Post IC temperature** __ - actual post intercooler temperature value 
* __   **Power steering temperature** __ - actual power steering  temperature value 
* __   **Gearbox oil temperature ** __ - actual gearbox oil temperature 
* __   **Differential oil temperature** __ - actual differential oil temperature value 
* __   **Brake fluid temperature** __ - actual brake fluid temperature value 
* __   **Ambient temperature** __ - actual ambinet temperature value 
* __   **Cylinder head temp. 1** __ - actual cylinder head temperature 1 value 
* __   **Cylinder head temp. 2** __ - actual cylinder head temperature 2 value 
* __** ECU temperature**__ – current ECU (microcontroller) temperature. This value should not exceed 105°C.




---

##Timers

**Logging channels:

* __**Timer 1**__  - current time of timer 1
* __**Timer 2**__  - current time of timer 2
* __**Drag race timer**__  - current time of Drag race timer
* __**Active timers**__  - shows active timers
* __**Timer fuel corr.**__  - current correction of the fuel dose (Lambda target or Injectors PW).  0 means no correction.
* __**Timer ign. corr.**__  - current correction of the ignition advance. 
* __**Timer boost corr.**__  - current correction of the boost targe


**Active timers:
* __**None**__  - none of the timers is active.
* __**Timer 1 active**__  - timer 1 is active.
* __**Timer 2 active**__  - timer 2 is active.
* __**Drag timer active**__  - Drag race timer is active.

---

##Torque active corr.

* Torque corrections flags
* Engine actual torque


---

##Unused

* toBeUsed99
* unused15
* CAM1 signal level
* D6
* Knock Action Ign. Retard


---

##Vss and gears

**Logging channels:

* **__Vehicle speed**__ – Estimated vehicle speed based on selected speed source (e.g., driven axle, GPS, etc.).
* __**Gear**__ – current calculated gear .
* __**Driven axle speed**__ – rotational speed of the driven axle (in RPM), derived from the input frequency.
* __**Undriven axle speed**__ – rotational speed of the undriven axle (in RPM), derived from the input frequency.
* __**Wheel speed FL / FR / RL / RR**__ – individual wheel speeds: Front Left, Front Right, Rear Left, and Rear Right (typically read via CAN from ABS or traction control system).
* __**GPS speed**__ – vehicle speed calculated from the GPS module data.
* __**Driven axle input frequency**__ – Raw frequency signal from the driven axle speed sensor.
* __**Undriven axle input frequency**__ – Raw frequency signal from the undriven axle speed sensor.
* __**Gear speed to RPM ratio**__ – calculated ratio between vehicle speed and engine RPM, used for gear estimation. Can be dirietly used to fill the {1} speed to RPM ratios.

---

##VVT

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

##WBO

**Logging channels:

* __   **Lambda 1** __ - actual Lambda value 
* __   **Lambda 2__** - actual Lambda value 2nd sensor (using external controller) 
* __  **Lambda is valid** __ - It indicates whether the sensor is functioning correctly and displaying accurate lambda values. In the case where the sensor is heating up or is damaged, the value of this channel is 'No'
* __   **AFR** __ - Air to fuel ratio for given Lambda and fuel type 
* __   **AFR 2**  __ - Air to fuel ratio for given Lambda 2 and fuel type 
* __   **WBO IP ADC** __ - internal ADC value for IP measure
* __   **WBO RI** __  - the value of measurerd voltage of sensor RI 
* __   **WBO Heater DC** __  - the lambda sensor heater DC 
* __   **WBO VS** __  - the value of sensor VS
* __   **WBO IP Meas. ** __ - the value of normalized value of sensor IP
* __   **WBO sensor temperature** __ - the temperature of the sensor is estimated based on the Nernst cell resistance (Ri). The minimum displayed temperature is approximately 620°C. If the temperature is 0°C, it indicates that the sensor is not sufficiently heated or is malfunctioning.
* __   **WBO is calibrating** __  - during the calibration process this channel is equal to Yes


---

##Custom #1

Custom log channel windows allow you to define and display your own channels.

By right-clicking on any log window, a menu will appear where you can add a channel to one of the three custom windows ("**__Add to custom**__").
By right-clicking on a Custom Log window, options appear to change the order of displayed channels ("**__Move up**__" / "**__Move down**__") and to remove a channel ("**__Remove from custom**__")
.



---

##Graph #1

The logging window allows for real-time as well as offline viewing of data sent by the device. The device always logs all available channels.
Logging channels are recorded at frequencies of **25 Hz**, **50 Hz**, **100 Hz**, or **200 Hz**, depending on the channel (the frequency is always displayed next to the channel name).
The logging window consists of 12 tabs. Each tab can be given a custom name and assigned independent logging channels for display.


##KEYBOARD SHORTCUTS

* **0 to 9** - switches between tabs
* **CTRL + arrow left / right** - move between tabs
* **Arrows up / down ** - zoom in / out
* **Q or arrow up** -  zoom in
* **A or arrow down** - zoom out
* **Z** - zoom selected area
* **SHIFT + S** - change line style
* **M** - mark a flag on the log


##TOOLBAR

| Icon | Description |
|![ICONS/save.png](Images/ICONS/save.png)|  Save current log data to file |
|![ICONS/open.png](Images/ICONS/open.png)| Open previously save log data from file|
|![ICONS/append.png](Images/ICONS/append.png)| Append previously save log data to existing log|
|![ICONS/exportCSV.png](Images/ICONS/exportCSV.png)| Export log data to CSV text file|
|![ICONS/zoomIn.png](Images/ICONS/zoomIn.png)| Zoom in the view (__**key Q or arrow UP**__)|
|![ICONS/zoomOut.png](Images/ICONS/zoomOut.png)| Zoom out the view (__**key A or arrow DOWN**__)                      |
|![ICONS/zoomFullOut.png](Images/ICONS/zoomFullOut.png)| Zoom full out                 |
|![ICONS/zoomExtent.png](Images/ICONS/zoomExtent.png)|  Zoom selected area (__**key Z**__)          |
|![ICONS/clearLog.png](Images/ICONS/clearLog.png)|  Clear all logged data |
|![ICONS/startLog.png](Images/ICONS/startLog.png)|  Resume  logging |
|![ICONS/stopLog.png](Images/ICONS/stopLog.png)|  Pause logging |
|![ICONS/logList.png](Images/ICONS/logList.png)|  View configuration|
|![ICONS/presetList.png](Images/ICONS/presetList.png)|  Presets configuration	  |
|![ICONS/config.png](Images/ICONS/config.png)|  Channels configuration	 |
|![ICONS/condition.png](Images/ICONS/condition.png)| Conditional logging |

**Save current  log data to file
This function allows saving the current log to a file on the computer's disk.

**Open log data 
This function allows loading a previously recorded file from disk into memory, as well as loading a log recorded using the EDL device.

**Append log data 
This function allows appending a log from a file to the current log stored in the computer’s memory.

**Export to CSV  

t is possible to export the logged data to a CSV text file, which can later be analyzed in other software. Please note that the size of the CSV files will be significant (approximately 5 MB per 1 minute of logging).
If a section of the log is selected, only the selected area will be exported to the file.

After clicking the Export to CSV icon, the following selection window will appear:

![exportCSV.png](Images/exportCSV.png)

* **Export** – allows you to choose whether only the visible channels (Only visible) or all available channels (All channels) should be exported.
* **Frequency** – defines the frequency at which data will be exported. For 50 Hz and 100 Hz options, channels with a logging frequency equal to or higher than the selected frequency (e.g., Analog inputs, RPM, etc.) will be exported at that frequency. All other channels will be exported at 25 Hz. Keep in mind that the higher the frequency, the larger the resulting file size.
* **Estimated file size** – estimated size of the resulting file in MB.


** Zoom in/out ** 
This option allows you to zoom in or out on the visible data range.

** Zoom full out
This option maximizes the displayed data range, limited by the minimum allowed zoom level.

** Zoom selected area
This option automatically adjusts the selected log area to fit the size of the display window.

**Resume / Pause logging
This button allows you to pause and resume the display of new log values. When paused, you can navigate through the log manually; otherwise, the log view will scroll automatically as new data is received. The pause function does not stop data collection from the device. Once resumed, all data logged during the pause will be displayed.


##MAIN VIEW

The lines on the graphs can be displayed in two ways: as continuous lines (with linear interpolation between logged data points) or as discrete points representing the exact values recorded by the ECU at specific timestamps.
This allows for better data interpretation, especially when a given channel is logged at a lower frequency.
The illustration below shows both line rendering methods. You can switch between them during operation using the keyboard shortcut **SHIFT + S**.

![logLines.png](Images/logLines.png)


---

##Tune Display

 Here, you can view and analyze relevant information.


---

##Scope

The **Scope tool** allows for the visualization of pulses from the **Primary Trigger**, **CAM1**, and **CAM2** sensors for the purposes of diagnostics, technical support, and verification of correct configuration. It also assists with the configuration of the **VVTi** system.

Additionally, this tool enables visualization of the ignition system operation (e.g., dwell time, spark angle) as well as the fuel system behavior (e.g., injector opening times and moments).

The scope data also includes information about:
* the number of cylinders
* the Primary Trigger configuration
* the firing order
* details regarding the selected signal edges


**Toolbar Description:

| Icon | Description |
|![ICONS/save.png](Images/ICONS/save.png)|  Save current scope data to file |
|![ICONS/open.png](Images/ICONS/open.png)| Open previously save scope data from file|
|![ICONS/zoomIn.png](Images/ICONS/zoomIn.png)| Zoom in the view (__**key Q or arrow UP**__)|
|![ICONS/zoomOut.png](Images/ICONS/zoomOut.png)| Zoom out the view (__**key A or arrow DOWN**__)                      |
|![ICONS/zoomFullOut.png](Images/ICONS/zoomFullOut.png)| Zoom full out                 |
|![ICONS/zoomExtent.png](Images/ICONS/zoomExtent.png)|  Zoom selected area (__**key Z**__)          |
|![ICONS/blueArrowDown.png](Images/ICONS/blueArrowDown.png)|  Start to gather the data        |


**To acquire scope data, follow these steps:

1. Preconfigure the trigger system, including sensor types, trigger settings, etc.

2. Click the blue arrow located on the toolbar of the Scope window.

3. A progress window will appear, indicating that data acquisition is in progress.

4. Start cranking the engine.

5. The progress bar in the window should begin to move, indicating that the data buffer is filling.

6. Once the buffer is full, the collected data will be displayed automatically.

You can also click the **Cancel button** at any time – in this case, the data collected up to the point of cancellation will be shown. If the progress bar does not move, it means that the **EMU** is not detecting any pulses on the **Primary Trigger**, **CAM1**, or **CAM2** inputs.


Below is a sample scope capture from a **Nissan VQ35** engine. The scope window is divided into five separate sections, each visualizing the following signals:
* Primary trigger pulses
* CAM#1 pulses
* CAM#2 pulses
* Ignition outputs
* Injection outputs


Additional information is displayed in the title bar of the scope window. The title bar contains the following information:

* Number of defined teeth
* First trigger tooth
* Trigger angle
* Number of cylinders
* Phase inversion
* Defined firing order
* Ignition angle (ignition angle at the moment the data was captured)
* File path (if the data was opened from a saved file)


![Scope/scope1.png](Images/Scope/scope1.png) 


The picture below shows the **Primary trigger** section of the scope.

1. Selected trigger edge – indicates whether the rising or falling edge is used (Falling, Rising).

2. Thick red line – marks the synchronization point of the trigger decoder (e.g., missing tooth).

3. Red circle on the red line – indicates the cycle synchronization point.

4. Red lines – represent trigger pulses. Gray lines – represent ignored pulses (for multitooth-type triggers). To capture these, the **__Take skipped edges on scope__** option must be enabled in the **Primary trigger** settings.

5.  Primary tooth index (full cycle) – shows the index number of each tooth within the complete engine cycle

![Scope/scopePrimaryTrigger.png](Images/Scope/scopePrimaryTrigger.png) 

The picture below shows the **CAM#1** section of the scope.

1. Selected trigger edge – indicates whether the falling or rising edge is used.

2. Blue circle on blue line – represents the **CAM #1** synchronization point.

3. The pulse angle (0–720) – indicates the angle position of the pulse within the full engine cycle.

4. Factor value – the ratio of times between consecutive CAM teeth. This value is used in the configuration of **CAM #1** patterns, such as: **Shorter than factor**, **Longer than factor**, **Factors sequence**

![Scope/scopeCAM1.png](Images/Scope/scopeCAM1.png)

The picture below shows the **CAM#2** section of the scope.

1. Selected trigger edge – indicates whether the falling or rising edge is used.

2. Green circle on green line – marks the CAM #2 synchronization point.

3. Scope pulse angle (0–720) – indicates the angle of the pulse within the full engine cycle.

4. Nearest primary tooth – shows the closest primary trigger tooth. This information is useful when configuring the **__Primary Teeth Window pattern__**.

![Scope/scopeCAM2.png](Images/Scope/scopeCAM2.png)

The picture below shows the **Ignition** section of the scope.

1. Dashed line – indicates the expected spark angle.

2. Green line – marks the Top Dead Center (**TDC**) of the corresponding cylinder.

3. Blue line – represents the **dwell time**, with the dwell duration value displayed.

4. Real spark angle – shows the actual ignition timing at which the spark occurred.

5. Cylinder index – indicates the cylinder number for the corresponding ignition event.

![Scope/scopeIgnition.png](Images/Scope/scopeIgnition.png)

The picture below shows the *Injection** section of the scope.


1. Green line – marks the Top Dead Center (**TDC**) of the corresponding cylinder.

2. Cylinder index – indicates the cylinder number.

3.  Line indicates injection duration – a horizontal line showing the injector opening period; the purple circle marks the **Start of injection**.

4. Injection time (ms) – displays the injection duration in milliseconds.

5. Injection end angle – indicates the angle in degrees before **TDC** at which the **injection ends.**

![Scope/scopeInjection.png](Images/Scope/scopeInjection.png)








---

##Dyno

 Here, you can view and analyze relevant information.


---

##Autotune

More information about {1}

---

##Scatter #1

Scatter Plot

The **Scatter Plot** is a powerful diagnostic and visualization tool available in the EMU Black software. It allows you to display logged data points on a 2D chart with an optional third dimension represented by color.

* The **X** and **Y** axes can be assigned to any available log channels (e.g., RPM, MAP, IAT, Throttle Position).

* The **Z** axis is represented by a color gradient, allowing for visualization of a third parameter such as Lambda, Knock Level, or Ignition Angle.


For each logged data sample, a single point is plotted on the chart. Over time, this creates a cloud of points that illustrates how the engine operated across the selected parameters.

Example usage:

* **RPM vs. MAP** with color representing **Lambda** to analyze fueling consistency.
* **TPS vs. RPM** with color showing **Ignition angle&& to review spark advance strategy.
* **IAT vs. RPM** with color for **Knock level** to evaluate detonation sensitivity under varying temperatures.

--
**Configuration

![scatterPlot.png](Images/scatterPlot.png)

* **X,Y,Z Axis channel ** - specifies the log channel assigned to the X, Y, or Z axis of the scatter plot. The range (minimum and maximum values) for each axis is taken automatically from the graph log configuration for the selected channel.
<br>
* **X,Y,Z Axis filter samples  ** -specifies the number of samples used in the moving average filter for the X, Y, and Z axis channels. This filter smooths the displayed data by averaging a specified number of recent log samples, helping to reduce noise and fluctuations in the scatter plot.
<br>
* ** Point size ** - defines the size of the points displayed in the scatter plot.. Increasing point size can reduce rendering performance, especially when displaying a large number of points.

--
**Displayed data range

The range of data shown in the scatter plot depends on the selection made in the {1} window:

* If a region is selected in the graph log, only the points within that selection will be displayed.
* If no selection is made, all logged data points will be shown.



!!⚠️ Displaying all points from large logs may negatively impact application performance. For optimal responsiveness, it is recommended to work with selected data ranges when analyzing large logs.

This behavior allows for flexible and efficient data inspection, especially when focusing on specific events or operating conditions.





---

##AFR

AFR

---

##AFR 2

AFR 2

---

##Ambient temperature

Ambient temperature

---

##Analog #1

Analog #1

---

##BARO

BARO

---

##Battery voltage

Battery voltage

---

##Boost

Boost

---

##Boost DC

Boost DC

---

##Boost Target

Boost Target

---

##Brake fluid temperature

Brake fluid temperature

---

##CAN Analog #1

CAN Analog #1

---

##CLT

CLT

---

##Coolant fan DC

Coolant fan DC

---

##Custom ignition trim #1

Custom ignition trim #1

---

##Cyl. head temp. #1 status

Cyl. head temp. #1 status

---

##Cylinder head temp. #1

Cylinder head temp. #1

---

##Differential fuel pressure

Differential fuel pressure

---

##Differential oil temperature

Differential oil temperature

---

##Dwell Time

Dwell Time

---

##EGT #1

EGT #1

---

##Engine oil pressure

Engine oil pressure

---

##Engine oil temperature

Engine oil temperature

---

##Ethanol content

Ethanol content

---

##EWG DC

EWG DC

---

##EWG position

EWG position

---

##EWG target

EWG target

---

##Fuel custom correction #1

Fuel custom correction #1

---

##Fuel level

Fuel level

---

##Fuel pressure

Fuel pressure

---

##Fuel Temperature

Fuel Temperature

---

##Gear

Gear

---

##Gearbox oil temperature

Gearbox oil temperature

---

##IAT

IAT

---

##Idle Ign. Correction

Idle Ign. Correction

---

##Ign. custom correction #1

Ign. custom correction #1

---

##Ignition Angle

Ignition Angle

---

##Ignition From Table

Ignition From Table

---

##Injectors DC

Injectors DC

---

##Injectors PW

Injectors PW

---

##Knock Action Ign. Retard

Knock Action Ign. Retard

---

##Knock action status

Knock action status

---

##Knock count

Knock count

---

##Knock Engine Noise

Knock Engine Noise

---

##Knock ign corection

Knock ign corection

---

##Knock ign retard cyl 1

Knock ign retard cyl 1

---

##Knock Level Peak

Knock Level Peak

---

##Knock voltage peak cyl 1

Knock voltage peak cyl 1

---

##Lambda

Lambda

---

##Lambda 2

Lambda 2

---

##Lambda target

Lambda target

---

##Lambda target from table

Lambda target from table

---

##LC Cut

LC Cut

---

##LC Fuel Enrichment

LC Fuel Enrichment

---

##LC Ignition angle

LC Ignition angle

---

##MAP

MAP

---

##MAP rate

MAP rate

---

##Overrun status

Overrun status

---

##Post IC temperature

Post IC temperature

---

##Power steering fluid temp

Power steering fluid temp

---

##PPS

PPS

---

##Pre IC temperature

Pre IC temperature

---

##PWM#1 DC

PWM#1 DC

---

##RPM

RPM

---

##Secondary inj. DC

Secondary inj. DC

---

##Secondary inj. PW

Secondary inj. PW

---

##Secondary injectors split

Secondary injectors split

---

##Short term trim

Short term trim

---

##Tables blend

Tables blend

---

##toBeRemoved

toBeRemoved

---

##TPS

TPS

---

##Vehicle Speed

Vehicle Speed

---

##VVT CAM 2 status

VVT CAM 2 status

---

##Cranking correction

Cranking correction

---

##Unused4444

Unused4444

---

##Idle ign. correction

Idle ign. correction

---

##Idle PID ign. correction

Idle PID ign. correction

---

##Flat shift

**Logging channels:

* **__RPM**__ - actual engine RPM
* __   **Flat shift active** __ - flag indicating whether the flat shift strategy is active
* __   **Flat shift cut %** __ -  the value of ignition or injection events currently being cut (depending on the strategy configuration)
* __   **F.Flat shift corection** __ - fuel dose correction applied by the active Flat Shift strategy
* __   **Fuel cut percent**__ -   current percentage of injector cut (aggregated for all active strategies)
* __   **Spark cut percent** __ -  current percentage of ignition event cut (aggregated for all active strategies)
  













---

##Pit limiter

**Logging channels:

* __** Pit limiter state**__ - a channel indicating whether the pit limiter strategy is active.
* __** Pit limiter cut**__ - the percentage of ignition events or fuel injections being cut off.
* __** Pit limiter target speed**__ - the speed that the pit limiter strategy will strive to maintain.

---

##Pit limiter speed target

Pit limiter speed target

---

##CAM1 #1 status

CAM1 #1 status

---

##FF Ethanol content

FF Ethanol content

---

##MAP sensor rate

MAP sensor rate

---

##Rolling start

**Logging channels:

* __** Rolling start state**__ - a channel indicating whether the rolling start strategy is active.
* __** Rolling start target**__ - engine RPM that the rolling start strategy will maintain.
* __** Rolling start fuel corr**__ - current fuel dose correction.
* __**Rolling start ign. corr.**__ - current ignition advance angle correction.

---

##Debug

* PID Tu
* PID Ampl
* reserved8872
* reservedRR
* D7
* SOVERFLOW
* debugW
* D3
* D4
* D1
* CPU Load
* frameStamp
* reserved176


---

##reserved8

reserved8

---

##LC cut

LC cut

---

##LC fuel enrichment

LC fuel enrichment

---

##LC ignition angle

LC ignition angle

---

##Gearbox

* Gear leaver load cell
* Leaver load cell sensor status
* Gearbox sensor status


---

##Gear shift

**Logging channels:
* __   **Gear shift state** __ - the current state of the gear shift strategy
* __   **Gear shift state torque reduction** __ - actual value of the torque reduction during up shift..
* __   **Gear lever action** __ - this channel specifies the desired action that the gear shift strategy is supposed to execute.
* __   **Gear lever shift up** __ - this channel specifies if the shift up request switch is pressed. Channel used only when leaver uses switches.
* __   **Gear lever shift down** __ - this channel specifies if the shift down request switch is pressed. Channel used only when leaver uses switches.
* __   **Gear lever load cell voltage** __ - the gear lever load cell voltage.  Channel used only when leaver uses load cell sensor.
* __   **Gear lever load cell sensor status ** __ - actual status of the gear position sensor. Channel used only when leaver uses load cell sensor.
* __   **Gear sensor status ** __ - actual status of the gear position sensor
* __   **Gear unknown** __ - this channel indicates whether the voltage from the sensor is within the voltage ranges defined for the gears.


**Meaning of gear shift state
* __   **Disabled** __ - the controller is disabled 
* __   **Not active** __ - the controller is enabled but doesnt perform any operation
* __   **Rejected - clutch engaged** __ - the strategy was not activated because the clutch pedal was pressed.
* __   **Rejected - gearbox sensor error** __ - - the strategy was not activated because there is an error connected to the gear box sensor.  
* __   **Rejected - leaver sensor errorr** __ - the strategy was not activated because there is an error connected to the gear lever sensor.    
* __   **Rejected - upshift low RPM ** __ - the strategy was not activated because the RPMs are too low for the up shift .
* __   **Rejected - downshift high RPM ** __ - the strategy was not activated because the RPMs are too high for the down shift .
* __   **Rejected - gear unknown ** __ - the strategy was not activated because the current gear is unknown. 
* __   **Rejected - gear neutral ** __ - the strategy was not activated because the gear is neutral.
* __   **Rejected - gear reverse** __ - the strategy was not activated because the gear is reverse
* __   **Rejected - VSS too low** __ - the strategy was not activated because the vehicle speed is too low. 
* __   **Rejected - upshift tps too low** __ - The attempt to upshift failed because the throttle position was below the defined **__Min TPS to cut**__ value in the {1}.
* __   **Rejected - downshift tps too high** __ - The attempt to downshift failed because the throttle position was above the defined **__Max TPS to blip**__ value in the {2}.

* __   **Upshift - shift** __ - the strategy performs the up shift torque redcution (cut, ignition corr, DBW target corr).
* __   **Upshift - recovery** __ - the strategy performs recovery from the torque redcution stage.
* __   **Downshift - shift** __ - the strategy performs the down shift blip.
* __   **Downshift - recovery** __ - the strategy performs recovery from the blip stage.		
* __   **Rearm** __ - the strategy is rearm state.			


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


**Meaning of gear sensor status
* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input


---

##Analog 1

Analog 1

---

##CAN Analog 1

CAN Analog 1

---

##Custom ignition trim 1

Custom ignition trim 1

---

##Cyl. head temp. 1 status

Cyl. head temp. 1 status

---

##Cylinder head temp. 1

Cylinder head temp. 1

---

##EGT 1

EGT 1

---

##Fuel custom correction 1

Fuel custom correction 1

---

##Ign. custom correction 1

Ign. custom correction 1

---

##PWM1 DC

PWM1 DC

---

##CAN Analog 10

CAN Analog 10

---

##CAN Analog 11

CAN Analog 11

---

##Analog inputs CAN

**Logging channels:

* __** CAN Analog 1 - CAN Analog 12**__ the voltage of the given analog input set by CAN BUS (eg. can switch board or user defined CAN)

---

##Idle effective DC

Idle effective DC

---

##Acc. enrich. async PW

Acc. enrich. async PW

---

##EWG

**Logging channels:

* __   **EWG position**__ - current position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG target**__ - current desired position of the electronic wastegate (0% means the wastegate is fully open, 100% means the wastegate is fully closed)
* __   **EWG output DC**__ - current DC controlling the electric motor of the wastegate, ranging from -100 to 100, where 0 means no current is driving the motor
* __  **EWG pos sensor status** __ -actual EWG position sensor status


**Meaning of EWG pos sensor status:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input



---

##EWG output DC

EWG output DC

---

##Boost tables blend

Boost tables blend

---

##Paddle shift

**Logging channels:

* __ **Paddle shift status**__  - status of the **__Paddle shift**__ strategy
* __ **Paddle shift states**__  - states of the **__Paddle shift**__ strategy logged @ 100hz
* __   **Paddle up** __ - actual egnine oil pressure value 
* __   **Paddle down** __ - state of the switch used to shift down
* __   **N switch** __ - state of the switch that can be used to engage **__Neutral**__ gear
* __   **R switch** __ - state of the switch that can be used to engage **__ Reverse**__  gear
* __ **Performing downshift**__  - the **__Paddle shift**__ strategy is executing a downshift
* __ **Performing upshift**__  - the **__Paddle shift**__ strategy is executing an upshift
* __   **Paddle hold switches** __ - state of the switches in the ** __Hold** __ state


**Meaning of Paddle shift  statuses:

* __**OK**__ - no errors
* __**Rejected - RPM**__ - RPM are too low or too high to perform paddle shift 
* __**Rejected - VSS**__ - vehicle speed is too high to perform paddle shift 
* __**Rejected - clutch**__ - the clutch pedal is not pressed to perform paddle shift 
* __**Rejected - gear out of range**__ - attempt to shift to a gear lower than Reverse or higher than the maximum number of gears


**Meaning of Paddle shift  states:

* __**Inactive**__ - the paddle shift strategy is inactive
* __**Performing downshift**__ - the paddle shift strategy performs downshift
* __**Performing upshift**__ - the paddle shift strategy performs upshift
* __**Solenoid down**__ - the state of downshift solenoid
* __**Solenoid up**__ - the state of upshift solenoid
* __**Preload**_ - paddle shift strategy perfomrs preload phase



---

##ambientTemperature

ambientTemperature

---

##analogIn1

analogIn1

---

##asyncAccPW

asyncAccPW

---

##Baro

Baro

---

##Batt

Batt

---

##boostDC

boostDC

---

##boostTablesBlend

boostTablesBlend

---

##boostTarget

boostTarget

---

##brakeFluidTemperature

brakeFluidTemperature

---

##CANain1

CANain1

---

##CANain10

CANain10

---

##CANain11

CANain11

---

##coolantFanDC

coolantFanDC

---

##crankingFuelCorrection

crankingFuelCorrection

---

##customIgnTrim1

customIgnTrim1

---

##cylHeadTemp1

cylHeadTemp1

---

##cylHeadTemp1Status

cylHeadTemp1Status

---

##deltaFPR

deltaFPR

---

##diffOilTemp

diffOilTemp

---

##dwellTime

dwellTime

---

##Egt1

Egt1

---

##engineNoise

engineNoise

---

##ewgDC

ewgDC

---

##ewgPosition

ewgPosition

---

##ewgTarget

ewgTarget

---

##flexFuelEthanolContent

flexFuelEthanolContent

---

##fuelCustomCorr1Value

fuelCustomCorr1Value

---

##fuelLevel

fuelLevel

---

##fuelPressure

fuelPressure

---

##fuelTemperature

fuelTemperature

---

##gear

gear

---

##gearBoxOilTemp

gearBoxOilTemp

---

##idleEffectiveDC

idleEffectiveDC

---

##idlePIDIgnCorr

idlePIDIgnCorr

---

##IgnAngle

IgnAngle

---

##ignCustomCorr1Value

ignCustomCorr1Value

---

##ignFromTable

ignFromTable

---

##injDC

injDC

---

##knockActionsStatus

knockActionsStatus

---

##knockCount

knockCount

---

##knockIgnCorrAll

knockIgnCorrAll

---

##knockIgnCorrCyl1

knockIgnCorrCyl1

---

##knockLevel

knockLevel

---

##knockVoltagePeakCyl1

knockVoltagePeakCyl1

---

##lambdaTarget

lambdaTarget

---

##lambdaTargetFromTable

lambdaTargetFromTable

---

##lcFuelEnrich

lcFuelEnrich

---

##lcIgnRetard

lcIgnRetard

---

##lcSparkCut

lcSparkCut

---

##mapSensorRate

mapSensorRate

---

##oilPressure

oilPressure

---

##oilTemperature

oilTemperature

---

##overrunStatus

overrunStatus

---

##pitLimitSpeedTarget

pitLimitSpeedTarget

---

##postICTemperature

postICTemperature

---

##powerSteeringTemperature

powerSteeringTemperature

---

##preICTemperature

preICTemperature

---

##pulseWidth

pulseWidth

---

##pwm2OutputDC

pwm2OutputDC

---

##pwmOutputDC

pwmOutputDC

---

##scondarypulseWidth

scondarypulseWidth

---

##secondaryInjDC

secondaryInjDC

---

##secondaryInjSplit

secondaryInjSplit

---

##shorTermTrim

shorTermTrim

---

##vssSpeed

vssSpeed

---

##vvt1Status

vvt1Status

---

##wbo2AFR

wbo2AFR

---

##wboAFR

wboAFR

---

##Engine basic

**Logging channels:

* __**ECU state__** - device state
* **__RPM**__ - actual engine RPM
* **__MAP**__ -  actual MAP  value 
* **__Baro**__ - actual BARO value 
* **__Boost**__  - actual boost pressure
* **__TPS**__  - actual hrotle position 
* **__PPS**__  - actual accelerator pedal position
* **__IAT**__  - actual inake air emperaure 
* **__CLT**__  - actual coolant temperature
* **__Estimated airflow**__  - estimated airflow through the engine in g/s (used by {1} strategy)
* **__Battery voltage**__  - actuall battery voltage
* **__Engine runtime**__  -  time in seconds since engine start
* **__Tables set**__  - actual tables set
* **__ECU reset**__ -  each time the ECU is powered on or reset (e.g., after a firmware upgrade), the ECU reset channel takes the value 20 and decreases to 0. This allows for easy identification of ECU reset points in the log. Additionally, the ECU reset cause channel provides detailed information about the reason for the ECU reset.


**Meaning of ECU state:

* ** __INACTIVE**__ - the device is turned on, there is no signal from the position sensor / crankshaft, fuel is not supplied, and no spark is generated.
* **__CRANKING**__ - this is the state in which the engine revolutions usually oscillate around 200 rotations, and the controller tries to start the engine by dosing fuel and generating sparks. The transition to the next state occurs when the engine speed exceeds the Cranking threshold.
* **__AFTERSTART**__ - this is the state after starting the engine in which the Afterstart fuel correction is active.
* **__RUNNING__** - proper engine operation. 






---

##ECU

**Logging channels:

* __** ECU temperature**__ – current ECU (microcontroller) temperature. This value should not exceed 105°C.

* __** ECU reset cause **__ – reason for ECU reset:
* Power on – ECU was reset due to power-on
* Watchdog – ECU was reset by the internal watchdog. This is a very uncommon situation.  Please save the log / your project and contact our technical support (tech@ecumaster.com)
* Software reset – ECU was reset by software (e.g. during firmware upgrade)
* JTAG – ECU was reset by the JTAG programmer


* __**Engine protection code**__ – engine protection strategy is active:
* EGT – Exhaust Gas Temperature protection active
* FPRD – Fuel pressure protection active
* OVEB – Overboost protection active
* STT – Stuck throttle protection active
* OILP – Oil pressure cut protection active


* __**Autotune rejection reason__** – when the autotune tool is running, each log sample is marked with whether it was used to calculate the proposed VE map or the reason it was rejected:

* Accepted – the log sample was used to generate the VE map
* Rejected RPM – engine RPM is outside the range defined in the Autotune tool
* Rejected MAP – manifold pressure is outside the range defined in the Autotune tool
* Rejected TPS – throttle position is outside the range defined in the Autotune tool
* Rejected transient – log sample rejected due to a transient condition
* Rejected overrun – log sample rejected due to active overrun strategy
* Rejected fuel cut – log sample rejected due to active fuel cut
* Rejected spark cut – log sample rejected due to active spark cut
* Rejected acc enrich – log sample rejected due to active acceleration enrichment
* Rejected WBO – sample rejected because the lambda sensor was not operating within its valid range
* HBRIDGE 1 mode – H-bridge 1 operating mode:
* Outputs – H-bridge 1 used in single output mode
* DBW – H-bridge 1 used for drive-by-wire throttle control
* HBRIDGE 2 mode – H-bridge 2 operating mode:
* Outputs – H-bridge 2 used in single output mode
* EWG – H-bridge 2 used to control an electronic wastegate
* MQB signal on output A – H-bridge 2 output A used to generate a signal for MQB transmission


* **__CANBUS state**__ – status of the CAN bus:
* BUS OK – no CAN bus errors
* MODULE DISCONNECTED – CAN module disconnected (!!only applies to EMU Classic!!)
* BUS ERROR – CAN bus error. Possible causes include incorrect communication speed, swapped CANL/CANH, or bus short-circuit


* **__CANBUS load**__ – CAN system buffer load in percentage, based on the frames being sent

* **__CANBUS overload**__ – this flag indicates that strategies attempted to send more CAN frames  than allowed by the internal buffers

* **__CANBUS Rx buffer full**__ – CAN receive buffer is full; some frames may not be received

* **__Priority queue overflow__** – priority queue overflow. This should not occur during normal operation

* **__Priority queue elements__** – current number of elements in the priority queue

* **__Making permanent__** – ECU is writing data (maps and variables) to flash memory (via the "Make Permanent" function)

* **__Real-time autotune active__** – real-time autotune strategy is active

* **__EMU Classic__** – flag indicating that the device is an EMU Classic

* **__Scope buffer used__** – fill level of the Scope buffer. This channel is used by the EMU client when the Scope tool is running

* **__Data changing__** – internal channel used by the EMU client

* **__M32 active__** – indicates the state of the secondary microcontroller

* **__M32 CRC errors__** – indicates communication errors between internal microcontrollers



---

##Effective fuel pressure delta

Effective fuel pressure delta

---

##Idle effectiveFuelPressure DC

Idle effectiveFuelPressure DC

---

##Fuel pressure error

Fuel pressure error

---

##Injectors trim

**Logging channels:

* **Injectors PW ** - base injectors pulse witdth.
* **Injector 1 trim ** - injector 1 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 2 trim ** - injector 2 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 3 trim ** - injector 3 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 4 trim ** - injector 4 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 5 trim ** - injector 5 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 6 trim ** - injector 6 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 7 trim ** - injector 7 trim in percent. A value of 0 means no pulse width correction is applied.
* **Injector 8 trim ** - injector 8 trim in percent. A value of 0 means no pulse width correction is applied.

---

##Fuel

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
* **__Fuel level**__  - actual fuel level 
* __   **Fuel usage**__ - current fuel consumption.
* __   **Fuel used**__ - fuel consumed since engine start.
* __   **Lambda guard status__** - status of the {1} strategy.


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

---

##Fuel acceleration

**Logging channels:

* __   **TPS rate  ** __  - change in the throttle position in %/s
* __   **MAP rate  ** __ -  change in intake manifold pressure in kPa/s. Used when acceleration enrichment is based on the MAP sensor instead of the TPS
* __   **Acc. enrichment %**__ - percentage correction of the fuel mixture; positive values indicate enrichment, negative values indicate leaning. 
* __   **Acc. enrich. async PW**__ - asynchronous enrichment pulse width.
* __   **Acc. enrichment correction**__ - total value of acceleration enrichment corrections from the {1} and {2}



---

##Fuel corrections

**Logging channels:

* __   **Short term trim**__ - current short-term fuel trim adjustment based on Lambda sensor readings.
* __   **Acc. enrichment %**__ - percentage correction of the fuel mixture; positive values indicate enrichment, negative values indicate leaning. 
* __ **Ethanol correction**__ – current fuel dose correction based on ethanol content in the fuel
* __   **Warmup enrichment**__ - enrichment during the engine warm-up phase.
* __   **Afterstart enrichment**__ - mixture enrichment after engine start defined in the  {1} table.
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

##Fuel cut reason

* Analog 4
* frameStamp


---

##Fuel cut source

**Logging channels:

* __   **Fuel cut source 1 and 2**__ -  indicates the strategy responsible for triggering the fuel / injectors cut .


**Fuel cut sources:
* __   **None**__ - no fuel cut is currently active.
* __   **TC**__ - cut is triggered by the active {1} strategy.
* __   **Idle**__ - cut is triggered by the active {2} strategy. 
* __   **LC**__ -  cut is triggered by the active {3} strategy. 
* __   **Rev limiter**__ - cut is triggered by the active {4} strategy. 
* __   **Flat shift**__ - cut is triggered by the active {5} strategy. 
* __   **Pit limiter **__ - cut is triggered by the active {6} strategy. 
* __   **ALS **__ - cut is triggered by the active {7} strategy. 
* __   **Rolling start**__ - cut is triggered by the active {8} strategy. 
* __   **Gear shift**__ - cut is triggered by the active {9} strategy. 
* __   **Overboost**__ - cut is triggered by the active {10} strategy. 
* __   **Oil press. cut**__ - cut is triggered by the active {11} strategy. 
* __   **Stuck throttle**__ - cut is triggered by the active {12} strategy. 
* __   **Start / stop**__ - cut is triggered by the active {13} strategy. 
* __   **Overrun**__ - cut is triggered by the active {14} strategy. 
* __   **Overpressure**__ - cut is triggered by the active {15} strategy (Fuel cut above pressure)
* __   **Per inj. cut **__ - cut is triggered by the active {16} strategy (Per cylinder fuel cut) 
* __   **Cycling idle**__ - cut is triggered by the active {17} strategy. 
* __   **Cut over RPM**__ - cut is triggered by the active {18} strategy (RPM limit). 





---

##Traction control

**Logging channels:
 	
* __** TC status**__ - the current status of the Traction control strategy.

* __** TC intervention**__ - the Traction control strategy is reducing engine torque.

* **__TC torq. reduction**__ - the current torque reduction request.
* __** TC slip**__ - the slip between the axles.
* __** TC slip target**__ - the maximum allowable slip between the axles.

* __** Undriven axle speed**__ - the speed of the vehicle's undriven axle  (defined in {1}).
* __** Driven axle speed**__ - the speed of the vehicle's driven axle (defined in {2}).

* __** TC dRPM**__ - the change in engine RPM corrected by all adjustments.
* __** TC dRPM Raw**__ - the change in engine RPM over a unit of time defined by the Sensitivity parameter.

* __** TC user rotary pos**__ - the position of the rotary switch defined in General/Rotary switch.



**Meaning of  TC statuses:

* **__Disabled__** - the strategy is not activated in the device configuration.

* **__Inactive - switch off__** - the strategy is turned off by the user.

* **__Inactive - below RPM__** - the engine speed is below the minimum RPM defined in the strategy settings.

* **__Inactive - below VSS__** - the vehicle speed is below the minimum speed defined in the strategy settings.

* **__Inactive - gear shift__** - the strategy is inactive due to the activity of the Gear Shift strategy.

* **__Inactive - ESP__** - The strategy is inactive because there is no torque limitation request from the ESP system.

* **__Active - differential__** - the strategy is active in Diff mode.

* **__Active - percent__** - the strategy is active in Percent mode.

* **__Active - RPM based__** - the strategy is active in RPM based mode.
* **__Active - ESP__** - the strategy is active, The strategy is active; the ESP system has issued a request to reduce torque.
<br>


---

##Ignition corr. flags

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
* **__I.Spark cut active__**  - spark cut is active
* **__I.DSG Correction__** -  ignition correction is active due to the DSG Gearbox Control Strategy.
* **__I.Rev Matching__** -  ignition correction is active due to the Rev Matching Strategy.
* **__I.User Function Corr__** -  ignition correction is active due to a User-Defined Function.
* **__I.Spark cut source__**  - the strategy performing spark cut
* **__I.Afterstart lock__**  - ignition is locked by afterst lock strategy ({1})


---

##Acc enrichment correction

Acc enrichment correction

---

##Secondary inj. split

Secondary inj. split

---

##DBW M32 DBW On

DBW M32 DBW On

---

##M32 CRC Erorrs

M32 CRC Erorrs

---

##Sensors status

**Logging channels:

* __   **AC  EVAP status** __ - actual AC evaporator temperature sensor status
* __   **AC pressure status** __ - actual airconditioning sensor status
* __   **Ambient  temp. status** __ - actual mbinet temperature sensor status
* __   **Back pressure status** __ - actual back pressure sensor status
* __   **BARO status** __ - actual baromeric pressure sensor status
* __   **Brake fluid temp. status** __ - actual brake fluid temperature status
* __   **Coolant  pressure status** __ - actual coolant pressue sensor status
* __   **Crankcase pressure status** __ - actual MAP sensor status
* __   **Cylinder head temp. 1 status** __ - actual cylinder head temperature sensor 1 status
* __   **Cylinder head temp. 2 status** __ - actual cylinder head temperature sensor 2 status
* __   **Differentail oil pressure status** __ - differential oil pressure sensor status
* __   **Diffteerential oil temp. status** __ - actual differential oil temperature status
* __   **Engine oil pressure status** __ - actual engine oil sensor status
* __   **Engine oil temp. status** __ - actual engine oil temperature sensor status
* __   **Fuel pressure status** __ - actual fuel pressure sensor status
* __   **Fuel temperature status** __ - actual fuel temperature sensor status 
* __   **Gearbox oil temp. status** __ - actual gearbox oil temperature status
* __   **IAT  status** __ - actual inake air temperature  sensor status
* __   **MAP status** __ - actual MAP sensor status
* __   **Nitrous pressure state** __ - actual status of nitrous pressure sensor
* __**PPS main status**__ - Status of the main TPS sensor
* __**PPS check status**__ - Status of the TPS check sensor
* __   **Post IC temp. status** __ - actual post intercooler temperature sensor status
* __   **Pre IC temp. status** __ - actual pre intercooler temperature sensor status 
* __   **Power steering fluid temp. status** __ - actual power steering temperature sensor status
* __   **Pre throttle boost sensor status** __ - pre throttle boost sensor status
* __**TPS main status**__ - Status of the main TPS sensor
* __**TPS check status**__ - Status of the TPS check sensor
* __   **Wastegate dome pressure sensor status** __ - wastegate dome pressure sensor status



**Meaning of TPS and PPS statuses:

* __**OK**__ - Sensor is functioning correctly
* __**Unassigned**__ - Sensor is not assigned
* __**Short to ground**__ - Voltage from the sensor is below the valid voltage min
* __**Short to 5V**__ - Voltage from the sensor is above the valid voltage max
* __**Check error**__ - The error between the expected and actual voltage of the check sensor is greater than the error tolerance.


**Meaning of other statuses:

* __   **OK** __ -  sensor is operating correctly
* __   **Short to ground** __ -  the voltage from the sensor is lower than the defined minimum value
* __   **Short to 5V** __ -  the voltage from the sensor is higher than the defined maximum value
* __   **Unassigned** __ -  the sensor has not been assigned an analog input
* __   **CAN-BUS** __ -  the sensor value is overridden by user-defined CAN stream




---

##Functions

**Logging channels:

* __   **Fn1 to 12**__ -  indicates the state of the function
* __   **User fn check engine flag**__ -  ndicates whether any of the functions activates the __**Check Engine**__ flag.


---

##Trans-brake

**Logging channels:
* **__Trans-brake state__** - current status of the trans-brake strategy.


**Possible states:
* **__Inactive__** - strategy is inactive
* **__Active__** - startegy is active and transbrake is locked (100% DC)
* **__Active bump__** - startegy is active and performs bump.
* **__Active creep__** - startegy is active and performs creep.


---

##Coolant pressure

Coolant pressure

---

##Fuel corr. flags

**Logging channels:

* __   **F. Short term trim**__  - indicates that {1}  correction is active and currently modifying the injected fuel amount.
* __   **F. ASE correction**__  - indicates that {2}correction is active and currently modifying the injected fuel amount.
* __   **F. Warmup correction**__  - indicates that {3} correction is active and currently modifying the injected fuel amount.
* __   **F. FPR correction**__  - indicates that fuel pressure correction is active and currently modifying the injected fuel amount.
* __   **F. Fuel cut**__  - indicates that a fuel cut is currently active. More information about the reason for the fuel cut can be found in the {4}  log group.
* __   **F. Decelerate correction**__  - indicates that a {5} enrichment (deceleration  condition) is currently active. 
* __   **F. Acelerate correction**__  - indicates that a {6} enrichment is currently active. 
* __   **F. BARO correction**__  - indicates that a Baro correction is currently active. 
* __   **F. Fuel temp. correction**__  - indicates that a {7}  correction is currently active. 

* __   **F. IAT user correction**__  - indicates that a {8}  correction is currently active. 
* __   **F. EGT correction**__  - indicates that a {9}  correction is currently active. 
* __   **F. ALS correction**__  - indicates that a {10} correction is currently active. 
* __   **F. LC correction**__  - indicates that a {11} correction is currently active. 
* __   **F. Flat shift correction**__  - indicates that a {12} correction is currently active. 
* __   **F. Timer correction**__  - indicates that a {13}  correction is currently active. 
* __   **F. Cycling idle correction**__  - indicates that a {14}  correction is currently active. 
* __   **F. Lambda guard**__  - indicates that a {15} correction is currently active. 
* __   **F. Rev matching**__  - indicates that a {16} correction is currently active. 
* __   **F. DSG correction**__  - indicates that a {17}  correction is currently active. 
* __   **F. Custom correction 1 - 3**__  - indicates that a {18}  correction is currently active. 
* __   **F. Nitrous correction**__  - indicates that a {19} correction is currently active. 

---

##Ignition

**Logging channels:

* __   **Ignition angle** __ -  final calculated ignition advance angle. !!⚠Note that {1}  ignition trims and knock sensor corrections are not included here. 
* __   **Ignition from table** __ -  ignition advance angle read from the {2}
* __   **Ignition custom correction 1-3** __ -   Correction values from the {3} tables.
* __   **Dwell time** __ -  actual dwell time of the ignition coil.
* __   **Sprak cut percent** __ - current percentage of ignition events being cut.  
* __   **CAM sync trigger tooth** __ - index of the primary trigger tooth after which synchronization with the camshaft sensor (CAM sync) occurred.
* __   **Trigger sync status** __ -  status of engine synchronization with the trigger signals. See detailed description below.
* __   **CAM1 signal present** __ - indicates whether the ECU is receiving any signal on the CAM1 input.
 * __   **CAM2 signal present** __ -  indicates whether the ECU is receiving any signal on the CAM2 input.
* __   **Trigger error** __ -  channel indicating the presence of errors related to decoding trigger signals. See detailed explanation below.
* __   **Dwell error** __ -  difference between the requested and actual dwell time. This difference may result from engine angular acceleration or trigger decoding errors.
* __   **Executed sparks count** __ -   counter incremented by 1 each time a spark is executed.
* __   **Overdwell** __ -  flag indicating that the requested dwell time was longer than the available time between ignition events. This is especially critical in engines with a distributor at high RPM, where the available time for charging the coil is very short.
* __   **Wasted spark** __ - flag indicating that the ignition system is operating in wasted spark mode.
* __   **Forced low pass filter** __ -  flag indicating that a low-pass filter is forced on the trigger input (typically when there is no signal from the crankshaft).
* __   **Trigger error count** __ -  each trigger error increases the value of this channel by 1. After reaching 255, the counter rolls over and starts again from 0.


**Meaning of Trigger sync status:	

* **NOSYNC** - no signal is present at the primary trigger input..
* **SYNCHRONISING** - signal is present at the primary trigger input. The trigger system is attempting to synchronize. If CAM sync is used, the ECU is also waiting for camshaft synchronization. No fuel injection or ignition is performed in this state.
* **SYNCHRONISED** - he trigger system is fully synchronized. The ECU delivers fuel and executes ignition events.



**Meaning of Trigger error status:	

* **TOOTH OUT OF RANGE** - the expected missing or extra tooth was not detected when it should have been. Check sensor wiring and shielding. Verify trigger edge settings.
* **UNEXPECTED MISSING TOOTH**  - An unexpected missing or extra tooth was detected. This may indicate a trigger wheel concentricity issue. When a __**VR sensor**__ is used for the __**Primary trigger**__, and an unexpected missing tooth error occurs, a 4.7k&#x3a9;-20k&#x3a9; resistor can be connected in series between the sensor output and the primary trigger input. Additionally, enabling the puld-down resistor may help stabilize the signal.
* **FALSE PRIMARY TRIGGER FILTERED** - The primary trigger decoder detected an unexpected pulse that was ignored.
* **FALSE SECONDARY TRIGGER FILTERED** - The camshaft trigger decoder detected an unexpected pulse that was ignored.
* **FALSE CAM2 TRIGGER FILTERED** - The CAM 2 decoder detected an unexpected pulse that was ignored.

---

##Switches BT

**Logging channels:

* __ ** BT Switch 1__ ** - the state of the BT switch 1 from eDash PRO
* __ ** BT Switch 2__ ** - the state of the BT switch 2 from eDash PRO
* __ ** BT Switch 3__ ** - the state of the BT switch 3 from eDash PRO
* __ ** BT Switch 4__ ** - the state of the BT switch 4 from eDash PRO
* __ ** BT Switch 5__ ** - the state of the BT switch 5 from eDash PRO
* __ ** BT Switch 6__ ** - the state of the BT switch 6 from eDash PRO
* __ ** BT Switch 7__ ** - the state of the BT switch 7 from eDash PRO
* __ ** BT Switch 8__ ** - the state of the BT switch 8 from eDash PRO

---

##EDL

!!**⚠IMPORTANT!**: The EDL data logger channels display correct data only when both Tx and Rx terminals are connected to the EDL logger!


**Logging channels:

* __** EDL connected__**  – indicates that the EDL logger is connected and communicating with the EMU.
* __** EDL SD card state __**  – status of the SD card inside the EDL device.
* __** EDL BT state __** – Status of the Bluetooth module in the EDL device.
* __** EDL write errors __** – Number of errors encountered while attempting to write a sector to the SD card. The value is limited to 255. If write errors occur frequently, the SD card should be replaced.
* __** EDL read errors __** – Number of errors encountered while attempting to read a sector from the SD card. The value is limited to 255. If read errors occur, the SD card should be replaced.



**Meaning of EDL SD card state status:	

* ** __No card** __ –  no SD card inserted.
* ** __Mounting** __  – the SD card is being mounting. 
* ** __Idle** __  – the SD card is mounted and ready to log data.
* ** __Recording** __  – data is currently being recorded to the SD card
* ** __Card error** __  – SD card error. The card could not be mounted or written to.


**Meaning of EDL BT state

* ** __Not connected** __ – EDL device is not connected
* ** __Initializing** __ – BT module is being initialized
* ** __Working** __ – BT module is in a working state
* ** __Error** __ – BT module could not be initialized and is not operational

---

##Idle ignition correction

Idle ignition correction

---

