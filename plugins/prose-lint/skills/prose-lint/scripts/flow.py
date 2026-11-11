# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "sudachipy>=0.6.8",
#     "sudachidict-core>=20240409",
# ]
# ///
"""flow.py - how the body sentences of a Japanese document end, join and vary.

The other scripts report a wording to take out. This one counts what a rewrite
tends to take out with it: the endings that say how sure the writer is, the
words that join one sentence to the next, and the uneven length of sentences.
It rules on nothing. It prints a profile, the passages where three or more
sentences in a row share one shape, and, with --before, how the profile moved
between the text as it was and the text as it stands.

    uv run flow.py [--before <original>] [--json] <file>

Per body sentence (headings, tables, quotes and code are masked, as in
koyobun.py). A list item is running text when it holds two or more sentences,
or one sentence of 60 characters or more, which is what two short sentences
become once joined; it is read as a paragraph of its own, without a label in
bold at its head. A shorter item, or a phrase, stays masked. A deck extract's `- ` items are read
as body text:

    ending   the class of the final predicate:
             plain     a bare statement (する, した, だ, である, です, ます, ている)
             explain   のだ, のである, のです, ためである, からだ, わけだ
             judge     だろう, でしょう, と考えられる, と思われる, といえる, かもしれない,
                       はずだ, ようだ, らしい, 可能性がある, おそれがある, 見込みだ
             stance    べきだ, たい, とよい, てほしい, てください, ましょう, 必要がある,
                       なければならない, てはならない, 欠かせない, 願う
             negative  ない, ません, with none of the above
             question  か, ？
             nominal   体言止め
    form     the last two morphemes, which is what the eye sees repeat (ます, でした, である)
    opener   the sentence opens with a connective (しかし, そのため, また, 例えば) or a
             demonstrative (この, その, これ, それ, こうした)
    joints   接続助詞 and 連用中止 inside the sentence, counted as koyobun.py counts them
    lone     no opener, no joint and no demonstrative: a sentence tied to nothing around it
    topic    the sentence opens on a topic of its own: no opener, and a noun with は inside its first
             clause (up to the first 読点). では, には and their kin set a scene and stay out
    paren    the sentence holds a parenthesis: a gloss, a short name or a source kept inside it

The profile gives, over the body sentences: their count, mean length and its
coefficient of variation; the share of 100 characters or more and the share
under 30; the share of each ending class; the share that are lone; the share
with an opener; the share that open on a topic of their own; the share that
hold a parenthesis; joints per sentence; and the longest run of one form. A
document of 12 body sentences or more is marked `flat` when 40 % of them or
more are lone and a sentence holds 0.6 joints or fewer. Measured for 1.11.0:
14 columns by 文化庁国語課 (2014-2018), the 建議 and a council report hold 0.75 to
1.63 joints a sentence, and 14 % to 26 % of their sentences are lone, 53 % in
one column; a report Claude wrote under this plugin's hooks held 0.46 and 54 %.
Measured for 1.12.0 on 35 documents of ministries and public bodies (2009-2022)
and on drafts Claude wrote from notes of eight of them: the eight hold 15 % of
sentences of 100 characters or more (median) and their drafts 0 %, 4 % under 30
characters and 19 %, 17 % opening on a topic of their own and 32 %, 18 % with a
parenthesis and 12 %. references/flow-japanese.md, section 4, has the tables.
Two kinds of passage are listed with their lines:

    ending_run  three or more sentences in a row, in one paragraph, with the same form
                and the same class
    lone_run    three or more lone sentences in a row, in one paragraph

A run is a place to read, and a finding only when the sentences differ in kind
(a fact, its reason, a judgement) and the shape hides it. A list of steps or of
measured values is uniform by nature.

With --before, each figure is printed for both texts, and a line is marked
`flatter` when it moved the way a rewrite flattens a text: more plain endings,
fewer openers, fewer joints, more lone sentences, more sentences, less variation
in length, fewer long sentences, more short ones, more sentences opening on a
topic of their own. The marks are a direction, like the naturalness score; the
thresholds are this skill's, set on the documents SKILL.md names.

Sentence splitting and masking come from natural-japanese's textcore.py, as in
koyobun.py. A full stop written 「．」 is read as 「。」. Exit code 0; 1 on an input
error.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import koyobun  # noqa: E402 - the tokeniser, the mask and the joint rule are shared
from koyobun import (  # noqa: E402
    get_tokenizer,
    iter_lines_with_no,
    mask_markdown_structure,
    read_source_file,
    split_sentences_with_lines,
    strip_trailing_symbols,
)

RUN = 3  # sentences in a row that make a run
ITEM_SENTENCE_CHARS = 60  # a one-sentence list item this long is read as prose
LONG_CHARS = 100  # a sentence this long carries a ground and its claim, or a concession and a verdict
SHORT_CHARS = 30  # a sentence under this is one clause
TOPIC_CLAUSE_MORPHEMES = 14  # how far into a sentence with no 読点 its opening clause is read
LIST_ITEM_RE = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(?:\*\*[^*]+\*\*[:：]?\s*)?")
# Below these, a document is too short to call flat, and its figures say little.
FLAT_MIN_SENTENCES = 12
FLAT_LONE_PCT = 40.0
FLAT_JOINTS = 0.6
ENDINGS = (
    ("question", r"(?:か|かな|だろうか|でしょうか|のか)$|[？?]$"),
    ("explain", r"(?<!も)(?:の|ん)(?:だ|です|である|でした|だった|であった|であろう)$|(?:ため|から|わけ|ゆえ)(?:だ|です|である|でした|だった|であった)$"),
    ("judge", r"(?:だろう|でしょう|であろう|かもしれない|かもしれません|かも知れない|はず(?:だ|です|である)"
              r"|と(?:考え|思わ|み|見|推定さ|推測さ|予想さ|期待さ|解釈さ)られ(?:る|ます|た|ました|ている|ています)"
              r"|と(?:考える|考えます|考えている|考えています|思う|思います|みる|推定する|推測する)"
              r"|と(?:いえる|言える|いえます|言えます|いえよう|言えよう|解釈できる|判断できる)"
              r"|(?:よう|そう|みたい)(?:だ|です|である)|らしい|らしいです"
              r"|(?:可能性|おそれ|恐れ|見込み|余地)(?:が|も|は)(?:ある|あります|高い|低い|否定できない|残る|残ります)"
              r"|見込み(?:だ|です|である)|(?:と|が)(?:示唆|推察)され(?:る|ます|ている))$"),
    ("stance", r"(?:べき(?:だ|です|である|だろう|でしょう)|たい|たいです|たいと(?:考え|思い)(?:る|ます|ています)"
               r"|(?:と|ば|ほうが|方が)(?:よい|良い|いい)(?:です|だろう|でしょう)?|てほしい|て欲しい|てください|て下さい"
               r"|ましょう|(?:よ|こ|そ|ろ|と|も|お|ぼ|の)う|必要(?:が|は)(?:ある|あります)|必要(?:だ|です|である)"
               r"|なければな(?:らない|りません)|なくてはな(?:らない|りません)|てはな(?:らない|りません)"
               r"|欠かせない|欠かせません|願(?:う|います|いします|いいたします)|お勧めします|勧める|望ましい|望ましいです|望まれる)$"),
    ("negative", r"(?:ない|ません|ぬ|ず)(?:です|でした|だろう|でしょう)?$|(?:なかった|ませんでした)$"),
)
ENDINGS = tuple((name, re.compile(pattern)) for name, pattern in ENDINGS)
# Words that open a sentence by joining it to the one before. A 接続詞 by part of speech counts too.
OPENERS = (
    "しかし", "だが", "ただ", "ただし", "もっとも", "とはいえ", "それでも", "一方", "他方", "反対に", "逆に", "むしろ",
    "そのため", "このため", "したがって", "よって", "そこで", "それゆえ", "ゆえに", "だから", "ですから", "なので", "その結果",
    "また", "さらに", "加えて", "なお", "しかも", "そして", "次に", "まず", "最後に", "続いて", "併せて", "あわせて", "同様に",
    "つまり", "すなわち", "要するに", "言い換えると", "例えば", "たとえば", "具体的には", "特に", "とりわけ", "実際", "実は",
    "なぜなら", "というのも", "では", "それでは", "さて", "ところで", "ちなみに", "このように", "こうして", "以上", "いずれにせよ",
)
DEMONSTRATIVES = re.compile(r"(?<![一-鿿ぁ-ゖァ-ヺ])(?:この|その|これ|それ|こう|そう|ここ|そこ|こちら|そちら|当該|同[様社氏年月日])")
OPENER_RE = re.compile(r"^(?:" + "|".join(sorted(OPENERS, key=len, reverse=True)) + r")(?=[、，,はもにでがを]|$|[一-鿿ぁ-ゖァ-ヺ])")
DEMO_OPEN_RE = re.compile(r"^(?:この|その|これ|それ|こう|そう|ここ|そこ|こちら|そちら|当該|同[様社氏年月日])")
NEGATORS = {"ない", "ぬ", "ず", "ん"}


def _pos(m) -> tuple:
    return m.part_of_speech()


def ending_of(text: str, tok, mode) -> tuple[str, str]:
    """Return (class, form) of a sentence's final predicate."""
    core = koyobun.TAIL_NOTE_RE.sub("", text.strip()).strip()
    core = re.sub(r"[。．.！!、，\s]+$", "", core)
    question = text.strip().endswith(("？", "?")) or core.endswith(("？", "?"))
    core = core.rstrip("？?")
    ms = strip_trailing_symbols(list(tok.tokenize(core, mode)))
    if not ms:
        return "nominal", ""
    form = "".join(m.surface() for m in ms[-2:])
    last = ms[-1]
    if question:
        return "question", form
    if _pos(last)[0] in {"名詞", "代名詞", "接尾辞"} and re.search(r"[一-鿿々ぁ-ゖァ-ヺA-Za-z0-9]", last.surface()):
        # 見込み。 and 必要。 are 体言止め; 見込みだ is caught by the classes below.
        return "nominal", form
    for name, pattern in ENDINGS:
        if pattern.search(core):
            if name == "stance" and re.search(r"(?:よ|こ|そ|ろ|と|も|お|ぼ|の)う$", core):
                # 意志の う (しよう, 考えよう): a verb's 意志推量形. だろう and でしょう were caught as judge.
                if not (_pos(last)[0] == "助動詞" and last.dictionary_form() in {"う", "よう"}) and not _pos(last)[5].startswith("意志推量形"):
                    continue
            if name == "question" and not (_pos(last)[0] == "助詞" and _pos(last)[1] in {"終助詞", "副助詞"}):
                continue
            if name == "negative" and not any(
                # 少ない and 危ない end in ない and deny nothing.
                (_pos(m)[0] == "助動詞" and m.dictionary_form() in NEGATORS) or (_pos(m)[0] == "形容詞" and m.dictionary_form() == "ない")
                for m in ms[-4:]
            ):
                continue
            return name, form
    return "plain", form


