<!-- run id: trun_3b693d434bb94e6d96d0a999fe5a4730 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 16:38 IST via mcp__parallel-task__getResultMarkdown, body below is verbatim -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6d96d0a999fe5a4730
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T10:25:06.633000Z
**Modified:** 2026-10-24T10:32:30.335642Z

## Output

# Build Jaipur's Accessible Route Demo in Nine Hours

## Executive Summary

- **Build A Small, Auditable Route Network**: OpenSidewalks explicitly distinguishes network connectivity from geometries that merely cross [17] -> build a reviewed neighborhood footpath graph, not a citywide promise of safety.
- **Reuse The India Adaptation, Not Its Evaluation As Detection Accuracy**: The Chandigarh study covers about **40 km**, uses **Gemini gemini-2.5-flash**, and reports guidance ratings from **3 annotators on 50 segments** [3] -> copy its locally appropriate taxonomy and human-review pattern.
- **Use Complementary Models**: RampNet specializes in curb ramps; Tile2Net extracts pedestrian networks from **orthorectified aerial imagery**, not street photos [2][1] -> use a general detector plus sidewalk masks for tonight's images, and treat RampNet as an additional specialist.
- **Respect Imagery Rights Before Building On Them**: Mapillary imagery is CC-BY-SA, while Google Maps terms prohibit using its content to train, test, validate, or fine-tune AI models and restrict derived content [24][27] -> prefer team-owned photos or a clearly permitted open-imagery workflow.
- **Keep Geolocation Reviewable**: Project Sidewalk's label-position estimator reports a **1.47 m median test error** in its own evaluation [14] -> even a published estimator is not a guarantee of the correct side of a Jaipur street.
- **Route Around Barriers, Not Just Toward A Score**: Valhalla supports runtime costing, GraphHopper supports custom models, and openrouteservice exposes wheelchair restrictions [12][15] [94] -> distinguish hard exclusions, preference penalties, and unknown accessibility.
- **Do Not Put Heavy World Models On The Critical Path**: Voyager documents **60 GB minimum GPU memory at 540p**, with **80 GB recommended** [48] -> use real-image stepping or a precomputed browser asset for the demonstration.
- **Demonstrate Evidence, Not Certification**: Depth Anything V2 separates relative-depth models from separately fine-tuned metric models [25] -> show estimated geometry as uncertain, and reserve "verified" for reviewed observations.

**Scope and confidence.** This is a broad, source-backed inventory for **24 October 2026**, not a defensible claim to have found every project on the internet. It includes directly relevant projects, useful components, and leads that are not yet safe to fork. Some requested names/platforms did not yield a verifiable, licensed, task-specific artifact; those gaps are stated rather than filled with invented repositories.

**How to read the inventories:** `U` means the field was not established in the reviewed source. Dates labeled "code push" are observed repository `pushed_at` dates, not release dates or guarantees of ongoing maintenance. Stars and monthly downloads are observed snapshots, not quality scores. For runtime, `Y` means explicitly supported/documented; `E` is an engineering expectation, not a benchmark; `?` is unverified; `UI` means browser visualization only, not browser inference. No project was installation-tested on your hardware during this research. Source-reported performance numbers remain **author claims**, not Jaipur validation.


## 1. Chandigarh Supplies The Right Taxonomy, Not A Ready Jaipur Detector

### The February 2026 paper: exactly what is reusable

**"Towards Human-AI Accessibility Mapping in India: VLM-Guided Annotations and POI-Centric Analysis in Chandigarh"**, arXiv **2602.09216v2**, is dated **17 February 2026**. Its authors are Varchita Lalwani, Utkarsh Agarwal, Michael Saugstad, Manish Kumar, Jon E. Froehlich, and Anupam Sobti. [3]

The key decision is to adapt **Project Sidewalk's human annotation interface**, rather than assume that American curb-ramp categories transfer unchanged. The adaptation replaces "Curb Ramp" with **"Curb Style"**, retains three severity levels, adds vendors, drainage channels, parked two-wheelers, and construction debris, expands surface problems to loose brick, mud and unpaved shoulders, and distinguishes absent pedestrian space from unusable pedestrian space. [3]

The VLM is **Gemini gemini-2.5-flash**. It receives the OSM road type and the first and last Street View panoramas associated with a segment, then generates mission guidance for annotators. This is **not** a trained autonomous detector of every barrier, nor a demonstrated wheelchair-routing system. [3]

| Requested Point | Verified Finding | What It Means Tonight |
|---|---|---|
| Code | A dedicated public repository for this adaptation was not established; the upstream Project Sidewalk repository is available. | Do not assume the India-specific fork can be cloned tonight. |
| Data | The study describes its annotations and analysis, but a downloadable, licensed Chandigarh release was not established. | The reported dataset is not automatically an available training set. |
| Study scope | About **40 km**, **3 sectors**, around **230 POIs**, and **1,644 improvement locations**. [3] | Useful local evidence, not coverage of Jaipur. |
| Image coverage filter | Retained paths with at least **75%** geometry overlap with Street View coverage. [3] | Image availability shapes the evaluated network. |
| Guidance evaluation | **50 street segments**, **3 annotators**, **150 ratings per criterion**. [3] | Small human-rating study, not detection precision/recall. |
| Relevance | Mean **4.97/5**, SD **0.26**. [3] | Guidance usually concerns the right task. |
| Accuracy | Mean **4.40/5**, SD **0.71**. [3] | Guidance still needs checking. |
| Usefulness | Mean **4.61/5**, SD **0.70**; the abstract reports **4.66/5 overall**. [3] | Do not advertise these as "AI barrier detection accuracy." |
| Planning result | Education and transport score lowest in the reported category analysis. [3] | POI-centered audits are a useful presentation pattern. |

**Decision:** borrow the taxonomy and POI-centered workflow immediately; do not spend the evening attempting to reproduce the paper or searching for an unconfirmed checkpoint.

### Training and evaluation data: India first, complementary foreign data second

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **India Driving Dataset**<br>`https://idd.insaan.iiit.ac.in/` | U - obtain official terms | U | U | Indian road scenes; official site reports 10,000 images, 34 classes, 182 drive sequences. | C: data only; G: model-dependent; B: preview | Use for appearance/domain adaptation, not as a ready accessibility-barrier taxonomy. [31] |
| **Mapillary Vistas**<br>`https://www.mapillary.com/dataset/vistas` | CC BY-NC-SA | U | U | Diverse street-scene segmentation data. | C: data only; G: model-dependent; B: preview | Train/evaluate sidewalk and object masks; keep its noncommercial terms separate from ordinary Mapillary imagery. [88] |
| **segments/sidewalk-semantic**<br>`https://huggingface.co/datasets/segments/sidewalk-semantic` | See source note below | U | U | Belgian sidewalk segmentation images. | C: data only; G: model-dependent; B: preview | Useful masks for a baseline; not evidence of Jaipur transfer. [36] |
| **Kaggle IDD repack**<br>`https://www.kaggle.com/datasets/mitanshuchakrawarty/new-idd-dataset` | U - upstream rights still apply | U | U | Community-resized/repackaged IDD data, not a new official benchmark. | C: data only; G: model-dependent; B: preview | Convenience only; prefer the official source and preserve labels. [86] |
| **SideSeeing**<br>`https://arxiv.org/abs/2407.06464` | U for code/data | Published 2024 | U | Multimodal sidewalk assessment dataset and collection tools. | C/G/B: component-dependent, ? | Relevant for collecting sidewalk-level observations; release details below. [30] |
| **UrbanVGGT**<br>`https://arxiv.org/pdf/2603.22531` | U for code/data | 2026 preprint | U | Sidewalk-width estimation using segmentation, feed-forward 3D, ground-plane fitting and camera-height scale. | C: ?; G: ?; B: outputs only | A strong geometry design reference; do not assume an installable released package. [33] |

The distinction matters: a dataset can be open for research without permitting every deployment, and a car-view segmentation dataset can recognize Indian appearance without labeling passable wheelchair space. For tonight, a small, consented Jaipur photo set with reviewed labels is more decision-useful than claiming success from a foreign benchmark.

**Additional dataset release details, quoted from the primary cards/papers:**

- Dataset URL: https://huggingface.co/datasets/segments/sidewalk-semantic [36]   Paper URL: not provided; citation information is marked "[Needs More Information]" [36]   License: cc-by-nc-4.0 [36]   Classes: 35 classes, IDs 0-34, including flat-sidewalk, flat-road, vehicles, construction, objects, nature, sky, and void categories [36]   Size: 1K-10K [36]; total file size: 324 MB [36]   Split: one split [36]   Code/checkpoints: linked models include tobiasc/segformer-b0-finetuned-segments-sidewalk, chainyo/segformer-sidewalk, nielsr/sidewalk-semantic-demo, nickmuchi/segformer-b4-finetuned-segments-sidewalk, nielsr/segformer-finetuned-sidewalk, and chainyo/segformer-b1-sidewalk [36]   Published date: not shown. Updated dates shown include Mar 23, 2023; Jul 5, 2023; Sep 11, 2023; Mar 21, 2022; Jun 27, 2023; and Mar 14, 2025 [36]   Downloads last month: 118 [36]   Indian sidewalks: no; the dataset is of sidewalk images gathered in Belgium in summer 2021 [36]   Hardware: not given.

- Paper/dataset: "SideSeeing: A multimodal dataset and collection of tools for sidewalk assessment." [30] Exact paper URL: https://arxiv.org/abs/2407.06464 [30] Dataset/tools URL: https://sites.usp.br/sideseeing/ [30] License: a license link is provided, but the license terms are not shown. [30] Classes: a 68-element taxonomy for sidewalk scene identification. [30] Size: three hours, 12 kilometers, nine hospitals, and 325,000 video frames with corresponding sensor data. [30] Code/checkpoint links: not shown. Published/updated dates: submitted 9 Jul 2024; last revised 12 Jul 2024. [30] Downloads: not shown. Hardware: chest-mounted mobile devices with accelerometer, gyroscope, magnetometer, and GPS. [30] Indian sidewalks: not specified; samples were collected near hospitals in Brazil and the USA. [30]

- UrbanVGGT paper: https://arxiv.org/pdf/2603.22531. Published/updated: 19 Aug 2026. [33] No license, code/checkpoint links, or download counts are shown. Benchmark: approximately 300 Google Street View images, 640 x 640 pixels, 90-degree FOV; sidewalk widths range from 0.56 m to 3.94 m. [33] Prototype: 1,931 valid image-level measurements covering 527 unique OpenStreetMap street segments across New York City, Sao Paulo, and Nairobi. [33] Classes: sidewalk-width measurements/estimates; no formal class taxonomy is given. [33] It does not specifically address Indian sidewalks. Hardware details are not given; the method uses Google Street View car imagery and assumes a fixed 2.5 m camera height. [33]

