# SC-02 image sources, raw research log (Indian street / footpath imagery)

Date: 2026-10-24. Scope: online sources of Indian street and footpath images for "accessible walking routes from street imagery, all of India". Google Street View excluded.
Method: Parallel search MCP first, then primary pages, then `curl` (HEAD, Range GET, public JSON APIs of Zenodo, figshare, Kaggle, Mendeley, GitHub, OpenCity CKAN).

Tags:
- **VERIFIED** = seen on the primary page, or returned by the host's own API / HTTP response today.
- **UNVERIFIED** = from a secondary source, a search excerpt only, or inferred.
- Byte counts are exact API values. "GB" = 10^9 bytes.

---

## 0. Ranking for SC-02 (quick view)

| rank | source | why it matters for walking routes | access friction |
|---|---|---|---|
| 1 | IDD Segmentation (IDD 20k) | pixel classes `sidewalk`, `curb`, `non-drivable fallback`; Hyderabad + Bengaluru | free login, licence shown at download |
| 2 | Indian Footpath Damage Segmentation (Zenodo 17154852) | only India footpath-surface masks found; Pune; CC BY 4.0 | none, direct URL |
| 3 | e-Yantra "Semantic Segmentation datasets of Indian roads" (Kaggle) | `footpath`, `road`, `pothole`, `shallow` masks at knee height | Kaggle login; GPL 2 |
| 4 | IDD-AW | rain, fog, low light, snow; same IDD label tree | free login |
| 5 | RDD2022 India | 9,665 road images, potholes and cracks; Delhi, Gurugram, Haryana | none (figshare); per-country S3 zip is dead |
| 6 | Mapillary API (India coverage) | live street-level photos, CC BY-SA; detections include manholes, curbs | free access token |
| 7 | IRDID (GitHub) | open-manhole class, 200 images | none, but images scraped from news/stock sites, licence claim not safe |

---

## 1. IDD family (IIIT Hyderabad, INSAAN)

Source pages: https://insaan.iiit.ac.in/datasets , https://insaan.iiit.ac.in/ , https://idd.insaan.iiit.ac.in/dataset/details , label code https://github.com/AutoNUE/public-code/blob/master/helpers/anue_labels.py

Download entry point for every item: `https://idd.insaan.iiit.ac.in/dataset/download/` . `curl -sIL` returns `HTTP/1.1 302 Found`, `Location: /accounts/login/?next=/dataset/download/` (VERIFIED). So no direct file URLs are published; files are behind a free account.

