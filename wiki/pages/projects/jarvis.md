---
title: J.A.R.V.I.S. — Mark VII voice assistant
type: project
tags: [voice-assistant, python, local, equity-research]
created: 2026-07-03
updated: 2026-08-09
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

**Max-subscription backend** (as of 2026-07-27): a `claude_cli.py` shim shells out to the
local `claude` CLI instead of the SDK, so calls bill the Max subscription rather than API
credits (`CLAUDE_BACKEND=cli`). Measured 2026-08-08, that costs latency: ~6s of spawn
overhead for a trivial reply, 10–15s for a chat turn (two calls — ticker extraction, then
the answer). The API path streamed in 1–2s. The trade is deliberate; speed for money.

**Valuation discipline** (as of 2026-08-08): the DCF is a **pure DCF**. A 2026-08-07 pass
found the terminal value was growing year-5 free cash flow forever, locking growth-phase
capex and a mid-ramp margin into the perpetuity — Reliance came out at ₹446 against a
₹1,335 price. Fixed with normalized steady-state economics (terminal NOPAT from a
steady-state margin, reinvestment = g ÷ terminal ROIC, per Damodaran), exposed as two
editable assumptions. Reliance moved to ₹631. The standing rule is that only *methodology*
errors get fixed — no input is ever tuned to close the gap to market price. Following from
that, the old "coherence gate" (which hid the DCF and led with the analyst target whenever
the DCF fell outside 0.5–2× of price) was **removed on 2026-08-08**: chat, the written
recommendation and the spoken verdict now all lead with the DCF intrinsic value, and the
analyst target is a one-line reference.

**Two bugs worth remembering** (2026-08-08): the spoken conclusion was being dropped
because `speak()` truncated the summary at 900 characters *before* splitting it into
sentences, and the verdict is always the last sentence — fixed by splitting first and by
moving the conclusion to second position so it survives a barge-in. Separately, the
short-term "technical mode" router matched bare *trade/trading*, so an ordinary question
like "what is Swiggy trading at" returned a thin technical note instead of the full model;
only explicit short-horizon intent triggers it now.

Per repo history (June 2026) it was removed from web deployment and moved local-only.
Part of [[files-repo]]. Uses [[claude-anthropic]] and yfinance. See also [[voicebox]];
the institutional prompt patterns (assumption logs, sourced WACC, football field) came
from the user's "Claude AI for Finance Professionals" book ([[kdp-books]]).
