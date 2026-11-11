# /// script
# requires-python = ">=3.10"
# dependencies = ["sudachipy>=0.6.8", "sudachidict-core>=20240409"]
# ///
"""words.py - word choice in the body sentences of Japanese documents.

    uv run words.py <skill scripts dir> <out.json> <file.md>...

Per document, over the body sentences flow.py reads, per 1,000 characters:
    katakana     katakana words of 2 characters or more (tokens), and the distinct words
    lone_kanji   a noun written as one kanji standing as a word of its own: not joined to another
                 noun, a prefix or a suffix (語, 値, 軸, 核, 鍵, 柱). Counters, units and the
                 common formal nouns (点, 際, 旨, 上, 中, 後, 前, 間, 時, 方, 人, 日, 年, 月) are left out
    frames       surface frames the translationese reference names:
                 可能にする, ことができる, を提供する, を持つ, を行う, において, に関する, のための,
                 これら/それら, 彼/彼女/彼ら, によって/により + れる
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import flow  # noqa: E402
import koyobun  # noqa: E402
from sudachipy import SplitMode  # noqa: E402

SKIP_KANJI = set("点際旨上中下後前間時方人日年月度分秒円件個名本社者等他外内各全同当本約第計次両元新旧数回毎")
FRAMES = {
    "可能にする": r"を可能に(?:する|し|します|した|している)",
    "ことができる": r"ことが(?:でき|可能)",
    "を提供する": r"を提供(?:する|し|します|した|している|いたします)",
    "を持つ": r"を(?:持つ|持って|持ち|有する|有して|有し)",
    "を行う": r"を(?:行う|行い|行って|行います|行った|行いました|実施する|実施し)",
    "において": r"に(?:おいて|おける|おきまして)",
    "に関する": r"に関(?:する|して|し)",
    "のための": r"のための",
    "これら/それら": r"(?:これら|それら)",
    "彼/彼女/彼ら": r"(?:彼ら|彼女|(?<![一-鿿])彼(?![一-鿿岸方]))",
    "によって/により": r"に(?:よって|より)(?![、,]?(?:も|いっそう|一層|良|よ[いく]|高|多|少|大|小|強|広|早|速|詳))",
    "することで": r"することで",
    "ための": r"ための",
}
FRAMES = {k: re.compile(v) for k, v in FRAMES.items()}
KATA = re.compile(r"[ァ-ヴー]{2,}")


def main() -> int:
    out = Path(sys.argv[2])
    tok = koyobun.get_tokenizer()
    res = {}
    for f in sys.argv[3:]:
        text, err = koyobun.read_source_file(Path(f))
        if err:
            continue
        sents = flow.read_sentences(text)
        chars = sum(s["chars"] for s in sents)
        if not chars:
            continue
        kata, lone, frames = Counter(), Counter(), Counter()
        for s in sents:
            t = s["text"]
            ms = [m for m in tok.tokenize(t, SplitMode.C)]
            for w in KATA.findall(t):
                kata[w] += 1
            for i, m in enumerate(ms):
                surf, pos = m.surface(), m.part_of_speech()
                if len(surf) == 1 and re.fullmatch(r"[一-鿿]", surf) and pos[0] == "名詞" and pos[1] == "普通名詞" and surf not in SKIP_KANJI:
                    prev, nxt = (ms[i - 1] if i else None), (ms[i + 1] if i + 1 < len(ms) else None)
                    joined = lambda x: x is not None and x.part_of_speech()[0] in {"名詞", "接頭辞", "接尾辞"} or (
                        x is not None and re.fullmatch(r"[0-9０-９一二三四五六七八九十百千万]+", x.surface()))
                    if not joined(prev) and not joined(nxt):
                        lone[surf] += 1
            for k, rx in FRAMES.items():
                frames[k] += len(rx.findall(t))
        per = lambda n: round(1000 * n / chars, 2)
        res[Path(f).stem] = {
            "chars": chars, "sentences": len(sents),
            "katakana_per_1000": per(sum(kata.values())), "katakana_distinct": len(kata),
            "katakana_top": kata.most_common(25),
            "lone_kanji_per_1000": per(sum(lone.values())), "lone_kanji_top": lone.most_common(25),
            "frames_per_1000": {k: per(v) for k, v in frames.items()},
            "frames": dict(frames),
        }
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
