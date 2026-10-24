# BRAINSTORM SYNTHESIS v1 (claude, 2026-10-24 ~16:40 IST)

Inputs: claude's 10 ideas; hermes (hyp-hermes m_1792839711352_5de342); dsh (hyp-dsh m_1792839755721_830337, file research/dsh/SC02-BRAINSTORM.md); helpers' files sc02-SOTA.md, sc02-PIXEL-AS-DATA.md, sc02-FACTOR-UNIVERSE.md. codex reply pending.

## Votes on claude's 10

| # | idea | hermes | dsh | claude's resolution |
|---|---|---|---|---|
| 1 | two detectors agree, else "needs a human look" | KEEP, must abstain on stage | KEEP+CHANGE: triangulate with physics, not two weak models voting | KEEP: detector A + detector B + a physics/geometry check; abstain shown on stage |
| 2 | kerb height in cm from depth | CHANGE: second view or geometry check + error bars | KILL: monocular depth is not metric | **CHANGE, not kill**: height from THREE independent routes (shadow altimetry, vanishing-point/camera-height geometry, metric depth MoGe-2 + GeoCalib); show the spread as an error bar; disagree = abstain; ground-truth 3 real campus kerbs with a ruler on camera |
| 3 | same kerb, different sky slider | KEEP, label synthetic | KEEP | KEEP, every generated frame labelled "simulated" |
| 4 | leave-time routing | KEEP, the real gap vs Google Maps | KEEP as confidence, not guarantee | KEEP as "likely blocked 17:00-21:00 (based on X)" |
| 5 | F1 pit wall for Dadi | KEEP, 3 numbers, drop jargon after 1 slide, do not infantilise | KEEP (emotional core) | KEEP, 3 numbers: extra minutes, kerbs climbed, rest stops |
| 6 | street tells its story | KEEP, confidence on every inference | KEEP, only 3 measurable signals | KEEP 3: shadow clock, wall stain = flood depth, wet surface = drainage |
| 7 | 3D world model of a crossing | KEEP only if under 2 h | CHANGE: no fake 3D; hand-modelled or labelled 2.5D | CONDITIONAL: try AnySplat/splat from the user's photo walk with a 2 h cap; else 2.5D parallax; always labelled "reconstructed" |
| 8 | one-tap Hindi municipal complaint | KEEP as closing button | KEEP | KEEP |
| 9 | ward score heat map | KILL as centrepiece | CHANGE to a coverage map | CHANGE: a "known / unknown" coverage map, honest |
| 10 | voice-first Hindi | KEEP, pre-recorded | (no vote) | KEEP, pre-recorded narration + live TTS optional |

## New ideas from the fleet (strongest first)

| idea | from | why it is strong |
|---|---|---|
| Shadow altimetry / shadow clock (height and time from the sun) | hermes 2, dsh 1, pixel-as-data 1-2 | three sources converged; physics, checkable, the oil-tank story |
| Scar ledger: every failure bound to CAG lines, court orders, RTI, grievance complaints ("reported 4 times since 2023, fixed 0") | hermes 3, dsh 5 (crowd scars) | compelled evidence from the idea-channel framework; works where there are no images |
| Trips not taken counter: elderly/disabled population near each failed crossing x avoidance = trips lost per day and rupees | hermes 5 | the number no competitor computes; nonconsumption channel |
| Street audit receipt: one click gives candidate, OSM segment, evidence crop, route delta, every field linked to source | dsh 2 | the honest answer to "is this real?" |
| LUNAR-TIE registration of the photo to the map (horizon, vanishing points, ground plane, side of road) with tie lines and residuals | dsh 3 | the map-matching challenge in the statement |
| Photo as measuring tape (camera height + vanishing point) | hermes 1 | becomes route 2 of idea 2 |
| Live path on ANY uploaded photo, allowed to say "no route, here is why" | dsh risk mitigation | kills "does it work on my street?" |

## Biggest risks named
- hermes: precision claims outrunning evidence (one wrong "12 cm" kills the measurement story). Fix: abstain, error bars, 3 ruler ground truths, never claim past validated error.
- dsh: credibility collapse ("only prepared images"). Fix: any uploaded photo goes through live; honest "unknown".
- Both: do not assume Google Street View coverage in India.

## Story candidates (user picks)
| story | from | opening line |
|---|---|---|
| **Billu the one-eyed street cat**, woodcut, kerb height, goes where wheelchairs cannot; the site is his patrol; he measures the city with his body | hermes | "Billu is 22 cm tall. He can cross this road. Dadi cannot." Ending: Billu sits on the one ramp that works |
| **Kamla, 68, Jaipur**, stopped going to the temple 3 years ago | dsh | "beta, yahan se nahi ja paungi"; cursor is her stick; the route animates like a lap |
| **Dadi + grandchild** | claude | (draft) |
| possible merge (claude) | | Billu guides Kamla: the cat is the narrator and measuring stick, Kamla is the human stake |
