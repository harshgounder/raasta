# SC-02 PIXEL-AS-DATA: what one street photo (or a few) can reveal about walking and accessibility in India

v1, 2026-10-24 16:24 IST, claude (subagent for the lead). Scope per DECISIONS.md D1 + D2: SC-02, all of India, any hour, month, weather.
Sources searched with Parallel web_search / web_fetch, 2026-10-24 between ~16:05 and ~16:24 IST.

Status tags used in every row:
- **VERIFIED**: I opened the page or PDF with web_fetch this session and the claim is in the text I read.
- **EXCERPT**: seen only in a web_search excerpt, page not opened. Probably right, not checked in full.
- **COMPUTED**: I ran the number myself (script in scratchpad, two engines where noted).
- **HYPOTHESIS**: my idea, no source found that does it. Physics may be sound, nobody has shown it works.

---

## 0. One screen

```
   one photo  ─────────────────────────────────────────────────────────────────►  what SC-02 learns
   ┌──────────────────────────────┐
   │ pixels  (shadows, sky, water, │──► sun az/el ──► time of day, camera heading, object heights,
   │  cracks, stains, scuffs, text)│                  objects OUTSIDE the frame, shade hours
   │                               │──► water ──────► wet now, puddle, flood depth history (stain line)
   │                               │──► surface ────► material, cracks, kerb height, width, tactile state
   │                               │──► traces ─────► vehicles mounting kerbs, desire paths, vendor hours
   │                               │──► context ────► script/region, season, haze, lights, socioeconomics
   ├──────────────────────────────┤
   │ metadata (EXIF, Mapillary)    │──► GPS, time, heading, device, focal, exposure, on_foot flag
   ├──────────────────────────────┤
   │ many photos of one spot       │──► persistence: permanent barrier vs. hourly vs. one-off
   └──────────────────────────────┘
   no street photo at all ──► satellite: footpath presence, tree/building shadows, bare-soil desire lines
```

The rule carried over from LUNAR-TIE (`sih-idea/05-FACTOR-SPACE-UNIVERSE.md` L8-9, "every single pixel of dark or light is data") and the SOLAR guerrilla standard (`method/IDEATION-SOLAR.md` L152-154: "a physical quantity that is a deterministic function of the hidden ... quantity you want, that is visible in open data, and that the incumbent industry does not already read"). Every row below is held to that standard: a cue, the hidden quantity, the equation or statistic that links them, who already does it, and what SC-02 does with it.

**8 signals that can be demoed tonight** are in section 6.

---

## 1. The two analogies, checked

### 1.1 Floating-roof oil tanks (the hedge-fund trick): VERIFIED

| claim | source | status |
|---|---|---|
| Orbital Insight estimated oil in tanks with floating lids: "As a tank is depleted, the lid sinks, and the sun casts shadows on the inside of the tank changes. By detecting patterns in how those shadows change, analysts can estimate how much oil is available" | WIRED, 2015-03-16, https://www.wired.com/2015/03/orbital-insight | VERIFIED |
| "Orbital Insight ... tracks oil inventory in floating roof tanks (FRTs) using algorithms that calculate fluctuations in the volume of oil contained in FRTs by measuring cast shadows"; cloud cover over FRTs is used as an information-uncertainty index that moves market returns | Journal of Financial Markets 2024, https://www.sciencedirect.com/science/article/abs/pii/S1386418124000314 | VERIFIED (abstract + intro) |
| Ursa Space does the same with radar (SAR): "By measuring the height of the lid, plus ... diameter, we can use geometry to calculate the number of barrels"; ~1.7 million tank measurements; Cushing measurement 0.98 correlation with EIA since June 2019 | https://ursaspace.com/blog/an-inside-look-at-sar-based-measurements | VERIFIED |
| Orbital Insight uses "shadows ... and pulses of radar" | Business Insider 2020-04-21, https://www.businessinsider.com/gv-backed-orbital-insights-images-from-space-track-oil-storage-2020-4 | VERIFIED (headline + one line only) |
| Orbital Insight analysis said China built ~4x more SPR/commercial tanks than estimated and used floating-roof shadows to estimate fill | Radio Free Asia 2016-10-17, https://www.rfa.org/english/commentaries/energy_watch/hidden-10172016105720.html | EXCERPT |
| Academic version: optical near-nadir, "the position of a tank's floating roof can be estimated from the size of the shadow created by the tank's" wall | IEEE 2021, https://ieeexplore.ieee.org/document/9437809 | EXCERPT |

The geometry, in one line: the tank wall casts a crescent shadow onto the lid. Crescent width w (pixels x GSD), sun elevation e: depth of lid below rim d = w tan(e). Fill = (wall height - d) / wall height. Same algebra as every shadow row below. The lesson for SC-02 is not "shadows" alone but three things the trade did:
1. a hidden number (barrels) is a **deterministic function** of a visible one (crescent width),
2. the **regime** (clouds) is itself a signal of how much to trust the reading (the 2024 paper),
3. a **second sensor** (SAR) cross-checks the optical one. Same as LUNAR-TIE move M5 (two paths, agreement = confidence).

### 1.2 LUNAR-TIE pixel-as-data catalog, transposed to footpaths

Left column quoted from `~/sih-idea/05-FACTOR-SPACE-UNIVERSE.md` L69-89. Right column is the SC-02 analog (HYPOTHESIS unless a row in section 3 gives a source).

| LUNAR-TIE pixel-as-data entry | SC-02 street-photo analog |
|---|---|
| sun geometry: shadow algebra | time of day, camera heading, pole/tree/building heights, objects outside frame, shade hours (3.A) |
| terrain height: shadow envelope | kerb height and step height from the kerb's own shadow (3.C4) |
| albedo / composition | footpath material (pavers, concrete, granite, soil), wet vs dry (3.B, 3.C) |
| detector state: dark current vs temperature | ISO + exposure time = scene light level, a lux proxy at night (3.F2) |
| sensor identity: PRNU | same phone across uploads: dedupe, contributor trust, anti-spam (3.F5) |
| codec state: compression residue | forwarded WhatsApp copy vs original, metadata stripped or not (3.F5) |
| real resolution: slanted-edge MTF from crater rims | slanted-edge MTF from kerb edges: can this photo resolve a 13 mm grate gap at all? (3.F4) |
| texture class: Hurst / PSD exponent | surface roughness class, broken vs intact paving (3.C2) |
| acquisition conditions: tile vs solar ephemeris | EXIF time vs shadow-implied time: consistency check, clock or fake detection (3.A1) |

---

## 2. Shadow algebra for India, run (not predicted)

Script: `scratchpad/sc02/sun.py` (NOAA general solar position formula, no dependencies). Cross-checked with **pvlib** (`uv run --with pvlib`), a second engine.

