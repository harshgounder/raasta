<!-- run id: trun_3b693d434bb94e6db97e777cfbe9e92c -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6db97e777cfbe9e92c
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:10.021949Z
**Modified:** 2026-10-24T09:01:31.861185Z

## Output

# Build A Voice-Scam Detector That Survives Unseen Clones

## Executive Summary

- **Start With Cross-Dataset Evidence**: Spectra-AASIST reports **1.46% EER on In-the-Wild**, while the SpeechAntiSpoofingArena wrapper reports **43.01%** for original AASIST on that dataset. These are different systems and evaluation recipes, not a controlled head-to-head experiment -> prioritize reproducible cross-dataset testing over a famous model name. [32][19]
- **Keep A Lightweight Baseline**: AASIST-L has **85,306 parameters**, supplied pretrained weights, and a reported **0.99% EER on ASVspoof 2019 LA** -> keep it as a compact baseline and possible deployment fallback, not as proof of unseen-generator robustness. [4]
- **Use Recent Models Selectively**: The 2026 XLSR-MamBo work supplies checkpoints and reports **4.97% In-the-Wild EER** for MamBo3, but its downstream evaluation is English-only -> it is a strong research starting point, not an established Hindi detector. [30][16]
- **CPU Feasibility Is Not Browser Feasibility**: The temporal-coherence/MS-CLAP repository reports CPU inference at approximately **one file per second**; its paper reports **17.7% EER on ASVspoof 5** -> consider it an independently structured CPU branch, while separately measuring memory, latency and short-clip behavior. [35][21]
- **Short Clips Need An Inconclusive Result**: Several supplied wrappers select approximately **four seconds** of audio, whereas the problem includes two-second clips -> expose actual speech duration, padding and an abstention state instead of presenting every output as a reliable verdict. [19][10]
- **Compression And Playback Are Core Tests**: SAFE evaluates processing and audio laundering, with combined noise, reverberation and over-the-air conditions among the hardest cases -> make phone-channel stress testing part of the main demo, not a hidden appendix. [9]
- **Indian Coverage Requires New Holdouts**: IndicSynth offers **4,000 hours, 989 target speakers and 12 low-resource Indian languages**; LRLspoof contains **1,304,455 synthetic samples across 66 languages**, but no genuine class -> use them as complementary resources, not as a ready-made balanced Indian test set. [34][37]
- **Separate Detection From Fraud**: A June 2026 Delhi Police case alleges cloned executive instructions in a fraud exceeding **INR 10 crore**. Conversely, legitimate synthesized speech is not necessarily fraudulent -> demonstrate a risk signal plus safe callback guidance, not a claim to determine criminal intent. [23]

**Recommended hackathon direction:** build an upload/microphone interface with a quality gate, one reproducible SSL detector, a lightweight comparison model, and an optional structurally different CPU detector. Show performance under duration, language, silence, loudness and telephone-channel changes. The proposed combinations below are engineering recommendations, not experimentally demonstrated ensemble gains.

This is a broad, evidence-ranked inventory, not a provably exhaustive census of every repository. **NR** means not publicly confirmed in the available material. An absent date is not replaced with a repository creation date. Popularity figures are observed page snapshots, not guaranteed live counts on October 24, 2026. Published results below are attributed measurements or vendor claims; none represents a fresh independent evaluation performed for this report.

## 1. Ranked Detector Inventory: What To Fork First

### Benchmark evidence and deployment fit

Ranking weighs relevance to unseen attacks, available code and checkpoints, reproducibility, recency and practical deployment. It is deliberately not a leaderboard sorted by incompatible EER figures.

| Rank / ID | Name and plain-language function | Weights | Live demo | Browser, CPU and 4 GB GPU | Reported benchmark evidence | Useful combination |
|---|---|---|---|---|---|---|
| 1 / M1 | **Spectra-AASIST**: combines a pretrained speech representation with an AASIST-style detector. | Yes; model card supplies a loading path. | Arena evaluation interface is linked; current uptime NR. | Browser-local inference NR; CPU and 4 GB peak-memory measurements NR. | Model card: **ITW 1.46%**, ASVspoof 2021 DF **2.52%**, 2021 LA **5.25%**, ASVspoof 5 **14.22% EER**. Training overlap with every evaluation corpus is not fully established here. [32] | Test alongside AASIST-L and a temporal branch; resolve the license inconsistency before distributing a fork. |
| 2 / M2 | **XLSR-MamBo**: combines XLSR speech features with Mamba/Hydra sequence models. | Yes, linked checkpoints. | Hosted live demo NR. | Browser NR; CPU/4 GB inference NR. CUDA/custom dependency setup makes it a higher installation risk. | MamBo3: **ITW 4.97%**, 2021 LA **0.81%**; MamBo4: ITW **5.17%**, 2021 DF **1.43% EER**. These are variant-specific, not one model's combined score. [16][30] | RawBoost, consented Indian holdouts, CodecFake/DFADD stress sets. |
| 3 / M3 | **SSL_Anti-spoofing**: a well-established wav2vec 2.0/XLSR detector with augmentation. | Yes, LA and DF checkpoints. | NR. | Browser/CPU/4 GB measurements NR; older Python/PyTorch environment needs attention. | **2021 LA 0.82% EER**, min t-DCF 0.2066; **2021 DF 2.85% EER**. This does not establish ITW or Indian-language performance. [5] | RawBoost plus the official evaluation harness; strong reproducibility baseline. |
| 4 / M4 | **AASIST-L**: a very small raw-waveform detector. | Yes. | Available through third-party integrations; its own hosted demo NR. | Best compact porting candidate in this inventory, but CPU latency, browser execution and 4 GB inference remain unverified. | **2019 LA 0.99% EER**, 85,306 parameters. No verified unseen-domain EER for this exact variant here. [4] | Quality gate, ONNX investigation, SSL detector comparison. |
| 5 / M5 | **AASIST**: the original graph-attention anti-spoofing baseline. | Yes. | Arena wrapper exists; uptime NR. | Browser-local NR; CPU/4 GB measurements NR. The original repository's training memory is not an inference requirement. | Original **2019 LA 0.83% EER**. Arena wrapper: **ITW 43.01%**, 2021 DF **17.04%**, 2021 LA **12.35% EER**. [4][19] | Essential negative/control baseline for exposing domain shift. |
| 6 / M6 | **Temporal-coherence/MS-CLAP detector**: checks how audio embeddings change over time, then uses XGBoost experts. | Yes, trained model assets in repository. | Example clips, not a confirmed live service. | Author reports CPU inference without a GPU, approximately one file/second. Browser-local and peak RAM NR; 4 GB GPU unnecessary for the claimed CPU path. | Paper: **ASVspoof 5 17.7% EER** versus 25.9% for its static comparison. ITW result is **AUC 0.976 on a subset**, not full-dataset EER. [35][21] | A structurally different branch to compare with SSL/AASIST; validate complementary errors before fusion. |
| 7 / M7 | **Nes2Net speech releases**: nested networks using self-supervised speech features. | Linked checkpoints and speech-specific releases. | Inference examples; hosted demo NR. | Repository explicitly describes a CPU option. Browser and 4 GB memory NR. | Do not use the root repository's singing-voice result as an unseen speech benchmark; relevant speech-release EER was not established here. [27] | Follow its ASVspoof speech branches, not the root singing configuration; combine with RawBoost/evaluation tooling. |
| 8 / M8 | **Gustking XLSR classifier**: ready-to-load Hugging Face real/fake audio classifier. | Yes. | A linked Space exists; uptime NR. | Browser-local/CPU/4 GB performance NR. | ASVspoof 2019 evaluation reports EER **0.0401**, but the metric's unit convention is not sufficiently clear here to convert it to a percentage. No confirmed unseen-domain EER. [12] | Quick UI and inference integration; compare against an official baseline before relying on it. |
| 9 / M9 | **garystafford wav2vec2 detector**: Hugging Face classifier for genuine versus TTS/cloned speech. | Yes. | Linked Aawaaz Space; uptime NR. | Browser-local/CPU/4 GB NR. Published timing is hardware-dependent, not a verified deployment budget. | Named unseen-attack EER NR; model card explicitly warns about novel TTS, conversion and noise. [18] | A fast application scaffold, not the strongest evidence-backed detector. |
| 10 / M10 | **Hemgg Deepfake-audio-detection**: 94.6M-parameter Hugging Face audio classifier. | Yes. | Linked Heem2 Space; uptime NR. | Browser-local/CPU/4 GB NR. | Card reports **accuracy 0.9545**, not unseen EER; card also says more information/data are needed. [15] | Reuse the front end or pipeline, then swap in a better-tested backend. |
| 11 / M11 | **MelodyMachine Deepfake-audio-detection-V2**: another 94.6M-parameter Transformers classifier. | Yes. | Linked API-style Space; uptime NR. | Browser-local/CPU/4 GB NR. | Accuracy is reported; named unseen EER and sufficiently detailed generalization evidence NR. [17] | Useful integration reference; do not interpret downloads as robustness evidence. |
| 12 / M12 | **RawBMamba**: bidirectional Mamba operating on raw audio. | Yes. | NR. | Browser/CPU/4 GB NR. | **2019 LA 1.19%**, 2021 LA **3.39%**, 2021 DF **15.85% EER**. The DF result is an important counterweight to the attractive architecture. [33] | RawBoost and reproducible cross-domain tests; architecture comparison rather than first production choice. |
| 13 / M13 | **Original lab260 AASIST3 release**: older SSL/AASIST-derived model. | Yes, but explicitly **not the paper's weights**. | Arena link exists. | Browser/CPU/4 GB NR; wrapper pads/truncates to approximately four seconds. | Arena: **2019 LA 9.44%**, ITW **29.72%**, 2021 DF **28.73% EER**. Maintainer marks release outdated/unmaintained. [10] | Reproduce as a cautionary baseline; do not merge blindly. |
| Watch / M14 | **Spectra-AASIST3**: the replacement recommended by the old AASIST3 card. | Not confirmed in the evidence summarized here. | NR. | Browser/CPU/4 GB NR. | No score is promoted here without an established compatible citation and protocol. [10] | Inspect as an upgrade candidate after M1; not a verified drop-in recommendation in this report. |

