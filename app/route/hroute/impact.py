"""ELEMENT x BODY impact engine (RAASTA, SC-02).

impact(element, context, body) -> {verdict: block|cost|warn|none, seconds, risk 0-1, reason, ...}

Pipeline (one call):
  1. resolve the element (id or {id, attrs overrides, confidence}) from taxonomy/elements.json
  2. presence p = confidence x hour curve[hour] x season factor   (only when hour / season are given)
  3. interaction rules (taxonomy/interactions.json) change the attributes for this context and co-present
     elements, and may create compound elements (rain x pothole -> hole hidden under water); compounds
     are scored too and the worst result wins
  4. ONE SCORING FUNCTION PER BODY CATEGORY (SCORERS below: wheeled, ambulant, visual, hearing, cognitive,
     elderly, systemic, situational). Each reads the leaf's own sensitivity vector and hard limits from
     taxonomy/bodies.json, so the same obstruction gives a different weight per body leaf
  5. verdict: block (hard limit broken, or risk >= BLOCK_RISK, with p >= BLOCK_P), cost (seconds >= COST_S),
     warn (risk >= WARN_RISK or seconds >= WARN_S), none

All thresholds and scales in this file are ASSUMPTIONS (claude, 2026-10-25) and are listed in
taxonomy/README.md. Sourced numbers live in the taxonomy JSON with their source keys.
"""
from __future__ import annotations

import json
import math
import os
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
TAX = os.path.join(os.path.dirname(HERE), "taxonomy")

BLOCK_RISK = 0.6      # ASSUMPTION
try:
    from .config import cfg as _cfg
    BLOCK_P = float(_cfg()["block_p"])   # read from assumptions.json, not a copy
except Exception:  # pragma: no cover - engine usable without the router package config
    BLOCK_P = 0.5
COST_S = 15.0         # ASSUMPTION
WARN_S = 8.0          # ASSUMPTION
WARN_RISK = 0.1       # ASSUMPTION
COST_RISK = 0.35      # ASSUMPTION: a risk this high on something that covers the whole path cannot be stepped round
RANK = {"none": 0, "warn": 1, "cost": 2, "block": 3}

# seconds added at full intensity and full sensitivity, per axis (ASSUMPTION)
SEC = {"vertical": 60, "width": 60, "slope": 120, "cross": 60, "roughness": 60, "slip": 40, "fall": 20,
       "overhead": 10, "visibility": 15, "contrast": 40, "glare": 30, "flicker": 20, "noise": 40, "air": 90,
       "heat": 90, "cold": 40, "crowd": 90, "vehicle": 30, "animal": 40, "water": 120, "electric": 0,
       "cognitive": 90, "wait": 120, "effort": 120}
# risk weight per hazard axis (ASSUMPTION)
HAZ = {"fall": 0.9, "slip": 0.6, "overhead": 0.45, "vehicle": 0.7, "animal": 0.5, "electric": 1.0, "air": 0.4,
       "heat": 0.5, "cold": 0.3, "crowd": 0.4, "water": 0.5, "vertical": 0.3, "flicker": 0.6}
SEEN_AXES = ("fall", "vertical", "overhead", "slip", "animal")   # hazards you avoid by seeing them
AXIS_LABEL = {"vertical": "level change", "width": "clear width", "slope": "slope", "cross": "cross slope",
              "roughness": "surface evenness / vibration", "slip": "slip", "fall": "fall into hole/drop",
              "overhead": "head-height hazard", "collision": "walks into it (found by cane contact)", "find_and_pass": "find it and pass it", "visibility": "has to be seen", "contrast": "low contrast",
              "glare": "glare", "flicker": "flashing light", "noise": "noise", "air": "air quality",
              "heat": "heat", "cold": "cold", "crowd": "crowd", "vehicle": "moving vehicles",
              "animal": "animals", "water": "standing water", "electric": "electrocution", "cognitive":
              "wayfinding load", "wait": "forced wait", "effort": "exertion"}

LIGHT_DEFICIT = {"day": 0.0, "dawn": 0.5, "dusk": 0.5, "night_lit": 0.55, "night_dark": 1.0}
WEATHER_CONTRAST = {"fog": 0.7, "smog": 0.5, "haze": 0.25, "dust_storm": 0.9, "heavy_rain": 0.5, "rain": 0.3,
                    "drizzle": 0.15, "storm": 0.6, "snow": 0.4}
WET_WEATHER = {"drizzle", "rain", "heavy_rain", "storm", "snow"}


