---
title: J.A.R.V.I.S. — Mark VII voice assistant
type: project
tags: [voice-assistant, python, local]
created: 2026-07-03
updated: 2026-07-04
sources: [~/files/JARVIS]
---

A J.A.R.V.I.S.-style voice assistant ("Mark VII"): front end in `public/` (`index.html`,
`app.js`, `styles.css` — served as Flask static files) + a **Python/Flask backend**
(`server.py`, port 3000). The backend calls the [[claude-anthropic]] API for the assistant
brain and has **optional Gmail integration** (Google OAuth, read-only scope). Config via
`.env` (`ANTHROPIC_API_KEY`, `GOOGLE_CLIENT_ID/SECRET`).

**Desktop launch** (as of 2026-07): `launcher.py`, started by a `JARVIS.app` Desktop icon,
boots the Flask backend, waits for the port, then opens a chromeless Chrome "app window"
(its own `.chrome-app-profile/`) pointed at it; quitting JARVIS from the Dock tears the
server down. `start.sh` remains the manual path.

**Equity Report Engine** (`report_engine.py`, added 2026-07): chat-triggered institutional
equity reports — yfinance real market data → factor analysis + DCF in pure Python →
Excel financial model (openpyxl) + institutional PDF (reportlab), delivered as download
URLs. Deterministic core works offline; the server routes models to save tokens (cheap
model for chat, `REPORT_MODEL` claude-opus-4-8 for report narrative, with graceful
fallback to the no-LLM deterministic report).

Per repo history (June 2026) it was **removed from web deployment and moved to local-only**
— access gating went through several iterations (API-key gate → access-code system →
two-mode personal-key/shared-code) and TTS pronunciation of "J.A.R.V.I.S." was fixed in
the local server version.

Part of [[files-repo]]. See also [[voicebox]] — a local voice studio (cloning/TTS/STT)
that could replace cloud TTS for local voice projects like this one.
