---
title: Institutional Trader — NSE intraday options paper-trading
type: project
tags: [trading, nse, options, python, upstox]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/institutional-trader/CLAUDE.md, ~/files/institutional-trader/README.md, ~/files/institutional-trader/studies/]
---

A **paper-trading** algo system for NSE intraday options. Scans NIFTY, BANKNIFTY and ~100
liquid stocks every 5 minutes, scores each with a 3-family model, and surfaces buy-option
(CALL/PUT) signals when they clear strict gates (alpha, ORB, alignment, min-premium,
liquidity). **It never places orders** — [[tejas-jadhav]] places them manually in
[[upstox]] ([[upstox-data]] holds the instrument metadata).

**The full 4-strategy lineup and validation status: [[trading-strategies]].**
What return is realistically achievable: [[capital-curve-verdict]].

## Honest status (as of 2026-07)

Four strategies, all paper forward-tests. After real-premium testing on [[nse-bhavcopy]]
(2019→Sep'24) the picture sharpened ([[real-data-fade-validation]]): the **one durable edge is
the gated stock fade credit spread** (+5.3% of width, 54% win, 5/6 years positive — modest, ~⅓–½
of its optimistic backtest). The **index fade credit spread was DOWNGRADED** — net-negative
(−1.4%) out-of-time and a directional-gate salvage failed out-of-sample; it's regime-dependent, not
durable. A thin **ORB+VWAP index trend-ride** (+0.9%/18 mo) survives. The 3-Family stock strategy
has **no proven durable edge** (−1.0% over a full year). **Not proven profitable overall** — the
project's own docs insist on saying so. The 5%/month + 80% win-rate goal is infeasible by ~3–6×.

## Architecture

Two decoupled processes, both launchd jobs:
- **Engine** (`engine/engine_runner.py`) — headless daemon; scans, fires signals, resolves
  paper trades, 15:30 EOD-book; writes `engine.db`, `signals.db`, `trade_log.json`, etc.
- **Viewer** (`main.py`) — read-only desktop dashboard, re-reads disk every 15 s. Trading
  logic never goes in the GUI.

Current research/backtests live in `studies/`; `How_We_Built_The_Strategy.pdf` and
`BACKTEST_RESULTS.md` are the historical build journey (superseded).

Part of [[files-repo]].