Other discovered leads include **RUGD** (`http://rugd.vision/`) for unstructured-ground semantics and **RELLIS-3D** (`https://unmannedlab.org/research/RELLIS-3D`) for multimodal off-road perception. They are adjacent terrain resources, not verified Jaipur accessibility datasets; their reuse licences, current updates and deployment requirements remain U in this inventory.


## 2. Combine Barrier Boxes With Footpath Masks And Human Review

### RampNet illustrates both the opportunity and the transfer risk

RampNet bootstraps curb-ramp training annotations from government location data and street panoramas. Its published dataset contains **214,385 panoramas and 849,904 labels**; the repository is MIT-licensed, but that does not by itself establish unrestricted rights to the underlying Google imagery. [2]

Its updated repository also documents an evaluation correction: on a **1,000-panorama gold set**, at threshold **0.55**, corrected one-to-one matching gives **precision 0.949** and **recall 0.873**. These are the authors' results for that evaluation, not an India benchmark. The paper-state and corrected-evaluation versions must not be casually mixed. [2]

For Jaipur, RampNet answers "is there a ramp-like feature?" It cannot by itself answer "is this whole route traversable?" Likewise, finding a vehicle is not equivalent to finding a blocked footpath: the vehicle must occupy the pedestrian corridor, and usable clearance must be considered. The recommended integration is **detector -> sidewalk mask -> spatial relationship -> reviewed barrier**, not detector label -> automatic closure.

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **ProjectSidewalk/RampNet**<br>`https://github.com/ProjectSidewalk/RampNet` | MIT code; imagery/data rights separate | 2026-10-22 | 9 | Curb-ramp specialist with pretrained inference and released dataset links. | C: Y setup; G: ?; B: UI only | Optional specialist alongside a general detector; inspect panorama/seam assumptions. [2] [21] |
| **ProjectSidewalk/SidewalkWebpage**<br>`https://github.com/ProjectSidewalk/SidewalkWebpage` | MIT | 2026-10-23 | 110 | Human auditing, severity labels, open GeoJSON/CSV exports. | C: server E; G: not needed for UI; B: Y | Borrow annotation patterns; full deployment needs Docker, database and configuration. [16] [58] |
| **ProjectSidewalk/sidewalk-tagger-ai**<br>`https://github.com/ProjectSidewalk/sidewalk-tagger-ai` | Apache-2.0 | 2026-10-16 | 0 | Fine-grained Project Sidewalk tag/severity learning. | C: ?; G: ?; B: no documented inference | Useful classifier research; not a complete detector/geolocator. [60] |
| **VIDA-NYU/tile2net**<br>`https://github.com/VIDA-NYU/tile2net` | BSD-3-Clause | 2026-09-12 | 231 | Aerial imagery -> sidewalk/crosswalk/road polygons and connected centerlines. | C: preprocessing E; G: CUDA required, 4GB ?; B: outputs | Graph bootstrapping only if suitable aerial imagery exists; not a street-image obstacle model. [1] [61] |
| **IDEA-Research/GroundingDINO**<br>`https://github.com/IDEA-Research/GroundingDINO` | Apache-2.0 | 2024-08-12 | 10701 | Text-prompted open-set bounding boxes. | C: Y; G: ?; B: UI only | Prompt poles, parked vehicles, stairs and debris; send selected boxes to a segmenter. [5] [22] |
| **AILab-CVC/YOLO-World**<br>`https://github.com/AILab-CVC/YOLO-World` | GPL-3.0 | 2025-02-26 | 6588 | Open-vocabulary detection with a prompt-then-detect workflow. | C: E export-dependent; G: E for small model, untested; B: ? | Good candidate for repeated fixed prompts; validate export and packaging early. [7] [68] |
| **google/owlv2-base-patch16-ensemble**<br>`https://huggingface.co/google/owlv2-base-patch16-ensemble` | Apache-2.0 | Model dated June 2023 | 1,668,866 downloads/month observed | Text-conditioned zero-shot object detection. | C: E slow; G: ?; B: ? | Alternative detector for a prompt comparison, not a reason to run several in production. [9] |
| **microsoft/Florence-2-base**<br>`https://huggingface.co/microsoft/Florence-2-base` | MIT | U for checkpoint update | 2,922,384 downloads/month observed | Detection, phrase grounding, captioning and other prompted vision tasks. | C: Y fallback; G: E, untested; B: ? | A compact alternative; pin processor/runtime and preserve structured coordinates. [8] |
| **facebookresearch/sam2**<br>`https://github.com/facebookresearch/sam2` | Apache-2.0 | 2026-05-30 | 20051 | Prompted image/video segmentation, not semantic accessibility classification. | C: ?; G: ?; B: UI is not inference | Refine detector boxes or human clicks into masks; do not expect class names from SAM alone. [10] [72] |
| **ultralytics/ultralytics**<br>`https://github.com/ultralytics/ultralytics` | AGPL-3.0; commercial terms separate | 2026-10-23 | 62771 | YOLO detection/segmentation training and inference tooling. | C: E; G: E for small variants; B: export-dependent ? | Fast route for common objects; custom missing-ramp/broken-footpath classes need data. [42] [81] |
| **navblind/Sidewalk-semantic-seg**<br>`https://github.com/navblind/Sidewalk-semantic-seg` | U - inspect dependency licences | U | 12 stars in discovery snapshot | Older sidewalk semantic-segmentation experiments. | C: ?; G: ?; B: ? | A research baseline, not an assumed maintained app. [84] |

**Interpretation:** choose one detector first. Grounding DINO has documented CPU mode; the **4 GB** suggestions above are estimates, not verified memory measurements. Reduce resolution and batch size, and precompute outputs if the model is not responsive enough.

### Small VLMs: explain evidence, do not invent geometry

The following primary cards/repository notes retain their checkpoint-specific licence and compute distinctions. Unless explicitly stated in a row, update, popularity and CPU/4 GB/browser compatibility remain **U**. A VLM's fluent explanation is not proof that a ramp exists or that a passage has sufficient width.

| Resource URL | Source-Stated Licence, Function, Version, Popularity And Compute Facts | Jaipur Integration Decision |
|---|---|---|
| `https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct` | Qwen2.5-VL-3B-Instruct  The repo contains the instruction-tuned 3B Qwen2.5-VL model. [46] Model size: 4B params. [46] Downloads last month: 2,021,924. [46] No exact license, CPU/4GB, or browser evidence is provided. Qwen2.5-VL can accurately localize objects in an image by generating bounding boxes or points, and it can provide stable JSON outputs for coordinates and attributes. [46] The model supports a wide range of resolution inputs. [46] These values will be rounded to the nearest multiple of 28. [46] | Optional structured review; use the exact checkpoint licence, not a generic Qwen-family assumption. |
| `https://github.com/ultralytics/ultralytics` | Ultralytics is licensed under AGPL-3.0. [42] YOLO26n detection has 2.4M parameters and reports 38.9 ms CPU ONNX speed. [42] YOLO26n-seg has 2.7M parameters and reports 53.3 ms CPU ONNX speed. [42] The models support object detection and instance segmentation. [42] No 4GB, browser, downloads/stars, release-date, or coordinate-accuracy evidence is provided. | Already in the detector table; do not confuse a detector with a VLM. |
| `https://huggingface.co/vikhyatk/moondream2` | License: apache-2.0. [54] Model size: 2B params. [54] This repository contains the latest (2025-06-21) release of Moondream 2. [54] Downloads last month 2,320,743. [54] Moondream is a small vision language model designed to run efficiently everywhere. [54] Sharper Object Detection uses reinforcement learning on higher-quality bounding-box annotations. [54] Grounded Reasoning explicitly grounds reasoning in spatial positions within the image before answering. [54] Object Detection returns objects, while Pointing returns points. [54] No CPU, 4GB, or browser evidence is provided. Accurate coordinate limitations are not specified. | Candidate compact visual assistant; review grounding output against the photo. |
| `https://github.com/huggingface/transformers.js` | License: Apache-2.0. [45] Model size, last release, downloads, and stars are not stated. Browser inference runs on CPU via WASM by default; WebGPU is available experimentally. [45] The library supports object detection and image segmentation, including mapping pixels to objects. [45] No 4GB evidence or coordinate-accuracy limitations are stated. | Browser inference runtime only for supported/exported models; not blanket compatibility for this catalog. |
| `https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct` | License: Apache 2.0. [40][522.157]   Model size: 0.3B params. [40]   Downloads last month: 231,254. [40]   It can run inference on one image with under 1GB of GPU RAM. [40] No CPU, 4GB, or browser evidence is provided. [40]   SmolVLM can answer questions about images, describe visual content, or transcribe text. [40] The model does not support image generation. [40]   No explicit detection, segmentation, grounded explanation, or accurate-coordinate capability is documented. [40][522.95-97] The model may produce content that appears factual but may not be accurate. [40] | Optional image/crop explanation. Verify export support before promising browser inference. |

**Failure case to design around:** "missing ramp" and "missing sidewalk" are absence claims. If the relevant curb, crossing or corridor is hidden, label **unknown/occluded**, not "missing." A pole, pedestrian or parked scooter becomes a routing barrier only after its relationship to the usable corridor is established. These are proposed application rules, not claims that the listed models already implement them.


## 3. Get Lawful Jaipur Images Before Depending On An API