# ---------------------------------------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------------------------------------
@lru_cache(maxsize=1)
def data():
    with open(os.path.join(TAX, "elements.json")) as f:
        E = json.load(f)
    with open(os.path.join(TAX, "bodies.json")) as f:
        Bd = json.load(f)
    with open(os.path.join(TAX, "interactions.json")) as f:
        R = json.load(f)
    return {"elements": {e["id"]: e for e in E["elements"]}, "curves": E["hour_curves"],
            "seasons": E["season_profiles"], "bodies": {b["id"]: b for b in Bd["bodies"]}, "rules": R["rules"],
            "element_list": E["elements"], "body_list": Bd["bodies"], "element_tree": E["tree"],
            "body_tree": Bd["tree"]}


def element(eid):
    return data()["elements"][eid]


def body(bid):
    return data()["bodies"][bid]


# ---------------------------------------------------------------------------------------------------------
# context
# ---------------------------------------------------------------------------------------------------------
def norm_context(ctx: dict | None) -> dict:
    c = dict(ctx or {})
    hour = c.get("hour")
    if not c.get("light"):
        if hour is None:
            c["light"] = "day"
        else:
            h = int(hour) % 24
            c["light"] = ("dawn" if h in (5, 6) else "day" if 7 <= h <= 16 else "dusk" if h in (17, 18)
                          else "night_lit")
    c.setdefault("weather", "clear")
    c["co_present"] = c.get("co_present") or []
    tags = set()
    w = c["weather"]
    if w in ("heavy_rain", "storm") or c.get("waterlogged"):
        tags |= {"water", "flood"}
    if c.get("festival"):
        tags.add("festival")
    for eid in c["co_present"]:
        e = data()["elements"].get(eid)
        if e:
            tags |= set(e["tags"])
    c["_co_tags"] = tags
    if c.get("temp_c") is None and w == "heatwave":
        c["temp_c"] = 45
    if c.get("aqi") is None and w == "smog":
        c["aqi"] = 350
    c["_vis_env"] = max(LIGHT_DEFICIT.get(c["light"], 0.0), WEATHER_CONTRAST.get(w, 0.0))
    return c


def presence(el: dict, ctx: dict, conf: float) -> tuple[float, str]:
    t = el["temporal"]
    p, why = conf, [f"confidence {conf:.2f}"]
    if ctx.get("presence_from_ledger"):
        return round(p, 3), why[0] + " (presence from the evidence ledger)"
    if ctx.get("hour") is not None and t["pattern"] != "permanent":
        curve = data()["curves"].get(t.get("hour_curve") or "constant", [1.0] * 24)
        f = curve[int(ctx["hour"]) % 24]
        p *= f
        why.append(f"hour {int(ctx['hour'])} curve '{t.get('hour_curve')}' x{f:.2f}")
    if ctx.get("season") and t.get("season", "all") != "all":
        f = data()["seasons"][t["season"]].get(ctx["season"], 1.0)
        p *= f
        why.append(f"season {ctx['season']} x{f:.2f}")
    return round(p, 3), ", ".join(why)


# ---------------------------------------------------------------------------------------------------------
# interactions
# ---------------------------------------------------------------------------------------------------------
def _match(when: dict, el: dict, ctx: dict) -> bool:
    tags = set(el["tags"])
    if "weather_any" in when and ctx["weather"] not in when["weather_any"]:
        return False
    if "light_any" in when and ctx["light"] not in when["light_any"]:
        return False
    if "season_any" in when and ctx.get("season") not in when["season_any"]:
        return False
    if "hour_range" in when:
        h = ctx.get("hour")
        if h is None or not (when["hour_range"][0] <= int(h) <= when["hour_range"][1]):
            return False
    if "temp_min" in when and (ctx.get("temp_c") is None or ctx["temp_c"] < when["temp_min"]):
        return False
    if "aqi_min" in when and (ctx.get("aqi") is None or ctx["aqi"] < when["aqi_min"]):
        return False
    if when.get("festival") and not ctx.get("festival"):
        return False
    if "tags_any" in when and not (tags & set(when["tags_any"])):
        return False
    if "ids_any" in when and el["id"] not in when["ids_any"]:
        return False
    if "co_present_tags_any" in when and not (ctx["_co_tags"] & set(when["co_present_tags_any"])):
        return False
    if "co_present_any" in when and not (set(ctx["co_present"]) & set(when["co_present_any"])):
        return False
    return True


