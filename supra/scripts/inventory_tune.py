"""Full inventory of tune symbols with classification and key value decode.
Goal: categorize all symbols so we can review every area systematically."""
import re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TUNE = os.path.join(os.path.dirname(__file__), "..", "tunes", "supra tune export 05242026.xml.emub3")
xml = open(TUNE).read()

# Parse all symbols
syms = []
for m in re.finditer(
    r'<symbol name="([^"]+)"\s*(?:value="([^"]*)")?\s*storage="([^"]+)"(?:\s+width="(\d+)"\s+height="(\d+)")?\s*(?:type="([^"]*)")?\s*(?:data="([^"]*)")?\s*/>',
    xml,
):
    name, value, storage, w, h, typ, data = m.groups()
    syms.append({
        "name": name, "value": value, "storage": storage,
        "width": int(w) if w else None, "height": int(h) if h else None,
        "type": typ, "data": data,
    })

print(f"Total symbols in tune: {len(syms)}")

# Classification by functional area
CATEGORIES = {
    "ignition_main":   ["ignTable","mapBins","rpmBins","ignBlend","FFIgn"],
    "fuel_main":       ["veTable","fuelTable","injectorsCalTime","injSet","stoichRatio"],
    "lambda":          ["lambdaTable","lambdaTarget","FFLambda","lambdaScale","wbo"],
    "cranking":        ["cranking","crankPrime"],
    "ase":             ["aseTbl","aseCltBins","aseRuntimeBin","FFASE"],
    "warmup":          ["warmup","cltBinsWarmup","FFWarmup"],
    "idle":            ["idle","cyclingIdle"],
    "dbw":             ["dbw","DBW","pedalMap","pps","tps","characteristic"],
    "boost":           ["boost","wastegate","ewg","mapTarget"],
    "vvt":             ["vvt","cam1","cam2","camAdv","camRet"],
    "knock":           ["knock"],
    "transient":       ["accEnrich","acc_enrich","decel","tipIn","trans"],
    "overrun":         ["overrun"],
    "trigger":         ["trigger","gapDetection","cam2Sens","camSync","crank2Sync"],
    "flex_fuel":       ["flexFuel","ethanol","FF","blend"],
    "limits":          ["limit","limiter","Limit","cut","Cut"],
    "fan":             ["fan","coolantFan"],
    "fuelpump":        ["fuelPump","fpr"],
    "egt":             ["egt","EGT"],
    "launch":          ["lc","launch","stage","prestage","trans_brake","transBrake","pitLimiter"],
    "als":             ["als","ALS"],
    "nitrous":         ["nos","nitrous","Nitrous"],
    "shift":           ["shift","paddle","gear","clutch"],
    "checksum":        ["checksum","Checksum","CRC"],
    "calibration":     ["voltage","baro","BARO","iat","clt","sensor","tempCal","Cal"],
    "outputs":         ["output","pwm","PWM","relay"],
}

def categorize(name):
    nlow = name.lower()
    hits = []
    for cat, kws in CATEGORIES.items():
        for kw in kws:
            if kw.lower() in nlow:
                hits.append(cat)
                break
    return hits or ["misc"]

cat_groups = {}
for s in syms:
    cats = categorize(s["name"])
    for c in cats:
        cat_groups.setdefault(c, []).append(s["name"])

print(f"\nCategorization summary (symbols per category):")
for c in sorted(cat_groups, key=lambda x: -len(cat_groups[x])):
    print(f"  {c:15s} {len(cat_groups[c]):3d}")

# For deep dive, print the symbol names in interesting categories that we haven't covered
print("\n=== AREAS NOT YET COVERED IN DETAIL ===")
covered = {"cranking","idle","overrun","flex_fuel"}
interesting = ["ignition_main","fuel_main","lambda","ase","warmup","dbw","boost","vvt",
               "knock","transient","trigger","limits","launch","als","egt","calibration"]
for cat in interesting:
    print(f"\n--- {cat} ({len(cat_groups.get(cat,[]))}) ---")
    for n in sorted(cat_groups.get(cat, [])):
        print(f"  {n}")
