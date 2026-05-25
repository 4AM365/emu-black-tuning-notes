##Functions

The user has 12 functions at their disposal, which can be used to create complex strategies based on logical operations. There are 32 **__operators**__ (logical conditions) available that can be combined using OR and AND logical functions.

A function can be a **__virtual**__ function, whose result can be used to activate strategies in the EMU, control device outputs, set the rev limiter value, adjust the ignition timing, or activate the check engine light.

**  !! ⚠ Please note! The function evaluation is performed at a frequency of 25 Hz (same as the log channels), which means that the delay between meeting the function’s conditions and the change of its output value can be up to 40 ms.

To define a function, double-click on the desired function in the main tree view with the left mouse button. A configuration window for the function will appear. 
To add a function operator, double-click on the **...** symbol.

![functions_definition_window.png](Images/functions_definition_window.png)


* **Function name** - a function name defined by the user (maximum 8 characters). It will be displayed everywhere the function can be assigned.


* **Output** - if the function is meant to control an EMU output, this output should be assigned in the output field. If the function is only to set its value (or for example, the rev limiter), select "**__Virtual**__" as the output.


* **Invert output** - checking this option inverts the state of the EMU selected output (it does not invert the function result).


* **Action**  - specifies what action the function should perform. Regardless of the selected action, the function value in the log will be either 0 or 1 depending on its state.


The following actions are available:

 *     **Set output only** - sets the output value. If "Virtual" is selected as the output, only the function value will change.
* **Set rev limiter** - allows setting the rev limiter when the function value is 1 (true). The rev limiter RPM will be defined by the "Value" parameter. The rev limiter strategy will always choose the lowest RPM value if the rev limiter is activated from multiple sources.
* ** Set ignition correction ** - if the function value is 1 (true), it allows introducing an ignition timing correction defined in the "Value" field. Negative values cause ignition retard, positive values advance the ignition.
* **Set check engine** - if the function value is 1 (true), the check engine light will be activated.


!! ** Note: Regardless of the selected action, if the Output field value is not "Virtual," the selected device output will also be set.

Individual operators can be combined using **AND** connectors to create a group of operators. These groups can be combined using **OR** logical functions, enabling the creation of complex conditions to activate functions.

Right-clicking on a selected operator will bring up a menu with options:

* **Remove operator** - removes the operator from the function.
* **Move down** - moves the operator to the group of operators below.
* **Move up** - moves the operator to the group of operators above.
* **Remove all operators** - removes all operators for the given function.


The status of all functions can be observed in the log (channels **__Fn 1 to Fn 12**__) and on the lower status bar (fields F1 to F12). Active functions (with a value of 1) are highlighted in green. Functions are evaluated sequentially from **__F1**__ to **__F12,**__ which can be important when creating functions that use the results of other functions.


**!!All information about log channels bitfields and enumerations can be found in {1}  
--

##** Operators **

!!The following description contains **false** and **true** notions. False means a value of **'0'** (zero), and true means any value other than zero (e.g. **'1'** or **0.01V**).

**__Testing operations

![functions_testingoperators.png](Images/functions_testingoperators.png)

**__ Operations__** 

**Is True** 
Returns 1 when the Channel value is true (non-zero); 0 otherwise.

**Is False**
Returns 1 when the Channel value is false (zero); 0 otherwise.

** True delay ** - defines the time the result of operation is true to change the operatr state to true
** False delay ** - defines the time the result of operation is true to change the operatr state to false

--


**__Comparing operations

![functions_compareOperators.png](Images/functions_compareOperators.png)

**__ Operations__** 

** Equal 
Returns 1 when the Channel value = Constant; returns 0 otherwise.

** Not Equal 
Returns 1 when the Channel value is not equal to Constant; returns 0 otherwise.

** Less 
Returns 1 when the Channel value <Constant; returns 0 otherwise.


**Less or Equal 
Returns 1 when the Channel value <= Constant; returns 0 otherwise.


**Greater 
Returns 1 when the Channel value > Constant; returns 0 otherwise.

** Greater or Equal 
Returns 1 when the Channel value >= Constant; returns 0 otherwise.

** Channel #1** - defines the logging channel  that is used for comparing 
** Constant** - defines the constant that is used for compare with the selected channel 
** True delay ** - defines the time the result of operation is true to change the operatr state to true
** False delay ** - defines the time the result of operation is true to change the operatr state to false

--


**__Logic operations

![functions_logicOperators.png](Images/functions_logicOperators.png)


