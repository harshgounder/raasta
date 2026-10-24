// /map v2: full-bleed 2.5D map. MapLibre native layers only (labels, extrusions, clustering and pitch all work together);
// v1 (deck.gl overlay, src/pages/map.js) is archived in archive/map-v1/ and still powers /what-if through src/demo/mapview.js.
import * as maplibregl from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import 'maplibre-gl/dist/maplibre-gl.css'
import './map2.css'
import { boot, esc, t, getLang, onLang } from '../pages/common.js'
import { cities, loadCity, pickRoutes, hhmm } from '../data/data.js'
import { reduceMotion } from '../shell/shell.js'
import { baseStyle, labelLayers, PAPER, INK, RED, BLUE } from './style.js'
import { addIcons, iconId, glyphSvg } from './icons.js'
import { buildElements, fanExpr, CATEGORY, CATEGORY_LABEL, NAME } from './elements.js'
import FALLBACK from './impact-fallback.json'
maplibregl.setWorkerUrl(workerUrl)

boot('map')
const L = (en, hi) => ({ en, hi: hi ?? en })
const tr = (o) => esc(t(o))
const page = document.getElementById('page')
page.className = 'mv2'
page.innerHTML = `
  <div class="mv2-bar" role="toolbar" aria-label="${esc(t(L('map controls', 'नक्शे के नियंत्रण')))}">
    <label class="ctl city"><span class="k">${tr(L('area', 'इलाका'))}</span><select class="city-sel" aria-label="area"></select></label>
    <label class="ctl time"><span class="k"><span class="kt">${tr(L('leave at', 'निकलें'))}</span> <output>08:00</output></span><input type="range" min="0" max="23.5" step="0.5" value="8" aria-label="leave time"></label>
    <div class="ctl seg view" role="radiogroup" aria-label="view">
      <button type="button" role="radio" data-v="3d" aria-checked="true">2.5D</button><button type="button" role="radio" data-v="2d" aria-checked="false">2D</button>
    </div>
    <button type="button" class="ctl panel-btn" aria-expanded="true">${tr(L('panel', 'पैनल'))}</button>
  </div>
  <div class="mv2-map" id="map"></div>
  <aside class="mv2-panel" aria-label="route and filters">
    <button type="button" class="sheet-handle" aria-label="open or close the panel"><span></span></button>
    <section class="p-trip"></section>
    <section class="p-route" aria-live="polite"></section>
    <section class="p-body"></section>
    <section class="p-cats"></section>
    <p class="p-foot"></p>
  </aside>
  <div class="mv2-legend" aria-label="legend"></div>
  <div class="el-card" role="dialog" aria-live="polite" hidden></div>
  <div class="seg-tip" hidden></div>`
const $ = (s) => page.querySelector(s)

// ---------- state
const S = { list: [], city: null, els: [], sc: 0, profile: 'manual_wheelchair', leaf: null, hour: 8, view: '3d', panel: innerWidth > 760,
  hidden: new Set(), whatIf: false, pinned: null, impact: null, tree: null, cond: 'clear', bodyDocs: new Map() }
const q = new URLSearchParams(location.search)

