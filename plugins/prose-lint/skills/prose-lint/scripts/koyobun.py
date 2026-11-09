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
(文化審議会建議, 2022-01-07); the other five are house rules, three of them
with the item of the 建議 they lean on.
    passive          use the passive sparingly (Ⅲ-3 ケ)
    clause_chain     avoid long chains of conjunctive particles and continuative forms, 3 or more (Ⅲ-3 カ)
    comma_chain      house rule: clauses strung on 読点 (Aし、Bして、Cする), 2 or more clause-closing 読点 (after Ⅲ-3 カ)
    kanji_suru       limit verbs made of one kanji and する (Ⅱ-8)
    etc              use 等 and など with care (Ⅱ-5 イ)
    ga_conjunction   house rule: every conjunctive が, for the reader to keep the contrastive ones (after Ⅲ-3 カ)
    sasete_itadaku   house rule: させていただく where no permission is being asked (after Ⅱ-6 ウ)
    nominal_ending   house rule: 体言止め in body sentences (after JTF style guide 1.1.2/1.1.3)
    negated_predicate house rule: the sentence's final predicate is negated

Five more read the parts the sentence checks mask: the header row of each
Markdown table, and the slides of a deck that pptx_text.py wrote
(`## Slide <n>` sections). The table rules follow the
header guidance of the Microsoft Writing Style Guide and the WordPress
documentation style guide; the title rules follow 「公用文作成の考え方」 Ⅲ-2
on 標題 and 見出し, and Garner and Alley (2013) on two-line slide headlines.
    table_deixis     a column header opens with a demonstrative or a referring word (その確率, 上記の値);
                     その他, これまで and これから stay
    table_particle   a column header ends in が, を, に or の and runs on into its cells
    title_symbol     a slide title holds no Japanese word, no Latin word of 4 letters and no lower-case
                     word of 3 (ET, W1, KPI); the thresholds are this skill's
    title_lines      a slide title runs over 2 lines in the extract
    title_only       a slide holds only its title and at most a page number, the title is a sentence
                     (a 読点, or a predicate at its end), and it has no word for the slide's role from
                     this skill's list (課題, 例題, 問題, 目標, まとめ, 要点, 目次, 結論) and no line of thanks

With --academic, two more checks list the spoken forms that a surface regex
cannot tell from ordinary verbs (使って, したがって, もたらす). Both come from
the table of 話し言葉的 words in 柏野ほか (2016), 言語処理学会第22回年次大会
P18-1; references/academic-japanese.md cites the rest.
    tte              って as a particle (この手法って, 来るって言った)
    tara             たら/だら, the conditional of た (上げたら, 読んだら)

Usage:
    uv run koyobun.py [--academic] [--json] <file>
    uv run koyobun.py --nj-dir      # print the natural-japanese scripts directory

