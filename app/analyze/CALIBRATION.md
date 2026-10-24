# CALIBRATION: per-class decision policy tuned on C6 dev, scored on dev AND test (2026-10-24 ~20:05 IST)

Inputs: `data/labels/c6-v1.jsonl` (100 team labels, AI-assisted, human pass pending), receipts of
`out/online-v2` (313 images, 98 of the 100 labelled ones covered), official scorer `eval/eval_c6.py`
(run with `--out-md/--out-json` into `calib/`. Outputs in `eval/` are never written by this lane.
One early run did overwrite `eval/C6-RESULTS.md` and `eval/c6-results.json` by accident; both were
restored with `git checkout` right away and git now shows them clean).

## Split (fixed, before any tuning)

`sha1(basename(file))` even -> dev, odd -> test: **dev 46, test 54** (`calib/c6-dev.jsonl`,
`calib/c6-test.jsonl`). Positives (image level, `unsure` excluded):

| class | dev GT+ / scored | test GT+ / scored |
|---|---|---|
| missing_kerb_ramp | 3 / 28 | 1 / 30 |
| steps | 0 / 39 | 3 / 49 |
| broken_or_missing_footpath | 15 / 30 | 18 / 39 |
| pole_obstruction | 8 / 30 | 5 / 38 |
| parked_vehicle | 3 / 30 | 5 / 29 |

Kerb ramp, steps and parked vehicle have too few positives on either side to tune or to read
anything from. The bootstrap CIs in `calib/eval-*.md` show this.

## What can change (raasta/policy.py, live and offline)

No model is retrained and no threshold of the detectors themselves changes. Only the decision on
top of the stored scores changes, per C6 class:
- `single_A` / `single_B`: a one-detector hit with score >= t becomes ACCEPT with a **lower evidence
  tier** (`evidence_tier: "single detector (calibrated for this class, lower tier)"`). The default
  needs both detectors.
- `context_downgrade`: an A+B agreement on the carriageway becomes ABSTAIN (on-footpath families).
Grid: single_A in {off, .10, .15, .20, .25, .30, .40}, single_B in {off, .20, .25, .30, .35, .40, .50},
context on/off. The objective is dev image-level F1. Ties go to higher precision, then to the simpler rule.

## Round 1, "naive" (best dev F1 per class, >= 3 dev positives)

| class | chosen | dev F1 (default -> chosen) | test F1 (default -> chosen) | test "yes on every image" F1 |
|---|---|---|---|---|
| missing_kerb_ramp | A>=.10 or B>=.40 | 0.00 -> 0.67 | 0.00 -> 0.00 (1 positive) | 0.06 |
| steps | default (0 dev positives) | n/a | 0.40 -> 0.40 | 0.12 |
| broken_or_missing_footpath | B>=.20 | 0.00 -> 0.67 | 0.00 -> **0.61** | **0.63** |
| pole_obstruction | B>=.30 | 0.71 -> 0.84 | 0.27 -> 0.26 | 0.23 |
| parked_vehicle | A>=.10 or B>=.30 | 0.00 -> 0.30 | **0.46 -> 0.36** | 0.29 |
| **micro (5 classes)** | | 0.24 -> 0.62 | 0.22 -> **0.47** | |

Reading: the micro gain on test comes almost entirely from broken/missing footpath. There, a
single OWLv2 hit at >= 0.20 fires on nearly every image (recall 0.94, precision 0.45). That scores
**below "say yes on every image" (0.63)** because 46 % of test images are positive. The rule carries
no information. Pole did not carry over (0.27 -> 0.26). Parked vehicle got worse (0.46 -> 0.36).
Kerb ramp was tuned on 3 positives. **Round 1 overfit dev.**

## Round 2, "guarded" (SHIPPED as `calib/policy.json`)

Guard added: a class changes only if it has >= 5 dev positives AND its best dev F1 beats both the
default rule and "yes on every image" by >= 0.05 on dev. Only **pole_obstruction (B >= 0.30)** passes.
Everything else keeps the two-detector rule.

| | dev micro P / R / F1 | test micro P / R / F1 |
|---|---|---|
| default (two detectors, carriageway -> ABSTAIN) | 0.38 / 0.17 / 0.24 | 0.27 / 0.19 / 0.22 |
| round 1 naive | 0.46 / 0.97 / 0.62 | 0.33 / 0.78 / 0.47 |
| **round 2 guarded (shipped)** | 0.44 / 0.28 / 0.34 | 0.23 / 0.22 / **0.23** |

Per class on test, guarded: kerb 0.00, steps 0.40, broken/missing footpath 0.00 (ABSTAIN 90 %),
pole 0.26, parked vehicle 0.46.

**Honesty note on leakage:** the round-2 guard was written after seeing the round-1 test numbers.
So round 2's test score is not a clean held-out number. It is a "no worse than default" check.
The clean held-out result is round 1: **the per-class rules learned on dev did not generalise,
apart from the trivial area-class rule.** A real gain needs better evidence (a kerb-ramp
classifier, footpath segmentation trained on Indian streets, more labels), not threshold moves.

## Switches

`ANALYZE_POLICY=calibrated` (default, guarded) | `naive` (round 1, for a demo where the
broken/missing footpath class should say yes with a lower tier) | `default` (two detectors only).
Every receipt detection carries `base_status` (agreement-only decision) and `evidence_tier`, so the
site can show "single detector" differently.

## Reproduce

```
cd app/analyze
.venv/bin/python tools/calibrate.py --run out/online-v2    # split, grid on dev, eval dev+test -> calib/
```
Outputs: `calib/policy.json` (+ dev log, top-5 grid points per class), `calib/eval-{base,cal}-{dev,test}.{md,json}`,
`calib/naive-v1/` (round 1), re-decided receipts in `out/online-v2-base/` and `out/online-v2-cal/`.
