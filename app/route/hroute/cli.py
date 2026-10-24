"""Precompute demo JSON for the site.

  .venv/bin/python -m hroute.cli precompute            # all demo areas
  .venv/bin/python -m hroute.cli precompute jaipur     # one area
  .venv/bin/python -m hroute.cli build --city x --bbox S W N E
  .venv/bin/python -m hroute.cli route --city jaipur --start LAT LON --end LAT LON --profile manual_wheelchair

Writes app/site-data/<city>/{network.geojson, routes.json, barriers.json, meta.json}.
Extra barrier records for an area (from /analyze or labelling) can be dropped in
app/site-data/<city>/barriers.input.json (a JSON list of records) and are attached before routing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

from . import attach as A
from . import photos
from . import routing as R
from .config import CACHE, PROFILES, SITE_DATA, cfg
from .costs import TIERS, tier
from .network import FootNetwork, build_network
from .sources import project_sidewalk_records

# coordinates checked against Nominatim (OSM geocoder) on 2026-10-24
AREAS = {
    "jaipur": {
        "name": "Jaipur walled city (Hawa Mahal, Badi Chaupar, Johari Bazar)",
        "bbox": (26.913, 75.815, 26.928, 75.833),
        "terrain": "dense historic bazaar grid, arcaded footpaths, west India (Rajasthan)",
        "scenarios": [
            {"id": "hawa-johari", "name": "Hawa Mahal to Johari Bazar",
             "start": {"lat": 26.92393, "lon": 75.82687, "label": "Hawa Mahal (Nominatim 26.923932, 75.826865)"},
             "end": {"lat": 26.91585, "lon": 75.82484, "label": "Johari Bazar (Nominatim 26.915852, 75.824841)"}},
            {"id": "palace-hawa", "name": "City Palace to Hawa Mahal",
             "start": {"lat": 26.92621, "lon": 75.82383, "label": "City Palace (Nominatim 26.926210, 75.823835)"},
             "end": {"lat": 26.92393, "lon": 75.82687, "label": "Hawa Mahal"}},
            {"id": "palace-quarter", "name": "City Palace gate to Tripolia side (OSM-mapped staircases)",
             "start": {"lat": 26.924666, "lon": 75.818491, "label": "City Palace gate (hermes-b prototype scenario)"},
             "end": {"lat": 26.925527, "lon": 75.817887, "label": "Tripolia side"}},
        ],
    },
    # Jaipur photo areas (JAIPUR-PHOTOS.md): built where the 130 /analyze records in
    # site-data/jaipur/barriers.input.json actually sit; the walled-city "jaipur" key above is unchanged.
    # Road names are the OSM names of the nearest road in the built network, not geocoder lookups.
    "jaipur-photos": {
        "name": "Jaipur photo area west: Tirpoliya Bazar photo to Sawai Jai Singh Circle (OSM name)",
        "bbox": (26.921, 75.788, 26.931, 75.811),
        "terrain": "arterial roads and a roundabout west of the walled city, west India (Rajasthan)",
        "records_from": "jaipur",
        "photo_evidence": "jaipur-photos",
        "what_if": False,
        "scenarios": [
            {"id": "tirpoliya-sjs-circle", "name": "Tirpoliya Bazar photo spot to the Sawai Jai Singh Circle photo spot",
             "start": {"lat": 26.925775, "lon": 75.807055,
                       "label": "GPS of Commons photo 'Jaipur Tirpoliya Bazar' (Gopal lal soni, CC BY-SA 4.0)"},
             "end": {"lat": 26.92596, "lon": 75.79229,
                     "label": "GPS of Mapillary photos 288940249442301 and 451767995919838 (Sawai Jai Singh Circle)"}},
            {"id": "sjs-circle-south-north", "name": "Across Sawai Jai Singh Circle, south to north past the photo spot",
             "start": {"lat": 26.9233, "lon": 75.7923, "label": "about 300 m south of the photo spot"},
             "end": {"lat": 26.9287, "lon": 75.7921, "label": "Bihari Marg (OSM), about 300 m north"}},
        ],
    },
    "jaipur-photos-south": {
        "name": "Jaipur photo area south: primary road at 26.908 N 75.819 E (two Mapillary photos)",
        "bbox": (26.903, 75.812, 26.914, 75.825),
        "terrain": "primary road with service links, south of the walled city, west India (Rajasthan)",
        "records_from": "jaipur",
        "photo_evidence": "jaipur-photos",
        "what_if": False,
        "scenarios": [
            {"id": "south-primary", "name": "Along the primary road past the Mapillary photo spot",
             "start": {"lat": 26.9101, "lon": 75.8191, "label": "about 200 m north of the photo spot"},
             "end": {"lat": 26.9050, "lon": 75.8178, "label": "about 380 m south of the photo spot"}},
        ],
    },
    "chandigarh": {
        "name": "Chandigarh Sector 17 and Sector 10 (Project Sidewalk deployment)",
        "bbox": (30.733, 76.775, 30.755, 76.800),
        "terrain": "planned grid city with V-road hierarchy and dual carriageways, north India",
        "evidence": "project_sidewalk",
        "scenarios": [
            {"id": "s17-museum", "name": "Sector 17 to Government Museum (Sector 10)",
             "start": {"lat": 30.74007, "lon": 76.78259, "label": "Sector 17 (Nominatim centroid 30.740065, 76.782589)"},
             "end": {"lat": 30.74895, "lon": 76.78744, "label": "Government Museum and Art Gallery (Nominatim 30.748945, 76.787437)"}},
            {"id": "s10-labelled", "name": "Sector 10 streets with the densest Project Sidewalk labels",
             "start": {"lat": 30.7492, "lon": 76.7836, "label": "Sector 10, south-west of the labelled streets"},
             "end": {"lat": 30.7522, "lon": 76.7874, "label": "Sector 10, north-east of the labelled streets"}},
        ],
    },
    "varanasi": {
        "name": "Varanasi old city and ghats (Godowlia, Dashashwamedh, Kashi Vishwanath)",
        "bbox": (25.300, 83.000, 25.316, 83.016),
        "terrain": "riverside ghats with long stone steps and narrow galis, east India (Gangetic plain)",
        "scenarios": [
            {"id": "godowlia-dashashwamedh", "name": "Godowlia to Dashashwamedh Ghat",
             "start": {"lat": 25.30924, "lon": 83.00684, "label": "Godowlia (Nominatim 25.309241, 83.006841)"},
             "end": {"lat": 25.30625, "lon": 83.01015, "label": "Dashashwamedh Ghat (Nominatim 25.306248, 83.010153)"}},
            {"id": "vishwanath-manikarnika", "name": "Kashi Vishwanath Temple to Manikarnika Ghat",
             "start": {"lat": 25.31082, "lon": 83.01067, "label": "Kashi Vishwanath Temple (Nominatim 25.310822, 83.010668)"},
             "end": {"lat": 25.31077, "lon": 83.01402, "label": "Manikarnika Ghat (Nominatim 25.310768, 83.014021)"}},
        ],
    },
}
LEAVE_TIMES = ["2026-10-25T08:00:00+05:30", "2026-10-25T19:00:00+05:30"]


def _net(city, rebuild=False):
    p = os.path.join(CACHE, "networks", f"{city}.pkl")
    if os.path.exists(p) and not rebuild:
        return FootNetwork.load(p)
    net = build_network(city, bbox=AREAS[city]["bbox"])
    net.save(p)
    return net


def _slim_route(r):
    if r is None:
        return None
    r = dict(r)
    r["barriers_truncated"] = len(r["barriers"]) > 40
    r["barriers"] = r["barriers"][:40]  # barrier_count / blocking_count keep the full numbers
    return r


def _attach_all(net, records):
    placements = []
    for r in records:
        try:
            placements.append(A.attach(net, r))
        except Exception as ex:  # one bad record never aborts a precompute
            placements.append({"record_id": r.get("id"), "type": r.get("type"), "status": "REJECT",
                               "reason": f"{type(ex).__name__}: {ex}", "record": r, "segment_id": None})
    return placements


def _route_set(net, s, e):
    by_time = {}
    for lt in LEAVE_TIMES:
        by_time[lt] = {}
        for p in PROFILES:
            r = R.route(net, s, e, p, lt)
            for k in ("shortest", "accessible", "least_blocked"):
                if r.get(k):
                    r[k] = _slim_route(r[k])
            by_time[lt][p] = r
    return by_time


WHAT_IF_NOTE = ("WHAT-IF record placed by the routing lane to show how profile and leave time change the route. "
                "Not an observation.")


def _what_if(net, base):
    """Place three labelled what-if records on routes of `base`, route, then remove them.

    vendor (60 cm clear, seen 19:00 the evening before) on the pram's own 19:00 route: blocks a pram
    at 19:00 (p_present >= 0.5) but is only a soft cost at 08:00, so leave time changes the pram route.
    6 cm kerb on a crossing of the wheelchair route and a 7.5 % ramp on the elderly walker route:
    profile changes the route.
    """
    s = (base["start"]["lat"], base["start"]["lon"])
    e = (base["end"]["lat"], base["end"]["lon"])

    def ids_of(profile, lt):
        r = R.route(net, s, e, profile, lt)
        x = r.get("accessible") or r.get("least_blocked") or r.get("shortest") or {}
        return x.get("segment_ids", [])

    def longest(ids, kind, skip=()):
        c = [i for i in ids[1:-1] if net.segments[i]["kind"] == kind and i not in skip]
        return max(c, key=lambda i: net.segments[i]["length_m"]) if c else None

    def at(sid):
        g = net.segments[sid]["geom"]
        m = g.interpolate(0.5, normalized=True)
        lon, lat = net.to_lonlat(m.x, m.y)
        return {"segment_id": sid, "at_m": round(g.length / 2, 1), "lat": lat, "lon": lon}

    recs = []

    def vendor(sid):
        return {"id": f"whatif-{base['id']}-vendor", "type": "vendor", **at(sid), "position": "barrier",
                "gps_error_m": 1.5, "confidence": 0.95, "status": "ACCEPT", "permanence": "temporary",
                "half_life_h": 6, "clear_width_cm": 60, "observed_at": "2026-10-24T19:00:00+05:30",
                "source": "what_if",
                "label": "vendor cart leaving 60 cm clear, seen 19:00 the evening before. " + WHAT_IF_NOTE}

    wc = ids_of("manual_wheelchair", LEAVE_TIMES[0])
    k = next((i for i in wc if net.segments[i]["kind"] == "crossing"), None)
    if k:
        recs.append({"id": f"whatif-{base['id']}-kerb", "type": "missing_kerb_ramp", "height_cm": 6, **at(k),
                     "position": "barrier", "gps_error_m": 1.5, "confidence": 0.9, "status": "ACCEPT",
                     "permanence": "permanent", "observed_at": "2026-10-24", "source": "what_if",
                     "label": "6 cm kerb, no ramp. " + WHAT_IF_NOTE})
    sl = longest(ids_of("walker_elderly", LEAVE_TIMES[0]), "sidewalk")
    if sl:
        recs.append({"id": f"whatif-{base['id']}-slope", "type": "steep_slope", "slope_pct": 7.5, **at(sl),
                     "position": "barrier", "gps_error_m": 1.5, "confidence": 0.9, "status": "ACCEPT",
                     "permanence": "permanent", "observed_at": "2026-10-24", "source": "what_if",
                     "label": "ramp at 7.5% (1:13): within MoHUA 1:12, steeper than IRC:103-2022 1:15. "
                              + WHAT_IF_NOTE})
    if not recs:
        return None
    placements = _attach_all(net, recs)  # kerb + slope first, so the vendor search sees them
    # try the pram's own sidewalk segments until one shows a leave-time difference (searched, then disclosed)
    pram_ids = ids_of("pram", LEAVE_TIMES[1])
    walkable = ("sidewalk", "footway", "shared_street")
    cands = sorted((i for i in pram_ids[1:-1] if net.segments[i]["kind"] in walkable),
                   key=lambda i: (net.segments[i]["kind"] != "sidewalk", -net.segments[i]["length_m"]))[:40]
    v = cands[0] if cands else None
    for c in cands:
        A.attach(net, vendor(c))
        differs = any(ids_of(p, LEAVE_TIMES[0]) != ids_of(p, LEAVE_TIMES[1])
                      for p in ("pram", "manual_wheelchair"))
        A.detach(net, f"whatif-{base['id']}-vendor")
        if differs:
            v = c
            break
    if v:
        recs.append(vendor(v))
        placements += _attach_all(net, [recs[-1]])
    routes = _route_set(net, s, e)
    for rec in recs:
        A.detach(net, rec["id"])
    return {"id": f"{base['id']}-whatif", "name": f"{base['name']} (WHAT-IF: vendor, 6 cm kerb, steep ramp)",
            "what_if": True, "note": WHAT_IF_NOTE, "start": base["start"], "end": base["end"],
            "what_if_records": recs, "what_if_placements": placements, "routes": routes}


def _photo_extras(area, placements, records_path) -> dict:
    """Photo areas only: link every placement to its photo (hroute/photos.py) and count why records
    did not attach. Never changes a placement's status, segment or p."""
    if not area.get("photo_evidence"):
        return {}
    written = photos.link_placements(placements, area["photo_evidence"])
    return {"records_file": os.path.relpath(records_path, os.path.dirname(SITE_DATA)),
            "accept_p": cfg()["attach"]["accept_p"], "why": photos.reason_counts(placements),
            "photos": {k: v for k, v in sorted(written.items())}}


