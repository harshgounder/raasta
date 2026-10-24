"""Export ACCEPT + ABSTAIN detections of geotagged receipts as barrier records for the routing
service: app/site-data/<city>/barriers.input.json (a JSON list, read by `hroute.cli precompute`),
and copy the annotated photo next to it (app/site-data/<city>/evidence/<stem>.jpg) so the site can
show the photo behind each barrier.

  python3 tools/export_barriers.py out/geo-v1 [--site ../site-data] [--merge]

Record = app/route/README.md "Barrier record" (type, lat, lon, heading, side_hint, position,
distance_m, gps_error_m, confidence, status, height_cm, observed_at, source, label, photo, ref)
plus provenance (image_path, licence, author, source_url, receipt_id, box, image_wh,
footpath_context, scores, why, height_err_cm). Existing records from other producers in the file
are kept (records with source_tool == "app/analyze" are replaced) when --merge is given.
"""
import argparse
import collections
import glob
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(HERE))

CITY_SLUG = {"bagru / nh48 (peri-urban highway)": "jaipur-outskirts", "muj-dehmi-kalan": "jaipur-outskirts",
             "india (city not stated)": "india-unstated"}


def slug(city: str | None) -> str:
    c = (city or "unknown").strip().lower()
    return CITY_SLUG.get(c) or re.sub(r"[^a-z0-9]+", "-", c).strip("-") or "unknown"


ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--site", default=os.path.join(os.path.dirname(HERE), "site-data"))
ap.add_argument("--merge", action="store_true")
a = ap.parse_args()

summary = {os.path.splitext(os.path.basename(r["image"]))[0]: r for r in json.load(open(os.path.join(a.run, "summary.json")))}
by_city = collections.defaultdict(list)
counts = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(os.path.join(a.run, "receipts", "*.json"))):
    r = json.load(open(f))
    stem = os.path.splitext(os.path.basename(f))[0]
    lat, lon = r["intake"]["lat"], r["intake"]["lon"]
    if lat is None or lon is None:
        continue
    city = slug(r["source"].get("city") or r["placement"].get("city"))
    img_path = summary.get(stem, {}).get("image")
    ann = os.path.join(a.run, "annotated", stem + ".jpg")
    ev_rel = f"evidence/{stem}.jpg"
    n_rec = 0
    for d in r["detections"]:
        if d["status"] not in ("ACCEPT", "ABSTAIN"):
            continue
        rec = {"id": d["id"], "type": d["class_family"], "lat": lat, "lon": lon, "position": "camera",
               "gps_error_m": r["intake"]["gps_error_m"], "confidence": d["confidence"], "status": d["status"],
               "source": ("mapillary" if stem.startswith("mly") else "video_frame" if stem.startswith("yt") else "photo"),
               "label": d["class"], "observed_at": r["intake"]["captured_at"],
               "photo": f"site-data/{city}/{ev_rel}",
               "ref": "; ".join(x for x in (r["source"].get("licence"), r["source"].get("author"),
                                            r["source"].get("source_url")) if x) or None,
               "receipt_ref": os.path.relpath(f, REPO),
               "source_tool": "app/analyze", "receipt_id": r["id"],
               "image_path": os.path.relpath(img_path, REPO) if img_path else None,
               "licence": r["source"].get("licence"), "author": r["source"].get("author"),
               "source_url": r["source"].get("source_url"), "box": d["box"], "image_wh": [r["image"]["w"], r["image"]["h"]],
               "scores": d["scores"], "why": d["why"],
               "footpath_context": (d.get("footpath_context") or {}).get("verdict")}
        if r["intake"].get("heading") is not None:
            rec["heading"] = r["intake"]["heading"]
        for k in ("side_hint", "distance_m", "height_cm", "height_err_cm"):
            if d.get(k) is not None:
                rec[k] = d[k]
        by_city[city].append({k: v for k, v in rec.items() if v is not None})
        counts[city][f"{d['status']} {d['class_family']}"] += 1
        n_rec += 1
    if n_rec and os.path.exists(ann):
        os.makedirs(os.path.join(a.site, city, "evidence"), exist_ok=True)
        shutil.copyfile(ann, os.path.join(a.site, city, ev_rel))
    counts[city]["images"] += 1

for city, recs in sorted(by_city.items()):
    path = os.path.join(a.site, city, "barriers.input.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    keep = []
    if a.merge and os.path.exists(path):
        try:
            keep = [x for x in json.load(open(path)) if x.get("source_tool") != "app/analyze"]
        except (OSError, json.JSONDecodeError):
            keep = []
    with open(path, "w") as fh:
        json.dump(keep + recs, fh, indent=1)
    print(f"{city}: {len(recs)} records ({len(keep)} kept from others) -> {os.path.relpath(path, REPO)}")
print()
for city, c in sorted(counts.items()):
    acc = {k[7:]: v for k, v in c.items() if k.startswith("ACCEPT ")}
    abs_ = {k[8:]: v for k, v in c.items() if k.startswith("ABSTAIN ")}
    print(f"| {city} | {c['images']} | {sum(acc.values())} | {sum(abs_.values())} | {acc} | {abs_} |")
