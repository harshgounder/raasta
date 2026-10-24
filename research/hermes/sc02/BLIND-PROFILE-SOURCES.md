# BLIND-PROFILE-SOURCES: what we could add to /analyze tomorrow morning

hermes, 2026-10-25 00:30 IST, research only. Closes the gap flagged in `PHASE2-MAP.md` clause 2: the blind
profile currently has no detector evidence behind it, because tactile paving, crossings and signals are not
in our detection classes at all.

Five needs, five lines of attack: tactile paving, marked zebra, unmarked crossing, crossing signals
(including audible), kerb edges and ramps. Ranked by how fast they could be in `/analyze` tomorrow, not by
how interesting they are.

## The ranked five

### 1. Project Sidewalk validator heads: curbramp, missing curbramp, crosswalk

- What it is: the University of Washington Makeability Lab's training pipeline for the models that validate
  crowdsourced sidewalk labels. Five DINOv2-Large classifiers, one per label type: curb ramp, missing curb
  ramp, obstacle, surface problem, crosswalk.
- Why it fits: two of our five needs are covered outright, kerb edges and ramps (curbramp, missing curbramp)
  and marked crossings (crosswalk). The label vocabulary is already accessibility-native, not generic objects.
- Licence: code **MIT**, models **MIT** per the Hugging Face model cards. Dataset `sidewalk-tagger-ai-validated`
  is **MIT** as well.
- Size and recency: repo 62 MB, last push **2026-10-22** (two days ago). HF model repos per label, safetensors,
  DINOv2 backbone. `export_onnx.py` plus a test ship in the repo, which is the part that matters for speed.
- URLs: https://github.com/ProjectSidewalk/sidewalk-validator-ai , HF collection
  `projectsidewalk/project-sidewalk-validator-models`, datasets at https://huggingface.co/projectsidewalk
- Weights downloadable: yes, public, no gate.
- Honest limits: trained on Google Street View panoramas from deployed Project Sidewalk cities, which is a
  US-heavy domain, with 90 degree perspective crops generated from panoramas. Our inputs are phone photos and
  Wikimedia frames, so expect a domain gap and re-validate on our C6 set before printing any number. It is a
  **validator** head (is this label correct), not a free-standing detector, so it runs on a crop we already
  produced, which is exactly how /analyze is structured.
- Integration cost: export ONNX (script provided), add as a third opinion on existing detections, roughly
  half a day including the C6 re-run. Highest value per hour of anything on this list.

### 2. The OSM tag channel: tactile_paving, kerb, crossing:signal, traffic_signals:sound

- What it is: not a model. OpenStreetMap already carries `tactile_paving=yes/no/incorrect`,
  `kerb=lowered/raised/flush`, `crossing=marked/unmarked`, `crossing:signal`, and in some regions
  `traffic_signals:sound` and `traffic_signals:vibration`.
- Why it fits: it is the only public source that speaks to **audible signals** at all, and it costs nothing
  to read. It slots into the routing service's existing evidence tiers as `source=osm_tag`, which the graph
  already understands and already labels honestly.
- Licence: ODbL 1.0. Size: zero bytes, it arrives with the network we already build.
- Coverage in India: thin and uneven, which is why it ranks second and not first. But "thin and honestly
  labelled" beats "missing and implied", and it covers the signal question that no dataset answers.
- Integration cost: a few hours in the network builder, no model, no GPU, no download.

### 3. Zero-shot prompt extension for tactile paving, plus Roboflow's Dot-Stop and Line-Go set as the check

- What it is: our two open-vocabulary detectors (YOLOE, OWLv2) are driven by 14 text prompts. Tactile paving
  is not among them. Adding `yellow tactile paving`, `blister paving`, `guiding tiles`, `tactile studs` costs
  a config change, not a training run.
- The check set: Roboflow Universe, Tactile-Paving-Blind-Assist, **68 images**, classes exactly
  `Dot-Stop` and `Line-Go` (the two real tactile types), published 2026-03, open source dataset, free to
  download after a Roboflow account. Small, so it is an honest smoke test rather than an evaluation.
- Licence: Roboflow Universe datasets are normally CC BY 4.0, but **check the licence field on the dataset
  page before shipping**, I did not see it rendered in tonight's fetch.
- URL: https://universe.roboflow.com/guilhermes-workspace-tvpvw/tactile-paving-blind-assist-nifnq
- Honest limit: 68 images cannot train a head, and zero-shot prompts on a yellow-on-grey texture will
  over-fire on painted kerbs and road markings. Treat any tactile output as ABSTAIN-grade until we have 300
  Indian positives.
