import { boot, head, bi, esc, getLang } from './common.js'
import { backendUrl, setBackendUrl } from '../shell/shell.js'
import './scan.css'

// LIVE SCAN: photo -> POST {api}/scan -> job id -> GET {api}/scan/{id}/events (Server-Sent Events, read with fetch).
// Each stage lights up as its event arrives and draws its real output over the photo.
// No backend / unreachable: replays a recorded real run from /content/scan-examples/ and says so.
// v1 of this page (single /analyze call) is archived at app/site/archive/scan-v1/.
boot('scan')
const page = document.getElementById('page')
const EXAMPLES = [
  { file: 'street-cart-on-footpath.json', en: 'street: cart on footpath' },
  { file: 'hallway-hospital.json', en: 'indoor: hospital hallway' },
  { file: 'night-road-patna.json', en: 'night: road in Patna' },
]

// the stages, in the order the server emits them. `wait` = the event that means "this stage is now running"
const STAGES = [
  { id: 'intake', k: '01 intake', n: 'Intake', m: 'EXIF, GPS, capture time, light + blur check', full: true },
  { id: 'detector_a', k: '02 detector A', n: 'YOLOE-11s-seg', m: 'open-vocabulary segmentation, 14 text prompts' },
  { id: 'detector_b', k: '03 detector B', n: 'OWLv2 base patch16', m: 'open-vocabulary detection, same 14 prompts' },
  { id: 'agreement', k: '04 agreement', n: 'A vs B, IoU >= 0.30', m: 'both see it: ACCEPT. one sees it: ABSTAIN. weak: REJECT', full: true },
  { id: 'footpath_mask', k: '05 footpath mask', n: 'SegFormer-B0 sidewalk', m: 'footpath vs road under each object' },
  { id: 'depth', k: '06 depth', n: 'Depth Anything V2 Small', m: 'metric depth, outdoor fine-tune' },
  { id: 'measure', k: '07 measure', n: '3 height routes', m: 'depth, vanishing point, shadow: 2 of 3 must agree', full: true },
  { id: 'vlm', k: '08 vision describer', n: 'opencode-go/mimo-v2.6-flash', m: 'reads photo + numbered boxes: scene, elements, box verdicts', wait: 'vlm_start' },
  { id: 'impact', k: '09 body impact', n: 'impact matrix lookup', m: 'block / slow / warn / none per body' },
  { id: 'reasoner', k: '10 text reasoner', n: 'opencode-go/deepseek-v4.1-flash', m: 'text only: element list, per-body notes, plain answer', wait: 'reasoner_start' },
  { id: 'placement', k: '11 placement', n: 'GPS to footpath segment', m: 'only with browser GPS or EXIF GPS' },
  { id: 'receipt', k: '12 verdict', n: 'Receipt', m: 'raasta-receipt-v1 + scan block', final: true },
]
const WIRES = [['intake', 'detector_a'], ['intake', 'detector_b'], ['detector_a', 'agreement'], ['detector_b', 'agreement'],
  ['agreement', 'footpath_mask'], ['agreement', 'depth'], ['footpath_mask', 'measure'], ['depth', 'measure'],
  ['agreement', 'vlm'], ['measure', 'impact'], ['vlm', 'reasoner'], ['impact', 'reasoner'], ['reasoner', 'placement'], ['reasoner', 'receipt'], ['placement', 'receipt']]

const HOW = [
  { n: 'Detector A: YOLOE-11s-seg', lic: 'AGPL-3.0', g: 'fast on a 4 GB GPU, gives masks', b: 'small model, invents boxes at low thresholds' },
  { n: 'Detector B: OWLv2 base', lic: 'Apache-2.0', g: 'different design and data from A, so agreement means something', b: 'slower, boxes only, loose on vague prompts' },
  { n: 'Footpath: SegFormer-B0 sidewalk', lic: 'NVIDIA SegFormer code licence; fine-tune card has none (unverified)', g: 'says if an object stands on the footpath or the road', b: 'trained on Belgian streets; rooms have no footpath class' },
  { n: 'Depth: Depth Anything V2 Small', lic: 'Apache-2.0 (Small)', g: 'distances from one photo', b: 'outdoor fine-tune, indoor metres are rough' },
  { n: 'Vision: mimo-v2.6-flash (opencode Go)', lic: 'hosted API, licence unchecked', g: 'reads rooms, hallways, steps, light: things no prompt covers', b: 'can see things that are not there; never ACCEPTs alone' },
  { n: 'Reasoner: deepseek-v4.1-flash (opencode Go)', lic: 'hosted API, licence unchecked', g: 'text only, turns all outputs into a plain answer', b: 'only as right as its inputs' },
]

