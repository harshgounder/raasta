# SC-02 S2: maximum information per pixel

Lane S2, hermes, written 2026-10-24 16:40 IST. Research only, no code. Companion file:
`INDIA-CHAOS-FACTORS.md` (the factor list and the what-if round).

The thesis in one line: a photograph of a footpath is not a picture of a footpath, it is a measurement
record, a timestamp, a weather log and a confession, if you know how to read it. Each section below is one
readable channel, what it yields, what it costs to extract, and the honest confidence.

## 1. Geometry: the frame is a measuring tape

| read | how | yields | confidence | needs |
|---|---|---|---|---|
| camera height | phone held at eye level, or GSV rig height (about 2.5 m for the car camera) | scale for everything else | high if height known, else unknown | one anchor per capture session |
| vanishing points | two horizontal line families (kerb edge, wall top) | true horizon, so pitch and roll without IMU | high | 2 visible line families |
| kerb height | vertical offset between road plane and footpath plane at a known distance | cm, the number the whole pitch hangs on | medium to high, degrades on occlusion | a clean kerb corner in frame |
| footpath width | lateral distance between kerb and wall/edge | cm, plus passable width between obstructions | high | both edges visible |
| cross-slope | tilt of the footpath plane | percent grade, the thing that tips wheelchairs | low to medium from one view, high from multi-view | 2+ views or a level reference |

Calibration anchor from a real Indian audit, not from theory: measured footpath heights of 200 to 250 mm
around a set of blocks, against a 150 mm standard (https://www.gtkp.com/document/irf-world-road-meeting-2017-paper-814/,
fetched 2026-10-24). That is the shape of the claim we can make: not "bad footpath", but "230 mm, standard
is 150 mm, that is 80 mm too high for a wheelchair and exactly the height that makes a ramp illegal".

Ground truth discipline: three kerbs measured by hand with a ruler, on camera, in the same session as the
demo captures. Without that, every centimetre on the site is an assertion.

## 2. Shadows: the clock and the ruler that come free with sunlight

| read | physics | yields | confidence |
|---|---|---|---|
| capture time | shadow azimuth plus sun ephemeris for the date and city | time of day to within about an hour from one shadow | medium |
| true north | shadow direction plus time | orientation without compass or EXIF | medium |
| object height | shadow length divided by tan(solar altitude) | height of a pole, a sign, a parked car, a person | high for isolated objects on flat ground |
| objects outside the frame | shadow of an obstruction whose body is off camera | evidence something blocks the path that the photo does not show | low to medium, but it is a genuinely novel signal |
| staged cleanup | same corner at 05:30 (clean) versus 18:00 (vendors) | proves the failure is time-conditional, not cosmetic | high |

This is the same trick as reading oil-tank shadows from orbit to predict inventories, and it is the single
cheapest way to make a judge feel the system sees more than they do. The honest limit: shadows fail in
overcast monsoon and at night, which is why it is a channel, not the method.

## 3. Surfaces: stains, wet patches and wear are a flood and drainage log

| read | how | yields | confidence |
|---|---|---|---|
| water staining line on a wall or kerb | horizontal tide mark, height relative to kerb | past flood depth in cm, so the monsoon risk of that exact spot | medium |
| wet patch persistence | dark patch on a dry day, algae or moss film | chronic drainage failure, not a one-off rain | medium |
| tyre and two-wheeler tracks on a footpath | rubber marks, oil drips, scuff arcs | the footpath is used as a parking or riding lane, the single most Indian failure mode | high |
| wear polish on a ramp lip | smooth, lighter stone at the edge | how many wheels actually roll there, so it is a used route, not a dead one | low to medium |
| repaired patches | colour mismatch, fresh concrete boundary | how often this spot has been dug up | medium |

Value for the pitch: it converts a static photo into a history. "This is not a wet footpath, this is the
sixth flood at this spot since 2022, and here is the stain line at 40 cm."

## 4. Signage and language: the street's own text layer

