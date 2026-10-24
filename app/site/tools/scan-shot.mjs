// end-to-end check of the LIVE SCAN page: starts Vite, opens /scan/ in headless Brave, uploads a photo to the
// live backend (?api=), waits for the receipt, screenshots desktop + mobile; then plays a recording with no backend.
// usage: node tools/scan-shot.mjs IMAGE [API]   -> shots/scan-live.png, shots/scan-live-mobile.png, shots/scan-rec.png
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'
import { mkdir } from 'node:fs/promises'

const [img, api = 'http://127.0.0.1:8010'] = process.argv.slice(2)
const server = await createServer({ root: new URL('..', import.meta.url).pathname, logLevel: 'error', server: { port: 0 } })
await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--enable-unsafe-swiftshader'] })
await mkdir(new URL('../shots/', import.meta.url), { recursive: true })
let errors = 0
async function one(name, vp, url, act) {
  const p = await browser.newPage()
  await p.setViewport(vp)
  p.on('pageerror', (e) => { errors++; console.log(name, 'PAGEERROR', e.message) })
  p.on('console', (m) => { if (m.type() === 'error') { console.log(name, 'console.error', m.text()) } })
  const t0 = Date.now()
  await p.goto(base + url, { waitUntil: 'networkidle2', timeout: 60000 })
  await act(p)
  await p.waitForFunction(() => document.querySelector('.sl-final.on'), { timeout: 90000 })
  await new Promise((r) => setTimeout(r, 1500))
  const st = await p.$eval('.sl-status', (e) => e.textContent)
  const nodes = await p.$$eval('.sl-node', (ns) => ns.map((n) => `${n.dataset.id}:${[...n.classList].filter((c) => ['wait', 'run', 'done', 'fail'].includes(c)).join('')}`))
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)
  console.log(name, ((Date.now() - t0) / 1000).toFixed(1) + 's', '|', st, '|', nodes.join(' '), '| h-overflow', overflow)
  await p.screenshot({ path: new URL(`../shots/${name}.png`, import.meta.url).pathname, fullPage: true })
  await p.close()
}
const upload = async (p) => { const h = await p.$('input.up'); await h.uploadFile(img) }
await one('scan-live', { width: 1440, height: 900 }, `/scan/?api=${encodeURIComponent(api)}`, upload)
await one('scan-live-mobile', { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, `/scan/?api=${encodeURIComponent(api)}`, upload)
await one('scan-rec', { width: 1440, height: 900 }, '/scan/?api=http://127.0.0.1:9', async (p) => { await p.evaluate(() => document.querySelector('[data-ex="1"]').click()) })
await browser.close(); await server.close()
process.exit(errors ? 2 : 0)
