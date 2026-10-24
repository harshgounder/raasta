# SELECTION-FRAMEWORK.md: how the two repos pick a problem, and how to use it on Hypnexis

v1, 2026-10-24, written by a claude subagent from a read-only pass over `~/startup-idea-lab` and `~/startup-universe`.
Sections 1 to 3 and 5 are extraction: every point cites a file (and lines where useful). Section 4 is ADAPTATION, NOT FROM THE REPOS, and is marked as such.
Tags: VERIFIED = checked on disk this session. UNVERIFIED = claim not checked here.

---

## 0. Headline findings (read this first)

| # | finding | evidence | grade |
|---|---|---|---|
| F1 | `startup-idea-lab` has NO script or prompt that ranks ideas or problems. Every script scores research REPORTS (depth/citation density), not ideas. | `scripts/report-supervisor.py` docstring L2-27; `scripts/calibrate.py` L1-33; `scripts/redo-wave.py` L1-26; `scripts/launch-idea-runs.py` L1-6 | VERIFIED |
| F2 | The idea-mining stage ("STAGE B") was planned and never built. | `CONTINUATION-PIPELINE.md` L197 "STAGE B ... NOT YET BUILT"; `CONTINUATION-MASTER.md` L200; `MAPPING.md` L17; `RESUME-PROMPT.md` L31; `WAVE-TRACKER.md` L77 | VERIFIED |
| F3 | The actual idea-selection rubrics live as TEXT inside the generated research reports in `results/` (scorecards, weights, kill gates), plus a synthesis in `research/methodology-masterdoc.md`. | section 2 below | VERIFIED |
| F4 | `startup-universe` holds a teaching version of the same logic: problem scoring table, 5-rung evidence ladder, build gate, hypothesis + pre-registered kill criteria. | `01-problem-discovery/*`, `04-idea-validation/*`, `pre-seed-pack/03-CUSTOMER.md`, `pre-seed-pack/11-GOD-TIER-EDGE.md` | VERIFIED |
| F5 | `startup-universe/13-research-loop/` is empty (0 files). ROADMAP.md still shows layers 01-04 as `[ ]` and CHECKPOINT.md says "skeleton only", but the chapter files exist on disk. Both tracking files are stale. | `ls` count 0; `ROADMAP.md` L39-60; `CHECKPOINT.md` L5-9 | VERIFIED |
| F6 | The rubrics do not agree on one formula. There are at least 9 weighted scorecards with different factors and weights. They do agree on the ordering principle: money or costly behaviour beats talk. | section 2.3 | VERIFIED |

---

## 1. Where the framework lives

### 1.1 Core files (the selection logic itself)

| role | path | what it holds |
|---|---|---|
| CORE synthesis | `~/startup-idea-lab/research/methodology-masterdoc.md` | evidence hierarchy (L12-19), 10 ranked channels (L23-122), evidence ledger + kill-criteria-first rule (L139-140), five-interview rule (L142-143), buy-vs-build (L145-146), 8-line summary (L150-159) |
| CORE rubric | `~/startup-idea-lab/results/redo-redo-idea-founder-frameworks.content.md` (gen-3, the DEEP gen per CONTINUATION-MASTER L42) | evidence ladder L0-L5 (L108-119), method decision tree (L203), ranked channels (L328-343), 8-factor weighted scorecard (L345-360), 7-stage experiment ladder with kill conditions (L362-374), pipeline stages (L297-326) |
| CORE rubric | `~/startup-idea-lab/results/redo-redo-idea-complaint-mining.content.md` (gen-3, DEEP per CONTINUATION-MASTER L37) | 6-level evidence ladder (L68-79), workaround table (L81-92), 6-factor opportunity score (L342-355), 10-test validation + kill table (L357-370), 10-step automation pipeline (L372-383) |
| CORE rubric | `~/startup-idea-lab/results/idea-complaint-mining.content.md` (gen-1) | 19-field evidence record (L256-277), dedupe rule (L281-283), four-factor score with formula (L285-302), 8-level evidence ladder (L304-317), kill tests (L325-334) |
| CORE teaching | `~/startup-universe/01-problem-discovery/01-what-a-problem-is.md` | problem strength formula (L25), urgency spectrum (L27-39), buyer/user/beneficiary (L41-55), 5-dimension ranking table + thresholds (L78-92) |
| CORE teaching | `~/startup-universe/01-problem-discovery/03-validating-pain.md` | 5-rung evidence ladder (L15-52), vanity vs validation (L81-98), 3-of-5 build gate (L135-146), 7 red flags (L148-158) |
| CORE teaching | `~/startup-universe/04-idea-validation/01-hypothesis-framework.md`, `02-experiments.md`, `03-interpreting-results.md` | if/then/because hypotheses, riskiest assumption first, one-page experiment design, valid-result test, support/falsify/ambiguous, pivot types, kill rules |
| CORE gate | `~/startup-universe/pre-seed-pack/11-GOD-TIER-EDGE.md` | pre-mortem (L9-29), pre-registered kill criteria template (L31-45) |

### 1.2 Supporting files

