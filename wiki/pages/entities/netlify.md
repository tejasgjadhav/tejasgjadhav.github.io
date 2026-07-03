---
title: Netlify — deployment for the ~/files sites
type: entity
tags: [hosting, deployment]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/netlify.toml]
---

Hosts the static sites in [[files-repo]]. `netlify.toml` publishes the repo root and
defines serverless functions in `netlify/functions/` — notably a **`claude` function**
(26 s timeout, `/api/claude` redirect) that proxies the [[claude-anthropic]] API for the
web-deployed features. Sites served this way include the root personal pages,
[[scmhrd-ai-finance]] and [[trade-regimes-website]]. [[jarvis]] was removed from web
deployment (June 2026) and runs local-only.
