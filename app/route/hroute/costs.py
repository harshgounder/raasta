"""Per-profile segment costs from attached evidence, at a leave time.

segment cost (s) = travel (length / profile speed)
                 + barrier delay: per barrier type, clusters (same type within dedupe_m) combined as
                   1 - prod(1 - p_eff) times the type's cost_s, where p_eff = p_present x p_attach
                 + uncertainty: -ln(1 - min(p_unseen, 0.99)) x profile unknown_penalty_s, with
                   p_unseen = 1 - (1 - per_100m)^(uncovered_length / 100) for linear kinds, per_segment
                   for short kinds. Only clear-type evidence covers length (clear_radius_m around it).
A barrier never makes a segment cheaper. A blocking rule with combined p_eff >= block_p removes the
segment for that profile. Unknown segments are never called safe.

Tiers: known_barrier (photo or volunteer-label barrier), known_clear (photo or volunteer label says
fine), osm_tag (only OSM tags), unknown. what_if records cost like barriers but are not evidence.
"""
from __future__ import annotations

import datetime as dt
import math

from .attach import IST, has_clock_time, parse_time
from .config import cfg, clear_types, evidence_sources, source_class

MOHUA_PCT = 100 / 12   # 8.33 %, MoHUA Harmonised Guidelines 2021 (Mar 2022 print) cl. 3.7.2 kerb ramp max 1:12
IRC_PCT = 100 / 15     # 6.67 %, IRC:103-2022 sec 6.7 Fig. 48 kerb ramp max 1:15
TIERS = ("known_barrier", "known_clear", "osm_tag", "unknown")


def _accepted(seg):
    return [e for e in seg["evidence"] if e.get("status", "ACCEPT") == "ACCEPT"]


def tier(seg: dict) -> str:
    evs = [e for e in _accepted(seg) if e.get("source") in evidence_sources()]
    if any(e.get("type") not in clear_types() for e in evs):
        return "known_barrier"
    if evs:
        return "known_clear"
    if any(e.get("source") == "osm_tag" for e in _accepted(seg)):
        return "osm_tag"
    return "unknown"


def p_present(ev: dict, leave: dt.datetime) -> tuple[float, str]:
    conf = float(ev.get("confidence") or 0.8)
    obs = parse_time(ev.get("observed_at"))
    if ev.get("permanence", "permanent") != "temporary":
        return conf, f"permanent, confidence {conf:.2f}"
    tc = cfg()["temporal"]
    t = ev["type"]
    hl = float(ev.get("half_life_h") or tc["default_half_life_h"].get(t, 24))
    if obs is None:
        decay, age_h = 0.0, None
    else:
        age_h = max(0.0, (leave - obs).total_seconds() / 3600)
        decay = 0.5 ** (age_h / hl)
    rec = tc["recurrence"].get(t, 0.0)
    base = max(decay, rec)
    curve = tc["hour_curve"].get(t)
    ratio = 1.0
    timed = has_clock_time(ev.get("observed_at"))
    if curve and timed:
        lh = leave.astimezone(IST).hour
        oh = obs.astimezone(IST).hour
        ratio = curve[lh] / max(curve[oh], 0.1)
    p = conf * min(1.0, base * ratio)
    why = (f"temporary: seen {age_h:.0f} h before leave time" if age_h is not None else "temporary: date unknown")
    why += f", half-life {hl:g} h -> {decay:.2f}, recurrence {rec:.2f}"
    if curve:
        why += (f", hour curve x{ratio:.2f} (ASSUMPTION)" if timed
                else ", observation has no time of day so no hour-curve ratio")
    return round(p, 3), why + f" => p_present {p:.2f}"


def _slope_text(s: float) -> str:
    ratio = f"1:{100 / s:.0f}" if s > 0 else "flat"
    return (f"slope {s:.1f}% ({ratio}): MoHUA HG 2021 cl. 3.7.2 limit 1:12 (8.33%) {'met' if s <= MOHUA_PCT + 1e-9 else 'exceeded'}, "
            f"IRC:103-2022 sec 6.7 limit 1:15 (6.67%) {'met' if s <= IRC_PCT + 1e-9 else 'exceeded'}")


