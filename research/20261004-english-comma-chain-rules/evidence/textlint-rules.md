# Which textlint rules flag an English sentence by its commas or joined clauses, what does each count or match, default threshold, and maintenance recency?

## Evidence
| Claim | Publisher | URL | Published | Grade | Quote | Corroboration |
|---|---|---|---|---|---|---|
| textlint-rule-max-comma counts commas (,) per sentence; default max is 4, so a sentence with 5 or more commas is reported | textlint-rule GitHub org (azu) | https://github.com/textlint-rule/textlint-rule-max-comma | unknown | B | no quote (WebFetch paraphrase; search snippet agrees: default 4, "5 or more") | single_source |
| max-comma latest npm version 4.0.0, published and modified 2023-11-26 (about 34 months before AS_OF) | npm registry | https://registry.npmjs.org/textlint-rule-max-comma | 2023-11-26 | B | no quote | single_source |
| max-comma repository shows 41 commits; v2.0.0 release notes: "fix sentence splitting" and "update libraries and improve analysis" (release year not stated on fetched page) | GitHub | https://github.com/textlint-rule/textlint-rule-max-comma/releases/tag/v2.0.0 | unknown | B | no quote | single_source |
| textlint-rule-en-max-word-count caps words per sentence; no default (README example uses max 50); latest 2.0.1, modified 2023-02-13 | npm registry | https://registry.npmjs.org/textlint-rule-en-max-word-count | 2023-02-13 | B | no quote | single_source |
| textlint-rule-sentence-length caps characters per sentence; default 100; latest 5.2.1, modified 2026-01-03 | npm registry | https://registry.npmjs.org/textlint-rule-sentence-length | 2026-01-03 | B | "The total number of characters allowed on each sentences. Sentence.length > 100 and throw Error" (WebFetch rendering of README) | single_source |
| Textlint wiki collection lists English rules max-comma ("Limit maximum comma(,) count in a sentence."), en-max-word-count, write-good, rousseau, stop-words; none described as clause-based | textlint project wiki | https://github.com/textlint/textlint/wiki/Collection-of-textlint-rule | unknown | B | "Limit maximum comma(,) count in a sentence." | single_source |
| textlint-rule-write-good wraps the write-good linter, rousseau wraps rousseau; their descriptions mention no comma splice or run-on check (check not read in their READMEs) | textlint wiki | https://github.com/textlint/textlint/wiki/Collection-of-textlint-rule | unknown | B | "naive linter for English prose for developers who can't write good" | single_source |

## Falsifier
| Query | What came back | Does it change the answer |
|---|---|---|
| "textlint rule detect comma splice run-on sentence" (allowed_domains npmjs.com, github.com), plus an open-web variant with "independent clauses" and "part-of-speech" | Only max-comma and unrelated grammar guides. Non-textlint hits (lex00/sentences issue 41, rjwalters/anvil issue 1182 comma_stack) appeared, not read. No textlint rule using POS tags or a parser for comma splices was found. | No. Finding nothing is the result; the count-based answer stands for the rules found. |

## Search log
| Query | Facet | Sources adopted |
|---|---|---|
| textlint rule max-comma comma count per sentence | definition | max-comma GitHub |
| textlint rule comma splice run-on sentence English | falsifier | none |
| textlint-rule-en-capitalization textlint-rule-sentence-length textlint English rules list comma | definition | sentence-length, wiki |
| fetch max-comma GitHub / npm registry | data | GitHub, npm |
| fetch wiki collection | practice | wiki |
| textlint rule "run-on" OR "comma splice" ... part-of-speech | falsifier | none |
| fetch npm en-max-word-count, sentence-length | data | npm |
| textlint rule detect comma splice run-on sentence (github.com, npmjs.com) | falsifier | none |

## Gaps
- Practice facet is thin: no practitioner reports on max-comma false positives or on its use in English prose; a practitioner source (the DEV Community post "How I use linters to check my writing") appeared in search but was not opened.
- Exact semantics (what character counts as a comma, whether it counts the full-width comma) not quoted from the README; WebFetch gave paraphrase only. Reading the repo source would settle it.
- Last commit date of max-comma repository not obtained (npm publish date used). v2.0.0 release year unknown.
- write-good and rousseau READMEs not opened; whether they flag comma-joined clauses is unverified.
- Falsifier covered by search only; absence from the wiki collection and npm/GitHub search is not proof of absence.
