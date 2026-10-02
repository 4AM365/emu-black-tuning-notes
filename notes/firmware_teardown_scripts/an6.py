import os
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
L=lambda n: open(os.path.join(FW,n),'rb').read()
a=L("emuBlack_3_059.bin")[28:]; b=L("emuBlack_3_060.bin")[28:]; d=L("emuBlack_3_061.bin")[28:]
for n1,n2,x,y in (("059","060",a,b),("060","061",b,d),("059","061",a,d)):
    z=bytes(p^q for p,q in zip(x,y))
    nz=sum(1 for v in z if v)
    # longest zero run
    best=cur=0
    for v in z:
        cur = cur+1 if v==0 else 0
        best=max(best,cur)
    print("%s^%s: %d/%d bytes differ (%.2f%%)  longest identical run: %d bytes"%(n1,n2,nz,len(z),100*nz/len(z),best))
