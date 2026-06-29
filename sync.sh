#!/usr/bin/env bash
# Pull latest changes from ~/.claude/ back into the repo for committing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Syncing from ~/.claude/ -> repo..."

cp "$CLAUDE_DIR/CLAUDE.md" "$SCRIPT_DIR/"
cp "$CLAUDE_DIR/goals.yaml" "$SCRIPT_DIR/"
cp "$CLAUDE_DIR/my-tasks.yaml" "$SCRIPT_DIR/"
cp "$CLAUDE_DIR/commands/"*.md "$SCRIPT_DIR/commands/"
cp "$CLAUDE_DIR/docs/"*.md "$SCRIPT_DIR/docs/" 2>/dev/null || true

echo "Scheduled tasks:"
mkdir -p "$SCRIPT_DIR/scheduled-tasks"
for dir in "$CLAUDE_DIR/scheduled-tasks/"/*/; do
  task=$(basename "$dir")
  mkdir -p "$SCRIPT_DIR/scheduled-tasks/$task"
  cp "$dir/SKILL.md" "$SCRIPT_DIR/scheduled-tasks/$task/SKILL.md"
  echo "  synced: $task"
done

echo "Done. Review changes and commit:"
echo "  git add -A && git commit -m 'update chief-of-staff config'"
