# KALPANA — ENGINEERING CONSTITUTION
### v1.0 · 2026-07 · Ratified alongside BLUEPRINT.md, DESIGN-REVIEW-V2.md, ENGINEERING-PLAN.md
Every contribution — human or AI — is bound by this document. Amendments require an ADR.
A rule that cannot be checked in CI or code review is a wish; wherever possible, each article
names its enforcement mechanism.

---

## Article 1 — Core Philosophy

1.1 **The objective is the film.** Every line of code is justified by its effect on final film
quality, measured by CineBench. Code that cannot trace to that objective does not merge.
1.2 **Contracts outlive implementations.** We are building a decade-long system out of parts
with two-year lifespans. Interfaces are the asset; implementations are consumables.
1.3 **Boring by default.** Choose the most boring technology that meets the measured need.
Novelty must buy a measurable capability, documented in an ADR.
1.4 **Evidence over opinion.** Disagreements resolve by measurement (benchmark, profile, A/B),
not seniority. If it can't be measured yet, build the measurement first.
1.5 **Delete proudly.** Removed code is a contribution. The Absorption Doctrine (Article 20)
makes deletion a designed outcome, not a failure.
1.6 **Usable at every milestone.** The product must build a watchable film at all times
(`kalpana make` green on main). No milestone leaves the system in a torn-down state.

## Article 2 — Interface-First Design

2.1 New capability = schema first, implementation second. The schema PR merges before or with
the first producer/consumer, never after.
2.2 Every subsystem interaction goes through generated SDK types. Direct dict/JSON passing
between services is a CI failure (type-check gate).
2.3 An interface is designed for its *second* implementation: if you cannot describe a plausible
alternative implementation, the interface is too specific — it is leaking implementation.
2.4 Human interfaces count: CLI flags and Studio UI actions are contracts too; breaking them
follows the same deprecation policy (Article 16).

## Article 3 — Stable Contracts vs Replaceable Implementations

3.1 **Frozen tier** (change requires ADR + major version): EventRecord, StateQuery/View,
Derivation, ShotPackage, Take, CritiqueReport, Note, ModelAdapter, policy formats.
3.2 **Stable tier** (additive evolution, minor version): craft-system inputs/outputs, warehouse
schemas, CLI surface.
3.3 **Free tier** (change at will): everything inside a service boundary.
3.4 Schema evolution is additive-only within a major version: new optional fields yes; renames,
removals, semantic changes no. Breaking change = new major + a shim that translates old↔new,
kept until deprecation completes.
3.5 Every frozen-tier schema has a versioned JSON Schema file, golden example payloads, and a
round-trip test (`example → parse → serialize → identical`).

## Article 4 — Architecture Decision Records

4.1 An ADR is required for: any frozen-tier change; any new external dependency (service, model
provider, database); any technology swap; any deviation from ENGINEERING-PLAN.md; any numeric
trigger crossing (Article 8).
4.2 Format (one page max): Context → Options considered (≥2) → Decision → Consequences →
**Reversal criterion** (what evidence would undo this).
4.3 ADRs are immutable once accepted; superseding requires a new ADR that links back.
4.4 `docs/adr/` is part of the reviewable diff — an unrecorded architectural decision is a defect.

## Article 5 — Coding Standards

5.1 Python: uv-managed, ruff (lint+format) clean, mypy --strict on `packages/` and service
boundaries, pydantic models generated from schemas only (no hand-written duplicates).
TypeScript: strict mode, eslint clean, types imported from generated SDK only.
5.2 No hand-rolled parsing/serialization of contract types. No stringly-typed IDs — typed ID
wrappers everywhere (`ShotId`, not `str`).
5.3 Comments state constraints the code cannot (invariants, ordering requirements, ToS limits) —
never narration of the obvious. Every module docstring links the plan section it implements.
5.4 Function size, naming, and structure follow the surrounding file. Consistency beats personal
style; style arguments are settled by the formatter, permanently.
5.5 Errors: fail loudly with typed exceptions at boundaries; never swallow; every retry has a
bounded budget and lands in the event log.

## Article 6 — Repository Organization

6.1 One monorepo. The layout in ENGINEERING-PLAN.md §3 is normative; new top-level directories
require an ADR.
6.2 Dependency direction is enforced (import-linter in CI): `apps → services → packages`;
services never import each other — they speak SDK over the wire; `schemas` imports nothing.
6.3 Each craft system directory contains `README.md` with: purpose, contract references, and its
**deletion criterion** (Article 20). A system without a deletion criterion does not merge.
6.4 No code outside the repo: notebooks, scripts, and experiments live in `research/` (Article 11)
or die.

## Article 7 — Testing Philosophy

