# /// script
# requires-python = ">=3.10"
# dependencies = ["regex>=2023.0", "sudachipy>=0.6.8", "sudachidict-core>=20240409"]
# ///
"""eval.py - measure the lint layers on a fixed corpus of real documents.

    prose-lint-run uv run eval.py --manifest <manifest.json> [--labels <labels.jsonl>] [--findings <findings.jsonl>]

Run it through prose-lint-run, so the downloaded Node and vale are on PATH: a missing tool stops the
run, because a layer that cannot run would otherwise read as zero hits.

The manifest holds {"docs": [{"path": ..., "group": ...}]}. A group that starts with en- is
English; any other group is Japanese. For each rule the output gives hits per 1,000 characters
(Japanese) or per 1,000 words (English) in each group, so a rule can be compared across writers.

labels.jsonl holds known defects, one object per line, with the keys doc, line, quote and class.
The output gives, per class, how many labels a mechanical hit lands on. findings.jsonl holds what
a reading agent reported, with the keys doc and either sentence or line: a finding detects a label
when its sentence contains the label's quote, or, with no sentence, when its line is the label's.

The output is JSON on stdout with sorted keys and no timestamps, so two runs on one corpus compare
byte for byte. Keep the corpus, the manifest and the labels outside the repository: they can hold
client text.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent.parent.parent / "hooks")]
# lint comes first: koyobun puts natural-japanese's own lint.py on sys.path.
import lint  # isort: skip
import koyobun  # isort: skip
import register  # isort: skip

NJ_LINT = HERE.parent / "vendor" / "natural-japanese" / "scripts" / "lint.py"
FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)
JOBS = max(2, (os.cpu_count() or 4) - 2)
TOKENIZER = threading.Lock()  # koyobun shares one sudachipy tokenizer


def size(text: str, lang: str) -> int:
    """Return the non-space characters (ja) or the words (en) outside fenced code."""
    body = FENCE.sub("", text)
    return len(body.split()) if lang == "en" else len("".join(body.split()))


def natural_japanese(path: Path) -> list[dict]:
    args = ["uv", "run", "--quiet", str(NJ_LINT), "--genre", "business", "--reading-load", "--json", str(path)]
    try:
        out = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=180, check=False).stdout
        return json.loads(out).get("findings", []) if out.strip() else []
    except (OSError, ValueError, subprocess.SubprocessError):
        return []


def layers(path: Path, text: str, lang: str, tables: dict[str, list[dict]]) -> list[tuple[str, int]]:
    """Return (rule key, line) for every hit on one document."""
    hits = [(f'textlint/{m.get("ruleId")}', m.get("line", 0)) for m in lint.textlint(path, lang)]
    kinds = ("general",) if lang == "en" else tuple(tables)
    for kind in kinds:
        hits += [(f'register/{kind}/{h["matched"].lower()}', h["line"]) for h in register.find_hits(text, tables[kind])]
    if lang == "en":
        return hits + [(f'vale/{v["ruleId"]}', v["line"]) for v in lint.vale(path)]
    hits += [(f'natural-japanese/{f.get("category")}', f.get("line", 0) or 0) for f in natural_japanese(path)]
    with TOKENIZER:
        found = koyobun.run(text)[0]
    return hits + [(f'koyobun/{f["check"]}', f["line"]) for f in found]


def key(path: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.expanduser(path)))


def read_jsonl(path: Path | None) -> list[dict]:
    if path is None:
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def detected(label: dict, findings: list[dict]) -> bool:
    for f in findings:
        if key(f["doc"]) != key(label["doc"]):
            continue
        if label.get("quote") and label["quote"] in (f.get("sentence") or ""):
            return True
        if not f.get("sentence") and f.get("line") == label.get("line"):
            return True
    return False


def recall(labels: list[dict], lines: dict[str, set[int]], findings: list[dict]) -> dict:
    out: dict = defaultdict(lambda: {"labels": 0, "layer_hit": 0, "detected": 0})
    for label in labels:
        row = out[label["class"]]
        row["labels"] += 1
        row["layer_hit"] += label.get("line") in lines.get(key(label["doc"]), ())
        row["detected"] += detected(label, findings)
    return dict(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--labels", type=Path)
    ap.add_argument("--findings", type=Path)
    args = ap.parse_args()
    missing = [tool for tool in ("node", "vale", "uv") if not shutil.which(tool)]
    if missing:
        print(f"error: not on PATH: {', '.join(missing)}", file=sys.stderr)
        return 1
    docs = json.loads(args.manifest.read_text(encoding="utf-8"))["docs"]
    tables = {kind: register.load_entries(register.read_register(register.default_register(kind)))
              for kind in register.REGISTERS}

    def measure(doc: dict) -> tuple[dict, int, list[tuple[str, int]]]:
        path, lang = Path(doc["path"]), "en" if doc["group"].startswith("en-") else "ja"
        text = path.read_text(encoding="utf-8", errors="replace")
        return doc, size(text, lang), layers(path, text, lang, tables)

    sizes, documents = Counter(), Counter()
    rules: dict = defaultdict(Counter)
    lines: dict[str, set[int]] = defaultdict(set)
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        for doc, n, hits in pool.map(measure, docs):
            sizes[doc["group"]] += n
            documents[doc["group"]] += 1
            for rule, line in hits:
                rules[rule][doc["group"]] += 1
                lines[key(doc["path"])].add(line)

    per_k = lambda hits, group: round(hits * 1000 / max(sizes[group], 1), 3)
    print(json.dumps({
        "groups": {g: {"docs": documents[g], "size": sizes[g]} for g in sizes},
        "rules": {r: {g: {"hits": c[g], "per_1000": per_k(c[g], g)} for g in c} for r, c in rules.items()},
        "recall": recall(read_jsonl(args.labels), lines, read_jsonl(args.findings)),
    }, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
