"""Step 4 place: hand detections to the routing service's attachment model.

Order: (1) HTTP POST {city, records} to ROUTE_URL (app/route hroute.api, /barriers);
(2) if the service is down, run app/route/hroute/attach.py in-process on the cached network
    app/route/cache/networks/<city>.pkl with commit=False (read-only);
(3) else return lat/lon + gps_error_m and mark placement pending.
Record schema = app/route/README.md "Barrier record"."""
from __future__ import annotations

import math
import os
import sys

import requests

from . import config

_NETS: dict = {}


def side_hint(box, vp_x: float | None, img_w: int) -> str | None:
    """Left/right footpath as seen in the image: which side of the vanishing point the box sits on."""
    cx = (box[0] + box[2]) / 2
    ref = vp_x if vp_x is not None else img_w / 2
    margin = 0.06 * img_w
    if cx < ref - margin:
        return "left"
    if cx > ref + margin:
        return "right"
    return None


def distance_ahead(box, hz: dict, f: float) -> float | None:
    vb = box[3]
    if vb - hz["v_h"] < 5:
        return None
    hc = sum(config.CAM_HEIGHT_M) / 2
    d = f * hc / (vb - hz["v_h"])
    return round(min(d, 40.0), 1)


def records(dets: list[dict], meta: dict) -> list[dict]:
    out = []
    for d in dets:
        if d["status"] not in ("ACCEPT", "ABSTAIN"):
            continue
        r = {"id": d["id"], "type": d["class_family"], "lat": meta["lat"], "lon": meta["lon"],
             "position": "camera", "gps_error_m": meta["gps_error_m"], "confidence": d["confidence"],
             "status": d["status"], "source": "photo", "label": d["class"], "photo": meta["image_id"],
             "observed_at": meta.get("captured_at")}
        if meta.get("heading") is not None:
            r["heading"] = meta["heading"]
        if d.get("side_hint"):
            r["side_hint"] = d["side_hint"]
        if d.get("distance_m") is not None:
            r["distance_m"] = d["distance_m"]
        if d.get("height_cm") is not None:
            r["height_cm"] = d["height_cm"]
        out.append({k: v for k, v in r.items() if v is not None})
    return out


def _net(city: str):
    if city in _NETS:
        return _NETS[city]
    path = os.path.join(config.ROUTE_DIR, "cache", "networks", f"{city}.pkl")
    if not os.path.exists(path):
        _NETS[city] = None
        return None
    if config.ROUTE_DIR not in sys.path:
        sys.path.insert(0, config.ROUTE_DIR)
    from hroute.network import FootNetwork
    _NETS[city] = FootNetwork.load(path)
    return _NETS[city]


def place(recs: list[dict], meta: dict) -> dict:
    base = {"lat": meta.get("lat"), "lon": meta.get("lon"), "gps_error_m": meta.get("gps_error_m"),
            "city": meta.get("city"), "records_sent": len(recs)}
    if meta.get("lat") is None or meta.get("lon") is None:
        return {**base, "status": "pending", "why": "no lat/lon (EXIF or form): placement needs a location"}
    if not recs:
        return {**base, "status": "nothing_to_place", "why": "no ACCEPT/ABSTAIN detections"}
    city = (meta.get("city") or "").strip().lower() or None
    errors = []
    if city:
        try:
            r = requests.post(config.ROUTE_URL, json={"city": city, "records": recs}, timeout=8)
            if r.status_code == 200:
                return {**base, "status": "placed", "via": f"HTTP {config.ROUTE_URL}", "result": r.json()}
            errors.append(f"route service HTTP {r.status_code}: {r.text[:160]}")
        except requests.RequestException as e:
            errors.append(f"route service not reachable ({type(e).__name__})")
        try:
            net = _net(city)
            if net is not None:
                if config.ROUTE_DIR not in sys.path:
                    sys.path.insert(0, config.ROUTE_DIR)
                from hroute.attach import attach
                res = []
                for rec in recs:
                    try:
                        res.append(attach(net, dict(rec), commit=False))
                    except ValueError as e:
                        res.append({"record_id": rec["id"], "status": "REJECT", "reason": str(e)})
                return {**base, "status": "placed", "via": f"in-process hroute.attach on cache/networks/{city}.pkl (commit=False)",
                        "notes": errors, "result": {"placements": res}}
            errors.append(f"no cached footpath network for city '{city}'")
        except Exception as e:  # noqa: BLE001
            errors.append(f"in-process attach failed: {type(e).__name__}: {e}")
    else:
        errors.append("no city given: the routing service needs one to pick a network")
    return {**base, "status": "pending", "why": "; ".join(errors), "records": recs}
