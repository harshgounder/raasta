import datetime as dt
import math

from conftest import LAT0, LON0

from hroute import attach as A
from hroute import routing as R
from hroute.config import cfg
from hroute.costs import barrier_effect, p_present, segment_cost

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
LEAVE = dt.datetime(2026, 10, 25, 9, 0, tzinfo=IST)
M_LAT = 1 / 110_800  # degrees per metre (approx at 27 N)


def _main_rd_sidewalks(net):
    return {s["side"]: s for s in net.segments.values()
            if s["kind"] == "sidewalk" and (s["parent_road"] or {}).get("name") == "Main Rd"
            and net.to_lonlat(*s["geom"].interpolate(0.5, normalized=True).coords[0])[0] < LON0 + 0.001}


# ---------------------------------------------------------------- network
def test_network_has_generated_sidewalks_both_sides_and_crossings(net):
    sw = _main_rd_sidewalks(net)
    assert set(sw) == {"L", "R"}
    assert all(s["source"] == "generated" for s in sw.values())
    # L of a west->east road is the north side
    n_lat = net.to_lonlat(*sw["L"]["geom"].interpolate(0.5, normalized=True).coords[0])[1]
    s_lat = net.to_lonlat(*sw["R"]["geom"].interpolate(0.5, normalized=True).coords[0])[1]
    assert n_lat > LAT0 > s_lat
    kinds = {s["kind"] for s in net.segments.values()}
    assert {"sidewalk", "crossing", "steps", "footway", "link"} <= kinds
    # at a square junction the two footpaths of a block corner meet in one shared node,
    # so the graph is connected without any stitched connector
    assert "connector" not in kinds
    crossings = [s for s in net.segments.values() if s["kind"] == "crossing"]
    assert crossings and all(s["crossing"] == "generated" for s in crossings)
    steps = [s for s in net.segments.values() if s["kind"] == "steps"]
    assert steps[0]["source"] == "osm" and steps[0]["evidence"][0]["type"] == "steps"
    for s in net.segments.values():
        for k in ("id", "geom", "length_m", "side", "parent_road", "source", "evidence"):
            assert k in s
    assert net.stats()["components"] == 1


# ---------------------------------------------------------------- attachment
def _wrong_side_record(**kw):
    rec = {"id": "t-wrong-side", "type": "pole_obstruction", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005,
           "heading": 90.0, "gps_error_m": 3.0, "confidence": 0.9, "status": "ACCEPT",
           "observed_at": "2026-10-20T10:00:00+05:30", "source": "test"}
    rec.update(kw)
    return rec


def test_attach_wrong_side_uses_side_hint(net):
    """Camera GPS sits on the north footpath, but the photo shows the pole on the RIGHT footpath
    while looking east. Right of an eastbound view = south side. Must attach south, not nearest."""
    sw = _main_rd_sidewalks(net)
    res = A.attach(net, _wrong_side_record(side_hint="right"))
    assert res["status"] == "ACCEPT", res
    assert res["segment_id"] == sw["R"]["id"]
    assert res["p"] >= 0.7
    assert any(e["id"] == "t-wrong-side" for e in net.segments[sw["R"]["id"]]["evidence"])
    assert not any(e.get("id") == "t-wrong-side" for e in net.segments[sw["L"]["id"]]["evidence"])


def test_attach_without_side_hint_does_not_claim_far_side(net):
    sw = _main_rd_sidewalks(net)
    res = A.attach(net, _wrong_side_record(id="t-nohint"), commit=False)
    assert res["segment_id"] != sw["R"]["id"]
    ps = {c["segment_id"]: c["p"] for c in res["candidates"]}
    assert ps[sw["L"]["id"]] > ps[sw["R"]["id"]]


def test_attach_abstains_when_ambiguous_or_far(net):
    far = A.attach(net, {"type": "pothole", "lat": LAT0 + 0.01, "lon": LON0, "source": "test"})
    assert far["status"] == "ABSTAIN" and far["segment_id"] is None
    # detector itself abstained: never attached, candidates kept
    ab = A.attach(net, _wrong_side_record(id="t-abstain", side_hint="right", status="ABSTAIN"))
    assert ab["status"] == "ABSTAIN" and ab["candidates"]
    assert not any(e.get("id") == "t-abstain" for s in net.segments.values() for e in s["evidence"])


