# KALPANA ENGINE
## Master Design Document — The AI Film Studio
### Script → Hollywood-Quality Film. Investor-grade & research-grade blueprint. v1.0, 2026-07

---

## 0. Thesis

Every existing product (Kling, Hailuo, Luma, Pika, Runway, Sora, Veo) solves **prompt → clip**.
A film is not a set of clips. A film is a *causally consistent world*, observed by a *camera with
intent*, edited to shape *emotion over time*. The quality ceiling of clip generators is not their
diffusion models — it is that **nothing owns the world, the intent, or the time axis**.

KALPANA's core bet: **final film quality = model quality × direction quality × consistency quality
× editing quality.** The industry competes only on the first factor. The other three are unclaimed,
are language-and-systems problems rather than diffusion problems, and compound: a 7/10 video model
under a 10/10 director/continuity/edit stack beats a 10/10 model driven by a one-line prompt.

Architecture in one sentence: a **persistent world model** (the single source of truth), written to
by a **pre-production agent swarm**, read by **model-agnostic shot generation**, policed by an
**adversarial quality loop**, and commanded by an **AI Director** that plans like a filmmaker and
approves like a studio.

---

## 1. System Overview

```
                              ┌────────────────────────────┐
                              │        SCREENPLAY IN        │
                              └──────────────┬─────────────┘
 PHASE I — COMPREHENSION                     ▼
   S1 Screenplay Parser → S2 Narrative Analyzer → S3 Emotion-Arc Mapper → S4 Scene-Graph Builder
                              │  writes everything to ▼
                    ╔═════════════════════════════════════════════╗
                    ║           WORLD MODEL (source of truth)      ║
                    ║  entities · states · timeline · style bible  ║
                    ╚═════════════════╦═══════════════════════════╝
 PHASE II — PRE-PRODUCTION            ▼ (agents read/write world model)
   S5 Casting & Character Bibles   S6 Location Scouting    S7 Prop/Costume Dept
   S8 Cinematography Plan          S9 Storyboards          S10 Blocking & Motion
   S11 Dialogue Timing & Voice Casting        S12 Music Spotting & Sound Design Plan
                                      ▼
 PHASE III — PRODUCTION (per shot, parallel, model-agnostic)
   S13 Shot Compiler → S14 MODEL ROUTER → S15 Generation → S16 QUALITY GAUNTLET
        ▲                                                      │ fail: targeted repair
        └───────────────── regenerate only what failed ◄───────┘
 PHASE IV — POST
   S17 Assembly Editor → S18 Continuity Audit → S19 Color Grade → S20 Sound Mix/Foley
   S21 Lip-Sync Refinement → S22 Titles/Subtitles/Translation
 PHASE V — DELIVERY
   S23 Mastering & Encodes → S24 Final QA Screening → S25 Provenance/C2PA + License Manifest
                                      ▼
                              ┌────────────────────────────┐
                              │        FINISHED FILM        │
                              └────────────────────────────┘
   Orchestrating everything: AI DIRECTOR + PRODUCER (budget/schedule) + SCRIPT SUPERVISOR (continuity)
```

---

## 2. The Pipeline — Every Stage

Format per stage: **Purpose / IO / Models & techniques / Why this wins / Alternatives & tradeoffs / Evolution.**

### PHASE I — STORY COMPREHENSION

**S1. Screenplay Parser**
- *Purpose:* lossless structural decomposition: scenes, sluglines, action, dialog, parentheticals, transitions.
- *IO:* raw text → typed AST (scene/beat/line objects with IDs).
- *Models:* frontier LLM with a formal screenplay grammar (Fountain superset) + constrained decoding to schema; deterministic fallback parser for well-formed input.
- *Why:* every downstream agent needs stable IDs to reference ("S12.beat3.line2") — free-text handoffs destroy consistency.
- *Alternatives:* pure-LLM freeform reading (fragile references); regex-only (misses implied structure). Hybrid wins.
- *Evolution:* accept novels/treatments; an adaptation agent converts prose → screenplay first.

