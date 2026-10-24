# PARALLEL-DIGEST: 8 Parallel ultra deep-research runs, Hypnexis 2026

Built 2026-10-24 ~15:00 IST by Claude Code (subagent) from the 8 verbatim files in this folder.
All 8 runs were `completed` at the first status check (14:51 IST). None timed out.

| Label | Run id | Verbatim file | Lines / bytes | Read in full |
|---|---|---|---|---|
| AI-01 | trun_3b693d434bb94e6db97e777cfbe9e92c | parallel-AI-01.md | 351 / 58,469 | yes (1 page) |
| AI-02 | trun_3b693d434bb94e6d84c17b91b1cf5539 | parallel-AI-02.md | 509 / 69,505 | yes (2 pages) |
| AI-03 | trun_3b693d434bb94e6dad9164f0529a3e55 | parallel-AI-03.md | 475 / 70,820 | yes (2 pages) |
| AI-04 | trun_3b693d434bb94e6dabd881b185649dc4 | parallel-AI-04.md | 502 / 62,091 | yes (1 page) |
| HM-01 | trun_3b693d434bb94e6db9c60a2a1e987fd3 | parallel-HM-01.md | 582 / 68,898 | yes (2 pages) |
| HM-02 | trun_3b693d434bb94e6da71f0ac39267f122 | parallel-HM-02.md | 375 / 62,520 | yes (1 page) |
| W3 (W3-01 + W3-02) | trun_3b693d434bb94e6d8d02d86e3a27f54c | parallel-W3.md | 415 / 60,916 | yes (1 page) |
| CROSS | trun_3b693d434bb94e6db91d2d643e22de36 | parallel-CROSS.md | 473 / 55,848 | yes (1 page) |

How the verbatim files were made: the MCP tool spilled each result to a tool-results file (JSON or plain text); a python script pulled the text out unchanged and prepended a 3-line header (run id, processor ultra, fetched time). Char counts match what the tool reported (small 3-4 char gaps on two files are the trailing newline / byte-vs-char count). A first fetch of AI-03 and W3 returned only the header line; a refetch returned the full report.

## Rules for reading this digest

- **Every repo, licence, date, star count and "runs from website" value below is UNVERIFIED: not opened by us.** It is what the Parallel report says, copied as stated. Star counts are the report's snapshot, not live.
- "NR" = the report itself says not resolved / not established.
- "Web run" = the report's own column for browser / hosted demo / website runtime. "Hosted demo listed" means a link exists, uptime not tested by the report or by us.
- Wow ideas and what-ifs are the report's proposals, not tested builds.

---

## AI-01: voice-clone scam detector (2-10 s clips, unseen cloners)

### (a) Top 10 fork candidates (report's own rank M1-M10)

| # | Name | URL | Licence | Last update | Stars / popularity | Web run |
|---|---|---|---|---|---|---|
| 1 | Spectra-AASIST | https://huggingface.co/lab260/Spectra-AASIST | CONFLICT: header Apache-2.0, body MIT | NR | 5 HF likes, 120 monthly downloads | Arena interface linked, uptime NR; browser-local NR |
| 2 | XLSR-MamBo | https://github.com/saki-ciallo/XLSR-MamBo | MIT | 2026 paper; commit NR | 0 stars | hosted demo NR; CUDA install risk |
| 3 | SSL_Anti-spoofing | https://github.com/TakHemlata/SSL_Anti-spoofing | MIT | NR (created 2022) | NR | NR |
| 4 | AASIST-L | https://github.com/clovaai/aasist | MIT | NR | NR | third-party integrations only; best compact porting candidate |
| 5 | AASIST (original) | https://github.com/clovaai/aasist + https://huggingface.co/SpeechAntiSpoofingBenchmarks/AASIST | MIT | NR | wrapper: 1 HF like, 74 monthly downloads | Arena wrapper exists, uptime NR |
| 6 | Temporal-coherence / MS-CLAP | https://github.com/stbiadmin/audiodeepfake_public | MIT | 2026 paper; commit NR | 0 stars, 0 forks | example clips, no live service; CPU ~1 file/s (author claim) |
| 7 | Nes2Net | https://github.com/Liu-Tianchi/Nes2Net | Apache-2.0 | notices Apr 2025, Mar 2026 | NR | CPU option documented; hosted NR |
| 8 | Gustking XLSR classifier | https://huggingface.co/Gustking/wav2vec2-large-xlsr-deepfake-audio-classification | Apache-2.0 | NR | 6 likes, 21,035 monthly downloads | linked HF Space, uptime NR |
| 9 | garystafford wav2vec2 detector | https://huggingface.co/garystafford/wav2vec2-deepfake-voice-detector | Apache-2.0 | NR | 6 likes, 11,513 monthly downloads | linked "Aawaaz" Space, uptime NR |
| 10 | Hemgg Deepfake-audio-detection | https://huggingface.co/Hemgg/Deepfake-audio-detection | Apache-2.0 | NR | 4 likes, 12,936 monthly downloads | linked Space, uptime NR |

