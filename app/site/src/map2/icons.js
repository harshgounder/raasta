// ink pictograms per element category. This SVG set is the production icon set: it is resolution free,
// inherits the ink and paper tokens, and covers every element through its glyph field. Codex's raster
// set was never delivered, so nothing waits on it.
// every glyph is drawn in a 64x64 box with round strokes; badge() wraps it in the severity shape:
//   block  = solid ink disc, paper glyph          slow = paper disc, thick ink ring, ink glyph
//   warn   = same as slow (drawn smaller by the map)   unsure = paper disc, dashed ring, "?" tag (ABSTAIN)
//   clear  = paper rounded square, ink glyph (positive evidence: seen and fine, on that date only)
const G = {
  pole_obstruction: '<path d="M32 14v36M24 50h16M32 14c6 0 10 2 12 6"/><circle cx="45" cy="22" r="3" fill="currentColor"/>',
  parked_vehicle: '<path d="M12 40v-7l5-9h22l8 9h5v7z"/><circle cx="21" cy="42" r="4.5" fill="var(--bg)"/><circle cx="44" cy="42" r="4.5" fill="var(--bg)"/><path d="M20 32l3-5h13l4 5"/>',
  broken_footpath: '<rect x="13" y="17" width="38" height="30" rx="2"/><path d="M13 32h38M32 17v30M22 17l6 10-5 7 7 13"/>',
  missing_kerb_ramp: '<path d="M10 44h20V26h24"/><path d="M38 40l10 -10M38 30l10 10"/>',
  kerb_ramp_present: '<path d="M10 44h44V26L28 44"/>',
  steps: '<path d="M12 48h10v-9h10v-9h10v-9h10"/>',
  pothole: '<ellipse cx="32" cy="38" rx="19" ry="8"/><path d="M22 37c4-3 16-3 20 0"/><path d="M20 22l4 6M32 18v8M44 22l-4 6"/>',
  vendor: '<path d="M16 24h32l-4-8H20z"/><path d="M20 24v14h24V24"/><path d="M14 38h36"/><circle cx="22" cy="44" r="4"/><circle cx="42" cy="44" r="4"/>',
  missing_footpath: '<path d="M22 44c-4 0-5-6-4-11s4-7 6-6 1 7 0 10 0 7-2 7zM40 36c-4 0-5-6-4-11s4-7 6-6 1 7 0 10 0 7-2 7z"/><path d="M12 52L52 12"/>',
  open_drain: '<rect x="12" y="20" width="40" height="24" rx="2"/><path d="M20 20v24M28 20v24M36 20v24M44 20v24"/>',
  waterlogging: '<path d="M10 30c5-5 9-5 14 0s9 5 14 0 9-5 14 0M10 42c5-5 9-5 14 0s9 5 14 0 9-5 14 0"/>',
  steep_slope: '<path d="M10 46h44V20z"/><path d="M22 34l6 0"/>',
  crossing_marked: '<path d="M14 18v28M24 18v28M34 18v28M44 18v28"/>',
  clear: '<path d="M16 33l10 10 22-22"/>',
  other: '<path d="M32 12l20 20-20 20-20-20z"/><path d="M32 24v10"/><circle cx="32" cy="41" r="2" fill="currentColor"/>',
}
export const ICON_TYPES = Object.keys(G)
export const glyphKey = (type) => (G[type] ? type : 'other')

function badge(type, sev, ink = '#111111', paper = '#F3F3F3') {
  const g = G[glyphKey(type)]
  const fg = sev === 'block' ? paper : ink, bg = sev === 'block' ? ink : '#FFFFFF'
  const ring = sev === 'block' ? `<circle cx="40" cy="40" r="34" fill="${ink}" stroke="${paper}" stroke-width="4"/>`
    : sev === 'unsure' ? `<circle cx="40" cy="40" r="33" fill="#FFFFFF" stroke="${ink}" stroke-width="5" stroke-dasharray="9 6"/>`
    : sev === 'clear' ? `<rect x="7" y="7" width="66" height="66" rx="14" fill="#FFFFFF" stroke="${ink}" stroke-width="4"/>`
    : `<circle cx="40" cy="40" r="33" fill="#FFFFFF" stroke="${ink}" stroke-width="7"/>`
  const tag = sev === 'unsure' ? `<g><circle cx="64" cy="16" r="13" fill="${ink}"/><text x="64" y="22" font-family="Arial, sans-serif" font-weight="900" font-size="18" text-anchor="middle" fill="#FFFFFF">?</text></g>` : ''
  const op = sev === 'unsure' ? 0.7 : 1
  return `<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80">
    <ellipse cx="42" cy="74" rx="20" ry="4" fill="#000" opacity="0.18"/>${ring}
    <g transform="translate(8 8)" style="--bg:${bg}" color="${fg}" fill="none" stroke="${fg}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="${op}">${g.replaceAll('var(--bg)', bg)}</g>${tag}</svg>`
}
// a plain glyph for DOM use (legend, filters, cards)
export function glyphSvg(type, size = 28, sev = 'slow') {
  return badge(type, sev).replace('width="80" height="80"', `width="${size}" height="${size}" aria-hidden="true" focusable="false"`)
}
export const SEVS = ['block', 'slow', 'warn', 'unsure', 'clear']
export const iconId = (type, sev) => `el-${glyphKey(type)}-${sev === 'warn' ? 'slow' : sev}`

// register every type x severity as a MapLibre image (rasterised at 2x for crisp edges on projectors)
export async function addIcons(map) {
  const jobs = []
  for (const type of ICON_TYPES) for (const sev of ['block', 'slow', 'unsure', 'clear']) {
    const id = `el-${type}-${sev}`
    if (map.hasImage(id)) continue
    const img = new Image(160, 160)
    const svg = badge(type, sev).replace('width="80" height="80"', 'width="160" height="160"')
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg)
    jobs.push(img.decode().then(() => { if (!map.hasImage(id)) map.addImage(id, img, { pixelRatio: 2 }) }).catch((e) => console.warn('icon', id, e.message)))
  }
  await Promise.all(jobs)
}
