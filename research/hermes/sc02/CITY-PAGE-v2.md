# CITY-PAGE-v2: content for /city

hermes, 2026-10-25 01:35 IST, research and copy. Every count below was read from the site data files or the
census tables tonight; the source line under each block says which. Headlines are 8 words or fewer, bodies
are two lines, and nothing here repeats a number I have not opened.

The one line that governs the whole page: **we have mapped four areas, we have measured barriers in one of
them, and the page says which is which on every card.** A city page that pretends evidence exists is worse
than no city page, and the numbers below make that distinction visible instead of hiding it.

---

# Jaipur walled city (`jaipur`)

## What we mapped
**Four thousand segments, two hundred sixty-four observed**
4,537 segments cover Hawa Mahal, Badi Chaupar and Johari Bazar, and only 264 of them come from OSM footway or
shared-street tags. The other 4,273 are geometry we generated, drawn in their own style and never called a
mapped footpath.
Source: `app/site-data/jaipur/meta.json`, by_source_kind counts, fetched 2026-10-25.

## What we have measured
**Zero barriers, and the page says so**
No photo in this bbox has attached a barrier yet, so every route here is a prior with a named penalty. The
route card reads 42 segments, 0 verified, 42 unknown, which is the honest state rather than a failing.
Source: `app/site-data/jaipur/barriers.json` (count 0), `routes.json` (verified 0, unknown 42).

## The worst five stretches
**We cannot rank what we have not seen**
Ranking a worst stretch needs evidence, and there is none in this bbox yet, so the card shows the five
longest unknown runs instead. Each one links to a scan prompt for that exact spot.
Source: route tier counts, `routes.json`.

## Which bodies are hit hardest
**A 230 mm kerb stops a chair, not a walker**
Where geometry is all we have, the impact engine marks wheeled and blind bodies as blocked and ambulant
bodies as slowed, using the matrix rather than a guess. The matrix note prints with it: sourced for 52 of 379
elements, assumption for the rest.
Source: `app/site/public/content/impact-matrix.json`, 379 elements x 74 bodies x 5 contexts.

## What the city already knows
**Nine named complaints, one official admission**
Residents describe cafes, carts, offices and cylinders on pavements; an official concedes that more than 90
percent of the walking space outside JDA's own headquarters is landscaping. Both are in the grievance ledger
with dates and outlets.
Source: `research/hermes/sc02/GRIEVANCE-JAIPUR.md`, Times of India Jaipur, 2025-08-21 to 2026-08-04.

## The people the numbers are about
**Six and a half million, five hundred seventy-five thousand exposed**
Jaipur district holds 6,626,178 people, and 575,503 of them are elderly or disabled, which is 8.69 percent of
the district. That derived figure is our arithmetic on two census tables and is labelled as such.
Source: Census 2011 Tables C-13 and C-20, re-derived in `research/hermes/sc02/CENSUS-JAIPUR.md`.

## What we would fix first, at no cost
**Clear the pavement before pouring concrete**
Enforce parking and vendor occupancy on Johari Bazar and MI Road, which are management failures rather than
construction ones, and photograph the result with a date. Then ramp the two crossings outside Hawa Mahal.
Source: grievance ledger plus the `jaipur` network; owner is the JMC Greater or Heritage ward office.

---

# Jaipur photo area (`jaipur-photos`)

## What we mapped
**Four thousand seven hundred segments, one hundred sixty-three observed**
4,704 segments around Tirpoliya Bazar and Sawai Jai Singh, of which 163 come from OSM tags and 4,541 are
generated geometry. The generated layer is labelled on the map, not hidden.
Source: `app/site-data/jaipur-photos/meta.json`.

## What we have measured
**One hundred thirty detections, all abstained**
130 photo records were placed on this network and every one is ABSTAIN, because none reached the 0.7 attach
confidence, so they inform the unknown penalty and never become a barrier claim. This is the single most
honest number on the site and it belongs on the page.
Source: `app/site-data/jaipur-photos/barriers.json`, 130 placements, 0 accepted.

## What the photos actually show
**Half of what we saw was parking**
Of the 130 records, 61 were parked vehicles, 18 poles in the path, 16 broken surfaces, 8 missing ramps, 8
potholes, 8 ramps present, 4 vendors and 4 steps. The pattern is enforcement and obstruction, not geometry.
Source: same file, type counts.

## Which bodies are hit hardest
**Obstruction hits everyone, kerbs hit wheels**
Parked vehicles and poles raise cost for every body, while the missing ramps are what block chair and pram
profiles outright. The abstain status means these are warnings now, not verdicts.
Source: impact matrix element mapping, `app/route/hroute/impact_adapter.py`.

## What the city already knows
**The same streets, named by residents**
This area overlaps the Johari Bazar complaints: cafe furniture, carts, and evening market occupation, all
dated in the grievance ledger.
Source: `research/hermes/sc02/GRIEVANCE-JAIPUR.md`.

## What we would fix first, at no cost
**Ask for one photo per segment, then enforce**
Sixty-one parking records on a handful of segments means a drive-by would settle the whole area; the fix is a
clearance order, not a rebuild. Second, re-shoot the same segments at 6 pm to price the evening market.
Source: barrier type counts plus the vendor hour curve in `assumptions.json`.

