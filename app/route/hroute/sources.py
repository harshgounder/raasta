"""Evidence sources other than /analyze.

Project Sidewalk (Chandigarh deployment, label data CC0 1.0 per the Project Sidewalk API page, cite the CHI 2019 paper; street geometry ODbL, https://sidewalk-chandigarh.cs.washington.edu/v3/api).
Only label coordinates, types, tags, validations and image capture dates are used. The panoramas are
Google Street View, so no GSV imagery is fetched, shown or used for detection (DECISIONS D4).
"""
from __future__ import annotations

import json
import os

import requests

from .config import CACHE

PS_BASE = "https://sidewalk-chandigarh.cs.washington.edu"

_OBST_VEHICLE = {"parked car", "parked bike", "parked scooter/motorcycle", "parked auto"}
_OBST_VENDOR = {"street vendor", "cart"}


def fetch_project_sidewalk(bbox_swne, city="chandigarh", refresh=False) -> dict:
    s, w, n, e = bbox_swne
    path = os.path.join(CACHE, "ps", f"{city}_labels_{s}_{w}_{n}_{e}.geojson")
    if os.path.exists(path) and not refresh:
        with open(path) as f:
            return json.load(f)
    url = f"{PS_BASE}/v3/api/rawLabels?bbox={w},{s},{e},{n}&filetype=geojson"
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(r.text)
    return r.json()


def ps_label_to_record(feat) -> dict | None:
    p = feat["properties"]
    lt = p.get("label_type")
    tags = set(p.get("tags") or [])
    if p.get("correct") is False:
        return None  # validators marked it wrong
    t, perm = None, "permanent"
    if lt == "NoCurbRamp":
        t = "missing_kerb_ramp"
    elif lt == "Obstacle":
        if tags & _OBST_VEHICLE:
            t, perm = "parked_vehicle", "temporary"
        elif tags & _OBST_VENDOR:
            t, perm = "vendor", "temporary"
        else:
            t = "pole_obstruction"  # pole, sign, tree, vegetation, litter...: a fixed obstacle on the path
    elif lt == "SurfaceProblem":
        t = "open_drain" if "drainage" in tags else "broken_footpath"
    elif lt == "NoSidewalk":
        t = "missing_footpath"
    elif lt == "CurbRamp":
        t = "kerb_ramp_present"
    elif lt == "Crosswalk":
        t = "crossing_marked"
    elif lt == "Signal":
        t = "clear"
    if t is None:
        return None
    agree, dis = p.get("agree_count") or 0, p.get("disagree_count") or 0
    conf = 0.9 if p.get("correct") is True else min(0.9, max(0.55, 0.75 + 0.05 * (agree - dis)))
    lon, lat = feat["geometry"]["coordinates"][:2]
    cap = p.get("image_capture_date")
    return {
        "id": f"ps-{p['label_id']}", "type": t, "lat": lat, "lon": lon, "position": "barrier",
        "gps_error_m": 4.0, "confidence": round(conf, 2), "status": "ACCEPT", "permanence": perm,
        "observed_at": f"{cap}-15" if cap and len(cap) == 7 else cap, "source": "project_sidewalk",
        "label": f"Project Sidewalk {lt}" + (f" ({', '.join(sorted(tags))})" if tags else "")
                 + (f", severity {p['severity']}" if p.get("severity") else ""),
        "ref": f"{PS_BASE} label {p['label_id']} (CC0 1.0, Project Sidewalk CHI 2019); validations +{agree}/-{dis}",
    }


def project_sidewalk_records(bbox_swne, city="chandigarh") -> list[dict]:
    fc = fetch_project_sidewalk(bbox_swne, city)
    out = [ps_label_to_record(f) for f in fc.get("features", [])]
    return [r for r in out if r]
