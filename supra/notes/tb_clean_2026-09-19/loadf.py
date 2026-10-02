import pandas as pd, numpy as np
COLS=['TIME','RPM','Idle target','TPS','TPS voltage','DBW Out. DC','DBW target','DBW Target source','Idle state','Idle air %','Idle PID air % correction','Idle ignition correction','Idle ignition target','Ignition Angle','CLT','IAT','MAP','Baro','Engine oil pressure','Engine oil pressure status','Battery voltage','Driven axle speed','Lambda 1','Lambda is valid','Short term trim','PPS','Data changing','Making permanent','AC Clutch','Coolant fan','Fuel temp.','Estimated airflow','Injectors PW','VE','Afterstart Enrichment','Warmup enrichment','Fuel Cut','Overrun status','Idle ramp down offset','ECU State']
def load():
    p=r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\fullchannels.csv"
    hdr=open(p,encoding='utf-8',errors='replace').readline().strip().split(';')
    use=[c for c in COLS if c in hdr]
    df=pd.read_csv(p,sep=';',usecols=use,low_memory=False)
    df['MR']=df.MAP*df.RPM/1000; df['err']=df.TPS-df['DBW target']
    return df
