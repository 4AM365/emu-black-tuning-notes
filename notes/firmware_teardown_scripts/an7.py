import os,struct
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
L=lambda n: open(os.path.join(FW,n),'rb').read()
names=["emuBlack_3_051.bin","emuBlack_3_052.bin","emuBlack_3_053.bin","emuBlack_3_054.bin",
       "emuBlack_3_055.bin","emuBlack_3_056.bin","emuBlack_3_057.bin","emuBlack_3_058.bin",
       "emuBlack_3_059.bin","emuBlack_3_060.bin","emuBlack_3_061.bin"]
F={n:L(n) for n in names}
print("=== exact differing offsets, 059 vs 060 vs 061 (body offsets, +28 for file) ===")
a,b,d=F["emuBlack_3_059.bin"][28:],F["emuBlack_3_060.bin"][28:],F["emuBlack_3_061.bin"][28:]
for i in range(len(a)):
    if not(a[i]==b[i]==d[i]):
        print("  body %#08x (file %#08x): 059=%02x 060=%02x 061=%02x"%(i,i+28,a[i],b[i],d[i]))
print()
print("=== consecutive-version prefix agreement (position-keyed keystream test) ===")
for i in range(len(names)-1):
    x=F[names[i]][28:]; y=F[names[i+1]][28:]
    n=min(len(x),len(y))
    pre=0
    while pre<n and x[pre]==y[pre]: pre+=1
    diff=sum(1 for k in range(n) if x[k]!=y[k])
    print("  %s -> %s  len %6d/%6d  common prefix %7d  bytes differing in overlap %6d (%.1f%%)"%(
        names[i][9:14],names[i+1][9:14],len(x),len(y),pre,diff,100*diff/n))
