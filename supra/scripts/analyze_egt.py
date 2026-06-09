import pandas as pd, numpy as np

df = pd.read_csv(r'C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\all-channels-reduced-idlaircorr.csv', sep=';')
df.columns = df.columns.str.strip()

out = []
def p(*a):
    out.append(' '.join(str(x) for x in a))

p('rows', len(df), 'duration %.1fs' % (df['TIME'].iloc[-1]-df['TIME'].iloc[0]))
p('ECU State:', dict(df['ECU State'].value_counts()))
p('Lambda valid:', dict(df['Lambda is valid'].value_counts()))

# Identify active EGT channels
egt_all = ['CAN EGT '+str(i) for i in range(1,9)] + ['EGT 1','EGT 2']
p('\n=== EGT channel activity ===')
active_egt = []
for c in egt_all:
    v = df[c]
    nz = (v != 0).sum()
    if nz > 100:
        active_egt.append(c)
    p(f'{c}: mean {v.mean():.0f} max {v.max():.0f} nonzero {nz}')
p('active EGT:', active_egt)

# Running + warmed: ECU State 3, CLT>70, and EGTs sane (>200)
run = df[(df['ECU State']==3) & (df['CLT']>70)].copy()
p('\n=== Warm running rows: %d ===' % len(run))

# EGT evenness on warm running where all active EGTs > 300
if active_egt:
    mask = run[active_egt].gt(300).all(axis=1)
    egtw = run[mask]
    p('rows with all EGT>300: %d' % len(egtw))
    p('\n=== EGT evenness (warm, all firing) ===')
    means = {}
    for c in active_egt:
        means[c] = egtw[c].mean()
        p(f'{c}: mean {egtw[c].mean():.0f} median {egtw[c].median():.0f} p95 {egtw[c].quantile(.95):.0f}')
    mv = np.array(list(means.values()))
    p('spread mean-to-mean: %.0f C  (min %.0f / max %.0f)' % (mv.max()-mv.min(), mv.min(), mv.max()))

# Lambda tracking
p('\n=== Lambda tracking (warm, valid) ===')
lv = df[(df['ECU State']==3) & (df['Lambda is valid']==1)].copy()
for tc in ['Lambda target','Lambda target from table']:
    if tc in lv: p(tc,'mean %.3f'%lv[tc].mean())
for mc in ['Lambda 1','Lambda 2']:
    p(mc,'mean %.3f'%lv[mc].mean())
lv['err1'] = lv['Lambda 1'] - lv['Lambda target']
lv['err2'] = lv['Lambda 2'] - lv['Lambda target']
p('Lambda1 - target: mean %.3f  std %.3f  absmean %.3f' % (lv['err1'].mean(), lv['err1'].std(), lv['err1'].abs().mean()))
p('Lambda2 - target: mean %.3f  std %.3f  absmean %.3f' % (lv['err2'].mean(), lv['err2'].std(), lv['err2'].abs().mean()))
p('Short term trim: mean %.2f std %.2f'%(lv['Short term trim'].mean(), lv['Short term trim'].std()))

# Per-injector trims
p('\n=== Injector trims (warm running) ===')
for i in range(1,9):
    c='Injector %d trim'%i
    if c in run:
        v=run[c]
        if (v!=0).any():
            p(f'{c}: mean {v.mean():.2f} min {v.min():.2f} max {v.max():.2f}')

# Break by load region
p('\n=== Lambda error by MAP band (warm valid) ===')
bins=[0,50,100,150,250]
lv['band']=pd.cut(lv['MAP'],bins)
for b,g in lv.groupby('band',observed=True):
    if len(g)<20: continue
    p(f'MAP{b}: n {len(g)} tgt {g["Lambda target"].mean():.3f} L1 {g["Lambda 1"].mean():.3f} L2 {g["Lambda 2"].mean():.3f} err1 {(g["Lambda 1"]-g["Lambda target"]).mean():+.3f} err2 {(g["Lambda 2"]-g["Lambda target"]).mean():+.3f}')

with open('egt_results.txt','w') as f:
    f.write('\n'.join(out))
print('written')
