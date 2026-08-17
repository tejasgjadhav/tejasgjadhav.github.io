---
title: Book covers — the pipeline, the click test, and the shelf they sell on
type: concept
tags: [kdp, covers, design, amazon, compliance]
created: 2026-08-11
updated: 2026-08-16
sources: [~/.claude/CLAUDE.md, ~/files/kdp-books/claude-cowork-finance/cover/]
---

How covers for [[tejas-jadhav]]'s KDP titles get made, settled over ten rounds on the
**Claude Cowork for Finance** cover on 2026-08-11. The catalog itself is [[kdp-books]] and the
listing side is [[kdp-listing-operations]].

## Three agents, and only the last one can block

A panel of critics second-guessing a cover is the wrong structure, because it argues about taste
instead of fixing the design. The pipeline is now a sequence.

1. **The designer** returns a specification and never writes the final file. The spec carries exact
   type sizes, exact colour values, exact spacing, the geometry of any drawn device, and what it
   deliberately left out.
2. **The executor** builds that spec in HTML and CSS, renders it with headless Chrome, and verifies
   its own work in pixels. It samples the image to confirm the ink edges land where the spec says
   they land. It does not redesign, and it reports any place it had to deviate.
3. **The compliance gate** is the only reviewer with a veto. It runs every claim on the cover
   against the manuscript, checks counts, third-party names, confidentiality, credentials, rank
   claims and spine width, and it also checks that the cover does not read as machine-made.

The gate earned its place on the first run. It caught a `border` declared on both `html` and
`body`, which shifted the whole design by 32 pixels and painted the footer over the frame. A design
review would have called that cover fine.

## The click test comes before the craft test

A cover has one job. A person scrolling past it stops, wants to know more, and taps. So the first
question is what survives at a phone thumbnail about 160 pixels tall, and the second is whether
what survives makes a stranger curious. A category label such as "AI for finance" is a shelf, not a
reason to tap.

Two rules follow from that. **The front cover carries outcomes, never inventory.** A buyer does not
buy 13 chapters or 148 pages, so the counts belong in the description and on the back cover where a
considering buyer looks for specs. **A cover device must not frame the whole book as one worked
example.** A schedule rail was the strongest of five rounds and it still died, because a single
named routine tells the buyer the book is only that routine.

## Match the product's register, never its mark

Every Claude title ranking on Amazon on 2026-08-11 sat on a warm cream ground with a clay accent
and a serif title. Colour and typeface are not trademarks, so copying that register is fair and it
is what earns recognition in one glance. Two of those covers print Anthropic's starburst and one
prints "ANTHROPIC" as a corner badge, which is a trademark exposure and a takedown risk however
well it sells. The line sits exactly there: register yes, mark never. See [[claude-anthropic]].

The shipped Cowork cover, J, nudges the palette off Anthropic's published values on purpose. The
ground is `#F3EEE4` rather than `#F0EEE6` and the accent is `#CE6440` rather than `#D97757`.
Perceptually it is the same family, so nothing is lost in recognition, and the cover no longer
wears their exact trade dress directly above a notice saying it is not affiliated with them. The
nudge also lifted the title's contrast against the ground from 2.69:1 to 3.29:1.

## The byline is a selling point, so it is set like one

The name reads `TEJAS JADHAV, CFA, FRM` on one line, never wrapped, with the post-nominals
attached. It sits in the accent colour on the white author band, large enough to read on a phone,
and it is checked at a 280-pixel render because that is roughly the Amazon product-page size on a
phone. On cover J it measures 4.53:1 against white, which clears the standard for body text and not
merely for large text. The disclaimer under it does not carry the accent colour.

## Dimensions come from KDP's calculator

KDP publishes the paperback cover formula and does not publish the hardcover one, so the Cover
Calculator is the only authority for hardcover. Measured for this book: paperback at 114 pages is
12.507 by 9.25 inches with a 0.257-inch spine, and hardcover at 120 pages is 14.034 by 10.417
inches with a 0.459-inch spine, a 0.591-inch wrap and a 0.394-inch hinge. The barcode zone is 2 by
1.2 inches of solid white, at least 0.25 inches clear of both the spine and the trim, in whichever
corner you choose. Lay the back-cover copy out around it rather than trimming copy after a
rejection.

## The no-template checklist

A cover that reads as generated is a commercial defect, so the gate also rejects the house style of
machine-made covers. No letter-spaced all-caps eyebrow above the title. No three-item all-caps list
with square bullets. No trust bar of specs separated by dots. No stack of full-width bands where
nothing crosses a boundary. No single accent colour doing six unrelated jobs. No one typeface at
every size. No synthetic weight or width distortion to force a line to fit. And no cover that
asserts its own honesty, because "real screenshots" reads as defensive.

Fonts are sourced for the design rather than chosen from what is installed, under a licence that
permits commercial use — SIL OFL, Apache 2.0 or public domain. The handover names the fonts and
their licence.

## Resembling a competitor: the risk is Amazon, not a court (2026-08-16)

Settled while checking the [[claude-beginners-book]] cover against a ranking competitor's in the
same category. **Copyright protects a specific expression, not a look.** A cream ground, an
orange accent, halftone dots, a large serif title, a numbered feature strip and a byline at the
foot are conventions running through most covers in that category, typefaces are not
copyrightable in the US, and colours are not ownable. That is the same reasoning that already
licenses copying the ranking Claude register.

**The realistic exposure is a rights complaint, which can suspend a listing without any court
involved**, and the argument back happens while sales stop. So separate on the distinctive
devices and keep the functional ones. A competitor's signature badge — its shape, its corner,
its two-tier number setting — is the most identifying element, and changing or dropping it does
most of the work. A shared decorative motif should differ in count or grade so the two separate
at thumbnail, which is where a buyer would confuse them. A feature strip listing the book's own
verified contents is functional rather than decorative, and that is the strongest position to
hold if anyone asks.

**Scan supplied artwork for accidental lookalike marks.** A cover file he generated himself
carried a small fan-shaped ornament above the byline that read as a miniature Anthropic
starburst. Removing it mattered more than the overall resemblance did, because a small lookalike
of the mark is what turns a style question into a trademark one. See [[claude-anthropic]].

## Building from supplied artwork

**Report the effective print resolution before building the wrap.** A 1023 px source blown up to
the 1875 px a 6×9 bleed needs at 300 DPI lands at an effective 164 DPI. KDP accepts it and prints
it, and large serif edges come out softer than they look on screen. Kindle needs a much smaller
lift and is unaffected. The honest options are to regenerate the source larger or to use a real
300 DPI rebuild for print and the supplied file for Kindle.

**Check the back panel with your eyes, because the geometry gates cannot see it.** One wrap build
mirrored the front artwork underneath the back text — reversed title, flipped badge, upside-down
labels — with the description printed straight over it. Every gate passed.

**A large canvas has to be rendered in bands on 8 GB of RAM.** An 800 DPI cover is roughly 77
megapixels and headless Chrome returns a blank screenshot or dies on a single surface that size.
Render horizontal bands and stitch, then prove the joins three ways: align a downscale of the
large file against the known-good 300 DPI render on a ±2 px grid and confirm it minimises at
(0,0), run a numeric row-difference scan, and crop the flagged rows at full resolution, because a
seam that lands on a line of glyphs flags every time and is a false positive. Re-measure safe
margins on the large file directly rather than scaling them from the small one.

**KDP's own spec is 300 DPI and PDF is their preferred print-cover format.** An 800 DPI JPEG buys
nothing for a KDP upload and is the right file only when a different printer or distributor asks
for raster.
