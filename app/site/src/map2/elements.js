// every element in a city (placed barriers, ABSTAIN records, positive evidence, OSM-tag evidence on segments)
// turned into map points that sit ON the footpath segment they belong to.
// placement rules (why the v1 blobs floated off the lines: v1 drew record.lat/lon, which is the CAMERA position
// for photo records, and many detections share one photo, so they piled up in one spot):
//   ACCEPT + segment_id      -> the point at at_m along that segment (from the placement's candidate list), else its middle
//   ABSTAIN with candidates  -> hollow icon at the best candidate's at_m on that segment; hover lists all candidates
//   ABSTAIN, no candidate    -> hollow icon at the camera position ("photo taken outside this footpath network")
//   OSM-tag evidence         -> the middle of the tagged segment
// co-located points (one photo can carry 10+ detections) get a fan offset in screen pixels so every icon shows.

const R = 6371000
const toXY = ([lng, lat], lat0) => [lng * Math.PI / 180 * R * Math.cos(lat0 * Math.PI / 180), lat * Math.PI / 180 * R]
export function pointAlong(path, m) {
  if (!path?.length) return null
  if (path.length === 1 || m == null) return path[Math.floor(path.length / 2)]
  const lat0 = path[0][1]
  let acc = 0
  for (let i = 1; i < path.length; i++) {
    const a = toXY(path[i - 1], lat0), b = toXY(path[i], lat0), d = Math.hypot(b[0] - a[0], b[1] - a[1])
    if (acc + d >= m || i === path.length - 1) {
      const k = d ? Math.min(1, Math.max(0, (m - acc) / d)) : 0
      return [path[i - 1][0] + (path[i][0] - path[i - 1][0]) * k, path[i - 1][1] + (path[i][1] - path[i - 1][1]) * k]
    }
    acc += d
  }
  return path.at(-1)
}
const lengthOf = (path) => { let s = 0; const lat0 = path[0][1]; for (let i = 1; i < path.length; i++) { const a = toXY(path[i - 1], lat0), b = toXY(path[i], lat0); s += Math.hypot(b[0] - a[0], b[1] - a[1]) } return s }
const mid = (path) => pointAlong(path, lengthOf(path) / 2)

export const CATEGORY = {
  parked_vehicle: 'vehicles', vendor: 'vendors', pole_obstruction: 'poles', broken_footpath: 'surface', pothole: 'surface',
  missing_footpath: 'surface', open_drain: 'surface', waterlogging: 'surface', missing_kerb_ramp: 'kerbs', steps: 'kerbs',
  steep_slope: 'kerbs', kerb_ramp_present: 'seen fine', crossing_marked: 'seen fine', clear: 'seen fine',
}
export const CATEGORY_LABEL = {
  vehicles: { en: 'parked vehicles', hi: 'खड़ी गाड़ियाँ' }, vendors: { en: 'vendors and carts', hi: 'ठेले' }, poles: { en: 'poles', hi: 'खंभे' },
  surface: { en: 'broken surface, potholes, drains', hi: 'टूटी सतह, गड्ढे, नाली' }, kerbs: { en: 'kerbs, steps, slopes', hi: 'कर्ब, सीढ़ियाँ, ढलान' },
  'seen fine': { en: 'seen fine (ramp, crossing)', hi: 'ठीक देखा (रैंप, क्रॉसिंग)' }, other: { en: 'other', hi: 'अन्य' },
}
export const NAME = {
  pole_obstruction: { en: 'pole in the footpath', hi: 'रास्ते में खंभा' }, parked_vehicle: { en: 'vehicle on the footpath', hi: 'फुटपाथ पर गाड़ी' },
  broken_footpath: { en: 'broken footpath', hi: 'टूटा फुटपाथ' }, missing_kerb_ramp: { en: 'kerb with no ramp', hi: 'रैंप नहीं' },
  kerb_ramp_present: { en: 'kerb ramp', hi: 'रैंप है' }, steps: { en: 'steps', hi: 'सीढ़ियाँ' }, pothole: { en: 'pothole', hi: 'गड्ढा' },
  vendor: { en: 'vendor or cart on the footpath', hi: 'फुटपाथ पर ठेला' }, missing_footpath: { en: 'no footpath', hi: 'फुटपाथ ही नहीं' },
  open_drain: { en: 'open drain', hi: 'खुली नाली' }, waterlogging: { en: 'standing water', hi: 'पानी भरा' }, steep_slope: { en: 'steep slope', hi: 'खड़ी ढलान' },
  crossing_marked: { en: 'marked crossing', hi: 'ज़ेबरा क्रॉसिंग' }, clear: { en: 'seen clear', hi: 'साफ़ देखा' },
}
const TYPE_BACK = { pole: 'pole_obstruction', missing_ramp: 'missing_kerb_ramp' }
const POSITIVE = new Set(['kerb_ramp_present', 'crossing_marked', 'clear'])
const OSM_TYPE = (e) => {
  const t = String(e.type ?? '')
  if (/step/.test(t)) return 'steps'
  if (/surface|smooth/.test(t)) return 'broken_footpath'
  if (/incline|slope/.test(t)) return 'steep_slope'
  if (/kerb/.test(t)) return 'missing_kerb_ramp'
  if (/sidewalk/.test(t)) return 'missing_footpath'
  return t || 'other'
}

