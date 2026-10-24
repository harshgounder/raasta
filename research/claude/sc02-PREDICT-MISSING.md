# SC-02: predicting what we cannot see (v1, 2026-10-24 ~16:45 IST, claude)

Scope: every factor SC-02 needs (D) that no street photo gives us (A), and the math / stats / ML that can PREDICT it for any place in India, any hour, any season. Inputs read in full before writing: `research/WAVE-2-SC02-BRIEF.md` (4,903 B), `DECISIONS.md` (1,892 B), `method/COPYPASTE-METHOD.md` (4,755 B), `method/LUNAR-TIE-FOR-SC02.md` (2,948 B). Total 14,498 B read, matches `wc -c`.
Overlap check: `research/claude/sc02-SOTA.md` and `sc02-PARTS.md` already cover the detectors, depth, map matching repos and routing engines. This file does not repeat them; it covers the PREDICTION layer around them.

## Grades used

| grade | meaning |
|---|---|
| VERIFIED | page opened with web_fetch in this session (2026-10-24, 16:20-16:40 IST) and the claim is on that page |
| SEEN | URL came back in a live web_search this session; claim is from the search excerpt, page not opened |
| UNVERIFIED | from my memory or inference; not checked this session |
| COMPUTED | number computed by a script in this session (shown inline) |

Rule from DECISIONS D2 kept everywhere: a predicted value is a prior with an error bar, shown as "inferred", never as "observed", and a segment with no evidence stays "unknown", never "safe" (LUNAR-TIE 4-layer contract: raw evidence / geometry + covariance / residual / prior-flagged preview).

## The common skeleton (one model, many factors)

Every factor below plugs into the same per-segment belief, so the build is one pipeline, not 20 projects:

```
              covariates x_s (free, all-India)                 photos (when they exist)
  OSM tags, POI mix, road class, Open Buildings height,          detector A + detector B
  canopy height, DEM/HAND, AEF 64-d embedding, VIIRS,            (agreement = confidence)
  IMD rain today, hour-of-day, month                                     |
            |                                                            v
            v                                                   likelihood p(photo | z_s)
   prior p(z_s | x_s)  --- spatial smoothing over the graph --->  posterior p(z_s | data)
   (logistic / GBDT / GP)    (graph Matern GP, label propagation,        |
                              hierarchical pooling by ward/city)         v
                                                            conformal ACCEPT / ABSTAIN / REJECT
                                                                         |
                                                                         v
                                      edge cost = E[cost] or CVaR_alpha[cost], plus "unknown" flag
                                                                         |
                                                                         v
                                      risk-averse route  +  "best next photo" (value of information)
```

z_s = the hidden state of segment s (footpath exists, width class, blocked now, waterlogged now, shaded now, lit now, kerb ok). Photos update it; covariates set its prior.

---

## F1. Footpath existence and width where no street image exists

**Method.** (a) Semantic segmentation of aerial / satellite tiles into sidewalk, crosswalk, road, then polygon to centreline network (Tile2Net). (b) Cross-view fusion of satellite + street view for occluded sidewalks. (c) A graph model that spreads evidence along the street (RoadTagger: CNN on tiles + GNN on the road graph). (d) For India where sidewalks are often absent or informal, a prior p(footpath | road class, building density, ward) learned from our own labels and the Chandigarh / Pune data.

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| Hosseini et al., Tile2Net, "Mapping the walk", CEUS 101:101950 | 2023 | https://www.sciencedirect.com/science/article/pii/S0198971523000133 | VERIFIED (trained on Cambridge, DC, NYC orthophotos; model weights public) | https://github.com/VIDA-NYU/tile2net VERIFIED (beta, PyTorch 2, "not yet ready for production") |
| Esri Pedestrian Infrastructure Classification (Tile2Net architecture), sidewalk IoU 82.67 | 2024-2026 | https://www.arcgis.com/home/item.html?id=c0d520baa30d4b47ab36232231c17875 | SEEN | ArcGIS model |
| DB-Net, cross-view satellite + street view sidewalk segmentation, ISPRS J. | 2026 | https://www.sciencedirect.com/science/article/abs/pii/S0924271626003503 | SEEN | not seen |
| He et al., RoadTagger: road attribute inference with GNNs (AAAI 2020) | 2019/2020 | https://arxiv.org/abs/1912.12408 | SEEN | https://github.com/mitroadmaps/roadtagger VERIFIED (pretrained model + docker) |
| Verma, Ukkusuri, crosswalk detection from satellite for pedestrian network completion, TRR | 2023 | https://journals.sagepub.com/doi/10.1177/03611981231210545 | SEEN | no |
| Pedestrianfer / OASIS-style inference of a sidewalk graph from the street graph (arXiv 2410.19762) | 2024 | https://arxiv.org/pdf/2410.19762 | SEEN | unknown |
| Hamim, Kancharla, Ukkusuri, sidewalk mapping from street view in Bangladesh (local labels lift IoU) | 2024 | https://journals.sagepub.com/doi/10.1177/23998083231200445 | SEEN | no |

**Data and India status.**
| need | Indian / all-India source | status |
|---|---|---|
| sub-metre RGB tiles | Bhuvan high-res basemap (WMS), Esri / Google / Bing tiles (terms limit bulk ML use) | UNVERIFIED for licence; Tile2Net was trained on US orthophotos, India transfer is unknown and probably weak (tree cover, no planimetric labels) |
| labels for India | Indian Footpath Damage Segmentation Dataset (583 images, Pune), e-Yantra IIT Bombay Indian Roads (footpath class, 3,227 images), Chandigarh Project Sidewalk deployment (arXiv 2602.09216) | SEEN (Zenodo 15414238, Sci Data 2025; datasetninja); 2602.09216 page opened but abstract not in extract, so its content is SEEN only |
| OSM footway tags | OSM India | **test not run**: Overpass query for Jaipur/MUJ bbox failed because the Bash sandbox blocks outbound network (curl error 7). Command is in the log below for anyone to run |

**SC-02 use.** Tonight: no Tile2Net run (US-trained, GPU time, tiles licence). Instead a cheap prior: p(footpath exists | OSM highway class, building density from Open Buildings, distance to market POIs), shown as "inferred, 0.xx". Later: fine-tune Tile2Net on 200 hand-labelled Jaipur tiles and fuse with street-view detections (DB-Net idea).

## F2. OSM completeness (how much of the map is missing at all)

**Method.** Regress true quantity (building area, road length) on free covariates (population GHS-POP, night lights, land cover) with random forests, then completeness = OSM / predicted (Herfort 2023). Older: multilevel regression + poststratification on visual audits, plus sigmoid saturation of contribution curves (Barrington-Leigh and Millard-Ball 2017).

