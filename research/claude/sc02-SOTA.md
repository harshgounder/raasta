# SC-02 research frontier + SOTA map (2023-2026), v1

Written 2026-10-24 16:22-16:40 IST by claude (sub-lane: SOTA). Source: ~28 Parallel web_search calls + 2 web_fetch batches (12 pages fetched), session `sc02-sota-7f3a9c1e2b4d6a8f0e1c3b5d7a9f2e4c`.
Read first: `research/WAVE-2-SC02-BRIEF.md`, `DECISIONS.md` (D1 SC-02, D2 all-India any time/weather).

## Grading used here (honest version of "VERIFIED")

| grade | meaning |
|---|---|
| **V-F** | page fetched with web_fetch this session; claim read on the primary page |
| **V-S** | primary page (the URL in the row) came back as a search hit this session and the claim is in its excerpt; page not fully opened |
| **UNV** | not seen this session (from memory, or only a secondary mention). Treat as a lead, not a fact |

Hardware column = my estimate for a GTX 1650 4 GB / 7 GB RAM box unless a number is quoted from the page. **All "4 GB ok" calls are UNVERIFIED predictions** until dsh smoke-tests them (S1 lane).

---

## 1. Sidewalk / kerb ramp / obstacle detection and sidewalk networks

| # | item (venue, date) | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 1 | **Towards Human-AI Accessibility Mapping in India: VLM-Guided Annotations and POI-Centric Analysis in Chandigarh** (AI4UP @ AAAI 2026; arXiv 2602.09216 v2 17 Feb 2026) | https://arxiv.org/html/2602.09216 | no code link seen on the paper page; data flows into Project Sidewalk (CC0, row 3) | **India label set** (US "Curb Ramp" replaced by "Curb Style": sloped edge, stepped drop, broken kerb, drainage gap; new obstacle tags parked car, carts, drainage, electric box; new no-sidewalk tag "too dirty/cluttered"); VLM guidance = **gemini-2.5-flash** fed OSM road type + first/last GSV pano of each segment; segment kept only if >=75% GSV coverage; severity weights 0.2 / 0.6 / 1.0 for severity 1/2/3; ~40 km audited, 1,644 fix locations | API (Gemini) | V-F |
| 2 | Project Sidewalk Chandigarh deployment (live, v11.13.0, updated 2026-09-16) | https://sidewalk-chandigarh.cs.washington.edu/ | Project Sidewalk is open source (MIT per DECISIONS D1 input) | Real Indian labelled panos to seed/test our detector; proof Indian deployment exists | web | V-S |
| 3 | Project Sidewalk API + **AccessScore** (streets, intersections, regions) | https://sidewalk-newberg.cs.washington.edu/api | **data CC0 1.0** (stated on page) | Ready label dump (CSV/GeoJSON) per city incl. Chandigarh; AccessScore formula to copy for our segment score | CPU | V-S |
| 4 | **RampNet**: bootstrapping kerb ramp detection from open government metadata (ICCV 2025 workshop; arXiv 2508.09415) | https://github.com/ProjectSidewalk/RampNet ; model https://huggingface.co/projectsidewalk/rampnet-model | **MIT** (repo + HF model); 90.1M params; 214,376 panos / 849,895 labels dataset (463 GB) | Pretrained kerb-ramp detector on 2048x4096 equirect panos -> heatmap; AP 0.9205 / P 0.949 / R 0.873 at thr 0.55 **with flip TTA** (single pass lower, page says so). US ramps, so on Indian kerbs it shows the domain gap (good "why we label our own" slide) | 4 GB: fp16 likely (UNV); CPU slow | V-F |
| 5 | Towards Fine-Grained Sidewalk Accessibility Assessment with Deep Learning: Initial Benchmarks and an Open Dataset (ASSETS 2024 poster) | https://dl.acm.org/doi/10.1145/3663548.3688531 | open dataset (link in paper, UNV) | 33 fine-grained conditions from 640x640 crops (too steep, no tactile, uneven, brick); finding: larger noisy training data hurt | 4 GB ok (classifier) | V-S |
| 6 | SideSeeing: multimodal dataset + tools for sidewalk assessment (arXiv 2407.06464; UrbanAccess 2024) | https://arxiv.org/abs/2407.06464 | tools released (licence UNV) | Chest-mounted video + IMU + GPS capture protocol (325k frames, 12 km); template for our own phone walk capture at MUJ | CPU | V-S |
| 7 | Tile2Net: sidewalk/crosswalk/footpath polygons + network from aerial tiles (CEUS 2023) | https://github.com/VIDA-NYU/tile2net | open source (licence UNV) | Footpath network where OSM has none; trained on US ortho tiles, India ortho availability is the blocker | 4 GB marginal | V-S |
| 8 | CitySurfaces (sidewalk material segmentation, Hosseini et al.) | not found this session | UNV | Surface material (asphalt, brick, tiles) as a cost term | ? | UNV (zero results this session) |
| 9 | **UrbanVGGT**: sidewalk width from a single street-view image (arXiv 2603.22531 v2 Aug 2026) | https://arxiv.org/abs/2603.22531 | code not linked on abs page | Pipeline: SegFormer-B5 sidewalk mask -> VGGT 3D -> ground plane fit -> camera-height scale -> width; MAE 0.252 m, 95.5% within 0.5 m (Washington DC). Copy this for width + kerb height | 4 GB: VGGT-1B tight (UNV) | V-F |
| 10 | Sidewalk width from SVI at two pitch angles + Canny + trigonometry (EPB: Urban Analytics 2026) | https://journals.sagepub.com/doi/10.1177/23998083251369602 | no code seen | Cheap no-depth width fallback | CPU | V-S |
| 11 | S2DB-Net: cross-view satellite + street-view sidewalk segmentation (ISPRS J 2026) | https://github.com/EdgedEnd/S2DB-Net | **MIT** | Fuse top-down + street view to find sidewalk presence | 4 GB marginal | V-S |
| 12 | Safety-oriented sidewalk and road segmentation for smartphone assistive navigation, SENSATION-DS (arXiv 2607.21137, Jul 2026) | https://arxiv.org/abs/2607.21137 | dataset 2,752 pairs (licence UNV) | **Road-as-Sidewalk Error Rate** = false-safe metric; SAM2 pseudo-labels; Android ONNX. Metric fits "unknown never safe" (D2) | phone / CPU | V-S |
| 13 | PEDESTRIAN: egocentric dataset for obstacle detection on pavements (arXiv 2512.19190, Dec 2025) | https://arxiv.org/abs/2512.19190 | dataset (licence UNV) | 29 pavement obstacle classes, 340 phone videos; extra training data | 4 GB ok | V-S |
| 14 | **Indian Footpath Damage Segmentation Dataset** (Scientific Data 2025, Pune) | https://www.nature.com/articles/s41597-025-06207-x | **open on Zenodo**, academic use | 583 Pune footpath images, pixel masks, severity low/med/high from crack width; Indian footpath surface damage labels ready | 4 GB ok (U-Net) | V-S |
| 15 | Validating pedestrian infrastructure data: SVI audits vs government field data (Urban Science 2025) | https://www.mdpi.com/2413-8851/9/4/130 | n/a | Evidence that SVI audits agree/disagree with field truth; Q&A defence | n/a | V-S |
| 16 | Sidewalk detection ensemble vs ONE-PEACE LLM (arXiv 2405.14876) | https://arxiv.org/pdf/2405.14876 | UNV | Ensemble segmentation beats an LLM for sidewalk pixels; supports "detector + VLM" split | 4 GB ok | V-S |
| 17 | 基于深度学习的盲道和盲道障碍物识别算法 (blind road + obstacle multi-task, 电子科技 2024) | https://journal.xidian.edu.cn/dzkj/CN/Y2024/V37/I3/75 | no code | One network: tactile-path segmentation + obstacle detection, mIoU 93.5, 18.5 FPS; pattern for "is obstacle ON the path" overlap test | 4 GB ok | V-S |
| 18 | 基于YOLOv8的盲道及盲道障碍物智能检测 (CSDN, May 2025) | https://blog.csdn.net/QQ_1309399183/article/details/148002695 | blog code | Overlap logic: obstacle mask intersect path mask -> blocked. Same rule we need for footpath | 4 GB ok | V-S |
| 19 | LPC-YOLO all-round obstacle detection for blind walking (计算机技术与发展 2025/26) | https://wjfz.cbpt.cnki.net/portal/journal/portal/client/paper/3354872651e983217b80a2ea7e003d15 | no code | YOLOv8n + small-object attention + monocular ranging | 4 GB ok | V-S |
| 20 | CNNを用いた階段認識とデプスカメラを用いた段差検出 (JSOD 2023) | https://www.jstage.jst.go.jp/article/jsod/21/1/21_78/_article/-char/ja/ | no code | Stair recognition + step (段差) detection for blind navigation | 4 GB ok | V-S |
| 21 | 深度画像のビュー変換を用いた路面の段差検知 (VRSJ AC2023) | https://www.conference.vrsj.org/ac2023/program/doc/2D2-04.pdf | no code | Depth -> point cloud -> rotate to bird's eye -> step edges. Works on monocular metric depth too | CPU | V-S |
| 22 | 휠체어 사용자를 위한 보도파손 경고시스템 (KIPS 2024) | https://www.manuscriptlink.com/society/kips/conference/ask2024/file/downloadSoConfManuscript/abs/KIPS_C2024A0261 | no code | YOLOv5 sidewalk damage warning for elderly wheelchair users + RTK geotag | phone | V-S |
| 23 | Tactile paving detection and tracking, Tenji10K dataset (IEEJ Trans 2024) | https://cir.nii.ac.jp/crid/1360869856034332288?lang=en | dataset (licence UNV) | Tactile tile detection (Indian metro areas have tactile tiles too) | 4 GB ok | V-S |
| 24 | Multi-faceted sensory substitution for curb alerting (arXiv 2408.14578) | https://www.alphaxiv.org/ko/abs/2408.14578 | custom curb dataset (UNV) | YOLOv8-seg curb segmentation for blind users | 4 GB ok | V-S |

