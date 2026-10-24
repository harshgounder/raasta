"""Check report-form.json against the other lanes' files: every element id exists in the taxonomy, every routing type is
one the routing service accepts, every body leaf exists in bodies.json with the same routing profile."""
import json, os, sys
APP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
form = json.load(open(os.path.join(APP, "site/public/content/report-form.json")))
els = {e["id"] for e in json.load(open(os.path.join(APP, "route/taxonomy/elements.json")))["elements"]}
bodies = {b["id"]: b for b in json.load(open(os.path.join(APP, "route/taxonomy/bodies.json")))["bodies"]}
ROUTE_TYPES = {"missing_kerb_ramp", "steps", "broken_footpath", "missing_footpath", "pole_obstruction", "parked_vehicle",
               "pothole", "open_drain", "vendor", "waterlogging", "steep_slope"}  # app/route/hroute/config.py
bad = []
n_types = n_q = 0
for c in form["categories"]:
    for t in c["types"]:
        n_types += 1
        if t["element"] and t["element"] not in els: bad.append(f"element {t['element']} ({t['id']}) not in elements.json")
        if t["route_type"] and t["route_type"] not in ROUTE_TYPES: bad.append(f"route_type {t['route_type']} ({t['id']})")
        if not t.get("hi"): bad.append(f"no Hindi for {t['id']}")
    ids = {t["id"] for t in c["types"]}
    for q in c.get("details", []):
        n_q += 1
        for f in q.get("for", []):
            if f not in ids: bad.append(f"detail {q['id']} names unknown type {f}")
        if not any(o["id"] == "unsure" for o in q["options"]): bad.append(f"detail {q['id']} has no 'not sure'")
n_leaves = 0
for g in form["bodies"]:
    for leaf in g["leaves"]:
        n_leaves += 1
        b = bodies.get(leaf["id"])
        if not b: bad.append(f"body {leaf['id']} not in bodies.json")
        elif b.get("legacy_profile") != leaf["profile"]: bad.append(f"body {leaf['id']} profile {leaf['profile']} != {b.get('legacy_profile')}")
print(f"{len(form['categories'])} categories, {n_types} types, {n_q} detail questions, {n_leaves} body leaves; problems: {len(bad)}")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