| read | yields | why it matters for India |
|---|---|---|
| script detection (Devanagari, Tamil, Bengali, Kannada, Telugu, Gujarati, Punjabi, Odia) | which state and often which city, without geotags | image sources are not geotagged; the script is a free region classifier |
| shop board language mix | likely state, likely income band of the catchment | supports the equity argument, not decoration |
| sign content (hospital, clinic, school, bus stop, police) | trip purpose for the route | "this failed kerb is on the only wheelchair route to a clinic" |
| temporary signs, handbills | markets, events, vendors | predicts vendor-hour obstruction |

Confidence: high for script family from a clear sign, medium for city, low for income inference. Do not
overclaim income; keep it to state and city.

## 5. Vegetation, season and weather

| read | yields | confidence |
|---|---|---|
| leaf-on versus leaf-off, flowering species | season and roughly which month | medium |
| wet ground plus green canopy plus flat light | monsoon, so the failure is seasonal | medium |
| long shadows plus dry dust | pre-monsoon summer, when footpath heat matters more than water | low |
| dust film on surfaces | recent dry spell, or construction next door | low |

Use this to prove the system is season-aware, which is the literal scope of the statement ("any time,
season, weather"). It also justifies the same-kerb-different-sky slider with evidence rather than a filter.

## 6. Reflections and glare

| read | yields | confidence |
|---|---|---|
| reflection in a shop window or wet road | geometry of what is behind the camera, sometimes the other side of the street | low, but impressive when it works |
| specular glare on a wet footpath | surface water and slope direction | low |
| mirror image of a sign | the sign's text when the sign faces away | low |

Treat as a flourish, never as a claim. One demo moment, clearly labelled as an inference.

## 7. Reconstruction when the photo is bad, missing or old

| case | method | what the site shows |
|---|---|---|
| blurry or low-resolution frame | multi-frame agreement from a video walk (median stack over 30 frames) | "recovered from 30 frames", with the frames shown |
| occluded kerb (car, vendor, crowd) | reconstruct the edge from the frames before and after, plus a splat of the segment | the kerb line continues through the obstruction, marked as inferred |
| no coverage at all | neighbour interpolation along the street graph, flagged as low confidence | a grey segment, never a fake reading |
| a single photo of one crossing | Gaussian splat from a 60 second phone walk, judge rides it in first person | the wheelchair-eye view |

The LUNAR-TIE discipline applies: when the image is incomplete, reconstruct, mark the reconstruction, and
never let an inference wear the same colour as a measurement. That rule is also the answer to the biggest
risk claude and I agree on.

## 8. What this file does not claim

- No cm-level accuracy on cross-slope from a single frame. It is a multi-view or bust.
- No claim that shadow timing works in overcast or at night.
- No income or caste inference from signage. Ethnic and income inference from street imagery is both
  unreliable and reputationally dangerous for a judged pitch.
- No assertion that any of the above is built. It is a research map of what is physically extractable.

## 9. Sources actually read

- GTKP, WALKABILITY, ACCESSIBILITY and SAFETY AUDITS, kerb heights 200 to 250 mm measured in an Indian
  audit (https://www.gtkp.com/document/irf-world-road-meeting-2017-paper-814/, 2026-10-24).
- UNDP India, Disability Accessibility Audit report, 2024 PDF, audit method and manhole placement guidance
  (https://www.undp.org/sites/g/files/zskgke326/files/2024-11/dissability_accessibility_audit_report.pdf,
  2026-10-24).
- CPPR Pedestrian Audit Report 2008, footpath widths measured in inches in an Indian city
  (https://www.cppr.in/wp-content/uploads/2012/10/Pedestrian-Audit-Report-2008.pdf, 2026-10-24).
- IRC:103 as the pedestrian infrastructure standard referenced by Indian studies, cited via
  https://www.researchgate.net/publication/396002556 (abstract only, standard text not opened, UNVERIFIED
  clause wording).
