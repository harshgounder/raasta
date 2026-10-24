// story v2 frame capture: Vite dev server + headless Brave, /?snap (no lerp, no idle motion), one jpg every STEP px
// into shots/v2/<tag>/, plus console errors. usage: node tools/story-frames.mjs [--step 300] [--from 0] [--to 0] [--mobile] [--tag desk] [--gpu amd|sw]
import { parseArgs } from 'node:util'
import { mkdir, writeFile } from 'node:fs/promises'
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'

const { values: a } = parseArgs({ options: { step: { type: 'string', default: '300' }, from: { type: 'string', default: '0' }, to: { type: 'string', default: '0' }, mobile: { type: 'boolean', default: false }, tag: { type: 'string', default: '' }, gpu: { type: 'string', default: 'amd' }, wait: { type: 'string', default: '350' }, ys: { type: 'string', default: '' } } })
const common = ['--use-angle=gl-egl', '--ignore-gpu-blocklist']
const args = a.gpu === 'sw' ? ['--enable-unsafe-swiftshader'] : [...common, '--disable-vulkan-surface']
const root = new URL('..', import.meta.url).pathname
const server = await createServer({ root, logLevel: 'error', server: { port: 0 } })
await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--hide-scrollbars', ...args] })
const vp = a.mobile ? { width: 390, height: 844, deviceScaleFactor: 1, isMobile: true, hasTouch: true } : { width: 1440, height: 900, deviceScaleFactor: 1 }
const tag = a.tag || (a.mobile ? 'mobile' : 'desk')
const out = `${root}shots/v2/${tag}/`
await mkdir(out, { recursive: true })
const page = await browser.newPage()
await page.setViewport(vp)
const errs = []
page.on('pageerror', (e) => errs.push('pageerror ' + e.message))
page.on('console', (m) => { if (m.type() === 'error') errs.push('console ' + m.text()) })
await page.goto(base + '/?snap', { waitUntil: 'load', timeout: 60000 })
await page.waitForFunction(() => window.__story && window.__story.ready(), { timeout: 20000 }).catch(() => errs.push('textures not ready in 20 s'))
const total = await page.evaluate(() => __story.total)
const to = Number(a.to) || total + 900
const step = Number(a.step)
const wait = (ms) => new Promise((r) => setTimeout(r, ms))
const list = []
const ys = a.ys ? a.ys.split(',').map(Number) : []
if (!ys.length) for (let y = Number(a.from); y <= to; y += step) ys.push(y)
for (const y of ys) {
  await page.evaluate((y) => scrollTo(0, y), y)
  await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))))
  await wait(Number(a.wait))
  const f = `y-${String(y).padStart(6, '0')}.jpg`
  await page.screenshot({ path: out + f, type: 'jpeg', quality: 70, captureBeyondViewport: false })
  list.push(f)
}
await writeFile(out + 'frames.json', JSON.stringify({ total, step, vp, panels: await page.evaluate(() => __story.panels()), errs, list }, null, 1))
console.log(JSON.stringify({ total, frames: list.length, errs }, null, 1))
await browser.close(); await server.close()