def apply_interactions(el: dict, attrs: dict, ctx: dict, b: dict | None = None) -> tuple[dict, list]:
    a = dict(attrs)
    fired = []
    blind = bool(b and b.get("limits", {}).get("light_independent"))
    for r in data()["rules"]:
        if el["category"] == "compound":
            break  # compounds already are the combination
        if blind and r.get("sighted_only"):
            continue
        if not _match(r["when"], el, ctx):
            continue
        eff = r["effect"]
        for k, v in eff.get("mul", {}).items():
            if a.get(k) is not None:
                a[k] = a[k] * v
        for k, v in eff.get("add", {}).items():
            a[k] = (a.get(k) or 0) + v
        for k, v in eff.get("set", {}).items():
            a[k] = v
        fired.append(r)
    for k in ("fall", "slip", "overhead", "vehicle", "animal", "electric", "air", "heat", "cold", "crowd",
              "contrast_loss", "glare", "flicker", "visibility_needed", "cognitive", "roughness"):
        if a.get(k) is not None:
            a[k] = max(0.0, min(1.0, a[k]))
    return a, fired


# ---------------------------------------------------------------------------------------------------------
# shared math
# ---------------------------------------------------------------------------------------------------------
def _cl(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def intensities(a: dict, b: dict, ctx: dict) -> dict:
    lim = b.get("limits", {})
    min_w = lim.get("min_width_cm", 60)
    comfort = max(1.33 * min_w, 120.0)
    cw = a.get("clear_width_cm")
    I = {
        "vertical": _cl((a.get("vertical_cm") or 0) / 15.0),
        "width": 0.0 if cw is None else _cl((comfort - cw) / comfort),
        "slope": _cl((a.get("slope_pct") or 0) / 8.33),
        "cross": _cl((a.get("cross_slope_pct") or 0) / 5.0),
        "noise": 0.0 if a.get("noise_db") is None else _cl((a["noise_db"] - 60) / 40.0),
        "water": _cl((a.get("water_cm") or 0) / 20.0),
        "wait": _cl((a.get("wait_s") or 0) / 120.0),
        "visibility": a.get("visibility_needed") or 0.0,
        "contrast": a.get("contrast_loss") or 0.0,
    }
    for k in ("roughness", "slip", "fall", "overhead", "glare", "flicker", "air", "heat", "cold", "crowd",
              "vehicle", "animal", "electric", "cognitive", "effort"):
        I[k] = _cl(a.get(k) or 0.0)
    return I


def unseen_sighted(a: dict, b: dict, ctx: dict) -> float:
    """chance a sighted walker misses a hazard that has to be seen (darkness, fog, contrast)."""
    env = max(ctx["_vis_env"], a.get("contrast_loss") or 0.0)
    return _cl((a.get("visibility_needed") or 0) * b["sensitivity"]["visibility"] * (0.25 + 0.75 * env) * 1.5)


def core(a, b, ctx, sec_mult=None, risk_mult=None, skip_sec=()):
    sens = b["sensitivity"]
    I = intensities(a, b, ctx)
    sm, rm = sec_mult or {}, risk_mult or {}
    secs, risks = {}, {}
    for ax, scale in SEC.items():
        if ax in skip_sec:
            continue
        v = sens.get(ax, 0) * I.get(ax, 0) * scale * sm.get(ax, 1.0)
        if v > 0:
            secs[ax] = v
    run = a.get("run_m")
    if run and "slope" in secs:
        secs["slope"] *= min(1.0, run / 20.0)  # short ramps cost little time (ASSUMPTION: 20 m = full)
    detour = a.get("detour_m") or 0
    if detour:
        secs["detour"] = detour / b["speed_mps"] * sens.get("detour", 0.3)
    for ax, w in HAZ.items():
        r = _cl(sens.get(ax, 0) * I.get(ax, 0) * w * rm.get(ax, 1.0))
        if r > 0:
            risks[ax] = r
    return secs, risks


def common_terms(a, b, ctx, secs, risks, notes):
    """hermes cross-cutting needs: crossing time, rest spacing; plus relief from positive elements."""
    L = a.get("crossing_length_m")
    if L:
        startup = 2.5  # NCHRP 562: older pedestrians' start-up time 2.5 s (source NCHRP562_speeds)
        need = L / b["speed_mps"] + startup
        green = a.get("green_s")
        if green:
            if need > green:
                short = _cl((need - green) / green)
                risks["vehicle_stranded"] = _cl(0.6 * short * max(0.4, b["sensitivity"]["vehicle"]))
                secs["crossing_time"] = need - green
                notes.append(f"crossing time: needs {need:.0f} s at {b['speed_mps']} m/s for {L:.0f} m, green "
                             f"is {green:.0f} s (stranded {need - green:.0f} s)")
            else:
                notes.append(f"crossing time: needs {need:.0f} s, green {green:.0f} s, fits")
        else:
            exposure = _cl(need / 10.0, 0.5, 2.5)
            if "vehicle" in risks:
                risks["vehicle"] = _cl(risks["vehicle"] * exposure)
            notes.append(f"crossing time: {need:.0f} s exposed to traffic on an unsignalised {L:.0f} m crossing")
    gap = a.get("rest_gap_m")
    rest = b.get("rest_spacing_m")
    if gap and rest and gap > rest:
        deficit = gap / rest - 1
        secs["rest_spacing"] = min(300.0, deficit * 30.0)
        notes.append(f"rest spacing: {gap:.0f} m with no rest, leaf {b.get('hermes_id')} needs one every "
                     f"{rest} m (hermes ASSUMPTION A)")
    rel = a.get("relief") or 0
    benefit = 0.0
    if rel:
        s = b["sensitivity"]
        benefit = -rel * 30.0 * max(s.get("effort", 0), s.get("heat", 0), s.get("visibility", 0) * 0.5,
                                    s.get("cognitive", 0) * 0.5)
    return benefit


def hard_geometry(a, b, lim=None, notes=None, helper=False):
    """block reasons from geometry vs this leaf's hard limits."""
    lim = lim if lim is not None else b.get("limits", {})
    out = []
    cw = a.get("clear_width_cm")
    narrow = cw is not None and lim.get("min_width_cm") is not None and cw < lim["min_width_cm"]
    v = a.get("vertical_cm") or 0
    mv = lim.get("max_vertical_cm")
    if mv is not None and helper and lim.get("hand_propelled"):
        mv += 10  # ASSUMPTION: a helper can tip a chair over about 10 cm more (FU 4.19, 10.22)
    if mv is not None and v > mv and (a.get("spans_path") or narrow):
        out.append(f"level change {v:.0f} cm > {mv:g} cm limit and no way round "
                   f"({'covers the path' if a.get('spans_path') else f'{cw:.0f} cm left beside it'})")
    if narrow:
        out.append(f"clear width {cw:.0f} cm < {lim['min_width_cm']:g} cm")
    s = a.get("slope_pct") or 0
    if lim.get("max_slope_pct") is not None and s > lim["max_slope_pct"] + 1e-9:
        out.append(f"slope {s:.1f}% > {lim['max_slope_pct']:g}%")
    cs = a.get("cross_slope_pct") or 0
    if lim.get("max_cross_slope_pct") is not None and cs > lim["max_cross_slope_pct"] + 1e-9:
        out.append(f"cross slope {cs:.1f}% > {lim['max_cross_slope_pct']:g}%")
    w = a.get("water_cm") or 0
    if lim.get("max_water_cm") is not None and w > lim["max_water_cm"]:
        out.append(f"water {w:.0f} cm > {lim['max_water_cm']:g} cm")
    return out


def _seen_mult(u):
    return 0.3 + 1.7 * u


def _apply_seen(risks, a, b, u, axes=SEEN_AXES):
    sens = b["sensitivity"]
    I = intensities(a, b, {})
    for ax in axes:
        if ax in HAZ:
            r = _cl(sens.get(ax, 0) * I.get(ax, 0) * HAZ[ax] * _seen_mult(u))
            if r > 0:
                risks[ax] = r
            else:
                risks.pop(ax, None)


def _always_hazards(a, hard, risks):
    if (a.get("electric") or 0) >= 0.9:
        hard.append("live electricity in reach (never routed, FU 6.04)")
    if "never_route" in a.get("_tags", ()):
        hard.append("railway track is never a walking edge (FU 4.11, 8.10)")


# ---------------------------------------------------------------------------------------------------------
# ONE SCORING FUNCTION PER BODY CATEGORY
# each returns (hard_reasons, seconds_by_term, risk_by_term, notes, benefit_s)
# ---------------------------------------------------------------------------------------------------------
def score_wheeled(a, b, ctx):
    lim = b.get("limits", {})
    notes = []
    a = dict(a)
    if a.get("clear_width_cm") is not None and (a.get("crowd") or 0) > 0.5:
        a["clear_width_cm"] = a["clear_width_cm"] - 30 * a["crowd"]  # crowd eats width (ASSUMPTION)
        notes.append("crowd narrows the usable width")
    hard = hard_geometry(a, b, notes=notes, helper=ctx.get("helper"))
    sm = {"roughness": 1.3 if lim.get("caster_small") else 1.0}
    if lim.get("hand_propelled") and "metal" in a.get("_tags", ()):
        sm["heat"] = 1.5
        if (a.get("heat") or 0) > 0:
            notes.append("hot metal handrims / railings burn hands")
    if ctx.get("temp_c"):
        sm["heat"] = sm.get("heat", 1.0) * (1 + max(0, ctx["temp_c"] - 35) / 10)
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult={"vehicle": 1.2}, skip_sec=("visibility",))
    _apply_seen(risks, a, b, unseen_sighted(a, b, ctx))
    if (a.get("roughness") or 0) >= 0.85 and (a.get("slip") or 0) >= 0.5:
        hard.append("mud or loose surface: wheels sink (FU 6.17)")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_ambulant(a, b, ctx):
    notes = []
    hard = hard_geometry(a, b, helper=False)
    rm = {"fall": 1.2, "crowd": 1.3}
    sm = {}
    if ctx["weather"] in WET_WEATHER:
        rm["slip"] = 1.5
        sm["slip"] = 1.5
        notes.append("wet weather: slip risk up for aids and prostheses")
    if ctx.get("temp_c"):
        sm["heat"] = 1 + max(0, ctx["temp_c"] - 35) / 10
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult=rm, skip_sec=("visibility",))
    u = unseen_sighted(a, b, ctx)
    _apply_seen(risks, a, b, u)
    for ax in ("fall", "slip"):
        if ax in risks:
            risks[ax] = _cl(risks[ax] * rm.get(ax, 1.0))
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_visual(a, b, ctx):
    lim = b.get("limits", {})
    notes = []
    hard = []
    cane = lim.get("cane_skill", 0.3)
    found_by_cane = (a.get("cane_detectable") if a.get("cane_detectable") is not None else 1.0) * cane
    if lim.get("light_independent"):
        miss = 1.0  # no useful vision: day or night does not matter
    else:
        resid = lim.get("residual_day", 0.3)
        env = max(ctx["_vis_env"], a.get("contrast_loss") or 0.0) * lim.get("night_factor", 1.0)
        miss = _cl(resid + (1 - resid) * env)
    u = _cl((a.get("visibility_needed") or 0) * miss * (1 - 0.6 * found_by_cane))
    if (a.get("overhead") or 0) > 0:
        u_over = _cl(miss * (1 - (a.get("cane_detectable") or 0) * cane))
    else:
        u_over = 0.0
    rm = {}
    hearing = not lim.get("no_hearing")
    nd = a.get("noise_db")
    if hearing and nd and nd >= 75:
        rm["vehicle"] = 1 + (nd - 70) / 40.0
        notes.append(f"noise {nd:.0f} dB masks traffic sound used to cross")
    if not hearing:
        rm["vehicle"] = 1.5
    if "silent_vehicle" in a.get("_tags", ()):
        rm["vehicle"] = rm.get("vehicle", 1.0) * 1.4
        notes.append("silent vehicles cannot be heard")
    spans = bool(a.get("spans_path"))
    # point hazards: stepping round them costs little time once announced; the cost is risk
    skip = ("vertical", "width", "roughness", "fall", "visibility") if not spans else ()
    secs, risks = core(a, b, ctx, risk_mult=rm, skip_sec=skip)
    if not spans:
        secs["slow_down"] = 6.0 * u
        # a fixed object standing in the walking line (pole, box, bollard, cart) is found by cane CONTACT, not
        # avoided: the contact is the hazard (impact, losing the line) and passing it costs a trail-around.
        # Without this term a mid-path pole scored "none" for a white-cane user (map review 2026-10-25).
        # ASSUMPTION: weights 0.4 risk / 12 s at full contact; guide dogs steer round most of it (dog_avoids).
        if a.get("clear_width_cm") is not None and (a.get("visibility_needed") or 0) >= 0.3:
            contact = _cl(miss * (a["visibility_needed"]) * max(0.5, b["sensitivity"].get("visibility", 0.5)))
            if lim.get("dog_avoids") or "guide dog" in str(b.get("aid", "")):
                contact *= 0.4
            if contact > 0:
                risks["collision"] = _cl(0.4 * contact)
                secs["find_and_pass"] = 12.0 * contact
    _apply_seen(risks, a, b, u, axes=("fall", "vertical", "slip", "animal"))
    if u_over:
        I = intensities(a, b, ctx)
        risks["overhead"] = _cl(b["sensitivity"]["overhead"] * I["overhead"] * HAZ["overhead"] * _seen_mult(u_over))
        notes.append("head-height object: a long cane passes under it")
    if "signal" in a.get("_tags", ()) and "clear" not in a.get("_tags", ()):
        secs["no_audible_signal"] = 20.0 * b["sensitivity"]["cognitive"]
    if "tactile" in a.get("_tags", ()) and (a.get("cognitive") or 0) > 0.3:
        risks["misleading_tactile"] = 0.3
        notes.append("tactile paving that misleads (IRC:103 Fig. 31 case, FU 1.29)")
    if (a.get("fall") or 0) >= 0.9 and u > 0.5:
        hard.append("deep open drop that cannot be seen or reliably found with a cane")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    if "tactile" in a.get("_tags", ()) and "clear" in a.get("_tags", ()):
        ben -= 30.0
    return hard, secs, risks, notes, ben


