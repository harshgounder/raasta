// RAASTA landing page, story v2: "Isse kuch nahi hoga" (story/STORY-v2.md, beats 0-9).
// Motion grammar from story/SANTIONI-MOTION-FINE.md, rebuilt lean for this page:
//   - ONE perspective camera (fov 35, z 5). Each beat is a shot ("panel") that pins while its own camera pedestals
//     down (and, on street shots, trucks sideways to follow the cat), so depth gives every felt move: a layer at z
//     moves 5/(5-z) screen units per camera unit. Never a zoom.
//   - the next panel slides up over the current one (the current drifts up at 0.25 while it is covered), with an
//     ink rule on the incoming edge. Panels are drawn with a scissor per frame rect, so they truly overlap.
//   - the shown scroll follows the page scroll with lerp 0.08 per frame (60 fps basis). No velocity tilt, gaze drift
//     or shake (user note 00:0x: backdrops never wobble). Captions ride at 1.10 and open with an 800 ms box ease when they pass the 60% line.
//   - one ink-flood plate (beat 7 to 8), one loud hit (beat 4 horn, from the recordings), one long crane (beat 8).
// Characters are 2.5D planes (chars.js), placeholders until the painted files land. Sound is recordings only
// (sound.js). Every line of text lives in lines.js. Reduced motion or no WebGL: a still comic strip.
import * as THREE from 'three'
import './story.css'
import { initShell, reduceMotion } from '../shell/shell.js'
import { LINES, TAGS_B1, TAGS_B7, PHONE, CTA, STILL_NOTES } from './lines.js'
import { charPlane, setCharFrame, startCharWatch, charTexture, resetCharSubs } from './chars.js'
import { createSound } from './sound.js'

const INK = '#151515', PAPER = '#f3f3f3', RED = '#c82924', MARIGOLD = '#e8a33d'
const ART = `${import.meta.env.BASE_URL}art/v3/`
const FOV = 35, CZ = 5, TAN = Math.tan((FOV / 2) * Math.PI / 180)
const q = new URLSearchParams(location.search)
const SNAP = q.has('snap')                          // capture mode: no lerp, no idle time motion
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const smooth = (a, b, v) => { const x = clamp((v - a) / (b - a)); return x * x * (3 - 2 * x) }
const lerp = (a, b, k) => a + (b - a) * k

// the shell's sound gate talks about the old story; this page has its own sound toggle, so skip the gate here
try { sessionStorage.setItem('hyp.entered', '1') } catch {}
initShell({ page: 'story', withAudio: false })
const homeMark = document.querySelector('.home-mark')
if (homeMark) { homeMark.textContent = 'raasta'; homeMark.setAttribute('aria-label', 'RAASTA home') }

const hasGL = (() => { try { return !!document.createElement('canvas').getContext('webgl2') } catch { return false } })()
const ui = Object.assign(document.createElement('div'), { className: 'story-ui' })
document.body.append(ui)

if (reduceMotion.matches || !hasGL || q.has('still')) comic()
else film()

// ------------------------------------------------------------------------------------------------------------
// shared DOM pieces
function lineHTML(l, extra = '') {
  return `<div class="bx">${l.who ? `<span class="who">${l.who}</span>` : ''}<p class="hi" lang="hi">${l.hi}</p><p class="en">${l.en}</p>${extra}</div>`
}
function mapCardHTML() {
  // a generic "normal map": grey blocks, one clean blue line, a plain pin. No brand.
  return `<div class="bx mapcard" aria-hidden="true"><svg viewBox="0 0 220 150" width="220" height="150">
    <rect width="220" height="150" fill="#ecebe6"/>
    <g fill="#d9d7cf"><rect x="10" y="10" width="60" height="40"/><rect x="80" y="10" width="70" height="40"/><rect x="160" y="10" width="50" height="40"/>
    <rect x="10" y="62" width="60" height="78"/><rect x="80" y="62" width="70" height="30"/><rect x="80" y="100" width="70" height="40"/><rect x="160" y="62" width="50" height="78"/></g>
    <path d="M30 140 L30 56 L190 56 L190 20" fill="none" stroke="#3b7be0" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="190" cy="20" r="8" fill="#3b7be0"/><circle cx="30" cy="140" r="6" fill="#fff" stroke="#3b7be0" stroke-width="3"/></svg>
    <span class="mc-l">normal map</span></div>`
}
// a close-up inset cut from the approved art (santioni inset grammar: a small framed close-up rides over the wide)
function cropHTML(img, ux, uy, zoom, label, ia = 1.5) {
  const w = 240, h = 160, bw = w * zoom, bh = bw / ia
  const x = Math.min(0, Math.max(w - bw, -(ux * bw - w / 2))), y = Math.min(0, Math.max(h - bh, -(uy * bh - h / 2)))
  return `<div class="bx crop" aria-hidden="true"><div class="cimg" style="background-image:url(${ART}${img});background-size:${bw}px ${bh}px;background-position:${x}px ${y}px"></div>${label ? `<span class="crop-l">${label}</span>` : ''}</div>`
}
function phoneHTML() {
  return `<div class="bx phone" aria-label="the RAASTA route on Dadu's phone"><div class="scr">
    <b>${PHONE.title}</b>${PHONE.rows.map((r) => `<span>${r}</span>`).join('')}<i>${PHONE.foot}</i></div></div>`
}
function ctaSection() {
  const sec = document.createElement('section')
  sec.className = 'story-cta'
  sec.innerHTML = `<div class="tear" aria-hidden="true"></div>
    <div class="cta-in">
      <p class="cta-k">${CTA.head.en}</p>
      <div class="cta-row">
        <a class="cta box" href="${CTA.scan.href}"><b>${CTA.scan.label}</b><span>${CTA.scan.sub}</span></a>
        <a class="cta box red" href="${CTA.map.href}"><b>${CTA.map.label}</b><span>${CTA.map.sub}</span></a>
      </div>
      <p class="cta-tag"><b>${LINES.S11.brand}.</b> <span lang="hi">${LINES.S11.hi}</span> <small>${LINES.S11.en}</small></p>
    </div>`
  return sec
}

