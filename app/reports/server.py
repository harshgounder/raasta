"""RAASTA reports service: a person reports a barrier, gets an AI first look in seconds, their own routes
change at once, a human verifies, and verified reports go into the next public map update.

Run from app/reports:
  .venv/bin/uvicorn server:app --host 127.0.0.1 --port 8790

POST /reports                 multipart: photo (optional) + form fields (see ReportIn below)
GET  /reports/{id}            the report and its status trail
GET  /reports?mine=<device>   one person's past reports (anonymous device id kept in localStorage)
POST /reports/{id}/verify     reviewer action, header X-Review-Token (env REPORTS_REVIEW_TOKEN, or data/review-token.txt)
GET  /reports/{id}/photo      the uploaded photo
GET  /health                  service state, which neighbours answer, which AI models are configured

Neighbours (called over HTTP, never imported): the /analyze detector (ANALYZE_URL, default :8010) and the routing
service (ROUTE_URL, default :8020, POST /barriers and /route). See REPORT-BUILD.md for the design and its whys.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, File, Form, Header, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import ai
import lookups as L

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("REPORTS_DATA", os.path.join(HERE, "data"))
DB = os.path.join(DATA, "reports.db")
PHOTOS = os.path.join(DATA, "photos")
ANALYZE_URL = os.environ.get("ANALYZE_URL", "http://127.0.0.1:8010").rstrip("/")
ROUTE_URL = os.environ.get("ROUTE_URL", "http://127.0.0.1:8020").rstrip("/")
ROUTE_NETS = os.path.abspath(os.path.join(HERE, "..", "route", "cache", "networks"))
IST = timezone(timedelta(hours=5, minutes=30))
# promises shown to the person. demo values, stated as such in the UI
VERIFY_HOURS = float(os.environ.get("REPORTS_VERIFY_HOURS", "24"))
ANSWER_HOURS = float(os.environ.get("REPORTS_ANSWER_HOURS", "48"))
MAX_PHOTO = 15 * 1024 * 1024
DUP_RADIUS_M = 30.0

os.makedirs(PHOTOS, exist_ok=True)
import httpx  # noqa: E402

app = FastAPI(title="RAASTA reports", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
DBLOCK = threading.Lock()
NETLOCK = threading.Lock()
RATE: dict = {}  # ip -> recent POST times (simple flood guard; each new device id costs a network copy)
RATE_MAX = int(os.environ.get("REPORTS_RATE_MAX", "30"))  # per 10 minutes per IP


def now() -> datetime:
    return datetime.now(IST)


def iso(d: datetime | None) -> str | None:
    return d.isoformat(timespec="seconds") if d else None


def review_token() -> str:
    t = os.environ.get("REPORTS_REVIEW_TOKEN")
    if t:
        return t
    p = os.path.join(DATA, "review-token.txt")
    if not os.path.exists(p):
        with open(p, "w") as f:
            f.write(uuid.uuid4().hex)
        os.chmod(p, 0o600)
    return open(p).read().strip()


def next_map_update(d: datetime) -> datetime:
    """public map updates: every Sunday 06:00 IST (demo cadence, an assumption shown in the UI)."""
    days = (6 - d.weekday()) % 7
    t = (d + timedelta(days=days)).replace(hour=6, minute=0, second=0, microsecond=0)
    return t if t > d else t + timedelta(days=7)


# ---------------------------------------------------------------- storage

def db() -> sqlite3.Connection:
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    return c


with db() as c:
    c.executescript("""
    CREATE TABLE IF NOT EXISTS reports (
      id TEXT PRIMARY KEY, device_id TEXT, created_at TEXT, lat REAL, lon REAL, accuracy_m REAL,
      category TEXT, type TEXT, body TEXT, fields TEXT, photo TEXT, city TEXT,
      status TEXT, steps TEXT, ai TEXT, analyze TEXT, personal TEXT, public TEXT, review TEXT, dup_of TEXT);
    CREATE INDEX IF NOT EXISTS reports_device ON reports(device_id);
    CREATE TABLE IF NOT EXISTS events (report_id TEXT, at TEXT, step TEXT, detail TEXT);
    """)
with db() as c:
    cols = {r[1] for r in c.execute("PRAGMA table_info(reports)")}
    if "client_id" not in cols:
        c.execute("ALTER TABLE reports ADD COLUMN client_id TEXT")
        c.execute("UPDATE reports SET client_id=json_extract(fields,'$.client_id') WHERE client_id IS NULL")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS reports_client ON reports(device_id, client_id) WHERE client_id IS NOT NULL")
    # steps left 'active' by a restart (daemon threads die with the process) are marked failed, so pages stop polling
    for r in c.execute("SELECT id, steps FROM reports WHERE steps LIKE '%\"active\"%'").fetchall():
        st = json.loads(r["steps"])
        for x in st:
            if x["state"] == "active" and x["id"] in ("ai_first_look", "personal_route"):
                x["state"] = "failed"
                x["at"] = datetime.now(IST).isoformat(timespec="seconds")
                x.setdefault("detail", {})["why"] = "the service restarted while this step ran"
        c.execute("UPDATE reports SET steps=? WHERE id=?", [json.dumps(st, ensure_ascii=False), r["id"]])
review_token()  # make sure the demo reviewer token exists (data/review-token.txt, 0600) unless the env sets one


def jload(s, default=None):
    try:
        return json.loads(s) if s else default
    except ValueError:
        return default


def save(rid: str, **cols):
    sets = ", ".join(f"{k}=?" for k in cols)
    vals = [json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for v in cols.values()]
    with DBLOCK, db() as c:
        c.execute(f"UPDATE reports SET {sets} WHERE id=?", [*vals, rid])


def load(rid: str) -> dict | None:
    with db() as c:
        r = c.execute("SELECT * FROM reports WHERE id=?", [rid]).fetchone()
    if not r:
        return None
    d = dict(r)
    for k in ("fields", "steps", "ai", "analyze", "personal", "public", "review"):
        d[k] = jload(d[k], {} if k != "steps" else [])
    return d


def set_step(rid: str, step: str, state: str, detail: dict | None = None, at: datetime | None = None):
    """state: done | active | waiting | failed | skipped."""
    with DBLOCK, db() as c:
        row = c.execute("SELECT steps FROM reports WHERE id=?", [rid]).fetchone()
        steps = jload(row["steps"], []) if row else []
        for s in steps:
            if s["id"] == step:
                s["state"] = state
                if state in ("done", "failed", "skipped"):
                    s["at"] = iso(at or now())
                if detail:
                    s.setdefault("detail", {}).update(detail)
        c.execute("UPDATE reports SET steps=? WHERE id=?", [json.dumps(steps, ensure_ascii=False), rid])
        c.execute("INSERT INTO events VALUES (?,?,?,?)", [rid, iso(now()), f"{step}:{state}",
                                                          json.dumps(detail or {}, ensure_ascii=False)[:4000]])


def initial_steps(created: datetime) -> list[dict]:
    return [
        {"id": "received", "state": "done", "at": iso(created)},
        {"id": "ai_first_look", "state": "active", "eta": iso(created + timedelta(seconds=20))},
        {"id": "personal_route", "state": "active", "eta": iso(created + timedelta(seconds=30))},
        {"id": "human_verification", "state": "waiting", "eta": iso(created + timedelta(hours=VERIFY_HOURS)),
         "detail": {"reviewer": "demo reviewer (a RAASTA team member), not a city official"}},
        {"id": "answer", "state": "waiting", "eta": iso(created + timedelta(hours=ANSWER_HOURS))},
        {"id": "public_update", "state": "waiting", "eta": iso(next_map_update(created + timedelta(hours=VERIFY_HOURS))),
         "detail": {"cadence": "weekly, Sunday 06:00 IST (demo cadence)"}},
    ]


# ---------------------------------------------------------------- geometry helpers

def haversine(a_lat, a_lon, b_lat, b_lon) -> float:
    r = 6371000.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp, dl = p2 - p1, math.radians(b_lon - a_lon)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def nearby_reports(rid, lat, lon, radius=DUP_RADIUS_M) -> list[dict]:
    if lat is None or lon is None:
        return []
    d = radius / 111000.0
    with db() as c:
        rows = c.execute("SELECT id, lat, lon, category, type, created_at, status, device_id FROM reports "
                         "WHERE id != ? AND lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?",
                         [rid, lat - d, lat + d, lon - d * 1.2, lon + d * 1.2]).fetchall()
    out = []
    for r in rows:
        m = haversine(lat, lon, r["lat"], r["lon"])
        if m <= radius and r["status"] != "rejected":
            out.append({"id": r["id"], "distance_m": round(m, 1), "category": r["category"], "type": r["type"],
                        "created_at": r["created_at"], "status": r["status"]})
    return sorted(out, key=lambda x: x["distance_m"])


# ---------------------------------------------------------------- neighbours

def call_analyze(photo_path: str, captured_at: str | None) -> dict:
    """the /analyze detector on the photo. We send the image ONLY: with a city plus lat/lon, /analyze would POST the
    detections to the PUBLIC route network itself (raasta/place.py), which must wait for human verification."""
    t0 = time.time()
    try:
        with open(photo_path, "rb") as f:
            r = httpx.post(f"{ANALYZE_URL}/analyze", files={"image": (os.path.basename(photo_path), f, "image/jpeg")},
                           data={"captured_at": captured_at} if captured_at else {}, timeout=90)
        if r.status_code != 200:
            return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}", "seconds": round(time.time() - t0, 2)}
        rc = r.json()
        dets = [{k: d.get(k) for k in ("class", "class_family", "status", "confidence", "side_hint", "distance_m",
                                        "height_cm", "height_err_cm", "why")}
                for d in rc.get("detections", []) if d.get("status") in ("ACCEPT", "ABSTAIN")][:12]
        return {"ok": True, "receipt_id": rc.get("id"), "counts": rc.get("counts"), "detections": dets,
                "condition": rc.get("condition_bin"), "models": {k: v for k, v in (rc.get("models") or {}).items()
                                                                  if k.startswith("detector") or k == "depth"},
                "seconds": round(time.time() - t0, 2), "pipeline_s": (rc.get("timings") or {}).get("total_s")}
    except httpx.HTTPError as e:
        return {"ok": False, "error": f"/analyze not reachable at {ANALYZE_URL} ({type(e).__name__})",
                "seconds": round(time.time() - t0, 2)}
    except Exception as e:  # noqa: BLE001  (non-JSON body, unreadable photo): never kill the pipeline thread
        return {"ok": False, "error": f"/analyze answer unusable ({type(e).__name__})", "seconds": round(time.time() - t0, 2)}


def personal_city(device_id: str, city: str) -> str:
    return f"u{abs(hash_dev(device_id)) % 10**10:010d}--{city}"


def hash_dev(s: str) -> int:
    import hashlib
    return int(hashlib.sha256(s.encode()).hexdigest()[:12], 16)


def ensure_personal_net(pcity: str, city: str) -> bool:
    """the reporter's own copy of the city network: same file the routing service saved, under a personal name.
    The routing service loads it like any city; public routes never see what is attached here."""
    dst = os.path.join(ROUTE_NETS, f"{pcity}.pkl")
    with NETLOCK:
        if os.path.exists(dst):
            return False
        src = os.path.join(ROUTE_NETS, f"{city}.pkl")
        tmp = f"{dst}.{uuid.uuid4().hex}.tmp"
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
        return True


def route_record(rep: dict, route_type: str, status: str = "ACCEPT") -> dict:
    f = rep["fields"]
    side = f.get("side")
    rec = {"id": f"report-{rep['id']}", "type": route_type, "lat": rep["lat"], "lon": rep["lon"],
           "position": "barrier", "gps_error_m": max(5.0, min(float(rep.get("accuracy_m") or 15), 60.0)),
           "confidence": 0.6, "status": status, "observed_at": f.get("observed_at") or rep["created_at"],
           "source": "upload", "label": f"reported by a person, {rep.get('status', 'unverified')}: {f.get('type_label', route_type)}",
           "ref": f"RAASTA report {rep['id']}"}
    if side in ("left", "right"):
        rec["side_hint"] = side
    hints, _ = L.detail_hints(rep.get("category"), f.get("details"))
    for k, v in hints.items():  # the person's own answers: kerb height, width left
        rec[k] = v
    return rec


def f_side_both(rep: dict) -> bool:
    return (rep.get("fields") or {}).get("side") == "both"


def route_check(city: str, seg_id: str, profile: str) -> dict | None:
    seg = L.segment_coords(city, seg_id)
    if not seg:
        return None
    (lon1, lat1), (lon2, lat2) = seg[0], seg[-1]
    r = httpx.post(f"{ROUTE_URL}/route", json={"city": city, "start": {"lat": lat1, "lon": lon1},
                                               "end": {"lat": lat2, "lon": lon2}, "profile": profile}, timeout=30)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}"}
    d = r.json()
    best = d.get("accessible") or d.get("least_blocked") or {}
    mine = [b for b in (best.get("barriers") or []) + (best.get("blocking") or [])
            if str(b.get("evidence_id") or "").startswith("report-")]
    short = d.get("shortest") or {}
    return {"status": d.get("status"), "uses_segment": seg_id in (best.get("segment_ids") or []),
            "report_on_route": [{k: b.get(k) for k in ("evidence_id", "type", "blocking", "why")} for b in mine][:4],
            "shortest_hits_report": any(str(b.get("evidence_id") or "").startswith("report-")
                                        for b in (short.get("barriers") or []) + (short.get("blocking") or [])),
            "shortest_blocked": short.get("blocked_for_profile"), "shortest_length_m": short.get("length_m"),
            "length_m": best.get("length_m"), "minutes": best.get("minutes"),
            "blocked_for_profile": best.get("blocked_for_profile"), "summary": d.get("summary"),
            "from": [lat1, lon1], "to": [lat2, lon2]}


def attach_personal(rep: dict, route_type: str, profile: str) -> dict:
    t0 = time.time()
    city = rep.get("city")
    if not city:
        return {"ok": False, "why": "this place is outside the areas we have mapped so far; it goes into the next "
                                    "map update instead", "seconds": 0}
    pcity = personal_city(rep["device_id"], city)
    created = ensure_personal_net(pcity, city)
    rec = route_record(rep, route_type)
    try:
        dr = httpx.post(f"{ROUTE_URL}/barriers", json={"city": pcity, "record": rec, "commit": False}, timeout=30)
        if dr.status_code != 200:
            return {"ok": False, "why": f"routing service HTTP {dr.status_code}: {dr.text[:160]}", "seconds": round(time.time() - t0, 2)}
        dry = dr.json()
        res0 = (dry.get("results") or [{}])[0]
        cands = res0.get("candidates") or []
        seg = res0.get("segment_id") or (cands[0].get("segment_id") if cands else None)
        how = "placed by the routing service (p >= its accept bar)"
        if res0.get("status") != "ACCEPT" and cands:
            # the public bar (p >= 0.7) is for evidence nobody stood next to. The person was there, so on THEIR
            # own network the report goes on the nearest footpath piece; the public map waits for a human check.
            rec["segment_id"] = seg
            if cands[0].get("at_m") is not None:
                rec["at_m"] = cands[0]["at_m"]
            how = (f"placed on the nearest footpath piece {seg} ({cands[0].get('distance_m')} m away, routing p="
                   f"{cands[0].get('p')}); the public placement waits for a person to confirm the spot")
        before = route_check(pcity, seg, profile) if seg else None
        r = httpx.post(f"{ROUTE_URL}/barriers", json={"city": pcity, "record": rec, "commit": True}, timeout=30)
        if r.status_code == 200 and f_side_both(rep) and len(cands) > 1:
            rec2 = {**rec, "id": rec["id"] + "-b", "segment_id": cands[1]["segment_id"]}
            rec2.pop("at_m", None)
            httpx.post(f"{ROUTE_URL}/barriers", json={"city": pcity, "record": rec2, "commit": True}, timeout=30)
        if r.status_code != 200:
            return {"ok": False, "why": f"routing service HTTP {r.status_code}: {r.text[:160]}", "seconds": round(time.time() - t0, 2)}
        res = (r.json().get("results") or [{}])[0]
        after = route_check(pcity, res.get("segment_id") or seg, profile) if (res.get("segment_id") or seg) else None
    except httpx.HTTPError as e:
        return {"ok": False, "why": f"routing service not reachable at {ROUTE_URL} ({type(e).__name__})",
                "seconds": round(time.time() - t0, 2)}
    return {"ok": res.get("status") == "ACCEPT", "personal_city": pcity, "new_copy": created, "city": city,
            "placement": {k: res.get(k) for k in ("status", "segment_id", "p", "reason")}, "how": how,
            "public_placement": {k: res0.get(k) for k in ("status", "segment_id", "p", "reason")},
            "candidates": [{k: c.get(k) for k in ("segment_id", "p", "distance_m", "side", "kind")}
                           for c in (res.get("candidates") or [])[:3]],
            "profile": profile, "route_before": before, "route_after": after,
            "record_status": "reported, unverified", "seconds": round(time.time() - t0, 2)}


# ---------------------------------------------------------------- the first-look pipeline

def personal_step(rid: str, t_recv: datetime, route_type: str | None):
    """the person's own routes: attach at once, as "reported, unverified"."""
    rep = load(rid)
    f = rep["fields"]
    profile = L.profile_for_body(rep.get("body")) or "manual_wheelchair"
    if not route_type:
        save(rid, personal={"ok": False, "why": "this kind of problem does not change footpath routing yet; it is "
                                                 "still recorded and sent to the authority"})
        set_step(rid, "personal_route", "skipped", {"why": "not a routing barrier type"})
    elif rep["lat"] is None:
        save(rid, personal={"ok": False, "why": "no location given"})
        set_step(rid, "personal_route", "skipped", {"why": "no location"})
    else:
        try:
            pr = attach_personal(rep, route_type, profile)
        except Exception as e:  # noqa: BLE001
            pr = {"ok": False, "why": f"could not attach: {type(e).__name__}: {str(e)[:160]}"}
        pr["seconds_since_received"] = round((now() - t_recv).total_seconds(), 2)
        save(rid, personal=pr)
        set_step(rid, "personal_route", "done" if pr.get("ok") else "skipped" if not rep.get("city") else "failed",
                 {"seconds": pr["seconds_since_received"], "why": pr.get("why"),
                  "placement": (pr.get("placement") or {}).get("status")})


