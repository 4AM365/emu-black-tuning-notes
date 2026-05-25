##Introduction

This help section provides an overview of the **EMU Black software application**.

For details about the EMU Black hardware — including specifications, wiring, installation, and connections — please refer to the **EMU Black Hardware Manual**:
https://www.ecumaster.com/files/EMU_BLACK/EMU_BLACK_manual.pdf

Descriptions of individual strategies and parameters are available directly within the software in the **{1}**.

The **EMU Black software** provides complete access to all engine control configuration. Users can modify parameters, calibration tables, and strategies for fueling, ignition, boost control, and auxiliary systems. The software also supports configuration of inputs and outputs, sensor calibration, and setup of advanced features such as drive-by-wire throttle control, variable valve timing, launch control, and gear-dependent strategies.

Real-time data from all connected sensors can be monitored and logged, enabling precise tuning and diagnostics.

You can create or open a **project**, which represents a tune file containing all calibrations, settings, maps, and user-defined objects.


---

##Software and Firmware version

Firmware is the internal EMU Black program that controls all aspects of device behavior. Firmware and Client software are distributed together, and the latest Client must be used with the latest firmware.

The Client software is backward-compatible, meaning it can communicate with older firmware versions, but older Client versions will not work with newer Firmware.
The latest versions of the EMU Black software, including test and development builds, are always available at Ecumaster Test Versions: (https://www.ecumaster.com/testVersions.html). Official stable releases can be downloaded from the EMU Black product page: (https://www.ecumaster.com/products/emu-black/).

Firmware can be updated directly from the EMU Black software by selecting **Upgrade firmware** from the File menu and opening the appropriate firmware file. The process must not be interrupted, and all injectors and ignition coils should be disconnected beforehand. To prevent data loss, it is recommended to save the current project before performing the upgrade. If communication issues occur or the computer’s power supply is unstable (for example, due to low battery on a laptop), the upgrade should not be attempted. If the upgrade fails, restart the device and repeat the procedure.


---

##Connection, Projects, and Files

<i><b>Note:</b> The EMU Black Client software can be launched and used without connecting the device. This allows creating and editing projects offline, which can later be uploaded to the ECU when connected.</i>

During the first connection to the EMU Black device, a window will appear displaying the device name. By default, the device’s unique serial number is used, but it can be changed to any preferred name. A subdirectory with this name is created in **My Documents / EMU_BLACK_V3**, where device configurations, projects, and logs are stored.

A quicksave subdirectory is created for each device, storing working copies of calibrations when the user presses **F2** (to __Make maps permanent__).

The following file types are used by the Client software:
|File description| File extension|
|Project file| *.emub3|
|Data log file| *.emublog3|
|Scope file| *.emubscp3|
|Layout files| *.emublayout|

<b>Saving Changes</b>
When a parameter or table value is changed, it is immediately sent to the EMU Black device, but only stored in a temporary copy of the project. To keep the changes after disconnecting the PC, the __Make permanent__ command must be used.

---

##Appearance of the application

The screenshot below shows the Client after the launch in Standard appearance (light mode):
![General_help/Appearance_1.png](Images/General_help/Appearance_1.png)

The application can also be displayed in **Dark mode** interface.
![General_help/Appearance_2.png](Images/General_help/Appearance_2.png)

User interface is divided into 5 areas:
1. Menu bar
2. Toolbar
3. Tree view panel with project parameters
4. Help panel
5. Status bar
6. Desktop workspace area

---

##Menu bar

The menu bar is located at the top of the application. Below is a description of all available menu functions:

**File**
| | |
|__**Open project..**__|	Open previously saved project __*.emub3__ (**Ctrl + O**)|
|__**Save project as..**__|	Save current project to a new file __*.emub3__ (**Ctrl + S**)|
|__**Save project as XML..**__|	Save current project as XML (**Ctrl + S**)|
|__**Import EMU BLACK V2 project..**__|	Import EMU Black V2 project file __*.emub__|
|__**Compare current project..**__|	Opens the __Project Comparator__ window.|
|__**Show full screen**__|	Toggle full screen mode (**Ctrl + F**)|
|__**Upgrade firmware...**__|	Change the internal software of a device|
|__**Restore to defaults**__|	Restore a device to the default settings. Deletes all settings.|
|__**Make permanent / Clear modified cells mark**__| Online mode: saves all changes to device Flash memory and stores a settings file in __MyDocuments/EMU_BLACK/DeviceName/QuickSave__ (**F2**).<br>
Offline mode: removes modified cell highlights in parameter tables.|
|__**Exit**__|	Exit the application. The desktop arrangement is saved upon exiting (**Alt + X**)|

**Edit**
| | |
|__**Undo**__|	Undo the last operation performed (**Ctrl+Z**).|
|__**Redo**__|	Redo a previously undone operation (**Ctrl+Y**).|
|__**Show undo list..**__|	Display a window with all operations performed.|
|__**Show/hide Tree view panel**__|	Show or hide the __Tree view__ (option) panel (**F9**).|
|__**Show/hide Event log**__|	Show or hide application log panel (**Shift + F9**).|

**Desktops**
| | |
|__**Restore desktops**__|	Reads desktop configurations from the following file: 
__MyDocuments / EMU_BLACK_V3/DEFAULT / desktops.emublayout__|
|__**Store desktops**__|	Save desktop configurations to the following file: 
__MyDocuments / EMU_BLACK_V3/DEFAULT / desktops.emublayout__|
|__**Open desktop templates...**__|	Read the desktop configuration from a selected file.|
|__**Save desktop templates...**__|	Save desktop configurations to a file.|
|__**Next desktop**__|	Switch to the next desktop (**Ctrl + Shift + P**).|
|__**Previous desktop**__|	Switch to the previous desktop (**Ctrl + Shift + O**).|
|__**Switch desktop to...**__|	Switch to any selected desktop (**Ctrl + 0 – 9**).|
|__**Switch Tree view panel / windows**__|	Switch between option panel and workspace windows (**TAB**)|
|__**Collapse all items in Tree view panel**__|	Collapse all options in the left parameters Tree view (**Ctrl + \ **)|

**Tools**
| | |
|__**Device password**__| {1}|
|__**DBW calibration tool**__| {2}|
|__**Calibrate WBO circuit**__| {3}|
|__**Test outputs**__|	Opens window which allows to test all EMU Black outputs. {4}|
|__**Diff. oil bleed**__| {5}|
|__**Autotune**__|	Log based autotune. {6}|
|__**Logbook**__|	The logbook records some data like maximum RPM, maximum CLT, etc. {7}|
|__**User defined CAN stream**__|	Allows user to define custom CAN stream. {8}|
|__**Set EDL-1 datalogger time**__|	In the case of using EDL-1 data logger, this options copy the PC computer time to the logger internal clock. {9}|
|__**Show assigned outputs**__|	Opens window which allows user to display all EMU Black outputs with information if given output is assigned and what is its function. {10}|
|__**Show assigned inputs**__|	Opens window which allows user to display all EMU Black inputs (digital, analog and precision analog) with information if given inputs is assigned and what is its function. {11}|
|__**User names...**__|	Assign a name to a connected EMU Black device. {12}|
|__**Scope**__|	Add a __Scope__ window to the desktop. {13}|
|__**Graph log**__|	Add a __Graph log__ window to the desktop (F6). {14}|
|__**Tune display**__|	Display a floating window showing the selected engine parameters live. Go to the __Tune display__ window description for more details (F7). {15}|
|__**Customize keys**__|	Change the shortcut keys assignment. {16}|
|__**General options**__|	Display a dialogue window with the application options. The description of the G__eneral options__ window is available below. {17}|
|__**Available strategies**__|	The list of available strategies. When the strategy is unchecked it will disappear from parameters tree view. {18}|
|__**Decode VW coding...**__| {19}|
|__**Vehicle VIN...**__| {20}|
|__**Project comment...**__| {21}|

**Windows**
| | |
|__**Tile Horizontally**__|	Organizes all open windows in a horizontal layout, reducing empty space between them.|
|__**Tile Vertically**__|	Organizes all open windows in a vertical layout, reducing empty space between them.|
|__**Next**__|	Activate the next window.|
|__**Previous**__|	Activate the previous window.|
|__**Close all windows**__|	Close all windows on current desktop (**Ctrl + Shift + C**).|

**Help**
| | |
|__**General help**__|	Display __Help__ window.|
|__**Show pinout**__|	Opens the __Help__ window at the __Pinout__ section.|
|__**Show/Hide help panel**__|	Show or hide the panel with help for each ECU setting. {22}|
|__**About**__| Open a window with information about the software version|


---

##Toolbar

There are icons on the toolbar  indicating: ![General_help/Toolbar.png](Images/General_help/Toolbar.png)
* __**Make tables permanent**__ – saving changes to the non-volatile memory of a device.
* __**Open project**__ – opening a project.
* __**Save project**__ – saving the current project.
* __ **Restore desktops**__ – loading the desktop configurations from a file.
* __**Store desktops**__ – saving the current desktop configurations to a file.
* __**Outputs test**__ – opens a window that allows testing of all EMU Black outputs. 
* __**Show assigned outputs**__ – opens a window displaying all EMU Black outputs with information about their assignment and function. 
* __**Show assigned inputs**__ – opens a window displaying all EMU Black inputs (digital, analog, and precision analog) with information about their assignment and function. 
* __**Customize keys**__ – opens a dialog to change shortcut key assignments. 
* __**Available strategies**__ – displays the list of available strategies. When a strategy is unchecked, it will disappear from the parameters tree view. 
* __**Logbook**__ – opens the logbook, which records data such as maximum RPM, maximum coolant temperature (CLT), and other key engine values. 
* __**Autotune**__ – opens the log-based autotune function. 
* __**General Options**__ – opening the __General Options__ configuration window. 
* __**Scope**__ – opening a __Scope__ window. 
* __**Graph log**__ – opening a __Graph Log__ window. 
* __**Tune display**__ – opening a __Tune Display__ window. 


---

##Tree view panel

The **__Tree view__ panel** is located on the left side of the main application window. It can be resized by dragging its border, allowing you to adjust the layout to your needs. 

The Tree view provides quick access to all functions of the **EMU Black**, organized into an expandable tree structure. This panel contains all settings for individual strategies, arranged in categories for clear and intuitive navigation. Depending on the firmware version, the available set of categories and functions may vary.

![General_help/Tree_view.png](Images/General_help/Tree_view.png)

<b>Structure of the panel</b>
The tree consists of main categories and their subcategories. Expanding a category gives the user access to parameters, tables, and configuration tools.

Available categories include:
* **Sensors and inputs** – setup of engine sensors and fail-safe values.
* **Engine start** – functions and tables related to engine cranking.
* **Fueling** – fuel dose settings.
* **Ignition** – ignition angle configuration.
* **Overrun** – parameters related to fuel cut during engine braking.
* **Knock sensors** – configuration of knock detection system.
* **Idle** – idle speed control.
* **Functions** – auxiliary strategies.
* **Outputs** – AUX outputs setup (fuel pump, coolant fan, PWM outputs, etc.).
* **Boost** – boost pressure control.
* **DBW (Drive By Wire)** – electronic throttle control.
* **Traction control** – traction control system settings.
* **VVT (Variable Valve Timing)** – camshaft phasing configuration.
* **Sport** – motorsport-oriented features.
* **Nitrous** – nitrous oxide system control.
* **Tables switching** – switching between maps and tables.
* **Engine protection** – engine safety strategies.
* **Timers** – time-based functions.
* **DSG Gearbox** – integration with DSG transmission.
* **Other** – strategies that cannot be assigned to other categories.
* **CAN, Serial** – CAN bus communication.
* **Log** – data logging configuration.
* **Gauges** – real-time parameter visualization.


<b>Search bar (filtering)</b>
The search bar is used to quickly locate items or parameters within the tree. Entering a keyword filters the entire tree so that only relevant elements remain visible.
* The search is applied not only to item names, but also to the parameters available within those items. This means that even if the item itself has a different name, it will still appear in the results if one of its parameters matches the search term.
* All unrelated items are hidden while the filter is active. 
* Once the search term is cleared, the full tree with all items becomes visible again.


<b>Types of data elements</b>
Inside categories and subcategories, users can find different types of data configuration elements, such as:
* **Wizard** – guided setup wizard. 
* **Parameters** – list of settings for specific category. 
* **Table 2D** – two-dimensional table. 
* **Table 3D** – three-dimensional table. 
* **Text Log** – a list of channels with their current values. 
* **Graph Log** – a graph showing channels values over time. 
* **Gauge** – real-time gauge. 
* **Dyno** – on-road power estimation tool. 
* **Scope** – oscilloscope for signal analysis. 
* **Tune Display** – view and analyze relevant engine information in real time. 
* **Autotune** – a tool that processes gathered log data and assists in building the VE table. 
* **DBW Autotune** – used for automatic throttle calibration. 
* **Scatter Plot** – diagnostic and visualization tool that displays logged data points on a 2D chart, with an optional third dimension represented by color. 
* **Project comment** – allows saving comments within both the ECU memory and the project file, enabling easy comparison between projects. 
* **User defined CAN stream** – in addition to predefined CAN devices, users can send and receive custom CAN frames. 
* **Functions** – user-defined logical functions. 


Double-clicking an element opens its configuration window in the Workspace area (default position: top left corner).

<b>Context menu</b>
Right-clicking a category or subcategory opens a context menu with the following options:
|Command| Description|
|__**Collapse subitems**__| Collapse all subcategories of the selected item|
|__**Collapse all**__|Collapse the entire tree|
|__**Open all windows on desktop**__| Open all elements from the selected category in the Workspace|
|__**Close all windows on desktop**__| Close all opened windows from the selected category.|

<b>Keyboard shortcuts and navigation</b>
The following keyboard and mouse actions are available for faster navigation and operation within the __Tree view__ panel and Workspace windows:
|Shortcut| Description|
|**Tab**| Switch between the __Tree view__ panel and Workspace windows|
|**Ctrl + \**| Collapse all categories in the __Tree view__|
|**F9**| Show or hide the __Tree view__ panel|
|**Arrow Up/Down**| Move between entriesArrow Left/RightCollapse or expand nodes of the tree|
|**Enter**| Collapse/expand a node (like Arrow Left/Right), or open the configuration window if the selected entry is not expandable|
|<b>Mouse double-click</b>| Collapse/expand a node of the tree, or open the selected configuration window|


---

##Help panel

The **__Help__** panel provides descriptions of individual settings and parameters available in the Tree view panel. 

It is closely linked to the __Tree view__ panel and dynamically displays information related to the currently selected parameter.

![General_help/Help_1.png](Images/General_help/Help_1.png)

When a setting, table, or channel is selected in the __Tree view__, the __Help__ panel automatically updates to show a detailed description, including its purpose, functionality, and available configuration options. This feature allows users to quickly understand the meaning and usage of each parameter without the need to refer to external manuals.

Above the name of each described parameter, there is a blue, underlined link showing the full path to its location within the tree structure. This makes it easy to trace where the parameter is found within the __Tree view__ panel.

Additionally, within the __Help__ panel text, other parameters may be referenced as links. These links are also displayed in blue and underlined, allowing quick navigation to those related parameters.

The __Help__ panel includes a toolbar with two navigation buttons: ![General_help/Help_2.png](Images/General_help/Help_2.png)
* **__Expand / collapse__** – shows / hides the help panel
* **__Move to previous page__** – returns to the previously viewed parameter.
* **__Move to next page__** – moves forward in the browsing history.
* **__Language selection__** – the EMU Black V3 help is available in multiple languages. The language can be changed at any time. Please note that the content is translated automatically.


The **Move to previous/next page** buttons are active when there is a browsing history available.

Right-clicking within the __Help__ panel opens a context menu with the following options:
|Command| Description|
|__**Copy**__| Copies the current description or parameter information to the clipboard (**Ctrl + C**). This option is available only when text is selected within the Help panel or after using the __Select all__ option.|
|__**Select all**__| Selects all text within the Help panel, allowing you to quickly copy or review the entire description (**Ctrl + A**).|

Note that when navigating to a previous description or clicking the path link in the __Help__ panel, the __Tree view__ panel will not highlight the selected parameter, and the previous selection will remain in place.

For more general information about the software (pinout, main menu, desktops, etc.), a separate __General Help__ window can be opened from the main menu or with the **F1** key.

---

##Status bar

The status field contains important information on the status of a connected device.
| Status| Description|
|__**Connection status**__| DISCONNECTED - there is no communication with EMU device<br>
CONNECTED - communication with EMU device established|
|__**Ignition status (IS)**__| Information about synchronization of ignition system<br>
NO SYNC – no synchronization<br>
SYNCHRONIZING – trying to synchronize<br>
SYNCHRONIZED – ignition system synchronized|
|__**EMU state (STATE:)**__| Current state of the EMU device<br>
UNKNOWN<br>
INACTIVE - there are no calculations connected to fuelling and ignition system<br>
CRANKING - in this state, fuel dose is taken directly from Cranking fuel table, and ignition angle is defined by Cranking ignition angle parameter<br>
AFTERSTART - the engine is running,  Afterstart enrichment is present<br>
RUNNING - the engine is running normally<br>
DELAYED TURN OFF|
|__**CAN BUS state (CAN Bus)**__| Current state of CAN BUS<br>
BUS OK - CAN BUS works correctly<br>
BUS ERROR  - CAN BUS error (inappropriate speed, wrong connection, termination problems)|
|__**Trigger error (TERR)**__| NO ERROR<br>
TOOTH OUT OF RANGE<br>
UNEXPECTED MISSING TOOTH<rb>
CAM SYNC ERROR<br>
CAM SYNC ERROR, TOOTH OUT OF RANGE<br>
FALSE SEC TRIGGER, FILTERED<br>
FALSE PRIM TRIGGER, FILTERED<br>
FALSE CAM2 TRIGGER, FILTERED|
|__**Check engine error codes (CEL)**__| Information about "check engine light"<br>
NONE<br>
CLT - CLT sensor error<br>
IAT - IAT sensor error<br>
MAP - MAP sensor error<br>
WBO - WBO sensor error<br>
EGT1 - EGT 1 sensor error<br>
EGT2 - EGT 2 sensor error<br>
EGT ALARM - exhaust gas temperature exceeds a defined limit<br>
KNOCK - engine knock detected<br>
FF SENSOR - Flex Fuel sensor error<br>
DBW - DBW error<br>
FPR - effective fuel pressure exceeds defined limits<br>
DIFF CTRL - differential control error (oil pressure pump issue)<br>
EWG - electronic wastegate error (position sensor issue)<br>
OILP - low oil pressure ( < 0.25 bar)|
|__**Engine protection codes (EP)**__| NONE - none<br>
CLT - coolant temperature<br>
EGT - exhaust gas temperature<br>
FPRD - fuel pressure protection active<br>
OILTL - oil temperature low<br>
OILTH - oil temperature high<br>
OVEB - overboost<br>
STT - stuck throttle protection active<br>
OILP - oil pressure low|
|__**Launch control (LC)**__| Launch control strategy active|
|__**Fuel Cut (FC)**__| Fuel cut value|
|__**Spark Cut (SC)**__| Spark cut value|
|__**Anti lag system state (ALS#1)**__| ALS strategy active|
|__**Gear cut (GC)**__| Gear cut strategy active|
|__**Knocking (KS)**__| Knock detected|
|__**Rolling anti lag state (RAL)**__| Rolling anti lag strategy active|
|__**Idle control state (IDL)**__| Idle control strategy active|
|__**State of Fuel Pump output (FP)**__| Fuel pump enabled|
|__**State of Coolant Fan output (CF)**__| Coolant fan enabled|
|__**State of Fn #1-12 (F1-F12)**__| Current value of each function (on or off)|
|__**State of air condition clutch (AC)**__| Current state of AC clutch|
|__**Conditional logging (CL )**__|Conditional logging enabled|
|__**Saving log in progress (SL)**__| Auto save log in progress|
|__**ECU board temperature (T:)**__| Temperature of the ECU. The Emu Black is designed to operate within a temperature range of -40°C to +105°C.|
|__**Device firmware version (FV:)**__| Firmware version of connected EMU device|

If the status of CAN bus 1 or 2 differs from 'OK,' it indicates errors along the bus.

---

##Desktop workspace area

Desktops are an important part of the application. They allow you to arrange your own sets of windows, which makes the software easier and quicker to use.
At the top of the workspace area, each desktop is represented as a tab, making it easy to switch between different window layouts.

Right-clicking on the tab allows you to use the **__Rename active desktop__** option to change the name of the active desktop.

<b>Keyboard shortcuts</b>
|Shortcut| Description|
|**Ctrl + 1..0**| Switch to any selected desktop (with the appropriate number)|
|**Ctrl + Shift + P**| Switch to the next desktop|
|**Ctrl + Shift + O**| Switch to the previous desktop|

Each set of desktops is associated with a specific device connected to the PC. This makes it possible to maintain different window layouts for different devices. Details on how device directories and configuration files are created can be found in the {1} chapter.

When the EMU Black client software starts, the default set of desktops is opened from:
__My Documents/EMU_BLACK_V3/DEFAULT/desktops.emublayout__.

If you want to use an existing set of desktops for another project, select __**Save desktop template**__ from the Desktops menu and overwrite the __desktops.emublayout__ file of the target device.
Alternatively, you can use __**Desktops / Open desktop template**__ to load a set of desktops created for another device.

During work on the desktop layout, you can save the current configuration with the __**Store desktops**__ option from the __Desktops__ menu, or by clicking the __**Store desktops**__ toolbar icon. The layout is saved to the __desktops.emublayout__ file in the device directory, or in the **Default** directory if no device was connected.

To restore a previous layout, select __**Restore desktops**__ from the __**Desktops**__ menu. This option reloads the __desktops.emublayout__ file from the device directory (or from **Default** if no device is connected). You can also restore a layout by clicking the __**Open desktops**__ icon on the taskbar.

The __desktops.emublayout__ file is automatically saved when exiting the program.
When a device is connected, its desktops layout is automatically loaded from the device directory.

---

##Pinout

Example wiring diagram:
https://www.ecumaster.com/files/EMU_BLACK/Wiring_Diagram_Example_4_cylinders_EMU_BLACK.pdf



![General_help/pinout_1.png](Images/General_help/pinout_1.png)

![General_help/pinout_2.png](Images/General_help/pinout_2.png)


---

##Windows

The **Windows** in the EMU Black software provide access to parameters, tables, diagnostic tools, and visualization features. Some windows are opened directly from the __**Tree View**__, others are available through the **Tools menu**, and several can be accessed in both ways.

Different types of windows are available depending on their purpose – for example, configuration windows for editing parameters and tables, or visualization windows for viewing data, such as __**Tune Display**__ or __**Graph Log**__, which show the course of logged channels over time. Some windows include a taskbar with dedicated icons for quick navigation and control.

In the following subsections, each window type is described in detail.
			

---

##Parameters

The **__Parameters__** is a window containing specific options. It can be opened from the __Tree View__ panel, depending on the selected category.
![General_help/parameters_1.png](Images/General_help/parameters_1.png)

A __Parameters__ always has two columns. The left column contains name of each option, while the right column displays the corresponding values. Clicking on a cell in the right column allows you to modify its content. This can be a selection from a list, an on/off option, or a field to enter a custom value.

The toolbar of the __Parameters__ window includes the following icons: ![General_help/parameters_2.png](Images/General_help/parameters_2.png)
* __**Open parameters**__ – open a file containing the configuration of the current parameters block.
* __**Save parameters**__ – save the configuration of the current parameters block.
* __**Restore to defaults**__ – restore default values for the current parameters block.
* __**Help**__ – open the __Help__ panel related to this __Parameters__.


Saving individual __Parameters__ is useful for sharing configurations with other users or creating a base set of settings, for example, configurations for different ignition systems.

---

##Table 2D

**2D tables** are used to show the relationship between two variables in a simple graphical form. The __2D Table__ window can be opened from the __Tree View__ panel, depending on the selected category. The values corresponding to the graph are located in the table below it, and each cell can be modified.

The upper row of the table corresponds to the vertical axis of the graph, while the lower row defines the horizontal axis (bins).
![General_help/2Dtable_1.png](Images/General_help/2Dtable_1.png)

<b>Toolbar icons</b>
The toolbar provides quick access to basic operations on __2D tables__: ![General_help/2Dtable_2.png](Images/General_help/2Dtable_2.png)
* **__Open 2D table__** – load the current 2D table from disk.
* **__Save 2D table__** – save the current 2D table to disk.
* **__Restore to defaults__** – restore the table to default values.
* **__Help__** – open the __Help__ panel with a description of the currently selected __2D table__.


<b>Editing cell values</b>
To change a cell value, highlight the desired cell and enter a new value. You can also adjust the value using the **+** and **−** keys. For finer adjustments, hold the **ALT** key; for larger adjustments, hold the **SHIFT** key.

Arithmetic operators can be applied to selected cells by entering a value followed by an operator. For example:
* Enter 5+ to add 5 to the selected cells.
* Enter 0.5\* to scale down the selected cells by 50%.
Available operators: +, −, *, /, %.

<b>Context menu</b>
The context menu provides additional editing and configuration options. Its content depends on whether you right-click the top or bottom row of the table.
To interpolate between table cells, right-click on the top row of the table.

The context menu for the top row:
|Command|Description|
|__**Interpolate horizontally**__|Horizontal interpolation: fills selected cells using linear interpolation between the left and right edges of the selection (key shortcut: **Ctrl** + **H**).|
|__**Equalize selection**__|Smooths values within the selection (key shortcut: **E**).|
|__**Copy cells**__|Copying the value of the selected cell(s) (key shortcut: **Ctrl** + **C**).|
|__**Paste cells**__|Pasting of the copied value(s) of the cell(s) in the highlighted area (key shortcut: **Ctrl** + **V**).|

The context menu for the bottom row:
|Command|Description|
|__**X Axis bins wizard**__|Opens a configuration window for defining the X axis|
|__**Axes usage info**__|Opens __Axis usage in Tables__ window showing which other tables share the same axis. Changes to the axis affect all linked tables.|

<b><i>X Axis bins wizard</i></b>
<i><b>Note:</b> Some axis definitions are common for several tables (e.g., load, RPM). When an axis definition is modified in one table, the same definition will also change in other tables that use it.</i>
|Parameter|Description|
|__**X min value**__|The minimum value on the X axis, (for all arguments smaller than X min value, the function value is the same as for __X min value__)|
|__**X max value**__|The maximum value on the X axis, (for all arguments greater than X max value, the function value is the same as for __X max value__)|
|__**Interpolation type**__|Selecting the type of distribution of points on the X axis<br>
**__Linear interpolation__** - distribution of a specified number of points (__**X points**__), evenly distributed over a specified interval (between the minimum and maximum values)<br>
__**Exponential interpolation #1/#2**__ - distribution of a specified number of points (__**X points**__) over a given range but with a higher density at the beginning of the interval and a lower density at the end. The distribution of points is described by an exponential function with an exponent equal to 1.4 for __**#1**__ and 1.6 for __**#2**__.|

<b>Keyboard Shortcuts</b>
|Shortcut| Description|
|**=**| Increase cell value|
|**Shift +  =**| Coarse increase of cell value|
|**Alt + =**| Fine increase of cell value|
|**-**| Decrease cell value|
|**Shift + -**| Coarse decrease of cell value|
|**Alt + -**| Fine decrease of cell value|
|**Ctrl + C**| Copy selected cells|
|**Ctrl + V**| Paste copied cells|
|**Ctrl + H**| Interpolate between selected cells|
|**Ctrl + Arrows**| Copy cell value to the cell indicated by the arrow key|
|**Ctrl + Z**| Undo last operation|
|**Ctrl + Y**| Redo last operation|
|**Ctrl + A**| Select all table cells|

<b>__General Options__ – __2D table__s configuration</b>
In the __General Options__ window (available from the main menu or the application toolbar), you can configure global settings for __2D tables__:
|Parameter| Description|
|__**New 2D table size**__| Defines the default size of a newly created 2D table: __Small, Medium, Big__.|
|__**Tables color**__| Sets the default color scheme for 2D tables.|



---

##Table 3D

**3D tables** are used to represent three-dimensional non-linear relations in an easy-to-use graphical form. The __3D Table__ window can be opened from the __Tree View__ panel, depending on the selected category. Each 3D table consists of numerical values defining a variable (e.g., ignition timing) in relation to two axes (e.g., load and RPM).
![General_help/3Dtable_1.png](Images/General_help/3Dtable_1.png)

<b>Toolbar icons</b>
The toolbar provides quick access to common __3D table__ functions:
![General_help/3Dtable_2.png](Images/General_help/3Dtable_2.png)
* __**Open 3D table**__ – load the current 3D table from disk.
* __**Save 3D table**__ – save the current 3D table to disk.
* __**Only 3D table**__ – switch to table-only view.
* __**Only 3D graph**__ – switch to graph-only view.
* __**Split vertically**__ – table and graph arranged vertically.
* __**Split horizontally**__ – table and graph side by side.
* __**Follow cursor**__ – track current table position with crossbar.
* __**Automodify above**__ – automatically increase values in cells above the modified cell if they are lower (cells marked with a white checker); useful when shaping VE tables.
* __**Help**__ – open the Help panel with a description of the currently selected __3D table__.
To load a table from an existing project, change the file extension mask to **.emu** in the open dialog window.

<b>Editing cell values</b>
To change a cell value, highlight the desired cell and enter a new value. You can also adjust the value using the = and − keys. For finer adjustments, hold the Alt key; for larger adjustments, hold the Shift key.

Arithmetic operators can be applied to selected cells by entering a value followed by an operator. For example:
* Enter 5+ to add 5 to selected cells.
* Enter 0.5\* to reduce all selected cells by 50%.
Available operators: +, −, *, /, %.

<b>Context menu</b>
The context menu provides editing and configuration options. Right-clicking on the table area opens the table context menu (interpolation and edit commands). Right-clicking on an axis description opens the axis context menu (axis wizards and info).

The context menu for the table area:
|Command| Description|
|__**Interpolate horizontally**__| Horizontal interpolation: the cell values in the selection area are calculated as a linear interpolation of the cells from the left and right edges of the selection (key shortcut: **Ctrl** + **H**).|
|__**Interpolate vertically**__| Vertical interpolation: the cell values in the selection area are calculated as a linear interpolation of the cells from the top and bottom edges of the selection (key shortcut: **Ctrl** + **L**).|
|__**Interpolate diagonally**__| Interpolation between vertices. Define the 4 corner points of the selection and the rest of the cells will be counted as bilinear interpolation. Combines two commands - first the horizontal interpolation followed by the vertical interpolation (key shortcut: **Ctrl** + **D**).|
|__**Equalize selection**__| Smoothing of the selected cells (key shortcut: **E**).|
|__**Copy cells**__| Copying the value of the selected cell(s) (key shortcut: **Ctrl** + **C**).|
|__**Paste cells**__| Pasting of the copied value(s) of the cell(s) in the highlighted area (key shortcut: **Ctrl** + **V**).|

The context menu for the axis:
|Command| Description|
|__**X Axis wizard**__| Launching a wizard for the X axis to define a new number of columns and generate X axis cells according to the selected type of interpolation|
|__**Y Axis wizard**__| Launching the Y-axis wizard to define a new number of rows and to generate Y-axis cells according to the selected type of interpolation|
|**__Axes usage info__**| Opens Axis usage in Tables window showing which other tables share the same axis. Changes to the axis affect all linked tables.|

<b>X / Y axis configuration</b>
<i><b>Note:</b> Some axis definitions are common for several tables (e.g., load, RPM). When an axis definition is modified in one table, the same definition will also change in other tables that use it.</i>

Parameters available in the axis wizard:
|Parameter|	Description|
|__**X/Y min value**__|	The minimum value on the Y axis|
|__**X/Y max value**__|	The maximum value on the Y axis|
|__**Interpolation type**__|	Selection of the type of distribution of points on the Y axis<br>
**__Linear interpolation__** - the distribution of a specified number of points (**__Y points__**), evenly distributed over a specified interval (between the minimum and the maximum value)<br>
__**Exponential interpolation #1/#2**__ - distribution of a specified number of points (__**Y points**__) over a given interval, with a higher density at the beginning of the interval and a lower density at the end. The distribution of points is described by an exponential function with an exponent equal to 1.4 for __**#1**__ and 1.6 for __**#2**__.|

<b>Navigation</b>
The 3D chart view can be rotated by holding down the left mouse button on the chart and moving the mouse. To return to the default view, double-click the left mouse button on the chart.
Cells and axes should be filled with appropriate values. Multiple cells can be selected with **Shift** + **arrow** keys, and **Ctrl** + **arrow** keys copy values to adjacent cells. Horizontal and vertical interpolation commands can also be helpful.

<b>Keyboard shortcuts</b>
|Shortcut|	Description|
|**=**|	Increase cell value|
|**Shift + =****|	Coarse increase of cell value|
|**Alt + =**|	Fine increase of cell value|
|**-**|	Decrease cell value|
|**Shift + -**|	Coarse decrease of cell value|
|**Alt + -**|	Fine decrease of cell value|
|**Ctrl + C**|	Copy selected cells|
|**Ctrl + V**|	Paste copied cells|
|**Ctrl + H**|	Interpolate between selected cells|
|**Ctrl + Arrows**|	Copy cell value to the cell indicated by the arrow key|
|**Ctrl + Z**|	Undo last operation|
|**Ctrl + Y**|	Redo last operation|
|**Shift + Arrows**|	Select area|
|**Ctrl + A**|	Select all table cells|
|**F**|	Toggle cursor tracking|
|**D**|	Toggle auto-modification of cells above RPM|

<b>__General Options__ – __3D tables__ configuration</b>
In the __General Options__ window (available from the main menu or the application toolbar), you can configure global settings for __3D tables__:
|Parameter| Description|
|__**Color scheme**__| Defines the color scheme of the 3D table and graph|
|__**Load on Y axis**__| Sets the load axis direction in VE, AFR, and IGN tables|
|__**Display square tables**__| Makes rectangular tables appear more square by increasing cell height|
|__**New 3D table appearance**__| Defines how 3D tables are displayed: Table and Graph shows both views; Only Table displays numerical data only.|
|__**New 3D table size**__| Defines the default size of a newly created 3D table: Small, Medium, Big.|
|__**Cubic 3D graph**__| |


---

##Wizard

The Wizard tool allows quick selection of a pre-saved, predefined configuration for a given sensor. For example, a wizard for an intake air temperature sensor provides an intuitive interface to set sensor characteristics.
![General_help/Wizard.png](Images/General_help/Wizard.png)

The first cell in the right column is always a drop-down list, allowing you to select the appropriate characteristics from sensors or devices defined by the manufacturer, such as thermistors, NTC sensors, or injectors. Each predefined configuration can be further modified to adjust individual parameters according to specific requirements.

---

##Autotune

&&include(help://Fueling/Autotune)

---

##Functions

&&include(help://Functions/Functions)

---

##User Defined CAN stream

##User names

The **__User Names__** feature allows you to assign custom names to __Outputs__, __Analog inputs__, __CAN switches__, and standard __Switches__.
This feature helps you clearly identify the purpose of each element, making it easier to understand system behavior and analyze logs.

Each name can be freely defined by the user, with a maximum length of 16 characters.
Once assigned, the custom names will appear in the Assigned Outputs and Inputs window as well as in log files, allowing quick identification of signals and functions.

For example, if __Analog Input 2__ is connected to an oil pressure sensor, assigning it the name “Oil pressure” makes it immediately clear what this input represents.

The __User Names__ windows can be opened from __Menu / Tools__.


---

##Project comment

&&include(help://Other/Projectcomment)

---

##Device password

To secure the device with a password, you need to go to the Tools menu and select the __Device password__ option.
![General_help/Device_password.png](Images/General_help/Device_password.png)

<b>After entering the password, the device will be secured, and this will be visible on the status bar in the form of a padlock.</b>

Upon restarting the device, to connect to it, you need to enter the password. Entering the correct password will unlock the device, and it will remain in this state until it is restarted again.

The client software remembers the password during runtime, so subsequent turning on/off of the device will not require re-entering the password.

<b>When the device is password protection the Quick save during Make permanent process is disabled.</b>

During connection to the encrypted device, there are 4 options to choose from:

1. <b>Quit</b> - exit the program
2. <b>Enter password</b> - enter the password.
3. <b>Load package</b> - allows loading an encrypted package with settings. If the password with which it was saved is identical to the password in the ECU, firmware, and calibration, it will be saved on the device. This allows sending clients new calibration versions without revealing their contents. This function is not yet available.
4. <b>Restore to default</b> - restores the device to factory settings. It removes all data and the password. 

---

##DBW calibration tool

&&include(help://DBW/DBWautotune)

---

##Calibrate WBO circuit

The __**Calibrate WBO Circuit**__ function is used to calibrate the internal wideband oxygen sensor controller in the EMU Black.
The __Calibrate WBO Circuit__ window can be accessed from __Menu / Tools__.
This calibration improves the accuracy of the lambda sensor readings, especially around Lambda = 1, and is recommended for EMU devices with PCB revisions older than “O”.

To perform the calibration:
1. <b>Disconnect</b> the oxygen sensor plug from the EMU device.
2. In the __Tools__ menu, select __Calibrate WBO Circuit__.
3. The calibration will run automatically.

The current calibration value is stored in the __Logbook__ (__Tools / Logbook__) and is independent of the loaded project or firmware.


---

##General options

The __General options__ window can be opened from the toolbar or from __Menu / Tools__.
The __**General options**__ window contains the following settings:

|Option| Description|
|**__Appearance__**| Defines the default appearance of the application: Standard (light mode) or Dark mode (dark interface).|
|__**Units**__| Metric - default units system
Imperial - imperial units system (℉, mph, psi ...)|
|__**Parameters panel size**__| Sets the size of the __Tree view__ panel. It can be changed here or by dragging the panel edge.|
|__**Show toolbar**__| Show/hide main application toolbar.|
|__**Mark modified cells**__| When a cell value is changed in the table, it is marked with a yellow triangle.|
|__**Load ECU desktops**__| Loads the desktops last used with the ECU.|
|__**New 2D table size**__| Defines the default size of a newly created 2D table: Small, Medium, Big.|
|__**Tables colour**__| Defines the color scheme of the 2D table graph. Available options: Standard, Blue-Violet, Blue-Green-Red.|
|__**Color scheme**__| Defines the color scheme of the 2D tables. Available options: Standard, Blue-Violet, Blue-Green-Red.|
|__**Load on Y axis**__| Sets the load axis direction in VE, AFR, and IGN tables|
|__**Display square tables**__| Makes rectangular tables appear more square by increasing cell height|
|__**New 3D table appearance**__| Defines how newly created 3D tables are displayed: **Table and Graph** shows both views; **Only Table** displays numerical data only.|
|__**New 3D table size**__| Defines the default size of a newly created 3D table: Small, Medium, Big.|
|__**Cubic 3D graph**__| 3d table visualization is displayed with constant aspect ration instead of filling all available space.|
|__**Stop logging when paused**__| When disabled, even if the log is paused, the EMU Black continues recording data in the background. When unpaused, all pending samples are then drawn on the graph.|
|__**Auto save logs**__| Automatic saving of logs onto the hard drive|
|__**Display system time**__| If enabled, displays system time (hour, minute, second) on the graph log x-axis. Otherwise, shows time from the start of logging.|
|__**Display min values marks**__| Displays the moments and values of minimum points on the log.|
|__**Display max values marks**__| Displays the moments and values of maximum points on the log.|
|__**Default gauge size**__| Defines the default size of newly created gauges: Small, Medium, Big.|
|__**Default gauge type**__| Defines the default type of newly created gauge: Round (analog needle with digital value), Value (numeric display), Bar (bar indicator).|
|__**Round gauge style**__| Defines the default visual style of round gauges: Standard, Deep Ocean, Amber Gold.|
|__**RTA algorithm**__| Defines the method used to calculate the corrected value for the current VE cell during Real-Time Auto-tuning.|
|__**RTA delay(ms)**__| Specifies the time interval (in milliseconds) between consecutive lambda re-evaluations for the selected cell. This delay helps ensure that each VE adjustment is based on a stable, settled lambda value.|
|__**RTA power factor(%)**__| Determines what percentage of the newly calculated theoretical VE value is applied to the current VE cell.
Example: If the current VE is 40, the algorithm calculates a target of 50, and the RTA Power Factor is set to 50%, the updated VE cell value will become 45.|
|__**Don't ask at app exit**__| Decide if you want to see the __“Are you sure you want to exit the application?”__ message.|



---

##Available strategies

The list of available strategies. The __Available Strategies__ window can be opened from the toolbar or from __Menu / Tools__. When the strategy is unchecked, it disappears from the parameters tree view. This helps to simplify navigation in the __Tree View__ panel when a strategy is not used.

![General_help/Available_strategies.png](Images/General_help/Available_strategies.png)



---

##Customize keys

The __**Customize keys**__ that allows user to change default keys assignment.
The __Customize Keys__ window can be opened from the toolbar or from __Menu / Tools__.

![General_help/Customize_keys.png](Images/General_help/Customize_keys.png)

To assign new keys combination, select function, press Assign button and then press the keys.

---

##Inputs assignment

The __**Inputs assignment**__ window shows the assignment of all EMU inputs to the corresponding functions and pins.
The __Inputs Assignment__ window can be opened from the toolbar or from __Menu / Tools__.

![General_help/Inputs_assignment.png](Images/General_help/Inputs_assignment.png)

The colors indicate the status of each output:
* <b>Green</b> – input is used
* <b>Yellow</b> – input is unused
* <b>Red</b> – more than one function is assigned to the same input

---

##Outputs assignment

The __**Outputs assignment**__ window shows the assignment of all EMU outputs to the corresponding functions and pins.
The __Outputs assignment__ window can be opened from the toolbar or from __Menu / Tools__.

![General_help/Outputs_assignment.png](Images/General_help/Outputs_assignment.png)

The colors indicate the status of each output:
* <b>Green</b> – output is used
* <b>Yellow</b> – output is unused
* <b>Red</b> – more than one function is assigned to the same output

---

##Test output

__**Note:** This feature is intended only for testing outputs and checking connections. Timing is approximate and does not follow the normal operation.__

The __Test Outputs__ window can be opened from the toolbar or from __Menu / Tools__.
__**Outputs test**__ window allows to manually pulse the selected output. In the case of coils output, the signal polarity follows ignition output coil type settings. The maximum coil dwell time is limited to 20 ms per cycle, to prevent coil from damage. To perform the test, setup output, on/off times and press the __Test__ button.

|Parameter|	Description|
|__**Output**__|	Output to be tested|
|__**Num cycles**__|	Number of on / off cycles during the test|
|__**Cycle on time**__|	The time in ms during the output is activated|
|__**Cycle off time**__|	The time in ms during the output is inactive|


---

##Logbook

__**Logbook**__ stores the selected parameters in internal flash memory of the device. The __Logbook__ window can be opened from the toolbar or from __Menu / Tools__. It can be a very good source of critical information like maximum registered coolant temperatures or maximum engine RPM (especial in the case of engine failure).
![General_help/Logbook.png](Images/General_help/Logbook.png)

|Parameter|Description|
|__**Maximum RPM**__| Maximum RPM registered|
|__**Maximum MAP (kPa)**__| Maximum MAP registered|
|__**Maximum CLT (C)**__| Maximum CLT registered|
|__**Maximum IAT (C)**__| Maximum IAT registered|
|__**Time on full throttle (s)**__| Total time spent with full throttle|
|__**Maximum EGT**__| Maximum EGT registered|
|__**Maximum VSS**__| Maximum vehicle speed registered|
|__**Error codes**__| Error codes registered since the last reset. More information is available in the {1} section under __Check engine error codes (CEL)__.|
|__**WDR cntr**__| Watchdog reset count|
|__**WBO cal**__| Value set by WBO sensor calibration|
|__**Last make permanent**__| Date/Time of last Make permanent operation|


---

##Diff. oil bleed

The __**Diff. oil bleed**__ function is used for bleeding the differential system. The __Diff. oil bleed__ window can be accessed from __Menu / Tools__. It activates the differential pump while the bleed screw is open, allowing trapped air to be released. When the engine is off, the pump runs for a short, predefined period (e.g. 3 seconds) and then stops. The user can then release the pressure, close the bleed screw, and repeat the cycle as needed. 

The function allows configuring the number of cycles and the off-time between them, similar to output testing. The operation is automatic and does not require an auxiliary output to be assigned.



---

##Vehicle VIN

The __**Vehicle VIN**__ option allows assigning a Vehicle Identification Number (VIN) to the ECU so that diagnostic OBD scanners can correctly read it.
The __Vehicle VIN__ window can be accessed from __Menu / Tools__.

The VIN number is stored in a dedicated memory area inside the ECU and is not part of the project file — it is not saved or loaded together with the project.


---

##Decode VW coding

In VW platforms (such as PQ35 and MQB), the ECU must transmit a specific coding structure to ensure full compatibility with other vehicle modules. The __Decode VW Coding__ window can be accessed from __Menu / Tools__. This coding describes parameters such as the CAN stream version, gearbox type, engine code, and other vehicle configuration data.

If the coding of other modules (e.g. dashboard, ABS, DSG) does not match the coding of the engine ECU, some systems may not operate correctly or may trigger communication errors.

Before replacing the original ECU, it is therefore recommended to record the CAN traffic from the stock ECU using the USBtoCAN interface and the Light Client software.

The __Decode VW Coding__ tool analyzes the recorded CAN data and extracts key configuration information, such as:
1. CAN version
2. Engine version
3. Gearbox code
4. MDI torque configuration
5. Number of cylinders
6. Engine type
7. Other relevant identifiers

After decoding, the tool can automatically populate the corresponding parameters in the VW CAN Stream configuration within the EMU software, ensuring proper communication and feature compatibility with vehicle systems.


---

##Tune Display

&&include(help://MiscElements/log_TuneDisplay)

---

##Scope

&&include(help://MiscElements/log_Scope)

---

##Graph Log

&&include(help://MiscElements/log_Graph_1)

---

##Text Log

The __**Text Log**__ allows real-time monitoring of selected engine parameters. This window can be opened from the corresponding category in the __Tree view__ panel. Parameters are grouped according to their function, making it easier to track the operation of specific systems, such as __Idle Control__. The __Text Log__ window displays channel values in a table format.
![General_help/Text_Log.png](Images/General_help/Text_Log.png)

When the EMU is connected, the __Text Log__ can display either Live data or Cursor values, depending on the cursor position in the __Graph Log__. Both modes work the same way whether the __Graph Log__ is paused or running:
* <b>Live data</b> - shown when the cursor is not pointing at the __Graph Log__ (i.e. outside of the graph area). Text is displayed with standard (regular) font.
* <b>Cursor values</b> - shown when the cursor is placed on a specific point in the __Graph Log__. Text is displayed in italic font.


Once the cursor is moved away from the __Graph Log__, the __Text Log__ automatically switches back to showing live data.

Each row in the table shows:
* Channel name
* Value
* Unit


Pressing the right mouse button in the windowl area displays the context menu:
|Command| Description|
|__**Add to Custom**__| Adding a channel to Custom panel|

**Custom Text Log**
The user can create three separate custom logging groups. Any channel can be assigned to one or more of these groups: __Custom 1__, __Custom 2__, and __Custom 3__.

Adding a Channel to a Custom Group:
1. In any __Text Log__ window, right-click on the desired channel.
2. Select __Add to Custom__, then choose the appropriate group (__Custom 1__, __Custom 2__, or __Custom 3__).

Pressing the right mouse button in the __Custom__ window area displays the context menu:
|Command| Description|
|__**Add to Custom**__| Adding a channel to another __Custom__ window|
|__**Remove from Custom**__| Removing a channel from the __Custom__ window|
|__**Move up**__| Moving the selected row up (**Alt + Up**)|
|__**Move down**__| Moving the selected row down (**Alt + Down**)|




---

##Gauge

The __**Gauges**__ tool provides real-time information on selected parameter values. The __Gauge__ windows can be accessed from the __Tree View__ panel. In addition to the analog display with a needle on a 270-degree scale, the gauge also shows the exact value in digital form. Examples are shown in the picture below.
![General_help/Gauge.png](Images/General_help/Gauge.png)

When the EMU is connected, the __Gauge__ shows either:

* Live data – shown when the cursor is not pointing at the __Graph Log__ (i.e. the cursor is outside of the graph area).
(For **Value** and **Bar** type gauges, live data is highlighted in green. For the **Round** type gauge, live data is shown in the standard form - no color highlight).

* Cursor values – shown when the cursor hovers over a specific point in the __Graph Log__.
(Displayed in blue for all gauge types.)

This works the same whether the __Graph Log__ is paused or not. Once the cursor is moved away from the __Graph Log__, the __Gauge__ automatically switches back to showing live data.

<b>Context menu</b>
Right-clicking on the Gauge area opens the context menu. The following options are available:
|Command| Description|
|__**Gauge type**__| Selects the type of gauge:<br>
**Round** - analog needle with digital value<br>
**Value** - numeric display<br>
**Bar** - bar indicator|
|**__Size__**| Resizes the gauge to one of three predefined sizes:<br>
**Small** - 128 px<br>
**Medium** - 196 px<br>
**Big** - 256 px
Optimal aspect ratio is applied for each type.|
|__**Channel properties**__| Opens the __Channel config__ window, allowing you to configure or change the properties of the selected channel.|

<b>General Options – 3D tables configuration</b>
In the __General Options__ window (available from the main menu or the application toolbar), you can configure global settings for __Gauges__:
|Parameter|	Description|
|__**Default gauge size**__|	Defines the default size of newly created gauges: **Small**, **Medium**, **Big**.|
|__**Default gauge type**__|	Defines the default type of newly created gauge: **Round** (analog needle with digital value), **Value** (numeric display), **Bar** (bar indicator).|
|__**Round gauge style**__|	Defines the default visual style of round gauges: **Standard**, **Deep Ocean**, **Amber Gold**.|


---

##Dyno

&&include(help://Other/Dyno)

---

##Scatter Plot

&&include(help://MiscElements/log_Scatter_1)

---

##Project Comparator

**__Project comparator__** allows you to compare a project saved on disk with the project currently loaded in the Client’s memory.
The __Project comparator__ window can be opened from __Menu / File__.
![General_help/Project_comparator.png](Images/General_help/Project_comparator.png)

The comparison is performed separately for variables and tables.

When differences are found in variables, you can right-click on a selected item to access an option that lets you update the parameter in memory with the corresponding value from the project file.

This tool is useful for verifying configuration differences, synchronizing projects between team members, or restoring specific settings without reloading the entire project.


---

##Set EDL-1 datalogger time

When using the EDL-1 data logger, the __Set EDL-1 datalogger time__ function copies the PC time to the logger’s internal clock.

The __Set EDL-1 datalogger time__ window can be accessed from __Menu / Tools__.


---

