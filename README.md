# prose-lint

A Claude Code plugin that lints the wording of a Japanese or English document and rules on every finding: fixed, or kept with a reason. Its hooks run the same checks on what Claude writes while it works.

## What it checks

| Layer | Japanese | English |
|---|---|---|
| Style | Settled first: the genre, the reader, the 文体 and where the words come from. Rewrites are written to it. | One line on the document and its reader |
| Reader | An agent in a fresh context finds each sentence that is unclear, reads as translated from English or sits off the style. | The same, for unclear sentences and English that follows a Japanese draft |
| textlint | The technical-writing, JTF, AI-writing and AI-words presets, and the kana rules of 内閣訓令 | Duplicated conjunctions and two Markdown-shape rules |
| Register | Your own table of rejected wordings. A plain Japanese word is matched on morpheme boundaries. | The table's negation row |
| Morphology | `koyobun.py`: checks from 「公用文作成の考え方」 and house rules, read with sudachipy | |
| Flow | `flow.py`: how the sentences end and join. It marks a document `flat`. | |
| Norm | `norm.py`: the rates of ordinary forms, laid beside a baseline of news text. It marks a document `off`. | |
| natural-japanese | Its lint and its naturalness score | |
| Translationese, academic mode, stop-ai-slop-jp | Registers and references for translated-sounding text, for papers and theses, and for blog posts and slide decks (a `.pptx` included) | |
| vale | | proselint, ai-tells and five house rules |

A translation in either direction is compared with its source first, by `pair_check.py` and by an agent in a fresh context.

`plugins/prose-lint/skills/prose-lint/SKILL.md` describes each layer and the ruling on each finding. The files under `references/` hold the sources and the measurements behind the rules.

### The flow and norm layers

The other layers each report a wording to take out, so a text can pass them all by leaving ordinary Japanese out. In 541 replies Claude wrote under these hooks, が joined clauses 6 times in 1,000 sentences, where news text holds 81 to 94. `flow.py` and `norm.py` count what the others leave unread.

- `flow.py` counts how the sentences end, how many clause joints a sentence holds and how many sentences are tied to nothing around them. After the fixes it compares the text with its original. A rewrite then keeps how sure each sentence is and how it ties to the next.
- `norm.py` counts clause joints, conjunctive が, opening connectives, demonstratives, the passive and verbs made of a noun and する. It lays each rate beside a baseline counted from 1,405 articles of Japanese Wikinews, and marks the text `off` when two or more rates sit past what 95 % of the baseline documents hold.

Measured with a baseline built from half of the Wikinews articles, `norm.py` marked 93.9 % of 297 of those replies `off`, 4.9 % of the 695 articles held out, 4.6 % of 109 science news articles edited by a public agency, and none of 27 human-written business and technical documents.

The sites of NHK and the national newspapers disallow AI agents in robots.txt. To hold a text to their prose, build a baseline from articles you hold:

```
uv run norm.py --build ~/.prose-lint/norm-baseline.json --name "<label>" --plain <folder>
```

## Install

```
/plugin marketplace add tomkd555/prose-lint
/plugin install prose-lint@prose-lint
```