Sentence splitting and Markdown masking come from natural-japanese's textcore.py,
so a sentence here is the same sentence lint.py sees. natural-japanese
(https://github.com/coji/natural-japanese, MIT) ships with this skill in
vendor/natural-japanese; NATURAL_JAPANESE_SCRIPTS, when set, names another copy
of its scripts directory. Headings, list items, tables,
quotes and code are masked there, which is what makes nominal_ending a body-only
check. In a deck extract the `- ` items hold the slide text, so they are read as
body text, and nominal_ending stays silent on them.

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
    candidates = [Path(env)] if env else []
    candidates.append(Path(__file__).resolve().parent.parent / "vendor/natural-japanese/scripts")
    return next((c for c in candidates if (c / "textcore.py").is_file()), None)


TEXTCORE_DIR = find_textcore_dir()
if TEXTCORE_DIR is None:
    print("error: vendor/natural-japanese/scripts/textcore.py is missing; reinstall prose-lint or set NATURAL_JAPANESE_SCRIPTS", file=sys.stderr)
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
COMMA_CHAIN_THRESHOLD = 2
# について, に対して, として and their kin: a 格助詞, a verb and て to the
# tokeniser, one particle to the reader, so they join no clauses.
COMPOUND_PARTICLES = {
    ("に", "つく"), ("に", "対する"), ("に", "関する"), ("に", "よる"),
    ("に", "おく"), ("に", "とる"), ("と", "する"),
}
# The guideline's examples are 模する, 擬する, 賭する and 滅する. These three work
# as particles, so this script exempts them.
KANJI_SURU_ALLOW = {"関する", "対する", "際する"}
KANJI_SURU_RE = re.compile(r"^[一-鿿々]する$")
NEGATORS = {"ない", "ぬ", "ん"}
HINTS = {
    "passive": "受身。動作主を主語にして能動で書けるなら書き換える",
    "clause_chain": "接続助詞・中止法が {n} 箇所。文を分ける",
    "comma_chain": "読点で節を {n} 回つないだ文。節ごとに文を分けるか、箇条書きにする",
    "kanji_suru": "漢字１字＋する。二字の熟語か訓読みの動詞で書く",
    "nominal_ending": "本文の体言止め。述語で終える",
    "etc": "「等」「など」。前に代表的・典型的なものを挙げる",
    "ga_conjunction": "接続助詞「が」。逆接でなければ文を切るか、「ので」「ため」で続ける",
    "sasete_itadaku": "「させていただく」。相手の許可を得る場面でなければ「します」「いたします」で書く",
    "negated_predicate": "文末の述語が否定。何であるかを書く（動詞を単に打ち消した文は残る）",
    "tte": "助詞「って」。話し言葉の形。主題なら「は」「とは」、引用なら「と」「という」で書く",
    "tara": "仮定の「たら」。話し言葉の形。「と」「ば」「場合」で書く",
    "table_deixis": "表の見出しが「{word}」で始まる。指す語を見出しに書き、見出しだけで列の値が分かるようにする",
    "table_particle": "表の見出しが助詞「{word}」で終わり、セルへ続く。列の値を表す名詞で終える",
    "title_symbol": "タイトルが記号と英数字だけ。何を示すかを言葉で書く",
    "title_lines": "タイトルが {n} 行。主題と要点を 2 行以内にまとめ、残りは本文に書く",
    "title_only": "タイトルだけのスライドの文に、役割を表す語（課題、まとめ、結論など）がない。役割を書くか、文を本文に移して要点をタイトルにする",
}
# Words that point at text outside a table header. The 同 words are listed one
# by one, since 同義語 and 同順位 name no earlier item; 同 as a word of its own
# (「同」「同 減少」「同、2022年」) is matched in _header_findings.
REFERRING = {
    "この", "その", "あの", "これ", "それ", "あれ", "ここ", "そこ", "あそこ", "こちら", "そちら", "あちら",
    "当該", "上記", "下記", "前記", "後記", "上述", "前述", "後述", "左記", "右記", "前者", "後者", "その後",
    "同上", "同左", "同右", "同前", "同社", "同氏", "同年", "同月", "同日", "同所", "同表", "同図", "同欄",
}
ROLE_WORDS = {"課題", "例題", "問題", "目標", "まとめ", "要点", "目次", "結論"}
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
JAPANESE_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿々]")
SLIDE_RE = re.compile(r"^## Slide \d+$")


def _pos(m) -> tuple:
    return m.part_of_speech()


def _compound_particle(ms: list, i: int) -> bool:
    v = i - 1 if ms[i].surface() == "て" else i
    return v >= 1 and (ms[v - 1].surface(), ms[v].dictionary_form()) in COMPOUND_PARTICLES


def _finding(line: int, check: str, excerpt: str, **fmt) -> dict:
    return {"line": line, "check": check, "excerpt": excerpt, "hint": HINTS[check].format(**fmt)}


