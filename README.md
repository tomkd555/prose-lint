# prose-lint

A Claude Code skill that runs the wording linters over one document, picks the configs its language calls for, and rules on every hit as fixed or kept with a reason. Japanese goes through four linters and a closing read-through; English through three linters and a closing read-through. Both sides carry a layer for the signs of LLM-written text, so a draft comes back reading as one person wrote it.

| Layer | Japanese | English |
|---|---|---|
| textlint | ja-technical-writing, JTF style and AI-writing presets; the kana rules of 内閣訓令 (four hiragana rules and a prh rule set, `assets/textlint/prh/koyobun-kana.yml`); い抜き, さ入れ and フィラー; the skill sorts findings into blocking, advisory and notation | write-good, terminology, a 40-word sentence cap, duplicated conjunctions at sentence starts, and the AI-writing preset's two Markdown-shape rules (bold-label bullets, emoji bullets, bold in headings) |
| Register | `scripts/register.py` over a Markdown table of rejected wordings that you grow one row at a time: definition by negation, the spoken register, the stock phrases of generated Japanese | the same table's English negation row |
| natural-japanese | `lint.py` in the AI-smell and reading-load lanes, the naturalness score, a baseline rerun after the fixes | — |
| Morphology | `scripts/koyobun.py`: passive, clause chains, 漢字１字＋する and 等/など from 「公用文作成の考え方」; conjunctive が, a lone たり, させていただく, 体言止め in body text and negated predicates as house rules | — |
| vale | — | proselint (redundancy, corporate speak, jargon, hedging); [ai-tells](https://github.com/tbhb/vale-ai-tells), 137 rules for the signs of LLM-written English (overused vocabulary, stock openers and closings, hedges, vague attributions, participial padding, copula dodges, transitions, figurative verbs, em dashes); `AISigns`, two house rules for the model talking about itself and emoji in headings |

The register ships with twelve sample rows. Two catch definition by negation (`ではない`, `not X but Y`, `rather than` and related forms), which the skill rewrites to say what a thing is. Four catch the spoken register in a formal document. Six catch the stock phrases of generated Japanese that natural-japanese's catalogue lists but its lint leaves to the eye: hearsay with no source, breadth adjectives, outcomes named by an abstract noun, an intention softened with と思います, and the boilerplate opening and closing of a blog post.

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

It copies the textlint and vale configs to `~/.prose-lint` (or `$PROSE_LINT_HOME`), runs `npm install` and `vale sync` there (the sync pulls proselint and ai-tells from the vale package hub), and puts the sample register at `~/.prose-lint/vocabulary.md`. The skill also runs this step itself when the linters are missing. Running it again refreshes `package.json`, the prh rule set, the fukushi dictionary and the AISigns style, and keeps a `.textlintrc*.json` or `.vale.ini` you have edited.

Requirements: Python 3.10+, [uv](https://docs.astral.sh/uv/), Node 20.18+ with npm for textlint, [vale](https://vale.sh/) 3.x for English, and natural-japanese. A missing tool skips its layer, and the report names it.

## Usage

Ask Claude Code to lint a document, with its path or with the text pasted in:

```
lint docs/proposal.md
textlint かけて: docs/手順書.md
check this English draft: README.md
AI っぽさを消して: docs/blog.md
```

The skill settles the language, runs the layers for it, and replies with a report: for Japanese, the naturalness score first, then every finding by layer as fixed or kept with a reason, then the counts from the rerun after the fixes; for English, the count of AI-sign hits per 1,000 words first, then the ledger, then the count that remains. It edits the document only where a finding holds, and never applies the linters' automatic fixes.

## Your register

`~/.prose-lint/vocabulary.md` is yours to edit. Each row is a regex, the wording to use instead, and the reason shown with each hit; the file's header gives the rules for a good row. Point `PROSE_LINT_REGISTER` at another file to keep it elsewhere.

The kana rules live next to it in `~/.prose-lint/textlint/prh/koyobun-kana.yml`, one rule per line of the 訓令's appendix with a test for each guard; add a row there for a house spelling, or delete one that misfires on your house style. `~/.prose-lint/textlint/dict/fukushi.yml` is the adverb dictionary, the rule's own minus the five words the 訓令 keeps in kanji.

## Contents

| Path | Holds |
|---|---|
| `plugins/prose-lint/skills/prose-lint/SKILL.md` | The routing, the layers, the ruling on each finding id, the report |
| `plugins/prose-lint/skills/prose-lint/scripts/` | `register.py`, `koyobun.py`, `setup.py` |
| `plugins/prose-lint/skills/prose-lint/assets/textlint/` | `package.json`, the two configs, `prh/koyobun-kana.yml`, `dict/fukushi.yml` |
| `plugins/prose-lint/skills/prose-lint/assets/vale/` | `.vale.ini`, `styles/AISigns/` |
| `plugins/prose-lint/skills/prose-lint/assets/vocabulary.sample.md` | The sample register |

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
| Harper, LanguageTool | Grammar and spelling; a different job, and a Rust or Java install |
| RedPen, Just Right!, MS Word 校正, Enno, 文賢 | Dormant since 2021, or a GUI or web form with no CLI |

## Credits and licence

MIT.

- `koyobun.py` imports `textcore.py` from [natural-japanese](https://github.com/coji/natural-japanese) (MIT, coji) at run time. `SKILL.md` restates natural-japanese's naturalness-score formula and bands from its `references/diagnose.md` and points to its other reference files, and six register rows restate patterns from its `references/forbidden-patterns.md`. No code from it is copied here.
- `assets/vale/.vale.ini` pulls [ai-tells](https://github.com/tbhb/vale-ai-tells) (MIT, Tony Burns) through the vale package hub; nothing from it is copied here.
- `assets/textlint/dict/fukushi.yml` is the dictionary of [textlint-rule-ja-hiragana-fukushi](https://github.com/lostandfound/textlint-rule-ja-hiragana-fukushi) (MIT, lostandfound) with five entries removed.
- The four 公用文 rules paraphrased in `SKILL.md` and `koyobun.py` come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07), https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html. The kana rules in `prh/koyobun-kana.yml` restate 「公用文における漢字使用等について」 (平成22年内閣訓令第1号).
