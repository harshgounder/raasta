# COPYPASTE-METHOD.md: the methodology in ~/Desktop/copypaste.txt, applied to Hypnexis

Source: `~/Desktop/copypaste.txt` (93,898 B, 642 lines, read in full by claude 2026-10-24 ~14:45). It is one long chat: an F1 pit-stop "total intelligence" research plan (L10-63), then the 8-step ML pipeline explanation (L86-121), then a full Kaggle pipeline master design merged with an OpenClaw-style multi-agent architecture (L141-641).
Not used: `~/Desktop/copypaste-ideas.txt` (95,499 B) is a different chat (vision-native LLM ideas); the user named only copypaste.txt.

## Part 1. The method, as written in the file

| # | move | what the file says | where |
|---|---|---|---|
| M1 | Treat the target as a convergence point | "a pit stop is not an event. It is a convergence point" of physics, chemistry, psychology, computation, regulation, weather, economics. Every phase is "a different lens trained on the same object" | L12 |
| M2 | Many lenses, each a phase | 16 phases: regulation, topology, tire chemistry, aero, setup, mechanics, human performance, data/telemetry, weather, game theory, materials, history/case studies, surface science, comms, economics, knowledge-graph synthesis | L14-60 |
| M3 | Meta source plan | official docs, archives, community data, papers, books, GitHub/Medium communities, libraries (FastF1) | L62-63 |
| M4 | Domain analysis before any data | "Step 1, Domain Analysis... what does reality actually look like?" then data audit, EDA, features... | L94-121 |
| M5 | Set D minus Set A | D = every factor from the domain map, A = what the data has, M = D - A. Each missing factor is Class I (proxy with noise), Class II (absorbed by other variables), Class III (unavailable, irreducible uncertainty) | L206-231 |
| M6 | Orchestrator never executes | pipeline_state.json, results_blackboard/, append-only audit.jsonl, heartbeat monitor; "the pipeline controller never trains models itself" | L155-175 |
| M7 | Blocking quality gates | "No phase begins until the previous phase's quality gate passes" | L153, gates at L243, L350, L459, L556, L596 |
| M8 | Parallel zoo of diverse families | statistical, GBDT, NN, distance, zero-shot families fan out in parallel; value of weaker families is diversity | L387-457 |
| M9 | A rule-based floor | "Hardcode the domain thresholds... If your ML models don't beat this, your ML is failing" | L403 |
| M10 | Tiered combination, keep only what helps | each ensemble tier must improve the previous one by 0.001 or it is removed: "Adding complexity that doesn't improve performance is always wrong" | L547-554 |
| M11 | Honest uncertainty layer | conformal prediction: prediction sets with guaranteed coverage; the model says when it is unsure | L567-595 |
| M12 | Submission ladder | floor first, then best single, then each ensemble tier, compare at each step | L608-617 |

## Part 2. ADAPTATION to Hypnexis (claude, not from the file)

| move | Hypnexis use |
|---|---|
| M1 + M2 lenses | For each in-scope statement, map the problem through every lens: the victim / user, the attacker or failure, Indian law and regulators, the tech (models, datasets), money (who loses how much), history (real incidents, news), the people who would use it, the judge's "what if". The project that wins is the one that sits at the convergence point a common person feels |
| M3 sources | WAVE-1-BRIEF source classes (all code hosts, forums, regions) |
| M5 D - A | D = everything the ideal product for the statement needs (from the lens map + the statement's key challenges). A = what the best forks already give. M = D - A, classed: I = we bolt on another fork, II = covered indirectly, III = cannot do in 15 h, say so honestly on the site |
| M6 + M7 | claude orchestrates, workers fill `research/<agent>/`; every phase closes with a written gate: wave 1 gate = every source class covered or logged as zero; pick gate = scored with reasons; build gate = live URL works end to end |
| M8 zoo | candidate projects per statement from many families (big repos, small niche repos, papers' code, competition winners, Chinese/Japanese/Korean hosts, HF Spaces); diversity is the point |
| M9 floor | for the chosen statement, ship a simple working baseline on the live URL FIRST, then upgrade |
| M10 combine | merging forks = ensembling: each merged part must visibly add something to the demo or it is cut |
| M11 uncertainty | a showpiece for non-expert judges: the product says "I am 92% sure, and here is why" or "I do not know" (e.g. AI-02 must admit when it cannot answer; AI-01 confidence on a clip; HM-02 alert severity). Honesty that is visible looks smart |
| M12 ladder | build ladder: L0 baseline live, L1 best single fork wired to the santioni site, L2 merged features, L3 polish, deck, video |