def score_hearing(a, b, ctx):
    lim = b.get("limits", {})
    notes = []
    rm = {}
    tags = a.get("_tags", ())
    if lim.get("no_hearing") and ({"road_walk", "vehicle", "silent_vehicle", "footpath_riding"} & set(tags)):
        rm["vehicle"] = 1.6
        notes.append("cannot hear vehicles from behind (FU 10.16)")
    if lim.get("partial_hearing") and (a.get("noise_db") or 0) >= 80:
        notes.append("hearing aid: loud noise is painful and drowns speech")
    if lim.get("cannot_call_for_help") and ({"isolated", "crime", "harassment"} & set(tags)):
        rm["crowd"] = 1.2
        notes.append("cannot easily call out for help")
    hard = hard_geometry(a, b)
    secs, risks = core(a, b, ctx, risk_mult=rm, skip_sec=("visibility",))
    _apply_seen(risks, a, b, unseen_sighted(a, b, ctx))
    if "crowd" in tags and (a.get("crowd") or 0) > 0.8:
        notes.append("public announcements and shouted warnings in a crush are not heard")
        risks["crowd"] = _cl(risks.get("crowd", 0) + 0.1)
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_cognitive(a, b, ctx):
    lim = b.get("limits", {})
    notes = []
    hard = hard_geometry(a, b)
    crowd = a.get("crowd") or 0
    sm = {"cognitive": 1 + crowd, "crowd": 1.2}
    rm = {"vehicle": 1.2 if b["sensitivity"]["cognitive"] >= 0.8 else 1.0}
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult=rm, skip_sec=("visibility",))
    _apply_seen(risks, a, b, unseen_sighted(a, b, ctx))
    nd = a.get("noise_db")
    if lim.get("max_noise_db") and nd and nd >= lim["max_noise_db"]:
        hard.append(f"noise {nd:.0f} dB >= {lim['max_noise_db']} dB sensory limit (ASSUMPTION)")
    if lim.get("max_flicker") and (a.get("flicker") or 0) >= lim["max_flicker"]:
        hard.append(f"flashing light {a['flicker']:.2f} >= {lim['max_flicker']} (seizure trigger, ASSUMPTION)")
    if "complex" in a.get("_tags", ()) or "signage" in a.get("_tags", ()):
        notes.append("decision point: pictograms and voice guidance help (hermes C1.1, C1.7)")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_elderly(a, b, ctx):
    notes = []
    hard = hard_geometry(a, b)
    rm = {"fall": 1.3, "slip": 1.3}  # a fall costs more: hip fracture (ASSUMPTION)
    sm = {}
    if ctx["weather"] in WET_WEATHER:
        rm["slip"] = 2.0
    if ctx.get("temp_c"):
        sm["heat"] = 1 + max(0, ctx["temp_c"] - 35) / 8
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult=rm, skip_sec=("visibility",))
    u = unseen_sighted(a, b, ctx)
    _apply_seen(risks, a, b, u)
    for ax in ("fall", "slip"):
        if ax in risks:
            risks[ax] = _cl(risks[ax] * rm[ax])
    if u > 0.3:
        notes.append("older eyes need more light and contrast")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_systemic(a, b, ctx):
    lim = b.get("limits", {})
    notes = []
    hard = hard_geometry(a, b)
    sm, rm = {}, {}
    aqi = ctx.get("aqi")
    if aqi:
        f = 1 + max(0, aqi - 100) / 300.0
        sm["air"] = rm["air"] = f
        notes.append(f"AQI {aqi}: CPCB health statement band applies")
    if ctx.get("temp_c"):
        sm["heat"] = rm["heat"] = 1 + max(0, ctx["temp_c"] - 35) / 8
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult=rm, skip_sec=("visibility",))
    _apply_seen(risks, a, b, unseen_sighted(a, b, ctx))
    air_eff = (a.get("air") or 0) * sm.get("air", 1.0)
    if lim.get("max_air") and air_eff >= lim["max_air"]:
        hard.append(f"air burden {air_eff:.2f} at or above the leaf limit {lim['max_air']} "
                    "(CPCB severe band: serious impact on lung/heart disease)")
    heat_eff = (a.get("heat") or 0) * sm.get("heat", 1.0)
    if lim.get("max_heat") and heat_eff >= lim["max_heat"]:
        hard.append(f"heat {heat_eff:.2f} at or above the leaf limit {lim['max_heat']} (IMD heat wave bands)")
    if lim.get("max_effort") and (a.get("effort") or 0) >= lim["max_effort"]:
        hard.append(f"exertion {a['effort']:.2f} >= {lim['max_effort']} (ASSUMPTION)")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


