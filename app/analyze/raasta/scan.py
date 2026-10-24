"""LIVE SCAN: the /analyze stages run one by one, each stage emitting an event with its real output.

emit(stage, data) is called as each stage finishes. Stages, in order:
  queued, intake, detector_a, detector_b, agreement, footpath_mask, depth, measure, vlm, impact, placement, receipt
The receipt is the same raasta-receipt-v1 as /analyze plus a "scan" block (VLM scene + elements + impacts).
POST /analyze does not use this module; pipeline.analyze is untouched.
"""
from __future__ import annotations

import base64
import io
import time

import numpy as np
from PIL import Image

from . import config, impact, intake, measure, models, place, policy, vlm
from .pipeline import IST, _f, _parse_time, agree, family_nms, footpath_context
from . import sun as sunmod

import concurrent.futures as cf
import datetime as dt

_POOL = cf.ThreadPoolExecutor(max_workers=1)

LICENCES = {
    "detector_A": {"name": "YOLOE-11s-seg", "by": "Ultralytics / THU (YOLOE paper 2025)", "licence": "AGPL-3.0",
                   "kind": "open-vocabulary detection + segmentation, text prompts",
                   "good": "fast on a 4 GB GPU (~0.1-0.3 s), gives masks", "bad": "small model, weak on Indian clutter, invents boxes at low thresholds"},
    "detector_B": {"name": "OWLv2 base patch16 ensemble", "by": "Google", "licence": "Apache-2.0",
                   "kind": "open-vocabulary detection (CLIP-style image-text matching)",
                   "good": "different architecture and training data from A, so their agreement means something",
                   "bad": "slower (~1-2 s), boxes only, high recall on vague prompts like 'broken pavement'"},
    "footpath_mask": {"name": "SegFormer-B0 sidewalk (malra/segformer-b0-finetuned-segments-sidewalk-4)", "by": "NVIDIA SegFormer, fine-tune by malra on segments.ai sidewalk",
                      "licence": "base code: NVIDIA SegFormer licence; fine-tune card: no licence field (UNVERIFIED)",
                      "kind": "semantic segmentation: footpath vs road vs other",
                      "good": "tells if an object sits on the footpath or the carriageway", "bad": "trained on Belgian streets; indoor scenes have no footpath class"},
    "depth": {"name": "Depth Anything V2 Metric Outdoor Small", "by": "TikTok / HKU", "licence": "Apache-2.0 (Small checkpoint)",
              "kind": "monocular metric depth", "good": "one photo -> distances", "bad": "outdoor fine-tune: indoor metres are rough; scale depends on focal length guess"},
    "reasoner": {"name": "opencode-go/deepseek-v4.1-flash", "by": "DeepSeek, served by opencode Go", "licence": "hosted API (model licence not checked tonight: UNVERIFIED)",
                 "kind": "text only: turns detector decisions + the vision description + body table into the element list and a plain answer",
                 "good": "cheap, fast text model; never sees pixels so it cannot hallucinate from the photo", "bad": "can only be as right as its inputs; may over-generalise"},
    "vlm": {"name": "opencode-go/mimo-v2.6-flash", "by": "Xiaomi MiMo, served by opencode Go", "licence": "hosted API (model licence not checked tonight: UNVERIFIED)",
            "kind": "reads the whole photo + the numbered boxes, names scene, elements, measurements",
            "good": "understands rooms, hallways, steps, lighting, things no detector prompt covers",
            "bad": "can say 'visible' to things that are not there; its measurements are estimates, never ACCEPT on its own"},
}

SEG_COLOURS = {  # label id -> RGBA (ink style: footpath dark ink, road light grey hatch-like, curb red-ish ink)
    2: (17, 17, 17, 120), 7: (17, 17, 17, 170), 5: (17, 17, 17, 90),       # footpath, curb, driveway
    1: (120, 120, 120, 70), 3: (200, 41, 36, 60), 4: (120, 120, 120, 70),  # road, crosswalk, cycle lane
}


