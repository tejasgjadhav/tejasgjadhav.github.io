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

## [2026-07-08] ingest | 0DTE calm-filter + fade dedup + Google entity de-merge
Scheduled memory/wiki sync from sessions 9e3c4735 (institutional-trader) and daae2bc8 (identity).
trading-strategies §5: quantified the 0DTE NIFTY calm-filter now DEPLOYED — skip week when rv5 ≥
0.9% (win 85.0→87.8%, avg +3.2→+4.0%/margin, 2025 +₹1.7k→+₹23.2k, commit 91a6330); added the
rejected 90% VWAP-flush stock-intraday idea (net −0.095%/trade, win-rate manufactured by exit
geometry). trading-strategies §1b: stock fade v1/v2 cross-book dedup (one position/stock, v2 always
wins, v2 scans first; phantom-strike guard; commit 334dac1). google-identity-seo: the "many tejas
jadhav now" appearance is Google's entity DE-MERGE working, not a regression; qualified "tejas jadhav
books" query already shows the correct photo; re-confirmed no claimable Knowledge Panel exists.
Bumped updated dates; refreshed index.

## [2026-07-14] ingest | scheduled sync — 0DTE entry-time verdict, non-fade falsification, monthly long-call shelved, Telegram live, KDP books
From recent sessions (d62dc509, fdd1caa2, c6185cc3, 65910cfe). trading-strategies: added
§5 0DTE entry-time sweep verdict (09:16 open stays — later entry buys ~3–4pp win% but gives
up 35–45% of profit, edge is opening theta/IV crush; ZERO_DTE_ENTRY_TIME.md); new §6 monthly
futures REV1-v2 + its long-CALL expression SHELVED 2026-07-14 (MONTHLY_CALL_ENABLED=False; ¾ of
the 12-mo P&L was one POLYCAB gap); cross-cutting lesson that no non-fade intraday edge is in
reach (long straddle/gamma/debit verticals lose both eras). institutional-trader: Telegram alerts
now LIVE (@Algotejasbot → "Algo Trader by Tejas", all 8 sources, _tg fan-out). kdp-books: "Claude
AI for Finance Professionals" re-counted to 17ch/135+ prompts, added "Claude Cowork for Finance"
(11 caps + capstone + limits, 112pp), hardcover live-text-layer cover gotcha. Bumped updated dates;
refreshed index.

## [2026-07-14] ingest | algo-trading book page + global-first reorientation
Scheduled sync from recent sessions. New page pages/projects/claude-algo-trading-book.md
for the "Claude for Algo Trading" book (built off institutional-trader): pipeline, real
GitHub+Qt screenshots, CFA no-advice voice, and the 2026-07-14 global-first reorientation
(India→US translation table, inline glosses, README re-captured at 235 commits). Indexed.
Monthly long-call SHELVED and 0DTE NIFTY facts already recorded in the prior run — no
trading-page change needed. (Job daily-application routine at 9:35 AM filed to memory only —
no wiki home.)

