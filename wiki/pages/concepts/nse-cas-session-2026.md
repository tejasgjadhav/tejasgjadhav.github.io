---
title: NSE Closing Auction Session, live from 3 August 2026
type: concept
tags: [nse, sebi, market-structure, options, trading]
created: 2026-08-26
updated: 2026-08-26
sources: [https://www.nseindia.com/static/products-services/closing-auction-session]
---

SEBI's Closing Auction Session took effect on 3 August 2026. Phase 1 covers only stocks that carry
F&O contracts on both NSE and BSE. Everything else trades as it did before. This page exists because
[[institutional-trader]] scans on the closing price, so the mechanics of that price are part of the
strategy.

**The distinction that is easy to get wrong.** At 15:15 it is only the cash leg of an F&O stock that
stops. That stock's options and futures keep trading normally until 15:40, and so do index futures
and index options.

The cash-segment sub-windows for an F&O stock:

| window | what happens |
|---|---|
| 15:00–15:15 | normal continuous trading, and the VWAP window for the auction's reference price |
| 15:15–15:20 | transition; no new orders are accepted, and orders outside a ±3% band around the reference price are not carried forward |
| 15:20–15:25 | order entry session I, market and limit orders |
| 15:25–15:30 | order entry session II, limit orders only, with a random close between 15:28 and 15:30 |
| 15:30–15:35 | matching; the single price that maximises executed volume becomes the official close |

A non-F&O stock still trades to 15:30 and still closes on the VWAP of the last thirty minutes.
Equity derivatives run to 15:40, and that extra window exists on purpose so participants can react to
the discovered closing price.

**One argument to retire.** The 15:36 to 15:40 window is not structurally illiquid. The case for wide
quotes there rested on the underlying being unhedgeable, and that is only true of the cash leg. Stock
futures trade right through to 15:40, so a market maker can hedge. Whether that window is liquid in
practice has to be measured rather than assumed, which is what the closing-auction recorder described
on [[institutional-trader]] was built to do.
