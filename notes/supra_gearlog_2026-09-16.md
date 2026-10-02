# Supra calculated-gear error: gearlog.csv

**Practical test recommendation after general interface review:** Assuming correct sensor supply as requested by owner, Hall mode with the EMU's internal 1K pull-up is a reasonable controlled diagnostic trial, following ECUMaster's explicit Hall-input guidance. This is not proof that the Tacoma output is open-collector or that pull-up absence caused the fault. Prior statements rejecting this as a next trial were too categorical. Observe the signal's low/high states and repeat the stationary log; restore prior setting if signal operation worsens. A pull-up does not make an incompatible voltage interface compatible.

**Latest diagnostic update:** Toyota's 2007 factory wiring shows the M/T V1 speed sensor supplied by fused ignition battery voltage, not 5V. The owner's stated 5V feed is a mismatch with factory wiring and now takes priority over the unconfirmed missing-pull-up hypothesis. See the final section below.

Analyzed 2026-09-16. Sources:
- `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\Supra.xml.emub3`, modified 2026-09-15 16:05:41.
- `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\misc log csv\gearlog.csv`, modified 2026-09-16 19:01:55.

CSV: 32,399 samples, TIME 0–1297.52 s. Only TIME, RPM, MAP, Vehicle Speed, Gear, Clutch pedal switch, Brake pedal switch, PPS are present. No Data changing, Making permanent, Gear unknown, raw speed-input frequency or axle speeds. Calibration continuity cannot be checked or segmented at live edits. The XML precedes the CSV modification date but its identity with the live calibration is unverified. Event-local evidence below does not depend on that identity.

## Finding

False vehicle-speed bursts cause false gear assignments at a stop. Exact upstream electrical/source fault remains unverified.

At 713.40 s: speed 0.188, RPM 1052, Gear 0. At 713.48 s: speed 44.375, RPM 1052. Speed reaches 52 by 713.60 s; Gear becomes 5 at 713.68 s (RPM 1051). Speed returns to 0.188 by 714.16 s. Throughout, brake=1, clutch=0, PPS=0 and MAP=37. Gear returns to 0 at 714.08 s. This is a speed artifact during stopped idle, not a physical acceleration or shift.

At 1103.52 s: speed 0.188, RPM 1007, Gear 0. Speed reaches 44.562 at 1103.72 s. Gear becomes 5 at 1103.84 s, RPM 1000. Speed returns to 0.188 by 1104.28 s. Again brake=1, clutch=0, PPS=0 and MAP stays 37 during the burst. Thus a pressed clutch or a clutch-switch edge is not necessary for this fault.

## Governing calculation

Local EMU help: `docs/emu-black-help/Sensorsandinputs.md:762`: R = 16 * Vehicle speed / RPM. Help also states gear cannot be correctly inferred with clutch pressed and recommends calibrating from Gear speed to RPM ratio.

At 713.68 s, R=16*52/1051=0.791627; at 1103.84 s, R=16*44.562/1000=0.712992. These erroneous speed inputs are followed by fifth-gear assignments in the log.

Sensitivity at a fixed 1050 RPM: speeds 0, 0.188, 44.562, 52 give R=0, 0.002865, 0.67904, 0.792381 respectively. This is direct arithmetic from the documented equation, not a drivetrain model. No assumed tire or final-drive inputs are needed.

Acceleration sanity check: (44.375-0.188)/0.08=552.3375 km/h/s =153.4271 m/s² while idle RPM is unchanged and brake is held. Such a pulse is inconsistent with actual movement. The full recording contains 34 adjacent steps exceeding 8 km/h; this count describes signal discontinuities, not 34 independent faults, and is not a pooled calibration-performance statistic.

## XML observations and limits

Raw values: gearDetectionType=2, numGears=6, gearRatio1..6=595/1097/1652/2388/2958/4096, gearRatioTolerance=5, gearDelay=10. Speed path: vssSource=1, speedRatio=128, vssFilter=50, drivenAxleSource=3, drivenAxleRatio=685, drivenAxleDivider=4, drivenAxleFilter=25. Digital input: VSSSensorType=1, VSSPullup=0, VSSInputFilter=1, VSSTrigerEdge=0. clutchPedalInput=3.

These are raw XML values, not verified UI scales or enum labels. Do not infer an exact gear-ratio correction, delay in milliseconds, or wiring change from them. No tune edits made. The CSV does not establish physical gear during all moving intervals or verify all six reference ratios.

Next diagnostic: verify selected vehicle-speed source in EMU, then record that source/axle speed, raw VSS frequency if available, Gear speed to RPM ratio, Gear unknown and edit flags alongside existing channels. Probe the selected speed signal and its ground/supply during a stationary burst to distinguish input/wiring noise from source/configuration issues. Ratio/tolerance changes cannot correct phantom road speed.

Related historical evidence: `supra/notes/vss_signal_integrity.md` records similar false speed bursts and explicitly says the prior clutch-ground repair did not eliminate them. This new capture independently confirms the symptom remains; it does not establish the same physical cause.

## Follow-up: Tacoma sensor and verified input configuration

