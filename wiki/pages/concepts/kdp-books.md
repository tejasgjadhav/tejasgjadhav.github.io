---
title: KDP book catalog — AI and Practical Finance Series
type: concept
tags: [kdp, books, writing, amazon]
created: 2026-07-03
updated: 2026-08-16
sources: [~/files/kdp-dashboard/data/books.json]
---

[[tejas-jadhav]]'s published KDP titles (author credentials: CFA, FRM), most in the
**AI and Practical Finance Series**, in Kindle/paperback/hardcover formats:

1. **Claude AI for Finance Professionals** (featured; Kindle 2026-03-17, $5.99) —
   institutional-grade prompts for analysis, valuation & investment research ([[claude-anthropic]]).
   Re-humanized 2026-07-13/14 and re-counted: front matter corrected from "16 Chapters · 120+
   Prompts" to **"17 Chapters · 135+ Prompts"** (120 numbered + 14 flagship CRAFT + the Ch.1
   master). Interior `KDP_PRINT_INTERIOR_v6_ch1_prompting.pdf` 182 pp; EPUB
   `DIGITAL_BOOK_BLOCK_v6_ch1_prompting.epub`.
2. **AI Prompts for Financial Analysis** (Kindle 2026-03-11) — 100+ practical prompts
3. **AI Prompts for Financial Analysis — Equity Research Edition**
4. **Stop Losing Money** (Kindle 2026-04-07)
5. **The Wealth Code of Chhatrapati Shivaji Maharaj** (Kindle 2026-04-09)
6. **Claude Cowork for Finance** (v5 rebuild 2026-08-02) — eleven capabilities + capstone +
   an honest closing chapter on the tool's limits. **v5 voice/credibility pass:** em-dash density
   cut 16.4 → 5.3 per 1000 words, all 13 templated "Why Cowork, in plain terms" closing boxes
   removed, employer names scrubbed from the author bio, and three original decision frameworks
   added (Delegation Test Ch.1, Verification Tier Ch.2, Automation Payback Line Ch.3), plus a
   "When Not to Use Cowork" table and an honest tool comparison in Ch.13, Appendix C (46-code
   failure catalogue, 14 flagged silent) and Appendix D (measurement protocol for every Time
   Impact figure + Amazon-compliant honest-review ask). Ch.9 gained "The Public Record", citing
   the Institutional-Trader repo's pre-registered OBJECTIVE_SPEC.md, the CAPITAL_CURVE_RESULTS
   breach of its own drawdown cap, and BANKNIFTY_0DTE_REJECTION / DATA_AVAILABILITY_LIMITS as
   checkable public stress tests; stale counts corrected 212 commits/eight studies -> **383
   commits, 56 studies** (verified against the local clone). 111 pp. **Front matter restructured for the Amazon pre-read** (~10% sample): full disclaimers
   and About the Author moved to the BACK behind a short front notice, so Ch.1 moved p14 -> p10
   and the Delegation Test now lands on p11, inside the sample. Slash commands (/goal, /loop)
   deliberately NOT added - they are Claude Code features covered in [[claude-code-finance-book]].
   A one-page **"Why This Book Is Different"** now sits on p4, right after the TOC and before any
   setup material: five checkable differentiators, the case against (no independent validation),
   and a "do not buy this if..." close. Retitled *How This Book Differs From Every Other Claude Book*. The old
   "Before You Start" preamble (smarter-chatbot metaphor, capability count) was cut as
   throat-clearing, and the toy CLAUDE.md example was replaced by the **real operating agreement** —
   Context / 7 numbered work rules / Output / Shortcuts, genericised for a research desk with no
   personal detail, credited to Karpathy's context engineering. 112 pp, exactly page-neutral vs v4;
   preview-zone em-dash density 2.2/1000.
   Build source now lives at `~/files/kdp-books/claude-cowork-finance/` (`src/*.xhtml` +
   `build.py`, Playwright/Chromium two-pass TOC). Interior `COWORK_PRINT_INTERIOR_v5.pdf`;
   EPUB `COWORK_EPUB_v5.epub`. Covers Claude's Cowork mode for finance workflows
   ([[claude-anthropic]]).

Both #1 and #6 print PDFs pass the full KDP font audit after each rebuild; deliverables replace the
same filenames in `~/Downloads/`. **Hardcover cover gotcha:** the AI-book hardcover cover is a
flattened image with a *live text layer* (author bio + spine title painted over white patches) —
render to 300 DPI first to bake the text in before widening the spine, else editing wipes it; sized
14.346 × 10.417" for the 248-pp block.

**More cover-rejection gotchas (2026-07-20, from Stop Losing Money + Wealth Code wraps):**
- **Spine text touching KDP's spine fold guide gets rejected — a blank spine never does.** KDP
  rejected "Stop Losing Money" repeatedly because the vertical spine title sat on the fold line with
  letters spilling out of the ~7 mm spine into the back panel, while our own overlay kept "passing".
  Fix = remove spine text entirely (verify 0.0000% ink in the spine channel); default thin books to a
  clean blank spine.
