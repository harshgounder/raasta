"""Why things ABSTAIN, per source / condition, placement outcomes. Reads receipts of one run.
  python3 tools/breakdown.py out/online-v2
"""
import collections
import glob
import json
import os
import sys

run = sys.argv[1]
why = collections.Counter()
fam_status = collections.defaultdict(collections.Counter)
by_src = collections.defaultdict(collections.Counter)
by_cond = collections.defaultdict(collections.Counter)
place = collections.Counter()
place_det = collections.Counter()
ctx = collections.Counter()
judge = collections.Counter()
hs = collections.Counter()
for f in glob.glob(os.path.join(run, "receipts", "*.json")):
    r = json.load(open(f))
    src = os.path.basename(f).split("_")[0]
    by_src[src]["images"] += 1
    by_cond[r["condition"]["light"]]["images"] += 1
    p = r["placement"]
    place[p["status"] + (" via " + p["via"].split(" ")[0] if p.get("via") else "")] += 1
    for pl in (p.get("result") or {}).get("placements", []):
        place_det[pl.get("status")] += 1
    for d in r["detections"]:
        st = d["status"]
        fam_status[d["class_family"]][st] += 1
        by_src[src][st] += 1
        by_cond[r["condition"]["light"]][st] += 1
        if st == "ABSTAIN":
            w = d["why"]
            key = ("A+B agree but on carriageway" if "carriageway" in w else
                   "only detector A" if "only detector A" in w else
                   "only detector B" if "only detector B" in w else w[:50])
            why[key] += 1
        if d.get("footpath_context"):
            ctx[d["footpath_context"]["verdict"]] += 1
        if d.get("judge"):
            judge[d["judge"].get("answer") or "failed"] += 1
        if d.get("height"):
            hs[d["height"]["height_status"]] += 1
print("ABSTAIN reasons:", dict(why.most_common()))
print("footpath context verdicts (non-REJECT dets):", dict(ctx))
print("judge answers:", dict(judge))
print("height status:", dict(hs))
print("image placement:", dict(place))
print("per-detection placement:", dict(place_det))
print("\n| family | ACCEPT | ABSTAIN | REJECT |\n|---|---|---|---|")
for k, c in sorted(fam_status.items(), key=lambda x: -x[1]["ACCEPT"]):
    print(f"| {k} | {c['ACCEPT']} | {c['ABSTAIN']} | {c['REJECT']} |")
print("\n| source | images | ACCEPT | ABSTAIN | ACCEPT/img |\n|---|---|---|---|---|")
for k, c in sorted(by_src.items()):
    print(f"| {k} | {c['images']} | {c['ACCEPT']} | {c['ABSTAIN']} | {c['ACCEPT'] / max(1, c['images']):.2f} |")
print("\n| light | images | ACCEPT | ABSTAIN | ACCEPT/img |\n|---|---|---|---|---|")
for k, c in sorted(by_cond.items()):
    print(f"| {k} | {c['images']} | {c['ACCEPT']} | {c['ABSTAIN']} | {c['ACCEPT'] / max(1, c['images']):.2f} |")
