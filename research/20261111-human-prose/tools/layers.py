"""layers.py - run every mechanical layer of the skill over a set of Markdown files.

    python3 layers.py <skill dir> <out.json> <file.md>...

Per file: flow.py --json, koyobun.py --json, register.py --json for the general,
translationese and slop registers, textlint -f json, natural-japanese lint.py --json.
Writes one JSON object keyed by file stem.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

skill = Path(sys.argv[1])
out = Path(sys.argv[2])
files = [Path(f) for f in sys.argv[3:]]
home = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint")
S = skill / "scripts"
NJ = skill / "vendor" / "natural-japanese" / "scripts"


def run(args):
    r = subprocess.run(args, capture_output=True, encoding="utf-8", check=False)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"error": (r.stderr or r.stdout)[-400:]}


res = json.loads(out.read_text()) if out.exists() else {}
for f in files:
    if f.stem in res:
        continue
    d = {}
    d["flow"] = run(["uv", "run", "-q", "--no-project", str(S / "flow.py"), "--json", str(f)])
    d["koyobun"] = run(["uv", "run", "-q", "--no-project", str(S / "koyobun.py"), "--json", str(f)])
    for kind in ("general", "translationese", "slop"):
        args = ["uv", "run", "-q", "--no-project", str(S / "register.py"), "--json"]
        if kind == "general":
            args += ["--register", str(skill / "assets" / "vocabulary.sample.md")]
        else:
            args += ["--" + kind]
        d["reg_" + kind] = run(args + [str(f)])
    d["textlint"] = run(["node", str(home / "textlint/node_modules/textlint/bin/textlint.js"), "--config",
                         str(home / "textlint/.textlintrc.json"), "-f", "json", str(f)])
    nj = run(["uv", "run", "-q", "--no-project", str(NJ / "lint.py"), "--genre", "business", "--reading-load", "--json", str(f)])
    if isinstance(nj, dict):
        nj.pop("paragraphs", None)
    d["nj"] = nj
    res[f.stem] = d
    out.write_text(json.dumps(res, ensure_ascii=False))
    print(f.stem, "ok", file=sys.stderr)