- **Keep the back-cover byline/bio off the lower back panel — it collides with KDP's auto-added ISBN
  barcode.** Move authorship to the front cover + spine instead. The barcode in KDP's preview is
  KDP's own (expected; don't add your own).
- **Dimensions are exact and per-binding/page-count.** e.g. Wealth Code B2: paperback 12.597×9.250",
  hardcover 14.111×10.417"; even a ~0.2" mismatch triggers the "cover size" error. When a cover is
  rejected, zoom into KDP's own error preview — the local overlay can lie.

Catalog now spans multiple editions (Spanish + German added 2026-07); ranks tracked daily in
[[kdp-dashboard]]. A further book is in build:
[[dotnet-architect-book]] (not yet in the catalog JSON as of 2026-07). See [[claude-algo-trading-book]]
for the algo-trading title.

## Added since 2026-07-23

Build directories now under `~/files/kdp-books/`: `claude-finance-professionals`,
`claude-finance-german`, `ai-prompts-book`, `german-a1-mastery`, `teen-money-playbook`,
`stop-losing-money`, `wealth-code`, plus shared `aplus-assets`.

- **AI Prompts for Financial Analysis** rebuilt 2026-07-12 from `kdp-books/ai-prompts-book`.
- **German A1 Mastery** rebuilt 2026-07-26 — 269-page PDF + EPUB. No audio companion yet.
- **Teen Money Playbook** — original teen personal-finance title, 97 pages, PDF + EPUB +
  covers, 2026-07-26. Written from scratch, not derived from any existing teen-finance book.
- [[claude-code-finance-book]] — "Claude Code for Finance", v3 delivered 2026-07-25 (172 pp),
  cover and upload still outstanding.

The listing side of all this — descriptions, editorial reviews, A+ modules, and the Amazon
policy that constrains them — is its own page: [[kdp-listing-operations]]. The binding rule
from 2026-07-30 is that **a cover or blurb may only claim what the manuscript delivers**,
verified by grepping the manuscript, not by trusting the previous cover.

## Cowork book, reviewed and rebuilt 2026-08-10

A month after publishing, [[tejas-jadhav]] read **Claude Cowork for Finance** back and rejected it.
His objections were that it is not in his voice, that a non-developer cannot follow it, that it
never says plainly what to do, and that it reads as AI-written. He also flagged that ECAS and a
mutual-fund dashboard mean nothing to an American reader, which is most of his audience. The
rebuild ran under a hard constraint that paperback and hardcover page counts must not change, and
they held at 114 and 120.

**The version that shipped is v9, and the reason is accuracy rather than prose.** ChatGPT and
Gemini both preferred the earlier v6, but they were rating the writing of one file. v6 contradicts
itself in seven places: Chapter 1 says the Pro plan covers everything while Chapter 5 needs a
separately billed API key, one chapter's own arithmetic is wrong by a factor of two, the same job
costs two hours in a table and an afternoon in the prose two pages later, and Google Drive is used
by four chapters but installed by none. The book sells on the claim that every number traces back
to something, so the reader who follows it hits a wall and stops trusting the rest.

Ten sharp lines were restored into v9 after the voice pass over-flattened it, and three were left
out because they are staccato fragments. The general rule that came out of this — the fragment ban
wins, a complete sentence carrying one fact stays — is now [[voice-pass]].

## The Cowork cover, settled 2026-08-11

Ten rounds ran through the cover pipeline described in [[book-covers]], and cover **J** ships. It
sits in the register the ranking Claude titles use, a cream ground with a clay accent and the title
alone, with the palette deliberately nudged off Anthropic's published values so the cover carries
the recognition without wearing their trade dress. It prints no starburst and no vendor badge. The
files are `COWORK_EBOOK_Cover_J.jpg`, `COWORK_PAPERBACK_Cover_J_114pp.pdf` and
`COWORK_HARDCOVER_Cover_J_120pp.pdf` under `~/files/kdp-books/claude-cowork-finance/cover/`, and
covers A through H are superseded. Page counts are unchanged at 114 and 120, so the spine widths
came straight off KDP's calculator.

## Two additions from 2026-08-13

**"Claude AI for Absolute Beginners" reached a full draft.** All 75 chapters are written, the book
runs to 243 pages with 13 real product screenshots, and it is the first title outside finance. It
carries its own byline rule, its own interior identity and its own register rule, so it has its own
page: [[claude-beginners-book]].

**A Claude job-search book was assessed and rejected as a lead title.** A rival shipped the same
concept on 1 August 2026 and sits at 1.4 million in the Kindle store, and the winner of that whole
category sells two or three copies a day. The evidence and the one honest angle are in
[[job-search-book-verdict]].

**The translated editions are now their own project (2026-08-16).** German and Spanish editions
of the finance flagship ship on the same d1 cover design as the English one, and their counts,
their page difference and their open listing defects are recorded in
[[claude-finance-translations]]. The number that matters for both is **128 prompts and 18
chapters**, which the German listing description still contradicts.