| path | why it matters |
|---|---|
| `~/startup-idea-lab/results/idea-india-arbitrage.content.md` L395-415 | worked 5-factor ranking with a subtracted risk term (max 19) |
| `~/startup-idea-lab/results/redo-idea-india-arbitrage.content.md` L518-559 | 10-question decision tree, dated kill tests, 6-layer pipeline with 7 scored factors |
| `~/startup-idea-lab/results/idea-failed-startups.content.md` L211-226 | retry score /10 and its stated basis |
| `~/startup-idea-lab/results/idea-money-flow.content.md` L30, L224-231 | 30-point score (six 0-5 factors), weekly decision meeting, validation sprint |
| `~/startup-idea-lab/results/redo-redo-redo-redo-idea2-boring-saas.content.md` L97-106, L207-220, L324-336, L767-780 | hunting routine, AI-workflow scorecard, vertical selection matrix, validation + kill table |
| `~/startup-idea-lab/results/redo-redo-redo-redo-idea2-ai-workflows.content.md` L184-197, L207-216, L239-243, L347-360, L674-697 | boring-industry sheet, workflow test, kill rules, /25 matrix, 14-day checklist |
| `~/startup-idea-lab/results/redo-idea2-vertical-b2b.content.md` L53-63, L820-841, L1052-1061 | entry-quality score /100, vertical matrix, A-D evidence grades |
| `~/startup-idea-lab/results/redo-redo-idea2-api-tools.content.md` L158-166, L227-235, L634-643 | sheet with per-factor kill thresholds, workflow scorecard, dev-tool teardown checklist |
| `~/startup-idea-lab/standards/STANDARDS.md` + `standards/deep-contract.md` | the quality bar for RESEARCH REPORTS (not ideas); reusable for Hypnexis research lanes |
| `~/startup-idea-lab/prompts/idea-prompts.md`, `idea-prompts-wave2.md` | the prompts that asked for those scorecards ("End with ... scoring sheet", "scorecard", "selection matrix") |
| `~/startup-universe/03-customer/02-personas-and-segments.md` L54-64 | 4 beachhead criteria |
| `~/startup-universe/02-market/01-why-markets-beat-ideas.md` L21-35, `04-timing-and-waves.md` L45-96 | market over idea, "why now" = infrastructure cost drop |
| `~/startup-universe/pre-seed-pack/03-CUSTOMER.md` L9-21, L44-65 | 6-level evidence hierarchy, "level 4 or above" rule, ledger sorted by frequency x severity |

---

## 2. The framework itself (faithful summary)

### 2.1 The doctrine in five quotes

1. "Don't brainstorm ideas, mine evidence." (`methodology-masterdoc.md` L152, original has an em dash, replaced with a comma here)
2. "The strongest signal is a named buyer with a budget (RFP, grant, hiring, ad spend)." (`methodology-masterdoc.md` L153)
3. "Demand a second signal." (`methodology-masterdoc.md` L19, quoting the money-flow report)
4. "Kill criteria before launch: a candidate without a kill condition isn't a candidate." (`methodology-masterdoc.md` L159)
5. "A complaint is a lead; a workaround is stronger; a paid pilot or purchase order is stronger still." (`redo-redo-idea-complaint-mining.content.md` L15)

### 2.2 The pipeline (stages)

Three versions exist. They line up like this:

```
  idea-lab founder-frameworks g3, L303-312          idea-lab india g2, L550-557      universe 04-idea-validation
  ------------------------------------------        -------------------------        ---------------------------
  Collect    (APIs, feeds, reviews, tenders) daily  1 Ingest                         write 5-15 if/then/because hypotheses
  Normalize  (text, entities, dates)        daily   2 Normalize                      put them on a lean canvas
  Cluster    (problem labels)               weekly  3 Classify / 4 Extract           find the riskiest assumption
  Rank       (frequency, urgency, money)    weekly  5 Score (7 factors, each 0-5)    one-page experiment design (green/red/grey lines)
  Interview  (buyers and users)             weekly  6 Act: top 3 to interviews,      run cheapest experiment that can falsify it
  Concierge  (manual delivery)            biweekly    archive rest with reason code  read result: support / falsify / ambiguous
  Prototype  (narrow workflow)             monthly                                   pivot one thing, or kill on the pre-set number
  Kill/scale (thresholds)                  monthly
```

Masterdoc adds the operating cadence: a weekly radar (Mon procurement, Tue complaints, Wed funding, Thu regulation, Fri jobs, Sat trends, Sun "Synthesize + prune") at `methodology-masterdoc.md` L128-137, and the "five-interview rule": any anomaly gets five customer interviews before it becomes a candidate (L142-143).

### 2.3 Scoring rubrics found (all of them, with weights)

All scales are 0-5 or 1-5 per factor unless noted.

