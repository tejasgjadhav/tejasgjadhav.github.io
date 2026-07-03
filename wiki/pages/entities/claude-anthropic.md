---
title: Claude / Anthropic API
type: entity
tags: [ai, api, llm]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/JARVIS/server.py, ~/files/netlify.toml]
---

Anthropic's Claude powers several things in [[files-repo]]:
- [[jarvis]] — the Flask backend calls the Anthropic API directly (`ANTHROPIC_API_KEY` in `.env`)
- [[netlify]] — a `claude` serverless function proxies the API at `/api/claude` for web features
- [[kdp-books]] — the flagship title *Claude AI for Finance Professionals* teaches Claude
  prompting to finance professionals
- This wiki itself is maintained by Claude Code following the schema in `wiki/CLAUDE.md`.
