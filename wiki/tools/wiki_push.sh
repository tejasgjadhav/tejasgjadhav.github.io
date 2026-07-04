#!/usr/bin/env bash
# Safely commit + push ONLY the wiki/ subtree of the ~/files repo (which is the public
# tejasgjadhav.github.io site). Handles: secret scan, .env guard, .DS_Store exclusion, and
# rebase-onto-remote (the github.io repo is updated by other processes, so a plain push fails).
# Usage: wiki_push.sh ["commit message"]
set -uo pipefail
REPO="/Users/sayali/files"
cd "$REPO" || { echo "wiki-push: cannot cd $REPO"; exit 1; }

# 1) SECRET SCAN — block real credential assignments / private keys (prose like "api_secret for
#    an access_token" is fine; only VALUE assignments of 16+ chars or key headers abort).
if grep -rInE "(api[_-]?secret|access[_-]?token|api[_-]?key|password)[\"' ]*[:=][\"' ]*[A-Za-z0-9_-]{16,}|-----BEGIN (RSA|OPENSSH|PRIVATE)" wiki/ 2>/dev/null; then
  echo "wiki-push: ABORT — a possible secret was found in wiki/ (shown above). Not pushing."; exit 1
fi

# 2) Commit wiki/ changes (if any), wiki-only, no .DS_Store, never .env
if [ -n "$(git status --porcelain wiki/ | grep -v '\.DS_Store')" ]; then
  git add wiki/
  git reset -q -- 'wiki/.DS_Store' 'wiki/**/.DS_Store' 2>/dev/null || true
  if git diff --cached --name-only | grep -qE '\.env$|kite_access'; then
    echo "wiki-push: ABORT — .env/secret staged."; git reset -q; exit 1
  fi
  MSG="${1:-wiki: update $(date +%Y-%m-%d)}"
  git commit -q -m "$MSG" || true
fi

# 3) Nothing to push?
if [ -z "$(git log --oneline @{u}..HEAD 2>/dev/null)" ] && git diff --quiet @{u} 2>/dev/null; then
  echo "wiki-push: nothing to push (up to date)"; exit 0
fi

# 4) Push, rebasing onto the concurrently-updated remote. Stash any unrelated working changes.
STASHED=0
if [ -n "$(git status --porcelain)" ]; then git stash push -u -q -m wiki-push-wip && STASHED=1; fi
git fetch -q origin
if ! git rebase -q origin/main; then
  git rebase --abort 2>/dev/null
  [ "$STASHED" -eq 1 ] && git stash pop -q
  echo "wiki-push: ABORT — rebase conflict with remote; resolve manually."; exit 1
fi
if git push -q origin main; then echo "wiki-push: pushed to origin/main ✓"; RC=0; else echo "wiki-push: push failed"; RC=1; fi
[ "$STASHED" -eq 1 ] && git stash pop -q || true
exit ${RC:-0}
