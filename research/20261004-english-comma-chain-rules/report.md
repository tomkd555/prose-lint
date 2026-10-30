# Existing rules for comma-chained English sentences — scan (as of 2026-10-04)

Purpose: decide which existing rule, if any, prose-lint's English side adopts to flag sentences lengthened by joining clauses with commas.

Scope: textlint rules and published Vale styles. Assumptions: the reader maintains prose-lint; the Japanese side already has `comma_chain` in `koyobun.py`; a rule is a candidate only when textlint or Vale can run it.

## Question analysis
- Decision: the prose-lint maintainer adds an existing textlint rule or Vale rule to the English side, writes a house rule, or leaves the English side as it is.
- Question type: evaluative
- Presuppositions: an existing rule can tell a clause-joining comma from a list comma or an introductory-phrase comma — verify. The English side has no coverage today — verify.
- Useless answer: a catalogue of rule names with no account of what each one counts and which sentences it fires on.

Sub-questions and falsifiers:

1. Which textlint rules flag an English sentence by its commas or joined clauses? Falsifier: a textlint rule that finds comma splices by clause structure.
2. Which published Vale styles ship a rule for comma splices, run-ons or comma-heavy sentences, and through which extension point? Falsifier: a published style with such a rule on `sequence` or `script`.
3. How well does a pattern rule separate a comma splice from a list comma or an introductory-phrase comma? Falsifier: a pattern-based detector reported with high precision on ordinary prose.
4. Do the layers prose-lint already runs on English fire on a comma-chained sentence? Falsifier: a rule in ai-tells or proselint that targets comma-joined clauses in general.

Materials: none.

## Answer
No textlint rule and no Vale style among the nine styles read detects a comma splice or a chain of comma-joined clauses by structure. The rules that exist count: `textlint-rule-max-comma` counts commas per sentence, and a six-line Vale `occurrence` rule does the same with no new dependency. A count flags a five-item list at any cap that also catches a three-clause splice, and it passes a one-comma splice at every cap of 1 or more. A count rule therefore fits the advisory tier only. prose-lint's English side today flags comma chains only where four ai-tells rules match one tail shape each. Confidence: medium. The count rules' behaviour was confirmed by running them; the absence of a structural rule rests on nine styles and on searches, and each accuracy figure comes from one study.

The mechanism: an English comma marks a list item, an introductory phrase, an appositive and a clause joint with one character, and telling them apart takes knowing whether each side holds a subject and a finite verb. textlint's English rules and Vale's regex extension points see tokens. The published studies that do find comma splices use parse-tree features, and their recall stays low. Japanese differs in kind: the 連用形 or 接続助詞 before a 読点 marks the clause joint on the token itself, which is why `comma_chain` works with a tokeniser alone. The answer rests on one assumption: that the nine styles read stand for what Vale users publish.

## Findings

### 1. Which textlint rules flag an English sentence by its commas or joined clauses?
- `textlint-rule-max-comma` counts commas per sentence. Its default cap is 4, so it reports a sentence with five or more [S1]. The installed 4.0.0 source computes `text.split(",").length - 1`, so it counts the ASCII comma only (local read of the package from [S1]). Version 4.0.0 was published on 2023-11-26 [S1]. Single source.
- The textlint wiki's rule collection lists these English rules: max-comma, en-max-word-count, write-good, rousseau and stop-words. None is described as clause-based [S2]. Single source.
- `textlint-rule-en-max-word-count` caps words per sentence; prose-lint already sets it to 40 [S3].

Falsifier: "textlint rule detect comma splice run-on sentence" on npmjs.com and github.com, plus a variant with "part-of-speech". Only max-comma and unrelated grammar guides came back. The answer stands.

### 2. Which published Vale styles ship such a rule?
- Vale's `occurrence` extension point caps how often a token appears in a scope, and the documentation's own example caps commas per sentence at 3 [S4].
- Microsoft and RedHat each ship `SentenceLength` as an `occurrence` rule on words, at 30 and 32 [S5][S6]. Both are level `suggestion`.
- Local sync and grep of nine styles [S5][S6][S7]. The comma-named rules are `OxfordComma` in Google, Microsoft and RedHat. The rules on `sequence` or `script` are `Readability.Polysyllables`, `RedHat.Using` and five ai-tells vocabulary rules; none concerns clauses. The nine styles:
  - Microsoft
  - Google
  - RedHat
  - alex
  - Joblint
  - write-good
  - Readability
  - proselint
  - ai-tells
