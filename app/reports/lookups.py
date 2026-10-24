"""Read-only lookups for the reports service: the form tree, city areas, known barriers, the impact matrix, the
element taxonomy and the authority table. Every file here belongs to another lane; this module only reads them."""
from __future__ import annotations

import json
import os
import threading
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, ".."))
SITE_DATA = os.path.join(APP, "site-data")
FORM = os.path.join(APP, "site", "public", "content", "report-form.json")
IMPACT = os.path.join(APP, "site", "public", "content", "impact-matrix.json")
ELEMENTS = os.path.join(APP, "route", "taxonomy", "elements.json")
BODIES = os.path.join(APP, "route", "taxonomy", "bodies.json")
NETS = os.path.join(APP, "route", "cache", "networks")
AUTH = os.path.join(HERE, "authorities.json")
MAP_UPDATE = os.path.join(HERE, "data", "map-update")
ROUTE_URL = os.environ.get("ROUTE_URL", "http://127.0.0.1:8020").rstrip("/")
_lock = threading.Lock()


def _j(p, default=None):
    try:
        with open(p) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


@lru_cache(maxsize=1)
def form() -> dict:
    return _j(FORM, {"categories": [], "bodies": []})


def form_type(tid: str | None) -> dict | None:
    for c in form()["categories"]:
        for t in c["types"]:
            if t["id"] == tid:
                return {**t, "category": c["id"], "category_en": c["en"], "category_hi": c["hi"]}
    return None


def detail_hints(category: str | None, details: dict | None) -> tuple[dict, list[dict]]:
    """the branch answers as routing hints (height_cm, clear_width_cm) and as readable lines for the AI and reviewer."""
    hints, lines = {}, []
    cat = next((c for c in form()["categories"] if c["id"] == category), None)
    for q in (cat or {}).get("details", []):
        v = (details or {}).get(q["id"])
        o = next((o for o in q["options"] if o["id"] == v), None)
        if not o:
            continue
        lines.append({"q": q["en"], "a": o["en"]})
        for k in ("height_cm", "clear_width_cm"):
            if k in o:
                hints[k] = min(hints.get(k, o[k]), o[k]) if k == "clear_width_cm" else max(hints.get(k, 0), o[k])
    return hints, lines


def all_form_types() -> list[dict]:
    return [{"id": t["id"], "category": c["id"], "en": t["en"], "route_type": t["route_type"], "element": t["element"]}
            for c in form()["categories"] for t in c["types"]]


def profile_for_body(bid: str | None) -> str | None:
    for g in form()["bodies"]:
        for leaf in g["leaves"]:
            if leaf["id"] == bid:
                return leaf["profile"]
    b = body_info().get(bid or "")
    return b.get("legacy_profile") if b else None


@lru_cache(maxsize=1)
def body_info() -> dict:
    d = _j(BODIES, {"bodies": []})
    return {b["id"]: b for b in d.get("bodies", [])}


@lru_cache(maxsize=1)
def elements() -> dict:
    d = _j(ELEMENTS, {"elements": []})
    return {e["id"]: e for e in d.get("elements", [])}


def route_type_for_element(eid: str | None) -> str | None:
    e = elements().get(eid or "")
    rt = (e or {}).get("detector_class")
    return rt if rt and rt not in ("kerb_ramp_present", "crossing_marked", "clear") else None


@lru_cache(maxsize=1)
def _impact():
    return _j(IMPACT, None)


def impact_for(eid: str | None, context: str = "day_clear") -> dict | None:
    """which bodies this element blocks (B), costs (C) or warns (W), from the site's impact matrix."""
    m = _impact()
    if not m or not eid or eid not in m["elements"]:
        return None
    i = m["elements"].index(eid)
    ctx = m["contexts"].get(context) or next(iter(m["contexts"].values()))
    row = ctx["verdict"][i]
    names = {b["id"]: b["name"] for b in m.get("body_info", [])}
    out = {"B": [], "C": [], "W": []}
    for j, v in enumerate(row):
        if v in out:
            out[v].append(m["bodies"][j])
    return {"context": ctx.get("label"), "blocks": out["B"], "costs": out["C"], "warns": out["W"],
            "names": {b: names.get(b, b) for b in out["B"] + out["C"][:20]}, "of": len(m["bodies"])}


# ------------------------------------------------------------- cities

@lru_cache(maxsize=1)
def city_boxes() -> dict:
    """bbox of each city that has a routing network (cache/networks/<city>.pkl) and a site-data network file."""
    out = {}
    for f in sorted(os.listdir(NETS)) if os.path.isdir(NETS) else []:
        if not f.endswith(".pkl") or "--" in f:
            continue
        city = f[:-4]
        g = _j(os.path.join(SITE_DATA, city, "network.geojson"))
        if not g:
            continue
        xs, ys = [], []
        for ft in g.get("features", []):
            geom = ft.get("geometry") or {}
            if geom.get("type") == "LineString":
                for x, y in geom["coordinates"]:
                    xs.append(x)
                    ys.append(y)
        if xs:
            meta = _j(os.path.join(SITE_DATA, city, "meta.json"), {}) or {}
            out[city] = {"bbox": [min(ys), min(xs), max(ys), max(xs)], "name": meta.get("area", city)}
    return out


