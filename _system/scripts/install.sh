#!/usr/bin/env bash
# ============================================================================
# install.sh - 한국 마케팅 스킬 설치
# ============================================================================
# Installs the Korean marketing skill suite into Claude Code's skill directory.
# Skills are discovered dynamically from <repo>/skills/*/SKILL.md — no
# hardcoded roster.
#
# Source layout:                       Installed layout:
#   <repo>/                              $INSTALL_HOME/
#     _system/                             _system/          (<skill>/../../_system)
#     skills/<name>/SKILL.md               skills/_system/   (copy: the path models write)
#                                          skills/<name>/SKILL.md
#
# Usage:
#   ./install.sh                Install full skill suite
#   ./install.sh --claude-only  Skip Replicate-dependent skills (creative)
#
# Environment:
#   BORING_INSTALL_HOME  Override the install root (default: ~/.claude; TVM_INSTALL_HOME still works)
# ============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"        # repo root
SOURCE_SKILLS_DIR="$REPO_ROOT/skills"
SOURCE_SYSTEM_DIR="$REPO_ROOT/_system"
INSTALL_HOME="${BORING_INSTALL_HOME:-${TVM_INSTALL_HOME:-$HOME/.claude}}"
SKILLS_DIR="$INSTALL_HOME/skills"
SYSTEM_DIR="$INSTALL_HOME/_system"   # beside skills/, so <skill>/../../_system resolves
SYSTEM_COPY_DIR="$SKILLS_DIR/_system" # models often rewrite that path as skills/_system
CLAUDE_ONLY=false
VERSION="1.0.0"

# Skills that require a Replicate API token (skipped with --claude-only)
REPLICATE_SKILLS=("creative")

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude-only)
      CLAUDE_ONLY=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--claude-only]"
      echo ""
      echo "Options:"
      echo "  --claude-only  Skip Replicate-dependent skills (${REPLICATE_SKILLS[*]})"
      echo "  --help         Show this help message"
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'"
      echo "Run '$0 --help' for usage."
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

info()    { echo -e "${CYAN}[info]${RESET}  $1"; }
success() { echo -e "${GREEN}[done]${RESET}  $1"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $1"; }

copy_tree() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  if command -v rsync &>/dev/null; then
    rsync -a --exclude='.DS_Store' --exclude='.git' "$src/" "$dst/"
  else
    # Trailing-slash cp -R nests the source directory on some GNU cp builds.
    cp -a "$src/." "$dst/"
    find "$dst" -name '.DS_Store' -delete 2>/dev/null || true
  fi
}

is_replicate_skill() {
  local name="$1"
  for r in "${REPLICATE_SKILLS[@]}"; do
    [[ "$name" == "$r" ]] && return 0
  done
  return 1
}

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  한국 마케팅 스킬 v${VERSION} Installer${RESET}"
echo -e "  ────────────────────────────────────"
echo ""
info "Source:  $REPO_ROOT"
info "Target:  $SKILLS_DIR"
if $CLAUDE_ONLY; then
  warn "Mode:    Claude-only (Replicate-dependent skills excluded)"
else
  info "Mode:    Full suite"
fi
echo ""

# ---------------------------------------------------------------------------
# Validate source tree
# ---------------------------------------------------------------------------
if [[ ! -f "$SOURCE_SYSTEM_DIR/brand-memory.md" ]]; then
  echo "Error: Cannot find _system/brand-memory.md under $REPO_ROOT"
  echo "Run this script from inside the korean-marketing-skills repo."
  exit 1
fi

# ---------------------------------------------------------------------------
# Discover skills dynamically (any skills/*/SKILL.md)
# ---------------------------------------------------------------------------
SKILLS=()
if [[ -d "$SOURCE_SKILLS_DIR" ]]; then
  while IFS= read -r skill_md; do
    SKILLS+=("$(basename "$(dirname "$skill_md")")")
  done < <(find "$SOURCE_SKILLS_DIR" -mindepth 2 -maxdepth 2 -name 'SKILL.md' | sort)
fi

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  warn "No skills found under $SOURCE_SKILLS_DIR (installing _system only)."
fi

# ---------------------------------------------------------------------------
# Install system files
# ---------------------------------------------------------------------------
info "Installing system files..."
for dir in "$SYSTEM_DIR" "$SYSTEM_COPY_DIR"; do
  mkdir -p "$dir"
  copy_tree "$SOURCE_SYSTEM_DIR" "$dir"
  chmod +x "$dir/scripts/"*.sh "$dir/scripts/"*.py 2>/dev/null || true
done
success "_system/ ($(find "$SYSTEM_DIR" -type f | wc -l | tr -d ' ') files)"

# ---------------------------------------------------------------------------
# Install skills
# ---------------------------------------------------------------------------
INSTALLED_COUNT=0
SKIPPED_COUNT=0
for skill in "${SKILLS[@]+"${SKILLS[@]}"}"; do
  if $CLAUDE_ONLY && is_replicate_skill "$skill"; then
    warn "Skipping $skill (--claude-only)"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    continue
  fi
  info "Installing skill: $skill"
  mkdir -p "$SKILLS_DIR/$skill"
  copy_tree "$SOURCE_SKILLS_DIR/$skill" "$SKILLS_DIR/$skill"
  chmod +x "$SKILLS_DIR/$skill/scripts/"*.sh "$SKILLS_DIR/$skill/scripts/"*.py 2>/dev/null || true
  INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
  success "$skill/"
done

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  Installation Complete${RESET}"
echo -e "  ─────────────────────"
echo ""
success "$INSTALLED_COUNT skills installed"
if [[ "$SKIPPED_COUNT" -gt 0 ]]; then
  warn "$SKIPPED_COUNT skills skipped (--claude-only)"
fi
success "Skills: $SKILLS_DIR"
success "System: $SYSTEM_DIR"
echo ""

if ! $CLAUDE_ONLY && [[ -z "${REPLICATE_API_TOKEN:-}" ]]; then
  warn "REPLICATE_API_TOKEN not found in environment."
  warn "The creative skill needs it to generate images/video."
  warn "Set it with: export REPLICATE_API_TOKEN=r8_your_token_here"
  echo ""
fi

echo -e "  Run ${CYAN}doctor.sh${RESET} to verify your installation."
echo ""
