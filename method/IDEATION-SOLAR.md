# IDEATION-SOLAR.md: how the HackX solar campaign generated, tested and picked ideas, and how to reuse it on Hypnexis

v1, 2026-10-24, written by a claude subagent from a read-only pass over `~/hackx-solar`, `~/hackx-solar-hold`, `~/solar-lead-engine`, `~/solar-lead-engine-notes`, plus `~/hypnexis-main/research/WAVE-1-BRIEF.md` and `~/hypnexis-main/PROBLEM-STATEMENTS.md`.
Feeds lane L4 of WAVE-1-BRIEF (L72), whose merged output is `method/IDEATION-METHOD.md`.

Sections 1 to 4 and 6 are EXTRACTION: every point cites a file and line range (`L12-30`). Section 5 is ADAPTATION, NOT FROM THE SOLAR REPOS, and is marked as such.
Tags: VERIFIED = read on disk or computed this session. UNVERIFIED = not checked here. Paths are relative to `~` unless absolute.

The event, for context: HackX 4.0, Manipal University Jaipur, 11 to 12 Sep 2026, 36-hour in-person, Fintech PS #2 "Solar Lead Discovery and Qualification Engine" (`hackx-solar/CONTINUATION.md` L8-15). Team ORESHNK, product PRABHA (`solar-lead-engine-notes/ROUND3-SCRIPT-DREAM.md` L3-5). The team reached a 7-minute round 3 (`solar-lead-engine-notes/PRABHA-ROUND3-INDEX.md` L1-3). The final result is NOT FOUND on disk (grep for won/winner/prize/placed over the notes: 0 relevant hits).

---

## 0. Headline findings (read this first)