def opens_on_topic(ms: list) -> bool:
    """True when a noun with は stands in the opening clause: 「政府は、…」「この制度の対象は…」.

    では, には, については and their kin put は after a particle; they set a scene and are left out.
    """
    head = []
    for m in ms:
        pos = _pos(m)
        if pos[1] == "読点" or len(head) >= TOPIC_CLAUSE_MORPHEMES:
            break
        if pos[0] not in {"補助記号", "空白"}:
            head.append(m)
    for i, m in enumerate(head):
        if i and m.surface() == "は" and _pos(m)[0] == "助詞" and _pos(m)[1] == "係助詞":
            return _pos(head[i - 1])[0] != "助詞"
    return False


def joints_of(ms: list) -> int:
    """Count 接続助詞 and 連用中止, by koyobun.py's rule for clause_chain."""
    n = 0
    for i, m in enumerate(ms):
        pos = _pos(m)
        before_comma = i + 1 < len(ms) and _pos(ms[i + 1])[1] == "読点"
        is_joint = (pos[0] == "助詞" and pos[1] == "接続助詞") or (
            pos[0] in {"動詞", "形容詞", "助動詞"} and pos[5].startswith("連用形") and before_comma
        )
        if is_joint and not koyobun._compound_particle(ms, i):
            n += 1
    return n


