import { boot, head, bi, t, esc, onLang, getLang } from './common.js'
import { content, cities } from '../data/data.js'

boot('data')
const page = document.getElementById('page')
page.innerHTML = head({ kicker: { en: 'data', hi: 'डेटा' }, title: { en: 'where every line comes from', hi: 'हर रेखा कहाँ से आई' },
  lede: { en: 'Map data, photos, labels, code, fonts and the numbers we quote, each with its licence. Rows marked verify are still being checked.', hi: 'नक्शा, फ़ोटो, लेबल, कोड, फ़ॉन्ट और हमारे आँकड़े, हर एक का लाइसेंस. "verify" वाली पंक्तियाँ अभी जाँची जा रही हैं.' } }) + `<div class="src"></div>
  <h2 class="section-title">${bi({ en: 'city data on this site', hi: 'इस साइट पर शहर डेटा' })}</h2><div class="cities"></div>
  <p class="muted">${bi({ en: 'Full licence texts ship with the site: /fonts/OFL.txt, /fonts/OFL-Gloock.txt, /fonts/OFL-Baloo2.txt, /chars/SOURCES.md.', hi: 'पूरे लाइसेंस साइट के साथ हैं: /fonts/OFL.txt, /fonts/OFL-Gloock.txt, /fonts/OFL-Baloo2.txt, /chars/SOURCES.md.' })}</p>`
const src = await content('sources')
const list = await cities()
function render() {
  const hi = getLang() === 'hi'
  page.querySelector('.src').innerHTML = (src.placeholder ? `<p class="muted small">${hi ? 'कुछ लाइसेंस पर "verify" टैग है; सबमिशन से पहले हर पंक्ति स्रोत पर दोबारा जाँची जाएगी.' : 'Some licences still carry a verify tag; every row is re-checked at the provider page before submission.'}</p>` : '') + src.groups.map((g) => `<section class="src-group"><h2 class="section-title" style="font-size:30px">${esc(t(g.title))}</h2>
    <div class="table-wrap box"><table><thead><tr><th>${hi ? 'स्रोत' : 'source'}</th><th>${hi ? 'उपयोग' : 'used for'}</th><th>${hi ? 'लाइसेंस' : 'licence'}</th></tr></thead><tbody>
    ${g.rows.map((r) => `<tr><td><a href="${esc(r.url)}"${r.url.startsWith('http') ? ' target="_blank" rel="noopener"' : ''}>${esc(r.name)}</a></td><td>${esc(r.use)}</td><td>${esc(r.license)}${r.verify ? ' <span class="verify">verify</span>' : ''}</td></tr>`).join('')}
    </tbody></table></div></section>`).join('')
  page.querySelector('.cities').innerHTML = `<div class="table-wrap box"><table><thead><tr><th>id</th><th>${hi ? 'नाम' : 'name'}</th><th>${hi ? 'प्रकार' : 'kind'}</th></tr></thead><tbody>
    ${list.map((c) => `<tr><td>${esc(c.id)}</td><td>${esc(c.name)}</td><td>${c.mock ? (hi ? 'नकली' : 'mock') : (hi ? 'असली' : 'real')}</td></tr>`).join('') || '<tr><td colspan="3">none</td></tr>'}</tbody></table></div>`
}
render(); onLang(render)
