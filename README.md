# prose-lint

A Claude Code skill that runs the wording linters over one document, picks the configs its language calls for, and rules on every hit as fixed or kept with a reason. Japanese goes through four linters and a closing read-through; English through three linters and a closing read-through.

| Layer | Japanese | English |
|---|---|---|
| textlint | ja-technical-writing, JTF style and AI-writing presets plus three hiragana rules; the skill sorts findings into blocking, advisory and notation | write-good, terminology, a 40-word sentence cap, duplicated conjunctions at sentence starts |
| Register | `scripts/register.py` over a Markdown table of rejected wordings that you grow one row at a time | the same table's English rows |
| natural-japanese | `lint.py` in the AI-smell and reading-load lanes, the naturalness score, a baseline rerun after the fixes | — |
| Morphology | `scripts/koyobun.py`: passive, clause chains, 漢字１字＋する and 等/など from 「公用文作成の考え方」; 体言止め in body text and negated predicates as house rules | — |
| vale | — | proselint: redundancy, corporate speak, jargon, hedging |

The register ships with six sample rows. Two of them catch definition by negation (`ではない`, `not X but Y`, `rather than` and related forms), which the skill rewrites to say what a thing is.

## Install

```
/plugin marketplace add coji/natural-japanese
/plugin install natural-japanese@natural-japanese
/plugin marketplace add tomkd555/prose-lint
/plugin install prose-lint@prose-lint
```

Without the plugin system, clone the repository and copy `plugins/prose-lint/skills/prose-lint` to `~/.claude/skills/`; clone [natural-japanese](https://github.com/coji/natural-japanese) anywhere and set `NATURAL_JAPANESE_SCRIPTS` to its `skills/natural-japanese/scripts` directory.

Then install the linters once:

```
uv run python <skill dir>/scripts/setup.py
```

It copies the textlint and vale configs to `~/.prose-lint` (or `$PROSE_LINT_HOME`), runs `npm install` and `vale sync` there, and puts the sample register at `~/.prose-lint/vocabulary.md`. The skill also runs this step itself when the linters are missing.

Requirements: Python 3.10+, [uv](https://docs.astral.sh/uv/), Node 20.18+ with npm for textlint, [vale](https://vale.sh/) for English, and natural-japanese. A missing tool skips its layer, and the report names it.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
textlint かけて: docs/手順書.md
check this English draft: README.md
```

The skill settles the language, runs the layers for it, and replies with a report: for Japanese, the naturalness score first, then every finding by layer as fixed or kept with a reason, then the counts from the rerun after the fixes. It edits the document only where a finding holds, and never applies the linters' automatic fixes.

## Your register

`~/.prose-lint/vocabulary.md` is yours to edit. Each row is a regex, the wording to use instead, and the reason shown with each hit; the file's header gives the rules for a good row. Point `PROSE_LINT_REGISTER` at another file to keep it elsewhere.

## Contents

| Path | Holds |
|---|---|
| `plugins/prose-lint/skills/prose-lint/SKILL.md` | The routing, the layers, the ruling on each finding id, the report |
| `plugins/prose-lint/skills/prose-lint/scripts/` | `register.py`, `koyobun.py`, `setup.py` |
| `plugins/prose-lint/skills/prose-lint/assets/` | textlint `package.json` and configs, the vale config, `vocabulary.sample.md` |

## Credits and licence

MIT.

- `koyobun.py` imports `textcore.py` from [natural-japanese](https://github.com/coji/natural-japanese) (MIT, coji) at run time. `SKILL.md` restates natural-japanese's naturalness-score formula and bands from its `references/diagnose.md` and points to its other reference files. No code from it is copied here.
- The four 公用文 rules paraphrased in `SKILL.md` and `koyobun.py` come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html.