page.innerHTML = head({ compact: true, kicker: { en: 'live scan', hi: 'लाइव स्कैन' }, title: { en: 'photograph anything. watch it think.', hi: 'कुछ भी फ़ोटो करें. उसे सोचते देखें.' },
  lede: { en: 'A street, a footpath, a room or a hallway. Two detectors, a footpath mask, depth, a vision model and a text model each do one job. You see every step, its model, its time and its real output.', hi: 'गली, फुटपाथ, कमरा या गलियारा. हर कदम, उसका मॉडल, समय और असली नतीजा दिखता है.' } }) + `
<div class="scan-live">
  <div class="sl-top">
    <section class="sl-input">
      <div class="sl-btns">
        <label class="btn primary">${bi({ en: 'take a photo', hi: 'फ़ोटो लें' })}<input type="file" accept="image/*" capture="environment" class="cam" aria-label="take a photo"></label>
        <label class="btn box">${bi({ en: 'upload', hi: 'अपलोड' })}<input type="file" accept="image/*" class="up" aria-label="upload a photo"></label>
      </div>
      <div class="sl-drop">${bi({ en: 'or drop a photo here', hi: 'या फ़ोटो यहाँ डालें' })}</div>
      <label class="sl-gps"><input type="checkbox" class="gps"> <span>${bi({ en: 'add my location (browser GPS, accuracy is sent too)', hi: 'मेरी लोकेशन जोड़ें' })}</span> <output class="gps-out"></output></label>
      <p class="sl-status" aria-live="polite"></p>
      <p class="sl-rec-banner"></p>
      <div><p class="sl-key" style="margin:0 0 6px">${bi({ en: 'recorded real runs (play even with no backend):', hi: 'रिकॉर्ड किए गए असली रन:' })}</p><div class="sl-examples"></div></div>
      <details class="sl-api"><summary>backend</summary><input type="url" placeholder="https://your-tunnel.trycloudflare.com" value="${esc(backendUrl())}"><button type="button" class="btn box save-api">save</button></details>
    </section>
    <section>
      <div class="sl-photo"><div class="empty">${bi({ en: 'your photo appears here, then each model draws on it', hi: 'आपकी फ़ोटो यहाँ' })}</div></div>
      <div class="sl-layers"></div>
      <p class="sl-key">solid box = detector A (YOLOE) · dashed box = detector B (OWLv2) · line + number = A and B agree (IoU) · ringed number = vision model · red = final ACCEPT</p>
    </section>
  </div>
  <div class="sl-flow-wrap"><div class="sl-flow"><svg class="wires" aria-hidden="true"></svg></div>
    <div class="sl-inspect"><h3 class="ins-h">data inspector: tap a stage</h3><pre class="ins"></pre><div class="sl-log"></div></div>
  </div>
  <section class="sl-final"><h2>result</h2><p class="muted">${bi({ en: 'The verdict appears here when the last stage finishes.', hi: 'आख़िरी कदम के बाद नतीजा यहाँ.' })}</p></section>
  <h2 class="section-title" style="font-size:28px">${bi({ en: 'how it works', hi: 'यह कैसे काम करता है' })}</h2>
  <div class="sl-how">${HOW.map((h) => `<article><h3>${esc(h.n)}</h3><span class="lic">${esc(h.lic)}</span><p class="g">${esc(h.g)}</p><p class="b">${esc(h.b)}</p></article>`).join('')}</div>
</div>`

const $ = (s) => page.querySelector(s)
const flow = $('.sl-flow')
flow.insertAdjacentHTML('beforeend', STAGES.map((s) => `<button type="button" class="sl-node wait${s.full ? ' full' : ''}${s.final ? ' final' : ''}" data-id="${s.id}">
  <span class="k"><span>${esc(s.k)}</span><span class="tm"></span></span><span class="n">${esc(s.n)}</span><span class="m">${esc(s.m)}</span><span class="o"></span></button>`).join(''))
$('.sl-examples').innerHTML = EXAMPLES.map((e, i) => `<button type="button" class="btn" data-ex="${i}">${esc(e.en)}</button>`).join('')

// ---------------- state ----------------
let run = null           // { events: {stage: data}, img, W, H, recorded }
const layers = { a: true, b: true, agree: true, mask: false, depth: false, vlm: true, final: true }
const LAYER_NAMES = { a: 'detector A', b: 'detector B', agree: 'agreement', mask: 'footpath mask', depth: 'depth', vlm: 'vision model', final: 'final' }
function drawLayerButtons() {
  $('.sl-layers').innerHTML = Object.keys(layers).map((k) => `<button type="button" data-l="${k}" aria-pressed="${layers[k]}" ${run && !hasLayer(k) ? 'disabled' : ''}>${LAYER_NAMES[k]}</button>`).join('')
}
function hasLayer(k) {
  const e = run?.events ?? {}
  return { a: e.detector_a, b: e.detector_b, agree: e.agreement, mask: e.footpath_mask?.mask_png, depth: e.depth?.depth_png, vlm: e.vlm?.ok, final: e.receipt }[k]
}
$('.sl-layers').addEventListener('click', (ev) => { const b = ev.target.closest('[data-l]'); if (!b) return; layers[b.dataset.l] = !layers[b.dataset.l]; drawLayerButtons(); paint() })
drawLayerButtons()

