##Knock sensors

The knock sensing strategy is responsible for detecting engine knock using vibration sensors (knock sensors) and taking protective actions for the engine (retarding ignition timing). Knock in an engine is an abnormal combustion of the air-fuel mixture, where flame fronts collide with each other, generating shock waves that repeatedly bounce off the walls of the combustion chamber. These shock waves cause the engine block and cylinder head to vibrate at a frequency of 3-20 kHz, which we hear as a metallic knock.

Knock occurs after the top dead center (usually around 10-12 degrees ATDC). Detection of knock using a knock sensors involve measuring the vibrations of the engine block for each cylinder individually during the so-called knock window (defined by the start angle of measurement and the duration of measurement expressed in degrees), and then comparing the measured voltage with the voltage defined for the correct combustion process (Engine noise).

If the measured voltage is higher than the **__Engine noise voltage**__, knock is present. The greater the voltage difference, the more severe the knock.

The figure below illustrates the knock window.

![Knock/knockWindow.png](Images/Knock/knockWindow.png)

The concept of knock resonance frequency is also related to knock. This is the vibration frequency of the engine block associated with the cylinder diameter. The formula for calculating the knock resonance frequency is presented below:

** F = 900 / (PI x R), 

where 

**F** - knock frequency in kHz
**R** - is the engine cylinder radius expressed in mm

It should be noted that the calculated frequency may not be useful in practice, as other mechanical elements of the engine (e.g., the valvetrain, pistons) can generate vibrations within the calculated frequency range, making correct knock detection impossible.

In such a case, the only solution is to analyze the signal spectrum (e.g., using a PC and a recorded signal directly from the sensor) for both correct combustion and knock, to select the optimal frequency for knock detection.

When using two knock sensors (e.g., V-type engines, some inline engines), it is necessary to assign each sensor to specific cylinders in the Sampling table.

In the event of knock detection, it is possible to retard the ignition to eliminate it. The V3 software allows for per-cylinder ignition correction (only the cylinders where knock occurred will have their ignition timing corrected), which requires the engine to be running in full sequential ignition mode. Otherwise, the ignition correction will apply simultaneously to all cylinders.

Once the knock ceases, the ignition timing correction will be incrementally restored to zero. Each detected knock event increases the **__Knock count**__. This count can be utilized to create a function that, upon exceeding a certain **__Knock count**__ threshold, switches the ignition table to a more conservative ignition timing map.

!!**⚠Knock, especially under load, can quickly lead to engine damage! This is a highly undesirable situation, and the ECU should be calibrated to prevent its occurrence.

!!**⚠Knock control strategy ignition timing correction, since it works per cylinder, is not visible on the __Ignition angle__ log channel! You should observe the knock strategy ignition correction channels.



**Logging channels:

* __  **Knock level peak** __ - the maximum registered knock peak (**__Engine noise**__ - **__Knock voltage peak cyl**__) since the last sample in the log. A value of 0 indicates no knock, while values greater than zero indicate knock. The higher the value, the more severe the knock
* __  **Knocking cylinders**__ -  A list of cylinders where knock was detected since the last sample in the log.
* __  **Knock actions status __ **  - the current status of the knock sensor action strategy.
* __  **Knock voltage peak cyl #1 - #8__ ** - the integrated voltage from the knock sensor for each respective cylinder.
* __  **Knock count__ ** - the number of engine cycles in which knock was detected. If this channel reaches the value of 65535, it will no longer increment.
* __  **Knock ign retard cyl #1-#8__** - these channels show the current ignition correction for each specific cylinder.
* __  **Knock engine noise__** - the reference voltage for which combustion proceeds correctly (no knock). If the **__Knock voltage peak cyl**__ exceeds this value, the ECU recognizes that knock has been detected.



**Meaning of Knock action statuses:

* __   **Disabled__** -  the knock sensor action strategy is not enabled.
* __   **Inactive - condition not met __** The necessary conditions for the strategy (e.g., too low RPM) have not been met.
* __   **Inactive no knock__** - the conditions for the action strategy have been met, but no knock has been detected.
* __   **Active__** - knock has been detected, and the action strategy is active.








---

[Auto](help://Knocksensors/Knocksensors) 
##Sensor parameters

!!**⚠Per cylinder** gain is allowed only when the engine operates in full sequential mode (cam sync required)! Otherwise all values in cylinder gain fields should be the same!

{#1}


---

[Auto](help://Knocksensors/Knocksensors) 
##Sampling

Sampling configuration allows the assignment of knock sensor(s) to specific cylinders.
More information about knock window can be found in the {1} section.

{#1}


---

[Auto](help://Knocksensors/Knocksensors) 
##Action

The **__Action**__ strategy allows for the correction of ignition timing upon detection of knock. The status of this strategy can be monitored through the **__Knock action**__ status logging channel.

!!**⚠Per cylinder** ignition control type is allowed only when the engine operates in full sequential mode (cam sync required)!

In every engine cycle, for each cylinder where the **__Knock level__** is greater than zero, the value of **__Knock ignition retard**__  is increased proportionally to the **__Knock level__** and **__Ignition retard rate**__.

if (Knock level > 0)
{
     Knock ignition retard = Knock ignition retard + Knock level*Ignition retard rate;
    
      if ( Knock ignition retard > Max ignition retard)
           Knock ignition retard = Max ignition retard;
}
else every Knock restore rate engine cycles
{
      Knock ignition retard = Knock ignition retard - 1;
}

{#1}


---

[Auto](help://Knocksensors/Knocksensors) 
##Engine noise

This table defines the reference voltage for correct combustion of the air-fuel mixture as a function of RPM and load. If the current voltage from the knock sensor exceeds the voltage defined in this table, it indicates the presence of knock.


---

[Auto](help://Knocksensors/Knocksensors) 
##Knock Sensing

{#1}


---

[Auto](help://Knocksensors/Knocksensors) 
##Gear correction

The **__Gear gain correction__** table allows adjustment of the knock sensor signal gain to adapt the vibration level for different gears.
 A value of 0 means no signal correction, positive values increase the sensor voltage, and negative values decrease it.










---

