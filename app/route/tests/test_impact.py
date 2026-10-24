"""ELEMENT x BODY impact engine: the same element weighs differently per body leaf, context matters,
combinations create compound elements, and the router adapter keeps the old path untouched."""
import datetime as dt
import json
import os
import threading

import pytest
from conftest import LAT0, LON0

from hroute import attach as A
from hroute import impact as I
from hroute import impact_adapter as IA
from hroute import routing as R
from hroute.costs import segment_cost

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
LEAVE = dt.datetime(2026, 10, 25, 9, 0, tzinfo=IST)
M_LAT = 1 / 110_800
DAY, NIGHT = {"hour": 11}, {"hour": 21}


def v(e, ctx, b):
    return I.impact(e, ctx, b)


# ------------------------------------------------------------------ the brief's examples
def test_same_pothole_four_bodies_four_verdicts():
    assert v("pothole", DAY, "mw_self")["verdict"] == "block"
    assert v("pothole", DAY, "walking_frame")["verdict"] == "cost"
    assert v("pothole", NIGHT, "low_vision_moderate")["verdict"] == "warn"
    assert v("pothole", DAY, "deaf")["verdict"] == "none"


def test_dust_costs_copd_not_wheelchair():
    assert v("construction_dust", DAY, "copd_asthma")["verdict"] == "cost"
    assert v("construction_dust", DAY, "mw_self")["verdict"] == "none"


def test_pothole_block_reason_names_limit_and_width():
    r = v("pothole", DAY, "mw_self")
    assert "8 cm > 2 cm" in r["reason"] and "80 cm left beside it" in r["reason"]


def test_one_scoring_function_per_category_and_every_leaf_has_one():
    assert set(I.SCORERS) == {"wheeled", "ambulant", "visual", "hearing", "cognitive", "elderly", "systemic",
                              "situational"}
    for b in I.data()["body_list"]:
        assert b["scorer"] in I.SCORERS
        assert set(b["sensitivity"]) >= {"vertical", "air", "noise", "vehicle", "crowd"}


# ------------------------------------------------------------------ hard limits per leaf
def test_kerb_power_chair_vs_step_climbing_chair():
    assert v("kerb_150_no_ramp", DAY, "pw_standard")["verdict"] == "block"
    assert v("kerb_150_no_ramp", DAY, "pw_step_climbing")["verdict"] != "block"  # S95 median 20 cm


def test_measured_low_kerb_does_not_block_attendant_chair():
    e = {"id": "kerb_150_no_ramp", "attrs": {"vertical_cm": 6}}
    assert v(e, DAY, "mw_attendant")["verdict"] != "block"
    assert v(e, DAY, "mw_self")["verdict"] == "block"


def test_helper_lifts_manual_chair_over_small_kerb():
    e = {"id": "kerb_150_no_ramp", "attrs": {"vertical_cm": 8}}
    assert v(e, DAY, "mw_self")["verdict"] == "block"
    assert v(e, {**DAY, "helper": True}, "mw_self")["verdict"] != "block"


def test_ramp_slope_irc_vs_hg():
    assert v("kerb_ramp_steep_1in10", DAY, "mw_self")["verdict"] == "block"        # > 1:15
    assert v("kerb_ramp_good", DAY, "mw_self")["verdict"] in ("none", "warn")      # 6% <= 6.67%
    assert v("kerb_ramp_steep_1in10", DAY, "mw_active_rigid")["verdict"] == "block"  # > 1:12
    assert v("running_slope_6", DAY, "mw_active_rigid")["verdict"] != "block"


def test_bollards_80cm_block_chair_and_pram_not_walker():
    assert v("bollards_narrow_80", DAY, "mw_self")["verdict"] == "block"
    assert v("bollards_narrow_80", DAY, "mobility_scooter")["verdict"] == "block"
    assert v("bollards_narrow_80", DAY, "no_impairment_adult")["verdict"] in ("none", "warn")


def test_steps_block_wheels_cost_crutches():
    assert v("steps_short_flight", DAY, "mw_self")["verdict"] == "block"
    assert v("steps_short_flight", DAY, "pram_stroller")["verdict"] == "block"
    assert v("steps_short_flight", DAY, "crutches_bilateral")["verdict"] in ("cost", "block")
    assert v("steps_short_flight", DAY, "deaf")["verdict"] in ("none", "warn")