def first_look(rid: str):
    rep = load(rid)
    t_recv = datetime.fromisoformat(rep["created_at"])
    f = rep["fields"]
    photo = os.path.join(PHOTOS, rep["photo"]) if rep.get("photo") else None
    results: dict = {}

    def run_analyze():
        results["analyze"] = call_analyze(photo, f.get("observed_at")) if photo else {"ok": False, "skipped": "no photo"}

    th = threading.Thread(target=run_analyze, daemon=True)
    th.start()
    # the personal route does not wait for the AI: the person's own choice of type is enough to avoid it now
    form_rt = (L.form_type(rep["type"]) or {}).get("route_type")
    pth = threading.Thread(target=personal_step, args=(rid, t_recv, form_rt), daemon=True) if form_rt else None
    if pth:
        pth.start()
    near = nearby_reports(rid, rep["lat"], rep["lon"])
    known = L.known_barriers_near(rep.get("city"), rep["lat"], rep["lon"], DUP_RADIUS_M)
    # the AI first look runs alongside /analyze; it waits for the detector at most a few seconds
    th.join(timeout=float(os.environ.get("REPORTS_ANALYZE_WAIT_S", "4")))
    an = results.get("analyze") or {"ok": False, "pending": "detector still running; added to the report when done"}
    try:
        look = ai.first_look(rep, an, near, known, photo)
    except Exception as e:  # noqa: BLE001
        look = {"engine": "first look failed", "engine_ok": False, "failed": True, "ai_error": f"{type(e).__name__}: {str(e)[:200]}"}
    elapsed = (now() - t_recv).total_seconds()
    look["seconds_since_received"] = round(elapsed, 2)
    dup = look.get("duplicate_of")
    save(rid, ai=look, analyze=an, dup_of=dup if dup else None)
    with DBLOCK, db() as c:  # never overwrite a reviewer's decision that landed while the AI ran
        c.execute("UPDATE reports SET status='ai_checked' WHERE id=? AND status='received'", [rid])
    set_step(rid, "ai_first_look", "failed" if look.get("failed") else "done",
             {"seconds": round(elapsed, 2), "engine": look.get("engine"), "models": look.get("models_used")})
    if pth:
        pth.join(timeout=120)
    else:  # the form type is not a routing type: maybe the AI's element is
        personal_step(rid, t_recv, L.route_type_for_element(look.get("element")))
    if th.is_alive():
        th.join(timeout=90)
    if results.get("analyze") and results["analyze"] is not an:
        save(rid, analyze=results["analyze"])


