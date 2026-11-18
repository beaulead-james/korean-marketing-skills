#!/usr/bin/env bash
# ============================================================================
# package.sh - 한국 마케팅 스킬 패키지
# ============================================================================
# Builds the distributable zip: plugin manifest, skills, system core,
# automations, and customer docs. Verifies the zip's file manifest against
# the staged source after building.
#
# Included:  .claude-plugin/  skills/  _system/  automations/
#            README.md  SYSTEM-GUIDE.md  TOOLS.md  CHANGELOG.md
# Excluded:  PROVENANCE.md, tests/, .github/, internal/ (repo-only),
#            _system/scripts/outputs/ (build artifacts), .DS_Store, .env*,
#            __pycache__, *.pyc, .git
#
# Usage:
#   ./package.sh                 Build into _system/scripts/outputs/
#   ./package.sh --output-dir D  Custom output directory
#
# Output:
#   korean-marketing-skills-1.0.0.zip (top-level dir inside: korean-marketing-skills/)
# ============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"          # repo root
PACKAGE_NAME="korean-marketing-skills-$(tr -d "[:space:]" < "$REPO_ROOT/_system/VERSION")"
STAGE_TOP="korean-marketing-skills"
OUTPUT_DIR="$SCRIPT_DIR/outputs"

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [--output-dir PATH]"
      echo ""
      echo "Options:"
      echo "  --output-dir PATH  Directory for the output zip"
      echo "                     (default: _system/scripts/outputs/)"
      echo "  --help             Show this help message"
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'"
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BOLD="\033[1m"
GREEN="\033[0;32m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

info()    { echo -e "  ${CYAN}[info]${RESET}  $1"; }
success() { echo -e "  ${GREEN}[done]${RESET}  $1"; }
fail()    { echo -e "  ${RED}[fail]${RESET}  $1"; }

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  한국 마케팅 스킬 - Packager${RESET}"
echo -e "  ────────────────────────────────────"
echo ""
info "Source:  $REPO_ROOT"
info "Output:  $OUTPUT_DIR/${PACKAGE_NAME}.zip"
echo ""

# ---------------------------------------------------------------------------
# Preflight: required top-level pieces must exist
# ---------------------------------------------------------------------------
REQUIRED_PATHS=(
  ".claude-plugin/plugin.json"
  ".claude-plugin/marketplace.json"
  "README.md"
  "SYSTEM-GUIDE.md"
  "TOOLS.md"
  "CHANGELOG.md"
  "_system/CONVENTIONS.md"
  "_system/brand-memory.md"
  "_system/output-format.md"
  "_system/scripts/install.sh"
  "_system/scripts/doctor.sh"
  "_system/scripts/brand_context.py"
  "automations/README.md"
  "automations/hooks/hooks.json"
  "skills/start-here/SKILL.md"
  "agents/research.md"
)
PRE_FAIL=0
for p in "${REQUIRED_PATHS[@]}"; do
  if [[ ! -f "$REPO_ROOT/$p" ]]; then
    fail "Missing required file: $p"
    PRE_FAIL=1
  fi
done
if [[ "$PRE_FAIL" -ne 0 ]]; then
  fail "Preflight failed — fix missing files before packaging."
  exit 1
fi
SKILL_COUNT=$(find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -name 'SKILL.md' | wc -l | tr -d ' ')
success "Preflight passed ($SKILL_COUNT skills found)"

# ---------------------------------------------------------------------------
# Stage
# ---------------------------------------------------------------------------
STAGE_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/boring-package.XXXXXX")"
STAGE_DIR="$STAGE_ROOT/$STAGE_TOP"
mkdir -p "$STAGE_DIR"
trap 'rm -rf "$STAGE_ROOT"' EXIT

RSYNC_EXCLUDES=(
  --exclude='.DS_Store'
  --exclude='.git'
  --exclude='.env'
  --exclude='.env.*'
  --exclude='__pycache__'
  --exclude='*.pyc'
  --exclude='_system/scripts/outputs'
)

info "Staging distribution tree..."
STAGE_SOURCES=(
  "$REPO_ROOT/.claude-plugin"
  "$REPO_ROOT/skills"
  "$REPO_ROOT/agents"
  "$REPO_ROOT/_system"
  "$REPO_ROOT/automations"
  "$REPO_ROOT/README.md"
  "$REPO_ROOT/SYSTEM-GUIDE.md"
  "$REPO_ROOT/TOOLS.md"
  "$REPO_ROOT/CHANGELOG.md"
)
if command -v rsync >/dev/null 2>&1; then
  rsync -a "${RSYNC_EXCLUDES[@]}" "${STAGE_SOURCES[@]}" "$STAGE_DIR/"
