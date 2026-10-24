import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'
const root = '/home/liebert511/hypnexis-main/app/site/'
const server = await createServer({ root, logLevel: 'error', server: { port: 0 } }); await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--use-angle=gl-egl', '--ignore-gpu-blocklist', '--disable-vulkan-surface'] })
const page = await browser.newPage(); await page.setViewport({ width: 1440, height: 900 })
const errs = []; page.on('pageerror', (e) => errs.push(e.message))
await page.goto(base + '/', { waitUntil: 'networkidle0' })
await page.waitForFunction(() => window.__story?.ready(), { timeout: 20000 })
await page.evaluate(() => { window.__dts = []; let l = performance.now(); const f = (n) => { __dts.push(n - l); l = n; if (__dts.length < 2000) requestAnimationFrame(f) }; requestAnimationFrame(f) })
await page.mouse.move(700, 450)
for (let i = 0; i < 300; i++) { await page.mouse.wheel({ deltaY: 90 }); await new Promise((r) => setTimeout(r, 16)) }
const r = await page.evaluate(() => { const d = __dts.slice(5).sort((a, b) => a - b); return { n: d.length, med: d[d.length >> 1], p95: d[Math.floor(d.length * 0.95)], max: d.at(-1), y: scrollY, shown: __story.shown, gl: (() => { const g = document.querySelector('.story-gl').getContext('webgl2'); const e = g.getExtension('WEBGL_debug_renderer_info'); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : '?' })() } })
console.log(JSON.stringify({ ...r, errs }))
await browser.close(); await server.close()
