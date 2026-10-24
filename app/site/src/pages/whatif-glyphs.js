// pictograms for /what-if. the barrier types /map already draws come from src/map2/icons.js (same badge shapes);
// the taxonomy categories icons.js has no glyph for (weather, light, air, crowds, animals, crossings, rest, ...) are
// drawn here in the same grammar: 64x64 box, round 5 px strokes, ink on paper. codex's art/out/v3/icons set was
// not on disk when this was written (2026-10-25 00:40 IST); when it lands, swap ART below to its file names.
import { glyphSvg, ICON_TYPES } from '../map2/icons.js'

const G = {
  weather: '<path d="M18 36a10 10 0 0 1 2-20 13 13 0 0 1 25 3 9 9 0 0 1 1 17z"/><path d="M22 44l-3 8M33 44l-3 8M44 44l-3 8"/>',
  rain: '<path d="M18 36a10 10 0 0 1 2-20 13 13 0 0 1 25 3 9 9 0 0 1 1 17z"/><path d="M22 44l-3 8M33 44l-3 8M44 44l-3 8"/>',
  heat: '<circle cx="32" cy="32" r="10"/><path d="M32 10v6M32 48v6M10 32h6M48 32h6M16 16l4 4M44 44l4 4M48 16l-4 4M20 44l-4 4"/>',
  fog: '<path d="M12 22h40M16 32h36M12 42h34M20 52h26"/>',
  wind: '<path d="M10 26h30a7 7 0 1 0-7-7M10 36h40a7 7 0 1 1-7 7M10 46h18"/>',
  light_time: '<path d="M40 12a20 20 0 1 0 12 30 16 16 0 0 1-12-30z"/>',
  night: '<path d="M40 12a20 20 0 1 0 12 30 16 16 0 0 1-12-30z"/>',
  lamp: '<path d="M26 54h12M32 54V22M32 22c0-6 4-10 12-10M38 16h12l-3 8h-6z"/><path d="M44 30v4M50 28l3 3"/>',
  glare: '<circle cx="24" cy="26" r="8"/><path d="M24 10v4M24 38v4M8 26h4M36 26h4"/><path d="M30 46l24-10M34 54l20-8"/>',
  air_noise: '<path d="M20 50c-6-6 6-10 0-16s6-10 0-16M32 50c-6-6 6-10 0-16s6-10 0-16M44 50c-6-6 6-10 0-16s6-10 0-16"/>',
  smoke: '<path d="M20 50c-6-6 6-10 0-16s6-10 0-16M32 50c-6-6 6-10 0-16s6-10 0-16M44 50c-6-6 6-10 0-16s6-10 0-16"/>',
  noise: '<path d="M12 26h8l12-10v32L20 38h-8z"/><path d="M40 24c4 4 4 12 0 16M46 18c8 8 8 20 0 28"/>',
  crowd_safety: '<circle cx="20" cy="18" r="5"/><circle cx="44" cy="18" r="5"/><circle cx="32" cy="24" r="5"/><path d="M12 48c0-10 4-16 8-16s8 6 8 16M36 48c0-10 4-16 8-16s8 6 8 16M24 54c0-12 4-18 8-18s8 6 8 18"/>',
  crowd: '<circle cx="20" cy="18" r="5"/><circle cx="44" cy="18" r="5"/><circle cx="32" cy="24" r="5"/><path d="M12 48c0-10 4-16 8-16s8 6 8 16M36 48c0-10 4-16 8-16s8 6 8 16M24 54c0-12 4-18 8-18s8 6 8 18"/>',
  animal: '<path d="M14 36c0-8 6-12 14-12h12l6-6 4 4-2 6v12H20zM20 48v-12M28 48v-12M40 48v-12M48 48v-12"/><circle cx="46" cy="22" r="1.5" fill="currentColor"/>',
  traffic_crossings: '<path d="M14 18v28M24 18v28M34 18v28M44 18v28"/><path d="M50 10l-6 6"/>',
  crossing: '<path d="M14 18v28M24 18v28M34 18v28M44 18v28"/>',
  signal: '<rect x="24" y="8" width="16" height="36" rx="4"/><circle cx="32" cy="18" r="3.5" fill="currentColor"/><circle cx="32" cy="32" r="3.5"/><path d="M32 44v12"/>',
  vehicle: '<path d="M10 40v-8l6-10h24l10 10h4v8z"/><circle cx="20" cy="42" r="4.5"/><circle cx="44" cy="42" r="4.5"/>',
  terrain_transit: '<path d="M10 50l14-22 10 14 8-10 12 18z"/>',
  bus: '<rect x="14" y="12" width="36" height="34" rx="5"/><path d="M14 30h36M22 46v6M42 46v6"/><circle cx="22" cy="38" r="2" fill="currentColor"/><circle cx="42" cy="38" r="2" fill="currentColor"/>',
  amenities: '<path d="M12 34h40M16 34v14M48 34v14M14 26h36"/>',
  bench: '<path d="M12 34h40M16 34v14M48 34v14M14 26h36"/>',
  rest: '<path d="M12 34h40M16 34v14M48 34v14M14 26h36"/>',
  compound: '<path d="M22 14l-8 14h10l-6 14M42 14l-8 14h10l-6 14"/><path d="M12 52h40"/>',
  geometry: '<path d="M10 44h20V26h24"/>',
  surface: '<rect x="13" y="17" width="38" height="30" rx="2"/><path d="M13 32h38M32 17v30M22 17l6 10-5 7 7 13"/>',
  fixed_obstacles: '<path d="M32 14v36M24 50h16M32 14c6 0 10 2 12 6"/>',
  temporary_obstacles: '<path d="M14 46h36M18 46l6-24h16l6 24M22 34h20"/>',
  construction: '<path d="M14 46h36M18 46l6-24h16l6 24M22 34h20"/>',
  overhead: '<path d="M10 18h44l-6 10H16z"/><path d="M32 34v20M26 40l6-6 6 6"/>',
  water: '<path d="M10 30c5-5 9-5 14 0s9 5 14 0 9-5 14 0M10 42c5-5 9-5 14 0s9 5 14 0 9-5 14 0"/>',
  tactile: '<rect x="14" y="14" width="36" height="36" rx="3"/><circle cx="24" cy="24" r="2.5" fill="currentColor"/><circle cx="40" cy="24" r="2.5" fill="currentColor"/><circle cx="24" cy="40" r="2.5" fill="currentColor"/><circle cx="40" cy="40" r="2.5" fill="currentColor"/><circle cx="32" cy="32" r="2.5" fill="currentColor"/>',
  data: '<rect x="14" y="12" width="36" height="40" rx="3"/><path d="M22 24h20M22 32h20M22 40h12"/>',
  route: '<circle cx="18" cy="46" r="5"/><circle cx="46" cy="18" r="5"/><path d="M22 42c10-2 2-14 12-18s8 0 8-2"/>',
}
// codex art set (unused until it exists on disk; keep keys equal to the glyph keys above)
export const ART = {}

