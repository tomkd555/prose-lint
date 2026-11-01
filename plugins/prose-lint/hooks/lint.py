# /// script
# requires-python = ">=3.9"
# dependencies = ["regex>=2023.0"]
# ///
"""lint.py - the plugin's wording-check hooks.

    uv run --script lint.py file|reply|inject|plan < hook-input.json

file (PostToolUse on Write and Edit) lints a Markdown, text or HTML file Claude
wrote with textlint and the register, plus vale for English, and reports the
lines the tool changed (the whole file for a new one). A source file (.py, .ps1,
.js, .ts, .json, .yml, .yaml) runs the register alone and reports the hits that
hold Japanese, which sits in its comments and strings. A textlint finding of the
blocking tier or a register hit returns decision=block; advisory and vale
findings alone go to Claude as additionalContext and leave the write in place.
A counter per file stops reporting a set of findings after it has blocked 3
times in a row. A file in a folder named claude-reply is a reply draft: the
register rows flagged chat stay out, as they do for replies.

reply (Stop) lints a Japanese reply, keeps the findings in a file under
$CLAUDE_PLUGIN_DATA and appends them to a log, one line each, in
$PROSE_LINT_REPLY_LOG_DIR (default $PROSE_LINT_HOME/logs/replies), for a tool
that grows the register from replies; inject (UserPromptSubmit) prints them, so
Claude applies them from the next reply on, and deletes the file.

plan (PreToolUse on ExitPlanMode and AskUserQuestion) denies a plan that holds
points still open or unconfirmed, or a plan or question with a textlint finding
of the blocking tier; after 2 denials in a row the call goes through.

The tiers are SKILL.md's, "Step 3a - Japanese / textlint" and "Step 3b". Every
failure exits 0: a broken lint must not stop a write or a reply.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "prose-lint" / "scripts"))
import register

HOME = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint")
PROSE = {".md", ".markdown", ".txt", ".html", ".htm"}
CODE = {".py", ".ps1", ".js", ".ts", ".json", ".yml", ".yaml"}
SKIP_PARTS = {"node_modules", ".git", "__pycache__", "scratchpad"}
JAPANESE = re.compile(r"[぀-ヿ㐀-鿿]")
MAX_BLOCKS = 3
MAX_GATE = 2  # denials in a row before the plan gate lets a call through
MAX_SHOWN = 20
# Points a plan has not settled, which Claude settles by investigating.
OPEN_MARKS = (
    r"\bTBD\b", r"\bTBC\b", r"\bTODO\b", r"\?\?\?", r"open questions?", r"to be (decided|determined|confirmed)",
    r"decide later", r"we (need to|should) decide", r"which approach", r"\bunclear\b", r"not sure",
    "未定", "検討中", "後で決める", "どちらか", "いずれか")
# Points only the user can settle, through AskUserQuestion.
CONFIRM_MARKS = (
    r"needs? confirmation", r"\bunconfirmed\b", r"confirm with the user", r"ask the user",
    r"if the user (prefers|wants)", r"user decides", r"\bpending\b", "要確認", "未確認", "不明", "ユーザーに確認")
OPEN = re.compile("|".join(OPEN_MARKS), re.IGNORECASE)
CONFIRM = re.compile("|".join(CONFIRM_MARKS), re.IGNORECASE)

# The last segment of a textlint rule id, so preset prefixes do not matter.
JA_BLOCKING = {
    "ja-no-weak-phrase", "ja-no-redundant-expression", "ja-no-abusage", "ja-no-successive-word",
    "no-doubled-conjunctive-particle-ga", "no-double-negative-ja", "no-dropping-the-ra",
    "no-dropping-i", "no-insert-dropping-sa", "no-filler", "no-mix-dearu-desumasu",
    "prefer-tari-tari", "ja-keishikimeishi", "ja-hiragana-hojodoushi", "ja-hiragana-daimeishi",
    "ja-hiragana-fukushi", "prh",
}
JA_ADVISORY = {
    "no-doubled-joshi", "no-doubled-conjunction", "sentence-length", "max-ten",
    "max-kanji-continuous-len", "no-ai-hype-expressions", "ai-tech-writing-guideline",
    "no-ai-words", "no-synonyms",
}
# A line ending in one of these ends its sentence, so the next line starts a new one.
SENTENCE_END = ("。", "．", ".", "!", "?", "！", "？", ">", "|")
STALE = 86400  # seconds after which a block counter or a reply file is left over from an ended session


def lang_of(text: str) -> str:
    """Return 'ja' when hiragana make up more than 10 % of the non-space characters."""
    body = "".join(text.split())
    hiragana = sum(1 for c in body if "぀" <= c <= "ゟ")
    return "ja" if hiragana * 10 > len(body) else "en"


def tiers(messages: list[dict], lang: str):
    """Split textlint messages into (blocking, advisory, notation count)."""
    if lang == "en":  # Step 3b: every English textlint finding is fixed when it holds
        return list(messages), [], 0
    rule = lambda m: str(m.get("ruleId", "")).rsplit("/", 1)[-1]
    blocking = [m for m in messages if rule(m) in JA_BLOCKING]
    advisory = [m for m in messages if rule(m) in JA_ADVISORY]
    return blocking, advisory, len(messages) - len(blocking) - len(advisory)


def continues(prev: str, line: str) -> bool:
    """True when `line` carries on a sentence that `prev` started."""
    return bool(prev.strip()) and not prev.rstrip().endswith(SENTENCE_END) and not (
        register.LIST_ITEM.match(line) or line.lstrip().startswith(("#", "|", "<")))


def changed_lines(patch: list[dict], text: str) -> set[int]:
    """Return the lines a structuredPatch added, from the line their sentence starts on.

    textlint and the register report a sentence at its first line, which can sit above the
    added line when the paragraph is hard-wrapped.
    """
    added = set()
    for hunk in patch:
        n = hunk["newStart"]
        for line in hunk["lines"]:
            if line.startswith("+"):
                added.add(n)
            if line[:1] in (" ", "+"):
                n += 1
    rows = text.split("\n")
    lines = set()
    for n in added:
        start = n
        while start > 1 and continues(rows[start - 2], rows[start - 1]):
            start -= 1
        lines.update(range(start, n + 1))
    return lines


def run_json(args: list[str]):
    try:
        out = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=120, check=False).stdout
        return json.loads(out) if out.strip() else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def textlint(path: Path, lang: str) -> list[dict]:
    js = HOME / "textlint" / "node_modules" / "textlint" / "bin" / "textlint.js"
    conf = HOME / "textlint" / (".textlintrc.json" if lang == "ja" else ".textlintrc.en.json")
    node = shutil.which("node")
    if not (node and js.is_file() and conf.is_file()):
        return []
    # textlint exits 1 when it finds anything, so the exit code says nothing here.
    result = run_json([node, str(js), "--config", str(conf), "-f", "json", str(path)])
    try:
        return [m for f in result or [] for m in f["messages"]]
    except (KeyError, TypeError):
        return []


def vale(path: Path) -> list[dict]:
    exe = shutil.which("vale")
    conf = HOME / "vale" / ".vale.ini"
    if not (exe and conf.is_file()):
        return []
    result = run_json([exe, "--config", str(conf), "--output=JSON", str(path)])
    try:
        return [{"line": a["Line"], "ruleId": a["Check"], "message": a["Message"]}
                for alerts in (result or {}).values() for a in alerts]
    except (KeyError, TypeError, AttributeError):
        return []


def register_hits(text: str, fmt: str = "md", chat: bool = False) -> list[dict]:
    """Match the register; chat leaves out the rows flagged chat, as for a reply."""
    try:
        entries = register.load_entries(register.read_register(register.default_register()))
    except (OSError, UnicodeDecodeError):
        return []
    return register.find_hits(text, [e for e in entries if not (chat and "chat" in e["flags"])], fmt)


def prose_lang(text: str) -> str:
    """Return lang_of the running text: code fences hold no hiragana."""
    return lang_of(" ".join(t for t, _ in register.paragraphs(text)))


def textlint_text(text: str, path=None):
    """Return tiers() of textlint on text, read from path when that file holds the text."""
    lang = prose_lang(text)
    if path and Path(path).is_file():
        return tiers(textlint(Path(path), lang), lang)
    # textlint reads files, so the text goes to a temp file for the call.
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="prose-lint-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        return tiers(textlint(Path(tmp), lang), lang)
    finally:
        os.unlink(tmp)


def textlint_lines(messages: list[dict], suffix: str = "") -> list[str]:
    out = [f'L{m.get("line")} [{m.get("ruleId")}] {(str(m.get("message") or "").splitlines() or [""])[0]}{suffix}'
           for m in messages[:MAX_SHOWN]]
    if len(messages) > MAX_SHOWN:
        out.append(f"... and {len(messages) - MAX_SHOWN} more.")
    return out


def hit_lines(hits: list[dict]) -> list[str]:
    """One line per register row: the lines it matched, the words, the replacement."""
    rows: dict[tuple, list[dict]] = {}
    for h in hits:
        rows.setdefault((h["instead"], h["why"]), []).append(h)
    out = []
    for (instead, why), group in list(rows.items())[:MAX_SHOWN]:
        at = ", ".join(dict.fromkeys(f'L{h["line"]}' for h in group))
        words = ", ".join(dict.fromkeys(f'"{h["matched"]}"' for h in group))
        out.append(f"{at} {words} -> {instead}" + (f" ({why})" if why else ""))
    if len(rows) > MAX_SHOWN:
        out.append(f"... and {len(rows) - MAX_SHOWN} more rows.")
    return out


def session_id(data: dict) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("session_id") or "")) or "nosid"


def state_dir():
    """Return $CLAUDE_PLUGIN_DATA, which Claude Code gives every hook, after removing stale files."""
    if not os.environ.get("CLAUDE_PLUGIN_DATA"):
        return None
    base = Path(os.environ["CLAUDE_PLUGIN_DATA"])
    base.mkdir(parents=True, exist_ok=True)
    now = time.time()
    for f in [*base.glob("block-*"), *base.glob("gate-*"), *base.glob("reply-*.txt")]:
        try:
            if now - f.stat().st_mtime > STALE:
                f.unlink()
        except OSError:
            pass
    return base


def inside(path: Path, base: Path) -> bool:
    try:
        return path.resolve().is_relative_to(base.resolve())
    except (OSError, ValueError):
        return False


def holds_rows(path: Path) -> bool:
    """True for a register, or a file of the skill or of these hooks.

    They hold the rejected wordings as register rows and as test inputs.
    """
    parts = [p.lower() for p in path.parts]
    if any(parts[i:i + 2] in (["skills", "prose-lint"], ["prose-lint", "hooks"]) for i in range(len(parts) - 1)):
        return True
    return inside(path, HOME) or any(path.resolve() == register.default_register(kind).resolve()
                                     for kind in register.REGISTERS)


def lint_file(data: dict) -> int:
    path = Path(str((data.get("tool_input") or {}).get("file_path") or ""))
    suffix, parts = path.suffix.lower(), {p.lower() for p in path.parts}
    if suffix not in PROSE | CODE or parts & SKIP_PARTS or holds_rows(path):
        return 0
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    if not content.strip():
        return 0
    response = data.get("tool_response") or {}
    lines = None  # a new file, or a Claude Code that sends no patch: report the whole file
    if response.get("type") != "create" and "structuredPatch" in response:
        lines = changed_lines(response["structuredPatch"], content.replace("\r\n", "\n"))
        if not lines:
            return 0  # a deletion, or a rewrite with the same text, adds nothing to read

    fmt = "html" if suffix in (".html", ".htm") else "md"
    hits = register_hits(content, fmt, chat="claude-reply" in parts)
    if suffix in CODE:  # identifiers are ASCII: the register's Japanese hits fall in comments and strings
        hits = [h for h in hits if JAPANESE.search(h["matched"])]
        blocking, advisory, notation = [], [], 0
    else:
        # Routed on the running text: markup, styles and code fences hold no hiragana.
        lang = prose_lang(content) if fmt == "md" else lang_of(" ".join(t for t, _ in register.units(content, fmt)[0]))
        blocking, advisory, notation = tiers(textlint(path, lang), lang)
        if lang == "en":
            advisory += vale(path)
    if lines is not None:
        blocking, advisory, hits = ([f for f in found if f.get("line") in lines] for found in (blocking, advisory, hits))
        notation = 0

    has_block = bool(blocking or hits)
    key = hashlib.sha256(str(path).lower().encode("utf-8")).hexdigest()[:32]
    counter = (state_dir() or Path(tempfile.gettempdir())) / f"block-{session_id(data)}-{key}"
    if not has_block:
        counter.unlink(missing_ok=True)
        if not advisory:
            return 0
    else:
        # The loop guard counts blocks on the same findings: a new finding is reported afresh.
        found = sorted(f'{m.get("ruleId")}|{m.get("message")}' for m in blocking) + sorted(
            f'{h["matched"]}|{h["instead"]}' for h in hits)
        sig = hashlib.sha256("\n".join(found).encode("utf-8")).hexdigest()[:16]
        try:
            count, last = counter.read_text(encoding="utf-8").split()
            count = int(count) + 1 if last == sig else 1
        except (OSError, ValueError):
            count = 1
        counter.write_text(f"{count} {sig}", encoding="utf-8")
        if count > MAX_BLOCKS:
            return 0

    out = [f"[prose-lint] {path}"]
    if blocking:
        out.append(f"textlint reported {len(blocking)} finding(s) to fix. Rewrite those passages before continuing.")
        out += textlint_lines(blocking)
    if hits:
        out.append(f"The register matched {len(hits)} wording(s). A hit may stay when the wording is right "
                   "in context; say why. Otherwise rewrite it.")
        out += hit_lines(hits)
    if advisory:
        out.append(f"{len(advisory)} advisory finding(s) do not block: fix the ones that hold and say why each "
                   "of the others stays.")
        out += textlint_lines(advisory)
    if notation:
        out.append(f"{notation} notation finding(s) were also reported; leave them alone.")
    if has_block:
        out.append(f"If a finding cannot be followed, state the reason and let the user decide. After "
                   f"{MAX_BLOCKS} blocks in a row on the same findings, the hook stops reporting them.")
        result = {"decision": "block", "reason": "\n".join(out)}
    else:
        result = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(out)}}
    print(json.dumps(result, ensure_ascii=False))
    return 0


def next_file(data: dict):
    # lint.sh looks for this file before it starts Python for inject.
    base = state_dir()
    return base / f"reply-{session_id(data)}.txt" if base else None


def lint_reply(data: dict) -> int:
    path = next_file(data)
    if data.get("stop_hook_active") or path is None:
        return 0
    text = str(data.get("last_assistant_message") or "")
    if not text.strip() or prose_lang(text) != "ja":
        return 0
    blocking, advisory, _ = textlint_text(text)
    hits = register_hits(text, chat=True)
    if not (blocking or advisory or hits):
        return 0
    log_reply(data, blocking, hits, advisory)
    # The Stop hook runs in the background, so a quick next prompt can come before the findings;
    # the opening words name the reply they belong to.
    head = text.strip().splitlines()[0][:30]
    total = len(blocking) + len(hits) + len(advisory)
    out = [f'[prose-lint] The reply that began "{head}" tripped {total} wording finding(s):']
    out += textlint_lines(blocking) + hit_lines(hits) + textlint_lines(advisory, " (advisory)")
    out.append("Apply these from this reply on, and do not re-send that reply. A register hit may stay "
               "when the wording is right in context; say why.")
    # Appended: two Stop events can fire before the next prompt.
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return 0


def log_reply(data: dict, blocking: list[dict], hits: list[dict], advisory: list[dict]) -> None:
    """Append one line per finding: time|L<line>|<rule or register>|<message or word>|<advisory or instead>."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    first = lambda m: (str(m.get("message") or "").splitlines() or [""])[0]
    lines = ([f'{stamp}|L{m.get("line")}|{m.get("ruleId")}|{first(m)}|' for m in blocking]
             + [f'{stamp}|L{h["line"]}|register|{h["matched"]}|{h["instead"]}' for h in hits]
             + [f'{stamp}|L{m.get("line")}|{m.get("ruleId")}|{first(m)}|advisory' for m in advisory])
    base = Path(os.environ.get("PROSE_LINT_REPLY_LOG_DIR") or HOME / "logs" / "replies")
    try:
        base.mkdir(parents=True, exist_ok=True)
        with (base / f"{session_id(data)}.log").open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError:
        pass  # the log serves a later review; the findings still reach the next prompt


