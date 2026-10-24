// shared frame for all 8 pages: nav pill, language (en / hi), sound gate (click to enter), cursor badge, ink wipe page
// transitions, the rough-box filter that boils at 8 fps (santioni grammar: everything hand-cut redraws 8 times a second)
import './tokens.css'
import { createAudio } from '../kit/audio/audio.js'

export const PAGES = [
  { id: 'story', href: '/', en: 'story', hi: 'कहानी' },
  { id: 'map', href: '/map/', en: 'map', hi: 'नक्शा' },
  { id: 'scan', href: '/scan/', en: 'scan', hi: 'स्कैन' },
  { id: 'city', href: '/city/', en: 'city', hi: 'शहर' },
  { id: 'how', href: '/how/', en: 'how', hi: 'कैसे' },
  { id: 'what-if', href: '/what-if/', en: 'what if', hi: 'अगर' },
  { id: 'report', href: '/report/', en: 'report', hi: 'शिकायत' },
  { id: 'data', href: '/data/', en: 'data', hi: 'डेटा' },
]

const store = {
  get(k) { try { return localStorage.getItem(k) } catch { return null } },
  set(k, v) { try { localStorage.setItem(k, v) } catch {} },
  sget(k) { try { return sessionStorage.getItem(k) } catch { return null } },
  sset(k, v) { try { sessionStorage.setItem(k, v) } catch {} },
}
export const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)')

let lang = store.get('hyp.lang') === 'hi' ? 'hi' : 'en'
const langSubs = new Set()
export const getLang = () => lang
export const t = (o) => (o == null ? '' : typeof o === 'string' ? o : o[lang] ?? o.en ?? '')
export function onLang(fn) { langSubs.add(fn); return () => langSubs.delete(fn) }
export function setLang(l) {
  lang = l === 'hi' ? 'hi' : 'en'; store.set('hyp.lang', lang)
  document.documentElement.lang = lang
  document.querySelectorAll('[data-en]').forEach((el) => { el.textContent = el.dataset[lang] ?? el.dataset.en })
  langSubs.forEach((f) => f(lang))
}

// the BACKEND_URL for /analyze: ?api= > localStorage > window.HYP_CONFIG (public/config.js) > VITE_BACKEND_URL > none
export function backendUrl() {
  const q = new URLSearchParams(location.search).get('api')
  if (q) store.set('hyp.api', q)
  return (q || store.get('hyp.api') || window.HYP_CONFIG?.BACKEND_URL || import.meta.env.VITE_BACKEND_URL || '').replace(/\/$/, '')
}
export function setBackendUrl(u) { store.set('hyp.api', (u ?? '').trim()) }