Key numbers the report gives: Spectra-AASIST 1.46% EER In-the-Wild vs original AASIST 43.01% on the same set via the Arena wrapper (different recipes, not head-to-head). AASIST-L is 85,306 params, 0.99% EER on ASVspoof 2019 LA. Report's final stack: M3 baseline, M1/M2 upgrade, M4 compact control, M6 only if it helps. Avoid M13 (lab260/AASIST3): CC BY-NC(-ND) and marked outdated.

### (b) Best wow for a common person

Play an executive / family-member payment call; let the judge guess real or fake first, then the detector shows a risk signal with an "inconclusive" state and ends with a safe-callback step before money moves. (CROSS version: "Maa, It's Not Me", a panicked call in a family voice that interrupts a simulated payment.)

### (c) What-if questions (10)

1. Scammer uses a cloning tool you never trained on? 2. Only two seconds of audio? 3. Caller speaks Hindi or a regional language? 4. Comes through WhatsApp or a bad phone line? 5. Fake played through a loudspeaker? 6. Make it quieter or trim the silence? 7. A real person sounds robotic or uses assistive TTS? 8. Only one sentence is fake? 9. Your two models disagree? 10. I do not want my voice stored or sent away?

### (d) Indian-context numbers (as cited)

| Number | Source cited by report |
|---|---|
| Delhi Police case, 17 Jun 2026: cloned MD voice, fraud over INR 10 crore, 63 accounts, 5 arrests | India Today, 2026-06-17 (indiatoday.in ... 2928485-2026-06-17) |
| McAfee India, 2 May 2023: 47% experienced an AI voice scam or knew someone who had | digitalterminal.in McAfee release [11] |
| Same: 83% of Indian victims reported financial loss; 48% of those who lost money lost over INR 50,000 | digitalterminal.in [11], repeated by News18 [13] (not independent) |
| Same: 69% could not tell an AI voice from a real one | digitalterminal.in [11] |
| Survey base: 7,054 respondents across seven countries | digitalterminal.in [11] |
| IndicSynth: 4,000 h, 989 speakers, 12 low-resource Indian languages | ACL Anthology 2025.acl-long.1070 |
| Bodhan indic-speak TTS: 23 languages (test generator, not detector) | HF bodhan-ai collection; skilloutlook.com |

---

## AI-02: small-model (<=8B) analyst over messy databases

### (a) Top 10 fork candidates (picked from the report's recommended stack; report gives no single rank)

| # | Name | URL | Licence | Last update | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | XiYanSQL-QwenCoder-3B-2504 (report's first pick) | https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-3B-2504 | Apache-2.0 weights | family code pushed 2026-10-13 | 160 (family code repo) | no small-model demo; ModelScope demo is 32B |
| 2 | OmniSQL-7B | https://huggingface.co/seeklhy/OmniSQL-7B | Apache-2.0 | model 2025-03-06; code 2025-09-08 | 456 | no hosted demo |
| 3 | Arctic-Text2SQL-R1-7B | https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B | Apache-2.0 | NR | NR | community Spaces advertised, uptime NR |
| 4 | Text2SqlAgent framework | https://github.com/Text2SqlAgent/text2sql-framework | MIT | NR | NR | local dummy-DB example; Ollama/vLLM endpoints |
| 5 | TrustSQL | https://github.com/glee4810/TrustSQL | CC-BY-4.0 | NR | NR | NR |
| 6 | MAC-SQL | https://github.com/wbbeyourself/MAC-SQL | NR | NR | NR | NR |
| 7 | Vanna | https://github.com/vanna-ai/vanna | MIT | 2026-02-02 push, ARCHIVED | 23,816 | local UI; hosted NR |
| 8 | SQLCoder-7B-2 | https://huggingface.co/defog/sqlcoder-7b-2 | CC-BY-SA-4.0 weights | NR | NR | advertised https://defog.ai/sqlcoder-demo/ |
| 9 | WrenAI | https://github.com/Canner/WrenAI | AGPL-3.0 core, some parts Apache-2.0 | NR | NR | self-host; public demo NR |
| 10 | PremSQL (+ Prem-1B-SQL) | https://github.com/premAI-io/premsql | MIT library; model licence NR | NR | NR | local playground |

Report numbers: XiYan-3B 55.08% BIRD dev with M-Schema vs 52.09% with DDL; XiYan-7B 62.13% vs 57.43%; OmniSQL-7B 63.9%; Arctic-7B 68.9% dev. 4-bit 7B weights alone ~3.5 GB, so 3B is the practical 4 GB GPU start. CHASE-SQL 73% uses Gemini, not eligible. Vanna quickstart uses Claude Sonnet 4.5 (per CROSS), which breaks the <=8B rule.

### (b) Best wow for a common person

