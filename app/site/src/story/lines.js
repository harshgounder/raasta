// story v2: EVERY on-screen line lives here, so the native Hindi check can fix them in one pass.
// source: story/STORY-v2.md (beats) + research/hermes/sc02/HINDI-CHECK.md (Devanagari S1-S11, pending native read).
// rules: S1 / S3 / S10 share "इससे ... कुछ नहीं होगा" word for word; S9 "कुछ नहीं हुआ" stays distinct;
// the kid says "Dadu" (never "Dadaji"); the RAASTA wordmark stays Latin. No brand names.
export const LINES = {
  // beat 1, caption next to the clean generic map card
  S4: { hi: 'मैप पे सब साफ़ दिखता है।', en: 'On the map, it all looks clear.' },
  // beat 2, first bird lift
  S5: { hi: 'ऊपर से देखो। ये रास्ता नहीं, एक भूल-भुलैया है।', en: 'Look from above. This is not a path, it is a maze.' },
  // beat 4, the old woman turns back
  S6: { hi: 'वही मैप। वही रास्ता।', en: 'Same map. Same street.' },
  // beat 5, the kid and Dadu
  S7: { who: 'kid', hi: 'दादू, सब लोग नॉर्मल मैप इस्तेमाल करते हैं। ये क्यों? इससे कुछ नहीं होगा।', en: 'Dadu, everyone uses the normal map. Why this one? This won\'t do anything.' },
  S2: { who: 'Dadu', hi: 'हाँ, सही कहा।', en: 'Yes, you\'re right.' },
  // beat 6, second bird lift
  S8: { hi: 'हर जाल का रास्ता।', en: 'A way around every trap.' },
  // beat 8, arrival
  S9: { who: 'kid', hi: 'कुछ नहीं हुआ!', en: 'Nothing happened!' },
  S10: { who: 'Dadu', hi: 'इसीलिए तो। इससे हमें कुछ नहीं होगा।', en: 'That is exactly why. With this, nothing will happen to us.' },
  // tagline lockup: brand Latin, sentence Devanagari (S11 / S1)
  S11: { brand: 'RAASTA', hi: 'इससे कुछ नहीं होगा।', en: 'Use it, and nothing goes wrong.' },
}

// small ink tags (product labels), beat 1 obstacles and beat 7 ways around
export const TAGS_B1 = [
  { id: 'cart', en: 'vendor cart on footpath', uv: [0.53, 0.47] },
  { id: 'pole', en: 'pole', uv: [0.70, 0.33] },
  { id: 'bikes', en: 'parked bikes', uv: [0.80, 0.50] },
  { id: 'scooter', en: 'speeding scooter', uv: [0.93, 0.55] },
  { id: 'tiles', en: 'broken tiles', uv: [0.33, 0.83] },
  { id: 'pothole', en: 'pothole', uv: [0.62, 0.84] },
  { id: 'drain', en: 'open drain', uv: [0.80, 0.71] },
]
export const TAGS_B7 = [
  { id: 'ramp', en: 'ramp here, 40 m on', at: 0.18 },
  { id: 'cross', en: 'level crossing', at: 0.42 },
  { id: 'carts', en: 'before 5 pm: no carts yet', at: 0.66 },
]

// beat 5 phone screen (the one red object): a measured receipt
export const PHONE = {
  title: 'RAASTA',
  rows: ['kerb 18 cm: avoid', 'ramp in 40 m', 'cart after 5 pm', 'drain slab: covered side'],
  foot: 'route: 0 hurdles',
}

export const CTA = {
  head: { en: 'Your street next.' },
  scan: { label: 'Show us your street', sub: 'scan a photo of a footpath', href: '/scan/' },
  map: { label: 'See your route', sub: 'open the RAASTA map', href: '/map/' },
}

// still comic (reduced motion / no WebGL): one line of plain description where a beat has no subtitle
export const STILL_NOTES = {
  b3: 'A young man with earbuds steps over every gap. The normal map works for him.',
  b4: 'An old woman with a walker stops at the high kerb, the cart, the horn. She turns back.',
  b7: 'They take the ramp, the level crossing, the stretch before the carts. A wheelchair user passes on the same route.',
}
