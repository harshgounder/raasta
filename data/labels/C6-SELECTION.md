# C6 selection: which 100 images we labelled, and why

claude, 2026-10-24, 19:10 to 19:40 IST. Clause C6 of SC-02: "Project Sidewalk provides labelled examples from other countries, but Indian streets differ, so teams must label their own local images as well". No photo walk was possible (D4), so the set is built from the licensed Indian street images already pulled into `data/online/` (327 images, one sidecar JSON each).

Files:
- `data/labels/c6-v1.jsonl`: 100 lines, one per image (file, image size, city, condition, licence, source URL, author, 5 class labels with pixel boxes, extras, difficulty, note).
- `data/labels/C6-REVIEW-QUEUE.md`: the 20 images a human must confirm first.
- `data/labels/build_c6_labels.py`: builds the jsonl from the labelling drafts (fraction boxes to pixels, joins sidecars, validates). Drafts are in the session scratchpad (`c6/draft_{A,B,C}.jsonl`, originals kept as `*.orig.jsonl`).
- `eval/eval_c6.py`, `eval/C6-RESULTS.md`, `eval/c6-results.json`: the score.

## 1. How the 100 were picked

```
327 images in data/online
 - 37 marked usable_for_detection=false (title cards, canary placeholders, menus, blur)
 - 18 youtube-storyboard frames (160x90, too small to label boxes on)
 = 272 candidates  -> 12 contact sheets (24 per sheet), looked at by eye
 -> 98 picked to cover the 5 classes + negatives + conditions + cities
 -> +2 added at merge (cm_192 Shimla Ridge as a clean negative, mlypair_Panaji_2910... as a vehicle-view missing-footpath case)
 = 100 labelled
```

Pick rules, in order:
1. Class coverage first: every PS class needs positives. Steps came from hill towns and heritage plazas (Shimla Rivoli Road, Jaipur Jantar Mantar path, MUJ plaza, Panaji temple). Kerb ramps from crossings and junctions. Broken footpath from the Commons "damaged / rubble / messy / repair" files. Missing footpath from village, highway, old-city and hill roads. Poles and parked vehicles from market and commercial streets.
2. Negatives: clean footpaths and pedestrian plazas (Mysuru palace walk, Delhi campus path in rain, Puducherry Dumas Street, Gangtok MG Marg, Shimla Ridge). Per class, most images are negatives for that class (36 to 86 absent per class, see section 2), which is what the precision numbers need. Only 4 images are absent on all 5 classes; most Indian street photos carry at least one unsure.
3. Conditions: night, rain, flood, wet, snow, dusk, market, hill, village, highway, old-city lanes, photos taken from a vehicle.
4. Cities: 21 places, metros plus hill towns, coastal towns and villages.
5. Licence: CC / CC0 / PD first (90 of 100). 10 YouTube standard-licence frames were kept only where no CC frame gave that condition (Bengaluru night heavy rain, unnamed village in rain, Kerala village at dusk in rain, Bengaluru JP Nagar rain, Pune Tilak Road kerb case and pole case, Shimla hill road, Chandigarh arcade, Mumbai Lokhandwala night market, Kolkata Dalhousie rain). They stay internal per the licence table in `research/claude/sc02-IMAGE-SOURCES.md` section 8.
6. Same-spot bursts were thinned (1 of the 7 Salt Lake flood frames, 1 of the 2 Munnekollala pothole shots skipped, etc.) so one scene does not count many times.

## 2. What the set holds (computed from c6-v1.jsonl, not typed)

| class | present | absent | unsure | boxes |
|---|---|---|---|---|
| missing_kerb_ramp | 4 | 55 | 41 | 4 |
| steps | 4 | 86 | 10 | 6 |
| broken_or_missing_footpath | 34 (22 missing, 12 broken) | 36 | 30 | 47 |
| pole_obstruction | 14 | 55 | 31 | 25 |
| parked_vehicle | 8 | 53 | 39 | 15 |