const status = (msg, rec = false) => { const s = $('.sl-status'); s.textContent = msg; s.classList.toggle('rec', rec) }
const log = (msg) => { const l = $('.sl-log'); l.insertAdjacentHTML('beforeend', `<div>${esc(msg)}</div>`); l.scrollTop = l.scrollHeight }

// ---------------- wires ----------------
function wires() {
  const svg = flow.querySelector('svg.wires'), fr = flow.getBoundingClientRect()
  svg.setAttribute('viewBox', `0 0 ${fr.width} ${fr.height}`)
  svg.innerHTML = WIRES.map(([a, b]) => {
    const ra = flow.querySelector(`[data-id="${a}"]`).getBoundingClientRect(), rb = flow.querySelector(`[data-id="${b}"]`).getBoundingClientRect()
    const x1 = ra.left + ra.width / 2 - fr.left, y1 = ra.bottom - fr.top, x2 = rb.left + rb.width / 2 - fr.left, y2 = rb.top - fr.top
    const my = (y1 + y2) / 2
    return `<path data-w="${a}>${b}" d="M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}"/>`
  }).join('')
  refreshWires()
}
function refreshWires() {
  for (const p of flow.querySelectorAll('svg.wires path')) {
    const [a, b] = p.dataset.w.split('>')
    const na = flow.querySelector(`[data-id="${a}"]`), nb = flow.querySelector(`[data-id="${b}"]`)
    p.classList.toggle('done', na.classList.contains('done') && nb.classList.contains('done'))
    p.classList.toggle('live', na.classList.contains('done') && nb.classList.contains('run'))
    p.classList.toggle('red', b === 'receipt' && nb.classList.contains('done'))
  }
}
addEventListener('resize', wires)
requestAnimationFrame(wires)