**Takeaway:** M1 and M2 have the most attractive retrieved cross-dataset results, but M3 is a safer reproducibility anchor. M4 offers a genuinely small model, while M6 offers the clearest retrieved CPU claim. No retrieved evidence justifies promising that a large SSL model will fit a **4 GB GPU** or execute entirely inside the browser.

### URLs, dates, licenses and popularity

The following metadata applies to the same IDs above. "NR" in the update column means a latest commit/model revision was not established; a paper year or dated release notice is identified separately.

| ID | URL | Last update / dated evidence | License | Stars / downloads / other popularity |
|---|---|---|---|---|
| M1 | `https://huggingface.co/lab260/Spectra-AASIST` | Last model update NR. | **Conflict:** header Apache-2.0, body MIT; clarify before redistribution. [32] | 5 HF likes; 120 monthly downloads; GitHub stars NR. [32] |
| M2 | `https://github.com/saki-ciallo/XLSR-MamBo` | 2026 paper; latest repository commit NR. | MIT for code/models, according to repository. [30] | 0 stars in observed snapshot; downloads NR. [30] |
| M3 | `https://github.com/TakHemlata/SSL_Anti-spoofing` | Last update NR; repository creation was 2022, not a last-update date. | MIT. [5] | Stars/downloads NR. |
| M4 | `https://github.com/clovaai/aasist` | Last update NR. | MIT. [4] | Stars/downloads NR. |
| M5 | `https://github.com/clovaai/aasist`; wrapper: `https://huggingface.co/SpeechAntiSpoofingBenchmarks/AASIST` | Last update NR. | MIT. [4][19] | Wrapper: 1 HF like, 74 monthly downloads; repository stars NR. [19] |
| M6 | `https://github.com/stbiadmin/audiodeepfake_public` | 2026 paper; last commit NR. | MIT. [35] | 0 stars, 0 forks in observed snapshot; downloads NR. [35] |
| M7 | `https://github.com/Liu-Tianchi/Nes2Net` | Dated notices: April 2025 ASVspoof 5 release; March 2026 HF models. Exact last commit NR. [27] | Apache-2.0 for repository; dependencies retain their own terms. [27] | Stars/downloads NR. |
| M8 | `https://huggingface.co/Gustking/wav2vec2-large-xlsr-deepfake-audio-classification` | Last update NR. | Apache-2.0. [12] | 6 HF likes; **21,035 monthly downloads**; stars NR. [12] |
| M9 | `https://huggingface.co/garystafford/wav2vec2-deepfake-voice-detector` | Last update NR. | Apache-2.0. [18] | 6 HF likes; **11,513 monthly downloads**; stars NR. [18] |
| M10 | `https://huggingface.co/Hemgg/Deepfake-audio-detection` | Last update NR. | Apache-2.0. [15] | 4 HF likes; **12,936 monthly downloads**; stars NR. [15] |
| M11 | `https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2` | Last update NR. | Apache-2.0. [17] | 19 HF likes; **5,837 monthly downloads**; stars NR. [17] |
| M12 | `https://github.com/cyjie429/RawBMamba` | Latest update NR; creation June 6, 2024. | NR; do not assume permission to redistribute. [33] | 32 stars; downloads NR. [33] |
| M13 | `https://huggingface.co/lab260/AASIST3`; code: `https://github.com/mtuciru/AASIST3` | Explicitly outdated/unmaintained; exact last update NR. | **Conflict/restriction:** header CC BY-NC 4.0; body CC BY-NC-ND 4.0, including restrictions on modified redistribution. [10] | 3 HF likes; 428 monthly downloads; GitHub stars NR. [10] |
| M14 | `https://huggingface.co/lab260/Spectra-AASIST3` | Replacement recommendation verified; latest revision NR. | NR in the usable evidence here. | Stars/downloads NR. [10] |