## 2. VLMs for urban perception and accessibility auditing

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 25 | **Can VLMs Reliably Assess Sidewalk Accessibility Attributes from Pedestrian-Level Imagery?** (arXiv 2609.17882, 15 Sep 2026) | https://arxiv.org/abs/2609.17882 | **images + field-measured values released** | 4 VLMs, 514 Seoul images, width / long. slope / cross slope / pavement; **conformal prediction** gives 90% coverage; width best (half-width ~1.0 m); "no quantitative attribute reaches compliance precision", but CP says which attributes can screen. Direct recipe for our "needs a human look" refusal | API / local VLM | V-F |
| 26 | StreetViewAI: accessible street view with context-aware multimodal AI (UIST 2025) | https://dl.acm.org/doi/10.1145/3746059.3747756 | UNV | Gemini Flash 2.0 chat over GSV for blind users; 86.3% of 816 questions right. Shows the "ask the street" UX | API | V-S |
| 27 | OmniPath: multi-modal agentic framework for auditing wheelchair accessibility (arXiv 2606.24129, Jun 2026) | https://arxiv.org/abs/2606.24129 | paper CC BY 4.0; code UNV | Agent virtually traverses network in 0.5 m steps with 3D elevation data; finds barriers <20 mm invisible to 2D maps | API + GIS | V-S |
| 28 | From images to insights: ChatGPT + Google Street View walkability (Transportation Research D, 2026) | https://www.sciencedirect.com/science/article/pii/S1361920926000386 | no code seen | Scores + narrative of negatives per image, validated vs humans and CV | API | V-S |
| 29 | Urban walkability through different lenses: GPT-4o vs human (PLOS One, Apr 2025) | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0322078 | n/a | Where GPT-4o and people disagree on accessibility/safety | API | V-S |
| 30 | SAGAI: Streetscape Analysis with Generative AI (2025) | https://www.sciencedirect.com/science/article/pii/S1195103625000199 | **open source, CC BY 4.0 paper**, runs on free cloud | Bounding box in -> OSM + GSV + light LLaVA -> mapped scores. Closest forkable "bbox to map of VLM scores" pipeline | Colab / 4 GB small LLaVA (UNV) | V-S |
| 31 | Can an LLM assess urban design quality? walkability metrics (arXiv 2504.21040) | https://arxiv.org/abs/2504.21040 | n/a | Ontology-structured prompts raise GPT-4 reliability; prompt template idea | API | V-S |
| 32 | MSEF: VisualGLM-6B + GPT-4 street assessment, Harbin (arXiv 2506.05087) | https://arxiv.org/abs/2506.05087v1 | UNV | LoRA fine-tune on 15k street images, F1 0.84 objective features | GPU >4 GB | V-S |
| 33 | WalkCLIP (arXiv 2511.21947) | https://arxiv.org/html/2511.21947v1 | UNV | CLIP fine-tuned on GPT-4o pedestrian captions for walkability | 4 GB ok | V-S |
| 34 | ChatGPT vision reasoning + multisource spatial data for walkability (CEUS 2025) | https://www.sciencedirect.com/science/article/pii/S0198971525000729 | n/a | MLLM + spatial data fusion design | API | V-S |
| 35 | Multimodal walkability assessment + path optimisation with LLMs (BuildSys 2026) | https://dl.acm.org/doi/10.1145/3744256.3812561 | UNV | GPT-4o mini perceptual scores + Project Sidewalk labels -> routing cost. Nearest published twin of SC-02 | API | V-S |
| 36 | WalkVLM: aid visually impaired walking (ICCV 2025) | https://walkvlm2024.github.io/ ; code https://github.com/xiaoyuan1996/walkvlm | code released (licence UNV) | 12k video-annotation walking dataset; concise CoT reminders; good for blind-user mode | GPU | V-S |
| 37 | UrBench (AAAI 2025) | https://github.com/opendatalab/UrBench | eval code | GPT-4o 61.2% on urban multi-view tasks: numbers for "VLMs alone are not enough" | n/a | V-S |
| 38 | CityBench (KDD 2025 D&B, arXiv 2406.13945) | https://arxiv.org/abs/2406.13945 | UNV | 30 LLM/VLMs on urban tasks in 13 cities | n/a | V-S |
| 39 | CityCube: cross-view spatial reasoning in urban scenes (ACL 2026) | https://aclanthology.org/2026.acl-long.416.pdf | UNV | Lists urban VQA benchmarks; fine-tuned 2B beats proprietary on cross-view | n/a | V-S |
| 40 | Perceived walkability with SVI + explainable AI (Spatial Information Research, Nov 2025) | https://link.springer.com/article/10.1007/s41324-025-00656-7 | n/a | Sidewalk pixel share most sensitive factor (0.395) | 4 GB ok | V-S |
| 41 | **Qwen3-VL** (2B / 4B / 8B Instruct + Thinking) | https://github.com/qwenlm/qwen3-vl ; https://ollama.com/library/qwen3-vl:2b | **Apache 2.0** (HF card, ollama licence blob) | Local VLM judge: 2D grounding (boxes/points, JSON), 3D grounding, occlusion reasoning. 2B/4B on 4 GB via ollama q4 (UNV) | 4 GB (2B/4B q4) | V-S |
| 42 | Qwen2.5-VL grounding with JSON bbox output | https://qwenlm.github.io/blog/qwen2.5-vl | Apache 2.0 for 3B/7B (UNV) | Fallback VLM; stable JSON boxes | 4 GB (3B q4) | V-S |
| 43 | **Molmo2** (CVPR 2026) + **MolmoPoint** (Mar 2026) | https://github.com/allenai/molmo2 ; https://huggingface.co/allenai/Molmo2-8B | **Apache 2.0** | Pointing: "point at every pole on the footpath" -> pixel points -> SAM masks. MolmoPoint-8B 70.7% PointBench; Molmo2-4B exists | API/Colab (8B); 4B tight on 4 GB | V-S |

