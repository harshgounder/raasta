# /what-if v2 build notes

claude, 2026-10-25, started 00:15 IST. Goal: every question in `research/hermes/sc02/WHATIF-TREE.md` browsable as a
topic > subtopic > sub-subtopic tree, and every one runnable on the map from a precomputed engine run.

v1 (15-card wall, "we do not know yet" ratio) archived to `app/site/archive/whatif-v1/` (page html, whatif.js,
whatif.json, WHATIF-CHECK.md). Nothing deleted.

## Pipeline

```
research/hermes/sc02/WHATIF-TREE.md
   |  app/site/tools/build_whatif.py          (re-run picks up new rows; parses tables + recipes)
   v
app/site/public/content/whatif-tree.json     (tree, questions, answers, Hindi, parsed recipes, body tree)
   |  app/route/tools/precompute_whatif.py    (impact engine, one run per recipe)
   v
app/site-data/whatif/<id>.json               (baseline vs what-if routes for every body leaf)
app/site-data/whatif/index.json              (one line per id: changed?, deltas, verdict, for tree badges)
   |
   v
/what-if/  (app/site/what-if/index.html + src/pages/whatif.js + src/pages/whatif.css)
```

## Schemas (contract between the scripts and the page)

### whatif-tree.json

```
{ schema: "raasta-whatif-tree-v2", generated_at, source,
  counts: { rows, recipes_clean, recipes_fixed, recipes_flagged, topics, subtopics },
  topics: [ { id: "T1", name: "Weather", subtopics: [ { id: "T1.1", name: "Rain", items: ["T1.1.1", ...] } ] } ],
  items: { "T1.1.1": { id, topic_id, topic, subtopic_id, subtopic, subsub, q, q_hi, a, parts: ["route cost", "receipt"],
            recipe: { raw, city, inject_raw, place_raw, elements: [element ids], attrs: {}, body_hermes: "B1.1",
                      body: "mw_self", hour: 19.0, hhmm: "19:00", weather_raw, weather, light_raw, light, context: {} },
            recipe_status: "clean" | "fixed" | "flagged", recipe_notes: [ "..." ] } },
  bodies: { tree: {Category: {Group: {_leaves: [ids]}}}, info: { id: { name, hermes_id, scorer, path } } },
  elements: { id: { name, category, subcategory, glyph } } }
```

### site-data/whatif/<id>.json

```
{ id, city, scenario: { id, name, start: {lat, lon, label}, end: {lat, lon, label} }, trip_note,
  leave_time, context: { hour, weather, light, temp_c?, ... }, body: "mw_self", contrast: [6 body ids],
  injected: [ { element, name, glyph, segment_id, lon, lat, road, placement: "osm_road" | "landmark" | "route",
                placement_note, attrs, confidence } ],
  geoms: { g0: [[lon, lat], ...], g1: ... },
  variants: { <body id>: { base:   { geom, length_m, minutes, status, blocked, summary },
                            whatif: { geom, length_m, minutes, status, blocked, summary, hits: [ {element, verdict, why} ] },
                            delta_m, delta_min, changed, on_route, verdict, reason (contrast bodies only), reason_short,
                            element_verdicts: [ { element, verdict, seconds, risk, reason (contrast bodies only) } ] } },
  span_points: [[lon, lat], ...], base_leave_time, base_context, compare_body, place: { raw, kind, note },
  headline: "one line for the recipe body", compare: "inject" | "body" | "hour" }
```

`on_route` says whether that body's usual (baseline) route passes the injected spot. When it does not, the page
says so and shows the element verdict "if you met it", instead of implying a reroute.

## Parser (app/site/tools/build_whatif.py)

Run: `python3 -I app/site/tools/build_whatif.py` (no venv needed). Reads every markdown table row whose first cell is an
id `T<n>.<n>.<n>`, so new hermes rows are picked up on the next run. Rows are never dropped:

- 2 stage-5 rows (T2.4.3, T2.4.4) have no sub-subtopic cell: the subtopic name is used and the row is marked fixed.
- Recipe = `city; inject <what> [size] [at|near|on <place>]; body leaf; HH:MM; weather; light`.
  `<what>` is mapped to taxonomy element ids (app/route/taxonomy/elements.json) by an ordered keyword table (`RULES`),
  first match per piece, pieces split on "plus" / "versus" so combination rows inject 2 or 3 elements.
