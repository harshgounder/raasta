"""FastAPI service for /analyze.

Run from app/analyze:
  .venv/bin/uvicorn server:app --host 127.0.0.1 --port 8010
POST /analyze  multipart: image (file), optional lat, lon, heading, captured_at (ISO), city, gps_error_m
  -> receipt JSON (raasta-receipt-v1). ?annotated=1 also returns the annotated JPEG as base64.
GET  /health, /models
"""
from __future__ import annotations

import base64
import io
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from raasta import models, pipeline
from raasta.draw import annotate

def _warm():
    """Load all four models once with a blank image so the first real upload is not a cold start."""
    import os
    from PIL import Image
    if os.environ.get("ANALYZE_WARMUP", "1") != "1":
        return
    buf = io.BytesIO()
    Image.new("RGB", (640, 480), (128, 128, 128)).save(buf, "JPEG")
    os.environ.setdefault("ANALYZE_JUDGE", "1")
    try:
        models.yoloe(); models.owl(); models.depth_model(); models.seg_model()
        pipeline.analyze(buf.getvalue(), {})
        from raasta import vlm as _v
        from PIL import Image as _I
        _v.describe(_I.new("RGB", (64, 48), (128, 128, 128)), [], budget_s=8)   # marks dead providers once
    except Exception as e:  # noqa: BLE001
        print("warm-up failed:", type(e).__name__, e, flush=True)


@asynccontextmanager
async def lifespan(_app):
    await run_in_threadpool(_warm)
    yield


app = FastAPI(title="RAASTA /analyze", version="1", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MAX_BYTES = 25 * 1024 * 1024


@app.get("/health")
def health():
    return {"ok": True, "device": models.device(), "loaded": sorted(models._models)}


@app.get("/models")
def model_info():
    return models.versions()


@app.post("/analyze")
async def analyze(image: UploadFile = File(...), lat: str | None = Form(None), lon: str | None = Form(None),
                  heading: str | None = Form(None), captured_at: str | None = Form(None),
                  city: str | None = Form(None), gps_error_m: str | None = Form(None),
                  annotated: int = 0):
    data = await image.read()
    if not data:
        raise HTTPException(400, "empty image")
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "image over 25 MB")
    form = {"lat": lat, "lon": lon, "heading": heading, "captured_at": captured_at, "city": city,
            "gps_error_m": gps_error_m, "filename": image.filename}
    try:
        receipt, img = await run_in_threadpool(pipeline.analyze, data, form)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(422, f"could not analyse image: {type(e).__name__}: {e}") from e
    if annotated:
        buf = io.BytesIO()
        annotate(img, receipt).save(buf, "JPEG", quality=85)
        receipt["annotated_jpeg_b64"] = base64.b64encode(buf.getvalue()).decode()
    return receipt


@app.post("/unload")
def unload():
    models.unload_all()
    return {"ok": True}


# ---------------- LIVE SCAN: job queue + Server-Sent Events (see LIVE-SCAN.md) ----------------
# One worker thread runs jobs one at a time (4 GB GPU, ~2 GB free RAM). Events are kept in memory
# for the last JOBS_KEEP jobs so a page can reconnect or download the full log.
import json as _json
import queue as _queue
import threading as _threading
import time as _time
import uuid as _uuid

from fastapi.responses import StreamingResponse

from raasta import scan as _scan, vlm as _vlm

JOBS: dict = {}
JOBS_KEEP = 30
_Q: _queue.Queue = _queue.Queue()


def _worker():
    while True:
        jid = _Q.get()
        job = JOBS.get(jid)
        if not job:
            continue
        t0 = _time.time()

        def emit(stage, data, _job=job, _t0=t0):
            _job["events"].append({"stage": stage, "t": round(_time.time() - _t0, 3), "data": data})

        job["state"] = "running"
        emit("start", {"queue_wait_s": round(t0 - job["created"], 2)})
        try:
            _scan.run(job["data"], job["form"], emit)
            job["state"] = "done"
        except Exception as e:  # noqa: BLE001
            emit("error", {"error": f"{type(e).__name__}: {e}"})
            job["state"] = "error"
        job["data"] = None
        emit("end", {"state": job["state"], "total_s": round(_time.time() - t0, 2)})


_threading.Thread(target=_worker, daemon=True, name="scan-worker").start()


@app.post("/scan")
async def scan(image: UploadFile = File(...), lat: str | None = Form(None), lon: str | None = Form(None),
               heading: str | None = Form(None), captured_at: str | None = Form(None),
               gps_error_m: str | None = Form(None), city: str | None = Form(None)):
    data = await image.read()
    if not data:
        raise HTTPException(400, "empty image")
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "image over 25 MB")
    while len(JOBS) >= JOBS_KEEP:
        old = next((k for k, j in JOBS.items() if j["state"] in ("done", "error")), None)
        if old is None:
            raise HTTPException(503, "scan queue full, try again in a minute")
        JOBS.pop(old)
    jid = _uuid.uuid4().hex[:12]
    ahead = sum(1 for j in JOBS.values() if j["state"] in ("queued", "running"))
    JOBS[jid] = {"state": "queued", "created": _time.time(), "data": data, "events": [],
                 "form": {"lat": lat, "lon": lon, "heading": heading, "captured_at": captured_at,
                          "gps_error_m": gps_error_m, "city": city, "filename": image.filename}}
    JOBS[jid]["events"].append({"stage": "queued", "t": 0.0, "data": {"job_id": jid, "ahead": ahead}})
    _Q.put(jid)
    return {"job_id": jid, "ahead": ahead, "events": f"/scan/{jid}/events"}


@app.get("/scan/{jid}/events")
async def scan_events(jid: str):
    import asyncio
    if jid not in JOBS:
        raise HTTPException(404, "unknown job")

    async def gen():
        i, idle = 0, 0
        yield "retry: 2000\n\n"
        while True:
            job = JOBS.get(jid)
            if job is None:
                return
            ev = job["events"]
            while i < len(ev):
                e = ev[i]
                i += 1
                yield f"event: {e['stage']}\ndata: {_json.dumps(e, default=str)}\n\n"
                if e["stage"] == "end":
                    return
            idle += 1
            if idle % 50 == 0:
                yield ": keep-alive\n\n"
            await asyncio.sleep(0.1)

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/scan/{jid}")
def scan_log(jid: str):
    job = JOBS.get(jid)
    if not job:
        raise HTTPException(404, "unknown job")
    return {"job_id": jid, "state": job["state"], "events": job["events"]}


@app.get("/scan-info")
def scan_info():
    return {"vlm": _vlm.status(), "licences": _scan.LICENCES,
            "queue": sum(1 for j in JOBS.values() if j["state"] in ("queued", "running"))}
