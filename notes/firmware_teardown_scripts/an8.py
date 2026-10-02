import os,struct
FW=r"C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware"
def crc16(data,poly,init,refin,refout,xorout):
    def rb(b):
        r=0
        for i in range(8):
            if b>>i&1: r|=1<<(7-i)
        return r
    c=init
    for b in data:
        if refin: b=rb(b)
        c^=b<<8
        for _ in range(8):
            c=((c<<1)^poly)&0xFFFF if c&0x8000 else (c<<1)&0xFFFF
    if refout:
        r=0
        for i in range(16):
            if c>>i&1: r|=1<<(15-i)
        c=r
    return c^xorout
VAR={'CCITT-FALSE':(0x1021,0xFFFF,0,0,0),'XMODEM':(0x1021,0,0,0,0),'ARC':(0x8005,0,1,1,0),
     'MODBUS':(0x8005,0xFFFF,1,1,0),'KERMIT':(0x1021,0,1,1,0),'DNP':(0x3D65,0,1,1,0xFFFF),
     'CCITT-0x1D0F':(0x1021,0x1D0F,0,0,0),'MAXIM':(0x8005,0,1,1,0xFFFF),'USB':(0x8005,0xFFFF,1,1,0xFFFF)}
hits=0
for name in ["emuBlack_3_057.bin","emuBlack_3_059.bin","emuBlack_3_061.bin"]:
    d=open(os.path.join(FW,name),'rb').read()
    _,_,ver,l1,l2,c1,c2=struct.unpack('<4s6I',d[:28])
    s1=d[28:28+l1]; s2=d[28+l1:28+l1+l2]
    print("%s ver=%d hdr c1=%#06x c2=%#06x"%(name,ver,c1,c2))
    print("   sum8 s1=%#x s16 s1=%#x | sum8 s2=%#x s16 s2=%#x"%(
        sum(s1)&0xFF,sum(s1)&0xFFFF,sum(s2)&0xFF,sum(s2)&0xFFFF))
    for vn,(p,i,ri,ro,xo) in VAR.items():
        a=crc16(s1,p,i,ri,ro,xo); b=crc16(s2,p,i,ri,ro,xo)
        tag=[]
        if a==c1: tag.append("c1==CRC(sec1)")
        if b==c2: tag.append("c2==CRC(sec2)")
        if a==c2: tag.append("c2==CRC(sec1)")
        if b==c1: tag.append("c1==CRC(sec2)")
        if tag: print("   MATCH %-14s %s"%(vn,tag)); hits+=1
print("total matches:",hits)