// ---------------- photo + canvas ----------------
function setPhoto(src) {
  const ph = $('.sl-photo')
  ph.innerHTML = `<img class="base" alt="the scanned photo"><img class="ov mask" alt=""><img class="ov depth" alt=""><canvas></canvas>`
  const img = ph.querySelector('img.base')
  img.onload = () => paint()
  img.src = src
}
function paint() {
  const ph = $('.sl-photo'), img = ph.querySelector('img.base'), cv = ph.querySelector('canvas')
  if (!img || !cv || !run || !img.naturalWidth) return
  const e = run.events, W = run.W || img.naturalWidth, H = run.H || img.naturalHeight
  const r = img.getBoundingClientRect(), dpr = devicePixelRatio || 1
  cv.width = r.width * dpr; cv.height = r.height * dpr
  const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0)
  const sx = r.width / W, sy = r.height / H
  const B = (b) => [b[0] * sx, b[1] * sy, (b[2] - b[0]) * sx, (b[3] - b[1]) * sy]
  const ink = '#111', paper = '#f3f3f3', red = '#c82924'
  c.font = '800 11px system-ui, sans-serif'; c.textBaseline = 'top'
  const tag = (x, y, t, bg = ink, fg = paper) => { const w = c.measureText(t).width + 8; c.fillStyle = bg; c.fillRect(x, Math.max(0, y - 16), w, 15); c.fillStyle = fg; c.fillText(t, x + 4, Math.max(0, y - 14)) }
  const mk = ph.querySelector('img.mask'), dp = ph.querySelector('img.depth')
  if (e.footpath_mask?.mask_png && mk.src !== e.footpath_mask.mask_png) mk.src = e.footpath_mask.mask_png
  if (e.depth?.depth_png && dp.src !== e.depth.depth_png) dp.src = e.depth.depth_png
  mk.classList.toggle('on', !!(layers.mask && e.footpath_mask?.mask_png)); dp.classList.toggle('on', !!(layers.depth && e.depth?.depth_png))
  const halo = (draw) => { c.strokeStyle = paper; c.lineWidth = 5; draw(); c.strokeStyle = ink; c.lineWidth = 2; draw() }
  if (layers.a) for (const d of e.detector_a?.boxes ?? []) { const [x, y, w, h] = B(d.box); c.setLineDash([]); halo(() => c.strokeRect(x, y, w, h)); tag(x, y, `A ${d.prompt} ${d.score.toFixed(2)}`) }
  if (layers.b) for (const d of e.detector_b?.boxes ?? []) { const [x, y, w, h] = B(d.box); c.setLineDash([6, 4]); halo(() => c.strokeRect(x, y, w, h)); c.setLineDash([]); tag(x + w - 4 - c.measureText(`B ${d.prompt} ${d.score.toFixed(2)}`).width - 4, y + h + 16, `B ${d.prompt} ${d.score.toFixed(2)}`, paper, ink) }
  c.setLineDash([])
  if (layers.agree) for (const l of e.agreement?.links ?? []) {
    const a = B(l.A), b = B(l.B), ax = a[0] + a[2] / 2, ay = a[1] + a[3] / 2, bx = b[0] + b[2] / 2, by = b[1] + b[3] / 2
    halo(() => { c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke() })
    c.beginPath(); c.arc((ax + bx) / 2, (ay + by) / 2, 13, 0, 7); c.fillStyle = ink; c.fill()
    c.fillStyle = paper; c.textAlign = 'center'; c.fillText(l.iou.toFixed(2), (ax + bx) / 2, (ay + by) / 2 - 6); c.textAlign = 'left'
  }
  if (layers.vlm && e.vlm?.ok) {
    const sent = e.vlm_start?.boxes_sent ?? []
    for (const v of e.vlm.boxes ?? []) {
      const s = sent.find((q) => q.n === v.n); if (!s) continue
      const [x, y] = B(s.box); c.beginPath(); c.arc(x + 12, y + 12, 11, 0, 7); c.fillStyle = paper; c.fill(); c.strokeStyle = ink; c.lineWidth = 2; c.stroke()
      c.fillStyle = ink; c.textAlign = 'center'; c.fillText(String(v.n), x + 12, y + 6); c.textAlign = 'left'
      tag(x + 26, y + 18, `vision: ${v.verdict}${v.what ? ' (' + v.what + ')' : ''}`, paper, ink)
    }
    // elements placed by their "where" words (left/centre/right x near/middle/far)
    const col = { left: 0.18, centre: 0.5, center: 0.5, right: 0.82 }, row = { near: 0.82, middle: 0.55, far: 0.3 }
    const used = {}
    for (const el of e.vlm.elements ?? []) {
      const w = (el.where || '').toLowerCase().split(/\s+/)
      const fx = col[w.find((q) => q in col)] ?? 0.5, fy = row[w.find((q) => q in row)] ?? 0.55
      const key = fx + ':' + fy; used[key] = (used[key] ?? 0) + 1
      const x = fx * r.width, y = fy * r.height + (used[key] - 1) * 18
      tag(Math.min(x, r.width - 120), y, `◯ ${el.name}`, paper, ink)
    }
  }
  if (layers.final && e.receipt) for (const d of e.receipt.detections ?? []) {
    if (d.status !== 'ACCEPT') continue
    const [x, y, w, h] = B(d.box); c.strokeStyle = red; c.lineWidth = 4; c.strokeRect(x, y, w, h); tag(x, y + h + 16, `ACCEPT ${d.class}${d.height_cm ? ` ${d.height_cm}±${d.height_err_cm} cm` : ''}`, red, '#fff')
  }
}
addEventListener('resize', paint)