def score_situational(a, b, ctx):
    mode = b.get("limits", {}).get("mode", "adult")
    if mode == "wheeled":
        hard, secs, risks, notes, ben = score_wheeled(a, b, ctx)
        if b["id"] == "pram_stroller" and (a.get("heat") or a.get("air")):
            notes.append("the child in the pram sits at exhaust and hot-surface height")
            secs["child_exposure"] = 20.0 * max(a.get("heat") or 0, a.get("air") or 0)
        return hard, secs, risks, notes, ben
    if mode == "ambulant":
        return score_ambulant(a, b, ctx)
    notes = []
    hard = hard_geometry(a, b)
    rm, sm = {}, {}
    if mode == "child":
        rm = {"vehicle": 1.5, "fall": 1.3, "animal": 1.5}
        if (a.get("fall") or 0) >= 0.95 and (a.get("vertical_cm") or 0) >= 60:
            hard.append("deep open hole or drain: children fall in and drown (FU 2.08, 2.10, S11, S42)")
        if "vehicle" in a.get("_tags", ()) or "road_walk" in a.get("_tags", ()):
            notes.append("low eye height: drivers do not see a child behind parked vehicles")
        if "dog" in a.get("_tags", ()):
            notes.append("dog bites: children are the most bitten (S143)")
    elif mode == "pregnant":
        rm = {"slip": 1.4, "fall": 1.4, "heat": 1.3}
        if ctx.get("temp_c"):
            sm["heat"] = 1 + max(0, ctx["temp_c"] - 35) / 8
    secs, risks = core(a, b, ctx, sec_mult=sm, risk_mult=rm, skip_sec=("visibility",))
    _apply_seen(risks, a, b, unseen_sighted(a, b, ctx))
    for ax, m in rm.items():
        if ax in risks and ax in SEEN_AXES:
            risks[ax] = _cl(risks[ax] * m)
    lim = b.get("limits", {})
    if lim.get("max_air") and (a.get("air") or 0) >= lim["max_air"]:
        hard.append(f"air burden {a['air']:.2f} >= {lim['max_air']} (CPCB severe band, ASSUMPTION for pregnancy)")
    _always_hazards(a, hard, risks)
    ben = common_terms(a, b, ctx, secs, risks, notes)
    return hard, secs, risks, notes, ben