## 3. Open-vocabulary detection / segmentation (zero-shot)

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 44 | **SAM 3**: Segment Anything with Concepts (Meta, 19-20 Nov 2025; arXiv 2511.16719) + SAM 3.1 checkpoints (27 Mar 2026) | https://github.com/facebookresearch/sam3 | **SAM License** (custom); 848M params; needs Python 3.12, PyTorch 2.7, CUDA 12.6 | Text prompt "open drain", "pole on footpath" -> all instance masks. LVIS box AP 53.6 vs DINO-X 52.4 vs OWLv2* 45.5; SA-Co/Gold cgF1 55.7 vs Gemini 2.5 14.4 (from repo table) | 4 GB: tight / likely OOM at full res (UNV); Colab T4 ok (UNV) | V-F |
| 45 | **YOLOE**: Real-Time Seeing Anything (ICCV 2025; arXiv 2503.07465) | https://github.com/THU-MIG/yoloe ; https://docs.ultralytics.com/models/yoloe | **AGPL-3.0**; YOLOE-v8-S 12M params, 305.8 FPS (T4, text prompt) | Text, visual-exemplar and **prompt-free (4,585-name vocab)** detect+segment; re-parameterises into plain YOLO head after export. Best fit for detector A on GTX 1650 | **4 GB yes** (12-45M params) | V-F |
| 46 | DINO-X (IDEA, arXiv 2411.14347 v3 May 2025) | https://github.com/IDEA-Research/DINO-X-API | API examples repo Apache-2.0; model API-only via DeepDataSpace | Prompt-free "detect anything", LVIS-minival 59.8 AP; cloud second opinion | API | V-S |
| 47 | Grounding DINO 1.5 Pro / 1.6 Pro | https://github.com/IDEA-Research/DINO-X-API (benchmark table) | API-only | Older API option; 1.6 Pro LVIS-minival 57.7 | API | V-S |
| 48 | YOLO-World (CVPR 2024) | https://openaccess.thecvf.com/content/CVPR2024/papers/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.pdf | AGPL-3.0 via Ultralytics (Roboflow licence page) | Real-time open-vocab boxes; superseded by YOLOE for masks | 4 GB yes | V-S |
| 49 | OWLv2 (HF transformers) | https://huggingface.co/docs/transformers/en/model_doc/owlv2 | Apache 2.0 (UNV) | Text + **image-guided one-shot** detection: crop one Indian kerb drop, find more | 4 GB ok (base) | V-S |
| 50 | **Florence-2** large/base | https://huggingface.co/microsoft/Florence-2-large | **MIT** | Caption-to-phrase grounding, OD, region captions; independent second detector for the "two must agree" rule | 4 GB yes (0.23B / 0.77B) | V-S |
| 51 | RF-DETR (ICLR 2026) | https://github.com/roboflow/rf-detr | **Apache 2.0** (N to L); XL/2XL PML 1.0 | Fine-tune target once we have our own Indian labels; DINOv2 backbone transfers well (RF100-VL lead) | 4 GB: N/S train likely (UNV) | V-S |
| 52 | Ultralytics YOLO26 | https://docs.roboflow.com/models/model-licenses (listed) | AGPL-3.0 | Latest closed-set YOLO for fine-tune | 4 GB yes | V-S (mention only) |
| 53 | LLMDet (open-vocab detection with LLM supervision) | not found this session | UNV | Possible stronger open-vocab detector | ? | UNV (zero results) |
| 54 | SAM 2 | https://github.com/facebookresearch/sam2 | Apache 2.0 (UNV) | Box/point -> mask refine; video tracking along a walk | 4 GB (tiny/small) UNV | UNV |
| 55 | Gemini 2.5 as a detector (baseline row inside SAM 3 table) | https://github.com/facebookresearch/sam3 | API | Shows general VLMs are weak at exhaustive box detection (LVIS cgF1 16.1 vs SAM 3 40.6): use VLM to judge, not to box | API | V-F |

