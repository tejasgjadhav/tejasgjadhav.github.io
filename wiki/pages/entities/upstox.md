---
title: Upstox — broker & market-data API
type: entity
tags: [broker, api, trading, nse]
created: 2026-07-03
updated: 2026-07-03
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
