// screenshots of /map v2 into shots/map-v2/. usage: node tools/shot-map2.mjs [--gpu amd|sw] [--only name,...]
// desktop 1920x1080 and phone 390x844; hovers an element to capture the card. exits 2 on page or console errors.
import { parseArgs } from 'node:util'
import { mkdir } from 'node:fs/promises'
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'

const { values: a } = parseArgs({ options: { gpu: { type: 'string', default: 'amd' }, only: { type: 'string', default: '' }, browser: { type: 'string', default: '/usr/bin/brave' } } })
const args = a.gpu === 'sw' ? ['--enable-unsafe-swiftshader'] : ['--use-angle=gl-egl', '--ignore-gpu-blocklist', '--enable-features=Vulkan', '--disable-vulkan-surface']
const server = await createServer({ root: new URL('..', import.meta.url).pathname, logLevel: 'error', server: { port: 0 } })
await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: a.browser, headless: true, args: ['--no-first-run', '--hide-scrollbars', ...args] })
const wait = (ms) => new Promise((r) => setTimeout(r, ms))
const desk = { width: 1920, height: 1080, deviceScaleFactor: 1 }
const lap = { width: 1440, height: 900, deviceScaleFactor: 1 }
const phone = { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
const hoverFirst = (pred) => async (p) => {
  const pt = await p.evaluate((pred) => {
    const { map, S } = window.__map2
    const f = (eval(pred))
    const els = S.els.filter((x) => x.inside && f(x))
    const r = map.getContainer().getBoundingClientRect()
    const z = map.getZoom(), k = z >= 19 ? 1.25 : z >= 17 ? 1 + 0.25 * (z - 17) / 2 : 0.75 + 0.25 * (z - 14) / 3
    const size = (x) => (x.positive ? 0.46 : x.status !== 'ACCEPT' ? 0.54 : 0.6) * k
    for (const x of els) { const q = map.project(x.position); const fx = (x.fan?.[0] ?? 0) * size(x), fy = (x.fan?.[1] ?? 0) * size(x); if (q.x > 200 && q.x < r.width - 500 && q.y > 120 && q.y < r.height - 150) return { x: q.x + fx + r.left, y: q.y + fy + r.top, id: x.id } }
    return null
  }, pred)
  if (!pt) return 'no element in view'
  await p.mouse.move(pt.x, pt.y); await wait(300); await p.mouse.move(pt.x + 1, pt.y + 1); await wait(700)
  return pt.id
}
const jobs = [
  ['desk-chandigarh', desk, '/map/?city=chandigarh', null],
  ['desk-chandigarh-hover', desk, '/map/?city=chandigarh', async (p) => { await p.evaluate(() => window.__map2.map.jumpTo({ zoom: 17.2, center: window.__map2.S.els.find((x) => x.status === 'ACCEPT' && x.inside && !x.positive).position })); await wait(2500); return hoverFirst('(x) => x.status === "ACCEPT" && !x.positive')(p) }],
  ['desk-jaipur-photos', desk, '/map/?city=jaipur-photos', null],
  ['desk-jaipur-photos-hover', desk, '/map/?city=jaipur-photos', async (p) => { await p.evaluate(() => { const x = window.__map2.S.els.find((e) => e.inside && e.photo && e.candidates.length); window.__map2.map.jumpTo({ zoom: 17.6, center: x.position }) }); await wait(2500); return hoverFirst('(x) => x.photo && x.candidates.length')(p) }],
  ['desk-jaipur', desk, '/map/?city=jaipur', null],
  ['desk-2d', desk, '/map/?city=chandigarh', async (p) => { await p.click('.view [data-v="2d"]'); await wait(1500) }],
  ['laptop-chandigarh', lap, '/map/?city=chandigarh', null],
  ['desk-jaipur-photos-blind', desk, '/map/?city=jaipur-photos&body=blind_cane', async (p) => { await p.evaluate(() => { const x = window.__map2.S.els.find((e) => e.inside && e.photo && e.type === 'pole_obstruction'); window.__map2.map.jumpTo({ zoom: 17.4, center: x.position }) }); await wait(2500); return hoverFirst('(x) => x.type === "pole_obstruction"')(p) }],
  ['desk-chandigarh-blind-rain', desk, '/map/?city=chandigarh&body=blind_cane', async (p) => { await p.select('.ctx-sel', 'rain'); await wait(2500) }],
  ['desk-chandigarh-museum-tetra', desk, '/map/?city=chandigarh&trip=s17-museum&body=mw_tetraplegia', null],
  ['phone-card', phone, '/map/?city=chandigarh', async (p) => { await p.evaluate(() => { const { S, openCard, map } = window.__map2; const x = S.els.find((e) => e.status === 'ACCEPT' && e.inside && !e.positive); map.jumpTo({ zoom: 17.5, center: x.position }); openCard(x, { x: 100, y: 100 }, true) }); await wait(1500) }],
  ['phone-chandigarh', phone, '/map/?city=chandigarh', null],
  ['phone-panel', phone, '/map/?city=jaipur-photos', async (p) => { await p.click('.sheet-handle'); await wait(800) }],
]
await mkdir('shots/map-v2', { recursive: true })
let bad = 0
for (const [name, vp, path, prep] of jobs) {
  if (a.only && !a.only.split(',').some((o) => name.startsWith(o))) continue
  const page = await browser.newPage()
  await page.setViewport(vp)
  const problems = []
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon/.test(m.text())) problems.push(m.text()) })
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`))
  await page.evaluateOnNewDocument(() => { try { sessionStorage.setItem('hyp.entered', '1'); localStorage.setItem('kit.sound', 'off') } catch {} })
  await page.goto(base + path, { waitUntil: 'networkidle2', timeout: 90000 })
  await page.waitForFunction(() => window.__map2?.ready, { timeout: 60000 }).catch(() => problems.push('never ready'))
  // the camera flies 2.2 s and tiles stream in after it: wait until the map is idle, then a beat more
  await wait(3000)
  await page.evaluate(() => new Promise((r) => { const m = window.__map2?.map; if (!m) return r(); if (m.loaded() && !m.isMoving()) return r(); m.once('idle', r); setTimeout(r, 12000) }))
  await wait(1200)
  let note = ''
  if (prep) { try { note = (await prep(page)) ?? '' } catch (e) { problems.push(`prepare: ${e.message}`) } }
  await wait(800)
  await page.screenshot({ path: `shots/map-v2/${name}.png` })
  console.log(name, note, problems.length ? `PROBLEMS: ${problems.join(' | ')}` : 'ok')
  if (problems.length) bad++
  await page.close()
}
await browser.close(); await server.close()
process.exit(bad ? 2 : 0)
