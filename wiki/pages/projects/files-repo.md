---
title: ~/files repository — overview
type: project
tags: [overview, hub]
created: 2026-07-03
updated: 2026-07-05
sources: [~/files]
---

The `~/files` git repo IS `github.com/tejasgjadhav/tejasgjadhav.github.io` — [[tejas-jadhav]]'s
personal site repo, deployed via **GitHub Pages** (not Netlify — see correction on
[[netlify]], which hosts only a `claude` serverless function proxying
[[claude-anthropic]]). It's also his working monorepo — CFA/FRM charterholder, AI-finance
guest faculty at SCMHRD, KDP author ([[kdp-books]]), and builder of trading/finance
software. [[scmhrd-ai-finance]] and AIFINANCE are separate repos deployed as GitHub Pages
subpaths (`/SCMHRD/`, `/AIFINANCE/`) of the same site — never commit them into `~/files`
itself (a gitlink got in once and had to be removed).

## Projects (as of 2026-07)

- [[institutional-trader]] — NSE intraday options paper-trading system (the most active project)
- [[jarvis]] — J.A.R.V.I.S. Mark VII voice assistant, local-only deployment
- [[voicebox]] — dev checkout of the open-source local AI voice studio (cloning, TTS/STT, MCP)
- [[dotnet-architect-book]] — "The Senior .NET Architect's Handbook", 15-part book build
- [[kdp-dashboard]] — Amazon BSR tracking dashboard for his 5 KDP books
- [[trade-regimes-website]] — T&T regulatory reporting reference site (EMIR, Dodd-Frank, etc.)
- [[scmhrd-ai-finance]] — personal professional site: AI Finance expert / SCMHRD guest faculty
- [[aifinance]] — AI-in-finance landing page, own repo deployed at `/AIFINANCE/`
- [[upstox-data]] — shared Upstox instrument/options JSON supporting the trading work

Repo root also holds `index.html` (personal site: "Tejas Jadhav CFA FRM | AI in Finance
Author | Pune India"), `portfolio-review.html` (mutual fund portfolio review), `logs/`,
and Netlify/Google-verification config.

This wiki (`wiki/`) lives here too and is maintained per its own `CLAUDE.md` schema;
its link graph is kept current at `wiki/graph.html`.
