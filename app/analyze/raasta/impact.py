"""Per-body impact of each scanned element: block / slow / warn / none.

Source of truth is built by another lane: app/site/public/content/impact-matrix.json or
app/route/hroute/impact.py. This module only LOOKS UP those files at request time (so it picks them up
the moment they land, no restart). If neither exists it returns status "loading" and no numbers:
nothing is invented here.
"""
from __future__ import annotations

import importlib.util
import json
import os

from . import config

MATRIX = os.path.join(config.APP, "site", "public", "content", "impact-matrix.json")
IMPACT_PY = os.path.join(config.ROUTE_DIR, "hroute", "impact.py")
BODIES = {"MW": "manual wheelchair", "PW": "power wheelchair", "WK": "walker", "CR": "crutches", "PR": "pram",
          "BL": "blind (cane)", "LV": "low vision", "EL": "elderly", "PG": "pregnant", "CH": "child",
          "TI": "temporary injury", "LG": "heavy luggage"}
VERDICTS = ("block", "slow", "warn", "none")

# detector family -> scan element id (so detector-only findings also get a body row)
FAMILY_TO_ELEMENT = {"steps": "steps", "missing_kerb_ramp": "kerb_no_ramp", "kerb_ramp_present": "kerb_ramp",
                     "broken_footpath": "broken_paving", "missing_footpath": "no_footpath",
                     "pole_obstruction": "pole", "parked_vehicle": "parked_two_wheeler", "open_drain": "open_drain",
                     "pothole": "pothole", "vendor": "vendor_cart"}


def _elements(dets, v) -> list[dict]:
    out, seen = [], set()
    for d in dets:
        if d["status"] == "REJECT":
            continue
        eid = FAMILY_TO_ELEMENT.get(d["class_family"], d["class_family"])
        if eid in seen:
            continue
        seen.add(eid)
        out.append({"id": eid, "matrix_id": FAMILY_TO_MATRIX.get(d["class_family"]), "from": "detectors " + ("A+B" if all(v is not None for v in d["scores"].values()) else (d.get("only") or "?") + " only"),
                    "status": d["status"]})
    for e in (v or {}).get("elements") or []:
        if e["id"] in seen or e["id"] == "other":
            continue
        seen.add(e["id"])
        out.append({"id": e["id"], "matrix_id": SCAN_TO_MATRIX.get(e["id"]), "from": "VLM only", "status": "VLM_ONLY", "confidence": e.get("confidence")})
    return out


def _norm(val):
    s = str(val).lower()
    if s in VERDICTS:
        return s
    if s in ("x", "b", "block", "blocked", "hard"):
        return "block"
    if s in ("c", "cost") or s.startswith("+3") or s.startswith("+2"):
        return "slow"
    if s in ("w",) or s.startswith("+1"):
        return "warn"
    if s in ("0", "n", "none", "ok"):
        return "none"
    return s


# detector family -> matrix element: copied from app/route/hroute/impact_adapter.py LEGACY_TO_ELEMENT (00:07 IST)
FAMILY_TO_MATRIX = {"missing_kerb_ramp": "kerb_150_no_ramp", "steps": "steps_short_flight", "broken_footpath": "broken_pavers",
                    "missing_footpath": "no_footpath_road_walk", "pole_obstruction": "electric_pole_midpath",
                    "parked_vehicle": "two_wheeler_parked_footpath", "pothole": "pothole", "open_drain": "open_drain_parallel",
                    "vendor": "vendor_handcart", "kerb_ramp_present": "kerb_ramp_good"}
