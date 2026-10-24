"""Calibrate the per-class decision policy on the C6 DEV split only, then score dev AND test.

  .venv/bin/python tools/calibrate.py --run out/online-v2

1. split data/labels/c6-v1.jsonl by sha1(basename) into dev / test (fixed, ~50/50) -> calib/c6-{dev,test}.jsonl
2. re-run raasta.policy.decide offline on the run's receipts (scores, agreement and footpath context
   are in the receipts) for each grid point; score image-level F1 per class on DEV with the same rule
   as eval/eval_c6.py (ACCEPT of the class = predicted; `unsure` labels excluded)
3. pick per class: best dev F1; ties -> higher precision -> the default (simpler) rule. A class with
   fewer than MIN_POS dev positives keeps the default (too few to tune)
4. write calib/policy.json, re-decided receipts to out/<run>-cal/ (and out/<run>-base/ with the default
   policy), then run eval/eval_c6.py on dev and test for both, outputs in calib/ (never eval/)
"""
from __future__ import annotations

import argparse
import copy
import glob
import hashlib
import itertools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from raasta import policy as pol  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
LABELS = os.path.join(REPO, "data", "labels", "c6-v1.jsonl")
EVAL = os.path.join(REPO, "eval", "eval_c6.py")
CAL = os.path.join(HERE, "calib")
CLASSES = ["missing_kerb_ramp", "steps", "broken_or_missing_footpath", "pole_obstruction", "parked_vehicle"]
MIN_POS = 5          # guard (v2): fewer dev positives = keep the default
MARGIN = 0.05        # guard (v2): must beat the default AND "say yes on every image" by this on dev
BASE_POLICY = {"_other": {"context_downgrade": True}}
GRID_A = [None, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]
GRID_B = [None, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50]
GRID_CTX = [True, False]


def split():
    dev, test = [], []
    for line in open(LABELS, encoding="utf-8"):
        if not line.strip():
            continue
        d = json.loads(line)
        h = int(hashlib.sha1(os.path.basename(d["file"]).encode()).hexdigest(), 16)
        (dev if h % 2 == 0 else test).append(line.rstrip("\n"))
    os.makedirs(CAL, exist_ok=True)
    for name, rows in (("dev", dev), ("test", test)):
        with open(os.path.join(CAL, f"c6-{name}.jsonl"), "w") as f:
            f.write("\n".join(rows) + "\n")
    return [json.loads(x) for x in dev], [json.loads(x) for x in test]


def load_receipts(run):
    out = {}
    for f in glob.glob(os.path.join(run, "receipts", "*.json")):
        r = json.load(open(f))
        out[os.path.basename(r["image"].get("filename") or os.path.basename(f)[:-5] + ".jpg")] = (f, r)
    return out


def redecide(r, policy):
    r = copy.deepcopy(r)
    for d in r["detections"]:
        if "base_status" not in d:
            d["base_status"] = d["status"]
        pol.decide(d, policy)
    r["counts"] = {s: sum(1 for d in r["detections"] if d["status"] == s) for s in ("ACCEPT", "ABSTAIN", "REJECT")}
    r["policy"] = policy
    return r


def f1_for(labels, recs, cls, policy):
    tp = fp = fn = 0
    for lab in labels:
        item = {x["class"]: x for x in lab["labels"]}.get(cls)
        key = os.path.basename(lab["file"])
        if item is None or item["status"] == "unsure" or key not in recs:
            continue
        r = redecide(recs[key][1], policy)
        pred = any(d["status"] == "ACCEPT" and pol.FAMILY_TO_CLASS.get(d["class_family"]) == cls for d in r["detections"])
        gt = item["status"] == "present"
        tp += pred and gt
        fp += pred and not gt
        fn += (not pred) and gt
    p = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * rc / (p + rc) if p + rc else 0.0
    return f, p, rc, tp + fn


