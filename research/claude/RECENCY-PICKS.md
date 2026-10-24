# RECENCY PICKS: newest work for SC-02 (claude, 2026-10-24 ~17:10 IST)

Method (fixing the "too generic" failure): date-filtered sweeps, not relevance search. arXiv API sorted by submittedDate (keyword in title, last 90 days, 291 rows: RECENCY-ARXIV*.tsv), Hugging Face daily papers for every day 2026-07-25..10-24 (516 keyword rows: RECENCY-HF-DAILY.tsv), GitHub repos created after 2026-07-24 (362 rows: RECENCY-GITHUB.tsv). Raw in recency-raw/. Titles only so far: everything here is UNVERIFIED until opened (dsh/robotics lane opens them).

## arXiv, newest first (title seen in the arXiv API, not opened yet)

| date | id | title | SC-02 use |
|---|---|---|---|
| 2026-10-22 | 2610.30731 | Big World, Little Me: Comparing a First-Person VR Walkthrough Video and Static Slides for Communicating Height-Related ... | direct evidence for the multi-perspective "eye height" story: first-person walkthrough vs slides |
| 2026-10-22 | 2610.30994 | TRACE: Traversability-aware Reactive Navigation via VLM-driven Adaptive Constraints Estimation | VLM decides traversability constraints: detector/judge idea |
| 2026-10-22 | 2610.30839 | ProTrav: Probabilistic Traversability with Elevation Uncertainty Propagation for Risk-aware Navigation | uncertainty-aware cost for routing |
| 2026-10-22 | 2610.30660 | A Topology-Guided GeoAI Agentic Framework for Urban Flood Screening | waterlogging factor |
| 2026-10-19 | 2610.27271 | XoNav: An Exoskeleton as a Personalized Haptic Interface for Assisted Navigation | personalised navigation |
| 2026-10-18 | 2610.25223 | Map2Vid: Embodied Navigation Video Generation with Human-Friendly Motion Control | "walk the route before you go": generate the route as video |
| 2026-10-15 | 2610.24012 | **ChairNav: Cross-Embodiment Pre-training and Personalization for Long-Horizon Wheelchair Navigation** | wheelchair-specific navigation, 9 days old |
| 2026-10-15 | 2610.22461 | Mothership: A Two Tier Autonomous Refuse Collection System for Pedestrian Campuses | campus pedestrian graphs |
| 2026-10-14 | 2610.19330 | **NavAble: A Large-Scale Dataset and Synthetic Data Generation Pipeline for Blind Navigation** | low-vision profile + synthetic data |
| 2026-10-11 | 2610.15403 | A Decade of PhotoMappers: Longitudinal Study of Crowdsourced Disaster Photos Geolocalization with Vision-Language Models | geolocating online/crowd photos (C3 for social media images) |
| 2026-10-06 | 2610.08640 | RIWANav: Recursive World-Action Models with Self-Improvement for Urban Navigation | world model for urban navigation |
| 2026-10-06 | 2610.07982 | M3SunAgent: Monocular 3D Spatial Understanding Agent for Metric Depth Estimation and 3D Visual Grounding | kerb height route 3 |
| 2026-10-04 | 2610.04916 | PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation | |
| 2026-10-03 | 2610.04327 | When Satellite and Street Views Disagree: Cross-View Complementarity in Disaster Damage Assessment | two-routes agreement (satellite vs street) |
| 2026-10-01 | 2610.02000 | Weather-Aware Domain Adaptation for Street-View Weather Recognition | condition router (rain/fog/night fingerprint) |
| 2026-09-29 | 2609.36616 | CrossTimeEdit: A Decade-Spanning Cross-View Dataset and Reward-Guided Editing for Historical Street-View Generation | "same spot over years"; temporal change |
| 2026-09-26 | 2609.37476 | Learning Social Navigation from Internet Videos in the Policy State Space | learn from online walking videos |
| 2026-09-25 | 2609.31885 | Differentiable Dynamics for Autonomous Micro-Mobility Navigation | wheelchair dynamics / push effort |
| 2026-09-30 | 2609.39763 | DiffWAM: A Fast and Efficient Navigation World Action Model | |
| 2026-09-29 | 2609.36969 | Prior-Driven Enhancements in 3D Gaussian Splatting: Normals and Depths Regularization | splat quality |

## GitHub repos created after 2026-07-24 (stars at sweep time)

| created | repo | stars | SC-02 use |
|---|---|---:|---|
| 2026-09-18 | **Oldcircle/geo-sleuth**: agent skill that finds where a photo was taken from OSM geometry, elevation skylines, satellite imagery and street view | 4006 | geolocate online Indian photos with no GPS (C3) |
| 2026-08-24 | YellowO2/streetview-to-3d: walkable street corridor 3D point cloud from panoramas | 14 | 3D corridor for "switch body" |
| 2026-08-24 | City-Form-Lab/urban_network_analysis: pedestrian accessibility and flow metrics | 14 | trips/accessibility metrics |
| 2026-09-29 | martincantcode/15-minutes: interactive pedestrian accessibility map "for whom?" | 9 | UI reference |
| 2026-09-01 | Megvii-Algo-Team/OpusDet: unified open-vocabulary detection | 16 | detector candidate |
| 2026-08-23 | TeleHuman/WNM-3D: world navigation model with 3D scene conditioning | 116 | world model reference |
| 2026-08-26 | RoadScan-AI pothole detection + tracking | 25 | pothole extra class |

## HF daily papers (upvotes) worth a look
2026-10-14 Urbex: Agentic Spatial Grounding for City-Scale 3D Scenes (134); 2026-09-22 WorldCrafter: video world model with 3D-aware memory (162).