// ------------------------------------------------------------------------------------------------------------
// reduced motion / no WebGL: the same story as a still comic, one image per beat, captions under each
function comic() {
  document.body.classList.add('story-still')
  const beats = [
    ['bg_b0_title.png', null, 'RAASTA'],
    ['bg_b1_lane_far.png', LINES.S4],
    ['map_b2_dungeon.png', LINES.S5],
    ['bg_b1_lane_far.png', null, STILL_NOTES.b3],
    ['bg_b4_kerb.png', LINES.S6, STILL_NOTES.b4],
    ['bg_b1_lane_far.png', [LINES.S7, LINES.S2]],
    ['map_b6_dungeon_raasta.png', LINES.S8],
    ['bg_b4_kerb.png', null, STILL_NOTES.b7],
    ['bg_b8_temple.png', [LINES.S9, LINES.S10]],
  ]
  const main = document.createElement('main'); main.className = 'still'
  main.innerHTML = beats.map(([img, l, note]) => `<figure><img src="${ART}${img}" alt="" loading="lazy">
    <figcaption>${note ? `<p class="note">${note}</p>` : ''}${[l].flat().filter(Boolean).map((x) => `<div class="cap static">${lineHTML(x)}</div>`).join('')}</figcaption></figure>`).join('')
  document.body.append(main)
  document.body.append(ctaSection())
}

