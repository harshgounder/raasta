// live layer of the /how mill: moving parts, the grain, and the replay of a recorded scan.
// the static art comes from how-mill.gen.js (built by app/site/how/tools/build-mill.mjs); this file only writes
// attributes on refs, never re-renders the drawing.
import { iso, lineOnTop, segment, pathOf, translateAlong, towardViewer } from '../../how/tools/kit/iso-kit.mjs'
import { P, ANCH, LIVE, PANS, DRAWERS, HATCH_FRAMES, DRAWER_FRAMES } from './how-mill.gen.js'
import { EVENT_STAGE } from './how-data.js'

const TAU = Math.PI * 2
const still = matchMedia('(prefers-reduced-motion: reduce)')
const ease = (t) => (t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3))
const lerp3 = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]
const VERDICT_DROP = { B: 3.4, C: 2.2, W: 1.1, N: 0 }

export function mountMill(svg, { onStage, onReadout, onCounts }) {
  const q = (s) => svg.querySelector(s)
  const live = (n) => q(`[data-live="${n}"]`)
  const grain = q('.mill-grain-g')
  const layers = { chaff: q('[data-layer="chaff"]'), drop: q('[data-layer="drop"]'), grain: q('[data-layer="grain"]') }
  const door = [...q('[data-door]').children]
  const pile = [...svg.querySelectorAll('.mill-pile')]
  const ink = q('.mill-ink')
  const moves = Object.fromEntries([...svg.querySelectorAll('[data-move]')].map((el) => [el.dataset.move, el]))
  const pans = new Map([...svg.querySelectorAll('[data-pan]')].map((el) => [Number(el.dataset.pan), el]))
  const drawers = new Map([...svg.querySelectorAll('[data-drawer]')].map((el) => [el.dataset.drawer, [...el.children]]))
  const [tvx, tvy] = towardViewer(P)

  // ---- part poses (state), eased toward targets every frame ----
  const S = { clock: 0, aA: 0, aB: 0, wA: 0, wB: 0, gap: 0, wGap: 0, gear: 0, wGear: 0, gauge: -0.9, gaugeT: -0.9, dial: 0, dialT: 0, door: 0, doorT: 0, pile: 0,
    drawer: null, drawerOpen: 0, drawerT: 0, shake: 0, spoon: 0, spoonT: 0, bell: 0, letter: 0, letterT: 0, pans: new Map(), pansT: new Map() }

  const stoneTop = (c, r0, r1, z, a, n) => {
    let d = ''
    for (let i = 0; i < n; i++) {
      const t = a + (i / n) * TAU
      // harp furrows: slightly skewed off-radial, as on a real millstone
      d += lineOnTop([c[0] + Math.sin(t) * r0, c[1] - Math.cos(t) * r0], [c[0] + Math.sin(t + 0.32) * r1, c[1] - Math.cos(t + 0.32) * r1], z, P)
    }
    return d
  }
  const stoneSide = (c, r, z0, z1, a, n) => {
    let d = ''
    for (let i = 0; i < n; i++) {
      const t = a + (i / n) * TAU
      const nx = Math.cos(t), ny = Math.sin(t)
      if (nx * tvx + ny * tvy < 0.22) continue
      d += segment([c[0] + nx * r, c[1] + ny * r, z0], [c[0] + nx * r, c[1] + ny * r, z1], P)
    }
    return d
  }
  const needle = (c, z, r, turn) => lineOnTop([c[0] - Math.sin(turn) * 2, c[1] + Math.cos(turn) * 2], [c[0] + Math.sin(turn) * r, c[1] - Math.cos(turn) * r], z, P)
  const spokesY = (c, r, a) => [0, 1, 2].map((i) => { const t = a + (i / 3) * TAU; return pathOf([iso([c[0], c[1], c[2]], P), iso([c[0] + Math.cos(t) * r, c[1], c[2] + Math.sin(t) * r], P)]) }).join('')
  const spokesX = (c, r, a) => [0, 1, 2, 3].map((i) => { const t = a + (i / 4) * TAU; return pathOf([iso([c[0], c[1] + Math.cos(t) * 2.6, c[2] + Math.sin(t) * 2.6], P), iso([c[0], c[1] + Math.cos(t) * r, c[2] + Math.sin(t) * r], P)]) }).join('')
  // wall clock: 12 major ticks = 12 s per turn, the hand shows recorded server seconds
  const clockHand = (sec) => { const t = (sec / 12) * TAU, c = LIVE.clock.c; return pathOf([iso([c[0] - Math.sin(t) * 1.8, c[1], c[2] - Math.cos(t) * 1.8], P), iso([c[0] + Math.sin(t) * LIVE.clock.r, c[1], c[2] + Math.cos(t) * LIVE.clock.r], P)]) }
  const setFrame = (list, f) => list.forEach((g, i) => { const on = i === f; if ((g.style.display === 'none') === on) g.style.display = on ? '' : 'none' })

  const memo = new WeakMap()
  const setA = (el, name, v) => { let m = memo.get(el); if (!m) memo.set(el, (m = {})); if (m[name] !== v) { m[name] = v; el.setAttribute(name, v) } }
  const liveEls = {}
  const L = (n) => liveEls[n] ?? (liveEls[n] = live(n))
  const r2 = (v) => Math.round(v * 100) / 100
  function draw() {
    setA(L('stoneA-top'), 'd', stoneTop(LIVE.stoneA.c, 9, 33, 90, S.aA, 12))
    setA(L('stoneA-side'), 'd', stoneSide(LIVE.stoneA.c, 37, 76, 90, S.aA, 30))
    setA(L('stoneB'), 'd', stoneSide(LIVE.stoneB.c, 37, 61, 74.5, S.aB, 30))
    setA(L('gauge'), 'd', needle(LIVE.gauge.c, LIVE.gauge.z, LIVE.gauge.r, S.gauge))
    setA(L('dial'), 'd', needle(LIVE.dial.c, LIVE.dial.z, LIVE.dial.r, S.dial))
    setA(L('gapwheel'), 'd', spokesY(LIVE.gapwheel.c, LIVE.gapwheel.r - 1.4, S.gap))
    setA(L('gear-big'), 'd', spokesX(LIVE.gearBig.c, LIVE.gearBig.r - 2, S.gear))
    setA(L('gear-small'), 'd', spokesX(LIVE.gearSmall.c, LIVE.gearSmall.r - 1.6, -S.gear * (13 / 8)))
    setA(L('clock'), 'd', clockHand(S.clock))
    setA(L('pulley'), 'd', spokesY(LIVE.pulley.c, LIVE.pulley.r - 1.5, S.aB * 1.8))
    setFrame(door, Math.round(S.door * HATCH_FRAMES))
    pile.forEach((c, i) => { const on = i < S.pile; if ((c.style.display === 'none') === on) c.style.display = on ? '' : 'none' })
    for (const [cat, frames] of drawers) setFrame(frames, cat === S.drawer ? Math.round(S.drawerOpen * DRAWER_FRAMES) : 0)
    setA(moves.sieve, 'transform', translateAlong(P, [S.shake > 0 ? r2(Math.sin(S.shake * 40) * 0.9) : 0, 0, 0]))
    setA(moves.spoon, 'transform', translateAlong(P, [0, 0, -r2(S.spoon * 3)]))
    setA(moves.bell, 'transform', `rotate(${r2(Math.sin(S.bell * 30) * 6 * Math.max(0, 1 - S.bell))} ${iso([28, 24, 84], P).join(' ')})`)
    setA(moves.letter, 'transform', translateAlong(P, [0, 0, r2(S.letter * 10)]))
    for (const [i, el] of pans) setA(el, 'transform', translateAlong(P, [0, 0, -r2(S.pans.get(i) ?? 0)]))
  }

  // ---- grain and bits ----
  let gpos = ANCH.sky, gvis = false
  const placeGrain = () => {
    const [x, y] = iso(gpos, P)
    grain.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)})`)
    grain.style.opacity = gvis ? '1' : '0'
  }
  // arc between two world points with an apex lift
  const arc = (a, b, t, lift = 18) => { const p = lerp3(a, b, t); p[2] += Math.sin(Math.PI * t) * lift; return p }
  const bits = []
  function spawnBits(n, kind, from, to, layer, delay = 0) {
    for (let i = 0; i < n; i++) {
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
      c.setAttribute('class', 'mill-bit'); c.dataset.k = kind; c.setAttribute('r', kind === 'reject' ? '1.3' : '1.7')
      layer.append(c)
      const jitter = [(Math.random() - 0.5) * 30, (Math.random() - 0.5) * 18, 0]
      bits.push({ el: c, a: [from[0] + jitter[0], from[1] + jitter[1] * 0.6, from[2]], b: [to[0] + jitter[0] * 0.4, to[1] + jitter[1] * 0.3, to[2]], t0: delay + i * 0.045, dur: 0.75 })
    }
  }
  function clearBits() { bits.splice(0).forEach((b) => b.el.remove()) }

  // ---- timeline from a recorded run ----
  let plan = null, clock = 0, playing = false, frame = 0, last = 0, cursor = 0
  const counts = { ACCEPT: 0, ABSTAIN: 0, REJECT: 0, hatch: 0 }

  function build(run) {
    const ev = run.events.filter((e) => e.stage !== 'end')
    const segs = []
    let prev = 0
    for (const e of ev) {
      const real = Math.max(0, e.t - prev)
      segs.push({ stage: e.stage, n: EVENT_STAGE[e.stage], t0: prev, t1: e.t, real, show: Math.max(real, e.stage === 'queued' || e.stage === 'start' ? 0.5 : 0.95) })
      prev = e.t
    }
    // outside the scan: route cost, route, report (no timing exists for them in the recording)
    segs.push({ stage: 'route', n: 14, outside: true, real: 0, show: 1.4 }, { stage: 'tray', n: 15, outside: true, real: 0, show: 1.2 }, { stage: 'report', n: 17, outside: true, real: 0, show: 1.6 })
    let acc = 0
    for (const s of segs) { s.a = acc; acc += s.show; s.b = acc }
    const accept = run.impact.rows.find((r) => r.status === 'ACCEPT') ?? run.impact.rows[0] ?? null
    return { run, segs, total: acc, accept }
  }

  const fmt = (v) => (v == null ? '' : `${v.toFixed(2)} s`)
  function enter(seg) {
    const r = plan.run
    onStage?.(seg.n, seg)
    const sayAt = seg.outside ? 'outside the scan, no timing' : `t ${seg.t1.toFixed(2)} s`
    let say = ''
    switch (seg.stage) {
      case 'queued': say = `photo in: ${r.size[0]} x ${r.size[1]} px, queued, 0 ahead`; break
      case 'start': say = 'worker picks up the job'; break
      case 'intake': say = `condition: ${r.condition}`; S.gaugeT = r.light === 'night' ? 0.9 : r.light === 'dusk' ? 0 : -0.9; break
      case 'detector_a': say = `detector A: ${r.detA.n} boxes from ${r.detA.prompts} prompts`; break
      case 'detector_b': say = `detector B: ${r.detB.n} boxes`; break
      case 'agreement': {
        say = `agreement: ${r.agree.ACCEPT} ACCEPT, ${r.agree.ABSTAIN} ABSTAIN, ${r.agree.REJECT} REJECT`
        spawnBits(Math.min(r.agree.REJECT, 36), 'reject', ANCH.sieveBack, ANCH.chaffMouth, layers.chaff, 0.25)
        spawnBits(Math.min(r.agree.ABSTAIN, 14), 'abstain', ANCH.sieveFront, ANCH.hatchMouth, layers.drop, 0.35)
        if (r.agree.ABSTAIN) S.doorT = 1
        break
      }
      case 'vlm_start': say = `vision check asked about ${r.vlm.sent} boxes`; S.spoonT = 1; break
      case 'footpath_mask': {
        const net = r.final.ABSTAIN - r.agree.ABSTAIN
        const moved = r.policy.filter((p) => /carriageway|calibrated|ground/.test(p.why)).length
        say = moved ? `ground check changed ${moved} decision${moved > 1 ? 's' : ''}: ${r.final.ACCEPT} ACCEPT, ${r.final.ABSTAIN} ABSTAIN` : `ground check: no change (${r.final.ACCEPT} ACCEPT)`
        if (net > 0) { spawnBits(net, 'abstain', ANCH.sieveFront, ANCH.hatchMouth, layers.drop, 0.3); S.doorT = 1 }
        break
      }
      case 'depth': say = `depth: near ${r.depth.near_m} m, far ${r.depth.far_m} m`; S.dialT = 0.5; break
      case 'measure': {
        const h = r.heights
        say = h.length ? `${h.length} height${h.length > 1 ? 's' : ''} tried: ${h.map((x) => x.status).join(', ')}` : 'no kerb or step in view: nothing to measure'
        S.dialT = 0
        if (h.some((x) => x.status !== 'OK' && x.cm == null)) S.doorT = 1
        break
      }
      case 'vlm': say = r.vlm.ok ? 'vision check answered' : 'vision check unavailable: HTTP 401, key refused'; S.spoonT = 0; break
      case 'impact': {
        const a = plan.accept
        say = a ? `${a.name}: block ${a.all.block}, cost ${a.all.slow}, warn ${a.all.warn}, none ${a.all.none} of 74 bodies (${r.impact.context})` : 'no element to weigh'
        if (a) { S.drawer = a.category; S.drawerT = 1 }
        break
      }
      case 'reasoner_start': say = 'reasoner asked'; S.bell = 0.001; break
      case 'reasoner': say = r.reasoner.ok ? 'reasoner answered (advisory)' : 'reasoner unavailable: HTTP 401 (advisory only)'; break
      case 'placement': say = `placement ${r.placement.status}: ${r.placement.why ?? ''}`; if (r.placement.status !== 'placed') S.doorT = 1; break
      case 'receipt': say = `receipt ${r.receipt.id} written`; ink?.classList.add('on'); break
      case 'route': say = 'route cost: the chute prices the element per body'; S.drawerT = 0; break
      case 'tray': say = 'route: lands in the tray with its date tag'; break
      case 'report': say = 'report loop: a person confirms, the letter goes out'; S.letterT = 1; break
    }
    onReadout?.({ seg, say, at: sayAt, total: plan.total })
  }
  function exit(seg) {
    const r = plan.run
    if (seg.stage === 'agreement') Object.assign(counts, { ACCEPT: r.agree.ACCEPT, ABSTAIN: r.agree.ABSTAIN, REJECT: r.agree.REJECT })
    if (seg.stage === 'footpath_mask') Object.assign(counts, { ACCEPT: r.final.ACCEPT, ABSTAIN: r.final.ABSTAIN, REJECT: r.final.REJECT })
    counts.hatch = counts.ABSTAIN + (['placement', 'receipt'].includes(seg.stage) || seg.outside ? 0 : 0)
    S.pile = Math.min(14, counts.ABSTAIN)
    onCounts?.({ ...counts })
    if (['agreement', 'footpath_mask', 'measure', 'placement'].includes(seg.stage)) setTimeout(() => { S.doorT = 0 }, 650)
  }

  // where the grain is during a segment (u in 0..1)
  function grainAt(seg, u) {
    const r = plan.run
    const cat = plan.accept?.category
    const drawer = DRAWERS.find((d) => d.cat === cat)
    switch (seg.stage) {
      case 'queued': case 'start': return [arc(ANCH.sky, ANCH.mouth, ease(u), 0), true]
      case 'intake': return [lerp3(ANCH.mouth, ANCH.gate, ease(u)), u < 0.5]
      case 'detector_a': return u < 0.5 ? [lerp3(ANCH.gate, ANCH.duct, ease(u * 2)), u > 0.15] : [lerp3(ANCH.duct, ANCH.eye, ease(u * 2 - 1)), u < 0.9]
      case 'detector_b': return [ANCH.gap, false]
      case 'agreement': return [lerp3(ANCH.spoutTop, ANCH.sieve, ease(u)), r.final.ACCEPT > 0 || r.agree.ACCEPT > 0]
      case 'vlm_start': case 'footpath_mask': case 'depth': case 'measure': case 'vlm': return [ANCH.sieve, r.final.ACCEPT > 0]
      case 'impact': {
        if (!drawer) return [arc(ANCH.sieve, ANCH.scales, ease(u)), r.final.ACCEPT > 0]
        return u < 0.5 ? [arc(ANCH.sieve, drawer.front, ease(u * 2), 30), true] : [arc(drawer.front, ANCH.scales, ease(u * 2 - 1), 10), true]
      }
      case 'reasoner_start': case 'reasoner': return [ANCH.scales, r.final.ACCEPT > 0]
      case 'placement': case 'receipt': return [u < 1 && seg.stage === 'placement' ? arc(ANCH.scales, ANCH.pin, ease(u), 14) : ANCH.pin, r.final.ACCEPT > 0]
      case 'route': return [lerp3(ANCH.pin, ANCH.tray, ease(u)), r.final.ACCEPT > 0]
      case 'tray': case 'report': return [ANCH.tray, r.final.ACCEPT > 0]
    }
    return [gpos, gvis]
  }

  function step(dt) {
    const calm = still.matches
    const k = (tc) => (calm ? 1 : 1 - Math.exp(-dt / tc))
    // replay
    if (playing && plan) {
      clock += dt
      while (cursor < plan.segs.length && clock >= plan.segs[cursor].b) { exit(plan.segs[cursor]); cursor++; if (cursor < plan.segs.length) enter(plan.segs[cursor]) }
      if (cursor >= plan.segs.length) { playing = false; onReadout?.({ done: true, total: plan.total }) }
      else {
        const seg = plan.segs[cursor]
        const u = (clock - seg.a) / seg.show
        ;[gpos, gvis] = grainAt(seg, u)
        // work in progress on the part that does it
        const busy = seg.stage
        S.wA = busy === 'detector_a' ? 7 : 0
        S.wB = busy === 'detector_b' ? -7 : 0
        S.wGap = busy === 'footpath_mask' ? 3 : 0
        S.wGear = busy === 'impact' ? 2.4 : 0
        S.shake = busy === 'agreement' ? S.shake + dt : 0
        if (busy === 'reasoner_start' || busy === 'reasoner') S.bell = Math.min(1, S.bell + dt / 0.9)
        if (busy === 'impact' && u > 0.55 && plan.accept?.v74 && !S.pansT.size) plan.accept.v74.split('').forEach((v, i) => { S.pansT.set(i, VERDICT_DROP[v] ?? 0); pans.get(i)?.setAttribute('data-v', v) })
        if (busy === 'impact' && u > 0.6) S.drawerT = 0
        const t = seg.outside ? null : seg.t0 + Math.min(1, u) * seg.real
        if (t != null) S.clock = t
        onReadout?.({ tick: true, t })
      }
    }
    // ease poses
    S.aA += S.wA * dt; S.aB += S.wB * dt; S.gap += S.wGap * dt; S.gear += S.wGear * dt
    S.gauge += (S.gaugeT - S.gauge) * k(0.35)
    const dialWant = S.dialT ? S.dialT + Math.sin(clock * 9) * 0.25 : 0
    S.dial += (dialWant - S.dial) * k(0.25)
    S.door += (S.doorT - S.door) * k(0.18)
    S.drawerOpen += (S.drawerT - S.drawerOpen) * k(0.2)
    S.spoon += (S.spoonT * 0.35 - S.spoon) * k(0.3)
    S.letter += (S.letterT - S.letter) * k(0.4)
    for (const [i, v] of S.pansT) S.pans.set(i, (S.pans.get(i) ?? 0) + (v - (S.pans.get(i) ?? 0)) * k(0.3))
    // bits
    for (let i = bits.length - 1; i >= 0; i--) {
      const b = bits[i]
      b.t0 -= dt
      const u = -b.t0 / b.dur
      if (u < 0) { b.el.style.opacity = '0'; continue }
      if (u >= 1) { b.el.remove(); bits.splice(i, 1); continue }
      const p = lerp3(b.a, b.b, u); p[2] += Math.sin(Math.PI * u) * 8 - u * u * 2
      const [x, y] = iso(p, P)
      b.el.setAttribute('cx', x.toFixed(1)); b.el.setAttribute('cy', y.toFixed(1)); b.el.style.opacity = String(Math.min(1, (1 - u) * 4))
    }
    placeGrain()
    draw()
  }
  const busy = () => playing || bits.length || Math.abs(S.door - S.doorT) > 0.002 || Math.abs(S.drawerOpen - S.drawerT) > 0.002 || Math.abs(S.gauge - S.gaugeT) > 0.002 || Math.abs(S.dial) > 0.002 || Math.abs(S.letter - S.letterT) > 0.002 || [...S.pansT].some(([i, v]) => Math.abs((S.pans.get(i) ?? 0) - v) > 0.01)
  let visible = true
  function tick(now) {
    const dt = last ? Math.min((now - last) / 1000, 0.1) : 1 / 60
    last = now
    step(dt)
    frame = visible && busy() ? requestAnimationFrame(tick) : 0
    if (!frame) last = 0
  }
  const kick = () => { if (!frame && visible) frame = requestAnimationFrame(tick) }
  new IntersectionObserver((e) => { visible = e[e.length - 1].isIntersecting; if (visible) kick() }, { rootMargin: '80px 0px' }).observe(svg)

  function reset() {
    clearBits()
    Object.assign(S, { clock: 0, wA: 0, wB: 0, wGap: 0, wGear: 0, gaugeT: -0.9, dialT: 0, doorT: 0, pile: 0, drawer: null, drawerT: 0, shake: 0, spoonT: 0, bell: 0, letterT: 0 })
    S.pansT.clear(); S.pans.clear(); pans.forEach((el) => el.removeAttribute('data-v'))
    Object.assign(counts, { ACCEPT: 0, ABSTAIN: 0, REJECT: 0, hatch: 0 })
    ink?.classList.remove('on')
    gpos = ANCH.sky; gvis = false
  }
  function play(run) {
    reset()
    plan = build(run); clock = 0; cursor = 0
    if (still.matches) {
      // reduced motion: jump to the end state, one still frame
      for (const s of plan.segs) { enter(s); exit(s) }
      ;[gpos, gvis] = grainAt(plan.segs[plan.segs.length - 1], 1)
      if (plan.accept?.v74) plan.accept.v74.split('').forEach((v, i) => { S.pansT.set(i, VERDICT_DROP[v] ?? 0); S.pans.set(i, VERDICT_DROP[v] ?? 0); pans.get(i)?.setAttribute('data-v', v) })
      S.doorT = 0; S.door = 0; S.drawerT = 0; S.drawerOpen = 0; S.letter = S.letterT
      clearBits(); step(0)
      onReadout?.({ done: true, total: plan.total })
      return
    }
    playing = true
    enter(plan.segs[0])
    kick()
  }
  function stop() { playing = false; reset(); step(0) }
  // idle: stones turn slowly so the mill reads as a machine
  step(0)
  return { play, stop, get playing() { return playing }, kick }
}
