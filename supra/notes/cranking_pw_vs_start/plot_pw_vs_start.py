"""Small multiples: average cranking injector PW vs time to start (first fuel -> 750 rpm), binned by CLT.

Reads crank_events.csv (from scan_crank_events.py) and writes pw_vs_start_by_clt.png next to this script.
Average PW = mean of the first-1 s and last-0.5 s PW. Cranking PW falls roughly linearly through a crank
(Will, 2026-10-02), so the mean of the two ends stands in for the whole crank (10-02 cold: 2.82 both ways).
Only cranks after the 2026-06-29 injector deadtime update (Will, 2026-10-02).
Excluded: pedal/flood-clear cranks (except 10-01 #1, whose pedal came after 5 s of hover — its end PW is the
pre-pedal 0.5 s), duplicate logs, and events with no CLT channel.
"""
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
STARTED, NOSTART = '#2a78d6', '#eb6834'          # categorical slots 1 and 2
NOSTART_Y = 10.0                                  # plotted position of "no start" (time axis tops out at 8.5)

ev = pd.read_csv(os.path.join(HERE, 'crank_events.csv'))
ev = ev[~ev.log.isin(['50hz log wont_idle.csv', 'goodrunwithvoltage.csv']) & ev.CLT.notna()]
ev = ev[ev.date >= '2026-06-29']                  # after the injector deadtime update
first_1001 = (ev.log == 'new_cranking_rules.csv') & (ev.t < 10)
ev = ev[~ev.pedal_or_flood | first_1001].copy()
ev.loc[(ev.log == 'new_cranking_rules.csv') & (ev.t < 10), 'PW_last05s'] = 2.63   # pre-pedal 8.7–9.2 s
ev['PW_avg'] = (ev.PW_first1s + ev.PW_last05s) / 2
ev['y'] = ev.fuel_to_750_s.fillna(NOSTART_Y)
ev['label'] = pd.to_datetime(ev.date).dt.strftime('%m-%d') + '  ' + ev.CLT.round().astype(int).astype(str) + '°'
ev.loc[(ev.log == 'new_cranking_rules.csv') & (ev.t > 10), 'label'] += '  (wet ports)'
ev['offset'] = [(6, 4)] * len(ev)

for (log, t0), off in {('goodrun.csv', 33.2): (-58, 6), ('goodrun.csv', 595.9): (-62, -10),
                       ('allchannels_smoothclt.csv', 82.9): (6, 6), ('wont_idle.csv', 138.9): (-62, 6),
                       ('newhotstart.csv', 2475.6): (6, 6), ('wont_idle.csv', 700.5): (6, -10)}.items():
    m = (ev.log == log) & ((ev.t - t0).abs() < 0.2)
    ev['offset'] = [off if hit else o for hit, o in zip(m, ev.offset)]

bins = [(0, 40, 'Cold  (CLT < 40 °C)'), (40, 80, 'Warm  (40–80 °C)'), (80, 130, 'Hot  (CLT > 80 °C)')]
proposed = {0: (3.90 + 2.81) / 2, 2: (3.12 + 2.99) / 2}   # new tables replayed on the 10-02 starts

plt.rcParams.update({'font.family': 'sans-serif', 'font.size': 9, 'axes.edgecolor': GRID,
                     'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2})
fig, axs = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True, facecolor=SURF)
for c, (lo, hi, title) in enumerate(bins):
    ax = axs[c]
    ax.set_facecolor(SURF)
    d = ev[(ev.CLT >= lo) & (ev.CLT < hi)]
    ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.axhspan(9.2, 10.8, color=GRID, alpha=0.5, lw=0)
    ok, no = d[d.fuel_to_750_s.notna()], d[d.fuel_to_750_s.isna()]
    ax.scatter(ok.PW_avg, ok.y, s=64, color=STARTED, edgecolor=SURF, lw=2, zorder=3, label='started')
    ax.scatter(no.PW_avg, no.y, s=72, marker='X', color=NOSTART, edgecolor=SURF, lw=1.5, zorder=3, label='no start')
    for _, p in d.iterrows():
        if p.label:
            ax.annotate(p.label, (p.PW_avg, p.y), xytext=p.offset, textcoords='offset points',
                        fontsize=7.5, color=INK2)
    if c in proposed:
        ax.axvline(proposed[c], color=INK2, lw=1.5, ls=(0, (4, 3)), zorder=2)
        ax.text(proposed[c], 8.8, ' new tables', color=INK2, fontsize=7.5, va='top')
    ax.set_xlim(2.0, 4.0); ax.set_ylim(0, 10.8)
    ax.set_yticks([0, 2, 4, 6, 8, NOSTART_Y]); ax.set_yticklabels(['0', '2', '4', '6', '8', 'no start'])
    ax.set_title(f"{title}   n = {len(d)}", loc='left', color=INK, fontsize=10, fontweight='bold')
    ax.set_xlabel('average cranking PW (ms)')
    if c == 0:
        ax.set_ylabel('first fuel → 750 rpm (s)')
axs[0].legend(loc='center right', frameon=False, fontsize=8, labelcolor=INK2)
fig.suptitle('Supra cranking PW vs time to start, by coolant temperature', x=0.01, ha='left',
             color=INK, fontsize=12, fontweight='bold')
fig.text(0.01, 0.01, 'Average PW = mean of first-1 s and last-0.5 s PW. Pedal / flood-clear cranks and logs without '
         'CLT excluded. Cranks after the 06-29 injector deadtime update only. Starts before 10-01 left Cranking at '
         '400–500 rpm.', color=INK2, fontsize=7.2)
fig.tight_layout(rect=(0, 0.04, 1, 0.95))
fig.savefig(os.path.join(HERE, 'pw_vs_start_by_clt.png'), dpi=150, facecolor=SURF)
print(ev[['date', 'log', 'CLT', 'PW_avg', 'fuel_to_750_s']].round(2).to_string(index=False))