| Source / URL | Licence And Access | Update / Popularity | CPU / 4 GB GPU / Browser | India/Jaipur Reality | Integration Decision |
|---|---|---|---|---|---|
| **Team-owned photos/video** | Obtain contributor permission and avoid exposing identifiable bystanders unnecessarily. | Your capture date; popularity N/A. | C: Y processing; G: optional; B: display. | You control where and when you capture. | Best fallback: upload a small reviewed neighborhood set with GPS, heading and capture time. |
| **Mapillary API v4**<br>`https://www.mapillary.com/developer/api-documentation` | Authenticated Graph API/entity endpoints and vector tiles; client/user tokens. Imagery is CC-BY-SA with attribution. [35][24] | API changelog includes 2026 entries; image freshness is per capture. [35] Stars/downloads N/A. | C: Y requests; G: not required; B: viewer possible. | A global service is not evidence of useful coverage on your selected Jaipur footpaths. | Query the exact demonstration area first. Preserve image IDs, capture time, attribution and pose metadata. |
| **KartaView**<br>`https://kartaview.org/doc`<br>`https://kartaview.org/terms` | Public and authenticated endpoints; protected requests use access tokens. Check image and API terms separately. [29] | U; popularity U. | C: Y requests; G: not required; B: viewer. | Jaipur coverage was not established. | Backup open-imagery source, not a guaranteed replacement for Mapillary. |
| **Google Street View Static API**<br>`https://developers.google.com/maps/documentation/streetview/policies` | Proprietary service; attribution required. General prefetch/index/store/cache prohibition, with panorama-ID exceptions. [26] | Policy updated **2026-10-21**. [26] Popularity N/A. | C: requests; G: not required; B: licensed display. | Chandigarh's use shows that city had usable imagery in its study, not that Jaipur has complete current coverage. [3] | Do not bulk-download panoramas or treat this as an unrestricted training/validation source. |
| **Bhuvan/NRSC**<br>`https://bhuvan.nrsc.gov.in/wiki/index.php/Information_for_Developers` | API/data-specific conditions; no blanket open licence established. | U; popularity U. | C: requests; G: not required; B: geospatial layers. | Developer services are geospatial/search services; a usable Jaipur street-panorama API was not established. | Potential basemap/context source, not an assumed street-image supplier. |

**The important legal split:** ordinary Mapillary imagery and the **Mapillary Vistas research dataset do not have the same licence**. The former is documented as CC-BY-SA; Vistas is documented as **CC BY-NC-SA**. [24] [88]

Google's current general terms prohibit exporting/scraping content outside the services, caching except where permitted, creating content based on Google Maps content, and using content to improve AI models, including training, testing, validation and fine-tuning. They also contain restrictions on use with non-Google maps. The exact service-specific agreement matters; do not infer that a published paper grants your application those rights. [27]

**Primary KartaView/Bhuvan details:**

- KartaView is a free and open platform for street level imagery. [101] Anyone can contribute images with a smartphone and our open source apps. [101] The service collects, stores and distributes georeferenced street view imagery and spatial 3D data. [101] Use is free of charge. [101]  KartaView software is licensed under the MIT License, while street images and 3D spatial data are licensed under Creative Commons Attribution-ShareAlike 4.0 International. [101] Users may copy, distribute, transmit and adapt data if they comply with the applicable license and credit Grab and KartaView contributors. [101] The required credit is "(c) Grab and KartaView Contributors". [101] Submitted content is also subject to a worldwide, royalty-free, non-exclusive, perpetual, irrevocable license to Grab, including commercial use. [101]  The source provides app links for Apple App Store, Google Play, and an Android APK download. [101] It does not state an API, star ratings, download counts, or update frequency. KartaView may detect signs, lanes and road curvature from uploaded images. [101] Account registration requires true, accurate, current and complete information, and users must be at least 18. [101]

- Bhuvan Geoportal has been developed using open source solutions, with no limitation of licenses or vendor dependencies. [85] OpenLayers API uses the 2 Clause BSD license; GeoServer/GeoWebCache use the GNU General Public License; UMN MapServer/TileCache use the MIT License. [85] Existing framework code supports visualization of Satellite and Base map data, and adding WMS/KML layers. [85] The Search Web API returns latitude and longitude for place names. [85] Update frequency, stars, downloads, and hardware are not stated. Street-level panoramas are not described.

**Decision:** make lawful image acquisition a first-hour go/no-go check. Keep team-owned photos as the working fallback. Neither India coverage nor present-day accessibility should be inferred from a provider's global marketing map.


## 4. Attach Evidence To The Correct Footpath, Not The Nearest Road

### A reusable geolocation case, with a measurable limitation

`ProjectSidewalk/label-latlng-estimation` estimates a label's latitude/longitude from its placement in a Street View viewport. Its published estimator reports **1.47 m median test error**, and its current repository distinguishes an authoritative Python implementation from the frozen earlier R analysis. That makes it useful code to inspect, but the original calibration is not automatically valid for a different camera or imagery provider. [14]

OpenSidewalks supplies the complementary representation: explicit pedestrian entities and connections. It uses WGS-84 coordinates; crossing geometries do not automatically connect, and sidewalks/crossings have explicit connection rules. This prevents a visually plausible line intersection from silently becoming a wheelchair crossing. [17]

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **ProjectSidewalk/label-latlng-estimation**<br>`https://github.com/ProjectSidewalk/label-latlng-estimation` | U - no explicit licence established | 2026-09-03 | 1 | Image-label position -> estimated geographic location. | C: Python Y; G: not required E; B: integration only | Use as a calibration/reference implementation, not universal camera geometry. [14] [59] |
| **OpenSidewalks/OpenSidewalks-Schema**<br>`https://github.com/OpenSidewalks/OpenSidewalks-Schema` | U - metadata does not identify a standard licence | 2026-10-20 | 63 | Pedestrian graph schema with nodes, edges, zones and accessibility metadata. | C: data/schema; G: not required; B: data | Use the concepts and a compatible GeoJSON edge model. [17] [62] |
| **wouterbohets/leuvenmapmatching**<br>`https://github.com/wouterbohets/leuvenmapmatching` | See source note below | U | U | Trace-to-network map matching. | C: E; G: not required E; B: no native UI | Match the camera trajectory first; it does not itself locate a visible obstacle.  |
| **cyang-kth/fmm**<br>`https://github.com/cyang-kth/fmm` | See source note below | U | U | Fast map matching for GPS trajectories. | C: E; G: not required E; B: no native UI | Useful for larger photo sequences; not a one-image pixel-to-world solution. [92] |

OSM's `sidewalk=*` describes the presence of sidewalks associated with a road; separately mapped sidewalks require a distinct graph representation. A walking road-centerline network is not proof of a separate, continuous footpath. [90]

**Proposed image-to-segment pipeline:**

1. **Keep the observation and inferred location separate.** Store image ID/provider, capture timestamp, camera GPS, heading, camera type, bounding box/mask, class, confidence and reviewer status.
2. **Resolve projection before geometry.** A perspective-image pixel and an equirectangular-panorama pixel need different camera models. Use heading to form a bearing, and depth/ground-plane evidence only when available. Camera GPS is not the obstacle's GPS.
3. **Generate several segment candidates.** Compare bearing, distance, side of street, graph geometry and consistency across nearby views. Do not force the globally nearest edge.
4. **Treat uncertainty explicitly.** If opposite-side footpaths are plausible, retain candidates and request a map click. Save the review rather than burying it inside a confidence score.
5. **Split and connect the graph deliberately.** Attach an obstacle interval to the appropriate edge; keep crossing/ramp transitions explicit. Deduplicate repeated observations, and distinguish temporary blockage from persistent infrastructure.

For tonight, use a **manual "assign to this footpath" control** as part of the product, not as an embarrassment. The useful demonstration is that a corrected observation changes the correct route edge and leaves the opposite footpath unaffected.

**Source-specific map-matcher details:**

- License: Apache-2.0. [92]   Code/source URL: https://github.com/cyang-kth/fmm [92]   Function: Open-source map-matching framework integrating hidden Markov models and precomputation; it matches noisy GPS data to a road network. [92]   Release/update/stars: 1,055 stars; 369 commits; created 2017-10-27. [92]   CPU operation: C++ implementation using Rtree, optimized routing, and OpenMP parallel computing. [92]   Inputs: OpenStreetMap or ESRI shapefile road networks, and Point CSV, Trajectory CSV, or Trajectory Shapefile GPS data. [92]   Wheelchair/footpath graph support and custom obstacle weights are not specified in the source.   Limitations: direct OSM input was removed because raw datasets may contain topology errors; shapefile input from osmnx is suggested. [92]

**Decision:** build a reviewed two-sided pedestrian graph before trying to automate all geolocation.


## 5. Choose Routing By Barrier Control, Not By Brand Recognition

AccessMap is the closest architectural reference: its current infrastructure repository combines a React application with the **Unweaver** routing engine and expects externally generated pedestrian data. It is not a complete Jaipur dataset or a one-command universal accessibility router. [13]

GraphHopper, Valhalla and OTP solve different integration problems. GraphHopper supports custom routing models; Valhalla exposes runtime edge/vertex costing; OTP builds multimodal networks from sources such as OSM and GTFS and exposes GraphQL APIs. Those capabilities do not mean your image-derived barrier table is automatically consumed. [15][12][6]

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **TaskarCenterAtUW/AccessMap**<br>`https://github.com/TaskarCenterAtUW/AccessMap` | U - inspect component licences | 2026-10-14 | 2 | Accessibility-preference-aware pedestrian routing app/infrastructure. | C: E; G: unnecessary; B: Y UI | Best reference for UX/data integration; heavier than a small custom prototype. [13] [63] |
| **TaskarCenterAtUW/unweaver**<br>`https://github.com/TaskarCenterAtUW/unweaver` | U - see source details | U | U | Composable research routing engine used by AccessMap. | C: E; G: unnecessary; B: API client | Candidate for profile-specific edge costs if its example runs immediately. [100] |
| **gboeing/osmnx**<br>`https://github.com/gboeing/osmnx` | MIT | 2026-07-31 | 5877 | Download/model OSM networks and support graph analysis/routing. | C: E; G: unnecessary; B: exported map/API | Recommended graph acquisition/scaffolding; review missing footpaths and custom weights. [4] [20] |
| **GIScience/openrouteservice**<br>`https://github.com/GIScience/openrouteservice` | GPL-3.0 | U | U | Routing service with wheelchair-specific request restrictions. | C: E server; G: unnecessary; B: client | Strong off-the-shelf option; verify local data and barrier-update workflow. [98] [94] |
| **opentripplanner/OpenTripPlanner**<br>`https://github.com/opentripplanner/OpenTripPlanner` | U in reviewed metadata; inspect LICENSE | 2026-10-14 | 2755 | Multimodal journey planner with wheelchair options. | C: Y JVM; G: unnecessary; B: GraphQL client | Prefer if transit and station accessibility are central; excessive setup for a tiny street-only demo. [6] [91] [65] |
| **valhalla/valhalla**<br>`https://github.com/valhalla/valhalla` | MIT | 2026-10-19 | 6355 | C++ routing engine with dynamic runtime costing. | C: Y native; G: unnecessary; B: API client | Useful production foundation; custom barriers still need ingestion/cost integration. [12] [64] |
| **graphhopper/graphhopper**<br>`https://github.com/graphhopper/graphhopper` | Apache-2.0 | 2026-10-07 | 6726 | Java routing engine with custom models and elevation/access support. | C: Y Java; G: unnecessary; B: API client | Custom models are useful, but do not assume a turnkey current wheelchair profile. [15] [66] |
| **pgRouting/pgrouting**<br>`https://github.com/pgRouting/pgrouting` | Mostly GPL-2.0-or-later; component exceptions | 2026-09-27 | 1435 | Routing algorithms inside PostGIS/PostgreSQL. | C: E database; G: unnecessary; B: your API | Good if PostGIS already works; keep obstacle costs in your own edge table. [11] [67] |
| **Routino**<br>`http://www.routino.org/software/` | See exact source details below | U | U | OSM-based routing with configurable profiles. | C: E; G: unnecessary; B: web frontend | A lightweight alternative to inspect, not assumed to have modern live barrier ingestion. [99] |

