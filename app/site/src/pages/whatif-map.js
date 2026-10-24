// the "run on the map" panel for /what-if. loaded with a dynamic import the first time a reader presses the button,
// so maplibre (about 1 MB) never costs a phone that only reads the questions.
// draws: route without the what-if (ink, dashed, offset 7 px to one side so it stays visible where both routes share a street), route with it (red, on top), the injected element(s) as badges,
// start and end pins. same base style as /map (src/map2/style.js, santioni ink on paper).
import * as maplibregl from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import 'maplibre-gl/dist/maplibre-gl.css'
import { baseStyle, labelLayers, INK, RED, PAPER } from '../map2/style.js'
import { glyph, sevOf } from './whatif-glyphs.js'
import { esc } from './common.js'

maplibregl.setWorkerUrl(workerUrl)

const empty = { type: 'FeatureCollection', features: [] }
const line = (coords) => (coords?.length > 1 ? { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: coords } } : null)

export function createWhatifMap(container) {
  const map = new maplibregl.Map({ container, style: baseStyle(), center: [75.825, 26.92], zoom: 15, pitch: 0, attributionControl: { compact: true },
    cooperativeGestures: matchMedia('(pointer: coarse)').matches })
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-left')
  map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-right')
  let markers = []
  const ready = new Promise((res) => map.on('load', () => {
    map.addSource('base', { type: 'geojson', data: empty })
    map.addSource('wi', { type: 'geojson', data: empty })
    map.addLayer({ id: 'base-case', type: 'line', source: 'base', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': PAPER, 'line-width': 9, 'line-offset': -7 } })
    map.addLayer({ id: 'base', type: 'line', source: 'base', layout: { 'line-cap': 'butt', 'line-join': 'round' }, paint: { 'line-color': INK, 'line-width': 4, 'line-dasharray': [1.6, 1.1], 'line-offset': -7 } })
    map.addSource('span', { type: 'geojson', data: empty })
    map.addLayer({ id: 'wi-case', type: 'line', source: 'wi', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': PAPER, 'line-width': 11, 'line-opacity': 0.9 } })
    map.addLayer({ id: 'wi', type: 'line', source: 'wi', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': RED, 'line-width': 6 } })
    map.addLayer({ id: 'span', type: 'circle', source: 'span', paint: { 'circle-radius': 6, 'circle-color': PAPER, 'circle-stroke-color': INK, 'circle-stroke-width': 3 } })
    // phones: shop and clinic names turn the small map into confetti; keep streets and major places only
    for (const l of labelLayers()) map.addLayer(container.clientWidth < 600 && l.id === 'lbl-poi-minor' ? { ...l, layout: { ...l.layout, visibility: 'none' } } : l)
    res()
  }))
  // tiles that fail must not leave a blank panel: our own layers draw on the paper ground anyway
  map.on('error', (e) => console.warn('whatif map', e?.error?.message ?? e))

  async function show(run, bodyId, { fit = true } = {}) {
    await ready
    const v = run.variants?.[bodyId] ?? run.variants?.[run.body]
    const g = (k) => (k ? run.geoms?.[k] : null)
    const base = line(g(v?.base?.geom)), wi = line(g(v?.whatif?.geom))
    map.getSource('base').setData(base ? { type: 'FeatureCollection', features: [base] } : empty)
    map.getSource('wi').setData(wi ? { type: 'FeatureCollection', features: [wi] } : empty)
    const span = (run.span_points ?? []).length > 1 ? run.span_points : []
    map.getSource('span').setData({ type: 'FeatureCollection', features: span.map((c) => ({ type: 'Feature', properties: {}, geometry: { type: 'Point', coordinates: c } })) })
    for (const m of markers) m.remove()
    markers = []
    const pin = (ll, txt, cls) => {
      const el = Object.assign(document.createElement('div'), { className: `map-pin ${cls}`, textContent: txt })
      markers.push(new maplibregl.Marker({ element: el, anchor: 'bottom', offset: [0, -4] }).setLngLat(ll).addTo(map))
    }
    const first = (wi ?? base)?.geometry.coordinates
    if (first) { pin(first[0], 'from', 'from'); pin(first.at(-1), 'to', 'to') }
    else if (run.scenario?.start) { pin([run.scenario.start.lon, run.scenario.start.lat], 'from', 'from'); pin([run.scenario.end.lon, run.scenario.end.lat], 'to', 'to') }
    const ev = Object.fromEntries((v?.element_verdicts ?? []).map((x) => [x.element, x.verdict]))
    const seen = new Map()
    for (const x of run.injected ?? []) {
      if (x.lon == null || x.lat == null) continue
      const key = `${x.lon.toFixed(5)},${x.lat.toFixed(5)}`
      const n = seen.get(key) ?? 0
      seen.set(key, n + 1)
      if (n > 3) continue // a long stretch is many records on one spot list; four badges say it
      const el = document.createElement('div')
      el.className = 'wi-mk'
      el.innerHTML = glyph(x.glyph, 46, sevOf(ev[x.element] ?? v?.verdict))
      el.title = x.name ?? x.element
      el.setAttribute('role', 'img'); el.setAttribute('aria-label', esc(x.name ?? x.element))
      markers.push(new maplibregl.Marker({ element: el, anchor: 'center', offset: [n * 18, -n * 18] }).setLngLat([x.lon, x.lat]).addTo(map))
    }
    if (fit) {
      const pts = [...(base?.geometry.coordinates ?? []), ...(wi?.geometry.coordinates ?? []), ...(run.injected ?? []).filter((x) => x.lon != null).map((x) => [x.lon, x.lat]), ...span]
      if (pts.length) {
        const b = pts.reduce((bb, p) => bb.extend(p), new maplibregl.LngLatBounds(pts[0], pts[0]))
        const narrow = container.clientWidth < 600
        map.fitBounds(b, { padding: narrow ? { top: 50, bottom: 40, left: 30, right: 30 } : 70, maxZoom: 17.5, duration: matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 700 })
      }
    }
  }
  return { map, show, resize: () => map.resize() }
}