# ------------------------------------------------------------------ sensory and cognitive leaves
def test_head_height_sign_blocks_cane_user_not_wheelchair():
    assert v("low_signboard", DAY, "blind_cane")["verdict"] == "block"
    assert v("low_signboard", DAY, "mw_self")["verdict"] == "none"
    # a guide dog steers round it
    assert I.RANK[v("low_signboard", DAY, "blind_guide_dog")["verdict"]] < I.RANK["block"]


def test_open_manhole_blocks_blind_and_child():
    assert v("open_manhole", DAY, "blind_cane")["verdict"] == "block"
    assert v("open_manhole", DAY, "child_5_12")["verdict"] == "block"


def test_loud_dj_blocks_autism_none_for_deaf():
    eve = {"hour": 20}
    assert v("loudspeaker_dj", eve, "autism_sensory")["verdict"] == "block"
    assert v("loudspeaker_dj", eve, "deaf")["verdict"] == "none"


def test_flashing_billboard_blocks_photosensitive_epilepsy_only():
    assert v("led_billboard_flashing", DAY, "epilepsy_photosensitive")["verdict"] == "block"
    assert v("led_billboard_flashing", DAY, "mw_self")["verdict"] in ("none", "warn")


def test_road_walk_worse_for_deaf_than_hearing_adult():
    d = v("no_footpath_road_walk", DAY, "deaf")
    a = v("no_footpath_road_walk", DAY, "no_impairment_adult")
    assert d["risk"] > a["risk"] and I.RANK[d["verdict"]] >= I.RANK["cost"]


def test_noise_masks_traffic_for_blind_walker():
    quiet = v({"id": "crossing_4plus_lanes", "attrs": {"noise_db": 55}}, DAY, "blind_cane")
    loud = v({"id": "crossing_4plus_lanes", "attrs": {"noise_db": 95}}, DAY, "blind_cane")
    assert loud["risk"] > quiet["risk"]


# ------------------------------------------------------------------ systemic and air
def test_severe_aqi_blocks_copd_and_cardiac_not_wheelchair():
    assert v("aqi_severe_450", DAY, "copd_asthma")["verdict"] == "block"
    assert v("aqi_severe_450", DAY, "cardiac")["verdict"] == "block"
    assert v("aqi_severe_450", DAY, "mw_self")["verdict"] == "none"
    assert "CPCB" in v("aqi_severe_450", DAY, "copd_asthma")["reason"]


def test_context_aqi_raises_dust_cost_for_copd():
    lo = v("road_dust_resuspension", {**DAY, "aqi": 80}, "copd_asthma")
    hi = v("road_dust_resuspension", {**DAY, "aqi": 380}, "copd_asthma")
    assert hi["seconds"] > lo["seconds"] and "aqi_x_airborne" in hi["rules_fired"]


# ------------------------------------------------------------------ combinations
def test_rain_turns_pothole_into_hidden_hole():
    r = v("pothole", {**DAY, "weather": "heavy_rain"}, "low_vision_moderate")
    assert r.get("compound") == "hidden_hole_under_water" and r["verdict"] == "block"
    assert "rain_x_hole_hidden" in r["rules_fired"]


def test_night_no_light_open_drain_is_fall_hazard_for_older_walker():
    day = v("open_drain_parallel", DAY, "older_70_79")
    night = v("open_drain_parallel", {"hour": 22, "light": "night_dark"}, "older_70_79")
    assert "night_x_dark_x_drain" in night["rules_fired"]
    assert night["risk"] >= day["risk"] and night["verdict"] == "block"


def test_heat_makes_metal_railing_cost_for_hand_propelled_chair():
    cool = v("guardrail_continuous", {**DAY, "temp_c": 30}, "mw_self")
    hot = v("guardrail_continuous", {**DAY, "temp_c": 45}, "mw_self")
    assert "heat_x_metal" in hot["rules_fired"] and hot["seconds"] > cool["seconds"]


def test_wet_granite_slip_for_elderly():
    dry = v("polished_granite", DAY, "older_80_frail")
    wet = v("polished_granite", {**DAY, "weather": "rain"}, "older_80_frail")
    assert wet["risk"] > dry["risk"] and I.RANK[wet["verdict"]] >= I.RANK["cost"]