**Takeaway:** a sophisticated engine cannot repair a missing sidewalk graph or wrong-side obstacle assignment. For a bounded demo, controlling the graph and showing why an edge is excluded matters more than nationwide routing throughput.

**Documented profile details and limits:**

- Wheelchair routing restrictions are available through `options.profile_params.restrictions` for the `wheelchair` profile. [94] `surface_type` specifies the minimum surface type; the default is `"cobblestone:flattened"`. [94] `track_type` defaults to `"grade1"`, and `smoothness_type` defaults to `"good"`. [94] `maximum_sloped_kerb` accepts `0.03`, `0.06` (default), `0.1`, or `any`. [94] `maximum_incline` accepts `3`, `6` (default), `10`, `15`, or `any` percent. [94] `minimum_width` specifies the minimum road width in meters. [94]  The `avoid_features` array can avoid `steps`; `steps` is available for wheelchair profiles. [94] `ferries` can also be avoided for wheelchair routing. [94] The wheelchair example combines both with surface, track, smoothness, kerb, and incline restrictions. [94] Weightings prioritize specified factors over the shortest path. [94] This source does not provide separate OSM guidance for footways versus street-side attributes, nor concrete cost values or graph-routing custom-weight syntax beyond these options.

- Wheelchair routing options include `inaccessibleStreetReluctance`, multiplying the cost of traversing a street edge that is not wheelchair-accessible, default `25.0` [91]; `maxSlope`, the maximum slope fraction, default `0.083` [91]; `slopeExceededReluctance`, default `1.0` [91]; and `stairsReluctance`, default `100.0` [91]. [91]  For elevators, `onlyConsiderAccessible` controls whether an entity must be explicitly marked wheelchair accessible [91]. Stops and trips default to `onlyConsiderAccessible: true`, with inaccessible cost `3600` and unknown-accessibility cost `600` [91]. The supplied evidence does not specify kerb, width, surface, separately mapped footway, or custom graph-weight guidance.

- Wheelchair-specific profiles, kerb costs, slope costs, and separately mapped footway versus street-side attributes are not provided in the evidence corpus.  - Vehicle width: default 1.6 m for car, bus, and taxi; 2.6 m for truck. [95] - Vehicle length is specified in meters. [95] - Steps factor is a beta factor multiplying the cost of steps or stairs; its range is 0.1 to 100000 and its default is 8. [95] - Avoid-bad-surfaces ranges from 0 to 1; 1 completely disallows bad surfaces, including start and end points, and the default is 0.25. [95] - Shortest changes costing to quasi-shortest, purely distance-based costing, disables other costings and penalties, and defaults to false. [95] - Linear cost factors are customized cost factors specified as an array of JSON objects. [95] - Objects can be GeoJSON LineString features or plain objects with a shape key containing an encoded six-digit-precision polyline. [95] - Factors greater than 1 increasingly avoid edges; factors less than 1 increasingly favor them; the default is 1. [95]

- Source: https://github.com/TaskarCenterAtUW/unweaver [100]   License: A LICENSE file is present, but its license type is not stated. [100]   Function: Unweaver is a flexible routing engine that reads formats including OpenStreetMap, finds shortest-path routes through a web API, and supports customizable cost functions and direction specifications through profiles. [100]   Release/update/stars: Not stated in the provided source.   CPU operation: Not stated in the provided source.  Wheelchair/footpath graph: The example uses a sidewalk network and produces a routable GeoPackage graph. [100] The example weighting uses a precalculated value for a stereotyped manual wheelchair user. [100]   Custom obstacle weights: The system supports heavily parameterized, per-user dynamic edge costs and customizable cost functions. [100]   Inputs: It can ingest linear formats processable by GDAL, including GeoJSON and Shapefiles. [100]   Limitations: Non-Python dependencies are required. [100] The graph describes a digraph rather than a multidigraph, while multidigraph support is planned. [100] Example sidewalk data must be requested from the Taskar Center or repository author. [100]

- Routino is an application for finding a route between two points using OpenStreetMap topographical data. [99] A custom database is generated from raw OpenStreetMap XML data. [99] An optimum shortest or quickest route is determined from two latitude/longitude points. [99] Routes support common transport forms including foot, bicycle, horse, motorcar and motorcycle. [99]  The software records highway types, transport permissions, speed limits, one-way restrictions, weight, height, width and length limits. [99] Transport weight, height, width and length can be specified, and road-property preferences can be selected. [99] The simplest type of turn restrictions is obeyed. [99] Wheelchair routing, custom obstacle weights and a dedicated wheelchair/footpath graph are not stated. [99]  An HTML route description, GPX track or route file, and plain-text data files can be produced. [99] The design aims include flexible routing preferences, sensible defaults and very fast route finding. [99] The route is only as good as the input data, and the software has no warranty. [99]  Routino is free software under the GNU Affero General Public License, version 3 or later. [99] Source code is available from the download directory and Subversion repository. [99] Version 3.4.4 is listed with changes including Python-script replacement, HTML and Javascript modernization, and bug fixes. [99] No star rating is stated. [99]

**Proposed demo cost model, not a published safety standard:**

`edge_cost = length * preference_multiplier + surface_penalty + obstruction_penalty + uncertainty_penalty`

Apply **hard exclusions first** for reviewed impassable steps, an unusable crossing transition, or a confirmed full-width blockage. Use separate wheelchair and elderly-walker profiles, expose each profile's settings, and do not quietly convert an unknown width or slope into zero risk. If all paths violate the selected constraints, return **"No verified accessible route"**, not a fabricated safe detour.


## 6. Depth And 3D Improve Inspection, Not Automatic Safety Certification

### Metric3D versus relative depth: different evidence, different promises

Depth Anything V2 has separately licensed size variants: **Small weights are Apache-2.0**, while **Base/Large/Giant weights are CC-BY-NC-4.0**. Its default relative-depth predictions and its separately fine-tuned metric models must not be conflated. [25]

Metric3D predicts metric depth and surface normals, but its documentation warns about focal-length effects and unusual views/objects. UniDepth is another metric-depth candidate, with a **CC BY-NC 4.0** licence and a documented V2 release on **28 February 2025**. Neither reviewed source establishes Jaipur kerb-height accuracy. [28][23]

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **DepthAnything/Depth-Anything-V2**<br>`https://github.com/DepthAnything/Depth-Anything-V2` | Code/Small: Apache-2.0; larger weights: CC-BY-NC-4.0 | 2026-03-24 | 9020 | Single-image relative depth; separate metric checkpoints. | C: E small; G: E small, untested; B: documented Transformers.js path | Use Small for a preview; do not label arbitrary depth values as centimetres. [25] [71] |
| **YvanYin/Metric3D**<br>`https://github.com/YvanYin/Metric3D` | BSD-2-Clause code; verify checkpoint conditions | 2025-03-13 | 2336 | Metric depth and normals from one image. | C: ?; G: ?; B: outputs only | Candidate for ground-plane/step hypotheses after camera checks. [28] [70] |
| **lpiccinelli-eth/UniDepth**<br>`https://github.com/lpiccinelli-eth/UniDepth` | CC BY-NC 4.0 | 2025-05-18 | 1273 | Monocular metric-depth estimation. | C: ?; G: ?; B: outputs only | Compare geometry estimates offline; do not deploy unverified thresholds as safety facts. [23] [69] |

For a genuine height/slope estimate, the proposed pipeline is camera calibration -> back-projected 3D -> robust local ground plane -> elevation difference or plane angle -> uncertainty estimate. Camera pitch, scale error, occlusion and the model's smoothing of a thin kerb can invalidate the result. A "depth heatmap" is a useful visual aid, not a kerb-height instrument.

### Reconstruct a scene before considering an invented world

Nerfstudio offers a mature capture/processing/training/viewer workflow, including COLMAP-based processing for images, video and 360 capture. It requires an NVIDIA CUDA card in its documented installation path. gsplat is an Apache-2.0 CUDA rasterization/training library, not a complete georeferenced accessibility application. [43][47]

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **nerfstudio-project/nerfstudio**<br>`https://github.com/nerfstudio-project/nerfstudio` | Apache-2.0 | 2025-07-29 | 12010 | NeRF/Gaussian scene workflow and web visualizer. | C: preprocessing only; G: CUDA required, 4GB ?; B: UI | Use overlapping team-owned capture; export a small precomputed scene. [43] [76] |
| **nerfstudio-project/gsplat**<br>`https://github.com/nerfstudio-project/gsplat` | Apache-2.0 | 2026-09-19 | 5803 | Fast Gaussian rasterization/training primitives. | C: not primary backend; G: CUDA, 4GB ?; B: separate viewer | Pair with poses/COLMAP and a browser viewer, not raw disconnected photos. [47] [19] |
| **facebookresearch/vggt**<br>`https://github.com/facebookresearch/vggt` | Checkpoint-specific; original noncommercial; commercial variant differs | 2026-05-19 | 14497 | Feed-forward cameras, depth, point maps and tracks. | C: ?; G: ?; B: Gradio UI only | Useful pose/geometry bootstrap; original versus commercial checkpoint matters. [50] [75] |
| **naver/mast3r**<br>`https://github.com/naver/mast3r` | CC BY-NC-SA 4.0 code; checkpoint conditions apply | 2025-06-30 | 3116 | Image-pair matching and sparse-global-alignment reconstruction. | C: ?; G: ?; B: demo UI | Try for overlapping images when pose is missing; not a geolocation guarantee. [41] [74] |
| **naver/dust3r**<br>`https://github.com/naver/dust3r` | CC BY-NC-SA 4.0; training/base-checkpoint conditions | 2025-09-24 | 7357 | 3D reconstruction from images of the same scene. | C: ?; G: ?; B: demo UI | Alternative geometry bootstrap, with licence restrictions and uncertain metric scale. [51] [73] |

