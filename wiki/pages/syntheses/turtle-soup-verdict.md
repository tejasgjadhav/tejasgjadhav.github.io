---
title: Turtle Soup (PDH/PDL liquidity sweep) — backtested and rejected
type: synthesis
tags: [trading, backtest, strategy, nse, mcx, intraday]
created: 2026-08-10
updated: 2026-08-29
sources: [~/files/HANDOFF-turtlesoup.md]
---

An Instagram reel showed an MT5 expert advisor trading a previous-day-high/low liquidity sweep.
The question was what the strategy is, whether it works, and whether any configuration of it can
win above 80% of the time on any instrument. It was backtested on 2026-08-10.

## What the strategy is

The strategy is **Turtle Soup**, published by Linda Raschke and Larry Connors in *Street Smarts*
(1995). Mark the previous session's high and low. A sweep happens when a 1-minute candle closes
beyond one of those levels by a buffer. The first opposite-colour candle after the sweep is the
confirmation. Entry comes on a later candle breaking that confirmation candle's extreme, the stop
sits at its other extreme, and the target is the opposite side of the previous day's range.

The same mechanic is sold under several other names. Wyckoff calls it a Spring or an Upthrust, and
ICT material calls it a PDH/PDL raid with a market-structure shift. Larry Williams' "Oops!" is a
cousin that additionally requires a gap open.

## The verdict: it is a coin flip after costs

Testing covered 54,189 setups from January 2022 to August 2026, across NIFTY, BANKNIFTY, SENSEX,
FINNIFTY, NEXT50, MIDCPNIFTY, 54 NSE stocks and 8 MCX commodities. Fills were conservative: the
stop takes priority on any bar that could have touched both levels, positions force flat at 15:25,
one trade per day, no entries after 15:00.

| Symbol | Trades | Win % | Net bps/trade | Gross bps/trade |
|---|---|---|---|---|
| NIFTY | 924 | 12.9 | −1.83 | +1.17 |
| BANKNIFTY | 942 | 14.0 | −1.06 | +1.94 |
| SENSEX | 933 | 13.0 | −1.18 | +1.82 |

Break-even cost is 1.2 to 1.9 bps round trip, and Indian index futures cost more than that — STT
alone is 2 bps on the sell leg since October 2024. A 48-cell parameter sweep found four positive
cells, all on BANKNIFTY, all with t below 0.7. Per-year P&L flips sign every year. MCX commodities
over two months returned +0.18% equal-weighted across five contracts whose individual results ran
from −20.8% to +10.0%, which is the signature of a zero-expectancy bet rather than an edge.

Leverage does not help. Applying 7x turned the one- and two-month index results into losses of 3
to 23%, because leverage multiplies a negative expectancy instead of repairing it.

## The finding worth keeping

The requirement scales with the target, and that is why the 80% question answers itself. Earning
3% a month on margin at 7x over roughly 20 trades needs about 2.1 bps net per trade on notional.
Translated into how far the strategy must beat its own baseline:

| Configuration | Excess needed over baseline |
|---|---|
| 0.25R target (the 80% win-rate zone) | 46.7 points |
| 1R target | 29.2 points |
| 5R target | 9.7 points |
| 5R target, stop widened to 30 bps | 2.4 points |

The largest genuine excess measured anywhere in the data was about 1 point, and it was not
statistically significant. **The 80% win-rate zone is the worst place to hunt for an edge**,
because a tight target makes each point of edge worth the least. This is the same conclusion the
project reached from a different direction in [[trading-strategies]], where the house rule is to
report win rate and never optimize it.

## Two things learned along the way

**A 90.77% win rate turned out to be a lookahead bug.** The excursion walk started on the entry
bar itself, so for a short entered at the confirmation candle's high, that bar's low had usually
printed before the trigger existed. The trade was being credited with a move that happened before
it was placed. A win rate that good is a bug report, not a result.

**[[upstox]] v3 historical-candle is public and needs no authentication.** The endpoint is
`https://api.upstox.com/v3/historical-candle/{urlencoded_key}/minutes/1/{to}/{from}`, and 1-minute
history reaches back to January 2022, returning empty before that. Instrument keys come from
`engine.instruments.to_instrument_key` in [[institutional-trader]]. MCX keys exist, but a live
contract carries only its own listing history, so a continuous commodity series needs contract
stitching through the expired-instruments endpoint, and that one does need the auth token.

## What happened next

The same harness was pointed at the general question rather than this one strategy. It searched
3,550 gate and geometry combinations for anything that clears a 70 per cent win rate and 3 per cent
a month together, and found nothing. That study is on [[wr70-verdict]], and it measures the tension
the arithmetic above predicted.