7.1 Test the contract, not the implementation: the primary test suite for any subsystem is
runnable against any implementation of its interface (contract tests). Adapter #2 must pass
adapter #1's suite unchanged.
7.2 The **golden film** is the supreme test: `kalpana make` on fixed inputs with stub models must
produce byte-identical artifacts on every commit (determinism harness). Non-determinism is
quarantined behind seeds and recorded in provenance.
7.3 Pyramid: many fast unit tests; contract/integration tests per interface; ONE e2e golden film
per fidelity tier. Slow tests must justify their runtime.
7.4 Every bug fix lands with the test that would have caught it. No exceptions.
7.5 AI outputs are tested by property, not snapshot: schema validity, constraint satisfaction,
metric thresholds — never "expect this exact text/image."
7.6 Injected-failure drills are tests too: degraded adapter, contradictory world-state write,
mid-run kill + resume. They run in CI weekly, not in postmortems.

## Article 8 — Benchmarking & Performance

8.1 CineBench is the only quality number that may be cited without qualification. All tuning
claims reference a CineBench (or subordinate benchmark) delta.
8.2 Performance work requires a profile first; PRs claiming speedups include before/after numbers
on a fixed corpus.
8.3 Numeric upgrade triggers (from ENGINEERING-PLAN §5 ADRs) are monitored, not remembered:
each trigger is a dashboard alert (e.g., world-query p95 >100ms → open the Neo4j ADR).
8.4 Cost is a performance metric: every Take, Derivation, and film carries cost; ₹/finished-minute
per tier is published on the dashboard continuously.

## Article 9 — Quality Gates Before Merge

A PR merges only when ALL hold (CI-enforced):
(a) lint + typecheck + unit + contract tests green;
(b) golden-film e2e green;
(c) schema-compat check green (no breaking change without major bump + shim);
(d) import-direction check green;
(e) secrets scanner green;
(f) coverage on changed lines ≥80% (measured, not aspirational);
(g) if behavior changed: docs updated in the same PR;
(h) if architectural: ADR included;
(i) one reviewer approval — the reviewer's checklist is literally Articles 2, 3, 5, 7 of this
document. AI-authored code is reviewed to the same standard as human code, by a different
author than the generator.

## Article 10 — Documentation Standards

10.1 Docs live in the repo, versioned with the code they describe; stale docs are defects.
10.2 Three canonical layers, no others: `docs/adr/` (decisions), per-package `README.md`
(purpose, contracts, deletion criterion, runbook), and the four root documents (BLUEPRINT,
DESIGN-REVIEW-V2, ENGINEERING-PLAN, this CONSTITUTION).
10.3 Every service README contains a runnable quickstart (`make dev` or equivalent) verified by
CI (docs-test job executes it).
10.4 Write for the engineer who joins in year 5: record *why*, link the plan, name the trade-off.

## Article 11 — Research vs Production Separation

11.1 `research/` is the only home for experimental code: no production imports from it, ever
(import-linter enforced). Promotion to production = rewrite against contracts + tests, not a move.
11.2 Every research project starts with a one-page charter: hypothesis, metric, GPU/time budget,
**kill criterion**. Charters expire; expired projects are archived with a findings note —
negative results are documented, not deleted.
11.3 Research may not sit on the critical path of any milestone ≤M7 (plan §7). A milestone
blocked on research is a planning defect; re-scope the milestone.
11.4 Models are dependencies: research checkpoints never serve production traffic; production
models are versioned, registered, and load through the same adapter/policy interfaces.

## Article 12 — Security

12.1 No secrets in the repo — scanner in CI blocks; credentials live in the secrets manager;
per-provider keys are scoped and rotated on a schedule.
12.2 All user content (scripts, notes, films) is tenant-scoped at the storage layer from day one,
even while single-tenant.
12.3 Prompt-injection boundary: user script text is data, never instructions — craft-system
prompts must structurally separate user content from directives (delimited fields, not
concatenation); a red-team test suite of hostile screenplays runs in CI.
12.4 Generated code/config from AI tools is reviewed like any dependency: least privilege,
sandboxed execution for anything that runs user-influenced content.
12.5 Supply chain: lockfiles committed; dependency update PRs are reviewed, not auto-merged;
provenance (SLSA-style) recorded for release artifacts.

## Article 13 — Privacy & Licensing

13.1 Every asset in every film carries provenance: model, version, seed, license reference —
the license manifest is generated, signed (C2PA), and stored with the master. A film whose
manifest is incomplete does not ship.
13.2 Likeness protection is input AND output: real-person detection on scripts and on generated
faces; user-provided reference likenesses require recorded consent.
13.3 User creative content is never used for training without explicit, revocable, logged opt-in;
the notes/taste corpus is collected under the same consent regime.
13.4 Provider ToS constraints are encoded in the capability registry (machine-checkable), not
in engineers' memories.
13.5 Data deletion requests propagate through the event log via crypto-shredding (per-tenant
keys), preserving log integrity while honoring erasure.

