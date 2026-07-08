---
title: Trading strategies — the 4-strategy lineup and their honest standing
type: concept
tags: [trading, strategy, nse, options, backtest]
created: 2026-07-03
updated: 2026-07-08
sources: [~/files/institutional-trader/CLAUDE.md, ~/files/institutional-trader/studies/STOCK_OPTIONS_NO_EDGE.md, ~/files/institutional-trader/studies/CAPITAL_CURVE_RESULTS.md, ~/files/institutional-trader/studies/INTRADAY_90PCT_WINRATE.md]
---

The strategies implemented in [[institutional-trader]], with their validation status as of
2026-07. All run as **paper forward-tests** (manual orders in Upstox, [[upstox-data]] feed).

## 1. 3-Family stocks (intraday, ~100-stock universe)

Alpha-z score (TREND 0.72 + FLOW 0.18 + EVENT 0.10) → gates: |alpha-z| > 0.55 with ≥2/3
families agreeing · 5-min ORB break with volume surge · market alignment (long only when
Nifty up, short when down) · min option premium ≥ ₹30 on the OTM+1 · liquidity (spread ≤ 4%,
OI ≥ 100). Buy OTM+1 CALL/PUT, exit +10% / −15% on premium. Gates 4 (don't-chase) and 5
(wide-open) were **disabled 2026-06** — didn't hold on real option data.

**Standing: real DIRECTION edge, but not net-profitable as option-buying.** Tested full-gate on
REAL Kite 5-min back to 2019 ([[buy-strategies-real-2019]]): 19,454 signals, **50.6% hit,
+0.107%/trade on the underlying, positive in EVERY year 2019→2026.** The gates are real — a no-gate
proxy is a 48% coin flip — so this is a fairer verdict than "overfit". BUT +0.107% is the *underlying*
move; options leverage it ~10× yet theta/IV/bid-ask/−15% stops/costs eat it → the engine's real-option
1-year test came in **−1.0% net (55% win)**. Direction durable, execution unprofitable. Min-premium is
kept only for the cost/spread benefit (~3× tighter spreads); the 13 `PRIORITY_STOCKS` are a UI focus
tilt only (per-stock win-rate selection overfits).

## 2. ORB+VWAP index (NIFTY/BANKNIFTY, intraday)

15-min ORB + VWAP + 30-min trend + clean-trend filter → buy ATM, trend-ride exit (exit on
VWAP reclaim after +12%, hard −15% stop).

**Standing: thin AND inconsistent — weaker than the 18-month window implied.** The +0.9%/18mo
(train+test) looked durable, but the REAL Kite 5-min test back to 2019 ([[buy-strategies-real-2019]])
shows only **+0.04% underlying move/trade, ~39% hit, and NEGATIVE in ~2 of 8 years per index** (NIFTY
2020/2026; BANKNIFTY 2023/2025). Options leverage the lean but theta/IV/−15% stops/costs eat it
(engine standing: "+0.8% gross → ~0% net"). A thin, regime-sensitive forward-test — 3-Family's
direction edge is actually MORE consistent than this one.

## 3. Index fade credit spread (NIFTY + FINNIFTY, multi-day — "swing credit")

Daily Donchian-10 breakout → **sell a credit spread against it** (up-break → bear-call,
down-break → bull-put), ≥10 DTE, short 1-OTM, width 3, hold to expiry, hard stop 2× credit.
Overnight carry. `engine/swing_credit.py`.

**Standing: DOWNGRADED (2026-07) — regime-dependent, not durable.** Looked validated on the
Oct'24–Jun'26 window (+12–20% net/trade), but the **real-data test on [[nse-bhavcopy]] premiums
2019→Sep'24 came in NET-NEGATIVE (−1.4% of width, 181 trades)** — positive only in 2019 & 2024,
the favorable regimes. A [[real-data-fade-validation|salvage attempt]] (fade DOWN-breaks only +
flush ≥0.5%) looked great in-sample (+15.1%, 78% win, 6/6 years) but **FAILED out-of-sample** on
Upstox Oct'24→date (the direction asymmetry reversed; deployed gate −2.8%) — a bull-regime
artifact. Gates reverted; the fade runs ungated as a small forward-test. The *follow* version loses
too — no durable directional edge, it's regime timing. Capital curve (favorable-regime figures, 43
trades/20 mo): ~0.8%/mo on ₹2 L at 13% DD; 5%/mo infeasible by 3–6× ([[capital-curve-verdict]]).