const BADGE = (inner, sev, ink = '#111111', paper = '#F3F3F3') => {
  const fg = sev === 'block' ? paper : ink, bg = sev === 'block' ? ink : '#FFFFFF'
  const ring = sev === 'block' ? `<circle cx="40" cy="40" r="34" fill="${ink}" stroke="${paper}" stroke-width="4"/>`
    : sev === 'clear' ? `<rect x="7" y="7" width="66" height="66" rx="14" fill="#FFFFFF" stroke="${ink}" stroke-width="4"/>`
    : `<circle cx="40" cy="40" r="33" fill="#FFFFFF" stroke="${ink}" stroke-width="7"/>`
  return `<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80"><ellipse cx="42" cy="74" rx="20" ry="4" fill="#000" opacity="0.18"/>${ring}<g transform="translate(8 8)" color="${fg}" fill="none" stroke="${fg}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">${inner}</g></svg>`
}

// verdict letter / word -> badge severity (block = solid ink disc, cost/warn = ringed, none = rounded square)
export const sevOf = (v) => (v === 'block' || v === 'B' ? 'block' : v === 'none' || v === 'N' ? 'clear' : 'slow')

export function glyph(key, size = 28, sev = 'slow') {
  if (key && ICON_TYPES.includes(key) && key !== 'other') return glyphSvg(key, size, sev)
  const inner = G[key] ?? G.compound
  return BADGE(inner, sev).replace('width="80" height="80"', `width="${size}" height="${size}" aria-hidden="true" focusable="false"`)
}
