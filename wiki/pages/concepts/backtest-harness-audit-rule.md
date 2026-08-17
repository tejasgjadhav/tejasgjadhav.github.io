---
title: Research scripts are production code — the backtest harness audit rule
type: concept
tags: [trading, backtesting, verification, research]
created: 2026-08-16
updated: 2026-08-17
sources: [~/files/institutional-trader/studies/, ~/files/institutional-trader/HANDOFF.md]
---

A backtest that gates a deployment decision is production code, and it gets audited like production
code. This rule was written after a leg-misalignment defect in the [[institutional-trader]] study
and it has since caught two more failures of the same family.

**Audit the harness adversarially before you trust a result that would change a live book.** A
harness produces a number whether or not it is correct, and a wrong number is indistinguishable
from a right one at the point where you read it. The three defects found so far were all invisible
to every statistical test run on the output.

**The failures that produced the rule:**

- **Option legs joined by position rather than by date.** Two legs of the same spread came from
  separate queries and were zipped together in order, so a missing row in one series silently
  paired every subsequent trade with the wrong day. Join by date, always, and assert the join.
- **A corporate-action scale mismatch (2026-08-15).** Adjusted price series were compared against
  unadjusted strikes, which pinned ATM to the far end of the ladder, picked both legs deep in the
  money and booked fabricated full-credit wins. The tell was a per-symbol credit-to-width of 0.90
  or more on split and bonus names against 0.44–0.49 on names with no corporate action.
- **Live entry rules not modelled (2026-08-16).** The engine skips a name it already holds open,
  and the harness only enforced a 3-day gap, so 59% of in-sample trades were re-entries the live
  book could never have taken — and they skewed toward names still going against the position.

**What each one has in common:** the defect inflated the result, no test on ₹ per trade could see
it, and it was found by looking at the mechanism rather than the distribution. Two things surface
this family cheaply. Reconcile the backtest's own distribution against live fills, because all 21
live fills sitting at a credit-to-width of 0.39–0.47 is what exposed the 0.96 rows as impossible.
And check that the instrument still trades on the cadence the backtest assumed, because a cadence
change can invalidate a seven-year result without moving any per-trade number at all.

**Re-audit after every material fix.** A harness audited before a change is not an audited harness
after it, and the parity fix on this repo is currently unreviewed.

**Name the gate your data cannot model, and treat it as the ceiling.** A harness is limited by its
inputs before it is limited by its code. The [[institutional-trader]] backtest runs on end-of-day
exchange files that carry a close and an open-interest figure and no bid or ask, while the live
engine refuses any trade whose spread is worse than 6% — a gate that rejected 59% of candidates on
the day it was measured. Perfect code on incomplete data still returns an answer that does not
describe live trading. So score the harness against what it could ever achieve rather than against
perfection: every known bug fixed and both windows re-run is the honest maximum, and getting past it
needs data that does not exist or a forward record of real fills. **A forward record of fifty
resolved trades is worth more than another week of harness work**, because it is the only
measurement that includes the spread gate, the fills and the slippage.

**A parameter frozen into a record at entry outlives the policy that set it.** One live position
carried a stop for nineteen days after the books stopped using stops, because the stop level was
written into the position when it opened and nothing re-read the configuration afterwards. Audit
stored parameters against current config at load time, and prefer reading a live value to freezing
a copy.

Related: [[institutional-trader]], [[trading-strategies]], [[capital-curve-verdict]],
[[nse-bhavcopy]], [[upstox]].
