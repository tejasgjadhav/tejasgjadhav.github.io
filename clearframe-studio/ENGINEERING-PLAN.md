# KALPANA — Engineering Master Plan
### Converting the frozen V2 architecture into a buildable program. v1.0, 2026-07.
Target: evolve for a decade without a rewrite. Method: **contracts outlive implementations.**

---

## 1. Dependency Graph

Nine subsystems. Arrows = "needs to exist first" (interface-level, not feature-complete).

```
                      ┌─────────────────────────────┐
                      │ 0. SCHEMAS & CONTRACTS      │  ← everything depends on this
                      └──────┬──────────────────────┘
                             ▼
             ┌───────────────────────────────┐
             │ 1. PRODUCTION STATE (PS)      │  event log · world graph ·
             │    versioned, event-sourced   │  artifacts · style anchors
             └───┬───────────┬───────────┬───┘
                 ▼           ▼           ▼
   ┌─────────────────┐ ┌───────────┐ ┌─────────────────────┐
   │ 2. DERIVATION   │ │ 3. RENDER │ │ 4. CRAFT SYSTEMS    │
   │    GRAPH (DG)   │ │  ABSTRACT.│ │ story/look/camera/  │
   │ invalidation,   │ │ adapters +│ │ performance/sound/  │
   │ incremental     │ │ router    │ │ edit/director/prod. │
   └────────┬────────┘ └─────┬─────┘ └──────────┬──────────┘
            └──────────┬─────┴─────────┬────────┘
                       ▼               ▼
              ┌─────────────┐   ┌─────────────┐
              │ 5. CRITIC   │   │ 6. STUDIO UI│  (screenplay editor, animatic
              │ gate→rank   │   │  + notes    │   player, notes, dashboards)
              └──────┬──────┘   └──────┬──────┘
                     ▼                 ▼
              ┌────────────────────────────┐
              │ 7. DATA ENGINE             │  telemetry → labeling → training
              └──────────────┬─────────────┘
                             ▼
              ┌────────────────────────────┐
              │ 8. CINEBENCH               │  needs a full pipeline to score
              └────────────────────────────┘
   9. INFRA (queue, storage, GPU pool, observability) — horizontal, grows with each milestone.
```

**Parallelizable after Schemas (0) + PS skeleton (1):** Render adapters (3), Craft systems (4),
Studio UI (6), Critic v0 (5) — four independent tracks.
**Strictly serial:** 0 → 1 → 2 (the graph engine needs real state to derive from);
7 needs PS's event log format; 8 needs an end-to-end pipeline (any fidelity).

---

## 2. Development Phases

Every milestone ends with a **usable product** and a **demo film**.

**M0 — Contracts & Walking Skeleton** *(complexity: S)*
- *Objective:* every schema defined; a stub pipeline runs end-to-end ("hello film": script in →
  black frames + silence out) through real interfaces.
- *Deliverables:* `schemas/` package (versioned, code-generated TS+Python types); event-log store;
  CLI `kalpana make film.fountain`; stub adapters.
- *Success:* pipeline runs from CLI; every artifact content-addressed; replaying the event log
  reproduces identical outputs (determinism harness green).
- *Risks:* over-designing schemas — mitigate: schemas are versioned, additive-only; ship v0 fast.
- *Extensibility:* this IS the extensibility — everything after M0 is swapping stubs.

**M1 — Comprehension & Production State v1** *(M)*
- *Objective:* script → typed AST → world graph (entities, states, timeline) with contradiction checks.
- *Deliverables:* screenplay parser (Fountain superset + LLM assist), narrative dossier, emotion
  curves, scene graph writer/reader API; state branching (git semantics v0: branch + diff).
- *Success:* 20 diverse test scripts parse with zero unresolved entity references; injected
  continuity contradictions (test suite) are 100% caught at write time.
- *Prereq:* M0. *Risk:* LLM parse variance → constrained decoding + golden-file tests.

**M2 — Renderer Abstraction + First Real Pixels** *(M)*
- *Objective:* ShotPackage → Take through a router with 2 adapters (1 image API for boards,
  1 video API) + identity conditioning plumbing.