Ask "What was revenue last month?" over a synthetic sales DB with duplicate orders, an `N/A` amount, an ambiguous `03/04/2025` date and a fan-out join. The first correct move is a clarifying question; then it shows rows, cleaning rules, before/after counts and the SQL. Tagline from the report: "it shows why this answer is supported, and stops when it is not." (CROSS version: "Where did the canteen's money go?")

### (c) What-if questions (10)

1. The data is wrong? 2. The same order appears twice? 3. Dates mean different things? 4. "Revenue" means something different to me? 5. It lies confidently? 6. It returns zero because the query is broken? 7. It joins the wrong tables? 8. It leaks data, deletes rows or follows instructions inside a cell? 9. The answer is not in the database? 10. No internet or only a small laptop?

### (d) Indian-context numbers

None in the report. (Loss cases cited are TransAlta $33.3M spreadsheet error, JPMorgan London Whale, Citibank/Revlon ~$500M; none Indian.)

---

## AI-03: GraphRAG with themes, graph + vector store, synced split-screen UI

### (a) Top 10 fork candidates

| # | Name | URL | Licence | Last push | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | LightRAG (report's first pick) | https://github.com/HKUDS/LightRAG | MIT | 2026-10-15 | 40,235 | REST server + WebUI; public live service NR |
| 2 | Neo4j LLM Graph Builder | https://github.com/neo4j-labs/llm-graph-builder | Apache-2.0 | 2026-10-17 | 5,283 | hosted: https://llm-graph-builder.neo4jlabs.com/ |
| 3 | Microsoft GraphRAG | https://github.com/microsoft/graphrag | MIT | 2026-10-20 | 36,398 | backend only |
| 4 | nano-graphrag | https://github.com/gusye1234/nano-graphrag | MIT | 2026-01-27 | 3,990 | backend only |
| 5 | Kotaemon | https://github.com/Cinnamon/kotaemon | Apache-2.0 | 2026-07-14 | 25,829 | HF Space: https://huggingface.co/spaces/cin-model/kotaemon |
| 6 | RAGFlow | https://github.com/infiniflow/ragflow | Apache-2.0 | 2026-10-23 | 92,773 | https://cloud.ragflow.io/ ; recommends 4 CPU / 16 GB / 50 GB |
| 7 | Tencent WeKnora | https://github.com/Tencent/WeKnora | unresolved, read LICENSE | 2026-10-22 | 35,064 | https://weknora.weixin.qq.com/ |
| 8 | GraphRAG Visualizer | https://github.com/noworneverev/graphrag-visualizer | MIT | 2026-02-25 | 429 | static: https://noworneverev.github.io/graphrag-visualizer/ |
| 9 | FalkorDB GraphRAG SDK | https://github.com/FalkorDB/GraphRAG-SDK | Apache-2.0 | 2026-10-12 | 1,014 | SDK; build own viewer |
| 10 | react-force-graph (UI layer) | https://github.com/vasturiano/react-force-graph | MIT | 2026-09-29 | 3,319 | browser component |

Report notes: no candidate meets all five deliverables unchanged. Zilliz vector-graph-rag has no graph DB (fails a literal "graph DB + vector DB" rubric). Four of five inspected GraphRAG HF Spaces were in runtime or build error. Microsoft says graph extraction is ~75% of its indexing cost.

### (b) Best wow for a common person

Ask "What are the main themes?" (graph lights up labelled communities, chat says thematic retrieval), then a precise factual question (switches to local retrieval, dims the rest, lights the exact path), then click an edge to open the source page passage. CROSS version: "One Scam. Three Stories." three unrelated complaints snap together on one shared payment handle, each edge opens its quote, editing the identifier makes the edge retract.

### (c) What-if questions (10)

1. I upload my own PDF instead of yours? 2. I ask what all the documents are about? 3. I ask one precise factual question? 4. The answer is wrong? 5. Two documents disagree? 6. One person or company has several names? 7. The information is not in any document? 8. I delete a document or add a newer version? 9. I do not understand the graph? 10. I click a node and ask a follow-up?

### (d) Indian-context numbers

None in the AI-03 report. CROSS ties AI-03 to the 101,928 cybercrime cases (see CROSS section).

---

## AI-04: RAG failure lab (retrieval vs generation diagnosis)

### (a) Top 10 fork candidates

