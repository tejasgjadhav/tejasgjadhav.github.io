#!/bin/bash
# Run this once on your local machine to set up ~/.claude/ memory
# Usage: bash setup-local-memory.sh

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
MEMORY_DIR="$CLAUDE_DIR/memory"
HOOKS_DIR="$CLAUDE_DIR/hooks"

echo "Setting up Tejas Jadhav memory vault on this machine..."
echo ""

# Create directories
mkdir -p "$MEMORY_DIR" "$HOOKS_DIR"

# Copy memory files
cp "$REPO_DIR/memory/"*.md "$MEMORY_DIR/"
echo "✓ Copied $(ls "$MEMORY_DIR"/*.md | wc -l | tr -d ' ') memory files to ~/.claude/memory/"

# Copy CLAUDE.md
cp "$REPO_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
echo "✓ CLAUDE.md installed at ~/.claude/CLAUDE.md"

# Install user-level session hook
cat > "$HOOKS_DIR/session-start.sh" << 'HOOK'
#!/bin/bash
# User-level session start — Tejas Jadhav memory

MEMORY_DIR="$HOME/.claude/memory"
COUNT=$(ls "$MEMORY_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')

echo "╔══════════════════════════════════════════════════════╗"
echo "║  TEJAS JADHAV — Memory Loaded                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Memory vault: $COUNT notes at ~/.claude/memory/"
echo "CLAUDE.md: loaded ✓  |  Auto-save: ON"
echo "────────────────────────────────────────────────────────"
HOOK
chmod +x "$HOOKS_DIR/session-start.sh"
echo "✓ Session-start hook installed"

# Install settings.json (user-level)
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
  echo ""
  echo "⚠ ~/.claude/settings.json already exists — not overwriting."
  echo "  Add this hook manually if needed:"
  echo '  "SessionStart": [{"matcher":"","hooks":[{"type":"command","command":"bash $HOME/.claude/hooks/session-start.sh"}]}]'
else
  cat > "$SETTINGS_FILE" << 'SETTINGS'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash $HOME/.claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
SETTINGS
  echo "✓ ~/.claude/settings.json created with session hook"
fi

echo ""
echo "Done! Your local machine now has full memory vault."
echo ""
echo "To keep in sync: git pull in this repo and re-run this script."
echo "Auto-saves during sessions write to memory/conversations.md in the repo."
echo "Commit and push to sync back to GitHub."
