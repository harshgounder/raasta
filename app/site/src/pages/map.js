import { boot, head, bi, t, esc, onLang, getLang, legendHtml, cityPicker, mockBanner } from './common.js'
import { createMapView } from '../demo/mapview.js'
import { receiptHtml, toReceipt, paintCrops } from '../demo/receipt.js'
import { fill, hhmm } from '../data/data.js'

boot('map')
const page = document.getElementById('page')
page.innerHTML = head({ compact: true, kicker: { en: 'live map', hi: 'लाइव नक्शा' }, title: { en: 'the route your body can take', hi: 'वह रास्ता जिस पर आपका शरीर चल सके' },
  lede: { en: 'Grey is the shortest route. Red is the one that avoids every known barrier for the profile you pick, at the hour you leave. Tap a dot to see its photo receipt.', hi: 'स्लेटी सबसे छोटा रास्ता है. लाल वह रास्ता है जो आपकी प्रोफ़ाइल और निकलने के समय के लिए हर पक्की रुकावट से बचता है. फ़ोटो रसीद के लिए बिंदु पर टैप करें.' } }) + `
  <div class="mock-slot"></div>
  <div class="controls">
    <span class="city-slot"></span>
    <label class="field scen" hidden>${bi({ en: 'trip', hi: 'सफ़र' })}<select class="scen-sel"></select></label>
    <div class="field">${bi({ en: 'profile', hi: 'प्रोफ़ाइल' })}<div class="seg profiles" role="radiogroup" aria-label="profile"></div></div>
    <label class="field time">${bi({ en: 'leave at', hi: 'निकलने का समय' })} <output>09:00</output><input type="range" min="0" max="23.5" step="0.5" value="9" aria-label="leave time"></label>
    <div class="field">${bi({ en: 'base map', hi: 'आधार नक्शा' })}<div class="seg base" role="radiogroup" aria-label="base map">
      <button type="button" role="radio" aria-checked="true" data-base="paper">${bi({ en: 'paper', hi: 'कागज़' })}</button><button type="button" role="radio" aria-checked="false" data-base="streets">${bi({ en: 'streets', hi: 'सड़कें' })}</button></div></div>
    <button type="button" class="btn box replay">${bi({ en: 'replay walk', hi: 'फिर से चलाओ' })}</button>
  </div>
  <div class="map-grid">
    <div class="map-wrap box"><div class="map" id="map"></div></div>
    <aside class="side">
      <section class="summary box" aria-live="polite"></section>
      <div class="receipt-slot"><p class="empty box">${bi({ en: 'Tap a barrier dot to open its receipt.', hi: 'रसीद देखने के लिए रुकावट वाले बिंदु पर टैप करें.' })}</p></div>
      ${legendHtml()}
    </aside>
  </div>`

const $ = (s) => page.querySelector(s)
const view = createMapView($('#map'), { onSelect: (b) => showReceipt(b) })
let city = null
function showReceipt(b) {
  const slot = $('.receipt-slot')
  if (!b) { slot.innerHTML = ''; return }
  slot.innerHTML = receiptHtml(toReceipt(b)); paintCrops(slot)
}
function summary() {
  const { shortest, accessible } = view.state.routes, prof = city?.routes.profiles?.find((p) => p.id === view.state.profile)
  const vars = (r) => ({ len: Math.round(r.length_m), extra: shortest ? Math.max(0, Math.round(r.length_m - shortest.length_m)) : '?', n: r.barriers_hit?.length ?? 0,
    unknown: r.unknown_m ?? '?', profile: t(prof?.label) || view.state.profile, time: hhmm(view.state.hour), minutes: Math.round(r.length_m / (prof?.speed_mps ?? 0.9) / 60) })
  const s = shortest ? `<p><i class="key" aria-hidden="true"></i>${esc(fill(t(shortest.summary), vars(shortest)))}</p>` : ''
  const a = accessible ? `<p><i class="key acc" aria-hidden="true"></i>${esc(fill(t(accessible.summary), vars(accessible)))}</p>${(accessible.assumptions ?? []).map((x) => `<small>${esc(x)}</small>`).join('')}`
    : `<p><i class="key acc" aria-hidden="true"></i>${getLang() === 'hi' ? 'इस प्रोफ़ाइल और समय के लिए कोई जाँचा हुआ रास्ता नहीं. हम अंदाज़ा नहीं लगाते.' : 'No checked route for this profile at this hour. We do not guess.'}</p>`
  const lt = city?.routes?.leave_times
  const note = lt?.length ? `<small>${getLang() === 'hi' ? 'गणना इन समयों के लिए' : 'computed for'} ${lt.map((x) => esc(x.slice(11, 16))).join(', ')}; ${getLang() === 'hi' ? 'सबसे पास वाला दिखाया' : 'the nearest is shown'}</small>` : ''
  $('.summary').innerHTML = s + a + note
}
function scenarios() {
  const sc = city?.scenarios ?? [], lab = $('.scen')
  lab.hidden = sc.length < 2
  $('.scen-sel').innerHTML = sc.map((x, i) => `<option value="${i}">${esc(x.name)}</option>`).join('')
}
$('.scen-sel').addEventListener('change', (e) => { view.setScenario(+e.target.value); summary(); showReceipt(null) })
function profiles() {
  const box = $('.profiles')
  box.innerHTML = (city?.routes.profiles ?? []).map((p) => `<button type="button" role="radio" aria-checked="${p.id === view.state.profile}" data-p="${esc(p.id)}">${esc(t(p.label))}</button>`).join('')
}
$('.profiles').addEventListener('click', (e) => {
  const b = e.target.closest('[data-p]'); if (!b) return
  view.setProfile(b.dataset.p); profiles(); summary()
})
const range = $('input[type="range"]'), out = $('output')
range.addEventListener('input', () => { out.textContent = hhmm(+range.value); view.setHour(+range.value); summary() })
$('.base').addEventListener('click', async (e) => {
  const b = e.target.closest('[data-base]'); if (!b) return
  const got = await view.setBasemap(b.dataset.base)
  $('.base').querySelectorAll('button').forEach((x) => x.setAttribute('aria-checked', String(x.dataset.base === got)))
})
$('.replay').addEventListener('click', () => view.replay())

const picker = await cityPicker(async (c) => { city = c; $('.mock-slot').innerHTML = mockBanner(c); await view.setCity(c); scenarios(); profiles(); summary(); showReceipt(null) })
$('.city-slot').append(picker.el)
city = picker.first
if (city) {
  $('.mock-slot').innerHTML = mockBanner(city)
  const go = async () => { await view.setCity(city); scenarios(); profiles(); summary() }
  view.map.loaded() ? go() : view.map.once('load', go)
  const qb = new URLSearchParams(location.search).get('barrier'); if (qb) view.map.once('idle', () => view.select(qb))
} else $('.summary').innerHTML = `<p>${getLang() === 'hi' ? 'अभी कोई शहर डेटा नहीं.' : 'No city data yet.'}</p>`
onLang(() => { profiles(); summary(); view.lang(); if (view.state.selected) showReceipt(view.state.selected) })
window.__view = view
