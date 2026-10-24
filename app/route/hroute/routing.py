"""Shortest route vs accessible route per profile and leave time, with honest coverage counts."""
from __future__ import annotations

import datetime as dt

import networkx as nx
import numpy as np
from scipy.spatial import cKDTree

from .attach import IST, parse_time
from .config import PROFILES, cfg, clear_types, evidence_sources, source_class
from .costs import TIERS, age_text, segment_cost

BIG = 1e7


def _main_index(net):
    cache = getattr(net, "_ntree", None)
    if cache is None:
        g = net.graph
        comp = max(nx.connected_components(g), key=len)
        # never snap onto a node that only touches median segments (generated median sides are not
        # footpaths; starting there would make every wheelchair route look blocked)
        nodes = [n for n in comp
                 if any(net.segments[k]["kind"] != "median" for _, _, k in g.edges(n, keys=True))]
        cache = (cKDTree(np.array([net.nodes[n] for n in nodes])), nodes)
        net._ntree = cache
    return cache


def snap(net, lat, lon):
    x, y = net.to_xy(lat, lon)
    tree, nodes = _main_index(net)
    d, i = tree.query((x, y))
    return nodes[int(i)], float(d)


def _path_segments(g, path, keyw):
    out = []
    for a, b in zip(path, path[1:]):
        ks = g.get_edge_data(a, b)
        best = min(ks, key=lambda k: keyw(k))
        out.append((a, b, best))
    return out


def _geometry(net, segs):
    coords = []
    for a, b, sid in segs:
        s = net.segments[sid]
        c = net.line_lonlat(s["geom"])
        if s["u"] != a:
            c = c[::-1]
        if coords and coords[-1] == c[0]:
            c = c[1:]
        coords.extend(c)
    return {"type": "LineString", "coordinates": coords}


SNAP_MAX_M = 75.0


def describe(net, segs, profile, leave, kind, status="ok") -> dict:
    now = dt.datetime.now(IST)
    length = travel = delay = unc = 0.0
    counts = {t: 0 for t in TIERS}
    hits, blocks, dates, classes = [], [], [], set()
    what_if = False
    for a, b, sid in segs:
        s = net.segments[sid]
        c = segment_cost(s, profile, leave)
        length += s["length_m"]
        travel += c["travel_s"]
        delay += c["delay_s"]
        unc += c["uncertainty_s"]
        counts[c["tier"]] += 1
        what_if = what_if or c["what_if"]
        for h in c["hits"]:
            hits.append({**h, "segment_id": sid, "kind": s["kind"]})
        blocks += [{**h, "segment_id": sid} for h in c["blocks"]]
        for e in s["evidence"]:
            if e.get("source") in evidence_sources():
                classes.add(source_class(e.get("source")))
                t = parse_time(e.get("observed_at"))
                if t:
                    dates.append(t)
    n = len(segs)
    mapped_m = sum(net.segments[sid]["length_m"] for _, _, sid in segs if net.segments[sid]["source"] == "osm")
    unknown_m = sum(net.segments[sid]["length_m"] for _, _, sid in segs
                    if segment_cost(net.segments[sid], profile, leave)["tier"] == "unknown")
    observed = {e.get("id") for _, _, sid in segs for e in net.segments[sid]["evidence"]
                if e.get("source") in evidence_sources() and e.get("type") not in clear_types()
                and e.get("status", "ACCEPT") == "ACCEPT"}
    oldest = min(dates) if dates else None
    newest = max(dates) if dates else None
    plabel = cfg()["profiles"][profile]["label"]
    parts = [f"{n} segments: {counts['known_barrier']} with a known barrier",
             f"{counts['known_clear']} seen clear", f"{counts['osm_tag']} from OSM tags only",
             f"{counts['unknown']} unknown"]
    summary = ", ".join(parts)
    who = []
    if "photo" in classes:
        who.append("photos")
    if "volunteer_label" in classes:
        who.append("labelled by Project Sidewalk volunteers")
    if oldest:
        summary += f"; evidence {' and '.join(who)}, oldest {age_text(oldest, now)} ({oldest.date().isoformat()})"
    else:
        summary += "; no photo or volunteer-label evidence on this route"
    summary += (f"; {mapped_m:.0f} m mapped, {length - mapped_m:.0f} m estimated, "
                f"{len(observed)} barrier{'s' if len(observed) != 1 else ''} observed")
    if what_if:
        summary += "; includes WHAT-IF records (placed to demonstrate, not observed)"
    if blocks and kind == "shortest":
        summary = f"Blocked for {plabel.lower()} by {len(blocks)} barrier(s). " + summary
    out = {
        "kind": kind, "profile": profile, "profile_label": plabel, "status": status,
        "leave_time": leave.isoformat(), "length_m": round(length, 1),
        "minutes": round((travel + delay) / 60, 1),
        "minutes_detail": {"walk_or_roll": round(travel / 60, 1), "barrier_delay": round(delay / 60, 1)},
        "uncertainty_cost_s": round(unc, 1),
        "_uncertainty_cost_about": "routing penalty in cost seconds for unseen barriers; NOT travel time, never show as minutes",
        "unknown_m": round(unknown_m, 1), "unknown_share_pct": round(100 * unknown_m / length, 1) if length else 0.0,
        "mapped_m": round(mapped_m, 1), "estimated_m": round(length - mapped_m, 1),
        "barriers_observed": len(observed),
        "evidence_line": (f"{mapped_m:.0f} m mapped, {length - mapped_m:.0f} m estimated, "
                          f"{len(observed)} barrier{'s' if len(observed) != 1 else ''} observed"),
        "segments": n, **counts, "tiers": counts,
        "oldest_evidence": oldest.date().isoformat() if oldest else None,
        "newest_evidence": newest.date().isoformat() if newest else None,
        "barrier_count": len(hits), "blocking_count": len(blocks),
        "barriers": hits, "blocking": blocks, "blocked_for_profile": bool(blocks), "what_if": what_if,
        "summary": summary + ".", "segment_ids": [sid for _, _, sid in segs],
        "geometry": _geometry(net, segs),
    }
    return out


