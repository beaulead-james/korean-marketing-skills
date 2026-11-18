#!/usr/bin/env python3
"""Autocomplete mining via a public suggest endpoint. Stdlib only.

Default engine is Google. `--engine naver` uses Naver autocomplete, the free
path for Korean keywords. No API key.

Usage:
    python3 suggest.py "ai marketing" [options]
    python3 suggest.py --engine naver "보일러 수리" --mode base

Options:
    --engine ENGINE google (default) | naver
    --mode MODE     Probe set: all (default) | base | alphabet | questions |
                    prepositions | comparisons. Comma-combine: questions,prepositions
    --lang LANG     Google hl hint. Default: en. Ignored for naver. Use ko for Korean Google.
    --format FMT    Output: json (default) | lines (suggestions only, one per line)
    --delay SECS    Seconds between requests. Default: 0.12
    --max-probes N  Safety cap on number of probes. Default: 60

Output (json):
    {"keyword": ..., "probes_run": N, "unique_suggestions": N,
     "suggestions": [{"suggestion": ..., "probe": ..., "probe_type": ...}, ...]}

Exit codes: 0 ok, 1 bad args, 2 network failure on every probe.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://suggestqueries.google.com/complete/search"
NAVER_ENDPOINT = "https://ac.search.naver.com/nx/ac"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
KO_SUFFIXES = ["비용", "가격", "추천", "후기", "업체", "예약", "근처", "비교"]
KO_PREFIXES = ["어떻게", "왜", "언제", "어디서"]
CHOSEONG = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"

QUESTION_PREFIXES = [
    "what", "how", "why", "when", "where", "who", "which",
    "can", "is", "does", "should", "will",
]
PREPOSITION_SUFFIXES = ["for", "with", "without", "vs", "to", "near", "like"]
COMPARISON_PROBES = [
    ("best {kw}", "comparison"),
    ("{kw} alternatives", "comparison"),
    ("{kw} review", "comparison"),
    ("{kw} pricing", "comparison"),
]
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def build_probes(keyword, modes):
    """Return list of (probe_query, probe_type) preserving order, deduped."""
    probes = []
    if "base" in modes or "all" in modes:
        probes.append((keyword, "base"))
    if "alphabet" in modes or "all" in modes:
        probes.extend((f"{keyword} {ch}", "alphabet") for ch in ALPHABET)
    if "questions" in modes or "all" in modes:
        probes.extend((f"{p} {keyword}", "question") for p in QUESTION_PREFIXES)
    if "prepositions" in modes or "all" in modes:
        probes.extend((f"{keyword} {s}", "preposition") for s in PREPOSITION_SUFFIXES)
    if "comparisons" in modes or "all" in modes:
        probes.extend((t.format(kw=keyword), pt) for t, pt in COMPARISON_PROBES)
    seen, out = set(), []
    for q, t in probes:
        if q not in seen:
            seen.add(q)
            out.append((q, t))
    return out


def build_naver_probes(keyword, modes):
    """Korean probe set. Alphabet mode walks choseong instead of a-z."""
    probes = []
    if "base" in modes or "all" in modes:
        probes.append((keyword, "base"))
    if "alphabet" in modes or "all" in modes:
        probes.extend((f"{keyword} {ch}", "alphabet") for ch in CHOSEONG)
    if "questions" in modes or "all" in modes:
        probes.extend((f"{p} {keyword}", "question") for p in KO_PREFIXES)
    if "prepositions" in modes or "all" in modes:
        probes.extend((f"{keyword} {s}", "preposition") for s in KO_SUFFIXES)
    if "comparisons" in modes or "all" in modes:
        probes.extend(
            (q, "comparison")
            for q in (f"{keyword} 추천", f"{keyword} 후기", f"{keyword} 비교", f"{keyword} 가격")
        )
    seen, out = set(), []
    for q, t in probes:
        if q not in seen:
            seen.add(q)
            out.append((q, t))
    return out


def fetch_suggestions(query, lang):
    """One suggest request. Returns list of suggestion strings."""
    params = urllib.parse.urlencode({"client": "firefox", "hl": lang, "q": query})
    req = urllib.request.Request(
        f"{ENDPOINT}?{params}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
    # Response is JSON: [query, [suggestion, ...], ...]. Encoding varies; try
    # utf-8 first, fall back to latin-1 (endpoint sometimes serves ISO-8859-1).
    try:
        data = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        data = json.loads(raw.decode("latin-1"))
    if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
        return [s for s in data[1] if isinstance(s, str)]
    return []


def fetch_naver(query):
    """One Naver autocomplete request. Returns suggestion strings."""
    params = urllib.parse.urlencode(
        {
            "q": query,
            "con": "1",
            "frm": "nv",
            "ans": "2",
            "r_format": "json",
            "r_enc": "UTF-8",
            "r_unicode": "0",
            "t_koreng": "1",
            "run": "2",
            "rev": "4",
            "q_enc": "UTF-8",
            "st": "100",
        }
    )
    req = urllib.request.Request(
        f"{NAVER_ENDPOINT}?{params}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    items = data.get("items") if isinstance(data, dict) else None
    if not items or not isinstance(items[0], list):
        return []
    out = []
    for row in items[0]:
        if isinstance(row, list) and row and isinstance(row[0], str):
            out.append(row[0])
    return out


def main():
    ap = argparse.ArgumentParser(description="Autocomplete miner (Google or Naver)")
    ap.add_argument("keyword")
    ap.add_argument("--engine", default="google", choices=["google", "naver"])
    ap.add_argument("--mode", default="all")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--format", default="json", choices=["json", "lines"])
    ap.add_argument("--delay", type=float, default=0.12)
    ap.add_argument("--max-probes", type=int, default=60)
    args = ap.parse_args()

    keyword = args.keyword.strip().lower()
    if not keyword:
        print("error: empty keyword", file=sys.stderr)
        return 1

    modes = {m.strip() for m in args.mode.split(",") if m.strip()}
    valid = {"all", "base", "alphabet", "questions", "prepositions", "comparisons"}
    if not modes or modes - valid:
        print(f"error: invalid --mode (valid: {sorted(valid)})", file=sys.stderr)
        return 1

    if args.engine == "naver":
        probes = build_naver_probes(keyword, modes)[: args.max_probes]
        fetch = lambda probe: fetch_naver(probe)
    else:
        probes = build_probes(keyword, modes)[: args.max_probes]
        fetch = lambda probe: fetch_suggestions(probe, args.lang)
    results = {}  # suggestion -> (probe, probe_type); first probe wins
    errors = 0
    for i, (probe, ptype) in enumerate(probes):
        try:
            for s in fetch(probe):
                s_norm = s.strip().lower()
                if s_norm and s_norm != keyword and s_norm not in results:
                    results[s_norm] = (probe, ptype)
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
            errors += 1
            print(f"warn: probe '{probe}' failed: {e}", file=sys.stderr)
        if i < len(probes) - 1:
            time.sleep(args.delay)

    if errors == len(probes):
        print("error: all probes failed (network/endpoint unavailable)", file=sys.stderr)
        return 2

    if args.format == "lines":
        for s in sorted(results):
            print(s)
    else:
        payload = {
            "keyword": keyword,
            "engine": args.engine,
            "probes_run": len(probes),
            "probes_failed": errors,
            "unique_suggestions": len(results),
            "suggestions": [
                {"suggestion": s, "probe": p, "probe_type": t}
                for s, (p, t) in sorted(results.items())
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
