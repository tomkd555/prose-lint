---
name: prose-lint
description: Runs the wording linters on a file or pasted text and picks the ones the text's language calls for - for Japanese, textlint with the Japanese config (technical-writing and JTF presets, the AI-writing preset, the kana rules of 内閣訓令 through prh and the hiragana rules, い抜き・さ入れ・フィラー), a register of rejected wordings including definition by negation and the AI stock phrases, natural-japanese's lint in both lanes with its naturalness score and baseline rerun, and a sudachipy morphology lint (passive, clause chains, 漢字１字＋する and 等/など from 公用文作成の考え方; conjunctive が, lone たり, させていただく, body 体言止め and negated predicates as house rules); for English, textlint with the English config, the register's English negation row, and vale with proselint, the ai-tells package and two house rules for the signs of LLM-written text. Triggers on 「textlint かけて」「lint して」「lint 回して」「校正して」「表記チェック」「vale かけて」「否定形を消して」「否定で定義した文を直して」「AI っぽさを消して」, "run textlint", "lint this file", "proofread this", "check this English draft", "does this read as AI-written". Use it whenever the user names a linter or asks for a wording check on a document.
---

# Prose lint

Runs the linters over one text on demand, settles which config the text's
language calls for, and rules on every hit. Read `{SKILL_DIR}` below as the
absolute path of this skill's directory, and `{HOME}` as `$PROSE_LINT_HOME`, or
`~/.prose-lint` when that is unset.

## Step 0 - setup

`{HOME}/textlint/node_modules`, `{HOME}/vale/styles/proselint` and
`{HOME}/vale/styles/ai-tells` hold the installed linters. When any is missing,
run once:

```
uv run python {SKILL_DIR}/scripts/setup.py
```

It needs `npm` for textlint and `vale` on PATH for the vale packages, and
reports a missing tool as `skip`. A layer whose tool is missing is reported as
skipped in the final report; the other layers still run. The Japanese
morphology and natural-japanese layers need `uv` and the natural-japanese
plugin (`/plugin marketplace add coji/natural-japanese`, then
`/plugin install natural-japanese@natural-japanese`); `uv run {SKILL_DIR}/scripts/koyobun.py --nj-dir`
prints the directory it found, written `{NJ}` below.

## Step 1 - settle the target

A path in the request is the target. Pasted text goes to a `.md` file in a
temporary directory first, because textlint, vale and the scripts all read
files.

With no path given and no file in play from the conversation, ask which text to
lint.

## Step 2 - route by script

Hiragana over 10% of the non-whitespace body means Japanese, otherwise English:

```
uv run python -c "import re,sys;t=open(sys.argv[1],encoding='utf-8').read();b=len(re.sub(r'\s','',t));print('ja' if len(re.findall('[ぁ-ゟ]',t))*10>b else 'en')" <file>
```

It counts hiragana alone on purpose: the Japanese an English document quotes is
terminology - kanji and katakana, almost no hiragana - so an English document
holding a dozen Japanese terms still routes to English.

A mixed document runs once, under its majority language. Findings that land on a
quotation in the other language get dropped.

## Step 3a - Japanese

Four mechanical layers, then the review. Each layer reports suspicions; the
ruling on each hit is yours and goes in the report.

### textlint

```
{HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.json <file>
```

textlint exits 1 when it finds anything, so read the output and ignore the exit
code. The findings fall in three tiers by rule id:

- Blocking - fix these: `no-ai-hype-expressions`, `ai-tech-writing-guideline`,
  `ja-no-weak-phrase`, `ja-no-redundant-expression`, `ja-no-abusage`,
  `ja-no-successive-word`, `no-doubled-conjunctive-particle-ga`,
  `no-double-negative-ja`, `no-dropping-the-ra`, `@textlint-ja/no-dropping-i`,
  `@textlint-ja/no-insert-dropping-sa`, `@textlint-ja/no-filler`,
  `no-mix-dearu-desumasu`, and the kana rules: `ja-keishikimeishi`,
  `ja-hiragana-hojodoushi`, `ja-hiragana-daimeishi`, `ja-hiragana-fukushi`
  and `prh`. The four hiragana rules and prh together restate 「公用文における
  漢字使用等について」(平成22年内閣訓令第1号) 別紙: prh carries the
  conjunctions, auxiliaries and the fixed phrases of its item キ (但し, 出来る,
  様に, 通り, 致します and the rest), and each prh message names the item it
  comes from. The fukushi dictionary is the rule's own minus the five words the
  訓令 keeps in kanji (更に, 既に, 最も, 僅か, 若しくは). A kana rule firing on
  a proper noun, a legal term or a quotation is kept, with that reason.