// ---------------- stage events ----------------
const summary = {
  intake: (d) => `${d.w}x${d.h} · light ${d.condition?.light ?? '?'} · blur ${d.condition?.blur ?? d.condition?.sharpness ?? '?'} · GPS ${d.location?.source ?? 'none'}`,
  detector_a: (d) => `${d.boxes.length} boxes · ${d.device ?? ''}`,
  detector_b: (d) => `${d.boxes.length} boxes${d.ok === false ? ' · FAILED' : ''}`,
  agreement: (d) => `${d.counts.ACCEPT} ACCEPT · ${d.counts.ABSTAIN} ABSTAIN · ${d.counts.REJECT} REJECT`,
  footpath_mask: (d) => d.shares ? `footpath ${Math.round(d.shares.footpath * 100)}% · road ${Math.round(d.shares.road * 100)}% of pixels` : 'failed',
  depth: (d) => d.stats ? `near ${d.stats.near_m} m · far ${d.stats.far_m} m (outdoor scale)` : 'failed',
  measure: (d) => d.heights.length ? d.heights.map((h) => `${h.class}: ${h.height_status}${h.height_cm ? ` ${h.height_cm}±${h.height_err_cm} cm` : ''}`).join(' · ') : 'no level change to measure',
  vlm: (d) => d.ok ? `${d.scene}${d.indoor ? ' (indoor)' : ''} · ${d.elements.length} elements · ${d.seconds}s` : `NOT AVAILABLE: ${d.error}`,
  impact: (d) => d.status === 'loading' ? 'body impacts loading (matrix not built yet)' : `${d.rows.length} elements x ${d.body_count ?? Object.keys(d.bodies ?? {}).length} bodies · ${d.context}`,
  reasoner: (d) => d.ok ? `${d.elements.length} elements · ${d.bodies.length} body notes` : `NOT AVAILABLE: ${d.error}`,
  placement: (d) => d.placement?.status ?? d.placement?.why ?? 'done',
  receipt: (d) => `${d.counts.ACCEPT} ACCEPT · ${d.counts.ABSTAIN} ABSTAIN · ${d.timings.total_s}s total`,
}
function node(id) { return flow.querySelector(`[data-id="${id}"]`) }
function setState(id, st) { const n = node(id); if (!n) return; n.classList.remove('wait', 'run', 'done', 'fail'); n.classList.add(st) }
function resetFlow() {
  for (const s of STAGES) { setState(s.id, 'wait'); const n = node(s.id); n.querySelector('.o').textContent = ''; n.querySelector('.tm').textContent = '' }
  $('.sl-log').innerHTML = ''; $('.ins').textContent = ''; $('.ins-h').textContent = 'data inspector: tap a stage'
  $('.sl-final').classList.remove('on'); $('.sl-final').innerHTML = '<h2>result</h2><p class="muted">running...</p>'
  refreshWires()
}
const RUN_NEXT = { start: ['intake'], intake: ['detector_a'], detector_a: ['detector_b'], detector_b: ['agreement'], agreement: ['footpath_mask'], footpath_mask: ['depth'], depth: ['measure'], measure: ['impact'], impact: [], reasoner: ['placement'], placement: ['receipt'] }

function onEvent(ev) {
  const { stage, data, t } = ev
  run.events[stage] = data
  log(`${(t ?? 0).toFixed(2).padStart(6)} s  ${stage}`)
  if (stage === 'queued') status(data.ahead ? `queued: ${data.ahead} scan(s) ahead of you` : 'starting...', run.recorded)
  if (stage === 'intake') { run.W = data.w; run.H = data.h; if (data.image && !run.localUrl) setPhoto(data.image) }
  if (stage === 'vlm_start') setState('vlm', 'run')
  if (stage === 'reasoner_start') setState('reasoner', 'run')
  if (stage === 'error') { status(`error: ${data.error}`, true); for (const s of STAGES) if (node(s.id).classList.contains('run')) setState(s.id, 'fail') }
  const s = STAGES.find((q) => q.id === stage)
  if (s) {
    const n = node(stage)
    const failed = (stage === 'vlm' || stage === 'reasoner') && data.ok === false
    setState(stage, failed ? 'fail' : 'done')
    n.querySelector('.o').textContent = summary[stage]?.(data) ?? ''
    if (stage === 'vlm' && data.model) n.querySelector('.n').textContent = `opencode-go/${data.model}`
    const sec = data.seconds ?? data.timings?.total_s
    n.querySelector('.tm').textContent = sec != null ? `${Number(sec).toFixed(2)} s` : ''
    for (const nx of RUN_NEXT[stage] ?? []) if (!node(nx).classList.contains('done')) setState(nx, 'run')
    if (stage === 'measure' && !run.events.vlm) setState('vlm', 'run')
    inspect(stage)
  }
  if (stage === 'start') for (const nx of RUN_NEXT.start) setState(nx, 'run')
  if (stage === 'receipt') final(data)
  if (stage === 'end') status(run.recorded ? `RECORDING finished (recorded ${run.recordedAt}). This was not a live run.` : `done in ${data.total_s} s (live, ${new URL(backendUrl()).host})`, run.recorded)
  drawLayerButtons(); paint(); refreshWires()
}

function slim(o) { return JSON.stringify(o, (k, v) => (typeof v === 'string' && v.startsWith('data:image') ? `<${v.slice(5, 14)} ${Math.round(v.length * 0.75 / 1024)} KB>` : v), 2) }
function inspect(id) {
  const d = run?.events?.[id]; if (!d) return
  flow.querySelectorAll('.sl-node.sel').forEach((n) => n.classList.remove('sel')); node(id)?.classList.add('sel')
  $('.ins-h').textContent = `data inspector: ${id} (the real event payload)`
  const txt = slim(d); $('.ins').textContent = txt.length > 12000 ? txt.slice(0, 12000) + '\n... (truncated)' : txt
}
flow.addEventListener('click', (ev) => { const n = ev.target.closest('.sl-node'); if (n) inspect(n.dataset.id) })

