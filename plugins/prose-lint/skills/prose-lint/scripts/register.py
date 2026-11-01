# /// script
# requires-python = ">=3.9"
# dependencies = ["regex>=2023.0"]
# ///
"""register.py - match a file against a register of rejected wordings.

The register is a CSV, or a Markdown table, whose columns are Pattern, Instead
and Why. Pattern is a regex in the syntax of the `regex` module; the block-name
form \\p{IsX} is also accepted and read as \\p{InX}. In the Markdown form a pipe
inside a pattern is written \\| so it does not split the table; the CSV takes
it as it is.

In the Markdown form, the latest `## ` heading above a row names its group,
and each hit carries it: `[Rewrite]` or `[Read in context]`, for example.

A CSV headed Pattern,Instead,Except holds plain words: Pattern lists words
split by 、, each matched literally and without regard to case; a word that
starts or ends with a Latin letter matches as a whole word. Except may open
with the flags chat (the hooks leave the row out of replies) and quote (a hit
inside 「」, “” or "" or on a > line is dropped), each followed by a space; the
rest is shown with each hit as the exception. A CSV saved in the Windows-31J code page also reads.

Fenced code blocks are skipped. Consecutive lines of a paragraph are joined
before matching, because hard-wrapped Japanese puts a line break inside a word;
a space goes between two Latin characters, and a list item starts a new
paragraph. In an HTML file, a block element ends a unit, inline tags are
removed, entities decoded, and script, style, pre and comments skipped. The
plain-word rows also take a heading and a table cell as units of their own and
read through Markdown emphasis, links and full-width Latin letters. A row whose
pattern does not compile is reported on stderr.

Usage:
    uv run register.py [--register <vocabulary.md> | --academic | --translationese | --slop] [--json] <file>

The register is --register, else $PROSE_LINT_REGISTER, else
vocabulary.md in $PROSE_LINT_HOME or ~/.prose-lint, else assets/vocabulary.sample.md next to this script.
--academic reads the academic register instead: $PROSE_LINT_ACADEMIC_REGISTER, else
academic.md in the same home, else assets/academic.sample.md.
--translationese reads the register of English constructions carried into Japanese:
$PROSE_LINT_TRANSLATIONESE_REGISTER, else translationese.md in the same home, else
assets/translationese.sample.md.
--slop reads the register of stop-ai-slop-jp's phrase lists: $PROSE_LINT_SLOP_REGISTER, else
slop.md in the same home, else assets/slop.sample.md.
Exit code 0 on any number of hits; 1 on an input error.
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import os
import sys
from pathlib import Path

import regex

SEP = "\x1f"  # stands in for an escaped pipe while the row is split
ASSETS = Path(__file__).resolve().parent.parent / "assets"
# (environment variable, file in the home directory, sample in assets/)
REGISTERS = {
    "general": ("PROSE_LINT_REGISTER", "vocabulary.md", "vocabulary.sample.md"),
    "academic": ("PROSE_LINT_ACADEMIC_REGISTER", "academic.md", "academic.sample.md"),
    "translationese": ("PROSE_LINT_TRANSLATIONESE_REGISTER", "translationese.md", "translationese.sample.md"),
    "slop": ("PROSE_LINT_SLOP_REGISTER", "slop.md", "slop.sample.md"),
}


def default_register(kind: str = "general") -> Path:
    var, name, sample = REGISTERS[kind]
    env = os.environ.get(var)
    if env:
        return Path(env)
    home = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint") / name
    return home if home.is_file() else ASSETS / sample


def read_register(path: Path) -> str:
    """Return a register's text, decoded as UTF-8 or else Windows-31J.

    Excel's plain CSV save writes the ANSI code page, which is Windows-31J on Japanese Windows.
    """
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp932")


def ascii_width(text: str) -> str:
    """Turn full-width Latin letters, digits and symbols into ASCII, one character for one."""
    return regex.sub(r"[！-～]", lambda m: chr(ord(m.group()) - 0xFEE0), text)


def word_pattern(cell: str) -> str:
    """Return the regex of a plain-word cell: words split by 、, matched literally, any case.

    The words go through ascii_width, as the text they are matched against does.
    """
    alts = []
    for word in (ascii_width(w.strip()) for w in cell.split("、")):
        if not word:
            continue
        alt = regex.escape(word)
        if regex.match(r"[A-Za-z]", word[0]):
            alt = "(?<![A-Za-z])" + alt
        if regex.match(r"[A-Za-z]", word[-1]):
            alt += "(?![A-Za-z])"
        alts.append(alt)
    return "(?i:" + "|".join(alts) + ")" if alts else ""


def load_entries(text: str) -> list[dict]:
    text = text.lstrip("﻿")
    rows = []
    words = False  # a CSV headed Except holds plain words
    if text.startswith(("Pattern,", '"Pattern"')):  # the CSV form, told apart by its header line
        reader = csv.DictReader(io.StringIO(text))
        words = "Except" in (reader.fieldnames or [])
        for r in reader:
            rows.append(([(r.get(k) or "").strip() for k in ("Pattern", "Instead", "Except" if words else "Why")], ""))
    else:
        group = ""  # the latest `## ` heading names the group of the rows under it
        for line in text.splitlines():
            t = line.strip()
            if t.startswith("## "):
                group = t[3:].strip()
            if not t.startswith("|"):
                continue
            cells = [c.strip().replace(SEP, "|") for c in t.replace("\\|", SEP).strip("|").split("|")]
            if len(cells) >= 3:
                rows.append((cells, group))
    entries = []
    for cells, group in rows:
        if not cells[0] or cells[0] == "Pattern" or regex.fullmatch(r":?-{3,}:?", cells[0]):
            continue
        why, flags = cells[2], []
        if words:
            while m := regex.match(r"\s*(chat|quote)(?:\s+|$)", why):
                flags.append(m.group(1))
                why = why[m.end():]
            why = f"exception: {why.strip()}" if why.strip() else ""
        source = word_pattern(cells[0]) if words else regex.sub(r"\\([pP])\{Is", r"\\\1{In", cells[0])
        if not source:
            continue
        try:
            rx = regex.compile(source)
        except regex.error as exc:
            print(f"warning: row skipped, pattern does not compile ({exc}): {cells[0]}", file=sys.stderr)
            continue
        entries.append({"pattern": cells[0], "regex": rx, "instead": cells[1], "why": why, "group": group,
                        "flags": flags, "words": words})
    return entries


LIST_ITEM = regex.compile(r"\s*(?:[-*+]|\d+[.)])\s")
LATIN = regex.compile(r"[A-Za-z0-9,.;:]")


def paragraphs(content: str):
    """Yield (joined text, [(offset, line_no)]) per paragraph outside code fences."""
    buf, starts, fence = "", [], None
    for no, line in enumerate(content.splitlines() + [""], 1):
        marker = line.lstrip()[:3]
        is_fence = marker in ("```", "~~~") and (fence is None or marker == fence)
        if is_fence:
            fence = None if fence else marker
        if is_fence or fence or not line.strip() or LIST_ITEM.match(line):
            if buf:
                yield buf, starts
            buf, starts = "", []
            if is_fence or fence or not line.strip():
                continue
        if buf and LATIN.match(buf[-1]) and LATIN.match(line.lstrip()[:1] or " "):
            buf += " "
        starts.append((len(buf), no))
        buf += line.strip() if buf else line


BLOCK_TAGS = ("p|div|li|td|th|tr|h[1-6]|hr|section|article|header|footer|nav|aside|table|thead|tbody|tfoot|"
              "ul|ol|dl|dt|dd|blockquote|figure|figcaption|caption|title|main|details|summary")
SKIP_TAGS = "script|style|pre"
# Inline elements a Markdown file may carry; a < before any other word is text, as in a<b.
INLINE_TAGS = ("a|abbr|b|br|cite|code|del|em|i|img|ins|kbd|mark|q|rp|rt|ruby|s|small|span|strong|sub|sup|u|wbr|"
               + BLOCK_TAGS)
BREAK = "\x1e"  # marks the end of a unit inside one line
QUOTE = regex.compile('「[^」\n]*」|“[^”\n]*”|"[^"\n]*"')


def clean(line: str, normalize: bool, fmt: str = "md") -> str:
    """Remove tags from a line and turn block tags into unit breaks.

    With normalize, also remove Markdown emphasis and links, and apply ascii_width.
    """
    if "<" in line:
        line = regex.sub(r"(?is)<(rt|rp)\b[^>]*>.*?</\1\s*>", "", line)
        line = regex.sub(rf"(?i)</?(?:{BLOCK_TAGS})\b[^>]*>", BREAK, line)
        tag = r"</?[A-Za-z][^<>]*>" if fmt == "html" else rf"(?i)</?(?:{INLINE_TAGS})\b[^<>]*>"
        line = regex.sub(tag, "", line)
    if normalize:
        line = regex.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = regex.sub(r"\*\*|__|~~|`", "", line)
    if "&" in line:
        line = html.unescape(line)
    return ascii_width(line) if normalize else line


def units(content: str, fmt: str = "md", normalize: bool = False):
    """Return ([(joined text, [(offset, line_no)])], quoted line numbers), one entry per unit.

    Markdown: a paragraph, a heading, a table cell and a list item are units; fences are
    skipped. HTML: a block element is a unit; script, style, pre and comments are skipped.
    """
    out, buf, starts, quoted = [], "", [], set()
    fence, skip_until = None, None

    def flush():
        nonlocal buf, starts
        if buf:
            out.append((buf, starts))
        buf, starts = "", []

    for no, line in enumerate(content.splitlines(), 1):
        marker = line.lstrip()[:3]
        if marker in ("```", "~~~") and (fence is None or marker == fence):  # as paragraphs() does
            fence = None if fence else marker
            flush()
            continue
        if fence or not line.strip():
            flush()
            continue
        if fmt == "html":
            if skip_until:
                m = regex.search(skip_until, line)
                if not m:
                    continue
                line, skip_until = line[m.end():], None
                flush()
            line = regex.sub(rf"(?is)<({SKIP_TAGS})\b[^>]*>.*?</\1\s*>|<!--.*?-->", BREAK, line)
            m = regex.search(rf"(?i)<({SKIP_TAGS})\b|<!--", line)
            if m:
                skip_until = "-->" if m.group() == "<!--" else rf"(?i)</{m.group(1)}\s*>"
                line = line[:m.start()] + BREAK
            elif m := regex.search(r"<[A-Za-z/][^<>]*$", line):  # a tag whose attributes wrap
                skip_until = ">"
                line = line[:m.start()] + BREAK
        else:
            heading = regex.match(r"\s{0,3}#{1,6}(\s|$)", line)
            row = regex.match(r"\s*\|", line)
            if regex.match(r"\s*>", line):
                quoted.add(no)
            if heading or row or LIST_ITEM.match(line):
                flush()
            line = regex.sub(r"^\s*(>\s?)+", "", line)
            line = regex.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line)
            line = regex.sub(r"^\s{0,3}#{1,6}(\s+|$)", "", line)
            if row:  # one unit per cell
                line = line.replace("\\|", SEP).replace("|", BREAK).replace(SEP, "\\|")
            if heading or row:
                line += BREAK
        for k, seg in enumerate(clean(line, normalize, fmt).split(BREAK)):
            if k:
                flush()
            seg = seg.strip()
            if not seg:
                continue
            if buf and regex.match(r"[!-~]", buf[-1]) and regex.match(r"[!-~]", seg[0]):
                buf += " "  # an English hard wrap: the line break separated two words
            starts.append((len(buf), no))
            buf += seg
    flush()
    return out, quoted


def find_hits(content: str, entries: list[dict], fmt: str = "md") -> list[dict]:
    """Match the entries; fmt is "md" (Markdown and plain text) or "html"."""
    passes = []
    plain = [e for e in entries if not e.get("words")]
    if plain:  # the regex rows: full-width ！？０-９ in them stay as written
        passes.append((list(paragraphs(content)) if fmt == "md" else units(content, fmt)[0], plain, set()))
    words = [e for e in entries if e.get("words")]
    if words:
        found, quoted = units(content, fmt, normalize=True)
        passes.append((found, words, quoted))
    hits = []
    for found, es, quoted in passes:
        for text, starts in found:
            spans = [m.span() for m in QUOTE.finditer(text)]
            for e in es:
                for m in e["regex"].finditer(text):
                    line = next(no for off, no in reversed(starts) if off <= m.start())
                    if "quote" in e.get("flags", ()) and (
                            line in quoted or any(a < m.start() and m.end() < b for a, b in spans)):
                        continue
                    hits.append({"line": line, "matched": m.group(), "instead": e["instead"], "why": e["why"],
                                 "group": e["group"], "flags": e.get("flags", [])})
    return sorted(hits, key=lambda h: h["line"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--register", type=Path)
    group.add_argument("--academic", action="store_true", help="read the academic register")
    group.add_argument("--translationese", action="store_true", help="read the translationese register")
    group.add_argument("--slop", action="store_true", help="read the stop-ai-slop-jp register")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    kind = ("academic" if args.academic else "translationese" if args.translationese
            else "slop" if args.slop else "general")
    reg = args.register or default_register(kind)
    try:
        entries = load_entries(read_register(reg))
        content = Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    hits = find_hits(content, entries, "html" if Path(args.file).suffix.lower() in (".html", ".htm") else "md")
    if args.json:
        print(json.dumps({"file": args.file, "register": str(reg), "hits": hits}, ensure_ascii=False, indent=2))
    else:
        print(f"register: {reg} ({len(entries)} rows)")
        for h in hits:
            why = f' ({h["why"]})' if h["why"] else ""
            group = f' [{h["group"]}]' if h["group"] else ""
            print(f'L{h["line"]}{group} "{h["matched"]}" -> {h["instead"]}{why}')
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
