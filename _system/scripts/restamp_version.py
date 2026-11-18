#!/usr/bin/env python3
"""restamp_version.py — set the product version everywhere it is stamped.

Usage: restamp_version.py 3.1.0
Touches: .claude-plugin/plugin.json (version), .claude-plugin/marketplace.json (plugins[0].version),
         _system/scripts/install.sh (VERSION=), skills/*/SKILL.md (metadata.boring.version).
Python 3 stdlib only.
"""
import json, re, sys
from pathlib import Path

def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__); return 0
    v = argv[1]
    root = Path(__file__).resolve().parents[2]
    for name in ("plugin.json", "marketplace.json"):
        pj = root / ".claude-plugin" / name
        d = json.loads(pj.read_text())
        if name == "plugin.json":
            d["version"] = v
        else:
            for pl in d.get("plugins", []):
                pl["version"] = v
        pj.write_text(json.dumps(d, indent=2) + "\n")
    (root / "_system" / "VERSION").write_text(v + "\n")
    inst = root / "_system" / "scripts" / "install.sh"
    inst.write_text(re.sub(r'^VERSION="[^"]*"', f'VERSION="{v}"', inst.read_text(), flags=re.M))
    n = 0
    for sk in sorted((root / "skills").glob("*/SKILL.md")):
        t = sk.read_text()
        t2 = re.sub(r"^(\s+version:\s*)\S+", rf"\g<1>{v}", t, count=1, flags=re.M)
        if t2 != t:
            sk.write_text(t2); n += 1
    print(f"stamped {v}: plugin.json, marketplace.json, _system/VERSION, install.sh, {n} skills")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
