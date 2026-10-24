"""MOCK city data for the site frame (not real evidence). writes ../site-data/mock/ in the schema the routing and
/analyze lanes are asked to produce, so the site can be built before real data lands. every record says mock: true.

run: python3 -I tools/make_mock.py   (from app/site)
"""
import json, math, os, pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / 'site-data' / 'mock'
OUT.mkdir(parents=True, exist_ok=True)
LAT0, LON0 = 26.8418, 75.5628          # near a campus in Jaipur; the grid itself is invented
DLAT, DLON = 0.00135, 0.0016            # about 150 m x 160 m blocks
OFF = 0.00006                           # sidewalk offset from the road centre line (~6 m)
ROWS, COLS = 4, 5

def node(i, j): return (LON0 + j * DLON, LAT0 + i * DLAT)
def dist(a, b):
    dx = (a[0] - b[0]) * 111320 * math.cos(math.radians(LAT0)); dy = (a[1] - b[1]) * 110540
    return math.hypot(dx, dy)
def r6(p): return [round(p[0], 6), round(p[1], 6)]

edges, eid = [], 0
def add_edge(a, b, source, road, side):
    global eid
    eid += 1
    edges.append({'id': f'e{eid}', 'a': a, 'b': b, 'source': source, 'road': road, 'side': side})
    return f'e{eid}'

# sidewalks both sides of every road block (generated: the mock pretends OSM has no footway here)
idx = {}
for i in range(ROWS):
    for j in range(COLS - 1):
        a, b = node(i, j), node(i, j + 1)
        for side, s in (('north', 1), ('south', -1)):
            idx[('h', i, j, side)] = add_edge((a[0], a[1] + s * OFF), (b[0], b[1] + s * OFF), 'osm' if (i == 0 and side == 'north') else 'generated', f'Row {i + 1} Road', side)
for j in range(COLS):
    for i in range(ROWS - 1):
        a, b = node(i, j), node(i + 1, j)
        for side, s in (('east', 1), ('west', -1)):
            idx[('v', i, j, side)] = add_edge((a[0] + s * OFF, a[1]), (b[0] + s * OFF, b[1]), 'osm' if (j == 0 and side == 'west') else 'generated', f'Lane {j + 1}', side)
emap = {e['id']: e for e in edges}

def along(e, p): a, b = e['a'], e['b']; return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)

TYPES = ['missing_ramp', 'steps', 'broken_footpath', 'pole', 'parked_vehicle']
barrier_specs = [
    (('h', 0, 1, 'south'), 0.5, 'pole', 'ACCEPT', 0.91, None, '2026-09-28'),
    (('h', 1, 1, 'north'), 0.35, 'parked_vehicle', 'ACCEPT', 0.84, None, '2026-10-21'),
    (('v', 1, 2, 'east'), 0.6, 'steps', 'ACCEPT', 0.88, (17, 3), '2026-10-02'),
    (('h', 2, 2, 'south'), 0.2, 'broken_footpath', 'ABSTAIN', 0.52, None, '2026-08-14'),
    (('v', 2, 3, 'west'), 0.95, 'missing_ramp', 'ACCEPT', 0.79, (19, 4), '2026-10-11'),
    (('h', 3, 3, 'north'), 0.5, 'parked_vehicle', 'REJECT', 0.31, None, '2026-10-19'),
    (('v', 0, 1, 'east'), 0.4, 'missing_ramp', 'ABSTAIN', 0.58, (14, 9), '2026-09-03'),
    (('h', 1, 3, 'south'), 0.7, 'pole', 'ACCEPT', 0.87, None, '2026-10-15'),
]
barriers = []
for n, (k, p, typ, status, conf, h, date) in enumerate(barrier_specs, 1):
    e = emap[idx[k]]
    barriers.append({'kind': 'barrier', 'id': f'b{n}', 'type': typ, 'status': status, 'confidence': conf,
        'segment_id': e['id'], 'segment_p': round(0.6 + 0.35 * conf, 2), 'segment_alternatives': [{'segment_id': e['id'], 'p': round(0.6 + 0.35 * conf, 2)}, {'segment_id': 'opposite side', 'p': round(0.4 - 0.35 * conf, 2)}],
        'height_cm': h[0] if h else None, 'height_err_cm': h[1] if h else None, 'observed': date,
        'photo': {'url': f'/placeholder/{typ}.svg', 'crop': [0.18, 0.2, 0.62, 0.6], 'credit': 'PLACEHOLDER drawing', 'license': 'ours'},
        'source_url': 'https://example.org/mock-source', 'detectors': {'a': {'label': typ, 'score': conf}, 'b': {'label': typ if status != 'REJECT' else 'none', 'score': round(conf - 0.08, 2)}},
        'mock': True, '_xy': along(e, p)})
clear_specs = [(('h', 0, 0, 'north'), '2026-10-20'), (('h', 0, 2, 'north'), '2026-10-20'), (('v', 0, 0, 'west'), '2026-10-18'),
               (('v', 1, 0, 'west'), '2026-10-18'), (('h', 3, 0, 'south'), '2026-07-30'), (('v', 2, 4, 'west'), '2026-10-09'),
               (('h', 2, 0, 'north'), '2026-10-12'), (('h', 2, 1, 'north'), '2026-10-12'), (('v', 2, 1, 'east'), '2026-10-12')]
