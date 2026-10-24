"""End to end: 3 reports (photo, no photo, duplicate) through the running services, with timings.
Run: app/reports/.venv/bin/python app/reports/tests/e2e.py  (reports :8790, route :8020, analyze :8010 must be up)
Writes app/reports/data/e2e-<time>.json and prints a table. Never prints the AI key or the review token."""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime

import httpx

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
API = os.environ.get("REPORTS_URL", "http://127.0.0.1:8790")
ROUTE = os.environ.get("ROUTE_URL", "http://127.0.0.1:8020")
PHOTO = os.path.join(REPO, "data", "online", "commons", "cm_273_Jaipur_Tirpoliya_Bazar_jpg.jpg")  # 26.925775, 75.807055, CC BY-SA 4.0
stamp = datetime.now().strftime("%H%M%S")


def post(fields: dict, photo: str | None = None) -> tuple[dict, float]:
    t0 = time.time()
    files = {"photo": (os.path.basename(photo), open(photo, "rb"), "image/jpeg")} if photo else None
    r = httpx.post(f"{API}/reports", data=fields, files=files, timeout=60)
    r.raise_for_status()
    return r.json(), time.time() - t0


def wait(rid: str, limit: float = 60) -> tuple[dict, float]:
    t0 = time.time()
    while time.time() - t0 < limit:
        d = httpx.get(f"{API}/reports/{rid}", timeout=10).json()
        st = {s["id"]: s["state"] for s in d["steps"]}
        if st["ai_first_look"] != "active" and st["personal_route"] != "active":
            return d, time.time() - t0
        time.sleep(0.25)
    raise TimeoutError(rid)


def public_route(city: str, frm, to, profile="manual_wheelchair") -> dict:
    r = httpx.post(f"{ROUTE}/route", json={"city": city, "start": {"lat": frm[0], "lon": frm[1]},
                                          "end": {"lat": to[0], "lon": to[1]}, "profile": profile}, timeout=30).json()
    best = r.get("accessible") or r.get("least_blocked") or {}
    return {"length_m": best.get("length_m"), "minutes": best.get("minutes"),
            "shortest_blocked": (r.get("shortest") or {}).get("blocked_for_profile")}


cases = [
    ("A photo", {"device_id": f"e2e-A-{stamp}", "category": "blocked", "type": "parked_vehicle", "body": "mw_self",
                 "lat": 26.925775, "lon": 75.807055, "accuracy_m": 12, "side": "left", "since": "always", "hurt": "road",
                 "words": "cars parked over the footpath, I had to roll on the road", "observed_at": "2026-10-25T00:30:00+05:30",
                 "location_source": "gps", "lang": "en", "details": json.dumps({"get_past": "road", "hours": "always", "vehicle": "car"})}, PHOTO),
    ("B no photo", {"device_id": f"e2e-B-{stamp}", "category": "level", "type": "kerb_no_ramp", "body": "walking_frame",
                    "lat": 26.90820, "lon": 75.81900, "accuracy_m": 8, "side": "right", "since": "month", "hurt": "turned_back",
                    "location_source": "gps", "lang": "hi", "details": json.dumps({"ramp": "none", "height": "knee"})}, None),
    ("C duplicate of A", {"device_id": f"e2e-C-{stamp}", "category": "blocked", "type": "parked_vehicle", "body": "pram_stroller",
                          "lat": 26.925800, "lon": 75.807090, "accuracy_m": 15, "side": "left", "since": "week", "hurt": "road",
                          "location_source": "map", "lang": "en"}, None),
]
rows, out = [], {"at": datetime.now().isoformat(timespec="seconds"), "api": API, "cases": []}
for name, f, photo in cases:
    rep, post_s = post(f, photo)
    done, wait_s = wait(rep["id"])
    st = {s["id"]: s for s in done["steps"]}
    ai, pr = done["ai"], done["personal"]
    pub = None
    if pr.get("ok") and pr.get("route_after"):
        a = pr["route_after"]
        pub = public_route(pr["city"], a["from"], a["to"], pr["profile"])
    row = {"case": name, "id": rep["id"], "city": done["city"], "post_s": round(post_s, 2),
           "ai_first_look_s": (st["ai_first_look"].get("detail") or {}).get("seconds"), "ai_engine": ai.get("engine"),
           "ai_models": ai.get("models_used"), "ai_error": ai.get("ai_error"), "type": ai.get("type"),
           "severity": ai.get("severity"), "duplicate_of": ai.get("duplicate_of"), "already_on_map": ai.get("already_on_map"),
           "authority": (ai.get("authority") or {}).get("office"), "confidence": ai.get("confidence"),
           "detector": {"ok": done["analyze"].get("ok"), "counts": done["analyze"].get("counts"), "s": done["analyze"].get("seconds")},
           "route_change_s": (st["personal_route"].get("detail") or {}).get("seconds"), "personal_ok": pr.get("ok"),
           "placement": pr.get("placement"), "public_placement": pr.get("public_placement"),
           "personal_before_m": (pr.get("route_before") or {}).get("length_m"), "personal_after_m": (pr.get("route_after") or {}).get("length_m"),
           "personal_after_shortest_blocked": (pr.get("route_after") or {}).get("shortest_blocked"),
           "personal_before_min": (pr.get("route_before") or {}).get("minutes"), "personal_after_min": (pr.get("route_after") or {}).get("minutes"),
           "public_same_route_min": (pub or {}).get("minutes"), "public_same_route_m": (pub or {}).get("length_m"), "public_shortest_blocked": (pub or {}).get("shortest_blocked"),
           "reply_en": (ai.get("reply") or {}).get("en"), "reply_hi": (ai.get("reply") or {}).get("hi")}
    rows.append(row)
    out["cases"].append({"row": row, "report": done})

