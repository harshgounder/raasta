# CITIES-EXPANSION: the next 12 Indian cities, and what I could actually verify tonight

hermes, 2026-10-25 01:10 IST, research. Read this as two parts: what is measured, and what is still a task.
I would rather hand over a short verified table with the gaps named than a long table with invented numbers.

## What failed, stated first because it changes how to read the table

- **Overpass is not usable from this box tonight.** overpass-api.de, overpass.kumi.systems and
  overpass.nchc.org.tw all returned no response in 40 s. overpass.osm.ch answered but returned
  `ways: 0` for a dense central-Delhi bbox (28.60, 77.20 to 28.62, 77.22), which cannot be true, so its
  data is not a full planet extract. I am not going to print footway counts from a source that says central
  Delhi has zero footways.
- **City-level disability tables are not in the all-India C-13 file** we already hold. That file is state
  level only, so district disability needs one C-20 download per state.
- Therefore the verified columns below are the state 60-plus share (computed by me tonight from
  `raw/census/DDW-0000C-13_india.csv`, single-year ages summed to 60 plus, divided by the state total) and
  the two city populations I fetched directly. Everything else is marked as a task with the exact method.

## The 12 cities

Order: demo value first, then scale. State 60-plus share is the verified demographic column, and it is the
number that matters for a footpath product because it is the population most exposed to a 230 mm kerb.

| # | city | state | city population 2011 (where fetched) | metro population 2011 | state 60-plus share, verified | why this city matters |
|---|---|---|---|---|---|---|
| 1 | Lucknow | Uttar Pradesh | to fetch | to fetch | 7.73 percent (UP, 15,439,904 of 199,812,341) | dense old-city lanes plus wide new arterials, and a state capital where a complaint has somewhere to land |
| 2 | Bhopal | Madhya Pradesh | to fetch | to fetch | 7.87 percent (MP, 5,713,316 of 72,626,809) | compact, walkable core with gas-affected and hill terrain, a good second-tier test of the terrain layer |
| 3 | Indore | Madhya Pradesh | to fetch | to fetch | 7.87 percent (MP) | consistently ranked India's cleanest city, which makes a footpath failure there a sharper story |
| 4 | Surat | Gujarat | to fetch | to fetch | 7.92 percent (Gujarat, 4,786,559 of 60,439,692) | flat, fast-growing, very wide roads, tests crossing length and signal timing rather than slopes |
| 5 | Ahmedabad | Gujarat | to fetch | to fetch | 7.92 percent (Gujarat) | riverfront and BRTS corridors, footpath quality varies street by street within one ward |
| 6 | Pune | Maharashtra | to fetch | to fetch | 9.88 percent (Maharashtra, 11,106,935 of 112,374,333) | highest 60-plus share of the large cities here, strong civic tech scene, existing PMC road data |
| 7 | Hyderabad | Telangana | to fetch | to fetch | AP undivided in 2011, so use the district C-20 file not a state share | metro footpaths are new in places and absent in the old city, which makes the generated-versus-observed split visible |
| 8 | Chennai | Tamil Nadu | to fetch | to fetch | 10.41 percent (TN, 7,509,758 of 72,147,030), the highest here | highest elderly share in the set, monsoon flooding on the same corridors, so weather and age interact |
| 9 | Kolkata | West Bengal | to fetch | to fetch | 8.48 percent (WB, 7,742,382 of 91,276,115) | narrow lanes, hand-pulled rickshaws, and the most pedestrian-dense streets in the country |
| 10 | Mumbai | Maharashtra | 12,442,373 (city), 18,394,912 metro, fetched 2026-10-25 | same | 9.88 percent (Maharashtra) | the hardest possible test: 41.8 percent slum population, footpaths used as shop floor, and a suburban rail network that dumps millions onto the same 3 m |
| 11 | Delhi | NCT of Delhi | 11,034,555 (city), 16,349,831 metro, fetched 2026-10-25 | same | 6.83 percent (NCT of Delhi, 1,147,445 of 16,787,941) | widest footpaths in the country next to the worst encroachment, and the only city with a full municipal ward map in OSM |
| 12 | Bengaluru | Karnataka | to fetch | to fetch | 9.48 percent (Karnataka, 5,791,032 of 60,195,297) | the strongest walking advocacy ecosystem, so an accessibility audit exists to compare against |

Note on the fetched populations: the census2011.co.in pages give city and urban agglomeration figures. The
Mumbai city number is the island city, not the metro, which is why both columns are shown. The Bangalore URL
I tried resolved to a Secunderabad page, so Bengaluru is marked to fetch rather than carrying a wrong number.

## What each city still needs, as a task list anyone can run

1. **OSM footway count.** Run the project's own builder for the city bbox rather than fighting Overpass:
   `python -m hroute.network --city <slug>` in `app/route` writes a `network.geojson` and a `meta.json` with
   `by_source_kind` counts, which is exactly the observed-versus-generated split we want. That is one
   command per city and it uses the same code path as Jaipur, so the numbers are comparable.
2. **Mapillary coverage.** Needs a Mapillary token; the public API returns an image count per bbox. Not done
   tonight, no token used.
3. **Open accessibility audits.** Search per city for municipal or NGO audits (Chennai and Pune both have
   advocacy groups; Bengaluru has a documented footpath audit). I did not run those searches tonight, and I
   will not claim a document exists until I have opened it.
4. **Disability by district.** One C-20 file per state from censusindia.gov.in, using the same column layout
   as the Rajasthan file already in `raw/census/`. For Telangana, use the district rows from the undivided
   Andhra Pradesh 2011 file, since the state did not exist at census time.

## Recommendation on order

If the goal is the next three cities rather than twelve: **Pune, Chennai, Lucknow**. Pune has the highest
elderly share among large cities, Chennai adds monsoon flooding on the same corridors, and Lucknow gives a
state capital with old-city geometry. Mumbai and Delhi are the biggest prizes and the biggest data fights,
and they should come after the pipeline has survived a second-tier city.

## What this file deliberately does not do

It does not invent footway counts, Mapillary numbers or audit citations. Three of the four columns the lead
asked for depend on tools that either failed tonight (Overpass) or need a token or a per-state download
(Mapillary, C-20), and the honest state is written above so anyone picking this up knows exactly where to
start rather than repeating a failed search.
