---
title: Capital-curve verdict — what return is actually achievable
type: concept
tags: [trading, risk, capital, backtest]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/institutional-trader/studies/CAPITAL_CURVE_RESULTS.md]
---

Replay of the validated index fade credit spread ([[trading-strategies]] §3) on real expired
option premiums — 43 trades, NIFTY+FINNIFTY, 2024-11 → 2026-06, 1 lot, gross of costs
(2026-06-29 study).

| Capital | Return/mo | Max DD | Verdict |
|---------|-----------|--------|---------|
| ₹1 L | 1.63% | **26%** | breaches the ≤15% DD cap |
| ₹2 L | **0.82%** | 13% | the realistic operating point |
| ₹3 L | 0.54% | 8.7% | safer, lower return |

**The 5%/month + 80% win-rate goal is infeasible by ~3–6×** on the validated edge. On a
small base, per-trade margin is too large a fraction of capital, so the drawdown cap binds
long before 5%/mo. Realistic: **~0.8%/mo on ₹2 L (~10%/yr), high variance** — and live
fills shave it further (figures are gross).

The one legitimate lever: more uncorrelated smaller trades (the stock fade, ~16/mo) could
lift ~0.8%/mo toward maybe 1.5–2.5%/mo *if* it survives live fills — still well short of 5%.

Part of the research in [[institutional-trader]].