On the first session after an install or an update, the SessionStart hook sets up the linters in the background, in about a minute. It fetches [uv](https://docs.astral.sh/uv/), [vale](https://vale.sh/) and Node when they are missing from PATH, each as a pinned release checked against its SHA-256. It copies the configs and the sample registers to `~/.prose-lint` and runs `npm install` and `vale sync` there. The hooks need bash, which macOS, Linux and Git for Windows provide. `~/.prose-lint/setup.log` holds the last run. A missing tool skips its layer, and the report names it.

A rerun keeps a config or register you have edited, and names each one that differs from the shipped file.

Without the plugin system, copy `plugins/prose-lint/skills/prose-lint` to `~/.claude/skills/` and run `uv run python ~/.claude/skills/prose-lint/scripts/setup.py` once.

## Hooks

`/plugin` asks at install whether to turn on the wording-check hooks. They are on by default, and `/plugin configure prose-lint@prose-lint` changes the setting.

- After each Write or Edit of a Markdown, text or HTML file, textlint and your register run on the changed lines, and vale runs on English. A finding of the tier the skill fixes, or a register hit, returns the passage to Claude to rewrite. Advisory findings are reported to Claude, and the write stays in place.
- A new Japanese file also runs `flow.py` and `norm.py`. A `flat` or `off` mark asks Claude to reread the file by paragraph, and the write stays in place.
- After each Write or Edit of a source file, the register reads the Japanese in comments and strings.
- After each Japanese reply, the same checks run in the background, and Claude receives the findings with your next prompt.
- Before a plan goes up for approval, the hook holds it back while a point is still open (TBD, 未定, 要確認).

The hooks skip `node_modules`, `.git`, `__pycache__`, `scratchpad`, the skill's own folder, `~/.prose-lint` and your registers.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
textlint かけて: docs/手順書.md
check this English draft: README.md
無機質な文章を直して: docs/報告書.md
論文調にして: thesis/chapter2.md
翻訳調を直して: docs/設計書.md
スライドの文言を直して: slides/review.pptx
翻訳をチェックして: docs/report.md と docs/report.ja.md
```

The skill settles the language, runs the layers for it and replies with a report: every finding by layer, as fixed or kept with a reason. It edits the document only where a finding holds, and never applies the linters' automatic fixes.

## Your register and settings

`~/.prose-lint/vocabulary.md` is yours to edit. Each row is a regex, the wording to use, and the reason shown with each hit. A `.csv` works too, and the docstring of `register.py` gives its columns and flags. The kana rules are in `~/.prose-lint/textlint/prh/koyobun-kana.yml`.

| Variable | Sets |
|---|---|
| `PROSE_LINT_HOME` | The folder for configs, registers and downloaded tools (default `~/.prose-lint`) |
| `PROSE_LINT_REGISTER` | Your register of rejected wordings |
| `PROSE_LINT_ACADEMIC_REGISTER`, `PROSE_LINT_TRANSLATIONESE_REGISTER`, `PROSE_LINT_SLOP_REGISTER` | The academic, translationese and stop-ai-slop-jp registers |
| `PROSE_LINT_PATTERNS` | A Markdown file of your notes on wordings you rejected, which the reader reads |
| `PROSE_LINT_NORM_BASELINE` | The baseline `norm.py` reads |
| `PROSE_LINT_REPLY_LOG_DIR` | The folder for the log of reply findings |
| `NATURAL_JAPANESE_SCRIPTS` | Another copy of natural-japanese's scripts |

## Contents

| Path under `plugins/prose-lint/` | Holds |
|---|---|
| `skills/prose-lint/SKILL.md` | The routing, the layers, the ruling on each finding and the report |
| `skills/prose-lint/scripts/` | `register.py`, `koyobun.py`, `flow.py`, `norm.py`, `pair_check.py`, `pptx_text.py`, `setup.py` and `eval.py` |
| `skills/prose-lint/assets/` | The textlint and vale configs, the sample registers and `norm-baseline.json` |
| `skills/prose-lint/references/` | The rules with their sources: translationese, academic Japanese, exemplar passages, flow, the English reader, the translation check and stop-ai-slop-jp |
| `skills/prose-lint/vendor/natural-japanese/` | natural-japanese 1.6.4 and its licence |
| `hooks/`, `bin/` | The setup and wording-check hooks, and `prose-lint-run` |

## Credits and licence

MIT. prose-lint is an independent project. [proselint](https://github.com/amperser/proselint) is a separate linter by other authors, which this skill runs through vale.

- `vendor/natural-japanese/` holds the `skills/natural-japanese` directory of [natural-japanese](https://github.com/coji/natural-japanese) (MIT © 2026 coji) 1.6.4, as published at commit 25a8638, with its `SKILL.md` renamed `guide.md`. Its `LICENSE` is beside it. `SKILL.md` restates its naturalness-score formula, and six register rows restate patterns from its `references/forbidden-patterns.md`.
- `references/stop-ai-slop-jp/` holds [stop-ai-slop-jp](https://github.com/iKora128/stop-ai-slop-jp) (MIT © 2026 Daichi Nagashima), a Japanese adaptation of [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), as published at commit e09d327, with its `SKILL.md` renamed `rules.md`. Its `LICENSE` is beside it. `assets/slop.sample.md` restates its phrase lists as regex rows.
- `assets/norm-baseline.json` holds rates counted from [Japanese Wikinews](https://ja.wikinews.org/) (CC BY 4.0, the Wikinews contributors), and the article text stays out of this repository.
- `assets/textlint/dict/fukushi.yml` is the dictionary of [textlint-rule-ja-hiragana-fukushi](https://github.com/lostandfound/textlint-rule-ja-hiragana-fukushi) (MIT © Hiroshi Takase) with five entries removed and one duplicate dropped. Its header holds the upstream copyright and permission notice.
- `assets/vale/.vale.ini` pulls [ai-tells](https://github.com/tbhb/vale-ai-tells) (MIT, Tony Burns) through the vale package hub. The setup downloads [uv](https://github.com/astral-sh/uv) (MIT or Apache-2.0), [vale](https://github.com/vale-cli/vale) (MIT) and [Node.js](https://nodejs.org/) (MIT) from their official releases. This repository stores none of them.
- `references/exemplars-japanese.md` quotes excerpts under their own terms: government documents under 公共データ利用規約（第1.0版）, and papers and a review under CC BY 4.0. The file gives the source, the URL and the licence of each excerpt.
- The academic, translationese and flow references restate rules from the guides and studies each file lists, with short quotations for citation.
- The 公用文 rules come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html. The kana rules restate 「公用文における漢字使用等について」 (平成22年内閣訓令第1号).