**S2. Narrative Analyzer**
- *Purpose:* understand the story the way a director does: theme, genre, stakes, POV, act structure, setups/payoffs, subtext per scene.
- *IO:* AST → narrative dossier (theme statement, act breaks, tension curve, scene intentions: "S14 exists to make the betrayal in S22 hurt").
- *Models:* long-context frontier LLM, chain-of-thought over the whole script; retrieval over a corpus of annotated produced screenplays for genre priors.
- *Why:* scene intention drives every craft decision (lens, music, pace). Without it you get pretty, meaningless shots.
- *Tradeoffs:* interpretations vary → Director agent selects among 3 candidate readings (judge panel) instead of trusting one pass.
- *Evolution:* preference-tuned "taste model" trained on which readings produced better-rated films.

**S3. Emotion-Arc Mapper**
- *Purpose:* continuous emotion/tension signal over story time, per scene and per character.
- *IO:* dossier + AST → emotion curves (valence/arousal/tension vs. time; per-character emotional state at every beat).
- *Techniques:* LLM annotation → smoothed spline; validated against genre-shape priors (e.g., thriller sawtooth).
- *Why:* this single artifact synchronizes cinematography, music, editing pace, and performance. It is the film's heartbeat.
- *Evolution:* learned from audience biometric/retention datasets (opt-in) — the first real "audience simulator."

**S4. Scene-Graph Builder**
- *Purpose:* convert story into a formal world: entities (characters, locations, props), relations, and state *as a function of time*.
- *IO:* AST + dossier → temporal scene graph in the World Model (S = entities × states × events; every fact time-stamped: "jacket torn from S17 onward").
- *Techniques:* LLM extraction → typed graph DB (property graph); contradiction checker (SAT-style constraints: a character cannot be in two places in one timeline slot).
- *Why:* continuity cannot be "remembered in a prompt." It must be a database the pipeline is *forced* to read.
- *Alternatives:* implicit memory in LLM context (decays, hallucinates). Formal graph wins decisively.
- *Evolution:* graph becomes the interface to true neural world models (Stage 6, §10).

### PHASE II — PRE-PRODUCTION

**S5. Casting & Character Bibles**
- *Purpose:* every character becomes a *reproducible digital actor*.
- *IO:* character list + narrative dossier → per-character bible: identity images (multi-view reference sheet: front/profile/¾, neutral + 6 emotions), body spec, wardrobe per story-day, voice spec, movement style ("carries left shoulder low"), personality prompt.
- *Models:* frontier image model for reference sheets; identity-embedding extractor (face + body); per-character LoRA/identity-adapter trained on the approved sheet; voice: cloned or designed TTS voice locked per character.
- *Why:* consistency must be *conditioned on assets*, not described in words. Words drift; embeddings don't.
- *Tradeoffs:* LoRA-per-character costs minutes of GPU per character — trivial vs. reshoots.
- *Evolution:* full riggable 3D neural avatar per character (gaussian-splat body + face rig) for exact control.

**S6. Location Scouting**
- *Purpose:* every location is a persistent asset with geography.
- *IO:* location list → per-location bible: establishing images from multiple angles, floor-plan sketch (LLM-generated spatial layout), lighting conditions per time-of-day, ambience sound spec.
- *Models:* image model for plates; VLM to verify angle coherence; layout as structured JSON (camera-relative geometry).
- *Why:* eyeline and geography errors (character exits left, enters left) are the most jarring amateur tells.
- *Evolution:* NeRF/3DGS environment reconstruction → true camera freedom inside a consistent space.

**S7. Prop, Costume & Makeup Department**
- *Purpose:* trackable object registry: hero props, wardrobe states, injuries/aging.
- *IO:* scene graph → asset sheets (image + description + state timeline) bound to characters/locations.
- *Why:* the coffee cup that teleports between hands has ended careers.

