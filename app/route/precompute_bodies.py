"""Precompute routes for EVERY body leaf of the impact engine (74) for the site map.

Run from app/route:  .venv/bin/python precompute_bodies.py [city ...]
Reads the cached networks (cache/networks/<city>.pkl, evidence already attached by `hroute.cli precompute`)
and the trips in app/site-data/<city>/routes.json (what-if trips skipped: their records are removed after
that scenario). For each trip x leave time x condition x body leaf it calls
impact_adapter.route_with_engine(..., engine="impact") and writes one compact file per trip:
app/site-data/<city>/routes-bodies/<trip>.json. The 7-profile routes.json stays as the fallback.

Compact format (schema raasta-routes-bodies-v1):
  paths: list of unique [[lon,lat],...] (6 decimals); every route points into it by index
  combos: {"<leave>|<cond>": {"<body>": {"st": status, "s": R, "a": R|null, "l": R|null}}}
  R = {p: path index, m: metres, min: minutes, bc: barriers met, blk: blocking count, bfp: blocked for body,
       obs: barriers observed, ev: evidence_line, unk: unknown share %, mm: mapped m, em: estimated m,
       why: [up to 4 blocking reasons]}
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from hroute import impact as I  # noqa: E402
from hroute import impact_adapter as IA  # noqa: E402
from hroute.network import FootNetwork  # noqa: E402

SITE_DATA = os.path.abspath(os.path.join(HERE, "..", "site-data"))
CACHE = os.path.join(HERE, "cache", "networks")
# conditions the map exposes. hour comes from the leave time (the adapter sets it); "dark" means no working
# streetlight and is only computed for the evening leave time. All ASSUMPTIONS of the engine apply.
CONDITIONS = {
    "clear": {"label": "clear weather", "context": {"weather": "clear", "season": "winter"}, "times": ("08", "19")},
    "rain": {"label": "heavy rain (monsoon)", "context": {"weather": "heavy_rain", "season": "monsoon"}, "times": ("08", "19")},
    "dark": {"label": "no working streetlight", "context": {"weather": "clear", "season": "winter", "light": "night_dark"}, "times": ("19",)},
}


def slim(r, paths, index):
    if not r:
        return None
    coords = [[round(x, 6), round(y, 6)] for x, y in r["geometry"]["coordinates"]]
    key = json.dumps(coords, separators=(",", ":"))
    if key not in index:
        index[key] = len(paths)
        paths.append(coords)
    why = []
    for b in (r.get("blocking") or [])[:4]:
        why.append({"type": b.get("type"), "el": b.get("element"), "why": (b.get("why") or "")[:160]})
    return {"p": index[key], "m": round(r["length_m"], 1), "min": r.get("minutes"), "bc": r.get("barrier_count", 0),
            "blk": r.get("blocking_count", 0), "bfp": bool(r.get("blocked_for_profile")),
            "obs": r.get("barriers_observed"), "ev": r.get("evidence_line"), "unk": r.get("unknown_share_pct"),
            "mm": r.get("mapped_m"), "em": r.get("estimated_m"), "why": why}


def run_city(city):
    rp = os.path.join(SITE_DATA, city, "routes.json")
    pk = os.path.join(CACHE, f"{city}.pkl")
    if not (os.path.exists(rp) and os.path.exists(pk)):
        print(f"[{city}] skipped: routes.json or cached network missing")
        return 0
    routes = json.load(open(rp))
    net = FootNetwork.load(pk)
    bodies = [b["id"] for b in I.data()["body_list"]]
    out_dir = os.path.join(SITE_DATA, city, "routes-bodies")
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for sc in routes["scenarios"]:
        if sc.get("what_if"):
            continue
        s = (sc["start"]["lat"], sc["start"]["lon"])
        e = (sc["end"]["lat"], sc["end"]["lon"])
        paths, index, combos = [], {}, {}
        for lt in routes["leave_times"]:
            hh = lt[11:13]
            for cid, c in CONDITIONS.items():
                if hh not in c["times"]:
                    continue
                key = f"{lt}|{cid}"
                combos[key] = {}
                for bid in bodies:
                    r = IA.route_with_engine(net, s, e, bid, lt, engine="impact", context=c["context"])
                    combos[key][bid] = {"st": r.get("status"), "s": slim(r.get("shortest"), paths, index),
                                        "a": slim(r.get("accessible"), paths, index),
                                        "l": slim(r.get("least_blocked"), paths, index)}
                    n += 1
        doc = {"schema": "raasta-routes-bodies-v1", "city": city, "trip": sc["id"], "name": sc["name"],
               "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "engine": "impact (app/route/hroute/impact_adapter.py route_with_engine)",
               "about": "minutes = travel time only; every number from the impact engine is an ASSUMPTION unless "
                        "the element or body names a source (app/route/taxonomy/README.md)",
               "leave_times": routes["leave_times"],
               "conditions": {k: {"label": v["label"], "context": v["context"], "times": list(v["times"])} for k, v in CONDITIONS.items()},
               "bodies": bodies, "paths": paths, "combos": combos}
        with open(os.path.join(out_dir, f"{sc['id']}.json"), "w") as f:
            json.dump(doc, f, separators=(",", ":"))
        print(f"[{city}/{sc['id']}] {len(paths)} distinct paths, {sum(len(v) for v in combos.values())} routes")
    return n


if __name__ == "__main__":
    t0 = time.time()
    cities = sys.argv[1:] or [d for d in sorted(os.listdir(SITE_DATA)) if os.path.exists(os.path.join(CACHE, f"{d}.pkl"))]
    total = sum(run_city(c) for c in cities)
    print(f"{total} routes in {time.time() - t0:.0f} s")
