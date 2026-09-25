# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "sudachipy>=0.6.8",
#     "sudachidict-core>=20240409",
# ]
# ///
"""koyobun.py - Japanese style checks that need morphology.

textlint and the vocabulary register work on surface strings. The checks here
turn on parts of speech, so this script tokenises with sudachipy and reports
each suspicion with a line number. Every hit is a suspicion; the ruling belongs
to the caller.

Checks (id - rule). The first four paraphrase items of 「公用文作成の考え方」
(文化審議会建議, 2022-01-07); the other five are house rules, each with the
item of the 建議 it leans on.
    passive          use the passive sparingly (Ⅲ-3 ケ)
    clause_chain     avoid long chains of conjunctive particles and continuative forms, 3 or more (Ⅲ-3 カ)
    kanji_suru       limit verbs made of one kanji and する (Ⅱ-8)
    etc              use 等 and など with care (Ⅱ-5 イ)
    ga_conjunction   house rule: every conjunctive が, for the reader to keep the contrastive ones (after Ⅲ-3 カ)
    tari_single      house rule: a たり with no partner; standard usage pairs it (AたりBたり)
    sasete_itadaku   house rule: させていただく where no permission is being asked (after Ⅱ-6 ウ)
    nominal_ending   house rule: 体言止め in body sentences (after JTF style guide 1.1.2/1.1.3)
    negated_predicate house rule: the sentence's final predicate is negated

Usage:
    uv run koyobun.py [--json] <file>
    uv run koyobun.py --nj-dir      # print the natural-japanese scripts directory

Sentence splitting and Markdown masking come from natural-japanese's textcore.py,
so a sentence here is the same sentence lint.py sees. The natural-japanese plugin
(https://github.com/coji/natural-japanese) must be installed; its scripts
directory is found through NATURAL_JAPANESE_SCRIPTS, the marketplace clone or
the plugin cache, in that order. Headings, list items, tables,
quotes and code are masked there, which is what makes nominal_ending a body-only
check.

Exit code 0 on any number of findings; 1 on an input error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

def find_textcore_dir() -> Path | None:
    env = os.environ.get("NATURAL_JAPANESE_SCRIPTS")
    plugins = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "plugins"
    tail = "skills/natural-japanese/scripts"
    candidates = [Path(env)] if env else []
    candidates.append(plugins / "marketplaces/natural-japanese" / tail)
    def version(p: Path) -> tuple:
        return tuple(int(n) if n.isdigit() else 0 for n in p.parents[2].name.split("."))

    candidates += sorted((plugins / "cache").glob(f"*/natural-japanese/*/{tail}"), key=version, reverse=True)
    return next((c for c in candidates if (c / "textcore.py").is_file()), None)


TEXTCORE_DIR = find_textcore_dir()
if TEXTCORE_DIR is None:
    print("error: natural-japanese is not installed; install the plugin or set NATURAL_JAPANESE_SCRIPTS", file=sys.stderr)
    sys.exit(1)
sys.path.insert(0, str(TEXTCORE_DIR))
try:
    from textcore import (  # noqa: E402
        get_tokenizer,
        iter_lines_with_no,
        mask_markdown_structure,
        read_source_file,
        split_sentences_with_lines,
        strip_trailing_symbols,
    )
except ImportError as exc:  # the marketplace clone is gone or moved
    print(f"error: textcore.py could not be imported from {TEXTCORE_DIR}: {exc}", file=sys.stderr)
    sys.exit(1)

CHAIN_THRESHOLD = 3
# The guideline's examples are 模する, 擬する, 賭する and 滅する. These three work
# as particles, so this script exempts them.
KANJI_SURU_ALLOW = {"関する", "対する", "際する"}
KANJI_SURU_RE = re.compile(r"^[一-鿿々]する$")
NEGATORS = {"ない", "ぬ", "ん"}
HINTS = {
    "passive": "受身。動作主を主語にして能動で書けるなら書き換える",
    "clause_chain": "接続助詞・中止法が {n} 箇所。文を分ける",
    "kanji_suru": "漢字１字＋する。二字の熟語か訓読みの動詞で書く",
    "nominal_ending": "本文の体言止め。述語で終える",
    "etc": "「等」「など」。前に代表的・典型的なものを挙げる",
    "ga_conjunction": "接続助詞「が」。逆接でなければ文を切るか、「ので」「ため」で続ける",
    "tari_single": "「たり」が一つ。「AたりBたり」と繰り返すか、「たり」を使わずに書く",
    "sasete_itadaku": "「させていただく」。相手の許可を得る場面でなければ「します」「いたします」で書く",
    "negated_predicate": "文末の述語が否定。何であるかを書く（動詞を単に打ち消した文は残る）",
}


def _pos(m) -> tuple:
    return m.part_of_speech()


def _findings_for(sentence, line: int, raw: str, ms: list) -> list[dict]:
    out: list[dict] = []

    def add(check: str, excerpt: str, **fmt) -> None:
        out.append({"line": line, "check": check, "excerpt": excerpt, "hint": HINTS[check].format(**fmt)})

    body = strip_trailing_symbols(ms)
    if not body:
        return out

    chain = 0
    tari = 0
    for i, m in enumerate(ms):
        pos = _pos(m)
        surf = m.surface()
        lemma = m.dictionary_form()

        # が as a 接続助詞 joins two clauses; the guideline keeps it for
        # contrast. Whether the clauses contrast is the caller's reading.
        if pos[0] == "助詞" and pos[1] == "接続助詞" and surf == "が":
            add("ga_conjunction", "".join(x.surface() for x in ms[max(0, i - 6) : i + 1]))

        # たり/だり as a 副助詞, counted per sentence and judged after the loop.
        if pos[0] == "助詞" and pos[1] == "副助詞" and lemma in {"たり", "だり"}:
            tari += 1

        # させていただく: する(未然)+せる+て+いただく, in any spelling of いただく.
        if (
            lemma == "せる"
            and i >= 1
            and ms[i - 1].dictionary_form() == "する"
            and i + 2 < len(ms)
            and ms[i + 1].surface() == "て"
            and ms[i + 2].dictionary_form() in {"いただく", "頂く"}
        ):
            add("sasete_itadaku", "".join(x.surface() for x in ms[max(0, i - 2) : i + 3]))

        # passive: れる/られる right after a verb (possible, honorific and
        # spontaneous readings share the form, so the ruling is the caller's).
        if pos[0] == "助動詞" and lemma in {"れる", "られる"} and i > 0 and _pos(ms[i - 1])[0] == "動詞":
            add("passive", ms[i - 1].surface() + surf)

        # clause chain: a 接続助詞, or a 連用形 verb/adjective before a 読点 (中止法).
        if pos[0] == "助詞" and pos[1] == "接続助詞":
            chain += 1
        elif (
            pos[0] in {"動詞", "形容詞", "助動詞"}
            and pos[5].startswith("連用形")
            and i + 1 < len(ms)
            and _pos(ms[i + 1])[1] == "読点"
        ):
            chain += 1

        # 漢字１字＋する, either as one verb token (資する) or as a one-kanji
        # noun followed by する (達＋する).
        if pos[0] == "動詞" and KANJI_SURU_RE.match(lemma) and lemma not in KANJI_SURU_ALLOW:
            add("kanji_suru", surf)
        elif (
            pos[0] == "名詞"
            and len(surf) == 1
            and re.match(r"[一-鿿]", surf)
            and i + 1 < len(ms)
            and ms[i + 1].dictionary_form() == "する"
            and _pos(ms[i + 1])[0] == "動詞"
            and surf + "する" not in KANJI_SURU_ALLOW
        ):
            add("kanji_suru", surf + ms[i + 1].surface())

        if surf in {"等", "など"} and pos[0] in {"助詞", "接尾辞", "名詞"}:
            add("etc", surf)

    if chain >= CHAIN_THRESHOLD:
        add("clause_chain", raw, n=chain)
    if tari == 1:
        add("tari_single", raw)

    # nominal ending: the last content morpheme is a noun and the sentence is
    # closed (a 。, or the last line of its paragraph). A hard-wrapped line that
    # ends mid-sentence has neither and is skipped.
    last = body[-1]
    has_letters = re.search(r"[一-鿿々ぁ-ゖァ-ヺA-Za-z0-9]", last.surface())  # emoji tag as 名詞
    if _pos(last)[0] in {"名詞", "代名詞"} and has_letters and sentence["closed"]:
        add("nominal_ending", raw)

    # negated predicate: a negator inside the final predicate chunk, i.e. after
    # the last noun or case/topic particle.
    tail_start = 0
    for i, m in enumerate(body):
        pos = _pos(m)
        if pos[0] in {"名詞", "代名詞"} or (pos[0] == "助詞" and pos[1] in {"格助詞", "係助詞", "副助詞"}):
            tail_start = i + 1
    # The negator has to close the predicate: only auxiliaries and particles may
    # follow it (ないだろう, ませんでした). なんとなく tokenises as なん+と+なく,
    # and that なく sits before a verb, so it stays silent.
    tail = body[tail_start:]
    for i, m in enumerate(tail):
        is_neg = (_pos(m)[0] == "助動詞" and m.dictionary_form() in NEGATORS) or (
            _pos(m)[0] == "形容詞" and m.dictionary_form() == "ない"
        )
        if is_neg and all(_pos(x)[0] in {"助動詞", "助詞", "補助記号"} for x in tail[i + 1 :]):
            add("negated_predicate", raw)
            break
    return out


def run(text: str) -> tuple[list[dict], dict]:
    masked = mask_markdown_structure(text)
    lines = iter_lines_with_no(masked)
    raw_by_no = dict(iter_lines_with_no(text))
    sentences = split_sentences_with_lines(lines, raw_by_no)
    tok = get_tokenizer()
    from sudachipy import SplitMode

    findings: list[dict] = []
    for no, sent, raw in sentences:
        # The splitter drops the 。 it split on, so look at what follows the
        # piece in its source line: a delimiter, or nothing at a paragraph end.
        raw_line = raw_by_no.get(no, "")
        idx = raw_line.find(raw)
        after = raw_line[idx + len(raw):].lstrip() if idx >= 0 else ""
        next_line = raw_by_no.get(no + 1, "")
        closed = after.startswith(("。", "！", "？", "．")) or (after == "" and not next_line.strip())
        ms = list(tok.tokenize(sent, SplitMode.C))
        findings.extend(_findings_for({"closed": closed}, no, raw, ms))
    counts: dict[str, int] = {}
    for f in findings:
        counts[f["check"]] = counts.get(f["check"], 0) + 1
    stats = {"sentences": len(sentences), "by_check": counts}
    return findings, stats


def main() -> int:
    if sys.argv[1:] == ["--nj-dir"]:
        print(TEXTCORE_DIR)
        return 0
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text, err = read_source_file(Path(args.file))
    if err:
        print(err, file=sys.stderr)
        return 1
    findings, stats = run(text)
    if args.json:
        print(json.dumps({"file": args.file, "stats": stats, "findings": findings}, ensure_ascii=False, indent=2))
        return 0
    for f in findings:
        print(f'L{f["line"]} [{f["check"]}] {f["excerpt"]} - {f["hint"]}')
    print(f'{len(findings)} finding(s) in {stats["sentences"]} sentence(s): {stats["by_check"]}')
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