**Takeaway:** the highest-download classifiers are not necessarily the strongest unseen-generator detectors. License uncertainty is also a practical ranking factor: M13 is a poor default for a freely modifiable public hackathon fork.

### Case study: why the AASIST numbers disagree

The original AASIST repository supplies pretrained checkpoints and reports **0.83% EER** on ASVspoof 2019 LA. Its compact sibling reports **0.99%** on that same benchmark. These results make the repository valuable for confirming that an implementation and scoring pipeline work. [4]

The Arena wrapper reports **43.01% EER on In-the-Wild** for original AASIST. It also documents deterministic selection of the first **64,600 samples**, mono 16 kHz input and wrapper-specific preprocessing. That result does not invalidate the original benchmark; it shows that dataset, checkpoint and preprocessing are part of the system being evaluated. [19]

**Decision:** reproduce one published baseline before experimenting, then freeze the preprocessing and evaluate on a separate corpus. A spectacular 2019 LA score alone is insufficient evidence for a two-second regional-language phone call.

## 2. Recent Papers, Competition Solutions And Reusable Tooling

### Competition evidence: winners are not always downloadable models

| Resource | URL | What it contributes | Date / license / popularity | Weights and live demo | Small-runtime status | Result and integration value |
|---|---|---|---|---|---|---|
| **ASVspoof 5 official toolkit** | `https://github.com/asvspoof-challenge/asvspoof5` | Baselines, protocols and scoring. | Challenge repository; latest update, license and stars NR. | Baseline resources exist; winner-specific weights and live demo NR. | Browser execution NR; use as offline/backend evaluation tooling. 4 GB inference depends on chosen model. | Track 1 prioritizes **minDCF**, with EER secondary; Track 2 uses a different primary cost metric. Do not rank every entry by one interchangeable score. [2] |
| **ASVspoof 5 winning-system analysis** | `https://arxiv.org/pdf/2601.03944v1` | Competition recipes and cross-dataset failure evidence. | 2026 paper; software license/stars/downloads NR. | Public winner code/weights/demo not established here. | CPU/4 GB/browser NR. | **T32** wins Track 1 closed; **T45** leads Track 2 open with min a-DCF **0.07**. Across additional datasets, nearly all systems exceed **10% EER**, and no system leads all six datasets. [42] |
| **SAFE Challenge** | `https://arxiv.org/html/2510.03387` | Blind testing, processing and playback/laundering evaluation; mixture-of-experts recipes. | 2025 paper, CC BY 4.0 for paper; code license/popularity NR. | Winner code/weights/live demo not established here. | Evaluation budget includes a **16 GB T4**, not evidence of 4 GB compatibility. | Reports balanced accuracy, not a directly interchangeable EER leaderboard. Top recipes combine LCNN/ResNet branches and differing spectrograms. [9] |
| **ADD 2023** | `https://arxiv.org/html/2305.13774v1` | Chinese challenge covering detection, localization and attribution. | 2023 paper; implementation license/popularity NR. | Public winner artifacts NR. | CPU/4 GB/browser NR. | Best FG-D weighted EER reported as **12.45%**. Generation, localization and attribution winners use other metrics and must not be called binary-detector winners. [41] |
| **AT-ADD 2026** | `https://at-add.com`; paper: `https://arxiv.org/html/2604.08184v1` | Broader audio-deepfake challenge and baseline lead. | Paper records baseline/data release **April 8, 2026**; latest update/license/popularity NR. | Specific downloadable winner weights/live demo not established here. | CPU/4 GB/browser NR. | Relevant multilingual/device-diversity lead; no compatible unseen EER promoted here. [14] |
| **RawBoost** | `https://github.com/TakHemlata/RawBoost-antispoofing` | Training-time waveform augmentation, not a standalone detector. | Latest update/license/stars/downloads NR in retrieved evidence. | Detector weights/demo N/A. | Offline preprocessing; browser and 4 GB measurements NR. | Merge with M2/M3 and compare against an unaugmented control. No standalone EER should be attributed to the augmentation alone. [8][30] |
| **SpeechAntiSpoofingArena** | `https://huggingface.co/spaces/SpeechAntiSpoofingBenchmarks/SpeechAntiSpoofingArena` | Common interface and documented model/dataset scoring recipes. | Latest update/license/popularity NR. | Model-dependent weights; linked public interface, uptime NR. | Browser interface does not establish browser-local inference or 4 GB backend fit. | Useful for comparing checkpoint and preprocessing behavior. Preserve the exact system configuration. [19][10] |
| **Awesome Fake Audio Detection** | `https://github.com/john852517791/awesome-fake-audio-detection` | Broad paper/code discovery catalogue, including recent niche work. | MIT for catalogue, not linked artifacts; latest commit/stars/downloads NR. | Weights/demo N/A. | Static catalogue usable in browser; backend N/A. | Best expansion point for additional 2026 papers and code. [25] |
| **Audio-Deepfake-Detection survey repository** | `https://github.com/media-sec-lab/Audio-Deepfake-Detection` | Dataset and method index. | Latest update/license/stars/downloads NR. | Weights/demo N/A. | Browser-readable catalogue; backend N/A. | Useful cross-check for less-famous datasets and augmentation methods. [8] |

**Takeaway:** competition reports are valuable design evidence, but a winning score without public code, checkpoints and an identifiable inference recipe is not a fork-ready deliverable. T32/T45 are documented identifiers; organization names should not be guessed.

### Niche and 2026 watchlist

These are leads to inspect after the runnable shortlist, not equivalent ready-to-deploy substitutes.

| Item and URL | Function and dated evidence | License / stars / downloads | Weights / live demo | Browser / CPU / 4 GB | Unseen EER and combination |
|---|---|---|---|---|---|
| **SafeEar**: `https://safeearweb.github.io/Project/`; paper: `https://arxiv.org/html/2409.09272` | Separates semantic and acoustic information, then detects using shuffled acoustic tokens; privacy-oriented 2024 research. | Paper CC BY-NC-ND 4.0; code license, stars and downloads NR. | Project/demo material referenced; runnable public weights and live interactive detector NR. | CPU/4 GB/browser NR; reported RTX 3090 training is not an inference requirement. | Its multilingual results are not proof of unseen Indian-phone performance. Combine its privacy ideas with a conventional detector, rather than assuming an available fork. [36] |
| **REIMU**: `https://arxiv.org/html/2608.00857v1` | August 2026 research lead listed in the specialist catalogue. | Code license, stars/downloads and last code update NR. | Weights/demo NR. | Browser/CPU/4 GB NR. | Compatible unseen EER NR; inspect before considering a merge. [25] |
| **Teffic Audio**: `https://tefficlabs.com/teffic-audio`; paper: `https://arxiv.org/html/2607.28351v2` | Recent detector/product-research lead; July 2026 paper listed in catalogue. | Open-source license, stars/downloads and last code update NR. | Public reusable weights and live-demo availability not established here. | Browser-local/CPU/4 GB NR. | Do not promote marketing or pooled benchmark numbers as an independently verified unseen-attack score. Compare only after obtaining the actual protocol. [25] |
| **Detecting Audio Deepfakes on the Edge: Lightweight SSL / Browser Plugin** | Catalogue entry: `https://github.com/john852517791/awesome-fake-audio-detection` | Browser/edge deployment paper listed **June 29, 2026**. | License, stars/downloads, latest code update NR. | Weights/live demo NR. | Browser deployment is the research topic, not a verified working browser implementation in this report. CPU/4 GB NR. | Strong follow-up lead for the deployment requirement; unseen EER NR. [25] |
| **Proteus** | Same catalogue URL. | Adversarial-robustness testing lead listed **June 28, 2026**. | License, stars/downloads, code update NR. | Weights/demo NR. | Browser/CPU/4 GB NR. | Use as a prospective red-team complement, not a proven detector replacement; compatible EER NR. [25] |
| **Intervention-Based Shortcut Diagnosis / Watermark Shortcut work** | Same catalogue URL. | Listed **July 3** and **June 22, 2026**, respectively. | Code license, stars/downloads and updates NR for both. | Weights/demo NR for both. | Browser/CPU/4 GB NR for both. | Directly relevant to silence/loudness and artifact leakage; diagnostic ideas, not a claimed ready-made fix. [25] |

