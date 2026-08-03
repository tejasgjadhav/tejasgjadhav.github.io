"""
Validate the sweep's leading candidate: rsi_gt65 + wide_range (momentum continuation).

Three tests it has to pass:
  1. year-by-year consistency (a regime artifact shows up as a few huge years)
  2. magnitude vs what options actually cost
  3. is the survivor cluster distinguishable from multiple-testing noise
"""
import numpy as np, pandas as pd, yfinance as yf

df = yf.download('^NSEI', start='2007-09-17', progress=False, auto_adjust=False)
if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
df = df.dropna(subset=['Open','High','Low','Close'])
C, H, L = df['Close'], df['High'], df['Low']

d = C.diff()
g = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
l = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = 100 - 100/(1 + g/l)
rng = (H - L)/C*100
rng_med = rng.rolling(50).median()

sig = (rsi > 65) & (rng > rng_med)
HOR = 2
fwd = (C.shift(-HOR)/C - 1)*100
ok = fwd.notna() & rng_med.notna()

print("SIGNAL: RSI(14) > 65  AND  day range > 50-day median range")
print(f"horizon: {HOR} sessions\n")

print("YEAR BY YEAR")
print(f"{'year':>6} {'n':>4} {'win%':>7} {'mean%':>8} {'median%':>9}   {'base win%':>9}")
yrs = []
for y, grp in df[ok].groupby(df[ok].index.year):
    m = sig.reindex(grp.index).fillna(False)
    f = fwd.reindex(grp.index)[m]
    b = fwd.reindex(grp.index)
    if len(f) < 5:
        print(f"{y:>6} {len(f):>4}   (too few)"); continue
    yrs.append((y, len(f), (f>0).mean()*100, f.mean()))
    print(f"{y:>6} {len(f):>4} {(f>0).mean()*100:>6.1f}% {f.mean():>+7.3f}% {f.median():>+8.3f}%   {(b>0).mean()*100:>8.1f}%")

pos = sum(1 for _,_,_,m in yrs if m > 0)
winbeat = sum(1 for _,_,w,_ in yrs if w > 55)
print(f"\npositive mean in {pos}/{len(yrs)} years;  win rate >55% in {winbeat}/{len(yrs)} years")

f_all = fwd[ok][sig[ok]]
print(f"\nOVERALL  n={len(f_all)}  win {(f_all>0).mean()*100:.1f}%  mean {f_all.mean():+.3f}%  median {f_all.median():+.3f}%")
print(f"  distribution: p5 {np.percentile(f_all,5):+.2f}%  p25 {np.percentile(f_all,25):+.2f}%  "
      f"p75 {np.percentile(f_all,75):+.2f}%  p95 {np.percentile(f_all,95):+.2f}%")
print(f"  worst {f_all.min():+.2f}%   best {f_all.max():+.2f}%")

# What does an ATM option need to break even? Use Tuesday's real quote as the reference.
SPOT, CE, PE = 24383.60, 77.75, 94.55
call_be = (24400+CE)/SPOT*100-100
print(f"\nMAGNITUDE vs COST")
print(f"  mean move on signal            {f_all.mean():+.3f}%")
print(f"  ATM call breakeven needs       {call_be:+.3f}%   (real quote, 04-Aug expiry)")
print(f"  moves clearing call breakeven  {(f_all > call_be).mean()*100:.1f}%")
print(f"  ATM straddle cost              {(CE+PE)/SPOT*100:.3f}%")
print(f"  moves clearing straddle cost   {(f_all.abs() > (CE+PE)/SPOT*100).mean()*100:.1f}%")
