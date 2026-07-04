---
title: Google identity/SEO fix for "tejas jadhav"
type: synthesis
tags: [seo, identity, google, knowledge-panel]
created: 2026-07-05
updated: 2026-07-05
sources: [~/files (root repo), ~/files/scmhrd-ai-finance, ~/files/aifinance]
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
