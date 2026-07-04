---
title: J.A.R.V.I.S. — Mark VII voice assistant
type: project
tags: [voice-assistant, python, local, equity-research]
created: 2026-07-03
updated: 2026-07-04
sources: [~/files/JARVIS, https://github.com/tejasgjadhav/JARVIS]
---

A J.A.R.V.I.S.-style voice-first **institutional equity research terminal** ("Mark VII"):
front end in `public/` (`index.html`, `app.js`, `styles.css` — served as Flask static
files) + a **Python/Flask backend** (`server.py`, port 3000). Public repo:
`github.com/tejasgjadhav/JARVIS` (real `.env` key protected via `skip-worktree`; repo
carries a masked `xx` copy for replication). Config via `.env`.

**Desktop launch** (as of 2026-07): `launcher.py`, started by a `JARVIS.app` Desktop icon,
boots the Flask backend, waits for the port, then opens a chromeless Chrome "app window"
(its own `.chrome-app-profile/`) pointed at it. `start.sh` remains the manual path.

**Voice pipeline** (as of 2026-07-04): always-on browser speech recognition (`en-IN`) with
**"Jarvis" wake word** — mic ignores everything until "Jarvis" (fuzzy-matched against
common mishears), then opens a **15-second command window**; saying "Jarvis" while it
talks interrupts TTS. A watchdog force-restarts the recogniser if Chrome silently kills it.
Local **faster-whisper** (`small.en`, [[voicebox]]-adjacent) powers `/api/transcribe` for
accurate push-to-talk. TTS is a tuned British-male SpeechSynthesis voice; an original SVG
arc reactor (no copyrighted GIFs) flares gold when speaking, pulses blue when listening.

**Analysis pipeline** (the core, as of 2026-07-04): ANY company mention in chat/voice →
Sonnet-5 ticker extraction (Haiku fallback; rename aliases e.g. Zomato→Eternal,
TATAMOTORS→TMPV/TMCV via live `yf.Search`) → **yfinance live data** (price, statements,
FX-converted for dual-listed, historical revenue CAGR, technicals, analyst consensus,
named-broker actions from ADR listings) → **Opus 4.8 authors the institutional note**
(persona: Goldman MD presenting to a sovereign-wealth-fund IC). Non-vanilla drivers:
revenue growth **triangulated** (company CAGR / industry / consensus, blend shown in
sources), **EBIT margin as a 5-year path** (trajectory, not flat), WACC build (RF+β×ERP),
bull/base/bear **scenarios** with probabilities, **comps** forced to direct rivals
(Swiggy for Eternal), **SOTP** for conglomerates, and an explicit **divergence factor**
vs street consensus. Short-term (6–12 mo) phrasing routes to a **technical mode**
(RSI/DMAs/momentum/support-resistance/entry-target-stop, no DCF).

**Deliverables**: full analysis in chat (numbers → analysis → full DCF calc table with
actual FY labels e.g. FY27E–FY31E → recommendation last); auto-downloaded **13-sheet
formula-linked Excel** (Cover · Analysis · Key Metrics · Scorecard · Assumptions-with-
sources · Model · Consensus · Brokers · Sensitivity · Scenarios · Comps · SOTP ·
Football-Field-with-chart) + **institutional PDF** (DejaVu Unicode font so ₹ renders).
JARVIS **speaks only** the 2-line company intro + final recommendation.

**Python layer validates only** (user's rule): independent DCF recompute matches the
Excel formulas to 0.000% (heavy `formulas`-engine execution gated behind
`VALIDATE_FORMULAS=1`), plus a **data-recency gate** (latest/previous quarter else flag).
Model routing: `EXTRACT_MODEL` sonnet-5 · `REPORT_MODEL` opus-4-8 · `CHAT_MODEL` haiku.

Per repo history (June 2026) it was removed from web deployment and moved local-only.
Part of [[files-repo]]. Uses [[claude-anthropic]] and yfinance. See also [[voicebox]];
the institutional prompt patterns (assumption logs, sourced WACC, football field) came
from the user's "Claude AI for Finance Professionals" book ([[kdp-books]]).