def read_sentences(text: str) -> list[dict]:
    """Return the body sentences with their line, paragraph number and features."""
    text = re.sub(r"(?<=[ぁ-ゖァ-ヺ一-鿿々）」\])])．", "。", text)
    deck = any(koyobun.SLIDE_RE.match(x) for x in text.split("\n"))
    body_text = re.sub(r"^- ", "", text, flags=re.MULTILINE) if deck else text
    # A list item of two or more sentences, or of one long sentence, is prose: drop its marker so
    # the mask keeps the line.
    rows, items, fence = body_text.split("\n"), set(), False
    for i, row in enumerate(rows):
        if koyobun.FENCE_RE.match(row):
            fence = not fence
        m = None if fence else LIST_ITEM_RE.match(row)
        ends = 0 if not m else len(re.findall(r"[。！？]", row[m.end():]))
        if m and (ends >= 2 or (ends == 1 and len(re.sub(r"\s", "", row[m.end():])) >= ITEM_SENTENCE_CHARS)):
            rows[i] = row[m.end():]
            items.add(i + 1)
    body_text = "\n".join(rows)
    masked = mask_markdown_structure(body_text)
    lines = iter_lines_with_no(masked)
    raw_by_no = dict(iter_lines_with_no(body_text))
    # A paragraph ends at a blank or masked line; a list item is a paragraph of its own.
    para_of, para, prev_blank = {}, 0, True
    for no, line in lines:
        if line.strip():
            if prev_blank or no in items or (no - 1) in items:
                para += 1
            para_of[no] = para
        prev_blank = not line.strip()
    tok = get_tokenizer()
    from sudachipy import SplitMode

    out = []
    for no, sent, raw in split_sentences_with_lines(lines, raw_by_no):
        if not re.search(r"[ぁ-ゖ]", sent):
            continue  # a label, a figure or a line of Latin text is no sentence to profile
        ms = list(tok.tokenize(sent, SplitMode.C))
        cls, form = ending_of(sent, tok, SplitMode.C)
        head = sent.lstrip("「『（(　 ")
        first = next((m for m in ms if _pos(m)[0] not in {"補助記号", "空白"}), None)
        connective = bool(OPENER_RE.match(head)) or (first is not None and _pos(first)[0] == "接続詞")
        demo_open = bool(DEMO_OPEN_RE.match(head))
        joints = joints_of(ms)
        out.append({
            "line": no, "para": para_of.get(no, 0), "text": raw, "chars": len(re.sub(r"\s", "", sent)),
            "ending": cls, "form": form, "opener": connective or demo_open, "connective": connective,
            "joints": joints, "lone": not (connective or demo_open or joints or DEMONSTRATIVES.search(sent)),
            "topic": not (connective or demo_open) and opens_on_topic(ms),
            "paren": bool(re.search(r"[（(]", sent)),
        })
    return out


