# TOP 5 v1 (claude, 2026-10-24 ~15:10 IST, PROVISIONAL)

Scope change 15:00 (user): smart cities and climate are IN because they can be made very flashy and visual.
Inputs: 8 Parallel ultra reports (research/claude/), hermes 163 leads + judge lens + wow scan, dsh wave 1, live checks (research/claude/VERIFY-1.md + 15:08 checks below). dsh wave 2 is still running. **More statements are released 18:15-20:15**, so this list can change.
Ranked, not scored (PICK-PLAYBOOK step 4). Each entry says where it loses.

## 1. CL-01 "Watch a forest disappear" (Satellite forest-loss alerts)
- **10-second reveal:** a 3D globe flies into Chhattisgarh; a time slider drags 2019 to 2026 and the Hasdeo forest turns to a coal pit in front of the judge; red AI alerts pop on the exact cleared patches; then the same model runs on a state it never trained on.
- **Why it is mind-blowing to a common person:** real, current Indian story. ET 28 May 2026: approval for coal mining in Hasdeo-Arand needing about **4.48 lakh trees** felled (VERIFIED via search excerpt); Springer case study 26 May 2026 maps the mine growth 2013-2025 from satellites (VERIFIED excerpt); PIB 1 May 2026: Great Nicobar project, up to **7.11 lakh trees** to be felled (VERIFIED excerpt).
- **AI/ML core:** NASA-IBM Prithvi-EO-2.0-300M (Apache-2.0, 19,504 downloads, VERIFIED on HF), TorchGeo (MIT, 4,211 stars, VERIFIED), Clay (Apache-2.0). Labels: Global Forest Watch / GLAD alerts (hermes opened).
- **Flashy layer:** globe.gl (MIT, 3,206 stars), deck.gl (MIT, 14,696), before/after swipe, santioni-style story.
- **What-ifs it answers live:** clouds (show cloud mask), crops harvested or leaves fell (same-season comparison, NDVI curve), river changed course (class map), unseen state (the statement's own test).
- **Where it loses:** Global Forest Watch already exists, so "innovation" must come from the story + the unseen-state test + the alert feed; Sentinel-2 download and preprocessing take time (precompute 2-3 small areas); Prithvi on a 4 GB GPU for small tiles is UNTESTED.

## 2. AI-03 "One Scam. Three Stories." (Topic-augmented knowledge graph)
- **10-second reveal:** three unrelated fraud complaints are uploaded; the 3D graph snaps them together on one shared UPI handle; click the edge and the exact sentence from each complaint opens; edit the handle and the link breaks.
- **Base:** LightRAG (MIT, 40,303 stars, pushed 2026-10-22, VERIFIED) + react-force-graph / 3D force graph (MIT). Neo4j LLM Graph Builder (Apache-2.0, 5,282, VERIFIED) as second route.
- **Common-person hook:** 101,928 cybercrime cases in 2024 + 1930 helpline (PIB, cited by Parallel CROSS, UNVERIFIED by us; note it is ALL cybercrime, not one scam type).
- **Where it loses:** needs an LLM for extraction (API allowed for AI-03); graph demos can feel abstract if the story is weak; four of five GraphRAG HF Spaces were broken per Parallel.
- **Feasibility:** highest of the five (Parallel CROSS rated it High).

## 3. SC-02 "The shortest path is a trap" (Accessible walking routes)
- **10-second reveal:** two routes from the MUJ gate to a clinic animate on a 3D map; the shortest one runs into stairs, a broken footpath and a parked bike (photo pops up for each); the accessible route goes around.
- **Base:** Project Sidewalk (MIT, 110 stars, pushed 2026-10-23, VERIFIED; open label API), arXiv 2602.09216 "Towards Human-AI Accessibility Mapping in India: VLM-guided..." (Project Sidewalk adapted for **Chandigarh**, found 15:08, to open), Grounding DINO (Apache-2.0, 10,701) or a VLM for zero-shot barrier detection, OSMnx (MIT, 5,883) for routing, deck.gl for the map.
- **Local edge:** the user is ON the MUJ campus; phone photos of real campus footpaths = the "label your own local images" requirement, and an authentic demo no one else has.
- **Where it loses:** street imagery coverage near MUJ is UNVERIFIED (Mapillary/GSV); small-barrier detection quality untested; routing on a footpath graph needs OSM footways that may be missing.

## 4. HM-02 "Different brands. Same ingredient. One warning." (Prescription safety checker)
- **10-second reveal:** a typed prescription with Dolo 650 + Combiflam; two brand cards collapse into one paracetamol node: total per day exceeds the limit; change the patient to a child or kidney disease and the verdict changes.
- **Base:** junioralive/Indian-Medicine-Dataset (MIT, 253,973 brands, VERIFIED by hermes + claude), DDInter 2.0 (302,516 interactions, redistribution licence NOT established), CDSCO banned-FDC lists (156 on 2 Aug 2024, 16 on 11 Jun 2026, per Parallel). Indian hospital medication-error median 34.11% across 307,106 patients (PMC12683552, per Parallel, UNVERIFIED by us).
- **Where it loses:** least flashy of the five; mostly deterministic, so "AI/ML" is thin (fuzzy brand match, OCR, explanation); the statement wants a pharmacist-built test set (none available yet); best app shell to fork has 1 star.

## 5. AI-01 "Maa, it's not me" (Voice-clone scam detection)
- **10-second reveal:** a panicked call in a family member's voice asks for money; the judge guesses real or fake; the detector flags it before the payment screen.
- **Base:** Spectra-AASIST (HF, apache-2.0, 143 downloads), AASIST (MIT, 308 stars, last push 2023), SSL_Anti-spoofing (MIT); Indian data: IndicSynth (12 languages, ACL 2025, per Parallel).
- **Common-person hook:** strongest emotional hook of all 13 (Delhi Police case June 2026, over INR 10 crore with a cloned MD voice, per Parallel, UNVERIFIED by us).
- **Where it loses:** detection does not hold up on real clips: AASIST 0.83% EER on ASVspoof 2019 vs 43.01% In-the-Wild (Parallel); hermes-B's test of one public ONNX detector called every fake clip real. A judge cloning their own voice live could break it on stage. Only viable with a two-detector "agree or say inconclusive" design.

## Runners-up (with the one reason they are out)
- SC-01 vehicle re-ID across cameras: very flashy (city flow arcs, car lights up on every camera), FastReID (Apache-2.0, 4,003) exists, but we have no multi-camera Indian traffic footage tonight.
- AI-04 "AI Courtroom: who lied?": very feasible (HHEM 120k downloads, CPU), but a dashboard is less mind-blowing to a common person.
- W3-02 "Pocket money for AI": strong story, but wallet + testnet work sits on the critical path.
- AI-02, HM-01, W3-01, CL-02 (2,000 two-person labels), CL-03, CL-04 (MATLAB): lower on wow or feasibility.

## Recommendation (claude)
Top pick **CL-01**: the most visual, a real Indian forest being cut right now, a foundation model doing the AI, and a built-in honesty test (unseen state). Safest strong pick: **AI-03**. Decide after a 30-minute feasibility spike on CL-01 (download one Hasdeo Sentinel-2 pair, run Prithvi or NDVI change on the GPU), and after the 18:15 release.