| # | Name | URL | Licence | Last push | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | Ragas | https://github.com/vibrantlabsai/ragas (CROSS lists explodinggradients/ragas) | Apache-2.0 | 2026-02-24 | 16,034 | no hosted demo |
| 2 | DeepEval | https://github.com/confident-ai/deepeval | Apache-2.0 | 2026-10-16 | 18,938 | no OSS hosted dashboard |
| 3 | RAGChecker | https://github.com/amazon-science/RAGChecker | Apache-2.0 | 2024-12-13 | 1,126 | none; Bedrock Llama 3 70B workflow |
| 4 | HHEM 2.1 Open | https://huggingface.co/vectara/hallucination_evaluation_model | Apache-2.0 | 2024 | 370 HF likes | HF Space: https://huggingface.co/spaces/vectara/hhem-2.1-open-demo ; <600 MB RAM, ~1.5 s per 2,000 tokens on CPU (publisher claim) |
| 5 | LettuceDetect | https://github.com/KRLabsOrg/LettuceDetect | MIT | 2026-09-07 | 614 | local Streamlit demo; span-level highlights |
| 6 | UpTrain | https://github.com/uptrain-ai/uptrain | Apache-2.0 | 2024-08-18 | 2,367 | https://demo.uptrain.ai/evals_demo/ |
| 7 | Langfuse | https://github.com/langfuse/langfuse | MIT core, enterprise exceptions | 2026-10-21 | 36,132 | https://langfuse.com/demo |
| 8 | open-rag-eval | https://github.com/vectara/open-rag-eval | Apache-2.0 | 2026-10-08 | 417 | https://openevaluation.ai/ |
| 9 | RAG Auditor | https://github.com/amitgambhir/rag-auditor | MIT | 2026-04-19 | 1 | not verified; uses Anthropic API |
| 10 | MIRAGE | https://github.com/Betswish/MIRAGE | Apache-2.0 | 2025-03-10 | 25 | HF Space: https://huggingface.co/spaces/gsarti/mirage |

Licence traps flagged: Phoenix is Elastic License 2.0; Lynx 8B weights are CC BY-NC 4.0; the "Adversarial-RAG-evaluation" repo has no established licence. Report's stack: Ragas or DeepEval + RAGChecker-style reason codes + HHEM or LettuceDetect + custom Streamlit.

### (b) Best wow for a common person

"A failure microscope for RAG": upload a short policy (Air Canada style), ask the same question three ways: correct and supported; wrong because the clause was not retrieved; wrong although the clause is on screen. The judge swaps the evidence and watches the diagnosis flip. (CROSS version: "AI Courtroom: Who Lied?" with Evidence Finder vs Answer Writer lights.)

### (c) What-if questions (10)

1. The answer is not in any uploaded document? 2. It finds the wrong paragraph? 3. The right paragraph is there and it still lies? 4. Only one sentence is wrong? 5. Two documents disagree or one is outdated? 6. I paraphrase or use another language? 7. A document says "ignore the rules"? 8. Who checks whether your evaluator is wrong? 9. Can private documents stay offline? 10. Hundreds of questions or a slow laptop?

### (d) Indian-context numbers

None. Cost cases cited: Moffatt v. Air Canada CA$812.02 total (CanLII 2024 BCCRT 149); Mata v. Avianca $5,000 penalty (court PDF); Deloitte Australia over A$97,000 refunded on ~A$440,000 (AP / Yahoo Finance). Note: the Yahoo reference title says "over $60K", the text says A$97,000; currency mismatch not checked by us.

---

## HM-01: reproducible molecule analysis ("ProvenanceLab")

### (a) Top 10 fork candidates (from the report's recommended build)

| # | Name | URL | Licence | Last push | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | RDKit | https://github.com/rdkit/rdkit | BSD-3-Clause | 2026-10-24 | 3,635 | no (Python/C++) |
| 2 | RDKit.js / MinimalLib | https://github.com/rdkit/rdkit-js | BSD-3-Clause | 2026-09-19 | 253 | yes, native WASM (subset of RDKit) |
| 3 | ChEMBL Structure Pipeline | https://github.com/chembl/ChEMBL_Structure_Pipeline | MIT | 2025-11-24 | 250 | no |
| 4 | Ketcher | https://github.com/epam/ketcher | Apache-2.0 | 2026-10-23 | 917 | yes, standalone WASM (offline) or remote |
| 5 | 3Dmol.js | https://github.com/3dmol/3Dmol.js | BSD-3-Clause + bundled notices | 2026-10-21 | 1,030 | yes, WebGL |
| 6 | TeachOpenCADD | https://github.com/volkamerlab/teachopencadd | CC-BY-4.0 | 2026-09-01 | 1,085 | Jupyter, server-backed |
| 7 | ro-crate-py | https://github.com/ResearchObject/ro-crate-py | Apache-2.0 | 2026-10-14 | 89 | no |
| 8 | conda-lock | https://github.com/conda/conda-lock | MIT + bundled notices | 2026-10-23 | 564 | no |
| 9 | DVC | https://github.com/treeverse/dvc | Apache-2.0 | 2026-10-19 | 15,939 | no |
| 10 | datamol | https://github.com/datamol-io/datamol | Apache-2.0 | 2026-09-09 | 556 | no |

Also named: Mol* (1,035, MIT, web viewer), JupyterLite (4,912, BSD-3, browser runtime), Stmol (214, MIT, server-backed). Frozen data: ChEMBL 37 SQLite/SDF + checksums (CC BY-SA 3.0); PubChem monthly dumps (`CURRENT-Full` is a moving path, not a snapshot).

### (b) Best wow for a common person

