<!-- run id: trun_3b693d434bb94e6d84c17b91b1cf5539 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6d84c17b91b1cf5539
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:10.546289Z
**Modified:** 2026-10-24T09:05:11.206679Z

## Output

# Build a Verifiable Small-Model Analyst for Messy Databases

## Executive Summary

- **Best Low-Memory Starting Point**: XiYanSQL-QwenCoder-3B-2504 reports **55.08% BIRD dev execution accuracy with M-Schema**, versus **52.09% with DDL**. Start here for a constrained demo, then add exploration and deterministic checks rather than building a SQL model from scratch. [44]
- **Stronger Hosted-GPU Candidates**: OmniSQL-7B reports **63.9% BIRD dev**; Arctic-Text2SQL-R1-7B reports **68.9% dev**. These are author-reported results, not results reproduced for this report. Benchmark both before choosing the final generator. [40][43]
- **Schema Representation Is A Real Lever**: XiYan's 7B-2504 result changes from **57.43% with DDL to 62.13% with M-Schema**, without changing the advertised model size. Spend hackathon time on schema selection, relationships, values, and business context, not just prompting. [41]
- **Abstention Already Has Reusable Precedents**: TrustSQL explicitly distinguishes answerable questions from infeasible ones and includes small-model paths using **T5-3B and SQLCoder-7B-2**. Borrow its decision structure, but replace any default proprietary classifiers. [29]
- **A Popular Repository Can Still Be A Maintenance Risk**: Vanna's retrieved repository metadata shows **23,816 stars**, a last push on **2026-02-02**, and **archived status**. Its retrieval, permissions, and presentation ideas remain useful, but do not assume active upstream maintenance. [66]
- **Four Gigabytes Is Not Seven-Billion-Parameter Comfort**: At four bits per parameter, nominal 7B weights alone occupy approximately **3.5 GB**, before context and runtime memory. Treat 3B as the practical first experiment for a 4 GB GPU; use CPU offload or hosted inference for larger models. These are memory estimates, not measured deployment results.
- **Leaderboard Scores Do Not Transfer With Code**: CHASE-SQL's reported **73.01% dev / 73.0% test** uses Gemini 1.5 Pro. ReFoRCE's cited enterprise-workflow results use o3. Their ideas are relevant; those implementations and scores are not automatically eligible under the open-weight <=8B rule. [105][106]
- **Build Two Success Criteria**: Optimize BIRD execution accuracy on its prescribed questions, but separately demonstrate dirty-data detection, ambiguity handling, permissions, and justified refusal. A query that executes is not, by itself, evidence that it answers the business question correctly.

**Recommended build:** a small SQL-specialist model, a deliberately small exploration/execution interface, a deterministic validation layer, and an explicit answer-or-abstain controller. Use an existing UI only if it does not consume the implementation budget.

This is a broad, actionable catalog of supported candidates and additional leads, not a claim that every repository on the internet has been enumerated. **NR** means the requested fact was not established in the available material; it does not mean zero or nonexistent. Performance figures below are **author or leaderboard claims unless otherwise stated**. Repository stars are retrieved snapshots, not guaranteed live counts on 2026-10-24.

## 1. The Stack To Fork: Small Generator, Observable Execution, Explicit Refusal

### XiYan-3B is the best first experiment for the constrained demo

XiYan's small checkpoints are unusually relevant because the model cards expose a concrete schema-format comparison. The 3B-2504 card reports **55.08% BIRD dev with M-Schema** and **52.09% with DDL**; the 7B-2504 card reports **62.13% and 57.43%**, respectively. The cards recommend the structured schema representation and describe support for SQLite, PostgreSQL, and MySQL. [44][41]

The implication is not that a different serialization guarantees those gains on your database. It is that a small model's inputs matter enough to deserve first-class engineering. For this hackathon, preserve primary keys, foreign keys, grain, sample values, null rates, and plausible join paths instead of sending a giant unfiltered schema.

Use the 3B checkpoint to make the complete loop work locally. Keep OmniSQL-7B and Arctic-7B behind the same generator interface for a second configuration when a larger GPU or sufficient CPU memory is available. OmniSQL's authors report that their model evaluations do not add the full schema-linking, revision, and selection pipeline around the generator, making it a sensible component to combine with an agent rather than a complete messy-database solution by itself. [27]

| Component | Concrete starting point | What it contributes | What you still implement |
|---|---|---|---|
| SQL generator | XiYanSQL-QwenCoder-3B-2504 | Small SQL-specialist checkpoint and M-Schema prompting | Local quantized serving, exact checkpoint pinning, task evaluation |
| Higher-accuracy alternative | OmniSQL-7B or Arctic-Text2SQL-R1-7B | Stronger reported BIRD dev results | Memory provisioning and comparable evaluation |
| Exploration loop | Text2SqlAgent/text2sql-framework | A small execution-centered agent interface; local OpenAI-compatible endpoints | A <=8B tool-capable model, read-only enforcement, bounded retries |
| Repair structure | MAC-SQL or selected CHESS ideas | Separate schema selection, decomposition, and correction | Replace proprietary defaults; keep orchestration inexpensive |
| Refusal controller | TrustSQL-inspired feasibility and error checks | Distinguishes cannot-answer from failed SQL | Domain-specific rules and a local classifier or deterministic policy |
| Validation | Your own SQL and result checks | Row counts, join fanout, value constraints, units, dates, missingness | The actual business semantics |
| Presentation | Existing chat/table UI, or a minimal custom page | Question, SQL, result, warnings, evidence | A truthful explanation tied to the executed result |

The winning integration is likely smaller than a full commercial-style agent platform. The execution-centered framework explicitly supports Ollama/vLLM-compatible endpoints, while MAC-SQL separates Selector, Decomposer, and Refiner roles. Neither fact establishes that the default configuration meets the model restriction. [39][61]

**Decision:** first deliver one complete, auditable question-to-answer path with XiYan-3B. Upgrade the generator only after profiling where the errors occur: schema selection, SQL reasoning, values, or business ambiguity.

## 2. Small SQL Models: Verified Candidates And Unattributed Claims

### Performance inventory

A blank BIRD result must not be filled with a Spider score, a private split, an aggregate across model sizes, or the score of a larger sibling checkpoint.

| Model / canonical URL | Advertised size | Plain-words description | BIRD dev EX | BIRD test EX | Best combination |
|---|---:|---|---:|---:|---|
| **XiYanSQL-QwenCoder-3B-2504** - `https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-3B-2504` | 3B | SQL-tuned Qwen Coder; structured schema prompting | **55.08% M-Schema; 52.09% DDL** | NR | M-Schema, value profiling, deterministic validation [44] |
| **XiYanSQL-QwenCoder-7B-2504** - `https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-7B-2504` | Nominal 7B | Larger sibling for the same SQL workflow | **62.13% M-Schema; 57.43% DDL** | NR | Same agent as the 3B model; swap only the generator [41] |
| **OmniSQL-7B** - `https://huggingface.co/seeklhy/OmniSQL-7B` | Nominal 7B | SQL specialist trained using large-scale synthetic SQL data | **63.9%**, reported greedy result | NR | Schema retrieval, execution repair, candidate validation [40] |
| **Arctic-Text2SQL-R1-7B** - `https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B` | Nominal 7B | Reinforcement-trained SQL reasoning model | **68.9%** | **68.5% on model card; qualification below** | Bounded execution feedback and verifier [43] |
| **CodeS** - `https://github.com/RUCKBReasoning/codes` | **1B, 3B, 7B** eligible siblings; 15B excluded | SQL-focused models and schema-filtering pipeline | NR in captured material | NR | Its 3B schema filter plus another small generator [25] |
| **SQLCoder-7B-2** - `https://huggingface.co/defog/sqlcoder-7b-2` | 7B | Mature SQL-specialist model with local-serving examples | NR | NR | TrustSQL-style feasibility checks; local SQL demo [26] |
| **SQL-R1** - `https://github.com/IDEA-FinAI/SQL-R1` | **3B, 7B** eligible siblings; 14B excluded | Cold-start SQL training followed by reward-driven improvement | NR by eligible checkpoint | NR by eligible checkpoint | Reuse training/reward code, not an unattributed family score [46] |
| **SENSE-7B** - `https://github.com/Yangjiaxi/Sense` | 7B final model; 13B sibling excluded | Learns from strong/weak SQL outputs and preference pairs | NR | NR | Execution-verified preference data and DPO-style training [48] |
| **MTSQL-R1** - `https://github.com/taichengguo/MTSQL-R1` | **1.7B, 4B** | Multi-turn SQL models that propose, execute, verify, and correct | NR; its cited tasks are CoSQL/SPARC | NR | Dialogue handling and correction across turns [45] |
| **Prem-1B-SQL** - `https://huggingface.co/premai-io/prem-1B-SQL` | Nominal 1B | Small local SQL model used with PremSQL | NR for official dev | NR for official test | PremSQL local pipeline; inspect checkpoint license first [58] |
| **xorazm-text2sql-0.8b** - `https://huggingface.co/shakha-de/xorazm-text2sql-0.8b` | 0.8B | Very small SQL-model lead appearing in the official BIRD table | **53.43% in the cited dev entry** | NR | Low-memory baseline; independently reproduce its setup [4] |
| **Llama-3-SQLCoder-8B** - `https://huggingface.co/defog/llama-3-sqlcoder-8b` | Nominal 8B; boundary review required | SQL model targeting PostgreSQL, Redshift, and Snowflake | NR | NR | Local-serving tooling and SQLCoder demo patterns [24] |
| **Llama-3.1-8B-Spider-SQL-Ko** - `https://huggingface.co/huggingface-KREW/Llama-3.1-8B-Spider-SQL-Ko` | Nominal 8B; boundary review required | Korean Spider fine-tune | NR | NR | Korean-language demo branch, not a BIRD replacement [49] |

