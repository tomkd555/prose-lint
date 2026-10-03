# prose-lint

A Claude Code skill that runs the wording linters over one document, picks the configs its language calls for, and rules on every hit as fixed or kept with a reason. Japanese goes through four linters and a closing read-through; English through three linters and a closing read-through. Both sides carry a layer for the signs of LLM-written text, so a draft comes back reading as one person wrote it.

| Layer | Japanese | English |
|---|---|---|
| textlint | ja-technical-writing, JTF style and AI-writing presets. The kana rules of 内閣訓令: four hiragana rules and a prh rule set, `assets/textlint/prh/koyobun-kana.yml`. い抜き, さ入れ and フィラー. The skill sorts findings into blocking, advisory and notation. | write-good, terminology, a 40-word sentence cap and duplicated conjunctions at sentence starts. The AI-writing preset's two Markdown-shape rules: bold-label bullets, emoji bullets and bold in headings. |
| Register | `scripts/register.py` over a Markdown table of rejected wordings that you grow one row at a time: definition by negation, the spoken register, the stock phrases of generated Japanese | the same table's English negation row |
| natural-japanese | `lint.py` in the AI-smell and reading-load lanes, the naturalness score, a baseline rerun after the fixes | — |
| Morphology | `scripts/koyobun.py`. From 「公用文作成の考え方」: passive, clause chains, 漢字１字＋する and 等/など. House rules: clauses strung on 読点, conjunctive が, a lone たり, させていただく, 体言止め in body text and negated predicates. | — |
| Academic mode | `register.py --academic` over a second table of 47 rows, each citing its sources. The spoken register: でも, すごく, こんな, と思う and です・ます. 文語調: べく and ごとく. The over-stiff forms: することができる and を行う. `koyobun.py --academic` for って and たら. The rules a regex cannot find, read from `references/academic-japanese.md`. | — |
| vale | — | proselint: redundancy, corporate speak, jargon and hedging. [ai-tells](https://github.com/tbhb/vale-ai-tells): 137 rules for the signs of LLM-written English. They cover overused vocabulary, stock openers and closings, hedges, vague attributions and participial padding. They also cover copula dodges, transitions, figurative verbs and em dashes. `AISigns`: three house rules for the model talking about itself, emoji in headings, and five or more commas in one sentence. |

The register ships with twelve sample rows. Two catch definition by negation (`ではない`, `not X but Y`, `rather than` and related forms), which the skill rewrites to say what a thing is. Four catch the spoken register in a formal document. Six catch the stock phrases of generated Japanese that natural-japanese's catalogue lists but its lint leaves to the eye: hearsay with no source, breadth adjectives, outcomes named by an abstract noun, an intention softened with と思います, and the boilerplate opening and closing of a blog post.

Academic mode runs on a Japanese paper, thesis or report, when you ask for the register of one or when the text carries a reference list and 本研究 or 本稿. It rewrites spoken Japanese into the written register of a paper and holds it back from the stiff forms the same guides warn against. Every row and rule rests on sources read for it:

- 文化審議会「公用文作成の考え方」
- the writing guides of thirteen universities (東北大学, 金沢大学, 立教大学 and others)
- fourteen lab and faculty guides
- three academic societies' author guides
- six research papers, among them a survey of 1,900 written and spoken words in 63 books and papers on writing (柏野ほか 2016) and a BCCWJ measure of how hard connectives are (馬場 2018)

`references/academic-japanese.md` quotes the passage behind each rule, lists where the sources disagree and how the skill rules then, and gives every source with its URL.

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

It copies the textlint and vale configs to `~/.prose-lint` (or `$PROSE_LINT_HOME`), runs `npm install` and `vale sync` there (the sync pulls proselint and ai-tells from the vale package hub), and puts the sample registers at `~/.prose-lint/vocabulary.md` and `~/.prose-lint/academic.md`. The skill also runs this step itself when the linters are missing. Running it again refreshes `package.json`, the prh rule set, the fukushi dictionary and the AISigns style, and keeps a `.textlintrc*.json` or `.vale.ini` you have edited.

Requirements: Python 3.10+, [uv](https://docs.astral.sh/uv/), Node 20.18+ with npm for textlint, [vale](https://vale.sh/) 3.x for English, and natural-japanese. A missing tool skips its layer, and the report names it.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
textlint かけて: docs/手順書.md
check this English draft: README.md
AI っぽさを消して: docs/blog.md
論文調にして: thesis/chapter2.md
```

The skill settles the language, runs the layers for it, and replies with a report. For Japanese, the report gives the naturalness score first, then every finding by layer as fixed or kept with a reason, then the counts from the rerun after the fixes. For English, it gives the count of AI-sign hits per 1,000 words first, then the ledger, then the count that remains. It edits the document only where a finding holds, and never applies the linters' automatic fixes.

## Your register

`~/.prose-lint/vocabulary.md` is yours to edit. Each row is a regex, the wording to use instead, and the reason shown with each hit; the file's header gives the rules for a good row. Point `PROSE_LINT_REGISTER` at another file to keep it elsewhere. `~/.prose-lint/academic.md` is the academic register in the same format, with `PROSE_LINT_ACADEMIC_REGISTER` to move it; add a row for your field's or journal's house usage, and cite the source in the `Why` column the way the shipped rows do.

The kana rules live next to it in `~/.prose-lint/textlint/prh/koyobun-kana.yml`, one rule per line of the 訓令's appendix with a test for each guard; add a row there for a house spelling, or delete one that misfires on your house style. `~/.prose-lint/textlint/dict/fukushi.yml` is the adverb dictionary, the rule's own minus the five words the 訓令 keeps in kanji.

## Contents

| Path | Holds |
|---|---|
| `plugins/prose-lint/skills/prose-lint/SKILL.md` | The routing, the layers, the ruling on each finding id, the report |
| `plugins/prose-lint/skills/prose-lint/scripts/` | `register.py`, `koyobun.py`, `setup.py` |
| `plugins/prose-lint/skills/prose-lint/assets/textlint/` | `package.json`, the two configs, `prh/koyobun-kana.yml`, `dict/fukushi.yml` |
| `plugins/prose-lint/skills/prose-lint/assets/vale/` | `.vale.ini`, `styles/AISigns/` |
| `plugins/prose-lint/skills/prose-lint/assets/vocabulary.sample.md` | The sample register |
| `plugins/prose-lint/skills/prose-lint/assets/academic.sample.md` | The academic register |
| `plugins/prose-lint/skills/prose-lint/references/academic-japanese.md` | The academic rules, the passages they rest on, the disagreements and the source list |

## Considered and left out

Surveyed in September 2026 while choosing the layers above; listed so the choice can be revisited.

| Tool | Why not |
|---|---|
| textlint-rule-stop-words (2,000 words) | Overlaps ai-tells and flags ordinary verbs (accelerate, accompany); ai-tells gives a rewrite with each hit |
| textlint-rule-preset-ai-words-ja | Its list comes from one tech-blog corpus (走る, 壊れる, 経路); it fired on a human-written note and stayed silent on a generated one |
| textlint-rule-ja-hiraku | Opens 及び, 更に, 既に and the other words the 訓令 keeps in kanji; the four hiragana rules plus prh follow the 訓令 as written |
| textlint-rule-rousseau | Its checks duplicate write-good; per-sentence readability alone did not earn a layer |
| vale Readability, Microsoft, Google | Grade-level metrics and one company's style; neither says whether a person wrote the text |
| vale signs-of-ai-writing, LLMCliches, Slop | Smaller ports of the same Wikipedia list; ai-tells covers them and is in the vale hub |
| textlint-rule-preset-ja-engineering-paper | Deletes 非常に and 極めて outright, rewrites 又は, 基に and 挙げる against the 訓令, and forces 「，．」; its register ideas are cited in the academic register instead |
| Harper, LanguageTool | Grammar and spelling; a different job, and a Rust or Java install |
| RedPen, Just Right!, MS Word 校正, Enno, 文賢 | Dormant since 2021, or a GUI or web form with no CLI |

## Credits and licence

MIT.

- `koyobun.py` imports `textcore.py` from [natural-japanese](https://github.com/coji/natural-japanese) (MIT, coji) at run time. `SKILL.md` restates natural-japanese's naturalness-score formula and bands from its `references/diagnose.md` and points to its other reference files, and six register rows restate patterns from its `references/forbidden-patterns.md`. No code from it is copied here.
- `assets/vale/.vale.ini` pulls [ai-tells](https://github.com/tbhb/vale-ai-tells) (MIT, Tony Burns) through the vale package hub; nothing from it is copied here.
- `assets/textlint/dict/fukushi.yml` is the dictionary of [textlint-rule-ja-hiragana-fukushi](https://github.com/lostandfound/textlint-rule-ja-hiragana-fukushi) (MIT, lostandfound) with five entries removed.
- The academic register and `references/academic-japanese.md` restate rules from the university, lab, society and research sources listed in that file, with short quotations for citation; no text is copied beyond those quotations.
- The four 公用文 rules paraphrased in `SKILL.md` and `koyobun.py` come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html. The kana rules in `prh/koyobun-kana.yml` restate 「公用文における漢字使用等について」 (平成22年内閣訓令第1号).
