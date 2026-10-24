// story v2 characters: 2.5D planes. Each one starts as a clean ink silhouette drawn on a canvas (placeholder) and
// swaps itself for the painted cut-out at /art/v3/chars/<name>.png the moment that file exists (re-checked every few
// seconds, so files can land while the page is open). Painted files are cropped to their alpha box on load, so the
// plane's bottom edge is the feet. Planes are anchored at the feet (bottom centre).
// facing: setFlip(+1) = face right. Placeholders are drawn facing right; painted files declare their own facing in
// REAL_FACING (the painted cat faces left).
import * as THREE from 'three'

const INK = '#151515', PAPER = '#f3f3f3'
const BASE = `${import.meta.env.BASE_URL}art/v3/chars/`
const REAL_FACING = { cat_walk_a: -1, cat_walk_b: -1, dadaji_kid: -1, kamla_walker: -1, guy_kabir: -1 }

// --- placeholder drawings: thick round strokes (limbs) + filled shapes, paper rim behind, so they read on ink art -
function canvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'); x.lineCap = 'round'; x.lineJoin = 'round'; return [c, x] }
// parts: [{ k: 'line', pts: [[x,y],...], w }, { k: 'ell', x, y, rx, ry, a }, { k: 'poly', pts }]
function draw(x, parts) {
  for (const pass of [0, 1]) {
    x.strokeStyle = x.fillStyle = pass ? INK : PAPER
    for (const p of parts) {
      const extra = pass ? 0 : 12
      x.beginPath()
      if (p.k === 'line') { p.pts.forEach(([a, b], i) => (i ? x.lineTo(a, b) : x.moveTo(a, b))); x.lineWidth = p.w + extra; x.stroke() }
      else if (p.k === 'ell') { x.ellipse(p.x, p.y, p.rx + extra / 2, p.ry + extra / 2, p.a ?? 0, 0, Math.PI * 2); x.fill() }
      else if (p.k === 'poly') { p.pts.forEach(([a, b], i) => (i ? x.lineTo(a, b) : x.moveTo(a, b))); x.closePath(); x.fill(); if (!pass) { x.lineWidth = extra; x.stroke() } }
    }
  }
}
const L = (pts, w) => ({ k: 'line', pts, w }), E = (x, y, rx, ry, a) => ({ k: 'ell', x, y, rx, ry, a }), PG = (pts) => ({ k: 'poly', pts })

