"""Run one LIVE SCAN against a running server and save the full event log (for the site's offline
recordings and for timing checks).
Usage: .venv/bin/python tools/record_scan.py IMAGE OUT.json [--api http://127.0.0.1:8010] [--label "..."]
       [--source-url URL --licence L] [--lat x --lon y --acc m]"""
import argparse
import json
import time

import requests

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("out")
ap.add_argument("--api", default="http://127.0.0.1:8010")
ap.add_argument("--label", default="")
ap.add_argument("--source-url", default="")
ap.add_argument("--licence", default="")
ap.add_argument("--lat")
ap.add_argument("--lon")
ap.add_argument("--acc")
a = ap.parse_args()

form = {k: v for k, v in {"lat": a.lat, "lon": a.lon, "gps_error_m": a.acc}.items() if v}
t0 = time.time()
r = requests.post(a.api + "/scan", files={"image": open(a.image, "rb")}, data=form, timeout=30)
r.raise_for_status()
jid = r.json()["job_id"]
events = []
with requests.get(f"{a.api}/scan/{jid}/events", stream=True, timeout=120) as s:
    buf = []
    for line in s.iter_lines(decode_unicode=True):
        if line is None:
            continue
        if line == "":
            data = "\n".join(x[5:].lstrip() for x in buf if x.startswith("data:"))
            buf = []
            if data:
                e = json.loads(data)
                e["client_t"] = round(time.time() - t0, 3)
                events.append(e)
                print(f"{e['client_t']:6.2f}s  {e['stage']}")
                if e["stage"] == "end":
                    break
            continue
        buf.append(line)
rec = {"schema": "raasta-scan-recording-v1", "recorded_at": time.strftime("%Y-%m-%d %H:%M:%S IST"),
       "label": a.label, "image_file": a.image.split("/")[-1], "source_url": a.source_url, "licence": a.licence,
       "client_total_s": round(time.time() - t0, 2), "events": events}
json.dump(rec, open(a.out, "w"), default=str)
print("saved", a.out, "total", rec["client_total_s"], "s")
