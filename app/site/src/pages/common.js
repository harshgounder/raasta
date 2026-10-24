// shared bits for the DOM pages: shell boot, bilingual text nodes, page head, the "never says safe" legend, city picker
import './page.css'
import { initShell, t, onLang, getLang } from '../shell/shell.js'
import { cities, loadCity } from '../data/data.js'

export { t, onLang, getLang }
export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
// a bilingual text node: the shell swaps data-en / data-hi on language change
export const bi = (o, tag = 'span', cls = '') => `<${tag}${cls ? ` class="${cls}"` : ''} data-en="${esc(o.en)}" data-hi="${esc(o.hi ?? o.en)}">${esc(t(o))}</${tag}>`

export function boot(page) {
  const shell = initShell({ page })
  shell.audio?.button.classList.add('box')
  return shell
}

export function head({ kicker, title, lede, compact = false }) {
  return `<header class="page-head${compact ? ' compact' : ''}">
    ${kicker ? bi(kicker, 'p', 'kicker') : ''}
    ${bi(title, 'h1')}
    ${lede ? bi(lede, 'p', 'lede') : ''}
  </header>`
}

export const legendHtml = () => `<section class="legend box" aria-label="map legend">
  ${bi({ en: 'we never say safe', hi: 'हम कभी "सुरक्षित" नहीं कहते' }, 'h2')}
  <ul>
    <li><i class="sw sw-barrier" aria-hidden="true"></i>${bi({ en: 'known barrier: a dated photo or label, checked', hi: 'पक्की रुकावट: तारीख वाली फ़ोटो या लेबल, जाँचा हुआ' })}</li>
    <li><i class="sw sw-clear" aria-hidden="true"></i>${bi({ en: 'known clear, on the date of the photo only', hi: 'साफ़ देखा, सिर्फ़ फ़ोटो की तारीख पर' })}</li>
    <li><i class="sw sw-unknown" aria-hidden="true"></i>${bi({ en: 'unknown: no photo yet, so no claim', hi: 'अज्ञात: अभी फ़ोटो नहीं, तो कोई दावा नहीं' })}</li>
  </ul>
  <ul class="dots">
    <li><i class="dot dot-accept" aria-hidden="true"></i>ACCEPT</li><li><i class="dot dot-abstain" aria-hidden="true"></i>ABSTAIN</li><li><i class="dot dot-reject" aria-hidden="true"></i>REJECT</li>
  </ul>
</section>`

// city select; returns { el, list, current() }. remembers the choice per viewer
export async function cityPicker(onChange) {
  const list = await cities()
  const wrap = document.createElement('label')
  wrap.className = 'field'
  let saved = null; try { saved = localStorage.getItem('hyp.city') } catch {}
  const first = list.find((c) => c.id === saved) ?? list[0]
  wrap.innerHTML = `${bi({ en: 'city', hi: 'शहर' })}<select>${list.map((c) => `<option value="${esc(c.id)}"${c.id === first?.id ? ' selected' : ''}>${esc(c.name)}${c.mock ? ' (mock)' : ''}</option>`).join('')}</select>`
  const sel = wrap.querySelector('select')
  sel.addEventListener('change', async () => { try { localStorage.setItem('hyp.city', sel.value) } catch {}; onChange(await loadCity(sel.value)) })
  return { el: wrap, list, first: first ? await loadCity(first.id) : null }
}

export const mockBanner = (city) => (city?.mock ? `<p class="mock-banner">${bi({ en: 'MOCK DATA: invented grid, placeholder photos. Real city data replaces it.', hi: 'नकली डेटा: बनाया हुआ नक्शा, अस्थायी फ़ोटो. असली डेटा आने पर बदलेगा.' })}</p>` : '')