# ---------------------------------------------------------------- profile rules
def _ev(**kw):
    e = {"status": "ACCEPT", "confidence": 0.9, "permanence": "permanent", "source": "test"}
    e.update(kw)
    return e


def test_steps_block_wheelchair_not_walker():
    ev = _ev(type="steps")
    assert barrier_effect(ev, "manual_wheelchair", LEAVE)["block"]
    assert barrier_effect(ev, "power_wheelchair", LEAVE)["block"]
    w = barrier_effect(ev, "default_walker", LEAVE)
    assert not w["block"] and w["cost_s"] > 0


def test_kerb_height_rule():
    low = barrier_effect(_ev(type="missing_kerb_ramp", height_cm=1.5), "manual_wheelchair", LEAVE)
    high = barrier_effect(_ev(type="missing_kerb_ramp", height_cm=12), "manual_wheelchair", LEAVE)
    unknown = barrier_effect(_ev(type="missing_kerb_ramp"), "manual_wheelchair", LEAVE)
    pram = barrier_effect(_ev(type="missing_kerb_ramp", height_cm=12), "pram", LEAVE)
    assert not low["block"] and low["cost_s"] > 0
    assert high["block"] and "12 cm > 2 cm" in high["why"]
    assert unknown["block"] and "not measured" in unknown["why"]
    assert not pram["block"]


def test_slope_uses_stricter_standard_for_wheelchairs_and_explains_both():
    ev = _ev(type="steep_slope", slope_pct=7.5)  # 1:13, between IRC 1:15 and MoHUA 1:12
    man = barrier_effect(ev, "manual_wheelchair", LEAVE)
    pw = barrier_effect(ev, "power_wheelchair", LEAVE)  # fix 8: power chairs also use the stricter 1:15
    walker = barrier_effect(ev, "walker_elderly", LEAVE)
    assert man["block"] and pw["block"] and not walker["block"] and walker["cost_s"] > 0
    assert "MoHUA" in man["why"] and "IRC:103-2022" in man["why"]
    assert "met" in man["why"] and "exceeded" in man["why"]
    ok = barrier_effect(_ev(type="steep_slope", slope_pct=6.0), "power_wheelchair", LEAVE)
    assert not ok["block"]


def test_temporary_vendor_depends_on_leave_time():
    ev = _ev(type="vendor", permanence="temporary", half_life_h=6, observed_at="2026-10-24T18:30:00+05:30")
    morning = p_present(ev, dt.datetime(2026, 10, 25, 6, 0, tzinfo=IST))[0]
    evening = p_present(ev, dt.datetime(2026, 10, 25, 18, 30, tzinfo=IST))[0]
    soon = p_present(ev, dt.datetime(2026, 10, 24, 19, 0, tzinfo=IST))[0]
    assert morning < evening <= soon
    assert morning < 0.2


def test_date_only_observation_has_no_hour_ratio():
    """fix 4: a YYYY-MM-DD date (Project Sidewalk) is not midnight; the hour curve ratio must be 1."""
    leave = dt.datetime(2026, 10, 25, 19, 0, tzinfo=IST)
    d_only = p_present(_ev(type="parked_vehicle", permanence="temporary", observed_at="2025-10-15"), leave)
    midnight = p_present(_ev(type="parked_vehicle", permanence="temporary",
                             observed_at="2025-10-15T00:00:00+05:30"), leave)
    rec = 0.35  # recurrence for parked_vehicle in assumptions.json
    assert abs(d_only[0] - 0.9 * rec) < 1e-6 and "no time of day" in d_only[1]
    assert midnight[0] > d_only[0] * 2  # the old behaviour inflated it by the hour-curve ratio


