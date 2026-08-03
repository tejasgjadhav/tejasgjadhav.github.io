"""
Test 1: multi-day holds with 1-3% targets, where cost drag stops dominating.

Constraint from the user: NO FADE entries — he already runs fades. So every entry
here is momentum / breakout / trend-continuation, long only.

Daily NIFTY, 19 years, triple barrier (target / stop / max hold), IS-OOS split,
expectancy reported NET of a 0.02% futures round trip.
"""
import numpy as np, pandas as pd, yfinance as yf, itertools

COST = 0.02          # % of notional, round trip
SPLIT = '2017-01-01'
LEV = 10.6           # NIFTY futures notional / margin

df = yf.download('^NSEI', start='2007-09-17', progress=False, auto_adjust=False)
if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
df = df.dropna(subset=['Open','High','Low','Close'])
C, H, L = df['Close'].values, df['High'].values, df['Low'].values
N = len(df)

sma20  = df['Close'].rolling(20).mean().values
sma50  = df['Close'].rolling(50).mean().values
sma200 = df['Close'].rolling(200).mean().values
hi20 = df['High'].rolling(20).max().shift(1).values
hi50 = df['High'].rolling(50).max().shift(1).values
hi60 = df['High'].rolling(60).max().shift(1).values
d_ = df['Close'].diff()
g = d_.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
l_ = (-d_.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = (100 - 100/(1+g/l_)).values
mom20 = df['Close'].pct_change(20).values*100
rng = ((df['High']-df['Low'])/df['Close']*100)
narrow = (rng < rng.rolling(50).median()).values

# momentum / breakout / continuation only — no mean-reversion entries
FILTERS = {
    'break_20d_high':      C > hi20,
    'break_50d_high':      C > hi50,
    'new_60d_high':        C > hi60,
    'trend_50_200':        (C > sma50) & (sma50 > sma200),
    'mom20_pos':           mom20 > 2,
    'rsi>60':              rsi > 60,
    'brk20_in_uptrend':    (C > hi20) & (C > sma200),
    'brk20_narrow_before': (C > hi20) & narrow,
    'mom20_and_trend':     (mom20 > 2) & (C > sma200),
}
for k in FILTERS:
    FILTERS[k] = np.nan_to_num(FILTERS[k], nan=False).astype(bool)


def barrier(i, tgt, stop, maxhold):
    e = C[i]; up = e*(1+tgt/100); dn = e*(1-stop/100)
    for j in range(i+1, min(i+1+maxhold, N)):
        if L[j] <= dn: return -stop
        if H[j] >= up: return tgt
    j = min(i+maxhold, N-1)
    return (C[j]/e - 1)*100


split_i = df.index.get_indexer([pd.Timestamp(SPLIT)], method='nearest')[0]
GRID = list(itertools.product([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [5, 10, 20]))
print(f"NIFTY daily {df.index[0].date()} -> {df.index[-1].date()}  |  cost {COST}%/trade, "
      f"leverage {LEV}x, split {SPLIT}")
print(f"entries: momentum/breakout/continuation only (no fades)\n")

rows = []
for fname, fmask in FILTERS.items():
    idx = np.where(fmask)[0]
    idx = idx[(idx > 200) & (idx < N-21)]
    for tgt, stop, mh in GRID:
        outs = np.array([barrier(i, tgt, stop, mh) for i in idx])
        is_m = idx < split_i
        if is_m.sum() < 40 or (~is_m).sum() < 25: continue
        a, b = outs[is_m], outs[~is_m]
        rows.append(dict(filt=fname, tgt=tgt, stop=stop, hold=mh,
            is_n=len(a), is_win=(a>0).mean()*100, is_net=a.mean()-COST,
            oos_n=len(b), oos_win=(b>0).mean()*100, oos_net=b.mean()-COST))

r = pd.DataFrame(rows)
r['oos_margin_pct'] = r.oos_net*LEV
print(f"cells tested: {len(r)}")
print(f"net-positive OOS: {(r.oos_net>0).sum()}   net-positive in BOTH windows: "
      f"{((r.is_net>0)&(r.oos_net>0)).sum()}\n")

surv = r[(r.is_net > 0) & (r.oos_net > 0)].sort_values('oos_net', ascending=False)
print(f"{'filter':22}{'tgt':>5}{'stop':>6}{'hold':>6}{'OOS win':>9}{'OOS net':>9}{'IS net':>8}{'%margin':>9}{'n':>6}")
for _, x in surv.head(15).iterrows():
    print(f"  {x.filt:20}{x.tgt:>5.1f}{x.stop:>6.1f}{x.hold:>6.0f}{x.oos_win:>8.1f}%"
          f"{x.oos_net:>+8.3f}%{x.is_net:>+7.3f}%{x.oos_margin_pct:>+8.2f}%{x.oos_n:>6.0f}")
if not len(surv): print("  none survived both windows.")

print(f"\nHIGHEST OOS WIN RATE (any expectancy):")
for _, x in r.sort_values('oos_win', ascending=False).head(5).iterrows():
    print(f"  {x.filt:20}{x.tgt:>5.1f}{x.stop:>6.1f}{x.hold:>6.0f}{x.oos_win:>8.1f}%"
          f"{x.oos_net:>+8.3f}% net")
r.to_csv('multiday_results.csv', index=False)
