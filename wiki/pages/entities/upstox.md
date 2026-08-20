---
title: Upstox — broker & market-data API
type: entity
tags: [broker, api, trading, nse]
created: 2026-07-03
updated: 2026-08-20
sources: [~/files/institutional-trader/CLAUDE.md, ~/files/institutional-trader/studies/DATA_AVAILABILITY_LIMITS.md]
---

Indian broker whose API feeds [[institutional-trader]]. The setup uses a free
**Analytics token only** (read-only data feed) — no trading token; all orders are placed
manually by [[tejas-jadhav]] in the Upstox app. Instrument masters cached in [[upstox-data]].

Data-depth limits (the binding constraint on backtests):
- Daily price candles: 2+ years · 5-min underlying candles: ~1 year
- **Live option-premium intraday candles: only ~3–4 weeks.**
- **Expired-instruments endpoint** (`/v2/expired-instruments/historical-candle/…`): daily option
  candles for expired contracts back to **~Oct 2024** — the real-premium source used for the
  Oct'24→date out-of-sample fade test ([[real-data-fade-validation]]). For real premiums *before*
  Oct 2024, Upstox has nothing — use [[nse-bhavcopy]] (free, back to 2019).


## Expired-contract candles enforce liquidity by construction (2026-08-20)

A candle on the expired-instruments endpoint exists only for a contract that actually traded that
day. There is no settlement-price fallback and no row for a strike nobody touched. That makes this
feed stricter than [[nse-bhavcopy]] for any test whose answer depends on how thin a contract is: an
illiquid leg simply produces no trade, so the liquidity penalty applies itself without the harness
having to model it.

The practical use is a cross-check rather than a preference. Run the same parameter sweep on both
sources and compare trade counts cell by cell. Where the bhavcopy counts hold up and these fall
away, the bhavcopy result was built on contracts that could never have been filled. See
[[backtest-harness-audit-rule]].

One operational note from the same session: this endpoint times out often enough under a long sweep
that the fetch has to be retried rather than treated as an empty result, and the leg cache that
sits in front of it must keep one format. A cache holding two shapes at once crashed a sweep twice
in [[institutional-trader]].