**Takeaway:** the recent research frontier includes shortcut diagnosis, adversarial testing and edge execution, not just larger classifiers. Keep a lead separate from a verified runnable artifact.

### Case study: SAFE versus clean benchmark success

SAFE's design withholds generator/source access and includes raw, processed and laundered audio. It therefore addresses a different operational question from recognizing artifacts within a familiar challenge distribution. Its findings identify noise, reverberation and over-the-air combinations as particularly difficult. [9]

The highest-performing recipes include multiple expert branches, while other submissions use AASIST, RawNet2 and SSL combinations. This is useful architecture evidence, but it does not establish that adding more branches will improve a new Indian short-clip detector. [9]

**Decision:** first measure whether two branches fail on different clips. Add fusion only when it improves a held-out operating point and still meets the resource budget. Show an actual playback/phone-channel failure rather than hiding it behind a clean-audio average.

## 3. Datasets: Build An Unseen-Attack Test, Not A Bigger Random Split

**N/A** below means detector weights or inference runtime do not apply to the dataset itself. Dataset processing/storage needs are separate from model inference needs.

| Dataset and URL | What it contains / why it matters | Latest dated evidence; license | Stars/downloads | Weights / live demo / small-runtime status | Relevant results and combination |
|---|---|---|---|---|---|
| **ASVspoof 2019 LA**: `https://datashare.ed.ac.uk/handle/10283/3336` | Official train/dev/eval foundation for the stated task. | 2019 release; latest update and dataset license NR here. | NR. | Weights N/A; live demo N/A; CPU preprocessing possible in principle, measured budget NR; browser/GPU N/A. | AASIST 0.83%, AASIST-L 0.99% EER are reference results. Keep evaluation isolated from training. [4] |
| **ASVspoof 2021 LA/DF**: `https://github.com/asvspoof-challenge/2021` | Challenge evaluation beyond the 2019 training setup. | 2021 challenge; latest update/license NR. | NR. | Weights/demo/inference N/A. | M3 reports LA 0.82%, DF 2.85%; compare by task, not a merged score. [8][5] |
| **ASVspoof 5**: `https://github.com/asvspoof-challenge/asvspoof5` | Newer challenge protocols and evaluation tooling. | Challenge materials; latest update/license NR. | NR. | Weights model-dependent; dataset demo/inference N/A. | M1 reports 14.22% EER; primary challenge metrics differ by track. [32][2] |
| **In-the-Wild**: `https://deepfake-total.com/in_the_wild` | Publicly collected real/fake celebrity/political speech: **20.8 h real, 17.2 h fake, 58 identities**. | Latest update NR; page states Apache-2.0. Underlying media rights still deserve attention. | Downloads/stars NR. | Weights N/A; associated DeepfakeTotal web interface exists; dataset inference N/A. | Central external test. Full benchmark and paper-specific subsets must be distinguished. [3][21] |
| **MLAAD**: `https://deepfake-total.com/mlaad` | Multilingual synthetic speech; intended to be paired with matching real data such as MAI-LABS. | Latest update NR; **CC BY-NC 4.0**. | NR. | Weights/demo/inference N/A. | Synthetic-only data cannot by itself establish genuine-class false alarms. Noncommercial restriction matters for later commercialization. [1] |
| **LRLspoof**: `https://huggingface.co/datasets/lab260/LRLspoof` | **1,304,455 TTS samples, 66 languages**, including low-resource language coverage. No genuine class. | Latest update NR; card says MIT. | 8 HF likes; **2,586 monthly downloads**. | Weights/demo N/A; **452 GB** published dataset size, multipart archive handling. Inference N/A. | Its **1-SRR** statistic is not detector EER. Pair with carefully matched genuine speech and held-out generators. [37] |
| **IndicSynth**: `https://github.com/vdivyas/IndicSynth`; paper: `https://aclanthology.org/2025.acl-long.1070` | **4,000 h**, **989 target speakers**, **12 low-resource Indian languages**; speaker metadata. | ACL **July 2025**; latest repository update/license NR. | NR. | Detector weights/live demo N/A; processing runtime NR. | High-value Indian adaptation resource, but no detector unseen EER is established by dataset size alone. [34] |
| **CodecFake**: `https://codecfake.github.io/`; code: `https://github.com/roger-tseng/CodecFake`; data: `https://huggingface.co/datasets/rogertseng/CodecFake` | Codec-resynthesized speech covering several neural codecs. | Interspeech **2024**; latest update and dataset's own license NR. VCTK's license is not automatically the new dataset's license. | NR. | Code yes; reusable detector weights/live demo NR; dataset inference N/A. | Useful for codec-TTS coverage and telephone/compression stress design; compatible EER not extracted here. [38] |
| **STCodecFake**: `https://zenodo.org/records/14631091` | 2025 English/Chinese codec-related dataset lead in the survey index. | **2025** listing; exact update/license NR. | NR. | Weights/live demo/inference N/A. | Useful additional codec-domain holdout; benchmark EER NR. [8] |
| **SpoofCeleb**: `https://arxiv.org/html/2409.17285v2` | Noisy celebrity-source speech, **1,251 identities and 23 attacks**, controlled splits. | Paper v2 **April 15, 2025**; dataset license/update NR. | NR. | Dataset weights/demo N/A; exact download packaging and small-host processing NR. | Paper reports RawNet2 **1.12%**, AASIST **2.37% EER** in its protocol. Those are not full In-the-Wild results. Non-English speech is filtered out. [39] |
| **Deepfake-Eval-2024**: `https://arxiv.org/html/2503.02857v2` | Real-world multimodal collection; audio component **56.5 h / 1,820 samples**, **42 audio languages**. | Paper v2 **March 5, 2025**; dataset license/update NR. | NR. | Dataset weights/live demo N/A; distribution and runtime NR. | Paper reports **AASIST 55.22% audio EER**. Its 60/40 fine-tuning split is not automatically a generator-disjoint test. [40] |
| **WaveFake**: `https://zenodo.org/record/5642694` | English/Japanese synthesis dataset; useful historical generator diversity. | **2021** listing; latest update/license NR here. | NR. | Weights/demo/inference N/A. | EER NR; auxiliary training/control set, not sufficient modern-cloner coverage. [8] |
| **CFAD**: `https://zenodo.org/record/8122764` | Chinese fake-audio resource. | **2022** listing; latest update/license NR. | NR. | Weights/demo/inference N/A. | EER NR; useful Chinese cross-language/domain comparison. [8] |
| **FoR**: `http://bil.eecs.yorku.ca/datasets` | Older English fake-or-real dataset. | **2019** listing; latest update/license NR. | NR. | Weights/demo/inference N/A. | EER NR; historical baseline, not the main unseen-2026 test. [8] |
| **FakeAVCeleb**: `https://github.com/DASH-Lab/FakeAVCeleb/tree/main` | Audio/video celebrity manipulation data. | **2021** listing; latest update/license NR. | NR. | Weights/demo/inference N/A. | EER NR; optional multimodal extension, lower priority for a phone-only task. [8] |