## 4. Monocular metric depth, height, slope

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 56 | **Depth Anything 3** (ByteDance Seed, Nov 2025) | https://github.com/ByteDance-Seed/depth-anything-3 | **DA3-SMALL 0.08B Apache, DA3-BASE 0.12B Apache, DA3METRIC-LARGE 0.35B Apache**; Giant/Large any-view CC BY-NC 4.0 | Metric depth + sky seg (DA3Metric-L), multi-view pose + depth (any-view), 3DGS head on Giant; DA3-Streaming <12 GB for long video | 4 GB: Small/Base yes, Metric-L fp16 likely (UNV) | V-F |
| 57 | Depth Anything V2 (NeurIPS 2024) + metric fine-tunes (Hypersim indoor, VKITTI outdoor) | https://github.com/DepthAnything/Depth-Anything-V2 | **Small Apache-2.0**; Base/Large/Giant CC-BY-NC-4.0 | Outdoor metric Small (24.8M) for kerb/step height; GGUF ports exist | **4 GB yes / CPU ok** | V-S |
| 58 | **MoGe-2 / MoGe-3** (Microsoft; MoGe-2 NeurIPS 2025) | https://github.com/microsoft/MoGe | code **MIT** (DINOv2 part Apache); moge-2-vits-normal 35M, vitb 104M, vitl 326M; MoGe-3 vitl 370M / vitg 1.25B | Metric point map + **normals** + FOV from one image: normals give ground slope, point map gives kerb step height directly. 60 ms ViT-L on 3090 | **4 GB yes (vits/vitb)** | V-F |
| 59 | UniDepthV2 (arXiv 2502.20110) | https://github.com/lpiccinelli-eth/UniDepth | **CC BY-NC 4.0** | Metric depth + camera intrinsics + confidence output; ViT-S variant; ONNX | 4 GB yes (ViT-S) | V-F |
| 60 | Depth Pro (Apple, ICLR 2025) | https://github.com/apple/ml-depth-pro | Apple custom licence (code + weights) | Sharp metric depth + focal length, 2.25 MP in 0.3 s on "standard GPU" | 4 GB: tight (UNV) | V-F |
| 61 | Metric3D v2 (TPAMI 2024) | https://github.com/YvanYin/Metric3D | BSD-2 code (repo says non-commercial use in one fork README); Replicate API | Metric depth + surface normals; "measure size of structures from a single image" | 4 GB (small) UNV; API | V-S |
| 62 | Floating No More: object-ground reconstruction, pixel height (CVPR 2025) | https://openaccess.thecvf.com/content/CVPR2025/papers/Man_Floating_No_More_Object-Ground_Reconstruction_from_a_Single_Image_CVPR_2025_paper.pdf | UNV | Pixel-height + perspective field: height of an object above ground without intrinsics | GPU | V-S |
| 63 | GeoCalib: single-image calibration (ECCV 2024) | https://github.com/cvg/GeoCalib | code Apache-2.0, weights separate licence | Gravity direction + focal from one photo -> level the ground plane -> slope + kerb height from depth; uncertainty output flags bad photos | 4 GB / CPU | V-S |
| 64 | Building height from single SVI via single-view metrology (ISPRS J 2022) | https://www.sciencedirect.com/science/article/abs/pii/S0924271622002106 | n/a | Vanishing points + segmentation + lines -> height. Classical cross-check for depth nets (two engines rule) | CPU | V-S |
| 65 | Single-image building height with shadow geometry (Remote Sensing 18(5) 801, Mar 2026) | https://www.mdpi.com/2072-4292/18/5/801 | n/a | Height proportional to shadow length; idea for daytime kerb/step height from shadows | CPU | V-S |
| 66 | StairNet + stair datasets (Sci Rep 2022; Mendeley 2023: 2,670 + 424 RGB, RGB-D variant) | https://data.mendeley.com/datasets/3jjdm6rn96/3 | dataset (licence on Mendeley, UNV) | Stair-line detection training data for "steps" class | 4 GB yes | V-S |
| 67 | RGB-D stair detection and estimation (Sensors 2023) | https://pmc.ncbi.nlm.nih.gov/articles/PMC9965719 | n/a | Riser height errors larger than width errors: warn that step height from images is the weak number | n/a | V-S |

