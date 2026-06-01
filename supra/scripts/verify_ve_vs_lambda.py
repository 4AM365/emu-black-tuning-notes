"""Verify VE-table shape against expanded lambda targets for 05312026 supra v2.

Logic: in this build the EMU veTable is the fuel DOSE and lambdaTable is NOT
applied as a fuel multiplier (it is a reference / closed-loop target only).
So the veTable must already carry the lambda enrichment by hand.

Test: air_VE_proxy = veTable * lambda_target. If the VE shape tracks the lambda
targets, this product is a smooth air-VE surface with no kink where boost
enrichment kicks in. A dip/discontinuity in the product across the enrichment
knee = veTable did NOT get the extra fuel the new lambda targets demand.
"""

def h2i(s):
    out = []
    for tok in s.split():
        out.append(int(tok, 16))
    return out

# ---- axes ----
mapBins   = h2i("14 23 31 40 4F 5D 6C 7B 89 98 A7 B5 C4 D3 E1 F0")          # 16, kPa
rpmBins   = h2i("1F4 34A 4A0 5F6 74C 8A3 9F9 B4F CA5 DFB F51 10A7 11FD 1353 14A9 1600 1756 18AC 1A02 1B58")  # 20
mapBinsL8 = h2i("14 28 3C 50 64 82 B4 F0")                                   # 8, kPa  (lambda X)
rpmBins10 = h2i("3E8 5DC 7D0 9C4 BB8 DAC FA0 1388 1770 1B58")                # 10 (lambda Y)
ppsBoost  = h2i("0 6 1C 2A 3A 48 56 62")                                     # 8, % (boost X = pedal)
rpmBoost  = h2i("DAC FA0 1194 1388 157C 1770 1964 1B58")                     # 8 (boost Y)

