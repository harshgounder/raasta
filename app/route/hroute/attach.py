"""Barrier attachment: which footpath segment does a detection belong to?

Record (from /analyze, Project Sidewalk, or manual):
  type, lat, lon, heading? (deg, clockwise from north, the camera's view direction),
  side_hint? (left|right: the barrier is on the left/right footpath of the road as seen in the image),
  position? (camera [default] | barrier: lat/lon is the camera GPS, or already the barrier spot),
  distance_m? (how far ahead of the camera the barrier is, camera mode only),
  gps_error_m, confidence, status ACCEPT/ABSTAIN, height_cm?, clear_width_cm?, slope_pct?,
  observed_at, permanence (permanent|temporary), half_life_h?

Model, for each candidate segment within search_radius_m of the record point:
  w = L_dist * L_bearing * L_side * prior(kind, type)
    L_dist    = exp(-d^2 / 2 sigma^2), sigma^2 = gps_error^2 + view_spread^2, d from the expected
                barrier point (camera point pushed forward along the heading)
    L_bearing = 0.5 + 0.5 |cos(segment bearing - heading)|   (photos look along footpaths)
    L_side    = side_match / side_mismatch when side_hint is given (road-relative side flipped if the
                camera looks against the road's drawing direction)
  p = w / (sum w + null_weight)   (null = "not on any mapped segment")
Attach to argmax when the detection status is ACCEPT and p >= accept_p, else ABSTAIN with candidates.
"""
from __future__ import annotations

import datetime as dt
import math
import uuid

from shapely.geometry import Point

from .config import BARRIER_TYPES, EXTRA_TYPES, cfg, clear_types

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def parse_time(v) -> dt.datetime | None:
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v if v.tzinfo else v.replace(tzinfo=IST)
    s = str(v).strip().replace("Z", "+00:00")
    for fmt in (None, "%Y-%m", "%Y"):
        try:
            t = dt.datetime.fromisoformat(s) if fmt is None else dt.datetime.strptime(s, fmt)
            return t if t.tzinfo else t.replace(tzinfo=IST)
        except ValueError:
            continue
    return None


def has_clock_time(v) -> bool:
    """True when a timestamp carries a time of day (date-only values such as Project Sidewalk's
    YYYY-MM image dates must not be read as midnight for hour-of-day curves)."""
    if v is None:
        return False
    if isinstance(v, dt.datetime):
        return True
    return "T" in str(v) or ":" in str(v)


def detach(net, record_id: str) -> int:
    """Remove one record's evidence from every segment (used by what-if scenarios)."""
    n = 0
    for s in net.segments.values():
        before = len(s["evidence"])
        s["evidence"] = [e for e in s["evidence"] if e.get("id") != record_id]
        n += before - len(s["evidence"])
    net.meta["placements"] = [p for p in net.meta.get("placements", []) if p["record_id"] != record_id]
    return n


def _compass(dx, dy) -> float:
    return math.degrees(math.atan2(dx, dy)) % 360


def _seg_bearing(geom, pt: Point) -> float:
    t = geom.project(pt)
    a = geom.interpolate(max(0.0, t - 1.5))
    b = geom.interpolate(min(geom.length, t + 1.5))
    if a.equals(b):
        a, b = Point(geom.coords[0]), Point(geom.coords[-1])
    return _compass(b.x - a.x, b.y - a.y)


def _adiff(a, b) -> float:
    return abs((a - b + 180) % 360 - 180)


def validate(rec: dict) -> dict:
    t = rec.get("type")
    ok = set(BARRIER_TYPES) | set(EXTRA_TYPES) | clear_types()
    if t not in ok:
        raise ValueError(f"unknown barrier type {t!r}; allowed: {sorted(ok)}")
    for k in ("lat", "lon"):
        if rec.get(k) is None:
            raise ValueError(f"missing {k}")
    out = dict(rec)
    out.setdefault("id", f"b-{uuid.uuid4().hex[:8]}")
    out.setdefault("status", "ACCEPT")
    out["status"] = str(out["status"]).upper()
    out.setdefault("confidence", 0.8)
    out.setdefault("gps_error_m", 8.0)
    out.setdefault("source", "photo")
    out.setdefault("position", "camera")
    if "permanence" not in out:
        out["permanence"] = "temporary" if t in ("parked_vehicle", "vendor", "waterlogging") else "permanent"
    if out["permanence"] == "temporary" and not out.get("half_life_h"):
        out["half_life_h"] = cfg()["temporal"]["default_half_life_h"].get(t, 24)
    if out.get("side_hint"):
        out["side_hint"] = str(out["side_hint"]).lower()
    return out


