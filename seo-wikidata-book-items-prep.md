# Wikidata book Q-items — prep (calendar item #6, user publishes)

**Why:** Q-items for the flagship books create author↔work edges INSIDE Google's Knowledge Graph
(strongest co-occurrence surface) and armor Q140561693 against deletion challenges (a person item
that anchors several work items reads as infrastructure, not vanity).

**How:** wikidata.org → "Create a new Item" (left menu), logged in as Tejasips. One item per book
(the WORK, not each edition). Then add statements. Claude can guide click-by-click; user types/publishes.

## Item 1 — Claude AI for Finance Professionals
- Label (en): Claude AI for Finance Professionals
- Description (en): 2026 book by Tejas Jadhav on AI prompts for financial analysis
- Statements:
  - P31 instance of → Q47461344 (written work)
  - P50 author → Q140561693 (Tejas Jadhav)
  - P407 language of work → Q1860 (English)
  - P577 publication date → 2026
  - P123 publisher → Q17637375 (Kindle Direct Publishing) [optional]

## Item 2 — AI Prompts for Financial Analysis
- Label (en): AI Prompts for Financial Analysis
- Description (en): 2026 book by Tejas Jadhav with AI prompts for equity research and risk management
- Statements: P31→Q47461344; P50→Q140561693; P407→Q1860; P577→2026

## Item 3 — Stop Losing Money
- Label (en): Stop Losing Money
- Description (en): 2026 personal finance book by Tejas Jadhav
- Statements: P31→Q47461344; P50→Q140561693; P407→Q1860; P577→2026

(Wealth Code + Claude Cowork can follow later; 3 items is enough for the effect.)

## After creating each item
- Back on Q140561693: the reverse edge appears automatically via P50 (no "notable work" statement
  needed immediately; P800 notable work → the new QIDs can be added as a nice-to-have).
- Add ISBN-13 (P212) later if print ISBNs are pulled from KDP dashboard.

## UI gotchas (from July experience)
- "+ add statement" position shifts after each publish; banners can push the publish button off-screen.
- Verify each save via `api.php?action=wbgetclaims&entity=<new QID>`.
- Never blind-click suggestion dropdowns — screenshot first.
