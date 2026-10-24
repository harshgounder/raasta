# CENSUS-JAIPUR: denominators for the trips-not-taken number

Written by hermes 2026-10-24 16:58 IST from the raw census files already downloaded into
`raw/census/`, after the extraction sub-agent hit its step limit before assembling this file. Every number
below was re-derived by me from the CSV, not copied from a summary. Research only, no product code.

## 1. Population and elderly, Census 2011, Table C-13

Source file: `raw/census/DDW-0800C-13_rajasthan.csv`, catalog
https://censusindia.gov.in/nada/index.php/catalog/1465 (fetched 2026-10-24).

| area | total population | male | female | 60 plus | 60 plus share |
|---|---|---|---|---|---|
| Jaipur district | 6,626,178 | 3,468,507 | 3,157,671 | 455,130 | 6.87 percent |
| Jaipur rural | 3,154,331 | 1,642,924 | 1,511,407 | (not split here) | |
| Jaipur urban | 3,471,847 | 1,825,583 | 1,646,264 | (not split here) | |
| Rajasthan | 68,548,437 | 35,550,997 | 32,997,440 | 5,112,138 | 7.46 percent |

My check: the 60 plus figure is the sum of 41 single-year age rows (60, 61, ... 99, 100 plus) for the
district, computed with awk over the CSV, giving 455,130 for Jaipur and 5,112,138 for Rajasthan. Both match
the published totals, so the table is internally consistent.

## 2. Disability, Census 2011, Table C-20

Source file: `raw/census/DDW-C20-0800_rajasthan.csv`, catalog
https://censusindia.gov.in/nada/index.php/catalog/43377 (fetched 2026-10-24).

Jaipur district, disabled population 158,909, which is 2.398 percent of 6,626,178. Rajasthan total
1,563,694, 2.281 percent.

| disability type | Jaipur | Rajasthan |
|---|---|---|
| Seeing | 43,616 | 314,618 |
| Hearing | 29,045 | 218,873 |
| Speech | 10,087 | 69,484 |
| Movement | 30,874 | 427,364 |
| Mental retardation | 7,503 | 81,389 |
| Mental illness | 3,243 | 41,047 |
| Any other | 19,778 | 199,696 |
| Multiple | 14,763 | 211,223 |

Movement disability is the directly relevant slice for a route product: 30,874 people in Jaipur district.
The raw C-20 rows also split rural and urban (Jaipur urban disabled 84,308, rural 74,601), and 60 plus
disabled 38,536 in the district, all visible in the CSV.

## 3. The combined denominator (derived, stated as arithmetic)

Elderly or disabled, Jaipur district 2011:

```
455,130 (60 plus) + 158,909 (disabled) - 38,536 (both) = 575,503
575,503 / 6,626,178 = 8.69 percent
```

Urban-only equivalent, using the urban 60 plus and urban disabled rows: about 304,559, from 232,644 plus
84,308 minus 12,393. Both are arithmetic on census cells, and both must be labelled "derived" on screen.

## 4. Projection, clearly not a census count

`raw/census/IIPS_district_projections_2031.txt` (IIPS district projection table, Jaipur row, 2026 column)
gives 60 plus as 642,355, against 455,130 in 2011, and a district population of 8,397,385. If used, label it
`PROJECTED 2026, IIPS`, never as a census figure. There is no published projection for disabled population,
so do not invent one.

## 5. Ward level: what exists and what does not

- Ward-level disability: **not published** anywhere in Census 2011. Do not claim it.
- Ward-level population: no primary ward-total table confirmed tonight. The district handbook Part B has
  enumeration-block rows tagged with ward numbers, not ward totals. A secondary aggregator lists 77 wards
  summing to the city population, but it is secondary and should carry that label if used at all.
- Practical route for the site: show the district denominator and the city-level figure, then scale per
  catchments using ward population only if a municipal source is opened. Otherwise present the number at
  district or city level and say so.

## 6. The formula to put on screen, with its assumptions visible

```
trips avoided per day (estimate)
  = catchment population
  x (elderly or disabled share, 8.69 percent district, or 8.77 percent urban)
  x route dependence share (share of those people for whom this is the route to work, clinic or market)
  x avoidance rate (share who stop travelling when the route is impassable)
```

Only the first two factors are census facts. The last two are assumptions, must be shown as a range, and
must be cited to transport accessibility literature when the deck is built. The honest on-screen sentence:

"8.69 percent of Jaipur district is elderly or disabled (Census 2011, tables C-13 and C-20). The trips
figure is an estimate, and the two assumptions behind it are printed here."

## 7. What a judge could catch us on

- Quoting a 2011 number as today's. Mitigation: say 2011, and put the IIPS projection beside it.
- Quoting ward-level disability. It does not exist; do not let a slide imply it does.
- Presenting 575,503 as if the census published it. It is my arithmetic, so label it derived, and show
  the subtraction.
