# C6 results: /analyze vs our own labelled Indian images

generated 2026-10-24T19:34:36+05:30 by `eval/eval_c6.py` (stdlib + numpy, `python3 -I`).
labels: `app/analyze/calib/c6-dev.jsonl` (46 images). Labels are TEAM LABELS MADE WITH AI ASSISTANCE and still need one human pass (see `data/labels/C6-REVIEW-QUEUE.md`).

Rules: a class counts as predicted on an image when the receipt has at least one ACCEPT detection of that class family. ABSTAIN (no ACCEPT, at least one ABSTAIN) counts as not predicted in the main numbers and is reported as the abstain rate; the 'answered only' column drops abstained images. `unsure` labels are excluded per class. Images with no receipt are coverage gaps, not misses. Box level: greedy one-to-one match by confidence at IoU >= 0.3.

## Headline (run with the widest coverage: `app/analyze/out/online-v2-base`, 45 of 46 labelled images)

| class | scored | GT+ | image P | image R | image F1 | abstain rate | box R @ IoU 0.3 |
|---|---|---|---|---|---|---|---|
| missing_kerb_ramp | 28 | 3 | 0.00 | 0.00 | 0.00 | 0.25 | 0.00 |
| steps | 39 | 0 | n/a | n/a | n/a | 0.26 | n/a |
| broken_or_missing_footpath | 30 | 15 | 0.00 | 0.00 | 0.00 | 0.87 | 0.00 |
| pole_obstruction | 30 | 8 | 0.83 | 0.62 | 0.71 | 0.33 | 0.18 |
| parked_vehicle | 30 | 3 | 0.00 | 0.00 | 0.00 | 0.60 | 0.00 |
| micro, 5 classes | | | 0.38 | 0.17 | 0.24 | | |

Small GT+ counts (kerb ramp 4, steps 4) make those rows anecdotes; see the bootstrap CI per run below.

## Label counts (computed from the jsonl)

| class | present | absent | unsure | boxes |
|---|---|---|---|---|
| missing_kerb_ramp | 3 | 25 | 18 | 3 |
| steps | 1 | 39 | 6 | 2 |
| broken_or_missing_footpath | 15 | 15 | 16 | 21 |
| pole_obstruction | 9 | 22 | 15 | 13 |
| parked_vehicle | 3 | 28 | 15 | 6 |

| condition group | images |
|---|---|
| day_dry | 31 |
| commercial | 20 |
| rain_wet_flood | 13 |
| market | 12 |
| residential | 8 |
| night | 5 |
| old_city_lane | 5 |
| hill | 4 |
| view_from_vehicle | 4 |
| village | 3 |
| highway | 1 |
| snow | 1 |

## Run `app/analyze/out/online-v2-base`

receipt files 313, valid receipts 313; labelled images covered: **45 of 46**.
not covered (1): `mlypair_Panaji_1763999497392607.jpg`

| class | scored imgs | GT+ | P | R | F1 | F1 95% CI | answered-only P / R | ACCEPT-or-ABSTAIN P / R | abstain rate | box P | box R (IoU 0.3) | GT boxes | pred boxes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| missing_kerb_ramp | 28 | 3 | 0.00 | 0.00 | 0.00 | 0.0 to 0.0 | 0.00 / 0.00 | 0.25 / 0.67 | 0.25 | 0.00 | 0.00 | 3 | 1 |
| steps | 39 | 0 | n/a | n/a | n/a | n/a | n/a / n/a | 0.00 / n/a | 0.26 | n/a | n/a | 0 | 0 |
| broken_or_missing_footpath | 30 | 15 | 0.00 | 0.00 | 0.00 | 0.0 to 0.0 | 0.00 / 0.00 | 0.50 / 0.93 | 0.87 | 0.00 | 0.00 | 21 | 2 |
| pole_obstruction | 30 | 8 | 0.83 | 0.62 | 0.71 | 0.333 to 0.933 | 0.83 / 1.00 | 0.50 / 1.00 | 0.33 | 0.22 | 0.18 | 11 | 9 |
| parked_vehicle | 30 | 3 | 0.00 | 0.00 | 0.00 | 0.0 to 0.0 | 0.00 / n/a | 0.14 / 1.00 | 0.60 | 0.00 | 0.00 | 6 | 5 |
| micro (5 classes) | | | 0.38 | 0.17 | 0.24 | | | | | | | | |

