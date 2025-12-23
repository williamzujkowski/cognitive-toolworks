#!/bin/bash
# sync-to-claude.sh - Make cognitive-toolworks agents/skills auto-discoverable by Claude Code
#
# This script creates symlinks in ~/.claude/ pointing to cognitive-toolworks
# Run this once after cloning, or after adding new agents/skills
#
# Usage: ./scripts/sync-to-claude.sh [--uninstall]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Uninstall mode
if [[ "$1" == "--uninstall" ]]; then
    echo "Removing cognitive-toolworks symlinks from ~/.claude..."

    # Remove skill symlinks
    for link in "$CLAUDE_DIR/skills"/ct-*; do
        if [[ -L "$link" ]]; then
            rm "$link"
            log_success "Removed $(basename "$link")"
        fi
    done

    # Remove agent symlinks
    for link in "$CLAUDE_DIR/agents"/ct-*.md; do
        if [[ -L "$link" ]]; then
            rm "$link"
            log_success "Removed $(basename "$link")"
        fi
    done

    echo "Done! cognitive-toolworks uninstalled from Claude."
    exit 0
fi

echo "Installing cognitive-toolworks to Claude Code..."
echo "Repository: $REPO_ROOT"
echo ""

# Ensure Claude directories exist
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

# === SKILLS ===
# Claude expects: ~/.claude/skills/<name>/SKILL.md
# We have: repo/skills/<name>/SKILL.md
# Solution: Symlink each skill directory with ct- prefix to avoid conflicts

echo "Syncing skills..."
skill_count=0
for skill_dir in "$REPO_ROOT/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    target="$CLAUDE_DIR/skills/ct-${skill_name}"

    if [[ -L "$target" ]]; then
        # Update existing symlink
        rm "$target"
    elif [[ -e "$target" ]]; then
        log_warn "Skipping $skill_name (non-symlink exists)"
        continue
    fi

    ln -s "$skill_dir" "$target"
    skill_count=$((skill_count + 1))
done
log_success "Linked $skill_count skills"

# === AGENTS ===
# Claude expects: ~/.claude/agents/<name>.md (single file with frontmatter)
# We have: repo/agents/<name>/AGENT.md (directory with AGENT.md inside)
# Solution: Symlink AGENT.md files directly with ct- prefix

echo "Syncing agents..."
agent_count=0
for agent_dir in "$REPO_ROOT/agents"/*/; do
    agent_name=$(basename "$agent_dir")
    agent_file="$agent_dir/AGENT.md"
    target="$CLAUDE_DIR/agents/ct-${agent_name}.md"

    if [[ ! -f "$agent_file" ]]; then
        log_warn "Skipping $agent_name (no AGENT.md)"
        continue
    fi

    if [[ -L "$target" ]]; then
        rm "$target"
    elif [[ -e "$target" ]]; then
        log_warn "Skipping $agent_name (non-symlink exists)"
        continue
    fi

    ln -s "$agent_file" "$target"
    agent_count=$((agent_count + 1))
done
log_success "Linked $agent_count agents"

echo ""
echo "=== Installation Complete ==="
echo "Skills:  $skill_count linked to ~/.claude/skills/ct-*"
echo "Agents:  $agent_count linked to ~/.claude/agents/ct-*.md"
echo ""
echo "All cognitive-toolworks items prefixed with 'ct-' for easy identification."
echo ""
echo "Test with:"
echo "  ls ~/.claude/skills/ct-* | head -5"
echo "  ls ~/.claude/agents/ct-*.md | head -5"
echo ""
echo "To uninstall: $0 --uninstall"