**Takeaway:** Arctic, OmniSQL, and XiYan are the most immediately useful performance candidates in this catalog. CodeS, SENSE, SQL-R1, and MTSQL-R1 add training or interaction components that can be merged into a stronger system rather than merely swapped into a chat box.

### Important score qualifications

**Arctic's test result needs a label, not silent reconciliation.** Its model card gives 68.5% test for the 7B checkpoint. The paper table captured here reports 68.9% dev for 7B but does not supply the corresponding 7B test result; its larger-model test result must not be reassigned to 7B. Retain the model-card claim with that qualification. [43][14]

**SQL-R1's headline is not a verified 3B/7B score.** The repository advertises 67.1% BIRD and 88.6% Spider, but the captured statement does not attribute that BIRD number to a specific eligible checkpoint and split. Likewise, PremSQL's 51.54% statement describes a "BIRD private dataset"; it is not sufficient to label it official BIRD test EX. [46][58]

**Korean evaluation is a different benchmark.** The KREW card reports 65.47% execution accuracy and 42.65% exact match on its Korean Spider validation set. Those are useful evidence of language specialization, not BIRD results. [49]

### Model licenses, activity, stars, and demos

For model-only entries, GitHub stars are not interchangeable with Hugging Face likes. Dates below are actual captured artifact/repository timestamps where available; paper dates and repository creation dates are not substituted for last updates.

| Model / family | Last update established | License established | GitHub stars established | Public live demo |
|---|---|---|---:|---|
| XiYan 3B/7B-2504 | Family code pushed **2026-10-13**; individual checkpoint update NR | **Apache-2.0 weights**; do not infer model-repository licensing from a missing API field | **160** for the family code repository | **No qualifying small-model demo established**; the advertised ModelScope demo is 32B [64][44][41][5] |
| OmniSQL-7B | Model artifact **2025-03-06**; code pushed **2025-09-08** | **Apache-2.0 model card** | **456** for OmniSQL repository | No hosted demo established; model card showed no inference provider [84][63][1] |
| Arctic-7B | NR | **Apache-2.0** | NR | **Yes, community Space links advertised**; uptime and exact deployed checkpoint not confirmed [43] |
| CodeS | NR | **Apache-2.0 code**; checkpoint/base-weight obligations need separate review | NR | No public hosted demo established; local demo repository exists [25] |
| SQLCoder-7B-2 | NR | **CC-BY-SA-4.0 weights** | NR | **Yes, advertised:** `https://defog.ai/sqlcoder-demo/`; availability not tested [26] |
| SQL-R1 | Last commit NR; dated project news is not a last-commit date | **Apache-2.0 code**; 3B card also states Apache-2.0 | NR | No public hosted demo established [46][86] |
| SENSE | NR | NR | **66** in retrieved repository snapshot | No public hosted demo established [48] |
| MTSQL-R1 | NR | **Apache-2.0 code**; checkpoint license NR | **46** in retrieved snapshot | No public hosted demo established; a GIF is not a live endpoint [45] |
| Prem-1B-SQL | NR | Model license NR; **PremSQL library is MIT** | NR | No public model demo established; local playground exists [58] |
| xorazm-0.8B | NR; BIRD entry date is not checkpoint activity | NR | NR | No public hosted demo established |
| Llama-3-SQLCoder-8B | NR | Card states **CC-BY-SA-4.0**; review upstream base-model terms too | NR | SQLCoder demo advertised [24] |
| KREW Korean SQL-8B | NR | Card states **Apache-2.0**; review upstream Llama terms too | Not applicable to model card | No inference provider shown [49] |

**Takeaway:** license eligibility and runtime eligibility are separate gates. A permissive agent repository does not grant rights to every checkpoint it loads, and a public demo may run a different, oversized model.

### Additional model and training leads worth preserving

These are useful discoveries, but their full qualifying benchmark and deployment metadata were not established:

| Lead / URL | What it offers | What remains unresolved |
|---|---|---|
| **distil-qwen3-4b-text2sql-gguf-4bit** - `https://huggingface.co/distil-labs/distil-qwen3-4b-text2sql-gguf-4bit` | A SQL-named 4B GGUF quantization lead; directly relevant to local inference | Official BIRD dev/test, measured 4 GB operation, current activity and demo status |
| **SkyRL-SQL** - `https://novasky-ai.notion.site/skyrl-sql` and `https://github.com/NovaSky-AI/SkyRL` | SQL reinforcement-learning project and training infrastructure | Exact qualifying checkpoint metadata, BIRD attribution, license and deployment details |
| **Kaggle Qwen2.5-3B Text2SQL QLoRA** - `https://www.kaggle.com/code/akarshikatripathi/qwen25-3b-text2sql-qlora` | A small-model SQL fine-tuning notebook lead | Reproducible output checkpoint, license and official benchmark result |
| **Kaggle Qwen 2.5 Unsloth notebook** - `https://www.kaggle.com/code/danielhanchen/kaggle-qwen-2-5-unsloth-notebook` | General small-model fine-tuning/export starting point | It is not, by itself, evidence of SQL specialization or BIRD accuracy |

Do not discard these leads merely because their metadata is incomplete, but do not promote them above reproducible, licensed checkpoints on the strength of a name or notebook title.

## 3. Open-Source Agents And Data-Analyst Applications To Fork

### An agent framework is not a benchmark-qualified model

Vanna is a useful case study in both opportunity and risk. Its repository describes natural-language querying, retrieval, SQL execution, presentation, permissions, and local Ollama integration. That is considerably closer to a business-user demo than a raw SQL model card. [34]

However, the repository metadata is archived, with its last push on 2026-02-02. The right response is not to discard the code, but to treat it as a component source with a maintenance burden. A polished interface and a large star count do not establish correct joins, dirty-value handling, or BIRD performance. [66]

The table distinguishes reusable software from the model defaults it ships with. **F** means framework hardware: the application may run on CPU, but inference inherits the selected model's requirements. Browser front ends are not evidence of browser-local model execution.

