import * as THREE from 'three'
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js'

// PLACEHOLDER street, built in code so the same street can be seen from any eye height (switch body).
// metres; x runs along the street, the footpath is z in [-W, 0], the road is z > 0 (the env plate draws the road
// surface and sky, see look/panel.js), the footpath top sits at y = KERB.
// every barrier is its own group with userData { barrier: type, label } so a tap (raycast) can name it.
// art arrives later as scene images (story.json scene_image); this stays as the fallback and as the 3D for body switching.

export const KERB = 0.2          // footpath height above the road (m); Indian kerbs are often higher, PLACEHOLDER value
export const W = 2.4             // footpath width (m)

export function createStreet(hatch) {
  const group = new THREE.Group()
  const barriers = []
  const fills = { mid: hatch.fillFor({ midKey: 'mid' }), accent: hatch.fillFor({ midKey: 'accent' }) }

  // one box with an outline hull (smooth normals on the hull so corners do not split open)
  function box(parent, [sx, sy, sz], [x, y, z], { mat = 'mid', rotY = 0 } = {}) {
    const geo = new THREE.BoxGeometry(sx, sy, sz)
    const mesh = new THREE.Mesh(geo, fills[mat])
    mesh.position.set(x, y, z); mesh.rotation.y = rotY
    const hullGeo = mergeVertices(geo.clone().deleteAttribute('normal').deleteAttribute('uv')); hullGeo.computeVertexNormals()
    const hull = new THREE.Mesh(hullGeo, hatch.outline); hatch.bindOutline(hull)
    mesh.add(hull)
    parent.add(mesh)
    return mesh
  }
  function cyl(parent, r, h, [x, y, z], { mat = 'mid', seg = 14 } = {}) {
    const geo = new THREE.CylinderGeometry(r, r, h, seg)
    const mesh = new THREE.Mesh(geo, fills[mat]); mesh.position.set(x, y + h / 2, z)
    const hullGeo = mergeVertices(geo.clone().deleteAttribute('normal').deleteAttribute('uv')); hullGeo.computeVertexNormals()
    const hull = new THREE.Mesh(hullGeo, hatch.outline); hatch.bindOutline(hull); mesh.add(hull)
    parent.add(mesh); return mesh
  }

  // the base street: footpath slabs (with joints), the wall of shops behind it, buildings across the road
  const base = new THREE.Group(); group.add(base)
  for (let x = -12; x < 40; x += 2) box(base, [1.96, KERB, W], [x + 1, KERB / 2, -W / 2])
  for (let x = -12; x < 40; x += 4.5) {
    const h = 3.2 + ((x * 7) % 3 + 3) % 3 * 0.6
    box(base, [4.4, h, 0.4], [x + 2.2, KERB + h / 2, -W - 0.2])
    box(base, [3.0, 2.2, 0.06], [x + 2.2, KERB + 1.1, -W + 0.03])               // shutter
    box(base, [4.6, 0.12, 0.7], [x + 2.2, KERB + 2.5, -W + 0.15])                // awning
  }
  for (let x = -12; x < 40; x += 6) { const h = 5 + ((x * 13) % 5 + 5) % 5; box(base, [5.6, h, 4], [x + 3, h / 2, 13]) }

  // barriers by type (the five SC-02 classes); each returns its group
  const builders = {
    pole(x) {                                             // a pole in the middle of the footpath
      const g = new THREE.Group(); cyl(g, 0.11, 6.5, [x, KERB, -W / 2], { mat: 'accent' })
      box(g, [0.5, 0.7, 0.05], [x, KERB + 2.3, -W / 2 + 0.12], { mat: 'accent' }); return g
    },
    parked(x) {                                           // a parked car with two wheels up on the footpath
      const g = new THREE.Group()
      box(g, [3.9, 0.9, 1.7], [x, KERB + 0.55, -0.55], { mat: 'accent' })
      box(g, [2.1, 0.6, 1.5], [x - 0.2, KERB + 1.3, -0.55], { mat: 'accent' })
      for (const dx of [-1.3, 1.3]) for (const dz of [-1.25, 0.15]) cyl(g, 0.3, 0.22, [x + dx, KERB + 0.3, -0.55 + dz])
      return g
    },
    steps(x) {                                            // a shop's steps taking the footpath's width
      const g = new THREE.Group()
      for (let i = 0; i < 3; i++) box(g, [2.4, 0.17 * (i + 1), 1.8 - i * 0.5], [x, KERB + 0.085 * (i + 1), -W + (1.8 - i * 0.5) / 2], { mat: 'accent' })
      return g
    },
    broken(x) {                                           // broken footpath: missing slabs, a tilted one, rubble
      const g = new THREE.Group()
      box(g, [1.9, KERB * 0.6, 1.1], [x - 0.6, KERB * 0.2, -0.9], { mat: 'accent', rotY: 0.18 })
      for (let i = 0; i < 7; i++) box(g, [0.25 + (i % 3) * 0.1, 0.12, 0.2 + (i % 2) * 0.1], [x + 0.5 + (i % 4) * 0.35, 0.06, -1.6 + (i % 3) * 0.4], { mat: 'accent', rotY: i })
      return g
    },
    'no-ramp'(x) {                                        // the footpath ends at a side street with a kerb drop and no ramp
      const g = new THREE.Group(); box(g, [0.25, KERB, W], [x, KERB / 2, -W / 2], { mat: 'accent' }); return g
    },
    ramp(x) {                                             // a kerb ramp: a slab sloping from the road up to the footpath edge
      const g = new THREE.Group(), run = 1.0, th = Math.atan2(KERB, run)
      const m = box(g, [1.4, 0.05, Math.hypot(run, KERB)], [x, KERB / 2, run / 2])
      m.rotation.x = th; return g
    },
    cart(x) {                                             // a vendor cart parked on the footpath (5 pm)
      const g = new THREE.Group()
      box(g, [1.7, 0.75, 0.95], [x, KERB + 0.8, -0.75], { mat: 'accent' })
      box(g, [1.9, 0.06, 1.15], [x, KERB + 1.9, -0.75], { mat: 'accent' })
      for (const dx of [-0.8, 0.8]) cyl(g, 0.03, 1.5, [x + dx, KERB + 0.4, -0.3])
      for (const dx of [-0.55, 0.55]) cyl(g, 0.22, 0.12, [x + dx, KERB + 0.2, -0.2])
      return g
    },
    // route line (the one red object of the map beat): flat, no outline, drawn on the footpath top
    route(x, f) {
      const g = new THREE.Group(), len = Math.max(0.5, (f.to ?? x + 10) - x)
      const m = new THREE.Mesh(new THREE.BoxGeometry(len, 0.02, f.w ?? 0.28), new THREE.MeshBasicMaterial({ color: f.color ?? '#c82924' }))
      m.position.set(x + len / 2, KERB + 0.015, f.z ?? -1.2); m.userData.keep = true; g.add(m); return g
    },
    // a stretch nobody has seen yet: ink dashes, never red, never "safe"
    unknown(x, f) {
      const g = new THREE.Group(), to = f.to ?? x + 6, mat = new THREE.MeshBasicMaterial({ color: f.color ?? '#111111' })
      for (let s = x; s < to; s += 0.7) {
        const m = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.02, 0.1), mat)
        m.position.set(s + 0.175, KERB + 0.015, f.z ?? -1.2); m.userData.keep = true; g.add(m)
      }
      return g
    },
  }
  const labels = { pole: 'pole in the path', parked: 'scooter on the footpath', steps: 'steps, no ramp', broken: 'broken footpath', 'no-ramp': 'kerb drop, no ramp',
    ramp: 'kerb ramp', cart: 'cart on the footpath', route: 'route', unknown: 'not seen yet: unknown' }

  // features: [{ type, x }] from story.json scene.street; the focus barrier gets the accent (selective colour).
  // each distinct feature list is built once and cached; set() only toggles visibility (it runs per beat per frame)
  const cache = new Map()
  let currentKey = null, current = null
  // per frame: a feature can show only after a beat progress (f.from), until one (f.until), or only for some bodies
  // (f.bodies); this is how carts arrive at 5 pm and how each body's route line is drawn on the map beat
  function gate({ progress = 0, body = null } = {}) {
    for (const g of current?.barriers ?? []) {
      const f = g.userData.f
      g.visible = progress >= (f.from ?? -1) && progress < (f.until ?? 2) && (!f.bodies || f.bodies.includes(body))
    }
  }
  function set(features = [], focus, state) {
    const key = JSON.stringify([features, focus ?? null])
    if (key === currentKey) { gate(state); return }
    currentKey = key
    for (const c of cache.values()) c.group.visible = false
    let c = cache.get(key)
    if (!c) {
      c = { group: new THREE.Group(), barriers: [] }
      for (const f of features) {
        const b = builders[f.type]; if (!b) { console.warn(`street: unknown barrier type ${f.type}`); continue }
        const g = b(f.x ?? 8, f)
        g.userData = { barrier: f.type, label: f.label ?? labels[f.type], note: f.note ?? null, f }
        g.traverse((o) => { if (o.isMesh && o.material !== hatch.outline && !o.userData.keep) o.material = f.type === focus || !focus ? fills.accent : fills.mid })
        c.group.add(g); c.barriers.push(g)
      }
      group.add(c.group); cache.set(key, c)
    }
    c.group.visible = true
    current = c; gate(state)
    barriers.length = 0; barriers.push(...c.barriers)
    // holes in the slab row for broken / no-ramp (hide the slabs that sit there)
    base.children.forEach((m) => { m.visible = true })
    for (const f of features) if (f.type === 'broken' || f.type === 'no-ramp') {
      const fx = f.x ?? 8, lo = f.type === 'broken' ? fx - 1.2 : fx + 0.1, hi = f.type === 'broken' ? fx + 1.6 : fx + 6
      base.children.forEach((m) => { if (Math.abs(m.position.y - KERB / 2) < 1e-3 && Math.abs(m.position.z + W / 2) < 1e-3 && m.position.x > lo && m.position.x < hi) m.visible = false })
    }
  }

  const ray = new THREE.Raycaster()
  function pick(ndc, camera) {
    ray.setFromCamera(ndc, camera)
    const hit = ray.intersectObjects(barriers.filter((g) => g.visible), true).find((h) => h.object.material !== hatch.outline)
    if (!hit) return null
    let g = hit.object; while (g && !g.userData.barrier) g = g.parent
    return g ? { type: g.userData.barrier, label: g.userData.label, note: g.userData.note, distance: hit.distance } : null
  }
  return { group, set, pick, get barriers() { return barriers } }
}