| # | finding | evidence | grade |
|---|---|---|---|
| F1 | No file, prompt or family is named "crazy" or "moonshot". The closest on-disk category is the **wild** family ("far transfer", deliberately far) in the idea generator. The user's own words "gold" and "monsters" map to `GUERRILLA-SIGNALS.md` and `MONSTER-HUNT-TRANSFER.md`. | `grep -rIli 'crazy\|moonshot'` over all four folders: 0 files. `hackx-solar/scripts/generate-idea-bank.py` L553-622. `hackx-solar/docs/PITCH-CONTEXT-AND-DIRECTIVES.md` L38-49 | VERIFIED |
| F2 | Ideas were NOT written by hand in bulk. A Python cross-product generator over 9 families made 9,140 raw combinations, 9,028 after exact dedupe, 8,071 after token-set Jaccard 0.82 dedupe (957 suppressed). Every entry carries trigger, mechanism, test, falsifier, cost, ring, and status NOT-TESTED. | raw and exact-dedupe counts computed this session by executing the generator's module body read-only; `ideas/IDEA-DEDUPE.md` L3; `ideas/IDEA-CENSUS.md` L3-17; generator L254-259, L729-772 | VERIFIED |
| F3 | No bank entry was ever tested as an entry. The census says all 8,071 are NOT-TESTED, and the tests that actually ran were about ten hand-picked hypotheses (section 3). The bank is a search space, used as a triage source, not a ranking. | `ideas/IDEA-CENSUS.md` L3, L36-52 | VERIFIED |
| F4 | The problem-statement pick and the mechanism pick were two different loops. The PS pick ran on 103 statements (keyword composite, 12 deep dossiers, a prior-art novelty pass, a startup lens, then the owner's call). The idea bank is solar-specific, so it was built after the pick to fill the chosen PS. | `vendored/event-repo/relations/RELATION-MAP.md` L1-19; `DECISION.md` L5-35; generator TARGETS L28-59 are all solar quantities | VERIFIED |
| F5 | The 10-dimension dossier rubric did not discriminate. In all 12 dossiers that carry it, novelty = 4 and demo-ability = 5. The pick was decided by the prior-art kill pass, the startup lens and the owner's "address" argument, not by the dossier scores. | grep of section F rows across `hackx-solar-hold/HX-*.md` (HX-001 L370-375, HX-002 L284-293, HX-016 L306-311, HX-023 L338-343, HX-028 L325-330, HX-038 L294-299, HX-055 L333-338, HX-057 L293-298, HX-067 L234-239, HX-070 L344-349, HX-083 L336-341, HX-090 L258-263) | VERIFIED |
| F6 | The strongest reusable pattern is the hypothesis loop: write a falsifier with every idea, run the cheapest test first (arithmetic before vision), publish the kill, then publish the correction when new data arrives. The guerrilla test is the full example: designed, killed by resolution arithmetic, then revived by street-level imagery with the retraction kept on the page. | `GUERRILLA-TEST-RESULT.md` L7-108 then L113-171 | VERIFIED |
| F7 | The pitch materials contain at least three claims that their own repo contradicts (the "one in twenty is wrong" guarantee, "seventy eight thousand crore", "lowered our yield by twelve percent"). Section 6.2 lists them so Hypnexis does not copy the error. | section 6.2 | VERIFIED |
| F8 | What the real room did: in round 3 the judges asked "Why not Jaipur?", "So it is a limitation, a blocker?" and "What about seasons and weather?". The first was answered weakly and the judge pressed. The deck used Leh while the app used Jaipur. | `solar-lead-engine-notes/ROUND3-HOSTILE-QA-ADDENDUM.md` L3-12, L18-23 | VERIFIED |

---

## 1. The ideation pipeline as actually run, step by step

### 1.1 The map

```
 103 statements, 106-page booklet
   |  parse + keyword clusters + composite score (ceiling, potential,
   |  winnability, frontend, novelty, bonus)  -> tiers A=2, B=4, C=97
   v
 12 deep dossiers, one fixed template (sections a..g), 10-dim winnability
   v
 NOVELTY-DERIVATION: lateral-transfer map, prior art BEFORE assertion,
   2 novelty claims killed, "judge distance" rule
   v
 TOP-5-STARTUP: money flow, data moat, incumbent response, follow-on, reference class
   v
 DECISION (owner): HX-002 solar, because of the address + money moving +
   demo written into the brief + the dual-axis mechanism
   v
 decomposition: 14 atoms, sets D / A / M (Class I, II, III), rings R0 / R1 / R2
   v
 ideation:  generator 9,140 raw -> 9,028 -> 8,071 (Jaccard 0.82)
            + 31 hand-written ideas with maths (degree 1..4)
            + 16 guerrilla inversions at the "oil-tank standard"
   v
 triage: ring, measurable falsifier tonight, a reason to exist;
   pre-register, report N
   v
 cheap tests: limits matrix, resolution arithmetic, precision falsifier,
   plausibility gates, PVGIS cross-check, territory citation audit
   v
 publish kills + corrections (KILLS K1..K11, KNOWN-DISAGREEMENTS, retractions)
   v
 DEMO-SCOPE: "not on screen in the 3-minute demo = not NOW"; 2 never-cut beats
   v
 pitch v1..v4, round-3 hooks, dream speech, hostile-QA repair after the room
```

### 1.2 The steps, with sources

| step | what was done | output | source |
|---|---|---|---|
| S1 | Parsed all 103 statements (10 themes) from the booklet; clustered them by build pattern ("a statement joins a cluster when its text matches the cluster pattern at least twice"); flagged near-duplicate statements at Jaccard >= 0.30 | theme census, 20 demand clusters, 1 near-duplicate pair | `vendored/event-repo/relations/RELATION-MAP.md` L1-19, L21-24, L301-307 |
| S2 | Scored every statement on 6 keyword-derived fields into a composite and a tier | `candidates-ranked.json`: tiers A 2, B 4, C 97. HX-002 solar ranked **6 of 103**, tier B, composite 2.52 (ceiling 3.0, potential 1.2, winnability 3.8, frontend 1.5, novelty 2.9). Top was HX-083 disaster early warning, 3.19 | `vendored/event-repo/relations/candidates-ranked.json`, parsed this session (VERIFIED) |
| S3 | Ran one deep research dossier per shortlisted PS on a fixed template: a demand, b money flow, c world competition, d prior art, e narrow novelty (mechanisms ranked by novelty to build cost), f winnability at a college hackathon (10 dimensions out of 5), g the 18-hour build, evidence ledger, next steps | 12 dossiers listed in `DECISION.md` L111-113; HX-002 rated 4.0/5 overall, "Go" | `hackx-solar-hold/HX-002.md` L1-12, L243-253, L276-293, L498; template headings in all 18 hold files (VERIFIED by heading grep) |
| S4 | Wrote the novelty derivation: first a lateral-transfer table ("which formal field already has machinery for this, and what breaks when you move it here"), then a prior-art search for every claim before writing it, then formal statements for survivors | 2 claims dead (HX-028 cross-modal deepfake, HX-002 satellite shading), 3 alive (HX-091 MUS/MaxSAT, HX-026 IRT, HX-001 affine arithmetic), ranked table | `NOVELTY-DERIVATION.md` L20-27, L31-46, L52-103, L105-172, L407-418 |
| S5 | Added the "judge distance" rule after the user relaxed the bar from world-first to "real, uncommon, competently applied": maximise the distance between the technique's home field and the panel's field | judge-distance audit table and re-ranked list | `NOVELTY-DERIVATION.md` L448-466, L467-489 |
| S6 | Scored the field by startup potential using the owner's own data-room tests | top 5: HX-002, HX-014, HX-026, HX-001, HX-016, each with a pre-registered kill test | `TOP-5-STARTUP.md` L18-41, L94-98, L140-144 |
| S7 | Owner picked HX-002 and recorded why and what was excluded, so the next session would not reopen it | the pick, five reasons, exclusion table, 5 mechanisms ranked by novelty to build cost, 5 risks | `DECISION.md` L5-35, L37-45, L68-78, L98-110 |
| S8 | Decomposed the PS into 14 atoms (only atom 2, roof geometry, is hard); enumerated every governing factor (set D), what the data gives (set A), and the missing set M split into Class I derivable, II inferable, III unavailable | atom table, D/A/M accounting, kill table of claims not to make | `SOLAR-WHOLE-MAP.md` L12-39, L43-152, L270-293 |
| S9 | Classified units into rings: R0 bare minimum, R1 rigor, R2 gold; units quarantined unless a research wave names them | 65 units: 38 R0, 17 R1, 10 R2 | `README.md` L1169-1189 |
| S10 | Ran the generator: targets x sources x mechanisms with compatibility filters, plus 8 other families; exact dedupe on (family, trigger, mechanism[:80]); Jaccard 0.82 near-dupe suppression keeping the first formulation | 8,071 ideas, census by family, ring and cost, a 180-entry tier-1 slice | generator L1-14, L25-249, L262-724, L729-772, L855-883; `IDEA-CENSUS.md` L5-34; `IDEA-BANK.md` L1-5 |
| S11 | Wrote 31 ideas by hand with their mathematics, grouped by distance from the problem: degree 1 load-bearing, degree 2 same principle new object, degree 3 from adjacent work, degree 4 different field same mathematical shape | IDEA 1 to IDEA 31 | `README.md` L434-1082 |
| S12 | Set an outside standard for cleverness (the floating-roof oil tank) and produced 16 "inversions" against it, each with a falsifier, then picked the 4 to defend and wrote an honesty section on what none of them are | `GUERRILLA-SIGNALS.md` | L12-62, L66-162, L166-181, L185-202 |
| S13 | Triage and test (section 3) | kills, corrections, constraint findings | `IDEA-CENSUS.md` L44-52; `MONSTER-HUNT-TRANSFER.md` L287-299 |
| S14 | Scoped the demo by one rule and a cut order fixed at hour zero | NOW / LATER / NEVER lists, 7 beats in 3:20 | `DEMO-SCOPE.md` L13-29, L33-51, L78-117, L120-156 |
| S15 | Built the pitch across four versions and three round-3 files, then repaired it after the real room | scripts, hooks, judge answers, hostile QA | `docs/PITCH-CONTEXT-AND-DIRECTIVES.md` L13-21; `solar-lead-engine-notes/ROUND3-*.md` |

Clock, as recorded: novelty derivation ~14:40 IST, top-5 ~15:00, pick ~15:15 on 2026-09-11, 14h 45m before the 06:00 submission (`NOVELTY-DERIVATION.md` L3, `TOP-5-STARTUP.md` L3, `DECISION.md` L3). DEMO-SCOPE was written with "about 12" hours left and 30 person-hours (`DEMO-SCOPE.md` L15-21).

---

## 2. The idea categories, with real examples quoted

### 2.1 The nine generator families (`scripts/generate-idea-bank.py`)

Counts are after dedupe, from `ideas/IDEA-CENSUS.md` L7-17. Raw counts before dedupe were computed this session.

| family | how it is generated | raw / kept | source |
|---|---|---:|---|
| inversion | target x source x mechanism, filtered by a class-to-source and class-to-mechanism compatibility table | 3,282 / 3,021 | L262-324 |
| adversarial | 25 failure modes x every mechanism as a countermeasure | 1,800 / 1,800 | L407-446 |
| business | 12 money models x 12 buyers x 12 value levers | 1,728 / 1,346 | L494-520 |
| product | 18 demo surfaces x a mechanism whitelist | 774 / 774 | L448-492 |
| honesty | 16 credibility instruments x the first 24 mechanisms | 384 / 384 | L522-551 |
| wild | 53 deliberately far fields x 10 atoms | 530 / 365 | L553-622 |
| orthogonal | 30 other industries x 14 atoms | 420 / 271 | L389-405 |
| decision | 14 decisions x a curated mechanism set | 94 / 94 | L326-387 |
| guerrilla | 16 visible proxies x 8 atoms | 128 / 16 | L624-724 |

Quoted examples (ids from `ideas/IDEA-BANK.jsonl` or `ideas/IDEA-BANK.md`, text verbatim):

**inversion**
- IDEA-00001: "we need usable roof area, and we have high-resolution optical imagery" / "cast-shadow geometry, H = L tan(theta), with error propagation"
- IDEA-00219: "we need roof orientation and tilt, and we have high-resolution optical imagery" / "shape from shading, I = R(p,q), with integrability constraints"
- IDEA-00319, a noise-floor example the census warns about (L40-43): "we need roof orientation and tilt, and we have night-time lights imagery" / "ISO-12233 slanted-edge MTF to state real resolution"

**decision**
- IDEA-03283: "the engine must block leads that are bright but unfinanceable" / "split conformal prediction with a finite-sample coverage guarantee"
- IDEA-03329: "the engine must decide when to stop qualifying and dispatch" / "LinUCB or Thompson sampling with regret bounds"

**orthogonal** (other industries that "solved a structurally identical problem")
- IDEA-03377: "actuarial pricing and risk pools solved a structurally identical problem, and our atom is prospect discovery" / "the transferable shape: pool a risk class, price it, and monitor adverse selection"
- IDEA-03470: "species distribution modelling solved a structurally identical problem, and our atom is routing and leakage" / "the transferable shape: predict presence from environmental covariates with biased samples"

**adversarial** (the "what could go wrong" family)
- IDEA-03797: "failure mode: a photo from another application is reused as evidence" / "countermeasure using cast-shadow geometry, H = L tan(theta), with error propagation" (`IDEA-BANK.md` L10-14)
- failure list entries: "every signal is perfect, which indicates an error rather than a gem" and "the feeder cannot accept the export, which invalidates the economics" (generator L416, L426)

**product** (demo surfaces)
- IDEA-05597: "demo surface: a single map of one industrial cluster with addressable kW as heat" (`IDEA-BANK.md` L829-833)
- IDEA-05640: "demo surface: a two-axis scatter where the blocked quadrant is visibly red" (`IDEA-BANK.md` L1087-1091)
- surface list entry: "a what-if panel showing the minimum change that flips a reject to an approve" (generator L463)

**business**
- IDEA-06371: "monetise as price per qualified lead with the solar EPC or installer as the buyer, improving cost per funded customer" (`IDEA-BANK.md` L283-287)
- the census's own named absurd case: "a homeowner priced per qualified lead" (`IDEA-CENSUS.md` L42-43)

**honesty**
- IDEA-08099: "credibility instrument: a frozen negative suite of leads that look viable and are not" (`IDEA-BANK.md` L556-560)
- IDEA-08123: "credibility instrument: a pre-registered mechanism list written before touching the held-out set" (`IDEA-BANK.md` L700-704)

**wild** (the closest thing on disk to "crazy ideas"; generator comment: "wild transfers, deliberately far", L553)
- IDEA-08483: "far transfer: spin-glass ground states applied to roof geometry" / "the shape: minimise a frustrated energy over discrete choices"
- IDEA-08751: "far transfer: cooperative game solution concepts applied to partner trust" / "the shape: a stable division when coalitions matter"
- IDEA-08884: "far transfer: causal structure discovery applied to finance readiness" / "the shape: learn the graph from conditional independences"
- falsifier template for the whole family: "the mapping is decorative: the imported structure reduces to a trivial baseline, or its assumptions fail on {atom}" (L619)

**guerrilla** (the user's "gold"; the standard is "a physically DETERMINISTIC function of a hidden economic quantity, visible in open imagery, invertible geometrically, and NOT already used by the incumbent industry", generator L625-628)
- "A solar water heater on the roof reveals an adopter ... It is not a prospect, it is a **revealed adopter**" (`GUERRILLA-SIGNALS.md` L73-94)
- "Diesel generator soot reveals already-paid backup cost ... Soot blackening is a **recorded history of generator runtime**" (L96-114)
- "Water tanker deliveries reveal panel-cleaning cost ... The water market reveals a solar maintenance cost" (L132-145)
- softer row: "construction stage across repeat imagery | the moment to approach" (L162)

The outside standard the guerrilla family was held to, stated as a formula (`GUERRILLA-SIGNALS.md` L57-62):

> Find a physical quantity that is a **deterministic function** of the hidden economic quantity you want, that is **visible in open data**, and that the incumbent industry **does not already read**.

### 2.2 The 31 hand-written ideas, by degree (`README.md` L434-1082)

| degree | meaning | example, quoted | lines |
|---|---|---|---|
| 1 | directly load-bearing | "IDEA 1. The conformal dispatch gate. *The highest-value idea in the project, and we already have working tested code for it.*" | L444-509 |
| 2 | same principle, different object | "IDEA 5. Condition-indexed dispatch instead of one global threshold." Unseen condition gets "a loud ABSTAIN rather than a heroic guess" | L614-640 |
| 3 | from adjacent work already researched | "IDEA 7. Roof corners as finite-rate-of-innovation signals." | L680-688 |
| 4 | different field, identical mathematical shape ("this is where the current plan has nothing") | "IDEA 10. 'Leads die after the quote' is a survival model." ; "IDEA 11. The questionnaire should ask the MINIMUM number of questions." (Wald SPRT: "a judge watches a lead get eliminated in two messages while a rival dashboard asks eight questions") ; "IDEA 16. A plausibility veto on suspiciously perfect leads." | L739-769, L773-804, L890-901 |

### 2.3 Event-level mechanisms from the novelty pass (other PSs)

| PS | formal object, quoted | lines |
|---|---|---|
| HX-091 Scheme Sarathi | "eligibility as SAT, explanation as MUS, household as MaxSAT" | `NOVELTY-DERIVATION.md` L182-245 |
| HX-026 Campus Phishing | "phishing simulation as a calibrated psychometric instrument" (2PL plus Fisher-information CAT) | L247-298 |
| HX-001 Underwriter | "affine arithmetic through the credit ratios, and referral as an information problem" | L300-362 |
| HX-002 Solar | "the dispatch decision, which is the part that is actually open": dispatch iff `P_v · P_c · R > C_visit + opportunity cost` | L364-403 |

---

## 3. The hypothesis-test loop

### 3.1 The rules of the loop

| rule | quoted source |
|---|---|
| every idea carries a test and a falsifier field | generator `add(family, trigger, mechanism, test, falsifier, cost, ring)` L254-259 |
| an entry earns effort only after three filters: ring (R0 first), "Falsifier measurability. If the falsifier cannot be measured with the data we have tonight, the entry goes to the queue", and "A reason to exist" | `IDEA-CENSUS.md` L44-50 |
| with about 20 labelled cases, pre-register and report N: "decide the mechanisms before looking at the held-out set, and write down how many were tried" | `IDEA-CENSUS.md` L52; `MONSTER-HUNT-TRANSFER.md` L283-299 |
| measure the ceiling before any model: "Build the lead limits matrix first" | `MONSTER-HUNT-TRANSFER.md` L89-119, L346-350 |
| a monster must survive honest out-of-sample attack; first tranche expects zero monsters | `README.md` L1191-1210 |
| kills are published, never deleted; corrections keep the old number visible | `CONTINUATION.md` L100-110; `KNOWN-DISAGREEMENTS.md` L49-51 |
| a gate must assert behaviour, not presence | `solar-lead-engine-notes/KILLS.md` L74-79 |

### 3.2 Tests that actually ran

| # | hypothesis | test | result | verdict | source |
|---|---|---|---|---|---|
| T1 | the brief's two buyers (home, SME) are symmetric | lead limits matrix, 48 cells, net of dispatch cost | residential 3 kW at 2.1 pc close: Rs 484 gross vs Rs 515 cost = **Rs -31**; commercial 100 kW: **Rs 15,613**; 45 of 48 viable, all 3 dead cells residential; paid search flips residential to Rs -947 | KILLED the symmetry; strategy changed to commercial and SME first | `LIMITS-MATRIX-FINDINGS.md` L16-65, L79-91 |
| T2 | a solar water heater can be detected from free imagery | resolution arithmetic against published detection work | 2 m x 1 m object at Sentinel-2 10 m = **0.2 x 0.1 pixels**; Google Solar API page had 0 India mentions; Bhuvan forbids bulk use | test designed, run blocked; "a constraint, not a null result" | `GUERRILLA-TEST-RESULT.md` L7-32, L34-48, L99-108 |
| T2b | (same, after the data-source wave) | source check of street-level imagery for Jaipur | Mapillary free for commercial use, Google Street View metadata free, Mappls names Jaipur; binding limit becomes coverage density and roadside sampling bias | earlier conclusion RETRACTED in place; test back on | `GUERRILLA-TEST-RESULT.md` L113-171 |
| T3 | the conformal gate guarantees precision of dispatched leads | `scripts/falsify-precision-claim.py` across base rates and score quality | coverage held everywhere; precision ranged 1.00 to 0.10 with weak scores | precision claim KILLED; coverage claim kept | `README.md` L466-499 |
| T3b | the shipped gate filters leads | independent re-run at several alpha values | at alpha 0.10: dispatch 0.899, precision 0.055, lift 1.09x | "a calibration tool, not a qualification filter" | `KNOWN-DISAGREEMENTS.md` L96-127 |
| T4 | the placement engine prints physically possible numbers | two plausibility gates plus a coverage-ratio check | caught 98.7 kWh/m2/day (diffuse added hourly), a 33-year payback (inverted efficiency), a hardcoded 0.61 coverage factor, and a hand-copied table | 3 bugs plus 1 transcription error fixed | `FINDING-ARCHITECTURE.md` L214-247 |
| T5 | optimal tilt is 25 degrees, not 27 | PVGIS v5.2 at the same site | PVGIS says 31; yield 8 pc optimistic | claim "overstated"; direction of flat vs tilted kept | `KNOWN-DISAGREEMENTS.md` L59-94 |
| T6 | the shadow window covers the day | sibling-function comparison, independent pass | window was 20.0 to 38.0 h; clear cells 65.6 pc -> 55.3 pc, flat 41.6 -> 35.1 kW | FIXED, old numbers kept in the table | `KNOWN-DISAGREEMENTS.md` L14-57 |
| T7 | our novelty claims are new | prior-art search before writing | HX-028 cross-modal and HX-002 shading both published | 2 KILLED | `NOVELTY-DERIVATION.md` L55-103 |
| T8 | the 15 territory research passes are citable | URL and Sources-section count per file | 1 of 15 has resolvable URLs (L10); 387 falsifiers, 1,130 NOT FOUND markers | 13 demoted to "method and falsifiers only" | `TERRITORY-AUDIT.md` L12-76 |
| T9 | annual generation is right; the two axes are independent; the demo case is stable; the gate fixed shading | property tests, mutation, sensitivity table | factor of 1000 in two lines (K1); finance axis ~93 points project terms vs 18 customer facts (K7); 1 pc shading moves the case through 3 of 4 quadrants (K8); helper had no caller (K11) | 11 kills K1 to K11, published | `solar-lead-engine-notes/KILLS.md` L7-79 |

### 3.3 The shape of one loop, as the guerrilla test ran it

```
idea with falsifier          "water-heater roofs convert better"      GS L73-94
  -> cheapest decisive test   pixel arithmetic, not a CV model          GTR L17-32
  -> result as a constraint   0.2 x 0.1 px, so satellite is out          GTR L50-56
  -> rescope the claim        demo-only on hand tiles, future paid feed  GTR L57-68
  -> next correct test        3-5 roof visual check, one hour            GTR L87-97
  -> new evidence arrives     street-level covers Jaipur                 GTR L119-136
  -> publish the retraction   "the conclusion was too strong"            GTR L115-118, L168-171
  -> new honest limitation    coverage density + roadside sampling bias  GTR L152-166
```

---

## 4. The pick logic

### 4.1 Which statement (event level)

| filter | HX-002 solar position | source |
|---|---|---|
| keyword composite over 103 | rank 6, tier B (not top) | `candidates-ranked.json` (computed) |
| deep dossier | 4.0/5, "Enter this problem" | `hackx-solar-hold/HX-002.md` L10 |
| novelty after prior art | rank 4 of 5: "keep the demo, drop the novelty claim"; the author's own pick was HX-091 then HX-026 | `NOVELTY-DERIVATION.md` L412-425 |
| judge distance | rank 5 of 5: "the best demo, the weakest novelty claim" | `NOVELTY-DERIVATION.md` L483-489 |
| startup lens | rank 1: money moving, Aurora absent from India, closed-loop outcome data as moat | `TOP-5-STARTUP.md` L35-41, L45-98 |
| owner's call | picked, deciding factor "the address": Jaipur in Rajasthan, first ten EPC customers reachable by road; organiser wrote the demo into the bonus clause | `DECISION.md` L13-35; `TOP-5-STARTUP.md` L254-266 |
| exclusions | Open Innovation theme ("comparatively more rigorous" judging); HX-091 by owner's call despite best novelty; HX-026 wrong beachhead; HX-014 second; HX-028 no wedge | `DECISION.md` L37-45 |

So novelty lost to buildability, money and locality. The repo says this openly: "The uncertainty is honest and it is the TAM" (`TOP-5-STARTUP.md` L263-266).

### 4.2 Which mechanism (inside the PS)

| reason | quoted source |
|---|---|
| it is the failure the organisers named: "leads die after the quote, at financing, because nobody checked affordability at the top of the funnel ... This sentence is our entire angle" | `README.md` L176-186 |
| "a reason to exist": "it is not a searched pattern, it is the failure the organisers named" | `MONSTER-HUNT-TRANSFER.md` L294-298 |
| cheap, one sentence, best demo beat: "a roof that looks perfect, gets a high score, and then a red gate stops it with a reason" | `README.md` L413-420 |
| two independent paths agreed (own dossier and the teammate's diagram) | `README.md` L421-423 |
| novelty to build cost 5/5 vs 2/5 in the dossier | `DECISION.md` L72-78; `HX-002.md` L245-253 |
| not claimable as novelty: discovery and joint scoring "is the assignment", "is the requirement" | `README.md` L1270-1281 |

### 4.3 What goes in the demo

- The rule: "if an item does not appear on screen in the three-minute demo, it is not a NOW item. No exceptions, including items that are intellectually the best thing we have." (`DEMO-SCOPE.md` L27-29)
- Two beats carry the pitch: the roof screen (where the panels go) and the blocked bright-but-unfinanceable roof, "85 seconds of 200 ... If only two things work, they must be N4 and N5." (L120-141), never cut (L156).
- Cut order agreed at hour zero, bottom dies first (L145-156). LATER is a plan, "a silently-dropped item is a lie" (L97-98). NEVER list: login, any trained model, CRM, nationwide claims (L102-116).
- Precompute the records and run the engine live on one address if asked "is this live?" (L160-174). Seeded, no-network fallback from hour zero (`DECISION.md` L102-110).

### 4.4 What was planned to impress judges, and what happened

| planned | source |
|---|---|
| success = the judge can say three things: "I understand what this does and who pays for it", "The two numbers they showed me were computed, and I could re-run it", "They showed me something they rejected and defended it" | `guide/02-WHAT-WE-ARE-BUILDING.md` L171-180 |
| open with silence and a real object (an A3 satellite print of a real roof), then a surprising number ("Minus thirty-one"), then a question; never open with your name | `ROUND3-HOOKS-AND-SCRIPT-V2.md` L8-10, L137-173 |
| "The speech sells the dream. The tech is the receipt." Three memorised lines: "Everybody sells contact. We sell evidence." / "We were wrong by a factor of one thousand, and we found it ourselves." / "Have you actually looked at the roof?" | `ROUND3-SCRIPT-DREAM.md` L7-16, L284-288 |
| ask the audience questions and answer them; childish examples (rubber duck in a bath, soot behind a scooter exhaust, counting fans outside a shop) | `PITCH-CONTEXT-AND-DIRECTIVES.md` L65-87 |
| "This is not larp": name seven existing parts built by others, "And not one of them joined to the others" | `docs/PITCH-SCRIPT-v3.md` L287-315; honesty limit `PITCH-CONTEXT-AND-DIRECTIVES.md` L202-221 |
| a ticker: "one rupee every thirty-six seconds" for a 100 kW roof, computed from engine yield and tariff | `PITCH-SCRIPT-v3.md` L111-157, L461-466 |
| a what-if table in the room's words ("what if it rains, or hails", "is it actually built", "what stops Google", "what if the customer cannot pay") | `PITCH-v4-NEW-BEATS.md` L292-334 |
| state vocabulary for "is it built": built vs designed, "never claim a design as a build and never apologise for a design being a design" | `PITCH-SCRIPT-v3.md` L448; `ROUND3-QA-AND-TECH.md` L9-36 |
| a NOT FOUND register said proudly: "every other team in the room will have an answer for everything" | `ROUND3-QA-AND-TECH.md` L176-193 |

What happened (the only record of the real room): three questions, one answered weakly ("not enough data yet, no time yet"), the judge pressed with "limitation" and "blocker". The repair: "a limit is something that cannot be done TODAY", priced as "hours, rupees, and one dataset", and "Do NOT say: we ran out of time" (`ROUND3-HOSTILE-QA-ADDENDUM.md` L18-70). The seasons question was the best one and the data covered it (L72-95).

---

## 5. ADAPTATION, NOT FROM THE SOLAR REPOS: a recipe for the Hypnexis round

Everything in this section is a proposal. Facts about Hypnexis come from `research/WAVE-1-BRIEF.md` and `PROBLEM-STATEMENTS.md`; any example idea below is a HYPOTHESIS until a wave-1 lane verifies it.

### 5.1 What is different this time

| solar (Sep) | Hypnexis (Oct), from WAVE-1-BRIEF L5-16 | consequence for the method |
|---|---|---|
| novelty of mechanism was scored hard; forking not the plan | "Copying or forking any project from GitHub, Gitee or anywhere is fine. Judges care about what they see, not novelty of code" | drop the prior-art kill as a gate on code; keep it only as a wording rule ("we built on X"), and score bases instead |
| judges: fintech jury, one pressed hard on data | "not deep tech experts ... mind-blowing to a common person and answer their 'what if this happens?' questions" | "judge distance" (S5) becomes a strength by default; the scarce thing is a visible wow plus live answers to what-if |
| deliverable: demo page plus pitch | live URL website, YC-style deck, video only if time | the site is the demo and the pitch; DEMO-SCOPE's rule applies to the site |
| ~15 h from pick to submission | build 17:30 to 05:00, about 11.5 h (L80-83) | cut order and NEVER list at hour zero, same as DEMO-SCOPE |
| 103 statements | 8 P-A statements, 6 P-B wow scan, HW-01 out (L18-24) | the S1 to S7 funnel shrinks to one evening table |

### 5.2 The recipe, step by step

**R1. One rubric over the 8 P-A statements, forced to spread.** F5 showed a 1-to-5 rubric where every row scored 4 and 5. Fix: rank the 8 statements 1 to 8 on each column instead of scoring them, so ties are impossible. Columns (proposal): wow for a common person in 10 seconds; number of judge what-ifs the demo can answer live; best forkable base exists and runs (licence, last commit, weights or demo); runs from a website (in-browser, hosted, local only, per WAVE-1-BRIEF L57); hours to a demo on our own data; one honest failure we can show and defend. Keep the solar habit of a written exclusion table (`DECISION.md` L37-45).

**R2. The limits matrix, renamed "what the statement permits".** Before choosing features, write for each statement the ceiling a 3-minute demo can show and the cost of each beat, exactly as the lead limits matrix measured what a cell permits before any scoring (`MONSTER-HUNT-TRANSFER.md` L89-119). Kill any statement whose best beat needs data or hardware we cannot get tonight.

**R3. The oil-tank formula, turned into a wow formula.** Solar asked for "a physical quantity that is a deterministic function of the hidden quantity, visible in open data, that the incumbent does not read". The judge-facing version: find the hidden thing the user cannot see today, and make it visible as a deterministic, checkable picture. Hypotheses to test per statement (UNVERIFIED, for lanes L1 to L3 to confirm or kill):
- AI-04: the exact retrieved chunk lights red beside the hallucinated sentence, so "retriever or generator?" is answered by looking.
- AI-03: the graph path behind every answer zooms and highlights, which the statement already asks for (`PROBLEM-STATEMENTS.md` L76).
- HM-02: two brand names that both hide paracetamol, shown as one shared ingredient node.
- AI-01: the same sentence in a real voice and a cloned voice, with the detector's verdict on a generator it never saw.

**R4. Run the generator idea, smaller.** Reuse the structure of `generate-idea-bank.py` (fields trigger, mechanism, test, falsifier, cost, ring; exact dedupe; Jaccard 0.82) with Hypnexis axes: base repo x feature x demo surface x what-if. Add one family solar never had: **fork-merge** (base A + base B + our join). Keep the census rule "Nothing here is canon" (`IDEA-CENSUS.md` L36-38) and cap the bank: 8,071 entries were never tested, so a bank bigger than a few hundred is noise tonight.

**R5. The what-if family is the adversarial family.** Solar's adversarial family was "failure mode x countermeasure" (generator L407-446) and its pitch carried a what-if table in the room's words (`PITCH-v4-NEW-BEATS.md` L292-334). For Hypnexis, make each what-if a button on the site that runs live, not a slide. Solar already had the surface idea: "a what-if panel showing the minimum change that flips a reject to an approve" (generator L463). Lane L3 supplies the 5 common-person questions per statement (WAVE-1-BRIEF L70).

**R6. Pre-register, test cheap, publish the kill.** For the chosen statement, write 3 to 5 hypotheses with falsifiers before building, run the cheapest decisive test first (arithmetic, a 5-sample check, a licence check), and put a short "what we killed" strip on the site. In solar this was the most reused pitch beat (K1 factor of 1000, `KILLS.md` L7-12).

**R7. The demo-scope rule, unchanged.** Not on screen in the 3-minute run = LATER. Two never-cut beats chosen at hour zero. Seeded offline fallback so no network call controls the pitch (`DEMO-SCOPE.md` L27-29, L145-156; `DECISION.md` L108-110).

**R8. The pitch spine, mapped to one santioni-level site.** One scroll story with the solar beat order: silent hook and real object, a surprising number, a question to the visitor, the hidden thing made visible (R3), the live what-if buttons (R5), "this is not larp" naming the forked projects as the proven parts we joined (`PITCH-SCRIPT-v3.md` L287-315, which is exactly a fork-merge story told honestly), the kill strip (R6), built vs designed, the close returns to the opening object. The santioni look kit lives at `~/site-clones/santioni` with 7 of 19 reference elements done and 9 partial as of 2026-10-11 (from the user's memory note, UNVERIFIED this session), so budget kit reuse, not a rebuild.

**R9. The answer bank before the room.** Write the 8 judge answers the way `docs/judge-answers.md` L1-6 did ("If you do not know an answer, say 'I do not know, and here is how we would find out.'"), plus the limit-vs-blocker line from the hostile QA (`ROUND3-HOSTILE-QA-ADDENDUM.md` L51-61). Make the deck, the site and the app use the same city, dataset and numbers, because the Leh vs Jaipur split is what the real judge attacked (L9-12).

**R10. What not to port.** The 103-statement keyword composite (8 statements do not need it). The 15 long territory passes whose citations did not resolve (`TERRITORY-AUDIT.md` L43-45). Any guarantee phrased as precision (section 6.2).

### 5.3 Clock for tonight (proposal)

```
17:00  wave 1 closes            R1 rank table + R2 permits table   (30 min)
17:30  user picks               R3 wow hypotheses + R6 pre-register (30 min)
18:00  fork base, freeze scope  R7 NOW/LATER/NEVER + cut order     (15 min)
18:15  build                    two never-cut beats first
02:00  site story + what-if buttons wired to live runs
04:00  answer bank + deck from the same numbers; rehearse twice
05:30  freeze; offline fallback tested
06:00  deadline (WAVE-1-BRIEF L9)
```

---

## 6. Red team of this file, and coverage audit

### 6.1 Claims in this file, graded

| claim | grade | why |
|---|---|---|
| no "crazy" or "moonshot" file exists | VERIFIED | recursive grep, text files, 0 hits |
| 9,140 / 9,028 / 8,071 counts | VERIFIED | generator executed read-only this session; 8,071 also matches census and jsonl line parse |
| HX-002 composite rank 6 of 103 | VERIFIED | parsed `candidates-ranked.json` this session |
| dossier rubric novelty 4 and demo 5 in 12 of 12 | VERIFIED | grep of section F rows; HX-026-impl and HX-091 files carry no such rows |
| the bank was built after the pick | VERIFIED as inference from content | every TARGET in the generator is a solar quantity (L28-59); no timestamp for the generator run was found |
| the round-3 result | NOT FOUND | no file records it |
| section 5 recipe | UNVERIFIED by design | adaptation, not tested |

### 6.2 Contradictions inside the solar repos (do not copy these)

| claim in the pitch | what the repo itself says | grade of the pitch claim |
|---|---|---|
| "Of the leads we pass, **at most one in twenty is wrong**, and that number is a guarantee" (`ROUND3-SCRIPT-DREAM.md` L87-88; same in `PITCH-SCRIPT-v3.md` L382, `ROUND3-QA-AND-TECH.md` L124-130) | coverage is guaranteed, precision is not: "It is **not** a precision guarantee", precision 0.280 on base rate 0.25 (`docs/judge-answers.md` L78-89); "a calibration tool, not a qualification filter" (`KNOWN-DISAGREEMENTS.md` L123-127) | WRONG as worded |
| "India has been handed **seventy eight thousand crore rupees**" (`ROUND3-SCRIPT-DREAM.md` L56, L219) | outlay Rs 75,021 crore (`HX-002.md` L4); Rs 28,024 crore released by 4 Aug 2026 (`PITCH-MODEL.md` L132-133); Rs 78,000 is the per-household 3 kW subsidy band | WRONG (rupee band confused with crore outlay) |
| "we **lowered** our own yield by twelve percent" (`ROUND3-SCRIPT-DREAM.md` L125-126) | yield went 1,418.63 to 1,349.32, about 4.9 pc (`ROUND3-QA-AND-TECH.md` L161-162); v3 says "about five percent" (`PITCH-SCRIPT-v3.md` L352); 12 pc is a separate gap to the European reference (`ROUND3-QA-AND-TECH.md` L63-64) | EXAGGERATED (two numbers merged) |
| "All three dead cells are residential at the industry-average conversion rate" (`LIMITS-MATRIX-FINDINGS.md` L46-47) | README corrects it: two at industry average, one at good-EPC, "which the CSV contradicts" (`README.md` L233-236) | WRONG in the findings file, corrected only in README |
| "The optimal tilt is 25 degrees, not the textbook 27" still stated in README (L300-303) | PVGIS puts it at 31; "The tilt claim is overstated" (`KNOWN-DISAGREEMENTS.md` L66-79) | EXAGGERATED, correction not propagated |
| census shows guerrilla = 16 as if 16 ideas x atoms | the generator emits 16 x 8 = 128, and the exact-dedupe key (family, trigger, mechanism[:80]) ignores the atom, so 112 collapse silently (L712-724 vs L733-737) | the "16" is correct; the atom cross-product never survived, which the census does not say |

### 6.3 Coverage audit (bytes read vs `wc -c`)

Fully read with the Read tool, every line: 31 files, **606,154 bytes** (`cat | wc -c` this session).

| file | wc -c | read | status |
|---|---:|---:|---|
| hackx-solar/README.md | 73,051 | 73,051 | FULL |
| hackx-solar/ideas/IDEA-BANK.md | 83,099 | 83,099 | FULL |
| hackx-solar/scripts/generate-idea-bank.py | 56,181 | 56,181 | FULL |
| hackx-solar-hold/HX-002.md | 61,404 | 61,404 | FULL |
| hackx-solar/NOVELTY-DERIVATION.md | 30,154 | 30,154 | FULL (byte-identical to vendored/event-repo copy, cmp) |
| hackx-solar/docs/PITCH-SCRIPT-v3.md | 26,657 | 26,657 | FULL |
| hackx-solar/vendored/event-repo/relations/RELATION-MAP.md | 18,259 | 18,259 | FULL |
| hackx-solar/SOLAR-WHOLE-MAP.md | 18,356 | 18,356 | FULL |
| solar-lead-engine-notes/PITCH-v4-NEW-BEATS.md | 16,902 | 16,902 | FULL |
| hackx-solar/MONSTER-HUNT-TRANSFER.md | 16,280 | 16,280 | FULL |
| hackx-solar/TOP-5-STARTUP.md | 15,362 | 15,362 | FULL (identical to vendored copy) |
| hackx-solar/docs/PITCH-CONTEXT-AND-DIRECTIVES.md | 14,509 | 14,509 | FULL |
| hackx-solar/GUERRILLA-SIGNALS.md | 14,409 | 14,409 | FULL |
| solar-lead-engine-notes/PITCH-MODEL.md | 13,145 | 13,145 | FULL |
| hackx-solar/FINDING-ARCHITECTURE.md | 12,722 | 12,722 | FULL |
| solar-lead-engine-notes/ROUND3-QA-AND-TECH.md | 12,430 | 12,430 | FULL |
| solar-lead-engine-notes/ROUND3-SCRIPT-DREAM.md | 11,633 | 11,633 | FULL |
| hackx-solar/DEMO-SCOPE.md | 10,504 | 10,504 | FULL |
| hackx-solar/GUERRILLA-TEST-RESULT.md | 9,870 | 9,870 | FULL |
| solar-lead-engine-notes/ROUND3-HOOKS-AND-SCRIPT-V2.md | 9,796 | 9,796 | FULL |
| hackx-solar/TERRITORY-AUDIT.md | 8,775 | 8,775 | FULL |
| hackx-solar/LIMITS-MATRIX-FINDINGS.md | 8,685 | 8,685 | FULL |
| hackx-solar/KNOWN-DISAGREEMENTS.md | 7,707 | 7,707 | FULL |
| hackx-solar/DECISION.md | 7,671 | 7,671 | FULL (identical to vendored copy) |
| solar-lead-engine-notes/ROUND3-HOSTILE-QA-ADDENDUM.md | 6,116 | 6,116 | FULL |
| hackx-solar/CONTINUATION.md | 5,886 | 5,886 | FULL |
| hackx-solar/docs/judge-answers.md | 5,836 | 5,836 | FULL |
| solar-lead-engine-notes/KILLS.md | 4,993 | 4,993 | FULL |
| hackx-solar/ideas/IDEA-CENSUS.md | 2,350 | 2,350 | FULL |
| hypnexis-main/PROBLEM-STATEMENTS.md | 17,002 | 17,002 | FULL |
| hypnexis-main/research/WAVE-1-BRIEF.md | 6,410 | 6,410 | FULL |
| hackx-solar/research/territory/T-what-if-missed.md | 88,765 | 28,164 | PARTIAL, lines 1-120 of 505 (verdict, omitted variables, no-go argument) |
| hackx-solar/guide/02-WHAT-WE-ARE-BUILDING.md | 8,781 | 4,722 | PARTIAL, lines 95-183; other guide files grep only |
| hackx-solar/ideas/IDEA-DEDUPE.md | 16,665 | 1,900 | PARTIAL, first 1,500 and last 400 bytes; the rest is an id table |
| 17 other `hackx-solar-hold/HX-*.md` dossiers | 1,039,073 | 36,536 | STRUCTURE ONLY: headings, section F score rows, decision lines (3.5 pc) |
| hackx-solar/ideas/IDEA-BANK.jsonl | 4,993,128 | parsed | MACHINE-PARSED: family counts plus 20 sampled entries |
| hackx-solar/vendored/event-repo/relations/candidates-ranked.json | 42,942 | parsed | MACHINE-PARSED: all 103 rows |

Not read (named in the brief or nearby, left for a second pass): `PITCH-SCRIPT-v2.md` (22,014), `SIH-METHOD-TRANSFER.md` (42,428), `SIH-TO-SOLAR-TRANSFER.md` (22,111), `TEAMMATE-PROPOSAL-AUDIT.md` (15,893), `INCOMPLETE-WORK.md` (10,677), `AUDIT-LOG.md` (19,131), `MASTER-STATUS.md` (11,693), guide files 00, 01, 03 to 10, the other 14 territory passes, `research/data-sources/DS1-DS10`, `vendored/sih-method/ideas/*` (the SIH ideation is lane L4's separate input), and the rest of `solar-lead-engine-notes` (FINAL-PLAN, ROADMAP, PRABHA-*, HAZARDS, and others). Folder totals for scale: hackx-solar 196 .md files, 5,062,029 bytes; hackx-solar-hold 19 .md, 1,100,767; solar-lead-engine 16 .md, 94,278; solar-lead-engine-notes 47 .md, 447,011.