- Advisory - each needs judgement: `no-doubled-joshi`, `no-doubled-conjunction`,
  `sentence-length` (90 characters), `max-ten`, `max-kanji-continuous-len`. A
  particle repeated in a plain list holds; the conjunctive が repeated in one
  sentence gets fixed. Fix the ones that hold and say why the others stay.
- Notation - every other rule: punctuation, spacing, numerals. Leave them alone
  unless the user asks for notation.

### The register

```
uv run {SKILL_DIR}/scripts/register.py <file>
```

The register is a Markdown table of rejected wordings: `$PROSE_LINT_REGISTER`,
else `{HOME}/vocabulary.md`, else the sample in `assets/`. The script prints
which one it read. The sample carries twelve rows in three groups.

- Definition by negation, two rows. The Japanese row on `ではない` also covers
  `でない`, `じゃない`, `に当たらない`, `該当しない` and `非該当`; the English
  row covers `not X but Y`, `X, not Y`, `rather than`, `instead of` and
  `not applicable`. Two forms stay: quoted text, and a verb plainly negated.
  Every other hit gets rewritten: say what the thing is; where the sentence
  draws a boundary, name what falls inside it; where it corrects a wrong idea,
  state the right one and leave the wrong one out. Write the sentence a
  business document would carry, in the words of the text around it; a
  template sentence reads as translation.
- The spoken register, four rows: なので and だから at a sentence start, 一番
  before an adjective, ほぼ全部. Rewrite in a formal document; a quotation or
  a deliberately casual text keeps them.
- The stock phrases of generated Japanese, six rows, each on a pattern that
  natural-japanese's catalogue lists but its lint leaves to the eye: hearsay
  with no source (と言われています, とされています, という声もあります),
  breadth adjectives that stand in for a list (様々な, 多様な, 幅広い),
  outcomes named by an abstract noun (を実現, に寄与, シームレス, 最適化), an
  intention softened with と思います, the closing ぜひ〜してみてください, and
  the opening 今回は〜について紹介します. Rewrite each as the row says: name
  the source or own the claim, list the items, say what changes, say it
  plainly, delete the boilerplate. A hit inside a quotation stays.

The regex reaches the surface forms only. The `negated_predicate` id of the
morphology lint below lists every sentence whose final predicate is negated;
read each one and rewrite the ones whose whole content is a denial:
「〜とは限らない」, 「〜するわけがない」, 「〜を含まない」, 「〜せず」 or
「〜しない」 used to define a thing or to draw its boundary, and a clause that
names only what something lacks. The other rows are handled as the register
says: kept when the wording fits the context and the reason is stated, otherwise
rewritten.

### natural-japanese lint

```
uv run {NJ}/lint.py --genre business --reading-load --json <file> > <tmp>/nj-1.json
```

`--genre business` selects natural-japanese's business profile, which mainly
switches off detectors that misfire on bullet-heavy business documents. The JSON goes to a temporary file so it serves twice: it is
the ledger the report rules on, and the baseline for the second run below. Two
lanes come out.

- The AI-smell lane: banned phrases, translationese, uniform sentence length,
  the 体言止め rate, paragraph-opening conjunctions, lexical variety. Judge each
  hit against the section for its category in the natural-japanese skill's
  `references/revision-guide.md`. Its antithesis detector counts `ではなく` and
  `だけでなく…も` across the document, fires at three occurrences, and sets the
  severity by their share of all sentences.
- The reading-load lane (`--reading-load`): a sentence over 90 characters, a
  buried enumeration, a kanji run, a double negative, a chain of の. Judge each
  hit against `references/readability-antipatterns.md`, catalogue A to J,
  applied from A. A split sentence that grows longer is a correct result.

Three more pieces of natural-japanese come in here.

- **The naturalness score.** From the JSON, count the AI-smell findings by
  severity and apply the formula and bands from natural-japanese's
  `references/diagnose.md` (by coji). This skill leaves the reading-load lane
  out of the count. Deduction = (critical×8 + warn×4 + info×0.5) ×
  (1000 / max(characters, 1000)); score = max(100 − deduction, 20). The bands
  are 90+ natural, 70–89 light, 50–69 needs work, under 50 heavy. Put the score
  and the band at the head of the report as a one-line summary, and say that it
  is the quick tier of that skill's diagnosis, with no judgement adjustment.
  The score varies between runs, so read it as a direction.
  Under 100 characters of body the score is skipped.
