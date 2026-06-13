# Key Conversations & Decisions

**Type:** Memory · Session Log  
**Tags:** #memory #sessions #decisions #insights

---

Key insights, decisions, and outcomes from past Claude sessions with [[profile|Tejas Jadhav]].

*This file is the running log of important things learned, decided, or created across sessions.*

---

## 2026-06-13 — Memory Graph Setup

**Session:** Set up Obsidian-style memory system for persistent context across all Claude sessions.

**Decision:** Rather than a visual web graph, use a `CLAUDE.md` + `memory/` vault approach so memory works natively in Claude Code, Cowork, and can be imported into Claude Projects for chat.

**Files created:**
- `CLAUDE.md` — always-loaded session context
- `memory/*.md` — detailed knowledge vault (11 files)
- `.claude/settings.json` — SessionStart hook to surface memory
- `.claude/hooks/session-start.sh` — prints memory status at session start

**Key insight:** `CLAUDE.md` is Claude Code's native memory mechanism — it's read at every web session start automatically. The `memory/` directory holds all detail. This is better than a custom web app.

---

*Add new entries below as sessions produce important decisions or insights.*

## Template for new entries

```
## YYYY-MM-DD — Session Topic

**Context:** What we were working on
**Decision:** Key decision made
**Outcome:** What was built/changed/learned
**Next:** What to do next time
```