- *Deliverables:* adapter SDK, capability registry, cost meter, N-take fan-out, storyboard pass.
- *Success:* same ShotPackage renders via either adapter with no upstream change; adapter added
  in <1 day by one engineer (measured); every take carries provenance + cost record.
- *Risk:* provider ToS/instability → registry marks capabilities per provider version; canary probe job.

**M3 — Animatic-First Path (the product moment)** *(M)*
- *Objective:* complete watchable film at draft fidelity: boards + character-voiced dialog (TTS)
  + music cues + EDL conform.
- *Deliverables:* dialogue timing from TTS timestamps; cue sheet; EDL (OpenTimelineIO) + ffmpeg
  conform; animatic player in UI.
- *Success:* any script → watchable animatic in <30 min, unattended; audio-first sync verified
  (dialog drift <50ms vs timestamps).
- *Why usable:* this alone beats every "prompt→clip" tool for story work.

**M4 — Selection Pressure (Critic v0 + repair)** *(M)*
- *Objective:* N drafts per shot → gate → rank → pick; targeted repair tree v0.
- *Deliverables:* zero-shot judge ensemble (identity embedding gate, artifact VLM, fidelity
  checklist), stakes-weighted aggregation, repair policies (re-prompt, re-seed, escalate model).
- *Success:* on a 50-shot benchmark, auto-selected takes beat random-take baseline in blind human
  pairwise ≥70%; failed-shot rate after ≤3 repair rounds <10%.
- *Risk:* judge unreliability → keep humans in sampling loop (audit 10% of gates), log everything.

**M5 — Notes & Data Engine v0 (the moat starts)** *(M)*
- *Objective:* structured human notes → actionable deltas → event log; telemetry + labeling UI.
- *Deliverables:* note schema (target, axis, direction, free text), note→derivation-invalidation
  mapping, labeling/audit web UI, telemetry warehouse tables.
- *Success:* a note like "warmer light, scene 4" auto-invalidates exactly scene-4 lighting-dependent
  derivations and nothing else; 100% of gate decisions + notes queryable in warehouse.

**M6 — Hero Pipeline (finished short film)** *(L)*
- *Objective:* cut-then-render: EDL survivors get hero renders; continuity audit; ACES grade;
  mix (ducking, loudness); lip-sync pass on close-ups; C2PA + license manifest.
- *Success:* a 3–5 min short produced unattended from script, passing: zero continuity violations
  (audit), loudness spec, identity gate ≥99% frames, blind panel rates it above the same script
  run through a single video tool (≥70% preference).

**M7 — CineBench + Router Learning** *(M)*
- *Objective:* measurable quality; weekly auto-remake of fixed benchmark scripts; Elo over versions;
  router priors from accumulated gauntlet outcomes; regression rollback.
- *Success:* CineBench report auto-published weekly; a deliberately degraded adapter is auto-detected
  and demoted within one cycle.

**M8 — Learning Studio (V2 endgame begins)** *(L→XL, ongoing)*
- *Objective:* trained Critic v1 (from M4–M7 labels), nightly DPO on craft policies, 3D scene
  state v0 (3DGS location plates + camera solve), performance-transfer experiments.
- *Success:* Critic v1 beats zero-shot ensemble on held-out human labels (AUC +10pts); one
  policy (e.g., editor pacing) measurably improves via preference training on CineBench.

---

## 3. Repository Architecture

Monorepo (one atomic change can touch schema + producers + consumers; CI enforces contract compat).