function cat(pose) {
  const [c, x] = canvas(520, 340)
  const s = pose === 'b' ? 1 : -1
  draw(x, [
    L([[150, 175], [100, 150], [92, 95], [112, 70]], 16),                                   // tail
    E(255, 190, 118, 50, -0.04),                                                            // body
    L([[180 + 14 * s, 205], [172 + 26 * s, 305]], 22), L([[214 - 14 * s, 210], [222 - 26 * s, 305]], 22),
    L([[300 + 14 * s, 205], [306 + 24 * s, 305]], 22), L([[336 - 14 * s, 205], [348 - 24 * s, 305]], 22),
    E(392, 142, 50, 44), PG([[360, 120], [366, 70], [396, 104]]), PG([[404, 102], [434, 70], [438, 124]]),
  ])
  x.fillStyle = PAPER; x.beginPath(); x.ellipse(410, 136, 7, 9, 0, 0, Math.PI * 2); x.fill()
  return c
}
function myna(up) {
  const [c, x] = canvas(520, 380)
  draw(x, [
    PG([[180, 212], [90, 252], [104, 226], [80, 224], [180, 198]]),
    E(258, 204, 86, 44, -0.18), E(334, 164, 36, 32),
    PG([[362, 156], [404, 166], [362, 176]]),
    up ? PG([[222, 186], [180, 80], [86, 26], [168, 120], [290, 196]]) : PG([[222, 210], [190, 300], [110, 350], [190, 260], [292, 206]]),
    up ? PG([[256, 182], [292, 70], [372, 22], [316, 120], [296, 192]]) : PG([[256, 214], [276, 300], [330, 356], [312, 270], [298, 210]]),
  ])
  x.fillStyle = PAPER; x.beginPath(); x.arc(342, 158, 6, 0, Math.PI * 2); x.fill()
  return c
}
// a standing / walking human: cx = hip x, foot = ground y, h = full height, lean, step phase (-1..1), extra parts
function human(x, cx, foot, h, { lean = 0, step = 0.6, stick = false, buds = false, bag = false, arm = null, dupatta = false } = {}) {
  // proportions: head 1/8, shoulders 0.82 h, hips 0.5 h; lean shifts the upper body forward
  const u = h / 100, ln = lean * 14 * u
  const sh = [cx + ln, foot - 81 * u], hp = [cx, foot - 49 * u]
  const head = [cx + ln * 1.25, foot - 92 * u]
  const lf = [hp[0] - 13 * u * step, foot - 1.5 * u], rf = [hp[0] + 13 * u * step, foot - 1.5 * u]
  const parts = [
    L([[hp[0] - 4 * u, hp[1]], [hp[0] - 4 * u - 6 * u * step, foot - 25 * u], lf], 8.5 * u),
    L([[hp[0] + 4 * u, hp[1]], [hp[0] + 4 * u + 6 * u * step, foot - 25 * u], rf], 8.5 * u),
    L([[lf[0] - 1 * u, lf[1]], [lf[0] + 6 * u, lf[1]]], 5 * u), L([[rf[0] - 1 * u, rf[1]], [rf[0] + 6 * u, rf[1]]], 5 * u),
    PG([[sh[0] - 12 * u, sh[1]], [sh[0] + 12 * u, sh[1]], [hp[0] + 10 * u, hp[1] + 2 * u], [hp[0] - 10 * u, hp[1] + 2 * u]]),
    E(sh[0] - 6 * u, sh[1] + 2 * u, 6 * u, 4 * u), E(sh[0] + 6 * u, sh[1] + 2 * u, 6 * u, 4 * u),
    L([[sh[0], sh[1]], [head[0], head[1] + 6 * u]], 5 * u),
    E(head[0], head[1], 7 * u, 8 * u),
    L(arm ?? [[sh[0] + 9 * u, sh[1] + 2 * u], [sh[0] + 13 * u, sh[1] + 19 * u], [sh[0] + 14 * u, sh[1] + 34 * u]], 5.5 * u),
    L([[sh[0] - 9 * u, sh[1] + 2 * u], [sh[0] - 13 * u, sh[1] + 19 * u], [sh[0] - 12 * u, sh[1] + 33 * u]], 5.5 * u),
  ]
  if (stick) parts.push(L([[sh[0] + 14 * u, sh[1] + 33 * u], [sh[0] + 22 * u, foot]], 3 * u))
  if (bag) parts.push(E(hp[0] - 12 * u, hp[1] - 12 * u, 6 * u, 9 * u))
  if (dupatta) parts.push(PG([[head[0] - 9 * u, head[1] - 4 * u], [head[0] + 6 * u, head[1] - 9 * u], [sh[0] - 4 * u, sh[1] + 30 * u], [sh[0] - 16 * u, sh[1] + 24 * u]]))
  draw(x, parts)
  if (buds) { x.fillStyle = PAPER; x.beginPath(); x.arc(head[0] + 3 * u, head[1], 1.8 * u, 0, Math.PI * 2); x.fill() }
}
function kabir() { const [c, x] = canvas(300, 700); human(x, 140, 690, 670, { step: 1, buds: true, bag: true }); return c }
function kamla() {
  const [c, x] = canvas(460, 640); human(x, 170, 630, 560, { lean: 1.4, step: 0.3, dupatta: true, arm: [[250, 180], [300, 260], [326, 326]] })
  draw(x, [L([[318, 326], [430, 326]], 12), L([[324, 326], [318, 628]], 10), L([[424, 326], [432, 628]], 10)])
  return c
}
function dadajiKid() {
  const [c, x] = canvas(560, 700)
  human(x, 210, 690, 640, { lean: 0.5, step: 0.5 })
  human(x, 410, 690, 380, { step: 0.7, arm: [[402, 388], [374, 394], [348, 386]] })     // the kid holds Dadu's hand
  return c
}
function zoya() {
  const [c, x] = canvas(520, 560)
  draw(x, [E(250, 430, 120, 120)])
  x.fillStyle = PAPER; x.beginPath(); x.arc(250, 430, 96, 0, Math.PI * 2); x.fill()
  draw(x, [L([[250, 430], [250, 430]], 30), L([[380, 520], [420, 520]], 50), L([[180, 160], [196, 330], [330, 330]], 14),
    L([[240, 190], [250, 320]], 70), E(258, 110, 40, 46), L([[260, 320], [360, 330], [376, 450], [400, 452]], 34), L([[262, 200], [300, 300], [300, 380]], 22)])
  return c
}
function scooter() {
  const [c, x] = canvas(700, 380)
  x.strokeStyle = INK; x.lineWidth = 8; x.lineCap = 'round'
  for (const [y, l] of [[110, 120], [170, 170], [230, 140], [290, 90]]) { x.beginPath(); x.moveTo(600, y); x.lineTo(600 + l * 0.6, y); x.stroke() }
  draw(x, [E(170, 300, 58, 58), E(490, 300, 58, 58), PG([[110, 260], [260, 210], [420, 214], [455, 120], [490, 118], [470, 262], [110, 282]]),
    L([[300, 210], [320, 120], [350, 70]], 46), E(352, 44, 36, 36), L([[340, 110], [460, 130]], 18)])
  return c
}
function cart(withVendor) {
  const [c, x] = canvas(720, 520)
  draw(x, [PG([[200, 200], [620, 200], [600, 380], [220, 380]]), L([[230, 200], [230, 70]], 10), L([[600, 200], [600, 70]], 10), PG([[190, 40], [640, 40], [660, 80], [170, 80]])])
  if (withVendor) human(x, 110, 510, 470, { lean: 1.6, step: 0.8, arm: [[218, 134], [236, 180], [214, 206]] })
  return c
}
function wheel() {
  const [c, x] = canvas(200, 200)
  draw(x, [E(100, 100, 86, 86)])
  x.strokeStyle = PAPER; x.lineWidth = 8
  x.beginPath(); x.arc(100, 100, 66, 0, Math.PI * 2); x.stroke()
  for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI; x.beginPath(); x.moveTo(100 + Math.cos(a) * 66, 100 + Math.sin(a) * 66); x.lineTo(100 - Math.cos(a) * 66, 100 - Math.sin(a) * 66); x.stroke() }
  return c
}
function logo() {
  const [c, x] = canvas(1024, 300)
  x.font = '400 220px Display, Georgia, serif'; x.textAlign = 'center'; x.textBaseline = 'middle'
  x.fillStyle = INK; x.fillText('RAASTA', 512, 160)
  return c
}