export function initShell({ page, withAudio = true } = {}) {
  document.documentElement.lang = lang
  document.body.classList.add(`${page}-page`)

  // rough edge filter, boiled by re-seeding
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true'); svg.style.position = 'absolute'
  svg.innerHTML = `<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="1" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter>`
  document.body.prepend(svg)
  const turb = svg.querySelector('feTurbulence')
  let seed = 1
  setInterval(() => { if (!reduceMotion.matches && !document.hidden) turb.setAttribute('seed', String((seed = (seed % 4) + 1))) }, 125)

  // nav
  const nav = document.createElement('nav')
  nav.className = 'site-nav box'; nav.setAttribute('aria-label', 'site')
  nav.innerHTML = `<button class="menu-btn" type="button" aria-expanded="false" data-en="menu" data-hi="मेनू">menu</button>` +
    PAGES.map((p) => `<a href="${p.href}" data-en="${p.en}" data-hi="${p.hi}"${p.id === page ? ' aria-current="page"' : ''}>${p[lang]}</a>`).join('') +
    `<button class="lang-btn" type="button" aria-label="language: switch English or Hindi">${lang === 'hi' ? 'EN' : 'हिंदी'}</button>`
  document.body.prepend(nav)
  const home = Object.assign(document.createElement('a'), { className: 'home-mark', href: '/', textContent: 'RAASTA' })
  home.setAttribute('aria-label', 'home: the story')
  document.body.prepend(home)
  const menuBtn = nav.querySelector('.menu-btn')
  menuBtn.addEventListener('click', () => { const o = nav.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', String(o)) })
  const langBtn = nav.querySelector('.lang-btn')
  langBtn.addEventListener('click', () => { setLang(lang === 'hi' ? 'en' : 'hi'); langBtn.textContent = lang === 'hi' ? 'EN' : 'हिंदी' })

  // audio: the story page brings its own graph (it rides the beds from scroll); other pages get a quiet bed
  let audio = withAudio ? createAudio() : null
  const attachAudio = (a) => { audio = a }

  // sound gate: only the story asks on entry. Subpages (map, city, what-if...) are opened cold by
  // judges from a link, so blocking them behind a story dialog is wrong; they stay silent until a press.
  const wantsGate = page === 'story'
  const entered = !wantsGate || store.sget('hyp.entered') === '1'
  const gateEl = document.createElement('div')
  gateEl.className = 'gate'; gateEl.setAttribute('role', 'dialog'); gateEl.setAttribute('aria-modal', 'true'); gateEl.setAttribute('aria-labelledby', 'gate-title')
  gateEl.innerHTML = `<h2 id="gate-title" data-en="the same street" data-hi="वही गली">${lang === 'hi' ? 'वही गली' : 'the same street'}</h2>
    <p data-en="A story about one footpath, seen by five bodies. Best with sound." data-hi="एक फुटपाथ की कहानी, पाँच शरीरों की नज़र से. आवाज़ के साथ बेहतर.">${lang === 'hi' ? 'एक फुटपाथ की कहानी, पाँच शरीरों की नज़र से. आवाज़ के साथ बेहतर.' : 'A story about one footpath, seen by five bodies. Best with sound.'}</p>
    <div class="row"><button class="box" type="button" data-answer="yes" data-en="enter with sound" data-hi="आवाज़ के साथ">${lang === 'hi' ? 'आवाज़ के साथ' : 'enter with sound'}</button>
    <button class="box quiet" type="button" data-answer="no" data-en="enter quietly" data-hi="बिना आवाज़">${lang === 'hi' ? 'बिना आवाज़' : 'enter quietly'}</button></div>`
  gateEl.hidden = entered
  document.body.append(gateEl)
  let resolvePass
  const gate = { el: gateEl, get open() { return !gateEl.hidden }, passed: new Promise((r) => { resolvePass = r }), boxes: () => [...gateEl.querySelectorAll('button')] }
  if (entered) resolvePass()
  else {
    document.documentElement.style.overflowY = 'hidden'
    requestAnimationFrame(() => gateEl.querySelector('button').focus())
  }
  gateEl.addEventListener('click', (e) => {
    const b = e.target.closest('[data-answer]'); if (!b) return
    const yes = b.dataset.answer === 'yes'
    if (audio) { audio.setMuted(!yes); if (yes) audio.unlock() }
    store.sset('hyp.entered', '1'); gateEl.hidden = true
    document.documentElement.style.overflowY = ''
    resolvePass(yes)
  })

  // pages after the first: sound starts on the first press anywhere (browsers want a gesture per document)
  if (withAudio) {
    const start = (e) => {
      if (gate.open || !audio || audio.muted || e.target.closest?.('.sound-toggle')) return
      if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return
      audio.unlock(); removeEventListener('pointerdown', start, true); removeEventListener('keydown', start, true)
    }
    addEventListener('pointerdown', start, true); addEventListener('keydown', start, true)
    // a quiet bed under every DOM page once the files are in
    const bed = setInterval(() => { if (audio?.ready) { audio.loop('drone-low', 0.22, { tc: 1.5 }); audio.loop('fog-air', 0.12, { tc: 1.5 }); clearInterval(bed) } }, 300)
    document.addEventListener('click', (e) => { if (e.target.closest('button, a, [role="radio"]') && audio?.ready) audio.play('ui-click', { gain: 0.5 }) })
  }

  // ink wipe between pages
  const wipe = Object.assign(document.createElement('div'), { className: 'wipe' })
  wipe.setAttribute('aria-hidden', 'true')
  document.body.append(wipe)
  if (store.sget('hyp.wipe') === '1' && !reduceMotion.matches) {
    store.sset('hyp.wipe', '0'); wipe.classList.add('start')
    requestAnimationFrame(() => requestAnimationFrame(() => { wipe.classList.remove('start'); wipe.classList.add('reveal') }))
    wipe.addEventListener('transitionend', () => { wipe.className = 'wipe' }, { once: true })
  }
  addEventListener('pageshow', (e) => { if (e.persisted) wipe.className = 'wipe' })
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]')
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return
    const url = new URL(a.href, location.href)
    if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash)) return
    e.preventDefault()
    if (audio?.ready) audio.play('whoosh', { gain: 0.7 })
    if (reduceMotion.matches) { location.href = url.href; return }
    store.sset('hyp.wipe', '1'); wipe.className = 'wipe cover'
    setTimeout(() => { location.href = url.href }, 470)
  })

  // cursor badge (DOM pages; the story draws it in GL)
  if (page !== 'story' && matchMedia('(hover: hover)').matches) {
    const c = Object.assign(document.createElement('div'), { className: 'cursor' })
    c.setAttribute('aria-hidden', 'true'); document.body.append(c)
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y
    addEventListener('pointermove', (e) => { x = e.clientX; y = e.clientY; c.classList.toggle('hot', !!e.target.closest?.('a, button, input, select, label, [role="radio"], .maplibregl-canvas')) })
    const tick = () => { const k = reduceMotion.matches ? 1 : 0.35; cx += (x - cx) * k; cy += (y - cy) * k; c.style.transform = `translate(${cx}px, ${cy}px)`; requestAnimationFrame(tick) }
    tick()
  }

  setLang(lang)
  return { gate, get audio() { return audio }, attachAudio, nav }
}
