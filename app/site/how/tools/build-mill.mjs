// the /how figure: an isometric masala chakki mill whose parts are the 17 stages of a RAASTA scan.
// built with the anatomy kit (vendored in ./kit, MIT, see ./kit/LICENSE). writes src/pages/how-mill.gen.js:
// the static SVG (every part in a <g data-stage>), the projection, and the anchors the live code moves things to.
//   node app/site/how/tools/build-mill.mjs
import { writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import * as k from './kit/iso-kit.mjs'
import * as G from './kit/lathe.mjs'
import { BODIES, BODY_TOPS, CATS } from '../../src/pages/how-runs.gen.js'

const HERE = dirname(fileURLToPath(import.meta.url))
const OUT = join(HERE, '../../src/pages/how-mill.gen.js')

const W = 1000
const H = 640
const AZ = 58
const EL = 30

// ---------- world layout (units ~ px, x along the flow, y toward the viewer, z up) ----------
const BASE = { x: -272, y: -102, w: 544, d: 204, r: 10 }
const BASE_H = 12
const FOOT_H = 6
const HOP = [-215, -12] // hopper axis
const STONE = [-120, -12] // stone axle
const SIEVE = { x: -50, y: -34, w: 64, d: 62, r: 3 }
const HATCH = { x: -46, y: 34, w: 52, d: 30, r: 2 }
const HATCH_H = 34
const CHAFF = { x: -46, y: -96, w: 50, d: 26, r: 2 }
const DIAL = [28, -22]
const SPOON = [28, 24]
const RACK = { x: 50, y: -98, w: 100, d: 44, r: 2 }
const RACK_H = 122
const WALL = { x: 170, y: -100, w: 94, d: 6, r: 1 }
const TRAY = { x: 202, y: 14, w: 56, d: 46, r: 3 }
const PIN = [156, 8]

const P = k.fitProjection(
  [...k.boxCorners(BASE, -BASE_H - FOOT_H, 0), [HOP[0] - 32, HOP[1] - 32, 196], [HOP[0] + 32, HOP[1] + 32, 196], [WALL.x + WALL.w, WALL.y, 176], [WALL.x, WALL.y, 176], [-215, -12, 236]],
  W, H, { pad: 26, azimuth: AZ, elevation: EL },
)
const V = G.viewOf(P)
const at = (p) => k.iso(p, P)
const S = (paths, style) => k.solidSvg(paths, style)
const L = (d, style) => k.lineSvg(d, style)
const D = (pts, style) => k.dotsSvg(pts, style)
const depth = (p) => k.depthOf(p, P)
const f1 = (v) => Math.round(v * 10) / 10

// ---------- convex polyhedra (for tilted ducts, the hopper frustum, wheels on any axis, the hatch door) ----------
function hull(points) {
  const pts = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1])
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
  const lower = []
  for (const p of pts) { while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) lower.pop(); lower.push(p) }
  const upper = []
  for (const p of pts.reverse()) { while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) upper.pop(); upper.push(p) }
  return lower.slice(0, -1).concat(upper.slice(0, -1))
}
// verts: world points; faces: arrays of vertex indices (any winding, convex body)
function polySolid(verts, faces) {
  const c = G.mul3(verts.reduce((a, v) => G.add3(a, v), [0, 0, 0]), 1 / verts.length)
  const info = faces.map((f) => {
    const a = verts[f[0]], b = verts[f[1]], d = verts[f[2]]
    let n = G.unit3(G.cross3(G.sub3(b, a), G.sub3(d, a)))
    const fc = G.mul3(f.reduce((s, i) => G.add3(s, verts[i]), [0, 0, 0]), 1 / f.length)
    if (G.dot3(n, G.sub3(fc, c)) < 0) n = G.mul3(n, -1)
    return { f, n, vis: G.dot3(n, V) > 1e-6 }
  })
  const edges = new Map()
  info.forEach((fi, idx) => fi.f.forEach((v, j) => {
    const w = fi.f[(j + 1) % fi.f.length]
    const key = v < w ? `${v}-${w}` : `${w}-${v}`
    if (!edges.has(key)) edges.set(key, [v, w, []])
    edges.get(key)[2].push(idx)
  }))
  const outline = [], crease = []
  for (const [, [a, b, fs]] of edges) {
    const vis = fs.map((i) => info[i].vis)
    const seg = k.pathOf([at(verts[a]), at(verts[b])])
    if (vis.length === 2 && vis[0] && vis[1]) crease.push(seg)
    else if (vis.some(Boolean)) outline.push(seg)
  }
  const shades = [[], [], [], []], top = []
  for (const fi of info) {
    if (!fi.vis) continue
    const d = k.pathOf(fi.f.map((i) => at(verts[i])), true)
    const tone = G.toneOf(fi.n, P)
    if (tone >= 4) top.push(d)
    else shades[tone].push(d)
  }
  return { fill: k.pathOf(hull(verts.map(at)), true), outline: outline.join(''), crease: crease.join(''), top: top.join(''), shades: shades.map((s) => s.join('')) }
}
// a box from a to b along its axis, w wide (horizontal, across) and h tall (across, up-ish), centred on the axis
function beam(a, b, w, h) {
  const u = G.unit3(G.sub3(b, a))
  let s = G.cross3(u, [0, 0, 1])
  if (G.len3(s) < 1e-6) s = [1, 0, 0]
  s = G.unit3(s)
  const n = G.unit3(G.cross3(s, u))
  const corners = (p) => [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([i, j]) => G.add3(p, G.add3(G.mul3(s, (i * w) / 2), G.mul3(n, (j * h) / 2))))
  const verts = [...corners(a), ...corners(b)]
  return polySolid(verts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
}
// an n-sided prism (a wheel, a hub, a motor) along any axis
function wheel(c, axis, r, len, n = 28, phase = 0) {
  const F = G.frameAlong(c, axis)
  const ring = (s) => Array.from({ length: n }, (_, i) => {
    const t = phase + (i / n) * Math.PI * 2
    return G.add3(G.add3(c, G.mul3(F.a, s)), G.add3(G.mul3(F.u, Math.cos(t) * r), G.mul3(F.v, Math.sin(t) * r)))
  })
  const verts = [...ring(0), ...ring(len)]
  const faces = [Array.from({ length: n }, (_, i) => i), Array.from({ length: n }, (_, i) => n + i)]
  for (let i = 0; i < n; i++) faces.push([i, (i + 1) % n, n + ((i + 1) % n), n + i])
  return { paths: polySolid(verts, faces), F }
}
// square frustum (the hopper), half sizes s0 at z0 and s1 at z1
function frustum(cx, cy, z0, z1, s0, s1) {
  const sq = (s, z) => [[cx - s, cy - s, z], [cx + s, cy - s, z], [cx + s, cy + s, z], [cx - s, cy + s, z]]
  const verts = [...sq(s0, z0), ...sq(s1, z1)]
  return polySolid(verts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
}
const byDepth = (pts) => [...pts].sort((a, b) => depth([a[0], a[1], 0]) - depth([b[0], b[1], 0]))
const faceRect = (x0, x1, y, z0, z1) => k.pathOf([at([x0, y, z0]), at([x1, y, z0]), at([x1, y, z1]), at([x0, y, z1])], true)
const faceRectX = (x, y0, y1, z0, z1) => k.pathOf([at([x, y0, z0]), at([x, y1, z0]), at([x, y1, z1]), at([x, y0, z1])], true)
const screws = (pts, z) => D(pts.map(([x, y]) => at([x, y, z])), { size: 0.5, tone: 'mid' })
const halo = (plan, z, h) => `<path class="iso-halo" d="${k.haloOf(plan, z, h, P)}"/>`
// a face-up dial: puck, bezel, ticks; needle drawn live
function dialFace(cx, cy, z, r, h, { ticks = 40, every = 5 } = {}) {
  const top = z + h
  const out = [S(k.cylinder(cx, cy, r, z, h, P, 56, 0.6), { tone: 'hi', crease: 'lo' })]
  out.push(L(k.sideArc(cx, cy, r, top - 2.2, P, 40), { tone: 'faint' }))
  out.push(L(k.knurl(cx, cy, r, top - 2.2, top, 60, P, 0.3), { tone: 'lo' }))
  out.push(L(k.ring(cx, cy, r - 1.8, top, P, 48), { tone: 'lo' }))
  const t = k.radialTicks(cx, cy, r - 2.4, ticks, every, top, [1.1, 2.4], P)
  out.push(L(t.minor, { tone: 'lo' }), L(t.major, { tone: 'mid' }))
  out.push(L(k.ring(cx, cy, 1.2, top, P, 12), { tone: 'mid' }))
  return out.join('')
}

// ---------- items: { key, svg } painted in ascending key ----------
const items = []
const put = (key, svg) => items.push({ key, svg })
const part = (stage, svg, extra = '') => `<g class="mill-part" data-stage="${stage}"${extra}>${svg}</g>`

// base plate on feet
{
  const out = [halo(BASE, -BASE_H - FOOT_H, BASE_H)]
  const feet = [...k.corners(BASE, 26), [BASE.x + BASE.w / 2, BASE.y + 26], [BASE.x + BASE.w / 2, BASE.y + BASE.d - 26]]
  for (const [x, y] of byDepth(feet)) {
    out.push(S(k.cylinder(x, y, 9, -BASE_H - FOOT_H, 1.8, P, 28), { tone: 'lo' }))
    out.push(S(k.cylinder(x, y, 7, -BASE_H - FOOT_H + 1.8, FOOT_H - 1.8, P, 28), { tone: 'mid' }))
  }
  out.push(S(k.slabOf(BASE, -BASE_H, BASE_H, P, 8, 1.6), { tone: 'mid', inner: L(k.sideSeam(BASE, -BASE_H + 4, P, 8), { tone: 'faint' }) }))
  out.push(L(k.planOutline(k.insetPlan(BASE, 6), 0, P), { tone: 'lo' }))
  const sc = k.corners(BASE, 12)
  out.push(L(sc.map(([x, y]) => k.ring(x, y, 2.4, 0, P, 16)).join(''), { tone: 'lo' }))
  out.push(D(sc.map(([x, y]) => at([x, y, 0])), { size: 0.55 }))
  // time ruler strip along the front edge: one major tick per second of the street scan (10.56 s), 4 minors between
  const strip = { x: -250, y: BASE.y + BASE.d - 18, w: 236, d: 8, r: 1 }
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: 'lo', crease: 'none' }))
  const tk = k.topTicks(strip.x + 4, strip.x + strip.w - 4, 4.4, 5, strip.y + 0.8, 0.6, [2, 3.8], P)
  out.push(L(tk.minor, { tone: 'lo' }), L(tk.major, { tone: 'mid' }))
  out.push(D([at([strip.x + 2, strip.y + 4, 0.6]), at([strip.x + strip.w - 2, strip.y + 4, 0.6])], { size: 0.45 }))
  // maker's label plate with three rule lines (stand for printed text)
  const lp = { x: 110, y: BASE.y + BASE.d - 26, w: 40, d: 16, r: 1.5 }
  out.push(S(k.slabOf(lp, 0, 0.8, P, 4), { tone: 'lo' }))
  out.push(L(k.planOutline(k.insetPlan(lp, 1.6), 0.8, P), { tone: 'faint' }))
  ;[[4, 30], [8, 22], [12, 26]].forEach(([dy, len]) => out.push(L(k.lineOnTop([lp.x + 6, lp.y + dy], [lp.x + 6 + len, lp.y + dy], 0.8, P), { tone: 'lo', free: true })))
  out.push(D([at([lp.x + 3, lp.y + 8, 0.8]), at([lp.x + lp.w - 3, lp.y + 8, 0.8])], { size: 0.45 }))
  put(-1e6, `<g class="mill-base">${out.join('')}</g>`)
}

