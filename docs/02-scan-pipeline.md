# 02, the scan pipeline, with the actual maths

hermes, 2026-10-25 02:25 IST. Scope: `app/analyze/raasta/*`. Every formula below is copied from the code with
its line number, so you can diff this page against the source. Numbers marked **measured** come from a run whose
output file is named; **ASSUMPTION** marks a value the code chooses rather than derives.

Stage order is the event order the server emits: `queued, start, intake, detector_a, detector_b, agreement,
vlm_start, footpath_mask, depth, measure, vlm, impact, reasoner_start, reasoner, placement, receipt, end`
(`app/analyze/LIVE-SCAN.md:17`).

## 1. Intake and condition

`raasta/intake.py` rotates by EXIF, reads GPS and heading when present, and bins the frame into light
(day/dusk/night/night_lit/night_or_indoor), blur (sharp/soft/blurry) and haze (clear/hazy), producing
`condition_bin` as `light/blur/haze` (`RECEIPT-SCHEMA.md:16`). Rain is explicitly `"not checked"` in the schema,
which is the honest state: we do not have a rain classifier, we have a user report and a weather feed.

Sun position is computed in `raasta/sun.py:15-17` from the standard solar equations (day angle `g`, equation of
time `eqt`, declination `decl`), used by the shadow route below. If capture time or GPS is missing, `sun` is
`null` and the shadow route returns "no shadow evidence" rather than guessing.

**Measured:** intake 0.11 to 0.60 s across the three recorded runs (`LIVE-SCAN.md:84-86`).

## 2. Two detectors and the agreement rule

Detector A is YOLOE-11s-seg with 14 text prompts (`raasta/models.py:78`, `conf=A_CONF, iou=0.5, imgsz=640,
half=True` on GPU). Detector B is OWLv2 with the same prompts. Both return boxes, labels and scores; nothing is
thresholded into a claim at this stage.

Agreement is a greedy one-to-one match, highest combined score first (`raasta/pipeline.py:49`), where a match
counts only if

```
iou(A.box, B.box) >= IOU_AGREE          # raasta/config.py:58, IOU_AGREE = 0.30
and family_group(A.class) == family_group(B.class)   # raasta/config.py:39 AGREE_GROUPS, :52 helper
```

and the matched box does not sit on the carriageway (stage 4). The IoU itself is the plain intersection over
union, `raasta/pipeline.py:14`. A detection then becomes:

- `ACCEPT` when both detectors agree under the rule above and the ground reads as footpath,
- `ABSTAIN` when one detector fires above `single_min` (default policy: needs both), or when the context stage
  demotes a carriageway agreement, or when the VLM denies it,
- `REJECT` otherwise.

**Measured example:** the street recording produced 1 ACCEPT, 10 ABSTAIN, 30 REJECT on one frame
(`LIVE-SCAN.md:84`). That ratio is not a bug, it is the policy: precision bought with abstention.

## 3. Footpath context, SegFormer-B0

The mask decides whether the ground under a box is footpath, carriageway, mixed or unknown, and reports
`footpath_frac` and `ground_frac` (`RECEIPT-SCHEMA.md:46`). An A+B agreement whose ground reads as carriageway
becomes ABSTAIN, which removed 428 false accepts in the run recorded in `app/analyze/RESULTS.md`.

**Measured:** mask 0.09 to 1.31 s (`LIVE-SCAN.md:84-86`).

## 4. Height, three routes, and the acceptance rule

Heights exist only for kerb and step families, and only when at least two of three routes agree within **6 cm
and 40 percent** (`app/analyze/RESULTS.md`). 36 of 289 kerb and step detections reached that bar, which is the
number to quote whenever someone asks how good the measurement is.

### Route 1, metric depth (`raasta/measure.py:144-176`)

Depth Anything V2 metric outdoor small (`raasta/config.py:72`). Take the median depth in a thin band at the
bottom and top of the box:

```
band = max(2, box_height // 10)
z_b  = median(depth[y2-band : y2, cx1:cx2])     # ground contact
z_t  = median(depth[y1 : y1+band, cx1:cx2])     # top of object
```

Rejects if either depth is outside 0.3 to 40 m, or if `z_t > 1.6 * z_b`, which means the box top is background
rather than the object. Then, for every focal length in `f_range + (f,)`, every horizon `v_h ± err`, and every
metric scale error `s ∈ {0.85, 1.0, 1.15}` (**ASSUMPTION**, about 15 percent):

