"""Thin adapter: let the existing router use the ELEMENT x BODY impact engine per body leaf.

Flag: route_with_engine(..., engine="impact", body="mw_self", context={...})   (engine="legacy" = old path)

Nothing in costs.py or routing.py is rewritten. The adapter
  * maps each attached evidence record (legacy barrier type + height/width/slope) to a taxonomy element,
  * scores it with hroute.impact for the chosen body leaf, keeping costs.p_present / p_attach as presence,
  * returns the same dict shape as costs.segment_cost, so routing.describe/route work unchanged,
  * swaps routing's segment_cost only for the calling thread (thread-local), so concurrent legacy requests
    in the API thread pool are not affected.
"""
from __future__ import annotations

import datetime as dt
import math
import threading
from contextlib import contextmanager

from . import costs as C
from . import impact as I
from . import routing as R
from .config import PROFILES, cfg, clear_types, evidence_sources, source_class

# legacy barrier type -> taxonomy element id (the receipt class_family vocabulary)
LEGACY_TO_ELEMENT = {
    "missing_kerb_ramp": "kerb_150_no_ramp",
    "steps": "steps_short_flight",
    "broken_footpath": "broken_pavers",
    "missing_footpath": "no_footpath_road_walk",
    "pole_obstruction": "electric_pole_midpath",
    "parked_vehicle": "two_wheeler_parked_footpath",
    "pothole": "pothole",
    "open_drain": "open_drain_parallel",
    "vendor": "vendor_handcart",
    "waterlogging": "waterlogging_shallow",
    "steep_slope": "running_slope_6",
}

# legacy profile -> default body leaf (so engine="impact" with a legacy profile name still works)
PROFILE_TO_BODY = {
    "manual_wheelchair": "mw_self", "power_wheelchair": "pw_standard", "walker_elderly": "older_with_walker",
    "pram": "pram_stroller", "crutches": "crutches_bilateral", "low_vision": "low_vision_severe",
    "default_walker": "no_impairment_adult",
}

CO_RADIUS_M = 10.0  # ASSUMPTION: two records interact (rain x pothole aside) only within 10 m on a segment

_local = threading.local()
_orig_segment_cost = R.segment_cost
_patch_lock = threading.Lock()
_patched = False


def element_for_evidence(ev: dict) -> tuple[str | None, dict]:
    t = ev.get("type")
    if ev.get("element"):           # a record may name a taxonomy element directly (new detectors)
        eid = ev["element"]
    elif t == "kerb_ramp_present":
        if ev.get("slope_pct") is None:
            return None, {}
        eid = "kerb_ramp_good"
    else:
        eid = LEGACY_TO_ELEMENT.get(t)
    if eid is None or eid not in I.data()["elements"]:
        return None, {}
    # a record may carry extra taxonomy attrs (what-if records: green_s, crossing_length_m, rest_gap_m, ...);
    # the measured fields below still win over them
    over = {k: v for k, v in (ev.get("attrs") or {}).items() if v is not None}
    if ev.get("height_cm") is not None:
        over["vertical_cm"] = float(ev["height_cm"])
    if ev.get("clear_width_cm") is not None:
        over["clear_width_cm"] = float(ev["clear_width_cm"])
    if ev.get("slope_pct") is not None:
        over["slope_pct"] = float(ev["slope_pct"])
    if t == "missing_kerb_ramp" and ev.get("height_cm") is None:
        over["vertical_cm"] = 15.0  # unknown height: assume the IRC 150 mm standard kerb (ASSUMPTION)
    return eid, over


