# IDEATION-LUNAR-TIE.md: how the SIH 2026 LUNAR-TIE idea was made, and what Hypnexis can reuse

v1, 2026-10-24, written by claude (subagent, read-only extraction). Lane L4 input for `method/IDEATION-METHOD.md` (see `research/WAVE-1-BRIEF.md` L71).

Rules for this file:
- Sections 1 to 5 are EXTRACTION. Every claim carries `path Lx-Ly`. Nothing in them comes from memory.
- Section 6 is labelled **ADAPTATION**. It is my mapping of the extracted moves onto the Hypnexis round. It is a hypothesis list, not research, and every per-statement line in it is UNVERIFIED until wave 1 leads land.
- Section 7 is the coverage audit (bytes and lines per file vs `wc`) plus a red-team of this file.

Path shorthand used below:

| short | full path |
|---|---|
| `I/` | `~/sih-idea/` (files 00 to 20 are byte-identical to `~/sih-2026/ideas/`, checked with `cmp` this session) |
| `S/` | `~/sih-2026/` |
| `R0/` | `~/lunar-tie-r0/` |
| `DEMO/` | `~/lunar-tie-demo/` |
| `FG` | `~/sih-field-guide/README.md` |
| `CSD` | `~/Videos/claude-sih data.txt` (the Claude Code chat export) |
| `CONT` | `~/Videos/sih-continue.txt` (Hermes session export, audit part) |
| `ROAST` | `~/sih-progress/ROASTER-SIH26166.md` (read in addition: it is the full Q&A source that `I/20` digests) |
| `H/` | `~/hypnexis-main/` |

---

## 0. One-screen summary

```
 229 live PS (226 published)            what made it "big brain"
        |                               ---------------------------------------------
        | W1 28 + W2 11 + W3 3 + W4 51   1 reframe: "derive truth from sensors that
        v  runs, user filters             disagree", engine not matcher
 10-row PICK-BOARD (ceiling-first)      2 go AROUND the wall: chain 300x as 18x + 16x,
        |                                 found by reading what experts avoided (the TELL)
        | 14 lenses, weights              3 two independent paths; agreement = confidence
        | 20/30/20/15/15                  4 physics replaces data: relight a DEM to make
        v                                 your own ground truth
 SIH26166 (ISRO, lunar correspondence)  5 algebra cancels the gap (quad-hash), theorems
        |                                 back the sub-pixel claim (CRB, FRI)
        | Jim Simons frame + factor      6 honesty IS the feature: abstain demo
        | universe + enumeration matrix  7 measure your own error without labels
        v                                8 stand on 2026 parts, do not build from bare metal
 LUNAR-TIE: 7-stage pipeline,           9 one picture a layman reads: NCC -0.021 vs 0.973
 swipe demo, abstain demo, day-5 gate  10 every number lie-hunted before the pitch
```

What I could NOT find: any record of how real judges reacted. A grep of `S/` root docs for internal-round results found only plans (`S/README.md` L95 "internal pitch deck (tomorrow)"), no outcome. Section 5 therefore describes what the pitch was designed to do, not what it achieved.

---

## 1. How the problem statement was chosen out of many

### 1.1 The size of the pool (the count itself was contested)

| count | meaning | source |
|---|---|---|
| 226 | published list, titles only (172 software / 54 hardware) | `S/INDEX.md` L97-98; `CONT` L753 (old continuation text) |
| 229 | live portal crawl: 174 software + 54 hardware + 1 polluted row (SIH26091) | `FG` L39; `S/INDEX.md` L99 |
| delta 3 | SIH26227/228/229 live but missing from the 226 mirror; AICTE email pending | `I/11` L79-81; `S/research/PICK-BOARD.md` L26-27 |

So "the SIH list had 226" is the published number; the team worked on 229 rows and flagged the clash instead of picking one silently.

### 1.2 The funnel

```
 229 rows (all-specs.json, full official text)                S/INDEX.md L99
   |
   | user scope 2026-08-27: "separate runs for ALL software topics, 2-3 runs per topic.
   | Winner record for EVERY winning AND other-position team"   S/CAMPAIGN-PLAN.md L3
   v
 W1 competition recon: 28 runs (process, winners 2017-2025, judges, org DNA, MUJ path,
   rival teams, PS banks, winner builds, testimonials)         S/CAMPAIGN-PLAN.md L9-40
 W2 idea-lab channels: 11 runs (money-flow, acquisition, workarounds, failed autopsies,
   compelled evidence, nonconsumption, geo-arbitrage, complaints, demand forecast,
   founder frameworks, convergence)                            S/CAMPAIGN-PLAN.md L42-58
 W3 scheme alignment: 3 runs                                   S/CAMPAIGN-PLAN.md L60-62
 W4 per-theme: 18 themes x (PS / prior winners / landscape)    S/CAMPAIGN-PLAN.md L64-68
   (fired: w4 = 51, 17 themes)                                 FG L83
   |
   | triangulation rule: "one method = anecdote, two = pattern, three = finding,
   | four = conviction"                                         S/CAMPAIGN-PLAN.md L7
   v
 user filters: software only, no reuse of own projects (kavach/BAHI), highest CEILING
   + research depth over assembly, fresh/novel, NOT agriculture  PICK-BOARD L3
   |
   v
 PICK-BOARD: 10 rows (8 ranked + 2 unranked)                   PICK-BOARD L7-18
 killed/demoted with reasons: 26150 DVR/NVR (commercial prior art), 26086 monsoon
   (agri crowd), 26119 (multi-year engineering), 26147 (no dataset), 26052 (hardware),
   26183 (index-like ceiling, crowd)                            I/11 L33-42
   |
   | 14-lens evaluation + combined weighting                   I/20 L11-25; ROAST L145-194
   v
 SIH26166  "Multi-modal, Sun angle and scale invariant image correspondence using
            Chandrayaan-2 optical images (OHRC, TMC and IIRS)"   I/09 L9-11
```

### 1.3 The reasons it won (as written by the team)

From `I/11` L5-13:

