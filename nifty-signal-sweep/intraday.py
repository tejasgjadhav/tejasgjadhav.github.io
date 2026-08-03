"""
Intraday factor decomposition on NIFTY hourly.

Structure the user asked for: break the signal into parts, combine them in a
weighted equation, optimize the weights, backtest.

The point of the design is the comparison between the last two rows:
optimized weights are fit on IS only, then applied untouched to OOS. The gap
between IS and OOS performance IS the overfit, measured rather than argued.
"""
import sys, numpy as np, pandas as pd, yfinance as yf

INTERVAL = sys.argv[1] if len(sys.argv) > 1 else '1h'
PERIOD   = sys.argv[2] if len(sys.argv) > 2 else 'max'
if INTERVAL == 'kite':
    # Cached Kite 5-minute history (see kite_fetch.py) — 7.5 years vs Yahoo's 58 sessions.
    d = pd.read_csv('nifty_5m.csv', parse_dates=['date']).set_index('date')
    d = d.rename(columns=str.capitalize)
    d.index.name = 'ts'   # avoid collision with the 'date' column added below
else:
    d = yf.download('^NSEI', interval=INTERVAL, period=PERIOD, progress=False, auto_adjust=False)
if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
d = d.dropna(subset=['Open','High','Low','Close'])
if d.index.tz is None: d.index = d.index.tz_localize('Asia/Kolkata')
else: d.index = d.index.tz_convert('Asia/Kolkata')
d['date'] = d.index.date
print(f"NIFTY {INTERVAL}: {len(d)} bars  {d.index[0]:%Y-%m-%d} -> {d.index[-1]:%Y-%m-%d}  "
      f"({d['date'].nunique()} sessions)   volume nonzero: {(d['Volume']>0).sum()}\n")

C, H, L, O, V = d['Close'], d['High'], d['Low'], d['Open'], d['Volume']

# ---- factors ("the parts") --------------------------------------------------
delta = C.diff()
g = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
l = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = 100 - 100/(1 + g/l)

# Yahoo reports zero volume on the index, so a true VWAP is not computable here.
# Substitute the session's running mean typical price — same "distance from the
# day's average price" idea, unweighted. Named honestly so nobody reads it as VWAP.
tp = (H + L + C)/3
grp = d.groupby('date')
sess_mean = tp.groupby(d['date']).expanding().mean().reset_index(level=0, drop=True)

# opening-range position: where is price vs the session's first bar
first_hi = grp['High'].transform('first')
first_lo = grp['Low'].transform('first')
or_pos = (C - first_lo) / (first_hi - first_lo).replace(0, np.nan) - 0.5

bar_no = grp.cumcount()
sess_first = C.groupby(d['date']).transform('first')
prev_close = C.groupby(d['date']).transform('last').shift(1)

ret1 = C.pct_change()*100
realvol = ret1.rolling(20).std()

F = pd.DataFrame({
    'mom4':      C.pct_change(4)*100,
    'rsi_c':     rsi - 50,
    'sessmean_dist': (C/sess_mean - 1)*100,
    'or_pos':    or_pos,
    'vol_reg':   realvol / realvol.rolling(100).median() - 1,
    'bar_no':    bar_no.astype(float),
    'day_ret':   (C/sess_first - 1)*100,
})

HOR = 1                                   # 1 hourly bar forward
fwd = (C.shift(-HOR)/C - 1)*100
# never predict across a session boundary
same_sess = pd.Series(d['date']).shift(-HOR).values == d['date'].values
fwd = fwd.where(pd.Series(same_sess, index=d.index))

