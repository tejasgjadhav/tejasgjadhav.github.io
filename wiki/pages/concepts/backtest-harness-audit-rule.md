---
title: Research scripts are production code — the backtest harness audit rule
type: concept
tags: [trading, backtesting, verification, research]
created: 2026-08-16
updated: 2026-08-21
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

**Name the friction your data source cannot represent, and say which side it flatters.** Two
option-price sources used by the same project behave in opposite ways here. The exchange bhavcopy
publishes a settlement close for every listed contract, whether or not a single lot changed hands,
so a harness built on it prices an untraded far-expiry leg at a theoretical value and the trade
passes through looking fillable. The only visible trace is the open-interest column, which is a
proxy for the problem rather than the problem itself. The broker's expired-contract candles work the
other way, because a candle exists only if the contract actually traded that day, so an illiquid leg
produces no trade at all and the constraint enforces itself.

The consequence is a rule about which window to believe. Any in-sample result that depends on
something which thins a contract out — time to expiry, distance from the money, a small underlying —
is the weakest kind of evidence, and the out-of-sample run is not a second opinion but the only
window where the constraint is physical. The diagnostic is a trade-count comparison cell by cell.
Where the out-of-sample counts fall away and the in-sample counts held up, the in-sample case was
built on contracts that could never have been filled. The tenor sweep in [[institutional-trader]] is
the case that produced this rule.

**A failed fetch must never look like a genuine absence.** The leg fetcher in the deployed harness
returned an empty result in two completely different situations. One was a data provider that gave
up after six retries, and the other was a contract that had genuinely never traded. Every persistent
timeout therefore deleted a signal without counting it, and the harness became non-deterministic: a
flaky network morning produced fewer trades than a good one, and the output said nothing about it.
Every out-of-sample figure the project had published came from that code.

The fix is a pattern worth reusing anywhere a harness reads from a network. A failed request returns
a value distinct from an empty result, only an explicit success body counts as evidence of absence,
dropped items are counted, and the run prints that count whether or not it is zero. A clean run then
reports positive evidence rather than the absence of a warning.

**Audit the script of record, not only the script you happen to be running.** The same fetch defect
was found and fixed in a derived sweep copy a full day before anyone checked the harness whose
numbers the project actually quotes. The copy was the thing being executed and the original was the
thing being cited.

**A cache that several scripts share needs a version tag.** Three research scripts in the same
project wrote and read one cache file while disagreeing about whether a value was a bare closing
price or a pair of closing price and open interest. A cache written with a plain truncating dump
left a fragment behind when a run was killed, the two formats mixed inside one file, and 17% of
37,258 entries ended up in the wrong shape. The next run crashed hours in with a type error raised
far from the cause. Write caches to a temporary file and rename them, tag the schema with a version,
and make the reader either heal or reject an entry of the wrong shape rather than trusting it.

**Rate the harness by dimension rather than as one number.** The [[institutional-trader]] harness
scores seven out of ten overall, and the breakdown is what carries the information. Statistical
honesty and out-of-sample discipline rate eight, because the harness has killed two in-sample
findings rather than only confirming them. Data fidelity and code correctness rate six. Execution
realism rates five and is the binding constraint, because a live spread gate that rejects most
candidates cannot be modelled at all without bid and ask history. The overall score cannot rise past
about eight on this data however much further work goes in, and the honest signal to watch is the
bug discovery rate. It has not reached zero, so the count of remaining defects is not known to be
zero either.

**One window can be mined until it stops being evidence.** A single out-of-sample window in this
project has now answered five separate questions. Each new question asked of the same data erodes
its independence, so a result drawn from it late is weaker evidence than the first one was. Prefer
the forward paper record once a window has been queried several times.

Related: [[institutional-trader]], [[trading-strategies]], [[capital-curve-verdict]],
[[nse-bhavcopy]], [[upstox]].
