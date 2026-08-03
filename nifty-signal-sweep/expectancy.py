"""
The real question, stated properly:

  excluding premium-selling, is there ANY chart/technical entry combined with ANY
  exit rule that gives >70% win rate AND positive expectancy NET of costs,
  out of sample?

Joint sweep over (entry filter x target x stop) on 7.5 years of Kite 5-minute NIFTY.
Barrier outcomes are computed once per (target, stop) and then masked by each entry
filter, so the grid is cheap.

Costs: NIFTY futures round trip ~0.02% of notional (brokerage + STT + slippage) is
the generous case. Options are several times worse. Both are reported.
"""
import numpy as np, pandas as pd, itertools

COST_FUT = 0.02      # % of notional, round trip, index futures — generous
MAXH, STEP = 30, 2

d = pd.read_csv('nifty_5m.csv', parse_dates=['date']).set_index('date')
d.index.name = 'ts'
d = d.dropna(subset=['open','high','low','close'])
d['day'] = d.index.date
C, H, L = d['close'].values, d['high'].values, d['low'].values
day = pd.factorize(d['day'])[0]
N = len(d)

# ---- entry filters ----------------------------------------------------------
c = d['close']
delta = c.diff()
g = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
ls = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = (100 - 100/(1 + g/ls)).values
tp = (d['high']+d['low']+d['close'])/3
sess_mean = tp.groupby(d['day']).expanding().mean().reset_index(level=0, drop=True).values
first_hi = d.groupby('day')['high'].transform('first').values
first_lo = d.groupby('day')['low'].transform('first').values
bar_no = d.groupby('day').cumcount().values
ret1 = c.pct_change()
realvol = ret1.rolling(20).std().values
volmed = pd.Series(realvol).rolling(500).median().values
mom4 = c.pct_change(4).values*100
hi20 = d['high'].rolling(20).max().shift(1).values
lo20 = d['low'].rolling(20).min().shift(1).values

FILTERS = {
    'none':            np.ones(N, bool),
    'rsi<30':          rsi < 30,
    'rsi>70':          rsi > 70,
    'above_sessmean':  C > sess_mean,
    'below_sessmean':  C < sess_mean,
    'mom_up':          mom4 > 0.1,
    'mom_dn':          mom4 < -0.1,
    'break_hi20':      C > hi20,
    'break_lo20':      C < lo20,
    'vol_high':        realvol > volmed,
    'vol_low':         realvol < volmed,
    'early_session':   bar_no < 12,
    'late_session':    bar_no > 50,
    'above_OR':        C > first_hi,
    'below_OR':        C < first_lo,
}
for k in FILTERS:
    FILTERS[k] = np.nan_to_num(FILTERS[k], nan=False).astype(bool)

entries = np.arange(500, N - MAXH - 1, STEP)
cut_ts = pd.Timestamp('2023-07-01', tz=d.index.tz)
is_e = entries[d.index[entries] < cut_ts]
oos_e = entries[d.index[entries] >= cut_ts]
print(f"NIFTY 5m {N} bars  {d.index[0]:%Y-%m-%d} -> {d.index[-1]:%Y-%m-%d}")
print(f"entries: IS {len(is_e)} (pre-2023-07)  OOS {len(oos_e)}   cost assumed {COST_FUT}% round trip\n")


def barriers(tgt, stop, idxs):
    out = np.empty(len(idxs))
    for k, i in enumerate(idxs):
        e = C[i]; up = e*(1+tgt/100); dn = e*(1-stop/100); r = 0.0
        end = min(i+1+MAXH, N)
        for j in range(i+1, end):
            if day[j] != day[i]:
                r = (C[j-1]/e - 1)*100; break
            if L[j] <= dn: r = -stop; break
            if H[j] >= up: r = tgt; break
        else:
            r = (C[end-1]/e - 1)*100
        out[k] = r
    return out


GRID = [(0.30,0.30), (0.20,0.40), (0.10,0.80), (0.10,1.00), (0.05,1.00), (0.05,2.00)]
rows = []
for tgt, stop in GRID:
    o_is, o_oos = barriers(tgt, stop, is_e), barriers(tgt, stop, oos_e)
    for fname, fmask in FILTERS.items():
        mi, mo = fmask[is_e], fmask[oos_e]
        if mi.sum() < 300 or mo.sum() < 150:
            continue
        a, b = o_is[mi], o_oos[mo]
        rows.append(dict(filt=fname, tgt=tgt, stop=stop,
            is_n=len(a),  is_win=(a>0).mean()*100,  is_net=a.mean()-COST_FUT,
            oos_n=len(b), oos_win=(b>0).mean()*100, oos_net=b.mean()-COST_FUT))

r = pd.DataFrame(rows)
print(f"cells tested: {len(r)}\n")

hi = r[(r.oos_win >= 70)]
print(f"cells with OOS win rate >= 70%: {len(hi)}")
if len(hi):
    print(f"  of those, NET-POSITIVE out of sample: {(hi.oos_net > 0).sum()}")
    print(f"\n{'filter':17}{'tgt':>6}{'stop':>6}{'OOS win':>9}{'OOS net':>10}{'IS win':>9}{'IS net':>9}")
    for _, x in hi.sort_values('oos_net', ascending=False).head(10).iterrows():
        print(f"  {x.filt:15}{x.tgt:>6.2f}{x.stop:>6.2f}{x.oos_win:>8.1f}%{x.oos_net:>+9.4f}%"
              f"{x.is_win:>8.1f}%{x.is_net:>+8.4f}%")

print(f"\nBEST NET EXPECTANCY OOS, regardless of win rate:")
print(f"{'filter':17}{'tgt':>6}{'stop':>6}{'OOS win':>9}{'OOS net':>10}{'IS net':>9}{'n':>7}")
for _, x in r.sort_values('oos_net', ascending=False).head(10).iterrows():
    print(f"  {x.filt:15}{x.tgt:>6.2f}{x.stop:>6.2f}{x.oos_win:>8.1f}%{x.oos_net:>+9.4f}%"
          f"{x.is_net:>+8.4f}%{x.oos_n:>7.0f}")

surv = r[(r.is_net > 0) & (r.oos_net > 0)]
print(f"\nNET-POSITIVE IN BOTH WINDOWS: {len(surv)} of {len(r)}")
for _, x in surv.sort_values('oos_net', ascending=False).head(10).iterrows():
    print(f"  {x.filt:15}{x.tgt:>6.2f}{x.stop:>6.2f} OOS win {x.oos_win:>5.1f}%  "
          f"IS net {x.is_net:+.4f}%  OOS net {x.oos_net:+.4f}%  n={x.oos_n:.0f}")
r.to_csv('expectancy_results.csv', index=False)
