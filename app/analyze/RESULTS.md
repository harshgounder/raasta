# app/analyze: RESULTS (lane B1, claude helper, 2026-10-24, updated ~20:15 IST)

Taken over from dsh (crashed). Everything below was run on this box: GTX 1650 4 GB, ~2 GB free RAM,
torch 2.13.0+cu130 / torchvision 0.28.0+cu130 (consistent pair, NMS on CUDA checked), transformers 5.20.2,
ultralytics 8.4.186. Numbers are computed from `out/*/summary.json` and the receipts by
`tools/summarize.py` and `tools/breakdown.py`, not estimated.

## Gate (19:30): PASSED at ~18:28

`out/gate/` = 3 real Indian photos (2 Wikimedia Commons Jaipur photos from dsh, 1 hermes-b Jaipur street frame),
receipts + annotated images, both detectors running. Result at that time: 5 ACCEPT (A+B agree),
8 ABSTAIN, 60 REJECT; 3.2 to 3.4 s per image warm (the first image paid 56 s of judge timeouts).
The same 3 images were re-run in `out/online-v2/` with the later footpath-context step (see below).

## What the service does

```
POST /analyze (multipart image + lat, lon, heading, captured_at, city, gps_error_m)   server.py
 1 intake    EXIF time / GPS / heading / 35 mm focal; condition bin light/blur/haze       raasta/intake.py
 2 detect A  YOLOE-11s-seg, 14 text prompts, cached text embeddings                        raasta/models.py
   detect B  OWLv2 base patch16 ensemble, same 14 prompts, fp16 GPU
   agree     IoU >= 0.3 + same class family -> ACCEPT; one model only -> ABSTAIN (score >= 0.25) or REJECT
   context   SegFormer-B0 sidewalk model: ground at the object's foot = footpath / carriageway /
             mixed / unknown; a vehicle, pole or vendor that A+B agree on but that stands on the
             carriageway is downgraded to ABSTAIN                                         raasta/pipeline.py
   judge     optional VLM (OpenRouter, then NVIDIA) on ABSTAIN crops, visible / not_visible /
             cannot_determine; keys read from env or ~/.hermes/.env in memory only       raasta/judge.py
 3 measure   kerb / step height: riser edges -> route 1 metric depth (Depth Anything V2 metric
             outdoor small), route 2 vanishing point + camera height 1.2-1.7 m, route 3 shadow
             altimetry (NOAA sun + pvlib cross-check); printed only if >= 2 routes agree and
             err <= 6 cm and <= 40 %                                                       raasta/measure.py, sun.py
 4 place     POST {city, records} to app/route /barriers (port 8020); if down, in-process
             hroute.attach on cache/networks/<city>.pkl (commit=False); else "pending"    raasta/place.py
 5 receipt   raasta-receipt-v1 JSON: id, sha256, detections[{class, class_family, box, scores{A,B},
             status, footpath_context, height{routes...}, height_cm?, height_err_cm?, routes_agreed?,
             side_hint, distance_m}], condition_bin, tier, judge, measure, placement, notes,
             timings, models, thresholds
```

Class families = the routing service's barrier types (missing_kerb_ramp, steps, broken_footpath,
missing_footpath, pole_obstruction, parked_vehicle, pothole, open_drain, vendor, plus the clear type
kerb_ramp_present), so a receipt record goes to /barriers without renaming.

## Full run: `out/online-v2/` (313 images: data/online 310 + 3 gate images)

All 313 processed, 0 crashes. Detections: **330 ACCEPT, 2,098 ABSTAIN, 6,958 REJECT**.

Timings on this box (warm, per image): detector A median 0.08 s; detector B (OWLv2 at 960 px) median
3.80 s, p90 4.58 s; depth 0.68 s when a kerb/step is present (123 images); footpath context ~0.15 s;
**total median 4.26 s, p90 5.78 s**. Cold model loads: A 0.2 s, B 3.7 s, depth 0.3 s, seg 0.1 s (weights
local). The 55-65 s outliers are judge timeouts on the first images.

| family | ACCEPT | ABSTAIN | REJECT |
|---|---|---|---|
| parked_vehicle | 182 | 835 | 1570 |
| pole_obstruction (pole, electric box, bollard) | 69 | 356 | 2109 |
| vendor | 27 | 112 | 336 |
| missing_footpath | 22 | 179 | 578 |
| missing_kerb_ramp | 11 | 80 | 531 |
| pothole | 7 | 119 | 526 |
| steps | 6 | 133 | 845 |
| broken_footpath | 5 | 223 | 245 |
| kerb_ramp_present | 1 | 58 | 208 |
| open_drain | 0 | 3 | 10 |

| source | images | ACCEPT / image |
|---|---|---|
| Commons (cm) | 94 | 1.28 |
| Mapillary (mly) | 43 | 0.81 |
| Mapillary pairs | 15 | 1.20 |
| Panoramax (pmx) | 20 | 0.15 |
| YouTube frames (yt) | 120 | 1.13 |
| YouTube storyboard (ytsb) | 18 | 0.89 |