## [2026-07-15] ingest | scheduled sync — Wikidata/ORCID identity build, SEO weekly, Telegram 7-not-8, watchlist 3:05 PM
From recent sessions (daae2bc8 photo/Wikidata, c4726db8 SEO reschedule, d62dc509 trader).
google-identity-seo: priority-1 lever DONE — Wikidata item Q140561693 created + built to 16
properties/23 statements incl. P18 image (Commons upload) and first independent source (P463
member-of CFA Institute cited to Mint 2026-02-02 p.13); ORCID 0009-0000-9407-6871 created and
two-way cross-linked (P496 + sameAs on all 3 sites); résumé fact corrections (Pune / Univ of Pune
/ MMS, WorldQuant removed as P69); seo-rank-monitor rescheduled daily→WEEKLY (Mondays ~08:01) and
upgraded to active safe-fix improver; ranking IMPROVED (qualified queries fully owned, bare-name
#1 AI Overview bullet, entity-thumbnail recrawl pending). tejas-jadhav: added Wikidata + ORCID
identifiers. institutional-trader: Telegram effective coverage corrected to 7 live books (3-Family
SCAN_3FAMILY_ENABLED=False + rejected, never fires); watchlist UI discipline — union_watchlist.json
builds 3:05 PM, on-demand scans stay terminal-only. Bumped updated dates; refreshed index.
(Job-search Naukri-now-works correction filed to memory only — no wiki home, per prior runs.)

## [2026-07-16] ingest | trader portfolio reframe + c/w-gate finding; algo book cover badge
From recent sessions. institutional-trader: reframed as a 6-book multi-strategy portfolio
(3-Family retired, README 5290cd5); watchlist consolidated to one daily 3:05 PM build (bd485a6,
removed 15-min sweep); 0DTE result Telegram moved to ~15:35 (a1251c3, watcher runs after settlement);
full Telegram cadence 9:16/15:05/15:10/15:35. trading-strategies: v2 UNION kept over D10-only (0b1e37d,
superset, +34% signals same win rate; CALL side stronger 88%/+38.7%); c/w-gate two-tier finding
(CW_BUCKET_ANALYSIS.md, 36b0cc1) — c/w≥0.40 IS the edge, below-gate money collapses ~10× at ~77% win,
0.35–0.40 band deferred pending 2019–24 validation. claude-algo-trading-book: cover GitHub badge +
Amazon platform-name-not-URL rule. Touched institutional-trader, trading-strategies,
claude-algo-trading-book pages; bumped updated dates; refreshed index.

## [2026-07-20] ingest | scheduled sync — watchlist-preview, UNION=D5, BSR/launchd+honesty, Amazon Ads, cover gotchas
From recent sessions. institutional-trader: watchlist "PASS" is a live PREVIEW snapshot — only the
~15:10 scan is binding (OFSS boundary-hugger flickered PASS but correctly didn't fire); UNION scanner
= D5 exactly (Donchian D5/D10/D15/D20 study — D10/15/20 are a subset of D5, scanner checks D5 first);
live bug sweep 5a7a18b (0DTE settlement fabrication in zero_dte.py/dte_multi.py via `spot ... or 0` →
fake WINs; "M&M" `&` broke Telegram HTML mode + marked-seen-before-send → alerts lost forever → rule:
HTML-escape fields + mark seen only after send; monthly_fut expiry now MOC close); watchlist timing →
build 14:45 / send 15:05 (01dc6d3, 6c20f32). trading-strategies: 0.35–0.40 c/w ~82% win is conditional
on the TP-50 exit, lower held-to-expiry. kdp-dashboard: scraper moved off GitHub Actions to local
launchd + Playwright headless Chrome (Amazon blocks curl_cffi/CI since ~Jul 17); honesty-first UI shows
real rank age + stale flags (917f7a1); catalog now 8 books incl Spanish+German editions. NEW page
amazon-ads: Sponsored Products for the flagship book — underspend from bids too low (don't cut bids to
fix ACOS), India account-balance throttle watch-item. kdp-books: added spine-on-fold + back-byline-vs-
barcode + exact-per-binding-dimension cover gotchas. New pages: amazon-ads. Touched institutional-trader,
trading-strategies, kdp-dashboard, kdp-books; bumped updated dates; refreshed index. Memory: new
amazon-ads-campaign + kdp-cover-gotchas, updated bsr-dashboard + institutional-trader-status.

## [2026-07-23] ingest | Telegram portfolio summary + Saavi branding, data ceiling, BA occupation, interview prep
institutional-trader: per-trade running portfolio summary on Telegram (_portfolio_summary_text, closed
W/L/win%/realized P&L + open count across 6 books) with user-chosen "Tejas's Saavi Institutional Trader"
branding (honesty caveat: paper/forward-test, "delivered for live trade" overstates); intraday
option-premium data ceiling = only Oct'24→now ~2yr real intraday (bhavcopy daily-close 2019→Sep'24, none
pre-2019) so hourly-c/w backtests cap at ~2yr; stock credit scans once/day at 15:10 (no hourly loop),
close-gate intentional; queued validation-only job "hourly-touch vs close-gate 0.40" → HOURLY_VS_CLOSE_ENTRY.md.
tejas-jadhav / google-identity-seo: 2026-07-23 monitor GREEN, AI Overview on-message + #1 organic, but
mobile entity slot hijacked by a Google Maps "place" entity; role audit — "business analyst" (Q1017553)
missing from Wikidata P106, plan to add (safe off-page), not yet applied; actively interviewing for
capital-markets BA/PO roles incl. UBS Corporate Actions PO. Touched projects/institutional-trader,
entities/tejas-jadhav, syntheses/google-identity-seo; bumped updated dates; refreshed index. Memory:
new interview-prep-assets, updated institutional-trader-status + google-photo-identity-fix + MEMORY.md.

## [2026-08-01] ingest | catch-up sync — 8 new project pages + KDP listing operations
Wiki had drifted since 2026-07-23. Added pages/projects/{vt-ocs, in-eq, ninja,
endowment-advisor, clearframe-studio, kalpana, globalaar-ops, claude-code-finance-book}
and pages/concepts/kdp-listing-operations. Updated files-repo (project list),
kdp-books (new titles + cover-claim compliance rule), index.md, graph.html.
Note: index.md was found overwritten in the working tree with free-text book notes;
restored from git and the notes handed back to the user separately.

## [2026-08-09] ingest | scheduled sync — JARVIS DCF purity + speech bugs, Module 1 shipped, memory-layers concept
Swept sessions from 2026-08-07/08. New page: concepts/ai-memory-layers (four-layer memory model +
link graph). Updated projects/jarvis (Max-CLI latency measured, terminal-value normalization,
coherence gate removed → DCF-first, 900-char speech truncation and trade/trading router bugs) and
projects/aifinance (ISBMS course site, Module 1 as delivered, Colab dropped for a Codex lab).
index.md entries refreshed for both.

## [2026-08-09] ingest | scheduled sync — memory durability layer; permissions now config, not manual
Second sweep of the day (an earlier run at 06:47 already filed JARVIS DCF/speech, ISBMS Module 1
and the ai-memory-layers concept — not repeated here). Sessions reviewed: memory-vault recovery,
Chrome-extension profiles, JARVIS mic/Swiggy routing, HDMI projector, M&M Q1 FY27 summary.
Only genuinely new material was filed. concepts/ai-memory-layers gained a durability section:
the layers are worthless unless each is backed up on a schedule, and the published layer (this
wiki) must never carry content from the private auto-memory layer. Everything else from those
sessions was already recorded — mic recovery and the projector Extended-display fix landed in
memory earlier today, and the FinBERT character-limit lesson was filed on 2026-08-08.
Deliberately NOT published: the Google Sheet credential from the ISBMS session, and the local
permission-mode configuration — both are machine/private facts, memory-only.
Memory: updated always-bypass-permissions-mode (bypass is now set in ~/.claude/settings.json via
defaultMode + skipDangerousModePermissionPrompt, so scheduled routines no longer stall on
prompts — the old "Claude cannot set this" note was stale), new chrome-extension-profiles, and
restored the missing four-layers-of-memory pointer in MEMORY.md.

## [2026-08-09] ingest | scheduled sync — Wikidata item deleted, gitlinks froze the Pages build, company-finance-app
Third sweep of the day; the 06:47 and 10:10 runs are not repeated here. Sessions reviewed: the
global remote-job drive, the Naukri drive, the Google-photo escalation, and today's commits.
Filed: **Wikidata Q140561693 was deleted 2026-08-08** for failing notability — the priority-1
Knowledge-Panel lever from 2026-07-15 is gone along with its P18 portrait, and the dead sameAs was
removed from index.html (25acf88); he reported the wrong photo again the same day. Also filed the
**gitlink breakage**: 12 sub-repos committed as mode-160000 entries broke the GitHub Pages build,
freezing the live site on its 2026-08-02 deploy until 486dc75 untracked them. New page:
projects/company-finance-app (Flask + yfinance lookup). Touched syntheses/google-identity-seo,
entities/tejas-jadhav, projects/files-repo; bumped updated dates; index.md refreshed.
Deliberately NOT published: the whole job-search layer — accepted-offer comp, the 38 LPA / USD 60k
quoting rule, and the application queue are private-memory facts and this wiki is public.
Memory: new files-repo-gitlinks-pages + company-finance-app, updated google-photo-identity-fix and
usd-remote-job-search (accepted Accenture offer joining 7 Sep 2026, no-Mumbai, salary rule, 29 applied).

## [2026-08-10] ingest | scheduled sync — v0 credit book, Turtle Soup rejected, the voice pass becomes a gate
Reviewed the sessions from the last 24 hours: the Saavi low-c/w work, the Cowork book review and
rebuild, the humanizer-versus-voice-pass comparison, the Instagram-reel strategy backtest, and the
remote-job drive. New pages: syntheses/turtle-soup-verdict (the reel's EA is Raschke and Connors'
Turtle Soup; 54,189 setups across NSE indices, 54 stocks and MCX say it is a coin flip after costs,
the 80% win-rate zone needs 46.7 points of edge, and one 90.77% result was a lookahead bug) and
concepts/voice-pass (the sentence-level grammar gate, the fragment ban beating the aphorism ban,
the humanizer skill demoted to structure, and the US-default audience). Updated
projects/institutional-trader (the v0 book on 0.35–0.40, the cross-book 3-day re-entry gap, the
15:15–15:40 deployment freeze, scan moved to 15:36, bhavcopy verification at 33 of 34 exact),
concepts/trading-strategies (0.30–0.35 is dead in all 432 configs; the win-rate arithmetic) and
concepts/kdp-books (Cowork v9 shipped for internal consistency, ten aphorisms restored, page counts
held). Bumped updated dates and refreshed index.md.
Deliberately NOT published: the job-search layer stays private-memory only — this wiki is public.
Memory: new turtle-soup-strategy-verdict and book-audience-us-default; updated
institutional-trader-status, kdp-finance-book-series, humanizer-skill-location and
usd-remote-job-search (the silent-no-op submit means throttling, and Lever needs its /thanks
confirmation).

## [2026-08-11] ingest | scheduled sync — the cover pipeline, index-price sources, and a claims audit
Reviewed 15 transcripts from the last 24 hours, including the cover worktree, the Saavi engine
session, the SEO and schema session, and the job-search runs. New page: concepts/book-covers — the
three-agent pipeline (designer writes a spec, executor builds and pixel-verifies it, compliance gate
is the only reviewer that can block), the click test at a phone thumbnail, outcomes on the front and
counts on the back, the ranking Claude register copied without Anthropic's mark, and KDP's
calculator as the only authority on hardcover dimensions. Updated concepts/kdp-books (cover J ships
for the Cowork book, palette nudged off Anthropic's published values, 114/120pp unchanged),
projects/institutional-trader (an index close is verified against NSE's index file because the CM
bhavcopy is equities only; the swing book has been off since 2026-07-24; the Telegram wording spec;
a rising credit/width can be intrinsic rather than time value and that kills the entry),
syntheses/google-identity-seo (the Mint feature claim and the "#1 Bestseller in India" wording were
audited off as unsupported, and the category ranks went back scoped and linked to the BSR audit) and
projects/kdp-dashboard (that audit is now the evidence behind the site's rank claims: 8 books, 20
formats, 17 countries, 85 live rankings, best category rank #5). index.md refreshed for all five.
Deliberately NOT published: the whole job-search layer, including application counts, salary
figures and the LinkedIn and Naukri throttling mechanics. This wiki is public and those are
private-memory facts.
Memory: new author-site-claim-accuracy; updated institutional-trader-status, kdp-finance-book-series,
kdp-cover-gotchas, usd-remote-job-search and naukri-bulk-apply-routine.
Correction worth keeping: he discussed raising the stock-credit exposure cap to Rs60,000 on
2026-08-11 and the config was not changed — STOCK_CREDIT_MAX_EXPOSURE is still 0, no cap.

## [2026-08-13] ingest | Session sync — T-1 closed, the August sales slide, and the beginners book draft
Swept the day's transcripts. Trading: appended the T-1 rejection, the expiry-cadence lesson and the
entry-time finding to institutional-trader and trading-strategies, and recorded that the ₹60,000
exposure cap has been asked for twice while the config still reads 0. KDP: filed the two-phase BSR
diagnosis of the August royalty slide on amazon-ads, and the Amazon-autocomplete keyword method plus
the KDP save mechanics on kdp-listing-operations. New pages: projects/claude-beginners-book (full
75-chapter draft, 243pp) and syntheses/job-search-book-verdict. kdp-books links both. Index updated,
graph regenerated.

## [2026-08-16] ingest | Session sync — the corporate-action bug, the translated editions, and a cover trade-dress call
Swept six transcripts from the last 24 hours. Trading: filed the corporate-action scale mismatch on
institutional-trader — adjusted Upstox closes against unadjusted bhavcopy strikes fabricated
full-credit wins across the whole history of the study, the fix derives spot by put-call parity,
and the result reverses the leadership to v1. Also recorded that a bootstrap then showed all three
books' confidence intervals contain zero, that the TP sweep refuted the idea of cutting the target
to force a positive net, that a parameter whose slope inverts between windows is noise, and that
the harness now models the live one-open-position-per-symbol rule which had been counting 59% of
in-sample trades the engine could never have taken. Nothing was deployed and every published number
is still pre-parity. trading-strategies carries the one-paragraph version.
KDP: new page projects/claude-finance-translations for the German and Spanish editions — 128
prompts and 18 chapters in both, the 14-page gap traced to the Microsoft walkthrough the Spanish
book lacks and confirmed independently by the Excel count, the d1 cover shipped for all three
editions, and the ebook cover built native at 1.6 rather than cropped from the 1.5 print front.
book-covers gained two sections: the trade-dress call (a rights complaint suspends a listing
without a court, so separate on the competitor's distinctive devices and keep the functional ones,
and scan supplied artwork for lookalike marks) and the mechanics of building from supplied artwork
(report effective DPI first, check the back panel by eye, render a large canvas in bands and prove
the seams three ways). claude-beginners-book records its cover round. kdp-books links the new page.
Memory: new kdp-finance-translations and cover-trade-dress-risk; updated institutional-trader-status,
claude-beginners-book and dev-machine-technical-gotchas.
Deliberately NOT published: the job-search transcript layer — CV content, target employers,
salary figures and application mechanics. This wiki is public and those stay in private memory.

## [2026-08-17] ingest | Session sync — the OI gate conceded, the frozen stop, and the hardcover that has no formula
Swept nine transcripts from the last 24 hours. Trading: institutional-trader gained the 17-Aug
section — he challenged the open-interest gate and won the argument, so it is recorded as a fidelity
fix rather than an edge, since no threshold above zero has ever been tested for win rate or return
and the live bid-ask check blocks everything it blocks. The bigger finding is the ceiling: the live
spread gate rejected 10 of 17 candidates that day and no bhavcopy backtest can model it, because
those files carry no bid or ask at all, so the harness is scored 7/10 against a maximum near 8 and
the forward record is the only route past it. Also filed: a live position carried a stop for
nineteen days after the books stopped using stops, because stop_cost is frozen into the record at
entry and nothing re-reads config; the engine read a DNS failure as an exchange holiday and lost the
15:17 watchlist, with the fix now reading its own database first and never caching a negative; the
settlement path had no date guard and fell through to the current live price; research inputs moved
out of /tmp after it was wiped twice; and two mermaid diagrams now sit in the README.
trading-strategies and backtest-harness-audit-rule carry the one-paragraph versions, the latter
gaining the general rule to name the gate your data cannot model and to audit any parameter frozen
at entry.
KDP: book-covers gained the hardcover correction — the inch spine formula in CLAUDE.md was wrong and
is withdrawn, because KDP's hardcover geometry is metric and the sheet must be built to the size KDP
itself states; plus JPG is accepted for the Kindle cover only, and a halftone must never be built by
cropping the finished front artwork. kdp-listing-operations gained the live policy changes (the 70%
band is now $2.99-$12.99, categories are three per format, four filed URLs are dead), the EPUB
delivery-fee arithmetic, and the keyword method: run a nonsense-string control before believing
autocomplete, probe compounds exactly as pasted, and treat Kindle and print as one corpus.
claude-beginners-book records cover v7, the rebuilt EPUB and two false back-cover claims corrected.
Memory: new tradingview-delayed-feeds; updated institutional-trader-status, claude-beginners-book,
kdp-cover-gotchas, kdp-publish-workflow, kdp-keyword-mistake-lessons, dev-machine-technical-gotchas,
runtime-verification-rule, resume-align-never-fabricate, usd-remote-job-search and
naukri-bulk-apply-routine.
Also corrected outside the wiki: the withdrawn hardcover spine formula in both copies of CLAUDE.md.
Deliberately NOT published: the job-search layer — application totals, the LinkedIn one-per-day cap
and the ATS mechanics, the CLO CV work, and the SEO identity monitoring. This wiki is public and
those stay in private memory.

## [2026-08-20] ingest | Session sync — the tenor sweep, and what a data source cannot show you
Minimum time-to-expiry was measured for the first time on the stock credit books and it splits them:
v2 and v0 are best at the deployed ten days, v1 is better at five in both in-sample cuts, and three
days is worse than five everywhere. Nothing was deployed, because the out-of-sample sweep had not
finished. institutional-trader and trading-strategies carry the numbers.
The finding underneath it is a data-source rule and it is filed on backtest-harness-audit-rule:
the exchange bhavcopy publishes a settlement close for every LISTED contract rather than only those
that traded, so it prices unfillable strikes and flatters any result that depends on thinness, while
the broker's expired-contract candles exist only where a trade happened and enforce the constraint
physically. nse-bhavcopy carried the wrong claim since July and is corrected in place with the
contradiction noted; upstox gained the matching section.
Also filed on institutional-trader: HDFCBANK fell hard and correctly produced no trade, because a
forty-point spread on a ₹720 stock cannot pay ₹50 of premium, which excludes cheap names
structurally; three parts of the interface reported three different signal rates and now all derive
from the one measured figure; and a message now goes out at 15:36 on empty days, so silence is a
fault signal rather than an ambiguity.
Memory: updated institutional-trader-status, backtest-harness-audit-rule,
dev-machine-technical-gotchas, job-search-answer-sheet and usd-remote-job-search.
Deliberately NOT published: the job-search layer (the salary figure was corrected to ₹37 LPA fixed
in private memory only), the Accenture background-check paperwork, and the SEO identity work.

## [2026-08-21] ingest | Session sync — the tenor verdict reversed, and six defects in the harness of record
The out-of-sample sweep answered the one question the tenor study left open, and it went against the
in-sample case. v1 looked better at a five-day floor in both in-sample cuts, and out-of-sample ten
days won every column, so the deployed floor stays at ten on all three stock credit books.
institutional-trader and trading-strategies both carry the reversal, and the paragraph that said the
sweep was still running is corrected in place.
The harness that produces the published numbers was then audited and gave up six defects. The worst
made a network failure indistinguishable from a contract that never traded, which made the harness
non-deterministic and means every out-of-sample figure the project has published came from that
code. A second defect let open interest leak between books, so 88% of v1 rows recorded another
book's contract, which inverted the shape of the open-interest table and changed the argument for
the deployed gate without changing the gate. The in-sample re-run came back identical, which is the
regression check the audit needed.
The re-run of the out-of-sample window then crashed on a cache that three research scripts share and
disagree about, with 17% of its entries in the wrong shape. The published out-of-sample figures are
therefore still the pre-fix ones. backtest-harness-audit-rule gained four general rules from all of
this: a failed fetch must never look like a genuine absence, audit the script of record rather than
the copy you run, a shared cache needs a version tag and an atomic write, and a window that has
answered five questions is spent evidence.
Also filed on institutional-trader: BANKNIFTY was deleted from the intraday code rather than left
behind a disabled flag, each intraday book now states why it stood down on the morning scan tick,
and a notification helper's return value was discarded by every caller, so a rotated token would
have ended every message permanently and silently.
Memory: updated institutional-trader-status and backtest-harness-audit-rule.
Deliberately NOT published: the job-search layer, which is what the other sessions in this window
were doing — the Naukri bulk-apply and profile-refresh runs, the daily remote applications and the
SEO identity monitor. Those stay in private memory and their own handoff files.

## [2026-08-23] ingest | Session sync — the 103 outsiders, a counter that could not see the loss, and a prospectus made queryable
The routine's 2026-08-22 run died mid-response when the machine slept, so this sync covers the two
days it missed as well as today.
On [[institutional-trader]], a name-by-name study of every F&O stock the system does not trade
started and its in-sample half finished. His premise held: NSE carries 208 stock underlyings, the
traded universe holds 113, and the name he said was missed is genuinely one of the 103 outsiders and
genuinely the best of them. Two findings temper it. Only 24 of the 103 produce a single trade in
almost six years, because the premium floor and the credit gate reject the rest, so most outsiders
are outside for a structural reason. And in the band where every live fill sits, the outsiders win
60.5% against the insiders' 78.8%, so the block would dilute the strongest book even though its
full-band numbers look good.
The same run exposed a gap worth more than the study. A DNS outage skipped 85 of the 103 symbols at
the underlying-fetch stage, which sits above the fetch-integrity counter, so the run reported itself
clean while measuring eighteen names. [[backtest-harness-audit-rule]] now carries the general rule:
an integrity counter proves nothing about the stages it does not watch. Two working practices are
filed beside it — a study should import the harness of record and override only its inputs, and a
long research run should yield to the live engine through a detached guard during the entry and scan
windows.
Also on that page: the project has cost roughly 120 hours over 68 days, measured from 496 commits,
with 78 hours the floor that commits alone defend.
[[shiprocket-dhrp-rag]] is a new page. He asked for a retrieval system over Shiprocket's 543-page
SEBI prospectus, step by step, because he teaches the build. LlamaIndex splits and embeds it,
ChromaDB holds 885 chunks, and the Codex tool writes page-cited answers, with no API key anywhere —
which is the constraint that matters, because his students have no paid subscriptions. It sits on a
worktree branch rather than on main.
[[aifinance]] gained Module 2, which is Prompt Engineering and RAG in twelve slides, with the
hallucination slide rebuilt around the question Bard actually answered wrong and a new slide
explaining what RAG is before the pipeline appears. Two production notes came with it: his edited
copy in Downloads becomes the source of truth, and Keynote silently refuses a deck that python-pptx
wrote speaker notes into.
[[amazon-ads]] gained a second campaign, two dollars a day for the beginners book, launched with all
ten keywords at the account floor. Its own arithmetic says the floor bid sits slightly above
break-even, so it buys velocity rather than profit. One reusable interface trap is recorded: per-row
bid edits in the campaign builder silently revert to the enter-list bid.
Memory: updated institutional-trader-status, backtest-harness-audit-rule, isbms-ai-finance-course,
dev-machine-technical-gotchas, amazon-ads-campaign, naukri-apply-mechanics, usd-remote-job-search and
seo-browser-profile-split; added shiprocket-dhrp-rag and home-network-wifi.
Deliberately NOT published: the job-search layer, which produced the day's largest finding — an Apply
button that looks dead is almost always a stale screenshot scale — along with the SEO identity work,
where the useful result is that a Google AI Overview is not personalised, and his home network
diagnosis. All three stay in private memory.

## [2026-08-24] ingest | The outsiders answered out of sample, and the best in-sample name did not confirm
Follow-up sync, same day, after the expansion study finished its out-of-sample leg overnight.
The result corrects what was filed yesterday. PAGEIND led the in-sample table at 24 trades and 88%
wins, and out of sample it managed six trades at 67%. That is a pass, not a confirmation, so the
in-sample figure no longer travels on its own. Both [[institutional-trader]] and the wiki index now
say so in place rather than quietly dropping the earlier claim.
Getting the number took three attempts, and the second failure is the useful part. The DNS outage
that ruined the first run turned out to be recurring and local, and the retry lost 79 symbols and 163
legs, measured nine names out of 103, and reported itself complete. A failure that reports success is
invisible to an exit code. [[backtest-harness-audit-rule]] now carries the fix as a general rule: run
the walk repeatedly behind a network gate, let the cache fatten so each pass refetches only what the
last one missed, and publish nothing until a pass finishes with no failures and no drops. Drop counts
converged 1,288 to 462 to clean under that loop.
Pooled, the outsiders returned 204 trades at 78.4% wins and +14.6% on margin. Six names had enough
in-sample history to judge and none confirmed decisively. The strongest names — TVSMOTOR, LTM and
four others — were names the in-sample window never saw at all, so the case for expansion now rests
on weaker evidence than the study intended to produce, and it says so. Nine candidates model at four
to ten and a half thousand rupees a month, a quarter to a half above the current stock books.
Nothing has been put into the configuration and no name has been admitted.
Memory: updated institutional-trader-status and backtest-harness-audit-rule.
