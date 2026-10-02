import os,collections
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
c=open(os.path.join(FW,"emuBlack_3_061.bin"),'rb').read()[28:]
P=256
H=[[0]*256 for _ in range(P)]
for i,b in enumerate(c): H[i%P][b]+=1
# distribution matching: if XOR w/ 256-periodic key, hist_k(b) == hist_0(b ^ (K0^Kk))
def best_delta(a,b):
    sc=[]
    for dl in range(256):
        s=sum(a[x]*b[x^dl] for x in range(256))
        sc.append((s,dl))
    sc.sort(reverse=True)
    return sc[0],sc[1]
ratios=[]
for k in range(1,32):
    (s1,d1),(s2,d2)=best_delta(H[0],H[k])
    ratios.append(s1/s2)
    if k<8: print("  col %3d best delta %3d score ratio vs 2nd: %.4f"%(k,d1,s1/s2))
print("mean top1/top2 ratio over 31 cols: %.4f  (>1.15 => real XOR signal, ~1.0 => no signal)"%(sum(ratios)/len(ratios)))
# ECB / duplicate block detection
for bs in (8,16,32):
    blocks=collections.Counter(c[i:i+bs] for i in range(0,len(c)-bs,bs))
    dup=sum(v-1 for v in blocks.values() if v>1)
    print("  block %2d: %d duplicate blocks of %d total"%(bs,dup,len(c)//bs))