**Decision:** do not promise real-time reconstruction on a **4 GB GPU**. Sparse, non-overlapping street photos, changing parked vehicles, and moving people are poor foundations for a faithful route reconstruction. A short, overlapping capture of one junction is a more credible optional showcase than an invented city-scale scene.

### World models, image-to-video, and monsoon editing: a separate synthetic layer

Voyager is particularly relevant to the request because it generates RGB-D video from a single image with an explicit camera path. Its documented **60 GB minimum / 80 GB recommended** GPU budget makes it a research/stretch component, not tonight's local inference path. [48]

The table preserves exact source-stated model/weight distinctions. Unstated CPU, 4 GB or browser inference support remains **U**, and a browser demo does not mean the backend model runs in the browser.

| Resource URL | Source-Stated Licence, Function, Version, Popularity And Compute Facts | Jaipur Integration Decision |
|---|---|---|
| `https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager` | Function: Voyager is a video diffusion framework that generates world-consistent 3D point-cloud sequences from a single image with a user-defined camera path, and generates aligned depth and RGB video for direct 3D reconstruction. [48] Its architecture jointly generates RGB and depth video and supports iterative scene extension. [48]  License/code/weights: The repository contains a LICENSE file. [48] Code and model weights were released on September 2, 2025; pretrained models can be downloaded with the provided Hugging Face command. [48] The exact license terms, GitHub stars, and download counts are not stated. [48]  Release/update: The repository was created on August 27, 2025, and lists 32 commits. [48] Later listed updates include HunyuanWorld-1.1 on October 22, 2025, HunyuanWorld-1.5 on December 18, 2025, and HY-World-2.0 on April 16, 2026. [48]  Hardware and control: Minimum GPU memory is 60 GB at 540p; 80 GB is recommended, with an NVIDIA CUDA GPU required. [48] Input is an image, and camera paths include forward, backward, left, right, turn_left, and turn_right; the path can also be modified in create_input.py. [48] Generated RGB-D video can be converted into a PLY point cloud. [48] The source distinguishes generated scene video from reconstructed point clouds, but does not state further camera-control limitations. [48] | Stretch only. Camera-controlled synthetic preview; custom Tencent licence must be read separately. Never use generated obstacles as map evidence. |
| `https://github.com/Wan-Video/Wan2.2` | Function: Wan2.2 is an open video-generation model supporting text-to-video, image-to-video, and text-image-to-video generation.[57][524.35][524.114] It also supports speech-to-video with audio, reference images, optional prompts, and pose-driven generation.[57]  License/code/weights: The repository is Apache-2.0 licensed.[57] The repository states that Wan2.2 inference code and model weights were released, but it does not specify a separate weights license.[57] Release date: July 28, 2025.[57] Latest listed updates include Wan2.2-Animate-14B integration into Diffusers on November 13, 2025, and Wan2.2-S2V-14B on August 26, 2025.[57] Stars/downloads are not provided.[57]  GPU and controls: An image-to-video command requires at least 80GB VRAM, while TI2V-5B can run on a GPU with at least 24GB VRAM, such as an RTX 4090.[57][524.118] Inputs/routes include text prompts, images, audio, and optional pose videos.[57][524.132-137] Image-to-video follows the input image aspect ratio, and the model can generate solely from an input image.[57][524.110-111] Pose-driven generation is specifically supported through the pose-video parameter.[57] The corpus does not describe camera-control inputs, explicit camera-control limitations, or reconstructed views; the documented output is generated video.[57][524.141-143] | Optional pre-rendered image-to-video. Native GPU requirements exceed the proposed 4 GB budget. |
| `https://github.com/Lightricks/LTX-Video` | Function: "This is the official repository for LTX-Video." "Support text-to-video and image-to-video generation." [44] "You can now generate a video conditioned on a set of images and/or short video segments." [44]  License: "License: Apache-2.0 license." [44] "New license for commercial use (OpenRail-M)." [44] Exact code/weights licensing details beyond these statements are not provided. Stars/downloads are not provided.  Release/update: "Initial release of LTX-Video." [44] "LTX-Video now supports up to 60 seconds of video." [44] "LTX-2 is now the primary home for LTX development." [44]  GPU VRAM: "Requires only 1GB of VRAM." [44] Hardware-specific requirements for the general repository are not provided.  Input/routes and camera control: "For image-to-video generation." [44] "Extending a video." [44] "For video generation with multiple conditions." [44] "Specify camera angles and movements." [44] "Multi-keyframe conditioning, 3D camera logic, and LoRA fine-tuning deliver frame-level precision and style consistency." [44] Input video segments must contain "a multiple of 8 frames plus 1," while the target frame number "should be a multiple of 8." [44]  Reconstructed versus generated views: The corpus does not provide a distinction. | Optional pre-rendered route teaser; verify exact weight licence and memory configuration. |
| `https://github.com/Tencent-Hunyuan/HunyuanWorld-Mirror` | Function: HunyuanWorld-Mirror is a feed-forward model for comprehensive 3D geometric prediction. It accepts images and optional camera poses, depth maps, and calibrated intrinsics, and predicts point clouds, depths, normals, camera parameters, and 3D Gaussians. [56] [56] [56]  License: The repository lists `License.txt`, but the supplied text does not include the exact license code. [56] Weights: `huggingface-cli download tencent/HunyuanWorld-Mirror --local-dir ./ckpts`; inference can download weights automatically. [56]  Release/update: Inference code and model weights were released October 22, 2025; training and evaluation code were released November 7, 2025. [56] Stars/downloads: not stated in the supplied repository text. [56]  GPU VRAM: no requirement is stated; the documentation recommends CUDA 12.4 and provides CPU fallback in the example. [56] [56] Camera control: provide camera poses and/or intrinsics as priors using `cond_flags`; otherwise these priors are optional. [56] Limitations: the supplied text does not specify further camera-control limitations. [56]  Reconstructed outputs include world-coordinate 3D point clouds, camera-frame depth and normals, camera poses, and 3D Gaussian parameters. [56] Generated views are novel views rendered using 3D Gaussians. [56] | Geometry/world-reconstruction candidate; separate its actual output from generative preview claims. Not the critical path. |
| `https://huggingface.co/Qwen/Qwen-Image-Edit` | Function: Qwen-Image-Edit is an image-editing model supporting semantic and appearance editing, including bilingual Chinese/English text editing.[53] It accepts an input image and text prompt through Diffusers.[53]  License/weights: Apache 2.0; 20B parameters, BF16 tensor type.[53][527.85-88] No exact release or update date is provided; the associated technical report is dated August 4, 2025.[53][527.112] The page shows 2.55k likes and 117,164 downloads last month.[53][527.83]  GPU VRAM: An actual VRAM requirement is not specified. The example uses BF16 on CUDA, with MPS noted for Apple devices.[53] Camera/input control: viewpoint editing is prompted from an input image and can rotate objects 90 or 180 degrees, including showing the object's back.[53][527.60] Limitations: the source does not state a dedicated camera-control interface or quantitative hardware requirement.[53][527.60] The examples are described as semantic editing and novel-view synthesis, but the source does not distinguish reconstructed views from generated views.[53] | Optional rain/season illustration. Preserve the original, label the edit synthetic, and never feed it back as a real barrier observation. |

For a monsoon illustration, ask an editor to depict rain/wet surfaces while keeping scene layout, but treat even "preserve geometry" as a generation request, not a guarantee. Do not infer flood depth, slip risk, drainage capacity, or wheelchair passability from edited pixels. The safer tonight feature is a **real-image route slideshow** with capture dates and arrows; any generated version belongs behind an explicit "Synthetic scenario" toggle.


## 7. Browser Components And Less-Obvious Fork Candidates

### Render the route and its evidence before adding a 3D spectacle

MapLibre handles the base map; deck.gl can render the route, candidate segments, barriers and uncertainty layers. Potree and Gaussian splat viewers solve a different problem: presenting precomputed 3D assets. None of these components supplies missing accessibility truth.

| Resource / URL | Licence | Observed Code Push Or Dated Release | Stars / Downloads | What It Does | CPU / 4 GB GPU / Browser | How To Combine It |
|---|---|---|---|---|---|---|
| **maplibre/maplibre-gl-js**<br>`https://github.com/maplibre/maplibre-gl-js` | See repository licence; API metadata is NOASSERTION | 2026-10-11 | 11852 | Interactive vector maps in the browser. | C: browser CPU; G: WebGL device-dependent; B: Y | Recommended basemap/GeoJSON line and point UI. [38] [18] |
| **visgl/deck.gl**<br>`https://github.com/visgl/deck.gl` | MIT | 2026-10-11 | 14652 | GPU geospatial layers and picking. | C: browser CPU; G: WebGL device-dependent; B: Y | Optional overlay for evidence points, routes, footprints and comparison layers. [52] [77] |
| **potree/potree**<br>`https://github.com/potree/potree` | See source note below | 2026-01-08 | 5645 | Large point-cloud browser viewer. | C: browser CPU; G: device-dependent; B: Y | Use for an actual reconstructed point cloud, not as the routing frontend. [55] [80] |
| **mkkellogg/GaussianSplats3D**<br>`https://github.com/mkkellogg/GaussianSplats3D` | MIT | 2025-10-19 | 2919 | Three.js Gaussian splat viewer. | C: browser CPU; G: device-dependent; B: Y | Load a precomputed small splat scene in an optional tab. [39] [78] |
| **playcanvas/supersplat**<br>`https://github.com/playcanvas/supersplat` | MIT | 2026-10-05 | 10313 | Browser Gaussian splat editing/viewing. | C: browser CPU; G: device-dependent; B: Y | Crop/clean a captured scene; do not spend the core nine hours learning reconstruction. [49] [82] |

A browser application does not require a CUDA installation on the visitor's machine, but large point clouds/splats can still exhaust browser memory or perform poorly on phones. Start with the route map and image evidence, then add 3D only if it improves the explanation.

**Browser licence/format details from the primary repositories:**

- - Project URL: https://github.com/maplibre/maplibre-gl-js [38] - License: MapLibre GL JS is licensed under the 3-Clause BSD license. [38] - Release/update/stars: Not stated in the source. [38] - Browser hardware: Not stated; the source only says rendering is GPU-accelerated. [38] - Useful layers/formats: GPU-accelerated vector tile rendering; examples include heatmap layers, 3D buildings, and population-density visualization. [38] - Route visualization integration: Not stated in the source. [38]

- URL: https://github.com/potree/potree [55]   Potree is a free open-source WebGL based point cloud renderer for large point clouds. [55]   LAS and LAZ support have been taken from the laslaz.js implementation of plas.io. [55]   License, release/update, stars, browser hardware, useful layers, and integration with route visualization are not stated in the provided source. [55]

