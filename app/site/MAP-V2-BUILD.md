# MAP v2 build log (claude, 2026-10-24 night, judging 03:00)

User verdict on v1: not visual, confusing, foggy; cramped; no place names; red blobs that float in a random area
and do not sit on the drawn footpaths; map too small, mostly horizontally; wants all elements, hover cards, 2.5D.

## Root causes found in v1 (checked in data, not guessed)

| complaint | cause |
|---|---|
| blobs off the pathways | v1 drew `record.lat/lon`. For photo records that is the CAMERA position (`record.position: "camera"`), and for Project Sidewalk labels it is the label point, not our generated sidewalk line. jaipur-photos: 130 records sit on only 10 distinct coordinates (one photo carries up to 13 detections), so they piled into one blob. |
| blobs concentrated in one random area | same; plus 89 of 130 (jaipur-photos) and 83 of 130 (jaipur-photos-south) records lie outside that network's bbox (both keys share one input file). |
| foggy, no names | v1 used a blank white style ("paper") with only our lines; no streets, buildings or POI names. |
| small map | 380 px side column + page head; map was ~60% of the viewport. |

## What v2 does

- Files: `src/map2/main.js` (page), `style.js` (base map), `elements.js` (placement), `icons.js` (pictograms),
  `map2.css`, `impact-fallback.json` (made by `tools/make_impact_fallback.py`). `map/index.html` now loads
  `src/map2/main.js`. v1 copied to `archive/map-v1/` (src/pages/map.js, map/index.html, page.css, mapview.js, old shots).
  `src/pages/map.js` and `src/demo/mapview.js` are left in place because `/what-if` still uses mapview.js.
- MapLibre only (no deck.gl on this page): labels, extrusions, clustering and pitch then share one depth and
  collision system. deck.gl stays in the bundle for /what-if.
- Base map: OpenFreeMap vector tiles (OpenMapTiles schema, OSM ODbL; credited in the attribution control and
  panel foot). Paper ground #F3F3F3, white streets, warm grey extruded buildings with a cast shadow
  (`fill-translate`), street names (OMT `transportation_name`) plus our own network's OSM road names, POI names
  (temples, markets, gates, landmarks) from z14. Decision: buildings are warm grey, NOT ink, because our
  footpaths are ink lines running along building fronts and would vanish on ink. If tiles fail the paper
  ground stays and our layers still draw (layers attach on `style.load`, not `load`).
- 2.5D: pitch 55, bearing -18, `flyTo` per trip; 2D/2.5D toggle (2D also hides extrusions).
- Footpaths: mapped (OSM) solid ink, estimated (generated) thin dashed ink at 55%; legend "estimated footpath, not mapped".
- Routes: RAASTA (accessible) thick red #C82924 with a white casing and a draw-in animation; least-blocked (no
  accessible route) dashed red; shortest blue #2E63B8, thinner, offset 7 px so the two never look alike or hide
  each other. Both carry line labels.
- Elements (placement in `elements.js`): ACCEPT -> point at `at_m` along its segment; ABSTAIN with candidates
  -> hollow dashed icon on the best candidate segment, hover highlights all candidates with their p; ABSTAIN with
  no candidate -> camera position, drawn only if inside the network bbox (coordinator rule). OSM-tag evidence
  (steps etc.) -> middle of the tagged segment. Co-located points fan out in rings (fixed slot offsets) with an
  ink anchor dot at the true spot. Clusters with a count only at z <= 15.
- Severity per body: block = solid ink disc, slow = ring, warn = small ring, not sure = dashed ring with "?",
  seen fine = square. Source: `/content/impact-matrix.json` when present (bundled at build via import.meta.glob,
  so no 404 in the console), else the fallback derived from `app/route/hroute/assumptions.json` (assumptions,
  labelled as such in the panel).
- Hover card (tap on phones): name, category, padded crop of the photo (opens the full photo), where-status in
  plain words, date seen, confidence, permanence, blocks/slows/warns per body, candidate footpaths for ABSTAIN,
  source credit + link.
- Panel: trip select, what-if toggle (what-if trips and records hidden unless on, labelled WHAT-IF), route card
  (metres, minutes, barriers met, evidence_line, unknown share, blocked-for-body with reasons, least-blocked),
  body tree, category toggles with in-view / total counts, honest notes (records outside the area are counted,
  not drawn). `uncertainty_cost_s` is never shown.
- City picker reads `/site-data/index.json` (every folder with network.geojson). Default city chandigarh (the
  only one with placed evidence); `?city=&trip=&body=` deep links.

## impact-matrix.json: what the map accepts (for the helper building it)

Any of: `{ bodies|tree: [ {id, label|name ({en,hi} or string), children:[...] } ... leaves may carry
profile|route_profile ], matrix|impacts|types: { <barrier type>: { <leaf id or routing profile>: "block"|"slow"|"warn"|"none" or {level, note} } } }`
or `rows: [{type, body|profile, level}]`. Leaves with no profile are mapped by name (wheel, pram, crutch, walker, vision).

## Data edits

`src/data/data.js`: fields ADDED only (barriers `raw`, clears `raw`, routes `blocked_for_profile`, `barriers_list`,
`uncertainty_cost_s` kept for completeness, never shown). Nothing existing changed. Backup in archive/map-v1/.

## Log
- 23:46 start, read data contract, data files, factcheck, art brief, route README.
- first build passed; first shots: labels missing in an early probe turned out to be timing (labels render once glyphs land).
  icon-offset from a feature array failed (`array` comes back as a string from the clustered source), fixed with a
  `match` over slot numbers. POI filter used `zoom` inside a filter; removed.