**Takeaway:** combine datasets by the failure mode they expose, not simply by their size. A synthetic-only multilingual corpus, an English celebrity corpus and a noisy real-world benchmark answer different questions.

### Case study: IndicSynth plus LRLspoof does not automatically produce an Indian benchmark

IndicSynth supplies Indian-language synthesis and target-speaker metadata. LRLspoof adds much broader low-resource TTS coverage, but explicitly contains only synthetic samples. Both can improve coverage of the fake class; neither automatically supplies an appropriately matched genuine comparison population. [34][37]

A detector could otherwise learn recording source, speaker, codec, silence padding or dataset packaging rather than synthesis. Recent catalogue entries specifically address speaker identity, shortcut diagnosis and watermark shortcuts, reinforcing the need to test those confounds rather than assuming multilingual scale removes them. [25]

**Decision:** collect consented genuine Hindi and regional-language speech under the same capture/transmission conditions as synthetic clips. Hold out speakers and generators, and group all transformations of the same original recording together. This is a proposed evaluation design, not a claim that the existing datasets already meet it.

### A concrete unseen-attack protocol

1. **Keep ASVspoof 2019 evaluation and ITW untouched.** Do not tune thresholds or select checkpoints repeatedly on them.
2. **Add leave-one-generator-out testing.** Keep generator families, not merely randomly selected files, outside training.
3. **Cross duration with conditions:** 2, 4, 6 and 10 seconds of actual speech; raw, normalized, silence-edited and phone-channel versions.
4. **Separate language and speaker holdouts.** Report Hindi and each tested regional language individually; label untested languages explicitly.
5. **Report EER plus deployment errors.** Include genuine-speech false alarms and synthetic misses at the chosen threshold, latency, peak RAM/VRAM and abstention rate.
6. **Publish the recipe.** Checkpoint, label orientation, resampler, VAD, crop/pad rule and score aggregation belong in the result record. The existing wrappers demonstrate why these details matter. [19][10]

## 4. Live Demos, Commercial Products And International Leads

Commercial systems are primarily **demo and workflow references**, not mergeable open-source detectors. A browser extension, web upload or API client does not establish that inference happens locally in the browser.

| Product / URL | Plain-language function | Last update; license; popularity | Public weights / live demo | Browser / CPU / 4 GB backend | Evidence, claims and what to borrow |
|---|---|---|---|---|---|
| **DeepfakeTotal**: `https://deepfake-total.com/` | Public upload/interactive audio-deepfake interface. | Update NR; code/model reuse license NR; stars/downloads NR. | Public browser interface exists; public reusable weights NR; uptime NR. | Browser UI yes; local-browser inference, CPU budget and 4 GB backend NR. | Borrow upload flow, educational examples and understandable result presentation. Do not infer a public backend API or open license. [26] |
| **Resemble Detect / DETECT-3B Omni**: `https://www.resemble.ai/detect/` | Commercial deepfake detection via extension, SDK/API and deployment options. | Update NR; public open-source license NR; stars/downloads NR. | Public reusable weights NR; contact/get-started/demo paths exist. | Browser extension yes; local inference unconfirmed. On-prem/air-gapped options advertised; 4 GB fit NR. | Vendor claims include **98.1% accuracy**, **51 languages** and sub-300 ms latency. These are not independently verified unseen EER. Borrow explanations, heatmaps and audit-trail ideas. [29] |
| **Pindrop Pulse**: `https://www.pindrop.com/use-cases/audio-deepfake-detection`; product: `https://www.pindrop.com/pulse-for-contact-centers` | Contact-center liveness/deepfake risk with agent feedback. | Update NR; open-source license NR; popularity NR. | Public reusable weights NR; sales demo, not confirmed unrestricted upload demo. | Agent/browser workflow, not established local inference; CPU/4 GB NR. | Vendor advertises detection from **two seconds** and **99%** on known engines. Do not translate that to 99% accuracy on unseen Indian scam calls. Borrow the live-agent warning workflow. [24] |
| **Reality Defender RealCall**: `https://www.realitydefender.com/product/realcall` | Live-call voice-clone risk detection. | Update/license/popularity NR. | Public weights NR; sales demo. | Browser-local/CPU/4 GB NR. | Unseen EER NR; borrow escalation/routing rather than attempting to fork proprietary inference. [31] |
| **Reality Defender RealAPI**: `https://www.realitydefender.com/product/realapi` | Structured detection results for uploaded/recorded media. | Update/license/popularity NR. | Public weights NR; page describes a free image/audio plan, with eligibility/current limits unconfirmed. | Hosted API; browser client possible, own CPU/4 GB backend not established. | Unseen EER NR; borrow structured evidence/results while keeping the application responsible for decisions. [31] |
| **Reality Defender RealMeeting**: `https://www.realitydefender.com/product/realmeeting` | Meeting-oriented face/voice manipulation monitoring. | Update/license/popularity NR. | Public weights NR; booked demo. | Local-browser/CPU/4 GB NR. | Unseen EER NR; useful if the project expands beyond telephone audio. [31] |
| **Reality Defender RealScan**: `https://www.realitydefender.com/product/realscan` | Browser-accessible media investigation workflow. | Update/license/popularity NR. | Public weights NR; access/demo terms unconfirmed. | Browser interface, not established browser-local model execution; CPU/4 GB NR. | Unseen EER NR; borrow investigator-friendly media/result organization. [31] |

**Takeaway:** borrow commercial presentation patterns without borrowing their certainty. Vendor accuracy, language counts and latency require their own test conditions; they cannot be inserted into the open-model EER ranking.

### Case study: Resemble's explanations versus an honest hackathon result

