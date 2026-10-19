# Translationese and style fit in Japanese

The material the reader in Step 3a works from. It names each marker of
Japanese that reads as translated from English, gives the test that decides
whether a sentence carries it, and gives the rewrite for each style the skill
settles in Step 2. `assets/translationese.sample.md` holds the few forms a
regex can find; everything else here needs the sentence and the document
around it.

Every source in section 6 was fetched on 2026-10-16, and the Microsoft guide
again on 2026-10-19 at its current build. Each quotation carries
its source's short name in 〔〕, the key the register rows and this file cite,
and section 6 gives the URL to check it against.

## 1. Why the reading carries this layer

A marker is a question to ask of a sentence, and the answer depends on the
document. Three findings point that way.

- The corpus evidence is narrow. In translated against original Japanese
  fiction, only two features held: "Two features (third person pronouns and
  longer paragraphs) are shown to be characteristic of translationese"
  〔Meldrum2009〕. Abstract nouns as subjects of transitive verbs and loanwords
  did not hold there. A translation scholar's column on Meldrum's 2009 article
  in 翻訳研究への招待 covers four of the features tested (代名詞, カタカナ語,
  女性語, 無生物主語) and concludes:
  「代名詞の頻繁な使用以外は実は、翻訳調の特徴とも言い切れないようです。」
  〔山田2020〕
- Some forms traced to English are now ordinary written Japanese. 形式名詞
  「点」, attested from 江戸後期, spread once it took on the senses of English
  *point*: 「英語pointの多義性を「点」が引き受けたことで、明治期以降形式名詞と
  して盛んに用いられた。」〔奥山2026〕
- Inanimate-subject transitive sentences occur in native Japanese corpora.
  Natural-autonomy nouns combine with a wide range of verbs: 「「風」のような
  「自然自律」タイプの名詞は，「受影性」の高いものから低いものまで幅広い動詞と
  結びついて連語を作っている」〔麻2016〕. In a Japanese-Chinese comparison, the
  Japanese examples stand out in textbook science explanations:
  「日本語では「教科書」における科学原理の説明が目立つのに対し」〔麻2024〕.
- Measured for this skill (section 4), several classic surface forms are
  common in human-written business and technical prose: において in 47 of 83
  documents, を行う in 52.

So the reader asks of each sentence what a Japanese colleague in the
document's field would have written, and flags the sentence when the answer
differs because of an English source.

## 2. The test for each sentence

1. **Back-translation.** Name the English word or phrase the writer was
   rendering. When the sentence makes sense only through that English word's
   sense, it is translationese. Microsoft's guide states the general rule:
   "To be more fluent translation, word-to-word translation should be
   avoided." "Strict word-to-word translation would make the tone stiff and
   unnatural." 〔Microsoft〕 §2.1.4
2. **Sense.** Check that the Japanese word carries the sense used. A
   translation company's column notes that 「英語の「provide」や「offer」という
   動詞は、「提供する」と訳されがちです」, and shows 提供する in a sense its
   dictionary entry lacks: 「もちろん、MWCは製品発表以外にも多くのことを提供
   する。」 becomes 「もちろん、製品発表以外にも多くの見どころがある。」
   〔川村2019〕
3. **Actor.** Find who does the act in Japanese. A thing, a value or a rule
   given a person's act is the commonest frame (section 3.2,
   `inanimate-subject`).
4. **Field and reader.** Ask what the reader's field writes. 「まずは想定読者を
   意識したうえで意味が伝わるかを考える。」〔インターブックス〕 For a UI term,
   the product's existing UI translations decide: 「まずこのUIの対訳集を検索
   し、一致した訳を使用する」〔川村2020〕.
5. **Style.** Check the sentence against the 文体 and the words the style line
   settled (section 3.3).

A rewrite starts from the meaning. Say in plain Japanese what the sentence
asserts and who acts, then find the words, as if the content had been
Japanese from the start.

## 3. Markers

Each marker has an id for the reader's findings, what it looks like, the test,
the rewrite, and when the form stays.

