# CLAUDE.md — Wiki Schema

This directory is an **LLM Wiki**: a persistent, agent-maintained knowledge base covering
all projects in `~/files` (current and future) plus anything else the user feeds it.
Pattern source: [sources/llm-wiki.md](sources/llm-wiki.md) (Karpathy). The LLM writes and
maintains everything here; the user curates sources and asks questions.

## Layout

```
wiki/
  CLAUDE.md          this schema — conventions + workflows
  index.md           content catalog of every page, grouped by type (update on every change)
  log.md             append-only chronological record of operations
  graph.html         GENERATED interactive link-graph view — never edit by hand
  tools/build_graph.py   regenerates graph.html from the current pages
  sources/           immutable raw inputs — NEVER edit files here
  pages/
    projects/        one page per project under ~/files
    concepts/        cross-project ideas, patterns, decisions
    entities/        tools, APIs, services, people
    syntheses/       durable answers filed back from queries
```

## Page format

Every page under `pages/` starts with YAML frontmatter, then a markdown body:

```markdown
---
title: Human-readable title
type: project | concept | entity | source | synthesis
tags: [comma, separated]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [paths or URLs this page draws on]
---

Body. Link other pages with [[wikilinks]] using the page's filename without .md,
e.g. [[institutional-trader]]. Link liberally — a link to a page that doesn't exist
yet marks something worth writing, not an error.
```

Conventions:
- Filenames: short-kebab-case, unique across all of `pages/` (wikilinks resolve by filename).
- Bump `updated` whenever a page's body changes.
- State facts with dates when they may go stale ("as of 2026-07, …").
- When new information contradicts an existing claim, don't silently overwrite —
  note the contradiction on the page and resolve it, or flag it for the next lint.

## Workflows

### Ingest (new source or new information)
1. If the source is a file/URL, save a copy verbatim into `sources/` (immutable).
2. Read it. Create or update **every** page the new information affects — typically
   several pages, not one. Add cross-references both ways.
3. New project appearing under `~/files`? Give it a `pages/projects/<name>.md` page.
4. Update `index.md` (add/adjust entries and one-line summaries).
5. Append a `log.md` entry.
6. Refresh the graph: `python3 tools/build_graph.py` (it also warns on broken links).
7. **Push** (standing preference — always publish): `tools/wiki_push.sh "wiki: <summary>"`.
   Publishes to the public github.io remote. Safe by construction (secret-scan, wiki-only stage,
   rebase-onto-remote). If it reports a possible secret or a rebase conflict, STOP and tell the user.

### Query (answer a question from the wiki)
1. Read `index.md` first to find relevant pages; drill into those pages.
2. Fall back to `sources/` or the actual project directories only when pages don't cover it.
3. Answer with citations to the pages used.
4. If the answer is durable (a comparison, analysis, discovered connection), file it as a
   page under `pages/syntheses/`, index it, and log it. Chat-only answers don't compound.

### Lint (health check)
Scan for: contradictions between pages · broken or one-way `[[wikilinks]]` · orphan pages
(no inbound links) · stale `updated` dates vs. reality of the project dirs · pages missing
from `index.md` or index entries whose page is gone · concepts mentioned often but lacking
their own page. Fix what's mechanical, report what needs the user's judgment, then log the
pass, refresh the graph (`python3 tools/build_graph.py`), and **push**
(`tools/wiki_push.sh "wiki: lint <summary>"`).

## log.md entry format

Append-only. Consistent prefix so it's greppable (`grep "^## \[" log.md | tail -5`):

```
## [YYYY-MM-DD] ingest|query|lint | short title
One or two lines: what was done, which pages were touched.
```

## Ground rules

- `sources/` is immutable; everything else in `wiki/` is yours to maintain.
- Never let `index.md` or `log.md` drift — they are updated in the same pass as the pages.
- Keep pages concise and factual; the value is in the links and the currency, not length.
- The wiki lives in the `~/files` git repo — commits are welcome after substantial passes.