| Project / URL | Plain-words description | License | Last update | Stars | Model size / restriction issue | BIRD dev / test | Demo | Combine with |
|---|---|---|---|---:|---|---|---|---|
| **Vanna** - `https://github.com/vanna-ai/vanna` | Retrieval-backed SQL agent with user-facing tables/charts and permissions | MIT | **2026-02-02 push; archived** | **23,816** | No fixed size; Ollama supported; F | NR / NR | Local UI/component; public hosted demo NR | XiYan/OmniSQL plus your validator [34][66] |
| **WrenAI** - `https://github.com/Canner/WrenAI` | Semantic-context BI agent with SQL, charts, and dashboards | **AGPL-3.0 core; some engine/SDK/skills components Apache-2.0** | NR | NR | No fixed size; advertised integrations are not proof of <=8B compatibility; F | NR / NR | Self-hosting/deployment examples; public anonymous demo NR | Curated semantic definitions plus local generator [33] |
| **DB-GPT** - `https://github.com/eosphoros-ai/DB-GPT` | Broad data-agent platform covering databases, files, SQL/Python, reports | MIT | NR | NR | Local vLLM/llama.cpp paths; choose <=8B; F | NR / NR | Local platform; public hosted demo NR | Small SQL specialist; borrow only needed modules [23] |
| **DB-GPT-Hub** - `https://github.com/eosphoros-ai/DB-GPT-Hub` | Text-to-SQL tuning and evaluation recipes | MIT | NR | **2,014** | Includes 7B and larger models; select eligible runs only | NR / NR | No live demo established | CodeS/Qwen/SQLCoder training; separate Spider claims from BIRD [35] |
| **Text2SqlAgent framework** - `https://github.com/Text2SqlAgent/text2sql-framework` | Execution-centered exploration/test/repair framework with a small tool surface | MIT | NR | NR | Ollama/vLLM endpoints supported; defaults/examples include proprietary models; F | NR / NR | Local dummy-database example | Best lightweight orchestration candidate for XiYan-3B [39] |
| **PremSQL** - `https://github.com/premAI-io/premsql` | Local SQL pipeline, execution and agent/playground components | MIT library | NR | NR | Local model paths exist; example agent may call GPT-4o; F | Official split NR / NR | Local playground | Prem-1B or another local specialist; replace cloud defaults [58] |
| **SQLChat** - `https://github.com/sqlchat/sqlchat` | Chat-style SQL client | MIT | NR | NR | Default OpenAI path; configurable endpoint can target Ollama; F | NR / NR | **Advertised public site:** `https://sqlchat.ai/`; uptime NR | Small-model endpoint plus strict read-only gateway [30] |
| **SQLBot** - `https://github.com/dataease/SQLBot` | Chinese ChatBI application with RAG, charts and integrations | **FIT2CLOUD license, GPLv3-based with additional restrictions** | NR | NR | Configurable model; qualifying local path needs testing; F | NR / NR | Local web deployment | Chinese UI inspiration, local SQL generator, validation [21] |
| **Chat2DB** - `https://github.com/OtterMind/Chat2DB` | Local-first database client with AI features | **Before 5.3.0 Apache-2.0; later source-available terms add conditions** | NR | NR | Bring-your-own model; F | NR / NR | Local application; public live demo NR | Schema browser/UI, not a substitute for an evaluation loop [32] |
| **Dataherald** - `https://github.com/Dataherald/dataherald` | Enterprise-oriented NL-to-SQL engine/API and integrations | Apache-2.0 | NR | NR | No qualifying fixed model established; F | NR / NR | Local/API deployment; public demo NR | Retrieval/API scaffolding plus small-model adapter [22] |
| **PandasAI** - `https://github.com/Sinaptik-AI/pandas-ai` | Conversational analysis of SQL and file data; can generate analysis code | MIT outside `pandasai/ee` | NR | NR | Captured example uses GPT-4.1-mini, which is ineligible; F | NR / NR | Colab/local examples, not a confirmed public live demo | Charts and file analysis; sandbox generated code [28] |
| **PydanticAITest** - `https://gitee.com/NanGePlus/PydanticAITest` | Chinese PydanticAI examples for PostgreSQL/MySQL and local/cloud models | MIT | Commit hash visible; date NR | **3** | No fixed eligible model established; F | NR / NR | Local examples | Small, understandable Chinese integration reference [55] |

**Takeaway:** for a short hackathon, the lightweight execution-centered framework is the cleanest starting point; Vanna and WrenAI offer richer product ideas but add integration and maintenance/licensing considerations.

### Niche implementations and training repositories

| Candidate / URL | Verified or clearly bounded contribution | Metadata and score caveats | Useful merge |
|---|---|---|---|
| **bird-text2sql** - `https://github.com/ShemsouThere/bird-text2sql` | Qwen Coder SFT/LoRA/GRPO, model merging and FastAPI-oriented workflow | 7B and 14B paths; repository's 7B setup specifies a **16 GB NVIDIA GPU**. Its larger-model score ranges must not be assigned to 7B. License, stars and last update NR; local demo only. [38] | Training/evaluation scaffolding, not a ready 4 GB solution |
| **dLounce/Text-to-SQL** - `https://github.com/dLounce/Text-to-SQL` | Qwen2.5-Coder-7B SFT/GRPO and execution-based reward work | **0 stars** in snapshot; license/last update NR. Reports **38.1 -> 53.1 -> 55.1** on a custom held-out setup, not official BIRD test. [31] | SQLite timeout/progress handling and a compact training experiment [31] |
| **Dataline** - `https://github.com/RamiAwar/dataline` | Additional natural-language data-analysis application lead | Qualifying model, official BIRD scores, current activity, measured hardware and live demo NR | UI/data-connection ideas; inspect license before merging |
| **py-nl2sql** - `https://github.com/pillarliang/py-nl2sql` | Additional small Python NL-to-SQL implementation lead | Qualifying model, official BIRD scores, current activity and live demo NR | A simpler codebase to inspect before adopting a larger platform |

These niche repositories are worth inspecting precisely because they may be easier to understand and modify. Their existence is not evidence that their reported experiment setup matches the hackathon's model, data, or hardware constraints.

## 4. Self-Correction, Verification, And Abstention Methods To Merge

### TrustSQL supplies the right product distinction: infeasible is not incorrect SQL

TrustSQL's central distinction maps directly to this problem statement: answer feasible questions, and abstain on infeasible ones. Its explored small-model paths include T5-3B and SQLCoder-7B-2, alongside proprietary models. It also studies feasibility/error-classification stages rather than treating every failure as a reason to generate another query. [29]

That distinction matters when the database lacks a required field, the question assumes a nonexistent relationship, or "revenue" has no agreed definition. An execution-repair loop cannot manufacture missing information. Borrow the controller structure, but make every classifier and verifier local and <=8B, or replace them with transparent rules. TrustSQL's cited default classifiers include GPT-4o, so its default experiment is not automatically eligible. [29]

| Method / URL | Mechanism in plain words | Eligible reuse | Model/benchmark caveat | License / activity / stars / demo |
|---|---|---|---|---|
| **TrustSQL** - `https://github.com/glee4810/TrustSQL` | Detect whether a question is answerable; generate SQL or abstain; optionally detect bad outputs | Feasibility/error taxonomy and small-model paths | Replace proprietary classification defaults; BIRD dev/test NR | CC-BY-4.0 repository material; last update/stars NR; live demo NR [29][68] |
| **RTS** - `https://arxiv.org/html/2501.10858` | Ask for help or abstain when schema linking is unreliable | Adaptive clarification and human-feedback loop | Reports **64.72%** with DeepSeek-7B in its RTS setup versus **66.21%** with gold schema; not a directly established official dev/test leaderboard comparison | Paper; qualifying implementation/license/stars/demo NR [36] |
| **MAC-SQL** - `https://github.com/wbbeyourself/MAC-SQL` | Selector chooses schema, Decomposer breaks down the query, Refiner repairs it | Role decomposition and execution correction | Default GPT-4 path ineligible; repository also documents a CodeLlama-7B SQL-Llama deployment path | License/update/stars/demo NR; eligible-size BIRD scores NR [61] |
| **Alpha-SQL** - `https://github.com/HKUSTDial/Alpha-SQL` | Searches alternative reasoning/actions using Monte Carlo Tree Search and self-supervised rewards | Search and candidate-revision logic | Default Qwen Coder 32B is excluded; a 7B configuration is present, but do not inherit the larger model's score | MIT; update/stars/live demo NR [65] |
| **DAIL-SQL** - `https://github.com/BeachWang/DAIL-SQL` | Selects useful few-shot examples and uses schema-linking/self-consistency components | Example selection and prompt construction | Captured **86.6%** is Spider EX with GPT-4, not eligible BIRD performance | Apache-2.0; update/stars/demo NR [60] |
| **DIN-SQL** - `https://github.com/MohammadrezaPourreza/Few-shot-NL2SQL-with-prompting` | Modular prompting and correction | Prompt structure and BIRD evaluation scripts | Captured BIRD path uses GPT-4; small-model transfer must be measured | MIT; **414 stars** in snapshot; update/demo NR [62] |
| **CHASE-SQL** - `https://arxiv.org/html/2410.01943` | Generates multiple reasoning paths/candidates and selects among them | Candidate diversity, execution feedback, selection | **73.01% dev / 73.0% test** uses Gemini 1.5 Pro; qualifying code/model configuration not established | Paper; forkable-code license/update/stars/demo NR [105] |
| **DB-Explore** - `https://arxiv.org/html/2503.04959v1` | Automates database exploration and instruction synthesis | Exploration-derived context before generation | Reports **52.1% BIRD**, but split and <=8B attribution are not established by the cited excerpt | Paper; code/license/update/stars/demo NR [107] |
| **ReFoRCE** - `https://arxiv.org/html/2502.00675` | Self-refinement, consensus and column exploration for enterprise workflows | Column exploration and agreement checks | Cited results use **o3** on Spider 2.0, not BIRD: **35.83% Snow / 36.56% Lite EX** | Paper; qualifying small-model implementation metadata NR [106] |
| **CHESS** - `https://github.com/ShayanTalaei/CHESS` | Multi-stage SQL-agent implementation worth inspecting for context reduction and candidate validation | Individual stages rather than wholesale adoption | Qualifying <=8B configuration and exact comparable BIRD results NR here | License/update/stars/live demo NR |