```
kalpana/
├── packages/
│   ├── schemas/            # THE source of truth: JSON Schema, versioned; codegen → py+ts. Why: contracts outlive code.
│   ├── sdk-py/ sdk-ts/     # generated clients; no service talks to another except through these
│   └── medialib/           # ffmpeg/OTIO/ACES wrappers, content-addressed artifact IO
├── services/
│   ├── state/              # Production State: event store, world graph projections, branching API
│   ├── graph/              # Derivation engine: dependency tracking, invalidation, scheduling
│   ├── systems/            # the 8 craft systems, one package each (story/ look/ camera/ performance/ sound/ edit/ director/ producer)
│   ├── render/             # router, capability registry, adapters/{openai,kling,luma,wan,...}, canary
│   ├── critic/             # gates, rankers, judge models, calibration
│   └── data-engine/        # telemetry ingest, warehouse schemas, labeling API, training jobs
├── apps/
│   ├── studio/             # web UI: script editor, animatic player, notes, dashboards
│   └── cli/                # kalpana CLI — headless studio; every feature lands here FIRST (testability)
├── eval/
│   ├── cinebench/          # benchmark scripts, pairwise protocol, Elo, weekly runner
│   └── goldens/            # golden films + golden derivations for regression
├── infra/                  # terraform + k8s/compose, GPU pool config, secrets policy
├── tests/                  # unit (per package) · integration (contract tests) · film (e2e golden)
└── docs/adr/               # Architecture Decision Records — every irreversible choice gets one
```

Why each exists in one line: `schemas` = decade-stability; `sdk` = no hidden coupling; `medialib` =
media correctness is shared, subtle, and testable; `state`/`graph` = the two durable services;
`systems` = deletable per Absorption Doctrine (each declares its deletion criterion in its README);
`render` = the vendor firewall; `critic` = the quality spine; `data-engine` = the flywheel machinery;
`cli` before `studio` = automatable, scriptable, CI-runnable product; `adr` = future engineers
inherit the *why*.

---

## 4. Interfaces (the contracts that must not churn)

All schemas versioned (`v:`), additive evolution only; breaking change = new major + adapter shim.

- **EventRecord** `{v, id, ts, actor, kind, payload, causes[]}` — append-only; the log IS the state.
- **StateQuery / StateView** — "world at (branch, t_story, t_wall)" → typed projection. Consumers
  never read the log directly.
- **Derivation** `{v, id, kind, input_hashes[], params_hash, code_version, output_artifacts[], cost, status}` —
  content-addressed both sides; identical inputs ⇒ cache hit, never re-run.
- **ShotPackage** `{v, shot_id, spec(framing/lens/motion/duration), conditioning{identity_refs[],
  location_plate, style_anchor, prev_frame?}, audio_track?, acceptance_criteria[], stakes, budget}` —
  the ONLY input a renderer may receive.
- **Take** `{v, take_id, shot_id, media_ref, model{provider,version,params,seed}, cost, provenance}`.
- **CritiqueReport** `{v, take_id, gates{name→pass|veto,evidence}, scores{axis→float,confidence},
  rank_context, repair_hints[]}`.
- **Note** `{v, target(entity|scene|shot|film), axis(light/pace/perf/...), direction, magnitude?,
  text, author}` — resolvable to a set of invalidated derivations.
- **ModelAdapter** (SDK interface): `capabilities() → CapabilityDecl`, `estimate(pkg) → {cost,eta}`,
  `generate(pkg) → Take`, `health() → CanaryResult`. Nothing else.
- **CritiquePolicy / RouterPolicy / EditPolicy** — policies are versioned data (weights + rules),
  not code branches; the Data Engine ships new policy versions, services just load them.

---

## 5. Technology Choices (and why)

