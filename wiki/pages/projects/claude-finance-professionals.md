---
title: Claude AI for Finance Professionals — the flagship book
type: project
tags: [kdp, books, writing, claude, finance, prompts]
created: 2026-08-26
updated: 2026-08-26
sources: [~/files/kdp-books/claude-finance-professionals/, ~/files/claude-finance-prompts/]
---

This is [[tejas-jadhav]]'s featured KDP title and the flagship of his series. It has been on
Kindle since March 2026 at $5.99, and the catalogue entry sits on [[kdp-books]]. The source lives
at `~/files/kdp-books/claude-finance-professionals`.

**As of 26 August 2026 the book is 205 pages and carries 122 prompts.** The spine works out to
0.4617 inches, which is exactly what the earlier cover wrap was cut for, so the covers did not have
to change. The upload files are in `~/Downloads`:
`Claude_AI_Finance_Professionals_FINAL_205pp_INTERIOR.pdf` is the KDP interior,
`..._FINAL_205pp_REVIEW.pdf` is a 19 MB reading copy that was verified page for page against it, and
`..._FINAL.epub` is the ebook. Every v17 through v20 file is superseded.

## One review started the rebuild

A customer called the book informative and well organised, and said it did not change how they work
with AI. He read that as the reader feeling the book was structurally the same thing over and over,
and he asked for the fix without touching the 122-prompt list.

## The repetition was counted rather than guessed

The source carried 307 repeated sentence instances inside the prompts. The 30-word standing
validation rule appeared 34 times across 13 chapters, the line telling the reader to run the
validation script appeared 13 times, and shared tone sentences accounted for 260. Each repeated
sentence is now wrapped in a span the stylesheets hide, and each desk carries one house-rules box
above its first prompt.

The prompts themselves did not change. `PROMPTS.md` was rebuilt from source and diffed after every
step, and it stayed byte-identical throughout, so anyone copying a prompt from the free web page
still gets the complete text.

## Chapter 1 now teaches the techniques it was already using

Anthropic's own guide names six techniques: clarity, examples, XML structure, role prompting,
thinking, and prompt chaining. He remembered four of them and asked for the rest. The new section
states measured facts about this book rather than general theory. Twenty-nine prompts already use
chain of thought and were never named as such. All 122 are zero-shot, and the book now says that is
deliberate and explains when a reader should write a worked example. No prompt uses XML tags,
because the CRAFT labels do that job. The four-layer desk is itself a chain, and the book had never
said so. Thirty technique notes sit in the chapters, and a one-page index called "Where Each
Technique Is Called Out" regenerates from them.

## The preview now opens on the two walkthroughs

He asked for the reorder and his own preview-zone rule supports it: the strongest differentiator
belongs inside the Look Inside sample. The differentiator here is the real runs. The order is How to
Use on page 6, the Introduction on page 8, "One by One Walkthrough with Claude Chat: Microsoft
Corporation" on page 9, the Claude Code backtest walkthrough on page 18, and Chapter 1 on page 23.

A browsing buyer now meets the line "Everything else in this book is illustrative. This chapter is
not" on page 9, with the real prompt screenshot underneath it. Before the reorder that sentence sat
behind fourteen pages of teaching prose, outside what most previews reach. The backtest walkthrough
ends by killing its own idea, which is the part no padded book would include. One trade-off travels
with the decision: the sample will now likely end inside the backtest, so a browser may never see a
desk chapter. The cover and the description sell the 122 prompts, and the preview's job is to prove
they are real.

He also asked for a reassurance line, and he was right to. His reorder put a dense institutional
prompt on page 9, which is the exact moment a beginner could decide the book is too advanced. The
chapter now opens by telling the reader not to worry about the prompt yet, because Chapter 1 teaches
it.

## The character stories were rewritten twice

The first pass rewrote all sixteen chapter resolutions so no two shared a shape, because ten of the
sixteen had contained "used Prompt N" and ten had pivoted on the word "because". That pass made them
denser and harder to read, and he rejected it.

The second pass put every opening and resolution into plain sequential English, and then translated
the jargon out of the stories themselves. "The US large-cap sleeve" became "the ten best US stocks
for the fund". "The correlation assumption" became "how closely stocks and bonds fall together".
"Precedent transactions" became "past deals used as price comparisons". The rule is that a story
carries no term it does not explain in the same breath. The technical vocabulary still lives in the
prompts, the framework tables and the glossary, because the prompts are the product and they stay
institutional. See [[voice-pass]].

## The prose cut was declined after measuring

He approved a 5 to 8 percent prose cut and the measurement argued against it. A near-duplicate scan
found five clusters above 72% similarity and three of those are house-rules boxes doing their job.
Cutting explanation out of a reference book leaves something denser and more clipped, which is what
dryness actually is. The rating track across the day ran 7 before the work, 7.5 after the repetition
pass, 8.5 after the chapter architecture, and 8.75 at the end.

## The free prompt site is not built from its repo

The prompt library at `https://tejasgjadhav.github.io/claude-finance-prompts/` and the repo at
`~/files/claude-finance-prompts` have diverged, and the repo holds the worse copy. The live page is
211,046 bytes in a green dark-mode design with sticky navigation and a search box. The local checkout
and the GitHub main branch both hold an older cream design at about 148,900 bytes. The live page was
deployed from somewhere else.

The repo's `PROMPTS.md` was also two prompts behind. Prompts 107 and 120 had lost their placeholders
in the tracked copy, and the live site and the book both carry the correct version. Both live files
were pulled into the repo and committed locally, and that commit was deliberately not pushed.
`build_site.py` still emits the old design, so regenerating the site from it and pushing would
downgrade the live page. Check the live bytes against the repo before touching that site.

The three-way check that proved the book, the QR code and the site agree is worth repeating on any
future edit. The QR on page 200 was regenerated from the URL with the same settings and compared byte
for byte, and `PROMPTS.md` rebuilt from the book source matched what the live site serves, all 122
prompts, with zero differing lines.

## Two build gotchas from the same day

EPUB XHTML predefines only five named entities, so `&middot;` used as a separator in 25 places failed
the QA parse. It would have failed KDP's conversion as well, not only the local build. Use the
numeric form.

Gemini reported that page 46 was truncated, and it was not. A `page-break-inside: avoid` rule had
pushed a whole sample-output block onto page 47 and left white space at the foot of 46. All 125
sample-output blocks were then checked line by line and every line was present. Gemini has made a
false truncation claim on his books once before, from reading a partial upload. Check the file before
acting on the claim.
