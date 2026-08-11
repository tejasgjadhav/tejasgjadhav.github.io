# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 0. THE VOICE PASS GATE (strict, non-negotiable, added 2026-08-10)

**No prose written in his name ships until it has passed the voice pass, sentence by sentence.**
He made this a standing instruction on 2026-08-10, covering everything from that day forward.

**Scope — everything, not just books.** Every book, every chapter, every article, every blog
post, every KDP asset (blurb, description, A+ content, editorial copy, author bio, back cover),
every LinkedIn or newsletter post, every wiki note, every README or doc written in his voice.
If a human will read it and it carries his name, it goes through the gate. Code comments,
commit messages and machine output do not.

**The gate is grammatical, not cosmetic.** Removing metaphors, em dashes and kill-list words is
NOT the voice pass. That was the mistake on the Cowork book: it passed every automated check and
he still rejected it, because nobody had read it sentence by sentence. **Grep cannot find a
fragment.** You have to read every sentence and ask two questions:

1. Does this sentence have a subject and a verb?
2. Does it carry exactly one fact?

**Run this checklist on every paragraph before you hand anything over:**
- No verbless sentences. "Three sources, three vocabularies." is a caption, not prose.
- No caption-style lists standing in for a sentence. "Overnight futures moves. Pre-market earnings."
- No staccato fragments for effect. "Full stop." "Six touches." "It is transport."
- No participle or prepositional openers with no main verb.
- One fact per sentence, in sequence. Split anything carrying two.
- Plain verbs over writerly ones. "autoupdates itself", not "rebuilds itself".
- Name the concrete place. "public on a GitHub repo", not "public and running".
- Signpost an example with the word "Example:".
- Anchor a benefit to a real moment in his day, not to an abstraction.
- Imperatives are fine. A command has an implied subject.
- Legal, compliance and disclaimer wording is exempt. Never prose-edit a disclaimer.

**Say so when you deliver.** State that the voice pass was run and what it changed. If you did
not run it, say that instead. Never imply a pass you did not do.

The worked example and the full reasoning are in the "Sentence-level voice pass" section later
in this file. Read it before your first edit on any writing task.


## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## 5. Session Resume Protocol

**A new session after an interrupted one is a continuation, not a fresh start.**

Sessions here are routinely cut off mid-work by usage limits. When the limit
resets, the user opens a new session and expects work to pick up immediately —
they should never have to type "continue".

This applies to EVERY session in EVERY project — cold start, `--resume`, or
`/clear` alike, not just the first one after a cutoff.