## Article 14 — Observability & Telemetry

14.1 The event log is the primary instrument; if an action isn't in the log, it didn't happen.
Every derivation, gate, note, cost, and model call emits a typed event.
14.2 OpenTelemetry traces span the full pipeline: a single trace follows a shot from ShotPackage
to accepted Take across every service.
14.3 Dashboards are code (versioned); the canonical four: film-build health, quality (CineBench +
gate rates), cost (₹/min by tier), provider health (canaries).
14.4 Alerts have runbooks; an alert without a runbook link is deleted. Pager load is itself a
tracked metric — noisy alerts are defects.

## Article 15 — Versioning

15.1 Schemas: semver per schema family; frozen tier bumps majors only via ADR.
15.2 Services: continuously deployed from main; compatibility guaranteed by schema versions, not
service versions (consumers pin schema majors, not service releases).
15.3 Policies and models: registry-versioned, immutable artifacts; every film records the exact
policy/model versions used (reproducibility: a film can be rebuilt bit-for-bit at draft tier).
15.4 The four root documents carry versions; code may cite them by section (e.g., PLAN §5).

## Article 16 — Deprecation Policy

16.1 Deprecation = announce (changelog + runtime warning) → dual-support window (shim) → measure
zero usage via telemetry → remove. Nothing is removed while the log shows callers.
16.2 Default windows: frozen-tier contracts 2 minors or 90 days (whichever longer); CLI/UI
surfaces 30 days; internal free-tier: none needed.
16.3 Every shim has an owner and an expiry issue filed at creation — shims are debt with a due date.

## Article 17 — Dependency Management

17.1 Adding a dependency is a decision: prefer stdlib > existing dep > new dep; new runtime
dependencies in `packages/` or `services/` require reviewer sign-off naming the alternative
considered (one line in the PR is enough; new *infrastructure* requires an ADR).
17.2 Pin everything (uv/pnpm lockfiles); scheduled update PRs weekly; a dependency that blocks
an update for >90 days gets an issue to replace or vendor it.
17.3 Model providers are dependencies of the highest risk class: minimum two viable adapters per
shot class at all times (PLAN R2); no craft system may name a provider — only capabilities.

## Article 18 — CI/CD

18.1 CI runs the full Article 9 gate set on every PR; main is always releasable; a red main is
an all-hands-stop defect.
18.2 CD: services deploy from main behind feature flags; risky paths (new adapter, new policy)
ship dark → canary → default, with automated rollback on golden-film or CineBench regression.
18.3 A fresh developer machine reaches a green golden film in ≤1 hour via one scripted command
(tested monthly in CI on a clean container).
18.4 Weekly scheduled jobs are part of CI: CineBench run, failure drills, docs-test, dependency
updates, canary probes.

## Article 19 — Definition of Done

19.1 The per-subsystem DoD tables in ENGINEERING-PLAN §9 are normative and CI-checkable where
possible; "done" claims cite them.
19.2 Universal DoD for any task: code + tests + docs + telemetry + (if applicable) ADR + golden
film green + demo-able from the CLI. If it can't be demonstrated with a command, it isn't done.
19.3 "Done" for research: findings documented against the charter's metric — including negative
results — and the kill/promote decision recorded.

## Article 20 — The Absorption Doctrine

20.1 **Premise:** frontier models will progressively subsume our pipeline stages. This is the
plan, not the threat. We win by riding capability growth with zero rewrites.
20.2 Every craft system and pipeline stage declares in its README a **deletion criterion**: the
external capability that makes it redundant, stated measurably (e.g., Continuity Audit: "a
generator holds cross-shot identity/wardrobe/lighting over ≥10-shot scenes with gate pass ≥99%,
verified on our corpus — then this system becomes a thin verification shim").
20.3 Quarterly **absorption review**: run the deletion-criterion tests against current frontier
models; any criterion met → file the deletion ADR within the quarter. Celebrate in the changelog.
20.4 Absorption mechanics: the replaced system's *interface remains* (Article 3); the frontier
capability is wrapped as the new implementation (usually inside an adapter or a policy); the old
implementation moves to `attic/` for one release, then deletes. Downstream consumers never change.
20.5 What is never absorbed (the permanent core): the Production State and its event log, the
Critic + CineBench (someone must judge, even judging models), the Data Engine and taste corpus,
and the contracts themselves. Investment concentrates there in proportion to everything else
becoming absorbable.
20.6 The corollary duty: never build differentiation *inside* a stage that has a plausible
≤3-year deletion criterion; build it in the permanent core instead.

---

### Ratification
This constitution governs all contributions from commit #1. It is amended only by ADR with the
same rigor it prescribes. Next action per ENGINEERING-PLAN §8: **M0 — `schemas/` package,
event store, walking skeleton.**

*— end of constitution —*
