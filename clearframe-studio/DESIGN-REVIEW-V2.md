# KALPANA ENGINE — Independent Design Review & Version 2
### Adversarial panel review of BLUEPRINT.md (v1). No reassurance. 2026-07.

---

## PART A — PANEL VERDICTS

**DeepMind Chief Scientist:** "This is GOFAI filmmaking — 25 hand-designed stages and 23 hand-prompted
agents. The Bitter Lesson will eat at least half of it. Within five years a single long-context
multimodal model will natively hold a scene's continuity across minutes of video. Your pipeline's
value is not the boxes; it is the *world state, the evaluator, and the data exhaust*. V1 doesn't
know which of its organs are disposable — that's its biggest strategic flaw. Also: seven separate
VLM judges is an uncalibrated committee. You will Goodhart yourself: takes will evolve to please
judges, not humans, and you have no held-out human ground truth loop to catch it."

**OpenAI Research Lead:** "You underestimate how fast native multi-shot generation with internal
memory is coming — treating video models as stateless clip functions is a 2024 assumption baked
into a 10-year architecture. Second: 23 agents is orchestration theater. Agent count is a cost,
not a feature — most of these are *roles* (prompts), not *systems*. You have maybe six real
systems. Third: 'the user never manually iterates' is wrong as a product thesis and wrong as a
data thesis — human notes are your scarcest, highest-value training signal and V1 has no interface
to collect them."

**Kling Senior Engineer:** "Your router assumes stable model behavior. In production, providers
ship silent model updates weekly; your empirical priors will be stale the day you compute them.
You need continuous canary probing, not a registry. Also, N-takes-and-select is correct but you
budgeted N=3; at real inference economics the right N for hero shots is 20–100 with cheap drafts —
your architecture should be elastic in N, and your critic must be strong enough to rank 100
candidates, which seven zero-shot VLMs cannot do reliably."

**Veo Senior Engineer:** "First/last-frame conditioning plus a property graph does not give you
*within-scene* visual coherence — lighting temperature, lens character, and film grain drift
shot-to-shot and no graph constraint catches 'the mood changed.' You need scene-level latent
anchors (shared conditioning embeddings per scene), not just entity facts. And your repair tree
depends on video inpainting being solved — today it is the weakest tool in the chain. Plan for it,
don't depend on it."

**Pixar Rendering Architect:** "You built a 2D studio and called geometry an 'evolution.' Space is
not optional: eyelines, parallax, light transport, blocking — these are 3D facts. Pixar's pipeline
is layout → animation → lighting for a reason: the film exists as a *spatial scene* long before
final pixels. Your storyboard→video jump skips layout entirely. Second: no ACES color pipeline, no
USD scene interchange, no render determinism/reproducibility story — re-running the same film must
give the same film. Third — and this is the one that matters — you generate takes and *then* cut.
Backwards. Cut the animatic first; spend hero-render money only on frames that survive the edit.
We never render what we won't ship."

**Academy Award-winning Director:** "Where is the acting? You track 'emotion labels' — a
performance is micro-behavior: hesitation before a word, an eyeline that lies, a hand that betrays.
Nothing in V1 generates or evaluates *performance*. Also, you've designed a studio that argues
with itself politely until something passes gates — but taste is not a rubric. Whose taste is this
system's? V1 has no answer. Give the human director a real seat: the machine drafts, the human
gives notes, the machine learns the human's taste. That is also your data moat. Finally: your
'audience simulator' watching the final cut is the single best idea in V1 — promote it from QA
footnote to a first-class training signal."

**Principal Systems Architect:** "Linear phases are a lie the moment the Director re-plans: a
wardrobe change at gate G4 invalidates boards, takes, and the cut, and V1 has no invalidation
semantics. This is a *build system* problem — artifacts are derivations over the world state with
dependency tracking and incremental recompute. Also missing: versioning/branching of the world
model (a film needs git semantics — try an alternate act 3 without destroying the first),
checkpointing at film scale, idempotent stage re-runs, and any notion of asset caching economics.
The 'blackboard' will become a swamp without schema migration and garbage collection from day one."

