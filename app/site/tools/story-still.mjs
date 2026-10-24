// story v2 reduced-motion check: emulates prefers-reduced-motion and saves a full-page shot of the still comic
import { createServer } from 'vite'
import puppeteer from 'puppeteer-core'
const root = new URL('..', import.meta.url).pathname
const server = await createServer({ root, logLevel: 'error', server: { port: 0 } }); await server.listen()
const base = server.resolvedUrls.local[0].replace(/\/$/, '')
const browser = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run'] })
const page = await browser.newPage(); await page.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true })
const errs = []; page.on('pageerror', (e) => errs.push(e.message))
await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }])
await page.goto(base + '/', { waitUntil: 'networkidle0' })
await page.screenshot({ path: root + 'shots/v2/still-mobile.jpg', type: 'jpeg', quality: 60, fullPage: true })
console.log(JSON.stringify({ errs, h: await page.evaluate(() => document.body.scrollHeight), gl: await page.evaluate(() => !!document.querySelector('.story-gl')) }))
await browser.close(); await server.close()
