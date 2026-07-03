---
title: J.A.R.V.I.S. — Mark VII voice assistant
type: project
tags: [voice-assistant, python, local]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/JARVIS]
---

A J.A.R.V.I.S.-style voice assistant ("Mark VII"): `index.html` front end + a **Python/Flask
backend** (`server.py`, port 3000) started with `start.sh`. The backend calls the
[[claude-anthropic]] API for the assistant brain and has **optional Gmail integration**
(Google OAuth, read-only scope). Config via `.env` (`ANTHROPIC_API_KEY`,
`GOOGLE_CLIENT_ID/SECRET`).

Per repo history (June 2026) it was **removed from web deployment and moved to local-only**
— access gating went through several iterations (API-key gate → access-code system →
two-mode personal-key/shared-code) and TTS pronunciation of "J.A.R.V.I.S." was fixed in
the local server version.

Part of [[files-repo]].
