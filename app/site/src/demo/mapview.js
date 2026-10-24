// the live map: MapLibre GL (base) + deck.gl (network evidence, routes, route animation, barriers)
// used by /map (full controls) and /what-if (driven by the buttons)
import * as maplibregl from 'maplibre-gl'
// the worker is a self-contained module; point MapLibre at the copy Vite ships (its default path breaks once bundled)
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
maplibregl.setWorkerUrl(workerUrl)
import 'maplibre-gl/dist/maplibre-gl.css'
import { MapboxOverlay } from '@deck.gl/mapbox'
import { PathLayer, ScatterplotLayer } from '@deck.gl/layers'
import { TripsLayer } from '@deck.gl/geo-layers'
import { PathStyleExtension } from '@deck.gl/extensions'
import { pickRoutes } from '../data/data.js'
import { reduceMotion, getLang } from '../shell/shell.js'

const INK = [18, 18, 18], RED = [200, 41, 36], PAPER = [255, 255, 255]
const PAPER_STYLE = { version: 8, sources: {}, layers: [{ id: 'paper', type: 'background', paint: { 'background-color': '#ffffff' } }] }
const STREETS = 'https://tiles.openfreemap.org/styles/positron'

function cumulative(path) {
  const R = 6371000, out = [0]
  for (let i = 1; i < path.length; i++) {
    const [a, b] = [path[i - 1], path[i]], la = (a[1] + b[1]) / 2 * Math.PI / 180
    const dx = (b[0] - a[0]) * Math.PI / 180 * R * Math.cos(la), dy = (b[1] - a[1]) * Math.PI / 180 * R
    out.push(out[i - 1] + Math.hypot(dx, dy))
  }
  return out
}

