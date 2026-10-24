"""Step 3 measure: kerb / step height in cm from three independent routes.

route 1 metric depth : Depth Anything V2 metric (outdoor) depth at the box's top and bottom bands,
                       back-projected with focal f and horizon row v_h: Y = (v_h - v) * Z / f.
route 2 geometry     : single-view metrology on the ground plane (level camera at height Hc):
                       h = Hc * (v_b - v_t) / (v_b - v_h). Hc in CAM_HEIGHT_M (assumed, stated).
route 3 shadow       : kerb shadow width w on the ground (from route 2's ground scale) and the sun
                       elevation e from time + GPS: h = w * tan(e) / |cos(alpha)|, alpha = angle between
                       the shadow direction and the kerb normal (needs camera heading).
Each route returns value +- err (half the min..max over its assumption grid). Agreement = intervals
overlap. A height is printed only when >= 2 routes agree and the error is small; otherwise ABSTAIN.
"""
from __future__ import annotations

import itertools
import math

import cv2
import numpy as np

from . import config


# ---------------- camera model ----------------
def focal_px(w: int, h: int, focal_35mm: float | None) -> dict:
    if focal_35mm and focal_35mm > 5:
        f = focal_35mm * math.hypot(w, h) / math.hypot(36, 24)
        return {"f": f, "f_range": (f * 0.97, f * 1.03), "source": f"EXIF 35 mm equiv {focal_35mm:.0f} mm"}
    def from_fov(deg):
        return (w / 2) / math.tan(math.radians(deg) / 2)
    lo, hi = config.HFOV_RANGE_DEG
    return {"f": from_fov(config.DEFAULT_HFOV_DEG), "f_range": (from_fov(hi), from_fov(lo)),
            "source": f"assumed horizontal FOV {config.DEFAULT_HFOV_DEG:.0f} deg (range {lo:.0f}-{hi:.0f})"}


def horizon(img_rgb: np.ndarray) -> dict:
    """Horizon row from the dominant vanishing point of street lines (assumes roll ~ 0)."""
    H, W = img_rgb.shape[:2]
    scale = 960 / max(H, W)
    small = cv2.resize(img_rgb, (int(W * scale), int(H * scale))) if scale < 1 else img_rgb
    sH, sW = small.shape[:2]
    gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 60, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength=int(0.06 * math.hypot(sH, sW)), maxLineGap=8)
    fallback = {"v_h": H / 2, "err": 0.12 * H, "source": "fallback: level camera, horizon at image centre",
                "n_lines": 0}
    if lines is None:
        return fallback
    segs = []
    for x1, y1, x2, y2 in np.asarray(lines).reshape(-1, 4).astype(float):
        ang = abs(math.degrees(math.atan2(y2 - y1, x2 - x1))) % 180
        ang = min(ang, 180 - ang)
        if 12 < ang < 78:                 # perspective lines, not horizontal or vertical
            segs.append((x1, y1, x2, y2))
    if len(segs) < 4:
        fallback["n_lines"] = len(segs)
        return fallback
    segs = segs[:120]
    pts = []
    for (a, b) in itertools.combinations(segs, 2):
        x1, y1, x2, y2 = a
        x3, y3, x4, y4 = b
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(d) < 1e-6:
            continue
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
        if -0.5 * sW < px < 1.5 * sW and 0.05 * sH < py < 0.95 * sH:
            pts.append((px, py))
    if len(pts) < 6:
        fallback["n_lines"] = len(segs)
        return fallback
    P = np.array(pts)
    # densest cluster: point with most neighbours within 4 % of the diagonal
    r = 0.04 * math.hypot(sW, sH)
    sample = P if len(P) <= 1500 else P[np.random.default_rng(0).choice(len(P), 1500, replace=False)]
    cnt = [(np.hypot(*(P - p).T) < r).sum() for p in sample]
    best = sample[int(np.argmax(cnt))]
    inl = P[np.hypot(*(P - best).T) < r]
    vy = float(np.median(inl[:, 1])) / scale
    mad = float(np.median(np.abs(inl[:, 1] - np.median(inl[:, 1])))) / scale
    frac = len(inl) / len(P)
    err = max(1.4826 * mad, 0.03 * H) * (1.0 if frac > 0.15 else 2.0)
    return {"v_h": vy, "vp_x": float(np.median(inl[:, 0])) / scale, "err": err,
            "source": f"vanishing point of {len(segs)} street lines, {len(inl)}/{len(P)} intersections agree",
            "n_lines": len(segs)}


