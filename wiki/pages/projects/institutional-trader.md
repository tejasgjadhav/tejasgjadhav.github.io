---
title: Institutional Trader — NSE intraday options paper-trading
type: project
tags: [trading, nse, options, python, upstox]
created: 2026-07-03
updated: 2026-08-17
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

**Objective re-spec** (`studies/OBJECTIVE_SPEC.md`, v1 2026-06-29): the original
"80% win rate + 5%/month" ask was formally replaced — win rate is gameable and
anti-correlated with profit (rrsweep study), so the target is now **monthly return on
fixed capital (₹1–3 L) under a HARD ≤15% drawdown cap**, win rate reported but never
targeted. Hypothesis: the binding constraint is position concurrency under the DD budget,
not signal availability. Results: [[capital-curve-verdict]].

**Live forward test** (as of 2026-07-04): the gated stock fade runs as a deployed paper
strategy — `engine/stock_credit.py` with `config.STOCK_CREDIT_*`, its own dashboard PM
tab, writing `data/stock_credit.json` / `stock_credit_positions.json` (12 open paper
positions, 1 lot each, e.g. bear-call spreads on breakout-LONG stocks).

**Alerts + canonical doc (2026-07-04; Telegram LIVE 2026-07-13):** Telegram and WhatsApp (free
CallMeBot API) message alerts are wired into the signal engine. **Telegram is now live** — bot
**@Algotejasbot** → channel *"Algo Trader by Tejas"*; `notifications.send_telegram()` fans out to
comma-separated chat/channel ids and `engine_runner._tg()` pushes once each on a new open (README +
in-app manual both say "TELEGRAM ALERTS — LIVE"; token/channel id in gitignored `.env`). The wiring
covers 8 sources but **effective coverage is 7 live books** (2026-07-15 correction): the 8th, 3-Family,
is `SCAN_3FAMILY_ENABLED = False` **and** rejected (−1.0% net), so it never fires and never sends — its
send-wiring is dormant. WhatsApp/phone *voice calls* per
signal are not possible via any free API — guaranteed calling would need paid Twilio.
`studies/STRATEGY_SUMMARY.md` is now the single canonical strategy table — kept in sync
with the app's STUDIES tab, local CLAUDE.md, and this wiki page whenever a strategy's
status changes. Repo remote confirmed: `github.com/tejasgjadhav/Institutional-Trader`.
Sizing: intraday credit-spread trades same-day close/reuse, ~₹32k/day avg deployed
capital, ~1.7 trades/day, peak day ~₹85k. Go-live bar unchanged and non-negotiable:
≥52% win rate AND profit factor >1 over 30+ signals — "don't automate below that."

## Architecture

Two decoupled processes, both launchd jobs:
- **Engine** (`engine/engine_runner.py`) — headless daemon; scans, fires signals, resolves
  paper trades, 15:30 EOD-book; writes `engine.db`, `signals.db`, `trade_log.json`, etc.
- **Viewer** (`main.py`) — read-only desktop dashboard, re-reads disk every 15 s. Trading
  logic never goes in the GUI.

**Watchlist UI build-time discipline (2026-07-15):** the engine builds `data/union_watchlist.json` at
**3:05 PM** (near the close); before then the PM DECISIONS panel must read "no scan yet today". An
on-demand intraday "check now" / "run" scan stays **terminal-only** — a manual `build_watchlist` run must
NOT overwrite the persisted file, or the UI wrongly shows morning data (fix: delete the file, the viewer
re-reads on its 15 s timer).

**2026-07-16 — portfolio reframe, cadence + timing fixes:**
- **README reframed as a multi-strategy portfolio** (commit 5290cd5): no longer led by "v2 fade (the
  winner)" but by "a portfolio of independent, individually-validated books" — six live: stock fades
  v1/v2, 0DTE NIFTY/SENSEX/BANKNIFTY, monthly futures. v2 stays flagged ★ leader but is one row of six.
  The retired 3-Family's stale "intraday window 09:45–13:00" NOW banner was removed from PM DECISIONS.