| # | rubric | factors and weights | scale / output | source |
|---|---|---|---|---|
| R1 | Four-factor complaint score | Frequency 30%, Urgency 30%, Payment evidence 25%, Workaround intensity 15% | `Opportunity Score = (30F + 30U + 25P + 15W) / 5` (0-5 inputs and weights summing to 100, so the range is 0-100) | `idea-complaint-mining.content.md` L285-302; repeated in `methodology-masterdoc.md` L62 |
| R2 | Validation scorecard | Pain consequence 20, Frequency 15, Existing workaround 15, Willingness to pay 20, Reachability 10, Buildability 10, Timing 5, Defensibility 5 (sum 100) | "Score each candidate from 0 to 5, then multiply by the stated weights" | `redo-redo-idea-founder-frameworks.content.md` L347-360 |
| R3 | Opportunity score | pain 0.25, frequency 0.20, payment evidence 0.20, reachability 0.15, timing 0.10, founder advantage 0.10 | written as `0.25 pain x 0.20 frequency x ...` but called a "weighted total" (read as a weighted sum; the literal "x" is a typo-level ambiguity in the source) | `redo-redo-idea-complaint-mining.content.md` L342-355 |
| R4 | India wedge score | urgency + distribution + willingness to pay + defensibility, MINUS execution risk | each 1-5, max 19; top ideas scored 14 | `idea-india-arbitrage.content.md` L397-415 |
| R5 | Pipeline score | unique users, urgency, workaround cost, willingness to pay, distribution access, timing, asset availability | each 0-5, unweighted | `redo-idea-india-arbitrage.content.md` L556 |
| R6 | 30-point score | Market Size, Purchase Proximity, Technical Feasibility, Team, Moat, Regulatory Fit | six 0-5 factors = 30; penalty flags for unit economics and no market need | `idea-money-flow.content.md` L30, L224-225 |
| R7 | Entry-quality score | Pain intensity 20, Recurring trigger 15, Buyer reachability 15, Wedge independence 15, Competition gap 15, Revenue quality 10, Implementation feasibility 10 | 1-5 per factor, weighted to /100 | `redo-idea2-vertical-b2b.content.md` L53-63, L820-841 |
| R8 | Vertical selection matrix | Founder access 25, Workflow frequency 20, Budget 20, Regulatory or error cost 15, Distribution fit 10, Expansion path 10 | weighted /5; "Founder access receives the highest weight because a technically correct product still fails if the team cannot reach the first users." | `redo-redo-redo-redo-idea2-boring-saas.content.md` L324-336 |
| R9 | Boring-industry sheet with kill thresholds | Pain frequency 20, Error cost 20, Buyer access 15, Data exhaust 15, Switching path 10, Recurring payment 10, Regulatory or trust risk 10 | 1-5; KILL if a factor is "Below 3" (regulatory: "Below 2") | `redo-redo-idea2-api-tools.content.md` L158-166 |
| R10 | Workflow opportunity scorecard | Frequency 20, Labor minutes 15, Error cost 20, Input structure 10, Human checkpoint 10, Integration access 15, Compliance fit 10 | plus "Evidence to collect in 14 days" per factor | `redo-redo-idea2-api-tools.content.md` L227-235 |
| R11 | Problem ranking table (teaching) | Frequency, Intensity, Willingness to pay, Market size, Existing solutions | each 1/3/5, max 25. "Problems scoring 20-25 are worth pursuing. Problems scoring below 15 need more investigation. Problems scoring below 10 are almost never startup material." | `startup-universe/01-problem-discovery/01-what-a-problem-is.md` L78-90 |
| R12 | Problem strength (teaching) | `Problem strength = Frequency x Intensity x Willingness to pay. If any one of these is near zero, the product has no market.` | multiplicative | same file L25 |
| R13 | Retry score (dead startups) | judgment emphasising "persistent pain, proof that a constraint changed, low test cost, manageable regulation, and evidence that assets or operations continued" | /10 | `idea-failed-startups.content.md` L213 |

Two honesty notes the sources attach to their own numbers:
- "The numbers are a founder scoring framework, not external market measurements." (`boring-saas` g5 L336)
- "These are derived scores for prioritization, not market facts." (`ai-workflows` g5 L360)

What the rubrics agree on. Membership is listed so the count can be checked; grouping of synonyms is my choice (strict: only factors named explicitly in the row above).

| factor group | rubrics that include it | count |
|---|---|---:|
| pain / urgency / intensity / error cost | R1 R2 R3 R4 R5 R7 R8 R9 R10 R11 R12 R13 | 12 |
| money / willingness to pay / budget / revenue | R1 R2 R3 R4 R5 R7 R8 R9 R11 R12 | 10 |
| frequency | R1 R2 R3 R8 R9 R10 R11 R12 | 8 |
| reachability / access / distribution | R2 R3 R4 R5 R7 R8 R9 | 7 |
| timing / trigger / constraint changed | R2 R3 R5 R7 R13 | 5 |
| defensibility / moat / competition gap | R2 R4 R6 R7 R11 | 5 |
| feasibility / buildability / execution risk | R2 R4 R6 R7 | 4 |

### 2.4 Evidence ladders (the evidence rules)