## 5. Adverse conditions + domain shift to India

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 68 | **IDD-AW** (WACV 2024) | https://iddaw.github.io/ | dataset (IIIT-H licence, UNV) | 5,000 Indian frames, rain / fog / low light / snow, paired NIR, 4-level labels, **Safe mIoU** metric. Our night/rain/fog test set for D2 | n/a | V-S |
| 69 | IDD India Driving Dataset (WACV 2019, still the base) | https://idd.insaan.iiit.ac.in/dataset/details | dataset (registration) | 10,003 images (Hyderabad, Bangalore), labels incl. sidewalk, curb, "drivable fallback", billboard, auto-rickshaw, animal | n/a | V-S |
| 70 | IDD-3D | https://idd3d.github.io/ | dataset | LiDAR + cams Hyderabad, 223k 3D boxes; depth sanity check on Indian streets | n/a | V-S |
| 71 | ACDC (fog / night / rain / snow, 4,006 images, with clear-condition twin per image) | https://acdc.vision.ee.ethz.ch/ | dataset | Paired adverse vs normal image of same place: model "before/after monsoon" demo | n/a | V-S |
| 72 | Rein: VFMs for domain-generalised segmentation (CVPR 2024) | https://github.com/w1oves/Rein | code (licence UNV) | 1% trainable tokens on DINOv2/EVA02; strong night results | GPU >4 GB train | V-S |
| 73 | FADA: frequency-adapted VFM for DGSS (NeurIPS 2024) | https://proceedings.neurips.cc/paper_files/paper/2024/file/aaf50c91c3fc018f6a476032d02114d9-Paper-Conference.pdf | UNV | +0.7 to +2.9 mIoU on ACDC fog/night/rain/snow | GPU | V-S |
| 74 | MFuser: Mamba bridge VFM + VLM for DGSS (CVPR 2025) | https://openaccess.thecvf.com/content/CVPR2025/supplemental/Zhang_Mamba_as_a_CVPR_2025_supplemental.pdf | UNV | Cityscapes -> ACDC 54.0 mIoU (EVA02-L) | GPU | V-S |
| 75 | Continual test-time adaptation of VFMs in adverse weather, BGQD (CVPR 2026 Findings) | https://www.computer.org/csdl/proceedings-article/cvprf/2026/475700h689/2kpVrsHCypG | UNV | Mask2Former-DINOv2 still drops under weather; evaluated **on IDD-AW** | GPU | V-S |
| 76 | QPrompt-R1: real-time DGSS (ICLR 2026) | https://proceedings.iclr.cc/paper_files/paper/2026/hash/765871e77d2ca65126d3d64d31aa6908-Abstract-Conference.html | code released (per paper) | 54 FPS domain-generalised segmentation | 4 GB maybe (UNV) | V-S |
| 77 | MoCE-IR all-in-one restoration (CVPR 2025) | https://github.com/eduardzamfir/MoCE-IR | code + models (licence UNV) | Haze/rain/noise removal before detection; 11M small model | 4 GB yes (S) | V-S |
| 78 | DarkIR low-light restoration (CVPR 2025; NTIRE 2025 best) | https://github.com/cidautai/DarkIR | code + HF weights (licence UNV) | Night photos: denoise + deblur + brighten in one net | 4 GB yes (UNV) | V-S |
| 79 | DA-CLIP degradation-aware CLIP (ICLR 2024) | https://proceedings.iclr.cc/paper_files/paper/2024/hash/467e109270678b3e2b3c2e7fa6b3d575-Abstract-Conference.html | code (UNV) | Its controller **classifies degradation type** (rain/haze/dark): auto-tag every photo with condition -> per-condition confidence | 4 GB ok (UNV) | V-S |
| 80 | LoViF 2026 real-world all-in-one restoration challenge report (arXiv 2607.21118) | https://arxiv.org/abs/2607.21118 | 20 verified team methods | Current best real-world restoration recipes (blur, low light, haze, rain, snow) | varies | V-S |
| 81 | ExDA / MIRAGE all-in-one IR (ICLR 2026) | https://proceedings.iclr.cc/paper_files/paper/2026/file/3cb18c3c31ff1b77b97f4512abd5e4a6-Paper-Conference.pdf | UNV | Newer than PromptIR/MoCE-IR; MIRAGE tiny 6M | 4 GB yes (UNV) | V-S |
| 82 | Adverse-weather + low-light dataset index (Project Sarvadrushti) | https://github.com/Project-Sarvadrushti/Adverse-Weather-and-Low-Light-Vision-Datasets | list | Includes **Sand/Dust (Sand11K 2025)** and smoke: India dust storms, Diwali smoke | n/a | V-S |
| 83 | Waterlogging detection on roads from PMGSY citizen app images (C-DAC Pune, ISPRS Annals 2025) | https://isprs-annals.copernicus.org/articles/X-5-W2-2025/203/2025/isprs-annals-X-5-W2-2025-203-2025.pdf | no code seen | 1,000 Indian waterlogged-road images, segmentation; monsoon class precedent | 4 GB ok | V-S |
| 84 | Safety-aware multi-task perception for Indian roads: anomalies incl. **potholes, waterlogging**, drivable area, lanes (Sci Rep, Jul 2026) | https://pubmed.ncbi.nlm.nih.gov/42410140 | CMIRD dataset (Thiruvananthapuram, Nagercoil; access UNV) | mAP@50 0.877 anomaly detection on South Indian roads | 4 GB ok | V-S |
| 85 | Dark Zurich (night segmentation benchmark) | not opened | dataset | Night eval | n/a | UNV |

