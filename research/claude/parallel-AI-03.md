<!-- run id: trun_3b693d434bb94e6dad9164f0529a3e55 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6dad9164f0529a3e55
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:11.017878Z
**Modified:** 2026-10-24T09:01:41.867778Z

## Output

# Build AI-03 Faster With Proven GraphRAG Components

## Executive Summary

- **Best General Starting Point**: LightRAG already documents document parsing, graph/vector storage, five query modes, source attribution, a WebUI and REST API. Its remaining AI-03 gap is not basic RAG; it is explicit community reporting and answer-to-graph synchronization. -> Start here if you want to build rather than integrate a large platform. [22]
- **Closest Graph-First Application**: Neo4j LLM Graph Builder already accepts PDFs/text, extracts relationships, previews graphs and chats with source metadata. -> Fork it if a graph database and visible provenance matter most; add demonstrable theme/community routing. [8]
- **Best Match To Thematic Retrieval**: Microsoft GraphRAG's global search uses community reports, while local search combines graph neighborhoods with source text. -> Use it, nano-graphrag or RAGU when the judging criterion really means community-level reasoning, not merely a colorful graph. [75][67][19][52]
- **Strong Regional Alternatives**: Tencent WeKnora, Yuxi, ApeRAG and HuixiangDou are real repositories, not just English-language list entries. -> Compare these before building document management, multilingual chat and deployment plumbing from scratch. [30][31][27][29]
- **Small Server Is Not A Free Pass**: RAGFlow recommends a starting configuration of **4 CPU cores, 16 GB RAM and 50 GB disk**. Microsoft estimates graph extraction at **roughly 75%** of its indexing cost. -> Pre-index the showcase corpus and separate upload/indexing work from interactive answering. These are project-specific figures, not universal requirements. [18][72]
- **The Missing Product Layer**: A graph viewer, a chat pane and citations do not by themselves prove that the displayed path produced the answer. -> Return evidence node, edge, chunk and community identifiers with every answer, and drive the visualization from that payload.
- **Beautiful Does Not Mean Grounded**: Graphologue generates interactive diagrams from LLM responses; Zilliz's vector-graph-rag explicitly avoids a graph database. -> Both are useful, but neither should be presented as satisfying an unmodified graph-DB-plus-vector-DB requirement. [90][99]
- **Demo Reliability Beats Demo Links**: The inspected Harry Potter and GraphRag_upload Spaces reported runtime errors; both Knowledge-graphs Spaces reported build errors. -> Treat hosted links as references, not as your live-demo dependency. [81][78][77][80]

**Recommendation:** Build a LightRAG-based backend plus a custom React evidence graph, or fork Neo4j LLM Graph Builder and add community reports. If the rubric strictly requires a separate graph database and vector database, explicitly configure both rather than relying on an in-memory graph or a single database's vector index.

**Scope and confidence:** This is a broad verified landscape, not a provable census of every repository on the internet. Repository existence and the cited documented features are verified; I did not execute every application. No candidate below was verified to meet all five deliverables, including the exact answer-synchronized split screen, unchanged. UI assessments and combination choices are editorial judgments. **NR** means not recovered or confirmed in the consulted material, not necessarily undisclosed. Stars and last-push dates are retrieved snapshots; last push is not the same as latest release or latest default-branch commit.


## 1. Turn The Five Deliverables Into A Build Contract

The most consequential distinction is between **thematic retrieval** and **graph-assisted factual retrieval**. Microsoft's local search identifies relevant entities and expands into relationships, community reports and source text. Its global search instead aggregates community reports to answer corpus-wide questions. DRIFT, or Dynamic Reasoning and Inference with Flexible Traversal, combines broad community-level initialization with more detailed follow-up retrieval. [67][75][74]

Use the following five deliverables throughout the catalogs. A documented component is not the same as a complete end-to-end implementation.

| Deliverable | What a convincing AI-03 implementation must show | Common false positive |
|---|---|---|
| **D1: Ingest And Extract** | PDF/text upload, readable chunks, entities and typed relationship triples | A preloaded graph with no document pipeline |
| **D2: Discover Themes** | Community membership, meaningful labels and preferably community summaries | Node colors or a UI's light/dark "themes" |
| **D3: Store Both Representations** | Persistent graph plus vector retrieval, with identifiers joining them | A diagram, or TF-IDF alone, described as two databases |
| **D4: Route And Ground** | Thematic versus local factual retrieval, source-backed answers and inspectable retrieval evidence | A mode selector without evidence that retrieval changes |
| **D5: Synchronize The Interface** | Uploader/chat beside a clickable graph; each answer focuses its communities, documents and paths | Separate chat and graph tabs that never exchange answer evidence |

**Takeaway:** The defensible differentiator is D5 joined to D4: show the actual evidence selected for an answer, not a decorative overview.

### Case Study: Neo4j Builder Gets You To A Visible Graph Quickly

Neo4j's builder documents ingestion of PDFs, DOCs and TXTs, entity/relationship extraction, conversational queries, source metadata and graph previews for selected files. It also documents Docker Compose deployment and a hosted application. That is unusually close to the user's desired product surface. [8]

The remaining decision is what to add, not whether to rebuild ingestion. For this hackathon, I would preserve its document-to-chunk-to-entity structure, add a community-report layer and expose an answer-evidence endpoint. A retrieval mode called `global_vector` is not, by its name alone, proof of Microsoft's community-report global search; demonstrate that distinction explicitly. [8][75]

### Case Study: Microsoft GraphRAG Trades Indexing Work For Corpus-Level Answers

Microsoft GraphRAG is a research pipeline rather than a finished hackathon web application. Its community reports give a concrete answer to "What themes run across these documents?", while its local search supplies entity-centered factual retrieval. Microsoft warns that indexing can be expensive and recommends prompt tuning for the user's own data. [1][75][67]

That makes it a strong methodological fit but a less direct UI starting point. Pairing it with GraphRAG Visualizer removes some artifact-exploration work, but you still need PDF handling, a request API and answer-specific graph selection. Also, Microsoft's **FastGraphRAG indexing method** is not the same project as Circlemind's **fast-graphrag** library. [14][72][20]


## 2. Retrieval Engines: Choose Community Reasoning Or Graph Neighborhoods

| Project | Plain-Words Description / Evidence | D1 Ingest + Extract | D2 Themes | D3 Graph + Vectors | D4 Routing + Grounding | D5 Interface |
|---|---|---|---|---|---|---|
| LightRAG | Document-to-KG RAG with an application server. [22] | PDF/text; entities/relations | High/low-level retrieval; community reports not established | Graph + vector backends | Local/global/hybrid/mix modes; citations | WebUI graph + chat; exact synchronization NR |
| Microsoft GraphRAG | Reference text-to-graph and community-report pipeline. [1][75] | Text pipeline; add PDF parser | Community reports + hierarchy | Graph/artifact + retrieval indexes; deployment choice matters | Global/local; DRIFT available | No turnkey split-screen app |
| nano-graphrag | Small, hackable GraphRAG implementation. [19] | Text; entities/relations; add PDF parser | Community reports | Replaceable graph/vector storage | Local/global; inspect source handling | Application UI to add |
| KAG | OpenSPG-based logical reasoning and professional-domain QA. [9] | Unstructured/structured knowledge construction | Not established as community-report routing | Graph-to-text cross-indexing; inspect chosen storage | Logical/multi-hop reasoning; source cross-index | Local web product; exact split screen NR |
| HippoRAG | Associative knowledge/memory retrieval with an index-serving interface. [12] | Text/OpenIE; add PDF parser | Not a verified community-report implementation | Local vectors or Qdrant/Chroma/Milvus | Passage retrieval with scores/source metadata | No verified end-user graph/chat UI |
| fast-graphrag | Promptable retrieval using Personalized PageRank. [20] | Text examples; add PDF parser | No verified thematic community layer | Graph-backed retrieval; inspect configured stores | Factual retrieval; reference-output tutorial | No verified split-screen app |
| Neo4j GraphRAG Python | Official Python construction/retrieval building blocks. [21] | KG pipeline with typed entities/relations | Add community computation/reports | Neo4j vectors; external vector retrievers supported | Vector/graph RAG building blocks | Backend SDK, not finished UI |
| FalkorDB GraphRAG SDK | Document-to-graph retrieval with traceable source chunks. [16] | PDF extra; entity/relation extraction | Community routing NR | FalkorDB graph + vector/full-text indexing | Source trace through MENTIONED_IN; return_context | SDK; build the answer-linked viewer |
| RAG-Anything | Multimodal ingestion/retrieval built around LightRAG. [23] | PDF/Office/images; multimodal entities | Inherited retrieval; community reports NR | Graph/vector fusion; configurable backends | Text/multimodal query paths; grounding inspect | Not a verified complete split-screen app |
| MiniRAG | Lightweight heterogeneous-graph retrieval for small-model settings. [70] | Indexing workflow; PDF layer NR | Not established as community-summary routing | Multiple graph backends documented | Graph-based retrieval; source UX NR | API/Docker, not verified finished graph UI |
| RAGU | Text-to-KG engine with several retrieval strategies. [52] | Text; typed entities/relations | Community summaries | Graph + vector retrieval | Local/global/vector/mixed + planner; answer citations NR | No verified graph/chat frontend |
| AWS GraphRAG Toolkit | Python graph-enhanced GenAI tools, including a lexical-graph framework. [87] | Construction framework | Detailed fit NR | Backend-specific; inspect deployment | Graph-enhanced retrieval framework | Not verified as an end-user app |
| Vector Graph RAG | Encodes entities/relations as vectors and retrieves multi-hop evidence. [99] | PDF/DOCX/web loaders; triples supported | Community summaries NR | Milvus; explicitly no graph DB required | Graph-like expansion + configurable reranking | React graph UI + FastAPI; exact evidence sync NR |
| Unified GraphRAG Research | Modular comparison framework, not a ready-made document product. [92] | Entity/relation KG construction | High-level structures for MS GraphRAG | Research-method dependent | Local/global variants; evaluate implementation | Application UI NR |