def test_p_attach_scales_barrier_probability():
    """fix 2: effective p = p_present x p_attach."""
    full = barrier_effect(_ev(type="pothole", p_attach=1.0), "manual_wheelchair", LEAVE)
    half = barrier_effect(_ev(type="pothole", p_attach=0.75), "manual_wheelchair", LEAVE)
    assert abs(half["p"] - 0.75 * full["p"]) < 1e-3 and half["cost_s"] < full["cost_s"]
    # a blocking type below block_p after p_attach becomes a soft cost, not a block
    soft = barrier_effect(_ev(type="steps", confidence=0.9, p_attach=0.5), "manual_wheelchair", LEAVE)
    assert not soft["block"] and soft["cost_s"] > 0


def _seg(kind="sidewalk", length=100.0, evidence=None):
    return {"id": "x", "kind": kind, "length_m": length, "evidence": evidence or []}


def test_uncertainty_formula_and_median_cost():
    """fixes 1+2: p = 1-(1-p100)^(len/100), cost = -ln(1-min(p,.99)) x penalty; medians use per_100m 1.0."""
    pen = cfg()["profiles"]["default_walker"]["unknown_penalty_s"]
    c = segment_cost(_seg("sidewalk", 100), "default_walker", LEAVE)
    p100 = cfg()["unknown_prior"]["per_100m"]["sidewalk"]
    assert abs(c["uncertainty_s"] - (-math.log(1 - p100) * pen)) < 1e-6
    c2 = segment_cost(_seg("sidewalk", 200), "default_walker", LEAVE)
    assert abs(c2["p_unseen"] - (1 - (1 - p100) ** 2)) < 1e-3
    med = segment_cost(_seg("median", 30), "default_walker", LEAVE)
    side = segment_cost(_seg("sidewalk", 30), "default_walker", LEAVE)
    assert med["uncertainty_s"] >= -math.log(0.01) * pen - 1e-6 > side["uncertainty_s"]
    for prof in ("manual_wheelchair", "power_wheelchair", "pram"):
        assert segment_cost(_seg("median", 30), prof, LEAVE)["blocked"]
    crossing = segment_cost(_seg("crossing", 10), "default_walker", LEAVE)
    assert abs(crossing["uncertainty_s"] - (-math.log(1 - 0.6) * pen)) < 1e-6


def test_barrier_never_makes_segment_cheaper_and_clear_only_covers_25m():
    """fix 3"""
    base = segment_cost(_seg("sidewalk", 100), "manual_wheelchair", LEAVE)
    bar = segment_cost(_seg("sidewalk", 100, [_ev(type="pothole", source="photo", at_m=50)]),
                       "manual_wheelchair", LEAVE)
    assert bar["weight"] > base["weight"] and bar["uncertainty_s"] == base["uncertainty_s"]
    assert bar["tier"] == "known_barrier"
    clear = segment_cost(_seg("sidewalk", 100, [_ev(type="clear", source="photo", at_m=50)]),
                         "manual_wheelchair", LEAVE)
    p100 = cfg()["unknown_prior"]["per_100m"]["sidewalk"]
    assert clear["tier"] == "known_clear"
    assert abs(clear["p_unseen"] - (1 - (1 - p100) ** 0.5)) < 1e-3  # 50 of 100 m still unseen
    assert 0 < clear["uncertainty_s"] < base["uncertainty_s"]


def test_same_type_labels_are_deduplicated():
    """fix 5: ten labels of one parked car within 5 m cost like one; two far clusters combine 1-prod(1-p)."""
    one = segment_cost(_seg("sidewalk", 100, [_ev(type="pothole", at_m=40)]), "default_walker", LEAVE)
    many = segment_cost(_seg("sidewalk", 100, [_ev(type="pothole", at_m=40 + i * 0.4, id=f"p{i}")
                                               for i in range(10)]), "default_walker", LEAVE)
    assert abs(many["delay_s"] - one["delay_s"]) < 1e-6
    assert len(many["hits"]) == 1 and many["hits"][0]["labels_in_cluster"] == 10
    two = segment_cost(_seg("sidewalk", 100, [_ev(type="pothole", at_m=10, id="a"),
                                              _ev(type="pothole", at_m=80, id="b")]), "default_walker", LEAVE)
    unit = cfg()["barriers"]["pothole"]["default_walker"]["cost_s"]
    assert abs(two["delay_s"] - (1 - (1 - 0.9) ** 2) * unit) < 1e-6 <= unit - two["delay_s"]


