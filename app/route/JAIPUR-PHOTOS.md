# JAIPUR-PHOTOS: footpath networks where the Jaipur photos are, and what attached

Routing lane, 2026-10-24 23:45 IST. Goal: put the 130 real /analyze detections from
`app/site-data/jaipur/barriers.input.json` on a footpath network. Rules kept: `accept_p` stays 0.7,
records without a heading go through the existing logic, the walled-city `jaipur` key is unchanged.
Every number below was computed by a script over the files, none typed by eye.

## Result in one line

**0 of 130 records placed on a segment, on any of the three Jaipur networks.** 130 ABSTAIN, 0 REJECT.
The networks now cover 105 of the 130 records (was 17), so the cause is no longer "outside the bbox":
it is that no detector-ACCEPT record reaches p 0.7. The map can still show every photo as a located
ABSTAIN observation with its annotated image and credit; none of them changes a route.

## 1. Where the records are

10 photos, 130 detection records (117 detector ABSTAIN, 13 detector ACCEPT). Records grouped by the first
network that has a segment within the 30 m search radius:

| network (city key) | bbox S W N E | records | photos | detector ACCEPT records |
|---|---|---|---|---|
| `jaipur` (walled city, unchanged) | 26.913 75.815 26.928 75.833 | 17 | mly 2530467737465123, pmx a010d4d5, pmx cca08f95 | 2 |
| `jaipur-photos` (new) | 26.921 75.788 26.931 75.811 | 41 | Commons cm_273 Tirpoliya Bazar, mlypair 288940249442301, mlypair 451767995919838 | 8 |
| `jaipur-photos-south` (new) | 26.903 75.812 26.914 75.825 | 47 | mlypair 240621417853612, mlypair 724686079525921 | 3 |
| none | | 25 | mly 1039818135346748, mly 1071581791885846 (north-west, 0 ACCEPT detections, not worth a network) | 0 |

New networks (OSM API 0.6 map tiles, Overpass refused connections again):

| key | nodes | segments | OSM-observed segments | generated segments | largest component |
|---|---|---|---|---|---|
| jaipur-photos | 3,142 | 4,704 | 163 (61 footway, 101 shared_street, 1 steps) | 4,541 | 3,130 of 3,142 nodes |
| jaipur-photos-south | 1,008 | 1,445 | 101 (26 footway, 74 shared_street, 1 crossing) | 1,344 | 981 of 1,008 nodes |

## 2. Attach counts and why records abstain

Per network, all 130 records attached (`barriers.json` key `why`, computed by `photos.reason_counts`):

| reason | jaipur-photos | jaipur-photos-south |
|---|---|---|
| placed (p >= 0.7) | 0 | 0 |
| ABSTAIN: photo outside this network (no segment within 30 m) | 89 | 83 |
| ABSTAIN: detector abstained (needs a human look), never placed | 33 | 44 |
| ABSTAIN: detector ACCEPT, best p < 0.7, no camera heading | 3 | 0 |
| ABSTAIN: detector ACCEPT, best p < 0.7, heading present | 5 | 3 |
| REJECT | 0 | 0 |

The 13 detector-ACCEPT records, each on the network that covers it:

