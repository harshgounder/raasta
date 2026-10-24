# app/route: footpath network + accessible routing (SC-02 lane B2)

Answers PS-ANCHOR clauses C3, C4, C5, KC2, KC3: a footpath NETWORK for any Indian place, barrier
detections placed on the right SEGMENT (with probability, or ABSTAIN), and shortest vs accessible routes
per body profile and leave time. It never says "safe": every segment is `known_barrier`, `known_clear`
(photo or volunteer label, with date), `osm_tag` (OSM tags only) or `unknown`, and routes report those counts.

## Run

```
cd app/route
uv venv .venv; uv pip install --python .venv osmnx networkx shapely pyproj fastapi uvicorn numpy scipy pytest httpx matplotlib
.venv/bin/python -m pytest -q tests                       # 27 tests, offline (synthetic graph)
.venv/bin/python -m hroute.cli precompute                 # jaipur chandigarh varanasi -> ../site-data/<city>/
.venv/bin/uvicorn hroute.api:app --port 8020              # API
```

## API

| method | path | body / result |
|---|---|---|
| POST | /network/build | `{city, bbox:[south,west,north,east]}` or `{city, place}` -> stats. Cached in cache/networks/<city>.pkl |
| POST | /barriers | `{city, records:[record...]}` -> per record ACCEPT (segment_id, p) or ABSTAIN (top 5 candidates) or REJECT |
| POST | /route | `{city, start:{lat,lon}, end:{lat,lon}, profile, leave_time, all_profiles?}` |
| GET | /network/{city}.geojson | every segment with kind, source, side, parent_road, crossing, tier, evidence |
| GET | /profiles, /assumptions, /health | |

Barrier record: `type` (missing_kerb_ramp, steps, broken_footpath, missing_footpath, pole_obstruction,
parked_vehicle, pothole, open_drain, vendor, waterlogging; extension steep_slope; positive evidence
kerb_ramp_present, crossing_marked, clear), `lat, lon, heading?, side_hint? (left|right), position?
(camera|barrier), distance_m?, gps_error_m, confidence, status (ACCEPT|ABSTAIN), height_cm?,
clear_width_cm?, slope_pct?, observed_at, permanence (permanent|temporary), half_life_h?, source, label, photo,
segment_id?`. Full schema for `app/site-data/<city>/barriers.input.json`: BARRIERS-INPUT-SCHEMA.md.

Route result: `status` ok | blocked_for_profile | too_far (snap > 75 m) | no_path | same_point, `shortest` and
`accessible` (or `least_blocked` + `blocking_barriers`), each with geometry (GeoJSON LineString, lon/lat),
length_m, minutes (travel time only), `uncertainty_cost_s` (a routing penalty, never minutes),
`unknown_share_pct`, `mapped_m` / `estimated_m`, `barriers_observed`, `evidence_line`, tier counts,
`barrier_count` / `blocking_count` (the `barriers` list is cut to 40 in precomputed files), oldest_evidence,
and a summary like "44 segments: 0 with a known barrier, 0 seen clear, 0 from OSM tags only, 44 unknown; no
photo or volunteer-label evidence on this route; 0 m mapped, 1506 m estimated, 0 barriers observed; start
snapped 31 m, end 11 m to the network."

## How it works

1. **Network** (`hroute/network.py`). OSM walk filter plus custom filters (footway, steps, path,
   pedestrian, footway=sidewalk|crossing) via OSMnx; when Overpass is unreachable it falls back to
   api.openstreetmap.org `/map` tiles (this happened on 2026-10-24, Overpass refused connections).
   Roads get generated sidewalks on both sides (offset = road width / 2 + 1 m; width from OSM width,
   lanes x 3.25 m, or a per-class default) unless an OSM footway already runs along that side
   (projected coverage >= 50 %). Median and traffic-island sides of dual carriageways and roundabouts
   are kept as `kind=median` only so crossings connect; they are blocked for wheelchairs and prams and
   carry the maximum uncertainty cost for everyone else; routes never snap onto a median-only node. Block
   corners join the two sidewalks; crossings join the two sides at junctions (`crossing=generated`
   unless the OSM junction node has crossing tags). OSM footways meeting a road get a `link` to the near corner
   and `crossing` segments to the far side; dangling ends and small islands are stitched with labelled `connector` segments.
   OSM tags become evidence with `source=osm_tag` (steps, bad surface/smoothness, wheelchair=no,
   incline, kerb on crossing nodes, sidewalk=no).
