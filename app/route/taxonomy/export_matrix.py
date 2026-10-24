"""Export the ELEMENT x BODY impact matrix for the site, plus computed counts for README.

Run from app/route:  .venv/bin/python taxonomy/export_matrix.py
Writes app/site/public/content/impact-matrix.json and taxonomy/COUNTS.json (counts computed, not typed).
"""
from __future__ import annotations

import collections
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from hroute import impact as I  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "site", "public", "content", "impact-matrix.json"))
CONTEXTS = {
    "day_clear": {"hour": 11, "weather": "clear", "season": "winter",
                  "label": "11:00, clear, winter"},
    "night_dark": {"hour": 21, "light": "night_dark", "weather": "clear", "season": "winter",
                   "label": "21:00, no working streetlight"},
    "monsoon_rain_evening": {"hour": 18, "weather": "heavy_rain", "season": "monsoon",
                             "label": "18:00, heavy rain, monsoon"},
    "heatwave_noon": {"hour": 13, "weather": "heatwave", "temp_c": 45, "season": "summer",
                      "label": "13:00, 45 C heat wave, summer"},
    "winter_smog_morning": {"hour": 7, "weather": "smog", "aqi": 380, "season": "winter",
                            "label": "07:00, smog, AQI 380"},
}
LETTER = {"block": "B", "cost": "C", "warn": "W", "none": "N"}


def main():
    t0 = time.time()
    d = I.data()
    els = [e["id"] for e in d["element_list"]]
    bods = [b["id"] for b in d["body_list"]]
    out = {"schema": "raasta-impact-matrix-v1",
           "about": ("verdict letters B=block C=cost W=warn N=none; seconds = route time added; risk 0-1. "
                     "Same element, different body leaf -> different weight. Engine app/route/hroute/impact.py, "
                     "data app/route/taxonomy/*.json. Numbers are ASSUMPTIONS unless the element/body names a source."),
           "elements": els, "bodies": bods,
           "element_info": [{"id": e["id"], "name": e["name"], "category": e["category"],
                             "subcategory": e["subcategory"], "detect": e["detect_from_photo"],
                             "detector_class": e["detector_class"], "pattern": e["temporal"]["pattern"],
                             "source": e["attrs_source"]} for e in d["element_list"]],
           "body_info": [{"id": b["id"], "name": b["name"], "path": b["path"], "scorer": b["scorer"],
                          "hermes_id": b["hermes_id"], "rpwd": b["rpwd"], "aid": b["aid"]} for b in d["body_list"]],
           "element_tree": d["element_tree"], "body_tree": d["body_tree"], "contexts": {}}
    stats = {}
    for cname, ctx in CONTEXTS.items():
        c = {k: v for k, v in ctx.items() if k != "label"}
        V, S, Rk = [], [], []
        hist = collections.Counter()
        for eid in els:
            row_v, row_s, row_r = [], [], []
            for bid in bods:
                r = I.impact(eid, c, bid)
                row_v.append(LETTER[r["verdict"]])
                row_s.append(int(round(r["seconds"])))
                row_r.append(round(r["risk"], 2))
                hist[r["verdict"]] += 1
            V.append("".join(row_v))
            S.append(row_s)
            Rk.append(row_r)
        out["contexts"][cname] = {"label": ctx["label"], "context": c, "verdict": V, "seconds": S, "risk": Rk}
        spread = sum(1 for row in V if len(set(row)) >= 3)
        stats[cname] = {"cells": len(els) * len(bods), "verdicts": dict(hist),
                        "elements_with_3plus_distinct_verdicts_across_bodies": spread}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, separators=(",", ":"))

    # computed counts
    cats = collections.Counter(e["category"] for e in d["element_list"])
    subs = {(e["category"], e["subcategory"]) for e in d["element_list"]}
    sourced_el = sum(1 for e in d["element_list"] if e["attrs_source"] != "ASSUMPTION")
    scorers = collections.Counter(b["scorer"] for b in d["body_list"])
    top = collections.Counter(b["path"][0] for b in d["body_list"])
    sub_b = {tuple(b["path"]) for b in d["body_list"]}
    hermes_leaves = sum(1 for b in d["body_list"] if b.get("hermes_leaf"))
    needs = collections.Counter(n["flag"] for b in d["body_list"] for n in b["needs"])
    created = {r["creates"] for r in d["rules"] if r["creates"]}
    counts = {
        "elements": len(els), "element_categories": len(cats), "element_subcategories": len(subs),
        "elements_per_category": dict(cats), "elements_with_named_source": sourced_el,
        "elements_assumption_only": len(els) - sourced_el,
        "detect_from_photo": dict(collections.Counter(e["detect_from_photo"] for e in d["element_list"])),
        "elements_mapped_to_detector_class": sum(1 for e in d["element_list"] if e["detector_class"]),
        "bodies": len(bods), "body_top_categories": dict(top), "body_subgroups": len(sub_b),
        "bodies_per_scorer": dict(scorers), "bodies_that_are_hermes_leaves": hermes_leaves,
        "bodies_claude_additions": len(bods) - hermes_leaves,
        "body_need_flags": dict(needs),
        "interaction_rules": len(d["rules"]), "rules_creating_compounds": sum(1 for r in d["rules"] if r["creates"]),
        "distinct_compounds_created": len(created),
        "rules_with_named_source": sum(1 for r in d["rules"] if r["source"] != "ASSUMPTION"),
        "matrix": stats, "matrix_file_bytes": os.path.getsize(OUT), "seconds_to_compute": round(time.time() - t0, 1),
    }
    with open(os.path.join(HERE, "COUNTS.json"), "w") as f:
        json.dump(counts, f, indent=1)
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