// back wall board with the ledger (16) and the complaint letter (17)
{
  const out = [S(k.slabOf(WALL, 0, 176, P, 3, 0.6), { tone: 'lo', inner: L(k.sideSeam(WALL, 8, P, 3), { tone: 'faint' }) + L(k.sideSeam(WALL, 168, P, 3), { tone: 'faint' }) })]
  out.push(screws([[WALL.x + 6, WALL.y + 3], [WALL.x + WALL.w - 6, WALL.y + 3]], 176))
  // planks: vertical joints on the front face, full height
  const fy = WALL.y + WALL.d
  for (const x of [WALL.x + 31, WALL.x + 62]) out.push(L(k.segment([x, fy, 8], [x, fy, 168], P), { tone: 'faint' }))
  // nails on the front face
  out.push(D([[WALL.x + 6, 160], [WALL.x + WALL.w - 6, 160], [WALL.x + 6, 16], [WALL.x + WALL.w - 6, 16]].map(([x, z]) => at([x, fy, z])), { size: 0.55, tone: 'mid' }))
  const wallSvg = out.join('')
  // shelf on two brackets
  const shelf = { x: 180, y: fy, w: 76, d: 18, r: 1 }
  const sh = []
  for (const x of [188, 244]) sh.push(S(k.slabOf({ x: x - 1.5, y: fy, w: 3, d: 14, r: 0.5 }, 64, 14, P, 2), { tone: 'mid' }))
  sh.push(S(k.slabOf(shelf, 78, 4, P, 3, 0.5), { tone: 'mid' }))
  sh.push(screws([[184, fy + 9], [252, fy + 9]], 82))
  // the ledger book standing on the shelf: rule lines are its printed lines, the live code inks one more per receipt
  const book = { x: 188, y: fy + 1, w: 54, d: 12, r: 1 }
  const bf = book.y + book.d
  const ledger = [S(k.slabOf(book, 82, 40, P, 3, 0.5), { tone: 'hi', crease: 'lo', inner: L(k.sideSeam(book, 86, P, 3), { tone: 'faint' }) })]
  const rules = []
  for (let i = 0; i < 6; i++) {
    const z = 116 - i * 4.4
    const len = [40, 34, 44, 30, 38, 26][i]
    rules.push(L(k.segment([book.x + 5, bf, z], [book.x + 5 + len, bf, z], P), { tone: 'lo', free: true }))
  }
  ledger.push(rules.join(''))
  ledger.push(`<path class="iso-line mill-ink" data-tone="hi" data-free="" d="${k.segment([book.x + 5, bf, 89.6], [book.x + 47, bf, 89.6], P)}"/>`)
  put(depth([WALL.x + 40, WALL.y, 0]), part(16, wallSvg + sh.join('') + ledger.join(''), ' data-name="ledger"'))
  // letter tucked into the ledger, lifts out at the report step
  const lt = { x: 226, y: fy + 4, w: 13, d: 2, r: 0.3 }
  const letter = [S(k.slabOf(lt, 112, 22, P, 2), { tone: 'hi', crease: 'lo' })]
  const ly = lt.y + lt.d
  letter.push(L(k.pathOf([at([lt.x, ly, 134]), at([lt.x + lt.w / 2, ly, 128]), at([lt.x + lt.w, ly, 134])]), { tone: 'lo' }))
  put(depth([WALL.x + 60, WALL.y + 10, 0]), part(17, `<g data-move="letter">${letter.join('')}</g>`))
  // wall clock: 12 major ticks, one per second; the hand reads the recorded server time of the scan
  const cc = [217, fy, 157]
  const ck = [S(wheel(cc, [0, 1, 0], 12, 2.4, 40).paths, { tone: 'mid', crease: 'lo' })]
  const face = (r, t) => [cc[0] + Math.sin(t) * r, fy + 2.4, cc[2] + Math.cos(t) * r]
  ck.push(S(wheel([cc[0], fy + 2.4, cc[2]], [0, 1, 0], 10.4, 0.4, 40).paths, { tone: 'hi', crease: 'faint' }))
  let maj = '', min = ''
  for (let i = 0; i < 60; i++) {
    const t = (i / 60) * Math.PI * 2
    const big = i % 5 === 0
    const seg = k.pathOf([at(face(10.2, t)), at(face(big ? 7.6 : 9, t))])
    if (big) maj += seg; else min += seg
  }
  ck.push(L(min, { tone: 'lo' }), L(maj, { tone: 'mid' }))
  ck.push(`<path class="iso-line" data-tone="hi" data-free="start" data-live="clock" style="stroke-width:1.1"/>`)
  ck.push(D([at([cc[0], fy + 2.8, cc[2]])], { size: 0.9, tone: 'hi' }))
  put(depth([WALL.x + 30, WALL.y + 12, 0]), part(16, ck.join(''), ' data-name="clock"'))
}

