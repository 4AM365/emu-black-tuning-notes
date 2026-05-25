"""Decode specific tune tables to display-value form for review."""
import re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TUNE = os.path.join(os.path.dirname(__file__), "..", "tunes", "supra tune export 05242026.xml.emub3")
xml = open(TUNE).read()

def get(symname):
    m = re.search(rf'<symbol name="{symname}"[^/]*?/>', xml)
    if not m: return None
    blob = m.group(0)
    out = {"name": symname}
    for k in ["value","storage","width","height","type","data"]:
        mm = re.search(rf'{k}="([^"]*)"', blob)
        if mm: out[k] = mm.group(1)
    return out

def hex_to_signed(h, bits):
    v = int(h, 16)
    if h.startswith("-"): return -int(h[1:], 16)  # EMU's sign-magnitude
    return v

def parse_data(data, storage):
    if not data: return []
    toks = data.strip().split()
    out = []
    for t in toks:
        if t.startswith("-"):
            out.append(-int(t[1:], 16))
        else:
            out.append(int(t, 16))
    return out

def show(symname, scale=1, label=None, fmt="%.2f"):
    s = get(symname)
    if not s:
        print(f"  [missing] {symname}")
        return
    if "data" in s:
        vals = parse_data(s["data"], s.get("storage","ubyte"))
        scaled = [v*scale for v in vals]
        w = int(s.get("width") or len(vals))
        h = int(s.get("height") or 1)
        print(f"  {label or symname}  storage={s['storage']}  {w}×{h}  scale={scale}")
        for r in range(h):
            row = scaled[r*w:(r+1)*w]
            print("    " + " ".join(fmt%v for v in row))
    else:
        print(f"  {label or symname} = {s.get('value','?')} ({s.get('storage','?')}, scale={scale})")

print("="*72)
print("AXIS BINS")
print("="*72)
show("rpmBins", 1, "rpmBins"); show("mapBins", 1, "mapBins")
show("cltBins8", 1, "cltBins8"); show("cltBins", 1, "cltBins (main, 16)")
show("tpsBins", 0.1, "tpsBins (%)"); show("ppsBins", 0.1, "ppsBins (%)")
show("flexFuelEthanolContentBins", 0.5, "Ethanol bins (%)")

print()
print("="*72); print("LAMBDA TARGETS"); print("="*72)
# Lambda table is ubyte; values like 5D = 93 → 0.93. So scale is /100.
show("lambdaTable", 0.01, "lambdaTable (E0 endpoint)")
show("lambdaTable2", 0.01, "lambdaTable2 (E100 endpoint)")
show("tblsFFLambdaBlend", 0.5, "FF Lambda blend (%)")

print()
print("="*72); print("VE TABLES"); print("="*72)
# VE u12 typical scale 0.1 (display 0-200%). Check first value.
show("veTable", 0.1, "veTable (table 1, ~%) — first 10 rows")
show("veTable2", 0.1, "veTable2 (table 2, ~%)")

print()
print("="*72); print("IGNITION (already covered idle; show middle/high load)")
print("="*72)
show("ignTable", 0.5, "ignTable (E0 endpoint, °BTDC)")
show("ignTable2", 0.5, "ignTable2 (E100 endpoint, °BTDC)")
show("tblsFFIgnBlend", 0.5, "FF Ignition blend (%)")

print()
print("="*72); print("WARMUP ENRICHMENT"); print("="*72)
show("cltBinsWarmup", 1, "Warmup CLT bins (°C)")
show("warmupTbl", 1, "warmupTbl (E0)")
show("warmupTbl2", 1, "warmupTbl2 (E100)")
show("tblsFFWarmupBlend", 0.5, "FF Warmup blend (%)")
show("warmupTblLambdaCorrTbl", 0.01, "Warmup lambda correction (E0)")
show("warmupTblLambdaCorrTbl2", 0.01, "Warmup lambda correction (E100)")

