##Timers

**Timers** allow control over ignition timing advance, fuel injection quantity, and boost target based on the duration of the selected timer. The timer starts when the activating function takes the value of 1 (__True__) and runs until the function returns to 0 (__False__). Adjustments to fuel injection, ignition timing, and boost target are only made when the activating function has a value of 1 (__True__).

Timers can be used, for example, to reduce ignition timing advance and enrich the fuel mixture when the engine operates under Wide Open Throttle (WOT) for a set duration. This helps decrease the likelihood of knock during prolonged full load conditions.

The maximum duration for the timer is 12.5 seconds. After this time, the timer will not increase further.

In the case of the **__Drag Race timer**__ its activation requires meeting two conditions defined by the parameters **__Drag race timer trigger**__ and **__Drag race timer activation switch**__.

For the **__Drag race imer trigger**__, in addition to standard functions, you can select **__Clutch**__ (the timer starts when the clutch pedal is released) or **__Transbrake**__ (the timer starts when the transbrake is disengaged).

If, during the timer operation, the clutch is pressed or the trigger function value is no longer True, the timer will reset to 0 and stop. The timer can be reactivated only after turning off the **__Drag race activation switch**__.

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

[Auto](help://Timers/Timers) 
##Parameters

{#1}


---

[Auto](help://Timers/Timers) 
##Fuel corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Timers/Timers) 
##Ign. corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Timers/Timers) 
##Boost corr.

Tables provide structured data representation, presenting information in a tabular format for easy reference and analysis. Detailed explanations and guidelines for working with tables will be provided here. 

{#1}

---

[Auto](help://Timers/Timers) 
##Fuel correction

The **__Fuel correction**__ table defines the fuel correction based on the timer's duration. A value of 0 means no correction. The correction is applied only if the timer activating function is active.


---

[Auto](help://Timers/Timers) 
##Ignition correction

The **__Ignition correction**__ table defines the igniton angle correction based on the timer's duration. A value of 0 means no correction. Positive values cause ignition timing advance, while negative values result in ignition timing retard. The correction is applied only if the timer activating function is active.


---

[Auto](help://Timers/Timers) 
##Boost correction

The **__Boost correction**__ table defines the boost target correction based on the timer's duration. A value of 0 means no correction. The correction is applied only if the timer activating function is active.


---

[Auto](help://Timers/Timers) 
##Timers

{#1}


---

