"""Portability: every skill must load brand context in all three install layouts.

`npx skills add` (vercel-labs/skills 1.8.1, tested 2026-11-13) copies skill folders
only: canonical copies in `.agents/skills/<name>/` (Codex, Cursor) and symlinks
`.claude/skills/<name> -> ../../.agents/skills/<name>` (Claude Code). `_system/` is not
copied. The Claude Code plugin keeps the repo layout (`skills/<name>/`). The shared
runtime therefore ships in `skills/start-here/scripts/` and skills call it as a sibling.

Set BMS_NPX_TEST=1 to also run the real CLI (needs node and network).
"""
import filecmp
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
RUNTIME = ("brand_context.py", "capability.py", "route.py")
CONTEXT = re.compile(r"python3 \$\{CLAUDE_SKILL_DIR\}(/[^\s`]*brand_context\.py) --for ([a-z0-9-]+)")
FIX = (
    "sed -i '' 's#${CLAUDE_SKILL_DIR}/../../_system/scripts/#${CLAUDE_SKILL_DIR}/../start-here/scripts/#g' "
    "skills/*/SKILL.md  (GNU sed: -i without '')"
)


def npx_layout(project):
    """Recreate what `npx skills add <repo> -a claude-code -a codex -a cursor` lays down."""
    agents = project / ".agents" / "skills"
    claude = project / ".claude" / "skills"
    agents.mkdir(parents=True)
    claude.mkdir(parents=True)
    for skill_md in SKILLS.glob("*/SKILL.md"):
        name = skill_md.parent.name
        shutil.copytree(skill_md.parent, agents / name, ignore=shutil.ignore_patterns("__pycache__"))
        (claude / name).symlink_to(Path("..") / ".." / ".agents" / "skills" / name)
    (project / "brand").mkdir()
    (project / "brand" / "brand.yaml").write_text("brand:\n  name: Hartline Plumbing (sample)\n  category: plumber\n")
    return {"claude-code": claude, "codex/cursor": agents, "plugin": SKILLS}


class Portability(unittest.TestCase):
    def test_runtime_copies_match_system_scripts(self):
        for name in RUNTIME:
            with self.subTest(script=name):
                self.assertTrue(
                    filecmp.cmp(ROOT / "_system" / "scripts" / name, SKILLS / "start-here" / "scripts" / name, shallow=False),
                    f"copy _system/scripts/{name} to skills/start-here/scripts/",
                )

    def test_context_line_loads_in_every_layout(self):
        project = Path(tempfile.mkdtemp())
        layouts = npx_layout(project)
        failures = []
        for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
            skill = skill_md.parent.name
            for rel, target in CONTEXT.findall(skill_md.read_text(encoding="utf-8")):
                for label, base in layouts.items():
                    script = os.path.normpath(str(base / skill) + rel)
                    result = subprocess.run(
                        [sys.executable, script, "--for", target],
                        capture_output=True, text=True, cwd=project,
                    )
                    if result.returncode or f"skill: {target}" not in result.stdout:
                        failures.append(f"{skill} [{label}]: {rel}")
        self.assertEqual(failures, [], "context line breaks outside the repo layout; fix with:\n" + FIX)

    def test_business_block_reaches_every_skill(self):
        project = Path(tempfile.mkdtemp())
        layouts = npx_layout(project)
        script = layouts["codex/cursor"] / "start-here" / "scripts" / "brand_context.py"
        out = subprocess.run([sys.executable, str(script), "--for", "seo-content"],
                             capture_output=True, text=True, cwd=project).stdout
        self.assertIn("## Business (brand.yaml)", out)
        self.assertIn("category: plumber", out)

    def test_route_finds_sibling_skills_in_npx_layout(self):
        project = Path(tempfile.mkdtemp())
        layouts = npx_layout(project)
        script = layouts["claude-code"] / "start-here" / "scripts" / "route.py"
        result = subprocess.run([sys.executable, str(script), "--task", "reviews"],
                                capture_output=True, text=True, cwd=project)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"task": "reviews"', result.stdout)
        self.assertNotIn('"error"', result.stdout)

    @unittest.skipUnless(os.environ.get("BMS_NPX_TEST") == "1", "set BMS_NPX_TEST=1 to run the real npx skills CLI")
    def test_real_cli_layout(self):
        tmp = Path(tempfile.mkdtemp())
        home, project = tmp / "home", tmp / "project"
        home.mkdir(); project.mkdir()
        env = dict(os.environ, HOME=str(home), DISABLE_TELEMETRY="1", DO_NOT_TRACK="1",
                   npm_config_cache=str(tmp / "npm"))
        subprocess.run(["npx", "-y", "skills@1.8.1", "add", str(ROOT), "--skill", "*",
                        "-a", "claude-code", "-a", "codex", "-a", "cursor", "-y"],
                       cwd=project, env=env, check=True, capture_output=True, timeout=600)
        self.assertTrue((project / ".agents" / "skills" / "start-here" / "scripts" / "brand_context.py").is_file())
        self.assertTrue((project / ".claude" / "skills" / "start-here").is_symlink())
        self.assertFalse((project / ".agents" / "_system").exists())
        self.assertFalse(any(home.rglob("SKILL.md")), "project scope must not write to HOME")
        (project / "brand").mkdir()
        out = subprocess.run([sys.executable, str(project / ".claude/skills/seo-content/../start-here/scripts/brand_context.py"),
                              "--for", "seo-content"], capture_output=True, text=True, cwd=project)
        self.assertIn("skill: seo-content", out.stdout)


if __name__ == "__main__":
    unittest.main()