// icon-offset per slot in icon units (the map multiplies by icon-size); slot 0 = no offset
export function fanOffset(slot) {
  if (!slot) return [0, 0]
  let ring = 1, left = slot - 1, cap = 6
  while (left >= cap) { left -= cap; ring++; cap = 6 * ring }
  const a = (left / cap) * Math.PI * 2 - Math.PI / 2 + (ring % 2 ? 0 : Math.PI / cap)
  return [Math.round(Math.cos(a) * 84 * ring), Math.round(Math.sin(a) * 84 * ring)]
}
// MapLibre cannot build an array from feature numbers, so icon-offset is a match over slot numbers
export const fanExpr = () => { const e = ['match', ['get', 'slot']]; for (let i = 1; i <= 120; i++) e.push(i, ['literal', fanOffset(i)]); e.push(['literal', [0, 0]]); return e }

export function buildElements(city) {
  const out = []
  const seg = (id) => city.edgeById.get(id)
  const atOn = (segment_id, cands) => {
    const e = seg(segment_id); if (!e) return null
    const c = (cands ?? []).find((x) => x.segment_id === segment_id)
    return c?.at_m != null ? pointAlong(e.path, c.at_m) : mid(e.path)
  }
  const fromPlacement = (b, positive) => {
    const pl = b.raw ?? {}, rec = pl.record ?? {}
    const type = TYPE_BACK[b.type] ?? pl.type ?? b.type
    const cands = pl.candidates ?? []
    const status = pl.status ?? b.status ?? 'ABSTAIN'
    let pos = null, where = 'segment'
    if (status === 'ACCEPT' && pl.segment_id) pos = atOn(pl.segment_id, cands)
    else if (cands.length) { pos = atOn(cands[0].segment_id, cands); where = 'best-candidate' }
    if (!pos) { pos = b.position ?? (rec.lon != null ? [rec.lon, rec.lat] : null); where = 'camera' }
    if (!pos) return
    const photo = pl.evidence_photo ?? rec.photo ?? null
    out.push({
      id: b.id ?? pl.record_id, type, status, positive, where, position: pos,
      segment_id: status === 'ACCEPT' ? pl.segment_id : null,
      candidates: cands.slice(0, 5).map((c) => ({ segment_id: c.segment_id, p: c.p, distance_m: c.distance_m, side: c.side, kind: c.kind, road: c.road })),
      p: pl.p ?? null, reason: pl.reason ?? null, confidence: rec.confidence ?? b.confidence ?? null,
      observed: rec.observed_at ?? b.observed ?? null, label: rec.label ?? b.label ?? null, source: rec.source ?? b.origin ?? null,
      photo: photo?.url ? { url: photo.url, crop: photo.crop ?? rec.photo?.crop ?? null, annotated: !!photo.annotated } : null,
      credit: photo?.credit ?? rec.ref ?? rec.label ?? null, source_url: photo?.source_url ?? rec.source_url ?? b.source_url ?? null,
      licence: photo?.licence ?? rec.licence ?? null, height_cm: rec.height_cm ?? null, permanence: rec.permanence ?? null,
      gps_error_m: rec.gps_error_m ?? null, what_if: /what_if/.test(rec.source ?? ''),
    })
  }
  for (const b of city.barriers ?? []) fromPlacement(b, false)
  for (const c of city.clears ?? []) fromPlacement({ ...c, type: c.raw?.type ?? 'clear', status: c.raw?.status ?? 'ACCEPT' }, true)
  // OSM-tag evidence riding on segments (steps, bad surface, incline, kerb tags)
  const seen = new Set(out.map((x) => x.id))
  for (const e of city.edges ?? []) for (const ev of e.raw ?? []) {
    if ((ev.source ?? '') !== 'osm_tag') continue
    const id = ev.id ?? `osm#${e.id}#${ev.type}`
    if (seen.has(id)) continue
    seen.add(id)
    const type = OSM_TYPE(ev)
    out.push({ id, type, status: 'ACCEPT', positive: POSITIVE.has(type), where: 'segment', position: mid(e.path), segment_id: e.id, candidates: [],
      p: null, reason: null, confidence: ev.confidence ?? null, observed: ev.observed_at ?? null, label: ev.label ?? `OSM tag: ${ev.type}`, source: 'osm_tag',
      photo: null, credit: 'OpenStreetMap contributors, ODbL', source_url: e.osm_way ? `https://www.openstreetmap.org/way/${e.osm_way}` : 'https://www.openstreetmap.org', licence: 'ODbL', osm: true })
  }
  // fan out co-located points (rounded to ~3 m) so a photo with 13 detections shows 13 icons
  const groups = new Map()
  for (const x of out) { const k = `${x.position[0].toFixed(5)},${x.position[1].toFixed(5)}`; (groups.get(k) ?? groups.set(k, []).get(k)).push(x) }
  for (const g of groups.values()) {
    g.forEach((x, i) => {
      x.stack = g.length
      if (g.length === 1) { x.slot = 0; x.fan = [0, 0]; return }
      // slot i -> a fixed offset (ring 1 holds 6, ring 2 holds 12, ...); the map turns slot into icon-offset (fanOffset)
      x.slot = i + 1; x.fan = fanOffset(i + 1)
    })
  }
  return out
}
