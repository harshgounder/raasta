// headless browser walk through /report: fill the branching form, send, wait for the trail, screenshot.
// usage: node app/reports/tests/ui_flow.mjs [siteBase] [outDir] [--mobile] [--photo path] [--offline]
import { createRequire } from 'node:module'
const puppeteer = createRequire('/home/liebert511/hypnexis-main/app/site/package.json')('puppeteer-core')
const args = process.argv.slice(2)
const flag = (k) => args.includes(k)
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d }
const pos = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--') && ['--photo', '--reports'].includes(args[i - 1])))
const base = pos[0] ?? 'http://127.0.0.1:5191', out = pos[1] ?? '/tmp'
const mobile = flag('--mobile'), photo = opt('--photo', null), reports = opt('--reports', null)
const b = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--use-fake-ui-for-media-stream', '--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
const p = await b.newPage()
await p.setViewport(mobile ? { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { width: 1440, height: 900 })
const ctx = b.defaultBrowserContext(); await ctx.overridePermissions(base, ['geolocation'])
await p.setGeolocation({ latitude: 26.92560, longitude: 75.80640, accuracy: 9 })
const errs = []
p.on('pageerror', (e) => errs.push('pageerror ' + e.message)); p.on('console', (m) => m.type() === 'error' && errs.push('console ' + m.text()))
await p.evaluateOnNewDocument(() => { try { sessionStorage.setItem('hyp.entered', '1'); localStorage.setItem('hyp.entered', '1') } catch {} })
const url = base + '/report/' + (reports ? `?reports=${encodeURIComponent(reports)}` : '')
await p.goto(url, { waitUntil: 'domcontentloaded' }); await p.waitForSelector('.cats button', { timeout: 20000 })
await p.evaluate(() => document.querySelector('.gate:not([hidden]) button:last-of-type')?.click())
await new Promise((r) => setTimeout(r, 800))
await p.screenshot({ path: `${out}/report-form${mobile ? '-mobile' : ''}.png`, fullPage: true })
const click = (sel) => p.evaluate((s) => { const e = document.querySelector(s); e.scrollIntoView({ block: 'center' }); e.click() }, sel)
await click('.cats [data-v="level"]'); await click('.types [data-v="kerb_no_ramp"]')
await click('.dq[data-q="ramp"] [data-v="none"]'); await click('.dq[data-q="height"] [data-v="shin"]')
await click('.bgroups [data-v="wheels"]'); await click('.leaves [data-v="mw_self"]')
await click('.gps'); await new Promise((r) => setTimeout(r, 1500))
await click('.side [data-v="left"]'); await click('.since [data-v="always"]'); await click('.hurt [data-v="turned_back"]')
if (photo) { const h = await p.$('.photo-in'); await h.uploadFile(photo); await new Promise((r) => setTimeout(r, 1200)) }
const t0 = Date.now()
await p.evaluate(() => { window.__clickAt = Math.round(performance.now()) })
await click('.send')
await p.waitForSelector('.trail-wrap:not([hidden])', { timeout: 30000 })
const sent = Date.now() - t0
let firstLook = null
for (let i = 0; i < 60; i++) {
  const s = await p.evaluate(() => [...document.querySelectorAll('.trail li')].map((li) => li.className))
  if (s.length && !s[1].includes('active') && !s[2].includes('active')) { firstLook = Date.now() - t0; break }
  if (!s.length) break
  await new Promise((r) => setTimeout(r, 500))
}
await p.evaluate(() => document.querySelector('.trail-wrap').scrollIntoView())
await p.screenshot({ path: `${out}/report-trail${mobile ? '-mobile' : ''}.png`, fullPage: true })
const info = await p.evaluate(() => ({ fetches: performance.getEntriesByType('resource').filter((e) => e.name.includes(':8790/') && e.initiatorType === 'fetch').slice(0, 4).map((e) => `${e.name.split(':8790')[1].slice(0, 30)} start=${Math.round(e.startTime)} dur=${Math.round(e.duration)}`), clickAt: window.__clickAt, key: document.querySelector('.key-status')?.innerText, rid: document.querySelector('.rid b')?.textContent, svc: document.querySelector('.svc')?.innerText, mine: document.querySelectorAll('.mine-ul li').length, overflow: document.documentElement.scrollWidth > innerWidth }))
console.log(JSON.stringify({ ...info, ms_to_trail: sent, ms_to_first_look_done: firstLook, errors: errs }, null, 1))
await b.close()