Resemble presents detection through multiple deployment surfaces and emphasizes explanations, visual evidence and auditability. Pindrop instead emphasizes a contact-center decision flow and immediate agent feedback. Both demonstrate that an operational warning needs more than a scalar score. [29][24]

For the hackathon, a useful result card should show duration, quality warnings, threshold, model disagreement and recommended next action. However, an attention heatmap or suspicious segment should not be described as proof of synthesis unless it has been validated as an explanation.

**Decision:** copy the clarity of the workflow, not unsupported percentages or forensic-sounding language.

### International and community coverage

The strongest concrete non-English expansion points in this inventory are **ADD**, **CFAD**, **STCodecFake**, Japanese coverage in **WaveFake**, multilingual **MLAAD/LRLspoof**, and Indian **IndicSynth**. These are more actionable than an unverified mirror or a social-media performance claim. [41][8][1][37][34]

Additional independently documented fork-ready winners or implementations were **not established in the available evidence** for Gitee, GitCode, ModelScope, Kaggle, Zhihu, CSDN, Bilibili, Korean/Russian community sources, Reddit/HN/X, Devpost or DoraHacks. That is an inventory gap, not evidence that none exist. No hackathon entry or commercial product is labeled open source merely because it has a public demo.

## 5. Indian Voice-Scam Evidence A Judge Can Understand

### Documented incident and correctly qualified statistics

| Evidence | What the source actually says | What not to claim | Demo/story implication |
|---|---|---|---|
| **Delhi Police / Mumbai-company case, June 17, 2026** | Police allege a cloned managing director's voice was used to instruct a deputy general manager; the reported fraud exceeded **INR 10 crore**, involved **63 accounts**, and led to **five arrests**. [23] | This is reported police attribution, not an independently published forensic proof of which cloning model was used. | Show an executive-payment call, then a warning and independent callback step before money moves. |
| **McAfee India release, May 2, 2023** | **47%** of respondents had experienced an AI voice scam **or knew someone who had**. [11] | Not "47% of Indians were personally scammed" and not a 2026 prevalence estimate. | Explain that the survey measures reported exposure, with a broader denominator than direct victims. |
| **Loss among Indian victims in that release** | **83%** reported financial loss; **48% of those who lost money** reported more than **INR 50,000** lost. [11] | Not 83% of all Indians, and not 48% of all respondents. | Connect a few seconds of audio to a potentially consequential payment decision without exaggerating prevalence. |
| **Difficulty telling voices apart** | **69%** of Indian respondents said they could not distinguish an AI voice from a real one in the cited release. [11] | Not a measured detector error rate or a controlled listening-test result. | Let the judge guess genuine/fake first, then show the detector with uncertainty. |
| **Survey scope and independence** | The India release describes **7,054 respondents across seven countries**. A News18 report repeats the same research. [11][13] | These are not two independent studies. The original global McAfee blog describes a different survey scope, so its denominator should not be silently merged with the India release. [22] | Label the source and year on the slide; use a recent case for immediacy and the older survey only for context. |

**Takeaway:** the strongest pitch is a concrete payment-fraud scenario, not an inflated national victim count. A current national police count specifically separating AI voice-clone scams from other cyber fraud was not publicly confirmed in this evidence set. Additional incident details should not be invented to make the story more dramatic.

### Case study: a cloned instruction is also an authorization failure

In the June 2026 case, the alleged mechanism is an apparently authoritative executive voice directing a payment. The important interaction is not simply whether a recording sounds artificial; it is whether an employee treats voice familiarity as sufficient payment authorization. [23]

A detector can add friction at that moment, but a genuine human impersonator, compromised account or legitimate synthesized accessibility voice complicates the binary story. The demo should therefore separate **"synthetic-speech risk"** from **"fraud confirmed"**.

**Decision:** end the demonstration with an independent callback or out-of-band approval. The detector is a warning layer, not a replacement for payment controls.

## 6. Merge Architecture For Two- To Ten-Second Clips

### A practical build sequence

| Layer | Recommended implementation | Why it belongs | Resource/failure check |
|---|---|---|---|
| Browser interface | File upload plus consented microphone capture; waveform, actual speech duration and condition toggles. | Makes the problem tangible without claiming browser-local ML. | Keep recordings private by default; show upload/retention behavior explicitly. |
| Audio contract | Decode, mono conversion and documented resampling; retain original metadata and quality indicators. | Existing wrappers require specific sample rates and crop rules. [19] | Reject decoding failures; do not silently interpret an incorrectly labeled sample rate. |
| Quality gate | Detect insufficient speech, extreme clipping, overwhelming noise and long silence. | Two seconds of file length may contain little speech. | Return "insufficient evidence" rather than manufacture confidence. Thresholds require validation. |
| Primary model | Start with M3 for reproduction; benchmark M1 or M2 as an upgrade. | M3 supplies a conventional training/checkpoint path; M1/M2 offer stronger retrieved cross-domain evidence. [5][32][16] | Time installation first. M2's CUDA dependencies can consume the hackathon. |
| Compact comparison | M4 AASIST-L. | Small parameter count makes it a useful constrained-deployment experiment. [4] | Measure actual latency/RAM; do not infer performance solely from parameter count. |
| Optional independent branch | M6 temporal/MS-CLAP. | Different representation and CPU-reported inference may expose different errors. [35] | CPU does not imply low RAM or good two-second performance. |
| Aggregation | Compare fixed-length windows and model disagreement; calibrate on development data only. | Avoid one fragile crop determining the entire recording. | Padding or repeating two seconds does not create four seconds of independent evidence. |
| Result card | "Elevated synthetic-speech risk", "no strong synthetic evidence", or "inconclusive"; include quality and disagreement. | Prevents a model score being mistaken for identity or fraud verification. | Do not label an uncalibrated score a probability. |
| Evaluation log | Model/checkpoint ID, crop rule, language, duration, perturbation and measured runtime. | Makes improvements and regressions visible. | Keep originals and transformed descendants in the same split. |

**Takeaway:** for a small backend, reduce the number of concurrently loaded large models before attempting a complex ensemble. A browser interface backed by a hosted model is an honest and useful hackathon deployment.

### Case study: the CPU route has a different trade-off

The temporal-coherence repository explicitly reports CPU execution and supplies trained assets. Its paper uses two-second analysis windows with one-second hops, which makes it particularly relevant to this short-clip task. However, its impressive ITW AUC comes from a subset, while its reported ASVspoof 5 EER is **17.7%**. These numbers describe different evaluations and cannot be combined into a single superiority claim. [35][21]

By contrast, XLSR-MamBo reports attractive cross-dataset EERs but has custom sequence-model dependencies and English-only evaluation. The practical choice is not "new versus old"; it is installation risk, memory, language coverage and the particular error profile. [30][16]

**Decision:** keep the CPU branch if it adds demonstrable coverage or guarantees a reliable demonstration on available hardware. Do not keep it merely to make the architecture diagram look more sophisticated.

### Stress tests that directly target the stated challenges

