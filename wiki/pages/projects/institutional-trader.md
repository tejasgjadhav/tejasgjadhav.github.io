---
title: Institutional Trader — NSE intraday options paper-trading
type: project
tags: [trading, nse, options, python, upstox]
created: 2026-07-03
updated: 2026-07-20
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

Current research/backtests live in `studies/`; `How_We_Built_The_Strategy.pdf` and
`BACKTEST_RESULTS.md` are the historical build journey (superseded).

Part of [[files-repo]].
