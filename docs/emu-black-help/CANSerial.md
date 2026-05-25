##CAN, Serial

The **__EMU BLACK**__ device supports the **__CAN 2.0B**__ bus, enabling communication with other devices. The CAN bus (__Control Area Network__) was developed for communication between devices in automotive applications. It is characterized by a very simple structure (only two wires) and very high resistance to interference. In modern cars, there can be dozens of different electronic modules communicating using the CAN bus.

Data frames are transmitted over the network, whose topology should look like the following diagram:

<center> ![CAN/topology.png](Images/CAN/topology.png) </center>

In automotive applications, typical data transmission speeds on the CAN bus are 1Mbps, 500kbps, and 250kbps. Depending on the speed, the following conditions must be met:

**For a speed of 1Mbps:

* The maximum distance of the connection wire between the bus and a node must be less than 30cm.
* The maximum bus length is 40m.
* The maximum number of nodes is 30.


**For a speed of 500kbps:

* The maximum distance of the connection wire between the bus and a node must be less than 30cm.
* The maximum bus length is 100m.
* The maximum number of nodes is 30.


Regardless of the speed, the CAN bus must have termination resistors of 120 Ohms at both ends. Additionally, all connections in the bus area must be made using twisted pair cables.

**!!The data transfer speed on a single bus must be identical for all devices.

**!!Failure to follow these rules will lead to improper functioning of the CAN bus and communication problems.

A CAN frame consists of an identifier (ID), the number of transmitted bytes (DLC), and the actual data. Depending on the bus type, the identifier can be 11-bit (0x0-0x7FF) or 29-bit (0x0-0x1FFFFFFF). The number of data bytes can range from 0 to 8.

![CAN/canFrame.png](Images/CAN/canFrame.png)

**Logging channels:

* __ **CANBUS State**__  - the status of the CAN bus.
* __ **CANBUS Load**__  - the processing load of CAN data being sent from the device.
* __ **CANBUS Overload**__  - the requested amount of data to be sent on the CAN bus exceeds the device's buffer size. Some frames may not have been sent.
* __ **CANBUS Rx Buffer Ful**__  - the requested amount of data to be received on the CAN bus exceeds the device's buffer size. Some frames may not have been received.


**Meaning of CANBUS States:

* __ *BUS OK**__ - no communication errors.
* __ *BUS ERROR**__ - CAN bus error. Possible causes may include incorrect bus speed selection, lack of termination, error in connecting CANL and CANH, or ID collision.

 Detailed EMU Black stream information is provided in the tables below. All multi-byte values use Little Endian byte order.

**EMU stream base ID+0 (default: 0x600) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0..1 | RPM | 16-bit U | 0 - 16000 | 1/1 | 1 | 0 | RPM |
| 2 | TPS | 8-bit U | 0 - 100 | 1/2 | 0.5 | 0 | % |
| 3 | IAT | 8-bit S | -40 - 127 | 1/1 | 1 | 0 | C |
| 4..5 | MAP | 16-bit U | 0 - 600 | 1/1 | 1 | 0 | kPa |
| 6..7 | Injector PW | 16-bit U | 0 - 50 | 1/62 | 0.016129 | 0 | ms |

**EMU stream base ID+1 (default: 0x601) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0..1 | AIN #1 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |
| 2..3 | AIN #2 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |
| 4..5 | AIN #3 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |
| 6..7 | AIN #4 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |

**EMU stream base ID+2 (default: 0x602) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0..1 | VSPD | 16-bit U | 0 - 400 | 1/1 | 1 | 0 | km/h |
| 2 | BARO | 8-bit U | 50 - 130 | 1/1 | 1 | 0 | kPa |
| 3 | Oil Temperature | 8-bit U | 0 - 160 | 1/1 | 1 | 0 | C |
| 4 | Oil Pressure | 8-bit U | 0 - 12 | 1/16 | 0.0625 | 0 | bar |
| 5 | Fuel Pressure | 8-bit U | 0 - 12 | 1/16 | 0.0625 | 0 | bar |
| 6..7 | CLT | 16-bit S | -40 - 250 | 1/1 | 1 | 0 | C |

**EMU stream base ID+3 (default: 0x603) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0 | Ignition Angle | 8-bit S | -60 - 60 | 1/2 | 0.5 | 0 | deg |
| 1 | Dwell Time | 8-bit U | 0 - 10 | 1/20 | 0.05 | 0 | ms |
| 2 | Lambda | 8-bit U | 0 - 2 | 1/128 | 0.0078125 | 0 | lambda |
| 3 | Lambda Correction | 8-bit U | 75 - 125 | 1/2 | 0.5 | 0 | % |
| 4..5 | EGT1 | 16-bit U | 0 - 1100 | 1/1 | 1 | 0 | C |
| 6..7 | EGT2 | 16-bit U | 0 - 1100 | 1/1 | 1 | 0 | C |

**EMU stream base ID+4 (default: 0x604) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0 | Gear | 8-bit U | 0 - 7 | 1/1 | 1 | 0 |  |
| 1 | ECU Temperature | 8-bit S | -40 - 120 | 1/1 | 1 | 0 | C |
| 2..3 | Battery Voltage | 16-bit U | 0 - 20 | 27/1000 | 0.027 | 0 | V |
| 4..5 | Error Flag<sup> 1 </sup> | 16-bit | bitfield | 1/1 | 1 | 0 |  |
| 6 | FLAGS 1<sup> 2 </sup> | 8-bit | bitfield | 1/1 | 1 | 0 |  |
| 7 | Ethanol Content | 8-bit U | 0 - 100 | 1/1 | 1 | 0 | % |

**EMU stream base ID+5 (default: 0x605) **
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0 | DBW Position | 8-bit U | 0 - 100 | 1/2 | 0.5 | 0 | % |
| 1 | DBW Target | 8-bit U | 0 - 100 | 1/2 | 0.5 | 0 | % |
| 2..3 | TC DRPM RAW | 16-bit S | 0 - 1000 | 1/1 | 1 | 0 |  |
| 4..5 | TC DRPM | 16-bit U | 0 - 400 | 1/1 | 1 | 0 |  |
| 6 | TC Torque Reduction | 8-bit U | 0 - 100 | 1/1 | 1 | 0 | % |
| 7 | PIT Limiter Torque Reduction | 8-bit U | 0 - 100 | 1/1 | 1 | 0 | % |

**EMU stream base ID+6 (default: 0x606)** 
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0..1 | AIN #5 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |
| 2..3 | AIN #6 | 16-bit U | 0 - 5 | 5/1024 | 0.0048828125 | 0 | V |
| 4 | OUTFLAGS1<sup> 3 </sup> | 8-bit | bitfield | 1/1 | 1 | 0 |  |
| 5 | OUTFLAGS2<sup> 4 </sup> | 8-bit | bitfield | 1/1 | 1 | 0 |  |
| 6 | OUTFLAGS3<sup> 5 </sup> | 8-bit | bitfield | 1/1 | 1 | 0 |  |
| 7 | OUTFLAGS4<sup> 6 </sup> | 8-bit | bitfield | 1/1 | 1 | 0 |  |

**EMU stream base ID+7 (default: 0x607)** 
| Byte |             Channel                 | Data Type |     Range     | Multiplier/Divider |      Factor     | Offset |     Unit     |
| 0..1 | Boost Target | 16-bit U | 0 - 600 | 1/1 | 1 | 0 | kPa |
| 2 | PWM#1 DC | 8-bit U | 0 - 100 | 1/1 | 1 | 0 | % |
| 3 | DSG Mode<sup> 7 </sup> | 4-bit U | enumeration | 1/1 | 1 | 0 |  |
| 4 | Lambda Target | 8-bit U | 0 - 1 | 1/100 | 0.01 | 0 | lambda |
| 5 | PWM#2 DC | 8-bit U | 0 - 100 | 1/1 | 1 | 0 | % |
| 6..7 | Fuel Used | 16-bit U | 0 - 255 | 1/100 | 0.01 | 0 | liter |

<sup> 1 </sup>Bits of **Error Flag** bitfield
| Bit index |      Error name      |                              Description                           |
| 0 | ERR_CLT | Coolant temperature sensor failed |
| 1 | ERR_IAT | IAT sensor failed |
| 2 | ERR_MAP | MAP sensor failed |
| 3 | ERR_WBO | Wide band oxygen sensor failed |
| 4 | ERR_EGT1 | EGT sensor #1 failed |
| 5 | ERR_EGT2 | EGT sensor #2 failed |
| 6 | ERR_ALARM | EGT too high |
| 7 | KNOCKING | Knock detected |
| 8 | FFSENSOR | Flex Fuel sensor failed |
| 9 | ERR_DBW | Drive by wire failure |
| 10 | ERR_FPR | Fuel pressure relative error |

<sup> 2 </sup>Bits of **FLAGS1** bitfield
| Bit index |       Flag name      |                              Description                           |
| 0 | GEARCUT | Gearcut active |
| 1 | ALS | ALS active |
| 2 | LC | Launch control active |
| 3 | IDLE | Is in idle state |
| 4 | TABLE SET | 0 - using table set #1, 1 - using table set #2 |
| 5 | TC INTERVENTION | 1 - traction control intervention |
| 6 | PIT LIMITER | Pit limiter active |

<sup> 3 </sup>Bits of **OUTFLAGS1** bitfield
| Bit index |       Flag name      |                              Description                           |
| 0 | PO1 | Parametric output #1 state |
| 1 | PO2 | Parametric output #2 state |
| 2 | PO3 | Parametric output #3 state |
| 3 | PO4 | Parametric output #4 state |
| 4 | PO5 | Parametric output #5 state |
| 5 | VPO1 | Virtual output #1 state |
| 6 | VPO2 | Virtual output #2 state |
| 7 | VPO3 | Virtual output #3 state |

<sup> 4 </sup>Bits of **OUTFLAGS2** bitfield
| Bit index |       Flag name      |                              Description                           |
| 0 | CANSW1 | CAN switch #1 state |
| 1 | CANSW2 | CAN switch #2 state |
| 2 | CANSW3 | CAN switch #3 state |
| 3 | CANSW4 | CAN switch #4 state |
| 4 | CANSW5 | CAN switch #5 state |
| 5 | CANSW6 | CAN switch #6 state |
| 6 | CANSW7 | CAN switch #7 state |
| 7 | CANSW8 | CAN switch #8 state |

<sup> 5 </sup>Bits of **OUTFLAGS3** bitfield
| Bit index |       Flag name      |                              Description                           |
| 0 | SW1 | Switch #1 state |
| 1 | SW2 | Switch #2 state |
| 2 | SW3 | Switch #3 state |
| 3 | MUXSW1 | MUX switch #1 state |
| 4 | MUXSW2 | MUX switch #2 state |
| 5 | MUXSW3 | MUX switch #3 state |
| 6 | LC MAP SET | Current set of launch control parameters |
| 7 | ALS MAP SET | Current set of ALS parameters |

<sup> 6 </sup>Bits of **OUTFLAGS4** bitfield
| Bit index |       Flag name      |                              Description                           |
| 0 | FPS | Fuel pump state |
| 1 | CF | Coolant fan state |
| 2 | ACCLUTCH | AC clutch state |
| 3 | ACFAN | AC fan state |
| 4 | NITROUS | Nitrous active |
| 5 | STARTER_REQ | Starter motor request (from start / stop strategy) |
| 6 | BOOST MAP SET | Current set of boost parameters |

<sup> 7 </sup>Values for channel: **DSG Mode**
|     Value     |       Description      |
| 2 | P |
| 3 | R |
| 4 | N |
| 5 | D |
| 6 | S |
| 7 | M |
| 15 | fault |




---

[Auto](help://CANSerial/CANSerial) 
##User defined CAN

In addition to supporting predefined devices, it is possible to send and receive information from the EMU via the CAN bus. You can define up to 8 custom frames (Rx, Tx). 

!!**⚠Unlike in firmware V2, in V3 software, it is possible to receive user-defined CAN frames even when the vehicle CAN stream is selected.

**Adding a User Defined CAN Frame

To add a user-defined CAN frame, go to the User Define CAN Stream window and select **Add new...**(1)  in the message column.

![CAN/userCAN.png](Images/CAN/userCAN.png)


![CAN/userCAN_addMessage.png](Images/CAN/userCAN_addMessage.png)

**Message ID (HEX)** - the CAN ID in hexadecimal format. Ensure the frame being sent has a unique CAN ID for the CAN bus to avoid collisions that could cause bus errors.

**DLC** - frame length in bytes.

**Extended ID** - in the CAN standard, there are two types of CAN IDs: 11-bit and 29-bit (Extended). If you want to use frames with a 29-bit CAN ID, select the extended option.

**RX** - specifies if the defined CAN frame will be used to receive information by the EMU BLACK.

**Update interval** - for **TX** frames (transmission), this parameter specifies how often the frame will be sent on the CAN bus.

**Timeout** - for **RX** frames, this is the time after which, if the next frame is not received, the frame data will take on the default values defined below.

**Byte[X] (HEX)** the default byte X value of the CAN frame in hexadecimal format. For sending data, this will be the value sent if no logging channel is assigned to the byte. For receiving data, these values will be used during initialization and if the next frame is not received within the specified timeout.

After adding the desired frame, you can define the logging channels you wish to export or import to/from the EMU and their format. To do this, in the frame area, select **Add new....** (2)
--
![CAN/userCAN_addChannel.png](Images/CAN/userCAN_addChannel.png)

** User CAN Message Tx Options

**Log channel** - select the log channel to send.

**Data type** - the format of the number sent in the data.
* **__8 bits unsigned**__- the sent value is in 8-bit unsigned format, ranging from **0 to 255**. Used for channels that only accept positive values, e.g., Analog In.
* **__8 bits signed**__ - the sent value is in 8-bit signed format, ranging from **-127 to 128**. Used for channels that accept both positive and negative values (e.g., IAT).
* **__16 bits signed big endian:**__ - the sent value is in 16-bit signed format (2 bytes) with a range of -32767 to 32768. Big-endian (also known as Motorola) means the higher byte is sent first.
* **__16 bits signed little endian:**__ - the sent value is in 16-bit signed format (2 bytes) with a range of -32767 to 32768. Little-endian (also known as Intel) means the lower byte is sent first.
* **__16 bits unsigned big endian:**__ - the sent value is in 16-bit unsigned format (2 bytes) with a range of 0 to 65535. Big-endian (Motorola) sends the higher byte first.
* **__16 bits unsigned little endian**__ - the sent value is in 16-bit unsigned format (2 bytes) with a range of 0 to 65535. Little-endian (Intel) sends the lower byte first.


**Byte pos** - the byte position in the frame data where the logging channel will be sent. If you selected a 16-bit format, the logging channel will occupy two bytes.

**Multiplier** - the value by which the sent logging channel value will be multiplied. For example, when choosing the Lambda channel and a multiplier of 100, if Lambda is 1, the sent value will be 100; if Lambda is 0.81, the sent value will be 81, etc.

**Divider** - the value by which the sent logging channel value will be divided. For example, when choosing the RPM channel and a divider of 4, if the RPM is 1000, the sent value will be 250.

**Offset** - the value added to the output value sent on the CAN.

**Output Value = Log channel value \* Multiplier / Divider + Offset.


**User CAN Message Rx Options

For **RX messages**, variables are initialized with default values from the message. If the user selects a timeout and the EMU does not receive the defined CAN frame within the specified time, the variables will take on the default values.

**Input value = Data from CAN \* Multiplier / Divider + Offset

**Input channels format:

* **__Wheel speeds**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__CAN Analog inputs:**__ - 1/255 V per bit, e.g., 100 = 1.96 V.
* **__GPS speed**__ - 2 km/h per bit, e.g., 100 = 200 km/h.
* **__Driven speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__Undriven speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__Vehicle speed**__ - 1/16 km/h per bit, e.g., 160 = 16 km/h.
* **__Rev limiter target CAN BUS**__ - 1 RPM per bit, e.g., 3000 = 3000 RPM.
* **__Rotary switch**__ - 1 per bit, e.g., 6 = Rotary switch position 6.
* **__Lambda 1**__ - 1/1000 per bit. 1000 = 1 &#x3bb. If 0, Lambda is not valid
* **__Lambda 2**__ - 1/1000 per bit. 1000 = 1 &#x3bb. If 0, Lambda is not valid
* **__Lateral G**__ - 1/64  per bit. e.g. 64 = 1G
* **__CLT**__ - 1&#xb0;C  per bit. e.g. 64 = 64&#xb0;C. When CLT is used as CAN Input  the **__CLT status__** log channel is set to CAN-BUS
* **__IAT**__ - 1&#xb0;C  per bit. e.g. 32 =32&#xb0;C. When IAT is used as CAN Input  the **__IAT status__** log channel is set to CAN-BUS




---

[Auto](help://CANSerial/CANSerial) 
##Serial

The EMU device features built-in RS232 serial communication (receiving/transmitting), allowing communication with external devices. Connection involves linking the **__EMU's TX**__ output to the **__RX**__ input of the external device. A shielded cable should be used.

**!!⚠For EDL-1 the firmware 1.21 or newer is required!

{#1}


---

[Auto](help://CANSerial/CANSerial) 
##CAN setup

!!**⚠All devices using the CAN bus must operate at the same speed! Incorrect topology and termination of the CAN bus can cause communication errors!

{#1}

**OBD 2 supported PIDs

| PID(hex) | PID(dec) | Description|
|0x1 |PID 01|MIL status, number of DTCs. Reported errors must be marked in {1} options. Reported DTCs: **__CLT, IAT, MAP, DBW, FlexFuel sensor__**|
|0x3 |PID 03|Fuel system status. Informs about lambda short term correction status.|
|0x5 |PID 05|CLT value [&#xb0;C]|
|0x6 |PID 06|Short term fuel trim [%]|
|0xa |PID 10|Fuel pressure [kPa]|
|0xb |PID 11|Intake manifold pressure [kPa]|
|0xc |PID 12|RPM|
|0xd |PID 13|Vehicle speed [km/h]|
|0xe |PID 14 |Timing advance [&#xb0;]|
|0xf |PID 15|IAT [&#xb0;C]|
|0x11|PID 17|Throttle position [%])|
|0x13 |PID 19|Oxygen sensor presence|
|0x14 |PID 20|Oxygen sensor 1 voltage [V] and fuel trim [%]|
|0x1f |PID 31|Engine runtime [s]|
|0x24 |PID 36|Oxygen sensor 1 equivalence ratio [&#x3bb;]|
|0x42 |PID 66|Battery voltage [V] |
|0x44 |PID 68|Fuel equivalence ratio target [&#x3bb;]|
|0x52 |PID 82|Ethanol content[%]|

--
** Streams descriptions


** AEM

CAN stream compatible with AEM standard.

Transmited IDs: ** 0x01F0A000, 0x01F0A003, 0x01F0A004

Outputs:
* RPM, CLT, IAT, TPS  
* Check engine flag
* Fuel pressure, Oil pressure
* Lamnda, Lambda target
* Vehicle speed
--

** Alfa Romeo GT 937/947

The immo frame (0x40) must be read from OEM ECU and send using user defined CAN.

Transmited IDs: ** 0x361, 0x3a1, 0x561

Inputs:
* Wheels speed

Outputs:
* RPM
* Check engine indicator
* CLT
* Water high temperature indicator
* Low oil pressure indicator (oil pressure sensor must be connected to EMU)
* Cruise control indicator

--

** Audi / VW

Transmited IDs: ** 0x280, 0x284, 0x288, 0x380, 0x480, 0x488, 0x580, 0x588, 0x48A

Outputs:

* Coding
* CLT, IAT, TPS, PPS
* Torque
* Brake switch
* Check engine, battery lamp
* Coolant FAN 
* Boost, oil temp 


Inputs:

* Oil temperature
* Brake switch (set CAN BUS as brake switch input in {2} configuration)
* AC pressure (set None as AC pressure input in {3} configuration)
* AC clutch 
* AC coolant fan request 
* Wheel speeds  
* PWM coolant fan 
* CC Up (CAN switch 8)
* CC Down (CAN switch 9)
* CC On / Off (CAN swtich 10)
* CC Set (CAN swtich 11)
* CC Resume (CAN swtich 12)
* CC Cancel (CAN switch 16)
* Tip up  (CAN swtich 13)
* LC  (CAN swtich 14)
* ESP switch (CAN swtich 15)
--

** BMW E46, E46 M3, Z4

Transmited IDs: ** 0x316, 0x329, 0x545

Outputs:
* RPM, CLT
* Oil temp (oil pressure sensor must be connected to EMU)
* Check engine indicator
* Battery lamp
* Shift light (M power version only)
* Oil temperature (oil temperature sensor must be connected to EMU)
* Low oil pressure indicator (oil pressure sensor must be connected to EMU)


Inputs:
* Brake switch (set CAN BUS as brake switch input in {4} configuration)
* DSC (CAN switch 20)
* AC request (CAN switch 19)
* Wheels speed
-- 
** BMW E90 series

Transmited IDs: **0xA8, 0xA9, 0xAA, 0x1D0 

Outputs:
* RPM, CLT
* Oil temp (oil pressure sensor must be connected to EMU)
* Check engine indicator
* Battery lamp
* Shift light (M power version only)
* Oil temperature (oil temperature sensor must be connected to EMU)
* Low oil pressure indicator (oil pressure sensor must be connected to EMU)


Inputs:
* Wheels speed
--
** Citroen C2 

Transmited IDs: ** 0x208, 0x348, 0x488

Outputs:
* RPM, 
* CLT
* Overtemperature 


Inputs:
* Wheels speed
* Brake switch (set CAN BUS as brake switch input in {5} configuration)
* Hand brake (CAN switch 18)
* ESP swtich (0.5 sec pulse of CAN switch 19) 
* AC request (CAN switch 20)
--

** Colt CZ 

Transmited IDs: ** 0x308, 0x608, 

Outputs:
* RPM, 
* Overtemperature indicator (>100C)
* Oil pressure indicator
* Coolant fan control
* Check engine lamp

Inputs:
* Wheels speed
* Brake switch (set CAN BUS as brake switch input in {6} configuration)
* AC request (CAN switch 2)
* Ignition on switch (CAN switch 3)
* Starter request (CAN switch 4)
--


** FIAT GRANDE PUNTO 2008

You need to connect a reverse gear sensor to the EMU device because information about its status is sent via the CAN bus to activate the reverse light.

Transmited IDs: ** 0xA28A001, 0xC7CA001, 0xA1CA001, 0xA18A001, 0x618A001, 0x628A001, 0x10A001

Inputs:
* Wheels speed 
* CAN Switch 12  - Brake status from BCM
* CAN Switch 13  - Drive style (Normal, City) 
* CAN Switch 14  - AC request
* CAN Switch 15 - Hand brake 
* CAN Switch 16 - Crank request 
* CAN Switch 17  - Cruise conrol on
* CAN Switch 18 - Cruise control resume
* CAN Switch 19 - Cruise control speed up
* CAN Switch 20 - Cruise control speed down


Outputs:
* Immo
* Speedo
* Odometer
* Boost pressure
* Shift light
* CLT
* Oil pressure lamp
* Engine status
* CLT warning lamp
* Reverse gear status
* Check engine status
* Cruise control light
* Clutch pedal status

--
** FIAT 500 EURO 5

You need to connect a reverse gear sensor to the device because information about its status is sent via the CAN bus to activate the reverse light.

Transmited IDs: **  0xC7CA001, 0xA1CA001, 0xA18A001, 0x618A001, 0x628A001, 0x10A001

Inputs:
* Wheels speed 
* CAN Switch 14 - AC request
* CAN Switch 15 - Hand brake 
* CAN Switch 16 - Crank request 
* Rotary swtich CAN 4 - Drive style (Normal, City, Sport, Winter, Eco, TracPlus, Race)


Outputs:
* Immo
* Speedo
* Odometer
* Boost pressure
* Shift light
* CLT
* Oil pressure lamp
* Engine status
* CLT warning lamp
* Reverse gear status
* Check engine status
* Cruise control light
* Clutch pedal status

--
** FIAT 500 EURO 6 / US VERSION

You need to connect a reverse gear sensor to the device because information about its status is sent via the CAN bus to activate the reverse light.

Transmited IDs: **  0xC7CA001, 0xA1CA001, 0xA18A001, 0x618A001, 0x628A001, 0x10A001

Inputs:
* Wheels speed 
* CAN Switch 12  - Brake status from BCM
* CAN Switch 14 - AC request
* CAN Switch 15 - Hand brake 
* CAN Switch 16 - Crank request 
* Rotary swtich CAN 4 - Drive style (Sport , City , Normal)


Outputs:
* Immo
* Speedo
* Odometer
* Boost pressure
* Shift light
* CLT
* Oil pressure lamp
* Engine status
* CLT warning lamp
* Reverse gear status
* Check engine status
* Cruise control light
* Clutch pedal status

--
** FORD FIESTA MK6
** FORD FOCUS  RS / ST

Transmited IDs:  **0x40, 0x200, 0x201, 0x205, 0x231, 0x270, 0x280, 0x420, 0x428, 0x4F1

Inputs:
* Brake switch (set CAN BUS as brake switch input in {7} configuration)
* Clutch pedal
* CAN Switch 1 - AC request
* CAN Switch 2 - ????
* CAN Switch 3 - TC On / Off
* CAN Switch 4 - Hand brake
* CAN Switch 5 - Front window heater
* CAN Switch 6 - Rear window heater
* Latching switch 4 - Comfort (LSW_A), Normal(LSW_B), Sport(LSW_C)


Outputs:
* RPM
* CLT
* Battery indicator
* Check engine indicator
* Oil pressure indicator
* Shift light
* Odometer
* Oil temperature
* Boost

--
** FORD FIESTA MK7

Transmited IDs:  **0xfd, 0x201,  0x420

Inputs:
???

Outputs:
* RPM
* CLT
* Battery indicator
* Check engine indicator
* Oil pressure indicator
* Odometer

--
** FORD MONDEO  MK 4

Transmited IDs:  **0xfd, 0x201,  0x420

Inputs:
* Wheels speed
* Clutch pedal
* Brake switch (set CAN BUS as brake switch input in {8} configuration)
* Cruise control reset (CAN switch 1)
* Cruise control off  (CAN switch 2)
* Cruise control on (CAN switch 3)
* Cruise control speed up (CAN switch 4) 
* Cruise control speed down (CAN switch 5)
* AC switch (CAN switch 6)
* ESP switch (CAN switch 7)


Outputs:
* RPM
* CLT
* Battery indicator
* Check engine indicator
* Oil pressure indicator
* Odometer

--

** LANCER EVO X

You need to connect a reverse gear sensor to the EMU device because information about its status is sent via the CAN bus to activate the reverse light.

Transmited IDs: ** 0x210, 0x212, 0x308, 0x312, 0x415, 0x608, 0x6fa, 0x763, 

Inputs:
* Wheels speed 
* Steering angle (please define sterring angle offset in {9}
* Yaw rate 
* Lateral G
* AC pressrure 
* AC switch (CAN switch 0) 
* DIfferential mode (Rotary swtich CAN 1)


Outputs:
* CLT
* Coolant fan control
* RPM
* TPS
* Torque estimation
--

** LOTUS ELISE S3, ELISE S3 CUP

Transmited IDs: ** 0x400, 0x114, 0x102,  0x401(CUP only)

Inputs:
* Wheels speed 


Outputs:
* CLT
* RPM
* TPS
* TC control status
* Dashboard information PIT LIM, LAUNC, TC xx (CUP only)
* CLT too high (CUP only)
* Oil pressure indicator (when any pressure sensor connected)
* Shift light based on shift light settings 
* Pit limiter indicator (CUP only)
* Check engine lamp
* Sport mode
* Cruise control 
* Brake and clutch siwtch
* Fuel level 
* Torque estimation for ESP system
--
** MAZDA MX-5 NC

Transmited IDs:  *0x201, 0x420

Outputs:
* RPM
* Vehicle speed
* Check engine
* Low battery voltage
* CLT
* Low oil pressure 


Inputs:
* Clutch switch
* Brake switch
* Hand brake (CAN swtich 20)
--
** MAZDA RX-8

Transmited IDs:  **0x41, 0x201, 0x300,  0x420, 0x50D, 0x620, 0x630

Outputs:
* RPM
* Vehicle speed
* Check engine
* Low battery voltage
* CLT
* Low oil pressure
* ABS control frame


Inputs:
* Wheels speeds


**__ABS**__

To ensure the ABS module functions correctly, an appropriate frame with ID 0x620 must be sent. Unfortunately, this frame differs between ABS modules. The available "ABS models" in the configuration (Model 2 to Model 5) are all the models we have managed to test. In case of an ABS error, you should try different models. If none of the models work, the only way to activate the ABS is to check the original CAN stream from the ECU (e.g., using USB TO CAN) and find the frame 0x620. In this case, you should select User defined as the model and send the frame 0x620 using **__User defined CAN**__.

**__POWER STEERING__**

The **__Emulate power steering__** option allows sending the power steering message (ID 0x300) if the power steering has been removed from the car. Otherwise, enabling this option will cause a CAN BUS error due to ID clash.
--
** MINI COOPER R50 / R53

Transmited IDs: ** 0x316, 0x329, 0x336, 0x545, 0x565, 0x61F

Outputs:
* RPM, CLT
* Oil temp (oil pressure sensor must be connected to EMU)
* Check engine indicator
* Battery lamp, TC lamp,  Cruise control lamp
* Shift light
* Oil temperature (oil temperature sensor must be connected to EMU, Chrono pack only)
* Low oil pressure indicator (oil pressure sensor must be connected to EMU)
* Fuel consumption


Inputs:
* Brake switch (set CAN BUS as brake switch input in {10} confiuration)
* DSC (CAN swtich 20)
* AC request (CAN switch 19)
* Wheels speed
--
** OPEL CORSA VXR

In the case of the Corsa VXR, you need to define the input to which the clutch switch ({11}) is connected and select the input to which the reverse gear switch is connected (Reverse gear switch in CAN configuration).

Transmited IDs: **0xC9,  0x1BC, 0x1F5, 0x4D1, 0x4C1, 0x1C1, 0x3D1, 0x1BD, 0x3E9, 0x3C9, 0x3F9, 0x2C5

Inputs:
* Wheels speed 
* CAN Switch 1  - AC request
* CAN Switch 2  - Crank request


Outputs
* Odometer
* RPM 
* Starter
* Fuel consumption
* Check engine
* Oil pressure
* Shift light
* Reverse lamp
* CLT

-- 
** POLARIS RZR 2024

Transmited IDs: ** 18FECA00, 0x18FEFC00, 0x0CFF2100, 0x18F00600, 0x1CFDDF00, 0x0CFF6600, 0x18FEEE00, 0x18F00500, 0x18FF6D00, 0x18FEE500, 0x18FEF100

Outputs:

* CLT
* RPM 
* VSS
* Odometer
* Gear (-1 - R, 0 - N, 1 - P,  2 - L, 3 - H)
* Front diff lock (require a switch connected to EMU)
* 4WD (requires a switch connected to EMU)
* Drive mode (requires a rotary switch or multistate latching switch connected to EMU)
* Fuel level
* Check engine light
* Overtemperature light (> 110C)

--
** PORSCHE 997.1 (2004-2008)

Transmited IDs: **0x242,  **0x441

Inputs:
* Wheels speed 
* Brake pedal
* Clutch pedal
* AC pressure
* CAN Switch 15 - CC enable
* CAN Switch 16 - CC cancel
* CAN Switch 16 - CC increase
* CAN Switch 16 - CC decrease
* CAN Switch 16 - CC resume
* CAN Switch 20 - AC request


Outputs:
* RPM 
* TPS
* Coolant fan DC
* Engine running status
* Check engine lamp
* Oil temeprerature
* Oil pressure


!!To control the **Coolant Fan** via CAN communication, set the coolant fan output to CAN BUS in the {12} configuration, and in the PWM control field, choose 100 Hz.

--
** RENAULT CLIO 3 RS

The immo frame (0x511) must be read from OEM ECU and send using user defined CAN.

** To send the frame read from the OEM ECU containing the immobilizer code, you need to select the "Send IMMO code (0x511)" option.

By default the following frame is sent (id, len, data) 
 0x511, 7, 0x0, 0x5D, 0x42, 0x8A, 0x90, 0x80, 0x06, 0x0

Transmited IDs: ** 0x511, 0x551, 0x181, 0x161, 0x1f9 **

Inputs:
* AC request (CAN Swtich 20)
* Wheels speed


Outputs:
* RPM
* Check engine indicator
* CLT
* Fuel consumption
* AC clutch
* Coolant fan control
* Immo
* ECU state
--
** SUBARU GH

Transmited IDs: ** 0x410, 0x411, 0x600, 0x601**

Inputs:
* Wheels speed
* 
* 
* 


Outputs:
* RPM
* CLT
* SI drive
* Cruise control status
* Brake switch
* Clutch switch


--
** Toyota GT86 /  Suabru BRZ

Transmited IDs: **  0x140, 0x141, 0x142, 0x144, 0x360, 0x361, 0x4c1**

Inputs:
* Wheels speed
* Brake switch (set CAN BUS as brake switch input in {13} configuration)
* CAN Switch 1 - Sport mode
* CAN Switch 2 - Traction control switch
* CAN Switch 3 - Reverse gear
* CAN Switch 4 - Handbrake
* CAN Switch 6 - Cranking request (Start button)
* CAN Switch 7 - AC clutch
* CAN Switch 8 - AC request


Outputs:
* RPM
* CLT
* ABS initialisation
* Power steering 
* Brake switch
* Fuel usage


---

[Auto](help://CANSerial/CANSerial) 
##CAN switch board

The **__Ecumaster CAN switch board**__ is an additional device that allows for the connection of extra switches and analog signals and their transmission via the CAN bus. The **__Ecumaster Wireless Racing Panel**__ also supports the **__CAN switch board**__ data format.

The CAN switch boards in version V1 using CAN ID 0x666 and V3 using **__CAN IDs 0x640, 0x641, 0x642**__ are supported.

For more information regarding the CAN switch board and Wireless Racing Panel, please visit www.ecumaster.com.

<center> ![CAN/csbv3.png](Images/CAN/csbv3.png) </center>

<center> ECUMASTER CAN Swtich board </center> 


<center> ![CAN/wireless.png](Images/CAN/wireless.png) </center>
<center> Ecumaster wireless Racing Panel </center>



---

[Auto](help://CANSerial/CANSerial) 
##PMU keyboard

The PMU keyboard enables the operation of a keyboard defined in the PMU device.

To read the state of keys of a connected and configured keyboard in the PMU, you need to select the option **__'Export keyboard state and buttons over CAN'__** in the keyboard settings and choose CAN ID to be 0x662.

In the EMU, keys can be assigned to CAN switch inputs or Latching switches if the key has more than 2 states.

{#1}


---

[Auto](help://CANSerial/CANSerial) 
##CAN keypad

EMU BLACK has the capability to support ECUMASTER keypads in various available sizes. To utilize the keypad, it should be connected to the CAN bus, and it is crucial to ensure that the CAN-BUS speed of the keypad matches that of the ECU.

![cankeypad.png](Images/cankeypad.png)


---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANkeypad) 
##Keypad

For configuring the keypad's speed and base ID, the ECUMASTER UBS2CAN interface and Ecumaster Light Client software can be employed. More information can be found on the ECUMASTER website in the CAN Keyboards and Light Client sections.

![cankeypadLightCLient.png](Images/cankeypadLightCLient.png)

CAN Keypads communicate with EMU using the CAN OPEN protocol. To ensure proper communication, the configuration of the keypad's base address in EMU should align with the base address configured in the keypad. The base address is 0x600 + CANOpen node ID. Supported CANOpen node IDs are from 0x15 to 0x1F.
Below is the connection diagram for connecting the keypad to the EMU BLACK device.

![cankeypadSchematic.png](Images/cankeypadSchematic.png)


{#1}


---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANkeypad) 
##Keys 1-8

Keys configuration allows for configuring the behavior, colors, and mapping to EMU switches for each key. The parameter __ KEY #X __ specifies the state of the EMU switch to be changed by a given key. The options include __CAN SW #X __ or Latching switches.

The parameter __KEY #X__ type defines the key's behavior upon pressing. The following options are available:

* **Non-latching red, green, blue, yellow** - pressing the button changes its color and the assigned EMU switch state. Upon release, the button returns to the initial state, and the assigned EMU switch turns off.

* **Latching red, green, blue, yellow** - pressing the button changes its color and the assigned EMU switch state. Upon release, the button remains active until pressed again, turning off the switch.

* **Latching red, green, blue, yellow blinking** - similar to the above, but the button pulsates in the selected color when in the on state.

* **Multistate Yellow-Green, Multistate Green-Red, Multistate Green-Blue** - pressing the button changes both the state and color. The button has three states: off, 1 (first color), and 2 (second color), and should be mapped to a Latching switch.

* **Radio button 1 Red, Green, Blue** - radio buttons create a group where only one can be pressed at a time. This function could be used, for example, for a gear selector in a DSG transmission (Park, Reverse, Neutral, Drive, Sport).

* **Radio button 2 Red, Green, Blue**  - a second group of radio buttons with the same functionality as radio button group 1.

* **Indicator Red, Green, Blue, Green Red** - is used to display a specific color on the key depending on the value of the Fn function. In the KEY #X field, you should select the function that will control the color of the button. The Indicator button itself has no other function besides displaying color.


**KEY #X of the FN #X type serves solely and exclusively to change the color of the Indicator-type button. In the case of other types of keys (KEY #X Type), selecting a function will result in the key not functioning.

**KEY #X of the DSG selector emulation type is exclusively used to emulate the gear selector of a DSG transmission and should be selected for Radio buttons. More information regarding the emulation of the DSG gearbox/gear selector can be found in the DSG Gearbox/Gear selector configuration.

The parameter __Key #X__ default state indicates the initial state of the button when the device is powered on.


---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANkeypad) 
##Keys 9-15

Keys configuration allows for configuring the behavior, colors, and mapping to EMU switches for each key. The parameter __ KEY #X __ specifies the state of the EMU switch to be changed by a given key. The options include __CAN SW #X __ or Latching switches.

The parameter __KEY #X__ type defines the key's behavior upon pressing. The following options are available:

* **Non-latching red, green, blue, yellow** - pressing the button changes its color and the assigned EMU switch state. Upon release, the button returns to the initial state, and the assigned EMU switch turns off.

* **Latching red, green, blue, yellow** - pressing the button changes its color and the assigned EMU switch state. Upon release, the button remains active until pressed again, turning off the switch.

* **Latching red, green, blue, yellow blinking** - similar to the above, but the button pulsates in the selected color when in the on state.

* **Multistate Yellow-Green, Multistate Green-Red, Multistate Green-Blue** - pressing the button changes both the state and color. The button has three states: off, 1 (first color), and 2 (second color), and should be mapped to a Latching switch.

* **Radio button 1 Red, Green, Blue** - radio buttons create a group where only one can be pressed at a time. This function could be used, for example, for a gear selector in a DSG transmission (Park, Reverse, Neutral, Drive, Sport).

* **Radio button 2 Red, Green, Blue**  - a second group of radio buttons with the same functionality as radio button group 1.

* **Indicator Red, Green, Blue, Green Red** - is used to display a specific color on the key depending on the value of the Fn function. In the KEY #X field, you should select the function that will control the color of the button. The Indicator button itself has no other function besides displaying color.


**KEY #X of the FN #X type serves solely and exclusively to change the color of the Indicator-type button. In the case of other types of keys (KEY #X Type), selecting a function will result in the key not functioning.

**KEY #X of the DSG selector emulation type is exclusively used to emulate the gear selector of a DSG transmission and should be selected for Radio buttons. More information regarding the emulation of the DSG gearbox/gear selector can be found in the DSG Gearbox/Gear selector configuration.

The parameter __Key #X__ default state indicates the initial state of the button when the device is powered on.

---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANkeypad) 
##Keys

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANswitchboard) 
##Configuration

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://CANSerial/CANSerial) [Auto](help://CANSerial/CANswitchboard) 
##Switches

The selection of the **__EMU**__ channel that will be assigned to the **__Switch 2**__ input on the **__CAN switch board**__.

The operating mode of **__Switch 2 input**__.
* **__Non-latching**__: the assigned channel will have a value of 1 when the button is pressed.
* **__Latching**__: with a single press of the button, the assigned channel will have a value of 1. The next press will change the button state to 0.
* **__Multistate**__: each press of the button changes its state to the next one. The switch must be assigned as a Latching switch channel. Configuration of states is done in the Latching switch settings.


The state of **__Switch 2**__ will activate the selected **__LED output**__ on the **__CAN switch board.**__

{#1}


---

[Auto](help://CANSerial/CANSerial) 
##CAN

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://CANSerial/CANSerial) 
##ECM switch board

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

[Auto](help://CANSerial/CANSerial) 
##ECM keyboard

The help content will cover essential details about parameters, their properties, and how to work with them effectively.

{#1}


---