- Integration cost: an hour to add prompts and run the 68 images, and it gives us a number to quote about
  whether the idea is viable at all.

### 4. CDSet for marked crossings, if OSM tags are absent

- What it is: Crosswalk DataSet, 3,434 images from vehicle-mounted cameras, day, rain, occlusion, night and
  damaged paint, split 3,080 train / 354 test, plus 1,770 extra labelled images. Companion code CDNet
  (YOLOv5-based, Jetson-targeted, so small and fast).
- Licence: Zenodo record is open access, **licence field to confirm** before redistribution.
- Size and date: 1.1 GB, published 2022-02-01.
- URL: https://zenodo.org/records/8289874 , paper doi 10.1007/s00521-022-07007-9
- Why it ranks fourth: it is a training set, and training a crossing detector is a tomorrow-afternoon job at
  best, whereas ranks 1 to 3 are hours. But if we need a crossing detector that does not depend on OSM tags,
  this is the best public corpus I found, and it includes night and rain, which is where our own detection
  numbers are weakest.
- Note: unmarked crossings are not in this dataset. Those stay OSM-only, which is honest, because an
  unmarked crossing is a social fact, not a painted object.

### 5. Research references with no downloadable weights tonight

Two papers are worth naming so nobody re-searches them, but neither is an asset we can add tomorrow.

- **Real-Time Segmentation of Tactile Paving and Zebra Crossings for Visually Impaired Assistance** (2026,
  PMC12899687). Improved DeepLabV3+ G-GhostNet, mPA 97 percent tactile and 93 percent zebra, mIoU 94 and 86,
  59.2 fps on a Huawei Atlas 310. Data availability statement: **on reasonable request**. So: method reference,
  not a download.
- **Tenji10K** (Takano and Nakane, Japan): 20 sequences, 10,000 first-person tactile paving images, exactly
  what we would want. I found **no public download or weights** in tonight's scan, only the paper and a
  ResearchGate entry. If someone finds the release, it jumps to rank 1 for tactile paving.

## Indian coverage data, what exists and what does not

What I could verify tonight:

- AFP via France24, **2026-07-10**: a Supreme Court-appointed committee found in **2024** that **84 percent of
  footpaths failed to meet basic engineering standards, and only one in four was usable**. Same piece:
  more than **30,000 pedestrians** are killed on Indian roads every year, about 11 percent of global road
  fatalities with roughly 1 percent of the world's vehicles.
  https://www.france24.com/en/live-news/20260710-india-s-choked-pavements-fail-pedestrians
- Same article, the June 2026 ruling's own words: `"If the road exists, there is a duty to ensure that there
  are demarcated and well-maintained footpaths for walkers."` This is a cleaner quote for the deck than the
  give-way line, because it states a duty rather than a priority.
- GTKP audit paper (2017, opened earlier this week): about 80 percent of the population coping with lack of
  accessible pedestrian infrastructure, listing kerb ramps, handrails, tactile paving and audible signals as
  the missing elements.
- MDPI 2023, `Reviewing the Universal Mobility of the Footpaths in the Centres of Historic Indian Cities`
  (Das Mahapatra), a peer-reviewed Indian footpath audit, useful as a method citation.
  https://www.mdpi.com/2071-1050/15/10/8039

What does **not** exist: an India-specific tactile paving coverage percentage. I looked and did not find one.
So the honest line for the deck is "84 percent of Indian footpaths fail basic engineering standards, and one
in four is usable", followed by "we do not have a tactile paving coverage figure for Indian cities, which is
part of why we measure it".

## What I would do first thing, in order

1. Export the Project Sidewalk curbramp and crosswalk heads to ONNX and run them on 50 of our existing 330
   ACCEPT crops. That single run tells us whether the quickest model in the world is even applicable here.
2. Add the four tactile prompts and run the 68 Dot-Stop and Line-Go images. An hour, and it converts
   "we could detect tactile paving" into a measured yes or no.
3. Wire OSM `tactile_paving`, `kerb` and `traffic_signals:sound` into the routing evidence tiers, because it
   is the only audible-signal source and it costs no model.
4. Only then consider CDSet training, and only if the crossing detector from step 1 fails on our frames.

Nothing here is code, and none of it is in the product until someone builds it. This file is the shopping
list with prices and caveats, not a claim that any of it works.
