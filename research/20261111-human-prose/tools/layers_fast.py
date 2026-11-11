import json, os, subprocess, sys
from pathlib import Path
skill = Path(sys.argv[1]); out = Path(sys.argv[2]); files = [Path(f) for f in sys.argv[3:]]
home = Path.home() / ".prose-lint"; S = skill / "scripts"
def run(args):
    r = subprocess.run(args, capture_output=True, encoding="utf-8", check=False)
    try: return json.loads(r.stdout)
    except ValueError: return {"error": (r.stderr or r.stdout)[-300:]}
res = {}
for f in files:
    d = {"koyobun": run(["uv", "run", "-q", "--no-project", str(S / "koyobun.py"), "--json", str(f)])}
    for kind in ("general", "translationese"):
        args = ["uv", "run", "-q", "--no-project", str(S / "register.py"), "--json"]
        args += ["--register", str(skill / "assets" / "vocabulary.sample.md")] if kind == "general" else ["--" + kind]
        d["reg_" + kind] = run(args + [str(f)])
    d["textlint"] = run(["node", str(home / "textlint/node_modules/textlint/bin/textlint.js"), "--config", str(home / "textlint/.textlintrc.json"), "-f", "json", str(f)])
    res[f.stem] = d
    out.write_text(json.dumps(res, ensure_ascii=False))
