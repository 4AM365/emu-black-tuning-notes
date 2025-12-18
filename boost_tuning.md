# How the model works
- EMU Black v3 uses a feed forward system. A known value is fed in, measurements are taken, and then a correction is made with either PID, a known value, or a table.

- The base map needs to be set up experiementally. Override your WGDC in boost settings, do a pull, and log the result. If you reach 120kpa boost at 45 wgdc for instance, go to the 120 column and enter 45 for that RPM.

- The nice thing about this is that as you climb in RPM, you can reduce WGDC to cancel out boost creep.

- I like to populate the region where the turbo isn't spolled with a high number like 100% to prioritize the turbo while it's spooling, then back it off in the midrange to manage torque. After 5000rpm, we can build boost again out to redline.

- I also like to match boost to pedal position so the car is manageable. You don't want a big hammer of boost hitting whenever you breathe on the throttle, you want to be able to ask for something and get it.