Owner states transmission and sensor are from a 2007 Tacoma; sensor is supplied from 5V+ and SGND. Exact sensor part number and whether output is shared with the cluster are pending. This describes installed wiring, not a verified sensor supply specification.

Read the installed matching firmware definition `C:\Program Files (x86)\Ecumaster\EMU Black V3\XML\Project\version3_059.xml` (tune project is 3.059). This resolves the previous enum uncertainty:
- VSSSensorType=1: Hall / Optical sensor.
- VSSPullup=0: None (neither pull-up nor pull-down).
- drivenAxleSource=3: Signal from VSS input.
- vssSource=1: Driven axle.
- gearDetectionType=2: Calculated from vehicle speed.
- Available VSS pull-ups include 4K7 (1), 1K (2), 820 ohm (3).

Thus the configured path is VSS pin -> driven axle -> vehicle speed -> calculated gear. This excludes a configured GPS/CAN speed source as the explanation in this XML.

Leading conditional hypothesis: missing signal pull-up if this sensor has an open-collector/open-drain output and no external/cluster pull-up. Local manufacturer help `docs/emu-black-help/Sensorsandinputs.md:171` states that Hall/optical sensors are typically open-collector/open-drain and recommends 1K pull-up; supply may be 5V or 12V depending on sensor. Sensor power is not a signal pull-up. Exact sensor output circuit and rated supply remain unverified; do not assert all 2007 Tacoma sensors are 5V or 12V, or prescribe a supply conversion without the part specification.

Confirmation: check exact sensor output/supply specification and shared wiring, then use Hall with 1K pull-up if open-collector and compatible. Scope signal relative to SGND at the ECU, with supply also monitored at the sensor. Stationary signal should hold one state; controlled shaft rotation should produce clean transitions. If a correct pull-up does not remove false edges, isolate sensor versus harness/ECU with the ECU input kept properly biased while the sensor is disconnected. Disappearance alone does not prove sensor failure; supply and sensor-end wiring remain candidates. Do not use a floating unplugged input as the control.

## Toyota factory wiring retrieved: supply mismatch confirmed

Source: Toyota Tacoma electrical wiring manual EM03N0U, printed page 366, overall wiring chart 29; downloaded PDF page 56, visually inspected. Public mirror: https://toyotaspace.com/wp-content/uploads/2024/11/2007-toyota-tacoma-wiring-diagram.pdf#page=56 . Local working copy `tmp/pdfs/tacoma2007-ewd.pdf`, rendered page `tmp/pdfs/tacoma-vss.png`.

Manual-transmission V1 (Vehicle Speed Sensor, Combination Meter):
- Pin 1 IG+, pink (P): fed by 10A IG1 fuse through 1J-9, PF-7, PA-4. This is switched battery supply.
- Pin 2 SE, white (W): return to combination meter C9(A)-3 through IH1-9.
- Pin 3 SI, red/yellow (R-Y): signal to combination meter C9(A)-6 through IH1-8.

This establishes the OEM supply and pin functions, but the block diagram does not expose the sensor's internal output stage. Do not call it definitively push-pull or externally pulled-up from this drawing. Factory SE runs to the meter; the drawing does not require replacing the owner's SGND with chassis ground.

Supplementary Toyota service-text reproduction indexed as 2006 Tacoma gives a battery-powered standalone test: battery positive to 1, negative to 2; voltmeter positive to 3, negative to 2; rotate shaft and observe approximately 0 to at least 11V, four pulses per sensor-shaft revolution. No external resistor is specified in that text. Source: https://cdn-2.onlymanuals.com/toyota/tacoma/toyota_tacoma_workshop_manual_2006_2006 . This compilation has mixed material and is supporting context, not an exact-year internal-circuit specification. The verified 2007 EWD independently establishes battery supply.

Conclusion: retract the ranking of missing pull-up as the leading identified issue. The documented discrepancy is supplying the OEM sensor with 5V instead of its factory ignition/battery feed. Undervoltage causing the observed glitches remains a hypothesis until an A/B measurement confirms it; no internal undervoltage threshold is known. First test the sensor independently with its correct fused battery supply, meter/scope between SI and SE and no ECU signal connection. Confirm output voltage/interface compatibility before reconnecting to EMU; never feed battery voltage into EMU's 5V reference. Retain Hall mode, and do not enable a pull-up merely on the basis of the word Hall. No calibration edits made.

## General Hall digital-input best practices, retrieved

Allegro Hall Effect IC Applications Guide describes open-collector digital Hall switches with a pull-up and separately identifies push-pull variants: https://www.allegromicro.com/en/Insights-and-Innovations/Technical-Documents/Hall-Effect-Sensor-IC-Publications/Hall-Effect-IC-Applications-Guide . TI likewise distinguishes these output types: https://www.ti.com/document-viewer/lit/html/SBOA196 . Therefore no universal resistor rule applies to every Hall sensor. The relevant practical default comes from ECUMaster's own guidance in `docs/emu-black-help/Sensorsandinputs.md:171`, which recommends an internal 1K pull-up for typical Hall/open-collector inputs. Combined with this tune's Hall mode and None bias selection, that supports trying the internal 1K setting under observed conditions without claiming an established hardware diagnosis. No extra external resistor or pull-up to 12V is recommended.
