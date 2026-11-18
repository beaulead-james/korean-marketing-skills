#!/usr/bin/env bash
# ============================================================================
# doctor.sh - Boring Marketing Skills Health Check
# ============================================================================
# Verifies a skill suite (source tree or installed copy): system files
# present, schemas parse, every skill's frontmatter is valid, the shared
# runtime scripts in skills/start-here/scripts match _system/scripts, scripts are
# executable, and optional API keys are reported.
#
# Skills are discovered dynamically — no hardcoded roster. The check root may
# be either layout:
#   source tree:  <root>/_system/  +  <root>/skills/<name>/SKILL.md
#   installed:    <root>/_system/  +  <root>/<name>/SKILL.md
#
# Usage:
#   ./doctor.sh                              Check the source tree this script lives in
#   BORING_INSTALL_HOME=~/.claude ./doctor.sh   Check an installed copy ($BORING_INSTALL_HOME/skills)
#
# Exit codes:
#   0  All required checks passed
#   1  One or more required checks failed
# ============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration — resolve the root to check
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_HOME="${BORING_INSTALL_HOME:-${TVM_INSTALL_HOME:-}}"   # TVM_ is the pre-4.0 name
if [[ -n "$INSTALL_HOME" ]]; then
  ROOT="$INSTALL_HOME/skills"            # installed: skills live here
  SYSTEM_DIR="$INSTALL_HOME/_system"     # installed: system lives beside skills/
else
  ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"    # source tree
  SYSTEM_DIR="$ROOT/_system"
fi
EXPECTED_VERSION="$(cat "$SYSTEM_DIR/VERSION" 2>/dev/null | tr -d '[:space:]' || true)"
EXPECTED_VERSION="${EXPECTED_VERSION:-unknown}"

# Where do skill dirs live? source tree has <root>/skills/, installed is flat.
if [[ -d "$ROOT/skills" ]]; then
  SKILLS_PARENT="$ROOT/skills"
else
  SKILLS_PARENT="$ROOT"
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BOLD="\033[1m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
DIM="\033[2m"
RESET="\033[0m"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

