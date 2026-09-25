# Vocabulary register

Wordings rejected in Japanese and English prose. `scripts/register.py` reads the
table below and reports every match with the line, the replacement and the reason.
Copy this file to `~/.prose-lint/vocabulary.md`, or point `PROSE_LINT_REGISTER`
at your own, and grow it one row per wording you reject.

## How to add a row

- The first column is a regex in the syntax of Python's `regex` module;
  `\p{IsHiragana}` and the other block names work. It must carry a boundary guard, or it fires on innocent text.
- Ban a wording together with its context. A bare term on its own collects
  exclusions until the row is useless.
- Escape a pipe as `\|`. A bare one would split the table column; the parser
  restores it.
- `Why` is shown with every hit: keep it to one or two short sentences.
- A hit is a suspicion. The wording may stay when it fits the context and the
  reason is stated.

| Pattern | Instead | Why |
| --- | --- | --- |
| ではな[いくか]\|(?<![まん])(?<!だけ)でな[いくか]\|じゃな[いくか]\|では(ありません\|ございません)\|じゃありません\|(?<!(日\|光\|雨\|風\|波\|弾\|球\|ボール\|バット\|体\|肌))に(当た\|あた)(らない\|りません)\|該当(しない\|せず\|しません)\|非該当 | 何であるかを書く。範囲を示すときは対象を挙げる。誤りを正すときは正しい内容だけを書く。 | 別のものを否定して定義する言い方である。引用は原文のまま残す。 |
| \bnot\s+(a\|an\|the\|to\s+be)\b\|\bnot\b[^.;:]{0,40}\bbut\b\|,\s*not\b\|\brather than\b\|\binstead of\b\|\bnot applicable\b\|\bdoes not apply\b\|\bN/A\b | Say what the thing is. To mark a boundary, name what falls inside it. To correct a mistake, state the right fact alone. | Defining a thing by what it is not. Quotations, and a sentence where not simply negates a verb, stay. |
| (?<![\p{IsCJKUnifiedIdeographs}\p{IsHiragana}\p{IsKatakana}A-Za-z0-9０-９々ー])なので | そのため、したがって | 文頭で接続詞として使った用法である。改まった文書では話し言葉の調子が出る。 |
| (?<![\p{IsCJKUnifiedIdeographs}\p{IsHiragana}\p{IsKatakana}A-Za-z0-9０-９々ー])だから(?!こそ) | そのため、したがって | 順接の接続詞として文頭に置いた用法である。改まった文書では話し言葉の調子が出る。 |
| 一番(?=(安[いくかっ]\|高[いくかっ]\|速[いくかっ]\|遅[いくかっ]\|多[いくかっ]\|少な\|大き\|小さ\|良[いくかっ]\|よ[いくかっ]\|悪[いくかっ]\|重要\|簡単\|確実)) | 最も | 形容詞の前に置く副詞の用法である。話し言葉の言い方で、書き言葉では「最も」と書く。 |
| (?<=(ほぼ\|ほとんど\|だいたい\|大体\|おおむね\|概ね\|およそ))全部 | ほぼすべて、大半（割合が言えるなら数字を書く） | 程度を表す副詞と組んだ言い方である。改まった文書では「ほぼすべて」のほうが収まりがよい。 |
| (?:と(?:も)?言われて(?:い\|お)(?:ます\|る)\|とされて(?:い\|お)(?:ます\|る)\|という声も(?:あ\|多)) | 誰が言ったのかを書く。出典を示せないなら、自分の判断として言い切る。 | 出所を示さない伝聞である。読み手は誰の判断か分からない。 |
| (?<![\p{IsCJKUnifiedIdeographs}\p{IsHiragana}ー])(?:様々な\|さまざまな\|多様な\|幅広い)(?=[\p{IsCJKUnifiedIdeographs}\p{IsKatakana}]) | 何と何があるのかを挙げる。数が言えるなら数字を書く。 | 具体を省いて広さだけを言う形容である。中身が伝わらない。 |
| を実現(?:し\|する\|でき\|可能)\|に寄与(?:し\|する)\|をシームレスに\|シームレスな\|を最適化(?:し\|する) | 何がどう変わるのかを動詞で書く（「短くなる」「一回で済む」）。 | 成果を抽象名詞でまとめる言い方である。読み手は何が起きるのか分からない。 |
| (?:して\|していき\|を進めて\|に取り組んで)(?:いき\|まいり)?たいと思います | 「します」「する」と言い切る。 | 意思を「思います」で弱めた言い方である。改まった文書では言い切る。 |
| ぜひ[^。]{0,20}(?:してみて\|お試し\|試して\|ご活用\|ご覧)(?:ください\|下さい) | 読み手が次に取る手順を書く。勧めるなら、その理由を書く。 | 記事の締めの定型句である。内容を運ばない。 |
| ^今回は[^。]{0,30}(?:について\|を)(?:紹介\|解説\|説明)(?:し\|いたし)ます | 冒頭で結論か本題を書く。 | 予告だけの冒頭である。本題に入るまでの読み手の時間を使う。 |