def barrier_rule(ev: dict, profile: str) -> dict | None:
    """What one record means for one profile, before probability: {block, cost_s, why}. None = no effect."""
    t = ev.get("type")
    if ev.get("status", "ACCEPT") != "ACCEPT":
        return None
    c = cfg()
    prof = c["profiles"][profile]
    if t in clear_types():
        if ev.get("slope_pct") is None or t != "kerb_ramp_present":
            return None
        t = "steep_slope"  # a ramp exists: judge its slope
    if t == "osm_wheelchair_no":
        if profile in ("manual_wheelchair", "power_wheelchair"):
            return {"block": True, "cost_s": 0.0, "why": "OSM says wheelchair=no"}
        return None
    if t == "steep_slope":
        s = float(ev.get("slope_pct") or 0)
        txt = _slope_text(s)
        blk = prof.get("slope_block_pct")
        if blk is not None and s > blk + 1e-9:
            return {"block": True, "cost_s": 0.0, "why": f"{txt}; {prof.get('slope_rule', '')}"}
        frm = prof.get("slope_cost_from_pct")
        if frm is not None and s > frm:
            return {"block": False, "cost_s": float(c["barriers"]["steep_slope"][profile]["cost_s"]), "why": txt}
        return {"block": False, "cost_s": 0.0, "why": txt + "; no cost for this profile"}
    rule = c["barriers"].get(t, {}).get(profile)
    if rule is None:
        return None
    block = bool(rule.get("block"))
    why = t.replace("_", " ")
    h = ev.get("height_cm")
    if "block_if_height_cm_gt" in rule:
        thr = rule["block_if_height_cm_gt"]
        if h is None:
            if rule.get("unknown_height") == "block":
                block = True
                why += f": height not measured, assumed above {thr:g} cm"
        elif float(h) > thr:
            block = True
            why += f": kerb {float(h):.0f} cm > {thr:g} cm limit"
        else:
            why += f": kerb {float(h):.0f} cm <= {thr:g} cm"
    if "block_if_clear_width_cm_lt" in rule and ev.get("clear_width_cm") is not None:
        cw = float(ev["clear_width_cm"])
        if cw < rule["block_if_clear_width_cm_lt"]:
            block = True
            why += f": clear width {cw:.0f} cm < {rule['block_if_clear_width_cm_lt']} cm"
    cost = float(rule.get("cost_s", 0)) + float(rule.get("per_cm_s", 0)) * float(h or 0)
    return {"block": block, "cost_s": cost, "why": why}


def barrier_effect(ev: dict, profile: str, leave: dt.datetime) -> dict | None:
    """One record alone: {block, cost_s, p, why} with p = p_present x p_attach."""
    r = barrier_rule(ev, profile)
    if r is None:
        return None
    pp, pwhy = p_present(ev, leave)
    p = round(pp * float(ev.get("p_attach") or 1.0), 3)
    return _decide(r["block"], r["cost_s"], p, r["why"], pwhy + f", x p_attach {float(ev.get('p_attach') or 1):.2f}")


def _decide(block, cost, p, why, pwhy):
    c = cfg()
    if block:
        if p >= c["block_p"]:
            return {"block": True, "cost_s": 0.0, "p": p, "why": f"BLOCK: {why} ({pwhy})"}
        return {"block": False, "cost_s": p * c["soft_block_cost_s"], "p": p,
                "why": f"would block, but p {p:.2f} < {c['block_p']}: soft cost ({why}; {pwhy})"}
    return {"block": False, "cost_s": p * cost, "p": p, "why": f"{why}: +{p * cost:.0f} s ({pwhy})"}


def _clusters(items, radius):
    """items: [(at_m or None, payload)], same type. Chain items closer than radius."""
    known = sorted((x for x in items if x[0] is not None), key=lambda x: x[0])
    out, cur = [], []
    for it in known:
        if cur and it[0] - cur[-1][0] > radius:
            out.append(cur)
            cur = []
        cur.append(it)
    if cur:
        out.append(cur)
    out += [[x] for x in items if x[0] is None]
    return out