clears = []
for n, (k, date) in enumerate(clear_specs, 1):
    e = emap[idx[k]]
    clears.append({'kind': 'clear', 'id': f'c{n}', 'segment_id': e['id'], 'observed': date, 'photo': {'url': '/placeholder/clear.svg', 'crop': [0, 0, 1, 1]}, 'source_url': 'https://example.org/mock-source', 'mock': True, '_xy': along(e, 0.5)})

ev = {}
for c in clears: ev[c['segment_id']] = ('clear', c['observed'])
for b in barriers:
    if b['status'] == 'ACCEPT': ev[b['segment_id']] = ('barrier', b['observed'])
    elif b['segment_id'] not in ev: ev[b['segment_id']] = ('unknown', None)

features = []
for e in edges:
    state, date = ev.get(e['id'], ('unknown', None))
    features.append({'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [r6(e['a']), r6(e['b'])]},
        'properties': {'kind': 'edge', 'id': e['id'], 'source': e['source'], 'highway': 'footway' if e['source'] == 'osm' else 'sidewalk',
            'side': e['side'], 'road_name': e['road'], 'length_m': round(dist(e['a'], e['b']), 1), 'evidence': state, 'observed': date,
            'barrier_ids': [b['id'] for b in barriers if b['segment_id'] == e['id']], 'mock': True}})
for x in barriers + clears:
    xy = x.pop('_xy')
    features.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': r6(xy)}, 'properties': x})
net = {'type': 'FeatureCollection', 'properties': {'city': 'mock', 'schema': 'hypnexis-network-v1', 'mock': True, 'generated_by': 'app/site/tools/make_mock.py'}, 'features': features}
(OUT / 'network.geojson').write_text(json.dumps(net, ensure_ascii=False))

# routes: A (row 0, col 0) to B (row 3, col 4) along sidewalks
def path_of(keys, rev=()):
    pts = []
    for k in keys:
        e = emap[idx[k]]; a, b = (e['b'], e['a']) if k in rev else (e['a'], e['b'])
        if not pts: pts.append(r6(a))
        pts.append(r6(b))
    return pts
def length(pts): return round(sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)), 1)
short_keys = [('h', 0, 0, 'south'), ('h', 0, 1, 'south'), ('v', 0, 2, 'east'), ('v', 1, 2, 'east'), ('h', 2, 2, 'south'), ('h', 2, 3, 'south'), ('v', 2, 4, 'west')]
acc_day = [('h', 0, 0, 'north'), ('h', 0, 1, 'north'), ('h', 0, 2, 'north'), ('h', 0, 3, 'north'), ('v', 0, 4, 'west'), ('v', 1, 4, 'west'), ('v', 2, 4, 'west')]
acc_eve = [('v', 0, 0, 'west'), ('v', 1, 0, 'west'), ('h', 2, 0, 'north'), ('h', 2, 1, 'north'), ('v', 2, 2, 'east'), ('h', 3, 2, 'north'), ('h', 3, 3, 'south')]
acc_walker = [('h', 0, 0, 'north'), ('h', 0, 1, 'north'), ('h', 0, 2, 'north'), ('v', 0, 3, 'west'), ('v', 1, 3, 'west'), ('h', 2, 3, 'north'), ('v', 2, 4, 'west')]
profiles = [
    {'id': 'manual_wheelchair', 'label': {'en': 'manual wheelchair', 'hi': 'व्हीलचेयर'}, 'speed_mps': 0.9},
    {'id': 'walker_elderly', 'label': {'en': 'walker', 'hi': 'वॉकर'}, 'speed_mps': 0.6},
    {'id': 'pram', 'label': {'en': 'pram', 'hi': 'बच्चा गाड़ी'}, 'speed_mps': 1.0},
    {'id': 'crutches', 'label': {'en': 'crutches', 'hi': 'बैसाखी'}, 'speed_mps': 0.7},
    {'id': 'low_vision', 'label': {'en': 'low vision', 'hi': 'कम दृष्टि'}, 'speed_mps': 0.8},
]
def seg_barriers(keys, statuses=('ACCEPT',)):
    ids = {idx[k] for k in keys}
    return [b['id'] for b in barriers if b['segment_id'] in ids and b['status'] in statuses]
routes = []
sp = path_of(short_keys)
routes.append({'id': 'r-short', 'kind': 'shortest', 'profile': 'any', 'depart_hours': [0, 24], 'path': sp, 'length_m': length(sp),
    'barriers_hit': seg_barriers(short_keys, ('ACCEPT', 'ABSTAIN')), 'summary': {'en': 'Shortest: {len} m. It crosses {n} known or unsure barriers.', 'hi': 'सबसे छोटा: {len} मीटर. इसमें {n} पक्की या संदिग्ध रुकावटें हैं.'}, 'mock': True})
