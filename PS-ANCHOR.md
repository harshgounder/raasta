# PS-ANCHOR: what SC-02 actually asks, and the check against straying (claude, 2026-10-24 ~17:05 IST)

Every agent reads this before adding anything. If a feature does not trace to a row here or to a rubric row, it is an EXTRA and goes after the core works.

## 1. The statement, clause by clause (verbatim from PROBLEM-STATEMENTS.md)

| # | clause | what we must SHOW | component | proof on stage |
|---|---|---|---|---|
| C1 | "detects accessibility barriers in street-level images" | barriers found in real Indian street photos | /analyze: detector A + B + judge | upload any photo -> boxes + labels |
| C2 | barrier list: "missing kerb ramps, steps and stairs, broken or missing footpaths, poles obstructing movement, and parked vehicles blocking footpaths" | ALL five classes covered (plus Indian extras as a bonus) | label set = these 5 first | a test image per class |
| C3 | "maps them to the correct footpath segments" | each detection placed on a specific segment of a footpath network, not just a map pin | /analyze place step: GPS + heading + side -> segment probability | click a barrier: its segment highlights |
| C4 | "Detections must be matched to the correct segment of the footpath network" | a footpath NETWORK exists (OSM footways; where India has none, generated sidewalk segments along roads) | graph builder | the network drawn on the map |
| C5 | "plans routes that avoid them" | routing on that network with barrier costs | /route | shortest route vs accessible route |
| C6 | "Project Sidewalk provides labelled examples from other countries, but Indian streets differ, so **teams must label their own local images as well**" | OUR OWN labelled Indian images (from online sources now, since no photo walk) with a measured score | labelling task + eval script | "we labelled N Indian images; precision/recall per class = X" |
| KC1 | "Detecting small barriers in varied street images" | small things (kerb edges, poles, bollards) + variety (night, rain, cities) | detectors + condition router | results split by condition |
| KC2 | "Matching detections to the correct map segments" | the C3 method with its error | place step + uncertainty cloud | wrong-side example handled |
| KC3 | "Planning routes on footpath networks with barrier-related costs" | profile costs (wheelchair, walker, pram) | /route cost model | route changes with profile |

## 2. Rubric (Unstop): innovation, problem understanding, technical feasibility, impact, scalability, presentation quality

| rubric | where we score it |
|---|---|
| problem understanding | Indian chaos factor universe, the two conflicting standards (1:12 vs 1:15), "never says safe" |
| technical feasibility | the live photo -> receipt -> route demo working on any uploaded photo; measured eval on our labelled set |
| innovation | shadow altimetry + 3-route height, two-detector agreement + abstain, time-of-day blockage, multi-perspective story |
| impact | 2.68 crore persons with disabilities (Census 2011), 36,526 pedestrian deaths in 2024 (MoRTH, to verify), trips-not-taken, scar ledger |
| scalability | any city with OSM, any online image source, crowd uploads, condition router |
| presentation | santioni-level site + YC deck |

## 3. The core vs the extras (build order)

**CORE (never cut, must work first):** C1 + C2 on real Indian photos; C3/C4 a footpath network and segment matching; C5 accessible vs shortest route; C6 our own labelled Indian test set with a real score.
**STRONG EXTRAS (after core):** kerb height with error bar (3 routes); ABSTAIN demo; leave-time routing; scar ledger; trips-not-taken; Hindi complaint; multi-perspective story site.
**NICE EXTRAS (only if time):** 3D/world-model "switch body" view; same-kerb-different-sky simulation; shadow clock; wall-stain flood depth; F1 pit wall styling; voice guidance.

## 4. Where we are drifting right now (claude's honest check, 17:05)
1. **C6 is at risk.** The user cannot take photos, so "label our own local images" must be done on online Indian images (Commons, Mapillary, YouTube frames, Reddit). We need a small labelled set (target 60-100 images, all 5 classes) and a real precision/recall number. Nobody owns this yet: **claude owns it now** (helper labels with a VLM pre-label + claude review, or the user reviews 15 minutes if possible).
2. **C4 network:** Indian OSM often has no sidewalk geometry. Without a footpath network, C3/C5 are just road routing. Fix: build sidewalk segments both sides of roads (offset) where OSM lacks footways, and say so.
3. **Research volume vs build:** 17:05 and no build started. Wave 2 research is enough for the core. Build starts now; research continues only for extras.
4. **World models and robotics** are EXTRAS unless a found item directly does C1/C3/C5 better (e.g. a traversability model as detector B).
