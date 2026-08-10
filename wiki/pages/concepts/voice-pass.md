---
title: The voice pass — the grammar gate every piece of his prose goes through
type: concept
tags: [writing, books, kdp, voice, editing]
created: 2026-08-10
updated: 2026-08-10
sources: [~/.claude/CLAUDE.md, ~/.claude/skills/humanizer/SKILL.md]
---

On 2026-08-10 [[tejas-jadhav]] made the voice pass a standing gate. No prose written in his name
ships until it has been read sentence by sentence. It covers every book, chapter, article, blog
post, KDP asset, post and note. Code comments, commit messages and machine output are out of
scope, and legal or disclaimer wording is exempt.

## The gate is grammatical, not cosmetic

Removing metaphors, em dashes and kill-list words is not the voice pass. That was the mistake on
the Cowork book, which passed every automated check and he still rejected it, because nobody had
read it sentence by sentence. **Grep cannot find a fragment.** Each sentence gets two questions:
does it have a subject and a verb, and does it carry exactly one fact?

His own example is the calibration. This was rejected:

> The tools are public and running. A market dashboard that rebuilds itself every weekday, an
> in-browser portfolio analyser, and a paper-trading signal system.

This is what it should have said:

> This book features tools that are public on a GitHub repo. Example: we have a market dashboard
> that autoupdates itself with the latest news each morning, before we log in to markets.

Five things changed. Every sentence has a subject and a verb. It names the concrete place, a
GitHub repo. It signposts the example with the word "Example:" instead of implying it. It anchors
the benefit to a real moment in his day. It uses a plain verb, "autoupdates itself", in place of a
writerly one.

## Polish, but never the AI feel

A full voice pass over the Cowork book stripped fifteen sharp lines out of it, and the book got
flatter. Two other models preferred the unedited version. Over-sanitised prose is itself the AI
feel, so the two rules are resolved this way. The fragment ban always wins: no verbless sentences,
no caption lists standing in for prose, no staccato two-word sentences for effect. The aphorism
ban is narrower than it reads: a sharp line that is a complete sentence carrying one fact is his
voice and it stays. What the ban actually targets is a decorative simile standing in for a point
rather than making it.

Ten lines were restored into the Cowork book on that basis, and three were deliberately left out
because they are staccato fragments. **Uniformity is the real tell**, not personality — identical
chapter openers, the same section skeleton every time, the same connective phrase forty times.

## The humanizer skill now defers to this

The `humanizer` skill was written for the 2023 anti-AI register: use fragments deliberately, vary
sentence length dramatically, open with a hook, reach for everyday analogies. By 2026 that is the
register every model produces when asked to sound human, so four of its five core rules were
reintroducing the exact defects this gate exists to catch. It was rewritten on 2026-08-10 to say
that the voice pass governs and wins any conflict. It stays useful for structure — cutting
throat-clearing openers, deleting "in this chapter we will explore", cutting 10% from every draft
— and it is no longer the authority on voice.

The same pass set the default audience to the United States, since that is about 80% of his
readership: dollars, the S&P 500, the SEC and FINRA, 401(k)s and IRAs, and no lakh, crore or
regional-language phrases. India is the stated exception, and a book serving both markets writes
the US version as the main text with India in a marked translation table, the pattern
[[claude-algo-trading-book]] already uses.

Applies to everything in [[kdp-books]], and hardest to the Amazon preview zone — the front matter
and first chapters that "Look Inside" shows on all three format listings. The listing side of the
same discipline lives in [[kdp-listing-operations]].
