#!/usr/bin/env bash
# Asserts the installer layout lets ${CLAUDE_SKILL_DIR}/../../_system resolve.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
BORING_INSTALL_HOME="$TMP" bash "$ROOT/_system/scripts/install.sh" >/dev/null
test -f "$TMP/_system/scripts/brand_context.py" || { echo "FAIL: _system not at \$INSTALL_HOME/_system"; exit 1; }
test -f "$TMP/skills/seo-content/SKILL.md" || { echo "FAIL: skill missing"; exit 1; }
SKILL_DIR="$TMP/skills/seo-content"
test -f "$SKILL_DIR/../../_system/scripts/brand_context.py" || { echo "FAIL: ../../_system does not resolve from a skill dir"; exit 1; }
# Models often rewrite <skill>/../../_system as skills/_system; that copy must run too.
PROJ="$TMP/proj"; mkdir -p "$PROJ/brand"
( cd "$PROJ" && python3 "$TMP/skills/_system/scripts/brand_context.py" --for seo-content ) | grep -q "skill: seo-content" || { echo "FAIL: skills/_system loader copy"; exit 1; }
( cd "$PROJ" && python3 "$TMP/skills/_system/scripts/route.py" --task seo-content ) | grep -q '"task": "seo-content"' || { echo "FAIL: skills/_system route copy"; exit 1; }
DOC="$(BORING_INSTALL_HOME="$TMP" bash "$ROOT/_system/scripts/doctor.sh" 2>&1)" || { echo "FAIL: doctor exit on installed copy"; exit 1; }
grep -q "checks passed" <<<"$DOC" || { echo "FAIL: doctor on installed copy"; exit 1; }
echo "install path OK"
