# Receipt schema `raasta-receipt-v1` (app/analyze, stable field names)

One JSON per image, from `POST /analyze` or `cli.py` (`<out>/receipts/<image stem>.json`; the stem is
the image file name without its extension). These names stay fixed. New fields may be added; none
will be renamed or removed without bumping `schema`.

## Top level

| field | type | meaning |
|---|---|---|
| `schema` | str | `"raasta-receipt-v1"` |
| `id` | str | `rx-<sha256[:12]>` of the image bytes |
| `image` | obj | `id` (`img-<sha[:12]>`), `sha256`, `w`, `h`, `filename` |
| `source` | obj | from the sidecar/form when present: `source`, `source_url`, `licence`, `author`, `city` |
| `intake` | obj | `exif{...}`, `lat`, `lon`, `location_source` (form/exif/null), `gps_error_m`, `heading`, `captured_at` (ISO or null), `sun` (null or `{elevation_deg, azimuth_deg, engine, check}`) |
| `condition` | obj | `bin`, `light` (day/dusk/night/night_lit/night_or_indoor), `light_source`, `blur` (sharp/soft/blurry), `haze` (clear/hazy), `rain` ("not checked"), `metrics{...}`, `rules` |
| `condition_bin` | str | `light/blur/haze`, e.g. `day/sharp/clear` |
| `tier` | obj | `tier`: `observed today` / `observed earlier` / `unknown`; `date`, `age_days` when known |
| `counts` | obj | `{ACCEPT, ABSTAIN, REJECT}` over `detections` |
| `detections` | list | see below, sorted ACCEPT, ABSTAIN, REJECT, then by score |
| `judge` | obj | `status` (`used` / `skipped`), `used` (bool), `why` (starts with "judge skipped:" when skipped), `calls`, `answered`, `budget_s`, `budget?` |
| `measure` | obj | `camera{f_px, f_source, height_m_assumed}`, `horizon{v_h, vp_x?, err, source, n_lines}`, `rule` |
| `placement` | obj | `status`: `placed` / `pending` / `nothing_to_place`; `via`, `why`, `result` (the route service's placements) or `records` (when pending) |
| `notes` | list[str] | failures and caveats |
| `timings` | obj | seconds: `intake_s, detect_A_s, detect_B_s, context_s, judge_s, depth_s?, measure_s, place_s, total_s, model_load_s{A,B,S,D}` |
| `models` | obj | model ids and versions, `torch`, `device`, `gpu` |
| `thresholds` | obj | `A_conf, B_conf, iou_agree, single_min{A,B}` |
| `created_at` | str | ISO, IST |
| `annotated_jpeg_b64` | str | only with `POST /analyze?annotated=1` |

## `detections[]`

| field | type | meaning |
|---|---|---|
| `id` | str | `<image.id>-dNN` |
| `class` | str | the prompt that won, one of the 14 prompts in `raasta/config.py PROMPTS` (e.g. `curb without ramp`) |
| `class_family` | str | routing barrier type: `missing_kerb_ramp, steps, broken_footpath, missing_footpath, pole_obstruction, parked_vehicle, pothole, open_drain, vendor`, or the clear type `kerb_ramp_present` |
| `box` | [x1,y1,x2,y2] | pixels in the EXIF-rotated image (`image.w` x `image.h`); for ACCEPT, the mean of the A and B boxes |
| `scores` | `{A, B}` | detector confidences, `null` for a model that did not see it |
| `labels` | `{A?, B?}` | prompt each detector gave |
| `iou_AB` | float | only when both detectors matched |
| `family_conflict` | str | only when A and B matched but chose different families in the same group |
| `status` | str | `ACCEPT` (A and B agree, IoU >= 0.3, same family group, not on the carriageway) / `ABSTAIN` (needs a human look) / `REJECT` |
| `why` | str | one line explaining the status |
| `confidence` | float | heuristic, not a probability: max(A,B) for ACCEPT, score x 0.5 for single-model |
| `footpath_context` | obj | `verdict`: `footpath` / `carriageway` / `mixed` / `unknown`, `footpath_frac`, `ground_frac` (not on REJECT) |
| `judge` | obj | only when the judge was asked: `answer` (`visible` / `not_visible` / `cannot_determine` / null), `reason`, `provider`, `model`, `seconds` or `error` |
| `height` | obj | only for kerb/step families: `height_status` (`ACCEPT` / `ABSTAIN` / `NO_ESTIMATE`), `why`, `routes[]` (`route`, `ok`, `value_cm?`, `err_cm?`, `why?`, `inputs?`), `routes_agreed?`, `riser_box`, `riser_note` |
| `height_cm`, `height_err_cm`, `routes_agreed` | float, float, list | only when `height.height_status == "ACCEPT"`; a height is never present without its error |
| `side_hint` | str/null | `left` / `right` footpath as seen in the image (box vs vanishing point); not on REJECT |
| `distance_m` | float/null | ground distance ahead of the camera (1.45 m camera height assumed); not on REJECT |

## For eval (C6)

- Match receipts to labels by `image.filename` (or the receipt file stem), boxes in `box` pixel space.
- For predicted positives use `status == "ACCEPT"`. Report ABSTAIN separately (abstain rate), never as a positive.
- Compare at the `class_family` level. `class` is finer and depends on the prompt.