def segment_cost_impact(seg: dict, body_id: str, leave: dt.datetime, context: dict | None = None) -> dict:
    b = I.body(body_id)
    legacy = b.get("legacy_profile") if b.get("legacy_profile") in PROFILES else "default_walker"
    ctx = dict(context or {})
    if ctx.get("hour") is None and leave is not None:
        ctx["hour"] = leave.astimezone(C.IST).hour  # sets light (night rules) and hour-range rules
    travel = seg["length_m"] / float(b["speed_mps"])
    delay, blocks, hits = 0.0, [], []
    c = cfg()
    recs = []
    for ev in seg["evidence"]:
        if ev.get("status", "ACCEPT") != "ACCEPT":
            continue
        if ev.get("type") == "osm_wheelchair_no":
            if b["scorer"] == "wheeled":
                blocks.append({"evidence_id": ev.get("id"), "type": "osm_wheelchair_no", "source": ev.get("source"),
                               "source_class": source_class(ev.get("source")), "blocking": True, "p_present": 1.0,
                               "why": "BLOCK: OSM says wheelchair=no", "lat": ev.get("lat"), "lon": ev.get("lon"),
                               "label": ev.get("label")})
            continue
        eid, over = element_for_evidence(ev)
        if eid is None:
            continue
        pp, pwhy = C.p_present(ev, leave)
        p = round(pp * float(ev.get("p_attach") or 1.0), 3)
        recs.append({"ev": ev, "eid": eid, "over": over, "p": p, "pwhy": pwhy, "at": ev.get("at_m")})
    groups = {}
    for i, r in enumerate(recs):
        # co-present = OTHER records that are likely there now (p >= block_p) and within CO_RADIUS_M along the
        # segment; records with no position never count (reviewer finding: stale or distant partners over-blocked)
        co = [o["eid"] for j, o in enumerate(recs) if j != i and o["p"] >= c["block_p"]
              and r["at"] is not None and o["at"] is not None and abs(r["at"] - o["at"]) <= CO_RADIUS_M]
        # verdict at full presence; presence is applied per cluster below, like costs.segment_cost
        res = I.impact({"id": r["eid"], "attrs": r["over"], "confidence": 1.0},
                       {**ctx, "co_present": co, "presence_from_ledger": True}, body_id)
        r["res"] = res
        groups.setdefault((r["eid"], res["verdict"] == "block"), []).append((r["at"], r))
    for (eid, is_block), items in groups.items():
        cl = C._clusters(items, float(c.get("dedupe_m", 5.0)))
        reps = [max(x, key=lambda it: it[1]["p"])[1] for x in cl]
        p_comb = 1 - math.prod(1 - r["p"] for r in reps)
        unit = max(I.route_penalty_s(r["res"], b) for r in reps)
        hard_block = is_block and p_comb >= c["block_p"]
        add = 0.0 if hard_block else p_comb * (c["soft_block_cost_s"] if is_block else unit)
        delay += add
        for rep, members in zip(reps, cl):
            ev, res = rep["ev"], rep["res"]
            item = {"evidence_id": ev.get("id"), "type": ev.get("type") or eid, "element": eid,
                    "source": ev.get("source"), "source_class": source_class(ev.get("source")),
                    "observed_at": ev.get("observed_at"), "p_present": rep["p"], "labels_in_cluster": len(members),
                    "lat": ev.get("lat"), "lon": ev.get("lon"), "label": ev.get("label"),
                    "verdict": res["verdict"], "risk": res["risk"], "rules_fired": res["rules_fired"],
                    "why": res["reason"] + f" ({rep['pwhy']})", "blocking": hard_block}
            if hard_block:
                item["why"] = "BLOCK: " + item["why"]
                blocks.append(item)
            else:
                if is_block:
                    item["why"] = (f"would block, but combined p {p_comb:.2f} < {c['block_p']}: soft cost. "
                                   + item["why"])
                item["type_cost_s"] = round(add, 1)
                item["type_p_combined"] = round(p_comb, 3)
            hits.append(item)
    if legacy in cfg().get("kind_block", {}).get(seg["kind"], []):
        blocks.append({"evidence_id": None, "type": "no_footpath_on_median", "source": "assumption",
                       "source_class": "assumption", "blocking": True, "p_present": 1.0,
                       "why": "BLOCK: generated median/island side, no footpath assumed (ASSUMPTION)",
                       "lat": None, "lon": None, "label": None})
    unc, p_unseen = C.uncertainty(seg, legacy)
    return {"blocked": bool(blocks), "blocks": blocks, "hits": hits, "travel_s": travel, "delay_s": delay,
            "uncertainty_s": unc, "p_unseen": round(p_unseen, 3),
            "weight": None if blocks else travel + delay + unc, "tier": C.tier(seg),
            "what_if": any(e.get("source") == "what_if" for e in seg["evidence"]),
            "engine": "impact", "body": body_id}


def _dispatch(seg, profile, leave):
    st = getattr(_local, "state", None)
    if st is None:
        return _orig_segment_cost(seg, profile, leave)
    return segment_cost_impact(seg, st["body"], leave, st["context"])


def _ensure_patched():
    global _patched
    with _patch_lock:
        if not _patched:
            R.segment_cost = _dispatch   # thread-local dispatch; legacy behaviour unchanged when unset
            _patched = True


@contextmanager
def using_body(body_id: str, context: dict | None = None):
    _ensure_patched()
    prev = getattr(_local, "state", None)
    _local.state = {"body": body_id, "context": context or {}}
    try:
        yield
    finally:
        _local.state = prev


def route_with_engine(net, start, end, profile_or_body="manual_wheelchair", leave_time=None,
                      engine="legacy", context=None) -> dict:
    """engine='legacy': routing.route unchanged. engine='impact': per body leaf via hroute.impact."""
    if engine == "legacy":
        return R.route(net, start, end, profile_or_body, leave_time)
    if engine != "impact":
        raise ValueError("engine must be 'legacy' or 'impact'")
    body_id = PROFILE_TO_BODY.get(profile_or_body, profile_or_body)
    b = I.body(body_id)  # KeyError for an unknown leaf
    legacy = b.get("legacy_profile") if b.get("legacy_profile") in PROFILES else "default_walker"
    with using_body(body_id, context):
        res = R.route(net, start, end, legacy, leave_time)
    res["engine"] = "impact"
    res["body"] = {"id": body_id, "name": b["name"], "scorer": b["scorer"], "path": b["path"],
                   "hermes_id": b.get("hermes_id"), "legacy_profile_for_unknowns": legacy}
    for k in ("shortest", "accessible", "least_blocked"):
        if res.get(k):
            res[k]["profile_label"] = b["name"]
            res[k]["body"] = body_id
    if res.get("summary"):
        res["summary"] = f"[impact engine, {b['name']}] " + res["summary"]
    return res