| record | photo | type | det. conf | heading | side | dist m | network | candidates within 30 m | best p (kind) | 2nd p (kind, m from aim point) | best p if GPS error were 5 m (NOT applied) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| img-cf451c61f175-d00 | cm_273_Jaipur_Tirpoliya_Bazar_jpg | pole_obstruction | 0.22 | none | left | 15.1 | jaipur-photos | 23 | 0.203 (sidewalk) | 0.136 (sidewalk, 17.3) | 0.483 |
| img-cf451c61f175-d01 | cm_273_Jaipur_Tirpoliya_Bazar_jpg | pole_obstruction | 0.20 | none | right | 13.0 | jaipur-photos | 23 | 0.203 (sidewalk) | 0.136 (sidewalk, 17.3) | 0.483 |
| img-cf451c61f175-d02 | cm_273_Jaipur_Tirpoliya_Bazar_jpg | pole_obstruction | 0.191 | none | right | 15.4 | jaipur-photos | 23 | 0.203 (sidewalk) | 0.136 (sidewalk, 17.3) | 0.483 |
| img-98f2145f33c2-d00 | mly_Jaipur_2530467737465123 | pole_obstruction | 0.835 | 167 | right | 7.0 | jaipur | 12 | 0.143 (footway) | 0.143 (footway, 0.6) | 0.215 |
| img-1179114b9c92-d00 | mlypair_Jaipur_240621417853612 | parked_vehicle | 0.305 | 194 | left | 24.1 | jaipur-photos-south | 22 | 0.467 (sidewalk) | 0.15 (sidewalk, 18.1) | 0.725 |
| img-b30d6373e6ba-d00 | mlypair_Jaipur_288940249442301 | parked_vehicle | 0.36 | 349 | left | 4.1 | jaipur-photos | 21 | 0.276 (sidewalk) | 0.13 (sidewalk, 28.0) | 0.218 |
| img-b30d6373e6ba-d01 | mlypair_Jaipur_288940249442301 | parked_vehicle | 0.297 | 349 | right | 6.6 | jaipur-photos | 21 | 0.167 (footway) | 0.162 (footway, 5.3) | 0.301 |
| img-c8986f1e079e-d00 | mlypair_Jaipur_451767995919838 | parked_vehicle | 0.58 | 331 | right | 5.4 | jaipur-photos | 20 | 0.153 (footway) | 0.151 (footway, 2.5) | 0.221 |
| img-c8986f1e079e-d01 | mlypair_Jaipur_451767995919838 | parked_vehicle | 0.434 | 331 | right | 6.3 | jaipur-photos | 20 | 0.154 (footway) | 0.152 (footway, 2.8) | 0.225 |
| img-c8986f1e079e-d02 | mlypair_Jaipur_451767995919838 | parked_vehicle | 0.302 | 331 | left | 3.1 | jaipur-photos | 20 | 0.191 (sidewalk) | 0.183 (sidewalk, 17.6) | 0.108 |
| img-0e4f73d5818b-d00 | mlypair_Jaipur_724686079525921 | vendor | 0.265 | 255 | right | 10.1 | jaipur-photos-south | 22 | 0.174 (sidewalk) | 0.157 (sidewalk, 18.3) | 0.204 |
| img-0e4f73d5818b-d01 | mlypair_Jaipur_724686079525921 | pole_obstruction | 0.215 | 255 | none | 13.1 | jaipur-photos-south | 22 | 0.167 (sidewalk) | 0.138 (sidewalk, 8.5) | 0.227 |
| img-1ba93624ec64-d00 | pmx_Jaipur_cca08f95 | missing_footpath | 0.331 | 83 | right | 1.1 | jaipur | 11 | 0.255 (sidewalk) | 0.14 (crossing, 14.3) | 0.208 |

Why, in words:

1. **GPS error.** Every record carries `gps_error_m: 15.0`. It is the intake form's default, not a measured
   value (receipts show `location_source: form`; Mapillary and Commons gave no accuracy). With view spread
   7 m the distance sigma is 16.6 m, so a segment 18 m away still keeps about 55 % of the weight of one 7 m
   away. In a generated network with 11 to 23 segments inside 30 m, that caps p near 0.15 to 0.47.
2. **Heading missing.** 3 ACCEPT records (Commons photo cm_273) have no heading, so no bearing or side term:
   best p 0.203. The existing logic decides and abstains.
3. **Two (or three) candidate segments.** The best detection in the set (pole, conf 0.835, Mapillary
   2026-07-29, walled city) aims at a node where three OSM footways meet (osm_way 1545693918 and
   1545722070): s4197 and s4198 tie at 0.143 each, 0.5 to 0.6 m from the aim point. The three
   parked-vehicle records at Sawai Jai Singh Circle show the same pattern (0.153 / 0.151 / 0.149).