- `sequence` matches token sequences with part-of-speech tags; its documentation shows no comma-splice example [S4].

Falsifier: "Vale style run-on OR comma splice rule extends: sequence OR extends: script". No style with such a rule came back, and the local grep found none in the nine. The answer stands for those nine.

### 3. How well does a pattern rule separate a splice from a list or an introductory phrase?
- A CRF with parse-tree features reached 0.91 precision and 0.28 recall on comma splices in learner English [S8]. Single source.
- The same study's baseline, with words, part-of-speech tags and distances to conjunctions and no parse, scored 0.75 precision and 0.17 recall on one test set and 0.88 and 0.08 on the other [S8]. Microsoft Word 2013 scored 0.74 and 0.15, and 0.90 and 0.13 [S8].
- That detector strips introductory phrases and properly joined clauses before it parses, and it adds clause features to keep commas around non-restrictive clauses out of the hits [S8].
- On naturally occurring run-ons, about 1% of sentences, a CRF with syntactic features reached 0.34 precision and 0.27 recall [S9]. Preprint, single source.
- A user report says LanguageTool accepted "I went to the park, it was sunny." [S10]. Grade C; it corroborates the direction only.

Falsifier: "rule-based comma splice checker high precision no parser regular expression POS tags evaluation". No precision figure for a hand-written pattern rule came back. The answer stands; ordinary-prose precision is unmeasured.

### 4. Do the layers prose-lint already runs fire on a comma-chained sentence?
- ai-tells ships 137 rule files at v1.37.0 and names no comma-splice or run-on rule [S7]. Four of its rules anchor on a comma for one tail shape each: `ConsequenceParticiple`, `ConsequenceClause`, `SummativeAppositive` and `VerbTricolon` (local read of the synced package from [S7]).
- proselint's check categories and write-good's nine checks include none on commas or sentence length [S11][S12].
- The local run below shows the shipped configuration passing both comma splices.

Falsifier: "vale-ai-tells OR proselint rule comma splice OR run-on OR comma-heavy". Nothing about either package came back. The answer stands.

## Local run
Seven sentences, run in this session against the packages `setup.py` installs, plus max-comma 4.0.0 and `AISigns.CommaCount`, the rule the scan led to. The run shows what each rule counts; it gives no rate.

| # | Sentence | Shipped textlint | Shipped vale before CommaCount | max-comma 4 | max-comma 2 | max-comma 1 | AISigns.CommaCount |
|---|---|---|---|---|---|---|---|
| 1 | `The parser reads the file, it builds a tree, it reports every error.` | pass | pass | pass | pass | hit | pass |
| 2 | `The service validates the request, checks the cache, queries the database, formats the response, and returns it to the caller, logging each step along the way.` | pass | VerbTricolon | hit | hit | hit | hit |
| 3 | `We reviewed the design, and we changed the schema, and then we rewrote the tests, which took a week, because the fixtures were stale, so the release slipped.` | pass | VerbTricolon | hit | hit | hit | hit |
| 4 | `The kit holds a hammer, a saw, a level, a square, and a tape.` | pass | pass | pass | hit | hit | pass |
| 5 | `After the review, the team merged the change.` | pass | pass | pass | pass | pass | pass |
| 6 | `The build passed, and the team shipped it.` | pass | pass | pass | pass | pass | pass |
| 7 | `It works, ship it.` | pass | pass | pass | pass | pass | pass |

The shipped-vale column lists comma-related hits; `JourneyMetaphors` on 2 and `BareHolds` on 4 are left out.

`AISigns.CommaCount` is an `occurrence` rule with `max: 4`, so it reports five or more commas. Its token is `[^\s,]+,\s`: the word before the comma, the comma and the whitespace after it. A first version counted the bare comma and showed two defects on a long document. It counted the comma inside `3,000`. It also reported a hit on a later line than the sentence that fired; with the word in the token, the hit lands on the right line.

## Where sources disagree
The ai-tells rule count: a search snippet gave 111 [S7, grade C row], the README and the local sync give 137 [S7]. The snippet describes an earlier version.