def test_unknown_segment_has_uncertainty_cost(net):
    sw = _main_rd_sidewalks(net)["L"]
    c = segment_cost(sw, "manual_wheelchair", LEAVE)
    assert c["tier"] == "unknown" and c["uncertainty_s"] > 0 and not c["blocked"]


def test_far_side_link_is_a_crossing(net):
    """fix 11: an OSM way meeting a road links to the near corner; reaching the far side is kind=crossing."""
    at3 = [s for s in net.segments.values() if (s["note"] or "").startswith("OSM way meets road at node 3")]
    assert {s["kind"] for s in at3} == {"link", "crossing"}


# ---------------------------------------------------------------- routing
def test_unknown_counting_and_summary(net):
    r = R.route(net, (LAT0, LON0), (LAT0 + 0.001, LON0 + 0.001), "manual_wheelchair", LEAVE.isoformat())
    acc = r["accessible"]
    assert r["status"] == "ok"
    assert acc["known_barrier"] == acc["known_clear"] == 0
    assert acc["unknown"] + acc["osm_tag"] == acc["segments"] > 0
    assert f"{acc['segments']} segments: 0 with a known barrier, 0 seen clear" in acc["summary"]
    assert "no photo or volunteer-label evidence" in acc["summary"]
    assert "snapped" in r["summary"]
    assert "safe" not in r["summary"].lower()


def test_evidence_counting_and_volunteer_wording(net):
    sw = _main_rd_sidewalks(net)
    A.attach(net, _wrong_side_record(id="t-ps", type="pothole", side_hint="right", source="project_sidewalk",
                                     observed_at="2026-10-20"))
    r = R.route(net, (LAT0 - 5 * M_LAT, LON0), (LAT0 - 5 * M_LAT, LON0 + 0.0009), "default_walker",
                LEAVE.isoformat())
    acc = r["accessible"]
    assert sw["R"]["id"] in acc["segment_ids"]
    assert acc["known_barrier"] >= 1 and acc["oldest_evidence"] == "2026-10-20"
    assert "labelled by Project Sidewalk volunteers" in acc["summary"]
    assert "verified by photo" not in acc["summary"]


def test_snap_too_far_status(net):
    r = R.route(net, (LAT0 + 0.003, LON0), (LAT0, LON0 + 0.001), "default_walker", LEAVE.isoformat())
    assert r["status"] == "too_far" and r["shortest"] is None and "snapped" in r["summary"]


def test_bad_leave_time_raises(net):
    import pytest
    with pytest.raises(ValueError):
        R.route(net, (LAT0, LON0), (LAT0, LON0 + 0.001), "default_walker", "half past tea")


def test_blocked_for_profile_reports_blocking_barriers(net):
    # 7 is only reachable over the staircase 3=6
    end = (LAT0, LON0 + 0.004)
    r = R.route(net, (LAT0, LON0), end, "manual_wheelchair", LEAVE.isoformat())
    assert r["status"] == "blocked_for_profile"
    assert r["accessible"] is None and r["least_blocked"]["geometry"]["coordinates"]
    assert any(b["type"] == "steps" for b in r["blocking_barriers"])
    assert "No route without a blocking barrier" in r["summary"]
    assert r["shortest"]["blocked_for_profile"] and r["shortest"]["blocking_count"] >= 1
    w = R.route(net, (LAT0, LON0), end, "default_walker", LEAVE.isoformat())
    assert w["status"] == "ok" and w["accessible"] is not None


