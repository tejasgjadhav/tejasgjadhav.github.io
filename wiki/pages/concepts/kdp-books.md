---
title: KDP book catalog — AI and Practical Finance Series
type: concept
tags: [kdp, books, writing, amazon]
created: 2026-07-03
updated: 2026-07-20
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
6. **Claude Cowork for Finance** (in finalization 2026-07) — restructured to **eleven capabilities
   + a capstone chapter + an honest closing chapter on the tool's limits** (front matter corrected
   from stale "twelve capabilities"). Interior `COWORK_PRINT_INTERIOR_v4.pdf` 112 pp; EPUB
   `COWORK_EPUB_v4.epub`. Covers Claude's Cowork mode for finance workflows ([[claude-anthropic]]).

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
