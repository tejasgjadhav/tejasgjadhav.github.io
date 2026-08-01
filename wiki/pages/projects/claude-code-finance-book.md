---
title: Claude Code for Finance (book build)
type: project
tags: [book, kdp, claude-code, writing]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/claude-code-finance-book/HANDOFF.md]
---

Book build at `~/files/claude-code-finance-book`, aimed at finance people who do not code.
**v3 delivered 2026-07-25**: 172-page 6×9 PDF (`claude-code-for-finance.pdf`) plus EPUB
(`Claude_Code_for_Finance_2026.epub`), 18 parts, ~43k words. Compliance scan clean. Cover
art and the KDP upload were left to [[tejas-jadhav]] separately.

**v1 was rejected outright by the author as AI slop and rebuilt from scratch.** The rebuild
is the interesting part, because it produced a reusable drafting pattern: every number in
the book has to come from a `facts/*.md` file written from a real captured session, and the
drafting agents are forbidden from inventing figures — a facts firewall. Real terminal
sessions were captured through a GNU `screen` harness (`demo/scap.sh`, `demo/repl.sh`) with
screenshots taken by computer-use, because the macOS `screencapture` CLI is blocked in that
context.

Structure: Part I setup (setup, prompt craft, goals and loops, `CLAUDE.md` + handoff +
memory wiki, wiring GitHub/API/connectors), Part II desks (fundamental analysis, valuation
via [[jarvis]], fixed income, [[institutional-trader]], technical analysis, portfolio
management, corporate finance and FP&A, Citi Pillar 3 via [[basel-analyzer]], ESG, ethics,
a thirty-day plan, appendix). US-oriented, with India as callout rather than default — the
same reorientation applied to [[claude-algo-trading-book]].

Voice exemplar for the whole build was
`claude-algo-trading-book/parts/02-working-with-the-machine.md`. See [[kdp-books]] for the
published catalog.
