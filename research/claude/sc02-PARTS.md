# SC-02 parts sweep, claude second engine (v1)

Built 2026-10-24 16:37 IST by `parts-raw/aggregate.py` from raw files in `research/claude/parts-raw/` (github/, hf/, arxiv/, web_items.json, harvest.log). Re-run the script to rebuild.

**Unique items kept: 712** (deduped by URL across all parts; an item appears once, under the first part that found it, with other parts listed in the `also` column).

| host | unique items kept |
|---|---|
| github | 420 |
| huggingface | 160 |
| arxiv | 99 |
| web | 22 |
| kaggle | 5 |
| gitee | 4 |
| mendeley | 1 |
| zenodo | 1 |

Caveats (read before trusting a row):
- `runs on` is a heuristic from repo language and keywords (yolo/lite/onnx => 4GB GPU/CPU, JS/TS => browser). Nothing here was executed on the GTX 1650. UNVERIFIED per row unless the row says otherwise.
- Stars, downloads, licence and last-push come straight from the API responses at harvest time (VERIFIED as API output, not checked against repo pages).
- Rows marked src `parallel` come from Parallel web_search excerpts; the facts in `what` are from those excerpts (UNVERIFIED beyond the excerpt).
- GitHub keyword search misses repos whose README is the only place the term appears and ranks by stars, so niche repos under ~5 stars are under-represented; the sort=updated pass partly fixes this.
- Gitee API sweep BLOCKED: gitee.com DNS failed (Errno -3) both inside and outside the sandbox at 16:22 IST. Gitee rows come from Parallel web_search only.
- Kaggle has no keyless search API; Kaggle rows come from Parallel web_search.

## 10 finds a plain search would likely miss (why each matters for SC-02)

