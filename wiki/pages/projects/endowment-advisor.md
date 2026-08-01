---
title: Endowment Advisor — multi-agent endowment chatbot
type: project
tags: [endowment, agents, fastapi, pptx, advisory]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/endowment-advisor/README.md]
---

Local-first multi-agent chatbot at `~/files/endowment-advisor` for analysing and comparing
university endowment funds, discussing portfolio construction and valuation, and generating
a pitch deck from the conversation.

- Frontend: vanilla HTML/CSS/JS chat UI with an Advisory / Analyze / Compare mode selector
  and a **Generate Deck** button, served by FastAPI, no build step.
- Backend: FastAPI — `/chat`, `/deck`, `/health`. Needs an [[claude-anthropic]] key in
  `backend/.env`; runs against LSEG mock data otherwise.
- Agents, each a separately system-prompted API call with prompts in `backend/prompts/`
  loaded at runtime: **Orchestrator** (routes by mode, synthesises the answer), **Research**
  (news/fundamentals via function-calling tools), **Valuation** (bond, FX, fundamentals and
  historical-pricing tools), **Deck-Builder** (conversation → slide outline → downloadable
  .pptx, generated locally).
- State is an in-memory per-session dict — restarting the server drops history.

The README carries an explicit disclaimer that the tool gives no licensed investment
advice. That is deliberate and matches the constraint on [[ninja]] and the books: as a
CFA/FRM charterholder, [[tejas-jadhav]] cannot ship anything that reads as personalized
advice.

Sits alongside the other research systems: [[jarvis]], [[in-eq]], [[basel-analyzer]].