// ---------- impact matrix (who an element blocks / slows / warns): /content/impact-matrix.json when it exists, else
// the fallback derived from the routing lane's assumptions. tolerant adapter, schema notes in MAP-V2-BUILD.md
const PROFILE_FALLBACK = [
  { id: 'wheels', label: L('on wheels', 'पहियों पर'), children: [
    { id: 'manual_wheelchair', label: L('manual wheelchair', 'व्हीलचेयर'), profile: 'manual_wheelchair' },
    { id: 'power_wheelchair', label: L('power wheelchair', 'बैटरी व्हीलचेयर'), profile: 'power_wheelchair' },
    { id: 'pram', label: L('pram', 'बच्चा गाड़ी'), profile: 'pram' } ] },
  { id: 'aids', label: L('walking aids', 'चलने में सहारा'), children: [
    { id: 'walker_elderly', label: L('walker (elderly)', 'वॉकर (बुज़ुर्ग)'), profile: 'walker_elderly' },
    { id: 'crutches', label: L('crutches', 'बैसाखी'), profile: 'crutches' } ] },
  { id: 'sight', label: L('sight', 'दृष्टि'), children: [{ id: 'low_vision', label: L('low vision', 'कम दृष्टि'), profile: 'low_vision' }] },
  { id: 'foot', label: L('on foot', 'पैदल'), children: [{ id: 'default_walker', label: L('walking', 'पैदल'), profile: 'default_walker' }] },
]
const guessProfile = (s) => {
  s = String(s).toLowerCase()
  if (/power|electric|motor/.test(s) && /wheel/.test(s)) return 'power_wheelchair'
  if (/wheel/.test(s)) return 'manual_wheelchair'
  if (/pram|stroller|buggy|baby/.test(s)) return 'pram'
  if (/crutch|cane|stick/.test(s)) return 'crutches'
  if (/walker|elder|old|senior/.test(s)) return 'walker_elderly'
  if (/vision|blind|sight|see/.test(s)) return 'low_vision'
  return 'default_walker'
}
const lab = (x) => (typeof x === 'string' ? L(x) : x ?? L('?'))
function normTree(nodes) {
  return (nodes ?? []).map((n) => {
    const kids = n.children ?? n.subcategories ?? n.leaves ?? n.items
    const label = lab(n.label ?? n.name ?? n.id)
    if (kids?.length) return { id: n.id ?? label.en, label, children: normTree(kids) }
    return { id: n.id ?? label.en, label, profile: n.profile ?? n.route_profile ?? n.routing_profile ?? guessProfile(`${n.id} ${label.en}`) }
  })
}
const levelOf = (v) => { const s = String(typeof v === 'object' && v ? v.level ?? v.impact ?? v.effect ?? '' : v ?? '').toLowerCase(); return /block/.test(s) ? 'block' : /slow|hard|delay/.test(s) ? 'slow' : /warn|caution|minor/.test(s) ? 'warn' : /none|ok|no/.test(s) ? 'none' : null }
async function loadImpact() {
  let j = null
  try { const r = await fetch('/content/impact-matrix.json', { cache: 'no-cache' }); if (r.ok && /json/.test(r.headers.get('content-type') ?? '')) j = await r.json() } catch {}
  const table = {}, put = (type, who, v) => { const l = levelOf(v); if (l) ((table[type] ??= {})[who] = { level: l, note: typeof v === 'object' ? v.note ?? v.why ?? null : null }) }
  let tree = null, src = 'fallback'
  if (j?.schema === 'raasta-impact-matrix-v1' && j.contexts) {
    // raasta-impact-matrix-v1 (app/route/hroute/impact.py): verdict strings per element over bodies, per context
    S.rim = j
    S.rimBody = new Map((j.body_info ?? []).map((b) => [b.id, b]))
    S.rimEl = new Map((j.element_info ?? []).map((e, i) => [e.id, i]))
    // detector class -> the first matrix element of that class (e.g. missing_kerb_ramp -> "Kerb 15 cm with no ramp")
    S.rimByClass = new Map(); (j.element_info ?? []).forEach((e, i) => { if (e.detector_class && !S.rimByClass.has(e.detector_class)) S.rimByClass.set(e.detector_class, i) })
    // clean names in the UI: provenance markers like "(claude addition)" stay in the data and show as a hover note
    const clean = (n) => String(n).replace(/\s*\((claude addition|legacy [^)]*)\)/gi, '').trim()
    const added = (b) => /\*/.test(b?.hermes_id ?? '') || /claude addition/i.test(b?.name ?? '')
    const walk = (obj) => Object.entries(obj).filter(([k]) => k !== '_leaves').map(([k, v]) => ({ id: `cat:${k}`, label: L(k), children: [...walk(v), ...(v._leaves ?? []).map((id) => { const b = S.rimBody.get(id); return { id, label: L(clean(b?.name ?? id.replace(/_/g, ' '))), profile: rimProfile(id), note: added(b) ? 'added by our team, not in the RPwD schedule' : b?.rpwd ? `RPwD schedule: ${b.rpwd}` : null } })] }))
    tree = walk(j.body_tree ?? {})
    src = 'impact-matrix.json'
  } else if (j) {
    tree = normTree(j.bodies ?? j.tree ?? j.body_tree ?? null)
    const m = j.matrix ?? j.impacts ?? j.impact ?? j.types ?? null
    if (m && !Array.isArray(m)) for (const [type, row] of Object.entries(m)) for (const [who, v] of Object.entries(row ?? {})) put(type, who, v)
    for (const r of (Array.isArray(m) ? m : j.rows ?? [])) put(r.type ?? r.element ?? r.barrier, r.body ?? r.profile ?? r.leaf, r)
    if (Object.keys(table).length) src = 'impact-matrix.json'
  }
  if (!Object.keys(table).length) for (const [type, row] of Object.entries(FALLBACK.types)) for (const [who, v] of Object.entries(row)) put(type, who, v)
  if (!tree?.length) tree = PROFILE_FALLBACK
  S.impact = table; S.tree = tree; S.impactSrc = src
}
// matrix body id -> one of the 7 routing profiles the precomputed routes exist for
function rimProfile(id) {
  if (/^mw_|attendant/.test(id)) return 'manual_wheelchair'
  if (/^pw_|tilt_in_space|mobility_scooter|hand_cranked/.test(id)) return 'power_wheelchair'
  if (/pram|stroller|delivery_trolley|rolling_luggage|vendor_cart/.test(id)) return 'pram'
  if (/crutch|leg_cast|amputee/.test(id)) return 'crutches'
  if (/walker|walking_frame|rollator|older_80|older_70|cane|parkinson|vertigo|frail/.test(id) && !/blind/.test(id)) return 'walker_elderly'
  if (/blind|low_vision|deafblind|albinism|night_blind/.test(id)) return 'low_vision'
  return 'default_walker'
}
// which matrix context the leave hour falls in: evening and night -> night_dark, otherwise day_clear (unless picked)
// conditions the map exposes. clear / dark / rain have per-body routes (app/route/precompute_bodies.py); heat and
// smog only change the icons (the matrix has those contexts, the routes do not yet)
const COND = {
  clear: { ctx: 'day_clear', label: L('clear weather', 'साफ़ मौसम') },
  dark: { ctx: 'night_dark', label: L('evening, no working streetlight', 'शाम, स्ट्रीटलाइट बंद') },
  rain: { ctx: 'monsoon_rain_evening', label: L('heavy rain (monsoon)', 'तेज़ बारिश') },
  heat: { ctx: 'heatwave_noon', label: L('45 C heat wave (icons only)', 'लू (सिर्फ़ आइकन)') },
  smog: { ctx: 'winter_smog_morning', label: L('smog, AQI 380 (icons only)', 'स्मॉग (सिर्फ़ आइकन)') },
}
const rimContext = () => COND[S.cond]?.ctx ?? 'day_clear'
const RIM = { B: 'block', C: 'slow', W: 'warn', N: 'none' }
// detector type (+ words in the record label) -> the matrix element that stands for it. Picked by hand at build time
// (the first element of a class was sometimes odd, e.g. a truck tailgate for every parked vehicle)
const RIM_PICK = {
  parked_vehicle: [[/motor|two.?wheel|scooter|bike/i, 'two_wheeler_parked_footpath'], [/auto|rickshaw/i, 'auto_rickshaw_stand'], [/.*/, 'car_parked_footpath']],
  pole_obstruction: [[/light|lamp/i, 'streetlight_pole'], [/sign/i, 'signpost_pole'], [/box|cabinet/i, 'junction_box'], [/.*/, 'electric_pole_midpath']],
  broken_footpath: [[/.*/, 'broken_pavers']], pothole: [[/.*/, 'pothole']], vendor: [[/.*/, 'vendor_handcart']],
  open_drain: [[/manhole/i, 'open_manhole'], [/.*/, 'missing_drain_slab']], waterlogging: [[/.*/, 'waterlogging_shallow']],
  steps: [[/.*/, 'steps_short_flight']], missing_footpath: [[/.*/, 'no_footpath_road_walk']], missing_kerb_ramp: [[/.*/, 'kerb_150_no_ramp']],
  steep_slope: [[/.*/, 'running_slope_10']], kerb_ramp_present: [[/.*/, 'kerb_ramp_good']],
}
function rimIndex(type, label) {
  for (const [re, id] of RIM_PICK[type] ?? []) if (re.test(label ?? '') && S.rimEl.has(id)) return S.rimEl.get(id)
  return S.rimByClass.get(type)
}
const leaves = (nodes = S.tree, out = []) => { for (const n of nodes) n.children ? leaves(n.children, out) : out.push(n); return out }
const leafOf = (id) => leaves().find((x) => x.id === id)
function impactFor(type, leaf, label) {
  if (S.rim) {
    const ei = rimIndex(type, label), bi = S.rim.bodies.indexOf(leaf?.id)
    const ctx = S.rim.contexts[rimContext()] ?? Object.values(S.rim.contexts)[0]
    if (ei == null || bi < 0 || !ctx) return null
    return { level: RIM[ctx.verdict[ei][bi]] ?? null, seconds: ctx.seconds?.[ei]?.[bi] ?? null, risk: ctx.risk?.[ei]?.[bi] ?? null, element: S.rim.element_info[ei], context: ctx.label }
  }
  const row = S.impact?.[type]; if (!row) return null
  return row[leaf?.id] ?? row[leaf?.profile] ?? null
}
const sevOf = (el, leaf) => {
  if (el.positive) return 'clear'
  if (el.status !== 'ACCEPT') return 'unsure'
  return impactFor(el.type, leaf, el.label)?.level ?? 'warn'
}
const SIZE = { block: 0.66, slow: 0.6, warn: 0.42, none: 0.38, unsure: 0.54, clear: 0.46 }

// ---------- map
const map = new maplibregl.Map({ container: $('#map'), style: baseStyle(), center: [76.78, 30.74], zoom: 15, pitch: 55, bearing: -18, maxPitch: 70,
  attributionControl: { compact: true }, hash: false, fadeDuration: 150 })
map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-left')
map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-right')
map.on('error', (e) => { if (!/openfreemap|Failed to fetch|NetworkError|AJAXError/i.test(e?.error?.message ?? '')) console.warn('map:', e?.error?.message) })

const fc = (features) => ({ type: 'FeatureCollection', features })
const line = (path, props) => ({ type: 'Feature', properties: props, geometry: { type: 'LineString', coordinates: path } })
const pt = (pos, props) => ({ type: 'Feature', properties: props, geometry: { type: 'Point', coordinates: pos } })