**Takeaway:** Microsoft GraphRAG, nano-graphrag and RAGU most directly expose the thematic/local distinction. LightRAG offers the more convenient application foundation, while Neo4j and FalkorDB make source-connected graph storage natural.

### Metadata, Deployment And Recommended Combinations

The deployment and UI columns below are recommendations or assessments, not measured capacity guarantees. A documented demo link is not a successful live runtime test.

| Project | URL | Stars | Last Push | License | Hosted Demo | Website / Small-Server / API Fit | UI Assessment | Combine With |
|---|---|---|---|---|---|---|---|---|
| LightRAG | https://github.com/HKUDS/LightRAG | 40235 | 2026-10-15 | MIT [24] | Video/setup demo; public live service NR | REST server + WebUI; plausible small-corpus API-backed deployment | Useful admin UI; custom polish recommended | RAG-Anything + react-force-graph |
| Microsoft GraphRAG | https://github.com/microsoft/graphrag | 36398 | 2026-10-20 | MIT [25] | Quickstart, not a verified hosted end-user app | Wrap library/CLI; index off request path | Backend only | GraphRAG Visualizer + FastAPI + PDF parser |
| nano-graphrag | https://github.com/gusye1234/nano-graphrag | 3990 | 2026-01-27 | MIT [37] | Examples; live service NR | Python/async methods; wrap API | Backend only | Kotaemon or custom React UI |
| KAG | https://github.com/OpenSPG/KAG | 9082 | 2026-01-28 | Apache-2.0 [39] | Local browser product; public demo NR | Docker Compose; SDK development path | Product interface; visual synchronization NR | OpenSPG tooling + custom evidence graph |
| HippoRAG | https://github.com/OSU-NLP-Group/HippoRAG | 4073 | 2026-10-06 | MIT [38] | Examples; hosted demo NR | Python and HTTP MCP; local or hosted model endpoints | Backend only | PDF parser + react-force-graph |
| fast-graphrag | https://github.com/circlemind-ai/fast-graphrag | 3965 | 2025-11-01 | MIT [35] | README advertises managed service; live health NR | Async Python library; hosted-model integration | Backend only | PDF parser + evidence API + graph renderer |
| Neo4j GraphRAG Python | https://github.com/neo4j/neo4j-graphrag-python | 1317 | 2026-10-24 | Unresolved; read LICENSE [36] | Examples; standalone demo NR | Python SDK behind your API; Neo4j required | Backend only | Neo4j Builder + community reports |
| FalkorDB GraphRAG SDK | https://github.com/FalkorDB/GraphRAG-SDK | 1014 | 2026-10-12 | Apache-2.0 [62] | Examples/documentation; hosted app NR | Python + FalkorDB Docker; benchmark target hardware first | Build own user-facing graph | React graph + return_context adapter |
| RAG-Anything | https://github.com/HKUDS/RAG-Anything | 23544 | 2026-10-12 | MIT [59] | Examples; standalone hosted app NR | Python package; OCR/parsing can dominate resources | Backend/multimodal support, not complete app | LightRAG server + document preview |
| MiniRAG | https://github.com/HKUDS/MiniRAG | 2018 | 2025-10-16 | MIT [58] | README documents API/Docker | API container; small-model suitability is an author positioning, not a server benchmark | Backend-oriented | PDF parser + visual evidence layer |
| RAGU | https://github.com/RaguTeam/RAGU | 139 | 2026-10-04 | MIT [57] | Examples; hosted app NR | Python retrieval/query methods; expose your API | Backend only | Neo4j/other persistence adapter + React |
| AWS GraphRAG Toolkit | https://github.com/awslabs/graphrag-toolkit | NR | NR | Apache-2.0[525.4] | Examples; hosted end-user demo NR | Infrastructure-oriented; not my tiny-server first choice | Backend only | Custom frontend and provenance adapter |
| Vector Graph RAG | https://github.com/zilliztech/vector-graph-rag | NR | NR | MIT[526.4] | Documented local frontend; hosted demo NR | FastAPI + React; Milvus Lite/server/cloud options | Promising ready-made graph surface | Add real graph DB if rubric demands one |
| Unified GraphRAG Research | https://github.com/JayLZhou/GraphRAG | NR | NR | NR | Research examples; hosted app NR | Python research code; local/cloud LLM backends | Research-oriented | Borrow methods, not a production UI |

**Takeaway:** Do not choose by stars alone. Select the retrieval mechanism that answers the rubric, then minimize the number of stores and services you must operate.

### Case Study: Zilliz Removes A Database, But Changes The Compliance Story

Zilliz's vector-graph-rag explicitly represents entities and relations in Milvus, supports multi-hop expansion and supplies a React graph frontend plus FastAPI. Its documentation supports Milvus Lite as well as server/cloud deployment. This is a particularly relevant niche discovery because it includes more visible application plumbing than many research libraries. [99]

The trade-off is explicit: it says **no graph database is required**. If the judges accept graph-structured retrieval regardless of physical storage, that can simplify the build. If D3 literally demands a graph DB plus a vector DB, add graph persistence or choose another foundation; do not relabel the vector representation as a second database. Its "SOTA" wording is an author claim, not an independently established result in this report. [99]


## 3. Full-Stack And Niche Apps: Reuse Product Plumbing Carefully

| Project | Description / Evidence | D1 Ingest + Extract | D2 Themes | D3 Storage | D4 Retrieval + Grounding | D5 Graph/Chat |
|---|---|---|---|---|---|---|
| Neo4j LLM Graph Builder | PDF/text to Neo4j, graph previews and conversational queries. [8] | PDF/text + triples | Add/verify community layer | Neo4j graph/vector; separate vector DB optional | Several retrieval modes + source metadata | Graph + chat; exact answer-linked path focus NR |
| Kotaemon | Document-chat app with detailed citations and document previews. [13] | PDF/text; graph strategy dependent | Depends on selected GraphRAG backend | Configurable document/vector stores | Hybrid RAG; citations; GraphRAG integration inspect | Clean chat/doc viewer; answer graph sync NR |
| RAGFlow | Document ingestion, retrieval workflows and grounded citation UI. [18] | PDF/text and many formats | Exact community routing NR | Inspect current graph configuration | Agentic retrieval + grounded citations | Product UI; exact answer-path graph NR |
| GraphRAG Visualizer | Viewer for GraphRAG-generated Parquet artifacts. [14] | Consumes artifacts; no PDF extraction | Displays communities/reports | Uses artifacts; requires upstream persistence | Search through separate graphrag-api | 2D/3D + node search; exact chat sync NR |
| GraphRAG Local UI | Local-model GraphRAG with FastAPI and Gradio/Plotly interfaces. [6] | TXT; PDF listed as upcoming | GraphRAG-dependent | GraphRAG artifacts/stores | Global/local/direct chat | 2D/3D graph; multiple/legacy apps |
| GraphRAG Local UI NC | An NC fork of the same local GraphRAG UI ecosystem. [7] | TXT; PDF not verified implemented | GraphRAG-dependent | Inherited artifacts/stores | Global/local/direct chat | Plotly graph; not verified synchronized split screen |
| R2R | REST-first ingestion, retrieval and document management with KG extraction. [4] | PDF/text + entities/relations | Community routing NR | Hybrid/KG platform; inspect selected persistence | Hybrid retrieval + cited answers | Complete answer-linked node graph NR |
| Text To Knowledge Graph | Small PDF/text-to-concept graph project with community coloring. [11] | PDF/text; concepts/proximity, not strictly NER | Community coloring | DataFrames; graph DB a later-stage option | Q&A use case, not full verified grounded router | Pyvis graph; full split screen absent from evidence |
| GraphRAG vs VectorRAG | Teaching/demo app showing extraction, communities and query traces. [56] | Text corpus + triples | Communities + LLM summaries | NetworkX + TF-IDF; not two DBs | Vector/graph/hybrid; source IDs and route | Interactive graph + trace; answer-path sync NR |
| Enterprise Starter | Local PDF comparison of flat RAG and community-enhanced RAG. [48] | PDF + extraction pipeline | Greedy-modularity communities + summaries | NetworkX + Chroma; graph DB to add | Graph/vector comparison; answer citations NR | Finished chat/graph UI NR |
| Knowledge Graph Skill | Tiny agent knowledge store with extraction, traversal and clickable visualization. [51] | Articles/text + entities/relations | No community-summary layer verified | Embedded graph; BM25/fuzzy, not vector DB | Traversal/search; grounded answer router to add | Force graph with clickable navigation |
| MiroFish | Multi-agent simulation/prediction product, not the same as document-grounded QA. [91] | Seed extraction; exact AI-03 PDF path NR | Community report fit NR | Required stores inspect | Simulation, not verified local/global grounded QA | Frontend/backend; exact evidence synchronization NR |