**__ Operations__** 

**And** 
 Returns 1 when the values of both Channel #1 and Channel #2 are true (non-zero);
returns 0 otherwise.

**Or** 
Returns 1 when at least one of the channels, i.e. Channel #1 or Channel #2 is true
(non-zero), returns 0 otherwise.

**Xor (Exclusive Or)** 
Returns 1 only when exactly one of the channels Channel #1 or Channel#2, has a value of true (non-zero), returns 0 otherwise.

** Channel #1** - defines logging channel  that is used as 1st argument for logic function
** Channel #2** - defines logging channel  that is used as 2nd argument for logic function
** True delay ** - defines the time the result of operation is true to change the operatr state to true
** False delay ** - defines the time the result of operation is true to change the operatr state to false

--

**__Bitwise operators

![functions_bitwiseOperators.png](Images/functions_bitwiseOperators.png)

All information about log channels bitfields and enumerations can be found in {2}  

**And bitwise**
This operator performs operations on bits between the value of **__Channel**__ AND **__Constant**__. This can be used to test status flags.

**Xor bitwse**
This operator performs operations on bits between the value of **__Channel**__ XOR  **__Constant**__. 

** Channel #1** - defines the logging channel  that is used for bitwise logic operation 
** Constant** - defines the 16 bits constant that is used for bitwise logic operation with the selected channel 
** True delay ** - defines the time the result of operation is true to change the operatr state to true
** False delay ** - defines the time the result of operation is true to change the operatr state to false

--
** Signal generating

**Flash** 

![functions_FlashOperator.png](Images/functions_FlashOperator.png)

This operation generates impulses so long as the __**Channel__** is __**true__** (non-zero).
When the __**Channel__** value assumes __**false__** (zero), the operation returns the value 0.
When high state appears on the __**Channel__** channel (non-zero value), the __**Flash__**
operation starts cycling between the value of 1 (duration defined by __**Time on__**) and
the value 0 (duration defined by __**Time off__**). When the __**Channel__** value is __**false__** (zero), the operation will immediately start returning 0, thus interrupting the cycle.


**Pulse** 

![functions_pulseOperator.png](Images/functions_pulseOperator.png)

This operation generates N pulses following appearance of a trigger edge.
When the selected edge appears (__**Rising__** or __**Falling__**) on the __**Channel__** impulse
generation will start. The number of impulses is determined by the __**Count__** parameter.
Each impulse has an active phase (then the operation returns 1) and a non-active
phase (the operation returns 0).
The __**Retrigger__** parameter determines if the appearance of a trigger edge during
impulse generation will cause the process to restart or if it will be ignored.

--

**__State-storing operations

**Set-Reset Latch

![functions_setResetOperator.png](Images/functions_setResetOperator.png)

The operation sets a new or returns the previous one according to the settings of
the two input channels: __**Set Channel__** and __**Reset Channel__**.

| Set channel value | Reset channel value | Operation value|
| true (non-zero)    | false (0)  | 1 |
|false (0) |true (non-zero) |0|
|true (non-zero) |true (non-zero) |0|
|false (0) |false (0) |previous value|

The initial value of this operation following starting the device can be defined using
the __**Default State__** parameter


**Toggle

![functions_toggleOperator.png](Images/functions_toggleOperator.png)

Toggle changes the state between 0 and 1 each time the selected __**Edge__** (**__Rising__** or
__**Falling__**) appears on the __**Channel__**.
__**Set channel__** allows setting the value to 1, and __**Reset channel__** resets the value to 0.
The initial value of this operation following starting the device can be defined using
the __**Default State__**.

|Toggle channel |Set channel value |Reset channel value |Operation value|
|Rising | false (0)| false (0) |state change|
|Falling |false (0)| false (0)| previous state|
|x |true (non-zero) |false (0)| 1|
|x |x |true (non-zero)| 0|

x - regardless of condition
The table uses the __**Toggle__** channel with an __**Edge: Rising__**


** Change

![functions_changedOperator.png](Images/functions_changedOperator.png)

If the value of the selected log channel changes more than the **__Threshold**__ value  the pulse of the duration of **__Time on**__  will be generated and the new value for comparision will be acquired.


** Hysteresis

![functions_hysteresisOperator.png](Images/functions_hysteresisOperator.png)

When **__Polarity**__ is set to **__Above**__, hysteresis returns 1 when source channel's value exceeds **__Upper Value**__, and remains in high state until source channel's value drops below **__Lower Value__**, then drops to low state (0).
If **__Polarity**__ is set to **__Below Hysteresis**__, it works in the opposite way.

