---
title: IN-EQ — multi-agent equity research MVP
type: project
tags: [equity-research, langgraph, fastapi, nextjs, agents]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/IN-EQ/HANDOFF.md]
---

AI equity research MVP at `~/files/IN-EQ`, pushed to `github.com/tejasgjadhav/IN-EQ`.
Enter a company name or ticker; a multi-agent pipeline fetches free financial data, runs a
simplified DCF, compares peers, scores risk, and issues a Buy/Hold/Sell call on an
interactive dashboard. **Runs end-to-end with zero API keys** ("template mode").

- Backend: FastAPI + LangGraph, 11 agents in `backend/app/agents/`, one `POST /api/research`
  endpoint. `graph.py` wires parallel bands and joins; `state.py` uses `operator.add`
  reducers because parallel branches write the same keys.
- Frontend: Next.js 15 + TypeScript + Tailwind + Chart.js, 9 dashboard sections, 4 charts.
  `frontend/lib/types.ts` mirrors the contract emitted by `agents/dashboard.py` — they must
  be kept in sync by hand.
- Verified end-to-end on AAPL (USD) and RELIANCE.NS (INR, ₹/Cr formatting, India macro).

As of 2026-07 deployment is deliberately **not done**: `render.yaml` and the Pages workflow
are committed but no Render service exists and `API_URL` is unset. Adding an
[[claude-anthropic]] key flips `meta.llm_mode` to `"claude"` and turns on real narratives
for news/risk/thesis.

Gotchas: the venv is `uv`-managed with no pip (`uv pip install --python .venv/bin/python`),
Python 3.12 because system python is 3.9; Node comes from nvm, off the default PATH; ports
are **8010/3010**, not 8000/3000, which [[jarvis]] and others already hold. Conservative
Sell ratings are expected output of the deliberately simple 5-year FCF model, not a bug.

Related research tooling: [[jarvis]] (voice-first, report-grade), [[endowment-advisor]]
(endowment/allocation), [[basel-analyzer]] (regulatory disclosure).
