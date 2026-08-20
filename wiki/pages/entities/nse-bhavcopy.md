---
title: NSE F&O bhavcopy — real historical option premiums
type: entity
tags: [data, nse, options, backtest]
created: 2026-07-03
updated: 2026-08-20
sources: [~/files/institutional-trader/studies/STOCK_OPTIONS_NO_EDGE.md, https://nsearchives.nseindia.com]
---

NSE's daily **F&O bhavcopy** — a free ZIP per trading day with the CLOSE, OPEN_INTEREST and OHLC of
**every listed** derivatives contract, **including expired ones**, back to 2019. (This page said
"every contract that traded" until 2026-08-20. That was wrong in a way that matters for backtests,
and the correction is in the section below.) This is the
real option-premium history that broker APIs do **not** expose ([[upstox]] expired-instruments
reaches back only to Oct 2024; [[zerodha-kite]] has no expired-instruments endpoint at all).

- **Old-format URL** (used by the backtests): `https://nsearchives.nseindia.com/content/historical/
  DERIVATIVES/{YYYY}/{MON}/fo{DD}{MON}{YYYY}bhav.csv.zip` — needs a browser User-Agent + a warm-up
  GET to nseindia.com for the session cookie. 404 = market holiday.
- Columns used: `INSTRUMENT, SYMBOL, EXPIRY_DT, STRIKE_PR, OPTION_TYP, CLOSE, OPEN_INT`.

## Why it matters

It unlocked the true pre-2024 backtests in [[institutional-trader]] that settled the fade-strategy
question ([[real-data-fade-validation]]): downloaded every trading day 2019→Sep'24 for NIFTY/FINNIFTY
+ the ~100-stock universe, giving 181 index and ~7k stock fade trades on **real** premiums — enough
to prove the gated stock fade durable (+5.3% of width) and the index fade regime-dependent (−1.4%).

Downloader/analyzer scripts (in `/tmp` during the study): `bhav_download*.py`,
`bhav_backtest_clean.py`, `bhav_backtest_stk_gated.py`. Contrast with [[upstox]] as the live feed +
the Oct'24→date real-premium source.


## It prices contracts that never traded, and that flatters a backtest

The file carries a settlement close for every contract on the list, whether or not a single lot
changed hands that day. A harness built on it therefore gives an untraded far-expiry strike a
perfectly plausible price, and a trade built on that strike passes through the test looking fillable
when nobody could have filled it. Nothing crashes and no value looks odd.

The only trace of the problem inside this data is the `OPEN_INT` column, which counts what is
outstanding rather than what traded, so it is a proxy and not the thing itself. Counting rejections
against it is still worth doing: the tenor sweep in [[institutional-trader]] used exactly that count
to show open-interest rejections rising three and a half times between a three-day and a
twenty-five-day expiry floor.

[[upstox]] expired-contract candles behave the opposite way and are the stricter instrument, because
a candle exists only where the contract traded. The general rule is on
[[backtest-harness-audit-rule]]: name the friction your data source cannot represent, and say which
side of the result it flatters.