| ladder | rungs, weakest to strongest | source |
|---|---|---|
| idea-lab L0-L5 | L0 abstract complaint or trend (1) / L1 repeated complaint by distinct users (2) / L2 spreadsheet, script, VA or manual ritual (3) / L3 existing paid workaround (4) / L4 buyer shares data, makes intro, or signs pilot (5) / L5 recurring payment or PO (6) | `founder-frameworks` g3 L110-117 |
| idea-lab 1-8 | one complaint / independent complaints / interviews about last real occurrence / documented workaround / existing budget / LOI or pilot scheduled / deposit or paid pilot / repeated use, renewal, referral | `complaint-mining` g1 L306-315 |
| universe 5 rungs | Anecdote ("worth zero") / Observation / Interview (10+ unprompted) / Commitment / Payment ("the gold standard") | `03-validating-pain.md` L15-52 |
| pre-seed 6 levels | Opinions / Hypotheticals / History / Time / Money / Usage; "every claim about demand in the deck must sit at level 4 or above" | `pre-seed-pack/03-CUSTOMER.md` L9-21 |

Other evidence rules:
- Dedupe by person, not post: "Count a person once per problem" (`complaint-mining` g1 L283); "The important unit is not the post; it is the unique affected user" (`founder-frameworks` g3 L106).
- Triangulation: "One method is an anecdote. Two methods are a pattern. Three methods are a finding. Four methods are a conviction." (`02-research-methods.md` L160). India g2 calls the same idea "The Three-Source Test" (`redo-idea-india-arbitrage` L561).
- Second-source rule for trends: "A trend should reach a second evidence source before it enters a build queue." (`complaint-mining` g3 L173)
- Evidence grades A-D: A official dataset/regulation/procurement/primary pricing ... D individual operator post. "No market-size claim should rely solely on grade C or D evidence." (`vertical-b2b` g2 L1052-1061)
- Stranger rule: "if the signal came from someone who has no relationship with you and no reason to be polite, it is probably real." (`03-validating-pain.md` L98)
- Competition is evidence of a market: "The absence of competition is usually evidence of the absence of customers." (`01-what-a-problem-is.md` L92)

### 2.5 Kill gates

| gate set | content | source |
|---|---|---|
| Immediate kills | "Kill immediately if the problem is not urgent, no buyer accepts a paid pilot, data rights are unavailable, fulfillment cost exceeds likely price, the product requires a prohibited regulatory action, or acquisition diligence cannot verify revenue and ownership. Stop experiments when the predeclared loss cap or time cap is reached." | `founder-frameworks` g3 L374 |
| 7-stage experiment ladder | 10 interviews (5 same pain) / concierge (3 complete) / paid pilot (2 deposits) / repeat (same buyer twice) / narrow product / retention / channel (3 qualified leads), each with a kill condition | `founder-frameworks` g3 L362-372 |
| 10 tests | Problem interviews 15 conv, 8 recent examples, kill if fewer than 5 recall a recent event ... Compliance "Core workflow depends on prohibited access" | `complaint-mining` g3 L357-370 |
| dated kill tests | Day 3 (15 interviews), Day 5, Day 7 (data access, compliance), Day 10 (3 paid pilots), Day 17, Day 21 ... | `redo-idea-india-arbitrage` L531-544 |
| AI-workflow kills | no representative documents, output not reviewable, unclear budget owner, fewer than 20 instances per month, high-liability decision without human approval | `ai-workflows` g5 L243, L697 |
| build gate (teaching) | build when at least 3 of 5 are yes: 10 strangers in own words; 5 found existing solution inadequate; 1 committed something of value; buyer/user/current workaround named; 1% of affected people = viable business | `03-validating-pain.md` L135-146 |
| pre-registration template | "Hypothesis: we believe [persona] will [action] because [reason] / Evidence that confirms: [number, method, sample] / Evidence that kills: [number, method, sample] / Decision deadline: [date]" | `11-GOD-TIER-EDGE.md` L36-40 |
| valid result | sample matches hypothesis; big enough that doubling would not flip it; behaviour was real; interpretation pre-committed | `02-experiments.md` L96-103 |
| decision buckets | Support / Falsify / Ambiguous. "Ambiguity is not a soft 'maybe yes'." | `03-interpreting-results.md` L29-37 |

### 2.6 Method choice by situation

"If you personally experience the pain, start with Graham and a concierge test. If you have access to a buyer but not a clear product, use JTBD and the Mom Test. If the category exists but value is poorly allocated, use Blue Ocean. If the problem is technical or regulated, mine grants, procurement, filings, and institutional exhaust. If the product already exists and has customers, consider acquisition before building." (`founder-frameworks` g3 L203)

Buy-vs-build: "Buy when: proven MRR exists, price < your build cost, distribution is the gap (fixable). Build when: no product exists, constraint changed, you have a wedge incumbents can't copy fast." (`methodology-masterdoc.md` L145-146). This is the closest analogue in the repos to the Hypnexis fork-first strategy.

Beachhead criteria: Accessible, Underserved, Similar buyers, Adjacent growth (`03-customer/02-personas-and-segments.md` L54-62).

---

## 3. Scripts and prompts that automate it

### 3.1 What exists

