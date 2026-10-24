"""Build elements.json, bodies.json, interactions.json for the RAASTA ELEMENT x BODY impact engine.

Run:  python3 -I app/route/taxonomy/build_taxonomy.py      (writes next to this file)

Why a script and not hand-written JSON: 300+ elements share a small set of archetypes (a hole, a width
squeeze, a step, an ambient condition ...). Each element row below names its archetype and only the numbers
that differ. That keeps every number visible in one place, and the JSON is regenerated, never hand-edited.

Number provenance (every attribute and sensitivity carries one of these):
  SOURCED  : a source key from SOURCES is named on the row (attrs_source / limit_sources).
  ASSUMPTION: claude design value, 2026-10-24/25, written so a reviewer can change it in one place.
Factor ids like "F2.01" point at research/claude/sc02-FACTOR-UNIVERSE.md rows (and their S-sources).
Body ids keep hermes' leaf ids (research/hermes/sc02/BODY-TAXONOMY.md) as `hermes_id`.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------------------------------------
# Sources (read 2026-10-24/25; see README for the read level of each)
# ---------------------------------------------------------------------------------------------------------
SOURCES = {
    "IRC103_2012_6.2.1": "IRC:103-2012 cl 6.2.1: pavement max 150 mm above road (verified, research/claude/VERIFY-STANDARDS.md)",
    "IRC103_2022_6.7": "IRC:103-2022 cl 6.7 Fig 48: kerb ramp not steeper than 1:15, flares 1:10 (verified, VERIFY-STANDARDS.md)",
    "HG2021_3.7.2": "MoHUA Harmonised Guidelines 2021 cl 3.7.2: kerb ramp max 1:12 (verified, VERIFY-STANDARDS.md)",
    "HG2021_3.7.3": "MoHUA HG 2021 cl 3.7.3: kerb ramp min width 900 mm (verified)",
    "HG2021_3.5.1": "MoHUA HG 2021 cl 3.5.1: walkway min 1200 mm, 1800 mm two-way, 1500 mm around trees/poles (verified)",
    "UK_IM_S98": "UK DfT Inclusive Mobility (FACTOR-UNIVERSE S98): thresholds over 10 mm a problem, cross-fall 2.5%, 95th pct power chair just over 700 mm wide (excerpt level)",
    "S96_crossslope": "FACTOR-UNIVERSE S96 (PubMed 41945617): one-rim propulsion around 3% cross slope (excerpt level)",
    "S95_stepclimb": "FACTOR-UNIVERSE S95 (PMC5672886): step-climbing power chairs median 20 cm step (excerpt level)",
    "S99_slope": "FACTOR-UNIVERSE S99 (TRID 921388): perceived slope limits, >5% costly (excerpt level)",
    "GTKP_2017": "GTKP IRF 2017 paper 814: Indian audit measured footpath heights 200 to 250 mm vs 150 mm standard (hermes MAX-INFO-PER-PIXEL.md)",
    "CPCB_AQI": "CPCB National AQI health statements (https://cpcb.nic.in/upload/NAAQS_2019.pdf; https://cpcb.nic.in/aqi_report.php), read as search excerpts 2026-10-24: 101-200 breathing discomfort to people with lung disease such as asthma, heart disease, children, older adults; 201-300 discomfort on prolonged exposure; 301-400 respiratory illness on prolonged exposure; 401-500 affects healthy people, serious impact on lung/heart disease",
    "IMD_HEAT": "IMD FAQ on heat wave (https://internal.imd.gov.in/section/nhac/dynamic/FAQ_heat_wave.pdf), search excerpt 2026-10-24: heat wave considered from 40 C plains / 30 C hills; actual max >= 45 C heat wave, >= 47 C severe",
    "NCHRP562_speeds": "TCRP 112 / NCHRP 562 (https://deldot.gov/Business/drc/manuals/nchrp_rpt_562.pdf), search excerpt: mean walking speed cane or crutch 0.80 m/s, walker 0.63 m/s, wheelchair 1.08 m/s; 0.9 m/s for less capable older pedestrians",
    "AGEING_2025": "Western et al., Age and Ageing 2025 (PubMed 41354090): mobility-limited older adults mean gait speed 0.77 m/s; 1.5% reach 1.2 m/s",
    "AGEING_2012": "Asher et al., Age and Ageing 2012 (PubMed 22695790): UK 65+ mean walking speed 0.9 m/s men, 0.8 m/s women",
    "RPWD_SCHEDULE": "RPwD Act 2016 Schedule (https://prsindia.org/files/bills_acts/acts_parliament/2016/Rights_of_Persons_with_Disabilities_Act_2016.pdf; Lok Sabha AU1109 list; hermes BODY-TAXONOMY.md read the Gazette text)",
    "HERMES_BODY": "research/hermes/sc02/BODY-TAXONOMY.md (hermes, 2026-10-25 00:05): 61 leaves, qualitative needs; N-codes are sourced, A-cells are hermes assumptions",
    "ASSUMPTIONS_JSON": "app/route/hroute/assumptions.json (existing 7-profile model): kerb block above 2 cm for wheelchairs, width 90 cm, slope 6.67%",
    "FU": "research/claude/sc02-FACTOR-UNIVERSE.md (348 factors; S-numbers inside)",
}

AXES = ["vertical_cm", "clear_width_cm", "slope_pct", "cross_slope_pct", "roughness", "slip", "fall",
        "overhead", "visibility_needed", "contrast_loss", "glare", "flicker", "noise_db", "air", "heat", "cold",
        "crowd", "vehicle", "animal", "water_cm", "electric", "cognitive", "wait_s", "detour_m", "effort",
        "cane_detectable", "spans_path", "relief", "crossing_length_m", "green_s", "rest_gap_m", "run_m"]

AXIS_DOC = {
    "vertical_cm": "height of a step, kerb, lip or depth of a hole/drop, cm",
    "clear_width_cm": "clear width left to pass beside or through the element, cm (null = does not limit width)",
    "slope_pct": "running slope, %", "cross_slope_pct": "cross slope, %",
    "roughness": "SURFACE EVENNESS term (hermes cross-cutting need 3): roughness / vibration, 0-1", "slip": "slip hazard, 0-1",
    "fall": "hole / drop / fall-into hazard severity, 0-1", "overhead": "head-height hazard, 0-1",
    "visibility_needed": "how much avoiding it relies on seeing it, 0-1",
    "contrast_loss": "how much it lowers visual contrast of the scene, 0-1", "glare": "glare, 0-1",
    "flicker": "flashing / strobe light, 0-1 (photosensitive trigger)", "noise_db": "sound level, dB(A) (null = quiet)",
    "air": "airborne particulate / smoke / gas burden, 0-1", "heat": "heat stress, 0-1", "cold": "cold stress, 0-1",
    "crowd": "crowd density, 0-1", "vehicle": "moving-vehicle conflict, 0-1", "animal": "animal threat, 0-1",
    "water_cm": "standing water depth, cm", "electric": "electrocution hazard, 0-1",
    "cognitive": "wayfinding / decision load, 0-1", "wait_s": "forced wait, s", "detour_m": "forced detour, m",
    "effort": "endurance / exertion burden, 0-1",
    "cane_detectable": "how well a long cane finds it, 0-1 (ground-level 1, overhead 0)",
    "spans_path": "true when it covers the whole width (cannot step around)",
    "relief": "positive element: how much it helps (shade, bench, audible signal), 0-1",
    "crossing_length_m": "CROSSING TIME term (hermes need 2): kerb-to-kerb length to cross, m; time needed = length / body speed + start-up",
    "green_s": "pedestrian green time, s (null = unsignalised); a body slower than length/green is stranded mid-road",
    "run_m": "length of a sloped run, m (null = long / unknown); a 2.5 m kerb ramp costs less time than a 100 m hill",
    "rest_gap_m": "REST SPACING term (hermes need 1): distance with no bench / shade / rest point, m; compared to each leaf's rest_spacing_m",
}

# ---------------------------------------------------------------------------------------------------------
# Temporal patterns
# ---------------------------------------------------------------------------------------------------------
HOUR_CURVES = {
    "constant": [1.0] * 24,
    # vendor and parked_vehicle copied from app/route/hroute/assumptions.json temporal.hour_curve (ASSUMPTION there)
    "vendor": [0.05, 0.02, 0.02, 0.02, 0.02, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.9, 0.9, 0.8, 0.7, 0.7, 0.8, 0.95,
               1.0, 1.0, 0.95, 0.8, 0.5, 0.2],
    "parked_vehicle": [0.3, 0.25, 0.25, 0.25, 0.25, 0.25, 0.3, 0.4, 0.55, 0.75, 0.9, 1.0, 1.0, 0.95, 0.9, 0.9, 0.95,
                       1.0, 1.0, 1.0, 0.9, 0.7, 0.5, 0.4],
    "school": [0, 0, 0, 0, 0, 0, 0.1, 0.9, 1.0, 0.3, 0.1, 0.1, 0.3, 1.0, 0.9, 0.4, 0.2, 0.1, 0, 0, 0, 0, 0, 0],
    "office_rush": [0.1, 0.05, 0.05, 0.05, 0.05, 0.1, 0.3, 0.6, 1.0, 1.0, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.9,
                    1.0, 1.0, 0.7, 0.4, 0.2, 0.1],
    "evening_market": [0.05, 0.02, 0.02, 0.02, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.6, 0.6, 0.7, 0.8,
                       0.9, 1.0, 1.0, 1.0, 0.9, 0.6, 0.2],
    "night": [1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0],
    "day": [0, 0, 0, 0, 0, 0.2, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.3, 0, 0, 0, 0, 0],
    "midday_heat": [0, 0, 0, 0, 0, 0, 0, 0.1, 0.3, 0.5, 0.8, 1.0, 1.0, 1.0, 1.0, 0.9, 0.7, 0.4, 0.1, 0, 0, 0, 0, 0],
    "temple": [0.05, 0, 0, 0, 0.3, 0.8, 1.0, 0.9, 0.6, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.4, 0.6, 0.9, 1.0, 0.8,
               0.4, 0.1, 0.05],
    "festival_evening": [0.3, 0.2, 0.1, 0.05, 0.05, 0.05, 0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.5, 0.6, 0.7,
                         0.9, 1.0, 1.0, 1.0, 1.0, 0.8, 0.5],
    "dawn_dusk": [0, 0, 0, 0, 0, 0.6, 1.0, 0.6, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.6, 1.0, 0.6, 0, 0, 0, 0],
    "fog_morning": [0.8, 0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.1, 0.2,
                    0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
}
HOUR_CURVES_SOURCE = "ASSUMPTION for all curves except vendor and parked_vehicle, which are the existing ASSUMPTION curves from assumptions.json; no Indian hourly survey found (FACTOR-UNIVERSE 5.01, PREDICT-MISSING F4)"

SEASONS = ["winter", "summer", "monsoon", "post_monsoon"]
SEASON_PROFILES = {
    "all": {"winter": 1, "summer": 1, "monsoon": 1, "post_monsoon": 1},
    "monsoon": {"winter": 0.05, "summer": 0.1, "monsoon": 1.0, "post_monsoon": 0.4},
    "monsoon_decay": {"winter": 0.3, "summer": 0.4, "monsoon": 1.0, "post_monsoon": 0.8},
    "summer": {"winter": 0.0, "summer": 1.0, "monsoon": 0.3, "post_monsoon": 0.3},
    "winter": {"winter": 1.0, "summer": 0.0, "monsoon": 0.0, "post_monsoon": 0.4},
    "winter_smog": {"winter": 1.0, "summer": 0.3, "monsoon": 0.05, "post_monsoon": 0.8},
    "dry": {"winter": 1.0, "summer": 1.0, "monsoon": 0.2, "post_monsoon": 0.7},
    "festival": {"winter": 0.4, "summer": 0.2, "monsoon": 0.4, "post_monsoon": 1.0},
}


def perm(hl_years=10):
    return {"pattern": "permanent", "half_life_h": hl_years * 8766, "hour_curve": "constant", "season": "all"}


def semi(hl_days=90, curve="constant", season="all"):
    return {"pattern": "semi_permanent", "half_life_h": hl_days * 24, "hour_curve": curve, "season": season}


def temp(hl_h, curve="constant", rec=0.0, season="all"):
    return {"pattern": "temporary", "half_life_h": hl_h, "hour_curve": curve, "recurrence": rec, "season": season}


def event(hl_h, curve="festival_evening", season="festival"):
    return {"pattern": "event", "half_life_h": hl_h, "hour_curve": curve, "season": season}


def ambient(curve="constant", season="all", hl_h=3):
    return {"pattern": "ambient", "half_life_h": hl_h, "hour_curve": curve, "season": season}


def weather(season="all", hl_h=6, curve="constant"):
    return {"pattern": "weather", "half_life_h": hl_h, "hour_curve": curve, "season": season}


# ---------------------------------------------------------------------------------------------------------
# Archetypes: default attributes (ASSUMPTION unless the element row names a source)
# ---------------------------------------------------------------------------------------------------------
ARCH = {
    "kerb": dict(vertical_cm=15, spans_path=True, fall=0.25, visibility_needed=0.6, cane_detectable=1.0),
    "ramp": dict(slope_pct=10, spans_path=True, visibility_needed=0.2, cane_detectable=0.8, run_m=2.5),
    "step": dict(vertical_cm=15, spans_path=True, fall=0.3, visibility_needed=0.6, effort=0.3, cane_detectable=1.0),
    "width": dict(clear_width_cm=80, cane_detectable=0.9, visibility_needed=0.3),
    "slope": dict(slope_pct=7, spans_path=True, effort=0.4, cane_detectable=0.3),
    "hole": dict(vertical_cm=8, clear_width_cm=80, fall=0.5, roughness=0.5, visibility_needed=0.8,
                 cane_detectable=0.7),
    "deep_hole": dict(vertical_cm=60, clear_width_cm=70, fall=0.95, visibility_needed=0.9, cane_detectable=0.6),
    "surface": dict(roughness=0.5, spans_path=True, visibility_needed=0.3, cane_detectable=0.8),
    "slippery": dict(slip=0.5, spans_path=True, visibility_needed=0.4, cane_detectable=0.3),
    "pole": dict(clear_width_cm=90, visibility_needed=0.5, cane_detectable=0.9, fall=0.05),
    "overhead": dict(overhead=0.6, cane_detectable=0.0, visibility_needed=0.7),
    "parked": dict(clear_width_cm=60, detour_m=10, vehicle=0.15, visibility_needed=0.3, cane_detectable=0.9),
    "vendor": dict(clear_width_cm=70, crowd=0.4, noise_db=70, cognitive=0.2, cane_detectable=0.8,
                   visibility_needed=0.3),
    "debris": dict(clear_width_cm=40, roughness=0.7, fall=0.3, vertical_cm=20, visibility_needed=0.5,
                   cane_detectable=0.8, air=0.15),
    "event": dict(crowd=0.8, noise_db=85, clear_width_cm=60, cognitive=0.5, detour_m=100),
    "animal": dict(animal=0.5, clear_width_cm=80, visibility_needed=0.4, cane_detectable=0.6),
    "crossing": dict(vehicle=0.6, wait_s=30, cognitive=0.3, visibility_needed=0.4, spans_path=True, crossing_length_m=10),
    "traffic": dict(vehicle=0.7, noise_db=75, cognitive=0.2),
    "light": dict(spans_path=True),
    "weather": dict(spans_path=True),
    "air": dict(air=0.6, spans_path=True),
    "noise": dict(noise_db=85, cognitive=0.3, spans_path=True),
    "crowd": dict(crowd=0.7, clear_width_cm=90, noise_db=72, cognitive=0.3),
    "social": dict(spans_path=True),
    "terrain": dict(spans_path=True),
    "transit": dict(spans_path=True),
    "positive": dict(relief=0.5),
    "compound": dict(),
}

# ---------------------------------------------------------------------------------------------------------
# Elements. Row: (id, name, archetype, overrides, temporal, detect, detector_class, refs, tags, attrs_source)
# detect: yes / partial / no (from a single street photo). detector_class: receipt class_family or routing type.
# ---------------------------------------------------------------------------------------------------------
TREE = []  # (category, category_name, [(subcategory, sub_name, [rows])])


def cat(cid, name, subs):
    TREE.append((cid, name, subs))


A = "ASSUMPTION"

cat("geometry", "Footpath geometry and level changes", [
    ("kerbs", "Kerbs, lips and level changes", [
        ("kerb_150_no_ramp", "Kerb 15 cm with no ramp", "kerb", {}, perm(), "partial", "missing_kerb_ramp", ["F1.02", "F1.03"], ["kerb"], "IRC103_2012_6.2.1"),
        ("kerb_high_22_no_ramp", "High kerb 20 to 25 cm, no ramp (measured Indian audit range)", "kerb", {"vertical_cm": 22, "fall": 0.35}, perm(), "partial", "missing_kerb_ramp", ["F1.02"], ["kerb"], "GTKP_2017"),
        ("kerb_low_6", "Low kerb about 6 cm", "kerb", {"vertical_cm": 6, "fall": 0.15}, perm(), "partial", "missing_kerb_ramp", ["F1.02"], ["kerb"], A),
        ("kerb_ramp_good", "Kerb ramp within 1:15, flush", "ramp", {"slope_pct": 6.0, "relief": 0.3}, perm(), "yes", "kerb_ramp_present", ["F1.03"], ["ramp", "clear"], "IRC103_2022_6.7"),
        ("kerb_ramp_steep_1in10", "Kerb ramp steeper than 1:12 (about 1:10)", "ramp", {"slope_pct": 10.0}, perm(), "partial", "kerb_ramp_present", ["F1.04"], ["ramp"], "HG2021_3.7.2"),
        ("kerb_ramp_steep_1in8", "Kerb ramp about 1:8", "ramp", {"slope_pct": 12.5}, perm(), "partial", "kerb_ramp_present", ["F1.04", "F1.12"], ["ramp"], A),
        ("kerb_ramp_flare_steep", "Kerb ramp side flares steeper than 1:10", "ramp", {"slope_pct": 5, "cross_slope_pct": 12, "fall": 0.15, "spans_path": False, "clear_width_cm": 100}, perm(), "partial", "kerb_ramp_present", ["F1.05"], ["ramp"], "IRC103_2022_6.7"),
        ("kerb_ramp_narrow_70", "Kerb ramp narrower than 70 cm", "ramp", {"slope_pct": 8, "clear_width_cm": 65}, perm(), "partial", "kerb_ramp_present", ["F1.06"], ["ramp"], "HG2021_3.7.3"),
        ("ramp_bottom_lip_3", "Ramp bottom lip / gutter step about 3 cm", "kerb", {"vertical_cm": 3, "fall": 0.2, "visibility_needed": 0.7}, perm(), "partial", "missing_kerb_ramp", ["F1.07"], ["kerb", "lip"], "UK_IM_S98"),
        ("footpath_step_down_repeated", "Footpath height changes every few metres", "step", {"vertical_cm": 12, "effort": 0.5}, perm(), "partial", "steps", ["F1.11"], ["kerb", "step"], A),
        ("driveway_ramp_warp", "Driveway ramp cutting across the footpath", "ramp", {"slope_pct": 3, "cross_slope_pct": 8, "spans_path": True}, perm(), "partial", None, ["F1.12", "F4.22"], ["ramp"], A),
        ("side_street_drop", "Footpath drops to road level at side street", "kerb", {"vertical_cm": 15, "vehicle": 0.3}, perm(), "partial", "missing_kerb_ramp", ["F1.13"], ["kerb"], A),
        ("footpath_dead_end", "Footpath ends abruptly", "kerb", {"vertical_cm": 15, "detour_m": 60, "cognitive": 0.3}, perm(), "partial", "missing_footpath", ["F1.14"], ["kerb"], A),
        ("footpath_drains_onto_path", "Badly graded footpath that holds water", "slope", {"slope_pct": 0, "cross_slope_pct": 3, "water_cm": 3, "slip": 0.3}, perm(), "partial", None, ["F2.26"], ["flood_prone"], A),
        ("road_higher_than_footpath", "Road raised above footpath (reversed step)", "kerb", {"vertical_cm": 10, "water_cm": 0}, perm(), "partial", None, ["W93"], ["kerb", "flood_prone"], A),
        ("utility_cover_raised", "Utility cover raised 3 cm", "kerb", {"vertical_cm": 3, "spans_path": False, "clear_width_cm": 90, "fall": 0.15}, perm(), "partial", "broken_footpath", ["F1.31"], ["lip", "metal"], A),
        ("utility_cover_sunk", "Utility cover sunk 4 cm", "hole", {"vertical_cm": 4, "fall": 0.25, "clear_width_cm": 90}, perm(), "partial", "broken_footpath", ["F1.31"], ["hole", "metal"], A),
        ("patch_height_mismatch", "Temporary patch with height mismatch", "kerb", {"vertical_cm": 3, "spans_path": True, "fall": 0.15}, semi(180), "partial", "broken_footpath", ["F2.30"], ["lip"], A),
        ("tree_root_heave", "Tree roots heaving slabs", "kerb", {"vertical_cm": 5, "roughness": 0.5, "fall": 0.2, "clear_width_cm": 80, "spans_path": False}, perm(), "partial", "broken_footpath", ["F2.31"], ["lip", "tree"], A),
        ("collapsed_kerb_edge", "Collapsed kerb edge", "hole", {"vertical_cm": 10, "fall": 0.45, "clear_width_cm": 90}, semi(365), "partial", "broken_footpath", ["F2.29"], ["hole", "kerb"], A),
        ("tabletop_crossing", "Raised tabletop crossing, footpath level", "positive", {"relief": 0.4, "vehicle": 0.1}, perm(), "yes", "kerb_ramp_present", ["F1.13"], ["clear", "crossing"], A),
    ]),
    ("stairs_ramps", "Stairs, ramps and grade-separated crossings", [
        ("steps_short_flight", "Short flight of 1 to 3 steps", "step", {}, perm(), "yes", "steps", ["F1.17"], ["step"], "IRC103_2012_6.2.1"),
        ("stairs_long_flight", "Long staircase (10+ steps)", "step", {"vertical_cm": 150, "effort": 0.9, "fall": 0.45}, perm(), "yes", "steps", ["F1.17"], ["step"], A),
        ("steps_no_handrail", "Steps with no handrail", "step", {"fall": 0.5}, perm(), "partial", "steps", ["F1.19"], ["step", "no_handrail"], A),
        ("high_riser_20", "Step risers above 15 cm (about 20 cm)", "step", {"vertical_cm": 20, "fall": 0.4}, perm(), "partial", "steps", ["F1.18"], ["step"], "IRC103_2012_6.2.1"),
        ("ramp_no_landing", "Long ramp with no landing", "ramp", {"slope_pct": 8.33, "effort": 0.7, "run_m": 9}, perm(), "partial", None, ["F1.20"], ["ramp"], A),
        ("ramp_no_handrail", "Ramp with no handrail", "ramp", {"slope_pct": 7, "fall": 0.25}, perm(), "partial", None, ["F1.19"], ["ramp", "no_handrail"], A),
        ("ramp_steep_long", "Steep long ramp (1:8, 12 m)", "ramp", {"slope_pct": 12.5, "effort": 0.9, "run_m": 12}, perm(), "partial", None, ["M527"], ["ramp"], A),
        ("fob_stairs_only", "Foot over bridge with stairs only", "step", {"vertical_cm": 550, "effort": 1.0, "fall": 0.5}, perm(), "yes", "steps", ["F1.23"], ["step", "fob"], A),
        ("fob_lift_broken", "Foot over bridge lift out of service", "step", {"vertical_cm": 550, "effort": 1.0, "fall": 0.5, "cognitive": 0.3}, temp(720, rec=0.5), "no", None, ["F1.23", "W8"], ["step", "fob"], A),
        ("fob_lift_working", "Foot over bridge with a working lift", "positive", {"wait_s": 60, "relief": 0.3}, temp(720), "partial", None, ["F1.23"], ["fob", "clear"], A),
        ("subway_stairs_only", "Pedestrian subway with stairs only", "step", {"vertical_cm": 400, "effort": 0.9, "contrast_loss": 0.4}, perm(), "partial", "steps", ["F1.24"], ["step", "flood_prone"], A),
        ("escalator_only", "Escalator only, no lift", "step", {"vertical_cm": 500, "fall": 0.4, "cognitive": 0.3, "effort": 0.1}, perm(), "partial", None, ["F1.23"], ["step"], A),
        ("ghat_steps", "Riverfront ghat steps", "step", {"vertical_cm": 300, "slip": 0.4, "effort": 0.8}, perm(), "yes", "steps", ["F8.17"], ["step"], A),
        ("hill_steps_path", "Hill town steps as the main path", "step", {"vertical_cm": 600, "effort": 1.0, "fall": 0.4}, perm(), "yes", "steps", ["F8.02"], ["step"], A),
        ("entrance_steps_destination", "Destination entrance has steps", "step", {"vertical_cm": 45}, perm(), "yes", "steps", ["W141"], ["step"], A),
    ]),
    ("width_slope", "Width, slope and through-route", [
        ("narrow_footpath_80", "Footpath clear width about 80 cm", "width", {"clear_width_cm": 80, "spans_path": True}, perm(), "partial", None, ["F1.08"], ["narrow"], "HG2021_3.5.1"),
        ("narrow_footpath_110", "Footpath clear width about 110 cm", "width", {"clear_width_cm": 110, "spans_path": True}, perm(), "partial", None, ["F1.08"], ["narrow"], "HG2021_3.5.1"),
        ("running_slope_6", "Running slope about 6%", "slope", {"slope_pct": 6}, perm(), "partial", "steep_slope", ["F1.09"], ["slope"], "S99_slope"),
        ("running_slope_10", "Running slope about 10%", "slope", {"slope_pct": 10, "effort": 0.7}, perm(), "partial", "steep_slope", ["F1.09"], ["slope"], A),
        ("cross_slope_4", "Cross slope about 4%", "slope", {"slope_pct": 0, "cross_slope_pct": 4, "effort": 0.3}, perm(), "partial", None, ["F1.10"], ["slope"], "S96_crossslope"),
        ("cross_slope_7", "Cross slope about 7%", "slope", {"slope_pct": 0, "cross_slope_pct": 7, "effort": 0.5, "fall": 0.15}, perm(), "partial", None, ["F1.10"], ["slope"], A),
        ("hill_gradient_road", "Hill town road gradient about 15%", "slope", {"slope_pct": 15, "effort": 1.0}, perm(), "partial", "steep_slope", ["F8.01"], ["slope"], A),
        ("no_turning_space", "No 1.5 m turning space at a corner", "width", {"clear_width_cm": 110, "detour_m": 15}, perm(), "partial", None, ["F1.32"], ["narrow"], A),
        ("bollards_narrow_80", "Bollards spaced about 80 cm", "width", {"clear_width_cm": 80, "spans_path": True}, perm(), "yes", "pole_obstruction", ["F1.25"], ["pole", "metal"], "UK_IM_S98"),
        ("bollards_ok_120", "Bollards spaced 120 cm", "width", {"clear_width_cm": 120, "spans_path": True}, perm(), "yes", "pole_obstruction", ["F1.25", "F4.21"], ["pole", "metal"], A),
        ("motorcycle_chicane_barrier", "Zig-zag barrier to stop motorcycles", "width", {"clear_width_cm": 70, "spans_path": True, "cognitive": 0.3}, perm(), "yes", "pole_obstruction", ["F1.25"], ["metal"], A),
        ("guardrail_continuous", "Continuous guardrail with no opening", "width", {"clear_width_cm": None, "detour_m": 150}, perm(), "yes", None, ["F1.26"], ["metal", "railing"], A),
        ("median_railing_no_gap", "Median railing, no gap to cross", "width", {"clear_width_cm": None, "detour_m": 250}, perm(), "yes", None, ["W124"], ["metal", "railing"], A),
        ("footpath_one_side_only", "Footpath on one side only", "crossing", {"wait_s": 20, "detour_m": 40}, perm(), "partial", None, ["F1.33"], ["crossing"], A),
        ("protrusion_100mm_plus", "Object protruding more than 10 cm into path", "overhead", {"overhead": 0.4, "cane_detectable": 0.3, "clear_width_cm": 100}, perm(), "partial", "pole_obstruction", ["F1.28"], ["overhead"], A),
        ("tactile_leads_into_pole", "Tactile paving that leads into a pole", "pole", {"cognitive": 0.4, "clear_width_cm": 100}, perm(), "partial", "pole_obstruction", ["F1.29", "W160"], ["tactile", "pole"], A),
    ]),
])

cat("surface", "Surface condition and materials", [
    ("holes", "Holes, drops and open drains", [
        ("pothole_small", "Small pothole, about 3 cm", "hole", {"vertical_cm": 3, "fall": 0.2, "clear_width_cm": 100}, semi(60), "yes", "pothole", ["F2.01"], ["hole"], A),
        ("pothole", "Pothole, about 8 cm deep", "hole", {}, semi(90), "yes", "pothole", ["F2.01", "F2.02", "F14.12"], ["hole"], A),
        ("pothole_deep", "Deep pothole, 15 cm or more", "hole", {"vertical_cm": 15, "fall": 0.7, "clear_width_cm": 60}, semi(90), "yes", "pothole", ["F2.02"], ["hole"], A),
        ("pothole_cluster", "Cluster of potholes across the path", "hole", {"spans_path": True, "roughness": 0.8, "fall": 0.55}, semi(90), "yes", "pothole", ["F2.01", "F2.32"], ["hole"], A),
        ("open_manhole", "Open manhole, cover missing", "deep_hole", {"vertical_cm": 150, "fall": 1.0, "clear_width_cm": 60}, temp(720, rec=0.2), "partial", "open_drain", ["F2.08", "F2.09", "S11"], ["hole", "drain"], A),
        ("manhole_cover_loose", "Loose or rocking manhole cover", "hole", {"vertical_cm": 2, "fall": 0.4, "visibility_needed": 1.0, "cane_detectable": 0.2}, semi(120), "no", None, ["F2.05"], ["metal", "hole"], A),
        ("open_drain_parallel", "Open drain along the footpath", "deep_hole", {"vertical_cm": 60, "fall": 0.85, "clear_width_cm": 80, "air": 0.2}, perm(), "yes", "open_drain", ["F2.06", "M529"], ["drain", "hole"], A),
        ("missing_drain_slab", "Missing drain slab in the footpath", "deep_hole", {"vertical_cm": 60, "fall": 0.95, "clear_width_cm": 50}, semi(120), "yes", "open_drain", ["F2.06"], ["drain", "hole"], A),
        ("plank_over_drain", "Wooden plank over a drain gap", "deep_hole", {"vertical_cm": 5, "fall": 0.6, "clear_width_cm": 40, "spans_path": True, "roughness": 0.6}, semi(60), "partial", "open_drain", ["F2.07"], ["drain"], A),
        ("loose_drain_slab", "Loose or rocking drain slab", "hole", {"vertical_cm": 4, "fall": 0.6, "visibility_needed": 1.0, "cane_detectable": 0.2, "spans_path": True}, semi(120), "no", None, ["F2.05", "M525"], ["drain"], A),
        ("open_trench", "Open trench from utility work", "deep_hole", {"vertical_cm": 80, "fall": 0.9, "spans_path": True, "clear_width_cm": 0, "detour_m": 80}, temp(24 * 21), "yes", "broken_footpath", ["F2.11"], ["hole", "construction"], A),
        ("sinkhole_cavein", "Cave-in / sinkhole", "deep_hole", {"vertical_cm": 100, "fall": 1.0, "spans_path": True, "clear_width_cm": 0, "detour_m": 100}, temp(24 * 14), "partial", "broken_footpath", ["F2.25"], ["hole"], A),
        ("borewell_pit", "Open borewell or pit next to the path", "deep_hole", {"vertical_cm": 1000, "fall": 1.0, "clear_width_cm": 100}, semi(60), "no", None, ["F2.10"], ["hole"], A),
        ("tree_pit_open", "Open tree pit, no grate", "hole", {"vertical_cm": 15, "fall": 0.5, "clear_width_cm": 90}, perm(), "yes", "broken_footpath", ["F1.30"], ["hole", "tree"], A),
        ("grating_parallel_slots", "Drain grating with slots parallel to travel", "hole", {"vertical_cm": 2, "fall": 0.35, "roughness": 0.4, "spans_path": True, "visibility_needed": 0.6, "cane_detectable": 0.5}, perm(), "partial", None, ["F1.16"], ["metal", "drain"], A),
        ("wide_joint_gap", "Wide joint or crack across path", "hole", {"vertical_cm": 2, "fall": 0.2, "spans_path": True, "roughness": 0.4}, perm(), "partial", "broken_footpath", ["F1.15"], ["crack"], A),
        ("broken_pavers", "Broken or tilted paver blocks", "surface", {"roughness": 0.7, "vertical_cm": 3, "fall": 0.25}, semi(180), "yes", "broken_footpath", ["F2.03", "F2.19"], ["surface", "broken"], A),
        ("missing_pavers", "Missing paver blocks", "hole", {"vertical_cm": 6, "fall": 0.35, "roughness": 0.6, "clear_width_cm": 80}, semi(180), "yes", "broken_footpath", ["F2.03"], ["hole", "broken"], A),
        ("cracked_slab", "Cracked concrete slabs", "surface", {"roughness": 0.5, "vertical_cm": 1.5}, semi(365), "yes", "broken_footpath", ["F2.04"], ["surface", "crack"], A),
        ("uneven_patchwork", "Uneven patchwork surface", "surface", {"roughness": 0.6, "vertical_cm": 2}, semi(365), "partial", "broken_footpath", ["F2.30"], ["surface"], A),
        ("crumbling_new_footpath", "New footpath already crumbling", "surface", {"roughness": 0.6, "vertical_cm": 2.5}, semi(90), "partial", "broken_footpath", ["F2.16"], ["surface", "broken"], A),
    ]),
    ("materials", "Surface materials and coatings", [
        ("polished_granite", "Polished granite slabs", "slippery", {"slip": 0.2, "glare": 0.3}, perm(), "partial", None, ["F2.18"], ["smooth_stone", "wet_slippery"], A),
        ("glazed_tiles", "Glazed tiles", "slippery", {"slip": 0.25, "glare": 0.3}, perm(), "partial", None, ["F2.18"], ["smooth_stone", "wet_slippery"], A),
        ("interlocking_pavers", "Interlocking concrete pavers", "surface", {"roughness": 0.35}, perm(), "yes", None, ["F2.17", "S100"], ["surface", "pavers"], A),
        ("cobbles_setts", "Cobbles or stone setts", "surface", {"roughness": 0.8, "vertical_cm": 2}, perm(), "yes", None, ["F2.17"], ["surface"], A),
        ("bitumen_smooth", "Smooth bitumen", "positive", {"relief": 0.1, "heat": 0.2}, perm(), "yes", None, ["F2.17"], ["dark_surface", "clear"], A),
        ("concrete_smooth", "Smooth concrete", "positive", {"relief": 0.1}, perm(), "yes", None, ["F2.17"], ["clear"], A),
        ("mud_kuccha", "Unpaved earth (kuccha) path", "surface", {"roughness": 0.7, "vertical_cm": 3, "air": 0.2}, perm(), "yes", "missing_footpath", ["F8.07", "F6.17"], ["unpaved", "surface"], A),
        ("gravel_loose", "Loose gravel", "surface", {"roughness": 0.9, "slip": 0.3}, semi(60), "partial", None, ["M526"], ["unpaved", "surface"], A),
        ("sand_layer", "Sand over paving", "surface", {"roughness": 0.8, "slip": 0.35, "air": 0.2}, temp(72), "partial", None, ["F3.34", "M526"], ["unpaved", "surface"], A),
        ("grass_verge", "Grass verge as path", "surface", {"roughness": 0.6, "visibility_needed": 0.5}, perm(), "yes", None, ["F2.17", "S100"], ["unpaved", "surface"], A),
        ("metal_plate_cover", "Steel plate over a trench", "slippery", {"slip": 0.3, "vertical_cm": 2, "roughness": 0.3}, temp(24 * 30), "partial", None, ["F2.11"], ["metal", "wet_slippery"], A),
        ("tactile_paving_correct", "Tactile paving laid correctly", "positive", {"relief": 0.6, "roughness": 0.15}, perm(), "partial", None, ["F1.29"], ["tactile", "clear"], A),
        ("tactile_paving_wrong", "Tactile paving laid wrongly", "surface", {"roughness": 0.15, "cognitive": 0.5, "spans_path": False}, perm(), "partial", None, ["F1.29"], ["tactile"], A),
        ("wet_leaves_algae", "Wet leaves and algae", "slippery", {"slip": 0.6}, weather("monsoon", 72), "partial", None, ["F6.22"], ["wet_slippery"], A),
        ("oil_spill", "Oil or diesel spill", "slippery", {"slip": 0.7, "spans_path": False, "clear_width_cm": 80}, temp(72), "partial", None, ["F3.32"], ["wet_slippery"], A),
        ("moss_shaded_steps", "Moss on shaded steps", "slippery", {"slip": 0.6, "vertical_cm": 15, "fall": 0.3}, weather("monsoon_decay", 24 * 60), "partial", "steps", ["F6.22"], ["wet_slippery", "step"], A),
        ("washing_water_hose", "Shop washing water / hose on footpath", "slippery", {"slip": 0.4, "water_cm": 1}, temp(1, "day"), "partial", None, ["F3.32"], ["wet_slippery"], A),
        ("holi_colour_residue", "Holi colour residue on surfaces", "slippery", {"slip": 0.4, "air": 0.2}, event(48, "day"), "partial", None, ["F5.06", "W70"], ["wet_slippery"], A),
        ("firecracker_debris", "Firecracker debris after Diwali", "surface", {"roughness": 0.3, "air": 0.4, "slip": 0.2}, event(48, "day"), "partial", None, ["F5.06"], ["surface"], A),
        ("dust_layer_construction", "Construction dust layer on path", "surface", {"roughness": 0.2, "slip": 0.25, "air": 0.35}, temp(72), "partial", None, ["F2.13"], ["surface", "dust"], A),
        ("cattle_dung", "Dung on the path", "slippery", {"slip": 0.4, "spans_path": False, "clear_width_cm": 90}, temp(24, rec=0.4), "partial", None, ["F3.26"], ["wet_slippery"], A),
    ]),
])

cat("fixed_obstacles", "Fixed obstacles and street furniture", [
    ("utilities", "Utility installations", [
        ("electric_pole_midpath", "Electric pole in the middle of the footpath", "pole", {"clear_width_cm": 70}, perm(), "yes", "pole_obstruction", ["F3.01"], ["pole", "metal", "electrical"], A),
        ("transformer_on_footpath", "Transformer / ring main unit on footpath", "pole", {"clear_width_cm": 60, "electric": 0.1, "heat": 0.1}, perm(), "yes", "pole_obstruction", ["F3.02", "F14.16"], ["electrical", "metal"], A),
        ("junction_box", "Utility junction box on footpath", "pole", {"clear_width_cm": 80, "electric": 0.05}, perm(), "yes", "pole_obstruction", ["F3.03"], ["electrical", "metal"], A),
        ("telecom_cabinet", "Telecom cabinet", "pole", {"clear_width_cm": 85}, perm(), "yes", "pole_obstruction", ["F3.06"], ["metal"], A),
        ("streetlight_pole", "Streetlight pole in path", "pole", {"clear_width_cm": 100}, perm(), "yes", "pole_obstruction", ["F7.04"], ["pole", "metal", "electrical"], A),
        ("signpost_pole", "Signpost pole", "pole", {"clear_width_cm": 100}, perm(), "yes", "pole_obstruction", ["F3.07"], ["pole", "metal"], A),
        ("hoarding_pole", "Hoarding pole", "pole", {"clear_width_cm": 80}, perm(3), "yes", "pole_obstruction", ["F3.07", "F13.17"], ["pole", "metal"], A),
        ("signal_pole", "Traffic signal pole on kerb", "pole", {"clear_width_cm": 100}, perm(), "yes", "pole_obstruction", ["F1.29"], ["pole", "metal", "electrical"], A),
        ("water_meter_box", "Water meter box raised above surface", "kerb", {"vertical_cm": 6, "spans_path": False, "clear_width_cm": 90, "fall": 0.2}, perm(), "partial", "broken_footpath", ["F1.31"], ["lip"], A),
        ("dangling_cables", "Dangling cables", "overhead", {"overhead": 0.5, "electric": 0.2, "cane_detectable": 0.1}, semi(120), "partial", None, ["F3.21"], ["electrical", "overhead"], A),
        ("guy_wire", "Pole guy wire across path", "overhead", {"overhead": 0.4, "cane_detectable": 0.3, "fall": 0.2, "clear_width_cm": 90}, perm(), "partial", None, ["F3.21"], ["overhead", "metal"], A),
    ]),
    ("furniture", "Street furniture, trees and structures", [
        ("tree_trunk_in_path", "Tree trunk inside the footpath", "pole", {"clear_width_cm": 70}, perm(30), "yes", "pole_obstruction", ["F3.04"], ["tree"], A),
        ("bus_shelter_in_path", "Bus shelter blocking the footpath", "pole", {"clear_width_cm": 60, "crowd": 0.3}, perm(), "yes", "pole_obstruction", ["F3.05"], ["metal"], A),
        ("bench_in_path", "Bench placed in the walking line", "pole", {"clear_width_cm": 90}, perm(), "yes", "pole_obstruction", ["F3.05"], [], A),
        ("dustbin_fixed", "Fixed dustbin in path", "pole", {"clear_width_cm": 95, "air": 0.1}, perm(), "yes", "pole_obstruction", ["F3.19"], [], A),
        ("planter_box", "Planter box on footpath", "pole", {"clear_width_cm": 85}, perm(), "yes", "pole_obstruction", ["F3.05"], [], A),
        ("police_booth", "Police booth on footpath", "pole", {"clear_width_cm": 60}, perm(), "yes", "pole_obstruction", ["F4.07"], [], A),
        ("dairy_booth", "Licensed dairy booth on footpath", "pole", {"clear_width_cm": 50, "crowd": 0.3}, semi(365), "yes", "vendor", ["F3.09"], ["vendor"], A),
        ("shrine_on_footpath", "Shrine built on footpath", "pole", {"clear_width_cm": 50, "crowd": 0.2}, perm(20), "yes", "pole_obstruction", ["F3.31"], ["religious"], A),
        ("kiosk_fixed", "Fixed vendor kiosk", "vendor", {"clear_width_cm": 60}, semi(120), "yes", "vendor", ["F3.12"], ["vendor"], A),
        ("otla_shop_platform", "Shop platform (otla) built onto footpath", "step", {"vertical_cm": 30, "clear_width_cm": 0, "detour_m": 20}, perm(5), "yes", "steps", ["F3.08"], ["step", "encroachment"], A),
        ("shop_steps_encroach", "Shop steps built into the footpath", "step", {"vertical_cm": 18, "spans_path": False, "clear_width_cm": 50}, perm(5), "yes", "steps", ["F3.08", "F4.17"], ["step", "encroachment"], A),
        ("generator_set", "Diesel generator on footpath", "pole", {"clear_width_cm": 50, "noise_db": 85, "air": 0.4, "heat": 0.2}, semi(60), "yes", "pole_obstruction", ["F3.17"], ["fumes"], A),
        ("atm_kiosk_step", "ATM kiosk with a step", "step", {"vertical_cm": 20, "spans_path": False, "clear_width_cm": 100}, perm(), "yes", "steps", ["F3.29"], ["step"], A),
        ("ac_unit_dripping", "AC units dripping onto footpath", "overhead", {"overhead": 0.2, "slip": 0.2, "cane_detectable": 0}, perm(), "partial", None, [], ["overhead"], A),
    ]),
    ("overhead", "Head-height hazards", [
        ("low_awning", "Shop awning below 2 m", "overhead", {}, semi(365), "partial", None, ["F1.27"], ["overhead"], A),
        ("low_branch", "Tree branch below 2 m", "overhead", {"overhead": 0.6}, semi(180), "partial", None, ["F1.27"], ["overhead", "tree"], A),
        ("low_signboard", "Signboard at head height", "overhead", {"overhead": 0.8}, semi(365), "partial", None, ["F1.27"], ["overhead", "metal"], A),
        ("vendor_umbrella_head_height", "Vendor umbrella at about 1.6 m", "overhead", {"overhead": 0.6, "crowd": 0.3}, temp(6, "vendor", 0.6), "partial", "vendor", ["M523"], ["overhead", "vendor"], A),
        ("overhead_wires_low", "Low overhead wires", "overhead", {"overhead": 0.5, "electric": 0.2}, semi(180), "partial", None, ["M524"], ["overhead", "electrical"], A),
        ("scaffolding_overhead", "Scaffolding over the footpath", "overhead", {"overhead": 0.6, "clear_width_cm": 80, "fall": 0.1}, temp(24 * 60), "yes", None, ["F3.17"], ["overhead", "construction", "metal"], A),
        ("hanging_banner", "Hanging banner or bunting", "overhead", {"overhead": 0.3}, event(24 * 5), "partial", None, ["F5.07"], ["overhead"], A),
        ("truck_tailgate_projection", "Parked truck tailgate projecting over path", "overhead", {"overhead": 0.6, "clear_width_cm": 80}, temp(3, "parked_vehicle"), "partial", "parked_vehicle", ["F3.30"], ["overhead", "vehicle"], A),
    ]),
])

cat("temporary_obstacles", "Temporary obstacles", [
    ("parked", "Parked and stopped vehicles", [
        ("two_wheeler_parked_footpath", "Two-wheelers parked on the footpath", "parked", {}, temp(2, "parked_vehicle", 0.35), "yes", "parked_vehicle", ["F3.13", "F4.03"], ["vehicle", "metal"], A),
        ("car_parked_footpath", "Car parked on the footpath", "parked", {"clear_width_cm": 30, "detour_m": 20}, temp(3, "parked_vehicle", 0.35), "yes", "parked_vehicle", ["F3.14"], ["vehicle", "metal"], A),
        ("car_on_kerb_ramp", "Car parked across the kerb ramp", "parked", {"clear_width_cm": 0, "spans_path": True, "detour_m": 60}, temp(2, "parked_vehicle", 0.3), "yes", "parked_vehicle", ["W13", "M13"], ["vehicle", "ramp_blocked"], A),
        ("auto_rickshaw_stand", "Auto-rickshaw stand on kerb", "parked", {"clear_width_cm": 70, "crowd": 0.3, "air": 0.2}, temp(4, "office_rush", 0.7), "yes", "parked_vehicle", ["F3.30"], ["vehicle"], A),
        ("e_rickshaw_queue", "E-rickshaw queue at kerb", "parked", {"clear_width_cm": 70, "vehicle": 0.3}, temp(2, "office_rush", 0.6), "yes", "parked_vehicle", [], ["vehicle", "silent_vehicle"], A),
        ("abandoned_vehicle", "Abandoned vehicle", "parked", {"clear_width_cm": 30, "detour_m": 20}, semi(120), "yes", "parked_vehicle", ["F3.15"], ["vehicle", "metal"], A),
        ("official_vehicle_parked", "Police / utility vehicle parked on footpath", "parked", {"clear_width_cm": 20}, temp(4), "yes", "parked_vehicle", ["F3.16", "F4.25"], ["vehicle"], A),
        ("loading_unloading", "Loading / unloading vehicle", "parked", {"clear_width_cm": 40, "vehicle": 0.4, "crowd": 0.3}, temp(0.5, "day", 0.5), "yes", "parked_vehicle", ["F3.30"], ["vehicle"], A),
        ("bicycle_dumped", "Bicycle lying on footpath", "parked", {"clear_width_cm": 80, "vertical_cm": 10, "fall": 0.2, "vehicle": 0}, temp(12), "yes", "parked_vehicle", ["M522"], ["metal"], A),
        ("shared_scooter_dumped", "Shared e-scooter lying across path", "parked", {"clear_width_cm": 60, "vertical_cm": 12, "fall": 0.25, "vehicle": 0}, temp(12), "yes", "parked_vehicle", ["M522"], ["metal"], A),
        ("delivery_bikes_cluster", "Cluster of delivery bikes outside restaurant", "parked", {"clear_width_cm": 40, "vehicle": 0.3}, temp(2, "evening_market", 0.7), "yes", "parked_vehicle", ["F4.02", "F13.13"], ["vehicle"], A),
    ]),
    ("vendors", "Vendors and commerce", [
        ("vendor_handcart", "Vendor handcart", "vendor", {}, temp(6, "vendor", 0.6), "yes", "vendor", ["F3.11"], ["vendor"], A),
        ("vendor_ground_mat", "Vendor goods on a mat on the ground", "vendor", {"clear_width_cm": 50, "vertical_cm": 2, "cane_detectable": 0.6}, temp(6, "vendor", 0.6), "yes", "vendor", ["F4.04"], ["vendor"], A),
        ("cafe_seating_spill", "Cafe seating spilling onto footpath", "vendor", {"clear_width_cm": 60, "noise_db": 72}, temp(6, "evening_market", 0.8), "yes", "vendor", ["F3.10", "F4.06"], ["vendor"], A),
        ("shop_display_spill", "Shop goods displayed on footpath", "vendor", {"clear_width_cm": 60}, temp(10, "day", 0.9), "yes", "vendor", ["F4.17"], ["vendor", "encroachment"], A),
        ("queue_outside_shop", "Queue outside a shop", "crowd", {"crowd": 0.6, "clear_width_cm": 70}, temp(2, "day", 0.5), "partial", None, ["F3.29"], ["crowd"], A),
        ("tea_stall_crowd", "Crowd around a tea stall", "crowd", {"crowd": 0.6, "clear_width_cm": 60, "air": 0.15}, temp(2, "office_rush", 0.8), "yes", "vendor", ["F3.29"], ["crowd", "vendor"], A),
        ("fruit_crates", "Crates stacked on footpath", "debris", {"clear_width_cm": 60, "vertical_cm": 40, "fall": 0.1, "roughness": 0.1}, temp(8, "day", 0.6), "yes", "vendor", ["F4.17"], ["vendor"], A),
        ("weekend_market_crowd", "Weekend market-street crowd", "crowd", {"crowd": 0.75, "clear_width_cm": 70}, event(8, "evening_market", "all"), "partial", "vendor", ["F5.02"], ["crowd", "vendor"], A),
        ("weekly_bazaar", "Weekly bazaar on the street", "event", {"crowd": 0.85, "clear_width_cm": 40, "noise_db": 80}, event(14, "day", "all"), "yes", "vendor", ["F5.15", "W158"], ["vendor", "crowd"], A),
        ("food_cart_fire", "Food cart with open flame / tandoor", "vendor", {"clear_width_cm": 70, "heat": 0.4, "air": 0.4}, temp(6, "evening_market", 0.7), "yes", "vendor", [], ["vendor", "smoke"], A),
    ]),
    ("construction", "Construction, works and waste", [
        ("dry_season_trenching", "Dry-season utility trenching wave", "debris", {"clear_width_cm": 30, "roughness": 0.8, "fall": 0.5, "vertical_cm": 40}, temp(24 * 30, "day", 0.3, "dry"), "partial", "broken_footpath", ["F5.16", "F5.10"], ["construction", "hole"], A),
        ("construction_pipes", "Construction pipes and material", "debris", {"clear_width_cm": 30}, temp(24 * 30), "yes", "broken_footpath", ["F3.17"], ["construction"], A),
        ("construction_debris", "Construction debris heap", "debris", {}, temp(24 * 14), "yes", "broken_footpath", ["F3.18", "F2.13"], ["construction", "dust"], A),
        ("sand_heap", "Sand heap on footpath", "debris", {"clear_width_cm": 30, "vertical_cm": 40, "slip": 0.3, "air": 0.25}, temp(24 * 7), "yes", "broken_footpath", ["F2.13"], ["construction", "dust"], A),
        ("soil_heap", "Excavated soil heap", "debris", {"clear_width_cm": 30, "vertical_cm": 50, "slip": 0.3}, temp(24 * 14), "yes", "broken_footpath", ["F2.13"], ["construction"], A),
        ("garbage_heap", "Garbage heap on footpath", "debris", {"clear_width_cm": 40, "vertical_cm": 30, "air": 0.3, "animal": 0.3, "slip": 0.2}, temp(48, rec=0.6), "yes", "broken_footpath", ["F2.28", "F3.19"], ["garbage"], A),
        ("garbage_bin_overflow", "Overflowing garbage bin", "debris", {"clear_width_cm": 70, "vertical_cm": 10, "air": 0.3, "animal": 0.3}, temp(24, rec=0.6), "yes", None, ["F5.14"], ["garbage"], A),
        ("metro_barricade", "Metro construction barricade", "width", {"clear_width_cm": 0, "spans_path": True, "detour_m": 200, "noise_db": 80, "air": 0.3}, semi(365 * 2), "yes", None, ["F3.22", "F8.12"], ["construction", "metal"], A),
        ("police_barricade", "Police barricade", "width", {"clear_width_cm": 50, "detour_m": 40}, temp(24 * 3), "yes", None, ["F3.22"], ["metal"], A),
        ("dug_footpath_unrestored", "Dug-up footpath left unrestored", "debris", {"clear_width_cm": 0, "spans_path": True, "roughness": 0.9, "detour_m": 60}, temp(24 * 45), "yes", "broken_footpath", ["F2.12"], ["construction"], A),
        ("scaffold_ground_poles", "Scaffold poles standing in path", "pole", {"clear_width_cm": 60, "overhead": 0.2}, temp(24 * 60), "yes", None, ["F3.17"], ["construction", "metal"], A),
        ("cement_mixer", "Cement mixer on footpath", "debris", {"clear_width_cm": 30, "noise_db": 85, "air": 0.3, "slip": 0.3}, temp(24 * 3, "day"), "yes", None, ["F3.17"], ["construction", "dust"], A),
        ("half_built_footpath", "Half-finished footpath works", "debris", {"clear_width_cm": 30, "vertical_cm": 20, "roughness": 0.8}, temp(24 * 60), "yes", "broken_footpath", ["F2.14"], ["construction"], A),
        ("incomplete_fob_ramp", "Incomplete bridge / ramp", "step", {"vertical_cm": 300, "spans_path": True, "detour_m": 300}, semi(365), "partial", None, ["F2.15"], ["construction"], A),
        ("broken_bollard_lying", "Broken bollard lying on footpath", "debris", {"clear_width_cm": 90, "vertical_cm": 15, "fall": 0.3}, semi(60), "yes", "broken_footpath", ["F2.27"], ["metal"], A),
        ("fallen_hoarding", "Fallen hoarding after storm", "debris", {"clear_width_cm": 0, "spans_path": True, "detour_m": 80}, temp(48), "yes", None, ["F6.18"], ["metal"], A),
    ]),
    ("events", "Events, festivals and closures", [
        ("festival_pandal", "Festival pandal on footpath / road", "event", {"clear_width_cm": 0, "detour_m": 150}, event(24 * 10), "yes", None, ["F3.23", "F5.06"], ["festival", "crowd"], A),
        ("wedding_shamiana", "Wedding tent on the road", "event", {"clear_width_cm": 0, "detour_m": 100, "noise_db": 95}, event(36, "festival_evening", "all"), "yes", None, ["F3.24"], ["festival", "loud"], A),
        ("procession_baraat", "Procession or wedding baraat", "event", {"crowd": 0.9, "noise_db": 100, "vehicle": 0.3, "flicker": 0.4, "detour_m": 200}, event(3, "festival_evening", "all"), "partial", None, ["F4.13"], ["festival", "loud", "crowd"], A),
        ("protest_rally", "Protest or rally blocking road", "event", {"crowd": 0.9, "noise_db": 90, "clear_width_cm": 0, "detour_m": 300}, event(6, "day", "all"), "partial", None, ["F4.14"], ["crowd"], A),
        ("vvip_road_closure", "VVIP movement road closure", "event", {"crowd": 0.2, "wait_s": 900, "noise_db": 70, "clear_width_cm": None}, event(2, "day", "all"), "no", None, ["F4.15"], [], A),
        ("ganesh_visarjan", "Immersion procession (Ganesh visarjan)", "event", {"crowd": 1.0, "noise_db": 105, "flicker": 0.5, "detour_m": 300, "water_cm": 2}, event(12, "festival_evening"), "partial", None, ["F5.06"], ["festival", "loud", "crowd"], A),
        ("holi_crowd", "Holi street crowd with colour", "event", {"crowd": 0.8, "noise_db": 90, "air": 0.4, "slip": 0.3, "contrast_loss": 0.2}, event(8, "day"), "partial", None, ["F5.06"], ["festival", "crowd"], A),
        ("diwali_firecracker_zone", "Firecrackers on the road (Diwali)", "event", {"crowd": 0.5, "noise_db": 120, "air": 0.7, "heat": 0.3, "flicker": 0.8, "fall": 0.1}, event(6, "night"), "partial", None, ["F5.06", "W69"], ["festival", "loud", "smoke"], A),
        ("election_rally_structures", "Election posters, stages, barricades", "event", {"crowd": 0.5, "noise_db": 85, "clear_width_cm": 60}, event(24 * 3, "day", "all"), "yes", None, ["F5.07"], ["crowd"], A),
        ("durga_puja_lane_crowd", "Durga Puja pandal approach lane crowd", "event", {"crowd": 1.0, "clear_width_cm": 80, "noise_db": 90, "detour_m": 0}, event(24 * 5), "partial", None, ["F14.08", "S60"], ["festival", "crowd", "narrow"], A),
        ("religious_queue_darshan", "Temple darshan queue on footpath", "crowd", {"crowd": 0.8, "clear_width_cm": 50, "wait_s": 60}, temp(3, "temple", 0.9), "partial", None, ["F5.18"], ["crowd", "religious"], A),
        ("pilgrimage_route_crowd", "Pilgrimage route crowd (yatra season)", "crowd", {"crowd": 0.9, "clear_width_cm": 80, "effort": 0.5}, event(24 * 10, "temple", "monsoon"), "partial", None, ["F8.16", "F5.18"], ["crowd", "religious"], A),
        ("sports_event_exit", "Stadium exit surge", "crowd", {"crowd": 1.0, "noise_db": 90, "clear_width_cm": 100}, event(2, "festival_evening", "all"), "no", None, [], ["crowd"], A),
    ]),
    ("people_animals", "People and animals on the path", [
        ("stray_cattle", "Stray cattle resting on path", "animal", {"animal": 0.4, "clear_width_cm": 50}, temp(2, "day", 0.4), "yes", None, ["F3.26", "F14.03"], ["animal"], "FU"),
        ("stray_dog_pack", "Stray dog pack", "animal", {"animal": 0.7, "clear_width_cm": 100}, temp(24 * 7, "night", 0.7), "yes", None, ["F3.27", "F14.01", "F14.02"], ["animal", "dog"], "FU"),
        ("single_dog_sleeping", "Street dog sleeping across the gap", "animal", {"animal": 0.3, "clear_width_cm": 60}, temp(3, "day", 0.6), "yes", None, ["M515"], ["animal", "dog"], A),
        ("monkeys", "Monkey troop (temple / hill towns)", "animal", {"animal": 0.6, "overhead": 0.2}, temp(2, "day", 0.6), "partial", None, ["F14.19"], ["animal"], A),
        ("goat_herd", "Goat or sheep herd crossing", "animal", {"animal": 0.2, "clear_width_cm": 30, "crowd": 0.4}, temp(0.5, "day"), "yes", None, [], ["animal"], A),
        ("camel_horse_cart", "Camel or horse cart on road edge", "animal", {"animal": 0.3, "vehicle": 0.3, "clear_width_cm": 100}, temp(0.5, "day"), "yes", None, ["F8.05"], ["animal", "vehicle"], A),
        ("open_urination_spot", "Open urination / spitting spot", "slippery", {"slip": 0.3, "air": 0.25, "spans_path": False, "clear_width_cm": 90}, perm(1), "partial", None, ["F4.18"], ["wet_slippery", "odour"], A),
        ("pigeon_feeding_spot", "Pigeon feeding spot (droppings, birds)", "animal", {"animal": 0.1, "slip": 0.3, "air": 0.2}, perm(5), "yes", None, [], ["animal", "wet_slippery"], A),
        ("people_sleeping_night", "People sleeping on the footpath at night (route around, never labelled publicly)", "width", {"clear_width_cm": 60, "cane_detectable": 0.9}, temp(8, "night", 0.8), "partial", None, ["F3.28", "W111"], ["dignity"], A),
        ("snakes_flooded_rural", "Snakes on flooded rural paths", "animal", {"animal": 0.5, "visibility_needed": 0.9}, weather("monsoon", 24), "no", None, ["F14.20"], ["animal"], A),
    ]),
])

cat("traffic_crossings", "Traffic and crossings", [
    ("crossings", "Crossings and signals", [
        ("zebra_good", "Marked zebra crossing, fresh paint", "crossing", {"green_s": 20, "vehicle": 0.4, "wait_s": 20, "relief": 0.2}, semi(365), "yes", None, ["F2.20"], ["crossing", "marking"], A),
        ("zebra_faded", "Faded zebra crossing", "crossing", {"vehicle": 0.6, "contrast_loss": 0.4}, semi(180), "yes", None, ["F2.20", "S63"], ["crossing", "marking", "faded"], "FU"),
        ("no_marked_crossing", "No marked crossing at all", "crossing", {"vehicle": 0.7, "wait_s": 45, "cognitive": 0.5}, perm(), "partial", None, ["F4.09"], ["crossing"], A),
        ("crossing_4plus_lanes", "Crossing 4+ lanes", "crossing", {"crossing_length_m": 16, "vehicle": 0.75, "wait_s": 60, "effort": 0.3}, perm(), "partial", None, ["F1.22"], ["crossing", "wide_road"], A),
        ("no_median_refuge", "Wide crossing with no median refuge", "crossing", {"crossing_length_m": 18, "vehicle": 0.7, "effort": 0.3}, perm(), "partial", None, ["F1.21"], ["crossing", "wide_road"], A),
        ("signal_dead", "Traffic signal dead", "crossing", {"vehicle": 0.8, "wait_s": 60, "cognitive": 0.5}, temp(72, rec=0.3), "no", None, ["F4.10", "F9.24"], ["crossing"], "FU"),
        ("signal_short_green", "Pedestrian green too short (vehicle-first signal)", "crossing", {"crossing_length_m": 14, "green_s": 8, "vehicle": 0.6, "wait_s": 90, "effort": 0.4}, perm(), "no", None, ["F5.13", "S66"], ["crossing", "signal"], "FU"),
        ("signal_no_audio", "Signal with no audible cue", "crossing", {"green_s": 20, "vehicle": 0.5, "wait_s": 40, "cognitive": 0.3}, perm(), "no", None, ["W18"], ["crossing", "signal"], A),
        ("signal_audible", "Accessible signal with audible cue", "positive", {"crossing_length_m": 10, "green_s": 20, "relief": 0.7, "wait_s": 40, "vehicle": 0.2, "spans_path": True}, perm(), "no", None, ["F1.29"], ["crossing", "signal", "clear"], A),
        ("free_left_turn", "Free left turn slip lane", "crossing", {"vehicle": 0.8, "wait_s": 30, "cognitive": 0.4}, perm(), "partial", None, [], ["crossing"], A),
        ("roundabout_crossing", "Crossing at a roundabout", "crossing", {"crossing_length_m": 12, "vehicle": 0.75, "wait_s": 60, "cognitive": 0.6}, perm(), "partial", None, [], ["crossing"], A),
        ("high_speed_uncontrolled", "Uncontrolled crossing of a fast road", "crossing", {"crossing_length_m": 14, "vehicle": 0.95, "wait_s": 90, "cognitive": 0.6}, perm(), "partial", None, ["F14.10"], ["crossing", "fast_road"], A),
        ("rail_level_crossing", "Rail level crossing (gate)", "crossing", {"vehicle": 0.4, "wait_s": 300, "roughness": 0.6, "vertical_cm": 3}, perm(), "yes", None, ["F8.09"], ["crossing", "rail"], A),
        ("rail_flangeway_gap", "Rail flangeway gap (caster trap)", "hole", {"vertical_cm": 5, "fall": 0.4, "spans_path": True, "clear_width_cm": None}, perm(), "partial", None, ["F8.09"], ["rail", "metal"], A),
        ("median_gap_vehicles", "Median gap shared with U-turning vehicles", "crossing", {"vehicle": 0.8, "wait_s": 40}, perm(), "partial", None, ["W125"], ["crossing"], A),
        ("crossing_kerbs_both_sides", "Crossing with a kerb on both sides", "kerb", {"vertical_cm": 15, "vehicle": 0.4}, perm(), "partial", "missing_kerb_ramp", ["F1.03"], ["kerb", "crossing"], A),
    ]),
    ("moving_traffic", "Moving vehicles near walkers", [
        ("two_wheelers_on_footpath", "Two-wheelers riding on the footpath", "traffic", {"vehicle": 0.6, "noise_db": 72}, temp(1, "office_rush", 0.8), "partial", None, ["F4.01", "F4.02"], ["vehicle", "footpath_riding"], "FU"),
        ("wrong_side_traffic", "Wrong-side traffic near crossing", "traffic", {"vehicle": 0.7, "cognitive": 0.4}, temp(1, "office_rush", 0.7), "partial", None, ["F4.08"], ["vehicle"], A),
        ("no_footpath_road_walk", "No footpath: walking in the carriageway", "traffic", {"vehicle": 0.8, "spans_path": True, "roughness": 0.2}, perm(), "yes", "missing_footpath", ["F1.01", "F14.11"], ["vehicle", "road_walk"], A),
        ("village_highway_no_footpath", "Highway through village, no footpath", "traffic", {"vehicle": 0.95, "noise_db": 85, "spans_path": True}, perm(), "yes", "missing_footpath", ["F8.08"], ["vehicle", "road_walk", "fast_road"], A),
        ("fast_road_edge", "Walking beside fast traffic without buffer", "traffic", {"vehicle": 0.6, "noise_db": 80, "air": 0.3}, perm(), "partial", None, ["F14.10"], ["vehicle", "fast_road"], A),
        ("bus_stop_bus_pullin", "Bus pulling into kerb at stop", "traffic", {"vehicle": 0.5, "crowd": 0.5, "air": 0.3}, temp(1, "office_rush", 0.9), "yes", None, [], ["vehicle", "crowd"], A),
        ("silent_ev_traffic", "Silent electric vehicles (e-rickshaws, EV scooters)", "traffic", {"vehicle": 0.5, "noise_db": None}, temp(1, "day", 0.9), "partial", None, [], ["vehicle", "silent_vehicle"], A),
        ("reversing_vehicles_driveway", "Vehicles reversing out of driveways", "traffic", {"vehicle": 0.5}, temp(1, "office_rush", 0.6), "partial", None, ["F1.12"], ["vehicle"], A),
        ("honking_dense_traffic", "Dense honking traffic", "traffic", {"vehicle": 0.5, "noise_db": 90, "cognitive": 0.4}, temp(2, "office_rush", 0.9), "no", None, [], ["vehicle", "loud"], A),
        ("truck_zone_industrial", "Industrial area with trucks", "traffic", {"vehicle": 0.85, "noise_db": 85, "air": 0.4}, perm(), "partial", None, ["F8.22"], ["vehicle", "fast_road"], A),
        ("school_van_drop", "School vans and parents at gate", "traffic", {"vehicle": 0.5, "crowd": 0.6}, temp(1, "school", 0.9), "partial", None, ["F5.03"], ["vehicle", "crowd"], A),
    ]),
])

cat("light_time", "Time of day, sun, shadow and lighting", [
    ("time_of_day", "Time of day", [
        ("time_dawn", "Dawn (low light)", "light", {"contrast_loss": 0.5, "glare": 0.3}, ambient("dawn_dusk"), "yes", None, ["F5.17"], ["low_light", "time"], A),
        ("time_morning", "Morning", "light", {"heat": 0.1}, ambient("day"), "yes", None, ["F5.01"], ["time", "daylight"], A),
        ("time_midday", "Midday", "light", {"heat": 0.5, "glare": 0.3}, ambient("midday_heat"), "yes", None, ["F5.01"], ["time", "daylight", "unshaded"], A),
        ("time_dusk", "Dusk", "light", {"contrast_loss": 0.55, "glare": 0.4}, ambient("dawn_dusk"), "yes", None, ["F5.17"], ["low_light", "time"], A),
        ("time_night_lit", "Night, street lit", "light", {"contrast_loss": 0.5, "glare": 0.3}, ambient("night"), "yes", None, ["F5.05"], ["night", "time"], A),
        ("time_night_dark", "Night, no working streetlight", "light", {"contrast_loss": 0.95, "visibility_needed": 0.0}, ambient("night"), "yes", None, ["F5.05", "M530"], ["night", "dark", "time"], A),
        ("time_late_night", "Late night (few people around)", "social", {"contrast_loss": 0.6, "cognitive": 0.2}, ambient("night"), "yes", None, ["F14.05", "F7.16"], ["night", "isolated", "time"], A),
        ("office_rush_window", "Office rush window", "crowd", {"crowd": 0.6, "vehicle": 0.4, "noise_db": 78, "clear_width_cm": None}, ambient("office_rush"), "no", None, ["F5.04"], ["time", "crowd"], A),
        ("school_dispersal_window", "School dispersal window", "crowd", {"crowd": 0.85, "vehicle": 0.4, "noise_db": 80, "clear_width_cm": 100}, ambient("school"), "no", None, ["F5.03", "M521"], ["time", "crowd"], A),
        ("evening_market_peak", "Evening market peak", "crowd", {"crowd": 0.8, "clear_width_cm": 70, "noise_db": 78}, ambient("evening_market"), "no", None, ["F5.01"], ["time", "crowd", "vendor"], A),
        ("waste_collection_hour", "Waste collection hour (bins out)", "debris", {"clear_width_cm": 80, "air": 0.2, "vertical_cm": 0, "fall": 0, "roughness": 0}, ambient("day"), "no", None, ["F5.14"], ["time", "garbage"], A),
    ]),
    ("sun_shadow", "Sun angle, shadow and glare", [
        ("low_sun_glare_ew", "Low sun glare on east-west street", "light", {"glare": 0.85, "contrast_loss": 0.4}, ambient("dawn_dusk"), "partial", None, ["F7.07"], ["glare", "sun"], A),
        ("high_sun_no_shade", "High sun on an unshaded stretch", "light", {"heat": 0.7, "glare": 0.4}, ambient("midday_heat", "summer"), "partial", None, ["F6.08"], ["sun", "unshaded"], A),
        ("deep_shadow_band", "Deep shadow band hiding the surface", "light", {"contrast_loss": 0.6}, ambient("day"), "yes", None, ["F7.09"], ["shadow"], A),
        ("dappled_tree_shadow", "Dappled tree shadow (pattern confuses edges)", "light", {"contrast_loss": 0.4, "flicker": 0.15, "cognitive": 0.1}, ambient("day"), "yes", None, ["F7.09"], ["shadow"], A),
        ("shadow_hides_defect", "Shadow hiding a surface defect", "light", {"contrast_loss": 0.5, "visibility_needed": 0.6, "fall": 0.15}, ambient("day"), "partial", None, ["F7.09", "W51"], ["shadow"], A),
        ("wet_road_glare", "Glare off a wet road", "light", {"glare": 0.7, "contrast_loss": 0.4}, weather("monsoon", 3), "partial", None, ["F7.06"], ["glare", "wet"], A),
        ("headlight_glare", "Oncoming headlight glare", "light", {"glare": 0.8, "contrast_loss": 0.3, "vehicle": 0.2}, ambient("night"), "partial", None, ["F7.06"], ["glare", "night"], A),
        ("glass_facade_glare", "Reflective glass facade glare", "light", {"glare": 0.6}, ambient("day"), "partial", None, [], ["glare"], A),
        ("shade_canopy", "Continuous tree shade", "positive", {"relief": 0.7, "heat": -0.3}, perm(20), "yes", None, ["F6.08"], ["shade", "clear"], "FU"),
    ]),
    ("lighting", "Street lighting", [
        ("streetlight_off", "Streetlight off on the stretch", "light", {"contrast_loss": 0.8}, temp(24 * 14, "night", 0.5), "partial", None, ["F7.01", "W72"], ["dark", "night"], "FU"),
        ("streetlight_sparse", "Streetlights spaced too far apart", "light", {"contrast_loss": 0.6}, perm(), "partial", None, ["F7.04"], ["dark", "night"], A),
        ("police_dark_spot", "Police-listed dark spot", "social", {"contrast_loss": 0.8, "cognitive": 0.3}, perm(2), "no", None, ["F7.03", "F14.04"], ["dark", "night", "isolated"], "FU"),
        ("power_cut", "Power cut (all lights off)", "light", {"contrast_loss": 0.95}, temp(2, "night"), "no", None, ["F7.10"], ["dark", "night"], A),
        ("shop_lights_only", "Shop lights only (dark after closing)", "light", {"contrast_loss": 0.6}, ambient("night"), "partial", None, ["F7.11"], ["dark", "night"], A),
        ("fob_subway_lights_off", "FOB / subway lights not working", "light", {"contrast_loss": 0.9, "cognitive": 0.3}, temp(24 * 14), "no", None, ["F7.12"], ["dark"], A),
        ("flickering_light", "Flickering streetlight or sign", "light", {"flicker": 0.8, "contrast_loss": 0.3}, semi(30, "night"), "no", None, [], ["flicker", "night"], A),
        ("led_billboard_flashing", "Flashing LED billboard", "light", {"flicker": 0.9, "glare": 0.5, "cognitive": 0.3}, perm(3), "partial", None, [], ["flicker", "glare"], A),
        ("well_lit_stretch", "Well-lit stretch", "positive", {"relief": 0.5}, perm(), "partial", None, ["F7.15"], ["lit", "clear"], A),
    ]),
    ("contrast_signage", "Contrast, markings and signage", [
        ("kerb_edge_no_contrast", "Kerb edge with no colour contrast", "light", {"contrast_loss": 0.6, "visibility_needed": 0.7, "fall": 0.2, "vertical_cm": 15, "spans_path": False}, perm(), "yes", None, ["F1.34", "F7.08"], ["low_contrast", "kerb"], "FU"),
        ("step_nosing_no_contrast", "Step nosings with no contrast", "light", {"contrast_loss": 0.6, "visibility_needed": 0.8, "fall": 0.3, "vertical_cm": 15}, perm(), "yes", "steps", ["F7.08"], ["low_contrast", "step"], A),
        ("faded_road_markings", "Faded road markings", "light", {"contrast_loss": 0.4, "cognitive": 0.2}, semi(180), "yes", None, ["F2.20", "S70"], ["marking", "faded"], A),
        ("no_signage", "No wayfinding signage", "light", {"cognitive": 0.6}, perm(), "partial", None, ["M7"], ["signage"], A),
        ("text_only_signage", "Text-only signage (no pictograms)", "light", {"cognitive": 0.5}, perm(), "yes", None, ["C1.7"], ["signage"], "HERMES_BODY"),
        ("signage_other_script", "Signage only in a script the user cannot read", "light", {"cognitive": 0.5}, perm(), "yes", None, ["F8.26"], ["signage"], A),
        ("complex_junction", "Complex multi-arm junction", "crossing", {"cognitive": 0.8, "vehicle": 0.6, "wait_s": 40}, perm(), "partial", None, ["F10.17"], ["crossing", "complex"], A),
        ("reflective_studs", "Reflective studs and markings", "positive", {"relief": 0.3}, semi(365), "yes", None, ["F7.14"], ["marking", "clear"], A),
    ]),
])

cat("weather", "Weather and season", [
    ("rain_water", "Rain and water on the ground", [
        ("drizzle", "Drizzle", "weather", {"slip": 0.2, "contrast_loss": 0.15}, weather("monsoon", 2), "partial", None, ["F6.01"], ["rain", "wet"], A),
        ("rain_moderate", "Moderate rain", "weather", {"slip": 0.35, "contrast_loss": 0.3, "noise_db": 65}, weather("monsoon", 3), "partial", None, ["F6.01"], ["rain", "wet"], A),
        ("rain_heavy", "Heavy rain (about 70 mm/h)", "weather", {"slip": 0.5, "contrast_loss": 0.5, "noise_db": 75, "water_cm": 3}, weather("monsoon", 2), "partial", None, ["F6.01", "S45"], ["rain", "wet", "heavy_rain"], "FU"),
        ("waterlogging_shallow", "Waterlogging, a few cm", "weather", {"water_cm": 5, "slip": 0.3, "visibility_needed": 0.8, "cane_detectable": 0.4}, weather("monsoon", 24), "partial", "waterlogging", ["F3.25", "F6.02"], ["water", "flood"], A),
        ("waterlogging_deep", "Waterlogging, 20 cm or more", "weather", {"water_cm": 25, "slip": 0.4, "fall": 0.3, "visibility_needed": 1.0, "cane_detectable": 0.2, "detour_m": 200}, weather("monsoon", 24), "partial", "waterlogging", ["F6.02", "W27"], ["water", "flood"], A),
        ("flooded_underpass", "Flooded underpass", "weather", {"water_cm": 60, "fall": 0.5, "electric": 0.2, "detour_m": 400}, weather("monsoon", 12), "partial", "waterlogging", ["F1.24"], ["water", "flood"], A),
        ("flowing_water_street", "Water flowing across the street", "weather", {"water_cm": 15, "slip": 0.5, "fall": 0.5}, weather("monsoon", 2), "partial", "waterlogging", ["F14.14"], ["water", "flood"], A),
        ("puddle_reflection", "Puddle (reflection, depth unknown)", "weather", {"water_cm": 3, "visibility_needed": 0.7, "spans_path": False, "clear_width_cm": 80}, weather("monsoon", 12), "yes", "waterlogging", ["F12.08"], ["water"], A),
        ("electrified_water", "Electrified water near a pole", "weather", {"water_cm": 10, "electric": 1.0}, weather("monsoon", 6), "no", None, ["F6.04", "F14.09"], ["water", "electrical"], "FU"),
        ("mud_after_rain", "Mud and slush after rain", "surface", {"roughness": 0.8, "slip": 0.6, "water_cm": 2}, weather("monsoon", 48), "partial", None, ["F6.17"], ["unpaved", "wet_slippery"], A),
        ("storm_drain_overflow", "Storm drain overflowing", "weather", {"water_cm": 10, "air": 0.3, "fall": 0.4}, weather("monsoon", 6), "partial", "waterlogging", ["F5.10"], ["water", "drain"], A),
        ("high_tide_flood", "High tide plus heavy rain flooding (coastal)", "weather", {"water_cm": 30, "detour_m": 300}, weather("monsoon", 6), "no", "waterlogging", ["F6.16"], ["water", "flood"], A),
        ("water_stain_line", "Water stain line (past flood marker)", "positive", {"relief": 0.0}, perm(), "partial", None, ["MAXINFO-3"], ["flood_prone"], A),
    ]),
    ("wind_storm", "Wind, storm and lightning", [
        ("dust_storm", "Dust storm (visibility near zero)", "weather", {"air": 0.9, "contrast_loss": 0.9, "overhead": 0.3, "noise_db": 80}, weather("summer", 3), "partial", None, ["F6.10", "S47"], ["dust", "storm"], "FU"),
        ("wind_gusts", "Strong wind gusts", "weather", {"overhead": 0.3, "effort": 0.3, "air": 0.2}, weather("summer", 3), "no", None, ["F6.18"], ["storm"], "FU"),
        ("cyclone_warning", "Cyclone warning in force", "weather", {"overhead": 0.6, "water_cm": 20, "electric": 0.3, "effort": 0.6}, weather("monsoon", 24), "no", None, ["F6.15"], ["storm", "water"], A),
        ("falling_branch_risk", "Falling branch risk in wind", "weather", {"overhead": 0.5}, weather("monsoon", 6), "no", None, ["F6.05", "F14.15"], ["storm", "tree"], "FU"),
        ("tree_fallen", "Fallen tree blocking path", "debris", {"clear_width_cm": 0, "spans_path": True, "vertical_cm": 50, "detour_m": 100, "electric": 0.1}, temp(24), "yes", None, ["F3.20"], ["tree", "storm"], "FU"),
        ("lightning_risk", "Lightning risk on open route", "weather", {"electric": 0.15}, weather("monsoon", 2), "no", None, ["F6.19"], ["storm"], A),
        ("hoarding_collapse_risk", "Hoarding collapse risk in storm", "weather", {"overhead": 0.4}, weather("summer", 3), "no", None, ["F13.17"], ["storm", "metal"], A),
    ]),
    ("heat_cold", "Heat and cold", [
        ("hot_day_40", "Hot day, 40 C (heat wave threshold, plains)", "weather", {"heat": 0.6}, weather("summer", 8, "midday_heat"), "no", None, ["F6.06"], ["heat"], "IMD_HEAT"),
        ("heatwave_45", "Heat wave, 45 C", "weather", {"heat": 0.85, "effort": 0.3}, weather("summer", 8, "midday_heat"), "no", None, ["F6.06", "S49"], ["heat"], "IMD_HEAT"),
        ("severe_heat_47", "Severe heat wave, 47 C", "weather", {"heat": 1.0, "effort": 0.5}, weather("summer", 8, "midday_heat"), "no", None, ["F6.06"], ["heat"], "IMD_HEAT"),
        ("hot_humid_heat_index", "Hot and humid (high heat index)", "weather", {"heat": 0.8, "effort": 0.4}, weather("monsoon", 8, "midday_heat"), "no", None, ["F6.21"], ["heat"], A),
        ("hot_metal_surface", "Sun-heated metal (railing, handrim, cover)", "weather", {"heat": 0.5, "spans_path": False}, weather("summer", 6, "midday_heat"), "no", None, ["F6.07", "M532"], ["heat", "metal"], A),
        ("hot_dark_paving", "Sun-heated dark paving (about 55 C)", "weather", {"heat": 0.6}, weather("summer", 6, "midday_heat"), "no", None, ["INDIA-CHAOS-10"], ["heat", "dark_surface"], A),
        ("warm_night", "Warm night (no cooling)", "weather", {"heat": 0.4}, weather("summer", 10, "night"), "no", None, [], ["heat", "night"], A),
        ("cold_wave", "Cold wave", "weather", {"cold": 0.7}, weather("winter", 24), "no", None, ["F6.20"], ["cold"], A),
        ("morning_ice_shaded", "Morning ice on shaded slope", "slippery", {"slip": 0.9, "cold": 0.5}, weather("winter", 4, "fog_morning"), "partial", None, ["F6.13"], ["ice", "wet_slippery"], A),
        ("snow_cover", "Snow on the path", "weather", {"slip": 0.6, "roughness": 0.6, "cold": 0.8, "water_cm": 10, "contrast_loss": 0.4}, weather("winter", 48), "yes", None, ["F6.12", "F3.33"], ["snow", "cold"], "FU"),
        ("slush", "Slush", "slippery", {"slip": 0.7, "water_cm": 5, "cold": 0.5}, weather("winter", 24), "yes", None, ["F3.33"], ["snow", "wet_slippery"], A),
    ]),
    ("visibility_weather", "Fog, smog and haze", [
        ("dense_fog", "Dense fog (visibility about 150 m or less)", "weather", {"contrast_loss": 0.85, "vehicle": 0.3, "cold": 0.3}, weather("winter", 4, "fog_morning"), "partial", None, ["F6.09", "S48"], ["fog"], "FU"),
        ("moderate_fog", "Moderate fog", "weather", {"contrast_loss": 0.5, "vehicle": 0.15}, weather("winter", 4, "fog_morning"), "partial", None, ["F6.09"], ["fog"], A),
        ("smog", "Smog", "weather", {"contrast_loss": 0.5, "air": 0.8}, weather("winter_smog", 12), "partial", None, ["F6.11"], ["smog", "air"], "FU"),
        ("haze", "Haze", "weather", {"contrast_loss": 0.3, "air": 0.4}, weather("winter_smog", 12), "partial", None, ["F6.23"], ["air"], A),
        ("rain_curtain", "Heavy rain curtain (low visibility)", "weather", {"contrast_loss": 0.6, "slip": 0.4, "noise_db": 75}, weather("monsoon", 1), "partial", None, ["F6.01"], ["rain", "heavy_rain"], A),
    ]),
])

cat("air_noise", "Things in the air and sound", [
    ("air", "Air quality, dust and smoke", [
        ("aqi_moderate_150", "AQI 101-200 (moderately polluted)", "air", {"air": 0.35}, weather("winter_smog", 24), "no", None, ["F6.11"], ["air", "aqi"], "CPCB_AQI"),
        ("aqi_poor_250", "AQI 201-300 (poor)", "air", {"air": 0.55}, weather("winter_smog", 24), "no", None, ["F6.11"], ["air", "aqi"], "CPCB_AQI"),
        ("aqi_very_poor_350", "AQI 301-400 (very poor)", "air", {"air": 0.75}, weather("winter_smog", 24), "no", None, ["F6.11", "W145"], ["air", "aqi"], "CPCB_AQI"),
        ("aqi_severe_450", "AQI 401-500 (severe)", "air", {"air": 0.95}, weather("winter_smog", 24), "no", None, ["F6.11", "W145"], ["air", "aqi"], "CPCB_AQI"),
        ("road_dust_resuspension", "Road dust kicked up by traffic", "air", {"air": 0.45, "contrast_loss": 0.1}, temp(2, "office_rush", 0.9, "dry"), "partial", None, ["F3.34"], ["dust", "air"], A),
        ("construction_dust", "Construction dust", "air", {"air": 0.6, "contrast_loss": 0.15}, temp(24 * 7, "day"), "partial", None, ["F2.13"], ["dust", "air"], A),
        ("garbage_burning_smoke", "Garbage burning smoke", "air", {"air": 0.7, "contrast_loss": 0.2, "heat": 0.1}, temp(3, "evening_market", 0.5, "winter_smog"), "partial", None, [], ["smoke", "air"], A),
        ("crop_burning_smoke", "Crop residue smoke (seasonal)", "air", {"air": 0.8, "contrast_loss": 0.3}, weather("winter_smog", 48), "no", None, [], ["smoke", "air"], A),
        ("bus_stop_exhaust", "Diesel exhaust at bus stop", "air", {"air": 0.5, "spans_path": False}, temp(1, "office_rush", 0.9), "no", None, [], ["fumes", "air"], A),
        ("generator_fumes", "Generator fumes", "air", {"air": 0.5, "noise_db": 85, "spans_path": False}, temp(4, "evening_market", 0.6), "partial", None, [], ["fumes", "air"], A),
        ("firecracker_smoke", "Firecracker smoke", "air", {"air": 0.85, "contrast_loss": 0.4, "noise_db": 100}, event(12, "night"), "no", None, ["F5.06"], ["smoke", "air", "festival"], A),
        ("holi_colour_powder", "Holi colour powder in the air", "air", {"air": 0.5, "contrast_loss": 0.2}, event(8, "day"), "partial", None, ["F5.06"], ["dust", "air", "festival"], A),
        ("pollen_season", "Pollen season", "air", {"air": 0.3}, weather("summer", 24 * 7), "no", None, [], ["air", "allergen"], A),
        ("sewer_gas_odour", "Sewer gas / open sewage odour", "air", {"air": 0.35, "cognitive": 0.1}, perm(), "no", None, [], ["air", "odour", "drain"], A),
        ("food_street_smoke", "Food street smoke (tandoor, frying)", "air", {"air": 0.4, "heat": 0.15}, temp(4, "evening_market", 0.9), "partial", None, [], ["smoke", "air"], A),
        ("incense_smoke_temple", "Incense smoke at temple", "air", {"air": 0.3}, temp(4, "temple", 0.9), "no", None, [], ["smoke", "air"], A),
        ("mosquito_fogging", "Mosquito fogging truck", "air", {"air": 0.7, "contrast_loss": 0.6, "vehicle": 0.3}, temp(0.3, "dawn_dusk", 0.2, "monsoon"), "partial", None, [], ["smoke", "air"], A),
        ("industrial_chemical_odour", "Industrial chemical odour", "air", {"air": 0.6}, perm(), "no", None, ["F8.22"], ["fumes", "air"], A),
    ]),
    ("noise", "Noise", [
        ("traffic_noise_75", "Traffic noise about 75 dB", "noise", {"noise_db": 75, "cognitive": 0.2}, ambient("office_rush"), "no", None, [], ["loud"], A),
        ("honking_bursts", "Honking bursts", "noise", {"noise_db": 95, "cognitive": 0.4}, ambient("office_rush"), "no", None, [], ["loud"], A),
        ("jackhammer_construction", "Jackhammer / construction noise", "noise", {"noise_db": 100, "air": 0.2}, temp(24 * 5, "day"), "partial", None, [], ["loud", "construction"], A),
        ("loudspeaker_dj", "Loudspeaker / DJ truck", "noise", {"noise_db": 105, "cognitive": 0.5, "flicker": 0.3}, event(4, "festival_evening", "all"), "partial", None, ["F4.13"], ["loud", "festival"], A),
        ("firecracker_bursts", "Firecracker bursts", "noise", {"noise_db": 125, "cognitive": 0.6, "flicker": 0.5}, event(6, "night"), "no", None, ["W69"], ["loud", "festival"], A),
        ("generator_noise", "Generator noise", "noise", {"noise_db": 85}, temp(4, "evening_market", 0.6), "no", None, [], ["loud"], A),
        ("temple_loudspeaker", "Temple / mosque loudspeaker", "noise", {"noise_db": 85}, ambient("temple"), "no", None, [], ["loud", "religious"], A),
        ("market_shouting", "Market hawker calls", "noise", {"noise_db": 80, "cognitive": 0.3}, ambient("evening_market"), "no", None, [], ["loud", "vendor"], A),
        ("metro_train_noise", "Elevated metro / train noise", "noise", {"noise_db": 90}, ambient("day"), "no", None, [], ["loud"], A),
        ("quiet_lane", "Quiet lane (traffic sound cues clear)", "positive", {"relief": 0.3, "noise_db": 50}, perm(), "no", None, [], ["quiet", "clear"], A),
    ]),
])

cat("crowd_safety", "Crowds and personal safety", [
    ("crowd", "Crowds", [
        ("crowd_light", "Light pedestrian crowd", "crowd", {"crowd": 0.3, "clear_width_cm": None, "noise_db": 65}, ambient("day"), "yes", None, ["F9"], ["crowd"], A),
        ("crowd_dense", "Dense crowd", "crowd", {"crowd": 0.8, "clear_width_cm": 70, "noise_db": 78}, ambient("evening_market"), "yes", None, ["F4.12"], ["crowd"], A),
        ("crowd_crush_risk", "Crowd-crush density in a narrow approach", "crowd", {"crowd": 1.0, "clear_width_cm": 40, "fall": 0.4, "noise_db": 90, "cognitive": 0.7}, event(4), "partial", None, ["F14.08", "S60"], ["crowd", "crush"], "FU"),
        ("bus_stop_crowd", "Crowd waiting at bus stop on footpath", "crowd", {"crowd": 0.6, "clear_width_cm": 60}, ambient("office_rush"), "yes", None, [], ["crowd"], A),
        ("station_exit_surge", "Station exit surge", "crowd", {"crowd": 0.9, "clear_width_cm": 80, "cognitive": 0.4}, ambient("office_rush"), "partial", None, [], ["crowd"], A),
        ("tourist_crowd", "Tourist crowd (old city)", "crowd", {"crowd": 0.7, "clear_width_cm": 80}, ambient("day", "winter"), "yes", None, ["F5.19"], ["crowd"], A),
        ("queue_atm", "ATM queue on footpath", "crowd", {"crowd": 0.4, "clear_width_cm": 80}, temp(1, "day", 0.5), "partial", None, ["F3.29"], ["crowd"], A),
    ]),
    ("social_safety", "Personal safety", [
        ("isolated_dark_stretch", "Isolated, unlit stretch with few people", "social", {"contrast_loss": 0.7, "cognitive": 0.3}, ambient("night"), "partial", None, ["F14.05"], ["isolated", "dark", "night"], "FU"),
        ("harassment_hotspot", "Reported harassment hotspot", "social", {"cognitive": 0.5}, perm(2), "no", None, ["F14.06"], ["harassment"], "FU"),
        ("chain_snatching_spot", "Chain-snatching reports", "social", {"cognitive": 0.3, "vehicle": 0.2}, perm(1), "no", None, ["F14.07"], ["crime"], A),
        ("robbery_vulnerable_spot", "Robbery targeting elderly or disabled", "social", {"cognitive": 0.4}, perm(1), "no", None, ["F14.17"], ["crime"], A),
        ("liquor_shop_crowd", "Crowd outside a liquor shop at night", "crowd", {"crowd": 0.5, "clear_width_cm": 80, "cognitive": 0.4}, ambient("night"), "partial", None, [], ["crowd", "harassment"], A),
        ("police_presence", "Police presence / CCTV", "positive", {"relief": 0.3}, perm(1), "partial", None, ["F14.18"], ["clear"], A),
        ("staring_stigma", "Staring / stigma towards disabled walkers", "social", {"cognitive": 0.3}, perm(1), "no", None, ["F4.20"], ["harassment"], A),
    ]),
])

cat("terrain_transit", "Terrain, region and transit nodes", [
    ("terrain", "Terrain and regional", [
        ("walled_city_narrow_lane", "Old walled-city lane about 2 m, mixed traffic", "traffic", {"clear_width_cm": 100, "vehicle": 0.6, "crowd": 0.6, "spans_path": True, "cognitive": 0.4}, perm(), "yes", None, ["F8.06", "W82"], ["narrow", "vehicle", "crowd"], A),
        ("village_kuccha_lane", "Village unpaved lane", "surface", {"roughness": 0.7, "vertical_cm": 4, "air": 0.2}, perm(), "yes", "missing_footpath", ["F8.07"], ["unpaved"], A),
        ("desert_sand_drift", "Desert-town sand drift", "surface", {"roughness": 0.85, "slip": 0.3, "air": 0.3}, weather("summer", 72), "partial", None, ["F8.05"], ["unpaved", "dust"], "FU"),
        ("coastal_corroded_cover", "Corroded cover (coastal)", "hole", {"vertical_cm": 3, "fall": 0.5, "visibility_needed": 0.9, "cane_detectable": 0.3}, semi(365), "partial", None, ["F8.04"], ["metal", "hole"], A),
        ("landslide_zone", "Landslide-prone hill path", "terrain", {"fall": 0.5, "overhead": 0.4, "roughness": 0.6, "slope_pct": 12, "effort": 0.8}, weather("monsoon", 24 * 7), "no", None, ["F6.14", "F8.03"], ["hill", "storm"], "FU"),
        ("flood_plain_seasonal", "Seasonal flood plain path", "terrain", {"water_cm": 40, "detour_m": 500, "fall": 0.3}, weather("monsoon", 24 * 30), "no", "waterlogging", ["F8.19"], ["water", "flood"], A),
        ("high_altitude", "High altitude (3,500 m)", "terrain", {"effort": 0.7, "cold": 0.4}, perm(), "no", None, ["F8.20"], ["altitude"], A),
        ("backwater_island_path", "Backwater / island path with ferry link", "terrain", {"roughness": 0.4, "wait_s": 600, "water_cm": 0}, perm(), "partial", None, ["F8.21"], ["ferry"], A),
        ("forest_tribal_track", "Hill tribal track", "terrain", {"roughness": 0.9, "slope_pct": 12, "vertical_cm": 15, "effort": 0.9}, perm(), "yes", None, ["F8.18"], ["hill", "unpaved"], A),
        ("gated_road_closed", "Gated / cantonment road closed", "terrain", {"clear_width_cm": 0, "detour_m": 600}, perm(), "partial", None, ["F8.15", "W140"], ["closed"], A),
        ("peri_urban_no_footpath", "New layout with no footpath yet", "traffic", {"vehicle": 0.5, "roughness": 0.4, "spans_path": True}, semi(365 * 2), "yes", "missing_footpath", ["F8.23"], ["road_walk"], A),
    ]),
    ("transit", "Transit nodes", [
        ("metro_entrance_no_lift", "Metro entrance with stairs, no lift", "step", {"vertical_cm": 500, "effort": 0.9}, perm(), "partial", "steps", ["F8.13"], ["step", "transit"], A),
        ("station_fob_no_lift", "Station FOB with no lift between platforms", "step", {"vertical_cm": 600, "effort": 1.0}, perm(), "partial", "steps", ["F8.11"], ["step", "transit"], "FU"),
        ("platform_gap", "Platform to train gap", "hole", {"vertical_cm": 25, "fall": 0.6, "clear_width_cm": None, "spans_path": True}, perm(), "no", None, [], ["transit", "hole"], A),
        ("bus_high_floor", "High-floor bus step", "step", {"vertical_cm": 40, "spans_path": True}, perm(), "yes", None, [], ["step", "transit"], A),
        ("bus_stop_no_platform", "Bus stop with no platform (board from road)", "traffic", {"vehicle": 0.5, "vertical_cm": 15, "spans_path": True}, perm(), "partial", None, [], ["transit", "vehicle"], A),
        ("railway_track_trespass", "Railway track as a shortcut", "traffic", {"vehicle": 1.0, "roughness": 0.9, "vertical_cm": 20, "spans_path": True}, perm(), "partial", None, ["F8.10", "F4.11", "F14.13"], ["rail", "never_route"], "FU"),
        ("new_metro_access_gap", "New metro station: last 100 m inaccessible", "debris", {"clear_width_cm": 40, "roughness": 0.6}, semi(365), "partial", None, ["F8.13", "S116"], ["transit", "construction"], "FU"),
        ("lift_out_of_service", "Lift out of service", "step", {"vertical_cm": 400, "effort": 0.9}, temp(24 * 30, rec=0.5), "no", None, ["W8"], ["step", "transit"], A),
    ]),
])

cat("amenities", "Amenities and relief (positive elements)", [
    ("rest", "Rest, shade and facilities", [
        ("bench_available", "Bench available", "positive", {"relief": 0.6}, perm(), "yes", None, ["F10.21"], ["rest", "clear"], A),
        ("drinking_water", "Drinking water point", "positive", {"relief": 0.4}, perm(), "partial", None, [], ["water_point", "clear"], A),
        ("accessible_toilet", "Accessible public toilet", "positive", {"relief": 0.5}, perm(), "partial", None, ["F10.20"], ["toilet", "clear"], A),
        ("toilet_locked", "Toilet locked / unusable", "positive", {"relief": 0.0, "cognitive": 0.1}, temp(24 * 7, rec=0.5), "no", None, ["W142"], ["toilet"], A),
        ("no_rest_200m", "No rest point for 200 m", "terrain", {"rest_gap_m": 200, "effort": 0.3}, perm(), "partial", None, ["F10.21"], ["no_rest"], A),
        ("no_rest_long_stretch", "No rest point for 500 m", "terrain", {"rest_gap_m": 500, "effort": 0.6}, perm(), "partial", None, ["F10.21", "W143"], ["no_rest"], A),
        ("handrail_continuous", "Continuous handrail", "positive", {"relief": 0.5}, perm(), "yes", None, ["F1.19"], ["handrail", "clear"], A),
        ("shelter_from_rain", "Covered walkway / rain shelter", "positive", {"relief": 0.5}, perm(), "yes", None, [], ["shade", "clear"], A),
        ("helpers_present", "Passers-by who help over a kerb", "positive", {"relief": 0.3}, ambient("day"), "no", None, ["F4.19"], ["helpers"], A),
    ]),
])

# Compound elements: created only by interaction rules (category 'compound'), but also scorable alone.
cat("compound", "Compound elements (created by combinations)", [
    ("compound", "Created by interaction rules", [
        ("hidden_hole_under_water", "Hole hidden under water", "compound", {"vertical_cm": 30, "fall": 0.9, "water_cm": 10, "visibility_needed": 1.0, "cane_detectable": 0.2, "spans_path": True}, weather("monsoon", 24), "no", "waterlogging", ["F6.03", "W1"], ["hole", "water"], "FU"),
        ("kerb_height_unknown_under_water", "Kerb of unknown height under water", "compound", {"vertical_cm": 15, "water_cm": 10, "fall": 0.5, "visibility_needed": 1.0, "cane_detectable": 0.3, "spans_path": True}, weather("monsoon", 24), "no", "waterlogging", ["W27"], ["kerb", "water"], A),
        ("night_open_drain_fall", "Unlit open drain (fall hazard at night)", "compound", {"vertical_cm": 60, "fall": 1.0, "visibility_needed": 1.0, "clear_width_cm": 80, "cane_detectable": 0.6}, ambient("night"), "no", "open_drain", ["F2.06", "W31"], ["hole", "drain", "night"], A),
        ("invisible_faded_zebra", "Zebra invisible in glare", "compound", {"vehicle": 0.8, "contrast_loss": 0.8, "wait_s": 40, "spans_path": True}, ambient("dawn_dusk"), "no", None, ["F2.20", "F7.07"], ["crossing"], A),
        ("burning_metal_rail", "Railing too hot to hold", "compound", {"heat": 0.9, "fall": 0.2}, weather("summer", 6, "midday_heat"), "no", None, ["M532", "F6.07"], ["heat", "metal"], A),
        ("traffic_masked_by_noise", "Traffic sound masked by noise", "compound", {"vehicle": 0.8, "noise_db": 95, "spans_path": True}, ambient("office_rush"), "no", None, ["W69"], ["vehicle", "loud"], A),
        ("festival_lane_crush", "Festival crowd in a narrow lane", "compound", {"crowd": 1.0, "clear_width_cm": 40, "fall": 0.5, "noise_db": 95, "cognitive": 0.8}, event(4), "no", None, ["F14.08", "W71"], ["crowd", "crush"], "FU"),
        ("wet_polished_slope", "Wet polished stone on a slope", "compound", {"slip": 0.9, "slope_pct": 6, "fall": 0.4}, weather("monsoon", 3), "no", None, ["F2.18", "W96"], ["wet_slippery"], A),
        ("dark_pothole", "Pothole at night (seen by day, invisible now)", "compound", {"vertical_cm": 8, "fall": 0.7, "visibility_needed": 1.0, "clear_width_cm": 80, "cane_detectable": 0.7}, ambient("night"), "no", "pothole", ["F7.05", "W73"], ["hole", "night"], A),
        ("live_wire_in_water", "Live wire in standing water", "compound", {"electric": 1.0, "water_cm": 10, "spans_path": True}, weather("monsoon", 6), "no", None, ["F6.04", "W30"], ["water", "electrical"], "FU"),
        ("smog_crossing_blind_spot", "Crossing in smog: drivers cannot see walker", "compound", {"vehicle": 0.9, "contrast_loss": 0.7, "air": 0.7, "wait_s": 40, "spans_path": True}, weather("winter_smog", 6), "no", None, ["F6.09", "W63"], ["crossing", "fog"], A),
        ("dust_storm_tree_fall", "Tree fall risk in dust storm", "compound", {"overhead": 0.8, "air": 0.9, "contrast_loss": 0.9}, weather("summer", 3), "no", None, ["F6.10", "F6.05"], ["storm", "tree"], A),
        ("ramp_into_pothole", "Kerb ramp that ends in a pothole", "compound", {"vertical_cm": 8, "slope_pct": 8, "fall": 0.6, "spans_path": True}, semi(90), "partial", "pothole", ["W159"], ["ramp", "hole"], A),
        ("dog_pack_dark_lane", "Dog pack in an unlit lane", "compound", {"animal": 0.9, "contrast_loss": 0.8}, ambient("night"), "no", None, ["F3.27", "W75"], ["animal", "dog", "night"], A),
        ("crowd_blocks_ramp", "Crowd standing on the only ramp", "compound", {"crowd": 0.8, "clear_width_cm": 30, "slope_pct": 8, "spans_path": True}, ambient("evening_market"), "no", None, ["INDIA-CHAOS-13"], ["crowd", "ramp_blocked"], A),
        ("icy_shaded_steps", "Icy steps in shade", "compound", {"slip": 1.0, "vertical_cm": 15, "fall": 0.7, "cold": 0.5}, weather("winter", 4, "fog_morning"), "no", "steps", ["F6.13"], ["ice", "step"], A),
        ("flooded_trench", "Trench filled with rainwater", "compound", {"vertical_cm": 80, "fall": 1.0, "water_cm": 40, "visibility_needed": 1.0, "cane_detectable": 0.2, "spans_path": True}, weather("monsoon", 24), "no", "waterlogging", ["F2.11", "F6.03"], ["hole", "water"], A),
        ("heat_long_unshaded_climb", "Long unshaded climb in heat", "compound", {"heat": 0.9, "slope_pct": 7, "effort": 0.9}, weather("summer", 6, "midday_heat"), "no", None, ["F6.06", "W57"], ["heat", "slope"], A),
        ("fog_unlit_crossing", "Fog at an unlit crossing", "compound", {"vehicle": 0.95, "contrast_loss": 0.95, "wait_s": 40, "spans_path": True}, weather("winter", 4, "fog_morning"), "no", None, ["F6.09", "F7.01"], ["crossing", "fog", "dark"], A),
        ("glare_hides_step", "Low-sun glare hiding a step edge", "compound", {"vertical_cm": 15, "fall": 0.5, "glare": 0.8, "visibility_needed": 1.0, "spans_path": True}, ambient("dawn_dusk"), "no", "steps", ["F7.07", "F7.08"], ["step", "glare"], A),
        ("procession_on_no_footpath_road", "Procession on a road with no footpath", "compound", {"crowd": 0.9, "vehicle": 0.6, "noise_db": 100, "spans_path": True, "detour_m": 300}, event(3), "no", None, ["F4.13", "F1.01"], ["crowd", "festival", "road_walk"], A),
        ("silent_ev_in_crowd", "Silent EV moving through a crowd", "compound", {"vehicle": 0.7, "crowd": 0.7, "noise_db": 70}, ambient("evening_market"), "no", None, [], ["vehicle", "silent_vehicle", "crowd"], A),
    ]),
])

# ---------------------------------------------------------------------------------------------------------
# Bodies. Leaves follow hermes BODY-TAXONOMY.md (ids kept as hermes_id) plus claude additions (marked).
# scorer: wheeled | ambulant | visual | hearing | cognitive | elderly | systemic | situational
# Sensitivity values: hermes qualitative grade mapped by GRADE (ASSUMPTION mapping), then claude per-axis edits.
# ---------------------------------------------------------------------------------------------------------
GRADE = {"none": 0.03, "low": 0.15, "medium": 0.4, "high": 0.7, "very_high": 0.95}
SENS_AXES = ["vertical", "width", "slope", "cross", "roughness", "slip", "fall", "overhead", "visibility",
             "contrast", "glare", "flicker", "noise", "air", "heat", "cold", "crowd", "vehicle", "animal", "water",
             "electric", "cognitive", "wait", "detour", "effort"]

ADULT = dict(vertical=0.05, width=0.03, slope=0.05, cross=0.02, roughness=0.03, slip=0.12, fall=0.12, overhead=0.1,
             visibility=0.1, contrast=0.03, glare=0.05, flicker=0.02, noise=0.03, air=0.08, heat=0.1, cold=0.05,
             crowd=0.08, vehicle=0.25, animal=0.15, water=0.08, electric=1.0, cognitive=0.03, wait=0.3, detour=0.3,
             effort=0.05)

BASE_BY_SCORER = {
    "wheeled": dict(ADULT, vertical=1.0, width=1.0, slope=1.0, cross=0.9, roughness=0.8, slip=0.25, fall=0.8,
                    overhead=0.05, visibility=0.15, crowd=0.6, vehicle=0.5, water=1.0, heat=0.3, air=0.04,
                    wait=0.6, detour=1.0, effort=0.6, animal=0.3),
    "ambulant": dict(ADULT, vertical=0.6, width=0.5, slope=0.6, cross=0.5, roughness=0.6, slip=0.8, fall=0.6,
                     visibility=0.2, crowd=0.5, water=0.5, effort=0.6, wait=0.5, detour=0.8, heat=0.2),
    "visual": dict(ADULT, vertical=0.2, width=0.2, slope=0.05, cross=0.05, roughness=0.05, slip=0.3, fall=0.6,
                   overhead=0.9, visibility=1.0, contrast=0.9, glare=0.8, crowd=0.6, vehicle=0.7, cognitive=0.5,
                   water=0.3, animal=0.3),
    "hearing": dict(ADULT, vehicle=0.45, noise=0.05, crowd=0.15),
    "cognitive": dict(ADULT, cognitive=0.9, noise=0.6, crowd=0.7, vehicle=0.5, flicker=0.3, glare=0.2),
    "elderly": dict(ADULT, vertical=0.4, slope=0.5, cross=0.3, roughness=0.3, slip=0.7, fall=0.7, visibility=0.4,
                    contrast=0.4, glare=0.4, heat=0.6, cold=0.4, crowd=0.4, vehicle=0.5, wait=0.4, effort=0.6,
                    width=0.15, animal=0.4),
    "systemic": dict(ADULT, air=0.6, heat=0.6, cold=0.4, slope=0.4, effort=0.7, wait=0.3),
    "situational": dict(ADULT),
}

# limits: max_vertical_cm, max_slope_pct, max_cross_slope_pct, min_width_cm, max_water_cm, max_aqi_air, max_noise_db
# (max_aqi_air is the 'air' intensity at which an air element becomes a block for this body)
BODY_ROWS = []


def B(bid, hermes_id, name, path, scorer, rpwd, aid, speed, speed_src, legacy, sens=None, limits=None,
      limit_src=None, risk_penalty_s=300, notes=""):
    BODY_ROWS.append(dict(id=bid, hermes_id=hermes_id, name=name, path=path, scorer=scorer, rpwd=rpwd, aid=aid,
                          speed_mps=speed, speed_source=speed_src, legacy_profile=legacy, sens_edits=sens or {},
                          limits=limits or {}, limit_sources=limit_src or {}, risk_penalty_s=risk_penalty_s,
                          notes=notes))


W_LIM = dict(max_vertical_cm=2, max_slope_pct=6.67, max_cross_slope_pct=5, min_width_cm=90, max_water_cm=10)
W_SRC = dict(max_vertical_cm="ASSUMPTIONS_JSON (2 cm block) + UK_IM_S98 (10 mm thresholds)",
             max_slope_pct="IRC103_2022_6.7 (1:15, stricter than HG2021 1:12, D-rule in assumptions.json)",
             max_cross_slope_pct="ASSUMPTION (S96 says one-rim propulsion from ~3%, costed below the block)",
             min_width_cm="ASSUMPTIONS_JSON 90 cm + HG2021_3.7.3 900 mm ramp + UK_IM_S98 chair ~70 cm",
             max_water_cm="ASSUMPTION (caster hub / footplate height)")

# A. Sensory > A1 Vision
B("blind_cane", "A1.1", "Blind, white-cane user", ["Sensory", "Vision"], "visual", "1.B(a) blindness", "white cane", 1.0, "ASSUMPTION", "low_vision",
  sens=dict(contrast=0.0, glare=0.0, visibility=1.0, overhead=1.0, noise=0.6, fall=0.8, cognitive=0.6),
  limits=dict(cane_skill=0.8, light_independent=True), notes="cane finds ground-level objects (cane_detectable); overhead is missed; relies on traffic sound")
B("blind_guide_dog", "A1.1*", "Blind, guide-dog user (claude addition)", ["Sensory", "Vision"], "visual", "1.B(a) blindness", "guide dog", 1.1, "ASSUMPTION", "low_vision",
  sens=dict(contrast=0.0, glare=0.0, overhead=0.5, animal=0.8, noise=0.5, crowd=0.7, fall=0.5),
  limits=dict(cane_skill=0.9, light_independent=True), notes="dog steers round obstacles incl. overhead; stray dogs distract the guide dog")
B("low_vision_severe", "A1.2", "Low vision, severe", ["Sensory", "Vision"], "visual", "1.B(b) low vision", "white cane, sometimes guide dog", 0.9, "ASSUMPTION", "low_vision",
  sens=dict(contrast=1.0, glare=0.9, fall=0.6), limits=dict(cane_skill=0.6, residual_day=0.5))
B("low_vision_moderate", "A1.3", "Low vision, moderate", ["Sensory", "Vision"], "visual", "1.B(b) low vision", "none or cane", 1.0, "ASSUMPTION", "low_vision",
  sens=dict(contrast=0.8, glare=0.8, fall=0.5, overhead=0.6), limits=dict(cane_skill=0.3, residual_day=0.25))
B("night_blind_glare", "A1.4", "Night-blind or glare-sensitive", ["Sensory", "Vision"], "visual", "1.B(b) low vision (field)", "cane", 1.0, "ASSUMPTION", "low_vision",
  sens=dict(glare=1.0, contrast=1.0, overhead=0.5), limits=dict(cane_skill=0.4, residual_day=0.1, night_factor=1.6))
B("albinism_photophobia", "A1.4*", "Albinism / photophobia (claude addition)", ["Sensory", "Vision"], "visual", "1.B(b) low vision", "dark glasses, sometimes cane", 1.0, "ASSUMPTION", "low_vision",
  sens=dict(glare=1.0, heat=0.5, contrast=0.8, overhead=0.4), limits=dict(cane_skill=0.2, residual_day=0.35))
B("deafblind", "A1.5", "Deaf-blind", ["Sensory", "Vision"], "visual", "5 multiple disabilities incl. deaf blindness", "white cane plus support person", 0.7, "ASSUMPTION", "low_vision",
  sens=dict(vehicle=1.0, noise=0.0, crowd=0.9, overhead=1.0, fall=0.9, cognitive=0.8, contrast=0.0, glare=0.0),
  limits=dict(cane_skill=0.7, light_independent=True, no_hearing=True))
# A2 Hearing
B("deaf", "A2.1", "Deaf", ["Sensory", "Hearing"], "hearing", "1.C(a) deaf (70 dB loss)", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(vehicle=0.5), limits=dict(no_hearing=True))
B("hard_of_hearing", "A2.2", "Hard of hearing (hearing aid)", ["Sensory", "Hearing"], "hearing", "1.C(b) hard of hearing (60-70 dB)", "hearing aid", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(vehicle=0.35, noise=0.5, crowd=0.3), limits=dict(partial_hearing=True))
B("deaf_low_vision", "A2.3", "Deaf with low vision", ["Sensory", "Hearing"], "visual", "5 multiple disabilities", "cane", 0.9, "ASSUMPTION", "low_vision",
  sens=dict(vehicle=1.0, noise=0.0, contrast=1.0, glare=0.9, crowd=0.8), limits=dict(cane_skill=0.5, residual_day=0.4, no_hearing=True))
B("speech_language", "A3.1", "Speech and language disability", ["Sensory", "Speech"], "hearing", "1.D speech and language", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(vehicle=0.25, cognitive=0.2, crowd=0.2), limits=dict(cannot_call_for_help=True))
# B1 Wheeled
B("mw_self", "B1.1", "Manual wheelchair, self-propelled", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "manual wheelchair", 1.08, "NCHRP562_speeds", "manual_wheelchair",
  sens=dict(heat=0.5), limits=dict(W_LIM, min_width_cm=90, caster_small=True, hand_propelled=True), limit_src=W_SRC)
B("mw_attendant", "B1.2", "Manual wheelchair, attendant-pushed", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "manual chair plus pusher", 1.1, "ASSUMPTION", "manual_wheelchair",
  sens=dict(heat=0.4, crowd=0.7, effort=0.4), limits=dict(W_LIM, max_vertical_cm=8, min_width_cm=110, caster_small=True),
  limit_src=dict(W_SRC, max_vertical_cm="ASSUMPTION: an attendant can tip a chair over about 8 cm", min_width_cm="ASSUMPTION; hermes A 1800 mm for the pair side by side, 110 cm in line"))
B("mw_active_rigid", "B1.1*", "Active-user rigid wheelchair (claude addition)", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "ultralight rigid chair", 1.3, "ASSUMPTION", "manual_wheelchair",
  sens=dict(vertical=0.8, roughness=0.6), limits=dict(W_LIM, max_vertical_cm=6, max_slope_pct=8.33, hand_propelled=True),
  limit_src=dict(W_SRC, max_vertical_cm="ASSUMPTION: wheelie over about 6 cm", max_slope_pct="HG2021_3.7.2 1:12"))
B("mw_tetraplegia", "B1.1**", "Manual chair, low arm function (claude addition)", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "manual chair with push gloves", 0.6, "ASSUMPTION", "manual_wheelchair",
  sens=dict(slope=1.0, cross=1.0, roughness=1.0, heat=0.9, cold=0.6, effort=1.0), limits=dict(W_LIM, max_slope_pct=5.0, max_cross_slope_pct=3, hand_propelled=True),
  limit_src=dict(W_SRC, max_slope_pct="ASSUMPTION (S99: >5% costly)", max_cross_slope_pct="S96_crossslope 3%"))
B("pw_standard", "B1.3", "Power wheelchair", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "power chair", 1.3, "ASSUMPTION", "power_wheelchair",
  sens=dict(slope=0.6, effort=0.1, roughness=0.6, heat=0.15), limits=dict(W_LIM, max_vertical_cm=5, min_width_cm=90),
  limit_src=dict(W_SRC, max_vertical_cm="ASSUMPTION (S95: ordinary power chairs climb far less than 20 cm)"))
B("pw_step_climbing", "B1.3*", "Step-climbing power chair (claude addition)", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "step-climbing chair", 1.2, "ASSUMPTION", "power_wheelchair",
  sens=dict(vertical=0.5, slope=0.5, effort=0.05), limits=dict(W_LIM, max_vertical_cm=20, max_slope_pct=8.33),
  limit_src=dict(W_SRC, max_vertical_cm="S95_stepclimb median 20 cm"))
B("tilt_in_space", "B1.4", "Tilt-in-space / reclining chair", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "large powered or attendant chair", 1.0, "ASSUMPTION", "power_wheelchair",
  sens=dict(roughness=1.0, effort=0.2, crowd=0.8), limits=dict(W_LIM, max_vertical_cm=2, min_width_cm=120),
  limit_src=dict(W_SRC, min_width_cm="ASSUMPTION; hermes A 1500 mm turning"))
B("mobility_scooter", "B1.5", "Mobility scooter", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "scooter", 1.6, "ASSUMPTION", "power_wheelchair",
  sens=dict(roughness=0.9, effort=0.05, width=1.0), limits=dict(W_LIM, max_vertical_cm=5, min_width_cm=100),
  limit_src=dict(W_SRC, min_width_cm="ASSUMPTION; hermes A 1500 mm"))
B("hand_cranked_tricycle", "B1.6*", "Hand-cranked tricycle (common in India, claude addition)", ["Mobility", "Wheeled"], "wheeled", "1.A locomotor", "hand-cranked tricycle", 1.5, "ASSUMPTION", "manual_wheelchair",
  sens=dict(width=1.0, slope=0.9, vehicle=0.7), limits=dict(W_LIM, max_vertical_cm=4, min_width_cm=100, hand_propelled=True),
  limit_src=dict(W_SRC, min_width_cm="ASSUMPTION (FU 10.26: wider than a chair)"))
# B2 Ambulatory aids
AMB_LIM = dict(max_vertical_cm=15, max_slope_pct=10, max_cross_slope_pct=8, min_width_cm=75, max_water_cm=15)
AMB_SRC = dict(max_vertical_cm="IRC103_2012_6.2.1 150 mm standard riser (ASSUMPTION that a riser above it blocks)", min_width_cm="ASSUMPTION (hermes A 900 mm)",
               max_slope_pct="ASSUMPTION", max_cross_slope_pct="ASSUMPTION", max_water_cm="ASSUMPTION")
B("walking_frame", "B2.1", "Walker (no wheels)", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "walking frame", 0.63, "NCHRP562_speeds", "walker_elderly",
  sens=dict(vertical=0.7, roughness=0.7, effort=0.8), limits=dict(AMB_LIM, max_vertical_cm=15, min_width_cm=65), limit_src=AMB_SRC)
B("rollator", "B2.2", "Rollator (four wheels, seat)", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "rollator", 0.7, "ASSUMPTION", "walker_elderly",
  sens=dict(vertical=0.9, roughness=0.8, cross=0.6), limits=dict(AMB_LIM, max_vertical_cm=4, min_width_cm=65, wheeled_aid=True),
  limit_src=dict(AMB_SRC, max_vertical_cm="ASSUMPTION: small rollator wheels jam above about 4 cm"))
B("crutches_bilateral", "B2.3", "Crutches, bilateral", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "crutches", 0.8, "NCHRP562_speeds", "crutches",
  sens=dict(slip=1.0, vertical=0.7, width=0.6), limits=dict(AMB_LIM, max_vertical_cm=10, min_width_cm=90),
  limit_src=dict(AMB_SRC, max_vertical_cm="hermes A: step-up 100 mm hard", min_width_cm="hermes A 900 mm"))
B("support_cane", "B2.4", "Support cane (not white cane)", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "cane", 0.8, "NCHRP562_speeds", "walker_elderly",
  sens=dict(vertical=0.4, roughness=0.6, slip=0.7), limits=dict(AMB_LIM, max_vertical_cm=20), limit_src=AMB_SRC)
B("prosthetic_lower", "B2.5", "Lower-limb prosthesis", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "prosthesis", 1.0, "ASSUMPTION", "crutches",
  sens=dict(slip=0.9, cross=0.8, roughness=0.5, slope=0.6), limits=dict(AMB_LIM, max_vertical_cm=20), limit_src=AMB_SRC)
B("orthosis_caliper", "B2.6", "Orthosis or caliper", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "caliper", 0.8, "ASSUMPTION", "crutches",
  sens=dict(vertical=0.8, slope=0.6), limits=dict(AMB_LIM, max_vertical_cm=15), limit_src=AMB_SRC)
B("amputee_no_prosthesis", "B2.7", "Above-knee amputation, no prosthesis", ["Mobility", "Ambulatory aids"], "ambulant", "1.A locomotor", "crutches or hopping", 0.6, "ASSUMPTION", "crutches",
  sens=dict(slip=1.0, vertical=0.9, fall=0.9, effort=0.9), limits=dict(AMB_LIM, max_vertical_cm=8, min_width_cm=90),
  limit_src=dict(AMB_SRC, max_vertical_cm="hermes A: zero-rise where possible; 8 cm ASSUMPTION"))
# B3 Gait, balance, stature
B("cp_ambulant", "B3.1", "Cerebral palsy, ambulant", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A(b) cerebral palsy", "none or crutches", 0.8, "ASSUMPTION", "crutches",
  sens=dict(crowd=0.8, noise=0.4, fall=0.8, roughness=0.7, contrast=0.3), limits=dict(AMB_LIM, max_vertical_cm=12, min_width_cm=100),
  limit_src=dict(AMB_SRC, min_width_cm="hermes A 1200 mm for ataxia (100 cm block)"))
B("parkinsons", "B3.2", "Parkinson's disease", ["Mobility", "Gait, balance, stature"], "ambulant", "4(a) chronic neurological (Parkinson's)", "cane", 0.75, "ASSUMPTION", "walker_elderly",
  sens=dict(crowd=0.95, fall=0.9, cognitive=0.5, width=0.7, wait=0.7), limits=dict(AMB_LIM, max_vertical_cm=12), limit_src=AMB_SRC,
  notes="freezing of gait in crowds, doorways and narrow gaps")
B("multiple_sclerosis", "B3.3", "Multiple sclerosis, relapsing", ["Mobility", "Gait, balance, stature"], "ambulant", "4(a) chronic neurological (MS)", "cane or rollator", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(heat=0.95, effort=0.9, glare=0.5), limits=dict(AMB_LIM, max_vertical_cm=12), limit_src=AMB_SRC, notes="Uhthoff: heat worsens symptoms (hermes)")
B("muscular_dystrophy", "B3.4", "Muscular dystrophy, ambulant", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A(d) muscular dystrophy", "walker", 0.65, "ASSUMPTION", "walker_elderly",
  sens=dict(effort=1.0, slope=0.9, vertical=0.9, fall=0.9), limits=dict(AMB_LIM, max_vertical_cm=10, max_slope_pct=8.33), limit_src=AMB_SRC)
B("post_polio", "B3.5", "Post-polio residual", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A locomotor", "cane or caliper", 0.8, "ASSUMPTION", "crutches",
  sens=dict(effort=0.8, vertical=0.8), limits=dict(AMB_LIM, max_vertical_cm=15), limit_src=AMB_SRC)
B("dwarfism", "B3.6", "Dwarfism (147 cm or less)", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A(c) dwarfism", "none", 1.0, "ASSUMPTION", "default_walker",
  sens=dict(vertical=0.6, crowd=0.8, vehicle=0.5, effort=0.4, slip=0.3, water=0.7), limits=dict(AMB_LIM, max_vertical_cm=25, max_water_cm=10),
  limit_src=dict(AMB_SRC, max_vertical_cm="ASSUMPTION scaled to shorter stride", max_water_cm="ASSUMPTION scaled to height"), notes="low eye height: hidden behind parked vehicles in crowds")
B("neuropathy_foot_drop", "B3.7", "Neuropathy or foot drop", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A locomotor", "cane, AFO", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(roughness=0.9, vertical=0.7, contrast=0.4, heat=0.5), limits=dict(AMB_LIM, max_vertical_cm=12), limit_src=AMB_SRC)
B("vertigo_balance", "B3.8", "Vertigo or balance disorder", ["Mobility", "Gait, balance, stature"], "ambulant", "not in Schedule (situational / chronic)", "cane, sometimes rollator", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(fall=1.0, crowd=0.8, glare=0.7, flicker=0.6, cross=0.8, cognitive=0.3), limits=dict(AMB_LIM, max_vertical_cm=12), limit_src=AMB_SRC)
B("leprosy_cured", "B3.9*", "Leprosy-cured, foot sensory loss (claude addition)", ["Mobility", "Gait, balance, stature"], "ambulant", "1.A(a) leprosy cured", "footwear, sometimes cane", 0.9, "ASSUMPTION", "walker_elderly",
  sens=dict(heat=0.9, roughness=0.8, water=0.6, fall=0.5), limits=dict(AMB_LIM, max_vertical_cm=15), limit_src=AMB_SRC,
  notes="cannot feel hot surfaces or injuries on feet")
B("acid_attack_survivor", "B3.10*", "Acid-attack survivor (claude addition)", ["Mobility", "Gait, balance, stature"], "visual", "1.A(e) acid attack victims", "varies; often sight loss", 1.0, "ASSUMPTION", "low_vision",
  sens=dict(heat=0.8, glare=0.9, air=0.4, crowd=0.6, contrast=0.7), limits=dict(cane_skill=0.3, residual_day=0.4),
  notes="skin heat and sun sensitivity, frequent partial sight loss, stigma in crowds")
# C Cognitive and neurological
B("intellectual_disability", "C1.1", "Intellectual disability", ["Cognitive and neurological"], "cognitive", "2 intellectual disability", "often with a supporter", 1.1, "ASSUMPTION", "default_walker",
  sens=dict(cognitive=1.0, vehicle=0.7, crowd=0.6))
B("specific_learning_disability", "C1.2", "Specific learning disability", ["Cognitive and neurological"], "cognitive", "2(a) specific learning disabilities", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(cognitive=0.6, noise=0.1, crowd=0.15, vehicle=0.3))
B("autism_sensory", "C1.3", "Autism, sensory-sensitive", ["Cognitive and neurological"], "cognitive", "2(b) autism spectrum disorder", "none", 1.2, "ASSUMPTION", "default_walker",
  sens=dict(noise=1.0, crowd=0.95, flicker=0.8, glare=0.6, cognitive=0.7, air=0.3), limits=dict(max_noise_db=100),
  limit_src=dict(max_noise_db="ASSUMPTION: 100 dB+ (DJ truck, firecrackers) treated as a block for sensory overload"))
B("dementia_early", "C1.4", "Dementia, early", ["Cognitive and neurological"], "cognitive", "3 mental illness / 4 neurological (not named)", "cane sometimes", 0.85, "AGEING_2012", "walker_elderly",
  sens=dict(cognitive=1.0, crowd=0.8, glare=0.6, contrast=0.6, fall=0.5, slip=0.4))
B("epilepsy_photosensitive", "C1.5", "Epilepsy, photosensitive", ["Cognitive and neurological"], "cognitive", "4(a) chronic neurological", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(flicker=1.0, glare=0.6, cognitive=0.2, noise=0.2, heat=0.3), limits=dict(max_flicker=0.7),
  limit_src=dict(max_flicker="ASSUMPTION: strong flashing lights treated as a block (seizure trigger, hermes C1.5)"))
B("anxiety_mental_illness", "C1.6", "Mental illness, anxiety or paranoia", ["Cognitive and neurological"], "cognitive", "3 mental illness", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(crowd=0.95, noise=0.7, cognitive=0.6, contrast=0.4))
B("low_literacy", "C1.7", "Low literacy", ["Cognitive and neurological"], "cognitive", "not in Schedule", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(cognitive=0.5, noise=0.05, crowd=0.1, vehicle=0.3))
# D Chronic and systemic
B("cardiac", "D1.1", "Cardiac condition", ["Chronic and systemic"], "systemic", "not in Schedule (chronic)", "none", 0.9, "ASSUMPTION", "walker_elderly",
  sens=dict(heat=0.95, effort=0.95, slope=0.8, air=0.7, cold=0.6), limits=dict(max_air=0.9, max_effort=0.9),
  limit_src=dict(max_air="CPCB_AQI: severe (401-500) 'serious health impacts on people with lung/heart disease'", max_effort="ASSUMPTION"))
B("copd_asthma", "D1.2", "COPD or asthma", ["Chronic and systemic"], "systemic", "not in Schedule (chronic)", "none, sometimes oxygen", 0.9, "ASSUMPTION", "walker_elderly",
  sens=dict(air=1.0, heat=0.8, cold=0.7, slope=0.7, effort=0.8), limits=dict(max_air=0.9),
  limit_src=dict(max_air="CPCB_AQI: 101-200 already 'breathing discomfort to people with lung disease such as asthma'; severe band blocks"))
B("sickle_cell_thalassemia", "D1.3", "Sickle cell disease or thalassemia", ["Chronic and systemic"], "systemic", "4(b) blood disorder", "none", 1.0, "ASSUMPTION", "default_walker",
  sens=dict(heat=0.95, cold=0.9, effort=0.8, air=0.4), notes="dehydration, heat and cold can trigger crises (hermes D1.3)")
B("haemophilia", "D1.8*", "Haemophilia (claude addition)", ["Chronic and systemic"], "systemic", "4(b) blood disorder", "none", 1.1, "ASSUMPTION", "default_walker",
  sens=dict(fall=0.9, slip=0.8, crowd=0.6, animal=0.6, vertical=0.4), notes="any fall or bite means bleeding risk")
B("chronic_fatigue_long_covid", "D1.4", "Chronic fatigue or long COVID", ["Chronic and systemic"], "systemic", "not in Schedule", "sometimes rollator", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(effort=1.0, heat=0.7, slope=0.8, wait=0.6, detour=0.8))
B("chronic_pain", "D1.5", "Chronic pain", ["Chronic and systemic"], "systemic", "not in Schedule", "cane or rollator", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(roughness=0.9, cold=0.8, effort=0.7, vertical=0.4))
B("diabetes_neuropathy", "D1.6", "Diabetes with neuropathy", ["Chronic and systemic"], "systemic", "not in Schedule", "cane", 0.85, "ASSUMPTION", "walker_elderly",
  sens=dict(heat=0.8, roughness=0.7, water=0.6, contrast=0.4, fall=0.5))
B("incontinence", "D1.7", "Incontinence", ["Chronic and systemic"], "systemic", "not in Schedule", "none", 1.2, "ASSUMPTION", "default_walker",
  sens=dict(detour=0.9, wait=0.9, effort=0.3), notes="toilet every A 500 m (hermes); toilet elements give relief")
# E Age and life stage
B("child_5_12", "E1.1", "Child, 5 to 12", ["Age and life stage"], "situational", "not in Schedule", "none", 1.2, "ASSUMPTION", "default_walker",
  sens=dict(vehicle=0.9, animal=0.9, fall=0.6, crowd=0.6, cognitive=0.5, water=0.7, electric=1.0), limits=dict(mode="child", max_water_cm=20),
  limit_src=dict(max_water_cm="ASSUMPTION scaled to height; FU 10.13 drains"), notes="low eye height: hidden behind parked vehicles; dog bites (S143)")
B("adolescent_school_bag", "E1.2", "Adolescent with school bag", ["Age and life stage"], "situational", "not in Schedule", "none", 1.3, "ASSUMPTION", "default_walker",
  sens=dict(vehicle=0.4, crowd=0.3), limits=dict(mode="adult"))
B("pregnant_third_trimester", "E1.3", "Pregnant, third trimester", ["Age and life stage"], "situational", "not in Schedule", "none", 1.0, "ASSUMPTION", "walker_elderly",
  sens=dict(heat=0.8, slip=0.9, fall=0.9, slope=0.6, effort=0.7, crowd=0.7, air=0.6, vertical=0.4), limits=dict(mode="pregnant", max_air=0.95),
  limit_src=dict(max_air="CPCB_AQI severe band (ASSUMPTION that pregnancy is treated like lung/heart disease)"))
B("older_60_69", "E1.4", "Older adult 60 to 69, independent", ["Age and life stage"], "elderly", "not in Schedule", "none", 1.0, "AGEING_2012", "walker_elderly",
  sens=dict(fall=0.5, slip=0.5, heat=0.5))
B("older_70_79", "E1.5", "Older adult 70 to 79, slow", ["Age and life stage"], "elderly", "not in Schedule", "cane often", 0.8, "AGEING_2012", "walker_elderly",
  sens=dict(fall=0.8, slip=0.8, heat=0.7, wait=0.6), limits=dict(max_vertical_cm=20))
B("older_80_frail", "E1.6", "Older adult 80+, frail", ["Age and life stage"], "elderly", "not in Schedule", "walker or cane, escort", 0.77, "AGEING_2025", "walker_elderly",
  sens=dict(fall=1.0, slip=1.0, heat=0.95, vertical=0.7, effort=0.9, crowd=0.7, cold=0.6), limits=dict(max_vertical_cm=15, min_width_cm=65),
  limit_src=dict(max_vertical_cm="IRC103_2012_6.2.1 riser (ASSUMPTION that a higher step blocks)", min_width_cm="ASSUMPTION: walking frame about 60 cm wide"))
B("older_with_walker", "E1.7*", "Older adult with walking frame (legacy walker_elderly)", ["Age and life stage"], "elderly", "not in Schedule", "walking frame", 0.79, "assumptions.json IRC older value (to_confirm)", "walker_elderly",
  sens=dict(fall=0.9, slip=0.9, vertical=0.7, roughness=0.6, width=0.5), limits=dict(max_vertical_cm=15, min_width_cm=65))
# F Temporary and situational
B("leg_cast_boot", "F1.1", "Lower limb in cast or boot", ["Temporary and situational"], "situational", "not in Schedule", "crutches or boot", 0.8, "NCHRP562_speeds", "crutches",
  sens=dict(slip=1.0, vertical=0.8, fall=0.8, effort=0.7), limits=dict(mode="ambulant", max_vertical_cm=12, min_width_cm=90))
B("post_surgery_abdominal", "F1.2", "Post-surgery, abdominal", ["Temporary and situational"], "situational", "not in Schedule", "none", 0.8, "ASSUMPTION", "walker_elderly",
  sens=dict(roughness=0.7, effort=0.8, crowd=0.6, slope=0.6), limits=dict(mode="adult"))
B("recent_injury_crutches", "F1.3", "Recent injury, crutches under 6 weeks", ["Temporary and situational"], "situational", "not in Schedule", "crutches", 0.8, "NCHRP562_speeds", "crutches",
  sens=dict(slip=1.0, vertical=0.8, fall=0.8, width=0.6, effort=0.7), limits=dict(mode="ambulant", max_vertical_cm=10, min_width_cm=90))
B("pram_stroller", "F1.4", "Pram or stroller", ["Temporary and situational"], "situational", "not in Schedule", "pram", 1.15, "assumptions.json (ASSUMPTION)", "pram",
  sens=dict(vertical=0.8, width=0.8, roughness=0.6, heat=0.5, vehicle=0.5, slope=0.5), limits=dict(mode="wheeled", max_vertical_cm=4, min_width_cm=70, max_slope_pct=12.5, max_water_cm=10),
  limit_src=dict(min_width_cm="assumptions.json 70 cm pram rule", max_vertical_cm="ASSUMPTION (lift front wheels over small kerbs)"))
B("carrying_child", "F1.5", "Carrying a child", ["Temporary and situational"], "situational", "not in Schedule", "none", 1.0, "ASSUMPTION", "walker_elderly",
  sens=dict(fall=0.8, slip=0.8, vertical=0.4, heat=0.5, visibility=0.3), limits=dict(mode="adult"))
B("head_load", "F1.6", "Carrying loads (head load, sacks)", ["Temporary and situational"], "situational", "not in Schedule", "none", 1.0, "ASSUMPTION", "default_walker",
  sens=dict(overhead=0.9, slip=0.6, crowd=0.5, heat=0.5), limits=dict(mode="adult"))
B("delivery_trolley", "F1.7", "Delivery worker with hand trolley", ["Temporary and situational"], "situational", "not in Schedule", "hand trolley", 1.1, "ASSUMPTION", "pram",
  sens=dict(vertical=0.6, width=0.8, roughness=0.5, crowd=0.6), limits=dict(mode="wheeled", max_vertical_cm=12, min_width_cm=80))
B("rolling_luggage", "F1.8", "Tourist with rolling luggage", ["Temporary and situational"], "situational", "not in Schedule", "rolling bag", 1.1, "ASSUMPTION", "pram",
  sens=dict(vertical=0.5, roughness=0.6, width=0.4, cognitive=0.4, heat=0.4), limits=dict(mode="wheeled", max_vertical_cm=25, min_width_cm=60))
B("vendor_cart_pusher", "F1.9", "Vendor pushing a cart", ["Temporary and situational"], "situational", "not in Schedule", "cart", 0.9, "ASSUMPTION", "pram",
  sens=dict(width=1.0, vertical=0.8, slope=0.8, heat=0.5), limits=dict(mode="wheeled", max_vertical_cm=8, min_width_cm=120, max_slope_pct=5),
  limit_src=dict(max_slope_pct="hermes A 1:20 for a loaded cart", min_width_cm="hermes A 1500 mm (120 cm block)"))
B("caregiver_pair", "F1.10", "Caregiver pair (person plus escort)", ["Temporary and situational"], "situational", "not in Schedule", "two abreast", 0.9, "ASSUMPTION", "walker_elderly",
  sens=dict(width=0.8, crowd=0.7, fall=0.4), limits=dict(mode="adult", min_width_cm=120),
  limit_src=dict(min_width_cm="HG2021_3.5.1 1200 mm walkway (1800 mm two-way)"))
B("no_impairment_adult", "Z0*", "Adult, no impairment (baseline, legacy default_walker)", ["Temporary and situational"], "situational", "not in Schedule", "none", 1.3, "assumptions.json (ASSUMPTION)", "default_walker",
  sens={}, limits=dict(mode="adult"))
# G Environmental sensitivity
B("heat_sensitive", "G1.1", "Heat-sensitive (medication, MS, cardiac)", ["Environmental sensitivity"], "systemic", "not in Schedule", "varies", 1.0, "ASSUMPTION", "default_walker",
  sens=dict(heat=1.0, effort=0.6), limits=dict(max_heat=0.95))
B("dust_sensitive", "G1.2", "Dust-sensitive (asthma, allergy)", ["Environmental sensitivity"], "systemic", "not in Schedule", "none", 1.2, "ASSUMPTION", "default_walker",
  sens=dict(air=0.95, effort=0.3))
B("noise_sensitive", "G1.3", "Noise-sensitive (autism, migraine)", ["Environmental sensitivity"], "cognitive", "not in Schedule", "none", 1.2, "ASSUMPTION", "default_walker",
  sens=dict(noise=1.0, flicker=0.5, cognitive=0.3, crowd=0.4))
B("crowd_averse", "G1.4", "Crowd-averse (anxiety, dementia)", ["Environmental sensitivity"], "cognitive", "not in Schedule", "none", 1.1, "ASSUMPTION", "default_walker",
  sens=dict(crowd=1.0, noise=0.5, cognitive=0.4))

# hermes BODY-TAXONOMY.md section 4/5 per-leaf needs, kept verbatim as (rest spacing m or None, tactile).
# Rest spacing is an hermes ASSUMPTION ("A") in every row; tactile N7 is sourced (IRC:103 tactile clause).
HERMES_NEEDS = {
    "A1.1": (30, "N7 required"), "A1.2": (30, "N7 required"), "A1.3": (50, "N7 preferred"), "A1.4": (50, "N7 preferred"),
    "A1.5": (30, "N7 required"), "A2.1": (None, "not needed"), "A2.2": (None, "not needed"), "A2.3": (30, "N7 required"),
    "A3.1": (None, "not needed"), "B1.1": (50, "not needed"), "B1.2": (100, "not needed"), "B1.3": (None, "not needed"),
    "B1.4": (None, "not needed"), "B1.5": (None, "not needed"), "B2.1": (30, "not needed"), "B2.2": (50, "not needed"),
    "B2.3": (30, "not needed"), "B2.4": (100, "not needed"), "B2.5": (100, "not needed"), "B2.6": (50, "not needed"),
    "B2.7": (30, "not needed"), "B3.1": (50, "not needed"), "B3.2": (50, "not needed"), "B3.3": (50, "not needed"),
    "B3.4": (50, "not needed"), "B3.5": (50, "not needed"), "B3.6": (50, "not needed"), "B3.7": (50, "not needed"),
    "B3.8": (30, "not needed"), "C1.1": (100, "not needed"), "C1.2": (None, "not needed"), "C1.3": (100, "not needed"),
    "C1.4": (50, "not needed"), "C1.5": (None, "not needed"), "C1.6": (None, "not needed"), "C1.7": (None, "N7 preferred"),
    "D1.1": (100, "not needed"), "D1.2": (100, "not needed"), "D1.3": (100, "not needed"), "D1.4": (50, "not needed"),
    "D1.5": (50, "not needed"), "D1.6": (50, "not needed"), "D1.7": (None, "not needed"), "E1.1": (100, "N7 helpful"),
    "E1.2": (None, "not needed"), "E1.3": (50, "not needed"), "E1.4": (100, "N7 helpful"), "E1.5": (50, "N7 helpful"),
    "E1.6": (30, "N7 helpful"), "F1.1": (30, "not needed"), "F1.2": (50, "not needed"), "F1.3": (30, "not needed"),
    "F1.4": (100, "not needed"), "F1.5": (100, "not needed"), "F1.6": (100, "not needed"), "F1.7": (None, "not needed"),
    "F1.8": (200, "not needed"), "F1.9": (None, "not needed"), "F1.10": (50, "N7 helpful"), "G1.1": (50, "not needed"),
    "G1.2": (100, "not needed"), "G1.3": (100, "not needed"), "G1.4": (None, "not needed"),
}


# ---------------------------------------------------------------------------------------------------------
# Interaction rules. when: weather_any / light_any / season_any / hour_range / temp_min / aqi_min / festival
#                         tags_any (element) / ids_any (element) / co_present_tags_any / co_present_any (ids)
#                  effect: mul / add / set on attributes, creates: compound element id
# ---------------------------------------------------------------------------------------------------------
WET = ["drizzle", "rain", "heavy_rain", "storm"]
RAIN = ["rain", "heavy_rain", "storm"]
NIGHTS = ["night_lit", "night_dark"]
INTERACTIONS = [
    ("rain_x_hole_hidden", dict(weather_any=RAIN, tags_any=["hole"]), dict(mul={"visibility_needed": 1.3, "fall": 1.4}, set={"cane_detectable": 0.3}, add={"water_cm": 5}), "hidden_hole_under_water", "Rain fills holes; the surface looks flat, the depth is unknown (W1, 6.03, S42, S44)", "FU"),
    ("waterlog_x_kerb_unknown", dict(tags_any=["kerb"], co_present_tags_any=["flood"]), dict(add={"water_cm": 10, "fall": 0.3}, set={"cane_detectable": 0.3, "visibility_needed": 1.0}), "kerb_height_unknown_under_water", "Standing water hides kerb edge and height (W27)", "FU"),
    ("waterlog_x_drain", dict(tags_any=["drain"], weather_any=RAIN), dict(mul={"fall": 1.5}, set={"visibility_needed": 1.0, "cane_detectable": 0.2}, add={"water_cm": 10}), "hidden_hole_under_water", "Open drains under floodwater drown people (S42, S43, F14.14): never route through", "FU"),
    ("night_x_dark_x_drain", dict(light_any=["night_dark"], tags_any=["drain", "hole"]), dict(mul={"fall": 1.5, "visibility_needed": 1.2}), "night_open_drain_fall", "No streetlight plus an open drain or hole: fall hazard (user example)", A),
    ("night_x_hole", dict(light_any=NIGHTS, tags_any=["hole"]), dict(mul={"fall": 1.25}), "dark_pothole", "Pothole seen by day is hard to see at night (7.05, W73)", "FU"),
    ("dust_x_low_contrast", dict(weather_any=["dust_storm", "smog", "fog", "haze"], tags_any=["low_contrast", "marking", "kerb", "step", "faded"]), dict(add={"contrast_loss": 0.4}, mul={"visibility_needed": 1.2}), None, "Dust, smog or fog removes the little contrast a kerb edge or marking had (low vision)", A),
    ("smog_x_crossing", dict(weather_any=["smog", "fog"], tags_any=["crossing"]), dict(mul={"vehicle": 1.3}, add={"contrast_loss": 0.4}), "smog_crossing_blind_spot", "In fog/smog drivers see walkers late (S48, W63)", "FU"),
    ("heat_x_metal", dict(temp_min=38, tags_any=["metal", "railing", "handrail"]), dict(add={"heat": 0.5}), "burning_metal_rail", "Sun-heated metal railings, covers and handrims burn hands (6.07, M532)", A),
    ("heat_x_dark_surface", dict(temp_min=38, tags_any=["dark_surface", "unshaded"]), dict(add={"heat": 0.3}), None, "Dark paving in the sun reaches about 55 C (INDIA-CHAOS A10)", A),
    ("crowd_x_traffic_noise", dict(tags_any=["crowd", "loud"], co_present_tags_any=["vehicle", "crossing"]), dict(add={"vehicle": 0.2, "noise_db": 5}), "traffic_masked_by_noise", "Crowd and noise mask vehicle sounds blind and hard-of-hearing walkers rely on", A),
    ("festival_x_narrow", dict(festival=True, tags_any=["narrow", "crowd"]), dict(mul={"crowd": 1.3}, add={"fall": 0.3}), "festival_lane_crush", "Festival crowd plus a narrow approach caused the Kolkata Durga Puja crush (S60, S123)", "FU"),
    ("glare_x_faded_zebra", dict(light_any=["dawn", "dusk"], tags_any=["faded", "marking"]), dict(add={"contrast_loss": 0.4, "vehicle": 0.15}), "invisible_faded_zebra", "Low-sun glare washes out a faded zebra for walkers and drivers (7.07, 2.20)", A),
    ("rain_x_smooth_stone", dict(weather_any=WET, tags_any=["smooth_stone", "wet_slippery", "metal"]), dict(mul={"slip": 2.5}), "wet_polished_slope", "Polished granite, tiles and metal plates turn slippery when wet (2.18, W96)", "FU"),
    ("rain_x_unpaved", dict(weather_any=RAIN, tags_any=["unpaved"]), dict(add={"slip": 0.4, "roughness": 0.2, "water_cm": 3}), None, "Kuccha paths turn to mud (W83)", A),
    ("rain_x_slope", dict(weather_any=WET, tags_any=["slope", "ramp", "step"]), dict(add={"slip": 0.3}), None, "Wet ramps and steps are where slips happen", A),
    ("waterlog_x_pole_electric", dict(tags_any=["electrical"], co_present_tags_any=["water", "flood"]), dict(set={"electric": 1.0}), "live_wire_in_water", "Electrified water near poles killed walkers (S50, S51, S121)", "FU"),
    ("rain_x_electrical", dict(weather_any=["heavy_rain", "storm"], tags_any=["electrical"]), dict(add={"electric": 0.5}), "live_wire_in_water", "Heavy rain plus exposed wiring (6.04)", "FU"),
    ("wind_x_tree", dict(weather_any=["storm", "dust_storm", "wind"], tags_any=["tree", "overhead"]), dict(add={"overhead": 0.4}), "dust_storm_tree_fall", "Tree and branch falls in storms (6.05, S52, S124)", "FU"),
    ("night_x_dogs", dict(light_any=NIGHTS, tags_any=["dog"]), dict(mul={"animal": 1.4}), "dog_pack_dark_lane", "Dog packs are more aggressive at night (3.27, W75)", "FU"),
    ("night_x_isolated", dict(light_any=NIGHTS, tags_any=["isolated", "harassment", "crime"]), dict(add={"cognitive": 0.3}), None, "Dark spots are linked to harassment (S56)", "FU"),
    ("ramp_x_pothole", dict(tags_any=["ramp"], co_present_tags_any=["hole"]), dict(add={"vertical_cm": 8, "fall": 0.4}), "ramp_into_pothole", "A kerb ramp that opens into a pothole is not a ramp (W159)", "FU"),
    ("crowd_x_ramp", dict(tags_any=["ramp"], co_present_tags_any=["crowd", "vendor"]), dict(set={"clear_width_cm": 30}), "crowd_blocks_ramp", "Crowd or vendor on the only ramp makes it effectively absent (INDIA-CHAOS 13)", A),
    ("parked_x_ramp", dict(tags_any=["ramp"], co_present_tags_any=["vehicle"]), dict(set={"clear_width_cm": 0}), None, "A parked vehicle on a ramp blocks it now (W13)", "FU"),
    ("cold_x_shade_slope", dict(weather_any=["cold_wave", "snow"], tags_any=["step", "slope", "ramp"]), dict(add={"slip": 0.6}), "icy_shaded_steps", "Morning ice on shaded steps and slopes (6.13)", A),
    ("rain_x_trench", dict(weather_any=RAIN, tags_any=["construction"]), dict(add={"water_cm": 20, "fall": 0.2}, set={"visibility_needed": 1.0}), "flooded_trench", "Open trenches fill with rainwater and vanish (2.11 x 6.03)", A),
    ("heat_x_slope", dict(temp_min=38, tags_any=["slope", "ramp", "step", "hill"]), dict(add={"heat": 0.4, "effort": 0.3}), "heat_long_unshaded_climb", "Climbing in heat (6.06, W57)", "IMD_HEAT"),
    ("fog_x_dark_crossing", dict(weather_any=["fog"], light_any=NIGHTS + ["dawn"], tags_any=["crossing"]), dict(add={"vehicle": 0.3, "contrast_loss": 0.4}), "fog_unlit_crossing", "Foggy dark crossings (6.09 x 7.01)", "FU"),
    ("glare_x_step", dict(light_any=["dawn", "dusk"], tags_any=["step", "kerb", "lip"]), dict(add={"glare": 0.6, "fall": 0.2}, mul={"visibility_needed": 1.2}), "glare_hides_step", "Low sun glare hides step edges (7.07 x 7.08)", A),
    ("procession_x_road_walk", dict(tags_any=["festival"], co_present_tags_any=["road_walk"]), dict(add={"vehicle": 0.3, "crowd": 0.2}), "procession_on_no_footpath_road", "A procession on a road with no footpath pushes walkers into traffic", A),
    ("silent_ev_x_crowd", dict(tags_any=["silent_vehicle"], co_present_tags_any=["crowd", "loud"]), dict(add={"vehicle": 0.25}), "silent_ev_in_crowd", "Quiet EVs in crowds are not heard by blind walkers", A),
    ("night_x_lowcontrast", dict(light_any=NIGHTS, tags_any=["low_contrast", "kerb", "step", "lip"]), dict(mul={"visibility_needed": 1.3}, add={"contrast_loss": 0.3}), None, "Kerb edges and steps lose contrast after dark (7.08)", "FU"),
    ("festival_x_noise", dict(festival=True, tags_any=["loud", "festival"]), dict(add={"noise_db": 10, "flicker": 0.2}), None, "Festival nights add DJ trucks and firecrackers (5.06, W69)", A),
    ("aqi_x_airborne", dict(aqi_min=201, tags_any=["air", "dust", "smoke", "fumes"]), dict(add={"air": 0.2}), None, "Local dust or smoke on top of a poor-AQI day (CPCB poor band 201-300)", "CPCB_AQI"),
    ("dry_x_dust", dict(season_any=["summer"], tags_any=["dust", "unpaved"]), dict(add={"air": 0.15}), None, "Dry season lifts more dust", A),
    ("monsoon_x_flood_prone", dict(season_any=["monsoon"], tags_any=["flood_prone"]), dict(add={"water_cm": 8}, set={"visibility_needed": 1.0}), "hidden_hole_under_water", "Spots with past flood marks flood again in monsoon (MAX-INFO 3)", A),
    ("night_x_vehicle", dict(light_any=["night_dark"], tags_any=["road_walk", "crossing", "fast_road"]), dict(mul={"vehicle": 1.3}), None, "Drivers do not see walkers in the dark (7.16)", "FU"),
    ("rain_x_crowd", dict(weather_any=RAIN, tags_any=["crowd"]), dict(add={"slip": 0.3, "crowd": 0.1}), None, "Crowd rush in rain in a narrow lane (S123)", "FU"),
    ("heat_x_crowd", dict(temp_min=38, tags_any=["crowd", "queue"]), dict(add={"heat": 0.3}), None, "Standing in a crowd in heat", A),
    ("holi_x_slip", dict(festival=True, tags_any=["wet_slippery", "smooth_stone"]), dict(add={"slip": 0.3}), None, "Holi colour water on smooth surfaces (W70)", A),
    ("night_x_construction", dict(light_any=NIGHTS, tags_any=["construction"]), dict(mul={"fall": 1.4, "visibility_needed": 1.3}), None, "Unlit work sites at night (2.11, 7.05)", A),
    ("rain_x_overhead_drip", dict(weather_any=WET, tags_any=["overhead"]), dict(add={"slip": 0.1}), None, "Awnings and AC units drip onto the walking line", A),
    ("wind_x_dust_unpaved", dict(weather_any=["dust_storm", "wind"], tags_any=["unpaved", "dust", "construction"]), dict(add={"air": 0.4, "contrast_loss": 0.3}), None, "Wind lifts dust from unpaved and construction spots (3.34, S47)", "FU"),
    ("dusk_x_vendor_crowd", dict(hour_range=[17, 21], tags_any=["vendor"]), dict(add={"crowd": 0.2}, mul={"clear_width_cm": 0.8}), None, "Evening vendor peak narrows the path further (5.01)", A),
    ("school_x_crossing", dict(hour_range=[13, 15], tags_any=["crossing"], co_present_tags_any=["crowd"]), dict(add={"crowd": 0.3, "vehicle": 0.1}), None, "School dispersal at a crossing (5.03, M521)", A),
    ("night_x_flicker", dict(light_any=NIGHTS, tags_any=["flicker"]), dict(mul={"flicker": 1.3}), None, "Flicker is stronger against a dark background", A),
    ("rain_x_metal_cover", dict(weather_any=WET, tags_any=["metal"], co_present_tags_any=["slope", "ramp"]), dict(add={"slip": 0.4}), "wet_polished_slope", "Wet metal plate on a slope", A),
]

# subcategories for hermes' flat sections C to G (claude grouping, display and tree only; scoring is per leaf)
SUBGROUP = {
    "C1.1": "Intellectual and learning", "C1.2": "Intellectual and learning", "C1.7": "Intellectual and learning",
    "C1.3": "Sensory processing", "G1.3": "Sensory processing", "C1.4": "Neurological", "C1.5": "Neurological",
    "C1.6": "Mental health", "G1.4": "Mental health",
    "D1.1": "Cardio-respiratory", "D1.2": "Cardio-respiratory", "D1.3": "Blood disorders", "D1.8*": "Blood disorders",
    "D1.4": "Fatigue and pain", "D1.5": "Fatigue and pain", "D1.6": "Metabolic and continence",
    "D1.7": "Metabolic and continence", "E1.1": "Children and adolescents", "E1.2": "Children and adolescents",
    "E1.3": "Pregnancy", "E1.4": "Older adults", "E1.5": "Older adults", "E1.6": "Older adults",
    "E1.7*": "Older adults", "F1.1": "Injury and recovery", "F1.2": "Injury and recovery",
    "F1.3": "Injury and recovery", "F1.4": "Pushing wheels", "F1.7": "Pushing wheels", "F1.8": "Pushing wheels",
    "F1.9": "Pushing wheels", "F1.5": "Carrying", "F1.6": "Carrying", "F1.10": "Accompanied", "Z0*": "Baseline",
    "G1.1": "Body-state sensitivities", "G1.2": "Body-state sensitivities",
}

# rules about seeing (light, glare, contrast): skipped for bodies with no useful vision (blind, deaf-blind),
# because darkness changes nothing for a cane user (claude design)
SIGHTED_ONLY = {"night_x_dark_x_drain", "night_x_hole", "dust_x_low_contrast", "glare_x_faded_zebra",
                "glare_x_step", "night_x_lowcontrast", "night_x_construction", "night_x_flicker"}

# ---------------------------------------------------------------------------------------------------------


def build():
    elements, tree_out = [], []
    for cid, cname, subs in TREE:
        c_node = {"id": cid, "name": cname, "subcategories": []}
        for sid, sname, rows in subs:
            s_node = {"id": sid, "name": sname, "elements": []}
            for (eid, name, arch, ov, tmp, det, dcls, refs, tags, asrc) in rows:
                attrs = {a: None for a in AXES}
                attrs.update({"spans_path": False, "cane_detectable": 1.0})
                attrs.update(ARCH[arch])
                attrs.update(ov)
                el = {"id": eid, "name": name, "category": cid, "subcategory": sid, "archetype": arch,
                      "attrs": attrs, "temporal": tmp, "detect_from_photo": det, "detector_class": dcls,
                      "factor_refs": refs, "tags": sorted(set(tags + [arch])),
                      "attrs_source": asrc if asrc in SOURCES else "ASSUMPTION",
                      "attrs_note": SOURCES.get(asrc, "claude design value from archetype + overrides")}
                elements.append(el)
                s_node["elements"].append(eid)
            c_node["subcategories"].append(s_node)
        tree_out.append(c_node)
    ids = [e["id"] for e in elements]
    assert len(ids) == len(set(ids)), "duplicate element id"

    bodies, btree = [], {}
    for r in BODY_ROWS:
        if len(r["path"]) == 1:  # hermes sections C to G are flat: add a subcategory (claude grouping)
            r["path"] = r["path"] + [SUBGROUP[r["hermes_id"]]]
        sens = dict(BASE_BY_SCORER[r["scorer"]])
        sens.update(r["sens_edits"])
        body = {k: v for k, v in r.items() if k != "sens_edits"}
        body["sensitivity"] = {a: round(float(sens[a]), 3) for a in SENS_AXES}
        hid = r["hermes_id"]
        hn = HERMES_NEEDS.get(hid) or HERMES_NEEDS.get(hid.rstrip("*"))
        rest = hn[0] if hn else None
        body["rest_spacing_m"] = rest
        body["tactile_need"] = hn[1] if hn else "not stated"
        body["hermes_leaf"] = hid if hid in HERMES_NEEDS else None
        needs = [{"need": "speed_mps", "value": r["speed_mps"],
                  "flag": "SOURCED" if r["speed_source"] in SOURCES else "A", "source": r["speed_source"]}]
        if rest:
            needs.append({"need": "rest_spacing_m", "value": rest, "flag": "A",
                          "source": f"HERMES_BODY leaf {hid} (hermes assumption)"})
        if hn:
            needs.append({"need": "tactile", "value": hn[1], "flag": "N7" if "N7" in hn[1] else "-",
                          "source": "HERMES_BODY N7 (IRC:103 tactile clause)"})
        for k, v in r["limits"].items():
            src = r["limit_sources"].get(k, "ASSUMPTION")
            needs.append({"need": k, "value": v, "flag": "A" if "ASSUMPTION" in str(src) or src == "ASSUMPTION" else "SOURCED",
                          "source": src})
        body["needs"] = needs
        body["sensitivity_source"] = ("ASSUMPTION: scorer base vector + per-leaf edits, graded from hermes "
                                      "BODY-TAXONOMY.md qualitative columns via GRADE map")
        bodies.append(body)
        node = btree
        for p in r["path"]:
            node = node.setdefault(p, {})
        node.setdefault("_leaves", []).append(r["id"])
    bids = [b["id"] for b in bodies]
    assert len(bids) == len(set(bids)), "duplicate body id"

    by_id = {e["id"]: e for e in elements}
    rules = []
    for rid, when, eff, creates, reason, src in INTERACTIONS:
        if creates:
            assert creates in by_id, creates
        rules.append({"id": rid, "when": when, "effect": eff, "creates": creates, "reason": reason,
                      "source": src if src in SOURCES else "ASSUMPTION",
                      "sighted_only": rid in SIGHTED_ONLY})

    meta = {"generated_by": "app/route/taxonomy/build_taxonomy.py", "sources": SOURCES}
    with open(os.path.join(HERE, "elements.json"), "w") as f:
        json.dump({**meta, "axes": AXIS_DOC, "hour_curves": HOUR_CURVES, "hour_curves_source": HOUR_CURVES_SOURCE,
                   "season_profiles": SEASON_PROFILES, "tree": tree_out, "elements": elements}, f, indent=1)
    with open(os.path.join(HERE, "bodies.json"), "w") as f:
        json.dump({**meta, "sensitivity_axes": SENS_AXES, "grade_map": GRADE,
                   "scorers": sorted(BASE_BY_SCORER), "scorer_base": BASE_BY_SCORER, "tree": btree,
                   "bodies": bodies}, f, indent=1)
    with open(os.path.join(HERE, "interactions.json"), "w") as f:
        json.dump({**meta, "rules": rules}, f, indent=1)
    return elements, bodies, rules


if __name__ == "__main__":
    e, b, r = build()
    print(f"elements {len(e)}, bodies {len(b)}, interactions {len(r)}")