| condition (from the labels, not the sidecar tags) | images |
|---|---|
| light: day / night / dusk | 84 / 13 / 3 |
| weather: dry / wet (after rain) / rain / flood / snow | 76 / 11 / 10 / 2 / 1 |
| setting: commercial | 45 |
| market | 25 |
| residential | 21 |
| heritage | 13 |
| old-city lane | 11 |
| hill | 10 |
| coastal | 10 |
| plaza | 7 |
| village | 5 |
| campus | 2 |
| highway | 1 |
| informal settlement | 1 |
| photo taken from a vehicle | 10 |

| source | images | licence | images |
|---|---|---|---|
| Wikimedia Commons | 52 | CC BY-SA (2.0 to 4.0, incl. Mapillary / Panoramax) | 55 |
| Mapillary (Esri relay) | 20 | CC BY (2.0 to 4.0, incl. YouTube CC BY) | 32 |
| YouTube CC BY frames | 11 | YouTube standard (internal only) | 10 |
| YouTube standard frames | 10 | CC0 | 2 |
| Mapillary same-spot pairs | 7 | Public domain | 1 |

Cities: Delhi 15, Kolkata 13, Mumbai 11, India (city not stated) 8, Bengaluru 7, Jaipur 7, Pune 7, Shimla 7, Puri 4, Chandigarh 4, Panaji 4, Chennai 3, Puducherry 2, and 1 each for Himachal (McLeod Ganj), MUJ / Dehmi Kalan, Bagru NH48, Gangtok, Agra, Chopta village, an unnamed village, a Kerala village.

## 3. Label rules (full guide: `data/labels/C6-LABEL-GUIDE.md`)

- Classes are the 5 PS classes. `broken_or_missing_footpath` merges the receipt families `broken_footpath` and `missing_footpath` and keeps `kind` = broken or missing.
- Every class on every image is `present`, `absent` or `unsure`. Unsure always carries a `why`. Unsure is excluded from scoring for that class.
- Boxes: one per instance, drawn as fractions of the image while looking at it, converted to pixels by `build_c6_labels.py` using the real JPEG size. They are rough (scored at IoU 0.3).
- `missing_kerb_ramp` is present only when a raised kerb is visible AT a point where a walker must get on or off (crossing, junction, footpath end). A raised kerb mid-block with no crossing in view is unsure. That is why this class has 41 unsure and only 4 present.
- Merge rule decided by me after the three drafts came back: a vehicle parked on the carriageway edge of a street that has no footpath is `parked_vehicle = unsure` (it blocks the walking edge, but the PS wording is "blocking footpaths"). One labeller had marked these absent and the other unsure; 5 lines were changed absent to unsure so the set uses one rule. Each changed line says so in `merge_changes` in the drafts. A human should settle this rule (queue item 9).
- One pole call was downgraded present to unsure at merge (mly_Kolkata_906852491733079: lane signboards look wall-mounted, not standing posts).

## 4. Who labelled, and how much to trust it

These are TEAM LABELS MADE WITH AI ASSISTANCE. Claude looked at every full image (Read tool) and labelled it. To fit the 21:30 deadline the 100 were split in three batches: idx 000 to 032 labelled by the lead session, 033 to 065 and 066 to 097 by two forks of the same session that shared one written guide. The lead then (a) drew every present box onto its image and checked all 34 images that carry boxes by eye, (b) re-viewed 9 negatives from the fork batches, (c) harmonised the parked-vehicle rule. No label was made by looking at /analyze output (the detectors were not consulted while labelling).

Not done yet, and needed before the number is quoted as final: one human pass, starting with `C6-REVIEW-QUEUE.md`.

## 5. Known weak spots

| weak spot | effect |
|---|---|
| kerb ramp and steps have only 4 present each | their precision / recall swing with one image; the 95 % bootstrap CI in C6-RESULTS.md shows it |
| many unsure (10 to 41 per class) | scored sets are 58 to 88 images per class, not 100 |
| 2 images (mlypair_Panaji_1763999497392607, mlypair_Panaji_2910646599241549) have no /analyze receipt yet | reported as coverage gaps |
| village (5), snow (1), highway (1) groups are tiny | per-condition numbers there are anecdotes, not rates |
| online images are not photo-walk images (framing chosen by photographers, few kerb-level close-ups) | C6 is met in spirit (our own labels on Indian streets), but a real photo walk would add kerb close-ups |
