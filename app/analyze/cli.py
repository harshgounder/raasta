"""Batch-run /analyze on a folder (recursive). Each image may have a sidecar JSON with the same stem
(<name>.json) carrying source, source_url, licence, author, city, lat, lon, heading, captured_at,
gps_error_m. Writes <out>/receipts/<stem>.json, <out>/annotated/<stem>.jpg and <out>/summary.json.

  .venv/bin/python cli.py IN_DIR [IN_DIR ...] --out OUT_DIR [--limit N] [--no-judge]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback

EXT = {".jpg", ".jpeg", ".png", ".webp"}


def find_images(dirs):
    for d in dirs:
        if os.path.isfile(d):
            yield d
            continue
        for root, _, files in os.walk(d):
            for f in sorted(files):
                if os.path.splitext(f)[1].lower() in EXT:
                    yield os.path.join(root, f)


def sidecar(path):
    stem = os.path.splitext(path)[0]
    for c in (stem + ".json", path + ".json"):
        if os.path.exists(c):
            try:
                with open(c, encoding="utf-8") as fh:
                    return json.load(fh)
            except (OSError, json.JSONDecodeError):
                return {}
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-judge", action="store_true")
    args = ap.parse_args()
    if args.no_judge:
        os.environ["ANALYZE_JUDGE"] = "0"
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from raasta import pipeline
    from raasta.draw import annotate

    os.makedirs(os.path.join(args.out, "receipts"), exist_ok=True)
    os.makedirs(os.path.join(args.out, "annotated"), exist_ok=True)
    rows = []
    imgs = list(find_images(args.inputs))
    if args.limit:
        imgs = imgs[: args.limit]
    for n, p in enumerate(imgs, 1):
        sc = sidecar(p)
        form = {k: sc.get(k) for k in ("lat", "lon", "heading", "captured_at", "city", "gps_error_m", "source",
                                       "source_url", "licence", "author", "location_quality")}
        form["licence"] = form.get("licence") or sc.get("license")
        form["source"] = form.get("source") or sc.get("source_kind")
        if form.get("heading") is None:
            form["heading"] = sc.get("camera_heading", sc.get("compass_angle"))
        form["captured_at"] = form.get("captured_at") or sc.get("capture_date")
        form["filename"] = os.path.basename(p)
        stem = os.path.splitext(os.path.basename(p))[0]
        t = time.time()
        try:
            with open(p, "rb") as fh:
                data = fh.read()
            rec, img = pipeline.analyze(data, form)
            with open(os.path.join(args.out, "receipts", stem + ".json"), "w", encoding="utf-8") as fh:
                json.dump(rec, fh, indent=1, default=str)
            annotate(img, rec).save(os.path.join(args.out, "annotated", stem + ".jpg"), "JPEG", quality=85)
            acc = [d for d in rec["detections"] if d["status"] == "ACCEPT"]
            heights = [f"{d['class']} {d['height_cm']:.0f}+-{d['height_err_cm']:.0f}" for d in acc if d.get("height_cm") is not None]
            row = {"image": p, "ok": True, "seconds": round(time.time() - t, 2), "counts": rec["counts"],
                   "accept": [d["class"] for d in acc],
                   "abstain": [d["class"] for d in rec["detections"] if d["status"] == "ABSTAIN"],
                   "heights": heights,
                   "height_status": [f"{d['class']}:{d['height']['height_status']}" for d in rec["detections"] if d.get("height")],
                   "condition": rec["condition_bin"], "tier": rec["tier"]["tier"],
                   "placement": rec["placement"]["status"], "judge": rec["judge"], "timings": rec["timings"],
                   "city": form.get("city"), "source": form.get("source"), "licence": form.get("licence")}
        except Exception as e:  # noqa: BLE001
            row = {"image": p, "ok": False, "seconds": round(time.time() - t, 2),
                   "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-800:]}
        rows.append(row)
        print(f"[{n}/{len(imgs)}] {os.path.basename(p)} {row['seconds']}s "
              + (f"A{row['counts']['ACCEPT']} Ab{row['counts']['ABSTAIN']} R{row['counts']['REJECT']} {row['accept'][:6]} {row['heights']}"
                 if row["ok"] else row["error"]), flush=True)
        with open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