// the drive (one worker): motor, belt and a jack shaft into the stone stand
{
  const mz = 15, my = 74
  const motor = []
  const cradle = { x: -214, y: my - 18, w: 40, d: 30, r: 2 }
  motor.push(halo(cradle, 0, 4), S(k.slabOf(cradle, 0, 4, P, 3, 0.5), { tone: 'lo' }))
  motor.push(screws(k.corners(cradle, 3.5), 4))
  for (const x of [-206, -184]) motor.push(S(k.slabOf({ x: x - 3, y: my - 14, w: 6, d: 22, r: 1 }, 4, 5, P, 2, 0.3), { tone: 'mid' }))
  // body lies along y: end bell, finned body, end bell
  motor.push(S(wheel([-195, my - 20, mz], [0, 1, 0], 10, 4, 32).paths, { tone: 'mid', crease: 'lo' }))
  motor.push(S(wheel([-195, my - 16, mz], [0, 1, 0], 11.4, 18, 36).paths, { tone: 'hi', crease: 'lo' }))
  motor.push(S(wheel([-195, my + 2, mz], [0, 1, 0], 10, 3, 32).paths, { tone: 'mid', crease: 'lo' }))
  motor.push(S(k.slabOf({ x: -201, y: my - 12, w: 12, d: 9, r: 1 }, mz + 10.4, 4.2, P, 2, 0.4), { tone: 'mid' }))
  motor.push(screws([[-198, my - 10], [-192, my - 5]], mz + 14.6))
  motor.push(S(wheel([-195, my + 5, mz], [0, 1, 0], 1.6, 3, 12).paths, { tone: 'mid' }))
  motor.push(S(wheel([-195, my + 8, mz], [0, 1, 0], 6, 3.6, 28).paths, { tone: 'hi', crease: 'lo' }))
  // jack shaft from the stand front face out to the same plane, with a bearing block and a big pulley
  const jx = -146, jz = 22, fy = STONE[1] + 42
  const sh = []
  sh.push(S(k.slabOf({ x: jx - 5, y: fy, w: 10, d: 6, r: 1 }, jz - 6, 12, P, 2, 0.4), { tone: 'mid' }))
  sh.push(S(wheel([jx, fy + 6, jz], [0, 1, 0], 1.8, my + 8 - fy - 6, 14).paths, { tone: 'mid', crease: 'none' }))
  sh.push(S(wheel([jx, my + 7.6, jz], [0, 1, 0], 11, 4.4, 40).paths, { tone: 'hi', crease: 'lo' }))
  sh.push(`<path class="iso-line" data-tone="mid" data-live="pulley"/>`)
  // flat belt: two straight runs tangent to both pulleys, in the plane y = my + 9.8
  // flat belt: the two outer tangents of both pulleys, on their front faces (plane y = bp)
  const bp = my + 11.8
  const c1 = [-195, mz], r1 = 6, c2 = [jx, jz], r2 = 11
  const dx = c2[0] - c1[0], dz = c2[1] - c1[1], dist = Math.hypot(dx, dz)
  const ang = Math.atan2(dz, dx), off = Math.acos((r1 - r2) / dist)
  const tang = (sgn) => {
    const a = ang + sgn * off
    return k.pathOf([at([c1[0] + Math.cos(a) * r1, bp, c1[1] + Math.sin(a) * r1]), at([c2[0] + Math.cos(a) * r2, bp, c2[1] + Math.sin(a) * r2])])
  }
  const belt = L(tang(1) + tang(-1), { tone: 'hi' })
  put(depth([-170, my, 0]), `<g class="mill-part" data-stage="drive" data-name="drive">${motor.join('')}${sh.join('')}${belt}</g>`)
}

