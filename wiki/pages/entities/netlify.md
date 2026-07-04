---
title: Netlify — serverless function for the ~/files sites
type: entity
tags: [hosting, deployment]
created: 2026-07-03
updated: 2026-07-05
sources: [~/files/netlify.toml]
---

**Correction (2026-07-05):** the `~/files` repo's own git remote is
`github.com/tejasgjadhav/tejasgjadhav.github.io` — the root site (and [[scmhrd-ai-finance]]
at `/SCMHRD/`, and AIFINANCE at `/AIFINANCE/`, each its own repo) is actually served by
**GitHub Pages**, not Netlify. `netlify.toml` still exists in the repo and defines
serverless functions in `netlify/functions/` — notably a **`claude` function** (26 s
timeout, `/api/claude` redirect) that proxies the [[claude-anthropic]] API — but Netlify's
role here is the serverless function only, not static-site hosting. [[trade-regimes-website]]'s
hosting wasn't re-verified in this pass. [[jarvis]] was removed from web deployment (June
2026) and runs local-only.