# scan element id (raasta/vlm.py ELEMENTS) -> matrix element. Indoor ids without a close matrix element stay unmapped.
SCAN_TO_MATRIX = {
    "no_footpath": "no_footpath_road_walk", "kerb_high": "kerb_150_no_ramp", "kerb_ramp": "kerb_ramp_good",
    "kerb_no_ramp": "kerb_150_no_ramp", "ramp_steep": "kerb_ramp_steep_1in8", "narrow_path": "narrow_footpath_80",
    "slope": "running_slope_6", "height_changes": "footpath_step_down_repeated", "path_ends": "footpath_dead_end",
    "gaps_cracks": "wide_joint_gap", "drain_grating": "grating_parallel_slots", "steps": "steps_short_flight",
    "handrail_present": "handrail_continuous", "handrail_missing": "steps_no_handrail", "bollards": "bollards_narrow_80",
    "guardrail": "guardrail_continuous", "low_overhead": "low_signboard", "protruding": "protrusion_100mm_plus",
    "tactile_paving": "tactile_paving_correct", "tree_pit": "tree_pit_open", "utility_cover": "utility_cover_raised",
    "pothole": "pothole", "broken_paving": "broken_pavers", "open_drain": "open_drain_parallel", "open_manhole": "open_manhole",
    "trench_dug": "open_trench", "debris": "construction_debris", "slippery": "polished_granite", "zebra_faded": "zebra_faded",
    "garbage": "garbage_heap", "pole": "electric_pole_midpath", "transformer_box": "transformer_on_footpath",
    "tree_trunk": "tree_trunk_in_path", "shop_platform": "otla_shop_platform", "seating_spill": "cafe_seating_spill",
    "vendor_cart": "vendor_handcart", "parked_two_wheeler": "two_wheeler_parked_footpath", "parked_car": "car_parked_footpath",
    "construction_material": "construction_pipes", "dangling_cables": "dangling_cables", "barricade": "police_barricade",
    "puddle": "waterlogging_shallow", "animals": "stray_cattle", "crowd": "crowd_dense", "moving_traffic": "fast_road_edge",
    "dark": "streetlight_off", "glare": "headlight_glare", "low_contrast_edge": "step_nosing_no_contrast",
    "turning_space": "no_turning_space", "lift": "fob_lift_working",
}
# the 12 body leaves shown as table columns (all 74 are counted in each row's "all_bodies")
KEY_BODIES = ["blind_cane", "low_vision_severe", "mw_self", "pw_standard", "older_with_walker", "crutches_bilateral",
              "pram_stroller", "older_80_frail", "child_5_12", "pregnant_third_trimester", "rolling_luggage", "no_impairment_adult"]
_MCACHE: dict = {}


def _matrix():
    st = os.stat(MATRIX)
    if _MCACHE.get("mtime") != st.st_mtime:
        _MCACHE.update(mtime=st.st_mtime, m=json.load(open(MATRIX)))
    return _MCACHE["m"]


def _context(cond: dict | None, v: dict | None) -> str:
    light = (cond or {}).get("light") or ""
    weather = ((v or {}).get("weather") or "").lower()
    if weather in ("rain", "wet"):
        return "monsoon_rain_evening"
    if "night" in light or (v or {}).get("light") == "night":
        return "night_dark"
    return "day_clear"


def _from_matrix(els, cond=None, v=None):
    m = _matrix()
    ids, bodies = m["elements"], m["bodies"]
    ctx = _context(cond, v)
    verdicts = m["contexts"][ctx]["verdict"]
    info = {e["id"]: e for e in m.get("element_info", [])}
    binfo = {b["id"]: b for b in m.get("body_info", [])}
    key = [b for b in KEY_BODIES if b in bodies]
    rows = []
    for e in els:
        mid = e.get("matrix_id")
        if mid not in ids:
            rows.append({**e, "bodies": None, "why_missing": "no matching element in the impact matrix (indoor or unmapped)"})
            continue
        letters = verdicts[ids.index(mid)]
        allb = {b: _norm(letters[i]) for i, b in enumerate(bodies)}
        counts = {k: sum(1 for x in allb.values() if x == k) for k in VERDICTS}
        rows.append({**e, "matrix_name": info.get(mid, {}).get("name"), "matrix_source": info.get(mid, {}).get("source"),
                     "bodies": {b: allb[b] for b in key}, "all_bodies": counts})
    return {"status": "ok", "source": "app/site/public/content/impact-matrix.json (" + m.get("schema", "") + ")",
            "context": ctx, "context_label": m["contexts"][ctx]["label"], "about": m.get("about"),
            "bodies": {b: binfo.get(b, {}).get("name", b) for b in key}, "body_count": len(bodies), "rows": rows}


def _from_py(els):
    spec = importlib.util.spec_from_file_location("hroute_impact_live", IMPACT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = next((getattr(mod, n) for n in ("impact_for", "impacts_for", "element_impact", "impact") if callable(getattr(mod, n, None))), None)
    if fn is None:
        raise AttributeError("hroute/impact.py has no impact_for / impacts_for / element_impact / impact function")
    rows = []
    for e in els:
        r = fn(e["id"])
        rows.append({**e, "bodies": {k: _norm(v) for k, v in r.items()} if isinstance(r, dict) else None})
    return {"status": "ok", "source": "app/route/hroute/impact.py", "bodies": getattr(mod, "BODIES", BODIES), "rows": rows}


def for_scan(dets, v, cond=None) -> dict:
    els = _elements(dets, v)
    errors = []
    for path, fn in ((MATRIX, lambda x: _from_matrix(x, cond, v)), (IMPACT_PY, _from_py)):
        if os.path.exists(path):
            try:
                return fn(els)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{os.path.basename(path)}: {type(e).__name__}: {e}")
    return {"status": "loading", "message": "body impacts loading: the impact matrix is being built by another lane; no numbers shown until it lands",
            "bodies": BODIES, "rows": [{**e, "bodies": None} for e in els], "errors": errors}
