// story.json schema (v1), checked at load so a content drop with a typo shows a warning instead of a blank page.
//
// story = { title:{en,hi}, subtitle:{en,hi}, bodies:[body], beats:[beat] }
// body  = { id, label:{en,hi}, eye_height_cm, fov?, pitch_deg?, ground?: 'footpath'|'road', z? (m across the street: 0 = kerb edge, -2.4 = shop wall, > 0 = road),
//           speed_mps?, filter:{ lowpass?: Hz, highpass?: Hz }, ambience: loop name, ambience_fallback?: loop name }
// beat  = { id, character: body id, eye_height_cm, screens?, title?: true,
//           text:{ en:[line, line], hi:[line, line] },
//           scene_image: null | "path.png" | { default: "path.png", <body id>: "path.png" },
//           scene:{ street:[{ type: pole|parked|steps|broken|no-ramp, x?: m, label?, note? }], focus?: type,
//                   time?: day|dusk|night, walk_m?, figure?: bool },
//           sound_cue: one-shot name (whoosh, tear, crack, stamp, clink, ...), bed?:{ loop: gain },
//           interactable:{ type: none|switch|tap-barrier|hold|press|link, label?:{en,hi}, done?:{en,hi}, href?,
//                          lift_m? (hold: how far the camera rises), clears_filter? (press: the muffle comes off),
//                          links?: [{ href, label:{en,hi} }] (link: several calls to action) },
//           after?: [caption numbers that wait for the interaction] }
// v2 additions (final story, 2026-10-24):
//   body.who:{en,hi}; beat.regime: a|b|c (ART-BRIEF palette regimes); beat.sequence: [body ids] (scroll walks the
//   bodies, the switch can still override); beat.camera: body id (camera stays at that body while the switch picks
//   whose route/line shows); beat.pitch_deg / beat.filter: overrides; beat.lines_by_body:{ <body id>:{en,hi} };
//   beat.speech:{ who, hi, roman, en, after?, when_body? } (a spoken Hindi line with a small English subtitle);
//   beat.receipt:{ title:{en,hi}, rows:[{k:{en,hi}, v:{en,hi}}], link?:{href,label} } (shown after the press);
//   scene.clock:[from_min, to_min] (clock in the eye tag follows the scroll); street feature from?/until?/bodies?/to?/z?
export const INTERACTABLES = ['none', 'switch', 'tap-barrier', 'hold', 'press', 'link']
export const BARRIERS = ['pole', 'parked', 'steps', 'broken', 'no-ramp', 'ramp', 'cart', 'route', 'unknown']

export function checkStory(s) {
  const warn = []
  if (!Array.isArray(s?.bodies) || !s.bodies.length) warn.push('no bodies')
  if (!Array.isArray(s?.beats) || !s.beats.length) warn.push('no beats')
  const ids = new Set((s.bodies ?? []).map((b) => b.id))
  for (const b of s.bodies ?? []) if (!(b.eye_height_cm > 0)) warn.push(`body ${b.id}: eye_height_cm missing`)
  const seen = new Set()
  for (const b of s.beats ?? []) {
    if (!b.id || seen.has(b.id)) warn.push(`beat id missing or repeated: ${b.id}`); seen.add(b.id)
    if (!ids.has(b.character)) warn.push(`beat ${b.id}: unknown character ${b.character}`)
    for (const x of [...(b.sequence ?? []), ...(b.camera ? [b.camera] : [])]) if (!ids.has(x)) warn.push(`beat ${b.id}: unknown body ${x}`)
    if (!b.text?.en || !b.text?.hi) warn.push(`beat ${b.id}: text.en / text.hi missing`)
    else if (b.text.en.length !== b.text.hi.length) warn.push(`beat ${b.id}: en and hi have a different number of lines`)
    const t = b.interactable?.type ?? 'none'
    if (!INTERACTABLES.includes(t)) warn.push(`beat ${b.id}: interactable ${t} unknown (treated as none)`)
    for (const f of b.scene?.street ?? []) if (!BARRIERS.includes(f.type)) warn.push(`beat ${b.id}: street type ${f.type} unknown`)
  }
  if ((s.beats ?? []).filter((b) => b.interactable?.type === 'hold').length > 1) warn.push('more than one hold beat: only the first gets the hold')
  for (const w of warn) console.warn('story.json:', w)
  return warn
}
