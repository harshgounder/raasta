# C6 results: /analyze vs our own labelled Indian images

generated 2026-10-24T19:35:06+05:30 by `eval/eval_c6.py` (stdlib + numpy, `python3 -I`).
labels: `app/analyze/calib/c6-test.jsonl` (54 images). Labels are TEAM LABELS MADE WITH AI ASSISTANCE and still need one human pass (see `data/labels/C6-REVIEW-QUEUE.md`).

Rules: a class counts as predicted on an image when the receipt has at least one ACCEPT detection of that class family. ABSTAIN (no ACCEPT, at least one ABSTAIN) counts as not predicted in the main numbers and is reported as the abstain rate; the 'answered only' column drops abstained images. `unsure` labels are excluded per class. Images with no receipt are coverage gaps, not misses. Box level: greedy one-to-one match by confidence at IoU >= 0.3.

## Headline (run with the widest coverage: `app/analyze/out/online-v2-cal`, 53 of 54 labelled images)

| class | scored | GT+ | image P | image R | image F1 | abstain rate | box R @ IoU 0.3 |
|---|---|---|---|---|---|---|---|
| missing_kerb_ramp | 30 | 1 | n/a | 0.00 | 0.00 | 0.27 | 0.00 |
| steps | 49 | 3 | 0.50 | 0.33 | 0.40 | 0.22 | 0.00 |
| broken_or_missing_footpath | 39 | 18 | 0.00 | 0.00 | 0.00 | 0.90 | 0.00 |
| pole_obstruction | 38 | 5 | 0.17 | 0.60 | 0.26 | 0.16 | 0.42 |
| parked_vehicle | 29 | 5 | 0.38 | 0.60 | 0.46 | 0.41 | 0.22 |
| micro, 5 classes | | | 0.23 | 0.22 | 0.23 | | |

Small GT+ counts (kerb ramp 4, steps 4) make those rows anecdotes; see the bootstrap CI per run below.

## Label counts (computed from the jsonl)

| class | present | absent | unsure | boxes |
|---|---|---|---|---|
| missing_kerb_ramp | 1 | 30 | 23 | 1 |
| steps | 3 | 47 | 4 | 4 |
| broken_or_missing_footpath | 19 | 21 | 14 | 26 |
| pole_obstruction | 5 | 33 | 16 | 12 |
| parked_vehicle | 5 | 25 | 24 | 9 |

| condition group | images |
|---|---|
| day_dry | 35 |
| commercial | 25 |
| market | 13 |
| residential | 13 |
| rain_wet_flood | 10 |
| night | 8 |
| view_from_vehicle | 6 |
| hill | 6 |
| old_city_lane | 6 |
| dusk | 3 |
| village | 2 |
| informal_settlement | 1 |

## Run `app/analyze/out/online-v2-cal`

receipt files 313, valid receipts 313; labelled images covered: **53 of 54**.
not covered (1): `mlypair_Panaji_2910646599241549.jpg`

| class | scored imgs | GT+ | P | R | F1 | F1 95% CI | answered-only P / R | ACCEPT-or-ABSTAIN P / R | abstain rate | box P | box R (IoU 0.3) | GT boxes | pred boxes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| missing_kerb_ramp | 30 | 1 | n/a | 0.00 | 0.00 | 0.0 to 0.0 | n/a / n/a | 0.12 / 1.00 | 0.27 | n/a | 0.00 | 1 | 0 |
| steps | 49 | 3 | 0.50 | 0.33 | 0.40 | 0.0 to 1.0 | 0.50 / 1.00 | 0.23 / 1.00 | 0.22 | 0.00 | 0.00 | 4 | 2 |
| broken_or_missing_footpath | 39 | 18 | 0.00 | 0.00 | 0.00 | 0.0 to 0.0 | 0.00 / 0.00 | 0.46 / 0.94 | 0.90 | 0.00 | 0.00 | 25 | 3 |
| pole_obstruction | 38 | 5 | 0.17 | 0.60 | 0.26 | 0.0 to 0.5 | 0.17 / 1.00 | 0.21 / 1.00 | 0.16 | 0.12 | 0.42 | 12 | 41 |
| parked_vehicle | 29 | 5 | 0.38 | 0.60 | 0.46 | 0.0 to 0.75 | 0.38 / 0.75 | 0.20 / 0.80 | 0.41 | 0.13 | 0.22 | 9 | 15 |
| micro (5 classes) | | | 0.23 | 0.22 | 0.23 | | | | | | | | |

Image-level F1 by condition (n = scored images for that class in that group; groups with n < 5 are noise):

