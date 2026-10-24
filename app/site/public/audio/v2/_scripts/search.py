import json, sys, time, urllib.parse, urllib.request
Q = {
 "street": ["india street morning", "india street ambience", "delhi street", "mumbai street ambience", "varanasi street", "indian city street"],
 "market": ["india market", "indian bazaar", "bazaar ambience", "market india crowd"],
 "wind": ["wind high", "wind gentle loop", "wind rooftop", "wind mountain soft"],
 "bell": ["temple bell", "hindu temple bell", "ghanta bell"],
 "paws": ["cat footsteps", "cat paws", "cat walking", "cat jump"],
 "purr": ["cat purr", "cat purring"],
 "myna": ["myna", "common myna", "mynah bird"],
 "wings": ["wings flapping", "bird wings flap", "pigeon flying away", "bird take off"],
 "scooter": ["scooter pass by", "moped passing", "motorbike pass by", "motorcycle passing"],
 "horn": ["rickshaw horn", "scooter horn", "india horn", "motorbike horn"],
 "walker": ["walker frame", "zimmer frame", "walking frame", "rollator"],
 "cane": ["walking cane", "walking stick", "footsteps pavement", "child footsteps"],
 "wheelchair": ["wheelchair", "wheelchair rolling"],
 "phone": ["phone tap", "touchscreen tap", "smartphone tap", "screen tap"],
 "resolve": ["singing bowl", "tanpura", "bell drone", "harmonium drone", "tibetan bowl"],
}
out = {}
only = sys.argv[1:] or list(Q)
for k in only:
    rows = {}
    for q in Q[k]:
        url = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode({"q": q, "license": "cc0,by", "page_size": 20})
        for attempt in range(3):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "raasta-sound/1.0"}), timeout=30))
                break
            except Exception as e:
                print("ERR", q, e, file=sys.stderr); time.sleep(4); d = {"results": []}
        for r in d.get("results", []):
            rows[r["id"]] = {k2: r.get(k2) for k2 in ("id", "source", "license", "license_version", "duration", "title", "creator", "url", "foreign_landing_url", "tags", "filetype", "bit_rate", "sample_rate")}
            rows[r["id"]]["tags"] = [t["name"] for t in (r.get("tags") or [])][:12]
            rows[r["id"]]["q"] = q
        time.sleep(1.2)
    out[k] = list(rows.values())
    print(k, len(rows), file=sys.stderr)
prev = {}
try:
    prev = json.load(open("cands.json"))
except Exception:
    pass
prev.update(out)
json.dump(prev, open("cands.json", "w"), indent=1)
