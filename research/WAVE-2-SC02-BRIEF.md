# WAVE 2 BRIEF: SC-02 deep research (v1, 2026-10-24 ~15:20 IST, claude/lead)

**The user picked SC-02: Accessible Walking Routes from Street Imagery.** (DECISIONS.md D1.) Every lane now works on SC-02 only.
Deadline reality: judging starts **03:00 IST**, freeze **02:30**. Wave 2 closes **16:45**; build starts ~17:00.

## The statement (verbatim core)
Detect accessibility barriers in street-level images (missing kerb ramps, steps and stairs, broken or missing footpaths, poles obstructing movement, parked vehicles blocking footpaths), map each detection to the correct footpath segment, and plan routes that avoid them. Project Sidewalk has labelled examples from other countries; Indian streets differ, so teams must label their own local images too.
Key challenges: small barriers in varied images; matching detections to the right map segment; routing on footpath networks with barrier costs.

## What the user wants on top (in force)
1. **Emotional + mass appeal:** elderly people, wheelchair users, parents with prams, people on crutches, the blind. A common person must feel "this helps everyone".
2. **Super flashy:** santioni-level website (character, story, sound, WebGL), the demo inside it.
3. **F1 total-intelligence method** (method/COPYPASTE-METHOD.md): map the problem through every lens before building (physics of a wheelchair, human body, regulation, weather, time of day, economics, history, adversaries), then D minus A.
4. **LUNAR-TIE image moves** (method/IDEATION-LUNAR-TIE.md section 3): two independent detectors that must agree (agreement = confidence), several images of the same spot agreeing, make our own test data, refuse when unsure ("needs a human look"), one before/after picture.
5. **World models:** generative / 3D models of the street (walk the route before you go, simulate a barrier, reconstruct a crossing in 3D, predict how a spot looks in monsoon).
6. **Fork, do not build:** find the best existing projects and merge them.

## Lanes

| lane | owner | deliverable (write as you go) |
|---|---|---|
| S1 code/models/data | **dsh** (sub-fleet unlimited; you may download, run and test code) | `research/dsh/sc02/` : candidates table + raw JSON per host. Cover: (a) street imagery sources with India coverage + API terms (Mapillary API v4, KartaView, Google Street View Static/metadata, Bhuvan, own phone photos), check coverage around MUJ Jaipur (lat 26.84, lon 75.56 approx; verify) ; (b) barrier detection: Project Sidewalk ML repos, curb-ramp detectors, Grounding DINO, YOLO-World, OWLv2, Florence-2, SAM 2, small VLMs (Qwen2.5-VL 3B etc.), sidewalk segmentation (Mapillary Vistas, Cityscapes, **IDD India Driving Dataset**, SegFormer/Mask2Former); (c) depth for step height (Depth Anything V2, Metric3D); (d) mapping detections to footpath segments (OpenSidewalks schema, OSM footways, Project Sidewalk geolocation, map matching); (e) routing with barrier costs (OSMnx, AccessMap, OpenTripPlanner wheelchair, Valhalla pedestrian costing, pgRouting, GraphHopper); (f) world models / 3D (Gaussian splatting from street images, nerfstudio, VGGT, MASt3R, DUSt3R, image-to-video models for "walk-through"); (g) the Chandigarh paper arXiv 2602.09216 code/data. For the top 3 of each class: download + run a smoke test on 3 images, record time on this box (GTX 1650 4 GB, 7 GB RAM). |
| S2 domain + people + regional | **hermes** (NO code) | `research/hermes/sc02/` : (a) F1-style lens map of SC-02: wheelchair physics (max ramp slope, kerb heights, surface roughness, width), Indian standards (MoHUA Harmonised Guidelines, IRC:103 pedestrian facilities, RPwD Act 2016, Accessible India Campaign / Sugamya Bharat), weather (monsoon), time-of-day (vendors, parking), economics; (b) India numbers: disabled population, elderly population, pedestrian deaths, footpath encroachment news (Jaipur especially), with URLs; (c) real human stories (named only if public) for the emotional hook; (d) competitor products (Google Maps wheelchair routes in India?, Wheelmap, AccessNow, Evelity, Sugamya Bharat app) and what they miss; (e) 10 common-person what-if questions with how the demo answers; (f) forums/regional sources (Reddit r/disability r/india, Indian disability orgs, Zhihu/CSDN on 无障碍 routes, Japan バリアフリー route apps, Korean 휠체어 경로). |
| S3 Parallel deep research | **claude** | 3 ultra runs: fork landscape incl. world models; India accessibility domain + stories; technical stack (map matching + routing costs + step height). |
| S4 architecture + site story | **claude** | `ARCHITECTURE.md`, `SITE-STORY.md` |
| S5 art + checks | **codex** after 16:28 | character + scene art (GPT-Image-2.5), verdicts on every artifact |

## Rules
Same as wave 1: every claim URL + fetched time, VERIFIED/UNVERIFIED, never narrow scope, log zero-result sources, reasons not verdicts, no em dashes, no AI-tell words. claude rechecks everything.
