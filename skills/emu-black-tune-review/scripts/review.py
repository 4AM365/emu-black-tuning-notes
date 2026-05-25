"""Review an EMU Black tune file against codified best-practice checks.

Usage:
  python review.py --tune <file.emub3> [--out-md <path>]

Produces a structured report. Each check is independent and contributes 0+ findings.
The report is markdown so it can be saved or piped to a viewer.
"""
import argparse, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Tune parsing helpers (subset of emu-black-tune; intentional duplication
# so this skill is standalone) ──────────────────────────────────────────────
def parse_emu_hex(s):
    out = []
    for tok in s.strip().split():
        if tok.startswith("-"):
            out.append(-int(tok[1:], 16))
        else:
            out.append(int(tok, 16))
    return out

def get_symbol(xml, name):
    m = re.search(rf'<symbol name="{name}"[^/]*?/>', xml)
    if not m: return None
    blob = m.group(0)
    out = {"name": name}
    for k in ["value", "storage", "width", "height", "type", "data"]:
        mm = re.search(rf'{k}="([^"]*)"', blob)
        if mm: out[k] = mm.group(1)
    return out

def decode_table(xml, name, scale=1.0):
    s = get_symbol(xml, name)
    if not s or "data" not in s: return None
    raw = parse_emu_hex(s["data"])
    return [v * scale for v in raw], int(s.get("width", len(raw))), int(s.get("height", 1))

def get_scalar(xml, name):
    s = get_symbol(xml, name)
    if not s or "value" not in s: return None
    try: return int(s["value"])
    except ValueError: return float(s["value"])

# ── Finding accumulator ─────────────────────────────────────────────────────
class Findings:
    def __init__(self):
        self.solid = []     # (area, msg, ref)
        self.discuss = []   # (area, msg, ref, action)
        self.gap = []       # (area, msg, ref)

    def ok(self, area, msg, ref=""):
        self.solid.append((area, msg, ref))
    def discuss_(self, area, msg, ref, action=""):
        self.discuss.append((area, msg, ref, action))
    def gap_(self, area, msg, ref=""):
        self.gap.append((area, msg, ref))

# ── Individual checks ───────────────────────────────────────────────────────
def check_idle_pid_limits(xml, F):
    pid_min = get_scalar(xml, "idleAirPIDOutMin")
    pid_max = get_scalar(xml, "idleAirPIDOutMax")
    int_min = get_scalar(xml, "idleAirFlowIntegralLimitMin")
    int_max = get_scalar(xml, "idleAirFlowIntegralLimitMax")
    if pid_min is None or pid_max is None: return
    asym = abs(abs(pid_max) - abs(pid_min))
    if asym > 4:
        F.discuss_("Idle PID",
            f"PID output limits are asymmetric: min={pid_min}, max={pid_max} "
            f"(|Δ|={asym}). Often a sign of compensating for a base airflow that's too high or too low.",
            "Banish p.3470 (IAC pinned = throttle stop issue)",
            f"If PID consistently rides one limit in logs, fix the base airflow table rather than widening this side.")
    else:
        F.ok("Idle PID", f"PID output limits roughly symmetric (min={pid_min}, max={pid_max}).",
             "Banish p.3470")
    if int_min is not None and int_max is not None:
        if abs(int_min) >= abs(pid_min) or abs(int_max) >= abs(pid_max):
            F.discuss_("Idle PID",
                f"Integrator limits ({int_min}..{int_max}) are NOT narrower than PID output limits "
                f"({pid_min}..{pid_max}). Wind-up can trap the controller in a low-airflow state during a "
                f"disturbance and cause a stall.",
                "Idle stall reference (notes/idle_stall.md)",
                f"Set integrator limits to ~60–80% of the PID output limits.")

def check_idle_ignition_reserve(xml, F):
    # Decode idleIgnitionTargetTbl (sbyte 4×4, scale 0.5)
    tgt = decode_table(xml, "idleIgnitionTargetTbl", scale=0.5)
    if not tgt: return
    vals, w, h = tgt
    warm_targets = [vals[r*w + c] for r in range(1, h) for c in range(w)]
    if not warm_targets: return
    avg_warm = sum(warm_targets) / len(warm_targets)
    if avg_warm < 8 or avg_warm > 25:
        F.discuss_("Idle ignition",
            f"Idle ignition target at warm CLT averages {avg_warm:.1f}° BTDC. Hartman (p.17885) "
            f"recommends 8–20° for typical idle. Outside this range suggests something unusual.",
            "Hartman p.17885")
    else:
        F.ok("Idle ignition", f"Idle ignition target at warm CLT ~{avg_warm:.1f}° BTDC (8–20° expected).",
             "Hartman p.17885")

def check_cranking_vs_idle_airflow(xml, F):
    crank = decode_table(xml, "idleCrankingDC", scale=0.5)
    active = decode_table(xml, "idleActiveAirflow", scale=0.5)
    if not crank or not active: return
    crank_hot = crank[0][-1]    # last CLT bin (hot)
    # Warm idle cell: row 2 (mid RPM band), col 6 or 7 (warm CLT)
    vals, w, _ = active
    if w < 7: return
    warm_idle = vals[2*w + 6]   # row 2, col 6 (CLT 96°C typically)
    ratio = crank_hot / warm_idle if warm_idle > 0 else 0
    if 1.0 <= ratio <= 1.75:
        F.ok("Cranking airflow",
             f"Hot cranking airflow {crank_hot:.1f}% vs warm idle {warm_idle:.1f}% → ratio {ratio:.2f}× "
             f"(RusEFI recommends 1.25–1.75×; 1.0–1.25× also fine with armed-state taper).",
             "RusEFI cranking guidance")
    elif ratio < 1.0:
        F.discuss_("Cranking airflow",
            f"Hot cranking airflow ({crank_hot:.1f}%) is BELOW warm idle demand ({warm_idle:.1f}%). "
            f"Likely starts only with abundant spark energy. Consider raising cranking airflow to "
            f"~{warm_idle*1.2:.0f}–{warm_idle*1.5:.0f}% for margin.",
            "RusEFI cranking guidance",
            f"Try `idleCrankingDC` last cell ≥ {warm_idle*1.2:.0f}%.")
    else:
        F.discuss_("Cranking airflow",
            f"Hot cranking airflow ({crank_hot:.1f}%) is >1.75× warm idle ({warm_idle:.1f}%, "
            f"ratio {ratio:.2f}×). May produce a large step at PID handoff post-start.",
            "RusEFI cranking guidance",
            f"Verify the armed-state table tapers between these values.")

def check_cruise_lambda(xml, F):
    lam = decode_table(xml, "lambdaTable", scale=0.01)
    if not lam: return
    vals, w, h = lam
    # Cruise zone: MAP cols 3–4 (60–90 kPa typical), RPM rows 3–6 (~3000–4500 RPM)
    cruise_cells = []
    for r in range(3, min(7, h)):
        for c in range(3, min(5, w)):
            cruise_cells.append(vals[r*w + c])
    if not cruise_cells: return
    avg = sum(cruise_cells) / len(cruise_cells)
    if avg < 0.95:
        F.discuss_("Lambda — cruise",
            f"Cruise zone lambda averages {avg:.3f} — richer than stoich. Banish (p.1605) "
            f"recommends λ ≈ 1.0–1.05 for fuel economy at cruise.",
            "Banish p.1605",
            f"Try {avg + 0.04:.2f}–1.00 in cruise cells; verify drivability after.")
    elif avg > 1.07:
        F.discuss_("Lambda — cruise",
            f"Cruise zone lambda averages {avg:.3f} — quite lean. Risk of lean misfire / EGT issues.",
            "Banish p.1605")
    else:
        F.ok("Lambda — cruise", f"Cruise lambda ~{avg:.2f} (well-set).", "Banish p.1605")

def check_idle_lambda(xml, F):
    lam = decode_table(xml, "lambdaTable", scale=0.01)
    if not lam: return
    vals, w, h = lam
    # Idle zone: MAP col 0–1 (< 50 kPa), RPM rows 0–1 (low RPM)
    idle_cells = []
    for r in range(0, 2):
        for c in range(0, 2):
            idle_cells.append(vals[r*w + c])
    if not idle_cells: return
    avg = sum(idle_cells) / len(idle_cells)
    if avg < 0.85:
        F.discuss_("Lambda — idle",
            f"Idle lambda averages {avg:.3f} — bore-wash risk (Banish p.3062: < 0.85 risky).",
            "Banish p.3062",
            f"Raise idle lambda target above 0.85.")
    elif avg > 1.05:
        F.discuss_("Lambda — idle",
            f"Idle lambda averages {avg:.3f} — lean for an idle target. May cause hunting on cammed engines.",
            "Banish p.3062")
    else:
        F.ok("Lambda — idle", f"Idle lambda ~{avg:.2f} (within healthy range 0.85–1.05).",
             "Banish p.3062")

def check_warmup_lambda(xml, F):
    wl = decode_table(xml, "warmupTblLambdaCorrTbl", scale=0.01)
    wl2 = decode_table(xml, "warmupTblLambdaCorrTbl2", scale=0.01)
    wl_zero = wl is None or all(v == 0 for v in wl[0])
    wl2_zero = wl2 is None or all(v == 0 for v in wl2[0])
    if wl is None and wl2 is None: return
    if wl_zero and wl2_zero:
        F.discuss_("Warmup",
            "`warmupTblLambdaCorrTbl` (and table 2) are all zeros — no commanded lambda shift during "
            "warmup. Warmup enrichment comes purely from VE-table adders, and closed-loop trim may "
            "unwind that enrichment once WBO validates cold.",
            "Hartman p.18099",
            "Either lock out closed-loop trim below CLT 60°C, or set warmup lambda correction to bias "
            "richer (e.g. −0.08 at 0°C decaying to 0 at 70°C).")

def check_boost_pid(xml, F):
    enable = get_scalar(xml, "boostPIDEnable")
    ctype = get_scalar(xml, "boostControlType")
    if enable is None: return
    if enable == 0 and ctype is not None and ctype > 0:
        F.discuss_("Boost",
            f"`boostPIDEnable = 0` with `boostControlType = {ctype}`. Boost is open-loop "
            f"(DC table only) and will drift with IAT, baro, and wastegate spring wear.",
            "Maximum Boost ch.13; Banish p.808",
            "If intentional, no change. If oversight, enable PID and verify KP/KI/KD are non-zero.")
    elif enable == 1:
        kp = get_scalar(xml, "boostKP")
        ki = get_scalar(xml, "boostKI")
        if kp == 0 and ki == 0:
            F.discuss_("Boost",
                "Boost PID enabled but KP and KI are both 0. PID will not affect output.",
                "EMU Black architecture")
        else:
            F.ok("Boost", f"Boost PID enabled with non-zero gains (KP={kp}, KI={ki}).",
                 "EMU Black architecture")

def check_knock(xml, F):
    min_tps = get_scalar(xml, "knockActionMinTps")
    retard = get_scalar(xml, "knockMaxIgnRetard")
    retard_rate = get_scalar(xml, "knockIgnRetardRate")
    restore_rate = get_scalar(xml, "knockRestoreRate")
    if min_tps is not None:
        if min_tps > 30:
            F.discuss_("Knock",
                f"`knockActionMinTps = {min_tps}` — knock retard inactive below {min_tps}% TPS. "
                f"Part-throttle detonation (cruise under boost) won't trigger ignition retard.",
                "Hartman p.21394, Banish p.343",
                "Reduce to 20–25%. The knock signal threshold prevents false trips at light loads anyway.")
        else:
            F.ok("Knock", f"`knockActionMinTps = {min_tps}` allows protection at part throttle.",
                 "Hartman p.21394")
    if retard_rate is not None and restore_rate is not None:
        if 3 <= retard_rate <= 6 and 4 <= restore_rate <= 8:
            F.ok("Knock", f"Retard/restore rates (retard={retard_rate}, restore={restore_rate}) "
                 "are in the typical range.", "EMU Black architecture")

def check_async_acc(xml, F):
    aa = decode_table(xml, "accEnrichmentAsync", scale=1.0)
    if aa and all(v == -100 for v in aa[0]):
        F.discuss_("Accel enrichment",
            "`accEnrichmentAsync` is all −100 — async branch effectively disabled.",
            "EMU Black architecture",
            "If drivability is good, leave alone. If tip-in bog persists despite tuned sync table, "
            "investigate async.")

def check_inj_dead_time(xml, F):
    s = get_symbol(xml, "injOpeningTimeTbl")
    if not s or "data" not in s: return
    raw = parse_emu_hex(s["data"])
    w = int(s.get("width", 12))
    h = int(s.get("height", 4))
    if h < 2: return
    row0 = raw[:w]
    all_same = all(raw[r*w:(r+1)*w] == row0 for r in range(h))
    if all_same:
        F.discuss_("Injector dead time",
            f"`injOpeningTimeTbl` has identical values across all {h} rows (only voltage axis varies). "
            f"If a vacuum-referenced regulator is in use, the second axis (rail pressure / differential) "
            f"should populate as well.",
            "Injector data-sheet practice",
            "Confirm regulator type; populate row dim if differential pressure varies operationally.")

def check_rpm_limit(xml, F):
    rpm_lim = get_scalar(xml, "rpmLimit")
    if rpm_lim and rpm_lim > 9000:
        F.discuss_("Safety", f"`rpmLimit = {rpm_lim}` — verify this matches the mechanical limit of the build.",
                   "Safety practice")

def check_overrun(xml, F):
    enter = get_scalar(xml, "overrunRPMOn") or get_scalar(xml, "overrunOnRpm")
    exit_ = get_scalar(xml, "overrunRPMOff") or get_scalar(xml, "overrunOffRpm")
    # Names vary; EMU Black uses different conventions
    # Just check enrichment/decay
    enr = get_scalar(xml, "overrunFuelEnrichment")
    if enr is not None and enr > 22:
        F.discuss_("Overrun",
            f"Overrun exit enrichment = {enr}%. Banish (p.4495) warns large pulses (>20–25%) "
            f"can stumble. Consider reducing.",
            "Banish p.4495")

# ── Driver ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune", required=True)
    ap.add_argument("--out-md", help="Write report to file; default = stdout")
    args = ap.parse_args()

    xml = open(args.tune).read()
    F = Findings()

    # Run all checks
    check_idle_pid_limits(xml, F)
    check_idle_ignition_reserve(xml, F)
    check_cranking_vs_idle_airflow(xml, F)
    check_cruise_lambda(xml, F)
    check_idle_lambda(xml, F)
    check_warmup_lambda(xml, F)
    check_boost_pid(xml, F)
    check_knock(xml, F)
    check_async_acc(xml, F)
    check_inj_dead_time(xml, F)
    check_rpm_limit(xml, F)
    check_overrun(xml, F)

    # Verification gaps — these don't run checks, they're inherent reminders
    F.gap_("VVT", "VVT advance tables require dyno sweep data per Banish (p.4552). "
                  "Cannot validate from tune alone.")
    F.gap_("Ignition timing", "MBT timing per cell requires dyno + knock data per Hartman (p.17888). "
                              "Cannot validate WOT advance from tune alone.")
    F.gap_("VE table", "VE table requires log-based correction against WBO trim. Shape can be "
                       "sanity-checked but accuracy requires data.")

    # Format report
    out = []
    out.append(f"# Tune review: `{os.path.basename(args.tune)}`\n")
    out.append("## ✓ Validated as solid\n")
    if not F.solid:
        out.append("_(no automatic validations triggered — check the discussion list)_\n")
    for area, msg, ref in F.solid:
        out.append(f"- **{area}** — {msg}  \n  _Reference: {ref}_")

    out.append("\n## ⚠ Worth discussing\n")
    if not F.discuss:
        out.append("_(no findings — tune is clean against codified checks)_\n")
    for area, msg, ref, action in F.discuss:
        out.append(f"- **{area}** — {msg}  \n  _Reference: {ref}_")
        if action:
            out.append(f"  _Suggested: {action}_")

    out.append("\n## ? Verification gaps (require dyno or log data)\n")
    for area, msg, ref in F.gap:
        out.append(f"- **{area}** — {msg}")
        if ref: out.append(f"  _Reference: {ref}_")

    report = "\n".join(out)
    if args.out_md:
        os.makedirs(os.path.dirname(args.out_md) or ".", exist_ok=True)
        with open(args.out_md, "w", encoding="utf-8") as f: f.write(report)
        print(f"Wrote {args.out_md}")
    else:
        print(report)

if __name__ == "__main__":
    main()
