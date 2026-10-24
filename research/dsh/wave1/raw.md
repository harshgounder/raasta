# Task Group Results

**Task Group ID:** tgrp_85133678a4ff429386c65a9af82acad2
**Status:** ✅ Complete
**Total Runs:** 8
**Running:** 0
**Completed:** 8
**Failed:** 0
**Created:** 2026-10-24T08:50:14.153535Z

**Metadata:**
- **created_at:** "2026-10-24T08:50:13.980Z"
- **processor:** "pro"
- **created_via:** "task-mcp"
- **inputs_count:** 8
- **output_type:** "json"

## Results

**Legend:**
- Status: ✅ Completed | ❌ Failed | 🟡 Running/Queued
- Confidence: 🟢 High | 🟡 Medium | 🔴 Low
- ⚠️ = Has warnings | 🚨 = Has errors

| Index | Status | Statement | Id | Best_fork_candidates | Models_weights | Mind_boggling_demo_angles | Sources | Risks | Missing_pieces | Regional_sources_checked | Datasets |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | ✅ completed | Voice-clone detection for phone scams: decide if a 2-10 second speech clip is genuine or synthetic, generalising to unseen voice-cloning tools. Tests: ASVspoof 2019, In-the-Wild. Pretrained self-supervised speech models allowed. | 🟢 AI-01 | 🟡 [<br>  {<br>    "browser_demo_feasible": "partial — feasible as a browser interface backed by Python inference; browser-native execution is not verified.",<br>    "last_update": "2026-10-19",<br>    "what_it_does": "AASIST detects spoofed speech using integrated spectro-temporal graph attention. Its official implementation includes pretrained AASIST and lightweight AASIST-L models evaluated on ASVspoof 2019 Logical Access.",<br>    "what_to_fork": "Best starting point for a lightweight demo: fork models/, the AASIST-L configuration and checkpoint, and data_utils.py. Build a single-clip CPU inference wrapper, bypass the GPU-only guard in main.py, and add browser recording/upload; explicitly handle the existing approximately four-second crop/repeat preprocessing.",<br>    "url": "https://github.com/clovaai/aasist",<br>    "stars": "308",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "AASIST"<br>  },<br>  {<br>    "browser_demo_feasible": "partial — feasible through a Python backend; the large SSL frontend is not a verified browser-native deployment.",<br>    "last_update": "2026-10-18",<br>    "what_it_does": "Combines pretrained wav2vec 2.0 features, an AASIST-style classifier, and RawBoost augmentation for speech anti-spoofing. The published experiments train on ASVspoof 2019 LA and evaluate on ASVspoof 2021 LA and DF; this does not establish performance on unseen phone-scam cloning tools.",<br>    "what_to_fork": "Fork model.py, data_utils_SSL.py, and the inference portion of main_SSL_DF.py, using the linked pretrained checkpoint. Add single-clip input, simplify device/DataParallel handling for CPU deployment, and expose it through a browser upload interface; use it as the heavier comparison model rather than the first client-side target.",<br>    "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",<br>    "stars": "184",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "SSL_Anti-spoofing"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "MIT (repository license; no separate weight-specific terms identified)",<br>    "runs_on_cpu_or_browser": "CPU with an adapted inference wrapper; not execution-tested here. Browser-native support unverified.",<br>    "size": "416 KB",<br>    "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST-L.pth",<br>    "name": "AASIST-L pretrained checkpoint"<br>  },<br>  {<br>    "license": "MIT (repository license; no separate weight-specific terms identified)",<br>    "runs_on_cpu_or_browser": "CPU with an adapted inference wrapper; not execution-tested here. Browser-native support unverified.",<br>    "size": "1.22 MB",<br>    "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST.pth",<br>    "name": "AASIST pretrained checkpoint"<br>  },<br>  {<br>    "license": "unknown",<br>    "runs_on_cpu_or_browser": "CPU path exists in the inference script; memory, compatibility and latency require testing. Browser-native support unverified.",<br>    "size": "1.18 GB",<br>    "url": "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",<br>    "name": "SSL anti-spoofing Best_LA_model_for_DF.pth"<br>  }<br>] | 🟡 [<br>  "Human versus detector: a browser plays consented genuine and cloned 2–10 second clips and asks the judge to guess before revealing the detector score. A Python backend runs AASIST-L and optionally the SSL model; present scores as evidence, not proof of authenticity.",<br>  "Phone-line stress test: browser audio controls add bandwidth restriction and noise to the same clip, then send each version to the inference backend. Display where the verdict changes, making robustness—or its failure—immediately visible.",<br>  "Unknown-cloner showdown: the browser reveals results on held-out cloning tools and In-the-Wild examples while a duration slider reduces available speech from ten seconds to two. Backend evaluation compares both detectors against fixed thresholds and displays an uncertain outcome when evidence is insufficient; this is a proposed evaluation feature, not an existing demonstrated capability."<br>] | 🟢 [<br>  "https://github.com/clovaai/aasist",<br>  "https://api.github.com/repos/clovaai/aasist",<br>  "https://github.com/clovaai/aasist/blob/main/main.py",<br>  "https://github.com/clovaai/aasist/blob/main/models/AASIST.py",<br>  "https://github.com/clovaai/aasist/blob/main/data_utils.py",<br>  "https://github.com/clovaai/aasist/blob/main/NOTICE",<br>  "https://github.com/clovaai/aasist/tree/main/models/weights",<br>  "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST-L.pth",<br>  "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST.pth",<br>  "https://github.com/TakHemlata/SSL_Anti-spoofing",<br>  "https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing",<br>  "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/model.py",<br>  "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",<br>  "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/data_utils_SSL.py",<br>  "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",<br>  "https://www.asvspoof.org/index2019.html",<br>  "https://datashare.ed.ac.uk/handle/10283/3336",<br>  "https://doi.org/10.7488/ds/2555",<br>  "https://deepfake-total.com/in_the_wild",<br>  "https://huggingface.co/datasets/mueller91/In-The-Wild",<br>  "https://www.modelscope.cn/datasets"<br>] | 🟡 [<br>  "Generalization and false reassurance: ASVspoof performance does not establish reliability on unseen cloning tools, two-second excerpts or telephone channels. ASVspoof 2019 explicitly lacks telephone/mobile codecs; synthetic speech is also not synonymous with a scam, and a genuine voice does not establish a legitimate caller.",<br>  "Deployment and privacy: the supplied evaluators are not turnkey browser applications, AASIST's main script rejects CPU execution, and the SSL checkpoint is 1.18 GB. Measure CPU latency and memory before promising responsiveness, and avoid retaining sensitive uploaded conversations.",<br>  "Licensing uncertainty: the repositories are MIT-licensed, but separate terms for externally hosted SSL weights were not established and the ASVspoof dataset license was not recovered. In-the-Wild has conflicting declarations: Apache-2.0 on the project page versus CC-BY-SA-4.0 on Hugging Face; resolve these before redistribution or commercial use."<br>] | 🟡 [<br>  "For the shortlisted repositories, a polished recording/upload interface and a tested single-clip CPU service still need to be built; the supplied entry points primarily evaluate dataset files.",<br>  "No verified browser-native checkpoint/runtime was established for these candidates. Fully local execution would require export, operator-compatibility checks and browser performance testing rather than merely loading the PyTorch checkpoint.",<br>  "A reproducible short-clip, unseen-generator evaluation and calibrated decision policy are missing: test 2–10 second excerpts on ASVspoof 2019 LA and In-the-Wild, add held-out cloning tools and telephone-channel transformations, and avoid silently treating repeated two-second audio as four seconds of independent evidence."<br>] | 🟡 [<br>  "ModelScope — examined its dataset catalogue; no relevant downloadable voice-clone detector was verified there."<br>] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown",<br>    "size": "7.12 GB (LA.zip)",<br>    "url": "https://datashare.ed.ac.uk/handle/10283/3336",<br>    "name": "ASVspoof 2019 — Logical Access"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown — conflicting Apache-2.0 and CC-BY-SA-4.0 declarations",<br>    "size": "37.9 hours according to the Hugging Face card; 58 celebrities and politicians",<br>    "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",<br>    "name": "In-the-Wild"<br>  }<br>] |
| 1 | ✅ completed | Data-analyst agent on messy databases: plain-English questions to SQL, executes, validates results, says when it cannot answer. Scored on BIRD. Open-weight models of 8B parameters or fewer only. | 🟢 AI-02 | 🟡 [<br>  {<br>    "browser_demo_feasible": "yes — browser interface with a local inference/database backend; not browser-only execution",<br>    "last_update": "unknown",<br>    "what_it_does": "Vanna provides a natural-language database agent, SQL execution tools, and a web component for presenting results. It supports Ollama, making a local model of 8B parameters or fewer a possible replacement for its hosted-model examples.",<br>    "what_to_fork": "Start with frontends/webcomponent/, the server examples, and RunSqlTool with SqliteRunner. Connect XiYanSQL-7B through an adapted local inference service; add result checks, explicit abstention, and BIRD evaluation. This combined agent has no verified BIRD score yet.",<br>    "url": "https://github.com/vanna-ai/vanna",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "Vanna"<br>  },<br>  {<br>    "browser_demo_feasible": "yes — existing browser UI backed by a locally running server",<br>    "last_update": "unknown",<br>    "what_it_does": "DB-GPT is an agentic data assistant that connects to databases and files, generates SQL and code, and executes analysis workflows. It documents private deployment and sandboxed execution.",<br>    "what_to_fork": "Reuse the SQL-query workflow and Web UI at localhost:5670. Configure only an approved model of 8B parameters or fewer, disable larger-model fallbacks, and add BIRD scoring plus answer-validation and refusal policies; no qualifying end-to-end BIRD score was verified.",<br>    "url": "https://github.com/eosphoros-ai/DB-GPT",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "DB-GPT"<br>  },<br>  {<br>    "browser_demo_feasible": "partial — useful SQL-generation components, but not a verified turnkey open-source browser application",<br>    "last_update": "unknown",<br>    "what_it_does": "XiYan-SQL describes schema representation, SQL candidate generation, refinement, and selection. Its standalone XiYanSQL-QwenCoder-7B-2504 model reports BIRD development execution accuracy of 62.13% with M-Schema and 57.43% with DDL.",<br>    "what_to_fork": "Use the linked XiYanSQL-QwenCoder and M-Schema components as the SQL engine behind Vanna or a thin custom UI. The examined repository is primarily a project index; do not treat its linked hosted GBI product or 32B demonstration as a qualifying fork. Restrict every generation, refinement, and selection model to at most 8B parameters.",<br>    "url": "https://github.com/XGenerationLab/XiYan-SQL",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "XiYan-SQL"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "CPU — requires CPU-oriented deployment or quantization; the supplied quickstart is not a verified CPU-only demo",<br>    "size": "15.25GB repository size reported by ModelScope; BF16 weights",<br>    "url": "https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-7B-2504",<br>    "name": "XiYanSQL-QwenCoder-7B-2504 — 7.62B parameters; preferred BIRD-scored SQL model"<br>  },<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "CPU — GGUF through llama.cpp; browser deployment not verified",<br>    "size": "4.68GB for Q4_K_M",<br>    "url": "https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",<br>    "name": "Qwen2.5-Coder-7B-Instruct-GGUF — 7.61B parameters, Q4_K_M"<br>  },<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "Both — CPU through llama.cpp; browser through a proposed wllama integration, not tested here",<br>    "size": "1.12GB for qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",<br>    "url": "https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",<br>    "name": "Qwen2.5-Coder-1.5B-Instruct-GGUF — 1.54B parameters, browser-first fallback; BIRD score unknown"<br>  }<br>] | 🟡 [<br>  "Database detective: ask a plain-English question over a messy database and watch the browser reveal schema inspection, generated joins, execution results, and proposed consistency checks before showing a chart. Use Vanna's frontend with a local XiYanSQL-7B backend, clearly displaying SQL and validation evidence.",<br>  "The analyst that refuses to bluff: include questions requiring missing fields or undefined business rules, then show an explicit cannot-answer response and a clarification request instead of fabricated numbers. Run this through the browser UI with custom answerability gates on the local backend; this refusal behavior must be implemented and evaluated.",<br>  "Airplane-mode analyst: after downloading the 1.12GB Qwen coder model and application assets, disconnect the network and answer questions entirely in the browser using wllama plus a browser-side SQLite engine. Show local SQL execution and a scorecard on selected original BIRD Mini-Dev examples; this is a proposed integration, not evidence that the small model matches XiYan's BIRD score."<br>] | 🟢 [<br>  "https://github.com/vanna-ai/vanna",<br>  "https://github.com/eosphoros-ai/DB-GPT",<br>  "https://github.com/XGenerationLab/XiYan-SQL",<br>  "https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-7B-2504",<br>  "https://www.modelscope.cn/models/XGenerationLab/XiYanSQL-QwenCoder-7B-2504",<br>  "https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",<br>  "https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",<br>  "https://github.com/ngxson/wllama",<br>  "https://github.com/ggml-org/llama.cpp",<br>  "https://bird-bench.github.io/",<br>  "https://github.com/bird-bench/mini_dev"<br>] | 🟡 [<br>  "Performance and portability: model download size is not total runtime memory. CPU inference may be slow, and wllama documents a 2GB per-file limit; larger models need splitting and sufficient browser memory. The 1.5B browser fallback has no verified BIRD score here.",<br>  "False confidence and misleading scoring: executable SQL can still use incorrect joins, filters, or business definitions. XiYan's reported BIRD development scores are standalone model results, not scores for the proposed validated/refusing agent; report the final system's execution accuracy and abstention performance separately.",<br>  "Execution safety and reuse terms: use read-only database access, bounded execution, and sandboxing rather than trusting generated SQL or code. Preserve BIRD's CC-BY-SA-4.0 obligations and applicable database-source terms when redistributing demonstration data."<br>] | 🟡 [<br>  "No examined project was verified to provide the complete combination of browser demo, exclusively <=8B models, SQL execution, semantic result validation, reliable abstention, and a published BIRD score.",<br>  "A validation-and-abstention layer: schema/field availability checks, ambiguity handling, result sanity checks, bounded repair attempts, and a dedicated unanswerable-question evaluation set. Successful execution alone is not semantic validation.",<br>  "A reproducible final-system BIRD harness recording model revision, quantization, prompts, schema format, evidence use, execution accuracy, latency, and refusals. Start with the original 500-example Mini-Dev subset, but do not label its score as full BIRD development or test performance.",<br>  "For browser-only execution, integration of wllama, browser-side SQL execution, database loading, caching, and memory management remains custom work; the shortlisted application frameworks normally use a backend."<br>] | 🟢 [<br>  "ModelScope — examined the XiYanSQL-QwenCoder-7B-2504 model card, licensing, size, benchmark table, and deployment examples"<br>] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "CC-BY-SA-4.0",<br>    "size": "Full benchmark: over 12,751 question–SQL pairs, 95 databases, 33.4GB; public-subset size unknown",<br>    "url": "https://bird-bench.github.io/",<br>    "name": "BIRD — public training/development resources; official test evaluation through the organizers"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "CC-BY-SA-4.0",<br>    "size": "500 question–SQL pairs from 11 databases",<br>    "url": "https://github.com/bird-bench/mini_dev",<br>    "name": "BIRD Mini-Dev — original 500-example SELECT-only subset, not the expanded V2 benchmark"<br>  }<br>] |
| 2 | ✅ completed | Interactive knowledge base: ingest PDFs and text, extract topics and triples, build a knowledge graph with themes, hybrid retrieval with a query router, grounded answers, split-screen app showing the graph path behind every answer. | 🟢 AI-03 | 🟡 [<br>  {<br>    "browser_demo_feasible": "yes — browser UI is available, backed by a LightRAG server/API and graph storage",<br>    "last_update": "2026-10-14",<br>    "what_it_does": "LightRAG builds a knowledge graph from documents and provides local, global, hybrid, and mixed retrieval modes. Its web UI supports document management, graph exploration, and querying.",<br>    "what_to_fork": "Fork the `/webui` frontend together with the LightRAG server/API integration; connect a graph store and seed it with a small PDF corpus. Add a custom split-screen answer-and-path panel, since the cited UI supports graph exploration but does not establish that exact layout.",<br>    "url": "https://github.com/HKUDS/LightRAG",<br>    "stars": "39,144",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "LightRAG"<br>  },<br>  {<br>    "browser_demo_feasible": "yes — a browser-facing application is available, but it depends on a backend and Neo4j",<br>    "last_update": "unknown",<br>    "what_it_does": "Transforms unstructured files, including PDFs and text, into a Neo4j knowledge graph. It offers several graph/vector/full-text chat modes, graph visualization through Neo4j Bloom, and source metadata for answers.",<br>    "what_to_fork": "Fork `frontend/` with the relevant `backend/` ingestion and chat components. Use the existing graph visualization and chat modes, then add a split-screen view that connects an answer’s source metadata to the corresponding graph path.",<br>    "url": "https://github.com/neo4j-labs/llm-graph-builder",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "Neo4j LLM Knowledge Graph Builder"<br>  },<br>  {<br>    "browser_demo_feasible": "partial — it has a web component and grounded retrieval features, but the repository calls for a substantial local deployment",<br>    "last_update": "2026-09-29",<br>    "what_it_does": "RAGFlow ingests heterogeneous documents, supports agentic multi-step retrieval, and can compile content into knowledge artifacts such as graphs and mind maps. It surfaces references and traceable citations for grounded answers.",<br>    "what_to_fork": "Start with `web/` and the relevant retrieval/knowledge-compilation endpoints; use a small, preloaded corpus and a backend deployment. Add a purpose-built graph-path view rather than assuming the existing graph artifact is an interactive answer-path visualization.",<br>    "url": "https://github.com/infiniflow/ragflow",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "RAGFlow"<br>  },<br>  {<br>    "browser_demo_feasible": "partial — the repository includes a `unified-search-app/` directory, but no existing graph-path browser UI was established",<br>    "last_update": "2026-10-08",<br>    "what_it_does": "Microsoft GraphRAG is a graph-based data pipeline and transformation suite for extracting structured information from unstructured text and forming targeted context for question answering. Its project documentation warns that indexing can be expensive and says the project is largely in maintenance mode.",<br>    "what_to_fork": "For a small demonstration, fork the relevant `packages/` pipeline and `unified-search-app/` as a starting point; add the graph-path and split-screen UI yourself. Keep the corpus small and account for its maintenance-mode status and indexing costs.",<br>    "url": "https://github.com/microsoft/graphrag",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "GraphRAG"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "Browser; Transformers.js documents CPU/WASM by default and WebGPU as an option",<br>    "size": "23 MB (`model_quantized.onnx`)",<br>    "url": "https://huggingface.co/Xenova/all-MiniLM-L6-v2/tree/main/onnx",<br>    "name": "Xenova/all-MiniLM-L6-v2 — quantized ONNX embedding weights"<br>  },<br>  {<br>    "license": "unknown",<br>    "runs_on_cpu_or_browser": "Browser via Transformers.js WebGPU example; Transformers.js also supports CPU/WASM generally, but performance for this weight was not confirmed",<br>    "size": "919 MB (`model_q4.onnx`)",<br>    "url": "https://huggingface.co/onnx-community/Qwen3-0.6B-ONNX/tree/main/onnx",<br>    "name": "Qwen3-0.6B-ONNX — `model_q4.onnx`"<br>  }<br>] | 🟡 [<br>  "Upload a short PDF in the browser UI, ask a question that spans multiple sections, and animate the retrieved entities and relations beside the grounded answer. A custom split-screen panel can highlight the source passages and graph path as the user switches between LightRAG’s local, global, and mixed retrieval modes.",<br>  "Run a bridge-question challenge over 2WikiMultihopQA: the browser shows the question, supporting paragraphs, and the dataset’s subject–relation–object evidence triples as a path, then reveals which supporting facts ground the answer.",<br>  "Show a curated micro-corpus in a browser using MiniLM’s small ONNX embedding weights and, optionally, Qwen3’s larger WebGPU-capable ONNX weights for generation. Preload the graph for this demo and make each answer reveal its connected evidence path; disclose the large model download and that the graph/backend is not thereby made browser-only."<br>] | 🟡 [<br>  "https://github.com/HKUDS/LightRAG",<br>  "https://github.com/HKUDS/LightRAG/commits/main/",<br>  "https://github.com/neo4j-labs/llm-graph-builder",<br>  "https://github.com/infiniflow/ragflow",<br>  "https://github.com/microsoft/graphrag",<br>  "https://huggingface.co/Xenova/all-MiniLM-L6-v2/tree/main/onnx",<br>  "https://huggingface.co/onnx-community/Qwen3-0.6B-ONNX/tree/main/onnx",<br>  "https://huggingface.co/docs/transformers.js/en/index",<br>  "https://huggingface.co/datasets/hotpotqa/hotpot_qa",<br>  "https://huggingface.co/datasets/framolfese/2WikiMultihopQA",<br>  "https://gitee.com/zhutao1221/LightRAG",<br>  "https://modelscope.cn/models/Qwen/Qwen3-0.6B"<br>] | 🟡 [<br>  "Performance and download size: the cited Qwen3 q4 ONNX file is 919 MB; browser WebGPU support is experimental in many browsers, so a lightweight embedding model or precomputed answers/graphs may be needed for a smooth demo.",<br>  "Infrastructure complexity: the graph experience is not established as an end-to-end browser-only app; Neo4j’s backend and frontend may need separate deployment, and RAGFlow recommends a starting configuration of 4 CPU cores, 16 GB RAM, and 50 GB disk.",<br>  "Licensing needs review: HotpotQA is CC BY-SA 4.0, 2WikiMultihopQA is listed as Apache-2.0, and the Qwen ONNX weight license was not established in the examined model evidence. Check weight, dataset, and redistribution terms before publishing a fork."<br>] | 🟡 [<br>  "A unified split-screen interface that synchronizes each answer with the exact graph path and supporting source passages; the examined projects offer pieces such as graph exploration, source metadata, or traceable citations, but the requested combined interaction was not established.",<br>  "A turnkey browser-only pipeline for PDF ingestion, topic/triple extraction, graph storage, retrieval, and answer generation. The examined graph projects use server-side components; browser-capable inference weights alone do not supply this complete pipeline.",<br>  "A small, reproducible demo bundle that connects a curated dataset’s evidence annotations to a prebuilt graph and provides deterministic, judge-friendly example queries is not supplied as one integrated artifact by the examined projects."<br>] | 🟢 [<br>  "Gitee — examined a LightRAG repository/mirror; it displayed an MIT license and repository contents, with some operations requiring login.",<br>  "ModelScope — examined Qwen3 search/model pages; the readable listing was limited and did not establish the model’s license or full repository contents."<br>] | 🟡 [<br>  {<br>    "usable_now": "yes — Hugging Face dataset page and downloadable dataset files were available in the examined sources",<br>    "license": "CC BY-SA 4.0",<br>    "size": "612.75 MB downloaded dataset files",<br>    "url": "https://huggingface.co/datasets/hotpotqa/hotpot_qa",<br>    "name": "HotpotQA"<br>  },<br>  {<br>    "usable_now": "yes — the Hugging Face dataset page documents loading the dataset",<br>    "license": "Apache-2.0 (original dataset license stated by the dataset card)",<br>    "size": "113,284 train; 12,981 validation; 12,995 test examples (dataset-card split counts)",<br>    "url": "https://huggingface.co/datasets/framolfese/2WikiMultihopQA",<br>    "name": "2WikiMultihopQA"<br>  }<br>] |
| 3 | ✅ completed | RAG evaluation pipeline that tests retriever and generator separately, generates synthetic questions, diagnoses retrieval failure vs hallucination, single-screen dashboard. | 🟢 AI-04 | 🟡 [<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2026-02-24",<br>    "what_it_does": "Ragas provides synthetic test generation and separate retrieval and answer-quality metrics. It is the strongest core for the requested evaluation pipeline, but needs a dashboard.",<br>    "what_to_fork": "Fork TestsetGenerator and the collections-based ContextRecall/Faithfulness metrics. Add a single-screen browser UI backed by Python, showing retrieved chunks, reference answers, generated answers, and separate scores. Activity metadata reflects retrieved repository snapshots, not guaranteed live values.",<br>    "url": "https://github.com/vibrantlabsai/ragas",<br>    "stars": "16,034 (retrieved repository snapshot)",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "Ragas"<br>  },<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "2026-10-23",<br>    "what_it_does": "EvalScope combines model evaluation, a RAGAS-backed RAG evaluation module, and a browser-accessible results dashboard. It is the most promising dashboard starting point among the reviewed projects.",<br>    "what_to_fork": "Fork the RAG evaluation integration and React/Vite visualization service; launch with evalscope service. Add synthetic-question generation and a dedicated retrieval-versus-generation diagnosis view. The UI runs in the browser; evaluation still uses a backend.",<br>    "url": "https://github.com/modelscope/evalscope",<br>    "stars": "3,583 (retrieved repository snapshot)",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "EvalScope"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2024-12-13",<br>    "what_it_does": "RAGChecker provides fine-grained diagnostic metrics for retrievers and generators, including claim recall, context utilization, noise sensitivity, hallucination, and faithfulness.",<br>    "what_to_fork": "Wrap RAGResults, RAGChecker.evaluate, and the diagnostic JSON output in a browser dashboard. Supply ground-truth answers and connect Ragas for synthetic questions; its documented checking example uses a remote 70B model rather than browser inference.",<br>    "url": "https://github.com/amazon-science/RAGChecker",<br>    "stars": "1,126 (retrieved repository snapshot)",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "RAGChecker"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2026-10-12",<br>    "what_it_does": "Giskard tests retrieval independently from answer quality and checks whether answers are grounded in retrieved documents. Its repository also provides RAG evaluation dataset-generation tooling.",<br>    "what_to_fork": "Fork the RAGResponse example, retrieval checks, and Groundedness scenarios; expose their results through a custom browser screen. Check compatibility between current modular packages and legacy RAGET generation examples; do not assume the Enterprise review interface is included in OSS.",<br>    "url": "https://github.com/Giskard-AI/giskard-oss",<br>    "stars": "5,888 (retrieved repository snapshot)",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "Giskard"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "Both — browser CPU through Transformers.js/WASM; also usable in CPU ONNX runtimes.",<br>    "size": "23MB for model_quantized.onnx; tokenizer/configuration files additional.",<br>    "url": "https://huggingface.co/Xenova/all-MiniLM-L6-v2/tree/main/onnx",<br>    "name": "Xenova/all-MiniLM-L6-v2 — quantized ONNX embeddings"<br>  },<br>  {<br>    "license": "unknown for the ONNX conversion repository; upstream Qwen weights are Apache-2.0.",<br>    "runs_on_cpu_or_browser": "Both — Transformers.js supports browser CPU/WASM execution; this model's demo performance remains unbenchmarked.",<br>    "size": "512MB for model_quantized.onnx; tokenizer/configuration files additional.",<br>    "url": "https://huggingface.co/onnx-community/Qwen2.5-0.5B-Instruct/tree/main/onnx",<br>    "name": "onnx-community/Qwen2.5-0.5B-Instruct — quantized ONNX generator"<br>  }<br>] | 🟡 [<br>  "Failure flight recorder: use browser toggles to remove the relevant retrieved chunk or inject an unsupported answer claim. A Python evaluator updates separate retrieval and faithfulness panels, with highlighted evidence and a probable—not definitive—failure diagnosis.",<br>  "Turn a document into its own exam: upload a document in the browser, generate synthetic questions through Ragas, and run two retrieval configurations against the same questions. One screen shows which configuration recovered evidence and whether the generator actually used it.",<br>  "Disconnect-the-internet demonstration: after caching assets, run MiniLM embeddings, a small document search, and the quantized Qwen generator inside the browser. Display local reference-based retrieval checks alongside clearly labeled precomputed judge scores; do not present those scores as live offline hallucination detection."<br>] | 🟢 [<br>  "https://github.com/explodinggradients/ragas",<br>  "https://api.github.com/repos/vibrantlabsai/ragas",<br>  "https://api.github.com/repos/vibrantlabsai/ragas/commits?per_page=1",<br>  "https://docs.ragas.io/en/stable/getstarted/rag_testset_generation/",<br>  "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/",<br>  "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",<br>  "https://github.com/modelscope/evalscope",<br>  "https://api.github.com/repos/modelscope/evalscope",<br>  "https://github.com/amazon-science/RAGChecker",<br>  "https://api.github.com/repos/amazon-science/RAGChecker",<br>  "https://api.github.com/repos/amazon-science/RAGChecker/commits?per_page=1",<br>  "https://github.com/Giskard-AI/giskard",<br>  "https://api.github.com/repos/Giskard-AI/giskard-oss",<br>  "https://docs.giskard.ai/oss/checks/use-cases/rag-evaluation",<br>  "https://huggingface.co/Xenova/all-MiniLM-L6-v2",<br>  "https://huggingface.co/Xenova/all-MiniLM-L6-v2/tree/main/onnx",<br>  "https://huggingface.co/onnx-community/Qwen2.5-0.5B-Instruct",<br>  "https://huggingface.co/onnx-community/Qwen2.5-0.5B-Instruct/tree/main/onnx",<br>  "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct",<br>  "https://huggingface.co/docs/transformers.js/en/index",<br>  "https://huggingface.co/datasets/galileo-ai/ragbench",<br>  "https://huggingface.co/datasets/rag-datasets/rag-mini-wikipedia",<br>  "https://modelscope.cn/models/Qwen/Qwen2.5-0.5B-Instruct"<br>] | 🟡 [<br>  "Misdiagnosis: faithfulness measures support in retrieved context, not independent factual truth. Missing references, imperfect synthetic questions, and judge errors can mislabel retrieval failures as hallucinations; use labeled examples and treat diagnoses as probabilistic.",<br>  "Latency and cost: RAGChecker's documented example uses a remote 70B model, while the small browser generator alone downloads 512MB of weights. Use small test batches, cached assets, and asynchronous progress; do not assume a small local generator is a reliable evaluator.",<br>  "Data governance: remote evaluation can expose uploaded documents and answers to model providers. Keep credentials server-side, obtain consent or use local processing, preserve dataset attribution, and resolve the ONNX conversion's unspecified license before redistributing it."<br>] | 🟡 [<br>  "No reviewed project was verified to supply the entire requested workflow turnkey. A unified screen still needs to join synthetic questions, retrieved evidence, generated answers, separate scores, and diagnosis.",<br>  "A shared result schema and diagnostic decision layer are needed to distinguish missing evidence, failure to use available evidence, unsupported claims, and unanswerable questions; metric scores alone do not establish causality.",<br>  "A validated, fully client-side evaluation stack is missing from the reviewed options. Browser embeddings and generation are feasible, but synthetic-question quality, evaluator calibration, offline packaging, and cross-browser performance still require implementation and testing."<br>] | 🟢 [<br>  "ModelScope — Qwen2.5-0.5B-Instruct model card",<br>  "ModelScope Community — EvalScope repository"<br>] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "CC-BY-4.0",<br>    "size": "95,381 rows; 451MB of files across 12 component datasets.",<br>    "url": "https://huggingface.co/datasets/galileo-ai/ragbench",<br>    "name": "RAGBench"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "CC-BY-3.0",<br>    "size": "918 question-answer rows and 3,200 corpus rows; 4,118 rows total.",<br>    "url": "https://huggingface.co/datasets/rag-datasets/rag-mini-wikipedia",<br>    "name": "rag-mini-wikipedia"<br>  }<br>] |
| 4 | ✅ completed | Zero-knowledge eligibility credentials: issuer signs a credential, holder proves one fact (over 18, state, income below limit) to a smart contract with a ZK proof, nothing else revealed. Circom or Noir, signature verified inside the circuit, browser proving. | 🟢 W3-01 | 🟡 [<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2026-10-23",<br>    "what_it_does": "Closest functional match: Noir circuits verify an issuer’s secp256k1 ECDSA signature over a credential commitment and prove attribute predicates to real Stellar/Soroban verification contracts. Browser proof generation exists, but witness generation currently uses a server endpoint, so the stock implementation does not meet strict browser-only privacy.",<br>    "what_to_fork": "Fork circuits/age_proof, circuits/composite_policy, frontend, packages/issuer, and the registry/verifier contracts. Use composite_policy for income upper bounds; move witness execution into the browser before claiming private inputs never leave the holder’s device. Its jurisdiction field represents countries, not US states.",<br>    "url": "https://github.com/ToluLabs/StellarCred",<br>    "stars": "30",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "StellarCred"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2026-02-12",<br>    "what_it_does": "Circom-based zero-knowledge certificates, zkKYC/age-proof circuits, smart contracts, and browser-facing demonstration applications. Proof generation runs locally through a MetaMask Snap; the documentation requires MetaMask Flask rather than a plain browser tab.",<br>    "what_to_fork": "Fork packages/zk-certificates, packages/snap, and packages/galactica-dapp. Start with ageProofZkKYC and the example credential; inspect providerSignatureCheck.circom and its composition before asserting the precise in-circuit signature guarantee. Prepare the WASM/proving keys and extension installation before judging.",<br>    "url": "https://github.com/Galactica-corp/galactica-monorepo",<br>    "stars": "13",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "galactica-monorepo"<br>  },<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "2026-04-29",<br>    "what_it_does": "Official Noir reference examples provide browser-based proving and a separate Noir-to-Solidity verification workflow. This is a useful implementation foundation, not a finished signed-credential eligibility application.",<br>    "what_to_fork": "Combine web-starter with solidity-example for a browser/EVM demo. Add credential issuance, in-circuit issuer-signature verification, the requested attribute predicate, and contract-side issuer/policy checks; these eligibility-specific pieces are not supplied by the starter.",<br>    "url": "https://github.com/noir-lang/noir-examples",<br>    "stars": "78",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "noir-examples"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2025-04-30",<br>    "what_it_does": "Privado ID SDK examples demonstrate identity creation, credential issuance, state transitions, proof generation, and authentication requests. The reviewed repository runs as command-line examples; the wider framework supports web-wallet proof generation and on-chain credential verification.",<br>    "what_to_fork": "Reuse issueCredential, generateProofs, and authentication-request examples, then add a browser holder UI and the framework’s on-chain verification integration. Download the circuit artifacts and configure RPC/state services; verify the selected signature-based circuit rather than assuming every credential proof checks a signature in-circuit.",<br>    "url": "https://github.com/PrivadoID/js-sdk-examples",<br>    "stars": "18",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "js-sdk-examples"<br>  }<br>] | 🟡 [] | 🟡 [<br>  "Private age gate: a demo issuer signs a date-of-birth credential, and the browser proves age ≥18 before a testnet contract unlocks access—without receiving the birth date. Build on StellarCred’s age circuit, replacing its server witness step with local execution for the strict privacy version.",<br>  "Means-tested grant without revealing salary: an issuer signs income, the browser proves income is below a public limit, and a contract releases a demonstration token. Adapt StellarCred’s upper-bound policy support and generate the witness locally; show that editing the signed income makes verification fail.",<br>  "Resident-only ballot: add a signed state-code attribute, then use the Noir browser starter to prove that it matches the ballot’s allowed state before Solidity opens voting. Show the contract receiving only the predicate proof and necessary public verification inputs; this requires a new state schema, not reuse of StellarCred’s country field."<br>] | 🟢 [<br>  "https://github.com/ToluLabs/StellarCred",<br>  "https://api.github.com/repos/ToluLabs/StellarCred",<br>  "https://github.com/ToluLabs/StellarCred/tree/main/circuits",<br>  "https://github.com/ToluLabs/StellarCred/tree/main/fixtures",<br>  "https://github.com/Galactica-corp/galactica-monorepo",<br>  "https://api.github.com/repos/Galactica-corp/galactica-monorepo",<br>  "https://github.com/Galactica-corp/galactica-monorepo/tree/main/packages/snap",<br>  "https://github.com/Galactica-corp/galactica-monorepo/tree/main/packages/zk-certificates",<br>  "https://github.com/Galactica-corp/galactica-monorepo/tree/main/packages/zk-certificates/circuits",<br>  "https://github.com/Galactica-corp/galactica-monorepo/blob/main/packages/zk-certificates/example/kycFields.json",<br>  "https://github.com/noir-lang/noir-examples",<br>  "https://api.github.com/repos/noir-lang/noir-examples",<br>  "https://github.com/PrivadoID/js-sdk-examples",<br>  "https://api.github.com/repos/PrivadoID/js-sdk-examples",<br>  "https://docs.privado.id/docs/verifier/on-chain-verification/overview"<br>] | 🟡 [<br>  "“Nothing else revealed” is too strong: StellarCred exposes verification activity and wallet-to-claim links, and its current witness endpoint introduces a server trust boundary. Public commitments, issuer identifiers, policy inputs, and transactions must be disclosed honestly in the demo’s privacy explanation.",<br>  "Proof validity is not the same as trustworthy eligibility. The contract must enforce the intended issuer, policy inputs, verification key, validity/revocation rules, and replay protections; a trusted issuer can still sign false attributes. Modified Galactica circuits also require a production phase-2 trusted setup.",<br>  "Live-demo reliability remains unbenchmarked: browser proving time and memory were not established in the reviewed evidence. Circuit artifacts and compiler/verifier-key versions must match, while Galactica additionally introduces extension installation and MetaMask Flask dependencies."<br>] | 🟡 [<br>  "For the closest match, StellarCred, replace POST /api/witness with browser-local witness execution before making an end-to-end holder-only privacy claim.",<br>  "Add a signed subnational-state schema and predicate. StellarCred’s documented jurisdiction encoding is an ISO country code, not a US-state credential.",<br>  "A polished, extension-free issuer → browser holder → smart-contract application covering all three requested predicates was not established among the reviewed projects. The Noir starter needs credential-specific integration, while the Privado example repository needs a browser frontend."<br>] | 🟢 [] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown",<br>    "size": "unknown",<br>    "url": "https://github.com/ToluLabs/StellarCred/tree/main/fixtures",<br>    "name": "StellarCred proof/test fixtures — age, income, jurisdiction, and negative cases"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown",<br>    "size": "1 example credential record",<br>    "url": "https://github.com/Galactica-corp/galactica-monorepo/blob/main/packages/zk-certificates/example/kycFields.json",<br>    "name": "Galactica example KYC credential fields"<br>  }<br>] |
| 5 | ✅ completed | Agent wallet: ERC-4337 account abstraction where an AI agent key can spend only inside an owner policy (allowed contracts/functions, per-tx and daily limits, recipients, expiry, owner approval outside policy), policies hold even if the agent is malicious or the key leaks. | 🟢 W3-02 | 🟡 [<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "unknown",<br>    "what_it_does": "Kernel is an ERC-4337 smart account with on-chain permissions composed from a signer and policies. These can restrict session keys by function selector, target, spending conditions and time windows without granting the root owner's authority.",<br>    "what_to_fork": "Fork Kernel plus the ZeroDev SDK's plugins/permission and TypeScript template. Build a browser dashboard for owner-authorized session creation and adversarial transactions through an RPC/bundler; pin compatible account, SDK and EntryPoint versions. A complete daily-budget and owner-exception workflow was not verified as turnkey.",<br>    "url": "https://github.com/zerodevapp/kernel",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "Kernel — ZeroDev"<br>  },<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "2026-09-21",<br>    "what_it_does": "Smart Sessions supplies session-key modules for ERC-7579-compatible accounts, with action-specific policies and signature validation. Available policy contracts include ERC20 spending limits, native-value limits, timeframes and contract whitelists.",<br>    "what_to_fork": "Fork contracts, policy modules and tests; adapt the linked session-keys example into a browser UI on a compatible ERC-4337 account. Crucially, configure a restricted session that disables the SDK's unmatched-call intent fallback: listing permissions alone is not documented as deny-by-default. Daily monetary reset semantics still need verification or implementation.",<br>    "url": "https://github.com/rhinestonewtf/smartsessions",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "AGPL-3.0",<br>    "name": "Smart Sessions — Rhinestone fork"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "unknown",<br>    "what_it_does": "Alchemy Modular Account V2 offers modular smart-account permissions, including address/function allowlists, ERC20 limits, cumulative native-token limits including gas, and expiry. Session-key validations are installed on the account rather than enforced only by an agent service.",<br>    "what_to_fork": "Fork the account and AllowlistModule, NativeTokenLimitModule and TimeRangeModule; connect them to a browser using the documented smart-accounts/viem installation flow. Keep agent validation selector-scoped, not global. Recipient-argument constraints, recurring daily resets and an owner-only exception UI require additional work or verification.",<br>    "url": "https://github.com/alchemyplatform/modular-account",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "GPL-3.0",<br>    "name": "Alchemy Modular Account V2"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "Both",<br>    "size": "137MB for model_quantized.onnx; tokenizer and runtime additional",<br>    "url": "https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/resolve/main/onnx/model_quantized.onnx?download=true",<br>    "name": "SmolLM2-135M-Instruct — quantized ONNX, optional intent proposer only"<br>  }<br>] | 🟡 [<br>  "Proposed demo: “Steal my agent key.” Reveal a disposable testnet session key in the browser, then let the judge attempt a forbidden contract, selector or recipient; display validation failures alongside a successful permitted payment, proving that the browser UI is not the security boundary.",<br>  "Proposed demo: “Death by a thousand small payments.” Configure a 5-USDC per-transaction cap and 12-USDC daily budget, then launch repeated 5-USDC payments from the browser: the third must fail despite passing the per-transaction rule. Drive a local development chain from the UI to demonstrate the specified daily-reset boundary after implementing and testing cumulative accounting.",<br>  "Proposed demo: “An agent that must ask.” An optional browser-local model proposes an out-of-policy payment, which remains blocked until the owner signs that exact transaction through a separate approval flow. Show that this one-off approval does not broaden the agent's session, then demonstrate expiry or revocation in the same dashboard."<br>] | 🟢 [<br>  "https://github.com/zerodevapp/kernel",<br>  "https://github.com/zerodevapp/sdk",<br>  "https://github.com/zerodevapp/sdk/tree/main/plugins/permission",<br>  "https://docs.zerodev.app/smart-accounts/permissions/intro",<br>  "https://github.com/rhinestonewtf/smartsessions",<br>  "https://github.com/rhinestonewtf/smartsessions/commits/main/",<br>  "https://github.com/rhinestonewtf/smartsessions/tree/main/contracts/external/policies",<br>  "https://docs.rhinestone.dev/smart-wallet/smart-sessions/overview",<br>  "https://docs.rhinestone.dev/smart-wallet/tutorials/session-keys",<br>  "https://github.com/alchemyplatform/modular-account",<br>  "https://www.alchemy.com/docs/wallets/smart-contracts/modular-account-v2/overview",<br>  "https://www.alchemy.com/docs/wallets/smart-contracts/modular-account-v2/session-keys/adding-session-keys",<br>  "https://github.com/zerodevapp/kernel/tree/dev/test",<br>  "https://github.com/rhinestonewtf/smartsessions/tree/main/test",<br>  "https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct",<br>  "https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/tree/main/onnx",<br>  "https://www.modelscope.cn/models/onnx-community/SmolLM2-135M-Instruct-ONNX/summary"<br>] | 🟡 [<br>  "Permission escape through configuration: Rhinestone documents permissive defaults and an unmatched-call Orchestrator fallback; Alchemy warns that global validation can upgrade the account or change ownership. The agent must not receive these broader capabilities, and restrictions must survive direct submission outside the UI.",<br>  "A leaked key can still spend its legitimate allowance. Contract bugs, incomplete cumulative accounting or unexamined execution paths can invalidate the intended boundary; revocation also races attacker transactions until mined. The reviewed material does not establish an unconditional malicious-agent security guarantee for the complete proposed configuration.",<br>  "Fork/deployment obligations: Smart Sessions and Alchemy use copyleft licenses, unlike MIT-licensed Kernel. Review redistribution and applicable source-disclosure obligations, and pin compatible deployed contracts, SDKs, EntryPoint and bundler infrastructure before relying on a live demo."<br>] | 🟡 [<br>  "No reviewed project was verified to supply the complete requested browser workflow: policy editor, owner/session separation, adversarial transaction controls, receipts and exact-transaction owner approvals in one turnkey application.",<br>  "A verified recurring daily monetary budget remains a gap. Retrieved documentation establishes spending, timeframe and usage/rate primitives, but not the complete daily-reset and cross-session aggregation semantics required here; transaction-count limits are not monetary budgets.",<br>  "The owner-exception path needs explicit integration: an out-of-policy request must remain blocked until a separate owner authorization approves the exact transaction, without silently widening the agent's permissions. Recipient argument restrictions and all relevant execution paths also need regression coverage."<br>] | 🟢 [<br>  "ModelScope — examined the SmolLM2-135M-Instruct-ONNX mirror; it provides download instructions but a sparse model card."<br>] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "MIT — repository license",<br>    "size": "unknown",<br>    "url": "https://github.com/zerodevapp/kernel/tree/dev/test",<br>    "name": "Kernel contract regression fixtures and mocks — software tests, not an ML training dataset"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "AGPL-3.0 — repository license",<br>    "size": "unknown",<br>    "url": "https://github.com/rhinestonewtf/smartsessions/tree/main/test",<br>    "name": "Smart Sessions argument-policy integration tests, unit tests and mocks — software tests, not an ML training dataset"<br>  }<br>] |
| 6 | ✅ completed | ProvenanceLab: reproducible molecule analysis. Validate SMILES precisely (broken valence, ambiguous stereochemistry, salts, tautomers), compute and compare properties, never silently fill missing values, reproduce any run exactly, frozen PubChem and ChEMBL snapshots. | 🟢 HM-01 | 🟡 [<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "unknown",<br>    "what_it_does": "RDKit.js exposes a subset of RDKit through WebAssembly for molecule parsing, rendering and descriptor calculation directly in JavaScript. It is the strongest starting point for a browser-local demo; its documented interface includes validity checks and stereochemistry tags.",<br>    "what_to_fork": "Start with examples/ and its Vanilla JS or React example. Build a batch-SMILES workbench around get_mol(), is_valid(), get_descriptors() and get_stereo_tags(); add explicit errors, property comparison and provenance export rather than assuming the JavaScript subset provides every Python validation function.",<br>    "url": "https://github.com/rdkit/rdkit-js",<br>    "stars": "248 in the inspected repository snapshot; live count not verified",<br>    "host": "GitHub",<br>    "license": "BSD-3-Clause",<br>    "name": "RDKit.js"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "unknown",<br>    "what_it_does": "ChEMBL Structure Pipeline provides structure checking, standardization and salt stripping/parent extraction. Its checker reports structure issues with penalty scores from 0 to 9.",<br>    "what_to_fork": "Reuse chembl_structure_pipeline/ and the README examples for checker.check_molblock(), standardizer.standardize_molblock() and standardizer.get_parent_molblock(). Expose a pinned Python service to the browser, displaying the original structure, proposed transformations and checker findings separately; native browser execution was not established.",<br>    "url": "https://github.com/chembl/ChEMBL_Structure_Pipeline",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "ChEMBL Structure Pipeline"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "unknown",<br>    "what_it_does": "Datamol is a Python molecular-processing library built on RDKit, with sanitization, standardization and molecule-processing examples. It offers an online Binder notebook, but that runs Python remotely rather than establishing client-side browser execution.",<br>    "what_to_fork": "Adapt docs/tutorials/The_Basics.ipynb and the notebooks/ and tests/ directories into a pinned reference workflow behind the browser UI. Treat fix_mol(), sanitize_mol() and standardize_mol() as explicit, logged operations—not automatic repairs applied before validation.",<br>    "url": "https://github.com/datamol-io/datamol",<br>    "stars": "552 in the inspected repository snapshot; live count not verified",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "datamol"<br>  }<br>] | 🟡 [] | 🟡 [<br>  "Proposed molecule X-ray: paste a batch of SMILES and watch the browser draw structures beside separate parse failures, valence findings and unspecified-stereochemistry warnings. RDKit.js handles local rendering and descriptors; detailed Python diagnostics use a pinned CPU service until equivalent browser functionality is verified.",<br>  "Proposed identity switchboard: compare the original salt, an explicitly selected parent and alternative tautomer forms, with property changes and every transformation shown side by side in the browser. ChEMBL parent extraction can run behind the UI; tautomer enumeration and its audit trail remain implementation work, and the original input is never overwritten.",<br>  "Proposed offline time machine: export a run capsule, disconnect, then import it into a browser that verifies the bundled engine and dataset hashes before replaying descriptor calculations on a small frozen subset. The UI flags changed outputs and preserves unavailable properties as null with reasons, rather than silently fetching or inventing replacements."<br>] | 🟢 [<br>  "https://github.com/rdkit/rdkit-js",<br>  "https://docs.rdkitjs.com/interfaces/JSMol.html",<br>  "https://github.com/rdkit/rdkit/tree/master/Code/MinimalLib",<br>  "https://github.com/chembl/ChEMBL_Structure_Pipeline",<br>  "https://github.com/datamol-io/datamol",<br>  "https://www.rdkit.org/docs/RDKit_Book.html",<br>  "https://www.rdkit.org/docs/Cookbook.html",<br>  "https://pubchem.ncbi.nlm.nih.gov/docs/downloads",<br>  "https://pubchem.ncbi.nlm.nih.gov/docs/rdf-ftp",<br>  "https://chembl.github.io/chembl-licensing",<br>  "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/"<br>] | 🟡 [<br>  "Chemical interpretation: successful parsing is not evidence of fully specified stereochemistry or the intended chemical identity. Sanitization bypasses, salt removal and tautomer choices must not be presented as harmless repairs; preserve the original and require explicit transformation policies.",<br>  "Execution and replay: RDKit.js exposes only a subset of RDKit, so advanced Python workflows cannot be assumed to run unchanged in-browser. Large data distributions are unsuitable as browser payloads; exact replay requires pinned artifacts, retained data and tested serialization, while a server fallback introduces upload/privacy considerations.",<br>  "Data rights and snapshot integrity: ChEMBL requires CC-BY-SA-3.0 compliance and attribution including its release version. PubChem licensing varies by contributor, and its documented monthly RDF refresh is not an immutable archive; retain permitted source bytes, provenance metadata and hashes rather than depending on a moving download URL."<br>] | 🟡 [<br>  "A unified browser UI and typed result contract are still needed: distinguish parse errors, chemical warnings, unavailable source values and calculation failures. Keep missing values null with reasons, and separate computed descriptors from experimental or predicted properties; the deterministic core needs no learned model weights.",<br>  "Browser/Python validation parity remains unestablished. Add and test detailed valence diagnostics, potential-but-unspecified stereochemistry detection, salt/mixture handling and an explicit tautomer policy without assuming these are all exposed by RDKit.js.",<br>  "A content-addressed replay capsule is not established by the reviewed projects: retain original inputs, engine/WASM or container artifacts, dependency versions, transformation options, descriptor definitions, dataset bytes, provenance, hashes and stable output serialization.",<br>  "The frozen data layer still needs assembly. Select a small ChEMBL 37 subset and retain a separately identified PubChem subset with contributor licensing and acquisition metadata; a verified immutable PubChem snapshot endpoint and a ready-made adversarial validation suite covering the requested edge cases were not established."<br>] | 🔴 [] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "CC-BY-SA-3.0",<br>    "size": "SDF: 888M compressed; SQLite: 5.4G compressed, as reported by the release directory",<br>    "url": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/",<br>    "name": "ChEMBL 37 release files"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown",<br>    "size": "unknown",<br>    "url": "https://pubchem.ncbi.nlm.nih.gov/docs/downloads",<br>    "name": "PubChem bulk downloads—source for a locally retained snapshot, not a verified immutable archive"<br>  }<br>] |
| 7 | ✅ completed | Prescription safety checker for Indian brand medicines: resolve brand names and combinations to active ingredients and strengths, flag interactions, duplicate ingredients and excessive doses by age/weight/kidney function, reduce alert fatigue. Test set needs a pharmacist. | 🟢 HM-02 | 🟡 [<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2025-04-14",<br>    "what_it_does": "MedicineDB API Server supports medicine lookup, fuzzy name matching, composition analysis and alternative suggestions. It is a useful Indian-brand resolution component, not a complete prescription-safety checker.",<br>    "what_to_fork": "Reuse server.py's fuzzy matching and composition parsing behind a browser search form. Adapt the Indian Medicine Dataset to its expected JSON schema, then add explicit ingredient, strength, formulation and ambiguity confirmation.",<br>    "url": "https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "INDIAN_MEDICINE_MCP_SERVER"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "2026-04-21",<br>    "what_it_does": "MedRecon provides medication reconciliation, interaction checking, dose validation and a Next.js dashboard. Its documented knowledge coverage is limited to 48 curated interactions and dose ranges for 18 common drugs.",<br>    "what_to_fork": "Use frontend/ and the check_interactions, validate_dose and reconcile_lists tools in mcp-server/. Add Indian brand resolution and pharmacist-reviewed rules; the supplied architecture requires backend services and a Gemini API key, so it is not browser-only.",<br>    "url": "https://github.com/astraedus/medrecon",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "MIT",<br>    "name": "MedRecon"<br>  },<br>  {<br>    "browser_demo_feasible": "yes",<br>    "last_update": "unknown",<br>    "what_it_does": "Tesseract.js performs OCR in browsers and Node.js. It can supply editable text from medicine-pack or printed-prescription images, but does not identify clinically correct medicines or validate doses.",<br>    "what_to_fork": "Reuse examples/ and the createWorker image-recognition workflow for local image upload and editable extraction. Self-host language files and require confirmation of names, decimal points and units; PDF rendering needs an additional component.",<br>    "url": "https://github.com/naptha/tesseract.js",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "Tesseract.js"<br>  },<br>  {<br>    "browser_demo_feasible": "partial",<br>    "last_update": "unknown",<br>    "what_it_does": "cql-execution executes clinical logic expressed as JSON ELM using TypeScript/JavaScript. It supplies a rules runtime, not Indian drug terminology or ready-made medication-safety rules.",<br>    "what_to_fork": "Reuse the examples and Library/Executor workflow for auditable pharmacist-authored dose and duplication rules. Start with a browser form calling a Node.js service; browser-only packaging and drug terminology integration remain development work.",<br>    "url": "https://github.com/cqframework/cql-execution",<br>    "stars": "unknown",<br>    "host": "GitHub",<br>    "license": "Apache-2.0",<br>    "name": "cql-execution"<br>  }<br>] | 🟡 [<br>  {<br>    "license": "Apache-2.0",<br>    "runs_on_cpu_or_browser": "Both",<br>    "size": "10.4 MB compressed",<br>    "url": "https://github.com/naptha/tessdata/blob/gh-pages/4.0.0/eng.traineddata.gz",<br>    "name": "Tesseract English OCR — eng.traineddata.gz"<br>  }<br>] | 🟡 [<br>  "Brand X-ray: select two Indian brands and watch each expand into its ingredients and strengths, revealing an overlapping ingredient hidden inside a combination product. A proposed browser-local version would use a pharmacist-checked catalogue subset and Tesseract.js for optional pack-photo input, with mandatory correction before checking.",<br>  "Patient-context replay: change age, weight or kidney-function inputs and see which pharmacist-approved dose rules change, with the calculation and missing-information checks shown beside each alert. Run a small, explicitly reviewed ruleset locally in JavaScript or through a browser-connected rules service—not an LLM-generated dosing recommendation.",<br>  "Signal, not sirens: load a synthetic multi-medicine prescription and switch between raw alerts and grouped, evidence-linked alerts, while keeping serious warnings visible. The browser groups repeated warnings by ingredient or mechanism and lets a pharmacist record overrides; the demonstration shows the interface concept, not proven alert-fatigue reduction."<br>] | 🟢 [<br>  "https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER",<br>  "https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER/commits/main/",<br>  "https://github.com/astraedus/medrecon",<br>  "https://github.com/astraedus/medrecon/commits/main/",<br>  "https://github.com/naptha/tesseract.js",<br>  "https://github.com/cqframework/cql-execution",<br>  "https://github.com/naptha/tessdata",<br>  "https://github.com/naptha/tessdata/blob/gh-pages/4.0.0/eng.traineddata.gz",<br>  "https://github.com/junioralive/Indian-Medicine-Dataset",<br>  "https://ddinter2.scbdd.com/",<br>  "https://ddinter2.scbdd.com/download",<br>  "https://gitee.com/icu_reese/rationalmedication"<br>] | 🟡 [<br>  "Clinical false reassurance: the shortlisted components do not establish complete Indian-brand coverage or validated age-, weight- and kidney-specific dosing. OCR, combination parsing and incomplete interaction coverage can miss hazards; unresolved medicines must be marked unknown, and pharmacist-reviewed test cases are essential.",<br>  "Data rights and freshness: DDInter is accessible but its download page states All Rights Reserved; an open redistribution license was not established. The Indian dataset advertises MIT, but upstream rights, current formulations and clinical accuracy still need assessment before distribution or deployment.",<br>  "Privacy and external-service exposure: MedRecon's supplied architecture uses Gemini and a public FHIR test server. Use synthetic cases for judging, do not send identifiable prescriptions to public services, and separate browser-local OCR from any explicitly disclosed backend processing."<br>] | 🟡 [<br>  "A pharmacist-maintained Indian brand-to-ingredient-and-strength layer with formulation, release type, salt equivalence, liquid concentrations, multi-ingredient combinations and explicit handling of uncertain matches. The examined catalogue's two composition fields are a starting point, not proof of complete normalization.",<br>  "A validated patient-specific dosing knowledge base covering pediatric and adult limits, frequency, total daily exposure and renal adjustment, including which renal-function measure each rule requires. The examined projects do not establish this complete coverage.",<br>  "A pharmacist-labelled gold-standard test set covering dangerous and harmless prescriptions, duplicate ingredients, ambiguous brands, boundary doses and missing patient information, with measured false-negative and false-positive rates.",<br>  "An integrated alert policy and workflow: evidence provenance, severity prioritization, duplicate-warning grouping, override reasons and usability testing. None of the examined components establishes that the proposed alert-fatigue reduction is clinically effective."<br>] | 🟢 [<br>  "Gitee"<br>] | 🟡 [<br>  {<br>    "usable_now": "yes",<br>    "license": "MIT",<br>    "size": "253,973 medicines, as reported by the repository",<br>    "url": "https://github.com/junioralive/Indian-Medicine-Dataset",<br>    "name": "Indian Medicine Dataset"<br>  },<br>  {<br>    "usable_now": "yes",<br>    "license": "unknown",<br>    "size": "302,516 DDI associations across 2,290 approved drugs; database scope, not a verified count of the downloadable CSV subset",<br>    "url": "https://ddinter2.scbdd.com/download",<br>    "name": "DDInter 2.0"<br>  }<br>] |

## Basis Information

### Basis for Index 0

```json
[
  {
    "field": "best_fork_candidates",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "Description: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" - clovaai/aasist License: MIT license"
        ]
      },
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "Our experiments are performed on the logical access (LA) and deepfake (DF) partition of the ASVspoof 2021 dataset (train on 2019 LA training and evaluate on 2021 LA and DF evaluation database)."
        ]
      },
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      },
      {
        "title": "api.github.com",
        "url": "https://api.github.com/repos/clovaai/aasist",
        "excerpts": [
          "\"milestones_url\": \"https://api.github.com/repos/clovaai/aasist/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/clovaai/aasist/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/clovaai/aasist/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/clovaai/aasist/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/clovaai/aasist/deployments\", \"created_at\": \"2021-10-12T06:49:59Z\", \"updated_at\": \"2026-10-19T08:49:02Z\", \"pushed_at\": \"2023-06-25T13:15:51Z\", \"git_url\": \"git://github.com/clovaai/aasist.git\", \"ssh_url\": \"git@github.com:clovaai/aasist.git\", \"clone_url\": \"https://github.com/clovaai/aasist.git\", \"svn_url\": \"https://github.com/clovaai/aasist\", \"homepage\": null, \"size\": 1455, \"stargazers_count\": 308, \"watchers_count\": 308, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 84, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 4, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      },
      {
        "title": "Ssl Anti Spoofing",
        "url": "https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "\"compare_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/compare/{base}...{head}\", \"merges_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/merges\", \"archive_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/{archive_format}{/ref}\", \"downloads_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/downloads\", \"issues_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/issues{/number}\", \"pulls_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/pulls{/number}\", \"milestones_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/deployments\", \"created_at\": \"2022-04-28T12:12:21Z\", \"updated_at\": \"2026-10-18T15:54:17Z\", \"pushed_at\": \"2023-09-26T04:35:06Z\", \"git_url\": \"git://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"ssh_url\": \"git@github.com:TakHemlata/SSL_Anti-spoofing.git\", \"clone_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"svn_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing\", \"homepage\": \"\", \"size\": 31307, \"stargazers_count\": 184, \"watchers_count\": 184, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 42, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 2, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      }
    ],
    "reasoning": "Official repositories establish the detector implementations and benchmark scope; repository metadata supplies the observed stars and update dates. Browser interfaces and CPU wrappers are proposed adaptations, not existing verified browser applications.",
    "confidence": "medium"
  },
  {
    "field": "models_weights",
    "citations": [
      {
        "title": "aasist/models/weights/AASIST-L.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST-L.pth",
        "excerpts": [
          "416 KB"
        ]
      },
      {
        "title": "aasist/models/weights/AASIST.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST.pth",
        "excerpts": [
          "1\\.22 MB"
        ]
      },
      {
        "title": "Pre_trained_SSL_anti-spoofing_models - Google Drive",
        "url": "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",
        "excerpts": [
          "|**Best\\_LA\\_model\\_for\\_DF.pth** Shared |Owner hidden |Dec 26, 2021 |1\\.18 GB |Download |"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/main_SSL_DF.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",
        "excerpts": [
          "#GPU device device = 'cuda' if torch.cuda.is_available() else 'cpu' print('Device: {}'.format(device))"
        ]
      }
    ],
    "reasoning": "Weight-file pages and the linked Drive folder identify the downloadable checkpoints and displayed sizes. CPU suitability is qualified: SSL has a CPU fallback, while AASIST requires an adapted entry point. Neither browser execution nor latency was demonstrated.",
    "confidence": "medium"
  },
  {
    "field": "id",
    "citations": [],
    "reasoning": "AI-01 is supplied explicitly in the user's input.",
    "confidence": "high"
  },
  {
    "field": "mind_boggling_demo_angles",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "We provide pre-trained AASIST and AASIST-L."
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "The dataset is intended to be used for evaluating deepfake detection and voice anti-spoofing machine-learning models. It is especially useful to judge a model's capability to generalize to realistic, in-the-wild audio samples."
        ]
      },
      {
        "title": "SSL_Anti-spoofing/data_utils_SSL.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/data_utils_SSL.py",
        "excerpts": [
          "self.list_IDs = list_IDs self.base_dir = base_dir self.cut=64600 # take ~4 sec audio (64600 samples)"
        ]
      }
    ],
    "reasoning": "These are explicitly proposed demo concepts built around available pretrained detectors, a generalization dataset and short-window preprocessing. The sources support the components, not a claim that these interfaces or robust outcomes already exist.",
    "confidence": "medium"
  },
  {
    "field": "sources",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "clovaai/aasist"
        ]
      },
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "URL: https://github.com/TakHemlata/SSL_Anti-spoofing"
        ]
      },
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "<https://doi.org/10.7488/ds/2555> [Download all files](https://datashare.ed.ac.uk/download/DS_10283_3336.zip?v=b53f0668f3b17ce72535fb60cac78923)"
        ]
      }
    ],
    "reasoning": "The list contains the repository, code, metadata, checkpoint, dataset and regional catalogue pages used for the reported findings. Individual source entries are grounded below.",
    "confidence": "high"
  },
  {
    "field": "risks",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "Full descriptions are available in the ASVspoof 2019 evaluation plan. ## Codec ## The original waveform format is PCM and compressed using Flac. No telephone or mobile codec was used."
        ]
      },
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "This dataset and the associated documentation are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) ."
        ]
      },
      {
        "title": "mueller91/In-The-Wild · Datasets at Hugging Face",
        "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",
        "excerpts": [
          "License: cc-by-sa-4.0"
        ]
      }
    ],
    "reasoning": "The source material directly establishes a telephone-codec domain gap, an AASIST CPU entry-point blocker and contradictory dataset licensing. Performance, privacy and misuse implications are deployment assessments rather than measured findings.",
    "confidence": "medium"
  },
  {
    "field": "missing_pieces",
    "citations": [
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "file_eval = genSpoof_list(dir_meta=eval_trial_path, is_train=False, is_eval=True) eval_set = Dataset_ASVspoof2019_devNeval(list_IDs=file_eval, base_dir=eval_database_path) eval_loader = DataLoader(eval_set, batch_size=config[\"batch_size\"], shuffle=False, drop_last=False, pin_memory=True)"
        ]
      },
      {
        "title": "aasist/data_utils.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/data_utils.py",
        "excerpts": [
          "def pad(x, max_len=64600): x_len = x.shape[0] if x_len >= max_len: return x[:max_len] need to pad num_repeats = int(max_len / x_len) + 1 padded_x = np.tile(x, (1, num_repeats))[:, :max_len][0] return padded_x"
        ]
      },
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "Our experiments are performed on the logical access (LA) and deepfake (DF) partition of the ASVspoof 2021 dataset (train on 2019 LA training and evaluate on 2021 LA and DF evaluation database)."
        ]
      }
    ],
    "reasoning": "The supplied code uses dataset-oriented evaluators and fixed-length preprocessing. Missing browser packaging and short-clip, phone-channel validation are limited to what was established for the shortlisted projects, not asserted as absent from every project worldwide.",
    "confidence": "medium"
  },
  {
    "field": "regional_sources_checked",
    "citations": [
      {
        "title": "数据集 - ModelScope 魔搭社区",
        "url": "https://www.modelscope.cn/datasets",
        "excerpts": [
          "[](https://www.modelscope.cn/)",
          "audio"
        ]
      }
    ],
    "reasoning": "The examined ModelScope catalogue exposes audio categories but did not establish a relevant downloadable detector. No successful Gitee examination is claimed.",
    "confidence": "medium"
  },
  {
    "field": "datasets",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "[asvspoof2019\\_evaluation\\_plan.pdf (5.81 MB)](https://datashare.ed.ac.uk/bitstreams/8dd50200-9778-4eae-863b-f6f3bfc21983/download) [asvspoof2019\\_Interspeech2019\\_submission.pdf (982.06 KB)](https://datashare.ed.ac.uk/bitstreams/bed1c1fb-5430-41c6-944e-9e079e61f5af/download) [LA.zip (7.12 GB)](https://datashare.ed.ac.uk/bitstreams/a9f87c35-f055-4015-80e2-2fdff0d46269/download) [PA.zip (16.45 GB)](https://datashare.ed.ac.uk/bitstreams/852ec9ad-fe51-48e7-93bd-5259b94e25d6/download) [README.txt (12.83 KB)](https://datashare.ed.ac.uk/bitstreams/765597d6-633f-418a-96b0-39274a8d56c9/download) [LICENSE\\_text.txt (19.47 KB)](https://datashare.ed.ac.uk/bitstreams/60c7de6d-37d3-45c1-b52e-9f18b0338e47/download) ## Licences"
        ]
      },
      {
        "title": "mueller91/In-The-Wild · Datasets at Hugging Face",
        "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",
        "excerpts": [
          "**Size:** 37\\.9 hours total 17\\.2 hours fake 20\\.7 hours real"
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "This dataset and the associated documentation are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) ."
        ]
      }
    ],
    "reasoning": "Official DataShare lists the LA archive and size. The In-the-Wild hosting card provides its size and download instructions; its license conflicts with the project's declaration, so the answer does not select a definitive license.",
    "confidence": "medium"
  },
  {
    "field": "best_fork_candidates.0",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "Description: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" - clovaai/aasist License: MIT license",
          "We train/validate/evaluate AASIST using the ASVspoof 2019 logical access dataset [4].",
          "We provide pre-trained AASIST and AASIST-L."
        ]
      },
      {
        "title": "api.github.com",
        "url": "https://api.github.com/repos/clovaai/aasist",
        "excerpts": [
          "\"milestones_url\": \"https://api.github.com/repos/clovaai/aasist/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/clovaai/aasist/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/clovaai/aasist/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/clovaai/aasist/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/clovaai/aasist/deployments\", \"created_at\": \"2021-10-12T06:49:59Z\", \"updated_at\": \"2026-10-19T08:49:02Z\", \"pushed_at\": \"2023-06-25T13:15:51Z\", \"git_url\": \"git://github.com/clovaai/aasist.git\", \"ssh_url\": \"git@github.com:clovaai/aasist.git\", \"clone_url\": \"https://github.com/clovaai/aasist.git\", \"svn_url\": \"https://github.com/clovaai/aasist\", \"homepage\": null, \"size\": 1455, \"stargazers_count\": 308, \"watchers_count\": 308, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 84, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 4, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      },
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      }
    ],
    "reasoning": "These establish the official AASIST implementation, MIT licensing, pretrained alternatives, ASVspoof 2019 evaluation, observed metadata and the CPU-blocking entry-point guard. The fork instructions are an engineering recommendation.",
    "confidence": "medium"
  },
  {
    "field": "best_fork_candidates.1",
    "citations": [
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "TakHemlata/SSL_Anti-spoofing",
          "License: MIT license",
          "Our experiments are performed on the logical access (LA) and deepfake (DF) partition of the ASVspoof 2021 dataset (train on 2019 LA training and evaluate on 2021 LA and DF evaluation database)."
        ]
      },
      {
        "title": "SSL_Anti-spoofing/model.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/model.py",
        "excerpts": [
          "cp_path = 'xlsr2_300m.pt' # Change the pre-trained XLSR model path. model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([cp_path]) self.model = model[0] self.device=device self.out_dim = 1024 return"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/main_SSL_DF.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",
        "excerpts": [
          "#GPU device device = 'cuda' if torch.cuda.is_available() else 'cpu' print('Device: {}'.format(device)) model = Model(args,device) nb_params = sum([param.view(-1).size()[0] for param in model.parameters()]) model =nn.DataParallel(model).to(device) print('nb_params:',nb_params)"
        ]
      },
      {
        "title": "Ssl Anti Spoofing",
        "url": "https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "\"compare_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/compare/{base}...{head}\", \"merges_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/merges\", \"archive_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/{archive_format}{/ref}\", \"downloads_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/downloads\", \"issues_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/issues{/number}\", \"pulls_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/pulls{/number}\", \"milestones_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/deployments\", \"created_at\": \"2022-04-28T12:12:21Z\", \"updated_at\": \"2026-10-18T15:54:17Z\", \"pushed_at\": \"2023-09-26T04:35:06Z\", \"git_url\": \"git://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"ssh_url\": \"git@github.com:TakHemlata/SSL_Anti-spoofing.git\", \"clone_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"svn_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing\", \"homepage\": \"\", \"size\": 31307, \"stargazers_count\": 184, \"watchers_count\": 184, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 42, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 2, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      }
    ],
    "reasoning": "The official repository and implementation identify the SSL detector, its benchmark scope, wav2vec frontend and CPU/device handling. Metadata supplies stars and update date; browser deployment remains a proposed backend wrapper.",
    "confidence": "medium"
  },
  {
    "field": "models_weights.0",
    "citations": [
      {
        "title": "aasist/models/weights/AASIST-L.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST-L.pth",
        "excerpts": [
          "AASIST-L.pth",
          "416 KB"
        ]
      },
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "License: MIT license"
        ]
      },
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      }
    ],
    "reasoning": "The file page identifies the lightweight checkpoint and size. MIT is the repository license rather than independently established weight terms; CPU execution requires replacing the supplied GPU-only entry point and remains untested.",
    "confidence": "medium"
  },
  {
    "field": "models_weights.1",
    "citations": [
      {
        "title": "aasist/models/weights/AASIST.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST.pth",
        "excerpts": [
          "AASIST.pth",
          "1\\.22 MB"
        ]
      },
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "License: MIT license"
        ]
      },
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      }
    ],
    "reasoning": "The file page supplies the checkpoint identity and size. Repository licensing is distinguished from separate weight terms, and CPU support is an adaptation assessment rather than a verified runtime result.",
    "confidence": "medium"
  },
  {
    "field": "models_weights.2",
    "citations": [
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "Pre-trained SSL antispoofing models are available for LA and DF [here](https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing)"
        ]
      },
      {
        "title": "Pre_trained_SSL_anti-spoofing_models - Google Drive",
        "url": "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",
        "excerpts": [
          "|**Best\\_LA\\_model\\_for\\_DF.pth**"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/main_SSL_DF.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",
        "excerpts": [
          "#GPU device device = 'cuda' if torch.cuda.is_available() else 'cpu' print('Device: {}'.format(device))"
        ]
      }
    ],
    "reasoning": "The repository links the pretrained folder, which lists the named DF checkpoint at 1.18 GB. The script has a CPU fallback, but the weight license and practical runtime were not established.",
    "confidence": "medium"
  },
  {
    "field": "mind_boggling_demo_angles.0",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "We provide pre-trained AASIST and AASIST-L."
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "For n = 58 celebrities and politicians, we collect both bona-fide and spoofed audio."
        ]
      }
    ],
    "reasoning": "Available detectors and genuine/spoofed recordings support a proposed blind listening comparison. The browser game and safeguards are proposed features.",
    "confidence": "medium"
  },
  {
    "field": "mind_boggling_demo_angles.1",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "Full descriptions are available in the ASVspoof 2019 evaluation plan. ## Codec ## The original waveform format is PCM and compressed using Flac. No telephone or mobile codec was used."
        ]
      },
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "We provide pre-trained AASIST and AASIST-L."
        ]
      }
    ],
    "reasoning": "The absence of telephone codecs in the benchmark motivates a proposed channel stress test using the available models. No robustness outcome is promised.",
    "confidence": "medium"
  },
  {
    "field": "mind_boggling_demo_angles.2",
    "citations": [
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "It is especially useful to judge a model's capability to generalize to realistic, in-the-wild audio samples."
        ]
      },
      {
        "title": "SSL_Anti-spoofing/data_utils_SSL.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/data_utils_SSL.py",
        "excerpts": [
          "self.list_IDs = list_IDs self.base_dir = base_dir self.cut=64600 # take ~4 sec audio (64600 samples)"
        ]
      }
    ],
    "reasoning": "In-the-Wild is explicitly intended to assess generalization, while fixed-duration preprocessing motivates examining evidence length. Held-out tool testing, the interface and uncertainty policy are proposals.",
    "confidence": "medium"
  },
  {
    "field": "risks.0",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "Full descriptions are available in the ASVspoof 2019 evaluation plan. ## Codec ## The original waveform format is PCM and compressed using Flac. No telephone or mobile codec was used."
        ]
      },
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "Our experiments are performed on the logical access (LA) and deepfake (DF) partition of the ASVspoof 2021 dataset (train on 2019 LA training and evaluate on 2021 LA and DF evaluation database)."
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "It is especially useful to judge a model's capability to generalize to realistic, in-the-wild audio samples."
        ]
      }
    ],
    "reasoning": "Benchmark scope and the explicit telephone-codec gap justify caution about unseen tools and real calls. Distinguishing synthesis from scam intent is a limitation of the requested binary task, not a measured benchmark result.",
    "confidence": "medium"
  },
  {
    "field": "risks.1",
    "citations": [
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      },
      {
        "title": "Pre_trained_SSL_anti-spoofing_models - Google Drive",
        "url": "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",
        "excerpts": [
          "|**Best\\_LA\\_model\\_for\\_DF.pth**"
        ]
      }
    ],
    "reasoning": "The CPU guard and large SSL checkpoint directly establish deployment concerns. Latency, memory and sensitive-audio retention are prospective risks requiring testing and design safeguards.",
    "confidence": "medium"
  },
  {
    "field": "risks.2",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "License: MIT license"
        ]
      },
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "License: MIT license"
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "This dataset and the associated documentation are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) ."
        ]
      },
      {
        "title": "mueller91/In-The-Wild · Datasets at Hugging Face",
        "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",
        "excerpts": [
          "License: cc-by-sa-4.0"
        ]
      }
    ],
    "reasoning": "The code licenses are explicit, but they do not independently resolve externally hosted checkpoint terms. In-the-Wild's project and hosting pages explicitly disagree on licensing.",
    "confidence": "medium"
  },
  {
    "field": "missing_pieces.0",
    "citations": [
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "file_eval = genSpoof_list(dir_meta=eval_trial_path, is_train=False, is_eval=True) eval_set = Dataset_ASVspoof2019_devNeval(list_IDs=file_eval, base_dir=eval_database_path) eval_loader = DataLoader(eval_set, batch_size=config[\"batch_size\"], shuffle=False, drop_last=False, pin_memory=True)"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/main_SSL_DF.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",
        "excerpts": [
          "#GPU device device = 'cuda' if torch.cuda.is_available() else 'cpu' print('Device: {}'.format(device))"
        ]
      }
    ],
    "reasoning": "The evaluated entry points are dataset-oriented Python scripts. A polished browser-facing single-clip service was not established for these repositories.",
    "confidence": "medium"
  },
  {
    "field": "missing_pieces.1",
    "citations": [
      {
        "title": "aasist/models/weights at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/tree/main/models/weights",
        "excerpts": [
          "Contents AASIST-L.pth AASIST.pth"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/model.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/model.py",
        "excerpts": [
          "cp_path = 'xlsr2_300m.pt' # Change the pre-trained XLSR model path. model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([cp_path]) self.model = model[0] self.device=device self.out_dim = 1024 return"
        ]
      }
    ],
    "reasoning": "The established artifacts are PyTorch/Fairseq checkpoints, not verified browser packages. Export and browser compatibility testing are recommendations, not claims of universal incompatibility.",
    "confidence": "medium"
  },
  {
    "field": "missing_pieces.2",
    "citations": [
      {
        "title": "aasist/data_utils.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/data_utils.py",
        "excerpts": [
          "def pad(x, max_len=64600): x_len = x.shape[0] if x_len >= max_len: return x[:max_len]"
        ]
      },
      {
        "title": "SSL_Anti-spoofing/data_utils_SSL.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/data_utils_SSL.py",
        "excerpts": [
          "self.list_IDs = list_IDs self.base_dir = base_dir self.cut=64600 # take ~4 sec audio (64600 samples)"
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "It is especially useful to judge a model's capability to generalize to realistic, in-the-wild audio samples."
        ]
      }
    ],
    "reasoning": "Fixed approximately four-second preprocessing and the separate generalization benchmark motivate explicit short-duration testing. The proposed phone-channel and held-out-tool protocol was not supplied as a verified result.",
    "confidence": "medium"
  },
  {
    "field": "regional_sources_checked.0",
    "citations": [
      {
        "title": "数据集 - ModelScope 魔搭社区",
        "url": "https://www.modelscope.cn/datasets",
        "excerpts": [
          "[](https://www.modelscope.cn/)",
          "audio"
        ]
      }
    ],
    "reasoning": "ModelScope's audio dataset catalogue was examined, without establishing a relevant downloadable detector.",
    "confidence": "medium"
  },
  {
    "field": "datasets.0",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "[asvspoof2019\\_evaluation\\_plan.pdf (5.81 MB)](https://datashare.ed.ac.uk/bitstreams/8dd50200-9778-4eae-863b-f6f3bfc21983/download) [asvspoof2019\\_Interspeech2019\\_submission.pdf (982.06 KB)](https://datashare.ed.ac.uk/bitstreams/bed1c1fb-5430-41c6-944e-9e079e61f5af/download) [LA.zip (7.12 GB)](https://datashare.ed.ac.uk/bitstreams/a9f87c35-f055-4015-80e2-2fdff0d46269/download) [PA.zip (16.45 GB)](https://datashare.ed.ac.uk/bitstreams/852ec9ad-fe51-48e7-93bd-5259b94e25d6/download) [README.txt (12.83 KB)](https://datashare.ed.ac.uk/bitstreams/765597d6-633f-418a-96b0-39274a8d56c9/download) [LICENSE\\_text.txt (19.47 KB)](https://datashare.ed.ac.uk/bitstreams/60c7de6d-37d3-45c1-b52e-9f18b0338e47/download) ## Licences"
        ]
      },
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://doi.org/10.7488/ds/2555",
        "excerpts": [
          "asvspoof2019\\_evaluation\\_plan.pdf (5.81 MB) asvspoof2019\\_Interspeech2019\\_submission.pdf (982.06 KB) LA.zip (7.12 GB) PA.zip (16.45 GB) README.txt (12.83 KB) LICENSE\\_text.txt (19.47 KB) ## Licences"
        ]
      }
    ],
    "reasoning": "The official record exposes LA.zip at 7.12 GB and a download link. A license file is listed, but its contents were not recovered, so the license remains unknown.",
    "confidence": "medium"
  },
  {
    "field": "datasets.1",
    "citations": [
      {
        "title": "mueller91/In-The-Wild · Datasets at Hugging Face",
        "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",
        "excerpts": [
          "**Size:** 37\\.9 hours total 17\\.2 hours fake 20\\.7 hours real",
          "Download You can download the full dataset as a single ZIP file directly from this repository or via the Hugging Face `datasets` library.",
          "License: cc-by-sa-4.0"
        ]
      },
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "For n = 58 celebrities and politicians, we collect both bona-fide and spoofed audio.",
          "This dataset and the associated documentation are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) ."
        ]
      }
    ],
    "reasoning": "The hosting card reports 37.9 hours and a downloadable ZIP, while the project confirms 58 subjects. Conflicting license declarations prevent a definitive license assignment.",
    "confidence": "medium"
  },
  {
    "field": "sources.0",
    "citations": [
      {
        "title": "GitHub - clovaai/aasist: Official PyTorch implementation of \"AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks\" · GitHub",
        "url": "https://github.com/clovaai/aasist",
        "excerpts": [
          "clovaai/aasist"
        ]
      }
    ],
    "reasoning": "Official AASIST repository source.",
    "confidence": "high"
  },
  {
    "field": "sources.1",
    "citations": [
      {
        "title": "api.github.com",
        "url": "https://api.github.com/repos/clovaai/aasist",
        "excerpts": [
          "\"milestones_url\": \"https://api.github.com/repos/clovaai/aasist/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/clovaai/aasist/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/clovaai/aasist/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/clovaai/aasist/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/clovaai/aasist/deployments\", \"created_at\": \"2021-10-12T06:49:59Z\", \"updated_at\": \"2026-10-19T08:49:02Z\", \"pushed_at\": \"2023-06-25T13:15:51Z\", \"git_url\": \"git://github.com/clovaai/aasist.git\", \"ssh_url\": \"git@github.com:clovaai/aasist.git\", \"clone_url\": \"https://github.com/clovaai/aasist.git\", \"svn_url\": \"https://github.com/clovaai/aasist\", \"homepage\": null, \"size\": 1455, \"stargazers_count\": 308, \"watchers_count\": 308, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 84, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 4, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      }
    ],
    "reasoning": "AASIST repository metadata source.",
    "confidence": "high"
  },
  {
    "field": "sources.2",
    "citations": [
      {
        "title": "aasist/main.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/main.py",
        "excerpts": [
          "device = \"cuda\" if torch.cuda.is_available() else \"cpu\" print(\"Device: {}\".format(device)) if device == \"cpu\": raise ValueError(\"GPU not detected!\")"
        ]
      }
    ],
    "reasoning": "AASIST entry-point code source.",
    "confidence": "high"
  },
  {
    "field": "sources.3",
    "citations": [
      {
        "title": "aasist/models/AASIST.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/AASIST.py",
        "excerpts": [
          "URL: https://github.com/clovaai/aasist/blob/main/models/AASIST.py"
        ]
      }
    ],
    "reasoning": "AASIST architecture code source.",
    "confidence": "high"
  },
  {
    "field": "sources.4",
    "citations": [
      {
        "title": "aasist/data_utils.py at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/data_utils.py",
        "excerpts": [
          "URL: https://github.com/clovaai/aasist/blob/main/data_utils.py"
        ]
      }
    ],
    "reasoning": "AASIST preprocessing code source.",
    "confidence": "high"
  },
  {
    "field": "sources.5",
    "citations": [
      {
        "title": "aasist/NOTICE at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/NOTICE",
        "excerpts": [
          "URL: https://github.com/clovaai/aasist/blob/main/NOTICE"
        ]
      }
    ],
    "reasoning": "AASIST license-notice source.",
    "confidence": "high"
  },
  {
    "field": "sources.6",
    "citations": [
      {
        "title": "aasist/models/weights at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/tree/main/models/weights",
        "excerpts": [
          "URL: https://github.com/clovaai/aasist/tree/main/models/weights"
        ]
      }
    ],
    "reasoning": "AASIST checkpoint-directory source.",
    "confidence": "high"
  },
  {
    "field": "sources.7",
    "citations": [
      {
        "title": "aasist/models/weights/AASIST-L.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST-L.pth",
        "excerpts": [
          "AASIST-L.pth"
        ]
      }
    ],
    "reasoning": "AASIST-L checkpoint-file source.",
    "confidence": "high"
  },
  {
    "field": "sources.8",
    "citations": [
      {
        "title": "aasist/models/weights/AASIST.pth at main · clovaai/aasist · GitHub",
        "url": "https://github.com/clovaai/aasist/blob/main/models/weights/AASIST.pth",
        "excerpts": [
          "AASIST.pth"
        ]
      }
    ],
    "reasoning": "AASIST checkpoint-file source.",
    "confidence": "high"
  },
  {
    "field": "sources.9",
    "citations": [
      {
        "title": "GitHub - TakHemlata/SSL_Anti-spoofing: This repository includes the code to reproduce our paper \"Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation\". · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "URL: https://github.com/TakHemlata/SSL_Anti-spoofing"
        ]
      }
    ],
    "reasoning": "Official SSL anti-spoofing repository source.",
    "confidence": "high"
  },
  {
    "field": "sources.10",
    "citations": [
      {
        "title": "Ssl Anti Spoofing",
        "url": "https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing",
        "excerpts": [
          "\"compare_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/compare/{base}...{head}\", \"merges_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/merges\", \"archive_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/{archive_format}{/ref}\", \"downloads_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/downloads\", \"issues_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/issues{/number}\", \"pulls_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/pulls{/number}\", \"milestones_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/milestones{/number}\", \"notifications_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/notifications{?since,all,participating}\", \"labels_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/labels{/name}\", \"releases_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/releases{/id}\", \"deployments_url\": \"https://api.github.com/repos/TakHemlata/SSL_Anti-spoofing/deployments\", \"created_at\": \"2022-04-28T12:12:21Z\", \"updated_at\": \"2026-10-18T15:54:17Z\", \"pushed_at\": \"2023-09-26T04:35:06Z\", \"git_url\": \"git://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"ssh_url\": \"git@github.com:TakHemlata/SSL_Anti-spoofing.git\", \"clone_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing.git\", \"svn_url\": \"https://github.com/TakHemlata/SSL_Anti-spoofing\", \"homepage\": \"\", \"size\": 31307, \"stargazers_count\": 184, \"watchers_count\": 184, \"language\": \"Python\", \"has_issues\": true, \"has_projects\": true, \"has_downloads\": false, \"has_wiki\": true, \"has_pages\": false, \"has_discussions\": false, \"forks_count\": 42, \"mirror_url\": null, \"archived\": false, \"disabled\": false, \"open_issues_count\": 2, \"license\": { \"key\": \"mit\", \"name\": \"MIT License\", \"spdx_id\": \"MIT\", \"url\": \"https://api.github.com/licenses/mit\", \"node_id\": \"MDc6TGljZW5zZTEz\" }, \"allow_forking\": true, \"is_template\": false, \"web_commit_signoff_required\": false, \"has_pull_requests\": true, \"pull_request_creation_policy\": \"all\", \"topics\": ["
        ]
      }
    ],
    "reasoning": "SSL repository metadata source.",
    "confidence": "high"
  },
  {
    "field": "sources.11",
    "citations": [
      {
        "title": "SSL_Anti-spoofing/model.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/model.py",
        "excerpts": [
          "URL: https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/model.py"
        ]
      }
    ],
    "reasoning": "SSL architecture and frontend code source.",
    "confidence": "high"
  },
  {
    "field": "sources.12",
    "citations": [
      {
        "title": "SSL_Anti-spoofing/main_SSL_DF.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/main_SSL_DF.py",
        "excerpts": [
          "#GPU device device = 'cuda' if torch.cuda.is_available() else 'cpu' print('Device: {}'.format(device))"
        ]
      }
    ],
    "reasoning": "SSL inference/device-handling code source.",
    "confidence": "high"
  },
  {
    "field": "sources.13",
    "citations": [
      {
        "title": "SSL_Anti-spoofing/data_utils_SSL.py at main · TakHemlata/SSL_Anti-spoofing · GitHub",
        "url": "https://github.com/TakHemlata/SSL_Anti-spoofing/blob/main/data_utils_SSL.py",
        "excerpts": [
          "utt_id = self.list_IDs[index] X, fs = librosa.load(self.base_dir+'flac/'+utt_id+'.flac', sr=16000) X_pad = pad(X,self.cut) x_inp = Tensor(X_pad) return x_inp,utt_id"
        ]
      }
    ],
    "reasoning": "SSL sampling and preprocessing code source.",
    "confidence": "high"
  },
  {
    "field": "sources.14",
    "citations": [
      {
        "title": "Pre_trained_SSL_anti-spoofing_models - Google Drive",
        "url": "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing",
        "excerpts": [
          "|**Best\\_LA\\_model\\_for\\_DF.pth**"
        ]
      }
    ],
    "reasoning": "Linked pretrained SSL weight-folder source.",
    "confidence": "high"
  },
  {
    "field": "sources.15",
    "citations": [
      {
        "title": " | ASVspoof",
        "url": "https://www.asvspoof.org/index2019.html",
        "excerpts": [
          "**5th June: Database Release via [Edinburgh DataShare](https://doi.org/10.7488/ds/2555) .**"
        ]
      }
    ],
    "reasoning": "Official ASVspoof 2019 page linking the dataset release.",
    "confidence": "high"
  },
  {
    "field": "sources.16",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://datashare.ed.ac.uk/handle/10283/3336",
        "excerpts": [
          "[asvspoof2019\\_evaluation\\_plan.pdf (5.81 MB)](https://datashare.ed.ac.uk/bitstreams/8dd50200-9778-4eae-863b-f6f3bfc21983/download) [asvspoof2019\\_Interspeech2019\\_submission.pdf (982.06 KB)](https://datashare.ed.ac.uk/bitstreams/bed1c1fb-5430-41c6-944e-9e079e61f5af/download) [LA.zip (7.12 GB)](https://datashare.ed.ac.uk/bitstreams/a9f87c35-f055-4015-80e2-2fdff0d46269/download) [PA.zip (16.45 GB)](https://datashare.ed.ac.uk/bitstreams/852ec9ad-fe51-48e7-93bd-5259b94e25d6/download) [README.txt (12.83 KB)](https://datashare.ed.ac.uk/bitstreams/765597d6-633f-418a-96b0-39274a8d56c9/download) [LICENSE\\_text.txt (19.47 KB)](https://datashare.ed.ac.uk/bitstreams/60c7de6d-37d3-45c1-b52e-9f18b0338e47/download) ## Licences"
        ]
      }
    ],
    "reasoning": "Official DataShare dataset and file-list source.",
    "confidence": "high"
  },
  {
    "field": "sources.17",
    "citations": [
      {
        "title": "ASVspoof 2019: The 3rd Automatic Speaker Verification Spoofing and Countermeasures Challenge database",
        "url": "https://doi.org/10.7488/ds/2555",
        "excerpts": [
          "<https://doi.org/10.7488/ds/2555>"
        ]
      }
    ],
    "reasoning": "Dataset DOI record read during research.",
    "confidence": "high"
  },
  {
    "field": "sources.18",
    "citations": [
      {
        "title": "\n   In-the-Wild Dataset\n  ",
        "url": "https://deepfake-total.com/in_the_wild",
        "excerpts": [
          "'In-the-Wild' Dataset"
        ]
      }
    ],
    "reasoning": "In-the-Wild project-page source.",
    "confidence": "high"
  },
  {
    "field": "sources.19",
    "citations": [
      {
        "title": "mueller91/In-The-Wild · Datasets at Hugging Face",
        "url": "https://huggingface.co/datasets/mueller91/In-The-Wild",
        "excerpts": [
          "Download You can download the full dataset as a single ZIP file directly from this repository or via the Hugging Face `datasets` library."
        ]
      }
    ],
    "reasoning": "In-the-Wild hosting-card and download source.",
    "confidence": "high"
  },
  {
    "field": "sources.20",
    "citations": [
      {
        "title": "数据集 - ModelScope 魔搭社区",
        "url": "https://www.modelscope.cn/datasets",
        "excerpts": [
          "[](https://www.modelscope.cn/)"
        ]
      }
    ],
    "reasoning": "Regional dataset catalogue examined.",
    "confidence": "high"
  }
]
```

