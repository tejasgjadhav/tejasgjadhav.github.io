# Wiki Log

Append-only. Entry format: `## [YYYY-MM-DD] ingest|query|lint | title`.
Last 5 entries: `grep "^## \[" log.md | tail -5`

## [2026-07-03] ingest | Wiki bootstrapped from Karpathy's LLM Wiki gist
Downloaded the pattern document to sources/llm-wiki.md, wrote the schema (CLAUDE.md),
and seeded 8 project pages by surveying ~/files: files-repo (hub), institutional-trader,
jarvis, dotnet-architect-book, kdp-dashboard, trade-regimes-website, scmhrd-ai-finance,
upstox-data. Created index.md and this log. Installed /wiki-ingest, /wiki-query,
/wiki-lint skills in ~/.claude/skills/.

## [2026-07-03] ingest | Trading strategies filed from institutional-trader docs
Read institutional-trader/CLAUDE.md and studies/ (CAPITAL_CURVE_RESULTS.md et al.).
Created pages/concepts/trading-strategies.md (4-strategy lineup + validation status) and
pages/concepts/capital-curve-verdict.md. Cross-linked from institutional-trader page;
index updated. Also broadened the wiki-query skill trigger to fire on project/strategy
questions, not just explicit "check my wiki" phrasing.

## [2026-07-03] ingest | Full sweep: entities, book catalog, enriched project pages, live graph
Deep pass over all current data. New pages: entities/tejas-jadhav, entities/upstox,
entities/netlify, entities/claude-anthropic, concepts/kdp-books (all 5 titles from
kdp-dashboard/data/books.json). Enriched jarvis (Flask + Anthropic + Gmail OAuth),
kdp-dashboard, files-repo, scmhrd-ai-finance, institutional-trader, upstox-data with
cross-links. Added tools/build_graph.py + generated graph.html (interactive link graph,
self-contained, dark-mode aware); schema and skills now regenerate it on every
ingest/lint, so the graph stays live as the wiki grows.

