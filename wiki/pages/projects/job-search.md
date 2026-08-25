---
title: The job search — routines, volumes, and the interview guides
type: project
tags: [job-search, naukri, linkedin, interview, business-analyst, product-owner]
created: 2026-08-25
updated: 2026-08-25
sources: [~/files/HANDOFF-naukri-daily.md, ~/files/HANDOFF-remote-jobs.md, ~/files/.claude/worktrees/brave-wilson-299feb/HANDOFF-tiaa-interview.md, ~/files/.claude/worktrees/swiggy-financial-analysis-7412fb/HANDOFF-ba-po-interview-guide.md]
---

[[tejas-jadhav]] is running a business analyst and product owner search alongside an accepted
Accenture offer that starts on 7 September 2026. He wants to beat that offer, so the search
continues. The target is capital markets work in Pune or fully remote.

## Three routines run every morning

They must not tread on each other, and they run in this order. At 9:08 the
`naukri-daily-refresh` routine bumps his profile so recruiters see him first. At 9:35
`daily-job-applications` works LinkedIn Easy Apply and the global ATS boards. At 10:12
`naukri-bulk-apply` carries the volume, because LinkedIn caps Easy Apply near one submission a
day now.

**The Naukri target is 30 to 40 a day and the pool does not support it.** On 25 August 2026 the
routine applied to 18 and the running Naukri total reached 91. About seven postings in ten were
external "Apply on company site", which the routine cannot drive. Twelve more native postings
were abandoned at the recruiter chatbot, because the first question asked for years in a domain
he has never worked in — workforce management, contact centre, card issuing, property and
casualty insurance, Microsoft Fabric, Workato, C#. Abandoning is the correct move there.
Answering would have meant inventing a number, which [[voice-pass]]'s sibling rule on résumés
forbids outright.

Two mechanics are worth carrying into the next run. A Naukri job page resolves from its ID
alone at `naukri.com/job-listings-j-<jobid>`, so a whole run can be driven from a list of IDs
without searching again. And `experience=` is silently dropped from a search URL, the same way
`ctcFilter=` is, so neither can be trusted as a filter. Pull the results and filter them in
code.

## Two interview guides, both built 25 August 2026

The general one is `~/Downloads/Tejas Jadhav_BA and PO Interview Guide.pdf`, 68 pages and 70
questions, with a question index on page 1 so he can revise from the questions and drop into
the explanation only where he needs it. It covers requirement gathering, elicitation, the
ceremonies, refinement versus grooming, t-shirt sizing, RAID, product vision against product
roadmap with samples, the requirements traceability matrix, and the API terms a business
analyst is expected to know. A whole section answers a wealth-management job description: a fit
map marking every line strong, partial or gap, his eight gaps with an honest line for each, a
domain crib, and seven SQL and API questions with runnable queries.

The role-specific one is `~/Downloads/Tejas Jadhav_TIAA Associate Director Product
Management_Interview Guide.pdf`, 40 pages, for a TIAA Mumbai Associate Director role in
product management. It covers TIAA and Nuveen, private credit, leveraged loans, CLO coverage
tests and waterfalls, ABOR against IBOR against PBOR, the end-of-day and start-of-day
sequence, attribution, the product craft, the analyst toolkit, a Snowflake primer, fund
accounting and the private fund lifecycle, and credit vocabulary.

## Research the named panelist before writing the guide

This is the reusable part. The TIAA guide was built after reading the panelist's live LinkedIn
profile in his own Chrome, not from the advert alone, and that read changed the guide twice
over. The panelist had personally implemented Eagle Accounting, Bloomberg PORT+ and FactSet
SPAR, so those three platforms went onto a never-claim list. He had also come up through
operations into product, so the guide weights lifecycle detail over product theory. Do the same
on every future interview guide. Find the panelist, read what they have actually done, and let
that set both the never-claim list and the emphasis.

Both guides state every gap as a gap and give him a scripted honest line for it. The worked case
studies carry teaching numbers rather than his project metrics, and that caveat travels with
the files.