// taxonomy rack (11): 12 drawers, one per element category; gear train (13) on its side
const DRAWERS = []
{
  const plinth = { x: RACK.x - 2, y: RACK.y - 2, w: RACK.w + 4, d: RACK.d + 4, r: 2 }
  const out = [halo(plinth, 0, 6), S(k.slabOf(plinth, 0, 6, P, 3, 0.6), { tone: 'lo' })]
  out.push(S(k.slabOf(RACK, 6, RACK_H - 6, P, 3, 0.8), { tone: 'mid', inner: L(k.sideSeam(RACK, 12, P, 3), { tone: 'faint' }) }))
  const cap = { x: RACK.x - 3, y: RACK.y - 3, w: RACK.w + 6, d: RACK.d + 6, r: 2 }
  out.push(S(k.slabOf(cap, RACK_H, 4, P, 3, 0.8), { tone: 'mid' }))
  out.push(screws(k.corners(cap, 5), RACK_H + 4))
  const fy = RACK.y + RACK.d
  const cols = 4, rows = 3, mx = 6, mz = 6, gap = 3.2
  const dw = (RACK.w - 2 * mx - (cols - 1) * gap) / cols
  const dh = (RACK_H - 6 - 2 * mz - (rows - 1) * gap) / rows
  const frames = 6, reach = 18
  const cells = []
  CATS.forEach((cat, i) => {
    const col = i % cols, row = Math.floor(i / cols)
    const x0 = RACK.x + mx + col * (dw + gap), z0 = RACK_H - mz - (row + 1) * dh - row * gap
    cells.push({ cat, x0, z0 })
  })
  // drawer recess outlines on the face (closed outlines, no loose ends)
  out.push(L(cells.map(({ x0, z0 }) => faceRect(x0 - 0.6, x0 + dw + 0.6, fy, z0 - 0.6, z0 + dh + 0.6)).join(''), { tone: 'lo' }))
  const drawerAt = ({ x0, z0 }, open) => {
    const o = []
    if (open > 0.2) {
      o.push(S(k.slabOf({ x: x0 + 1.2, y: fy, w: dw - 2.4, d: open, r: 0.4 }, z0 + 1.2, dh - 3, P, 2), { tone: 'mid' }))
    }
    const front = { x: x0, y: fy + open, w: dw, d: 1.6, r: 0.5 }
    o.push(S(k.slabOf(front, z0, dh, P, 2, 0.4), { tone: 'hi', crease: 'lo' }))
    const ff = front.y + front.d
    // label holder (closed outline) and pull
    o.push(L(faceRect(x0 + dw / 2 - 5, x0 + dw / 2 + 5, ff, z0 + dh - 9, z0 + dh - 4), { tone: 'lo' }))
    o.push(S(k.slabOf({ x: x0 + dw / 2 - 4, y: ff, w: 8, d: 2.2, r: 0.8 }, z0 + dh / 2 - 4, 2.4, P, 2), { tone: 'mid' }))
    o.push(D([at([x0 + 2, ff, z0 + 2]), at([x0 + dw - 2, ff, z0 + 2])], { size: 0.4, tone: 'mid' }))
    return o.join('')
  }
  const sorted = [...cells].sort((a, b) => depth([a.x0, fy, a.z0]) - depth([b.x0, fy, b.z0]))
  const drawersSvg = sorted.map((c) => {
    const groups = Array.from({ length: frames + 1 }, (_, f) => `<g data-f="${f}"${f ? ' style="display:none"' : ''}>${drawerAt(c, (f / frames) * reach)}</g>`).join('')
    DRAWERS.push({ cat: c.cat.id, front: [c.x0 + dw / 2, fy + reach + 2, c.z0 + dh / 2] })
    return `<g data-drawer="${c.cat.id}">${groups}</g>`
  }).join('')
  put(depth([RACK.x + 50, RACK.y + 10, 0]), part(11, out.join('') + drawersSvg, ' data-name="rack"'))
  // gear train on the +x face: two wheels that turn together (combination rules couple two trays)
  const gx = RACK.x + RACK.w
  const g = []
  g.push(S(k.slabOf({ x: gx, y: RACK.y + 6, w: 2, d: 34, r: 0.6 }, 50, 64, P, 2, 0.4), { tone: 'lo' }))
  g.push(screws([[gx + 2, RACK.y + 9], [gx + 2, RACK.y + 37]], 114))
  const big = wheel([gx + 2, -80, 92], [1, 0, 0], 14, 3, 32)
  const small = wheel([gx + 2, -65, 75.8], [1, 0, 0], 8.6, 3, 20)
  g.push(S(big.paths, { tone: 'mid', crease: 'lo' }), S(small.paths, { tone: 'mid', crease: 'lo' }))
  const hubB = wheel([gx + 5, -80, 92], [1, 0, 0], 3, 2, 16), hubS = wheel([gx + 5, -65, 75.8], [1, 0, 0], 2.4, 2, 14)
  g.push(S(hubB.paths, { tone: 'hi' }), S(hubS.paths, { tone: 'hi' }))
  g.push(`<path class="iso-line" data-tone="lo" data-live="gear-big"/><path class="iso-line" data-tone="lo" data-live="gear-small"/>`)
  put(depth([gx + 4, -70, 0]), part(13, g.join(''), ' data-name="gears"'))
}

// chaff bin (REJECT) behind the sieve
{
  const out = [halo(CHAFF, 0, 22), S(k.slabOf(CHAFF, 0, 22, P, 3, 0.6), { tone: 'lo', inner: L(k.sideSeam(CHAFF, 16, P, 3), { tone: 'faint' }) })]
  out.push(`<path class="mill-mouth" d="${k.pathOf(k.roundedPlan(k.insetPlan(CHAFF, 3), 3).map(([x, y]) => at([x, y, 22])), true)}"/>`)
  out.push(L(k.planOutline(k.insetPlan(CHAFF, 3), 22, P, 3), { tone: 'mid' }))
  put(depth([CHAFF.x + 25, CHAFF.y + 4, 0]), `<g class="mill-part" data-stage="reject" data-name="chaff">${out.join('')}</g><g data-layer="chaff"></g>`)
}

