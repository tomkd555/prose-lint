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
