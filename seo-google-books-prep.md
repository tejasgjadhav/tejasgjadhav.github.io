# Google Books Partner Center — upload prep (P1 highest-ROI action)

**Why:** verified 2026-07-23 — you have ZERO presence in Google Books (`inauthor:"Tejas Jadhav"`
returns nothing). Books inside Google's own corpus feed author-entity clustering directly into the
Knowledge Graph — no third-party gatekeeper. This is the strongest single lever for the person
Knowledge Panel that evicts the wrong "housing complex" card.

**Your part (~30 min):** create the account + upload. My part: this metadata is ready to paste.

## ⚠️ KDP Select caveat (read first)
If an EBOOK is enrolled in KDP Select, its digital exclusivity conflicts with distributing ebook
content elsewhere. SAFE ROUTE: upload the **PRINT edition** PDFs (interior + cover), set
**preview-only (20%)**, and do NOT enable "sell on Google Play" for any Select title. The entity
benefit comes from metadata + author clustering, not Play sales.

## Steps
1. Go to https://play.google.com/books/publish/ (Partner Center) → sign in with your Google account.
2. Create publisher account: name **Tejas Jadhav** (or your KDP imprint), country India.
3. Add each book ("Add book" → by ISBN if it has one, else create entry) with the metadata below.
4. Upload print interior PDF + front cover (from your KDP source folders, e.g. `~/files/kdp-books/`).
5. Settings per book: territories = WORLD, preview = 20%, "Buy link" → your Amazon page. Skip Play sales.

## Metadata (paste-ready)

Author (identical on every title — this exact string): **Tejas Jadhav**
Contributor role: Author. Website: https://tejasgjadhav.github.io/

| Field | Book 1 | Book 2 | Book 3 | Book 4 | Book 5 |
|---|---|---|---|---|---|
| Title | Claude AI for Finance Professionals | AI Prompts for Financial Analysis | Claude Cowork for Finance | Stop Losing Money | The Wealth Code of Chhatrapati Shivaji Maharaj |
| Subtitle | 120+ Institutional-grade Prompts for Financial Analysis, Valuation & Investment Research | 100+ Practical Prompts for Equity Research, Valuation, Investment Banking and Financial Risk Management | A Simple and Practical Guide to Building AI Agents and Financial Workflows | Real Stories from a Private Wealth Manager, Costly Mistakes from Investors & the 3-3-3 System That Fixes Them | Timeless Money Principles to Build Wealth, Security & Financial Freedom |
| Series | AI and Practical Finance Series | same | same | same | same |
| Language | English | English | English | English | English |
| ISBN-13 (print) | ← from your KDP dashboard | ← KDP | ← KDP | ← KDP | ← KDP |
| BISAC | BUS027000 (Finance) + COM004000 (AI) | same | same | BUS050000 (Personal Finance) | BUS050000 + HIS017000 |
| Amazon ASIN (ebook) | B0GSX73KF6 | B0GS5RL6XS | B0H1R2GZX9 | B0G7YSZZJM | B0D8R41W2F |

Descriptions: reuse each book's Amazon description verbatim (consistency helps entity matching).
German + Spanish editions of Claude AI: add after the English five (language de / es).

## After upload
Tell Claude → I'll verify `inauthor:"Tejas Jadhav"` in the Books API, and add Google Books URLs to
the /books page schema sameAs on the next natural update (no forced reindex).

## Also queued for after Goodreads approval
- Wikidata **P2963** (Goodreads author ID) = `69311592` — Claude will guide the add.
- OpenLibrary author record (openlibrary.org) → then Wikidata **P648**.
- ISNI self-registration (~€35, https://isni.org) → then Wikidata **P213**.
