// quick static preview of the generated mill (no Vite): writes a standalone html to the scratch dir given as argv[2]
// and screenshots it with headless Brave. node app/site/how/tools/preview.mjs OUT_DIR [zoomX zoomY zoomW]
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import puppeteer from 'puppeteer-core'
const HERE = dirname(fileURLToPath(import.meta.url))
const out = process.argv[2]
mkdirSync(out, { recursive: true })
const { SVG } = await import(join(HERE, '../../src/pages/how-mill.gen.js'))
const css = readFileSync(join(HERE, 'kit/iso.css'), 'utf8') + readFileSync(join(HERE, '../../src/pages/how-mill.css'), 'utf8')
const html = `<!doctype html><meta charset="utf-8"><style>${css} body{margin:0;background:#f3f3f3}</style><div class="iso mill-plate" data-theme="light" style="padding:10px;background:#f3f3f3">${SVG}</div>`
writeFileSync(join(out, 'preview.html'), html)
const b = await puppeteer.launch({ executablePath: '/usr/bin/brave', headless: true, args: ['--no-first-run'] })
const p = await b.newPage()
await p.setViewport({ width: 1600, height: 1060, deviceScaleFactor: 1 })
await p.goto('file://' + join(out, 'preview.html'))
await p.screenshot({ path: join(out, 'mill.png') })
const [zx, zy, zw] = process.argv.slice(3).map(Number)
if (zw) {
  await p.setViewport({ width: 1600, height: 1060, deviceScaleFactor: 3 })
  await p.screenshot({ path: join(out, 'zoom.png'), clip: { x: zx, y: zy, width: zw, height: zw * 0.66 } })
}
await b.close()
console.log('ok', out)
