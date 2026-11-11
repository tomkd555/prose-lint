# /// script
# requires-python = ">=3.10"
# dependencies = ["sudachipy>=0.6.8", "sudachidict-core>=20240409"]
# ///
"""features.py - features of human prose that flow.py does not count yet.

    uv run features.py <skill scripts dir> <out.json> <file.md>...

Per body sentence, read with flow.py's own sentence reader:
    open       how the sentence opens: connective, demonstrative, topic (… は within the first clause),
               setting (a time, place or condition phrase before the first 読点: では, には, において, 年, と, ば, 場合),
               subject (… が), other
    topicless  no は and no が in the sentence: the subject is carried over
    mo         the particle も (係助詞) in the sentence
    adv        a stance adverb in the sentence (特に, むしろ, やはり, 必ずしも, 実際, 確かに, もちろん, 依然, …)
    concede    a concession inside the sentence (ものの, とはいえ, にもかかわらず, 一方で, ながら(も), つつも, とはいっても, 〜が、 contrast is left out)
    process    the ending places the fact in a course of events (てきた, こととした, こととなった, ところである, に至った, つつある, ていく, ようになった)
    assess     the ending is an assessment predicate (重要である, 必要である, 求められる, 期待される, 望ましい, 課題である, 懸念される, 不可欠)
    nums       sentence holds a numeral
    paren      sentence holds a parenthesis
    quote      sentence holds 「」
Per document: paragraph shape (sentences per prose paragraph, share of one-sentence paragraphs),
kanji share of the body characters, share of body characters in list items, headings per 1000 characters,
and how often consecutive sentences share their opening type or their first topic noun.
"""
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import flow  # noqa: E402
import koyobun  # noqa: E402
from sudachipy import SplitMode  # noqa: E402

ADV = ("特に", "とりわけ", "むしろ", "やはり", "必ずしも", "実際", "確かに", "もちろん", "無論", "依然", "いわば", "あくまで",
       "おそらく", "恐らく", "きっと", "少なくとも", "せめて", "まさに", "そもそも", "かえって", "なかなか", "いずれも", "あえて",
       "当然", "到底", "決して", "ようやく", "すでに", "既に", "まだ", "いまだ", "未だ", "今や", "もはや", "さすがに", "幸い", "残念ながら",
       "もとより", "とかく", "概して", "一概に", "一見", "本来", "元来", "実に", "極めて", "非常に", "大いに", "かなり", "やや", "ほぼ")
ADV_RE = re.compile("|".join(sorted(ADV, key=len, reverse=True)))
CONCEDE_RE = re.compile(r"ものの|とはいえ|にもかかわらず|にも関わらず|一方で|ながらも|つつも|とはいっても|とは言っても|としても|であっても|にせよ|とは限ら")
PROCESS_RE = re.compile(r"(?:てき(?:た|ました|ている|ています|たところである|たところです)|こととし(?:た|ました|ている|ています)"
                        r"|こととなっ(?:た|ている)|こととなりました|ところ(?:である|です|であった)|に至っ(?:た|ている)|に至りました"
                        r"|つつあ(?:る|ります)|てい(?:く|きます)|ようにな(?:った|りました|っている|っています)|てい(?:る|ます)ところ(?:である|です))$")
ASSESS_RE = re.compile(r"(?:重要|必要|不可欠|肝要|有効|有用|課題|急務|大切|適当|適切|妥当|困難|可能)(?:である|です|となる|となります|となっている|となっています|と考える|と考えます)$"
                       r"|(?:求め|期待さ|懸念さ|望ま|危惧さ|想定さ|見込ま)れ(?:る|ます|ている|ています)$|望ましい$|欠かせ(?:ない|ません)$")
SETTING_RE = re.compile(r"(?:では|には|においては?|における|にあっては|としては|について(?:は|も)?|に関しては?|に対しては?|により|によって|に伴い|を踏まえ|を受け|の中、?|中で|際に?は?|場合(?:に|は|には)?|ときは?|時は?|年(?:度)?(?:[0-9０-９]+月)?(?:[0-9０-９]+日)?(?:に|には|から|以降|現在)?|月(?:に|には|から)?|現在|当時|近年|今後|従来|これまで|今回|今年|昨年|本年|先般|[るたいく]と|れば|なら|たら)$")


def body_stats(text: str) -> dict:
    rows = text.split("\n")
    fence = False
    prose = lists = heads = 0
    for r in rows:
        if koyobun.FENCE_RE.match(r):
            fence = not fence
            continue
        if fence or not r.strip() or r.startswith("<!--"):
            continue
        n = len(re.sub(r"\s", "", r))
        if r.lstrip().startswith("#"):
            heads += 1
        elif re.match(r"\s*(?:[-*+]|\d+[.)])\s", r):
            lists += n
        elif r.lstrip().startswith(("|", ">")):
            continue
        else:
            prose += n
    body = re.sub(r"\s", "", "".join(r for r in rows if not r.lstrip().startswith("#")))
    kanji = len(re.findall(r"[一-鿿々]", body))
    jp = len(re.findall(r"[一-鿿々ぁ-ゖァ-ヺー]", body))
    return {"prose_chars": prose, "list_chars": lists, "list_pct": round(100 * lists / max(prose + lists, 1), 1),
            "headings_per_1000": round(1000 * heads / max(prose + lists, 1), 2), "kanji_pct": round(100 * kanji / max(jp, 1), 1)}