4. **GPS error alone would not fix it.** Even at 5 m only one record crosses 0.7 (img-1179114b9c92-d00,
   0.725), and at 3 m still only that one (0.764). The rest stay at 0.10 to 0.55 because the candidates are
   genuinely close together.

Experiments tried and NOT shipped (no effect on the outcome, so no code change):

- Aligned-road side rule (only sidewalks of a road within 30 or 45 degrees of the heading can be "the left or
  right footpath of the road in view"; others get `side_mismatch`): best ACCEPT p rises to 0.545
  (img-1179114b9c92-d00) and 0.314 (img-b30d6373e6ba-d00). Still 0 placed. Several detector-ABSTAIN records
  would cross 0.7 under it, but they stay ABSTAIN by design.
- Merging candidate pieces split at degree-2 nodes (the 150 m `max_segment_m` split): no change, none of
  the tied candidates are split pieces; they meet at real junctions (degree 3 or more).

Even if the 13 had placed, their route effect would be small: 10 are parked vehicles or a vendor from
2015 to 2023 with confidence 0.27 to 0.58; with half-life 2 h and recurrence 0.35, p_present is about
0.1, so a few seconds of cost. The one strong record (pole 0.835, permanent) has no clear width, so it is a
90 s soft cost for wheelchairs, not a block.

## 3. Route scenarios (all 7 profiles, 08:00 and 19:00)

Three real-photo scenarios; what-if records are switched off for these keys (`what_if: False`), so nothing
on these routes is invented. Routes are identical at 08:00 and 19:00 for every row (checked: status,
length, minutes, barriers and segment ids), because no temporary barrier is attached.

| route | profile | metres | minutes | shortest m | barriers observed | unknown % | photos within 30 m of the route (ABSTAIN, not on a segment) |
|---|---|---|---|---|---|---|---|
| jaipur-photos / tirpoliya-sjs-circle | manual_wheelchair | 2324 | 38.7 | 2040 | 0 | 100.0 | rx-cf451c61f175, rx-b30d6373e6ba, rx-c8986f1e079e |
| jaipur-photos / tirpoliya-sjs-circle | power_wheelchair | 2324 | 29.8 | 2040 | 0 | 100.0 | same |
| jaipur-photos / tirpoliya-sjs-circle | walker_elderly | 2324 | 49.0 | 2040 | 0 | 100.0 | same |
| jaipur-photos / tirpoliya-sjs-circle | pram | 2324 | 33.7 | 2040 | 0 | 100.0 | same |
| jaipur-photos / tirpoliya-sjs-circle | crutches | 2324 | 48.4 | 2040 | 0 | 100.0 | same |
| jaipur-photos / tirpoliya-sjs-circle | low_vision | 2324 | 38.7 | 2040 | 0 | 100.0 | same |
| jaipur-photos / tirpoliya-sjs-circle | default_walker | 2080 | 26.7 | 2040 | 0 | 100.0 | same |
| jaipur-photos / sjs-circle-south-north | all 7 profiles | 836 | 13.9 / 10.7 / 17.6 / 12.1 / 17.4 / 13.9 / 10.7 | 836 | 0 | 100.0 | rx-b30d6373e6ba, rx-c8986f1e079e |
| jaipur-photos-south / south-primary | wheelchairs, walker, pram, crutches, low vision | 774 | 12.9 / 9.9 / 16.3 / 11.2 / 16.1 / 12.9 | 750 | 0 | 100.0 | rx-1179114b9c92, rx-0e4f73d5818b |
| jaipur-photos-south / south-primary | default_walker | 757 | 9.7 | 750 | 0 | 100.0 | same |

(minutes in profile order manual_wheelchair, power_wheelchair, walker_elderly, pram, crutches, low_vision,
default_walker.) Snap distances: tirpoliya-sjs-circle start 9 m, end 4 m; sjs-circle-south-north 20 / 30 m;
south-primary 18 / 30 m.

Wheelchair vs walker does differ on tirpoliya-sjs-circle (2324 m vs 2080 m), but the cause is the
`no_footpath_on_median` ASSUMPTION on the shortest route (segments s853, s614: generated median of the
dual carriageway), plus unknown-segment priors. **No real observed barrier changes any route**, so the
"real barrier changes the route" scenario the brief asked for does not exist in this data. I did not fake one.

## 4. The photo behind each record

Every placement in `site-data/jaipur-photos*/barriers.json` (ACCEPT or ABSTAIN) now carries
`evidence_photo` = `{url, annotated, copied_from, original_url, receipt_ref, receipt_id, credit, licence,
author, source_url, box, crop, image_wh, observed_at}`, and `record.photo` is now the object the site's
receipt reads (`{url, crop, credit, license}`; the old string is kept as `record.photo_path`). Crop = the
detection box padded 15 %, as fractions; the annotated images have the same pixel size as `image_wh`.
Top-level keys added for these two keys only: `records_file`, `accept_p`, `why`, `photos`.

Images: 10 annotated JPEGs from `app/analyze/out/geo-v1/annotated/`, long side capped at 1280 px, at
`app/site/public/evidence/jaipur-photos/<stem>.jpg` (2.6 MB total), served as `/evidence/jaipur-photos/...`.
Credits: Commons cm_273 Gopal lal soni CC BY-SA 4.0; Mapillary robot8a, boracasli, maiti21, thejeshgn,
miguel_andrade CC BY-SA 4.0; pmx ravidwivedi CC-BY-SA-4.0; each with its URL in `evidence_photo`.

Note for the site lane: `vite.config.js` lists every `site-data/<dir>` with a `network.geojson`, so
`jaipur-photos` and `jaipur-photos-south` now appear as cities automatically. Their ABSTAIN dots include
records far outside the bbox (89 and 83 of 130), because the input file is shared.

## 5. What would put a real barrier on the map (not done, needs a decision)

1. A measured GPS error. A phone upload carries `GPSHPositioningError` or browser `accuracy`; with 5 m the
   south parked vehicle passes (0.725). This is the live-demo path for Phase 2 clause 1.
2. A human pass over the photos that writes `segment_id` (schema already allows it; placement skipped).
   I did not do this: it would be me labelling, not a reviewer.
3. Photos taken looking along a straight block, away from junctions; junction photos tie by construction.

## Files changed (for dsh and anyone else editing app/route)

| file | change |
|---|---|
| `app/route/hroute/cli.py` | AREAS += `jaipur-photos`, `jaipur-photos-south`; `precompute` reads `records_from`, skips what-if when `what_if: False`, calls new `_photo_extras` (writes `records_file, accept_p, why, photos` into barriers.json for photo areas only), meta source line for photos; imports `photos`, `cfg`. Pre-change copy: `app/route/cache/old/jaipur-photos-pre/cli.py.v1` |
| `app/route/hroute/photos.py` | new: `photo_stem, annotated_source, crop_of, credit_of, copy_resized, link_placements, reason_counts` |
| `app/route/tests/test_photos.py` | new, 5 tests; suite is now 32 (27 old + 5), all pass |
| `app/route/cache/networks/jaipur-photos.pkl`, `jaipur-photos-south.pkl`, `cache/osmapi/jaipur-photos*/` | new network caches and OSM tiles |
| `app/site-data/jaipur-photos/`, `app/site-data/jaipur-photos-south/` | new: network.geojson, routes.json, barriers.json, meta.json |
| `app/site/public/evidence/jaipur-photos/*.jpg` | new: 10 annotated images |
| `app/route/JAIPUR-PHOTOS.md` | this file |

Not touched: `attach.py`, `costs.py`, `routing.py`, `api.py`, `network.py`, `assumptions.json`,
`app/site-data/jaipur/*`, any `app/site` page. Note: `precompute` with no city now also builds the two photo
keys (defaults to every AREAS key).

Re-run: `cd app/route; .venv/bin/python -m hroute.cli precompute jaipur-photos jaipur-photos-south --no-rebuild`
then `.venv/bin/python -m pytest -q tests`.
