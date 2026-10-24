// /how v2: the whole internal data flow as an anatomy-style figure (a masala chakki mill), the 17 stages as cards,
// and a ledger of the numbers we do not like. v1 is in app/site/archive/how-v1/.
import { boot, head, bi, esc } from './common.js'
import '../../how/tools/kit/iso.css'
import './how-mill.css'
import './how.css'
import { SVG } from './how-mill.gen.js'
import { RUNS } from './how-runs.gen.js'
import { STAGES, SOURCES, LEDGER } from './how-data.js'
import { mountMill } from './how-live.js'

boot('how')
const page = document.getElementById('page')
const srcKeys = Object.keys(SOURCES)
const fn = (keys) => keys.map((k) => `<a class="fn" href="#src-${k}" title="${esc(SOURCES[k].file)}">${srcKeys.indexOf(k) + 1}</a>`).join('')
const stageByN = new Map(STAGES.map((s) => [s.n, s]))

// timing of a stage in the selected recording (sum of the events that belong to it)
function timingOf(stage, run) {
  if (!stage.events.length) return 'not part of the scan: runs when someone routes or reports'
  const evs = run.events.filter((e) => stage.events.includes(e.stage))
  if (!evs.length) return ''
  const idx = run.events.findIndex((e) => e.stage === evs[evs.length - 1].stage)
  const done = run.events[idx].t
  const prev = idx > 0 ? run.events[idx - 1].t : 0
  return `${run.id} recording: done at t ${done.toFixed(2)} s (${Math.max(0, done - prev).toFixed(2)} s)`
}

function cardHtml(s, run, { compact = false } = {}) {
  return `<article class="stage-card" data-n="${s.n}">
    <header><span class="sc-n">${String(s.n).padStart(2, '0')}</span><h3>${esc(s.name)}</h3><span class="sc-part">${esc(s.part)}</span></header>
    <dl>
      <div><dt>in</dt><dd>${esc(s.input)}</dd></div>
      <div><dt>out</dt><dd>${esc(s.output)}</dd></div>
      <div><dt>model</dt><dd>${esc(s.model)}</dd></div>
      <div class="sc-num"><dt>measured</dt><dd>${esc(s.number)}${fn(s.numSrc)}</dd></div>
      <div><dt>goes wrong</dt><dd>${esc(s.fail)}</dd></div>
      <div><dt>we then</dt><dd>${esc(s.response)}${fn(s.src)}</dd></div>
      ${compact ? '' : ''}
      <div class="sc-time"><dt>this run</dt><dd data-timing="${s.n}">${esc(timingOf(s, run))}${s.events.length ? fn(['rec']) : ''}</dd></div>
    </dl>
  </article>`
}