// hopper (1) on its stand, with the feed gate and moisture gauge (2)
{
  const [hx, hy] = HOP
  const foot = { x: hx - 25, y: hy - 25, w: 50, d: 50, r: 3 }
  const st = [halo(foot, 0, 4), S(k.slabOf(foot, 0, 4, P, 3, 0.5), { tone: 'lo' })]
  st.push(screws(k.corners(foot, 4), 4))
  const posts = byDepth([[hx - 18, hy - 18], [hx + 18, hy - 18], [hx + 18, hy + 18], [hx - 18, hy + 18]])
  const back = posts.slice(0, 2), front = posts.slice(2)
  const postSvg = ([x, y]) => S(k.cylinder(x, y, 2.4, 4, 114, P, 16), { tone: 'mid', crease: 'none' }) + S(k.cylinder(x, y, 3.4, 4, 3, P, 16), { tone: 'mid' })
  st.push(back.map(postSvg).join(''))
  // cross braces on the two visible sides
  st.push(S(beam([hx - 18, hy + 18, 44], [hx + 18, hy + 18, 44], 2.2, 2.2), { tone: 'mid' }))
  st.push(S(beam([hx + 18, hy - 18, 60], [hx + 18, hy + 18, 60], 2.2, 2.2), { tone: 'mid' }))
  st.push(front.map(postSvg).join(''))
  const stand = st.join('')
  // gate block and slide (stage 2) with the condition gauge on a bracket
  const gate = { x: hx - 14, y: hy - 14, w: 28, d: 28, r: 2 }
  const gt = [S(k.slabOf(gate, 118, 14, P, 3, 0.6), { tone: 'mid', inner: L(k.sideSeam(gate, 125, P, 3), { tone: 'faint' }) })]
  gt.push(S(k.slabOf({ x: hx + 14, y: hy - 7, w: 9, d: 14, r: 0.6 }, 123.5, 2.4, P, 2, 0.3), { tone: 'hi', crease: 'lo' }))
  gt.push(S(k.slabOf({ x: hx + 22, y: hy - 3, w: 2, d: 6, r: 0.4 }, 122, 6, P, 2), { tone: 'mid' }))
  gt.push(S(k.slabOf({ x: hx - 6, y: hy + 14, w: 12, d: 10, r: 0.8 }, 120, 3, P, 2, 0.3), { tone: 'mid' }))
  gt.push(dialFace(hx, hy + 22, 123, 8, 4, { ticks: 30, every: 5 }))
  gt.push(`<path class="iso-line" data-tone="hi" data-free="start" data-live="gauge" style="stroke-width:1.1"/>`)
  const throat = { x: hx - 9, y: hy - 9, w: 18, d: 18, r: 1 }
  gt.push(S(k.slabOf(throat, 132, 4, P, 2, 0.4), { tone: 'mid' }))
  // hopper frustum with a rim and seams
  const hp = [S(frustum(hx, hy, 136, 186, 9, 30), { tone: 'mid', crease: 'lo' })]
  for (const z of [152, 170]) {
    const s = 9 + ((z - 136) / 50) * 21
    hp.push(L(k.pathOf([at([hx + s, hy - s, z]), at([hx + s, hy + s, z]), at([hx - s, hy + s, z])]), { tone: 'faint' }))
  }
  const rim = { x: hx - 32, y: hy - 32, w: 64, d: 64, r: 2 }
  hp.push(S(k.slabOf(rim, 186, 4, P, 3, 0.6), { tone: 'hi', crease: 'lo' }))
  hp.push(`<path class="mill-mouth" d="${k.pathOf(k.roundedPlan(k.insetPlan(rim, 4), 3).map(([x, y]) => at([x, y, 190])), true)}"/>`)
  hp.push(L(k.planOutline(k.insetPlan(rim, 4), 190, P, 3), { tone: 'mid' }))
  hp.push(screws(k.corners(rim, 2), 190))
  put(depth([hx, hy, 0]), `<g class="mill-part" data-stage="2" data-name="gate">${stand}${gt.join('')}</g>${part(1, hp.join(''), ' data-name="hopper"')}`)
}

// the stones (3 upper = detector A, 4 lower = detector B) on a stand with the gap wheel (6) and feed duct
{
  const [sx, sy] = STONE
  const stand = { x: sx - 42, y: sy - 42, w: 84, d: 84, r: 4 }
  const out = [halo(stand, 0, 54), S(k.slabOf(stand, 0, 54, P, 4, 1), { tone: 'mid', inner: L(k.sideSeam(stand, 6, P, 4), { tone: 'faint' }) + L(k.sideSeam(stand, 48, P, 4), { tone: 'faint' }) })]
  // vents on the +x face: closed slots
  const vx = stand.x + stand.w
  for (let i = 0; i < 5; i++) out.push(L(faceRectX(vx, sy - 24 + i * 7, sy - 20 + i * 7, 18, 36), { tone: 'lo' }))
  // access panel on the front face
  const fy = stand.y + stand.d
  out.push(S(k.slabOf({ x: sx - 30, y: fy, w: 60, d: 1.2, r: 0.4 }, 8, 38, P, 2, 0.3), { tone: 'mid' }))
  out.push(D([[sx - 27, 11], [sx + 27, 11], [sx - 27, 43], [sx + 27, 43]].map(([x, z]) => at([x, fy + 1.2, z])), { size: 0.5, tone: 'mid' }))
  const standSvg = out.join('')
  // gap wheel (stage 6): sets the stone gap = what counts as footpath ground
  const gw = []
  const hubW = wheel([sx, fy + 1.2, 27], [0, 1, 0], 3.2, 3, 16)
  const rimW = wheel([sx, fy + 4.2, 27], [0, 1, 0], 11, 2.6, 36)
  gw.push(S(hubW.paths, { tone: 'mid' }), S(rimW.paths, { tone: 'hi', crease: 'lo' }))
  gw.push(`<path class="iso-line" data-tone="mid" data-live="gapwheel"/>`)
  // pan, lower stone, upper stone
  const st = []
  st.push(S(k.cylinder(sx, sy, 45, 54, 6, P, 72, 0.8), { tone: 'lo' }))
  st.push(L(k.ring(sx, sy, 41, 60, P, 72), { tone: 'faint' }))
  const B = [S(k.cylinder(sx, sy, 37, 61, 13.5, P, 72, 0.6), { tone: 'mid', crease: 'lo' }), `<path class="iso-line" data-tone="lo" data-live="stoneB"/>`]
  const A = [S(k.cylinder(sx, sy, 37, 76, 14, P, 72, 0.8), { tone: 'hi', crease: 'lo' }), `<path class="iso-line" data-tone="lo" data-live="stoneA-side"/>`]
  A.push(`<path class="mill-mouth" d="${k.pathOf(k.circleRing(sx, sy, 7, 24).map(([x, y]) => at([x, y, 90])), true)}"/>`)
  A.push(L(k.ring(sx, sy, 7, 90, P, 24), { tone: 'mid' }), L(k.ring(sx, sy, 33, 90, P, 64), { tone: 'faint' }))
  A.push(`<path class="iso-line" data-tone="mid" data-live="stoneA-top"/>`)
  // outlet spout from the pan to the sieve
  const spout = S(beam([sx + 40, sy + 6, 57], [-44, -4, 46.5], 10, 4), { tone: 'mid', crease: 'lo' })
  // feed duct from the gate to the eye
  const duct = S(beam([HOP[0] + 12, HOP[1], 124], [sx - 8, sy, 98], 8, 6), { tone: 'mid', crease: 'lo' })
  const ductLegs = S(k.cylinder(-176, -12, 1.6, 0, 111.2, P, 12), { tone: 'mid', crease: 'none' }) + S(k.cylinder(-176, -12, 3.2, 0, 3, P, 12), { tone: 'mid' })
  put(depth([sx, sy, 0]),
    `<g class="mill-part" data-stage="6" data-name="stand">${standSvg}</g>` +
    `<g class="mill-part" data-stage="1" data-name="duct">${ductLegs}</g>` +
    `<g class="mill-part" data-stage="4" data-name="stoneB">${st.join('')}${B.join('')}</g>` +
    `<g class="mill-part" data-stage="3" data-name="stoneA">${A.join('')}</g>` +
    `<g class="mill-part" data-stage="1" data-name="duct">${duct}</g>` +
    `<g class="mill-part" data-stage="5" data-name="spout">${spout}</g>` +
    `<g class="mill-part" data-stage="6" data-name="gapwheel">${gw.join('')}</g>`)
}

