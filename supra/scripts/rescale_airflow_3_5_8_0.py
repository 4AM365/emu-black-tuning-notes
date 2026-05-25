"""Rescale all airflow-% tables to preserve TPS when actuator floor moves 2.4 -> 3.5.

Math:
  Preserve-TPS rule:  new% = A + B * old%
    B = (c_old - f_old) / (c_new - f_new)
    A = (f_old - f_new) / (c_new - f_new) * 100

  For [2.4, 8.0] -> [3.5, 8.0]:
    B = (8.0 - 2.4) / (8.0 - 3.5) = 5.6 / 4.5 = 1.244444
    A = (2.4 - 3.5) / 4.5 * 100   = -1.1 / 4.5 * 100 = -24.4444

  In raw ubyte (display = raw × 0.5):  new_raw = round(A/0.5 + B * old_raw) = round(-48.8889 + 1.2444 * old_raw)
  Cells below the new floor get clamped to 0.

  Additive correction (idleCustomCorrection):
    delta is in airflow-%, applied additively then converted via the same actuator range.
    ΔTPS = correction% / 100 × width.
    Preserve ΔTPS:  new = old × (c_old - f_old) / (c_new - f_new) = old × 1.2444
    No offset.
"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

f_old, f_new, c = 2.4, 3.5, 8.0
B = (c - f_old) / (c - f_new)
A_pct = (f_old - f_new) / (c - f_new) * 100
print(f"Rescale [{f_old},{c}] -> [{f_new},{c}]:")
print(f"  B (slope)        = {B:.6f}")
print(f"  A (offset, %)    = {A_pct:.6f}")
print(f"  In raw ubyte:    new_raw = round({A_pct/0.5:.4f} + {B:.4f} * old_raw)")
print(f"  Custom (delta):  new = round(old × {B:.4f})  (offset zero)")
print()

def rescale_preserve_tps(old_raw, additive=False):
    """Convert old raw byte → new raw byte using preserve-TPS rule.
    additive=True means use slope only (for delta tables like idleCustomCorrection)."""
    if additive:
        nr = old_raw * B
    else:
        nr = A_pct/0.5 + B * old_raw
    nr_round = int(round(nr))
    if not additive:
        # Clamp to >= 0 (TPS below new floor is not representable)
        if nr_round < 0: nr_round = 0
    # ubyte upper bound; sbyte handled by caller
    return nr_round

def parse_hex(s):
    """EMU sign-magnitude hex parser."""
    out = []
    for tok in s.strip().split():
        if tok.startswith("-"):
            out.append(-int(tok[1:], 16))
        else:
            out.append(int(tok, 16))
    return out

def fmt_hex(values, signed=False):
    out = []
    for v in values:
        if signed and v < 0:
            out.append(f"-{(-v):X}")
        else:
            if v < 0: v = 0  # clamp
            out.append(f"{v:X}")
    return " ".join(out)

# --- TABLES TO RESCALE ---
# Using the PROPOSED idleActiveAirflow (from the .emubt I exported today, post-fix)
ACTIVE_PROPOSED = "82 78 64 47 41 3F 3F 3F 95 8A 70 50 43 40 43 43 A2 96 7F 68 54 54 53 53 AC A2 8E 7A 7A 7A 78 78 AF A5 99 8B 87 84 82 82"

tables = [
    ("idleActiveAirflow",   ACTIVE_PROPOSED, "ubyte", 8, 5, False),
    ("idleArmedAirFlow",    "3E 48 51 57 5D 60 64 65", "ubyte", 8, 1, False),
    ("idleCrankingDC",      "A3 8E 79 64", "ubyte", 4, 1, False),
    ("overrunDBW",          "26 26 26 26 26 26 26 26", "ubyte", 8, 1, False),
    ("overrunDBW2",         "32 32 32 32 32 32 32 32", "ubyte", 8, 1, False),
    ("alsDBWTarget",        "1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E", "ubyte", 6, 4, False),
    ("alsDBWTarget2",       "1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E 1E", "ubyte", 6, 4, False),
    ("ralDBWTarget",        "14 14 14 14 14 14", "ubyte", 6, 1, False),
    ("pitLimiterDBWLimit",  "F 10 11 12 13 14 15 16 17 18", "ubyte", 10, 1, False),
    ("dbwBoostTargetLimit", "64 64 64 64 64 64", "ubyte", 6, 1, False),
    ("dbwCLTLimitTable",    "32 64 64 64 64", "ubyte", 5, 1, False),
    ("lcDBWTargetTable",    "C A 8 5 3 13 10 C 9 5 1B 16 12 D 8 22 1C 17 11 B", "ubyte", 5, 4, False),
]

print("=" * 78)
print("UNSIGNED AIRFLOW-% TABLES (preserve-TPS, clamped >= 0)")
print("=" * 78)
for name, data, storage, w, h, signed in tables:
    raw = parse_hex(data)
    new = [rescale_preserve_tps(r) for r in raw]
    print(f"\n{name}  ({w}×{h}, scale 0.5)")
    print(f"  OLD display %: {[f'{r*0.5:.1f}' for r in raw[:8]]}{'...' if len(raw)>8 else ''}")
    print(f"  NEW display %: {[f'{r*0.5:.1f}' for r in new[:8]]}{'...' if len(new)>8 else ''}")
    print(f"  OLD hex: {data}")
    print(f"  NEW hex: {fmt_hex(new)}")
    # Note any clamps
    clamps = sum(1 for n in new if n == 0 and (rescale_preserve_tps.__wrapped__ if False else 0) is None)
    underflow = sum(1 for r,n in zip(raw,new) if (A_pct/0.5 + B*r) < 0)
    if underflow:
        print(f"  ⚠ {underflow}/{len(raw)} cells clamped to 0 (were below new TPS floor)")

# Signed additive correction (different rule: slope only, no offset)
print()
print("=" * 78)
print("ADDITIVE CORRECTION (slope-only rescale)")
print("=" * 78)
ic_data = "2 0 -A -1F -28 2 0 -9 -1A -23 2 0 -7 -16 -1E 2 0 -5 -F -14 1 0 -3 -A -E"
ic_raw = parse_hex(ic_data)
ic_new = [rescale_preserve_tps(r, additive=True) for r in ic_raw]
print(f"\nidleCustomCorrection (5×5, sbyte, scale 0.5)")
print(f"  OLD: {[f'{r*0.5:.1f}' for r in ic_raw]}")
print(f"  NEW: {[f'{r*0.5:.1f}' for r in ic_new]}")
print(f"  OLD hex: {ic_data}")
print(f"  NEW hex: {fmt_hex(ic_new, signed=True)}")
print("  ⚠ Confirm this table is in ADDITIVE mode (not multiplicative scalar).")
print("    If multiplicative, do NOT rescale — multiplier is range-independent.")

# Scalar update
print()
print("=" * 78)
print("SCALAR UPDATE")
print("=" * 78)
print(f"  idleDBWTargetMin:  24 (=2.4%)  →  35 (=3.5%)")
print(f"  idleDBWTargetMax:  80 (=8.0%)  →  80 (unchanged)")
