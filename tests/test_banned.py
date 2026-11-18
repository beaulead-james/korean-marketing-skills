"""check_banned.sh: privacy terms fail, the house tool needs its disclosure on the line."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "_system" / "scripts" / "check_banned.sh"
HOUSE = "boring" + "funnels"
DISCLOSURE = "made by the author of this library"


# Real private names live in internal/privacy-terms.env, which is never published.
# The tests use a stand-in terms file with made-up names.
TERMS = Path(tempfile.mkdtemp()) / "privacy-terms.env"
TERMS.write_text("PRIV_I='zorblax holdings|/Us" + "ers/'\nPRIV_S='Quillon|\\bMarvo\\b'\n", encoding="utf-8")


def scan(text, name="skills/x/SKILL.md"):
    root = Path(tempfile.mkdtemp())
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    env = {**os.environ, "PRIVACY_TERMS_FILE": str(TERMS)}
    return subprocess.run(["bash", str(SCRIPT), str(root)], capture_output=True, text=True, env=env)


class Banned(unittest.TestCase):
    def test_clean_tree_passes(self):
        result = scan("A plumber in Dallas. Lowercase quillon is not the name.\n")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_privacy_terms_fail(self):
        for term in ("Zorblax Holdings", "zorblax holdings", "Quillon said", "Marvo wrote", "/Us" + "ers/someone",
                     "act" + "_2847561093", "AW" + "-9812345670"):
            with self.subTest(term=term):
                self.assertEqual(scan(f"line with {term}\n").returncode, 1)

    def test_fake_looking_placeholders_pass(self):
        self.assertEqual(scan("META_AD_ACCOUNT_ID=act" + "_123 or act" + "_1234567890, AW" + "-123456789\n").returncode, 0)

    def test_house_tool_needs_disclosure_on_the_line(self):
        self.assertEqual(scan(f"Try {HOUSE} for this step.\n").returncode, 1)
        line = f"Optional: {HOUSE} ({DISCLOSURE}, paid Pro with a free search) does this step.\n"
        self.assertEqual(scan(line).returncode, 0)

    def test_readme_may_disclose_in_first_person(self):
        self.assertEqual(scan(f"| {HOUSE} (mine) | Free search |\n", name="README.md").returncode, 0)
        self.assertEqual(scan(f"{HOUSE} finds clients.\n", name="README.md").returncode, 1)


    def test_author_company_needs_disclosure_on_the_line(self):
        site = "boring" + "marketing.com"
        self.assertEqual(scan(f"Want this weekly? See {site}.\n").returncode, 1)
        self.assertEqual(scan(f"> Want this running every week? The author's team builds it: {site}.\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
