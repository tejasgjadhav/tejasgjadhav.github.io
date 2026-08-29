---
title: Claude Code for Finance (book build)
type: project
tags: [book, kdp, claude-code, writing]
created: 2026-08-01
updated: 2026-08-29
sources: [~/files/claude-code-finance-book/HANDOFF.md, ~/files/claude-code-finance-book/HANDOFF-V6.md, ~/files/claude-code-finance-book/GAPS.md]
---

Book build at `~/files/claude-code-finance-book`, aimed at finance people who do not code.
**v3 delivered 2026-07-25**: 172-page 6×9 PDF (`claude-code-for-finance.pdf`) plus EPUB
(`Claude_Code_for_Finance_2026.epub`), 18 parts, ~43k words. Compliance scan clean. Cover
art and the KDP upload were left to [[tejas-jadhav]] separately.

**v1 was rejected outright by the author as AI slop and rebuilt from scratch.** The rebuild
is the interesting part, because it produced a reusable drafting pattern: every number in
the book has to come from a `facts/*.md` file written from a real captured session, and the
drafting agents are forbidden from inventing figures — a facts firewall. Real terminal
sessions were captured through a GNU `screen` harness (`demo/scap.sh`, `demo/repl.sh`) with
screenshots taken by computer-use, because the macOS `screencapture` CLI is blocked in that
context.

Structure: Part I setup (setup, prompt craft, goals and loops, `CLAUDE.md` + handoff +
memory wiki, wiring GitHub/API/connectors), Part II desks (fundamental analysis, valuation
via [[jarvis]], fixed income, [[institutional-trader]], technical analysis, portfolio
management, corporate finance and FP&A, Citi Pillar 3 via [[basel-analyzer]], ESG, ethics,
a thirty-day plan, appendix). US-oriented, with India as callout rather than default — the
same reorientation applied to [[claude-algo-trading-book]].

Voice exemplar for the whole build was
`claude-algo-trading-book/parts/02-working-with-the-machine.md`. See [[kdp-books]] for the
published catalog.


## V6, the capability update (24–25 August 2026)

The book is now 201 pages and it still has no KDP listing. A gap audit found the hole that
prompted the rewrite. V5 mentioned MCP three times and hooks once, and it never mentioned
plugins, subagents, the system prompt, the harness, TradingView, routines or output styles at
all. Chapter 5 had defended the omission in the text, saying connectors were described "at the
shape level, on purpose". That decision was the largest gap in the book, and the audit sits in
`GAPS.md`.

A new Part III answers it in four chapters. Chapter 15 covers the harness and the system
prompt, and it uses the author's own rig as the worked example. Chapter 16 covers plugins and
the finance marketplace. Chapter 17 takes his TradingView MCP server apart. Chapter 18 covers
skills, subagents, hooks and schedules. Every fact was verified on the machine rather than
recalled, which is the same facts-firewall discipline the v3 rebuild introduced.

Three findings from that verification are worth keeping. The Anthropic `finance` plugin ships
eight skills and its own `CONNECTORS.md` admits there is no accounting or ERP MCP server yet,
so the `small-business` plugin is what wires QuickBooks, Stripe, PayPal and Square. The
TradingView MCP server exposes exactly 78 tools in sixteen groups, counted from source rather
than read off the README. Its health check failed during the writing because the desktop app
was not running, and the chapter keeps that failure in as the honest picture of a local
connector. See [[claude-anthropic]].

A second round added the navigation the author asked for. A "Start Here" table on page 9 maps
fifteen jobs to chapters. A decision tree under it asks four questions and lands every path on
a chapter, and the one path that ends in a warning is the monthly chore whose last answer
cannot be checked. The thirty-day roadmap came back as Chapter 19. Every chapter now closes on
a BUILD THIS checklist. Chapter 1 gained a full interface guide, six rows for the screen and
twenty-one for the controls worth learning, each checked against the current docs because that
shortcut set moves.

One thing was assumed and turned out to be false. The author asked for the button walkthrough
"the way we have in our flagship book", and the flagship book does not contain one. All 29
files were read to establish that. Check before reusing content from another title.

## Covers, 25 August 2026