## 6. Potholes, road damage, open drains / manholes

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 86 | **RDD2022** multi-national road damage dataset incl. **India** (Geoscience Data Journal 2024) | https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547/1 | **CC BY 4.0** | 47,420 images, D40 = potholes; Indian subset for pothole class | 4 GB train YOLO-n/s | V-S |
| 87 | CRDDC 2022 challenge (IEEE BigData) | https://arxiv.org/abs/2211.11362 | winners' code (UNV) | Best F1 76.9% across 6 countries; India leaderboard | n/a | V-S |
| 88 | ORDDC 2024 (optimised road damage detection) + a submission repo | https://orddc2024.sekilab.global/data ; https://github.com/karmarv/orddc2024 | repo GPL-3.0 | Speed-optimised road damage models with released weights (V1 release) | 4 GB yes | V-S |
| 89 | YOLOv8-PD (Sci Rep 2024) | https://www.nature.com/articles/s41598-024-62933-z | UNV | Light RDD2022 detector; failure examples on potholes | 4 GB yes | V-S |
| 90 | MCPH-YOLO: manhole cover hazard states (Applied Soft Computing 2025) | https://www.sciencedirect.com/science/article/abs/pii/S1568494625008361 | dataset 11,561 images / 5 hazard states (access UNV) | Missing / broken / displaced manhole classes; mixed light and weather | 4 GB yes | V-S |
| 91 | MGB-YOLO manhole cover detection (Sci Rep 2023) | https://www.nature.com/articles/s41598-023-43173-z | UNV | Real-time manhole detection with stereo depth | 4 GB yes | V-S |
| 92 | Road surface anomalies dataset: **drain hole**, pothole, sewer cover, unpaved, **wet surface** (IEEE DataPort, Jul 2025) | https://ieee-dataport.org/documents/annotated-road-surface-anomalies-dataset-real-time-detection-using-yolov8 | DataPort terms (UNV) | 4,968 YOLO-format images; covers our drain + waterlogging classes | 4 GB yes | V-S |
| 93 | Roboflow manhole_cover dataset (classes good / broken / lose / **uncovered**) | https://universe.roboflow.com/manholecover/manhole_cover | Roboflow Universe licence per project (UNV) | 1,898 images incl. open manhole class | 4 GB yes | V-S |
| 94 | Roboflow pothole instance segmentation (780 images) | https://universe.roboflow.com/yolo-k0cch/potholes-detection-segmentation-4yi7g | **CC BY 4.0** | Pothole masks for area measure | 4 GB yes | V-S |
| 95 | Borewell pit / open pit detection | none found | none | Gap: no dataset found this session; use open-vocab ("open pit in ground") + own photos | n/a | gap logged |

## 7. Temporal change detection in street view

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 96 | CityPulse: street view time series change (AAAI 2024) | https://github.com/tianyuanhuang/citypulse | dataset 9,137 images / 757 locations; Siamese model | Detect "this footpath changed since last capture" (new encroachment / new ramp) | 4 GB ok | V-S |
| 97 | Street2Vec: self-supervised urban change from 15M London street images (CEUS 2024) | https://www.sciencedirect.com/science/article/pii/S0198971524000851 | UNV | Barlow Twins embeddings invariant to season/daytime, sensitive to structure change | 4 GB ok | V-S |
| 98 | **GeSCF**: zero-shot generalizable scene change detection with SAM (CVPR 2025) | https://arxiv.org/abs/2409.06214 | code (UNV) | Training-free change masks between two photos of same spot; +19.2% avg on SCD sets | 4 GB maybe | V-S |
| 99 | Segment Any Change / AnyChange (NeurIPS 2024) | https://arxiv.org/abs/2402.01188 | UNV | Training-free bitemporal SAM latent matching; point query for object-centric change | 4 GB maybe | V-S |
| 100 | Scene change detection with frozen DINOv2 + cross-attention (arXiv 2409.16850) | https://arxiv.org/abs/2409.16850 | UNV | Handles lighting/season/viewpoint differences | 4 GB ok | V-S |
| 101 | Large-scale GSV time series for urban change (Purdue I-GUIDE, Mar 2026) | https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1000&context=iguide | n/a | 13,115 time-series sets pipeline (GSV history scraping method) | n/a | V-S |