### 3.1 Words

**`sense`** - a word picked as the dictionary match of an English word, used
in a sense the Japanese word does not carry: 提供する for *provide* or *offer* in
「多くのことを提供する」〔川村2019〕, or a noun whose own senses fit nothing in
the sentence. Test: look the word up and find the sense used. Rewrite: say the
meaning plainly, then pick the word whose entry lists it; where no single word
fits, write the phrase.

**`field-term`** - a dictionary rendering where the reader's field has its own
term, or a fresh rendering of a term the product already fixes. Microsoft's
rule: "Use approved terminology from Microsoft Terminology - Globalization |
Microsoft Learn where applicable" 〔Microsoft〕 §2.1.3. The 建議 keeps
established loanwords:
「こうしたものは、ほかの言葉に言い換えるよりもそのまま用いる方が良い。」
〔公用文〕 Ⅱ-3. Rewrite in `business` and `paper`: the field's term in the
form the field writes it, katakana included. In `official` and `article`, use
the term the reader knows; where the reader may not, write the 建議's paraphrase
or the term with a short gloss.

**`katakana`** - a katakana word where an established Japanese word says the
same to this reader. The 建議 decides case by case: 「外来語は、語の性質や使う
場面に応じて対応を判断する」〔公用文〕 Ⅱ-3, with paraphrases such as アジェンダ
→ 議題 and サプライヤー → 仕入先. SmartHR goes further: 「カタカナ語を一切使用
しないことは現実的ではありませんが、安易に使用しないようにしましょう。」
〔SmartHR〕 One checker at a translation company writes
「個人的には漢字熟語などで代替可能と判断したらそれを優先したい。」, and in the same
paragraph 「実際には、よほど不自然でなければカタカナ語で良しとすることもある」.
The post follows a past translation's wording and the katakana a client
specifies, and weighs 「一般的に使われている言葉か専門分野の用語か」〔インターブックス〕.
Rule by the style's reader (section 5, D5).

**`comparative`** - より with an adjective and no object of comparison:
「「より大きい」「より悪い」というのは発明された翻訳調なので日本語としては不自然
です。」〔関西大CogLab〕 Rewrite: name what is compared, or state the change with a
verb (増えた, 上がった). 10 of the 83 human documents use より with an
adjective, among them より良い方向 and より少ない輸入代金 (section 4). The
skill's ruling: a set phrase of that kind stays.

### 3.2 Frames

**`inanimate-subject`** - a product, program, value, rule or abstract noun
made the agent of a transitive verb, or given a person's act or feeling.
The definition: 「抽象概念や自然現象など、
人間や動物以外の主語が動作をする＝無生物主語です。」〔関西大CogLab〕 The guides:
"In general, do not literally translate inanimate subject (such as product,
program and device) as the agent of action unless it is necessary. Use
passive voice and omit the subject instead." 〔Microsoft〕 §4.2;
「無生物はなるべく主語としないようにしてください。」〔Red Hat〕 §7.5;
「英語では無生物主語が用いられますが、日本語訳時にそのまま無生物主語を使う
と、違和感を抱かせる訳文になることあります。」〔GDI〕 A questionnaire across 13
languages found "The Japanese language has a strong tendency to avoid
inanimate subjects", and states the conditions that hold across the
languages: "Crosslinguistically, inanimate subjects are unacceptable under the
condition that the inanimate subject is the direct actor and the object is
affected." "On the other hand, inanimate subjects are acceptable under the
condition that the action is indirect and the inanimate subject is a trigger
of human emotion or something similar." 〔風間2016〕

The rewrite depends on the style:

| Style | Rewrite | Example |
| --- | --- | --- |
| `business`, a manual, with a verb of allowing, enabling or helping | the user's act as a condition, then a potential form | 「この機能はユーザーにデータ出力を可能にします。」 → 「この機能を使用すると、データを出力できます。」〔Manual Hub〕 |
| `business`, a manual, with a verb of improving or preventing | the result, or the cause and then the result | 「更新プログラムがシステム安定性を改善しました。」 → 「更新後、システムの安定性が向上しました。」; 「エラーがアプリケーションの起動を妨げました。」 → 「エラーにより、アプリケーションを起動できませんでした。」〔Manual Hub〕 |
| `business`, a step the computer does | a passive with the subject dropped, where the computer acts from the user's view | "In general, use active voice when the agent of action is person (user). Use passive voice when the action is automatically performed by computer from user's point of view." 〔Microsoft〕 §4.2 |
| `business`, a specification | the actor stays as subject | 「仕様書や法務寄りの文書では、「システムが〜」「本製品は〜」「アプリケーションが〜」のように、動作主体を明示した方が適切な場合があります。」〔Manual Hub〕 |
| any, a cause or condition | 「〜で」「〜の場合」「〜により」 and an intransitive verb | 「この関数を呼ぶことはメモリー不足を発生させます。」 → 「この関数を呼んだ場合、メモリー不足が発生します。」〔GDI〕; 「台風で13人が死んだ」〔関西大CogLab〕 |
| any, a finding | what was found as the predicate | 「この事実は、従来の前提が誤っていたことを示している。」 → 「この事実から、従来の前提が誤っていたと分かる。」〔natural-japanese〕 |

Red Hat keeps the active form where it is clearer:
「ただし、無生物の場合でも単刀直入の方がわかりやすい場合には能動態を使う場合も
あります。」〔Red Hat〕 §7.6. Manual Hub keeps UI text and feature descriptions
such as 「この機能は、一時ファイルを自動的に削除します。」, while Red Hat rewrites
a command's description of the same shape into a passive with により (section
5, D2). Corpus studies find natural-force subjects with many verbs 〔麻2016〕,
and inanimate-subject transitive sentences standing out in textbook science
explanations 〔麻2024〕; 関西大CogLab still rewrites
「台風が13人を殺した」 as 「台風で13人が死んだ」. Section 5, D2 gives the ruling.

**`pronoun`** - 彼, 彼女, 彼ら, あなた, 私たち, and それ standing for *it*.
Third-person pronouns are one of the two features that held in Meldrum's
corpus 〔Meldrum2009〕. The column on her work adds:
「「彼」の回数はあまり変わらないのに、「彼女」「彼ら」の使用頻度は「翻訳テクスト」
でとても多い」, and gives 「「He met his girlfriend」が「彼は彼の彼女に会った」と
訳されると、いかにも翻訳調に感じるでしょう。」〔山田2020〕 A study of
English-to-Japanese machine translation states that a well-formed, natural
sentence needs the English pronoun handled 「英語の代名詞を日本語の代名詞として
そのまま表現せず」, by dropping or replacing it 〔吉見2001〕. Microsoft, on *you*
and *I*: "the overuse of these pronouns will lead to unnatural text" §2.1.3;
on *we*: "First person plural pronoun (we, our) should be omitted in most
cases." §4.1.8; on 彼 and 彼女: "Don't use gendered pronouns (彼, 彼女 etc.)
in generic references." §3.1, which offers the second person or a role noun in
their place 〔Microsoft〕. Rewrite: drop it, or name the role
(利用者, 管理者, 担当者) or the person. A contract shows the drop:
「買主は全情報を秘密にしなければならず、他人に見せてはならない」〔ケースクエア〕.
It stays for a real person, "when you're writing about real people who use
those pronouns themselves." §3.1, and where "Usage of "あなた" is acceptable
depending on the context." §4.1.8 〔Microsoft〕.

**`subject-first`** - a stated subject at the head of sentence after sentence
(私は, このシステムは, オブジェクトは) where Japanese leaves it to context.
"For Japanese, firstly consider the omission of subject because it is often
unnatural to express it explicitly." 〔Microsoft〕 §4.1.8;
「主語で始まる日本語を見ると、英語翻訳っぽさが強くなるので避ける」〔清水川〕.
The limit is the 建議's: 「主語と述語の関係が明らかに分かるようにする。」
〔公用文〕 Ⅲ-3 オ. Drop a subject only where the reader can still recover it.