- **The skeleton.** For a document with headings and over about 3,000
  characters, run `uv run {NJ}/outline.py <file>` and read the headings and
  paragraph leads it prints in one pass: whether the line of argument holds from
  headings alone, whether each heading is a message, and whether sections repeat
  one template. Those findings join the ledger.
- **The second run.** After the fixes are applied, run lint.py again with
  `--baseline <tmp>/nj-1.json`. It sorts findings into resolved, new and
  persisting; a `new` finding is a fix that introduced a fresh smell, and it goes
  back into the ledger. The report states the three counts.

### 公用文 morphology lint

```
uv run {SKILL_DIR}/scripts/koyobun.py <file>
```

This script checks rules that turn on parts of speech, which no surface-string
linter sees. Four come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07,
https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html);
the rules below paraphrase its items. Five are house rules of this skill,
marked as such, three of them leaning on an item of the 建議. It tokenises
with sudachipy, on the same sentence split and Markdown mask lint.py uses, and
reports one line per suspicion. Each id carries its rule and its ruling:

- `passive` (Ⅲ-3 ケ, use the passive sparingly): れる/られる after a verb. The
  form is shared with 可能, 尊敬 and 自発, so read each hit. Rewrite when the
  agent is known and the active sentence reads naturally; keep a passive whose
  agent is unknown or beside the point.
- `clause_chain` (Ⅲ-3 カ, avoid long chains of conjunctive particles and
  continuative forms): three or more 接続助詞 or 連用中止 in one sentence; the
  threshold of three is this skill's. Split at the joint where the topic
  changes.
- `kanji_suru` (Ⅱ-8, limit verbs made of one kanji and する): a verb of that
  shape. The 建議 gives 模する, 擬する, 賭する and 滅する as examples, with
  似せる, なぞらえる, 賭ける and 滅ぼす as rewrites. This skill exempts 関する,
  対する and 際する, which work as particles. Rewrite with a native verb or a
  two-kanji compound; a legal term of art stays.
- `etc` (Ⅱ-5 イ, use 等 and など with care): every occurrence. The 建議 asks
  the writer to have the full content in mind and to put representative,
  typical items before 「等」「など」; check that each occurrence does.
- `ga_conjunction` (house rule, after Ⅲ-3 カ): every が used as a 接続助詞,
  with the words before it. The 建議 asks the writer not to string clauses on
  接続助詞; this check lists each が so that the ones that join two clauses
  with no contrast (「説明しますが、」, 「検討したが、」 before a result) get
  cut into two sentences or rewritten with ので or ため. A が that marks a real
  contrast stays, and the report says so.
- `tari_single` (house rule): a sentence with one たり and no partner.
  Standard usage pairs it (読んだり書いたりする); rewrite with the pair, or
  without たり (読むなどして). A たり that closes a list on purpose stays.
- `sasete_itadaku` (house rule, after Ⅱ-6 ウ): させていただく. The 建議 asks
  for 敬語 to be used as needed and not piled up; させていただく asks the reader's
  leave, so it stays only where leave is being asked. Elsewhere write します or
  いたします.
- `nominal_ending` (house rule: 体言止め only in headings and list items, after
  JTF 日本語標準スタイルガイド 1.1.2 and 1.1.3): a body sentence whose last content
  word is a noun. Headings, list items, tables and quotes are masked, so every
  hit is in running text; finish the sentence with a predicate. A label before
  a colon or a table-like paragraph laid out on purpose stays.
- `negated_predicate` (house rule: say what a thing is): the final predicate
  carries ない, ぬ or ません. This is the mechanised form of the second reading
  the register section asks for.

`--json` gives the same findings for the ledger.

### The review

Read the text once yourself for what no script decides: whether each paragraph serves the
document's purpose, whether terms stay consistent from start to end, and
whether the conclusion comes first.

## Step 3b - English

Three mechanical layers, then the review.

### textlint

```
{HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.en.json <file>
```