SCORERS = {"wheeled": score_wheeled, "ambulant": score_ambulant, "visual": score_visual,
           "hearing": score_hearing, "cognitive": score_cognitive, "elderly": score_elderly,
           "systemic": score_systemic, "situational": score_situational}


# ---------------------------------------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------------------------------------
def _resolve(el_in):
    if isinstance(el_in, str):
        return element(el_in), {}, 1.0
    eid = el_in.get("id") or el_in.get("element")
    base = element(eid)
    return base, dict(el_in.get("attrs") or {}), float(el_in.get("confidence", 1.0))


def _score_one(el, attrs, ctx, b, p, pwhy, fired):
    a = dict(attrs)
    a["_tags"] = tuple(el["tags"])
    hard, secs, risks, notes, benefit = SCORERS[b["scorer"]](a, b, ctx)
    seconds = sum(secs.values()) * p
    risk = (1 - math.prod(1 - r for r in risks.values())) * p if risks else 0.0
    if hard and p >= BLOCK_P:
        verdict = "block"
    elif risk >= BLOCK_RISK and p >= BLOCK_P:
        verdict = "block"
    elif hard:
        seconds += 600 * p  # would block, but presence is uncertain: soft cost like costs.py soft_block_cost_s
        verdict = "cost"
    elif seconds >= COST_S:
        verdict = "cost"
    elif risk >= COST_RISK and attrs.get("spans_path"):
        verdict = "cost"
    elif risk >= WARN_RISK or seconds >= WARN_S:
        verdict = "warn"
    else:
        verdict = "none"
    top_s = sorted(secs.items(), key=lambda kv: -kv[1])[:3]
    top_r = sorted(risks.items(), key=lambda kv: -kv[1])[:3]
    parts = []
    if hard:
        parts.append("BLOCK: " + "; ".join(hard))
    if top_s and seconds >= 1:
        parts.append("time: " + ", ".join(f"{AXIS_LABEL.get(k, k.replace('_', ' '))} +{v * p:.0f} s" for k, v in top_s if v * p >= 0.5))
    if top_r and risk >= 0.05:
        parts.append("risk: " + ", ".join(f"{AXIS_LABEL.get(k, k.replace('_', ' '))} {v:.2f}" for k, v in top_r))
    parts += notes
    if fired:
        parts.append("combination: " + "; ".join(r["reason"] for r in fired))
    if benefit < 0 and verdict == "none":
        parts.append(f"helps this body (about {-benefit:.0f} s easier)")
    reason = (f"{b['name']} x {el['name']}: {verdict}. " + ". ".join(x for x in parts if x)
              + f". Presence {p:.2f} ({pwhy}).")
    return {"verdict": verdict, "seconds": round(seconds, 1), "risk": round(min(1.0, risk), 3),
            "benefit_s": round(benefit, 1), "reason": reason, "element": el["id"], "body": b["id"],
            "scorer": b["scorer"], "presence": p, "hard": hard,
            "terms_s": {k: round(v * p, 1) for k, v in secs.items()},
            "terms_risk": {k: round(v, 3) for k, v in risks.items()},
            "rules_fired": [r["id"] for r in fired], "creates": [r["creates"] for r in fired if r["creates"]]}