| check | own script elev / az | pvlib elev / az | difference |
|---|---|---|---|
| Jaipur 2026-10-24 08:00 IST | 18.0 / 113.3 | 17.80 / 113.64 | 0.2 / 0.3 deg |
| Jaipur 2026-10-24 15:00 IST | 34.1 / 232.4 | 33.84 / 232.04 | 0.3 / 0.4 deg |
| Mumbai 2026-06-21 12:30 IST | 85.1 / 27.1 | 85.03 / 28.27 | 0.1 / 1.2 deg |
| Chennai 2026-06-21 12:30 IST | 78.6 / 336.4 | 78.68 / 336.85 | 0.1 / 0.5 deg |
| Jaipur 2026-12-21 12:30 IST | 39.7 / 181.3 | 39.73 / 181.28 | 0.0 / 0.0 deg |

Agreement within 0.3 deg elevation and 1.2 deg azimuth. COMPUTED, two engines agree.

### 2.1 Shadow lengths today (2026-10-24), shadow length = H / tan(elev)

| place | IST | sun elev | sun az | 1.6 m person shadow | 9 m pole shadow | shadow points to (deg from N) |
|---|---|---|---|---|---|---|
| Jaipur (MUJ) | 08:00 | 18.0 | 113.3 | 4.93 m | 27.73 m | 293 |
| Jaipur (MUJ) | 10:00 | 40.2 | 135.7 | 1.90 m | 10.67 m | 316 |
| Jaipur (MUJ) | 12:30 | 51.5 | 187.1 | 1.27 m | 7.16 m | 7 |
| Jaipur (MUJ) | 15:00 | 34.1 | 232.4 | 2.37 m | 13.32 m | 52 |
| Jaipur (MUJ) | 17:00 | 10.4 | 251.4 | 8.75 m | 49.21 m | 71 |
| Delhi | 12:30 | 49.5 | 189.4 | 1.36 m | 7.68 m | 9 |
| Mumbai | 12:30 | 59.5 | 183.6 | 0.94 m | 5.31 m | 4 |
| Chennai | 12:30 | 63.9 | 200.9 | 0.79 m | 4.42 m | 21 |
| Srinagar | 12:30 | 44.4 | 185.2 | 1.64 m | 9.20 m | 5 |

(full 25-row table in the script output; COMPUTED.)

### 2.2 India-only cue: the noon shadow flips direction south of the Tropic of Cancer

On 2026-06-21 at 12:30 IST, COMPUTED:

| place | lat | sun az | noon shadow points to |
|---|---|---|---|
| Jaipur | 26.84 N | 183.7 | 4 deg (north) |
| Delhi | 28.61 N | 198.6 | 19 deg (north) |
| Mumbai | 19.08 N | 27.1 | **207 deg (south)** |
| Chennai | 13.08 N | 336.4 | **156 deg (south)** |
| Srinagar | 34.08 N | 177.4 | 357 deg (north) |

Cities below 23.4 N (Mumbai, Chennai, Hyderabad, Bengaluru, Kolkata is ~22.6 N) get the sun north of zenith around the summer solstice, so noon shadows point south. A shadow-heading model trained on European or US street views (always north-pointing at noon) will get the camera heading wrong by up to 180 deg in half of India for part of the year. That is a concrete reason the pipeline must use the real ephemeris, not a learned prior. Also: in June at Jaipur noon a 9 m pole casts only 0.53 m of shadow (elev 86.6). Midday summer shade in India comes from trees and buildings, almost never from poles. COMPUTED.

### 2.3 Inversion examples (what the photo tells you)

| inversion | formula | worked example (COMPUTED) |
|---|---|---|
| height of an object from its shadow | H = L tan(e) | Jaipur 24 Oct 15:00 IST, e = 34.05 deg, shadow L = 6.3 m on flat footpath: H = 4.26 m |
| error on that height | dH = H sqrt((dL/L)^2 + (de / (sin e cos e))^2) | dL = 0.3 m, de = 1 deg: dH = +-0.26 m |
| time of day from shadow ratio L/H | e = atan(H/L), then invert the ephemeris | at 15:00 IST in Jaipur the sun drops 1.79 deg per 10 min, so a 1 deg error in e = about 5.6 min error in time |
| kerb height from the kerb's own shadow on the carriageway | h = w_s tan(e), w_s = shadow width measured along the sun azimuth | 150 mm kerb at e = 34 deg throws a 0.222 m shadow along the sun direction (narrower when the sun is not square to the kerb: divide by cos of the angle between sun azimuth and kerb normal) |
| camera heading | heading = sun azimuth + 180 - (image bearing of shadows after ground-plane rectification) | needs GPS + time (EXIF) and the horizon/gravity (GeoCalib); 180 deg ambiguity resolved by which end of the shadow touches the object |

---

## 3. The catalog

Columns: cue (what is visible) / reveals (the hidden quantity) / link (physics or statistics) / prior art (URL, status) / SC-02 use.

