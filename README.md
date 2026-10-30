# prose-lint

A Claude Code skill that runs the wording linters over one document, picks the configs its language calls for, and rules on every hit as fixed or kept with a reason. Japanese goes through a style settled first, a reader for translationese, five linters and a closing read-through; English through three linters and a closing read-through. Both sides carry a layer for the signs of LLM-written text.

| Layer | Japanese | English |
|---|---|---|
| Style | Settled before any layer runs: what the document is and who reads it, its 文体, and where its words come from (`business`, `paper`, `official`, `academic`, `article`). A calling skill can pass `style=<name>`. Every rewrite is written to it. | — |
| Reader | An agent in a fresh context reads the document against `references/translationese-japanese.md` and the exemplar passages for its style in `references/exemplars-japanese.md`, and flags each sentence that reads as translated from English or sits off the style: a word picked as the dictionary match of an English one, an English frame, a 文体 or a word at the wrong distance from the reader. A second read checks the rewrites. | — |
| Translationese | `register.py --translationese` over 13 rows, each resting on a style guide or study and measured against 83 human-written documents | — |
| textlint | ja-technical-writing, JTF style and AI-writing presets. The kana rules of 内閣訓令: four hiragana rules and a prh rule set, `assets/textlint/prh/koyobun-kana.yml`. い抜き, さ入れ and フィラー. A たり with no partner. Two spellings of one word in a document (ユーザー and ユーザ). The skill sorts findings into blocking, advisory and notation. | Duplicated conjunctions at sentence starts. The AI-writing preset's two Markdown-shape rules: bold-label bullets, emoji bullets and bold in headings. |
| Register | `scripts/register.py` over a Markdown table of rejected wordings that you grow one row at a time: definition by negation, the spoken register, the stock phrases of generated Japanese | the same table's English negation row |
| natural-japanese | `lint.py` in the AI-smell and reading-load lanes, the naturalness score, a baseline rerun after the fixes | — |
| Morphology | `scripts/koyobun.py`. From 「公用文作成の考え方」: passive, clause chains, 漢字１字＋する and 等/など. House rules: clauses strung on 読点, conjunctive が, させていただく, 体言止め in body text and negated predicates. | — |
| stop-ai-slop-jp | For blog posts, essays and slide decks. `register.py --slop` over 31 rows restating [stop-ai-slop-jp](https://github.com/iKora128/stop-ai-slop-jp)'s phrase lists and symbol rules, in three groups that each hit names: rewrite each hit, count the hits, or read in context. The rows were measured on technical books and Wikipedia articles, which hold no blog posts. A `.pptx` is read through `scripts/pptx_text.py`, tables and grouped shapes included. The reader finds its structure patterns (false agency, a thesis as a heading, uniform rhythm) and scores the five axes of its rubric out of 50. | — |
| Academic mode | `register.py --academic` over a second table of 47 rows, each citing its sources. The spoken register: でも, すごく, こんな, と思う and です・ます. 文語調: べく and ごとく. The over-stiff forms: することができる and を行う. `koyobun.py --academic` for って and たら. The rules a regex cannot find, read from `references/academic-japanese.md`. | — |
| vale | — | proselint: clichés, redundancy, corporate speak, jargon and hedging, and vale's check for a word typed twice. [ai-tells](https://github.com/tbhb/vale-ai-tells): rules for the signs of LLM-written English. They cover overused vocabulary, stock openers and closings, hedges, vague attributions and participial padding. They also cover copula dodges, transitions, figurative verbs and em dashes. `AISigns`: three house rules for the model talking about itself, emoji in headings, and five or more commas in one sentence. |

The register ships with twelve sample rows. Two catch definition by negation (`ではない`, `not X but Y`, `rather than` and related forms), which the skill rewrites to say what a thing is. Four catch the spoken register in a formal document. Six catch the stock phrases of generated Japanese that natural-japanese's catalogue lists but its lint leaves to the eye: hearsay with no source, breadth adjectives, outcomes named by an abstract noun, an intention softened with と思います, and the boilerplate opening and closing of a blog post.

Academic mode runs on a Japanese paper, thesis or report, when you ask for the register of one or when the text carries a reference list and 本研究 or 本稿. It rewrites spoken Japanese into the written register of a paper and holds it back from the stiff forms the same guides warn against. Every row and rule rests on sources read for it:

- 文化審議会「公用文作成の考え方」
- the writing guides of thirteen universities (東北大学, 金沢大学, 立教大学 and others)
- fourteen lab and faculty guides
- three academic societies' author guides
- six research papers, among them a survey of 1,900 written and spoken words in 63 books and papers on writing (柏野ほか 2016) and a BCCWJ measure of how hard connectives are (馬場 2018)

`references/academic-japanese.md` quotes the passage behind each rule, lists where the sources disagree and how the skill rules then, and gives every source with its URL.

The reading carries the translationese layer, because a surface form alone says little. The 83 human-written documents published before 2022-12 used the commonest forms freely: において in 47 and を行う in 52. The reader works from `references/translationese-japanese.md`, which names 20 markers in three groups (words, frames, style fit), gives a rewrite per style for each, and rests on these sources:

- Microsoft's Japanese localization style guide, the Red Hat and JTF style guides, SmartHR's writing guide and 文化審議会「公用文作成の考え方」
- translator-education articles with before/after pairs
- corpus studies of translated Japanese, among them Meldrum (2009), where only third-person pronouns and longer paragraphs held as markers

Each quotation names its source's URL, so it can be checked against the page. The register carries the 13 forms that a regex finds and human writers rarely use, or that need a ruling in context.

The reader and every rewrite also work from `references/exemplars-japanese.md`: eighteen paragraphs of present-day Japanese that institutions and award committees hold up as well written, grouped by the style that reads them. They come from 文化審議会's 「公用文作成の考え方」 and its 2018 report 「分かり合うための言語コミュニケーション」, デジタル庁's accessibility guidebook, and two papers that won 優秀賞 at 言語処理学会's annual meeting. Each passage is quoted verbatim, with notes on how its sentences open and end, which words they choose and how they join, and with the reason it was chosen.

## Install

```
/plugin marketplace add tomkd555/prose-lint
/plugin install prose-lint@prose-lint
```

That is the whole install. On the first session after an install or an update, the plugin's SessionStart hook (`hooks/session-start.sh`) sets up the linters in the background, in about a minute:

- It fetches [uv](https://docs.astral.sh/uv/) when none is on PATH; uv then fetches Python, sudachipy and python-pptx on first use.
- It runs `scripts/setup.py`. That script downloads [vale](https://vale.sh/) 3.25.1 and Node 24.22.2 with npm when they are not on PATH. It copies the textlint and vale configs to `~/.prose-lint` (or `$PROSE_LINT_HOME`) and runs `npm install` and `vale sync` there; the sync pulls proselint and ai-tells from the vale package hub. It puts the sample registers in the same directory as `vocabulary.md`, `academic.md`, `translationese.md` and `slop.md`.

Every download is a pinned release from the tool's official site, checked against its SHA-256 and kept under `~/.prose-lint`; a tool already on PATH is used as it is. The plugin's `bin/prose-lint-run` puts the downloaded tools on PATH for the skill's commands. The hook needs bash, which macOS, Linux and Git for Windows provide. `~/.prose-lint/setup.log` holds the last run, and `~/.prose-lint/.setup-version` the plugin version it set up; a setup with a failed step reruns on the next session. A plugin installed in a running session is set up when the skill first runs.

A rerun refreshes `package.json`, the prh rule set, the fukushi dictionary and the AISigns style. It keeps a `.textlintrc*.json` or `.vale.ini` you have edited and copies a register the update added. It names each config or register that differs from the shipped file so you can merge a change by hand. A missing tool skips its layer, and the report names it.

Without the plugin system, clone the repository, copy `plugins/prose-lint/skills/prose-lint` to `~/.claude/skills/`, and run `uv run python ~/.claude/skills/prose-lint/scripts/setup.py` once; put `~/.prose-lint/bin` and `~/.prose-lint/node` on PATH when it downloaded vale or Node there.

[natural-japanese](https://github.com/coji/natural-japanese) 1.6.4 ships in `skills/prose-lint/vendor/natural-japanese`; set `NATURAL_JAPANESE_SCRIPTS` to another copy's `skills/natural-japanese/scripts` directory to use that one for the morphology lint.

Vale 3.24 and later match `^` at the start of a paragraph only. ai-tells 1.37.0, the latest release on 2026-10-30, predates its fix for this ([tbhb/vale-ai-tells#88](https://github.com/tbhb/vale-ai-tells/pull/88), merged 2026-10-07). Until the next ai-tells release, its `ConclusionMarkers` rule finds a sentence-opening "Ultimately," or "Overall," only at the start of a paragraph. Run `setup.py` again after that release, or delete `~/.prose-lint/.setup-version` so the next session reruns it; `vale sync` pulls the latest ai-tells.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
textlint かけて: docs/手順書.md
check this English draft: README.md
AI っぽさを消して: docs/blog.md
論文調にして: thesis/chapter2.md
翻訳調を直して: docs/設計書.md
AI臭を消して: blog/2026-10-post.md
スライドの文言を直して: slides/review.pptx
```

The skill settles the language, runs the layers for it, and replies with a report. For Japanese, the report gives the naturalness score first, then every finding by layer as fixed or kept with a reason, then the counts from the rerun after the fixes. For English, it gives the count of AI-sign hits per 1,000 words first, then the ledger, then the count that remains. It edits the document only where a finding holds, and never applies the linters' automatic fixes.

## Your register

`~/.prose-lint/vocabulary.md` is yours to edit. Each row is a regex, the wording to use instead, and the reason shown with each hit; the file's header gives the rules for a good row. Point `PROSE_LINT_REGISTER` at another file to keep it elsewhere; a `.csv` with the header `Pattern,Instead,Why` is read the same way. `~/.prose-lint/academic.md` is the academic register in the same format, with `PROSE_LINT_ACADEMIC_REGISTER` to move it; add a row for your field's or journal's house usage, and cite the source in the `Why` column the way the shipped rows do. `~/.prose-lint/translationese.md` is the translationese register, with `PROSE_LINT_TRANSLATIONESE_REGISTER` to move it. `~/.prose-lint/slop.md` is the stop-ai-slop-jp register, with `PROSE_LINT_SLOP_REGISTER` to move it. Point `PROSE_LINT_PATTERNS` at a Markdown file of your own notes on wordings you rejected, and the reader reads it after the reference.

The kana rules live next to it in `~/.prose-lint/textlint/prh/koyobun-kana.yml`, one rule per line of the 訓令's appendix with a test for each guard; add a row there for a house spelling, or delete one that misfires on your house style. `~/.prose-lint/textlint/dict/fukushi.yml` is the adverb dictionary, the rule's own minus the five words the 訓令 keeps in kanji.

## Contents

| Path | Holds |
|---|---|
| `plugins/prose-lint/skills/prose-lint/SKILL.md` | The routing, the layers, the ruling on each finding id, the report |
| `plugins/prose-lint/hooks/` | `hooks.json` and `session-start.sh`, which run `setup.py` once per plugin version |
| `plugins/prose-lint/bin/prose-lint-run` | Runs a command with the downloaded uv, vale and Node on PATH |
| `plugins/prose-lint/skills/prose-lint/scripts/` | `register.py`, `koyobun.py`, `pptx_text.py`, `setup.py` |
| `plugins/prose-lint/skills/prose-lint/vendor/natural-japanese/` | natural-japanese 1.6.4 and its licence |
| `plugins/prose-lint/skills/prose-lint/assets/textlint/` | `package.json`, the two configs, `prh/koyobun-kana.yml`, `dict/fukushi.yml` |
| `plugins/prose-lint/skills/prose-lint/assets/vale/` | `.vale.ini`, `styles/AISigns/` |
| `plugins/prose-lint/skills/prose-lint/assets/vocabulary.sample.md` | The sample register |
| `plugins/prose-lint/skills/prose-lint/assets/academic.sample.md` | The academic register |
| `plugins/prose-lint/skills/prose-lint/assets/translationese.sample.md` | The translationese register |
| `plugins/prose-lint/skills/prose-lint/assets/slop.sample.md` | The stop-ai-slop-jp register |
| `plugins/prose-lint/skills/prose-lint/references/academic-japanese.md` | The academic rules, the passages they rest on, the disagreements and the source list |
| `plugins/prose-lint/skills/prose-lint/references/translationese-japanese.md` | The translationese markers, the test and the rewrite per style for each, the measurements, the disagreements and the source list |
| `plugins/prose-lint/skills/prose-lint/references/stop-ai-slop-jp/` | stop-ai-slop-jp as published at commit e09d327: its `SKILL.md` as `rules.md`, `phrases.md`, `structures.md`, `examples.md` and its licence |
| `plugins/prose-lint/skills/prose-lint/references/exemplars-japanese.md` | Passages of present-day Japanese per style, the features to take from each, and the source, selection reason and licence of each |

## Considered and left out

Surveyed in September 2026 while choosing the layers above; listed so the choice can be revisited.

| Tool | Why not |
|---|---|
| textlint-rule-stop-words (2,000 words) | Overlaps ai-tells and flags ordinary verbs (accelerate, accompany); ai-tells gives a rewrite with each hit |
| textlint-rule-preset-ai-words-ja | Its list comes from one tech-blog corpus and holds everyday words (走る, 壊れる, 経路) |
| textlint-rule-ja-hiraku | Opens 及び, 更に, 既に and the other words the 訓令 keeps in kanji; the four hiragana rules plus prh follow the 訓令 as written |
| textlint-rule-rousseau | Per-sentence readability and write-good's checks; neither earned a layer |
| textlint-rule-write-good, terminology, en-max-word-count | Removed in 1.5.0. Measured on six Go blog posts and five Rust book chapters (18,000 words): write-good's remaining check fired on many, few and several 34 times; terminology rewrote at run time, README and the verb indexes; a word cap says nothing about whether a sentence reads well |
| eleven ai-tells rules | Switched off in 1.5.0, because they fired more often on that human prose than on LLM-written articles on the same topics: For example, Therefore, implements, In other words, of course, a single channel. `.vale.ini` lists them |
| textlint-rule-ja-no-orthographic-variants | Reports 呼び出し時 against とき and 呼び方 against ほう, the pairs the 訓令 writes differently on purpose |
| textlint-rule-preset-smarthr | Its prh dictionary opens 及び and other words the 訓令 keeps in kanji; its other rules overlap the two presets |
| textlint-rule-common-misspellings | One hit in 41,000 words, on the COBOL keyword THRU |
| vale Readability, Microsoft, Google | Grade-level metrics and one company's style; neither says whether a person wrote the text |
| vale signs-of-ai-writing, LLMCliches, Slop | Smaller ports of the same Wikipedia list; ai-tells covers them and is in the vale hub |
| textlint-rule-preset-ja-engineering-paper | Deletes 非常に and 極めて outright, rewrites 又は, 基に and 挙げる against the 訓令, and forces 「，．」; its register ideas are cited in the academic register instead |
| Harper, LanguageTool | Grammar and spelling; a different job, and a Rust or Java install |
| RedPen, Just Right!, MS Word 校正, Enno, 文賢 | Dormant since 2021, or a GUI or web form with no CLI |

## Credits and licence

MIT. prose-lint is an independent project; [proselint](https://github.com/amperser/proselint) is a separate linter by other authors, which this skill runs through vale.

- `vendor/natural-japanese/` holds the `skills/natural-japanese` directory of [natural-japanese](https://github.com/coji/natural-japanese) (MIT © 2026 coji) 1.6.4, as published at commit 25a8638, with its `SKILL.md` renamed `guide.md` so Claude Code does not load it as a second skill. Its `LICENSE` sits beside it. The skill runs its `lint.py` and `outline.py`, and `koyobun.py` imports its `textcore.py`. `SKILL.md` restates its naturalness-score formula and bands from `references/diagnose.md` and points to sections 3 and 5 of its `SKILL.md`, and six register rows restate patterns from its `references/forbidden-patterns.md`.
- The SessionStart hook and `setup.py` download [uv](https://github.com/astral-sh/uv) (MIT or Apache-2.0), [vale](https://github.com/vale-cli/vale) (MIT) and [Node.js](https://nodejs.org/) (MIT, with the third-party licences in its archive) from their official releases. Nothing of them is stored in this repository.
- `references/stop-ai-slop-jp/` holds [stop-ai-slop-jp](https://github.com/iKora128/stop-ai-slop-jp) (MIT © 2026 Daichi Nagashima), itself a Japanese adaptation of [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), as published at commit e09d327, with its `SKILL.md` renamed `rules.md` so Claude Code does not load it as a second skill. Its `LICENSE` sits beside it. `assets/slop.sample.md` restates its phrase lists as regex rows.
- `assets/vale/.vale.ini` pulls [ai-tells](https://github.com/tbhb/vale-ai-tells) (MIT, Tony Burns) through the vale package hub; nothing from it is copied here.
- `assets/textlint/dict/fukushi.yml` is the dictionary of [textlint-rule-ja-hiragana-fukushi](https://github.com/lostandfound/textlint-rule-ja-hiragana-fukushi) (MIT © Hiroshi Takase) with five entries removed and one duplicate dropped; its header carries the upstream copyright and permission notice.
- The academic register and `references/academic-japanese.md` restate rules from the university, lab, society and research sources listed in that file, with short quotations for citation; no text is copied beyond those quotations.
- The translationese register and `references/translationese-japanese.md` restate rules from the style guides, translator articles and studies listed in that file, with short quotations for citation. The human-written documents they were measured against are natural-japanese's calibration sources, fetched for the measurement and not redistributed.
- `references/exemplars-japanese.md` quotes excerpts under their own terms. 文化審議会「公用文作成の考え方」, 文化審議会国語分科会「分かり合うための言語コミュニケーション（報告）」 and デジタル庁「ウェブアクセシビリティ導入ガイドブック」 are used under 公共データ利用規約（第1.0版）, which is compatible with CC BY 4.0. The papers by 川崎・永田・高村・大谷 (2025) and 永田・川崎・大谷・高村 (2024), from 言語処理学会's annual meetings, are CC BY 4.0. The file names the source and URL of each excerpt.
- The four 公用文 rules paraphrased in `SKILL.md` and `koyobun.py` come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html. The kana rules in `prh/koyobun-kana.yml` restate 「公用文における漢字使用等について」 (平成22年内閣訓令第1号).