def warm():
    """load each city's segment geometry once, so the first report in a city does not pay for it."""
    for c in L.city_boxes():
        try:
            L.segment_coords(c, "")
        except Exception:  # noqa: BLE001
            pass


threading.Thread(target=warm, daemon=True).start()


# ---------------------------------------------------------------- API

def public_view(rep: dict) -> dict:
    out = {k: rep[k] for k in ("id", "created_at", "lat", "lon", "accuracy_m", "category", "type", "body", "city",
                               "status", "steps", "ai", "personal", "review", "dup_of")}
    out["fields"] = {k: v for k, v in rep["fields"].items() if k not in ("contact",)}
    out["has_contact"] = bool(rep["fields"].get("contact"))
    out["photo_url"] = f"/reports/{rep['id']}/photo" if rep.get("photo") else None
    an = rep.get("analyze") or {}
    out["analyze"] = {k: an.get(k) for k in ("ok", "counts", "detections", "condition", "seconds", "error", "skipped",
                                              "pending", "models")}
    out["public"] = rep.get("public") or {}
    a = L.authorities()
    out["contacts"] = {"honest_line": a.get("honest_line"), "escalation": a.get("escalation") if (rep.get("city") or "").startswith("jaipur") else None}
    # authority shown from the CURRENT checked table (contacts can be corrected after a report was made)
    if out.get("ai") and out["ai"].get("authority", {}).get("office"):
        ft = L.form_type(out["ai"].get("type")) or {}
        cur = {x["office"]: x for x in L.authority_options(rep.get("city"))}
        out["ai"] = {**out["ai"], "authority": cur.get(out["ai"]["authority"]["office"]) or L.authority_for(rep.get("city"), ft.get("category"), ft.get("id"))}
    out["promises"] = {"verify_hours": VERIFY_HOURS, "answer_hours": ANSWER_HOURS,
                       "reviewer": "demo reviewer (a RAASTA team member), not a city official",
                       "map_update": "weekly, Sunday 06:00 IST (demo cadence)"}
    return out


