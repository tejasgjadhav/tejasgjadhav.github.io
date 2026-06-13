#!/bin/bash
# Runs on every Claude Code web session start — copies project skills to user-level skills dir
set -euo pipefail

# Only run in remote (web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

SKILLS_SRC="$CLAUDE_PROJECT_DIR/.claude/skills"
SKILLS_DEST="$HOME/.claude/skills"

if [ -d "$SKILLS_SRC" ]; then
  for skill_dir in "$SKILLS_SRC"/*/; do
    skill_name=$(basename "$skill_dir")
    dest="$SKILLS_DEST/$skill_name"
    mkdir -p "$dest"
    cp -f "$skill_dir/SKILL.md" "$dest/SKILL.md" 2>/dev/null || true
  done
fi
