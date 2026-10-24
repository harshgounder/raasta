#!/usr/bin/env python3
"""Parse research/hermes/sc02/WHATIF-TREE.md into app/site/public/content/whatif-tree.json.

  python3 app/site/tools/build_whatif.py            (from the project root, or anywhere)

Re-running picks up new rows: every markdown table row whose first cell is an id like T1.2.3 is read.
Every row is kept. A recipe that needs a fallback is marked "fixed" with the reason; one that cannot be
mapped to the engine is marked "flagged" with the reason (it still gets a run, comparing bodies).

Recipe grammar (hermes): `city; inject <what> [size] [at|near|on <place>]; <body leaf>; HH:MM; weather; light`.
The <what> text is mapped to taxonomy element ids (app/route/taxonomy/elements.json) by the ordered keyword
RULES below; ids that need a special run (confidence, hour compare, body compare) are in OVERRIDES.
All mappings are claude's reading of the recipe text (2026-10-25), listed per item in recipe_notes.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SRC = os.path.join(ROOT, 'research', 'hermes', 'sc02', 'WHATIF-TREE.md')
TAX = os.path.join(ROOT, 'app', 'route', 'taxonomy')
MATRIX = os.path.join(ROOT, 'app', 'site', 'public', 'content', 'impact-matrix.json')
OUT = os.path.join(ROOT, 'app', 'site', 'public', 'content', 'whatif-tree.json')
RUNS = os.path.join(ROOT, 'app', 'site-data', 'whatif')  # precompute output; when present, each item gets a run summary

CITIES = {'jaipur', 'chandigarh', 'varanasi', 'jaipur-photos'}

# glyph keys that app/site/src/map2/icons.js draws; anything else falls back to the element category key
ICON_TYPES = {'pole_obstruction', 'parked_vehicle', 'broken_footpath', 'missing_kerb_ramp', 'kerb_ramp_present', 'steps',
              'pothole', 'vendor', 'missing_footpath', 'open_drain', 'waterlogging', 'steep_slope', 'crossing_marked', 'clear'}

# ordered: first match per recipe piece wins (specific before general). (regex, [element ids], {attr overrides})
RULES = [
    (r'puddle', ['pothole', 'puddle_reflection'], {}),
    (r'ramp and steps', ['kerb_ramp_good', 'steps_short_flight'], {}),
    (r'rebuilt', ['kerb_ramp_good'], {}),
    (r'blocked route', ['kerb_high_22_no_ramp'], {}),
    (r'blocked ramp|repair promise', ['kerb_150_no_ramp'], {}),
    (r'waterlogged pothole', ['pothole', 'waterlogging_shallow'], {}),
    (r'underpass', ['flooded_underpass'], {}),
    (r'flood history|flood-dated|flood record', ['waterlogging_shallow'], {}),
    (r'waterlogging|waterlogged', ['waterlogging_shallow'], {}),
    (r'kerb 180 mm|high kerb', ['kerb_high_22_no_ramp'], {}),
    (r'low-contrast kerb', ['kerb_edge_no_contrast'], {}),
    (r'repaired kerb', ['kerb_ramp_good'], {}),
    (r'25 mm lip', ['ramp_bottom_lip_3'], {'vertical_cm': 2.5}),
    (r'crossing with one missing ramp', ['kerb_150_no_ramp'], {}),
    (r'missing_kerb_ramp|missing ramp|no ramp|kerb 150 mm|curb|kerb', ['kerb_150_no_ramp'], {}),
    (r'pole on tactile', ['tactile_leads_into_pole'], {}),
    (r'missing tactile|without tactile', ['no_marked_crossing'], {}),
    (r'tactile', ['tactile_paving_correct'], {}),
    (r'faded zebra', ['zebra_faded'], {}),
    (r'crossing_marked', ['zebra_good'], {}),
    (r'unmarked', ['no_marked_crossing'], {}),
    (r'no refuge|long crossing', ['no_median_refuge'], {}),
    (r'\bs signal|two signals', ['signal_short_green'], {}),
    (r'foot over bridge', ['fob_stairs_only'], {}),
    (r'stairs-only subway', ['subway_stairs_only'], {}),
    (r'slip road', ['free_left_turn'], {}),
    (r'level crossing', ['rail_flangeway_gap'], {}),
    (r'failed crossing', ['signal_dead'], {}),
    (r'drain smell', ['sewer_gas_odour'], {}),
    (r'open_drain|open drain', ['open_drain_parallel'], {}),
    (r'dark asphalt', ['hot_dark_paving'], {}),
    (r'unshaded|no shade|open stretch|shaded versus', ['high_sun_no_shade'], {}),
    (r'risers|steps', ['steps_short_flight'], {}),
    (r'narrow passage|narrow 0', ['narrow_footpath_80'], {}),
    (r'1\.2 m passage|narrow 1\.2', ['narrow_footpath_110'], {'clear_width_cm': 120}),
    (r'utility plate|metal plate', ['metal_plate_cover'], {}),
    (r'metal ramp', ['hot_metal_surface'], {}),
    (r'construction zone|construction corridor|construction dust|dust corridor|dust', ['construction_dust'], {}),
    (r'mud', ['mud_kuccha'], {}),
    (r'loose sand|sand', ['sand_layer'], {}),
    (r'smoke', ['garbage_burning_smoke'], {}),
    (r'school', ['school_van_drop', 'crowd_dense'], {}),
    (r'exposed stretch', ['wind_gusts'], {}),
    (r'awning with drip', ['low_awning'], {}),
    (r'open manhole|manhole', ['open_manhole'], {}),
    (r'low lighting|market lighting', ['streetlight_sparse'], {}),
    (r'unlit', ['streetlight_off'], {}),
    (r'lamp glare', ['headlight_glare'], {}),
    (r'west-facing', ['low_sun_glare_ew'], {}),
    (r'shadow boundary', ['deep_shadow_band'], {}),
    (r'vendor cluster|vendors', ['vendor_handcart', 'vendor_ground_mat'], {}),
    (r'handcart|fruit cart|vendor', ['vendor_handcart'], {}),
    (r'parked bikes|bike cluster|parked_vehicle|two-wheeler', ['two_wheeler_parked_footpath'], {}),
    (r'parked cars|parked vehicle', ['car_parked_footpath'], {}),
    (r'\bauto\b', ['auto_rickshaw_stand'], {}),
    (r'truck|tractor|loading', ['loading_unloading'], {}),
    (r'rickshaw', ['e_rickshaw_queue'], {}),
    (r'missing tiles', ['missing_pavers'], {}),
    (r'broken|paving', ['broken_pavers'], {}),
    (r'raised slab|dip\b', ['patch_height_mismatch'], {}),
    (r'patchwork', ['uneven_patchwork'], {}),
    (r'gravel', ['gravel_loose'], {}),
    (r'tree root', ['tree_root_heave'], {}),
    (r'leaves', ['wet_leaves_algae'], {}),
    (r'wet polished', ['wet_polished_slope'], {}),
    (r'polished', ['polished_granite'], {}),
    (r'oil spill', ['oil_spill'], {}),
    (r'cobble', ['cobbles_setts'], {}),
    (r'joint|tile-to-cobble', ['wide_joint_gap'], {}),
    (r'pole_obstruction|single-detector pole|pole after', ['electric_pole_midpath'], {}),
    (r'bollard', ['bollards_narrow_80'], {}),
    (r'tree pit', ['tree_pit_open'], {}),
    (r'meter box', ['water_meter_box'], {}),
    (r'utility box', ['junction_box'], {}),
    (r'\bsign\b', ['low_signboard'], {}),
    (r'guardrail', ['guardrail_continuous'], {}),
    (r'5 obstacles', ['electric_pole_midpath', 'junction_box', 'bench_in_path'], {}),
    (r'raised cover', ['utility_cover_raised'], {'vertical_cm': 5}),
    (r'low branch', ['low_branch'], {}),
    (r'scaffolding', ['scaffolding_overhead'], {}),
    (r'awning', ['low_awning'], {}),
    (r'cables 3 crossings|hose', ['washing_water_hose'], {}),
    (r'cable', ['overhead_wires_low'], {}),
    (r'shutter|pipe|railing end', ['protrusion_100mm_plus'], {}),
    (r'banner', ['hanging_banner'], {}),
    (r'ac unit', ['ac_unit_dripping'], {}),
    (r'hoarding', ['hoarding_pole'], {}),
    (r'shared-traffic|shared-use', ['two_wheelers_on_footpath'], {}),
    (r'dog', ['stray_dog_pack'], {}),
    (r'animal zone', ['monkeys'], {}),
    (r'animal|cattle', ['stray_cattle'], {}),
    (r'aarti', ['religious_queue_darshan'], {}),
    (r'wedding', ['procession_baraat'], {}),
    (r'festival', ['crowd_dense'], {}),
    (r'market crowd', ['weekend_market_crowd'], {}),
    (r'crowd', ['crowd_dense'], {}),
    (r'queue', ['queue_outside_shop'], {}),
    (r'closure', ['police_barricade'], {}),
    (r'tea stall', ['tea_stall_crowd'], {}),
    (r'display|encroachment|cylinders', ['shop_display_spill'], {}),
    (r'tables', ['cafe_seating_spill'], {}),
    (r'generator', ['generator_set'], {}),
    (r'debris|site gate|site blocking', ['construction_debris'], {}),
    (r'trench', ['open_trench'], {}),
    (r'half-finished', ['half_built_footpath'], {}),
    (r'barricade|metro corridor', ['metro_barricade'], {}),
    (r'cement', ['cement_mixer'], {}),
    (r'night works', ['jackhammer_construction'], {}),
    (r'1:10 ramp', ['kerb_ramp_steep_1in10'], {}),
    (r'1:12 ramp', ['ramp_steep_long'], {'slope_pct': 8.33, 'run_m': 8}),
    (r'percent slope|slope', ['running_slope_6'], {}),
    (r'no bench', ['no_rest_200m'], {}),
    (r'two benches', ['bench_available'], {}),
    (r'camber', ['cross_slope_4'], {}),
    (r'missing_footpath|wrong osm footway', ['no_footpath_road_walk'], {}),
    (r'state highway', ['fast_road_edge'], {}),
    (r'railway', ['rail_level_crossing'], {}),
    (r'private colony', ['gated_road_closed'], {}),
    (r'heritage', ['cobbles_setts'], {}),
    (r'clearance event', ['vendor_handcart'], {}),
    (r'pothole', ['pothole'], {}),
    (r'evidence|report|barrier|complaint|kerb measured|unknown kerb|off-segment', ['kerb_150_no_ramp'], {}),
]

# per-id special runs. confidence < block_p (0.5) turns a block into a soft cost: that is how the engine treats
# weak or contradicted evidence, which is what these rows ask about.
OVERRIDES = {
    'T1.1.7': {'elements': ['oil_spill'], 'note': 'first rain: the oil and dust film on the surface is read as the oil-spill slip element'},
    'T2.3.4': {'elements': ['vendor_handcart', 'two_wheeler_parked_footpath'], 'compare': 'hour', 'base_hour': 18.0, 'temporary': True,
               'note': 'a vendor cart and parked two-wheelers seen at 19:00 the evening before; the run compares 18:00 (baseline) with 06:00 through the hour curves'},
    'T9.3.7': {'elements': ['vendor_handcart', 'two_wheeler_parked_footpath'], 'compare': 'hour', 'base_hour': 18.0, 'temporary': True,
               'note': 'a vendor cart and parked two-wheelers seen at 19:00 the evening before; the run compares 18:00 (baseline) with 06:00 through the hour curves'},
    'T6.1.1': {'elements': ['kerb_high_22_no_ramp'], 'attrs': {'vertical_cm': 23}, 'note': 'kerb height 23 cm taken from the question'},
    'T12.1.1': {'elements': ['kerb_high_22_no_ramp'], 'attrs': {'vertical_cm': 23}, 'confidence': 0.6,
                'note': 'measured 23 cm against a user report of 10 cm: the measurement is kept at confidence 0.6 until a new photo'},
    'T7.1.1': {'confidence': 0.6, 'observed_at': '2019-03-01', 'note': '2019 evidence: kerb record at confidence 0.6'},
    'T7.1.2': {'confidence': 0.45, 'observed_at': '2010-01-01', 'note': '2010 evidence: confidence 0.45, below the 0.5 block line'},
    'T7.1.3': {'confidence': 0.5, 'observed_at': None, 'note': 'undated evidence: confidence 0.5'},
    'T7.1.4': {'p_attach': 0.35, 'note': 'record 40 m off-segment: attach probability 0.35'},
    'T7.1.5': {'confidence': 0.7, 'note': 'car-height capture: confidence 0.7'},
    'T7.1.6': {'confidence': 0.55, 'note': 'flood-dated evidence: confidence 0.55'},
    'T7.1.8': {'confidence': 0.95, 'note': 'three dated records agree: confidence 0.95'},
    'T7.2.4': {'confidence': 0.55, 'note': 'one detector only: confidence 0.55'},
    'T7.2.5': {'confidence': 0.4, 'note': 'vehicle seen on the carriageway, not the footpath: confidence 0.4 for the footpath'},
    'T7.2.6': {'confidence': 0.3, 'note': 'vendor recorded but cleared since: confidence 0.3'},
    'T7.2.8': {'confidence': 0.3, 'note': 'flood record on a dry day: confidence 0.3'},
    'T7.2.9': {'confidence': 0.5, 'note': 'repair claim against a broken photo: confidence 0.5 until a new photo'},
    'T7.3.1': {'confidence': 0.95, 'note': 'fresh user photo: confidence 0.95'},
    'T7.3.3': {'p_attach': 0.3, 'note': 'report with 60 m GPS error: attach probability 0.3'},
    'T7.3.4': {'confidence': 0.5, 'note': 'pin-only report, no photo: confidence 0.5'},
    'T7.3.5': {'confidence': 0.5, 'note': 'two contradictory reports: confidence 0.5'},
    'T7.3.6': {'confidence': 0.3, 'note': 'clear report after a pothole: pothole confidence 0.3'},
    'T7.3.9': {'confidence': 0.7, 'note': 'child report: confidence 0.7'},
    'T7.3.10': {'duplicate': True, 'note': 'two pothole reports 3 m apart: the engine clusters them (5 m dedupe)'},
    'T8.1.7': {'confidence': 0.6, 'note': 'anonymous report: confidence 0.6'},
    'T8.2.8': {'confidence': 0.2, 'note': 'vendor after a clearance drive: confidence 0.2'},
    'T10.1.2': {},
    'T10.1.5': {'confidence': 0.6, 'observed_at': '2019-03-01', 'note': '2019 evidence: kerb record at confidence 0.6'},
    'T10.2.4': {'confidence': 0.5, 'note': 'kerb height not measured: confidence 0.5'},
    'T11.1.3': {'elements': ['two_wheeler_parked_footpath'], 'attrs': {'clear_width_cm': 100}, 'compare': 'hour', 'base_hour': 9.0, 'temporary': True,
                'note': 'two-wheelers parked on the footpath leaving 100 cm, seen at 19:00 the evening before; same trip at 09:00 (baseline) and 18:00 (what-if): the parking hour curve changes the minutes, the path stays'},
    'T12.1.4': {'p_attach': 0.3, 'note': 'photo off the segment: attach probability 0.3'},
    'T12.1.5': {'confidence': 0.3, 'note': '20 identical text reports, no photo: confidence 0.3 (rate-limited as one)'},
}
# scenario rows with no physical thing to inject: the run compares the asking body with an adult with no impairment
BODY_COMPARE_WORDS = r'any route|generated segments|unknown segments|unknown stretch|upload|two routes|end of a|skipped|compare two wards|route card|shared device|offline|voice-first|low-end|export|school route|aeroplane|build a network|simulate|stale segments|ops page|boundary|mall frontage|bus depot|flyover|accessible versus shortest|route to a hospital'

WEATHER = {'dry': 'clear', 'clear': 'clear', 'rain': 'rain', 'first rain': 'rain', 'after rain': 'drizzle',
           'heavy rain': 'heavy_rain', 'flood': 'heavy_rain', 'hot': 'clear', 'fog': 'fog', 'windy': 'wind',
           'cold': 'cold_wave', 'hazy': 'haze'}
SEASON = {'rain': 'monsoon', 'first rain': 'monsoon', 'heavy rain': 'monsoon', 'flood': 'monsoon', 'after rain': 'monsoon',
          'hot': 'summer', 'fog': 'winter', 'cold': 'winter', 'windy': 'summer'}
LIGHT = {'day': 'day', 'dusk': 'dusk', 'dawn': 'dawn', 'night': 'night_lit', 'hazy': 'day'}


def clean(s):
    return re.sub(r'\s+', ' ', s.replace('\u2014', ', ').replace('\u2013', '-')).strip()


def parse_rows(md):
    rows = []
    for ln in md.splitlines():
        if not re.match(r'^\|\s*T\d+\.\d+\.\d+\s*\|', ln):
            continue
        cells = [clean(c) for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    return rows


def id_key(i):
    return tuple(int(x) for x in i[1:].split('.'))


def map_elements(text, E):
    """recipe inject text -> (elements, attrs, notes). Pieces split on 'plus' / 'versus'."""
    els, attrs, notes = [], {}, []
    low = text.lower()
    for piece in re.split(r'\bplus\b|\bversus\b', low):
        for rx, ids, over in RULES:
            if re.search(rx, piece):
                for i in ids:
                    if i in E and i not in els:
                        els.append(i)
                attrs.update(over)
                break
    return els[:3], attrs, notes


def numbers(text, els, E, attrs, notes):
    low = text.lower()
    span = None
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s*m\b(?!m)', low):
        v = float(m.group(1))
        if v < 2.5:
            for e in els:
                a = E[e]['attrs']
                if 'clear_width_cm' in a and a.get('clear_width_cm') is not None and E[e]['category'] in (
                        'geometry', 'fixed_obstacles', 'temporary_obstacles'):
                    attrs.setdefault('clear_width_cm', round(v * 100))
                    break
        else:
            span = max(span or 0, v)
    m = re.search(r'kerb (\d+) mm', low)
    if m:
        attrs['vertical_cm'] = int(m.group(1)) / 10
    m = re.search(r'(\d+(?:\.\d+)?) percent', low)
    if m:
        v = float(m.group(1))
        if any(E[e]['attrs'].get('cross_slope_pct') is not None for e in els):
            attrs['cross_slope_pct'] = v
        else:
            attrs['slope_pct'] = v
    m = re.search(r'1:(\d+) ramp', low)
    if m:
        attrs['slope_pct'] = round(100 / int(m.group(1)), 2)
    m = re.search(r'(\d+) s signal (?:at|on) an? (\d+) m crossing', low)
    if m:
        attrs['green_s'] = int(m.group(1)); attrs['crossing_length_m'] = int(m.group(2)); span = None
    m = re.search(r'unmarked (\d+) m crossing|(\d+) m crossing', low)
    if m and 'crossing_length_m' not in attrs:
        attrs['crossing_length_m'] = int(m.group(1) or m.group(2)); span = None
    m = re.search(r'(\d+) m (?:with )?no bench', low)
    if m:
        attrs['rest_gap_m'] = int(m.group(1)); span = None
    if 'no_rest_200m' in els and attrs.get('rest_gap_m', 0) >= 400:
        els[els.index('no_rest_200m')] = 'no_rest_long_stretch'
    m = re.search(r'(\d+) risers', low)
    if m:
        attrs['vertical_cm'] = int(m.group(1)) * 15
        notes.append(f'{m.group(1)} risers read as {int(m.group(1)) * 15} cm total rise (15 cm per riser, ASSUMPTION)')
    return span


def parse_recipe(raw, item_id, E, bodies_by_h):
    notes, status = [], 'clean'
    parts = [p.strip() for p in raw.split(';')]
    r = {'raw': raw}
    if len(parts) != 6:
        return None, 'flagged', [f'recipe has {len(parts)} fields, expected 6']
    city, what, bh, hhmm, w, li = parts
    if city not in CITIES:
        notes.append(f'city {city!r} unknown, using jaipur'); city = 'jaipur'; status = 'fixed'
    r['city'] = city
    injected = what.lower().startswith('inject')
    what_txt = re.sub(r'^inject\s+', '', what, flags=re.I)
    r['inject_raw'] = what_txt
    pm = re.search(r'\b(?:at|near|on|from)\s+(?:the\s+|a\s+|an\s+|one\s+)?([A-Z][\w\-\' ]+?)(?:,| on route|$| mid-path| entry| corner| lane| approach| frontage| side| inner| outer| crossing| clear strip| edge| arcade| market| underpass| service| bus stop| road)', what_txt)
    r['place_raw'] = pm.group(1).strip() if pm else None
    # elements
    ov = OVERRIDES.get(item_id, {})
    els, attrs, n2 = map_elements(what_txt, E)
    notes += n2
    if ov.get('elements'):
        els = list(ov['elements'])
    if ov.get('attrs'):
        attrs.update(ov['attrs'])
    compare = ov.get('compare', 'inject')
    if not injected and re.search(BODY_COMPARE_WORDS, what_txt.lower()) and compare == 'inject' and not ov.get('confidence') \
            and not re.search(r'ramp|kerb|vendor|signal|bench|encroachment|crossing|detour|upload an off|identical|wrong osm', what_txt.lower()):
        els = []
    span = numbers(what_txt, els, E, attrs, notes) if els else None
    if not els and compare == 'inject':
        if re.search(r'clear', what_txt.lower()) or re.match(r'^\d\d:\d\d', what_txt):
            compare = 'context'
            notes.append('nothing physical to inject: the run compares the trip in neutral conditions (11:00, clear, day) '
                         'with the recipe hour, weather and light')
        else:
            compare = 'body'
            notes.append('no physical element in the recipe: the run compares this body with an adult with no impairment '
                         'on the same trip, same hour and weather')
        if status == 'clean':
            status = 'fixed'
    if not injected and els and not ov.get('elements'):
        notes.append(f'recipe has no "inject" verb; element read from the words: {", ".join(els)}')
        status = 'fixed'
    if ov.get('elements'):
        status = 'fixed'
    r.update(elements=els, attrs=attrs, span_m=span, compare=compare)
    for k in ('confidence', 'observed_at', 'p_attach', 'duplicate', 'base_hour', 'temporary'):
        if k in ov:
            r[k] = ov[k]
    if ov.get('note'):
        notes.append(ov['note'])
    # body
    b = bodies_by_h.get(bh)
    if b is None:
        b = bodies_by_h.get(bh + '*')
        if b:
            notes.append(f'body {bh} resolved to the claude addition {bh}*')
    if b is None:
        notes.append(f'body {bh!r} not in bodies.json, using mw_self'); b = 'mw_self'; status = 'flagged'
    r['body_hermes'], r['body'] = bh, b
    # hour
    m = re.match(r'^(\d{1,2}):(\d{2})$', hhmm)
    if not m:
        notes.append(f'hour {hhmm!r} unreadable, using 11:00'); hhmm = '11:00'; status = 'flagged'; m = re.match(r'(\d+):(\d+)', hhmm)
    r['hhmm'] = f'{int(m.group(1)):02d}:{m.group(2)}'
    r['hour'] = round(int(m.group(1)) + int(m.group(2)) / 60, 2)
    # weather and light
    wl = w.lower()
    if wl not in WEATHER:
        notes.append(f'weather {w!r} unknown, using clear'); status = 'flagged'
    r['weather_raw'], r['weather'] = w, WEATHER.get(wl, 'clear')
    ctx = {'hour': int(m.group(1)), 'weather': r['weather']}
    if wl == 'hot':
        ctx['temp_c'] = 42
        notes.append('"hot" read as 42 C (above the IMD 40 C plains heat-wave line, ASSUMPTION)')
    if wl == 'flood':
        ctx['waterlogged'] = True
    if wl in SEASON:
        ctx['season'] = SEASON[wl]
    ll = li.lower()
    if ll not in LIGHT:
        notes.append(f'light {li!r} unknown, using the hour'); status = 'flagged'
    light = LIGHT.get(ll)
    if ll == 'night' and re.search(r'unlit|low lighting|dark', what_txt.lower()):
        light = 'night_dark'
    if ll == 'hazy':
        ctx['weather'] = r['weather'] = 'haze'
        notes.append('light "hazy" read as weather haze in daylight')
    if light:
        ctx['light'] = light
    r['light_raw'], r['light'], r['context'] = li, light, ctx
    return r, status, notes


VERB_WORD = {'block': 'blocked', 'cost': 'slowed', 'warn': 'warned', 'none': 'barely affected'}


def short_body(name):
    return re.sub(r'\s*\((?:claude addition|baseline[^)]*|legacy[^)]*)\)', '', name)


def enrich(items, B):
    """add a data-backed paragraph from the precomputed run: the asking body's result, then the same thing for
    every body leaf (counts), then named contrasts. Written from numbers, so the answer grows with the engine."""
    if not os.path.isdir(RUNS):
        return
    for iid, it in items.items():
        f = os.path.join(RUNS, f'{iid}.json')
        if not os.path.exists(f):
            continue
        try:
            d = json.load(open(f))
        except Exception as ex:
            it['recipe_notes'].append(f'run file unreadable: {ex}')
            continue
        V = d['variants']
        me = V.get(d['body'], {})
        parts = [d['headline']]
        if d['compare'] in ('inject', 'hour') and d.get('injected'):
            tally = {'block': [], 'cost': [], 'warn': [], 'none': []}
            for b, v in V.items():
                tally.get(v['verdict'], tally['none']).append(b)
            moved = [b for b, v in V.items() if v['changed'] and v['base']['geom'] != v['whatif']['geom']]
            parts.append(f'Same spot, all {len(V)} body leaves: it blocks {len(tally["block"])}, slows {len(tally["cost"])}, '
                         f'is a warning for {len(tally["warn"])} and changes nothing for {len(tally["none"])}; '
                         f'RAASTA re-routes {len(moved)} of them around it.')
            named = []
            for b in d['contrast'][1:]:
                v = V.get(b)
                if not v:
                    continue
                nm = short_body(B[b]['name']).lower()
                if v['whatif']['blocked']:
                    named.append(f'{nm}: no path without a blocking barrier')
                elif v['changed'] and v['base']['geom'] != v['whatif']['geom']:
                    named.append(f'{nm}: {VERB_WORD.get(v["verdict"], "changes")}, re-routed {v["delta_m"]:+.0f} m, {v["delta_min"]:+.1f} min')
                elif v['changed']:
                    named.append(f'{nm}: {VERB_WORD.get(v["verdict"], "changes")}, {v["delta_min"]:+.1f} min on the same path')
                elif v.get('on_route') is False:
                    named.append(f'{nm}: usual route does not pass this spot')
                else:
                    named.append(f'{nm}: no change to route or time')
            if named:
                parts.append('Different bodies, same thing. ' + '; '.join(named) + '.')
            inj = d['injected'][0]
            parts.append('Where: ' + inj['placement_note'] + '.')
        elif d['compare'] == 'body':
            slower = sorted(((v['delta_min'], b) for b, v in V.items() if v['changed']), reverse=True)
            if slower:
                top = ', '.join(f'{short_body(B[b]["name"]).lower()} {dm:+.0f} min' for dm, b in slower[:3])
                parts.append(f'On this trip {len(slower)} of {len(V)} body leaves get a different route or time than an '
                             f'adult with no impairment; the largest changes: {top}.')
        if d.get('trip_note'):
            parts.append(d['trip_note'])
        it['run'] = {'headline': d['headline'], 'detail': ' '.join(parts), 'changed': me.get('changed'),
                     'delta_m': me.get('delta_m'), 'delta_min': me.get('delta_min'), 'verdict': me.get('verdict'),
                     'compare': d['compare']}


def main():
    md = open(SRC, encoding='utf-8').read()
    E = {e['id']: e for e in json.load(open(os.path.join(TAX, 'elements.json')))['elements']}
    Bd = json.load(open(os.path.join(TAX, 'bodies.json')))
    bodies_by_h = {b['hermes_id']: b['id'] for b in Bd['bodies'] if b.get('hermes_id')}
    M = json.load(open(MATRIX))
    rows = parse_rows(md)
    items, seen = {}, set()
    topics = {}
    counts = {'rows': 0, 'recipes_clean': 0, 'recipes_fixed': 0, 'recipes_flagged': 0, 'duplicate_ids': 0}
    for cells in rows:
        iid = cells[0]
        notes = []
        if len(cells) == 8:  # no sub-subtopic column (stage-5 rows T2.4.3, T2.4.4)
            cells = cells[:3] + [cells[2]] + cells[3:]
            notes.append('row had no sub-subtopic cell; the subtopic name is used')
        if len(cells) != 9:
            print(f'[build_whatif] {iid}: {len(cells)} cells, kept with what could be read', file=sys.stderr)
            notes.append(f'row had {len(cells)} cells')
            cells = (cells + [''] * 9)[:9]
        # cells: id, topic, subtopic, subsub, question, answer, part, recipe, hindi
        _, topic, sub, subsub, q, a, part, recipe, hi = cells[:9]
        if iid in seen:
            counts['duplicate_ids'] += 1
            iid = iid + 'b'
            notes.append('duplicate id in the source; suffixed b')
        seen.add(iid)
        rec, status, rnotes = parse_recipe(recipe, iid, E, bodies_by_h)
        if notes and status == 'clean':
            status = 'fixed'
        notes += rnotes
        tid = 'T' + iid[1:].split('.')[0]
        sid = '.'.join(iid.split('.')[:2])
        tp = topics.setdefault(tid, {'id': tid, 'name': topic, 'subtopics': {}})
        st = tp['subtopics'].setdefault(sid, {'id': sid, 'name': sub, 'items': []})
        st['items'].append(iid)
        items[iid] = {'id': iid, 'topic_id': tid, 'topic': topic, 'subtopic_id': sid, 'subtopic': sub, 'subsub': subsub,
                      'q': q, 'q_hi': hi, 'a': a, 'parts': [p.strip() for p in re.split(r'\s\+\s|,', part) if p.strip()],
                      'recipe': rec, 'recipe_status': status, 'recipe_notes': notes}
        counts['rows'] += 1
        counts['recipes_' + status] += 1
    tl = []
    for tid in sorted(topics, key=lambda t: int(t[1:])):
        tp = topics[tid]
        subs = []
        for sid in sorted(tp['subtopics'], key=lambda s: tuple(int(x) for x in s[1:].split('.'))):
            st = tp['subtopics'][sid]
            st['items'].sort(key=id_key)
            subs.append(st)
        tl.append({'id': tid, 'name': tp['name'], 'subtopics': subs})
    counts['topics'] = len(tl)
    counts['subtopics'] = sum(len(t['subtopics']) for t in tl)
    enrich(items, {b['id']: b for b in Bd['bodies']})
    counts['runs'] = sum(1 for it in items.values() if it.get('run'))
    used = sorted({e for it in items.values() if it['recipe'] for e in it['recipe']['elements']})
    elements = {}
    for e in used:
        x = E[e]
        dc = x.get('detector_class')
        elements[e] = {'name': x['name'], 'category': x['category'], 'subcategory': x['subcategory'],
                       'glyph': dc if dc in ICON_TYPES else x['category']}
    binfo = {b['id']: {'name': b['name'], 'hermes_id': b.get('hermes_id'), 'scorer': b['scorer'], 'path': b['path']}
             for b in Bd['bodies']}
    out = {'schema': 'raasta-whatif-tree-v2', 'generated_at': dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).isoformat(timespec='seconds'),
           'source': 'research/hermes/sc02/WHATIF-TREE.md (hermes); parsed by app/site/tools/build_whatif.py',
           'counts': counts, 'topics': tl, 'items': dict(sorted(items.items(), key=lambda kv: id_key(kv[0].rstrip('b')))),
           'bodies': {'tree': M['body_tree'], 'info': binfo}, 'elements': elements}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(json.dumps(counts))
    for it in out['items'].values():
        if it['recipe_status'] == 'flagged':
            print('FLAGGED', it['id'], '|', it['recipe']['raw'] if it['recipe'] else '', '|', '; '.join(it['recipe_notes']))


if __name__ == '__main__':
    main()