@app.get("/health")
def health():
    def ping(url):
        try:
            return httpx.get(url, timeout=3).status_code == 200
        except httpx.HTTPError:
            return False
    with db() as c:
        n = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    return {"ok": True, "reports": n, "analyze": {"url": ANALYZE_URL, "up": ping(f"{ANALYZE_URL}/health")},
            "route": {"url": ROUTE_URL, "up": ping(f"{ROUTE_URL}/health")}, "ai": ai.info(),
            "cities": L.city_names(), "promises": {"verify_hours": VERIFY_HOURS, "answer_hours": ANSWER_HOURS}}


@app.post("/reports")
async def create_report(
    request: Request,
    device_id: str = Form(...), category: str = Form(...), type: str = Form(...), body: str | None = Form(None),
    lat: float | None = Form(None), lon: float | None = Form(None), accuracy_m: float | None = Form(None),
    location_source: str | None = Form(None), side: str | None = Form(None), observed_at: str | None = Form(None),
    since: str | None = Form(None), hurt: str | None = Form(None), words: str | None = Form(None),
    contact: str | None = Form(None), lang: str | None = Form(None), client_id: str | None = Form(None),
    details: str | None = Form(None),
    photo: UploadFile | None = File(None),
):
    if not device_id or len(device_id) > 80:
        raise HTTPException(422, "device_id required")
    if (lat is None) != (lon is None) or (lat is not None and not (-90 <= lat <= 90 and -180 <= lon <= 180)):
        raise HTTPException(422, "lat and lon must come together and be valid")
    ip = request.client.host if request.client else "?"
    t_now = time.time()
    RATE[ip] = [t for t in RATE.get(ip, []) if t_now - t < 600] + [t_now]
    if len(RATE[ip]) > RATE_MAX:
        raise HTTPException(429, "too many reports from this address; try again in a few minutes")
    created = now()
    rid = "r-" + created.strftime("%y%m%d") + "-" + uuid.uuid4().hex[:8]
    data, pname = b"", None
    if photo is not None and photo.filename:
        data = await photo.read()
        if len(data) > MAX_PHOTO:
            raise HTTPException(413, "photo over 15 MB")
        if data:
            ext = os.path.splitext(photo.filename)[1].lower()
            ext = ext if ext in (".jpg", ".jpeg", ".png", ".webp", ".heic") else ".jpg"
            pname = f"{rid}{ext}"
    ft = L.form_type(type)
    try:
        det = json.loads(details) if details else {}
        det = {str(k)[:40]: str(v)[:40] for k, v in det.items()} if isinstance(det, dict) else {}
    except ValueError:
        det = {}
    fields = {"details": det, "side": side, "observed_at": observed_at, "since": since, "hurt": hurt, "words": (words or "")[:2000],
              "contact": (contact or "")[:200], "lang": lang, "location_source": location_source,
              "client_id": client_id, "type_label": (ft or {}).get("en", type)}
    city = L.city_for(lat, lon) if lat is not None else None
    with DBLOCK, db() as c:
        # a report sent again from the offline queue: return the one already stored (check + insert under one lock,
        # plus a unique index on (device_id, client_id))
        if client_id:
            r = c.execute("SELECT id FROM reports WHERE device_id=? AND client_id=?", [device_id, client_id]).fetchone()
            if r:
                existing = r["id"]
                c.commit()
                return public_view(load(existing))
        c.execute("INSERT INTO reports (id, device_id, created_at, lat, lon, accuracy_m, category, type, body, fields, "
                  "photo, city, status, steps, client_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  [rid, device_id, iso(created), lat, lon, accuracy_m, category, type, body,
                   json.dumps(fields, ensure_ascii=False), pname, city, "received",
                   json.dumps(initial_steps(created)), client_id or None])
        c.execute("INSERT INTO events VALUES (?,?,?,?)", [rid, iso(created), "received:done", "{}"])
    if pname:
        with open(os.path.join(PHOTOS, pname), "wb") as fh:
            fh.write(data)
    threading.Thread(target=first_look, args=(rid,), daemon=True).start()
    return public_view(load(rid))


