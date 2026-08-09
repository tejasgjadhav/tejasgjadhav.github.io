---
title: ~/files repository — overview
type: project
tags: [overview, hub]
created: 2026-07-03
updated: 2026-08-09
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

**That rule has teeth — the live site was frozen for a week (found 2026-08-09).** Twelve
sub-project directories with their own repos had been committed as **gitlinks** (mode
`160000`) with no `.gitmodules`. GitHub Pages cannot resolve a gitlink, so the build kept
failing and the published site stayed on its **2026-08-02 deploy** while `main` moved on —
silently, because a failed Pages build looks like nothing at all from the browser. Fixed by
untracking the twelve and gitignoring them (commit `486dc75`), which is how
[[scmhrd-ai-finance]] was already handled; working directories were untouched and each
project keeps its own repo. When the live site looks stale, the check is
`git ls-files -s | grep 160000` — any hit is the bug.

## Projects (as of 2026-08)

- [[institutional-trader]] — NSE intraday options paper-trading system (the most active project)
- [[vt-ocs]] — ORB → Turtle → CPPI cash-equity system, paper engine deployed via launchd
- [[jarvis]] — J.A.R.V.I.S. Mark VII voice assistant, local-only deployment
- [[voicebox]] — dev checkout of the open-source local AI voice studio (cloning, TTS/STT, MCP)
- [[dotnet-architect-book]] — "The Senior .NET Architect's Handbook", 15-part book build
- [[kdp-dashboard]] — Amazon BSR tracking dashboard for his 5 KDP books
- [[trade-regimes-website]] — T&T regulatory reporting reference site (EMIR, Dodd-Frank, etc.)
- [[scmhrd-ai-finance]] — personal professional site: AI Finance expert / SCMHRD guest faculty
- [[aifinance]] — AI-in-finance landing page, own repo deployed at `/AIFINANCE/`
- [[upstox-data]] — shared Upstox instrument/options JSON supporting the trading work
- [[basel-analyzer]] — Basel III / Pillar 3 report analyzer (local-only repo)
- [[in-eq]] — multi-agent equity research MVP, keyless template mode, own repo
- [[ninja]] — institutional wealth advisory platform (IPS + portfolio engines), own repo
- [[endowment-advisor]] — multi-agent endowment chatbot with .pptx deck generation
- [[amazon-ads]] — Sponsored Products campaign state for the flagship KDP title
- [[clearframe-studio]] — free multilingual AI video suite (prototype and parser seed)
- [[kalpana]] — the engineered AI film studio that replaced it, milestone-gated
- [[globalaar-ops]] — LAN factory shop-floor operations app (the one non-finance project)
- [[claude-code-finance-book]] — "Claude Code for Finance" book build
- [[claude-algo-trading-book]] — "Claude for Algo Trading" book build
- [[company-finance-app]] — one-screen Flask lookup: company name in, price/revenue/market cap out

Repo root also holds `index.html` (personal site: "Tejas Jadhav CFA FRM | AI in Finance
Author | Pune India"), `portfolio-review.html` (mutual fund portfolio review), `logs/`,
and Netlify/Google-verification config.

This wiki (`wiki/`) lives here too and is maintained per its own `CLAUDE.md` schema;
its link graph is kept current at `wiki/graph.html`.