**Takeaway:** copy mechanisms, not headline scores. For the hackathon, a bounded repair loop plus feasibility checks is a safer first implementation than an expensive search tree with many calls to a small, uncertain verifier.

### Additional research leads, without invented reproducibility claims

| Lead | URL | Potential value | What is not established |
|---|---|---|---|
| **RSL-SQL** | `https://arxiv.org/html/2411.00073v2` | Schema-linking research | Qualifying checkpoint, usable code, license and comparable score |
| **LinkAlign** | `https://arxiv.org/html/2503.18596v3` | Schema-linking/alignment research | Full small-model deployment and benchmark metadata |
| **PremiseSQL** | `https://openreview.net/pdf?id=d2T52hH452` | Questions with incorrect premises; useful for refusal/clarification design | Forkable implementation and <=8B result |

For **OpenSearch-SQL**, the available discovery did not establish a reliable matching paper/repository pair. Do not confuse a text-to-SQL research system with unrelated OpenSearch SQL plugins.

## 5. Read BIRD And Spider 2.0 Results Without Breaking The Restriction

### Arctic versus CHASE illustrates why configuration matters

Arctic-7B is a candidate generator under the nominal size rule. CHASE-SQL's cited score comes from a proprietary frontier model. Both can inspire candidate generation and selection, but they occupy different eligibility categories. Replacing Gemini with a 3B model changes the experiment; it does not preserve CHASE's published accuracy. [43][105]

Likewise, ReFoRCE's Snow/Lite results address enterprise workflows, while Spider 2.0 contains **632 workflow problems**. They should inform exploration and robustness work, not be inserted into a BIRD dev/test column. [106][3]

| Entry or result | What the source actually supports | Hackathon treatment |
|---|---|---|
| Arctic-7B | 68.9% BIRD dev; model-card test claim qualified above | Eligible-size model candidate; reproduce exact setup |
| OmniSQL-7B | 63.9% BIRD dev in the cited paper | Eligible-size model candidate; add agent stages separately |
| XiYan 3B/7B-2504 | Size-specific BIRD dev scores with schema-format comparisons | Especially useful controlled baseline |
| xorazm-0.8B | Official BIRD-table dev entry at 53.43% | Interesting low-memory candidate; inspect evaluation details |
| SQL-R1 headline | 67.1% BIRD without captured size/split attribution | Do not label it a verified 3B/7B score |
| XiYan framework headline | Framework advertises 75.63% BIRD EX; small-model attribution not established | Framework inspiration, not an eligible model score [47] |
| XiYan 32B | 69.03% BIRD test for a 32B model | Exclude the checkpoint under the hard restriction [47] |
| CHASE-SQL | 73.01% dev / 73.0% test with Gemini 1.5 Pro | Reuse concepts only [105] |
| ReFoRCE | o3 results on Spider 2.0 Snow/Lite | Different benchmark and ineligible model [106] |
| dLounce custom experiment | 38.1/53.1/55.1 on its own held-out setup | Useful experiment, not official BIRD test [31] |

**Takeaway:** this is a set of benchmark-supported leads, not an exhaustive reconstruction of the current leaderboard. Keep official BIRD, Mini-Dev, custom splits, Spider, and Spider 2.0 in separate result sheets.

Useful benchmark entry points are `https://bird-bench.github.io/`, `https://github.com/bird-bench/mini_dev`, `https://spider2-sql.github.io/`, and `https://github.com/xlang-ai/Spider2`. The Spider 2.0 repository is MIT-licensed; that does not automatically describe the licensing of every referenced dataset or model. [51]

### Evaluation rules for your own submission

1. **Pin the complete configuration:** checkpoint revision, quantization, prompt, schema format, tools, retry budget and candidate count.
2. **Audit every model call:** generator, router, verifier, embedding model, reranker and summarizer must obey the restriction. A hidden proprietary fallback invalidates an otherwise local demo.
3. **Resolve nominal 8B boundaries explicitly:** model names and rounded Hugging Face metadata are not exact tensor counts. Keep the nominal-8B models in the catalog, but obtain organizer clarification and inspect the chosen checkpoint before relying on them.
4. **Separate benchmark and product policies:** refusal can be correct product behavior but still fail an execution-scored answerable benchmark item. Report execution accuracy and refusal behavior separately; do not count an abstention as a correct SQL answer.
5. **Hold out evaluation examples:** do not put gold SQL from the evaluation split into retrieved examples, fine-tuning data or scenario memory.
6. **Track failure categories:** wrong table, wrong join, wrong aggregation, value mismatch, date interpretation, missing business rule, execution error, timeout and unjustified refusal.

Uber's QueryGPT account explicitly notes that repeated evaluations can differ because of model nondeterminism. That is a reason to keep seeds/configurations and report repeatability, not to hide a favorable single run behind a headline percentage. [108]

## 6. Deployment: What A 4 GB GPU, CPU, Or Browser Can Actually Promise

### Four-bit weights are only the beginning

The arithmetic below is an engineering estimate using the advertised nominal parameter count. It excludes quantization metadata, KV cache, activations, runtime buffers and other application memory.

| Nominal size | Four-bit raw-weight estimate | 4 GB GPU | CPU | Browser | Hosted GPU |
|---:|---:|---|---|---|---|
| 0.8B-1.7B | About 0.4-0.85 GB | Most promising category, subject to runtime/context | Plausible with compatible quantization and adequate RAM | Requires supported browser runtime and converted weights | Optional |
| 3B | About 1.5 GB | Plausible first target; measure actual peak memory | Plausible; speed and RAM depend on hardware | Not established for the listed SQL checkpoints | Optional, useful for development |
| 4B | About 2 GB | Potentially feasible with tight context; not guaranteed | Plausible with adequate RAM | Not established for the listed checkpoint | Optional |
| 7B | About 3.5 GB | Tight to unsuitable for full offload once overhead is included | Plausible with sufficient RAM; partial GPU offload can help | Not established | Recommended for comfortable iteration or long contexts |
| Nominal 8B | About 4 GB | Raw weights already consume the nominal budget | Requires sufficient RAM and compatible runtime | Not established | Usually the simpler deployment choice; first settle size eligibility |

**Takeaway:** "runs on CPU" does not mean "runs in 4 GB system RAM," and "quantized" does not mean "fits completely in 4 GB VRAM." Do not promise latency without measuring the exact model, context and machine.

### Per-candidate deployment assignment

| Candidates | 4 GB GPU | CPU | Browser-local inference | Hosted GPU requirement |
|---|---|---|---|---|
| xorazm-0.8B, Prem-1B, CodeS-1B, MTSQL-1.7B | Smallest-weight category; conversion/runtime still need testing | Candidate path; checkpoint-specific support NR | No verified ready deployment | Not inherently required, but no measured deployment supplied |
| XiYan-3B, CodeS-3B, SQL-R1-3B | Best practical category to test first | XiYan card advertises compatible local quantization tooling; others require checkpoint-specific setup | No verified ready deployment | Optional [44] |
| MTSQL-4B, distil-Qwen3-4B-GGUF lead | Potentially feasible; actual memory NR | GGUF is directly relevant for the distil lead; measure both | No verified ready deployment | Optional, not established as necessary |
| SQLCoder-7B-2 | Tight; CPU offload is safer than assuming full GPU fit | Documented llama.cpp/Ollama-oriented local paths | No verified ready deployment | Optional if CPU latency is acceptable [26] |
| XiYan-7B, OmniSQL-7B, Arctic-7B, CodeS-7B, SQL-R1-7B, SENSE-7B | Do not promise full 4 GB fit | Possible with appropriate runtime/quantization; not individually benchmarked here | No verified ready deployment | Recommended for straightforward use; not a proven universal requirement |
| Nominal-8B SQLCoder/Korean checkpoints | Do not promise full 4 GB fit | Possible subject to RAM/runtime and exact-size eligibility | No verified ready deployment | Practical option after the eligibility check |
| All application frameworks in Section 3 | Application memory plus selected model; not independently a fit claim | Application can be separated from inference | A web UI is not browser-local inference | Inherits selected model |

