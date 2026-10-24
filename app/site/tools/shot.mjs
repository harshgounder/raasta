// headless page screenshots of the site (kit tools/shot.mjs adapted to the multi-page site; the kit's own copy is
// tools/shot-kit.mjs). starts Vite on a free port, opens headless Brave with a temp profile, saves shots/<name>.png,
// exits 2 on any page error or console error.
// usage: node tools/shot.mjs [--gpu sw|amd|nvidia] [--only story,map] [--mobile]
import { parseArgs } from 'node:util'
import { mkdir, writeFile } from 'node:fs/promises'
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'

const { values: a } = parseArgs({ options: { gpu: { type: 'string', default: 'amd' }, only: { type: 'string', default: '' }, mobile: { type: 'boolean', default: false }, browser: { type: 'string', default: '/usr/bin/brave' } } })
const common = ['--use-angle=gl-egl', '--enable-unsafe-webgpu', '--enable-features=Vulkan', '--ignore-gpu-blocklist']
const recipes = {
  sw: { args: ['--enable-unsafe-swiftshader'] },
  amd: { args: [...common, '--disable-vulkan-surface', '--use-webgpu-power-preference=default-low-power'] },
  nvidia: { args: [...common], env: { __NV_PRIME_RENDER_OFFLOAD: '1', __GLX_VENDOR_LIBRARY_NAME: 'nvidia', __EGL_VENDOR_LIBRARY_FILENAMES: '/usr/share/glvnd/egl_vendor.d/10_nvidia.json' } },
}
const recipe = recipes[a.gpu] ?? recipes.sw
const server = await createServer({ root: new URL('..', import.meta.url).pathname, logLevel: 'error', server: { port: 0 } })
await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: a.browser, headless: true, args: ['--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required', ...recipe.args], env: { ...process.env, ...recipe.env } })
const vp = a.mobile ? { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { width: 1440, height: 900, deviceScaleFactor: 1 }
const sfx = a.mobile ? '-mobile' : ''
const wait = (ms) => new Promise((r) => setTimeout(r, ms))

// name, path, prepare(page), entered (skip the sound gate)
const jobs = [
  ['gate', '/', null, false],
  ['story-title', '/', null, true],
  ['story-guy', '/', async (p) => { await p.evaluate(() => scrollTo(0, __lab.beats[1].top + innerHeight * 0.4)) }, true],
  ['story-cat', '/', async (p) => { await p.evaluate(() => scrollTo(0, __lab.beats[2].top + innerHeight * 0.3)) }, true],
  ['story-switch-cat', '/', async (p) => { await p.evaluate(() => scrollTo(0, __lab.beats[1].top + innerHeight * 0.4)); await wait(900); await p.click('.bodies [data-body="cat"]') }, true],
  ['story-oldlady', '/', async (p) => { await p.evaluate(() => scrollTo(0, __lab.beats[4].top + innerHeight * 0.8)) }, true],
  ['story-wheelchair', '/', async (p) => { await p.evaluate(() => scrollTo(0, __lab.beats[5].top + innerHeight * 0.4)) }, true],
  ['story-end', '/', async (p) => { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)) }, true],
  // map v2 (src/map2): no __view any more; tools/shot-map2.mjs takes the detailed map shots
  ['map', '/map/', async (p) => { await p.waitForFunction(() => window.__map2?.ready, { timeout: 60000 }); await wait(3000) }, true],
  ['scan', '/scan/', async (p) => { await p.click('.gallery [data-i="2"]') }, true],
  ['city', '/city/', null, true],
  ['how', '/how/', null, true],
  ['what-if', '/what-if/', async (p) => { await p.click('.runner [data-id="w2"]'); await wait(1200); await p.evaluate(() => scrollTo(0, 0)) }, true],
  ['report', '/report/', null, true],
  ['data', '/data/', null, true],
]
await mkdir('shots', { recursive: true })
let bad = 0
for (const [name, path, prep, entered] of jobs) {
  if (a.only && !a.only.split(',').some((o) => name.startsWith(o))) continue
  const page = await browser.newPage()
  await page.setViewport(vp)
  const problems = []
  page.on('console', (m) => { if (m.type() === 'error' && !/tiles\.openfreemap|ERR_|favicon/.test(m.text())) problems.push(m.text()) })
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`))
  await page.evaluateOnNewDocument((en) => { try { if (en) sessionStorage.setItem('hyp.entered', '1'); localStorage.setItem('kit.sound', 'off') } catch {} }, entered)
  await page.goto(base + path, { waitUntil: 'networkidle0', timeout: 60000 })
  if (path === '/') await page.waitForFunction(() => window.__lab?.ready, { timeout: 60000 }).catch(() => problems.push('story never ready'))
  else await wait(2500)
  if (prep) { try { await prep(page) } catch (e) { problems.push(`prepare: ${e.message}`) } }
  await wait(path === '/' ? 1600 : 1500)
  const full = !['/', '/map/'].includes(path) && name !== 'gate'
  await writeFile(`shots/${name}${sfx}.png`, await page.screenshot({ fullPage: full }))
  console.log(`${problems.length ? 'FAIL' : 'ok  '} ${name}${sfx}${problems.length ? ': ' + problems.join(' | ') : ''}`)
  if (problems.length) bad++
  await page.close()
}
await browser.close(); await server.close()
process.exit(bad ? 2 : 0)