def precompute(city: str, rebuild=True) -> dict:
    area = AREAS[city]
    net = _net(city, rebuild=rebuild)
    records = []
    if area.get("evidence") == "project_sidewalk":
        records += project_sidewalk_records(area["bbox"], city)
    extra = os.path.join(SITE_DATA, area.get("records_from", city), "barriers.input.json")
    if os.path.exists(extra):
        try:
            with open(extra) as f:
                records += json.load(f)
        except Exception as ex:
            print(f"[precompute] {extra} unreadable: {ex}")
    placements = _attach_all(net, records)
    net.invalidate()
    net.meta["stats"] = net.stats()
    net.save(os.path.join(CACHE, "networks", f"{city}.pkl"))

    out_dir = os.path.join(SITE_DATA, city)
    os.makedirs(out_dir, exist_ok=True)
    gj = net.to_geojson(tier_fn=tier)
    with open(os.path.join(out_dir, "network.geojson"), "w") as f:
        json.dump(gj, f, separators=(",", ":"))
    counts = {k: sum(p["status"] == k for p in placements) for k in ("ACCEPT", "ABSTAIN", "REJECT")}
    extra_keys = _photo_extras(area, placements, extra)
    with open(os.path.join(out_dir, "barriers.json"), "w") as f:
        json.dump({"city": city, "count": len(placements), "accepted": counts["ACCEPT"],
                   "abstained": counts["ABSTAIN"], "rejected": counts["REJECT"], **extra_keys,
                   "placements": placements},
                  f, separators=(",", ":"))

    scen_out = []
    for sc in area["scenarios"]:
        s = (sc["start"]["lat"], sc["start"]["lon"])
        e = (sc["end"]["lat"], sc["end"]["lon"])
        scen_out.append({**sc, "what_if": False, "routes": _route_set(net, s, e)})
    wi = _what_if(net, area["scenarios"][area.get("what_if_base", 0)]) if area.get("what_if", True) else None
    if wi:
        scen_out.append(wi)
    routes = {"city": city, "area": area["name"], "terrain": area["terrain"], "bbox_swne": area["bbox"],
              "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "leave_times": LEAVE_TIMES, "profiles": PROFILES, "scenarios": scen_out}
    with open(os.path.join(out_dir, "routes.json"), "w") as f:
        json.dump(routes, f, separators=(",", ":"))
    tiers = {t: 0 for t in TIERS}
    for sg in net.segments.values():
        tiers[tier(sg)] += 1
    meta = {"city": city, "area": area["name"], "terrain": area["terrain"], "bbox_swne": area["bbox"],
            "network": {k: v for k, v in net.meta.items() if k != "placements"}, "segment_tiers": tiers,
            "evidence_records": len(records), "placements": counts,
            "sources": ["OpenStreetMap contributors, ODbL (api.openstreetmap.org map tiles); the generated footpath network is derived from OSM, so the map credits OSM",
                        "Project Sidewalk Chandigarh: labelled by Project Sidewalk volunteers, label data CC0 1.0 (cite the "
                        "Project Sidewalk CHI 2019 paper); coordinates and tags only, no GSV imagery"
                        if area.get("evidence") == "project_sidewalk" else None],
            "assumptions": "app/route/hroute/assumptions.json"}
    if area.get("photo_evidence"):
        meta["sources"].append("Photos: Wikimedia Commons, Mapillary and other CC BY-SA 4.0 sources; per-photo author, "
                               "licence and URL in barriers.json placements[].evidence_photo")
    meta["sources"] = [x for x in meta["sources"] if x]
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    return meta


def table(city: str) -> str:
    d = json.load(open(os.path.join(SITE_DATA, city, "routes.json")))
    lines = []
    for sc in d["scenarios"]:
        lines.append(f"### {city} / {sc['id']}")
        lines.append("| profile | 08:00 status | 08:00 m | 08:00 min | 19:00 status | 19:00 m | 19:00 min |")
        lines.append("|---|---|---|---|---|---|---|")
        lts = d["leave_times"]
        for p in d["profiles"]:
            row = [p]
            for lt in lts:
                r = sc["routes"][lt][p]
                a = r.get("accessible") or r.get("least_blocked") or {}
                row += [r["status"], f"{a.get('length_m', 0):.0f}", f"{a.get('minutes', 0):.1f}"]
            lines.append("| " + " | ".join(row) + " |")
        sh = sc["routes"][lts[0]]["default_walker"].get("shortest") or {}
        lines.append(f"(shortest {sh.get('length_m', 0):.0f} m)")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="hroute")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("precompute")
    p1.add_argument("cities", nargs="*", default=list(AREAS))
    p1.add_argument("--no-rebuild", action="store_true")
    p2 = sub.add_parser("build")
    p2.add_argument("--city", required=True)
    p2.add_argument("--bbox", nargs=4, type=float, metavar=("S", "W", "N", "E"))
    p2.add_argument("--place")
    p4 = sub.add_parser("table")
    p4.add_argument("cities", nargs="*", default=list(AREAS))
    p3 = sub.add_parser("route")
    p3.add_argument("--city", required=True)
    p3.add_argument("--start", nargs=2, type=float, required=True)
    p3.add_argument("--end", nargs=2, type=float, required=True)
    p3.add_argument("--profile", default="manual_wheelchair")
    p3.add_argument("--leave", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "precompute":
        for c in a.cities:
            m = precompute(c, rebuild=not a.no_rebuild)
            print(c, json.dumps({"tiers": m["segment_tiers"], "records": m["evidence_records"],
                                 "placements": m["placements"],
                                 "stats": m["network"].get("stats")}))
    elif a.cmd == "table":
        for c in a.cities:
            print(table(c))
    elif a.cmd == "build":
        net = build_network(a.city, bbox=tuple(a.bbox) if a.bbox else None, place=a.place)
        net.save(os.path.join(CACHE, "networks", f"{a.city}.pkl"))
        print(json.dumps(net.stats(), indent=1))
    elif a.cmd == "route":
        net = FootNetwork.load(os.path.join(CACHE, "networks", f"{a.city}.pkl"))
        r = R.route(net, tuple(a.start), tuple(a.end), a.profile, a.leave)
        for k in ("shortest", "accessible", "least_blocked"):
            if r.get(k):
                r[k].pop("geometry", None)
        print(json.dumps(r, indent=1, default=str)[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