**S8. Cinematography Planner** *(detail in §7)*
- *IO:* scene intentions + emotion curves → per-scene visual grammar: shot progression pattern, lens set, camera height/movement vocabulary, lighting key, palette; per-shot spec (framing, focal length, DoF, movement, duration).

**S9. Storyboard Artist**
- *Purpose:* cheap visual draft of every shot *before* expensive video generation.
- *IO:* shot specs → still frames (fast image model, character/location-conditioned) → Director review.
- *Why:* iterating on stills is 100× cheaper than video; kill bad compositions early. This is exactly why real studios board everything.
- *Tradeoffs:* adds a stage — pays for itself immediately in regeneration savings.

**S10. Blocking & Motion Planner**
- *Purpose:* who stands where, moves when, looks at whom; camera choreography relative to actors.
- *IO:* floor plans + shot specs → blocking diagrams + motion scripts (splines/keyframes; text motion cues for video models that only take prompts).
- *Techniques:* spatial reasoning LLM + geometric solver for eyelines/180° rule; outputs both machine-readable trajectories and natural-language motion prompts.
- *Evolution:* physics-aware planners; RL-tuned camera agents imitating great operators (trained on annotated film corpora).

**S11. Dialogue Timing & Voice Production**
- *Purpose:* speech is the metronome of a scene.
- *IO:* dialog + character voices → per-line audio (emotion-directed TTS), word-level timestamps, pause/overlap plan, breath map.
- *Models:* best available emotional TTS with voice consistency; prosody directed by the emotion curve ("say it tired, falling intonation").
- *Why:* generating voice FIRST and cutting picture to sound (animation-style workflow) beats lip-syncing after — timing becomes ground truth.
- *Alternatives:* generate video then dub (always looks dubbed). Audio-first wins.

**S12. Music Spotting & Sound Design Plan**
- *Purpose:* decide where music lives before editing (spotting session), define motifs per character/theme, plan the diegetic sound world of each location.
- *IO:* emotion curves + scene list → cue sheet (in/out points, intensity, motif), ambience spec per location, foley checklist per action beat.
- *Models:* music generation with motif conditioning and stem output; sound-effects generation/retrieval hybrid.

### PHASE III — PRODUCTION

**S13. Shot Compiler**
- *Purpose:* compile everything the world model knows about a shot into a *generation package*: conditioning images (character refs, location plate, previous-shot last frame), motion script, dialog audio, style bible, negative constraints, and acceptance criteria.
- *Why:* the package IS the interface between your IP and any video model — models become plug-ins.

**S14. Model Router** *(detail in §6)* — chooses the generator per shot.

**S15. Generation** — image-to-video / keyframe-conditioned generation preferred over pure text-to-video whenever supported (storyboard frame + refs as anchors). N seeds per shot (default 3) generated in parallel.

**S16. Quality Gauntlet** *(detail in §5)* — every candidate judged; best-or-none advances; failures trigger *targeted* repair.

### PHASE IV — POST-PRODUCTION

**S17. Assembly Editor**
- *Purpose:* cut the film. Select takes, trim to rhythm, place transitions.
- *Techniques:* editing-grammar rules (cut on action, J/L audio cuts, reaction-shot logic) + emotion-curve pacing targets (shot-length distribution per tension level) + VLM verification of match-cuts; edit decision list (EDL) as output.
- *Why:* editing is where films are made or lost; an explicit EDL keeps it auditable and re-cuttable.
- *Evolution:* editor policy preference-trained on professional cuts (predict the next-cut decisions of great editors).

**S18. Continuity Audit** — full-film pass by the Script Supervisor agent (§4): every frame-pair across cuts checked against the world model (wardrobe, props, light direction, screen direction, eyelines). Violations → targeted reshoots.

**S19. Color Grade** — shot-to-shot color matching (histogram/illuminant alignment) then creative grade from the style bible (LUT selection/generation per emotional zone); VLM checks skin-tone fidelity.

**S20. Sound Mix & Foley** — foley synthesis per action beat, ambience beds per location, music stems ducked under dialog (sidechain), loudness spec (-14 LUFS streaming / -24 broadcast), spatial panning tied to blocking.