function addOurLayers() {
  map.addSource('net', { type: 'geojson', data: fc([]) })
  map.addSource('cand', { type: 'geojson', data: fc([]) })
  map.addSource('rt-short', { type: 'geojson', data: fc([]) })
  map.addSource('rt-raasta', { type: 'geojson', data: fc([]), lineMetrics: true })
  map.addSource('els', { type: 'geojson', data: fc([]), cluster: true, clusterMaxZoom: 15, clusterRadius: 34 })
  map.addSource('els-stack', { type: 'geojson', data: fc([]) })
  map.addSource('anchors', { type: 'geojson', data: fc([]) })
  map.addLayer({ id: 'net-est', type: 'line', source: 'net', filter: ['==', ['get', 'est'], true], layout: { 'line-cap': 'butt' },
    paint: { 'line-color': INK, 'line-opacity': 0.62, 'line-width': ['interpolate', ['linear'], ['zoom'], 14, 0.9, 17, 1.7, 19, 2.4], 'line-dasharray': [2.2, 2] } })
  map.addLayer({ id: 'net-map', type: 'line', source: 'net', filter: ['==', ['get', 'est'], false], layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': INK, 'line-width': ['interpolate', ['linear'], ['zoom'], 14, 1.4, 17, 2.8, 19, 4] } })
  map.addLayer({ id: 'net-hit', type: 'line', source: 'net', paint: { 'line-color': '#000', 'line-opacity': 0, 'line-width': 12 } })
  map.addLayer({ id: 'net-hover', type: 'line', source: 'net', filter: ['==', ['get', 'id'], ''], paint: { 'line-color': INK, 'line-width': 5, 'line-opacity': 0.9 } })
  map.addLayer({ id: 'cand', type: 'line', source: 'cand', layout: { 'line-cap': 'round' }, paint: { 'line-color': INK, 'line-width': ['+', 4, ['*', 14, ['get', 'p']]], 'line-opacity': 0.35 } })
  map.addLayer({ id: 'cand-lbl', type: 'symbol', source: 'cand', layout: { 'symbol-placement': 'line-center', 'text-field': ['get', 'txt'], 'text-font': ['Noto Sans Bold'], 'text-size': 13, 'text-allow-overlap': true }, paint: { 'text-color': INK, 'text-halo-color': '#fff', 'text-halo-width': 2.5 } })
  // shortest: blue, thinner, offset to one side so it never hides under (or looks like) the red RAASTA line
  map.addLayer({ id: 'rt-short-case', type: 'line', source: 'rt-short', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#FFFFFF', 'line-width': 9, 'line-offset': 7 } })
  map.addLayer({ id: 'rt-short', type: 'line', source: 'rt-short', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': BLUE, 'line-width': 5, 'line-offset': 7 } })
  map.addLayer({ id: 'rt-raasta-case', type: 'line', source: 'rt-raasta', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#FFFFFF', 'line-width': 13 } })
  map.addLayer({ id: 'rt-raasta', type: 'line', source: 'rt-raasta', filter: ['!=', ['get', 'least'], true], layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-width': 8, 'line-gradient': RED } })
  map.addLayer({ id: 'rt-least', type: 'line', source: 'rt-raasta', filter: ['==', ['get', 'least'], true], layout: { 'line-cap': 'butt', 'line-join': 'round' },
    paint: { 'line-width': 8, 'line-color': RED, 'line-dasharray': [1.4, 0.9] } })
  map.addLayer({ id: 'rt-short-lbl', type: 'symbol', source: 'rt-short', layout: { 'symbol-placement': 'line', 'symbol-spacing': 420, 'text-field': ['get', 'txt'], 'text-font': ['Noto Sans Bold'], 'text-size': 14, 'text-offset': [0, 1.3], 'text-letter-spacing': 0.06, 'text-transform': 'uppercase' }, paint: { 'text-color': BLUE, 'text-halo-color': '#fff', 'text-halo-width': 3 } })
  map.addLayer({ id: 'rt-raasta-lbl', type: 'symbol', source: 'rt-raasta', layout: { 'symbol-placement': 'line', 'symbol-spacing': 420, 'text-field': ['get', 'txt'], 'text-font': ['Noto Sans Bold'], 'text-size': 15, 'text-offset': [0, -1.3], 'text-letter-spacing': 0.06, 'text-transform': 'uppercase' }, paint: { 'text-color': RED, 'text-halo-color': '#fff', 'text-halo-width': 3 } })
  map.addLayer({ id: 'net-name', type: 'symbol', source: 'net', minzoom: 15, filter: ['all', ['!=', ['get', 'name'], ''], ['==', ['get', 'kind'], 'sidewalk'], ['!=', ['get', 'side'], 'R']],
    layout: { 'symbol-placement': 'line', 'text-field': ['get', 'name'], 'text-font': ['Noto Sans Bold'], 'text-size': ['interpolate', ['linear'], ['zoom'], 15, 13, 18, 16], 'symbol-spacing': 360, 'text-letter-spacing': 0.04, 'text-max-angle': 30, 'text-offset': [0, -0.9], 'text-pitch-alignment': 'viewport' },
    paint: { 'text-color': '#222', 'text-halo-color': PAPER, 'text-halo-width': 2.6 } })
  for (const l of labelLayers()) map.addLayer(l)
  // elements: anchor dot at the true spot for fanned stacks, cluster discs when zoomed out, icons
  map.addLayer({ id: 'el-anchor', type: 'circle', source: 'anchors', minzoom: 15, paint: { 'circle-radius': 4, 'circle-color': INK, 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.5, 'circle-pitch-alignment': 'map' } })
  map.addLayer({ id: 'el-cluster', type: 'circle', source: 'els', filter: ['has', 'point_count'], paint: { 'circle-color': INK, 'circle-radius': ['interpolate', ['linear'], ['get', 'point_count'], 2, 16, 50, 26, 200, 34], 'circle-stroke-color': '#fff', 'circle-stroke-width': 3, 'circle-pitch-alignment': 'viewport' } })
  map.addLayer({ id: 'el-cluster-n', type: 'symbol', source: 'els', filter: ['has', 'point_count'], layout: { 'text-field': ['get', 'point_count_abbreviated'], 'text-font': ['Noto Sans Bold'], 'text-size': 15, 'text-allow-overlap': true }, paint: { 'text-color': '#fff' } })
  const elLayer = (id, source) => ({ id, type: 'symbol', source, filter: ['!', ['has', 'point_count']],
    layout: { 'icon-image': ['get', 'icon'], 'icon-size': ['interpolate', ['linear'], ['zoom'], 14, ['*', 0.6, ['get', 'size']], 16, ['*', 0.74, ['get', 'size']], 17.5, ['get', 'size'], 19, ['*', 1.25, ['get', 'size']]],
      'icon-offset': fanExpr(), 'icon-allow-overlap': true, 'icon-ignore-placement': true, 'icon-pitch-alignment': 'viewport', 'icon-rotation-alignment': 'viewport', 'symbol-sort-key': ['get', 'rank'],
      'text-field': ['step', ['zoom'], '', 18, ['get', 'short']], 'text-font': ['Noto Sans Bold'], 'text-size': 12, 'text-offset': [0, 2.2], 'text-optional': true },
    paint: { 'text-color': INK, 'text-halo-color': '#fff', 'text-halo-width': 2 } })
  // fanned stacks (one photo, many detections) never cluster: they are already bounded rings around their true spot
  map.addLayer(elLayer('el-stack', 'els-stack'))
  map.addLayer(elLayer('el', 'els'))
}

// ---------- data -> sources
const netFc = (c) => fc(c.edges.map((e) => line(e.path, { id: e.id, est: !!e.estimated, name: e.road_name && e.road_name !== e.kind ? e.road_name : '', kind: e.kind || '', side: e.side || '', tier: e.tier || e.evidence || '' })))
let bbox = null
function cityBbox(c) {
  let [x0, y0, x1, y1] = [180, 90, -180, -90]
  for (const e of c.edges) for (const [x, y] of e.path) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y) }
  return [x0, y0, x1, y1]
}
const inBox = ([x, y], b, pad = 0.0004) => x >= b[0] - pad && x <= b[2] + pad && y >= b[1] - pad && y <= b[3] + pad
const visibleEls = () => S.els.filter((x) => !S.hidden.has(CATEGORY[x.type] ?? 'other') && (S.whatIf || !x.what_if) && x.inside)
function pushEls() {
  const leaf = leafOf(S.leaf)
  const vis = visibleEls()
  const order = { block: 5, slow: 4, warn: 3, unsure: 2, clear: 1, none: 0 }
  const feat = (x) => { const sev = sevOf(x, leaf); return pt(x.position, { id: x.id, icon: iconId(x.type, sev), size: SIZE[sev] ?? 0.4, slot: x.slot ?? 0, rank: -(order[sev] ?? 0), short: t(NAME[x.type] ?? L(x.type)) }) }
  map.getSource('els')?.setData(fc(vis.filter((x) => !(x.stack > 1)).map(feat)))
  map.getSource('els-stack')?.setData(fc(vis.filter((x) => x.stack > 1).map(feat)))
  const anchors = new Map(); for (const x of vis) if (x.stack > 1) anchors.set(x.position.join(), x.position)
  map.getSource('anchors')?.setData(fc([...anchors.values()].map((p) => pt(p, {}))))
  renderCats()
}

// ---------- routes
let markers = [], animRaf = 0
const scen = () => S.city?.scenarios?.[S.sc] ?? null
const endName = (end, which, sc) => {
  let s = String(end?.label ?? '').split(' (')[0].trim()
  if (/^GPS of|^about \d/i.test(s) || !s) {
    const m = String(end?.label ?? '').match(/\(([^)]*)\)\s*$/); const qn = String(end?.label ?? '').match(/'([^']+)'/)
    const parts = String(sc?.name ?? '').split(/ to (?:the )?/)
    s = qn?.[1] ?? (parts.length === 2 && !/,/.test(sc.name) ? parts[which === 'from' ? 0 : 1] : null) ?? (m?.[1] && !/CC BY|photo/i.test(m[1]) ? m[1] : null) ?? s ?? which
  }
  return s.replace(/ photo spot$/, '')
}
// START / END pins. The label sits on a stem in the screen quadrant (up/down x left/right) with the fewest element
// icons, re-chosen after every move, so a pin never sits on top of the icons it should point out
function placePins() {
  markers.forEach((m) => m.marker.remove()); markers = []
  const sc = scen(); if (!sc) return
  for (const [k, end] of [['from', sc.from], ['to', sc.to]]) {
    if (end?.lnglat?.[0] == null) continue
    const el = document.createElement('div'); el.className = `pin ${k} q-ur`
    el.innerHTML = `<div class="tag"><b>${k === 'from' ? tr(L('start', 'शुरू')) : tr(L('end', 'मंज़िल'))}</b><span>${esc(endName(end, k, sc))}</span></div><i class="stem"></i><i class="foot"></i>`
    el.title = end.label ?? ''
    markers.push({ el, at: end.lnglat, q: 'ur', marker: new maplibregl.Marker({ element: el, anchor: 'bottom' }).setLngLat(end.lnglat).addTo(map) })
  }
  layoutPins()
}
function layoutPins() {
  if (!markers.length) return
  const vis = visibleEls().map((x) => map.project(x.position))
  const others = (m) => markers.filter((o) => o !== m).map((o) => map.project(o.at))
  // route lines count too (sampled every few metres of vertices), so a label does not hide the red or blue line
  const routePts = [S.r?.shortest, S.r?.accessible ?? S.r?.least_blocked].filter(Boolean).flatMap((r) => r.path.filter((_, i) => i % 2 === 0).map((q) => map.project(q)))
  for (const m of markers) {
    const p = map.project(m.at), W = 300, H = 230
    const box = { ur: [p.x, p.y - H, p.x + W, p.y], ul: [p.x - W, p.y - H, p.x, p.y], dr: [p.x, p.y, p.x + W, p.y + H], dl: [p.x - W, p.y, p.x, p.y + H] }
    const cw = map.getContainer().clientWidth, ch = map.getContainer().clientHeight
    const mr = map.getContainer().getBoundingClientRect()
    const blockers = ['.mv2-legend', ...(S.panel ? ['.mv2-panel'] : [])].map((q) => $(q)?.getBoundingClientRect()).filter((r) => r && r.width)
      .map((r) => ({ left: r.left - mr.left, right: r.right - mr.left, top: r.top - mr.top, bottom: r.bottom - mr.top }))
    const score = (q) => { const [a, b, c, d] = box[q]; let n = 0
      for (const v of vis) if (v.x >= a && v.x <= c && v.y >= b && v.y <= d) n++
      for (const v of others(m)) if (v.x >= a && v.x <= c && v.y >= b && v.y <= d) n += 3
      for (const v of routePts) if (v.x >= a && v.x <= c && v.y >= b && v.y <= d) n += 0.5
      if (a < 0 || c > cw || b < 0 || d > ch) n += 50  // off screen
      for (const r of blockers) if (a < r.right && c > r.left && b < r.bottom && d > r.top) n += 40  // under the panel or legend
      return n + (q === m.q ? -0.5 : 0) }
    const q = ['ur', 'ul', 'dr', 'dl'].sort((x, y) => score(x) - score(y))[0]
    if (q === m.q) continue
    const flip = (q[0] === 'd') !== (m.q[0] === 'd')
    m.q = q; m.el.classList.remove('q-ur', 'q-ul', 'q-dr', 'q-dl'); m.el.classList.add(`q-${q}`)
    if (flip) { m.marker.remove(); m.marker = new maplibregl.Marker({ element: m.el, anchor: q[0] === 'd' ? 'top' : 'bottom' }).setLngLat(m.at).addTo(map) }
  }
}
// per-body routes: app/site-data/<city>/routes-bodies/<trip>.json (schema raasta-routes-bodies-v1)
async function loadBodyDoc() {
  const sc = scen(), c = S.list.find((x) => x.id === S.city?.id)
  if (!sc || !c?.bodies?.includes(sc.id)) return null
  const key = `${c.id}/${sc.id}`
  if (!S.bodyDocs.has(key)) {
    let doc = null
    try { const r = await fetch(`/site-data/${encodeURIComponent(c.id)}/routes-bodies/${encodeURIComponent(sc.id)}.json`); if (r.ok) doc = await r.json() } catch {}
    S.bodyDocs.set(key, doc)
  }
  return S.bodyDocs.get(key)
}
function bodyRoutes() {
  const doc = S.bodyDocs.get(`${S.city?.id}/${scen()?.id}`)
  if (!doc || !S.leaf) return null
  const hourOf = (lt) => +lt.slice(11, 13) + +lt.slice(14, 16) / 60
  const cond = COND[S.cond] && doc.conditions[S.cond] ? S.cond : 'clear'
  const times = doc.leave_times.filter((lt) => doc.combos[`${lt}|${cond}`])
  if (!times.length) return null
  const lt = times.reduce((a, b) => (Math.abs(hourOf(b) - S.hour) < Math.abs(hourOf(a) - S.hour) ? b : a))
  const x = doc.combos[`${lt}|${cond}`]?.[S.leaf]
  if (!x) return null
  const R = (o) => o && { path: doc.paths[o.p], length_m: o.m, minutes: o.min, barrier_count: o.bc, blocking_count: o.blk, blocked_for_profile: o.bfp,
    barriers_observed: o.obs, evidence_line: o.ev, unknown_share_pct: o.unk, mapped_m: o.mm, estimated_m: o.em, blocking: (o.why ?? []).map((w) => ({ type: w.type, why: w.why })) }
  return { shortest: R(x.s), accessible: R(x.a), least_blocked: x.a ? null : R(x.l), engine: 'impact', lt, cond, status: x.st }
}
function drawRoutes(animate = true) {
  const sc = scen(); if (!sc) return
  S.city.routes = sc
  const r = bodyRoutes() ?? pickRoutes(S.city, S.profile, S.hour)
  S.r = r
  const raasta = r.accessible ?? r.least_blocked
  map.getSource('rt-short')?.setData(fc(r.shortest ? [line(r.shortest.path, { txt: t(L('shortest route', 'सबसे छोटा रास्ता')) })] : []))
  map.getSource('rt-raasta')?.setData(fc(raasta ? [line(raasta.path, { least: !r.accessible, txt: r.accessible ? t(L('RAASTA route', 'रास्ता')) : t(L('least-blocked route', 'सबसे कम रुकावट')) })] : []))
  cancelAnimationFrame(animRaf)
  if (!animate || reduceMotion.matches) { map.setPaintProperty('rt-raasta', 'line-gradient', ['step', ['line-progress'], RED, 1, RED]); return }
  const t0 = performance.now(), dur = 1600
  const step = () => {
    const k = Math.min(1, (performance.now() - t0) / dur), e = 1 - Math.pow(1 - k, 3)
    map.setPaintProperty('rt-raasta', 'line-gradient', ['step', ['line-progress'], RED, Math.max(0.0005, e), 'rgba(200,41,36,0)'])
    if (k < 1) animRaf = requestAnimationFrame(step)
  }
  step()
}
function fitScenario(fly = true) {
  const sc = scen(); const r = S.r
  const pts = [...(r?.shortest?.path ?? []), ...((r?.accessible ?? r?.least_blocked)?.path ?? []), sc?.from?.lnglat, sc?.to?.lnglat].filter((p) => p?.[0] != null)
  if (!pts.length) { if (bbox) map.fitBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]], { duration: 0 }); return }
  let [x0, y0, x1, y1] = [180, 90, -180, -90]
  for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y) }
  const mobile = innerWidth <= 760
  const padding = mobile ? { top: 70, bottom: 140, left: 30, right: 30 } : { top: 90, bottom: 110, left: 110, right: S.panel ? 470 : 110 }
  const pitch = S.view === '3d' ? 55 : 0, bearing = S.view === '3d' ? -18 : 0
  const cam = map.cameraForBounds([[x0, y0], [x1, y1]], { padding, bearing })
  if (!cam) return
  const opts = { ...cam, zoom: Math.min(18, cam.zoom + (pitch ? 0.25 : 0)), pitch, bearing }
  fly && !reduceMotion.matches ? map.flyTo({ ...opts, duration: 2200, essential: true }) : map.jumpTo(opts)
}

// ---------- panel
const fmtM = (m) => (m == null ? '?' : m >= 1000 ? `${(m / 1000).toFixed(2)} km` : `${Math.round(m)} m`)
const PRETTY_BLOCK = { no_footpath_on_median: L('no footpath assumed on a road median or traffic island', 'डिवाइडर पर फुटपाथ नहीं माना') }
function renderTrip() {
  const sc = S.city?.scenarios ?? []
  const shown = sc.map((x, i) => [x, i]).filter(([x]) => S.whatIf || !x.what_if)
  $('.p-trip').innerHTML = `<label class="row"><span class="k">${tr(L('trip', 'सफ़र'))}</span><select class="trip-sel">${shown.map(([x, i]) => `<option value="${i}"${i === S.sc ? ' selected' : ''}>${x.what_if ? 'WHAT-IF: ' : ''}${esc(x.name)}</option>`).join('')}</select></label>
    <label class="chk"><input type="checkbox" class="wi"${S.whatIf ? ' checked' : ''}> ${tr(L('show what-if examples (placed by us to demo, not evidence)', 'what-if उदाहरण दिखाएँ (डेमो, सबूत नहीं)'))}</label>`
}
function renderRoute() {
  const r = S.r ?? {}, sc = scen(), leaf = leafOf(S.leaf), body = t(leaf?.label) || S.profile.replace(/_/g, ' ')
  const ra = r.accessible ?? r.least_blocked, sh = r.shortest
  if (!sc || !sh) { $('.p-route').innerHTML = `<p>${tr(L('No route for this trip yet.', 'इस सफ़र का रास्ता अभी नहीं.'))}</p>`; return }
  const lt = (S.city.scenarios[S.sc].leave_times ?? []).map((x) => x.slice(11, 16))
  const shBlocked = sh.blocked_for_profile || (sh.blocking_count ?? 0) > 0
  const blockWhy = (list) => {
    const by = new Map(); for (const b of list ?? []) { const k = b.type; by.set(k, (by.get(k) ?? 0) + 1) }
    return [...by].map(([k, n]) => `${n} x ${esc(t(PRETTY_BLOCK[k] ?? NAME[k] ?? L(k.replace(/_/g, ' '))))}`).join('; ')
  }
  const unknown = ra?.unknown_share_pct
  const near = ra ? nearRoute(ra.path, 20) : { placed: 0, unsure: 0 }
  const lines = []
  if (r.accessible) {
    lines.push(`<div class="rline raasta"><i></i><div><b>${tr(L('RAASTA route', 'रास्ता'))}</b> ${tr(L('for', 'के लिए'))} ${esc(body)}<br><span class="big">${fmtM(ra.length_m)}</span> <span class="big">${ra.minutes != null ? `${Math.round(ra.minutes)} min` : ''}</span>
      ${sh && ra.length_m > sh.length_m ? `<small>+${Math.round(ra.length_m - sh.length_m)} m ${tr(L('longer than the shortest', 'सबसे छोटे से ज़्यादा'))}</small>` : ''}</div></div>`)
  } else if (r.least_blocked) {
    lines.push(`<div class="rline raasta least"><i></i><div><b>${tr(L('No route avoids every block for', 'कोई रास्ता हर रुकावट से नहीं बचता:'))} ${esc(body)}.</b><br>${tr(L('Dashed red is the least-blocked route', 'लाल धारी: सबसे कम रुकावट वाला रास्ता'))}: <span class="big">${fmtM(ra.length_m)}</span>, ${tr(L('it meets', 'इसमें'))} ${ra.blocking_count ?? 0} ${tr(L('blocking barrier(s)', 'रोकने वाली रुकावटें'))}${ra.blocking?.length ? `: ${blockWhy(ra.blocking)}` : ''}.</div></div>`)
  }
  lines.push(`<div class="rline short"><i></i><div><b>${tr(L('Shortest route', 'सबसे छोटा रास्ता'))}</b> <span class="big">${fmtM(sh.length_m)}</span> ${sh.minutes != null ? `<span class="big">${Math.round(sh.minutes)} min</span>` : ''}
    ${sh.barrier_count ? `<br>${tr(L('meets', 'रास्ते में'))} <b>${sh.barrier_count}</b> ${tr(L('placed barriers', 'दर्ज रुकावटें'))}` : ''}
    ${shBlocked ? `<br><span class="warn">${tr(L('blocked for', 'रुकावट:'))} ${esc(body)}</span>${sh.blocking?.length ? `: ${blockWhy(sh.blocking)}` : ''}` : ''}</div></div>`)
  const facts = ra ? [
    [L('barriers met', 'रास्ते में रुकावटें'), `${ra.barrier_count ?? 0}${ra.blocking_count ? `, ${ra.blocking_count} ${t(L('blocking', 'रोकने वाली'))}` : ''}`],
    [L('evidence', 'सबूत'), esc(ra.evidence_line ?? '?')],
    near.unsure && [L('seen near it, not placed', 'पास में दिखे, रखे नहीं'), `${near.unsure} ${t(L('elements within 20 m (hollow icons): not sure which footpath, so the route does not count them', 'तत्व 20 m में (खोखले): पक्का नहीं कौन सा फुटपाथ, इसलिए गिने नहीं'))}`],
    [L('no photo or label yet', 'अभी कोई फ़ोटो या लेबल नहीं'), unknown != null ? `${Math.round(unknown)}% ${t(L('of the route', 'रास्ते का'))}` : '?'],
  ].filter(Boolean) : []
  $('.p-route').innerHTML = `<h2>${esc(sc.from ? endName(sc.from, 'from', sc) : '')} <span aria-hidden="true">&rarr;</span> ${esc(sc.to ? endName(sc.to, 'to', sc) : '')}</h2>
    ${sc.what_if ? `<p class="wi-tag">WHAT-IF: ${tr(L('example barriers placed by us to show how body and hour change the route; not evidence', 'हमारे रखे उदाहरण, सबूत नहीं'))}</p>` : ''}
    ${lines.join('')}
    <dl class="facts">${facts.map(([k, v]) => `<dt>${tr(k)}</dt><dd>${v}</dd>`).join('')}</dl>
    <p class="note">${r.engine === 'impact' ? `${tr(L('Computed for this body by the impact engine', 'इस शरीर के लिए गणना'))}: ${esc(r.lt.slice(11, 16))}, ${tr(COND[r.cond]?.label ?? L(r.cond))}${S.cond !== r.cond ? ` ${tr(L('(no route file for that condition; clear weather shown)', '(उस हालात की फ़ाइल नहीं; साफ़ मौसम)'))}` : ''}. ` : `${tr(L('Nearest of 7 movement profiles.', '7 प्रोफ़ाइल में सबसे पास.'))} `}${tr(L('Minutes are walking or rolling time only. "No photo yet" means unknown, never safe.', 'मिनट सिर्फ़ चलने का समय. "फ़ोटो नहीं" मतलब अज्ञात, सुरक्षित नहीं.'))} ${lt.length ? `${tr(L('Leave times computed:', 'गणना के समय:'))} ${lt.join(', ')}; ${tr(L('the nearest to your time is shown.', 'आपके समय के सबसे पास वाला.'))}` : ''}</p>`
}
// elements within d metres of a route polyline (local equirectangular metres; fine at street scale)
function nearRoute(path, d) {
  if (!path?.length) return { placed: 0, unsure: 0 }
  const lat0 = path[0][1] * Math.PI / 180, kx = 111320 * Math.cos(lat0), ky = 110540
  const P = path.map(([x, y]) => [x * kx, y * ky])
  let placed = 0, unsure = 0
  for (const el of S.els) {
    if (!el.inside || el.positive || (!S.whatIf && el.what_if)) continue
    const qx = el.position[0] * kx, qy = el.position[1] * ky
    let best = Infinity
    for (let i = 1; i < P.length && best > d; i++) {
      const [ax, ay] = P[i - 1], [bx, by] = P[i], dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy
      const k = L2 ? Math.max(0, Math.min(1, ((qx - ax) * dx + (qy - ay) * dy) / L2)) : 0
      best = Math.min(best, Math.hypot(qx - ax - k * dx, qy - ay - k * dy))
    }
    if (best <= d) el.status === 'ACCEPT' ? placed++ : unsure++
  }
  return { placed, unsure }
}
function renderBody() {
  const has = (n) => n.id === S.leaf || (n.children ?? []).some(has)
  const node = (n, depth) => n.children
    ? `<details${has(n) ? ' open' : ''}><summary>${tr(n.label)} <small>${leaves(n.children).length}</small></summary><div class="kids${n.children.some((c) => c.children) ? ' deep' : ''}">${n.children.map((c) => node(c, depth + 1)).join('')}</div></details>`
    : `<button type="button" role="radio" class="leaf" data-leaf="${esc(n.id)}" aria-checked="${n.id === S.leaf}"${n.note ? ` title="${esc(n.note)}"` : ''}>${tr(n.label)}</button>`
  const leaf = leafOf(S.leaf), prof = (S.city?.scenarios?.[S.sc]?.profiles ?? []).find((p) => p.id === leaf?.profile)
  const ctxSel = `<label class="row ctx"><span class="k">${tr(L('conditions', 'हालात'))}</span><select class="ctx-sel">${Object.entries(COND).map(([k, c]) => `<option value="${k}"${S.cond === k ? ' selected' : ''}>${tr(c.label)}</option>`).join('')}</select></label>`
  $('.p-body').innerHTML = `<h3>${tr(L('whose body?', 'किसका शरीर?'))} <small>${leaves().length} ${tr(L('bodies', 'शरीर'))}</small></h3><div class="tree" role="radiogroup" aria-label="body">${S.tree.map((n) => node(n, 0)).join('')}</div>
    ${ctxSel}
    <p class="note">${tr(L('Icons change with the body: solid = blocks, ring = slows, small = warns.', 'आइकन शरीर के साथ बदलते हैं: भरा = रोकता, घेरा = धीमा, छोटा = चेतावनी.'))}
    ${S.r?.engine === 'impact' ? tr(L('The route is computed for this exact body by the impact engine.', 'रास्ता इसी शरीर के लिए गणना किया गया है.')) : leaf?.profile ? `${tr(L('No per-body route file for this trip; showing the nearest of 7 movement profiles:', 'इस सफ़र की प्रति-शरीर फ़ाइल नहीं; 7 प्रोफ़ाइल में सबसे पास:'))} <b>${esc(t(prof?.label) || leaf.profile.replace(/_/g, ' '))}</b>.` : ''}
    ${leaf?.note ? `<small>${esc(leaf.label?.en ?? '')}: ${esc(leaf.note)}</small>` : ''}
    <small>${S.impactSrc === 'fallback' ? tr(L('Impact source: routing assumptions (app/route), not measured.', 'स्रोत: रूटिंग मान्यताएँ, मापा नहीं.')) : tr(L('Impact source: impact-matrix.json. Most element values there are assumptions; app/route/taxonomy/README says which are sourced.', 'स्रोत: impact-matrix.json. ज़्यादातर मान मान्यताएँ हैं; कौन से स्रोत वाले हैं, app/route/taxonomy/README में.'))}</small></p>`
}
function renderCats() {
  if (!S.city) return
  const b = map.getBounds()
  const all = S.els.filter((x) => x.inside && (S.whatIf || !x.what_if))
  const cats = new Map()
  for (const x of all) { const c = CATEGORY[x.type] ?? 'other'; const o = cats.get(c) ?? cats.set(c, { n: 0, view: 0, type: x.type }).get(c); o.n++; if (b.contains(x.position)) o.view++ }
  const unsure = all.filter((x) => x.status !== 'ACCEPT' && !x.positive).length
  const inView = all.filter((x) => !S.hidden.has(CATEGORY[x.type] ?? 'other') && b.contains(x.position)).length
  $('.p-cats').innerHTML = `<h3>${tr(L('elements on the footpaths', 'फुटपाथ पर चीज़ें'))} <small>${inView} ${tr(L('in view', 'दिख रहे'))} / ${all.length}</small></h3>
    <div class="cats">${[...cats].sort((a, b2) => b2[1].n - a[1].n).map(([c, o]) => `<button type="button" class="cat" data-cat="${esc(c)}" aria-pressed="${!S.hidden.has(c)}">${glyphSvg(o.type, 30, c === 'seen fine' ? 'clear' : 'slow')}<span>${tr(CATEGORY_LABEL[c] ?? L(c))}</span><b>${o.view}<small>/${o.n}</small></b></button>`).join('') || `<p class="note">${tr(L('No elements recorded in this area yet. Every footpath here is unknown, not safe.', 'इस इलाके में अभी कुछ दर्ज नहीं. हर फुटपाथ अज्ञात है, सुरक्षित नहीं.'))}</p>`}</div>
    ${unsure ? `<p class="note">${unsure} ${tr(L('are hollow: seen in a photo, not sure which footpath (ABSTAIN). Hover one to see the candidate footpaths.', 'खोखले: फ़ोटो में दिखे, पक्का नहीं कौन सा फुटपाथ. संभावित फुटपाथ देखने के लिए होवर करें.'))}</p>` : ''}
    ${S.outside ? `<p class="note">${S.outside} ${tr(L('more photo records lie outside this area and are not drawn.', 'और रिकॉर्ड इस इलाके के बाहर हैं, नहीं दिखाए.'))}</p>` : ''}`
}
function renderLegend() {
  $('.mv2-legend').innerHTML = `<ul>
    <li><i class="lg raasta"></i>${tr(L('RAASTA route for this body', 'इस शरीर का रास्ता'))}</li>
    <li><i class="lg short"></i>${tr(L('normal shortest route', 'सामान्य सबसे छोटा रास्ता'))}</li>
    <li><i class="lg mapped"></i>${tr(L('mapped footpath (OpenStreetMap)', 'नक्शे पर दर्ज फुटपाथ'))}</li>
    <li><i class="lg est"></i>${tr(L('estimated footpath, not mapped', 'अनुमानित फुटपाथ, नक्शे पर नहीं'))}</li>
  </ul><ul class="icons">
    <li>${glyphSvg('parked_vehicle', 26, 'block')}${tr(L('blocks', 'रोकता'))}</li>
    <li>${glyphSvg('parked_vehicle', 26, 'slow')}${tr(L('slows', 'धीमा'))}</li>
    <li class="sm">${glyphSvg('parked_vehicle', 18, 'slow')}${tr(L('warns', 'चेतावनी'))}</li>
    <li>${glyphSvg('parked_vehicle', 26, 'unsure')}${tr(L('not sure where', 'जगह पक्की नहीं'))}</li>
  </ul>`
}
function renderFoot() {
  const m = S.city?.meta ?? {}
  $('.p-foot').innerHTML = `${esc(m.area ?? m.name ?? '')}. ${tr(L('Footpaths and base map: OpenStreetMap contributors (ODbL), tiles OpenFreeMap. Generated footpaths are geometric estimates beside OSM roads.', 'फुटपाथ और नक्शा: OpenStreetMap (ODbL), टाइल्स OpenFreeMap. अनुमानित फुटपाथ OSM सड़कों के बगल में ज्यामितीय अंदाज़ा हैं.'))}`
}
const renderAll = () => { renderTrip(); renderRoute(); renderBody(); renderCats(); renderLegend(); renderFoot() }

// ---------- element card (hover on desktop, tap on touch)
const card = $('.el-card'), tip = $('.seg-tip')
const fmtDate = (s) => { if (!s) return null; const d = new Date(String(s).length === 10 ? s + 'T00:00:00' : s); return isNaN(d) ? String(s) : d.toLocaleDateString(getLang() === 'hi' ? 'hi-IN' : 'en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) }
function cropStyle(url, crop) {
  // pad the detector box to a readable thumbnail (at least 35% of the photo wide), keep it inside the image
  if (!crop) return `background-image:url('${encodeURI(url)}');background-size:cover;background-position:center`
  let [x, y, w, h] = crop
  const cx = x + w / 2, cy = y + h / 2
  const W = Math.min(1, Math.max(w * 1.8, 0.35)), H = Math.min(1, Math.max(h * 1.8, W * 0.66))
  const x0 = Math.min(Math.max(0, cx - W / 2), 1 - W), y0 = Math.min(Math.max(0, cy - H / 2), 1 - H)
  const px = W >= 1 ? 0 : (x0 / (1 - W)) * 100, py = H >= 1 ? 0 : (y0 / (1 - H)) * 100
  return `background-image:url('${encodeURI(url)}');background-size:${100 / W}% ${100 / H}%;background-position:${px}% ${py}%`
}
function cardHtml(el) {
  const name = t(NAME[el.type] ?? L(el.type.replace(/_/g, ' ')))
  const cat = t(CATEGORY_LABEL[CATEGORY[el.type] ?? 'other'])
  const leaf = leafOf(S.leaf)
  let where
  if (el.positive) where = L('seen fine here, on that date only', 'उस तारीख को यहाँ ठीक देखा')
  else if (el.status === 'ACCEPT') where = L(`placed on this footpath${el.p != null ? ` (p ${Math.round(el.p * 100)}%)` : ''}`, `इस फुटपाथ पर रखा${el.p != null ? ` (p ${Math.round(el.p * 100)}%)` : ''}`)
  else if (el.where === 'camera') where = L('seen in a photo, not sure where: no footpath within 30 m of the camera', 'फ़ोटो में दिखा, जगह पक्की नहीं')
  else where = L('seen in a photo, not sure which footpath (ABSTAIN): drawn on the most likely one', 'फ़ोटो में दिखा, पक्का नहीं कौन सा फुटपाथ')
  const groups = { block: [], slow: [], warn: [] }
  if (!el.positive) for (const lf of leaves()) { const lv = impactFor(el.type, lf, el.label)?.level; if (groups[lv]) groups[lv].push(t(lf.label)) }
  const few = (arr) => esc(arr.slice(0, 5).join(', ')) + (arr.length > 5 ? ` <i>+${arr.length - 5} ${t(L('more', 'और'))}</i>` : '')
  const mine = leaf && !el.positive ? impactFor(el.type, leaf, el.label) : null
  const imp = el.positive ? '' : `<div class="imp">
    ${mine ? `<p class="you ${esc(mine.level ?? '')}">${tr(L('for', 'के लिए'))} <b>${tr(leaf.label)}</b>: <b class="lv">${esc(mine.level === 'block' ? t(L('blocks', 'रोकता')) : mine.level === 'slow' ? t(L('slows', 'धीमा')) : mine.level === 'warn' ? t(L('warns', 'चेतावनी')) : t(L('no effect', 'असर नहीं')))}</b>${mine.seconds ? `, +${mine.seconds} s` : ''}${el.status !== 'ACCEPT' ? ` ${tr(L('(if it is on that footpath; routes do not count it until placed)', '(अगर उसी फुटपाथ पर है)'))}` : ''}</p>` : ''}
    ${[['block', L('blocks', 'रोकता')], ['slow', L('slows', 'धीमा करता')], ['warn', L('warns', 'चेतावनी')]].filter(([k]) => groups[k].length).map(([k, lb]) => `<p class="${k}"><b>${tr(lb)}</b> ${groups[k].length}: ${few(groups[k])}</p>`).join('') || `<p>${tr(L('no impact rule for this type yet', 'इस प्रकार का नियम अभी नहीं'))}</p>`}
    ${mine?.element ? `<small>${tr(L('matrix row', 'पंक्ति'))}: ${esc(mine.element.name)}; ${esc(mine.context ?? '')}; ${mine.element.source && !/^ASSUMPTION/i.test(mine.element.source) ? `${tr(L('sourced', 'स्रोत'))}: ${esc(mine.element.source)}` : tr(L('values are assumptions', 'मान मान्यताएँ हैं'))}</small>` : ''}</div>`
  const facts = [
    [L('date seen', 'देखा'), fmtDate(el.observed) ?? t(L('not dated', 'तारीख नहीं'))],
    [L('confidence', 'भरोसा'), el.confidence != null ? `${Math.round(el.confidence * 100)}%` : '?'],
    el.height_cm != null && [L('height', 'ऊँचाई'), `${el.height_cm} cm`],
    el.permanence && [L('lasts', 'टिकाऊ'), el.permanence === 'temporary' ? t(L('temporary (comes and goes)', 'अस्थायी')) : t(L('permanent', 'स्थायी'))],
  ].filter(Boolean)
  const cands = el.status !== 'ACCEPT' && el.candidates.length ? `<div class="cands"><b>${tr(L('candidate footpaths', 'संभावित फुटपाथ'))}</b><ol>${el.candidates.map((c) => `<li>${esc(c.kind ?? 'segment')} ${c.side ? `(${c.side === 'L' ? 'left' : c.side === 'R' ? 'right' : c.side} side)` : ''}${c.road ? `, ${esc(c.road)}` : ''}: p ${Math.round((c.p ?? 0) * 100)}%, ${c.distance_m ?? '?'} m</li>`).join('')}</ol>${el.reason ? `<small>${esc(el.reason)}</small>` : ''}</div>` : (el.reason && el.status !== 'ACCEPT' ? `<small>${esc(el.reason)}</small>` : '')
  return `<button type="button" class="x" aria-label="close">&times;</button>
    <header>${glyphSvg(el.type, 44, el.positive ? 'clear' : el.status === 'ACCEPT' ? 'block' : 'unsure')}<div><h3>${esc(name)}</h3><p>${esc(cat)}${el.what_if ? ' · WHAT-IF' : ''}</p></div></header>
    ${el.photo ? `<a class="ph" href="${esc(el.photo.url)}" target="_blank" rel="noopener" style="${cropStyle(el.photo.url, el.photo.crop)}" aria-label="open the photo"></a>` : ''}
    <p class="where ${el.status === 'ACCEPT' ? 'ok' : 'unsure'}">${tr(where)}</p>
    ${el.label ? `<p class="lbl">${esc(el.label)}</p>` : ''}
    <dl>${facts.map(([k, v]) => `<dt>${tr(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>
    ${imp}${cands}
    <p class="credit">${esc(el.credit ?? el.source ?? '')}${el.source_url ? ` <a href="${esc(el.source_url)}" target="_blank" rel="noopener">${tr(L('source', 'स्रोत'))}</a>` : ''}</p>`
}
function showCandidates(el) {
  const feats = []
  if (el && el.status !== 'ACCEPT') for (const c of el.candidates) { const e = S.city.edgeById.get(c.segment_id); if (e) feats.push(line(e.path, { p: c.p ?? 0, txt: `${Math.round((c.p ?? 0) * 100)}%` })) }
  map.getSource('cand')?.setData(fc(feats))
}
function openCard(el, at, pin = false) {
  if (!el) { if (!S.pinned) { card.hidden = true; showCandidates(null) } return }
  if (S.pinned && !pin && S.pinned !== el.id) return
  if (pin) S.pinned = el.id
  card.innerHTML = cardHtml(el); card.hidden = false
  card.classList.toggle('pinned', !!S.pinned)
  showCandidates(el)
  if (innerWidth <= 760) { card.style.left = ''; card.style.top = ''; return }
  const r = map.getContainer().getBoundingClientRect(), w = card.offsetWidth, h = card.offsetHeight
  let x = r.left + at.x + 26, y = r.top + at.y - h / 2
  if (x + w > innerWidth - 16) x = r.left + at.x - w - 26
  y = Math.max(r.top + 12, Math.min(y, innerHeight - h - 12))
  card.style.left = `${Math.max(12, x)}px`; card.style.top = `${y}px`
}
card.addEventListener('click', (e) => { if (e.target.closest('.x')) { S.pinned = null; card.hidden = true; showCandidates(null) } })
const elById = (id) => S.els.find((x) => x.id === id)

function wire() {
  for (const lid of ['el', 'el-stack']) {
  map.on('mousemove', lid, (e) => { map.getCanvas().style.cursor = 'pointer'; tip.hidden = true; const f = e.features?.[0]; if (f) openCard(elById(f.properties.id), e.point) })
  map.on('mouseleave', lid, () => { map.getCanvas().style.cursor = ''; if (!S.pinned) openCard(null) })
  map.on('click', lid, (e) => { const f = e.features?.[0]; if (f) { S.pinned = null; openCard(elById(f.properties.id), e.point, true) } })
  }
  map.on('click', (e) => { if (!map.queryRenderedFeatures(e.point, { layers: ['el', 'el-stack', 'el-cluster'] }).length && S.pinned) { S.pinned = null; card.hidden = true; showCandidates(null) } })
  map.on('click', 'el-cluster', async (e) => {
    const f = e.features[0]; const z = await map.getSource('els').getClusterExpansionZoom(f.properties.cluster_id)
    map.easeTo({ center: f.geometry.coordinates, zoom: Math.max(z, 15.2), duration: reduceMotion.matches ? 0 : 700 })
  })
  map.on('mouseenter', 'el-cluster', () => { map.getCanvas().style.cursor = 'zoom-in' })
  map.on('mouseleave', 'el-cluster', () => { map.getCanvas().style.cursor = '' })
  map.on('mousemove', 'net-hit', (e) => {
    if (map.queryRenderedFeatures(e.point, { layers: ['el', 'el-stack'] }).length) return
    const p = e.features?.[0]?.properties; if (!p) return
    map.setFilter('net-hover', ['==', ['get', 'id'], p.id])
    tip.hidden = false
    tip.innerHTML = `<b>${esc(p.name || p.kind)}</b><br>${p.est ? tr(L('estimated footpath, not mapped', 'अनुमानित फुटपाथ, नक्शे पर नहीं')) : tr(L('mapped footpath (OpenStreetMap)', 'नक्शे पर दर्ज फुटपाथ'))}<br><small>${esc(p.kind)} · ${esc(String(p.tier).replace(/_/g, ' '))}</small>`
    const r = map.getContainer().getBoundingClientRect()
    tip.style.left = `${Math.min(r.left + e.point.x + 16, innerWidth - 260)}px`; tip.style.top = `${r.top + e.point.y + 16}px`
  })
  map.on('mouseleave', 'net-hit', () => { tip.hidden = true; map.setFilter('net-hover', ['==', ['get', 'id'], '']) })
  let mv = 0
  map.on('moveend', () => { clearTimeout(mv); mv = setTimeout(() => { renderCats(); layoutPins() }, 120) })
}

// ---------- controls
// default trip: the one where the RAASTA route (manual wheelchair, first leave time) avoids the most placed barriers
function bestTrip(c) {
  let best = Math.max(0, c.scenarios.findIndex((s) => !s.what_if)), gain = 0
  c.scenarios.forEach((sc, i) => {
    if (sc.what_if) return
    const lt = sc.leave_times?.[0], rs = (sc.routes ?? []).filter((r) => r.profile === 'manual_wheelchair' && (!lt || r.leave_time === lt))
    const sh = rs.find((r) => r.kind === 'shortest'), ra = rs.find((r) => r.kind === 'accessible') ?? rs.find((r) => r.kind === 'least_blocked')
    const g = (sh?.barrier_count ?? 0) - (ra?.barrier_count ?? 0)
    if (g > gain) { gain = g; best = i }
  })
  return best
}
async function setCity(id, { trip = null } = {}) {
  const c = await loadCity(id)
  S.city = c
  if (!c.scenarios) c.scenarios = [{ id: 'trip', name: c.meta?.name ?? id, what_if: false, from: c.routes?.from, to: c.routes?.to, profiles: c.routes?.profiles ?? [], routes: c.routes?.routes ?? [], leave_times: [] }]
  bbox = cityBbox(c)
  S.els = buildElements(c)
  for (const x of S.els) x.inside = x.where !== 'camera' || inBox(x.position, bbox)
  S.outside = S.els.filter((x) => !x.inside).length
  const tIdx = trip != null ? c.scenarios.findIndex((s) => s.id === trip) : -1
  S.sc = tIdx >= 0 ? tIdx : bestTrip(c)
  if (c.scenarios[S.sc]?.what_if) S.whatIf = true
  const profs = (c.scenarios[S.sc].profiles ?? []).map((p) => p.id)
  if (profs.length && !profs.includes(S.profile)) { S.profile = profs[0]; S.leaf = leaves().find((l) => l.profile === S.profile)?.id ?? S.leaf }
  map.getSource('net')?.setData(netFc(c))
  $('.city-sel').value = id
  S.pinned = null; card.hidden = true; showCandidates(null)
  await loadBodyDoc()
  drawRoutes(); placePins(); pushEls(); renderAll(); fitScenario(true); syncUrl()
}
function syncUrl() {
  const u = new URL(location.href)
  u.searchParams.set('city', S.city?.id ?? ''); u.searchParams.set('trip', scen()?.id ?? ''); u.searchParams.set('body', S.leaf ?? '')
  history.replaceState(null, '', u)
}
const shortName = (c) => String(c.name).split(/:| \(|,/)[0].trim()
$('.city-sel').addEventListener('change', (e) => setCity(e.target.value))
$('.p-trip').addEventListener('change', async (e) => {
  if (e.target.matches('.trip-sel')) { S.sc = +e.target.value; S.pinned = null; card.hidden = true; await loadBodyDoc(); drawRoutes(); placePins(); renderRoute(); renderFoot(); fitScenario(true); syncUrl() }
  if (e.target.matches('.wi')) { S.whatIf = e.target.checked; if (!S.whatIf && scen()?.what_if) { S.sc = Math.max(0, S.city.scenarios.findIndex((s) => !s.what_if)); await loadBodyDoc(); drawRoutes(); placePins(); renderRoute(); fitScenario(true) } renderTrip(); pushEls() }
})
$('.p-body').addEventListener('change', (e) => { if (e.target.matches('.ctx-sel')) { S.cond = e.target.value; drawRoutes(); renderRoute(); pushEls(); renderBody(); if (S.pinned) openCard(elById(S.pinned), { x: 0, y: 0 }, true) } })
$('.p-body').addEventListener('click', (e) => {
  const b = e.target.closest('[data-leaf]'); if (!b) return
  S.leaf = b.dataset.leaf; S.profile = leafOf(S.leaf)?.profile ?? S.profile
  drawRoutes(); renderBody(); renderRoute(); pushEls(); syncUrl()
})
$('.p-cats').addEventListener('click', (e) => {
  const b = e.target.closest('[data-cat]'); if (!b) return
  const c = b.dataset.cat; S.hidden.has(c) ? S.hidden.delete(c) : S.hidden.add(c); pushEls()
})
const range = $('.time input'), out = $('.time output')
range.addEventListener('input', () => { S.hour = +range.value; out.textContent = hhmm(S.hour); drawRoutes(false); renderRoute(); pushEls(); renderBody() })
$('.view').addEventListener('click', (e) => {
  const b = e.target.closest('[data-v]'); if (!b) return
  S.view = b.dataset.v
  $('.view').querySelectorAll('button').forEach((x) => x.setAttribute('aria-checked', String(x.dataset.v === S.view)))
  map.setLayoutProperty('bld-3d', 'visibility', S.view === '3d' ? 'visible' : 'none')
  fitScenario(true)
})
const setPanel = (open) => { S.panel = open; document.body.classList.toggle('panel-closed', !open); $('.panel-btn').setAttribute('aria-expanded', String(open)) }
$('.panel-btn').addEventListener('click', () => setPanel(!S.panel))
$('.sheet-handle').addEventListener('click', () => setPanel(!S.panel))
setPanel(S.panel)
onLang(() => { renderAll(); placePins(); drawRoutes(false) })

// ---------- boot
await loadImpact()
S.leaf = q.get('body') && leafOf(q.get('body')) ? q.get('body') : leaves().find((l) => l.profile === S.profile)?.id ?? leaves()[0]?.id
S.profile = leafOf(S.leaf)?.profile ?? S.profile
S.list = await cities()
$('.city-sel').innerHTML = S.list.map((c) => `<option value="${esc(c.id)}">${esc(shortName(c))}${c.mock ? ' (mock)' : ''}${c.records ? ` · ${c.records} records` : ''}</option>`).join('')
const startId = (S.list.find((c) => c.id === q.get('city')) ?? S.list.find((c) => c.id === 'chandigarh') ?? S.list[0])?.id
const ready = async () => {
  await addIcons(map)
  addOurLayers(); wire()
  if (startId) await setCity(startId, { trip: q.get('trip') })
  else $('.p-route').innerHTML = `<p>${tr(L('No city data yet.', 'अभी कोई शहर डेटा नहीं.'))}</p>`
  window.__map2 = { map, S, setCity, openCard, elById, ready: true }
}
// style.load, not load: load waits for tiles, and an offline projector must still get our own layers
let started = false
const go = () => { if (started) return; started = true; ready() }
map.isStyleLoaded() ? go() : (map.once('style.load', go), map.once('load', go))
