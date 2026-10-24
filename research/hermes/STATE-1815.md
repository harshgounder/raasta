# HERMES STATE, 18:15 window (written 19:11 IST after gateway restart)

Lane: SC-02 research and fact-check. No deck work. No code. Product first.
Files root: `~/hypnexis-main/research/hermes/` and `~/hypnexis-main/research/hermes/sc02/`.

## Delivered and on disk

| file | size | what it holds |
|---|---|---|
| `sc02/LEGAL-PRIMARY.md` | 19K | 6 primary documents, quotes, safe and forbidden claims |
| `sc02/CENSUS-JAIPUR.md` | 4.8K | census denominators, re-derived by me from the CSVs |
| `sc02/GRIEVANCE-JAIPUR.md` | 27K | 43 press-sourced named grievances, 32 with derived coordinates |
| `sc02/MAX-INFO-PER-PIXEL.md` | 8.6K | the eight readable channels on a street photo, with confidences |
| `sc02/INDIA-CHAOS-FACTORS.md` | 8.9K | 32 factors in five groups, each with what-if and response |
| `sc02/IDEA-CHANNEL-LENS.md` | 5.2K | nine evidence lenses, opened vs unopened labelled |
| `sc02/SC02-EVIDENCE.md` | 7.1K | compelled-evidence routes and fetch recipes |
| `sc02/WOW-SCAN.md` | 5.5K | P-B statements scan (superseded by the SC-02 pick) |
| `AI-01..04, W3-01/02, HM-01/02 .md` | 12 to 22K each | wave-1 lead tables, 163 rows with URLs |
| `JUDGE-LENS.md`, `VERIFY-LOG.md`, `HM-02-evidence.md` | small | judge questions, dead-link sweep, HM-02 dataset evidence |
| `unstop/UNSTOP-FACTS.md` | 5.4K | official timeline and rubric, raw dumps alongside |

## Numbers I have verified myself, safe to print

- Jaipur district population 6,626,178; aged 60 plus 455,130 (6.87 percent), my own awk sum over 41 age
  rows of C-13. Rajasthan 68,548,437 and 5,112,138.
- Jaipur disabled 158,909 (2.398 percent), movement disability 30,874. Rajasthan 1,563,694.
- Derived elderly-or-disabled 575,503 (8.69 percent), subtraction shown in CENSUS-JAIPUR.md.
- IRC:103-2012 clause 6.2.1, line 673 of the extracted text: "Maximum height of a pavement (including
  kerb, walking surface, top-of-paving) shall not exceed 150 mm from the road level".
- 2026 INSC 647: "The citizen's fundamental right to walk on a demarcated footpath is primary and shall
  have priority over movement by motorised vehicles".
- 2024 INSC 858 Rajive Raturi, "A ceiling without a floor is hardly a sturdy structure".
- CPTR pedestrian audit criteria: even surface, continuity, at least 1.5 m wide.

## Do not print

- The Chandigarh +410 m route figure (cost model being fixed).
- Any CAG claim: the Rajasthan report is an 80 MB scan that would not download, so it is unread.
- Ward-level disability: not published in Census 2011.
- A Supreme Court claim that it mandated IRC dimensions: it did not.
- The two legal quotes still flagged unverified: the Bombay HC bollards line and the IRC "two wheelchairs"
  line.

## Open, with owners

- `app/route/hroute/assumptions.json` cites **IRC:103-2022** for the 1:15 kerb ramp and 150 mm kerb. I have
  the 2012 text verified in hand, and the 2022 PDF downloads truncated from law.resource.org, so the 2022
  citation is UNVERIFIED by me and the 1:15 figure rests on it. Either someone reads the 2022 clause, or
  the site cites 2012 for 150 mm and stops claiming 1:15 from a code it has not read.
- `assumptions.json` also cites MoHUA Harmonised Guidelines 2021 for 1:12 and 1200 mm clear width, not yet
  verified by me in primary text.
- Attribution problem, unresolved: a public repo `harshgounder/hypnexis-raah`, a `HERMES-DECK-CONTENT.md`,
  a "resolver and rule engine", an ONNX test and "palace-quarter numbers" have all been attributed to
  hermes. None of them are mine. I have written no code this round and made no push. If any of those touch
  the submitted product, the lead should check provenance before shipping.

## Current assignment (from 19:11)

1. This state file.
2. QUESTION ROUND: `sc02/QUESTION-ROUND.md`, batches of 50, question plus honest answer plus which product
   part handles it, one bus line per batch on its own thread.
3. Then `sc02/FACTCHECK-SITE.md`: every number the site prints, checked against primaries.
