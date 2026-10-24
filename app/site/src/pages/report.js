// /report v2: a person reports a barrier in a short branching flow, sees it recorded at once, gets an AI first look
// in seconds, their own routes avoid it straight away, and they can follow the human check and the public map update.
// backend: app/reports (FastAPI, port 8790). URL: ?reports= > window.HYP_CONFIG.REPORTS_URL > http://<host>:8790 on a
// local or LAN host. If it is down, the report is kept on this phone (localStorage outbox) and sent later.
// v1 (pick a known barrier, write a letter) is archived in app/site/archive/report-v1/ and lives on, fixed, in the
// "letter" section at the bottom. Build notes: app/reports/REPORT-BUILD.md
import { boot, head, esc, getLang, onLang, cityPicker, mockBanner } from './common.js'
import { content, fill, TYPE_LABEL } from '../data/data.js'
import './report.css'

boot('report')
const page = document.getElementById('page')
const $ = (s, r = page) => r.querySelector(s)
const $$ = (s, r = page) => [...r.querySelectorAll(s)]
// both languages side by side: the person reads whichever they read best
const two = (o, cls = '') => `<span class="two ${cls}"><span class="en">${esc(o.en)}</span><span class="hi" lang="hi">${esc(o.hi ?? '')}</span></span>`
const store = {
  get(k, d = null) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v) } catch { return d } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true } catch { return false } },
}