| Subsystem | Choice | Why (vs alternatives) |
|---|---|---|
| Schemas | JSON Schema + codegen (datamodel-code-generator / quicktype) | human-readable, polyglot, additive versioning; protobuf adds ops weight without cross-team scale yet — revisit at >20 engineers (ADR) |
| Event store + projections | **Postgres** (JSONB events, typed projection tables, pgvector for embeddings) | one boring database does log+graph+vectors at this scale; Neo4j deferred until graph queries measurably hurt (ADR with trigger metric: >100ms p95 on 3-hop queries) |
| Artifacts | S3-compatible object store (MinIO dev / cloud prod), content-addressed (sha256 keys) | dedupe, cache-correctness, provenance for free |
| Derivation graph | **Custom engine on Postgres + Temporal** for durable execution | Temporal gives retries/long-running/human-in-loop signals out of the box; a build-system library (Bazel-like) doesn't handle month-long jobs or human gates. Custom dependency layer stays thin (~2k LOC) |
| Services | **Python + FastAPI** (uv, ruff, pydantic from codegen) | the AI ecosystem is Python; FastAPI = typed contracts; performance is not the bottleneck (GPUs are) |
| Studio UI | **Next.js + TypeScript** (generated SDK), video via HLS | boring, hireable, SSR for dashboards; TS types generated from the same schemas |
| Media | ffmpeg + **OpenTimelineIO** (EDL) + **ACES/OCIO** (color) + USD later (3D) | industry interchange formats = pro tools interop + future 3D path |
| Queue/compute | Temporal workers; GPU pool via K8s + KEDA autoscale (Stage 2+) | one orchestration model for API calls and self-hosted inference |
| Telemetry/warehouse | OpenTelemetry → Postgres now, **ClickHouse when** event volume >10M/day (ADR trigger) | don't run two databases before the data demands it |
| Judges/critic | serve via vLLM (open VLMs) + API judges behind the same Adapter interface | judges are models too — same vendor firewall |
| Training (M8+) | PyTorch + Ray for distributed jobs; W&B/MLflow tracking | standard, replaceable |
| Auth/tenancy | ory/keycloak-class OSS, single-tenant first | multi-tenant is a business decision, not day-1 architecture |

Rule: **every "when do we upgrade" is an ADR with a numeric trigger**, so evolution is planned, not
argued.

---

## 6. Technical Risks (ranked)

**R1. Judge reliability / Goodharting** — the whole quality thesis leans on it.
- *Validate early:* M4 — measure judge-vs-human agreement on 500 labeled takes before building repair automation.
- *Fallback:* human audit sampling stays permanent; stakes-weighted (hero shots always human-checked).
- *Exit criterion:* Critic-human pairwise agreement ≥85% on held-out takes; measured quarterly, never assumed.

**R2. Provider churn & ToS ceilings** (silent model updates, rate limits, content rules).
- *Validate:* canary probes from M2 day one; capability registry keyed by provider *version*.
- *Fallback:* ≥2 adapters per shot class always; Stage-2 self-hosted open model as floor.
- *Exit:* a provider regression is detected and demoted within one canary cycle (test: inject a degraded stub).

**R3. Derivation-graph over-engineering** — building Bazel-for-films nobody needs yet.
- *Validate:* M0 skeleton with the 5 real derivation kinds only; complexity budget 2k LOC.
- *Fallback:* degrade to "recompute scene downstream" coarse invalidation — correct, just less efficient.
- *Exit:* a wardrobe-change note recomputes <15% of film derivations on the golden film.

**R4. Identity consistency below bar** (video models ignore conditioning).
- *Validate:* M2 spike — identity gate pass-rate per provider measured on 100 takes before promising it.
- *Fallback:* face/region video editing pass; or restrict hero characters to close-up-heavy coverage patterns (directorial workaround — cheap and honest).
- *Exit:* ≥95% frames within embedding threshold on 2+ providers.

**R5. Cost per finished minute unknown.**
- *Validate:* cost meter in every Take from M2; publish ₹/min per fidelity tier from M3.
- *Exit:* draft tier <$2/min, hero tier <$40/min at M6 (numbers to be re-based on first real data — the discipline is having the number, not the number).

**R6. Repair depends on video inpainting maturity.**
- *Fallback (default):* re-render from adjusted ShotPackage (cheap at draft tier) — inpainting is an optimization, never a dependency (V2 rule).

**R7. Solo-builder integration risk** (nine subsystems, one person).
- *Mitigation:* CLI-first, golden-film e2e test from M0 — the film either builds or the commit fails.

---

## 7. Research vs Engineering

**Deterministic engineering** (plan-able, estimable): schemas/SDK, event store, projections,
branching, derivation engine, adapters, cost metering, EDL/conform, ACES pipeline, loudness mix,
telemetry, labeling UI, CineBench harness, CI/CD, C2PA signing.

**Applied-ML engineering** (known methods, tuning risk): screenplay parsing with constrained
decoding, emotion curves, identity gates (embeddings), zero-shot judge ensemble, TTS direction,
music cue conditioning, router scoring.

**Research** (unknown outcomes — timebox + kill criteria): trained Critic beating zero-shot
(M8), DPO on craft policies, performance transfer, 3DGS scene state + camera solve integration,
G-buffer-conditioned rendering, scene-level style anchors that measurably reduce drift.