export function createMapView(container, { onSelect, basemap = 'paper' } = {}) {
  const map = new maplibregl.Map({ container, style: PAPER_STYLE, center: [75.566, 26.844], zoom: 15.5, attributionControl: { compact: true }, dragRotate: false, pitchWithRotate: false })
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right')
  const overlay = new MapboxOverlay({ interleaved: false, layers: [], getTooltip })
  map.addControl(overlay)
  const state = { city: null, profile: 'manual_wheelchair', hour: 9, selected: null, focus: null, speed: 0.9, routes: { shortest: null, accessible: null } }
  let trips = [], maxT = 1, t0 = performance.now(), raf = 0, markers = []

  function getTooltip({ object, layer }) {
    if (!object || !layer) return null
    const hi = getLang() === 'hi'
    if (layer.id === 'edges') {
      const ev = object.evidence === 'barrier' ? (hi ? 'पक्की रुकावट' : 'known barrier') : object.evidence === 'clear' ? `${hi ? 'साफ़ देखा' : 'known clear'} (${object.observed})` : (hi ? 'अज्ञात' : 'unknown')
      return { text: `${object.road_name ?? object.id}\n${ev}\n${object.source === 'generated' ? (hi ? 'बनाया गया फुटपाथ (OSM में नहीं)' : 'generated sidewalk (not in OSM)') : 'OSM footway'}`, className: 'map-tip' }
    }
    if (layer.id === 'barriers') return { text: `${object.type} · ${object.status}`, className: 'map-tip' }
    return null
  }

  function layers(now) {
    const c = state.city; if (!c) return []
    const sel = state.selected
    const selEdge = sel ? c.edgeById.get(sel.segment_id) : null
    const t = reduceMotion.matches ? maxT : ((now - t0) / 1000 * (maxT / 9)) % (maxT * 1.2)
    return [
      selEdge && new PathLayer({ id: 'sel-seg', data: [selEdge], getPath: (d) => d.path, getColor: [...RED, 110], getWidth: 16, widthUnits: 'pixels', capRounded: true }),
      new PathLayer({ id: 'edges', data: c.edges, pickable: true, getPath: (d) => d.path, widthUnits: 'pixels', capRounded: true,
        getColor: (d) => (d.evidence === 'barrier' ? RED : d.evidence === 'clear' ? INK : [...INK, state.focus === 'unknown' ? 255 : 120]),
        getWidth: (d) => (d.evidence === 'barrier' ? 4 : d.evidence === 'clear' ? 3 : state.focus === 'unknown' ? 5 : 2),
        getDashArray: (d) => (d.evidence === 'unknown' ? [2.5, 2] : [0, 0]), dashJustified: true,
        extensions: [new PathStyleExtension({ dash: true })], updateTriggers: { getColor: state.focus, getWidth: state.focus } }),
      state.routes.shortest && new PathLayer({ id: 'shortest', data: [state.routes.shortest], getPath: (d) => d.path, getColor: [...INK, 70], getWidth: 12, widthUnits: 'pixels', capRounded: true, jointRounded: true }),
      state.routes.accessible && new PathLayer({ id: 'accessible', data: [state.routes.accessible], getPath: (d) => d.path, getColor: [...RED, 120], getWidth: 10, widthUnits: 'pixels', capRounded: true, jointRounded: true }),
      new TripsLayer({ id: 'trips', data: trips, getPath: (d) => d.path, getTimestamps: (d) => d.ts, getColor: (d) => d.color, widthMinPixels: 6, capRounded: true, jointRounded: true,
        trailLength: reduceMotion.matches ? 1e9 : maxT * 0.35, currentTime: t, fadeTrail: true }),
      new ScatterplotLayer({ id: 'clears', data: c.clears, getPosition: (d) => d.position, getRadius: 4, radiusUnits: 'pixels', getFillColor: PAPER, getLineColor: INK, lineWidthUnits: 'pixels', getLineWidth: 2, stroked: true }),
      new ScatterplotLayer({ id: 'barriers', data: c.barriers, pickable: true, getPosition: (d) => d.position, radiusUnits: 'pixels', lineWidthUnits: 'pixels', stroked: true,
        getRadius: (d) => (sel?.id === d.id ? 14 : d.status === 'REJECT' ? 6 : 9),
        getFillColor: (d) => (d.status === 'ACCEPT' ? RED : PAPER), getLineColor: (d) => (d.status === 'REJECT' ? INK : d.status === 'ABSTAIN' ? RED : INK),
        getLineWidth: (d) => (sel?.id === d.id ? 4 : 2.5), updateTriggers: { getRadius: sel?.id, getLineWidth: sel?.id },
        onClick: ({ object }) => { select(object?.id); return true } }),
    ].filter(Boolean)
  }
  const draw = () => overlay.setProps({ layers: layers(performance.now()) })
  function loop() { draw(); raf = reduceMotion.matches ? 0 : requestAnimationFrame(loop) }

  function setRoutes() {
    const c = state.city; if (!c) return
    state.routes = pickRoutes(c, state.profile, state.hour)
    const prof = (c.routes.profiles ?? []).find((p) => p.id === state.profile)
    state.speed = prof?.speed_mps ?? 0.9
    trips = [state.routes.shortest && { r: state.routes.shortest, color: INK }, state.routes.accessible && { r: state.routes.accessible, color: RED }].filter(Boolean)
      .map(({ r, color }) => ({ path: r.path, ts: cumulative(r.path).map((m) => m / state.speed), color }))
    maxT = Math.max(1, ...trips.map((x) => x.ts.at(-1)))
    t0 = performance.now()
    if (!raf) loop()
  }
  function select(id) {
    const b = state.city?.barriers.find((x) => x.id === id) ?? null
    state.selected = b; draw()
    if (b) map.easeTo({ center: b.position, zoom: Math.max(map.getZoom(), 16.6), duration: reduceMotion.matches ? 0 : 700 })
    onSelect?.(b)
  }
  function fit() {
    const c = state.city; if (!c?.edges.length) return
    let [x0, y0, x1, y1] = [180, 90, -180, -90]
    for (const e of c.edges) for (const [x, y] of e.path) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y) }
    map.fitBounds([[x0, y0], [x1, y1]], { padding: 48, duration: 0 })
  }
  function placeMarkers() {
    markers.forEach((m) => m.remove()); markers = []
    const r = state.city?.routes
    for (const [k, end] of [['from', r?.from], ['to', r?.to]]) {
      if (!end?.lnglat) continue
      const el = Object.assign(document.createElement('div'), { className: `map-pin ${k}`, textContent: `${k === 'from' ? (getLang() === 'hi' ? 'से' : 'from') : (getLang() === 'hi' ? 'तक' : 'to')}: ${end.label}` })
      markers.push(new maplibregl.Marker({ element: el, anchor: 'bottom' }).setLngLat(end.lnglat).addTo(map))
    }
  }

  return {
    map,
    state,
    async setCity(city) {
      state.city = city; state.selected = null
      if (city.scenarios?.length) city.routes = city.scenarios[0]
      const ids = (city.routes.profiles ?? []).map((p) => p.id)
      if (ids.length && !ids.includes(state.profile)) state.profile = ids[0]
      fit(); placeMarkers(); setRoutes(); draw()
    },
    setScenario(i) { const c = state.city; if (!c?.scenarios?.[i]) return; c.routes = c.scenarios[i]; placeMarkers(); setRoutes(); draw() },
    setProfile(p) { state.profile = p; setRoutes() },
    setHour(h) { state.hour = h; setRoutes() },
    setFocus(f) { state.focus = f; draw() },
    select,
    // a record that is not in the city's barrier list (an /analyze answer): highlight its segment
    selectObject(b) {
      state.selected = b; draw()
      const e = b && state.city?.edgeById.get(b.segment_id)
      const at = b?.position ?? (e ? e.path[Math.floor(e.path.length / 2)] : null)
      if (at) map.easeTo({ center: at, zoom: Math.max(map.getZoom(), 16.6), duration: reduceMotion.matches ? 0 : 700 })
    },
    replay() { t0 = performance.now(); if (!raf) loop() },
    async setBasemap(kind) {
      if (kind !== 'streets') { map.setStyle(PAPER_STYLE); return 'paper' }
      try {
        const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 4000)
        const res = await fetch(STREETS, { signal: ctl.signal }); clearTimeout(timer)
        if (!res.ok) throw new Error(res.status)
        map.setStyle(await res.json()); return 'streets'
      } catch (e) { console.warn('base map offline, paper used:', e.message); map.setStyle(PAPER_STYLE); return 'paper' }
    },
    lang() { placeMarkers() },
  }
}
