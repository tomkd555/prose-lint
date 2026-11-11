# The administrative corpus of 1.12.0

35 documents written in ministries and public bodies, published from 2009 to
2022. Each was fetched on 2026-11-11. The HTML pages went through
`tools/extract.py` and the two PDFs through `pdftotext` and `tools/pdf2md.py`.
The texts are kept outside the repository; a row is reproduced by fetching its
URL and running the tools.

Chosen for: a named public body as the writer, a date before 2022-11, and a
body in running prose. One page fetched for the set was left out: 国税庁
タックスアンサー No.1120, whose text is revised every year and carries a 2026
date.

| Id | Kind | Document | Published | URL |
| --- | --- | --- | --- | --- |
| w2 | white | 内閣府「令和3年度 年次経済財政報告」第1章第1節 2021年前半までの経済動向 | 2021-09 | https://www5.cao.go.jp/j-j/wp/wp-je21/h01-01.html |
| w2b | white | the same, 第2章第1節 これまでの企業と投資 | 2021-09 | https://www5.cao.go.jp/j-j/wp/wp-je21/h02-01.html |
| w4 | white | 環境省「令和3年版 環境・循環型社会・生物多様性白書」第1部第1章第1節 新型コロナウイルス感染症の拡大の影響 | 2021-06 | https://www.env.go.jp/policy/hakusyo/r03/html/hj21010101.html |
| w4b | white | the same, 第2節 気候変動問題の影響 | 2021-06 | https://www.env.go.jp/policy/hakusyo/r03/html/hj21010102.html |
| w7 | white | 総務省「令和3年版 情報通信白書」コロナ禍における行政のデジタル活用の成果と課題 | 2021-07 | https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r03/html/nd122110.html |
| n3 | notice | 文部科学省「不登校児童生徒への支援の在り方について（通知）」 | 2019-10-25 | https://www.mext.go.jp/a_menu/shotou/seitoshidou/1422155.htm |
| n11 | notice | 文部科学省「障害のある児童生徒等に対する早期からの一貫した支援について（通知）」 | 2013-10-04 | https://www.mext.go.jp/a_menu/shotou/tokubetu/material/1340331.htm |
| n12 | notice | 文部科学省「性同一性障害に係る児童生徒に対するきめ細かな対応の実施等について」 | 2015-04-30 | https://www.mext.go.jp/b_menu/houdou/27/04/1357468.htm |
| n13 | notice | 文部科学省「体罰の禁止及び児童生徒理解に基づく指導の徹底について（通知）」 | 2013-03-13 | https://www.mext.go.jp/a_menu/shotou/seitoshidou/1331907.htm |
| r4 | speech | 日本銀行 総裁挨拶「最近の金融経済情勢と金融政策運営」（大阪経済4団体共催懇談会） | 2021-09-27 | https://www.boj.or.jp/about/press/koen_2021/ko210927a.htm |
| b2 | speech | 日本銀行 総裁講演「金融政策と企業行動：金融政策の効果波及経路と日本企業の構造変化」 | 2021-12-23 | https://www.boj.or.jp/about/press/koen_2021/ko211223a.htm |
| b3 | speech | 日本銀行 総裁講演「気候変動に関する日本銀行の取り組み」 | 2021-07-27 | https://www.boj.or.jp/about/press/koen_2021/ko210727a.htm |
| b4 | speech | 日本銀行 副総裁講演「最終局面を迎えたLIBOR移行対応」 | 2021-06-08 | https://www.boj.or.jp/about/press/koen_2021/ko210608a.htm |
| s2 | column | 総務省統計局 統計Today No.1「より良いコミュニケーションを目指して －「統計Today」の創刊」 | 2009-01-20 | https://www.stat.go.jp/info/today/001.html |
| s_010 | column | 統計Today No.10 | 2009-08-03 | https://www.stat.go.jp/info/today/010.html |
| s_030 | column | 統計Today No.30 | 2010-11-05 | https://www.stat.go.jp/info/today/030.html |
| s_050 | column | 統計Today No.50 | 2012-04-06 | https://www.stat.go.jp/info/today/050.html |
| s_070 | column | 統計Today No.70「世界に貢献する「Statistics Japan」」 | 2013-12-13 | https://www.stat.go.jp/info/today/070.html |
| s_090 | column | 統計Today No.90 | 2014-10-31 | https://www.stat.go.jp/info/today/090.html |
| s_110 | column | 統計Today No.110 | 2016-06-21 | https://www.stat.go.jp/info/today/110.html |
| s_130 | column | 統計Today No.130 | 2018-07-13 | https://www.stat.go.jp/info/today/130.html |
| s1 | column | 統計Today No.150 | 2019-10-01 | https://www.stat.go.jp/info/today/150.html |
| s_160 | column | 統計Today No.160 | 2020-08-05 | https://www.stat.go.jp/info/today/160.html |
| s_170 | column | 統計Today No.170 | 2021-04-20 | https://www.stat.go.jp/info/today/170.html |
| k1 | column | 国立国語研究所 ことば研究館「数字「０」の読み方」 | 2015-04-30 | https://www.kotobaken.jp/qa/yokuaru/qa-01/ |
| k2 | column | ことば研究館「「おぼえる」の漢字表記」 | 2015-04-30 | https://www.kotobaken.jp/qa/yokuaru/qa-02/ |
| k3 | column | ことば研究館「「おっしゃられる」のような二重敬語はどのぐらい使われていますか」 | 2018-08-31 | https://www.kotobaken.jp/qa/yokuaru/qa-50/ |
| k4 | column | ことば研究館「日本語で外来語が多いのはなぜですか」 | 2020-10-22 | https://www.kotobaken.jp/qa/yokuaru/qa-100/ |
| m1 | pr | 農林水産省 aff 2021年10月号「不思議がいっぱい！きのこの生態と豆知識」 | 2021-10 | https://www.maff.go.jp/j/pr/aff/2110/spe1_01.html |
| m2 | pr | aff 2021年10月号「詳しく知って楽しく食べよう！おいしいきのこ図鑑」 | 2021-10 | https://www.maff.go.jp/j/pr/aff/2110/spe1_02.html |
| m3 | pr | aff 2020年9月号「誰かに話したくなる お肉の豆知識」 | 2020-09 | https://www.maff.go.jp/j/pr/aff/2009/spe1_01.html |
| p4 | guide | 国民生活センター「「解約したはず！」「契約してない！」と思い込んでいませんか？ 予期せぬ“サブスク”の請求トラブルに注意！」 | 2021-10-07 | https://www.kokusen.go.jp/news/data/n-20211007_1.html |
| j2 | guide | 気象庁 知識・解説「キキクル（危険度分布）」 | the page as of 2022-06 | https://www.jma.go.jp/jma/kishou/know/bosai/riskmap.html |
| jtsb1 | report | 運輸安全委員会「鉄道事故調査報告書 RA2019-2 Ⅰ」 | 2019-03-28 | https://www.mlit.go.jp/jtsb/railway/rep-acci/RA2019-2-1.pdf |
| cocoa | report | 厚生労働省 COCOA不具合調査・再発防止策検討チーム「接触確認アプリ「COCOA」の不具合の発生経緯の調査と再発防止の検討について」 | 2021-04 | https://www.mhlw.go.jp/content/000769774.pdf |

The eight documents that were also written again from notes are w7 (W1 in the
reference), w4 (W2), n13 (N), r4 (S), s_070 (C1), k4 (C2), m3 (M) and p4 (A).
