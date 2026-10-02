import sys, math, collections
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
import os
d=open(os.path.join(FW,"emuBlack_3_061.bin"),'rb').read()
hdr=d[:28]; body=d[28:]
import struct
magic,fmt,ver,l1,l2,c1,c2=struct.unpack('<4s6I',hdr)
print("magic",magic,"fmt",fmt,"ver",ver,"l1",l1,"l2",l2,"c1",hex(c1),"c2",hex(c2),"sum",l1+l2+28,"filesize",len(d))
s1=body[:l1]; s2=body[l1:l1+l2]
def ent(b):
    c=collections.Counter(b); n=len(b)
    return -sum(v/n*math.log2(v/n) for v in c.values())
print("entropy sec1 %.4f  sec2 %.4f  whole %.4f"%(ent(s1),ent(s2),ent(body)))
print("distinct bytes sec1",len(set(s1)),"sec2",len(set(s2)))
# autocorrelation
print("--- autocorrelation on sec1 (top shifts) ---")
res=[]
for sh in range(1,2049):
    m=sum(1 for i in range(0,min(len(s1)-sh,60000)) if s1[i]==s1[i+sh])
    res.append((m/min(len(s1)-sh,60000),sh))
res.sort(reverse=True)
for r,sh in res[:15]: print("  shift %5d  match %.4f"%(sh,r))