let run = RUNS[0]
page.innerHTML = head({
  compact: true,
  kicker: { en: 'how it works', hi: 'यह कैसे काम करता है' },
  title: { en: 'the scan mill', hi: 'स्कैन की चक्की' },
  lede: { en: 'Every scan, drawn as a masala chakki. Two stones must turn together or nothing grinds; what the mill cannot decide drops through the ABSTAIN hatch. Hover or tap a part, or run a recorded photo through it. Every number is from our own logs, the bad ones too.', hi: 'हर स्कैन, एक मसाला चक्की की तरह. दो पत्थर साथ घूमें तभी पिसाई; जो तय न हो, वह ABSTAIN खिड़की से गिरता है. किसी हिस्से पर जाएँ या एक रिकॉर्ड की हुई फ़ोटो चलाएँ. हर संख्या हमारे अपने लॉग से है, खराब वाली भी.' },
}) + `
<section class="mill-wrap" aria-label="the scan mill">
  <figure class="iso mill-plate" data-theme="light">
    <div class="mill-corners" aria-hidden="true">
      <span data-corner="fig">Fig 1</span><span data-corner="title">The scan mill</span>
      <span data-corner="hint">hover or tap a part</span><span data-corner="readout" data-readout>idle</span>
    </div>
    <div class="mill-stage" tabindex="0" role="group" aria-label="mill figure: use the arrow keys to step through the 17 stages">${SVG}</div>
  </figure>
  <aside class="mill-side">
    <div class="mill-controls">
      <label class="field">${bi({ en: 'recorded photo', hi: 'रिकॉर्ड की हुई फ़ोटो' })}
        <select data-run>${RUNS.map((r, i) => `<option value="${i}">${esc(r.id)}: ${esc(r.label)}, ${r.client_total_s} s</option>`).join('')}</select></label>
      <div class="row">
        <button class="btn red" type="button" data-play>${bi({ en: 'run a photo through', hi: 'फ़ोटो चलाएँ' })}</button>
        <button class="btn" type="button" data-prev aria-label="previous stage">&larr;</button>
        <button class="btn" type="button" data-next aria-label="next stage">&rarr;</button>
      </div>
      <p class="mill-rec" data-rec></p>
    </div>
    <div class="mill-live" aria-live="polite">
      <div class="ml-clock"><span data-clock>0.00</span><small> s recorded server time</small></div>
      <p class="ml-say" data-say>press run: the grain is the photo, and it travels the stages in the order the scan really ran them.</p>
      <ul class="ml-counts"><li><i class="dot dot-accept"></i>ACCEPT <b data-c="ACCEPT">0</b></li><li><i class="dot dot-abstain"></i>ABSTAIN <b data-c="ABSTAIN">0</b></li><li><i class="dot dot-reject"></i>REJECT <b data-c="REJECT">0</b></li></ul>
    </div>
    <div class="mill-card" data-card>${cardHtml(STAGES[0], run)}</div>
  </aside>
</section>
<ul class="mill-keys" aria-label="legend">
  <li><i class="k-grain"></i>the red grain: the photo's evidence that survives every stage (the one red part)</li>
  <li><i class="k-hatch"></i>the hatch marked ABSTAIN: where the mill honestly jams</li>
  <li><i class="k-chaff"></i>the chaff bin behind the sieve: REJECT</li>
  <li><i class="k-pan"></i>74 pans, one per body leaf: during a run each pan sinks and darkens by its verdict (block darkest, then cost, then warn; none stays white)</li>
</ul>
<p class="mill-caption">Short stages are stretched to about a second so you can see them; the clock shows the recorded time. Stages 14, 15 and 17 are not part of a scan, so the recording has no time for them. Speed: one worker on a GTX 1650, one job at a time${fn(['live'])}.</p>

<h2 class="section-title">${bi({ en: 'the 17 stages', hi: '17 चरण' })}</h2>
<p class="list-note">${bi({ en: 'Card order is the pipeline order. In a live scan the vision check starts right after agreement and runs beside the ground and depth models, and body impact is read before placement.', hi: 'कार्ड पाइपलाइन के क्रम में हैं. असली स्कैन में विज़न जाँच सहमति के बाद शुरू होती है और साथ-साथ चलती है.' })}${fn(['live'])}</p>
<ol class="stage-list">${STAGES.map((s) => `<li id="stage-${s.n}">${cardHtml(s, run)}</li>`).join('')}</ol>

<h2 class="section-title">${bi({ en: 'what we are bad at', hi: 'हम किसमें कमज़ोर हैं' })}</h2>
<p class="list-note">${bi({ en: 'The ledger nailed to the mill wall. These are measured, not modest.', hi: 'चक्की की दीवार पर टँगा खाता. ये मापे हुए हैं.' })}</p>
<ol class="bad-ledger">${LEDGER.map((l) => `<li><span class="bl-num">${esc(l.num)}</span><span class="bl-what">${esc(l.what)}${fn(l.src)}</span></li>`).join('')}</ol>

<h2 class="section-title small">${bi({ en: 'sources', hi: 'स्रोत' })}</h2>
<ol class="sources">${srcKeys.map((k) => `<li id="src-${k}"><code>${esc(SOURCES[k].file)}</code> ${esc(SOURCES[k].what)}</li>`).join('')}</ol>
<p class="list-note muted">${bi({ en: 'Drawn with the anatomy figure kit (MIT). Stage cards are in English only for now.', hi: 'anatomy किट (MIT) से बना. कार्ड अभी सिर्फ़ अंग्रेज़ी में.' })}</p>`

// ---------- wiring ----------
const svg = page.querySelector('.mill-svg')
const card = page.querySelector('[data-card]')
const readoutCorner = page.querySelector('[data-readout]')
const clockEl = page.querySelector('[data-clock]')
const sayEl = page.querySelector('[data-say]')
const recEl = page.querySelector('[data-rec]')
const parts = [...svg.querySelectorAll('.mill-part')]
let shown = 1, hovering = false

