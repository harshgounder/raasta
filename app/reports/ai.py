"""AI first look, through the user's OpenCode Go subscription (OpenAI-compatible chat completions).

USER RULE: only these two models, nothing else:
  opencode-go/mimo-v2.6-flash      looks at the photo
  opencode-go/deepseek-v4.1-flash  reads everything and writes the structured first look + the reply

The key is read from env OPENCODE_GO_API_KEY, else from ~/.config/opencode/opencode.json (provider "opencode-go").
It is never printed, logged, stored or returned. If the call fails, a rules fallback fills the same fields and the
UI says plainly that the AI did not answer.
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import time

import httpx

import lookups as L

BASE_URL = os.environ.get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1").rstrip("/")
VISION_MODEL = "mimo-v2.6-flash"
TEXT_MODEL = "deepseek-v4.1-flash"
ALLOWED = {VISION_MODEL, TEXT_MODEL}
UA = "raasta-reports/0.1"
TIMEOUT = float(os.environ.get("REPORTS_AI_TIMEOUT_S", "60"))
SEVERITY = {1: "minor", 2: "slows people down", 3: "unsafe for some", 4: "blocks some people", 5: "dangerous, blocks most"}
_last_error: dict = {}


def _key() -> str | None:
    k = os.environ.get("OPENCODE_GO_API_KEY")
    if k and k.strip():
        return k.strip()
    try:
        with open(os.path.expanduser("~/.config/opencode/opencode.json")) as f:
            return (json.load(f)["provider"]["opencode-go"]["options"]["apiKey"] or "").strip() or None
    except (OSError, KeyError, ValueError):
        return None


def info() -> dict:
    return {"base_url": BASE_URL, "vision_model": f"opencode-go/{VISION_MODEL}", "text_model": f"opencode-go/{TEXT_MODEL}",
            "key_present": bool(_key()), "last_error": _last_error.get("msg")}


def _chat(model: str, messages: list, session: str, max_tokens: int = 900, json_mode: bool = False) -> tuple[str, float]:
    assert model in ALLOWED, "model not allowed by the user rule"
    key = _key()
    if not key:
        raise RuntimeError("no OpenCode Go key found")
    body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.2}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    t0 = time.time()
    r = httpx.post(f"{BASE_URL}/chat/completions", json=body, timeout=TIMEOUT,
                   headers={"Authorization": f"Bearer {key}", "User-Agent": UA, "x-opencode-session": session})
    dt = time.time() - t0
    if r.status_code != 200:
        msg = r.text[:200]
        try:
            msg = r.json().get("error", {}).get("message", msg)
        except ValueError:
            pass
        raise RuntimeError(f"HTTP {r.status_code}: {msg}")
    d = r.json()
    return (d["choices"][0]["message"].get("content") or "").strip(), dt


def _img_data_url(path: str) -> str:
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((768, 768))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _parse_json(s: str) -> dict:
    s = s.strip()
    m = re.search(r"\{.*\}", s, re.S)
    return json.loads(m.group(0) if m else s)


# ------------------------------------------------------------------ the look

def first_look(rep: dict, analyze: dict, near: list, known: list, photo: str | None) -> dict:
    t0 = time.time()
    f = rep["fields"]
    session = f"raasta-report-{rep['id']}"
    ft = L.form_type(rep["type"]) or {}
    out = {"models_used": [], "timings": {}}
    vision = None
    if photo:
        try:
            txt, dt = _chat(VISION_MODEL, [{"role": "user", "content": [
                {"type": "text", "text": (
                    "You look at a photo a person in India sent to report a problem on a footpath or street. "
                    f"They say it is: '{ft.get('en', rep['type'])}'. In at most 60 words, plain English: what barrier "
                    "do you see, where in the frame, roughly how big (kerb height, how much width is left), and does "
                    "the photo agree with what they said (yes / no / cannot tell)? No guessing beyond the photo.")},
                {"type": "image_url", "image_url": {"url": _img_data_url(photo)}}]}], session, max_tokens=2500)
            vision = txt
            out["models_used"].append(f"opencode-go/{VISION_MODEL}")
            out["timings"]["vision_s"] = round(dt, 2)
        except Exception as e:  # noqa: BLE001
            out["vision_error"] = _clean_err(e)
    out["photo_says"] = vision

    types = L.all_form_types()
    auth_opts = L.authority_options(rep.get("city"))
    prompt = {
        "task": "First look at a footpath barrier report for RAASTA, an accessible-routing app in India. Answer as JSON only.",
        "report": {"category": rep["category"], "type": rep["type"], "type_label": ft.get("en"), "body_or_aid": rep.get("body"),
                   "side_of_road": f.get("side"), "details": L.detail_hints(rep["category"], f.get("details"))[1], "since": f.get("since"), "hurt": f.get("hurt"), "words": f.get("words"),
                   "when": f.get("observed_at"), "location": {"lat": rep["lat"], "lon": rep["lon"], "accuracy_m": rep.get("accuracy_m")},
                   "mapped_area": rep.get("city")},
        "photo_model_says": vision or ("no photo" if not photo else "photo model failed"),
        "detector": {"ok": analyze.get("ok"), "detections": analyze.get("detections"), "note": "two-detector agreement; ACCEPT = both agree"} if analyze.get("ok") else None,
        "other_reports_within_30m": near[:8],
        "known_barriers_within_30m_on_our_map": known[:8],
        "allowed_types": [{"id": t["id"], "category": t["category"], "en": t["en"]} for t in types],
        "authority_options": [{"office": a["office"], "name": a["name"]} for a in auth_opts],
        "return_json_with_keys": {
            "type": "one id from allowed_types (keep the person's choice unless the photo or words clearly say otherwise)",
            "severity": "integer 1-5 (1 minor, 3 unsafe for some, 5 dangerous or blocks most people)",
            "duplicate_of": "id of an other_reports_within_30m entry that is the same problem, else null",
            "duplicate_reason": "short, or null",
            "already_on_map": "id from known_barriers_within_30m_on_our_map that is the same thing, else null",
            "authority": "one office id from authority_options",
            "reply_en": "2-3 short plain sentences to the person: what we understood, what happens next. Warm, no promises we cannot keep. Do not say 'safe'.",
            "reply_hi": "the same reply in simple spoken Hindi (Devanagari)",
            "confidence": "0..1, how sure you are of type and severity",
            "why": "one line"}}
    try:
        txt, dt = _chat(TEXT_MODEL, [
            {"role": "system", "content": "You triage street accessibility reports. Output one JSON object, nothing else."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)}], session, max_tokens=900, json_mode=True)
        d = _parse_json(txt)
        out["models_used"].append(f"opencode-go/{TEXT_MODEL}")
        out["timings"]["text_s"] = round(dt, 2)
        out.update(_normalise(d, rep, near, known, ft))
        out["engine"] = "opencode-go AI"
        out["engine_ok"] = True
        _last_error.pop("msg", None)
    except Exception as e:  # noqa: BLE001
        err = _clean_err(e)
        _last_error["msg"] = err
        out.update(rules(rep, near, known, ft, analyze))
        out["engine"] = "rules fallback (the AI did not answer)"
        out["engine_ok"] = False
        out["ai_error"] = err
    out["timings"]["total_s"] = round(time.time() - t0, 2)
    return out


def _clean_err(e: Exception) -> str:
    """public error text: our own 'HTTP <code>: <provider message>' lines only; anything else is just the type name,
    because library exception text can quote request headers (and so the key)."""
    msg = str(e)
    if isinstance(e, RuntimeError) and (msg.startswith("HTTP ") or msg.startswith("no OpenCode")):
        k = _key()
        return (msg.replace(k, "<key>") if k else msg)[:240]
    return type(e).__name__


def _common(rep, type_id, severity, near, known, dup, already, office_id, confidence) -> dict:
    ft = L.form_type(type_id) or L.form_type(rep["type"]) or {}
    el = ft.get("element")
    e = L.elements().get(el or "") or {}
    opts = {a["office"]: a for a in L.authority_options(rep.get("city"))}
    auth = opts.get(office_id) or L.authority_for(rep.get("city"), ft.get("category"), ft.get("id"))
    sev = max(1, min(5, int(severity or 3)))
    return {"type": ft.get("id", type_id), "type_label": {"en": ft.get("en"), "hi": ft.get("hi")},
            "category": ft.get("category"), "category_label": {"en": ft.get("category_en"), "hi": ft.get("category_hi")},
            "element": el, "element_name": e.get("name"), "element_path": [e.get("category"), e.get("subcategory")] if e else None,
            "route_type": ft.get("route_type"), "severity": sev, "severity_label": SEVERITY[sev],
            "affects": L.impact_for(el), "duplicate_of": dup if dup in {n["id"] for n in near} else None,
            "already_on_map": already if already in {k["id"] for k in known} else None,
            "nearby_reports": len(near), "authority": auth,
            "confidence": round(max(0.0, min(1.0, float(confidence if confidence is not None else 0.5))), 2)}


def _normalise(d: dict, rep, near, known, ft) -> dict:
    tid = d.get("type") if L.form_type(d.get("type")) else rep["type"]
    out = _common(rep, tid, d.get("severity"), near, known, d.get("duplicate_of"), d.get("already_on_map"),
                  d.get("authority"), d.get("confidence"))
    out["reply"] = {"en": str(d.get("reply_en") or "")[:600], "hi": str(d.get("reply_hi") or "")[:600]}
    out["why"] = str(d.get("why") or "")[:300]
    out["duplicate_reason"] = d.get("duplicate_reason")
    out["changed_type"] = tid != rep["type"]
    return out


def rules(rep, near, known, ft, analyze) -> dict:
    """deterministic stand-in with the same fields, used only when the AI call fails."""
    f = rep["fields"]
    base = {"level": 4, "surface": 3, "no_path": 4, "blocked": 3, "crossing": 4, "safety": 3, "other": 2}
    hints, _ = L.detail_hints(rep["category"], f.get("details"))
    sev = base.get(rep["category"], 3) + (1 if f.get("hurt") in ("fell", "hurt") else 0) \
        + (1 if hints.get("clear_width_cm", 999) < 70 or hints.get("height_cm", 0) >= 40 else 0)
    same = [n for n in near if n["type"] == rep["type"]]
    dup = same[0]["id"] if same else None
    rt = ft.get("route_type")
    already = next((k["id"] for k in known if rt and k["type"] == rt), None)
    det_agree = None
    if analyze.get("ok") and rt:
        det_agree = any(d.get("class_family") == rt and d.get("status") == "ACCEPT" for d in analyze.get("detections") or [])
    conf = 0.35 + (0.25 if det_agree else 0) + (0.1 if dup or already else 0)
    out = _common(rep, rep["type"], sev, near, known, dup, already, None, conf)
    a = out["authority"]
    lbl_en, lbl_hi = ft.get("en", rep["type"]), ft.get("hi", rep["type"])
    dup_en = " Someone reported the same thing here before; your report adds weight to it." if dup else ""
    dup_hi = " यहाँ पहले भी किसी ने यही बताया है; आपकी शिकायत से उसे और वज़न मिलता है." if dup else ""
    out["reply"] = {
        "en": f"We got your report: {lbl_en}.{dup_en} Your own routes avoid it from now. A person on our team checks it next, then it goes to {a['name']}.",
        "hi": f"आपकी शिकायत मिल गई: {lbl_hi}.{dup_hi} आपके अपने रास्ते अब से इससे बचेंगे. अगला कदम: हमारी टीम का एक व्यक्ति इसे जाँचेगा, फिर यह {a.get('name_hi') or a['name']} को जाएगी."}
    out["why"] = "rules: category default severity" + (", +1 because the person fell or got hurt" if f.get("hurt") in ("fell", "hurt") else "") + \
        (", +1 for no width left or a high step" if hints.get("clear_width_cm", 999) < 70 or hints.get("height_cm", 0) >= 40 else "") + \
        (f", detector {'agrees' if det_agree else 'does not confirm'}" if det_agree is not None else "")
    out["changed_type"] = False
    return out