// ------------------------------------------------------------------ backend
function reportsUrl() {
  const q = new URLSearchParams(location.search).get('reports')
  if (q) return q.replace(/\/$/, '')
  const c = window.HYP_CONFIG?.REPORTS_URL
  if (c) return c.replace(/\/$/, '')
  const h = location.hostname
  if (h === 'localhost' || /^(127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(h) || h.endsWith('.local')) return `${location.protocol}//${h}:8790`
  return ''
}
const API = reportsUrl()
const timeout = (ms) => { const c = new AbortController(); setTimeout(() => c.abort(), ms); return c.signal }
async function api(path, opts = {}, ms = 12000) {
  if (!API) throw new Error('no reports service set')
  const r = await fetch(API + path, { ...opts, signal: timeout(ms) })
  if (!r.ok) throw Object.assign(new Error(`HTTP ${r.status}`), { status: r.status, body: await r.text().catch(() => '') })
  return r.json()
}
let device = store.get('hyp.device')
if (!device) { device = 'd-' + (crypto.randomUUID?.() ?? Math.random().toString(36).slice(2) + Date.now().toString(36)); store.set('hyp.device', device) }

// ------------------------------------------------------------------ icons (drawn, one stroke weight)
const I = {
  kerb: '<path d="M3 20h8v-7h10"/><path d="M11 13v7"/>',
  crack: '<path d="M3 18h18"/><path d="M7 18l3-5 2 3 3-6 2 8"/>',
  gap: '<path d="M3 17h6M15 17h6"/><path d="M9 17l1 3h4l1-3"/>',
  block: '<rect x="8" y="5" width="8" height="12"/><path d="M3 20h18"/>',
  zebra: '<path d="M4 6v12M8 6v12M12 6v12M16 6v12M20 6v12"/>',
  lamp: '<path d="M8 21h8M12 21V8"/><path d="M12 8c0-3 6-3 6 0"/><path d="M18 8l-1 3h-2"/>',
  dots: '<circle cx="6" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="18" cy="12" r="1.5"/>',
  wheels: '<circle cx="10" cy="15" r="5"/><path d="M10 4v6h6l2 5"/>',
  walking_aid: '<path d="M8 4v16M8 9h8M16 9v11"/>',
  sight_hearing: '<path d="M2 12s4-6 10-6 10 6 10 6-4 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/>',
  age_body: '<circle cx="12" cy="5" r="2"/><path d="M12 7v7l-3 6M12 14l3 6M9 10h6"/>',
  mind: '<path d="M12 4a6 6 0 0 0-4 10.5V18h8v-3.5A6 6 0 0 0 12 4z"/><path d="M10 21h4"/>',
  none: '<circle cx="12" cy="5" r="2"/><path d="M12 7v8l-3 6M12 15l3 6M8 11h8"/>',
  pin: '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
  cam: '<rect x="3" y="7" width="18" height="13"/><circle cx="12" cy="13.5" r="3.5"/><path d="M8 7l2-3h4l2 3"/>',
}
const icon = (k) => `<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">${I[k] ?? I.dots}</svg>`

// ------------------------------------------------------------------ page skeleton
page.classList.add('rp')
page.innerHTML = head({ compact: true, kicker: { en: 'report a barrier', hi: 'रुकावट बताइए' },
  title: { en: 'what stopped you?', hi: 'आपको किसने रोका?' },
  lede: { en: 'Tell us in a few taps. It is recorded at once, an AI takes a first look in seconds, your own routes avoid it straight away, and a person checks it.', hi: 'कुछ टैप में बताइए. शिकायत तुरंत दर्ज होती है, AI कुछ सेकंड में देखता है, आपके अपने रास्ते तुरंत इससे बचते हैं, और फिर एक व्यक्ति जाँचता है.' } }) + `
  <p class="svc" role="status" aria-live="polite"></p>
  <div class="rp-cols">
    <form class="flow" novalidate>
      <section class="q" data-q="what"><h2>${two({ en: '1. what stopped you?', hi: '1. किसने रोका?' })}</h2><div class="cats grid"></div><div class="types chips" hidden></div><div class="details"></div>
        <label class="field other-words" hidden>${two({ en: 'say it in your words', hi: 'अपने शब्दों में बताइए' })}<textarea class="words-other" rows="3"></textarea></label></section>
      <section class="q" data-q="who"><h2>${two({ en: '2. who were you, or what aid do you use?', hi: '2. आप कौन थे, या कौन सा सहारा लेते हैं?' })}</h2><div class="bgroups grid"></div><div class="leaves chips" hidden></div>
        <button type="button" class="link skip-body">${two({ en: 'skip this question', hi: 'यह सवाल छोड़ें' })}</button></section>
      <section class="q" data-q="where"><h2>${two({ en: '3. where is it?', hi: '3. यह कहाँ है?' })}</h2>
        <div class="row"><button type="button" class="btn primary gps">${icon('pin')} ${two({ en: 'use my location', hi: 'मेरी लोकेशन लें' })}</button><span class="gps-out muted"></span></div>
        <div class="map" role="application" aria-label="map: tap to move the pin"></div>
        <p class="muted small">${two({ en: 'Tap the map or drag the pin to the exact spot.', hi: 'नक्शे पर टैप करें या पिन खींचकर सही जगह रखें.' })}</p>
        <h3>${two({ en: 'which side of the road?', hi: 'सड़क की किस तरफ़?' })}</h3><div class="chips side"></div></section>
      <section class="q" data-q="when"><h2>${two({ en: '4. when?', hi: '4. कब?' })}</h2>
        <div class="chips when"><button type="button" data-v="now" aria-pressed="true">${two({ en: 'just now', hi: 'अभी' })}</button><button type="button" data-v="earlier" aria-pressed="false">${two({ en: 'earlier', hi: 'पहले' })}</button></div>
        <input type="datetime-local" class="when-at" hidden aria-label="when it happened">
        <h3>${two({ en: 'how long has it been there?', hi: 'यह कब से है?' })}</h3><div class="chips since"></div></section>
      <section class="q" data-q="hurt"><h2>${two({ en: '5. did it hurt you or force you somewhere?', hi: '5. क्या इससे चोट लगी या कहीं और जाना पड़ा?' })}</h2><div class="chips hurt"></div></section>
      <section class="q" data-q="photo"><h2>${two({ en: '6. a photo, if you can', hi: '6. फ़ोटो, अगर ले सकें' })}</h2>
        <label class="btn primary photo-btn">${icon('cam')} ${two({ en: 'take or pick a photo', hi: 'फ़ोटो लें या चुनें' })}<input type="file" accept="image/*" capture="environment" class="photo-in" hidden></label>
        <div class="photo-prev"></div>
        <label class="field">${two({ en: 'anything else? (optional)', hi: 'कुछ और? (वैकल्पिक)' })}<textarea class="words" rows="3"></textarea></label></section>
      <section class="q" data-q="contact"><h2>${two({ en: '7. how can we reach you? (optional)', hi: '7. आपसे संपर्क कैसे करें? (वैकल्पिक)' })}</h2>
        <label class="field">${two({ en: 'phone or email, only to tell you what happened', hi: 'फ़ोन या ईमेल, सिर्फ़ नतीजा बताने के लिए' })}<input type="text" class="contact" autocomplete="tel"></label>
        <p class="muted small">${two({ en: 'We never show it to anyone else. You can leave it empty: this phone keeps your reports.', hi: 'यह किसी और को नहीं दिखाया जाता. खाली छोड़ सकते हैं: यह फ़ोन आपकी शिकायतें याद रखता है.' })}</p></section>
      <div class="send-row"><button type="submit" class="btn red send">${two({ en: 'send report', hi: 'शिकायत भेजें' })}</button><span class="need muted"></span></div>
    </form>
    <aside class="side-col">
      <section class="trail-wrap" hidden aria-live="polite"></section>
      <section class="mine"><h2>${two({ en: 'my reports', hi: 'मेरी शिकायतें' })}</h2><div class="mine-list"><p class="muted">${two({ en: 'none yet', hi: 'अभी कोई नहीं' })}</p></div></section>
    </aside>
  </div>
  <p class="honest-page">${two({ en: 'Every contact on this site was checked against an official website on 25 October 2026; where we could not confirm a phone number, we did not print one.', hi: 'इस साइट का हर संपर्क 25 अक्टूबर 2026 को सरकारी वेबसाइट से जाँचा गया; जहाँ फ़ोन नंबर पक्का नहीं हो पाया, वहाँ हमने नंबर नहीं छापा.' })}</p>
  <details class="letter"><summary>${two({ en: 'already on our map? write a complaint letter for it', hi: 'पहले से नक्शे पर है? उसके लिए शिकायत पत्र लिखें' })}</summary><div class="letter-body"></div></details>`

// ------------------------------------------------------------------ the form
const S = { details: {}, category: null, type: null, bodyGroup: null, body: null, lat: null, lon: null, acc: null, locSrc: null, side: null, when: 'now', since: null, hurt: null, photo: null }
const form = await content('report-form')
const cats = form.categories, bgroups = form.bodies

function chips(el, list, key, multi = false) {
  el.innerHTML = list.map((o) => `<button type="button" data-v="${esc(o.id)}" aria-pressed="${S[key] === o.id}">${o.icon ? icon(o.icon) : ''}${two(o)}</button>`).join('')
  el.onclick = (e) => {
    const b = e.target.closest('button[data-v]'); if (!b) return
    S[key] = S[key] === b.dataset.v && !multi ? null : b.dataset.v
    $$('button', el).forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.v === S[key])))
    el.dispatchEvent(new CustomEvent('pick', { detail: S[key] })); check()
  }
}
chips($('.cats'), cats, 'category')
function renderDetails() {
  const c = cats.find((x) => x.id === S.category)
  const qs = (c?.details ?? []).filter((q) => !q.for || (S.type && q.for.includes(S.type)))
  for (const k of Object.keys(S.details)) if (!qs.some((q) => q.id === k)) delete S.details[k]
  $('.details').innerHTML = qs.length && S.type ? qs.map((q) => `<div class="dq" data-q="${esc(q.id)}"><h3>${two(q)}</h3><div class="chips">${q.options.map((o) => `<button type="button" data-v="${esc(o.id)}" aria-pressed="${S.details[q.id] === o.id}">${two(o)}</button>`).join('')}</div></div>`).join('') : ''
}
$('.details').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-v]'); if (!b) return
  const q = b.closest('.dq').dataset.q
  S.details[q] = S.details[q] === b.dataset.v ? undefined : b.dataset.v
  if (!S.details[q]) delete S.details[q]
  b.parentElement.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.v === S.details[q])))
})
$('.types').addEventListener('pick', renderDetails)
$('.cats').addEventListener('pick', () => {
  const c = cats.find((x) => x.id === S.category)
  S.type = c?.types.length === 1 ? c.types[0].id : null
  $('.types').hidden = !c || c.types.length === 1
  if (c) chips($('.types'), c.types, 'type')
  $('.other-words').hidden = S.category !== 'other'
  renderDetails(); check()
})
chips($('.bgroups'), bgroups.map((g) => ({ ...g, icon: g.id })), 'bodyGroup')
$('.bgroups').addEventListener('pick', () => {
  const g = bgroups.find((x) => x.id === S.bodyGroup)
  S.body = g?.leaves.length === 1 ? g.leaves[0].id : null
  $('.leaves').hidden = !g || g.leaves.length === 1
  if (g) chips($('.leaves'), g.leaves, 'body')
})
$('.skip-body').onclick = () => { S.bodyGroup = S.body = null; $$('.bgroups button, .leaves button').forEach((b) => b.setAttribute('aria-pressed', 'false')); $('.leaves').hidden = true; $('[data-q="where"]').scrollIntoView({ behavior: 'smooth', block: 'start' }) }
chips($('.side'), form.side, 'side')
chips($('.since'), form.since, 'since')
chips($('.hurt'), form.hurt, 'hurt')
$('.when').onclick = (e) => {
  const b = e.target.closest('button[data-v]'); if (!b) return
  S.when = b.dataset.v; $$('.when button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)))
  $('.when-at').hidden = S.when !== 'earlier'
  if (S.when === 'earlier' && !$('.when-at').value) { const d = new Date(Date.now() - 3600e3); d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); $('.when-at').value = d.toISOString().slice(0, 16) }
}