def markers(text: str, pattern) -> list[str]:
    """Return 'L<n> <line>' for each line outside code fences that the pattern matches."""
    out, fence = [], False
    for no, line in enumerate(text.splitlines(), 1):
        if re.match(r"\s*```", line):
            fence = not fence
        elif not fence and pattern.search(line):
            out.append(f"L{no} {line.strip()}")
    return out


def plan_gate(data: dict) -> int:
    tool, tool_input = data.get("tool_name"), data.get("tool_input") or {}
    out = []
    if tool == "ExitPlanMode":
        text = str(tool_input.get("plan") or "")
        if not text.strip():
            return 0
        open_, confirm = markers(text, OPEN), markers(text, CONFIRM)
        blocking = textlint_text(text, tool_input.get("planFilePath"))[0]
        if open_:
            out += [f"{len(open_)} point(s) look unresolved. Investigate each and write the answer into the plan:",
                    *open_[:MAX_SHOWN]]
        if confirm:
            out += [(f"{len(confirm)} point(s) look unconfirmed. Settle them with AskUserQuestion, then write the "
                     "answer into the plan:"), *confirm[:MAX_SHOWN]]
        if blocking:
            out += [f"textlint reported {len(blocking)} wording finding(s) in the plan. Rewrite those passages.",
                    *textlint_lines(blocking)]
        if open_ or confirm:
            out.append("A risk or assumption stated as such under a Risks or Assumptions heading may stay; say so "
                       "and present the plan again. Anything else has to be settled first.")
        head = f'[prose-lint] {tool_input.get("planFilePath") or "the plan"}'
    elif tool == "AskUserQuestion":
        parts = []
        for q in tool_input.get("questions") or []:
            parts += [q.get("question"), q.get("header")]
            for o in q.get("options") or []:
                parts += [o.get("label"), o.get("description")]
        text = "\n\n".join(str(p) for p in parts if p)
        if not text.strip():
            return 0
        blocking = textlint_text(text)[0]
        if blocking:
            out += [f"textlint reported {len(blocking)} wording finding(s) in the question. Rewrite those passages.",
                    *textlint_lines(blocking),
                    ("Line numbers count the question, its header and its option labels and descriptions, "
                     "joined in that order.")]
        head = "[prose-lint] AskUserQuestion"
    else:
        return 0

    counter = (state_dir() or Path(tempfile.gettempdir())) / f"gate-{session_id(data)}-{tool}"
    try:
        count = int(counter.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        count = 0
    if not out or count >= MAX_GATE:
        counter.unlink(missing_ok=True)
        return 0
    counter.write_text(str(count + 1), encoding="utf-8")
    out = [head, *out, f"If a finding does not hold, say why and try again. After {MAX_GATE} denials the call goes through."]
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": "\n".join(out)}}, ensure_ascii=False))
    return 0


def inject(data: dict) -> int:
    path = next_file(data)
    if path is None:
        return 0
    try:
        text = path.read_text(encoding="utf-8")
        path.unlink()
    except OSError:
        return 0
    if text.strip():
        sys.stdout.write(text)
    return 0


def main() -> int:
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        mode = {"file": lint_file, "reply": lint_reply, "inject": inject, "plan": plan_gate}[sys.argv[1]]
        return mode(data) if isinstance(data, dict) else 0
    except Exception:  # noqa: BLE001 - fail open: a broken lint must not stop a write or a reply
        return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # a cp932 console cannot print Japanese
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