**Takeaway:** The niche comparison apps may teach the judges more clearly than a large platform. Their gaps are usually ingestion robustness, persistent storage and source-level traceability, not the basic force graph.

| Project | URL | Stars | Last Push | License | Hosted Demo | Website / Server / API | UI Assessment | Combine With |
|---|---|---|---|---|---|---|---|---|
| Neo4j LLM Graph Builder | https://github.com/neo4j-labs/llm-graph-builder | 5283 | 2026-10-17 | Apache-2.0 [26] | https://llm-graph-builder.neo4jlabs.com/ | Docker Compose / cloud deployment | Strong graph-first starting point | Community reports + answer-evidence adapter |
| Kotaemon | https://github.com/Cinnamon/kotaemon | 25829 | 2026-07-14 | Apache-2.0 [34] | https://huggingface.co/spaces/cin-model/kotaemon | Docker; Gradio application | Strong document-evidence UI | nano-graphrag or LightRAG + graph panel |
| RAGFlow | https://github.com/infiniflow/ragflow | 92773 | 2026-10-23 | Apache-2.0 [33] | https://cloud.ragflow.io/ | Docker/source + APIs; recommended 4 CPU/16 GB/50 GB | Strong document/product surface; heavier stack | Custom graph/evidence API |
| GraphRAG Visualizer | https://github.com/noworneverev/graphrag-visualizer | 429 | 2026-02-25 | MIT [32] | https://noworneverev.github.io/graphrag-visualizer/ | Static frontend + separate API/indexing backend | High-value graph exploration starter | Microsoft GraphRAG + upload service |
| GraphRAG Local UI | https://github.com/severian42/GraphRAG-Local-UI | 2319 | 2024-11-09 | MIT [40] | NR; README examples | FastAPI; local-model hardware additional | Functional prototype; transition/compatibility risk | PDF parser + modern graph frontend |
| GraphRAG Local UI NC | https://github.com/NavigatingCancer/GraphRAG-Local-UI-NC | 0 | 2024-11-09 | MIT [41] | NR | FastAPI + local interfaces | Fork, not an independent product architecture | Same additions as upstream |
| R2R | https://github.com/SciPhi-AI/R2R | 8018 | 2025-11-07 | MIT [66] | README video; public live demo NR | REST API; Docker full mode | API-rich; frontend fit requires inspection | React graph + community summaries |
| Text To Knowledge Graph | https://github.com/rahulnyk/knowledge_graph | 4161 | 2026-08-15 | MIT [65] | https://rahulnyk.github.io/knowledge_graph/ | Local Docker/personal-machine setup | Excellent minimal visual prototype | Chroma + graph DB + real citation-aware QA |
| GraphRAG vs VectorRAG | https://github.com/Rani8982/graphrag-vs-vectorrag | NR | NR | NR | NR | FastAPI + React/Vite | Especially useful explanatory demo pattern | Real PDF upload + embeddings + persistent stores |
| Enterprise Starter | https://github.com/kanerika-ai/graphrag-enterprise-starter | NR | NR | MIT[347.168-169] | NR | Local Python/model execution; not capacity-tested | Teaching/backend starter | React graph + persistence + provenance |
| Knowledge Graph Skill | https://github.com/Neurons-AI/knowledge-graph-skill | NR | NR | MIT[348.109-110] | NR | Pure JS, Node 18+, zero dependencies documented | Lightweight interaction inspiration | PDF parser + embeddings + community layer |
| MiroFish | https://github.com/666ghj/MiroFish | NR | NR | AGPL-3.0[523.4] | README links a live demo | Source or Docker deployment | Adjacent product/storytelling inspiration | Use patterns, not prediction claims as evidence |

**Takeaway:** Start from Neo4j Builder for the graph workflow or Kotaemon for the document-evidence workflow. Choose RAGFlow only if its broader stack solves needs you actually have.

### Case Study: Kotaemon Makes Evidence Readable, But Not Automatically Graphical

Kotaemon explicitly emphasizes detailed citations with document previews and offers multimodal parsing options, including OCR, tables and figures. Its Gradio UI is customizable, and it links hosted demos. These are valuable properties for a non-expert audience: they make an answer's source visible instead of asking the audience to trust a retrieval label. [13]

The extension I would build is a graph-selection bridge: clicking a citation selects the corresponding chunk and its extracted entities; selecting an entity opens the cited page. Do not assume backend compatibility is effortless: Kotaemon explicitly warns that installing nano-graphrag can introduce version conflicts. Freeze a known-working dependency set before polishing the UI. [13]

### Case Study: An Older Local UI Is A Prototype, Not A Maintenance Shortcut

GraphRAG Local UI documents global/local chat, a FastAPI service and 2D/3D Plotly visualization. However, its README describes a transition between separate applications and a legacy main UI; PDF support appears in its upcoming-features list rather than the verified TXT workflow. Its repository push snapshot is **2024-11-09**, despite the research request favoring 2025-2026 material. [6][40]

That is not a reason to discard the project. It is a reason to borrow its API and interaction ideas rather than promising an unchanged modern full-stack deployment. The NC fork is a real additional candidate, but inherited functionality and an inherited push timestamp are not evidence of an independently maintained new implementation. [7][41]


## 4. Chinese And Regional Projects: Real Alternatives, Uneven Fit

| Project | Description / Evidence | D1 Ingest + Extract | D2 Themes | D3 Storage | D4 Routing + Grounding | D5 Interface |
|---|---|---|---|---|---|---|
| Tencent WeKnora | Enterprise document knowledge framework with cited QA and GraphRAG. [30] | PDF/text + KG extraction | Wiki/page graph; community summaries not established | Neo4j + vector/keyword retrieval | Hybrid/agent retrieval; cited answers | Page graph; exact answer-linked triple graph NR |
| Yuxi / Yuxi-Know | Chinese knowledge-base/KG agent platform; older URL is xerrors/Yuxi-Know. [31][60] | MinerU/PaddleX/RapidOCR; exact extraction flow inspect | Community reports NR | Milvus + Neo4j listed with other services | RAG/agents and source-oriented chat | Workspace/chat; exact clickable path sync NR |
| ApeRAG | Graph/vector/full-text RAG platform with summary and vision indexes. [27] | Document platform; exact PDF-to-triple coverage inspect | Summary index is not proven community hierarchy | Graph/vector/full-text indexes | Hybrid retrieval; precise citation behavior inspect | Web app; exact answer graph synchronization NR |
| HuixiangDou | Professional knowledge assistant, including group-chat scenarios. [29] | PDF/text supported | Community thematic routing NR | Dense/sparse/KG retrieval documented | Knowledge assistant; answer-level citation UX NR | Web/mobile/pipeline code; exact graph UI NR |

**Takeaway:** Tencent WeKnora and Yuxi deserve first-pass evaluation, not an appendix. Neither a wiki link graph nor a summary index should automatically receive credit for semantic community-report retrieval.