def route(net, start, end, profile="manual_wheelchair", leave_time=None) -> dict:
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}; allowed {PROFILES}")
    if leave_time not in (None, ""):
        leave = parse_time(leave_time)
        if leave is None:
            raise ValueError(f"bad leave_time {leave_time!r}; use ISO 8601, e.g. 2026-10-25T08:00:00+05:30")
    else:
        leave = dt.datetime.now(IST)
    g = net.graph
    s, ds = snap(net, *start)
    t, dt_ = snap(net, *end)
    memo = {}

    def cost(sid):
        if sid not in memo:
            memo[sid] = segment_cost(net.segments[sid], profile, leave)
        return memo[sid]

    def w_len(a, b, d):
        return min(net.segments[k]["length_m"] for k in d)

    def w_acc(a, b, d):
        ws = [cost(k)["weight"] for k in d]
        ws = [x for x in ws if x is not None]
        return min(ws) if ws else None

    def w_force(a, b, d):
        return min((cost(k)["weight"] if cost(k)["weight"] is not None
                    else BIG + net.segments[k]["length_m"]) for k in d)

    snap_txt = f"start snapped {ds:.0f} m, end {dt_:.0f} m to the network"
    res = {"start": {"lat": start[0], "lon": start[1], "snap_m": round(ds, 1), "node": s},
           "end": {"lat": end[0], "lon": end[1], "snap_m": round(dt_, 1), "node": t},
           "profile": profile, "leave_time": leave.isoformat(), "city": net.city, "snap_max_m": SNAP_MAX_M}
    if max(ds, dt_) > SNAP_MAX_M:
        res.update(status="too_far", shortest=None, accessible=None,
                   summary=f"Start or end is more than {SNAP_MAX_M:.0f} m from the footpath network ({snap_txt}).")
        return res
    if s == t:
        res.update(status="same_point", shortest=None, accessible=None,
                   summary=f"Start and end snap to the same network node ({snap_txt}).")
        return res
    try:
        p_short = nx.dijkstra_path(g, s, t, weight=w_len)
    except nx.NetworkXNoPath:
        res.update(status="no_path", shortest=None, accessible=None,
                   summary=f"No footpath connection at all ({snap_txt}).")
        return res
    short = describe(net, _path_segments(g, p_short, lambda k: net.segments[k]["length_m"]), profile, leave,
                     "shortest")
    res["shortest"] = short

    def kw(k):
        w = cost(k)["weight"]
        return w if w is not None else BIG

    try:
        p_acc = nx.dijkstra_path(g, s, t, weight=w_acc)
        acc = describe(net, _path_segments(g, p_acc, kw), profile, leave, "accessible")
        res["accessible"] = acc
        res["status"] = "ok"
        extra = acc["length_m"] - short["length_m"]
        if short["blocked_for_profile"]:
            lead = (f"Shortest route ({short['length_m']:.0f} m) is blocked for {acc['profile_label'].lower()}; "
                    f"accessible route is {acc['length_m']:.0f} m ({extra:+.0f} m), {acc['minutes']:.0f} min. ")
        elif acc["segment_ids"] == short["segment_ids"]:
            lead = f"Shortest route is also the best for {acc['profile_label'].lower()}. "
        else:
            lead = (f"Accessible route is {acc['length_m']:.0f} m ({extra:+.0f} m vs shortest), "
                    f"{acc['minutes']:.0f} min. ")
        res["summary"] = lead + acc["summary"][:-1] + f"; {snap_txt}."
    except nx.NetworkXNoPath:
        p_f = nx.dijkstra_path(g, s, t, weight=w_force)
        least = describe(net, _path_segments(g, p_f, kw), profile, leave, "least_blocked", status="blocked")
        res["accessible"] = None
        res["least_blocked"] = least
        res["status"] = "blocked_for_profile"
        bl = least["blocking"]
        kinds = ", ".join(sorted({b["type"].replace("_", " ") for b in bl}))
        res["blocking_barriers"] = bl
        res["summary"] = (f"No route without a blocking barrier for {cfg()['profiles'][profile]['label'].lower()}. "
                          f"The least-blocked path ({least['length_m']:.0f} m) still crosses {len(bl)} blocking "
                          f"barrier(s): {kinds}; {snap_txt}.")
    return res


def route_all_profiles(net, start, end, leave_time=None, profiles=None) -> dict:
    out = {}
    for p in profiles or PROFILES:
        out[p] = route(net, start, end, p, leave_time)
    return out