// sieve (5) on rubber mounts
{
  const base = { x: SIEVE.x - 2, y: SIEVE.y - 2, w: SIEVE.w + 4, d: SIEVE.d + 4, r: 3 }
  const out = [halo(base, 0, 4), S(k.slabOf(base, 0, 4, P, 3, 0.5), { tone: 'lo' })]
  const posts = byDepth(k.corners(SIEVE, 5))
  for (const [x, y] of posts) {
    out.push(S(k.cylinder(x, y, 3.4, 4, 2, P, 16), { tone: 'mid' }))
    out.push(S(k.cylinder(x, y, 2, 6, 24, P, 14), { tone: 'mid', crease: 'none' }))
    out.push(S(k.cylinder(x, y, 3.8, 30, 5, P, 18), { tone: 'lo' }))
  }
  const tray = { x: SIEVE.x + 1, y: SIEVE.y + 1, w: SIEVE.w - 2, d: SIEVE.d - 2, r: 3 }
  const tr = [S(k.slabOf(tray, 35, 8, P, 3, 0.8), { tone: 'hi', crease: 'lo', inner: L(k.sideSeam(tray, 38, P, 3), { tone: 'faint' }) })]
  const inner = k.insetPlan(tray, 5)
  tr.push(`<path class="mill-mesh" d="${k.pathOf(k.roundedPlan(inner, 3).map(([x, y]) => at([x, y, 43])), true)}"/>`)
  tr.push(L(k.planOutline(inner, 43, P, 3), { tone: 'mid' }))
  tr.push(D(k.dotGrid(inner.x + 3, inner.y + 3, 12, 11, 4.2, 43, P), { size: 0.42, tone: 'lo' }))
  tr.push(screws(k.corners(tray, 2.4), 43))
  put(depth([SIEVE.x + 32, SIEVE.y + 31, 0]), part(5, out.join('') + `<g data-move="sieve">${tr.join('')}</g>`, ' data-name="sieve"'))
}