| Project | URL | Stars | Last Push | License | Hosted Demo | Website / Server / API | UI Assessment | Combine With |
|---|---|---|---|---|---|---|---|---|
| Tencent WeKnora | https://github.com/Tencent/WeKnora | 35064 | 2026-10-22 | Unresolved; read LICENSE [63] | https://weknora.weixin.qq.com/ | Compose, Helm, Lite binary; SDK/API options | Strong product candidate | Custom community reports + graph evidence endpoint |
| Yuxi / Yuxi-Know | https://github.com/xerrors/Yuxi | 7475 | 2026-10-23 | MIT [60] | NR | FastAPI + async worker; Docker Compose | Strong application foundation; multiple services | Community detection + evidence graph |
| ApeRAG | https://github.com/apecloud/ApeRAG | 1321 | 2026-09-12 | Apache-2.0 [61] | NR | Compose; browser UI + API docs; Helm option | Product-oriented; validate graph interaction | Custom provenance panel |
| HuixiangDou | https://github.com/InternLM/HuixiangDou | 2502 | 2025-11-24 | BSD-3-Clause [64] | https://openxlab.org.cn/apps/detail/tpoisonooo/huixiangdou-web | HTTP server; local model resources depend on setup | Chat-first rather than graph-first | Graph viewer + source/citation adapter |

**Takeaway:** Ant/OpenSPG KAG and AntV G6/Graphin cover different layers: reasoning infrastructure versus visualization. They can complement each other, but a shared ecosystem is not proof of plug-and-play integration. [9][53][42]

### Case Study: WeKnora's Two Kinds Of Graph Need Different Demo Promises

WeKnora documents PDF/TXT ingestion, cited knowledge-base answers and hybrid retrieval with GraphRAG. Its KG documentation describes entity/relationship extraction at ingestion and relationship-based retrieval at question time, using Neo4j and APOC. This is a substantive KG backend, not just a mind-map label. [30][76]

But its source-oriented documentation distinguishes the KG retrieval tool from a dedicated visualization REST endpoint, while the broader product also exposes relationships among wiki pages. For AI-03, I would add an adapter returning entity, relationship and source-chunk identifiers for each answer, rather than claiming the wiki graph already proves the answer's reasoning path. [76][30]

### Regional Leads And Boundaries That Should Not Be Hidden

| Lead / Ecosystem | Located URL Or Evidence | What Is Established | What Is Not Established |
|---|---|---|---|
| Ant / OpenSPG KAG | https://github.com/OpenSPG/KAG | OpenSPG-based reasoning framework; Apache-2.0; cataloged above. [9] | Exact AI-03 split screen |
| AntV visualization | https://github.com/antvis/G6 ; https://github.com/antvis/Graphin | Real open-source graph libraries. [53][42] | Document ingestion or grounded QA supplied by those libraries |
| Baidu KG service | https://ai.baidu.com/solution/kgaas | Located institutional KG product lead | An original reusable open-source AI-03 implementation, license, stars and runnable code were not confirmed |
| Gitee niche lead | https://gitee.com/wang_zhu_ge/knowledge-graph | Located knowledge-graph QA repository lead | License, update, stars, deliverable coverage and usable demo remain NR |
| Japanese tutorial lead | https://qiita.com/nogataka/items/9eedb6b88eb84042e699 | Located Japanese GraphRAG-related write-up | Independently verified full-stack original repository and reuse license remain NR |
| Korean learning repository lead | https://github.com/teddylee777/langchain-kr | Located Korean LangChain learning repository | A distinct complete AI-03 application was not established; stars/update/license not recovered here |
| GitCode / ModelScope / Zhihu / CSDN | No additional original implementation verified strongly enough to score | These remain useful discovery channels | I cannot honestly turn mirrors, tutorials or unattributed screenshots into additional verified projects |
| NetEase QAnything | https://github.com/netease-youdao/QAnything | Real PDF/text QA system, Docker/API, AGPL-3.0. [28] | KG extraction, communities and answer-linked graph were not established |

**Takeaway:** These are retained leads, not quietly discarded candidates. Their missing fields remain explicit; they should not inflate the count of verified close matches.


## 5. Graph UI Libraries: Buy Visual Leverage, Not Retrieval Claims

Every library in the next table is a **component**, not a full AI-03 backend. For D1, D2, D3 and D4, the answer is "supply or connect those capabilities yourself"; Graphology provides graph modeling/algorithms rather than the document and answer pipeline. For D5, each renderer supplies some interaction primitives, but none should receive automatic credit for answer-to-source synchronization. [93][55][53][54]

| Library | URL | Plain-Words Description | Stars | Last Push | License | Hosted Demo | Website / API Fit | Visual Assessment | Combine With |
|---|---|---|---|---|---|---|---|---|---|
| react-force-graph | https://github.com/vasturiano/react-force-graph | React force graphs in 2D/3D/VR/AR, with hover/click/zoom/drag. [55] | 3319 | 2026-09-29 | MIT [97] | Repository example gallery | Browser component; integrate with any API | Best default for a dramatic but controllable React demo | LightRAG / Neo4j evidence JSON |
| 3d-force-graph | https://github.com/vasturiano/3d-force-graph | Standalone 3D force-directed graph component. [49] | 6489 | 2026-09-29 | MIT [94] | https://vasturiano.github.io/3d-force-graph/example/basic/ | Static browser application; API-fed data | High spectacle; keep labels and camera motion restrained | Custom web app or wrapper |
| Sigma.js | https://github.com/jacomyal/sigma.js | WebGL graph renderer designed for thousands of nodes/edges. [46] | 12174 | 2026-09-16 | MIT [98] | https://www.sigmajs.org/ | Browser renderer; Graphology companion | Excellent dense 2D atlas; less confusing than 3D for inspection | Graphology + community metadata |
| G6 | https://github.com/antvis/G6 | Graph drawing, layouts, analysis, interaction and animation. [53] | 12322 | 2026-09-23 | MIT [96] | https://g6.antv.antgroup.com/en/examples | Browser library; API-fed graph | Strong polished, controllable enterprise-style graph | Neo4j / KAG / WeKnora adapter |
| Graphin | https://github.com/antvis/Graphin | React graph-analysis toolkit built on G6. [42] | 1099 | 2025-11-18 | MIT [95] | Repository examples; hosted demo health NR | React library; API-fed graph | Useful React wrapper; check version alignment | G6-compatible custom evidence UI |
| Reagraph | https://github.com/reaviz/reagraph | React network visualization built in WebGL. [82] | NR | NR | Apache-2.0 | https://reagraph.dev/ | Browser component | High-potential polished alternative; not runtime-tested here | Same evidence JSON contract |
| cosmos.gl engine | https://github.com/cosmosgl/graph | GPU-accelerated WebGL force-layout/rendering engine. [89] | 1302 | 2026-10-23 | MIT [84] | https://cosmosgl.github.io/graph/ | Browser GPU component | Excellent large-network spectacle; product UI still yours | Custom React shell + graph metadata |
| Cytoscape.js | https://github.com/cytoscape/cytoscape.js | Graph model, analysis and interactive rendering. [54] | 11228 | 2026-09-30 | MIT [85] | https://js.cytoscape.org/demos/tokyo-railways/ | Browser or analysis component | Best for inspectable paths, filtering and analytical controls | Graph backend + evidence/citation panel |
| vis-network | https://github.com/visjs/vis-network | Dynamic customizable network visualization. [43] | 3631 | 2026-09-25 | Apache-2.0 [86] | Repository/documentation examples | Browser library | Practical and familiar; more visual styling needed | Pyvis / Neovis / custom API |
| Pyvis | https://github.com/WestHealth/pyvis | Python package producing interactive network graphs. [47] | 1211 | 2024-04-24 | BSD-3-Clause [83] | Generated HTML/examples; hosted service NR | Generate HTML on server; embed in app | Fastest Python proof-of-concept; less app-native | NetworkX + FastAPI/Gradio |
| Neovis.js | https://github.com/neo4j-contrib/neovis.js | Neo4j data rendered with vis.js, configurable through Cypher. [88] | NR | NR | Apache-2.0 | API/example documentation | Browser library; use a safe backend rather than exposing credentials | Fast route from Neo4j to visible clusters | Neo4j Builder / Neo4j SDK |
| Graphology | https://github.com/graphology/graphology | JavaScript/TypeScript graph data structure and tooling. [93] | NR | NR | MIT | No standalone user-facing graph app established | Data/algorithm library, not a renderer | No UI itself | Sigma.js + community/path algorithms |
| React Flow / xyflow | https://github.com/xyflow/xyflow | Customizable React/Svelte node-based UI libraries. [44] | NR | NR | MIT | Project examples; live health NR | Browser UI library | Excellent extraction/retrieval pipeline diagrams; not my first force-KG choice | Show the ingestion/router workflow beside the KG |
| React Diagrams | https://github.com/projectstorm/react-diagrams | React/TypeScript flow and process diagramming. [45] | NR | NR | MIT | http://projectstorm.cloud/react-diagrams | Browser UI library | Good architecture/workflow view; not a retrieval engine | Pipeline explainer |
| Markmap | https://github.com/markmap/markmap | Markdown/plain-text mind maps. [5] | NR | NR | MIT | https://markmap.js.org/repl | Browser/static output | Clean topic outline, but not an extracted semantic KG | Community-summary navigation only |
| Graphologue | https://github.com/foundation-interface/graphologue | Turns LLM responses into interactive diagrams in real time. [90] | NR | NR | MIT | https://graphologue.app/ ; requires OpenAI key | Node/web app; documented local setup | Very strong interaction inspiration; diagrams are not proof of grounding | Attach real retrieval evidence before presenting as KG reasoning |

