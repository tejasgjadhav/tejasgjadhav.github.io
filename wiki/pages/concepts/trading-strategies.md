---
title: Trading strategies — the 4-strategy lineup and their honest standing
type: concept
tags: [trading, strategy, nse, options, backtest]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/institutional-trader/CLAUDE.md, ~/files/institutional-trader/studies/STOCK_OPTIONS_NO_EDGE.md, ~/files/institutional-trader/studies/CAPITAL_CURVE_RESULTS.md]
---

The strategies implemented in [[institutional-trader]], with their validation status as of
2026-07. All run as **paper forward-tests** (manual orders in Upstox, [[upstox-data]] feed).

## 1. 3-Family stocks (intraday, ~100-stock universe)

Alpha-z score (TREND 0.72 + FLOW 0.18 + EVENT 0.10) → gates: |alpha-z| > 0.55 with ≥2/3
families agreeing · 5-min ORB break with volume surge · market alignment (long only when
Nifty up, short when down) · min option premium ≥ ₹30 on the OTM+1 · liquidity (spread ≤ 4%,
OI ≥ 100). Buy OTM+1 CALL/PUT, exit +10% / −15% on premium. Gates 4 (don't-chase) and 5
(wide-open) were **disabled 2026-06** — didn't hold on real option data.

**Standing: no proven durable edge.** Looked +1.5% (64% win) on a 180-day window but came in
at **−1.0% (55% win) over a full year** — overfit to a regime. Min-premium is kept only for
the cost/spread benefit (~3× tighter spreads), not as a profit edge. The 13 `PRIORITY_STOCKS`
are a UI focus tilt only (per-stock win-rate selection overfits).

## 2. ORB+VWAP index (NIFTY/BANKNIFTY, intraday)

15-min ORB + VWAP + 30-min trend + clean-trend filter → buy ATM, trend-ride exit (exit on
VWAP reclaim after +12%, hard −15% stop).

**Standing: thin but durable — the one real intraday edge.** +0.9% over 18 months
(453 trades), positive on both train and test.

## 3. Index fade credit spread (NIFTY + FINNIFTY, multi-day — "swing credit")

Daily Donchian-10 breakout → **sell a credit spread against it** (up-break → bear-call,
down-break → bull-put), ≥10 DTE, short 1-OTM, width 3, hold to expiry, hard stop 2× credit.
Overnight carry. `engine/swing_credit.py`.

**Standing: DOWNGRADED (2026-07) — regime-dependent, not durable.** Looked validated on the
Oct'24–Jun'26 window (+12–20% net/trade), but the **real-data test on [[nse-bhavcopy]] premiums
2019→Sep'24 came in NET-NEGATIVE (−1.4% of width, 181 trades)** — positive only in 2019 & 2024,
the favorable regimes. A [[real-data-fade-validation|salvage attempt]] (fade DOWN-breaks only +
flush ≥0.5%) looked great in-sample (+15.1%, 78% win, 6/6 years) but **FAILED out-of-sample** on
Upstox Oct'24→date (the direction asymmetry reversed; deployed gate −2.8%) — a bull-regime
artifact. Gates reverted; the fade runs ungated as a small forward-test. The *follow* version loses
too — no durable directional edge, it's regime timing. Capital curve (favorable-regime figures, 43
trades/20 mo): ~0.8%/mo on ₹2 L at 13% DD; 5%/mo infeasible by 3–6× ([[capital-curve-verdict]]).

## 4. Stock fade credit spread (~100 stocks, high frequency ~16/mo)

Same fade, gated on credit/width ≥ 0.40 (rich premium = elevated post-breakout IV — the
edge) + short premium ≥ ₹50 + liquidity + open-position caps. `engine/stock_credit.py`.

**Standing: REAL-DATA CONFIRMED (2026-07) — the one durable, regime-robust edge.** Tested on
[[nse-bhavcopy]] premiums 2019→Sep'24 (718 trades): **+5.3% of width (~+9%/trade on margin),
54% win, positive in 5 of 6 years.** The credit/width gate IS the edge — strip it and the same
universe loses (−1.1%, like the index and like a generic spread). But the real edge is **~⅓–½ of
the optimistic backtest** (+16–25% → +5.3%; 65% → 54% win), so it's durable but modest, high
variance (2023 was −4.5%). **Keep lots at 1** (live mid-cap fills erode it further). See
[[real-data-fade-validation]].

## Cross-cutting lessons

- **Real option history goes back to 2019 after all** — via [[nse-bhavcopy]] (free daily CLOSE +
  OI for every contract, incl. expired), the data no broker API exposes. This unlocked the true
  pre-2024 backtests that overturned the index-fade "validation." Upstox expired-instruments
  reaches back only to Oct 2024.
- **6 positive years inside ONE regime is NOT out-of-sample.** The index-fade gate passed a 6/6
  year check and a positive bootstrap p5, yet failed the moment a genuinely different regime
  (Oct'24→date, post-peak correction) was tested. Only a different *regime* is a real holdout.
- Train/test inside a short window is not true out-of-sample — use the longest window the
  data allows.
- The ~100-stock universe is hand-picked by intraday movement, not market cap — a
  free-float-mcap top-100 lost head-to-head (61% vs 67%).
- House rule: honesty over optimism — frame everything gross-vs-net, sample size,
  out-of-sample fragility. Backtest before deploying any tunable change.

Research trail: `institutional-trader/studies/` (STOCK_OPTIONS_NO_EDGE.md Parts 10–11 hold the
real-bhavcopy verdicts + the failed index-fade gate) + reproducible scripts. Synthesis:
[[real-data-fade-validation]].