| file | what it automates | how it is run | does it rank ideas? |
|---|---|---|---|
| `~/startup-idea-lab/scripts/launch-idea-runs.py` | builds prompts from the two prompt banks (takes the LAST `META` block, L53-55) and launches Parallel deep-research runs through `~/parallel-ai-stack/scripts/parallel-deep-research.py` | `python3 launch-idea-runs.py [--processor ultra8x] [--names a,b]` (L5) | no |
| `~/startup-idea-lab/scripts/report-supervisor.py` | scores a report: composite `100*(0.30G + 0.20C + 0.15A + 0.15D + 0.10S + 0.05U + 0.05H)` (L156), hard gates (L158-169), verdict DEEP only if score >= 85 AND cite_d >= 0.8/K AND n >= 30K AND (table_d >= 1.0 OR conceptual) (L187-188) | `python3 report-supervisor.py <file>` or `... audit [N]` (L24-26) | no, it scores report density |
| `~/startup-idea-lab/scripts/redo-wave.py` | relaunches every report below DEEP with `deep-contract.md` appended; best-gen-wins; never overwrites (`next_gen_name`) | dry run default; `--fire`, `--names`, `--processor` (L21-25) | no |
| `~/startup-idea-lab/scripts/calibrate.py` | tests the scorer itself: anchors, monotonicity, adversarial cases, self-consistency; exit 1 = "checker lying" | `python3 calibrate.py [--verbose]` (L32) | no |
| `~/startup-idea-lab/standards/deep-contract.md` | prompt suffix: >= 0.8 unique sources per 1K chars, >= 20 data tables, >= 30K chars, ends with Sources / Evidence ledger / next steps | appended to every launch | no |
| `~/startup-idea-lab/prompts/idea-prompts*.md` + `idea-prompts-wave*.py` | prompt banks; wave-2 frame says every idea must be software, buildable by a solo tech founder, recurring revenue, digital distribution (`idea-prompts-wave2.md` L5-13) | via launch-idea-runs.py or the generators | no (they ask the model to WRITE scorecards) |

Path caveat (VERIFIED): the idea-lab copies of `report-supervisor.py audit`, `calibrate.py` and `redo-wave.py` resolve paths to `../test-results` and `../run-ledger`, which do not exist inside `~/startup-idea-lab`. Their working copies live in `~/parallel-ai-stack/scripts/` (`CONTINUATION-PIPELINE.md` L10-16). Single-file scoring works anywhere: running `python3 -I ~/startup-idea-lab/scripts/report-supervisor.py ~/startup-idea-lab/results/redo-redo-idea-founder-frameworks.content.md` this session returned `depth 89.1, verdict DEEP, cites 254`, which matches CONTINUATION-MASTER L42 (89.1, 254).

Known limit, in the repo's own words: "The checker is a density proxy, NOT truth ... It CAN'T catch: claims contradicted by the same source ... plausible-sounding invented numbers" (`CONTINUATION-MASTER.md` L185).

### 3.2 What does not exist

- No idea/problem scoring script. STAGE B "30+ idea cards per channel, evidence-ledgered (NEW pipeline, not yet built)" (`MAPPING.md` L17).
- No automation in `startup-universe` (no scripts directory; `13-research-loop/` empty).
- The described automation pipelines (complaint-mining g3 L372-383, india g2 L548-559) are prose specs only.

---

## 4. ADAPTATION, NOT FROM THE REPOS: choosing ONE of the 15 Hypnexis statements

Everything in this section is my proposal, built on sections 1-3 and on `~/hypnexis-main/PROBLEM-STATEMENTS.md` + `~/hypnexis-main/FLEET-BRIEF.md` (strategy section 00). It is a hypothesis list, not a sourced landing. Nothing here names a specific repo or model from memory; finding those is the P2 research job. The user decides the pick.

### 4.1 Translation table: startup factor to hackathon factor

| repo factor (sources) | why it maps | hackathon factor | what to measure |
|---|---|---|---|
| Existing workaround / payment evidence / evidence ladder (R1, R2, R3) | in the repos, money already moving is the proof. Under a fork-first strategy, open work already existing is the proof the core is doable | **F1 Fork base strength** | best rung reached on the fork ladder (4.2) |
| "Demand a second signal", Three-Source Test | one repo alone is a single point of failure | **F2 Independent bases** | count of independent usable bases (repo, model weights, dataset, hosted demo) |
| Buildability / implementation feasibility (R2, R7) | judges will not install anything (FLEET-BRIEF 00.2) | **F3 Website-runnable core** | can the core run in-browser or behind a hosted backend within our compute |
| Pain consequence / urgency (R1-R4, R11) | judges respond to stakes they can feel | **F4 Visible stakes** | the PS text names a harm a viewer understands in one sentence |
| Founder advantage / founder access (R3, R8) | R8 gives it the top weight | **F5 Our edge** | santioni kit (`~/site-clones/santioni`, FLEET-BRIEF 00.3), past work, team skills (UNKNOWN until user answers FLEET-BRIEF section 6) |
| Timing / trigger, kill on time cap (R2, R3) | the round has a hard clock (UNKNOWN length) | **F6 Human-time gates** | hours of mandatory manual work the PS demands (labelling, expert test sets, MATLAB, hardware) |
| Defensibility / competition gap (R2, R7) | other teams will fork the same obvious repos | **F7 Customisation delta** | what we add that a straight fork does not have |
| (new, from user strategy 00.3) | look and feel is a stated goal | **F8 Visual story** | how much of the result is a picture, a graph, a map, a path, a scorecard |
| Rubric fit (CL-04 only states one) | rubric for this round is UNKNOWN (FLEET-BRIEF section 6) | **F9 Rubric fit** | re-weight once the rubric is known |

