"""Probe which opencode-go models accept image input. Reads the key from ~/.config/opencode/opencode.json
in memory only; never prints it. Usage: .venv/bin/python tools/probe_opencode_vlm.py IMAGE [model ...]
Writes logs/vlm-probe.json."""
import base64, io, json, os, sys, time, concurrent.futures as cf
import requests
from PIL import Image

CFG = json.load(open(os.path.expanduser("~/.config/opencode/opencode.json")))
P = CFG["provider"]["opencode-go"]["options"]
URL = P["baseURL"].rstrip("/") + "/chat/completions"
KEY = P["apiKey"]
import uuid
SESSION = "raasta-scan-" + uuid.uuid4().hex[:12]

MODELS = sys.argv[2:] or ["qwen3.8-max", "qwen3.7-plus", "qwen3.8-flash", "glm-5.3", "glm-5.3-flash", "kimi-k3",
                          "mimo-v2.6-pro", "mimo-v2.6-flash", "gemini-4-argon-contributor", "gpt-5.6-luna",
                          "gpt-6-luna", "grok-4.7", "claude-haiku-5-5", "minimax-m3", "step-5-preview",
                          "muse-spark-1.3-contributor", "hy4-preview", "deepseek-v4-flash"]

img = Image.open(sys.argv[1]).convert("RGB")
img.thumbnail((640, 640))
buf = io.BytesIO(); img.save(buf, "JPEG", quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()
Q = ("Look at the photo. Reply JSON only: {\"scene\": \"street|footpath|market|room|hallway|staircase|entrance|other\", "
     "\"things\": [up to 5 short names of things that affect walking or wheelchair movement], \"colour_of_sky_or_ceiling\": \"...\"}")


def one(m):
    body = {"model": m, "max_tokens": 400, "temperature": 0,
            "messages": [{"role": "user", "content": [{"type": "text", "text": Q},
                                                       {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}}]}]}
    t = time.time()
    try:
        r = requests.post(URL, json=body, timeout=60, headers={"Authorization": "Bearer " + KEY, "x-opencode-session": SESSION})
        dt = round(time.time() - t, 2)
        if r.status_code != 200:
            return {"model": m, "ok": False, "status": r.status_code, "s": dt, "err": r.text[:200].replace(KEY, "<k>")}
        j = r.json()
        txt = (j["choices"][0]["message"].get("content") or "")
        return {"model": m, "ok": True, "s": dt, "reply": txt[:400], "usage": j.get("usage")}
    except Exception as e:  # noqa: BLE001
        return {"model": m, "ok": False, "s": round(time.time() - t, 2), "err": type(e).__name__ + ": " + str(e)[:150]}


with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(one, MODELS))
os.makedirs("logs", exist_ok=True)
json.dump({"image": sys.argv[1], "at": time.strftime("%Y-%m-%d %H:%M:%S"), "results": res},
          open("logs/vlm-probe.json", "w"), indent=1)
for r in res:
    print(json.dumps(r)[:600])