| light (condition bin) | images | ACCEPT / image |
|---|---|---|
| day | 249 | 1.06 |
| dusk | 24 | 1.17 |
| night | 27 | 0.78 |
| night_lit | 13 | 1.23 |

Per-image table (313 rows): `out/online-v2/SUMMARY.md`; breakdowns: `out/online-v2/BREAKDOWN.md`;
receipts: `out/online-v2/receipts/`; annotated images: `out/online-v2/annotated/`
(ACCEPT solid green, ABSTAIN dashed amber, REJECT not drawn, `[on road]` / `[on footpath]` tags).

Earlier run without the footpath-context step (`out/online-v1/`, 196 images): 501 ACCEPT. The context
step moved 428 A+B agreements to ABSTAIN in v2 because the ground under them reads as carriageway.

### Heights

289 kerb/step detections were measured. 36 reached a printed height (two routes agree, error small);
193 ABSTAIN (one route only, or spread too wide), 60 no plausible value. Only 4 of the 36 sit on an
ACCEPT detection:

| image | class | height |
|---|---|---|
| cm_264_Puducherry_street | curb without ramp | 8.5 +- 2.3 cm |
| cm_264_Puducherry_street | curb without ramp | 11.1 +- 3.2 cm |
| yt_SzDvWkilL_g_maxres3 | step | 24.2 +- 5.2 cm |
| yt_yCt0wJ15p20_maxres3 | curb without ramp | 6.6 +- 1.5 cm (looked at: a real raised kerb, the value looks low) |

**No height is validated.** There is no ruler ground truth (no photo walk, D4). Route 3 (shadow) never
fired: it needs capture time + GPS + heading together, and no online image has all three.
Routes 1 and 2 share the riser rows and the horizon estimate, so their agreement is **weaker than two
independent measurements**. They differ only in where the scale comes from (metric depth vs the
assumed 1.2-1.7 m camera height).

## What is ABSTAIN-heavy, and why

| ABSTAIN reason | count |
|---|---|
| only detector B (OWLv2) sees it | 1,623 |
| A and B agree, but the object stands on the carriageway | 428 |
| only detector A (YOLOE) sees it | 47 |

- OWLv2 proposes many boxes at 0.25-0.35 that YOLOE does not confirm. Most are the broad classes:
  broken_footpath (223 ABSTAIN vs 5 ACCEPT), missing_footpath, pothole, steps.
- Both detectors ignore the "on sidewalk" part of a prompt, so moving cars on the road agree as
  "parked car on sidewalk". The SegFormer context step catches part of this. In Indian mixed streets
  with no footpath, "on the carriageway" can still be a real barrier, so these stay ABSTAIN, not REJECT.
- The judge would settle single-model hits but did not work tonight (next section).
- Panoramax (0.15 ACCEPT/image) and night (0.78) are the weakest bins.

## Judge (VLM): capped, circuit-broken, support only

In the online-v2 batch the judge failed on every provider: OpenRouter free = HTTP 429, paid = 403
(no credit), NVIDIA = repeated ReadTimeouts. It cost up to 55 of 65 s on the first images. Since then (after v2):
- **budget 8 s per image** for all judge calls, enforced as a wall-clock deadline, one provider
  attempt per call, NVIDIA `llama-3.2-11b-vision` first (the only provider that answered);
- **circuit breaker**: 2 failed calls in a row -> judge skipped for 10 min, and the receipt says
  `judge.status: "skipped"` with `judge.why: "judge skipped: ..."`;
- **"visible" no longer promotes ABSTAIN -> ACCEPT** (`JUDGE_CAN_ACCEPT=0`). Sanity test: the judge said
  "visible" to stairs and to an open drain on a shop-roof crop, and in the test runs it said "visible" to
  13 of 13 crops. Only "not_visible" acts (-> REJECT).
Warm server, 4 uploads after the change: 7.4 / 10.0 / 12.3 / 12.9 s per receipt (judge 3.8-8.0 s,
the rest ~4-5 s); with `ANALYZE_JUDGE=0` it is ~3.4-5 s. Startup warms all 4 models (~20 s).

## Decision policy + C6 calibration (see CALIBRATION.md)

`raasta/policy.py` turns stored scores + agreement + footpath context into the status, per C6 class,
live and offline. Tuned on the C6 dev split only, scored on dev and test with `eval/eval_c6.py`.
Test micro F1: default 0.22, round-1 per-class tuning 0.47 (overfit: its gain is the
broken/missing-footpath rule, which is no better than "yes on every image"), **shipped guarded
policy 0.23**. Only pole_obstruction changed (single OWLv2 >= 0.30 -> ACCEPT, lower evidence tier).
Every detection now carries `base_status` and `evidence_tier`.

