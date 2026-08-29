---
title: The job search — routines, volumes, and the interview guides
type: project
tags: [job-search, naukri, linkedin, interview, business-analyst, product-owner]
created: 2026-08-25
updated: 2026-08-29
sources: [~/files/HANDOFF-naukri-daily.md, ~/files/HANDOFF-remote-jobs.md, ~/files/.claude/worktrees/brave-wilson-299feb/HANDOFF-tiaa-interview.md, ~/files/.claude/worktrees/swiggy-financial-analysis-7412fb/HANDOFF-ba-po-interview-guide.md]
---

[[tejas-jadhav]] is running a business analyst and product owner search alongside an accepted
Accenture offer that starts on 7 September 2026. He wants to beat that offer, so the search
continues. The target is capital markets work in Pune or fully remote.

## Three routines run every morning

They must not tread on each other, and they run in this order. At 9:08 the
`naukri-daily-refresh` routine bumps his profile so recruiters see him first. At 9:35
`daily-job-applications` works LinkedIn Easy Apply and the global ATS boards. At 10:12
`naukri-bulk-apply` carries the volume. LinkedIn's Easy Apply throttle has moved twice: it allowed
three a day on 11 August, fell to one on 17 August, and allowed ten again on 26 August.

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


## 148 applications as of 26 August 2026

Ten went out on 26 August, all through LinkedIn Easy Apply in his own Chrome profile, taking the
running total to 148. Three are worth watching. Luxoft is hiring a business analyst for trade and
transaction reporting in Pune District, which is daily OTC derivative reporting across jurisdictions
and is his delivery lane exactly. MyRemoteTeam posted a capital markets business analyst covering
equities, fixed income and securities lending, and the application went in four minutes after the
posting appeared. Double Duty Money Management, a New York boutique, is hiring a senior investment
operations analyst fully remote from India, and the founder is listed as the poster.

Two questions are open and only he can answer them. Double Duty asked whether he has completed an
MBA, and LinkedIn had pre-filled Yes. The answer was changed to No, because his degree is an MMS. He
should decide once whether he wants that answered Yes on the grounds that the MMS is a two-year
AICTE postgraduate management degree. Separately, four strong roles were skipped only for being
contracts, and two of them were the best domain matches of the whole sweep.

His LinkedIn profile still pre-fills wrong numbers into Easy Apply forms. This run offered thirteen
years in Office and twelve in investment banking, and each one was corrected by hand to his standing
figures of twelve years total and ten in financial services.

Two mechanics make the next run cheaper. Read the job description out of `document.body.innerText`
after a scroll, so triage costs one JavaScript call and no screenshot. And each click on Easy Apply
toggles the modal, so firing two clicks in one batch opens it and closes it again.

## Where the counters stand on 27 August 2026

The LinkedIn and global channel reached 158 applications. Ten went out that morning, numbered 149 to
158, and every one was confirmed. The best domain fits of the batch were Luxoft's Senior Business
Analyst for capital markets, covering OTC derivative clearing, interest-rate derivatives and fixed
income on an India-remote basis, and METRO Global Solution Center's AI Business Analyst in Pune. Ten
a day is now the working rate.

The Naukri channel reached 152. That day's run submitted 34 applications, inside its 30 to 40 target
band. The best fits were two Infosys roles in Pune, an AML Operations Functional SME and a KYC and
CDD Functional SME, plus an asset management and performance attribution lead at Crescendo Global.

Two corrections to his work history landed the same day and both change every CV. He is Lead
Business Analyst on the UBS OnePass data platform and not its owner, so "Product Owner" must never
appear against UBS. The Product Owner title with the team of eight belongs to the CETF programme at
Credit Suisse. And he worked entirely in Pune. Only Perfect Engineering Works is Satara, and Mumbai
now appears on no employment line at all. SIMSREE stays Mumbai in the education block, because the
institute is there. All 22 CVs in his Downloads folder were swept that day.

His final round at TIAA for Associate Director, Product Management is with a panelist named Bharath,
and reading that panelist's LinkedIn changed the preparation. Bharath is not an investments person.
He came up as an Infosys developer, led an implementation at Alliance Global, and has spent seven
years in product. So the second guide, 38 pages and separate from the first so it can be carried
alone, covers Python basics, the business-analyst work on a legacy-application migration, and
questions on operational stability, integration and generating custom reports. That matches the role
itself, which exists to build a data store for credit products.

One answer was scripted with him. Asked whether he has built a data store, he says yes and then
draws the line himself in the same breath. He defined tables and loaded data into them alongside a
Palantir Foundry engineer, and he resolved MSCI vendor identifiers against the bank's own. That is
the business-analyst half of building a data store. Naming the half he did not do is what makes the
yes credible.

## Where the volumes stand on 28 August 2026

The LinkedIn and global ATS channel reached 168 applications. Ten went out that morning and all ten
were confirmed on screen. The best of them was a capital markets business analyst role covering
equities, fixed income and agency securities lending, which is his lane word for word and is India
remote. A core banking business analyst post at Intellect Design Arena in Pune came second, and an
institutional custody product manager role at Ceffu came third on level and money.

The Naukri channel reached 163, and that day's run submitted eleven rather than the usual thirty to
forty. The reason is that the native-apply pool was genuinely exhausted, because most of what
remained asks the candidate to apply on the company's own site. The number was logged as eleven
rather than padded. The best fit was a payments-domain business analyst covering SWIFT, SEPA and
UPI, in Pune.

Two mechanics are worth carrying into the next run. Numeric salary fields reject the shorthand, so
"33 LPA" fails and 3300000 works, and the same trap appeared on two different forms in two days.
And notice period in days is three while his last working day is 31 August, not the generic thirty
that a form invites. From 7 September that answer changes again to whatever Accenture's probation
clause says, so he needs to read the clause before he quotes a number.

## The TIAA final round happened

He sat the round on 2026-08-27. He was asked what a leveraged loan is and answered on high debt to
EBITDA. He was asked about CLOs and described a pool of leveraged loans with a waterfall running
senior to mezzanine to equity. The follow-up asked what a loan operations team actually needs, and
he answered with the data sources: the accounting book of record, document data, and valuation data
including SOFR pricing, so the desk can see repricings and amendments.

The close was neutral to positive. The panelist said he would make sure the first-round interviewer
sends his feedback and that he would submit his own, then that HR takes its own time. The first half
carries information, because someone who has decided against a candidate does not volunteer to chase
the other panelist. The second half is honest rather than a hedge. At a captive the panel recommends
and HR runs the requisition, the banding and the offer, so two to four weeks is the normal clock and
a written offer inside seven days is unlikely.

That collides with his Accenture start on 7 September. The move is one email to the recruiter rather
than a note to the panel. It states the start date as a fact, asks for the expected decision date,
and asks specifically whether a verbal confirmation is possible before then. A general request for
an update gets a general answer, and naming the verbal gives them something they can actually
deliver inside a week. Around 8 September there is a second legitimate touch, because he will have
joined and his notice period will have changed, and the recruiter should hold the correct figure.
