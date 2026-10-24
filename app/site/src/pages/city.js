import { boot, head, bi, t, esc, onLang, getLang, cityPicker, mockBanner } from './common.js'
import { TYPE_LABEL } from '../data/data.js'

boot('city')
const page = document.getElementById('page')
page.innerHTML = head({ kicker: { en: 'city evidence', hi: 'शहर के सबूत' }, title: { en: 'what we know, and what we do not', hi: 'हम क्या जानते हैं, और क्या नहीं' },
  lede: { en: 'Every metre of footpath is a known barrier, known clear on a date, or unknown. Unknown is most of it, and we say so.', hi: 'फुटपाथ का हर मीटर या तो पक्की रुकावट है, किसी तारीख पर साफ़, या अज्ञात. ज़्यादातर अज्ञात है, और हम यह खुलकर कहते हैं.' } }) +
  `<div class="mock-slot"></div><div class="controls city-slot"></div><div class="dash"></div>`
const $ = (s) => page.querySelector(s)
const today = new Date()
const days = (a, b) => Math.round((b - new Date(a)) / 86400000)

function render(city) {
  $('.mock-slot').innerHTML = mockBanner(city)
  const hi = getLang() === 'hi'
  const len = { barrier: 0, clear: 0, unknown: 0 }, src = { osm: 0, generated: 0 }
  for (const e of city.edges) { len[e.evidence in len ? e.evidence : 'unknown'] += e.length_m ?? 0; src[e.source === 'osm' ? 'osm' : 'generated'] += e.length_m ?? 0 }
  const total = len.barrier + len.clear + len.unknown || 1
  const pct = (x) => Math.round((100 * x) / total)
  const byType = {}
  for (const b of city.barriers) { byType[b.type] ??= { ACCEPT: 0, ABSTAIN: 0, REJECT: 0 }; byType[b.type][b.status] = (byType[b.type][b.status] ?? 0) + 1 }
  const tr = city.trips
  let lo = null, hiV = null
  if (tr?.factors?.length) { lo = tr.factors.reduce((a, f) => a * f.low, 1); hiV = tr.factors.reduce((a, f) => a * f.high, 1) }
  else if (tr?.range) [lo, hiV] = tr.range
  const fixed = city.ledger.filter((x) => x.fixed).length
  $('.dash').innerHTML = `
    <div class="stats">
      <div class="stat box"><div class="n">${pct(len.unknown)}%</div><p>${hi ? 'फुटपाथ अज्ञात (कोई फ़ोटो नहीं)' : 'of the footpath is unknown (no photo)'}</p></div>
      <div class="stat box"><div class="n red">${pct(len.barrier)}%</div><p>${hi ? 'पर पक्की रुकावट' : 'has a known barrier'}</p></div>
      <div class="stat box"><div class="n">${pct(len.clear)}%</div><p>${hi ? 'किसी तारीख पर साफ़ देखा' : 'seen clear on a dated photo'}</p></div>
      <div class="stat box"><div class="n red">${city.ledger.length - fixed}</div><p>${hi ? `शिकायतें खुली, ${fixed} ठीक हुईं` : `complaints open, ${fixed} fixed`}</p></div>
    </div>
    <h2 class="section-title">${hi ? 'कवरेज' : 'coverage'}</h2>
    <div class="bar" role="img" aria-label="coverage: ${pct(len.barrier)}% barrier, ${pct(len.clear)}% clear, ${pct(len.unknown)}% unknown">
      <span class="b-barrier" style="width:${pct(len.barrier)}%"></span><span class="b-clear" style="width:${pct(len.clear)}%"></span><span class="b-unknown" style="width:${100 - pct(len.barrier) - pct(len.clear)}%"></span></div>
    <p class="muted">${Math.round(total)} m ${hi ? 'फुटपाथ' : 'of footpath'}: ${Math.round(src.osm)} m OSM, ${Math.round(src.generated)} m ${hi ? 'सड़क से बनाया गया (OSM में फुटपाथ नहीं)' : 'generated from roads (OSM has no footway there)'}.</p>
    <h2 class="section-title">${hi ? 'रुकावटें' : 'barriers'}</h2>
    <div class="table-wrap box"><table><thead><tr><th>${hi ? 'प्रकार' : 'type'}</th><th>ACCEPT</th><th>ABSTAIN</th><th>REJECT</th></tr></thead><tbody>
      ${Object.entries(byType).map(([k, v]) => `<tr><td>${esc(t(TYPE_LABEL[k]) || k)}</td><td>${v.ACCEPT ?? 0}</td><td>${v.ABSTAIN ?? 0}</td><td>${v.REJECT ?? 0}</td></tr>`).join('')}
    </tbody></table></div>
    <h2 class="section-title">${hi ? 'घाव का हिसाब' : 'scar ledger'}</h2>
    <p class="muted">${hi ? 'हर शिकायत, और कितने दिन से खुली है.' : 'Every complaint, and how many days it has been open.'}</p>
    <div class="table-wrap box"><table><thead><tr><th>${hi ? 'रुकावट' : 'barrier'}</th><th>${hi ? 'खंड' : 'segment'}</th><th>${hi ? 'शिकायत' : 'complaint'}</th><th>${hi ? 'किसे' : 'sent to'}</th><th>${hi ? 'ठीक हुआ' : 'fixed'}</th><th>${hi ? 'दिन' : 'days'}</th></tr></thead><tbody>
      ${city.ledger.map((x) => `<tr><td><a href="/map/?barrier=${esc(x.barrier_id)}">${esc(x.barrier_id)}</a></td><td>${esc(x.segment_id)}</td><td>${esc(x.complaint)}</td><td>${esc(x.to)}</td><td>${esc(x.fixed ?? (hi ? 'नहीं' : 'not yet'))}</td><td class="${x.fixed ? '' : 'open'}">${x.fixed ? days(x.complaint, new Date(x.fixed)) : days(x.complaint, today)}</td></tr>`).join('')}
    </tbody></table></div>
    <h2 class="section-title">${hi ? 'जो सफ़र नहीं हुए' : 'trips not taken'}</h2>
    ${lo != null ? `<div class="stat box"><div class="n red">${Math.round(lo)} to ${Math.round(hiV)}</div><p>${esc(tr.unit ?? '')}</p>
      <p class="assume">${hi ? 'मान्यता' : 'assumption'}: ${esc(tr.assumption ?? '')}</p>
      ${tr.factors ? `<p class="assume"><code>${tr.factors.map((f) => `${esc(f.name)} [${f.low} .. ${f.high}]`).join(' x ')}</code></p>` : ''}</div>`
      : `<p class="empty box">${hi ? 'अभी कोई अनुमान नहीं.' : 'No estimate yet.'}</p>`}`
}
const picker = await cityPicker(render)
$('.city-slot').append(picker.el)
if (picker.first) render(picker.first)
onLang(() => { const id = page.querySelector('select')?.value; if (picker.first) import('../data/data.js').then((m) => m.loadCity(id ?? picker.first.id)).then(render) })
