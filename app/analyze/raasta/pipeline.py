"""The /analyze pipeline: intake -> detect A + B (+ judge) -> measure -> place -> receipt."""
from __future__ import annotations

import datetime as dt
import time

import numpy as np

from . import config, intake, judge, measure, models, place, policy, sun as sunmod

IST = intake.IST


def iou(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def family_nms(dets: list[dict], thr=0.5) -> list[dict]:
    dets = sorted(dets, key=lambda d: -d["score"])
    keep: list[dict] = []
    for d in dets:
        if all(not (k["family"] == d["family"] and iou(k["box"], d["box"]) > thr) for k in keep):
            keep.append(d)
    return keep


def _parse_time(v):
    if v in (None, ""):
        return None
    try:
        t = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=IST)
    except ValueError:
        return None


def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def agree(a_dets, b_dets):
    """One-to-one matching, highest combined score first. Returns list of (a, b|None, iou) and unmatched b."""
    pairs = []
    for i, a in enumerate(a_dets):
        for j, b in enumerate(b_dets):
            if config.same_family(a["family"], b["family"]):
                v = iou(a["box"], b["box"])
                if v >= config.IOU_AGREE:
                    pairs.append((a["score"] + b["score"] + v, i, j, v))
    pairs.sort(reverse=True)
    used_a, used_b, matched = set(), set(), []
    for _, i, j, v in pairs:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        matched.append((a_dets[i], b_dets[j], v))
    single_a = [a for i, a in enumerate(a_dets) if i not in used_a]
    single_b = [b for j, b in enumerate(b_dets) if j not in used_b]
    return matched, single_a, single_b


def footpath_context(seg, box, W, H) -> dict:
    """What ground is under the object: share of footpath vs carriageway pixels in a band at the box foot."""
    sh, sw = seg.shape
    fx, fy = sw / W, sh / H
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    ya, yb = int((y2 - 0.05 * bh) * fy), int(min(H, y2 + 0.06 * H) * fy)
    xa, xb = int(max(0, x1 - 0.1 * bw) * fx), int(min(W, x2 + 0.1 * bw) * fx)
    band = seg[max(0, ya):max(ya + 1, yb), max(0, xa):max(xa + 1, xb)]
    if band.size == 0:
        return {"verdict": "unknown", "why": "empty band"}
    foot = int(np.isin(band, list(config.SEG_FOOTPATH)).sum())
    road = int(np.isin(band, list(config.SEG_ROAD)).sum())
    ground = foot + road
    if ground < 0.12 * band.size:
        return {"verdict": "unknown", "ground_frac": round(ground / band.size, 2),
                "why": "too little visible ground at the object's foot"}
    f = foot / ground
    v = "footpath" if f >= 0.5 else ("carriageway" if f < 0.2 else "mixed")
    return {"verdict": v, "footpath_frac": round(f, 2), "ground_frac": round(ground / band.size, 2)}