### 4.2 The fork ladder (adapted from the idea-lab L0-L5 ladder, `founder-frameworks` g3 L110-117)

| rung | what exists for this statement | score |
|---|---|---|
| K0 | only the PS text, nothing found | 0 |
| K1 | a paper or blog describing a method, no code | 1 |
| K2 | code exists but unmaintained, no weights, unclear licence | 2 |
| K3 | maintained repo, permissive licence, runs locally (we ran it) | 3 |
| K4 | K3 plus pretrained weights and a public dataset we can download | 4 |
| K5 | K4 plus an existing hosted demo (web UI) for the same task that we ran | 5 |

Rule carried over from the repos: a rung counts only when WE did the thing (ran it, downloaded it), the same way the repos count only behaviour, never stated intent (`03-validating-pain.md` L54-62). A README claim is K1-level evidence until run.

### 4.3 Proposed scorecard (weights are a proposal; change them once the rubric is known)

| factor | weight | 0 means | 5 means |
|---|---:|---|---|
| F1 Fork base strength | 25 | K0 | K5 |
| F2 Independent bases | 10 | one base | 3+ independent bases agree |
| F3 Website-runnable core | 20 | needs local install, hardware or long GPU training | runs in-browser or on a hosted backend we can afford |
| F4 Visible stakes | 10 | abstract | one-sentence harm a judge feels |
| F5 Our edge | 5 | none | existing asset fits directly |
| F6 Human-time gates (inverted) | 10 | mandatory multi-day human work with no shortcut | none |
| F7 Customisation delta | 5 | straight fork | clear added layer |
| F8 Visual story | 15 | text output only | the answer itself is a visual (graph, map, path, scorecard) |

`Score = sum(weight x factor) / 5`, range 0-100. This mirrors R2's form (0-5 per factor, weights sum to 100). F1 + F3 = 45 because FLEET-BRIEF 00.6 says fork availability and live-website fit are the two filters that follow from the strategy. F8 = 15 because the look-and-feel goal is explicit.

### 4.4 Kill gates (adapted from `founder-frameworks` g3 L374 and the R9 per-factor thresholds)

Kill a statement immediately if any of these hold after the research loop:
1. F1 below 3 after the P2 search (no runnable, licensed base). Source analogue: R9 "Below 3" kill.
2. F3 = 0: the core cannot be shown from a browser. Source analogue: "the product requires a prohibited ... action".
3. The PS forbids the website-only form. HW-01 says "Software-only solutions are not eligible" (PROBLEM-STATEMENTS L377). CL-04 requires "a machine learning algorithm in MATLAB" (L240). Both conflict with FLEET-BRIEF 00.2 unless the user changes the strategy.
4. A mandatory human gate with no shortcut found and no time for it (F6 = 0). Source analogue: "Stop experiments when the predeclared loss cap or time cap is reached."
5. Data rights unavailable for the named dataset. Source analogue: "data rights are unavailable".

### 4.5 Pre-scan of the 15 statements against the gates (from PS text only; no research done yet)

Facts in this table come only from `PROBLEM-STATEMENTS.md` and FLEET-BRIEF/CONTINUATION. Compute: hermes measured GTX 1650 4 GB VRAM, 7 GB RAM (`CONTINUATION.md` L16, UNVERIFIED by me).

| id | named bases in the PS (F1/F2 starting points) | stated human or tool gates (F6, kill 3-4) | visual hook in the PS (F8) | early flag |
|---|---|---|---|---|
| AI-01 | ASVspoof 2019, In-the-Wild; "Pretrained self-supervised speech models are allowed" (L30) | none stated | audio clip in, verdict out | open |
| AI-02 | BIRD benchmark (L53) | "only open-weight models with 8 billion parameters or fewer" (L53); 4 GB VRAM local risk | SQL trace, row checks | compute check needed |
| AI-03 | Neo4j, ChromaDB, Streamlit/React, pyvis, react-force-graph (L74-76) | none stated | split screen with clickable graph is a stated deliverable (L76) | open, strong F8 |
| AI-04 | none named | none stated | "colour-coded scorecards" on one screen (L99) | open, F8 |
| W3-01 | Circom, Noir; "Open-source circuit libraries may be used" (L128) | browser proof speed is a stated challenge (L135) | proof flow | open |
| W3-02 | ERC-4337; "any open model or a scripted bot" (L150) | none stated | policy and approval flow | open |
| CL-01 | Sentinel-2, public 30 m forest-loss maps as labels (L173-180) | must test on a state not in training (L180); training compute | map | compute check needed |
| CL-02 | published spending records, emission factors | "hand-label at least 2,000 spending lines, with two people agreeing on every label" (L202) | footprint with uncertainty | human gate |
| CL-03 | MathWorks repo, Building Data Genome Project 2, ASHRAE Great Energy Predictor III (L224) | must test on unseen buildings (L222) | retrofit ranking | open |
| CL-04 | MathWorks repo and starter Live Script (L245) | MATLAB required (L240); 5-min presentation; rubric 70/30 stated (L247) | presentation | kill-gate 3 conflict |
| HM-01 | frozen PubChem and ChEMBL snapshots (L276) | own test set of broken inputs (L276) | validation report per molecule | open |
| HM-02 | none named | test set built "with help from a pharmacist or pharmacy student" (L299) | flagged prescription | human gate |
| SC-01 | none named | multiple non-overlapping cameras, no plate reading (L321-326) | flow map between cameras | data check needed |
| SC-02 | Project Sidewalk (L350) | "teams must label their own local images" (L350) | route map avoiding barriers | human gate |
| HW-01 | none | "Software-only solutions are not eligible" (L377) | physical prototype | kill-gate 3 conflict |

