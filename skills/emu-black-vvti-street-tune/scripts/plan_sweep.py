"""Generate a VVT sweep test plan: which cells to test, in what order, with
the cruise speed/gear that puts you at each cell.

Usage:
  python plan_sweep.py [--vehicle-gear-ratios "1:3.5,2:2.0,3:1.5,4:1.2,5:1.0,6:0.83"] \
                       [--final-drive 3.266] [--tire-circumference-m 2.05]

If no vehicle parameters are given, the plan is purely (MAP, RPM) without
suggested speeds.
"""
import argparse, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Cells ordered by priority for street optimization
PRIORITY_CELLS = [
    # (MAP, RPM, rationale)
    ( 50, 2000, "Light cruise, low RPM — most miles, fuel economy gain"),
    ( 60, 2500, "Light cruise, mid RPM"),
    ( 70, 3000, "Cruise transition — engine wakes up here"),
    ( 80, 3500, "Brisk cruise"),
    ( 50, 3000, "Coasting / decel into cruise"),
    ( 40, 2000, "Light off-idle"),
    ( 90, 2500, "Just off boost"),
    (100, 3000, "Low boost, mid-range"),
    (120, 3500, "Spool zone"),
    (140, 4000, "Mid-boost mid-range"),
]

def parse_ratios(s):
    out = {}
    for part in s.split(","):
        g, r = part.split(":")
        out[int(g)] = float(r)
    return out

def cruise_speed(rpm, gear_ratio, final_drive, tire_circ_m):
    """Compute speed in km/h for given RPM in a given gear."""
    wheel_rpm = rpm / (gear_ratio * final_drive)
    return wheel_rpm * tire_circ_m * 60 / 1000  # m/min → km/h via /1000

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vehicle-gear-ratios", help='e.g. "1:3.5,2:2.0,3:1.5,4:1.2,5:1.0,6:0.83"')
    ap.add_argument("--final-drive", type=float)
    ap.add_argument("--tire-circumference-m", type=float, default=2.05)
    ap.add_argument("--sweep-min", type=float, default=0,  help="Lowest cam advance to test (°)")
    ap.add_argument("--sweep-max", type=float, default=40, help="Highest cam advance to test (°)")
    ap.add_argument("--sweep-step", type=float, default=5, help="Step size (°)")
    args = ap.parse_args()

    sweep_positions = []
    pos = args.sweep_min
    while pos <= args.sweep_max + 0.01:
        sweep_positions.append(pos)
        pos += args.sweep_step
    # Add a repeat of position 0 at the end as drift check
    sweep_positions_with_drift = sweep_positions + [args.sweep_min]

    print(f"# VVT-i street sweep plan")
    print()
    print(f"Sweep positions per cell: {sweep_positions} (then repeat {args.sweep_min}° as drift check)")
    print(f"Hold each position 15+ seconds. Confirm MAP stable before reading.")
    print()
    print(f"## Cells to test (in priority order)\n")

    have_speeds = bool(args.vehicle_gear_ratios and args.final_drive)
    ratios = parse_ratios(args.vehicle_gear_ratios) if args.vehicle_gear_ratios else None

    for i, (m, r, why) in enumerate(PRIORITY_CELLS):
        print(f"{i+1}. **{m} kPa MAP, {r} RPM** — {why}")
        if have_speeds:
            for gear, ratio in sorted(ratios.items()):
                kmh = cruise_speed(r, ratio, args.final_drive, args.tire_circumference_m)
                if 50 < kmh < 180:
                    mph = kmh * 0.621
                    print(f"     Gear {gear}: ~{kmh:.0f} km/h ({mph:.0f} mph)")
        print()

    print("## Per-cell procedure")
    print()
    print("1. Engage cruise control at the suggested speed in the suggested gear")
    print("2. Wait for MAP to stabilize at the target value (±2 kPa)")
    print("3. Apply VVT override at the first sweep position")
    print("4. Hold 15s; then step to the next position")
    print("5. After completing the sweep, repeat position 0 for the drift check")
    print("6. Save the log; run `analyze_sweep.py --log <file>`")
    print()
    print("## Constraints")
    print()
    print("- WBO must have validated (Lambda is valid == 1, typically ≥60s after start)")
    print("- Disable closed-loop fuel during the sweep (open-loop only)")
    print("- Test on a flat highway; same stretch for all cells if possible")
    print("- Repeat each cell sweep at least twice; the noise floor will be obvious")

if __name__ == "__main__":
    main()