**S21. Lip-Sync Refinement** — dedicated lip-sync model pass on close-ups (audio-conditioned facial re-animation), viseme accuracy scored; wide shots exempt (below perceptual threshold).

**S22. Titles, Subtitles, Translation** — subtitle timing from S11 timestamps; translation LLM with cultural-idiom care; optional full dub track re-using character voice identities in target language (voice consistency across languages).

### PHASE V — DELIVERY

**S23. Mastering** — resolution/codec ladder, HDR pass, poster frames, trailer auto-cut (highest-tension beats).
**S24. Final QA Screening** — a fresh "audience" VLM watches the entire film end-to-end (no pipeline context) and files issues like a test audience: confusion, boredom spikes, visible artifacts. Director triages.
**S25. Provenance & Rights** — C2PA manifest embedded (every asset's model, seed, license), full license manifest, content credentials. *Non-negotiable for commercial distribution.*

---

## 3. The AI Director

The Director is a **planning loop with taste**, not a chat prompt.

**Responsibilities:** own the creative interpretation (choose among S2 readings); approve/reject at every gate (bibles, boards, takes, cut); allocate the quality budget (which scenes deserve 10 takes vs 2 — driven by the emotion curve: climaxes get the compute); resolve inter-agent conflicts (cinematographer wants a slow push-in, editor wants pace → Director rules by scene intention); maintain the *vision document* (style bible: palette, grain, lens character, references) that every agent must cite.

**Architecture:**
- *Planner:* hierarchical — film goals → act goals → scene intentions → shot criteria. Re-plans when reality diverges (a location bible turned out moodier than intended → propagate).
- *Reasoning:* every decision recorded as `(decision, alternatives considered, reason, evidence)` — an auditable director's log. Test-time compute scales with stakes: cheap calls decided directly; expensive calls (final cut of the climax) get tree-search over alternatives with judge panels.
- *Memory:* working (current scene context), episodic (the log), and the World Model as ground truth. The Director never trusts its context window over the database.
- *Coordination:* agents are contractors — they submit work against acceptance criteria; the Director approves, rejects with notes, or escalates budget. Blackboard pattern: all artifacts land in the world model; agents subscribe to what they need.
- *Approval gates:* G1 interpretation → G2 bibles → G3 boards → G4 takes → G5 assembly → G6 final master. Each gate has explicit rubrics so "approval" is reproducible, not vibes.

---

## 4. The Agent Roster

| Agent | Owns | Key output |
|---|---|---|
| **Director** | vision, approvals, budget of attention | director's log, gate decisions |
| **Producer** | compute budget, schedule, model spend | cost plan; kills gold-plating on low-stakes shots |
| **Script Supervisor** | continuity truth | violation reports; the only agent with world-model write-audit power |
| **Casting Director** | character bibles | identity assets, voice casting |
| **Character Designer** | look development | reference sheets, wardrobe plates |
| **Location Scout** | location bibles | plates, floor plans, light/ambience specs |
| **Cinematographer (DoP)** | visual grammar | shot specs, lens/light plans |
| **Storyboard Artist** | pre-visualization | boards per shot |
| **Camera Operator** | motion execution | motion scripts per take |
| **Gaffer** | lighting continuity | light-direction map per location/time |
| **Blocking Choreographer** | staging | blocking diagrams, eyeline map |
| **Dialogue Director** | performance of lines | emotion-directed TTS takes |
| **Composer** | score | motif-based cues, stems |
| **Sound Designer** | world of sound | ambience beds, foley plan |
| **Editor** | the cut | EDL, pacing report |
| **Colorist** | grade | LUTs, shot-match report |
| **VFX Supervisor** | impossible shots | composite plans (split generation: bg plate + character pass) |
| **Lip-Sync Specialist** | mouth truth | refined close-ups |
| **Translator/Localizer** | languages | subs, dubs (voice-consistent) |
| **QA Auditor** | artifact hunting | defect reports per take (adversarial: rewarded for finding flaws) |
| **Audience Simulator** | fresh eyes | end-to-end screening notes |
| **Compliance Officer** | IP/likeness/safety | sanitization audits, C2PA, license manifest |
| **Archivist** | memory hygiene | world-model garbage collection, asset versioning |

Design rule: **every agent is a critic of some other agent's work.** No output enters the film unexamined. QA and creator roles are always different models or at least different prompts with opposed incentives.

---

## 5. The Quality Loop (the most important subsystem)

**Principle: generation is cheap and fallible; judgment must be cheaper and reliable.** Quality emerges from *selection pressure*, not from hoping a model gets it right.

**Per-take gauntlet (parallel judges, each a specialized VLM/metric):**
1. *Prompt fidelity* — does the take contain what the shot spec demands? (VLM checklist over spec fields)
2. *Identity* — face/body embedding distance to character bible < threshold (ArcFace-style + body re-ID); wardrobe classifier vs. costume state.
3. *Continuity* — first/last frames vs. adjacent shots and world model (prop presence, light direction, screen direction).
4. *Motion realism* — physics plausibility scorer (optical-flow smoothness, limb-kinematics sanity, object permanence through occlusion).
5. *Artifact hunt* — adversarial detector for extra fingers, morphing objects, texture boiling, temporal flicker.
6. *Cinematic quality* — composition score vs. intended framing; camera-movement smoothness vs. motion script.
7. *Performance* — facial-expression classification vs. intended emotion at beat timestamps; lip-sync viseme score on dialog shots.

**Aggregation:** weighted by shot stakes (from emotion curve). Hard gates (identity, artifacts) are veto; soft scores trade off.

**Repair decision tree (regenerate the minimum):**
```
FAIL identity        → re-condition with stronger reference weight / switch to identity-specialist model → retry
FAIL one region/time → inpaint or re-generate segment only (video inpainting), not whole shot
FAIL motion          → keep first frame (composition approved), regenerate with adjusted motion script
FAIL fidelity        → prompt surgery by a dedicated Prompt-Doctor agent (diff spec vs. VLM description; patch the delta)
FAIL 2× on same model→ ROUTER escalates: next-best model for this shot class
FAIL 2× on all models→ decompose: split shot into simpler shots (Director approves board change)
Budget exhausted     → Producer decides: accept best take with logged debt, or cut the shot in the edit
```
Everything logged → router priors and prompt libraries improve with every film (the studio *learns*).

---

## 6. Model Orchestration

**Capability registry** (live, versioned): per model — max duration, resolution, i2v/keyframe/motion-control support, identity-conditioning support, lip-sync, style range, cost/sec, latency, region/ToS constraints, and *empirical* quality priors per shot class (from our own gauntlet history, not vendor claims).

**Router = constrained optimizer:** for each shot, score every eligible model:
`score = Σ w_i · quality_prior(model, shot_class) − λ·cost − μ·latency`, subject to hard constraints (needs identity conditioning; needs 10s; ToS allows depicted content). Weights come from shot stakes (Producer sets λ per budget). Exploration: ε-greedy / Thompson sampling on a small fraction of low-stakes shots to keep priors fresh as models update.

**Ensemble mode for hero shots:** top-2 models generate in parallel; gauntlet picks. Split generation when it wins: background plate from the best environment model + character pass from the best identity model + composite.

**Abstraction:** one `ShotPackage → Take` interface; adapters per provider (API or self-hosted). Adding a new model = writing an adapter + letting the gauntlet calibrate its prior. **No prompt anywhere in the codebase is model-specific** — a Prompt-Compiler per adapter translates the package into each model's dialect.

---

## 7. Cinematic Intelligence

Not "apply rule of thirds." A **grammar of visual storytelling** compiled from film craft:

- *Inputs:* scene intention, emotion curve, character power dynamics, location geometry.
- *Knowledge:* codified craft rules (shot-reverse-shot, 180°, cut-on-action, lens psychology: wide=vulnerable-in-space, long=compressed-inevitability; height: low=power; movement: push-in=realization, handheld=instability) + a retrieval corpus of annotated reference scenes ("interrogation scenes graded by tension") for grounding by example.
- *Decision procedure:* per scene, choose a *visual strategy* (e.g., "start static wides, collapse to handheld close-ups as the lie unravels") justified against intention; compile to per-shot specs; verify after generation (VLM measures achieved framing/movement vs. spec — closes the loop).
- *Why grammar + retrieval beats end-to-end:* auditable, directable, and improvable per rule; an end-to-end "cinematography network" is a black box you can't note-give.
- *Evolution:* preference-optimize the strategy chooser on human cinematographer ratings (RLHF for shot design).

---

## 8. Character Consistency (guarantees, not hopes)

Layered identity stack — each layer independently enforced:
1. **Canonical identity:** approved reference sheet → face/body embeddings stored in world model (the *legal* definition of the character).
2. **Conditioning:** every generation receives identity images/adapters (IP-adapter/LoRA-class); never text-only.
3. **Verification:** gauntlet gate — embedding distance per take, per *frame sample* (catches mid-shot morphs). Hard veto.
4. **State overlay:** wardrobe/injury/age per story-day from the scene graph modifies conditioning (bible base + state delta images generated once, reused).
5. **Voice:** one locked TTS identity per character; emotion directed per line; same voice embedding reused for dubs.
6. **Movement & personality:** movement-style descriptor in every motion script; personality prompt governs the Dialogue Director's line readings; relationship state (from scene graph) modulates blocking distance and eyeline behavior.
7. **Drift repair:** if a whole scene's takes drift (model update, style bleed), Casting re-anchors: regenerate state deltas from canonical, re-run takes.
- *Evolution:* per-character neural avatars (rigged 3DGS) make identity exact and directable; video models then *render*, not invent, the person.

---

## 9. Continuity Engine — the World Model

- **Store:** property graph + asset store + event log. Entities (character/location/prop/costume) → states (time-indexed attributes) → events (state transitions caused by script beats). Every generated asset links back to the entities it depicts (provenance edges).
- **Constraint layer:** invariants checked on write (spatial exclusivity, light-direction consistency per location/time, object permanence). Violations block generation *before* GPUs burn.
- **Query layer:** the Shot Compiler asks: "state of the world at S17.shot4?" → the exact conditioning set. The Script Supervisor asks the inverse after generation: "does this take contradict any fact?"
- **Camera history:** every executed shot's framing/lens/position stored → enables coverage logic (don't cross the line; vary setups; match eyelines) and the editor's choice of matching angles.
- *Evolution (Stage 6):* attach a learned neural world-model as a *simulator* behind the graph — the graph remains the interface; the simulator provides physics/lighting rollouts for planning and, ultimately, rendering.

