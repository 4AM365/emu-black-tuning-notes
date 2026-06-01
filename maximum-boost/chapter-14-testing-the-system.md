---
title: "Chapter 14: Testing The System"
source: "Maximum Boost by Corky Bell (1997)"
chapter: 14
pages: "167–173"
topics: ["testing", "system test", "pressure measurement", "temperature measurement", "boost gauge", "EGT", "data acquisition"]
generated: "2026-05-24"
---

# Chapter 14: Testing The System

> *Maximum Boost* — Corky Bell (1997) | pages 167–173

Compressor
inlet
Temperature

*Fig. 14-2. Temperature*
gauging the intake for
determining temperature rise Hraugh the
turbo. Gauge | indicates ambient air
temperature available
to the turbo, Gauge 2
minus gauge 1 indicates temperature rise
across the turbo.

Compressor
Outlet
Conditions

So here the odd circumstance exists that flow is down, boost remains the
same, and the pressure ratio is higher. Any time the pressure ratio goes up,
heat goes up. Net result is that power is down and heat is up. Sounds almost
like a Roots blower. This may seem like science or some such, but it’s not really.
The idea that the turbo is told to make the same amount of boost out of less air
logically means it must work a bit harder to do so. The harder it has to work,
the more heat it makes. We’ve all experienced similar situations.

Toa measure flow losses through the intake system upstream of the turbo, insert a vacuum gauge just in front of the compressor inlet. Then

Standard barometric pressure

ARTE Rae bee = Standard barometric pressure — loss through filter

Standard barometric pressure is 29.97 in. hg. In practice, 30 can be used as
an approximation for 29.97.

Should the gauge read 3 inches of vacuum under maximum load conditions,
the percent loss can be judged to be

ae, Seo
Air filter flow loss = 30-3 1=11%

Obviously a zero loss is elusive, but the effort to create a low-restriction intake system will be rewarded with more power and less heat. All the same arguments apply to keeping the air filter element clean.

Thermodynamics is not everyone’s cup of tea, but the equations are simple,
and a fifteen-dollar calculator can solve them. The value in crunching the
numbers is to determine whether the turbo is the correct size. The air temperature entering the compressor is vital information, because it is the number
from which all others are calculated. Do not assume this temperature is ambient. If the air inlet is outside the engine compartment, compressor inlet temperature may be the same as ambient. If it is in the engine compartment, too
often the inlet air is diluted by air that has passed through the radiator or
looped around the exhaust manifold. Measure compressor inlet air temperature with a gauge positioned as in figure 14-2.

#|

ae

Mass llowmeter

Turbo

At fitter

Two quantities must be known at the outlet side of the turbo: pressure and
temperature. Compressor outlet pressure is the true boost produced by the
turbo, All measurements of the flow as it gets closer to the engine will be refer-

enced to this pressure for flow loss or efficiency calculations, For example, this
pressure minus the pressure entering the intake manifold will measure flow
loss characteristics of the intercooler and associated plumbing.

Compressor outlet temperature is the other factor required in calculating
the turbo size to fit the engine. It is used twice in the equation for IC efficiencies, 30 measure it carefully. Once pressure and temperature al the compressor
outlet are known, the real pressure ratio can be calculated, provided no intercooler is present. With an intercooler, pressure ratio calculation should wait
until the intercooler outlet conditions are known.

The most significant calculations to be made here are spot checks of the turbo’s efficiency range. The tools for these measurements are not adequate to determine the entire compressor map. Nevertheless, one can develop a feel for
whether the turbo is operating in the efficiency range that will get the job
done. These calculations are somewhat laborious, but there is no other way,
short of calling on a thermodynamics buddy.

At least two spots should be checked: somewhere around torque peak and at
maximum rpm—both, of course, at maximum boost. The check involves calculating the efficiency at which the compressor is operating and comparing those
numbers to the efficiency predicted by the compressor flow maps.

Compressor efficiency (E,,) is calculated using the following formula:

We (PR’™ x T 5s) = Tita
¢ ~ ~~ Temperature rise

where

PR = pressure ratio
Tabs = Compressor inlet temperature on the absolute scale (see glossary)

Because this is a thermodynamic formula of general applicability, it is necessary to insert the relevant temperature rise in the denominator (from Chapter 5):

Temperature rise = T,,~T',

The exponent 0.28 in the numerator is determined by the gas constant, a
number that indicates the extent to which a gas heats up when compressed.
The x’ key on the fifteen-dollar calculator will allow us to find the value of
PR®-28.

Example:

