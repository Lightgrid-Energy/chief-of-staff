#!/usr/bin/env bash
# Lightgrid Energy — AI Chief of Staff Installer
# Copies system files into ~/.claude/ for use with Claude Code

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo -e "${GREEN}AI Chief of Staff — Install${NC}"
echo "Installing to: $CLAUDE_DIR"
echo ""

# Create directories
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/contacts"
mkdir -p "$CLAUDE_DIR/task-outputs"
mkdir -p "$CLAUDE_DIR/docs"

# Copy files (skip if target already exists and is newer)
copy_if_older() {
  local src="$1"
  local dst="$2"
  if [ ! -f "$dst" ] || [ "$src" -nt "$dst" ]; then
    cp "$src" "$dst"
    echo -e "  ${GREEN}✓${NC} $(basename $dst)"
  else
    echo -e "  ${YELLOW}~${NC} $(basename $dst) (up to date)"
  fi
}

echo "Core files:"
copy_if_older "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
copy_if_older "$SCRIPT_DIR/goals.yaml" "$CLAUDE_DIR/goals.yaml"
copy_if_older "$SCRIPT_DIR/my-tasks.yaml" "$CLAUDE_DIR/my-tasks.yaml"

echo ""
echo "Commands:"
for f in "$SCRIPT_DIR/commands/"*.md; do
  copy_if_older "$f" "$CLAUDE_DIR/commands/$(basename $f)"
done

echo ""
echo "Docs:"
for f in "$SCRIPT_DIR/docs/"*.md; do
  copy_if_older "$f" "$CLAUDE_DIR/docs/$(basename $f)"
done

echo ""
echo -e "${GREEN}Done.${NC} System installed to ~/.claude/"
echo ""
echo "Next steps:"
echo "  1. Edit ~/.claude/CLAUDE.md — fill in all CUSTOMIZE sections"
echo "  2. Edit ~/.claude/goals.yaml — set your actual Q2 goals"
echo "  3. Connect MCP servers — see ~/.claude/docs/mcp-setup.md"
echo "  4. Open Claude Code and try: /gm"