def _span(vals):
    vals = [v for v in vals if v is not None and math.isfinite(v)]
    if not vals:
        return None
    lo, hi = min(vals), max(vals)
    return (lo + hi) / 2, (hi - lo) / 2


def _plausible(fam_prompt: str):
    lo, hi = config.KERB_PLAUSIBLE_CM
    if fam_prompt == "stairs":
        hi = 400.0
    return lo, hi


# ---------------- riser edges ----------------
def riser(img_rgb: np.ndarray, box, prompt: str) -> tuple[list, str]:
    """Narrow a kerb/step box to its riser: the lowest strong horizontal edge (kerb foot) and the
    next strong horizontal edge above it (kerb lip), from a Sobel-y row profile of the centre strip.
    Detector boxes include the top surface and the background, which inflates every height route."""
    if prompt == "stairs":
        return list(box), "stairs: whole box (total rise of the flight)"
    H, W = img_rgb.shape[:2]
    x1, y1, x2, y2 = [int(round(v)) for v in box]
    bw, bh = x2 - x1, y2 - y1
    if bh < 12 or bw < 12:
        return list(box), "box too small to refine"
    ya, yb = y1, min(H, y2 + max(2, bh // 10))
    strip = cv2.cvtColor(img_rgb[ya:yb, x1 + bw // 4:x2 - bw // 4], cv2.COLOR_RGB2GRAY).astype(np.float32)
    gy = np.abs(cv2.Sobel(cv2.GaussianBlur(strip, (5, 5), 0), cv2.CV_32F, 0, 1, ksize=3)).mean(axis=1)
    if gy.size < 8:
        return list(box), "strip too small"
    thr = gy.mean() + 1.0 * gy.std()
    peaks = [i for i in range(1, len(gy) - 1) if gy[i] >= thr and gy[i] >= gy[i - 1] and gy[i] >= gy[i + 1]]
    # merge peaks closer than 3 px
    merged = []
    for p in peaks:
        if merged and p - merged[-1] < 3:
            if gy[p] > gy[merged[-1]]:
                merged[-1] = p
            continue
        merged.append(p)
    lower = [p for p in merged if p >= 0.5 * bh]
    if len(merged) < 2 or not lower:
        return list(box), "no clear pair of horizontal edges; whole box used"
    foot = max(lower)
    above = [p for p in merged if p < foot - max(5, 0.08 * bh)]
    if not above:
        return list(box), "no lip edge above the foot edge; whole box used"
    lip = max(above)
    return [box[0], float(ya + lip), box[2], float(ya + foot)], \
        f"riser from horizontal edges: lip row {ya + lip}, foot row {ya + foot} (box rows {y1}-{y2})"


# ---------------- route 1: metric depth ----------------
def route_depth(depth: np.ndarray | None, box, cam: dict, hz: dict, prompt: str) -> dict:
    if depth is None:
        return {"route": "metric_depth", "ok": False, "why": "depth model not run"}
    H, W = depth.shape
    x1, y1, x2, y2 = [int(round(v)) for v in box]
    bh, bw = y2 - y1, x2 - x1
    if bh < 6 or bw < 6:
        return {"route": "metric_depth", "ok": False, "why": "box too small for depth bands"}
    cx1, cx2 = x1 + bw // 4, x2 - bw // 4
    band = max(2, bh // 10)
    zb = float(np.median(depth[max(0, y2 - band):y2, cx1:cx2]))
    zt = float(np.median(depth[y1:min(H, y1 + band), cx1:cx2]))
    if not (0.3 < zb < 40 and 0.3 < zt < 40):
        return {"route": "metric_depth", "ok": False, "why": f"depth out of range (bottom {zb:.1f} m, top {zt:.1f} m)"}
    if zt > zb * 1.6:
        return {"route": "metric_depth", "ok": False,
                "why": f"top band is background ({zt:.1f} m vs {zb:.1f} m at the bottom): box top is not on the object"}
    vb, vt = y2 - band / 2, y1 + band / 2
    vals = []
    for f in cam["f_range"] + (cam["f"],):
        for vh in (hz["v_h"] - hz["err"], hz["v_h"], hz["v_h"] + hz["err"]):
            for s in (0.85, 1.0, 1.15):   # metric-depth scale error, ~15 % (assumed)
                h = ((vh - vt) * zt * s - (vh - vb) * zb * s) / f
                vals.append(100 * h)
    v, e = _span(vals)
    lo, hi = _plausible(prompt)
    out = {"route": "metric_depth", "value_cm": round(v, 1), "err_cm": round(e, 1),
           "inputs": {"z_bottom_m": round(zb, 2), "z_top_m": round(zt, 2)}}
    if not (lo <= v <= hi):
        out.update(ok=False, why=f"value {v:.0f} cm outside plausible {lo:.0f}-{hi:.0f} cm")
    else:
        out["ok"] = True
    return out


# ---------------- route 2: camera-height geometry ----------------
def route_geometry(box, hz: dict, img_h: int, prompt: str) -> dict:
    x1, y1, x2, y2 = box
    vals = []
    for vh in (hz["v_h"] - hz["err"], hz["v_h"], hz["v_h"] + hz["err"]):
        if y2 - vh < 0.03 * img_h:
            continue
        for hc in config.CAM_HEIGHT_M:
            vals.append(100 * hc * (y2 - y1) / (y2 - vh))
    if not vals:
        return {"route": "geometry", "ok": False, "why": "box bottom is not clearly below the horizon (not on the ground plane)"}
    v, e = _span(vals)
    lo, hi = _plausible(prompt)
    out = {"route": "geometry", "value_cm": round(v, 1), "err_cm": round(e, 1),
           "assumes": f"level camera at {config.CAM_HEIGHT_M[0]}-{config.CAM_HEIGHT_M[1]} m, box bottom on the ground, "
                      "box top directly above it"}
    out["ok"] = lo <= v <= hi
    if not out["ok"]:
        out["why"] = f"value {v:.0f} cm outside plausible {lo:.0f}-{hi:.0f} cm"
    return out


# ---------------- route 3: shadow altimetry ----------------
def route_shadow(img_rgb, box, hz: dict, cam: dict, sun: dict | None, heading: float | None, light: str) -> dict:
    r = {"route": "shadow", "ok": False}
    if sun is None:
        return {**r, "why": "no shadow evidence: needs capture time + GPS for the sun position"}
    e = sun["elevation_deg"]
    if e < 5 or light not in ("day",):
        return {**r, "why": f"no shadow evidence: sun elevation {e:.1f} deg / light '{light}'"}
    if heading is None:
        return {**r, "why": "no shadow evidence: camera heading unknown, cannot orient the shadow"}
    shadow_dir = (sun["azimuth_deg"] + 180) % 360
    kerb_normal = (heading + 180) % 360          # kerb assumed to face the camera
    alpha = math.radians((shadow_dir - kerb_normal + 180) % 360 - 180)
    if abs(math.cos(alpha)) < 0.35:
        return {**r, "why": f"shadow runs along the kerb (alpha {math.degrees(alpha):.0f} deg), too oblique"}
    H, W = img_rgb.shape[:2]
    x1, y1, x2, y2 = [int(round(v)) for v in box]
    bh, bw = y2 - y1, x2 - x1
    ya, yb = y1, min(H, y2 + bh // 2)
    strip = cv2.cvtColor(img_rgb[ya:yb, x1 + bw // 4:x2 - bw // 4], cv2.COLOR_RGB2GRAY).astype(float)
    if strip.size == 0:
        return {**r, "why": "no shadow evidence: empty strip"}
    prof = strip.mean(axis=1)
    med = float(np.median(prof))
    dark = prof < 0.65 * med
    if dark.sum() < 2:
        return {**r, "why": "no shadow evidence: no dark band next to the edge"}
    # longest dark run
    best, cur, start, bs = 0, 0, 0, 0
    for i, d in enumerate(dark):
        if d:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best, bs = cur, start
        else:
            cur = 0
    r1, r2 = ya + bs, ya + bs + best
    vals = []
    for vh in (hz["v_h"] - hz["err"], hz["v_h"], hz["v_h"] + hz["err"]):
        if r1 - vh < 0.03 * H:
            continue
        for hc in config.CAM_HEIGHT_M:
            g1 = cam["f"] * hc / (r1 - vh)
            g2 = cam["f"] * hc / (r2 - vh)
            w = abs(g1 - g2)
            for de in (-1.0, 0, 1.0):
                vals.append(100 * w * math.tan(math.radians(e + de)) / abs(math.cos(alpha)))
    if not vals:
        return {**r, "why": "no shadow evidence: dark band not on the ground plane"}
    v, err = _span(vals)
    lo, hi = config.KERB_PLAUSIBLE_CM
    out = {**r, "value_cm": round(v, 1), "err_cm": round(err, 1),
           "inputs": {"sun_elev_deg": e, "alpha_deg": round(math.degrees(alpha), 1), "dark_rows": [r1, r2]}}
    out["ok"] = lo <= v <= hi
    if not out["ok"]:
        out["why"] = f"value {v:.0f} cm outside plausible {lo:.0f}-{hi:.0f} cm (dark band is probably not the kerb shadow)"
    return out


# ---------------- fusion ----------------
def fuse(routes: list[dict]) -> dict:
    good = [r for r in routes if r.get("ok")]
    if not good:
        return {"height_status": "NO_ESTIMATE", "why": "no route produced a plausible value"}
    if len(good) == 1:
        g = good[0]
        return {"height_status": "ABSTAIN", "why": f"only one route ({g['route']}) produced a value; not cross-checked",
                "single_route": {"route": g["route"], "value_cm": g["value_cm"], "err_cm": g["err_cm"]}}
    best_set: list[dict] = []
    for k in range(len(good), 1, -1):
        for combo in itertools.combinations(good, k):
            if all(abs(a["value_cm"] - b["value_cm"]) <= a["err_cm"] + b["err_cm"] for a, b in itertools.combinations(combo, 2)):
                best_set = list(combo)
                break
        if best_set:
            break
    if not best_set:
        vals = ", ".join(f"{g['route']} {g['value_cm']:.0f}+-{g['err_cm']:.0f}" for g in good)
        return {"height_status": "ABSTAIN", "why": f"routes disagree ({vals})", "routes_agreed": []}
    w = [1 / max(g["err_cm"], 0.5) ** 2 for g in best_set]
    v = sum(wi * g["value_cm"] for wi, g in zip(w, best_set)) / sum(w)
    vals = [g["value_cm"] for g in best_set]
    err = max(math.sqrt(1 / sum(w)), (max(vals) - min(vals)) / 2)
    res = {"routes_agreed": [g["route"] for g in best_set], "height_cm": round(v, 1), "height_err_cm": round(err, 1)}
    if err > config.HEIGHT_ACCEPT_MAX_ERR_CM or err / max(v, 1) > config.HEIGHT_ACCEPT_MAX_REL:
        return {"height_status": "ABSTAIN", "why": f"routes overlap but the spread is too wide (+-{err:.0f} cm)",
                "routes_agreed": res["routes_agreed"], "candidate": {"value_cm": res["height_cm"], "err_cm": res["height_err_cm"]}}
    return {"height_status": "ACCEPT", **res}
