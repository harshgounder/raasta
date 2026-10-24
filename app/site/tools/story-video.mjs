// story v2 real-time scroll recording (lerp ON, like a viewer): wheel-scrolls the whole story and records a webm
// via puppeteer's screencast (needs ffmpeg). usage: node tools/story-video.mjs [--mobile] [--speed 900]
import { parseArgs } from 'node:util'
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'
const { values: a } = parseArgs({ options: { mobile: { type: 'boolean', default: false }, speed: { type: 'string', default: '900' } } })
const root = new URL('..', import.meta.url).pathname
const server = await createServer({ root, logLevel: 'error', server: { port: 0 } }); await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run', '--hide-scrollbars', '--use-angle=gl-egl', '--ignore-gpu-blocklist', '--disable-vulkan-surface'] })
const page = await browser.newPage()
await page.setViewport(a.mobile ? { width: 390, height: 844 } : { width: 1280, height: 800 })
await page.goto(base + '/', { waitUntil: 'load' }); await page.waitForFunction(() => window.__story?.ready(), { timeout: 20000 })
await new Promise((r) => setTimeout(r, 800))
const out = `${root}shots/v2/scroll-${a.mobile ? 'mobile' : 'desk'}.webm`
const rec = await page.screencast({ path: out })
const total = await page.evaluate(() => __story.total + innerHeight)
const pxPerTick = Number(a.speed) / 30
await page.mouse.move(300, 300)
for (let y = 0; y < total; y += pxPerTick) { await page.mouse.wheel({ deltaY: pxPerTick }); await new Promise((r) => setTimeout(r, 33)) }
await new Promise((r) => setTimeout(r, 1500))
await rec.stop()
console.log(out)
await browser.close(); await server.close()