**Takeaway:** the strongest documented local-serving convenience in this catalog is SQLCoder's mature runtime support; the strongest first low-memory SQL-specialist experiment is XiYan-3B. Neither substitutes for an actual memory and latency test.

SQLCoder is also an instructive safety case. Its card warns that it was not trained to reject malicious write requests. A local model can therefore be convenient and still unsafe as an unrestricted database client. Enforce read-only access outside the model. [26]

For browser work, distinguish three projects: `https://github.com/mlc-ai/web-llm` for browser LLM inference, `https://github.com/duckdb/duckdb-wasm` for browser-side database execution, and `https://github.com/ggml-org/llama.cpp` for GGUF-oriented local inference. WebLLM is a browser inference engine, not proof that a listed SQL GGUF can be loaded directly into it; browser deployment is a separate conversion/runtime project. [78]

**Decision:** do not make browser-only inference the critical path. A local desktop/server model with a browser UI is the lower-risk hackathon architecture.

## 7. Validate Messy Data Before Turning It Into A Confident Answer

### A synthetic demo that exposes the real failure modes

Use a deliberately small, labeled **synthetic** sales database containing duplicate order rows, an `N/A` amount, an ambiguous date such as `03/04/2025`, a cancelled order, and a customer table that can multiply rows when joined incorrectly. Ask: "What was revenue last month?"

The first correct behavior may be a clarification: does revenue include cancelled orders, which date convention applies, and is revenue gross or net? Once the judge supplies those rules, show the selected tables, the normalization expressions, before/after row counts, the join checks and the final SQL. This demonstrates reasoning about the data without pretending that the model can recover unstated business truth from column names.

| Failure mode | Deterministic check or control | What the judge sees | Important limitation |
|---|---|---|---|
| `N/A`, empty strings, mixed numeric text | Profile values; normalize only with an explicit rule; count rejected conversions | Raw values, normalization rule, excluded-row count | `N/A` might be a legitimate category; do not erase it globally |
| Mixed/ambiguous dates | Recognize candidate formats; detect ambiguity; require locale or a rule | "Cannot distinguish March 4 from April 3" when appropriate | Parsing success is not semantic correctness |
| Duplicates | Establish grain and keys; compare row counts and distinct business identifiers | Duplicate report and chosen deduplication rule | Blanket `DISTINCT` can hide real events |
| Join multiplication | Compare pre/post-join counts and key cardinalities; inspect unmatched keys | Fanout warning and corrected join | More returned rows can be valid for a one-to-many question |
| Missing business rules | Require definitions for revenue, active customer, churn, refunds and time window | A concise clarification instead of invented logic | A model's plausible definition is not your company's definition |
| Wrong units or aggregation | Check currency, units, weighted versus unweighted averages, denominator and grain | Calculation definition beside result | The database may not contain conversion rates or complete denominators |
| Empty result | Compare against source counts and filters; test whether predicates eliminate everything | "Zero matching rows" distinguished from "query likely wrong" | An empty answer can be legitimate |
| Implausible values | Domain constraints and distribution checks | Negative-price/outlier/null warnings with examples | Outlier does not automatically mean error |
| Unsafe or expensive SQL | Read-only credentials, statement restrictions, query limits and execution timeout | Blocked write and bounded execution | A `LIMIT` does not make every aggregate or join cheap |
| Unsupported conclusion | Generate prose from actual result fields and validation status | SQL, result, checks, warnings and an explicit refusal state | A fluent narrative is not independent verification |

**Takeaway:** deterministic checks should expose uncertainty, not silently "clean" the database into whatever makes the answer look plausible.

### Ten questions a non-expert judge will ask

| # | Judge's "what if" question | Demo response | Observable pass condition |
|---:|---|---|---|
| 1 | **What if the data is wrong?** | Show `N/A`, invalid amounts and missingness before answering; preserve raw values | The answer states what was excluded or remains unreliable |
| 2 | **What if the same order appears twice?** | Show physical rows versus distinct order IDs; ask for the deduplication rule when necessary | The final count/amount follows an explicit grain |
| 3 | **What if dates mean different things?** | Present the ambiguous date and request a locale/date policy | No silent choice between plausible interpretations |
| 4 | **What if "revenue" means something different to me?** | Ask gross/net, refunds, cancellations and time-window questions | The rule appears beside the SQL and answer |
| 5 | **What if it lies confidently?** | Expand an evidence panel with executed SQL, result rows and failed/passed checks | Every numerical statement maps to a returned field/calculation |
| 6 | **What if it returns zero because the query is broken?** | Show source counts and progressively applied filters | Distinguishes verified zero from unresolved query failure |
| 7 | **What if it joins the wrong tables?** | Show foreign keys, join path and row-multiplication check | A deliberate bad join triggers a visible warning |
| 8 | **What if it leaks data, deletes rows, or follows instructions inside a cell?** | Attempt a forbidden table, write statement and instruction-like cell value | Permission enforcement blocks access/writes; cell content remains data |
| 9 | **What if the answer is not in the database?** | Ask for an unavailable cost, missing region or unsupported forecast | Explicit refusal naming the missing information; no invented SQL answer |
| 10 | **What if there is no internet or only a small laptop?** | Run a local small model, show its identity and measured latency; disable network fallback | The demo remains local or clearly declares its unavailable configuration |

**Takeaway:** judge trust comes from visible failure handling, not from a confidence percentage produced by the same model that wrote the query.

A practical answer object should contain: **answer, SQL, result summary, data-quality warnings, assumptions, validation checks, and status**. Use distinct statuses such as `answered`, `needs_clarification`, `insufficient_data`, `unsafe_request`, and `execution_failed`. This also makes errors easy to display and score without hiding them in prose.

## 8. Production Inspiration, Regional Sources, And Real Business Losses

### Borrow product patterns without importing forbidden models

OpenAI's internal-agent description grounds SQL in metadata, lineage and historical queries, evaluates important questions against golden SQL, and uses pass-through access permissions. Pinterest's published architecture combines context/intent retrieval with historical query patterns and EXPLAIN-before-EXECUTE. These are useful design references, not released <=8B implementations or accuracy guarantees for your build. [109][110]

Their shared lesson is that accumulated business knowledge matters. Their difference is also useful: a historical-query library can expand coverage, while a curated semantic definition constrains interpretation. Use both selectively rather than allowing old queries to overrule current metric definitions.

| Product / source URL | Demo pattern to borrow | Restriction or caveat |
|---|---|---|
| **Snowflake Cortex Analyst** - `https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository` | Question-to-verified-SQL examples; evaluate generated results against trusted queries | Wrong "verified" examples can reduce accuracy; logical semantic-model names matter [111][112] |
| **Databricks Genie** - `https://docs.databricks.com/aws/en/genie/monitor` | Benchmark questions paired with gold SQL; visible review workflow | Questions without SQL answers require manual review in the cited documentation [113] |
| **Looker** - `https://looker.com/` | Centralized metric logic and underlying SQL/explanation | Commercial semantic tooling is inspiration, not an eligible local model [114] |
| **OpenAI internal data agent** - `https://openai.com/index/inside-our-in-house-data-agent` | Lineage, query history, golden tasks and pass-through permissions | Not a forkable small-model release [109] |
| **Pinterest engineering** - `https://medium.com/pinterest-engineering/unified-context-intent-embeddings-for-scalable-text-to-sql-793635e60aac` | Retrieve analytical intent plus validated join/filter patterns; explain before execution | Published architecture, not a packaged <=8B agent [110] |
| **Vercel d0** - `https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools` | Reduce orchestration/tool clutter | The article says removing **80% of tools** improved its internal agent; that is a case-specific result, not a universal target [115] |
| **Uber QueryGPT** - `https://www.uber.com/us/en/blog/query-gpt` | Intent/dataset/SQL evaluation and repeatability awareness | Production narrative, not an eligible checkpoint; evaluations can be nondeterministic [108] |

**Takeaway:** semantic layers and verified examples are especially valuable for repeated business metrics. Exploration remains necessary for unfamiliar schemas, but should not invent business definitions that already have an owner.

### Regional and community coverage: what is actionable