**Takeaway:** Pick **react-force-graph** for a React hackathon, **G6** for a more controlled polished interface, **Sigma.js** for a dense 2D atlas, or **Cytoscape.js** for evidence-path analysis. Those are design recommendations, not a benchmark ranking.

### Case Study: A Beautiful Diagram Can Hide A Missing Evidence Model

Graphologue is compelling because the diagram grows as the LLM response arrives, and the interface invites direct interaction with that emerging structure. Its documented purpose is response-to-diagram generation, not document-grounded community retrieval. That makes it a good source of interaction ideas and a poor shortcut for proving factual provenance. [90]

The adaptation is to animate **retrieved** nodes and relationships first, then stream the explanation against those fixed evidence identifiers. If the model proposes a relationship absent from the retrieved graph, show it as a tentative suggestion rather than quietly inserting it as fact. This preserves the dramatic feeling without pretending the visualization validates the model.

### Source-Available Inspiration Is Not Automatically Permissive Open Source

InfraNodus is a particularly relevant inspiration: it represents text as a word/co-occurrence network, identifies communities and offers API/JSON export. However, its repository explicitly uses a **custom license**. It is not interchangeable with an MIT-licensed semantic entity/triple extractor, and its word network should not be described as the same evidence model. [50]

Its URL is https://github.com/noduslabs/infranodus and hosted product is https://www.infranodus.com/ . Stars and last update are NR here. D1 covers text-to-network rather than verified PDF-to-entity triples; D2 covers communities; D3 documents Neo4j but not the required paired vector store; D4's grounded thematic/local QA is NR; D5 supplies network exploration, not a verified AI-03 answer-linked split screen. Local Node/Neo4j installation is documented, but the cited setup is old; use it as inspiration unless its license and deployment suit your project. [50]

Also distinguish the **MIT cosmos.gl rendering engine** from the complete **Cosmograph product**: this research verifies the engine's license, not blanket open-source rights to every product feature. [89]


## 6. A Small-Server Architecture That Preserves The Evidence

**Recommended build A, balanced:** LightRAG for ingestion/extraction/retrieval, an explicit community-summary job, persistent graph and vector stores if required by the rubric, FastAPI for a normalized answer-evidence response, and react-force-graph for the split screen. LightRAG documents separate graph/vector storage roles and warns that its default stores are in-memory; choose persistence deliberately rather than assuming the defaults satisfy the deployment requirement. [22]

**Recommended build B, graph-first:** Neo4j LLM Graph Builder for upload, extraction and document graph handling; add community reports, a thematic/local router and a custom answer-evidence viewer. **Recommended build C, methodology-first:** nano-graphrag or Microsoft GraphRAG plus GraphRAG Visualizer and a document-ingestion API. These combinations are proposed architectures, not pretested integrations. [8][19][14]

| Layer | Proposed Implementation | What The Demo Must Expose | Small-Server Decision |
|---|---|---|---|
| Upload/parsing | PDF parser, optional OCR; store original pages | Document status, page numbers and parse failures | Keep OCR/indexing asynchronous |
| Extraction | Entities + typed relationships + mention provenance | Raw chunk beside extracted triples | Cache results and preserve original text |
| Communities | Graph community assignment plus summaries | Topic label, members and evidence documents | Recompute outside the chat request |
| Storage | Graph DB and vector DB, if literally required | Shared chunk/entity/document IDs | Keep services minimal; use hosted APIs where appropriate |
| Query router | Explicit thematic/local/mixed decision | A short "Why this route?" explanation | Begin deterministic; add model routing only if useful |
| Retrieval | Community reports or local graph/vector evidence | Retrieved chunks, communities, nodes and edges | Bound neighborhood expansion and payload size |
| Generation | Answer restricted to returned evidence | Claim-level source links; uncertainty/abstention | External LLM API avoids local inference hardware |
| Graph view | Stable overview plus answer-focused subgraph | Zoom, highlight, document links and path inspection | Render selected evidence, not every edge at once |

**Takeaway:** External model APIs reduce local inference requirements; they do not remove PDF parsing, indexing, database or browser-rendering work. No universal minimum RAM or dollar-cost promise is justified by the collected evidence.

The answer endpoint should return a contract like this. It is a proposed design, not a claim about any repository's existing response schema:

```json
{
  "answer": "...",
  "route": "thematic",
  "route_reason": "The question asks about patterns across documents",
  "community_ids": ["community-a"],
  "node_ids": ["entity-a", "entity-b"],
  "edge_ids": ["relation-a"],
  "evidence_paths": [["entity-a", "relation-a", "entity-b"]],
  "citations": [
    {"document_id": "doc-a", "chunk_id": "chunk-a", "page": 1}
  ],
  "unsupported_claims": []
}
```

### Case Study: FalkorDB Exposes The Primitive Your Frontend Needs

FalkorDB's SDK documents `MENTIONED_IN` edges connecting entities to source chunks and a `return_context=True` option that returns retrieval context. It also documents graph, vector and full-text retrieval steps. Those details matter more for AI-03 than a generic claim of "explainability": the frontend needs identifiers and evidence objects it can actually select. [16]

I would translate that context into the contract above, not let the UI guess which graph nodes match the answer text. Apply the same adapter pattern to whichever backend you choose. The repository's accuracy and "benchmark-leading" language remains the author's positioning; this report does not establish a cross-system performance winner. [16]

### Adjacent Temporal Memory And An Unmaintained Accelerator

**Graphiti** is a useful optional complement if the story includes changing facts. It tracks temporal context, source provenance and incremental updates; it has an Apache-2.0 license and a FastAPI API service. It is not, from the verified material, a turnkey PDF/community/split-screen application. URL: https://github.com/getzep/graphiti . Stars and current last push: NR; public demo: NR; self-hosting/API: documented; UI quality: backend-only in this evaluation; combine-with: your chosen document pipeline plus a time-aware evidence viewer. D1 PDF ingestion NR, D2 community reporting NR, D3 graph plus hybrid/semantic retrieval documented, D4 temporal retrieval but the requested thematic/local router NR, D5 finished UI NR. [100]

**Azure GraphRAG Accelerator** exposes GraphRAG through Azure-hosted API endpoints, but its repository says it is **no longer maintained**. URL: https://github.com/Azure-Samples/graphrag-accelerator . Stars, current last push and license were not recovered here; hosted public demo NR; deployment is Azure-oriented rather than my small-server first choice; visual quality NR; combine-with GraphRAG Visualizer only if you accept maintaining the integration. D1-D4 depend on the underlying GraphRAG pipeline; D5 is not a verified finished application. [73]


## 7. Demos Judges Remember: Make Every Visual Change Explain Something

I found useful **shareable-demo references**, but not enough comparable view/share data to label a ranked set "viral." The recommendations below concern visual storytelling and evidence, not verified social-media reach.

| Reference | Verified Behavior / Status | What To Borrow | What Not To Claim |
|---|---|---|---|
| Neo4j GraphRAG / Emil Eifrem talk | Shows the builder and document/chunk/concept graph; the live demonstration initially struggles with connectivity/rendering. [71] | Turn a familiar document into a visibly navigable structure | A frictionless live demo or measured virality |
| Graphologue | LLM responses become interactive diagrams in real time. [90] | Progressive reveal and direct interaction | That a generated diagram is retrieved evidence |
| GraphRAG Visualizer | Public viewer, 2D/3D graphs, node/relationship search and GraphRAG artifacts. [14] | Community drill-down and a credible graph explorer | That artifact upload is PDF ingestion |
| InfraNodus | Text networks, communities and top-node analysis; custom license. [50] | Legible clusters and a topic-first overview | Permissive reuse or equivalent entity semantics |
| GraphRAG WorkBench write-up | A **2025-12-23** secondary article describes 3D graphs, PDFs, communities and several search modes. [69] | A useful visual product checklist | A source-verified reusable repository; original code/license not established here |
| Transcend hackathon winner | Winner announcement describes OWL/SPARQL/RDF reasoning connecting code classes to papers and authors. [68] | A concrete question answered through an unexpected evidence bridge | A verified downloadable AI-03 implementation; code/license/server details remain NR |

