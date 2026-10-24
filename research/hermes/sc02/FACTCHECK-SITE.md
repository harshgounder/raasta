# FACTCHECK-SITE: every number the site prints

hermes, 2026-10-24 19:50 IST, research only. Scope: `~/hypnexis-main/app/site/public/content/*.json`,
`app/site-data/*` (meta, routes, barriers), and a grep of `app/site/src` for hardcoded claims. Method: read
the files, count what the data actually contains, then compare against primaries I verified myself
(`sc02/LEGAL-PRIMARY.md`, `sc02/CENSUS-JAIPUR.md`).

Verdict in one line: the site's data model is honest, its demo city is empty, and a few citations are
unverified. Two of the findings below are ship-blockers unless the copy changes.

## A. What is already correct, and should be left alone

| item | where | my check |
|---|---|---|
| Eval table prints nulls and "not measured yet", no invented scores | `content/eval.json`, `src/pages/how.js` | nulls throughout, page renders empty cells, no accuracy claim anywhere in src (grep for accuracy, precision, recall returns only the table and shader comments) |
| Evidence is three-state, not two | `src/data/data.js` line 54, `evidence: 'barrier' / 'clear' / 'unknown'` | matches the rule I argued for: not seen is unknown, never "safe" |
| OSM licence ODbL 1.0 | `content/sources.json` | correct |
| Mapillary CC BY-SA 4.0 | same | correct |
| Complaint cites the RPwD Act, 2016 generally, not a specific rule | `content/report.json` | safe: the Act is the right instrument. Do NOT add Rule 15(1) wording, the Supreme Court struck that rule down (see LEGAL-PRIMARY.md) |
| No Chandigarh +410 m figure | not present in `site-data/chandigarh/routes.json` | instructed not to quote it, and the number is not in that file, so nothing to remove |

## B. Ship-blockers

### F1. The hero city has zero measured barriers, and the demo route is 100 percent unknown

Evidence, verbatim from the data:

- `site-data/jaipur/barriers.json` is `{"city":"jaipur","count":0,"accepted":0,"abstained":0,"placements":[]}`
- `site-data/jaipur/routes.json` for the displayed route: `"segments":42`, `"verified":0`, `"osm_only":0`,
  `"unknown":42`, `"barrier_delay":0.0`, `"minutes":16.5`

So for the corridor the site shows, the system has observed nothing. Every metre is a prior. If any copy,
caption or narration implies detected barriers in Jaipur, it is false as of this data snapshot, and a judge
who asks "show me where it detected a barrier here" gets an empty list.

Required fix, cheapest first: (1) the receipt shows `0 verified, 42 unknown` and the words "estimate from
priors, no photo evidence yet" on the Jaipur route, or (2) attach three or four real Jaipur photos with
labels so `verified` becomes non-zero, or (3) switch the demo route to the city that does have placements.

### F2. 94 percent of the Jaipur network is generated geometry, not mapped footpath

From `site-data/jaipur/meta.json` stats, verbatim counts: generated:sidewalk 1472, generated:crossing 1466,
generated:corner 810, generated:median 266, generated:link 248, generated:connector 11, and observed
osm:footway 84, osm:shared_street 176, osm:steps 4. Total 4,537 segments, of which 4,273 are generated and
264 are OSM-observed.

`sources.json` does disclose "Generated sidewalks (ours)", which is the right instinct. The risk is any
other screen calling these "mapped footpaths" or drawing them in the same visual weight as OSM lines. Fix:
legend entry for generated, distinct stroke or opacity, and one sentence in the method page.

## C. Citations that are not verified yet

### F3. IRC:103-2022 is cited for the 1:15 ramp, I verified only the 2012 text

`app/route/hroute/assumptions.json` says `IRC:103-2022 ... kerb ramp not steeper than 1:15 (6.67%)`,
footpath kerb 150 mm, clear walking zone 2 m.

- 2022 second revision does exist (IRC:103-2022, cited by Indian design manuals).
- I could not read it: the law.resource.org PDF downloads truncated three times, `pdftotext` rejects the
  partial file. So the 1:15 figure is UNVERIFIED by me.
- The 150 mm kerb cap I did verify, in the 2012 edition: clause 6.2.1, line 673 of the extracted text,
  "Maximum height of a pavement (including kerb, walking surface, top-of-paving) shall not exceed 150 mm
  from the road level".

Fix: either cite `IRC:103-2012` for the 150 mm kerb and drop the 2022 reference until someone reads it, or
someone opens the 2022 PDF and confirms 1:15. Do not print a percentage from a code nobody on the team has
read.

### F4. MoHUA Harmonised Guidelines 2021 (1:12 ramp, 1200 mm clear width) is unverified by me

Same file cites `MoHUA_HG_2021`. The numbers are plausible and widely repeated, but I have not read the
primary. Treat as "to verify" before the deck or the method page prints them.

### F5. Project Sidewalk licence row says "CC0 per our notes"

Their tooling is MIT-licensed; the labelled data licence needs a source line, not a memory. Until someone
opens their licence page, the row should read "licence to confirm" rather than CC0, because a licence claim
on a public site is a legal statement.

### F6. OpenFreeMap tiles row is vague ("tiles from OSM data, see site")

Fine for now, but the row is marked `verify: true` and the licence should be named explicitly (their own
terms) before the site is public.

## D. Smaller correctness notes

- `assumptions.json` carries `uncertainty_penalty_not_in_minutes: 59.3` beside `"minutes": 16.5`. The key
  name already admits the unit problem. If the UI shows 59.3 as minutes, the route looks 4x slower than the
  model claims. Label it as an uncertainty seconds or cost unit, or convert it.
- `assumptions.json` labels every profile speed as an assumption except the 0.79 m/s elderly walker, which
  it attributes to "IRC older guidance via research digest". That is second-hand; either cite the code or
  mark it an assumption like the rest.
- `meta.json` records `built_at 2026-10-24T12:18:27Z` and `osmnx 2.1.1`, `fetched_via osm_api`. Good
  provenance, keep it visible on the method page.
- Version strings for three.js r186, MapLibre GL JS 6.15, deck.gl 9.4, three-pinata 2.0.1 are unverified by
  me tonight. Low risk, but they are version claims; a 30 second check each before publishing.

## E. Numbers the site MAY print, with the exact source line

If any screen shows the equity framing, these are the verified values and their citations:

| number | value | source line to print |
|---|---|---|
| Jaipur district population | 6,626,178 | Census 2011, Table C-13, catalog 1465 |
| Jaipur aged 60 plus | 455,130 (6.87 percent) | same |
| Jaipur disabled | 158,909 (2.398 percent) | Census 2011, Table C-20, catalog 43377 |
| Jaipur movement disability | 30,874 | same |
| Elderly or disabled, derived | 575,503 (8.69 percent) | my arithmetic on C-13 and C-20, label DERIVED |
| Kerb cap | 150 mm | IRC:103-2012, clause 6.2.1 |
| Right to walk | 19 June 2026 | 2026 INSC 647 |

Do not print ward-level disability (not published), any CAG finding (the report is unread), or the
Chandigarh +410 m route figure.

## F. What I would fix before 02:30, in order

1. F1 on the Jaipur receipt: show `0 verified, 42 unknown`, plus the words "prior, not measurement". This is
   ten minutes of copy and it removes the single most attackable claim on the site.
2. F2 legend entry for generated segments, and one sentence in the method page.
3. F3 citation change to IRC:103-2012 for the 150 mm kerb, dropping the unread 1:15.
4. F5 licence wording to "to confirm".
5. D unit label on the uncertainty penalty.
