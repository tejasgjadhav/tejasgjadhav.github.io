---
title: Amazon Ads — Sponsored Products for the flagship Claude-finance book
type: project
tags: [kdp, amazon, advertising, marketing]
created: 2026-07-20
updated: 2026-08-13
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

Part of [[files-repo]].