// ---------------- final card ----------------
const GLYPH = {
  level: '<path d="M3 26h8v-7h8v-7h8V5" fill="none" stroke="currentColor" stroke-width="3"/>',
  obstacle: '<path d="M15 3v24M9 27h12" stroke="currentColor" stroke-width="3"/><circle cx="15" cy="6" r="3" fill="currentColor"/>',
  surface: '<path d="M2 22h26M8 22l4-6 3 4 4-8 3 10" fill="none" stroke="currentColor" stroke-width="3"/>',
  water: '<path d="M15 4c-5 8-8 12-8 16a8 8 0 0016 0c0-4-3-8-8-16z" fill="none" stroke="currentColor" stroke-width="3"/>',
  light: '<circle cx="15" cy="15" r="6" fill="none" stroke="currentColor" stroke-width="3"/><path d="M15 2v4M15 24v4M2 15h4M24 15h4" stroke="currentColor" stroke-width="3"/>',
  indoor: '<path d="M7 27V4h16v23M18 16h2" fill="none" stroke="currentColor" stroke-width="3"/>',
  vehicle: '<circle cx="8" cy="22" r="4" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="23" cy="22" r="4" fill="none" stroke="currentColor" stroke-width="3"/><path d="M8 22l6-10h5l4 10" fill="none" stroke="currentColor" stroke-width="3"/>',
  people: '<circle cx="10" cy="8" r="3" fill="currentColor"/><circle cx="20" cy="8" r="3" fill="currentColor"/><path d="M6 27v-12h8v12M16 27v-12h8v12" fill="none" stroke="currentColor" stroke-width="3"/>',
  other: '<rect x="5" y="5" width="20" height="20" fill="none" stroke="currentColor" stroke-width="3"/>',
}
function glyph(id) {
  const g = /step|kerb|ramp|slope|height|threshold|handrail|lift|stairs/.test(id) ? 'level'
    : /pole|bollard|box|tree|barricade|cable|guardrail|overhead|protrud|platform|cart|vendor|seating|construction|clutter|door|turning/.test(id) ? (/door|turning|clutter|rug|lift/.test(id) ? 'indoor' : 'obstacle')
      : /pothole|paving|crack|gap|drain|manhole|trench|debris|surface|garbage|zebra|grating|tactile|tree_pit|utility|footpath|path/.test(id) ? 'surface'
        : /puddle|wet|slippery|water/.test(id) ? 'water' : /dark|glare|contrast|light/.test(id) ? 'light'
          : /parked|car|two_wheeler|motorcycle|traffic|vehicle/.test(id) ? 'vehicle' : /crowd|animal/.test(id) ? 'people' : 'other'
  return `<svg viewBox="0 0 30 30" aria-hidden="true">${GLYPH[g]}</svg>`
}
function final(rc) {
  const e = run.events, v = e.vlm ?? {}, rs = e.reasoner ?? {}, imp = e.impact ?? {}
  const box = $('.sl-final'); box.classList.add('on')
  const items = [], byKey = {}
  for (const d of rc.detections ?? []) {
    if (d.status === 'REJECT') continue
    const src = d.status === 'ACCEPT' ? 'A + B agree' : (Object.keys(d.labels ?? {}).length > 1 ? 'A + B, policy downgrade' : `detector ${Object.keys(d.labels ?? {}).join('+')} only`)
    const k = `${d.class}|${d.status}|${src}`
    if (byKey[k]) { byKey[k].n++; continue }
    items.push(byKey[k] = { id: d.class_family, name: d.class, st: d.status, src, note: d.why, h: d.height_cm ? `${d.height_cm} ± ${d.height_err_cm} cm` : '', n: 1 })
  }
  for (const el of v.elements ?? []) items.push({ id: el.id, name: el.name, st: 'VISION', src: `vision model, ${el.confidence}${el.where ? ', ' + el.where : ''}`, note: el.note, n: 1 })
  const acc = items.filter((i) => i.st === 'ACCEPT').length
  const verdict = acc ? `${acc} confirmed barrier${acc > 1 ? 's' : ''}` : 'nothing confirmed'
  const bodies = imp.bodies ?? {}
  const short = (b) => b.replace(/_/g, ' ').replace('pregnant third trimester', 'pregnant').replace('no impairment adult', 'baseline adult').replace('older with walker', 'walker 60+')
  const bodyTable = imp.status === 'ok'
    ? `<p class="sl-key">${esc(imp.source)} · context: ${esc(imp.context_label)} · ${esc(imp.about ?? '')}</p>
      <table class="sl-bodies"><tr><th>element (matrix id)</th><th>seen as</th>${Object.keys(bodies).map((b) => `<th title="${esc(bodies[b])}">${esc(short(b))}</th>`).join('')}<th>all ${imp.body_count} bodies</th></tr>${(imp.rows ?? []).map((r) => `<tr><td title="${esc(r.matrix_name ?? '')}">${esc(r.matrix_name ?? r.id)}</td><td>${esc(r.status === 'ACCEPT' ? 'certain' : r.status === 'ABSTAIN' ? 'possible' : r.status === 'VLM_ONLY' ? 'vision only' : r.status)}</td>${r.bodies ? Object.keys(bodies).map((b) => { const x = r.bodies[b] ?? '?'; return `<td class="${esc(x)}">${esc(x)}</td>` }).join('') + `<td>${r.all_bodies.block} block · ${r.all_bodies.slow} slow · ${r.all_bodies.warn} warn</td>` : `<td colspan="${Object.keys(bodies).length + 1}">${esc(r.why_missing ?? 'no row')}</td>`}</tr>`).join('')}</table>`
    : `<div class="sl-loading">BODY IMPACTS LOADING. The per-body matrix is being built by another lane. No numbers are shown until it lands: nothing here is invented.</div>`
  const honest = []
  for (const d of rc.detections ?? []) if (d.status === 'ABSTAIN') honest.push(`ABSTAIN: ${d.class}. ${d.why}`)
  for (const h of e.measure?.heights ?? []) if (h.height_status !== 'ACCEPT') honest.push(`height of ${h.class}: ${h.height_status}, not printed (routes did not agree)`)
  if (!v.ok) honest.push(`vision model not available (${v.error ?? 'no answer'}): rooms, lighting and things outside the 14 prompts are not covered in this run`)
  if (!rs.ok) honest.push(`text reasoner not available (${rs.error ?? 'no answer'}): no plain-language summary`)
  for (const n of rc.notes ?? []) honest.push(n)
  box.innerHTML = `<h2>result${run.recorded ? ' (RECORDING)' : ''}</h2>
    <p class="sl-verdict">${esc(verdict)}</p>
    <p class="sl-summary">${esc(rs.ok ? rs.answer : (v.ok ? v.summary : 'Only the detectors ran. See what is certain and what is not, below.'))}</p>
    ${v.ok ? `<p class="sl-key">scene: ${esc(v.scene)}${v.indoor ? ' (indoor)' : ''} · light ${esc(v.light)} · weather ${esc(v.weather)} · surface ${esc(v.surface)}</p>` : ''}
    <h2>elements that affect movement</h2>
    <ul class="sl-els">${items.map((i) => `<li class="${i.st === 'ACCEPT' ? 'acc' : i.st === 'ABSTAIN' ? 'abs' : ''}">${glyph(i.id)}<div><b>${esc(i.name)}${i.n > 1 ? ` x${i.n}` : ''}</b>${esc(i.note ?? '')}${i.h ? `<br>height ${esc(i.h)}` : ''}<br><span class="tag">${esc(i.st)} · ${esc(i.src)}</span></div></li>`).join('') || '<li><div>none found. That is not the same as clear.</div></li>'}</ul>
    ${(v.measurements ?? []).length ? `<h2>vision model estimates (ranges, not measured)</h2><ul class="sl-ms">${v.measurements.map((m) => `<li>${esc(m.what)}: ${esc(m.low)} to ${esc(m.high)} ${esc(m.unit)} (${esc(m.how)})</li>`).join('')}</ul>` : ''}
    <h2>per body</h2>${bodyTable}
    ${rs.ok && rs.bodies?.length ? `<ul class="sl-ms">${rs.bodies.map((b) => `<li><b>${esc(b.body)}</b>: ${esc(b.text)}</li>`).join('')}</ul>` : ''}
    <h2>what is not known</h2><ul class="sl-honest">${honest.map((h) => `<li>${esc(h)}</li>`).join('')}</ul>`
}

