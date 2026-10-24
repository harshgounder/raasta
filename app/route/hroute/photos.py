"""Photo behind a barrier record: link each placement to its annotated /analyze image and source credit.

Used by `cli.precompute` only for areas that set `photo_evidence` (the Jaipur photo areas). Kept apart
from attach.py and costs.py on purpose: it never changes a placement's status, segment or p, it only adds

  placement["evidence_photo"] = {url, annotated, original_url, receipt_ref, receipt_id, credit, licence,
                                 author, source_url, box, crop, image_wh, observed_at}
  placement["record"]["photo"] = {url, crop, credit, license}      (the shape app/site/src/demo/receipt.js reads)
  placement["record"]["photo_path"] = the old string path, kept

and copies the annotated image (long side <= max_px) to app/site/public/evidence/<slug>/<stem>.jpg.
"""
from __future__ import annotations

import os

from .config import ROOT

REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))  # hypnexis-main
SITE_PUBLIC = os.path.join(REPO, "app", "site", "public")


def photo_stem(rec: dict) -> str | None:
    """File stem shared by the receipt, the annotated image and the evidence copy."""
    for k in ("receipt_ref", "photo", "image_path"):
        v = rec.get(k)
        if v:
            return os.path.splitext(os.path.basename(str(v)))[0]
    return None


def annotated_source(rec: dict, repo: str = REPO) -> str | None:
    """app/analyze/out/<run>/annotated/<stem>.jpg next to the receipt, if it exists."""
    ref = rec.get("receipt_ref")
    stem = photo_stem(rec)
    if not ref or not stem:
        return None
    run_dir = os.path.dirname(os.path.dirname(os.path.join(repo, ref)))
    p = os.path.join(run_dir, "annotated", stem + ".jpg")
    return p if os.path.exists(p) else None


def crop_of(rec: dict, pad: float = 0.15) -> list[float] | None:
    """Detection box [x1,y1,x2,y2] in image pixels -> [x, y, w, h] in 0..1, padded, clamped."""
    box, wh = rec.get("box"), rec.get("image_wh")
    if not box or not wh or len(box) != 4 or not wh[0] or not wh[1]:
        return None
    W, H = float(wh[0]), float(wh[1])
    x1, y1, x2, y2 = (float(v) for v in box)
    px, py = (x2 - x1) * pad, (y2 - y1) * pad
    x1, y1 = max(0.0, x1 - px), max(0.0, y1 - py)
    x2, y2 = min(W, x2 + px), min(H, y2 + py)
    if x2 <= x1 or y2 <= y1:
        return None
    return [round(x1 / W, 4), round(y1 / H, 4), round((x2 - x1) / W, 4), round((y2 - y1) / H, 4)]


def credit_of(rec: dict) -> str:
    parts = [rec.get("author"), rec.get("licence"), rec.get("source_url")]
    parts = [str(p) for p in parts if p]
    return "; ".join(parts) if parts else str(rec.get("ref") or "credit unknown")


def copy_resized(src: str, dst: str, max_px: int = 1280) -> tuple[int, int]:
    """Copy an image with its long side capped at max_px (never upscaled). Returns the written size."""
    from PIL import Image

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        s = min(1.0, max_px / float(max(w, h)))
        if s < 1.0:
            im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
        im.save(dst, "JPEG", quality=85, optimize=True)
        return im.size


def link_placements(placements: list[dict], slug: str, public_root: str = SITE_PUBLIC, repo: str = REPO,
                    max_px: int = 1280) -> dict:
    """Add the photo link to every placement whose record names a receipt; copy each image once.

    Returns {stem: {"url", "size", "from"}} for the photos written (or None when no source image exists)."""
    written: dict[str, dict | None] = {}
    for pl in placements:
        rec = pl.get("record") or {}
        stem = photo_stem(rec)
        if not stem:
            continue
        if stem not in written:
            src = annotated_source(rec, repo)
            kind = "annotated"
            if src is None and rec.get("image_path") and os.path.exists(os.path.join(repo, rec["image_path"])):
                src, kind = os.path.join(repo, rec["image_path"]), "original"
            if src is None:
                written[stem] = None
            else:
                rel = f"evidence/{slug}/{stem}.jpg"
                size = copy_resized(src, os.path.join(public_root, rel), max_px)
                written[stem] = {"url": "/" + rel, "size": list(size), "from": os.path.relpath(src, repo),
                                 "kind": kind}
        w = written[stem]
        crop = crop_of(rec)
        ev = {"url": w["url"] if w else None, "annotated": bool(w and w["kind"] == "annotated"),
              "copied_from": w["from"] if w else None, "original_url": rec.get("source_url"),
              "receipt_ref": rec.get("receipt_ref"), "receipt_id": rec.get("receipt_id"),
              "credit": credit_of(rec), "licence": rec.get("licence"), "author": rec.get("author"),
              "source_url": rec.get("source_url"), "box": rec.get("box"), "crop": crop,
              "image_wh": rec.get("image_wh"), "observed_at": rec.get("observed_at")}
        pl["evidence_photo"] = ev
        if w:
            if isinstance(rec.get("photo"), str):
                rec["photo_path"] = rec["photo"]
            rec["photo"] = {"url": w["url"], "crop": crop or [0, 0, 1, 1], "credit": ev["credit"],
                            "license": rec.get("licence")}
    return written


def reason_counts(placements: list[dict]) -> dict:
    """Why records did not attach, grouped (computed from the placements, never typed by hand)."""
    out: dict[str, int] = {}
    for pl in placements:
        st = pl.get("status")
        if st == "ACCEPT":
            k = "placed (p >= accept_p)"
        elif st == "REJECT":
            k = "REJECT: " + str(pl.get("reason", "")).split(":")[0]
        else:
            r = str(pl.get("reason", ""))
            rec = pl.get("record") or {}
            if r.startswith("no footpath segment"):
                k = "ABSTAIN: photo outside this network (no segment within search radius)"
            elif r.startswith("detector abstained"):
                k = "ABSTAIN: detector abstained (needs a human look), never placed"
            elif rec.get("heading") is None:
                k = "ABSTAIN: detector ACCEPT, p < accept_p, no camera heading"
            else:
                k = "ABSTAIN: detector ACCEPT, p < accept_p, heading present"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))