```
v_b = y2 - band/2 ,  v_t = y1 + band/2
h_m = ((v_h - v_t) * z_t * s - (v_h - v_b) * z_b * s) / f
```

The result is `100 * h_m` cm, with `err_cm` from the span of all combinations, then rejected if outside the
plausible band for the prompt.

### Route 2, camera-height geometry (`raasta/measure.py:180-198`)

Assumes a level camera at a known height and the box bottom on the ground plane:

```
h_cm = 100 * h_c * (y2 - y1) / (y2 - v_h)      for h_c in CAM_HEIGHT_M, v_h ± err
```

Rejects when `y2 - v_h < 0.03 * image_height`, i.e. the box bottom is not clearly below the horizon, which is
the case where this route is meaningless rather than merely imprecise.

### Route 3, shadow altimetry (`raasta/measure.py:202-259`)

Needs sun elevation, camera heading and daylight, and refuses otherwise:

```
shadow_dir  = (sun.azimuth + 180) mod 360
kerb_normal = (heading + 180) mod 360
alpha       = signed angle between them
reject if |cos(alpha)| < 0.35        # shadow too oblique to measure
```

Then it looks for the kerb's dark band in a strip below the box, using a simple threshold:

```
prof = mean grey value per row
dark = prof < 0.65 * median(prof)     # longest dark run = shadow width in rows
```

Ground scale at two rows, and the height from the shadow width:

```
g(r) = f * h_c / (r - v_h)
w    = |g(r2) - g(r1)|                # shadow width in metres on the ground
h_m  = w * tan(radians(sun.elevation + de)) / |cos(alpha)| ,  de ∈ {-1, 0, +1} degrees
```

That ±1 degree on elevation is **ASSUMPTION** for atmospheric refraction and ephemeris error, and the plausible
band for kerbs is `KERB_PLAUSIBLE_CM`.

**Measured:** measure stage 0.02 to 0.12 s (`LIVE-SCAN.md:84-86`).

## 5. The two API models

`raasta/vlm.py` asks `mimo-v2.6-flash` for a short visual verdict (visible / not_visible / cannot_determine)
and `deepseek-v4.1-flash` for a text reason, with a 12 s cap on the vision call and 8 s on the reasoner
(`LIVE-SCAN.md:96`). The only power they have is **demotion**: the VLM can turn an ABSTAIN into a REJECT on
"deny" and can never promote anything to ACCEPT (`LIVE-SCAN.md:104`).

**Honest state:** both returned 401 for every model tried tonight, so this stage never ran
(`LIVE-SCAN.md:23-31`). The page and the receipt say "vision check unavailable in this build" rather than
implying it worked.

## 6. Placement, the 0.7 rule

`raasta/place.py` sends the box, GPS, heading and `gps_error_m` to the routing service, which returns candidate
segments with probabilities. Attach happens only at `p >= 0.7`; below that the record is `pending` with the top
five candidates (`RECEIPT-SCHEMA.md:23`). **Measured:** the Jaipur dry run attached 0 of 130 photos, and the four
records inside the bbox scored 0.14 and 0.26 (`PHASE2-MAP.md`, clause 1).

## 7. The receipt, which is the actual product

Everything above lands in one JSON per image, `raasta-receipt-v1`, with `id = rx-<sha256[:12]>`, per-stage
timings, thresholds, model ids and per-detection `why` strings (`RECEIPT-SCHEMA.md:9-29`). The schema is
append-only: fields may be added, none renamed. That constraint is why a receipt from tonight can be compared
with one from tomorrow.

**Measured end to end:** 10.56 s street, 6.61 s hallway, 4.35 s night (`LIVE-SCAN.md:84-86`), and a queue test
where the second of two scans posted 0.3 s apart waited 4.98 s and finished at 11.26 s (`LIVE-SCAN.md:91`).

## 8. What is weakest, in one list

1. Detector A and B can agree on a wrong label; the hallway run agreed on "electric box" for a chair
   (`LIVE-SCAN.md:101`).
2. Heights are rare (36 of 289) because the three routes rarely agree.
3. The VLM and reasoner have never run, so the demotion path is untested in production.
4. Placement, not detection, is what stops Jaipur from showing a single barrier.
5. Micro F1 is 0.23 on our own 100 images, with 46 dev and 54 test and a shipped policy that only changes the
   pole class (`CALIBRATION.md:53-66`).