| Source family | Supported finding | How to use it |
|---|---|---|
| Chinese / Alibaba ecosystem | XiYan provides small checkpoints, schema representation work and a broader agent framework; the official framework repository is `https://github.com/alibaba/XiYan-SQL` | Prioritize the 3B/7B checkpoints; do not substitute its 32B demo or framework headline for a qualifying small-model result [47] |
| Chinese application ecosystem | DB-GPT, SQLBot and the Gitee PydanticAI examples provide concrete implementation/UI material | Review model defaults and custom licenses before merging |
| ModelScope | XiYan's advertised 32B demo is a useful product reference | It is not an eligible <=8B demo [5] |
| Korean | KREW's Korean Spider checkpoint is a concrete language-specialized artifact | Keep its Korean Spider evaluation separate from BIRD [49] |
| Gitee / GitCode mirrors | An awesome-list mirror and examples were discovered; no additional independently benchmarked small model was established | Treat mirrors as discovery aids, not separate leaderboard systems |
| Japanese sources | No qualifying Japanese-specialist SQL checkpoint with complete metadata was established in this catalog | Do not interpret this as proof that none exists |
| Reddit / HN / hackathon discussions | Useful for pain points and deployment anecdotes; no independently supported hackathon-winning <=8B BIRD system was established here | Do not invent winner status or elevate anecdotes into benchmark evidence |
| Zhihu / CSDN / other secondary posts | Useful discovery channels, but no separate score is promoted here without a matching primary artifact | Follow the original repository/model card rather than a reposted headline |

**Takeaway:** regional coverage produces useful artifacts, but a mirrored repository, translated article or social post is not a new independently verified system.

### Real losses: operational analogues, not fabricated AI incidents

The cases below show why wrong calculations and unchecked outputs matter. They are **not claims that a text-to-SQL agent caused these events**.

| Case | Documented failure and financial meaning | Lesson for the demo | Source |
|---|---|---|---|
| **TransAlta electricity-contract bids** | The company filing describes a **$33.3M spreadsheet error**, in the filing's reporting currency, involving mismatched bids and unintended contract purchases. Do not relabel this automatically as US dollars. | Check ranges, alignment, units and business constraints before accepting an apparently valid calculation | TransAlta SEC filing: `https://www.sec.gov/Archives/edgar/data/1144800/000113717104000110/f6k2003q4tac.htm` |
| **JPMorgan London Whale post-mortem** | The task-force report discusses spreadsheet/manual-process and model-control weaknesses in a major trading-loss episode. It does not justify attributing the entire trading loss to one spreadsheet error. | Require independent reasonableness checks, change control and reconciliation; successful execution is not risk validation | JPMorgan task-force report, **2013-01-16** [57] |
| **Citibank / Revlon mistaken payment dispute** | Reuters reports the appellate ruling allowing Citibank to recoup about **$500M** mistakenly paid to lenders. This was a disputed erroneous payment, not proof of a permanent $500M realized loss. | Put high-consequence actions behind independent authorization; an analyst agent should not execute financial transfers [71] | Reuters, **2022-09-08**, appellate ruling coverage [71] |

**Takeaway:** distinguish an erroneous calculation, an erroneous transaction, exposure to loss, and a final realized loss. A trustworthy analyst must preserve those distinctions in its own explanations.

TransAlta is the closest analogy to this hackathon: a structured calculation can be syntactically valid while associating the wrong values with the wrong business objects. A query-result validator should therefore check relationships and totals, not merely whether the database returned rows.

The JPMorgan and Citibank examples add a second boundary: analysis and action should remain separate. Even a well-validated answer should not silently gain authority to update production data or trigger consequential transactions.

## 9. Synthesis: What To Build, What To Merge, What To Avoid

### The major strategies solve different failure classes

| Strategy | Main mechanism | Scope | Trade-off | Evidence base here | Best role |
|---|---|---|---|---|---|
| **Small SQL specialist** | Learns SQL mappings and patterns | Produces candidate SQL efficiently | Can still select the wrong schema, values or business meaning | Size-specific XiYan/OmniSQL/Arctic reports | Core generator |
| **Exploration agent** | Inspects schema, values and execution feedback | Unfamiliar or messy databases | More calls, more latency, more opportunities for tool misuse | Execution-centered framework; DB-Explore; enterprise-workflow research | Discover missing context before generation |
| **Semantic layer / verified query library** | Reuses governed definitions and known-good patterns | Repeated business metrics | Coverage and maintenance burden; bad examples propagate | Snowflake, Looker, Pinterest, OpenAI accounts | Stabilize high-value recurring questions |
| **Candidate search / self-correction** | Tries alternatives, executes, compares, revises | Recoverable generation errors | Agreement is not truth; wrong candidates can agree | CHASE, Alpha-SQL, MAC-SQL and related methods | Bounded second attempt, not unlimited retries |
| **Deterministic result validation** | Checks cardinalities, domains, units and constraints | Known data-quality and query hazards | Cannot invent missing domain knowledge | Engineering controls proposed for this task | Mandatory acceptance gate |
| **Abstention / clarification** | Detects infeasibility or unresolved assumptions | Missing data and ambiguity | May reduce execution score on answerable benchmark items | TrustSQL and RTS | Product-trust boundary |

**Takeaway:** no single strategy covers all failure modes. The strongest system combines a capable generator with external checks and an honest boundary on what the database can support.

Three tensions should shape implementation decisions.

**First, benchmark success and business trust are related but not identical.** BIRD rewards the expected execution result. A business demo additionally needs to distinguish a known answer from an assumption-dependent answer. Keep separate evaluation views rather than weakening refusal behavior to make a single score look better.

**Second, smaller orchestration can outperform a more impressive architecture operationally.** The execution-centered framework provides a local-endpoint path, while Vercel's account warns that a large tool surface can become counterproductive. This supports starting with a small interface, not assuming that all multi-agent research is unnecessary. [39][115]

**Third, model capability and knowledge quality are complementary.** XiYan's schema-format differences show why representation matters; historical-query and semantic-layer cases show why business meaning matters. A larger eligible model may help SQL reasoning, but it cannot safely infer an undisclosed revenue policy or recover absent data. [41][110][114]

### Recommended implementation order

1. **Freeze an eligible model and license.** Start with XiYan-3B-2504; keep OmniSQL-7B or Arctic-7B as an alternative configuration. Pin the exact artifact and audit every auxiliary model.
2. **Implement a read-only exploration/execution service.** Expose schema, bounded samples, profiles, query plans and bounded execution. Keep database permissions outside model control.
3. **Add deterministic acceptance checks.** Focus first on join fanout, duplicates, numeric conversion, date ambiguity, empty results and undefined metrics.
4. **Add one bounded repair path.** Reuse MAC-SQL-style separation or a lightweight execution-centered loop. Log the initial failure and the correction.
5. **Add explicit clarification and refusal.** Borrow TrustSQL's feasibility distinction; do not let repeated generation stand in for missing evidence.
6. **Show the evidence panel.** Question, selected tables, SQL, result, checks, assumptions and status should be visible without reading logs.
7. **Evaluate the exact shipped configuration.** Quantization, context limits, schema selection and retry count are part of the system, not invisible implementation details.

**Final recommendation:** build **XiYan-3B + structured schema/value exploration + read-only execution + deterministic checks + TrustSQL-inspired abstention**. Use a richer 7B SQL specialist only when measured hardware and error analysis justify it. The differentiator is not "it writes SQL"; it is **"it shows why this answer is supported, and stops when it is not."**

## References