def test_accessible_route_avoids_blocking_barrier(net):
    """Block the north footpath of Main Rd with an open drain; a wheelchair must cross to the south."""
    sw = _main_rd_sidewalks(net)
    A.attach(net, {"id": "drain", "type": "open_drain", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005,
                   "position": "barrier", "gps_error_m": 2, "source": "test", "observed_at": "2026-10-23"})
    assert any(e["id"] == "drain" for e in net.segments[sw["L"]["id"]]["evidence"])
    s, e = (LAT0 + 5 * M_LAT, LON0 + 0.00002), (LAT0 + 5 * M_LAT, LON0 + 0.00098)
    r = R.route(net, s, e, "manual_wheelchair", LEAVE.isoformat())
    assert r["shortest"]["blocked_for_profile"]
    assert sw["L"]["id"] in r["shortest"]["segment_ids"]
    assert r["status"] == "ok" and sw["L"]["id"] not in r["accessible"]["segment_ids"]
    assert r["accessible"]["length_m"] > r["shortest"]["length_m"]
    assert r["accessible"]["geometry"]["coordinates"]


def test_profile_and_leave_time_change_the_route(net):
    """fix 6: a vendor leaving 60 cm clear, seen the evening before, blocks a pram at 19:00 (p >= 0.5)
    but is only a soft cost at 08:00; a walker keeps the north footpath at both times."""
    sw = _main_rd_sidewalks(net)
    A.attach(net, {"id": "cart", "type": "vendor", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005,
                   "position": "barrier", "gps_error_m": 1.5, "confidence": 0.95, "clear_width_cm": 60,
                   "permanence": "temporary", "half_life_h": 6, "observed_at": "2026-10-24T19:00:00+05:30",
                   "source": "test"})
    s, e = (LAT0 + 5 * M_LAT, LON0 + 0.00002), (LAT0 + 5 * M_LAT, LON0 + 0.00098)
    eve = R.route(net, s, e, "pram", "2026-10-25T19:00:00+05:30")
    morn = R.route(net, s, e, "pram", "2026-10-25T08:00:00+05:30")
    walk = R.route(net, s, e, "default_walker", "2026-10-25T19:00:00+05:30")
    assert sw["L"]["id"] not in eve["accessible"]["segment_ids"]
    assert sw["L"]["id"] in morn["accessible"]["segment_ids"]
    assert sw["L"]["id"] in walk["accessible"]["segment_ids"]


def test_precompute_attach_all_rejects_without_aborting(net):
    """fix 9"""
    from hroute.cli import _attach_all
    out = _attach_all(net, [{"type": "pothole", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005, "source": "test"},
                            {"type": "unicorn", "lat": LAT0, "lon": LON0}, {"type": "steps"}])
    assert [o["status"] for o in out][1:] == ["REJECT", "REJECT"]
    assert out[0]["record"]["gps_error_m"] == 8.0  # the validated record, defaults filled


def test_route_reports_unknown_share_and_evidence_line_not_minutes(net):
    """hermes A/B: minutes is travel time only; uncertainty is a separate cost; unknown share in percent."""
    r = R.route(net, (LAT0, LON0), (LAT0 + 0.001, LON0 + 0.001), "manual_wheelchair", LEAVE.isoformat())
    acc = r["accessible"]
    assert "uncertainty_penalty_not_in_minutes" not in acc["minutes_detail"]
    assert abs(acc["minutes"] - sum(acc["minutes_detail"].values())) < 0.2
    assert acc["uncertainty_cost_s"] > 0 and 0 < acc["unknown_share_pct"] <= 100
    assert abs(acc["mapped_m"] + acc["estimated_m"] - acc["length_m"]) < 0.5
    assert acc["evidence_line"].endswith("0 barriers observed") and "m estimated" in acc["summary"]


def test_segment_id_override_places_without_probability(net):
    sid = _main_rd_sidewalks(net)["R"]["id"]
    res = A.attach(net, {"id": "given", "type": "pothole", "lat": LAT0, "lon": LON0, "segment_id": sid,
                         "source": "test"})
    assert res["status"] == "ACCEPT" and res["segment_id"] == sid and res["p"] == 1.0
    assert A.detach(net, "given") == 1