// ABSTAIN hatch box in front of the sieve: the door swings open when a stage abstains
const HATCH_FRAMES = 12
{
  const out = [halo(HATCH, 0, HATCH_H), S(k.slabOf(HATCH, 0, HATCH_H, P, 3, 0.8), { tone: 'mid', inner: L(k.sideSeam(HATCH, 4, P, 3), { tone: 'faint' }) })]
  out.push(`<path class="mill-mouth" d="${k.pathOf(k.roundedPlan(k.insetPlan(HATCH, 4), 3).map(([x, y]) => at([x, y, HATCH_H])), true)}"/>`)
  out.push(L(k.planOutline(k.insetPlan(HATCH, 4), HATCH_H, P, 3), { tone: 'mid' }))
  const fy = HATCH.y + HATCH.d
  const dx0 = HATCH.x + 9, dx1 = HATCH.x + HATCH.w - 9, dz0 = 6, dz1 = 28
  // the opening behind the door, and a pile of abstained grains inside it (live shows n of them)
  out.push(`<path class="mill-mouth" d="${faceRect(dx0, dx1, fy, dz0, dz1)}"/>`)
  const pile = []
  for (let i = 0; i < 14; i++) {
    const x = dx0 + 4 + (i % 7) * 3.6 + (Math.floor(i / 7) % 2) * 1.8
    const z = dz0 + 1.6 + Math.floor(i / 7) * 2.4
    pile.push(`<circle class="mill-pile" data-i="${i}" cx="${f1(at([x, fy - 3, z])[0])}" cy="${f1(at([x, fy - 3, z])[1])}" r="1.5" style="display:none"/>`)
  }
  out.push(pile.join(''))
  const doorAt = (deg) => {
    const t = (deg * Math.PI) / 180, hgt = dz1 - dz0, th = 1.6
    const top = [0, Math.sin(t) * hgt, Math.cos(t) * hgt]
    const nrm = [0, Math.cos(t) * th, -Math.sin(t) * th]
    const b0 = [dx0, fy, dz0], b1 = [dx1, fy, dz0]
    const v = [b0, b1, G.add3(b1, top), G.add3(b0, top)]
    const verts = [...v, ...v.map((p) => G.add3(p, nrm))]
    const door = polySolid(verts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
    let svg = S(door, { tone: 'hi', crease: 'lo' })
    if (deg === 0) {
      svg += k.faceTextSvg(k.sideMatrix([dx0 + (dx1 - dx0) / 2, fy + th, 0], 19.5, P, 'left'), 'ABSTAIN', { size: 4.4, tone: 'hi', anchor: 'middle' })
      svg += D([at([dx0 + 3, fy + th, dz1 - 3]), at([dx1 - 3, fy + th, dz1 - 3])], { size: 0.45, tone: 'mid' })
    }
    // pull ring at the top edge
    const pull = G.add3(G.add3([dx0 + (dx1 - dx0) / 2, fy, dz0], G.mul3(top, 0.88)), nrm)
    svg += S(k.slabOf({ x: pull[0] - 3, y: pull[1] - 0.2, w: 6, d: 1.6, r: 0.6 }, pull[2] - 1.2, 2.4, P, 2), { tone: 'mid' })
    return svg
  }
  const frames = Array.from({ length: HATCH_FRAMES + 1 }, (_, f) => `<g data-f="${f}"${f ? ' style="display:none"' : ''}>${doorAt((f / HATCH_FRAMES) * 96)}</g>`).join('')
  // hinge knuckles
  const knuckles = [dx0 + 4, dx1 - 10].map((x) => S(wheel([x, fy + 0.8, dz0], [1, 0, 0], 1.4, 6, 12).paths, { tone: 'mid' })).join('')
  put(depth([HATCH.x + 26, HATCH.y + 15, 0]), `<g data-layer="drop"></g>` + part('hatch', out.join('') + `<g data-door>${frames}</g>` + knuckles, ' data-name="hatch"'))
}

// measure dial (7) on a post beside the sieve
{
  const [x, y] = DIAL
  const out = [S(k.cylinder(x, y, 7, 0, 2.4, P, 24), { tone: 'lo' }), S(k.cylinder(x, y, 2.6, 2.4, 42, P, 16), { tone: 'mid', crease: 'none' })]
  out.push(L(k.sideArc(x, y, 2.6, 20, P, 12), { tone: 'faint' }))
  out.push(S(k.cylinder(x, y, 4.4, 40, 4, P, 18), { tone: 'mid' }))
  out.push(dialFace(x, y, 44, 13, 7, { ticks: 50, every: 5 }))
  out.push(`<path class="iso-line" data-tone="hi" data-free="start" data-live="dial" style="stroke-width:1.2"/>`)
  // crown + lug on the +x side
  out.push(S(k.slabOf({ x: x + 12.5, y: y - 2.2, w: 4.6, d: 4.4, r: 1 }, 46, 4, P, 2), { tone: 'mid' }))
  put(depth([x, y, 0]), part(7, out.join(''), ' data-name="dial"'))
}

// taster's spoon (8) on a post, with the bell (9) on top
{
  const [x, y] = SPOON
  const post = [S(k.cylinder(x, y, 6, 0, 2.4, P, 24), { tone: 'lo' }), S(k.cylinder(x, y, 2.2, 2.4, 74, P, 16), { tone: 'mid', crease: 'none' })]
  post.push(L(k.sideArc(x, y, 2.2, 30, P, 12), { tone: 'faint' }))
  post.push(S(k.cylinder(x, y, 3.6, 60, 6, P, 16), { tone: 'mid' }))
  const arm = [S(beam([x - 2, y - 1, 63], [-6, 8, 63], 2.2, 2.2), { tone: 'mid' })]
  arm.push(S(k.cylinder(-7, 8.4, 0.9, 56, 7, P, 10), { tone: 'mid', crease: 'none' }))
  arm.push(S(k.cylinder(-7, 8.4, 4.6, 53.6, 2.6, P, 24, 0.4), { tone: 'hi', crease: 'lo' }))
  arm.push(`<path class="mill-mouth" d="${k.pathOf(k.circleRing(-7, 8.4, 3.4, 18).map(([a, b]) => at([a, b, 56.2])), true)}"/>`)
  const bell = [S(k.cylinder(x, y, 5.4, 74, 1.6, P, 24), { tone: 'mid' }), S(k.cylinder(x, y, 4.6, 75.6, 5, P, 24, 0.4), { tone: 'hi', crease: 'lo' }), S(k.cylinder(x, y, 3, 80.6, 2.4, P, 18), { tone: 'hi', crease: 'lo' }), S(k.cylinder(x, y, 1.1, 83, 3, P, 12), { tone: 'mid' })]
  put(depth([x, y, 0]),
    `<g class="mill-part" data-stage="8" data-name="spoon">${post.join('')}<g data-move="spoon">${arm.join('')}</g></g>` +
    `<g class="mill-part" data-stage="9" data-name="bell"><g data-move="bell">${bell.join('')}</g></g>`)
}

// impact engine (12): 74 scale pans, one per body leaf, on tiers grouped by the 7 top body categories
const PANS = []
{
  const groups = BODY_TOPS.map((t) => BODIES.map((b, i) => ({ ...b, i })).filter((b) => b.top === t))
  const rows = []
  for (const g of groups) for (let s = 0; s < g.length; s += 13) rows.push(g.slice(s, s + 13))
  const nRows = rows.length // 8
  const x0 = 46, wRow = 108, rowD = 9
  const front = 38
  const tiers = []
  for (let r = 0; r < nRows; r++) tiers.push({ plan: { x: x0, y: front - (r + 1) * rowD, w: wRow, d: rowD, r: 0.6 }, z: 6 + r * 4.4 })
  const out = [halo({ x: x0, y: front - nRows * rowD, w: wRow, d: nRows * rowD, r: 2 }, 0, 10)]
  const plinth = { x: x0 - 3, y: front - nRows * rowD - 3, w: wRow + 6, d: nRows * rowD + 6, r: 2 }
  out.push(S(k.slabOf(plinth, 0, 4, P, 3, 0.5), { tone: 'lo' }))
  const pansSvg = []
  for (let r = nRows - 1; r >= 0; r--) {
    const { plan, z } = tiers[r]
    out.push(S(k.slabOf(plan, 4, z - 4 + 2, P, 2, 0.4), { tone: r % 2 ? 'mid' : 'lo', crease: 'faint' }))
  }
  // pans painted back row first, then by depth inside a row
  const list = []
  rows.forEach((row, r) => {
    const { plan, z } = tiers[r]
    const top = z + 2
    const span = (row.length - 1) * 8.2
    row.forEach((b, j) => list.push({ b, x: plan.x + wRow / 2 - span / 2 + j * 8.2, y: plan.y + rowD / 2, z: top, r }))
  })
  list.sort((a, b) => depth([a.x, a.y, a.z]) - depth([b.x, b.y, b.z]))
  for (const p of list) {
    const svg = S(k.cylinder(p.x, p.y, 0.8, p.z, 4.4, P, 8), { tone: 'mid', crease: 'none' }) + S(k.cylinder(p.x, p.y, 3.3, p.z + 4.4, 1.3, P, 20, 0.3), { tone: 'hi', crease: 'lo' })
    pansSvg.push(`<g data-pan="${p.b.i}">${svg}</g>`)
    PANS.push({ i: p.b.i, id: p.b.id, top: p.b.top, at: [f1(p.x), f1(p.y), f1(p.z)] })
  }
  put(depth([x0 + 54, front - 36, 0]), part(12, out.join('') + pansSvg.join(''), ' data-name="scales"'))
}

// placement pin (10) holding the top of the chute, the chute (14), the delivery tray (15) with its freshness tag
{
  const [px, py] = PIN
  const pin = [S(k.cylinder(px, py, 6, 0, 2.4, P, 20), { tone: 'lo' }), S(k.cylinder(px, py, 2.4, 2.4, 24, P, 16), { tone: 'mid', crease: 'none' })]
  pin.push(S(k.cylinder(px, py, 4, 16, 4.4, P, 18), { tone: 'hi', crease: 'lo' }))
  pin.push(L(k.knurl(px, py, 4, 16, 20.4, 20, P), { tone: 'lo' }))
  put(depth([px, py, 0]), part(10, pin.join(''), ' data-name="pin"'))
  const a = [px + 2, py, 28], b = [TRAY.x + 18, TRAY.y + 18, 13]
  const ch = [S(beam(a, b, 13, 2.2), { tone: 'mid', crease: 'lo' })]
  const u = G.unit3(G.sub3(b, a))
  const s = G.unit3(G.cross3(u, [0, 0, 1]))
  for (const side of [-1, 1]) {
    const off = G.mul3(s, side * 6.2)
    ch.push(S(beam(G.add3(G.add3(a, off), [0, 0, 2.2]), G.add3(G.add3(b, off), [0, 0, 2.2]), 1.2, 3), { tone: 'hi', crease: 'lo' }))
  }
  // slope knob (set per profile)
  ch.push(S(wheel(G.add3(a, G.mul3(s, -7.5)), s.map((v) => -v), 3.4, 2.4, 18).paths, { tone: 'hi', crease: 'lo' }))
  put(depth([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0]) + 2, part(14, ch.join(''), ' data-name="chute"'))
  const tr = [halo(TRAY, 0, 9), S(k.slabOf(TRAY, 0, 9, P, 3, 0.8), { tone: 'mid', inner: L(k.sideSeam(TRAY, 4, P, 3), { tone: 'faint' }) })]
  const inner = k.insetPlan(TRAY, 3.4)
  tr.push(`<path class="mill-mouth" d="${k.pathOf(k.roundedPlan(inner, 3).map(([x, y]) => at([x, y, 9])), true)}"/>`)
  tr.push(L(k.planOutline(inner, 9, P, 3), { tone: 'mid' }))
  // tag post + freshness tag
  const tx = TRAY.x + TRAY.w - 4, ty = TRAY.y + TRAY.d - 4
  tr.push(S(k.cylinder(tx, ty, 1.3, 9, 24, P, 10), { tone: 'mid', crease: 'none' }))
  tr.push(S(k.cylinder(tx, ty, 2.4, 33, 1.6, P, 12), { tone: 'mid' }))
  tr.push(L(k.segment([tx, ty, 33], [tx - 6, ty + 1, 27], P), { tone: 'lo' }))
  tr.push(S(k.slabOf({ x: tx - 13, y: ty + 0.4, w: 12, d: 1, r: 0.4 }, 16, 11, P, 2), { tone: 'hi', crease: 'lo' }))
  tr.push(L(k.segment([tx - 11, ty + 1.4, 24], [tx - 4, ty + 1.4, 24], P), { tone: 'lo', free: true }), L(k.segment([tx - 11, ty + 1.4, 20.5], [tx - 6, ty + 1.4, 20.5], P), { tone: 'lo', free: true }))
  tr.push(`<g data-layer="tray"></g>`)
  put(depth([TRAY.x + 28, TRAY.y + 23, 0]), part(15, tr.join(''), ' data-name="tray"'))
}

// ---------- order and write ----------
items.sort((a, b) => a.key - b.key)
const body = [
  `<defs><radialGradient id="mill-grain-g" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#f19a95"/><stop offset=".55" stop-color="#c82924"/><stop offset="1" stop-color="#7d1612"/></radialGradient></defs>`,
  ...items.map((i) => i.svg),
  `<g data-layer="grain"><g class="mill-grain-g" transform="translate(-50 -50)"><ellipse class="mill-grain-shadow" rx="7" ry="3.6" cy="7"/><circle class="mill-grain" r="4.8"/><circle class="mill-grain-hl" r="1.4" cx="-1.5" cy="-1.6"/></g></g>`,
]
const svg = k.figureSvg({
  width: W,
  height: H,
  label: 'An isometric masala chakki mill on a bench, drawn as the RAASTA scan pipeline: a hopper takes the photo, a feed gate with a gauge reads its light and blur, two grinding stones are the two detectors, a sieve on rubber mounts is the agreement step, a hatch marked ABSTAIN collects what cannot be decided, a chaff bin takes rejects, a dial measures height, a taster spoon and a bell stand for the vision model and the reasoner, a cabinet of 12 drawers holds the 379 element types, 74 small scale pans are the body leaves, two gears are the combination rules, a pin and a chute lead to a delivery tray, and a ledger on the wall keeps the receipt with a complaint letter tucked in it.',
  body,
  className: 'mill-svg',
})

// anchors the grain visits (world points)
const ANCH = {
  sky: [HOP[0], HOP[1], 236], mouth: [HOP[0], HOP[1], 191], gate: [HOP[0], HOP[1], 140],
  duct: [-150, -12, 108], eye: [STONE[0], STONE[1], 91], gap: [STONE[0], STONE[1], 76],
  spoutTop: [-80, -6, 61], sieve: [-18, -3, 44.5], sieveFront: [-20, 26, 44], hatchMouth: [-20, 49, 34],
  sieveBack: [-18, -32, 44], chaffMouth: [-21, -83, 22],
  scales: [100, 3, 51], pin: [PIN[0], PIN[1], 31], tray: [TRAY.x + 30, TRAY.y + 26, 9.5],
  ledger: [215, -80, 90],
}
const LIVE = {
  stoneA: { c: STONE, r: 37, z0: 76, z1: 90 }, stoneB: { c: STONE, r: 37, z0: 61, z1: 74.5 },
  gauge: { c: [HOP[0], HOP[1] + 22], z: 127.1, r: 6.4 }, dial: { c: DIAL, z: 51.1, r: 11 },
  gapwheel: { c: [STONE[0], STONE[1] + 42 + 1.2 + 4.2 + 2.6, 27], r: 10 },
  clock: { c: [217, WALL.y + WALL.d + 2.8, 157], r: 9 }, pulley: { c: [-146, 74 + 12.1, 22], r: 10 },
  gearBig: { c: [RACK.x + RACK.w + 5.1, -80, 92], r: 13 }, gearSmall: { c: [RACK.x + RACK.w + 5.1, -65, 75.8], r: 8 },
}
const gen = `// GENERATED by app/site/how/tools/build-mill.mjs (anatomy kit, MIT). do not edit by hand; rerun the script.
export const P = ${JSON.stringify(P)}
export const SVG = ${JSON.stringify(svg)}
export const ANCH = ${JSON.stringify(ANCH)}
export const LIVE = ${JSON.stringify(LIVE)}
export const PANS = ${JSON.stringify(PANS)}
export const DRAWERS = ${JSON.stringify(DRAWERS)}
export const HATCH_FRAMES = ${HATCH_FRAMES}
export const DRAWER_FRAMES = 6
`
writeFileSync(OUT, gen)
const solids = (svg.match(/class="iso-solid/g) || []).length
const paths = (svg.match(/<path/g) || []).length
console.log(`wrote ${OUT}: ${(gen.length / 1024).toFixed(0)} KB, ${solids} solids (incl. hatch/drawer frames), ${paths} paths, ${PANS.length} pans, ${DRAWERS.length} drawers`)