**Infrastructure:** GPU pool, Temporal cluster, object store, observability, secrets. All boring
on purpose.

Rule: research items may not sit on the critical path of any milestone ≤M7. Every research task
has a written kill criterion ("if no lift by N GPU-weeks, shelve + document").

---

## 8. Solo-Engineer Implementation Order (first ~6 months of commits)

1. **`schemas/` + codegen + CI contract tests** — cheapest day to define contracts is day 1; every later day they're load-bearing.
2. **Event store + content-addressed artifact store** (Postgres + MinIO) — state before behavior.
3. **CLI walking skeleton** with stub adapters → golden-film e2e test in CI — integration risk dies here, forever.
4. **Screenplay parser → world graph projections** — first real intelligence; ClearFrame's existing parser is the seed.
5. **Derivation engine v0** (coarse invalidation) — before more producers exist than you can retrofit.
6. **Render abstraction + image adapter** → storyboards land in the animatic player — first visible product.
7. **TTS dialogue + timing + EDL conform (ffmpeg/OTIO)** → **the animatic milestone**: watchable film, the demo that changes conversations.
8. **Video adapter #1 + N-take fan-out + identity gate** — first moving hero shots, first real quality data.
9. **Zero-shot judge ensemble + selection** — quality loop v0 running on real takes.
10. **Notes schema + invalidation mapping + minimal labeling UI** — the moat's data starts accumulating (earlier than "correct" sequencing would suggest, deliberately: data compounds with calendar time).
11. **Telemetry warehouse + cost dashboards** — you can no longer hold the system in your head; instruments before scale.
12. **Hero path pieces in order of audience impact: mix/ducking → grade → continuity audit → lip-sync.**
13. **CineBench v0** (3 scripts, monthly manual pairwise) — the speedometer, before any tuning claims.

Justifications embedded; the two deliberate inversions vs. "textbook" order: notes/telemetry land
before the hero pipeline (data compounds with time — every week without collection is moat
permanently lost), and CLI precedes any UI (a studio you can script is a studio you can test).

---

## 9. Definition of Done (objective, per subsystem)

| Subsystem | DONE means (all must hold) |
|---|---|
| Schemas | 100% of inter-service payloads validate; breaking change blocked by CI; py+ts types generated in build |
| Production State | event replay reproduces byte-identical projections; branch+merge on golden film passes; 3-hop world queries p95 <100ms; injected contradictions caught 100% |
| Derivation Graph | identical-input cache hit-rate 100% (property test); wardrobe-note test recomputes <15% of derivations; month-long paused job resumes losslessly (Temporal test) |
| Render Abstraction | 2+ adapters pass identical contract-test suite; new-adapter time <1 eng-day (timed, twice); every Take has provenance+cost; canary demotes injected bad adapter in one cycle |
| Craft Systems | each system's output validates against schema on 20-script corpus with 0 crashes; each README declares deletion criterion; policy hot-swap without redeploy |
| Critic | judge-human agreement ≥85% held-out; gate FPR <5% / FNR <10% on labeled artifact set; ranks 100 takes <5 min; calibration report auto-generated monthly |
| Studio UI | script→animatic→notes round-trip without CLI; note→precise-invalidation verified in e2e test; animatic scrub <200ms seek |
| Data Engine | 100% of gates/notes/costs queryable in warehouse <5 min after event; labeling throughput ≥200 takes/hr/rater; one nightly training job ships a policy version end-to-end |
| CineBench | fixed script set + frozen protocol doc; weekly automated run; Elo history plotted; injected regression auto-flagged; inter-rater agreement κ≥0.6 |
| Infra | fresh-machine bootstrap to green e2e <1 hr (scripted); zero secrets in repo (scanner in CI); restore-from-backup drill documented and rehearsed |

---

### Closing rule
V2 stays frozen. Any architecture change requires: (a) a named research breakthrough it responds
to, (b) an ADR, (c) a CineBench-measurable justification. Everything else is implementation —
and implementations are, by construction, disposable.

*— end of engineering plan —*