## [2026-07-03] ingest | Real-premium fade validation (bhavcopy 2019→Sep'24 + Upstox OOS)
Filed the session's real-data results from institutional-trader/studies/STOCK_OPTIONS_NO_EDGE.md
Parts 10–11. New pages: syntheses/real-data-fade-validation (the study) and entities/nse-bhavcopy
(the free real-premium source, back to 2019). Materially revised trading-strategies: STOCK fade
CONFIRMED durable on real data (+5.3% of width, 54% win, 5/6 yrs) but modest; INDEX fade DOWNGRADED
to regime-dependent (−1.4% real, and a direction+flush gate salvage that looked like +15.1%/78%
in-sample FAILED out-of-sample on Upstox Oct'24→date, reverted). Updated institutional-trader honest
status + upstox (expired-instruments endpoint / bhavcopy split). Added cross-links + the "6 positive
years in one regime ≠ out-of-sample" lesson. index.md updated; graph refreshed.

## [2026-07-03] ingest | Zerodha Kite entity page (setup only, no secrets)
Added entities/zerodha-kite documenting the Kite Connect setup: daily access-token auth flow,
instrument_token = exchange_token × 256, and the missing expired-instruments endpoint (why
[[nse-bhavcopy]] was used instead). Deliberately did NOT store the API key/secret/access-token in the
wiki — it's a git repo; secrets stay in the gitignored institutional-trader/.env. Cross-linked from
nse-bhavcopy; index + graph updated.

## [2026-07-04] ingest | Voicebox local AI voice studio installed
Cloned jamiepine/voicebox to ~/files/voicebox, full dev install verified (cloned-voice generation works).
Created pages/projects/voicebox.md (incl. 8GB-RAM → 0.6B model rule, dep pins, build patch); cross-linked files-repo and jarvis; index updated.

## [2026-07-04] ingest | BUY strategies tested on real Kite 5-min 2019→date
Filed institutional-trader/studies/BUY_STRATEGIES_2019_REALTEST.md. New page
syntheses/buy-strategies-real-2019: Zerodha Kite 5-min back to 2019 (the intraday data Upstox
couldn't reach) enabled the first all-regime test of the BUY strategies. 3-Family FULL-GATE (real
production code) = durable DIRECTION edge (50.6% hit, +0.107%/tr, +ve every year 2019→26) but −1%
net as option-buying; ORB+VWAP thin & inconsistent (+0.04%/tr, −ve ~2/8 yrs). Revised
trading-strategies (strategies 1 & 2) + zerodha-kite (now a key data source, not just a dead end);
index + graph updated.

## [2026-07-04] ingest | Project sweep: all pages brought current, graph refreshed
Swept every project dir under ~/files against its wiki page. Updated jarvis (public/ front
end, JARVIS.app → launcher.py chromeless-Chrome desktop launch, new report_engine.py —
yfinance→DCF→Excel/PDF equity reports with claude-opus-4-8 narrative + no-LLM fallback),
institutional-trader (OBJECTIVE_SPEC.md v1: return-on-capital under ≤15% DD replaces the
80%-WR/5%-mo ask; gated stock fade now DEPLOYED as paper forward test, 12 open positions),
and capital-curve-verdict (objective-spec cross-ref). Other 7 project pages verified
current, no changes needed. index.md summaries updated; graph rebuilt.

## [2026-07-04] ingest | JARVIS institutional pipeline + voice overhaul
Rewrote pages/projects/jarvis.md: wake-word voice ("Jarvis" + 15s window, watchdog, Whisper
STT), Opus-4.8 institutional analysis (triangulated growth, EBIT margin path, comps/SOTP/
scenarios/football-field), 13-sheet linked Excel + Unicode PDF, Python-validates-only rule,
public GitHub repo. Updated index entry; linked kdp-books.

## [2026-07-05] ingest | Scheduled sync: deploy-host correction, AIFINANCE, Google identity synthesis
Automated pass over the last 24h of Claude Code sessions. Fixed a real contradiction:
netlify.md/files-repo.md/scmhrd-ai-finance.md/tejas-jadhav.md all claimed Netlify hosts the
sites, but the repo remotes (tejasgjadhav.github.io, SCMHRD, AIFINANCE) confirm GitHub Pages
is the actual host — Netlify's role is the `claude` serverless function only. Corrected all
four pages. New page pages/projects/aifinance.md (landing page, own repo, a11y + SVG-icon
passes). New page pages/syntheses/google-identity-seo.md (canonical-portrait rule across
root/SCMHRD/AIFINANCE, shared Person schema @id, open Knowledge Panel path via Wikidata).
Added institutional-trader Telegram/WhatsApp alerts + STRATEGY_SUMMARY.md canonical-doc
note. Added dotnet-architect-book's WeasyPrint→Chrome-headless PDF fallback. Added
scmhrd-ai-finance's teaching-deck gotcha (hand-edited .pptx is now source of truth, not the
generator script). index.md + graph updated.

## [2026-07-04] ingest | Stock fade v2 (TP-50) deployed — the new leader
Grid+OOS-validated upgrade (short 2-OTM/width4/TP50%/stop3x): 85.35% win +24.5% width in-sample,
87.88% +31.9% OOS, >=79% win all 8 yrs. Deployed parallel to v1 at 1 lot; ORB+VWAP retired.
Updated trading-strategies (new 1b section) + index. Model vs practical P&L documented in repo study.

## [2026-07-06] ingest | scheduled sync — basel-analyzer + SENSEX Thursday 0DTE
Automated memory/wiki sync from recent sessions. NEW project page basel-analyzer
(deterministic-first Basel III/Pillar 3 analyzer, Ollama gpt-oss-120b + OpenRouter,
Refinitiv/LSEG, 9-agent graceful-degrade pipeline; local-only repo). Added §5 to
trading-strategies: NIFTY Tuesday 0DTE call-spread (deployed, pre-market rv5 checker) +
SENSEX Thursday 0DTE second-payday research (88.8% win, 89 weeklies, not yet deployed).
Indexed both; bumped trading-strategies updated date.

## [2026-07-07] ingest | 0DTE deployed + SENSEX/BANKNIFTY rollout
Session 9e3c4735 continued past the 2026-07-06 sync. Updated trading-strategies §5:
NIFTY Tuesday 0DTE CE-spread now FULLY deployed (pre-market status strip, banner, 5-line
rules card, 2-leg swing-table format on INTRADAY DECISIONS + new TRADE LOG section; commits
e0a4e9b/e69f827; first live paper entry 2026-07-07 09:16). Added rollout plan: 4 PM routine
installs SENSEX Thursday + (if it validates) BANKNIFTY 0DTE in the same format; consolidated
monthly-PnL view across the live lineup. Bumped updated date; refreshed index.