ok = F.notna().all(axis=1) & fwd.notna()
F, y = F[ok], fwd[ok]
n = len(F)
cut = int(n*0.6)
Fi, yi = F.iloc[:cut], y.iloc[:cut]        # in sample
Fo, yo = F.iloc[cut:], y.iloc[cut:]        # out of sample
print(f"usable bars {n}   IS {len(Fi)} (to {F.index[cut]:%Y-%m-%d})   OOS {len(Fo)}")
print(f"base: IS win {(yi>0).mean()*100:.1f}%  mean {yi.mean():+.4f}%   |   "
      f"OOS win {(yo>0).mean()*100:.1f}%  mean {yo.mean():+.4f}%\n")

# scaler fit on IS only, applied to both — no leakage
mu, sd = Fi.mean(), Fi.std()
Zi, Zo = (Fi-mu)/sd, (Fo-mu)/sd

def ev(score, yy, label):
    """Go long when score > 0; report hit rate and mean of the taken trades."""
    m = score > 0
    if m.sum() < 20: return f"{label:26} (too few)"
    t = yy[m]
    ic = np.corrcoef(score, yy)[0,1]
    return (f"{label:26} n={m.sum():5d}  win {(t>0).mean()*100:5.1f}%  "
            f"mean {t.mean():+.4f}%  IC {ic:+.3f}")

print("EACH PART ALONE")
print(f"{'factor':26} {'IN SAMPLE':>44}    {'OUT OF SAMPLE':>44}")
for c in F.columns:
    print(f"  {ev(Zi[c], yi, c):68}")
    print(f"  {'':26} {ev(Zo[c], yo, '-> OOS')[26:]}")

print("\nCOMBINED EQUATIONS")
eq = Zi.mean(axis=1), Zo.mean(axis=1)
print("  equal weight")
print(f"    IS   {ev(eq[0], yi, '')[26:]}")
print(f"    OOS  {ev(eq[1], yo, '')[26:]}")

# least-squares optimal weights on IS
w, *_ = np.linalg.lstsq(Zi.values, yi.values, rcond=None)
print("\n  optimized weights (least squares, fit on IS only)")
print("    " + "  ".join(f"{c}={wi:+.4f}" for c, wi in zip(F.columns, w)))
si, so = Zi.values@w, Zo.values@w
print(f"    IS   {ev(pd.Series(si, index=Zi.index), yi, '')[26:]}")
print(f"    OOS  {ev(pd.Series(so, index=Zo.index), yo, '')[26:]}")

# cost reality check
print("\nCOST CHECK")
best_oos = (pd.Series(so, index=Zo.index) > 0)
print(f"  optimized OOS mean per trade   {yo[best_oos].mean():+.4f}%")
print(f"  an index move of {yo[best_oos].mean():+.4f}% per trade must clear spread + decay.")

# ---- last-week slice --------------------------------------------------------
# Descriptive only. A week of bars cannot support fitting 7 weights; showing it
# separately so a small-sample number is never mistaken for a validated result.
last_day = F.index[-1].normalize()
wk = F.index >= (last_day - pd.Timedelta(days=7))
if wk.sum() >= 20:
    Fw, yw = F[wk], y[wk]
    Zw = (Fw - mu)/sd
    print(f"\nLAST 7 DAYS — DESCRIPTIVE ONLY (n={len(Fw)} bars, "
          f"{Fw.index[0]:%d %b} -> {Fw.index[-1]:%d %b})")
    print(f"  base            win {(yw>0).mean()*100:5.1f}%  mean {yw.mean():+.4f}%")
    sw = pd.Series(Zw.values@w, index=Zw.index)
    m = sw > 0
    if m.sum() >= 5:
        print(f"  optimized eq    win {(yw[m]>0).mean()*100:5.1f}%  mean {yw[m].mean():+.4f}%  n={m.sum()}")
    for c in F.columns:
        mm = Zw[c] > 0
        if mm.sum() >= 5:
            print(f"    {c:16} win {(yw[mm]>0).mean()*100:5.1f}%  mean {yw[mm].mean():+.4f}%  n={mm.sum()}")
    print(f"  NOTE: n={len(Fw)} over one week. At this size a +/-10pp swing in win rate is noise.")
