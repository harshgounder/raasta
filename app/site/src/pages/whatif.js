// /what-if v2: every question from research/hermes/sc02/WHATIF-TREE.md as a topic > subtopic > sub-subtopic tree,
// each one runnable on the map from a precomputed impact-engine run (app/route/tools/precompute_whatif.py ->
// /site-data/whatif/<id>.json). v1 (the 15-card wall) is in app/site/archive/whatif-v1/. notes: app/site/WHATIF-V2-BUILD.md
import { boot, head, bi, t, esc, onLang, getLang } from './common.js'
import { content } from '../data/data.js'
import { glyph, sevOf } from './whatif-glyphs.js'
import './whatif.css'

boot('what-if')
document.body.append(Object.assign(document.createElement('div'), { className: 'wi-headbar' }))
const page = document.getElementById('page')
const T = await content('whatif-tree')
const runs = new Map()
let index = {}
fetch('/site-data/whatif/index.json', { cache: 'no-cache' }).then((r) => (r.ok ? r.json() : {})).then((j) => { index = j?.items ?? j ?? {}; renderTree() }).catch(() => {})

const TOPIC_HI = { T1: 'मौसम', T2: 'रोशनी और समय', T3: 'सतह और टूट-फूट', T4: 'रुकावटें', T5: 'लोग और व्यापार', T6: 'शरीर', T7: 'डेटा और भरोसा',
  T8: 'शिकायत और ज़िम्मेदारी', T9: 'मेल: दो मुश्किलें एक साथ', T10: 'इंटरफ़ेस और भरोसा', T11: 'खर्च और समय', T12: 'किनारे के मामले' }
const CITY = { jaipur: 'Jaipur walled city', chandigarh: 'Chandigarh', varanasi: 'Varanasi old city', 'jaipur-photos': 'Jaipur photo area west' }
const VERDICT = { block: { en: 'blocks', hi: 'रोकता है' }, cost: { en: 'costs time', hi: 'समय लेता है' }, warn: { en: 'warns', hi: 'चेतावनी' }, none: { en: 'no effect', hi: 'असर नहीं' },
  changed: { en: 'route differs', hi: 'रास्ता बदलता है' }, same: { en: 'same route', hi: 'वही रास्ता' } }
const L = (en, hi) => ({ en, hi })
const BI = {
  search: L('search 300 questions', 'सवाल खोजें'), body: L('body', 'शरीर'), allBodies: L('every body', 'हर शरीर'),
  run: L('run on the map', 'नक्शे पर चलाओ'), hide: L('close the map', 'नक्शा बंद करो'), answer: L('what RAASTA does', 'RAASTA क्या करता है'),
  recipe: L('the run behind it', 'इसके पीछे का रन'), engine: L('on the map, from the engine', 'नक्शे पर, इंजन से'),
  without: L('without it', 'इसके बिना'), with: L('with it', 'इसके साथ'), contrast: L('same thing, different bodies', 'वही चीज़, अलग शरीर'),
  allTree: L('every body in the tree', 'पेड़ में हर शरीर'), placed: L('where it was placed', 'कहाँ रखा गया'), prev: L('previous', 'पिछला'), next: L('next', 'अगला'),
  questions: L('questions', 'सवाल'), noMatch: L('No question matches. Try a shorter word, or clear the body filter.', 'कोई सवाल नहीं मिला. छोटा शब्द आज़माएँ या शरीर फ़िल्टर हटाएँ.'),
  tree: L('questions by topic', 'विषय के हिसाब से सवाल'), passable: L('passable', 'जा सकते हैं'), blocked: L('blocked', 'रुका हुआ'),
  loading: L('loading the engine run', 'इंजन रन लोड हो रहा है'), legendBase: L('route without the what-if', 'बिना बदलाव का रास्ता'), legendWi: L('route with the what-if', 'बदलाव के साथ रास्ता'),
  hits: L('what the engine priced on the new route', 'नए रास्ते पर इंजन ने क्या गिना'),
}
const items = T.items ?? {}
const bodyInfo = T.bodies?.info ?? {}
const bodyName = (id) => bodyInfo[id]?.name ?? id ?? ''
const elName = (id) => T.elements?.[id]?.name ?? String(id ?? '').replaceAll('_', ' ')
const total = Object.keys(items).length
const fmtM = (m) => (m == null ? '' : `${m > 0 ? '+' : m < 0 ? '−' : '±'}${Math.abs(Math.round(m))} m`)
const fmtMin = (m) => (m == null ? '' : `${m > 0 ? '+' : m < 0 ? '−' : '±'}${Math.abs(Math.round(m * 10) / 10)} min`)
const letter = (v) => ({ block: 'B', cost: 'C', warn: 'W', none: 'N', changed: 'Δ', same: '=' }[v] ?? '')