**Takeaway:** The memorable moment is not "there are many dots." It is "the system found a connection across my documents, and I can inspect exactly why."

### Case Study: Transcend Wins Attention Through A Concrete Evidence Bridge

The hackathon announcement identifies **Transcend** as a winner and describes its second reasoning engine using the semantic web stack, including **OWL, SPARQL and RDF**. Its example asks which knowledge-graph-embedding methods a codebase implements and returns class names plus the papers and authors behind them. The announcement is dated **July 13, 2026**; this is a documented award precedent, not a claim that the project matches every AI-03 deliverable. [68]

The transferable lesson is specificity. For your demo, choose a question whose answer must cross two or more documents, then animate the exact bridge between the source entities and passages. A useful example scenario is "Which projects depend on the same risky supplier, and which documents establish each dependency?" This is a proposed demonstration question, not an observed Transcend capability.

### Hosted Hugging Face Spaces: Existence Is Verified, Liveness Is Not

The following exact Spaces exist. For all five, deployment code/license, last update and small-server capacity are **NR in the inspected evidence**; GitHub-style stars are **not applicable**. Because the inspected applications were failing, their five-deliverable coverage and actual UI quality are **not established**, rather than inferred from their names. Combine-with recommendation: use a Space only as a recoverable reference or fork after inspecting its files, not as the live dependency of your judged demo.

| Space | URL | Plain-Words Identification | Observed Hosted Status | D1 | D2 | D3 | D4 | D5 |
|---|---|---|---|---|---|---|---|---|
| Harry Potter GraphRAG Chat | https://huggingface.co/spaces/roeyzalta/harry-potter-graphrag-chat | Named GraphRAG chat demo | Runtime error. [81] | NR | NR | NR | NR | NR |
| GraphRag_upload | https://huggingface.co/spaces/ItsukiOvO/GraphRag_upload | Named upload demo | Runtime error. [78] | NR | NR | NR | NR | NR |
| ML6 Knowledge-graphs | https://huggingface.co/spaces/ml6team/Knowledge-graphs | Knowledge-graph demo; **55 likes** visible, not stars | Build error. [77] | NR | NR | NR | NR | NR |
| awacke1 Knowledge-graphs | https://huggingface.co/spaces/awacke1/Knowledge-graphs | Another knowledge-graph Space | Build error. [80] | NR | NR | NR | NR | NR |
| Duema GraphRAG QA Search | https://huggingface.co/spaces/watagassy/Duema-GraphRAG-QA-Search | Named QA/search demo | Runtime error; launch timeout reported. [79] | NR | NR | NR | NR | NR |

**Takeaway:** Keep a local, pre-indexed demonstration and a short recorded fallback. A hosted URL alone is not a reliability plan.

### A Proposed Demo Sequence With A Clear Payoff

Start with a small set of readable, related documents, not a gigantic unexplained graph. Upload one additional document live; show parsing, extracted triples and the new document's contribution to existing communities. Keep the camera stable and use a short, deliberate highlight animation instead of constant force-layout motion.

Ask a broad question first: "What are the main themes?" The graph should emphasize labeled communities and the chat should say **thematic retrieval**. Then ask a specific factual question, switch visibly to **local retrieval**, dim unrelated material and illuminate the exact relationship path. Finally, click a highlighted edge and open the supporting page passage. These are proposed interactions; they are not asserted to exist unchanged in the cataloged projects.

The visual grammar should be consistent: color for topic, shape for entity/document/chunk, line style for relationship type, and an explicit marker for uncertain or contradictory assertions. Do not imply that node size measures confidence unless the system actually computes a defensible confidence value.

### Ten "What If" Questions A Non-Expert Judge Will Ask

| # | Judge's Question | How The Proposed Demo Answers It | What The Screen Proves |
|---|---|---|---|
| 1 | **What if I upload my own PDF instead of your prepared files?** | Accept the upload, show parsing progress and its extracted triples; visibly mark its new nodes and document links | It is an ingestion system, not only a prebuilt graph |
| 2 | **What if I ask what all the documents are about?** | Select thematic retrieval; highlight labeled communities and show their supporting documents | Themes come from a community layer, not merely top similar chunks |
| 3 | **What if I ask one precise factual question?** | Select local retrieval, focus the relevant entities and show the shortest useful evidence path | Broad and factual questions use different evidence selection |
| 4 | **What if the answer is wrong?** | Let the judge click each claim's citation and inspect the original page/chunk beside the extracted relationship | The answer can be challenged against source material |
| 5 | **What if two documents disagree?** | Display both assertions with separate sources and, when present, dates; answer with the disagreement rather than silently merging it | Conflicting evidence remains visible |
| 6 | **What if one person or company has several names?** | Show an alias/entity-resolution inspector, including merged mentions and a reversible correction | Entity merging is inspectable rather than magical |
| 7 | **What if the information is not in any uploaded document?** | Abstain, show no supporting evidence path and offer a narrower query; keep external knowledge off or clearly separated | Grounding includes refusing unsupported answers |
| 8 | **What if I delete a document or add a newer version?** | Remove or version its chunks/assertions, update affected communities and show which answers/evidence change | Provenance drives lifecycle changes, not only display |
| 9 | **What if I do not understand the graph?** | Offer "show only this answer," community labels, plain-language edge descriptions and a document-first view | The interface explains rather than overwhelms |
| 10 | **What if I click a node and ask a follow-up?** | Scope the next query to the selected node/community; retain the visible path and open the new evidence | Graph exploration and chat are genuinely connected |

**Takeaway:** Rehearse these as observable behaviors. Do not promise contradiction handling, entity corrections or incremental deletion merely because your chosen backend contains a graph.


## Synthesis

The landscape separates into three different products that are often called the same thing: **a retrieval method**, **a document-knowledge application**, and **an interactive graph surface**. AI-03 needs all three joined through a shared evidence model. The most useful combination is therefore not necessarily the most popular single repository.

| Strategy / Major Candidates | Mechanism | Scope | Deployment Trade-Off | Evidence Strength / Main Risk | Best Decision |
|---|---|---|---|---|---|
| Microsoft GraphRAG / nano-graphrag / RAGU | Community summaries plus local graph/context retrieval | Closest thematic/local methodological fit | Build or integrate the application layer; indexing work is material | Method documented; final UI remains yours | Choose when community-level questions dominate. [75][19][52] |
| LightRAG / RAG-Anything / MiniRAG | Lightweight graph/vector retrieval; optional multimodal or small-model emphasis | Broad ingestion/retrieval building blocks | Convenient application/API path in LightRAG; verify persistence and exact thematic semantics | Strong component coverage, not proof of the exact requested UI | Best balanced hackathon foundation. [22][23][70] |
| Neo4j Builder / Neo4j SDK / FalkorDB SDK | Explicit graph construction and source-connected graph retrieval | Natural graph persistence and inspectability | Database setup and graph-schema choices; separate vector DB may still be a rubric choice | Good path/provenance primitives; community reporting may require additions | Choose when visible relationships and source traversal dominate. [8][21][16] |
| KAG / HippoRAG / fast-graphrag | Logical reasoning, associative memory or Personalized PageRank | Stronger specialized reasoning/retrieval focus | More work on document UX and the synchronized frontend | A reasoning method is not automatically a thematic product | Borrow the mechanism only if it solves a demonstrated question. [9][12][20] |
| Kotaemon / RAGFlow / R2R | Document management, parsing, retrieval and citation workflows | Broad product plumbing | More dependencies; some stacks are heavier | Citation UI may be stronger than graph synchronization | Choose when robust document UX is the bottleneck. [13][18][4] |
| WeKnora / Yuxi / ApeRAG / HuixiangDou | Regional full-stack knowledge and agent platforms | Multilingual/product-oriented alternatives | Inspect service count and distinguish page graphs from entity graphs | Strong real candidates; exact D2/D5 behavior varies | Evaluate alongside English-first apps, not after them. [30][31][27][29] |
| Vector Graph RAG | Entities/relations represented through vector retrieval | Backend plus a React/FastAPI graph surface | Can remove the graph database | May conflict with literal dual-database requirement | Use only with a clear storage-compliance story. [99] |
| react-force-graph / G6 / Sigma / Cytoscape / cosmos.gl | Interaction, layout and rendering | D5 primitives, not D1-D4 | Browser complexity replaces backend complexity | Visual beauty can mask missing provenance | Select one renderer; invest in the evidence adapter. [55][53][46][54][89] |

