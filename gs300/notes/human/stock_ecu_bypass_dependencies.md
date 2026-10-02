# Pulling the stock ECU out of Josh's GS300 — the short version

> **⛔ NOT THE SUPRA.** This is Josh's GS300 / Aristo / CD009. Never carry values, pins,
> hardware or conclusions between this car and the Supra notes in either direction, and never
> load `supra-specs` for it. Full caveat at the top of the canonical note.


**What this covers.** What breaks when the OEM Aristo ECU comes out and the EMU Black (v3) takes
over everything. Canonical note: [`../stock_ecu_bypass_dependencies.md`](../stock_ecu_bypass_dependencies.md) — that one wins.

**The rules.**
- The stock ECU is a node on the Toyota **BEAN multiplex** bus. The EMU can't join it. Anything
  the cluster or HVAC gets over multiplex has **no wire to repin** — it just stops.
- Casualties, all multiplex: **water temp gauge, charge light, oil pressure light, oil level
  light, oil temp**, and the HVAC's engine data.
- **They cannot be re-wired.** The cluster has its **own CPU** and paints them from bus messages —
  no sender exists in the car and the alternator `L` goes to the ECM, not the lamp. Restoring them
  means BEAN, or separate gauges. (Corrects earlier advice; see §2a of the canonical note.)
- Survivors: **speedometer** (ABS ECU drives it, not the engine ECU) and **fuel gauge**.
- **There is no IACV.** Both cars are ETCS-i — idle is the throttle plate. Cruise runs through
  the same throttle, so cruise dies with the stock ECU too.
- Watch the polarities: `M-REL` **sources** 12 V to the relay coil (not ground-switched), and
  `FPC` is a **PWM speed command** into a fuel pump ECU, not a relay drive.
- The **check sensors are fine** — the EMU uses a `TPS check tolerance map`, so an offset,
  differently-sloped `VTA2` is exactly what it expects. Scope all four traces to *fill the map*,
  not to decide whether they work. (Corrects an earlier, overcautious note.)
- **v3 wiring is the reverse of v2:** throttle `VTA` → **TPS input**, pedal `VPA` → a free analog
  input. Older guides have this backwards.

**Key numbers.**
- Tach `TACH` F59-20: square wave, 0 V ↔ Vbat, freq ∝ RPM. (GS300 cluster instead takes tach off
  the **igniter**, not the ECU — confirm which cluster is fitted.)
- Fans: `REC` F59-25 + `REC2` F60-18, a **PWM pair**. Fan temp is a **second** thermistor in the
  radiator lower tank (`TH+`/`TH-`), differential, not the engine-out sensor.
- Throttle: `M+`/`M-` PWM H-bridge, `CL+`/`CL-` clutch coil (blade won't move without it),
  `+BM` on its own **15 A ETCS fuse**.
- **CD009 has exactly one switch**: reverse, SPST normally-open, 2-wire, non-polarised. **No
  speed sensor, no neutral switch.**
- Start interlock is in the **starter circuit**, not the ECU — clutch switch replaces the A/T P/N
  switch. Reverse lamps take over that same switch's terminals 4–8.
- Speed for the EMU needs a new source: ABS tap (VR sine, needs conditioning), or a Hall pickup
  and trigger wheel. LOJ-type driveshaft pickup is 10 PPR; Z32/S13/S14 are 4 PPR — not interchangeable.

**BEAN, if you want the gauges back.** The bus is single-wire, **10 kbps**, NRZ, CSMA/CD with
bitwise arbitration and an 8-bit CRC — all in SAE 970297, now in `../../reference/wiring/`. The
[BeanMPX](https://github.com/fiztech-code/BeanMPX) Arduino library already transmits and receives
it. The protocol is not the obstacle; the **message dictionary** is, and it is not published.
**Sniff this car's bus before the stock ECU comes out** — afterwards the traffic is gone for good.

**The plan.** Phased task list in §10 of the canonical note: establish facts → capture what removal
destroys → decide → repin → chassis and CD009 → commission. Phases 0 and 1 happen with the stock
ECU still running.

**When to care.** Any repin, start-up or dash-fault question on this car.

**Still open.** What "IACV" refers to · which cluster is fitted · sequential turbo state · what
the EMU already owns on the piggyback · whether the fuel pump ECU is still in the car.