def _findings_for(sentence, line: int, raw: str, ms: list) -> list[dict]:
    out: list[dict] = []

    def add(check: str, excerpt: str, **fmt) -> None:
        out.append(_finding(line, check, excerpt, **fmt))

    body = strip_trailing_symbols(ms)
    if not body:
        return out

    chain = 0
    commas = 0
    for i, m in enumerate(ms):
        pos = _pos(m)
        surf = m.surface()
        lemma = m.dictionary_form()

        # が as a 接続助詞 joins two clauses; the guideline keeps it for
        # contrast. Whether the clauses contrast is the caller's reading.
        if pos[0] == "助詞" and pos[1] == "接続助詞" and surf == "が":
            add("ga_conjunction", "".join(x.surface() for x in ms[max(0, i - 6) : i + 1]))

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
        # comma chain: the same joints, counted only where a 読点 follows
        # (「、」「，」「,」). A clause closed by a noun (ため、 ところ、) is outside
        # both counts.
        before_comma = i + 1 < len(ms) and _pos(ms[i + 1])[1] == "読点"
        is_joint = (pos[0] == "助詞" and pos[1] == "接続助詞") or (
            pos[0] in {"動詞", "形容詞", "助動詞"} and pos[5].startswith("連用形") and before_comma
        )
        if is_joint and not _compound_particle(ms, i):
            chain += 1
            commas += before_comma

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

        if sentence["academic"]:
            context = "".join(x.surface() for x in ms[max(0, i - 4) : i + 2])
            if pos[0] == "助詞" and surf == "って":
                add("tte", context)
            if pos[0] == "助動詞" and lemma == "た" and surf in {"たら", "だら"}:
                add("tara", context)

    if chain >= CHAIN_THRESHOLD:
        add("clause_chain", raw, n=chain)
    if commas >= COMMA_CHAIN_THRESHOLD:
        add("comma_chain", raw, n=commas)

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


def _cells(row: str) -> list[str]:
    """Split a Markdown table row into its cells, without <br>, emphasis or code marks."""
    row = row.strip().removeprefix("|")
    row = row[:-1] if row.endswith("|") and not row.endswith("\\|") else row
    return [re.sub(r"<br\s*/?>", " ", c).replace("\\|", "|").strip().strip("*_`").strip()
            for c in re.split(r"(?<!\\)\|", row)]


def _header_findings(line: int, cell: str, tok, mode) -> list[dict]:
    """Check one column header for a referring opening and a particle ending."""
    ms = list(tok.tokenize(cell, mode)) if cell else []
    if not ms:
        return []
    out = []
    first = ms[0].surface()
    ditto = first == "同" and (len(ms) == 1 or _pos(ms[1])[0] in {"空白", "補助記号"})
    # その他 names a category, and これまで and これから a time.
    named = len(ms) > 1 and (first, ms[1].surface()) in {("その", "他"), ("その", "ほか"), ("これ", "まで"), ("これ", "から")}
    if (first in REFERRING or ditto) and not named:
        out.append(_finding(line, "table_deixis", cell, word=first))
    # Punctuation after the particle is dropped; a closing bracket stays, so the
    # が of 「h2（が）」 reads as a quoted token.
    while len(ms) > 1 and _pos(ms[-1])[0] == "補助記号" and _pos(ms[-1])[1] != "括弧閉":
        ms.pop()
    if _pos(ms[-1])[:2] == ("助詞", "格助詞") and ms[-1].surface() in {"が", "を", "に", "の"}:
        out.append(_finding(line, "table_particle", cell, word=ms[-1].surface()))
    return out