Let engine displacement = 200 cid, boost = LO psi, and compressor inlet
temperature = 90°F (= 90° + 460° = 550° absolute). At or near torque peak
(4500 rpm), let outlet temperature = 210°F; at maximum load (6500 rpm), let
outlet temperature = 235°F.

Using the formula for pressure ratio from Chapter 3,

14.7 + 10

Calculation of E, at or near the torque peak:

Using the formula for temperature rise from Chapter 5,
Temperature rise = 210°F -90°F = 120°F
Then

DT epi ,
i 5 ee ee — ) - 550° _ 6.72 = 72%

Pressure ratio =

Ambient
Temperature
in Front of

the Intercooler

*Fig. 14-3. Ambient*
temperature measurement, necessary for
determining intercooler
efficiency

intercooler
Outlet
Conditions

intake Manifold
Pressure

Using the formula for airflow from Chapter 3,

200 x 0.5 x 4500 x 0.85
1728

Calculation of E, at maximum rpm:
Using the formula for temperature rise from Chapter 5,

Temperature rise = 235°F — 90°F =145°F
Then

Airflow rate = = 221 cfm

0.23

(1.68 x 550°) — 550°

145°
Using the formula for airflow from Chapter 3,

200 x 0.5 x 6500 x 0.85
1728

These calculations give the pressure ratio and airflow for two points that
can be plotted on the compressor flow map, with pressure ratio the vertical
axis and airflow the horizontal axis (see Chapters 3 or 17). Compare the efficiency predicted by the curve on the flow map to the calculated values. If the
predicted efficiency is two or three points higher or lower than the calculated
values, all is well. If the numbers calculated are four or five points higher than
the map, we are in wonderful shape. If they are more than four or five points
lower, performance has been compromised, and it’s back to the drawing board

EB, = = 0.59 = 59%

Airflow rate = = 320 cfm

Accurate determination of the IC’s real capability is in part based on determination of the temperature of the air that cools the cores, Although this factor is
not used directly in calculations involving the turbo system, it is of interest in
really getting into checking the merit of one core design versus another with
respect to heat transfer coefficients.

Thermometer

¢ zi

Intercooler

Temperature and pressure must be measured again at the intercooler outlet.
These numbers are significant, because they are the conditions the engine will
experience, This naively assumes that not much will happen in the tube from
the intercooler back to the engine. With these data, we have enough information to determine the intercooler’s efficiency and the power loss due to boost
pressure loss.

Should any significant events occur in the charge’s trip from the IC to the intake manifold, they will show up in the intake manifold pressure relative to LC
outlet conditions, It is relatively common to have a throttle plate far too small

P compressor outlet P intercooler outlet
T compressor outlet T intercooler outlel

Fig, 14-4. The five
points of interest for
temperature and
pressure meastirement

P compressor inlet
T compressor inlet

P ambient
T ambient

P intake manifold

Air filter

for the job, and here is the way to find it. If more than 1 psi difference exists
between the IC outlet and the intake manifold, it will probably prove revealing
to check the pressure right in front of the throttle plate versus that in the manifold. This will determine if the loss is in the return tube or if the throttle plate
is the problem.

The boost gauge in the instrument panel is set up to read intake manifold
pressure. This is the amount of pressure you have left of the original pressure
created by the turbo less all losses incurred on the way to the intake manifold.
Try to keep the total loss under 2 psi—or, better yet, 10% of the boost pressure.

*Fig. 14-5. Measuring*
pressure loss across
the throttle body.
Gauge 1 minus gauge 2
indicates boost
#1 #2
pressure loss across
the throttle plate.
=—.