const DRAW = { cat_walk_a: () => cat('a'), cat_walk_b: () => cat('b'), myna_fly: () => myna(true), myna_fly_down: () => myna(false), guy_kabir: kabir, kamla_walker: kamla,
  dadaji_kid: dadajiKid, zoya_chair: zoya, scooter_speed: scooter, cart_vendor: () => cart(true), cart_wheel: wheel, logo_raasta: logo }
const WATCH = ['cat_walk_a', 'cat_walk_b', 'myna_fly', 'guy_kabir', 'kamla_walker', 'dadaji_kid', 'zoya_chair']

// --- shared texture cache: one entry per name, placeholder first, painted file swapped in ----------------
const cache = new Map()
const watchers = new Set()
export function charTexture(name) {
  if (cache.has(name)) return cache.get(name)
  const cv = DRAW[name]()
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
  const entry = { name, tex, aspect: cv.width / cv.height, real: false, facing: 1, subs: new Set() }
  cache.set(name, entry)
  if (WATCH.includes(name)) watchers.add(name)
  return entry
}
// crop a painted cut-out to its alpha box (so the plane's bottom edge is the feet)
function alphaBox(img) {
  const w = img.naturalWidth, h = img.naturalHeight
  const c = document.createElement('canvas'); c.width = w; c.height = h
  const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(img, 0, 0)
  const d = x.getImageData(0, 0, w, h).data
  let x0 = w, y0 = h, x1 = -1, y1 = -1
  for (let y = 0; y < h; y += 2) for (let xx = 0; xx < w; xx += 2) if (d[(y * w + xx) * 4 + 3] > 24) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (y < y0) y0 = y; if (y > y1) y1 = y }
  if (x1 < 0) return [0, 0, w - 1, h - 1]
  return [Math.max(0, x0 - 2), Math.max(0, y0 - 2), Math.min(w - 1, x1 + 2), Math.min(h - 1, y1 + 2)]
}
function cropTo(img, [x0, y0, x1, y1]) {
  const o = document.createElement('canvas'); o.width = x1 - x0 + 1; o.height = y1 - y0 + 1
  o.getContext('2d').drawImage(img, x0, y0, o.width, o.height, 0, 0, o.width, o.height)
  return o
}
// apply a crop box to an entry (painted file): texture, aspect
function setReal(e, img, box) {
  const cv = cropTo(img, box)
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4
  e.tex = t; e.aspect = cv.width / cv.height; e.real = true; e.facing = REAL_FACING[e.name] ?? 1; e.img = img; e.box = box
}

