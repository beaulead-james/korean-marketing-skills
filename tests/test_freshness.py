"""Every dated reference file is tracked by the CI freshness gate (tests/ttl_files.txt)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Freshness(unittest.TestCase):
    def test_dated_files_are_tracked(self):
        tracked = set((ROOT / "tests" / "ttl_files.txt").read_text().split())
        dated = set()
        for path in (ROOT / "skills").rglob("*.md"):
            head = "".join(path.read_text(encoding="utf-8").splitlines(True)[:40])
            if re.search(r"last-verified:\s*\d{4}-\d{2}-\d{2}", head) and re.search(r"ttl-days:\s*\d+", head):
                dated.add(str(path.relative_to(ROOT)))
        self.assertEqual(sorted(dated - tracked), [], "add these to tests/ttl_files.txt")
        missing = sorted(p for p in tracked if not (ROOT / p).is_file())
        self.assertEqual(missing, [], "tracked files that no longer exist")


if __name__ == "__main__":
    unittest.main()
