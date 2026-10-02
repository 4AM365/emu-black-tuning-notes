"""Scan EMU Black CSV logs for cranking events and tabulate injector PW vs time to start.

Usage: python scan_crank_events.py <folder-or-csv> [...]  -> crank_events.csv (next to this script)
Crank start = first injector pulse of a crank. With `ECU State`, the crank is the state-2 span;
without it, RPM > 0 after >= 1 s at 0, until RPM >= 450. Time to start = first pulse -> RPM >= 750.
"""
import sys, os, glob, datetime
import numpy as np, pandas as pd

WANT = ['TIME', 'RPM', 'ECU State', 'Injectors PW', 'Injectors cal. time', 'CLT', 'Ethanol content',
        'MAP', 'Battery voltage', 'Fuel pressure', 'Effective fuel pressure', 'TPS', 'PPS', 'Cranking correction']
FLOW_CC_PER_MS = 1230 / 60000          # injectorsSize at 400 kPa


def mg_per_injection(x):
    if 'Injectors cal. time' not in x:
        return np.nan
    net = (x['Injectors PW'] - x['Injectors cal. time']).clip(lower=0)
    if 'Effective fuel pressure' in x:
        dp = x['Effective fuel pressure']
    elif 'Fuel pressure' in x:
        dp = x['Fuel pressure'] * 100 + 98 - x['MAP']
    else:
        return np.nan
    eth = x['Ethanol content'] if 'Ethanol content' in x else 14
    rho = 0.745 + 0.044 * eth / 100
    return float((net * FLOW_CC_PER_MS * np.sqrt(dp.clip(lower=0) / 400) * rho * 1000).mean())


def events(path):
    h = pd.read_csv(path, sep=';', nrows=0)
    cols = {c.strip(): c for c in h.columns}
    if not {'TIME', 'RPM', 'Injectors PW'} <= cols.keys():
        return []
    df = pd.read_csv(path, sep=';', usecols=[cols[c] for c in WANT if c in cols], low_memory=False)
    df.columns = df.columns.str.strip()
    t, rpm, pw = df.TIME.values, df.RPM.values, df['Injectors PW'].values
    dt = float(np.median(np.diff(t)))
    spans = []
    if 'ECU State' in df:
        m = (df['ECU State'].values == 2).astype(int)
        d = np.diff(np.r_[0, m, 0])
        spans = list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))
    else:
        i, n1 = 1, int(1 / dt)
        while i < len(df):
            if rpm[i] > 0 and rpm[i - 1] == 0 and (rpm[max(0, i - n1):i] == 0).all():
                j = i
                while j < len(df) and 0 < rpm[j] < 450:
                    j += 1
                spans.append((i, j)); i = j
            i += 1
    out = []
    for s, e in spans:
        fu = np.where(pw[s:e] > 0.05)[0]
        if e - s < 3 or len(fu) == 0:
            continue
        f0 = s + fu[0]
        # A logging gap (> 1 s) right after a lone pre-gap sample means the crank really began after the gap.
        gaps = np.where(np.diff(t[f0:e]) > 1.0)[0]
        if len(gaps) and t[f0 + gaps[-1]] - t[f0] < 0.25:
            f0 = f0 + gaps[-1] + 1
            fu2 = np.where(pw[f0:e] > 0.05)[0]
            if len(fu2) == 0:
                continue
            f0 += fu2[0]
        seg = df.iloc[f0:e]
        first, last = seg.iloc[:int(1 / dt)], seg.iloc[-int(0.5 / dt):]
        net = lambda x: (x['Injectors PW'] - x['Injectors cal. time']).mean() if 'Injectors cal. time' in x else np.nan
        aft = df[(df.TIME >= t[f0]) & (df.TIME <= t[f0] + 15)]
        hit = np.where(aft.RPM.values >= 750)[0]
        g = lambda c, x=seg: round(float(x[c].mean()), 1) if c in x else np.nan
        flood = bool(('PPS' in seg and seg.PPS.max() > 5) or ('TPS' in seg and seg.TPS.max() > 12))
        out.append(dict(
            date=datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d'),
            log=os.path.basename(path), t=round(t[f0], 1), CLT=g('CLT'), E=g('Ethanol content'),
            Vb=g('Battery voltage'), MAP=g('MAP'),
            PW_first1s=round(first['Injectors PW'].mean(), 2), net_first1s=round(net(first), 2),
            PW_last05s=round(last['Injectors PW'].mean(), 2), net_last05s=round(net(last), 2),
            mg_first1s=round(mg_per_injection(first), 1), mg_last05s=round(mg_per_injection(last), 1),
            crk_first=g('Cranking correction', first), crk_last=g('Cranking correction', last),
            exit_rpm=int(rpm[e]) if e < len(df) else np.nan, crank_s=round(float(t[e - 1] - t[f0]) + dt, 2),
            fuel_to_750_s=round(float(aft.TIME.values[hit[0]] - t[f0]), 2) if len(hit) else np.nan, pedal_or_flood=flood))
    return out


if __name__ == '__main__':
    paths = []
    for a in sys.argv[1:]:
        paths += sorted(glob.glob(os.path.join(a, '**', '*.csv'), recursive=True)) if os.path.isdir(a) else [a]
    rows = []
    for p in paths:
        try:
            rows += events(p)
        except Exception as ex:
            print('skip', p, ex)
    r = pd.DataFrame(rows).sort_values(['date', 'log', 't'])
    r.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crank_events.csv'), index=False)
    pd.set_option('display.width', 300); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 300)
    print(r.to_string(index=False))
