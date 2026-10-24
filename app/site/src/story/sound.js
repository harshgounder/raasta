// story v2 sound: real recordings only (public/audio/v2/ + MANIFEST.json from the sound lane). No synth, ever.
// - nothing plays before a user gesture: the toggle button (or the first press after a remembered "on") unlocks it
// - loops (beds): gain = sum over beats of (share of screen that beat holds) x (beatGain[beat], else gain if the cue
//   lists that beat), smoothed; so beds crossfade with the panels
// - one-shots are fired by the story itself (cue(name)), tied to what is on screen: paw contacts, the horn, taps
// - MANIFEST v2 shape: { cues: [{ cue, beats, loop, gain, beatGain, roundRobin, variants: [{ stem, files: [ogg, m4a] }] }] }
//   (older flat shapes are still read). Re-checked every 8 s (then 30 s) until it exists.
const BASE = `${import.meta.env.BASE_URL}audio/v2/`
const KEY = 'raasta.sound'

export function createSound() {
  let ctx = null, master = null, cues = new Map(), on = false, loaded = false
  const store = { get() { try { return localStorage.getItem(KEY) } catch { return null } }, set(v) { try { localStorage.setItem(KEY, v) } catch {} } }
  // AAC (.m4a) first: every major browser decodes it (Safari never reliably decoded Ogg); Ogg is the fallback
  const aac = (() => { try { return document.createElement('audio').canPlayType('audio/mp4; codecs="mp4a.40.2"') !== '' } catch { return true } })()

  const btn = Object.assign(document.createElement('button'), { type: 'button', className: 'snd-btn box' })
  const label = () => {
    const live = on && ctx?.state === 'running'
    btn.textContent = live ? 'sound on' : 'sound off'
    btn.setAttribute('aria-pressed', String(live))
    btn.setAttribute('aria-label', live ? 'turn sound off' : 'turn sound on')
  }
  label()
  document.body.append(btn)

  const pickFiles = (files) => {
    const f = [files].flat().filter(Boolean)
    const a = f.filter((x) => /\.(m4a|mp4|aac)$/i.test(x)), o = f.filter((x) => /\.ogg$/i.test(x)), rest = f.filter((x) => !a.includes(x) && !o.includes(x))
    return aac ? [...a, ...o, ...rest] : [...o, ...a, ...rest]
  }
  const url = (f) => (/^(\/|https?:)/.test(f) ? f : BASE + f.replace(/^\.?\//, ''))
  async function readManifest() {
    try {
      const r = await fetch(`${BASE}MANIFEST.json`, { cache: 'no-cache' })
      if (!r.ok) return false
      const j = await r.json()
      const list = Array.isArray(j) ? j : j.cues ?? []
      cues = new Map()
      for (const c of list) {
        const name = String(c.cue ?? c.name ?? c.id ?? '')
        if (!name) continue
        const variants = (c.variants?.length ? c.variants : [{ files: c.files ?? c.file ?? c.src ?? c.path }]).map((v) => ({ stem: v.stem, files: pickFiles(v.files ?? v.file), loopEnd: Number(v.loopEndSeconds ?? c.loopEndSeconds) || 0, buf: null })).filter((v) => v.files.length)
        if (!variants.length) continue
        const beats = [c.beats ?? c.beat ?? []].flat().map((b) => Number(String(b).replace(/[^\d.]/g, ''))).filter(Number.isFinite)
        cues.set(name, { name, loop: !!c.loop, gain: Number(c.gain ?? 0.6), beatGain: c.beatGain ?? {}, beats, rr: c.roundRobin !== false, variants, last: -1, src: null, g: null })
      }
      return cues.size > 0
    } catch { return false }
  }
  let tries = 0
  const again = async () => { if (await readManifest()) { if (ctx) load(); return } tries++; setTimeout(again, tries < 20 ? 8000 : 30000) }
  readManifest().then((ok) => { if (ok) { if (ctx) load() } else setTimeout(again, 8000) })

  async function load() {
    if (loaded || !ctx || !cues.size) return
    loaded = true
    await Promise.all([...cues.values()].flatMap((c) => c.variants.map(async (v) => {
      for (const f of v.files) {                       // first format that decodes wins
        try { v.buf = await ctx.decodeAudioData(await (await fetch(url(f))).arrayBuffer()); break } catch { v.buf = null }
      }
    })))
    for (const c of cues.values()) if (c.loop && c.variants[0].buf) {
      c.g = ctx.createGain(); c.g.gain.value = 0; c.g.connect(master)
      c.src = ctx.createBufferSource(); c.src.buffer = c.variants[0].buf; c.src.loop = true
      // the .m4a beds carry 2048 wrap samples past the seam: loop on the manifest's loopEndSeconds (both formats)
      const le = c.variants[0].loopEnd; if (le > 0 && le < c.src.buffer.duration) { c.src.loopStart = 0; c.src.loopEnd = le }
      c.src.connect(c.g); c.src.start()
    }
  }
  function unlock() {
    if (!ctx) {
      try { if (navigator.audioSession) navigator.audioSession.type = 'playback' } catch {}
      ctx = new AudioContext()
      master = ctx.createGain(); master.gain.value = 0; master.connect(ctx.destination)
      ctx.onstatechange = label
    }
    ctx.resume?.()
    load()
  }
  function set(v) {
    on = v; store.set(v ? 'on' : 'off')
    if (v) unlock()
    if (master) master.gain.setTargetAtTime(v ? 0.9 : 0, ctx.currentTime, 0.25)
    label()
  }
  // remembered "on": the first press anywhere is the gesture (dropped as soon as the toggle itself is used)
  const first = (e) => { if (e.target.closest?.('.snd-btn')) return; drop(); set(true) }
  const drop = () => { removeEventListener('pointerup', first, true); removeEventListener('keydown', first, true) }
  if (store.get() === 'on') { addEventListener('pointerup', first, true); addEventListener('keydown', first, true) }
  btn.addEventListener('click', () => { drop(); set(!(on && ctx?.state === 'running')) })
  document.addEventListener('visibilitychange', () => { if (!ctx) return; if (document.hidden) ctx.suspend(); else if (on) ctx.resume() })

  const live = () => !!ctx && on && ctx.state === 'running'
  // beds: vis[beat] = 0..1 share of the screen
  function update(vis) {
    if (!live()) return
    const t = ctx.currentTime
    for (const c of cues.values()) {
      if (!c.loop || !c.g) continue
      let g = 0
      for (const [b, share] of Object.entries(vis)) {
        const bg = c.beatGain[b] ?? (c.beats.includes(Number(b)) ? c.gain : 0)
        g += share * bg
      }
      c.g.gain.setTargetAtTime(Math.min(1.2, g), t, 0.4)
    }
  }
  // one-shot: round robin (never the same file twice in a row) unless a variant is named; gain from beatGain[beat]
  function cue(name, { beat = null, variant = null, gain = null, delay = 0 } = {}) {
    if (!live()) return
    const c = cues.get(name); if (!c || c.loop) return
    const ready = c.variants.map((v, i) => [v, i]).filter(([v]) => v.buf)
    if (!ready.length) return
    let pick
    if (variant != null) pick = ready.find(([v, i]) => i === variant || v.stem === variant) ?? ready[0]
    else { const opts = ready.length > 1 ? ready.filter(([, i]) => i !== c.last) : ready; pick = c.rr ? opts[Math.floor(Math.random() * opts.length)] : opts[0] }
    c.last = pick[1]
    const s = ctx.createBufferSource(); s.buffer = pick[0].buf
    const g = ctx.createGain(); g.gain.value = gain ?? (beat != null ? c.beatGain[beat] : null) ?? c.gain
    s.connect(g); g.connect(master); s.start(ctx.currentTime + delay)
    c.fired = (c.fired ?? 0) + 1
  }
  return { update, cue, button: btn, get live() { return live() }, get cues() { return [...cues.values()] } }
}