// ---------------- live run ----------------
async function pos() {
  if (!$('.gps').checked || !navigator.geolocation) return null
  return new Promise((res) => navigator.geolocation.getCurrentPosition((p) => res(p.coords), () => res(null), { enableHighAccuracy: true, timeout: 8000, maximumAge: 30000 }))
}
$('.gps').addEventListener('change', async () => { if (!$('.gps').checked) { $('.gps-out').textContent = ''; return } $('.gps-out').textContent = 'locating...'; const c = await pos(); $('.gps-out').textContent = c ? `±${Math.round(c.accuracy)} m` : 'denied / unavailable' })

async function reachable(api) {
  try { const r = await fetch(`${api}/health`, { signal: AbortSignal.timeout(4000) }); return r.ok } catch { return false }
}
async function shrink(file) {
  // phones send 4-12 MB: above 3 MB downscale to 2048 px (EXIF is lost, so the capture time is sent from the file)
  if (file.size < 3e6) return { blob: file, note: '' }
  const bm = await createImageBitmap(file); const s = Math.min(1, 2048 / Math.max(bm.width, bm.height))
  const cv = Object.assign(document.createElement('canvas'), { width: Math.round(bm.width * s), height: Math.round(bm.height * s) })
  cv.getContext('2d').drawImage(bm, 0, 0, cv.width, cv.height)
  const blob = await new Promise((r) => cv.toBlob(r, 'image/jpeg', 0.88))
  return { blob, note: 'downscaled in the browser to 2048 px (EXIF dropped)', captured_at: new Date(file.lastModified).toISOString() }
}
async function scan(file) {
  const api = backendUrl()
  run = { events: {}, recorded: false, localUrl: URL.createObjectURL(file) }
  resetFlow(); setPhoto(run.localUrl); $('.sl-rec-banner').classList.remove('on')
  if (!api || !(await reachable(api))) {
    status(api ? `backend ${api} not reachable: playing a recorded real run instead` : 'no backend set: playing a recorded real run instead', true)
    return play(0)
  }
  status('uploading...')
  const [c, sh] = await Promise.all([pos(), shrink(file)])
  const fd = new FormData(); fd.append('image', sh.blob, file.name || 'photo.jpg')
  if (c) { fd.append('lat', c.latitude); fd.append('lon', c.longitude); fd.append('gps_error_m', Math.round(c.accuracy)) }
  if (sh.captured_at) fd.append('captured_at', sh.captured_at)
  if (sh.note) log(sh.note)
  try {
    const r = await fetch(`${api}/scan`, { method: 'POST', body: fd })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    const { job_id } = await r.json()
    status('scanning live...')
    await stream(`${api}/scan/${job_id}/events`)
  } catch (err) { status(`live scan failed (${err.message}): playing a recorded run instead`, true); play(0) }
}
async function stream(url) {
  const res = await fetch(url, { headers: { accept: 'text/event-stream' } })
  const rd = res.body.getReader(), dec = new TextDecoder(); let buf = ''
  for (;;) {
    const { value, done } = await rd.read(); if (done) break
    buf += dec.decode(value, { stream: true })
    let i
    while ((i = buf.indexOf('\n\n')) >= 0) {
      const chunk = buf.slice(0, i); buf = buf.slice(i + 2)
      const data = chunk.split('\n').filter((l) => l.startsWith('data:')).map((l) => l.slice(5).trimStart()).join('\n')
      if (data) { const ev = JSON.parse(data); onEvent(ev); if (ev.stage === 'end') return }
    }
  }
}