This pre-scan agrees with FLEET-BRIEF 00.6 and with hermes's ack in `CONTINUATION.md` L16 ("HW-01 not pickable", "CL-02 riskiest"). It is not a ranking: F1, F2, F3 and F7 need P2 research before any number is assigned.

### 4.6 Decision tree with confidence (0-20 per node)

```
[N1] Run the P2 discovery loop per shortlisted statement                          conf 17/20
     (repos on every code host, HF models + Spaces, Kaggle, papers with code,      reason: mirrors the repos' Collect step;
      competition winners; per FLEET-BRIEF 00.4)                                   scope set by user
  |
  +--[N2] Place each statement on the fork ladder K0-K5 (we run it, not read it)  conf 15/20
  |        reason: direct port of L0-L5; risk is time cost of actually running repos
  |
  +--[N3] Apply kill gates 4.4                                                     conf 16/20
  |        reason: gates 2-3 are read straight from PS text; gate 1 depends on N2 quality
  |
  +--[N4] Score survivors with 4.3                                                 conf 11/20
  |        reason: weights are my proposal; round rubric UNKNOWN; re-weight when known
  |
  +--[N5] Pre-register per top-3: "we believe <fork stack> can show <result>      conf 16/20
  |        in a browser demo; confirms if <number, method>; kills if <number,       reason: template copied from
  |        method>; deadline <time>"                                                11-GOD-TIER-EDGE L36-40
  |
  +--[N6] Smoke test = concierge analogue: run the forked core end to end on      conf 14/20
  |        5 real inputs from the PS's own datasets; support / falsify / ambiguous  reason: 02-experiments L96-103 valid-result rules
  |
  +--[N7] User picks ONE (FLEET-BRIEF phase P3)                                    conf 20/20 (user decides)
```

### 4.7 Evidence rules for the Hypnexis research lanes (adapted)

