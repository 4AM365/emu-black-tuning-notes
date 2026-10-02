"""Extract steady held-idle segments from an EMU Black CSV and report the airflow requirement.

Requirement is read as TOTAL commanded `Idle air %` while RPM is genuinely held — that is the
mass-flow command (the idle throttle is choked at idle MAP, so air% is flow and MAP is air/cycle;
see supra/notes/oil_viscosity_idle_airflow.md Result 12.1).

Also reports `bf = air - custom - PID` = base + fan, which reveals live table edits mid-log.

Usage:  python idle_steady_segments.py <log.csv> [<log.csv> ...]
"""
import sys
import pandas as pd

RATE_HZ = 25
WIN = 3 * RATE_HZ  # 3 s


def load(path):
    df = pd.read_csv(path, sep=';')
    df.columns = [c.strip() for c in df.columns]
    return df.dropna(axis=1, how='all')


def segments(df):
    df = df[df.RPM > 0].reset_index(drop=True)
    air, pid = df['Idle air %'], df['Idle PID air % correction']
    cust = df.get('Idle airflow custom corr.', pd.Series(0.0, index=df.index))
    df = df.assign(air=air, pid=pid, cust=cust, bf=air - cust - pid)

    sd = df.RPM.rolling(WIN, center=True, min_periods=WIN * 4 // 5).std()
    slope = df.RPM.rolling(WIN, center=True, min_periods=WIN * 4 // 5).apply(
        lambda v: (v[-15:].mean() - v[:15].mean()) / 3.0, raw=True)
    asd = df.air.rolling(WIN, center=True, min_periods=WIN * 4 // 5).std()

    ok = ((df['Idle state'] == 2) & (sd < 22) & (slope.abs() < 12) & (asd < 3.0)
          & (df.MAP < 50) & (df.TPS < 8.2))
    grp = (ok != ok.shift()).cumsum()

    rows = []
    for _, s in df[ok].groupby(grp[ok]):
        if len(s) < WIN:
            continue
        rpm = s.RPM.median()
        rows.append(dict(
            t0=round(s.TIME.iloc[0], 1), dur=round(s.TIME.iloc[-1] - s.TIME.iloc[0], 1), n=len(s),
            RPM=round(rpm), CLT=s.CLT.median(),
            OP=round(s['Engine oil pressure'].median(), 2) if 'Engine oil pressure' in s else None,
            air=round(s.air.median(), 1), pid=round(s.pid.median(), 1),
            cust=round(s.cust.median(), 1), bf=round(s.bf.median(), 2),
            MAP=round(s.MAP.mean(), 1), TPS=round(s.TPS.median(), 2),
            # torque-demand proxy: air% is mass flow, so per-cycle demand is flow/rpm
            spec_air=round(s.air.median() / rpm * 1000, 1)))
    return pd.DataFrame(rows)


if __name__ == '__main__':
    pd.set_option('display.width', 300)
    for path in sys.argv[1:]:
        print(f'=== {path} ===')
        print(segments(load(path)).to_string(index=False))
        print()