--




---

[Auto](help://Functions/Functions) 
##Fn 1

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 2

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 3

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 4

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 5

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 6

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 7

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 8

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 9

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 10

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 11

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn 12

The description of the function's operation can be found in the help section for the item {1}.

The list below represents all enumerations and bitfields, along with their associated logging channels.

<br>**Channel(s):** Gear shift state
** Enumeration**
* Disabled **0** 
* Not active **1** 
* Rejected - clutch engaged **2** 
* Rejected - gearbox sensor error **3** 
* Rejected - leaver sensor error **4** 
* Rejected - low RPM **5** 
* Rejected - downshift high RPM **6** 
* Rejected - gear unknown **7** 
* Rejected - gear neutral **8** 
* Rejected - gear reverse **9** 
* Rejected - VSS too low **10** 
* Rejected - upshift tps too low **11** 
* Rejected - downshift tps too high **12** 
* Upshift - shift **13** 
* Upshift - recovery **14** 
* Downshift - shift **15** 
* Downshift - recovery **16** 
* Rearm **17** 

<br>**Channel(s):** Paddle shift states
** Bitfield **
* Preload **1** 
* Solenoid up **2** 
* Solenoid down **4** 
* Performing upshift **8** 
* Performing downshift **16** 

<br>**Channel(s):** TC status
** Enumeration**
* Disabled **0** 
* Inactive - switch off **1** 
* Inactive - below RPM **2** 
* Inactive - below VSS **3** 
* Inactive - gear shift **4** 
* Inactive - ESP  **5** 
* Active - differential **6** 
* Active - percent **7** 
* Active - RPM based **8** 
* Active - ESP **9** 

<br>**Channel(s):** I.TC correction , Priority queue overflow , Real time autotune active , VTEC active , EMU Classic , Fuel Cut , Idle control active , Overdwell , Shift light , Nitrous active , DBW characteristic 2 , F.ASE correction , F.Warmup correction , F.IAT user corr. , F.EGT correction , F.Custom correction 1 , F.BARO correction , F.FPR correction , F.Fuel temp. correction , F.ALS correction , DBW control line active , F.LC correction , F.Decelerate correction , F.Accelerate correction , F.Fuel cut , F.Short term trim , F.Flat shift correction , F.Timer correction , I.Idle , I.KS correction , I.Custom correction 1 , I.LC correction , I.Rev limiter correction , I.Nitrous correction , F.Cycling idle correction , I.Custom correction 2 , I.Pit limit correction , I.Rolling LC correction , I.Ignition angle lock , I.ALS correction , I.Custom correction 3 , I.FS correction , I.Timer correction , Boost out of margin , CAM1 signal present , CAM2 signal present , AC Clutch , F.Custom correction 3 , F.Custom correction 2 , Cruise control engine start block , F. Lambda guard , I. Lambda guard , Boost lambda guard corr. , Gear unknown , EDL connected , Diff ctrl active , Diff ctrl oil pump active , F.Rev matching , I. Spark cut active , Brake pedal switch , Boost output disabled , WBO is calibrating , Wasted spark , Idle airflow custom corr. active , Paddle up , Paddle down , Clutch pedal switch , TC intervention , DSG clutch error , DSG fault , DSG torque reduction , DSG blip , DSG shift up , DSG shift down , I.DSG correction , F.DSG correction , Idle force open loop , EWP active , Cruise control is in margin , SOVERFLOW , Rev. match active , Rev. match armed , DSG LC , CANBUS overload , I.Rev Matching , Forced low pass filter , CANBUS Rx buffer full , M32 active , Lambda is valid , F.Nitrous correction , DSG block engine start , N switch , I.User fn correction , User fn check engine flag , R switch , Performing downshift , Performing upshift , Data changing , Ign. afterstart lock , M32 reset , Rx switch (active high) , Diff. ctrl pump error
** Enumeration**
* NO **0** 
* YES **1** 

<br>**Channel(s):** Outputs test state , Pit limiter state , Fn 1 , Fn 2 , Fn 3 , Fn 4 , Fn 5 , Fn 6 , Fn 7 , Fn 8 , Fn 9 , Fn 10 , Fn 11 , Fn 12 , Coolant fan , Fuel pump state
** Enumeration**
* Inactive **0** 
* Active **1** 

<br>**Channel(s):** INJ outputs
** Bitfield **
* INJ 6 **32** 
* INJ 5 **16** 
* INJ 4 **8** 
* INJ 3 **4** 
* INJ 2 **2** 
* INJ 1 **1** 

<br>**Channel(s):** Trigger error
** Bitfield **
* TOOTH OUT OF RANGE **1** 
* UNEXPECTED MISSING TOOTH **2** 
* CAM SYNC ERROR **4** 
* CAM SYNC ERROR, TOOTH OUT OF RANGE **8** 
* FALSE SEC TRIGGER, FILTERED **16** 
* FALSE PRIM TRIGGER, FILTERED **32** 
* FALSE CAM2 TRIGGER, FILTERED **64** 

<br>**Channel(s):** ALS state
** Enumeration**
* Disable **0** 
* Not armed **1** 
* Armed **2** 
* Active **3** 
* Exit **4** 
* Inactive above CLT **5** 
* Inactive below CLT **6** 
* Inactive above EGT **7** 
* Inactive below VSS **8** 

<br>**Channel(s):** Check engine code
** Bitfield **
* CLT **1** 
* IAT **2** 
* MAP **4** 
* WBO **8** 
* EGT1 **16** 
* EGT2 **32** 
* EGT ALARM **64** 
* KNOCK **128** 
* FF SENSOR **256** 
* DBW **512** 
* FPR **1024** 
* DIFF CTRL **2048** 
* DSG **4096** 
* EWG **8192** 
* OILP **16384** 

<br>**Channel(s):** CANBUS State
** Enumeration**
* BUS OK **0** 
* MODULE DISCONNECTED **1** 
* BUS ERROR **2** 

<br>**Channel(s):** AUX otuputs
** Bitfield **
* AUX 6 **1** 
* AUX 5 **2** 
* AUX 4 **4** 
* AUX 3 **8** 
* AUX 2 **16** 
* AUX 1 **32** 

<br>**Channel(s):** CLT status , IAT status , AC evap status , Pre IC temp. status , Diff. oil temp. status , Fuel temp. status , Gearbox oil temp. status , Power steering fluid temp. status , Engine oil pressure status , Fuel press. status , Engine oil temp. status , Diff. oil press. status , Coolant fluid press. status , Crankcase press. status , Post IC temp. status , Back press. status , AC press. status , MAP status , BARO status , Brake fluid temp. status , Cyl. head temp. 1 status , Ambient temp. status , Gearbox sensor status , Pre throttle boost sensor status , Cyl. head temp. 2 status , Gear lever load cell sensor status , EWG pos sensor status , Wastegate dome press. status , Nitrous pressure status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* CAN-BUS **4** 

<br>**Channel(s):** CAN Switch 1 , CAN Switch 2 , CAN Switch 3 , CAN Switch 4 , CAN Switch 5 , CAN Switch 6 , CAN Switch 7 , CAN Switch 8 , MUX switch 1 , MUX switch 2 , MUX switch 3 , Switch 1 , Switch 2 , Switch 3 , CAN Switch 9 , CAN Switch 10 , CAN Switch 11 , CAN Switch 12 , CAN Switch 13 , CAN Switch 14 , CAN Switch 15 , CAN Switch 16 , Nitrous stage 1 output , User switch 1 , User switch 2 , User switch 3 , User switch 4 , User switch 5 , User switch 6 , User switch 7 , User switch 8 , CAN Switch 17 , CAN Switch 18 , CAN Switch 19 , CAN Switch 20 , Nitrous stage 2 output
** Enumeration**
* ON **1** 
* OFF **0** 

<br>**Channel(s):** Latching SW1 , Latching SW2 , Latching SW3 , Latching SW4
** Enumeration**
* LSW_A **0** 
* LSW_B **1** 
* LSW_C **2** 
* LSW_D **3** 

<br>**Channel(s):** Boost source
** Enumeration**
* MAP **0** 
* Pre throttle sensor **1** 

<br>**Channel(s):** LC State
** Enumeration**
* Inactive **0** 
* Wait for activation **1** 
* Active prestage **2** 
* Active **3** 
* Wait for exit **4** 
* Exit **5** 

<br>**Channel(s):** Trigger sync status
** Enumeration**
* NOSYNC **0** 
* SYNCHRONISING **1** 
* SYNCHRONISED **2** 

<br>**Channel(s):** ECU State
** Enumeration**
* UNKNOWN **0** 
* INACTIVE **1** 
* CRANKING **2** 
* AFTERSTART **3** 
* RUNNING **4** 
* DELAYED TURN OFF **5** 

<br>**Channel(s):** Overrun status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Enter ignition ramp **2** 
* Active **3** 
* Exit ignition ramp **4** 
* Blocked by idle **5** 
* Blocked by ALS **6** 
* Blocked by blip **7** 
* Blocked by CC **8** 
* Blocked by rev match **9** 
* Blocked by DBW CAN control **10** 
* Disabled by switch **11** 

<br>**Channel(s):** Autotune rejection reason
** Enumeration**
* Accepted **0** 
* Rejected RPM **1** 
* Rejected MAP **2** 
* Rejected TPS **3** 
* Rejected transient **4** 
* Rejected overrun **5** 
* Rejected fuel cut **6** 
* Rejected spark cut **7** 
* Rejected acc enrich **8** 
* Rejected WBO **9** 

<br>**Channel(s):** CAM2 input level , CAM1 input level
** Enumeration**
* Low **0** 
* High **1** 

<br>**Channel(s):** DSG clutch
** Enumeration**
* Engaged **1** 
* Disengaged **0** 

<br>**Channel(s):** DSG mode
** Enumeration**
* UNKNOWN **0** 
* P **2** 
* R **3** 
* N **4** 
* D **5** 
* S **6** 
* M **7** 
* TT_PL **8** 
* TT_MI **9** 
* FAULT **10** 

<br>**Channel(s):** ECU reset cause
** Enumeration**
* Power on **0** 
* Watchdog **1** 
* Software reset **2** 
* JTAG **3** 
* Other **4** 

<br>**Channel(s):** DSG emulated selector pos
** Enumeration**
* P **0** 
* R **1** 
* N **2** 
* D **3** 
* S **4** 

<br>**Channel(s):** Overrun tables index , VE table index , VVT CAM1 table index , VVT CAM2 table index
** Enumeration**
* Table 1 **0** 
* Table 2 **1** 

<br>**Channel(s):** DBW Override
** Bitfield **
* DC **1** 
* TARGET **2** 

<br>**Channel(s):** Engine protection code
** Bitfield **
* CLT **1** 
* EGT **2** 
* FPRD **4** 
* OILTL **8** 
* OILTH **16** 
* OVEB **32** 
* STT **64** 
* OILP **128** 

<br>**Channel(s):** TPS main status , TPS check status , PPS main status , PPS check status
** Enumeration**
* Unassigned **0** 
* OK **1** 
* Short to ground **2** 
* Short to 5V **3** 
* Check error **4** 

<br>**Channel(s):** DBW Target source
** Enumeration**
* Target table **0** 
* Override **1** 
* Idle **2** 
* Idle blend **3** 
* DSG blip **4** 
* CAN control **5** 
* Launch control **6** 
* Cruise control **7** 
* Rev limiter **8** 
* Overrun **9** 
* Flat shift **10** 
* Rev matching **11** 
* Pit limiter **12** 
* ALS **13** 
* Rolling start **14** 
* Gear shift **15** 

<br>**Channel(s):** Idle state
** Enumeration**
* Inactive **0** 
* Armed **1** 
* Active **2** 
* Cranking **3** 
* DBW blend **4** 
* Afterstart delay **5** 
* Cycling idle **6** 
* DC overriden **7** 

<br>**Channel(s):** Cruise control state
** Enumeration**
* Disabled **0** 
* Inactive under vss **1** 
* Inactive **2** 
* Suspended **3** 
* Active **4** 
* Active with PID **5** 

<br>**Channel(s):** VVT CAM1 status , VVT CAM 2 status
** Enumeration**
* Disabled **0** 
* Inactive - start delay **1** 
* Inactive - below RPM **2** 
* Inactive - below CLT **3** 
* Active - DC override **4** 
* Active **5** 

<br>**Channel(s):** Fuel cut source 1
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overboost **512** 
* Oil press. cut **1024** 
* Stuck throttle **2048** 
* Start / stop **4096** 
* Overrun **8192** 
* Overpressure **16384** 

<br>**Channel(s):** Spark cut source
** Bitfield **
* TC **1** 
* Idle **2** 
* LC **4** 
* Rev limiter **8** 
* Flat shift **16** 
* Pit limiter **32** 
* ALS **64** 
* Rolling start **128** 
* Gear shift **256** 
* Overrun **512** 
* Cycling idle **1024** 
* DSG **2048** 

<br>**Channel(s):** Knocking cylinders
** Bitfield **
* CYL 1 **1** 
* CYL 2 **2** 
* CYL 3 **4** 
* CYL 4 **8** 
* CYL 5 **16** 
* CYL 6 **32** 
* CYL 7 **64** 
* CYL 8 **128** 

<br>**Channel(s):** Knock action status
** Enumeration**
* Disabled **0** 
* Inactive - conditions not met **1** 
* Inactive - no knock **2** 
* Active **3** 

<br>**Channel(s):** Rev. limiter target source
** Enumeration**
* None **0** 
* CLT **1** 
* IAT **2** 
* Oil temp **3** 
* Custom **4** 
* Ethanol content **5** 
* User function **6** 
* CAN BUS **7** 
* Fuel pressure prot. **8** 
* Launch control **9** 
* Rolling start **10** 

<br>**Channel(s):** Active rev. limiter
** Enumeration**
* None **0** 
* Limiter 1 **1** 
* Limiter 2 **2** 
* RPM fuel cut **3** 
* Launch control **4** 
* Rolling start **5** 

<br>**Channel(s):** Rolling start state
** Enumeration**
* Inactive **0** 
* Conditions not met **1** 
* Active **2** 
* Exit **3** 

<br>**Channel(s):** FF status
** Enumeration**
* Disabled **0** 
* OK **1** 
* Sensor error **2** 
* Connection error **3** 

<br>**Channel(s):** Gear lever action
** Enumeration**
* No action **0** 
* Up shift request **1** 
* Down shift request **2** 
* Error **3** 
* Unassigned **4** 

<br>**Channel(s):** Fuel cut source 2
** Bitfield **
* Per inj. cut **1** 
* Cycling idle **2** 
* Cut over RPM **8** 

<br>**Channel(s):** Paddle hold switches
** Bitfield **
* Paddle up **1** 
* Paddle down **2** 
* N switch **4** 
* R switch **8** 

<br>**Channel(s):** Paddle shift status
** Enumeration**
* OK **0** 
* Rejected - RPM **1** 
* Rejected - VSS **2** 
* Rejected - clutch **3** 
* Rejected - gear out of range **4** 
* Rejected - gear unknown **5** 

<br>**Channel(s):** DBW cal. tool state
** Enumeration**
* Disable **0** 
* TPS sensor dir **1** 
* TPS return to limp **2** 
* Find 10% **3** 
* Pre find 90% **4** 
* Find 90% **5** 
* Find 85% **6** 
* Return to limp **7** 
* Find -30% **8** 
* Find -80% **9** 
* Find -75% **10** 
* Write data to ECU **11** 
* PID tuning **12** 

<br>**Channel(s):** DBW HW state
** Bitfield **
* Error no signal **1** 
* Error wrong freq **2** 
* DBW mode **4** 

<br>**Channel(s):** Trans-brake state
** Enumeration**
* Inactive **0** 
* Active **1** 
* Active bump **2** 
* Active creep **3** 

<br>**Channel(s):** HBRIDGE 1 mode
** Enumeration**
* Outputs **0** 
* DBW **1** 

<br>**Channel(s):** HBRIDGE 2 mode
** Enumeration**
* Outputs **0** 
* EWG **1** 
* MQB signal on output A **2** 

<br>**Channel(s):** Active timers
** Bitfield **
* Timer 1 active **1** 
* Timer 2 active **2** 
* Drag timer active **4** 

<br>**Channel(s):** Nitrous stage 1 state , Nitrous stage 2 state
** Enumeration**
* Inactive **0** 
* Active delay **1** 
* Active LC **2** 
* Active timer **3** 
* Post active **4** 
* Finished **5** 

<br>**Channel(s):** Lambda guard status
** Enumeration**
* Disabled **0** 
* Active **1** 
* Lean cond. waiting **2** 
* Not active **3** 
* RPM not in range **4** 
* MAP not in range **5** 
* TPS not in range **6** 
* WBO sensor not valid **7** 
* CLT too low **8** 
* Transient fuel **9** 

<br>**Channel(s):** EDL SD card state
** Enumeration**
* No card **0** 
* Mounting **1** 
* Idle **2** 
* Recording **3** 
* Card error **4** 

<br>**Channel(s):** EDL BT state
** Enumeration**
* Not connected **0** 
* Initialisation **1** 
* Working **2** 
* Error **3** 

<br>**Channel(s):** ALS tables set
** Enumeration**
* 1 **0** 
* 2 **1** 


---

[Auto](help://Functions/Functions) 
##Fn #1

User-defined logical functions allow users to create custom operations to suit specific needs and requirements


---

