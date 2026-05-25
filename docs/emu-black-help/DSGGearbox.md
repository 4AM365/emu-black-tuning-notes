##DSG Gearbox

The **EMU BLACK** allows control of **DSG DQ250 / DQ500** transmissions for the **PQ35** and **MQB** platforms.

If the transmission is installed in the original vehicle, a key aspect is determining the vehicle ECU coding. This can be done by reading the information from the CAN bus of the original ECU using the **Ecumaster USB2CAN** or **Peak System CAN USB** interface and saving it to disk.

Next, the **Decode VW coding** tool from the **Tools menu** should be used to read the file. The result of this process is the following window:

![DSG/decodeCoding.png](Images/DSG/decodeCoding.png)


By selecting YES, the coding settings will be automatically applied to the DSG transmission configuration options.

If you want to use a DSG transmission in a non-VAG vehicle, a gear shifter is also required. For the PQ35 platform, EMU can emulate both the gear shifter and paddle shifters.

Activating the DSG transmission strategy will automatically enable the necessary CAN transmission (the CAN data stream for PQ35 and MQB differs). As a result, it is possible to select a different vehicle CAN protocol in the {1} options.

The **DSG** transmission requires precise information about the engine torque, making the proper configuration of the torque map crucial. If the reported torque is incorrect, it may cause jerking, clutch slipping, and long-term adaptation issues with the transmission.

During an **upshift**, the transmission sends a request to the ECU to reduce engine torque, which should be executed by retarding the ignition timing. If the torque reduction is too aggressive, it will result in harsh gear changes.

During a **downshift**, the transmission sends a request to the ECU to increase engine RPM to a target value. The gear change occurs when the requested RPM matches the engine speed. Therefore, proper calibration of the {2} is essential.

For auto-adaptation of the transmission, stable idle RPM is required. If the engine speed drops too much during adaptation, the process will be interrupted.

!!⚠For the proper operation of the DSG transmission, the EMU must send the current brake pedal status. In the case of the VAG platform, this signal is transmitted via CAN. If the transmission is installed in another vehicle, the brake pedal must be connected directly to the EMU input. 

!!**⚠It is necessary to check whether the Brake pedal shift channel correctly indicates the brake pedal status.

!!**⚠In the case of a DSG gearbox, a safety feature is implemented to prevent engine start with a gear engaged. Therefore, to start the engine, the brake pedal must be pressed, or the gearbox must be in the N or P position. Otherwise, fuel will not be delivered to the injectors, and the DSG block engine start channel will indicate "Yes.

!!**⚠When working with DSG transmissions, it is necessary to use a diagnostic device (e.g., VCDS) to verify whether all vehicle modules are functioning correctly and whether the transmitted data, such as torque, is accurate.

**Logging channels:

* __**Engine torque**__ - current engine torque (with corrections) in %
* __**Engine actual torque**__ - current engine torque (with corrections) in Nm
* __**Engine torque losses**__  current engine torque losses in %
* __**DSG  torque losses**__  - current DSG gearbox torque losses reported by the gearbox
* __**DSG  combined  load**__ - current value of comined load % from {3} table
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

--

##MQB PLATFORM

When using a DQ250 transmission from the MQB platform outside of an MQB vehicle, the component protection must be removed from the transmission software.

!!**⚠The maximum torque transmitted from the ECU to the transmission is **509** Nm.

The maximum torque achieved by the engine is defined by the VAG MDI torque parameter. 

**DQ250 CONNECTOR PINOUT

|DSG PIN| DESCRIPTION|
|10| CAN-H|
|11|+12V |
|13|+12V |
|15|CAN-L|
|17|Engine speed signal|
|16|GND|
|18|+12 |
|19| GND|

!!⚠For the **MQB** platform, a frequency signal is required, with a frequency in Hz equal to the engine's rotational speed. The EMU is capable of generating such a signal at the **__HBRIDGE 2 A__** output. Without this signal, the transmission will not shift gears properly and will enter emergency mode.


**CAN SWITCHES AND INPUTS ASSIGNEMENT MQB

* Launch control - CAN switch 18
* ESP switch - CAN switch 19
* ASR  switch - CAN switch 20
* Brake switch - Brake pedal switch (must be setup for CAN BUS source)
* Gearbox oil temperature - gearbox oil temp must be unassigned

--

##PQ35 PLATFORM

In the case of PQ35, the torque sent from the ECU to the transmission is expressed as a percentage of the maximum torque.
The maximum torque for the transmission is defined by the **VAG MDI torque** parameter. For the **DQ250** transmission, the maximum torque that can be sent from the ECU is **620 Nm**, whereas for the **DQ500**, it is **1240 Nm**.

**DQ250 CONNECTOR PINOUT

|DSG PIN| DESCRIPTION|
|10| CAN-H|
|11|+12V |
|13|+12V |
|15|CAN-L|
|16|GND|
|18|+12 |
|19| GND|


**DQ500 CONNECTOR PINOUT

|DSG PIN| DESCRIPTION|
|2| +12V|
|6| CAN-H|
|7|CAN-L|
|9|+12V|
|16|GND|


**CAN SWITCHES ASSIGNEMENT PQ35

* CC Up  - CAN switch 8
* CC Down - CAN switch 9
* CC On / Off - CAN swtich 10
* CC Set  - CAN swtich 11
* CC Resume - CAN swtich 12
* CC Cancel - CAN switch 16 
* Tip up - CAN swtich 13
* LC  - CAN swtich 14
* ESP switch - CAN swtich 15



---