def test_waterlogging_hides_kerb_when_co_present():
    r = v("kerb_low_6", {**DAY, "co_present": ["waterlogging_shallow"]}, "low_vision_severe")
    assert "waterlog_x_kerb_unknown" in r["rules_fired"]


def test_festival_narrow_lane_crush_for_wheelchair_and_crowd_averse():
    ctx = {"hour": 20, "festival": True}
    assert v("durga_puja_lane_crowd", ctx, "mw_self")["verdict"] == "block"
    assert I.RANK[v("durga_puja_lane_crowd", ctx, "crowd_averse")["verdict"]] >= I.RANK["cost"]


def test_electrified_water_blocks_everyone():
    for b in ("no_impairment_adult", "mw_self", "deaf", "child_5_12"):
        assert v("electrified_water", DAY, b)["verdict"] == "block"


# ------------------------------------------------------------------ time
def test_vendor_presence_follows_hour_curve():
    morning = v("vendor_handcart", {"hour": 3}, "mw_self")
    evening = v("vendor_handcart", {"hour": 19}, "mw_self")
    assert evening["presence"] > morning["presence"]
    assert evening["verdict"] == "block" and morning["verdict"] != "block"


def test_monsoon_waterlogging_absent_in_winter():
    assert v("waterlogging_deep", {"season": "winter"}, "mw_self")["verdict"] != "block"
    assert v("waterlogging_deep", {"season": "monsoon"}, "mw_self")["verdict"] == "block"


# ------------------------------------------------------------------ hermes cross-cutting needs
def test_crossing_time_strands_slow_walker_not_fast_one():
    slow = v("signal_short_green", DAY, "older_80_frail")
    fast = v("signal_short_green", DAY, "no_impairment_adult")
    assert slow["terms_s"]["crossing_time"] > fast["terms_s"]["crossing_time"]
    assert "green is 8 s" in slow["reason"]


def test_rest_spacing_cost_quotes_hermes_assumption():
    r = v("no_rest_long_stretch", DAY, "older_80_frail")
    assert r["verdict"] == "cost" and "hermes ASSUMPTION" in r["reason"] and "E1.6" in r["reason"]
    assert v("no_rest_long_stretch", DAY, "deaf")["verdict"] == "none"


# ------------------------------------------------------------------ data integrity
def test_taxonomy_counts_and_every_rule_reasoned():
    d = I.data()
    assert len(d["elements"]) >= 300 and len(d["bodies"]) >= 50 and len(d["rules"]) >= 40
    for r in d["rules"]:
        assert r["reason"] and r["source"]
        if r["creates"]:
            assert r["creates"] in d["elements"]
    leaves = {b["hermes_id"] for b in d["body_list"]}
    for hid in ("A1.1", "B1.1", "C1.3", "D1.2", "E1.6", "F1.4", "G1.4"):
        assert hid in leaves


def test_every_element_by_every_body_returns_a_verdict():
    d = I.data()
    for eid in list(d["elements"])[::7]:
        for bid in d["bodies"]:
            r = I.impact(eid, DAY, bid)
            assert r["verdict"] in I.RANK and 0 <= r["risk"] <= 1


# ------------------------------------------------------------------ router adapter
def test_adapter_legacy_engine_unchanged_and_impact_blocks_steps(net):
    end = (LAT0, LON0 + 0.004)
    legacy = IA.route_with_engine(net, (LAT0, LON0), end, "manual_wheelchair", LEAVE.isoformat(), engine="legacy")
    assert legacy["status"] == "blocked_for_profile" and "engine" not in legacy
    imp = IA.route_with_engine(net, (LAT0, LON0), end, "mw_self", LEAVE.isoformat(), engine="impact")
    assert imp["status"] == "blocked_for_profile" and imp["engine"] == "impact"
    walker = IA.route_with_engine(net, (LAT0, LON0), end, "deaf", LEAVE.isoformat(), engine="impact")
    assert walker["status"] == "ok"
    # legacy route after an impact route still uses the legacy cost function
    again = R.route(net, (LAT0, LON0), end, "manual_wheelchair", LEAVE.isoformat())
    assert again["status"] == "blocked_for_profile" and "engine" not in str(again.get("summary"))[:20]