### Chinese, Japanese and Korean leads: separate real artifacts from attractive names

The most useful verified regional discoveries are below. A repository being publicly visible does **not** establish permission to fork, redistribute data, or deploy weights. For fields not explicitly stated in the primary note, last update, popularity and CPU/4 GB/browser support remain **U**.

| Resource URL | Source-Stated Licence, Function, Version, Popularity And Compute Facts | Jaipur Integration Decision |
|---|---|---|
| `https://github.com/ChelseaGH/sidewalk_prototype_AI_Hub` | Actual implementation: The repository contains `darknet_ros/`, `psmnet/`, `zed-ros-wrapper/`, `CMakeLists.txt`, and `README.md`. [93] The Darknet_ros node detects objects, while PSMnet estimates depth; the system combines both outputs. [93] Pre-trained YOLOv3 and PSMNet weights are provided through download links. [93]  README/proposal: It describes the project as a prototype application of the SideGuide benchmark dataset. [93] URL: https://github.com/ChelseaGH/sidewalk_prototype_AI_Hub [93] Release/update/stars are not specified in the source. License: the source does not state an open-source software license; SideGuide data requires its copyright notice. [93]  Reusable: The ROS integration, object-detection workflow, depth-estimation workflow, and downloaded model weights are reusable. [93] Requirements include ZED SDK, ROS Kinetic, OpenCV, Python, PyTorch, torchvision, Ubuntu, and CUDA. [93] The source specifies CUDA but does not state CPU support or browser requirements. [93] Dataset original source: SideGuide, a publicly available sidewalk-navigation benchmark. [93] | Concrete SideGuide-related Korean sidewalk-navigation prototype. Useful taxonomy/sensor integration reference; not a live website shortcut. |
| `https://github.com/lengvietcuong/wheelchair-pathfinder` | Implemented code/checkpoints: The repository includes `main.py`, map-creation tools, A* pathfinding, benchmarking, map assets, and requirements. [97] The README describes standard and accessibility-aware searches, benchmarking, and an interactive CLI. [97] It provides setup commands using `pip install -r requirements.txt` and `python main.py`. [97]  URL: https://github.com/lengvietcuong/wheelchair-pathfinder [97]  License: Not specified in the source.  Release/update/stars: The provided evidence lists 29 commits and a default `main` branch, but no release, update, or star count. [97]  Reusable: The A* implementation, map-conversion tools, accessibility-cost logic, benchmark tooling, and map data are reusable components. [97] [97] [97]  CPU/GPU/browser needs: Not specified in the source. The application is run with Python from a shell. [97]  Dataset original source: The map is Central Park, New York City, drawn using Google Maps, with 23 nodes and 40 path segments. [97] The input map is a KMZ file used for path extraction. [97] | Small accessibility-aware A* application candidate; inspect map assumptions and licence. |
| `https://github.com/JezZh/tactile-path-segmentation` | - URL: https://github.com/JezZh/tactile-path-segmentation [96] - The repository contains training, evaluation, inference, benchmarking, ONNX, TensorRT, and temporal-cache code. [96] - The README reports a proposed compact SegFormer-B0 model and P-Strip strategy. [96] - Model weights and dataset images/masks are not included. [96] - Stars: 0; forks: 0; commits: 3; default branch: main. [96] - No license, release, or update information is provided in the source. [96] - Reusable components include the dataset loader, training/evaluation loops, model code, prediction script, benchmarks, and temporal-cache implementations. [96] - The stated deployment target is a Jetson Nano with TensorRT FP16; full-frame inference is reported at 1.70 FPS on that device. [96] - RTX 3090 benchmarks report approximately 116 FPS full-frame and 154 FPS with P-Strip. - CPU and browser requirements are not stated. - The dataset is described only as a custom pixel-level annotated dataset of 209 360-degree panoramic frames with five semantic classes; its original external source is not identified. [96] | Interesting tactile paving/curb segmentation lead; check whether code and weights actually exist before scheduling work. |
| `https://github.com/CMU-cabot/cabot-navigation` | Actual implemented code/checkpoints: "CaBot Navigation Packages" include cabot basic functions, behavior trees and plugins, robot URDF description, Gazebo launch files, multi-floor localization, message definitions, and core navigation logic using Nav2. [89] Tests are solely for navigation and localization. [89]  URL: https://github.com/CMU-cabot/cabot-navigation [89]   License: MIT license. [89]   Reusable components include multi-floor localization, mapping, RViz plugins, queue messages, and queue utilities. [89]   The corpus does not provide release, update, stars, CPU/GPU, browser, or dataset-original-source information. | Japanese-linked assistive-navigation ecosystem reference. ROS/robot deployment is not the same as a street-photo web app. |
| `https://github.com/yrmi99/SeoulElevatorGuide` | Implemented code/checkpoints: Top-level files include `public/`, `README.md`, `package-lock.json`, `package.json`, and `server.js`. [87] The repository has 8 commits. [87] README/proposal: "A web application that helps passengers find accessible routes with elevators in the Seoul Metro." [87] Features include "Search shortest accessible routes," "Step-by-step elevator guidance," and "Map view optional." [87]  URL: https://github.com/yrmi99/SeoulElevatorGuide [87]   License: Not stated in the source.   Release/update/stars: Not stated in the source.   Reusable: "It combines real-time subway route data (via ODsay API) with a curated dataset of elevator locations at stations." [87]   CPU/GPU/browser needs: Not stated in the source.   Dataset original source: Not stated in the source. | Useful accessible-route/elevator UI idea, but metro access is not sidewalk obstacle perception. |

Other concrete findings and exclusions:

- **SidewalkNet:** a unique, maintained, licensed artifact under this exact name was **not established**. Do not substitute Tile2Net, an unrelated Sidewalk Labs repository, or an arbitrary sidewalk-segmentation project and call it SidewalkNet.
- **SideGuide:** distinguish the sidewalk benchmark/prototype above from the unrelated developer-tools company returned under the same name.
- **Chinese tactile-paving listings:** results included YOLO-oriented dataset sales/tutorial claims, but no sufficiently established task-specific licensed release was identified for immediate reuse. A claim of thousands of images is not a verified downloadable open dataset.
- **Gitee/GitCode:** no additional verified task-specific licensed fork was established. **ModelScope** surfaced general object-detection models, but not a verified India-ready tactile-paving/barrier model. Do not mistake a mirror or generic detector for a new accessibility dataset.
- **GitLab:** a **Sidewalk Priority Toolkit** discovery describes a QGIS sidewalk-funding prioritization plugin, not image barrier detection or live wheelchair routing. Its exact reusable release was not established here.
- **WheeLog!** (`https://wheelog.com/en/`) and **Wheelmap** (`https://wheelmap.org/api/docs`) are useful accessibility-product/data leads. A reusable open source implementation with the required routing and imagery pipeline was not established here; treat them as adjacent, not verified tonight forks.
- **Community IDD code:** `https://github.com/IshanKuchroo/IDD-Indian-Driving-Dataset` and `https://github.com/Mohitasudani/idd_lite_segmentation` are candidate baseline implementations. They are not the official dataset licence or a verified accessibility detector; update, licence and hardware fields remain U here.

### Hackathon entries: inspiration is not verified working code or an award

Devpost entries can reveal useful product flows, but their narratives are self-reported. The following source notes preserve any actual repository links and explicitly distinguish missing licences or prize evidence. A winner claim is not inferred from appearing on Devpost.

| Resource URL | Source-Stated Licence, Function, Version, Popularity And Compute Facts | Jaipur Integration Decision |
|---|---|---|
| `https://devpost.com/software/pathable` | Project date: Mar 01, 2025. [34]  Actual repository/source link: No repository link is provided; the project lists pathable.vercel.app as its demo. [34]  License: Not stated. Prize: No prize win is explicitly stated; the project was submitted to Build With AI - UBC GDSC x Launchpad. [34]  Claimed functions: PathAble is a wheelchair-accessible route planner that generates optimized walking and transit routes while avoiding stairs, steep inclines, and inaccessible paths. [34]  Claimed technology: It integrates Google Maps APIs, Elevation Data, and Accessibility Filters. [34] The listed tools and technologies include Claude, Cursor, Google APIs, JavaScript, Lovable, OpenStreetMap, Supabase, TypeScript, and Vercel. [34]  Deployment constraints: The project reports lack of direct accessibility data, pedestrian-path limitations in Snap-to-Roads, and Google API query limits requiring optimization. [34] | Candidate only; do not make it a critical dependency tonight. |
| `https://devpost.com/software/accessgrid-ai` | Project date: May 29, 2026, based on the posted project updates. [32]   Repository/source: https://github.com/Ramachandranram4/AccessGrid-AI [32]   License: Not stated in the source.   Prize: No prize win is explicitly stated.   Functions: The project claims AI voice guidance, accessibility-aware routing, realtime obstacle detection, hazard reporting, safer-route recommendations, and voice-guided mobility support. [32]   Technology: Python, Gemini AI, OpenStreetMap, realtime computer-vision pipelines, voice interaction systems, and accessibility-aware routing logic. [32]   Deployment constraints: The source describes a mobile-first interface and realtime operation, but does not specify hosting, infrastructure, device, or network requirements. [32] | Candidate only; do not make it a critical dependency tonight. |
| `https://devpost.com/software/accessmapai` | Project date: The project was started on May 10, 2026. [37] It was submitted to HackDavis 2026. [37]  Repository/source: https://github.com/adiseshvsanklapur/AccessMapAI [37]  License: Not stated in the source. Prize: No prize is explicitly reported; the source identifies the HackDavis 2026 submission. [37]  Functions: Claim: AccessMap AI provides profile-aware, hazard-aware, explainable accessibility mapping; accessibility-optimized routes; route scoring; natural-language explanations; live hazard reporting and rerouting; AI sidewalk-photo analysis; and spoken navigation. [37]  Technology: The source lists OpenStreetMap, Open-Meteo Elevation API, Unitrans GTFS, NetworkX, Next.js, TypeScript, Tailwind CSS, shadcn/ui, Mapbox GL JS, Supabase Authentication, Web Speech API, FastAPI, and Gemini. [37] [37] [37]  Deployment constraints: Claim: Gemini analysis can use API quota, while mock mode supports offline demos without consuming quota. [37] The routing graph is based on open-source geospatial data and is described for UC Davis. [37] | Candidate only; do not make it a critical dependency tonight. |

