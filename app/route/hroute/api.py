"""FastAPI service for lane B2.

POST /network/build   {city, bbox:[south, west, north, east]} or {city, place}
POST /barriers        {city, records:[...], commit?:true}  or {city, record:{...}}
POST /route           {city, start:{lat,lon}, end:{lat,lon}, profile?, leave_time?, all_profiles?,
                       engine?: "legacy"|"impact", body?: body leaf id, context?: {weather, light, hour, ...}}
GET  /network/{city}.geojson
GET  /health, GET /profiles, GET /assumptions

Run: .venv/bin/uvicorn hroute.api:app --port 8020   (from app/route)
"""
from __future__ import annotations

import os
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import attach as A
from . import routing as R
from .config import CACHE, PROFILES, cfg
from .costs import tier
from .network import FootNetwork, build_network

app = FastAPI(title="hypnexis route (SC-02 lane B2)", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

NETS: dict[str, FootNetwork] = {}
LOCK = threading.Lock()


def net_path(city):
    return os.path.join(CACHE, "networks", f"{city}.pkl")


def get_net(city: str) -> FootNetwork:
    if city not in NETS:
        p = net_path(city)
        if not os.path.exists(p):
            raise HTTPException(404, f"no network for {city!r}; POST /network/build first")
        NETS[city] = FootNetwork.load(p)
    return NETS[city]


class BuildReq(BaseModel):
    city: str
    bbox: list[float] | None = Field(None, description="[south, west, north, east]")
    place: str | None = None
    refresh: bool = False


class BarrierReq(BaseModel):
    city: str
    records: list[dict] | None = None
    record: dict | None = None
    commit: bool = True


class Pt(BaseModel):
    lat: float
    lon: float


class RouteReq(BaseModel):
    city: str
    start: Pt
    end: Pt
    profile: str = "manual_wheelchair"
    leave_time: str | None = None
    all_profiles: bool = False
    engine: str = "legacy"           # "impact": per body leaf via hroute.impact_adapter (what-if page live runs)
    body: str | None = None          # body leaf id (taxonomy/bodies.json); defaults to the profile's leaf
    context: dict | None = None      # impact engine context: weather, light, hour, temp_c, season, ...


@app.get("/health")
def health():
    return {"ok": True, "loaded": list(NETS), "cached": sorted(
        f[:-4] for f in os.listdir(os.path.join(CACHE, "networks")) if f.endswith(".pkl"))
        if os.path.isdir(os.path.join(CACHE, "networks")) else []}


@app.get("/profiles")
def profiles():
    return {p: cfg()["profiles"][p] for p in PROFILES}


@app.get("/assumptions")
def assumptions():
    return cfg()


@app.post("/network/build")
def network_build(req: BuildReq):
    if not req.bbox and not req.place:
        raise HTTPException(400, "give bbox [south, west, north, east] or place")
    if req.bbox is not None:
        if len(req.bbox) != 4:
            raise HTTPException(422, "bbox must be [south, west, north, east]")
        so, we, no, ea = req.bbox
        if not (-90 <= so < no <= 90 and -180 <= we < ea <= 180):
            raise HTTPException(422, "empty or inverted bbox: need south < north and west < east")
        if (no - so) * (ea - we) > 0.01:
            raise HTTPException(422, "bbox too large for one build (max about 0.01 square degrees)")
    with LOCK:
        try:
            net = build_network(req.city, bbox=tuple(req.bbox) if req.bbox else None, place=req.place,
                                refresh=req.refresh)
        except Exception as ex:  # empty area, geocoder miss, OSM fetch failure
            raise HTTPException(422, f"could not build a network: {type(ex).__name__}: {ex}")
        if not net.segments:
            raise HTTPException(422, "no walkable ways found in this area")
        net.save(net_path(req.city))
        NETS[req.city] = net
    return {"city": req.city, "meta": {k: v for k, v in net.meta.items() if k != "placements"}}


@app.post("/barriers")
def barriers(req: BarrierReq):
    net = get_net(req.city)
    recs = list(req.records or []) + ([req.record] if req.record else [])
    if not recs:
        raise HTTPException(400, "no records")
    out = []
    with LOCK:
        for r in recs:
            try:
                out.append(A.attach(net, r, commit=req.commit))
            except ValueError as e:
                out.append({"record_id": r.get("id"), "status": "REJECT", "reason": str(e)})
        if req.commit:
            net.invalidate()
            net.meta["stats"] = net.stats()
            net.save(net_path(req.city))
    return {"city": req.city, "results": out,
            "accepted": sum(1 for o in out if o.get("status") == "ACCEPT"),
            "abstained": sum(1 for o in out if o.get("status") == "ABSTAIN")}


@app.post("/route")
def route(req: RouteReq):
    net = get_net(req.city)
    s, e = (req.start.lat, req.start.lon), (req.end.lat, req.end.lon)
    try:
        with LOCK:
            return _route(net, req, s, e)
    except ValueError as ex:
        raise HTTPException(400, str(ex))


def _route(net, req, s, e):
    if req.engine != "legacy":
        from .impact_adapter import route_with_engine
        try:
            return route_with_engine(net, s, e, req.body or req.profile, req.leave_time, engine=req.engine,
                                     context=req.context)
        except KeyError as ex:
            raise ValueError(f"unknown body leaf {ex}")
    if req.all_profiles:
        return {"city": req.city, "routes": R.route_all_profiles(net, s, e, req.leave_time)}
    return R.route(net, s, e, req.profile, req.leave_time)


@app.get("/network/{city}.geojson")
def network_geojson(city: str):
    return get_net(city).to_geojson(tier_fn=tier)