`cover/build_covers.py` builds all three KDP covers from one approved raster: a Kindle JPG at
1707 × 2560, a paperback PDF at 12.703 × 9.25 in, and a hardcover PDF at 14.217 × 10.417 in.
The print dimensions came from KDP's own Cover Calculator, driven in his Chrome for 6 × 9 at
201 pages on white paper, which is the method [[book-covers]] settled on after the hardcover
formula was withdrawn.

The byline was patched rather than redrawn. "CFA, FRM" had been set about 40% smaller than the
name, and the fix rebuilds only the byline band and heals the halftone dots around it pixel by
pixel. A full HTML rebuild was attempted first and abandoned: the title face measures 3.72
width-per-cap and every heavy Didone on Google Fonts sits between 5.2 and 5.7, so matching it
would have meant the synthetic-width distortion his own cover rules ban.

The front art is 1024 × 1536. That clears KDP's ebook minimum but sits under the 1800 × 2700 a
6 × 9 print cover needs at 300 dpi, so the display letters are soft under a magnifier at print
size. Regenerate the source art at 2× before publishing the print editions.

**The free prompt page stays off the cover.** He put it plainly: if people can read the link
they have no reason to buy. The back cover promises the free page and the address lives in
Appendix A behind a QR code. KDP would have allowed the URL — their ebook cover "must not" list
holds only two items, copyright infringement and any mention of pricing or a temporary
promotion — so this was a commercial call rather than a compliance one.

## Published — the Kindle went live on 27 August 2026

The book has a listing at last. The Kindle edition is live at ASIN `B0HGQ35XP9` and sells for
$4.99. The paperback and the hardcover were still marked "In review" on his KDP bookshelf that
afternoon. Everything written above this section about the book being unpublished is out of date.

Three builds landed that day. v7 was the 201-page interior with the Start Here table, the decision
tree, the Chapter 1 interface guide, the BUILD THIS boxes and the thirty-day roadmap as Chapter 19.
v8 numbered the rows of the Chapter 1 screen table 1 to 6 so they match the labels printed on the
figure, because the table and the figure had been describing the same six things without a shared
numbering. v9 added one fact to Chapter 1: Claude Code needs a paid Pro or Max plan and has no free
tier. Upload v9.

He asked for a badge in one corner of the Kindle cover reading "Free Online Prompt Library". It
ships top right, as a tilted orange tab in the cream strip above the title. Top right is the only
corner the halftone dot fields leave clear. The badge names the offer and does not print the
address, so the rule above still holds: the URL stays in Appendix A. Both compliance questions were
checked against KDP's own pages that day. The badge is neither a price nor a temporary promotion,
and KDP's Hyperlink Guidelines list links to ancillary material as permitted, which puts the
in-book link on firmer ground than the badge.

Three cover faults surfaced in review and all three are fixed. The spine had been reading "JADHAV"
on its own, which breaks his one-line name rule, so both wraps now read `CLAUDE CODE FOR FINANCE —
TEJAS JADHAV, CFA, FRM` behind a shrink-to-fit guard. The hardcover back text was too light and its
body weight went from 400 to 540. Darker type sets wider, so the same point sizes wrapped onto more
lines and pushed the text column into KDP's barcode box, and the sizes and leading had to come back
down. Example: after the fix the last line of back-cover text sits 1.79 inches above the bottom on
the paperback and 2.20 inches on the hardcover, and KDP's barcode box is 2 by 1.2 inches. The byline
overflow he screenshotted came from the source art, whose byline span is asymmetric at 72 pixels
left and 28 right, so centring it in the fit box put the M of FRM on the trim guide.

The Kindle cover file is `Claude Code for Finance - kindle cover 800dpi.jpg` at 2560 × 3840 pixels
and 1.45 MB. The subtitle reads the same on the cover art, the interior title page and the metadata
field, because KDP treats a cover that contradicts the detail page as a rejection trigger. Ads for
the title are on [[amazon-ads]], and the keyword work is on [[kdp-listing-operations]].

The print editions went live on 2026-08-28, the paperback at 24.99 dollars and the hardcover at
44.99, and both now show as format swatches beside the Kindle on the detail page. They were attached
to the auto ad campaign the same day. See [[amazon-ads]] for that, and for the account balance
alert that is currently stopping every one of his campaigns from delivering.
