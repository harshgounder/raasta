#!/usr/bin/env python3
"""Build data/labels/c6-v1.jsonl from the labelling drafts (fraction boxes) + image sidecars.

Draft lines (one per image) carry boxes as fractions of the image; this script converts them to
pixels using the real image size, joins city / licence / source from the sidecar JSON next to
each image in data/online/, validates every line, and writes the final jsonl.

usage: python3 -I data/labels/build_c6_labels.py DRAFT1.jsonl [DRAFT2.jsonl ...] [--out PATH]
Stdlib only (image size read from the JPEG/PNG header, no PIL needed).
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ONLINE = os.path.join(ROOT, "data", "online")
CLASSES = ["missing_kerb_ramp", "steps", "broken_or_missing_footpath", "pole_obstruction", "parked_vehicle"]
STATES = {"present", "absent", "unsure"}


def image_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h
        if head[:2] != b"\xff\xd8":
            raise ValueError(f"not a JPEG/PNG: {path}")
        f.seek(2)
        while True:
            b = f.read(1)
            while b and b != b"\xff":
                b = f.read(1)
            while b == b"\xff":
                b = f.read(1)
            if not b:
                raise ValueError(f"no SOF marker: {path}")
            marker = b[0]
            seg_len = struct.unpack(">H", f.read(2))[0]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                f.read(1)
                h, w = struct.unpack(">HH", f.read(4))
                return w, h
            f.seek(seg_len - 2, 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("drafts", nargs="+")
    ap.add_argument("--out", default=os.path.join(HERE, "c6-v1.jsonl"))
    args = ap.parse_args()
    rows = []
    for dp in args.drafts:
        with open(dp, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        sys.exit(f"{dp}:{n}: bad JSON {e}")
    seen = set()
    out = []
    errors = []
    for d in sorted(rows, key=lambda r: r["idx"]):
        rel = d["file"]
        if rel in seen:
            errors.append(f"duplicate {rel}")
            continue
        seen.add(rel)
        img = os.path.join(ONLINE, rel)
        side = os.path.splitext(img)[0] + ".json"
        if not os.path.exists(img):
            errors.append(f"missing image {rel}")
            continue
        w, h = image_size(img)
        sc = json.load(open(side, encoding="utf-8")) if os.path.exists(side) else {}
        labels = []
        for c in CLASSES:
            v = (d.get("labels") or {}).get(c)
            if not v or v.get("state") not in STATES:
                errors.append(f"{rel}: class {c} missing or bad state")
                continue
            item = {"class": c, "status": v["state"], "boxes": []}
            if v["state"] == "present":
                bxs = v.get("boxes") or []
                if not bxs:
                    errors.append(f"{rel}: {c} present without a box")
                for b in bxs:
                    if len(b) != 4 or not all(0.0 <= x <= 1.0 for x in b) or b[2] <= b[0] or b[3] <= b[1]:
                        errors.append(f"{rel}: {c} bad fraction box {b}")
                        continue
                    item["boxes"].append([round(b[0] * w), round(b[1] * h), round(b[2] * w), round(b[3] * h)])
                if v.get("kind"):
                    item["kind"] = v["kind"]
            if v["state"] == "unsure":
                item["why"] = v.get("why", "")
                if not item["why"]:
                    errors.append(f"{rel}: {c} unsure without why")
            labels.append(item)
        cond = d.get("cond") or {}
        tags = [cond.get("light"), cond.get("weather")] + list(cond.get("setting") or []) + ([("view_" + cond["view"])] if cond.get("view") else [])
        out.append({
            "file": rel,
            "image_w": w, "image_h": h,
            "city": sc.get("city"),
            "condition": cond,
            "condition_tags": [t for t in tags if t],
            "licence": sc.get("licence"),
            "source_url": sc.get("source_url"),
            "author": sc.get("author"),
            "labels": labels,
            "extras": d.get("extras", []),
            "difficulty": d.get("difficulty"),
            "note": d.get("note", ""),
            "label_method": "team label made with AI assistance (Claude looked at each full image; boxes drawn as fractions then converted to pixels); needs one human pass",
            "label_version": "c6-v1",
            "labelled_on": "2026-10-24",
        })
    if errors:
        print("ERRORS:")
        for e in errors:
            print(" ", e)
        sys.exit(1)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} lines to {args.out}")


if __name__ == "__main__":
    main()