Run the same underlying real and fake clips through:

- **Duration:** 2/4/6/10 seconds of speech, documenting the crop and pad rule.
- **Silence:** remove, add and relocate silence without changing spoken content.
- **Loudness:** matched normalization and gain changes; include a non-clipped and clipped version.
- **Channel:** proposed G.711/AMR/Opus-style telephone/compression conditions, plus an actual speaker-to-microphone replay where feasible.
- **Background:** quiet, household noise, music and reverberation.
- **Language/speaker:** held-out Hindi/regional-language speakers; mark unsupported languages.
- **Editing:** short synthetic insertions within otherwise genuine recordings, not only fully synthetic files.
- **Novel synthesis:** generator families excluded from training; keep a consented newly generated test set separate from public benchmarks.

These are proposed experiments, not claims of measured robustness. SAFE's processing results and the 2026 shortcut-related papers provide the motivation. [9][25]

As one optional **test generator, not a detector**, Bodhan's September 2026 release includes `https://huggingface.co/bodhan-ai/indic-speak`; the associated release reports TTS coverage of **23 languages**. Keep any such generated holdout out of adaptation training, obtain required permissions, and do not assume its release implies a detector benchmark. [43][44]

## 7. Ten Questions A Non-Expert Judge Will Ask

| # | "What if..." question | How the demo should answer | Honest boundary |
|---|---|---|---|
| 1 | **"What if the scammer uses a cloning tool you never trained on?"** | Reveal a sealed generator holdout after the model is frozen; display its result separately from familiar generators. | Passing one new tool does not establish universal future-tool detection. |
| 2 | **"What if I only have two seconds?"** | Run the same utterance at 2/4/6/10 seconds; show actual speech duration and an inconclusive state. | Padding does not create new evidence; several existing wrappers were designed around roughly four seconds. [19][10] |
| 3 | **"What if the caller speaks Hindi or my regional language?"** | Offer named, consented language samples and separate per-language outcomes. | Do not substitute multilingual pretraining or an English result for measured Indian-language performance. M2's English-only limitation is explicit. [16] |
| 4 | **"What if it comes through WhatsApp or a bad phone line?"** | Toggle a documented codec/channel transformation and show whether risk or abstention changes. | A clean WAV score is not a telephone score; processing and playback are known challenge conditions. [9] |
| 5 | **"What if the fake is played through a loudspeaker?"** | Replay a consented fake into a microphone and compare it with the source file. | Report this as an over-the-air test, with room/device conditions, not a universal replay guarantee. |
| 6 | **"What if I make it quieter or trim the silence?"** | One-click gain and silence edits, with the same spoken content and side-by-side scores. | A large change is a robustness failure worth showing, not explaining away. Shortcut-diagnosis work is directly relevant. [25] |
| 7 | **"What if a real person sounds robotic or uses assistive TTS?"** | Include genuine unusual speech and legitimate TTS; distinguish authenticity from malicious intent. | A synthetic label does not mean a scam; a genuine label does not mean an authorized caller. |
| 8 | **"What if only one sentence is fake?"** | Insert a short synthetic segment and show window-level outputs alongside the whole-clip result. | A whole-clip detector may miss localized edits; segment outputs are not automatically validated localization. |
| 9 | **"What if your two models disagree?"** | Show both outputs and return inconclusive; explain the safe callback action. | Do not average arbitrary scores and call the result a calibrated probability. |
| 10 | **"What if I do not want my voice stored or sent away?"** | Display where processing occurs, retention settings and a delete action; demonstrate a tested local/CPU path if available. | A web page or browser extension is not proof of local inference. SafeEar is a relevant privacy-oriented research reference, not an automatic privacy guarantee. [36] |

**Takeaway:** the best demonstration is not ten successful predictions. It is a transparent comparison that shows when the detector works, when it degrades and when the user should rely on independent verification.

## 8. Synthesis: Which Stack Wins Under Which Constraint?

| Strategy | Mechanism | Evidence base | Scope and trade-off | Deployment horizon | Recommended role |
|---|---|---|---|---|---|
| **AASIST-L / original AASIST** | Compact raw-waveform anti-spoofing. | Strong familiar benchmark; original AASIST's retrieved ITW result is weak. [4][19] | Easy reference point; small size does not solve domain shift. | Best immediate baseline/porting experiment. | Keep as control and possible fallback. |
| **SSL_Anti / Spectra / MamBo** | Pretrained speech representation plus learned discrimination. | Stronger retrieved cross-dataset results, but different protocols and incomplete Indian evidence. [5][32][16] | Better research starting point; heavier dependencies, memory uncertainty and possible data-overlap questions. | Immediate if environment/checkpoints work; robustness adaptation takes longer. | Primary detector family. |
| **Temporal/MS-CLAP** | Temporal embedding consistency plus tree experts. | Public code/assets and CPU claim; subset AUC and ASVspoof 5 EER must remain separate. [35][21] | Different error mechanism; CPU accessibility does not establish low memory or best accuracy. | Useful hackathon alternative. | Optional complementary branch. |
| **Competition mixtures of experts** | Fuse architectures/features and augmentation. | Strong blind-challenge recipes; public winner artifacts often not established. [9][42] | Potential diversity benefits, but installation and calibration costs increase. | Later optimization, not first milestone. | Borrow recipes after measuring branch complementarity. |
| **Commercial detection** | Hosted/proprietary risk scoring integrated into workflows. | Vendor claims and product documentation, not comparable open unseen EER. [24][29][31] | Polished integration; limited inspectability and no established forkable weights. | Fast workflow prototype if access exists. | UX inspiration or clearly labeled external comparator. |
| **Indian/multilingual data adaptation** | Match language, speaker and channel coverage. | Valuable new corpora; genuine-class matching and generator-disjoint evaluation remain essential. [34][37][1] | Addresses a real gap but can also introduce dataset shortcuts. | Essential beyond the initial demo. | Build consented holdouts before claiming Indian readiness. |

The central tension is that **benchmark strength, recency and deployability are different dimensions**. A tiny model can be easy to host yet fail across domains; a recent model can have attractive EER yet remain English-only; a polished browser product can still perform all computation remotely. The retrieved ASVspoof 5 analysis further warns that high challenge rank does not guarantee leadership across external datasets. [42]

A second tension concerns explainability. Commercial interfaces make outputs easy to act on, but an attractive explanation cannot repair an uncalibrated detector. A third concerns multilingual scale: a million synthetic files can expand fake coverage while leaving genuine regional-language false alarms almost unmeasured.

**Final choice:** deliver a reproducible M3 baseline, test M1/M2 as the primary upgrade, retain M4 as a compact control, and add M6 only if it improves held-out errors within the measured hardware budget. Pair that stack with ITW, an untouched challenge evaluation, consented Indian short-clip holdouts and visible channel/shortcut tests. Present **synthetic-speech risk plus an inconclusive option**, not "scam proven". That is a stronger hackathon contribution than an unsupported claim of universal clone detection.

## References

