# SC-02 brainstorm (dsh), 16:40 IST

## (a) five ideas, two of them crazy

**1. Shadow altimetry: a one-photo height sensor (crazy, physics).**
For an image with a capture time and a rough location, compute the sun's azimuth and elevation
(NOAA solar position formula, no dependency), measure the shadow length of a pole, kerb or step
against a known reference in frame, and solve for the object height. A 17 cm kerb is exactly the
kind of number a wheelchair user cares about, and it comes from geometry, not a model. The demo is
a sun slider: drag the time, the shadow moves, the height estimate and its error bar move with it.
This is the hedge-fund oil-tank trick applied to a kerb, and it is explainable to any judge.
Falsifier: shadows at noon or under overcast are unusable; the site must say "no shadow evidence".

**2. The street audit receipt (product).**
One click on a photo returns a signed, timestamped audit record: barrier candidates, the exact OSM
segment, the evidence crop, the confidence, and the route delta in metres and minutes for a
wheelchair user. It looks like a receipt because it is auditable: every field links to its source.
Judges understand a receipt; municipalities understand a receipt; it is also the honest answer to
"is this real or a demo".

**3. Lunar-tie registration (reuse).**
Treat each photograph as a frame to register to the footpath graph. Estimate the horizon and
vanishing points, build an approximate ground plane, then score OSM segment candidates by distance,
bearing consistency and which side of the road the camera sees. Report a confidence, draw the tie
lines on the map, and let the presenter confirm. This is the same habit as the Chandrayaan-2 tie
points: multi-scale, outlier rejection, residual inspection, never a silent assumption.

**4. Dadi's pit wall (emotional, F1).**
A walking route drawn like an F1 lap: a vertical profile of kerbs and steps, a "bump count", a
"push effort" trace, and rest stops as pit stops. Rain turns into a safety car. Every segment has a
time loss and a risk, and the judge can see why one route is 400 m longer but actually possible.
This is the emotional core and the F1 methodology the user asked for.

**5. Crowd scars (guerrilla, hermes owns the lens).**
Mine public complaints (X, Reddit, Google Maps reviews, municipal grievance portals, news) for
geotagged footpath failures, and put the quotes on the map as pins. We did not just walk the street,
we read ten thousand complaints about it. This is the cheapest way to cover a whole city without
imagery, and it is a differentiator no fork gives us.

Runner-up crazy: frame-mine YouTube walking tours of Jaipur with yt-dlp (installed), geolocate by
landmark, and use those frames as a free street-level dataset. Licence: review each channel before
publishing frames.

## (b) critique of claude's ten

| # | idea | verdict | reason |
|---|---|---|---|
| 1 | two detectors must agree + needs a human look | KEEP, CHANGE | agreement between two weak models is theatre. Use one detector plus a physics cross-check (shadows) plus human confirm. Call it evidence triangulation, not two-model voting. |
| 2 | depth model gives kerb height in cm | KILL | monocular depth is relative, not metric. Claiming cm will be caught by one informed judge and it poisons the rest. Replace with shadow altimetry and known-size references. |
| 3 | same kerb, different sky slider | KEEP | honest robustness demo, and it doubles as a failure-mode exhibit. Needs paired captures; if absent, degrade the image synthetically and show confidence drop, labelled as simulation. |
| 4 | leave-time routing (vendors at 6 pm) | CHANGE | good instinct, no evidence tonight. Turn it into time-of-day confidence from complaint timestamps and vendor sightings, not a guarantee. |
| 5 | F1 pit wall for Dadi | KEEP, MERGE | strongest emotional idea. Merge with idea 4 above: one lap view, rest stops as pits, rain as safety car. |
| 6 | the street tells its story | KEEP, NARROW | keep only signals we can measure tonight: stain height (flood line), tyre marks on footpath, wear polish. Three signals, each with a caveat. |
| 7 | 3D world model of one crossing | CHANGE | full 3D from one image misleads. Either a hand-modelled 3D of one crossing with a wheelchair-eye path, or a 2.5D depth reveal labelled illustrative. Do not fake geometry. |
| 8 | one-tap Hindi municipal complaint with RPwD clause | KEEP | cheap, very Indian, gives the demo a consequence beyond the screen. Template plus photo plus geotag plus clause. |
| 9 | ward accessibility score heat map | KILL tonight | no data, and a score implies coverage we do not have. Replace with a coverage map: verified, unknown, and unverified, per area. |
| 10 | voice-first Hindi guidance | KEEP if cheap | browser speechSynthesis has hi-IN voices. Make it Dadi's voice, not a robot, and keep it off by default because autoplay is blocked. |

## (c) the single biggest risk

**Credibility collapse.** The site is beautiful, the barriers are hand-reviewed, and a judge asks
"does it work on my street?" If the honest answer is "no, only on these prepared images", the wow
turns into distrust in one question. Mitigation: one live path that works on any uploaded photo,
even if it returns "no accessible route, here is why and here is what is unknown", plus visible
provenance on every claim. The demo must be able to say "I do not know" in front of the judge.

## (d) story and character

Kamla, 68, Jaipur. She stopped going to the temple three years ago: three steps at the entrance and
a footpath that becomes a drain in the monsoon. The site is her street, her route, her voice. The
first screen is her sentence: "beta, yahan se nahi ja paungi." The cursor is her walking stick. The
route animates like a lap, the barriers light up where she would stop, and the last screen is the
same street with the route that works. Woodcut grandmother, santioni look, harmonium and temple
bells, one step sound when a barrier is confirmed.

## Method notes (NOTICE 6 and 7)

- S1 parts hunt: I have the 8-statement wave and the SC-02 sweep running; next is a dedicated
  parts hunt for pothole, kerb, stair, drain, vendor and map-matching components across GitHub,
  HF, arXiv, Gitee (blocked, logged), GitCode, ModelScope (blocked), Devpost, ETHGlobal.
- Internet-map ladder for images, with GET route and licence: Mapillary (token), KartaView (API
  empty here), Wikimedia Commons (works, CC), Flickr CC (key), YouTube walking tours (yt-dlp,
  review licence), municipal complaint photos (public), news photos (fair use risk), Bhuvan
  satellite (public), OSM (ODbL). Tonight: Commons plus OSM, YouTube only if licence is clear.
- RE arsenal used: `re manifest` (15 domains, 135 actions, 41 components), `re playbook design`
  (tokens, slop audit, style compare) and `re playbook media` (probe, frames, audio). The design
  playbook matters for the santioni look: tokens first, slop audit before shipping, compare after.
- Predicted factors: for every missing measurement (kerb height, cross slope, passing width) name
  the paper or formula that estimates it, and mark it as inferred, never measured.
