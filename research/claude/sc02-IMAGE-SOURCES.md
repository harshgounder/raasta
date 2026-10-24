# SC-02 image sources: kinds, instances, GET routes, licences, coverage, what was pulled

claude, 2026-10-24 (16:55 to ~19:30 IST). Brief: no own photos (D4), all footpath images from online sources, all of India (D2), Google Street View out (D4). Method: internet-map ladder (`~/ideas/2026-10-23-internet-map/v2-plan.md`): list every KIND (L3), then instances (L4/L5), then a tested GET route + licence (P4).
Companion files:
- `research/claude/sc02-image-datasets-raw.md` (dataset + grievance + news + X detail, written by a helper agent this session, 28,323 bytes, its own VERIFIED/UNVERIFIED tags)
- `research/dsh/IMAGE-SOURCES-SC02.md` (dsh's earlier pass, 16:37). This file supersedes two of its results: Mapillary is reachable without a token (route below) and KartaView has a keyless 1.0 route (server still silent from this network).
- Data: `data/online/` (images + one sidecar JSON per image, `MANIFEST.csv`, `COUNTS.md`, `_scripts/`).

## 0. Result in one screen

```
pulled into data/online/ : 327 images, each with a sidecar JSON (source_url, licence, author, city, lat/lon, date, condition tags)
  commons             94   CC BY / CC BY-SA / CC0 / PD      street-level photos picked by eye from 33 Commons categories
  youtube             84   YouTube standard licence         3 real 1280x720 frames per video (25/50/75 %), 28 videos
  mapillary           43   CC BY-SA 4.0                     via Esri's PUBLIC Mapillary layer, no Mapillary token
  youtube-cc          36   CC BY (YouTube CC flag)          same frame route, 12 CC-licensed walking tours
  mapillary-pairs     32   CC BY-SA 4.0                     16 same-spot (30 m) pairs, 1 to 10.7 years apart
  panoramax           20   CC BY-SA 4.0                     keyless STAC API (most India items are POI menu shots)
  youtube-storyboard  18   YouTube standard licence         1 frame every 9.93 s, 60 s windows, 160x90 (preview only)
  225 of 327 are CC / CC0 / PD; 290 marked usable_for_detection; 117 geotagged; 22 named places + unnamed villages
  + Project Sidewalk Chandigarh: 3,347 CC0 labels (geojson); their image crops are Google Street View, so excluded
```

| finding | why it matters | grade |
|---|---|---|
| Mapillary imagery + metadata is reachable with NO token through Esri's public "Mapillary Oriented Imagery Layer" (ArcGIS item b7625f3fec7b45f2877b8dfc02ee82de, `access: public`) | the only dense, modern, CC BY-SA street-level source with GPS + heading; dsh had it as BLOCKED | VERIFIED (43 images pulled) |
| YouTube video streams return HTTP 403 on this box (yt-dlp 2026.07.04 has no JS runtime: deno absent, EJS not installed), so `--download-sections` fails | the brief's "fetch a short segment with yt-dlp + ffmpeg" route does not work tonight without an install | VERIFIED (4 player clients tried) |
| YouTube's own auto frames `i.ytimg.com/vi/<id>/maxres{1,2,3}.jpg` are real 1280x720 frames from inside the video, no download | 84 frames from 28 walking tours pulled with zero video bytes | VERIFIED (viewed) |
| Project Sidewalk Chandigarh labels are CC0 and downloadable (3,347 labels, 9 types, 4.1 MB geojson), but every label's `pano_source` is `gsv` | labels usable as barrier priors on the map; image crops would be Google Street View, which D4 excludes | VERIFIED |
| Reddit `.json` endpoints return 403 "blocked by network security"; RSS answered once (37 r/bangalore posts) then 429 | Reddit is a reference-only kind tonight; no images pulled | VERIFIED |
| The first 32 YouTube candidates (normal search) carry no CC flag, but a CC-filtered search (`&sp=EgIwAQ%253D%253D`) found 12 Indian walking tours with yt-dlp `license` = "Creative Commons Attribution license (reuse allowed)": Delhi x4, Mumbai x3, Varanasi, Agra, Gangtok, Chopta (snow), Jaipur Hawa Mahal | CC BY frames can go on the public demo page with credit; standard-licence frames stay internal | VERIFIED (12 of 12 flags read from metadata) |
| Same-spot imagery exists: 16 Mapillary pairs within 30 m, 1 to 10.7 years apart (3 good view matches), plus 4 Commons groups (a 7-photo flood burst, a next-day Shimla pair) | real "same kerb, different time" material instead of a simulated slider | VERIFIED (viewed) |

## 1. The ladder: every KIND of source for Indian street/footpath images (L3)

Kinds come from (a) the brief, (b) dsh's table, (c) the helper's dataset sweep, (d) what the probes turned up (the Esri relay is a kind nobody listed). A kind with no working route says so.

| # | kind (L3) | instances (L4) | GET route tested 2026-10-24 | licence | result |
|---|---|---|---|---|---|
| K1 | open street-level platform | Mapillary | (a) Graph API `graph.mapillary.com/images?bbox=..&access_token=` ; (b) tiles `tiles.mapillary.com/maps/vtp/mly1_public/2/{z}/{x}/{y}` ; (c) **Esri relay** `https://mapillary.img.arcgis.com/arcgis/rest/services/Mapillary/FeatureServer/0/query` with a JSON envelope, `where=1=1&outFields=*&outSR=4326&f=json` | CC BY-SA 4.0 imagery; Esri item says "subject to Mapillary's Terms of Use" | (a) 500 "Invalid OAuth 2.0 Access Token"; (b) 403; (c) **200, image URL + date + heading + creator + sequence**. Caps at about 40-50 records per query; `resultOffset` does not page. `returnCountOnly` always says 400000 (fake) |
| K1 | same | Panoramax (federated, OSM France instance) | `https://api.panoramax.xyz/api/search?bbox=W,S,E,N&limit=40` (STAC); assets `hd` / `sd` (2048 px) / `thumb` | CC-BY-SA-4.0 per item | 200 keyless. India items exist in all 8 metros probed, but most are point-of-interest shots (menus, shop interiors) |
| K1 | same | KartaView (Grab) | keyless `POST https://api.openstreetcam.org/1.0/list/nearby-photos/` form `lat,lng,radius` (2.0 read endpoints need auth per the pipeworx MCP notes) | CC BY-SA 4.0 | server completes TLS then never answers from this network (3 tries, 23 to 150 s). Route known, untested |
| K1 | same | Google Street View | Static API with key | Google Maps terms ban AI train/test/validate | EXCLUDED (D4) |
| K1 | same | Mappls (MapmyIndia) street view | key + commercial terms | commercial | not tested; needs a key |
| K2 | crowd-audit label platform | Project Sidewalk, Chandigarh deployment | `https://sidewalk-chandigarh.cs.washington.edu/v3/api/rawLabels?filetype=geojson` (also `/v3/api/overallStats`, `/labelTypes`, `/cities`) | CC0 1.0 ("Project Sidewalk data is dedicated to the public domain under CC0 1.0", API page) | 200, 4,103,646 bytes, 3,347 labels. Imagery behind labels = GSV, excluded |
| K3 | free-licence media commons | Wikimedia Commons | `commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:..&prop=imageinfo|coordinates&iiprop=url|extmetadata&iiurlwidth=1280`; geosearch variant in dsh's note | per file (CC BY, CC BY-SA, CC0, PD) | 200; 1,613 files listed from 33 categories, 94 pulled |
| K4 | photo-sharing with CC filter | Flickr | `api.flickr.com/services/rest/?method=flickr.photos.search&license=4,5,9,10&has_geo=1&bbox=..&api_key=` | per photo CC | `code 100 Invalid API Key` without a key. Needs a free key (account login, user's call) |
| K5 | video platform, walking tours | YouTube | metadata: `yt-dlp -j`; frames: `i.ytimg.com/vi/<id>/maxres1.jpg` (also `maxres2/3`, `hq1-3` 480x360, `sd1-3` 640x480); storyboard `sb0` 160x90 every ~10 s | standard YouTube licence unless the video is CC | metadata + auto frames + storyboards work; stream download 403 (see section 4) |
| K6 | link aggregator / forum | Reddit (r/india, r/bangalore, r/mumbai, r/delhi, r/jaipur, r/pune, r/chennai, r/kolkata, r/hyderabad, r/chandigarh, r/indianurbanism) | `.json` search: 403; `search.rss`: 200 once then 429 | user content, no licence grant | reference only; no images pulled |
| K7 | microblog civic complaints | X: @mybmc, @GBA_office, @footpath_india, @WhitefieldWards, @chennaicorp, @PMCPune (detail in datasets-raw s10) | X API pay-per-use, posts read $0.005 each; Nitter shut down (Aug-Sep 2026) | poster's copyright; X ToS bans scraping | not pulled |
| K8 | news photo sets | The Hindu, Times of India, Hindustan Times articles on footpath encroachment, 2024-2026 (9 URLs in datasets-raw s9) | plain web | all rights reserved | reference only |
| K9 | municipal grievance apps | Swachhata-MoHUA, BBMP Sahaaya / GBA, MCGM, MCD 311, NDMC 311, Rajasthan Sampark 181, Chennai PGR, PMC CARE, I Change My City | no public photo gallery or photo API found; ICMC bulk CSV (OpenCity, 16,071 rows, CC BY-SA 2.0) has lat/lon + text, no image URLs | varies | NOT FOUND for photos |
| K10 | research datasets, India road scenes | IDD (20k seg, has `sidewalk` + `curb`), IDD-AW (rain/fog/low light), RDD2022 India, Pune footpath damage (Zenodo), e-Yantra Indian roads (footpath class), MahaRoadNet (Pune potholes incl. night), DataCluster footpath sample, IRDID (open manholes) | see section 7 table | mixed (CC BY 4.0, GPL 2, login-gated) | URLs + sizes VERIFIED by helper, Zenodo size re-checked by me |
| K11 | stock / editorial photo libraries | Getty, Alamy, Shutterstock, Unsplash, Pexels | Unsplash/Pexels have free licences with their own terms (not CC) | not CC | not probed tonight (gap) |
| K12 | dashcam / ride-hailing corpora | KartaView Grab open dataset (Indonesia, not India), Ola/Uber (closed) | - | - | no Indian open set found |
| K13 | satellite / aerial (context only) | Bhuvan, Sentinel-2, Esri World Imagery | dsh tested OSM + Bhuvan | various | not street level; out of scope for this file |
| K14 | relays / mirrors of K1 | Esri Living Atlas Mapillary layers (oriented imagery b7625f3f..., coverage vector tiles 6958f9f1...) | see K1 (c) | inherits Mapillary terms | WORKS: this is how Mapillary was reached |

Kinds I looked for and did not find an Indian instance of: open 360-degree city captures by an Indian municipality; a public photo API on any Indian grievance portal; a CC-flagged Indian walking-tour channel. These go in the not-found ledger (section 9), not dropped.

## 2. Mapillary in detail (K1 via K14)

Route (no token, no login, public ArcGIS item):

```
GET https://mapillary.img.arcgis.com/arcgis/rest/services/Mapillary/FeatureServer/0/query
    ?geometry={"xmin":75.80,"ymin":26.90,"xmax":75.85,"ymax":26.95,"spatialReference":{"wkid":4326}}
    &geometryType=esriGeometryEnvelope&where=1=1&outFields=*&outSR=4326&f=json
-> features[]: geometry (lon, lat, z), attributes: Name (= Mapillary image id), Sequence, AcquisitionDate (ms),
   CameraHeading, CameraPitch, Creator, ImagePath (signed fbcdn URL of the image, full resolution)
```

Gotchas found by testing: the comma-string bbox returns 0 features; only the JSON envelope works. About 40-50 records per call, `resultOffset` repeats the same page, so a city must be tiled into small cells. The signed `ImagePath` URLs expire (the `oe=` parameter), so store the image id and re-query, never store the URL alone. The ArcGIS item is in "beta" (Esri Living Atlas, created 2026-05-20, updated 2026-07-02).

Warning seen in the data: all 5 Bengaluru picks (newest sequences, 2026-07-20) are a white image with the text "BB2 OWNED MAPILLARY CANARY A 1784534450". They are marked `usable_for_detection: false`. Reading: a test or canary sequence uploaded to Mapillary; it is a reminder that a relay can serve non-photo content and that each pulled image needs a look.

Coverage per place, measured with a 4 x 4 grid of cells over each core box (cell = box/4; one query per cell; counts are floors because of the 50-record cap):

| place | area | cells with imagery (of 16) | cells with 2+ capture months | images seen (floor, sum of cells) | months seen (min to max) |
|---|---|---|---|---|---|
| Jaipur | metro, old walled city + core | 15 | 9 | 603 | 2015-01 to 2026-07 (14 distinct months) |
| Delhi | metro core (CP, Old Delhi) | 15 | 6 | 599 | 2014-12 to 2026-07 (16 distinct months) |
| Mumbai | metro core (Fort, Colaba) | 12 | 7 | 462 | 2016-12 to 2026-07 (13 distinct months) |
| Bengaluru | metro core (MG Road, Shivajinagar) | 16 | 10 | 790 | 2017-09 to 2026-04 (21 distinct months) |
| Chennai | metro core (George Town, Triplicane) | 15 | 4 | 392 | 2015-09 to 2026-04 (17 distinct months) |
| Kolkata | metro core (Esplanade, Bara Bazar) | 12 | 3 | 359 | 2015-09 to 2026-10 (11 distinct months) |
| Pune | metro core (Peth areas, FC Road) | 16 | 7 | 719 | 2019-10 to 2026-08 (10 distinct months) |
| Chandigarh | planned city (Sectors 17, 22) | 8 | 3 | 304 | 2016-06 to 2019-06 (5 distinct months) |
| Shimla | hill town (Mall Road) | 7 | 3 | 265 | 2018-02 to 2019-03 (3 distinct months) |
| Panaji | coastal town (Goa) | 13 | 5 | 570 | 2019-03 to 2026-08 (11 distinct months) |
| Puri | coastal small town (Odisha) | 1 | 0 | 45 | 2026-02 to 2026-02 (1 distinct months) |
| MUJ-Dehmi-Kalan | village / peri-urban (Manipal Univ Jaipur area) | 1 | 0 | 1 | 2015-06 to 2015-06 (1 distinct months) |
| Bagru-village | village / small town near Jaipur | 3 | 0 | 5 | 2015-06 to 2015-06 (1 distinct months) |

A single query per whole box (`_scripts/mly_count.json`) returns the newest sequences first (Jaipur 2026-07, Delhi 2026-07, Kolkata up to 2026-10, Panaji 2026-08), which hides the older layers; the grid shows them. Full per-cell detail with sample image ids: `data/online/_scripts/mly_grid.json`.

Reading: all 7 metro cores have imagery in 12 to 16 of 16 cells, with captures from 2014-12 up to 2026-10. Panaji (coastal) is well covered (13/16). Chandigarh (8/16) and Shimla (7/16) are thinner and old (newest 2019-06 and 2019-03), so a "known clear (photo date)" there carries a 7 year old date, which the D2 honesty rule already handles. Puri, the MUJ box and the Bagru box are near empty (1 to 3 cells; the Bagru hits are the NH48 highway). Villages are the weak spot for Mapillary; YouTube village walks and Commons fill some of it.

## 3. Wikimedia Commons in detail (K3)

Categories harvested (33, 1,613 files listed, 292 candidates after a keyword filter, 94 picked by eye from 10 contact sheets): Sidewalks in India, Footpaths in India, Kerbs in India, Sidewalks in Kolkata, Potholes in India, Rain in {Mumbai, Bengaluru, Chennai, Delhi, Kolkata}, Night in {Jaipur, Delhi, Mumbai, Bengaluru, Pune, Chandigarh, Shimla}, Streets in {Jaipur, Shimla, Pune, Bengaluru, Chennai, Old Delhi, Mumbai, Kolkata, Panaji, Puri, Pondicherry, Himachal Pradesh}, Mall Road Shimla, Markets in {Jaipur, Pune}, Pedestrianised streets in India.
Useful further categories seen in listings (not yet pulled): Rain in Hyderabad / Kochi / Thiruvananthapuram / Salem, Night in 43 Indian cities, Streets in 51 Indian cities, Markets in 16 Indian cities, Curb cuts, Kerb ramps, Roadworks in Himachal Pradesh, Traffic congestion in Himachal Pradesh.
Limits: many Night-in-city files are skylines (not street level, skipped); 11 picks from "Sidewalks/Footpaths in India" have no city in their categories (sidecar says "India (city not stated)"); few files carry GPS (geotagged share is in `COUNTS.md`).

## 4. YouTube walking tours in detail (K5)

What works and what does not (tested on video 1hJPYWfFhS0):

| route | result |
|---|---|
| `yt-dlp -j` metadata (title, channel, upload date, duration, licence flag, formats) | works, ~20 s per video |
| `yt-dlp --download-sections "*420-480"` (ffmpeg) | ffmpeg exit 8, HTTP 403 on googlevideo |
| `yt-dlp -f 134` native download | HTTP 403 |
| player clients `tv_simply, tv, ios, mweb, web_embedded` | "format not available" or "page needs to be reloaded" |
| cause | yt-dlp warns "No supported JavaScript runtime could be found"; deno is not installed and the yt-dlp uv tool env has no EJS package. Fix = install deno or `yt-dlp-ejs` (an install: needs the user's GO) |
| `i.ytimg.com/vi/<id>/maxres1.jpg` / `maxres2` / `maxres3` | 200, 1280x720 frames from inside the video. Position: near 25/50/75 % of the runtime (common description; exact second not published, so sidecars mark `timestamp_s_approx` UNVERIFIED) |
| storyboard `sb0` (from `-j` formats) | 200, 160x90 tiles, one per 9.93 s for a 25 min video: a true "1 frame every ~10 s" sequence, too small for detection |

The 28 videos (all standard licence; frames pulled for all 28; storyboard 10 s sequences for #1, #8, #22):

| # | place | where | time | weather | setting | length | uploaded | channel | URL | licence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Jaipur | Jaipur streets, night | night | dry | market, street, mela | 25m19s | 2022-01-14 | Walking Indian | https://www.youtube.com/watch?v=1hJPYWfFhS0 | standard (no CC flag) |
| 2 | Jaipur | Jaipur bazaars, evening to night | night | dry | market, bazaar | 60m40s | 2024-01-14 | Global Walks | https://www.youtube.com/watch?v=M1H6IOw_38E | standard (no CC flag) |
| 3 | Jaipur | Jaipur city streets | day | dry | street, old city | 44m54s | 2026-06-25 | Māyā Walks | https://www.youtube.com/watch?v=3FVdYrcpc7U | standard (no CC flag) |
| 4 | Delhi | Chandni Chowk, Old Delhi, evening | evening | dry | market, old city | 33m09s | 2026-10-02 | Walking in India | https://www.youtube.com/watch?v=6_AVNLrOq7M | standard (no CC flag) |
| 5 | Delhi | Old Delhi | day | dry | market, old city, lanes | 40m58s | 2025-11-14 | Walking in India | https://www.youtube.com/watch?v=x1VTXV75tfI | standard (no CC flag) |
| 6 | Delhi | Delhi at night | night | dry | street, market | 42m40s | 2025-10-31 | Walking in India | https://www.youtube.com/watch?v=1GZvEIvzRWg | standard (no CC flag) |
| 7 | Mumbai | Mumbai monsoon walk | day | rain | street | 22m28s | 2023-07-09 | Life Ambience | https://www.youtube.com/watch?v=3jLj6dHMEg8 | standard (no CC flag) |
| 8 | Mumbai | Dadar, Mumbai, rain | day | rain | street, market | 40m37s | 2024-07-08 | Life Ambience | https://www.youtube.com/watch?v=5M8qbDHhaAg | standard (no CC flag) |
| 9 | Mumbai | Dharavi, Mumbai, rain | day | rain | informal settlement, lanes | 57m57s | 2026-07-05 | Life Ambience | https://www.youtube.com/watch?v=zj0_El-Djes | standard (no CC flag) |
| 10 | Mumbai | Lokhandwala Market, Andheri, night | night | dry | market | 41m53s | 2026-01-15 | Universal Survey  | https://www.youtube.com/watch?v=g73mowyEHdU | standard (no CC flag) |
| 11 | Bengaluru | Bengaluru streets, night, heavy rain | night | rain | street | 38m26s | 2026-10-17 | Silent Ghats | https://www.youtube.com/watch?v=jM7nhJMzFkI | standard (no CC flag) |
| 12 | Bengaluru | JP Nagar, Bengaluru, rain | day | rain | residential, street | 24m36s | 2022-08-19 | RedSwift | https://www.youtube.com/watch?v=2BjF1hRir-E | standard (no CC flag) |
| 13 | Bengaluru | Central Bengaluru, 1 Aug 2026 | day | dry | street, commercial | 97m46s | 2026-08-08 | Indian Traveller  | https://www.youtube.com/watch?v=QOg1Q4qIigY | standard (no CC flag) |
| 14 | Chennai | Georgetown, Chennai | day | dry | market, street | 22m08s | 2026-07-14 | I love Walking Tours | https://www.youtube.com/watch?v=ONWiU3YIQEA | standard (no CC flag) |
| 15 | Chennai | Nochi Nagar, Chennai | day | dry | residential, coastal, fish market | 39m19s | 2026-10-17 | The Indian Ambience | https://www.youtube.com/watch?v=LyNIGrJYDeo | standard (no CC flag) |
| 16 | Kolkata | Bara Bazar, Kolkata, rain | day | rain | market | 57m05s | 2023-08-27 | Mars Walker TV  | https://www.youtube.com/watch?v=2Jiwa5P6zQM | standard (no CC flag) |
| 17 | Kolkata | Dalhousie, Kolkata, rain | day | rain | street, heritage | 20m00s | 2025-07-22 | The SkyWalker | https://www.youtube.com/watch?v=kn4IfvrC65o | standard (no CC flag) |
| 18 | Pune | Pune street life | day | dry | street | 34m39s | 2026-10-19 | Scrolling Street | https://www.youtube.com/watch?v=MO7W1yElSRs | standard (no CC flag) |
| 19 | Pune | Tilak Road, Pune | day | dry | street, commercial | 37m42s | 2026-06-28 | Universal Survey  | https://www.youtube.com/watch?v=fZLx7heZHtc | standard (no CC flag) |
| 20 | Chandigarh | Shastri Market, Sector 22, Chandigarh | day | dry | market | 24m10s | 2024-11-03 | Walking And Exploring  | https://www.youtube.com/watch?v=WxzFxXvpAvo | standard (no CC flag) |
| 21 | Chandigarh | Sector 17, Chandigarh | day | dry | market, plaza | 11m20s | 2026-09-04 | YJwalks | https://www.youtube.com/watch?v=JpAxfAtxTz8 | standard (no CC flag) |
| 22 | Shimla | walk to Mall Road, Shimla | day | dry | hill, street | 34m16s | 2025-12-28 | England Guru | https://www.youtube.com/watch?v=8v4YACEK1FI | standard (no CC flag) |
| 23 | Shimla | Shimla streets to Mall Road | day | dry | hill, residential, street | 37m34s | 2026-01-03 | England Guru | https://www.youtube.com/watch?v=C7ELEq-ic_I | standard (no CC flag) |
| 24 | Panaji | Patto to Panjim Market, Goa | day | dry | coastal, market, small city | 25m04s | 2023-05-26 | Lesley in Goa | https://www.youtube.com/watch?v=yCt0wJ15p20 | standard (no CC flag) |
| 25 | village (unnamed) | Indian village, rainy season | day | rain | village, rural | 12m09s | 2022-02-13 | Mars Walker TV  | https://www.youtube.com/watch?v=2w9iBkJoyJ0 | standard (no CC flag) |
| 26 | Kerala village (unnamed) | Kerala village, rainy evening | evening | rain | village, rural | 27m16s | 2026-08-21 | The Indian Ambience | https://www.youtube.com/watch?v=pceOQwANIAU | standard (no CC flag) |
| 27 | Varanasi | Varanasi narrow streets | day | dry | lanes, old city | 34m29s | 2023-03-02 | LADmob | https://www.youtube.com/watch?v=Odh_7dQwzYQ | standard (no CC flag) |
| 28 | Hyderabad | Charminar market, evening | evening | dry | market, heritage | 18m14s | 2025-11-23 | Niranjan Komreddy | https://www.youtube.com/watch?v=RrsFF16ILMY | standard (no CC flag) |

CC-licensed walking tours (found with YouTube's Creative Commons search filter; licence flag read from each video's metadata; frames in `data/online/youtube-cc/`, 28 of 36 usable):

| # | place | where | time | weather | setting | length | uploaded | channel | URL | licence |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Delhi | New Delhi slum lanes, night | night | dry | informal settlement, lanes | 68m23s | 2025-05-26 | Streets & Ambience | https://www.youtube.com/watch?v=jcc5OjGDLqw | CC BY (YouTube flag) |
| C2 | Mumbai | Mumbai everyday streets | day | dry | street, market | 17m24s | 2025-03-14 | Streets & Ambience | https://www.youtube.com/watch?v=nMlUr3H08jA | CC BY (YouTube flag) |
| C3 | Mumbai | Dharavi, Mumbai | day | dry | informal settlement, lanes | 31m52s | 2025-03-24 | Streets & Ambience | https://www.youtube.com/watch?v=Ry1qEdnRlbc | CC BY (YouTube flag) |
| C4 | Varanasi | Varanasi narrow streets | day | dry | lanes, old city | 47m23s | 2025-04-17 | Streets & Ambience | https://www.youtube.com/watch?v=CVLfFqMb5zo | CC BY (YouTube flag) |
| C5 | Delhi | Old Delhi spice market, morning | morning | dry | market, old city | 36m51s | 2025-05-25 | Streets & Ambience | https://www.youtube.com/watch?v=SzDvWkilL_g | CC BY (YouTube flag) |
| C6 | Agra | Agra city streets | day | dry | street | 32m37s | 2025-03-28 | Streets & Ambience | https://www.youtube.com/watch?v=x0Wi6yjEEPg | CC BY (YouTube flag) |
| C7 | Gangtok | Gangtok, Sikkim (hill town) | day | dry | hill, street | 15m16s | 2026-08-29 | far and beyond | https://www.youtube.com/watch?v=nGwQBosWKUA | CC BY (YouTube flag) |
| C8 | Chopta village | Chopta village, Uttarakhand | day | snow | village, rural, hill | 3m31s | 2026-02-15 | The City Walker | https://www.youtube.com/watch?v=q34CCR7t-6M | CC BY (YouTube flag) |
| C9 | Jaipur | Hawa Mahal area, Jaipur | day | dry | market, old city, heritage | 7m06s | 2025-05-26 | perefectvoyagetrips | https://www.youtube.com/watch?v=5BmAUpQtxJ8 | CC BY (YouTube flag) |
| C10 | Delhi | Connaught Place, New Delhi | day | dry | commercial, street | 8m26s | 2025-01-20 | Urban Walk Tours | https://www.youtube.com/watch?v=rbNmnkPBoyw | CC BY (YouTube flag) |
| C11 | Mumbai | Mumbai evening walk | evening | dry | street | 22m09s | 2025-03-16 | Streets & Ambience | https://www.youtube.com/watch?v=QQ2oXrC1dQA | CC BY (YouTube flag) |
| C12 | Delhi | dark narrow streets of New Delhi | night | dry | lanes | 44m20s | 2025-03-26 | Streets & Ambience | https://www.youtube.com/watch?v=AHJpk-HDmL0 | CC BY (YouTube flag) |

Channel "Streets & Ambience" publishes many Indian walks under CC BY (8 of the 12 above); its other CC videos in the search list include Old Delhi Khari Baoli to Sadar Bazar (6JlPJ8VHa4E), Chandni Chowk (ocOXaOaAaTc), Asaf Ali Road to Paharganj (2lExdfkfIFI), Sadar Thana Road (g6yuGjcHD5g), Varanasi night (2ZxQOLQa5ns). Not checked one by one for the flag; the search filter put them there.

Frame quality check (by eye, contact sheets): 6 of 84 frames are a title card, overlay or food close-up and carry `usable_for_detection: false`; the other 78 show street scenes. City labels come from video titles. Two sets look less like their titled city than expected (3FVdYrcpc7U "Jaipur" frame 2 shows overhead wires; 1GZvEIvzRWg "Delhi at night") and are flagged `city_source: title` for a human check.
More candidates found by search but not pulled (ids in `_scripts/youtube_search_results.jsonl`, 120 rows): Delhi Aerocity and New Delhi station night walks, Mumbai Marine Drive heavy rain, Mumbai Hiranandani rain, Bengaluru Indiranagar rain, Kolkata Park Street after rain, Hyderabad HITEC City night, Goa Fontainhas, Chennai Ranganathan Street, Chandigarh Sukhna Lake, Varanasi ghats evening.

## 5. Same spot over time or angle (temporal change, multi-view)

| group | source | what | dates | use |
|---|---|---|---|---|
| saltlake_sectorV_2007-08-13_burst | Commons cm_113 to cm_119 (7 files) | flooded road in Sector V, Salt Lake, Kolkata, shot from slightly different angles | 2007-08-13 10:32:59 to 10:35:27 | multi-view of one waterlogged stretch |
| shimla_scandalpoint_day1_vs_day2 | Commons cm_191, cm_192 | The Scandal Point, Shimla | 2014-05-07 12:08 vs 2014-05-08 10:40 | same spot, next day, different light and crowd |
| shimla_mallroad_2014-05-07 | Commons cm_187, cm_193 | Mall Road, Shimla, 44 s apart | 2014-05-07 16:17 | two angles |
| munnekollala_pothole_2021-07-19 | Commons cm_075, cm_076 | deformed road, Munnekollala, Bengaluru | 2021-07-19 | two shots of one pothole |
| YouTube storyboard runs | youtube-storyboard (3 x 6 frames) | Jaipur night market, Dadar Mumbai rain, Shimla walk | 10 s apart | consecutive views of one street (walk direction) |
| YouTube maxres1/2/3 | youtube (28 x 3) | same walk, 3 points | ~25/50/75 % of the video | same route, different stretches; not the same spot |
| Mapillary temporal pairs | mapillary-pairs (see below) | same 30 m cell, different sequences and months | 16 pairs, gaps 364 to 3905 days | before/after on one stretch of road |

Mapillary temporal pairs (`data/online/mapillary-pairs/`, `_temporal_pairs.json`): found by taking the oldest sequences in every multi-month grid cell, querying a 30 m box around each, and keeping the oldest and newest sequence when their months differ. 30 m does not guarantee the same view: heading and side of road differ, so each pair was graded by eye.

| pair | place | dates | gap (days) | heading diff | view match (by eye) |
|---|---|---|---|---|---|
| P0 | Jaipur | 2015-06-29 vs 2017-01-22 | 572 | 18 | good: same road ahead, similar heading |
| P1 | Jaipur | 2019-06-06 vs 2023-11-17 | 1625 | 61 | weak: within 30 m but different view or blur |
| P2 | Delhi | 2014-12-21 vs 2015-12-20 | 364 | 12 | fair: same junction area, similar heading |
| P3 | Delhi | 2020-02-15 vs 2023-09-17 | 1310 | 90 | weak: within 30 m but different view or blur |
| P4 | Mumbai | 2021-09-20 vs 2025-11-16 | 1518 | 7 | good: same market street, same heading, 4 years apart |
| P5 | Mumbai | 2022-03-30 vs 2025-12-31 | 1372 | 29 | weak: within 30 m but different view or blur |
| P6 | Bengaluru | 2017-05-01 vs 2020-02-23 | 1028 | 63 | weak: within 30 m but different view or blur |
| P7 | Bengaluru | 2017-05-01 vs 2022-07-08 | 1894 | 123 | weak: within 30 m but different view or blur |
| P8 | Kolkata | 2016-02-03 vs 2024-12-19 | 3241 | 137 | weak: within 30 m but different view or blur |
| P9 | Kolkata | 2018-06-29 vs 2024-12-19 | 2364 | 3 | weak: within 30 m but different view or blur |
| P10 | Pune | 2015-06-26 vs 2026-03-05 | 3905 | 176 | weak: within 30 m but different view or blur |
| P11 | Pune | 2018-10-19 vs 2026-02-28 | 2689 | 173 | weak: within 30 m but different view or blur |
| P12 | Shimla | 2018-02-03 vs 2019-03-03 | 393 | 8 | good: same hill road, similar heading |
| P13 | Shimla | 2018-02-03 vs 2019-03-03 | 393 | 174 | fair: same tunnel, opposite directions |
| P14 | Panaji | 2019-03-29 vs 2022-08-06 | 1226 | 39 | weak: within 30 m but different view or blur |
| P15 | Panaji | 2019-03-28 vs 2023-09-13 | 1630 | 65 | weak: within 30 m but different view or blur |

Best for the "same kerb, different sky" slider: P4 (Mumbai market street, 2021-09 vs 2025-11, 7 degrees apart), P0 (Jaipur, 2015-06 vs 2017-01), P12 (Shimla hill road, 2018-02 vs 2019-03).

Also present but not pulled: Mapillary multi-month cells in every metro (grid table above); Commons "Night in X" vs "Streets in X" for the same landmark (for example Jaipur Hawa Mahal day vs night) would give day/night pairs of one place.

## 6. What was pulled (data/online)

```
data/online/
  commons/              cm_<idx>_<title>.jpg + .json
  youtube/              yt_<videoid>_maxres{1,2,3}.jpg + .json   (standard licence)
  youtube-cc/           yt_<videoid>_maxres{1,2,3}.jpg + .json   (CC BY)
  youtube-storyboard/   ytsb_<videoid>_t<seconds>.jpg + .json
  mapillary/            mly_<place>_<imageid>.jpg + .json, _same_spot_multi_sequence.json
  mapillary-pairs/      mlypair_<place>_<imageid>.jpg + .json, _temporal_pairs.json
  panoramax/            pmx_<place>_<id8>.jpg + .json
  project-sidewalk/     chandigarh_rawLabels_2026-10-24.geojson (CC0 labels, no images)
  MANIFEST.csv          one row per image
  COUNTS.md             generated counts (rerun: python3 -I data/online/build_manifest.py)
  _scripts/             every script used + YouTube metadata + coverage JSON
```

Sidecar fields: `file, source_kind, source_url, licence, author, city, lat, lon, capture_date, condition_tags, usable_for_detection, pulled_at` plus source extras (`timestamp_s_approx`, `camera_heading`, `sequence`, `same_spot_group`, `commons_categories`, `licence_url`).

total images with sidecar: **327**; geotagged: 117; usable for detection: 290

| source | images |
|---|---|
| commons | 94 |
| youtube | 84 |
| mapillary | 43 |
| youtube-cc | 36 |
| mapillary-pairs | 32 |
| panoramax | 20 |
| youtube-storyboard | 18 |

| city / place | images |
|---|---|
| Mumbai | 41 |
| Delhi | 40 |
| Kolkata | 37 |
| Jaipur | 31 |
| Bengaluru | 30 |
| Shimla | 28 |
| Pune | 21 |
| Chennai | 17 |
| Panaji | 13 |
| Chandigarh | 12 |
| India (city not stated) | 11 |
| Puri | 6 |
| Varanasi | 6 |
| Bagru / NH48 (peri-urban highway) | 5 |
| Himachal small towns | 4 |
| Puducherry | 3 |
| village (unnamed) | 3 |
| Hyderabad | 3 |
| Kerala village | 3 |
| Gangtok | 3 |
| Chopta village | 3 |
| Agra | 3 |
| Assam (Guwahati area) | 2 |
| Dehmi Kalan / MUJ (village) | 2 |

| condition | images |
|---|---|
| day (tag) | 254 |
| night | 55 |
| rain/monsoon | 63 |
| market | 81 |
| residential | 29 |
| hill | 34 |
| snow | 3 |
| same spot / sequence | 63 |
| coastal | 13 |
| village/small town | 24 |
| footpath barrier visible | 45 |

| licence | images |
|---|---|
| YouTube standard licence | 102 |
| CC BY-SA 4.0 | 97 |
| Creative Commons Attribution license | 36 |
| CC BY-SA 3.0 | 25 |
| CC-BY-SA-4.0 | 20 |
| CC BY 3.0 | 19 |
| CC BY 2.0 | 7 |
| CC BY 4.0 | 7 |
| CC0 | 5 |
| CC BY-SA 2.0 | 5 |
| Public domain | 2 |
| CC BY 2.5 | 1 |
| CC BY-SA 2.5 | 1 |


Condition tags were assigned by eye from 256 px contact sheets (time of day for YouTube frames by a mean-luminance threshold, then checked on the sheets). They are a starter label, not ground truth.

## 7. Indian datasets (K10), exact routes

From `sc02-image-datasets-raw.md` (helper, VERIFIED tags there); the Zenodo size I re-checked myself.

| dataset | download route | size | images | footpath-relevant content | licence | login |
|---|---|---|---|---|---|---|
| Indian Footpath Damage Segmentation (Pune) | `https://zenodo.org/api/records/17154852/files/Indian%20Footpath%20Damage%20Segmentation%20Dataset.zip/content` | 4,504,525,071 bytes (re-checked via Zenodo API 2026-10-24) | 583 + masks | footpath damage polygons, severity CSV | CC BY 4.0 | no |
| IDD Segmentation 20k | `https://idd.insaan.iiit.ac.in/dataset/download/` | 18.5 GB + 5.5 GB | 20,000 | `sidewalk`, `curb` pixel classes | shown at download | free login |
| IDD-AW | same | 19 GB | 5,000 RGB+NIR (1,500 rain, 1,500 fog, 1,000 low light, 1,000 snow) | IDD label tree | shown at download | free login |
| RDD2022 (India 9,665 images inside) | `https://ndownloader.figshare.com/files/38030910` | 13,264,172,619 bytes (whole set; India-only S3 zip is 403) | 9,665 India | potholes, cracks (road surface) | CC BY 4.0 | no |
| e-Yantra Indian roads | `https://www.kaggle.com/datasets/eyantraiit/semantic-segmentation-datasets-of-indian-roads` | 7,073,614,191 bytes | ~3,227 labelled (UNVERIFIED) | `footpath`, `pothole`, `road`, `shallow path` | GPL 2 | Kaggle login |
| MahaRoadNet (Pune) | `https://data.mendeley.com/datasets/ycgcv8tk23` | 1,843,637,240 bytes | 523 | potholes, includes night with street lights | CC BY 4.0 | no |
| DataCluster footpath sample | `https://www.kaggle.com/datasets/dataclusterlabs/footpath-dataset` | 163,181,439 bytes | ~100 free | footpath boxes, day + night, "200+ Indian cities" | Kaggle says CC0, vendor says owned | Kaggle login |
| IRDID | `https://github.com/ahs695/Indian-Road-Damage-Infrastructure-Dataset` | small | 1,200 | open manhole, waterlogging, broken road edge | claims CC BY 4.0 but its own metadata lists news/stock/Google sources | no; licence unsafe |
| FootpathVision (Dhaka, not India) | `https://data.mendeley.com/datasets/szkhrh8dc8/1` | 4,618,969,012 bytes | 1,238 | encroached vs clear footpaths | CC BY 4.0 | no |

Not downloaded tonight (sizes 1.8 to 24 GB on a slow link; brief said small samples only).

## 8. Licence rules for the demo (one table to follow)

| source | can show in the demo | can train/fine-tune | must do |
|---|---|---|---|
| Commons CC0 / PD | yes | yes | nothing (credit is polite) |
| Commons CC BY x | yes | yes | name author + licence + link (sidecar has all three) |
| Commons / Mapillary / Panoramax CC BY-SA x | yes | yes; derived images (crops, overlays) must stay CC BY-SA | attribution + share-alike on derived images |
| Project Sidewalk labels | yes | yes | cite CHI 2019 paper (requested, CC0 does not require) |
| Project Sidewalk image crops | no | no | they are Google Street View |
| YouTube frames, CC BY videos (youtube-cc) | yes | yes | credit channel + video URL (sidecar has both) |
| YouTube frames, standard licence (youtube, youtube-storyboard) | internal demo with on-screen credit; risky for a public site | no | ask the creator before public release; prefer CC sources on the public page |
| Reddit / X / news photos | no (link out instead) | no | permission from the poster |

## 9. Not-found and blocked ledger

| item | status | what would unblock it |
|---|---|---|
| Mapillary official API / tiles | token required (500 / 403) | free token from a Mapillary account (user's login) |
| KartaView 1.0 nearby | TLS ok, no response from this network | retry from another network |
| Flickr CC geotagged | API key required | free key (user's login) |
| YouTube segment download | 403, no JS runtime | install deno or yt-dlp-ejs (user GO) |
| CC-licensed walking tours for Bengaluru, Chennai, Kolkata, Pune, Chandigarh, Shimla | CC filter searched only 4 queries (India, street, Mumbai, Delhi) | run the CC filter search per city |
| Reddit images | JSON 403, RSS 429 | official Reddit API app (user's login) or manual picks with OP permission |
| grievance-portal photos | no public gallery found on 9 portals | RTI or a data partnership |
| Mapillary true per-city image totals | layer caps at ~50 per call and `returnCountOnly` is fake | official token + tiles, or a finer grid |
| village street imagery | Mapillary MUJ box: 2 images (2017); Bagru box hit the highway; YouTube has 2 rain-village walks | a finer village list from OSM `place=village` + the Esri relay |

## 10. Red team of this file

| claim | grade | check |
|---|---|---|
| Mapillary reachable with no token via Esri layer | VERIFIED | 43 + pair images downloaded; item JSON says `access: public` |
| Esri layer allows reuse | UNVERIFIED in detail | item says content "subject to Mapillary's Terms of Use"; Mapillary imagery licence is CC BY-SA 4.0 (helper cites help.mapillary.com); the Esri relay terms themselves not read |
| `maxres1/2/3` = frames at 25/50/75 % | UNVERIFIED (position) / VERIFIED (they are in-video frames) | viewed 84 frames; positions not published by YouTube |
| storyboard interval 9.93 s | VERIFIED | computed from `1/fps` of sb0 for 3 videos |
| 3,347 Chandigarh labels all GSV | VERIFIED | counted `pano_source` values in the geojson |
| per-city Mapillary coverage | floors only | 50-record cap per query; "cells with imagery" is the honest unit |
| condition tags | starter labels | assigned by eye at 256 px; luminance threshold for YouTube day/night |
| city of each YouTube frame | from the video title | two flagged for a human check |
| Panoramax India "mostly POI shots" | VERIFIED for the 20 pulled | 13 of 20 are menus/interiors/food; larger sample not checked |
| counts in section 0 and 6 | VERIFIED | generated by `build_manifest.py` from sidecars on disk, not typed |
| 12 videos are CC BY | VERIFIED (flag) / UNVERIFIED (uploader owns all footage) | yt-dlp `license` field read per video; a CC flag is the uploader's claim |
| Mapillary pairs show the "same spot" | PARTLY | within 30 m by GPS; only 3 of 16 match the view well by eye, 2 fair, 11 weak |
| per-cell coverage "cells with imagery" | VERIFIED as floors | 4 x 4 grid, 1 query per cell, 50-record cap; Puri's 45 images sit in 1 cell |
| night count 55 | VERIFIED after correction | first pass used a luminance threshold that called lit night markets "day"; 29 sidecars corrected by eye |

Mistakes made during the run (logged, fixed): commons harvest first hit Commons rate limits (retry loop added); Panoramax probe first died on partial reads (retry + smaller pages); Mapillary grid script first failed to import its helper under `python3 -I` (path fix); a Reddit retry with longer waits was refused by the permission layer as rate-limit evasion, so Reddit stopped at the blocked state above; the YouTube day/night tag first came from a brightness threshold that labelled lit night markets as day (29 sidecars corrected by eye); my first claim "no CC Indian walking tours" was wrong and was replaced after the CC-filter search worked.

## 11. Next steps (need the user's GO where marked)

1. (GO: install) deno or yt-dlp-ejs so true 10 s frames at 720p can be cut from 3-4 videos (night, rain, market, hill).
2. Use the Esri relay with a 10 x 10 grid on the demo cities to build the "known / unknown coverage" layer from ARCHITECTURE-v1 (dates per cell feed the "photo date" tier).
3. Pull more Mapillary same-spot pairs for the "same kerb, different sky" slider (real pairs instead of simulated).
4. Overlay Project Sidewalk Chandigarh CC0 labels on the OSM walk graph as barrier priors (3,347 points, 9 label types).
5. (GO: logins) Mapillary token and Flickr key, both free, both need the user's account.