## Sources
| # | Source | URL | Published | Grade | Quote | Corroboration |
|---|---|---|---|---|---|---|
| S1 | textlint-rule-max-comma, README | https://github.com/textlint-rule/textlint-rule-max-comma | unknown | B | "It means that report an error if the sentence include 5 or more `,`" | single_source; the installed source agrees |
| S1 | textlint-rule-max-comma, npm registry | https://registry.npmjs.org/textlint-rule-max-comma | 2023-11-26 | B | no quote | single_source |
| S2 | textlint wiki, Collection of textlint rule | https://github.com/textlint/textlint/wiki/Collection-of-textlint-rule | unknown | B | "Limit maximum comma(,) count in a sentence." | single_source |
| S3 | textlint-rule-en-max-word-count, npm registry | https://registry.npmjs.org/textlint-rule-en-max-word-count | 2023-02-13 | B | no quote | single_source |
| S4 | Vale documentation, occurrence | https://docs.vale.sh/checks/occurrence | unknown | B | "occurrence enforces the maximum or minimum number of times a particular token can appear in a given scope." | single_source; the local rule behaved as documented |
| S4 | Vale documentation, sequence | https://docs.vale.sh/checks/sequence | unknown | B | no quote | single_source |
| S5 | errata-ai Microsoft style, SentenceLength | https://raw.githubusercontent.com/errata-ai/Microsoft/master/Microsoft/SentenceLength.yml | unknown | B | "Try to keep sentences short (< 30 words)." | corroborated by the synced file |
| S5 | errata-ai Google, write-good and proselint styles | https://github.com/errata-ai/Google/tree/master/Google | unknown | B | no quote (directory listing) | corroborated by the local grep |
| S6 | RedHat style (vale-at-red-hat), SentenceLength and Using, read from the package `vale sync` delivered | https://redhat-documentation.github.io/vale-at-red-hat/reference-guide.html | unknown | B | "Try to keep sentences to an average of 32 words or fewer." | single_source; the URL is the rule file's own link field and the page itself was left unopened |
| S7 | tbhb/vale-ai-tells | https://github.com/tbhb/vale-ai-tells | unknown | B | no quote (README summary) | corroborated by the local sync: 137 files |
| S7 | tbhb/vale-ai-tells, search snippet giving 111 rule files | https://github.com/tbhb/vale-ai-tells | unknown | C | no quote | conflicting with the README; see above |
| S8 | Lee, Yeung, Chodorow, "Automatic Detection of Comma Splices", PACLIC 28 | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "our model achieved an average of 0.91 precision and 0.28 recall in detecting comma splices" | single_source |
| S9 | Zheng et al. (Grammarly), run-on correction, arXiv preprint | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | "Only 1% of sentences in RealESL are run-ons, which may not be the case in other forms of ESL corpora." | single_source |
| S10 | LanguageTool issue 719, user report | https://github.com/languagetool-org/languagetool/issues/719 | 2017-06-03 | C | no quote | single_source |
| S11 | amperser/proselint, README | https://github.com/amperser/proselint | unknown | B | no quote (category list) | corroborated by the errata-ai port [S5] |
| S12 | btford/write-good, README | https://github.com/btford/write-good | unknown | B | "Checks for `so` at the beginning of the sentence." | corroborated by the errata-ai port [S5] |

Freshness: S8 and S9 date from 2014 and 2018. The searches surfaced no later study that scores a detector a linter could embed.

## Re-fetch
| Figure | URL | Sentence returned | Outcome |
|---|---|---|---|
| max-comma default 4, reports at five or more | https://github.com/textlint-rule/textlint-rule-max-comma | "Default: `4`" and "It means that report an error if the sentence include 5 or more `,`" | confirmed |
| Vale occurrence caps a token per scope; example caps commas at 3 | https://docs.vale.sh/checks/occurrence | "`occurrence` enforces the maximum or minimum number of times a particular token can appear in a given scope." with `max: 3`, `token: ','` | confirmed |
| 0.91 precision, 0.28 recall | https://aclanthology.org/Y14-1063.pdf | "our model achieved an average of 0.91 precision and 0.28 recall in detecting comma splices" (read from the PDF's abstract; the text fetch could not parse the PDF) | confirmed |

## Not covered
- LanguageTool and other grammar checkers that parse: outside the textlint and Vale scope. Whether one of them could run as a further layer of prose-lint is a separate question.
- Vale styles beyond the nine read: GitLab, Datadog, Elastic and the rest were left unread.
- rousseau and stop-words, listed in the textlint wiki, were left unread.
- Precision on ordinary, non-learner prose: both studies use learner English.
- Practitioner reports on max-comma's false positives: the searches surfaced none.
- A research-team run would add a wider sweep of Vale styles, the LanguageTool rule set with its measured rates, and a test on a real corpus.

This report reflects what these searches surfaced, which differs from the balance of informed opinion.
