"""Decode Supra .emublog3 (504-byte records, 25 Hz) -> DataFrame. Layout pinned 2026-10-02 against
drive_home_today.csv (04-08) and all-channel-reference.csv (05-30), R^2 = 1.000 on every channel below."""
import zlib, numpy as np, pandas as pd
REC = 504
def u8(A,o): return A[:,o].astype(float)
def i8(A,o): return A[:,o].astype(np.int8).astype(float)
def u16(A,o): return (A[:,o].astype(np.int32)|(A[:,o+1].astype(np.int32)<<8)).astype(float)
CH = {"RPM":lambda A:u16(A,63), "MAP":lambda A:u16(A,66)/256, "Boost":lambda A:u8(A,97), "Boost Target":lambda A:u16(A,162)/256,
      "Boost DC":lambda A:u16(A,160)/512, "TPS":lambda A:u16(A,71)/10, "PPS":lambda A:u16(A,75)/10, "CLT":lambda A:u8(A,191),
      "IAT":lambda A:u16(A,98)/256, "EGT 1":lambda A:u16(A,106), "EGT 2":lambda A:u16(A,108), "Injectors PW":lambda A:u16(A,120)*0.01613,
      "Idle target":lambda A:u16(A,111), "Ignition Angle":lambda A:i8(A,95)/2, "Ethanol content":lambda A:u16(A,195)/512,
      "Short term trim":lambda A:i8(A,128)/16-4, "Idle state":lambda A:u16(A,379)/256, "Data changing":lambda A:u16(A,473)/32768,
      "Lambda 1":lambda A:u16(A,449)/1024, "Lambda is valid":lambda A:u8(A,363)/12}
for c in range(1,7):
    CH[f"Knock voltage peak cyl {c}"]=(lambda c: lambda A:u8(A,404+c)*5/255)(c)
    CH[f"Injector {c} trim"]=(lambda c: lambda A:u8(A,226+c))(c)
def read(path):
    b=open(path,"rb").read(); d=zlib.decompressobj(16+zlib.MAX_WBITS)
    try: out=d.decompress(b)
    except zlib.error: out=b""
    k=len(out)//REC
    A=np.frombuffer(out[:k*REC],dtype=np.uint8).reshape(k,REC)
    df=pd.DataFrame({n:f(A) for n,f in CH.items()}); df.insert(0,"TIME",np.arange(k)*0.04)
    return df, len(out)%REC
