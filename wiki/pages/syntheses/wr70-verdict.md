---
title: The 70% win rate and 3% a month cannot both hold — search closed
type: synthesis
tags: [trading, backtest, strategy, nse, intraday, win-rate]
created: 2026-08-29
updated: 2026-08-29
sources: [~/files/HANDOFF-wr70.md]
---

After the sweep fade died on [[turtle-soup-verdict]], the question became whether any other
intraday setup could clear two constraints at once: a win rate at or above 70 per cent, and a net
return of 3 per cent a month on margin. The study ran on 2026-08-10 and closed the line the same
day. It is the largest single search in the [[institutional-trader]] research so far.

## The arithmetic came first

On a driftless random walk with the stop at one R, the probability of reaching a target of k times
R before the stop is 1 divided by 1 plus k. A 70 per cent win rate therefore puts the target at
0.4286R, and expectancy at that geometry is exactly zero. Profit requires the observed win rate to
beat that baseline. Adding the 3 per cent monthly hurdle at a 60 basis point stop gives the full
specification: about a 76 per cent win rate, which is roughly 6 percentage points of genuine edge
over the baseline.

That number explains the earlier failure. The sweep fade stopped out on a single one-minute candle,
about 6 basis points, so trading cost was half the risk and the required edge was around 46
percentage points. **The high win rate corner is the most expensive place to hunt, because a tight
target makes each point of edge worth the least.**

## What was measured

The scan built five-minute bars, computed fourteen features with no lookahead, and recorded a
first-touch outcome for every entry across two sides, five stops and five target ratios. Entries
were taken every fifteen minutes between 09:30 and 14:30 across thirty instruments, six indices and
twenty-four large caps. That produced 713,227 candidate entries and 3,550 gate by geometry cells.
Quintile edges were fitted on 2022 to 2024 and applied unchanged to 2025 and 2026, and the
out-of-sample half was never searched over.

| | in sample | out of sample |
|---|---|---|
| cells with a true hit rate at or above 70% | 499 | 532 |
| of those, net positive | **0** (best −1.80 bps) | **0** (best −1.41 bps) |
| best net across all cells | +3.39 bps, at a 7.3% hit rate | +0.27 bps, t = 0.88 |
| cells net positive | 29 of 3,550 | 2 of 3,550 |
| in-sample to out-of-sample net correlation | — | **−0.112** |

**Zero cells anywhere reach a 70 per cent hit rate and a positive net, and that holds even in
sample, where the search had 3,550 chances to overfit.** Out of sample only 2 cells of 3,550 turned
a profit, against the roughly 1,775 you would expect if every edge were a coin flip. The negative
correlation between the two halves says the in-sample winners actively reversed rather than merely
faded.

Everything profitable sits at the far end of the range. The best in-sample cell earned 3.39 basis
points at a 7.3 per cent hit rate, on a 120 basis point stop with a 1.5R target, which is rare large
wins and nothing like the requested shape. It did not survive out of sample either. The profitable
in-sample cells were long-momentum gates fitted to the 2022 to 2024 bull market, and out of sample
they invert by 0.77 to 3.85 basis points.

## What this does not license anyone to claim

Every gate tested was univariate, meaning one feature and one quintile. Conjunctions were never
searched, and classical candlestick practice is a conjunction: an engulfing bar, at prior support,
after a downtrend. Non-linear models over the same features, named multi-bar patterns as such, and
non-OHLC information such as order flow, market depth and options positioning were all left
untested. The defensible claim is narrow. In liquid Indian equities and indices intraday, no single
condition OHLC gate tested delivers a 70 per cent hit rate with positive net expectancy, and the
largest genuine excess measured anywhere was about 1 percentage point against a 6 point requirement.

## Two things to carry forward

The scan script carries a bug worth fixing before anyone reuses it. It compares a win percentage
defined as the probability of a positive outcome, which includes end-of-day exits, against a
baseline defined as the probability of touching the target first. Those are different quantities,
so its excess and z columns are not a valid test. Its net and t columns are sound, and the table
above uses the corrected hit rate.

The deployed book survives all of this because it earns from a different source. The gated stock
credit spread on [[institutional-trader]] makes its money from volatility and time decay, not from
direction, which is why it held out of sample when directional fades and momentum gates did not.
The method discipline is on [[backtest-harness-audit-rule]], and the strategy ledger is on
[[trading-strategies]].