"Same molecule has several meanings": `CCO` vs `OCC` show different byte hashes but matching chemistry identity; acid vs sodium salt shows a parent link, not identity; then Wi-Fi off and the run replays from the archived bundle; then a valid molecule from the retracted hexacyclinol paper (retracted 14 Nov 2012) renders fine but carries a red evidence warning. Product line from the report: "we show exactly what was submitted, what changed, where every value came from, why a value is missing."

### (c) What-if questions (10)

1. I type a molecule that cannot exist as drawn? 2. I write the same molecule differently? 3. I forget the left/right-handed version? 4. One entry is a salt or has a different charge? 5. These are tautomers? 6. A property is blank? 7. PubChem changes tomorrow or the Wi-Fi dies? 8. I run this on another laptop? 9. AI says it is a good drug? 10. The paper is wrong or retracted?

### (d) Indian-context numbers

None in HM-01. CROSS adds only that the Indian Pharmacopoeia sets identity, purity and strength standards (ipc.gov.in), no numbers.

---

## HM-02: Indian prescription safety checker

### (a) Top 10 fork candidates (report gives no star counts for any of these)

| # | Name | URL | Licence (as stated) | Last update (as stated) | Stars | Web run / backend |
|---|---|---|---|---|---|---|
| 1 | RxCheck (report's "strongest starting shell") | https://github.com/indiser/Rxcheck | MIT code | created 2026-05-28; commit NR | NR | Flask/PostgreSQL app; 34-brand mapping; OCR flow sends images to Gemini (CROSS) |
| 2 | Indian Medicine MCP Server | https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER | MIT code | created 2025-04-14 | NR | local service, 15 endpoints; needs a medicine JSON |
| 3 | A-Z Medicine Dataset of India | https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india | CC BY-SA 4.0 | "four years ago"; prices Nov 2022 | NR | downloadable CSV; only 2 composition fields |
| 4 | 1mg 117k Medicine Complete Data | https://www.kaggle.com/datasets/abhay13072009/1mg-117k-medicine-complete-data-with-image-link | uploader says MIT (does not license 1mg content) | "two months ago" | NR | downloadable NDJSON |
| 5 | India Medicines and Drug Info Dataset | https://www.kaggle.com/datasets/apkaayush/india-medicines-and-drug-info-dataset | CC BY-NC-SA 4.0 | "a year ago"; collected 2025 | NR | downloadable, ~300,000 rows claimed |
| 6 | DDInter 2.0 | https://ddinter2.scbdd.com/ | redistribution licence not established | data update 2024-05-14 | NR | working web interface; no public API established |
| 7 | RxNorm / RxNav (terminology only) | https://lhncbc.nlm.nih.gov/RxNav/ | public APIs; source terms vary | monthly; June 1, 2026 release seen | NR | REST + RxNav-in-a-Box; DDI API retired ~Jan 2, 2024 |
| 8 | RapidFuzz | https://github.com/rapidfuzz/RapidFuzz | MIT | NR | NR | local library |
| 9 | Med7 | https://github.com/kormilitzin/med7 | Apache 2.0 | Nov 2024 updates | NR | local spaCy models |
| 10 | CDSCO FDC lists | https://cdsco.gov.in/opencms/opencms/en/Drugs/FDC | official; machine-readable licence not established | lists dated 2024-08-02 and 2026-06-11 | n/a | website/PDF |

Also named: Medicine Drug Advisor (MIT, created 2025-06-18), MedOps medicine-dataset (253,973 products, licence not established), chinmays18 prescription OCR (MIT, 71% char / 84% word accuracy, author-reported), DrugBank open data 5.1.22 (CC0 vocab only, 2026-06-27).

Report defect spotted by us: the OpenEMR row cites [57], which in the reference list is the ICMR hypertension PDF (OpenEMR is [53]). Several rows also carry repeated citation strings like "[54] [54] [54] ...". Treat HM-02 citations as needing a check.

### (b) Best wow for a common person

Two different-looking brand cards collapse into one shared ingredient: synthetic Product A 650 mg paracetamol BD + Product B 500 mg TDS = 2,800 mg/day, shown as one grouped exposure card ("two products contain the same ingredient" plus "dose assessment uses these patient assumptions"); change age, weight or kidney context and the status changes, not just the colour. CROSS line: "Different Brands. Same Ingredient. One Warning."

### (c) What-if questions (10)

1. Two different brands both contain paracetamol? 2. The doctor misspells a brand? 3. One tablet has three or more drugs? 4. The prescription says OD, BD, TDS or SOS? 5. The patient is a child? 6. The patient has kidney disease? 7. Syrup, half tablet, injection or modified-release? 8. The combination is prohibited in India? 9. The doctor gets too many alerts? 10. Internet fails, brand unknown, or the AI makes something up?

### (d) Indian-context numbers (as cited)

| Number | Source cited by report |
|---|---|
| Indian hospital medication errors: 40 studies, 307,106 patients, median error rate 34.11% (2025 review) | PMC12683552 "Epidemiology of Medication Errors in Indian Hospital Settings" |
| Error stages: prescribing 40% (30 studies), administration 31% (28), transcription 22% (19), dispensing 11% (21); do not add them | same, PMC12683552 |
| Study quality: 31 moderate, 5 low, 4 high | same, PMC12683552 |
| CDSCO prohibited FDCs: 156 dated 2 Aug 2024; 16 dated 11 Jun 2026 (S.O. 3068(E) to 3083(E)) | cdsco.gov.in FDC portal + list PDFs + 2026 Gazette PDF |
| FDC ban commentary dated 24 Sep 2024 | PMC11970505 |
| A-Z dataset 32.06 MB, 9 cols; 250k dataset "over 248,000 drugs", 58 cols; MedOps 253,973 products; 1mg scrape 117,000+; Tata 1mg 2025 set ~300,000 rows | the respective Kaggle / GitHub cards |

---

## W3-01 + W3-02 (one run): ZK eligibility credential, and an AI agent wallet with hard limits

### (a1) W3-01 top 10 fork candidates

| # | Name | URL | Licence | Last push | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | Noir examples (exact-fit start) | https://github.com/noir-lang/noir-examples | MIT | 2026-04-29 | 78 | yes (local) web starters |
| 2 | snarkjs | https://github.com/iden3/snarkjs | GPL-3.0 | 2026-10-01 | 2,040 | yes (local browser) fullProve |
| 3 | circomlib | https://github.com/iden3/circomlib | LGPL-3.0 | 2026-10-22 | 749 | no (circuits) |
| 4 | Anon Aadhaar (India story) | https://github.com/anon-aadhaar/anon-aadhaar | MIT | 2025-04-21 | 253 | yes (browser-local) |
| 5 | ZK Email | https://github.com/zkemail/zk-email-verify | MIT | 2026-10-01 | 435 | yes (linked demo) |
| 6 | Semaphore | https://github.com/semaphore-protocol/semaphore | MIT | 2026-09-18 | 1,093 | yes (public demo); membership only, not signed-income |
| 7 | Noir web prover | https://github.com/Apertrue/noir-web-prover | Apache-2.0 | 2026-07-22 | 0 | yes (local browser) |
| 8 | zkPassport packages (current SDK) | https://github.com/zkpassport/zkpassport-packages | unresolved | 2026-10-23 | 40 | frontend + phone proving |
| 9 | Privado ID JS SDK | https://github.com/PrivadoID/js-sdk | Apache-2.0 | 2026-10-16 | 73 | no (SDK) |
| 10 | Self / OpenPassport | https://github.com/selfxyz/self | unresolved | 2026-10-23 | 1,264 | standalone browser proving not established |

Testing helpers named: zkbugs (351, MIT), Circomspect (269, GPL-3.0), Picus (52, MIT), 0xPARC zk-bug-tracker (731, MIT). Audits cited: ZK Email zkSecurity May 2024 (SHA256 template could return zero), yAcademy (missing range checks), Semaphore V4 Mar 2024 (critical scalar-range issues, fixed).

### (a2) W3-02 top 10 fork candidates

| # | Name | URL | Licence | Last push | Stars | Web run |
|---|---|---|---|---|---|---|
| 1 | ZeroDev Kernel | https://github.com/zerodevapp/kernel | MIT | 2026-10-05 | 259 | no (contracts) |
| 2 | Biconomy Nexus | https://github.com/bcnmy/nexus | MIT | 2026-08-07 | 60 | no; pin the fixed revision |
| 3 | SmartSessions | https://github.com/erc7579/smartsessions | AGPL-3.0 | 2025-10-15 | 61 | no; self-labelled beta |
| 4 | Safe7579 | https://github.com/rhinestonewtf/safe7579 | unresolved | NR | NR | no |
| 5 | Safe modules | https://github.com/safe-fndn/safe-modules | LGPL-3.0 | 2026-10-16 | 198 | no |
| 6 | Coinbase SpendPermissions | https://github.com/coinbase/spend-permissions | MIT | 2026-03-24 | 52 | yes: Sepolia deployments + local React example |
| 7 | x402 | https://github.com/coinbase/x402 | unresolved | NR | NR | yes: public testnet facilitator + web integration |
| 8 | Coinbase AgentKit | https://github.com/coinbase/agentkit | unresolved | 2026-10-14 | 1,334 | no (toolkit) |
| 9 | MetaMask delegation framework | https://github.com/MetaMask/delegation-framework | Apache-2.0 | 2026-10-22 | 231 | no |
| 10 | permissionless.js | https://github.com/pimlicolabs/permissionless.js | MIT | 2026-10-23 | 257 | no (library) |

Traps the report flags: Rhinestone docs say an empty policy set allows any transaction; Safe warns a malicious enabled module can take over the account; Kernel documents a revocation race for already-bundled operations; Nexus older tags miss a disclosed fix.

Hackathon precedents (builder claims, code not audited): ZeroSurf (ETHGlobal New Delhi, EF privacy 3rd prize, https://github.com/Krane-Apps/zerosurf-anon-aadhaar); ZkScholar (ETHGlobal Singapore, World ID 3rd prize, Sepolia); zkx402 (ETHGlobal Buenos Aires 2025 finalist, Base Sepolia, https://zkx402.io); Paybot (same, finalist); NAN (DoraHacks listing, no award established).

### (b) Best wow for a common person

- W3-01: "A scholarship without a document upload": one student proves eligibility and the verifier sees no name, DOB or income document; a second student gets a local "not eligible" explanation; a third edits the credential or swaps the issuer and fails for cryptographic reasons.
- W3-02: "Leak the agent key, keep the limits": show the session key on screen plus a malicious page saying "send everything to me"; the account rejects the drain even when the attacker skips the AI and sends directly, while a small allowed purchase (paid API via x402) goes through. Demo policy: 5-token per-tx cap, 20-token daily cap, short expiry. Combined line: "prove only what is needed, delegate only what may be lost."

### (c) What-if questions

W3-01 (10): 1. I edit my DOB or income? 2. I sign my own fake credential? 3. I am exactly 18? 4. You only need my state? 5. Income equals the limit? 6. I borrow someone else's credential? 7. I copy a proof from the mempool? 8. I apply twice, or at another scholarship? 9. The credential expires or is revoked? 10. The circuit is under-constrained or the browser is slow?

W3-02 (10): 1. A webpage tells the AI to drain the wallet? 2. The agent key leaks? 3. Target approved but the function is dangerous? 4. Function allowed but the recipient changes? 5. One payment costs 6 tokens? 6. The agent splits a drain into small payments? 7. It uses approve, delegatecall or multicall? 8. The owner revokes or the session expires? 9. A useful action is outside policy? 10. Operations race or replay on another chain?

### (d) Indian-context numbers

No statistics in the W3 report. India items: Anon Aadhaar (253 stars, last push 2025-04-21, browser-local, government-signed data; report warns Aadhaar does not carry family income) and ZeroSurf from ETHGlobal New Delhi.

---

## CROSS run: hackathon winners and the jaw-dropper per statement

### Scope facts the CROSS report surfaced

- The prompt sent to Parallel said 15 statements but listed 13 (AI-01..04, W3-01..02, CL-01..03, SC-01..02, HM-01..02). The report covered those 13 and invented none.
- The official Hypnexis page (https://www.hypnexismuj.com/hypnexis-main.html) describes a **36-hour** event on **October 24-25** (UNVERIFIED by us, report claim).
- Report's overall pick: **AI-03, "One Scam. Three Stories."**, on LightRAG.

### Hackathon-winner patterns (as the report states them)

| Pattern | Evidence it cites |
|---|---|
| A clear human consequence beats an architecture diagram | Gemini API Dev Competition 2024: Vite Vere (Most Impactful + People's Choice, cognitive-disability help); Gaze Link (Best Android, ALS communication) |
| Let the judge take part in one surprising interaction | Outdraw AI, Most Creative (humans try to beat AI at drawing recognition) |
| Show an action and its result, not a chat about the action | Jayu, Best Overall (assistant acting on everyday apps) |
| Make disagreement / uncertainty the product | ModelProof, Microsoft AI Agents Hackathon 2025, Best JS/TS |
| Turn invisible technical work into a verdict plus drill-down | PRism, Microsoft AI Dev Days 2026 Grand Prize (Deployment Confidence Score); RiskWise, Best Overall 2025 |
| AI-03 has a direct precedent | Bits2Brain, Best Java 2025: "Knowledge Star Map" from fragmented notes |
| A bounded domain-fit problem can win without spectacle | SIH 2024, Team Paradox (JMI), SIH1680 keyword spotting in audio, problem from NTRO |
| Indian winner centred on a familiar commercial decision | ASTRA (India), Best Multi-Agent, Microsoft AI Dev Days 2026 |
| Execution outweighs polish in at least one public rubric | AWS AI Agent Global Hackathon 2025: technical execution 50%, impact 20%, creativity 10%, functionality 10%, presentation 10%; ~3-minute video + deployed URL |
| Failure as the climax | proof altered and rejected, payment blocked, uncertain medicine match withheld |
| Popularity is not capability | Scam AI #1 Product Hunt 31 Jan 2025; Gemini 3 gallery winners Netra, Proofy.AI, Globot (no accuracy or reach data) |

### Jaw-dropping concept per statement (CROSS, proposed, not tested)

| Statement | Concept title | Ten-second reveal | Base the report names | Feasibility (report's estimate) |
|---|---|---|---|---|
| AI-01 | "Maa, It's Not Me" | familiar-voice emergency call, warning interrupts a fake payment | clovaai/aasist (MIT) | Medium |
| AI-02 | "Where Did The Canteen's Money Go?" | messy ledger becomes one explainable leakage chart with clickable rows + SQL | vanna-ai/vanna (MIT; swap out Claude Sonnet 4.5 default) | Medium |
| AI-03 | "One Scam. Three Stories." | three complaints connect through one payment handle, each edge opens its quote | HKUDS/LightRAG (MIT) | **High, narrow inputs** |
| AI-04 | "AI Courtroom: Who Lied?" | two red lights show whether retrieval or generation broke the answer | RAGChecker + Ragas (Apache-2.0) | Medium-high |
| W3-01 | "Scholarship Approval Without Showing Your ID" | valid proof, no name/DOB/income visible; tampered proof rejected | semaphore-protocol/boilerplate (MIT) | Medium |
| W3-02 | "Give An AI Pocket Money, Not Your Bank Account" | allowed purchase works, overspend rejected by the contract | zerodevapp/kernel (MIT) | Medium |
| CL-01 | "A Forest Change You Can Point To" | dated before/after slider shows a vegetation-loss candidate | Darren-Dcruz/Satellite-Deforestation-Detector (MIT, needs Earth Engine) | Medium-high with prepared imagery |
| CL-02 | "Your Receipt Has A Smoke Trail" | spending table unfolds into an emissions Sankey | ignite-analytics/carbon-accounting (CC BY-SA 4.0) + USEPA/useeior (MIT) | Medium |
| CL-03 | "Tomorrow's Hostel Energy Peak" | hostel digital twin shows tomorrow's forecast peak | buds-lab/building-data-genome-project-2 (3,053 meters, 1,636 buildings, 2016-17) | Medium |
| SC-01 | "Find The Car Without Reading Its Plate" | click a car, candidate sightings light up across cameras, plates masked | OpenVINO vehicle-reid-0001 (512-value embedding) | Medium |
| SC-02 | "The Shortest Path Is A Trap" | shortest route hits stairs, accessible route avoids them with photo evidence | ProjectSidewalk/SidewalkWebpage (MIT) + AccessMap | Medium on a tiny campus graph |
| HM-01 | "One Molecule, Two Runs, Inspectable Evidence" | molecule + descriptors + manifest; rerun matches; bad input fails visibly | RDKit (BSD) + napoles-uach/stmol (MIT) | High for a bounded analysis |
| HM-02 | "Different Brands. Same Ingredient. One Warning." | two brand cards expand to one shared ingredient, pharmacist-review flag | indiser/Rxcheck (MIT) + INDIAN_MEDICINE_MCP_SERVER | Medium |

Proposed 12-hour plan for AI-03 (report): 0-1 h run backbone and check licences; 1-3 h synthetic fixtures + schema + one API contract with a provenance field on every edge; 3-6 h ingest, extract, topic augmentation, graph, evidence panel; 6-8 h story and transitions (must work without sound or 3D); 8-10 h hostile tests (wrong identifier, contradiction, injected instruction, timeout); 10-11 h clean deploy; 11-12 h rehearse and freeze. Three-minute script: stakes (0:15), reveal (0:30), proof (1:10), what-if retraction (1:50), contribution (2:30), limits (3:00).

### Indian-context numbers from CROSS (as cited)

| Number | Source cited |
|---|---|
| 101,928 cybercrime cases in 2024 (all cybercrime, not voice-clone); 1930 helpline for complaints | PIB / MHA press release PRID 2287039, 21 Jul 2026 |
| DPDP Rules notified 14 Nov 2025, phased compliance | PIB PDF doc20251117695301 |
| India Cooling Action Plan: 20-25% less cooling demand, 25-40% less cooling energy by 2037-38 (targets) | PIB PRID 1568328 |
| SIH 2024 winner Team Paradox, JMI, SIH1680 | JMI press release, 19 Dec 2024 |
| Hypnexis: 36 hours, Oct 24-25 | hypnexismuj.com official page |

---

## Cross-run red flags for whoever uses this

| Flag | Where | Grade |
|---|---|---|
| Report says "15 statements" were requested but only 13 were enumerated in our prompt | CROSS | VERIFIED (report text says so; worth checking our own brief) |
| Ragas owner differs: vibrantlabsai/ragas (AI-04) vs explodinggradients/ragas (CROSS); likely a rename or redirect | AI-04, CROSS | UNVERIFIED |
| HM-02 OpenEMR row cites the wrong reference number; repeated "[n] [n] [n]" citation strings | HM-02 | VERIFIED as a text defect in the report |
| Spectra-AASIST licence conflict (Apache-2.0 header vs MIT body) | AI-01 | UNVERIFIED (report claim) |
| Vanna archived with 23,816 stars; Vanna quickstart default model breaks the <=8B rule | AI-02, CROSS | UNVERIFIED (report claim) |
| RxNav drug-interaction API discontinued around 2 Jan 2024 | HM-02 | UNVERIFIED (report claim) |
| Deloitte refund: text A$97,000 vs reference title "$60K" | AI-04 | UNVERIFIED, likely USD vs AUD |
| All stars / pushes are the report's snapshot as of its run (08:52-09:05 UTC, 2026-10-24) | all | as stated |