**Decision:** do not replace a working map/image prototype with an untested hackathon repository simply because its description matches the problem. No task-specific hackathon winner with independently established award, licence, and functioning end-to-end barrier pipeline was confirmed in the reviewed material.


## 8. The Recommended Nine-Hour Fork-And-Merge Build

**Recommendation:** build a limited-area, evidence-first website with **MapLibre + one detector + a reviewed footpath graph + custom routing costs**. Use Project Sidewalk and AccessMap as component/design references, not as mandatory full-stack deployments. Their primary sources show substantial backend/data dependencies; avoiding those dependencies is a scheduling decision, not a judgment that the projects are poor. [16][13]

### The minimum architecture

| Layer | Tonight's Choice | Merge Contract | Fallback |
|---|---|---|---|
| Images | Team-owned Jaipur photos; permitted Mapillary imagery if local coverage and access work | Image ID, licence/attribution, capture time, GPS, heading, camera type | A preloaded, reviewed neighborhood gallery |
| Vision | Grounding DINO **or** Florence-2-base; optional existing small YOLO pipeline | Boxes/masks, class, confidence, model/version, original image dimensions | Precompute detections; keep image upload and human review live |
| Footpath masks | A compatible segmentation checkpoint only if already working; optional SAM refinement | Mask/polygon and confidence, not a claim of passability | Reviewer-drawn corridor and obstacle footprint |
| Geography | OSMnx/OSM as a starting point plus manually reviewed two-sided footpaths and crossings | Stable edge IDs and explicit graph connections | A small authored GeoJSON graph |
| Barrier association | Candidate edge assignment plus a correction control | Observation ID -> edge ID/interval, reviewer, confidence, timestamp | Explicit manual edge assignment |
| Routing | CPU shortest-path search with your own edge weights; Unweaver only if its example works quickly | Profile, excluded edges, penalties, explanation and route geometry | Preloaded graph, live rerouting after barrier toggles |
| Web | MapLibre; add deck.gl only for layers it simplifies | Route, candidate segments, evidence cards and attribution | Simple GeoJSON layers; no heavy 3D |
| Optional preview | Real image stepping; small precomputed splat scene | Clear distinction between observed and synthetic | Omit video generation entirely |

These are **proposed integration choices**, not measured performance claims. The important feature is a traceable chain from photo -> reviewed barrier -> specific edge -> changed route.

### A realistic timebox

| Time | Deliverable | Acceptance Test |
|---|---|---|
| **0:00-1:00** | Select a small Jaipur neighborhood; confirm lawful images; establish graph and deployment skeleton | The website loads a map, images and explicit footpath edges |
| **1:00-3:00** | Run one detector; store outputs; implement evidence cards | Click a detection and inspect its source image, class and confidence |
| **3:00-4:30** | Associate observations to candidate footpath edges; add manual correction | Move a barrier between opposite sides and see only the intended edge change |
| **4:30-6:00** | Implement wheelchair/elderly profiles, hard exclusions and penalties | A blocked edge causes a detour; a disconnected graph returns no verified route |
| **6:00-7:30** | Route comparison, legend, attribution, capture dates and review status | Users can explain why the recommended route differs from shortest distance |
| **7:30-8:30** | Integrate deployment, cache permitted artifacts and remove fragile dependencies | Demo survives a slow network/model failure |
| **8:30-9:00** | Rehearse and inspect every showcased edge/photo | No hidden wrong-side assignment or unsupported "safe" claim remains |

Parallelize image/vision, graph/routing, and frontend work if team size allows. Do not start training from scratch, a full-city graph import, or a world-model deployment unless the team already has that component running.

### The demo story judges should see

Show the shortest route crossing a **reviewed step/blockage**, the alternative route avoiding that edge, and the original image that explains the change. Then show an ambiguous detection being corrected to the opposite footpath and the route updating accordingly. Finish with an occluded location labeled **unknown**, and a case where the app refuses to claim a verified accessible route.

This is a more credible result than a citywide green route rendered over unverified road centerlines. Describe it as an **accessibility-aware prototype**, not a wheelchair-safety certification.


## Synthesis: Choose Evidence Over Coverage And Spectacle

| Strategy | Mechanism | Geographic Scope | Main Trade-Off | Evidence Base | Time Horizon |
|---|---|---|---|---|---|
| **Reviewed Jaipur graph + compact vision** | Detect candidates, verify edge assignment, apply explicit exclusions/costs | Small neighborhood | Less coverage, greater auditability | Local images and reviewer decisions | Best fit for tonight |
| **AccessMap / openrouteservice / production routing integration** | Rich pedestrian attributes and routing profiles | Potentially larger, if data exists | Integration and data preparation dominate | Structured map attributes; not image truth by itself | Next iteration after the demo |
| **Metric depth / VGGT / reconstruction** | Infer geometry and poses, reconstruct an observed scene | Well-captured segments | Calibration, overlap, compute and licence constraints | Estimated geometry from real observations | Optional experiment after the core works |
| **Generative video / monsoon editing** | Synthesize plausible views or weather | Apparent broad coverage | Can alter or invent accessibility-critical details | Synthetic content, not ground truth | Presentation-only stretch feature |

The non-obvious tension is that **more impressive visual coverage can mean weaker evidence**. A small graph with reviewed edges can support an honest routing decision; a generated walk-through cannot establish whether a kerb exists today. Conversely, a well-tested routing engine can still fail if the barrier was attached to the wrong side of the road.

Another tension is between **openness and usable rights**. MIT/Apache code can coexist with noncommercial weights, restricted imagery, unlicensed project data, or custom model terms. The catalogue keeps those layers separate because "the repository is public" is not a sufficient deployment decision.

**Final fork/merge choice:** start with **MapLibre + OSMnx/custom pedestrian graph + Grounding DINO or Florence-2 + a human correction panel + explicit CPU routing costs**. Add AccessMap/Unweaver concepts where useful, and postpone full 3D/world-model work. The outcome to optimize tonight is a route whose exclusions can be explained from real, attributed evidence.

### The Three Biggest Technical Risks

1. **Wrong-side localization and broken pedestrian topology.** A visually correct detection attached to the opposite footpath or a falsely connected crossing produces a wrong route. **Mitigation:** reviewed two-sided edges, explicit crossing nodes, candidate assignments and manual correction; never equate nearest road with correct sidewalk.

2. **Domain shift and false geometric certainty.** Jaipur's informal surfaces, drainage, vendors and parked two-wheelers differ from the source distributions; monocular depth can miss or smooth a small kerb. **Mitigation:** use the India-adapted taxonomy, review showcased images, separate temporary objects from infrastructure, and keep occluded/uncalibrated observations unknown rather than converting them into passable edges.

3. **Unavailable, stale or impermissible imagery plus integration/compute failure.** Coverage may fail exactly where a route needs evidence; old images can misrepresent current parking or construction; API restrictions or a heavy backend can break the live demo. **Mitigation:** lawful team-owned fallback photos, capture dates and observation expiry, precomputed model outputs, a small local graph, and no heavy world model on the critical path.

## References

