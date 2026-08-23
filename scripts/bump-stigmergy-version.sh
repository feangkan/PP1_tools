#!/usr/bin/env bash
# Create the next Vn snapshot (Linux / cloud agent). Usage:
#   ./scripts/bump-stigmergy-version.sh "Short description" "v0.9 label"
set -euo pipefail
NOTES="${1:?Notes required}"
INTERNAL="${2:-}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSIONS="$REPO_ROOT/02-assessment-tasks/assessment-1-development/versions"
DEV="$REPO_ROOT/02-assessment-tasks/assessment-1-development"
LATEST_FILE="$VERSIONS/LATEST.txt"
CURRENT=0
[[ -f "$LATEST_FILE" ]] && CURRENT="$(tr -d '[:space:]' < "$LATEST_FILE")"
NEXT=$((CURRENT + 1))
DEST="$VERSIONS/V$NEXT"
if [[ -d "$DEST" ]]; then
  echo "V$NEXT already exists — not overwriting." >&2
  exit 1
fi
mkdir -p "$DEST"
for f in stigmergy-generator.py stigmergy-guide.html stigmergy-how-to.md stigmergy-text-catalog.md; do
  cp "$DEV/$f" "$DEST/$f"
done
COMMIT="$(git -C "$REPO_ROOT" rev-parse --short HEAD)"
echo "$COMMIT" > "$DEST/git-commit.txt"
{
  echo "V$NEXT"
  echo "Notes: $NOTES"
  [[ -n "$INTERNAL" ]] && echo "Internal: $INTERNAL"
  echo "Git: $COMMIT"
} > "$DEST/VERSION.txt"
echo "$NEXT" > "$LATEST_FILE"
echo "Created V$NEXT at $COMMIT — update VERSION-MANIFEST.md, commit, push."
echo "On Windows: .\\scripts\\sync-claude-code-local.ps1"