**VC Technical Partner:** "The KPI — 'highest-quality film' — is unmeasurable as stated. No blind
evaluation protocol, no benchmark, no baseline. If you can't measure it, you can't claim it, can't
tune to it, and can't raise on it. Second: unit economics are absent — cost per finished minute at
each quality tier is THE operating number. Third: the moat claims are asserted, not designed — the
data flywheel has no labeling infrastructure, no telemetry schema, no training loop. A flywheel
without a data engine is a metaphor."

---

## PART B — THE NINE QUESTIONS

**1. What important AI systems are completely missing?**
- **Performance/acting system** — generation and evaluation of micro-behavior; the largest quality
  gap nobody addresses. Includes an *act-to-video* path: human performs a scene on webcam →
  performance transfer to the digital actor (the strongest control signal available today).
- **Layout/animatic stage (previz)** — the film as a cheap, complete, watchable object *at all
  times*, refined progressively. V1 has storyboards then jumps to hero pixels.
- **3D scene state** — geometry as first-class: 3DGS/NeRF locations, riggable avatars, camera
  solve; the property graph stores facts, not space.
- **Data engine** — telemetry schema, labeling UI, human-audit sampling, nightly preference-
  optimization loops. The flywheel's actual machinery.
- **Human notes interface** — structured director feedback ("more hesitation before the line",
  "warmer") that maps to machine-actionable deltas AND becomes training data.
- **Evaluation benchmark ("CineBench")** — blind pairwise human protocol + calibrated critic;
  the company's speedometer.