### 3.A Light, sun and geometry

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| A1 | direction + length of cast shadows of vertical things (poles, people, bollards) | sun azimuth and elevation, so time of day (if date + place known), or place (if time known) | shadow azimuth = sun azimuth + 180; H/L = tan(e); invert ephemeris (sec. 2) | Bellingcat chronolocation by shadow length, uses SunCalc, notes each length occurs twice a day, needs flat ground and object at right angles to camera https://www.bellingcat.com/resources/2021/05/18/unsure-when-a-video-or-photo-was-taken-how-to-tell-by-measuring-the-length-of-shadows VERIFIED; Bellingcat ShadowFinder (MIT licence) maps all places a shadow of given length could occur at a given UTC time https://github.com/bellingcat/ShadowFinder VERIFIED | stamp every photo with a shadow-time; compare to EXIF time; disagreement > 30 min = clock wrong or photo re-used (LUNAR-TIE M5: two sources must agree) |
| A2 | long shadow lines on the ground, sky brightness gradient, shading on vertical facades, pedestrians | sun direction relative to camera from a single image, with a probability map | "the majority of long shadows should be ... produced by vertical things"; each shadow line votes for a sun azimuth (180 deg ambiguity); naive Bayes fusion of sky, shadows, facades, pedestrians | Lalonde, Efros, Narasimhan, IJCV 2012, "Estimating the Natural Illumination Conditions from a Single Outdoor Image" http://graphics.cs.cmu.edu/people/jlalonde/pubs/papers/lalonde_ijcv_11.pdf VERIFIED; earlier "What do the sun and the sky tell us about the camera?" IJCV 2010, focal length, zenith and azimuth from sun position, under 1 deg azimuth error on a sequence https://link.springer.com/article/10.1007/s11263-009-0291-4 EXCERPT | camera heading when EXIF/Mapillary compass is missing; Mapillary's `computed_compass_angle` is zero for many images according to the osmapp source comment https://github.com/zbycz/osmapp/blob/master/src/services/images/getMapillaryImage.ts EXCERPT. Heading is needed to put a detection on the correct side of the street (the statement's "map each detection to the correct footpath segment") |
| A3 | a shadow on the footpath whose caster is outside the frame | an off-frame pole, tree, wall, signboard or building, with its height x distance constrained | shadow line points back along the sun azimuth to the caster; tip distance + elevation gives H if the base position is known from OSM/another photo | Torralba and Freeman, CVPR 2012, "Accidental pinhole and pinspeck cameras: revealing the scene outside the picture": "a person walking under direct illumination from the sun ... casts a well defined shadow ... we could reconstruct the scene around the person and outside of the picture frame" https://people.csail.mit.edu/torralba/publications/shadows.pdf VERIFIED; Bouman et al. ICCV 2017 corner cameras recover hidden people from penumbra at wall edges https://openaccess.thecvf.com/content_iccv_2017/html/Bouman_Turning_Corners_Into_ICCV_2017_paper.html EXCERPT; PlatoNeRF (MIT 2024) uses shadows to model hidden objects (needs lidar) https://news.mit.edu/2024/researchers-leverage-shadows-model-3d-scenes-blocked-objects-0618 EXCERPT | "there is a ~4.3 m object 3 m east of this frame": a pole in the footpath that no camera angle showed; feeds the pole-obstruction barrier class and the shade map. HYPOTHESIS for the street use, physics VERIFIED |
| A4 | building / tree shadow edges across the footpath; visible sky fraction above the walker | shade hours per footpath segment per day and month | project the sun path onto a fisheye of the sky; a sun position falling on a non-sky pixel = shaded at that minute; sky view factor by annulus sum | Middel et al. 2018, "Sky View Factor footprints", GSV to fisheye, Sobel + flood-fill sky mask, sun path every 15 min, daily sun duration maps for New York and San Francisco, 15,938,172 GSV locations https://www.sciencedirect.com/science/article/pii/S2212095518301883 VERIFIED; panorama SVF + irradiance with tree transmittance, irradiance MAE 77.8 W/m2, "walking route optimization" https://www.sciencedirect.com/science/article/pii/S0360132324009132 EXCERPT; MIT Treepedia Green View Index from GSV https://senseable.mit.edu/treepedia/treepedia_publication.pdf EXCERPT | "shaded route" toggle for elderly and pram users: cost += exposure minutes at that hour; India in May at 14:00 is the killer case (heat). Uses the June table in 2.2: poles give no shade, trees and buildings do |
| A5 | horizon line, vanishing points, up-vectors | camera roll, pitch, focal length (field of view), gravity direction | single-image calibration; learned + geometric optimisation | GeoCalib (ECCV 2024) intrinsics + gravity from one image https://github.com/cvg/GeoCalib EXCERPT; Perspective Fields (CVPR 2023) roll, pitch, FoV https://github.com/jinlinyi/PerspectiveFields EXCERPT | ground-plane rectification for shadow bearings (A1, A2) and metric measurements (C3-C5) |
| A6 | known-size objects (door ~2.1 m, auto-rickshaw, two-wheeler, standard kerb), horizon row | camera height above ground (phone at ~1.5 m on foot vs car rig ~2.5 m) | single view metrology: camera height = object height x (horizon row - base row) / (top row - base row) | UrbanVGGT: single-image sidewalk width with camera-height scale calibration, MAE 0.252 m, 95.5% within 0.50 m on Washington DC; "metric scale calibration is the most critical component"; width bias is linear in assumed camera height; best value 2.5 m for GSV https://arxiv.org/pdf/2603.22531 VERIFIED; Mapillary image field `on_foot` (pedestrian capture true/false/null) https://www.mapillary.com/developer/api-documentation VERIFIED | COMPUTED consequence: if a phone photo taken at 1.5 m is scaled with the GSV value 2.5 m, every width and kerb height is inflated by 2.5/1.5 = 1.67x, a 0.9 m footpath reads as 1.5 m and passes the wheelchair test it should fail. So camera height must be estimated per photo, never assumed |

### 3.B Water: now, recent, historic

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| B1 | mirror-like reflection of sky, lamps or buildings on the ground; dark glossy patch | wet surface or standing water now | water is specular; reflected light is polarised; a mirrored copy of a vertical object below the ground line = water surface | polarisation-based wet-road detection from a rear-view camera, tested at ~100 km/h https://www.sciencedirect.com/science/article/pii/S0389430403000067 EXCERPT; UW-Bench, 7,677 urban waterlogging images incl. low light and reflections https://arxiv.org/html/2407.08109v1 EXCERPT; BayFlood (Nature Comms 2026): a VLM asked "Does the street in this image show more than a foot of standing water?" on 926,212 dashcam images, 0.2% flagged https://www.nature.com/articles/s41467-026-75938-1 EXCERPT | wet = slip risk for crutches and elderly; standing water hides potholes and open drains (blind users); temporary cost on that segment |
| B2 | wet patch still present + photo date + rain record for that date | drainage quality of the segment | if wet many hours after the last rain, water is not draining | HYPOTHESIS (rain from IMD / Open-Meteo by EXIF date and GPS) | permanent "poor drainage" flag; in monsoon the segment gets a standing-water cost even with no fresh photo |
| B3 | water reaching wheels, exhaust, door handle of a car, a person's knee | flood depth at capture time | reference objects of known height; 11 levels on a human body in Chaudhary et al.; car levels none/pipe/handle/roof | Chaudhary et al., ISPRS Annals 2019, objects Person, Car, Bus, Bicycle, House; 11 levels from 0 (no water) to 10 (person submerged) https://isprs-annals.copernicus.org/articles/IV-2-W5/5/2019/isprs-annals-IV-2-W5-5-2019.pdf VERIFIED; GPT-4 Vision floodwater depth from reference objects https://arxiv.org/abs/2402.16684 EXCERPT; YOLOv4 car-reference levels https://link.springer.com/article/10.1007/s11269-023-03669-9 EXCERPT | crowd photos during monsoon set the segment impassable for wheels above ~a kerb height (HYPOTHESIS threshold) |
| B4 | a horizontal stain, mud, silt or "tide" line on compound walls, shop shutters, poles, at the same height along a stretch | historic peak flood depth on that stretch | turbid water leaves a mud line on non-porous surfaces when it recedes; porous materials wick water up, so stains on them overestimate the peak | USGS high-water marks: "Turbid water can leave a 'mud line' (or sometimes 'foam line' or 'stain line') on nonporous surfaces"; porous concrete/wood "can wick water higher than the actual peak" https://www.usgs.gov/mission-areas/water-resources/science/high-water-marks VERIFIED; multispectral imagery shows HWM on brick, plywood, concrete (not steel) https://ascelibrary.org/doi/10.1061/9780784485309.064 EXCERPT | a dry-season photo predicts the monsoon: "this stretch floods to ~30 cm" (stain height via A6 metrology). Monsoon-season routing cost from a single January photo. Detector: HYPOTHESIS (VLM prompt + horizontal-line consistency across several walls) |
| B5 | silt/sand fans on the footpath, debris lines, algae/moss in paver joints | recent overflow path of a drain; persistent damp | sediment deposits where flow slows; algae needs persistent moisture | HYPOTHESIS | slip cost; marks the drain that overflows (pairs with D-grates) |

