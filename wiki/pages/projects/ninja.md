---
title: NINJA — institutional wealth advisory platform
type: project
tags: [wealth, advisory, nextjs, github-pages, india]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/NINJA/README.md]
---

Client-side wealth advisory web app at `~/files/NINJA`, live at
`tejasgjadhav.github.io/NINJA`. Own repo, not part of [[files-repo]].

Flow: landing → a 6-question suitability interview (investor type, objective, horizon,
risk tolerance, corpus, constraints) → an **IPS engine** that codifies the answers into a
formal Investment Policy Statement (return expectations, risk profile, liquidity, asset
allocation with policy bands, review/rebalancing rules) → a **deterministic portfolio
engine** (risk × horizon allocation matrix, tilted by objective and constraints) mapped to
a curated catalog of real Indian products — mutual funds, index funds, international FoFs,
REITs/InvITs, PMS strategies → a dashboard with CAGR/volatility/Sharpe/drawdown, allocation
donut, geographic exposure, goal tracker, drift and rebalancing suggestions, one-page IPS
summary, and an auto-drafted quarterly review letter.

Both engines are **deterministic and rule-generated**, not LLM-generated — the "AI
insights" are rule outputs. That matters for the same no-advice reason that constrains
[[endowment-advisor]] and the books: [[tejas-jadhav]] holds CFA/FRM, so anything that
looks like personalized advice is a standards problem, not just a product choice.

Stack: Next.js App Router · React · TypeScript · Tailwind · shadcn/ui · Framer Motion ·
Recharts. Static export deployed by GitHub Actions. Dev server runs on the `/NINJA`
basePath; `npx tsx scripts/engine-sanity.ts` checks engine invariants.
