# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

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
