#!/bin/bash
# Repo-level session start — syncs repo memory → ~/.claude/ (repo is source of truth)

REPO_MEMORY="$(pwd)/memory"
USER_MEMORY="$HOME/.claude/memory"
USER_CLAUDE_MD="$HOME/.claude/CLAUDE.md"
REPO_CLAUDE_MD="$(pwd)/CLAUDE.md"

mkdir -p "$USER_MEMORY"

# Sync repo memory files → ~/.claude/memory/
if [ -d "$REPO_MEMORY" ]; then
  cp "$REPO_MEMORY"/*.md "$USER_MEMORY/" 2>/dev/null
fi

# Sync CLAUDE.md → ~/.claude/CLAUDE.md
if [ -f "$REPO_CLAUDE_MD" ]; then
  cp "$REPO_CLAUDE_MD" "$USER_CLAUDE_MD"
fi

COUNT=$(ls "$USER_MEMORY"/*.md 2>/dev/null | wc -l | tr -d ' ')

echo "╔══════════════════════════════════════════════════════╗"
echo "║  TEJAS JADHAV — Memory Loaded                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Synced: repo/memory/ → ~/.claude/memory/ ($COUNT notes)"
echo "CLAUDE.md: loaded ✓"
echo ""
echo "Memory files:"
for f in "$USER_MEMORY"/*.md; do
  [ -f "$f" ] && echo "  • $(basename "$f" .md)"
done
echo ""
echo "Auto-save is ON — memories saved automatically."
echo "────────────────────────────────────────────────────────"