def profile(sents: list[dict]) -> dict:
    n = len(sents)
    if not n:
        return {"sentences": 0}
    lengths = [s["chars"] for s in sents]
    mean = statistics.fmean(lengths)
    classes = {c: sum(1 for s in sents if s["ending"] == c) for c in ("plain", "explain", "judge", "stance", "negative", "question", "nominal")}
    longest, run, prev = 0, 0, None
    for s in sents:
        key = (s["para"], s["form"], s["ending"])
        run = run + 1 if key == prev else 1
        prev = key
        longest = max(longest, run)
    pct = lambda k: round(100 * k / n, 1)
    return {
        "sentences": n,
        "mean_chars": round(mean, 1),
        "length_cv": round(statistics.pstdev(lengths) / mean, 2) if mean else 0.0,
        "long_pct": pct(sum(1 for x in lengths if x >= LONG_CHARS)),
        "short_pct": pct(sum(1 for x in lengths if x < SHORT_CHARS)),
        "plain_pct": pct(classes["plain"]),
        "ending_pct": {c: pct(k) for c, k in classes.items()},
        "opener_pct": pct(sum(s["opener"] for s in sents)),
        "connective_pct": pct(sum(s["connective"] for s in sents)),
        "topic_open_pct": pct(sum(s["topic"] for s in sents)),
        "paren_pct": pct(sum(s["paren"] for s in sents)),
        "joints_per_sentence": round(sum(s["joints"] for s in sents) / n, 2),
        "lone_pct": pct(sum(s["lone"] for s in sents)),
        "longest_form_run": longest,
        "flat": n >= FLAT_MIN_SENTENCES and pct(sum(s["lone"] for s in sents)) >= FLAT_LONE_PCT
        and sum(s["joints"] for s in sents) / n <= FLAT_JOINTS,
    }