def city_names() -> dict:
    return {k: v["name"] for k, v in city_boxes().items()}


def city_for(lat: float, lon: float, pad_deg: float = 0.0015) -> str | None:
    best = None
    for c, v in city_boxes().items():
        s, w, n, e = v["bbox"]
        if s - pad_deg <= lat <= n + pad_deg and w - pad_deg <= lon <= e + pad_deg:
            area = (n - s) * (e - w)
            if best is None or area < best[0]:
                best = (area, c)
    return best[1] if best else None


_SEGS: dict = {}


def segment_coords(city: str, seg_id: str):
    """segment geometry, from the routing service's own geojson (authoritative), cached per base city."""
    base = city.split("--", 1)[-1]
    with _lock:
        if base not in _SEGS:
            g = None
            try:
                import httpx
                r = httpx.get(f"{ROUTE_URL}/network/{base}.geojson", timeout=60)
                if r.status_code == 200:
                    g = r.json()
            except Exception:  # noqa: BLE001
                g = None
            g = g or _j(os.path.join(SITE_DATA, base, "network.geojson"), {"features": []})
            _SEGS[base] = {(ft.get("properties") or {}).get("id"): ft["geometry"]["coordinates"]
                           for ft in g.get("features", []) if (ft.get("geometry") or {}).get("type") == "LineString"}
    return _SEGS[base].get(seg_id)


@lru_cache(maxsize=16)
def _known(city: str):
    d = _j(os.path.join(SITE_DATA, city, "barriers.json"), {}) or {}
    out = []
    for p in d.get("placements", []):
        r = p.get("record") or {}
        if r.get("lat") is None or p.get("type") in ("kerb_ramp_present", "crossing_marked", "clear"):
            continue
        out.append({"id": p.get("record_id"), "type": p.get("type"), "lat": r["lat"], "lon": r["lon"],
                    "status": p.get("status"), "observed_at": r.get("observed_at"), "source": r.get("source")})
    return out


def known_barriers_near(city: str | None, lat, lon, radius_m: float) -> list[dict]:
    if not city or lat is None:
        return []
    import math

    def haversine(a_lat, a_lon, b_lat, b_lon):
        p1, p2 = math.radians(a_lat), math.radians(b_lat)
        h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b_lon - a_lon) / 2) ** 2
        return 2 * 6371000.0 * math.asin(math.sqrt(h))
    out = []
    for k in _known(city):
        m = haversine(lat, lon, k["lat"], k["lon"])
        if m <= radius_m:
            out.append({**k, "distance_m": round(m, 1)})
    return sorted(out, key=lambda x: x["distance_m"])[:8]


# ------------------------------------------------------------- authorities

@lru_cache(maxsize=1)
def authorities() -> dict:
    return _j(AUTH, {"cities": {}, "default": {}})


def authority_for(city: str | None, category: str | None, type_id: str | None) -> dict:
    a = authorities()
    region = "jaipur" if (city or "").startswith("jaipur") else (city or "")
    table = a["cities"].get(region) or a["default"]
    for rule in table.get("rules", []):
        if type_id in rule.get("types", []) or category in rule.get("categories", []):
            return {**table["offices"][rule["office"]], "office": rule["office"], "region": region or "india"}
    office = table.get("fallback")
    return {**table["offices"][office], "office": office, "region": region or "india"}


def authority_options(city: str | None) -> list[dict]:
    a = authorities()
    region = "jaipur" if (city or "").startswith("jaipur") else (city or "")
    table = a["cities"].get(region) or a["default"]
    return [{"office": k, **v} for k, v in table["offices"].items()]


# ------------------------------------------------------------- next map update queue

def unqueue_from_map_update(rep: dict):
    p = os.path.join(MAP_UPDATE, f"{rep.get('city') or 'unmapped'}.input.json")
    if not os.path.exists(p):
        return
    with _lock:
        cur = _j(p, []) or []
        keep = [r for r in cur if not str(r.get("id", "")).startswith(f"report-{rep['id']}")]
        if len(keep) != len(cur):
            with open(p + ".tmp", "w") as f:
                json.dump(keep, f, ensure_ascii=False, indent=1)
            os.replace(p + ".tmp", p)


def queue_for_map_update(rep: dict, record: dict):
    """verified reports wait here in the routing lane's input format (BARRIERS-INPUT-SCHEMA.md) for the next map
    update. Nothing touches the public network until that update runs."""
    os.makedirs(MAP_UPDATE, exist_ok=True)
    city = rep.get("city") or "unmapped"
    p = os.path.join(MAP_UPDATE, f"{city}.input.json")
    with _lock:
        cur = _j(p, []) or []
        record = {**record, "status": "ACCEPT", "label": record.get("label", "").replace("unverified", "verified by a person")}
        cur = [r for r in cur if r.get("id") != record["id"]] + [record]
        with open(p + ".tmp", "w") as f:
            json.dump(cur, f, ensure_ascii=False, indent=1)
        os.replace(p + ".tmp", p)
