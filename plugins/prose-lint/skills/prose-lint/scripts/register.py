# /// script
# requires-python = ">=3.9"
# dependencies = ["regex>=2023.0"]
# ///
"""register.py - match a file against a register of rejected wordings.

The register is a Markdown table whose columns are Pattern, Instead and Why.
Pattern is a regex in the syntax of the `regex` module; the block-name form
\\p{IsX} is also accepted and read as \\p{InX}. A pipe inside a pattern is
written \\| so it does not split the table.

Fenced code blocks are skipped. Consecutive lines of a paragraph are joined
before matching, because hard-wrapped Japanese puts a line break inside a word;
a space goes between two Latin characters, and a list item starts a new
paragraph. A row whose pattern does not compile is reported on stderr.

Usage:
    uv run register.py [--register <vocabulary.md>] [--json] <file>

The register is --register, else $PROSE_LINT_REGISTER, else
vocabulary.md in $PROSE_LINT_HOME or ~/.prose-lint, else assets/vocabulary.sample.md next to this script.
Exit code 0 on any number of hits; 1 on an input error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import regex

SEP = "\x1f"  # stands in for an escaped pipe while the row is split
SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "vocabulary.sample.md"


def default_register() -> Path:
    env = os.environ.get("PROSE_LINT_REGISTER")
    if env:
        return Path(env)
    home = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint") / "vocabulary.md"
    return home if home.is_file() else SAMPLE


def load_entries(text: str) -> list[dict]:
    entries = []
    for line in text.splitlines():
        t = line.strip()
        if not t.startswith("|"):
            continue
        cells = [c.strip().replace(SEP, "|") for c in t.replace("\\|", SEP).strip("|").split("|")]
        if len(cells) < 3 or not cells[0] or cells[0] == "Pattern" or regex.fullmatch(r":?-{3,}:?", cells[0]):
            continue
        try:
            rx = regex.compile(regex.sub(r"\\([pP])\{Is", r"\\\1{In", cells[0]))
        except regex.error as exc:
            print(f"warning: row skipped, pattern does not compile ({exc}): {cells[0]}", file=sys.stderr)
            continue
        entries.append({"pattern": cells[0], "regex": rx, "instead": cells[1], "why": cells[2]})
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


def find_hits(content: str, entries: list[dict]) -> list[dict]:
    hits = []
    for text, starts in paragraphs(content):
        for e in entries:
            for m in e["regex"].finditer(text):
                line = next(no for off, no in reversed(starts) if off <= m.start())
                hits.append({"line": line, "matched": m.group(), "instead": e["instead"], "why": e["why"]})
    return sorted(hits, key=lambda h: h["line"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--register", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    reg = args.register or default_register()
    try:
        entries = load_entries(reg.read_text(encoding="utf-8"))
        content = Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    hits = find_hits(content, entries)
    if args.json:
        print(json.dumps({"file": args.file, "register": str(reg), "hits": hits}, ensure_ascii=False, indent=2))
    else:
        print(f"register: {reg} ({len(entries)} rows)")
        for h in hits:
            print(f'L{h["line"]} "{h["matched"]}" -> {h["instead"]} ({h["why"]})')
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 or cp1252 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