1. [ProjectSidewalk/sidewalk-panorama-tools](https://github.com/ProjectSidewalk/sidewalk-panorama-tools): pulls GSV, Mapillary and Panoramax panoramas plus Google depth maps for every labelled point and crops one image per label. Ready-made data pipe for the Chandigarh labels.
2. [RampNet model on HF](https://huggingface.co/projectsidewalk/rampnet-model) + 214k-pano dataset: curb ramp heatmap detector (ICCV25 CV4A11y); a second detector to pair with an open-vocab one for agreement.
3. [Project Sidewalk API](https://projectsidewalk.org/api) lists India among 11 deployment countries and arXiv 2602.09216 describes the Chandigarh deployment; whether Chandigarh labels are downloadable from the public API is UNVERIFIED (check before relying on it).
4. [IRDID](https://github.com/ahs695/Indian-Road-Damage-Infrastructure-Dataset): Indian dataset with an OPEN MANHOLE class (200 imgs) plus dug surfaces and temporary barriers.
5. [Indian Footpath Damage Segmentation (Pune, Zenodo)](https://zenodo.org/records/15414238): 583 footpath images with pixel masks and severity, Sci Data 2025.
6. [e-Yantra IITB Indian roads seg](https://www.kaggle.com/datasets/eyantraiit/semantic-segmentation-datasets-of-indian-roads): 3227 knee-height images with a footpath class, close to a phone-in-hand viewpoint.
7. [ほこナビDP + 歩行空間ネットワークデータ spec](https://www.hokonavi.go.jp/opendata/): Japan's national footpath link schema (step height, width, gradient) with a web editor; a tested schema for barrier costs.
8. [arXiv 2609.17882](https://arxiv.org/abs/2609.17882): VLM sidewalk width/slope with conformal prediction intervals; gives the math for refuse-when-unsure.
9. [vlkryl/streetview_objectmapping](https://github.com/vlkryl/streetview_objectmapping) (MRF triangulation) and [Mapillary map features](https://www.mapillary.com/developer/api-documentation): turn detections from several images into one map point; this is the multi-image agreement step.
10. [soundscape-community/soundscape-web-client](https://github.com/soundscape-community/soundscape-web-client): Soundscape spatial-audio callouts in the browser, so the blind-user mode can live inside the demo site.
Also: [zaogao00/BlindRoadMonitor](https://github.com/zaogao00/BlindRoadMonitor) (obstacle-on-tactile-path IoU rule), [Gitee 灵瞳 占道经营 detector](https://gitee.com/xiao-wang-oh/zdjy) (street vendor encroachment), [Reclaim Chennai](https://reclaimchennai.city/) (GPS evidence camera with spoof flag), [Safetipin](https://safetipin.com/our-apps) (audit data incl Jaipur; Nite app = windscreen auto-capture), [cine1052rene/wheelway](https://github.com/cine1052rene/wheelway) (refuses to route on unmeasured widths).

Rows shown in part tables: 474; the rest of the 712 unique items are in the appendix.

## sidewalk segmentation (`sidewalk_seg`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [serey-roth/street-sidewalk-segmentation](https://github.com/serey-roth/street-sidewalk-segmentation) | github | ? | ? | 2025 | DeepLabV3+ seg + Qwen2.5-VL safety check dual pipeline | 4GB GPU (3B VLM) |  |
| 2 | [gunstillrattles/sidewalk-segmentation-unet](https://github.com/gunstillrattles/sidewalk-segmentation-unet) | github | ? | ? | 2026-10 | UNet-ResNet34 on segments/sidewalk-semantic, curb class | 4GB GPU |  |
| 3 | [VIDA-NYU/city-surfaces](https://github.com/VIDA-NYU/city-surfaces) | github | 56 stars | BSD-3-Clause | 2026-01-27 | CitySurfaces semantic segmentation of sidewalk surfaces | 4GB GPU? (unverified) |  |
| 4 | [charbel-a-hC/SidewalkDetection](https://github.com/charbel-a-hC/SidewalkDetection) | github | 18 stars | MIT | 2024-07-20 | Sidewalk detection for autonomous robot repository using RGB image semantic segmentation through deep neural c... | 4GB GPU? (unverified) |  |
| 5 | [navblind/Sidewalk-semantic-seg](https://github.com/navblind/Sidewalk-semantic-seg) | github | 12 stars | none | 2019-02-20 | Semantic segmentation for sidewalks. It has different models and options to train over. | 4GB GPU? (unverified) |  |
| 6 | [ddehueck/BostonStreetCaster](https://github.com/ddehueck/BostonStreetCaster) | github | 10 stars | none | 2019-05-12 | Sidewalk image segmentation and analysis project for the City of Boston department of Public Works | 4GB GPU? (unverified) |  |
| 7 | [uncle-TT/Obstacle-on-Blind-Sidewalks-Dataset-and-Model-by-Te...](https://github.com/uncle-TT/Obstacle-on-Blind-Sidewalks-Dataset-and-Model-by-Tensorflow-2.3) | github | 8 stars | Apache-2.0 | 2023-10-07 | This is an open source project on the deployment of deep learning to embedded microprocessors. The project est... | CPU (native) | obstacle |
| 8 | [mknz/dsr-road-roughness-prediction](https://github.com/mknz/dsr-road-roughness-prediction) | github | 6 stars | MIT | 2024-07-25 | Sidewalk semantic segmentation | 4GB GPU? (unverified) |  |
| 9 | [rlnav/sidewalk_planner](https://github.com/rlnav/sidewalk_planner) | github | 6 stars | none | 2019-12-17 | Mobile robot local planner based on sidewalk segmentation. | 4GB GPU / CPU |  |
| 10 | [YOLOv8-YOLOv11-Segmentation-Studio/footpath-segmentation261](https://github.com/YOLOv8-YOLOv11-Segmentation-Studio/footpath-segmentation261) | github | 4 stars | none | 2024-10-28 |  | 4GB GPU / CPU |  |
| 11 | [yunxdai/Intensity-based_Sidewalk_Segmentation](https://github.com/yunxdai/Intensity-based_Sidewalk_Segmentation) | github | 4 stars | none | 2021-07-02 |  | CPU (native) |  |
| 12 | [dh031200/Sidewalk_Obstacle_Detect](https://github.com/dh031200/Sidewalk_Obstacle_Detect) | github | 4 stars | GPL-3.0 | 2022-08-22 | Detect sidewalk obstacles with Object detection, Instance segmentation and Object tracking with Depth estimati... | 4GB GPU? (unverified) |  |
| 13 | [nurulgofran/Route-Planning-for-the-Visually-Impaired](https://github.com/nurulgofran/Route-Planning-for-the-Visually-Impaired) | github | 2 stars | MIT | 2026-08-02 | The Road Scene Understanding for the Visually Impaired initiative aims to develop a Sidewalk Environment Detec... | 4GB GPU? (unverified) |  |
| 14 | [Amnafiaz200/Real-time-road-scene-Segmentation-controller](https://github.com/Amnafiaz200/Real-time-road-scene-Segmentation-controller) | github | 1 stars | none | 2026-05-12 | Real-time semantic segmentation and vision-based heading controller for autonomous robotics using RGB video in... | 4GB GPU? (unverified) |  |
| 15 | [kauevestena/deep_pavements_sample_picker](https://github.com/kauevestena/deep_pavements_sample_picker) | github | 2 stars | Apache-2.0 | 2025-09-28 | Repository to use the capacities of recent semantic segmentation models with language models, and train a more... | 4GB GPU? (unverified) |  |

_+11 more kept for this part, listed in the appendix._

## curb ramp detection (`curb_ramp`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [ProjectSidewalk/sidewalk-tagger-ai](https://github.com/ProjectSidewalk/sidewalk-tagger-ai) | github | ? | ? | 2025 | 33-class sidewalk condition classifier + open dataset (ASSETS 24) | 4GB GPU |  |
| 2 | [projectsidewalk/sidewalk-tagger-ai-curbramp (HF)](https://huggingface.co/projectsidewalk/sidewalk-tagger-ai-curbramp) | huggingface | ? | apache-2.0 | 2026 | DINOv2 multi-label tagger for curb ramp crops | 4GB GPU |  |
| 3 | [ProjectSidewalk/RampNet + projectsidewalk/rampnet-model](https://github.com/ProjectSidewalk/RampNet) | github | 214k pano dataset | ? | 2025-2026 | curb ramp heatmap detector on equirect panos, ICCV25 CV4A11y; HF weights | 4GB GPU (2048x4096 input, tight) | curb_ramp |
| 4 | [Project Sidewalk ai-subsystems doc (sidewalk-auto-labeler, D...](https://github.com/ProjectSidewalk/SidewalkWebpage/blob/develop/docs/ai-subsystems.md) | github | doc | MIT (repo) | 2026-08 | map of all PS AI repos: auto-labeler, depth-aware crops via Depth Anything V2 | n/a |  |
| 5 | [rzou15/Object-detection-in-Point-Cloud-road-boundary](https://github.com/rzou15/Object-detection-in-Point-Cloud-road-boundary) | github | 134 stars | none | 2018-05-08 | Object detection in Point Cloud is popular in HD Map and sensor-based autonomous driving. There basically four... | CPU (native) |  |
| 6 | [ProjectSidewalk/SidewalkWebpage](https://github.com/ProjectSidewalk/SidewalkWebpage) | github | 110 stars | MIT | 2026-10-23 | Project Sidewalk web page | browser | osm_footway |
| 7 | [hey2525/Road-boundary-edge-curb-detection](https://github.com/hey2525/Road-boundary-edge-curb-detection) | github | 73 stars | none | 2019-01-05 |  | CPU (native) |  |
| 8 | [linyliny/curb_detection](https://github.com/linyliny/curb_detection) | github | 71 stars | none | 2021-09-23 | based on the paper A real-time curb detection and tracking method for UGVs by using a 3D-LIDAR sensor | CPU (native) |  |
| 9 | [crankler/awesome-lidar-curb-detection](https://github.com/crankler/awesome-lidar-curb-detection) | github | 48 stars | none | 2022-05-18 | A list of open source code about point cloud curb detection (processing) | ? |  |
| 10 | [speedzjy/lidar_curb_detection](https://github.com/speedzjy/lidar_curb_detection) | github | 39 stars | none | 2022-05-13 | 3D Lidar Curb Dectection implementation in ROS | CPU (native) |  |
| 11 | [bigbigpark/LiDAR-CURB-DETECTION](https://github.com/bigbigpark/LiDAR-CURB-DETECTION) | github | 27 stars | none | 2022-04-15 | Simple algorithm to detect the curb of road environment using 3D LiDAR | CPU (native) |  |
| 12 | [guoyangzhao/CurbNet](https://github.com/guoyangzhao/CurbNet) | github | 25 stars | none | 2026-04-02 | Curb Detection Framework Based on LiDAR Point Cloud Segmentation | 4GB GPU? (unverified) |  |
| 13 | [jmaye/curb-detection](https://github.com/jmaye/curb-detection) | github | 24 stars | none | 2013-04-23 | A C++ based library for curb detection | CPU (native) |  |
| 14 | [SohaibAl-emara/3D_Lidar_Curb_Detection](https://github.com/SohaibAl-emara/3D_Lidar_Curb_Detection) | github | 22 stars | none | 2019-12-25 |  | CPU (native) |  |
| 15 | [ProjectSidewalk/sidewalk-ai-api](https://github.com/ProjectSidewalk/sidewalk-ai-api) | github | 2 stars | Apache-2.0 | 2026-10-24 | This serves as an API implementation of the Project Sidewalk AI models for tagging and validating labels. | 4GB GPU? (unverified) |  |

_+9 more kept for this part, listed in the appendix._

## stairs/steps detection (`stairs`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [aperezyus/stairs_detection](https://github.com/aperezyus/stairs_detection) | github | 47 stars | GPL-3.0 | 2024-02-08 | Detection and modelling of staircases using a wearable depth sensor | CPU (native) |  |
| 2 | [Prassi07/staircase_autonomy](https://github.com/Prassi07/staircase_autonomy) | github | 27 stars | BSD-3-Clause | 2025-06-19 | A complete ROS 2 package for real-time staircase perception using 3D point cloud data. Features stable detecti... | CPU (native) |  |
| 3 | [bossenti/Real-Time-Detection-of-Stairs](https://github.com/bossenti/Real-Time-Detection-of-Stairs) | github | 14 stars | none | 2025-11-05 | Groupwork with 5 other students in an university course. Shows different approaches to detect stairs in real t... | 4GB GPU? (unverified) |  |
| 4 | [mdequanter/BlindNavTech](https://github.com/mdequanter/BlindNavTech) | github | 10 stars | Apache-2.0 | 2025-06-20 | Code and research for a master's thesis on advanced obstacle detection for the visually impaired. Uses 3D LiDA... | 4GB GPU? (unverified) | obstacle |
| 5 | [KangneoungLee/staircase_detection](https://github.com/KangneoungLee/staircase_detection) | github | 6 stars | MIT | 2023-11-09 |  | CPU (native) |  |
| 6 | [saavn03/Staircase-detection](https://github.com/saavn03/Staircase-detection) | github | 6 stars | none | 2021-07-31 | Staircase detection for visually impaired person using open-CV python | 4GB GPU? (unverified) |  |
| 7 | [szturobotics/Stair-detection-and-modelling-project](https://github.com/szturobotics/Stair-detection-and-modelling-project) | github | 4 stars | GPL-3.0 | 2023-09-07 | @An Onboard Framework for Stairscase Modelling Based on Point Clouds for Robots’ Stairs-Climbing | ? |  |
| 8 | [dhruv47/Detection-of-Staircase-for-visually-impaired](https://github.com/dhruv47/Detection-of-Staircase-for-visually-impaired) | github | 3 stars | none | 2022-02-03 |  | 4GB GPU? (unverified) |  |
| 9 | [marcoacc90/cnn-staircase-mobilenet](https://github.com/marcoacc90/cnn-staircase-mobilenet) | github | 2 stars | none | 2020-11-06 | MobileNet for staircase detection | 4GB GPU / CPU |  |
| 10 | [juanpbotero98/Staircase-Detection](https://github.com/juanpbotero98/Staircase-Detection) | github | 2 stars | none | 2021-06-02 |  | 4GB GPU? (unverified) |  |
| 11 | [c-Ath-Y/Barrier-Free-Scout-An-Environment-Detection-App-Powe...](https://github.com/c-Ath-Y/Barrier-Free-Scout-An-Environment-Detection-App-Powered-by-Unitree-Go2) | github | 1 stars | none | 2025-11-26 | Powered by the Unitree Go2 robot, this app automates accessibility inspections. Using advanced sensors, it ide... | browser |  |
| 12 | [AkshayScrKiddie/Facade-object-detection-using-YoLoV8m](https://github.com/AkshayScrKiddie/Facade-object-detection-using-YoLoV8m) | github | 1 stars | none | 2025-06-11 | Classification of façade objects such as windows, stairs, and doors within the images of buildings in street v... | 4GB GPU / CPU |  |
| 13 | [Dataclusterlabspvtltd/Stairs_Image_Dataset_Parts_of_House_In...](https://huggingface.co/datasets/Dataclusterlabspvtltd/Stairs_Image_Dataset_Parts_of_House_Indoor) | huggingface | 94 dl, 0 likes | other | 2026-07-14 | HF dataset: Stairs Image Dataset , Parts of House Indoor (Sample) ⚠️ This is a fr... | data |  |
| 14 | [mateoguaman/iphone_stairs_ramps](https://huggingface.co/datasets/mateoguaman/iphone_stairs_ramps) | huggingface | 59 dl, 0 likes | ? | 2025-04-15 | HF dataset: iphone_stairs_ramps Description Processed entire iphone_stairs_ramps w... | data |  |
| 15 | [mihir98/finetuned-stairs](https://huggingface.co/mihir98/finetuned-stairs) | huggingface | 14 dl, 0 likes | ? | 2025-04-20 | HF model: text-generation | 4GB GPU? (unverified) |  |

_+8 more kept for this part, listed in the appendix._

## pothole detection (`pothole`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Pothole Dataset Indian / Indian Road Dataset](https://www.kaggle.com/datasets/harshlokhande7/pothole-dataset-indian-indian-road-dataset) | kaggle | 8 downloads | ? | 2026-09 | Indian pothole/crack images for YOLO | data |  |
| 2 | [lukekratz/raspberry-pi-5-hailo-8-pothole-detection-system](https://github.com/lukekratz/raspberry-pi-5-hailo-8-pothole-detection-system) | github | 144 stars | MIT | 2025-05-22 | This is the official repository for the automatic pothole detection, classification and sizing system | 4GB GPU? (unverified) |  |
| 3 | [jhasuman/potholes-detection](https://github.com/jhasuman/potholes-detection) | github | 94 stars | none | 2023-03-24 | This is a deep learning model for detecting the potholes on roads. The model is using YOLO-v2. | 4GB GPU / CPU |  |
| 4 | [Cyash/Pothole_Detection](https://github.com/Cyash/Pothole_Detection) | github | 87 stars | NOASSERTION | 2024-05-15 | Pothole Detection using Masked-RCNN | 4GB GPU? (unverified) |  |
| 5 | [anantSinghCross/pothole-detection-system-using-convolution-n...](https://github.com/anantSinghCross/pothole-detection-system-using-convolution-neural-networks) | github | 85 stars | MIT | 2020-09-23 | Real-time detection of potholes on roads using video (via Webcam) processed through a CNN model. | 4GB GPU? (unverified) |  |
| 6 | [thiagortk/Road-surface-detection-and-differentiation-conside...](https://github.com/thiagortk/Road-surface-detection-and-differentiation-considering-surface-damages) | github | 57 stars | GPL-3.0 | 2021-01-28 | Semantic Segmentation in road surfaces, considering different pattern like asphalt, unpaved, potholes, etc. | 4GB GPU? (unverified) | road_damage |
| 7 | [FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage_Assess...](https://github.com/FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage_Assessment) | github | 57 stars | MIT | 2024-01-07 | Automated pothole detection and road damage assessment using YOLOv8-seg for real-time analysis. | 4GB GPU / CPU | road_damage |
| 8 | [noorkhokhar99/Pothole-Detection-Pothole-Detection-using-pyth...](https://github.com/noorkhokhar99/Pothole-Detection-Pothole-Detection-using-python-and-deep-learning) | github | 49 stars | none | 2024-08-11 | Pothole Detection // Pothole Detection using python and deep learning | 4GB GPU / CPU |  |
| 9 | [shubhank-saxena/Pothole-Detection](https://github.com/shubhank-saxena/Pothole-Detection) | github | 47 stars | none | 2019-07-01 | Pothole detection via Mask Rcnn | 4GB GPU? (unverified) |  |
| 10 | [CityofEdmonton/AI-Pothole-Detection-Using-YOLO](https://github.com/CityofEdmonton/AI-Pothole-Detection-Using-YOLO) | github | 42 stars | none | 2019-08-21 | YOLO: Real-Time Object Detection | 4GB GPU / CPU |  |
| 11 | [PeterHdd/pothole-detection-yolo](https://github.com/PeterHdd/pothole-detection-yolo) | github | 41 stars | Apache-2.0 | 2025-12-16 | YOLO-based pothole detection model trained with custom dataset deployed on Nebius Cloud, the repository includ... | browser |  |
| 12 | [aaryasaraf0907-lgtm/ai-ml-based-pothole-detection](https://github.com/aaryasaraf0907-lgtm/ai-ml-based-pothole-detection) | github | 1 stars | none | 2026-10-22 | AI/ML-powered pothole detection using YOLO-based computer vision, with severity classification, GPS-tagged rep... | 4GB GPU / CPU |  |
| 13 | [aditimaurya20/Pothole-Detection-System](https://github.com/aditimaurya20/Pothole-Detection-System) | github | 1 stars | none | 2026-10-20 | A Django-based pothole detection system using YOLO and OpenCV for real-time detection from images, videos, and... | 4GB GPU / CPU |  |
| 14 | [aravindreddym-034/AI-Based-Road-Pothole-Detection-and-Locali...](https://github.com/aravindreddym-034/AI-Based-Road-Pothole-Detection-and-Localization-Using-YOLOv8) | github | 4 stars | MIT | 2026-10-19 | 🚧 AI-based road pothole detection and localization using YOLOv8 deep learning and computer vision. | 4GB GPU / CPU |  |
| 15 | [Ryukijano/Pothole-detection-Yolov8](https://huggingface.co/datasets/Ryukijano/Pothole-detection-Yolov8) | huggingface | 2253 dl, 8 likes | openrail | 2023-06-01 | HF dataset: | data |  |

_+10 more kept for this part, listed in the appendix._

## road damage detection (RDD India) (`road_damage`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [RDD2022 India Pothole D40](https://www.kaggle.com/datasets/vidishbijalwan/rdd2022-india-pothole-d40) | kaggle | 1530 imgs | RDD2022 terms | 2026-05 | India-only pothole subset of RDD2022 (Delhi, Gurugram), VOC boxes | data |  |
| 2 | [N-RDD2024](https://data.mendeley.com/datasets/27c8pwsd6v/4) | mendeley | 10 classes | CC BY 4.0 (Mendeley default) | 2024-01 | RDD2022 relabelled with manhole covers (D70), crossing blur (D50) | data |  |
| 3 | [Saber0722 Road-Anomaly-Detection](https://github.com/Saber0722/Road-Anomaly-Detection) | github | ? | ? | ? | YOLO training on RDD India-only splits | 4GB GPU |  |
| 4 | [fyangneil/pavement-crack-detection](https://github.com/fyangneil/pavement-crack-detection) | github | 429 stars | none | 2025-02-22 |  | CPU (native) |  |
| 5 | [USC-InfoLab/rddc2020](https://github.com/USC-InfoLab/rddc2020) | github | 292 stars | GPL-3.0 | 2022-10-15 | road damage detection challenge 2020 | 4GB GPU? (unverified) |  |
| 6 | [shomnathsomu/crack-detection-opencv](https://github.com/shomnathsomu/crack-detection-opencv) | github | 162 stars | none | 2024-08-30 | Crack Detection On Highway Or Pavement Using OpenCV | 4GB GPU? (unverified) |  |
| 7 | [oracl4/RoadDamageDetection](https://github.com/oracl4/RoadDamageDetection) | github | 116 stars | none | 2026-05-05 | Road damage detection application, using YOLOv8 deep learning model trained on Crowdsensing-based Road Damage ... | 4GB GPU / CPU |  |
| 8 | [mahdi65/roadDamageDetection2020](https://github.com/mahdi65/roadDamageDetection2020) | github | 95 stars | Apache-2.0 | 2022-03-26 | repository contain codes for IEEE BigData Cup Challange 2020 | 4GB GPU? (unverified) |  |
| 9 | [juhuyan/CrackDataset_DL_HY](https://github.com/juhuyan/CrackDataset_DL_HY) | github | 64 stars | none | 2022-03-30 | Pavement surface crack datasets for DL based crack detection | ? |  |
| 10 | [TTMRonald/AerialCrackDetection](https://github.com/TTMRonald/AerialCrackDetection) | github | 45 stars | none | 2017-08-22 | Use Keras to detect the pavement cracks in aerial images. | 4GB GPU? (unverified) |  |
| 11 | [zhaohmng-outlook-com/21-](https://github.com/zhaohmng-outlook-com/21-) | github | 43 stars | none | 2019-08-23 | “21世纪新政宣言”和“三朝罪恶元凶王沪宁” ----推崇一篇见解温和奇特不左不右极罕见难得解困可行很有现实意义的文章《21世纪新政宣言》，和介绍一篇见解也独特但观点很强硬的《三朝罪恶元凶王沪宁》供比较和参考： 21世纪... | ? |  |
| 12 | [Mathweuzz/rdd2022-cpu-baseline](https://github.com/Mathweuzz/rdd2022-cpu-baseline) | github | 1 stars | MIT | 2026-10-23 | Reproducible CPU-only road damage detection on RDD2022 with domain-aware COCO evaluation and an IEEE paper | 4GB GPU / CPU |  |
| 13 | [dishantpatil-dev/AI-Road-Damage-Hazard-Detection-using-Compu...](https://github.com/dishantpatil-dev/AI-Road-Damage-Hazard-Detection-using-Computer-Vision-YOLO-Gemini-Flask-and-GPS) | github | 1 stars | MIT | 2026-10-22 | AI-powered road encroachment detection system that uses computer vision to identify unauthorized roadside obst... | 4GB GPU / CPU | encroachment |
| 14 | [VasuML07/RoadXAI](https://github.com/VasuML07/RoadXAI) | github | 1 stars | none | 2026-10-22 | An Explainable Deep Learning Framework for Automated Road Surface Damage Detection and Severity Assessment | 4GB GPU? (unverified) |  |
| 15 | [dronefreak/RDD2022](https://huggingface.co/datasets/dronefreak/RDD2022) | huggingface | 48712 dl, 3 likes | cc-by-sa-4.0 | 2026-10-01 | HF dataset: RDD2022: Multi-National Road Damage Detection Dataset (4-Class YOLO Ex... | data |  |

_+10 more kept for this part, listed in the appendix._

## open manhole/drain detection (`manhole`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [IRDID Indian Road Damage & Infrastructure Dataset](https://github.com/ahs695/Indian-Road-Damage-Infrastructure-Dataset) | github | 1200 imgs | ? | ? | 6 classes incl potholes, cracks, OPEN MANHOLES (200 each), dug surfaces, barriers | data |  |
| 2 | [Road Damage Dataset: Potholes, Cracks and Manholes](https://www.kaggle.com/datasets/lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes) | kaggle | 2000+ imgs, 37 upvotes | ? | 2025 | YOLO labels incl manholes | data |  |
| 3 | [Xuding0829/Well 井盖隐患识别](https://github.com/Xuding0829/Well) | github | ? | GPL-3.0 | ? | YOLOv5 manhole cover hazard (broken/missing/open) detection | 4GB GPU |  |
| 4 | [coding-parrot/pothole-reporter](https://github.com/coding-parrot/pothole-reporter) | github | 158 stars | MIT | 2026-10-14 | Pothole Reporter is an independent Android app for documenting potholes, garbage and open manholes, with backg... | browser |  |
| 5 | [xi029/YOLO-Vue-Flask](https://github.com/xi029/YOLO-Vue-Flask) | github | 21 stars | GPL-3.0 | 2025-03-15 | 基于Flask开发后端、Vue开发前端框架，MySQL作为存储数据库，在Web端部署YOLOv5井盖缺陷检测模型 | 4GB GPU / CPU |  |
| 6 | [DhanushRavichandran/Manhole-monitoring-And-Fault-Detection](https://github.com/DhanushRavichandran/Manhole-monitoring-And-Fault-Detection) | github | 16 stars | none | 2024-11-28 |  | ? |  |
| 7 | [Benny0323/Yolov5-based-well-detection](https://github.com/Benny0323/Yolov5-based-well-detection) | github | 5 stars | AGPL-3.0 | 2025-02-11 | The hidden danger of manhole cover detection based on KDWC-YOLOv5(Knowledge Distillation Well Cover-YOLOv5) | 4GB GPU / CPU |  |
| 8 | [XTCi/manhole-cover](https://github.com/XTCi/manhole-cover) | github | 4 stars | none | 2025-04-29 | 井盖检测系统 | browser |  |
| 9 | [ZhWangg/ManholeCoverDetection](https://github.com/ZhWangg/ManholeCoverDetection) | github | 4 stars | none | 2023-07-12 | MyCourseDesign | 4GB GPU? (unverified) |  |
| 10 | [swiss-territorial-data-lab/proj-streetview](https://github.com/swiss-territorial-data-lab/proj-streetview) | github | 4 stars | MIT | 2025-11-17 | Detection of manholes on street view images and reprojection to an EPSG system | 4GB GPU? (unverified) |  |
| 11 | [bhamap/Custom-ObjectDetection-Manhole-Detection](https://github.com/bhamap/Custom-ObjectDetection-Manhole-Detection) | github | 3 stars | none | 2020-09-04 | Customized Object Detection Model implemented using Transfer Learning Concept. Detects Closed and Open Manhole... | 4GB GPU? (unverified) |  |
| 12 | [XavierYu404/Data-Augmented-Deep-Learning-Model-for-Abnormal-...](https://github.com/XavierYu404/Data-Augmented-Deep-Learning-Model-for-Abnormal-Road-Manhole-Cover-Detection) | github | 3 stars | none | 2023-02-16 |  | 4GB GPU? (unverified) |  |
| 13 | [tanzirulnayan/Monsoon-Challenge](https://github.com/tanzirulnayan/Monsoon-Challenge) | github | 3 stars | MPL-2.0 | 2019-03-26 | Monsoon Challenge is an adventure game where a person prevents himself from falling into open manholes. The ma... | CPU (native) |  |
| 14 | [reddy895/PotHole-Detector](https://github.com/reddy895/PotHole-Detector) | github | 2 stars | GPL-3.0 | 2026-10-17 | An AI-powered road safety system that uses a camera to detect potholes, damaged roads, open manholes, debris, ... | 4GB GPU? (unverified) |  |
| 15 | [ChickenGor/safedrive](https://github.com/ChickenGor/safedrive) | github | 1 stars | none | 2026-09-06 | Vision-based ADAS prototype using YOLO for pothole, crack, manhole, vehicle and person detection, with explain... | browser |  |

_+12 more kept for this part, listed in the appendix._

## obstacle on footpath (`obstacle`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [berkott/NavigationAssistant](https://github.com/berkott/NavigationAssistant) | github | 5 stars | MIT | 2019 | sidewalk, crosswalk, traffic light, obstacle live detection | CPU |  |
| 2 | [nandiyang/robot-navigable-city](https://github.com/nandiyang/robot-navigable-city) | github | ? | ? | 2026 | video frames + GPS sync + YOLOv8 barrier detection geotagged to interactive map | 4GB GPU |  |
| 3 | [caozx1110/ETDCar](https://github.com/caozx1110/ETDCar) | github | 27 stars | Apache-2.0 | 2022-04-07 | "基于路径规划的智能盲人导航车"-小车导航及避障 | 4GB GPU? (unverified) |  |
| 4 | [godragun/esp32_telegram_cam_loaction_blindstick](https://github.com/godragun/esp32_telegram_cam_loaction_blindstick) | github | 13 stars | none | 2025-12-22 | 🦯 Smart blind stick with ESP32-CAM, GPS, Telegram bot alerts, and obstacle detection for visually impaired nav... | CPU (native) |  |
| 5 | [Yashk1434/smart_headset_for_blind_people](https://github.com/Yashk1434/smart_headset_for_blind_people) | github | 11 stars | none | 2025-06-04 | A compact, wearable assistive device enhancing mobility, safety, and independence for visually impaired indivi... | CPU (native) |  |
| 6 | [NDharshan/iNeuron-Blind-Navigation](https://github.com/NDharshan/iNeuron-Blind-Navigation) | github | 9 stars | none | 2023-01-31 | This project attempts to create a system which would bring in added ease to the visually impaired, through our... | 4GB GPU? (unverified) |  |
| 7 | [himanshugupta2004/Object-Detection-Model](https://github.com/himanshugupta2004/Object-Detection-Model) | github | 9 stars | none | 2025-04-12 | Smart Blind Assistance System is an AI-powered wearable tool that uses a webcam and laptop to detect obstacles... | 4GB GPU / CPU |  |
| 8 | [yshshrm/RaahDarshani](https://github.com/yshshrm/RaahDarshani) | github | 8 stars | none | 2018-03-06 | IoT based application to make life easier for the visually impaired. | ? |  |
| 9 | [prajwal714/Intelligent-Stick-for-Visually-Impaired](https://github.com/prajwal714/Intelligent-Stick-for-Visually-Impaired) | github | 7 stars | MIT | 2020-09-06 | Hardware project which uses Pi camera and mobileNet SSD to classify obstacles and measure distance using ultra... | 4GB GPU / CPU |  |
| 10 | [souravs17031999/Object-Detection-MobileNet-cv](https://github.com/souravs17031999/Object-Detection-MobileNet-cv) | github | 7 stars | none | 2022-06-22 | Real time Object detection: object detection system to enhance pedestrian safety and assist visually impaired ... | browser |  |
| 11 | [Neural-Nexus-IoTrix-2-0/intellicane](https://github.com/Neural-Nexus-IoTrix-2-0/intellicane) | github | 2 stars | none | 2026-10-20 | ESP32-based smart cane for the visually impaired , obstacle and drop-off detection with haptic feedback, AI v.... | CPU (native) |  |
| 12 | [sindhujasankaramoorthy/BlindObstacleDetection](https://github.com/sindhujasankaramoorthy/BlindObstacleDetection) | github | 2 stars | none | 2026-10-19 | An assistive system designed to detect obstacles and provide alerts to help visually impaired individuals navi... | app/CPU |  |
| 13 | [bharath2957s/Digital-Vision-Companion](https://github.com/bharath2957s/Digital-Vision-Companion) | github | 2 stars | MIT | 2026-09-13 | 👁️ AI-powered assistive tool for the visually impaired. Features real-time obstacle detection, distance estima... | browser |  |
| 14 | [Abtinzandi/Obstacle-Detection-Dataset-YOLO](https://huggingface.co/datasets/Abtinzandi/Obstacle-Detection-Dataset-YOLO) | huggingface | 3835 dl, 19 likes | mit | 2026-10-05 | HF dataset: ROD-Dataset: Real-Time Obstacle Detection for Smartphone-Based Assisti... | data |  |
| 15 | [eziodad/Obstacle-Detection-Dataset-YOLO](https://huggingface.co/datasets/eziodad/Obstacle-Detection-Dataset-YOLO) | huggingface | 1062 dl, 0 likes | mit | 2026-09-01 | HF dataset: ROD-Dataset: Real-Time Obstacle Detection for Smartphone-Based Assisti... | data |  |

_+9 more kept for this part, listed in the appendix._

## parked vehicle on sidewalk (`parked_vehicle`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Public Eye (Bengaluru Traffic Police + Janaagraha)](https://dev.janaagraha.org/works/civic-participation) | web | city | closed | live | citizens report parking violations with photos | app |  |
| 2 | [wangyinzhi1989/CVIntegratedPlatform](https://github.com/wangyinzhi1989/CVIntegratedPlatform) | github | 166 stars | none | 2020-09-28 | 一款基于深度学习，提供数据标注、模型训练、模型部署、基于已有模型自动标注等功能的计算机视觉一体化平台。 操作简单，无需深度学习理论即可实现AI落地。处理分类、目标检测、目标跟踪等计算机视觉任务。 应用场景：交通执法（车辆... | 4GB GPU? (unverified) |  |
| 3 | [abhishekapk/SMART-PARKING-SYSTEM](https://github.com/abhishekapk/SMART-PARKING-SYSTEM) | github | 55 stars | MIT | 2023-10-09 | Computerized systems being an integral part of the current era, an automated parking system is one of its most... | ? |  |
| 4 | [qunshansj/YOLO_Illegal_Parking_Detection](https://github.com/qunshansj/YOLO_Illegal_Parking_Detection) | github | 36 stars | none | 2023-11-05 | 基于YOLO的机动车乱停乱放检测系统(源码＆部署教程) | 4GB GPU / CPU |  |
| 5 | [xxxxZhou/Road-occupancy-operation-and-vehicle-illegal-parkin...](https://github.com/xxxxZhou/Road-occupancy-operation-and-vehicle-illegal-parking-detection) | github | 13 stars | none | 2023-01-02 | Use yolov5 to realize the road occupation operation and vehicle parking violation detection in urban streets, ... | 4GB GPU / CPU |  |
| 6 | [prakharninja0927/illegal-Parking-Detection](https://github.com/prakharninja0927/illegal-Parking-Detection) | github | 12 stars | none | 2024-03-20 |  | 4GB GPU? (unverified) |  |
| 7 | [revaldianggara/illegal-parking-detection](https://github.com/revaldianggara/illegal-parking-detection) | github | 6 stars | none | 2023-12-17 | Deteksi ilegal parkir menggunakan raspberry, model yolov3 darknet53 | 4GB GPU / CPU |  |
| 8 | [kimmyoungji/2024_inisw4_Illegal-parking-reporting-guideline-...](https://github.com/kimmyoungji/2024_inisw4_Illegal-parking-reporting-guideline-service_app) | github | 5 stars | none | 2024-06-18 | 2024 고려대 지능정보 아카데미 04기 04조 프로젝트 : 안전신문고 불법주정차 신고 가이드라인 서비스 | app/CPU |  |
| 9 | [wangdefa12138/YOLOv9-Parking-Violation-Detection](https://github.com/wangdefa12138/YOLOv9-Parking-Violation-Detection) | github | 5 stars | GPL-3.0 | 2026-04-29 | 基于YOLOv9的车辆违停、压线、违规变道检测系统，带GUI界面 | 4GB GPU / CPU |  |
| 10 | [sgandhi04/K9](https://github.com/sgandhi04/K9) | github | 5 stars | none | 2021-10-09 | Parks, downtowns, malls, and stores are places that we visit frequently in our day to day lives. These public ... | CPU (native) |  |
| 11 | [share2code99/vehicle_parking_violation_detection_yolov10n_ti...](https://github.com/share2code99/vehicle_parking_violation_detection_yolov10n_timm) | github | 4 stars | none | 2025-11-05 | 城市道路车辆违停识别与车牌检测_YOLOv10n+Timm实现_1 | 4GB GPU / CPU |  |
| 12 | [yufish87/LiDAR-based_Illegal_Parking_Detection_AMR](https://github.com/yufish87/LiDAR-based_Illegal_Parking_Detection_AMR) | github | 1 stars | NOASSERTION | 2026-09-24 | NTUST GDEP Undergraduate Project | CPU (native) |  |
| 13 | [Leonard0429/illegal-parking-detection](https://github.com/Leonard0429/illegal-parking-detection) | github | 1 stars | none | 2026-08-09 | AI-assisted illegal parking detection using YOLO26, OpenCV, and Streamlit | 4GB GPU / CPU |  |
| 14 | [Shyamsundar2203/parkwatch](https://github.com/Shyamsundar2203/parkwatch) | github | 1 stars | NOASSERTION | 2026-07-27 | illegal Parking or vehicle detection system | 4GB GPU? (unverified) |  |
| 15 | [shangzx/Hazardous-Materials-Vehicle-Illegal-Parking-Behavior...](https://huggingface.co/datasets/shangzx/Hazardous-Materials-Vehicle-Illegal-Parking-Behavior-Detection-Dataset) | huggingface | 49 dl, 0 likes | cc-by-nc-sa-4.0 | 2026-03-05 | HF dataset: Hazardous Materials Vehicle Illegal Parking Behavior Detection Dataset... | data |  |

_+7 more kept for this part, listed in the appendix._

## street vendor/encroachment detection (`encroachment`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [灵瞳 YOLOv8-DeepSeek street governance (占道经营)](https://gitee.com/xiao-wang-oh/zdjy) | gitee | ? | ? | ? | YOLOv8n street-vendor encroachment detection, 93% mAP50 claimed, LLM report layer | 4GB GPU |  |
| 2 | [isaychris/litter-detection-tensorflow](https://github.com/isaychris/litter-detection-tensorflow) | github | 21 stars | none | 2018-05-31 | Object Detection algorithm trained to identify litter from Google Streets :: [CIS490 Project Management Final ... | 4GB GPU? (unverified) |  |
| 3 | [samadon1/accraflood](https://github.com/samadon1/accraflood) | github | 7 stars | MIT | 2026-06-30 | Terrain-derived drainage and building-encroachment detection for Accra, Ghana | 4GB GPU? (unverified) |  |
| 4 | [bipinthecoder/Street-Litter-Detection](https://github.com/bipinthecoder/Street-Litter-Detection) | github | 5 stars | NOASSERTION | 2023-11-04 | This Project focuses on building an Object detection model that detects Litter from two geographical locations... | 4GB GPU / CPU |  |
| 5 | [qunshansj/YOLO_Street_Vendor_Detection](https://github.com/qunshansj/YOLO_Street_Vendor_Detection) | github | 4 stars | none | 2023-11-05 | 基于YOLO的游商游贩检测系统(源码＆部署教程＆数据集) | 4GB GPU / CPU |  |
| 6 | [GouranshAgarwal/UrbanEncroachmentDetection](https://github.com/GouranshAgarwal/UrbanEncroachmentDetection) | github | 2 stars | none | 2026-05-05 |  | 4GB GPU? (unverified) |  |
| 7 | [osamabinIaggin/project-vision](https://github.com/osamabinIaggin/project-vision) | github | 2 stars | NOASSERTION | 2026-08-10 | Deep-learning + GIS pipeline detecting flood-driving drainage encroachment from 5 cm aerial imagery , U-Net s.... | 4GB GPU? (unverified) |  |
| 8 | [0xMoni/LitterLens](https://github.com/0xMoni/LitterLens) | github | 2 stars | none | 2026-04-08 | From space to street , AI-powered garbage dump detection for Bengaluru 🛰️🗑️ | browser |  |
| 9 | [QQ767172261/How-to-use-the-deep-learning-framework-target-de...](https://github.com/QQ767172261/How-to-use-the-deep-learning-framework-target-detection-algorithm-yolov8-to-train-roadshare-operator) | github | 1 stars | none | 2026-01-03 | 如何使用深度学习框架目标检测算法yolov8训练占道经营摆摊识别数据集 识别检测违法占道经营摆摊检测 建立基于深度学习的占道摆摊行为检测 | 4GB GPU / CPU |  |
| 10 | [dishantpatil-dev/ai_road_encroachment_detection](https://github.com/dishantpatil-dev/ai_road_encroachment_detection) | github | 1 stars | MIT | 2026-10-22 |  | 4GB GPU? (unverified) |  |
| 11 | [bskr-cjee/mtech-project-nitr](https://github.com/bskr-cjee/mtech-project-nitr) | github | 1 stars | none | 2025-04-16 | Detection of Load Encroachment in Distance Relays using Synchrophasor Measurements | 4GB GPU? (unverified) |  |
| 12 | [VishnuKumar2311019/LandEnchroachmentDetection](https://github.com/VishnuKumar2311019/LandEnchroachmentDetection) | github | 1 stars | none | 2026-10-02 | AI-driven geospatial system for detecting and monitoring government land encroachment using computer vision, s... | browser |  |
| 13 | [Jie04Wen/RiverChangeFormer](https://github.com/Jie04Wen/RiverChangeFormer) | github | 1 stars | MIT | 2026-09-18 | UAV-based river encroachment change detection built on ChangeFormerV6, featuring grouped dataset splitting, Mi... | 4GB GPU? (unverified) |  |
| 14 | [DriveFuzz: Discovering Autonomous Driving Bugs through Drivi...](https://arxiv.org/abs/2211.01829v1) | arxiv | paper | arXiv | 2022-10-25 | Autonomous driving has become real; semi-autonomous driving vehicles in an affordable price range ar... | n/a (paper) |  |

## tactile paving detection (`tactile`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [GRFB-UNet tactile paving segmentation](https://gitee.com/electric-kettle-star/tactile-paving-identification) | gitee | ? | none | ? | 盲道 segmentation system, GRFB-UNet | 4GB GPU |  |
| 2 | [YellowBlock231 盲道损坏检测](https://gitee.com/Vision-Studios/YellowBlock231) | gitee | 0 stars | none | ? | tactile paving damage segmentation, YOLO11 variant + dataset | 4GB GPU |  |
| 3 | [zaogao00/BlindRoadMonitor](https://github.com/zaogao00/BlindRoadMonitor) | github | ? | ? | 2026 | YOLOv8n 26 classes, obstacle-on-tactile-path IoU rule, TTS alerts; mAP50 0.776 | 4GB GPU |  |
| 4 | [JezZh/tactile-path-segmentation](https://github.com/JezZh/tactile-path-segmentation) | github | ? | ? | 2026 | 360 pano tactile paving seg on Jetson Nano, P-Strip temporal trick | edge |  |
| 5 | [bestxiangest/Intelligent-Guide-Cane](https://github.com/bestxiangest/Intelligent-Guide-Cane) | github | 38 stars | none | 2026-04-30 | 星辰引路者是一款基于ESP32-S3微控制器的多模态智能导盲系统，旨在帮助视障人士更安全、便捷地出行。该系统集成了多种传感器和人工智能技术，能够实时检测周围环境，识别障碍物、盲道和红绿灯，并通过语音交互提供导航和天气查询... | CPU (native) |  |
| 6 | [Chon2020/GRFB-Unet](https://github.com/Chon2020/GRFB-Unet) | github | 34 stars | GPL-3.0 | 2023-11-08 | GRFB-UNet: A new multi-scale attention network with group receptive field block for tactile paving segmentatio... | 4GB GPU? (unverified) |  |
| 7 | [surferjin/-](https://github.com/surferjin/-) | github | 13 stars | none | 2019-05-07 | 盲道识别 障碍物检测 红绿灯检测 人行道检测 | ? |  |
| 8 | [alicema-creator/Python-Qt-Detection-and-recognition-of-sidew...](https://github.com/alicema-creator/Python-Qt-Detection-and-recognition-of-sidewalk-tactile-paving) | github | 10 stars | none | 2024-04-01 | 🔥🔥🔥Python+Qt人行道盲道特征检测识别窗体程序Detection and recognition of sidewalk tactile paving | 4GB GPU? (unverified) |  |
| 9 | [QQ767172261/The-deep-learning-framework-target-detection-alg...](https://github.com/QQ767172261/The-deep-learning-framework-target-detection-algorithm-yolov8-is-used-to-train-blind-paths-and-obsta) | github | 7 stars | none | 2025-12-19 | 使用深度学习框架目标检测算法yolov8训练盲道及障碍物检测数据集，并通过建立gui界面对道路中的盲道及障碍物识别。 | 4GB GPU / CPU |  |
| 10 | [Westley-Winks/tactile-paving-detector](https://github.com/Westley-Winks/tactile-paving-detector) | github | 6 stars | CC-BY-SA-4.0 | 2022-03-31 | Detects tactile paving in images using deep learning | 4GB GPU? (unverified) |  |
| 11 | [tahababou12/EchoPath](https://github.com/tahababou12/EchoPath) | github | 5 stars | none | 2025-02-12 | Smart AI Blind Cane with Object Detection using Yolo11n | 4GB GPU / CPU |  |
| 12 | [dungnotnull/accessible-shopping-visually-impaired-agent-skil...](https://github.com/dungnotnull/accessible-shopping-visually-impaired-agent-skill) | github | 5 stars | MIT | 2026-07-30 | 🛒 Production-grade multi-agent Claude Skill for accessible retail UX & inclusive store design. Audits indoor w... | 4GB GPU? (unverified) |  |
| 13 | [Team-Invisible/HapticRoad-iOS](https://github.com/Team-Invisible/HapticRoad-iOS) | github | 4 stars | none | 2022-01-03 | 시각장애인을 위한 모바일 점자블록 서비스 Haptic Road🚦 | app/CPU |  |
| 14 | [alekziyi/Tactile-paving-Identification](https://github.com/alekziyi/Tactile-paving-Identification) | github | 3 stars | none | 2024-03-09 |  | 4GB GPU? (unverified) |  |
| 15 | [Vante934/blind_road_dataset](https://github.com/Vante934/blind_road_dataset) | github | 2 stars | none | 2026-09-09 | 盲道检测系统 | 4GB GPU? (unverified) |  |

_+6 more kept for this part, listed in the appendix._

## wheelchair routing (`wheelchair_routing`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [tajimei/accessroute](https://github.com/tajimei/accessroute) | github | 49 commits | ? | 2026-03 | JP barrier-free route iOS app, AI chat need extraction (wheelchair, pram, cane, elderly) | app |  |
| 2 | [cine1052rene/wheelway](https://github.com/cine1052rene/wheelway) | github | ? | ? | 2026 | KR wheelchair/crutch subway route PWA, refuses to route on unmeasured door widths | browser |  |
| 3 | [AccessMap (TCAT)](https://tcat.cs.washington.edu/accessmap) | web | live | open source | 2026 | profile-based routing: max uphill/downhill, avoid raised curbs and stairs | browser |  |
| 4 | [openrouteservice wheelchair profile](https://giscience.github.io/openrouteservice/v7.1.1/documentation/routing-options/Routing-Options) | web | docs | GPL-3.0 | ? | maximum_sloped_kerb, maximum_incline, minimum_width, avoid_polygons | CPU (Java) |  |
| 5 | [Valhalla pedestrian type=wheelchair costing](https://github.com/valhalla/valhalla/blob/master/docs/docs/api/route/api-reference.md) | github | docs | MIT | 2026 | step_penalty, max_grade, walking_speed for wheelchair; map matching built in | CPU |  |
| 6 | [RajPShinde/Autonomous_Wheelchair](https://github.com/RajPShinde/Autonomous_Wheelchair) | github | 20 stars | BSD-3-Clause | 2022-03-30 | ROS Package for an Autonomous Wheelchair capable of navigating in an indoor environments. | CPU (native) |  |
| 7 | [ryanmccartney/Autonomous_Electric_Wheelchair](https://github.com/ryanmccartney/Autonomous_Electric_Wheelchair) | github | 15 stars | MIT | 2019-04-26 | Open Autonomous Navigation Platform for Power Wheelchairs | 4GB GPU? (unverified) |  |
| 8 | [ShivamThukral/Wheelchair-Navigation](https://github.com/ShivamThukral/Wheelchair-Navigation) | github | 13 stars | MIT | 2021-12-16 | Real-time wheelchair navigation with shared control using model predictive path integral (MPPI) controller | CPU (native) |  |
| 9 | [LorenzoStucchi/Wheelchair-OsmAnd](https://github.com/LorenzoStucchi/Wheelchair-OsmAnd) | github | 13 stars | MIT | 2021-03-31 | Routing profile for wheelchair to be used in OsmAnd app | browser |  |
| 10 | [EasyWalk-PRIN/OpenNav](https://github.com/EasyWalk-PRIN/OpenNav) | github | 6 stars | MIT | 2026-06-17 | Official code for the OpenNav: Efficient Open Vocabulary 3D Object Detection for Smart Wheelchair Navigation -... | 4GB GPU? (unverified) |  |
| 11 | [species/osrm-wheelchair-profiles](https://github.com/species/osrm-wheelchair-profiles) | github | 6 stars | Unlicense | 2017-11-14 | Routing profiles for different kinds of wheelchair users for OSRM (Open Source Routing Machine) | ? |  |
| 12 | [WillianYe/Multi-robot-dispatch-platform](https://github.com/WillianYe/Multi-robot-dispatch-platform) | github | 5 stars | none | 2024-09-09 | 多智能轮椅调度云平台，实现多轮椅任务分配、自主路径规划导航、状态监控 | CPU (native) |  |
| 13 | [rltoSD/Affordable_Smart_WheelChair_Navigation](https://github.com/rltoSD/Affordable_Smart_WheelChair_Navigation) | github | 5 stars | none | 2019-08-28 | Navigation Stacks Team Repository for the Affordable Smart WheelChair Research at UCSD | 4GB GPU? (unverified) |  |
| 14 | [rajagopalanvg/AN-INTELLIGENT-AIDING-ROBOTIC-DEVICE](https://github.com/rajagopalanvg/AN-INTELLIGENT-AIDING-ROBOTIC-DEVICE) | github | 5 stars | none | 2021-11-05 | An Intelligent Robotics Device (IRD) is developed in order to support safe mobility for disabled or elderly pe... | CPU (native) |  |
| 15 | [abdulrahimzulfiqar/ROS2-Autonomous-Wheelchair](https://github.com/abdulrahimzulfiqar/ROS2-Autonomous-Wheelchair) | github | 4 stars | none | 2026-07-09 | An end-to-end Autonomous Smart Wheelchair powered by ROS 2 (Humble), Raspberry Pi 4, and 2D LiDAR. Features pr... | CPU (native) |  |

_+14 more kept for this part, listed in the appendix._

## accessible navigation app (`access_app`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [DiversMap](https://diversproject.diversmapofficial.com/) | web | ? | closed | ? | JP crowd-shared barrier-free route posting app | app |  |
| 2 | [GL-LinGood/Barrier-free-Traverse](https://github.com/GL-LinGood/Barrier-free-Traverse) | github | 82 stars | none | 2021-03-13 | 设置不同的栅格地图，采用TSP问题的求解思路，应用多种算法实现单个机器人在有障碍和无障碍情况下的全覆盖路径规划： 动态规划、分支限界、蚁群算法、模拟退火以及简单的弓字型遍历。还实现了MTSP，即多旅行商问题。 | 4GB GPU? (unverified) |  |
| 3 | [chikitang/A](https://github.com/chikitang/A) | github | 76 stars | none | 2022-06-08 | !DOCTYPE html> <html lang="en" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark" data-a11... | browser |  |
| 4 | [sozialhelden/wheelmap-frontend](https://github.com/sozialhelden/wheelmap-frontend) | github | 57 stars | MIT | 2026-10-14 | Source code of the wheelmap.org React.js frontend application | browser |  |
| 5 | [sozialhelden/wheelmap-classic](https://github.com/sozialhelden/wheelmap-classic) | github | 47 stars | AGPL-3.0 | 2026-03-03 | :wheelchair: Legacy "classic" wheelmap.org (deprecated) | browser |  |
| 6 | [sozialhelden/wheelmap-android](https://github.com/sozialhelden/wheelmap-android) | github | 37 stars | none | 2017-04-18 | An android app for wheelmap | app/CPU |  |
| 7 | [AccessMap/accessmap](https://github.com/AccessMap/accessmap) | github | 19 stars | none | 2023-12-29 | The AccessMap web application | browser |  |
| 8 | [AccessMap/accessmap-webapp](https://github.com/AccessMap/accessmap-webapp) | github | 11 stars | none | 2023-04-19 | AccessMap web app: interactive accessible mapping services. | browser |  |
| 9 | [AccessMap/AccessMap-webapp-2015](https://github.com/AccessMap/AccessMap-webapp-2015) | github | 11 stars | MIT | 2015-10-26 | Deprecated front end for Access Map Seattle, which was originally created for Seattle's Hack the Commute. For ... | browser |  |
| 10 | [sozialhelden/wheelmap-iphone2](https://github.com/sozialhelden/wheelmap-iphone2) | github | 10 stars | none | 2017-05-24 | Take wheelmap iOS Version to the next level | ? |  |
| 11 | [ukasik123/Testscript-3](https://github.com/ukasik123/Testscript-3) | github | 9 stars | none | 2015-09-05 | <!DOCTYPE html> <html lang="en" class=""> <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object:... | browser |  |
| 12 | [anonympins/libertide](https://github.com/anonympins/libertide) | github | 1 stars | BSD-3-Clause | 2026-10-24 | Libertide - a fully accessible navigation agent helper (LLM analysis of all your OS/Browser apps) | browser |  |
| 13 | [KFNMasheke/AccessMap-SA](https://github.com/KFNMasheke/AccessMap-SA) | github | 1 stars | MIT | 2026-10-23 | Maps access to clinics, schools, libraries, and other essential services | ? |  |
| 14 | [TaskarCenterAtUW/AccessMap](https://github.com/TaskarCenterAtUW/AccessMap) | github | 2 stars | NOASSERTION | 2026-10-14 | A sidewalk routing, accessibillity preferences-aware routing "app" for mobile web. | browser |  |

## pedestrian network generation (Tile2Net-like) (`ped_network`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Tile2Net FOSS4G NA 2026 talk](https://talks.osgeo.org/foss4g-na-2026/talk/WZM9DM) | web | talk 2026-11-03 | n/a | 2026 | Tile2Net raster to GIS network pipeline status | n/a |  |
| 2 | [VIDA-NYU/tile2net](https://github.com/VIDA-NYU/tile2net) | github | 231 stars | BSD-3-Clause | 2026-09-12 | Automated mapping of pedestrian networks from aerial imagery tiles | 4GB GPU? (unverified) |  |
| 3 | [OpenSidewalks/OpenSidewalks-Schema](https://github.com/OpenSidewalks/OpenSidewalks-Schema) | github | 63 stars | NOASSERTION | 2026-10-20 | Repository for the draft proposal of the OpenSidewalks schema | browser | osm_footway |
| 4 | [OpenSidewalks/opensidewalks-data](https://github.com/OpenSidewalks/opensidewalks-data) | github | 11 stars | none | 2023-12-29 |  | 4GB GPU? (unverified) |  |
| 5 | [AccessMap/accessmap-data](https://github.com/AccessMap/accessmap-data) | github | 7 stars | none | 2023-07-06 | Moved to [OpenSidewalks repo](https://github.com/OpenSidewalks/opensidewalks-data) (AccessMap data builds and ... | 4GB GPU? (unverified) |  |
| 6 | [TaskarCenterAtUW/iOSPointMapper](https://github.com/TaskarCenterAtUW/iOSPointMapper) | github | 7 stars | none | 2026-10-14 | iOS application that collects standardized information (in OpenSideWalks format) for accurate mapping of outdo... | app/CPU |  |
| 7 | [OpenSidewalks/osmizer](https://github.com/OpenSidewalks/osmizer) | github | 3 stars | MIT | 2017-09-17 | GeoJSON -> OSM Import Tool for the OpenSidewalks project | 4GB GPU? (unverified) |  |
| 8 | [aki18-1861529/OpenSidewalks-API](https://github.com/aki18-1861529/OpenSidewalks-API) | github | 2 stars | none | 2022-05-20 |  | 4GB GPU? (unverified) |  |
| 9 | [msradam/opensidewalks-nyc](https://github.com/msradam/opensidewalks-nyc) | github | 2 stars | Apache-2.0 | 2026-10-06 | OpenSidewalks NYC: an independent pedestrian network dataset of New York City in the OpenSidewalks Schema, wit... | 4GB GPU? (unverified) | osm_footway |
| 10 | [TCAT-UW/OpenSidewalksCollectioniOS](https://github.com/TCAT-UW/OpenSidewalksCollectioniOS) | github | 2 stars | NOASSERTION | 2020-06-26 |  | app/CPU |  |
| 11 | [idp-tum/sidewalk-width-extractor](https://github.com/idp-tum/sidewalk-width-extractor) | github | 2 stars | MIT | 2022-10-16 | Demo for sidewalk width extraction from aerial orthophotos using neural networks. | 4GB GPU? (unverified) |  |
| 12 | [TaskarCenterAtUW/TDEI-gateway](https://github.com/TaskarCenterAtUW/TDEI-gateway) | github | 1 stars | NOASSERTION | 2026-10-23 | An API for applications consuming data from and publishing data to the Transportation Data Equity Initiative (... | CPU (native) |  |
| 13 | [TaskarCenterAtUW/TDEI-Deployment-Project](https://github.com/TaskarCenterAtUW/TDEI-Deployment-Project) | github | 1 stars | NOASSERTION | 2025-06-26 | The Transportation Data Exchange Initiative (TDEI) Deployment Project. OpenSidewalks is led by the Taskar Cent... | ? |  |
| 14 | [wherobots/tile2net-pt2](https://huggingface.co/wherobots/tile2net-pt2) | huggingface | 0 dl, 0 likes | cc-by-3.0 | 2026-04-23 | HF model: | 4GB GPU? (unverified) |  |
| 15 | [TraversRL: Traversable Pedestrian Pathway Generation With Re...](https://arxiv.org/abs/2607.17479v1) | arxiv | paper | arXiv | 2026-07-20 | Automatically generating pedestrian pathways from aerial images requires producing a connected netwo... | n/a (paper) |  |

_+2 more kept for this part, listed in the appendix._

## OSM sidewalk/footway tools (`osm_footway`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [ほこナビDP (MLIT pedestrian space network data platform)](https://www.hokonavi.go.jp/opendata/) | web | national JP | Govt Standard Terms 2.0 | 2026-03 | JP national schema for footpath links with width/step/slope; nwd-editor web editor | data/browser |  |
| 2 | [歩行空間ネットワークデータ整備仕様 (2024)](https://www.geospatial.jp/ckan/dataset/0401) | web | spec | Govt Standard Terms 2.0 | 2024-12 | node/link barrier attribute spec (step height, width, gradient) for routing | spec |  |
| 3 | [OpenSidewalks Schema + TDEI osw validation lib](https://taskarcenteratuw.github.io/tcat-wiki/opensidewalks/schema) | web | spec | open | 2026 | kerb=raised/rolled/flush, curb ramp nodes, edges; python validator | CPU |  |
| 4 | [kauevestena/osm_sidewalkreator](https://github.com/kauevestena/osm_sidewalkreator) | github | 49 stars | GPL-3.0 | 2026-07-31 | Plugin designated to create the Geometries of Sidewalks (separated from streets) based on OpenStreetMap Street... | 4GB GPU? (unverified) |  |
| 5 | [mapbox/osm-sidewalker](https://github.com/mapbox/osm-sidewalker) | github | 24 stars | BSD-2-Clause | 2017-10-23 | Detecting untagged sidewalks in OSM | browser |  |
| 6 | [a-b-street/speedwalk](https://github.com/a-b-street/speedwalk) | github | 24 stars | Apache-2.0 | 2026-09-18 | Assess and map separate sidewalk ways in OSM | browser |  |
| 7 | [thompsondt/osm-kerb-kit](https://github.com/thompsondt/osm-kerb-kit) | github | 8 stars | NOASSERTION | 2025-06-12 | An open design system for visualizing curbs, crossings, streets, and sidewalk features. | ? |  |
| 8 | [bryanvallejo16/shortest-walking-path-tartu](https://github.com/bryanvallejo16/shortest-walking-path-tartu) | github | 8 stars | CC0-1.0 | 2022-02-09 | Shortest path analysis in OSM walking network in Tartu, Estonia. From the Kissing Students to all cafes fetche... | browser |  |
| 9 | [komar41/crowdsourcing-and-sidewalk-data](https://github.com/komar41/crowdsourcing-and-sidewalk-data) | github | 5 stars | none | 2024-03-11 | Coverage of OpenStreetMap (OSM) sidewalk data and its trustworthiness index | 4GB GPU? (unverified) |  |
| 10 | [YaroShkvorets/ottawa-sidewalk-research](https://github.com/YaroShkvorets/ottawa-sidewalk-research) | github | 3 stars | MIT | 2017-11-05 | validate and prepare sidewalk data for OSM tagging | browser |  |
| 11 | [PeakNav/global-openstreetmap-extraction-slippy-tiles-tar](https://huggingface.co/datasets/PeakNav/global-openstreetmap-extraction-slippy-tiles-tar) | huggingface | 893 dl, 0 likes | other | 2026-09-14 | HF dataset: | data |  |
| 12 | [wikimedia/linked-openstreetmap-wikidata-wikipedia-wikivoyage](https://huggingface.co/datasets/wikimedia/linked-openstreetmap-wikidata-wikipedia-wikivoyage) | huggingface | 424 dl, 2 likes | cc0-1.0 | 2026-10-06 | HF dataset: Linked OpenStreetMap × Wikidata × Wikipedia × Wikivoyage Users of open... | data |  |
| 13 | [cong-khanh/openstreetmap](https://huggingface.co/spaces/cong-khanh/openstreetmap) | huggingface | 0 likes, sdk docker | ? | 2025-12-29 | HF space: docker | browser (Space) |  |
| 14 | [NoeFlandre/what-is-openstreetmap](https://huggingface.co/spaces/NoeFlandre/what-is-openstreetmap) | huggingface | 0 likes, sdk static | ? | 2026-09-16 | HF space: static | browser (Space) |  |
| 15 | [Crowdsourcing and Sidewalk Data: A Preliminary Study on the ...](https://arxiv.org/abs/2210.02350v1) | arxiv | paper | arXiv | 2022-10-05 | Sidewalks play a key role in urban mobility of everyday life. Ideally, sidewalks provide a safe walk... | n/a (paper) |  |

## map matching (`map_matching`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [vlkryl/streetview_objectmapping](https://github.com/vlkryl/streetview_objectmapping) | github | ? | MIT | ? | MRF triangulation of detections across several street-view panos + depth to one GPS point | CPU |  |
| 2 | [Amsterdam-AI-Team/Geolocalization_of_Street_Objects](https://github.com/Amsterdam-AI-Team/Geolocalization_of_Street_Objects) | github | ? | ? | 2020 | refactored MRF triangulation, Faster R-CNN detections from panoramas | CPU |  |
| 3 | [cyang-kth/fmm](https://github.com/cyang-kth/fmm) | github | 1059 stars | Apache-2.0 | 2024-07-09 | Fast map matching, an open source framework in C++ | CPU (native) |  |
| 4 | [graphhopper/map-matching](https://github.com/graphhopper/map-matching) | github | 808 stars | Apache-2.0 | 2020-12-02 | The map matching functionality is now located in the main repository https://github.com/graphhopper/graphhoppe... | app/CPU |  |
| 5 | [bmwcarit/barefoot](https://github.com/bmwcarit/barefoot) | github | 693 stars | Apache-2.0 | 2023-04-14 | Java map matching library for integrating the map into software and services with top online and offline map m... | app/CPU |  |
| 6 | [engcang/FAST-LIO-Localization-QN](https://github.com/engcang/FAST-LIO-Localization-QN) | github | 296 stars | NOASSERTION | 2024-10-28 | A Map-based localization implementation combining FAST-LIO2 as an odometry with Quatro + Nano-GICP as a map ma... | CPU (native) |  |
| 7 | [ad-freiburg/pfaedle](https://github.com/ad-freiburg/pfaedle) | github | 295 stars | GPL-3.0 | 2026-07-24 | Precise map-matching for public transit feeds. Generates high-quality GTFS shapes from OSM data. | CPU (native) |  |
| 8 | [zdsjjtTLG/TrackIt](https://github.com/zdsjjtTLG/TrackIt) | github | 291 stars | MIT | 2026-07-30 | Map Matching Python Package Based on Hidden Markov Model(HMM) | 4GB GPU? (unverified) |  |
| 9 | [wannesm/LeuvenMapMatching](https://github.com/wannesm/LeuvenMapMatching) | github | 256 stars | NOASSERTION | 2024-02-11 | Leuven.MapMatching toolbox for aligning GPS measurements to locations on a map. | 4GB GPU? (unverified) |  |
| 10 | [tengyu-liu/GenDexGrasp](https://github.com/tengyu-liu/GenDexGrasp) | github | 211 stars | none | 2025-09-03 | Code Repository for GenDexGrasp: Generalizing Dexterous Grasping across Robotic Hands via Contact Map Matching | 4GB GPU? (unverified) |  |
| 11 | [mapbox/mapbox-directions-swift](https://github.com/mapbox/mapbox-directions-swift) | github | 206 stars | ISC | 2026-09-15 | Traffic-aware directions and map matching in Swift on iOS, macOS, tvOS, watchOS, and Linux | app/CPU |  |
| 12 | [jagodki/Offline-MapMatching](https://github.com/jagodki/Offline-MapMatching) | github | 174 stars | GPL-3.0 | 2020-08-19 | a QGIS-plugin for matching a trajectory with a network using a Hidden Markov Model and Viterbi algorithm | 4GB GPU? (unverified) |  |
| 13 | [sefinek/osmo-overlay](https://github.com/sefinek/osmo-overlay) | github | 8 stars | NOASSERTION | 2026-10-24 | Telemetry overlays for DJI Osmo Action footage: speed, maps, tilt and G-force. Editor with live preview and ex... | ? |  |
| 14 | [jayykernel/intelligent-dead-reckoning-system](https://github.com/jayykernel/intelligent-dead-reckoning-system) | github | 3 stars | none | 2026-10-23 | Intelligent Dead Reckoning (IDR) system : sensor-agnostic GNSS+INS fusion for Android and edge deployments, co... | 4GB GPU / CPU |  |
| 15 | [addy90/map-matching-2](https://github.com/addy90/map-matching-2) | github | 95 stars | AGPL-3.0 | 2026-09-28 | High Performance Map Matching with Markov Decision Processes (MDPs) and Hidden Markov Models (HMMs). | CPU (native) |  |

_+5 more kept for this part, listed in the appendix._

## street view downloader (`sv_download`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [ProjectSidewalk/sidewalk-panorama-tools](https://github.com/ProjectSidewalk/sidewalk-panorama-tools) | github | ? | ? | 2026 | downloads GSV/Mapillary/Panoramax panos + depth maps for labels, crops per label | CPU |  |
| 2 | [Mapillary map features API (42 point classes incl manholes, ...](https://www.mapillary.com/developer/api-documentation) | web | API | Mapillary terms (CC BY-SA imagery) | 2026 | server-side triangulated object points from 3+ images; free barrier priors | API |  |
| 3 | [OpenStreetCam / KartaView API](https://api.openstreetcam.org/api/doc.html) | web | API | ? | ? | sequences matched to OSM ways, nearby photos by wayId | API |  |
| 4 | [koito19960406/ZenSVI](https://github.com/koito19960406/ZenSVI) | github | 213 stars | MIT | 2026-09-29 | This package is a one-stop solution for downloading, cleaning, analyzing street view imagery | 4GB GPU? (unverified) |  |
| 5 | [kartaview/android](https://github.com/kartaview/android) | github | 138 stars | MIT | 2025-03-29 | Android app for collecting KartaView imagery | app/CPU |  |
| 6 | [stiles/streetview-dl](https://github.com/stiles/streetview-dl) | github | 109 stars | MIT | 2026-04-02 | Discover and download high-resolution Google Street View panoramas by URL or coordinates. Query areas, build g... | 4GB GPU? (unverified) |  |
| 7 | [cplusx/google-street-view-panorama-download](https://github.com/cplusx/google-street-view-panorama-download) | github | 77 stars | MIT | 2019-03-25 | A python tool to download google street view panorama images with given location | 4GB GPU? (unverified) |  |
| 8 | [kartaview/upload-scripts](https://github.com/kartaview/upload-scripts) | github | 64 stars | MIT | 2025-04-03 | Uploader tools for KartaView | 4GB GPU? (unverified) |  |
| 9 | [yousephzidan/gsvp-dl](https://github.com/yousephzidan/gsvp-dl) | github | 62 stars | MIT | 2026-02-25 | Download Google Street View panoramas efficiently. | 4GB GPU? (unverified) |  |
| 10 | [kartaview/ios](https://github.com/kartaview/ios) | github | 47 stars | MIT | 2021-05-24 | iOS app for collecting KartaView data | ? |  |
| 11 | [fdd4s/streetview-dl](https://github.com/fdd4s/streetview-dl) | github | 33 stars | Unlicense | 2024-01-29 | Street View 360 panos downloader | ? |  |
| 12 | [gitouche-sur-osm/mapillary_takeout](https://github.com/gitouche-sur-osm/mapillary_takeout) | github | 26 stars | GPL-3.0 | 2021-07-13 | Download your "unprocessed original" images back from Mapillary | 4GB GPU? (unverified) |  |
| 13 | [kartaview/josm-plugin](https://github.com/kartaview/josm-plugin) | github | 22 stars | NOASSERTION | 2024-07-31 | The KartaView JOSM plugin production version (development version is maintained internally) | app/CPU |  |
| 14 | [bitplane/mapillary_downloader](https://github.com/bitplane/mapillary_downloader) | github | 2 stars | NOASSERTION | 2026-10-22 | better get my mapillary data before it's too late. | 4GB GPU? (unverified) |  |
| 15 | [ZrimYoung/StreetViewDownloader](https://github.com/ZrimYoung/StreetViewDownloader) | github | 5 stars | MIT | 2026-10-21 | Batch download and stitch Google Street View tiles into panoramas using Maps Tile API | 4GB GPU? (unverified) |  |

_+9 more kept for this part, listed in the appendix._

## photo geolocation / visual place recognition (`geoloc_vpr`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Oldcircle/geo-sleuth](https://github.com/Oldcircle/geo-sleuth) | github | 4003 stars | MIT | 2026-10-23 | An agent skill that finds where a photo was taken , OpenStreetMap geometry, elevation skylines, satellite ima.... | 4GB GPU / CPU |  |
| 2 | [AnyLoc/AnyLoc](https://github.com/AnyLoc/AnyLoc) | github | 647 stars | BSD-3-Clause | 2024-03-13 | AnyLoc: Universal Visual Place Recognition (RA-L 2023) | 4GB GPU? (unverified) |  |
| 3 | [VicenteVivan/geo-clip](https://github.com/VicenteVivan/geo-clip) | github | 414 stars | MIT | 2026-10-07 | This is an official PyTorch implementation of our NeurIPS 2023 paper "GeoCLIP: Clip-Inspired Alignment between... | 4GB GPU? (unverified) |  |
| 4 | [serizba/salad](https://github.com/serizba/salad) | github | 384 stars | GPL-3.0 | 2025-10-27 | Optimal Transport Aggregation for Visual Place Recognition | 4GB GPU? (unverified) |  |
| 5 | [amaralibey/MixVPR](https://github.com/amaralibey/MixVPR) | github | 337 stars | none | 2024-06-13 | MixVPR: Feature Mixing for Visual Place Recognition (WACV 2023) | 4GB GPU? (unverified) |  |
| 6 | [gmberton/MegaLoc](https://github.com/gmberton/MegaLoc) | github | 313 stars | MIT | 2026-08-06 | An image retrieval model for any localization task | 4GB GPU? (unverified) |  |
| 7 | [gmberton/awesome-Visual-Place-Recognition](https://github.com/gmberton/awesome-Visual-Place-Recognition) | github | 307 stars | MIT | 2025-09-17 | A curated list of awesome Visual Place Recognition papers | ? |  |
| 8 | [LukasHaas/PIGEON](https://github.com/LukasHaas/PIGEON) | github | 285 stars | NOASSERTION | 2024-07-21 | Code for the CVPR 2024 paper highlight and demo "PIGEON: Predicting Image Geolocations". | 4GB GPU? (unverified) |  |
| 9 | [Lu-Feng/SelaVPR](https://github.com/Lu-Feng/SelaVPR) | github | 269 stars | MIT | 2026-02-04 | Official repository for the ICLR 2024 paper "Towards smooth Adaptation of Pre-trained Models for Visual Place ... | 4GB GPU? (unverified) |  |
| 10 | [arrenglover/openfabmap](https://github.com/arrenglover/openfabmap) | github | 230 stars | NOASSERTION | 2024-07-02 | Open-source C++ code for the FAB-MAP visual place recognition algorithm | CPU (native) |  |
| 11 | [Ivamic/immich-steward](https://github.com/Ivamic/immich-steward) | github | 24 stars | AGPL-3.0 | 2026-10-24 | Self-hosted companion for Immich that finds where photos without GPS were taken. Suggestions from photos taken... | 4GB GPU? (unverified) |  |
| 12 | [skriptkiddy98x/spybrain](https://github.com/skriptkiddy98x/spybrain) | github | 3 stars | none | 2026-10-21 | Local-first OSINT desktop for journalists and investigators: offline photo geolocation (GeoCLIP), breach and p... | 4GB GPU? (unverified) |  |
| 13 | [cn171g11/mma-guessr](https://github.com/cn171g11/mma-guessr) | github | 7 stars | NOASSERTION | 2026-10-19 | MmaGuessr street-view geolocation game (OSM + Mapillary) hosted on GitHub Pages | browser |  |
| 14 | [Xenova/geoclip-large-patch14](https://huggingface.co/Xenova/geoclip-large-patch14) | huggingface | 703 dl, 5 likes | mit | 2024-05-09 | HF model: transformers.js | 4GB GPU / CPU |  |
| 15 | [NemesisAlm/GeolocationCountryClassification](https://huggingface.co/spaces/NemesisAlm/GeolocationCountryClassification) | huggingface | 13 likes, sdk gradio | ? | 2025-04-25 | HF space: gradio | browser (Space) |  |

_+9 more kept for this part, listed in the appendix._

## monocular depth/height (`depth`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | github | 9020 stars | Apache-2.0 | 2026-03-24 | [NeurIPS 2024] Depth Anything V2. A More Capable Foundation Model for Monocular Depth Estimation | 4GB GPU? (unverified) |  |
| 2 | [LiheYoung/Depth-Anything](https://github.com/LiheYoung/Depth-Anything) | github | 8244 stars | Apache-2.0 | 2024-07-17 | [CVPR 2024] Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data. Foundation Model for Monocular... | 4GB GPU? (unverified) |  |
| 3 | [ByteDance-Seed/Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3) | github | 6565 stars | Apache-2.0 | 2026-07-27 | Depth Anything 3 | 4GB GPU? (unverified) |  |
| 4 | [isl-org/MiDaS](https://github.com/isl-org/MiDaS) | github | 5417 stars | MIT | 2024-08-23 | Code for stable monocular depth estimation described in "Ranftl et. al., Towards stable Monocular Depth Estima... | 4GB GPU? (unverified) |  |
| 5 | [nianticlabs/monodepth2](https://github.com/nianticlabs/monodepth2) | github | 4509 stars | NOASSERTION | 2026-10-05 | [ICCV 2019] Monocular depth estimation from a single image | 4GB GPU? (unverified) |  |
| 6 | [prs-eth/Marigold](https://github.com/prs-eth/Marigold) | github | 3243 stars | Apache-2.0 | 2026-09-06 | [CVPR 2024 - Oral, Best Paper Award Candidate] Marigold: Repurposing Diffusion-Based Image Generators for Mono... | GPU 8GB+ likely |  |
| 7 | [isl-org/ZoeDepth](https://github.com/isl-org/ZoeDepth) | github | 2834 stars | MIT | 2025-05-05 | Metric depth estimation from a single image | 4GB GPU? (unverified) |  |
| 8 | [DepthAnything/Video-Depth-Anything](https://github.com/DepthAnything/Video-Depth-Anything) | github | 2293 stars | Apache-2.0 | 2025-10-07 | [CVPR 2025 Highlight] Video Depth Anything: Consistent Depth Estimation for Super-Long Videos | 4GB GPU? (unverified) |  |
| 9 | [tinghuiz/SfMLearner](https://github.com/tinghuiz/SfMLearner) | github | 2015 stars | MIT | 2021-10-26 | An unsupervised learning framework for depth and ego-motion estimation from monocular videos | 4GB GPU? (unverified) |  |
| 10 | [ialhashim/DenseDepth](https://github.com/ialhashim/DenseDepth) | github | 1608 stars | GPL-3.0 | 2022-12-07 | High Quality Monocular Depth Estimation via Transfer Learning | 4GB GPU? (unverified) |  |
| 11 | [TanmayJain09/depthWizard](https://github.com/TanmayJain09/depthWizard) | github | 3 stars | MIT | 2026-10-24 | Semantic-aware uncertainty calibration for single-view DSM elevation estimation (Depth Anything V2 + per-class... | 4GB GPU? (unverified) |  |
| 12 | [AIVFI/Video-Depth-Estimation-Rankings-and-Stereo-Video-Conve...](https://github.com/AIVFI/Video-Depth-Estimation-Rankings-and-Stereo-Video-Conversion-Rankings) | github | 261 stars | none | 2026-10-23 | We look forward to models based on MiniMax H3. ChronoDepth Depth Any Video Depth Anything Depth Pro DepthCraft... | ? |  |
| 13 | [ZhangYangyi03/agentic-eda](https://github.com/ZhangYangyi03/agentic-eda) | github | 1 stars | MIT | 2026-10-23 | Synthesis-script search on open-source EDA (yosys + berkeley-abc), where every candidate must be proven equiva... | ? |  |
| 14 | [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) | huggingface | 1481015 dl, 68 likes | apache-2.0 | 2024-07-05 | HF model: depth-estimation | 4GB GPU? (unverified) |  |
| 15 | [depth-anything/DA3METRIC-LARGE](https://huggingface.co/depth-anything/DA3METRIC-LARGE) | huggingface | 367466 dl, 28 likes | apache-2.0 | 2025-11-13 | HF model: depth-estimation | 4GB GPU? (unverified) |  |

_+9 more kept for this part, listed in the appendix._

## shadow detection and sun position (`shadow_sun`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [mourner/suncalc](https://github.com/mourner/suncalc) | github | 3504 stars | BSD-2-Clause | 2026-10-05 | A tiny JavaScript library for calculating sun/moon positions and phases. | browser |  |
| 2 | [stevewongv/InstanceShadowDetection](https://github.com/stevewongv/InstanceShadowDetection) | github | 180 stars | Apache-2.0 | 2023-10-03 | Instance Shadow Detection (CVPR 2020) | 4GB GPU? (unverified) |  |
| 3 | [hvorragend/ha-blueprints](https://github.com/hvorragend/ha-blueprints) | github | 172 stars | NOASSERTION | 2026-10-23 | Cover Control Automation is a comprehensive Home Assistant blueprint that automatically manages window coverin... | 4GB GPU? (unverified) |  |
| 4 | [clmun/Shadow](https://github.com/clmun/Shadow) | github | 156 stars | none | 2026-04-14 | Show Current Sun Position and Shadow of House (Generate SVG) | 4GB GPU? (unverified) |  |
| 5 | [xw-hu/DSC](https://github.com/xw-hu/DSC) | github | 142 stars | none | 2024-09-09 | Direction-Aware Spatial Context Features for Shadow Detection and Removal / CVPR 2018 (Oral) & TPAMI 2019 | ? |  |
| 6 | [zijundeng/BDRAR](https://github.com/zijundeng/BDRAR) | github | 129 stars | none | 2018-08-05 | Code for the ECCV 2018 paper "Bidirectional Feature Pyramid Network with Recurrent Attention Residual Modules ... | 4GB GPU? (unverified) |  |
| 7 | [stevewongv/SSIS](https://github.com/stevewongv/SSIS) | github | 127 stars | NOASSERTION | 2024-09-17 | Instance Shadow Detection with A Single-Stage Detector [SSIS & SSISv2] (CVPR 2021 Oral & TPAMI 2022) | 4GB GPU? (unverified) |  |
| 8 | [brocoo/BRSunTracker](https://github.com/brocoo/BRSunTracker) | github | 125 stars | Apache-2.0 | 2017-02-02 | Augmented Reality classes that track and displays the sun position on the screen, available on Cocoapods | ? |  |
| 9 | [kittenish/Image-Shadow-Detection-and-Removal](https://github.com/kittenish/Image-Shadow-Detection-and-Removal) | github | 111 stars | none | 2017-11-21 |  | ? |  |
| 10 | [rdmtc/node-red-contrib-sun-position](https://github.com/rdmtc/node-red-contrib-sun-position) | github | 111 stars | Apache-2.0 | 2026-06-24 | This is a ultimate Node-Red Timer, Sun, Moon and Blind flow control. | browser |  |
| 11 | [klausbrunner/sunce](https://github.com/klausbrunner/sunce) | github | 2 stars | MIT | 2026-10-24 | A fast, scripting-friendly CLI solar position and sunrise/sunset/twilight calculator | CPU (native) |  |
| 12 | [manasdutt2003/Shadow_detection_and_removal](https://github.com/manasdutt2003/Shadow_detection_and_removal) | github | 1 stars | none | 2026-10-24 |  | 4GB GPU? (unverified) |  |
| 13 | [jedarden/sun-sim](https://github.com/jedarden/sun-sim) | github | 2 stars | MIT | 2026-10-23 | Interactive sun position simulator with compass rose visualization | browser |  |
| 14 | [heesup/Drone-Shadow-Detection](https://huggingface.co/datasets/heesup/Drone-Shadow-Detection) | huggingface | 8 dl, 0 likes | ? | 2025-12-24 | HF dataset: | data |  |
| 15 | [heesup/Drone-Shadow-Detection](https://huggingface.co/heesup/Drone-Shadow-Detection) | huggingface | 0 dl, 0 likes | apache-2.0 | 2025-12-24 | HF model: | 4GB GPU? (unverified) |  |

_+7 more kept for this part, listed in the appendix._

## low-light enhancement (`lowlight`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [zhihongz/awesome-low-light-image-enhancement](https://github.com/zhihongz/awesome-low-light-image-enhancement) | github | 1855 stars | none | 2026-05-12 | This is a resouce list for low light image enhancement | ? |  |
| 2 | [caiyuanhao1998/Retinexformer](https://github.com/caiyuanhao1998/Retinexformer) | github | 1558 stars | MIT | 2026-05-23 | "Retinexformer: One-stage Retinex-based Transformer for Low-light Image Enhancement" (ICCV 2023 Top-10 Cited 🏆... | 4GB GPU? (unverified) |  |
| 3 | [Li-Chongyi/Zero-DCE](https://github.com/Li-Chongyi/Zero-DCE) | github | 1087 stars | none | 2024-01-12 | Zero-DCE code and model | browser |  |
| 4 | [JIA-Lab-research/SNR-Aware-Low-Light-Enhance](https://github.com/JIA-Lab-research/SNR-Aware-Low-Light-Enhance) | github | 1045 stars | none | 2022-11-21 | This is the official implementation for the paper "SNR-aware low-light image enhancement" in CVPR2022 | 4GB GPU? (unverified) |  |
| 5 | [Fediory/HVI-CIDNet](https://github.com/Fediory/HVI-CIDNet) | github | 855 stars | MIT | 2026-03-09 | [CVPR2025 && NTIRE2025] HVI: A New Color Space for Low-light Image Enhancement (Official Implementation) | 4GB GPU? (unverified) |  |
| 6 | [cuiziteng/Illumination-Adaptive-Transformer](https://github.com/cuiziteng/Illumination-Adaptive-Transformer) | github | 588 stars | Apache-2.0 | 2024-02-27 | 🌕 [BMVC 2022] You Only Need 90K Parameters to Adapt Light: A Light Weight Transformer for Image Enhancement an... | 4GB GPU? (unverified) |  |
| 7 | [pvnieo/Low-light-Image-Enhancement](https://github.com/pvnieo/Low-light-Image-Enhancement) | github | 574 stars | MIT | 2022-08-18 | Python implementation of two low-light image enhancement techniques via illumination map estimation | 4GB GPU? (unverified) |  |
| 8 | [baidut/OpenCE](https://github.com/baidut/OpenCE) | github | 526 stars | MIT | 2018-06-28 | Contrast Enhancement Techniques for low-light images | ? |  |
| 9 | [Li-Chongyi/Zero-DCE_extension](https://github.com/Li-Chongyi/Zero-DCE_extension) | github | 522 stars | none | 2024-01-26 |  | 4GB GPU? (unverified) |  |
| 10 | [jinyeying/night-enhancement](https://github.com/jinyeying/night-enhancement) | github | 467 stars | MIT | 2024-08-29 | [ECCV2022] "Unsupervised Night Image Enhancement: When Layer Decomposition Meets Light-Effects Suppression", h... | browser |  |
| 11 | [yanivbahalul/Riddick](https://github.com/yanivbahalul/Riddick) | github | 1 stars | MIT | 2026-10-24 | Deep Learning Based Low Light Image & Video Enhancement | 4GB GPU? (unverified) |  |
| 12 | [MarkLaMer/Noise-Aware-Deep-Curve-Estimation](https://github.com/MarkLaMer/Noise-Aware-Deep-Curve-Estimation) | github | 1 stars | none | 2026-10-23 | NA-DCE: Noise-Aware Deep Curve Estimation: zero-reference low-light image enhancement in PyTorch. CISC 473 cap... | 4GB GPU? (unverified) |  |
| 13 | [Project-Sarvadrushti/Adverse-Weather-and-Low-Light-Vision-Da...](https://github.com/Project-Sarvadrushti/Adverse-Weather-and-Low-Light-Vision-Datasets) | github | 14 stars | GPL-3.0 | 2026-10-22 | This repository curates datasets for fog, haze, smoke, rain, snow, and low-light image restoration and underst... | 4GB GPU? (unverified) | dehaze_derain |
| 14 | [keras-io/Enhance_Low_Light_Image](https://huggingface.co/spaces/keras-io/Enhance_Low_Light_Image) | huggingface | 158 likes, sdk gradio | ? | 2023-02-10 | HF space: gradio | browser (Space) |  |
| 15 | [keras-io/low-light-image-enhancement](https://huggingface.co/keras-io/low-light-image-enhancement) | huggingface | 21 dl, 88 likes | apache-2.0 | 2024-07-09 | HF model: image-to-image | 4GB GPU? (unverified) |  |

_+9 more kept for this part, listed in the appendix._

## dehaze/derain (`dehaze_derain`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [swz30/Restormer](https://github.com/swz30/Restormer) | github | 2665 stars | MIT | 2025-10-23 | [CVPR 2022--Oral] Restormer: Efficient Transformer for High-Resolution Image Restoration. SOTA for motion debl... | 4GB GPU? (unverified) |  |
| 2 | [kritiksoman/GIMP-ML](https://github.com/kritiksoman/GIMP-ML) | github | 1560 stars | MIT | 2024-10-12 | AI for GNU Image Manipulation Program | 4GB GPU? (unverified) |  |
| 3 | [swz30/MPRNet](https://github.com/swz30/MPRNet) | github | 1397 stars | NOASSERTION | 2024-04-18 | [CVPR 2021] Multi-Stage Progressive Image Restoration. SOTA results for Image deblurring, deraining, and denoi... | 4GB GPU? (unverified) |  |
| 4 | [google-research/maxim](https://github.com/google-research/maxim) | github | 1083 stars | Apache-2.0 | 2023-06-09 | [CVPR 2022 Oral] Official repository for "MAXIM: Multi-Axis MLP for Image Processing". SOTA for denoising, deb... | 4GB GPU? (unverified) |  |
| 5 | [thekevinscott/UpscalerJS](https://github.com/thekevinscott/UpscalerJS) | github | 904 stars | MIT | 2026-10-22 | Enhance Images with Javascript and AI. Increase resolution, retouch, denoise, and more. Open Source, Browser &... | browser |  |
| 6 | [mv-lab/InstructIR](https://github.com/mv-lab/InstructIR) | github | 748 stars | MIT | 2024-09-26 | [ECCV 2024] InstructIR: High-Quality Image Restoration Following Human Instructions https://huggingface.co/spa... | 4GB GPU? (unverified) |  |
| 7 | [zhilin007/FFA-Net](https://github.com/zhilin007/FFA-Net) | github | 730 stars | none | 2023-08-06 | FFA-Net: Feature Fusion Attention Network for Single Image Dehazing | 4GB GPU? (unverified) |  |
| 8 | [Algolzw/image-restoration-sde](https://github.com/Algolzw/image-restoration-sde) | github | 724 stars | MIT | 2024-07-23 | Image Restoration with Mean-Reverting Stochastic Differential Equations, ICML 2023. Winning solution of the NT... | GPU 8GB+ likely |  |
| 9 | [murufeng/CVPR_2021_Papers](https://github.com/murufeng/CVPR_2021_Papers) | github | 660 stars | none | 2021-07-10 | CVPR2021最新论文汇总，主要包括：Transformer, NAS，模型压缩，模型评估，图像分类，检测，分割，跟踪，GAN，超分辨率，图像恢复，去雨，去雾，去模糊，去噪，重建等等 | ? |  |
| 10 | [IDKiro/DehazeFormer](https://github.com/IDKiro/DehazeFormer) | github | 592 stars | MIT | 2024-08-18 | Vision Transformers for Single Image Dehazing | 4GB GPU? (unverified) |  |
| 11 | [chengzi-yuan/HyPolFormer](https://github.com/chengzi-yuan/HyPolFormer) | github | 1 stars | MIT | 2026-10-22 | The official code and model repository for the paper PrismFormer: Polarity-Gated Linear Attention and Wavelet-... | ? |  |
| 12 | [moizishere-droid/Image-Dehazing-AODnet](https://github.com/moizishere-droid/Image-Dehazing-AODnet) | github | 1 stars | none | 2026-10-20 |  | 4GB GPU? (unverified) |  |
| 13 | [nightfury/Image_Face_Upscale_Restoration-GFPGAN](https://huggingface.co/spaces/nightfury/Image_Face_Upscale_Restoration-GFPGAN) | huggingface | 684 likes, sdk gradio | ? | 2022-11-18 | HF space: gradio | browser (Space) |  |
| 14 | [dx8152/Qwen-Image-Edit-2509-Light_restoration](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Light_restoration) | huggingface | 3034 dl, 250 likes | apache-2.0 | 2025-11-25 | HF model: image-to-image | 4GB GPU? (unverified) |  |
| 15 | [avans06/Image_Face_Upscale_Restoration-GFPGAN-RestoreFormer-...](https://huggingface.co/spaces/avans06/Image_Face_Upscale_Restoration-GFPGAN-RestoreFormer-CodeFormer-GPEN) | huggingface | 176 likes, sdk gradio | ? | 2025-11-27 | HF space: gradio | browser (Space) |  |

_+8 more kept for this part, listed in the appendix._

## image inpainting/restoration (`inpaint`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Sanster/IOPaint](https://github.com/Sanster/IOPaint) | github | 23297 stars | Apache-2.0 | 2025-04-29 | Image inpainting tool powered by SOTA AI Model. Remove any unwanted object, defect, people from your pictures ... | GPU 8GB+ likely |  |
| 2 | [Acly/krita-ai-diffusion](https://github.com/Acly/krita-ai-diffusion) | github | 10774 stars | GPL-3.0 | 2026-10-03 | simpler interface for generating images with AI in Krita. Inpaint and outpaint with optional text prompt, no t... | GPU 8GB+ likely |  |
| 3 | [zyddnys/manga-image-translator](https://github.com/zyddnys/manga-image-translator) | github | 10529 stars | GPL-3.0 | 2026-10-11 | Translate manga/image 一键翻译各类图片内文字 https://cotrans.touhou.ai/ (no longer working) | 4GB GPU? (unverified) |  |
| 4 | [advimman/lama](https://github.com/advimman/lama) | github | 10344 stars | Apache-2.0 | 2025-02-05 | 🦙 LaMa Image Inpainting, Resolution-stable Large Mask Inpainting with Fourier Convolutions, WACV 2022 | 4GB GPU? (unverified) |  |
| 5 | [open-mmlab/mmagic](https://github.com/open-mmlab/mmagic) | github | 7475 stars | Apache-2.0 | 2024-08-06 | OpenMMLab Multimodal Advanced, Generative, and Intelligent Creation Toolbox. open the magic 🪄: Generative-AI (... | GPU 8GB+ likely |  |
| 6 | [lxfater/inpaint-web](https://github.com/lxfater/inpaint-web) | github | 6122 stars | GPL-3.0 | 2025-12-23 | A free and open-source inpainting & image-upscaling tool powered by webgpu and wasm on the browser。/ 基于 Webgpu... | browser |  |
| 7 | [zuruoke/watermark-removal](https://github.com/zuruoke/watermark-removal) | github | 5193 stars | none | 2026-08-14 | a machine learning image inpainting task that instinctively removes watermarks from image indistinguishable fr... | 4GB GPU? (unverified) |  |
| 8 | [hgmzhn/manga-translator-ui](https://github.com/hgmzhn/manga-translator-ui) | github | 3112 stars | GPL-3.0 | 2026-10-14 | 基于manga-image-translator 实现的开源漫画AI翻译桌面工具。支持日、韩、英文漫画自动处理，集成OpenAl、Gemini等多翻译引擎；实现OCR文字检测、原文擦除、AI翻译、图像修复、译文排版完整链... | 4GB GPU? (unverified) |  |
| 9 | [ogkalu2/comic-translate](https://github.com/ogkalu2/comic-translate) | github | 2980 stars | Apache-2.0 | 2026-09-11 | AI comic and manga translator app/browser extension for automatically translating comics, manga, manhwa, BDs, ... | browser |  |
| 10 | [zllrunning/video-object-removal](https://github.com/zllrunning/video-object-removal) | github | 2710 stars | MIT | 2019-09-27 | Just draw a bounding box and you can remove the object you want to remove. | 4GB GPU? (unverified) |  |
| 11 | [GigLaboCom/wipemark-app](https://github.com/GigLaboCom/wipemark-app) | github | 3 stars | NOASSERTION | 2026-10-24 | Watermark remover , strips text overlays and image watermarks from photos and video. | CPU (native) |  |
| 12 | [AndreaBonn/image-generator](https://github.com/AndreaBonn/image-generator) | github | 1 stars | GPL-3.0 | 2026-10-24 | Local, offline AI image generator and editor for your own NVIDIA GPU (runs on 8 GB). Pick a task instead of tu... | GPU 8GB+ likely |  |
| 13 | [AbrahamPaulJ/nightmare-mobile](https://github.com/AbrahamPaulJ/nightmare-mobile) | github | 114 stars | NOASSERTION | 2026-10-24 | On-device ComfyUI style node graph for image/video diffusion models on Android. Local SD1.5, SDXL, Flux, Z-ima... | app/CPU |  |
| 14 | [stable-diffusion-v1-5/stable-diffusion-inpainting](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting) | huggingface | 200861 dl, 119 likes | creativeml-openrail-m | 2024-09-06 | HF model: text-to-image | GPU 8GB+ likely |  |
| 15 | [diffusers/stable-diffusion-xl-1.0-inpainting-0.1](https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1) | huggingface | 90488 dl, 390 likes | openrail++ | 2023-09-03 | HF model: text-to-image | GPU 8GB+ likely |  |

_+9 more kept for this part, listed in the appendix._

## Gaussian splatting from few images (`gs_fewshot`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) | github | 24315 stars | NOASSERTION | 2025-10-17 | Original reference implementation of "3D Gaussian Splatting for Real-Time Radiance Field Rendering" | GPU 8GB+ likely |  |
| 2 | [playcanvas/engine](https://github.com/playcanvas/engine) | github | 17129 stars | MIT | 2026-10-23 | Powerful web graphics runtime built on WebGL, WebGPU, WebXR and glTF | browser |  |
| 3 | [playcanvas/supersplat](https://github.com/playcanvas/supersplat) | github | 10450 stars | MIT | 2026-10-23 | 3D Gaussian Splat Editor | browser | splat_viewer |
| 4 | [MrNeRF/awesome-3D-gaussian-splatting](https://github.com/MrNeRF/awesome-3D-gaussian-splatting) | github | 8966 stars | MIT | 2026-10-04 | Curated list of papers and resources focused on 3D Gaussian Splatting, intended to keep pace with the anticipa... | GPU 8GB+ likely |  |
| 5 | [nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat) | github | 5832 stars | Apache-2.0 | 2026-09-19 | CUDA accelerated rasterization of gaussian splatting | GPU 8GB+ likely |  |
| 6 | [dreamgaussian/dreamgaussian](https://github.com/dreamgaussian/dreamgaussian) | github | 4359 stars | MIT | 2024-01-02 | [ICLR 2024 Oral] Generative Gaussian Splatting for Efficient 3D Content Creation | GPU 8GB+ likely |  |
| 7 | [hustvl/4DGaussians](https://github.com/hustvl/4DGaussians) | github | 3985 stars | Apache-2.0 | 2024-10-27 | [CVPR 2024] 4D Gaussian Splatting for Real-Time Dynamic Scene Rendering | GPU 8GB+ likely |  |
| 8 | [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) | github | 3903 stars | GPL-3.0 | 2026-10-24 | Train, inspect, edit, automate, and export 3D Gaussian Splatting scenes from a single native application. | CPU (native) |  |
| 9 | [MrForExample/ComfyUI-3D-Pack](https://github.com/MrForExample/ComfyUI-3D-Pack) | github | 3888 stars | MIT | 2025-12-29 | An extensive node suite that enables ComfyUI to process 3D inputs (Mesh & UV Texture, etc) using cutting edge ... | 4GB GPU / CPU |  |
| 10 | [sparkjsdev/spark](https://github.com/sparkjsdev/spark) | github | 3804 stars | MIT | 2026-10-20 | :sparkles: An advanced 3D Gaussian Splatting renderer for THREE.js | browser | splat_viewer |
| 11 | [rsasaki0109/visloc-rs](https://github.com/rsasaki0109/visloc-rs) | github | 135 stars | NOASSERTION | 2026-10-24 | SfM, visual-inertial SLAM, 3D Gaussian Splatting and localization in pure Rust | CPU (native) |  |
| 12 | [banana484/2026_Arxiv_gaussian-splatting-Paper_List](https://github.com/banana484/2026_Arxiv_gaussian-splatting-Paper_List) | github | 2 stars | none | 2026-10-24 |  | GPU 8GB+ likely |  |
| 13 | [WilliamLiu-1997/Gaussian-Splat-Lite](https://github.com/WilliamLiu-1997/Gaussian-Splat-Lite) | github | 258 stars | Apache-2.0 | 2026-10-24 | High performance 3D Gaussian Splatting (3DGS) renderer for Three.js. WebGPU and WebGL2. Supports PLY, SPZ, Str... | browser | splat_viewer |
| 14 | [KCBtheone/splatatlas-runs](https://huggingface.co/datasets/KCBtheone/splatatlas-runs) | huggingface | 8691 dl, 1 likes | cc-by-4.0 | 2026-09-19 | HF dataset: SplatAtlas Runs Bundle This is the large per-experiment artifact bundl... | data |  |
| 15 | [brandonsmart/splatt3r](https://huggingface.co/spaces/brandonsmart/splatt3r) | huggingface | 76 likes, sdk gradio | ? | 2026-07-14 | HF space: gradio | browser (Space) |  |

_+9 more kept for this part, listed in the appendix._

## feed-forward 3D reconstruction (`ff3d`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [facebookresearch/vggt](https://github.com/facebookresearch/vggt) | github | 14556 stars | NOASSERTION | 2026-05-19 | [CVPR 2025 Best Paper Award] VGGT: Visual Geometry Grounded Transformer | GPU 8GB+ likely |  |
| 2 | [naver/dust3r](https://github.com/naver/dust3r) | github | 7357 stars | NOASSERTION | 2025-09-24 | DUSt3R: Geometric 3D Vision Made Easy | 4GB GPU? (unverified) |  |
| 3 | [facebookresearch/vggt-omega](https://github.com/facebookresearch/vggt-omega) | github | 4684 stars | NOASSERTION | 2026-09-22 | [CVPR 2026 Oral] VGGT Omega | GPU 8GB+ likely |  |
| 4 | [facebookresearch/map-anything](https://github.com/facebookresearch/map-anything) | github | 3853 stars | Apache-2.0 | 2026-08-07 | MapAnything: Universal Feed-Forward Metric 3D Reconstruction | 4GB GPU? (unverified) |  |
| 5 | [rmurai0610/MASt3R-SLAM](https://github.com/rmurai0610/MASt3R-SLAM) | github | 3226 stars | NOASSERTION | 2025-11-09 | [CVPR 2025] MASt3R-SLAM: Real-Time Dense SLAM with 3D Reconstruction Priors | 4GB GPU? (unverified) |  |
| 6 | [naver/mast3r](https://github.com/naver/mast3r) | github | 3140 stars | NOASSERTION | 2025-06-30 | Grounding Image Matching in 3D with MASt3R | 4GB GPU? (unverified) |  |
| 7 | [MIT-SPARK/VGGT-SLAM](https://github.com/MIT-SPARK/VGGT-SLAM) | github | 1164 stars | BSD-2-Clause | 2026-06-29 | VGGT-SLAM: Dense RGB SLAM Optimized on the SL(4) Manifold | GPU 8GB+ likely |  |
| 8 | [HengyiWang/spann3r](https://github.com/HengyiWang/spann3r) | github | 1145 stars | NOASSERTION | 2025-02-25 | [3DV'25 Award Candidate] 3D Reconstruction with Spatial Memory | 4GB GPU? (unverified) |  |
| 9 | [wzzheng/StreamVGGT](https://github.com/wzzheng/StreamVGGT) | github | 987 stars | NOASSERTION | 2025-10-27 | [ICLR 2026] Streaming 4D Visual Geometry Transformer | GPU 8GB+ likely |  |
| 10 | [DengKaiCQ/VGGT-Long](https://github.com/DengKaiCQ/VGGT-Long) | github | 909 stars | NOASSERTION | 2026-03-20 | Official implement of VGGT-Long | GPU 8GB+ likely |  |
| 11 | [sou350121/Spatial-Intelligence-Handbook](https://github.com/sou350121/Spatial-Intelligence-Handbook) | github | 36 stars | NOASSERTION | 2026-10-24 | 空間智能的跨 embodiment 手冊 , , 把 SLAM / VIO / 3D 表徵 / 感測器堆疊 / 部署坑 在 機械臂 / 無人機 / 自駕 / 人形 / 水下 之間橫向比較，底層共用 3DGS / VGG.... | GPU 8GB+ likely |  |
| 12 | [Whitelnzcy/LightRecon3D](https://github.com/Whitelnzcy/LightRecon3D) | github | 1 stars | none | 2026-10-24 | Structure-aware indoor 3D reconstruction based on DUSt3R with line/plane auxiliary supervision. | 4GB GPU? (unverified) |  |
| 13 | [minsu1206/RelationVGGT](https://github.com/minsu1206/RelationVGGT) | github | 3 stars | none | 2026-10-22 | [NeurIPS 2026] RelationVGGT: Visual Geometry Transformers for 3D Spatial Relation Segmentation ; official impl... | GPU 8GB+ likely |  |
| 14 | [facebook/VGGT-1B](https://huggingface.co/facebook/VGGT-1B) | huggingface | 523043 dl, 150 likes | cc-by-nc-4.0 | 2025-03-17 | HF model: image-to-3d | GPU 8GB+ likely |  |
| 15 | [naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric](https://huggingface.co/naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric) | huggingface | 78497 dl, 20 likes | ? | 2024-07-18 | HF model: image-to-3d | 4GB GPU? (unverified) |  |

_+9 more kept for this part, listed in the appendix._

## street change detection (`change_det`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [gmayday1997/SceneChangeDet](https://github.com/gmayday1997/SceneChangeDet) | github | 249 stars | MIT | 2023-03-05 | pytorch implementation of scene change detection | 4GB GPU? (unverified) |  |
| 2 | [DoongLi/Awesome-Scene-Change-Detection](https://github.com/DoongLi/Awesome-Scene-Change-Detection) | github | 169 stars | none | 2026-10-21 | This repo contains a curative list of scene change detection(SCD), including papers, videos, codes, and relate... | ? |  |
| 3 | [SAMMiCA/ChangeSim](https://github.com/SAMMiCA/ChangeSim) | github | 140 stars | MIT | 2022-10-28 | A multi-modal, photo-realistic dataset for online end-to-end scene change detection and more (accepted to IROS... | 4GB GPU? (unverified) |  |
| 4 | [geoyee/LabCD](https://github.com/geoyee/LabCD) | github | 113 stars | GPL-3.0 | 2023-03-20 | 遥感变化检测标注工具『Remote sensing change detection annotation tool』 | CPU (native) |  |
| 5 | [kensakurada/sscdnet](https://github.com/kensakurada/sscdnet) | github | 107 stars | MIT | 2021-10-18 | Semantic Scene Change Detection Network (CSCDNet + SSCDNet) | 4GB GPU? (unverified) |  |
| 6 | [Aryia-Behroziuan/neurons](https://github.com/Aryia-Behroziuan/neurons) | github | 94 stars | none | 2023-11-15 | An ANN is a model based on a collection of connected units or nodes called "artificial neurons", which loosely... | 4GB GPU / CPU |  |
| 7 | [AutoCompSysLab/towards-generalizable-scene-change-detection](https://github.com/AutoCompSysLab/towards-generalizable-scene-change-detection) | github | 84 stars | Apache-2.0 | 2025-12-02 | This repository represents the official implementation of the paper titled "Towards Generalizable Scene Change... | 4GB GPU? (unverified) |  |
| 8 | [geoyee/PdRSCD](https://github.com/geoyee/PdRSCD) | github | 72 stars | Apache-2.0 | 2021-09-08 | 基于『飞桨』的遥感变化检测工具（Remote sensing change detection tool based on『PaddlePaddle』） | 4GB GPU? (unverified) |  |
| 9 | [Breakthrough/python-scene-detection-tutorial](https://github.com/Breakthrough/python-scene-detection-tutorial) | github | 56 stars | none | 2020-07-03 | :snake: Tutorial on detecting video shot changes using Python and OpenCV. Part 1 covers basic threshold detect... | ? |  |
| 10 | [chickenbestlover/awesome-scene-change-detections](https://github.com/chickenbestlover/awesome-scene-change-detections) | github | 55 stars | MIT | 2022-10-13 | A curated list of datasets, codes, and papers related to scene change detection. | ? |  |
| 11 | [Chumsy0725/O-SCD](https://github.com/Chumsy0725/O-SCD) | github | 26 stars | none | 2026-10-20 | Official Repository for "Changes in Real Time: Online Scene Change Detection with Multi-View Fusion" (CVPR26-H... | 4GB GPU? (unverified) |  |
| 12 | [Tatsh/scenechange](https://github.com/Tatsh/scenechange) | github | 5 stars | LGPL-2.1 | 2026-10-19 | Scene change detection plugin for VapourSynth. | CPU (native) |  |
| 13 | [Typical-Player/mimo](https://github.com/Typical-Player/mimo) | github | 1 stars | GPL-3.0 | 2026-10-10 | QML application for scene change detection | CPU (native) |  |
| 14 | [physicl/bedroom-change-detection-state-monitoring](https://huggingface.co/datasets/physicl/bedroom-change-detection-state-monitoring) | huggingface | 3102 dl, 0 likes | other | 2026-06-15 | HF dataset: Bedroom Change Detection & State Monitoring Generated by datapack-impo... | data |  |
| 15 | [Csc722Sp26Group1/CSC722_SP26_GROUP1_CHANGE_DETECTION](https://huggingface.co/datasets/Csc722Sp26Group1/CSC722_SP26_GROUP1_CHANGE_DETECTION) | huggingface | 920 dl, 0 likes | ? | 2026-04-30 | HF dataset: | data |  |

_+9 more kept for this part, listed in the appendix._

## crowdsourced civic issue reporting (`civic`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [Swachhata-MoHUA app (Janaagraha IChangeMyCity platform)](https://play.google.com/store/apps/details?id=com.ichangemycity.swachhbharat) | web | 65.8K reviews, 4041 cities | closed | live | national photo + GPS civic complaint pipeline to ward officers | app |  |
| 2 | [Sugamya Bharat App (DEPwD)](https://g3ict.org/headlines/india-sugamya-bharat-app-to-enable-persons-with-disabilities-register-lack-of-accessibility-in-built-envrionment-and-transport) | web | national | closed | 2025 upgrade (Sarvam chatbot, per Rajya Sabha AU3168) | govt crowd app to report accessibility barriers with photos; the official sink for our detections | app |  |
| 3 | [Jantra civic issue platform](https://www.jantra.app/) | web | claims 50+ Indian cities | closed | 2026 | AI photo categorisation of potholes etc | app |  |
| 4 | [srinu-p-p/Swachhata (CivicLink)](https://github.com/srinu-p-p/Swachhata) | github | ? | ? | ? | mobile-first civic report web app (photo, voice, GPS) | browser |  |
| 5 | [Reclaim Chennai (30 free footpath tools)](https://reclaimchennai.city/) | web | 30 tools | ? | 2026 | GPS-stamped evidence camera with spoof flag, footpath/ward tools, offline PWA | browser |  |
| 6 | [mysociety/fixmystreet](https://github.com/mysociety/fixmystreet) | github | 620 stars | NOASSERTION | 2026-10-23 | This is mySociety's popular map-based reporting platform: easy to install in new countries and regions | ? |  |
| 7 | [markaspot/mark-a-spot](https://github.com/markaspot/mark-a-spot) | github | 72 stars | GPL-2.0 | 2026-10-23 | Civic issue tracking platform with Drupal 11 backend and Vue.js PWA frontend · Open311 compliant | ? |  |
| 8 | [codeforamerica/open311dashboard](https://github.com/codeforamerica/open311dashboard) | github | 58 stars | none | 2012-04-02 | Visualizing and analyzing Open311 data on one unified, customizable dashboard | 4GB GPU? (unverified) |  |
| 9 | [visiblegovernment/django-fixmystreet](https://github.com/visiblegovernment/django-fixmystreet) | github | 54 stars | none | 2011-11-01 | A django port of MySociety's FixMyStreet, maintained by VisibleGovernment.ca | 4GB GPU? (unverified) |  |
| 10 | [mysociety/fixmystreet-mobile](https://github.com/mysociety/fixmystreet-mobile) | github | 49 stars | NOASSERTION | 2023-04-20 | Cordova application for making reports to FixMyStreet | browser |  |
| 11 | [City-of-Bloomington/uReport](https://github.com/City-of-Bloomington/uReport) | github | 42 stars | AGPL-3.0 | 2026-10-12 | Issue tracking and constituent relationship management system with an Open311 (GeoReport v2) endpoint designed... | ? |  |
| 12 | [open311/open311.github.io](https://github.com/open311/open311.github.io) | github | 39 stars | none | 2022-05-24 | Open311 Specs and Wiki | browser |  |
| 13 | [bensheldon/open311status](https://github.com/bensheldon/open311status) | github | 37 stars | MIT | 2026-10-20 | Open311 Status monitors and aggregates the status of dozens of Open311 API endpoints, providing benchmarks and... | ? |  |
| 14 | [codeforamerica/three](https://github.com/codeforamerica/three) | github | 33 stars | BSD-3-Clause | 2021-03-11 | An easy-to-use Python wrapper for the Open311 API. | 4GB GPU? (unverified) |  |
| 15 | [codeforamerica/open311](https://github.com/codeforamerica/open311) | github | 32 stars | MIT | 2018-08-08 | A Ruby wrapper for the Open311 API | ? |  |

_+8 more kept for this part, listed in the appendix._

## walkability score (`walkability`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [arXiv 2608.20026 SVI to street quality indicators (Qwen2.5-V...](https://arxiv.org/pdf/2608.20026) | arxiv | paper | arXiv | 2026-08 | VLM sidewalk presence as Bernoulli per segment from GSV | n/a |  |
| 2 | [Safetipin (Safety Audit + Nite app)](https://safetipin.com/our-apps) | web | 8 Indian cities incl Jaipur, 800+ audits each | closed | live | 9-param audit incl Walkpath, Lighting; Nite app = phone on vehicle windscreen auto-capture | app |  |
| 3 | [ITDP India walkability audits (People Near Transit)](https://itdp.in/topic-resources/walking-and-cycling) | web | reports 2026 | reports | 2026-07 | footpath audit framework (21 km Chennai), PNT method | n/a |  |
| 4 | [plus-mobilitylab/netascore](https://github.com/plus-mobilitylab/netascore) | github | 65 stars | MIT | 2026-10-24 | NetAScore - Network Assessment Score Toolbox for Sustainable Mobility | ? |  |
| 5 | [perryrjohnson/Walk-Score](https://github.com/perryrjohnson/Walk-Score) | github | 22 stars | none | 2019-05-29 | Reverse Engineering Walk Score's API Methodology: What makes a location "Walkable"? | 4GB GPU? (unverified) |  |
| 6 | [kcredit/Walkable-Accessibility-Score](https://github.com/kcredit/Walkable-Accessibility-Score) | github | 16 stars | none | 2025-09-15 | This repository contains the code for calculating an open source Walkable Accessibility Score (WAS), a spatial... | 4GB GPU? (unverified) |  |
| 7 | [YellowO2/streetview-to-3d](https://github.com/YellowO2/streetview-to-3d) | github | 14 stars | MIT | 2026-10-15 | Reconstructs a walkable street corridor into a 3D point cloud from Google Street View / Apple Look Around pano... | 4GB GPU? (unverified) |  |
| 8 | [ropensci-archive/rwalkable](https://github.com/ropensci-archive/rwalkable) | github | 12 stars | NOASSERTION | 2022-05-10 | :no_entry: ARCHIVED :no_entry: Walkability Scores | ? |  |
| 9 | [chris31415926535/walkscore](https://github.com/chris31415926535/walkscore) | github | 9 stars | NOASSERTION | 2023-12-19 | Score Walks with the Walk Score API | ? |  |
| 10 | [samanthaandrews/abq-street-art](https://github.com/samanthaandrews/abq-street-art) | github | 7 stars | Apache-2.0 | 2018-03-14 | Coding Bootcamp Capstone - Interactive Walkable Art Map - Find and locate public art in Albuquerque, learn mor... | ? |  |
| 11 | [ubc-library-rc/qgis-walkability](https://github.com/ubc-library-rc/qgis-walkability) | github | 5 stars | CC-BY-4.0 | 2025-04-07 | Using spatial network analysis in QGIS to calculate a walkability index for downtown Vancouver | browser |  |
| 12 | [redfin/WalkScoreApi](https://github.com/redfin/WalkScoreApi) | github | 5 stars | none | 2015-08-19 | Example use of Walk Score APIs in Node.js | browser |  |
| 13 | [sarahhagstrom/chrome-walkscore](https://github.com/sarahhagstrom/chrome-walkscore) | github | 4 stars | none | 2013-11-13 | Right-Click Walk Score Chrome Extension | browser |  |
| 14 | [PasLoin/Brussels-Pedestrian-Network](https://github.com/PasLoin/Brussels-Pedestrian-Network) | github | 1 stars | MIT | 2026-10-24 | Pedestrian network quality tool for Brussels , walkability scores, missing crossings & sidewalk gap detection.... | 4GB GPU? (unverified) |  |
| 15 | [copilot-autogent/realestate-radar](https://github.com/copilot-autogent/realestate-radar) | github | 1 stars | none | 2026-10-19 | 實價登錄雷達 , Taiwan real estate analytics: actual transaction prices, map view, price history, walkability scores | browser |  |

_+10 more kept for this part, listed in the appendix._

## accessibility audit tools (`audit_tools`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [arXiv 2602.09216 Project Sidewalk Chandigarh (VLM mission gu...](https://arxiv.org/abs/2602.09216) | arxiv | paper | arXiv | 2026-02 | first Project Sidewalk India deployment, India-adapted tags, VLM guidance | n/a | audit_tools |
| 2 | [Project Sidewalk API](https://projectsidewalk.org/api) | web | 56 cities, 11 countries | open data | 2026-07 | labels as GeoJSON/CSV incl Chandigarh | API |  |
| 3 | [Siasat Hyderabad footpath walk (IRC 1.8 m / 2.5 m clear widt...](https://www.siasat.com/from-nampally-to-jubilee-hills-footpaths-exist-on-paper-only-3543100) | web | news 2026-09-23 | news | 2026-09 | manual walk audit of 5 localities, none met IRC width | n/a |  |
| 4 | [CAG Chennai Road to Open Data (footpath KPIs + quality toolk...](https://www.cag.org.in/project/road-open-data) | web | city | ? | 2016 | footpath condition KPIs + citizen assessment app, Chennai | app |  |
| 5 | [lfelker/sidewalk_quality_assessment](https://github.com/lfelker/sidewalk_quality_assessment) | github | 1 stars | none | 2017-05-12 | metric calculation for municipal sidewalk data and extrapolated sidewalk data compared to ground truth osm ped... | 4GB GPU? (unverified) |  |
| 6 | [CUUATS/sidewalk-inventory](https://github.com/CUUATS/sidewalk-inventory) | github | 1 stars | none | 2018-11-30 | Sidewalk Inventory and Assessment of the Champaign-Urbana Urbanized Area | 4GB GPU? (unverified) |  |
| 7 | [CUUATS/sidewalk-map](https://github.com/CUUATS/sidewalk-map) | github | 1 stars | BSD-3-Clause | 2018-11-30 | ArcGIS map application for displaying Sidewalk Network Inventory and Assessment data | browser |  |
| 8 | [gianluca-fonseca/streetlens](https://github.com/gianluca-fonseca/streetlens) | github | 1 stars | MIT | 2026-09-02 | Open, bilingual street-audit platform for Costa Rica: sidewalk condition, Ley 7600 accessibility, drainage, an... | browser |  |
| 9 | [achikiCOA/SidewalkAssessmentTool](https://github.com/achikiCOA/SidewalkAssessmentTool) | github | 0 stars | none | 2026-06-11 |  | browser |  |
| 10 | [Mary-h86/SidewalkToolbox](https://github.com/Mary-h86/SidewalkToolbox) | github | 0 stars | none | 2021-09-26 | Scalable Solutions for the Measurement, Assessment and Analysis of Urban Sidewalks | ? |  |
| 11 | [abdenny/vh-assessment](https://github.com/abdenny/vh-assessment) | github | 0 stars | none | 2023-01-11 | http://scared-sidewalk.surge.sh/ | browser |  |
| 12 | [shampan-xyz/sidewalk-explorer-](https://github.com/shampan-xyz/sidewalk-explorer-) | github | 0 stars | BSD-3-Clause | 2026-04-06 | Interactive viewer for the Sidewalk Network Inventory and Assessment | browser |  |
| 13 | [shampan-xyz/sidewalk-inventory](https://github.com/shampan-xyz/sidewalk-inventory) | github | 0 stars | BSD-3-Clause | 2026-04-06 | Sidewalk Network Inventory and Assessment of the Champaign-Urbana Urbanized Area | ? |  |
| 14 | [TobiasHollander/Nashville-Sidewalk-Folium-Map](https://github.com/TobiasHollander/Nashville-Sidewalk-Folium-Map) | github | 0 stars | none | 2021-05-06 | A folium map of Nashville's sidewalk inventory for ada self-assessment. | 4GB GPU? (unverified) |  |
| 15 | [SIM: A mapping framework for built environment auditing base...](https://arxiv.org/abs/2505.24076v1) | arxiv | paper | arXiv | 2025-05-29 | Built environment auditing refers to the systematic documentation and assessment of urban and rural ... | n/a (paper) |  |

_+1 more kept for this part, listed in the appendix._

## deck.gl/MapLibre route animation (`deckgl_route`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [asdfghj1237890/mini-macau](https://github.com/asdfghj1237890/mini-macau) | github | 637 stars | MIT | 2026-10-24 | Trilingual 3D visualization of Macau's public transit and aviation , LRT, buses, ferries, and MFM airport fli.... | browser |  |
| 2 | [amalChandran/trail-android](https://github.com/amalChandran/trail-android) | github | 516 stars | MIT | 2026-10-08 | 🚕 Simple, smooth animation for route / polylines on google maps using projections. | app/CPU |  |
| 3 | [RodrigoHamuy/react-three-map](https://github.com/RodrigoHamuy/react-three-map) | github | 322 stars | MIT | 2026-07-18 | Use React and Three.js inside Mapbox and Maplibre | browser |  |
| 4 | [egmalt/house-planner](https://github.com/egmalt/house-planner) | github | 298 stars | MIT | 2026-10-01 | Self-hosted house planner: true-scale 2D floor plan, 3D, satellite map overlay, sewer, electrical, water and u... | browser |  |
| 5 | [opengeos/mapwidget](https://github.com/opengeos/mapwidget) | github | 255 stars | MIT | 2026-10-12 | Custom Jupyter widgets for creating interactive 2D/3D maps using popular JavaScript libraries with bidirection... | browser |  |
| 6 | [pratik-123/GoogleMap](https://github.com/pratik-123/GoogleMap) | github | 119 stars | none | 2020-10-07 | Google Map to use create path on map and play vehicle on path like Uber and Ola | app/CPU |  |
| 7 | [jblsmith/street-view-movie-maker](https://github.com/jblsmith/street-view-movie-maker) | github | 114 stars | none | 2020-11-25 | Generating animated previews of map routes from street view | ? |  |
| 8 | [dvt3d/maplibre-three-plugin](https://github.com/dvt3d/maplibre-three-plugin) | github | 99 stars | Apache-2.0 | 2026-07-26 | a bridge plugin that cleverly connects MapLibre GL JS with Three.js, enabling developers to implement 3D rende... | browser |  |
| 9 | [Open-X-Humanoid/BICMap](https://github.com/Open-X-Humanoid/BICMap) | github | 93 stars | NOASSERTION | 2026-09-10 | A WebGL-based robotics map visualization SDK for SLAM maps, point clouds, 3D models, and robot navigation. | browser |  |
| 10 | [luciobaiocchi/heard](https://github.com/luciobaiocchi/heard) | github | 89 stars | Apache-2.0 | 2026-08-08 | Offline group-safety mesh for hikers: ESP32 + GPS + LoRa, with a firmware-in-the-loop simulator and 3D replay ... | 4GB GPU? (unverified) |  |
| 11 | [kenjiyoshidahome2026-bit/ortho-earth](https://github.com/kenjiyoshidahome2026-bit/ortho-earth) | github | 10 stars | none | 2026-10-24 | Open-source 3D globe map engine for the browser , WebGPU, MapLibre GL JS compatible API, 3D Tiles, terrain at.... | browser |  |
| 12 | [FelisPimeja/osm-simple3d-editor](https://github.com/FelisPimeja/osm-simple3d-editor) | github | 16 stars | ISC | 2026-10-24 | Browser-based 3D building editor for OpenStreetMap (Simple 3D Buildings): MapLibre + three.js, no backend | browser |  |
| 13 | [bradleybond512/crystal-ball](https://github.com/bradleybond512/crystal-ball) | github | 11 stars | NOASSERTION | 2026-10-24 | Tauri 2 desktop intelligence platform , Cesium.js 3D globe, 185 live panels, MCP server for Claude Code, and .... | browser |  |

## browser splat viewers (`splat_viewer`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [antimatter15/splat](https://github.com/antimatter15/splat) | github | 3081 stars | MIT | 2025-11-16 | WebGL 3D Gaussian Splat Viewer | browser |  |
| 2 | [mkkellogg/GaussianSplats3D](https://github.com/mkkellogg/GaussianSplats3D) | github | 2926 stars | MIT | 2025-10-19 | Three.js-based implementation of 3D Gaussian splatting | browser |  |
| 3 | [yzslab/gaussian-splatting-lightning](https://github.com/yzslab/gaussian-splatting-lightning) | github | 1113 stars | NOASSERTION | 2026-05-25 | A 3D Gaussian Splatting framework with various derived algorithms and an interactive web viewer | browser |  |
| 4 | [playcanvas/model-viewer](https://github.com/playcanvas/model-viewer) | github | 712 stars | MIT | 2026-08-13 | 3D Model Viewer supporting glTF and 3D Gaussian Splats | browser |  |
| 5 | [playcanvas/supersplat-viewer](https://github.com/playcanvas/supersplat-viewer) | github | 603 stars | MIT | 2026-10-23 | User-friendly, high-performance viewer for 3D Gaussian splats | browser |  |
| 6 | [Visionary-Laboratory/visionary](https://github.com/Visionary-Laboratory/visionary) | github | 531 stars | Apache-2.0 | 2026-10-15 | Visionary: The World Model Carrier Built on WebGPU-Powered Gaussian Splatting Platform | browser |  |
| 7 | [reall3d-com/Reall3dViewer](https://github.com/reall3d-com/Reall3dViewer) | github | 519 stars | MIT | 2026-09-11 | This is a 3DGS(3D Gaussian Splatting) viewer built on Three.js, with features for marking, measurements, prese... | browser |  |
| 8 | [KeKsBoTer/web-splat](https://github.com/KeKsBoTer/web-splat) | github | 310 stars | Apache-2.0 | 2026-10-23 | 3D Gaussian Splatting Renderer implemented in WebGPU (WGPU) and Rust | browser |  |
| 9 | [sciencebanda09/topoloka](https://github.com/sciencebanda09/topoloka) | github | 2 stars | MIT | 2026-10-24 | One phone video in, a photorealistic metric indoor twin out - free-roam Gaussian-splat viewer + 5 cm navigatio... | browser |  |
| 10 | [Sen2Maker/BuildingWebViewer](https://github.com/Sen2Maker/BuildingWebViewer) | github | 3 stars | none | 2026-10-24 | 本地三维数据工具箱：网格、线框、点云与三维高斯，支持点云处理和导出。Local 3D toolbox for meshes, wireframes, point clouds and Gaussian splats. B... | browser |  |
| 11 | [pearsonkyle/Gaussian-Splat-Viewer](https://huggingface.co/spaces/pearsonkyle/Gaussian-Splat-Viewer) | huggingface | 4 likes, sdk static | ? | 2026-04-26 | HF space: static | browser (Space) |  |
| 12 | [vettorazi/splatViewer](https://huggingface.co/spaces/vettorazi/splatViewer) | huggingface | 1 likes, sdk static | ? | 2023-09-30 | HF space: static | browser (Space) |  |
| 13 | [spatialai/SplatViewer](https://huggingface.co/spatialai/SplatViewer) | huggingface | 0 dl, 0 likes | ? | 2024-08-05 | HF model: | GPU 8GB+ likely |  |

## voice navigation for blind (`blind_voice`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [intelligent-blind-stick](https://gitee.com/wang-bingqi/intelligent-blind-stick) | gitee | ? | MulanPSL-2.0 | ? | OpenCV colour tactile path detection + ultrasonic + voice | CPU |  |
| 2 | [team8/outdoor-blind-navigation (SightWalk)](https://github.com/team8/outdoor-blind-navigation) | github | ? | ? | ? | sidewalk navigation for blind, YOLOv4-tiny, audio + vibration | CPU/edge |  |
| 3 | [wink-wink-wink555/blind_navigation (ARIADNE)](https://github.com/wink-wink-wink555/blind_navigation) | github | ? | ? | 2025 | YOLO tactile paving + voice + multi-agent assistant, Flask | 4GB GPU |  |
| 4 | [StreetViewAI (UIST 25)](https://dl.acm.org/doi/10.1145/3746059.3747756) | web | paper | paper | 2025-09 | accessible street view for blind users with context-aware AI agent | n/a |  |
| 5 | [soundscape-community/soundscape](https://github.com/soundscape-community/soundscape) | github | 45 stars | MIT | 2026 | community-maintained Microsoft Soundscape iOS (3D audio beacons) | app |  |
| 6 | [soundscape-community/soundscape-web-client](https://github.com/soundscape-community/soundscape-web-client) | github | ? | ? | 2026 | Soundscape-like spatial audio callouts in the BROWSER, any platform | browser |  |
| 7 | [Scottish-Tech-Army/Soundscape-Android](https://scottish-tech-army.github.io/Soundscape-Android) | github | 10 stars | Other | 2026-08 | Android Soundscape rebuild (2026), street preview before visit | app |  |
| 8 | [Scottish-Tech-Army/soundscape-backend](https://github.com/Scottish-Tech-Army/soundscape-backend) | github | 2 stars | MIT | 2026-07 | backend tiles (pmtiles) for Soundscape | CPU |  |
| 9 | [VoiceVista (Soundscape resurrection)](https://www.perkins.org/resource/microsoft-soundscape-app-being-discontinued) | web | App Store | closed (MIT base) | 2023+ | free iOS successor of Soundscape | app |  |
| 10 | [soundscapecloud/soundscape](https://github.com/soundscapecloud/soundscape) | github | 745 stars | MIT | 2018-10-02 | Soundscape - a personal music streaming server | CPU (native) |  |
| 11 | [AndyShaman/BYDMate](https://github.com/AndyShaman/BYDMate) | github | 441 stars | NOASSERTION | 2026-10-14 | BYD DiLink app (3.0/5.0/5.1, UI7): split screen 1/3+2/3, navigation on instrument cluster, Yandex Navigator on... | app/CPU |  |
| 12 | [Nitnelav/awesome-acoustic](https://github.com/Nitnelav/awesome-acoustic) | github | 152 stars | CC0-1.0 | 2026-10-13 | A list of awesome open-source acoustic packages and resources. | browser |  |
| 13 | [microsoft/soundscape](https://github.com/microsoft/soundscape) | github | 151 stars | MIT | 2023-08-29 | An iOS application/service that aids navigation through spatialized audio | app/CPU |  |
| 14 | [scikit-maad/scikit-maad](https://github.com/scikit-maad/scikit-maad) | github | 140 stars | BSD-3-Clause | 2026-05-21 | Open-source and modular toolbox for quantitative soundscape analysis in Python | 4GB GPU? (unverified) |  |
| 15 | [benjiyaya/ComfyUI-H3-VisionPromptor](https://github.com/benjiyaya/ComfyUI-H3-VisionPromptor) | github | 108 stars | MIT | 2026-08-09 | Feed an idea (plus optional reference images) and get Minimax H3 prompt , with shots, camera vocabulary, dial.... | 4GB GPU? (unverified) |  |

_+16 more kept for this part, listed in the appendix._

## India street datasets (`india_data`)

| # | name | host | stars / dl | licence | last update | what it covers | runs on | also |
|---|---|---|---|---|---|---|---|---|
| 1 | [e-Yantra IITB Semantic Segmentation datasets of Indian roads](https://www.kaggle.com/datasets/eyantraiit/semantic-segmentation-datasets-of-indian-roads) | kaggle | 3227 imgs | ? | 2021 | road / footpath / pothole / shallow path masks, knee-height delivery-robot view | data |  |
| 2 | [Indian Footpath Damage Segmentation Dataset (Pune)](https://zenodo.org/records/15414238) | zenodo | 583 imgs, 4.5 GB | open (Zenodo) | 2025-05 | pixel masks of footpath cracks with severity, Sci Data 2025 s41597-025-06207-x | data |  |
| 3 | [DataCluster Footpath Image Dataset (India)](https://www.kaggle.com/datasets/dataclusterlabs/footpath-dataset) | kaggle | 500+ imgs sample | commercial (sample only) | ? | footpath images from 200+ Indian cities | data |  |
| 4 | [IDD India Driving Dataset (IIIT-H)](https://idd.insaan.iiit.ac.in/dataset/details) | web | 10,003 seg imgs, 46,588 det | IDD terms (registration) | ? | Hyderabad/Bangalore, 34 classes incl sidewalk, curb, billboard, autorickshaw | data |  |
| 5 | [NanoNets/IndianRoadsObjectDetectionDataset](https://github.com/NanoNets/IndianRoadsObjectDetectionDataset) | github | 49 stars | none | 2021-03-18 |  | 4GB GPU / CPU |  |
| 6 | [Ruthvik9/IDD-PeD](https://github.com/Ruthvik9/IDD-PeD) | github | 14 stars | none | 2026-02-18 | This repo contains the implementation of the intention and trajectory baselines trained and evaluated on our I... | 4GB GPU? (unverified) |  |
| 7 | [shubham1810/idd3d_kit](https://github.com/shubham1810/idd3d_kit) | github | 14 stars | none | 2022-10-20 | Code and Details for IDD-3D paper accepted at WACV 2023. | ? |  |
| 8 | [anishmadan23/semantic-segmentation-indian-driving-dataset](https://github.com/anishmadan23/semantic-segmentation-indian-driving-dataset) | github | 13 stars | none | 2020-05-01 | This repository implements Semantic Segmentation of the Indian Driving Dataset. It contains two architectures ... | 4GB GPU? (unverified) |  |
| 9 | [DAYA7624/Semantic-Segmentation-on-Indian-Driving-Dataset](https://github.com/DAYA7624/Semantic-Segmentation-on-Indian-Driving-Dataset) | github | 8 stars | none | 2022-02-12 |  | 4GB GPU? (unverified) |  |
| 10 | [mohanrajmit/IDD](https://github.com/mohanrajmit/IDD) | github | 7 stars | none | 2021-05-10 | Indian driving dataset using semantic segmetnation | 4GB GPU? (unverified) |  |
| 11 | [Dalageo/road-segmentation-idd](https://github.com/Dalageo/road-segmentation-idd) | github | 7 stars | GPL-3.0 | 2026-04-23 | Distinguishing Urban Roads from Non-Road Regions in the Indian Driving Dataset(IDD) Using Binary Deep Learning... | 4GB GPU? (unverified) |  |
| 12 | [AbhayVAshokan/Road-Segmentation-Dataset](https://github.com/AbhayVAshokan/Road-Segmentation-Dataset) | github | 7 stars | none | 2021-01-03 | Road Dataset for semantic segmentation: extracted from Indian Driving Dataset | ? |  |
| 13 | [AbhayVAshokan/Semantic-Segmentation-of-Road-Surface](https://github.com/AbhayVAshokan/Semantic-Segmentation-of-Road-Surface) | github | 6 stars | none | 2022-12-08 | Implements semantic segmentation of road surface using India Driving Dataset (IDD). | 4GB GPU? (unverified) |  |
| 14 | [yashmarathe21/semantic-segmentation-on-indian-driving-datase...](https://github.com/yashmarathe21/semantic-segmentation-on-indian-driving-dataset) | github | 6 stars | none | 2020-05-31 | Implemented UNet and PSPNet architectures using Tensorflow on idd20k_lite dataset. The idd20k_lite dataset has... | 4GB GPU / CPU |  |
| 15 | [geosensing/soundscape](https://github.com/geosensing/soundscape) | github | 1 stars | none | 2026-10-21 | Measuring Sound Levels on Streets of Delhi and Bangalore | browser |  |

_+13 more kept for this part, listed in the appendix._

## GitHub code search (5 key queries)

| query | total | items returned | distinct repos (first 12: repo -> file) | status |
|---|---|---|---|---|
| `"project sidewalk" api labels` | 371 | 50 | ProjectSidewalk/SidewalkWebpage -> frontend/css/pages/api-docs/raw-labels.css; ProjectSidewalk/sidewalk-panorama-tools -> docs/api-fields.md; Amsterdam-AI-Team/Accessible_Route_Planning -> notebooks/4b. Get project sidewalk crossing features.ipynb | 200 |
| `"surface" "incline" "kerb" routing footway` | 818 | 50 | GIScience/openrouteservice -> ors-api/src/main/java/org/heigit/ors/api/requests/routing/RequestProfileParamsRestrictions.java; osmandapp/OsmAnd-resources -> routing/routing.xml; streetcomplete/StreetComplete -> CHANGELOG.md; ayaan-gupta/curbcut -> api/curbcut/routing.py; RandomSearch18/marvellous-mapping-machine -> backend/routing_engine.py; fryanpan/family-bike-map -> docs/research/BC-239-map-data-routing-review.md; kauevestena/oswm_codebase -> generation/routing_demo_gen.py; Mironiusz/piwo1-hackyeah -> plans_finished/routing_engine/ROUTING_ENGINE_PRD.md; graphhopper/graphhopper -> core/src/main/resources/com/graphhopper/util/de_DE.txt; oliwia9g/HackYeah2026 -> backend/engine/routing.py; tilezen/vector-datasource -> docs/CHANGELOG.md; kauevestena/opensidewalkmap_beta -> oswm_runtime/routing/profile_rules.py | 200 |
| `curb_ramp sidewalk filename:labels` | 4 | 4 | ProjectSidewalk/RampNet -> scripts/build_sparse_labels.py; anncy0413/StreetAudit -> website-demo/Label-main/backend/config/labels.maps-mini.json; ProjectSidewalk/sidewalk-panorama-tools -> tests/test_rawlabels_mapillary.py | 200 |
| `opensidewalks` | 1146 | 50 | MobilityData/Mobility-Data-Interoperability-Principles -> data/specifications/opensidewalks.md; OpenSidewalks/OpenSidewalks-Schema -> resources/josm/presets/opensidewalks.xml; TaskarCenterAtUW/tcat-wiki -> docs/assistant/os-connect/concept/opensidewalks.md; Liamzhangg/RoamAble -> back_end/scripts/fetch_opensidewalks.js; sbauguessBAH/ITS-JPO-Astro-Public -> src/content/posts/press2024its4us_opensidewalks.htm.md; taranprits2/uOttaMove -> server/scripts/fetch_opensidewalks.js; trackawesomelist/trackawesomelist -> content/2023/04/20/README.md; APA-Technology-Division/urban-and-regional-planning-resources -> README.md; OpenSidewalks/OpenSidewalkQuestsMVP -> OpenSidewalks/app/src/main/java/de/tcat/opensidewalks/Prefs.java; icopy-site/awesome-cn -> docs/awesome/urban-and-regional-planning-resources.md; OpenSidewalks/opensidewalks_cli -> opensidewalks_cli/cli.py | 200 |
| `wheelchair costing valhalla` | 1656 | 50 | stadiamaps/valinor -> valhalla-proto/proto/options.proto; carpooling-egy/matching-engine -> internal/adapter/valhalla/client/proto/options.proto; KrakeKrake/P92-GeoTab-Road-Compliance -> nhvr-valhalla/proto/descriptors/options.proto; jarodwille/navapp -> proto/options.proto; openmove/om-valhalla -> proto/options.proto; ep-infosec/22_teslamotors_valhalla -> valhalla/sif/dynamiccost.h; zzerogu/moduCNU -> backend/valhalla_server/valhalla/valhalla/sif/wheelchair_cost.h; Pedritos22/LajkonikGO -> backend/app/road_routes.py; eric-erki/valhalla -> src/sif/dynamiccost.cc; routeco/valhalla-python -> src/sif/transitcost.cc; bisrun/valhalla3 -> src/sif/dynamiccost.cc; valhalla/valhalla -> docs/docs/api/map-matching.md | 200 |

## Appendix: overflow rows

**sidewalk_seg**: [nvidia/segformer-b5-finetuned-cityscapes-1024-1024](https://huggingface.co/nvidia/segformer-b5-finetuned-cityscapes-1024-1024); [facebook/mask2former-swin-large-mapillary-vistas-s...](https://huggingface.co/facebook/mask2former-swin-large-mapillary-vistas-semantic); [nvidia/segformer-b0-finetuned-cityscapes-1024-1024](https://huggingface.co/nvidia/segformer-b0-finetuned-cityscapes-1024-1024); [segments/sidewalk-semantic](https://huggingface.co/datasets/segments/sidewalk-semantic); [UCLA-VAIL/SidewalkBench-Assets](https://huggingface.co/datasets/UCLA-VAIL/SidewalkBench-Assets); [sergiopaniego/segformer-b0-segments-sidewalk-finet...](https://huggingface.co/spaces/sergiopaniego/segformer-b0-segments-sidewalk-finetuned); [andresgtn/sidewalk-semantic-segmentation](https://huggingface.co/spaces/andresgtn/sidewalk-semantic-segmentation); [Can VLMs Reliably Assess Sidewalk Accessibility At...](https://arxiv.org/abs/2609.17882v1); [Lightweight Machine Learning-Driven Monocular Side...](https://arxiv.org/abs/2608.25178v1); [Safety-oriented sidewalk and road segmentation for...](https://arxiv.org/abs/2607.21137v1); [Monocular 3D Occupancy Perception for Robots on Si...](https://arxiv.org/abs/2606.19122v2)

**curb_ramp**: [wumboingwumbos/Autonomous-Powerwheel](https://github.com/wumboingwumbos/Autonomous-Powerwheel); [projectsidewalk/rampnet-dataset](https://huggingface.co/datasets/projectsidewalk/rampnet-dataset); [projectsidewalk/rampnet-crop-model-dataset-round2](https://huggingface.co/datasets/projectsidewalk/rampnet-crop-model-dataset-round2); [projectsidewalk/rampnet-model](https://huggingface.co/projectsidewalk/rampnet-model); [starkAhmed43/leak-curber-kcat-km-starter](https://huggingface.co/starkAhmed43/leak-curber-kcat-km-starter); [build-small-hackathon/curbcheck](https://huggingface.co/spaces/build-small-hackathon/curbcheck); [starkAhmed43/leak-curber-enzyme-classification-sta...](https://huggingface.co/starkAhmed43/leak-curber-enzyme-classification-starter); [Curbinton/SlimGPT](https://huggingface.co/spaces/Curbinton/SlimGPT); [RampNet: A Two-Stage Pipeline for Bootstrapping Cu...](https://arxiv.org/abs/2508.09415v1)

**stairs**: [akshara-ns/stairs-vs-nonstairs-automl](https://huggingface.co/akshara-ns/stairs-vs-nonstairs-automl); [nepyope/pi05-can-30fps-staircase-12k](https://huggingface.co/nepyope/pi05-can-30fps-staircase-12k); [andrei12304/escalier-infini-infinite-staircase-cha...](https://huggingface.co/spaces/andrei12304/escalier-infini-infinite-staircase-challenge); [mimadintropin/devil-s-staircase-ascension](https://huggingface.co/spaces/mimadintropin/devil-s-staircase-ascension); [TRISTAR: Triple-Signal Stair Recognition and Visio...](https://arxiv.org/abs/2607.03818v1); [Staircase Recognition and Location Based on Polari...](https://arxiv.org/abs/2505.19026v3); [Raising the Bar(ometer): Identifying a User's Stai...](https://arxiv.org/abs/2410.02790v1); [StairNetV3: Depth-aware Stair Modeling using Deep ...](https://arxiv.org/abs/2308.06715v1)

**pothole**: [keremberke/yolov8n-pothole-segmentation](https://huggingface.co/keremberke/yolov8n-pothole-segmentation); [keremberke/yolov8m-pothole-segmentation](https://huggingface.co/keremberke/yolov8m-pothole-segmentation); [keremberke/pothole-segmentation](https://huggingface.co/datasets/keremberke/pothole-segmentation); [keremberke/yolov8s-pothole-segmentation](https://huggingface.co/keremberke/yolov8s-pothole-segmentation); [sovitrath/pothole_yolov8_nano](https://huggingface.co/spaces/sovitrath/pothole_yolov8_nano); [meet25284/pothole-repair-env](https://huggingface.co/spaces/meet25284/pothole-repair-env); [Edge-Cloud Collaborative Pothole Detection via Onb...](https://arxiv.org/abs/2605.10055v1); [Real-time pothole detection with onboard sensors a...](https://arxiv.org/abs/2511.11643v1); [iWatchRoadv2: Pothole Detection, Geospatial Mappin...](https://arxiv.org/abs/2510.16375v1); [stable Video-Based Pothole Detection and Area Esti...](https://arxiv.org/abs/2505.21049v1)

**road_damage**: [cvtechniques/Road_Damage_Detection_USA](https://huggingface.co/datasets/cvtechniques/Road_Damage_Detection_USA); [rezzzq/yolo12s-road-damage-rdd2022](https://huggingface.co/rezzzq/yolo12s-road-damage-rdd2022); [dronefreak/rdd2022-yolov8m](https://huggingface.co/dronefreak/rdd2022-yolov8m); [nsr51324/Road_Damage_Object_Detection](https://huggingface.co/nsr51324/Road_Damage_Object_Detection); [shrey-14/Road-damage-detection](https://huggingface.co/spaces/shrey-14/Road-damage-detection); [Cyril-36/road-damage-detection](https://huggingface.co/spaces/Cyril-36/road-damage-detection); [StripRFNet: A Strip Receptive Field and Shape-Awar...](https://arxiv.org/abs/2510.16115v1); [Joint Training of Image Generator and Detector for...](https://arxiv.org/abs/2509.03465v1); [Advancing Pavement Distress Detection in Developin...](https://arxiv.org/abs/2408.05649v1); [Deep Learning Approaches in Pavement Distress Iden...](https://arxiv.org/abs/2308.00828v1)

**manhole**: [boom5497/NQhhAhYo](https://github.com/boom5497/NQhhAhYo); [liup93/manhole](https://huggingface.co/datasets/liup93/manhole); [P-khosravi/manhole-detection-yolo26](https://huggingface.co/P-khosravi/manhole-detection-yolo26); [delima87/manhole_covers_dataset](https://huggingface.co/datasets/delima87/manhole_covers_dataset); [badsaarow/manhole-worker-safety-7b-lora](https://huggingface.co/badsaarow/manhole-worker-safety-7b-lora); [Siddhaarth94/qwen2-7b-ManholeDetail](https://huggingface.co/Siddhaarth94/qwen2-7b-ManholeDetail); [Dezzex2/Manhole_Damage_LLM](https://huggingface.co/spaces/Dezzex2/Manhole_Damage_LLM); [GentleSky/Manhole_Analysis_Platform](https://huggingface.co/spaces/GentleSky/Manhole_Analysis_Platform); [Road Damage and Manhole Detection using Deep Learn...](https://arxiv.org/abs/2510.03797v1); [Adversarial Manhole: Challenging Monocular Depth E...](https://arxiv.org/abs/2408.14879v1); [YOLOv8-Based Visual Detection of Road Hazards: Pot...](https://arxiv.org/abs/2311.00073v1); [Performance Analysis Of Neuro Genetic Algorithm Ap...](https://arxiv.org/abs/1209.1048v1)

**obstacle**: [kunalrana123/Moon-Rock-Obstacle-Detection](https://huggingface.co/spaces/kunalrana123/Moon-Rock-Obstacle-Detection); [ameliang/rt-detr-street-obstacle-detection](https://huggingface.co/spaces/ameliang/rt-detr-street-obstacle-detection); [projectsidewalk/sidewalk-validator-ai-obstacle](https://huggingface.co/projectsidewalk/sidewalk-validator-ai-obstacle); [unixio/nova-obstacle-detection](https://huggingface.co/unixio/nova-obstacle-detection); [krishan1298/Robot_Obstacle_Detection](https://huggingface.co/krishan1298/Robot_Obstacle_Detection); [Smart Navigation for Visual Prostheses in Virtual ...](https://arxiv.org/abs/2610.05772v1); [Milo, a Fully Autonomous Indoor/Outdoor Robotic Gu...](https://arxiv.org/abs/2607.19530v1); [PEDESTRIAN: An Egocentric Vision Dataset for Obsta...](https://arxiv.org/abs/2512.19190v1); [DISHA: Low-Energy Sparse Transformer at Edge for O...](https://arxiv.org/abs/2406.15864v1)

**parked_vehicle**: [audyddl/illegal-parking-models](https://huggingface.co/audyddl/illegal-parking-models); [theAshes/illegal-parking-detector](https://huggingface.co/spaces/theAshes/illegal-parking-detector); [dhruvv1402/illegal_parking](https://huggingface.co/spaces/dhruvv1402/illegal_parking); [Mothership: A Two Tier Autonomous Refuse Collectio...](https://arxiv.org/abs/2610.22461v1); [MicroVision: An Open Dataset and Benchmark Models ...](https://arxiv.org/abs/2603.18192v1); [Zenbo Patrol: A Social Assistive Robot Based on Mu...](https://arxiv.org/abs/2510.04190v1); [Deep Learning for On-Street Parking Violation Pred...](https://arxiv.org/abs/2505.06818v1)

**tactile**: [TayR-D/patchwork-cve](https://github.com/TayR-D/patchwork-cve); [boom5497/zsgfoHYW](https://github.com/boom5497/zsgfoHYW); [EmbedEarth/tactile-paving](https://huggingface.co/datasets/EmbedEarth/tactile-paving); [LARAD: Layout-Aware Road Anomaly Detection via Spa...](https://arxiv.org/abs/2607.12858v1); [GuideTWSI: A Diverse Tactile Walking Surface Indic...](https://arxiv.org/abs/2603.07060v1); [SimTac: A Physics-Based Simulator for Vision-Based...](https://arxiv.org/abs/2511.11456v1)

**wheelchair_routing**: [Stockfish-2921769/AutoBarrier-CPS](https://github.com/Stockfish-2921769/AutoBarrier-CPS); [DanielCuevas1208/gtfs-accessibility-auditor](https://github.com/DanielCuevas1208/gtfs-accessibility-auditor); [pouyapd/SafeTraj-Experiments](https://github.com/pouyapd/SafeTraj-Experiments); [unitreerobotics/G1_WBT_Inspire_Push_Wheelchair](https://huggingface.co/datasets/unitreerobotics/G1_WBT_Inspire_Push_Wheelchair); [samitesla/various_wheelchairs](https://huggingface.co/datasets/samitesla/various_wheelchairs); [sd-concepts-library/wheelchair](https://huggingface.co/sd-concepts-library/wheelchair); [jstnde/laura_wheelchair](https://huggingface.co/jstnde/laura_wheelchair); [fouadmahmoud281/ai-wheelchair-navigation-yolov5](https://huggingface.co/fouadmahmoud281/ai-wheelchair-navigation-yolov5); [derthieme/wheelmatch-wheelchair-wizard](https://huggingface.co/spaces/derthieme/wheelmatch-wheelchair-wizard); [memox2211/medical-marvels-wheelchair-hero-s-journe...](https://huggingface.co/spaces/memox2211/medical-marvels-wheelchair-hero-s-journey); [ChairNav: Cross-Embodiment Pre-training and Person...](https://arxiv.org/abs/2610.24012v1); [Gridnberg: A Topography-Aware Pedestrian Routing D...](https://arxiv.org/abs/2607.22523v1); [Optimizing Nursing Care Taxi Dispatch using Intege...](https://arxiv.org/abs/2606.29725v1); [OmniPath: A Multi-Modal Agentic Framework for Audi...](https://arxiv.org/abs/2606.24129v1)

**ped_network**: [Slow Brain, Fast Planner: Latency-Resilient VLM-Au...](https://arxiv.org/abs/2606.20458v1); [UrbanVGGT: Scalable Sidewalk Width Estimation from...](https://arxiv.org/abs/2603.22531v2)

**map_matching**: [weijiezz/map-matching-dataset](https://huggingface.co/datasets/weijiezz/map-matching-dataset); [Hierarchical Spatial-Temporal Graph-Enhanced Model...](https://arxiv.org/abs/2603.24054v1); [UM3: Unsupervised Map to Map Matching](https://arxiv.org/abs/2508.16874v2); [PartSLAM: Unsupervised Part-based Scene Modeling f...](https://arxiv.org/abs/2306.10782v1); [Map matching queries on realistic input graphs und...](https://arxiv.org/abs/2211.02951v3)

**sv_download**: [WilliamSampaio/street-view-image-extractor](https://github.com/WilliamSampaio/street-view-image-extractor); [charlottev/google-streetview-images-by-country](https://huggingface.co/datasets/charlottev/google-streetview-images-by-country); [facebook/mask2former-swin-large-mapillary-vistas-p...](https://huggingface.co/facebook/mask2former-swin-large-mapillary-vistas-panoptic); [paidaixing/Image_mapillary_Street_level](https://huggingface.co/datasets/paidaixing/Image_mapillary_Street_level); [BilalSardar/Google-Street-View-360-panorama-Image-...](https://huggingface.co/spaces/BilalSardar/Google-Street-View-360-panorama-Image-Downloader); [canada-guesser/canadian_streetview_cities_models](https://huggingface.co/canada-guesser/canadian_streetview_cities_models); [lebfla11/streetview-eu-geocell-demo](https://huggingface.co/spaces/lebfla11/streetview-eu-geocell-demo); [everettshen/StreetView360X](https://huggingface.co/everettshen/StreetView360X); [A citizen science toolkit to collect human percept...](https://arxiv.org/abs/2403.00174v4)

**geoloc_vpr**: [GaryHuang/NTU_geolocation](https://huggingface.co/datasets/GaryHuang/NTU_geolocation); [0xRafie/asean-geolocation](https://huggingface.co/datasets/0xRafie/asean-geolocation); [MVRL/geoclip-location-encoder](https://huggingface.co/MVRL/geoclip-location-encoder); [VicenteVivanco/geoclip-geolocation](https://huggingface.co/VicenteVivanco/geoclip-geolocation); [geolocation-from-speech-demo/geolocation-from-spee...](https://huggingface.co/spaces/geolocation-from-speech-demo/geolocation-from-speech-demo); [Cross-View Geolocalization and Disaster Mapping wi...](https://arxiv.org/abs/2408.06761v1); [Cross-view image geo-localization with Panorama-BE...](https://arxiv.org/abs/2408.05475v1); [LLMGeo: Benchmarking Large Language Models on Imag...](https://arxiv.org/abs/2405.20363v1); [Visual Place Recognition](https://arxiv.org/abs/2211.14533v1)

**depth**: [LiheYoung/depth-anything-large-hf](https://huggingface.co/LiheYoung/depth-anything-large-hf); [depth-anything/Depth-Anything-V2](https://huggingface.co/spaces/depth-anything/Depth-Anything-V2); [LiheYoung/Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything); [depth-anything/DA3-BENCH](https://huggingface.co/datasets/depth-anything/DA3-BENCH); [dangth2004/KITTI-Depth-Estimation](https://huggingface.co/datasets/dangth2004/KITTI-Depth-Estimation); [Which Depth Estimator for Jetson AGX Orin? A 2026 ...](https://arxiv.org/abs/2610.27199v1); [AnchorD: Metric Grounding of Monocular Depth Using...](https://arxiv.org/abs/2605.02667v1); [MetricAnything: Scaling Metric Depth Pretraining w...](https://arxiv.org/abs/2601.22054v2); [Benchmark on Monocular Metric Depth Estimation in ...](https://arxiv.org/abs/2510.04723v1)

**shadow_sun**: [MKFMIKU/Instance-Shadow-Removal](https://huggingface.co/MKFMIKU/Instance-Shadow-Removal); [MochunniaN1/IMAGE_SHADOW_REMOVAL_CHALLENGE](https://huggingface.co/MochunniaN1/IMAGE_SHADOW_REMOVAL_CHALLENGE); [dalgiuyu/Unet-Shadow-Removal](https://huggingface.co/spaces/dalgiuyu/Unet-Shadow-Removal); [RenDetNet: Weakly-supervised Shadow Detection with...](https://arxiv.org/abs/2408.17143v1); [CoolWalks for active mobility in urban street netw...](https://arxiv.org/abs/2405.01225v2); [Delving into Dark Regions for stable Shadow Detect...](https://arxiv.org/abs/2402.13631v1); [Detect Any Shadow: Segment Anything for Video Shad...](https://arxiv.org/abs/2305.16698v2)

**lowlight**: [keras-io/lowlight-enhance-mirnet](https://huggingface.co/keras-io/lowlight-enhance-mirnet); [ishicode/low-light-dataset](https://huggingface.co/datasets/ishicode/low-light-dataset); [aryadytm/photo-low-light-enhance](https://huggingface.co/spaces/aryadytm/photo-low-light-enhance); [OLiVES-Lowlight/OLiVES](https://huggingface.co/datasets/OLiVES-Lowlight/OLiVES); [LyliaEngine/lowlight_02](https://huggingface.co/LyliaEngine/lowlight_02); [LEIQ-Assessor: Multi-dimensional Quality Assessmen...](https://arxiv.org/abs/2606.29752v1); [Lightweight Low-Light Image Enhancement via Distri...](https://arxiv.org/abs/2604.11071v3); [Unsupervised Image Prior via Prompt Learning and C...](https://arxiv.org/abs/2405.11478v1); [Equipping Diffusion Models with Differentiable Spa...](https://arxiv.org/abs/2404.09735v1)

**dehaze_derain**: [ohayonguy/PMRF_blind_face_image_restoration](https://huggingface.co/ohayonguy/PMRF_blind_face_image_restoration); [deepghs/image_restoration](https://huggingface.co/deepghs/image_restoration); [Anbinh93/image_restoration](https://huggingface.co/datasets/Anbinh93/image_restoration); [laoduanaaa/Image_Restoration_Datasets](https://huggingface.co/datasets/laoduanaaa/Image_Restoration_Datasets); [Real-World Remote Sensing Image Dehazing: Benchmar...](https://arxiv.org/abs/2503.17966v2); [Image Deraining via Self-supervised Reinforcement ...](https://arxiv.org/abs/2403.18270v1); [Dual-Scale Single Image Dehazing Via Neural Augmen...](https://arxiv.org/abs/2209.05913v1); [Model-Based Single Image Deep Dehazing](https://arxiv.org/abs/2111.10943v3)

**inpaint**: [richarrrddd/lama_testing.ptl](https://huggingface.co/richarrrddd/lama_testing.ptl); [Sanster/Lama-Cleaner-lama](https://huggingface.co/spaces/Sanster/Lama-Cleaner-lama); [diffusers/stable-diffusion-xl-inpainting](https://huggingface.co/spaces/diffusers/stable-diffusion-xl-inpainting); [facebook/lama](https://huggingface.co/datasets/facebook/lama); [lexlms/legal_lama](https://huggingface.co/datasets/lexlms/legal_lama); [3DTexMOR: 3D Gaussian Multi-Object Removal via Tex...](https://arxiv.org/abs/2610.11198v1); [Zero-Shot Object Removal via Attention Masking, La...](https://arxiv.org/abs/2609.28342v1); [Task-Decoupled Image Inpainting Framework for Clas...](https://arxiv.org/abs/2410.02894v1); [Paint by Inpaint: Learning to Add Image Objects by...](https://arxiv.org/abs/2404.18212v3)

**gs_fewshot**: [Voxel51/gaussian_splatting](https://huggingface.co/datasets/Voxel51/gaussian_splatting); [szymanowiczs/splatter_image](https://huggingface.co/spaces/szymanowiczs/splatter_image); [camenduru/gaussian-splatting](https://huggingface.co/camenduru/gaussian-splatting); [splats/Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-D...](https://huggingface.co/splats/Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled-oQ4e); [kishimisu/3d-gaussian-splatting-webgl](https://huggingface.co/kishimisu/3d-gaussian-splatting-webgl); [Rethinking Sparse-View 3D Gaussian Splatting: A Fe...](https://arxiv.org/abs/2610.25887v1); [SparseStreet: Sparse Gaussian Splatting for Real-T...](https://arxiv.org/abs/2606.03909v1); [DIAL-GS: Dynamic Instance Aware Reconstruction for...](https://arxiv.org/abs/2511.06632v2); [EMD: Explicit Motion Modeling for High-Quality Str...](https://arxiv.org/abs/2411.15582v2)

**ff3d**: [naver/DUSt3R_ViTLarge_BaseDecoder_512_dpt](https://huggingface.co/naver/DUSt3R_ViTLarge_BaseDecoder_512_dpt); [facebook/vggt](https://huggingface.co/spaces/facebook/vggt); [facebook/vggt-omega](https://huggingface.co/spaces/facebook/vggt-omega); [dslighfdsl/dust3r_new](https://huggingface.co/datasets/dslighfdsl/dust3r_new); [DorayakiLin/DorayakiLin_vggt_pick_coke_on_mat_2](https://huggingface.co/datasets/DorayakiLin/DorayakiLin_vggt_pick_coke_on_mat_2); [G3T Up! Gravity Aligned Coordinate Frames Simplify...](https://arxiv.org/abs/2605.27372v1); [DelowlightSplat: Feed-Forward Gaussian Splatting f...](https://arxiv.org/abs/2605.26629v1); [Mix3R: Mixing Feed-forward Reconstruction and Gene...](https://arxiv.org/abs/2605.03359v1); [Feed-Forward 3D Scene Modeling: A Problem-Driven P...](https://arxiv.org/abs/2604.14025v2)

**change_det**: [DarthReca/actu-change-detection](https://huggingface.co/DarthReca/actu-change-detection); [Intel/scene-change-detection](https://huggingface.co/Intel/scene-change-detection); [ghomasHudson/style_change_detection](https://huggingface.co/ghomasHudson/style_change_detection); [Hamzakoybasi/change-detection-gradio](https://huggingface.co/spaces/Hamzakoybasi/change-detection-gradio); [abdulaziz01/Satellite_Change_Detection](https://huggingface.co/spaces/abdulaziz01/Satellite_Change_Detection); [Online Geometric Change Detection via Scene Decomp...](https://arxiv.org/abs/2609.17302v1); [From Image Hashing to Scene Change Detection](https://arxiv.org/abs/2605.12259v1); [Information-Bottleneck Driven Binary Neural Networ...](https://arxiv.org/abs/2507.03504v2); [CEBSNet: Change-Excited and Background-Suppressed ...](https://arxiv.org/abs/2505.15322v1)

**civic**: [SIAMESEFISH/Chennai-Civic-issues-Reporting-Website...](https://github.com/SIAMESEFISH/Chennai-Civic-issues-Reporting-Website-final); [Ankitkumar06102005/Junsuno-app](https://github.com/Ankitkumar06102005/Junsuno-app); [mysociety/mysociety-docs-theme](https://github.com/mysociety/mysociety-docs-theme); [anshumanshahu/Civic_Issues](https://huggingface.co/datasets/anshumanshahu/Civic_Issues); [Mostlysane28/bbmp-civic-issue-detector](https://huggingface.co/Mostlysane28/bbmp-civic-issue-detector); [Akhand3110/civic-issue-ai-backend](https://huggingface.co/spaces/Akhand3110/civic-issue-ai-backend); [Sayemkhan1111/civic-issue-classifier](https://huggingface.co/spaces/Sayemkhan1111/civic-issue-classifier); [Intelligent Pothole Detection and Road Condition A...](https://arxiv.org/abs/1710.02595v2)

**walkability**: [msrbuilds/roji-denki-3d-store](https://github.com/msrbuilds/roji-denki-3d-store); [AEnigmista/ViT-Walkability](https://huggingface.co/AEnigmista/ViT-Walkability); [mdamandeh/user-conditioned-walkability-assessment](https://huggingface.co/datasets/mdamandeh/user-conditioned-walkability-assessment); [mdamandeh/user-conditioned-walkability-assessment-...](https://huggingface.co/mdamandeh/user-conditioned-walkability-assessment-model); [asdlfjsdfj/walkability-ph](https://huggingface.co/spaces/asdlfjsdfj/walkability-ph); [kernrocke/walkability-cvd-risk](https://huggingface.co/spaces/kernrocke/walkability-cvd-risk); [From Street View Imagery to Street Quality Indicat...](https://arxiv.org/abs/2608.20026v1); [Walkable to Whom? Capturing Subjective Variability...](https://arxiv.org/abs/2608.06934v1); [Assessing the livability within the 15-minute city...](https://arxiv.org/abs/2601.14307v1); [WalkCLIP: Multimodal Learning for Urban Walkabilit...](https://arxiv.org/abs/2511.21947v1)

**audit_tools**: [Estimating city-level travel patterns using street...](https://arxiv.org/abs/1802.02915v1)

**blind_voice**: [mracette/soundscape](https://github.com/mracette/soundscape); [andrewmcgivery/obsidian-soundscapes](https://github.com/andrewmcgivery/obsidian-soundscapes); [museumsvictoria/spatial_audio_server](https://github.com/museumsvictoria/spatial_audio_server); [ta012/SSLAM](https://github.com/ta012/SSLAM); [GoliathFrostMinaret/Endel-Desktop-Latest-2026](https://github.com/GoliathFrostMinaret/Endel-Desktop-Latest-2026); [newsbubbles/ismail](https://github.com/newsbubbles/ismail); [2three1y/insomniaos](https://github.com/2three1y/insomniaos); [sidfeels/visually-impaired-llm-assistance-dataset](https://huggingface.co/datasets/sidfeels/visually-impaired-llm-assistance-dataset); [nehdf/Landmark_Navigation_Blind_Spot](https://huggingface.co/datasets/nehdf/Landmark_Navigation_Blind_Spot); [sidfeels/phi-3.5-visually-impaired-assistant](https://huggingface.co/sidfeels/phi-3.5-visually-impaired-assistant); [OhMondon/Walking-Assistant-for-the-Visually-Impair...](https://huggingface.co/spaces/OhMondon/Walking-Assistant-for-the-Visually-Impaired); [sameersyed/blind-navigation-backend](https://huggingface.co/spaces/sameersyed/blind-navigation-backend); [Navigating Independence: A Survey of Visually Impa...](https://arxiv.org/abs/2606.00025v1); [Advancing Accessibility: Augmented Reality Solutio...](https://arxiv.org/abs/2512.19047v1); [Multimodal Feedback for Task Guidance in Augmented...](https://arxiv.org/abs/2510.01690v1); [DARAS: Dynamic Audio-Room Acoustic Synthesis for B...](https://arxiv.org/abs/2507.08135v2)

**india_data**: [priyanshi0609/Indian-Address-Parser](https://github.com/priyanshi0609/Indian-Address-Parser); [geosensing/streetscope](https://github.com/geosensing/streetscope); [izzako/segformer-b5-finetuned-IDD-L2_v2](https://huggingface.co/izzako/segformer-b5-finetuned-IDD-L2_v2); [khushhiii08/IDD_Detection_for_YOLO](https://huggingface.co/datasets/khushhiii08/IDD_Detection_for_YOLO); [Furqan7007/IDDAW_OFFICIAL](https://huggingface.co/datasets/Furqan7007/IDDAW_OFFICIAL); [vamsikkomati/anpr_idd](https://huggingface.co/spaces/vamsikkomati/anpr_idd); [facebook/mms-tts-idd](https://huggingface.co/facebook/mms-tts-idd); [bhasker412/IDD-YOLO-Tracking](https://huggingface.co/spaces/bhasker412/IDD-YOLO-Tracking); [ziyan98/E2K-cd82-Qwen3.8-27B-sft_first_idd-cc-iter...](https://huggingface.co/ziyan98/E2K-cd82-Qwen3.8-27B-sft_first_idd-cc-iter7); [Performance Analysis of YOLOv11 and YOLOv8 for Mix...](https://arxiv.org/abs/2606.12066v1); [RoadscapesQA: A Multitask, Multimodal Dataset for ...](https://arxiv.org/abs/2602.12877v1); [DriveIndia: An Object Detection Dataset for Divers...](https://arxiv.org/abs/2507.19912v4); [Pedestrian Intention and Trajectory Prediction in ...](https://arxiv.org/abs/2506.22111v1)

## Coverage log per host

`hits` = results returned by the API for that query (GitHub shows returned of total_count); `kept` = passed the per-part relevance regex (before cross-part dedupe and top-N cut). Zero-result queries are kept in the log on purpose.

### github (238 queries)

| part | query | hits | kept | http |
|---|---|---|---|---|
| access_app | バリアフリー マップ [sort=stars] | 2 of 2 | 2 | 200 |
| access_app | 无障碍 地图 [sort=stars] | 9 of 9 | 9 | 200 |
| access_app | accessibility map app [sort=stars] | 30 of 274 | 3 | 200 |
| access_app | accessible navigation app [sort=stars] | 30 of 404 | 4 | 200 |
| access_app | accessmap [sort=stars] | 30 of 147 | 30 | 200 |
| access_app | barrier free map [sort=stars] | 30 of 48 | 28 | 200 |
| access_app | wheelmap [sort=stars] | 30 of 39 | 30 | 200 |
| access_app | accessibility map app [sort=updated] | 30 of 274 | 5 | 200 |
| access_app | accessible navigation app [sort=updated] | 30 of 404 | 9 | 200 |
| audit_tools | accessibility audit [sort=stars] | 30 of 2694 | 0 | 200 |
| audit_tools | built environment audit street view [sort=stars] | 0 of 0 | 0 | 200 |
| audit_tools | sidewalk assessment [sort=stars] | 14 of 14 | 14 | 200 |
| audit_tools | sidewalk audit [sort=stars] | 4 of 4 | 4 | 200 |
| audit_tools | virtual audit street view [sort=stars] | 0 of 0 | 0 | 200 |
| audit_tools | built environment audit street view [sort=updated] | 0 of 0 | 0 | 200 |
| audit_tools | sidewalk audit [sort=updated] | 4 of 4 | 4 | 200 |
| blind_voice | 視覚障害 ナビ [sort=stars] | 0 of 0 | 0 | 200 |
| blind_voice | 盲人 导航 [sort=stars] | 20 of 20 | 19 | 200 |
| blind_voice | audio navigation blind [sort=stars] | 30 of 91 | 30 | 200 |
| blind_voice | blind navigation app [sort=stars] | 30 of 146 | 30 | 200 |
| blind_voice | navigation visually impaired [sort=stars] | 30 of 1566 | 30 | 200 |
| blind_voice | soundscape [sort=stars] | 30 of 3598 | 25 | 200 |
| blind_voice | blind navigation app [sort=updated] | 30 of 146 | 30 | 200 |
| blind_voice | soundscape [sort=updated] | 30 of 3598 | 26 | 200 |
| change_det | 变化检测 [sort=stars] | 30 of 540 | 5 | 200 |
| change_det | scene change detection [sort=stars] | 30 of 197 | 29 | 200 |
| change_det | street view change detection [sort=stars] | 10 of 10 | 10 | 200 |
| change_det | urban change detection street [sort=stars] | 2 of 2 | 2 | 200 |
| change_det | scene change detection [sort=updated] | 30 of 197 | 28 | 200 |
| change_det | street view change detection [sort=updated] | 10 of 10 | 10 | 200 |
| civic | citizen grievance india [sort=stars] | 30 of 38 | 30 | 200 |
| civic | civic issue reporting [sort=stars] | 30 of 4275 | 30 | 200 |
| civic | fixmystreet [sort=stars] | 30 of 178 | 30 | 200 |
| civic | municipal complaint app [sort=stars] | 30 of 53 | 30 | 200 |
| civic | open311 [sort=stars] | 30 of 220 | 30 | 200 |
| civic | pothole reporting app [sort=stars] | 30 of 312 | 30 | 200 |
| civic | swachhata [sort=stars] | 30 of 42 | 30 | 200 |
| civic | civic issue reporting [sort=updated] | 30 of 4275 | 30 | 200 |
| civic | fixmystreet [sort=updated] | 30 of 178 | 30 | 200 |
| curb_ramp | curb cut detection [sort=stars] | 0 of 0 | 0 | 200 |
| curb_ramp | curb detection [sort=stars] | 30 of 78 | 29 | 200 |
| curb_ramp | curb ramp detection [sort=stars] | 3 of 3 | 3 | 200 |
| curb_ramp | kerb ramp [sort=stars] | 1 of 1 | 1 | 200 |
| curb_ramp | project sidewalk [sort=stars] | 30 of 140 | 29 | 200 |
| curb_ramp | curb cut detection [sort=updated] | 0 of 0 | 0 | 200 |
| curb_ramp | curb ramp detection [sort=updated] | 3 of 3 | 3 | 200 |
| deckgl_route | deck.gl animation [sort=stars] | 8 of 8 | 3 | 200 |
| deckgl_route | deck.gl trips layer [sort=stars] | 2 of 2 | 2 | 200 |
| deckgl_route | maplibre 3d [sort=stars] | 30 of 366 | 29 | 200 |
| deckgl_route | maplibre route animation [sort=stars] | 8 of 8 | 8 | 200 |
| deckgl_route | route animation map [sort=stars] | 30 of 108 | 25 | 200 |
| deckgl_route | deck.gl trips layer [sort=updated] | 2 of 2 | 2 | 200 |
| deckgl_route | maplibre route animation [sort=updated] | 8 of 8 | 8 | 200 |
| dehaze_derain | 去雨 去雾 [sort=stars] | 25 of 25 | 24 | 200 |
| dehaze_derain | all-in-one image restoration [sort=stars] | 30 of 118 | 29 | 200 |
| dehaze_derain | image dehazing [sort=stars] | 30 of 1315 | 30 | 200 |
| dehaze_derain | image deraining [sort=stars] | 30 of 294 | 30 | 200 |
| dehaze_derain | image dehazing [sort=updated] | 30 of 1315 | 30 | 200 |
| dehaze_derain | image deraining [sort=updated] | 30 of 294 | 30 | 200 |
| depth | 単眼深度推定 [sort=stars] | 5 of 5 | 4 | 200 |
| depth | curb height estimation [sort=stars] | 0 of 0 | 0 | 200 |
| depth | depth anything [sort=stars] | 30 of 933 | 30 | 200 |
| depth | metric depth estimation [sort=stars] | 30 of 120 | 29 | 200 |
| depth | monocular depth estimation [sort=stars] | 30 of 1556 | 30 | 200 |
| depth | depth anything [sort=updated] | 30 of 933 | 29 | 200 |
| depth | metric depth estimation [sort=updated] | 30 of 120 | 30 | 200 |
| encroachment | 占道经营 检测 [sort=stars] | 8 of 8 | 8 | 200 |
| encroachment | encroachment detection [sort=stars] | 30 of 92 | 21 | 200 |
| encroachment | hawker detection [sort=stars] | 3 of 3 | 3 | 200 |
| encroachment | sidewalk encroachment [sort=stars] | 4 of 4 | 4 | 200 |
| encroachment | street litter detection [sort=stars] | 7 of 7 | 6 | 200 |
| encroachment | street vendor detection [sort=stars] | 9 of 9 | 9 | 200 |
| encroachment | encroachment detection [sort=updated] | 30 of 92 | 24 | 200 |
| encroachment | street vendor detection [sort=updated] | 9 of 9 | 9 | 200 |
| ff3d | dust3r [sort=stars] | 30 of 104 | 30 | 200 |
| ff3d | feed-forward 3d reconstruction [sort=stars] | 30 of 63 | 30 | 200 |
| ff3d | mast3r [sort=stars] | 30 of 179 | 30 | 200 |
| ff3d | pi3 reconstruction [sort=stars] | 5 of 5 | 5 | 200 |
| ff3d | spann3r [sort=stars] | 6 of 6 | 6 | 200 |
| ff3d | vggt [sort=stars] | 30 of 637 | 29 | 200 |
| ff3d | dust3r [sort=updated] | 30 of 104 | 30 | 200 |
| ff3d | vggt [sort=updated] | 30 of 637 | 30 | 200 |
| geoloc_vpr | 视觉位置识别 [sort=stars] | 30 of 72 | 20 | 200 |
| geoloc_vpr | geoclip [sort=stars] | 30 of 66 | 30 | 200 |
| geoloc_vpr | image geolocalization [sort=stars] | 30 of 71 | 30 | 200 |
| geoloc_vpr | street view geolocation [sort=stars] | 30 of 43 | 29 | 200 |
| geoloc_vpr | visual place recognition [sort=stars] | 30 of 288 | 29 | 200 |
| geoloc_vpr | image geolocalization [sort=updated] | 30 of 71 | 30 | 200 |
| geoloc_vpr | visual place recognition [sort=updated] | 30 of 288 | 23 | 200 |
| gs_fewshot | 3dgs [sort=stars] | 30 of 2897 | 29 | 200 |
| gs_fewshot | few-shot gaussian splatting [sort=stars] | 20 of 20 | 20 | 200 |
| gs_fewshot | gaussian splatting [sort=stars] | 30 of 5307 | 30 | 200 |
| gs_fewshot | sparse view gaussian splatting [sort=stars] | 30 of 96 | 30 | 200 |
| gs_fewshot | street gaussian [sort=stars] | 30 of 40 | 30 | 200 |
| gs_fewshot | gaussian splatting [sort=updated] | 30 of 5307 | 29 | 200 |
| gs_fewshot | sparse view gaussian splatting [sort=updated] | 30 of 96 | 30 | 200 |
| india_data | IDD dataset [sort=stars] | 30 of 96 | 24 | 200 |
| india_data | bangalore street [sort=stars] | 30 of 52 | 29 | 200 |
| india_data | india driving dataset [sort=stars] | 30 of 39 | 30 | 200 |
| india_data | india sidewalk [sort=stars] | 1 of 1 | 1 | 200 |
| india_data | indian roads dataset [sort=stars] | 30 of 66 | 30 | 200 |
| india_data | indian street dataset [sort=stars] | 4 of 4 | 4 | 200 |
| india_data | IDD dataset [sort=updated] | 30 of 96 | 19 | 200 |
| india_data | india driving dataset [sort=updated] | 30 of 39 | 30 | 200 |
| inpaint | 图像修复 [sort=stars] | 30 of 219 | 15 | 200 |
| inpaint | image inpainting [sort=stars] | 30 of 2781 | 30 | 200 |
| inpaint | lama inpainting [sort=stars] | 30 of 216 | 30 | 200 |
| inpaint | object removal inpainting [sort=stars] | 30 of 147 | 30 | 200 |
| inpaint | image inpainting [sort=updated] | 30 of 2781 | 30 | 200 |
| inpaint | lama inpainting [sort=updated] | 30 of 216 | 30 | 200 |
| lowlight | 低照度增强 [sort=stars] | 30 of 52 | 14 | 200 |
| lowlight | low light enhancement [sort=stars] | 30 of 2019 | 29 | 200 |
| lowlight | night image enhancement [sort=stars] | 30 of 98 | 29 | 200 |
| lowlight | retinexformer [sort=stars] | 30 of 35 | 30 | 200 |
| lowlight | zero-dce [sort=stars] | 30 of 217 | 30 | 200 |
| lowlight | low light enhancement [sort=updated] | 30 of 2019 | 30 | 200 |
| lowlight | zero-dce [sort=updated] | 30 of 217 | 30 | 200 |
| manhole | マンホール 検出 [sort=stars] | 0 of 0 | 0 | 200 |
| manhole | 井盖 检测 [sort=stars] | 30 of 37 | 29 | 200 |
| manhole | drain cover detection [sort=stars] | 1 of 1 | 0 | 200 |
| manhole | manhole detection [sort=stars] | 30 of 130 | 30 | 200 |
| manhole | open manhole [sort=stars] | 30 of 47 | 30 | 200 |
| manhole | manhole detection [sort=updated] | 30 of 130 | 29 | 200 |
| manhole | open manhole [sort=updated] | 30 of 47 | 30 | 200 |
| map_matching | 地图匹配 [sort=stars] | 30 of 169 | 5 | 200 |
| map_matching | fmm map matching [sort=stars] | 7 of 7 | 7 | 200 |
| map_matching | hidden markov map matching [sort=stars] | 23 of 23 | 22 | 200 |
| map_matching | map matching [sort=stars] | 30 of 1922 | 21 | 200 |
| map_matching | valhalla meili [sort=stars] | 3 of 3 | 3 | 200 |
| map_matching | hidden markov map matching [sort=updated] | 23 of 23 | 22 | 200 |
| map_matching | map matching [sort=updated] | 30 of 1922 | 10 | 200 |
| obstacle | 障害物 検出 歩行 [sort=stars] | 0 of 0 | 0 | 200 |
| obstacle | 盲人 避障 [sort=stars] | 9 of 9 | 9 | 200 |
| obstacle | footpath obstacle [sort=stars] | 4 of 4 | 4 | 200 |
| obstacle | obstacle detection visually impaired [sort=stars] | 30 of 537 | 30 | 200 |
| obstacle | pedestrian obstacle detection [sort=stars] | 30 of 77 | 27 | 200 |
| obstacle | sidewalk obstacle detection [sort=stars] | 14 of 14 | 14 | 200 |
| obstacle | obstacle detection visually impaired [sort=updated] | 30 of 537 | 30 | 200 |
| obstacle | sidewalk obstacle detection [sort=updated] | 14 of 14 | 14 | 200 |
| osm_footway | opensidewalks schema [sort=stars] | 4 of 4 | 4 | 200 |
| osm_footway | openstreetmap footway [sort=stars] | 5 of 5 | 5 | 200 |
| osm_footway | osm sidewalk [sort=stars] | 22 of 22 | 22 | 200 |
| osm_footway | osmnx walk network [sort=stars] | 5 of 5 | 5 | 200 |
| osm_footway | sidewalk osm editor [sort=stars] | 1 of 1 | 1 | 200 |
| osm_footway | openstreetmap footway [sort=updated] | 5 of 5 | 5 | 200 |
| osm_footway | osm sidewalk [sort=updated] | 22 of 22 | 22 | 200 |
| parked_vehicle | 불법주정차 [sort=stars] | 24 of 24 | 24 | 200 |
| parked_vehicle | 违停 检测 [sort=stars] | 25 of 25 | 25 | 200 |
| parked_vehicle | illegal parking detection [sort=stars] | 30 of 109 | 30 | 200 |
| parked_vehicle | parked vehicle detection [sort=stars] | 30 of 64 | 29 | 200 |
| parked_vehicle | sidewalk parking detection [sort=stars] | 1 of 1 | 1 | 200 |
| parked_vehicle | illegal parking detection [sort=updated] | 30 of 109 | 30 | 200 |
| parked_vehicle | sidewalk parking detection [sort=updated] | 1 of 1 | 1 | 200 |
| ped_network | opensidewalks [sort=stars] | 21 of 21 | 21 | 200 |
| ped_network | pedestrian network aerial imagery [sort=stars] | 2 of 2 | 2 | 200 |
| ped_network | sidewalk mapping aerial [sort=stars] | 0 of 0 | 0 | 200 |
| ped_network | sidewalk network extraction [sort=stars] | 1 of 1 | 1 | 200 |
| ped_network | tile2net [sort=stars] | 5 of 5 | 5 | 200 |
| ped_network | sidewalk network extraction [sort=updated] | 1 of 1 | 1 | 200 |
| ped_network | tile2net [sort=updated] | 5 of 5 | 5 | 200 |
| pothole | 坑洼 检测 [sort=stars] | 30 of 62 | 30 | 200 |
| pothole | 포트홀 [sort=stars] | 30 of 31 | 30 | 200 |
| pothole | pothole detection [sort=stars] | 30 of 4594 | 30 | 200 |
| pothole | pothole segmentation [sort=stars] | 30 of 201 | 30 | 200 |
| pothole | pothole yolo [sort=stars] | 30 of 876 | 30 | 200 |
| pothole | pothole detection [sort=updated] | 30 of 4594 | 28 | 200 |
| pothole | pothole yolo [sort=updated] | 30 of 876 | 29 | 200 |
| road_damage | RDD2020 india [sort=stars] | 0 of 0 | 0 | 200 |
| road_damage | RDD2022 [sort=stars] | 30 of 108 | 30 | 200 |
| road_damage | 道路損傷 [sort=stars] | 3 of 3 | 2 | 200 |
| road_damage | 路面 病害 检测 [sort=stars] | 30 of 33 | 30 | 200 |
| road_damage | crackathon [sort=stars] | 30 of 65 | 30 | 200 |
| road_damage | pavement crack detection [sort=stars] | 30 of 102 | 30 | 200 |
| road_damage | road damage detection [sort=stars] | 30 of 1584 | 30 | 200 |
| road_damage | RDD2022 [sort=updated] | 30 of 108 | 30 | 200 |
| road_damage | road damage detection [sort=updated] | 30 of 1584 | 29 | 200 |
| shadow_sun | 阴影检测 [sort=stars] | 30 of 53 | 16 | 200 |
| shadow_sun | shade map [sort=stars] | 30 of 734 | 4 | 200 |
| shadow_sun | shadow detection [sort=stars] | 30 of 938 | 18 | 200 |
| shadow_sun | shadow simulation city [sort=stars] | 4 of 4 | 1 | 200 |
| shadow_sun | sun position [sort=stars] | 30 of 1092 | 14 | 200 |
| shadow_sun | shadow detection [sort=updated] | 30 of 938 | 2 | 200 |
| shadow_sun | sun position [sort=updated] | 30 of 1092 | 15 | 200 |
| sidewalk_seg | 人行道 分割 [sort=stars] | 2 of 2 | 2 | 200 |
| sidewalk_seg | 歩道 セグメンテーション [sort=stars] | 0 of 0 | 0 | 200 |
| sidewalk_seg | footpath segmentation [sort=stars] | 8 of 8 | 8 | 200 |
| sidewalk_seg | pedestrian walkway semantic segmentation [sort=stars] | 0 of 0 | 0 | 200 |
| sidewalk_seg | sidewalk detection deep learning [sort=stars] | 2 of 2 | 2 | 200 |
| sidewalk_seg | sidewalk segmentation [sort=stars] | 30 of 45 | 30 | 200 |
| sidewalk_seg | footpath segmentation [sort=updated] | 8 of 8 | 8 | 200 |
| sidewalk_seg | sidewalk segmentation [sort=updated] | 30 of 45 | 30 | 200 |
| splat_viewer | gaussian splat viewer web [sort=stars] | 30 of 61 | 30 | 200 |
| splat_viewer | spark splat [sort=stars] | 30 of 68 | 29 | 200 |
| splat_viewer | three.js gaussian splat [sort=stars] | 30 of 105 | 28 | 200 |
| splat_viewer | webgl gaussian splatting [sort=stars] | 30 of 81 | 29 | 200 |
| splat_viewer | webgpu splat [sort=stars] | 30 of 86 | 30 | 200 |
| splat_viewer | gaussian splat viewer web [sort=updated] | 30 of 61 | 29 | 200 |
| splat_viewer | webgl gaussian splatting [sort=updated] | 30 of 81 | 30 | 200 |
| stairs | 楼梯 检测 [sort=stars] | 9 of 9 | 9 | 200 |
| stairs | 階段 検出 [sort=stars] | 0 of 0 | 0 | 200 |
| stairs | staircase detection [sort=stars] | 30 of 55 | 28 | 200 |
| stairs | stairs detection [sort=stars] | 30 of 52 | 29 | 200 |
| stairs | step detection visually impaired [sort=stars] | 12 of 12 | 0 | 200 |
| stairs | staircase detection [sort=updated] | 30 of 55 | 29 | 200 |
| stairs | stairs detection [sort=updated] | 30 of 52 | 29 | 200 |
| sv_download | 街景 下载 [sort=stars] | 5 of 5 | 5 | 200 |
| sv_download | google street view download [sort=stars] | 30 of 49 | 30 | 200 |
| sv_download | kartaview [sort=stars] | 12 of 12 | 12 | 200 |
| sv_download | mapillary download [sort=stars] | 27 of 27 | 27 | 200 |
| sv_download | street view imagery python [sort=stars] | 13 of 13 | 9 | 200 |
| sv_download | streetview downloader [sort=stars] | 21 of 21 | 21 | 200 |
| sv_download | zensvi [sort=stars] | 6 of 6 | 6 | 200 |
| sv_download | google street view download [sort=updated] | 30 of 49 | 30 | 200 |
| sv_download | mapillary download [sort=updated] | 27 of 27 | 27 | 200 |
| tactile | 점자블록 [sort=stars] | 12 of 12 | 12 | 200 |
| tactile | 盲道 检测 [sort=stars] | 30 of 43 | 30 | 200 |
| tactile | 点字ブロック [sort=stars] | 1 of 1 | 1 | 200 |
| tactile | blind path detection [sort=stars] | 30 of 35 | 30 | 200 |
| tactile | tactile paving detection [sort=stars] | 4 of 4 | 4 | 200 |
| tactile | tactile paving [sort=stars] | 30 of 31 | 30 | 200 |
| tactile | tactile paving detection [sort=updated] | 4 of 4 | 4 | 200 |
| tactile | tactile paving [sort=updated] | 30 of 31 | 30 | 200 |
| walkability | 步行性 [sort=stars] | 30 of 705 | 0 | 200 |
| walkability | pedestrian level of service [sort=stars] | 6 of 6 | 3 | 200 |
| walkability | street walkability [sort=stars] | 30 of 249 | 8 | 200 |
| walkability | walkability index [sort=stars] | 30 of 182 | 11 | 200 |
| walkability | walkability score [sort=stars] | 30 of 450 | 11 | 200 |
| walkability | walkability index [sort=updated] | 30 of 182 | 6 | 200 |
| walkability | walkability score [sort=updated] | 30 of 450 | 7 | 200 |
| wheelchair_routing | 車椅子 ナビ [sort=stars] | 0 of 0 | 0 | 200 |
| wheelchair_routing | 휠체어 경로 [sort=stars] | 1 of 1 | 1 | 200 |
| wheelchair_routing | 轮椅 导航 [sort=stars] | 5 of 5 | 5 | 200 |
| wheelchair_routing | accessible routing [sort=stars] | 30 of 1259 | 0 | 200 |
| wheelchair_routing | barrier free routing [sort=stars] | 18 of 18 | 15 | 200 |
| wheelchair_routing | wheelchair navigation [sort=stars] | 30 of 178 | 30 | 200 |
| wheelchair_routing | wheelchair routing [sort=stars] | 30 of 68 | 30 | 200 |
| wheelchair_routing | wheelchair navigation [sort=updated] | 30 of 178 | 30 | 200 |
| wheelchair_routing | wheelchair routing [sort=updated] | 30 of 68 | 30 | 200 |

### huggingface (180 queries)

| part | query | hits | kept | http |
|---|---|---|---|---|
| access_app | accessibility navigation [datasets] | 0 | 0 | 200 |
| access_app | accessibility navigation [models] | 0 | 0 | 200 |
| access_app | accessibility navigation [spaces] | 0 | 0 | 200 |
| audit_tools | sidewalk accessibility [datasets] | 0 | 0 | 200 |
| audit_tools | sidewalk accessibility [models] | 0 | 0 | 200 |
| audit_tools | sidewalk accessibility [spaces] | 0 | 0 | 200 |
| blind_voice | blind navigation [datasets] | 1 | 1 | 200 |
| blind_voice | visually impaired [datasets] | 3 | 3 | 200 |
| blind_voice | blind navigation [models] | 0 | 0 | 200 |
| blind_voice | visually impaired [models] | 1 | 1 | 200 |
| blind_voice | blind navigation [spaces] | 3 | 3 | 200 |
| blind_voice | visually impaired [spaces] | 8 | 8 | 200 |
| change_det | change detection [datasets] | 21 | 20 | 200 |
| change_det | change detection [models] | 22 | 21 | 200 |
| change_det | change detection [spaces] | 25 | 24 | 200 |
| civic | civic issue [datasets] | 1 | 1 | 200 |
| civic | civic issue [models] | 1 | 1 | 200 |
| civic | civic issue [spaces] | 11 | 11 | 200 |
| curb_ramp | curb [datasets] | 13 | 13 | 200 |
| curb_ramp | curb ramp [datasets] | 1 | 1 | 200 |
| curb_ramp | project sidewalk [datasets] | 14 | 14 | 200 |
| curb_ramp | curb [models] | 21 | 20 | 200 |
| curb_ramp | curb ramp [models] | 4 | 4 | 200 |
| curb_ramp | project sidewalk [models] | 17 | 17 | 200 |
| curb_ramp | curb [spaces] | 13 | 13 | 200 |
| curb_ramp | curb ramp [spaces] | 0 | 0 | 200 |
| curb_ramp | project sidewalk [spaces] | 0 | 0 | 200 |
| dehaze_derain | dehaze [datasets] | 3 | 3 | 200 |
| dehaze_derain | derain [datasets] | 6 | 6 | 200 |
| dehaze_derain | image restoration [datasets] | 10 | 10 | 200 |
| dehaze_derain | dehaze [models] | 15 | 15 | 200 |
| dehaze_derain | derain [models] | 28 | 28 | 200 |
| dehaze_derain | image restoration [models] | 12 | 12 | 200 |
| dehaze_derain | dehaze [spaces] | 16 | 16 | 200 |
| dehaze_derain | derain [spaces] | 13 | 13 | 200 |
| dehaze_derain | image restoration [spaces] | 50 | 50 | 200 |
| depth | depth-anything [datasets] | 16 | 16 | 200 |
| depth | depth estimation [datasets] | 7 | 6 | 200 |
| depth | metric3d [datasets] | 0 | 0 | 200 |
| depth | depth-anything [models] | 50 | 50 | 200 |
| depth | depth estimation [models] | 16 | 16 | 200 |
| depth | metric3d [models] | 19 | 8 | 200 |
| depth | depth-anything [spaces] | 50 | 50 | 200 |
| depth | depth estimation [spaces] | 50 | 50 | 200 |
| depth | metric3d [spaces] | 9 | 0 | 200 |
| encroachment | encroachment [datasets] | 0 | 0 | 200 |
| encroachment | street vendor [datasets] | 0 | 0 | 200 |
| encroachment | encroachment [models] | 0 | 0 | 200 |
| encroachment | street vendor [models] | 0 | 0 | 200 |
| encroachment | encroachment [spaces] | 0 | 0 | 200 |
| encroachment | street vendor [spaces] | 0 | 0 | 200 |
| ff3d | dust3r [datasets] | 6 | 6 | 200 |
| ff3d | mast3r [datasets] | 5 | 5 | 200 |
| ff3d | vggt [datasets] | 50 | 50 | 200 |
| ff3d | dust3r [models] | 19 | 19 | 200 |
| ff3d | mast3r [models] | 15 | 15 | 200 |
| ff3d | vggt [models] | 50 | 48 | 200 |
| ff3d | dust3r [spaces] | 11 | 11 | 200 |
| ff3d | mast3r [spaces] | 8 | 8 | 200 |
| ff3d | vggt [spaces] | 28 | 27 | 200 |
| geoloc_vpr | geoclip [datasets] | 4 | 3 | 200 |
| geoloc_vpr | geolocation [datasets] | 8 | 8 | 200 |
| geoloc_vpr | visual place recognition [datasets] | 0 | 0 | 200 |
| geoloc_vpr | geoclip [models] | 24 | 24 | 200 |
| geoloc_vpr | geolocation [models] | 19 | 18 | 200 |
| geoloc_vpr | visual place recognition [models] | 0 | 0 | 200 |
| geoloc_vpr | geoclip [spaces] | 2 | 2 | 200 |
| geoloc_vpr | geolocation [spaces] | 25 | 23 | 200 |
| geoloc_vpr | visual place recognition [spaces] | 2 | 0 | 200 |
| gs_fewshot | gaussian splatting [datasets] | 19 | 19 | 200 |
| gs_fewshot | splat [datasets] | 50 | 50 | 200 |
| gs_fewshot | gaussian splatting [models] | 13 | 13 | 200 |
| gs_fewshot | splat [models] | 50 | 50 | 200 |
| gs_fewshot | gaussian splatting [spaces] | 4 | 4 | 200 |
| gs_fewshot | splat [spaces] | 50 | 50 | 200 |
| india_data | idd [datasets] | 22 | 10 | 200 |
| india_data | india road [datasets] | 0 | 0 | 200 |
| india_data | indian driving [datasets] | 2 | 2 | 200 |
| india_data | idd [models] | 50 | 18 | 200 |
| india_data | india road [models] | 2 | 2 | 200 |
| india_data | indian driving [models] | 0 | 0 | 200 |
| india_data | idd [spaces] | 48 | 6 | 200 |
| india_data | india road [spaces] | 3 | 3 | 200 |
| india_data | indian driving [spaces] | 0 | 0 | 200 |
| inpaint | inpainting [datasets] | 50 | 50 | 200 |
| inpaint | lama [datasets] | 50 | 50 | 200 |
| inpaint | inpainting [models] | 50 | 50 | 200 |
| inpaint | lama [models] | 50 | 49 | 200 |
| inpaint | inpainting [spaces] | 50 | 50 | 200 |
| inpaint | lama [spaces] | 50 | 50 | 200 |
| lowlight | low-light [datasets] | 22 | 21 | 200 |
| lowlight | low light enhancement [datasets] | 0 | 0 | 200 |
| lowlight | low-light [models] | 50 | 40 | 200 |
| lowlight | low light enhancement [models] | 3 | 3 | 200 |
| lowlight | low-light [spaces] | 50 | 50 | 200 |
| lowlight | low light enhancement [spaces] | 15 | 15 | 200 |
| manhole | manhole [datasets] | 4 | 4 | 200 |
| manhole | manhole [models] | 4 | 4 | 200 |
| manhole | manhole [spaces] | 13 | 13 | 200 |
| map_matching | map matching [datasets] | 1 | 1 | 200 |
| map_matching | map matching [models] | 0 | 0 | 200 |
| map_matching | map matching [spaces] | 0 | 0 | 200 |
| obstacle | obstacle detection [datasets] | 11 | 11 | 200 |
| obstacle | sidewalk obstacle [datasets] | 1 | 1 | 200 |
| obstacle | obstacle detection [models] | 7 | 7 | 200 |
| obstacle | sidewalk obstacle [models] | 3 | 3 | 200 |
| obstacle | obstacle detection [spaces] | 11 | 11 | 200 |
| obstacle | sidewalk obstacle [spaces] | 0 | 0 | 200 |
| osm_footway | openstreetmap [datasets] | 28 | 26 | 200 |
| osm_footway | openstreetmap [models] | 0 | 0 | 200 |
| osm_footway | openstreetmap [spaces] | 2 | 2 | 200 |
| parked_vehicle | illegal parking [datasets] | 1 | 1 | 200 |
| parked_vehicle | parked vehicle [datasets] | 0 | 0 | 200 |
| parked_vehicle | illegal parking [models] | 1 | 1 | 200 |
| parked_vehicle | parked vehicle [models] | 0 | 0 | 200 |
| parked_vehicle | illegal parking [spaces] | 3 | 3 | 200 |
| parked_vehicle | parked vehicle [spaces] | 0 | 0 | 200 |
| ped_network | sidewalk aerial [datasets] | 0 | 0 | 200 |
| ped_network | tile2net [datasets] | 0 | 0 | 200 |
| ped_network | sidewalk aerial [models] | 0 | 0 | 200 |
| ped_network | tile2net [models] | 1 | 1 | 200 |
| ped_network | sidewalk aerial [spaces] | 0 | 0 | 200 |
| ped_network | tile2net [spaces] | 0 | 0 | 200 |
| pothole | pothole [datasets] | 36 | 36 | 200 |
| pothole | pothole [models] | 50 | 50 | 200 |
| pothole | pothole [spaces] | 50 | 48 | 200 |
| road_damage | pavement crack [datasets] | 0 | 0 | 200 |
| road_damage | rdd2022 [datasets] | 5 | 5 | 200 |
| road_damage | road damage [datasets] | 13 | 13 | 200 |
| road_damage | pavement crack [models] | 1 | 1 | 200 |
| road_damage | rdd2022 [models] | 13 | 13 | 200 |
| road_damage | road damage [models] | 22 | 22 | 200 |
| road_damage | pavement crack [spaces] | 3 | 3 | 200 |
| road_damage | rdd2022 [spaces] | 0 | 0 | 200 |
| road_damage | road damage [spaces] | 50 | 50 | 200 |
| shadow_sun | shadow detection [datasets] | 1 | 1 | 200 |
| shadow_sun | shadow removal [datasets] | 0 | 0 | 200 |
| shadow_sun | shadow detection [models] | 3 | 1 | 200 |
| shadow_sun | shadow removal [models] | 2 | 2 | 200 |
| shadow_sun | shadow detection [spaces] | 0 | 0 | 200 |
| shadow_sun | shadow removal [spaces] | 1 | 1 | 200 |
| sidewalk_seg | footpath segmentation [datasets] | 1 | 1 | 200 |
| sidewalk_seg | mapillary vistas [datasets] | 8 | 3 | 200 |
| sidewalk_seg | segformer cityscapes [datasets] | 0 | 0 | 200 |
| sidewalk_seg | sidewalk [datasets] | 50 | 50 | 200 |
| sidewalk_seg | footpath segmentation [models] | 0 | 0 | 200 |
| sidewalk_seg | mapillary vistas [models] | 2 | 2 | 200 |
| sidewalk_seg | segformer cityscapes [models] | 50 | 42 | 200 |
| sidewalk_seg | sidewalk [models] | 50 | 50 | 200 |
| sidewalk_seg | footpath segmentation [spaces] | 0 | 0 | 200 |
| sidewalk_seg | mapillary vistas [spaces] | 1 | 0 | 200 |
| sidewalk_seg | segformer cityscapes [spaces] | 6 | 0 | 200 |
| sidewalk_seg | sidewalk [spaces] | 24 | 24 | 200 |
| splat_viewer | splat viewer [datasets] | 0 | 0 | 200 |
| splat_viewer | splat viewer [models] | 1 | 1 | 200 |
| splat_viewer | splat viewer [spaces] | 3 | 3 | 200 |
| stairs | staircase [datasets] | 1 | 0 | 200 |
| stairs | stairs [datasets] | 7 | 6 | 200 |
| stairs | staircase [models] | 17 | 12 | 200 |
| stairs | stairs [models] | 11 | 11 | 200 |
| stairs | staircase [spaces] | 3 | 3 | 200 |
| stairs | stairs [spaces] | 3 | 3 | 200 |
| sv_download | mapillary [datasets] | 24 | 24 | 200 |
| sv_download | street view [datasets] | 50 | 44 | 200 |
| sv_download | mapillary [models] | 3 | 3 | 200 |
| sv_download | street view [models] | 29 | 23 | 200 |
| sv_download | mapillary [spaces] | 2 | 2 | 200 |
| sv_download | street view [spaces] | 16 | 10 | 200 |
| tactile | blind road [datasets] | 0 | 0 | 200 |
| tactile | tactile paving [datasets] | 1 | 1 | 200 |
| tactile | blind road [models] | 0 | 0 | 200 |
| tactile | tactile paving [models] | 0 | 0 | 200 |
| tactile | blind road [spaces] | 0 | 0 | 200 |
| tactile | tactile paving [spaces] | 0 | 0 | 200 |
| walkability | walkability [datasets] | 1 | 1 | 200 |
| walkability | walkability [models] | 2 | 2 | 200 |
| walkability | walkability [spaces] | 2 | 2 | 200 |
| wheelchair_routing | wheelchair [datasets] | 4 | 4 | 200 |
| wheelchair_routing | wheelchair [models] | 7 | 7 | 200 |
| wheelchair_routing | wheelchair [spaces] | 4 | 4 | 200 |

### arxiv (55 queries)

| part | query | hits | kept | http |
|---|---|---|---|---|
| access_app | accessible navigation app mobility impairment | 6 | 0 | 200 |
| audit_tools | built environment audit street view | 3 | 2 | 200 |
| audit_tools | sidewalk accessibility audit | 2 | 2 | 200 |
| blind_voice | audio augmented reality blind | 11 | 11 | 200 |
| blind_voice | navigation visually impaired | 50 | 49 | 200 |
| change_det | scene change detection | 50 | 48 | 200 |
| change_det | street-view change detection | 18 | 15 | 200 |
| civic | civic issue reporting crowdsourcing | 1 | 1 | 200 |
| curb_ramp | curb cut street view | 0 | 0 | 200 |
| curb_ramp | curb ramp detection | 4 | 1 | 200 |
| dehaze_derain | image dehazing | 50 | 50 | 200 |
| dehaze_derain | image deraining | 50 | 50 | 200 |
| depth | curb height estimation | 4 | 2 | 200 |
| depth | monocular metric depth | 50 | 49 | 200 |
| encroachment | sidewalk encroachment | 0 | 0 | 200 |
| encroachment | street vendor detection | 1 | 1 | 200 |
| ff3d | feed-forward 3D reconstruction | 50 | 50 | 200 |
| ff3d | pointmap reconstruction | 50 | 44 | 200 |
| geoloc_vpr | image geolocalization street view | 30 | 27 | 200 |
| geoloc_vpr | visual place recognition | 50 | 48 | 200 |
| gs_fewshot | sparse view gaussian splatting | 50 | 50 | 200 |
| gs_fewshot | street scene gaussian splatting | 36 | 28 | 200 |
| india_data | India pedestrian infrastructure | 1 | 1 | 200 |
| india_data | India street images dataset | 4 | 2 | 200 |
| india_data | Indian driving dataset | 24 | 13 | 200 |
| inpaint | image inpainting object removal | 50 | 50 | 200 |
| lowlight | low-light image enhancement | 50 | 50 | 200 |
| manhole | manhole detection | 11 | 5 | 200 |
| manhole | open manhole | 0 | 0 | 200 |
| map_matching | map matching | 50 | 27 | 200 |
| map_matching | matching detections to road segments | 0 | 0 | 200 |
| obstacle | obstacle detection blind pedestrian | 2 | 2 | 200 |
| obstacle | sidewalk obstacle detection | 4 | 4 | 200 |
| osm_footway | OpenStreetMap sidewalk completeness | 1 | 1 | 200 |
| parked_vehicle | illegal parking detection | 10 | 9 | 200 |
| parked_vehicle | sidewalk parking | 12 | 6 | 200 |
| ped_network | pedestrian network extraction aerial imagery | 2 | 2 | 200 |
| ped_network | sidewalk network generation | 22 | 16 | 200 |
| pothole | pothole detection | 50 | 48 | 200 |
| road_damage | RDD2022 road damage | 3 | 3 | 200 |
| road_damage | pavement distress detection | 24 | 24 | 200 |
| road_damage | road damage detection India | 6 | 6 | 200 |
| shadow_sun | shadow detection | 50 | 44 | 200 |
| shadow_sun | street shade pedestrian | 2 | 1 | 200 |
| sidewalk_seg | footpath segmentation street view | 0 | 0 | 200 |
| sidewalk_seg | sidewalk segmentation | 39 | 33 | 200 |
| stairs | stair detection | 46 | 26 | 200 |
| stairs | staircase detection | 50 | 27 | 200 |
| sv_download | street view imagery toolkit | 1 | 1 | 200 |
| tactile | blind road segmentation | 11 | 7 | 200 |
| tactile | tactile paving detection | 7 | 6 | 200 |
| walkability | walkability index | 9 | 5 | 200 |
| walkability | walkability street view | 9 | 6 | 200 |
| wheelchair_routing | accessible pedestrian routing | 8 | 3 | 200 |
| wheelchair_routing | wheelchair routing | 13 | 10 | 200 |

### github-code (5 queries)

| part | query | hits | kept | http |
|---|---|---|---|---|
| CODE | "project sidewalk" api labels | 50 of 371 | 3 | 200 |
| CODE | "surface" "incline" "kerb" routing footway | 50 of 818 | 34 | 200 |
| CODE | curb_ramp sidewalk filename:labels | 4 of 4 | 3 | 200 |
| CODE | opensidewalks | 50 of 1146 | 11 | 200 |
| CODE | wheelchair costing valhalla | 50 of 1656 | 34 | 200 |

### gitee

API `https://gitee.com/api/v5/search/repositories` not reachable: DNS resolution failure for gitee.com (curl exit 6, python Errno -3), tested 16:21 and 16:23 IST, sandboxed and unsandboxed. 1 query attempted and logged in harvest.log, rest skipped. Replacement: Parallel web_search `search_46df0f5ee37831c55acf2bf16e175284` (5 Chinese queries), 4 Gitee repos kept.

### parallel web_search (Kaggle, Gitee, gov, papers)

| search_id | objective | kept |
|---|---|---|
| search_ca7e3f06227c7acb52f3153569c04a4f | Kaggle India pothole/footpath/manhole/RDD/encroachment | 9 |
| search_5fd889f8ed666ea75b4a85109039ec60 | Indian civic reporting apps (Swachhata, ICMyC, Sugamya Bharat) | 5 |
| search_46df0f5ee37831c55acf2bf16e175284 | Gitee 盲道/井盖/占道经营/无障碍/人行道 | 10 |
| search_99258614030acb8cb8a2aa1533ad8a04 | Project Sidewalk India + ML repos | 6 |
| search_cb45abcf1a473e8ae504b9505b1bc50c | JP/KR/CN barrier-free route apps and open data | 5 |
| search_7ccd45d9a3d97db19623cf27800f19b3 | 2025-26 VLM sidewalk accessibility research code | 8 |
| search_4d595b42ed19be39dfde52a4c63d4f90 | OpenSidewalks/TDEI/AccessMap + wheelchair routing engines | 4 |
| search_395d9a9b5f4e1cefa33905bad3691455 | India street datasets beyond IDD | 2 |
| search_d27193d9c07b4fec74361be8200bbe88 | Soundscape successors + Indian blind nav | 5 |
| search_89c7d51a84d3cb8584560622ac948443 | geolocating detections from multiple panos, Mapillary map features | 4 |
| search_2da5ec9b33edb03b460012a80d15074f | Indian walkability / safety audit tools | 4 |