## 8. Feed-forward 3D, splats, world models

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 102 | **VGGT** (CVPR 2025 best paper) | https://github.com/facebookresearch/vggt | code commercial-friendly since 29 Jul 2025; **VGGT-1B-Commercial** checkpoint (no military use); original ckpt NC | Cameras + depth + point maps from 1 to hundreds of views in seconds; base of UrbanVGGT width method | 4 GB: 1B tight, few frames maybe (UNV) | V-S |
| 103 | MapAnything (Meta, arXiv 2509.13414) | https://github.com/facebookresearch/map-anything | licence UNV | **Metric** multi-view 3D, 12+ tasks; COLMAP + gsplat export; wraps VGGT/DUSt3R/MASt3R/Pi3-X | GPU | V-S |
| 104 | CUT3R (CVPR 2025 oral) | https://github.com/CUT3R/CUT3R | UNV | Streaming metric pointmaps from a walk video; can probe unseen views | GPU | V-S |
| 105 | Fast3R (CVPR 2025) | https://github.com/facebookresearch/fast3r | **FAIR NC Research License** | 1000+ images one pass | GPU large | V-S |
| 106 | DUSt3R / MASt3R (Naver) | https://github.com/naver/mast3r | **CC BY-NC-SA 4.0** | Pair matching + 3D; non-commercial | GPU | V-S |
| 107 | **AnySplat**: feed-forward 3DGS from unposed views (SIGGRAPH Asia 2025) | https://github.com/InternRobotics/AnySplat | **MIT**; HF Gradio demo | Few phone photos of a crossing -> Gaussian splat in one pass: "reconstruct the crossing in 3D" demo | HF Space / GPU (UNV on 4 GB) | V-S |
| 108 | **World Labs Marble + World API** (Marble GA 12 Nov 2025; World API 21 Jan 2026) | https://www.worldlabs.ai/blog/announcing-the-world-api ; https://docs.worldlabs.ai/api | paid API (model `marble-1.1`) | Image / multi-image / pano / video -> explorable 3D world, SPZ splats 100k/500k/full; "walk the route before you go" | API | V-S |
| 109 | Spark (Gaussian splats in Three.js, World Labs open source) | https://sparkjs.dev/ (named in https://www.worldlabs.ai/blog/bigger-better-worlds) | open source (licence UNV) | Render splats inside the santioni-style WebGL site | browser | V-S (mention) |
| 110 | NVIDIA **Lyra 2.0** (Apr 2026; GUI + training Jul 2026) | https://github.com/nv-tlabs/lyra ; https://huggingface.co/nvidia/Lyra-2.0 | code **Apache-2.0**; model 14B (Wan-14B based) | Single image -> camera-controlled walkthrough video -> 3DGS/mesh (~90 m scenes) | big GPU only | V-S |
| 111 | HunyuanWorld-Voyager (+ WorldMirror 1.1, WorldPlay 1.5, FlashWorld 5-10 s 3DGS) | https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager | **Tencent community licence** (check India/territory terms, UNV) | Image + camera path -> RGB-D video -> point cloud | big GPU | V-S |
| 112 | NVIDIA Cosmos 3 (Jun 2026) | https://arxiv.org/abs/2606.02800 ; https://blogs.nvidia.com/blog/open-world-models-physical-ai/ | **OpenMDW 1.1**; Nano 16B, Super 64B | Text/image -> video world sim: "this street in monsoon" what-if clips | API / big GPU | V-S |
| 113 | Genie 3 / Project Genie (DeepMind) | https://deepmind.google/models/genie | access via Project Genie (Labs), not an open API | Real-time explorable worlds from text; demo inspiration only | web app | V-S |
| 114 | Wan 2.x image-to-video (open weights) | not opened | Apache 2.0 (UNV) | Base model under Lyra 2.0; I2V walk clip | GPU >=8 GB (UNV) | UNV |

## 9. Geo-localisation and map matching

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 115 | GeoCLIP (NeurIPS 2023) | https://github.com/VicenteVivan/geo-clip | **MIT** | GPS guess for photos with stripped EXIF (coarse, km level) | 4 GB / CPU | V-S |
| 116 | PIGEON / PIGEOTTO (CVPR 2024) | https://lukashaas.github.io/PIGEON-CVPR24 | UNV | 40.4% within 25 km; coarse only | GPU | V-S |
| 117 | **MegaLoc** (CVPRW 2025) | https://github.com/gmberton/MegaLoc | **MIT**; torch.hub one-liner, 8448-d descriptor | Match a user photo to nearby Mapillary/GSV frames -> exact spot -> correct footpath segment; also dedups "several images of the same spot agree" | 4 GB yes | V-S |
| 118 | OrienterNet (CVPR 2023) | https://github.com/facebookresearch/OrienterNet | repo licence listed as ODbL (UNV for weights) | Sub-metre position + heading by matching photo BEV to **OpenStreetMap** raster; then left/right side of road -> which footway | 4 GB ok (UNV) | V-S |
| 119 | Scaling image geo-localisation to continent level (NeurIPS 2025) | https://proceedings.neurips.cc/paper_files/paper/2025/file/c2891461cb314d016da16efa06f7f1d5-Paper-Conference.pdf | code at scaling-geoloc.github.io (UNV) | 68% within 200 m over Western Europe with aerial cross-view; India not covered | GPU | V-S |
| 120 | Project Sidewalk segment logic (segment = OSM way + first/last GSV pano, >=75% coverage) | https://arxiv.org/html/2602.09216 | see row 1 | Simple, defensible detection -> segment rule to copy | CPU | V-F |

## 10. Accessible routing research

| # | item | URL | code / licence | what it gives SC-02 | runs on | grade |
|---|---|---|---|---|---|---|
| 121 | AccessMap (TCAT, UW) | https://tcat.cs.washington.edu/accessmap ; https://github.com/AccessMap | open source (UNV per repo) | Per-profile routing (cane, manual / powered wheelchair) with slope tolerance + kerb ramp need | CPU | V-S |
| 122 | OpenSidewalks Schema (2024) | https://sidewalks.washington.edu/2024/05/30/schema/ | open spec | Graph-first footway schema (edges/nodes, crossings, kerbs); our output format so others can reuse | CPU | V-S |
| 123 | OS-CONNECT statewide sidewalk dataset (UW News, Mar 2025) | https://www.washington.edu/news/2025/03/25/os-connect-accessmap-accessible-sidewalks/ | dataset | ML + human vetting at state scale; "no incline >5%, kerb ramps" filter example | n/a | V-S |
| 124 | **Accessibility for Whom?** perceptions across disability groups + personalised routing (CHI 2025; arXiv 2502.19888) | https://dl.acm.org/doi/10.1145/3706598.3713421 | open dataset (per paper) | Per-group passability of each barrier type -> cost weights per persona (wheelchair, cane, blind, pram); OSMnx prototype | CPU | V-S |
| 125 | OpenStreetMap suitability for wheelchair routing (AGILE GIScience Series 7, Jun 2026) | https://agile-giss.copernicus.org/articles/7/12/2026 | CC BY 4.0 | Which OSM tags matter (surface, incline, kerb, barrier, smoothness); gap check for Indian OSM | CPU | V-S |
| 126 | accessible-route-planner (GitHub) | https://github.com/yinli-systems/accessible-route-planner | licence UNV | Profiles (manual / power wheelchair, stroller), hazard scoring, and states that route confidence is bounded by OSM tag completeness | server | V-S |
| 127 | OSM Wheelchair routing wiki (tags incl. kerb heights, sidewalk:*:smoothness) | https://wiki.openstreetmap.org/wiki/Wheelchair_routing | wiki | Tag set to write our detections back as OSM-style attributes | n/a | V-S |
| 128 | FHWA-HRT-23-084 Sidewalk Mapping for Pedestrian Navigation workshop (Sep 2023) | https://highways.dot.gov/sites/fhwa.dot.gov/files/FHWA-HRT-23-084.pdf | public | Government view of the data gap; Q&A citation | n/a | V-S |
| 129 | Chandigarh severity weighting (0.2 / 0.6 / 1.0) as segment cost | https://arxiv.org/html/2602.09216 | see row 1 | Ready published cost weights for barrier severity | CPU | V-F |
| 130 | Uncertainty-aware / probabilistic accessible routing with missing sidewalk data | none found | none | **Gap**: no primary paper surfaced this session. Our own rule (unknown != safe, D2) + conformal intervals (row 25) is a fair novelty claim, but say "we did not find prior work" not "first" | CPU | gap logged |