1. Every fork candidate row: URL, fetched date, licence, last commit date, stars, weights yes/no, dataset yes/no, ran-it yes/no, VERIFIED or UNVERIFIED (FLEET-BRIEF rule 2 plus the repo's 19-field record idea, `complaint-mining` g1 L256-277).
2. Two independent bases before a statement scores F1 >= 4 (second-signal rule).
3. Grade evidence A-D as in `vertical-b2b` g2 L1052-1061: A = we ran it, B = official docs/benchmark leaderboard, C = blog or review, D = forum post. No F1 score on C/D alone.
4. Lane reports can reuse `deep-contract.md`'s closing structure (Sources, Evidence ledger, next steps) and be density-checked with `python3 -I ~/startup-idea-lab/scripts/report-supervisor.py <report.md>`, keeping in mind it measures density, not truth (`CONTINUATION-MASTER.md` L185).
5. Never-delete: superseded scores get archived as v1, v2 (both repos and the user's rules).

---

## 5. Coverage audit

Bytes from `wc -c`; "read" bytes computed with `sed -n <range>p | wc -c` for partial reads. Files read in full = 100%.

### 5.1 startup-idea-lab

| file | size (B) | read (B) | how |
|---|---:|---:|---|
| README.md | 4,264 | 4,264 | full |
| MAPPING.md | 4,531 | 4,531 | full |
| CONTINUATION-MASTER.md | 25,905 | 25,905 | full |
| CONTINUATION-PIPELINE.md | 16,918 | 16,918 | full |
| CONTINUATION-DECISIONS.md | 19,519 | 19,519 | full |
| research/methodology-masterdoc.md | 11,061 | 11,061 | full |
| research/synthesis-draft.md | 2,568 | 2,568 | full |
| standards/STANDARDS.md | 5,984 | 5,984 | full |
| scripts/STANDARDS.md | 5,984 | 5,984 | identical to standards/STANDARDS.md (`cmp`) |
| standards/deep-contract.md | 2,982 | 2,982 | full |
| prompts/idea-prompts.md | 16,678 | 16,678 | full |
| prompts/idea-prompts-wave2.md | 24,093 | 24,093 | full |
| scripts/launch-idea-runs.py | 3,558 | 3,558 | full |
| scripts/report-supervisor.py | 12,327 | 12,327 | full, plus one test run |
| scripts/redo-wave.py | 8,505 | 8,505 | full |
| scripts/calibrate.py | 7,185 | 7,185 | full |
| results/redo-redo-idea-founder-frameworks.content.md | 45,490 | 45,490 | full |
| results/redo-redo-idea-complaint-mining.content.md | 63,871 | 63,871 | full |
| results/idea-complaint-mining.content.md | 68,734 | 4,434 | L255-334 (scoring section) |
| results/idea-india-arbitrage.content.md | 88,115 | 1,660 | L390-419 |
| results/redo-idea-india-arbitrage.content.md | 82,621 | 5,892 | L510-569 |
| results/idea-money-flow.content.md | 65,985 | 5,847 | L25-34 + L215-234 |
| results/idea-failed-startups.content.md | 70,725 | 4,534 | L205-229 |
| results/idea-taxonomy.content.md | 88,492 | 1,348 | L155-170 |
| results/redo-redo-redo-redo-idea2-boring-saas.content.md | 126,322 | 6,231 | 4 scorecard ranges |
| results/redo-redo-redo-redo-idea2-ai-workflows.content.md | 117,779 | 11,367 | 3 scorecard ranges |
| results/redo-idea2-vertical-b2b.content.md | 91,572 | 5,352 | 3 scorecard ranges |
| results/redo-redo-idea2-api-tools.content.md | 126,980 | 12,115 | 2 scorecard ranges |
| CONTINUATION-INDEX.md, RESUME-PROMPT.md, WAVE-TRACKER.md, SWEEP-LOG.md, research/calibration-log.md | 17,685 / 7,089 / 17,325 / 4,917 / 5,727 | grep only | keyword grep (stage b, scorecard, rubric, kill) |
| the other ~540 md files (results of waves 3-34 territory maps, other generations, prompts w3-w34, research/*.content.md, PG/YC/journal notes) | not summed | 0 | NOT READ: these are territory maps (WHERE signal lives), not selection rubrics, per `CONTINUATION-MASTER.md` L10 and D9 |

idea-lab totals (computed with `wc -c`): 18 files read in full = 281,423 B; 10 reports read in part = 58,780 B of 927,325 B (6.3%).

### 5.2 startup-universe

| file | size (B) | read (B) | how |
|---|---:|---:|---|
| README.md | 4,112 | 4,112 | full |
| ROADMAP.md | 12,404 | 12,404 | full |
| CHECKPOINT.md | 5,140 | 5,140 | full |
| 01-problem-discovery/01-what-a-problem-is.md | 19,766 | 19,766 | full |
| 01-problem-discovery/02-research-methods.md | 19,084 | 19,084 | full |
| 01-problem-discovery/03-validating-pain.md | 18,693 | 18,693 | full |
| 04-idea-validation/01-hypothesis-framework.md | 20,163 | 20,163 | full |
| 04-idea-validation/02-experiments.md | 19,882 | 19,882 | full |
| 04-idea-validation/03-interpreting-results.md | 22,517 | 22,517 | full |
| pre-seed-pack/03-CUSTOMER.md | 7,400 | 7,400 | full |
| pre-seed-pack/11-GOD-TIER-EDGE.md | 12,349 | 12,349 | full |
| 02-market/01-why-markets-beat-ideas.md | 16,380 | 5,722 | L1-60 |
| 02-market/04-timing-and-waves.md | 16,732 | 5,590 | L40-99 |
| 02-market/02-market-sizing.md | 13,015 | 1,668 | L60-84 |
| 03-customer/02-personas-and-segments.md | 7,392 | 2,294 | L40-84 |
| 02-market/03-market-structure.md, 03-customer/01-customer-discovery.md, 03-customer/03-jobs-to-be-done.md, pre-seed-pack/00-README.md, pre-seed-pack/02-MARKET.md | 14,687 / 7,530 / 7,830 / 8,120 / 37,406 | grep only | keyword grep (score, rank, criteria, kill, beachhead) |
| 13-research-loop/ | 0 files | n/a | empty |

universe totals (computed): 11 files read in full = 161,510 B; 4 chapters read in part = 15,274 B of 53,519 B (28.5%).
| TEMPLATE.md, 00-founder/* (6 files), other pre-seed-pack files (01, 04-10, templates/) | not summed | 0 | NOT READ: founder psychology, legal, finance, team; not selection logic |

### 5.3 hypnexis-main

| file | size (B) | read (B) | how |
|---|---:|---:|---|
| PROBLEM-STATEMENTS.md | 17,002 | 17,002 | full |
| FLEET-BRIEF.md | 7,383 | 7,383 | full (v2) |
| README.md | 654 | 654 | full |
| CONTINUATION.md | 1,462 | 1,462 | full |

### 5.4 Red-team of this file (claims graded)

| claim | grade | why |
|---|---|---|
| No script in either repo ranks ideas | VERIFIED | read all 4 scripts in full; universe has no scripts dir |
| STAGE B never built | VERIFIED | 5 files say so; no later file contradicts (greps) |
| The 13 rubrics in 2.3 are all the rubrics | UNVERIFIED | ~540 md files not read; other reports may hold more scorecards. The 20 idea topics' best gens were grepped only for 10 topics |
| R3 is a weighted sum | UNVERIFIED (interpretation) | source writes "x" between terms; I read it as a sum because it says "weighted total" |
| Factor-group counts in 2.3 | VERIFIED against the listed membership; the synonym grouping is my choice, so a different grouping gives different counts | |
| Section 4 weights and ladder | adaptation, not evidence | proposal only |
| GTX 1650 4 GB compute | UNVERIFIED | taken from CONTINUATION.md L16 (hermes) |