1. *GitHub - VIDA-NYU/tile2net: Automated mapping of pedestrian networks from aerial imagery tiles · GitHub*. https://github.com/VIDA-NYU/tile2net
2. *GitHub - ProjectSidewalk/RampNet: RampNet is a two-stage pipeline that addresses the scarcity of curb ramp detection datasets by using government location data to automatically generate over 210,000 annotated Google Street View panoramas. This new dataset is then used to train a state-of-the-art curb ramp detection model that significantly outperforms previous efforts. · GitHub*. https://github.com/ProjectSidewalk/RampNet
3. *Towards Human-AI Accessibility Mapping in India: VLM-Guided Annotations and POI-Centric Analysis in Chandigarh*. https://arxiv.org/pdf/2602.09216
4. *GitHub - gboeing/osmnx: Download, model, analyze, and visualize street networks and other geospatial features from OpenStreetMap. · GitHub*. https://github.com/gboeing/osmnx
5. [GitHub - IDEA-Research/GroundingDINO: [ECCV 2024] Official implementation of the paper "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection" · GitHub](https://github.com/IDEA-Research/GroundingDINO)
6. *GitHub - opentripplanner/OpenTripPlanner: An open source multi-modal trip planner · GitHub*. https://github.com/opentripplanner/OpenTripPlanner
7. [GitHub - AILab-CVC/YOLO-World: [CVPR 2024] Real-Time Open-Vocabulary Object Detection · GitHub](https://github.com/AILab-CVC/YOLO-World)
8. *microsoft/Florence-2-base · Hugging Face*. https://huggingface.co/microsoft/Florence-2-base
9. *google/owlv2-base-patch16-ensemble · Hugging Face*. https://huggingface.co/google/owlv2-base-patch16-ensemble
10. *GitHub - facebookresearch/sam2: The repository provides code for running inference with the Meta Segment Anything Model 2 (SAM 2), links for downloading the trained model checkpoints, and example notebooks that show how to use the model. · GitHub*. https://github.com/facebookresearch/sam2
11. *GitHub - pgRouting/pgrouting: Repository contains pgRouting library. Development branch is "develop", stable branch is "master" · GitHub*. https://github.com/pgRouting/pgrouting
12. *GitHub - valhalla/valhalla: Open Source Routing Engine for OpenStreetMap · GitHub*. https://github.com/valhalla/valhalla
13. *GitHub - TaskarCenterAtUW/AccessMap: A sidewalk routing, accessibillity preferences-aware routing "app" for mobile web. · GitHub*. https://github.com/TaskarCenterAtUW/AccessMap
14. *GitHub - ProjectSidewalk/label-latlng-estimation · GitHub*. https://github.com/ProjectSidewalk/label-latlng-estimation
15. *GitHub - graphhopper/graphhopper: Open source routing engine for OpenStreetMap. Use it as Java library or standalone web server. · GitHub*. https://github.com/graphhopper/graphhopper
16. *GitHub - ProjectSidewalk/SidewalkWebpage: Project Sidewalk web page · GitHub*. https://github.com/ProjectSidewalk/SidewalkWebpage
17. *GitHub - OpenSidewalks/OpenSidewalks-Schema: Repository for the draft proposal of the OpenSidewalks schema · GitHub*. https://github.com/OpenSidewalks/OpenSidewalks-Schema
18. *Maplibre Gl Js*. https://api.github.com/repos/maplibre/maplibre-gl-js
19. *Nerfstudio Project*. https://api.github.com/repos/nerfstudio-project/gsplat
20. *api.github.com*. https://api.github.com/repos/gboeing/osmnx
21. *api.github.com*. https://api.github.com/repos/ProjectSidewalk/RampNet
22. *Idea Research*. https://api.github.com/repos/IDEA-Research/GroundingDINO
23. *GitHub - lpiccinelli-eth/UniDepth: Universal Monocular Metric Depth Estimation · GitHub*. https://github.com/lpiccinelli-eth/UniDepth
24. *CC-BY-SA license for open data – Mapillary*. https://help.mapillary.com/hc/en-us/articles/115001770409-CC-BY-SA-license-for-open-data
25. [GitHub - DepthAnything/Depth-Anything-V2: [NeurIPS 2024] Depth Anything V2. A More Capable Foundation Model for Monocular Depth Estimation · GitHub](https://github.com/DepthAnything/Depth-Anything-V2)
26. *Policies and attributions for Street View Static API  |  Google for Developers*. https://developers.google.com/maps/documentation/streetview/policies
27. *Google Maps Platform Terms Of Service | Google Cloud*. https://cloud.google.com/maps-platform/terms
28. *GitHub - YvanYin/Metric3D: The repo for "Metric3D: Towards Zero-shot Metric 3D Prediction from A Single Image" and "Metric3Dv2: A Versatile Monocular Geometric Foundation Model..." · GitHub*. https://github.com/YvanYin/Metric3D
29. *KartaView*. https://kartaview.org/doc
30. *SideSeeing: A multimodal dataset and collection of tools for sidewalk assessment*. https://arxiv.org/abs/2407.06464
31. *IDD*. https://idd.insaan.iiit.ac.in/
32. *AccessGrid AI | Devpost*. https://devpost.com/software/accessgrid-ai
33. *UrbanVGGT: Scalable Sidewalk Width Estimation from Street View Images*. https://arxiv.org/pdf/2603.22531
34. *PathAble | Devpost*. https://devpost.com/software/pathable
35. *API Documentation*. https://www.mapillary.com/developer/api-documentation
36. *segments/sidewalk-semantic · Datasets at Hugging Face*. https://huggingface.co/datasets/segments/sidewalk-semantic
37. *AccessMapAI | Devpost*. https://devpost.com/software/accessmapai
38. *GitHub - maplibre/maplibre-gl-js: MapLibre GL JS - Interactive vector tile maps in the browser · GitHub*. https://github.com/maplibre/maplibre-gl-js
39. *GitHub - mkkellogg/GaussianSplats3D: Three.js-based implementation of 3D Gaussian splatting · GitHub*. https://github.com/mkkellogg/GaussianSplats3D
40. *HuggingFaceTB/SmolVLM-256M-Instruct · Hugging Face*. https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct
41. *GitHub - naver/mast3r: Grounding Image Matching in 3D with MASt3R · GitHub*. https://github.com/naver/mast3r
42. *GitHub - ultralytics/ultralytics: Ultralytics YOLO27, YOLO26, YOLO11, YOLOv8 — object detection, instance segmentation, semantic segmentation, image classification, pose estimation, object tracking · GitHub*. https://github.com/ultralytics/ultralytics
43. *GitHub - nerfstudio-project/nerfstudio: A collaboration friendly studio for NeRFs · GitHub*. https://github.com/nerfstudio-project/nerfstudio
44. *GitHub - Lightricks/LTX-Video: Official repository for LTX-Video · GitHub*. https://github.com/Lightricks/LTX-Video
45. *GitHub - huggingface/transformers.js: State-of-the-art Machine Learning for the web. Run 🤗 Transformers directly in your browser, with no need for a server! · GitHub*. https://github.com/huggingface/transformers.js
46. *Qwen/Qwen2.5-VL-3B-Instruct · Hugging Face*. https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct
47. *GitHub - nerfstudio-project/gsplat: CUDA accelerated rasterization of gaussian splatting · GitHub*. https://github.com/nerfstudio-project/gsplat
48. *GitHub - Tencent-Hunyuan/HunyuanWorld-Voyager: Voyager is an interactive RGBD video generation model conditioned on camera input, and supports real-time 3D reconstruction. · GitHub*. https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager
49. *GitHub - playcanvas/supersplat: 3D Gaussian Splat Editor · GitHub*. https://github.com/playcanvas/supersplat
50. [GitHub - facebookresearch/vggt: [CVPR 2025 Best Paper Award] VGGT: Visual Geometry Grounded Transformer · GitHub](https://github.com/facebookresearch/vggt)
51. *GitHub - naver/dust3r: DUSt3R: Geometric 3D Vision Made Easy · GitHub*. https://github.com/naver/dust3r
52. *GitHub - visgl/deck.gl: WebGL2 powered visualization framework · GitHub*. https://github.com/visgl/deck.gl
53. *Qwen/Qwen-Image-Edit · Hugging Face*. https://huggingface.co/Qwen/Qwen-Image-Edit
54. *vikhyatk/moondream2 · Hugging Face*. https://huggingface.co/vikhyatk/moondream2
55. *GitHub - potree/potree: WebGL point cloud viewer for large datasets · GitHub*. https://github.com/potree/potree
56. [GitHub - Tencent-Hunyuan/HunyuanWorld-Mirror: [ICML 2026] WorldMirror: Fast and Universal 3D reconstruction model for versatile tasks · GitHub](https://github.com/Tencent-Hunyuan/HunyuanWorld-Mirror)
57. *GitHub - Wan-Video/Wan2.2: Wan: Open and Advanced Large-Scale Video Generative Models · GitHub*. https://github.com/Wan-Video/Wan2.2
58. *api.github.com*. https://api.github.com/repos/ProjectSidewalk/SidewalkWebpage
59. *Label Latlng Estimation*. https://api.github.com/repos/ProjectSidewalk/label-latlng-estimation
60. *Sidewalk Tagger Ai*. https://api.github.com/repos/ProjectSidewalk/sidewalk-tagger-ai
61. *Vida Nyu*. https://api.github.com/repos/VIDA-NYU/tile2net
62. *Opensidewalks Schema*. https://api.github.com/repos/OpenSidewalks/OpenSidewalks-Schema
63. *api.github.com*. https://api.github.com/repos/TaskarCenterAtUW/AccessMap
64. *api.github.com*. https://api.github.com/repos/valhalla/valhalla
65. *api.github.com*. https://api.github.com/repos/opentripplanner/OpenTripPlanner
66. *api.github.com*. https://api.github.com/repos/graphhopper/graphhopper
67. *api.github.com*. https://api.github.com/repos/pgRouting/pgrouting
68. *Yolo World*. https://api.github.com/repos/AILab-CVC/YOLO-World
69. *Lpiccinelli Eth*. https://api.github.com/repos/lpiccinelli-eth/UniDepth
70. *api.github.com*. https://api.github.com/repos/YvanYin/Metric3D
71. *Depth Anything V2*. https://api.github.com/repos/DepthAnything/Depth-Anything-V2
72. *api.github.com*. https://api.github.com/repos/facebookresearch/sam2
73. *api.github.com*. https://api.github.com/repos/naver/dust3r
74. *api.github.com*. https://api.github.com/repos/naver/mast3r
75. *api.github.com*. https://api.github.com/repos/facebookresearch/vggt
76. *Nerfstudio Project*. https://api.github.com/repos/nerfstudio-project/nerfstudio
77. *api.github.com*. https://api.github.com/repos/visgl/deck.gl
78. *api.github.com*. https://api.github.com/repos/mkkellogg/GaussianSplats3D
79. *api.github.com*. https://api.github.com/repos/huggingface/transformers.js
80. *api.github.com*. https://api.github.com/repos/potree/potree
81. *api.github.com*. https://api.github.com/repos/ultralytics/ultralytics
82. *api.github.com*. https://api.github.com/repos/playcanvas/supersplat
83. *User Reference ¶*. https://osmnx.readthedocs.io/en/stable/user-reference.html
84. *GitHub - navblind/Sidewalk-semantic-seg: Semantic segmentation for sidewalks. It has different models and options to train over. · GitHub*. https://github.com/navblind/Sidewalk-semantic-seg
85. *Information for Developers - Bhuvan Wiki*. https://bhuvan.nrsc.gov.in/wiki/index.php/Information_for_Developers
86. *Indian Driving Dataset (IDD Dataset)*. https://www.kaggle.com/datasets/mitanshuchakrawarty/new-idd-dataset
87. *GitHub - yrmi99/SeoulElevatorGuide: A web application that helps passengers find accessible routes with elevators in the Seoul Metro. It combines real-time subway route data (via ODsay API) with a curated dataset of elevator locations at stations. · GitHub*. https://github.com/yrmi99/SeoulElevatorGuide
88. *Mapillary*. https://www.mapillary.com/dataset/vistas
89. *GitHub - CMU-cabot/cabot-navigation · GitHub*. https://github.com/CMU-cabot/cabot-navigation
90. *Key:sidewalk - OpenStreetMap Wiki*. https://wiki.openstreetmap.org/wiki/Key:sidewalk
91. *Route Request - OpenTripPlanner 2*. https://docs.opentripplanner.org/en/latest/RouteRequest/
92. *GitHub - cyang-kth/fmm: Fast map matching, an open source framework in C++ · GitHub*. https://github.com/cyang-kth/fmm
93. *GitHub - ChelseaGH/sidewalk_prototype_AI_Hub: Prototype Sidewalk Navigation Application Based on the SideGuide Benchmark Dataset · GitHub*. https://github.com/ChelseaGH/sidewalk_prototype_AI_Hub
94. *Routing Options | openrouteservice backend documentation*. https://giscience.github.io/openrouteservice/api-reference/endpoints/directions/routing-options
95. *API reference - Valhalla Docs*. https://valhalla.github.io/valhalla/api/turn-by-turn/api-reference/
96. *GitHub - JezZh/tactile-path-segmentation · GitHub*. https://github.com/JezZh/tactile-path-segmentation
97. *GitHub - lengvietcuong/wheelchair-pathfinder: The Wheelchair Path Finder application allows users to find optimal routes in a mapped environment using the A* algorithm, with consideration for accessibility constraints such as slopes, kerb ramps, and sidewalk widths. · GitHub*. https://github.com/lengvietcuong/wheelchair-pathfinder
98. *GitHub - GIScience/openrouteservice: 🌍 The open source route planner api with plenty of features. · GitHub*. https://github.com/GIScience/openrouteservice
99. *Routino : Software*. http://www.routino.org/software/
100. *GitHub - TaskarCenterAtUW/unweaver: A flexible, composable config-based, research-oriented routing engine · GitHub*. https://github.com/TaskarCenterAtUW/unweaver
101. *KartaView*. https://kartaview.org/terms
