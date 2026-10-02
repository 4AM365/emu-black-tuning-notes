"""Decode + dedupe Supra LogAutosave .emublog3 files (Mar 1 - Sep 29 2026) -> data/eb_all.pkl (gitignored cache)."""
import sys,os,glob,pickle,hashlib,numpy as np,pandas as pd
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","..","skills","emu-black-log-emublog3","scripts")); from supra_decode_504 import read
L=r"C:/Users/WTCra/OneDrive/Documents/EMU_BLACK_V3/Supra/LogAutosave"
seen=set(); frames=[]; files=[]
for p in sorted(glob.glob(L+"/2026*.emublog3")):
    nm=os.path.basename(p)[:16]
    if not ("20260301"<=nm[:8]<="20260929"): continue
    df,rem=read(p)
    run=df[df.RPM>500]
    if len(run)<250: files.append(dict(f=nm,kept=False,why="short")); continue
    r=run.RPM.values.astype(np.int32); blocks=[hashlib.md5(r[i:i+250].tobytes()).hexdigest() for i in range(0,len(r)-249,250)]
    dup=np.mean([b in seen for b in blocks])
    if dup>0.5: files.append(dict(f=nm,kept=False,why=f"dup {dup:.0%}")); continue
    seen.update(blocks)
    df=df.astype(np.float32); df["file"]=nm; df["day"]=nm[:8]
    frames.append(df); files.append(dict(f=nm,kept=True,min=round(len(df)/1500,1)))
A=pd.concat(frames,ignore_index=True); A["file"]=A.file.astype("category"); A["day"]=A.day.astype("category")
F=pd.DataFrame(files); print(F[~F.kept].to_string()); print("kept files",F.kept.sum(),"rows",len(A))
pickle.dump((A,F),open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","data","eb_all.pkl"),"wb"))
print(A.groupby(pd.cut(A["Idle state"],[-1,0.5,1.5,2.5,3.5,10])).size())