def always_yes(labels, recs, cls):
    pos = neg = 0
    for lab in labels:
        item = {x["class"]: x for x in lab["labels"]}.get(cls)
        if item is None or item["status"] == "unsure" or os.path.basename(lab["file"]) not in recs:
            continue
        pos += item["status"] == "present"
        neg += item["status"] == "absent"
    p = pos / (pos + neg) if pos + neg else 0.0
    return round(2 * p / (p + 1), 4) if p else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    dev, test = split()
    recs = load_receipts(a.run)
    chosen, log = {"_other": {"context_downgrade": True}}, {}
    for cls in CLASSES:
        rows = []
        for sa, sb, ctx in itertools.product(GRID_A, GRID_B, GRID_CTX):
            if cls not in ("pole_obstruction", "parked_vehicle") and ctx is False:
                continue                       # context only acts on on-footpath families
            pp = {"_other": {"context_downgrade": True}, cls: {"single_A": sa, "single_B": sb, "context_downgrade": ctx}}
            f, p, r, npos = f1_for(dev, recs, cls, pp)
            simple = (sa is None) + (sb is None) + (ctx is True)
            rows.append((round(f, 4), round(p, 4), simple, sa, sb, ctx, r, npos))
        base = [x for x in rows if x[3] is None and x[4] is None and x[5] is True][0]
        best = max(rows, key=lambda x: (x[0], x[1], x[2]))
        npos = base[7]
        ay = always_yes(dev, recs, cls)
        if npos < MIN_POS:
            pick, why = base, f"only {npos} dev positives (< {MIN_POS}): kept the default rule"
        elif best[0] < base[0] + MARGIN:
            pick, why = base, f"best dev F1 {best[0]:.2f} does not beat the default {base[0]:.2f} by {MARGIN}"
        elif best[0] < ay + MARGIN:
            pick, why = base, (f"best dev F1 {best[0]:.2f} does not beat 'yes on every image' ({ay:.2f}) by {MARGIN}: "
                               "the rule carries no information")
        else:
            pick, why = best, f"dev F1 {base[0]:.2f} -> {best[0]:.2f} (always-yes {ay:.2f})"
        chosen[cls] = {"single_A": pick[3], "single_B": pick[4], "context_downgrade": pick[5]}
        log[cls] = {"dev_positives": npos, "dev_always_yes_f1": ay,
                    "test_always_yes_f1": always_yes(test, recs, cls), "default_dev": {"f1": base[0], "p": base[1], "r": base[6]},
                    "chosen_dev": {"f1": pick[0], "p": pick[1], "r": pick[6]}, "why": why,
                    "top5": [dict(zip(["f1", "p", "simple", "single_A", "single_B", "ctx", "r"], x[:7]))
                             for x in sorted(rows, key=lambda x: (-x[0], -x[1], -x[2]))[:5]]}
        print(f"{cls:28s} dev+={npos:2d} default F1 {base[0]:.2f} -> chosen {chosen[cls]} F1 {pick[0]:.2f}  ({why})")
    with open(os.path.join(CAL, "policy.json"), "w") as f:
        json.dump({"policy": chosen, "chosen_on": "C6 dev split (sha1(basename) even)", "source_run": a.run,
                   "log": log}, f, indent=1)
    # write re-decided receipts for the labelled images and score with the official eval
    for tag, policy in (("base", BASE_POLICY), ("cal", chosen)):
        od = os.path.join(os.path.dirname(a.run.rstrip("/")), os.path.basename(a.run.rstrip("/")) + f"-{tag}", "receipts")
        os.makedirs(od, exist_ok=True)
        for key, (f, r) in recs.items():
            with open(os.path.join(od, os.path.basename(f)), "w") as fh:
                json.dump(redecide(r, policy), fh, default=str)
        for split_name in ("dev", "test"):
            res = subprocess.run([sys.executable, "-I", EVAL, "--labels", os.path.join(CAL, f"c6-{split_name}.jsonl"),
                                  "--pred", os.path.dirname(od),
                                  "--out-md", os.path.join(CAL, f"eval-{tag}-{split_name}.md"),
                                  "--out-json", os.path.join(CAL, f"eval-{tag}-{split_name}.json")],
                                 capture_output=True, text=True)
            print(f"\n== {tag} policy, {split_name} split ==\n" + res.stdout.strip() + res.stderr.strip()[-400:])


if __name__ == "__main__":
    main()