// photo: shrink on the phone before upload (mobile data), keep a preview
$('.photo-in').addEventListener('change', async (e) => {
  const f = e.target.files?.[0]; if (!f) return
  S.photo = await shrink(f).catch(() => f)
  $('.photo-prev').innerHTML = `<figure><img alt="your photo" src="${URL.createObjectURL(S.photo)}"><figcaption class="muted small">${esc(f.name)} · ${(S.photo.size / 1024).toFixed(0)} KB <button type="button" class="link rm-photo">${two({ en: 'remove', hi: 'हटाएँ' })}</button></figcaption></figure>`
  $('.rm-photo').onclick = () => { S.photo = null; $('.photo-prev').innerHTML = ''; $('.photo-in').value = '' }
})
async function shrink(file, max = 1600) {
  if (file.size < 1.2e6) return file
  const bmp = await createImageBitmap(file, { imageOrientation: 'from-image' })
  const k = Math.min(1, max / Math.max(bmp.width, bmp.height))
  const c = Object.assign(document.createElement('canvas'), { width: Math.round(bmp.width * k), height: Math.round(bmp.height * k) })
  c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height)
  const blob = await new Promise((r) => c.toBlob(r, 'image/jpeg', 0.85))
  return new File([blob], file.name.replace(/\.\w+$/, '') + '.jpg', { type: 'image/jpeg' })
}

// map + GPS. maplibre loads only when the map scrolls near (the page stays light on a phone)
let map = null, marker = null
const DEFAULT = [75.8066, 26.9258] // Jaipur photo area (Tirpoliya Bazar); the pin waits for GPS or a tap
function setPin(lon, lat, src, acc = null) {
  S.lon = +lon.toFixed(6); S.lat = +lat.toFixed(6); S.locSrc = src; S.acc = acc
  $('.gps-out').innerHTML = `${S.lat}, ${S.lon}${acc != null ? ` · ±${Math.round(acc)} m` : ''} · ${esc(src === 'gps' ? 'GPS' : getLang() === 'hi' ? 'नक्शे से' : 'map pin')}`
  if (map) { marker.setLngLat([S.lon, S.lat]); map.easeTo({ center: [S.lon, S.lat], zoom: Math.max(map.getZoom(), 17) }) }
  check()
}
async function loadMap() {
  if (map) return
  const [mod, { default: workerUrl }] = await Promise.all([import('maplibre-gl'), import('maplibre-gl/dist/maplibre-gl-worker.mjs?url'), import('maplibre-gl/dist/maplibre-gl.css')])
  const maplibregl = mod.Map ? mod : mod.default
  maplibregl.setWorkerUrl?.(workerUrl)
  const center = S.lon != null ? [S.lon, S.lat] : DEFAULT
  map = new maplibregl.Map({ container: $('.map'), style: 'https://tiles.openfreemap.org/styles/positron', center, zoom: 16, attributionControl: { compact: true }, dragRotate: false, pitchWithRotate: false })
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right')
  const el = Object.assign(document.createElement('div'), { className: 'pin', innerHTML: icon('pin') })
  marker = new maplibregl.Marker({ element: el, anchor: 'bottom', draggable: true }).setLngLat(center).addTo(map)
  marker.on('dragend', () => { const p = marker.getLngLat(); setPin(p.lng, p.lat, 'map') })
  map.on('click', (e) => setPin(e.lngLat.lng, e.lngLat.lat, 'map'))
}
new IntersectionObserver((es, o) => { if (es.some((x) => x.isIntersecting)) { o.disconnect(); loadMap().catch((err) => { console.warn("report map:", err?.message ?? err); $('.map').innerHTML = `<p class="muted pad">${two({ en: 'The map could not load. Use the location button.', hi: 'नक्शा नहीं खुला. लोकेशन बटन दबाएँ.' })}</p>` }) } }, { rootMargin: '300px' }).observe($('.map'))
$('.gps').onclick = () => {
  if (!navigator.geolocation) { $('.gps-out').textContent = getLang() === 'hi' ? 'इस ब्राउज़र में GPS नहीं' : 'no GPS in this browser'; return }
  $('.gps-out').textContent = getLang() === 'hi' ? 'ढूँढ रहे हैं...' : 'finding you...'
  navigator.geolocation.getCurrentPosition((p) => {
    if (p.coords.accuracy > 60) {
      if (map) map.easeTo({ center: [p.coords.longitude, p.coords.latitude], zoom: 17 })
      $('.gps-out').innerHTML = two({ en: `GPS is only good to ±${Math.round(p.coords.accuracy)} m here, too rough to place it. Tap the exact spot on the map.`, hi: `यहाँ GPS सिर्फ़ ±${Math.round(p.coords.accuracy)} मीटर तक सही है, जगह तय करने के लिए काफ़ी नहीं. नक्शे पर सही जगह टैप करें.` })
      return
    }
    setPin(p.coords.longitude, p.coords.latitude, 'gps', p.coords.accuracy)
  },
    (err) => { $('.gps-out').textContent = (getLang() === 'hi' ? 'लोकेशन नहीं मिली: नक्शे पर टैप करें' : 'no location: tap the map instead') + ` (${err.code === 1 ? 'permission' : 'timeout'})` },
    { enableHighAccuracy: true, timeout: 12000, maximumAge: 30000 })
}

function check() {
  const missing = []
  if (!S.type) missing.push(getLang() === 'hi' ? 'क्या रोका' : 'what stopped you')
  if (S.lat == null) missing.push(getLang() === 'hi' ? 'जगह' : 'where')
  if (S.category === 'other' && !$('.words-other').value.trim()) missing.push(getLang() === 'hi' ? 'अपने शब्द' : 'your words')
  $('.need').textContent = missing.length ? (getLang() === 'hi' ? 'बाकी: ' : 'still needed: ') + missing.join(', ') : ''
  $('.send').disabled = missing.length > 0
  return !missing.length
}
$('.words-other').addEventListener('input', check)
check()