def _png_b64(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def mask_png(seg: np.ndarray) -> tuple[str, dict]:
    h, w = seg.shape
    rgba = np.zeros((h, w, 4), np.uint8)
    for k, c in SEG_COLOURS.items():
        rgba[seg == k] = c
    n = seg.size
    shares = {"footpath": round(float(np.isin(seg, list(config.SEG_FOOTPATH)).sum()) / n, 3),
              "road": round(float(np.isin(seg, list(config.SEG_ROAD)).sum()) / n, 3)}
    im = Image.fromarray(rgba, "RGBA")
    im.thumbnail((480, 480))
    return _png_b64(im), shares


def depth_png(depth: np.ndarray) -> tuple[str, dict]:
    d = depth.astype(np.float32)
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    g = np.clip((d - lo) / max(1e-3, hi - lo), 0, 1)
    g = (255 * (1 - g)).astype(np.uint8)        # near = light, far = dark (ink)
    im = Image.fromarray(g, "L")
    im.thumbnail((480, 480))
    return _png_b64(im), {"near_m": round(float(lo), 1), "far_m": round(float(hi), 1),
                          "median_m": round(float(np.median(d)), 1)}


def _t():
    return time.time()


def run(data: bytes, form: dict, emit) -> dict:
    form = form or {}
    T: dict = {}
    t0 = _t()
    notes: list[str] = []

    # ---- intake
    t = _t()
    img, exif, sha = intake.load_image(data)
    W, H = img.size
    image_id = "img-" + sha[:12]
    lat = _f(form.get("lat")) if form.get("lat") not in (None, "") else exif.get("lat")
    lon = _f(form.get("lon")) if form.get("lon") not in (None, "") else exif.get("lon")
    heading = _f(form.get("heading")) if form.get("heading") not in (None, "") else exif.get("heading")
    cap_raw = form.get("captured_at") if _parse_time(form.get("captured_at")) else exif.get("captured_at")
    cap = _parse_time(cap_raw)
    cap_has_time = cap is not None and len(str(cap_raw).strip()) > 10
    loc_src = "browser GPS" if form.get("lat") not in (None, "") else ("exif" if exif.get("lat") is not None else None)
    gps_err = _f(form.get("gps_error_m")) or exif.get("gps_error_m") or (8.0 if loc_src == "exif" else 15.0)
    sun = sunmod.sun(lat, lon, cap) if (lat is not None and lon is not None and cap_has_time) else None
    cond = intake.condition(img, cap if cap_has_time else None, sun["elevation_deg"] if sun else None)
    T["intake_s"] = round(_t() - t, 3)
    thumb = img.copy()
    thumb.thumbnail((1280, 1280))
    tb = io.BytesIO()
    thumb.save(tb, "JPEG", quality=80)
    emit("intake", {"seconds": T["intake_s"], "w": W, "h": H, "sha256": sha, "image_id": image_id,
                    "exif": {k: v for k, v in exif.items() if k in ("make", "model", "focal_35mm", "captured_at", "lat", "lon", "heading", "gps_error_m")},
                    "location": {"lat": lat, "lon": lon, "source": loc_src, "gps_error_m": gps_err},
                    "captured_at": cap.isoformat() if cap else None, "sun": sun, "condition": cond,
                    "image": "data:image/jpeg;base64," + base64.b64encode(tb.getvalue()).decode()})

    # ---- detector A
    t = _t()
    a_dets = family_nms(models.run_a(img))
    T["detect_A_s"] = round(_t() - t, 3)
    emit("detector_a", {"model": "YOLOE-11s-seg", "detail": f"open-vocabulary segmentation, {len(config.PROMPT_LIST)} text prompts",
                        "prompts": config.PROMPT_LIST, "threshold": config.A_CONF, "seconds": T["detect_A_s"],
                        "boxes": a_dets, "device": models.device()})

    # ---- detector B
    t = _t()
    try:
        b_dets = family_nms(models.run_b(img))
        b_ok = True
    except Exception as e:  # noqa: BLE001
        b_dets, b_ok = [], False
        notes.append(f"detector B failed ({type(e).__name__}: {e}); every detection is single-model")
    T["detect_B_s"] = round(_t() - t, 3)
    emit("detector_b", {"model": "OWLv2 base patch16 ensemble", "detail": f"open-vocabulary detection, same {len(config.PROMPT_LIST)} prompts",
                        "threshold": config.B_CONF, "seconds": T["detect_B_s"], "boxes": b_dets, "ok": b_ok})

    # ---- agreement
    t = _t()
    matched, single_a, single_b = agree(a_dets, b_dets)
    dets: list[dict] = []
    links = []
    for a, b, v in matched:
        top = a if a["score"] >= b["score"] else b
        box = [round((x + y) / 2, 1) for x, y in zip(a["box"], b["box"])]
        d = {"class": top["prompt"], "class_family": top["family"], "box": box,
             "scores": {"A": a["score"], "B": b["score"]}, "iou_AB": round(v, 3),
             "labels": {"A": a["prompt"], "B": b["prompt"]}, "status": "ACCEPT",
             "why": f"A and B agree (IoU {v:.2f}, same family)", "confidence": round(max(a["score"], b["score"]), 3),
             "boxes_AB": {"A": a["box"], "B": b["box"]}}
        dets.append(d)
        links.append({"A": a["box"], "B": b["box"], "iou": round(v, 3), "label": top["prompt"]})
    for s, who, thr in [(x, "A", config.A_SINGLE_MIN) for x in single_a] + [(x, "B", config.B_SINGLE_MIN) for x in single_b]:
        st = "ABSTAIN" if s["score"] >= thr else "REJECT"
        dets.append({"class": s["prompt"], "class_family": s["family"], "box": s["box"],
                     "scores": {"A": s["score"] if who == "A" else None, "B": s["score"] if who == "B" else None},
                     "labels": {who: s["prompt"]}, "status": st, "confidence": round(s["score"] * 0.5, 3), "only": who,
                     "why": ("only detector %s sees it: needs a second look" % who) if st == "ABSTAIN"
                     else f"only detector {who}, score {s['score']:.2f} < {thr}"})
    order = {"ACCEPT": 0, "ABSTAIN": 1, "REJECT": 2}
    dets.sort(key=lambda d: (order[d["status"]], -max(v or 0 for v in d["scores"].values())))
    T["agree_s"] = round(_t() - t, 3)
    emit("agreement", {"rule": f"same family (or same group) and IoU >= {config.IOU_AGREE} -> ACCEPT; one detector only and score >= 0.25 -> ABSTAIN; else REJECT",
                       "links": links, "decisions": [{k: d.get(k) for k in ("class", "status", "why", "box", "iou_AB", "scores", "only")} for d in dets],
                       "counts": {s: sum(1 for d in dets if d["status"] == s) for s in order}, "seconds": T["agree_s"]})

    # ---- VLM kick-off (runs over the network while the GPU does mask, depth and measure)
    shown = [d for d in dets if d["status"] != "REJECT"][:14]
    vboxes = []
    for i, d in enumerate(shown, 1):
        d["vlm_n"] = i
        vboxes.append({"n": i, "src": "A+B" if d["status"] == "ACCEPT" else (d.get("only") or "A"),
                       "label": d["class"], "box": d["box"]})
    emit("vlm_start", {"chain": vlm.status()["chain"], "boxes_sent": vboxes})

    def _v(_t0=_t()):
        r = vlm.describe(img, vboxes, budget_s=float(form.get("vlm_budget_s") or 12))
        r["wall_s"] = round(_t() - _t0, 3)
        return r
    vfut = _POOL.submit(_v)

    # ---- footpath mask
    t = _t()
    seg = None
    try:
        seg = models.run_seg(img)
        for d in dets:
            d["footpath_context"] = footpath_context(seg, d["box"], W, H)
        png, shares = mask_png(seg)
    except Exception as e:  # noqa: BLE001
        png, shares = None, None
        notes.append(f"footpath-context model failed ({type(e).__name__}: {e})")
    for d in dets:
        policy.decide(d)
    dets.sort(key=lambda d: (order[d["status"]], -max(v or 0 for v in d["scores"].values())))
    T["context_s"] = round(_t() - t, 3)
    emit("footpath_mask", {"model": "SegFormer-B0 sidewalk", "seconds": T["context_s"], "mask_png": png, "shares": shares,
                           "legend": {"dark ink": "footpath / kerb / driveway", "grey": "road / cycle lane", "red": "crosswalk"},
                           "policy": [{k: d.get(k) for k in ("class", "status", "why", "footpath_context")} for d in dets if d["status"] != "REJECT"]})

    # ---- depth (always, so the page can show it; outdoor-trained model)
    t = _t()
    depth = None
    try:
        depth = models.run_depth(img)
        dpng, dstats = depth_png(depth)
    except Exception as e:  # noqa: BLE001
        dpng, dstats = None, None
        notes.append(f"depth model failed ({type(e).__name__}: {e})")
    T["depth_s"] = round(_t() - t, 3)
    emit("depth", {"model": "Depth Anything V2 Metric Outdoor Small", "seconds": T["depth_s"], "depth_png": dpng, "stats": dstats,
                   "caveat": "metres assume the model's own camera; indoors the scale is rough"})

    # ---- measure (heights of level changes: 3 routes, printed only when 2 of 3 agree)
    t = _t()
    arr = np.asarray(img)
    hz = measure.horizon(arr)
    cam = measure.focal_px(W, H, exif.get("focal_35mm"))
    need = [d for d in dets if d["status"] in ("ACCEPT", "ABSTAIN") and d["class_family"] in config.LEVEL_CHANGE]
    for d in need:
        rb, rnote = measure.riser(arr, d["box"], d["class"])
        routes = [measure.route_depth(depth, rb, cam, hz, d["class"]),
                  measure.route_geometry(rb, hz, H, d["class"]),
                  measure.route_shadow(arr, rb, hz, cam, sun, heading, cond["light"])]
        fz = measure.fuse(routes)
        d["height"] = {**fz, "routes": routes, "riser_box": [round(v, 1) for v in rb], "riser_note": rnote}
        if fz["height_status"] == "ACCEPT":
            d["height_cm"], d["height_err_cm"] = fz["height_cm"], fz["height_err_cm"]
    T["measure_s"] = round(_t() - t, 3)
    emit("measure", {"seconds": T["measure_s"], "horizon": {k: (round(v, 1) if isinstance(v, float) else v) for k, v in hz.items()},
                     "camera": {"f_px": round(cam["f"], 1), "f_source": cam["source"]},
                     "heights": [{"class": d["class"], "box": d["box"], **{k: d["height"].get(k) for k in ("height_status", "height_cm", "height_err_cm", "routes_agreed")},
                                  "routes": [{k: r.get(k) for k in ("route", "ok", "height_cm", "err_cm", "why")} for r in d["height"]["routes"]]} for d in need],
                     "rule": "a height is printed only when >= 2 of 3 routes (depth, vanishing-point geometry, shadow) agree"})

    # ---- VLM: started in a thread after agreement, joined here
    v = vfut.result()
    for b in v.get("boxes") or []:
        for d in shown:
            if d.get("vlm_n") == b["n"]:
                d["vlm"] = b
                # support only: the VLM never upgrades ABSTAIN to ACCEPT (see config.JUDGE_CAN_ACCEPT)
                if b["verdict"] == "deny" and d["status"] == "ABSTAIN":
                    d["status"], d["why"] = "REJECT", d["why"] + "; VLM denies it"
                elif b["verdict"] == "confirm" and d["status"] == "ABSTAIN":
                    d["why"] += "; VLM supports it (still ABSTAIN: one detector + VLM is not two detectors)"
    T["vlm_s"] = v.get("wall_s")
    emit("vlm", {**v, "seconds": T["vlm_s"]})

    # ---- per-body impact
    t = _t()
    imp = impact.for_scan(dets, v, cond)
    T["impact_s"] = round(_t() - t, 3)
    emit("impact", {**imp, "seconds": T["impact_s"]})

    # ---- text reasoner (opencode-go deepseek-v4.1-flash): element list, per-body text, plain answer
    t = _t()
    emit("reasoner_start", {"model": "opencode-go/" + vlm.TEXT_MODEL})
    rs = vlm.reason(dets, v, imp, budget_s=float(form.get("reason_budget_s") or 8))
    T["reasoner_s"] = round(_t() - t, 3)
    emit("reasoner", {**rs, "seconds": T["reasoner_s"]})

    # ---- placement
    t = _t()
    for n, d in enumerate(dets):
        d["id"] = f"{image_id}-d{n:02d}"
        if d["status"] != "REJECT":
            d["side_hint"] = place.side_hint(d["box"], hz.get("vp_x"), W)
            d["distance_m"] = place.distance_ahead(d["box"], hz, cam["f"])
    meta = {"lat": lat, "lon": lon, "heading": heading, "gps_error_m": gps_err, "city": form.get("city"),
            "image_id": image_id, "captured_at": cap.isoformat() if cap else None}
    placement = place.place(place.records(dets, meta), meta) if lat is not None else {"status": "skipped", "why": "no GPS (browser location off and no EXIF GPS)"}
    T["place_s"] = round(_t() - t, 3)
    emit("placement", {"seconds": T["place_s"], "placement": placement})

    T["total_s"] = round(_t() - t0, 3)
    counts = {s: sum(1 for d in dets if d["status"] == s) for s in ("ACCEPT", "ABSTAIN", "REJECT")}
    if counts["ACCEPT"] == 0:
        notes.append("no detection confirmed by both detectors; nothing here is certain")
    notes.append("never 'safe': no ACCEPT here means 'unknown', not 'clear'")
    receipt = {
        "schema": "raasta-receipt-v1", "id": "rx-" + sha[:12],
        "image": {"id": image_id, "sha256": sha, "w": W, "h": H, "filename": form.get("filename")},
        "intake": {"lat": lat, "lon": lon, "location_source": loc_src, "gps_error_m": gps_err, "heading": heading,
                   "captured_at": cap.isoformat() if cap else None, "sun": sun},
        "condition": cond, "condition_bin": cond["bin"], "counts": counts, "detections": dets,
        "scan": {"vlm": v, "impact": imp, "reasoner": rs}, "placement": placement, "notes": notes, "timings": T,
        "models": models.versions(), "licences": LICENCES,
        "thresholds": {"A_conf": config.A_CONF, "B_conf": config.B_CONF, "iou_agree": config.IOU_AGREE},
        "created_at": dt.datetime.now(IST).isoformat(timespec="seconds"),
    }
    emit("receipt", receipt)
    return receipt
