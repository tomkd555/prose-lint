# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "sudachipy>=0.6.8",
#     "sudachidict-core>=20240409",
# ]
# ///
"""norm.py - how far a Japanese text sits from a baseline of human-written text.

The other scripts report a wording to take out, so a text can clear them all by
leaving ordinary Japanese out: the が and ので that join clauses, the connective
that opens a sentence, the demonstrative, the passive, the サ変 verb. This one
counts those forms with sudachipy and lays each rate beside the same rate in a
baseline of human-written documents. Six rates are marked, each on the side a
text moves to when those forms are left out: `low` under the value 95 % of the
baseline's documents reach, `high` over the value 95 % of them stay under. Two
or more marks make the text `off`. It rules on nothing.

    uv run norm.py [--baseline <baseline.json>] [--json] <file>
    uv run norm.py --build <baseline.json> --name <label> [--plain] <file or folder> ...

--build writes a baseline from a set of human-written documents, one document a
file: news articles, editorials, reports. A folder is read with every .md and
.txt file under it; --plain reads the files as plain text with no Markdown. The
baseline holds the rates and no text. The default baseline is
$PROSE_LINT_NORM_BASELINE, else norm-baseline.json in $PROSE_LINT_HOME or
~/.prose-lint, else assets/norm-baseline.json beside this script, which was
built from Japanese Wikinews (CC BY 4.0).

Rates, per sentence of running text (code, tables, headings and quotes are left
out; a list item is read as a sentence):

    joints         接続助詞 and 連用中止 in a sentence                           marked low
    glue           ga, opener and demonstrative together, per 100 sentences   marked low
    ga             が as a 接続助詞, per 100 sentences
    opener         sentences that open with a 接続詞, per 100
    demonstrative  こ・そ・あ words (この, それ, こうした), per 100 sentences
    passive        れる/られる after a verb, per 100 sentences
    sahen          verbs made of a noun and する (確認する), as a share of all verbs, %  marked low
    negative_end   sentences whose final predicate is negated, per 100        marked high
    colon          a colon followed by text, per 100 sentences                marked high
    length         mean sentence length in characters                         marked low

ga, opener, demonstrative and passive are printed for reading and carry no mark:
a news article of 10 sentences often holds none of one of them.

A document under 10 sentences gets its rates and no marks. Exit code 0; 1 on an
input error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from pathlib import Path

MIN_SENTENCES = 10
OFF_MARKS = 2
FENCE = re.compile(r"^\s*(```|~~~)")
LIST = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
SPLIT = re.compile(r"(?<=[。！？])")
KANA = re.compile(r"[ぁ-ゟ]")
COLON = re.compile(r"[：:]\s*\S")
DEMONSTRATIVE = {"この", "その", "あの", "こうした", "そうした", "これら", "それら", "こう", "そう"}
NEGATORS = {"ない", "ぬ", "ん"}
FEATURES = ("joints", "glue", "ga", "opener", "demonstrative", "passive", "sahen", "negative_end", "colon", "length")
# The side each marked rate moves to when ordinary forms are left out.
DIRECTION = {"joints": "low", "glue": "low", "sahen": "low", "negative_end": "high", "colon": "high", "length": "low"}
HINTS = {
    ("joints", "low"): "節をつなぐ接続助詞や連用中止が少ない。原因、条件、対比が本文にある文は、ので・が・と・て でつなぐ",
    ("glue", "low"): "接続助詞「が」、文頭の接続詞、指示語が少ない。前の文との関係が本文にあるなら、また・しかし・そのため や この・その で示す",
    ("sahen", "low"): "「名詞＋する」の動詞が少ない。確認する、修正する、追加する のように、その分野で使う動詞で書く",
    ("negative_end", "high"): "否定で終わる文が多い。したことと、その結果を述べる文にする",
    ("colon", "high"): "コロンでつないだ行が多い。主語と述語のある文にする",
    ("length", "low"): "文が短い。関係のある文はつないで 1 文にする",
}


def home() -> Path:
    return Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint")


def default_baseline() -> Path:
    env = os.environ.get("PROSE_LINT_NORM_BASELINE")
    candidates = [Path(env)] if env else []
    candidates += [home() / "norm-baseline.json", Path(__file__).resolve().parent.parent / "assets" / "norm-baseline.json"]
    return next((c for c in candidates if c.is_file()), candidates[-1])


def sentences(text: str, plain: bool = False) -> list[str]:
    """Return the sentences of the running text; a list item counts as a sentence."""
    out: list[str] = []
    para: list[str] = []

    def flush() -> None:
        out.extend(s.strip() for s in SPLIT.split("".join(para)) if s.strip())
        para.clear()

    fence = False
    for line in text.splitlines():
        if not plain:
            if FENCE.match(line):
                fence = not fence
                continue
            if fence:
                continue
            line = re.sub(r"`[^`]*`", "X", line)
            line = re.sub(r"\*\*|__", "", line)
            line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        stripped = line.strip()
        if not stripped or (not plain and stripped.startswith(("#", "|", ">", "<", "---"))):
            flush()
        elif not plain and LIST.match(line):
            flush()
            para.append(LIST.sub("", line).strip())
            flush()
        elif plain:
            para.append(stripped)
            flush()
        else:
            para.append(stripped)
    flush()
    return [s for s in out if KANA.search(s) and len(s) >= 6]


def rates(sents: list[str], tok) -> dict:
    """Return the rates of one document."""
    from sudachipy import SplitMode

    n = len(sents)
    count = dict.fromkeys(("joints", "ga", "opener", "demonstrative", "passive", "negative_end", "colon"), 0)
    verbs = sahen = 0
    for sent in sents:
        ms = tok.tokenize(sent, SplitMode.C)
        count["colon"] += len(COLON.findall(sent))
        body = [m for m in ms if m.part_of_speech()[0] not in {"補助記号", "空白"}]
        if body and body[0].part_of_speech()[0] == "接続詞":
            count["opener"] += 1
        for i, m in enumerate(ms):
            pos = m.part_of_speech()
            if pos[0] == "助詞" and pos[1] == "接続助詞":
                count["joints"] += 1
                count["ga"] += m.surface() == "が"
            elif (pos[0] in {"動詞", "形容詞", "助動詞"} and pos[5].startswith("連用形")
                  and i + 1 < len(ms) and ms[i + 1].part_of_speech()[1] == "読点"):
                count["joints"] += 1
            if pos[0] == "代名詞" and m.surface()[:1] in "こそあ" or pos[0] in {"連体詞", "副詞"} and m.surface() in DEMONSTRATIVE:
                count["demonstrative"] += 1
            if pos[0] == "助動詞" and m.dictionary_form() in {"れる", "られる"} and i and ms[i - 1].part_of_speech()[0] == "動詞":
                count["passive"] += 1
            if pos[0] == "動詞" and pos[1] == "一般":
                verbs += 1
            elif pos[0] == "動詞" and m.dictionary_form() == "する" and i and ms[i - 1].part_of_speech()[0] == "名詞":
                verbs += 1
                sahen += 1
        # the final predicate: what follows the last noun or case particle
        tail = []
        for m in body:
            pos = m.part_of_speech()
            if pos[0] in {"名詞", "代名詞"} or (pos[0] == "助詞" and pos[1] in {"格助詞", "係助詞", "副助詞"}):
                tail = []
            else:
                tail.append(m)
        for i, m in enumerate(tail):
            pos = m.part_of_speech()
            negator = (pos[0] == "助動詞" and m.dictionary_form() in NEGATORS) or (pos[0] == "形容詞" and m.dictionary_form() == "ない")
            if negator and all(x.part_of_speech()[0] in {"助動詞", "助詞"} for x in tail[i + 1:]):
                count["negative_end"] += 1
                break
    result = {"joints": count["joints"] / n}
    result.update({k: count[k] * 100 / n for k in ("ga", "opener", "demonstrative", "passive", "negative_end", "colon")})
    result["glue"] = result["ga"] + result["opener"] + result["demonstrative"]
    result["sahen"] = sahen * 100 / verbs if verbs else 0.0
    result["length"] = statistics.mean(len(s) for s in sents)
    return {k: round(result[k], 2) for k in FEATURES}


def tokenizer():
    from sudachipy import Dictionary

    return Dictionary().create()


def build(paths: list[str], name: str, plain: bool) -> dict:
    files: list[Path] = []
    for p in paths:
        pp = Path(p)
        files += sorted(f for f in pp.rglob("*") if f.suffix.lower() in {".md", ".txt"}) if pp.is_dir() else [pp]
    tok = tokenizer()
    rows = []
    total = 0
    for f in files:
        try:
            sents = sentences(f.read_text(encoding="utf-8"), plain)
        except (OSError, UnicodeDecodeError):
            continue
        if len(sents) >= MIN_SENTENCES:
            rows.append(rates(sents, tok))
            total += len(sents)
    if len(rows) < 20:
        raise SystemExit(f"error: {len(rows)} document(s) of {MIN_SENTENCES} sentences or more; a baseline needs 20")
    bands = {}
    for k in FEATURES:
        values = sorted(r[k] for r in rows)
        q = statistics.quantiles(values, n=20, method="inclusive")
        bands[k] = {"p05": round(q[0], 2), "p50": round(statistics.median(values), 2), "p95": round(q[18], 2)}
    return {"name": name, "documents": len(rows), "sentences": total, "bands": bands}


def judge(values: dict, baseline: dict, n: int) -> list[dict]:
    out = []
    for k in FEATURES:
        band = baseline["bands"][k]
        mark = ""
        if n >= MIN_SENTENCES:
            mark = "low" if values[k] < band["p05"] else "high" if values[k] > band["p95"] else ""
            mark = mark if mark == DIRECTION.get(k) else ""
        out.append({"rate": k, "value": values[k], "median": band["p50"], "low": band["p05"], "high": band["p95"],
                    "mark": mark, "hint": HINTS.get((k, mark), "")})
    return out


def run(text: str, baseline: dict, plain: bool = False) -> dict:
    sents = sentences(text, plain)
    if not sents:
        return {"sentences": 0, "rates": [], "off": False, "baseline": baseline["name"]}
    rows = judge(rates(sents, tokenizer()), baseline, len(sents))
    marks = sum(1 for r in rows if r["mark"])
    return {"sentences": len(sents), "rates": rows, "marks": marks, "off": marks >= OFF_MARKS, "baseline": baseline["name"]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--baseline")
    ap.add_argument("--build", metavar="OUT")
    ap.add_argument("--name", default="baseline")
    ap.add_argument("--plain", action="store_true", help="read the files as plain text, with no Markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.build:
        baseline = build(args.paths, args.name, args.plain)
        Path(args.build).write_text(json.dumps(baseline, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f'{args.build}: {baseline["documents"]} documents, {baseline["sentences"]} sentences')
        return 0
    path = Path(args.baseline) if args.baseline else default_baseline()
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
        text = Path(args.paths[0]).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    result = run(text, baseline, args.plain)
    if args.json:
        print(json.dumps({"file": args.paths[0], **result}, ensure_ascii=False, indent=1))
        return 0
    print(f'baseline: {baseline["name"]} ({baseline["documents"]} documents); {result["sentences"]} sentence(s)')
    for r in result["rates"]:
        line = f'{r["rate"]:<14}{r["value"]:>8}   baseline {r["median"]} ({r["low"]} to {r["high"]})'
        print(line + (f'   {r["mark"]} - {r["hint"]}' if r["mark"] else ""))
    if result["sentences"] and result["sentences"] < MIN_SENTENCES:
        print(f"under {MIN_SENTENCES} sentences: no marks")
    elif result.get("off"):
        print(f'off: {result["marks"]} rates sit on the far side of what 95 % of the baseline documents hold')
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
