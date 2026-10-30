# Do the layers prose-lint already runs on English fire on a comma-chained sentence?

Collected in the main session under the collector's floors.

## Evidence
| Claim | Publisher | URL | Published | Grade | Quote | Corroboration |
|---|---|---|---|---|---|---|
| vale-ai-tells ships 137 rule files at v1.37.0; its README names no rule for comma splices or run-on sentences | tbhb/vale-ai-tells | https://github.com/tbhb/vale-ai-tells | unknown | B | no quote (README summary through WebFetch) | corroborated by the local sync: 137 files in the style directory |
| proselint's README lists 24 check categories, from annotations to weasel_words; none concerns comma count, comma splices, run-ons or sentence length | amperser/proselint | https://github.com/amperser/proselint | unknown | B | no quote (category list through WebFetch) | corroborated by the errata-ai port: 36 files, no such rule |
| write-good ships nine checks (`passive, illusion, so, thereIs, weasel, adverb, tooWordy, cliches, eprime`); none concerns commas or sentence length | btford/write-good | https://github.com/btford/write-good | unknown | B | "Checks for `so` at the beginning of the sentence." | single_source |

## Local run (this session, 2026-10-04)
Packages installed by `setup.py` into a scratch home: the shipped English textlint config, vale 3.17.1 with proselint, ai-tells and AISigns. Sample: seven sentences.

| # | Sentence | Commas |
|---|---|---|
| 1 | `The parser reads the file, it builds a tree, it reports every error.` | 2 |
| 2 | `The service validates the request, checks the cache, queries the database, formats the response, and returns it to the caller, logging each step along the way.` | 5 |
| 3 | `We reviewed the design, and we changed the schema, and then we rewrote the tests, which took a week, because the fixtures were stale, so the release slipped.` | 5 |
| 4 | `The kit holds a hammer, a saw, a level, a square, and a tape.` | 4 |
| 5 | `After the review, the team merged the change.` | 1 |
| 6 | `The build passed, and the team shipped it.` | 1 |
| 7 | `It works, ship it.` | 1 |

- Shipped textlint English config: no finding on any of the seven. The 40-word cap stays silent; the longest sentence has 28 words.
- Shipped vale config: `ai-tells.VerbTricolon` on sentences 2 and 3, `ai-tells.JourneyMetaphors` on 2, `ai-tells.BareHolds` on 4. Sentences 1 and 7, the two comma splices, pass.
- Four ai-tells rules anchor on a comma. Each is an `existence` regex for one tail shape:
  - `ConsequenceParticiple`: `, leaving the` and `, making it`
  - `ConsequenceClause`: `, so the`
  - `SummativeAppositive`: `, a fact` and `, which is exactly the`
  - `VerbTricolon`: three parallel verbs

## Falsifier
| Query | What came back | Does it change the answer |
|---|---|---|
| "vale-ai-tells" OR "proselint" rule "comma splice" OR "run-on" OR "comma-heavy" sentence detect | Grammar guides and online checkers only; nothing about either package | No. The local grep of both synced styles for comma, run-on and splice found the four tail rules above and no general rule |

## Search log
| Query | Facet | Sources adopted |
|---|---|---|
| vale-ai-tells tbhb rules list comma splice run-on sentence | definition | tbhb/vale-ai-tells |
| proselint checks list comma splice run-on sentence length | definition | amperser/proselint (fetched directly) |
| write-good checks list "lexical illusions" "so" "there is" comma splice | definition | btford/write-good (fetched directly) |
| "vale-ai-tells" OR "proselint" rule "comma splice" OR "run-on" OR "comma-heavy" sentence detect | falsifier | none |

## Gaps
- The READMEs carry no publication date; the versions are the ones `vale sync` and `npm install` delivered on 2026-10-04.
- The sample is seven sentences written for this run. It shows what each rule counts; it gives no rate.