const S = { q: '', body: '', topic: null, sub: null, sel: null, mapOpen: false, mapBody: null }

page.innerHTML = head({ compact: true, kicker: L('what if', 'अगर'), title: L(`${total} questions, every one runs on the map`, `${total} सवाल, हर एक नक्शे पर चलता है`),
  lede: L('Asked the way people on the street ask them. Pick a topic, then a subtopic, then a question. Each answer says what RAASTA does, which data it uses, what it asks you for, and what it shows meanwhile. Run on the map shows the route with and without the problem, for your body and for others.',
    'जैसे सड़क पर लोग पूछते हैं. पहले विषय, फिर उप-विषय, फिर सवाल चुनें. हर जवाब बताता है कि RAASTA क्या करता है, कौन सा डेटा लेता है, आपसे क्या माँगता है और तब तक क्या दिखाता है. नक्शे पर चलाओ: समस्या के साथ और बिना रास्ता, आपके शरीर और दूसरों के लिए.') }) + `
  <div class="wi2">
    <aside class="wi-tree" aria-label="${esc(t(BI.tree))}">
      <button type="button" class="wi-drawer btn primary" aria-expanded="false" aria-controls="wi-tree-body">${bi(BI.tree)} <span class="wi-drawer-n"></span></button>
      <div class="wi-tree-body" id="wi-tree-body">
        <label class="wi-search"><span class="sr-only">${esc(t(BI.search))}</span><input type="search" placeholder="${esc(t(BI.search))}" autocomplete="off" spellcheck="false"></label>
        <label class="wi-bodyf field">${bi(BI.body)}<select></select></label>
        <nav class="wi-topics"></nav>
      </div>
    </aside>
    <section class="wi-main" aria-live="polite"></section>
  </div>`
const $ = (s) => page.querySelector(s)
const tree = $('.wi-topics'), main = $('.wi-main')

// ---- body filter: only the leaves the questions actually use, with counts
function renderBodyFilter() {
  const n = {}
  for (const it of Object.values(items)) if (it.recipe?.body) n[it.recipe.body] = (n[it.recipe.body] ?? 0) + 1
  const opts = Object.entries(n).sort((a, b) => b[1] - a[1])
  $('.wi-bodyf select').innerHTML = `<option value="">${esc(t(BI.allBodies))} (${total})</option>` +
    opts.map(([id, k]) => `<option value="${esc(id)}"${S.body === id ? ' selected' : ''}>${esc(bodyName(id))} · ${esc(bodyInfo[id]?.hermes_id ?? '')} (${k})</option>`).join('')
}

const hay = (it) => `${it.id} ${it.topic} ${it.subtopic} ${it.subsub} ${it.q} ${it.q_hi ?? ''} ${it.a} ${(it.parts ?? []).join(' ')} ${it.recipe?.inject_raw ?? ''} ${it.recipe?.place_raw ?? ''} ${bodyName(it.recipe?.body)}`.toLowerCase()
const matches = (it) => it && (!S.body || it.recipe?.body === S.body) && (!S.q || S.q.split(/\s+/).every((w) => hay(it).includes(w)))

function badge(id) {
  const x = index[id]
  if (!x) return ''
  const v = x.verdict ?? (x.blocked_whatif ? 'block' : x.changed ? 'cost' : 'none')
  return `<i class="wi-b v-${esc(v)}" title="${esc(t(VERDICT[v] ?? VERDICT.none))}${x.delta_m != null ? `, ${fmtM(x.delta_m)}` : ''}">${letter(v)}</i>`
}

