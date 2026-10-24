"""Review follow-ups: concurrent resends with one client_id store one report; a verify reversed to rejected leaves the
map-update queue; the AI thread does not overwrite a reviewer's decision; a bad lat is refused."""
import concurrent.futures as cf, json, os, time, uuid
import httpx
API = os.environ.get("REPORTS_URL", "http://127.0.0.1:8790")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
tok = os.environ.get("REPORTS_REVIEW_TOKEN") or open(os.path.join(ROOT, "data", "review-token.txt")).read().strip()
dev, cid = f"robust-{uuid.uuid4().hex[:6]}", "c-" + uuid.uuid4().hex[:8]
f = {"device_id": dev, "client_id": cid, "category": "surface", "type": "pothole", "lat": "26.92575", "lon": "75.80655"}
with cf.ThreadPoolExecutor(6) as ex:
    ids = list(ex.map(lambda _: httpx.post(f"{API}/reports", data=f, timeout=30).json()["id"], range(6)))
mine = httpx.get(f"{API}/reports", params={"mine": dev}).json()["reports"]
print("6 concurrent resends ->", len(set(ids)), "distinct id(s),", len(mine), "stored")
rid = ids[0]
v = httpx.post(f"{API}/reports/{rid}/verify", json={"decision": "verified"}, headers={"X-Review-Token": tok}).json()
q = os.path.join(ROOT, "data", "map-update", f"{v['city']}.input.json")
inq = lambda: any(r["id"].startswith(f"report-{rid}") for r in json.load(open(q)))
print("verified early (AI may still run): status", v["status"], "queued", inq())
time.sleep(6)
print("after the AI thread finished: status", httpx.get(f"{API}/reports/{rid}").json()["status"])
v2 = httpx.post(f"{API}/reports/{rid}/verify", json={"decision": "rejected"}, headers={"X-Review-Token": tok}).json()
print("reversed to rejected: status", v2["status"], "still queued", inq())
print("bad lat ->", httpx.post(f"{API}/reports", data={**f, "client_id": "x", "lat": "95"}).status_code)