Licence: login page says "License will be displayed before downloading a dataset." (VERIFIED, https://idd.insaan.iiit.ac.in/accounts/login). Exact licence text not visible without an account (UNVERIFIED). A third-party repo calls it a non-commercial "Indian Driving Dataset Research Use License" (UNVERIFIED, https://github.com/sushant-mishra-dtu/ADAS/blob/main/DATASET_LICENSE.md). NCVPRIPG 2019 page: "open dataset, available for anyone across the world, for research" (VERIFIED, https://cvit.iiit.ac.in/ncvpripg19/idd-challenge).

| item | size (as listed) | images / content | cities | conditions | footpath-relevant classes | tag |
|---|---|---|---|---|---|---|
| IDD Segmentation (IDD 20k Part I) | 18.5 GB | 10,003 images (6,993 train / 981 val / 2,029 test), 182 drive sequences, mostly 1080p | Hyderabad, Bengaluru and outskirts | daytime driving (no weather split stated) | `sidewalk` (level3Id 2, level2 non-drivable), `curb` (level3Id 13, barrier), `non-drivable fallback`, `drivable fallback`, `parking`, `person`, `pole`, `billboard` | sizes, counts, cities VERIFIED (insaan + dataset/details); classes VERIFIED in anue_labels.py |
| IDD Segmentation (IDD 20k Part II) | 5.5 GB | with Part I: 20,000 images (14K train / 2K val / 4K test) from 350 drive sequences | not stated on page | not stated | same label set | VERIFIED (insaan datasets page) |
| IDD Detection | 22.8 GB | 46,588 images (31,569 / 10,225 / 4,794), boxes | Hyderabad, Bengaluru | not stated | boxes only: person, rider, vehicles, animal, traffic sign/light. No sidewalk | VERIFIED |
| IDD 117k | 72 GB | IDD-Detection + IDD-95K-Detection (65,328 / 9,977 / 19,850) | not stated | not stated | boxes only | VERIFIED (added Nov 05, 2024) |
| IDD Lite | 26.9 MB | subsampled IDD, 7 level-1 classes, 256x128 masks | Hyderabad, Bengaluru | - | no separate sidewalk: `sidewalk` folds into level1 "non-drivable" (level1Id 1 in anue_labels.py) | size VERIFIED (insaan); 7 classes VERIFIED (NCVPRIPG page); fold-in VERIFIED from code |
| IDD Temporal | 7 parts: 23.7 + 21.1 + 14.2 + 12.1 + 9.6 (val) + 10.8 + 7.8 GB = 99.3 GB | +-15 neighbour frames around IDD seg/det frames (unlabelled context) | as IDD | as IDD | no new labels | sizes VERIFIED, sum computed |
| IDD Multimodal | 6.5 + 6.6 + 3.0 GB | stereo 15 fps, GPS 15 Hz, 16-ch LiDAR, OBD | Hyderabad, Bengaluru (UNVERIFIED for this part) | - | none | VERIFIED |
| IDD-3D | 236 GiB | multi-camera + LiDAR, ~223k 3D boxes, 17 categories, 5+ hours | Hyderabad | various | no sidewalk class | VERIFIED (insaan + https://idd3d.github.io/) |
| IDD-PeD (pedestrian intention, 2025) | 46 GB | annotated video, 650K+ boxes; labels include pedestrian, crosswalk, bus station, pedestrian traffic light | India (city UNVERIFIED) | illumination changes, occlusion | crosswalk, pedestrian behaviour | size from https://india-data.org/dataset-details/08c7609a-565b-4f85-90e6-77589c0b882c (VERIFIED in excerpt); login need UNVERIFIED; repo https://github.com/Ruthvik9/IDD-PeD |
| I2WDD, IDD-X, MTSVD, FGVD | 19.4 / 160 / 138 / 2.6 GB | driving video / fine-grained vehicles | - | - | not footpath-relevant | VERIFIED sizes |

Answer to "does a sidewalk class exist?": yes. `sidewalk` is a level-3/level-4 label in IDD segmentation (and `curb` too). In IDD-Lite it is merged into "non-drivable". VERIFIED.

---

## 2. IDD-AW (adverse weather)

| field | value | tag |
|---|---|---|
| paper | Shaik et al., WACV 2024, pp. 4614-4623. open access on thecvf.com (WACV 2024 repository, entry "Shaik_IDD-AW"); PDF: https://iddaw.github.io/static/pdfs/IDDAW_WACV24_final.pdf ; DOI 10.1109/WACV57701.2024.00455 | VERIFIED |
| project page | https://iddaw.github.io/ | VERIFIED |
| download | `https://idd.insaan.iiit.ac.in/dataset/download/` (login, "24 hour token" per competition instructions). Test images: https://tinyurl.com/iddawtest (not resolved by me) | download route VERIFIED; tinyurl target UNVERIFIED |
| size | 19 GB | VERIFIED (insaan) |
| images | 5,000 RGB + paired NIR (JAI FS-3200D-10GE camera): 1,500 rain, 1,500 fog, 1,000 low light, 1,000 snow | VERIFIED (https://mobility.iiit.ac.in/iddaw_blog.php, safe-seg-24 dataset page) |
| labels | pixel-level semantic + instance; 4-level hierarchy, 7 labels at level 1, 30 at level 4 | VERIFIED |
| sidewalk / curb in IDD-AW | expected via the shared IDD level-4 tree | UNVERIFIED (not checked in IDD-AW files) |
| cities | "various states and terrains of India, from the highways of Hyderabad to the snowy hills of Manali" | VERIFIED (blog); full city list UNVERIFIED |
| registration | yes (same IDD account) | VERIFIED |
| licence | shown at download; ICPR 2024 page says data "will be made publicly available post-competition in accordance with ICPR guidelines" | UNVERIFIED exact text |

---

## 3. RDD2022 India subset

| field | value | tag |
|---|---|---|
| figshare record | https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547 , DOI 10.6084/m9.figshare.21431547 | VERIFIED |
| full zip | `RDD2022_released_through_CRDDC2022.zip`, https://ndownloader.figshare.com/files/38030910 , **13,264,172,619 bytes** (page shows "Download all (12.36 GB)") | VERIFIED via `api.figshare.com/v2/articles/21431547`; ndownloader returns 302 to a 10-second signed S3 URL |
| India-only zip | https://bigdatacup.s3.ap-northeast-1.amazonaws.com/2022/CRDDC2022/RDD2022/Country_Specific_Data_CRDDC2022/RDD2022_India.zip , README says "502.3 MB - train and test" | size VERIFIED in README; **URL returns HTTP 403 today (2026-10-24)**, both HEAD and Range GET, so treat as dead. Same 403 for the all-country `RDD2022.zip` S3 link |
| India image count | **9,665** `India_*.jpg` (7,706 train with XML + 1,959 test) | VERIFIED by counting `File_List_CRDDC_RDD2022.txt` (https://ndownloader.figshare.com/files/38030826, 3,250,534 bytes); matches arXiv 2209.08538 table (7706 / 1959 / 9665) |
| India annotations | 6,831 train labels (paper table) | UNVERIFIED (paper excerpt only) |
| cities | Delhi, Gurugram (metro) + non-metro Haryana; local roads, state and national highways, plain areas | VERIFIED (Wiley GDJ data article, https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/gdj3.260) |
| capture | vehicle-mounted smartphone | VERIFIED (Dataset Ninja summary; paper) |
| classes | challenge uses D00 longitudinal, D10 transverse, D20 alligator crack, D40 pothole; "data includes annotations for multiple categories" | VERIFIED (https://crddc2022.sekilab.global/data/) |
| manhole class | not among the 4 challenge classes; whether XMLs carry a manhole code | UNVERIFIED |
| footpath / sidewalk | none (road surface only) | VERIFIED |
| conditions | not described | - |
| licence | CC BY 4.0 (figshare API `license: CC BY 4.0`); GitHub repo code MIT | VERIFIED |
| registration | none for figshare | VERIFIED |
| other copies | RDD2020 on Mendeley https://data.mendeley.com/datasets/5ty2wb6gvg/1 (India, Japan, Czech; 26,336 images). Old S3 `train.tar.gz` (RDD2020) HEAD timed out today | Mendeley VERIFIED in excerpt; S3 UNVERIFIED |

---

## 4. "IRDID" and other datasets with open manholes

| name | URL | images | classes | licence | registration | notes | tag |
|---|---|---|---|---|---|---|---|
| **IRDID, Indian Road Damage & Infrastructure Dataset** | https://github.com/ahs695/Indian-Road-Damage-Infrastructure-Dataset (created 2026-03-11, 14 commits) | 1,200 (200 per class), split 840/180/180 | pothole, crack, **open manhole**, waterlogged road, broken road edge, construction zone (image-level labels in `annotations/labels.csv`, no boxes) | LICENSE file says CC BY 4.0 | none (git clone) | **licence risk**: `metadata/dataset_metadata.csv` `source` column, counted by me: Google creative commons 300, Google Maps 206, Google Images 94, YouTube 71, NDTV 48, The Hindu 43, India Today 26, TOI 24, Getty 20, Alamy 14, Shutterstock 12, Dreamstime 12, iStock 5, ... So most images are third-party copyrighted; the CC BY claim cannot cover them. Google Maps share also clashes with the GSV exclusion | VERIFIED (README, LICENSE, metadata counted) |
| RAD (Road Anomaly Detection), Kaggle | https://www.kaggle.com/datasets/rohitsuresh15/radroad-anomaly-detection | 11,800 images + raw videos, 371 road scenarios | LMV, HMV, Road Damages (potholes, cracks, protrusions, **manholes** merged in one class), unsurfaced road, pedestrians, speed bumps | MIT (Kaggle metadata) | Kaggle login to download | 7,852,662,180 bytes; updated 2023-11-28; paper https://link.springer.com/chapter/10.1007/978-981-97-2004-0_34 ; cities not stated | VERIFIED via Kaggle API |
| N-RDD2024 (Mendeley) | https://data.mendeley.com/datasets/27c8pwsd6v/4 , DOI 10.17632/27c8pwsd6v.4 | re-labelled RDD2022 subset (India share UNVERIFIED) | 10 classes incl. D70 **manhole covers**, D50 pedestrian crossing blur | not read | none | API JSON was too large and truncated | partly VERIFIED (excerpt) |
| Road Damage Dataset: Potholes, Cracks and Manholes (Sci Rep 2026) | https://www.kaggle.com/datasets/lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes | 2,009 | pothole, crack, manhole | CC BY 4.0, "no registration" | none (Zenodo) | **Rome and Sacrofano, Italy, not India.** Only useful for manhole appearance | VERIFIED (PMC13181123) |

Search terms used: "Indian road damage dataset manhole", "IRDID Indian road damage image dataset", "open manhole detection dataset India", "Indian road anomalies dataset potholes manholes speed breakers".

---

## 5. Pune footpath damage segmentation (Zenodo)

| field | value | tag |
|---|---|---|
| title | Indian Footpath Damage Segmentation Dataset (creator Priti Chakurkar) | VERIFIED |
| Zenodo records | v1 **15414238** (2025-05-14), newer **17154852** (2025-09-18, "latest") | VERIFIED via `zenodo.org/api/records/.../versions` |
| DOIs | 10.5281/zenodo.15414238 , 10.5281/zenodo.17154852 ; concept DOI 10.5281/zenodo.15414237 | VERIFIED (API; concept via OpenAIRE) |
| files (both versions identical) | `Indian Footpath Damage Segmentation Dataset.zip` **4,504,525,071 bytes**; `Footpath Damage severity levels_annotations.csv` 9,371; `Indian Footpath Damage Segmentation Dataset.md` 2,459; `LICENSE.txt` 931 | VERIFIED (API); zip Range GET returned `206`, `content-range: bytes 0-0/4504525071` |
| direct URL | https://zenodo.org/api/records/17154852/files/Indian%20Footpath%20Damage%20Segmentation%20Dataset.zip/content | VERIFIED |
| images | 583 JPG + PNG masks; 411 train / 85 val / 87 test | VERIFIED (record .md) |
| labels | single class "footpath damage" (cracks etc.), LabelMe polygons; severity low/medium/high from crack width | VERIFIED (.md, Sci Data paper) |
| city | Pune, eight high-traffic pedestrian corridors, professional SLR camera | VERIFIED (https://www.nature.com/articles/s41597-025-06207-x , PMC12686011) |
| conditions | "diverse lighting and weather conditions" (no per-image tags) | VERIFIED wording, split UNVERIFIED |
| licence | CC BY 4.0. LICENSE.txt: "This dataset and associated materials (e.g., annotations, images, documentation) are licensed under the Creative Commons Attribution 4.0 International License." | VERIFIED |
| registration | none | VERIFIED |
| caveat | masks mark damage, not the footpath extent; no sidewalk-vs-road mask | VERIFIED from .md |

---

## 6. e-Yantra (IIT Bombay)

| field | value | tag |
|---|---|---|
| name | Semantic Segmentation datasets of Indian roads | VERIFIED |
| URL | https://www.kaggle.com/datasets/eyantraiit/semantic-segmentation-datasets-of-indian-roads | VERIFIED |
| size | 7,073,614,191 bytes, about 18.5k files, folder `Indian_road_data` | VERIFIED (Kaggle API `totalBytes`, page excerpt) |
| labelled images | 3,227 (2,475 train / 752 val) | UNVERIFIED (Dataset Ninja, https://datasetninja.com/indian-roads-semantic-segmentation) |
| classes | road, **footpath**, **pothole**, shallow path, background | VERIFIED (Kaggle description) |
| purpose | "created for delivery robots with knee heightened delivery robots... Sidewalk delivery robots can also use this dataset" | VERIFIED |
| city / conditions | not stated | UNVERIFIED |
| licence | GPL 2 (Kaggle metadata) | VERIFIED |
| registration | Kaggle account to download | VERIFIED (Kaggle norm) |
| last update | 2021-11-19 | VERIFIED (API) |

No other e-Yantra road or pothole dataset was found (searched "e-Yantra pothole dataset", "e-Yantra IIT Bombay road dataset images", "eyantra pothole detection dataset github").

---

## 7. Other Indian pedestrian / footpath / road datasets (2021-2026)

| name | URL | size (bytes) | images | classes / content | city | conditions | licence | login | tag |
|---|---|---|---|---|---|---|---|---|---|
| DataCluster Labs Footpath Image Dataset (sample) | https://www.kaggle.com/datasets/dataclusterlabs/footpath-dataset | 163,181,439 | about 100 image files + 50 annotation files in the free sample; "500+" claimed | footpath (COCO/YOLO/VOC) | "200+ cities across India" | day and night, phone 2022-2023 | Kaggle says CC0, but page says images are owned by Data Cluster Labs and the larger set is sold | Kaggle login | size, licence VERIFIED (API); file count VERIFIED (page) |
| MahaRoadNet | https://data.mendeley.com/datasets/ycgcv8tk23 , DOI 10.17632/ycgcv8tk23.1 | 1,843,637,240 (`Pune-potholes-20260721T053223Z-1-001.zip`) | 523 | potholes | Pune | sunny, overcast, shadows, **night with street lighting**; Mar-May 2026 | CC BY 4.0 | none | VERIFIED (Mendeley API) |
| Road Anomaly Detection System Dataset | https://data.mendeley.com/datasets/fbhdy3bxgv/2 | 801,543,787 (`Road Images.zip`) | 600 (300 pothole, 300 good road) | classification | Pune area (Vishwakarma Institute) UNVERIFIED | - | CC BY 4.0 | none | VERIFIED (API) |
| indian-road-potholes (Roboflow) | https://universe.roboflow.com/project-o3ot9/indian-road-potholes | not shown | 4,306 | pothole boxes | not stated | - | CC BY 4.0 | free Roboflow account/API key to export | VERIFIED (page) |
| Indian Roads Detection (Roboflow) | https://universe.roboflow.com/indian-road-dataset/indian-roads-detection | not shown | 2.62k | footpath class listed in search | not stated | - | not read | Roboflow account | UNVERIFIED (search page excerpt) |
| sensing localy (Roboflow, workspace "Walkable") | via https://universe.roboflow.com/search?q=class%3Aencroachment | - | 414 | encroachment, broken footpath, damaged-footpath type classes | not stated | - | not read | Roboflow account | UNVERIFIED |
| Indian Roads Dataset (Kaggle) | https://www.kaggle.com/datasets/mitangshu11/indian-roads-dataset | 1,829,879,018 | 4000+ | speed-breaker, pothole, unpaved road (YOLO) | not stated | - | Unknown | Kaggle login | VERIFIED (API) |
| IDD-PeD | see section 1 | 46 GB | video | pedestrian intention, crosswalk | India | illumination | not read | UNVERIFIED | partly VERIFIED |
| Indian Pedestrian Intention Dataset (subset) | https://github.com/Drupad-DeV/Indian-Pedestrian-Intention-Dataset | - | 17 clips (full set 240 clips, ~43 min, not public) | crossing intention | not stated | - | MIT badge | none | VERIFIED (excerpt) |
| DIRS21 (IEEE DataPort) | https://ieee-dataport.org/documents/dirs21-dataset-indian-road-scenarios , DOI 10.21227/esy0-sm56 | - | 5,093 | pedestrian, rider, car, bus, truck, NMV, e-auto | not stated | weather, season, illumination | not read | IEEE account | VERIFIED (excerpt) |
| DriveIndia (2025) | https://arxiv.org/html/2507.19912v2 | - | - | object detection, southern India incl. Hyderabad | - | - | not read | - | UNVERIFIED |
| Indistreet2K25 (Mendeley) | https://data.mendeley.com/datasets/s5hm86nyn6/1 | - | - | traffic scene, diverse weather | - | - | - | **embargoed until 4 March 2030** | VERIFIED (excerpt) |
| Images and Captions of Indian Streets (Kaggle) | https://www.kaggle.com/datasets/shinigdapriyasathish/images-and-its-captions-of-indian-streets | - | 1,350 | captions only | various | - | Apache 2.0 | Kaggle login | VERIFIED (excerpt) |
| FootpathVision (not India, Dhaka) | https://data.mendeley.com/datasets/szkhrh8dc8/1 | 4,618,969,012 (`Encroached.zip` 2,583,163,526 + `Unencroached.zip` 2,035,805,486) | 1,238 | encroached vs clear footpath (vendors, parking) | Dhaka, Bangladesh | - | CC BY 4.0 | none | VERIFIED (API). Closest visual match to Indian encroachment |
| Kolkata walkability from GSV (code) | https://github.com/AnshulTechnoWeR/walkability-detection-kolkata | - | 21,942 GSV images (not shared) | tree, streetlight, footpath, encroachment | Kolkata | - | - | - | excluded (GSV); method reference only |
| Kolkata visual walkability via Mapillary (ISPRS 2025) | https://isprs-annals.copernicus.org/articles/X-5-W2-2025/209/2025 | - | Mapillary images | greenery, openness, pavement, crowdedness | Kolkata | - | paper CC BY 4.0 | - | VERIFIED (excerpt). Shows Mapillary India route works |
| **Mapillary API** (live imagery) | https://www.mapillary.com/developer/api-documentation/ | per image | coverage in India varies by city | map features include `object--manhole`, `object--catch-basin`, crosswalk; detections include potholes | many Indian cities | any | user images CC BY-SA 4.0 (https://help.mapillary.com/hc/en-us/articles/115001770409); Vistas research set CC BY-NC-SA | free access token | VERIFIED (Mapillary pages) |

---

## 8. Municipal grievance apps / portals

| portal | URL | photos at filing | public view of others' photos | bulk data / API | terms note | tag |
|---|---|---|---|---|---|---|
| I Change My City (Janaagraha) | https://www.ichangemycity.com/bangalore/complaints | yes | site lists city feeds and per-complaint pages (Bangalore, Mumbai, Panaji); pages are a JS app, `curl` returned 0 bytes, so photo visibility without login not confirmed | (a) OpenCity CSV 2019-2022: https://data.opencity.in/dataset/i-change-my-city-data , 16,071 rows, 7.9 MiB, has lat/lon, title, description, category, status, **no image URL column**; 6,234 rows full-text match "footpath". (b) AWS open-data bucket now marked **Deprecated** (https://registry.opendata.aws/ichangemycity) | OpenCity CSV: CC BY-SA 2.0. AWS registry: "There are no restrictions on the use of data received from IChangeMyCity.com" | CSV VERIFIED via CKAN API; photo access UNVERIFIED |
| Swachhata-MoHUA | https://play.google.com/store/apps/details?id=com.ichangemycity.swachhbharat ; portal https://www.swachh.city/ | yes (photo + geo) | in-app "see nearby complaints, vote on them"; no public web gallery found | none found | app terms not read | VERIFIED (Play listing, Janaagraha page); web view NOT FOUND |
| BBMP Sahaaya / "Namma Bengaluru (Sahaaya 2.0)" (now GBA) | https://apps.karnataka.gov.in/app/87/en | text, photos, videos | "citizens can view the status of the grievances"; public photo view NOT FOUND | none found | - | VERIFIED (listing) |
| MCGM 1916 / MyBMC | https://www.mcgm.gov.in ; complaint form https://marg.mcgm.gov.in/MARG/welcomePage.html | UNVERIFIED | NOT FOUND | none found | "All Rights Reserved" footer | VERIFIED links |
| Delhi MCD 311 | lodge: https://mcd.everythingcivic.com/citizen/createissue ; app https://play.google.com/store/apps/details?id=com.everythingcivic.mcd | "Submit a request with a photo & GPS Location" | track page needs complaint id; public gallery NOT FOUND | none found | - | VERIFIED (Play, MCD portal) |
| NDMC 311 (New Delhi) | https://online.ndmc.gov.in/311_dashboard/ | UNVERIFIED | dashboard exists (aggregate) | - | - | VERIFIED link |
| Rajasthan Sampark 181 (Jaipur) | https://sampark.rajasthan.gov.in/ | document upload (150 ppi) | login to view; homepage shows only daily counts | none found | - | VERIFIED |
| Greater Chennai Corp PGR / Namma Chennai | https://erp.chennaicorporation.gov.in/pgr ; app https://play.google.com/store/apps/details?id=com.ceedeev.grivenancev2 | yes | complaint detail page is public by number, e.g. `.../pgr/citizen/greViewComplaint.jsp?complaintNo=2025-954BCL`; fetched HTML (65,536 bytes) had no image tags | none found | - | VERIFIED (page fetched, no photos) |
| Pune PMC CARE | https://pmccare.in/ ; CMS https://complaint.pmc.gov.in/home?language=en | "Click a picture of grievance" | NOT FOUND | none found | - | VERIFIED |

Summary: none of the official portals exposes a public photo gallery or a photo API that I could confirm. ICMC is the only one with open bulk complaint data, and that data has locations but no images.

---

## 9. News photo galleries on footpath encroachment (all rights reserved; use only as visual reference, not training data)

| outlet | example URL | date | what is shown | licence | tag |
|---|---|---|---|---|---|
| The Hindu | https://www.thehindu.com/news/cities/bangalore/bengalurus-footpaths-belong-to-everyone-but-pedestrians/article71182538.ece | 2026-07-05 | multi-photo story: Magadi Road, Uttarahalli Road, Kasturba Road footpaths | (c) The Hindu, all rights reserved | VERIFIED (excerpt with photo credits) |
| The Hindu | https://www.thehindu.com/news/cities/bangalore/footpath-drive-wipes-out-decades-old-shops-near-kr-market-in-bengaluru/article71310005.ece | 2026-08-06 | K.R. Market clearance | all rights reserved | VERIFIED |
| The Hindu | https://www.thehindu.com/news/cities/bangalore/bengaluru-minister-krishna-byre-gowda-orders-setting-up-of-joint-police-civic-teams-to-monitor-footpath-encroachment/article71427863.ece | 2026-09-04 | Shivajinagar vendors | all rights reserved | VERIFIED |
| The Hindu | https://www.thehindu.com/news/national/karnataka/mcc-begins-drive-against-footpath-encroachments-in-mysuru/article71206686.ece | 2026-07-10 | Mysuru clearance | all rights reserved | VERIFIED |
| Times of India | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-08-04 | Jaipur, Riddhi Siddhi vendors | all rights reserved | VERIFIED |
| Times of India | https://timesofindia.indiatimes.com/city/jaipur/encroachments-make-jaipur-footpaths-unsafe/articleshow/131374323.cms | 2026-05-28 | Jaipur | all rights reserved | VERIFIED |
| Times of India | https://timesofindia.indiatimes.com/city/bengaluru/footpath-drive-continues-in-bengaluru-as-garbage-remains-shopkeepers-reclaim-space/articleshow/132144965.cms | 2026-07-02 | Bengaluru Safe Footpaths drive | all rights reserved | VERIFIED |
| Times of India | https://timesofindia.indiatimes.com/city/delhi/court-push-makes-civic-agencies-inspect-vikaspuri-footpath-encroachment/articleshow/131368768.cms | 2026-05-28 | Delhi Vikaspuri | all rights reserved | VERIFIED |
| Hindustan Times | https://www.hindustantimes.com/cities/pune-news/pmc-slaps-notice-to-ias-officer-puja-s-mother-for-footpath-encroachment-101720892403517.html | 2024-07-13 | Pune, Baner Road | all rights reserved | VERIFIED (found via origin-pre-prod mirror) |
| Deccan Herald | NOT FOUND in this pass (searched "Deccan Herald footpath encroachment photos Bengaluru") | - | - | - | NOT FOUND |

No dedicated "photo gallery" section page was confirmed for any outlet; these are article photo sets.

---

## 10. X / Twitter

| handle | who | what it posts | tag |
|---|---|---|---|
| @mybmc | Brihanmumbai Municipal Corporation, ~1M followers | replies with "cleared footpath" photos; citizens tag it with encroachment photos (e.g. https://x.com/NigelRCoutinho/status/2112177718515376215, 2026-10-19) | VERIFIED |
| @GBA_office | Greater Bengaluru Authority (successor to BBMP), 99.3K followers, "Dial 1533 to report civic issues" | official updates, Safe Footpaths drive | VERIFIED |
| @BBMPCOMM, @BBMPCares | old BBMP handles; still tagged in complaints (e.g. https://x.com/WhitefieldWards/status/1731351576445370777) | activity after the GBA switch UNVERIFIED | partly VERIFIED |
| @ICCCBengaluru | Bengaluru command centre, linked from GBA bio | - | VERIFIED (mention) |
| @footpath_india | "Safe Footpaths", citizen account since Nov 2014, 10.1K posts | footpath encroachment photos | VERIFIED |
| @WhitefieldWards | Whitefield citizens group | logged 65+ Sahaaya complaints in 1 km of footpath (2023-12-03) | VERIFIED |
| @chennaicorp | Greater Chennai Corporation | replies with PGR complaint numbers | VERIFIED |
| @PMCPune | Pune Municipal Corporation, listed by PMC as a grievance channel | - | VERIFIED (PMC CMS page) |
| @ichangemycity | Janaagraha ICMC | handle not confirmed in this pass (Facebook page confirmed: facebook.com/ichangemycity) | UNVERIFIED |
| @WeThePeopleBLR | not confirmed | - | NOT FOUND |

Access route:
- X API is pay-per-use only for new sign-ups; Posts read $0.005 per post, user read $0.010 (https://docs.x.com/x-api/getting-started/pricing). VERIFIED. Legacy Basic ($200/mo) and Pro moved to pay-per-use during 2026 (UNVERIFIED, third-party blogs). At $0.005, 10,000 post reads cost $50 (computed).
- Nitter: X sent cease-and-desist letters on 24 Aug 2026; nitter.net offline, repo archived 11 Sep 2026; xcancel returns HTTP 451 (TechCrunch 2026-09-15; nitter.net notice). A few self-hosted forks still list as healthy on https://status.d420.de/ (2026-10-20), which itself says "Please do NOT use these instances for scraping". VERIFIED.
- Media on X belongs to the posters; X ToS forbids scraping. Use only with consent or via the API.

---

## Lie hunt (self-check of this file)

| claim | risk | result |
|---|---|---|
| RDD2022 India = 9,665 | could be eyeballed | counted `India_*.jpg` lines in the official file list: 9,665; XMLs: 7,706. VERIFIED |
| RDD2022_India.zip 502.3 MB downloadable | link may be stale | it is stale: 403 today. Wrote it as dead |
| IRDID is CC BY 4.0 | licence file vs actual image sources | most images come from news, stock and Google sources per its own metadata. Flagged |
| Pune dataset 4.5 GB | page rounding | exact 4,504,525,071 bytes from API and Range GET |
| IDD has sidewalk | from memory | checked in anue_labels.py |
| IDD licence is non-commercial | secondary source | left UNVERIFIED |
| IDD-AW includes sidewalk | inferred | left UNVERIFIED |
| Sci Rep 2026 manhole dataset is Indian | search snippet looked Indian | it is Rome, Italy. Marked not India |
| ICMC has public photos | assumed | not confirmed; bulk CSV has no image column |