The English config covers write-good, terminology, a 40-word sentence cap,
duplicated conjunctions at the start of consecutive sentences, and two
Markdown-shape rules of the AI-writing preset, `no-ai-list-formatting` (a
bullet that opens with a bold label and a colon, an emoji bullet) and
`no-ai-emphasis-patterns` (bold inside a heading, an emoji before a bold
label). Those two report in Japanese; restate the finding in English in the
report. All of these are fixed when they hold.

### vale

```
vale --config {HOME}/vale/.vale.ini <file>
```

Three styles run: proselint (redundancy, corporate speak, jargon, hedging),
`ai-tells` (https://github.com/tbhb/vale-ai-tells, the signs of LLM-written
English, 137 rules), and `AISigns`, two house rules shipped in
`assets/vale/styles/AISigns` for what ai-tells leaves out: the model talking
about itself or a token pasted from a chat interface (`AISigns.Chatbot`), and an
emoji in a heading or list item (`AISigns.Emoji`). vale exits 1 on any finding.
Every ai-tells rule is `error`, so the tier comes from the message's opening
words, which name the family:

- Fixed - the families that name a stock phrase, a filler or a chat artefact:
  `AI closing`, `AI opening`, `AI sycophancy`, `AI hedge`, `AI stacked hedge`,
  `AI conclusion`, `AI vague attribution`, `AI copula dodge`, `AI participial
  padding`, `AI transition`, `AI overused word`, `AI vocabulary`, `AI cliché`,
  `AI puffery`, every `AI ... heading`, `AI structure announcement`,
  `AI metacommentary`, `AI restatement`, `AI empty modifier`, `AI intensifier`,
  `AI quantity metaphor`, `AI list intro`, `AI label-and-explain`,
  `AI sequencing`, `AI contrast`, `AI contrast by negation`, `AI strawman
  contrast`, `AI stilted negation`, `AI stacked absence`, `AI negated subject`,
  `AI evasion`, `AI strategy buzzword`, and both AISigns rules. Fix them; a hit inside a quotation or on
  a term of art stays, with that reason.
- Advisory - the families that name a figure of speech, a rhythm or a
  punctuation mark, which human writers also use: `AI overused verb` (the
  Figurative rules), every `AI ... metaphor`, `AI figurative noun`,
  `AI punctuation` (an em dash is a sign only when a paragraph holds three or
  more; a capital after a colon is a style choice), `AI tricolon`, `AI staccato`,
  `AI noun string`, `AI numbered lead-in`, `AI rhetoric`, `AI rhetorical
  self-answer`, `AI mic-drop`, `AI pseudo-cleft`, `AI anthropomorphism`,
  `AI anthropomorphic adjective`, and proselint. Fix the ones that hold and say why the others stay.

Two ai-tells rules that police one project's own wording (`HouseStyle`,
`ShipOveruse`) are switched off in the shipped `.vale.ini`.

### The register

Run `register.py` on the file. Its English negation row is the only linter
that carries the rule on definition by negation; the Japanese rows find nothing
in English text. Rewrite each hit the same way as in Step 3a.

### The review

With the `elements-of-style:writing-clearly-and-concisely` skill installed
(https://github.com/obra/the-elements-of-style), invoke it for the judgement
layer; without it, read for needless words, passive voice that hides the actor,
and vague nouns yourself. Then read once for the signs no regex catches:
three items where two or four were the truth, a paragraph that opens with a
claim and closes with its restatement, headings that all take the same shape,
a document that agrees with the reader, and a synonym cycled to avoid repeating
a name.

## Reporting

- **Report every finding as fixed, or as kept with a stated reason.** A hit is a
  suspicion, and the reason a wording stays is part of the report.
- **Never rewrite the user's text silently, and never mass-apply the lint
  output.** A run over a long document produces more hits than problems, and
  applying them wholesale flattens prose the user wrote deliberately. `textlint
  --fix` is off the table for the same reason.
- For Japanese, open with the naturalness score and its band, then the ledger
  by layer, then the second run's resolved / new / persisting counts. A score
  alone says nothing about the register hits, so it never replaces the ledger.
- For English, open with one line: the count of ai-tells and AISigns hits and
  the count per 1,000 words, from the vale run before the fixes (`vale
  --output line` piped to a count of lines holding `ai-tells` or `AISigns`,
  over `wc -w`). It is a direction, like the naturalness score, and never
  replaces the ledger. After the fixes, run vale again and state the count
  that remains.
- Name every layer that was skipped and the tool it lacked.
- Report in Markdown in the reply.