def runs(sents: list[dict]) -> list[dict]:
    """Return the ending_run and lone_run passages."""
    out = []

    def collect(kind: str, key) -> None:
        group: list[dict] = []
        for s in sents + [None]:
            k = key(s) if s is not None else None
            if group and k is not None and k == key(group[-1]):
                group.append(s)
                continue
            if len(group) >= RUN:
                out.append({
                    "check": kind, "line": group[0]["line"], "to_line": group[-1]["line"], "count": len(group),
                    "form": group[0]["form"] if kind == "ending_run" else "",
                    "excerpt": " / ".join(g["text"][-12:] for g in group[:4]),
                })
            group = [s] if (s is not None and k is not None) else []

    collect("ending_run", lambda s: (s["para"], s["form"], s["ending"]))
    collect("lone_run", lambda s: (s["para"],) if s["lone"] else None)
    return sorted(out, key=lambda f: (f["line"], f["check"]))


# (key, label, the direction that reads flatter: +1 when a rise is flatter, the least change that counts)
MOVES = (
    ("sentences", "sentences", +1, None),
    ("mean_chars", "mean length", -1, None),
    ("length_cv", "length variation (CV)", -1, 0.05),
    ("long_pct", "sentences of 100 characters or more %", -1, 5.0),
    ("short_pct", "sentences under 30 characters %", +1, 5.0),
    ("plain_pct", "plain endings %", +1, 5.0),
    ("opener_pct", "sentences with an opener %", -1, 5.0),
    ("topic_open_pct", "sentences opening on a topic %", +1, 5.0),
    ("joints_per_sentence", "joints per sentence", -1, 0.15),
    ("lone_pct", "lone sentences %", +1, 5.0),
    ("longest_form_run", "longest run of one ending", +1, 1),
)


def compare(before: dict, after: dict) -> list[dict]:
    rows = []
    for key, label, sign, least in MOVES:
        b, a = before.get(key, 0), after.get(key, 0)
        if key == "sentences":
            flatter = b > 0 and a >= b * 1.15  # sentences cut apart: over 15 % more of them
        elif key == "mean_chars":
            flatter = b > 0 and a <= b * 0.85
        else:
            flatter = (a - b) * sign >= least
        rows.append({"key": key, "label": label, "before": b, "after": a, "flatter": bool(flatter)})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--before", help="the text as it was before the rewrite; prints both profiles and how they moved")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text, err = read_source_file(Path(args.file))
    if err:
        print(err, file=sys.stderr)
        return 1
    sents = read_sentences(text)
    result = {"file": args.file, "profile": profile(sents), "runs": runs(sents)}
    if args.before:
        old, err = read_source_file(Path(args.before))
        if err:
            print(err, file=sys.stderr)
            return 1
        result["before"] = profile(read_sentences(old))
        result["moves"] = compare(result["before"], result["profile"])
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    p = result["profile"]
    if not p["sentences"]:
        print("no body sentence to profile")
        return 0
    if args.before:
        print(f'{"":40}{"before":>9}{"after":>9}')
        for row in result["moves"]:
            print(f'{row["label"]:40}{row["before"]:>9}{row["after"]:>9}{"  flatter" if row["flatter"] else ""}')
        print(f'{"sentences with a parenthesis %":40}{result["before"].get("paren_pct", 0):>9}{p["paren_pct"]:>9}')
        b, a = result["before"].get("ending_pct", {}), p["ending_pct"]
        for c in a:
            print(f'{"  " + c + " %":40}{b.get(c, 0):>9}{a[c]:>9}')
        marked = sum(row["flatter"] for row in result["moves"])
        print(f"{marked} of {len(MOVES)} figures moved flatter")
    else:
        for key, label, _, _ in MOVES:
            print(f"{label:40}{p[key]:>9}")
        print(f'{"sentences with a parenthesis %":40}{p["paren_pct"]:>9}')
        for c, v in p["ending_pct"].items():
            print(f'{"  " + c + " %":40}{v:>9}')
    if p["flat"]:
        print(f'flat: {p["lone_pct"]} % of the sentences are lone and a sentence holds {p["joints_per_sentence"]} joints '
              f"(the line is {FLAT_LONE_PCT:g} % and {FLAT_JOINTS:g})")
    for f in result["runs"]:
        what = f'{f["count"]} sentences end in 「{f["form"]}」' if f["check"] == "ending_run" else f'{f["count"]} lone sentences'
        print(f'L{f["line"]}-L{f["to_line"]} [{f["check"]}] {what}: {f["excerpt"]}')
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
