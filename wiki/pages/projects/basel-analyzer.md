---
title: basel-analyzer
type: project
tags: [project, basel, regulatory, llm, refinitiv, banking]
created: 2026-07-06
updated: 2026-07-06
sources: [~/files/basel-analyzer]
---

**basel-analyzer** (`~/files/basel-analyzer`, own git repo, **local-only — no GitHub remote**) is
an LLM-augmented, peer-benchmarked **Basel III / Pillar 3 report analyzer** for
[[tejas-jadhav]]. It ingests a bank's Pillar 3 disclosure and produces a scored, narrated,
peer-benchmarked report. v2 (commit `a0e89ab`) rebuilt it as **deterministic-first**; commit
`8e1833d` added the interactive workflow chart.

## Core design: deterministic-first, degrade gracefully

The pipeline always completes on a deterministic core; three augmentation agents are **optional**
and drop out cleanly when their dependency is absent — no hard failure, the flow reroutes through
the surviving agents and still emits a report.

- **LLM Gap-Fill agent** + **LLM Narrative agent** — run `gpt-oss-120b` via **Ollama**
  (local/GPU), with **[[openrouter]]** as the cloud fallback. Skipped with no model.
- **Refinitiv Benchmark agent** — pulls peer-benchmark data from **Refinitiv ([[lseg]])** via an
  App Key (`lseg-data.config.json`). Skipped with no Workspace/creds.
- "Degraded · no GPU · no Workspace" mode runs deterministic-only.

## Pipeline (9 agents, flow order)

Ingest → **Deterministic Extractor** (*ground truth*) → LLM Gap-Fill (opt) → Reconciliation
Engine → Ratios/Gaps/Horizon → Refinitiv Benchmark (opt) → Scoring → LLM Narrative (opt) →
Report Assembler. The deterministic extractor is the ground-truth source; LLM output is
**reconciled against it, never trusted blindly** — the same honesty-over-optimism discipline
[[tejas-jadhav]] applies to the [[trading-strategies]] work.

## Artifacts

- `analyze.py` / `workflow.py` — entry points.
- `workflow-chart.html` — self-contained interactive agent-wise chart (one card per agent,
  color-coded by owner, provenance tags `deterministic`/`llm`/`refinitiv`/`derived`, and a
  run-mode toggle that dims the three optional agents to visualise degraded mode). Linked from
  README, verified in-browser (9 cards, 0 console errors).
- Repo dirs: `basel_analyzer/`, `llm/`, `benchmarks/`, `config/`, `samples/`, `tests/`, `out/`,
  `cache/`; `HANDOFF.md` holds session state.

Shares the [[lseg]] data dependency with [[endowment-advisor]].