- **Watchlist consolidated to ONE daily 3:05 PM build** (commit bd485a6): the every-15-min 100-stock
  sweep was removed (25 engine passes/day → 1). `notify_nearmiss()` now rebuilds `union_watchlist.json`
  **and** sends the ⛔ DO-NOT-TRADE Telegram digest together at 3:05 — justified because breakouts are
  defined by the *daily close* and the stock spreads are held-to-expiry, so nothing needs placing before
  the 3:30 close.
- **0DTE result Telegram now arrives ~15:35, not ~15:40** (commit a1251c3): the outcome watcher runs
  *after* the settlement steps in each post-close 5-min cycle (previously before, costing an extra cycle).
- **Full daily Telegram timeline:** ~9:16 0DTE entry · 15:05 DO-NOT-TRADE watchlist digest · ~15:10
  stock credit v1/v2 signals · ~15:35 0DTE WIN/LOSS result.
- **New c/w-gate two-tier finding** (deferred, not deployed) — see [[trading-strategies]].

**2026-07-20 — watchlist-preview vs binding-scan, UNION=D5, live bug sweep, timing:**
- **Watchlist "PASS" is a live PREVIEW snapshot, not a fired signal — only the ~15:10 scan is binding.**
  A c/w-boundary-hugger (OFSS flickering 0.383↔0.43 around the 0.40 gate) can show "PASS" in the union
  watchlist yet correctly not fire, because at the binding scan instant its c/w was below 0.40 — so
  PASS + no book entry + no Telegram are consistent, not a bug. The ~82% win in the 0.35–0.40 c/w bucket
  is **conditional on the TP-50 exit** (buy back at ~half the entry credit, stop at 3× credit);
  hold-to-expiry is materially lower — a discretionary sub-gate trade held to expiry isn't the
  backtested setup. See [[trading-strategies]].
- **UNION scanner = D5** (Donchian standalone D5/D10/D15/D20 study, validation-only worktree): the runner
  checks D5 first and D10/D15/D20 breaks are a strict subset of D5's, so live UNION is mathematically the
  loosest (D5) definition — running stricter D-values alongside is a no-op; the credit/width gate remains
  the bottleneck.
- **Live bug sweep (commit 5a7a18b):** settlement fabrication fixed in BOTH 0DTE books
  (`zero_dte.py`/`dte_multi.py` used `spot = _spot() or entry_spot or 0` → a 15:30 quote failure gave
  spot 0 → intrinsic 0 → **fabricated WIN + wrong Telegram**; now settle on the expiry-day daily close).
  **"M&M" silently lost every alert** — Mahindra's `&` breaks Telegram HTML mode (400) while the position
  was marked "seen" before the send → lost forever; durable rule: HTML-escape all dynamic Telegram fields
  and mark "seen" only AFTER a successful send (+ plain-text retry on 400). `monthly_fut` now books expiry
  at the MOC close, not midnight.
- **Watchlist timing → build 14:45 / send digest 15:05** (commits 01dc6d3, 6c20f32, supersedes the single
  3:05 PM build): digest sends from a pre-built file for reliable timing; gate cells now show actual
  **C/W + PREM** numbers, not a bare tick.

