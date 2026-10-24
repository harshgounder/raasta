"""Scene describer / judge VLM for LIVE SCAN.

Given the photo with the detector boxes drawn and numbered, a vision-language model returns JSON:
scene type, every movement-relevant element (from ELEMENTS) with its place in the image, a verdict on
each numbered detector box, rough measurements with ranges, and light / weather / surface.

Provider: opencode-go ONLY (user order 2026-10-25 ~00:05 IST), OpenAI-compatible at
https://opencode.ai/zen/go/v1, header x-opencode-session required. Vision: mimo-v2.6-flash.
Text-only reasoner: deepseek-v4.1-flash (reason()). The key is read on every call from
~/.config/opencode/opencode.json (or env OPENCODE_GO_API_KEY), so a fixed key works without a restart.
On 2026-10-24/25 every call (text and image) answered 401 "Upstream request failed: Invalid credential"
(see LIVE-SCAN.md). A 401 skips the provider for RETRY_DEAD_S, then it is tried again.
archive/vlm.v1-nvidia-chain.py has the earlier NVIDIA chain (not used: user order).
Keys are never printed, logged or written into an event or receipt.
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import threading
import time
import uuid

import requests
from PIL import ImageDraw


# element vocabulary: ids from research/claude/sc02-FACTOR-UNIVERSE.md (L1-L3, L6, L7) plus an indoor
# extension (marked "in") that is NOT in that file: the scan accepts rooms and hallways too.
ELEMENTS: dict[str, tuple[str, str]] = {
    # id: (name, factor id or "in")
    "no_footpath": ("no footpath on this side", "1.01"),
    "kerb_high": ("high kerb / footpath edge", "1.02"),
    "kerb_ramp": ("kerb ramp present", "1.03"),
    "kerb_no_ramp": ("kerb with no ramp", "1.03"),
    "ramp_steep": ("steep ramp", "1.04"),
    "narrow_path": ("narrow clear walking width", "1.08"),
    "slope": ("sloping path", "1.09"),
    "height_changes": ("footpath height keeps changing", "1.11"),
    "path_ends": ("footpath ends abruptly", "1.14"),
    "gaps_cracks": ("joints, cracks, gaps", "1.15"),
    "drain_grating": ("drain grating", "1.16"),
    "steps": ("steps / stairs", "1.17"),
    "handrail_present": ("handrail present", "1.19"),
    "handrail_missing": ("handrail missing at steps or ramp", "1.19"),
    "bollards": ("bollards", "1.25"),
    "guardrail": ("continuous railing with no gap", "1.26"),
    "low_overhead": ("low overhead object (sign, awning, branch)", "1.27"),
    "protruding": ("object protruding into path", "1.28"),
    "tactile_paving": ("tactile paving", "1.29"),
    "tree_pit": ("open tree pit", "1.30"),
    "utility_cover": ("utility / manhole cover", "1.31"),
    "pothole": ("pothole", "2.01"),
    "broken_paving": ("broken or missing paving", "2.03"),
    "open_drain": ("open drain / missing slab", "2.06"),
    "open_manhole": ("open manhole", "2.08"),
    "trench_dug": ("dug-up path / trench", "2.11"),
    "debris": ("soil, sand or debris heap", "2.13"),
    "surface": ("surface material", "2.17"),
    "slippery": ("slippery surface (wet, polished, tiles)", "2.18"),
    "zebra_faded": ("faded zebra crossing", "2.20"),
    "garbage": ("garbage on path", "2.28"),
    "pole": ("pole in path", "3.01"),
    "transformer_box": ("transformer / electric box", "3.02"),
    "tree_trunk": ("tree trunk in path", "3.04"),
    "shop_platform": ("shop platform / otla on path", "3.08"),
    "seating_spill": ("seating spill", "3.10"),
    "vendor_cart": ("vendor cart / stall", "3.11"),
    "parked_two_wheeler": ("two-wheeler parked on path", "3.13"),
    "parked_car": ("car parked on path", "3.14"),
    "construction_material": ("construction material", "3.17"),
    "dangling_cables": ("dangling cables", "3.21"),
    "barricade": ("barricade", "3.22"),
    "puddle": ("puddle / waterlogging", "3.25"),
    "animals": ("cattle or dogs", "3.26"),
    "crowd": ("crowd / queue", "3.29"),
    "moving_traffic": ("moving vehicles beside or on the path", "4.x"),
    "dark": ("poor lighting", "7.x"),
    "glare": ("glare", "7.06"),
    "low_contrast_edge": ("low-contrast step or kerb edge", "7.08"),
    # indoor extension
    "threshold": ("door threshold / raised sill", "in"),
    "door_narrow": ("narrow door", "in"),
    "door_heavy": ("heavy or self-closing door", "in"),
    "door": ("door / doorway", "in"),
    "indoor_ramp": ("indoor ramp", "in"),
    "lift": ("lift / elevator", "in"),
    "clutter": ("clutter or furniture in the way", "in"),
    "rug_mat": ("loose rug or mat", "in"),
    "wet_floor": ("wet floor", "in"),
    "turning_space": ("tight turning space", "in"),
    "signage": ("signage / wayfinding", "in"),
}

SCENES = ["street", "footpath", "market", "room", "hallway", "staircase", "entrance", "other"]

PROMPT = """You audit one photo for how easily people can MOVE through the place (wheelchair users, blind people, elderly, prams, children). It may be a street, footpath, market, room, hallway, staircase or entrance.
Numbered boxes on the photo come from two object detectors:
{boxes}
Reply with ONE compact JSON object, no prose, no markdown, at most 8 elements and 3 measurements:
{{"scene":"<one of {scenes}>","indoor":true|false,"summary":"<max 20 words>",
"el":[["<element id>","<left|centre|right> <near|middle|far>","<high|medium|low>","<max 8 words>"]],
"bx":[[<box number>,"<confirm|deny|unsure>","<what is really there, max 4 words>"]],
"ms":[["<what>",<low>,<high>,"<cm|m|count|%>","<compared against, max 6 words>"]],
"light":"<day|dusk|night|indoor-bright|indoor-dim>","weather":"<dry|wet|rain|fog|indoor>","surface":"<max 5 words>"}}
Element ids allowed: {ids}
Only list what you can see. Give every numbered box a verdict. Measurements are ranges."""


def _opencode_cfg():
    k = os.environ.get("OPENCODE_GO_API_KEY")
    url = "https://opencode.ai/zen/go/v1"
    try:
        c = json.load(open(os.path.expanduser("~/.config/opencode/opencode.json")))
        o = c["provider"]["opencode-go"]["options"]
        url = o.get("baseURL", url)
        k = k or o.get("apiKey")
    except Exception:  # noqa: BLE001
        pass
    return url.rstrip("/") + "/chat/completions", k


# USER ORDER 2026-10-25 ~00:05 IST: opencode-go ONLY, two models. mimo-v2.6-flash = vision describer,
# deepseek-v4.1-flash = text-only reasoner. No other providers or models by default.
VISION_MODEL = os.environ.get("SCAN_VISION_MODEL", "mimo-v2.6-flash")
TEXT_MODEL = os.environ.get("SCAN_TEXT_MODEL", "deepseek-v4.1-flash")
TIMEOUT_S = float(os.environ.get("SCAN_VLM_TIMEOUT_S", 45))
RETRY_DEAD_S = 60.0        # a 401 provider is re-tried after this, so a fixed key works without a restart
_DEAD: dict = {}           # "opencode-go" or model -> (reason, until_ts)
_SESSION = "raasta-scan-" + uuid.uuid4().hex[:12]
_LOCK = threading.Lock()


def _is_dead(k) -> str | None:
    v = _DEAD.get(k)
    if v and time.time() < v[1]:
        return v[0]
    return None


def status() -> dict:
    url, key = _opencode_cfg()
    return {"provider": "opencode-go", "base_url": url.rsplit("/chat/completions", 1)[0], "key_present": bool(key),
            "vision_model": "opencode-go/" + VISION_MODEL, "text_model": "opencode-go/" + TEXT_MODEL,
            "chain": ["opencode-go/" + VISION_MODEL],
            "dead": {k: v[0] for k, v in _DEAD.items() if time.time() < v[1]}}


def _call(model: str, messages: list, budget_s: float, max_tokens: int, json_mode: bool = False) -> dict:
    """One opencode-go chat call. Returns {ok, seconds, text | error}. Never returns or logs the key."""
    url, key = _opencode_cfg()
    if not key:
        return {"ok": False, "seconds": 0, "error": "no opencode-go key (opencode.json or OPENCODE_GO_API_KEY)"}
    why = _is_dead("opencode-go") or _is_dead(model)
    if why:
        return {"ok": False, "seconds": 0, "error": f"skipped: {why} (retry in <= {int(RETRY_DEAD_S)} s)"}
    t = time.time()
    try:
        body = {"model": model, "max_tokens": max_tokens, "temperature": 0.1, "messages": messages}
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        r = requests.post(url, timeout=(4, max(2.0, min(TIMEOUT_S, budget_s))),
                          json=body,
                          headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                                   "x-opencode-session": _SESSION})
        sec = round(time.time() - t, 2)
        if r.status_code != 200:
            why = f"HTTP {r.status_code}"
            try:
                why += ": " + str(r.json().get("error", {}).get("message", ""))[:80]
            except Exception:  # noqa: BLE001
                pass
            why = why.replace(key, "<key>")
            with _LOCK:
                _DEAD["opencode-go" if r.status_code in (401, 403) else model] = (why, time.time() + RETRY_DEAD_S)
            return {"ok": False, "seconds": sec, "error": why}
        msg = r.json()["choices"][0]["message"]
        return {"ok": True, "seconds": sec, "text": msg.get("content") or msg.get("reasoning_content") or ""}
    except requests.RequestException as e:
        return {"ok": False, "seconds": round(time.time() - t, 2), "error": type(e).__name__}


def marked_image(img, boxes: list[dict], max_side=768):
    """Copy of the photo, downscaled, with numbered boxes (A solid, B dashed look via double line)."""
    im = img.copy()
    im.thumbnail((max_side, max_side))
    s = im.size[0] / img.size[0]
    d = ImageDraw.Draw(im)
    for b in boxes:
        x1, y1, x2, y2 = [v * s for v in b["box"]]
        col = (255, 220, 0) if b["src"] == "A" else (0, 220, 255)
        d.rectangle([x1, y1, x2, y2], outline=col, width=3)
        d.rectangle([x1, max(0, y1 - 16), x1 + 22, max(16, y1)], fill=(0, 0, 0))
        d.text((x1 + 4, max(0, y1 - 15)), str(b["n"]), fill=col)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode(), im.size


def _parse(txt: str) -> dict | None:
    txt = re.sub(r"<think>.*?</think>", "", txt or "", flags=re.S)
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return None
    raw = m.group(0)
    for attempt in (raw, re.sub(r",\s*([}\]])", r"\1", raw)):
        try:
            return json.loads(attempt)
        except json.JSONDecodeError:
            continue
    return None


def _clean(j: dict, nboxes: int) -> dict:
    j = dict(j)
    if "el" in j:
        j["elements"] = [{"id": e[0], "where": e[1] if len(e) > 1 else "", "confidence": e[2] if len(e) > 2 else "low",
                          "note": e[3] if len(e) > 3 else ""} for e in j.get("el") or [] if isinstance(e, list) and e]
    if "bx" in j:
        j["boxes"] = [{"n": b[0], "verdict": b[1] if len(b) > 1 else "unsure", "what": b[2] if len(b) > 2 else ""}
                      for b in j.get("bx") or [] if isinstance(b, list) and b]
    if "ms" in j:
        j["measurements"] = [{"what": m[0], "low": m[1], "high": m[2], "unit": m[3] if len(m) > 3 else "",
                              "how": m[4] if len(m) > 4 else ""} for m in j.get("ms") or [] if isinstance(m, list) and len(m) >= 3]
    els = []
    for e in j.get("elements") or []:
        if not isinstance(e, dict):
            continue
        eid = str(e.get("id", "")).strip()
        known = eid in ELEMENTS
        box = e.get("box")
        if not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box)):
            box = None
        else:
            box = [max(0, min(1000, float(v))) for v in box]
            if box[2] <= box[0] or box[3] <= box[1]:
                box = None
        conf = str(e.get("confidence", "low")).lower()
        where = str(e.get("where", ""))
        if conf in ("near", "middle", "far"):          # model split "centre near" across two fields
            where, conf = f"{where} {conf}", "medium"
        e = {**e, "where": where, "confidence": conf if conf in ("high", "medium", "low") else "low"}
        els.append({"id": eid if known else "other", "raw_id": None if known else eid,
                    "name": ELEMENTS[eid][0] if known else eid.replace("_", " "),
                    "factor": ELEMENTS[eid][1] if known else None,
                    "where": str(e.get("where", ""))[:30], "box_1000": box,
                    "confidence": str(e.get("confidence", "low")).lower()[:6], "note": str(e.get("note", ""))[:90]})
    bx = []
    for b in j.get("boxes") or []:
        if isinstance(b, dict) and isinstance(b.get("n"), (int, float)) and 1 <= int(b["n"]) <= nboxes:
            v = str(b.get("verdict", "unsure")).lower()
            bx.append({"n": int(b["n"]), "verdict": v if v in ("confirm", "deny", "unsure") else "unsure",
                       "what": str(b.get("what", ""))[:50]})
    ms = []
    for m in j.get("measurements") or []:
        if isinstance(m, dict) and isinstance(m.get("low"), (int, float)) and isinstance(m.get("high"), (int, float)):
            ms.append({"what": str(m.get("what", ""))[:40], "low": m["low"], "high": m["high"],
                       "unit": str(m.get("unit", ""))[:6], "how": str(m.get("how", ""))[:80],
                       "kind": "VLM estimate, not measured"})
    scene = str(j.get("scene", "other")).lower()
    return {"scene": scene if scene in SCENES else "other", "indoor": bool(j.get("indoor")),
            "summary": str(j.get("summary", ""))[:200], "elements": els, "boxes": bx, "measurements": ms,
            "light": str(j.get("light", ""))[:20], "weather": str(j.get("weather", ""))[:20],
            "surface": str(j.get("surface", ""))[:80]}


def describe(img, boxes: list[dict], budget_s: float = 30.0, on_try=None) -> dict:
    """boxes: [{n, src: 'A'|'B', label, box(px)}]. Tries the chain inside the time budget."""
    t0 = time.time()
    b64, _ = marked_image(img, boxes)
    W, H = img.size
    lines = "\n".join(f"  {b['n']}: detector {b['src']} says '{b['label']}' at "
                      f"[{int(b['box'][0] / W * 1000)},{int(b['box'][1] / H * 1000)},{int(b['box'][2] / W * 1000)},{int(b['box'][3] / H * 1000)}]"
                      for b in boxes) or "  (no boxes: the detectors found nothing above threshold)"
    prompt = PROMPT.format(boxes=lines, scenes=SCENES, ids=", ".join(ELEMENTS))
    r = _call(VISION_MODEL, [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}}]}], budget_s, 3000)
    base = {"provider": "opencode-go", "model": VISION_MODEL, "seconds": r["seconds"],
            "tries": [{"provider": "opencode-go", "model": VISION_MODEL, "ok": r["ok"], "seconds": r["seconds"],
                       **({"error": r["error"]} if not r["ok"] else {})}]}
    if not r["ok"]:
        return {"ok": False, **base, "error": r["error"]}
    j = _parse(r["text"])
    if j is None:
        return {"ok": False, **base, "error": "reply was not JSON", "raw": r["text"][:300]}
    return {"ok": True, **base, **_clean(j, len(boxes))}


REASON_PROMPT = """You turn the output of a photo-scanning pipeline into a plain answer for a person who needs to move through this place.
Inputs (JSON): detector decisions (ACCEPT = two detectors agree, ABSTAIN = only one, REJECT = dropped), the vision model's description (may be missing), and the body-impact table (may say 'loading').
{inputs}
Reply with ONE JSON object only:
{{"elements":[["<element id from the inputs>","<ACCEPT|ABSTAIN|VLM_ONLY>","<why it matters for movement, max 14 words>"]],
"bodies":[["<body code e.g. MW, BL, EL, PR>","<one sentence, max 20 words, what this place means for that body, ONLY from the inputs>"]],
"answer":"<3 sentences max, plain language: what is here, what is certain, what is not known>"}}
Rules: never call a place safe; ABSTAIN and VLM_ONLY items are 'possible', not certain; do not invent numbers; if the body table says loading, say impacts are not computed yet."""


def reason(decisions: list, vlm_out: dict, impact: dict, budget_s: float = 25.0) -> dict:
    """Text-only step on deepseek-v4.1-flash: element list, per-body explanations, final plain answer."""
    inputs = json.dumps({
        "detections": [{k: d.get(k) for k in ("class", "class_family", "status", "why")} for d in decisions if d.get("status") != "REJECT"][:14],
        "vision": {k: vlm_out.get(k) for k in ("scene", "indoor", "summary", "elements", "measurements", "light", "weather", "surface")} if vlm_out.get("ok") else {"missing": vlm_out.get("error")},
        "impact": {"status": impact.get("status"), "rows": [{k: r.get(k) for k in ("id", "status", "bodies")} for r in impact.get("rows", [])]},
    }, default=str)[:6000]
    r = _call(TEXT_MODEL, [
        {"role": "system", "content": "You are a JSON API. Return exactly one valid JSON object and nothing else. No reasoning, no markdown, no explanation."},
        {"role": "user", "content": REASON_PROMPT.format(inputs=inputs)}], budget_s, 2000, json_mode=True)
    base = {"provider": "opencode-go", "model": TEXT_MODEL, "seconds": r["seconds"]}
    if not r["ok"]:
        return {"ok": False, **base, "error": r["error"]}
    j = _parse(r["text"])
    if j is None:
        return {"ok": False, **base, "error": "reply was not JSON", "raw": r["text"][:300]}
    els = [{"id": str(e[0])[:40], "status": str(e[1])[:10] if len(e) > 1 else "", "why": str(e[2])[:120] if len(e) > 2 else ""}
           for e in j.get("elements") or [] if isinstance(e, list) and e]
    bodies = [{"body": str(b[0])[:4], "text": str(b[1])[:160]} for b in j.get("bodies") or [] if isinstance(b, list) and len(b) >= 2]
    return {"ok": True, **base, "elements": els, "bodies": bodies, "answer": str(j.get("answer", ""))[:600]}