## Placement + geotagged barrier export (C1 -> C3)

`out/geo-v1`: all 94 geotagged images in data/online (sidecar lat/lon, `camera_heading` now read).
`tools/export_barriers.py` writes ACCEPT + ABSTAIN detections as records in the
`app/route/BARRIERS-INPUT-SCHEMA.md` format to `app/site-data/<city>/barriers.input.json` and copies
the annotated photo to `app/site-data/<city>/evidence/<stem>.jpg` (record `photo`; `ref` = licence;
author; URL; `receipt_ref` = the receipt). Jaipur: 10 images, 13 ACCEPT + 117 ABSTAIN records
(Bagru/NH48 and MUJ go to `jaipur-outskirts`, 1 + 29). All 13 cities are listed in the final report table.

**Dry-run attach on the current networks (commit=False): 0 of 130 Jaipur and 0 of 93 Chandigarh
records attach.** 113 Jaipur records have "no footpath segment within 30 m": the photos lie outside
the small walled-city bbox (75.819-75.833 E, 26.913-26.928 N). The 4 photos inside it give p = 0.14
and 0.26 < 0.7. The network has to cover the photo locations (routing lane) before Jaipur shows
observed barriers. The export reruns in one command once geo-v2 (calibrated policy) finishes.

Online-v2 placement: 213 images have no lat/lon -> `pending`. The route service on :8020 was down,
so the in-process fallback ran.

## Known gaps (honest)

1. **Accuracy is low and the labels are thin.** On the C6 test half (54 images, AI-assisted labels,
   human pass pending), micro image-level F1 = 0.23 (P 0.23, R 0.22). Per class: steps 0.40,
   parked vehicle 0.46, pole 0.26, kerb ramp 0.00, broken/missing footpath 0.00 (90 % ABSTAIN).
   Kerb ramp has 1 test positive and steps 3: these are anecdotes. Details in CALIBRATION.md.
2. Kerb ramp classes are weak: "curb without ramp" 11 ACCEPT, "curb ramp" 1. Open-vocabulary detectors
   do not separate ramp from no-ramp. The Project Sidewalk DINOv2 ramp/no-ramp ONNX heads
   (ASSETS-verified.md) are the obvious next detector for this pair. Not wired in.
3. The footpath-context model was trained on Belgian sidewalks (segments.ai). On Indian scenes it
   labels most ground as road (1,380 carriageway vs 104 footpath verdicts). 865 detections are
   "unknown" because the object hides its own foot.
4. The condition bin is heuristic. Lit night scenes with no sky in the top 12 % of the frame can read
   as day. Rain is not checked.
5. EXIF times can be wrong: the 1970s-looking Backstreet photo carries 2012-01-07 (a scan date), so
   its tier says "observed earlier 2012".
6. `project-sidewalk/` in data/online is empty (its imagery is Google Street View, which is out per
   D4), so no Project Sidewalk examples were run.
7. Licences: the YouTube frames are standard-licence (demo with attribution only), and
   `out/*/annotated/` contains derived copies of them. Decide before committing `out/` to a repo that
   goes public.
8. HF downloads stalled on this network, so the weights were fetched with `tools/pfetch.py`
   (parallel ranges) into `weights/` (gitignored, 1.3 GB including the 572 MB MobileCLIP file that is
   only needed to rebuild the text embeddings).

## Run

```
cd app/analyze
uv venv --python 3.12 .venv; uv pip install --python .venv/bin/python -r requirements.lock
python3 tools/pfetch.py google/owlv2-base-patch16-ensemble weights/owlv2-base-patch16-ensemble
python3 tools/pfetch.py depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf weights/da2-metric-outdoor-small
python3 tools/pfetch.py malra/segformer-b0-finetuned-segments-sidewalk-4 weights/segformer-sidewalk --skip .h5,.msgpack,.onnx
# yoloe-11s-seg.pt + mobileclip_blt.ts in weights/, then once:
.venv/bin/python tools/make_text_pe.py
HF_HUB_OFFLINE=1 .venv/bin/uvicorn server:app --host 127.0.0.1 --port 8010      # POST /analyze, ?annotated=1
HF_HUB_OFFLINE=1 .venv/bin/python cli.py IN_DIR --out OUT_DIR [--no-judge]       # batch + annotated images
python3 tools/summarize.py OUT_DIR/summary.json; python3 tools/breakdown.py OUT_DIR
```
Env knobs: `ANALYZE_JUDGE=0`, `ANALYZE_JUDGE_MAX`, `JUDGE_TIMEOUT_S`, `JUDGE_BUDGET_S`, `ROUTE_URL`,
`ANALYZE_LOW_MEM=1` (unload each model after use), `ANALYZE_CPU=1`.
Server smoke test (19:12): HTTP 200, 14.4 s on the second request (B still warming), annotated JPEG
returned, in-process placement ran.
