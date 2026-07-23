---
title: Google identity/SEO fix for "tejas jadhav"
type: synthesis
tags: [seo, identity, google, knowledge-panel]
created: 2026-07-05
updated: 2026-07-23
sources: [~/files (root repo), ~/files/scmhrd-ai-finance, ~/files/aifinance, ~/files/HANDOFF-seo-photo.md]
---

Google search for "tejas jadhav" was showing other same-name people's photos (a barista,
an actor, a Justdial photographer) because [[tejas-jadhav]]'s own web properties had no
usable photo signals. Root causes found and fixed (2026-07-04): a placeholder image, a
dead canonical URL (site referenced `/scmhrd-ai-finance/` while the live path is
`/SCMHRD/`), a stale `sameAs` list, mismatched `og:image` dimensions (792×792 declared vs
800×800 actual), and a `Person.image` schema that was a plain string instead of a full
`ImageObject`.

**Fix applied, now the standing rule:** one canonical portrait,
`https://tejasgjadhav.github.io/tejas-jadhav.jpg` (blue blazer), referenced by the exact
same URL everywhere — root site, [[scmhrd-ai-finance]] (`/SCMHRD/`), and [[aifinance]]
(`/AIFINANCE/`) — in `<img>`, `og:image`, `twitter:image`, and Person schema. AIFINANCE's
Person schema deliberately shares the same `@id` (`#person`) as root's, to merge as one
entity for Google. Never duplicate or rename the photo file. GitHub profile
(`github.com/tejasgjadhav`) was also overhauled to match: portrait avatar, name "Tejas
Jadhav, CFA, FRM", bio/location/website/LinkedIn filled in, and a public profile-README
repo created.

**No Knowledge Panel exists yet** (checked 2026-07-04). Path to get one, in priority
order: (1) create a Wikidata item — strongest lever; (2) get titles into Google Books
Partner Center; (3) more third-party coverage. This is open/unstarted if the user wants to
pursue it.

**Escalation note:** filed a thumbs-down + written report on a wrong-photo AI Overview via
the page-**footer** "Send feedback" link — the AI-Overview's own "Report a problem" widget
never loaded in-browser. Search Console indexing was requested for both the root domain
and `/SCMHRD/`; impressions were already up +600% same day. Google recrawl takes days to
weeks — re-check in ~3 weeks before escalating further.

**Entity de-merge — the "many tejas jadhav now" effect is progress, not regression (2026-07-08):**
the user noticed the plain-name query, which used to surface one person, now reads as a common name
with many people. This is Google's remediation working: it had wrongly *merged* several same-name
people into one entity (the user's bio stitched to another face), and the wrong-photo feedback filed on
the 4th is exactly the signal that makes Google *split* the conflated entity — which transiently shows
the name as generic before it re-anchors on the right person. Good signs already visible: the qualified
query **"tejas jadhav books"** AI Overview shows the correct blue-blazer photo + the book series
(reconciliation working on qualified queries; only the bare-name query still lags), and LinkedIn /
github.io / Amazon own the top-3 on the qualified search. **Re-confirmed there is still NO claimable
Knowledge Panel** across plain, qualified, and books queries — the right-hand box is the AI Overview's
source list, not a panel, and Google's own feedback-URL entity-id returned "unknown"; the claim/verify
flow only activates from a live panel, so the **Wikidata item remains the real lever** to mint one.

**Wikidata item now EXISTS — the priority-1 lever is DONE (2026-07-15):** created
**Tejas Jadhav ([Q140561693](https://www.wikidata.org/wiki/Q140561693))**, "Indian finance professional
and author on AI in finance". Built out via the authenticated Wikidata API (far faster than the finicky
web form) to **16 properties / 23 statements** — instance-of human, occupation writer + financial analyst,
citizenship India, official website, LinkedIn/GitHub/Facebook/Amazon-author IDs, employers Citigroup +
Wipro + HDFC, educated-at SIMSREE + University of Pune, family name Jadhav, languages, and **P18 image =
`Tejas Jadhav CFA FRM.png`** (user uploaded a self-portrait to Wikimedia Commons under CC-BY-4.0, the only
way to feed the correct blue-blazer photo into Google's Knowledge Graph). First **independently-sourced**
statement added: P463 member-of CFA Institute, cited to *Mint* newspaper (2 Feb 2026, p.13) — a CFA
Society India charterholder listing (name-in-a-list, not an editorial feature; "Featured in Mint" on the
site overstates it). The QID is now in the Person-schema `sameAs` on **all three** sites (root, SCMHRD,
AIFINANCE), bidirectionally linked. Notability caveat stands (self-created, mostly self-published
sources) — the Amazon-published books + the Mint citation give it a fighting chance if AfD'd.

**ORCID cross-link (2026-07-15):** user created ORCID **0009-0000-9407-6871**, wired as a two-way
citation — Wikidata P496 = ORCID, ORCID URL in Person `sameAs` on all 3 sites, and the ORCID record
carries website backlink + Employment (Wipro, Pune) + 5 books. ORCID ↔ Wikidata ↔ sites now all
cross-confirm the same person. Fact corrections applied from the résumé: works from **Pune** (not
Bengaluru), BE from **University of Pune**, Master's is **MMS** (WorldQuant University removed as P69 — not
his school).

**Monitor cadence now WEEKLY (2026-07-15):** the `seo-rank-monitor` scheduled task was switched from daily
to **Mondays ~08:01** — the build work (photo, entity, ORCID) is finished, so what remains is a patient
wait on Google's recrawl clock. It was also upgraded from monitor-only to an active improver that
auto-applies SAFE structural fixes (entity/`sameAs`/portrait consistency, JSON-LD, dead links) and pushes;
credential/account actions and on-page keyword churn / re-indexing stay hard-forbidden (re-indexing resets
Google's eval clock). Standing lesson: **off-page authority is the durable lever; stop churning on-page**.

**Ranking as of 2026-07-15 — IMPROVED:** all three qualified queries (`+cfa`, `+author`, `+finance`) are
fully owned in the top-3 by github.io / LinkedIn / Amazon; on the bare-name query the user rose to the
**#1 AI Overview bullet**. The one residual issue is the bare-name entity thumbnail still showing a wrong
same-name person's photo (the blue-blazer portrait not yet adopted as the entity image) — consistent with
the entity de-merge still settling; the new Wikidata P18 image is the fix, now a days-to-weeks recrawl
wait the weekly monitor watches. Full session handoff: `~/files/HANDOFF-seo-photo.md`.

**2026-07-23 monitor + role audit:** health GREEN, structure unchanged (nothing manufactured to edit). On
the bare-name query the AI Overview is now **fully on-message** ("CFA Charterholder, FRM-certified finance
professional, published author… Citi, HDFC, Swiss banks… AI and financial analysis") and github.io is **#1
organic** — but on **mobile** the entity-panel slot is **hijacked by a Google Maps "place" entity**
("Tejas Jadhav — Housing complex… Permanently closed", Pune) rather than a person Knowledge Panel (still no
claimable panel). Photo still not adopted (KG recrawl lag). Remaining levers are all user-gated Google-account
actions: report/claim the wrong Maps place, wait on the P18 recrawl, earn genuine backlinks. **Role audit:**
"author" is fully covered everywhere; **"business analyst" was missing** from Wikidata + schema — plan is
Wikidata **P106 += business analyst (Q1017553)** with a source (safe off-page statement), *not* an on-page
keyword; blocked at session end on the logged-in Chrome being connected, not yet applied. See [[tejas-jadhav]].