### 3.C Surface: material, decay, geometry

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| C1 | cracks, potholes, alligator cracking, broken slabs | surface damage class and severity | detection / segmentation | RDD2022: 47,420 road images from Japan, India, Czech Republic, Norway, USA, China, 55,000+ damage instances; India part from Delhi, Gurugram, Haryana https://arxiv.org/abs/2209.08538 EXCERPT; Indian Footpath Damage Segmentation Dataset (Pune, Scientific Data 2025): 583 images from 8 high-traffic corridors, pixel masks, severity low/medium/high, GPS + capture time + conditions metadata https://www.nature.com/articles/s41597-025-06207-x VERIFIED | the "broken footpath" barrier class; severity sets cost; the Pune set is the closest Indian footpath (not road) training data found |
| C2 | texture statistics of the walking surface (PSD slope, Hurst exponent, joint spacing) | material (interlocking pavers, concrete, granite, cement tiles, bare soil) and roughness class | power spectrum / fractal texture, same as LUNAR-TIE d4 texture-fractal run | IRC:103-2022 lists concrete blocks, cement tiles, interlocking tiles and RCC bollards used on Indian footpaths https://law.resource.org/pub/in/bis/irc/irc.gov.in.078.2.2020.pdf EXCERPT; roughness to wheelchair vibration: HYPOTHESIS | wheelchair comfort cost (rough pavers vs smooth concrete); soil = impassable in monsoon |
| C3 | fading of paver colour, worn edges, exposed aggregate, patched repairs | age and maintenance history | weathering and wear; patch colour mismatch = repair | HYPOTHESIS | prior that a segment will degrade; municipal repair priority list |
| C4 | the step/kerb face and its shadow; depth map | kerb or step height (can a wheelchair cross?) | h = w_s tan(e) (sec. 2.3); or metric depth + ground-plane fit | Depth Anything V2 metric models (indoor/outdoor) https://github.com/DepthAnything/Depth-Anything-V2/blob/main/metric_depth/README.md EXCERPT; Metric3D v2 zero-shot metric depth + normals https://www.computer.org/csdl/journal/tp/2024/12/10638254/1ZsL7pJrPpe EXCERPT; in UrbanVGGT's comparison, Metric3Dv2 and UniDepthV2 were the best depth backbones after VGGT https://arxiv.org/pdf/2603.22531 VERIFIED; kerb-shadow method: HYPOTHESIS | **two engines**: shadow algebra and metric depth. Agree within ~2 cm = confident; disagree = "needs a human look" (LUNAR-TIE M5 + M10) |
| C5 | footpath edges on a fitted ground plane | clear width (wheelchair needs space) | segmentation + 3D reconstruction + plane fit + camera-height scale | UrbanVGGT (above) VERIFIED | width bottleneck per segment; the camera-height trap in A6 |
| C6 | curb ramp presence | missing kerb ramp (a statement barrier class) | heatmap detector on panoramas | RampNet (Project Sidewalk, ICCV'25 workshop): AP 0.9205, precision 0.9492, recall 0.8727 at threshold 0.55 on a 1,000-panorama gold set https://huggingface.co/projectsidewalk/rampnet-model VERIFIED; Project Sidewalk deep learning on GSV, ASSETS 2019 https://dl.acm.org/doi/10.1145/3308561.3353798 EXCERPT | detector A for ramps; US-trained, so Indian transfer must be measured on our own labels (statement says so) |
| C7 | yellow raised bars/domes, their continuity, what they lead into | tactile paving present / broken / obstructed / leading into a pole or tree ("tactile trap") | detection + path following | GPT-4o on GoPro footage around metro stations, 3-tier tactile obstruction risk https://journals.sagepub.com/doi/10.1177/23998083261462585 EXCERPT; YOLO11 tactile paving from bicycle camera, mAP50 0.777 https://dl.acm.org/doi/full/10.1145/3737611.3776614 EXCERPT; Chennai report on missing tactile paving and kerb ramps https://www.newindianexpress.com/cities/chennai/2025/Feb/03/encroachments-kerb-parking-make-footpaths-inaccessible-for-disabled-in-chennai EXCERPT | blind-user profile: a tactile line that ends in a pole is worse than none (HYPOTHESIS cost rule) |
| C8 | manhole covers: missing, sunken, raised, broken; grates and their slot direction | open-drain fall hazard; trip edge; caster/cane trap | cover state classes; slot parallel to travel catches narrow wheels and cane tips | manhole cover state normal/broken/down from dashcam, YOLOX https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2024.1337984/full EXCERPT; Swiss STDL manhole detection on street view + triangulation to coordinates https://tech.stdl.ch/PROJ-STREETVIEW/ EXCERPT; storm-drain + manhole RetinaNet https://pubmed.ncbi.nlm.nih.gov/32784983 EXCERPT; slot-direction rule: HYPOTHESIS | open manhole = hard block for every profile; triangulation from 2+ photos places it on the right segment |

### 3.D Traces of use (what people and vehicles do here when nobody is photographing)

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| D1 | black rubber scuffs and chipped corners on kerb faces, broken or bent bollards, tyre tracks in dust on the footpath | two-wheelers/cars mounting or riding the footpath here (rate, not just one event) | rubber transfer and edge spalling accumulate per mounting; a worn notch = a habitual entry point | no detector found. Ground truth that the behaviour is common: Bengaluru traffic police booked 42,810 cases of parking on footpaths and 6,011 of driving on footpaths in 2022 up to mid-June https://www.thehindu.com/news/cities/bangalore/video-we-went-looking-for-a-good-footpath-in-bengaluru-look-what-we-found/article65560118.ece VERIFIED; IRC:103-2022: "two-wheelers are seen riding on the footpath especially when the streets are congested" EXCERPT; damaged bollard photo, Bengaluru 2026 https://www.thehindu.com/news/cities/bangalore/bengalurus-footpaths-belong-to-everyone-but-pedestrians/article71182538.ece EXCERPT. Detector: HYPOTHESIS | "vehicles on footpath" is a statement barrier; scuffs predict it even in a photo with no vehicle present. A SOLAR-style guerrilla signal: deterministic, visible, nobody reads it |
| D2 | worn bare-soil lines across verges, medians and open plots (desire paths) | revealed pedestrian demand where the formal path is missing, blocked or longer | repeated trampling removes vegetation, positive feedback; pedestrians pick lowest effort | agent-based desire path prediction, CEUS 2025 https://www.sciencedirect.com/science/article/pii/S0198971525000043 EXCERPT; energy-based model: "pedestrians seek the route of lowest metabolic energy demand" https://www.sciencedirect.com/science/article/pii/S026427512501008X EXCERPT; desire lines hand-mapped over satellite imagery https://journals.library.ualberta.ca/constellations/index.php/constellations/article/download/18871/14659/0 EXCERPT | add as graph edges flagged "walk yes, wheels no" (soil, ruts, mud in monsoon); also tells the city where to build the next footpath |
| D3 | vendor carts, tarps, poles of folded stalls, chained carts, display racks, chairs | footpath encroachment and its **hours** | detection + time stamp (A1 shadow-time or EXIF); folded/chained cart in a morning photo = the stall opens later | StreetVendor-SLI: 2,794 street-level images for vendor detection (YOLO) https://pmc.ncbi.nlm.nih.gov/articles/PMC12337018 EXCERPT; Changsha IVSEN, 15,904 vendors, YOLOv8 + PSPNet street-edge features https://www.sciencedirect.com/science/article/abs/pii/S0264275125007875 EXCERPT; SIPSI, 3,907 vendors detected from street view https://www.sciencedirect.com/science/article/pii/S0264275122003985 EXCERPT; FootpathVision (Dhaka): 1,238 images, encroached vs clear, stalls/pushcarts/furniture and illegal parking, CC BY 4.0 https://github.com/tahshina01/Footpath-Sidewalk-Encroachment VERIFIED. Time-of-day encroachment from one photo: HYPOTHESIS | time-dependent barrier: the route at 10:00 differs from the route at 19:00. Most Indian-shaped dataset found is Dhaka FootpathVision |
| D4 | count of parked two-wheelers/cars per metre of kerb, on and off the footpath | parking pressure, likely footpath blocking | detection density; combined with signs | Georgia Tech CURA: GSV parking signs + parked vehicles found ~85% of road segments with true parking (Atlanta) https://resilience.research.gatech.edu/feature/mapping-street-parking-using-google-street-view-images EXCERPT; Chennai kerb parking blocking footpaths EXCERPT (link in C7) | parked-vehicle barrier class from the statement; density in a footpath-free photo still predicts blocking nearby |
| D5 | garbage piles, overflowing bins, plastic litter | obstruction + collection schedule + slip/smell + attracts animals | detection; litter is the most changeable street feature | SpotGarbage (UbiComp 2016), GINI dataset, 87.69% mean accuracy, Android app https://dl.acm.org/doi/10.1145/2971648.2971731 EXCERPT, code https://github.com/KudaP/SpotGarbage EXCERPT; pLitterStreet 13,000+ vehicle-camera images https://arxiv.org/abs/2401.14719 EXCERPT; GSV change study: litter was the only feature that differed in more than 20% of image pairs https://pubmed.ncbi.nlm.nih.gov/40467920 EXCERPT | transient barrier with a decay time; persistent dump = permanent |
| D6 | dogs, cattle, goats; dung | animal risk (bites, falls) for children, elderly, blind | detection | IDD India Driving Dataset has an "animal" class among 34 classes, 10,004 images, Hyderabad + Bangalore https://arxiv.org/abs/1811.10200 EXCERPT; stray dog detection in Kashmir, YOLOv11 https://www.researchgate.net/publication/392396041_Automated_Detection_and_Threshold-Based_Alerting_of_Stray_Dogs EXCERPT; Indian roadway animals R-3D-YOLOv3 https://www.mdpi.com/2079-9292/10/24/3079 EXCERPT | soft cost by profile; repeated sightings at one spot = a pack territory (HYPOTHESIS) |
| D7 | sand, gravel, brick stacks, rebar, debris on the footpath; dug trenches; cables | active construction, a temporary barrier with an expected duration | open-vocabulary detection; change detection over time | Bengaluru reports of construction debris and dug footpaths https://www.thehindu.com/news/cities/bangalore/encroached-footpaths-fast-moving-vehicles-put-pedestrians-at-risk-at-wind-tunnel-junction/article71053149.ece EXCERPT; "The minefield called footpath" (dug, repaired, dug again) https://www.thehindu.com/opinion/open-page/the-minefield-called-footpath/article71356731.ece EXCERPT; detector: HYPOTHESIS (Grounding DINO / OWLv2 prompts "sand pile", "brick stack") | time-boxed barrier; reopens when a later photo shows it gone |

### 3.E Context: region, season, air, light, people

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| E1 | script and language on signboards (Devanagari, Tamil, Bengali, Gurmukhi ...), STD codes in phone numbers, PIN codes, state code on number plates | region and language, often the city, with no GPS | script to state is a strong prior; STD and RTO codes are lookup tables | Bharat Scene Text Dataset: 6,582 images, 11 Indian languages + English, detection, script ID, recognition https://arxiv.org/abs/2511.23071 EXCERPT; IndicPhotoOCR toolkit (MIT licence), 11 languages + English, ViT script ID, HF demo https://github.com/Bhashini-IITJ/IndicPhotoOCR EXCERPT; MIST, ~12K scene images, 11 scripts https://cdn.iiit.ac.in/cdn/ilocr.iiit.ac.in/dataset/static/assets/img/publication/scene_text/MIST-Multilingual-Incidental-Dataset-for-Scene-Text%20Detection.pdf EXCERPT; plate/STD use: HYPOTHESIS | geolocate photos with stripped GPS (WhatsApp forwards); set the UI language for the user automatically; region sets monsoon calendar priors. Number plates must be blurred before storage (privacy) |
| E2 | leaf state, flowering, dry leaf litter, green-up after rain | season / month; time since monsoon onset | phenology from colour (greenness) over time | dashcam tree phenology, green-up date from daily images https://pmc.ncbi.nlm.nih.gov/articles/PMC9570992/ EXCERPT; StreetTree: 12.2M street view images, 3.37M trees, season label per image https://arxiv.org/html/2602.19123v1 EXCERPT; seasonal bias of street view indicators, larger in monsoonal climates https://www.sciencedirect.com/science/article/pii/S0198971525000559 EXCERPT | a second clock (month) to check EXIF; also warns that a Google image from the dry season understates monsoon problems |
| E3 | haze: washed-out far buildings, low contrast, raised dark channel | PM2.5 level / visibility | atmospheric scattering; dark channel prior (haze lifts the darkest channel) | Learning Pollution Maps from Mobile Phone Images (IJCAI 2022): 382 phone images from Delhi and Ghaziabad matched to CPCB sensors, MAE 44 ug/m3, and sensors under 2 km apart already disagree a lot https://ijcai.org/proceedings/2022/0697.pdf VERIFIED; PM25Vision: 11,114 Mapillary images aligned with WAQI stations https://arxiv.org/pdf/2509.16519 EXCERPT | Delhi winter fog/smog: low-vision users, asthma; also an image-quality gate (hazy far field = do not trust far detections) |
| E4 | streetlight heads on poles (day photos); lit pools on the ground and dark gaps (night photos) | night lighting coverage and gaps | detection; illuminance pool spacing | street lighting condition detection with YOLO-CSE https://www.mdpi.com/2073-8994/17/8/1294 EXCERPT; nighttime street view "almost nonexistent", synthesised with a diffusion model conditioned on SDGSAT-1 radiance https://www.sciencedirect.com/science/article/pii/S1569843226000622 EXCERPT; lighting and pedestrian reassurance (Fotios) https://eprints.whiterose.ac.uk/id/eprint/81121/3/Unwin%20Fotios%202011%20Does%20lighting%20contribute%20to%20reassurance.pdf EXCERPT | night routing: unlit = cost for women, elderly; a pothole you cannot see at night is worse |
| E5 | colour of the light at night: orange-yellow (sodium) vs white (LED); colour temperature of daylight | lamp type, so whether the stretch was retrofitted; overcast vs clear; golden hour | spectral signature of the source; white balance | India's Street Lighting National Programme: 1,31,10,745 LED streetlights installed by EESL by 30 June 2024 https://pib.gov.in/PressReleasePage.aspx?PRID=2040102 EXCERPT; illuminant colour temperature from images (Wandell lab) https://web.stanford.edu/~wandell/data/papers/CIC99.pdf EXCERPT; lamp-type inference: HYPOTHESIS | a still-sodium street may be an un-maintained ward (prior); daylight colour cross-checks shadow-time |
| E6 | car and two-wheeler make/model/age mix | neighbourhood income, education, voting (US) | statistical association; 88 car attributes; linear models | Gebru et al., PNAS 2017: 50,881,098 GSV images, 200 US cities, ~22M cars detected, 2,657 car classes, voting prediction r = 0.74 for 2008 https://www.pnas.org/doi/10.1073/pnas.1700035114 VERIFIED | Indian transfer (SUV vs auto-rickshaw vs two-wheeler ratio): HYPOTHESIS. Use it to check equity (are poor wards getting fewer photos and fixes?), never to route people away from poor areas |
| E7 | whole-scene look | perceived safety, liveliness, beauty | crowd pairwise votes, learned regressor | StreetScore (MIT Media Lab): trained on 2,920 New York + Boston images with crowd safety rankings https://www.media.mit.edu/projects/streetscore/overview/ VERIFIED; Place Pulse 2.0 study: visible street features explain ~18% of perception variation, 110,000 locations, 56 cities https://www.sciencedirect.com/science/article/pii/S0169204621002206 EXCERPT; Naik et al. PNAS 2017 change in Streetscore over time https://www.pnas.org/doi/10.1073/pnas.1619003114 EXCERPT | a soft "feels safe at night" layer; US/European training means it must be re-labelled locally before any claim |

### 3.F Metadata and the camera as an instrument

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| F1 | EXIF DateTimeOriginal, GPS lat/lon/alt, GPSImgDirection, Make, Model, FocalLength, ExposureTime, ISO | time, place, heading, device, lens | standard tags | Mapillary API v4 image fields include `altitude` (from EXIF), `camera_parameters` (focal, k1, k2), `camera_type` (perspective, fisheye, equirectangular), `on_foot`, `sequence`, `sfm_cluster` (point cloud), `mesh` https://www.mapillary.com/developer/api-documentation VERIFIED; `captured_at` (ms since epoch), `compass_angle`, `computed_compass_angle`, `computed_geometry` https://blog.mapillary.com/update/2021/06/23/getting-started-with-the-new-mapillary-api-v4.html EXCERPT | time + place drive the ephemeris (sec. 2); `sfm_cluster` gives free 3D for kerb heights; `on_foot` gives camera height (A6) |
| F2 | ExposureTime t, f-number N, ISO S | scene brightness (exposure value), so a light-level proxy at night | EV100 = log2(N^2 / t) - log2(S / 100); each +1 EV = twice the light | photographic exposure standard (no fetched source this session); use for lighting: HYPOTHESIS | "how dark is this footpath at night" from any phone photo, no light meter |
| F3 | blur streak length and direction | camera speed during exposure; capture from a moving vehicle vs a walker | blur length = speed x exposure / (depth x pixel pitch / focal) | Image as an IMU (2025): camera motion from a single motion-blurred image, "the extent and direction of motion blur provide direct cues about the camera's motion" https://arxiv.org/html/2503.17358 VERIFIED; vehicle speed from one blurred image (2008) https://www.sciencedirect.com/science/article/pii/S0262885607000881 EXCERPT | quality gate: if blur > kerb edge width, do not measure kerb height from this frame; also tells car-mounted (road-centre view, far footpath) from walker photos |
| F4 | sharpness across a straight high-contrast edge (kerb edge, paver joint) | real resolution of this photo (MTF) | ISO 12233 slanted-edge method; LUNAR-TIE used crater rims | LUNAR-TIE catalog `05-FACTOR-SPACE-UNIVERSE.md` L85-86 (internal); street use: HYPOTHESIS | refuse to judge "gap > 13 mm" or crack width when the photo cannot resolve it (honest abstention, M10) |
| F5 | sensor noise fingerprint (PRNU); JPEG quantisation tables, double compression | same phone across uploads; forwarded / edited copy | PRNU is a per-sensor pattern; recompression leaves traces | LUNAR-TIE catalog L81-84 (internal); street use: HYPOTHESIS | dedupe crowd photos, spot one person spamming fake barriers, weight originals over WhatsApp forwards |
| F6 | sky colour, contrast, hard shadow edges | weather class (sunny/cloudy/rain/haze), illuminant | learned classifiers on weather features | two-class weather classification (sunny/cloudy), PAMI 2017 https://pubmed.ncbi.nlm.nih.gov/28113309 EXCERPT; SVM 4-class (rainy, low light, haze, clear) 92.8% https://arxiv.org/abs/2409.00821 EXCERPT | condition tag on every detection; the condition-split evaluation D2 demands (night/monsoon/fog/dust behaviour "must be shown, not claimed") |

### 3.G Many photos of one place (time is a sensor)

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| G1 | same spot across capture dates | which barriers are permanent (step, pole), hourly (vendor), daily (parked car), one-off (garbage, construction) | change detection; persistence = fraction of captures where the barrier is present | CityPulse (AAAI 2024): GSV time series ~1,000 coordinates, 6 cities, avg 10 images per series over 2007-2023 https://ojs.aaai.org/index.php/AAAI/article/download/30216/32163 EXCERPT; Naik et al. PNAS 2017 physical urban change https://www.pnas.org/doi/10.1073/pnas.1619003114 EXCERPT; building height change from multi-temporal street view (Baidu time machine) https://www.mdpi.com/2076-3417/16/1/550 EXCERPT | barrier cost x persistence; unseen for N months = "unknown", never "safe" (D2 rule) |
| G2 | several photos from different positions | 3D position of a barrier (triangulation), true heights | multi-view geometry | STDL manhole triangulation from street view (C8) EXCERPT; Mapillary `sfm_cluster` VERIFIED (F1) | snaps the detection to the right footpath segment and side of the street |
| G3 | shadow position in photos at different hours | building/tree heights without any depth model; shade map for every hour | two shadow observations solve height and caster position | HYPOTHESIS (shadow algebra, sec. 2.3) | shade map validation |

### 3.H No street photo: satellite and aerial fallback

| # | cue | reveals | link | prior art | SC-02 use |
|---|---|---|---|---|---|
| H1 | footpath and crosswalk pixels from above | footpath presence, crosswalks, network topology | semantic segmentation of orthoimagery to polygons to centreline graph | Tile2Net (NYU/MIT): roads, sidewalks, crosswalks, footpaths from aerial tiles, ~90%+ of sidewalks recognised in Boston and Cambridge, trained on ~19 cm imagery https://github.com/VIDA-NYU/tile2net EXCERPT, https://news.mit.edu/2023/open-source-tool-mapping-sidewalks-0315 EXCERPT; S2DB-Net satellite + street-view joint sidewalk segmentation (ISPRS 2026) https://github.com/EdgedEnd/S2DB-Net EXCERPT; Esri pedestrian infrastructure model https://doc.arcgis.com/en/pretrained-models/latest/imagery/introduction-to-pedestrian-infrastructure-classification-model.htm EXCERPT | coarse layer for streets Mapillary has never driven; marked lower confidence. Indian streets with tree cover and narrow lanes will defeat nadir views (UrbanVGGT notes occlusion by trees and overhangs) |
| H2 | building and tree shadows in satellite images | building/tree heights, so shade at any hour on the footpath | H = L tan(e) with satellite sun angles from metadata | building height from shadows in high-res satellite images https://www.sciencedirect.com/science/article/pii/S0924271616301939 EXCERPT; deep learning object heights from shadows https://pmc.ncbi.nlm.nih.gov/articles/PMC10575158 EXCERPT | shade map where no street photo exists; the oil-tank trick pointed at trees |
| H3 | bare-soil lines in green or open land | desire paths at city scale | see D2 | HYPOTHESIS for automatic detection | candidate informal edges |
| H4 | waterlogging extent after rain (SAR sees through cloud) | flood-prone segments | SAR water is dark (specular away from sensor) | Ursa uses SAR for tanks (1.1) VERIFIED; urban flood SAR for footpaths: not searched this session | monsoon layer when it is cloudy (the 2024 oil paper's lesson: optical fails under cloud) |

---

## 4. Fusion: how the signals check each other (LUNAR-TIE M5, M10, M11)

| claim made about a segment | engine 1 | engine 2 | agree | disagree |
|---|---|---|---|---|
| photo time | EXIF DateTimeOriginal | shadow-time (A1) + daylight colour (E5) + leaf state month (E2) | trust the photo | flag "clock wrong or reused photo", lower weight |
| camera heading | EXIF/Mapillary compass | sun azimuth from shadows (A1, A2) | place detection on that side of the street | use the shadow heading; if no shadows, ask a human |
| kerb / step height | kerb shadow width x tan(e) (C4) | metric depth + ground plane (C4, C5), or Mapillary SfM points (F1) | publish height | "needs a human look" |
| footpath blocked by vehicles | parked vehicle detection now (D4) | kerb scuffs, bent bollards (D1), repeat photos (G1) | permanent-ish cost | one-off, decay cost |
| floods in monsoon | stain line height (B4) | crowd flood photos (B3), SAR (H4) | monsoon cost | keep both, show range |
| shade at 14:00 in May | street sky fisheye + sun path (A4) | satellite shadow heights (H2) | shade layer | lower confidence |

Negative information (Jim Simons frame, `IDEATION-LUNAR-TIE.md` L152): no hard shadows = overcast or night, so the shadow engines abstain and the condition tag says why; a segment with zero photos is "unknown", not "safe" (D2).

---

## 5. Where this sits against the brief

| brief item (WAVE-2-SC02-BRIEF.md) | rows that serve it |
|---|---|
| barrier classes: missing kerb ramps, steps, broken footpaths, poles, parked vehicles | C6, C4, C1, A3 (off-frame poles), D4 + D1 |
| map detection to the correct segment | A1/A2 heading, G2 triangulation, F1 SfM, E1 geolocation without GPS |
| any time / weather / month (D2) | A1 time, E2 month, F6 weather, E3 haze, E4/E5 night, B1-B4 water, G1 persistence |
| emotional hook (elderly, prams, wheelchairs, blind) | A4 shade for elderly, C7 tactile traps for blind, C8 open manholes, B4 "this floods every monsoon" |
| LUNAR-TIE moves (two detectors, refuse when unsure, own test data) | section 4, F4 abstain, sec. 2 two-engine sun check; own test data: render shadows of a known pole at known hours with the ephemeris (physics-made ground truth, LUNAR-TIE M6) |
| world models | G3 and A4 give a per-hour light simulation of the street; H2 heights give geometry for a 3D replay |

---

## 6. The 8 signals to demo tonight (ranked: striking x buildable on GTX 1650 4 GB)

| rank | demo | inputs | tools | output on screen | confidence 0-20 and why |
|---|---|---|---|---|---|
| 1 | **Shadow clock + compass**: one photo, its EXIF GPS/time; pvlib sun position; draw where shadows must point; compare | 1 phone photo from MUJ today | pvlib (installed in a uv env and run), GeoCalib optional | "photo time agrees with shadows within N min; camera faces 52 deg"; mismatch flag on a re-used photo | 16: math is COMPUTED and cross-checked; shadow bearing measurement on uneven ground is the risk |
| 2 | **The object outside the frame**: a pole/tree shadow crossing the footpath, caster not visible; H = L tan(e) | same photo set, one with an off-frame caster | the formula + manual or SAM 2 shadow mask | "a 4.3 m +-0.3 m object stands ~3 m east, outside this picture" with an arrow off the edge | 14: physics VERIFIED (Torralba), street automation HYPOTHESIS; needs a clean flat shadow |
| 3 | **Shade-hours map** for elderly: sky mask + sun path overlay per hour (Middel method) | 3-5 photos looking up or a Mapillary panorama | SegFormer/any sky segmentation + pvlib | per-segment bar "shaded 11:00-15:00 in May, exposed today at 15:00" and a shaded-route toggle | 15: method VERIFIED in literature; phone photos are not fisheyes, so coverage is partial |
| 4 | **Kerb height, two engines**: kerb shadow width x tan(e) vs Depth Anything V2 / Metric3D | photo of a kerb in sun | depth model (small fits 4 GB), pvlib | "kerb 15 cm (shadow) vs 17 cm (depth): agree, wheelchair cannot cross"; or "needs a human look" | 12: depth models are EXCERPT-level here; the 1.67x camera-height trap must be handled |
| 5 | **Dry-season photo predicts the monsoon**: stain/tide line on walls and shutters, height by known objects | 1 photo of a wall/shutter line | VLM prompt (Qwen2.5-VL 3B or API) + manual height ref | "water reached ~30 cm here; this segment closes to wheels in monsoon" | 11: USGS physics VERIFIED; no stain-line detector exists, porous walls overestimate |
| 6 | **Wet now + drainage score**: reflection/specular patch + rain on that date | photo after any rain, date | VLM yes/no prompt (BayFlood style) + Open-Meteo history | "standing water, 20 h after last rain: poor drainage" | 10: the drainage inference is HYPOTHESIS; needs a rain day |
| 7 | **Encroachment clock**: vendors / parked two-wheelers + shadow-time, and kerb scuffs as the "it happens even when empty" signal | 2+ photos of one stretch at different hours (or Mapillary sequence dates) | YOLO-World / Grounding DINO open-vocab | "blocked 17:00-22:00 by carts; scuffed kerb: vehicles mount here" and route changes by hour | 12: detection is easy; scuff detection is HYPOTHESIS |
| 8 | **The photo knows where it is**: script + STD code + plate state code with GPS removed | a WhatsApp-forwarded photo | IndicPhotoOCR (MIT) | "Devanagari + 0141 + RJ-14: Jaipur, UI switches to Hindi", plates blurred | 13: OCR toolkit EXCERPT-level; lookups are simple tables |

Decision tree for the build lead (confidence per node, 0-20):

```
start: do we have photos with intact EXIF? (MUJ own phone photos: yes)          [18]
 ├─ yes ─► demo 1 shadow clock (needs sun, today 16:24 IST: sun still up)        [16]
 │         └─ shadows clean on flat paving? ─ yes ─► demo 2 off-frame object      [14]
 │                                          └ no ──► skip 2, keep 1 as heading only
 │         ─► demo 3 shade hours (sky segmentation works on phone photos)         [15]
 │         ─► demo 4 kerb two-engine (one sunlit kerb photo)                      [12]
 ├─ no (Mapillary/forwards) ─► demo 8 geolocate by script; Mapillary fields      [13]
 └─ any photo ─► demos 5-7 via VLM prompts, shown with "HYPOTHESIS" badge       [10-12]
```

Time note: sunset at MUJ Jaipur today is about 17:50 IST (pvlib minute scan; sun elevation 10.4 deg at 17:00 and 7.1 deg at 17:15, COMPUTED). Shadows get very long and soft below ~10 deg, so any new sunlit shadow photos for demos 1, 2 and 4 should be taken before ~17:00. Otherwise use photos already on the phone with EXIF intact.

---

## 7. Red-team of this file (I tried to prove it wrong)

| claim | grade | why |
|---|---|---|
| Orbital Insight used floating-roof shadows for oil inventory | VERIFIED | WIRED + J. Financial Markets 2024 text read |
| Ursa 0.98 correlation with EIA Cushing | VERIFIED as Ursa's own marketing claim | self-reported, not independent |
| Shadow tables and tropic flip | VERIFIED (COMPUTED, 2 engines) | pvlib and own script agree within 0.3 deg elev, 1.2 deg az |
| "Kolkata ~22.6 N" and the list of cities below the tropic | UNVERIFIED | latitudes from memory, not looked up this session; Hyderabad and Bengaluru are well south, Kolkata is close to the line |
| Shadows reveal off-frame objects | VERIFIED for the physics (Torralba 2012) | street-scale automatic use is HYPOTHESIS |
| 1.67x width inflation from wrong camera height | VERIFIED as arithmetic, mechanism VERIFIED (UrbanVGGT: linear bias in assumed height) | the 1.5 m phone height itself is an assumption |
| Mapillary `computed_compass_angle` is often zero | EXCERPT, one developer's code comment | could be outdated |
| SLNP 1.31 crore LEDs by June 2024 | EXCERPT | PIB page not opened |
| RDD2022 India subset details, Tile2Net accuracy | EXCERPT | not opened |
| Kerb scuffs measure mounting rate | HYPOTHESIS | no paper found; behaviour itself VERIFIED as common (Bengaluru case counts) |
| Stain line predicts monsoon depth | HYPOTHESIS for the detector, VERIFIED for the physics (USGS) | porous wicking overestimates (USGS says so) |
| Lamp colour reveals retrofit status | HYPOTHESIS | sodium vs LED colour difference is common knowledge but not sourced here |
| EV formula for light level | UNVERIFIED (no source fetched) | standard photography formula, written from memory |
| Car mix predicts Indian income | HYPOTHESIS | Gebru is US-only; two-wheeler-dominant traffic may break it |
| Demo confidence scores | UNVERIFIED | my estimates, nothing built yet |

Possible over-claim to watch: the off-frame height needs the caster's base position; with only one photo you get height x distance, not height alone, unless the base is found on the map or in a second photo. Section 2.3 and row A3 say so; the demo copy must say so too.

---

## 8. Coverage audit and gaps

Files read this session:

| file | bytes (`wc -c`) | read |
|---|---|---|
| research/WAVE-2-SC02-BRIEF.md | 4,903 | full |
| DECISIONS.md | 1,892 | full |
| ~/sih-idea/05-FACTOR-SPACE-UNIVERSE.md | 7,537 | full |
| method/IDEATION-LUNAR-TIE.md | 44,573 | sections 2-3 only (L143-263), as asked; rest not read |
| method/IDEATION-SOLAR.md | 43,016 | section 2.1-2.3 (L90-175), as asked; rest not read |

Searches run: 28 web_search calls (each 2-3 queries) and 5 web_fetch batches (22 URLs, 0 errors).

Gaps (named, not hidden):
- No search for SAR urban flood mapping of footpaths (H4), PRNU on phone photos (F5), slanted-edge MTF on street images (F4), wheelchair vibration vs surface roughness (C2). Each is marked HYPOTHESIS.
- No Indian dataset found for kerb scuffs, stain lines, desire paths, tactile paving or night street photos. Closest Indian sets: Pune footpath damage (VERIFIED), IDD (EXCERPT), RDD2022 India (EXCERPT), Bharat Scene Text (EXCERPT).
- Place Pulse 2.0 original paper (Dubey et al. 2016) not fetched; only a downstream study.
- Dark channel prior original (He et al.) not fetched; only cited by the PM2.5 papers.
- Zero-result notes: no paper found that infers vendor operating hours from one photo; none that detects tyre marks on kerbs; none that reads flood stain lines automatically from street photos.

Scratch artefacts: `/tmp/claude-1000/-home-liebert511/cc043658-cf6e-4a18-9856-e8de7ef64a10/scratchpad/sc02/sun.py` (own ephemeris + tables), `check_pvlib.py` (second engine).