let checking = false
async function probe() {
  if (checking) return; checking = true
  for (const name of [...watchers]) {
    const img = new Image()
    const ok = await new Promise((r) => { img.onload = () => r(true); img.onerror = () => r(false); img.src = `${BASE}${name}.png?v=${Math.floor(Date.now() / 60000)}` })
    if (!ok || !img.naturalWidth) continue
    const e = cache.get(name)
    setReal(e, img, alphaBox(img))
    // walk pairs are pixel-aligned: crop both poses with the UNION box so the swap never shifts or rescales the body
    const pn = PAIR[name], pe = pn && cache.get(pn)
    if (pe?.real && pe.img && pe.img.naturalWidth === img.naturalWidth && pe.img.naturalHeight === img.naturalHeight) {
      const u = [Math.min(e.box[0], pe.box[0]), Math.min(e.box[1], pe.box[1]), Math.max(e.box[2], pe.box[2]), Math.max(e.box[3], pe.box[3])]
      setReal(e, img, u); setReal(pe, pe.img, u)
    }
    watchers.delete(name)
    // a walk pair swaps only when both poses are painted (never a white cat and a black cat alternating)
    for (const f of cache.values()) f.subs.forEach((fn) => fn())
  }
  checking = false
}
// re-check every 6 s for the first 3 minutes, then every 30 s (keeps the console quiet on a long visit)
// layout() rebuilds every scene: forget the old meshes' swap hooks so they can be freed
export function resetCharSubs() { for (const e of cache.values()) e.subs.clear() }
export function startCharWatch() {
  probe(); let n = 0
  const tick = () => { if (!watchers.size) return; if (!document.hidden) probe(); n++; setTimeout(tick, n < 30 ? 6000 : 30000) }
  setTimeout(tick, 6000)
}

const PAIR = { cat_walk_a: 'cat_walk_b', cat_walk_b: 'cat_walk_a', myna_fly: 'myna_fly_down', myna_fly_down: 'myna_fly' }
// which entry actually shows for a name: if its walk partner is painted and it is not, borrow the partner
function shown(name) {
  const e = charTexture(name), p = PAIR[name] && charTexture(PAIR[name])
  if (p && p.real && !e.real) return p
  if (p && e.real && !p.real) return e
  return e
}

// a plane anchored at the feet; height in world units; follows texture swaps
export function charPlane(name, height) {
  const geo = new THREE.PlaneGeometry(1, 1); geo.translate(0, 0.5, 0)
  const mat = new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, alphaTest: 0.02 })
  const mesh = new THREE.Mesh(geo, mat)
  mesh.userData.name = name; mesh.userData.flip = 1; mesh.userData.h = height
  const fit = () => {
    const e = shown(mesh.userData.name)
    if (mat.map !== e.tex) { mat.map = e.tex; mat.needsUpdate = true }
    mesh.scale.set(height * e.aspect * mesh.userData.flip * e.facing, height, 1)
  }
  mesh.userData.fit = fit
  fit(); charTexture(name).subs.add(fit); if (PAIR[name]) charTexture(PAIR[name]).subs.add(fit)
  mesh.userData.setFlip = (f) => { if (mesh.userData.flip !== f) { mesh.userData.flip = f; fit() } }
  return mesh
}
// switch the drawing a plane shows (walk cycle a/b, wing up/down)
export function setCharFrame(mesh, name) {
  if (mesh.userData.name === name) return
  mesh.userData.name = name
  const e = charTexture(name); if (!e.subs.has(mesh.userData.fit)) e.subs.add(mesh.userData.fit)
  mesh.userData.fit()
}
