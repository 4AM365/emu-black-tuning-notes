import os,collections
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
c=open(os.path.join(FW,"emuBlack_3_061.bin"),'rb').read()[28:]
# Assume XOR w/ 256-periodic key; assume vector table bytes at i%4==3 are 0x08 (flash addr MSB)
K={}
for j in range(1,64):
    K[4*j+3]=c[4*j+3]^0x08
# validate on the NEXT periods: positions 256..2048 with i%4==3 should also decrypt to 0x08
ok=tot=0
for i in range(256,2048):
    if i%4==3 and (i%256) in K:
        tot+=1
        if c[i]^K[i%256]==0x08: ok+=1
print("vector-table hypothesis: %d/%d (%.1f%%) of i%%4==3 decrypt to 0x08 in 0x100-0x800"%(ok,tot,100*ok/tot))
# what DO they decrypt to?
cnt=collections.Counter(c[i]^K[i%256] for i in range(256,4096) if i%4==3 and (i%256) in K)
print("distribution:",cnt.most_common(6))
print()
print("raw ciphertext c[0:64] grouped by 4:")
for o in range(0,64,16): print("  %04x %s"%(o,' '.join(c[o+k:o+k+4].hex() for k in range(0,16,4))))
print()
print("c[i]^c[i+256] for i in 0..128 (=p[i]^p[i+256]):")
x=bytes(c[i]^c[i+256] for i in range(128))
for o in range(0,128,16): print("  %04x %s"%(o,x[o:o+16].hex(' ')))