2. **Attachment** (`hroute/attach.py`). Probability over segments within 30 m:
   distance (GPS error + view spread) x bearing alignment x road-relative side x kind prior, with a
   null "off network" weight. Attach when the detection is ACCEPT and p >= 0.7, else ABSTAIN with the
   candidate list. Tested on the wrong-side case (GPS on the north footpath, photo shows the barrier
   on the right while looking east -> attaches to the south footpath).
3. **Costs** (`hroute/costs.py`, numbers in `hroute/assumptions.json`). Per barrier type and profile:
   hard block or seconds. Kerb without ramp blocks wheelchairs above 2 cm (unmeasured height is
   treated as above). Slopes: both wheelchair profiles use the stricter 1:15 (IRC:103-2022 sec 6.7, Fig. 48,
   verified) over 1:12 (MoHUA HG 2021 cl. 3.7.2, verified); the explanation always states both. Effective
   barrier p = p_present x p_attach; temporary barriers use p_present = confidence x min(1, max(half-life
   decay, recurrence) x hour-curve ratio), ratio 1 when the observation has no time of day. Same-type
   labels within 5 m form one cluster (p = max); clusters of a type combine as 1 - prod(1 - p).
   Uncertainty: p_unseen = 1 - (1 - per_100m)^(uncovered length / 100) (per_segment for crossings,
   corners, links), cost = -ln(1 - min(p, 0.99)) x profile penalty. Only clear-type evidence covers
   length, 25 m each side of the label; a barrier never makes a segment cheaper.
4. **Routing** (`hroute/routing.py`). Dijkstra on length (shortest) and on profile cost with blocked
   segments removed (accessible). No path -> `blocked_for_profile` plus the least-blocked path and the
   barriers that block it.

## Precomputed areas (app/site-data/<city>/)

| city | area | evidence |
|---|---|---|
| jaipur | walled city: Hawa Mahal, Badi Chaupar, Johari Bazar, City Palace (palace-quarter scenario: OSM staircases block wheelchairs) | OSM tags only (drop B1 records in barriers.input.json) |
| chandigarh | Sector 17 and Sector 10 | labelled by Project Sidewalk volunteers (label data CC0 1.0, cite their CHI 2019 paper; coordinates and tags only, no GSV imagery) |
| varanasi | Godowlia, Dashashwamedh Ghat, Kashi Vishwanath, Manikarnika Ghat (river ghats, steps) | OSM tags |

Each city also has one `<scenario>-whatif` scenario (`what_if: true`): a vendor leaving 60 cm (seen 19:00
the evening before), a 6 cm kerb and a 7.5 % ramp, placed by this lane to show that profile and leave time
change the route. They are labelled WHAT-IF in every record and summary, never count as evidence, and are
removed from the network after that scenario. The vendor segment is searched until a leave-time difference
appears; that search is disclosed here.

Files: `network.geojson`, `routes.json` (scenarios x 2 leave times x 7 profiles), `barriers.json`
(placements with candidates), `meta.json`. Re-run `precompute` after adding records.

## Known gaps

- All cost numbers, hour curves and unknown priors are ASSUMPTIONS (named in assumptions.json);
  no Indian hourly survey of vendors or footpath parking was found.
- Generated sidewalks are geometric guesses: they say where a footpath would be, not that one exists.
- Start/end snap to the nearest network node (snap distance is reported), not onto a segment.
- No elevation model: slopes only come from OSM incline tags or measured records.