**`can`** - 〜が可能です, 〜することが可能である, 〜することができる. Microsoft
lists "xxx が可能です" under the forms to avoid, with できます in its place
〔Microsoft〕 §2.1.2. 「しかし、この表現は「can」の直訳です。」〔谷口2010〕, with
「このシステムでは、顧客データと購入データを一括管理できる。」 as the rewrite;
its second page adds 「「する事が出来る」という表現は、シンプルに「できる」と修正し
ましょう。」〔谷口2010〕. 「ユーザーに簡潔明瞭に伝えるため、「することができる」
などの冗長な表現は極力避けましょう。」〔SmartHR〕 The 建議 lists the same
rewrite among 「回りくどい言い方や不要な繰り返しはしない」: 「利用することができる→
利用できる」〔公用文〕 Ⅱ-5. Rewrite to できる where it says the same in the
style's 文体; 26 of the 83 human documents use a form the row matches
(section 4), so the
register puts the row in the group read in context. natural-japanese's
reading-load lane already lists 〜ことができる as wordiness; rule on it once.

**`by-means`** - 〜することにより, 〜によって for *by ~ing*. Microsoft lists
"xxxx することにより、xxxx によって" under the forms to avoid, with すると and
すれば in its place 〔Microsoft〕 §2.1.2. A column on translating passives
turns 「酢酸エチルを加水分解することにより酢酸が製造される。」 into
「酢酸エチルを加水分解して酢酸を製造する。」. For another sentence it prefers
「酢酸エチルを加水分解することにより酢酸が生成する。」, a choice it bases on the
verb 生成 and in which the form stays 〔ミドリ〕. Rewrite with して, すると or
すれば where the sentence reads the same; the form stays where the plainer one
does not fit, as in that example.

**`have`** - 〜を持つ with an abstract object, 〜を提供する or 〜で構成される
with a thing as subject, 〜に存在する before a noun. The @IT exercises call
such sentences grammatical but translated: 「下記の文章は、日本語としては問題
ありませんが、翻訳調のため多少読みにくくなっています。」〔谷口2010〕 Its answers:
「このシステムは以下の3つの機能を提供する。」 → 「このシステムの機能は以下の3つ
である。」; 〜という値を持つ → 「システム起動時には“価格”属性の値は0である。」;
〜に存在する問題点 → 「対象となる業務の問題点をリストアップする。」 Rewrite with
ある, である or の.

**`light-verb`** - a noun with 〜を実行する or 〜を行う where the verb says it.
Microsoft's rule makes the verb the default: "In general, use "～します"
instead of "noun + を実行します (行います)" unless it becomes wordy." Its table
rewrites 「アプリケーションのインストールを実行します。」 as
「アプリケーションをインストールします。」. Where the verb form would be wordy, as
with three verbs, it keeps 「行の追加、移動、または削除を行います。」. It also
keeps a katakana noun as a noun: "don't convert katakana nouns to verbs unless
such verbs are already common and familiar in Japan." 〔Microsoft〕 §4.1.12.
SmartHR lists 削除を行う as the form to avoid, with 削除する 〔SmartHR〕. 29 of
the 83 human documents use 〜の〇〇を行う (section 4), so the reader flags the
light verb only where the verb form says the same without growing wordy.

**`passive`** - an agent passive (〜によって〜される) or a passive that hides
who acts. 「受身形の表現は、文の構造を難しくしたり責任の所在を曖昧にしたりする
場合がある。」〔公用文〕 Ⅲ-3 ケ. It stays where 「行為の主体を示す必要がない場合
や、行為の対象や目的を目立たせるのに、受身形の使用が効果的な場合もある。」
〔公用文〕, and for what the computer does in a UI (`inanimate-subject`).