# ---- tables ----
lam1 = h2i("5D 5D 5D 5D 5A 57 52 4C 5D 5D 5D 5D 5A 56 51 4C 61 61 61 61 5C 55 50 4B 64 64 64 61 5C 55 50 4B 64 64 64 60 5B 54 50 4B 64 64 64 5F 5A 53 4F 4B 64 64 63 5E 59 53 4F 4B 64 64 62 5E 58 52 4F 4A 64 63 61 5D 58 52 4E 4A 64 63 60 5C 57 51 4E 49")
lam2 = h2i("5D 5D 5D 5D 5C 5A 57 54 5D 5D 5D 5D 5C 5A 57 54 61 61 61 61 5E 5A 57 53 64 64 64 61 5E 59 56 53 64 64 64 61 5E 59 56 53 64 64 64 60 5D 58 55 52 64 64 63 5F 5C 57 55 52 64 64 62 5E 5B 56 54 52 64 63 61 5D 5A 55 53 51 64 63 60 5C 59 55 53 51")
ve1  = h2i("162 167 17C 1BB 213 230 23D 247 251 25B 264 269 26E 274 279 27E 174 182 1A2 1DE 22A 242 24E 258 260 26A 272 277 27C 281 286 28B 189 19F 1C7 200 240 256 262 26B 273 27B 283 288 28D 291 296 29B 19A 1BA 1EB 222 252 269 275 27C 284 28B 293 297 29C 2A0 2A4 2A9 1A9 1D2 207 23E 266 27D 287 28E 294 29A 2A1 2A5 2AA 2AE 2B2 2B7 1BD 1E6 21D 252 279 28F 299 29F 2A4 2A9 2B0 2B4 2B8 2BB 2BF 2C3 1D1 1FA 22F 263 288 29E 2A9 2AE 2B3 2B6 2BD 2C0 2C4 2C8 2CB 2CF 1E4 20E 242 273 296 2AB 2B6 2BD 2C2 2C6 2CB 2CE 2D2 2D5 2D9 2DC 1F8 223 254 282 2A3 2B7 2C3 2CB 2D0 2D4 2DA 2DD 2E0 2E3 2E6 2E9 20C 235 264 290 2AE 2C2 2CF 2D7 2DE 2E2 2E8 2EA 2ED 2F0 2F2 2F5 21A 242 271 29C 2B8 2CB 2D8 2E0 2E8 2EE 2F4 2F6 2F9 2FC 2FE 301 221 24B 27A 2A3 2C0 2D2 2DE 2E8 2F0 2F8 2FE 301 304 307 30A 30D 229 251 280 2A9 2C6 2D7 2E3 2EE 2F7 300 306 30A 30E 311 315 319 231 257 285 2AE 2CA 2DB 2E7 2F2 2FC 306 30E 312 316 31A 31E 322 238 25C 289 2B2 2CD 2DD 2E8 2F3 2FE 309 312 316 31A 31E 322 326 23B 261 28C 2B4 2CE 2DD 2E8 2F3 2FE 309 312 316 31A 31E 322 326 241 265 28F 2B4 2CD 2DB 2E6 2F0 2FA 305 30E 312 317 31B 31F 324 246 269 291 2B3 2CA 2D8 2E3 2EC 2F6 300 30A 30E 313 317 31B 320 24B 26C 293 2B3 2C8 2D6 2E0 2E9 2F2 2FC 306 30A 30F 314 318 31D 24F 26F 295 2B3 2C7 2D4 2DE 2E7 2EF 2F9 303 308 30D 311 316 31B")
ve2  = h2i("168 171 193 1C6 212 234 240 246 24A 250 255 25B 25F 263 266 26A 179 188 1AC 1E3 228 247 251 255 259 25D 262 268 26C 270 273 277 18E 19F 1C9 200 23F 25B 264 267 26A 26D 271 277 27B 27F 282 286 1A3 1BD 1EC 222 250 26C 275 278 27A 27C 280 286 28A 28E 291 295 1B6 1D2 208 23E 266 27E 286 288 28A 28B 28E 293 297 29B 29E 2A2 1C8 1E4 21C 253 27A 290 298 29A 29A 29A 29C 2A0 2A4 2A8 2AB 2AF 1D9 1F9 22F 264 28A 29F 2A7 2AA 2AA 2AA 2AA 2AD 2B1 2B5 2B8 2BC 1EB 20F 242 273 297 2AB 2B4 2B7 2B8 2B8 2B8 2BA 2BE 2C2 2C5 2C9 1FD 223 254 282 2A3 2B6 2BF 2C4 2C6 2C6 2C6 2C6 2CA 2CE 2D1 2D5 20E 235 265 290 2AF 2C0 2CA 2CF 2D1 2D3 2D3 2D3 2D7 2DB 2DE 2E2 21B 242 272 29B 2B8 2C9 2D3 2D8 2DB 2DC 2DC 2DC 2E0 2E4 2E7 2EB 221 24B 27A 2A3 2BF 2CF 2D8 2DE 2E2 2E6 2E8 2E8 2EC 2F0 2F3 2F7 229 251 280 2A8 2C4 2D3 2DD 2E3 2E8 2EE 2F3 2F5 2F9 2FD 300 304 231 257 285 2AD 2C7 2D6 2E0 2E6 2ED 2F5 2FC 2FE 302 306 309 30D 238 25D 289 2B0 2C8 2D7 2E0 2E8 2EF 2F8 300 303 307 30B 30E 312 23B 261 28C 2B1 2C9 2D7 2E0 2E8 2EF 2F8 300 304 308 30C 30F 313 241 265 28F 2B1 2C7 2D3 2DC 2E3 2EB 2F4 2FD 303 307 30B 30E 312 246 269 290 2B0 2C4 2CE 2D7 2DF 2E7 2F0 2F9 300 304 308 30B 30F 24B 26C 292 2B0 2C1 2CA 2D2 2DA 2E3 2EC 2F6 2FE 302 306 309 30D 24F 26F 294 2B0 2BF 2C7 2CF 2D7 2E0 2E9 2F3 2FC 300 304 307 30B")
bt1  = h2i("0 4 16 21 2D 38 43 4D 0 4 16 21 2D 38 43 4D 0 4 16 21 2D 38 43 4D 0 4 16 21 2D 38 43 4D 0 4 16 21 2D 38 43 4D 0 4 17 23 30 3C 48 53 0 4 19 26 34 40 4C 58 0 4 1A 28 37 44 51 5E")
bt2  = h2i("0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82 0 8 25 38 4D 60 72 82")
boostEthanolBlend = h2i("64 56 48 37 23 E 3 0 0")  # weight % of target1 across ethanol bins
ethBins = h2i("0 19 32 4B 64 7D 96 AF C8")  # 0/25/50/75/100/125/150/175/200 -> /2 = ethanol %? see below

