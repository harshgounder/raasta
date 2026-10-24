"""Precompute one map run per what-if question (RAASTA /what-if v2).

  cd app/route; .venv/bin/python tools/precompute_whatif.py            # all items
  cd app/route; .venv/bin/python tools/precompute_whatif.py T1.1.1 T9.1.1

Reads  app/site/public/content/whatif-tree.json   (built by app/site/tools/build_whatif.py)
Writes app/site-data/whatif/<id>.json + index.json (schema in app/site/WHATIF-V2-BUILD.md)

For every recipe: pick the trip (a demo scenario from hroute.cli.AREAS, or a trip along the named OSM road),
route it with the impact engine (hroute.impact_adapter.route_with_engine) for EVERY body leaf, once without and
once with the injected element(s) placed as what-if records on a real segment of the recipe body's route, and
store both geometries, metres, minutes, the engine's reason text, and the element verdict per body.
Records carry source "what_if" and are removed again after the run; the cached networks are never saved.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTE = os.path.dirname(HERE)
sys.path.insert(0, ROUTE)

from hroute import impact as I  # noqa: E402
from hroute import impact_adapter as IA  # noqa: E402
from hroute.cli import AREAS  # noqa: E402
from hroute.config import CACHE, SITE_DATA  # noqa: E402
from hroute.network import FootNetwork  # noqa: E402

PROJECT = os.path.dirname(os.path.dirname(ROUTE))
TREE = os.path.join(PROJECT, 'app', 'site', 'public', 'content', 'whatif-tree.json')
OUT = os.path.join(SITE_DATA, 'whatif')

DEFAULT_SCEN = {'jaipur': 'hawa-johari', 'chandigarh': 's17-museum', 'varanasi': 'godowlia-dashashwamedh',
                'jaipur-photos': 'tirpoliya-sjs-circle'}
# landmarks: the Nominatim points already recorded in hroute/cli.py AREAS (checked 2026-10-24), each the start or
# end of a demo trip. (city, lowercase key) -> (scenario id, 'start' | 'end')
LANDMARKS = {
    ('jaipur', 'hawa mahal'): ('hawa-johari', 'start'),
    ('jaipur', 'city palace'): ('palace-hawa', 'start'),
    ('chandigarh', 'sector 17'): ('s17-museum', 'start'),
    ('chandigarh', 'sector 10'): ('s10-labelled', 'mid'),
    ('varanasi', 'godowlia'): ('godowlia-dashashwamedh', 'start'),
    ('varanasi', 'dashashwamedh'): ('godowlia-dashashwamedh', 'end'),
    ('varanasi', 'kashi vishwanath'): ('vishwanath-manikarnika', 'start'),
    ('varanasi', 'manikarnika'): ('vishwanath-manikarnika', 'end'),
}
# spoken place name -> the OSM road name in the built network (checked by listing net.roads names, 2026-10-25)
ROADS = {
    ('jaipur', 'johari bazar'): 'Johari Bazar', ('jaipur', 'badi chaupar'): 'Badi Chaupar',
    ('jaipur', 'chandpole'): 'Chandpol Bazaar', ('jaipur', 'mi road'): 'Mirza Ismail Road',
    ('jaipur', 'tripolia'): 'Tripolia Bazaar',
}
CONTRAST = ['mw_self', 'blind_cane', 'older_80_frail', 'pram_stroller', 'crutches_bilateral', 'no_impairment_adult',
            'cardiac']
SPAN_CATS = {'surface', 'weather', 'light_time', 'air_noise', 'crowd_safety', 'terrain_transit', 'temporary_obstacles'}
WALK = ('sidewalk', 'footway', 'shared_street')
VERB = {'block': 'blocks the way for', 'cost': 'slows the trip for', 'warn': 'is a warning for',
        'none': 'does not change the trip for', 'minor': 'barely slows the trip for'}
_NETS = {}


def net_for(city):
    if city not in _NETS:
        _NETS[city] = FootNetwork.load(os.path.join(CACHE, 'networks', f'{city}.pkl'))
    return _NETS[city]


def road_name(net, seg):
    pr = seg.get('parent_road')
    if isinstance(pr, dict):
        return pr.get('name') or ''
    if pr is not None and hasattr(net, 'roads'):
        return (net.roads.get(pr) or {}).get('name') or ''
    return ''


def scen(city, sid):
    for s in AREAS[city]['scenarios']:
        if s['id'] == sid:
            return s
    return AREAS[city]['scenarios'][0]


def pick_route(res):
    return res.get('accessible') or res.get('least_blocked') or res.get('shortest') or {}


def leave_iso(h):
    hh, mm = int(h), int(round((h - int(h)) * 60))
    return f'2026-10-25T{hh:02d}:{mm:02d}:00+05:30'


def road_trip(net, name, half=300.0):
    """start/end about `half` m either side of the middle of the named road's footpaths, along the road."""
    pts = []
    for s in net.segments.values():
        if s['kind'] in WALK and road_name(net, s) == name:
            pts += list(s['geom'].coords)
    if len(pts) < 4:
        return None
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    syy = sum((p[1] - my) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ux, uy = math.cos(ang), math.sin(ang)
    proj = sorted(((p[0] - mx) * ux + (p[1] - my) * uy, p) for p in pts)
    lo, hi = proj[0][0], proj[-1][0]
    mid = (lo + hi) / 2
    a, b = max(lo, mid - half), min(hi, mid + half)
    pa = min(proj, key=lambda t: abs(t[0] - a))[1]
    pb = min(proj, key=lambda t: abs(t[0] - b))[1]
    la = net.to_lonlat(*pa)
    lb = net.to_lonlat(*pb)
    return (la[1], la[0]), (lb[1], lb[0]), round(b - a)


def resolve_place(city, place, net):
    """-> (kind, value, note). kind: road | landmark | none"""
    if not place:
        return 'none', None, 'the recipe names no place'
    p = place.lower().strip()
    for (c, k), v in ROADS.items():
        if c == city and k in p:
            return 'road', v, f'"{place}" is the OSM road "{v}"'
    for (c, k), v in LANDMARKS.items():
        if c == city and k in p:
            return 'landmark', v, f'"{place}" is the {v[1]} point of the demo trip "{scen(city, v[0])["name"]}" (Nominatim point)'
    names = {road_name(net, s) for s in net.segments.values()}
    for n in names:
        if n and (n.lower() in p or p in n.lower()):
            return 'road', n, f'"{place}" matched the OSM road "{n}"'
    return 'none', None, f'"{place}" is not an OSM name in the {city} network built for this demo'


def seg_point(net, sid, at=None):
    g = net.segments[sid]['geom']
    at = g.length / 2 if at is None else max(0.0, min(g.length, at))
    m = g.interpolate(at)
    lon, lat = net.to_lonlat(m.x, m.y)
    return round(lon, 6), round(lat, 6), round(at, 1)


ICONS = {'pole_obstruction', 'parked_vehicle', 'broken_footpath', 'missing_kerb_ramp', 'steps', 'pothole', 'vendor',
         'missing_footpath', 'open_drain', 'waterlogging', 'steep_slope', 'crossing_marked'}


def short_reason(r):
    if not r:
        return None
    r = r.split(' Presence ')[0].replace('BLOCK: BLOCK: ', 'BLOCK: ')
    return r


def choose_anchor(net, ids, els, kind, value, E, cover=None):
    """placement: the named road / landmark / middle of the recipe body's route; among the candidates there,
    the segment that the most body leaves' baseline routes pass (so 'same thing, different bodies' compares
    bodies that actually meet it)."""
    cover = cover or {}
    crossing_like = any(E[e]['category'] == 'traffic_crossings' or E[e]['subcategory'] == 'kerbs' for e in els)
    inner = ids[1:-1] if len(ids) > 2 else ids
    pref = [i for i in inner if net.segments[i]['kind'] == ('crossing' if crossing_like else 'sidewalk')]
    if not pref:
        pref = [i for i in inner if net.segments[i]['kind'] in (('crossing',) if crossing_like else WALK)]
    if not pref:
        pref = [i for i in inner if net.segments[i]['kind'] != 'median'] or inner
    def best(cands, near=None):
        # most bodies first, then closest to the wanted point (distance in metres, projected CRS)
        if near is None:
            return max(cands, key=lambda i: cover.get(i, 0))
        return max(cands, key=lambda i: (cover.get(i, 0), -net.segments[i]['geom'].distance(near)))

    if kind == 'road':
        on = [i for i in pref if road_name(net, net.segments[i]) == value]
        if not on and crossing_like:
            # a crossing next to the named road: crossings within 40 m of that road's route segments
            road_ids = [i for i in inner if road_name(net, net.segments[i]) == value]
            on = [i for i in pref if any(net.segments[i]['geom'].distance(net.segments[r]['geom']) < 40 for r in road_ids)]
        if on:
            return best(on), 'osm_road'
    from shapely.geometry import Point
    if kind == 'landmark' and value is not None:
        P = Point(*value)
        near = [i for i in pref if 15 < net.segments[i]['geom'].distance(P) < 150]
        if near:
            return best(near, P), 'landmark'
        far = [i for i in pref if net.segments[i]['geom'].distance(P) > 15] or pref
        return min(far, key=lambda i: net.segments[i]['geom'].distance(P)), 'landmark'
    # the middle half of the route by length
    tot = sum(net.segments[i]['length_m'] for i in ids)
    acc, midset = 0.0, []
    for i in ids:
        if tot * 0.25 <= acc <= tot * 0.75:
            midset.append(i)
        acc += net.segments[i]['length_m']
    cands = [i for i in pref if i in midset] or pref
    c = None
    if midset:
        c = net.segments[midset[len(midset) // 2]]['geom'].interpolate(0.5, normalized=True)
    return best(cands, c), 'route'


def span_ids(net, ids, anchor, span):
    if not span:
        return [anchor]
    k = ids.index(anchor)
    out, acc = [], 0.0
    for i in ids[k:]:
        if net.segments[i]['kind'] == 'median':
            continue
        out.append(i)
        acc += net.segments[i]['length_m']
        if acc >= min(span, 400.0) or len(out) >= 12:
            break
    return out


def make_records(net, item, els, seg_list, rec, E, leave):
    recs = []
    attrs = {k: v for k, v in (rec.get('attrs') or {}).items() if v is not None}
    for si, sid in enumerate(seg_list):
        L = net.segments[sid]['length_m']
        for ei, e in enumerate(els):
            at = min(L, L / 2 + 2.0 * ei)  # co-located within the 10 m co-presence radius
            lon, lat, at = seg_point(net, sid, at)
            r = {'id': f'wi-{item}-{e}-{si}', 'type': E[e].get('detector_class') or e, 'element': e,
                 'source': 'what_if', 'status': 'ACCEPT', 'confidence': rec.get('confidence', 0.9),
                 'observed_at': rec.get('observed_at', leave[:10]) if 'observed_at' in rec else leave[:10],
                 'permanence': 'temporary' if rec.get('temporary') else 'permanent', 'p_attach': rec.get('p_attach', 1.0), 'at_m': at, 'lat': lat, 'lon': lon,
                 'label': f'WHAT-IF {item}: {E[e]["name"]} (placed to demonstrate, not observed)', 'attrs': attrs}
            if rec.get('temporary'):  # seen at 19:00 the evening before: costs.p_present applies half-life, recurrence, hour curve
                r.update(observed_at='2026-10-24T19:00:00+05:30', confidence=0.95)
            if attrs.get('vertical_cm') is not None:
                r['height_cm'] = attrs['vertical_cm']
            if attrs.get('clear_width_cm') is not None:
                r['clear_width_cm'] = attrs['clear_width_cm']
            if attrs.get('slope_pct') is not None:
                r['slope_pct'] = attrs['slope_pct']
            recs.append((sid, r))
            if rec.get('duplicate') and si == 0:
                r2 = dict(r, id=r['id'] + '-dup', at_m=round(min(L, at + 3.0), 1))
                recs.append((sid, r2))
    return recs


def put(net, recs):
    for sid, r in recs:
        net.segments[sid]['evidence'].append(r)


def take(net, recs):
    ids = {r['id'] for _, r in recs}
    for sid, _ in recs:
        net.segments[sid]['evidence'] = [e for e in net.segments[sid]['evidence'] if e.get('id') not in ids]


class Geoms:
    def __init__(self):
        self.by_hash, self.store = {}, {}

    def add(self, geom):
        coords = [[round(x, 6), round(y, 6)] for x, y in (geom or {}).get('coordinates', [])]
        if not coords:
            return None
        h = hashlib.md5(json.dumps(coords).encode()).hexdigest()
        if h not in self.by_hash:
            gid = f'g{len(self.by_hash)}'
            self.by_hash[h] = gid
            self.store[gid] = coords
        return self.by_hash[h]


def slim(res, geoms, full):
    r = pick_route(res)
    out = {'geom': geoms.add(r.get('geometry')), 'length_m': round(r.get('length_m') or 0, 1),
           'minutes': r.get('minutes'), 'status': res.get('status'),
           'blocked': res.get('status') == 'blocked_for_profile', 'kind': r.get('kind')}
    if full:
        out['summary'] = res.get('summary')
    return out


def whatif_hits(res):
    r = pick_route(res)
    seen, out = set(), []
    for h in (r.get('barriers') or []) + (r.get('blocking') or []):
        if str(h.get('evidence_id') or '').startswith('wi-') and h.get('element') not in seen:
            seen.add(h.get('element'))
            out.append({'element': h.get('element'), 'verdict': h.get('verdict', 'block' if h.get('blocking') else None),
                        'blocking': bool(h.get('blocking')), 'why': h.get('why')})
    return out


def element_verdicts(els, rec, ctx, body):
    out = []
    attrs = {k: v for k, v in (rec.get('attrs') or {}).items() if v is not None}
    for e in els:
        c = dict(ctx)
        c['co_present'] = [x for x in els if x != e]
        try:
            v = I.impact({'id': e, 'attrs': attrs, 'confidence': rec.get('confidence', 0.9) * rec.get('p_attach', 1.0)},
                         c, body)
            out.append({'element': e, 'verdict': v['verdict'], 'seconds': v['seconds'], 'risk': v['risk'],
                        'reason': v['reason'], 'compound': v.get('compound')})
        except Exception as ex:  # never drop a body silently: the error text is stored
            out.append({'element': e, 'verdict': 'none', 'seconds': 0, 'risk': 0, 'reason': f'engine error {ex}'})
    return out


def run_item(item):
    iid = item['id']
    rec = item['recipe']
    E = I.data()['elements']
    city = rec['city']
    net = net_for(city)
    body = rec['body']
    els = rec['elements']
    compare = rec.get('compare', 'inject')
    ctx = dict(rec['context'])
    leave = leave_iso(rec['hour'])
    kind, value, pnote = resolve_place(city, rec.get('place_raw'), net)
    # trip
    trip_note = ''
    if kind == 'landmark':
        sc = scen(city, value[0])
        if value[1] in ('start', 'end'):
            p = sc[value[1]]
            x, y = net.to_xy(p['lat'], p['lon'])
            value = (x, y)
        else:
            value = None
    else:
        sc = scen(city, DEFAULT_SCEN[city])
    start, end = (sc['start']['lat'], sc['start']['lon']), (sc['end']['lat'], sc['end']['lon'])
    scenario = {'id': sc['id'], 'name': sc['name'], 'start': sc['start'], 'end': sc['end']}
    base_ctx, base_leave, base_body_fixed = ctx, leave, None
    if compare == 'context':
        base_ctx, base_leave = {'hour': 11, 'weather': 'clear', 'light': 'day'}, leave_iso(11)
    elif compare == 'hour':
        bh = rec.get('base_hour', 9.0)
        base_ctx, base_leave = {**ctx, 'hour': int(bh), 'light': 'day'}, leave_iso(bh)
    elif compare == 'body':
        base_body_fixed = 'no_impairment_adult'
    base_res = IA.route_with_engine(net, start, end, body, leave, engine='impact', context=ctx)
    if kind == 'road':
        ids0 = pick_route(base_res).get('segment_ids') or []
        if not any(road_name(net, net.segments[i]) == value for i in ids0):
            rt = road_trip(net, value)
            if rt:
                start, end, extent = rt
                scenario = {'id': f'along-{value.lower().replace(" ", "-")}', 'name': f'Along {value} (OSM road)',
                            'start': {'lat': round(start[0], 6), 'lon': round(start[1], 6), 'label': f'{value}, one end'},
                            'end': {'lat': round(end[0], 6), 'lon': round(end[1], 6), 'label': f'{value}, other end'}}
                trip_note = (f'The demo trips do not use {value}, so this run walks along {value} itself '
                             f'(about {extent} m between two points on the road).')
                base_res = IA.route_with_engine(net, start, end, body, leave, engine='impact', context=ctx)
    ids = pick_route(base_res).get('segment_ids') or []
    bodies = [b['id'] for b in I.data()['body_list']]
    contrast = [body] + [b for b in CONTRAST if b != body][:5]
    # baselines first (no what-if records), so the placement can pick the spot most bodies' routes share
    base = {}
    for b in bodies:
        if compare == 'body':
            if 'adult' not in base:
                base['adult'] = IA.route_with_engine(net, start, end, base_body_fixed, leave, engine='impact', context=ctx)
            base[b] = base['adult']
        elif compare != 'hour':
            base[b] = IA.route_with_engine(net, start, end, b, base_leave, engine='impact', context=base_ctx)
    base.pop('adult', None)
    cover = {}
    for b, r in base.items():
        for i in set(pick_route(r).get('segment_ids') or []):
            cover[i] = cover.get(i, 0) + 1
    injected, recs, span_pts = [], [], []
    if els and ids:
        anchor, how = choose_anchor(net, ids, els, kind if kind != 'none' else None, value, E, cover)
        span = rec.get('span_m') if any(E[e]['category'] in SPAN_CATS for e in els) else None
        seg_list = span_ids(net, ids, anchor, span)
        recs = make_records(net, iid, els, seg_list, rec, E, leave)
        seg = net.segments[anchor]
        rn = road_name(net, seg)
        along = 0.0
        for i in ids:
            if i == anchor:
                break
            along += net.segments[i]['length_m']
        if how == 'osm_road':
            note = f'{pnote}; placed on a {seg["kind"]} segment of {rn}'
        elif how == 'landmark':
            note = f'{pnote}; placed on the nearest {seg["kind"]} segment of the route to it' + (f' (on {rn})' if rn else '')
        else:
            note = (f'{pnote}, so it is placed on the baseline route of "{scenario["name"]}", '
                    f'{along:.0f} m from the start, on a {seg["kind"]} segment' + (f' of {rn}' if rn else ''))
        if span and len(seg_list) > 1:
            note += f'; repeated on {len(seg_list)} route segments to cover about {rec.get("span_m"):.0f} m'
        if compare != 'hour':
            note += f'. {cover.get(anchor, 0)} of {len(bodies)} body leaves pass this spot on their usual route'
        lon, lat, at = seg_point(net, anchor)
        for e in els:
            x = E[e]
            injected.append({'element': e, 'name': x['name'], 'category': x['category'],
                             'glyph': x.get('detector_class') if x.get('detector_class') in ICONS else x['category'],
                             'segment_id': anchor, 'segments': seg_list, 'lon': lon, 'lat': lat, 'road': rn or None,
                             'segment_kind': seg['kind'], 'placement': how, 'placement_note': note,
                             'attrs': rec.get('attrs') or {}, 'confidence': rec.get('confidence', 0.9),
                             'p_attach': rec.get('p_attach', 1.0), 'temporary': bool(rec.get('temporary'))})
        span_pts = [list(seg_point(net, s_)[:2]) for s_ in seg_list]
    if compare == 'hour':  # the same records at both hours: only the hour changes
        put(net, recs)
        try:
            for b in bodies:
                base[b] = IA.route_with_engine(net, start, end, b, base_leave, engine='impact', context=base_ctx)
        finally:
            take(net, recs)
    geoms = Geoms()
    variants = {}
    anchor_id = injected[0]['segment_id'] if injected else None
    try:
        for b in bodies:
            full = b in contrast
            rb = base[b]
            put(net, recs)
            try:
                rw = IA.route_with_engine(net, start, end, b, leave, engine='impact', context=ctx)
            finally:
                take(net, recs)
            vb, vw = slim(rb, geoms, full), slim(rw, geoms, full)
            vw['hits'] = whatif_hits(rw)
            ev = element_verdicts(els, rec, ctx, b) if els else []
            dm = round(vw['length_m'] - vb['length_m'], 1)
            dmin = round((vw['minutes'] or 0) - (vb['minutes'] or 0), 1)
            changed = vb['geom'] != vw['geom'] or vb['blocked'] != vw['blocked'] or abs(dmin) >= 0.1
            worst = max(ev, key=lambda x: (I.RANK[x['verdict']], x['risk'])) if ev else None
            on_route = anchor_id in (pick_route(rb).get('segment_ids') or []) if anchor_id else None
            reason = vw['hits'][0]['why'] if vw['hits'] else (worst['reason'] if worst else None)
            v = {'base': vb, 'whatif': vw, 'delta_m': dm, 'delta_min': dmin, 'changed': changed, 'on_route': on_route,
                 'verdict': worst['verdict'] if worst else ('changed' if changed else 'same'),
                 'reason': reason, 'reason_short': short_reason(reason)}
            if full:
                v['element_verdicts'] = ev
            else:
                v['element_verdicts'] = [{k: x[k] for k in ('element', 'verdict', 'seconds', 'risk')} for x in ev]
                v.pop('reason')
            variants[b] = v
    finally:
        take(net, recs)
    me = variants[body]
    headline = make_headline(item, me, injected, compare, rec, base_body_fixed)
    out = {'id': iid, 'city': city, 'scenario': scenario, 'trip_note': trip_note, 'leave_time': leave,
           'base_leave_time': base_leave, 'context': ctx, 'base_context': base_ctx, 'body': body, 'contrast': contrast,
           'compare': compare, 'compare_body': base_body_fixed, 'injected': injected, 'span_points': span_pts,
           'place': {'raw': rec.get('place_raw'), 'kind': kind, 'note': pnote},
           'geoms': geoms.store, 'variants': variants, 'headline': headline,
           'engine': 'hroute.impact_adapter.route_with_engine(engine="impact")',
           'generated_at': dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).isoformat(timespec='seconds')}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f'{iid}.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    return iid, {'changed': me['changed'], 'delta_m': me['delta_m'], 'delta_min': me['delta_min'],
                 'verdict': me['verdict'], 'blocked_base': me['base']['blocked'], 'blocked_whatif': me['whatif']['blocked'],
                 'placement': injected[0]['placement'] if injected else None, 'compare': compare,
                 'n_changed_bodies': sum(1 for v in variants.values() if v['changed'])}


def bname(b):
    n = re.sub(r'\s*\((?:claude addition|baseline[^)]*|legacy[^)]*)\)', '', I.body(b)['name'])
    return n[0].lower() + n[1:]


def make_headline(item, v, injected, compare, rec, base_body):
    b = bname(rec['body'])
    vb, vw = v['base'], v['whatif']
    dm, dmin = v['delta_m'], v['delta_min']
    if compare == 'body':
        if vw['blocked']:
            return (f'Same trip, same hour: an adult with no impairment walks {vb["length_m"]:.0f} m in {vb["minutes"]:.0f} min; '
                    f'for {b} every path crosses a blocking barrier, and RAASTA shows the least-blocked one ({vw["length_m"]:.0f} m) with each barrier named.')
        return (f'Same trip, same hour: an adult with no impairment walks {vb["length_m"]:.0f} m in {vb["minutes"]:.0f} min; '
                f'RAASTA routes {b} over {vw["length_m"]:.0f} m in {vw["minutes"]:.0f} min ({dm:+.0f} m, {dmin:+.0f} min).')
    if compare in ('context', 'hour'):
        what = 'at ' + rec['hhmm'] + (f', {rec["weather_raw"]}, {rec["light_raw"]}' if compare == 'context' else '')
        return (f'For {b}, the same trip {what}: {vw["length_m"]:.0f} m, {vw["minutes"]:.0f} min, against '
                f'{vb["length_m"]:.0f} m, {vb["minutes"]:.0f} min in the comparison run ({dm:+.0f} m, {dmin:+.0f} min).')
    def nm(x):
        n = re.sub(r'\s*\([^)]*\)', '', x['name'])
        return n[0].lower() + n[1:] if not n[:2].isupper() else n
    names = ' and the '.join(nm(x) for x in injected[:2]) or 'the element'
    plural = len(injected) > 1

    def vb_(k, default):
        w = VERB.get(k, default)
        if plural:
            w = w.replace('blocks', 'block').replace('slows', 'slow').replace('is a ', 'are a ').replace('does not', 'do not')
        return w
    where = injected[0]['road'] if injected and injected[0].get('road') else 'the route'
    verdict = v['verdict']
    if verdict == 'none' and v['changed']:
        verdict = 'minor'
    if vw['blocked'] and not vb['blocked']:
        return (f'The {names} on {where} {vb_(verdict, "changes")} {b}: no route is left without a blocking barrier, '
                f'so RAASTA shows the least-blocked path ({vw["length_m"]:.0f} m) and names the barrier.')
    if v['changed'] and vb['geom'] != vw['geom']:
        return (f'The {names} on {where} {vb_(verdict, "changes the trip for")} {b}: RAASTA moves the route '
                f'({vb["length_m"]:.0f} m to {vw["length_m"]:.0f} m, {dm:+.0f} m, {dmin:+.1f} min).')
    if v['changed']:
        return (f'The {names} on {where} {vb_(verdict, "changes the trip for")} {b}: same path, '
                f'{dmin:+.1f} min priced in ({vw["minutes"]:.0f} min in all).')
    return (f'The {names} on {where} {vb_(verdict, "does not change the trip for")} {b} on this trip: '
            f'the route and its {vw["minutes"]:.0f} min stay the same; the switcher shows the bodies it does change.')


def main(argv):
    tree = json.load(open(TREE))
    items = [it for it in tree['items'].values() if it.get('recipe')]
    if argv:
        items = [it for it in items if it['id'] in argv]
    idx_path = os.path.join(OUT, 'index.json')
    idx = {}
    if argv and os.path.exists(idx_path):
        idx = json.load(open(idx_path))
    errors = {}
    with Pool(min(10, os.cpu_count() or 2)) as pool:
        for res in pool.imap_unordered(safe_run, items):
            iid, row = res
            if 'error' in row:
                errors[iid] = row['error']
                print('ERROR', iid, row['error'], flush=True)
            else:
                idx[iid] = row
                print(iid, row, flush=True)
    os.makedirs(OUT, exist_ok=True)
    with open(idx_path, 'w') as f:
        json.dump(dict(sorted(idx.items())), f, separators=(',', ':'))
    print(json.dumps({'items': len(items), 'written': len(items) - len(errors), 'errors': errors}))


def safe_run(item):
    try:
        return run_item(item)
    except Exception as ex:
        import traceback
        return item['id'], {'error': f'{type(ex).__name__}: {ex} | {traceback.format_exc()[-600:]}'}


if __name__ == '__main__':
    main(sys.argv[1:])
