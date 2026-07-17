---
title: Claude for Algo Trading (book build)
type: project
tags: [book, kdp, algo-trading, writing]
created: 2026-07-14
updated: 2026-07-16
sources: [~/files/claude-algo-trading-book]
---

Book project: **"Claude for Algo Trading — Algo Trading Strategies, Backtesting and All"**
by Tejas Jadhav, CFA. First full draft completed 2026-07-10 (~16.7k words, 14 parts).

**Pipeline** (copied from [[dotnet-architect-book]]): markdown `parts/*.md` → `build.py` →
`book.html` → `claude-for-algo-trading.pdf`, rendered with headless Chrome (WeasyPrint is
broken on this Mac — the same [[files-repo]] gotcha).

**Source material** is the [[institutional-trader]] repo: README, CLAUDE.md,
BACKTEST_RESULTS.md, and `studies/` (STRATEGY_SUMMARY.md, STOCK_FADE_TP50_UPGRADE.md,
DATA_AVAILABILITY_LIMITS.md). The IS/OOS seam used in ch4 *is* the data boundary itself —
bhavcopy 2019→Sep'24 in-sample, Upstox expired-contracts Oct'24→Jul'26 out-of-sample,
Zerodha Kite 5-min for the underlying.

**Screenshots are real:** 6 GitHub captures via headless Chrome plus 5 live dashboard tabs
rendered by the actual PySide6 app through `QWidget.grab()` (Qt self-render needs no
screen-recording TCC, unlike shell `screencapture`).

**Voice:** the humanizer skill (popular non-fiction, first person, no AI slop). Standing
constraint — the author is a CFA charterholder, so **no investment advice**: everything is
framed as backtests against stated parameters, with disclaimers in the frontmatter and
Appendix D.

**Reoriented global-first (2026-07-14).** The book no longer opens in Indian markets cold:
the front matter now leads by saying the method is universal ("it works in New York, London,
or Mumbai") and frames India as the author's *worked example*, not the default. A front-matter
**India→US translation table** maps every local term in one glance — NSE→NYSE/Nasdaq,
Nifty→S&P 500, Sensex→Dow, Bank Nifty→XLF, Upstox/Zerodha→Alpaca/IBKR/Schwab,
bhavcopy→(no cheap US equivalent), ₹1 lakh→~$1,200, ₹15 lakh→~$18,000, STT→brokerage/SEC
fees, 0DTE→same term — backed by inline glosses at first mention. GitHub screenshots were
re-captured against the updated README (now framed as a multi-strategy paper-trading system
with Windows installers and a strategy table, **235 commits**).

**Cover badge + Amazon platform-name rule (2026-07-16).** All three covers (Kindle ebook,
paperback wrap, hardcover) now carry a badge — **"INCLUDES THE COMPLETE OPEN-SOURCE SYSTEM ON
GITHUB."** — and the back-cover bio says the code/studies are "published openly on GitHub." This
applies a non-obvious KDP rule: **naming a platform ("GitHub") is allowed; printing a URL/link is
what Amazon prohibits** — so reference the repo by platform name, never as a `github.com/...` link,
on any cover or interior.

One of the KDP titles alongside those tracked in [[kdp-dashboard]]. Part of [[files-repo]].