def analyze(data: bytes, form: dict | None = None, today: dt.date | None = None) -> tuple[dict, object]:
    form = form or {}
    T: dict = {}
    t0 = time.time()
    notes: list[str] = []

    # ---- 1 intake
    t = time.time()
    img, exif, sha = intake.load_image(data)
    W, H = img.size
    image_id = "img-" + sha[:12]
    lat = _f(form.get("lat")) if form.get("lat") not in (None, "") else exif.get("lat")
    lon = _f(form.get("lon")) if form.get("lon") not in (None, "") else exif.get("lon")
    heading = _f(form.get("heading")) if form.get("heading") not in (None, "") else exif.get("heading")
    cap_raw = form.get("captured_at") if _parse_time(form.get("captured_at")) else exif.get("captured_at")
    cap = _parse_time(cap_raw)
    # a date without a clock time ("2025-10-31") gives the tier stamp but no sun position / hour check
    cap_has_time = cap is not None and len(str(cap_raw).strip()) > 10
    loc_src = "form" if form.get("lat") not in (None, "") else ("exif" if exif.get("lat") is not None else None)
    gps_err = _f(form.get("gps_error_m")) or exif.get("gps_error_m") or (8.0 if loc_src == "exif" else 15.0)
    if form.get("location_quality") == "approximate":
        gps_err = max(gps_err, _f(form.get("gps_error_m")) or 50.0)
    sun = sunmod.sun(lat, lon, cap) if (lat is not None and lon is not None and cap_has_time) else None
    cond = intake.condition(img, cap if cap_has_time else None, sun["elevation_deg"] if sun else None)
    today = today or dt.datetime.now(IST).date()
    if cap is None:
        tier = {"tier": "unknown", "why": "no capture time (EXIF or form)"}
    elif cap.astimezone(IST).date() == today:
        tier = {"tier": "observed today", "date": cap.date().isoformat()}
    else:
        tier = {"tier": "observed earlier", "date": cap.date().isoformat(),
                "age_days": (today - cap.astimezone(IST).date()).days}
    T["intake_s"] = round(time.time() - t, 3)

    # ---- 2 detect
    t = time.time()
    a_dets = family_nms(models.run_a(img))
    T["detect_A_s"] = round(time.time() - t, 3)
    t = time.time()
    try:
        b_dets = family_nms(models.run_b(img))
        b_ok = True
    except Exception as e:  # noqa: BLE001
        b_dets, b_ok = [], False
        notes.append(f"detector B failed ({type(e).__name__}: {e}); every detection is single-model")
    T["detect_B_s"] = round(time.time() - t, 3)

    matched, single_a, single_b = agree(a_dets, b_dets)
    dets: list[dict] = []
    for a, b, v in matched:
        top = a if a["score"] >= b["score"] else b
        box = [round((x + y) / 2, 1) for x, y in zip(a["box"], b["box"])]
        d = {"class": top["prompt"], "class_family": top["family"], "box": box,
             "scores": {"A": a["score"], "B": b["score"]}, "iou_AB": round(v, 3),
             "labels": {"A": a["prompt"], "B": b["prompt"]}, "status": "ACCEPT",
             "why": f"A and B agree (IoU {v:.2f}, same family)", "confidence": round(max(a["score"], b["score"]), 3)}
        if a["family"] != b["family"]:
            d["family_conflict"] = f"A says {a['family']}, B says {b['family']} (same group)"
        dets.append(d)
    for s, who, thr in [(x, "A", config.A_SINGLE_MIN) for x in single_a] + [(x, "B", config.B_SINGLE_MIN) for x in single_b]:
        st = "ABSTAIN" if s["score"] >= thr else "REJECT"
        dets.append({"class": s["prompt"], "class_family": s["family"], "box": s["box"],
                     "scores": {"A": s["score"] if who == "A" else None, "B": s["score"] if who == "B" else None},
                     "labels": {who: s["prompt"]}, "status": st, "confidence": round(s["score"] * 0.5, 3),
                     "why": ("only detector %s sees it: needs a human look" % who) if st == "ABSTAIN"
                     else f"only detector {who}, score {s['score']:.2f} < {thr}"})
    order = {"ACCEPT": 0, "ABSTAIN": 1, "REJECT": 2}
    dets.sort(key=lambda d: (order[d["status"]], -max(v or 0 for v in d["scores"].values())))

    # ---- footpath context (SegFormer-B0 sidewalk model, trained on Belgian streets: domain gap stated)
    t = time.time()
    try:
        seg = models.run_seg(img)
        for d in dets:
            c = footpath_context(seg, d["box"], W, H)
            d["footpath_context"] = c
        seg_ok = True
    except Exception as e:  # noqa: BLE001
        seg_ok = False
        notes.append(f"footpath-context model failed ({type(e).__name__}: {e})")
    T["context_s"] = round(time.time() - t, 3)
    for d in dets:                      # per-class decision policy (raasta/policy.py, CALIBRATION.md)
        policy.decide(d)
    dets.sort(key=lambda d: (order[d["status"]], -max(v or 0 for v in d["scores"].values())))

    # ---- judge (settles single-model detections). Hard cap: JUDGE_BUDGET_S for all calls of one
    # image, one provider attempt per call, circuit breaker after JUDGE_BREAKER_FAILS failures in a row.
    t = time.time()
    ok, jwhy = judge.available()
    judge_info = {"status": "skipped", "used": False, "why": jwhy, "calls": 0, "answered": 0,
                  "budget_s": config.JUDGE_BUDGET_S}
    if ok:
        calls = 0
        # PS core families first: those are the ones a person most needs settled
        queue = sorted([d for d in dets if d["status"] == "ABSTAIN"],
                       key=lambda d: (d["class_family"] not in config.PS_CORE_FAMILIES,
                                      -max(v or 0 for v in d["scores"].values())))
        for d in queue:
            left = config.JUDGE_BUDGET_S - (time.time() - t)
            if calls >= config.JUDGE_MAX_CALLS or left < 1.0:
                if left < 1.0:
                    judge_info["budget"] = f"stopped at the {config.JUDGE_BUDGET_S:.0f} s budget"
                break
            ans = judge.ask(img, d["box"], d["class"], budget_s=left)
            if ans.get("skipped"):
                judge_info["why"] = ans["error"]
                break
            calls += 1
            d["judge"] = ans
            if ans.get("answer") == "visible" and config.JUDGE_CAN_ACCEPT:
                d["status"], d["why"] = "ACCEPT", d["why"].replace("needs a human look", "") + "VLM judge says visible"
                d["accepted_by"] = "single detector + VLM judge (weaker than A+B)"
            elif ans.get("answer") == "visible":
                d["why"] += "; VLM judge says visible (support only: the judge also said 'visible' to stairs and an open drain on a shop roof in a sanity test)"
            elif ans.get("answer") == "not_visible":
                d["status"], d["why"] = "REJECT", "single detector; VLM judge says not visible"
            elif ans.get("answer") is None:
                judge_info["why"] = f"judge call failed: {ans.get('error')}"
                if not judge.available()[0]:
                    judge_info["why"] = judge.available()[1]
                    break
        answered = sum(1 for d in dets if (d.get("judge") or {}).get("answer"))
        judge_info.update(used=answered > 0, calls=calls, answered=answered,
                          status="used" if answered else "skipped")
        if not answered:
            judge_info["why"] = "judge skipped: " + judge_info["why"].removeprefix("judge skipped: ")
    T["judge_s"] = round(time.time() - t, 3)
    dets.sort(key=lambda d: (order[d["status"]], -max(v or 0 for v in d["scores"].values())))

    # ---- 3 measure
    t = time.time()
    arr = np.asarray(img)
    hz = measure.horizon(arr)
    cam = measure.focal_px(W, H, exif.get("focal_35mm"))
    need = [d for d in dets if d["status"] in ("ACCEPT", "ABSTAIN") and d["class_family"] in config.LEVEL_CHANGE]
    depth = None
    if need:
        td = time.time()
        try:
            depth = models.run_depth(img)
        except Exception as e:  # noqa: BLE001
            notes.append(f"depth model failed ({type(e).__name__}: {e})")
        T["depth_s"] = round(time.time() - td, 3)
    for d in need:
        rb, rnote = measure.riser(arr, d["box"], d["class"])
        routes = [measure.route_depth(depth, rb, cam, hz, d["class"]),
                  measure.route_geometry(rb, hz, H, d["class"]),
                  measure.route_shadow(arr, rb, hz, cam, sun, heading, cond["light"])]
        fz = measure.fuse(routes)
        d["height"] = {**fz, "routes": routes, "riser_box": [round(v, 1) for v in rb], "riser_note": rnote}
        if d["class"] == "stairs":
            d["height"]["measures"] = "total rise of the boxed flight, not one riser"
        if fz["height_status"] == "ACCEPT":
            d["height_cm"], d["height_err_cm"], d["routes_agreed"] = fz["height_cm"], fz["height_err_cm"], fz["routes_agreed"]
    T["measure_s"] = round(time.time() - t, 3)

    # ---- 4 place
    t = time.time()
    for n, d in enumerate(dets):
        d["id"] = f"{image_id}-d{n:02d}"
        if d["status"] != "REJECT":
            d["side_hint"] = place.side_hint(d["box"], hz.get("vp_x"), W)
            d["distance_m"] = place.distance_ahead(d["box"], hz, cam["f"])
    meta = {"lat": lat, "lon": lon, "heading": heading, "gps_error_m": gps_err, "city": form.get("city"),
            "image_id": image_id, "captured_at": cap.isoformat() if cap else None}
    placement = place.place(place.records(dets, meta), meta)
    T["place_s"] = round(time.time() - t, 3)
    T["total_s"] = round(time.time() - t0, 3)
    T["model_load_s"] = dict(models.LOAD_SECONDS)

    counts = {s: sum(1 for d in dets if d["status"] == s) for s in ("ACCEPT", "ABSTAIN", "REJECT")}
    if not b_ok:
        pass
    if counts["ACCEPT"] == 0:
        notes.append("no detection confirmed by both detectors; this image says nothing for certain")
    notes.append("never 'safe': a segment with no ACCEPT detection here stays 'unknown', not 'clear'")
    receipt = {
        "schema": "raasta-receipt-v1",
        "id": "rx-" + sha[:12],
        "image": {"id": image_id, "sha256": sha, "w": W, "h": H, "filename": form.get("filename")},
        "source": {k: form.get(k) for k in ("source", "source_url", "licence", "author", "city") if form.get(k)},
        "intake": {"exif": {k: v for k, v in exif.items()}, "lat": lat, "lon": lon, "location_source": loc_src,
                   "gps_error_m": gps_err, "heading": heading, "captured_at": cap.isoformat() if cap else None,
                   "sun": sun},
        "condition": cond,
        "condition_bin": cond["bin"],
        "tier": tier,
        "counts": counts,
        "detections": dets,
        "judge": judge_info,
        "measure": {"camera": {"f_px": round(cam["f"], 1), "f_source": cam["source"],
                               "height_m_assumed": list(config.CAM_HEIGHT_M)},
                    "horizon": {k: (round(v, 1) if isinstance(v, float) else v) for k, v in hz.items()},
                    "rule": "a height is printed only when >= 2 of 3 routes agree within their errors and "
                            f"err <= {config.HEIGHT_ACCEPT_MAX_ERR_CM} cm and <= {int(config.HEIGHT_ACCEPT_MAX_REL*100)} % of the value"},
        "placement": placement,
        "notes": notes,
        "timings": T,
        "models": models.versions(),
        "thresholds": {"A_conf": config.A_CONF, "B_conf": config.B_CONF, "iou_agree": config.IOU_AGREE,
                       "single_min": {"A": config.A_SINGLE_MIN, "B": config.B_SINGLE_MIN}},
        "created_at": dt.datetime.now(IST).isoformat(timespec="seconds"),
    }
    return receipt, img
