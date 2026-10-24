// screenshots of /how v2 into shots/how-v2/: desktop + mobile, rest, hover, mid-run moments, reduced motion,
// plus overflow and console checks. node how/tools/shot-how.mjs [--zoom]   (run from app/site)
import { mkdir, writeFile } from 'node:fs/promises'
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'

const OUT = 'shots/how-v2'
await mkdir(OUT, { recursive: true })
const server = await createServer({ root: new URL('../..', import.meta.url).pathname, logLevel: 'error', server: { port: 0 } })
await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--hide-scrollbars'] })
const wait = (ms) => new Promise((r) => setTimeout(r, ms))
let bad = 0

async function open(vp, { reduce = false } = {}) {
  const page = await browser.newPage()
  await page.setViewport(vp)
  if (reduce) await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }])
  const problems = []
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|ERR_/.test(m.text())) problems.push(m.text()) })
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`))
  await page.evaluateOnNewDocument(() => { try { sessionStorage.setItem('hyp.entered', '1'); localStorage.setItem('kit.sound', 'off') } catch {} })
  await page.goto(base + '/how/', { waitUntil: 'networkidle0', timeout: 60000 })
  await wait(1200)
  return { page, problems }
}
const shot = async (page, name, opts = {}) => { await writeFile(`${OUT}/${name}.png`, await page.screenshot(opts)); console.log('shot', name) }
const overflow = (page) => page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)

// desktop
{
  const { page, problems } = await open({ width: 1440, height: 1000, deviceScaleFactor: 1 })
  await shot(page, 'desktop-rest')
  await shot(page, 'desktop-full', { fullPage: true })
  // hover the sieve
  const box = await page.evaluate(() => { const r = document.querySelector('[data-name="sieve"]').getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2] })
  await page.mouse.move(box[0], box[1]); await wait(400)
  await shot(page, 'desktop-hover-sieve')
  await page.mouse.move(5, 5)
  await page.evaluate(() => window.__how.play(0))
  const fps = await page.evaluate(() => new Promise((res) => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < 2000) requestAnimationFrame(f); else res(n / 2) }; requestAnimationFrame(f) }))
  console.log('fps during run (headless, software):', fps)
  for (const [ms, name] of [[1, 'run-01-hopper'], [3000, 'run-02-stoneA'], [3800, 'run-03-agreement'], [2200, 'run-04-ground'], [2600, 'run-05-impact'], [2500, 'run-06-placement'], [6000, 'run-07-end']]) { await wait(ms); await shot(page, name) }
  const of = await overflow(page)
  console.log(`desktop overflow ${of}px; ${problems.length ? 'PROBLEMS ' + problems.join(' | ') : 'no console errors'}`)
  if (of > 0 || problems.length) bad++
  if (process.argv.includes('--zoom')) {
    await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 3 })
    await page.evaluate(() => scrollTo(0, 0)); await wait(300)
    const r = await page.evaluate(() => { const b = document.querySelector('.mill-svg').getBoundingClientRect(); return { x: b.x, y: b.y, w: b.width, h: b.height } })
    const tiles = [['z-hopper', 0.0, 0.0], ['z-stones', 0.22, 0.25], ['z-sieve', 0.42, 0.42], ['z-rack', 0.58, 0.2], ['z-scales', 0.52, 0.5], ['z-tray', 0.7, 0.6]]
    for (const [name, fx, fy] of tiles) await shot(page, name, { clip: { x: r.x + r.w * fx, y: r.y + r.h * fy, width: r.w * 0.3, height: r.h * 0.38 } })
  }
  await page.close()
}
// mobile
{
  const { page, problems } = await open({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true })
  await shot(page, 'mobile-rest')
  await shot(page, 'mobile-full', { fullPage: true })
  await page.evaluate(() => window.__how.play(2))
  await wait(3500)
  await shot(page, 'mobile-run')
  const of = await overflow(page)
  console.log(`mobile overflow ${of}px; ${problems.length ? 'PROBLEMS ' + problems.join(' | ') : 'no console errors'}`)
  if (of > 0 || problems.length) bad++
  await page.close()
}
// reduced motion: run jumps to a still end frame
{
  const { page, problems } = await open({ width: 1440, height: 1000, deviceScaleFactor: 1 }, { reduce: true })
  await page.evaluate(() => window.__how.play(0)); await wait(500)
  await shot(page, 'reduced-motion-end')
  if (problems.length) { bad++; console.log('reduced PROBLEMS', problems.join(' | ')) }
  await page.close()
}
await browser.close(); await server.close()
process.exit(bad ? 2 : 0)
