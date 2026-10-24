"""Decision policy: detector scores + agreement + footpath context -> ACCEPT / ABSTAIN / REJECT.

Works on receipt detection dicts, so the same code runs live (pipeline.py) and offline on old
receipts (tools/calibrate.py). Per-class parameters come from config.POLICY, chosen on the C6 dev
split only (CALIBRATION.md).

Per eval class:
  single_A / single_B : a one-detector hit with score >= this is ACCEPTed with the lower evidence
                        tier "single detector" (None = never; the default two-detector rule)
  context_downgrade   : an A+B agreement whose foot stands on the carriageway becomes ABSTAIN
  abstain_floor       : single hits below single_* but >= this are ABSTAIN, below are REJECT
"""
from __future__ import annotations

from . import config

FAMILY_TO_CLASS = {
    "missing_kerb_ramp": "missing_kerb_ramp", "steps": "steps",
    "broken_footpath": "broken_or_missing_footpath", "missing_footpath": "broken_or_missing_footpath",
    "pole_obstruction": "pole_obstruction", "parked_vehicle": "parked_vehicle",
}

DEFAULT = {"single_A": None, "single_B": None, "context_downgrade": False, "abstain_floor": 0.25}


def params_for(family: str, policy: dict | None = None) -> dict:
    policy = config.POLICY if policy is None else policy
    cls = FAMILY_TO_CLASS.get(family, "_other")
    p = dict(DEFAULT)
    p.update(policy.get("_other", {}))
    p.update(policy.get(cls, {}))
    return p


def decide(d: dict, policy: dict | None = None) -> None:
    """Set d['status'], d['why'], d['evidence_tier'] in place. Keeps d['base_status'] (the agreement-only
    decision) so the policy can be re-run on old receipts."""
    if "base_status" not in d:
        d["base_status"] = d["status"]
    p = params_for(d["class_family"], policy)
    a, b = (d.get("scores") or {}).get("A"), (d.get("scores") or {}).get("B")
    ctx = (d.get("footpath_context") or {}).get("verdict")
    j = (d.get("judge") or {}).get("answer")
    if a is not None and b is not None:
        if p["context_downgrade"] and ctx == "carriageway" and d["class_family"] in config.ON_FOOTPATH_FAMILIES:
            d["status"], d["evidence_tier"] = "ABSTAIN", "two detectors, but on the carriageway"
            d["why"] = (f"A and B agree (IoU {d.get('iou_AB', 0):.2f}), but the ground under it reads as carriageway, "
                        "not footpath (a barrier only where people walk on the road)")
        else:
            d["status"], d["evidence_tier"] = "ACCEPT", "two detectors agree"
            d["why"] = f"A and B agree (IoU {d.get('iou_AB', 0):.2f}, same family)"
        return
    who, s = ("A", a) if a is not None else ("B", b)
    thr = p["single_A"] if who == "A" else p["single_B"]
    if j == "not_visible":
        d["status"], d["evidence_tier"] = "REJECT", "single detector, judge says not visible"
        d["why"] = "single detector; VLM judge says not visible"
    elif thr is not None and s >= thr:
        d["status"], d["evidence_tier"] = "ACCEPT", "single detector (calibrated for this class, lower tier)"
        d["why"] = (f"only detector {who} (score {s:.2f} >= {thr} calibrated on the C6 dev split for "
                    f"{FAMILY_TO_CLASS.get(d['class_family'], d['class_family'])}); weaker than A+B")
    elif s >= p["abstain_floor"]:
        d["status"], d["evidence_tier"] = "ABSTAIN", "single detector"
        d["why"] = f"only detector {who} sees it: needs a human look"
    else:
        d["status"], d["evidence_tier"] = "REJECT", "single detector, low score"
        d["why"] = f"only detector {who}, score {s:.2f} < {p['abstain_floor']}"
    if j == "visible" and d["status"] == "ABSTAIN":
        d["why"] += "; VLM judge says visible (support only)"