check_pass() { echo -e "  ${GREEN}✓${RESET}  $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
check_fail() { echo -e "  ${RED}✗${RESET}  $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
check_warn() { echo -e "  ${YELLOW}!${RESET}  $1  ${DIM}(optional)${RESET}"; WARN_COUNT=$((WARN_COUNT + 1)); }

check_file() {
  local filepath="$1"
  local label="${2:-$1}"
  if [[ -f "$filepath" ]]; then
    check_pass "$label"
  else
    check_fail "$label  ${DIM}(missing: $filepath)${RESET}"
  fi
}

check_exec() {
  local filepath="$1"
  local label="${2:-$1}"
  if [[ ! -f "$filepath" ]]; then
    check_fail "$label  ${DIM}(missing: $filepath)${RESET}"
  elif [[ -x "$filepath" ]]; then
    check_pass "$label (executable)"
  else
    check_fail "$label  ${DIM}(not executable — run: chmod +x $filepath)${RESET}"
  fi
}

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  Boring Marketing Skills - Doctor${RESET}"
echo -e "  ──────────────────────────────────"
echo ""
echo -e "  ${DIM}Checking root:   $ROOT${RESET}"
echo -e "  ${DIM}System files:    $SYSTEM_DIR${RESET}"
echo -e "  ${DIM}Skills:          $SKILLS_PARENT${RESET}"
echo ""

# ---------------------------------------------------------------------------
# Check 1: System files
# ---------------------------------------------------------------------------
echo -e "${BOLD}  System Files${RESET}"
if [[ ! -d "$SYSTEM_DIR" ]]; then
  check_fail "System directory exists"
  echo ""
  echo -e "  ${RED}System directory not found at $SYSTEM_DIR${RESET}"
  echo -e "  Run install.sh first (or check BORING_INSTALL_HOME)."
  exit 1
fi
check_pass "System directory exists"
check_file "$SYSTEM_DIR/VERSION"           "Version file"
check_file "$SYSTEM_DIR/brand-memory.md"   "Brand memory spec"
check_file "$SYSTEM_DIR/output-format.md"  "Output format spec"
check_file "$SYSTEM_DIR/CONVENTIONS.md"    "Authoring conventions"

# ---------------------------------------------------------------------------
# Check 2: Python availability (needed for schema + frontmatter checks)
# ---------------------------------------------------------------------------
PYTHON=""
if command -v python3 &>/dev/null; then
  PYTHON="python3"
elif command -v python &>/dev/null; then
  PYTHON="python"
fi

# ---------------------------------------------------------------------------
# Check 3: Schemas parse
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  Schemas${RESET}"
SCHEMA_COUNT=0
if [[ -d "$SYSTEM_DIR/schemas" ]]; then
  for schema in "$SYSTEM_DIR/schemas/"*.schema.json; do
    [[ -e "$schema" ]] || continue
    SCHEMA_COUNT=$((SCHEMA_COUNT + 1))
    name="$(basename "$schema")"
    if [[ -n "$PYTHON" ]]; then
      if "$PYTHON" -m json.tool "$schema" >/dev/null 2>&1; then
        check_pass "$name parses"
      else
        check_fail "$name  ${DIM}(invalid JSON)${RESET}"
      fi
    else
      check_warn "$name present (python not found; JSON not validated)"
    fi
  done
  if [[ "$SCHEMA_COUNT" -eq 0 ]]; then
    check_fail "Schemas present  ${DIM}(no *.schema.json in $SYSTEM_DIR/schemas)${RESET}"
  fi
else
  check_fail "Schemas directory exists  ${DIM}(missing: $SYSTEM_DIR/schemas)${RESET}"
fi

# Required schemas
for required in ad-matrix voc brand-manifest; do
  check_file "$SYSTEM_DIR/schemas/$required.schema.json" "Required schema: $required"
done

# ---------------------------------------------------------------------------
# Check 4: Scripts present and executable
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  Scripts${RESET}"
check_exec "$SYSTEM_DIR/scripts/install.sh"        "Installer"
check_exec "$SYSTEM_DIR/scripts/doctor.sh"         "Doctor (this script)"
check_exec "$SYSTEM_DIR/scripts/brand_context.py"  "Brand context loader"
check_exec "$SYSTEM_DIR/scripts/refresh_check.py"  "Freshness checker"

for s in brand_context.py capability.py route.py; do
  vendored="$SKILLS_PARENT/start-here/scripts/$s"
  if [[ ! -f "$vendored" ]]; then
    check_fail "Shared runtime: start-here/scripts/$s  ${DIM}(missing; skills installed with npx skills add call it as a sibling)${RESET}"
  elif [[ -f "$SYSTEM_DIR/scripts/$s" ]] && ! cmp -s "$vendored" "$SYSTEM_DIR/scripts/$s"; then
    check_fail "Shared runtime: start-here/scripts/$s differs from _system/scripts/$s  ${DIM}(copy _system/scripts/$s over it)${RESET}"
  else
    check_pass "Shared runtime: start-here/scripts/$s"
  fi
done

if [[ -z "$PYTHON" ]]; then
  check_warn "python3 not found — brand_context.py and frontmatter checks unavailable"
fi

# ---------------------------------------------------------------------------
# Check 5: Skills — discovered dynamically, frontmatter validated
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  Skills${RESET}"

SKILL_DIRS=()
while IFS= read -r skill_md; do
  SKILL_DIRS+=("$(dirname "$skill_md")")
done < <(find "$SKILLS_PARENT" -mindepth 2 -maxdepth 2 -name 'SKILL.md' -not -path "*/_system/*" 2>/dev/null | sort)

if [[ ${#SKILL_DIRS[@]} -eq 0 ]]; then
  check_warn "No skills found under $SKILLS_PARENT (roster may still be in progress)"
else
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill="$(basename "$skill_dir")"
    if [[ -z "$PYTHON" ]]; then
      check_pass "Skill: $skill (SKILL.md present; frontmatter not validated — no python)"
      continue
    fi
    FM_ERR="$("$PYTHON" - "$skill_dir/SKILL.md" "$EXPECTED_VERSION" <<'PYEOF'
import re, sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read()
lines = text.splitlines()
errors = []

if not lines or lines[0].strip() != "---":
    print("no frontmatter (file must start with ---)")
    sys.exit(1)
end = None
for i in range(1, len(lines)):
    if lines[i].strip() == "---":
        end = i
        break
if end is None:
    print("unterminated frontmatter (no closing ---)")
    sys.exit(1)

fm = "\n".join(lines[1:end])
for key in ("name", "description"):
    if not re.search(rf"^{key}:\s*\S", fm, re.M):
        errors.append(f"missing '{key}:'")
if not re.search(r"^metadata:", fm, re.M):
    errors.append("missing 'metadata:' block")
m = re.search(r"^\s*version:\s*['\"]?([\w.\-]+)['\"]?\s*$", fm, re.M)
if not m:
    errors.append("missing metadata.boring.version")
elif m.group(1) != sys.argv[2]:
    errors.append(f"metadata.boring.version is '{m.group(1)}', expected '{sys.argv[2]}'")

# Strict YAML parsers (the npx skills CLI) skip a skill whose plain scalar holds ": " or " #".
for line in fm.splitlines():
    km = re.match(r"^([A-Za-z_-]+):\s+(.*)$", line)
    if km and km.group(2)[:1] not in "\"'[{|>" and (": " in km.group(2) or " #" in km.group(2)):
        errors.append(f"'{km.group(1)}:' holds ': ' or ' #' unquoted; strict YAML parsers skip this skill (quote the value or use a period)")

if errors:
    print("; ".join(errors))
    sys.exit(1)
PYEOF
)" && FM_OK=true || FM_OK=false
    if $FM_OK; then
      check_pass "Skill: $skill (frontmatter valid, version $EXPECTED_VERSION)"
    else
      check_fail "Skill: $skill  ${DIM}($FM_ERR)${RESET}"
    fi
    # Portability: npx skills add copies skill folders only, so ../../_system never arrives.
    if grep -q '/\.\./\.\./_system/' "$skill_dir/SKILL.md"; then
      check_warn "Skill: $skill points at ../../_system/ (breaks outside the Claude Code plugin; use \${CLAUDE_SKILL_DIR}/../start-here/scripts/, CONVENTIONS §3)"
    fi
    # Per-skill scripts, if any, must be executable
    if [[ -d "$skill_dir/scripts" ]]; then
      while IFS= read -r s; do
        if [[ ! -x "$s" ]]; then
          check_fail "Skill script not executable: ${s#"$SKILLS_PARENT"/}"
        fi
      done < <(find "$skill_dir/scripts" -type f \( -name '*.sh' -o -name '*.py' \) 2>/dev/null)
    fi
  done
fi

# ---------------------------------------------------------------------------
# Check 6: Optional API keys
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}  API Keys (optional)${RESET}"
if [[ -n "${REPLICATE_API_TOKEN:-}" ]]; then
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
    -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
    "https://api.replicate.com/v1/account" 2>/dev/null || echo "000")
  if [[ "$HTTP_STATUS" == "200" ]]; then
    check_pass "Replicate API token valid"
  elif [[ "$HTTP_STATUS" == "000" ]]; then
    check_warn "Replicate API - could not reach api.replicate.com"
  else
    check_warn "Replicate API token present but returned HTTP $HTTP_STATUS"
  fi
else
  check_warn "REPLICATE_API_TOKEN not set (needed for /creative)"
fi

if [[ -n "${FIRECRAWL_API_KEY:-}" ]]; then
  check_pass "FIRECRAWL_API_KEY set (enhanced scraping available)"
else
  check_warn "FIRECRAWL_API_KEY not set (research skills fall back to WebFetch/WebSearch)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
TOTAL=$((PASS_COUNT + FAIL_COUNT))
echo ""
echo -e "  ──────────────────────────────────"
echo ""

if [[ "$FAIL_COUNT" -eq 0 ]]; then
  echo -e "  ${GREEN}${BOLD}All $PASS_COUNT checks passed.${RESET}"
  if [[ "$WARN_COUNT" -gt 0 ]]; then
    echo -e "  ${YELLOW}$WARN_COUNT optional warnings.${RESET}"
  fi
  echo ""
  exit 0
else
  echo -e "  ${RED}${BOLD}$FAIL_COUNT of $TOTAL checks failed.${RESET}"
  if [[ "$WARN_COUNT" -gt 0 ]]; then
    echo -e "  ${YELLOW}$WARN_COUNT optional warnings.${RESET}"
  fi
  echo ""
  echo -e "  Run ${CYAN}install.sh${RESET} to fix missing files."
  echo ""
  exit 1
fi