**`no-chain`** - の stacked because an English noun phrase was kept whole:
「この様に、名詞が中心の英文をそのまま和文に翻訳してしまうと、必然的に『の』が
増えてしまうのです。」〔ISS〕 The 建議: 「「の」「に」「も」「て」などの助詞を
連続して使うと、文が長くなるだけでなく稚拙な印象を与えてしまうおそれがある。」
〔公用文〕 Ⅲ-3 キ. Rewrite with a verb: 「被験薬をヒトに初めて投与する臨床試験で
のリスクを特定し、軽減するための戦略に関するガイドライン」〔ISS〕.

**`prenominal`** - a long relative clause carried in front of its noun.
「ただし、長い修飾節を含む文は、文を分けることで、より読みやすくなることが
多い。」〔公用文〕 Ⅲ-3 ク. Split it: 「新しいソフトウェアが先月リリースされまし
た。」「このソフトには業務効率を向上させる多くの機能が備わっています。」
〔ケースクエア〕

**`literal`** - a construction mirrored word for word: "are scheduled to run
during" → 「に実行されるようにスケジュールされます」 and "is configured to run" →
「に実行されるように設定されます」, which Microsoft marks incorrect in favour of
「に実行されます」〔Microsoft〕 §2.1.4. 「Aおよび／またはB」 belongs
here too: 「翻訳調の文章には、読みにくいうえに意味が分かりにくい表現があります。」
〔谷口2010〕; list the cases instead.

**`list`** - three or more parallel items in running text, often in English
order with および before the last. Microsoft avoids 「xxx、yyy、および zzz」
〔Microsoft〕 §2.1.2; Red Hat prescribes 「3 つ以上の語句を併記する場合、
「および」や「または」などの並列接続詞の直前には読点を打ちます。」〔Red Hat〕
§7.1. The 建議 settles it by layout: 「一文の中で、並立する情報を三つ以上列挙す
るときには、箇条書を利用するなどして分かりやすく示す。」〔公用文〕 Ⅲ-3 ウ.

**`dash`** - an em dash inside a Japanese sentence. "In Japanese, do not use
it unless necessary." 〔Microsoft〕 §4.1.9; 「説明がダッシュのペアで囲まれてい
る場合には、かっこに置き換えます。」, and a dash joining a heading to its
explanation becomes 「コロン+半角スペース」〔Red Hat〕 §5.3.9. natural-japanese
reads a dash inserted mid-sentence as an English em dash carried over
〔natural-japanese〕. A published title quoted as written keeps its dash: in 10
of the 14 human documents with a dash, it sat only in a quoted or linked
title. The mid-sentence dashes came from one RIETI column and three essays
(section 4). Microsoft allows a dash where it is necessary and Red Hat avoids
it 「原則として」, so in `article` the reader rules on each by its sentence
(section 5, D6).

### 3.3 Style fit

**`buntai`** - a sentence off the 文体 the style settled. 「敬体と常体のどちらを
使うかは、文書の目的や読み手に応じて決めます。」〔JTF〕 §1.1.1. Rewrite in the
style's 文体; `paper` and `academic` hold である throughout.

**`goshu`** - words at the wrong distance from the reader. The 建議 and its
解説:
「傾向として、和語より漢語、動詞的表現より名詞的表現で、対象が客観化されて距離
感が大きくなりやすい。」 and 「重厚さや正確さを高めるには、述部に漢語を用いる。」
「分かりやすさや親しみやすさを高めるには、述部に訓読みの動詞を用いる。」
〔公用文〕 Rule by style: `official`, `paper` and `academic` take 漢語
predicates where the sentence carries weight; `article` takes 訓読み verbs and
everyday words; `business` follows the paragraph around the hit. A 漢語 word
that stands alone in a 和語 paragraph, or the reverse, gets matched to its
neighbours.

**`formality`** - a word off the document's distance in either direction.
Stiffer than its voice: "Microsoft voice avoids an unnecessarily formal
tone." 〔Microsoft〕 §2.1.2, with 推奨します → お勧めします among its pairs; this
applies to `article` and to customer-facing `business` text, while `official`
and `paper` keep the written word. Softer than its 文体: a spoken word in a
written document, such as the conjunction けど, which section 1.2 of
`references/academic-japanese.md` classes as spoken and the academic register
rewrites as が or であるが. This applies to every style except a deliberately
casual `article`.

