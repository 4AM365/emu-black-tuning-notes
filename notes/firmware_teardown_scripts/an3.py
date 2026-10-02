import os
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
d=open(os.path.join(FW,"emuBlack_3_061.bin"),'rb').read()
body=d[28:]
W=1024
print("windowed match-rate at shift 256 (windows >15%):")
hits=[]
for w in range(0,len(body)-256-W,W):
    m=sum(1 for i in range(w,w+W) if body[i]==body[i+256])
    r=m/W
    if r>0.15: hits.append((w,r))
print(" count of hot windows:",len(hits),"of",len(body)//W)
for w,r in hits[:25]: print("   off %#08x rate %.3f"%(w+28,r))
# longest run of period-256 equality
best=(0,0); cur=0
for i in range(len(body)-256):
    if body[i]==body[i+256]:
        cur+=1
        if cur>best[0]: best=(cur,i-cur+1)
    else: cur=0
print("longest period-256 equal run: %d bytes at body off %#x (file %#x)"%(best[0],best[1],best[1]+28))
o=best[1]
print("ciphertext there:",body[o:o+48].hex(' '))