def candidates(net, rec: dict) -> tuple[list[dict], float]:
    ac = cfg()["attach"]
    x, y = net.to_xy(rec["lat"], rec["lon"])
    pt = Point(x, y)
    heading = rec.get("heading")
    camera = rec.get("position", "camera") == "camera"
    q = pt
    if heading is not None and camera:
        hr = math.radians(float(heading))
        fr = float(rec.get("distance_m") or ac["forward_range_m"])
        q = Point(x + math.sin(hr) * fr, y + math.cos(hr) * fr)
    gps = max(float(rec.get("gps_error_m") or 0), ac["min_gps_error_m"])
    spread = ac["view_spread_m"] if camera else 1.0
    sigma2 = gps ** 2 + spread ** 2
    radius = max(ac["search_radius_m"], 0.0)
    tree, ids = net.tree()
    priors = ac["kind_prior"].get(rec["type"], ac["kind_prior"]["default"])
    side_hint = rec.get("side_hint") if rec.get("side_hint") in ("left", "right") else None
    out = []
    for j in tree.query(pt.buffer(radius)):
        sid = ids[j]
        s = net.segments[sid]
        g = s["geom"]
        if g.distance(pt) > radius:
            continue
        d = g.distance(q)
        l_dist = math.exp(-d * d / (2 * sigma2))
        l_bear, l_side, why = 1.0, 1.0, []
        if heading is not None:
            delta = _adiff(_seg_bearing(g, q), float(heading)) % 180
            l_bear = 0.5 + 0.5 * abs(math.cos(math.radians(delta)))
        if side_hint and heading is not None:
            cam_side = None
            road = net.roads.get((s.get("parent_road") or {}).get("id"))
            if s.get("side") in ("L", "R") and road is not None:
                rbear = _seg_bearing(road["geom"], q)
                same_dir = _adiff(rbear, float(heading)) < 90
                lr = "left" if s["side"] == "L" else "right"
                cam_side = lr if same_dir else ("right" if lr == "left" else "left")
                why.append(f"segment is the {cam_side} footpath as seen along heading {float(heading):.0f}")
            elif camera:
                near = g.interpolate(g.project(pt))
                hr = math.radians(float(heading))
                lat_off = math.sin(hr) * (near.y - y) - math.cos(hr) * (near.x - x)
                if abs(lat_off) >= 1.0:
                    cam_side = "left" if lat_off > 0 else "right"
            if cam_side:
                l_side = ac["side_match"] if cam_side == side_hint else ac["side_mismatch"]
        prior = priors.get(s["kind"], 0.5)
        w = l_dist * l_bear * l_side * prior
        out.append({"segment_id": sid, "w": w, "distance_m": round(d, 1), "kind": s["kind"],
                    "at_m": round(g.project(q), 1),
                    "side": s.get("side"), "source": s["source"],
                    "road": (s.get("parent_road") or {}).get("name"),
                    "terms": {"dist": round(l_dist, 3), "bearing": round(l_bear, 3), "side": round(l_side, 3),
                              "prior": prior}, "why": why})
    total = sum(c["w"] for c in out) + ac["null_weight"]
    for c in out:
        c["p"] = round(c.pop("w") / total, 3)
    out.sort(key=lambda c: -c["p"])
    return out, round(ac["null_weight"] / total, 3)


def attach(net, rec: dict, commit: bool = True) -> dict:
    """Place one record. Returns the placement result; attaches evidence when ACCEPTed."""
    rec = validate(rec)
    ac = cfg()["attach"]
    if rec.get("segment_id") and rec["segment_id"] in net.segments:
        # caller already knows the segment (what-if records, manual fixes): no probability step
        cands, p_null = [{"segment_id": rec["segment_id"], "p": 1.0, "distance_m": None,
                          "kind": net.segments[rec["segment_id"]]["kind"], "at_m": rec.get("at_m"),
                          "why": ["segment_id given by caller"]}], 0.0
    else:
        cands, p_null = candidates(net, rec)
    best = cands[0] if cands else None
    result = {"record_id": rec["id"], "type": rec["type"], "detection_status": rec["status"],
              "candidates": cands[:5], "p_off_network": p_null, "accept_p": ac["accept_p"], "record": rec}
    if best is None:
        result.update(status="ABSTAIN", segment_id=None, p=0.0,
                      reason=f"no footpath segment within {ac['search_radius_m']:.0f} m")
    elif rec["status"] != "ACCEPT":
        result.update(status="ABSTAIN", segment_id=None, p=best["p"],
                      reason="detector abstained; placement kept as candidates only")
    elif best["p"] < ac["accept_p"]:
        result.update(status="ABSTAIN", segment_id=None, p=best["p"],
                      reason=f"best segment p={best['p']:.2f} < {ac['accept_p']}")
    else:
        result.update(status="ACCEPT", segment_id=best["segment_id"], p=best["p"],
                      reason=f"p={best['p']:.2f} >= {ac['accept_p']}")
        if commit:
            ev = {k: rec.get(k) for k in ("id", "type", "source", "status", "confidence", "observed_at",
                                          "permanence", "half_life_h", "height_cm", "clear_width_cm",
                                          "slope_pct", "lat", "lon", "heading", "side_hint", "gps_error_m",
                                          "label", "photo", "ref")}
            ev["p_attach"] = best["p"]
            ev["at_m"] = best.get("at_m")  # position along the segment, for the 25 m clear radius and 5 m dedupe
            seg = net.segments[best["segment_id"]]
            seg["evidence"] = [e for e in seg["evidence"] if e.get("id") != ev["id"]] + [ev]
    if commit:
        net.meta.setdefault("placements", [])
        net.meta["placements"] = [p for p in net.meta["placements"] if p["record_id"] != rec["id"]]
        net.meta["placements"].append(result)
    return result