def test_adapter_same_evidence_different_bodies(net):
    A.attach(net, {"id": "imp-dust", "type": "pothole", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005,
                   "position": "barrier", "gps_error_m": 2, "source": "test", "observed_at": "2026-10-23"})
    seg = next(s for s in net.segments.values() if any(e.get("id") == "imp-dust" for e in s["evidence"]))
    mw = IA.segment_cost_impact(seg, "mw_self", LEAVE)
    deaf = IA.segment_cost_impact(seg, "deaf", LEAVE)
    assert mw["blocked"] and not deaf["blocked"]
    assert set(mw) >= set(segment_cost(seg, "manual_wheelchair", LEAVE))


def test_adapter_patch_is_thread_local(net):
    seg = next(iter(net.segments.values()))
    out = {}

    def legacy_thread():
        out["legacy"] = R.segment_cost(seg, "default_walker", LEAVE)

    with IA.using_body("mw_self"):
        assert R.segment_cost(seg, "default_walker", LEAVE).get("engine") == "impact"
        t = threading.Thread(target=legacy_thread)
        t.start()
        t.join()
    assert "engine" not in out["legacy"]


def test_matrix_export_exists_and_matches_engine():
    p = os.path.join(os.path.dirname(__file__), "..", "..", "site", "public", "content", "impact-matrix.json")
    if not os.path.exists(p):
        pytest.skip("matrix not exported yet")
    m = json.load(open(p))
    ei, bi = m["elements"].index("pothole"), m["bodies"].index("mw_self")
    cell = m["contexts"]["day_clear"]["verdict"][ei][bi]
    assert cell == "B"


def test_darkness_changes_nothing_for_cane_user_but_matters_for_low_vision():
    bd, bn = v("pothole", DAY, "blind_cane"), v("pothole", NIGHT, "blind_cane")
    assert (bd["verdict"], bd["risk"]) == (bn["verdict"], bn["risk"])
    assert v("pothole", NIGHT, "low_vision_moderate")["risk"] > v("pothole", DAY, "low_vision_moderate")["risk"]


def test_same_element_spreads_across_bodies_in_matrix_terms():
    verdicts = {I.impact("vendor_handcart", {"hour": 19}, b)["verdict"] for b in I.data()["bodies"]}
    assert len(verdicts) >= 3


def test_adapter_leave_time_sets_night_for_rules(net):
    A.attach(net, {"id": "imp-night", "type": "open_drain", "lat": LAT0 + 5 * M_LAT, "lon": LON0 + 0.0005,
                   "position": "barrier", "gps_error_m": 2, "source": "test", "observed_at": "2026-10-23"})
    seg = next(s for s in net.segments.values() if any(e.get("id") == "imp-night" for e in s["evidence"]))
    night = dt.datetime(2026, 10, 25, 22, 0, tzinfo=IST)
    r = IA.segment_cost_impact(seg, "older_60_69", night)       # no light given: leave time must set it
    hit = next(h for h in r["hits"] if h.get("evidence_id") == "imp-night")
    assert "night_x_hole" in hit["rules_fired"]
    day = IA.segment_cost_impact(seg, "older_60_69", LEAVE)
    hit_d = next(h for h in day["hits"] if h.get("evidence_id") == "imp-night")
    assert "night_x_hole" not in hit_d["rules_fired"]


def _seg(evs, length=120.0):
    return {"id": "t", "kind": "sidewalk", "length_m": length, "evidence": evs, "source": "osm"}


def _rec(**kw):
    e = {"status": "ACCEPT", "confidence": 0.9, "permanence": "permanent", "source": "test"}
    e.update(kw)
    return e


def test_adapter_clusters_duplicate_labels_and_combines_p():
    same_spot = [_rec(id=f"p{i}", type="pothole", confidence=0.4, at_m=50 + i) for i in range(3)]
    r = IA.segment_cost_impact(_seg(same_spot), "mw_self", LEAVE)
    assert not r["blocked"] and len(r["hits"]) == 1 and r["hits"][0]["labels_in_cluster"] == 3
    one = IA.segment_cost_impact(_seg(same_spot[:1]), "deaf", LEAVE)
    three = IA.segment_cost_impact(_seg(same_spot), "deaf", LEAVE)
    assert three["delay_s"] == pytest.approx(one["delay_s"])   # duplicates do not add cost again
    spread = [_rec(id=f"q{i}", type="pothole", confidence=0.4, at_m=20 + 30 * i) for i in range(3)]
    r3 = IA.segment_cost_impact(_seg(spread), "mw_self", LEAVE)
    assert r3["blocked"]                                        # 1-(1-0.4)^3 = 0.78 >= block_p, like costs.py