- Sizes: `< 2.5 m` on a width element becomes clear_width_cm; longer lengths become a span (the element is repeated
  along the route); `kerb 180 mm`, `N percent`, `1:10 ramp`, `12 s signal at a 14 m crossing`, `400 m with no bench`,
  `N risers` (15 cm each, ASSUMPTION) become engine attrs.
- Weather words map to the engine's weather states (dry -> clear, after rain -> drizzle, flood -> heavy_rain +
  waterlogged, hot -> clear + 42 C ASSUMPTION, windy -> wind, cold -> cold_wave, hazy -> haze); a season is set where
  the word implies one. Light: night with "unlit / low lighting" in the recipe -> night_dark, else night_lit.
- Body leaf ids are hermes ids (B1.1, A1.2 ...) resolved through bodies.json `hermes_id`.
- `OVERRIDES` handle rows whose point is evidence quality (confidence or attach probability below the 0.5 block line,
  old or undated records, duplicates) or the clock (hour compare with temporary vendor / parking records seen 19:00
  the evening before, so the router's own hour curves decide).
- Rows with nothing physical to inject (interface, export, offline, ward questions) run as a body compare: the asking
  body against an adult with no impairment on the same trip, same hour and weather.

Status meaning: clean = every field read as written; fixed = a fallback or override was needed (the reason is in
`recipe_notes` and shown on the page); flagged = could not be read (none at the moment).

## Precompute (app/route/tools/precompute_whatif.py)

Run: `cd app/route; .venv/bin/python tools/precompute_whatif.py [ids...]` (about 6 min for all 300 on 10 processes;
with ids it updates those files and their index rows). Then re-run build_whatif.py so each item gets its `run` summary.

Per recipe:
1. Trip. Place names resolve in this order: a known OSM road name in the built network (Johari Bazar, Badi Chaupar,
   Chandpole -> "Chandpol Bazaar", MI Road -> "Mirza Ismail Road", or any exact road-name match), then a landmark that
   is already a Nominatim-checked start/end point in `hroute/cli.py AREAS` (Hawa Mahal, City Palace, Sector 17,
   Sector 10, Godowlia, Dashashwamedh, Kashi Vishwanath, Manikarnika). If the demo trip does not use the named road,
   the run walks along that road (about 600 m between two points on it) and says so in `trip_note`.
   Names that do not resolve (Ajmeri Gate x8, JLN Marg, Adarsh Nagar, "Walled City", "OSM footway": they are outside
   the built bbox or not road names) go on the baseline route and the placement note says exactly that.
2. Baselines for all 74 body leaves (impact engine, recipe hour/weather/light), no what-if records.
3. Placement: on the asking body's route, among the segments that match the place (crossing segments for kerb and
   crossing elements, footpath segments otherwise), the one that the most body leaves' baselines pass. Span lengths
   repeat the element on the following route segments (max 400 m / 12 segments) for surface, water, light, air,
   crowd and temporary-obstacle elements.
4. What-if runs for all 74 leaves with the records attached (source "what_if", removed afterwards; networks are not
   saved). compare "hour" attaches the same temporary records to both runs; compare "body" uses an adult with no
   impairment as the baseline.
5. Per body: both geometries (deduplicated), metres, minutes, blocked or not, the engine's own reason text, the
   element verdict straight from `hroute.impact.impact` (what it would do if met), and `on_route`.

Result of the 00:54 run: 300 / 300 written, 0 errors. Placement: osm_road 64, landmark 79, route 122, none needed 35
(body compares). compare: inject 262, body 35, hour 3. The asking body's run differs from its baseline in 294 of
300 rows (route or minutes). Files 33 to 124 KB each, 20 MB in all, loaded one at a time by the page.

## Routing API

`hroute/api.py` `/route` accepts `engine: "impact"`, `body` and `context` (pass-through to
`impact_adapter.route_with_engine`; legacy path unchanged; unknown body -> 400). Test added
(`tests/test_api.py::test_api_route_impact_engine_passthrough`), plus `tests/test_impact.py::test_adapter_record_attrs_pass_through`
for the adapter change (records may carry extra taxonomy `attrs`; measured height/width/slope still win).
`pytest -q tests`: 78 passed. The uvicorn on :8020 was started without --reload, so it serves the new fields only
after a restart (not restarted here, another lane may own it).

## Page (page lane, claude fork, 2026-10-25 00:40 to 01:00 IST)