## 4. Measurements

Human-written set: the web entries of natural-japanese's calibration corpus
(`corpus/sources.json` at commit b251b9b, tag v1.5.2, of https://github.com/coji/natural-japanese), fetched on
2026-10-16 with its `corpus/fetch.py` and limited to the 83 published before
2022-12 (business 27 + 1, tech 40, essay 7, slide 8; 832,702 characters). They
include 内閣府 and 総務省 white papers, RIETI columns and company incident
reports.

| Form | Human documents hit (of 83) |
| --- | --- |
| 彼, 彼女, 彼ら, 彼等, 彼女たち + particle | 1 (essay) |
| この機能/システム/関数… が …を可能に/提供/実現…, or 手助けをする | 0 |
| それ/これ/このこと/この事実/この結果/このデータ が …を示す/意味する/証明する/もたらす (何を意味する excluded) | 1 |
| 値/属性/意味/役割 を持つ | 2 |
| に存在する + kanji or katakana noun | 1 |
| および／または | 0 |
| されるように設定/構成/スケジュールされ | 0 |
| dash (—, ―, ─, ‒, –) beside Japanese, with or without a space | 14 (10 only in a quoted or linked title) |
| が可能 / することが可能 + です・でし・である・であり・であっ・で、・だ・となる・になる・な and their -り/-っ forms | 26 |
| することにより / することによって / することによる | 13 |
| を可能にする | 7 |
| あなた + particle | 9 |
| 私たち + particle | 4 |
| より + adjective | 10 |
| ことができる | 22 |
| の〇〇を行う | 29 |
| において | 47 |
| を行う | 52 |

The first 13 forms are the rows of `assets/translationese.sample.md`. The
register's first group holds those at 2 documents or fewer; its second group
holds those at 4 to 26. The other five forms were measured with these
patterns, in the syntax of Python's `regex` module:

- より + adjective: `(?<![\p{IsCJKUnifiedIdeographs}\p{IsHiragana}])より(?:大き|小さ|多[いくか]|少な|良[いくか]|よい|悪[いくか]|高[いくか]|低[いくか]|速[いくか]|遅[いくか]|強[いくか]|弱[いくか]|重要|簡単|深[いくか]|広[いくか])`
- ことができる: `することができ(?:る|ます|た|ない|ません|れば)`
- の〇〇を行う: `(?<=[\p{IsCJKUnifiedIdeographs}\p{IsKatakana}ー])の[\p{IsCJKUnifiedIdeographs}\p{IsKatakana}ー]{2,}を(?:行[うっいわ]|おこな|実行し)`
- において: `において`
- を行う: `を行(?:う|い|います|った|って)`

To reproduce a figure, fetch the set as above, run
`scripts/register.py --register <file> --json` over each document with a
register file holding the row, and count the documents with at least one hit.
The pages may have changed since 2026-10-16.

Notes on the counts:

- より + adjective: the hits include より良い方向, より少ない輸入代金 and
  1より小さい.
- Dash: the four documents with a mid-sentence dash are one RIETI column and
  three essays; the other ten have the dash only inside a quoted book or
  article title, or a linked article title.
- The fetched pages carry some site text around the article, such as links to
  later articles; two of the dash hits are such links.
- に存在する: widened to also catch に存在するすべて, the row matched 3
  documents (システムに存在するすべてのドキュメント among them), so it stops at
  a kanji or katakana noun.

## 5. Where the sources disagree

- **D1 Passive.** The software guides turn an inanimate subject into a
  passive 〔Microsoft〕〔Red Hat〕; the 建議 warns that a passive can blur who
  is responsible, and grants it where the actor need not be shown 〔公用文〕. Ruling: a passive for what the computer does from the user's
  view; elsewhere the actor named or the condition form.
- **D2 Inanimate subject as a marker.** The guides avoid it 〔Microsoft〕
  〔Red Hat〕〔GDI〕, and a 13-language questionnaire finds Japanese avoids it
  〔風間2016〕. Meldrum did not confirm abstract-noun subjects as a marker of
  translated fiction 〔Meldrum2009〕, and corpus studies find the construction
  with natural-force nouns and in textbook science explanations 〔麻2016〕
  〔麻2024〕. Manual Hub keeps UI text and feature
  descriptions active; Red Hat rewrites a command's description into a
  passive. Ruling, this skill's own: flag a product, program, value or
  abstract noun given a person's act. Keep a feature description where the
  plain active sentence is clearer, as Red Hat §7.6 also allows. Read a
  natural force sentence by sentence against 風間2016's two conditions and
  麻2016's corpus pairs; 関西大CogLab's typhoon example is one to rewrite.
- **D3 および before the last item.** Microsoft lists 「xxx、yyy、および zzz」
  among the forms to avoid, though its own §4.1.12 example
  「行の追加、移動、または削除を行います。」 puts 、または before the last item;
  Red Hat writes the form, with a 読点 before および, in its own example. Ruling: follow the document's own habit, and set
  three or more parallel items out as a list 〔公用文〕.
- **D4 ことができる.** SmartHR rewrites 「することができる」, @IT 「する事が
  出来る」, and the 建議 「利用することができる」; Microsoft's own target sentence
  ends 「自分だけのパスワードを作ることができます。」 §2.2.3. Ruling: rewrite
  where できる says the same in the style's 文体.
- **D5 Katakana.** SmartHR tries a 漢字語 first, and so does one checker at
  インターブックス as a personal preference. Microsoft keeps its approved
  terminology. The 建議 keeps established loanwords 〔公用文〕 Ⅱ-3, and for a
  technical term chooses by the term and the setting among a paraphrase, an
  added explanation, and the term kept as it is where its spread is wanted
  〔公用文〕 Ⅱ-2. インターブックス uses the katakana a client specifies. Ruling: the reader the style names
  decides; an engineer reads the field's katakana, a general reader the
  建議's paraphrase.
- **D6 Dash.** Microsoft and Red Hat avoid it in Japanese; human writers keep
  it in published titles and in some essays (section 4). Ruling: a quoted
  title keeps its dash; elsewhere rewrite it, and in `article` rule by the
  sentence.

## 6. Sources

### Style guides and standards

- 〔Microsoft〕 Microsoft. *Japanese Localization Style Guide*. No edition date printed; the build of 2025-07-18. https://aka.ms/japanese-styleguide
- 〔公用文〕 文化審議会. 「公用文作成の考え方（建議）」 and its 解説, 令和4年1月7日. https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf
- 〔JTF〕 日本翻訳連盟 翻訳品質委員会. 『JTF日本語標準スタイルガイド（翻訳用）』第4.0版, 2026年7月25日. https://www.jtf.jp/pdf/jtf_style_guide.pdf
- 〔Red Hat〕 Red Hat Localization Services. 『Red Hat 日本語スタイルガイド』, 2014年7月改訂. https://community.jboss.org/servlet/JiveServlet/previewBody/52925-102-2-171801/DOC-954596.pdf
- 〔SmartHR〕 SmartHR Design System. 「ライティング › 基本的な考え方」. https://smarthr.design/products/contents/writing-style/
- 〔谷口2010〕 谷口功. 「さらば、翻訳調の文章！ 技術者向け校正ルール」, @IT, 2010年3月23日. https://atmarkit.itmedia.co.jp/ait/articles/1003/23/news095.html
- 〔清水川〕 清水川. 「翻訳する時に心がけていること」, Scrapbox, 2019年. https://scrapbox.io/shimizukawa/%E7%BF%BB%E8%A8%B3%E3%81%99%E3%82%8B%E6%99%82%E3%81%AB%E5%BF%83%E3%81%8C%E3%81%91%E3%81%A6%E3%81%84%E3%82%8B%E3%81%93%E3%81%A8

### Translator education

- 〔Manual Hub〕 Manual Hub. 「なぜ「〜を可能にします」は翻訳っぽく見えるのか 〜無生物主語と日本語表現の関係〜」, 2026年6月1日. https://note.com/manualhub/n/n34515e8fafdf
- 〔GDI〕 グローバリゼーションデザイン研究所. 「【第13回】翻訳の基本テクニック：無生物主語」, 2019年1月. https://globalization.co.jp/basics-of-app-translation/13-inanimate-subject/
- 〔山田2020〕 山田優. 「【第10回】通訳翻訳研究の世界～翻訳研究編～「翻訳調」とはどんな訳文なのか」, 日本会議通訳者協会, 2020年2月3日. https://www.japan-interpreters.org/news/ti-research10/
- 〔ケースクエア〕 ケースクエア. 「翻訳が不自然になる原因とは？日本語を自然にするコツと修正方法」. https://www.honyaku-service.com/column/unnatural-translation.html
- 〔川村2019〕 川村インターナショナル. 「「なぜか読みにくい」訳文の正体①遠距離でのすれ違い」, 2019年1月18日. https://www.k-intl.co.jp/blog/B_1901118
- 〔川村2020〕 川村インターナショナル. 「ITシステムの操作マニュアルを翻訳する」, 2020年1月10日. https://www.k-intl.co.jp/blog/B_200110A
- 〔ISS〕 津村建一郎. 「第15回：『の』重なりを防ぐ」, アイ・エス・エス, 2020年3月2日. https://www.issjp.com/columns/column-4717/
- 〔関西大CogLab〕 関西大学 Cognitive Lab. 『日英翻訳の技術』の紹介ページ, 2020年6月. https://wps.itc.kansai-u.ac.jp/cricket/research/book-1/
- 〔ミドリ〕 ミドリインターナショナル. 「翻訳のヒント「受動態の訳し方」」, 2012年9月. https://www.midorico.co.jp/tip/201209.html
- 〔インターブックス〕 インターブックス. 「「カタカナ語」との終わりなき戦い」, 2025年4月1日更新. https://www.interbooks.co.jp/news-room/multiling-3403/

### Research

- 〔Meldrum2009〕 Yukari Fukuchi Meldrum. *Contemporary Translationese in Japanese Popular Literature*. PhD thesis, University of Alberta, 2009. https://ualberta.scholaris.ca/handle/123456789/102474
- 〔吉見2001〕 吉見毅彦. 「英日機械翻訳における代名詞翻訳の改良」, 自然言語処理 8(3), 2001. https://ndlsearch.ndl.go.jp/en/books/R000000004-I5841027
- 〔風間2016〕 風間伸次郎. 「地域的・類型論的観点からみた無生物主語について」, 北方言語研究 6, 2016. https://eprints.lib.hokudai.ac.jp/dspace/handle/2115/60796
- 〔麻2016〕 麻子軒. 「連語論的アプローチによる無生物主語他動詞文の日中対照：コレスポンデンス分析による成立要因の検討」, 計量国語学 30(7), 2016. https://www.jstage.jst.go.jp/article/mathling/30/7/30_395/_article/-char/ja
- 〔麻2024〕 麻子軒. 「日中における無生物主語他動詞文の使用実態調査 : レジスターとジャンルに注目して」, 現代日本語研究 15, 2024. https://ir.library.osaka-u.ac.jp/repo/ouka/all/98462
- 〔奥山2026〕 奥山光. 「形式名詞「点」の成立の二つの要因──類別詞用法との連続性およびpointの多義性の引き受け──」, 日本語の研究 22(1), 2026. https://www.jstage.jst.go.jp/article/nihongonokenkyu/22/1/22_1/_article/-char/ja

### Tool

- 〔natural-japanese〕 coji. natural-japanese, `skills/natural-japanese/references/translationese.md` and the inanimate-subject detector in `skills/natural-japanese/scripts/lint.py` (MIT). https://github.com/coji/natural-japanese