// ---------------- recordings ----------------
let playing = 0
async function play(i) {
  const ex = EXAMPLES[i]; const my = ++playing
  let rec
  try { rec = await (await fetch(`/content/scan-examples/${ex.file}`)).json() } catch { status('recording not found', true); return }
  run = { events: {}, recorded: true, recordedAt: rec.recorded_at }
  resetFlow()
  $('.sl-rec-banner').textContent = `RECORDING, NOT LIVE: a real run of "${rec.label}" recorded ${rec.recorded_at} on the GTX 1650 backend, replayed at its real pace. ${rec.licence ? 'Photo: ' + rec.licence + '.' : ''}`
  $('.sl-rec-banner').classList.add('on')
  status('playing a recording', true)
  let last = 0
  for (const ev of rec.events) {
    const gap = Math.min(2.5, Math.max(0, (ev.t ?? 0) - last)); last = ev.t ?? last
    await new Promise((r) => setTimeout(r, gap * 1000))
    if (my !== playing) return
    onEvent(ev)
  }
}
$('.sl-examples').addEventListener('click', (ev) => { const b = ev.target.closest('[data-ex]'); if (b) play(+b.dataset.ex) })

// ---------------- inputs ----------------
for (const sel of ['.cam', '.up']) $(sel).addEventListener('change', (e) => { const f = e.target.files?.[0]; if (f) scan(f); e.target.value = '' })
const drop = $('.sl-drop')
for (const t of ['dragenter', 'dragover']) addEventListener(t, (e) => { e.preventDefault(); drop.classList.add('over') })
for (const t of ['dragleave', 'drop']) addEventListener(t, (e) => { e.preventDefault(); if (t === 'drop' || e.target === drop) drop.classList.remove('over') })
addEventListener('drop', (e) => { const f = e.dataTransfer?.files?.[0]; if (f && f.type.startsWith('image/')) scan(f) })
$('.save-api').addEventListener('click', () => { setBackendUrl($('.sl-api input').value); status(`backend saved: ${backendUrl() || 'none'}`) })
if (getLang() === 'hi') status('')
