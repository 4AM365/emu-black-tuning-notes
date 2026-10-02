import os,struct,collections
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
d=open(os.path.join(FW,"emuBlack_3_061.bin"),'rb').read()
body=d[28:]
P=256
cols=[collections.Counter() for _ in range(P)]
for i,b in enumerate(body): cols[i%P][b]+=1
key=bytes(c.most_common(1)[0][0] for c in cols)
print("recovered key (assuming plaintext 0x00 mode):")
print(key.hex())
# how dominant is the mode?
doms=[c.most_common(1)[0][1]/sum(c.values()) for c in cols]
print("mode dominance min %.3f avg %.3f max %.3f"%(min(doms),sum(doms)/len(doms),max(doms)))
pt=bytes(b^key[i%P] for i,b in enumerate(body))
print("\nfirst 128 bytes decrypted:")
for o in range(0,128,16):
    print("%04x  %s  %s"%(o,pt[o:o+16].hex(' '),''.join(chr(x) if 32<=x<127 else '.' for x in pt[o:o+16])))
import re
strs=re.findall(rb'[ -~]{6,}',pt)
print("\nASCII strings found: %d"%len(strs))
for s in strs[:40]: print("   ",s[:70])