# reviewer verifies A (token read from env or data/review-token.txt, never printed)
tok = os.environ.get("REPORTS_REVIEW_TOKEN") or open(os.path.join(ROOT, "data", "review-token.txt")).read().strip()
bad = httpx.post(f"{API}/reports/{rows[0]['id']}/verify", json={"decision": "verified"}, timeout=10)
v = httpx.post(f"{API}/reports/{rows[0]['id']}/verify", json={"decision": "verified", "by": "e2e demo reviewer"},
               headers={"X-Review-Token": tok}, timeout=10).json()
mine = httpx.get(f"{API}/reports", params={"mine": cases[0][1]["device_id"]}, timeout=10).json()
queue = os.path.join(ROOT, "data", "map-update", f"{rows[0]['city']}.input.json")
qd = json.load(open(queue)) if os.path.exists(queue) else []
out["verify"] = {"without_token_http": bad.status_code, "status": v["status"],
                 "steps": {s["id"]: s["state"] for s in v["steps"]}, "public": v["public"],
                 "queued_in_map_update_file": any(r["id"] == f"report-{rows[0]['id']}" for r in qd), "queue_file": queue}
# the detector result lands after the first look; wait for it on the photo case
for _ in range(120):
    a = httpx.get(f"{API}/reports/{rows[0]['id']}", timeout=10).json()["analyze"]
    if a.get("ok") or a.get("error"):
        break
    time.sleep(0.5)
out["detector_A_final"] = a
out["mine"] = {"device": cases[0][1]["device_id"], "count": len(mine["reports"])}
path = os.path.join(ROOT, "data", f"e2e-{stamp}.json")
json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)

for r in rows:
    print(f"{r['case']:<18} {r['id']}  city={r['city']}  post={r['post_s']}s  ai_first_look={r['ai_first_look_s']}s ({r['ai_engine']}, models={r['ai_models']})"
          f"  route_change={r['route_change_s']}s personal_ok={r['personal_ok']}  dup_of={r['duplicate_of']}  type={r['type']} sev={r['severity']}"
          f"  personal {r['personal_before_m']}->{r['personal_after_m']} m, {r['personal_before_min']}->{r['personal_after_min']} min (shortest blocked={r['personal_after_shortest_blocked']})"
          f"  public same trip={r['public_same_route_m']} m, {r['public_same_route_min']} min (shortest blocked={r['public_shortest_blocked']})  detector={r['detector']}")
    if r["ai_error"]:
        print("   ai_error:", r["ai_error"])
print("verify:", json.dumps(out["verify"]))
print("detector A (final):", json.dumps({k: a.get(k) for k in ("ok", "counts", "seconds", "error")}))
print("mine:", out["mine"], "\nsaved", path)
sys.exit(0)
