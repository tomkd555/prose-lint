# /// script
# requires-python = ">=3.10"
# ///
"""pair_check.py - compare a translation with its source, section by section.

    uv run pair_check.py <source> <target> [--glossary <terms.tsv>]

Prints one JSON object per line with the keys kind, section, line and message. Every line is a
suspicion for the reader of the pair to rule on. The kinds:

    number    a number, or a percentage, that the other side lacks in that section
    glossary  a source term whose target term is missing from that section
    leftover  source-language text left in the target: a quoted phrase of two or more words in
              a Japanese target, or kana and kanji in an English target
    heading   a heading of the target still in the source language

The direction comes from the target's hiragana, as Step 2 of the skill routes a document. Sections are the `## ` blocks, matched by
order; when the two sides hold different numbers of sections, the documents are compared whole.
The glossary is a TSV of source term and target term, and a run without one skips that kind.
Fenced code, inline code, URLs and citation markers such as [E12] stay out of every comparison.
Full-width digits count as digits. A number spelled in words or in kanji numerals (第一条, 令和七年)
goes unread, and so does a compound such as 3 億 5000 万: its form in the other language shows as a
difference to rule on, and so does a year in 令和 against its Western year.

Exit code 0 on any number of findings; 1 on an input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)
SKIP = re.compile(r"`[^`\n]*`|https?://\S+|\[E\d+(?:,\s*E\d+)*\]")
NUMBER = re.compile(r"(?<![\dA-Za-z.,])(\d[\d,]*(?:\.\d+)?)[ \t]*(万|億|million\b|billion\b|thousand\b)?[ \t]*(%|％|パーセント|percent\b)?", re.IGNORECASE)
SCALE = {"万": 10_000, "億": 100_000_000, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000}
FULL_WIDTH = str.maketrans("０１２３４５６７８９，．", "0123456789,.")
HIRAGANA = re.compile(r"[ぁ-ゟ]")
KANA_KANJI = re.compile(r"[ぁ-ヿ㐀-鿿]")
HEADING = re.compile(r"^(#{1,6}) +(.+)$", re.MULTILINE)
SLIDE_TITLE = re.compile(r"Slide \d+$")  # the section title pptx_text.py writes
QUOTED = re.compile(r'"[^"\n]*[A-Za-z]{2,} [A-Za-z]{2,}[^"\n]*"|「[^」\n]*[A-Za-z]{2,} [A-Za-z]{2,}[^」\n]*」')


def plain(text: str) -> str:
    """Blank fenced code, inline code, URLs and citations, keeping line breaks."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group())
    return SKIP.sub(blank, FENCE.sub(blank, text))


def sections(text: str) -> list[tuple[str, int, str]]:
    """Split text at `## ` headings into (heading, first line, body)."""
    out = [["", 1, []]]
    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            out.append([line[3:].strip(), no, []])
        else:
            out[-1][2].append(line)
    return [(h, n, "\n".join(body)) for h, n, body in out if h or any(s.strip() for s in body)]


def numbers(text: str) -> Counter:
    """Return the numbers in text as a Counter of (value, is_percent)."""
    found = Counter()
    for m in NUMBER.finditer(text.translate(FULL_WIDTH)):
        value = float(m.group(1).replace(",", "")) * SCALE.get((m.group(2) or "").lower(), 1)
        found[(round(value, 6), bool(m.group(3)))] += 1
    return found


def has_term(term: str, text: str) -> bool:
    """True when text holds term, in any case, with a Latin term as a whole word."""
    head = "(?<![A-Za-z])" if term[:1].isascii() and term[:1].isalpha() else ""
    tail = "(?![A-Za-z])" if term[-1:].isascii() and term[-1:].isalpha() else ""
    return re.search(head + re.escape(term) + tail, text, re.IGNORECASE) is not None


def compare_section(source: tuple, target: tuple, glossary, to_ja: bool) -> list[dict]:
    """Compare one (heading, line, body) section of each side."""
    head, line, tgt = target
    add = lambda kind, message: {"kind": kind, "section": head, "line": line, "message": message}
    whole_src, whole_tgt = f"{source[0]}\n{source[2]}", f"{head}\n{tgt}"
    a, b = numbers(whole_src), numbers(whole_tgt)
    label = lambda n: format(n[0], "f").rstrip("0").rstrip(".") + ("%" if n[1] else "")
    found = [add("number", f"{label(n)} is in the source only") for n in (a - b)]
    found += [add("number", f"{label(n)} is in the target only") for n in (b - a)]
    found += [add("glossary", f"{s} is in the source and {t} is not in the target")
              for s, t in glossary if has_term(s, whole_src) and not has_term(t, whole_tgt)]
    if to_ja:
        found += [add("leftover", m.group()) for m in QUOTED.finditer(tgt)]
    else:
        found += [add("leftover", m.group()) for m in KANA_KANJI.finditer(tgt)][:1]
    return found


def compare(source: str, target: str, glossary: list[tuple[str, str]]) -> list[dict]:
    src, tgt = plain(source), plain(target)
    to_ja = len(HIRAGANA.findall(tgt)) * 10 > len("".join(tgt.split()))
    pairs_s, pairs_t = sections(src), sections(tgt)
    if len(pairs_s) != len(pairs_t):
        pairs_s, pairs_t = [("", 1, src)], [("", 1, tgt)]
    found = []
    for pair in zip(pairs_s, pairs_t):
        found += compare_section(*pair, glossary, to_ja)
    for m in HEADING.finditer(tgt):
        head = m.group(2).strip()
        if to_ja != bool(KANA_KANJI.search(head)) and re.search("[A-Za-zぁ-ヿ㐀-鿿]", head) and not SLIDE_TITLE.match(head):
            line = tgt.count("\n", 0, m.start()) + 1
            found.append({"kind": "heading", "section": head, "line": line, "message": head})
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--glossary", type=Path)
    args = ap.parse_args()
    try:
        source = args.source.read_text(encoding="utf-8")
        target = args.target.read_text(encoding="utf-8")
        rows = args.glossary.read_text(encoding="utf-8-sig").splitlines() if args.glossary else []
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    glossary = [tuple(r.split("\t")[:2]) for r in rows if r.count("\t") >= 1]
    for finding in compare(source, target, glossary):
        print(json.dumps(finding, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
