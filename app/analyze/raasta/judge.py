"""Optional VLM judge for single-model (ABSTAIN) detections. Answers only
visible / not_visible / cannot_determine as short JSON. Keys are read from the environment at
runtime (OPENROUTER_API_KEY, NVIDIA_API_KEY); if absent there, the two named variables are read from
~/.hermes/.env into memory. Keys are never logged, printed or written to a receipt."""
from __future__ import annotations

import base64
import concurrent.futures as cf
import io
import json
import os
import re
import time

import requests

from . import config

_KEYS: dict | None = None
_POOL = cf.ThreadPoolExecutor(max_workers=2)
_DEAD: set = set()
_STRIKES: dict = {}


def _strike(key, n=2):
    _STRIKES[key] = _STRIKES.get(key, 0) + 1
    if _STRIKES[key] >= n:
        _DEAD.add(key)


# NVIDIA first: on 2026-10-24 it was the only provider that answered (OpenRouter free = 429, paid = 403)
PROVIDERS = [
    ("nvidia", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1/chat/completions", config.NVIDIA_MODELS),
    ("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions",
     config.OPENROUTER_MODELS),
]


def _keys() -> dict:
    global _KEYS
    if _KEYS is not None:
        return _KEYS
    k = {}
    for _, name, _, _ in PROVIDERS:
        if os.environ.get(name):
            k[name] = os.environ[name]
    env = os.path.expanduser("~/.hermes/.env")
    if len(k) < len(PROVIDERS) and os.path.exists(env):
        try:
            for line in open(env, encoding="utf-8", errors="ignore"):
                m = re.match(r"\s*(?:export\s+)?([A-Z0-9_]+)\s*=\s*(.*)$", line)
                if m and m.group(1) in {p[1] for p in PROVIDERS} and m.group(1) not in k:
                    v = m.group(2).strip().strip('"').strip("'")
                    if v:
                        k[m.group(1)] = v
        except OSError:
            pass
    _KEYS = k
    return k


def available() -> tuple[bool, str]:
    if not config.JUDGE_ENABLED:
        return False, "judge skipped: disabled (ANALYZE_JUDGE=0)"
    ok, why = breaker_state()
    if not ok:
        return False, why
    ks = _keys()
    have = [f"{p[0]}:{m}" for p in PROVIDERS if p[1] in ks and p[0] not in _DEAD
            for m in p[3] if (p[0], m) not in _DEAD]
    if not have:
        return False, "judge skipped: no live provider (no key, or every provider failed earlier this run)"
    return True, "providers: " + ", ".join(have)


def _crop_b64(img, box, pad=0.35) -> str:
    W, H = img.size
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    c = img.crop((max(0, int(x1 - pad * bw)), max(0, int(y1 - pad * bh)),
                  min(W, int(x2 + pad * bw)), min(H, int(y2 + pad * bh))))
    c.thumbnail((512, 512))
    buf = io.BytesIO()
    c.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


PROMPT = ("You check one street-photo crop for a pedestrian accessibility audit in India. "
          "Question: is there a '{label}' in this crop (on or blocking the footpath)? "
          "Answer with JSON only, no prose: {{\"answer\": \"visible\" | \"not_visible\" | \"cannot_determine\", "
          "\"reason\": \"<10 words>\"}}")


_BREAKER = {"fails_in_row": 0, "open_until": 0.0, "last_error": None}


def breaker_state() -> tuple[bool, str]:
    """Circuit breaker: after JUDGE_BREAKER_FAILS failed calls in a row the judge is skipped for
    JUDGE_COOLDOWN_S seconds (process-wide), so a dead provider never slows a receipt again."""
    if time.time() < _BREAKER["open_until"]:
        left = int(_BREAKER["open_until"] - time.time())
        return False, (f"judge skipped: {_BREAKER['fails_in_row']} failed calls in a row "
                       f"(last: {_BREAKER['last_error']}); retry in {left} s")
    return True, "closed"


def ask(img, box, label: str, budget_s: float | None = None) -> dict:
    """ONE provider attempt (first live provider/model), timeout = min(JUDGE_TIMEOUT_S, budget left)."""
    ok, why = breaker_state()
    if not ok:
        return {"answer": None, "error": why, "skipped": True}
    ks = _keys()
    cand = [(prov, keyname, url, model) for prov, keyname, url, models in PROVIDERS
            if keyname in ks and prov not in _DEAD for model in models if (prov, model) not in _DEAD]
    if not cand:
        return {"answer": None, "error": "no live judge provider", "skipped": True}
    prov, keyname, url, model = cand[0]
    timeout = config.JUDGE_TIMEOUT_S if budget_s is None else max(1.0, min(config.JUDGE_TIMEOUT_S, budget_s))
    body = {"model": model, "max_tokens": 120, "temperature": 0,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT.format(label=label)},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_crop_b64(img, box)}"}}]}]}
    t = time.time()
    err = None
    try:
        # hard wall-clock deadline: requests' timeout is per socket read, so it can overrun the budget
        fut = _POOL.submit(requests.post, url, json=body, timeout=(min(3.0, timeout), timeout),
                           headers={"Authorization": f"Bearer {ks[keyname]}", "Content-Type": "application/json"})
        try:
            r = fut.result(timeout=timeout)
        except cf.TimeoutError:
            raise requests.Timeout("wall-clock deadline") from None
        if r.status_code != 200:
            err = f"{prov}/{model}: HTTP {r.status_code}"
            if r.status_code in (401, 402, 403):
                _DEAD.add(prov)
            else:                       # 429 / 404 / 5xx: drop this model, next call tries the next one
                _DEAD.add((prov, model))
    except requests.RequestException as e:
        err = f"{prov}/{model}: {type(e).__name__} after {time.time() - t:.0f} s"
        _strike((prov, model))
    if err:
        _BREAKER["fails_in_row"] += 1
        _BREAKER["last_error"] = err
        if _BREAKER["fails_in_row"] >= config.JUDGE_BREAKER_FAILS:
            _BREAKER["open_until"] = time.time() + config.JUDGE_COOLDOWN_S
        return {"answer": None, "error": err, "seconds": round(time.time() - t, 2)}
    _BREAKER.update(fails_in_row=0, open_until=0.0)
    try:
        txt = r.json()["choices"][0]["message"]["content"] or ""
        m = re.search(r"\{.*\}", txt, re.S)
        ans = json.loads(m.group(0)) if m else {"answer": "cannot_determine", "reason": "unparsed"}
    except Exception:  # noqa: BLE001
        ans = {"answer": "cannot_determine", "reason": "unparsed reply"}
    a = str(ans.get("answer", "")).lower()
    if a not in ("visible", "not_visible", "cannot_determine"):
        a = "cannot_determine"
    _STRIKES[(prov, model)] = 0
    return {"answer": a, "reason": str(ans.get("reason", ""))[:80], "provider": prov, "model": model,
            "seconds": round(time.time() - t, 2)}
