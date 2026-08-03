"""
Combination sweep for NIFTY daily: which pairs/triples of conditions maximize win rate,
and do they survive out of sample?

Guards baked in, because win rate alone is trivially gameable:
  - every combo reported with mean AND median, not just hit rate
  - strict time split: IS 2007-2017, OOS 2018-2026 (no shuffling, no leakage)
  - minimum sample sizes in BOTH windows
  - ranked on IS, then judged on OOS — the drop-off is the actual finding
  - multiple-testing is explicit: we count how many combos were tried
"""
import itertools, numpy as np, pandas as pd, yfinance as yf

HORIZON = 2           # sessions forward
MIN_IS, MIN_OOS = 60, 30
SPLIT = '2018-01-01'

df = yf.download('^NSEI', start='2007-09-17', progress=False, auto_adjust=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])

C, H, L, O = df['Close'], df['High'], df['Low'], df['Open']

# ---- condition primitives ---------------------------------------------------
d = C.diff()
gain = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
loss = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = 100 - 100 / (1 + gain / loss)

sma20, sma50, sma200 = C.rolling(20).mean(), C.rolling(50).mean(), C.rolling(200).mean()
ret1 = C.pct_change() * 100
realvol = ret1.rolling(20).std()
vol_med = realvol.rolling(250).median()
hi20 = H.rolling(20).max().shift(1)
lo20 = L.rolling(20).min().shift(1)
rng = (H - L) / C * 100
rng_med = rng.rolling(50).median()

COND = {
    'trend_up_50':    C > sma50,
    'trend_dn_50':    C < sma50,
    'above_200':      C > sma200,
    'below_200':      C < sma200,
    'rsi_lt35':       rsi < 35,
    'rsi_gt65':       rsi > 65,
    'rsi_40_60':      (rsi >= 40) & (rsi <= 60),
    'vol_low':        realvol < vol_med,
    'vol_high':       realvol > vol_med,
    'break_20d_hi':   C > hi20,
    'break_20d_lo':   C < lo20,
    'near_20d_lo':    (C <= lo20 * 1.01) & (C > lo20),
    'near_20d_hi':    (C >= hi20 * 0.99) & (C < hi20),
    'gap_up':         O > C.shift(1),
    'gap_dn':         O < C.shift(1),
    'narrow_range':   rng < rng_med,
    'wide_range':     rng > rng_med,
    'up_day':         C > C.shift(1),
    'down_day':       C < C.shift(1),
    'below_20':       C < sma20,
    'above_20':       C > sma20,
}

fwd = (C.shift(-HORIZON) / C - 1) * 100
valid = fwd.notna() & sma200.notna() & vol_med.notna() & rng_med.notna()
is_mask = valid & (df.index < SPLIT)
oos_mask = valid & (df.index >= SPLIT)


def stats(mask):
    f = fwd[mask]
    if len(f) == 0:
        return None
    return dict(n=len(f), win=(f > 0).mean() * 100, mean=f.mean(), median=f.median())


base_is, base_oos = stats(is_mask), stats(oos_mask)
print(f"NIFTY daily {df.index[0].date()} -> {df.index[-1].date()}   horizon {HORIZON} sessions")
print(f"IS  (< {SPLIT}): n={base_is['n']}  base win {base_is['win']:.1f}%  mean {base_is['mean']:+.3f}%")
print(f"OOS (>={SPLIT}): n={base_oos['n']}  base win {base_oos['win']:.1f}%  mean {base_oos['mean']:+.3f}%\n")

names = list(COND)
combos = []
for k in (1, 2, 3):
    combos.extend(itertools.combinations(names, k))

rows = []
for combo in combos:
    m = pd.Series(True, index=df.index)
    for c in combo:
        m &= COND[c]
    s_is, s_oos = stats(m & is_mask), stats(m & oos_mask)
    if not s_is or not s_oos:
        continue
    if s_is['n'] < MIN_IS or s_oos['n'] < MIN_OOS:
        continue
    rows.append(dict(
        combo=' + '.join(combo), k=len(combo),
        is_n=s_is['n'], is_win=s_is['win'], is_mean=s_is['mean'],
        oos_n=s_oos['n'], oos_win=s_oos['win'], oos_mean=s_oos['mean'],
    ))

res = pd.DataFrame(rows)
print(f"combinations tried: {len(combos)}   passing size filter: {len(res)}")
print(f"(multiple testing: at {len(res)} tests, ~{int(len(res)*0.05)} will look 'significant' at p<0.05 by luck alone)\n")

top = res.sort_values('is_win', ascending=False).head(15)
print("TOP 15 BY IN-SAMPLE WIN RATE  — watch the OOS column, that is the whole point")
print(f"{'combo':52} {'IS n':>5} {'IS win':>7} {'IS mean':>8} {'OOS n':>6} {'OOS win':>8} {'OOS mean':>9} {'drop':>7}")
for _, r in top.iterrows():
    print(f"{r.combo[:52]:52} {r.is_n:>5.0f} {r.is_win:>6.1f}% {r.is_mean:>+7.3f}% "
          f"{r.oos_n:>6.0f} {r.oos_win:>7.1f}% {r.oos_mean:>+8.3f}% {r.oos_win-r.is_win:>+6.1f}")

# A combo only survives if it beats base in BOTH windows and makes money in both.
surv = res[(res.is_win > base_is['win'] + 3) & (res.oos_win > base_oos['win'] + 3)
           & (res.is_mean > 0) & (res.oos_mean > 0)]
print(f"\nSURVIVORS (beat base by >3pp in BOTH windows, positive mean in both): {len(surv)}")
if len(surv):
    for _, r in surv.sort_values('oos_win', ascending=False).head(12).iterrows():
        print(f"  {r.combo[:52]:52} IS {r.is_win:5.1f}%/{r.is_mean:+.3f}%  "
              f"OOS {r.oos_win:5.1f}%/{r.oos_mean:+.3f}%  (n {r.is_n:.0f}/{r.oos_n:.0f})")
else:
    print("  none.")

res.to_csv('sweep_results.csv', index=False)
print(f"\nfull table -> sweep_results.csv ({len(res)} rows)")
