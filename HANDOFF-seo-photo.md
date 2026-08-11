# HANDOFF — Google identity / photo / entity work

Last updated: 2026-08-11 (session: scheduled `seo-rank-monitor` run + interactive follow-up)

## Goal

When someone searches **"tejas jadhav"**, Google should show **his** face — the blue-blazer podium
portrait — not one of the other real people who share the name. Ranking is secondary and tracked only
because it feeds the photo outcome.

Canonical portrait: `https://tejasgjadhav.github.io/tejas-jadhav.jpg` (1200×1200 JPEG, 128,874 bytes).
It is `~/files/tejas-jadhav.jpg`. **There is no .png** — that was the deleted Commons copy. Never
duplicate, rename, re-crop or re-encode it.

Full history lives in the memory file, which is the source of truth:
`/Users/sayali/.claude/projects/-Users-sayali-files/memory/google-photo-identity-fix.md`
Read it before doing anything here.

## Where things stand (2026-08-11)

**Infrastructure: green.** Root / `/SCMHRD/` / `/AIFINANCE/` all 200. Pages build healthy (no gitlinks).
All JSON-LD parses. All three properties share Person `@id` `https://tejasgjadhav.github.io/#person`,
`name` exactly "Tejas Jadhav", `image` = the portrait.

**Photo: improving, not won.** His portrait is image-strip **tile 4** on the bare name (was tile 6 for
three runs), now served via his Amazon.in author page. The bare-name **AI Overview returned** on 11 Aug
after two days absent, with him as the **first of three** "Prominent Profiles" and his correct photo on
the top source card. Goal condition is tile 1 or a true entity thumbnail — not reached.

**The July regression and its cause.** On 23 Jul the AI Overview was entirely about him (single-entity
framing). **Wikidata Q140561693 was deleted 8 Aug** for failing notability, taking all 23 claims
including the P18 portrait. The Commons file died a day later as an orphan. Framing degraded to a
disambiguation menu. This is the single identified cause.

## Hard limits — do not cross

- **Never re-create the Wikidata item or re-upload to Commons.** G4 recreation is speedy-deleted and
  risks blocking his account. He does not clear Wikidata notability: every source is self-created
  (own site, LinkedIn, GitHub, Facebook, Topmate, Amazon, Goodreads, ORCID) plus five KDP
  self-published books plus a name in an alphabetical list in Mint. Verified ≠ notable.
- **No re-indexing requests, no Search Console re-submits.** Both were done in July. Repeats reset
  Google's evaluation clock.
- **No credential or account actions** — Google, Wikimedia, Commons, Search Console sign-in, CAPTCHAs.
- **No on-page keyword churn or cosmetic rewrites.** Structural correctness and factual accuracy only.
- The Google Maps place cards ("Tejas Jadhav — Housing society/complex", Pimpri-Chinchwad and Wadgaon
  Shinde) are **genuine listings**. Do not false-report them. Editing them is a user-gated action.

## What shipped this session

**Commit 7117375 (root repo, live):** false-claim cleanup, user-approved after he confirmed the
claims were untrue.

- Removed a `NewsArticle` schema node headlined "TEJAS JADHAV, CFA, FRM featured in Mint Newspaper"
  (publisher livemint.com). Its cited URL `pressreader.com/article/281702621142581` returns
  PressReader's generic homepage — the string "Tejas" appears **0 times** to a crawler.
- Removed `Person.award` "Featured in Mint Newspaper" and the PressReader `sameAs` edge (10 → 9).
- Restated Mint accurately on-page: Mint published CFA Society India's roll of 2025 charterholders on
  2 February 2026, and his name appears in that list. **His words: "that is a name in the list and not
  a feature."**
- Removed "#1 Bestseller in India" everywhere. **His words: "we are not featured as no.1 best seller
  in india."**

**Kept because true:** the free-Kindle launch rank, scoped to "#1 in its free Kindle category on
Amazon.in at launch" (his words: "point in time rankings for amazon.in in free kindle categories").

## In progress at handoff time

He then corrected the cut as too broad: **the category best-seller ranks are real and audited** at
`https://tejasgjadhav.github.io/BSR/`. That dashboard shows 8 books, 20 formats, 17 countries, 85 live
rankings, best category rank **#5**, e.g. #13 Financial Risk Management (Kindle Store US), #43
Netherlands, #39 Business & Economics in German, #152 Valuation. Some country rows are marked stale
(May 2026).

**Next step: restore an accurate, audit-linked category-rank claim** in the FAQPage answer, the Book
node description and the meta descriptions — pointing at the BSR page as the evidence trail. Do not
restore bare "bestselling"; the defensible form names the category scope and links the audit.

## Also flagged, not touched

`scmhrd-ai-finance/index.html` still carries "Bestsellers" as a stat tile and "an Amazon bestseller"
in the bio. No rank number, so softer than what was removed, but it is not audit-linked either.

## Standing gotchas

- **Facebook now returns 400 to curl** (was 200). It is anti-bot, not a dead link — `facebook.com/zuck`
  and a nonsense handle both return 400. LinkedIn 999/429 and Amazon 429/503 are likewise anti-bot.
  Do not remove any of these from `sameAs` on a status code alone. Only a real 404 is a failure.
- **If a root-site edit "doesn't go live":** check `curl -sI` last-modified against the latest commit,
  then `git ls-tree -r HEAD | awk '$1=="160000"'` before assuming CDN lag. Gitlinks with no
  `.gitmodules` fail the Pages build silently — this hid a week-long outage 2 Aug → 9 Aug.
- **Every nested Person node** (author, instructor, founder) must carry the shared `#person` @id, not
  just the top-level node. SCMHRD's `Course.instructor` was missing it until 10 Aug (commit 0fb1483).
- Google is still serving a **cached snippet for the deleted Wikidata page** on "tejas jadhav finance".
  The page is 404 and the API says `missing`. Nothing to fix; do not recreate.

## The only real remaining lever

Genuine third-party coverage — a journalist profile, a trade-publication interview, an
organiser-published speaker listing, an independent book review, a citation record. That is what
clears both the Wikidata bar and the Knowledge Panel confidence threshold, and it cannot be
manufactured. On-page is maxed.
