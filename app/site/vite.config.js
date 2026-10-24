import { defineConfig } from 'vite'
import { readdirSync, existsSync, statSync, readFileSync, createReadStream, cpSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, resolve, extname } from 'node:path'

// city data lives OUTSIDE the site (another lane writes it): ~/hypnexis-main/app/site-data/<city>/{network.geojson,routes.json,...}
// dev: served at /site-data/*, plus a generated /site-data/index.json (the list of cities)
// build: copied into dist/site-data/ with the same index, so the static site works offline
const DATA = resolve(import.meta.dirname, '../site-data')
const types = { '.json': 'application/json', '.geojson': 'application/geo+json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml' }

function cityIndex() {
  if (!existsSync(DATA)) return { cities: [] }
  const cities = readdirSync(DATA).filter((d) => statSync(join(DATA, d)).isDirectory() && existsSync(join(DATA, d, 'network.geojson')))
    .map((id) => {
      let meta = {}
      for (const f of ['city.json', 'meta.json']) try { meta = { ...JSON.parse(readFileSync(join(DATA, id, f), 'utf8')), ...meta } } catch {}
      const files = readdirSync(join(DATA, id)).filter((f) => /\.(json|geojson)$/.test(f))
      // per-body routes (app/route/precompute_bodies.py): trip ids that have a routes-bodies/<trip>.json, so the map never asks for a missing file
      const rb = join(DATA, id, 'routes-bodies')
      const bodies = existsSync(rb) ? readdirSync(rb).filter((f) => f.endsWith('.json')).map((f) => f.slice(0, -5)) : []
      return { id, name: meta.name ?? meta.area ?? id, mock: meta.mock ?? id.startsWith('mock'), records: meta.evidence_records ?? null, files, bodies }
    })
    // real data first, mocks last
    // real data first (most evidence first), mocks last
    .sort((a, b) => Number(a.mock) - Number(b.mock) || (b.records ?? 0) - (a.records ?? 0) || a.id.localeCompare(b.id))
  return { cities }
}

function siteData() {
  return {
    name: 'site-data',
    configureServer(server) {
      server.middlewares.use('/site-data', (req, res, next) => {
        const path = decodeURIComponent(req.url.split('?')[0])
        if (path === '/index.json') { res.setHeader('content-type', 'application/json'); res.end(JSON.stringify(cityIndex())); return }
        const file = resolve(DATA, '.' + path)
        if (!file.startsWith(DATA) || !existsSync(file) || !statSync(file).isFile()) { res.statusCode = 404; res.end('not found'); return }
        res.setHeader('content-type', types[extname(file)] ?? 'application/octet-stream')
        res.setHeader('cache-control', 'no-store')
        createReadStream(file).pipe(res)
      })
    },
    closeBundle() {
      const out = resolve(import.meta.dirname, 'dist/site-data')
      if (existsSync(DATA)) cpSync(DATA, out, { recursive: true })
      else mkdirSync(out, { recursive: true })
      writeFileSync(join(out, 'index.json'), JSON.stringify(cityIndex()))
    },
  }
}

// multi-page: every page is a real index.html in its own folder, so it opens directly on a static host (Vercel)
const here = (p) => resolve(import.meta.dirname, p)
const input = Object.fromEntries(['', 'map', 'scan', 'city', 'how', 'what-if', 'report', 'data'].map((d) => [d || 'story', here(d ? `${d}/index.html` : 'index.html')]))

export default defineConfig({
  base: '/',
  appType: 'mpa',
  plugins: [siteData()],
  build: { target: 'es2022', chunkSizeWarningLimit: 2500, rollupOptions: { input } },
  server: { host: true },
})