---

## 10. Research Agenda (ranked by expected quality lift)

1. **VLM-as-judge fidelity** — everything depends on judges that see artifacts humans see. Fine-tune judges on human-labeled defect datasets from our own gauntlet history (proprietary data flywheel #1).
2. **Identity-preserving conditioning** — better-than-IP-adapter identity injection into video DiTs; per-character LoRA at scale.
3. **Keyframe/interval control** — generation conditioned on first+last frames + trajectory (the storyboard becomes literal control, not inspiration).
4. **Video inpainting / regional editing** — repair without full regeneration (the economics of the quality loop hinge on this).
5. **Preference optimization for craft policies** — RLHF/DPO on Director/DoP/Editor decisions vs. professional ratings (proprietary flywheel #2: our approval logs are the training data).
6. **Test-time compute scaling** — tree search over creative decisions with learned value functions ("does this cut serve the scene?").
7. **Neural world models** — Genie/Dreamer-class simulators for blocking rollouts and eventually rendering.
8. **Long-horizon memory architectures** — graph-grounded agent memory (what we build in §9 is the scaffold).
9. **Audio research** — emotion-controllable TTS, singing, foley synthesis from video (audio is half the film and one-tenth of the industry's attention).
10. **Self-improving pipeline** — every gate decision + outcome is a labeled example; nightly distillation of "what the Director learned" into policy updates.

---

## 11. Roadmap

| Stage | What | Why it exists | Exit criterion |
|---|---|---|---|
| 1 | **Best APIs, full pipeline** (Kling/Veo/Runway/Luma via router; ElevenLabs voice; Suno/Udio-class music) | prove direction+continuity+edit stack lifts quality NOW; collect gauntlet data | our film > any single-tool film, blind-judged |
| 2 | **Open models self-hosted** (Wan/Hunyuan-class) | cost control, no ToS ceilings, regional latency; router mixes APIs+local | ≥70% shots on owned inference at equal quality |
| 3 | **Fine-tunes & adapters** (identity LoRAs, style tunes, control adapters, distilled fast drafts) | consistency and control beyond what APIs expose | identity gate pass-rate >99% first-take |
| 4 | **Specialized models** (storyboard model, lip-sync model, inpainting model, judge models) | each pipeline box gets a purpose-built organ | gauntlet judges beat human spot-checks |
| 5 | **Domain video foundation models** (dialog scenes, product/finance explainers, Indic-language content) | 3M curated domain clips beat 300M generic; our niches, our data | domain quality > frontier general models in-domain |
| 6 | **World models** | consistency by construction: render from simulation, not sampling | multi-shot scenes with zero continuity edits |
| 7 | **Self-improving Director** | approval logs + audience outcomes → policy learning; the studio gets better with every film it makes | quality curve provably rising film-over-film |

Stages overlap; the router makes every stage additive rather than a rewrite. **The pipeline (Phases I–V) never changes shape — only the organs upgrade.**

---

## 12. Technology Stack (Stage-1 concrete)

- **Orchestration:** typed agent framework (LangGraph-class or in-house), every artifact schema-validated; message bus + blackboard (world model).
- **World model:** property graph DB (Neo4j-class) + object store for assets + event-sourced log (replayable).
- **Agents:** frontier LLM for Director/Producer/analysts; specialized VLMs for judges; per-craft system prompts + tool access.
- **Generation:** adapter services per provider; GPU pool (K8s + queue) for open models from Stage 2.
- **Media:** ffmpeg/OpenTimelineIO for EDL & conform; loudness pipeline; C2PA signing.
- **Observability:** every take, judge score, cost, decision logged — this dataset IS the company.

---

## 13. Objective Comparisons (key contested choices)

| Choice | Options | Winner & why |
|---|---|---|
| Consistency | prompt memory vs **formal world model** | world model — verifiable, deletes hallucination class |
| Generation input | text-to-video vs **keyframe/i2v-first** | i2v — composition approved cheaply as stills first |
| Audio order | video-first dub vs **audio-first cut** | audio-first — timing ground truth, lip-sync tractable |
| Quality | single best take vs **N takes + selection** | selection — pressure beats hope; N scales with stakes |
| Cinematography | end-to-end learned vs **grammar + retrieval + verify** | grammar — auditable, note-giving works |
| Models | single vendor vs **router + registry** | router — no vendor ceiling, empirical priors compound |
| Editing | generate-in-order vs **EDL over take library** | EDL — recuttable, auditable, parallelizable |

---

## 14. What Makes This Defensible

1. **The world model + gauntlet logs are proprietary data no model vendor has** — labeled (spec, take, judgment, repair, outcome) tuples at film scale.
2. **Craft policies improve with use** (flywheels #1/#2) — a studio that learns.
3. **Model-agnosticism converts the industry's $100M model war into our free R&D.**
4. **Compliance-native** (C2PA, license manifests, likeness gates) — the only architecture large brands and studios can legally adopt.
5. **The KPI is the film, not the clip** — incumbents must rebuild from the world-model out to follow.

*— end of blueprint —*