- **World-model versioning** — git semantics: branch, diff, merge alternate cuts/readings.
- **Scene-level style anchors** — shared latent conditioning per scene for mood/lens/grain
  coherence (the drift the graph can't see).
- **Rights/likeness verification for user scripts** — real-person detection, defamation risk,
  age-rating classification. Compliance was output-side only in V1.
- **Cost model & caching economy** — per-shot marginal cost tracking; asset reuse across projects.

**2. Which assumptions break within five years?**
- *"Video models are stateless clip generators."* Native multi-shot, memory-bearing generation
  arrives; parts of the continuity engine become redundant — the architecture must let models
  absorb pipeline boxes without a rewrite (see Absorption Doctrine, V2).
- *"Judges are cheaper and reliable."* Judge-generator gaps invert; Goodharting becomes the
  dominant failure mode. Human-anchored calibration is permanent, not bootstrap.
- *"Keyframe+prompt is the conditioning interface."* Latent/state-level APIs will replace prompt
  dialects; the Prompt-Compiler must become a Conditioning-Compiler.
- *"LoRA-per-character is needed."* Zero-shot identity conditioning is nearly there; keep the
  identity *contract* (embedding + verification), swap the mechanism freely.
- *"N=3 takes."* Inference cost falls ~10×/2yr; selection pressure should scale elastically to
  N=100 drafts. Architecture must be N-elastic; critics must rank, not just gate.

**3. What would you redesign from scratch today?**
- **Linear phases → reactive derivation graph** (build-system semantics; incremental recompute).
- **Generate-then-cut → cut-then-render** (animatic-first; hero pixels only for surviving frames).
- **Seven judges → one continuously-trained multi-task Critic** + rotating held-out human audits.
- **23 agents → ~8 systems** (roles are prompts, not services).
- **2D pipeline → hybrid neural-graphics core** (geometry now, not later).

**4. Where does V1 over-depend on today's diffusion models?**
Identity adapters, keyframe conditioning, video inpainting for repair, prompt dialects — all are
patches over diffusion's lack of persistent state. V2 isolates this behind a **Renderer
Abstraction**: the pipeline produces a *scene state*; "render" is a swappable backend (diffusion
today, simulation-conditioned diffusion next, world-model rollout later). Nothing upstream may
depend on how pixels are made.

**5. Beyond diffusion — which paradigm?**
Neither pure diffusion nor pure world-model: the winning shape is **simulate-then-render** —
explicit/learned 3D scene state + learned dynamics for motion truth, with diffusion demoted to a
*neural final-mile renderer* conditioned on G-buffers (depth/normals/segmentation/motion vectors)
from the simulation. It inherits controllability from graphics and photorealism from generative
models, and it converts continuity from a verification problem into a *construction guarantee*.
V2 commits to this as the destination; the derivation graph makes the migration incremental.

**6. What makes it fundamentally harder to copy?**
- The **taste corpus**: structured human director notes + outcomes, collected by the notes
  interface from day one. Nobody can scrape taste.
- **Benchmark ownership**: publish CineBench, run the public leaderboard — competitors calibrate
  on your yardstick.
- **Persistent creative assets**: user-owned characters/worlds that accumulate across projects
  (franchise lock-in; an asset marketplace adds network effects).
- **Vertical data**: Indic-language performance/speech/story data no Western lab prioritizes.
- **The derivation-graph exhaust**: (state, decision, result, human-override) tuples at film
  scale — the only dataset that trains an AI Director, and it only exists inside this product.

**7. Highest-leverage research breakthroughs (ranked):**
1. Region/time-local video editing that actually works (repair economics flip the cost curve).
2. Scene-state-conditioned generation (G-buffer/layout control of video diffusion).
3. A perceptual film-quality reward model aligned with human audiences (kills Goodhart, enables RL).
4. Performance transfer (drive digital actors from human reference acting).
5. 4D lift of generated takes (video → 3D scene) closing the loop between rendering and simulation.
6. Native long-horizon memory in video models (absorb continuity; ride it, don't fight it).

**8. Self-improvement without manual intervention:**
Instrument everything into one **event log**: every derivation, critic score, human note,
regeneration cause, and — post-release — audience retention per scene. Nightly: (a) DPO/RLHF on
craft policies from approve/reject pairs; (b) critic recalibration against sampled human audits;
(c) router prior refresh from canary probes; (d) prompt/conditioning library distillation from
successful repairs. Weekly: auto-remake of a fixed benchmark script with the updated stack;
CineBench-score the delta; auto-rollback on regression. Humans appear only as *labels in the log*,
never as steps in the loop.

**9. What would DeepMind/OpenAI/Pixar criticize most?**
DeepMind: hand-designed pipeline vs. scale — answered by the Absorption Doctrine (below).
OpenAI: agent sprawl and the no-human-iteration thesis — answered by consolidation + notes-first
product. Pixar: no geometry, no ACES/USD, and rendering before cutting — answered by the
neural-graphics core, standards adoption, and animatic-first refinement. All three: "your KPI is
unmeasurable" — answered by CineBench as a first-class subsystem.

---

## PART C — KALPANA V2

### C.1 Prime directives (unchanged objective, new constitution)
1. **Objective:** highest-quality final cinematic video from a user script.
2. **Animatic-first:** the complete film exists at every moment at some fidelity; money follows
   the cut, never precedes it.
3. **Absorption Doctrine:** every module declares its *deletion criterion* — the frontier-model
   capability that makes it redundant. When met, delete the module, keep its interface and its
   data. The durable core is: World State, Critic, Data Engine, CineBench, and the notes corpus.
4. **Renderer Abstraction:** nothing upstream knows how pixels are made.
5. **Human notes are gold:** autonomous by default, directable by design; every note is data.

### C.2 Architecture

```
                            ┌────────────────────────────────┐
                            │            SCRIPT              │
                            └───────────────┬────────────────┘
                                            ▼
        ╔═══════════════════════════════════════════════════════════════╗
        ║                    PRODUCTION STATE  (versioned, branchable)    ║
        ║  ┌────────────┐  ┌──────────────────┐  ┌────────────────────┐  ║
        ║  │ WORLD GRAPH│  │  SCENE STATE 3D  │  │  STYLE ANCHORS      │ ║
        ║  │ facts/time │  │ 3DGS locations,  │  │ per-scene latents:  │ ║
        ║  │ entities   │  │ avatars, camera  │  │ light/lens/grain/   │ ║
        ║  │ events     │  │ solve, blocking  │  │ palette embeddings  │ ║
        ║  └────────────┘  └──────────────────┘  └────────────────────┘  ║
        ║            + EVENT LOG (every decision, score, note)            ║
        ╚═══════════════════════════╦═══════════════════════════════════╝
                                    ║  (all artifacts are DERIVATIONS
                                    ║   over this state — build-system
                                    ║   semantics, incremental recompute)
      ┌─────────────────────────────╩──────────────────────────────────┐
      │                    DERIVATION GRAPH ENGINE                      │
      │   story analysis → bibles → layout/previz → ANIMATIC (v0 film)  │
      │   → draft takes (cheap N≈20) → EDL v1 → hero renders (N≈3–5,    │
      │   only surviving shots) → conform → grade(ACES) → mix → master  │
      │   Any upstream change ⇒ precise invalidation ⇒ minimal redo     │
      └───────┬───────────────────┬───────────────────┬────────────────┘
              ▼                   ▼                   ▼
      ┌──────────────┐   ┌────────────────┐   ┌──────────────────┐
      │ 8 SYSTEMS    │   │ RENDERER       │   │ THE CRITIC       │
      │ Director*    │   │ ABSTRACTION    │   │ one multi-task   │
      │ Story        │   │ route/ensemble │   │ model: fidelity, │
      │ Look(cast/   │   │ across models; │   │ identity, motion,│
      │  loc/props)  │   │ canary probes; │   │ continuity, cine,│
      │ Camera&Stage │   │ N-elastic;     │   │ PERFORMANCE;     │
      │ Performance  │   │ diffusion now →│   │ ranks 100 takes; │
      │ Sound&Music  │   │ sim-conditioned│   │ human-audit      │
      │ Edit         │   │ render later   │   │ calibrated       │
      │ Producer&    │   └────────────────┘   └──────────────────┘
      │  Compliance  │        * Director consults the human notes
      └──────────────┘          interface; every note → event log
                                    ║
        ╔═══════════════════════════╩═══════════════════════════════════╗
        ║                        DATA ENGINE                             ║
        ║  telemetry schema · labeling & audit UI · nightly DPO on       ║
        ║  policies · critic recalibration · router canaries · weekly    ║
        ║  benchmark auto-remake → CINEBENCH score → rollback on regress ║
        ╚════════════════════════════════════════════════════════════════╝
```

### C.3 What changed from V1 and why

| V1 | V2 | Justification |
|---|---|---|
| 5 linear phases, 25 stages | **Derivation graph** over Production State | re-planning invalidates precisely; no stale artifacts; parallel by construction |
| generate takes → then edit | **Animatic-first, cut-then-render** | Pixar economics: never render what you won't ship; film always screenable |
| property graph only | **World Graph + 3D Scene State + Style Anchors** | space and mood are not symbolic facts; eyelines/parallax/drift need geometry & latents |
| 7 zero-shot VLM judges | **One trained Critic** + rotating human audits | calibration, ranking at N=100, Goodhart defense |
| 23 agents | **8 systems** (roles = prompts inside them) | agents are cost; systems are architecture |
| "user never iterates" | **Notes-first collaboration**, autonomy optional | notes are the taste moat AND the better product |
| no acting subsystem | **Performance system** (direction, transfer, critic axis) | the largest unaddressed quality gap |
| identity via LoRA specifics | **Identity contract** (embedding + verification), mechanism-agnostic | survives zero-shot identity conditioning |
| repair assumes inpainting | repair prefers **re-render from scene state**; inpainting opportunistic | don't depend on the weakest tool |
| KPI asserted | **CineBench**: blind pairwise human protocol + calibrated critic score | unmeasurable KPIs are wishes |
| flywheel asserted | **Data Engine** subsystem with schemas & nightly loops | a flywheel needs machinery |
| color "grade" | **ACES pipeline, USD interchange, OpenTimelineIO, deterministic re-render** | professional interchange & reproducibility |
| compliance at output | compliance at **input and output** (likeness/defamation/rating) | user scripts are a legal surface too |

### C.4 Migration & staging (revised roadmap deltas)
- Stage 1 adds: animatic path, notes interface, event log, CineBench v0 (human pairwise on remade
  benchmark scripts). These four are cheap and create the moat immediately.
- Stage 2–3 adds: 3DGS locations + camera solve; Critic v1 trained on accumulated gauntlet labels.
- Stage 4–5: G-buffer-conditioned rendering experiments; performance transfer.
- Stage 6–7 unchanged (world models; self-improving Director) but now arrive as *renderer and
  policy upgrades inside stable interfaces* rather than re-architectures.

### C.5 The one-paragraph verdict
V1 designed a studio of agents around today's models. V2 designs an *economy of derivations*
around a versioned production state, spends pixels only after the cut, treats geometry and taste
as first-class, makes its own evaluator the product's spine, and is constitutionally prepared to
delete half of itself as frontier models grow — keeping the four assets that compound forever:
the production state, the critic, the benchmark, and the notes corpus.

*— end of review —*