// ------------------------------------------------------------------------------------------------------------
function film() {
  const coarse = matchMedia('(pointer: coarse)').matches
  const maxDpr = Math.min(devicePixelRatio || 1, coarse ? 2 : 1.75)
  let dpr = Number(q.get('dpr')) || maxDpr

  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' })
  renderer.setPixelRatio(dpr)
  renderer.autoClear = false
  renderer.domElement.className = 'story-gl'
  renderer.domElement.setAttribute('aria-hidden', 'true')
  document.body.prepend(renderer.domElement)
  const cam = new THREE.PerspectiveCamera(FOV, 1, 0.05, 60)

  // screen readers: the moving overlay is hidden from them; the whole story is here as plain text, in order
  ui.setAttribute('aria-hidden', 'true')
  const sr = document.createElement('section'); sr.className = 'sr-only'; sr.setAttribute('aria-label', 'the story as text')
  const srLine = (l) => `<li>${l.who ? l.who + ': ' : ''}<span lang="hi">${l.hi}</span> (${l.en})</li>`
  sr.innerHTML = `<h1>RAASTA</h1><ol>${srLine(LINES.S4)}${srLine(LINES.S5)}<li>${STILL_NOTES.b3}</li>${srLine(LINES.S6)}<li>${STILL_NOTES.b4}</li>${srLine(LINES.S7)}${srLine(LINES.S2)}${srLine(LINES.S8)}<li>${STILL_NOTES.b7}</li>${srLine(LINES.S9)}${srLine(LINES.S10)}<li>RAASTA. <span lang="hi">${LINES.S11.hi}</span> (${LINES.S11.en})</li></ol>`
  document.body.append(sr)
  const space = Object.assign(document.createElement('div'), { className: 'story-space' })
  document.body.append(space)
  document.body.append(ctaSection())
  const sound = createSound()
  // story-tied sound events: fire once when u crosses th going forward (not on a long jump), re-arm when back above
  const armed = new Map()
  const at = (key, u, th, fn) => {
    if (u >= th) { if (!armed.get(key) && u - th < 0.8) fn(); armed.set(key, true) }
    else if (u < th - 0.15) armed.set(key, false)
  }
  let lastPaw = 0, hornDone = false                  // the horn is latched: once per visit, never on scroll back
  const paw = (m) => { if (m.userData.contact && performance.now() - lastPaw > 170) { lastPaw = performance.now(); sound.cue('cat_paws') } }

  // stable viewport height on phones: measure the large viewport (100lvh) so the URL bar does not re-layout
  const probe = Object.assign(document.createElement('div'), { className: 'lvh-probe' })
  document.body.append(probe)

  // textures
  const loader = new THREE.TextureLoader()
  const texCache = new Map()
  const tex = (name) => {
    if (texCache.has(name)) return texCache.get(name)
    const t = loader.load(ART + name, () => { t.userData.ready = true })
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4
    texCache.set(name, t); return t
  }
  const IA = { 'map_b2_dungeon.png': 1, 'map_b6_dungeon_raasta.png': 1 }
  const ia = (n) => IA[n] ?? 1.5
  // alpha gradient to fade a layer's top edge into the panel colour (temple sky)
  const fadeTopMap = (() => {
    const c = document.createElement('canvas'); c.width = 1; c.height = 64
    const g = c.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 64)
    gr.addColorStop(0, '#000'); gr.addColorStop(0.22, '#fff'); gr.addColorStop(1, '#fff')
    g.fillStyle = gr; g.fillRect(0, 0, 1, 64)
    return new THREE.CanvasTexture(c)
  })()

  let W = 1, H = 1, aspect = 1
  const halfH = (z) => (CZ - z) * TAN
  const halfW = (z) => halfH(z) * aspect

  // a backdrop plane at depth z that covers the frame for the whole camera range r = {x0, x1, y0, y1}
  function cover(scene, name, z, r, { alignX = 0, alignY = 0, fadeTop = false } = {}) {
    const a = ia(name)
    const needW = 2 * halfW(z) + Math.abs(r.x1 - r.x0), needH = 2 * halfH(z) + Math.abs(r.y1 - r.y0)
    const w = Math.max(needW, needH * a) * 1.01, h = w / a
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex(name), alphaMap: fadeTop ? fadeTopMap : null, transparent: fadeTop, depthWrite: false }))
    m.position.set((r.x0 + r.x1) / 2 + alignX * (w - needW) / 2, (r.y0 + r.y1) / 2 + alignY * (h - needH) / 2, z)
    m.renderOrder = -100 + z
    scene.add(m)
    return m
  }
  // the near kerb strip (bg_b1_lane_near: content in the top half, rows 45-512 of 1024): rises in from the bottom
  function nearStrip(scene, z, r, show = 0.22) {
    const needW = 2 * halfW(z) + Math.abs(r.x1 - r.x0)
    const w = needW * 1.02, h = w / 1.5
    const ymin = Math.min(r.y0, r.y1), hh = halfH(z)
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex('bg_b1_lane_near.png'), transparent: true, depthWrite: false }))
    m.position.set((r.x0 + r.x1) / 2, ymin - hh + show * 2 * hh - 0.456 * h, z)
    m.renderOrder = 50
    scene.add(m)
    return m
  }
  // place a character so its feet sit at a fraction of the frame height (from the bottom) at the camera's current y
  const groundY = (camY, z, frac) => camY - halfH(z) + frac * 2 * halfH(z)
  const screenX = (camX, z, f) => camX + (f * 2 - 1) * halfW(z)

  function addChar(scene, name, h, z, order = 0) {
    const m = charPlane(name, h * (aspect < 0.8 ? 0.78 : 1));        // portrait phones: figures a touch smaller in the narrow frame
 m.position.z = z; m.renderOrder = order + z; scene.add(m); m.userData.dist = 0; return m
  }
  // walking: alternate frames on distance, bob on the step, face the direction of travel
  function walk(m, x, y, { frames = null, stride = 0.1, bob = 0.012, face = 1, sway = 0 } = {}) {
    const last = m.userData.lastX ?? x
    const dx = x - last
    m.userData.dist += Math.abs(dx); m.userData.lastX = x
    const ph = m.userData.dist / stride
    const step = Math.floor(ph); m.userData.contact = step !== m.userData.step; m.userData.step = step
    if (frames) setCharFrame(m, frames[Math.floor(ph) % 2])
    const moving = Math.abs(dx) > 1e-5
    m.position.x = x
    m.position.y = y + (moving ? Math.abs(Math.sin(ph * Math.PI)) * bob : 0)
    m.rotation.z = moving ? Math.sin(ph * Math.PI) * sway : 0
    if (Math.abs(dx) > 1e-4) m.userData.setFlip(dx > 0 ? face : -face)
  }
  // the myna flaps: two drawings while it is a placeholder, a wing squash once the painted single pose lands
  function flap(m, t, rate = 7) {
    const ph = Math.sin(t * rate * Math.PI * 2)
    if (charTexture('myna_fly').real) { setCharFrame(m, 'myna_fly'); m.scale.y = m.userData.h * (0.72 + 0.28 * Math.abs(ph)) }
    else setCharFrame(m, ph > 0 ? 'myna_fly' : 'myna_fly_down')
  }
  // ripples on a puddle: thin ink rings that grow and fade (time driven, the backdrop itself never moves)
  function ripples(sc, n = 3) {
    const rings = []
    for (let i = 0; i < n; i++) {
      const m = new THREE.Mesh(new THREE.RingGeometry(0.86, 1, 48), new THREE.MeshBasicMaterial({ color: INK, transparent: true, depthWrite: false }))
      m.renderOrder = -10; sc.add(m); rings.push(m)
    }
    return (pos, t, size) => rings.forEach((m, i) => {
      const ph = (t * 0.55 + i / n) % 1
      m.position.set(pos.x, pos.y, pos.z + 0.01)
      const r = size * (0.15 + ph)
      m.scale.set(r, r * 0.28, 1); m.material.opacity = (1 - ph) * 0.85
    })
  }
  const flood = () => new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    uniforms: { p: { value: 0 }, cols: { value: 120 }, ink: { value: new THREE.Color(INK) }, mari: { value: new THREE.Color(MARIGOLD) }, paper: { value: new THREE.Color(PAPER) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform float p; uniform float cols; uniform vec3 ink, mari, paper; varying vec2 vUv;
      float h(float x){ return fract(sin(x * 127.1 + 3.7) * 43758.5453); }
      void main(){
        float c = floor(vUv.x * cols); float f = fract(vUv.x * cols);
        float o = h(c), o2 = h(c + 91.0);
        float a1 = (p - o * 0.30) / 0.42 + o2 * 0.08;          // ink streak height in this column
        float a2 = (p - 0.50 - o2 * 0.18) / 0.28;              // marigold rises after the black hold
        float tip = (1.0 - abs(f - 0.5) * 2.0) * 0.06;         // pointed streak tips
        vec3 col = paper; float a = 0.0;                        // paper = see-through: the streaks rise over the last shot
        if (vUv.y < a1 + tip) { col = ink; a = 1.0; }
        if (vUv.y < a2 + tip) { col = mari; a = 1.0; }
        gl_FragColor = vec4(col, a);
        #include <colorspace_fragment>
      }`,
  })
  const mapWipe = () => new THREE.ShaderMaterial({
    uniforms: { a: { value: tex('map_b2_dungeon.png') }, b: { value: tex('map_b6_dungeon_raasta.png') }, p: { value: 0 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform sampler2D a, b; uniform float p; varying vec2 vUv;
      void main(){
        vec4 ca = texture2D(a, vUv), cb = texture2D(b, vUv);
        float k = smoothstep(p - 0.012, p + 0.012, vUv.y);       // drawn from the top down, in step with the pedestal
        gl_FragColor = mix(ca, cb, k);
        #include <colorspace_fragment>
      }`,
  })

  // top-down map shot: fill the frame, pedestal down the route, the myna crosses
  function mapShot(sc, route) {
    const side = aspect >= 1 ? 2 * halfW(0) * 1.02 : 2 * halfH(0) * 1.2
    const mx = aspect < 1 ? (0.5 - 0.455) * side : 0
    const travel = Math.max(0.2, side - 2 * halfH(0) - 0.04)
    const mat = route ? mapWipe() : new THREE.MeshBasicMaterial({ map: tex('map_b2_dungeon.png') })
    const map = new THREE.Mesh(new THREE.PlaneGeometry(side, side), mat)
    map.position.set(mx, 0, 0); sc.add(map)
    const myna = addChar(sc, 'myna_fly', 0.6, 1.6, 5)
    return (u, t, c) => {
      const L = this.len
      // pedestal DOWN like every other shot (content rises as you scroll): END/temple first, then down to START/home
      c.x = 0; c.y = lerp(travel / 2, -travel / 2, smooth(-0.8, L + 0.8, u))
      if (route) mat.uniforms.p.value = lerp(1.03, -0.02, smooth(-0.2, L * 0.95, u))
      at(`map${route}-wings`, u, -0.4, () => sound.cue('wingbeats', { variant: route ? 1 : 0 }))
      if (route) at('b6-hint', u, 0.2, () => sound.cue('ending_resolve', { beat: 6 }))
      else at('b2-myna', u, 0.5, () => sound.cue('myna_call'))
      const k = clamp((u + 0.7) / (L + 1.4))
      const dir = route ? -1 : 1
      myna.position.set(screenX(0, 1.6, route ? lerp(1.15, -0.15, k) : lerp(-0.15, 1.15, k)), groundY(c.y, 1.6, lerp(0.02, 0.92, k)), 1.6)
      myna.rotation.z = 0.45 * dir; myna.userData.setFlip(dir); flap(myna, t)
    }
  }

  // ---------------------------------------------------------------------------------------------------------
  // the panels (beats). len = screens the shot stays pinned. u = screens since the panel pinned (negative while
  // it slides in, above len while the next one covers it). cam = this shot's own camera.
  const DEFS = [
    // 0. title: dawn over the old city, Billu wakes and walks off
    { beat: 0, len: 1.1, bg: PAPER, build(sc) {
      const r = { x0: 0, x1: 0.25, y0: 0.35, y1: -0.5 }
      cover(sc, 'bg_b0_title.png', -3, r, { alignY: 0.2 })
      const cat = addChar(sc, 'cat_walk_a', 0.32, 1.4)
      return (u, t, c) => {
        const k = smooth(-0.3, this.len + 1, u)
        c.x = lerp(r.x0, r.x1, k); c.y = lerp(r.y0, r.y1, k)
        const wk = smooth(0.25, this.len + 0.9, u)
        walk(cat, screenX(c.x, 1.4, lerp(0.16, 0.86, wk)), groundY(c.y, 1.4, 0.06), { frames: ['cat_walk_a', 'cat_walk_b'], stride: 0.06, bob: 0.008 })
        paw(cat); at('b0-purr', u, -0.6, () => sound.cue('cat_purr')); at('b0-bell', u, 0.05, () => sound.cue('temple_bell', { beat: 0 }))
      }
    } },
    // 1. the cat's street: behind Billu at 22 cm. The street acts: a vendor pushes his cart onto the footpath,
    //    the pothole ripples, a scooter tears past; each hurdle gets an ink tag as Billu passes it
    { beat: 1, len: 2.8, bg: PAPER, build(sc, P) {
      const zf = -2.5, zc = 0.35, zn = 1.1
      const pan = Math.max(1.6, (2 * halfH(zf) * 1.5 - 2 * halfW(zf)) * 0.85)
      const r = { x0: 0, x1: pan, y0: 0.35, y1: -0.45 }
      const far = cover(sc, 'bg_b1_lane_far.png', zf, r, { alignY: 0.35 })
      nearStrip(sc, zn, r, 0.2)
      const cat = addChar(sc, 'cat_walk_a', 0.6, zc)
      const myna = addChar(sc, 'myna_fly', 0.34, 0.9, 5)
      const scooter = addChar(sc, 'scooter_speed', 0.8, 0.75, 4)
      const cartM = addChar(sc, 'cart_vendor', 0.95, -0.7)
      const wheel = addChar(sc, 'cart_wheel', 0.4, -0.69)
      wheel.geometry = new THREE.PlaneGeometry(1, 1)            // spins about its centre
      const ripple = ripples(sc)
      const fw = far.geometry.parameters.width, fh = far.geometry.parameters.height
      P.tags = TAGS_B1.map((tg) => ({ ...tg, pos: new THREE.Vector3(far.position.x + (tg.uv[0] - 0.5) * fw, far.position.y + (0.5 - tg.uv[1]) * fh, zf) }))
      const pothole = P.tags.find((tg) => tg.id === 'pothole').pos
      return (u, t, c) => {
        const L = this.len, k = smooth(-0.6, L + 0.6, u), w = smooth(0, L, u)
        c.x = lerp(r.x0, r.x1, w); c.y = lerp(r.y0, r.y1, k)
        const fx = lerp(0.26, 0.44, w)
        walk(cat, screenX(c.x, zc, fx), groundY(c.y, zc, 0.12), { frames: ['cat_walk_a', 'cat_walk_b'], stride: 0.085, bob: 0.012 })
        paw(cat)
        P.catScreenX = fx
        // the vendor pushes the cart in from the right and parks it across the footpath
        const ck = smooth(0.15, 1.5, u)
        const cx = screenX(c.x, -0.7, lerp(1.25, 0.66, ck))
        walk(cartM, cx, groundY(c.y, -0.7, 0.3), { stride: 0.2, bob: 0.004 }); cartM.userData.setFlip(-1)
        const cw = cartM.scale.x                                    // negative when mirrored
        wheel.position.set(cx + cw * 0.07, groundY(c.y, -0.7, 0.3) + 0.2, -0.69)
        wheel.rotation.z = (cartM.userData.dist / 0.15)
        ripple(pothole, t, 0.32)
        // the scooter tears past once (enters fast from the right, motion lines trailing)
        const sk = clamp((u - L * 0.62) / 0.4)
        at('b1-scooter', u, L * 0.62 - 0.12, () => sound.cue('scooter_passby', { variant: 0 }))
        at('b1-myna', u, L - 0.2, () => sound.cue('myna_call'))
        scooter.visible = sk > 0 && sk < 1
        scooter.position.set(screenX(c.x, 0.75, lerp(1.4, -0.45, sk)), groundY(c.y, 0.75, 0.08), 0.75); scooter.userData.setFlip(-1)
        // Gunjan lifts off above Billu at the end of the shot (pre-announces the bird view)
        const mk = clamp((u - L + 0.2) / 1.0)
        myna.visible = mk > 0
        myna.position.set(screenX(c.x, 0.9, fx + 0.04 + mk * 0.3), groundY(c.y, 0.9, 0.32 + mk * 0.9), 0.9)
        flap(myna, t); myna.userData.setFlip(1)
      }
    } },
    // 2. bird lift 1: the top view is a dungeon map; the normal map's blue line runs through every trap.
    //    The map fills the frame; the shot pedestals from START (home) to END (temple) as Gunjan crosses
    { beat: 2, len: 1.7, bg: PAPER, build(sc) { return mapShot.call(this, sc, false) } },
    // 3. the young guy: Billu sits and watches, Kabir crosses with ease
    { beat: 3, len: 1.5, bg: PAPER, build(sc) {
      const zf = -2.5, r = { x0: 0.3, x1: 0.6, y0: 0.05, y1: -0.25 }
      cover(sc, 'bg_b1_lane_far.png', zf, r, { alignY: 0.45, alignX: -0.3 })
      nearStrip(sc, 1.1, r, 0.16)
      const kabir = addChar(sc, 'guy_kabir', 1.25, 0.1)
      const cat = addChar(sc, 'cat_walk_a', 0.44, 0.7)
      return (u, t, c) => {
        const k = smooth(-1, this.len + 1, u)
        c.x = lerp(r.x0, r.x1, k); c.y = lerp(r.y0, r.y1, k)
        cat.position.set(screenX(c.x, 0.7, 0.14), groundY(c.y, 0.7, 0.1), 0.7); cat.userData.setFlip(1)
        const wk = clamp((u + 0.4) / (this.len + 0.9))
        const x = screenX(c.x, 0.1, lerp(-0.12, 1.12, wk))
        const hop = Math.max(0, Math.sin(clamp((wk - 0.32) / 0.1) * Math.PI)) * 0.1 + Math.max(0, Math.sin(clamp((wk - 0.6) / 0.1) * Math.PI)) * 0.08
        walk(kabir, x, groundY(c.y, 0.1, 0.16) + hop, { stride: 0.14, bob: 0.018, sway: 0.02 })
        at('b3-steps', u, -0.35, () => sound.cue('young_steps')); at('b3-purr', u, 0.9, () => sound.cue('cat_purr', { gain: 0.16 }))
      }
    } },
    // 4. the old woman: same normal map, stuck at the high kerb, the horn (the one loud hit), she turns back
    { beat: 4, len: 2.3, bg: PAPER, build(sc, P) {
      const r = { x0: -0.1, x1: 0.15, y0: 0.15, y1: -0.25 }
      cover(sc, 'bg_b4_kerb.png', -1.5, r, { alignY: 0.1 })
      const kamla = addChar(sc, 'kamla_walker', 1.45, 0.3)
      const cat = addChar(sc, 'cat_walk_a', 0.42, 0.9)
      const scooter = addChar(sc, 'scooter_speed', 0.9, 1.2, 4)
      return (u, t, c) => {
        const L = this.len, k = smooth(-1, L + 1, u)
        c.x = lerp(r.x0, r.x1, k); c.y = lerp(r.y0, r.y1, k)
        // in (0..0.42), stop at the kerb (shake), horn at 0.55 of the pin, turn back from 0.62
        let f
        const p = u / L
        if (p < 0.45) f = lerp(-0.1, 0.5, smooth(-0.35, 0.45, p))
        else if (p < 0.62) f = 0.5 + (SNAP ? 0 : Math.sin(t * 9) * 0.002)
        else f = lerp(0.5, 0.18, smooth(0.62, 1.25, p))
        walk(kamla, screenX(c.x, 0.3, f), groundY(c.y, 0.3, 0.14), { stride: 0.06, bob: 0.006, sway: 0.01 })
        if (kamla.userData.contact && kamla.userData.step % 2 === 0) sound.cue('walker_taps')
        if (p >= 0.62) kamla.userData.setFlip(-1); else if (p > 0) kamla.userData.setFlip(1)
        walk(cat, screenX(c.x, 0.9, lerp(0.02, 0.2, smooth(-0.2, 0.5, p))), groundY(c.y, 0.9, 0.04), { frames: ['cat_walk_a', 'cat_walk_b'], stride: 0.06, bob: 0.008 })
        const sk = clamp((p - 0.5) / 0.12)
        at('b4-horn', p * L, 0.53 * L, () => { if (!hornDone && sound.live) { hornDone = true; sound.cue('horn_hit') } })   // THE one loud hit
        at('b4-turn', p * L, 0.64 * L, () => sound.cue('walker_taps', { variant: 'walker_tap_4', gain: 0.4 }))
        scooter.visible = sk > 0 && sk < 1
        scooter.position.set(screenX(c.x, 1.2, lerp(1.4, -0.5, sk)), groundY(c.y, 1.2, 0.02), 1.2); scooter.userData.setFlip(-1)
        P.shake = sk > 0 && sk < 1 ? 1 - Math.abs(sk - 0.5) * 2 : 0
      }
    } },
    // 5. Dadu and the kid: the question, the deadpan answer, then the phone (the one red object)
    { beat: 5, len: 2.4, bg: PAPER, build(sc) {
      const zf = -2.2, r = { x0: -0.2, x1: 0.05, y0: 0.1, y1: -0.2 }
      cover(sc, 'bg_b1_lane_far.png', zf, r, { alignY: 0.5, alignX: -1 })
      nearStrip(sc, 1.1, r, 0.14)
      const dk = addChar(sc, 'dadaji_kid', 1.35, 0.2)
      const cat = addChar(sc, 'cat_walk_a', 0.42, 0.8)
      return (u, t, c) => {
        const k = smooth(-1, this.len + 1, u)
        c.x = lerp(r.x0, r.x1, k); c.y = lerp(r.y0, r.y1, k)
        const f = lerp(0.95, 0.62, smooth(-0.8, 0.3, u))
        walk(dk, screenX(c.x, 0.2, f), groundY(c.y, 0.2, 0.15), { stride: 0.08, bob: 0.008, sway: 0.008 })
        at('b5-steps', u, -0.5, () => sound.cue('cane_and_steps', { variant: 'cane_steps_old', gain: 0.7 }))
        at('b5-kid', u, -0.25, () => sound.cue('cane_and_steps', { variant: 'kid_steps', gain: 0.45 })); at('b5-cane', u, 0.4, () => sound.cue('cane_and_steps', { variant: 'cane_tap_1' }))
        at('b5-phone', u, 1.45, () => { sound.cue('phone_tap', { variant: 'phone_tap_3' }); sound.cue('phone_tap', { variant: 'phone_tap_1', delay: 0.45 }) })
        dk.userData.setFlip(-1)
        if (!SNAP) dk.scale.y = Math.abs(dk.scale.y) // idle breathing kept off: steady plane reads cleaner
        cat.position.set(screenX(c.x, 0.8, 0.12), groundY(c.y, 0.8, 0.06), 0.8); cat.userData.setFlip(1)
      }
    } },
    // 6. bird lift 2: the same map, the RAASTA route draws itself around every trap
    { beat: 6, len: 2.0, bg: PAPER, build(sc) { return mapShot.call(this, sc, true) } },
    // 7. the walk with RAASTA: the way around each hurdle; Zoya passes on the same route
    { beat: 7, len: 2.5, bg: PAPER, build(sc, P) {
      const zf = -2.5, zc = 0.3
      const pan = Math.max(1.4, (2 * halfH(zf) * 1.5 - 2 * halfW(zf)) * 0.7)
      const r = { x0: pan * 0.15, x1: pan, y0: 0.0, y1: -0.35 }
      cover(sc, 'bg_b1_lane_far.png', zf, r, { alignY: 0.55 })
      nearStrip(sc, 1.1, r, 0.15)
      const dk = addChar(sc, 'dadaji_kid', 1.3, zc)
      const zoya = addChar(sc, 'zoya_chair', 1.0, 0.05)
      const cat = addChar(sc, 'cat_walk_a', 0.4, 0.6)
      P.tags = TAGS_B7.map((tg) => ({ ...tg, pos: new THREE.Vector3() }))
      return (u, t, c) => {
        const L = this.len, w = smooth(-0.5, L + 0.5, u)
        c.x = lerp(r.x0, r.x1, w); c.y = lerp(r.y0, r.y1, smooth(-1, L + 1, u))
        // the way around: they step out toward the kerb ramp, then back in past the drain (a depth detour, staged)
        const pin = u / L, bump = (a, b) => smooth(a, a + 0.08, pin) * (1 - smooth(b - 0.08, b, pin))
        const dz = 0.35 * bump(0.14, 0.4) - 0.3 * bump(0.58, 0.84)
        dk.position.z = zc + dz
        const dx = screenX(c.x, zc + dz, 0.52)
        walk(dk, dx, groundY(c.y, zc + dz, 0.15 - dz * 0.12), { stride: 0.1, bob: 0.01, sway: 0.01 })
        if (dk.userData.contact && dk.userData.step % 3 === 0) sound.cue('cane_and_steps', { variant: dk.userData.step % 2 ? 'cane_tap_1' : 'cane_tap_2' })
        at('b7-kid', u, -0.2, () => sound.cue('cane_and_steps', { variant: 'kid_steps', gain: 0.4 }))
        at('b7-zoya', u, L * 0.3 + 0.2, () => sound.cue('wheelchair_roll')); at('b7-myna', u, L * 0.6, () => sound.cue('myna_call'))
        walk(cat, screenX(c.x, 0.6, 0.3 + Math.sin(u * 2.2) * 0.02), groundY(c.y, 0.6, 0.08), { frames: ['cat_walk_a', 'cat_walk_b'], stride: 0.07, bob: 0.01 })
        paw(cat)
        const zk = clamp((u - L * 0.3) / (L * 0.7 + 0.8))
        zoya.visible = zk > 0 && zk < 1
        walk(zoya, screenX(c.x, 0.05, lerp(-0.2, 1.25, zk)), groundY(c.y, 0.05, 0.2), { stride: 0.2, bob: 0.004 })
        for (const tg of P.tags) tg.pos.set(dx + 0.15, dk.position.y + 1.42, zc + dz)
        P.pin = u / L
      }
    } },
    // ink flood plate: white to black streaks, a black hold, then marigold rises (colour arrives)
    { beat: 7.5, len: 0.9, bg: PAPER, overlay: true, build(sc) {
      const mat = flood(); mat.uniforms.cols.value = Math.round(clamp(W / 11, 40, 160))
      const m = new THREE.Mesh(new THREE.PlaneGeometry(2 * halfW(0), 2 * halfH(0)), mat); sc.add(m)
      return (u, t, c) => { c.x = 0; c.y = 0; mat.uniforms.p.value = clamp((u + 1) / (this.len + 1.3)) }   // streaks already rising as the plate slides in (never a blank panel)
    } },
    // 8. arrival in marigold, the payoff lines, then the one long crane up into the sky with the tagline
    { beat: 8, len: 3.2, bg: MARIGOLD, build(sc, P) {
      // the crane stays inside the painting (the plate is sized for the whole rise), so no edge ever shows
      const zf = -2.0, crane = 1.35
      const r = { x0: 0, x1: 0, y0: 0, y1: -0.2 }
      cover(sc, 'bg_b8_temple.png', zf, { x0: 0, x1: 0, y0: r.y1, y1: r.y1 + crane }, { alignY: 0 })
      const dk = addChar(sc, 'dadaji_kid', 1.1, 0.2)
      const kamla = addChar(sc, 'kamla_walker', 1.05, 0.05)
      const cat = addChar(sc, 'cat_walk_a', 0.38, 0.75)
      const myna = addChar(sc, 'myna_fly', 0.45, 1.2, 5)
      // Dadu holds up his phone to Kamla: the red screen (the product) is the one red thing in the frame
      const phone = new THREE.Mesh(new THREE.PlaneGeometry(0.075, 0.13), new THREE.MeshBasicMaterial({ color: RED }))
      phone.renderOrder = 10; sc.add(phone)
      return (u, t, c) => {
        const L = this.len
        const cr = smooth(1.5, L + 0.8, u)                       // the crane: camera rises, the street sinks away
        c.x = 0; c.y = lerp(r.y0, r.y1, smooth(-1, 1.5, u)) + cr * crane
        const base = lerp(r.y0, r.y1, smooth(-1, 1.5, u))
        walk(dk, screenX(0, 0.2, lerp(0.05, 0.36, smooth(-0.9, 0.6, u))), groundY(base, 0.2, 0.12), { stride: 0.08, bob: 0.008, sway: 0.008 })
        kamla.position.set(screenX(0, 0.05, 0.7), groundY(base, 0.05, 0.16), 0.05); kamla.userData.setFlip(-1)
        const ph = smooth(0.7, 1.1, u)
        at('b8-swell', u, -0.6, () => sound.cue('ending_resolve', { beat: 8 })); at('b8-bell', u, 0.45, () => sound.cue('temple_bell', { beat: 8 }))
        at('b8-wings', u, 1.5, () => sound.cue('wingbeats'))
        phone.visible = ph > 0.01 && !charTexture('dadaji_kid').real   // the painted pair has no free hand: a floating red patch reads as a glitch
        phone.position.set(dk.position.x + Math.abs(dk.scale.x) * 0.1, dk.position.y + dk.scale.y * (0.52 + 0.1 * ph), 0.21)
        phone.scale.setScalar(Math.max(0.01, ph) * (aspect < 0.8 ? 0.7 : 1))
        walk(cat, screenX(0, 0.75, lerp(-0.05, 0.22, smooth(-0.8, 0.7, u))), groundY(base, 0.75, 0.04), { frames: ['cat_walk_a', 'cat_walk_b'], stride: 0.06, bob: 0.008 })
        const mk = smooth(1.4, L + 0.9, u)
        myna.visible = mk > 0.001
        myna.position.set(screenX(0, 1.2, lerp(0.3, 0.75, mk)), groundY(base, 1.2, 0.25) + mk * (crane + 1.6), 1.2)
        myna.rotation.z = 0.5; myna.userData.setFlip(1); flap(myna, t)
      }
    } },
  ]

  // ---------------------------------------------------------------------------------------------------------
  let panels = [], rides = [], total = 0
  function layout() {
    W = innerWidth; H = Math.max(probe.offsetHeight || innerHeight, innerHeight); aspect = W / H
    renderer.setSize(W, H, false)
    renderer.domElement.style.height = H + 'px'
    cam.aspect = aspect; cam.updateProjectionMatrix()
    for (const p of panels) p.scene.traverse((o) => { o.geometry?.dispose?.(); o.material?.dispose?.() })   // materials only; shared textures stay
    resetCharSubs()
    let A = 0
    panels = DEFS.map((d, i) => {
      const P = { ...d, i, A, scene: new THREE.Scene(), cam: { x: 0, y: 0 }, tags: [] }
      P.update = d.build.call(P, P.scene, P)
      A += (d.len + 1) * H
      return P
    })
    const last = panels.at(-1)
    total = last.A + last.len * H + H
    space.style.height = total + 'px'
    buildRides()
  }

  // riding DOM: captions, insets, the wordmark, tags. S = the scroll y where the item's centre crosses the 62% line
  function ride(html, panel, u, cls, side = 'l') {
    const el = document.createElement('div'); el.className = `ride ${cls} side-${side}`; el.innerHTML = html
    ui.append(el)
    rides.push({ el, S: panels[panel].A + u * H, h: 0, inState: false })
  }
  function buildRides() {
    ui.innerHTML = ''; rides = []
    const sub = (l, p, u, side) => ride(lineHTML(l), p, u, 'cap', side)
    ride(`<div class="bx title"><h1 class="wordmark"><span>RAASTA</span></h1><p class="scroll-hint">scroll</p></div>`, 0, -0.18, 'title-ride', 'c')
    sub(LINES.S4, 1, 0.25, 'l')
    ride(mapCardHTML(), 1, 0.55, 'inset', 'r')
    ride(cropHTML('bg_b1_lane_far.png', 0.66, 0.86, 3.2, 'pothole + open drain'), 1, 1.75, 'inset', 'l')
    sub(LINES.S5, 2, 0.55, 'l')
    ride(cropHTML('bg_b4_kerb.png', 0.62, 0.47, 2.6, 'kerb: 18 cm, no ramp'), 4, 0.75, 'inset', 'l')
    sub(LINES.S6, 4, 1.75, 'r')
    sub(LINES.S7, 5, 0.35, 'l')
    sub(LINES.S2, 5, 1.0, 'r')
    ride(phoneHTML(), 5, 1.65, 'inset phone-ride', 'r')
    sub(LINES.S8, 6, 0.6, 'l')
    sub(LINES.S9, 9, 0.25, 'l')
    sub(LINES.S10, 9, 0.85, 'r')
    ride(`<div class="bx lockup"><p class="brand">${LINES.S11.brand}.</p><p class="hi" lang="hi">${LINES.S11.hi}</p><p class="en">${LINES.S11.en}</p></div>`, 9, 2.75, 'tagline', 'c')
    for (const r of rides) r.h = r.el.offsetHeight
    // tags
    for (const P of panels) for (const tg of P.tags) {
      const el = document.createElement('div'); el.className = 'tag'; el.innerHTML = `<span>${tg.en}</span>`
      ui.append(el); tg.el = el; tg.on = false
    }
    // the painted logo replaces the type wordmark once it exists
    const img = new Image()
    img.onload = () => { const h1 = ui.querySelector('.wordmark'); if (h1) { h1.innerHTML = ''; img.alt = 'RAASTA'; h1.append(img) } }
    img.src = `${ART}chars/logo_raasta.png`
  }

  // ---------------------------------------------------------------------------------------------------------
  let target = scrollY, shown = SNAP ? scrollY : 0, last = performance.now(), tAcc = 0
  addEventListener('scroll', () => { target = scrollY }, { passive: true })
  let lastW = innerWidth, lastH = innerHeight
  let rt = 0
  addEventListener('resize', () => {
    // phones: ignore the URL bar showing/hiding (height-only change under 160 px); desktop: any change relayouts
    if (coarse && innerWidth === lastW && Math.abs(innerHeight - lastH) < 160) return
    clearTimeout(rt); rt = setTimeout(() => { lastW = innerWidth; lastH = innerHeight; layout() }, 150)
  })
  const v = new THREE.Vector3()
  const ink = new THREE.Color(INK)
  let frames = 0, slow = 0, fast = 0

  function frame(now) {
    const dt = Math.min(0.1, (now - last) / 1000); last = now
    tAcc = SNAP ? shown / 160 : tAcc + dt          // capture mode: element time follows scroll so frames differ
    target = scrollY
    const prev = shown
    const k = SNAP ? 1 : 1 - Math.pow(1 - (coarse ? 0.22 : 0.08), dt * 60)
    shown = Math.abs(target - shown) < 0.05 ? target : lerp(shown, target, k)
    const s = shown

    renderer.setScissorTest(true)
    renderer.setScissor(0, 0, W, H); renderer.setClearColor(PAPER); renderer.clear()
    const vis = {}, prog = {}
    for (let i = 0; i < panels.length; i++) {
      const P = panels[i], next = panels[i + 1]
      const E = P.A + P.len * H
      // an overlay plate (the ink flood) does not slide: it is fixed to the screen and floods over the shot below it
      const gone = next ? (next.overlay ? next.A + 0.7 * H : next.A) : Infinity
      if (s < P.A - H || s >= gone) { hideTags(P); continue }
      const y = P.overlay ? 0 : s < P.A ? P.A - s : s > E && !next?.overlay ? -(s - E) * 0.25 : 0       // frame top on screen (px)
      const u = (s - P.A) / H
      P.update(u, tAcc, P.cam)
      // backdrops never wobble: the camera only pedestals/trucks with scroll (user note 00:0x: no sway, no shake, no tilt)
      cam.position.set(P.cam.x, P.cam.y, CZ)
      cam.rotation.set(0, 0, 0)
      cam.updateMatrixWorld()
      const bottom = next && !next.overlay && s > next.A - H ? next.A - s : H     // where the next panel's top edge is
      const top = Math.max(0, y), bot = Math.min(H, y + H, bottom)
      if (bot <= top) { hideTags(P); continue }
      renderer.setViewport(0, -y, W, H)
      renderer.setScissor(0, H - bot, W, bot - top)
      if (!P.overlay) { renderer.setClearColor(P.bg); renderer.clear() }
      renderer.render(P.scene, cam)
      if (y > 0) { renderer.setScissor(0, Math.max(0, H - y - 3), W, 3); renderer.setClearColor(ink); renderer.clear() }  // the ink rule on the incoming edge
      // sound: share of the screen this beat holds, and its pinned progress
      const share = (bot - top) / H
      const b = Math.floor(P.beat)
      vis[b] = Math.max(vis[b] ?? 0, share); prog[b] = Math.max(prog[b] ?? -1, (s - P.A) / (P.len * H))
      // tags follow their world points
      for (const tg of P.tags) {
        v.copy(tg.pos).project(cam)
        const tx = (v.x + 1) / 2 * W, ty = (1 - v.y) / 2 * H + y
        let want
        if (P.beat === 1) want = u > -0.2 && (tx < (P.catScreenX + 0.22) * W || u > P.len * 0.85)
        else want = P.pin != null && P.pin > tg.at && P.pin < tg.at + 0.3
        const inside = ty > top + 20 && ty < bot - 10 && tx > 10 && tx < W - 10
        const hw = tg.hw ?? (tg.hw = (tg.el.firstChild.offsetWidth >> 1) || 60), lx = clamp(tx, 12 + hw, W - 12 - hw)   // keep the label on screen
        tg.el.style.transform = `translate3d(${lx.toFixed(1)}px, ${ty.toFixed(1)}px, 0)`
        tg.el.classList.toggle('on', want && inside)
      }
    }
    renderer.setScissorTest(false)

    // riding text: centre crosses the 62% line at S, moves at 1.10
    for (const r of rides) {
      const cy = 0.62 * H + (r.S - s) * 1.1
      const off = cy < -r.h || cy > H + r.h
      r.el.style.visibility = off ? 'hidden' : 'visible'
      if (off) continue
      r.el.style.transform = `translate3d(0, ${(cy - r.h / 2).toFixed(1)}px, 0)`
      if (!r.inState && cy < 0.74 * H) { r.inState = true; r.el.classList.add('in') }
      else if (r.inState && cy > 0.86 * H) { r.inState = false; r.el.classList.remove('in') }
      r.el.style.opacity = clamp((cy - r.h / 2 - 0.02 * H) / (0.1 * H)).toFixed(3)
    }
    sound.update(vis)

    // adaptive quality: drop the pixel ratio when frames run long, raise it back slowly when there is room
    frames++
    if (dt > 1 / 45) slow++; else if (dt < 1 / 58) fast++
    if (frames >= 90) {
      if (slow > 30 && dpr > 0.75) { dpr = Math.max(0.75, dpr * 0.8); renderer.setPixelRatio(dpr); renderer.setSize(W, H, false) }
      else if (fast > 85 && dpr < maxDpr) { dpr = Math.min(maxDpr, dpr * 1.1); renderer.setPixelRatio(dpr); renderer.setSize(W, H, false) }
      frames = slow = fast = 0
    }
    requestAnimationFrame(frame)
  }
  function hideTags(P) { for (const tg of P.tags) tg.el?.classList.remove('on') }

  layout()
  startCharWatch()
  if (q.has('y')) { scrollTo(0, Number(q.get('y'))); target = shown = scrollY }
  requestAnimationFrame(frame)
  window.__story = { sound: () => sound.cues.map((c) => ({ name: c.name, loaded: c.variants.some((v) => !!v.buf), fired: c.fired ?? 0, gain: c.g ? +c.g.gain.value.toFixed(3) : null })), get shown() { return shown }, get total() { return total }, panels: () => panels.map((p) => ({ beat: p.beat, A: p.A, len: p.len })), ready: () => [...texCache.values()].every((t) => t.userData.ready) }
}
