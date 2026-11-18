#!/usr/bin/env bash
# check_banned.sh [dir] — fail if internal, private or vendor terms appear in the tree.
#   1. internal names and the private measurement path (anywhere)
#   2. privacy terms: client names, author paths, ad account IDs, conversion labels (anywhere)
#   3. vendor names, outside the files allowed to name the vendor
#   4. boringfunnels, only on a line that carries the house-tool disclosure (CONVENTIONS §13)
set -uo pipefail
ROOT="${1:-.}"
EXCL=(--exclude-dir=.git --exclude-dir=internal --exclude-dir=node_modules --exclude-dir=__pycache__ --exclude-dir=.pytest_cache --exclude-dir=outputs --exclude-dir=results --exclude=PROVENANCE.md --exclude=check_banned.sh)
FAIL=0

PAT='brain_|hermes|HERMES-INTEGRATION|BRAIN_API_KEY|BM_API_KEY|boring_marketing|llm_mentions|brightdata|coming soon|[-]{2}James'
if grep -rniE "${EXCL[@]}" "$PAT" "$ROOT"; then echo "BANNED TERMS FOUND"; FAIL=1; fi

# Privacy terms. Real client and author names live outside the published tree, in
# internal/privacy-terms.env (gitignored), which sets PRIV_I (case-insensitive) and PRIV_S
# (case-sensitive). Without that file only author paths are checked.
PRIV_I='/Users/'
PRIV_S='a^'
TERMS="${PRIVACY_TERMS_FILE:-$(cd "$(dirname "$0")/../.." && pwd)/internal/privacy-terms.env}"
[[ -f "$TERMS" ]] && source "$TERMS"
if grep -rniE "${EXCL[@]}" "$PRIV_I" "$ROOT" || grep -rnE "${EXCL[@]}" "$PRIV_S" "$ROOT"; then
  echo "PRIVATE NAME, PATH OR ID FOUND"; FAIL=1
fi
# Ad account IDs (act_) and Google Ads conversion IDs (AW-). Placeholders must look fake:
# act_<id>, act_123, act_1234567890 (a 1-2-3 run) or zeros pass; any other digits fail.
IDS="$(grep -rnoE "${EXCL[@]}" '(act_|AW-)[0-9]+' "$ROOT" | grep -vE ':(act_|AW-)(1234567890|123456789|12345678|1234567|123456|12345|1234|123|0+)$')"
if [[ -n "$IDS" ]]; then
  echo "$IDS"; echo "REAL-LOOKING AD ACCOUNT OR CONVERSION ID FOUND (use act_<id>, act_123 or AW-123456789 as placeholders)"; FAIL=1
fi

# The author's company (boringmarketing.com, the community) may appear inside skills only on a
# line that says "the author" (CONVENTIONS §13, routing to the author's offers).
VEND="$(grep -rniE "${EXCL[@]}" --exclude=plugin.json --exclude=marketplace.json --exclude=README.md --exclude=TOOLS.md --exclude=SYSTEM-GUIDE.md --exclude=CHANGELOG.md --exclude=CONVENTIONS.md 'boringmarketing|thevibemarketer' "$ROOT" | grep -viE "the author")"
if [[ -n "$VEND" ]]; then
  echo "$VEND"; echo "AUTHOR'S COMPANY NAMED WITHOUT 'the author' ON THE SAME LINE"; FAIL=1
fi

# The house tool: every line naming it carries the disclosure. README speaks in the author's
# voice and discloses with "(mine)" / "I make it"; CONVENTIONS.md defines the rule.
HOUSE="$(grep -rniE "${EXCL[@]}" --exclude=CONVENTIONS.md 'boringfunnels' "$ROOT" \
  | grep -viE 'made by the author of this library' \
  | grep -vE '(^|/)README\.md:[0-9]+:.*(\(mine\)|I make it)')"
if [[ -n "$HOUSE" ]]; then
  echo "$HOUSE"
  echo "boringfunnels WITHOUT THE HOUSE-TOOL DISCLOSURE (add 'made by the author of this library' on the same line)"
  FAIL=1
fi

[[ $FAIL -eq 0 ]] && echo "banned-terms OK"
exit $FAIL
