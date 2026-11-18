#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/brands/acme" "$TMP/brands/northwind" "$TMP/campaigns/x"; echo acme > "$TMP/brands/active"
PRE=$(python3 -c "import json;print(json.load(open('$ROOT/automations/hooks/hooks.json'))['hooks']['PreToolUse'][0]['hooks'][0]['command'])")
POST=$(python3 -c "import json;print(json.load(open('$ROOT/automations/hooks/hooks.json'))['hooks']['PostToolUse'][0]['hooks'][0]['command'])")
# cross-client write must be blocked (exit 2)
set +e; echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"file_path\":\"$TMP/brands/northwind/voice-profile.md\"}}" | bash -c "$PRE"; rc=$?; set -e
[ "$rc" -eq 2 ] || { echo "FAIL: cross-client write not blocked (rc=$rc)"; exit 1; }
# active-client write allowed (exit 0)
echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"file_path\":\"$TMP/brands/acme/voice-profile.md\"}}" | bash -c "$PRE"
# asset manifest appends once
echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"file_path\":\"$TMP/campaigns/x/post.md\"}}" | bash -c "$POST"
echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"file_path\":\"$TMP/campaigns/x/post.md\"}}" | bash -c "$POST"
[ "$(grep -c 'campaigns/x/post.md' "$TMP/brands/acme/assets.md")" -eq 1 ] || { echo "FAIL: asset manifest"; exit 1; }
# Bash-path isolation: a shell redirect into a non-active client must be blocked too
PREB=$(python3 -c "import json;print(json.load(open('$ROOT/automations/hooks/hooks.json'))['hooks']['PreToolUse'][1]['hooks'][0]['command'])")
set +e; echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"command\":\"printf hello > $TMP/brands/northwind/x.md\"}}" | bash -c "$PREB"; rc=$?; set -e
[ "$rc" -eq 2 ] || { echo "FAIL: bash cross-client write not blocked (rc=$rc)"; exit 1; }
echo "{\"cwd\":\"$TMP\",\"tool_input\":{\"command\":\"cat brands/acme/brand.yaml && ls brands/active\"}}" | bash -c "$PREB"
echo "hooks bash-path OK"
echo "hooks OK"
