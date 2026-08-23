---
title: AIFINANCE — landing page
type: project
tags: [personal-site, seo, landing-page]
created: 2026-07-05
updated: 2026-08-23
sources: [~/files/aifinance, https://github.com/tejasgjadhav/AIFINANCE]
---

A landing page for [[tejas-jadhav]]'s AI-in-finance work. Own repo
`github.com/tejasgjadhav/AIFINANCE`, deployed via GitHub Pages at
`tejasgjadhav.github.io/AIFINANCE`. `gh` CLI is not installed on this machine, so PRs on
this repo must be merged locally via git rather than `gh pr create`.

Design/accessibility pass (2026-07-04) using the `ui-ux-pro-max` skill: fixed
`prefers-reduced-motion` support, made the accordion keyboard-accessible, added focus
rings, a skip link, and SEO/OG meta. A later visual pass replaced ~40 emoji icons with a
24-icon custom SVG sprite system plus motion polish (spring easing, sheen sweep). Shares
the site's canonical portrait and Person schema `@id` (`#person`) with the root site for
Knowledge Panel entity merging — see [[tejas-jadhav]].

**Course site** (as of 2026-08): the page now carries [[tejas-jadhav]]'s ISBMS PGDM
Sem-III elective, *Agentic AI & Advanced Analytics in Finance* — 30 hours, ten 3-hour
modules, first class 8 August 2026. The institute's session-plan PDF is the binding source
for module content; module cards mirror it rather than being free-written, and one slide
deck per module lives in `slides/`, linked from "Class Materials". A factual catch: the
plan's Module 6 case cites a ₹1,000 crore RBI penalty on HDFC Bank that does not exist, so
the site runs that case without the figure.

Module 1 shipped as *Foundations of Agentic AI*: what a transformer is, gen AI vs AI agent
vs agentic AI, and the [[jarvis]] orchestration flow chart (with its real agent names) as
the worked example of agentic orchestration. The lab is deliberately keyless — students
have no Claude subscription, so practice runs on free tools. An early Colab notebook was
dropped because it did not actually demonstrate Codex; the replacement has students pull a
share price, revenue and P&L in plain Python, then do the same through Codex, and compare
scale and lines of code. Deck house style follows [[scmhrd-ai-finance]]: 20 slides
max, last slides are practice questions.

Module 2 shipped on 21 August 2026 as *Prompt Engineering and RAG*, in twelve slides. It keeps the
Module 1 design system, which is a navy and gold palette with Georgia titles and a tip answer printed
under every practice question. Two slides were rebuilt at [[tejas-jadhav]]'s instruction. The
hallucination slide now runs in three parts: what a hallucination is, then the question that was
actually answered wrong, which is Bard's James Webb exoplanet claim from February 2023, then the
types with an example each. A new slide explains what RAG is before the pipeline slide appears: the
full form, then retrieve, augment and generate one at a time, with the classroom analogy that a plain
chatbot sits a closed-book exam while a RAG bot sits an open-book exam and writes the page number in
the margin. The techniques slide was later simplified so that re-ranking reads as shortlist then
interview, and self-consistency reads as three analysts computing one ratio.

Two production notes came out of building it. Once he has edited a deck himself, his copy in the
Downloads folder is the source of truth and gets edited in place, which is the same rule
[[scmhrd-ai-finance]] follows. And Keynote silently refuses to open a deck that python-pptx wrote
speaker notes into, with no window and no error, so teaching notes ship as a separate one-page PDF
instead of inside the file.

The RAG half of this module now has a worked build behind it in
[[shiprocket-dhrp-rag]], which runs the same pipeline over a real SEBI prospectus with no API key.

Part of [[files-repo]].