def test_adapter_far_or_stale_partner_does_not_fire_rules():
    ramp = _rec(id="ramp", type="kerb_ramp_present", slope_pct=6, at_m=5)
    car_far = _rec(id="car", type="parked_vehicle", permanence="temporary", at_m=110,
                   observed_at="2026-09-01T10:00:00+05:30")
    r = IA.segment_cost_impact(_seg([ramp, car_far]), "mw_self", LEAVE)
    h = next(x for x in r["hits"] if x["evidence_id"] == "ramp")
    assert "parked_x_ramp" not in h["rules_fired"] and not h["blocking"]
    car_near = _rec(id="car2", type="parked_vehicle", at_m=7)
    r2 = IA.segment_cost_impact(_seg([ramp, car_near]), "mw_self", LEAVE)
    h2 = next(x for x in r2["hits"] if x["evidence_id"] == "ramp")
    assert "parked_x_ramp" in h2["rules_fired"] and h2["blocking"]


def test_adapter_record_alone_does_not_fire_co_present_rule_on_itself():
    r = IA.segment_cost_impact(_seg([_rec(id="h", element="honking_dense_traffic", at_m=10)]), "deaf", LEAVE)
    assert "crowd_x_traffic_noise" not in r["hits"][0]["rules_fired"]
    assert r["hits"][0]["type"] == "honking_dense_traffic"


def test_co_present_none_is_ok():
    assert I.impact("pothole", {"co_present": None}, "mw_self")["verdict"] == "block"


# map review 2026-10-25: a mid-path pole scored "none" for a white-cane user. A fixed object in the walking
# line is found by cane contact, which is itself the hazard. Plus five obvious cases checked at the same time.
def test_white_cane_midpath_pole_is_not_none():
    day = {"hour": 11, "weather": "clear", "season": "winter"}
    r = I.impact("electric_pole_midpath", day, "blind_cane")
    assert r["verdict"] in ("warn", "cost", "block"), r["reason"]
    assert r["terms_risk"].get("collision", 0) > 0
    # the term is vision-specific: the baseline adult is unaffected, a guide dog lowers it
    assert I.impact("electric_pole_midpath", day, "no_impairment_adult")["verdict"] == "none"
    assert I.impact("electric_pole_midpath", day, "blind_guide_dog")["risk"] < r["risk"]


def test_obvious_cases_hold():
    day = {"hour": 11, "weather": "clear", "season": "winter"}
    night = {"hour": 21, "light": "night_dark", "weather": "clear", "season": "winter"}
    assert I.impact("open_drain_parallel", day, "blind_cane")["verdict"] == "block"
    assert I.impact("open_manhole", night, "low_vision_severe")["verdict"] == "block"
    assert I.impact("reversing_vehicles_driveway", day, "deaf")["verdict"] in ("warn", "cost", "block")
    assert I.impact("steps_short_flight", day, "mw_self")["verdict"] == "block"
    assert I.impact("kerb_high_22_no_ramp", day, "older_with_walker")["verdict"] in ("cost", "block")


def test_adapter_record_attrs_pass_through():
    """what-if records may carry extra taxonomy attrs; measured fields (height_cm ...) still win."""
    eid, over = IA.element_for_evidence({"type": "what_if", "element": "signal_short_green",
                                         "attrs": {"green_s": 12, "crossing_length_m": 14, "run_m": None}})
    assert eid == "signal_short_green" and over == {"green_s": 12, "crossing_length_m": 14}
    eid, over = IA.element_for_evidence({"type": "missing_kerb_ramp", "height_cm": 18, "attrs": {"vertical_cm": 5}})
    assert eid == "kerb_150_no_ramp" and over["vertical_cm"] == 18.0
    assert IA.element_for_evidence({"type": "steps"})[1] == {}