function renderTree() {
  const searching = !!S.q
  let shown = 0
  const html = (T.topics ?? []).map((tp) => {
    const subs = tp.subtopics.map((s) => ({ ...s, list: s.items.map((id) => items[id]).filter(matches) })).filter((s) => s.list.length)
    const n = subs.reduce((a, s) => a + s.list.length, 0)
    if (!n) return ''
    shown += n
    const open = searching || S.topic === tp.id
    return `<div class="wi-t${open ? ' open' : ''}">
      <button type="button" class="wi-trow" data-topic="${esc(tp.id)}" aria-expanded="${open}"><span class="wi-tid">${esc(tp.id)}</span>${bi(L(tp.name, TOPIC_HI[tp.id] ?? tp.name), 'span', 'wi-tname')}<span class="wi-n">${n}</span></button>
      ${open ? `<div class="wi-subs">${subs.map((s) => {
        const so = searching || S.sub === s.id
        return `<div class="wi-s${so ? ' open' : ''}">
          <button type="button" class="wi-srow" data-sub="${esc(s.id)}" aria-expanded="${so}"><span class="wi-tid">${esc(s.id)}</span><span class="wi-sname">${esc(s.name)}</span><span class="wi-n">${s.list.length}</span></button>
          ${so ? `<ul class="wi-items">${s.list.map((it) => `<li><button type="button" class="wi-irow" data-id="${esc(it.id)}" aria-current="${S.sel === it.id}">
            <span class="wi-iid">${esc(it.id)}</span><span class="wi-isub">${esc(it.subsub || it.q)}</span>${badge(it.id)}</button></li>`).join('')}</ul>` : ''}
        </div>`
      }).join('')}</div>` : ''}
    </div>`
  }).join('')
  tree.innerHTML = html || `<p class="wi-none">${bi(BI.noMatch)}</p>`
  page.querySelector('.wi-drawer-n').textContent = `${shown}/${total}`
  const cur = tree.querySelector('[aria-current="true"]')
  if (cur && !isNarrow()) cur.scrollIntoView({ block: 'nearest' })
}
const isNarrow = () => matchMedia('(max-width: 980px)').matches

