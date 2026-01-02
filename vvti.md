vvti PID tuning

Max and min solenoid output - not too important, used 5% to 90% to keep the range large. We could use this to set a floor and get rid of the vvt-i clatter.

setpoint - this is where all of the calcs start, and is also the inflection point between 'we need more' and 'we need less'. Super important.

P and setpoint - the 'forcing function' of the PID is the oil pressure moving the cam forward. We are enabling the forcing function with the PID. This changes drastically with oil pressure and temperature. Need to set the system with the engine hot. Some may disable vvt-i when the engine is cold entirely.

Proportional - this is the initial attack. We want A LOT. We can then control it with strong integral.

Imagine chasing after a car that is moving away from you. You approach it, but if you go too fast and don't slow down you'll overshoot it.

Proportional control means we 'approach' with speed in proportion to the difference between our position and our target.

If we are a little slow or a little fast, we measure this over time (an integral is the area under a curve over time) and then we add or subtract from the proportional term.

Proportional control can work on its own, but in order to approach a term very fast we will overshoot very far. Proportional control acts on the difference between position and target and varies the control parameter (speed of approach for us) to get there. The less of a difference there is, the less duty cycle will be commanded. 

Damping prevents overshoot, allows for more aggressive P, and prevents oscillation.

Integral control corrects for steady-state offsets. It's a running counter of 'how far off we are from the target'. It then adds or subtracts duty cycle to squeeze down the error range.
An integral correction limit keeps the term from accumulating huge error values. If our error value is too big, we probably need to change the proportional term. 