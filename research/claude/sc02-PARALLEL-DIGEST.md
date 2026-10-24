# SC-02 Parallel digest (FORK, DOMAIN, TECH)

For: SC-02 lead architect. Accessible walking routes from street images, all of India. Website demo due 02:30 IST, 25 Oct 2026.
Written: 2026-10-24 ~16:45 IST by Claude Code from three Parallel `ultra` deep-research runs, all read to the last line.

| Report | Run id | Saved verbatim at | Bytes / lines | Read |
|---|---|---|---|---|
| FORK | trun_3b693d434bb94e6d96d0a999fe5a4730 | `sc02-parallel-FORK.md` | 89,832 / 487 | lines 1-487 |
| DOMAIN | trun_3b693d434bb94e6db887b33ded0ba06b | `sc02-parallel-DOMAIN.md` | 41,115 / 361 | full (inline result) |
| TECH | trun_3b693d434bb94e6d87726663222684a7 | `sc02-parallel-TECH.md` | 53,793 / 687 | lines 1-687 |

**Grades used below.** `RV` = the report itself labels it verified (DOMAIN's "verified figure" tables). `U` = UNVERIFIED: stated by a report with a citation, not re-checked by me. `C` = computed by me from the report's numbers. `ME` = my inference, not in any report. No licence, URL, star count or model was opened or install-tested by me. FORK states plainly that nothing was install-tested on any hardware.

**Scope warning first.** All three reports shrink the problem to one small reviewed area (FORK and DOMAIN: a Jaipur corridor/neighbourhood; TECH: "a small selected campus area"). SC-02 says all of India. The architect has to own that gap: demo one verified corridor, and show the India-wide path as data plumbing (OSM India extract + open imagery + the same per-edge evidence model), labelled as not yet run. `ME`

---

## 0. One-screen answer

```
street photo (team-owned / Mapillary CC-BY-SA)
   |
   v
[detect]  YOLO-World-S (Ultralytics, AGPL) + 2nd model (OWLv2 or Grounding DINO)   -> boxes, "unsure" if only one model fires
   |
   v
[mask]    SAM 2.1 tiny box-prompted (optional) or reviewer-drawn corridor          -> obstacle footprint vs footpath
   |
   v
[depth]   Depth Anything V2 Metric Small (vkitti, max_depth=80)                     -> metres, height shown as "unknown" unless measured
   |
   v
[locate]  pose sidecar + ray projection + candidate edges (30 m radius) + 1-click human reassign
   |
   v
[graph]   OSMnx walk graph (simplify=False, retain_all=True, extra tags) + hand-fixed two-sided footpaths + explicit crossings
   |
   v
[route]   NetworkX Dijkstra on own edge_cost(); hard exclusions first; "No verified route" allowed
   |
   v
[web]     MapLibre + deck.gl (PathLayer, TripsLayer, ScatterplotLayer) ; evidence card per barrier
[3D]      optional only: photo walkthrough; Splatfacto needs ~6 GB, so not on the 4 GB laptop
```

Recommended stack is near-identical across FORK and TECH, except the detector pick (see section 4, contradiction C1).

---

## 1. FORK report

### 1.1 Recommended fork-merge stack (FORK section 8, "minimum architecture")

| Layer | FORK's choice tonight | Merge contract (fields to carry) | Fallback |
|---|---|---|---|
| Images | Team-owned Jaipur photos; permitted Mapillary if coverage works | image ID, licence/attribution, capture time, GPS, heading, camera type | preloaded reviewed gallery |
| Vision | Grounding DINO **or** Florence-2-base; optional small YOLO | boxes/masks, class, confidence, model/version, original image dims | precompute detections; keep upload + human review live |
| Footpath masks | segmentation checkpoint only if already working; optional SAM | mask/polygon + confidence, not a passability claim | reviewer-drawn corridor and obstacle footprint |
| Geography | OSMnx/OSM + manually reviewed two-sided footpaths and crossings | stable edge IDs, explicit connections | small authored GeoJSON graph |
| Barrier association | candidate edge + correction control | observation ID -> edge ID/interval, reviewer, confidence, timestamp | manual edge assignment |
| Routing | CPU shortest path, own weights; Unweaver only if its example runs fast | profile, excluded edges, penalties, explanation, geometry | preloaded graph, live reroute on barrier toggle |
| Web | MapLibre; deck.gl only where it simplifies | route, candidates, evidence cards, attribution | plain GeoJSON layers |
| Optional preview | real-image stepping; small precomputed splat | observed vs synthetic kept separate | omit video generation |

FORK's final line: "MapLibre + OSMnx/custom pedestrian graph + Grounding DINO or Florence-2 + a human correction panel + explicit CPU routing costs." Postpone 3D/world models. `U`

FORK demo cost model (its own proposal, "not a published safety standard"):
`edge_cost = length * preference_multiplier + surface_penalty + obstruction_penalty + uncertainty_penalty`, hard exclusions applied first.

### 1.2 Top candidates per class (as FORK states them; all `U`)

"Runs where": C = CPU, G = 4 GB GPU, B = browser. Y = documented, E = FORK's engineering guess, ? = unknown, UI = browser display only.

**Detection**

| Candidate | URL | Licence | Code push / date | Stars or downloads | Runs where |
|---|---|---|---|---|---|
| Grounding DINO | github.com/IDEA-Research/GroundingDINO | Apache-2.0 | 2024-08-12 | 10,701 stars | C: Y (documented CPU mode); G: ?; B: UI |
| YOLO-World (AILab-CVC) | github.com/AILab-CVC/YOLO-World | GPL-3.0 | 2025-02-26 | 6,588 | C: E; G: E small, untested; B: ? |
| Ultralytics (YOLO26/YOLO-World wrapper) | github.com/ultralytics/ultralytics | AGPL-3.0 (commercial separate) | 2026-10-23 | 62,771 | YOLO26n det 2.4M params, **38.9 ms CPU ONNX**; YOLO26n-seg 2.7M, **53.3 ms CPU ONNX** (Ultralytics' own figures, CPU model unstated) |
| OWLv2 base ensemble | huggingface.co/google/owlv2-base-patch16-ensemble | Apache-2.0 | model June 2023 | 1,668,866 downloads/month | C: E slow; G: ? |
| Florence-2-base | huggingface.co/microsoft/Florence-2-base | MIT | U | 2,922,384 downloads/month | C: Y fallback; G: E |
| RampNet (curb-ramp specialist) | github.com/ProjectSidewalk/RampNet | MIT code, imagery rights separate | 2026-10-22 | 9 | C: Y setup; G: ? |
| sidewalk-tagger-ai | github.com/ProjectSidewalk/sidewalk-tagger-ai | Apache-2.0 | 2026-10-16 | 0 | tag/severity classifier, not a detector |
| Small VLMs: Qwen2.5-VL-3B (4B params, 2,021,924 dl/mo, licence not stated), moondream2 (Apache-2.0, 2B, release 2025-06-21, 2,320,743 dl/mo, has detect + point), SmolVLM-256M (Apache-2.0, 0.3B, **under 1 GB GPU RAM** per card, no detection) | HF cards | as listed | as listed | as listed | explain evidence only, never geometry |
| transformers.js | github.com/huggingface/transformers.js | Apache-2.0 | U | U | browser inference: WASM CPU default, WebGPU experimental |

**Segmentation**

| Candidate | URL | Licence | Date | Popularity | Runs where |
|---|---|---|---|---|---|
| SAM 2 | github.com/facebookresearch/sam2 | Apache-2.0 | 2026-05-30 | 20,051 | C ?, G ?; prompted masks, no class names |
| segments/sidewalk-semantic (data) + SegFormer B0/B1/B4 fine-tunes | huggingface.co/datasets/segments/sidewalk-semantic | **cc-by-nc-4.0** | updates 2022-2025 | 118 dl last month | Belgium 2021 images, 35 classes, 324 MB, not Indian |
| Mapillary Vistas (data) | mapillary.com/dataset/vistas | **CC BY-NC-SA** (differs from ordinary Mapillary CC-BY-SA) | U | U | data only |
| India Driving Dataset (IDD) | idd.insaan.iiit.ac.in | U, get official terms | U | 10,000 images, 34 classes, 182 sequences | data only; Indian appearance, not accessibility labels |
| Tile2Net | github.com/VIDA-NYU/tile2net | BSD-3-Clause | 2026-09-12 | 231 | **aerial orthophotos only**, CUDA required, 4 GB ? |
| tactile-path-segmentation | github.com/JezZh/tactile-path-segmentation | none stated | 3 commits | 0 | SegFormer-B0, no weights/data shipped; Jetson Nano 1.70 FPS, RTX 3090 ~116 FPS |
| navblind/Sidewalk-semantic-seg | github.com/navblind/Sidewalk-semantic-seg | U | U | 12 | old baseline |
| IDD community code | github.com/IshanKuchroo/IDD-Indian-Driving-Dataset, github.com/Mohitasudani/idd_lite_segmentation | U | U | U | baseline leads only |

**Depth**

| Candidate | URL | Licence | Date | Popularity | Runs where |
|---|---|---|---|---|---|
| Depth Anything V2 | github.com/DepthAnything/Depth-Anything-V2 | code + **Small Apache-2.0**; Base/Large/Giant **CC-BY-NC-4.0** | 2026-03-24 | 9,020 | C: E small; G: E small; B: Transformers.js path documented |
| Metric3D | github.com/YvanYin/Metric3D | BSD-2-Clause code, check checkpoints | 2025-03-13 | 2,336 | ?; needs correct focal length |
| UniDepth | github.com/lpiccinelli-eth/UniDepth | **CC BY-NC 4.0** | V2 2025-02-28, push 2025-05-18 | 1,273 | ? |
| UrbanVGGT (paper, sidewalk width) | arxiv.org/pdf/2603.22531 | none shown | "19 Aug 2026" | none | method only; widths 0.56-3.94 m; ~300 GSV images; 1,931 measurements on 527 OSM segments (NYC, Sao Paulo, Nairobi); assumes 2.5 m camera height |

**Geolocation / map matching**

| Candidate | URL | Licence | Date | Popularity | Note |
|---|---|---|---|---|---|
| label-latlng-estimation | github.com/ProjectSidewalk/label-latlng-estimation | **no licence established** | 2026-09-03 | 1 | **1.47 m median test error** in its own eval; calibration is GSV-specific |
| OpenSidewalks-Schema | github.com/OpenSidewalks/OpenSidewalks-Schema | no standard licence identified | 2026-10-20 | 63 | crossings do not auto-connect; explicit connection rules |
| fmm | github.com/cyang-kth/fmm | Apache-2.0 | created 2017-10-27 | 1,055 stars | HMM GPS-trace matching, C++/OpenMP; raw OSM input removed, use osmnx shapefile |
| leuvenmapmatching | github.com/wouterbohets/leuvenmapmatching | U | U | U | trace matching, does not locate a seen obstacle |

**Routing**

| Candidate | URL | Licence | Date | Stars | Wheelchair facts FORK quotes |
|---|---|---|---|---|---|
| OSMnx | github.com/gboeing/osmnx | MIT | 2026-07-31 | 5,877 | graph scaffolding |
| openrouteservice | github.com/GIScience/openrouteservice | GPL-3.0 | U | U | wheelchair `profile_params.restrictions`: `maximum_incline` 3/6 (default)/10/15/any %, `maximum_sloped_kerb` 0.03/0.06 (default)/0.1/any, `minimum_width`, `surface_type` default `cobblestone:flattened`, `smoothness_type` default `good`, `avoid_features: steps` |
| OpenTripPlanner | github.com/opentripplanner/OpenTripPlanner | U | 2026-10-14 | 2,755 | `maxSlope` default **0.083**, `stairsReluctance` 100, `inaccessibleStreetReluctance` 25, unknown-access cost 600, inaccessible 3600 |
| Valhalla | github.com/valhalla/valhalla | MIT | 2026-10-19 | 6,355 | steps factor default 8 (0.1-100000), avoid-bad-surfaces default 0.25, linear cost factors on GeoJSON LineStrings |
| GraphHopper | github.com/graphhopper/graphhopper | Apache-2.0 | 2026-10-07 | 6,726 | custom models; no turnkey wheelchair profile assumed |
| pgRouting | github.com/pgRouting/pgrouting | mostly GPL-2.0+ | 2026-09-27 | 1,435 | inside PostGIS |
| AccessMap + Unweaver | github.com/TaskarCenterAtUW/AccessMap, /unweaver | U (LICENSE file, type unstated) | 2026-10-14 | 2 | closest architecture reference; Unweaver sample sidewalk data must be requested from the authors |
| Routino | routino.org/software | AGPL-3.0+ | v3.4.4 | U | no wheelchair routing stated |
| wheelchair-pathfinder | github.com/lengvietcuong/wheelchair-pathfinder | none stated | 29 commits | U | toy A*, Central Park, 23 nodes / 40 segments |

**3D / world models (all off the critical path)**

| Candidate | Licence | Hardware as stated | FORK verdict |
|---|---|---|---|
| nerfstudio (Apache-2.0, 12,010 stars) + gsplat (Apache-2.0, 5,803) | Apache-2.0 | CUDA required, 4 GB ? | small overlapping capture of one junction only |
| VGGT (14,497 stars) | original noncommercial, commercial variant differs | ? | pose/geometry bootstrap |
| MASt3R / DUSt3R | CC BY-NC-SA 4.0 | ? | overlapping images only |
| HunyuanWorld-Voyager | custom Tencent licence | **60 GB min at 540p, 80 GB recommended** | stretch only |
| Wan2.2 | Apache-2.0 | I2V **80 GB**, TI2V-5B **24 GB** | pre-render only |
| LTX-Video | Apache-2.0 + OpenRail-M | repo claims "only 1 GB of VRAM" | pre-render teaser, verify |
| HunyuanWorld-Mirror | License.txt, code unstated | CPU fallback in example | geometry candidate |
| Qwen-Image-Edit | Apache 2.0, 20B BF16 | VRAM unstated | monsoon illustration, label synthetic |

**Web viz**

| Candidate | Licence | Date | Stars | Use |
|---|---|---|---|---|
| MapLibre GL JS | 3-Clause BSD | 2026-10-11 | 11,852 | basemap + GeoJSON |
| deck.gl | MIT | 2026-10-11 | 14,652 | route, evidence, uncertainty layers |
| Potree | unstated | 2026-01-08 | 5,645 | real point clouds only |
| GaussianSplats3D | MIT | 2025-10-19 | 2,919 | optional splat tab |
| SuperSplat | MIT | 2026-10-05 | 10,313 | crop/clean splat |

**Imagery sources (FORK section 3)**

| Source | Terms | Verdict |
|---|---|---|
| Team-owned photos | contributor permission, blur bystanders | best fallback |
| Mapillary API v4 | imagery **CC-BY-SA** with attribution, token auth | check exact demo area coverage first |
| KartaView | software MIT, imagery **CC BY-SA 4.0**, credit "(c) Grab and KartaView Contributors" | backup; Jaipur coverage not established |
| Google Street View Static | proprietary; no prefetch/cache; policy updated **2026-10-21**; Maps terms ban use to **train, test, validate or fine-tune** AI | do not bulk-pull or use for validation |
| Bhuvan/NRSC | API-specific conditions; no street panoramas described | basemap/context only |

Regional and hackathon leads FORK lists (all "candidate only"): ChelseaGH/sidewalk_prototype_AI_Hub (Korean SideGuide, ROS + YOLOv3 + PSMNet, CUDA), CMU-cabot/cabot-navigation (MIT, robot), yrmi99/SeoulElevatorGuide (metro elevators), Devpost PathAble (2025-03-01, no repo), AccessGrid AI (2026-05-29, github.com/Ramachandranram4/AccessGrid-AI), AccessMapAI (HackDavis 2026, github.com/adiseshvsanklapur/AccessMapAI, has a mock mode). No prize confirmed for any. "SidewalkNet" as a real licensed artifact: not established. Gitee/GitCode/ModelScope: nothing task-specific verified.

### 1.3 Chandigarh paper (FORK section 1)

| Field | Detail (`U`) |
|---|---|
| Title | "Towards Human-AI Accessibility Mapping in India: VLM-Guided Annotations and POI-Centric Analysis in Chandigarh" |
| ID / date | arXiv **2602.09216v2**, 17 Feb 2026 |
| Authors | Varchita Lalwani, Utkarsh Agarwal, Michael Saugstad, Manish Kumar, Jon E. Froehlich, Anupam Sobti |
| Method | adapts Project Sidewalk's human annotation UI; VLM is **gemini-2.5-flash**, fed OSM road type + first and last Street View panorama of a segment, writes mission guidance for human annotators. Not an autonomous detector, not a router |
| Taxonomy changes | "Curb Ramp" -> **"Curb Style"**; 3 severity levels kept; adds **vendors, drainage channels, parked two-wheelers, construction debris**; surface adds **loose brick, mud, unpaved shoulders**; splits **absent** vs **unusable** pedestrian space |
| Scope | ~**40 km**, **3 sectors**, ~**230 POIs**, **1,644 improvement locations**; kept paths with at least **75%** overlap with Street View coverage |
| Evaluation | **50 segments x 3 annotators = 150 ratings** per criterion. Relevance **4.97/5** (SD 0.26), Accuracy **4.40/5** (SD 0.71), Usefulness **4.61/5** (SD 0.70); abstract says **4.66/5 overall** |
| Finding | education and transport POIs scored lowest |
| Code / data | no dedicated public repo for the India fork found; no licensed Chandigarh data release found |
| Use tonight | copy the taxonomy and the POI-centred audit view; do not cite the ratings as detection accuracy |

### 1.4 FORK's three technical risks

1. **Wrong-side localisation and broken pedestrian topology.** Mitigation: reviewed two-sided edges, explicit crossing nodes, candidate assignments, manual correction; nearest road is not the correct footpath.
2. **Domain shift and false geometric certainty** (Jaipur surfaces, drains, vendors, two-wheelers; monocular depth smooths small kerbs). Mitigation: India taxonomy, review every image shown in the demo, split temporary vs infrastructure, occluded or uncalibrated stays unknown.
3. **Missing, stale or impermissible imagery plus integration/compute failure.** Mitigation: team-owned fallback photos, capture dates with expiry, precomputed outputs, small local graph, no heavy world model live.

---

## 2. DOMAIN report

### 2.1 Every India number, with source and date

| # | Number | What it is (and is not) | Source, date | Grade |
|---|---|---|---|---|
| 1 | **2.68 crore (26.8 million), 2.21%** | persons with disabilities, Census 2011. Not a 2026 count | Census of India 2011 disability data (UNSD deck) [3] | RV |
| 2 | **5.4368 million** | Census 2011 "In Movement" disability. Not "wheelchair users" | same [3] | RV |
| 3 | **2.2%** overall, rural **2.3%**, urban **2.0%** | NSS 76th round, Jul-Dec 2018, released 23 Nov 2019 | NSO Report No. 583; PIB 23 Nov 2019 [16][20] | RV |
| 4 | electric wheelchair **2.1%**, manual **9.8%** | share among locomotor-disabled people **who acquired an aid**. Not national wheelchair prevalence | NSS Report 583 [20] | RV |
| 5 | **149 million aged 60+, 10.5%** | as of 1 July 2022 | UNFPA/IIPS India Ageing Report 2023 [4] | RV |
| 6 | **347 million, 20.8%** by 2050 | projection | same [4] | RV |
| 7 | **~230 million, ~15%** by 2036 | projection | PIB, 28 Oct 2025 [13] | RV |
| 8 | **153 million** elderly | reference year not stated, do not use as 2026 count | UNFPA India article, 23 Dec 2023 [40] | RV (as caveat) |
| 9 | **36,526 pedestrian deaths = 20.6% of 177,175** road deaths | all reported pedestrian deaths 2024. Not "caused by footpaths" | MoRTH, Road Accidents in India 2024 [7] | RV |
| 10 | **15,418 pedestrian injuries, 4,328 pedestrian deaths** | million-plus cities subset only, 2024 | same [7] | RV |
| 11 | Jaipur **860 road deaths 2024**, **849 in 2023** | all road users, not only pedestrians | same [7] | RV |
| 12 | Jaipur change 2023->2024: **+11 deaths, +1.3%** | computed from row 11 | me | C |
| 13 | **22.9%** falls | LASI Wave 1 elderly fact sheet, fieldwork 2017-18; recall period not stated, not annual, not street falls | IIPS/MoHFW LASI W1 [15] | RV |
| 14 | Accessible India: **1,671** buildings audited, **1,314** funded for retrofit, **1,748** govt buildings with features (different cohorts, do not divide) | progress as of 2 Dec 2024 | PIB 2 Dec 2024 [1] | RV |
| 15 | **709** fully + **4,068** partially accessible rail stations | 2 Dec 2024 | PIB [1] | RV |
| 16 | **8,695** fully + **42,348** partially accessible buses | 2 Dec 2024 | PIB [1] | RV |
| 17 | **95** central + **676** state websites accessible, **476** state live | 2 Dec 2024 | PIB [1] | RV |
| 18 | Original AIC targets: 50 buildings in 50 cities by Jul 2016; 50% govt buildings in capitals by Jul 2018; 50% rail stations by Mar 2018; 10% govt buses by Mar 2018; 50% govt websites by Mar 2017 | campaign launched 3 Dec 2015 | Rajya Sabha reply 26 Jul 2018 [26] | RV |
| 19 | Govt consultation still citing gaps and data needs | 9 Oct 2026 | PIB [8] | U |
| 20 | Karnataka: **21 smart-road projects in 7 smart cities** without tactile tiles | Karnataka, not Jaipur | CAG Report No. 11 of 2025 [24] | RV |

DOMAIN's suggested main slide: **2.68 crore (Census 2011)**, **347 million older people projected by 2050**, **36,526 pedestrian deaths in 2024**. Caveats in speaker notes.

Not established anywhere in DOMAIN: a current all-India wheelchair-user count, a Jaipur-wide % of broken footpaths, any deaths attributable to footpath condition.

### 2.2 Laws and standards, exact clauses

**RPwD Act 2016** [11] (`RV`)

| Section | Requirement |
|---|---|
| **40** | Central Govt to frame accessibility standards for physical environment, transport, ICT, services |
| **41** | measures for accessible transport, facilities **and roads** |
| **42** | accessible information, communication and technology, accessible formats, universal design (so the website itself must be accessible) |
| **44** | building permission and completion/occupancy certificates tied to accessibility compliance |
| **45-46** | timelines for existing public buildings and service providers, linked to notification of rules (not from the Act's passage date) |

**MoHUA Harmonised Guidelines 2021 vs IRC:103-2022** [5][27][29] (`RV`)

| Element | MoHUA HG 2021 | IRC:103-2022 (2nd revision) | IRC:103-2012 |
|---|---|---|---|
| Clear width | min **1,200 mm**; **1,800 mm** two-way | min **2 m** clear walking zone (two wheelchairs pass) | U |
| Kerb height | discusses kerbs up to **200 mm** (not a climbable allowance) | footpath kerb **150 mm** | U |
| Kerb-ramp gradient | not steeper than **1:12** | not steeper than **1:15** | **1:12** |
| Surface / crossfall | slip-resistant, flush road transition | crossfall **1:50 to 1:100** | U |
| Rest | walkways over **60 m**: rest/street furniture every **30 m** | seating with backs, armrests, shade | U |
| Older pedestrian speed | U | U | design value **~0.79 m/s** |

Conversions (C): 1:12 = **8.33%**, 1:15 = **6.67%**, 1:50 = 2%, 1:100 = 1%.

**Supreme Court, Rajive Raturi v. Union of India** (`RV`)
- **8 Nov 2024**, [2024] 11 S.C.R. 970, 2024 INSC 858 (bench led by CJI D.Y. Chandrachud): Rule 15(1) standards were largely recommendatory and did not meet the Act's mandatory scheme; Union directed to frame **mandatory baseline rules** with consultation; accessibility tied to dignity and constitutional rights. [6]
- **23 Feb 2026** correction: progressive compliance under existing Rule 15(1) standards and Accessible India targets must **"continue unabated"** while the mandatory baseline is built. Do not say the 2024 ruling paused obligations. [21] (indiankanoon)

Pitch line DOMAIN proposes: "We help people navigate today's gaps and help authorities identify tomorrow's repairs."

### 2.3 Jaipur and India footpath news (all TOI unless noted, `RV` as reported, not surveys)

| Date | Place | What was reported |
|---|---|---|
| 28 May 2026 | Jaipur | encroachment on Tonk Road, B2 Bypass, Sahkar Marg, markets near Ridhhi Siddhi and Barkat Nagar push walkers into traffic; vending committee inactive [17] |
| 21 Jun 2026 | Jaipur | "SC orders pavement overhaul, but civic bodies have failed Jaipur pedestrians before" [35] |
| 4 Aug 2026 | Jaipur | cafe seating around Gopalpura; vendors and office vehicles on pavements in Ashok Nagar and C-Scheme; "blocked despite SC push" [18] |
| 30 Sep 2023 | Mumbai | Karan Shah, bollards (below) [22] |
| 21 Sep 2025 | Bengaluru (New Indian Express) | Prakash Jothady fall (below) [30] |
| 5 Apr 2026 | Bengaluru (NewsKarnataka) | "Broken Footpaths Put Bengaluru Seniors At Daily Risk", listed in references only, not used in text [25] |
| (undated in list) | TOI business | "This CEO walks the talk: Why aren't roads built for wheelchairs?", listed in references only [23] |

DOMAIN's framing advice: pilot a small auditable corridor; treat vendors as a space-management issue, not as the enemy.

### 2.4 Real public stories (names are in published news)

| Person | Report | Story | Product lesson |
|---|---|---|---|
| **Karan Shah**, Mumbai, wheelchair user with spinal muscular atrophy | TOI, 30 Sep 2023 [22] | bollards at Cadell Road and King's Circle block his wheelchair. Quote: **"Bikes, scooters, humans can go through those poles, but a wheelchair user can't."** | measure usable clearance, not "footpath present". No injury or fix is reported, do not add one |
| **Prakash Jothady**, senior citizen, Malleswaram, Bengaluru | New Indian Express, 21 Sep 2025 [30] | going for groceries, slipped on wet soil from pipe-work excavation on a footpath, sprained knee | old photos expire; rain + construction need a recheck state |

### 2.5 Competitor apps and what they miss (DOMAIN section 5)

| Tool | What it does (date) | What it misses / what we must prove |
|---|---|---|
| **Google Maps** | wheelchair-accessible walking routes, **global, Android + iOS, where data exists**, announced 17 Oct 2023 [14] | do NOT say "not in India". Jaipur coverage unknown. No documented live detection of parked bikes or poles, clearance, surface, freshness, per-profile limits |
| **Wheelmap** | crowdsourced accessible **places**, traffic-light ratings [9] | place, not the path between places |
| **AccessNow** | rate places on ramps, lifts, lighting, sound [32] | directory, not route continuity |
| **Sugamya Bharat app** (DEPwD) | geotagged complaints, tracking, routing to officers; MyGov page dated 28 Jul 2026 (page date, not launch) [33] | reports a barrier, does not give an alternative route; no API integration exists, do not claim one |
| **Evelity** | profile-adapted indoor **and outdoor** wayfinding (hospitals, campuses, hubs) [10] | no India deployment confirmed; do not call it indoor-only |
| **Microsoft Soundscape** | 3D-audio spatial awareness; went open source Dec 2022, original services ended Aug 2023 [19] | retired service; no pothole/clearance detection |

From FORK, more prior art: Project Sidewalk (human audits, AccessScore), AccessMap (UW, preference routing), WheeLog! (wheelog.com), Devpost AccessMapAI / AccessGrid AI / PathAble.

DOMAIN's honest gap: **"fresh, explainable, user-specific evidence about the whole outdoor journey."** Not "first accessible map."

### 2.6 Physics and human factors numbers

| Topic | Number | Source | Grade |
|---|---|---|---|
| Ramp limits | 1:12 (8.33%) MoHUA / IRC 2012; 1:15 (6.67%) IRC:103-2022 kerb ramp | [5][27][29] | RV, C for % |
| Kerb climb | no single safe number; 150 mm design kerb is **not** a climbable step; never tell a user to wheelie | WSP Manual v5.0, 2019 [43]; IRC [27] | RV |
| Surface effort | **11** manual wheelchair users: more propulsion demand on grass, pavers, ramp vs smooth concrete | Koontz et al. 2005 [38] | RV |
| Surface effort | **13** experienced users: more rim work/power on aggregate concrete and incline | Hurd et al. 2009 [34] | RV |
| Rim work vs energy | mechanical work at the wheel is not metabolic energy; no "twice the energy" claim | DOMAIN | RV |
| Older walking speed | ~**0.79 m/s** design value (IRC older guidance) | [29] | RV |
| Signal timing | Swiss older adults struggled to meet **1.2 m/s**, esp. oldest group | 2017 study [36] | RV |
| Healthy older usual pace | **140.9 cm/s** (22 adults) | GAITRite study [37] | RV |
| Rest spacing | every **30 m** on walkways over **60 m** | MoHUA [5] | RV |
| Rain | US Access Board: wet conditions change firmness/stability | [41] | RV |
| Crossing time (C) | a 7 m crossing: 8.9 s at 0.79 m/s vs 5.8 s at 1.2 m/s | computed: 7/0.79, 7/1.2 | C (7 m is my example) |

### 2.7 The 10 what-ifs (judge questions, DOMAIN's answers in short)

| # | What if | Answer |
|---|---|---|
| 1 | a vehicle parks after the photo | show timestamps, accept reports, expire evidence; never say "real-time" unless measured |
| 2 | AI misses a pole, hole or broken ramp | false negative is a safety event; low-confidence or occluded stays unknown; critical transitions need a human check |
| 3 | no accessible route exists | say **"No verified route found"**, name the blocking link, offer report/assist; never sneak in steps |
| 4 | GPS puts user on the wrong side | side-of-street confirm; ask the user to confirm a landmark or side |
| 5 | rain / waterlogging | dry-weather photo cannot certify today; flag uncertain, avoid obscured critical segments; no invented flood-depth threshold |
| 6 | works for powered chair, not manual, pram or crutches | profile-dependent; ask equipment; show width, slope, surface |
| 7 | user cannot see screen / no internet | screen reader, keyboard, contrast, large targets; cached routes with visible age; does not replace a cane |
| 8 | Google Maps already does this | yes, globally where data exists; our add is local clearance, surface, freshness, shown on Jaipur routes |
| 9 | privacy / cost of images | small corridor, permitted capture, minimal retention, blur faces/plates, check terms; cost is an open question |
| 10 | someone is hurt following the route | no guarantee; supervised testing; injury reduction is unproven |

DOMAIN's user profiles: manual/powered wheelchair, older pedestrian, parent with pram, crutches, low vision (tactile continuity, crossing info, audio/text). Proposed evaluation metrics: route completion, unexpected barriers, assistance needed, **dangerous false-clear results**, observation age.

---

## 3. TECH report

### 3.1 Pipeline recipe per step (code-level)

**Step 1, detection (TECH section 1)**
- Default: **YOLO-World-S (v2) + OWLv2 base** (easiest install), or YOLO-World-S + Grounding DINO-T if DINO already works. Treat them as different, not independent.
- Code: `from ultralytics import YOLOWorld; model = YOLOWorld("yolov8s-worldv2.pt"); model.set_classes([...]); model.predict(img, imgsz=640, conf=0.12, iou=0.5, device=0 or "cpu")`. conf 0.12 is a deliberately loose proposal threshold.
- Second model: `pipeline("zero-shot-object-detection", model="google/owlv2-base-patch16-ensemble")`.
- 7 labels and the decision each needs: stairs; single step (close crop, shadows); **kerb without ramp** (no-ramp-detected is not no-ramp); curb ramp (check landing, width); broken pavement; pole (ground-contact point + remaining passage); parked motorbike (time-dependent).
- Agreement score (not a probability): `0.5*match(same class, IoU>=0.30) + 0.3*footpath_context + 0.2*independent_view_support`; single-model hit -> `unsure`; only a reviewer sets `verified`. VLM answers limited to `visible / not_visible / cannot_determine`.
- Local audit: hand-label **40-60 photos** incl. negatives, shadows, roots, distant obstacles; per-class precision/recall, disagreement rate, review fraction; hold some out.
- Grounding DINO -> SAM 2.1 Tiny: box prompt -> mask; mask is not a second vote.

**Step 2, metric depth (TECH section 2)**
- First try: **Depth Anything V2 Metric Small** (24.8M params), outdoor vkitti checkpoint, run from `metric_depth/`:
  `DepthAnythingV2(encoder="vits", features=64, out_channels=[48,96,192,384], max_depth=80)`, load `checkpoints/depth_anything_v2_metric_vkitti_vits.pth`, `model.infer_image(cv2.imread(...))` -> HxW metres. Indoor max_depth is 20.
- Alternatives: Metric3D v2 (needs real focal length + its full resize/pad/canonical-camera pipeline; ViT-L KITTI AbsRel 0.052, delta1 0.974), UniDepthV2 (points + intrinsics + confidence; KITTI delta1 98.9).
- Kerb height: back-project with `K^-1 [u,v,1]`, fit lower plane, `height_cm = 100*|median(P_upper . n + b)|`. Do not subtract two depth readings. Reject distant, occluded, blurred, reflective, sloped or tiny curbs; show **"height unknown"** unless one curb is tape-measured.

**Step 3, geolocation (TECH section 3)**
- Pose sidecar per image: `image_id, observed_at, lat, lon, horizontal_accuracy_m, heading_deg, heading_reference, pitch, roll, image_width, image_height, exif_orientation, camera_intrinsics, source, source_image_id, license`. EXIF `GPSImgDirectionRef` T = true north, M = magnetic; `GPSTrack` is travel direction, not camera direction.
- Mapillary fields: `computed_geometry, computed_compass_angle, compass_angle, captured_at, thumb_2048_url` via `https://graph.mapillary.com/IMAGE_ID?access_token=...&fields=...`. Panoramas: cut a perspective view first.
- Projection: ground-contact pixel, `ray = solve(K,[u,v,1])`, ENU via `R_enu_cam`, bearing `atan2(east,north)`, `pyproj.Geod(ellps="WGS84").fwd(lon,lat,bearing,dist)`. Radial vs axial depth handled.
- Matching: project the obstacle (not the camera), search candidate edges in a **30 m** radius (demo choice for an assumed **5-15 m** GPS error), rank by normalised distance, visibility, direction, road side, crossing vs sidewalk; keep top-k; review when opposite sides tie; snap to measure `s` and split a short interval. Keep `semantic_confidence` and `location_confidence` separate.
- Multi-photo: least-squares ray intersection `triangulate_xy` with `cond(A) > 1e4` rejection; no moving bikes.
- CRS: **EPSG:32643 (UTM 43N)** for Jaipur.

**Step 4, graph (TECH section 4)**
- `ox.settings.useful_tags_way += [foot, access, sidewalk, sidewalk:left, sidewalk:right, wheelchair, surface, smoothness, width, incline, lit, tactile_paving, crossing]`; `useful_tags_node += [barrier, kerb, kerb:height, wheelchair, tactile_paving]`; `ox.graph_from_polygon(poly, network_type="walk", simplify=False, retain_all=True)`; `ox.project_graph(G, to_crs="EPSG:32643")`; `save_graphml`. Default access filter drops `access=private`.
- Missing sidewalks: Shapely `line.offset_curve(+/-offset_m)` -> dashed, `unknown` candidates. Tile2Net needs CUDA, zoom 19+, warns about non-US scenes.
- OpenSidewalks topology: shared nodes at crossings, short connector footways, directional incline, split edges where width changes.
- Cost: `C_p(e) = inf` if a confirmed constraint fails (or strict policy rejects unknowns), else `(L/v_p)(1 + P_slope + P_surface + P_width) + P_crossing + sum P_barrier + P_unknown`, all nonnegative, seconds-equivalent, slope per direction.
- Profiles: manual wheelchair, elderly walker, pram, low vision (hard vs soft vs unknown columns in TECH table).
- AccessScore (Project Sidewalk) = `sigmoid(sum w_i)`, experimental, for overview only.

**Step 5, routing (TECH section 5)**
- **OSMnx + NetworkX backend is "best tonight"**; client-side Dijkstra as frozen fallback; Valhalla later; OSRM needs a foot profile at `osrm-extract`.
- `route_for_profile()` builds a DiGraph keeping the cheapest parallel edge and its `original_edge=(u,v,k)`; on `NetworkXNoPath` returns `{"status":"no_verified_route"}`. Baseline "shortest" and profile route from the same graph snapshot.
- API: `POST /observations`, `GET /jobs/{id}`, `PATCH /observations/{id}`, `GET /graph`, `POST /route` (origin, destination, profile, as_of, unknown_policy). FastAPI + GraphML/GeoJSON + static images; inference outside the route request.
- Observation and Edge schemas listed in TECH (incl. `valid_until`, `height_method`, `height_uncertainty`, OSM-style `check_date:*`).

**Step 6, 3D (TECH section 6)**: Splatfacto via `ns-process-data images` -> `ns-train splatfacto --max-num-iterations 3000` -> `ns-export gaussian-splat`; 20-50 overlapping photos of one crossing; needs a **12-24 GB rental GPU** as a planning figure. Viewers: antimatter15/splat, Spark (`SparkRenderer`, `SplatMesh`), gsplat.js (drops SH colour).

**Step 7, browser (TECH section 7)**: MapLibre + deck.gl `MapboxOverlay({interleaved:false})`; `PathLayer` underlay, `TripsLayer` playhead (timestamps in seconds from route start, 32-bit float issue), `ScatterplotLayer` evidence (pickable, click opens card). Visual grammar: shortest = thin muted; profile route = bright + animated traveller; confirmed barrier solid; unsure hollow amber; uncertainty halo; inferred sidewalk dashed. No red/green only; keyboard; reduced-motion; text comparison.

### 3.2 Timings on a 4 GB GPU / CPU

The honest answer from TECH: **no report contains a measured 4 GB GPU or laptop CPU timing for any model.** Every number is from other hardware or is a memory statement.

| Item | Figure in reports | Hardware | Use for 4 GB? |
|---|---|---|---|
| YOLO-World (paper) | 35.4 AP, **52 FPS** | V100 | no |
| SAM 2.1 Tiny | **91.2 FPS** | A100 | no |
| YOLO26n det / seg | **38.9 ms / 53.3 ms** CPU ONNX | Ultralytics docs, CPU not named | rough CPU hint only |
| SmolVLM-256M | under 1 GB GPU RAM | card | fits |
| Qwen2.5-VL-3B | ~6 GB weights at 2 bytes/param before activations | arithmetic | no, unless remote |
| FlashAttention-2 | standard path Ampere/Ada/Hopper; BF16 needs newer GPUs | docs | GTX 1650 (Turing) cannot use the BF16 examples |
| Depth Anything V2 Small | 24.8M params | card | likely fits (`ME`, untested) |
| Splatfacto | ~6 GB default, ~12 GB big | nerfstudio docs | no |
| Voyager / Wan2.2 I2V / TI2V-5B | 60-80 GB / 80 GB / 24 GB | repos | no |
| tactile-path SegFormer-B0 | 1.70 FPS Jetson Nano, ~116 FPS RTX 3090 | repo | not applicable |

TECH's acceptance budget: **2 s per image on GPU, 10 s on CPU**, else precompute. Its `bench()` helper (warm-up, `torch.cuda.synchronize`, p50/p95, `max_memory_allocated`) is in the verbatim file. Run each model in its own process to free VRAM.

### 3.3 Hour-by-hour plan (TECH) mapped to tonight

Mapping to IST is mine (`ME`): start 17:00, end 02:00, 30 min buffer before 02:30.

| Hour | IST | Deliverable | Gate | Fallback |
|---|---|---|---|---|
| 0-1 | 17:00-18:00 | pick polygon + demo crossing; Vite/React/MapLibre shell; Python env; one detector; graph data; upload + sidecar | map loads, one real image + metadata visible | frozen local graph + local photos |
| 1-2 | 18:00-19:00 | OSM walk graph with tags; fix sides, gates, crossings on the demo corridor | origin-destination connect through real topology | hand-drawn GeoJSON, labelled demo-authored |
| 2-3 | 19:00-20:00 | YOLO-World on photos; save boxes, crops; measure latency/VRAM | key photos have inspectable detections | CPU batch, remote, or hand labels |
| 3-4 | 20:00-21:00 | 2nd detector; label normalise; agreement; `unsure` + review actions | disagreement -> review item | single-model flagged unsure; human as 2nd channel |
| 4-5 | 21:00-22:00 | contact-point projection, candidate edges, reassignment UI; depth test on featured curb | reviewer can fix side and crossing | manual edge assignment; height unknown or tape-measured |
| 5-6 | 22:00-23:00 | profile costs, hard exclusions, unknown policy, expiry, baseline vs profile routes, no-route | profile change changes route or explains why not | client-side Dijkstra on frozen graph; precomputed routes |
| 6-7 | 23:00-00:00 | route animation, evidence cards, uncertainty styling, keyboard/text | a viewer can explain the detour unaided | static lines + clickable photos |
| 7-8 | 00:00-01:00 | optional splat on another GPU, else photo walkthrough | scene or sequence appears in budget | stop 3D; photos/video; any generated clip marked synthetic |
| 8-9 | 01:00-02:00 | freeze; test profile changes, no-route, stale bike, wrong-side snap, missing GPS, mobile, offline; record demo | happy path + honest failures | fully static build with cached graph and evidence |

FORK's own 9-hour plan is the same shape (0-1 setup, 1-3 detector + evidence cards, 3-4:30 edge assignment, 4:30-6 profiles, 6-7:30 comparison + attribution, 7:30-8:30 deploy hardening, 8:30-9 rehearsal).

Scope cut order if late (TECH): drop centimetre claims first, live inference second, Gaussian reconstruction third. Protect graph correctness, evidence, profile routing.

Demo story (FORK + TECH agree): shortest route hits a reviewed step/blockage -> alternative route -> click to the photo; then fix a wrong-side detection and watch only that edge change; end on an occluded spot marked unknown and a case that refuses to claim a route.

---

## 4. Contradictions and flags

| ID | Issue | Where | What to do |
|---|---|---|---|
| C1 | **Detector pick differs.** FORK: Grounding DINO **or** Florence-2, one detector. TECH: YOLO-World-S + OWLv2 (or + DINO), two detectors | FORK s8 vs TECH s1 | pick TECH's two-model setup if the 4 GB box handles YOLO-World; DINO is the overlap. `ME` |
| C2 | **RampNet numbers.** TECH quotes paper: dataset 94.0% P / 92.5% R, detector **0.9236 AP**. FORK quotes the repo's corrected eval: **P 0.949, R 0.873** at threshold 0.55 on a 1,000-panorama gold set, and warns not to mix them | TECH s1 vs FORK s2 | if cited, say which version; neither is an India number |
| C3 | **Licence trap in TECH's code.** TECH's snippet uses `ultralytics.YOLOWorld` = **AGPL-3.0**; FORK lists the original YOLO-World repo as **GPL-3.0**. Fine for a hackathon, matters if the site code is published closed | FORK s2 | note in README |
| C4 | **Depth checkpoint licence.** FORK: DA-V2 Small weights Apache-2.0. TECH uses the **metric vkitti Small** checkpoint, whose licence neither report states; trained on Virtual KITTI 2 (licence not stated in reports) | FORK s6, TECH s2 | UNVERIFIED, check the metric_depth README before claiming open use |
| C5 | **Ramp standard (known fact check).** DOMAIN: MoHUA HG 2021 kerb ramp **1:12**, IRC:103-2022 **1:15**, IRC:103-2012 1:12. Matches the known fact. No report contradicts it | DOMAIN s2, s6 | show both with version labels |
| C6 | **Router defaults vs Indian standards** (`C`). OTP `maxSlope` default **0.083** = 1:12 (MoHUA). ORS `maximum_incline` default **6%** is stricter than both 8.33% and 6.67%. Neither engine default equals IRC 1:15 | FORK s5 | expose slope limit per profile; default to 1:15 (6.67%) and show MoHUA 1:12 as the looser option. `ME` |
| C7 | **ORS `maximum_sloped_kerb` units.** FORK lists 0.03/0.06/0.1 with no unit; DOMAIN kerb heights are in mm (150, 200). Likely metres (0.06 m = 60 mm) | FORK s5 | UNVERIFIED, check ORS docs before quoting |
| C8 | **Width rule differs by standard**: MoHUA 1.2 m min / 1.8 m two-way vs IRC:103-2022 2 m clear zone | DOMAIN s2 | width threshold per standard, labelled |
| C9 | **Scope**: TECH plans a "campus", FORK/DOMAIN a Jaipur corridor, SC-02 is all of India | all | demo corridor + India-wide data path story. For India-wide CRS: India spans UTM zones **42N-47N** (C: zone = floor((lon+180)/6)+1 for 68 E -> 42, 97 E -> 47), so EPSG:32643 is Jaipur-only |
| C10 | **GPS error 5-15 m** in TECH is an assumption from its prompt, not a sourced figure | TECH s0, s3 | label as assumption |
| C11 | **UrbanVGGT date**: arXiv id 2603.22531 implies a March 2026 submission, FORK says "Published/updated 19 Aug 2026" | FORK s1 | likely a revision date; UNVERIFIED |
| C12 | **Chandigarh usefulness**: per-criterion usefulness 4.61/5 vs abstract "4.66/5 overall" | FORK s1 | both from the paper; quote the one with its label |
| C13 | **Google Maps**: DOMAIN says it already has global wheelchair walking routes (2023), so "first accessible map in India" is false. FORK says Google terms ban using Maps content to train/test/validate AI. Chandigarh study still used Street View panoramas | DOMAIN s5, FORK s3 | do not use GSV for our eval set; do not claim Google lacks the feature |
| C14 | **Ultralytics model names**: FORK cites YOLO26n numbers while the repo title lists **YOLO27**; TECH uses `yolov8s-worldv2.pt` | FORK refs, TECH s1 | a newer YOLO line may exist; check before install (UNVERIFIED) |
| C15 | **Speed for older pedestrians**: 0.79 m/s design (IRC 2012) vs 1.2 m/s signal assumption (Swiss) vs 1.409 m/s healthy older usual pace | DOMAIN s6 | user-adjustable pace, default 0.79 for crossing checks. `ME` |

No direct number clash was found between DOMAIN and the other two on India statistics; FORK and TECH carry no India population or law figures.

---

## 5. Red-team of this digest

| Claim in this digest | Grade | Why |
|---|---|---|
| All three files saved verbatim with 3-line header | VERIFIED | extracted programmatically from tool output; run-id line present in each body; sizes 41,115 / 89,832 / 53,793 bytes |
| All three read to the end | VERIFIED | FORK 1-487, TECH 1-687 paged; DOMAIN read in full as inline result |
| India numbers and clauses | UNVERIFIED by me | report-labelled verified (RV); no primary PDF opened in this pass. The biggest-risk ones to re-check before the slide: 36,526 / 177,175 (MoRTH 2024), Jaipur 860, Raturi 23 Feb 2026 correction, PIB 9 Oct 2026 |
| Repo licences, stars, push dates | UNVERIFIED | snapshot from FORK's GitHub API reads; none opened by me |
| "No 4 GB timing exists in the reports" | VERIFIED | searched while reading; only V100, A100, Jetson, RTX 3090 and unnamed-CPU ONNX numbers appear |
| IST hour mapping | my plan, not a report fact | |
| C6 slope comparisons, % conversions, crossing times, UTM zones | VERIFIED (arithmetic) | 1/12 = 0.0833, 1/15 = 0.0667, 7/0.79 = 8.86 s, 7/1.2 = 5.83 s, (68+180)/6 = 41.3 -> 42, (97+180)/6 = 46.2 -> 47 |
| C4, C7, C11, C14 | UNVERIFIED | flagged as open checks |