**2026-07-23 — per-trade portfolio summary + "Saavi" branding, data ceiling, queued job:**
- **Running portfolio summary on Telegram after every trade RESULT** (deployed):
  `engine_runner._portfolio_summary_text()` tallies **closed** W/L / win% / realized P&L plus the
  **open count** across all six outcome books, and sends once per cycle right after any genuinely-new
  WIN/LOSS (guarded so a summary failure can't disturb trading; 60 s throttle; win% stays closed-only).
- **Branding header the user chose:** *"📈 Tejas's Saavi Institutional Trader has till date delivered
  for live trade-"*. Claude flagged that "delivered for live trade" overstates a **paper/forward-test**
  (no real orders) and offered accurate softenings; the user kept the original wording — a branding call,
  but the honesty caveat stands (cf. the no-overstatement discipline elsewhere in [[tejas-jadhav]]'s work).
- **Intraday option-premium data ceiling (why long hourly backtests are impossible):** real intraday
  (1-min) stock-option premiums exist **only Oct'24→now (~2 yrs)** via [[upstox]] expired-instruments;
  **2019→Sep'24 = [[nse-bhavcopy]] daily-close only** (no intraday c/w computable); **pre-2019 = no
  stock-option data at all**. Any hourly-c/w study is capped at ~2 yrs / single regime — the 10-yr answer
  is the daily-close c/w that is already the deployed gate.
- **Stock credit engine scans exactly once/day at 15:10** (`STOCK_CREDIT_SCAN_AFTER = "15:10"`, guarded
  once-per-date) — no hourly loop; "fire the first intraday touch of 0.40" is a likely trap (selling into
  reverting IV spikes), which is why the close-gate is intentional. See [[trading-strategies]].
- **Queued validation-only job "Backtest hourly-touch vs close-gate 0.40 (v2+v1)"** → will write
  `HOURLY_VS_CLOSE_ENTRY.md` + a UI card, no live-engine change; measures whether the extra signals the
  hourly rule catches are reverting-spike noise or real edge, over the ~2 yrs of intraday data. Not yet run.

Current research/backtests live in `studies/`; `How_We_Built_The_Strategy.pdf` and
`BACKTEST_RESULTS.md` are the historical build journey (superseded).

Part of [[files-repo]].

**2026-08-10 — the v0 book, one cross-book re-entry rule, and a deployment freeze:**
- **STOCK CREDIT v0 is the third stock book** (`engine/stock_credit_v0.py`, live paper since
  2026-07-31). The v2 gate takes credit/width at or above 0.40, so names kept piling up in the
  watchlist just underneath it. v0 runs v2's exact geometry on the 0.35–0.40 band with the exits
  that band wants: take profit at 40% of credit, no stop. It imports v2's module through importlib,
  so every v2 fix reaches it automatically. The evidence is deliberately thin and the page for it
  says so: in-sample 2019→Sep'24 wins 77.4% and is positive in only 4 of 6 years (n=310), while
  out-of-sample Oct'24→Jul'26 wins 90.7% and is positive in all 3 years on just 43 trades.
- **The band below is dead and stays rejected.** A 432-configuration sweep over geometries, strike
  steps, widths, targets and stops found 0.30–0.35 negative in every test (+0.2% in-sample, −5.2%
  out-of-sample). See [[trading-strategies]].
- **The 3-day re-entry gap is now cross-book.** No book fires on a name that any book entered within
  `STOCK_CREDIT_REENTRY_GAP_DAYS`. One function, `data_utils.recent_entry_symbols()`, reads all three
  book files, so the rule cannot drift between books. This matches the backtest, where the gap was
  per symbol with no notion of separate books. A repeat entry at new levels is allowed once the gap
  expires; consecutive days are not.
- **The engine is frozen for deployments between 15:15 and 15:40.** Day markers live in memory, so
  restarting inside the scan window makes it re-scan. Deploy after the close.
- **Timings moved:** the watchlist digest rebuilds at 15:31 on the post-auction close and the stock
  credit scan runs once at 15:36. The 15:10 figure recorded above is stale.
- **Watchlist prices are verified against [[nse-bhavcopy]], 33 of 34 exact over two sessions.** When a
  specific name is challenged, compare its signal price to `ClsPric` in the bhavcopy rather than
  reasoning from the code. That is what settled both HAL and GRASIM.

**2026-08-11 — index prices get their own source file, and the message wording is his:**
- **An index close is verified against NSE's index file, not the bhavcopy.** The CM bhavcopy carries
  equities only and has no NIFTY row, so it can never settle an index price. The official closes sit
  at `nsearchives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv`. All three checked exact
  to the paisa that day: NIFTY 24,471.70, FINNIFTY 26,432.40 and BANKNIFTY 57,446.25. So
  `todays_close()` is correct for indices as well as stocks. Use the file that covers the instrument
  class before arguing about a price. See [[nse-bhavcopy]].
- **The swing credit book is switched off and stays off.** `SWING_CREDIT_ENABLED` has been False
  since 2026-07-24, when the index fade failed out-of-sample at −1.4% of width. Its three open
  positions all date from July and predate the stale-bar fix, so they carry no signal price and no
  swing signal can fire until the flag flips. Anyone reading the book count should know that.
- **The Telegram wording is a spec, not a preference.** The NIFTY and SENSEX books say INTRADAY and
  never "0DTE" in anything a person reads. A result message names the execution date as an ordinal.
  The closing summary reads "TOTAL TRADES = 8 OUT OF WHICH OUR SYSTEM ACHIEVED 8 WINS AND 0 LOSSES",
  with no ticks and no crosses, and it bolds the win count, the percentage and the realized amount.
- **A higher credit/width is not always a better entry.** The 09:30 re-check splits the credit into
  time value and intrinsic before it says anything. Example: a credit of ₹29.50 at 0.492 was ₹9.80 of
  time value and ₹19.70 of intrinsic, because spot had moved ₹16.60 through the short strike, while
  the same ₹24.85 at entry was all time value. The edge this book trades is in the time value, so
  that is a do-not-buy even though the headline number improved.

## 2026-08-13 — T-1 closed, and a lesson about what a backtest cannot see

- **The T-1 (expiry-eve) entry is rejected and the region is closed.** Two studies record it so
  nobody mines it again. `studies/T1_EXPIRY_EVE.md` covers a 09:16 entry at 2% or more out of the
  money, which produces win rates of 95 to 100% on credits of about ₹3.70, at a credit/width of
  0.01 to 0.10 against the proven 0.40 gate. `studies/T1_CLOSE_ENTRY.md` is the main record, with
  1,405 trades and a true in-sample and out-of-sample split. NIFTY fails on money and on a
  direction that inverts out of sample. SENSEX cannot be tested before Oct-2024. Both are indexed
  in `studies/README.md`. Nothing was ever deployed.
- **A cadence change can invalidate a seven-year backtest, and no ₹/trade test will catch it.**
  BANKNIFTY held the only edge in that study that spanned both regimes, and it was priced on
  roughly 52 expiries a year. Weeklies have ended and the count is now 12 a year, so ₹38,446 a year
  becomes ₹9,612. Every statistical check ran on ₹/trade and none of them could have found this.
  Confirm that the instrument still trades on the cadence the backtest assumed. The re-open
  condition is recorded: BANKNIFTY weeklies returning.
- **Intraday option premiums exist from Oct-2024 onward.** An earlier claim that they cannot be
  tested at all was too strong. The hard boundary is pre-Oct-2024, which is a smaller claim. See
  [[upstox]].
- **The ₹60,000 exposure cap has now been asked for twice and still is not in the config.** He
  raised it on 2026-08-11 and again on 2026-08-13, and `engine/config.py` still reads
  `STOCK_CREDIT_MAX_EXPOSURE = 0`. Read the config before telling him a cap is live.
- **The viewer's watchlist table taught a Qt lesson worth keeping.** Turning the horizontal
  scrollbar off makes Qt compress columns whenever their total exceeds the viewport, so every
  fixed width in the code was silently overridden and six rounds of pixel-tuning changed nothing.
  Columns now take shares of the measured viewport and wrap to a second line rather than clip.
  The general point is that his screenshots found three defects that every code check had passed,
  so verify the render rather than the source.

## The corporate-action bug and the leadership reversal (2026-08-15/16)

**A scale mismatch had been fabricating wins for the whole history of this repo.**
`fetch_upstox_historical` returns split- and bonus-ADJUSTED closes, while bhavcopy `STRIKE_PR`
and Upstox expired strikes are UNADJUSTED as listed. On a split name the two scales diverge,
ATM pins to the far end of the ladder, both legs get picked deep ITM, credit approaches width,
margin approaches zero, and settling against the same adjusted price books a full-credit win
that never happened. The symptom was visible in the per-symbol median credit-to-width: HCLTECH
0.96, PIDILITIND 0.95, DRREDDY 0.95, HDFCBANK 0.91, all of them split or bonus names, against
0.44–0.49 on names with no corporate action. He root-caused it by refusing a +182.8% ROM and a
1.92:1 win-to-loss as impossible for a vertical, and by refusing an arbitrary c/w cap and asking
for evidence instead.

**The fix is put-call parity rather than a heuristic guard.** Two guards were tried and failed.
Spot is now derived from the option chain itself, `S = K + C − P` at the strike where `|CE − PE|`
is least, because both quotes carry the same unadjusted scale as the strikes and a split cannot
desync them. The adjusted equity series is still used for the Donchian breakout only. In-sample
can do this because bhavcopy carries every strike. Out-of-sample cannot, because Upstox expired
candles exist only for strikes that actually traded, so a parity OOS run returned two of the
books at almost no trades. OOS still uses drift and ladder-edge guards, and that asymmetry is a
known weakness of the current numbers.

**The headline is now the median cohort, because the high-c/w tail is not what the live book
trades.** v2 draws 33.4% of its profit from c/w ≥ 0.65 and v1 draws 38.8%, on high-priced
dense-ladder names such as MARUTI at 0.73 and LT at 0.60, while all 21 live fills sit at c/w
0.39–0.47. At the median cohort the honest numbers are v2 80.3% win and +24.0% ROM in-sample
against 77.1% and −0.3% out-of-sample, v1 79.7% and +23.5% against 80.2% and +5.4%, and v0
81.5% and +18.8% against 76.8% and −3.9%. **v1 is the only book positive in both windows, which
reverses the entire history of this repo.** v0 has no tail at all because its band caps at 0.40,
so its headline needs no discount.

**A bootstrap then showed the out-of-sample window cannot rank the books at all.** The 90%
confidence intervals are v2 [−26.6%, +29.9%], v1 [−3.3%, +13.5%] and v0 [−18.7%, +9.1%], and all
three contain zero. v2's 2024 "year" is four trades. In-sample is far better measured but it is
circular, because the c/w gate, the geometry, the TP levels and the union were all chosen on that
window, and it carries its own defect: bhavcopy closes are settlement prints, and 85% of rows
with premium at or above ₹50 carry zero open interest. **Neither window is a green light, so
nothing was deployed.** See [[capital-curve-verdict]] and [[trading-strategies]].

**The take-profit sweep refuted his own suggestion.** He proposed cutting v2's target to force a
positive net. A lower target buys win rate and gives back average win size, and the two cancel:
v2's ROM is flat between +23.4% and +24.1% in-sample across a range that more than doubles the
target, and TP-30 is its worst out-of-sample cell at −3.4%. v2 is positive in 2 of 3 years at
every level, so no exit fixes a year-failure. **A parameter whose slope inverts between windows
is noise**, which is exactly what v1 does — ROM falls as TP rises in-sample and rises
out-of-sample — so v1 stays at TP-40 even though the OOS column alone would argue for TP-70.

**The harness now models the live one-open-position-per-symbol rule.** Each book tracks the exit
date of the position it holds per symbol and refuses to re-enter that name until it closes. The
old harness only enforced the 3-day gap, so 59% of in-sample trades and 31% of out-of-sample
trades were same-book re-entries inside 35 days, which the live engine could never have taken.
The bias has a direction: a winner hits its target fast and releases the name while a loser stays
open to expiry, so the counted re-entries were drawn disproportionately from names still going
against the book. Five harness gaps stay open — daily caps, 2019-era lot sizes, margin computed
as width minus credit rather than SPAN, no bid-ask or open-interest gate, and guards rather than
parity out-of-sample — and the harness has not been adversarially audited since the parity fix.
See [[backtest-harness-audit-rule]].

**Everything published is still pre-parity and wrong.** The viewer tables and cards, studies SS5
and SS6, the Telegram evidence lines and the CLAUDE.md book table all carry superseded numbers
until one consolidated correction pass runs.

## 2026-08-17 — the open-interest gate conceded, and the ceiling named

**He challenged the open-interest gate and he was right.** It was deployed at ten lots, then five,
then dropped to "any open interest at all", and every one of those deploys rested on how many signals
survived rather than on any measured win rate or return. No threshold above zero has ever been tested
for profitability in either window. What the gate genuinely is: a fidelity fix. A bhavcopy close on a
contract that never traded is NSE's theoretical settlement price rather than a price anyone could
have filled, so pricing entries off those contracts inflates the result. Applying the gate roughly
halved in-sample return, and that is a measurement correction rather than evidence the gate helps.
Live it is inert, because the bid-ask check blocks every name the open-interest gate blocks and six
more besides.

**The structural ceiling is now the honest headline caveat.** The live engine refuses a trade whose
bid-ask spread is worse than 6%, and on 17 August that gate rejected **10 of 17 candidates, 59% of
them**. No bhavcopy backtest can ever apply it, because those files carry a close and an open-interest
figure and no bid or ask at all. So every published return is computed over a population that includes
names the engine would have refused as too wide to trade, and that is a larger source of optimism than
any open-interest threshold. The audit therefore scores the harness at 7 out of 10 with a ceiling near
8: reaching 8 means every known bug fixed and both windows re-run, 9 would need real historical
bid-ask data that does not exist at any price he knows of, and 10 is not a backtest at all. The
forward record began on 6 August and holds four resolved trades. At fifty it would say more about
whether these books work than every hour of harness work, because it is the only measurement that
includes the spread gate, the actual fills and the slippage. See [[backtest-harness-audit-rule]].

## The frozen-parameter defect, found on a live position

No book has run a stop since July, and one open position had one anyway. `stop_cost` is written into
each position record at entry and frozen there, so a BAJAJ-AUTO bear call opened on 29 July kept the
stop that was policy that day. Nineteen days later it sat about thirty points from firing and
realising a loss of ₹9,068 under a policy that says there are no stops. He cleared it. New positions
now store no stop at all, and a module-level override inside the v2 book — which was the real source
of the phantom stop the viewer had been advertising for weeks — is gone.

Clearing the field exposed a second bug immediately: the resolver compared a float against an empty
value, which raises an error that the surrounding handler would have swallowed on every cycle.
**The general defect stands and is worth carrying to any system with frozen parameters: no book
re-checks its stored exit rules against the current configuration when it loads.** The take-profit
level is safe only by accident, because positions store no take-profit field and the resolver reads
the current value each time it runs.

## The day the engine called a trading day a holiday

On 17 August the engine lost its network at 15:15, and the watchlist he stages before the close was
lost with it. The chain is worth keeping because every link is a common mistake. A recheck routine
rebuilt its whole message every five seconds from 09:30 onward, roughly 66,000 needless API calls a
day, which exhausted the connection. The failure surfaced as an empty result rather than an error, and
the market-open check cannot tell an empty result from a day on which nothing traded, so it concluded
the exchange was shut and cached that verdict. The 15:17 list ran late and found nothing; the 15:31
rebuild found twenty breakouts.

The fix reads the engine's own database first. It writes a market snapshot every few seconds all
session, and it was sitting on 3,301 snapshots dated that day while it declared a holiday. That layer
needs no network at all. If both it and the index check are silent the day is treated as trading and
the verdict is never cached, because **a false holiday silently costs a whole trading day while a
false trading day costs nothing — the per-stock price guard still refuses to fire on stale data.**

Settlement carried a related defect. It asked for the expiry day's bar, got an empty result because
the vendor publishes no same-day daily bar, and fell through to the current live price on every
settlement. It only ever looked correct because settlement runs after 15:40, when the live print
happens to equal the auction close, which was undocumented and load-bearing. It now settles only on a
bar dated the expiry itself.

Research inputs moved out of `/tmp` into a gitignored `research/` directory after `/tmp` was wiped
twice, taking a 1.6 GB price pickle and a cached options-leg store with it and killing two sweeps.

## Architecture is now drawn, not only described

The README carries two mermaid diagrams inside the existing architecture section. The first shows the
data flow, and it makes the decoupling visible: every arrow into the viewer comes from disk and none
comes from the engine, so a viewer crash cannot stop trading. The second is the daily clock as a
timeline from the 09:15 open through the 15:15 auction and deployment freeze, the 15:17 pre-stage
list, the 15:31 digest, the official close struck at 15:35, the scan at 15:36 and settlement at
15:40. Mermaid was chosen over an image on purpose, because GitHub renders it natively and it stays
diffable, so a schedule change moves the diagram in the same commit instead of leaving it silently
stale. The 15:17 watchlist is a pre-stage list rather than a signal, because it is built before the
auction matches and its strikes can still move. See [[nse-bhavcopy]] and the session note in
[[trading-strategies]].
