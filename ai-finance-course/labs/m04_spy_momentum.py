#!/usr/bin/env python3
"""Module 4 lab: a 20-day breakout rule on SPY, tested honestly on two years of daily data.

The rule, in one sentence: buy at the next open when SPY closes above its prior 20-day high,
and sell at the next open when it closes below its prior 10-day low. Long only, all in or flat.

The signal is read on a closed bar and the trade happens at the NEXT session's open, so the
test cannot see the future. Costs are charged per side at half the round-trip figure.
Nothing here is fitted: 20 and 10 were chosen before the data was downloaded.

Usage: python3 m04_spy_momentum.py            (default window: the last 24 completed months)
"""
import sys
from datetime import date

import numpy as np
import pandas as pd
import yfinance as yf

TICKER = "SPY"
ENTRY_LOOKBACK, EXIT_LOOKBACK = 20, 10
ROUND_TRIP_BPS = [5, 10, 20]
RISK_FREE = 0.0  # stated, not hidden


def test_window(today=None):
    """The last 24 completed calendar months."""
    today = today or date.today()
    end = date(today.year, today.month, 1)  # first day of the current month is excluded
    start = date(end.year - 2, end.month, 1)
    return start, end


def load(start, end):
    warm = date(start.year, start.month - 3 if start.month > 3 else start.month + 9, 1)
    if start.month <= 3:
        warm = warm.replace(year=start.year - 1)
    px = yf.download(TICKER, start=warm, end=end, auto_adjust=True, progress=False)
    if px.empty:
        sys.exit("yfinance returned no data (network blocked?)")
    px.columns = [c[0] if isinstance(c, tuple) else c for c in px.columns]
    return px[["Open", "High", "Low", "Close"]]


def signals(px):
    prior_high = px["Close"].rolling(ENTRY_LOOKBACK).max().shift(1)
    prior_low = px["Close"].rolling(EXIT_LOOKBACK).min().shift(1)
    enter = px["Close"] > prior_high
    exit_ = px["Close"] < prior_low
    pos = pd.Series(0, index=px.index)
    holding = False
    for i in range(len(px)):
        if holding and exit_.iloc[i]:
            holding = False
        elif not holding and enter.iloc[i]:
            holding = True
        pos.iloc[i] = int(holding)
    return pos.shift(1).fillna(0).astype(int)  # acted on at the next session


def backtest(px, pos, bps):
    """Daily returns of the strategy. A position held from open to open earns open-to-open."""
    oo = px["Open"].pct_change().shift(-1)  # return from today's open to tomorrow's open
    gross = (oo * pos).fillna(0)
    trades = pos.diff().abs().fillna(pos.iloc[0])
    cost = trades * (bps / 2 / 1e4)
    return gross - cost


def monthly(r):
    return (1 + r).resample("ME").prod() - 1


def stats(r):
    eq = (1 + r).cumprod()
    dd = (eq / eq.cummax() - 1).min()
    ann = r.mean() * 252 - RISK_FREE
    vol = r.std() * np.sqrt(252)
    down = r[r < 0].std() * np.sqrt(252)
    return {
        "total": eq.iloc[-1] - 1,
        "sharpe": ann / vol if vol > 0 else float("nan"),
        "sortino": ann / down if down > 0 else float("nan"),
        "max_dd": dd,
    }


def trade_list(px, pos, bps):
    """One row per round trip: entry open, exit open, net return."""
    rows, entry = [], None
    opens = px["Open"]
    for i in range(1, len(pos)):
        if pos.iloc[i] == 1 and pos.iloc[i - 1] == 0:
            entry = i
        elif pos.iloc[i] == 0 and pos.iloc[i - 1] == 1 and entry is not None:
            rows.append((opens.iloc[entry] * (1 + bps / 2 / 1e4), opens.iloc[i] * (1 - bps / 2 / 1e4), i - entry))
            entry = None
    return [(b / a - 1, d) for a, b, d in rows]


if __name__ == "__main__":
    start, end = test_window()
    px = load(start, end)
    pos = signals(px)
    px, pos = px.loc[str(start):], pos.loc[str(start):]
    px, pos = px.iloc[:-1], pos.iloc[:-1]  # the last bar has no next open to trade on
    round_trips = int(pos.diff().clip(lower=0).sum())
    hold = pos.sum()
    print(f"{TICKER} 20-day breakout, entry 20 / exit 10, long only. Backtest, not a live record.")
    print(f"Test window: {px.index[0].date()} to {px.index[-1].date()} "
          f"({len(px)} sessions). Round trips: {round_trips}. Days in market: {hold} of {len(px)}.")

    bench = px["Open"].pct_change().shift(-1).fillna(0)
    table = pd.DataFrame({"SPY buy and hold": monthly(bench)})
    summary = {"SPY buy and hold": stats(bench)}
    trades = {}
    for b in ROUND_TRIP_BPS:
        r = backtest(px, pos, b)
        table[f"rule @ {b} bps"] = monthly(r)
        summary[f"rule @ {b} bps"] = stats(r)
        trades[b] = trade_list(px, pos, b)

    print("\nMonthly returns (net of the stated cost, percent):")
    print((table * 100).round(1).rename(lambda d: d.strftime("%Y-%m")).to_string())
    print("\nSummary over the window (annualised, risk-free rate 0):")
    for k, s in summary.items():
        print(f"  {k:18s} total {s['total']*100:6.1f}%   Sharpe {s['sharpe']:5.2f}   "
              f"Sortino {s['sortino']:5.2f}   max drawdown {s['max_dd']*100:6.1f}%")
    print("\nClosed round trips, net of cost:")
    for b, t in trades.items():
        wins = sum(1 for r, _ in t if r > 0)
        avg_hold = np.mean([d for _, d in t]) if t else 0
        print(f"  @ {b:2d} bps: {len(t)} trades, {wins} winners ({wins/len(t)*100:.0f}%), "
              f"average hold {avg_hold:.0f} sessions, best {max(r for r,_ in t)*100:+.1f}%, "
              f"worst {min(r for r,_ in t)*100:+.1f}%")
    print("  A win rate on fewer than 30 trades is not evidence. Say so in your report.")
    mid = px.index[0] + pd.DateOffset(years=1)
    print("\nFirst 12 months vs last 12 months, total return, percent:")
    for k in table.columns:
        r = table[k]
        first = (1 + r[r.index < mid]).prod() - 1
        second = (1 + r[r.index >= mid]).prod() - 1
        print(f"  {k:18s} first {first*100:6.1f}%   second {second*100:6.1f}%")
    print("\nThe parameters were not fitted to this data. A different window will give different numbers.")
