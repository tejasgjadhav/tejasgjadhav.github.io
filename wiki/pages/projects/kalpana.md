---
title: KALPANA — AI film studio engine
type: project
tags: [video, architecture, milestones, determinism, python]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/kalpana/HANDOFF.md]
---

Local-only Python repo at `~/files/kalpana` (uv, Python 3.12 — always `uv run`, system
python is 3.9). The engineered successor to the [[clearframe-studio]] prototype: a full AI
film studio built to a **frozen V2 architecture** — animatic-first, derivation graph,
absorption doctrine, Critic, CineBench, data engine — documented in BLUEPRINT.md,
DESIGN-REVIEW-V2.md and ENGINEERING-PLAN.md.

Execution rules, set by the owner and unusually strict: one milestone at a time, definition
of done before advancing, no architectural change without an ADR plus approval, and **every
milestone plan must name its top three technical risks with explicit validation
strategies** — risks that cannot be validated get recorded as research assumptions, not
stated as engineering facts. That last rule is the same intellectual-honesty pattern that
runs through [[capital-curve-verdict]] and [[trading-strategies]].

State as of 2026-07-10 (session paused by owner):
- **M0 complete** (`198105e`, 20 tests) — frozen-tier v0 schemas, golden examples,
  generated pydantic types, JSONL event store + sha256 content-addressed store (ADR-0001),
  derivation runner with content-addressed caching, stub pipeline, `kalpana make` /
  `kalpana replay`, determinism verified by replay hash-match.
- **M1** — comprehension and production state: real screenplay parser (ported from the
  ClearFrame `ScriptParser`), world-graph projections, contradiction checks, branching v0.
- **M2 complete** (`6d8ef0e`, 96 tests) — capability declarations and provenance records,
  render SDK, capability-driven pluggable router, Pollinations (live-verified) and Runway
  (fixture-tested, key-gated) adapters, fan-out and cost meter, canary demotion drill,
  `kalpana make --boards`.
- **M3 planned, not started** — animatic-first; gated on owner rulings about ffmpeg
  install, player scope, remote/CI, and TTS engine.

Standing requirement from D9: any change to generated code ships with a compatibility
report (added/removed/changed types, schema and serialization compat, migrations). Never
hand-edit `src/kalpana/sdk/models/` — run `scripts/gen_models.sh`.