[Auto](help://DSGGearbox/DSGGearbox) 
##Parameters

Selecting a **DSG type** other than **__Disable__** triggers the transmission of the appropriate data stream (PQ35 or MQB) onto the CAN bus. This allows you to select a different vehicle's stream in the CAN Bus settings, enabling integration with vehicles retrofitted with a **DSG gearbox**. 

!!⚠Everything will function correctly as long as there are no conflicts between the CAN IDs of the data frames sent by the EMU, the DSG gearbox, and the vehicle's original CAN frames.

{#1}




---

[Auto](help://DSGGearbox/DSGGearbox) 
##Emulation

**!!⚠Emulation works only with PQ35 platform!

When installing a DSG gearbox in a non-VW group vehicle, this option enables the emulation of different VW modules required by the gearbox (eg. for the launch control)

{#1}



---

[Auto](help://DSGGearbox/DSGGearbox) 
##Paddle shifters

**!!⚠Paddle shifter emulation works only with PQ35 platform!

The DSG paddle shifters strategy enables the activation of the paddle shift module emulation, which sends information via the CAN bus to the gearbox requesting an upshift or downshift. This function should not be activated if the vehicle is already equipped with a paddle shift module, as it would cause a conflict on the CAN bus.


{#1}


---

[Auto](help://DSGGearbox/DSGGearbox) 
##Gear selector

**!!⚠Gear selector works only with PQ35 platform!

If the original gear selector is missing, it is possible to emulate it. There are two emulation options. One is using a rotary switch, and the other, recommended method, is using the ECUMASTER CAN keypad.

Emulating the gear lever prevents the possibility of changing gears from P without the brake pedal pressed and changing to P and R while the vehicle is moving (VSS &gt; 0). When using a rotary switch, the selected gear will be chosen regardless of its position. In the case of a keyboard, the protection prevents changing gears and the currently illuminated key.

The current gear set on the selector can be checked in the log channel __ **DSG emulated selector pos.

**ROTARY SWITCH:
When using a rotary switch, it should be configured in the Sensor and Inputs section. Positions from 0 to 4 will be used in the order P, R, N, D, S. Rotary switch values above 4 will be treated as 4.

** KEYPAD:
For a keyboard, firstly define a group of 5 radio buttons to ensure that only one key at a time will be pressed. In the KEY parameters, select the option DSG selector emulation. Next, in the Gear selector parameters, assign keys to specific gears. The figures below illustrate an example configuration of the keypad and Gear selector.

![keypadEmulator.png](Images/keypadEmulator.png)





---

[Auto](help://DSGGearbox/DSGGearbox) 
##Post blip level cal.

The post blip level table defines throttle position in post blip phase. This value can be altered by rev matching strategy in the case the RPM are higher than target RPM.
To configure this table, the throttle positions must be determined experimentally so that the unloaded engine reaches the RPM values defined on the X-axis.



---

[Auto](help://DSGGearbox/DSGGearbox) 
##Blip level cal.

The Blip level calibration table defines the throttle position during the blip phase.
The values in the table should be determined experimentally to achieve the target RPM (**__DSG blip RPM target__**) as quickly as possible for different gears and various differences between the actual and target RPM.

The picture below shows a real-world example where the blip was either too strong or too weak.
![dgs_blip_cal.png](Images/dgs_blip_cal.png)

The picture below shows a perfect rev match.
![dgs_blip_cal_ideal.png](Images/dgs_blip_cal_ideal.png)








---

[Auto](help://DSGGearbox/DSGGearbox) 
##Engine Torque

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://DSGGearbox/DSGGearbox) 
##Engine torque

The **Engine torque** table is used to define the engine torque as a function of load and RPM. These values should be experimentally gathered on a dyno to accurately reflect the engine's actual torque output. Incorrect values in the table may cause driveability issues and problems with the gearbox's TCU adaptation process.

!!**⚠It is important to check with the VCDS tool if the values from the ECU (Engine actual torque) match the torque read by the gearbox!



---

[Auto](help://DSGGearbox/DSGGearbox) 
##Engine torque losses

The Engine torque losses table defines the mechanical torque losses of the engine. 

!!**⚠We recommend setting the entire table to a value of 0.


---

[Auto](help://DSGGearbox/DSGGearbox) 
##Gear selector cal.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://DSGGearbox/DSGGearbox) 
##Combined load

By default, the X-axis of the {1} table uses TPS (for Alpha-N strategy) or MAP (for Speed Density strategy). In the case of the Speed Density strategy, it is possible to use the **__Combined load**__ table, which allows the X-axis of the {2} table to depend on a combination of **TPS** and **MAP**. This enables more precise torque definition, especially in low load conditions.
To make the engine torque calculation strategy use this table , the **Use combined load** option must be enabled in {3}


---

[Auto](help://DSGGearbox/DSGGearbox) 
##Ign. torque reduction

When the **__Up shift torque reduction__** parameter is set to **Advanced**, this table defines the ignition retard angle for a given load (**__MAP, TPS, or Combined Load__**) and the torque reduction request from the transmission.
The choice of the load axis depends on the selected fueling strategy (**__Speed Density / Alpha N__**) or the **__Combined Load__** option in {1}



---

[Auto](help://DSGGearbox/DSGGearbox) 
##Cut torque reduction

When the **__Up shift torque reduction__** parameter is set to **Advanced**,  this table defines the percentage of ignition cuts for a given load (**__MAP, TPS, or Combined Load__**) and the torque reduction request from the transmission.
The choice of the load axis depends on the selected fueling strategy (**__Speed Density / Alpha N__**) or the **__Combined Load__** option in {1}

---

[Auto](help://DSGGearbox/DSGGearbox) 
##DSG

{#1}


---

