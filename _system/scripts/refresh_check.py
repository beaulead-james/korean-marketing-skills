#!/usr/bin/env python3
"""
refresh_check.py — freshness gate for dated reference files (CONVENTIONS §7).

Reference files carry a header line (anywhere in the first 40 lines) like:

  last-verified: 2026-06-10 · ttl-days: 90 · refresh: web search "X algorithm <month year>"

or the same keys on separate lines. This script compares last-verified + ttl-days
against today.

Usage:
  refresh_check.py <file> [<file> ...]

Exit codes:
  0  all files fresh
  1  at least one file stale (a refresh warning is printed for each)
  2  header missing/unparseable in at least one file, or file not found

Python 3 stdlib only.
"""

import datetime
import re
import sys

HEADER_LINES = 40


def check(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as f:
            head = "".join(f.readline() for _ in range(HEADER_LINES))
    except OSError as e:
        print(f"{path}: cannot read ({e})", file=sys.stderr)
        return 2

    m_date = re.search(r"last-verified:\s*(\d{4}-\d{2}-\d{2})", head)
    m_ttl = re.search(r"ttl-days:\s*(\d+)", head)
    m_refresh = re.search(r"refresh:\s*(.+)", head)

    if not m_date or not m_ttl:
        print(f"{path}: no 'last-verified:' + 'ttl-days:' header found — treat as "
              f"unverified and add the header per CONVENTIONS §7", file=sys.stderr)
        return 2

    verified = datetime.date.fromisoformat(m_date.group(1))
    ttl = int(m_ttl.group(1))
    age = (datetime.date.today() - verified).days

    if age <= ttl:
        return 0

    print(f"{path}: STALE — last verified {verified.isoformat()} ({age} days ago, "
          f"ttl {ttl}d). Refresh before relying on it.")
    if m_refresh:
        print(f"  refresh instruction: {m_refresh.group(1).strip()}")
    print("  After refreshing, update the 'last-verified:' date in the file.")
    return 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    worst = 0
    for path in argv:
        worst = max(worst, check(path))
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