def opening(sent: str, ms: list, s: dict) -> tuple[str, str]:
    """Return (type, first topic noun)."""
    if s["connective"]:
        kind = "connective"
    elif flow.DEMO_OPEN_RE.match(sent.lstrip("「『（(　 ")):
        kind = "demonstrative"
    else:
        kind = None
    # the first clause: up to the first 読点, or the first 12 morphemes
    head, topic = [], ""
    for m in ms:
        if m.part_of_speech()[1] == "読点" or len(head) >= 14:
            break
        head.append(m)
    surf = "".join(m.surface() for m in head)
    for i, m in enumerate(head):
        pos = m.part_of_speech()
        if pos[0] == "助詞" and pos[1] == "係助詞" and m.surface() == "は" and i > 0:
            nouns = [x.surface() for x in head[:i] if x.part_of_speech()[0] in {"名詞", "代名詞", "接尾辞", "接頭辞"}]
            topic = "".join(nouns[-3:])
            # では、には、については: a setting, not the topic itself
            prev = head[i - 1]
            if prev.part_of_speech()[0] == "助詞":
                return kind or "setting", ""
            return kind or "topic", topic
    if kind:
        return kind, ""
    if SETTING_RE.search(surf):
        return "setting", ""
    for i, m in enumerate(head):
        pos = m.part_of_speech()
        if pos[0] == "助詞" and pos[1] == "格助詞" and m.surface() == "が" and i > 0:
            return "subject", ""
    return "other", ""


def main() -> int:
    out = Path(sys.argv[2])
    res = {}
    tok = koyobun.get_tokenizer()
    for f in sys.argv[3:]:
        text, err = koyobun.read_source_file(Path(f))
        if err:
            print(err, file=sys.stderr)
            continue
        sents = flow.read_sentences(text)
        n = len(sents)
        if not n:
            continue
        rows = []
        for s in sents:
            sent = s["text"]
            ms = [m for m in tok.tokenize(sent, SplitMode.C)]
            kind, topic = opening(sent, ms, s)
            core = re.sub(r"[。．.！!？?、，\s]+$", "", koyobun.TAIL_NOTE_RE.sub("", sent.strip()).strip())
            has_wa = any(m.surface() == "は" and m.part_of_speech()[1] == "係助詞" for m in ms)
            has_ga = any(m.surface() == "が" and m.part_of_speech()[1] == "格助詞" for m in ms)
            rows.append({
                "open": kind, "topic": topic, "topicless": not (has_wa or has_ga), "no_wa": not has_wa,
                "mo": any(m.surface() == "も" and m.part_of_speech()[1] == "係助詞" for m in ms),
                "adv": bool(ADV_RE.search(sent)), "concede": bool(CONCEDE_RE.search(sent)),
                "process": bool(PROCESS_RE.search(core)), "assess": bool(ASSESS_RE.search(core)),
                "nums": bool(re.search(r"[0-9０-９]", sent)), "paren": bool(re.search(r"[（(]", sent)),
                "quote": "「" in sent, "para": s["para"], "ending": s["ending"], "form": s["form"], "chars": s["chars"],
                "joints": s["joints"], "lone": s["lone"],
            })
        pct = lambda k: round(100 * sum(1 for r in rows if r[k]) / n, 1)
        opens = Counter(r["open"] for r in rows)
        paras = Counter(r["para"] for r in rows)
        sizes = list(paras.values())
        same_open = same_topic = pairs = 0
        run, longest_open = 1, 1
        for a, b in zip(rows, rows[1:]):
            if a["para"] != b["para"]:
                run = 1
                continue
            pairs += 1
            if a["open"] == b["open"] and a["open"] in ("topic", "subject", "other"):
                same_open += 1
            if a["topic"] and a["topic"] == b["topic"]:
                same_topic += 1
            run = run + 1 if a["open"] == b["open"] == "topic" else 1
            longest_open = max(longest_open, run)
        # the spread of ending classes inside paragraphs of 3 sentences or more
        mixes = []
        for p, size in paras.items():
            if size >= 3:
                mixes.append(len({r["ending"] for r in rows if r["para"] == p}))
        res[Path(f).stem] = {
            "sentences": n,
            "open_pct": {k: round(100 * v / n, 1) for k, v in opens.items()},
            "topicless_pct": pct("topicless"), "no_wa_pct": pct("no_wa"), "mo_pct": pct("mo"), "adv_pct": pct("adv"),
            "concede_pct": pct("concede"), "process_pct": pct("process"), "assess_pct": pct("assess"),
            "nums_pct": pct("nums"), "paren_pct": pct("paren"), "quote_pct": pct("quote"),
            "paragraphs": len(sizes), "sent_per_para": round(statistics.fmean(sizes), 2),
            "para_size_cv": round(statistics.pstdev(sizes) / statistics.fmean(sizes), 2),
            "one_sentence_para_pct": round(100 * sum(1 for x in sizes if x == 1) / len(sizes), 1),
            "same_topic_pair_pct": round(100 * same_topic / max(pairs, 1), 1),
            "same_open_pair_pct": round(100 * same_open / max(pairs, 1), 1),
            "longest_topic_open_run": longest_open,
            "ending_classes_per_para3": round(statistics.fmean(mixes), 2) if mixes else None,
            "forms": Counter(r["form"] for r in rows).most_common(8),
            **body_stats(text),
        }
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