---

## Coverage log (zero-result or thin areas)

| query area | result |
|---|---|
| CitySurfaces primary page | not returned by search this session |
| LLMDet | not returned |
| Borewell / open pit dataset | none found |
| Uncertainty-aware accessible routing paper | none found (queries: "probabilistic accessible routing incomplete sidewalk data", "risk-aware pedestrian routing barriers uncertainty") |
| Dark Zurich, Wan 2.x, SAM 2 | not opened this session (known from memory only) |
| Code for 2602.09216 (Chandigarh) | no code link on the arXiv HTML; the paper says the tool is the adapted Project Sidewalk |
| Code for UrbanVGGT, OmniPath, 2609.17882 | abs pages fetched; no code link on abs page (2609.17882 releases images + values) |

Counted rows (grep, not eyeballed): 130 numbered rows = 13 V-F + 110 V-S + 7 not verified (UNV rows 8, 53, 54, 85, 114; gap rows 95, 130).

## Red-team of this file (try to prove it wrong)

| claim | risk | grade |
|---|---|---|
| "YOLOE runs on 4 GB" | params (12-45M) from repo are V-F; the VRAM fit is my inference, not tested | UNVERIFIED |
| "SAM 3 likely OOM on 4 GB" | 848M params is V-F; OOM is a guess, could fit at fp16 low res | UNVERIFIED |
| RampNet AP 0.92 | real number but measured **with flip TTA** on US panos; does not transfer to Indian kerbs | VERIFIED, scope-limited |
| "2609.17882 gives the refusal recipe" | it shows CP coverage on Seoul; Indian photos not tested | VERIFIED source, EXAGGERATION risk if pitched as proven for India |
| DA3 licences per model | read from the repo model card table | VERIFIED (V-F) |
| Depth Anything V2 Small Apache, others NC | from repo README excerpt | VERIFIED (V-S) |
| VGGT commercial | only the VGGT-1B-Commercial checkpoint; original stays NC | VERIFIED (V-S) |
| Molmo2 Apache 2.0 | HF card excerpt says Apache 2.0 | VERIFIED (V-S) |
| MASt3R/DUSt3R/Fast3R non-commercial | LICENSE files in search excerpt | VERIFIED (V-S); fine for a hackathon demo, flag in Q&A |
| Hunyuan licence territory limits | I recall Tencent community licences exclude some regions; not checked for India | UNVERIFIED, check before use |
| "Our unknown-not-safe routing is novel" | absence of evidence from ~2 queries | UNVERIFIED, do not claim "first" |

## Top 10 for tonight (build-relevant, ranked)

1. **2602.09216 Chandigarh** (row 1): Indian label taxonomy (Curb Style, carts, drainage, electric box), gemini-2.5-flash guidance prompt inputs, segment rule, severity weights 0.2/0.6/1.0. Copy all four.
2. **Project Sidewalk API, CC0** (rows 2-3): Chandigarh labels as our seed / test set + AccessScore formula.
3. **YOLOE** (row 45, AGPL, 12M+): detector A, text + prompt-free, real-time on the GTX 1650 (to be smoke-tested).
4. **Florence-2 (MIT) or OWLv2** (rows 49-50): detector B for "two must agree"; SAM 3 (row 44) via Colab/API as the mask referee.
5. **Qwen3-VL 2B/4B, Apache, ollama** (row 41) as local VLM judge with JSON boxes; Gemini 2.5 Flash as the cloud one, same as the Chandigarh paper.
6. **Conformal prediction for VLM accessibility (2609.17882)** (row 25): calibrated intervals -> "needs a human look" and segment = unknown (D2).
7. **MoGe-2 vits/vitb (MIT) + GeoCalib** (rows 58, 63), cross-checked by **DA3METRIC-Large / DA2-Small metric (Apache)** (rows 56-57): kerb/step height + slope with two engines; UrbanVGGT (row 9) recipe for width.
8. **IDD-AW + RDD2022 India + DA-CLIP condition tag** (rows 68, 86, 79): show night/rain/fog numbers, not claims; tag each photo's condition.
9. **MegaLoc (MIT) + OrienterNet (OSM)** (rows 117-118): put a user photo on the right footway segment; also groups "several images of the same spot".
10. **AnySplat (MIT) for own-photo 3D crossing + World Labs Marble API for walk-through** (rows 107-108), rendered in-site with Spark (row 109); Lyra 2.0 / Cosmos 3 only as cited future work (too big for the box).
