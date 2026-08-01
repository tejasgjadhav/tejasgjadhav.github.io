---
title: KDP listing operations — descriptions, editorial reviews, A+ content
type: concept
tags: [kdp, amazon, policy, marketing, listings]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/HANDOFF.md, ~/files/kdp-books/DESCRIPTIONS-rewrite-2026-07-27.md, ~/files/kdp-books/EDITORIAL-REVIEW-blurbs-draft.md]
---

What was learned running the Amazon listing side of [[kdp-books]], as distinct from writing
the books. Pass of 2026-07-27 rewrote the descriptions for three titles, entered editorial
reviews, and built A+ modules.

## Policy first, then act

The standing rule that came out of this pass (now section 8 of the global `CLAUDE.md`):
for anything touching KDP, check the actual Amazon policy **before** acting, and stop if
the requested action violates it. Known rules so far:

- No rank or "#1 bestseller" claims, and no time-sensitive statements, in descriptions.
- **No customer-review quotes or star symbols in A+ content — explicit Amazon ban.**
- Editorial reviews must be real and attributed. Never invent personas. That is both Amazon
  policy and CFA Standard I for [[tejas-jadhav]].
- No incentivised customer reviews.
- A+ images ≤5000 px per side and <5 MB, with exact per-module dimensions.

Reuse of verbatim customer-review text in editorial reviews is **not settled** policy, so
the reviews were entered as named-consent testimonials (bold headline / quote / italic name
and title), no "Amazon review" label, no stars, and anonymous reviewers skipped.

## Cover and metadata compliance

A cover, blurb or A+ module may only claim what the manuscript actually delivers. Grep the
manuscript for every claim before approving any of them. The case that forced the rule
(2026-07-30): a cover claimed "Excel add-ins, Bloomberg integration" when the book had
neither — its connectors were FactSet, LSEG, PitchBook and Google Workspace. Naming a
vendor implies a relationship, so prefer generic wording. Counts (chapters, prompts, pages)
must be counted in the source, never carried over from the previous cover. Confidentiality
and credential rules apply to the back-cover bio exactly as they do to the interior — see
[[tejas-jadhav]].

## Mechanics learned

- Descriptions are set through the page's CKEditor instance
  (`CKEDITOR.instances.editor1.setData(html)` + `updateElement`), then Save and Continue,
  then Publish — per format, three formats per book.
- A format already "live with unpublished changes" pushes those pending edits out too.
- Ref-clicks on Save/Publish often hit hidden duplicate dialogs; scroll to the bottom and
  click the visible button by coordinate. Verify the submit from the bookshelf status, not
  the toast, which vanishes.

Ranks for all of this are tracked in [[kdp-dashboard]]; paid demand in [[amazon-ads]].
