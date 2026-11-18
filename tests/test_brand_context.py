import subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parents[1] / "_system" / "scripts"
SKILL = Path(__file__).resolve().parents[1] / "skills" / "direct-response-copy" / "SKILL.md"

def run(root):
    r = subprocess.run([sys.executable, str(SCRIPTS / "brand_context.py"), "--skill-file", str(SKILL), "--root", str(root)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout

class BrandContext(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp()); (self.root / "brand").mkdir()
        (self.root / "brand" / "positioning.md").write_text("# Positioning\nAngle: X\n")

    def test_marketing_md_first_then_preferences(self):
        (self.root / "MARKETING.md").write_text("Goal: leads. Never discount.\n")
        (self.root / "brand" / "preferences.md").write_text("Banned: 'unlock'\n")
        out = run(self.root)
        i_m, i_p, i_pos = out.index("MARKETING.md"), out.index("preferences.md"), out.index("positioning.md")
        self.assertTrue(i_m < i_p < i_pos)

    def test_marketing_md_truncates_at_300(self):
        (self.root / "MARKETING.md").write_text("\n".join(f"line {i}" for i in range(400)))
        out = run(self.root)
        self.assertIn("truncated at 300 lines", out); self.assertNotIn("line 350", out)

    def test_absent_files_unchanged(self):
        out = run(self.root)
        self.assertNotIn("MARKETING.md", out); self.assertNotIn("preferences.md", out)

    def test_brand_env_flag_without_values(self):
        (self.root / "brand" / ".env").write_text("KIT_API_KEY=secret123\n")
        out = run(self.root)
        self.assertIn("brand .env present: yes", out); self.assertNotIn("secret123", out)

    def test_checks_filtered_to_skill_and_all(self):
        (self.root / "brand" / "checks.md").write_text(
            "# Checks\n\n- [all] Does every number match the brief?\n"
            "- [direct-response-copy] Does the headline use the customer's words?\n"
            "- [email-sequences] Is every subject under 40 characters?\n")
        out = run(self.root)
        self.assertIn("2 yes/no checks", out)
        self.assertIn("customer's words", out); self.assertIn("match the brief", out)
        self.assertNotIn("40 characters", out)

    def test_gold_cases_newest_three_for_this_skill(self):
        g = self.root / "brand" / "gold"
        for d in ("2026-11-01-a", "2026-11-05-b", "2026-11-09-c", "2026-11-12-d"):
            (g / "direct-response-copy").mkdir(parents=True, exist_ok=True)
            (g / "direct-response-copy" / f"{d}.md").write_text("# case\n")
        (g / "paid-ads").mkdir(parents=True)
        (g / "paid-ads" / "2026-11-13-z.md").write_text("# other\n")
        out = run(self.root)
        self.assertIn("2026-11-12-d.md", out); self.assertIn("2026-11-05-b.md", out)
        self.assertNotIn("2026-11-01-a.md", out); self.assertNotIn("2026-11-13-z.md", out)
        self.assertLess(out.index("2026-11-12-d.md"), out.index("2026-11-09-c.md"))

if __name__ == "__main__":
    unittest.main()
