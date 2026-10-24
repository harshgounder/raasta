# C6 labelling guide v1 (claude, 2026-10-24 ~19:35 IST)

Look at each image with the Read tool (full image, path = /home/liebert511/hypnexis-main/data/online/<file>).
Never look at /analyze outputs (app/analyze/out/*) while labelling: labels must be independent of the detector.

## The 5 PS classes (keys) and the exact rules

| key | present when | absent when | unsure when |
|---|---|---|---|
| missing_kerb_ramp | a RAISED kerb (footpath or median edge clearly above the road, about 10 cm or more) is visible at a point where a walker must get on or off the footpath (junction, zebra, footpath end, gap, lane or driveway mouth) and no ramp is there | no raised kerb visible; footpath flush with road; the transition point in view has a ramp | raised kerb visible but no transition point in view; too far, dark or blurred to judge height |
| steps | one or more steps or stairs, or a step up/down of one riser or more, ON or INTO the walking path (stair flights, shop plinth steps that are the walking surface, a raised footpath section reached by a step). A plain kerb along the road is NOT steps | no level change of a step in the walking path | a level change may exist but cannot be seen clearly |
| broken_or_missing_footpath | BROKEN: walking surface visibly cracked, tiles missing, holes, rubble, dug up, open drain in it, deep standing water covering it. MISSING: a road in a built-up place or a highway where people must walk on the carriageway because no footpath exists on a side in view. Give "kind": "broken" or "missing" | footpath present and intact; pedestrian-only lane, plaza or mall road with an intact surface (the whole width is walking space) | surface condition cannot be seen (crowd, dark, far); cannot tell whether a footpath exists |
| pole_obstruction | a pole, post, sign post, bollard, electric or utility box, transformer standing ON the footpath walking surface (or in a pedestrian lane) and narrowing it | no such object in the walking path (poles on the road edge outside the walking path do not count) | cannot tell if the pole stands on the footpath or on the road |
| parked_vehicle | a parked (stationary, unattended or clearly parked) car, two-wheeler, auto, bicycle or cart ON the footpath surface or in a pedestrian-only space, blocking walking | no parked vehicle on any footpath; vehicles parked on the carriageway only | vehicle position (footpath vs road) cannot be judged; moving vs parked unclear |

Strict rule: if you cannot see it clearly, mark unsure. Never guess. An image with no footpath at all gets missing_kerb_ramp=absent, pole_obstruction and parked_vehicle=absent unless the space people walk in is a pedestrian-only lane.

## Boxes
For each PRESENT class give one box per instance (max 6 per class; for a long row of parked bikes, one box around the row is fine) as FRACTIONS of the image: [x0, y0, x1, y1] with 0..1, left-top to right-bottom. A merge script converts to pixels with the real image size. Boxes are rough (they are scored at IoU 0.3).
For missing footpath: box the road-edge strip where a footpath should be. For broken: box the damaged patch.

## Condition fields
light: day | dusk | night ; weather: dry | rain | wet (after rain) | flood | snow ; setting: list from market, hill, village, residential, commercial, old_city_lane, highway, plaza, informal_settlement, coastal, heritage, campus
view: walker | vehicle (photo from inside a car or bike)

## Extras (not scored, but record)
"extras": short list, for example "vendor on footpath", "tree in footpath", "pothole on road", "railing", "animal", "kerb ramp present", "tactile paving".

## Output: one JSON object per line in the draft file named in your task
{"idx":"012","file":"commons/cm_016_....jpg","labels":{"missing_kerb_ramp":{"state":"absent"},"steps":{"state":"absent"},"broken_or_missing_footpath":{"state":"present","kind":"broken","boxes":[[0.4,0.6,0.7,0.9]]},"pole_obstruction":{"state":"unsure","why":"pole may be on road edge"},"parked_vehicle":{"state":"absent"}},"cond":{"light":"day","weather":"dry","setting":["commercial"],"view":"walker"},"extras":["tree in footpath"],"difficulty":2,"note":"one line: what makes it hard, if anything"}

difficulty: 0 easy, 1 some judgement, 2 hard, 3 very hard (many unsure or borderline). Every "unsure" needs a "why".