def uncertainty(seg: dict, profile: str) -> tuple[float, float]:
    """(seconds, p_unseen). Only clear-type evidence near its position reduces it."""
    c = cfg()
    up = c["unknown_prior"]
    pen = c["profiles"][profile]["unknown_penalty_s"]
    k = seg["kind"]
    L = seg["length_m"]
    clears = [e for e in _accepted(seg) if e.get("type") in clear_types()
              and (e.get("source") in evidence_sources() or e.get("source") == "osm_tag")]
    if k in up["per_100m"]:
        r = float(up.get("clear_radius_m", 25.0))
        ivs = sorted((max(0.0, (e.get("at_m") if e.get("at_m") is not None else L / 2) - r),
                      min(L, (e.get("at_m") if e.get("at_m") is not None else L / 2) + r)) for e in clears)
        covered, end = 0.0, -1.0
        for a, b in ivs:
            if b <= end:
                continue
            covered += b - max(a, end)
            end = b
        uncovered = max(0.0, L - covered)
        p100 = float(up["per_100m"][k])
        p = 1 - (1 - p100) ** (uncovered / 100) if p100 < 1 else (1.0 if uncovered > 0 else 0.0)
    elif k in up["per_segment"]:
        p = 0.0 if clears else float(up["per_segment"][k])
    else:
        p = 1 - (1 - 0.3) ** (L / 100)
    if p <= 0:
        return 0.0, 0.0
    return -math.log(1 - min(p, 0.99)) * pen, p


def segment_cost(seg: dict, profile: str, leave: dt.datetime) -> dict:
    c = cfg()
    prof = c["profiles"][profile]
    travel = seg["length_m"] / prof["speed_mps"]
    delay, blocks, hits = 0.0, [], []
    groups = {}
    for ev in seg["evidence"]:
        r = barrier_rule(ev, profile)
        if r is None:
            continue
        pp, pwhy = p_present(ev, leave)
        p = pp * float(ev.get("p_attach") or 1.0)
        groups.setdefault((ev.get("type"), r["block"]), []).append(
            (ev.get("at_m"), {"ev": ev, "rule": r, "p": p, "pwhy": pwhy}))
    for (t, is_block), items in groups.items():
        cl = _clusters(items, float(c.get("dedupe_m", 5.0)))
        reps = [max(x, key=lambda it: it[1]["p"])[1] for x in cl]
        p_comb = 1 - math.prod(1 - r["p"] for r in reps)
        unit = max(r["rule"]["cost_s"] for r in reps)
        n_labels = len(items)
        for rep, members in zip(reps, cl):
            ev = rep["ev"]
            item = {"evidence_id": ev.get("id"), "type": t, "source": ev.get("source"),
                    "source_class": source_class(ev.get("source")), "observed_at": ev.get("observed_at"),
                    "p_present": round(rep["p"], 3), "labels_in_cluster": len(members),
                    "lat": ev.get("lat"), "lon": ev.get("lon"), "label": ev.get("label"),
                    "why": rep["rule"]["why"] + f" ({rep['pwhy']})"}
            hits.append(item)
        if is_block and p_comb >= c["block_p"]:
            for h in hits[-len(reps):]:
                h["why"] = "BLOCK: " + h["why"]
                h["blocking"] = True
                blocks.append(h)
        else:
            add = p_comb * (c["soft_block_cost_s"] if is_block else unit)
            delay += add
            for h in hits[-len(reps):]:
                h["blocking"] = False
                h["type_cost_s"] = round(add, 1)
                h["type_p_combined"] = round(p_comb, 3)
                h["type_labels"] = n_labels
    kind_block = profile in c.get("kind_block", {}).get(seg["kind"], [])
    if kind_block:
        blocks.append({"evidence_id": None, "type": "no_footpath_on_median", "source": "assumption",
                       "source_class": "assumption", "blocking": True, "p_present": 1.0,
                       "why": "BLOCK: generated median/island side of a dual carriageway or roundabout, "
                              "no footpath assumed (ASSUMPTION)", "lat": None, "lon": None, "label": None})
    unc, p_unseen = uncertainty(seg, profile)
    return {"blocked": bool(blocks), "blocks": blocks, "hits": hits, "travel_s": travel, "delay_s": delay,
            "uncertainty_s": unc, "p_unseen": round(p_unseen, 3),
            "weight": None if blocks else travel + delay + unc, "tier": tier(seg),
            "what_if": any(e.get("source") == "what_if" for e in seg["evidence"])}


def age_text(t: dt.datetime, now: dt.datetime) -> str:
    days = (now - t).total_seconds() / 86400
    if days < 1:
        return "today"
    if days < 45:
        return f"{days:.0f} days ago"
    if days < 365:
        return f"{days / 30.44:.0f} months ago"
    y = days / 365.25
    return f"{y:.1f} years ago" if y < 10 else f"{math.floor(y)} years ago"
