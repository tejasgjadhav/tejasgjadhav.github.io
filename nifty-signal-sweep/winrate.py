"""
Where does a >70% win rate actually come from?

The entry-signal sweeps all failed to beat ~50%. But win rate is not a property
of the entry — it is mostly a property of the EXIT rule. Make the target small
relative to the stop and the win rate rises mechanically, with no predictive
power whatsoever.

This runs a triple-barrier test on 7.5 years of Kite 5-minute NIFTY:
  enter long every Nth bar, exit on first touch of +target / -stop,
  or at session end. Sweep target and stop. Report win rate AND expectancy.

If win rate rises while expectancy stays flat, the win rate is an artifact.
"""
import numpy as np, pandas as pd

d = pd.read_csv('nifty_5m.csv', parse_dates=['date']).set_index('date')
d.index.name = 'ts'
d = d.dropna(subset=['open', 'high', 'low', 'close'])
d['day'] = d.index.date
C, H, L = d['close'].values, d['high'].values, d['low'].values
day = pd.factorize(d['day'])[0]
N = len(d)
MAXH = 30          # give each trade up to 30 bars (2.5 hours)
STEP = 3           # subsample entries so the sweep runs in reasonable time

print(f"NIFTY 5m  {len(d)} bars  {d.index[0]:%Y-%m-%d} -> {d.index[-1]:%Y-%m-%d}")
print(f"entries every {STEP} bars, max hold {MAXH} bars, exit at session end\n")

entries = np.arange(0, N - MAXH - 1, STEP)


def run(tgt_pct, stop_pct):
    """First-touch triple barrier. Returns (win_rate, mean_return_pct, n)."""
    outs = np.empty(len(entries))
    for k, i in enumerate(entries):
        e = C[i]
        up, dn = e * (1 + tgt_pct/100), e * (1 - stop_pct/100)
        r = 0.0
        for j in range(i + 1, min(i + 1 + MAXH, N)):
            if day[j] != day[i]:                    # session end: exit at last close
                r = (C[j-1]/e - 1) * 100
                break
            if L[j] <= dn:                          # stop checked first = conservative
                r = -stop_pct
                break
            if H[j] >= up:
                r = tgt_pct
                break
        else:
            r = (C[min(i + MAXH, N-1)]/e - 1) * 100
        outs[k] = r
    return (outs > 0).mean()*100, outs.mean(), len(outs)


print(f"{'target%':>8} {'stop%':>7} {'ratio':>7} {'WIN RATE':>10} {'mean/trade':>12} {'net of 0.01% cost':>19}")
print("-"*70)
COST = 0.01   # round-trip cost as % of notional — deliberately generous for index futures
for tgt, stop in [(0.30, 0.30), (0.20, 0.40), (0.15, 0.60), (0.10, 0.80),
                  (0.10, 1.00), (0.05, 1.00), (0.05, 2.00), (0.03, 3.00)]:
    wr, mean, n = run(tgt, stop)
    flag = "  <-- over 70%" if wr >= 70 else ""
    print(f"{tgt:>8.2f} {stop:>7.2f} {stop/tgt:>6.1f}x {wr:>9.1f}% {mean:>+11.4f}% {mean-COST:>+18.4f}%{flag}")

print("\nSame sweep, but entries filtered by the best factor from the earlier sweep")
print("(session-mean distance > 0) — does a 'good' entry change the picture?\n")
tp = (d['high'] + d['low'] + d['close'])/3
sess_mean = tp.groupby(d['day']).expanding().mean().reset_index(level=0, drop=True)
filt = ((d['close']/sess_mean - 1) > 0).values
ent_all = entries
entries = np.array([i for i in ent_all if filt[i]])
print(f"filtered entries: {len(entries)} of {len(ent_all)}")
print(f"{'target%':>8} {'stop%':>7} {'WIN RATE':>10} {'mean/trade':>12}")
print("-"*45)
for tgt, stop in [(0.30, 0.30), (0.10, 1.00), (0.05, 2.00)]:
    wr, mean, n = run(tgt, stop)
    print(f"{tgt:>8.2f} {stop:>7.2f} {wr:>9.1f}% {mean:>+11.4f}%")
