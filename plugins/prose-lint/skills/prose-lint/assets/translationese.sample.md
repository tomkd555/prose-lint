# Translationese register

English constructions carried into Japanese that a regex can find.
`scripts/register.py --translationese` reads the tables below and reports every
match with the line, the replacement and the reason. `setup.py` copies this file
to `~/.prose-lint/translationese.md`; edit that copy, or point
`PROSE_LINT_TRANSLATIONESE_REGISTER` at your own.

Most translationese needs the sentence around it to judge, and the reader in
Step 3a of the skill handles it from `references/translationese-japanese.md`.
These rows hold the forms that rest on a published source, each measured
against 83 human-written documents published before 2022-12 (business,
technical, essays and slides), as that reference's section 4 records. The bracket at the end
of each `Why` names the sources; section 6 of the reference gives each in full.
The rules for writing a row are those of `vocabulary.sample.md`.

## Rewrite

Each row matched at most 2 of the 83 human documents. Rewrite the hit to the
style the skill settled, in the words of the text around it, and keep it only
for the exception its `Why` names.

| Pattern | Instead | Why |
| --- | --- | --- |
| (?<![\p{IsCJKUnifiedIdeographs}])彼(?:女)?(?:ら\|等\|たち)?(?=[はがのをにもとでへや]) | 名前か役割（担当者、利用者、筆者）で書く。前の文から分かるなら省く。 | 英語の代名詞をそのまま移した形である。翻訳小説では「彼女」「彼ら」が特に多く現れる。実在の人物を、その人が使う代名詞で指す文は残す。〔Meldrum2009、山田2020、吉見2001、Microsoft〕 |
| この(?:機能\|ツール\|システム\|製品\|サービス\|アプリ\|設定\|変更\|更新\|手法\|仕組み\|関数\|コマンド\|プログラム)(?:を[^。、]{0,10}こと)?(?:は\|が)[^。]{0,25}(?:を(?:可能に\|支援\|提供\|実現\|妨げ\|要求\|発生させ)\|手助けをす) | 人の操作を条件にして「〜を使うと、〜できる」と書くか、「〜により」「〜では」で始める。仕様書で動作の主体を示す文は主語を残す。 | 「この機能は」「この関数を呼ぶことは」のように、機能や製品を動作の主体にした英語の構文である。〔Manual Hub、GDI、谷口2010、Microsoft、Red Hat〕 |
| (?<![\p{IsCJKUnifiedIdeographs}])(?:それ\|これ\|このこと\|この事実\|この結果\|このデータ)(?:は\|が)[^。]{0,30}(?<!何)を(?:意味\|示し\|示す\|示して\|証明\|もたら) | 「〜から、〜と分かる」「つまり〜である」と、分かったことを述語にする。 | 「事実」「結果」や指示語を主語にして「示す」「意味する」「もたらす」を続けた英語の構文である（This fact suggests、The result shows）。〔natural-japanese〕 |
| (?<![\p{IsCJKUnifiedIdeographs}])(?:値\|属性\|意味\|役割)を持(?:つ\|ち\|って\|った\|ちます\|っています\|っている) | 「〜の値は〜である」「〜には意味がある」のように、「である」「ある」で書く。 | 「値」「意味」「役割」を目的語にした have の訳である。〔谷口2010、natural-japanese〕 |
| に存在する(?=[\p{IsCJKUnifiedIdeographs}\p{IsKatakana}]) | 「〜の」「〜にある」で名詞につなぐ。 | 翻訳調の例に挙がる連体修飾である。「業務に存在する問題点」は「業務の問題点」で足りる。〔谷口2010〕 |
| (?:および\|及び)[／/](?:または\|又は) | 当てはまる組み合わせを箇条書きで挙げる。 | 「A and/or B」を移した形で、読みにくく意味も取りにくい。〔谷口2010〕 |
| されるように(?:スケジュール\|設定\|構成)され | 「〜に実行されます」のように、起きることだけを書く。 | 「are scheduled to run」「is configured to run」を語順どおりに訳した形である。〔Microsoft〕 |

## Read in context

Each row matched 4 to 26 of the 83 human documents: the form is ordinary
written Japanese in some documents and a carried-over English construction in
others. Rewrite where the plainer form says the same thing in the document's
style, and keep it with the reason where the style or the sentence needs it.

| Pattern | Instead | Why |
| --- | --- | --- |
| (?:することが\|が)可能(?:です\|でし\|である\|であり\|であっ\|で、\|だ\|となる\|となり\|となっ\|になる\|になり\|になっ\|な) | 「〜できる」「〜できます」と書く。 | can を訳した硬い言い方で、「できる」で足りる。〔Microsoft、谷口2010〕 |
| することによ(?:って\|り\|る) | 「〜して」「〜すると」「〜すれば」と書く。 | 「することにより」「することによって」は by 〜ing の訳である。技術文書の翻訳例には、この形を残した訳を選ぶものもある。〔Microsoft、ミドリ〕 |
| を可能に(?:する\|し\|します\|した) | 「〜できる」「〜できるようになる」と、人を主語にして書く。 | enable や allow の訳で、機能や仕組みを動作の主体にする。〔Manual Hub〕 |
| (?<![\p{IsCJKUnifiedIdeographs}\p{IsKatakana}])あなた(?:の\|は\|が\|を\|に\|も\|へ\|と\|で\|から\|まで\|より) | 省く。要るときは役割（利用者、管理者、お客様）で書く。 | you を訳した形で、多用すると不自然になる。文脈によっては使える。〔Microsoft〕 |
| (?<![\p{IsCJKUnifiedIdeographs}])私たち(?:は\|が\|の\|も\|を\|に\|へ\|と\|で\|から) | 省くか、組織の名前で書く。 | we を訳した形で、多くの場合は省く。明確にするために要るときは「私たち」か組織の名前で書く。〔Microsoft〕 |
| [—―─‒–]{1,2}(?=\s?[\p{IsHiragana}\p{IsKatakana}\p{IsCJKUnifiedIdeographs}])\|(?<=[\p{IsHiragana}\p{IsKatakana}\p{IsCJKUnifiedIdeographs}]\s?)[—―─‒–]{1,2} | 文中の補足は括弧に入れ、見出しと説明のつなぎはコロンにするか、文を分ける。 | 英語のダッシュを和文に持ち込んだ形で、和文では原則として使わない。引用した題名は原文のまま残す。〔natural-japanese、Microsoft、Red Hat〕 |