// ------------------------------------------------------------------ send (or keep on the phone)
function formData(r) {
  const fd = new FormData()
  for (const [k, v] of Object.entries(r)) if (v != null && v !== '' && k !== 'photo' && k !== 'photo_data') fd.append(k, v)
  if (r.photo) fd.append('photo', r.photo, r.photo.name || 'photo.jpg')
  return fd
}
const toDataUrl = (f) => new Promise((ok, no) => { const fr = new FileReader(); fr.onload = () => ok(fr.result); fr.onerror = no; fr.readAsDataURL(f) })
const fromDataUrl = async (u, name) => new File([await (await fetch(u)).blob()], name, { type: 'image/jpeg' })

$('.flow').addEventListener('submit', async (e) => {
  e.preventDefault(); if (!check()) return
  const observed = S.when === 'earlier' && $('.when-at').value ? new Date($('.when-at').value).toISOString() : new Date().toISOString()
  const words = [S.category === 'other' ? $('.words-other').value.trim() : '', $('.words').value.trim()].filter(Boolean).join(' / ')
  const r = { device_id: device, client_id: 'c-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), category: S.category, type: S.type, body: S.body,
    lat: S.lat, lon: S.lon, accuracy_m: S.acc, location_source: S.locSrc, side: S.side, observed_at: observed, since: S.since, hurt: S.hurt,
    words, contact: $('.contact').value.trim(), lang: getLang(), photo: S.photo, details: JSON.stringify(S.details) }
  $('.send').disabled = true; $('.send').classList.add('busy')
  try {
    const rep = await api('/reports', { method: 'POST', body: formData(r) }, 25000)
    remember(rep.id); showTrail(rep); resetForm()
  } catch (err) {
    if (err.status >= 400 && err.status < 500) { // the service answered and refused: saving it would only retry forever
      const w = $('.trail-wrap'); w.hidden = false
      w.innerHTML = `<div class="key-status off">${two({ en: 'The service did not accept this report.', hi: 'सेवा ने यह शिकायत स्वीकार नहीं की.' })}</div><p class="small">${esc(err.body?.slice(0, 200) ?? err.message)}</p>`
      return
    }
    const saved = { ...r, photo: null, photo_data: S.photo ? await toDataUrl(S.photo).catch(() => null) : null, photo_name: S.photo?.name, saved_at: new Date().toISOString(), why: String(err.message) }
    const box = store.get('hyp.reports.outbox', [])
    let ok = store.set('hyp.reports.outbox', [...box, saved])
    if (!ok) { saved.photo_data = null; saved.photo_dropped = !!S.photo; ok = store.set('hyp.reports.outbox', [...box, saved]) } // storage full: keep the words, drop the photo
    showOffline(saved, ok)
    if (ok) resetForm() // a second tap must not queue the same report twice
  } finally { $('.send').classList.remove('busy'); check() }
})
function resetForm() {
  Object.assign(S, { details: {}, category: null, type: null, bodyGroup: S.bodyGroup, body: S.body, side: null, since: null, hurt: null, photo: null })
  $$('.cats button, .types button, .side button, .since button, .hurt button').forEach((b) => b.setAttribute('aria-pressed', 'false'))
  $('.types').hidden = true; $('.details').innerHTML = ''; $('.other-words').hidden = true; $('.photo-prev').innerHTML = ''; $('.photo-in').value = ''; $('.words').value = ''; $('.words-other').value = ''
  check()
}
// one flush at a time; items leave the outbox by client_id only after the server has them, so a report saved while a
// flush runs is never overwritten. A 4xx answer will never succeed: the item moves to hyp.reports.refused (kept).
let flushing = false
async function flushOutbox() {
  if (flushing || !API || !store.get('hyp.reports.outbox', []).length) return
  flushing = true
  try {
    for (const r of store.get('hyp.reports.outbox', [])) {
      let done = false, refused = null
      try {
        const photo = r.photo_data ? await fromDataUrl(r.photo_data, r.photo_name || 'photo.jpg') : null
        const rep = await api('/reports', { method: 'POST', body: formData({ ...r, photo, saved_at: undefined, why: undefined, photo_name: undefined, photo_dropped: undefined }) }, 25000)
        remember(rep.id); done = true
      } catch (e) { if (e.status >= 400 && e.status < 500 && e.status !== 429) refused = `HTTP ${e.status}` }
      if (done || refused) {
        store.set('hyp.reports.outbox', store.get('hyp.reports.outbox', []).filter((x) => x.client_id !== r.client_id))
        if (refused) store.set('hyp.reports.refused', [...store.get('hyp.reports.refused', []), { ...r, refused }])
      }
    }
  } finally { flushing = false; renderMine() }
}
function showOffline(saved, ok) {
  const w = $('.trail-wrap'); w.hidden = false
  w.innerHTML = `<div class="key-status off">${two(ok ? { en: 'Saved on this phone. Not sent yet.', hi: 'इस फ़ोन में सहेजी गई. अभी भेजी नहीं गई.' } : { en: 'Could not send, and this phone could not save it.', hi: 'भेज नहीं पाए, और फ़ोन में भी सहेज नहीं पाए.' })}</div>
    ${saved.photo_dropped ? `<p class="small">${two({ en: 'This phone had no room for the photo, so only the words and the place were kept.', hi: 'फ़ोन में फ़ोटो के लिए जगह नहीं थी, इसलिए सिर्फ़ शब्द और जगह रखी गई.' })}</p>` : ''}
    <p>${two({ en: `The report service is not answering (${saved.why}). We try again when you come back online and every 30 seconds while this page is open.`, hi: 'शिकायत सेवा अभी जवाब नहीं दे रही. इंटरनेट लौटने पर और पेज खुला रहने तक हर 30 सेकंड में फिर कोशिश करेंगे.' })}</p>`
  renderMine(); w.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
addEventListener('online', flushOutbox)
setInterval(flushOutbox, 30000)

// ------------------------------------------------------------------ status trail
const STEP = {
  received: { en: 'received and recorded', hi: 'मिल गई और दर्ज हो गई' },
  ai_first_look: { en: 'AI first look', hi: 'AI की पहली नज़र' },
  personal_route: { en: 'added to your routes now', hi: 'अभी आपके रास्तों में जुड़ गई' },
  human_verification: { en: 'a person checks it', hi: 'एक व्यक्ति जाँचता है' },
  answer: { en: 'answer to you', hi: 'आपको जवाब' },
  public_update: { en: 'added for everyone in the next map update', hi: 'अगले नक्शा अपडेट में सबके लिए' },
}
const fmt = (iso) => iso ? new Date(iso).toLocaleString(getLang() === 'hi' ? 'hi-IN' : 'en-IN', { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', second: '2-digit' }) : ''
const fmtDay = (iso) => iso ? new Date(iso).toLocaleString(getLang() === 'hi' ? 'hi-IN' : 'en-IN', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' }) : ''
let poll = null, current = null, ticking = false, lastSig = ''


function showTrail(rep) {
  current = rep.id
  const w = $('.trail-wrap'); w.hidden = false
  w.innerHTML = trailHtml(rep)
  w.querySelector('.again')?.addEventListener('click', () => { $('.flow').scrollIntoView({ behavior: 'smooth' }) })
  clearTimeout(poll)
  const live = rep.steps.some((s) => s.state === 'active' && ['ai_first_look', 'personal_route'].includes(s.id))
  const open = rep.steps.some((s) => ['active', 'waiting'].includes(s.state))
  const young = Date.now() - new Date(rep.created_at) < 180e3 // a step still running after 3 min is stuck: slow down
  if (open) poll = setTimeout(() => refresh(rep.id), live && young ? 1000 : 20000)
  if (live && !ticking) { ticking = true; tick() }
  const sig = rep.id + rep.steps.map((s) => s.state).join()
  if (sig !== lastSig) { lastSig = sig; renderMine() } // the list only changes when a step does
}
async function refresh(id) {
  if (id !== current) return
  clearTimeout(poll)
  try {
    const rep = await api(`/reports/${encodeURIComponent(id)}`)
    if (id === current) showTrail(rep) // the person may have opened another report meanwhile
  } catch { if (id === current) { clearTimeout(poll); poll = setTimeout(() => refresh(id), 5000) } }
}
function tick() { // live seconds on the running steps
  const t0 = $('.trail')?.dataset.t0; if (!t0) { ticking = false; return }
  $$('.trail .live-s').forEach((x) => { x.textContent = ((Date.now() - new Date(t0)) / 1000).toFixed(0) + ' s' })
  if ($('.trail .live-s')) setTimeout(tick, 250)
  else ticking = false
}

function trailHtml(rep) {
  const st = Object.fromEntries(rep.steps.map((s) => [s.id, s]))
  const ai = rep.ai ?? {}, pr = rep.personal ?? {}
  const key = rep.status === 'verified' ? { en: 'Checked by a person. It is going on the public map.', hi: 'एक व्यक्ति ने जाँच ली. यह सबके नक्शे पर जा रही है.' }
    : rep.status === 'rejected' ? { en: 'A person checked it and could not confirm it.', hi: 'जाँच में पक्का नहीं हो पाया.' }
    : pr.ok ? { en: 'Recorded. Your routes already avoid it.', hi: 'दर्ज हो गई. आपके रास्ते अब इससे बचते हैं.' }
    : { en: 'Recorded. We have it.', hi: 'दर्ज हो गई. हमें मिल गई.' }
  const li = (id, body) => {
    const s = st[id] ?? { state: 'waiting' }
    const when = s.at ? `<time datetime="${esc(s.at)}">${esc(fmt(s.at))}</time>` : s.state === 'active' ? `<span class="live-s">0 s</span>` : s.eta ? `<span class="eta">${two({ en: 'expected by ' + fmtDay(s.eta), hi: 'अनुमानित: ' + fmtDay(s.eta) })}</span>` : ''
    return `<li class="st-${esc(s.state)}"><span class="dot" aria-hidden="true"></span><div><p class="st-head">${two(STEP[id])}<span class="st-state">${esc(stateWord(s.state))}</span></p><p class="st-when">${when}</p>${body ?? ''}</div></li>`
  }
  const aiBody = st.ai_first_look?.state === 'active' ? `<p class="muted">${two({ en: 'reading your report and photo now', hi: 'आपकी शिकायत और फ़ोटो अभी पढ़ रहे हैं' })}</p>` : aiHtml(rep)
  const prBody = st.personal_route?.state === 'active' ? '' : prHtml(pr)
  const hv = st.human_verification ?? {}
  const hvBody = hv.state === 'done' ? `<p>${two({ en: `decision: ${rep.review?.decision}`, hi: `फ़ैसला: ${rep.review?.decision === 'verified' ? 'सही पाई गई' : rep.review?.decision === 'duplicate' ? 'पहले से दर्ज' : 'पक्का नहीं'}` })}</p>`
    : `<p class="muted small">${two({ en: `within ${rep.promises?.verify_hours ?? 24} hours. Honest note: this is a demo, so the reviewer is a RAASTA team member, not a city official.`, hi: `${rep.promises?.verify_hours ?? 24} घंटे में. सच्ची बात: यह डेमो है, जाँचने वाला RAASTA टीम का सदस्य है, नगर निगम का अधिकारी नहीं.` })}</p>`
  const ans = rep.review?.answer
  const esc30 = `<p class="muted small">${two({ en: 'We never promise a repair date: the city owns that clock. No answer from the office in 30 days? You can escalate with the same evidence.', hi: 'हम मरम्मत की तारीख़ का वादा नहीं करते: वह शहर के हाथ में है. 30 दिन में दफ़्तर से जवाब नहीं? उसी सबूत के साथ आगे भेज सकते हैं.' })}</p>`
  const ansBody = ans ? `<blockquote>${two(ans)}</blockquote>${esc30}` : `<p class="muted small">${two({ en: `within ${rep.promises?.answer_hours ?? 48} hours${rep.has_contact ? ', here and on the contact you gave' : ', here on this page (no contact given)'}`, hi: `${rep.promises?.answer_hours ?? 48} घंटे में${rep.has_contact ? ', यहाँ और आपके दिए संपर्क पर' : ', इसी पेज पर'}` })}</p>`
  const pu = st.public_update ?? {}
  const puBody = `<p class="muted small">${two(pu.state === 'skipped' ? { en: 'not added: the check did not confirm it', hi: 'नहीं जोड़ी गई: जाँच में पक्की नहीं हुई' } : { en: `Public routes change only after a person checks it. Updates go out weekly (Sunday 06:00, demo cadence).${rep.public?.update_at ? ' Yours: ' + fmtDay(rep.public.update_at) + '.' : ''}`, hi: `सबके रास्ते तभी बदलते हैं जब कोई व्यक्ति जाँच ले. अपडेट हर हफ़्ते (रविवार सुबह 6 बजे, डेमो).${rep.public?.update_at ? ' आपकी: ' + fmtDay(rep.public.update_at) + '.' : ''}` })}</p>`
  return `<div class="key-status">${two(key)}</div>
    <p class="rid">${two({ en: 'report', hi: 'शिकायत' })} <b>${esc(rep.id)}</b>${rep.photo_url ? ` · <a href="${esc(API + rep.photo_url)}" target="_blank" rel="noopener">${two({ en: 'photo', hi: 'फ़ोटो' })}</a>` : ''}</p>
    <ol class="trail" data-t0="${esc(rep.created_at)}">
      ${li('received', `<p class="muted small">${esc(rep.fields?.type_label ?? rep.type)}${rep.lat != null ? ` · ${rep.lat}, ${rep.lon}` : ''}${rep.city ? ` · ${esc(rep.city)}` : ''}</p>`)}
      ${li('ai_first_look', aiBody)}
      ${li('personal_route', prBody)}
      ${li('human_verification', hvBody)}
      ${li('answer', ansBody)}
      ${li('public_update', puBody)}
    </ol>
    <button type="button" class="btn box again">${two({ en: 'report another', hi: 'एक और बताइए' })}</button>`
}
const stateWord = (s) => ({ done: getLang() === 'hi' ? 'हो गया' : 'done', active: getLang() === 'hi' ? 'चल रहा है' : 'running', waiting: getLang() === 'hi' ? 'बाकी' : 'waiting', failed: getLang() === 'hi' ? 'नहीं हो पाया' : 'did not work', skipped: getLang() === 'hi' ? 'लागू नहीं' : 'not needed' }[s] ?? s)

function aiHtml(rep) {
  const ai = rep.ai ?? {}; if (!ai.type) return ''
  const myBody = rep.body
  const aff = ai.affects
  const blocksMe = aff && myBody && aff.blocks.includes(myBody)
  const models = (ai.models_used ?? []).length ? ai.models_used.join(' + ') : null
  const engine = ai.engine_ok
    ? `<p class="model">${two({ en: `by ${models} in ${ai.timings?.total_s ?? '?'} s`, hi: `${models} द्वारा, ${ai.timings?.total_s ?? '?'} सेकंड में` })}</p>`
    : `<p class="model warn">${two({ en: `The AI (opencode-go/mimo-v2.6-flash for the photo, opencode-go/deepseek-v4.1-flash for the text) did not answer: ${ai.ai_error ?? ai.vision_error ?? 'error'}. These lines come from fixed rules instead.`, hi: 'AI ने जवाब नहीं दिया. नीचे की बातें तय नियमों से भरी गई हैं.' })}</p>`
  return `${engine}
    <dl class="facts">
      <dt>${two({ en: 'what', hi: 'क्या' })}</dt><dd>${two(ai.type_label ?? {})}${ai.changed_type ? ` <span class="small muted">${two({ en: '(changed from your choice)', hi: '(आपके चुनाव से बदला)' })}</span>` : ''}<br><span class="small muted">${esc(ai.element_name ?? '')}${ai.element_path ? ' · ' + esc(ai.element_path.join(' / ')) : ''}</span></dd>
      <dt>${two({ en: 'how bad', hi: 'कितना गंभीर' })}</dt><dd><span class="sev s${ai.severity}">${'■'.repeat(ai.severity)}${'□'.repeat(5 - ai.severity)}</span> ${esc(ai.severity_label ?? '')}</dd>
      ${aff ? `<dt>${two({ en: 'who it stops', hi: 'किसे रोकता है' })}</dt><dd>${two({ en: `blocks ${aff.blocks.length} of the ${aff.of} kinds of people and aids we model, slows ${aff.costs.length}, warns ${aff.warns.length}${myBody ? (blocksMe ? '. That includes you.' : '. Your aid is not in the blocked list for this kind of barrier, by our model.') : ''}`, hi: `हमारे ${aff.of} तरह के लोगों और सहारों में से ${aff.blocks.length} को रोकता है${blocksMe ? '. इनमें आप भी हैं.' : ''}` })}<br><span class="small muted">${esc(aff.blocks.slice(0, 6).map((b) => aff.names?.[b] ?? b).join(', '))}${aff.blocks.length > 6 ? ', ...' : ''}</span></dd>` : ''}
      <dt>${two({ en: 'seen before?', hi: 'पहले देखा?' })}</dt><dd>${ai.duplicate_of ? two({ en: `yes, report ${ai.duplicate_of} is the same problem. Yours adds weight to it.`, hi: `हाँ, शिकायत ${ai.duplicate_of} यही है. आपकी शिकायत उसे वज़न देती है.` }) : ai.already_on_map ? two({ en: `already on our map as ${ai.already_on_map}; your report confirms it is still there`, hi: `हमारे नक्शे पर पहले से है (${ai.already_on_map}); आपकी शिकायत बताती है कि यह अब भी है` }) : two({ en: `new: no report within 30 m (${ai.nearby_reports ?? 0} nearby of any kind)`, hi: 'नई: 30 मीटर में ऐसी कोई शिकायत नहीं' })}</dd>
      <dt>${two({ en: 'goes to', hi: 'किसे जाएगी' })}</dt><dd>${authHtml(ai.authority, rep.contacts)}</dd>
      <dt>${two({ en: 'how sure', hi: 'कितना यकीन' })}</dt><dd>${Math.round((ai.confidence ?? 0) * 100)}%${ai.why ? ` <span class="small muted">· ${esc(ai.why)}</span>` : ''}</dd>
      ${ai.photo_says ? `<dt>${two({ en: 'the photo', hi: 'फ़ोटो में' })}</dt><dd class="small">${esc(ai.photo_says)}</dd>` : ''}
      ${detHtml(rep.analyze)}
    </dl>
    ${ai.reply?.en || ai.reply?.hi ? `<blockquote class="reply">${two(ai.reply)}</blockquote>` : ''}`
}
function authHtml(a, c) {
  if (!a) return ''
  const link = a.url ? ` <a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(new URL(a.url).host)}</a>` : ''
  const phones = a.phones?.length ? `<br><span class="small">${a.phones.map((n) => `<a href="tel:${esc(n.replace(/[^0-9+]/g, ''))}">${esc(n)}</a>`).join(', ')}</span> <span class="small muted">${two(a.phones_caveat ?? { en: '', hi: '' })}</span>` : ''
  const unchecked = !a.checked ? `<br><span class="small muted">${two({ en: 'no contact checked for this city yet, so none is printed', hi: 'इस शहर का संपर्क अभी जाँचा नहीं गया, इसलिए नहीं छापा' })}</span>` : ''
  const esc2 = c?.escalation ? `<br><span class="small">${two(c.escalation)}</span>` : ''
  const honest = c?.honest_line ? `<p class="small muted honest">${two(c.honest_line)}</p>` : ''
  return `${two({ en: a.name ?? '', hi: a.name_hi ?? '' })}${link}${phones}${unchecked}${esc2}${honest}`
}
function detHtml(an) {
  if (!an || an.skipped) return ''
  if (!an.ok) return `<dt>${two({ en: 'detector', hi: 'डिटेक्टर' })}</dt><dd class="small muted">${esc(an.pending ?? an.error ?? 'not run')}</dd>`
  const acc = (an.detections ?? []).filter((d) => d.status === 'ACCEPT')
  const fam = [...new Set(acc.map((d) => d.class_family))]
  return `<dt>${two({ en: 'detector', hi: 'डिटेक्टर' })}</dt><dd class="small">${two({ en: acc.length ? `two detectors agree on: ${fam.join(', ').replace(/_/g, ' ')}` : 'two detectors found nothing they both agree on', hi: acc.length ? `दो डिटेक्टर सहमत: ${fam.join(', ').replace(/_/g, ' ')}` : 'दोनों डिटेक्टर किसी बात पर सहमत नहीं' })} <span class="muted">(${Number(an.counts?.ACCEPT) || 0} agreed, ${Number(an.counts?.ABSTAIN) || 0} unsure, ${Number(an.seconds) || '?'} s)</span></dd>`
}
function prHtml(pr) {
  if (!pr || pr.ok == null) return ''
  if (!pr.ok) return `<p class="muted small">${two({ en: pr.why ?? 'could not attach it to your routes', hi: 'आपके रास्तों में नहीं जोड़ पाए' })}</p>`
  const b = pr.route_before, a = pr.route_after
  const change = b?.length_m != null && a?.length_m != null ? (a.length_m !== b.length_m || a.uses_segment !== b.uses_segment
    ? { en: `A test route through this spot was ${Math.round(b.length_m)} m; for your routes it is now ${Math.round(a.length_m)} m and goes around it${a.shortest_blocked ? ' (the short way counts as blocked for you)' : ''}.`, hi: `इस जगह से होकर एक जाँच रास्ता ${Math.round(b.length_m)} मीटर था; अब आपके लिए ${Math.round(a.length_m)} मीटर है और इससे बचकर जाता है.` }
    : { en: `For ${pr.profile?.replace(/_/g, ' ')} it slows you rather than stops you, so your route now counts it: a test trip through this spot went from ${b.minutes?.toFixed(1)} to ${a.minutes?.toFixed(1)} min${a.report_on_route?.[0]?.why ? ` (${a.report_on_route[0].why})` : ''}. There is no shorter way around here, so the route stays and warns you.`, hi: `${pr.profile?.replace(/_/g, ' ')} के लिए यह रोकती नहीं, धीमा करती है. आपका रास्ता अब इसे गिनता है: इस जगह से होकर जाँच यात्रा ${b.minutes?.toFixed(1)} से ${a.minutes?.toFixed(1)} मिनट हो गई. यहाँ कोई छोटा दूसरा रास्ता नहीं, तो रास्ता वही है और आपको चेतावनी देता है.` }) : null
  return `<p class="small">${two({ en: `marked "reported, unverified" on your own copy of the ${pr.city} map in ${pr.seconds_since_received} s`, hi: `आपके अपने ${pr.city} नक्शे पर "बताई गई, अभी जाँची नहीं" के रूप में ${pr.seconds_since_received} सेकंड में` })}</p>
    ${change ? `<p class="small">${two(change)}</p>` : ''}<p class="small muted">${esc(pr.how ?? '')}</p>`
}

// ------------------------------------------------------------------ my reports
function remember(id) { const m = store.get('hyp.reports.mine', []); if (!m.includes(id)) store.set('hyp.reports.mine', [id, ...m].slice(0, 100)) }
async function renderMine() {
  const box = store.get('hyp.reports.outbox', [])
  let list = []
  try { if (API) list = (await api(`/reports?mine=${encodeURIComponent(device)}`)).reports } catch { list = null }
  const known = store.get('hyp.reports.mine', [])
  const row = (r) => {
    const last = [...(r.steps ?? [])].reverse().find((s) => s.state === 'done')
    return `<li><button type="button" class="link open" data-id="${esc(r.id)}"><b>${esc(r.type_label ?? r.type)}</b> <span class="muted small">${esc(r.id)} · ${esc(fmt(r.created_at))}</span><br><span class="small">${last ? two(STEP[last.id]) : ''}</span></button></li>`
  }
  $('.mine-list').innerHTML = (box.length ? `<p class="small">${two({ en: `${box.length} waiting on this phone to be sent`, hi: `${box.length} इस फ़ोन में भेजे जाने का इंतज़ार कर रही हैं` })}</p>` : '') +
    (list == null ? `<p class="muted small">${two({ en: `service offline; ${known.length} report ids kept on this phone`, hi: 'सेवा बंद है' })}</p>` : list.length ? `<ul class="mine-ul">${list.map(row).join('')}</ul>` : `<p class="muted">${two({ en: 'none yet', hi: 'अभी कोई नहीं' })}</p>`)
  $$('.mine-list .open').forEach((b) => b.addEventListener('click', async () => { try { showTrail(await api(`/reports/${encodeURIComponent(b.dataset.id)}`)); $('.trail-wrap').scrollIntoView({ behavior: 'smooth', block: 'start' }) } catch {} }))
}

// ------------------------------------------------------------------ service banner
async function health() {
  const el = $('.svc')
  if (!API) { el.className = 'svc off'; el.innerHTML = two({ en: 'The report service is not set up for this site yet. You can still fill the form: the report stays on this phone and is sent when it is.', hi: 'इस साइट के लिए शिकायत सेवा अभी चालू नहीं. फ़ॉर्म भरें: शिकायत इस फ़ोन में रहेगी और सेवा चालू होते ही भेजी जाएगी.' }); return }
  try {
    const h = await api('/health', {}, 5000)
    el.className = 'svc on'
    el.innerHTML = two({ en: `service online · AI first look: ${h.ai.vision_model} (photo) + ${h.ai.text_model} (text)${h.ai.last_error ? ' · last AI call failed, rules stand in' : ''}`, hi: `सेवा चालू · AI: ${h.ai.vision_model} (फ़ोटो) + ${h.ai.text_model} (लिखा हुआ)` })
    flushOutbox()
  } catch {
    el.className = 'svc off'
    el.innerHTML = two({ en: 'The report service is not answering right now. Your report will be saved on this phone and sent later.', hi: 'शिकायत सेवा अभी जवाब नहीं दे रही. आपकी शिकायत इस फ़ोन में सहेजी जाएगी और बाद में भेजी जाएगी.' })
  }
}
health(); renderMine()
const last = new URLSearchParams(location.search).get('id')
if (last && API) api(`/reports/${encodeURIComponent(last)}`).then(showTrail).catch(() => {})
onLang(() => { if (current) refresh(current); renderMine(); check() })

// ------------------------------------------------------------------ v1 letter, fixed (see REPORT-BUILD.md, root cause)
let letterReady = false
$('.letter').addEventListener('toggle', async (e) => { if (e.target.open && !letterReady) { letterReady = true; await letter($('.letter-body')) } })
async function letter(root) {
  root.innerHTML = `<div class="mock-slot"></div><div class="report-grid"><div class="stack"><span class="city-slot"></span>
      <label class="field">${two({ en: 'barrier', hi: 'रुकावट' })}<select class="pick"></select></label>
      <label class="field">${two({ en: 'your name (optional)', hi: 'आपका नाम (वैकल्पिक)' })}<input type="text" class="name" autocomplete="name"></label>
      <div class="field">${two({ en: 'language of the letter', hi: 'पत्र की भाषा' })}<div class="seg langs" role="radiogroup" aria-label="letter language"><button type="button" role="radio" data-l="hi" aria-checked="true">हिंदी</button><button type="button" role="radio" data-l="en" aria-checked="false">English</button></div></div></div>
    <div><label class="field">${two({ en: 'draft', hi: 'मसौदा' })}<textarea class="draft" spellcheck="false"></textarea></label>
      <div class="row-btns"><button type="button" class="btn primary copy">${two({ en: 'copy', hi: 'कॉपी' })}</button><a class="btn box wa" target="_blank" rel="noopener">${two({ en: 'share on WhatsApp', hi: 'WhatsApp पर भेजें' })}</a></div>
      <p class="muted small">${two({ en: 'Draft only. Confirm the ward office address on /city before sending; the legal basis is the RPwD Act, 2016.', hi: 'सिर्फ़ मसौदा. भेजने से पहले /city पर वार्ड कार्यालय का पता देख लें; कानूनी आधार RPwD अधिनियम, 2016 है.' })}</p></div></div>`
  const q = (s) => root.querySelector(s)
  const tpl = await content('report')
  const formLabel = Object.fromEntries(cats.flatMap((c) => c.types.filter((t) => t.route_type).map((t) => [t.route_type, { en: t.en, hi: t.hi }])))
  // root cause fix 3: types the template does not know (pothole, vendor, missing_footpath, open_drain) had raw ids
  const label = (b, L) => tpl.types[b.type]?.[L] ?? TYPE_LABEL[b.type]?.[L] ?? formLabel[b.raw_type ?? b.type]?.[L] ?? String(b.type).replace(/_/g, ' ')
  // root cause fix 2: most placements carry segment_id null (ABSTAIN: placed only as candidates); use the best candidate
  const segOf = (b) => b.segment_id ?? b.raw?.candidates?.[0]?.segment_id ?? null
  const roadOf = (b, city) => { const e = city.edgeById.get(segOf(b)); const c = b.raw?.candidates?.find((x) => x.road); return (e?.road_name && !['sidewalk', 'crossing', 'corner'].includes(e.road_name) ? e.road_name : null) ?? c?.road ?? null }
  let city = null, L = 'hi'
  const list = () => (city?.barriers ?? []).filter((b) => b.status !== 'REJECT')
  function options() {
    const bs = list()
    // root cause fix 1: cities with no barrier records (jaipur, varanasi) left an empty select and an empty letter
    q('.pick').innerHTML = bs.length ? bs.map((b) => `<option value="${esc(b.id)}">${esc(label(b, getLang()))} · ${esc(roadOf(b, city) ?? `${b.position[1].toFixed(4)}, ${b.position[0].toFixed(4)}`)} · ${esc(b.status)} · ${esc(b.id)}</option>`).join('')
      : `<option value="">${esc(getLang() === 'hi' ? 'इस इलाके में अभी कोई दर्ज रुकावट नहीं. ऊपर नई शिकायत करें.' : 'no barrier recorded in this area yet. Report one above.')}</option>`
    q('.pick').disabled = !bs.length
  }
  function draft() {
    const b = list().find((x) => x.id === q('.pick').value); if (!b) { q('.draft').value = ''; q('.wa').removeAttribute('href'); return }
    const road = roadOf(b, city) ?? (L === 'hi' ? `${b.position[1].toFixed(5)}, ${b.position[0].toFixed(5)} के पास की सड़क` : `the road near ${b.position[1].toFixed(5)}, ${b.position[0].toFixed(5)}`)
    const height = b.height_cm != null ? fill(tpl.height_line[L], { height: `${b.height_cm} ± ${b.height_err_cm} cm` }) : ''
    const photo = b.photo?.url ? new URL(b.photo.url, location.origin).href : (b.source_url ?? '')
    const text = fill(tpl.template[L], { type: label(b, L), road, segment: segOf(b) ?? (L === 'hi' ? 'अज्ञात' : 'not placed yet'), lat: b.position[1].toFixed(6), lng: b.position[0].toFixed(6),
      date: b.observed ?? '?', height, photo, status: b.status, name: q('.name').value.trim() || (L === 'hi' ? '(आपका नाम)' : '(your name)'), today: new Date().toISOString().slice(0, 10) })
    q('.draft').value = text; q('.wa').href = `https://wa.me/?text=${encodeURIComponent(text)}`
  }
  q('.pick').addEventListener('change', draft); q('.name').addEventListener('input', draft)
  q('.langs').addEventListener('click', (e) => { const b = e.target.closest('[data-l]'); if (!b) return; L = b.dataset.l; q('.langs').querySelectorAll('button').forEach((x) => x.setAttribute('aria-checked', String(x === b))); draft() })
  q('.copy').addEventListener('click', async () => { try { await navigator.clipboard.writeText(q('.draft').value) } catch { q('.draft').select() } })
  const picker = await cityPicker((c) => { city = c; q('.mock-slot').innerHTML = mockBanner(c); options(); draft() })
  q('.city-slot').append(picker.el); city = picker.first
  if (city) { q('.mock-slot').innerHTML = mockBanner(city); options(); draft() }
  onLang(() => { options(); draft() })
}