def structure_findings(text: str, tok) -> list[dict]:
    """Check the column headers of each table and, in a pptx_text.py extract, the slide titles."""
    from sudachipy import SplitMode

    lines = text.split("\n")
    deck = any(SLIDE_RE.match(x) for x in lines)
    out: list[dict] = []
    slides: list[dict] = []
    fence: tuple[str, int] | None = None  # the open fence's character and length, as textcore tracks it
    for i, line in enumerate(lines):
        if m := FENCE_RE.match(line):
            run = m.group(1)
            if fence is None:
                fence = (run[0], len(run))
            elif run[0] == fence[0] and len(run) >= fence[1] and not m.group(2).strip():
                fence = None
            continue
        if fence:
            continue
        # The header row only: a first column often holds the 同 of a ditto or a quoted answer.
        if "|" in line and TABLE_SEPARATOR_RE.match(line) and i > 0 and "|" in lines[i - 1]:
            for cell in _cells(lines[i - 1]):
                out.extend(_header_findings(i, cell, tok, SplitMode.C))
        if not deck:
            continue
        heading = HEADING_RE.match(line)
        if SLIDE_RE.match(line):
            slides.append({"title": [], "other": False, "notes": False})
        elif not slides or slides[-1]["notes"]:
            continue
        elif heading and heading.group(2) == "Notes":
            slides[-1]["notes"] = True
        elif heading and len(heading.group(1)) == 3:
            slides[-1]["title"].append((i + 1, heading.group(2)))
        elif line.strip() and not re.fullmatch(r"(- )?\d+", line.strip()):  # a page number is no content
            slides[-1]["other"] = True
    for s in slides:
        if not s["title"]:
            continue
        no, parts = s["title"][0][0], [t for _, t in s["title"]]
        excerpt, whole = " / ".join(parts), "".join(parts)
        # Four letters, or three in lower case, make a word (softmax, Thank You, ask);
        # ET, W1 and KPI are symbols. The thresholds are this skill's.
        if not JAPANESE_RE.search(whole) and not re.search(r"[A-Za-z]{4}|[a-z]{3}", " ".join(parts)):
            out.append(_finding(no, "title_symbol", excerpt))
        if len(parts) > 2:
            out.append(_finding(no, "title_lines", excerpt, n=len(parts)))
        # A section or closing slide names its section in a noun phrase; a sentence
        # alone on a slide leaves the reader to guess what it is.
        ms = list(tok.tokenize(whole, SplitMode.C))
        body = strip_trailing_symbols(ms)
        sentence = bool(re.search("[、，]", whole)) or (body and _pos(body[-1])[0] in {"動詞", "助動詞", "形容詞"})
        # A role word labels the slide when a colon, a は or the end follows it
        # (課題：…, 目標は…); the 問題 of 問題なく labels nothing. A closing line of
        # thanks says what its slide is too.
        role = "ありがとう" in whole or any(m.surface() in ROLE_WORDS and (
            k + 1 == len(ms) or _pos(ms[k + 1])[0] in {"補助記号", "空白"} or ms[k + 1].surface() == "は")
            for k, m in enumerate(ms))
        if not s["other"] and sentence and not role:
            out.append(_finding(no, "title_only", excerpt))
    return out


def run(text: str, academic: bool = False) -> tuple[list[dict], dict]:
    # A deck extract holds its slide text in `- ` items, which the mask blanks; read
    # them as body text, and leave the 体言止め of a bullet, the medium's form, alone.
    deck = any(SLIDE_RE.match(x) for x in text.split("\n"))
    items = {no for no, x in enumerate(text.split("\n"), 1) if deck and x.startswith("- ")}
    body_text = re.sub(r"^- ", "", text, flags=re.MULTILINE) if deck else text
    masked = mask_markdown_structure(body_text)
    lines = iter_lines_with_no(masked)
    raw_by_no = dict(iter_lines_with_no(body_text))
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
        findings.extend(f for f in _findings_for({"closed": closed, "academic": academic}, no, raw, ms)
                        if not (f["check"] == "nominal_ending" and no in items))
    findings = sorted(findings + structure_findings(text, tok), key=lambda f: f["line"])
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
    ap.add_argument("--academic", action="store_true", help="also list the spoken particles tte and tara")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text, err = read_source_file(Path(args.file))
    if err:
        print(err, file=sys.stderr)
        return 1
    findings, stats = run(text, academic=args.academic)
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