function show(n, { from = 'hover' } = {}) {
  const key = String(n)
  parts.forEach((p) => p.classList.toggle('hot', p.dataset.stage === key))
  if (n === 'drive') {
    card.innerHTML = `<article class="stage-card"><header><span class="sc-n">DR</span><h3>The drive</h3><span class="sc-part">one motor, one belt: one worker</span></header><dl>
      <div><dt>what it is</dt><dd>the scan server runs one worker thread on one GPU, a GTX 1650 with 4 GB${fn(['live', 'results'])}</dd></div>
      <div class="sc-num"><dt>measured</dt><dd>two scans posted 0.3 s apart: the second waited 4.98 s and finished at 11.26 s${fn(['live'])}</dd></div>
      <div><dt>goes wrong</dt><dd>a crowd of uploads queues up behind one job</dd></div>
      <div><dt>we then</dt><dd>tell each upload how many jobs are ahead of it (the event log starts with "queued, ahead: n")${fn(['rec'])}</dd></div></dl></article>`
    return
  }
  if (n === 'hatch' || n === 'reject') {
    card.innerHTML = n === 'hatch'
      ? `<article class="stage-card"><header><span class="sc-n">AB</span><h3>The ABSTAIN hatch</h3><span class="sc-part">where the mill honestly jams</span></header><dl>
          <div><dt>what drops in</dt><dd>a detection only one detector saw (score 0.25 or more), an agreed object standing on the carriageway, a height below the bar, a photo with no place</dd></div>
          <div class="sc-num"><dt>measured</dt><dd>2,098 ABSTAIN vs 330 ACCEPT in the 313-image batch; 1,623 of them because only detector B saw it${fn(['results'])}</dd></div>
          <div><dt>we then</dt><dd>show it as unknown on the map, never as clear: no ACCEPT means unknown, not safe${fn(['rec'])}</dd></div></dl></article>`
      : `<article class="stage-card"><header><span class="sc-n">RJ</span><h3>The chaff bin</h3><span class="sc-part">REJECT</span></header><dl>
          <div><dt>what drops in</dt><dd>boxes neither rule keeps: one detector only, below a 0.25 score</dd></div>
          <div class="sc-num"><dt>measured</dt><dd>6,958 REJECT in the 313-image batch${fn(['results'])}</dd></div>
          <div><dt>we then</dt><dd>keep them in the receipt, never on the map${fn(['rec'])}</dd></div></dl></article>`
    return
  }
  const s = stageByN.get(Number(n))
  if (!s) return
  shown = s.n
  card.innerHTML = cardHtml(s, run)
  if (from === 'key') svg.closest('.mill-stage').setAttribute('aria-label', `stage ${s.n} of 17: ${s.name}, ${s.part}`)
}
for (const p of parts) {
  p.addEventListener('pointerenter', () => { hovering = true; show(p.dataset.stage) })
  p.addEventListener('pointerleave', () => { hovering = false })
  p.addEventListener('click', () => { show(p.dataset.stage); if (matchMedia('(max-width: 900px)').matches) card.scrollIntoView({ block: 'nearest', behavior: 'smooth' }) })
}
const stepTo = (d) => show(((shown - 1 + d + 17) % 17) + 1, { from: 'key' })
page.querySelector('[data-prev]').addEventListener('click', () => stepTo(-1))
page.querySelector('[data-next]').addEventListener('click', () => stepTo(1))
svg.closest('.mill-stage').addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); stepTo(1) }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); stepTo(-1) }
})

const setRec = () => { recEl.innerHTML = `<a href="${esc(run.source_url)}" rel="noopener">${esc(run.file)}</a>, ${esc(run.licence)}. Recorded ${esc(run.recorded_at)}, client total ${run.client_total_s} s.${fn(['rec', 'live'])}` }
setRec()
const mill = mountMill(svg, {
  onStage: (n) => { if (!hovering) show(n, { from: 'run' }) },
  onReadout: (r) => {
    if (r.tick) { if (r.t != null) clockEl.textContent = r.t.toFixed(2); return }
    if (r.done) { readoutCorner.textContent = `done: receipt ${run.receipt.id}`; page.querySelector('[data-play] span').textContent = 'run it again'; return }
    sayEl.textContent = r.say
    readoutCorner.textContent = `${String(r.seg.n).padStart(2, '0')} ${stageByN.get(r.seg.n)?.name ?? ''} · ${r.at}`
    if (r.seg.outside) clockEl.textContent = '--'
  },
  onCounts: (c) => { for (const k of ['ACCEPT', 'ABSTAIN', 'REJECT']) page.querySelector(`[data-c="${k}"]`).textContent = c[k] },
})
page.querySelector('[data-play]').addEventListener('click', () => { mill.play(run) })
page.querySelector('[data-run]').addEventListener('change', (e) => {
  run = RUNS[Number(e.target.value)]
  setRec(); mill.stop()
  clockEl.textContent = '0.00'; sayEl.textContent = 'press run.'; readoutCorner.textContent = 'idle'
  page.querySelectorAll('[data-c]').forEach((el) => { el.textContent = '0' })
  page.querySelectorAll('.stage-list [data-timing]').forEach((el) => { const s = stageByN.get(Number(el.dataset.timing)); el.innerHTML = esc(timingOf(s, run)) + (s.events.length ? fn(['rec']) : '') })
  show(shown)
})
window.__how = { mill, RUNS, play: (i = 0) => mill.play(RUNS[i]) }