def impact(el_in, context: dict | None, body_id: str) -> dict:
    """element instance x context x body leaf -> verdict, seconds, risk 0-1, reason."""
    el, over, conf = _resolve(el_in)
    b = body(body_id)
    ctx = norm_context(context)
    attrs = dict(el["attrs"])
    attrs.update(over)
    attrs, fired = apply_interactions(el, attrs, ctx, b)
    p, pwhy = presence(el, ctx, conf)
    res = _score_one(el, attrs, ctx, b, p, pwhy, fired)
    # compounds created by the combination are scored too; the worst one wins (same presence)
    for cid in dict.fromkeys(res["creates"]):
        cel = element(cid)
        cattrs = dict(cel["attrs"])
        for k in ("vertical_cm", "clear_width_cm"):  # keep the measured geometry of the real instance
            if over.get(k) is not None:
                cattrs[k] = over[k]
        cr = _score_one(cel, cattrs, ctx, b, p, pwhy, [])
        worse = (RANK[cr["verdict"]], cr["risk"]) > (RANK[res["verdict"]], res["risk"])
        if worse:
            cr["seconds"] = max(cr["seconds"], res["seconds"])
            cr["risk"] = max(cr["risk"], res["risk"])
            cr["reason"] = (f"{b['name']} x {el['name']} -> {cel['name']} (combination: "
                            + "; ".join(r["reason"] for r in fired if r["creates"] == cid) + "): "
                            + cr["reason"].split(": ", 1)[1])
            cr["element"] = el["id"]
            cr["compound"] = cid
            cr["hard"] = list(dict.fromkeys(res["hard"] + cr["hard"]))
            cr["base_terms_s"] = res["terms_s"]
            cr["rules_fired"] = res["rules_fired"]
            cr["creates"] = res["creates"]
            res = cr
    return res


def route_penalty_s(res: dict, b: dict | None = None) -> float:
    """seconds a router adds for a non-blocking result: time + risk x the leaf's risk penalty."""
    b = b or body(res["body"])
    return max(0.0, res["seconds"]) + res["risk"] * float(b.get("risk_penalty_s", 300))


def bodies_by_scorer() -> dict:
    out = {}
    for b in data()["body_list"]:
        out.setdefault(b["scorer"], []).append(b["id"])
    return out