1. *seeklhy/OmniSQL-7B · Hugging Face*. https://huggingface.co/seeklhy/OmniSQL-7B
2. *GitHub - XGenerationLab/XiYan-SQL: A MULTI-GENERATOR ENSEMBLE FRAMEWORK FOR NATURAL LANGUAGE TO SQL · GitHub*. https://github.com/XGenerationLab/XiYan-SQL
3. *Spider 2.0*. https://spider2-sql.github.io/
4. *BIRD-bench*. https://bird-bench.github.io/
5. *GitHub - XGenerationLab/XiYanSQL-QwenCoder: XiYanSQL models for Text-to-SQL. · GitHub*. https://github.com/XGenerationLab/XiYanSQL-QwenCoder
6. *bird-bench/mini_dev*. https://github.com/bird-bench/mini_dev
7. *Hugging Face – The AI community building the future.*. https://huggingface.co/
8. *BIRD-INTERACT: Re-imagining Text-to-SQL Evaluation for ...*. https://arxiv.org/abs/2510.05318
9. *bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF · Hugging Face*. https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF
10. *BIRD-SQL Evaluation Framework | bird-bench/mini_dev | DeepWiki*. https://deepwiki.com/bird-bench/mini_dev/2-bird-sql-evaluation-framework
11. *PremiseSQL: Evaluating Premise Critique and Abstention in ...*. https://openreview.net/pdf?id=d2T52hH452
12. *Text-to-SQL Agents in Production 2026: Architectures, Safety ...*. https://niteagent.com/blog/text-to-sql-agents-production-2026
13. *Text-to-SQL LLM Leaderboard 2026: Spider and BIRD Ranked*. https://awesomeagents.ai/leaderboards/text-to-sql-leaderboard
14. *Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL*. https://arxiv.org/html/2505.20315v2
15. *Arctic-Text2SQL-R1 Tops BIRD and Wins Broadly*. https://www.snowflake.com/en/blog/engineering/arctic-text2sql-r1-sql-generation-benchmark
16. *SQLBot/docs/README.en.md at main · dataease/SQLBot · GitHub*. https://github.com/dataease/SQLBot/blob/main/docs/README.en.md
17. *【日本語 GPT 文章生成】Hugging Face 入門① 〜Pipelineで*. https://www.youtube.com/watch?v=Fss7czY2R0s
18. *TrustSQL: Benchmarking Text-to-SQL Reliability with ...*. https://ui.adsabs.harvard.edu/abs/arXiv:2403.15879
19. *学習済みモデルを共有する - Hugging Face*. https://huggingface.co/learn/llm-course/ja/chapter4/3
20. *CodeS: Towards Building Open-source Language Models for Text-to-SQL*. https://arxiv.org/html/2402.16347v1
21. *GitHub - dataease/SQLBot: 基于大模型和 RAG 的智能问数系统，对话式...*. https://github.com/dataease/SQLBot
22. *GitHub - Dataherald/dataherald: Interact with your SQL database, Natural Language to SQL using LLMs · GitHub*. https://github.com/Dataherald/dataherald
23. *GitHub - eosphoros-ai/DB-GPT: open-source agentic AI data assistant for the next generation of AI + Data products. · GitHub*. https://github.com/eosphoros-ai/DB-GPT
24. *defog/llama-3-sqlcoder-8b · Hugging Face*. https://huggingface.co/defog/llama-3-sqlcoder-8b
25. *GitHub - RUCKBReasoning/codes: The source code of CodeS (SIGMOD 2024). · GitHub*. https://github.com/RUCKBReasoning/codes
26. *defog/sqlcoder-7b-2 · Hugging Face*. https://huggingface.co/defog/sqlcoder-7b-2
27. [GitHub - RUCKBReasoning/OmniSQL: [VLDB' 25] Synthesizing High-quality Text-to-SQL Data at Scale. SynSQL-2.5M is the first million-scale cross-domain text-to-SQL dataset. · GitHub](https://github.com/RUCKBReasoning/OmniSQL)
28. *GitHub - sinaptik-ai/pandas-ai: Chat with your database or your datalake (SQL, CSV, parquet). PandasAI makes data analysis conversational using LLMs and RAG. · GitHub*. https://github.com/Sinaptik-AI/pandas-ai
29. *TrustSQL: Benchmarking Text-to-SQL Reliability with Penalty-Based Scoring*. https://arxiv.org/html/2403.15879
30. *GitHub - sqlchat/sqlchat: Chat-based SQL Client and Editor for the next decade · GitHub*. https://github.com/sqlchat/sqlchat
31. *GitHub - dLounce/Text-to-SQL: Fine-tuned Qwen2.5-Coder-7B for text-to-SQL with execution-filtered SFT and GRPO on BIRD and Spider · GitHub*. https://github.com/dLounce/Text-to-SQL
32. *GitHub - OtterMind/Chat2DB: Chat2DB is a free, cross-platform, local-first database client and SQL workspace for developers, DBAs, analysts, and data teams. Connect to 40+ databases, manage data, edit and run SQL, and use your own AI model to generate, explain, and optimize queries. Available on desktop, web, Docker, and CLI, with MCP support. · GitHub*. https://github.com/OtterMind/Chat2DB
33. *GitHub - Canner/WrenAI: GenBI (Generative BI) for AI agents, an open-source, governed text-to-SQL through an open context layer that turns natural-language questions into trusted dashboards, charts, and SQL across 20+ data sources, such as BigQuery, Snowflake, PostgreSQL, ClickHouse, Amazon Redshift, Databricks and more. · GitHub*. https://github.com/Canner/WrenAI
34. *GitHub - vanna-ai/vanna: 🤖 Chat with your SQL database 📊. Accurate Text-to-SQL Generation via LLMs using Agentic Retrieval 🔄. · GitHub*. https://github.com/vanna-ai/vanna
35. *GitHub - eosphoros-ai/DB-GPT-Hub: A repository that contains models, datasets, and fine-tuning techniques for DB-GPT, with the purpose of enhancing model performance  in Text-to-SQL · GitHub*. https://github.com/eosphoros-ai/DB-GPT-Hub
36. *Reliable Text-to-SQL with Adaptive Abstention*. https://arxiv.org/html/2501.10858
37. *GitHub - ShayanTalaei/CHESS: Contextual Harnessing for Efficient SQL Synthesis · GitHub*. https://github.com/ShayanTalaei/CHESS
38. *GitHub - ShemsouThere/bird-text2sql · GitHub*. https://github.com/ShemsouThere/bird-text2sql
39. *GitHub - Text2SqlAgent/text2sql-framework: Agentic text-to-SQL SDK: hand the LLM one execute_sql tool and let it explore the schema, test queries, and self-correct — no RAG, no semantic layer. 20/20 on an 80-table Spider run. Built-in tracing and scenario support. · GitHub*. https://github.com/Text2SqlAgent/text2sql-framework
40. *OmniSQL: Synthesizing High-quality Text-to-SQL Data at Scale*. https://arxiv.org/html/2503.02240
41. *XGenerationLab/XiYanSQL-QwenCoder-7B-2504 · Hugging Face*. https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-7B-2504
42. *shakha-de/xorazm-text2sql-0.8b · Hugging Face*. https://huggingface.co/shakha-de/xorazm-text2sql-0.8b
43. *Snowflake/Arctic-Text2SQL-R1-7B · Hugging Face*. https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B
44. *XGenerationLab/XiYanSQL-QwenCoder-3B-2504 · Hugging Face*. https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-3B-2504
45. *GitHub - taichengguo/MTSQL-R1: Official Code for MTSQL-R1: Towards Long-Horizon Multi-Turn Text-to-SQL via Agentic Training (In ACL 2026 Main) · GitHub*. https://github.com/taichengguo/MTSQL-R1
46. [GitHub - DataArcTech/SQL-R1: [NeurIPS'25] Official Repository for the Paper "SQL-R1: Training Natural Language to SQL Reasoning Model By Reinforcement Learning" · GitHub](https://github.com/IDEA-FinAI/SQL-R1)
47. *GitHub - alibaba/XiYan-SQL · GitHub*. https://github.com/alibaba/XiYan-SQL
48. [GitHub - Yangjiaxi/Sense: [ACL24] Official repo for "Synthesizing Text-to-SQL Data from Weak and Strong LLMs" · GitHub](https://github.com/Yangjiaxi/Sense)
49. *huggingface-KREW/Llama-3.1-8B-Spider-SQL-Ko · Hugging Face*. https://huggingface.co/huggingface-KREW/Llama-3.1-8B-Spider-SQL-Ko
50. *mylovextt/Awesome-Text2SQL*. https://gitee.com/mylovextt/Awesome-Text2SQL
51. [GitHub - xlang-ai/Spider2: [ICLR 2025 Oral] Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows · GitHub](https://github.com/xlang-ai/Spider2)
52. *GitHub - eosphoros-ai/Awesome-Text2SQL: Curated tutorials and resources for Large Language Models, Text2SQL,  Text2DSL、Text2API、Text2Vis and more. · GitHub*. https://github.com/eosphoros-ai/Awesome-Text2SQL
53. *Citigroup cannot recoup Revlon payouts after nearly $900 million gaffe: U.S. judge | Reuters*. https://www.reuters.com/article/business/citigroup-cannot-recoup-revlon-payouts-after-nearly-900-million-gaffe-us-jud-idUSKBN2AG1TG
54. *GitHub - gleanwork/mcp-server: MCP server for Glean API integration · GitHub*. https://github.com/gleanwork/mcp-server
55. *PydanticAITest: PydanticAI开源框架，搭建基于PostgreSQL、MySQL的Text2SQL应用进行SQL语句生成，支持GPT大模型、国产大模型、开源本地大模型*. https://gitee.com/NanGePlus/PydanticAITest
56. *GitHub - RamiAwar/dataline: Chat with your data - AI data analysis and visualization on CSV, Postgres, MySQL, Snowflake, SQLite... · GitHub*. https://github.com/RamiAwar/dataline
57. *Report of JPMorgan Chase & Co. Management Task Force Regarding 2012 CIO Losses January 16, 2013*. https://ypfsresourcelibrary.blob.core.windows.net/fcic/YPFS/JPMorgan%20Management%20Task%20Force%20Regarding%202012%20CIO%20Losses%201-16-13.pdf
58. *GitHub - premAI-io/premsql: End-to-End Local-First Text-to-SQL Pipelines · GitHub*. https://github.com/premai-io/premsql
59. *GitHub - pillarliang/py-nl2sql: A toolkit for converting natural language to SQL statements. · GitHub*. https://github.com/pillarliang/py-nl2sql
60. *GitHub - BeachWang/DAIL-SQL: A efficient and effective few-shot NL2SQL method on GPT-4. · GitHub*. https://github.com/BeachWang/DAIL-SQL
61. *GitHub - wbbeyourself/MAC-SQL: MAC-SQL: A Multi-Agent Collaborative Framework for Text-to-SQL · GitHub*. https://github.com/wbbeyourself/MAC-SQL
62. *GitHub - MohammadrezaPourreza/Few-shot-NL2SQL-with-prompting · GitHub*. https://github.com/MohammadrezaPourreza/Few-shot-NL2SQL-with-prompting
63. *api.github.com*. https://api.github.com/repos/RUCKBReasoning/OmniSQL
64. *Xiyansql Qwencoder*. https://api.github.com/repos/XGenerationLab/XiYanSQL-QwenCoder
65. [GitHub - HKUSTDial/Alpha-SQL: 🔥[ICML'25] Official repository for the paper "Alpha-SQL: Zero-Shot Text-to-SQL using Monte Carlo Tree Search" · GitHub](https://github.com/HKUSTDial/Alpha-SQL)
66. *Vanna Ai*. https://api.github.com/repos/vanna-ai/vanna
67. *GitHub - NovaSky-AI/SkyRL: SkyRL: A Modular Full-stack RL Library for LLMs · GitHub*. https://github.com/NovaSky-AI/SkyRL
68. *GitHub - glee4810/TrustSQL · GitHub*. https://github.com/glee4810/TrustSQL
69. *Human error costs TransAlta $24-million on contract bids - The Globe and Mail*. https://www.theglobeandmail.com/report-on-business/human-error-costs-transalta-24-million-on-contract-bids/article18285651
70. *TRANSALTA CORP 6-K filed February 2, 2004*. https://www.sec.gov/Archives/edgar/data/1144800/000113717104000110/f6k2003q4tac.htm
71. *Citigroup wins appeal over mistaken Revlon wire transfer*. https://www.cnbc.com/2022/09/08/citigroup-wins-appeal-over-mistaken-revlon-wire-transfer.html
72. *SkyRL-SQL: Matching GPT-4o and o4-mini on Text2SQL with Multi-Turn RL | Notion*. https://novasky-ai.notion.site/skyrl-sql
73. *GitHub - duckdb/duckdb-wasm: WebAssembly version of DuckDB · GitHub*. https://github.com/duckdb/duckdb-wasm
74. *premai-io/prem-1B-SQL · Hugging Face*. https://huggingface.co/premai-io/prem-1B-SQL
75. *GitHub - ggml-org/llama.cpp: LLM inference in C/C++ · GitHub*. https://github.com/ggml-org/llama.cpp
76. *Qwen/Qwen2.5-Coder-3B-Instruct-GGUF · Hugging Face*. https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF
77. *DualSQL: Text-to-SQL with Multi-Agent Reinforcement Learning*. https://arxiv.org/html/2609.18135v1
78. *GitHub - mlc-ai/web-llm: High-performance In-browser LLM Inference Engine · GitHub*. https://github.com/mlc-ai/web-llm
79. *BVI-AOM: A New Training Dataset for Deep Video Compression Optimization The authors would like to acknowledge funding from Netflix Inc., University of Bristol, and the UKRI MyWorld Strength in Places Programme (SIPF00006/1). For the purpose of open access, the author has applied a Creative Commons Attribution (CC BY) license to any Author Accepted Manuscript version arising.*. https://arxiv.org/html/2408.03265
80. *NSF-SciFy: Mining the NSF Awards Database for Scientific Claims*. https://arxiv.org/html/2503.08600
81. *Llama 3 Sqlcoder 8B*. https://huggingface.co/api/models/defog/llama-3-sqlcoder-8b
82. *Prem 1B Sql*. https://huggingface.co/api/models/premai-io/prem-1B-SQL
83. *Arctic Text2Sql R1 7B*. https://huggingface.co/api/models/Snowflake/Arctic-Text2SQL-R1-7B
84. *Omnisql 7B*. https://huggingface.co/api/models/seeklhy/OmniSQL-7B
85. *Xiyansql Qwencoder 3B 2504*. https://huggingface.co/api/models/XGenerationLab/XiYanSQL-QwenCoder-3B-2504
86. *MPX0222forHF/SQL-R1-3B · Hugging Face*. https://huggingface.co/MPX0222forHF/SQL-R1-3B
87. *MPX0222forHF/SQL-R1-7B · Hugging Face*. https://huggingface.co/MPX0222forHF/SQL-R1-7B
88. *GitHub - ContextualAI/bird-sql: ContextualAI's text-to-SQL pipeline for BIRD benchmark · GitHub*. https://github.com/ContextualAI/bird-sql
89. *distil-labs/distil-qwen3-4b-text2sql-gguf-4bit · Hugging Face*. https://huggingface.co/distil-labs/distil-qwen3-4b-text2sql-gguf-4bit
90. *api.github.com*. https://api.github.com/repos/sqlchat/sqlchat
91. *Text2Sql Framework*. https://api.github.com/repos/Text2SqlAgent/text2sql-framework
92. *api.github.com*. https://api.github.com/repos/RamiAwar/dataline
93. *Pandas Ai*. https://api.github.com/repos/Sinaptik-AI/pandas-ai
94. *Premai Io*. https://api.github.com/repos/premai-io/premsql
95. *api.github.com*. https://api.github.com/repos/Canner/WrenAI
96. *api.github.com*. https://api.github.com/repos/Dataherald/dataherald
97. *Eosphoros Ai*. https://api.github.com/repos/eosphoros-ai/DB-GPT
98. *api.github.com*. https://api.github.com/repos/OtterMind/Chat2DB
99. *api.github.com*. https://api.github.com/repos/dataease/SQLBot
100. *Idea Finai*. https://api.github.com/repos/IDEA-FinAI/SQL-R1
101. *Dail Sql*. https://api.github.com/repos/BeachWang/DAIL-SQL
102. *Mac Sql*. https://api.github.com/repos/wbbeyourself/MAC-SQL
103. *Alpha Sql*. https://api.github.com/repos/HKUSTDial/Alpha-SQL
104. *api.github.com*. https://api.github.com/repos/ShayanTalaei/CHESS
105. *CHASE-SQL: Multi-Path Reasoning and Preference Optimized Candidate Selection in Text-to-SQL*. https://arxiv.org/html/2410.01943
106. *ReFoRCE: A Text-to-SQL Agent with Self-Refinement, Consensus Enforcement, and Column Exploration*. https://arxiv.org/html/2502.00675
107. *DB-Explore: Automated Database Exploration and Instruction Synthesis for Text-to-SQL*. https://arxiv.org/html/2503.04959v1
108. *QueryGPT – Natural Language to SQL Using Generative AI*. https://www.uber.com/us/en/blog/query-gpt
109. *Inside OpenAI's in-house data agent | OpenAI*. https://openai.com/index/inside-our-in-house-data-agent
110. *Unified Context-Intent Embeddings for Scalable Text-to-SQL | by Pinterest Engineering*. https://medium.com/pinterest-engineering/unified-context-intent-embeddings-for-scalable-text-to-sql-793635e60aac
111. *%cortex-analyst% Verified Query Repository*. https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository
112. *%cortex-analyst% evaluations*. https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst-evaluations
113. *Test and monitor a Genie Agent | Databricks on AWS*. https://docs.databricks.com/aws/en/genie/monitor
114. *Looker business intelligence platform embedded analytics | Google Cloud*. https://looker.com/
115. *We removed 80% of our agent's tools*. https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools
