##Tables switching

The **__Table switching**__ options are responsible for switching the basic tables responsible for fuel dosing, ignition timing, etc. The tables can be switched using switches or functions (e.g., changing the base ignition map in the case of excessive knocking events).

When using a **__Flex Fuel**__ sensor to measure the ethanol content in the fuel, it is possible to blend the ignition, lambda target, ASE, Warmup, and Cranking tables based on the fuel composition.

To do this, for the tables of interest, go to the {1} configuration, select the **__Flex Fuel**__ option, and then configure the blend characteristics in **__the FF xxxx blend**__ tables.

**Logging channels:

* __ **FF blend VE**__ - the current blend percentage between the **__VE**__ tables. A value of 100% means that the VE value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__VE **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend ign**__ - the current blend percentage between the **__Ignition angle**__ tables. A value of 100% means that the ignition timing value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Ignition angle **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend lambda**__ - the current blend percentage between the **__Lambda target**__ tables. A value of 100% means that the **__Lambda target**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Lambda target **__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend warmup**__ - the current blend percentage between the **__Warmup enrichment**__ tables. A value of 100% means that the **__Warmup enrichment**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Warmup enrichment**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend cranking fuel**__ - the current blend percentage between the **__Cranking fuel**__ tables. A value of 100% means that the **__Cranking fuel**__ value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__Cranking fuel**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **FF blend ASE**__ - the current blend percentage between the **__ASE**__ tables. A value of 100% means that the **__ASE__** value is taken from table 1, while a value of 0% means it is taken from table 2. In the case where a switch or function is chosen for changing the **__ASE**__ table, the value of this channel takes only two values: 100% for table 1 and 0% for table 2.
* __ **VE table index**__ - index of the currently used VE table.
* __ **VVT CAM1 table index**__ - index of the currently used **__VVT CAM1**__ table.
* __ **VVT CAM2 table index**__ - index of the currently used **__VVT CAM2**__ table.
* __ **Overrun tables index**__ - index of the currently used **__Overrun**__ tables.


---

[Auto](help://Tablesswitching/Tablesswitching) 
##Parameters

The following parameters allow for the configuration of the switching method for individual tables. For tables that allow blending between them, the Flex Fuel option is available.


{#1}


---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF Ign blend

**__FF Ign blend**__ table allows blending between **__Ignition 1**__ and **__2**__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Swtich IGN tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final ignition angle**__ = Ignition table 1 x Blending% + Ignition table 2 x (100% - Blending%)


---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF Lambda target blend

**__FF Lambda target blend**__ table allows blending between **__Lambda trgt. 1**__ and **__2 **__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Swtich lambda tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final lambda target**__ = Lambda table 1 x Blending% + Lambda table 2 x (100% - Blending%)



---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF Crank. fuel blend

**__FF crank fuel blend**__ table allows blending between **__Cranking fuel 1**__ and **__2 **__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Switch cranking fuel tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final cranking fuel**__ = Cranking fuel table 1 x Blending% + Cranking fuel table 2 x (100% - Blending%)



---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF ASE blend

**__FF ASE blend**__ table allows blending between **__ASE 1**__ and **__2 **__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Switch ASE tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final ASE enrichment**__ = ASE table 1 x Blending% + ASE table 2 x (100% - Blending%)



---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF Warmup blend

**__FF warmup blend**__ table allows blending between **_Warmup 1**__ and **__2 **__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Switch warmup tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final warmup enrichment**__ = Warmup table 1 x Blending% + Warmup table 2 x (100% - Blending%)



---

[Auto](help://Tablesswitching/Tablesswitching) 
##Tables

{#1}




---

[Auto](help://Tablesswitching/Tablesswitching) 
##VE blend

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Tablesswitching/Tablesswitching) 
##FF VE blend

**__FF VE blend**__ table allows blending between **__VE 1**__ and **__2 **__  tables, depending on the ethanol content in the fuel.

To activate this blending, in the {1} options, select Flex Fuel as the switch option for **__Switch VE tables**__.
 
**__Blending%**__ = Ethanol content blend[Ethanol content] 
**__Final VE**__ = VE table 1 x Blending% + VE table 2 x (100% - Blending%)



---

