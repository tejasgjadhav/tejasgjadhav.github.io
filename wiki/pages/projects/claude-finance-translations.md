---
title: Claude AI for Finance Professionals — the German and Spanish editions
type: project
tags: [kdp, book, translation, covers, german, spanish]
created: 2026-08-16
updated: 2026-08-16
sources: [~/files/kdp-books/claude-finance-german/HANDOFF.md, ~/files/kdp-books/claude-finance-spanish/HANDOFF.md]
---

Two translated editions of the flagship finance title live in their own project folders:
`~/files/kdp-books/claude-finance-german` and `~/files/kdp-books/claude-finance-spanish`.
Each carries a HANDOFF.md holding the counted manuscript facts. The catalog they belong to is
[[kdp-books]] and the cover pipeline that produced their artwork is [[book-covers]].

## The counts, verified per chapter on 2026-08-16

Both editions run **128 numbered prompts, 18 chapters and 15 CRAFT flagships**. The German PDF
is **362 pages** and the Spanish is **348**. A raw string count of the flagship heading returns
18 in both books, but three of those print across a page break, so 15 is the real number. An
Excel-model spec sits under every prompt, which is why the German book counts 129 `EXCEL-MODELL`
headings — 128 prompts plus one in the walkthrough — and the Spanish counts exactly 128.

**The 14-page difference is one section, not padding.** The German edition carries a Microsoft
prompt walkthrough at pp.23–33 between chapters 1 and 2, and the Spanish edition has nothing
there. Microsoft is still in the Spanish book as the subject of the institutional DCF in
Chapter 3, so that back-cover bullet was rewritten rather than reused. The Excel count confirms
the difference independently, which is a useful pattern: **two counts that disagree for the same
reason are stronger evidence than either alone.**

## Covers

All three editions now share the **d1 design**, the cream ground with the full-bleed orange
band, so the shelf reads as one series. Paperback and hardcover ship as PDF wraps and Kindle
ships as an 800 DPI JPEG.

**The ebook cover is not a crop of the print front panel.** A 6×9 print front is a 1.5 ratio and
KDP's ebook spec wants 1.6, so a cropped print cover gets letterboxed in the Kindle store and
loses height against every book beside it. Both designs were drawn at 2560×4096, which is
already 1.6, so the ebook file is the native shape and the print wrap is the adaptation. Build
the ebook cover from the source design rather than from the wrap.

**The hardcover gate caught a real bug.** On the Spanish wrap the eyebrow and title landed at
y 0.749 while the trim only starts at 0.7085, which would have glued the title into the wrap.
This is the same bug class as the German footer one, so measure both panels against the trim
rather than the canvas. Details of the gate itself sit in [[book-covers]].

**One interior serves both print formats.** KDP's margin table has no separate hardcover gutter
rule, and at 348 pages the symmetric 0.698" side margins clear the 0.625" requirement on
whichever side the spine lands. The interior is not mirrored, so the side margins can never be
reduced without re-checking, and the bottom margin has only 0.034" of headroom.

## Open defects as of 2026-08-16

- The **Spanish title page says "130+ Prompts originales"** and the real number is 128. That
  page sits inside the Amazon Look Inside sample, so buyers can see it.
- The **German listing description contradicts the covers**. It says "über 130 sofort
  einsetzbare Claude-Prompts" twice and "17 strukturierte Kapitel", where the 17 is copied from
  the English book. The correct numbers are 128 and 18.
- Five superseded German cover files carrying the false "130+ Prompts" claim are parked in
  `~/Downloads/PDFs/` and must never be uploaded.

Related: [[kdp-books]], [[book-covers]], [[kdp-listing-operations]], [[kdp-dashboard]],
[[claude-anthropic]].
