# 03, the footpath network

hermes, 2026-10-25 02:55 IST. Scope: `app/route/hroute/network.py` (870 lines). Every claim below carries a
line reference. Numbers marked **measured** come from the city builds in `app/site-data/<city>/meta.json`.

## What the network is

A directed graph of walkable segments, where each segment is either **observed** (OSM had a footway, path,
steps or pedestrian way) or **generated** (we placed one beside a road that has none). The distinction is
carried in `source` on every segment and is never collapsed: `source=osm` versus `source=generated`
(`network.py:6-7`), and the site prints the split on every route line (`routing.py:110-111`).

## What we pull from OSM

Three Overpass filters, at file level so they are easy to audit:

```
ROAD_FILTER     network.py:35   highway=*, excluding area=yes and access=private
FOOT_FILTER     network.py:38   highway=footway|steps|path|pedestrian, excluding access=private
SIDEWALK_FILTER network.py:39   footway=sidewalk|crossing
```

Way tags kept include `sidewalk`, `sidewalk:left`, `sidewalk:right`, `sidewalk:both`, `footway`, `surface`
(`network.py:41`); node tags include `crossing`, `kerb`, `kerb:height`, `barrier`, `tactile_paving`,
`wheelchair` (`network.py:44`). That node list is the whole reason the router can speak about kerb height,
tactile paving and wheelchair access at all, and it is also why our coverage is thin: Indian OSM rarely carries
these tags.

Surface quality is filtered with two negative vocabularies: `BAD_SURFACE` (unpaved, gravel, ground, dirt, sand,
mud, grass, earth, pebblestone, and similar, `network.py:47`) and `BAD_SMOOTH` (bad, very_bad, horrible,
very_horrible, impassable, `network.py:49`). Road class priority runs trunk down to residential
(`network.py:50`), and excluded classes include motorway, construction and abandoned (`network.py:289`).

## How a generated sidewalk is placed

When a road has no sidewalk geometry on a side, we offset a line to that side:

```
offset = road_width_estimate / 2 + 1 m          network.py:8
road_width = lanes * lane_width_m               network.py:410-412   (when OSM gives lanes)
road_width = road_width_m[highway_class]        network.py:417       (otherwise a class default)
```

`_road_offset()` at `network.py:405` returns the offset and a text reason, so every generated segment can say
where its width came from. The generated segment is added with `source="generated"`, `side` and `parent` set to
the road it follows (`network.py:737`), and the parent is what lets the site say "this footpath is an
assumption beside that road" rather than presenting it as mapped.

Other generated kinds and their lines: `corner` at `network.py:745`, `crossing` at `network.py:753`,
`connector` at `network.py:810`, `network.py:840` and `network.py:865`. Each carries the same `source` tag, so
the honest count is always one group-by away.

## Snapping and coordinate handling

- Projection is per city, stored in `meta.json` as `crs` (EPSG:32643 for Jaipur, i.e. UTM 43N).
- Snapping uses a KD-tree over the largest connected component, and deliberately excludes nodes that only
  touch median segments, because starting a route on a median would make every wheelchair route look blocked
  (`routing.py:17-28`, comment at 22-23).
- Snapping is capped at `SNAP_MAX_M = 75.0` m (`routing.py:60`); beyond that the route returns
  `status="too_far"` with the distance (`routing.py:174-177`).

## Measured composition, all four cities

| city | segments | OSM observed | generated | generated share |
|---|---|---|---|---|
| jaipur | 4,537 | 264 | 4,273 | 94.2 percent |
| jaipur-photos | 4,704 | 163 | 4,541 | 96.5 percent |
| chandigarh | 7,047 | 511 | 6,536 | 92.7 percent |
| varanasi | 4,279 | 114 | 4,165 | 97.3 percent |

Source: `app/site-data/<city>/meta.json`, `stats.by_source_kind`, read 2026-10-25.

The kind breakdown for Jaipur, verbatim from the same file: generated sidewalk 1,472, crossing 1,588, corner
810, median 266, link 126, connector 11, against osm footway 84, shared_street 176, steps 4.

## What this stage cannot do

1. It cannot invent a kerb height. If OSM lacks `kerb:height` and no photo measured one, the segment carries no
   height and the cost model uses the unknown penalty, not a default.
2. It cannot tell a footpath from a verge. A generated line beside a road is geometrically plausible and
   semantically unknown, which is why the site styles it differently and why the route summary says
   "estimated" for those metres.
3. It cannot place a barrier. That is `attach.py`, and the 0.7 threshold lives there; the network only offers
   candidate segments.
