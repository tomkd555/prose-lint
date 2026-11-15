# prose-lint

prose-lint is a Claude Code plugin that lints the wording of a Japanese or English document, then fixes each finding or leaves the passage unchanged and states why. Its hooks run some of these checks on what Claude writes as it works.

## Install

```
/plugin marketplace add tomkd555/prose-lint
/plugin install prose-lint@prose-lint
```

On the first session after an install or an update, a hook sets up the linters under `~/.prose-lint` in the background. It fetches [uv](https://docs.astral.sh/uv/), [vale](https://vale.sh/) and Node when they are missing from PATH, each as a pinned release checked against its SHA-256. The hooks need bash, which macOS, Linux and Git for Windows provide. If a tool is missing, the layer of checks that uses it is skipped, and the report says so.

To install without the plugin system, copy `plugins/prose-lint/skills/prose-lint` to `~/.claude/skills/` and run `uv run python ~/.claude/skills/prose-lint/scripts/setup.py` once. A skill copied by hand has no hooks and no `prose-lint-run`, the command that puts the downloaded tools on PATH. Its layers therefore use only the tools already on your PATH, and the report marks a layer whose tool is not there as skipped.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
check this English draft: README.md
textlint かけて: docs/手順書.md
翻訳調を直して: docs/設計書.md
スライドの文言を直して: slides/review.pptx
翻訳をチェックして: docs/report.md と docs/report.ja.md
```

The skill detects the document's language and runs the layers for that language. Its reply is a report that lists every finding by layer and marks each one as fixed or as left unchanged, with the reason. Claude edits the document only to fix the findings it has confirmed.

## What it checks

| Layer | Checks on Japanese text | Checks on English text |
|---|---|---|
| Style | The genre, the reader and the 文体, decided first. Every rewrite follows them. | A one-line statement of what the document is and who reads it |
| Reader | An agent in a fresh context finds each sentence that is unclear or reads as translated from English. | The same, for unclear sentences and English that keeps the structure of a Japanese draft |
| textlint | The technical-writing, JTF, AI-writing and AI-words presets, and the kana rules of 内閣訓令 | Duplicated conjunctions and two rules on Markdown structure |
| Register | Your own table of rejected wordings | The row of that table on definition by negation |
| Morphology | `koyobun.py`: checks from 「公用文作成の考え方」, built on sudachipy's morphological analysis | |
| Flow and norm | `flow.py` counts how the sentences end and join. `norm.py` compares how often the text uses common forms, such as connectives, demonstratives and the passive, with a baseline counted from news text. | |
| natural-japanese | Its lint and its naturalness score | |
| Modes | Translationese, academic writing, and blog posts and slide decks (a `.pptx` included) | |
| vale | | proselint, ai-tells and five house rules |

A translation in either direction is compared with its source first. For the details, `plugins/prose-lint/skills/prose-lint/SKILL.md` describes each layer, and the `references/` folder beside it holds the sources behind the rules.

## Hooks

`/plugin` asks during installation whether to turn on the wording-check hooks. They are on by default. To change the setting, run `/plugin configure prose-lint@prose-lint`.

- After each Write or Edit of a Markdown, text or HTML file, textlint and your register of rejected wordings run on the changed lines; when the text is English, vale also runs on it. For each finding the skill would fix, the hook returns the passage to Claude to rewrite.
- After each Write or Edit of a source file, the hook checks the Japanese in comments and strings against your register.
- After each reply Claude writes in Japanese, textlint and your register run on the reply in the background, so Claude receives the findings with your next prompt.
- Before Claude shows you a plan or a question, the hook checks its wording. The hook blocks a plan that still has an unresolved item (TBD, 未定, 要確認).

## Configuration

Your register is `~/.prose-lint/vocabulary.md`, and it is yours to edit. Each row holds a regex, the wording to use, and the reason shown with each hit. Running the setup again keeps any config file or register you have edited.

These environment variables set the files and folders prose-lint uses:

| Environment variable | File or folder |
|---|---|
| `PROSE_LINT_HOME` | The folder for configs, registers and downloaded tools (default `~/.prose-lint`) |
| `PROSE_LINT_REGISTER` | Your register of rejected wordings |
| `PROSE_LINT_ACADEMIC_REGISTER`, `PROSE_LINT_TRANSLATIONESE_REGISTER`, `PROSE_LINT_SLOP_REGISTER` | The academic, translationese and stop-ai-slop-jp registers |
| `PROSE_LINT_PATTERNS` | A Markdown file of your notes on wordings you rejected, which the Reader layer reads |
| `PROSE_LINT_NORM_BASELINE` | The baseline `norm.py` reads |
| `PROSE_LINT_REPLY_LOG_DIR` | The folder for the log of reply findings |
| `NATURAL_JAPANESE_SCRIPTS` | A copy of natural-japanese's scripts to use in place of the bundled one |

The shipped baseline holds rates counted from Japanese Wikinews. To compare a text with prose other than news, build a baseline from articles of that kind that you have. Run this command in the skill's `scripts` folder:

```
uv run norm.py --build ~/.prose-lint/norm-baseline.json --name "<label>" --plain <folder>
```

## Credits and licence

MIT. prose-lint is an independent project. [proselint](https://github.com/amperser/proselint) is a separate linter by other authors, which this skill runs through vale.

- `vendor/natural-japanese/` holds the `skills/natural-japanese` directory of [natural-japanese](https://github.com/coji/natural-japanese) (MIT © 2026 coji) 1.6.4, as published at commit 25a8638, with its `SKILL.md` renamed `guide.md`. Its `LICENSE` is beside it. prose-lint's `SKILL.md` restates natural-japanese's naturalness-score formula, and six register rows restate patterns from natural-japanese's `references/forbidden-patterns.md`.
- `references/stop-ai-slop-jp/` holds [stop-ai-slop-jp](https://github.com/iKora128/stop-ai-slop-jp) (MIT © 2026 Daichi Nagashima) as published at commit e09d327, with its `SKILL.md` renamed `rules.md`. stop-ai-slop-jp is a Japanese adaptation of [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop). Its `LICENSE` is beside it. `assets/slop.sample.md` restates its phrase lists as regex rows.
- `assets/norm-baseline.json` holds rates counted from [Japanese Wikinews](https://ja.wikinews.org/) (CC BY 4.0, the Wikinews contributors), and the article text stays out of this repository.
- `assets/textlint/dict/fukushi.yml` is the dictionary of [textlint-rule-ja-hiragana-fukushi](https://github.com/lostandfound/textlint-rule-ja-hiragana-fukushi) (MIT © Hiroshi Takase) with five entries removed and one duplicate dropped. Its header holds the upstream copyright and permission notice.
- `assets/vale/.vale.ini` pulls [ai-tells](https://github.com/tbhb/vale-ai-tells) (MIT, Tony Burns) through the vale package hub. The setup downloads [uv](https://github.com/astral-sh/uv) (MIT or Apache-2.0), [vale](https://github.com/vale-cli/vale) (MIT) and [Node.js](https://nodejs.org/) (MIT) from their official releases. This repository stores none of them.
- `references/exemplars-japanese.md` quotes excerpts under their own terms: government documents under 公共データ利用規約（第1.0版）, and papers and a review under CC BY 4.0. The file gives the source, the URL and the licence of each excerpt.
- The academic, translationese and flow references restate rules from the guides and studies each file lists, with short quotations for citation.
- The 公用文 rules come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html. The kana rules restate 「公用文における漢字使用等について」 (平成22年内閣訓令第1号).