Files (v1 is in `archive/whatif-v1/`, nothing deleted):

| file | what |
|---|---|
| `what-if/index.html` | new title + description, same config.js and font preload pattern |
| `src/pages/whatif.js` | full rewrite: tree, question view, engine block, deep links, body filter, search |
| `src/pages/whatif.css` | new, scoped to this page (page.css untouched) |
| `src/pages/whatif-map.js` | the map panel, loaded with a dynamic import on the first "Run on the map", so maplibre (1 MB chunk) is never fetched by a reader who only browses questions |
| `src/pages/whatif-glyphs.js` | pictograms: icons.js glyphs for the barrier types /map already draws, plus 64x64 round-stroke glyphs for taxonomy categories icons.js lacks (weather, light, air/noise, crowd, animal, crossing, transit, rest, compound ...). `art/out/v3/icons/` did not exist at build time; `ART` is the hook for codex's set |
| `tools/shot-whatif.mjs` | screenshots into `shots/whatif-v2/`, fails on page errors, console errors or horizontal overflow |

How it reads:
- Left: search (every word must match: id, topic, question, Hindi, answer, part, inject text, place, body), body filter (leaves used by the recipes, with counts), 12 topics with counts. One topic opens at a time, then one subtopic, then its questions; search opens every match. Badges per question come from `site-data/whatif/index.json` (B block, C cost, W warn, N none, Δ route differs, = same), the page works without it.
- Right: id + breadcrumb, the question in Gloock (Hindi question below; in Hindi mode they swap), hermes' answer, then "what the engine found" (`items[].run.detail`, visible without opening the map), product-part chips, the recipe box (city, element names with glyphs, place, body, hour, weather, light, the raw recipe, recipe_notes), the Run on the map button with previous/next, the map panel, and the engine block (deltas, without/with stats, reason_short, contrast bodies).
- Map panel: legend above the map (labels follow `compare`: without/with, adult vs this body, hour vs hour), baseline route ink dashed and offset 7 px so it stays visible where it shares a street with the red what-if route, injected elements as badges (severity from the body's element verdict), span_points as ringed dots, from/to pins, fit to both routes. Side: body, deltas, stats, an on_route=false note ("usual route does not pass this spot, if met: verdict"), engine hits, where it was placed, the contrast bodies as buttons, and every body leaf of the tree (`bodies.tree`) in a grouped select that swaps to `variants[body]`.
- Deep links: `/what-if#T1.1.2` selects, `/what-if#T1.1.2/run` also opens the map. Selection uses replaceState.
- Phone (<= 980 px): the tree is a "questions by topic" drawer; question, answer, recipe, run button, map (60vh), side panel stack in one column. The shell's sound button is moved into the header strip on this page only (it covered the answer text and the tree).

Checks: `npm run build` passes. `node tools/shot-whatif.mjs`: 14 shots, desktop 1440x900 and phone 375x812, no page or console errors, no horizontal overflow (T1.1.1, T2.1.1 span, T6.1.1, T6.1.1 body switch, T9.1.1, T10.1.1 body compare, T11.1.3 hour compare in Hindi, a click through all 12 topics, search "kerb", phone top, drawer, full page, map).

Known gaps: whatif-tree.json is about 690 KB raw (about 100 KB gzip), fine on 4G but it could drop unused body info; codex icon art is not wired because the folder does not exist yet; the tree's Hindi covers UI labels, topic names and questions, while subtopic names and answers are English (the source has no Hindi for them).

## Recipe parse count (00:54 build)

300 rows, 12 topics, 45 subtopics. Recipes: 244 clean, 56 fixed, 0 flagged, 0 dropped. 300 / 300 have a run file.
Fixed = 2 rows with no sub-subtopic cell, 35 body compares (no physical element: interface, export, ward, offline rows),
13 rows with no "inject" verb where the element was read from the words, and 6 overrides (first rain T1.1.7, hour
compares T2.3.4 / T9.3.7 / T11.1.3, kerb height from the question T6.1.1 / T12.1.1). Each has its reason in
`recipe_notes`. Taxonomy gaps worth a new element: "tactile missing at a crossing" (mapped to no_marked_crossing),
"cremation smoke" (mapped to garbage_burning_smoke), "lamp glare" (mapped to headlight_glare).

Rebuild order after hermes adds rows: build_whatif.py -> precompute_whatif.py -> build_whatif.py (adds `run`).
