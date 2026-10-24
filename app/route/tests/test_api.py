from conftest import LAT0, LON0
from fastapi.testclient import TestClient

from hroute import api


def test_api_barriers_route_geojson(net, tmp_path, monkeypatch):
    monkeypatch.setattr(api, "net_path", lambda city: str(tmp_path / f"{city}.pkl"))
    api.NETS["synthetic"] = net
    c = TestClient(api.app)
    r = c.post("/barriers", json={"city": "synthetic", "records": [
        {"id": "a1", "type": "steps", "lat": LAT0 + 5 / 110_800, "lon": LON0 + 0.0005, "position": "barrier",
         "gps_error_m": 2, "confidence": 0.9, "status": "ACCEPT", "observed_at": "2026-10-01", "source": "test"},
        {"id": "a2", "type": "flying_carpet", "lat": LAT0, "lon": LON0}]})
    assert r.status_code == 200
    body = r.json()
    assert body["accepted"] == 1 and body["results"][1]["status"] == "REJECT"
    r = c.post("/route", json={"city": "synthetic", "start": {"lat": LAT0, "lon": LON0},
                               "end": {"lat": LAT0, "lon": LON0 + 0.002}, "profile": "manual_wheelchair",
                               "leave_time": "2026-10-25T08:00:00+05:30"})
    assert r.status_code == 200
    out = r.json()
    assert out["status"] in ("ok", "no_verified_route") and out["shortest"]["geometry"]["coordinates"]
    r = c.post("/route", json={"city": "synthetic", "start": {"lat": LAT0, "lon": LON0},
                               "end": {"lat": LAT0, "lon": LON0 + 0.002}, "all_profiles": True})
    assert len(r.json()["routes"]) == 7
    assert c.post("/route", json={"city": "synthetic", "start": {"lat": LAT0, "lon": LON0},
                                  "end": {"lat": LAT0, "lon": LON0}, "profile": "jetpack"}).status_code == 400
    gj = c.get("/network/synthetic.geojson").json()
    assert gj["type"] == "FeatureCollection" and gj["features"]
    assert {"tier", "source", "side", "evidence"} <= set(gj["features"][0]["properties"])
    assert c.get("/network/nowhere.geojson").status_code == 404


def test_api_validation_and_stats(net, tmp_path, monkeypatch):
    """fixes 12-14: empty bbox -> 422, bad leave_time -> 400, meta stats refreshed after attaching."""
    monkeypatch.setattr(api, "net_path", lambda city: str(tmp_path / f"{city}.pkl"))
    api.NETS["synthetic"] = net
    c = TestClient(api.app)
    assert c.post("/network/build", json={"city": "x", "bbox": [26.9, 75.8, 26.9, 75.9]}).status_code == 422
    assert c.post("/network/build", json={"city": "x", "bbox": [27.0, 75.8, 26.9, 75.9]}).status_code == 422
    assert c.post("/network/build", json={"city": "x", "bbox": [1, 2, 3]}).status_code == 422
    r = c.post("/route", json={"city": "synthetic", "start": {"lat": LAT0, "lon": LON0},
                               "end": {"lat": LAT0, "lon": LON0 + 0.001}, "leave_time": "tomorrow-ish"})
    assert r.status_code == 400 and "leave_time" in r.json()["detail"]
    before = net.meta.get("stats", {}).get("segments_with_evidence", 0)
    c.post("/barriers", json={"city": "synthetic", "record": {
        "id": "z1", "type": "pothole", "lat": LAT0 + 5 / 110_800, "lon": LON0 + 0.0005, "position": "barrier",
        "gps_error_m": 2, "source": "test"}})
    assert net.meta["stats"]["segments_with_evidence"] >= before + 1 or before > 0


def test_api_route_impact_engine_passthrough(net, tmp_path, monkeypatch):
    """/what-if v2 live runs: engine, body and context pass through to impact_adapter.route_with_engine."""
    monkeypatch.setattr(api, "net_path", lambda city: str(tmp_path / f"{city}.pkl"))
    api.NETS["synthetic"] = net
    c = TestClient(api.app)
    q = {"city": "synthetic", "start": {"lat": LAT0, "lon": LON0}, "end": {"lat": LAT0, "lon": LON0 + 0.002},
         "leave_time": "2026-10-25T19:00:00+05:30"}
    r = c.post("/route", json={**q, "engine": "impact", "body": "blind_cane", "context": {"weather": "rain"}})
    assert r.status_code == 200
    out = r.json()
    assert out["engine"] == "impact" and out["body"]["id"] == "blind_cane"
    assert c.post("/route", json={**q, "engine": "impact", "body": "no_such_leaf"}).status_code == 400
    assert c.post("/route", json={**q, "engine": "warp"}).status_code == 400
    assert c.post("/route", json=q).json().get("engine") is None  # legacy path unchanged