| paper | year | URL | grade | code |
|---|---|---|---|---|
| Herfort et al., global urban building completeness in OSM, Nat Commun 14:3985 (random forest over 13,189 urban centres; India "hardly mapped") | 2023 | https://www.nature.com/articles/s41467-023-39698-6 | VERIFIED (code + data on figshare 10.6084/m9.figshare.22241776 / 22217038) | yes |
| HeiGIT update with new data (South Asia 7-17% completeness band) | 2024 | https://heigit.org/analysis-of-osm-building-data-completeness-using-new-data | SEEN | - |
| Barrington-Leigh, Millard-Ball, "The world's user-generated road map is more than 80% complete", PLOS ONE | 2017 | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0180698 | VERIFIED (MRP + sigmoid saturation) | data public |

**India data.** GHS-POP, VIIRS (VNL), ESA WorldCover are global (cited in Herfort, VERIFIED as inputs). Google Open Buildings v3 and Microsoft footprints both cover India: India has 151 M buildings in Microsoft vs 514 M in Google per a 2025 comparison (SEEN, https://pmc.ncbi.nlm.nih.gov/articles/PMC12559435/).
**SC-02 use.** Tonight: one number per city on the site: "OSM here has X km of footways for Y km of roads", with the Herfort completeness for the urban centre as context. It tells the judge why "no data" is the normal case in India. Later: a footway-completeness model per ward, same RF recipe with footway length as target.

## F3. Kerb height and slope where no photo exists

**Honest physics first (COMPUTED).** DEM pixels cannot see a 15 cm kerb. For slope between two DEM samples L metres apart, 1-sigma slope error = sqrt(2) * sigma_z / L (independent errors, a pessimistic case since real DEM errors are correlated):

| DEM (stated accuracy) | sigma_z | L = 30 m | L = 100 m | L = 300 m |
|---|---|---|---|---|
| Copernicus GLO-30, relative < 2 m LE90 | 1.22 m | 5.73 % | 1.72 % | 0.57 % |
| CartoDEM, relative > 5 m LE90 | 3.04 m | 14.33 % | 4.30 % | 1.43 % |
| CartoDEM, absolute 8 m LE90 | 4.86 m | 22.93 % | 6.88 % | 2.29 % |

The ramp limit (8.33 % for new ADA curb ramps, archive.ada.gov, SEEN) is smaller than the 30 m error. So: DEM gives **street-scale running grade over 100-300 m**, never kerb height, never ramp slope. CartoDEM is also a **surface** model (rooftops, trees included), per the NRSC spec sheet: "although this is termed CartoDEM, it is a DSM" (SEEN, https://bhoonidhi.nrsc.gov.in/bhoonidhi_resources/help/sampleprods/Cartosat-1/DEM/CartoDEM-Specs.pdf).

**Methods for the kerb itself.**
- Monocular metric depth or homography on the photo (in sc02-SOTA, not repeated).
- Where photos exist on some kerbs of a street: Gaussian process / kriging over the street graph. Kerbs on one street are usually cast by one contractor at one time, so heights are correlated along the street. Graph Matern GP (Borovitskiy et al., AISTATS 2021) gives mean + variance at unphotographed kerbs; edge-GPs (Hodge-compositional, AISTATS 2024) model values on edges directly.
- Hierarchical pooling: kerb height ~ Normal(mu_street, tau_street), mu_street ~ Normal(mu_ward, tau_ward), mu_ward ~ Normal(mu_city, ...). A single new photo on a street moves every kerb on it.

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| Borovitskiy et al., Matern Gaussian Processes on Graphs | 2020/2021 (v4 2026-05) | https://arxiv.org/abs/2010.15538 | VERIFIED | https://github.com/spbu-math-cs/Graph-Gaussian-Processes (SEEN in PDF excerpt) |
| Yang, Borovitskiy, Isufi, Hodge-Compositional Edge GPs | 2024 | https://proceedings.mlr.press/v238/yang24e.html | SEEN | project page linked |
| NeRF vs LiDAR for ADA sidewalk slopes, mean abs diff 0.49 deg cross slope | 2025 | https://www.mdpi.com/2412-3811/10/8/191 | SEEN | - |
| Ai and Tsai, mobile LiDAR ADA sidewalk assessment, TRR 2542 | 2016 | https://journals.sagepub.com/doi/10.3141/2542-04 | SEEN | - |
| CartoDEM validation (flat terrain abs height accuracy 4.7 m), JISRS | 2012 | https://link.springer.com/article/10.1007/s12524-012-0212-9 | SEEN | - |

**India data.** CartoDEM V3R1 1 arc-sec (~32 m) free tiles on Bhuvan (VERIFIED, https://bhuvan-app1.nrsc.gov.in/2dresources/bhuvanstore.php); 10 m CartoDEM is priced (SEEN, NRSC policy page). Copernicus GLO-30, SRTM, ALOS AW3D30 are global (UNVERIFIED this session for download route; standard knowledge).
**SC-02 use.** Tonight: running grade per long edge from GLO-30 or CartoDEM with the error bar from the table above, flagged "terrain grade, not kerb". Kerb height: Class III without a photo, said out loud on the site. If 2+ kerbs on one campus street are photographed, a 30-line GP / hierarchical normal model fills the rest with a variance band. Later: phone LiDAR (iPhone Pro) as ground truth.

## F4. Probability a footpath is blocked by vendors or parked vehicles at a given hour

**Method.** Model the count of blocking objects on segment s at hour h as a point process with intensity
`lambda(s, h, d) = exp(beta . x_s) * g_category(h, d)`
where x_s = POI mix within 100 m (shops, markets, schools, temples, hospitals, metro/bus stops), road class, building density, land use; g = diurnal / weekly profile per POI category; d = day type (weekday, Sunday, festival). Then `P(blocked) = 1 - exp(-lambda * dt)`. Inhomogeneous Poisson is the floor; a Hawkes term adds self-excitation (one vendor cart draws others; a wedding procession clusters parking). Fit with photo timestamps as events once they exist.
Evidence this works for parking: NYC parking-ticket legality prediction with POI + mobility features, random forest F1 0.82-0.90 across four spatial scales (VERIFIED); Thessaloniki deep residual nets for violation rate (SEEN); Google Popular Times alone predicts road traffic counts in Budapest and Kyoto (VERIFIED).

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| Spatiotemporal legality of on-street parking from open data + ML, Annals of GIS (authors not checked) | 2019 | https://www.tandfonline.com/doi/full/10.1080/19475683.2019.1679882 | VERIFIED | - |
| Deep learning for on-street parking violation prediction (Thessaloniki) | 2022 / 2025 | https://arxiv.org/abs/2505.06818 | SEEN | - |
| Data-driven crowdsensing framework for parking violation detection (data completion for unsensed areas), IEEE TMC | 2024 | https://www.computer.org/csdl/journal/tm/2024/06/10315026/1RXVFg3qevC | SEEN | - |
| Estimating traffic from Google Popular Times, Transp. Res. Interdiscip. Persp. | 2026 | https://www.sciencedirect.com/science/article/pii/S2590198226001387 | VERIFIED | - |
| Spatio-temporal Hawkes point processes: a review, JABES | 2024 | https://link.springer.com/article/10.1007/s13253-024-00653-7 | SEEN | - |
| Likelihood-free spatiotemporal Hawkes with missing data (unreported events) | 2025 | https://arxiv.org/pdf/2502.07111 | SEEN | - |
| tick (Hawkes simulation + inference), hawkeslib, HawkesPyLib | - | https://github.com/X-DataInitiative/tick , https://pypi.org/project/hawkeslib , https://pypi.org/project/HawkesPyLib | SEEN | yes |

**India data.** OSM POIs (all India, sparse in places). Street Vendors Act 2014 makes Town Vending Committees survey vendors at least once every 5 years and designate vending zones (SEEN, indiacode / mohua PDFs), so vending-zone lists exist per city in principle; only 1,341 of 4,315 towns had framed vending plans by 2021 (SEEN, PRS committee summary). PM SVANidhi: 53,76,074 identified vendors nationally, state-wise only, not district-wise (SEEN, Lok Sabha SQ 318, 2023). Google Popular Times: shown in Maps from opted-in Location History (SEEN, Google help); no official API, scraping is against terms (UNVERIFIED legal status, treat as off-limits).
**SC-02 use.** Tonight: parametric lambda with hand-set diurnal curves per POI category (stated as a prior, not fitted), slider "leave at 10:00 / 18:00 / 21:00" changes which segments go amber. Very visible, about 60 lines. Later: fit beta and the Hawkes kernel from timestamped user photos (each photo = observation of presence/absence at (s, t)).

## F5. Waterlogging probability in monsoon

**Method.** Terrain: fill sinks, flow direction, flow accumulation, HAND (height above nearest drainage); low HAND + high accumulation + impervious surface = ponding. Then a susceptibility model (logistic / RF / XGBoost with SHAP) on known waterlogging points, and a rain trigger: `P(waterlogged_s | today) = sigmoid(a + b*log(rain_24h) + c*HAND_s + d*flowacc_s + e*impervious_s)`. All-weather validation from Sentinel-1 SAR (clouds do not block radar).

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| GIS-AHP waterlogging susceptibility in Delhi, 10 factors (rainfall weight 24.5 %, flow accumulation, drainage distance) | 2026-10 | https://www.tandfonline.com/doi/full/10.1080/23789689.2026.2744500 | SEEN | - |
| Urban waterlogging risk in North Delhi, 19 parameters at ward scale, Acta Geophysica | 2024 | https://link.springer.com/article/10.1007/s11600-024-01336-0 | SEEN | - |
| Explainable ML waterlogging with negative-sampling strategies, IJDRR | 2026 | https://www.sciencedirect.com/science/article/pii/S2212420925008027 | SEEN | - |
| Feature-selection + interpretable ML waterlogging (AUC 0.846), J Env Mgmt | 2025 | https://pubmed.ncbi.nlm.nih.gov/40882273 | SEEN | - |
| HAND terrain enhancements, Water Resources Research | 2019 | https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019WR024837 | SEEN | - |
| GRASS r.hand addon (HAND + inundation for given water levels) | 2026 | https://grass.osgeo.org/grass-stable/manuals/addons/r.hand.html | VERIFIED | yes |
| Sen1Floods11, Sentinel-1 flood dataset (CVPRW 2020) | 2020 | https://github.com/EOEPCA/Sen1Floods11-Dataset | VERIFIED | dataset + code |
| Mumbai urban floods 2018-2025 from Sentinel-1 (VV+VH, 10 m) | 2026 | https://www.mdpi.com/2673-4834/7/3/91 | SEEN | - |
| Global Flood Database v1, 913 events 2000-2018 at 250 m, CC BY-NC 4.0 | 2021 | https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1 | VERIFIED | Earth Engine |

**India data (checked).**
| source | what | grade |
|---|---|---|
| IMD 0.25 deg daily gridded rainfall, 1901-2024, NetCDF (Pai et al. 2014) | 0.25 deg = 24.8 km x 27.6 km at Jaipur's latitude (COMPUTED): a district-scale trigger, not a street-scale one | VERIFIED https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html |
| imdlib: archive + provisional real-time 0.25 deg rain + GPM rain, clip by district | `imd.load('rain', '2026-10-01', '2026-10-05', source='realtime')` | VERIFIED https://imdlib.readthedocs.io/en/latest/Usage.html |
| IMD API list: district-wise nowcast, station nowcast, AWS/ARG data, district warnings, district rainfall | access terms (IP whitelisting or key) not on page | VERIFIED list, access UNVERIFIED https://api.imd.gov.in/public/api_reference.html |
| Bhuvan Flood Hazard Zones (1998-2019 inundation frequency) | **only 6 states: Andhra Pradesh, Assam, Bihar, Odisha, Uttar Pradesh, West Bengal. No Rajasthan.** River floods mostly; flash floods "may not have been captured" | VERIFIED https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood_hz/flood_hz.php?uname=empty |
| CartoDEM V3R1 30 m (Bhuvan), Copernicus GLO-30 | terrain inputs | VERIFIED (CartoDEM listing) |

**SC-02 use.** Tonight: HAND + flow accumulation on a 30 m DEM for the demo area (pysheds or richdem or GRASS r.hand), joined to edges; multiply by the IMD real-time rain for the district via imdlib. Demo line: "it rained 64 mm in Jaipur district today, these 3 underpass segments are likely under water". Honest caveat on site: 30 m DEM misses kerb-scale drains, choked drains are invisible (Class III). Later: train on geotagged waterlogging reports (news, municipal complaint portals, user photos) with Sentinel-1 scenes from monsoon dates as extra positives.

## F6. Pothole and surface decay emergence over time

**Method.** Survival / hazard models: time until a segment crosses a distress threshold. Markov condition-state chains with Weibull or Bayesian-estimated hazard rates (the dominant family in pavement management), plus covariates (traffic, monsoon rainfall, age since last resurfacing). Pothole-specific ML: RF / kNN on condition indicators (London: 55.5 % of pothole sections and 99.6 % of non-pothole sections predicted, SEEN).

| paper | year | URL | grade |
|---|---|---|---|
| Markov deterioration hazard model with monsoon rainfall, Nepal national highways (Bayesian estimation; average bituminous life 4.22 years; rain interpolated with IDW vs Empirical Bayesian Kriging 3D) | 2025 | https://www.mdpi.com/2412-3811/10/3/52 | VERIFIED |
| Review: pavement performance models (Weibull, Markov-Weibull, Kaplan-Meier, Bayesian) | 2023 | https://www.maxapress.com/data/article/dts/preview/pdf/DTS-2023-0021.pdf | SEEN |
| Review: stochastic pavement deterioration models (Markov, semi-Markov, Bayesian, GPR) | 2025 | https://www.sciencedirect.com/science/article/pii/S1110016825002005 | SEEN |
| Survival analysis on LTPP asphalt fatigue cracking | 2022 | https://www.mdpi.com/2071-1050/14/19/12408 | SEEN |
| Pothole prediction with RF and kNN on condition indicators (Transport for London) | 2025 | https://www.sciencedirect.com/org/science/article/abs/pii/S0965092X25000350 | SEEN |
| Bayesian neural network + cuckoo search for probabilistic deterioration | 2025 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11906751 | SEEN |

**India data.** No open footpath condition time series found. Road age: not open nationally (UNVERIFIED; PMGSY rural road data exists via OMMAS but it is rural roads, not urban footpaths). Rain: IMD grid (VERIFIED). Proxy for "age": change detection between yearly Google Open Buildings 2.5D Temporal rasters (new construction nearby means recent digging) and AEF embedding drift between years (see F14).
**SC-02 use.** Tonight: not a model, a sentence and a curve: "a surface marked fair in October has a Y % chance of turning poor by next monsoon" using a two-state Markov chain with a transition rate taken from the Nepal paper as a stated borrowed prior (label it borrowed). Later: fit our own rates from repeat photos of the same segment.

## F7. Barrier persistence / half-life (is the photo from March still true tonight?)

**Method.** Each barrier type gets a survival function S(t) = P(still present t days after last seen). Exponential (constant hazard) as floor: half-life t_half = ln 2 / h. Types differ by orders of magnitude: parked car (hours), vendor cart (daily cycle, see F4), construction debris (weeks), pole / step / missing ramp (years). Kaplan-Meier on repeat observations of the same spot; Cox model for covariates. Change detection between repeat street images gives the events (CityPulse).
Then the segment belief decays toward the prior: `p_now = p_prior + (p_last - p_prior) * S(t)`.

| paper | year | URL | grade |
|---|---|---|---|
| Huang et al., CityPulse: urban change with street view time series (AAAI 2024; ~1,000 coordinates, 6 cities, avg 10 images over 16 years) | 2024 | https://arxiv.org/abs/2401.01107 | VERIFIED (title/authors), method details SEEN |
| Ma, Li, Long, temporal evolution of urban physical disorder, 20 M Chinese street view images 2013-2022, YOLOv8 for 14 elements | 2025 | https://www.tandfonline.com/doi/full/10.1080/24694452.2025.2467330 | SEEN |
| Curtis et al., spatio-temporal instability of GSV imagery dates (82.4 % of date changes within 25 m of intersections) | 2013 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3923560 | SEEN |

**India data.** Mapillary / KartaView sequences where they exist (covered by dsh lane), own repeat phone photos. No India barrier-duration dataset found (logged as zero).
**SC-02 use.** Tonight: hand-set half-lives per class (car 2 h, vendor 1 day with diurnal return, debris 14 days, pole / step permanent), stated as assumptions, used to fade old photos on the map ("seen 9 days ago, 63 % still there"). Very cheap, very legible. Later: estimate hazards from repeat photos (Kaplan-Meier).

## F8. Streetlight presence and night safety

**Method.** Satellite night lights give area brightness, not lamp positions: VIIRS DNB pixels are 750 m, Black Marble VNP46 products 500 m (VERIFIED). One DNB pixel is 0.56 km2 (COMPUTED), many streets. So: (a) VIIRS as a coarse prior; (b) streetlight poles detected in daytime street view (YOLO + depth + triangulation, Hong Kong 2026, SEEN; StreetScouting AP 0.841 for lights, SEEN); (c) night street view to model lit fraction (Fan and Biljecki 2024, VERIFIED); (d) VLM-rated perceived safety from street views (cited as validated in a 2026 paper, SEEN).

| paper / data | year | URL | grade |
|---|---|---|---|
| NASA Black Marble VNP46 (daily / monthly / yearly night lights) | 2018- | https://www.earthdata.nasa.gov/data/projects/black-marble | VERIFIED |
| Fan, Biljecki, Nighttime street view imagery for urban lighting, Sust. Cities Soc. 116:105862 | 2024 | https://ual.sg/publication/2024-scs-night-svi/2024-scs-night-svi.pdf | VERIFIED |
| Nightlight-nightlife interplay: lighting thresholds vs perceived safety (image lighting proxies IU, AVGIL, SPOT) | 2026 | https://www.sciencedirect.com/science/article/pii/S1569843226000622 | SEEN |
| Streetlight detection + geolocation from GSV (YOLOv5x + depth + triangulation) | 2026 | https://www.sciencedirect.com/science/article/pii/S0960148125026151 | SEEN |

**India data.** VIIRS covers India (global). Streetlight inventories: some smart-city / EESL Street Lighting National Programme dashboards (UNVERIFIED, not checked). OSM `highway=street_lamp` and `lit=yes` tags are sparse (UNVERIFIED, Overpass test blocked).
**SC-02 use.** Tonight: per-segment "night" factor = VIIRS radiance percentile (coarse) combined with `lit=*` where tagged, plus detector counts of lamp poles in any daytime photo. Show as a night toggle that turns dark segments grey "unknown at night" (Class III unless a lamp is seen). Later: night photos from users, brightness proxies from Fan and Biljecki.

## F9. Crowding (pedestrian density on the footpath)

**Method.** Direct-demand models: pedestrian count ~ POI density + street-view pixel classes + network centrality (betweenness from OSMnx). Predicting walking counts at 4,145 US count sites from GSV + POI (SEEN); deep model for pedestrian flow from GSV detections (SEEN); Popular Times to traffic (VERIFIED, F4).

| paper | year | URL | grade |
|---|---|---|---|
| Predicting bicycling and walking traffic from street view and destination data, Transp. Res. D | 2021 | https://www.sciencedirect.com/science/article/abs/pii/S1361920920308361 | SEEN |
| Predicting urban vitality / pedestrian flows with deep learning on GSV detections (Smart Cities 8(2):58) | 2025 | https://www.mdpi.com/2624-6511/8/2/58 | SEEN |
| Pedestrian dynamics from real-time urban sensors with ML, EPB | 2025 | https://journals.sagepub.com/doi/full/10.1177/23998083251319058 | SEEN |

**India data.** Census 2011 ward population (old), WorldPop / GHS-POP 100 m (global, UNVERIFIED download today), OSM POIs, betweenness from OSM. Mobile operator data: not open.
**SC-02 use.** Tonight: betweenness centrality x POI density as a "busy" index, time-scaled by the same diurnal curves as F4. Matters most for blind users and wheelchair users (width left). Later: count people in user photos (detector already runs) as observations.

## F10. Heat and shade

**Method.** Physics, not ML: sun position from (lat, lon, time) -> project shadows of buildings (height from Open Buildings 2.5D or Microsoft height layer) and trees (canopy height raster) onto footpath buffers; shade fraction per edge per hour; add LST for surface heat. CoolPaths (2026) does exactly this pipeline with pvlib + pybdshadow + 1 m canopy height + SRTM and routes to cooler paths (VERIFIED, code on GitHub).

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| CoolPaths: street-scale PET mapping and cooler routes from open data | 2026 | https://www.sciencedirect.com/science/article/pii/S2590252026000565 | VERIFIED | https://github.com/deepankverma/coolpaths (link VERIFIED on paper page) |
| pybdshadow: building shadows from sun position (suncalc), pip install | - | https://github.com/ni1o1/pybdshadow | VERIFIED | yes |
| Walking in the Shade: shadow-oriented pedestrian navigation (ray tracing on LoD2), SIGSPATIAL | 2024 | https://dl.acm.org/doi/10.1145/3678717.3691287 | SEEN | - |
| Kolaxidis et al., reducing solar exposure in pedestrian routing, Trans. GIS | 2025 | https://onlinelibrary.wiley.com/doi/full/10.1111/tgis.70110 | SEEN | - |
| ShadeRoute NYC (1.07 M footprints with heights, shade-weighted Dijkstra) | - | https://github.com/bapatakshay1/shade-route | SEEN | yes |
| Thermal-comfort pedestrian routing with LST + street vegetation, IJGI 15(7):313 | 2026 | https://www.mdpi.com/2220-9964/15/7/313 | SEEN | - |

**India data (checked).**
| source | what | grade |
|---|---|---|
| Google Open Buildings 2.5D Temporal: building presence, counts, **heights**, annual 2016-2023, 4 m effective, covers South Asia, CC BY 4.0 or ODbL | heights for India | VERIFIED https://sites.research.google/gr/open-buildings/temporal |
| Microsoft building density + height, global ~100 m (2020 Q4, 2023 Q4), CDLA-Permissive 2.0 | coarse heights | VERIFIED https://github.com/microsoft/buildings |
| Microsoft GlobalMLBuildingFootprints: India 110 M footprint edits in a 2024 update; height estimates exist for a subset | footprints | SEEN https://github.com/microsoft/GlobalMLBuildingFootprints |
| Meta / WRI 1 m canopy height (CC BY 4.0, AWS); CHMv2 with DINOv3 (arXiv 2603.06382, 2026) | tree shade | SEEN (WRI page opened but extract had no metadata; AWS registry excerpt SEEN) |
| Landsat Collection 2 Level-2 Surface Temperature (30 m resampled, no use restrictions) ; ECOSTRESS 70 m | LST | VERIFIED (USGS page) ; ECOSTRESS SEEN |

**SC-02 use.** Tonight: YES, top pick. Shade fraction per edge for "now" and for "2 pm in May", from Open Buildings heights + canopy + pybdshadow. Same sun math checks a photo's timestamp and heading (LUNAR-TIE P2). Later: PET with CoolPaths, LST from Landsat.

## F11. Missing images and occlusions

**Method.** Two different jobs; keep them apart (LUNAR-TIE honesty rule):
1. Estimate what is behind an occluder for the BELIEF: amodal segmentation (predict the full footpath mask under a parked car), or semantic-layout inpainting of dynamic objects. Output goes into the posterior as a soft label with lower weight.
2. Make a PREVIEW for people: diffusion inpainting / novel view synthesis, always stamped "reconstructed".

| paper | year | URL | grade | code |
|---|---|---|---|---|
| Xu et al., Amodal completion via progressive mixed context diffusion (CVPR 2024), training-free | 2024 | https://github.com/k8xu/amodal | SEEN | yes |
| pix2gestalt, zero-shot amodal segmentation by synthesis | 2024 | https://gestalt.cs.columbia.edu/ | SEEN | weights on HF |
| Amodal SAM (image + video) | 2026 | https://arxiv.org/abs/2604.20748 | SEEN | - |
| Segment Anything, Even Occluded (SAMEO, Amodal-LVIS 300 K) | 2025 | https://arxiv.org/abs/2503.06261 | SEEN | - |
| Tuning-free amodal segmentation via the occlusion-free bias of inpainting models, AAAI 2026 | 2026 | https://ojs.aaai.org/index.php/AAAI/article/view/37509/41471 | SEEN | - |
| Road layout recovery by inpainting dynamic objects in semantic maps (MICC-SRI) | ~2019 | https://flore.unifi.it/bitstream/2158/1195600/1/road_layout.pdf | SEEN | dataset |
| Segmentation of occluded sidewalks in satellite images (inpainting with priors), ICPR | 2012 | https://www.computer.org/csdl/proceedings-article/icpr/2012/06460256/12OmNx1qV3o | SEEN | - |

**SC-02 use.** Tonight: occlusion flag only ("footpath 40 % hidden by a parked car: the car IS the barrier; surface under it unknown"). Later: amodal mask under cars as a down-weighted observation; diffusion preview stamped "reconstructed".

## F12. Uncertainty in map matching (which segment does this photo belong to?)

**Method.** HMM: hidden state = candidate footpath segment, emission = Gaussian on distance from GPS fix to segment (sigma 5-15 m for phones), transition = penalty on |route distance - straight distance| between consecutive fixes (Newson and Krumm 2009). For one photo, skip Viterbi and keep the full posterior over nearby segments, add a heading term (camera bearing vs segment bearing) and a side-of-road term (left/right footpath from where the kerb sits in the image). Forward-backward gives a probability per segment for photo sequences.

| paper / tool | year | URL | grade | code |
|---|---|---|---|---|
| Newson, Krumm, Hidden Markov map matching through noise and sparseness, ACM SIGSPATIAL (test data released) | 2009 | https://www.microsoft.com/en-us/research/publication/hidden-markov-map-matching-noise-sparseness | VERIFIED | test set |
| Yang, Gidofalvi, Fast map matching (HMM + precomputed UBODT), IJGIS 32(3) | 2018 | https://www.tandfonline.com/doi/full/10.1080/13658816.2017.1400548 | SEEN | https://github.com/cyang-kth/fmm VERIFIED (C++/Python, FMM + STMatch, H3 hex match) |
| Enhanced HMM map matching for pedestrian navigation (EHMM-P), Electronics 13(9) | 2024 | https://www.mdpi.com/2079-9292/13/9/1685 | SEEN | - |
| Smartphone GNSS map matching comparison (Montreal; Fast HMM best) | 2025 | https://www.sciencedirect.com/science/article/pii/S2352146524003430 | SEEN | - |

**SC-02 use.** Tonight: YES. Per-photo posterior over the 3-5 nearest footpath segments with GPS sigma + heading; draw it as the "uncertainty cloud" (LUNAR-TIE P1). If the top segment has < 0.7 probability, ABSTAIN and ask the user to tap the side of the road. FMM is overkill for single photos; a 40-line numpy posterior is enough.

## F13. Graph-level prediction (fill the network from a few labelled streets)

**Method.** Barrier presence is spatially autocorrelated along streets and within wards. Options in rising cost:
1. Label propagation / harmonic functions on the street graph (Zhu, Ghahramani, Lafferty 2003, UNVERIFIED classic).
2. Graph Matern GP (F3): posterior mean + variance per edge, closed form for small graphs.
3. GNN on the road graph with image + covariate node features (RoadTagger, VERIFIED repo).
4. Hierarchical Bayesian pooling across segments, wards, cities: BYM2 spatial random effect (INLA), or a simple Beta-Binomial per ward with a city prior, so a ward with 3 photos borrows strength from the city and a city with 0 photos borrows from India-wide rates. Spatial MRP (Sutton, Almquist, Wakefield 2025, SEEN) and structured-prior MRP (Bayesian Analysis 2021, SEEN).
5. Transfer from labelled cities: Project Sidewalk now has 1,648,977 labels and 2,273,754 validations over 32,501 km (VERIFIED, API page) across 50+ cities in 10 countries including India (SEEN, GitHub README); cross-city training helps but degrades with distance (Duan et al. ASSETS 2022, SEEN; Weld et al. ASSETS 2019, SEEN). Geo-embeddings make "similar street" computable anywhere: AlphaEarth Foundations Satellite Embedding, 64-d per 10 m pixel, annual 2017+, CC BY 4.0 (VERIFIED, Earth Engine catalog), also mirrored on Source Cooperative (SEEN); SatCLIP location embeddings (AAAI 2025, SEEN).

| paper / tool | year | URL | grade |
|---|---|---|---|
| RoadTagger (CNN + GNN road attributes) | 2020 | https://github.com/mitroadmaps/roadtagger | VERIFIED |
| Matern GPs on graphs | 2021 | https://arxiv.org/abs/2010.15538 | VERIFIED |
| Spatial MRP with BYM2 priors | 2025 | https://arxiv.org/abs/2503.05915 | SEEN |
| Improving MRP with structured priors | 2021 | https://sites.stat.columbia.edu/gelman/research/published/improving_mrp.pdf | SEEN |
| survey::svysmoothArea (BYM2 via INLA, Fay-Herriot) | - | https://cran.r-project.org/web/packages//survey/vignettes/survey-sae.html | SEEN |
| AlphaEarth Satellite Embedding V1 | 2025 | https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL | VERIFIED |
| SatCLIP | 2023/2025 | https://www.microsoft.com/en-us/research/publication/satclip-global-general-purpose-location-embeddings-with-satellite-imagery | SEEN |
| Project Sidewalk fine-grained 33-tag benchmark + open dataset, ASSETS 2024 | 2024 | https://dl.acm.org/doi/10.1145/3663548.3688531 | SEEN |
| Chandigarh adaptation of Project Sidewalk with VLM-guided annotation (AAAI 2026) | 2026 | https://arxiv.org/abs/2602.09216 | SEEN (page opened, content not in extract) |

**SC-02 use.** Tonight: YES, as hierarchical Beta-Binomial + label propagation on the campus / demo graph. Every unphotographed segment gets a probability and a "how many photos is this based on" count. Later: AEF embeddings as node features so a Jaipur street with no photo borrows from a similar-looking Pune or Chandigarh street; GNN once we have >1,000 labelled segments.

## F14. Active learning: which photo should a user take next?

**Method.** Value of information on the ROUTE, not on the map. For candidate segment e with barrier probability p_e:
`VOI(e) = E_route_cost(now) - [ p_e * E_route_cost(e blocked) + (1-p_e) * E_route_cost(e clear) ]`
Ask for the photo with the highest VOI per metre of detour. This is the remote-sensing Canadian Traveller Problem (IJCAI 2009, VERIFIED: the VOI sensing policy was best in most of their test cases; author names not checked). For model training instead of routing, BALD (mutual information over an ensemble) picks images to label, as in UAV informative path planning (IEEE T-RO 2023, VERIFIED).

| paper | year | URL | grade |
|---|---|---|---|
| Canadian Traveler Problem with Remote Sensing, IJCAI (authors not checked) | 2009 | https://www.ijcai.org/Proceedings/09/Papers/080.pdf | VERIFIED |
| Informative path planning framework for active learning in UAV semantic mapping, IEEE T-RO (authors not checked) | 2023 | https://arxiv.org/pdf/2302.03347v3 | VERIFIED |
| Popovic et al., learning-based adaptive informative path planning survey, RAS | 2024 | https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/popovic2024jras.pdf | SEEN |
| Bayesian graph traversal (GP prior over node rewards and edge costs), Decision Analysis | 2026 | https://ideas.repec.org/a/inm/ordeca/v23y2026i1p11-27.html | SEEN |
| Evidential uncertainty sampling for active learning, Machine Learning | 2024 | https://link.springer.com/article/10.1007/s10994-024-06567-2 | SEEN |

**SC-02 use.** Tonight: YES. One button on the map: "the most useful photo you can take is HERE (it could save a wheelchair user a 400 m detour)". Brute-force VOI over the 20 most uncertain edges near the route is milliseconds on a campus graph.

## F15. Uncertainty-aware routing

**Method ladder.**
| level | objective | when |
|---|---|---|
| expected cost | min sum_e (len_e + penalty * p_e) | baseline |
| chance-constrained | min length s.t. P(no barrier on route) >= 1 - alpha; with independence, sum_e -log(1 - p_e) <= -log(1 - alpha), a resource-constrained shortest path | wheelchair users who cannot back-track |
| CVaR_alpha | min the mean of the worst alpha tail of route cost (cost includes detour if blocked) | "plan for a bad day" slider |
| worst-case (min-max) over an uncertainty set | edge cost in an interval; classic interval min-max is easy (Dagstuhl ATMOS 2017, SEEN) | unknown segments |
| adaptive with recourse (Canadian Traveller) | policy that re-plans when a barrier is discovered; Bayesian CTP with correlated edges (UAI 2017, VERIFIED) ; distributionally-safe adaptive routing with only confidence intervals on edge costs (Flajolet, Blandin, Jaillet, arXiv 1408.3374, VERIFIED) | live navigation |

Practical trick: a "dead-end" penalty. For a wheelchair, the cost of hitting a step is not the step, it is the detour back to the last junction plus the alternative, so penalty_e = expected backtrack length. This is the CTP recourse in one number.

| paper | year | URL | grade |
|---|---|---|---|
| Papadimitriou, Yannakakis, Shortest paths without a map (Canadian Traveller), TCS 84 | 1991 | https://sites.cs.ucsb.edu/~suri/cs235/Rlist/noMapNavigation.pdf | SEEN |
| Shortest path under uncertainty: exploration vs exploitation (BCTP, HSPD algorithm), UAI (authors not checked) | 2017 | https://www.auai.org/uai2017/proceedings/papers/26.pdf | VERIFIED |
| Flajolet, Blandin, Jaillet, adaptive routing under uncertainty with distributionally safe guarantees (Singapore data) | 2014/2016 | https://arxiv.org/abs/1408.3374 | VERIFIED |
| CTP on outerplanar graphs, MFCS | 2024 | https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.19/LIPIcs.MFCS.2024.19.pdf | SEEN |
| Risk-averse selfish routing with CVaR, IJCAI | 2026 | https://ijcai.org/proceedings/2026/0052.pdf | SEEN |
| Stochastic shortest path with on-time arrival reliability (PACE) | 2018 | https://www.computer.org/csdl/proceedings-article/mdm/2018/413301a040/12OmNwdL7l8 | SEEN |
| Bolten, Caspi, Personalized Pedestrian Network Analysis (AccessMap cost profiles), PLOS ONE | 2021 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7978374 | SEEN |
| Accessibility for Whom? disability-group barrier perceptions + OSMnx personalised routing, CHI 2025 | 2025 | https://dl.acm.org/doi/full/10.1145/3706598.3713421 | SEEN |

**SC-02 use.** Tonight: YES. Three routes side by side: shortest, expected-cost, "95 % sure" (chance-constrained, done as a weighted shortest path on -log(1-p) with a Lagrange multiplier sweep, 10 Dijkstra calls). Plus dead-end penalty. Later: true CTP policy with re-planning in the live app.

## F16. Calibrated confidence

**Method.** Split conformal on a held-out set of our own labelled Indian photos: score = 1 - p(true class); threshold at the ceil((n+1)(1-alpha))/n quantile; output a SET {barrier}, {clear}, {barrier, clear}. Set of size 2 = ABSTAIN ("needs a human look"); size 1 = ACCEPT/REJECT. Conformal risk control bounds the expected false-negative rate of barriers directly (what a wheelchair user cares about). For the graph layer, conformalised GNN (CF-GNN) gives coverage on node/edge predictions. Detector boxes: conformal object detection. Model uncertainty itself: deep ensembles or MC dropout; with two different detectors (LUNAR-TIE M5) we already have a 2-member ensemble for free.

| paper | year | URL | grade |
|---|---|---|---|
| Angelopoulos et al., Conformal Risk Control, ICLR 2024 (bounds FNR; example tasks in vision) | 2024 | https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html | VERIFIED page; abstract text from SEEN excerpt |
| Huang, Jin, Candes, Leskovec, CF-GNN (coverage on graphs, up to 74 % smaller sets), NeurIPS 2023 | 2023 | https://proceedings.neurips.cc/paper_files/paper/2023/hash/54a1495b06c4ee2f07184afb9a37abda-Abstract-Conference.html | VERIFIED |
| Clarkson, distribution-free prediction sets for node classification, ICML 2023 | 2023 | https://proceedings.mlr.press/v202/clarkson23a.html | SEEN |
| Zargarbashi et al., conformal prediction sets for GNNs, ICML 2023 | 2023 | https://proceedings.mlr.press/v202/h-zargarbashi23a.html | SEEN |
| Probabilistic object detection with conformal prediction, COPA 2026 | 2026 | https://proceedings.mlr.press/v329/ries26a.html | SEEN |
| Copula-based conformal prediction for object detection | 2024 | https://proceedings.mlr.press/v230/mukama24a.html | SEEN |
| Conformal risk training (CVaR-type risks end-to-end), NeurIPS 2025 | 2025 | https://openreview.net/forum?id=uBEiZd2P0K | SEEN |
| Gal, Ghahramani, Dropout as a Bayesian approximation, ICML | 2016 | https://proceedings.mlr.press/v48/gal16.html | VERIFIED |
| Lakshminarayanan et al., deep ensembles, NeurIPS | 2017 | https://proceedings.neurips.cc/paper_files/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html | SEEN |
| MC-CP: conformalised Monte Carlo dropout, AAAI 2024 | 2024 | https://ojs.aaai.org/index.php/AAAI/article/view/30084 | SEEN |

**Caveat that matters.** Conformal coverage holds only if calibration and test photos are exchangeable. Night, monsoon and a new city break that. So calibrate per condition bin (the LUNAR-TIE zoo-router bins: day/night/rain/fog/glare) = Mondrian conformal, and ABSTAIN loudly in a bin with too few calibration photos.
**SC-02 use.** Tonight: YES, split conformal per bin on 60-100 labelled campus photos (honest small n: with n = 60 and alpha = 0.1 the threshold is the 55th smallest score, ceil(61 * 0.9) = 55, COMPUTED by hand). Later: conformal risk control on FNR, CF-GNN on the graph.

## F17. Extra factors not in the brief (added)

| factor | prediction method | data | grade | tonight? |
|---|---|---|---|---|
| Open drain / missing slab next to footpath | street-view detection + prior from road class and building density | Indian Roads (e-Yantra) has "shallow" class (SEEN) | SEEN | prior only |
| Surface type under dust / water (smooth vs gravel) | photo classification + AEF embedding as prior | Project Sidewalk 33 tags (SEEN) | SEEN | later |
| Stray animals / cattle on footpath | Poisson with POI (dairy, temple, market) | none found | UNVERIFIED | no, Class III |
| Fog / smog visibility (Indo-Gangetic winter) | IMD visibility in API station data; CPCB AQI | IMD API list (VERIFIED list) | partial | later |
| Festival / procession closures | calendar features + city event lists into F4 lambda | no structured national feed found | UNVERIFIED | stated assumption |
| Construction digging (utility work) | yearly change in Open Buildings 2.5D Temporal + AEF embedding drift (dot product between years, per the catalog) | VERIFIED datasets | VERIFIED | later |
| GPS error itself (urban canyons) | sigma from building height around the point (Open Buildings) feeding F12 | VERIFIED dataset | inference UNVERIFIED | yes, 5 lines |

---

## The 8 picks: impressive AND doable tonight (17:00 to 02:30, GTX 1650 4 GB, 7 GB RAM)

Ranked by "a judge sees it in 10 seconds" times "fits in under 2 hours".

| # | prediction | math | inputs (all free, all-India) | est. effort | why a judge cares |
|---|---|---|---|---|---|
| 1 | Shade on every footpath edge, now and "2 pm in May" | sun position + building/tree shadow projection (pybdshadow, CoolPaths recipe) | Open Buildings 2.5D heights (VERIFIED), Meta canopy (SEEN), OSM edges | 1.5-2 h | heat kills in Indian summers; physics you can see move with a time slider |
| 2 | Waterlogging chance per edge given today's rain | HAND + flow accumulation from a 30 m DEM x IMD real-time district rain in a logistic link | CartoDEM / GLO-30 (VERIFIED listing), imdlib realtime (VERIFIED) | 1.5 h | monsoon is the Indian barrier; "it rained 64 mm today, avoid these 3" |
| 3 | Hourly blockage probability (vendors, parked bikes) | inhomogeneous Poisson lambda(s,h) from OSM POI mix x diurnal curves; P = 1 - e^(-lambda dt); Hawkes term described, not fitted | OSM POIs | 1 h | time slider turns market streets amber at 18:00: the "Indian street" moment |
| 4 | Fill unphotographed segments with honest probabilities | hierarchical Beta-Binomial (segment < street < ward) + label propagation on the street graph; show n photos behind each number | our labels, OSM graph | 1-1.5 h | "unknown" stays visibly unknown while neighbours inform it |
| 5 | Which segment a photo belongs to, with a cloud | per-photo HMM-style posterior (GPS Gaussian x heading x side-of-road), ABSTAIN under 0.7 | photo EXIF GPS + heading, OSM footways | 1 h | answers the statement's own key challenge (matching to the right segment) |
| 6 | "95 % sure" accessible route | chance-constrained shortest path via -log(1-p) weights + Lagrange sweep; plus dead-end (backtrack) penalty from CTP | outputs of 2-5 | 1 h | three routes side by side; the safe one is visibly different |
| 7 | "Best next photo" button | value of information on route cost over the 20 most uncertain edges (remote-sensing CTP) | outputs of 4 + 6 | 45 min | turns every user into a mapper; shows the system knows what it does not know |
| 8 | Calibrated ACCEPT / ABSTAIN / REJECT per detection, per condition bin | split conformal (Mondrian by day/night/rain bin), two detectors as a 2-member ensemble | 60-100 labelled campus photos | 1 h | "I am 92 % sure" or "needs a human look", with a coverage guarantee stated honestly |

Cheap add-ons if time is left: barrier half-life fading of old photos (F7, 20 min), DEM running grade with error bars (F3, 30 min), VIIRS night prior (F8, 30 min).
Not tonight: Tile2Net on Indian tiles, GNN, AEF transfer, pothole survival fit, amodal inpainting, Sentinel-1 flood training.

## Red-team of this file (trying to prove it wrong)

| claim | attack | verdict |
|---|---|---|
| "Open Buildings heights cover India" | page says "South Asia", does not list India by name | VERIFIED for South Asia; India inside South Asia is near-certain, still confirm by loading a Jaipur tile before building on it |
| "DEM cannot give kerb height" | maybe 2.5 m Cartosat DSM could | CartoDEM 2.5 m exists (NRSC 2024 slides, SEEN) but is a surface model and not free; the error table still kills kerb-scale use. Holds |
| "Bhuvan flood hazard has no Rajasthan" | maybe another Bhuvan layer covers it | VERIFIED for the flood hazard zone page (6 states listed). Other Bhuvan flood layers not checked: UNVERIFIED |
| "IMD API usable tonight" | access terms not on the page | UNVERIFIED; fall back to imdlib real-time grid, which is VERIFIED as a documented feature (not run here) |
| "hand-set diurnal curves are a prediction" | they are assumptions | EXAGGERATED if shown as fitted. Site must say "prior from POI type, not fitted yet" |
| "conformal gives a guarantee" | not under shift (night, rain, other city) | holds only within a bin with exchangeable calibration; stated in F16 |
| "Popular Times as a footfall source" | no API; scraping breaks terms | not used tonight; listed only as research evidence |
| "Overpass footway count for Jaipur" | not computed | test blocked by sandbox (curl error 7). No number given. Command below |
| Effort estimates | predictions, not measurements | UNVERIFIED, my guesses |
| Several papers marked SEEN | only search excerpts read | content claims for SEEN rows could be off; none of the 8 picks depends only on a SEEN source except Meta canopy (fallback: NDVI > 0.3 from Sentinel-2, as CoolPaths does, VERIFIED) |

## Coverage and zero-result log

- 26 web_search calls, 4 web_fetch calls (38 URLs opened, 38 returned; 3 returned thin extracts: WRI canopy page, arXiv 2602.09216, ICLR CRC page).
- Zero results / not found: an India dataset of barrier durations; an open India footpath condition time series; a national streetlight inventory feed (not searched deeply); an open festival / procession closure feed.
- Test not run: `curl --data-urlencode 'data=[out:json][timeout:50];(way["highway"="footway"](26.80,75.50,26.88,75.62);way["footway"="sidewalk"](26.80,75.50,26.88,75.62);way["sidewalk"](26.80,75.50,26.88,75.62););out tags;' https://overpass-api.de/api/interpreter` (Bash sandbox: no outbound network). dsh lane can run it.
- Numbers COMPUTED in this session: DEM slope errors (table F3), IMD grid size at 26.84 N, VIIRS pixel areas, conformal rank for n = 60.

## D minus A table (Set D = what SC-02 needs, Set A = what a street photo gives)

Class I = predict with a proxy (noise stated), Class II = absorbed by other variables, Class III = unavailable, say so on the site.

| factor | observed by (A) | predicted by (when not observed) | class | tonight? |
|---|---|---|---|---|
| footpath exists | photo + segmenter | OSM tags + building density prior (now); Tile2Net / DB-Net on aerial tiles (later) | I | prior only |
| footpath width | photo + metric depth | Tile2Net polygon width (later); road-class prior | I | prior only |
| kerb height | photo + depth | GP / hierarchical normal along the same street if 2+ kerbs seen; none otherwise | I where neighbours seen, III elsewhere | yes (campus) |
| kerb ramp present | photo detector | Beta-Binomial by street + junction type | I | yes |
| ramp / footpath slope (local) | photo + depth (weak) | none from DEM at < 30 m (COMPUTED errors) | III | no |
| street running grade (> 100 m) | not visible in photo | CartoDEM / GLO-30 with error bar | I | yes |
| steps / stairs | photo detector | building entrance prior from OSM | I | prior only |
| poles / fixed obstacles | photo detector | label propagation along street | I | yes |
| parked vehicles now | photo (if taken now) | Poisson lambda(s, h) from POI mix; half-life fade of old photos | I | yes |
| vendors now | photo (if taken now) | lambda(s, h) + vending-zone lists where a city publishes them | I | yes |
| waterlogging now | photo during rain | HAND + flow accumulation x IMD rain (logistic) | I | yes |
| choked drains | rarely visible | none | III | no (say so) |
| potholes / surface decay next season | photo (current state only) | Markov hazard with borrowed rate, monsoon rain covariate | I (borrowed prior) | sentence only |
| barrier still present (staleness) | repeat photo | survival S(t) per class, half-life fading | I | yes |
| shade / heat at hour h | photo shadows at capture time only | sun geometry + building/tree heights (pybdshadow); LST later | I (physics, low noise) | yes |
| lighting at night | night photo | VIIRS (750 m, coarse) + OSM lit + lamp-pole detection in day photos | I (coarse) / III without lamps seen | yes (coarse) |
| perceived safety at night | not from a day photo | VLM rating of night photos (later) | III tonight | no |
| crowding | person count in photo | betweenness x POI x diurnal curve | I | yes |
| surface under occluder | not visible | amodal segmentation (down-weighted); preview inpainting stamped "reconstructed" | I (weak) / III for truth | flag only |
| which segment the photo is on | GPS + heading (noisy) | per-photo posterior / HMM; ABSTAIN under 0.7 | I | yes |
| GPS error size | not observed | building height around point (urban canyon) | II (absorbed into map-match sigma) | yes |
| detector correctness | two-detector agreement | split conformal per condition bin | I | yes |
| segments with no data anywhere in India | nothing | hierarchical pooling segment < ward < city < India; AEF embedding similarity (later) | I with wide intervals | yes (pooling) |
| best next observation | n/a | value of information on route cost | derived | yes |
| route risk | n/a | expected cost, chance-constrained, CVaR, CTP recourse | derived | yes (first two + dead-end penalty) |
| stray animals, festival closures | photo by chance | none fitted | III | no (say so) |
| fog / smog visibility | photo | IMD station visibility, CPCB AQI (later) | II/I | later |