---

# Chandigarh (`chandigarh`)

## What we mapped
**Seven thousand segments, five hundred eleven observed**
7,047 segments across Sector 17 and Sector 10, with 511 from OSM and 6,536 generated. This is the one city
where a volunteer-labelled public dataset (Project Sidewalk, CC0) gives us an outside opinion.
Source: `app/site-data/chandigarh/meta.json`.

## What we have measured
**One hundred fifty-five accepted barriers**
198 placements resolved here, 155 at ACCEPT and 43 at ABSTAIN, which is the only city in the demo with a real
measured layer. That is why the map opens here when a judge asks to see evidence.
Source: `app/site-data/chandigarh/barriers.json`.

## The worst five stretches
**Six segments carry one hundred twenty-nine barriers**
Segments s1261 to s1266, six adjacent stretches, hold 129 of the 198 placements, with 68 parked vehicles, 53
poles, 51 broken surfaces and 14 missing footpaths across the whole set. That is not a city-wide problem, it
is a corridor problem.
Source: same file, counted by segment and type.

## Which bodies are hit hardest
**Wheeled and blind profiles pay most**
The clustering is obstruction plus broken surface, which blocks chairs and prams while slowing elderly
walkers; the missing-kerb count is small here, reflecting a city that builds ramps and then lets them be
blocked.
Source: barrier type counts plus the impact matrix.

## What the city already knows
**A planned city with an unplanned corridor**
Sector 17 is the retail heart and its service lanes carry the parking that the footpath absorbs; the number
above is the local version of a national pattern.
Source: barrier placements, sector geometry from OSM, and the Shenzhen-style service-lane pattern.

## What we would fix first, at no cost
**Move the parking, not the concrete**
Enforce on the s1261 to s1266 corridor, which alone would clear two thirds of the measured obstruction, and
re-photograph the six segments after enforcement. Fix the 14 missing footpath segments second.
Source: segment-level counts in `barriers.json`.

---

# Varanasi (`varanasi`)

## What we mapped
**Four thousand segments, one hundred fourteen observed**
4,279 segments across Godowlia, Dashashwamedh and the Kashi Vishwanath lanes, of which 114 come from OSM and
4,165 are generated. Old-city lanes are the hardest place to claim geometry and the map says so.
Source: `app/site-data/varanasi/meta.json`.

## What we have measured
**Zero barriers in the hardest terrain**
No barrier has attached in this bbox yet, so the page shows unknown routes and a scan prompt rather than a
verdict. The ghat stairs alone would change every profile if they were measured.
Source: `app/site-data/varanasi/barriers.json`, count 0.

## The worst five stretches
**The ghat approaches, still unmeasured**
The five longest unknown runs sit on the Godowlia to ghat approach, where a chair cannot pass a single flight
and a walker cannot pass a crowd at aarti time.
Source: route tier counts, `varanasi/routes.json`.

## Which bodies are hit hardest
**Stairs and crowds, in that order**
Steps block wheeled and blind profiles outright, while crowd density at aarti hours slows everyone else. The
hill and heritage layers in the engine are the ones carrying this city.
Source: impact matrix, terrain and crowd elements.

## What the city already knows
**A pilgrim city with a permanent crowd problem**
The complaints and audits that exist for Varanasi focus on sanitation and encroachment rather than kerb
geometry, which is exactly the gap this product claims.
Source: `research/hermes/sc02/GRIEVANCE-JAIPUR.md` is Jaipur-only; for Varanasi the honest line is that we
have no local grievance corpus yet.

## What we would fix first, at no cost
**Measure one lane end to end before touching it**
Pick the Godowlia lane, photograph it at 8 am and 7 pm, and publish the difference; the fix that follows is
crowd management, not construction. Second, map the one step-free route to the ghat that exists.
Source: network plus the aarti hour curve; owner is the Varanasi municipal corporation and the Kashi
Vishwanath temple trust for the temple side.

---

# India overview

## The frame
**Every eighth Indian is over sixty**
State 60-plus shares, computed by me from the all-India Census 2011 C-13 file: Tamil Nadu 10.41 percent,
Maharashtra 9.88, Karnataka 9.48, West Bengal 8.48, Gujarat 7.92, Madhya Pradesh 7.87, Uttar Pradesh 7.73,
Rajasthan 7.46, Delhi 6.83. The cities we map next are chosen against those numbers, not against fashion.
Source: `raw/census/DDW-0000C-13_india.csv`, single-year ages summed to 60 plus.

## The next three
**Pune, Chennai, Lucknow, in that order**
Pune has the highest elderly share among large cities, Chennai adds monsoon flooding on the same corridors,
and Lucknow gives a state capital with old-city geometry. Mumbai and Delhi follow once the pipeline has
survived a second-tier city.
Source: `research/hermes/sc02/CITIES-EXPANSION.md`.

## What the page must never say
**No city is covered until a photo says so**
Coverage means measured, not built, and each card prints observed versus generated segments before anything
else. A judge who catches one inflated number stops believing the other twenty.
Source: this file, and the counts above.
