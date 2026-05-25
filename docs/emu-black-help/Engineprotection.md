##Engine protection

The **Engine protection** functions provide additional engine safeguarding and allow configuration of error notification methods (**MIL** lamp). 

Activating the **Stuck throttle** function is recommended for both electronic and mechanical throttle types (where a jammed control cable could occur).








---

[Auto](help://Engineprotection/Engineprotection) 
##Check engine light

The **Check engine light** function allows you to define how basic errors detected by the EMU are reported and to specify which errors should be reported.

If errors are to be sent via the CAN bus, select the **CAN-BUS** option in the **__Check engine light output__** settings.

!!⚠If the **__Check Engine**__ status is sent via a vehicle-specific CAN stream, the information about the warning light being on is always transmitted when the engine is not running. It is also necessary to select **__CAN BU**__  as the **__Check Engine Light Output**__ option and enable reporting of the relevant error codes.

Current errors can be read from the __**Check engine code**__ log channel.

{#1}


---

[Auto](help://Engineprotection/Engineprotection) 
##EGT Alarm

The **EGT alarm** function is used to signal when the exhaust gas temperature exceeds a defined limit. There is also an option to signal temperature overrun through the check engine light. To enable this feature, select Report EGT Alarm in the {1} options.

{#1}


---

[Auto](help://Engineprotection/Engineprotection) 
##Fuel pressure prot.

The **Fuel pressure** protection function allows for engine RPM restriction and indicates a failure with the Check engine** light when the effective fuel pressure exceeds defined limits. 

**A fuel pressure sensor must be connected and calibrated for this function to work properly.

To enable the **Check engine** light for this feature, ensure **__Report fuel pressure failure__** is checked in {1} configuration.

{#1}


---

[Auto](help://Engineprotection/Engineprotection) 
##Stuck throttle

The **Stuck throttle** protection strategy is designed to protect the driver in the event of a jammed throttle. This function is especially recommended as a safety feature for electronic throttles (DBW). In the case of a jammed throttle or electronic throttle failure, pressing the brake pedal will cut the fuel dose to prevent the engine from revving up.

{#1}


---

[Auto](help://Engineprotection/Engineprotection) 
##Oil press. cut

The **Oil pressure cut** strategy is used to protect the engine in case of low oil pressure during operation. If the oil pressure at a given RPM falls below the defined threshold, the engine will shut off. The minimum oil pressure for each RPM level is specified in the {1} table.



---

[Auto](help://Engineprotection/Engineprotection) [Auto](help://Engineprotection/Oilpress_cut) 
##Parameters

The help content will cover essential details about parameters, their properties, and how to work with them effectively.


{#1}


---

[Auto](help://Engineprotection/Engineprotection) [Auto](help://Engineprotection/Oilpress_cut) 
##Oil press. cut tbl

The **Oil pressure cut** table is used to define the minimum allowable oil pressure for each RPM level and is applied in the {1} protection strategy.








---

