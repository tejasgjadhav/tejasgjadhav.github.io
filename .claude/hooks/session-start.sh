#!/bin/bash
# Session start hook — surfaces memory vault status for Tejas Jadhav

MEMORY_DIR="$(dirname "$0")/../../memory"
CLAUDE_MD="$(dirname "$0")/../../CLAUDE.md"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  TEJAS JADHAV — Memory Graph Loaded                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Count memory files
if [ -d "$MEMORY_DIR" ]; then
  COUNT=$(ls "$MEMORY_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "Memory vault: $COUNT notes loaded from /memory/"
  echo ""
  echo "Available memory files:"
  for f in "$MEMORY_DIR"/*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f" .md)
    echo "  • $name"
  done
else
  echo "Memory vault not found. Expected: /memory/"
fi

echo ""
echo "CLAUDE.md: $([ -f "$CLAUDE_MD" ] && echo 'loaded ✓' || echo 'not found')"
echo ""
echo "To save a memory: create or edit a file in /memory/"
echo "To update context: edit CLAUDE.md"
echo "────────────────────────────────────────────────────────"