1. [
   MLAAD: The Multi-Language Audio Anti-Spoofing
  Dataset (version 9)
  ](https://deepfake-total.com/mlaad)
2. *GitHub - asvspoof-challenge/asvspoof5 · GitHub*. https://github.com/asvspoof-challenge/asvspoof5
3. [
   In-the-Wild Dataset
  ](https://deepfake-total.com/in_the_wild)
4. *GitHub - clovaai/aasist: Official PyTorch implementation of "AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks" · GitHub*. https://github.com/clovaai/aasist
5. *GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper "Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation". · GitHub*. https://github.com/TakHemlata/SSL_Anti-spoofing
6. *Deepfake Detection that Generalizes Across Benchmarks*. https://arxiv.org/html/2508.06248v1
7. *SONAR: A Synthetic AI-Audio Detection Framework and Benchmark*. https://arxiv.org/html/2410.04324v1
8. *GitHub - media-sec-lab/Audio-Deepfake-Detection: Research progress on speech deepfake detection: Relevant datasets aggregated from the review literature and publicly available codes · GitHub*. https://github.com/media-sec-lab/Audio-Deepfake-Detection
9. *Synthetic Audio Forensics Evaluation (SAFE) Challenge*. https://arxiv.org/html/2510.03387
10. *lab260/AASIST3 · Hugging Face*. https://huggingface.co/lab260/AASIST3
11. *McAfee Reveals 47% Of Indians Have Faced AI Voice Scams*. https://digitalterminal.in/tech-companies/mcafee-reveals-47-of-indians-have-faced-ai-voice-scams
12. *Gustking/wav2vec2-large-xlsr-deepfake-audio-classification · Hugging Face*. https://huggingface.co/Gustking/wav2vec2-large-xlsr-deepfake-audio-classification
13. *AI Voice Cloning New Weapon of Cyber Criminals; 83% Indians Report Financial Loss: McAfee Report | Tech News - News18*. https://www.news18.com/tech/ai-voice-cloning-new-weapon-of-cyber-criminals-83-indians-report-financial-loss-mcafee-report-7700359.html
14. *AT-ADD: All-Type Audio Deepfake Detection Challenge Evaluation Plan*. https://arxiv.org/html/2604.08184v1
15. *Hemgg/Deepfake-audio-detection · Hugging Face*. https://huggingface.co/Hemgg/Deepfake-audio-detection
16. *XLSR-MamBo: Scaling the Hybrid Mamba-Attention Backbone for Audio Deepfake Detection*. https://arxiv.org/html/2601.02944
17. *MelodyMachine/Deepfake-audio-detection-V2 · Hugging Face*. https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2
18. *garystafford/wav2vec2-deepfake-voice-detector · Hugging Face*. https://huggingface.co/garystafford/wav2vec2-deepfake-voice-detector
19. *SpeechAntiSpoofingBenchmarks/AASIST · Hugging Face*. https://huggingface.co/SpeechAntiSpoofingBenchmarks/AASIST
20. *What survives the codec shift: Pooled no-vocals residuals for speech deepfake detection*. https://arxiv.org/html/2609.33375
21. *Audio Deepfake Detection Using Temporal Coherence Analysis*. https://arxiv.org/html/2609.09489
22. *AI Calling—Scammers turn to AI voice cloning tools for a new breed of scam | McAfee Blog*. https://www.mcafee.com/blogs/privacy-identity-protection/artificial-imposters-cybercriminals-turn-to-ai-voice-cloning-for-a-new-breed-of-scam/
23. *Delhi gang uses AI to clone Mumbai MD’s voice, siphons Rs 10 crore from firm - Delhi News | India Today*. https://www.indiatoday.in/cities/delhi/story/ai-voice-cloning-fraud-delhi-police-arrest-five-rs-10-crore-mumbai-company-scam-2928485-2026-06-17
24. *Audio Deepfake Detection | Pindrop*. https://www.pindrop.com/use-cases/audio-deepfake-detection
25. *GitHub - john852517791/awesome-fake-audio-detection: A list of tools, papers and code related to Fake Audio Detection. · GitHub*. https://github.com/john852517791/awesome-fake-audio-detection
26. [
   Deepfake Total
  ](https://deepfake-total.com/)
27. *GitHub - Liu-Tianchi/Nes2Net: A Lightweight Nested Architecture for Foundation Model Driven Speech Anti-spoofing · GitHub*. https://github.com/Liu-Tianchi/Nes2Net
28. *OmniSpeech AI Detect™ Now Available on the Zoom App Marketplace — Offering RealTime Deepfake Audio Detection for Zoom Meetings*. https://www.omni-speech.com/post/omnispeech-ai-detect-now-available-on-zoom-marketplace-turning-zoom-into-a-real-time-deepfake-aud
29. *Multimodal, Real-Time Deepfake Detection at Enterprise Scale | Resemble AI*. https://www.resemble.ai/detect/
30. *GitHub - saki-ciallo/XLSR-MamBo: updating · GitHub*. https://github.com/saki-ciallo/XLSR-MamBo
31. *Deepfake and AI caller detection | Reality Defender*. https://www.realitydefender.com/
32. *lab260/Spectra-AASIST · Hugging Face*. https://huggingface.co/lab260/Spectra-AASIST
33. *GitHub - cyjie429/RawBMamba · GitHub*. https://github.com/cyjie429/RawBMamba
34. *IndicSynth: A Large-Scale Multilingual Synthetic Speech Dataset for Low-Resource Indian Languages - ACL Anthology*. https://aclanthology.org/2025.acl-long.1070
35. *GitHub - stbiadmin/audiodeepfake_public · GitHub*. https://github.com/stbiadmin/audiodeepfake_public
36. *SafeEar: Content Privacy-Preserving Audio Deepfake Detection*. https://arxiv.org/html/2409.09272
37. *lab260/LRLspoof · Datasets at Hugging Face*. https://huggingface.co/datasets/lab260/LRLspoof
38. *CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems*. https://codecfake.github.io/
39. *SpoofCeleb: Speech Deepfake Detection and SASV In The Wild*. https://arxiv.org/html/2409.17285v2
40. *Deepfake-Eval-2024: A Multi-Modal In-the-Wild Benchmark of Deepfakes Circulated in 2024*. https://arxiv.org/html/2503.02857v2
41. *ADD 2023: the Second Audio Deepfake Detection Challenge*. https://arxiv.org/html/2305.13774v1
42. *ASVspoof 5: Evaluation of Spoofing, Deepfake, and Adversarial Attack Detection Using Crowdsourced Speech*. https://arxiv.org/pdf/2601.03944v1
43. *Bodhan September 2026 - a bodhan-ai Collection*. https://huggingface.co/collections/bodhan-ai/bodhan-september-2026
44. *Bodhan AI and AI4Bharat Launch Four Open AI Models to Build India's Multilingual Education Ecosystem | Skilloutlook.com*. https://skilloutlook.com/education/bodhan-ai-and-ai4bharat-launch-four-open-ai-models-to-build-indias-multilingual-education-ecosystem