| condition | missing_kerb_ramp | steps | broken_or_missing_footpath | pole_obstruction | parked_vehicle |
|---|---|---|---|---|---|
| all | F1 0.00 (P n/a R 0.00, abst 0.27, n 30) | F1 0.40 (P 0.50 R 0.33, abst 0.22, n 49) | F1 0.00 (P 0.00 R 0.00, abst 0.90, n 39) | F1 0.26 (P 0.17 R 0.60, abst 0.16, n 38) | F1 0.46 (P 0.38 R 0.60, abst 0.41, n 29) |
| day_dry | F1 n/a (P n/a R n/a, abst 0.22, n 23) | F1 0.50 (P 0.50 R 0.50, abst 0.26, n 31) | F1 0.00 (P 0.00 R 0.00, abst 0.92, n 26) | F1 0.33 (P 0.21 R 0.75, abst 0.12, n 25) | F1 0.57 (P 0.50 R 0.67, abst 0.44, n 18) |
| commercial | F1 n/a (P n/a R n/a, abst 0.27, n 11) | F1 n/a (P n/a R n/a, abst 0.29, n 24) | F1 0.00 (P 0.00 R 0.00, abst 0.88, n 16) | F1 0.50 (P 0.38 R 0.75, abst 0.24, n 17) | F1 0.60 (P 0.50 R 0.75, abst 0.31, n 13) |
| market | F1 n/a (P n/a R n/a, abst 0.00, n 7) | F1 n/a (P n/a R n/a, abst 0.27, n 11) | F1 0.00 (P 0.00 R 0.00, abst 0.90, n 10) | F1 0.00 (P 0.00 R 0.00, abst 0.36, n 11) | F1 0.50 (P 0.50 R 0.50, abst 0.40, n 5) |
| residential | F1 0.00 (P n/a R 0.00, abst 0.33, n 6) | F1 0.00 (P 0.00 R n/a, abst 0.27, n 11) | F1 0.00 (P 0.00 R 0.00, abst 0.71, n 7) | F1 0.00 (P 0.00 R n/a, abst 0.00, n 8) | F1 0.00 (P 0.00 R n/a, abst 0.20, n 5) |
| rain_wet_flood | F1 n/a (P n/a R n/a, abst 0.40, n 5) | F1 0.00 (P n/a R 0.00, abst 0.22, n 9) | F1 0.00 (P n/a R 0.00, abst 0.75, n 8) | F1 0.00 (P 0.00 R n/a, abst 0.12, n 8) | F1 0.67 (P 0.50 R 1.00, abst 0.20, n 5) |
| night | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 n/a (P n/a R n/a, abst 0.12, n 8) | F1 0.00 (P n/a R 0.00, abst 1.00, n 5) | F1 0.00 (P 0.00 R n/a, abst 0.40, n 5) | F1 0.67 (P 0.50 R 1.00, abst 0.40, n 5) |
| view_from_vehicle | F1 n/a (P n/a R n/a, abst 0.67, n 3) | F1 n/a (P n/a R n/a, abst 0.20, n 5) | F1 0.00 (P n/a R 0.00, abst 1.00, n 4) | F1 0.00 (P 0.00 R n/a, abst 0.00, n 3) | F1 n/a (P n/a R n/a, abst 1.00, n 3) |
| hill | F1 n/a (P n/a R n/a, abst 0.40, n 5) | F1 1.00 (P 1.00 R 1.00, abst 0.00, n 5) | F1 0.00 (P n/a R 0.00, abst 1.00, n 6) | F1 0.00 (P 0.00 R n/a, abst 0.17, n 6) | F1 n/a (P n/a R n/a, abst 0.50, n 4) |
| old_city_lane | F1 n/a (P n/a R n/a, abst 0.00, n 6) | F1 n/a (P n/a R n/a, abst 0.20, n 5) | F1 0.00 (P n/a R 0.00, abst 1.00, n 5) | F1 0.00 (P 0.00 R n/a, abst 0.00, n 3) | F1 n/a (P n/a R n/a, abst 0.75, n 4) |
| dusk | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 3) | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 0.00 (P 0.00 R 0.00, abst 0.33, n 3) |
| village | F1 n/a (P n/a R n/a, abst 0.00, n 2) | F1 n/a (P n/a R n/a, abst 0.00, n 2) | F1 0.00 (P n/a R 0.00, abst 0.50, n 2) | F1 0.00 (P 0.00 R n/a, abst 0.00, n 2) | F1 n/a (P n/a R n/a, abst 0.00, n 1) |
| informal_settlement | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 n/a (P n/a R n/a, abst 0.00, n 1) | F1 0.00 (P n/a R 0.00, abst 1.00, n 1) | - | F1 n/a (P n/a R n/a, abst 1.00, n 1) |

