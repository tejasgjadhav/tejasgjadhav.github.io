---
title: Amazon Ads — Sponsored Products for the flagship Claude-finance book
type: project
tags: [kdp, amazon, advertising, marketing]
created: 2026-07-20
updated: 2026-08-29
sources: [~/files/HANDOFF-amazon-ads.md]
---

Amazon Advertising (Sponsored Products) campaign on [[tejas-jadhav]]'s flagship KDP title
**"Claude AI for Finance Professionals"** (see [[kdp-books]]) — campaign
`A08827853M0646XUVFNUL`, entity `ENTITY2H0HGLW74CYKG`. Working state, bid table and watch-items
live in `~/files/HANDOFF-amazon-ads.md`. Rank feedback comes from the [[kdp-dashboard]].

**The recurring failure mode: underspend from bids set too low.** On 2026-07-20 the campaign spent
only ~$3.79/day (568 impressions) against a **$10/day budget** (~$7.48/day the prior week). Root
cause was low bids strangling volume, not the budget. **Through-line lesson: cutting bids to fix
ACOS quietly kills impressions and sales** — on profitable, low-ACOS keywords the right move is to
*raise* bids.

**Bids raised (2026-07-20)** on the winners: `claude ai for investment bankers` (drove a $93.96
sale) $0.90→$1.50; `claude ai made easy` (3.4% ACOS) and `claude ai manual` (4.2%) →$1.50;
`using claude for investing` (5.7%) →$1.50; `claude ai for finance professionals` →$1.20;
`claude ai`/`claude for finance` →$1.10; broad `claude` (discovery) →$1.00. Left at the floor
(at/above break-even): `claude finance`, `ai finance`, `ai finance books`.

**Deciding diagnostic:** recheck daily spend 3–4 days after a bid raise. If it climbs toward
$9–10/day, bids were the bottleneck. **If it stays stuck under ~$6/day despite much higher bids,
the block is the India account-balance alert throttling delivery** — a payment/settings matter only
the user can clear; no bid change fixes it.

## 2026-08-13 — the August sales slide, diagnosed against his own rank history

Royalties ran about $1,800 in June, about $1,600 in July, and about $500 across the first 13 days
of August. He asked why, and the [[kdp-dashboard]] answers it: the decline came in two phases and
neither of them is a keyword problem.

1. **Kindle slid in early July, before any metadata changed.** June's median rank was about 61,000.
   The first week of July it jumped to about 115,000 and stayed in the 95,000 to 138,000 band all
   month. That is the new-release halo expiring, since Amazon boosts a title for roughly 60 to 90
   days, plus the competing Claude titles arriving on the shelf. This part was coming regardless.
2. **The paperback, which is the revenue engine, broke in the Jul 29–31 window.** It held June-level
   ranks of 60,000 to 80,000 through Jul 27, then went to 118,708 on Jul 29 and 143,966 on Jul 31.
   That is the long-keyword set going live plus a Jul-28 manuscript re-upload triggering another
   review. The revert stopped the bleeding and the rank never recovered; August sits around 97,000
   to 115,000.

Ranks 1.5 to 2 times worse across both formats matches $60 a day in June falling to about $38 a
day, so the arithmetic closes. **The lever is velocity and reviews, not metadata.** Churning
keywords is what caused the damage, so the correct move after the pending swaps is to freeze them.
The campaign converts at about 32% ACOS, so running the flagship nearer $10 a day and accepting
roughly break-even ads for three or four weeks is what buys back the sales that rebuild rank.

The keyword evidence method that came out of the same session is on [[kdp-listing-operations]].

## A second campaign, for the beginners book (2026-08-21)

A separate campaign now runs for [[claude-beginners-book]] at two dollars a day, in the United
States, on manual targeting with dynamic bids set to go down only. One ad group carries all three
formats at their live listing prices, which are cheaper on Kindle and paperback and dearer on
hardcover than the listing plan recommended. Ten keywords all sit at the sixty-cent account floor and
all are exact match, drawn from his own title, which is now a live Amazon autocomplete term, from a
term that converted twice on the flagship, and from the probe-verified corpus. Four phrase negatives
keep out free, pdf, course and download.

The economics say plainly what this campaign is. Paperback royalty is about four and a half dollars,
Kindle royalty is around a dollar on a large file, and break-even cost per click at a ten to twelve
percent conversion rate is roughly half of what the floor bid costs. The floor therefore sits
slightly above break-even unless hardcover sales mix in, which makes this a purchase of velocity
rather than a profit engine. The kill trigger is the same as the other small tests: a hundred clicks
with fewer than two orders means pause it and move the budget back to the flagship. Committed daily
spend across seven campaigns is now about twenty-four dollars, and actual spend has historically run
at half to sixty percent of the cap.

One interface trap is worth recording, because it costs a launch. In the campaign builder, editing a
bid inside the added-keywords table does not commit. The new value appears, the accessibility
attribute updates, and then the row reverts to the enter-list bid as soon as another row is clicked.
The enter-list custom bid is the one that sticks. To give keywords different bids, launch them flat
and change them afterwards from the campaign's targeting tab.

Part of [[files-repo]].

## A third campaign, on the day the Claude Code book went live (27 August 2026)

He asked for a three-dollar campaign as soon as the book had a listing. It launched and Amazon
confirmed it on screen. The campaign is named "Claude Code Finance - Auto - Aug 2026" and it runs
US Sponsored Products with automatic targeting, dynamic bids up and down, a default bid of
seventy-five cents, a three-dollar daily budget and no end date.

Automatic targeting was chosen deliberately. A book on its first day has no search-term data, so the
auto campaign generates that data and the terms that win become a manual campaign later.

The campaign advertises the Kindle edition alone, and that was a constraint rather than a choice.
The product picker in the ads console returned exactly one result, because the paperback and the
hardcover were still in review on his bookshelf, and the console can only attach an ASIN that is
live. He made the point that the paperback is the better vehicle, and he is right. A paperback
royalty per conversion is several times a Kindle royalty, so it absorbs the ad cost far better.
Attach the paperback to this campaign as soon as it clears review.

Committed daily spend across eight campaigns is now about twenty-seven dollars. See
[[claude-code-finance-book]] for the title itself.

## The print editions attached, and then every campaign stopped

A scheduled routine watched the detail page and acted the morning the print formats appeared. On
2026-08-28 all three formats were live: the Kindle at 4.99 dollars, the paperback at 24.99 and the
hardcover at 44.99. Both print ASINs went into the auto campaign's single ad group, and a fresh page
load confirms three products in it. The Kindle ad reads Delivering and the two print ads read
Pending review, which is the normal state for a new ad. Nothing else was touched, so the budget
stays at three dollars a day and the targeting stays automatic.

The same console now shows a red banner across every campaign, saying the campaigns have stopped
delivering because of insufficient balance and asking him to add balance to his India account. That
turns the balance alert from a throttle into a hard stop. **Check that banner before diagnosing any
underspend as a bid problem**, because the July diagnosis on this page assumes delivery is possible
at all.