| reason | quote or number |
|---|---|
| hardest = self-filtering crowd | "hardest problem in the 229-PS set: 20x-320x scale, shadow inversion, pan-vs-hyperspectral modality: the crowd filters itself out" |
| public data exists | chmapbrowse, LROC, SELENE |
| the grading rule is written down | "exact acceptance contract (sub-pixel, uniform, RMSE, inlier count/ratio) = we know what we are scored on" |
| empty lane | "low registration count (0/500 at check time)" |
| verified whitespace | "landscape research scored it 8.6/10 weighted, strongest in the theme" |

`I/14` L33-34 makes the contract point sharper: "ISRO tells you exactly how they will grade you. This is the most honest, checkable PS in the whole 229-row set."

### 1.4 The weighting that picked it (and the honesty about single lenses)

The combined weight: "winn 20%, ceiling 30%, whitespace 20%, data 15%, kill-inverse 15%. Only 166 stays top quartile in all five, every alternative spikes one lens and crashes another" (`I/20` L18-22).

The team published the lenses where 166 LOSES, which is the part worth copying:

| lens | ranking | 166 position | source |
|---|---|---|---|
| win-only | 26073 > 26103 > 174 > 142 > 166 | 5th | `ROAST` L194 |
| data-only | 26175 > 26168 > 174 = 142 > 166 | 5th | `ROAST` L194 |
| product score | 26174 460 > 26166 453 > 26142 426 | 2nd | `PICK-BOARD` L22 |
| ceiling | 166 tied stars5 with 142, 175, 26066 ("only 4 of 229 are stars5") | tied 1st | `ROAST` L71-80 |
| whitespace | 166 9.4, number 1 of 7 families | 1st | `ROAST` L152, L185 |
| riskiest | 166 first (TBD dataset, day-5 gate) | 1st (bad) | `ROAST` L182 |
| combined | 166 > 174 > 175 > 142 > 26066 > 26143 | 1st | `ROAST` L194 |

The board order was a deliberate re-rank by the ceiling lens, and the board says so: "this board is RE-RANKED by ceiling lens. Source Table 23 order ... SIH26174 460 (1st) > SIH26166 453 (2nd)" (`PICK-BOARD` L22).

### 1.5 The crowd and sponsor checks

| question | answer found | source |
|---|---|---|
| is the theme crowded? | Space = 9 of 229 PS = 4.0%, vs Smart Automation 55 | `ROAST` L157 |
| does niche mean easy? | No: "the pool shrinks, but its average competence probably goes up" | `CSD` L99; `I/06` L45-52 |
| will ISRO refuse to pay? | 7 orgs in SIH history gave no winner; for 3 of them nobody was shortlisted; ISRO SIH1523 was "a QUALITY gate, not a ghosting"; Dept of Space 2026-27 budget Rs 13,705.63 crore | `I/06` L6-43 |
| what bar is realistic? | user wanted "god level phd level stuff" (`CSD` L43); reframed to "you don't need PhD-level, you need genuinely-new-and-checkable" | `CSD` L104; `I/06` L53-55 |
| what if it is impossible? | teammate claims scored FALSE / HALF TRUE / FALSE, then a falsifiable day-5 test replaced the debate | `I/14` L8-14, L91-104 |
| backups if it dies | 26174, 26142, 26175, 26066, 26143 ranked with scores | `I/11` L15-24 |

---

## 2. The ideation frames used (concrete, with quotes)

### 2.1 Frame A: the Jim Simons frame (the root of everything)

Origin (2026-08-02, a different hackathon session), verbatim user text: "take the adaptibility and the way it tries to connect and relate everything into first quantize them then relate them in math equations the methodology that everything is interrelated and that even wrong info or negetive info gives you info which is valuable is gold like how jim simons had done with medallion funds" (`I/01` L12-17).

The three parts it was turned into (`I/01` L19-28):
1. QUANTIZE first ("Give the quality a number and a unit before you relate it to anything").
2. RELATE as equations ("Interrelation is not vibes; it is a model").
3. NEGATIVE INFORMATION IS INFORMATION ("A failed match, a dead URL, a wrong measurement, a rejected hypothesis: each one narrows the space").

The push that forced it (2026-08-27), user verbatim, rejecting a domain-scoped first wave map: "u only used stuff that is directly relevent here ... think u are jim simons and all this and all the data u see is your market and market data ... its like u are thinking on a npc mindset" (`I/01` L35-43).

The reframe sentence: "the Moon archive is the market, every image is a tick, the correspondences are the hidden alpha." (`I/01` L45-46). The same block was pasted into every research run as a MINDSET contract: "the lunar image archive is the tick tape; correspondences are the alpha; noise is the microstructure; conditions (sun angle, scale, modality, texture, artifacts) are the regimes." (`I/02` L12-17).

The transfer map (`I/01` L53-72), a selection:

| finance / quant | lunar image problem |
|---|---|
| PCA factor models | "eigenmoon" appearance factors |
| regime detection (CUSUM/HMM) | sun-angle / modality / artifact regimes |
| portfolio theory + Kelly | blending the 3 matcher tracks |
| backtest time-splits | holdout + condition-split validation |
| Cramer-Rao bound | the sub-pixel accuracy limit |
| point-process statistics | crater catalogs (Ripley's K) |
| causal counterfactual | relighting: what A would look like at B's sun |
| analog markets | medical MI registration, astrometry plate-solving, rover nav |

Rules that fell out of it (`I/01` L76-90): lateral fields first ("Domain scoping is the NPC trap"), structure from research never from the head, numbers with units over adjectives, condition-split holdouts, "HONEST ABSTENTION: like a quant that refuses a trade when the model is outside its regime", failures are data.

The one-line payoff the team wrote: "A winner here is not the team that implements SIFT best. It is the team that knows the Cramer-Rao bound on sub-pixel shift, uses Kelly weights to blend three matcher tracks, and treats the crater field as a marked point process on a sphere." (`I/01` L94-97).

### 2.2 Frame B: the forward model, "no adjectives"

User verbatim: "we dont use general npc shit language like blurr i dont want that i want what is blurr here? a pixel error that shift right by this degree and this place in this unit used i want exact data for everything and if a research doesnt bring us that we do more research!" (`I/04` L5-17).

Contract given to every run (`I/04` L33-50): no qualitative adjectives ("Blur" = MTF value at a frequency), a VARIABLE TABLE with symbol, SI unit, range, instrument, source, and "effect equation (how it converts into registration/pixel error)", a units dictionary, primary sources only, and a MISSING-NUMBER register (N2M) for anything not published. Nine runs covered illumination, surface, optics, detectors, motion, geometry, artifacts, data volume, and coupling (`I/04` L53-219). Why: it "turns 'sub-pixel accuracy' from a slogan into a budget" (`I/04` L223-227).

### 2.3 Frame C: the factor space universe

User principles verbatim: "everything interrelated. every variable and force must be counted. exact data or more research. my examples were just examples, go far beyond." and "every single pixel of dark or light is data. consider what math/logic theory could possibly be used (did you miss any?)" (`I/05` L5-9).

| piece | what it is | source |
|---|---|---|
| 14 layers | L1-L5 equipment/environment/geometry/artifacts/archive, L6 method math, L7 estimation, L8 lateral math, L9 orthogonal markets, L10 self-computed numbers, L11 operational chain, L12 demand/risk/self-audit, L13 theory inventory, L14 pixel-as-data | `I/05` L13-25 |
| 74-theory inventory | "the 'what if I missed something' pass" (corrected from "~90" to 74) | `I/05` L27-65 |
| pixel-as-data catalog | each dark or light pixel also tells: sun geometry (shadow algebra), relief, composition, detector temperature, sensor identity (PRNU), codec state, cosmic rays, real resolution (MTF from crater rims), texture class | `I/05` L69-89 |
| rings | DIRECT (problem), MID (ecosystem), WIDE (community, patents, judges, funding, policy) | `I/05` L98-103 |

### 2.4 Frame D: census-first web (fix for "invented from intuition")

The team caught that frames A-C were partly invented and wrote: "The prior universe (05, FACTOR-SPACE-UNIVERSE) was invented from intuition. This one is derived from literature counts." (`I/15` L3). Rule: "No paper count means no field." (`I/15` L32).

The distance rule (`I/16` L13-19) is a test, not a label:
- d=1 DIRECT: shares a sensor, modality or metric term with the PS text.
- d=2 INDIRECT: shares a method with a d=1 field (MI, optimal transport, bundle adjustment) but no sensor. Examples: medical MI, astrometry, rover SLAM, cryo-EM.
- d=3 PARTIAL: shares only an axiom or theorem (DTW warping, channel capacity, percolation, QAP).

### 2.5 Frame E: dissect every field as a chain, insert each step at 2+ places

`I/17` L3: a vision LLM is treated "not as a name but as a process of intermediates", each mapped to multiple pipeline stages. The master mapping table (`I/17` L87-105) crosses every intermediate (encoder, connector, LLM backbone, grounding, pretraining, decoding, optics, photometry) with every stage (ingest ... visual) and counts multiplicity. Rule: "Any intermediate not tried at two or more stages must justify why one is sufficient." (`I/17` L105). `I/18` does the same for optics, photometry, matching, geometry and other fields' registration systems.

### 2.6 Frame F: the exhaustive enumeration matrix

`I/19` L3: "For every web field in 16, list every model, every dataset with size and license and gated flag plus fallback, every theory and axiom with USE vs DEEP-MINE vs NO tag, every metric." Rows without a distinct URL fail (`I/19` L131). Each dataset row carries size, licence, gate, fallback (`I/19` L58-69). Its stated purpose: "This is what fixes the habit of using training data memory." (`I/19` L131).

### 2.7 Frame G: the axiom harvest (idea -> axiom -> TEST -> gold -> falsifier)

`S/ideas/IDEATION-DEEP-01.md` L5-8: "axioms the session asserts but never tests, corollaries it never draws, ideas derivable by pushing its own logic one level further. every row: idea -> the axiom behind it -> the TEST -> what gold it could yield." Each row has a falsifier and a data need, for example A1 "falsifier: hash errors > tie ambiguity rate => bridge needs rework. data need: none (synthetic). 1 day of work" (L22-25).

`S/ideas/IDEATION-DEEP-02.md` L11-17 applies it across the user's OTHER repos: vision-native-llm and beyond-pixels are "the REPRESENTATION-THEORY twin of lunar-tie's build ... LUNAR-TIE = the THIRD sibling". 40 falsifiable ideas were banked this way (`S/GRAND-ARCHITECTURE.md` L423-424).

### 2.8 Frame H: three idea streams kept apart, then merged

`I/00` L7-41: Stream A (Hermes, the Jim Simons wave), Stream B (a separate Claude Code chat: SOTA matchers + campus lead), Stream C (the sih-2026 repo campaign). Each idea keeps its source; the flat log `I/12` gives every idea one row and a status (FIRED / LANDED / QUEUED / BUILD / LEAD / RULE).

---

## 3. How the idea became "big brain": the moves

Ordinary solution (the baseline everyone would ship): run SIFT or SuperGlue on an image pair, fit a homography, show matched dots. The MUJ/SAC 2025 paper is exactly that class: "SIFT, ASIFT, AKAZE, RIFT2, SuperGlue ... SuperGlue consistently won" (`I/06` L61-66). Below are the moves that turned it into LUNAR-TIE, in the order they appear in the record.

| # | move | what changed | evidence |
|---|---|---|---|
| M1 | **Reframe the task** | "the PS is not 'image matching': it is 'derive truth from sensors that disagree'. everyone will show a matcher. we show an ENGINE." | `S/GRAND-ARCHITECTURE.md` L437-438 |
| M2 | **Find "one generation behind"** | the closest prior work uses a 2020 model; "Nobody has published RoMa v2, MASt3R, or MatchAnything against OHRC/TMC-2/IIRS" | `I/06` L59-71; `CSD` L106-114 |
| M3 | **Go around the wall, not through** | do not match a ~300x gap in one hop; chain OHRC<->TMC-2 (~18x) and TMC-2<->IIRS (~16x) and compose | `I/07` L8-18; `CSD` L197-199 |
| M4 | **Read what the experts avoided (the TELL)** | "the Sept 2025 MUJ/SAC baseline did NOT match OHRC<->IIRS directly ... Even the team with direct SAC access treated LRO's cameras as the common intermediate" | `I/06` L104-110; `CSD` L225 |
| M5 | **Two independent paths, agreement = confidence** | internal bridge via TMC-2 + external bridge via LRO; "Where the two paths AGREE: strong sub-pixel registration with built-in confidence. Where they DISAGREE: diagnostic"; demo number "path A and path B agree to within X pixels on Y% of tie points" | `I/07` L62-76 |
| M6 | **Make your own ground truth with physics** | relight a DEM with the Lunar-Lambertian equation at many sun angles to get same-terrain, different-sun pairs "without needing to get lucky" in the archive | `I/07` L20-36; `I/06` L198-226 |
| M7 | **Remove the problem before the model sees it** | "Turns part of the sun-angle problem from 'the matcher has to be invariant to X' into 'we removed X before the matcher saw it'"; and a three-panel story: raw, normalized, matched | `I/07` L103-115 |
| M8 | **Cancel the gap with algebra** | quad-hash of 4 crater centroids: "any similarity lambda*z+mu cancels EXACTLY ... the 270-350x OHRC<->IIRS gap never gets matched across: it is CANCELLED algebraically, then refined locally" | `S/GRAND-ARCHITECTURE.md` L188-197 |
| M9 | **Put a theorem under the claim** | Cramer-Rao bound as the sub-pixel limit (`I/01` L62); FRI sampling: crater centroids "recoverable below the sampling floor ... subpixel BY THEOREM, not by interpolation" | `S/ideas/IDEATION-DEEP-02.md` L22-34 |
| M10 | **Honesty as a product feature** | abstain instead of a fake match; a FAILURE DEMO on stage; "judges remember the team that refuses to fake it" | `I/10` L66-69; `I/01` L85-86; `I/11` L27-31 |
| M11 | **Measure your own error with no labels** | loop-closure residual; "this is the eval story judges will love: 'we measure our own error without labels'" (untested, with a falsifier) | `S/ideas/IDEATION-DEEP-01.md` L47-54 |
| M12 | **Stand on fresh parts** | 7 pieces of 2026 lunar infrastructure (Moonstone, MoonAnything, StereoLunar, Lunar-G2R, cGAN normalization, OHRC SfS, DistillMatch); "we are assembling from parts, not building from bare metal" | `I/06` L159-196 |
| M13 | **Narrow, citable first-claim** | "first to repurpose a lunar multimodal foundation model for dense correspondence rather than masked reconstruction" | `I/07` L88-101 |
| M14 | **Second-order products ride on the first** | the registered grid feeds flare-quality calendars, PSR/ice ranking, rockfall detection, mineral stacks ("the fusion product nobody ships") | `S/GRAND-ARCHITECTURE.md` L216-234; `S/ideas/IDEATION-DEEP-02.md` L159-162 |
| M15 | **Turn a weakness into a lemma** | "appearance matching alone cannot bridge 300x" from three sources becomes a citable negative result, so "why geometry first" is "citable, not rhetorical" | `S/ideas/IDEATION-DEEP-01.md` L130-134 |
| M16 | **Use the people next door** | an MUJ student already co-publishes with the SAC scientists behind the data; "Finding and talking to this person is worth more than almost anything else on the todo list" | `I/06` L73-86 |
| M17 | **One picture a layman reads** | synthetic pair: naive SIFT NCC -0.021 / coverage 18.5% vs LUNAR-TIE NCC 0.973 / coverage 99.8% | `DEMO/comparison_stats.json` L2-5; image `DEMO/comparison_ours_vs_naive.png` |
| M18 | **Cross-corpus convergence** | three of the user's repos, from different fields, land on the same 3 principles (continuous geometry, physics first, calibrated uncertainty as the product) | `S/GRAND-ARCHITECTURE.md` L95-125 |

The pattern under all 18, in one line each:

```
  see the hard part  ->  find who already routes around it  ->  route around it twice
          |                                                         |
          v                                                         v
  make the hard data yourself (physics)          make the two routes check each other
          |                                                         |
          +---------------------> refuse when unsure <--------------+
                                         |
                                         v
                      show it as ONE picture + ONE failure on stage
```

What was still unbuilt when the big-brain story was written (do not copy the overclaim risk): "[ NOT started ] PANGU engine, LeJEPA pretraining, quad-hash MVP, IIRS ingest ... overall ~30-35% of the Dec product" (`S/GRAND-ARCHITECTURE.md` L428-432). What WAS built: a classical spine of 17 modules with 196/196 tests (`R0/README.md` L9-13, L48-75), on synthetic plus early real data.

---

## 4. Feasibility and strategy gates

### 4.1 The feasibility case (answering "it is impossible")

| teammate claim | verdict | why | source |
|---|---|---|---|
| "ISRO dropped this, impossible" | FALSE | ISRO published acceptance criteria; "Nobody publishes acceptance criteria for a problem they consider impossible." | `I/14` L12 |
| "300x gap makes matching impossible" | HALF TRUE | direct match is near-impossible, so the design chains the gap and anchors on crater graphs + SPICE | `I/14` L13 |
| "No data" | FALSE | sources named in the PS; "TBD" means a curated set will be ADDED | `I/14` L14 |

The "honest middle" lists where the doubter is right (`I/14` L67-89): the direct OHRC<->IIRS hop really fails ("1 IIRS pixel covers ~285x285 OHRC pixels"), uniformity is a real anti-cheat, sub-pixel is "the last expensive fraction", the dataset will come late, 1.21 billion pixels need memmap tiling, and ISRO has given no winner before.

### 4.2 The kill gate (the move that ended the argument)

`I/14` L91-104: a 7-day spike, "20 valid ties spread across 4 grid cells, or the plan commits to the kill gate (we pick the backup PS and lose nothing but 7 days)". The line to copy: "This is how you answer an aggressive no-sayer in a team: put the falsifiable test on the table, not a debate." (`I/14` L103-104). Same gate in `I/11` L25-31 with the rule "over a wrong number, we say 'we don't know'".

### 4.3 Risk register and probabilities (stated, not hidden)

`I/14` L141-157 grades each step (day-5 gate: high; sub-pixel OHRC<->TMC-2: good; IIRS sub-pixel: lower "and the design does not depend on it"). `I/09` L148-157 has six risks with first signal and action; the only FATAL one is "Fake claims in deck ... NEVER show unverifiable ties".

### 4.4 Process gates that kept the corpus honest

| gate | rule | source |
|---|---|---|
| DEEP or nothing | score >= 85, cite density >= 0.8 per K chars, table density >= 1 per 10K | `I/11` L44-47 |
| full-body reads | "wc -c byte match (user rule: never read first + last few sentences)" | `I/11` L47-48 |
| errata audit | 24 fixes, incl. 2 HIGH fabrications ("Twelve-million new maps", "<0.125 m") | `I/11` L55-58; `CONT` L262-305 |
| dead-URL calibration | 10,691 URLs, 3,213 HEAD-dead; GET sample: 53% alive, 17% blocked, 17% unreachable, 13% true 404 -> ~4% exposure; "don't over-claim '30% fabricated'" | `I/11` L55-58; `CONT` L385-416 |
| bug, not lie | 128 of the 501 "true 404s" were the team's own regex keeping backticks; the rest were moved NASA/USGS pages | `CONT` L1443-1459, L1497-1499 |
| 9-failure self-audit | e.g. "Wave map designed from my head (3rd violation ...)" | `I/11` L60-75 |
| gate-first build | ticket -> implementation -> independent gate run -> negative-gate battery -> lie-hunt -> fix -> append-only log | `R0/README.md` L27-40 |
| scope discipline | "what this repo is NOT": no learned models, no crater graph, no Ch-2 required, no sub-pixel claims yet | `R0/ARCHITECTURE.md` L63-67 |
| truth tiers | every metric stamped synthetic / public-benchmark / real-flight; "We do not ship a green bar on a red gate" | `R0/README.md` L110-126 |

---

## 5. Pitch package logic (what was built to land with judges)

Reminder from section 0: no judge outcome is recorded on disk. This is the design logic.

### 5.1 The order of the story

| beat | content | source |
|---|---|---|
| name + one-liner | LUNAR-TIE: "We make the Moon's own instruments agree, sub-pixel." | `I/10` L7-8 |
| 15-second hook | "Same crater. Different sun. Different instrument. 1.21 billion pixels per scene, and no way to compare them." then open the demo | `I/10` L12-16 |
| the wall | 20x scale, shadow inversion, modality, uniformity anti-cheat, sub-pixel | `I/10` L30-41 |
| the solution | 4 stages, 3 matcher tracks, 2 cross-scale anchors | `I/10` L45-54 |
| the demo | CLI tiles -> overlap proof -> THE SWIPE with clickable tie dots -> live metrics -> registered product -> FAILURE DEMO | `I/10` L56-69 |
| evidence | traceability matrix (every PS clause -> test -> metric), 3 baselines, scene holdout, 1-command rerun | `I/10` L71-77 |
| impact | plug-in for ISRO's PRADAN archive, reusable for multi-instrument missions | `I/10` L79-85 |
| the ask | 8 weeks, 6 roles, a week-1 deliverable that is itself a test | `I/10` L87-93 |

### 5.2 Why it was expected to land (the levers)

1. **Show it working live, not on a slide.** "A working comparison in real time reads completely differently from a static PPT slide of numbers." (`I/07` L38-48; `CSD` L203).
2. **Every dot is checkable.** "every tie point you click, you can verify" (`I/10` L123-124); "every tie point shown must be zoomable to its own pixels" (`I/08` L66-68).
3. **The failure demo.** "an intentionally hard pair -> system says 'insufficient geometry confidence, abstain' ... judges remember the team that refuses to fake it" (`I/10` L66-69).
4. **Three audiences, three one-minute versions.** sponsor judge (national data infrastructure), vision judge (the math), product judge (one command, no cloud, abstain over hallucinate) (`ROAST` L198-202).
5. **Analogies for non-experts.** cameras as "the microscope", "the normal camera", "the spectrum eye" (`ROAST` L40-61); scale invariance for a school kid: "large crater has small craters around it like islands around continent - pattern of distances to neighbors stays same whether zoomed or not" (`ROAST` L292-294); for a village elder: "If three eyes disagree, map wrong, rover drives wrong" (`ROAST` L304-306).
6. **Pre-answered hostile questions.** 40 Q&A incl. "What if judges ask an RMSE number you have not measured?" -> "On verified pairs our aim is X ... on hard variant we report abstain not number" (`ROAST` L324-326); "another GitHub repo already does it?" -> "Their own README says registration is not started" (`ROAST` L336-338; `I/10` L109-111); "wrong reference?" -> rejection layer + 50-negative test (`ROAST` L244-246).
7. **Fidelity audit before the pitch.** 5 issues found in the pitch itself (fabricated "12 million maps", unsourced "<0.125 m", invented "0.61" ratio, invented demo specs, a dropped qualifier) and fixed (`I/10` L126-134).
8. **The deck as engine, not matcher.** slide 1 reframe, slide 2 the built spine with "naive NCC -0.021 vs ours 0.9725", slide 6 the honesty layer, close "three corpora, one convergence" (`S/GRAND-ARCHITECTURE.md` L435-451).

---

## 6. ADAPTATION: a reusable recipe for the Hypnexis round

Everything in this section is my mapping, not extracted fact. Constraints it must respect come from the Hypnexis files and are cited.

### 6.1 What is different this time (the constraints, cited)

| constraint | SIH 2026 (LUNAR-TIE) | Hypnexis now | source |
|---|---|---|---|
| time | weeks (campaign 08-27 to 09-08+, finale Dec) | ends **06:00 IST 25 Oct 2026**; build window 17:30 to 05:00 | `H/research/WAVE-1-BRIEF.md` L9, L76-82 |
| code rules | own pipeline, gate-first | "Copying or forking any project from GitHub, Gitee or anywhere is fine. Judges care about what they see, not novelty of code" | WAVE-1 L10; `H/FLEET-BRIEF.md` L7 |
| judges | ISRO payload scientists who check geometry (`ROAST` L276-278) | "not deep tech experts. The project must look and sound mind-blowing to a common person and answer their 'what if this happens?' questions" | WAVE-1 L14 |
| deliverable | software + registered product + ties + metrics | live URL website; app only if run from the user's PC behind the site; YC-style deck; video last | WAVE-1 L13; FLEET-BRIEF L8 |
| look | dark dashboard swipe | santionispirits.com level (comic/woodcut WebGL, scroll story, motion, sound), base kit `~/site-clones/santioni` | FLEET-BRIEF L9 |
| statements | 229, pick 1 | 15, pick 1; P-A: AI-01..04, HM-01, HM-02, W3-01, W3-02 | WAVE-1 L11, L20-24 |
| team | 6 people + adviser | user + agent fleet | WAVE-1 L12 |

Consequence: keep the THINKING moves of section 3; drop the 241-run research machine, the paper, and the multi-week build.

### 6.2 The recipe (12 steps, each tied to the LUNAR-TIE move it reuses)

```
 [1 contract] -> [2 weighted pick] -> [3 frame + TELL] -> [4 fork bench] -> [5 around-the-wall merge]
                                                                                   |
 [12 lie-hunt] <- [11 hour gates] <- [10 site story] <- [9 what-if wall] <- [8 swipe] <- [7 self-check] <- [6 abstain]
```

| step | do this | reused from | done when |
|---|---|---|---|
| 1 write the scoring contract | Copy the statement's own words (the PS "Key Challenges" and "Explanation" lines) next to the judge rule "mind-blowing to a common person + answers what-ifs". This is the Hypnexis version of "ISRO tells you exactly how they will grade you" | `I/14` L33-34; WAVE-1 L14; `H/PROBLEM-STATEMENTS.md` | one table: clause -> how the site shows it |
| 2 weighted pick with the losing lenses shown | Score each P-A statement on 5-6 lenses, publish where the winner LOSES (as `ROAST` L194 did). Lens candidates from FLEET-BRIEF L12: forkable open work exists, core runs in a browser or hosted backend, visual story, what-if coverage, wow for a common person, kill risk. Weights are the user's call | `I/20` L18-22; `PICK-BOARD` L22 | user picks one with reasons in view |
| 3 Jim Simons transfer + the TELL | For the pick, write a 3-row minimum transfer map (field that already solved it -> exact transfer -> expected edge), the rule the M1 runs had (`I/02` L19-23). Then hunt the TELL: where do the best existing projects route AROUND the hard clause instead of through it? | `I/01` L53-72; `I/06` L104-110 | 3 rows + 1 TELL sentence with links |
| 4 fork bench, not a single fork | Line up 3-6 existing repos/models for the same clause, like Idea G's live table of 6+ matchers. Gate each with the replication rule: "official code + weights = buildable ... project-page-only = vaporware". Check licence and last commit (WAVE-1 L56) | `I/07` L148-158; `S/ideas/IDEATION-DEEP-02.md` L88-95 | 3+ forks that run, with URLs + fetched time |
| 5 merge two routes | Use two independent forks/methods for the core answer and treat agreement as confidence, disagreement as a diagnosis shown to the user | M5 dual-bridge, `I/07` L62-76 | the site can show "A and B agree / disagree because ..." |
| 6 abstain on stage | Build the "I do not know" path and put it in the demo on purpose | M10, `I/10` L66-69 | one scripted hard input that the system refuses |
| 7 self-check without labels | A number the system computes about its own answer (agreement rate, a validation query, a consistency re-check) | M11, `S/ideas/IDEATION-DEEP-01.md` L47-54 | number visible next to each answer |
| 8 one picture | A before/after view a non-expert reads in 2 seconds, like NCC -0.021 vs 0.973 (`DEMO/comparison_stats.json` L2-5). Naive tool on the left, ours on the right, same input | M17, M7 three-panel story `I/07` L109-111 | hero section of the site |
| 9 what-if wall | Pre-write the questions a common person asks, in persona form (school kid, elder, family, skeptic friend), and wire each answer to a live control on the site, the way `ROAST` answered 40 questions incl. personas | `ROAST` L206-366; `I/20` L26-34 | every what-if has a button or a scripted example |
| 10 site story in pitch order | Scroll beats follow the LUNAR-TIE pitch order: hook (one sentence + one picture) -> the wall (3 reasons it is hard, with numbers) -> the idea (go around the wall) -> live demo (swipe + clickable evidence) -> failure demo (abstain) -> what-if wall -> impact. Build on the santioni kit | `I/10` L12-93; FLEET-BRIEF L9 | all beats live on the URL |
| 11 hour gates (the day-5 gate, compressed) | Set falsifiable checkpoints with a switch-to-backup rule. Example (my proposal): if the merged core does not answer one real example end to end by an agreed hour, switch to the backup statement. Times are for the user to set inside the 17:30 to 05:00 window | `I/14` L91-104; WAVE-1 L76-82 | gate times written in DECISIONS, pass/fail logged |
| 12 lie-hunt before submit | Every number on the site and deck gets a source or the label "(aim)". The SIH pitch had 5 invented items before its audit | `I/10` L126-134; `CONT` L262-305 | zero untraced numbers |

### 6.3 What to drop from the SIH method (time, not value)

| SIH piece | why drop tonight |
|---|---|
| 241-run, 14-layer research machine (`I/03` L217-223) | weeks of runs; wave 1 already covers discovery |
| paper sequence (`I/08`) | no paper deliverable in Hypnexis (WAVE-1 L13) |
| self-computed J-wave numbers (`I/03` L126-141) | needs data downloads and days |
| 74-theory inventory (`I/05` L27-65) | keep only the 3-row transfer map from step 3 |
| gate-first per-module battery (`R0/README.md` L27-40) | keep the idea (independent check + lie-hunt) at site level, not per module |

### 6.4 First-guess mapping to the P-A statements (UNVERIFIED hypotheses, no research behind them)

These only show how the moves could apply. They are inputs for wave 1 to confirm or kill, not picks. The statement facts in column 2 are quoted from `H/PROBLEM-STATEMENTS.md`.

| id | statement hook (cited) | LUNAR-TIE move that maps | likely common-person what-if | abstain / failure demo |
|---|---|---|---|---|
| AI-01 | "keeps working on voice-cloning tools never seen during training" (L23); "Avoiding misleading shortcuts such as silence duration or loudness" (L38) | M5 two independent detectors, agreement = confidence; condition-split holdout like scene holdout (`I/01` L83-84) | "what if they clone MY mom's voice?" | clip too short or noisy -> "not enough evidence" |
| AI-02 | "returns the correct answer or acknowledges that it cannot answer" (L46); "A plausible but wrong answer is worse than none" (L51) | M10 abstain is literally in the PS; M11 self-check by row counts and value checks (L51) | "what if the data is wrong or the question makes no sense?" | an unanswerable question -> refusal with the reason |
| AI-03 | "Showing the exact graph path supporting every answer" (L84) | M17 one picture (graph zooms to the path); "every dot clickable" (`I/10` L123-124) | "how do I know it did not make that up?" | question with no support in the docs -> no path, says so |
| AI-04 | "show whether a wrong response came from retrieving the wrong chunks or from the model hallucinating" (L92) | M5 two routes tested apart = the PS itself; disagreement as diagnosis | "what if the AI lies confidently?" | red card on a planted hallucination |
| HM-01 | "never silently fills missing values" (L269); "Distinguishing 'not computed', 'not available' and 'not applicable'" (L284) | M10 truth tiers on every number (`R0/README.md` L116-118) | "what if I paste a broken molecule?" | broken SMILES -> precise reason, not "invalid" |
| HM-02 | "two brands that both contain paracetamol" (L297); "Too many minor alerts cause alert fatigue" (L299) | M7 remove noise before the user sees it; M17 one picture | "what if my grandmother takes both?" | unknown brand -> "cannot resolve, ask pharmacist" |
| W3-01 | "proves a specific fact ... revealing nothing else" (L121); "under-constrained signal ... forge a proof" (L128) | M10 show the forged-proof attempt failing on stage | "what if someone fakes being over 18?" | forged proof rejected live |
| W3-02 | "policies must hold even if the agent misbehaves" (L148) | M10 failure demo: the agent tries to overspend and the wallet blocks it | "what if the AI gets hacked and empties my wallet?" | out-of-policy payment held for owner approval |

Note on fit: AI-02, AI-04, HM-01, W3-01 and W3-02 put "refuse or catch the bad case" inside the statement text itself, which is where the LUNAR-TIE abstain move transfers most directly. This is an observation from the PS text, not a recommendation; selection belongs to the wave 1 board and the user.

### 6.5 The pitch skeleton, transposed (adaptation)

| LUNAR-TIE beat (`I/10`) | Hypnexis transposition |
|---|---|
| "Same crater. Different sun." hook | one sentence a common person feels (a scam call, a wrong prescription, a leaked wallet key), then the picture |
| "three eyes disagree" (`I/10` L118) | the everyday failure, in numbers from wave 1 (sourced) |
| 4-stage solution, 3 tracks | forks merged into 2 independent routes + a referee |
| THE SWIPE, clickable dots | before/after on the site, each claim clickable to its evidence |
| FAILURE DEMO | the scripted refusal |
| 40-question roaster | the what-if wall on the site plus a printed Q&A for the user |
| "abstain over lie" close | "it tells you when it does not know" |

---

## 7. Coverage audit and red-team

### 7.1 Files read (lines read vs `wc -l`, bytes per `wc -c`)

Method: the Read tool returned each file whole (no truncation notice); `sih-continue.txt` was read in 4 chunks (L1-450, L450-899, L900-1349, L1350-1771). Line counts match `wc -l` in every row. The tool does not report a char count, so bytes are `wc -c` of the file and "read" means every line was returned.

| file | wc -l | wc -c | lines read | full? |
|---|---|---|---|---|
| I/00-ORIGIN-PROVENANCE.md | 82 | 4,252 | 1-82 | yes |
| I/01-JIM-SIMONS-FRAME.md | 98 | 5,246 | 1-98 | yes |
| I/02-M1-WC-WAVES-FIRED.md | 212 | 11,550 | 1-212 | yes |
| I/03-QUEUED-WAVES.md | 223 | 11,986 | 1-223 | yes |
| I/04-FORWARD-MODEL-I-WAVE.md | 227 | 13,648 | 1-227 | yes |
| I/05-FACTOR-SPACE-UNIVERSE.md | 146 | 7,537 | 1-146 | yes |
| I/06-CLAUDE-CODE-FORENSICS.md | 253 | 13,581 | 1-253 | yes |
| I/07-CONTENT-IDEAS.md | 176 | 9,356 | 1-176 | yes |
| I/08-PAPER-AND-BENCHMARK-PLAN.md | 69 | 3,591 | 1-69 | yes |
| I/09-BUILD-BLUEPRINT.md | 157 | 8,090 | 1-157 | yes |
| I/10-PITCH-PACKAGE.md | 134 | 6,372 | 1-134 | yes |
| I/11-STRATEGY-GATES.md | 107 | 4,786 | 1-107 | yes |
| I/12-IDEA-LOG.md | 136 | 8,930 | 1-136 | yes |
| I/13-COMPLETENESS-AUDIT.md | 176 | 9,516 | 1-176 | yes |
| I/14-FEASIBILITY-CASE.md | 163 | 9,568 | 1-163 | yes |
| I/15-EMPIRICAL-CENSUS.md | 36 | 4,614 | 1-36 | yes |
| I/16-WEB-GRAPH.md | 96 | 9,507 | 1-96 | yes |
| I/17-VISION-LLM-DISSECTION.md | 113 | 14,397 | 1-113 | yes |
| I/18-FIELD-CHAIN-DISSECTION.md | 102 | 10,196 | 1-102 | yes |
| I/19-EXHAUSTIVE-ENUMERATION-MATRIX.md | 135 | 10,797 | 1-135 | yes |
| I/20-TEAM-ARMORY.md | 68 | 3,823 | 1-68 | yes |
| I/README.md | 81 | 4,802 | 1-81 | yes |
| S/ideas/README.md (differs from I/README) | 76 | 4,575 | 1-76 | yes |
| S/ideas/00..20 (21 files) | same as I/ | same as I/ | not re-read | byte-identical, `cmp` = SAME for all 21 |
| S/ideas/IDEATION-DEEP-01.md | 168 | 10,199 | 1-168 | yes |
| S/ideas/IDEATION-DEEP-02.md | 173 | 10,458 | 1-173 | yes |
| S/CAMPAIGN-PLAN.md | 90 | 8,542 | 1-90 | yes |
| S/GRAND-ARCHITECTURE.md | 450 | 27,104 | 1-451 (last line unterminated) | yes |
| S/INDEX.md | 207 | 11,394 | 1-207 | yes |
| S/research/PICK-BOARD.md (extra) | 33 | 5,640 | 1-33 | yes |
| ~/sih-progress/ROASTER-SIH26166.md (extra) | 374 | 30,515 | 1-374 | yes |
| FG (sih-field-guide/README.md) | 135 | 7,643 | 1-136 | yes |
| R0/README.md | 140 | 9,445 | 1-141 | yes |
| R0/ARCHITECTURE.md | 78 | 3,866 | 1-79 | yes |
| DEMO/comparison_stats.json | 5 | 145 | 1-6 | yes |
| DEMO/comparison_ours_vs_naive.png | n/a | 849,302 | viewed as image | yes (1 of 5 PNGs viewed) |
| CONT (Videos/sih-continue.txt) | 1,771 | 150,396 | 1-1771 in 4 chunks | yes |
| CSD (Videos/claude-sih data.txt) | 279 | 44,278 | 1-280 | yes |
| H/research/WAVE-1-BRIEF.md | 90 | 6,410 | 1-91 | yes |
| H/PROBLEM-STATEMENTS.md | 385 | 17,002 | 1-386 | yes |
| H/FLEET-BRIEF.md (extra) | 96 | 7,853 | 1-97 | yes |
| H/README.md (extra) | 13 | 654 | 1-14 | yes |
| ~/hermes_logs/ANSWER_PROTOCOL_2026-10-02.md (user rule) | 304 | 18,700 | 1-305 | yes |

Totals for the `wc` set (41 files incl. the extras, excluding the PNG and the 21 mirrors): 7,857 lines, 560,964 bytes, all lines returned.

### 7.2 Gaps in coverage (named, not hidden)

| item | status |
|---|---|
| `~/lunar-tie-demo` README | does not exist: the folder has only 5 PNGs + `comparison_stats.json`. I viewed `comparison_ours_vs_naive.png`; `A_ohrc_synth.png`, `B_tmc2_warp.png`, `registered_overlay.png`, `side_by_side.png` not viewed |
| `S/research/PITCH-SIH26166.md` (7,305 B), `~/sih-progress/PITCH-5MIN-SIH26166.md` (16,712 B), `S/research/TEAM-BRIEF-SIH26166.md` | NOT read; covered only through their digests `I/10`, `I/20`, `I/09` |
| the W4 landscape report that holds the 8.6 / 9.4 scores | NOT read; the scores are quoted as the team stated them |
| judge outcome of the internal pitch | NOT FOUND on disk (grep of `S/` root docs, section 0) |

### 7.3 Red-team of this file (graded)

| claim in this file | grade | why |
|---|---|---|
| "SIH list had 226" | VERIFIED with a caveat | 226 = published titles (`S/INDEX.md` L97); team worked on 229 live rows (`FG` L39) |
| SIH26166 was chosen by a 14-lens combined weighting | VERIFIED as the team's stated method | `I/20` L11-22, `ROAST` L145-194; the weights themselves were chosen by the team, not derived |
| SIH26166 was the "best" PS | UNVERIFIED | only the team's own scoring exists; single lenses rank it 5th (`ROAST` L194) |
| the pitch "landed with judges" | UNVERIFIED | no outcome recorded; section 5 is design logic only |
| LUNAR-TIE solved the 300x gap | EXAGGERATED if said | quad-hash, PANGU, IIRS ingest were "NOT started"; overall ~30-35% of the Dec product (`S/GRAND-ARCHITECTURE.md` L428-432) |
| NCC -0.021 vs 0.973 | VERIFIED, synthetic only | `DEMO/comparison_stats.json` L2-5; inputs are `A_ohrc_synth.png` / `B_tmc2_warp.png` (synthetic by name); no real-pair number of this kind found |
| 196/196 tests, 17 modules | VERIFIED as stated in the README, not re-run by me | `R0/README.md` L9-13, L87 |
| grand finale date | CONFLICT in sources | `I/11` L94-96 says 2026-09-20 grand finale; `I/README` L74-75 and `FG` L12-14 say Dec 2026 finale and 09-20 was the PS deadline (later sources win) |
| OHRC resolution | MINOR CONFLICT | 0.25 m/px in `I/06` L114-117 and `I/10` L20; "about 28 cm per pixel" in `CSD` L132 |
| section 6 per-statement mappings | UNVERIFIED (by design) | no research run; quoted PS lines are exact, the mappings are my hypotheses |
| "AI-02/AI-04/HM-01/W3-01/W3-02 contain the refuse/catch clause" | VERIFIED against PS text | `H/PROBLEM-STATEMENTS.md` L46, L92, L269, L128, L148 |

### 7.4 Style check

Run on this file 2026-10-24 before handing over (grep, case-insensitive): em dash U+2014 = 0, en dash U+2013 = 0, all 90+ phrases of the `~/AGENTS.md` AI-tell list = 0 hits. File size at check: 44,536 bytes.