Image-level F1 by condition (n = scored images for that class in that group; groups with n < 5 are noise):

| condition | missing_kerb_ramp | steps | broken_or_missing_footpath | pole_obstruction | parked_vehicle |
|---|---|---|---|---|---|
| all | F1 0.00 (P 0.00 R 0.00, abst 0.25, n 28) | F1 n/a (P n/a R n/a, abst 0.26, n 39) | F1 0.00 (P 0.00 R 0.00, abst 0.87, n 30) | F1 0.71 (P 0.83 R 0.62, abst 0.33, n 30) | F1 0.00 (P 0.00 R 0.00, abst 0.60, n 30) |
| day_dry | F1 0.00 (P 0.00 R 0.00, abst 0.17, n 18) | F1 n/a (P n/a R n/a, abst 0.20, n 25) | F1 0.00 (P 0.00 R 0.00, abst 0.91, n 22) | F1 0.67 (P 0.80 R 0.57, abst 0.36, n 22) | F1 0.00 (P 0.00 R 0.00, abst 0.67, n 21) |
| commercial | F1 0.00 (P n/a R 0.00, abst 0.44, n 9) | F1 n/a (P n/a R n/a, abst 0.29, n 17) | F1 0.00 (P n/a R 0.00, abst 0.92, n 12) | F1 0.77 (P 0.83 R 0.71, abst 0.36, n 14) | F1 0.00 (P 0.00 R 0.00, abst 0.69, n 13) |
| rain_wet_flood | F1 0.00 (P n/a R 0.00, abst 0.50, n 8) | F1 n/a (P n/a R n/a, abst 0.33, n 12) | F1 0.00 (P n/a R 0.00, abst 0.86, n 7) | F1 1.00 (P 1.00 R 1.00, abst 0.33, n 6) | F1 0.00 (P 0.00 R 0.00, abst 0.50, n 8) |
| market | F1 0.00 (P n/a R 0.00, abst 0.00, n 7) | F1 n/a (P n/a R n/a, abst 0.11, n 9) | F1 0.00 (P 0.00 R 0.00, abst 0.57, n 7) | F1 0.67 (P 1.00 R 0.50, abst 0.50, n 8) | F1 0.00 (P 0.00 R 0.00, abst 0.60, n 5) |
| residential | F1 n/a (P n/a R n/a, abst 0.50, n 4) | F1 n/a (P n/a R n/a, abst 0.29, n 7) | F1 0.00 (P n/a R 0.00, abst 1.00, n 4) | F1 n/a (P n/a R n/a, abst 0.00, n 2) | F1 0.00 (P 0.00 R n/a, abst 0.67, n 6) |
| night | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 4) | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 n/a (P n/a R n/a, abst 0.00, n 2) | F1 0.00 (P n/a R 0.00, abst 1.00, n 2) |
| old_city_lane | F1 0.00 (P 0.00 R n/a, abst 0.00, n 5) | F1 n/a (P n/a R n/a, abst 0.33, n 3) | F1 0.00 (P 0.00 R 0.00, abst 0.50, n 4) | F1 n/a (P n/a R n/a, abst 0.50, n 4) | F1 n/a (P n/a R n/a, abst 0.00, n 1) |
| hill | F1 n/a (P n/a R n/a, abst 0.00, n 3) | F1 n/a (P n/a R n/a, abst 0.25, n 4) | F1 0.00 (P 0.00 R 0.00, abst 0.50, n 2) | F1 n/a (P n/a R n/a, abst 0.25, n 4) | F1 n/a (P n/a R n/a, abst 0.50, n 4) |
| view_from_vehicle | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 n/a (P n/a R n/a, abst 0.00, n 4) | F1 0.00 (P n/a R 0.00, abst 1.00, n 1) | F1 1.00 (P 1.00 R 1.00, abst 0.00, n 2) | F1 0.00 (P n/a R 0.00, abst 1.00, n 3) |
| village | F1 n/a (P n/a R n/a, abst 0.00, n 3) | F1 n/a (P n/a R n/a, abst 0.33, n 3) | F1 0.00 (P n/a R 0.00, abst 1.00, n 2) | F1 n/a (P n/a R n/a, abst 0.00, n 3) | F1 n/a (P n/a R n/a, abst 0.33, n 3) |
| highway | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 0.00 (P n/a R 0.00, abst 1.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 1.00, n 1) |
| snow | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 1.00, n 1) | - | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 1) |