@app.get("/reports/{rid}")
def get_report(rid: str):
    rep = load(rid)
    if not rep:
        raise HTTPException(404, "no such report")
    return public_view(rep)


@app.get("/reports/{rid}/photo")
def get_photo(rid: str):
    rep = load(rid)
    if not rep or not rep.get("photo"):
        raise HTTPException(404, "no photo")
    return FileResponse(os.path.join(PHOTOS, rep["photo"]))


@app.get("/reports")
def list_reports(mine: str = Query(..., min_length=4, max_length=80)):
    with db() as c:
        ids = [r["id"] for r in c.execute("SELECT id FROM reports WHERE device_id=? ORDER BY created_at DESC LIMIT 100",
                                          [mine]).fetchall()]
    out = []
    for i in ids:
        v = public_view(load(i))
        out.append({k: v[k] for k in ("id", "created_at", "category", "type", "status", "steps", "city", "dup_of")}
                   | {"type_label": v["fields"].get("type_label"), "ai_reply": (v["ai"] or {}).get("reply")})
    return {"device": mine, "reports": out}


@app.post("/reports/{rid}/verify")
def verify(rid: str, payload: dict, x_review_token: str | None = Header(None)):
    if not x_review_token or x_review_token != review_token():
        raise HTTPException(401, "reviewer token required (X-Review-Token)")
    rep = load(rid)
    if not rep:
        raise HTTPException(404, "no such report")
    decision = payload.get("decision", "verified")
    if decision not in ("verified", "rejected", "duplicate"):
        raise HTTPException(422, "decision: verified | rejected | duplicate")
    t = now()
    review = {"decision": decision, "note": (payload.get("note") or "")[:1000], "by": payload.get("by") or "demo reviewer",
              "at": iso(t), "answer": payload.get("answer") or {}}
    if not review["answer"]:
        a = (rep.get("ai") or {}).get("authority") or {}
        review["answer"] = {
            "en": ("A person on our team checked your report and confirmed it. It is on your routes now and goes on the "
                   f"public map in the next update. We are sending it to {a.get('name', 'the city office')}.")
            if decision == "verified" else "A person on our team checked your report and could not confirm it. Your own "
            "routes keep avoiding it until you remove it.",
            "hi": ("हमारी टीम के एक व्यक्ति ने आपकी शिकायत जाँची और सही पाई. यह अभी आपके रास्तों में है और अगले अपडेट में सबके नक्शे पर "
                   f"आएगी. हम इसे {a.get('name_hi') or a.get('name', 'नगर निगम')} को भेज रहे हैं.")
            if decision == "verified" else "हमारी टीम ने आपकी शिकायत जाँची पर पक्की नहीं कर पाई. आपके अपने रास्ते इससे बचते रहेंगे."}
    public = rep.get("public") or {}
    if decision != "verified":
        L.unqueue_from_map_update(rep)  # a verify reversed later must not reach the public map
    if decision == "verified":
        rt = (L.form_type(rep["type"]) or {}).get("route_type") or L.route_type_for_element((rep.get("ai") or {}).get("element"))
        if rt:
            public = {"queued": True, "update_at": iso(next_map_update(t)), "status": "queued for the next map update"}
            L.queue_for_map_update(rep, route_record(rep, rt))
        else:  # crossings, light, safety: not a footpath routing type yet; it is still on the record and the complaint
            public = {"queued": False, "update_at": iso(next_map_update(t)),
                      "status": "recorded for the public map notes; this kind of problem does not change routes yet"}
    save(rid, review=review, public=public, status=decision)
    set_step(rid, "human_verification", "done", {"decision": decision, "by": review["by"]}, at=t)
    set_step(rid, "answer", "done", {"answer": review["answer"]}, at=t)
    if decision == "verified":
        set_step(rid, "public_update", "active", {"update_at": public["update_at"]})
    else:
        set_step(rid, "public_update", "skipped", {"why": decision})
    return public_view(load(rid))
