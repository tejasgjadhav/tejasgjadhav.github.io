---
title: AIFINANCE — landing page
type: project
tags: [personal-site, seo, landing-page]
created: 2026-07-05
updated: 2026-08-09
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

Part of [[files-repo]].