## 4. Stock fade credit spread (~100 stocks, high frequency ~16/mo)

Same fade, gated on credit/width ≥ 0.40 (rich premium = elevated post-breakout IV — the
edge) + short premium ≥ ₹50 + liquidity + open-position caps. `engine/stock_credit.py`.

**Standing: REAL-DATA CONFIRMED (2026-07) — the one durable, regime-robust edge.** Tested on
[[nse-bhavcopy]] premiums 2019→Sep'24 (718 trades): **+5.3% of width (~+9%/trade on margin),
54% win, positive in 5 of 6 years.** The credit/width gate IS the edge — strip it and the same
universe loses (−1.1%, like the index and like a generic spread). But the real edge is **~⅓–½ of
the optimistic backtest** (+16–25% → +5.3%; 65% → 54% win), so it's durable but modest, high
variance (2023 was −4.5%). **Keep lots at 1** (live mid-cap fills erode it further). See
[[real-data-fade-validation]].

## 1b. Stock fade v2 — TP-50 (THE LEADER, deployed 2026-07-04)

Same signal + gate as #4's stock fade, new geometry/exits: **short 2-OTM · width 4 · take-profit 50%
of credit · stop 3×**. 96-config grid on real bhavcopy (entry+exit costs) then OOS on Upstox
Oct'24→Jul'26: **in-sample 85.35% win (233W/40L), +24.5% of width, win ≥79% every year 2019–24;
OOS 87.88% (116W/16L), +31.9%.** Only 4 of 60 months negative; max losing streak 4; median win +32 /
median loss −51 (% width). ~4–6 trades/mo (vs v1's ~10). Runs PARALLEL to v1 at 1 lot;
ORB+VWAP retired from the dashboard to make room. Live fills = the one unproven link.
Study: `institutional-trader/studies/STOCK_FADE_TP50_UPGRADE.md`.

**Cross-book dedup (2026-07-07, commit `334dac1`):** because v1 and v2 share the same signal, both
would fade the same stock and stack two positions on one name. Now enforced permanently — **one
position per stock across both books, v2 always wins**: the runner reorders so v2 scans first (its book
is current when v1 runs) and v1 then skips any stock v2 already holds open. Same session added a
phantom-strike guard (rejecting bogus/non-existent strikes before they book).

## 5. Index 0DTE expiry-day call-spread — NIFTY Tuesday (deployed) + SENSEX Thursday / BANKNIFTY (rolling out)

A distinct edge from the multi-day #3 index fade: an **expiry-day 0DTE** short call-spread —
short CE ~0.5% OTM at the open, ~200-pt wing, settled the same day — gated by a **calm-week
filter** (`rv5`, realized vol from the prior 5 closes; skip when the tape is hot). On NIFTY this
runs on **Tuesday** weekly expiry and is **fully deployed** (commits `e0a4e9b`, `e69f827`), first
live paper entry 2026-07-07 09:16. The INTRADAY DECISIONS tab now reads top-to-bottom: a dynamic
pre-market **status strip** (🟢 "signal expected 9:16 · rv5 calm" / 🟡 filter says skip / ⚪ not
expiry — both inputs, expiry calendar + rv5, are final by 9:00 so the strip is reliable pre-open),
a one-line banner (*0DTE NIFTY CE spread · ~90% win OOS · +5.9%/margin · margin ≈ ₹14k/lot = max
loss*), a 5-line rules card, then the trade table. The 0DTE book renders in the **same 2-leg
swing-table format** as the credit-spread books (① SELL / ② BUY · instrument · lot · entry premium
· now/exit · leg P&L · net/status) in BOTH the INTRADAY DECISIONS tab and a new TRADE-LOG-tab
section. Actual short strike = live opening price × 1.005 → nearest 50, set at 9:15–9:16.
Averages ~₹2.3k/month/lot and takes a −₹12k week a few times a year.

**Calm-filter, quantified + deployed (2026-07-07, commit `91a6330`):** the gate is **skip the week
when NIFTY `rv5` ≥ 0.9%** — losses cluster when recent realized vol / 5-day run-ups are high; VIX
added nothing beyond `rv5`. Filtered vs unfiltered on 2019→Jun'26: **win 85.0% → 87.8%, avg +3.2% →
+4.0% of margin, 2025 +₹1,715 → +₹23,219, max DD −₹23.9k → −₹17.3k**, ~278 trades vs 373, total 7.5-yr
PnL within 4% (₹136k vs ₹142k). Filtered is the chosen deployed version; it passed the repo's
robustness gates (threshold-neighborhood 0.7–1.2, untuned 0.75%-OTM sibling, mechanism = a short-gamma
book belongs in calm regimes). A separately-tested **90% VWAP-flush stock intraday** idea (buy a stock
≥2% below day-VWAP, TP +0.20% / stop −3.0%, EOD close) was **rejected as non-deployable** — the 90% win
is manufactured by the risk-3%-to-make-0.2% exit geometry (a no-signal baseline already wins ~83%); net
−0.095%/trade after costs (`studies/INTRADAY_90PCT_WINRATE.md`). Confirms the house lesson that a high
win *rate* is not an edge.

**Second-payday research (2026-07-06, via /loop):** the same structure ported to **BSE SENSEX
Thursday** weekly expiry (short CE ~0.5% OTM, ~600-pt wing ≈ same %). Backtested on all **89
expired SENSEX weeklies Oct'24→Jul'26 with real premiums: 88.8% win, +7.57%/margin, +₹67k (1
lot); 2025 alone 90.2%, 2026 H1 92.3%.** NOT yet deployed — honest caveats: only 21 months of BSE
history (no 2019 depth — BSE weeklies are young), Oct–Dec'24 was negative (expiry-change era), the
NIFTY calm-filter does **not** transfer to SENSEX (it would run unfiltered or self-tuned), and BSE
option spreads are wider than the cost model assumes. Combined "Tuesday + Thursday" ≈ ₹5.5k/mo/lot
but paid **lumpily** (many +₹1–3k weeks, a −₹15–30k week several times/year). See
[[capital-curve-verdict]] — 5%/mo remains infeasible; this adds paying *days*, not a bigger edge.

**Rollout plan (as of 2026-07-07):** a post-market (~4 PM) routine is scheduled to install the
**SENSEX Thursday** and — *if it validates* — **BANKNIFTY** 0DTE books, each rendering in the same
intraday 2-leg table + trade log. (Note: this is the expiry-day 0DTE CE-spread family — distinct
from the *daily Donchian* BANKNIFTY fade that was rejected at −6.7% under #3.) The app also now
surfaces a **consolidated monthly-PnL view** (STUDIES tab + GitHub) across the whole live lineup —
stock fade v2 (2 lots) + stock credit (1 lot) + intraday NIFTY / SENSEX / BANKNIFTY 0DTE — so the
blended, honestly-lumpy monthly number sits in one place.

## Cross-cutting lessons

- **Real option history goes back to 2019 after all** — via [[nse-bhavcopy]] (free daily CLOSE +
  OI for every contract, incl. expired), the data no broker API exposes. This unlocked the true
  pre-2024 backtests that overturned the index-fade "validation." Upstox expired-instruments
  reaches back only to Oct 2024.
- **6 positive years inside ONE regime is NOT out-of-sample.** The index-fade gate passed a 6/6
  year check and a positive bootstrap p5, yet failed the moment a genuinely different regime
  (Oct'24→date, post-peak correction) was tested. Only a different *regime* is a real holdout.
- Train/test inside a short window is not true out-of-sample — use the longest window the
  data allows.
- The ~100-stock universe is hand-picked by intraday movement, not market cap — a
  free-float-mcap top-100 lost head-to-head (61% vs 67%).
- House rule: honesty over optimism — frame everything gross-vs-net, sample size,
  out-of-sample fragility. Backtest before deploying any tunable change.

Research trail: `institutional-trader/studies/` (STOCK_OPTIONS_NO_EDGE.md Parts 10–11 hold the
real-bhavcopy verdicts + the failed index-fade gate) + reproducible scripts. Synthesis:
[[real-data-fade-validation]].