Turbine Inlet Exhaust manifold pressure can better be described as Turbine Inlet Pressure.
Pressure = ''[‘his TIP is an evil thing. In the final analysis, | suspect TIP will be called the
only evil thing brought to bear by the turbo. The reason TIP is an undesirable
quantity is the fact that it is almost always greater than the intake manifold
pressure (IMP?) generated by the turbo, When this occurs, a certain portion of
the burned exhaust gas is pushed back into the combustion chamber during
the cam overlap period. This situation is detrimental to several things, all explained elsewhere in this book.

It is this writer’s opinion that a good street turbo system will show the ratio
of TIP to IMP to be approximately 2. [fa ratio of greater than 2 exists, the turbo is too small and is choking the system down and not permitting much power
gain, If the ratio is less than 2, often the boost threshold will be higher than
desirable for commuter car use. This situation is offset by the fact that as the
ratio comes down, power goes up. In fact, one of the design parameters of a

*Fig. 14-6. Measuring*
turbine inlet pressure.
The steel line will
reduce exhaust gas
temperature to silicone
hose allowables.

Tailpipe
Back Pressure

*Fig. 14-7. Determining tailpipe*
restriction distribution. Gauge
#1 indicates total tailpipe back
pressure. #2 indicates back
pressure caused by the pipe and
muffler. #3 indicates back pressure caused by the muffler. #1
minus #2 ts pressure loss across
the converter. #2 minus #3 1s

race turbo system is that the 'T'TP/IMP ratio be less than 1. When this crossover
point is reached, where intake pressure becomes greater than exhaust pressure, a turbo can begin to make serious power. This is one of the reasons the ’’87
Formula 1 racers could generate over 1000 bhp from 90 cubic inches. It may
come about one day that we can have our cake and more cake again when variable area turbine nozzle turbos are commonplace. They will permit low boost
thresholds while allowing boost to exceed TIP once boost has stabilized at its
maximum setting.

Measuring turbine inlet pressure requires a bit more effort than other pressure measurements, as exhaust gases are obviously very hot.

= 10" of 5/32" steel line

Where do you suppose the fairy tale started that tailpipe back pressure was
needed to prevent burned exhaust valves? Someone ought to quickly inform all
those racers out there that they are in serious trouble. Tailpipe back pressure
can be just as evil as TIP but at least it is easy to do something about. Potential
gains are more power and less heat in the system—exactly the right things to
achieve.

In measuring tailpipe back pressure, it is also necessary to measure restriction distribution, as indicated in figure 14-7. In so doing, one can determine
what contribution to the total back pressure is created by the pipe, catalytic
converter, and muffler.

Tailpipe back pressure is partly responsible for the magnitude of the turbine inlet pressure. Any decrease in tailpipe pressure that can be brought
about will be reflected in a nice decrease in TIP

#3

Muffler

pressure lass through the pipe.

Air/Fuel Ratio

*Fig. 14-8. Left: The*
excellent air/fuel ratio
meter from Horiba.
While expensive, tt
offers lab-test-quality
results, and its sensor
can be mounted at the
end of the tailpipe.
Right: Although not a
lab test instrument, a
diode-readout mixture
indicator is an excellent
low-cost tuning guide.

AiR/FUEL Ratio 171

Knowing the air/fuel ratio is somewhat like knowing your checkbook balance.
It tells you what you've got and where you stand, but not what you can do
about it. A wide variety of pieces have recently been introduced to the market
for measuring afr.

The neat little oxygen-sensor-based units on the market will give you a good
guide, if not exact numbers, but real accuracy has yet to come cheap. For serious tuners, the Horiba and Motec meters are perhaps top of the line. Check the
source listings at the end of the book and gather the information to make a reasonable decision.

Measurement of the numbers is nothing more than equipment and time.
Evaluation of those numbers is where a bit of experience helps out. When testing, two significant numbers will be required: cruise afr and full-throttle aff.
Cruise afr will likely be in the range of 14.0 to 15.0 to 1, Full throttle is where
the fun is and should be close to 12.5 or 13.0 to 1.

For the home tuner, the oxygen sensor that fits into the tailpipe near the
heat source will do a good job. It can be considered a permanent installation
and checked as often as desired.

utan | RICH
TO

s
FUEL AIR RATIO

Inspecting the
Engine for
Turbo-induced
Damage

*Fig. 15-1. Worst case*
scenarios ire never
preity, and the fallout
from a malfunctioning
turbo system ts no exception.

om TROUBLE

Wren investigating running problems on a turbocharged engine, you need
to remember that there are two categories of problems that can arise. The first
category includes those types of problems that can happen to any engine,
whether turbocharged or not. Turbo engines can still have problems with
spark plugs, plug wires, coils, ignition control boxes, EFI computers, timing
chains, water pumps, fan belts, alternators, throwout bearings, cam bearings,
and .. . the picture is obvious. With regard to these problems, a turbo engine is
no different from a normally aspirated engine. Today’s attitude toward service
and repair of the turbocharged performance car generally leads to the somewhat ridiculous/comical response of, “Whatever the problem, it’s that damn
turbo’s fault.” Fixes for general engine problems can be sought elsewhere and
are not within the scope of this book.

The second category is the malfunction of a component in the turbocharger
system, or a problem caused by a malfunctioning turbo system. This chapter offers a guide to isolating and recognizing these problems, Also, at the end of the
chapter, you'll find a troubleshooting guide which offers a lot of information.
Study it carefully and eliminate the simple things first.

When you encounter any problem that even remotely hints at possible engine
damage, it is best to check it out pronto. Get proof that the engine is undamaged, or focus on fixing it. Worrisome signs are rough running at idle, loss of
power, or bluish-gray or white smoke issuing from the tailpipe. Excessive puffing of oil vapor from the valve cover or crankcase breather is also cause for con