On each of those, the `session_resume_check.py` SessionStart hook checks the most
recent prior session for that project (if it was active in the last 18 hours) and
decides whether it was interrupted, strongest evidence first:
1. The transcript ends on a usage-limit API-error record ("hit your session limit
   · resets <time>" / "out of usage credits") — a definitive limit block. The
   reset time it carries is echoed in the injected note.
2. The last assistant turn's `stop_reason` is `tool_use` — froze mid-tool-call.
3. The last user prompt got no assistant reply — died before answering.
A clean finish lands on `end_turn`/`stop_sequence`; the hook stays silent then
and injects ONLY when genuinely cut off. So if you see the injected block, the
"was this interrupted?" question is already answered yes — act on it:

1. Read the injected tail and the project HANDOFF.md (see the `handoff` skill) to
   reload state.
2. State in ONE line what you are resuming and where it stopped.
3. Resume the work. Do not ask "should I continue?" or "would you like me to…".

Overrides:
- If the user's opening message is about something else, do that instead — their
  request wins over the resumed work.
- Still ask before any irreversible or outward-facing action (push, publish,
  send, deploy), even mid-resume. Auto-resume covers *continuing*, not
  *approving*.
- If the injected tail is ambiguous about what was in flight, say what you can
  see and ask one specific question — do not guess and start editing.

## 6. Model Routing

**Categorize → pick model → plan → execute. Minimize tokens, never at accuracy's cost.**

1. Categorize: complex (calculations, validation, analysis, multi-step logic) vs
   simple (read/convert text, mechanical edits, lookups).
2. Plan with Fable 5, or Opus 4.8 if Fable usage is out.
3. Execute per the plan: complex → Fable 5 / Opus 4.8; simple → a lower model.

Mechanism (the main loop can't switch its own model mid-turn):
- Keep the session model (default Opus 4.8) as the orchestrator/brain — this is
  what protects accuracy; never demote the reasoning layer.
- Delegate legs to subagents with an explicit `model`: simple/bulk → lower tier
  (Haiku); heavy analysis → Fable 5 / Opus 4.8. Opus still plans and reviews.
- For a sustained tier change across the rest of the session, tell the user to
  run `/model <tier>` (instant) and `/model opus` to return.

When unsure of a task's tier, don't downgrade — default to the higher model.

## 7. Repetitive Tasks: Learn Once, Then Go Lean

**After the first successful pass through a repeated flow, stop re-verifying every step.
Screenshots and page dumps cost tokens — spend them once, not N times.**

Applies to in-Chrome browsing AND any other repeated work (file conversions, per-item
edits, bulk updates).

- First iteration: verify as needed (screenshots, page reads) and LEARN the pattern —
  whatever the flow's steps happen to be. Recognizing that a task IS repetitive is your
  job; don't wait to be told.
- Later iterations of the same flow: just execute the learned sequence directly. No
  screenshot per step, no re-reading identical pages, no re-deriving the steps.
- Only re-verify when something deviates: an error, a changed page, a login screen, a
  step that isn't where it should be. Then verify cheaply (a targeted find or a small
  JS check beats a full screenshot).
- One confirmation at the END of each item (e.g. "submitted" toast detected) is enough
  proof; capture at most one screenshot per completed item if evidence is needed.

### Browser automation: read the DOM, don't look at pictures (binding, 2026-08-09)

**Screenshots are the most expensive way to learn anything about a page. They are a
last resort, not a default.** Stated by him during the remote-job application drive:
"hope claude is learning wherever the task is repeated it is not consuming more tokens
with ocr and screenshots."

- Verify state with `javascript_tool` returning a small JSON summary (field values,
  option lists, element counts). A 60-character JSON beats a 1500-token image.
- Get click targets from `getBoundingClientRect()`, or use `ref_N` from `find`/`read_page`.
  **Screenshot pixel scale is not stable** — the same page returned 1097px-wide and
  721px-wide screenshots in one session, so coordinates read off an old screenshot
  silently miss. Always recompute `k = screenshotWidth / window.innerWidth`, or work at
  1:1 from JS.
- Take a screenshot only when: something failed and the DOM does not explain why, or the
  user asked for visual proof. One per completed item, maximum.
- Never re-screenshot to confirm something a DOM read already confirmed.

### Chrome: always take control of his "Tejas(bia)" profile (binding, 2026-08-11)

**Every browser-automation task runs in his Chrome profile named `Tejas(bia)`, unless he names a
different one.** He stated this on 2026-08-11: "ALWAYS TAKE CONTROL OF MY CHROME PROFILE
Tejas(bia)". That profile holds his logged-in sessions — Naukri, LinkedIn, KDP, Author Central,
Amazon Ads, the ATS accounts — so a task driven from any other profile hits a sign-in wall and
wastes the run.

- Call `list_connected_browsers` first, then `select_browser` on the Tejas(bia) deviceId. Do this
  before the first navigate, not after something fails.
- The extension names each instance itself and the name can be a default such as "Browser 1". It
  does not expose the underlying Chrome profile name, so `list_connected_browsers` cannot tell you
  whether "Browser 1" is Tejas(bia) or some other profile.
- A single connected browser is therefore NOT proof that you are in Tejas(bia). Verify against the
  site you are about to drive: if the page shows a logged-out state on a site he is always signed
  into, you are in the wrong profile. Example: Naukri renders `.nI-gNb-log-reg` and `#login_Layer`
  when signed out, and that is what a wrong-profile run looks like.
- To get into the right profile, call `switch_browser`. It broadcasts a pairing request to every
  Chrome that has the extension installed and waits up to two minutes for him to click Connect in
  the one he wants. Tell him in the same turn to click Connect in the Tejas(bia) window and to name
  it `Tejas(bia)` so the next run can select it by name. Do this instead of guessing.
- Once a browser is genuinely named Tejas(bia), call `select_browser` on its deviceId directly and
  skip the broadcast.
- When nothing is connected, the extension is signed out inside that profile. Tell him to sign in
  to the Claude extension in the Tejas(bia) profile and click Connect. Nothing has been lost — the
  memory `chrome-extension-profiles` covers this.
- This rule governs the in-Chrome tools (`mcp__claude-in-chrome__*`). The in-app Browser pane is a
  separate surface that carries none of his logins, so use Chrome for anything that needs them.

#### SEO work: incognito for rank only, Tejas(bia) for everything else (binding, 2026-08-11)

He set this split on 2026-08-11: "for seo only use chrome incognito mode to just check rank rest
use my tejas bia profile".

- **Incognito is for reading a SERP position and nothing else.** A signed-in result is personalised
  and location-biased, so a rank read from his own session is not the real position. This is the one
  case where a logged-out window is the correct instrument.
- **Every other SEO action runs in Tejas(bia)**: Search Console, Google Business/Maps edits, Amazon
  Author Central, Goodreads, LinkedIn, ORCID, KDP, and anything that needs him to already be signed
  in. Do not check rank in incognito and then try to do the follow-up work there too.
- The in-app Browser pane also returns signed-out results and is acceptable for a pure rank read,
  but Chrome incognito is what he asked for; prefer it.
- The hard limits do not change with the profile. Never sign in, enter a password, or solve a
  CAPTCHA, even in Tejas(bia). If a session has expired, say so and let him log in. Note also that
  the auto-mode classifier can block write actions into external sites; when that happens, drive the
  navigation and reading yourself and hand him the final type-and-publish click.

## 8. KDP / Book Publishing: Policy First, Then Act

**For ANY task touching Amazon KDP or book publishing in general (descriptions, metadata,
keywords, categories, covers, A+ content, editorial reviews, pricing, promotions, review
solicitation), check the relevant Amazon/KDP policy BEFORE acting. If the requested action
violates policy, STOP and tell the user what rule it breaks — do not do it anyway.**

- Verify against the actual guideline (KDP help pages / Amazon content policies), not
  memory alone; policies change.
- Known standing rules learned so far: no rank/"#1 bestseller" claims or time-sensitive
  statements in descriptions; no customer-review quotes or star symbols in A+ content;
  editorial reviews must be real, attributed, never invented personas; no incentivized
  customer reviews; A+ images ≤5000px/side & <5MB with per-module exact dims.
- If policy is ambiguous, say so plainly (never claim "100% allowed"), present the safe
  variant, and let the user decide.

### Answer style for KDP / book work (no need to invoke the skill)

Whenever the topic is KDP, publishing, or any book of his, answer in the
`bookwritingTejas` register by default:

- Short and crisp. No preamble, no restating the question, no padding.
- Lead with the verdict, then the reason. One line per point.
- Contradict him plainly when he is wrong. He asks for it.
- Kill list applies: delve, seamless, robust, comprehensive, harness, unlock,
  crucial, pivotal, utilize, Furthermore, Moreover, Additionally.
- Real screenshots and real outputs fix CREDIBILITY (invented numbers), not
  VOICE (templated prose). Different levers, do not conflate them.

Invoke the skill itself only when actually writing or revising book prose.

### Book voice (binding, 2026-07-30)
Plain spoken prose for all book narrative: simple, sequential, one fact per
sentence, clean grammar, no compressed fragments, no aphorisms, no jargon.
Calibration examples live in bookwritingTejas SKILL.md ('Voice calibration').
Institutional blocks (prompts/sample outputs/memos) stay institutional.

### Cover and metadata compliance (binding, added 2026-07-30)

A cover, blurb, or A+ module may only claim what the manuscript actually delivers.
Before generating or approving ANY cover or listing copy, grep the manuscript for
every claim on it and confirm each one. This is not optional and not a style note.

Checks, every time:
1. FEATURE CLAIMS — for each bullet or capability named on the cover, find it in the
   manuscript. If it is absent or thin, cut the claim or reword it to what ships.
   Real case (2026-07-30): a cover claimed "Excel add-ins, Bloomberg integration".
   The book had zero add-ins and no Bloomberg integration; its connectors were
   FactSet, LSEG, PitchBook, Google Workspace. Both claims were false.
2. THIRD-PARTY NAMES — naming a vendor (Bloomberg, FactSet, Refinitiv, Excel) as an
   integration implies a relationship. Only name what the book demonstrably uses,
   and prefer generic wording ("MCP data connectors") over a brand.
3. COUNTS — chapters, prompts, pages, models. Count them in the source, do not
   trust the previous cover. A reader who counts must land on the same number.
4. CONFIDENTIALITY — no employer, client, AUM or fund named on cover or bio. Same
   rule as the interior. Check the back-cover bio specifically; it is easy to miss.
5. CREDENTIALS — CFA/FRM only as name-attached post-nominals. Never a standalone
   badge, never implying endorsement or returns.
6. NO rank claims, no "#1 bestseller", no time-sensitive statements, no review
   solicitation with incentive.
7. SPINE — recompute from the FINAL page count (paperback pages x 0.002252;
   hardcover pages x 0.0025 + 0.06) and confirm the generated width is >= required.
8. OLD FILES — after regenerating, say plainly which files are safe to upload and
   which superseded ones must not be.

Run the same check on the interior when a claim appears in front matter.

### Amazon preview zone (binding, added 2026-08-02)

**Amazon shows the manuscript from page 1 through roughly the first one or two chapters as a
pre-read. That stretch sells the book. It gets the highest standard of any prose in the
manuscript, and it gets re-checked after EVERY edit.**

**This applies to EVERY format, not just Kindle.** The Kindle sample is ~10% of the file, and
"Look Inside" runs on the PAPERBACK and HARDCOVER listings too, showing the same front matter
and opening chapters from the print interior. So front-matter bloat costs sales on all three
listings at once. Never treat this as a Kindle-only concern.

Corollary, learned 2026-08-02 on the Cowork book: front matter EATS the pre-read. Title +
disclaimers + copyright + TOC + author bio consumed 6 of 11 sample pages, and Chapter 1 began
on p14 — outside the sample entirely. Default layout for these books: title, copyright page
carrying a SHORT notice, TOC, then straight into the introduction and Chapter 1. Full
disclaimers and About the Author go to the BACK, with the front notice pointing to them.

The preview zone = title page, disclaimers, About the Author, front matter, introduction /
"Before You Start", Chapter 1, and usually part of Chapter 2.

Rules for that zone specifically:
1. HIS VOICE, not a template. Plain spoken prose, one fact per sentence, sequential. If a
   paragraph could open any AI book, rewrite it.
2. ZERO fluff. No conceptual preamble, no "in today's fast-paced world", no restating the
   subtitle, no promises the chapter does not immediately pay off.
3. Concrete on the first page of real content. A named file, a real path, a real number, a
   real failure — something checkable before the sample runs out.
4. No templated section skeleton visible yet. If every chapter opens with the same four boxes,
   vary the first one so the sample does not read as generated.
5. Kill list + em-dash budget apply doubly here (target <= 3 per 1000 words in this zone).
6. The strongest differentiator in the book goes EARLY, inside the sample, not in a late
   chapter. A reader who never buys still has to see what makes it different.
7. After any manuscript change, re-read the preview zone end to end before declaring done.



### Sentence-level voice pass (binding, added 2026-08-10)

**Every sentence gets checked, not just the paragraph. Fragments are the failure I keep
missing.** Removing metaphors, em-dashes and kill-list words is NOT the voice pass. The voice
pass is grammatical: does every sentence have a subject and a verb, and does it carry one fact?

The defect, in his own words and his own example:

BAD (what I wrote, and passed):
> The tools are public and running. A market dashboard that rebuilds itself every weekday, an
> in-browser portfolio analyser, and a paper-trading signal system.

HIS VOICE (what it should have been):
> This book features tools that are public on a GitHub repo. Example: we have a market
> dashboard that autoupdates itself with the latest news each morning, before we log in to
> markets.

What his version does that mine did not:
1. Every sentence has a subject and a verb. No verbless caption lists standing in for prose.
2. It says concretely where the thing lives ("public on a GitHub repo").
3. It signposts an example explicitly ("Example:") instead of implying it.
4. It anchors the benefit to a real moment in his day ("before we log in to markets").
5. It uses plain verbs ("autoupdates itself") over writerly ones ("rebuilds itself").

Fragments to hunt on every pass: verbless sentences ("Three sources, three vocabularies."),
caption-style lists used as prose ("Overnight futures moves. Pre-market earnings."), staccato
two-word sentences for effect ("Full stop." "Six touches."), and participle or prepositional
openers with no main verb. Imperatives are fine — a command has an implied subject.

**Correct his grammar, copy his voice.** He has said plainly that he can be wrong on grammar
and that fixing it is my job. So take the rhythm, the concreteness and the sequencing from his
examples, then write it in clean English: restore missing articles ("a GitHub repo", "a market
dashboard"), use a colon rather than a hyphen after "Example", and fix agreement and tense.
Never reproduce his slips as if they were style, and never leave a sentence ungrammatical
because he wrote it that way.

Run this check on book prose, chapter drafts, blurbs, listing copy, wiki notes and anything
else written in his name. Grep-able proxies (em-dash count, kill list) do not detect fragments;
you have to read every sentence.


### Polish, but never the AI feel (binding, added 2026-08-10)

**Over-sanitised prose IS the AI feel.** On 2026-08-10 a full voice pass stripped fifteen
aphorisms out of the Cowork book. Every check passed and the book got flatter, and two other
models preferred the unedited version. He was right: removing the lines that sound like a person
is not editing, it is sterilising.

**Resolve the two rules this way, because they conflict.**
- The **fragment ban wins, always.** No verbless sentences. No caption lists standing in for
  prose. No staccato two- or three-word sentences for effect ("Full stop." "Six touches."
  "Once is weather." "The analyst signs.").
- The **aphorism ban is narrower than it reads.** A sharp line that is a COMPLETE SENTENCE with a
  subject and a verb, carrying one fact, is his voice and it stays. "A reconciliation you never
  audit is a rumour with a timestamp." "Confidence is the thing the tool is best at faking."
  "An automation that produces a record nobody acts on is a filing habit wearing the costume of
  a process." Those are keepers. Do not flatten them into "proves nothing".
- What the old ban actually targets: decorative similes that stand in for the point rather than
  making it. Example of a fair cut: "Scheduling is worth more than intelligence, in the same way
  that a colleague who is reliably adequate every day beats one who is brilliant when he shows
  up" became "A task that runs every day without being asked is worth more than a cleverer task
  you have to remember to start." The simile was decorating a point it never made.

**The test before you cut a sharp line.** Ask two questions. Does it have a subject and a verb?
Does it make the point, or only decorate a point made elsewhere? Cut it only if it fails one.
Never cut it merely for being memorable.

**Uniformity is the real tell.** Identical chapter openers, the same section skeleton every
time, the same connective phrase forty times, every sentence the same length. That is what reads
as machine-written, not personality. Polished is good. Interchangeable is not.
