# Determined by three things:
- TPS rate limit
- DBW characteristics
- boost vs PPS

## TPS Rate Limit
- Controls 'bucking' sensation at low speed by slowly opening or closing the throttle body.
- Not a huge adjustment range here. You get a span of 125 degrees/second to play with on top of the default level, which is from 0 to 1300 degrees/sec.
- Try a small value first and then dial it back until it feels snappy enough.
- Make it much lower at low speeds and much higher at high speeds. 

## DBW Characteristic
- Makes a bigger difference than the TPS rate limit even.
- Linear mapping at high RPM ranges will give you the most predictable closing feel, but sometimes its good to blow the throttle body open early to increase system efficiency and then control power level by selecting wastegate duty cycle based on pedal position.

## DBW Characteristic type
- You can define the DBW characteristic as well as the rate limit based on MAP instead of RPM.
- This creates potential for circular logic, where a 'gentle' throttle map at low MAP means you never get enough TPS to actually build that MAP up, although your WGDC will be higher because it's PPS based.

- I like the car to feel like it's 'ready to launch'. That means getting the MAP up early and then using TPS to apply power. This also means that pre-throttle boost reference vs MAP is preferable, because you can have whatever you want in the intake plenum based on your power needs, but have the power 'ready to go' in the charge pipes.