- 23:58 notes started. Icons up 20%, START/END pins moved onto tall thin stems so the icon rings at the start stay visible.
- 00:05 coordinator facts applied: chandigarh is the default area (only area with placed evidence); camera-position
  records outside the network bbox are not drawn, the panel counts them ("N more photo records lie outside this
  area"); ABSTAIN reads "seen in a photo, not sure which footpath"; what-if trips and records hidden behind a toggle.
- 00:08 impact-matrix.json landed (raasta-impact-matrix-v1: 379 elements x 74 bodies x 5 contexts, verdict letters
  B/C/W/N + seconds + risk). Adapter added: body tree from `body_tree` (category > subcategory > leaf, names from
  `body_info`), verdicts from the context picked by leave time (before 18:30 = day_clear, later = night_dark) or by
  the new "conditions" select. Detector types map to one matrix element each (RIM_PICK in main.js, e.g. parked
  vehicle -> car_parked_footpath, or two_wheeler_parked_footpath when the label says motorcycle/scooter). Each of
  the 74 bodies maps to one of the 7 routing profiles the precomputed routes exist for (rimProfile); the panel says
  which route is shown. The file is fetched at runtime (an early version bundled it with import.meta.glob; a 1.2 MB
  file that was still being written broke the dev server, so that was reverted).
- 00:12 "seen near it, not placed" count on the route card: hollow elements within 20 m of the RAASTA route.
- 00:16 2D toggle refits the camera; laptop (1440) top bar fixed; phone bar fits city, time, 2.5D/2D.
- 00:19 UI notes that most matrix values are assumptions (app/route/taxonomy/README), card shows the matrix row and
  whether it is sourced. tools/shot.mjs map job updated for v2 (it called the v1 `__view`).

## Screenshots (shots/map-v2/, all taken with tools/shot-map2.mjs, zero console errors)
desk-chandigarh, desk-chandigarh-hover, desk-jaipur-photos, desk-jaipur-photos-hover, desk-jaipur-photos-blind,
desk-jaipur, desk-2d (1920x1080); laptop-chandigarh (1440x900); phone-chandigarh, phone-panel, phone-card (390x844 @2x).

## Honest gaps (what is still weak)
- Chandigarh: the 155 placed labels cluster around the Sector 17 plaza near the END of the default trip, and the
  route itself meets 0 placed barriers. At the fit zoom the END pin tag covers part of that cluster; zoom in or click
  a count disc.
- jaipur-photos / -south: every record is ABSTAIN, so every icon is hollow and the routes count 0 barriers; the
  route card says how many hollow ones sit within 20 m.
- Icons are my SVG stand-ins (icons.js), not codex's ink set (art/out/v3/icons/ did not exist when checked). Swap
  point: replace `badge()` glyphs or load icons.json in addIcons().
- Routes are precomputed for 7 profiles only; the 74-body picker changes icon severity per body, but the route
  shown is the nearest of the 7 profiles. The engine route (impact_adapter.route_with_engine) is not wired in.
- Matrix oddity worth a look by its owner: blind_cane gets N (no effect) for electric_pole_midpath in day_clear.
- Base map needs the network (OpenFreeMap tiles, glyphs). Offline: paper ground + our footpaths, routes, icons and
  HTML pins still draw; street/POI names and cluster numbers do not.
- Hindi: main panel strings and element names are bilingual; matrix body and element names are English only.

## v2.1 (coordinator review, 00:20 to 01:00 IST)
1. Brand: the shell's top-left mark now reads RAASTA (src/shell/shell.js; old copy in archive/map-v1/). The story
   gate title "the same street" is the story's own title and was left alone.
2. Body names: "(claude addition)" and "(legacy ...)" are stripped in the UI; provenance shows as a hover title on
   the body button and as a note under the picker: "added by our team, not in the RPwD schedule", or the RPwD entry.
3. Routes for all 74 bodies: app/route/precompute_bodies.py (impact engine) -> app/site-data/<city>/routes-bodies/
   <trip>.json, 10 trips, 3,700 routes, 1.8 MB total; unique paths stored once, routes index into them. vite.config.js
   lists the files per city (`bodies` in /site-data/index.json) so the map never requests a missing file. The map
   loads the trip's file, picks leave time (nearest) x condition x body; falls back to the 7-profile routes.json
   (and says so) when a trip has no file. Conditions select: clear, evening with no streetlight, heavy rain (routes
   + icons), heat wave and smog (icons only, the route stays clear-weather and says so).
4. Chandigarh default trip: the existing `s10-labelled` trip already runs THROUGH the densest placed labels
   (segments s1261 to s1266, Sector 10 by the CLTA tennis stadium; the cluster is in Sector 10, not at the Sector
   17 plaza). Shortest 622 m meets 33 placed barriers and is blocked for a manual wheelchair by 3 vehicles and
   1 pole; the RAASTA route is 1.04 km and meets 0. The map now picks, per city, the trip where the RAASTA route
   avoids the most placed barriers (`bestTrip`), so no new routing scenario was needed. START/END labels now sit
   in the screen quadrant with the fewest icons and route vertices, off the legend and panel (`layoutPins`).
5. Matrix bug fixed in app/route/hroute/impact.py (see app/route/taxonomy/README.md, "Change 2026-10-25"), with tests;
   matrix re-exported.
6. Icons: art/out/v3/icons/ still does not exist (checked 00:52); the stand-ins stay.
New shots: desk-chandigarh (new default trip), desk-chandigarh-blind-rain, desk-chandigarh-museum-tetra; all others
re-taken. tools/shot-map2.mjs now waits for map idle (the first phone shot was taken mid-fly with tiles missing).
Known: in the s10 trip the dense icons sit on top of the blue shortest line, so only its ends show; zoom in.