def grid(flat, w):
    return [flat[i*w:(i+1)*w] for i in range(len(flat)//w)]

LAM1 = grid(lam1, 8)   # [rpm10][map8]
LAM2 = grid(lam2, 8)
VE1  = grid(ve1, 16)   # [rpm20][map16]
VE2  = grid(ve2, 16)
BT1  = grid(bt1, 8)    # [rpm8][pps8]
BT2  = grid(bt2, 8)

def interp1(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i+1]:
            t = (x - xs[i]) / (xs[i+1] - xs[i])
            return ys[i] + t*(ys[i+1]-ys[i])
    return ys[-1]

def lam_at(LAM, mapv, rpmv):
    # interp over map (cols) then rpm (rows)
    row_vals = []
    for r in range(len(rpmBins10)):
        row_vals.append(interp1(mapv, mapBinsL8, LAM[r]))
    return interp1(rpmv, rpmBins10, row_vals) / 100.0

# ---- E60 blended lambda target onto VE grid, product smoothness test ----
# ethBins raw/2 = ethanol %. boostEthanolBlend weight for target1.
print("Ethanol bins (%):", [e/2 for e in ethBins])
print("boostEthanolBlend (target1 weight %):", boostEthanolBlend)

# lambda blend: build E60 lambda by blending lam1/lam2 via tblsFFLambdaBlend
ffLam = h2i("C8 B8 A7 93 7C 64 47 26 0")  # target1 weight, scale 0.5 -> %
print("tblsFFLambdaBlend (t1 weight %, raw*0.5):", [v*0.5 for v in ffLam])
# E60 -> ethanol 60%. ethBins/2 = [0,12.5,25,37.5,50,62.5,75,87.5,100]
ethPct = [e/2 for e in ethBins]
w1_60 = interp1(60, ethPct, [v*0.5 for v in ffLam]) / 100.0
print(f"E60 target1 (pump) weight = {w1_60:.3f}, target2 (eth) weight = {1-w1_60:.3f}")

def lamE60(mapv, rpmv):
    return w1_60*lam_at(LAM1, mapv, rpmv) + (1-w1_60)*lam_at(LAM2, mapv, rpmv)

VE_SCALE = 0.1
print("\n=== Product test: veTable*lambda (air-VE proxy) across MAP at each RPM ===")
print("Looking for monotonic-smooth rise then plateau; a DIP at the boost knee = mismatch.\n")
# Use ve1 (pump) with E0 lambda for clean single-fuel check, and E60 blend for ve-as-shipped
for label, VE, lamfun in [("VE1 x lam1(E0)", VE1, lambda m,r: lam_at(LAM1,m,r)),
                          ("VE1 x lamE60", VE1, lamE60),
                          ("VE2 x lam2(E100)", VE2, lambda m,r: lam_at(LAM2,m,r))]:
    print(f"--- {label} ---")
    print("RPM   " + " ".join(f"{m:>4}" for m in mapBins) + "   (MAP kPa)")
    for ri in range(0, 20, 3):
        rpmv = rpmBins[ri]
        prod = []
        for ci, mapv in enumerate(mapBins):
            p = VE[ri][ci]*VE_SCALE * lamfun(mapv, rpmv)
            prod.append(p)
        print(f"{rpmv:>5} " + " ".join(f"{p:4.0f}" for p in prod))
    print()

# ---- boost vs TPS: confirm X axis = pedal/TPS, show E60 boost target ----
print("=== Boost target vs TPS (pedal) — confirms boost referenced to TPS ===")
print("X = pedal %:", ppsBoost)
print("E60 blended boost target (kPa), rows = RPM:")
print("RPM   " + " ".join(f"{p:>4}" for p in ppsBoost) + "  (pedal %)")
for ri in range(8):
    row = []
    for ci in range(8):
        b = w1_60*BT1[ri][ci] + (1-w1_60)*BT2[ri][ci]
        row.append(b)
    print(f"{rpmBoost[ri]:>5} " + " ".join(f"{b:4.0f}" for b in row))
