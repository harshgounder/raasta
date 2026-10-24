// story v2 sound wiring test against the REAL public/audio/v2/MANIFEST.json: presses the toggle, walks the scroll
// through the whole story in small steps (snap mode), then reports per-cue loaded / fired counts and bed gains.
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'
const root = new URL('..', import.meta.url).pathname
const server = await createServer({ root, logLevel: 'error', server: { port: 0 } }); await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--autoplay-policy=no-user-gesture-required'] })
const page = await browser.newPage(); await page.setViewport({ width: 1440, height: 900 })
const errs = []; page.on('pageerror', (e) => errs.push(e.message)); page.on('console', (m) => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()) })
await page.goto(base + '/?snap', { waitUntil: 'load' }); await page.waitForFunction(() => window.__story?.ready(), { timeout: 20000 })
await page.click('.snd-btn')
await page.waitForFunction(() => __story.sound().filter((c) => c.loaded).length > 10, { timeout: 30000 }).catch(() => errs.push('cues not loaded in 30 s'))
const label = await page.$eval('.snd-btn', (b) => b.textContent)
const total = await page.evaluate(() => __story.total)
const beds = []
for (let y = 0; y < total; y += 120) {
  await page.evaluate((y) => scrollTo(0, y), y)
  await new Promise((r) => setTimeout(r, 45))
  if (y % 2400 === 0) beds.push([y, await page.evaluate(() => Object.fromEntries(__story.sound().filter((c) => c.gain != null).map((c) => [c.name, c.gain])))])
}
await new Promise((r) => setTimeout(r, 800))
console.log(JSON.stringify({ label, cues: await page.evaluate(() => __story.sound().map((c) => `${c.name}: loaded ${c.loaded} fired ${c.fired}`)), beds, errs }, null, 1))
await browser.close(); await server.close()