for prof in profiles:
    for keys, hours, tag in ((acc_day, [6, 17], 'day'), (acc_eve, [17, 24], 'evening'), (acc_eve, [0, 6], 'night')):
        if prof['id'] in ('walker_elderly', 'crutches') and tag == 'day': keys = acc_walker
        p = path_of(keys)
        routes.append({'id': f'r-{prof["id"]}-{tag}', 'kind': 'accessible', 'profile': prof['id'], 'depart_hours': hours, 'path': p, 'length_m': length(p),
            'barriers_hit': seg_barriers(keys), 'barriers_avoided': seg_barriers(short_keys, ('ACCEPT', 'ABSTAIN')),
            'unknown_m': round(length(p) * (0.35 if tag != 'day' else 0.2)),
            'summary': {'en': 'For a {profile} leaving at {time}: {len} m, {extra} m longer, no known barrier. {unknown} m of it has no photo yet.',
                        'hi': '{time} पर निकलने वाले {profile} के लिए: {len} मीटर, {extra} मीटर ज़्यादा, कोई पक्की रुकावट नहीं. {unknown} मीटर की अभी कोई फ़ोटो नहीं.'},
            'assumptions': ['evening: parked vehicles on Row 2 north side (assumed from shop hours, not observed)'] if tag != 'day' else [], 'mock': True})
(OUT / 'routes.json').write_text(json.dumps({'city': 'mock', 'schema': 'hypnexis-routes-v1', 'mock': True, 'from': {'label': 'gate', 'lnglat': sp[0]}, 'to': {'label': 'chemist', 'lnglat': sp[-1]}, 'profiles': profiles, 'routes': routes}, ensure_ascii=False, indent=1))

# precomputed /analyze answers (scan page offline fallback)
rec = []
for b in barriers[:5]:
    rec.append({'id': f'rx-{b["id"]}', 'mock': True, 'image': {'url': b['photo']['url'], 'w': 1200, 'h': 800},
        'boxes': [{'x': 0.24, 'y': 0.22, 'w': 0.5, 'h': 0.56, 'label': b['type'], 'score': b['confidence'], 'status': b['status']}],
        'status': b['status'], 'abstain_reason': 'the two detectors disagree' if b['status'] == 'ABSTAIN' else None,
        'barrier': {k: v for k, v in b.items() if k not in ('kind',)},
        'height': {'value_cm': b['height_cm'], 'err_cm': b['height_err_cm'], 'routes': [{'method': 'shadow', 'cm': b['height_cm'] + 1 if b['height_cm'] else None}, {'method': 'camera geometry', 'cm': b['height_cm'] - 1 if b['height_cm'] else None}, {'method': 'metric depth', 'cm': b['height_cm']}]} if b['height_cm'] else None,
        'place': {'segment_id': b['segment_id'], 'p': b['segment_p'], 'candidates': b['segment_alternatives']},
        'pipeline': {'detector_a': 'open-vocab detector (mock)', 'detector_b': 'second detector (mock)', 'judge': 'VLM judge (mock)'}})
(OUT / 'receipts.json').write_text(json.dumps({'schema': 'hypnexis-receipts-v1', 'mock': True, 'receipts': rec}, ensure_ascii=False, indent=1))
(OUT / 'city.json').write_text(json.dumps({'name': 'MOCK grid (invented data)', 'mock': True, 'center': [LON0 + 2 * DLON, LAT0 + 1.5 * DLAT], 'zoom': 16.2}))
(OUT / 'ledger.json').write_text(json.dumps({'mock': True, 'entries': [
    {'barrier_id': 'b1', 'segment_id': barriers[0]['segment_id'], 'complaint': '2026-09-29', 'fixed': None, 'to': 'municipal ward office (mock)'},
    {'barrier_id': 'b3', 'segment_id': barriers[2]['segment_id'], 'complaint': '2026-10-03', 'fixed': None, 'to': 'municipal ward office (mock)'},
    {'barrier_id': 'b5', 'segment_id': barriers[4]['segment_id'], 'complaint': '2026-08-20', 'fixed': '2026-10-11', 'to': 'PWD (mock)'},
    {'barrier_id': 'b8', 'segment_id': barriers[7]['segment_id'], 'complaint': '2026-10-16', 'fixed': None, 'to': 'electricity board (mock)'}]}, indent=1))
(OUT / 'trips.json').write_text(json.dumps({'mock': True, 'unit': 'trips per day not taken on this grid',
    'assumption': 'MOCK: residents x share with a mobility need x trips per day x share of trips that hit a known barrier and are dropped; every factor is a placeholder until the content lane sources it',
    'factors': [{'name': 'residents in the grid', 'low': 4000, 'high': 6000}, {'name': 'share with a walking disability or using a walker (placeholder)', 'low': 0.02, 'high': 0.04}, {'name': 'trips per person per day', 'low': 2, 'high': 2.5}, {'name': 'share of those trips dropped (placeholder)', 'low': 0.5, 'high': 0.6}]}, indent=1))
print('wrote', OUT, len(edges), 'edges', len(barriers), 'barriers', len(clears), 'clear', len(routes), 'routes')
