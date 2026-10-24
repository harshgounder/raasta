// barrier evidence "receipt": photo crop, ACCEPT / ABSTAIN / REJECT badge, height +- error, observed date, segment
// placement, detectors, source link. works for a network barrier record and for an /analyze answer
import { t, getLang } from '../shell/shell.js'
import { TYPE_LABEL } from '../data/data.js'

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const L = {
  observed: { en: 'observed', hi: 'देखा गया' }, height: { en: 'height', hi: 'ऊँचाई' }, segment: { en: 'segment', hi: 'खंड' },
  source: { en: 'source', hi: 'स्रोत' }, conf: { en: 'confidence', hi: 'भरोसा' }, det: { en: 'detectors', hi: 'डिटेक्टर' },
  none: { en: 'not measured', hi: 'मापा नहीं' }, mock: { en: 'mock data', hi: 'नकली डेटा' }, why: { en: 'why', hi: 'क्यों' },
  status: { ACCEPT: { en: 'accept', hi: 'स्वीकार' }, ABSTAIN: { en: 'abstain', hi: 'अनिश्चित' }, REJECT: { en: 'reject', hi: 'अस्वीकार' } },
  meaning: { ACCEPT: { en: 'two detectors agree: known barrier', hi: 'दोनों डिटेक्टर सहमत: पक्की रुकावट' }, ABSTAIN: { en: 'not sure, so we do not guess', hi: 'पक्का नहीं, इसलिए अंदाज़ा नहीं' }, REJECT: { en: 'checked: not a barrier', hi: 'जाँचा: रुकावट नहीं' } },
}

// normalise an /analyze answer or a network barrier into one shape
export function toReceipt(x) {
  if (!x) return null
  const b = x.barrier ?? x
  return {
    id: x.id ?? b.id, type: b.type, status: (x.status ?? b.status ?? 'ABSTAIN').toUpperCase(), confidence: b.confidence ?? x.boxes?.[0]?.score ?? null,
    height_cm: x.height?.value_cm ?? b.height_cm ?? null, height_err_cm: x.height?.err_cm ?? b.height_err_cm ?? null, heightRoutes: x.height?.routes ?? null,
    observed: b.observed ?? x.observed ?? null, photo: b.photo ?? (x.image ? { url: x.image.url, crop: [0, 0, 1, 1] } : null),
    segment_id: x.place?.segment_id ?? b.segment_id ?? null, segment_p: x.place?.p ?? b.segment_p ?? null,
    candidates: x.place?.candidates ?? b.segment_alternatives ?? [], source_url: b.source_url ?? x.source_url ?? null,
    detectors: b.detectors ?? null, origin: b.origin ?? null, label: b.label ?? null, reason: x.abstain_reason ?? b.abstain_reason ?? null, mock: !!(x.mock ?? b.mock),
  }
}

export function receiptHtml(r) {
  if (!r) return ''
  const st = ['ACCEPT', 'ABSTAIN', 'REJECT'].includes(r.status) ? r.status : 'ABSTAIN'
  const h = r.height_cm != null ? `${r.height_cm} cm <span class="pm">± ${r.height_err_cm ?? '?'} cm</span>` : t(L.none)
  const routes = r.heightRoutes?.filter((x) => x.cm != null).map((x) => `${esc(x.method)} ${x.cm}`).join(' · ')
  const det = r.detectors ? `A ${esc(r.detectors.a?.label)} ${r.detectors.a?.score ?? ''} · B ${esc(r.detectors.b?.label)} ${r.detectors.b?.score ?? ''}` : ''
  const cand = r.candidates?.length ? r.candidates.map((c) => `${esc(c.segment_id)} ${Math.round((c.p ?? 0) * 100)}%`).join(' · ') : ''
  return `<article class="receipt box" data-status="${st}">
    <header><span class="badge-st st-${st.toLowerCase()}">${st}</span><span class="type">${esc(t(TYPE_LABEL[r.type]) || r.type)}</span>${r.mock ? `<span class="placeholder-tag">${t(L.mock)}</span>` : ''}</header>
    <p class="meaning">${r.origin === 'project_sidewalk' ? (getLang() === 'hi' ? `Project Sidewalk का मानव लेबल (CC0), हमारा डिटेक्टर नहीं${r.label ? `: ${esc(r.label)}` : ''}` : `human label from Project Sidewalk (CC0), not our detector${r.label ? `: ${esc(r.label)}` : ''}`) : t(L.meaning[st])}${r.reason ? `. ${t(L.why)}: ${esc(r.reason)}` : ''}</p>
    ${r.photo?.url ? `<canvas class="crop" width="480" height="300" data-src="${esc(r.photo.url)}" data-crop="${esc(JSON.stringify(r.photo.crop ?? [0, 0, 1, 1]))}" role="img" aria-label="photo crop of the barrier"></canvas>
      ${r.photo.credit ? `<p class="credit">${esc(r.photo.credit)}${r.photo.license ? `, ${esc(r.photo.license)}` : ''}</p>` : ''}` : ''}
    <dl>
      <dt>${t(L.height)}</dt><dd>${h}${routes ? `<small>${routes}</small>` : ''}</dd>
      <dt>${t(L.observed)}</dt><dd>${esc(r.observed ?? '?')}</dd>
      <dt>${t(L.segment)}</dt><dd>${esc(r.segment_id ?? '?')}${r.segment_p != null ? ` · p ${Math.round(r.segment_p * 100)}%` : ''}${cand ? `<small>${cand}</small>` : ''}</dd>
      ${r.confidence != null ? `<dt>${t(L.conf)}</dt><dd>${Math.round(r.confidence * 100)}%</dd>` : ''}
      ${det ? `<dt>${t(L.det)}</dt><dd><small>${det}</small></dd>` : ''}
      <dt>${t(L.source)}</dt><dd>${r.source_url ? `<a href="${esc(r.source_url)}" target="_blank" rel="noopener">${esc(new URL(r.source_url, location.href).hostname)}</a>` : '?'}</dd>
    </dl>
  </article>`
}

// draw photo crops into their canvases (after the html is in the DOM)
export function paintCrops(root) {
  root.querySelectorAll('canvas.crop[data-src]').forEach((c) => {
    const img = new Image()
    img.onload = () => {
      const [x, y, w, h] = JSON.parse(c.dataset.crop)
      const sw = Math.max(1, w * img.naturalWidth), sh = Math.max(1, h * img.naturalHeight)
      c.height = Math.round(c.width * sh / sw)
      c.getContext('2d').drawImage(img, x * img.naturalWidth, y * img.naturalHeight, sw, sh, 0, 0, c.width, c.height)
    }
    img.onerror = () => { c.replaceWith(Object.assign(document.createElement('p'), { className: 'credit', textContent: getLang() === 'hi' ? 'फ़ोटो नहीं मिली' : 'photo not found' })) }
    img.src = c.dataset.src
  })
}