**Takeaway:** The non-obvious tension is that the best-looking graph can be the least faithful explanation, while the most faithful community-retrieval engine can have almost no user interface. Resolve that tension by treating the graph as a view of retrieved evidence, not as an independent illustration generated after the answer.

**My final choice:** LightRAG plus a custom answer-evidence API and react-force-graph, with explicit community summaries and persistent graph/vector backends. If preserving an existing graph-first application saves more time for your team, choose Neo4j LLM Graph Builder instead. In either case, make the judged innovation the same: **one question, one visible retrieval route, one inspectable evidence subgraph, and one click back to the original document**.

## References

1. *GitHub - microsoft/graphrag: A modular graph-based Retrieval-Augmented Generation (RAG) system · GitHub*. https://github.com/microsoft/graphrag
2. *GitHub - mudler/LocalAGI: LocalAGI is a powerful, self-hostable AI Agent platform designed for maximum privacy and flexibility. A complete drop-in replacement for OpenAI's Responses APIs with advanced agentic capabilities. No clouds.  Local AI that works on consumer-grade hardware (CPU and GPU). · GitHub*. https://github.com/mudler/LocalAGI
3. *GitHub - Dicklesworthstone/llm_aided_ocr: Enhances Tesseract OCR output using LLMs (local or API) for error correction, smart chunking, and markdown formatting of scanned PDFs · GitHub*. https://github.com/Dicklesworthstone/llm_aided_ocr
4. *GitHub - SciPhi-AI/R2R: SoTA production-ready AI retrieval system. Agentic Retrieval-Augmented Generation (RAG) with a RESTful API. · GitHub*. https://github.com/SciPhi-AI/R2R
5. *GitHub - markmap/markmap: Build mindmaps with plain text · GitHub*. https://github.com/markmap/markmap
6. *GitHub - severian42/GraphRAG-Local-UI: GraphRAG using Local LLMs - Features robust API and multiple apps for Indexing/Prompt Tuning/Query/Chat/Visualizing/Etc. This is meant to be the ultimate GraphRAG/KG local LLM app. · GitHub*. https://github.com/severian42/GraphRAG-Local-UI
7. *GitHub - NavigatingCancer/GraphRAG-Local-UI-NC: NC fork of GraphRag-Local-UI -- GraphRAG using Local LLMs - Features robust API and multiple apps for Indexing/Prompt Tuning/Query/Chat/Visualizing/Etc. This is meant to be the ultimate GraphRAG/KG local LLM app. · GitHub*. https://github.com/NavigatingCancer/GraphRAG-Local-UI-NC
8. *GitHub - neo4j-labs/llm-graph-builder: Neo4j graph construction from unstructured data using LLMs · GitHub*. https://github.com/neo4j-labs/llm-graph-builder
9. *GitHub - OpenSPG/KAG: KAG is a logical form-guided reasoning and retrieval framework based on OpenSPG engine and LLMs.  It is used to build logical reasoning and factual Q&A solutions for professional domain knowledge bases. It can effectively overcome the shortcomings of the traditional RAG vector similarity calculation model. · GitHub*. https://github.com/OpenSPG/KAG
10. *GitHub - RUC-NLPIR/FlashRAG: ⚡FlashRAG: A Python Toolkit for Efficient RAG Research (WWW2025 Resource) · GitHub*. https://github.com/RUC-NLPIR/FlashRAG
11. *GitHub - rahulnyk/knowledge_graph: Convert any text to a graph of knowledge. This can be used for Graph Augmented Generation or Knowledge Graph based QnA · GitHub*. https://github.com/rahulnyk/knowledge_graph
12. [GitHub - OSU-NLP-Group/HippoRAG: [NeurIPS'24] HippoRAG is a novel RAG framework inspired by human long-term memory that enables LLMs to continuously integrate knowledge across external documents. RAG + Knowledge Graphs + Personalized PageRank. · GitHub](https://github.com/OSU-NLP-Group/HippoRAG)
13. *GitHub - Cinnamon/kotaemon: An open-source RAG-based tool for chatting with your documents. · GitHub*. https://github.com/Cinnamon/kotaemon
14. *GitHub - noworneverev/graphrag-visualizer: A web-based tool for visualizing and exploring artifacts from Microsoft's GraphRAG. · GitHub*. https://github.com/noworneverev/graphrag-visualizer
15. *GitHub - vitali87/code-graph-rag: The ultimate RAG for your monorepo. Query, understand, and edit multi-language codebases with the power of AI and knowledge graphs · GitHub*. https://github.com/vitali87/code-graph-rag
16. *GitHub - FalkorDB/GraphRAG-SDK: Build fast and accurate GenAI apps with GraphRAG SDK at scale  🌟 · GitHub*. https://github.com/FalkorDB/GraphRAG-SDK
17. *GitHub - SapienzaNLP/relik: Retrieve, Read and LinK: Fast and Accurate Entity Linking and Relation Extraction on an Academic Budget (ACL 2024) · GitHub*. https://github.com/SapienzaNLP/relik
18. *GitHub - infiniflow/ragflow: RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent capabilities to create a superior context layer for LLMs · GitHub*. https://github.com/infiniflow/ragflow
19. *GitHub - gusye1234/nano-graphrag: A simple, easy-to-hack GraphRAG implementation · GitHub*. https://github.com/gusye1234/nano-graphrag
20. *GitHub - circlemind-ai/fast-graphrag: RAG that intelligently adapts to your use case, data, and queries · GitHub*. https://github.com/circlemind-ai/fast-graphrag
21. *GitHub - neo4j/neo4j-graphrag-python: Neo4j GraphRAG for Python · GitHub*. https://github.com/neo4j/neo4j-graphrag-python
22. [GitHub - HKUDS/LightRAG: [EMNLP2025] LightRAG: Simple and Fast Retrieval-Augmented Generation · GitHub](https://github.com/HKUDS/LightRAG)
23. *GitHub - HKUDS/RAG-Anything: "RAG-Anything: All-in-One RAG Framework" · GitHub*. https://github.com/HKUDS/RAG-Anything
24. *api.github.com*. https://api.github.com/repos/HKUDS/LightRAG
25. *api.github.com*. https://api.github.com/repos/microsoft/graphrag
26. *Llm Graph Builder*. https://api.github.com/repos/neo4j-labs/llm-graph-builder
27. *GitHub - apecloud/ApeRAG: ApeRAG: Production-ready GraphRAG with multi-modal indexing, AI agents, MCP support, and scalable K8s deployment · GitHub*. https://github.com/apecloud/ApeRAG
28. *GitHub - netease-youdao/QAnything: Question and Answer based on Anything. · GitHub*. https://github.com/netease-youdao/QAnything
29. *GitHub - InternLM/HuixiangDou: HuixiangDou: Overcoming Group Chat Scenarios with LLM-based Technical Assistance · GitHub*. https://github.com/InternLM/HuixiangDou
30. *GitHub - Tencent/WeKnora: Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki. · GitHub*. https://github.com/Tencent/WeKnora
31. *GitHub - xerrors/Yuxi: 结合知识库、知识图谱管理的 多租户 Agent Harness 平台。 An agent harness that integrates a LightRAG knowledge base and knowledge graphs. Build with LangChain + Vue + FastAPI, support DeepAgents、MinerU PDF、Neo4j 、MCP. · GitHub*. https://github.com/xerrors/Yuxi-Know
32. *Graphrag Visualizer*. https://api.github.com/repos/noworneverev/graphrag-visualizer
33. *api.github.com*. https://api.github.com/repos/infiniflow/ragflow
34. *api.github.com*. https://api.github.com/repos/Cinnamon/kotaemon
35. *Fast Graphrag*. https://api.github.com/repos/circlemind-ai/fast-graphrag
36. *Neo4J Graphrag Python*. https://api.github.com/repos/neo4j/neo4j-graphrag-python
37. *Nano Graphrag*. https://api.github.com/repos/gusye1234/nano-graphrag
38. *Osu Nlp Group*. https://api.github.com/repos/OSU-NLP-Group/HippoRAG
39. *api.github.com*. https://api.github.com/repos/OpenSPG/KAG
40. *Graphrag Local Ui*. https://api.github.com/repos/severian42/GraphRAG-Local-UI
41. *Graphrag Local Ui Nc*. https://api.github.com/repos/NavigatingCancer/GraphRAG-Local-UI-NC
42. *GitHub - antvis/Graphin: 🌌 A React toolkit for graph visualization based on G6. · GitHub*. https://github.com/antvis/Graphin
43. *GitHub - visjs/vis-network: :dizzy: Display dynamic, automatically organised, customizable network views. · GitHub*. https://github.com/visjs/vis-network
44. *GitHub - xyflow/xyflow: React Flow | Svelte Flow - Powerful open source libraries for building node-based UIs with React (https://reactflow.dev) or Svelte (https://svelteflow.dev). Ready out-of-the-box and infinitely customizable. · GitHub*. https://github.com/xyflow/xyflow
45. *GitHub - projectstorm/react-diagrams: a super simple, no-nonsense diagramming library written in react that just works · GitHub*. https://github.com/projectstorm/react-diagrams
46. *GitHub - jacomyal/sigma.js: A JavaScript library aimed at visualizing graphs of thousands of nodes and edges · GitHub*. https://github.com/jacomyal/sigma.js
47. *GitHub - WestHealth/pyvis: Python package for creating and visualizing interactive network graphs. · GitHub*. https://github.com/WestHealth/pyvis
48. *GitHub - kanerika-ai/graphrag-enterprise-starter: Comparing standard RAG and GraphRAG · GitHub*. https://github.com/kanerika-ai/graphrag-enterprise-starter
49. *GitHub - vasturiano/3d-force-graph: 3D force-directed graph component using ThreeJS/WebGL · GitHub*. https://github.com/vasturiano/3d-force-graph
50. *GitHub - noduslabs/infranodus: A Node.Js / Neo4J tool that translates words and relations into network graphs and shows you how it all connects. · GitHub*. https://github.com/noduslabs/infranodus
51. *GitHub - Neurons-AI/knowledge-graph-skill: Knowledge Graph Agent Skill · GitHub*. https://github.com/Neurons-AI/knowledge-graph-skill
52. *GitHub - RaguTeam/RAGU: Modular GraphRAG framework · GitHub*. https://github.com/RaguTeam/RAGU
53. *GitHub - antvis/G6: ♾ A Graph Visualization Framework in JavaScript. · GitHub*. https://github.com/antvis/G6
54. *GitHub - cytoscape/cytoscape.js: Graph theory (network) library for visualisation and analysis · GitHub*. https://github.com/cytoscape/cytoscape.js
55. *GitHub - vasturiano/react-force-graph: React component for 2D, 3D, VR and AR force directed graphs · GitHub*. https://github.com/vasturiano/react-force-graph
56. *GitHub - Rani8982/graphrag-vs-vectorrag: Interactive benchmark comparing Vector RAG, Graph RAG, and a hybrid router — with a live UI showing how text becomes entities/relationships (knowledge graph) vs. TF-IDF vectors, plus a side-by-side look at how graph traversal replaces multi-hop SQL joins. · GitHub*. https://github.com/Rani8982/graphrag-vs-vectorrag
57. *api.github.com*. https://api.github.com/repos/RaguTeam/RAGU
58. *api.github.com*. https://api.github.com/repos/HKUDS/MiniRAG
59. *Rag Anything*. https://api.github.com/repos/HKUDS/RAG-Anything
60. *Yuxi Know*. https://api.github.com/repos/xerrors/Yuxi-Know
61. *api.github.com*. https://api.github.com/repos/apecloud/ApeRAG
62. *Graphrag Sdk*. https://api.github.com/repos/FalkorDB/GraphRAG-SDK
63. *api.github.com*. https://api.github.com/repos/Tencent/WeKnora
64. *api.github.com*. https://api.github.com/repos/InternLM/HuixiangDou
65. *Knowledge Graph*. https://api.github.com/repos/rahulnyk/knowledge_graph
66. *Sciphi Ai*. https://api.github.com/repos/SciPhi-AI/R2R
67. *Local Search - GraphRAG*. https://microsoft.github.io/graphrag/query/local_search/
68. *Transcend Hackathon Winners announcement: how the community used GitLab Orbit to solve real problems - Community - GitLab Forum*. https://forum.gitlab.com/t/transcend-hackathon-winners-announcement-how-the-community-used-gitlab-orbit-to-solve-real-problems/134491
69. *GraphRAG WorkBench:Microsoft GraphRAG 生成的交互式 3D 可视化知识图谱*. https://www.53ai.com/news/knowledgegraph/2025122395273.html
70. [GitHub - HKUDS/MiniRAG: [ACL2026] "MiniRAG: Making RAG Simpler with Small and Open-Sourced Language Models" · GitHub](https://github.com/HKUDS/MiniRAG)
71. *GraphRAG: The Marriage of Knowledge Graphs and RAG: Emil Eifrem | AI Engineer*. https://ai.engineer/talks/graphrag
72. *Methods - GraphRAG*. https://microsoft.github.io/graphrag/index/methods/
73. *GitHub - Azure-Samples/graphrag-accelerator: One-click deploy of a Knowledge Graph powered RAG (GraphRAG) in Azure · GitHub*. https://github.com/Azure-Samples/graphrag-accelerator
74. *DRIFT Search - GraphRAG*. https://microsoft.github.io/graphrag/query/drift_search/
75. *Global Search - GraphRAG*. https://microsoft.github.io/graphrag/query/global_search/
76. *知识图谱 · WeKnora 文档*. https://weknora.weixin.qq.com/docs/03-features/09-knowledge-graph
77. *RE:Belle - a Hugging Face Space by ml6team*. https://huggingface.co/spaces/ml6team/Knowledge-graphs
78. *GraphRag Upload - a Hugging Face Space by ItsukiOvO*. https://huggingface.co/spaces/ItsukiOvO/GraphRag_upload
79. *Duema GraphRAG QA Search - a Hugging Face Space by watagassy*. https://huggingface.co/spaces/watagassy/Duema-GraphRAG-QA-Search
80. *RE:Belle - a Hugging Face Space by awacke1*. https://huggingface.co/spaces/awacke1/Knowledge-graphs
81. *Harry Potter Graphrag Chat - a Hugging Face Space by roeyzalta*. https://huggingface.co/spaces/roeyzalta/harry-potter-graphrag-chat
82. *GitHub - reaviz/reagraph: 🕸 WebGL Graph Visualizations for React. Maintained by @goodcodeus. · GitHub*. https://github.com/reaviz/reagraph
83. *api.github.com*. https://api.github.com/repos/WestHealth/pyvis
84. *Cosmograph Org*. https://api.github.com/repos/cosmograph-org/cosmos
85. *api.github.com*. https://api.github.com/repos/cytoscape/cytoscape.js
86. *Vis Network*. https://api.github.com/repos/visjs/vis-network
87. *GitHub - awslabs/graphrag-toolkit: Python toolkit for building graph-enhanced GenAI applications · GitHub*. https://github.com/awslabs/graphrag-toolkit
88. *GitHub - neo4j-contrib/neovis.js: Neo4j + vis.js = neovis.js. Graph visualizations in the browser with data from Neo4j. · GitHub*. https://github.com/neo4j-contrib/neovis.js
89. *GitHub - cosmosgl/graph: GPU-accelerated force graph layout and rendering · GitHub*. https://github.com/cosmograph-org/cosmos
90. *GitHub - foundation-interface/graphologue: Use LLM to stream diagrams, instead of tokens, in real-time! (UIST 2023 Paper) · GitHub*. https://github.com/ucsd-creativitylab/graphologue
91. *GitHub - 666ghj/MiroFish: A Simple and Universal Swarm Intelligence Engine, Predicting Anything. 简洁通用的群体智能引擎，预测万物 · GitHub*. https://github.com/666ghj/MiroFish
92. *GitHub - JayLZhou/GraphRAG: In-depth study of the graphrag · GitHub*. https://github.com/JayLZhou/GraphRAG
93. *GitHub - graphology/graphology: A robust & multipurpose Graph object for JavaScript & TypeScript. · GitHub*. https://github.com/graphology/graphology
94. *3D Force Graph*. https://api.github.com/repos/vasturiano/3d-force-graph
95. *api.github.com*. https://api.github.com/repos/antvis/Graphin
96. *api.github.com*. https://api.github.com/repos/antvis/G6
97. *React Force Graph*. https://api.github.com/repos/vasturiano/react-force-graph
98. *api.github.com*. https://api.github.com/repos/jacomyal/sigma.js
99. *GitHub - zilliztech/vector-graph-rag: Graph RAG with pure vector search, achieving SOTA performance in multi-hop reasoning scenarios. · GitHub*. https://github.com/zilliztech/vector-graph-rag
100. *GitHub - getzep/graphiti: Build Real-Time Knowledge Graphs for AI Agents · GitHub*. https://github.com/getzep/graphiti