// ---- the question
const humanHour = (r) => r?.hhmm ?? (r?.hour != null ? `${String(Math.floor(r.hour)).padStart(2, '0')}:${String(Math.round((r.hour % 1) * 60)).padStart(2, '0')}` : '')
function recipeHtml(it) {
  const r = it.recipe ?? {}
  const els = (r.elements ?? []).map((e) => `<span class="wi-el">${glyph(T.elements?.[e]?.glyph, 26, 'slow')}${esc(elName(e))}</span>`).join('')
  const rows = [
    [L('city', 'शहर'), esc(CITY[r.city] ?? r.city ?? '')],
    [L('what is put on the street', 'सड़क पर क्या रखा'), els || esc(r.inject_raw ?? '')],
    [L('where', 'कहाँ'), esc(r.place_raw || (getLang() === 'hi' ? 'आधार रास्ते पर' : 'on the baseline route'))],
    [L('for whom', 'किसके लिए'), `${esc(bodyName(r.body))} <small>${esc(r.body_hermes ?? '')}</small>`],
    [L('when', 'कब'), `${esc(humanHour(r))} · ${esc(r.weather_raw ?? r.weather ?? '')} · ${esc(r.light_raw ?? r.light ?? '')}`],
  ]
  return `<dl class="wi-recipe">${rows.map(([k, v]) => `<div><dt>${bi(k)}</dt><dd>${v}</dd></div>`).join('')}</dl>
    ${r.raw ? `<p class="wi-raw"><code>${esc(r.raw)}</code></p>` : ''}
    ${(it.recipe_notes ?? []).length ? `<ul class="wi-notes">${it.recipe_notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul>` : ''}`
}

function siblings(id) {
  const it = items[id]
  const tp = T.topics.find((x) => x.id === it.topic_id)
  const flat = (T.topics ?? []).flatMap((x) => x.subtopics.flatMap((s) => s.items)).filter((k) => matches(items[k]))
  const i = flat.indexOf(id)
  return { prev: flat[i - 1], next: flat[i + 1], tp }
}

function renderMain() {
  const it = items[S.sel]
  if (!it) { main.innerHTML = ''; return }
  const { prev, next } = siblings(it.id)
  main.innerHTML = `<article class="wi-q">
      <p class="wi-crumb"><span class="wi-qid">${esc(it.id)}</span> ${bi(L(it.topic, TOPIC_HI[it.topic_id] ?? it.topic))} <b>›</b> ${esc(it.subtopic)} <b>›</b> ${esc(it.subsub ?? '')}</p>
      ${getLang() === 'hi' && it.q_hi ? `<h2 class="wi-qh" lang="hi">${esc(it.q_hi)}</h2><p class="wi-qhi" lang="en">${esc(it.q)}</p>`
        : `<h2 class="wi-qh">${esc(it.q)}</h2>${it.q_hi ? `<p class="wi-qhi" lang="hi">${esc(it.q_hi)}</p>` : ''}`}
      <div class="wi-cols">
        <div class="wi-ans">
          ${bi(BI.answer, 'h3')}
          <p class="wi-a">${esc(it.a)}</p>
          ${it.run?.detail ? `${bi(L('what the engine found', 'इंजन ने क्या पाया'), 'h3', 'wi-found-h')}<p class="wi-a wi-found">${esc(it.run.detail)}</p>` : ''}
          <ul class="wi-parts" aria-label="product part">${(it.parts ?? []).map((p) => `<li>${esc(p)}</li>`).join('')}</ul>
        </div>
        <div class="wi-rec box">${bi(BI.recipe, 'h3')}${recipeHtml(it)}</div>
      </div>
      <div class="wi-actions">
        <button type="button" class="btn red wi-run" aria-expanded="${S.mapOpen}" aria-controls="wi-mappanel">${bi(S.mapOpen ? BI.hide : BI.run)}</button>
        <span class="wi-nav">${prev ? `<button type="button" class="btn" data-go="${esc(prev)}">← ${bi(BI.prev)} <small>${esc(prev)}</small></button>` : ''}${next ? `<button type="button" class="btn" data-go="${esc(next)}">${bi(BI.next)} <small>${esc(next)}</small> →</button>` : ''}</span>
      </div>
      <section class="wi-mappanel" id="wi-mappanel" ${S.mapOpen ? '' : 'hidden'}>
        <div class="wi-legend"><span><i class="k base"></i>${bi(BI.legendBase)}</span><span><i class="k wi"></i>${bi(BI.legendWi)}</span><span><i class="k dot"></i>${bi(L('where the what-if sits', 'बदलाव कहाँ है'))}</span></div>
        <div class="wi-mapbox box"><div class="wi-map"></div></div>
        <aside class="wi-side box"></aside>
      </section>
      <section class="wi-engine box"><h3>${bi(BI.engine)}</h3><div class="wi-eng-body"><p class="muted">${bi(BI.loading)}</p></div></section>
    </article>`
  loadRun(it.id).then((run) => { if (S.sel === it.id) { renderEngine(it, run); if (S.mapOpen) openMap(run) } })
}

async function loadRun(id) {
  if (!runs.has(id)) runs.set(id, fetch(`/site-data/whatif/${encodeURIComponent(id)}.json`, { cache: 'no-cache' }).then((r) => (r.ok ? r.json() : null)).catch(() => null))
  return runs.get(id)
}

const variantOf = (run, b) => run?.variants?.[b] ?? run?.variants?.[run?.body]
const offRoute = (v) => (v?.on_route === false ? `<p class="wi-off">${bi(L(`This body's usual route does not pass this spot, so nothing moves. If they met it: ${t(VERDICT[v.element_verdicts?.[0]?.verdict ?? v.verdict] ?? VERDICT.none)}.`, `इस शरीर का सामान्य रास्ता इस जगह से नहीं गुज़रता, इसलिए कुछ नहीं बदलता. अगर सामने आए: ${VERDICT[v.element_verdicts?.[0]?.verdict ?? v.verdict]?.hi ?? 'असर नहीं'}.`))}</p>` : '')
const hourOf = (iso) => (iso ? iso.slice(11, 16) : '')
const labels = (run) => run?.labels ?? (run?.compare === 'body' ? { base: run.compare_body ? `${bodyName(run.compare_body)}` : L('adult, no impairment', 'बिना अक्षमता वयस्क'), whatif: L('this body', 'यह शरीर') }
  : run?.compare === 'hour' ? { base: L(`at ${hourOf(run.base_leave_time)}`, `${hourOf(run.base_leave_time)} बजे`), whatif: L(`at ${hourOf(run.leave_time)}`, `${hourOf(run.leave_time)} बजे`) }
  : run?.compare === 'context' ? { base: L('usual conditions', 'सामान्य हालात'), whatif: L('these conditions', 'ये हालात') } : { base: BI.without, whatif: BI.with })
const lbl = (x) => (typeof x === 'string' ? x : t(x))

function statLine(r, name) {
  if (!r) return ''
  return `<div class="wi-stat"><span class="wi-stat-k">${esc(name)}</span><b>${r.length_m != null ? `${Math.round(r.length_m)} m` : ''}</b><b>${r.minutes != null ? `${r.minutes} min` : ''}</b>
    <span class="wi-flag ${r.blocked ? 'bad' : ''}">${bi(r.blocked ? BI.blocked : BI.passable)}</span></div>`
}
function deltaHtml(v) {
  if (!v) return ''
  return `<p class="wi-delta"><span class="${(v.delta_m ?? 0) > 0 ? 'up' : ''}">${fmtM(v.delta_m)}</span><span class="${(v.delta_min ?? 0) > 0 ? 'up' : ''}">${fmtMin(v.delta_min)}</span>
    ${v.verdict ? `<span class="wi-vd v-${esc(v.verdict)}">${bi(VERDICT[v.verdict] ?? VERDICT.none)}</span>` : ''}</p>`
}

function contrastHtml(run, active) {
  const ids = [...new Set([run.body, ...(run.contrast ?? [])])].filter((b) => run.variants?.[b])
  return `<div class="wi-contrast" role="group" aria-label="${esc(t(BI.contrast))}">${ids.map((b) => {
    const v = run.variants[b]
    return `<button type="button" class="wi-cb${b === active ? ' on' : ''}" data-body="${esc(b)}" aria-pressed="${b === active}">
      <span class="wi-cb-v v-${esc(v.verdict ?? 'none')}">${letter(v.verdict) || '·'}</span><span class="wi-cb-n">${esc(bodyName(b))}${b === run.body ? ' ★' : ''}</span>${v.on_route === false ? `<span class="wi-cb-off">${bi(L('usual route does not pass this spot', 'सामान्य रास्ता यहाँ से नहीं गुज़रता'))}</span>` : `<span class="wi-cb-d">${fmtM(v.delta_m)}</span>`}</button>`
  }).join('')}</div>`
}

function renderEngine(it, run) {
  const box = main.querySelector('.wi-eng-body')
  if (!box) return
  if (!run) {
    box.innerHTML = `<p>${bi(L('This question runs from its recipe above. Its precomputed run is added by the next data build (app/route/tools/precompute_whatif.py); the map then draws it here.', 'यह सवाल ऊपर की रेसिपी से चलता है. इसका पहले से गणना किया रन अगले डेटा बिल्ड में जुड़ता है, फिर नक्शा इसे यहीं दिखाता है.'))}</p>`
    return
  }
  const v = variantOf(run, run.body)
  const lb = labels(run)
  box.innerHTML = `${run.headline && !it.run?.detail ? `<p class="wi-head">${esc(run.headline)}</p>` : ''}
    ${deltaHtml(v)}
    <div class="wi-stats">${statLine(v?.base, lbl(lb.base))}${statLine(v?.whatif, lbl(lb.whatif))}</div>
    ${offRoute(v)}${(v?.reason_short ?? v?.reason) ? `<p class="wi-reason">${esc(v.reason_short ?? v.reason)}</p>` : ''}
    ${run.trip_note ? `<p class="muted small">${esc(run.trip_note)}</p>` : ''}
    <h4>${bi(BI.contrast)}</h4>${contrastHtml(run, run.body)}`
}

// ---- the map panel
let mapApi = null, mapLoading = null
async function openMap(run) {
  const panel = main.querySelector('.wi-mappanel')
  if (!panel || !run) return
  panel.hidden = false
  const el = panel.querySelector('.wi-map')
  mapLoading ??= import('./whatif-map.js')
  const { createWhatifMap } = await mapLoading
  // the panel is re-rendered per question: keep one map and move its container in
  if (!mapApi) mapApi = createWhatifMap(Object.assign(document.createElement('div'), { className: 'wi-map-inner' }))
  const inner = mapApi.map.getContainer()
  if (inner.parentElement !== el) el.append(inner)
  mapApi.resize()
  const lb = labels(run), asL = (x) => (typeof x === 'string' ? L(x, x) : x)
  panel.querySelector('.wi-legend').innerHTML = `<span><i class="k base"></i>${bi(asL(lb.base))}</span><span><i class="k wi"></i>${bi(asL(lb.whatif))}</span>${(run.injected ?? []).length ? `<span><i class="k dot"></i>${bi(L('where the what-if sits', 'बदलाव कहाँ है'))}</span>` : ''}`
  S.mapBody = run.variants?.[S.mapBody] ? S.mapBody : run.body
  await mapApi.show(run, S.mapBody)
  window.__whatif = { map: mapApi.map, run, ready: true }
  renderSide(run)
}

function bodySelectHtml(run) {
  const tr = T.bodies?.tree ?? {}
  let h = ''
  for (const [cat, groups] of Object.entries(tr)) {
    for (const [grp, node] of Object.entries(groups)) {
      const leaves = (node?._leaves ?? []).filter((b) => run.variants?.[b])
      if (!leaves.length) continue
      h += `<optgroup label="${esc(cat)} › ${esc(grp)}">${leaves.map((b) => {
        const v = run.variants[b]
        return `<option value="${esc(b)}"${b === S.mapBody ? ' selected' : ''}>${esc(bodyName(b))} · ${letter(v.verdict) || '·'} ${v.on_route === false ? (getLang() === 'hi' ? 'रास्ते पर नहीं' : 'not on usual route') : fmtM(v.delta_m)}</option>`
      }).join('')}</optgroup>`
    }
  }
  return h
}

function renderSide(run) {
  const side = main.querySelector('.wi-side')
  if (!side) return
  const b = S.mapBody, v = variantOf(run, b), lb = labels(run)
  const hits = (v?.whatif?.hits ?? []).slice(0, 5)
  side.innerHTML = `<p class="wi-side-k">${bi(BI.body)}</p><h3 class="wi-side-b">${esc(bodyName(b))} <small>${esc(bodyInfo[b]?.hermes_id ?? '')}</small></h3>
    ${deltaHtml(v)}
    <div class="wi-stats">${statLine(v?.base, lbl(lb.base))}${statLine(v?.whatif, lbl(lb.whatif))}</div>
    ${offRoute(v)}${(v?.reason_short ?? v?.reason) ? `<p class="wi-reason">${esc(v.reason_short ?? v.reason)}</p>` : ''}
    ${hits.length ? `<h4>${bi(BI.hits)}</h4><ul class="wi-hits">${hits.map((h) => `<li>${glyph(T.elements?.[h.element]?.glyph, 24, sevOf(h.verdict))}<span><b>${esc(elName(h.element))}</b> ${esc(h.why ?? '')}</span></li>`).join('')}</ul>` : ''}
    ${(run.injected ?? []).length ? `<h4>${bi(BI.placed)}</h4><ul class="wi-placed">${dedupePlaced(run.injected).map((x) => `<li>${glyph(x.glyph, 24, 'slow')}<span><b>${esc(x.name ?? elName(x.element))}</b>${x.road ? ` · ${esc(x.road)}` : ''}${x.placement_note ? `<br><small>${esc(x.placement_note)}</small>` : ''}</span></li>`).join('')}</ul>` : ''}
    <h4>${bi(BI.contrast)}</h4>${contrastHtml(run, b)}
    <label class="field wi-allb">${bi(BI.allTree)}<select>${bodySelectHtml(run)}</select></label>`
}
const dedupePlaced = (list) => { const seen = new Set(); return list.filter((x) => { const k = `${x.element}|${x.road ?? ''}`; if (seen.has(k)) return false; seen.add(k); return true }) }

async function setMapBody(b) {
  const run = await loadRun(S.sel)
  if (!run?.variants?.[b]) return
  S.mapBody = b
  if (mapApi) await mapApi.show(run, b, { fit: true })
  renderSide(run)
}

// ---- selection, hash, events
function select(id, { run = false, scroll = true } = {}) {
  const it = items[id]
  if (!it) return
  S.sel = id; S.topic = it.topic_id; S.sub = it.subtopic_id
  if (run) S.mapOpen = true
  S.mapBody = null
  history.replaceState(null, '', `#${id}${S.mapOpen ? '/run' : ''}`)
  renderTree(); renderMain()
  if (scroll && isNarrow()) { closeDrawer(); main.scrollIntoView({ block: 'start' }) }
}
function closeDrawer() { const b = $('.wi-drawer'); b.setAttribute('aria-expanded', 'false'); $('.wi-tree').classList.remove('open') }

tree.addEventListener('click', (e) => {
  const tb = e.target.closest('[data-topic]'), sb = e.target.closest('[data-sub]'), ib = e.target.closest('[data-id]')
  if (ib) return select(ib.dataset.id)
  if (sb) { S.sub = S.sub === sb.dataset.sub ? null : sb.dataset.sub; return renderTree() }
  if (tb) { S.topic = S.topic === tb.dataset.topic ? null : tb.dataset.topic; S.sub = null; return renderTree() }
})
let qt = 0
$('.wi-search input').addEventListener('input', (e) => { clearTimeout(qt); qt = setTimeout(() => { S.q = e.target.value.trim().toLowerCase(); renderTree() }, 120) })
$('.wi-bodyf select').addEventListener('change', (e) => { S.body = e.target.value; renderTree() })
$('.wi-drawer').addEventListener('click', (e) => { const o = $('.wi-tree').classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', String(o)) })
main.addEventListener('click', async (e) => {
  const go = e.target.closest('[data-go]'), cb = e.target.closest('[data-body]'), runBtn = e.target.closest('.wi-run')
  if (go) return select(go.dataset.go)
  if (cb) {
    if (!S.mapOpen) { S.mapOpen = true; S.mapBody = cb.dataset.body; history.replaceState(null, '', `#${S.sel}/run`); const run = await loadRun(S.sel); toggleRunBtn(); await openMap(run); return main.querySelector('.wi-mappanel')?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }) }
    return setMapBody(cb.dataset.body)
  }
  if (runBtn) {
    S.mapOpen = !S.mapOpen
    history.replaceState(null, '', `#${S.sel}${S.mapOpen ? '/run' : ''}`)
    toggleRunBtn()
    if (S.mapOpen) { const run = await loadRun(S.sel); await openMap(run); main.querySelector('.wi-mappanel')?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }) }
    else main.querySelector('.wi-mappanel').hidden = true
  }
})
main.addEventListener('change', (e) => { if (e.target.closest('.wi-allb')) setMapBody(e.target.value) })
function toggleRunBtn() {
  const b = main.querySelector('.wi-run'); if (!b) return
  b.setAttribute('aria-expanded', String(S.mapOpen)); b.innerHTML = bi(S.mapOpen ? BI.hide : BI.run)
}

function fromHash() {
  const [id, mode] = decodeURIComponent(location.hash.slice(1)).split('/')
  if (items[id]) { select(id, { run: mode === 'run', scroll: false }); return true }
  return false
}
addEventListener('hashchange', fromHash)
renderBodyFilter()
if (!fromHash()) {
  const first = T.topics?.[0]?.subtopics?.[0]?.items?.[0]
  S.topic = T.topics?.[0]?.id ?? null
  if (first) { S.sel = first; S.sub = items[first]?.subtopic_id; renderTree(); renderMain() } else renderTree()
}
onLang(() => { $('.wi-search input').placeholder = t(BI.search); renderBodyFilter(); renderTree(); renderMain() })
