"""
Module 5 lab: Monte Carlo one-day VaR on five US large caps.

What it does, in order:
  1. Pull two years of daily adjusted closes for five tickers from Yahoo Finance (yfinance).
  2. Turn the closes into daily log returns.
  3. Measure the mean vector and the covariance matrix of those returns.
  4. Cholesky-factor the covariance matrix so the simulated draws carry the same correlations.
  5. Draw 10,000 simulated one-day return vectors.
  6. Value an equal-weighted $1,000,000 portfolio in each one.
  7. Sort the 10,000 outcomes. The 500th worst is the 95% VaR, the 100th worst is the 99% VaR.
     The mean of everything past each line is the CVaR at that level.
  8. Cross-check against historical simulation and the parametric (normal) method.
  9. Backtest: count how many of the last 250 real trading days lost more than the 99% VaR,
     and say which Basel traffic-light zone that count lands in.

Every number this prints is a simulation on the dates it prints. It is not a forecast.
"""
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "JNJ"]
WEIGHTS = np.array([0.20] * 5)
PORTFOLIO_VALUE = 1_000_000          # dollars
N_PATHS = 10_000
LEVELS = [0.95, 0.99]
SEED = 42
YEARS = 2

end = pd.Timestamp.today().normalize()
start = end - pd.DateOffset(years=YEARS)
raw = yf.download(TICKERS, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"),
                  auto_adjust=True, progress=False)
if raw.empty:
    sys.exit("No data returned from yfinance. Check the network and try again.")
prices = raw["Close"][TICKERS].dropna()
log_ret = np.log(prices / prices.shift(1)).dropna()

mu = log_ret.mean().values
sigma = log_ret.cov().values
corr = log_ret.corr()
L = np.linalg.cholesky(sigma)

rng = np.random.default_rng(SEED)
Z = rng.standard_normal((N_PATHS, len(TICKERS)))
R = mu + Z @ L.T
simple_ret = np.exp(R) - 1
pnl = PORTFOLIO_VALUE * (simple_ret @ WEIGHTS)


def var_cvar(p, level):
    cut = np.quantile(p, 1 - level)
    return -cut, -p[p <= cut].mean()


print("=" * 72)
print("MONTE CARLO ONE-DAY VaR | five US large caps, equal-weighted, $1,000,000")
print("=" * 72)
print(f"Data window     : {prices.index[0].date()} to {prices.index[-1].date()} "
      f"({len(log_ret)} daily returns)")
print(f"Paths           : {N_PATHS:,}   seed = {SEED}")
print("Return model    : multivariate normal on daily log returns (Cholesky)")
print()
print("--- Step 1: inputs measured from history ---")
tbl = pd.DataFrame({
    "weight": WEIGHTS,
    "last close $": prices.iloc[-1].values,
    "mean daily %": mu * 100,
    "daily vol %": np.sqrt(np.diag(sigma)) * 100,
    "annual vol %": np.sqrt(np.diag(sigma)) * np.sqrt(252) * 100,
}, index=TICKERS).round(3)
print(tbl.to_string())
print()
print("Correlation of daily log returns:")
print(corr.round(2).to_string())
print()

print("--- Step 2: VaR and CVaR from the 10,000 simulated days ---")
rows = []
for lv in LEVELS:
    v, c = var_cvar(pnl, lv)
    rows.append({"level": f"{lv:.0%}", "VaR $": round(v), "VaR %": round(v / PORTFOLIO_VALUE * 100, 2),
                 "CVaR $": round(c), "CVaR %": round(c / PORTFOLIO_VALUE * 100, 2)})
res = pd.DataFrame(rows).set_index("level")
print(res.to_string())
print()

print("--- Step 3: the same portfolio by the other two methods ---")
hist_pnl = PORTFOLIO_VALUE * ((np.exp(log_ret.values) - 1) @ WEIGHTS)
port_sigma = float(np.sqrt(WEIGHTS @ sigma @ WEIGHTS))
port_mu = float(WEIGHTS @ mu)
cmp_rows = []
for lv in LEVELS:
    mv, mc = var_cvar(pnl, lv)
    hv, hc = var_cvar(hist_pnl, lv)
    z = norm.ppf(1 - lv)
    pv = -PORTFOLIO_VALUE * (port_mu + z * port_sigma)
    pc = -PORTFOLIO_VALUE * (port_mu - port_sigma * norm.pdf(z) / (1 - lv))
    cmp_rows.append({"level": f"{lv:.0%}", "Monte Carlo VaR $": round(mv), "Historical VaR $": round(hv),
                     "Parametric VaR $": round(pv), "MC CVaR $": round(mc), "Hist CVaR $": round(hc),
                     "Param CVaR $": round(pc)})
print(pd.DataFrame(cmp_rows).set_index("level").to_string())
print()

print("--- Step 4: backtest the 99% VaR against the last 250 real days ---")
var99, _ = var_cvar(pnl, 0.99)
last250 = hist_pnl[-250:]
breaches = int((last250 < -var99).sum())
zone = "green (0-4)" if breaches <= 4 else "yellow (5-9)" if breaches <= 9 else "red (10 or more)"
worst_day = log_ret.index[-250:][np.argmin(last250)].date()
print(f"99% one-day VaR used  : ${var99:,.0f}")
print(f"Days tested           : 250 ({log_ret.index[-250].date()} to {log_ret.index[-1].date()})")
print(f"Breaches              : {breaches}   expected about 2 or 3")
print(f"Basel zone            : {zone}")
print(f"Worst real day        : {worst_day}, P&L ${last250.min():,.0f}")
print()
print("--- The three worst real days in the whole two-year window ---")
order = np.argsort(hist_pnl)[:3]
for j in order:
    print(f"{log_ret.index[j].date()}   P&L ${hist_pnl[j]:,.0f}")
print(f"Real days below the 99% VaR across all {len(hist_pnl)} days: {int((hist_pnl < -var99).sum())}")
print()
print("Every figure above is a simulation on the dates stated. It is not a forecast.")
