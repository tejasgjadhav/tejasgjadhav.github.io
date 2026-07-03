---
title: ~/files repository — overview
type: project
tags: [overview, hub]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files]
---

The `~/files` git repo is [[tejas-jadhav]]'s working monorepo — CFA/FRM charterholder,
AI-finance guest faculty at SCMHRD, KDP author ([[kdp-books]]), and builder of
trading/finance software. Several subdirectories deploy as static sites via [[netlify]],
which also hosts a `claude` serverless function ([[claude-anthropic]]).

## Projects (as of 2026-07)

- [[institutional-trader]] — NSE intraday options paper-trading system (the most active project)
- [[jarvis]] — J.A.R.V.I.S. Mark VII voice assistant, local-only deployment
- [[dotnet-architect-book]] — "The Senior .NET Architect's Handbook", 15-part book build
- [[kdp-dashboard]] — Amazon BSR tracking dashboard for his 5 KDP books
- [[trade-regimes-website]] — T&T regulatory reporting reference site (EMIR, Dodd-Frank, etc.)
- [[scmhrd-ai-finance]] — personal professional site: AI Finance expert / SCMHRD guest faculty
- [[upstox-data]] — shared Upstox instrument/options JSON supporting the trading work

Repo root also holds `index.html` (personal site: "Tejas Jadhav CFA FRM | AI in Finance
Author | Pune India"), `portfolio-review.html` (mutual fund portfolio review), `logs/`,
and Netlify/Google-verification config.

This wiki (`wiki/`) lives here too and is maintained per its own `CLAUDE.md` schema;
its link graph is kept current at `wiki/graph.html`.