else
  for src in "${STAGE_SOURCES[@]}"; do
    base="$(basename "$src")"
    if [[ -d "$src" ]]; then
      mkdir -p "$STAGE_DIR/$base"
      cp -a "$src/." "$STAGE_DIR/$base/"
    else
      cp -a "$src" "$STAGE_DIR/"
    fi
  done
  rm -rf "$STAGE_DIR/_system/scripts/outputs"
fi

# Belt-and-braces: internal docs and dev artifacts must not ship
rm -f "$STAGE_DIR/V3-DESIGN.md"
rm -rf "$STAGE_DIR/tests" "$STAGE_DIR/.github" "$STAGE_DIR/PROVENANCE.md" "$STAGE_DIR/internal"
find "$STAGE_DIR" \( -name '.DS_Store' -o -name '*.pyc' -o -name '.env' -o -name '.env.*' \) -delete 2>/dev/null || true
find "$STAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true

# Scripts must ship executable
chmod +x "$STAGE_DIR/_system/scripts/"*.sh "$STAGE_DIR/_system/scripts/"*.py 2>/dev/null || true
find "$STAGE_DIR/skills" -path '*/scripts/*' -type f \( -name '*.sh' -o -name '*.py' \) -exec chmod +x {} + 2>/dev/null || true

STAGED_COUNT=$(find "$STAGE_DIR" -type f | wc -l | tr -d ' ')
success "Staged $STAGED_COUNT files"

# ---------------------------------------------------------------------------
# Build zip
# ---------------------------------------------------------------------------
mkdir -p "$OUTPUT_DIR"
ZIP_PATH="$OUTPUT_DIR/${PACKAGE_NAME}.zip"
rm -f "$ZIP_PATH"

info "Building zip..."
( cd "$STAGE_ROOT" && zip -r -q -X "$ZIP_PATH" "$STAGE_TOP" )
success "Built $ZIP_PATH"

# ---------------------------------------------------------------------------
# Manifest verification: zip contents vs staged source
# ---------------------------------------------------------------------------
info "Verifying manifest..."
STAGED_LIST="$STAGE_ROOT/staged.list"
ZIPPED_LIST="$STAGE_ROOT/zipped.list"
( cd "$STAGE_ROOT" && find "$STAGE_TOP" -type f | sort > "$STAGED_LIST" )
zipinfo -1 "$ZIP_PATH" | grep -v '/$' | sort > "$ZIPPED_LIST"

if diff -q "$STAGED_LIST" "$ZIPPED_LIST" >/dev/null; then
  success "Manifest verified: $(wc -l < "$ZIPPED_LIST" | tr -d ' ') files in zip match staged source"
else
  fail "Manifest mismatch between staged source and zip:"
  diff "$STAGED_LIST" "$ZIPPED_LIST" | sed 's/^/    /' || true
  exit 1
fi

# Spot-check: required files present, excluded files absent
VERIFY_FAIL=0
for p in "${REQUIRED_PATHS[@]}"; do
  if ! grep -qxF "$STAGE_TOP/$p" "$ZIPPED_LIST"; then
    fail "Required file missing from zip: $p"
    VERIFY_FAIL=1
  fi
done
for bad in "V3-DESIGN.md" ".DS_Store" ".env" "__pycache__" ".pyc"; do
  if grep -q "$bad" "$ZIPPED_LIST"; then
    fail "Excluded artifact found in zip (pattern: $bad)"
    VERIFY_FAIL=1
  fi
done
if [[ "$VERIFY_FAIL" -ne 0 ]]; then
  exit 1
fi
success "Spot checks passed (required files present, internal artifacts absent)"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1 | tr -d ' ')
FILE_COUNT=$(wc -l < "$ZIPPED_LIST" | tr -d ' ')
echo ""
echo -e "${BOLD}  Package Complete${RESET}"
echo -e "  ────────────────"
echo ""
success "Archive:  $ZIP_PATH"
success "Files:    $FILE_COUNT"
success "Size:     $ZIP_SIZE"
success "Skills:   $SKILL_COUNT"
echo ""
