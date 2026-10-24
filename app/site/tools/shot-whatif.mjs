// screenshots of /what-if v2 into shots/whatif-v2/. usage: node tools/shot-whatif.mjs [--gpu amd|sw] [--only name,...]
// desktop 1440x900 and phone 375x812. exits 2 on page errors or console errors.
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
const desk = { width: 1440, height: 900, deviceScaleFactor: 1 }
const phone = { width: 375, height: 812, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
const mapReady = async (p) => { await p.waitForFunction(() => window.__whatif?.ready, { timeout: 45000 }); await p.evaluate(() => new Promise((r) => { const m = window.__whatif.map; if (m.loaded() && !m.isMoving()) r(); else m.once('idle', r) })); await wait(1500) }
const scrollTo = (sel) => async (p) => { await p.evaluate((s) => { const e = document.querySelector(s); if (e) scrollTo(0, e.getBoundingClientRect().top + scrollY - (innerWidth < 640 ? 100 : 84)) }, sel); await wait(500) }
const jobs = [
  ['desk-tree-T1.1.1', desk, '/what-if/#T1.1.1', null, false],
  ['desk-map-T1.1.1', desk, '/what-if/#T1.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-mappanel')(p) }, false],
  ['desk-map-T6.1.1', desk, '/what-if/#T6.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-actions')(p) }, false],
  ['desk-map-T9.1.1', desk, '/what-if/#T9.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-mappanel')(p) }, false],
  ['desk-body-switch-T6.1.1', desk, '/what-if/#T6.1.1/run', async (p) => { await mapReady(p); const b = await p.$$('.wi-side .wi-cb'); if (b[2]) { await b[2].click(); await wait(1800) } await scrollTo('.wi-mappanel')(p) }, false],
  ['desk-map-T10.1.1', desk, '/what-if/#T10.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-mappanel')(p) }, false],
  ['desk-map-T2.1.1', desk, '/what-if/#T2.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-mappanel')(p) }, false],
  ['desk-hindi-T11.1.3', desk, '/what-if/#T11.1.3/run', async (p) => { await mapReady(p); await p.click('.lang-btn'); await wait(2000); await scrollTo('.wi-q')(p) }, false],
  ['desk-topics-all', desk, '/what-if/#T1.1.1', async (p) => { await p.evaluate(async () => { for (const t of [...document.querySelectorAll('[data-topic]')].map((x) => x.dataset.topic)) { document.querySelector('[data-topic="' + t + '"]').click(); await new Promise((r) => setTimeout(r, 30)); const s = document.querySelector('.wi-t.open [data-sub]'); s?.click(); await new Promise((r) => setTimeout(r, 30)); document.querySelector('.wi-irow')?.click(); await new Promise((r) => setTimeout(r, 300)) } }) }, false],
  ['desk-search', desk, '/what-if/#T4.1.1', async (p) => { await p.type('.wi-search input', 'kerb'); await wait(600) }, false],
  ['phone-top-T1.1.1', phone, '/what-if/#T1.1.1', null, false],
  ['phone-drawer', phone, '/what-if/#T6.1.1', async (p) => { await p.click('.wi-drawer'); await wait(500); await scrollTo('.wi-tree')(p) }, false],
  ['phone-full-T6.1.1', phone, '/what-if/#T6.1.1', null, true],
  ['phone-map-T9.1.1', phone, '/what-if/#T9.1.1/run', async (p) => { await mapReady(p); await scrollTo('.wi-mappanel')(p) }, false],
]
await mkdir('shots/whatif-v2', { recursive: true })
let bad = 0
for (const [name, vp, path, prep, full] of jobs) {
  if (a.only && !a.only.split(',').some((o) => name.startsWith(o))) continue
  const page = await browser.newPage()
  await page.setViewport(vp)
  const problems = []
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon/.test(m.text())) problems.push(m.text()) })
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`))
  await page.evaluateOnNewDocument(() => { try { sessionStorage.setItem('hyp.entered', '1'); localStorage.setItem('kit.sound', 'off'); localStorage.setItem('hyp.lang', 'en') } catch {} })
  await page.goto(base + path, { waitUntil: 'networkidle2', timeout: 90000 })
  await page.waitForSelector('.wi-qh', { timeout: 30000 }).catch(() => problems.push('no question rendered'))
  await wait(1200)
  if (prep) { try { await prep(page) } catch (e) { problems.push(`prepare: ${e.message}`) } }
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)
  if (overflow > 0) problems.push(`horizontal overflow ${overflow}px`)
  await page.screenshot({ path: `shots/whatif-v2/${name}.png`, fullPage: full })
  console.log(name, problems.length ? `PROBLEMS: ${problems.join(' | ')}` : 'ok')
  if (problems.length) bad++
  await page.close()
}
await browser.close(); await server.close()
process.exit(bad ? 2 : 0)