print()
print("="*72); print("ASE (Afterstart enrichment)"); print("="*72)
show("aseCltBins", 1, "ASE CLT bins (°C)"); show("aseRuntimeBin", 1, "ASE runtime bin (revs?)")
show("aseTbl", 1, "aseTbl (E0)")
show("aseTbl2", 1, "aseTbl2 (E100)")
show("tblsFFASEBlend", 0.5, "FF ASE blend (%)")

print()
print("="*72); print("VVT (CAM1)"); print("="*72)
show("vvtiMapBins10", 1, "VVT MAP bins"); show("vvtiRpmBins10", 1, "VVT RPM bins")
show("cam1AdvTblB", 1, "Cam1 advance target (E0)")
# Other cam tables?
for n in ["cam1AdvTblA","cam1AdvTbl","cam1AdvBoost","cam1AdvBoostTbl"]:
    if get(n): show(n, 1, n)

print()
print("="*72); print("BOOST CONTROL"); print("="*72)
for s in ["boostTargetTable","boostTarget","boostDCTbl","boostBaseDC","boostPIDKP","boostPIDKI","boostPIDKD",
         "boostKnockRetard","boostPIDMin","boostPIDMax","boostControlMode","boostGear","boostGearTbl",
         "ewgDuty","ewgTbl","wastegateBaseDC","boostTargetCLTCorrection"]:
    s_o = get(s)
    if s_o:
        scale = 0.1 if "Target" in s and "table" in s.lower() else 1
        show(s, scale, s)

# Try common names
print("--- searching for boost target table ---")
for sym in [r["name"] if isinstance(r,dict) else r for r in [get(n) for n in [
    "boostTargetTbl","boostTargetTbl2","boostBaseTable","boostBaseDCTbl","boostTblTbl",
    "boostMaxBoostMap","boostMapTarget"]] if r]:
    show(sym, 1, sym)

print()
print("="*72); print("ACCELERATION ENRICHMENT (transient)"); print("="*72)
for s in ["accEnrichRPMBins","accEnrichTPSBins","accEnrichTbl","accEnrichRate","accEnrichDecay",
         "accEnrichMin","accEnrichAsyncTbl","accEnrichAsyncRPMBins","accEnrichCltCorr",
         "accEnrichTime","accEnrichMaxTime","accEnrichMinTPSRate"]:
    if get(s): show(s, 1, s)

print()
print("="*72); print("KNOCK CONTROL"); print("="*72)
for s in ["knockAdaptiveLearn","knockBaseLevel","knockBaseLevelTbl","knockRetardRate","knockRetardMax",
         "knockMaxRetardCyl","knockNoiseTable","knockSensitivity","knockGate","knockRPMBins",
         "knockMaxRetardRate","knockRecoveryRate","knockMaxAdaptive","knockThreshold","knockThresholdTbl",
         "knockAvgFilter","knockEngNoise","knockHpfFreq","knockDecimation"]:
    if get(s): show(s, 1, s)

print()
print("="*72); print("LIMITS / SAFETY"); print("="*72)
for s in ["rpmLimit","rpmLimitHardCut","fuelCutRpmLimit","sparkCutRpmLimit","mapLimit","mapLimitHardCut",
         "boostCut","cltLimit","cltLimitHardCut","iatLimit","oilPressLimit","fuelPressLimit",
         "knockShutdownLevel","wbo1FailLambdaCut","engineProtectionMaxAFR","engineProtectionMinMAP"]:
    if get(s): show(s, 1, s)

print()
print("="*72); print("INJECTOR CALIBRATION"); print("="*72)
for s in ["injectorsCalTime","injectorsBattCorr","injectorsBattCorrBins","injectorsCC","injectorsOpenTime",
         "injectorsClosingTime","injPwMinPercent","staticFlow","injCal","injSet","injSetMode"]:
    if get(s): show(s, 1, s)

print()
print("="*72); print("MISC INTERESTING SCALARS"); print("="*72)
for s in ["stoichRatio","stoichRatioTable","fuelStoich","crankingThreshold","engineDisplacement",
         "cylindersN","cylinders","fuelType","baroMinValue","battVoltMin","battVoltMax",
         "crankingPrimerPW","primingPulsePW","postStartIdleRPMIncrease","fastIdleRPM"]:
    if get(s): show(s, 1, s)
