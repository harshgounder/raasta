<!-- run id: trun_3b693d434bb94e6dabd881b185649dc4 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6dabd881b185649dc4
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:11.506465Z
**Modified:** 2026-10-24T09:01:28.000181Z

## Output

# Build a RAG Failure Lab From Reusable Open Tools

## Executive Summary

- **Build An Integration, Not Another Judge**: Ragas, DeepEval, and RAGChecker already supply substantial evaluation machinery; RAGChecker explicitly separates retriever and generator diagnostics. Your differentiator should be the explanation of *why* an answer failed and the side-by-side evidence display. -> Reuse scorers and build the diagnostic workflow. [20][23][25]
- **The Twelve Requested Names Are Real, But Their Roles Differ**: Some are scoring libraries, some are observability systems, and some have changed direction. Current AutoRAG describes a librarian agent, while Giskard distinguishes its new v3 from the older RAGET workflow. -> Pin an inspected version rather than copying an old comparison article. [21][26]
- **Four Small-Detector Leads Are Real**: LettuceDetect, HHEM, MiniCheck, and Lynx exist, but differ in output granularity, compute needs, and licensing. -> Use a grounding detector as one component, not as a complete RAG evaluator. [5][1][31][42]
- **CPU-First Is Plausible, Not Universal**: Vectara reports that HHEM uses less than 600 MB RAM and takes around 1.5 seconds for a 2,000-token example on a modern x86 CPU. These are publisher claims, not measurements from this research. ARES documents a much heavier workflow, including A100-scale requirements. -> Prefer HHEM for the first offline experiment; do not promise that every evaluator runs comfortably on a laptop. [1][22]
- **A Dashboard Is Not A Root-Cause Engine**: Langfuse, Phoenix, Opik, and MLflow can help expose traces and evaluations, but the requested retrieval-versus-generation explanation still needs explicit diagnostic logic. -> Keep one presentation layer and attach scorers behind it. [10][24][39][58]
- **Licenses Change The Shortlist**: Phoenix uses Elastic License 2.0; Lynx's inspected 8B weights use CC BY-NC 4.0; AutoRAG's librarian engine and Dazzi desktop have different licenses. -> Separate permissive code, restricted weights, and source-available products before merging anything. [24][42][21]
- **The Closest Small Prototypes Deserve Inspection**: RAG Auditor documents synthetic questions, evaluation, and root-cause reporting; an adversarial RAG harness documents failure clustering and a dashboard. Both are tiny repositories, and the latter's license was not established. -> Treat them as accelerators to inspect, not proven production foundations. [69][8][87][88]
- **Real Costs Make The Demo Understandable**: Air Canada's misleading chatbot advice led to a CA$812.02 award including interest and fees; fabricated legal citations led to a $5,000 US federal-court penalty in Mata v. Avianca. -> Demonstrate a supported answer, an unsupported answer, and a missing-evidence answer using the same visible policy documents. [57][99]

**Bottom line:** my recommended hackathon stack is **Ragas or DeepEval + RAGChecker-style diagnostics + HHEM or LettuceDetect + a custom Streamlit screen**. Add Langfuse only if trace persistence is important. This is an engineering recommendation, not a benchmark result.

The inventory below is a broad reuse map, **not a defensible claim to enumerate every project worldwide**. Repository dates and stars are retrieved metadata snapshots available to this research, not synchronized live counts. A push date is not a release date. Published demo links are distinguished from demos whose availability was actually exercised; no load-testing or production-readiness claim is made here.

## 1. Make Retrieval Failure And Generation Failure Visibly Different

The central distinction is between **finding the evidence**, **using the evidence faithfully**, and **answering the question correctly**. These are not interchangeable. RAGChecker's documented metrics make this concrete: retriever claim recall and context precision sit alongside generator context utilization, noise sensitivity, hallucination, self-knowledge, and faithfulness. [25]

### A diagnostic contract for AI-04

| Output | What it should measure | Required inputs | What it must not silently imply |
|---|---|---|---|
| Context relevance | Whether retrieved chunks address the question | Question, retrieved chunks | That all necessary evidence was retrieved |
| Retrieval completeness | Whether required evidence appears in the retrieved set | Gold evidence or reference claims, retrieved chunks | That a relevant-looking chunk contains the answer |
| Faithfulness | Whether answer claims are supported by the supplied context | Answer, actual context sent to the generator | That the context itself is true or current |
| Answer accuracy | Whether the answer agrees with a trusted reference | Question, answer, reference answer or adjudicated facts | That accuracy can always be established without a reference |
| Failure attribution | Which stage is implicated and why | The above, chunk ranks, actual prompt context, trace | A mathematically proven causal explanation from one score |

The practical implication is simple: **an answer can be faithful to a bad document and still be wrong**. Conversely, a correct answer supplied from a model's memory can be unsupported by the uploaded documents. Your interface should show both dimensions rather than compress them into one green number.

### Case study: use RAGChecker as the diagnostic vocabulary

RAGChecker is useful because its documented decomposition is finer than "the answer failed." Its claim-level metrics can distinguish missing relevant claims from poor use of available context. Its published workflow uses claim extraction and checking, with an AWS Bedrock Llama 3 70B example, so its analysis should not be mistaken for a free, lightweight classifier. [25]

For the hackathon, translate those measurements into plain-language reason codes. For example, "the policy exception was absent from the retrieved chunks" is a retrieval diagnosis; "the exception was present, but the answer contradicted it" implicates generation. These are your application's diagnostic interpretations, not pre-existing guarantees supplied by the library.

### Recommended failure rules

| Observed condition | Dashboard label | Suggested next action |
|---|---|---|
| Required evidence missing; answer wrong | Retrieval suspect | Inspect chunking, filters, ranking, and top-k |
| Supporting evidence present; answer unsupported | Generation suspect | Inspect instructions and claim-level support |
| Evidence retrieved but removed before the model call | Context-assembly failure | Inspect truncation, reranking, and prompt construction |
| Retrieval poor and answer also invents facts | Mixed failure | Report both causes rather than forcing a binary label |
| Answer follows an obsolete or incorrect source | Source-quality failure | Replace or version the source |
| No trusted reference exists | Accuracy unknown | Score support, but do not certify truth |
| Evaluators disagree | Review required | Expose both judgments and supporting spans |

**Decision:** implement an **oracle-context replay**: keep the generator fixed, substitute known-good evidence, and compare the answer. Treat the result as diagnostic evidence, not formal causal proof. Controlled retrieval conditions are also relevant to the research direction represented by RAG-Safety-Bench. [55]

## 2. The Twelve Requested Frameworks: What To Fork

### Reading the capability tables

- **D1:** the requested scoring backend. **Y** means documented coverage of the requested scoring family; **P** means only part of it, configurable integration, or a different notion of correctness.
- **D2:** synthetic questions from documents. **P** includes generic synthetic data or adversarial generation requiring adaptation.
- **D3:** automated failure/root-cause reporting. **P** includes traces, metric explanations, or labels that still need your diagnostic rules.
- **D4:** the requested single-screen evidence-and-answer dashboard. **P** means a useful UI exists, but the exact AI-04 layout still needs work.
- **-:** not established in the inspected material. This is not proof the feature is impossible or absent from every version.
- **Demo Y:** a published hosted endpoint exists. **Demo N:** no hosted live demo was verified; a local demo, notebook, video, or screenshot may still exist.
- Dashboard assessments below are **desk assessments of suitability**, not hands-on usability scores.

### Identity, maintenance, and license

| Project and URL | Plain-words description | Last push snapshot | License | Stars snapshot |
|---|---|---:|---|---:|
| **Ragas** - https://github.com/vibrantlabsai/ragas | Evaluation metrics and synthetic test-set generation for RAG and related applications | 2026-02-24 | Apache-2.0 | 16,034 [14] |
| **DeepEval** - https://github.com/confident-ai/deepeval | Python testing framework with RAG-specific metrics and synthetic data | 2026-10-16 | Apache-2.0 | 18,938 [16] |
| **TruLens** - https://github.com/truera/trulens | Instrument applications and evaluate their traces and responses | 2026-10-08 | MIT | 3,594 [28] |
| **ARES** - https://github.com/stanford-futuredata/ARES | Research framework using trained judges and statistical calibration for RAG evaluation | 2025-03-28 | Apache-2.0 | 738 [30] |
| **RAGChecker** - https://github.com/amazon-science/RAGChecker | Claim-level evaluation that separates retriever and generator behavior | 2024-12-13 | Apache-2.0 | 1,126 [29] |
| **Phoenix** - https://github.com/Arize-ai/phoenix | Self-hostable AI observability and evaluation application | 2026-10-15 | **Elastic License 2.0**, not unrestricted OSI open source | 11,841 [13][24] |
| **Langfuse** - https://github.com/langfuse/langfuse | Trace, dataset, and evaluation infrastructure for LLM applications | 2026-10-21 | MIT core; exceptions for enterprise directories | 36,132 [27][10] |
| **Giskard** - https://github.com/Giskard-AI/giskard-oss | Current agent/security testing plus a legacy RAG evaluation lineage | 2026-10-12 | Apache-2.0 | 5,888 [17] |
| **promptfoo** - https://github.com/promptfoo/promptfoo | Configurable evaluation and red-teaming with a local results viewer | 2026-10-23 | MIT | 26,337 [33] |
| **UpTrain** - https://github.com/uptrain-ai/uptrain | LLM evaluation, RAG metrics, failure analysis, and a self-hosted dashboard | 2024-08-18 | Apache-2.0 | 2,367 [92][11] |
| **continuous-eval** - https://github.com/relari-ai/continuous-eval | Modular evaluation of retrieval and generated answers | 2026-08-10 | Apache-2.0 | 517 [46] |
| **AutoRAG** - https://github.com/Marker-Inc-Korea/AutoRAG | Current repository centers on a librarian agent, not simply the older RAG optimizer | 2026-10-24 | Librarian engine Apache-2.0; Dazzi desktop FSL-1.1-MIT | 5,174 [15][21] |

The maintenance dates should influence inspection priority, not become a proxy for correctness. In particular, RAGChecker can remain useful despite an older push date, while an actively changing repository can invalidate an old integration tutorial.

### Deliverable coverage, execution, demos, and combinations

| Project | D1 | D2 | D3 | D4 | Runtime and API dependence | Live demo | Dashboard suitability | Combine with |
|---|:---:|:---:|:---:|:---:|---|---|---|---|
| Ragas | Y | Y | P | - | Python; documented API examples; judge/model choice determines compute | N | Bring your own UI | HHEM, RAGChecker, Streamlit [20] |
| DeepEval | Y | Y | P | - | Python; API or supported local models | N for an OSS hosted dashboard | Test-first; do not confuse Confident AI's hosted features with the OSS package | Streamlit or Langfuse [23] |
| TruLens | P | - | P | P | Instrumentation plus evaluator/model dependencies | N; Colab published | Trace-oriented; verify the bundled UI for the chosen version | Ragas or MiniCheck [18] |
| ARES | P | Y | P | P | Training/calibration workflow can be heavy; local vLLM and API paths documented | Y: https://ares-ai.vercel.app/ | Research demonstration, not an assumed production AI-04 screen | Human-labeled calibration set; custom UI [22] |
| RAGChecker | Y | - | Y | - | CLI/Python; documented Bedrock large-model workflow | N | No turnkey dashboard established | Ragas questions; custom dashboard [25] |
| Phoenix | P | - | P | P | Self-hosted application; evaluator compute is separate | N verified | Strong observability candidate; custom paired evidence view still needed | Ragas or DeepEval [24] |
| Langfuse | P | - | P | P | Self-host via Docker/Kubernetes; attach evaluator services | Y: https://langfuse.com/demo | Strong traces/datasets; not a semantic root-cause engine by itself | Ragas, DeepEval, HHEM [10] |
| Giskard | P | Y, version-dependent | P | P | Current scans document Python 3.12+ and provider integration | N verified | Scan/report orientation; legacy RAGET differs from v3 | Pin legacy RAGET if needed, or use current scans separately [26] |
| promptfoo | P | P | P | P | CLI/library; provider-dependent model calls | N verified | Strong regression grid; not naturally a retrieved-text evidence panel | RAG scorers and custom assertions [12] |
| UpTrain | P | - | Y | P | Python/API evaluation; self-hosted dashboard via Docker | Y: https://demo.uptrain.ai/evals_demo/ | Useful beta dashboard and failure-pattern orientation | Synthetic generator plus custom reference checks [11] |
| continuous-eval | P | - | P | - | Deterministic metrics plus LLM metrics requiring a provider key | N | Library, not a dashboard | Streamlit; separate question generator [19] |
| AutoRAG, current | - | - | - | - | Current engine documents Node 24+, Bun, and model login/API paths | N verified | Librarian/desktop interfaces are not an evaluation dashboard | Use as the RAG system under test, or inspect a historical optimizer tag [21] |

**Decision:** for AI-04, the most direct starting points are **Ragas/DeepEval for tests**, **RAGChecker for decomposition**, and **UpTrain for an existing evaluation-dashboard approach**. Langfuse and Phoenix are better considered observability shells than substitutes for the scoring backend.

### Case study: Giskard and AutoRAG expose version-drift risk

Giskard's current documentation explicitly separates a v3 rewrite from v2, which is no longer actively maintained. The older RAGET workflow generates questions, reference answers, and context, while current material emphasizes dynamic and adversarial testing. A tutorial saying "Giskard does document-grounded RAG test generation" can therefore be relevant but version-incomplete. [26]

AutoRAG presents a different divergence: the current repository is organized around a librarian agent with several user surfaces. Its datasource "doctor" is not automatically a retrieval-versus-hallucination evaluator. The practical lesson is to select the actual artifact you need: current engine, historical optimizer, or evaluation library. A familiar project name is not a stable feature contract. [21]

## 3. Four Hallucination Detectors, Four Different Trade-Offs

These models mainly answer **"is this claim supported by this context?"** They do not independently supply retrieval recall, a trusted answer key, synthetic questions, and a complete dashboard.

### Models, licenses, and maintenance

| Project/model and URL | Plain-words description | Last update established | License | Popularity |
|---|---|---|---|---|
| **LettuceDetect** - https://github.com/KRLabsOrg/LettuceDetect | Local hallucination detection with character/token-level unsupported spans | Repo push 2026-09-07; v0.2.2 documented July 5, 2026 | MIT code/models | 614 GitHub stars [45][5] |
| **HHEM 2.1 Open** - https://huggingface.co/vectara/hallucination_evaluation_model | Scores whether a response follows from supplied evidence | Release/citation material establishes 2024; latest modification not established | Apache-2.0 | GitHub stars N/A; 370 HF likes observed [1] |
| **MiniCheck** - https://github.com/Liyan06/MiniCheck ; model: https://huggingface.co/lytang/MiniCheck-Flan-T5-Large | Checks factual support for individual claims | Repo push 2025-08-27 | Apache-2.0 code; inspected Flan-T5 weights MIT; do not generalize to every variant | 228 GitHub stars [43][31][32] |
| **Lynx** - https://github.com/patronus-ai/Lynx-hallucination-detection ; model: https://huggingface.co/PatronusAI/Llama-3-Patronus-Lynx-8B-Instruct | Larger instruction-tuned hallucination judge | Repo push 2024-07-10 | Repository license not resolved; inspected 8B weights **CC BY-NC 4.0** | 47 GitHub stars [44][42] |

### Practical fit

| Detector | D1 | D2 | D3 | D4 | Runtime | Live demo | Dashboard quality | Combine with |
|---|:---:|:---:|:---:|:---:|---|---|---|---|
| LettuceDetect | P: support only | - | P: offending spans | P: local demo | Local encoders and a generative variant; benchmark your actual CPU rather than borrowing GPU claims | N hosted; local Streamlit demo documented | Especially useful for red span highlighting | Ragas/DeepEval plus custom root-cause rules [5] |
| HHEM | P: support only | - | P: support score/sentence checks | P: demo | Approximately 0.1B parameters; publisher gives explicit CPU/RAM claims | Y: https://huggingface.co/spaces/vectara/hhem-2.1-open-demo | Simple detector demonstration, not a full pipeline | CPU-first FastAPI scorer and Ragas [1] |
| MiniCheck | P: support only | - | P: sentence-level flags | P: notebook/service example | Flan-T5-Large variant is 770M; documented larger-model benchmarks use substantial GPU hardware; CPU speed not established | Published Bespoke playground, but exact model/version not confirmed: https://playground.bespokelabs.ai/ | No complete OSS RAG dashboard established | RAGChecker or an answer-accuracy evaluator [31] |
| Lynx | P: support only | - | P: judge explanation | - | Inspected 8B model; larger than the encoder options; not my default small-server choice | N verified | Bring your own UI | Research comparison, subject to weight-license restrictions [42] |

The takeaway is not "smallest model wins." Choose between **a score**, **unsupported spans**, and **a generative explanation**, then evaluate that choice on your own documents.

### Case study: HHEM versus LettuceDetect

HHEM is attractive for an offline demonstration because its model card makes a concrete CPU deployment claim. It evaluates context-response support and publishes an HF Space. That makes it a plausible fast gate before a more expensive judge, but its English model card and support-oriented output should not be expanded into a claim of universal multilingual answer correctness. [1]

LettuceDetect is attractive for a different reason: its span-level output maps naturally to the requested interface. Instead of only showing a red scorecard, the application can highlight the unsupported phrase in the answer. Its current documentation includes multilingual variants and a local Streamlit example. That is a UI advantage, not evidence that it will outperform HHEM or MiniCheck on your corpus. [5]

**Decision:** start with **one** detector, preserve per-claim outputs, and calibrate thresholds on a small human-reviewed set. Do not average several unrelated scores into an unexplained "hallucination percentage."

## 4. Observability And Synthetic-Data Building Blocks Beyond The Usual List

These projects are useful additions, but most are not complete document-to-question-to-root-cause applications. Their value lies in reusable tracing, evaluation infrastructure, or data generation. Opik, for example, documents tracing, automated evaluation, and dashboards; Distilabel documents synthetic-data and AI-feedback pipelines. [39][70]

### Metadata and purpose

| Project and URL | Plain-words description | Last push | License | Stars |
|---|---|---:|---|---:|
| **Opik** - https://github.com/comet-ml/opik | Trace and evaluate LLM applications with an observability UI | 2026-10-13 | Apache-2.0 | 22,553 [50] |
| **LangWatch / LangEvals** - https://github.com/langwatch/langwatch | Observability, evaluations, and simulation tooling; LangEvals moved into the monorepo | 2026-10-24 | Apache-2.0 | 4,990 [96][34] |
| **Evidently** - https://github.com/evidentlyai/evidently | Reports and monitoring with ranking, similarity, and LLM-related metrics | 2026-09-29 | Apache-2.0 | 7,984 [93] |
| **MLflow** - https://github.com/mlflow/mlflow | General experiment tracking extended to LLM traces and evaluation | 2026-10-21 | Apache-2.0 | 28,470 [94] |
| **Weave** - https://github.com/wandb/weave | Instrument functions and compare LLM/agent evaluations | 2026-10-08 | Apache-2.0 | 1,137 [77] |
| **OpenEvals** - https://github.com/langchain-ai/openevals | Ready-made evaluators to embed in another application | 2026-10-22 | MIT | 1,230 [76] |
| **Distilabel** - https://github.com/argilla-io/distilabel | Generate synthetic datasets and AI feedback using configurable models | 2026-10-19 | Apache-2.0 | 3,435 [84] |

### Deliverable and deployment fit

| Project | D1 | D2 | D3 | D4 | Runtime | Live demo | Dashboard suitability | Combine with |
|---|:---:|:---:|:---:|:---:|---|---|---|---|
| Opik | P | - | P | P | Self-hosted components and Python/TS SDKs; judge compute separate | N verified | Strong observability candidate | Ragas and HHEM [39] |
| LangWatch/LangEvals | P | P: simulations | P | P | Current setup documents Node 24; evaluator dependencies vary | N; introduction video is not a live app | Promising combined platform; exact AI-04 panel unconfirmed | Ragas or OpenEvals [62] |
| Evidently | P | - | P | P | Local reports/monitoring; LLM checks depend on configured models | Y: https://demo.evidentlyai.com/ | Strong monitoring/reporting, not specifically evidence beside answer | Retrieval metrics and Ragas [61] |
| MLflow | P | - | P | P | Local server documented; evaluator model requirements vary | Y: https://demo.mlflow.org/ | Strong tracking; more infrastructure than a small bespoke screen | Existing scorers [58] |
| Weave | P | - | P | P | SDK plus evaluation/model dependencies; full self-hosted UI path not established here | N; Colab available | Hosted-oriented integration needs inspection | Ragas or MiniCheck [73] |
| OpenEvals | P | - | P | - | Evaluator library; model/provider dependent | N verified | None standalone | Langfuse, Phoenix, or your UI [66] |
| Distilabel | P: feedback | P: generic generation | - | - | API, Transformers, and vLLM backends documented | N verified | Pipeline library, not a dashboard | Ragas-style document question generation [70] |

Do not count LangEvals and its new monorepo home as two independent active systems. Likewise, do not count a commercial dashboard as an OSS deliverable merely because an accompanying SDK is open source.

### Case study: Langfuse versus Phoenix as the shell

Langfuse offers datasets, tracing, and self-hosted deployment, making it a reasonable place to retain questions, outputs, scores, timings, and evaluator versions. Its MIT core is attractive for a permissive integration, but enterprise directory exceptions still matter. [10]

Phoenix offers a self-hostable observability application and deployment options, but uses Elastic License 2.0. The operational attraction and the legal classification are separate questions: a useful self-hosted product is not automatically unrestricted open source. For a hackathon, either may work; for a redistributed commercial fork, the distinction deserves review. [24]

**Decision:** choose **one** trace store. Two observability platforms rarely make a short demonstration clearer; a well-designed evidence panel usually does.

## 5. Research, Attribution, Benchmarks, And Tiny Repositories Worth Mining

The most valuable niche projects contribute a missing mechanism: automatic questions, claim labels, model-internal attribution, pairwise ranking, adversarial conditions, or performance measurements. They should not all be presented as interchangeable RAG evaluators.

### Metadata and reusable contribution

| Project and URL | Plain-words contribution | Last push/update established | License | Stars |
|---|---|---|---|---:|
| **BenchmarkQED** - https://github.com/microsoft/benchmark-qed | Automated benchmark construction and evaluation, including generated queries | 2026-10-23 | MIT | 102 [48][35] |
| **open-rag-eval** - https://github.com/vectara/open-rag-eval | Generate queries, evaluate RAG/retrieval, and inspect results in a viewer | 2026-10-08 | Apache-2.0 | 417 [47][40] |
| **OpenBMB RAGEval** - https://github.com/OpenBMB/RAGEval | Scenario/schema-driven generation of documents, questions, answers, and references | 2025-04-02 | License not resolved in retrieved metadata | 240 [80][75] |
| **RAGElo** - https://github.com/zetaalphavector/RAGElo | Compare retrieval/answer alternatives with pairwise judgments and Elo ratings | 2026-09-24 | Apache-2.0 | 133 [85][71] |
| **MIRAGE** - https://github.com/Betswish/MIRAGE | Attribute generated text to documents using model-internal saliency | 2025-03-10 | Apache-2.0 | 25 [95][54] |
| **RAGTruth** - https://github.com/ParticleMedia/RAGTruth | Word-level hallucination annotations and detector training/evaluation resources | 2024-12-02 | MIT repository; inspect individual data artifacts as well | 278 [81][59] |
| **RAGBench** - https://github.com/rungalileo/ragbench | Reproducible RAG benchmark/evaluation resources | 2024-06-12 | Repository license not resolved | 24 [86][63] |
| **AlignScore** - https://github.com/yuh-zha/AlignScore | Score factual consistency between context and claims | 2024-03-11 | MIT code; weight license not established here | 177 [82][72] |
| **SelfCheckGPT** - https://github.com/potsawee/selfcheckgpt | Detect suspicious sentences using disagreement among sampled answers | 2024-06-26 | MIT | 636 [83][60] |
| **RAGMark** - https://github.com/zferic/RAGMark | Benchmark quality and performance across RAG pipeline stages | 2026-10-02 | MIT | 2 [91][64] |
| **RAG-Safety-Bench** - https://github.com/The-Safe-AI-Lab/RAG-Safety-Bench | Compare safety under oracle, on-topic, random, and non-RAG conditions | Latest repository update not established | Benchmark CC BY-SA 4.0; code licensing needs separate inspection | Not established [55] |
| **RAG Auditor** - https://github.com/amitgambhir/rag-auditor | Small end-to-end evaluation prototype with synthetic questions and failure reports | 2026-04-19 | MIT | 1 [87][69] |
| **Adversarial RAG evaluation harness** - https://github.com/ShivanshSharma007s/Adversarial-RAG-evaluation-harness | Adversarial contexts, proxy scores, failure clustering, and FastAPI dashboard | 2026-07-10 | Not established | 1 [88][8] |

Small repositories are especially useful for inspecting UI and orchestration ideas. Their existence, however, does not establish robust tests, safe dependencies, or reliable evaluator calibration.

### Deliverables, execution, and pairing

| Project | D1 | D2 | D3 | D4 | Runtime | Live demo | Dashboard suitability | Combine with |
|---|:---:|:---:|:---:|:---:|---|---|---|---|
| BenchmarkQED | P | Y | - | - | Model/backend dependent; small-server requirements not established | N verified | No AI-04 dashboard established | RAGChecker [35] |
| open-rag-eval | P | Y | P | P | Python/Flask evaluation paths; backend dependent | Y: https://openevaluation.ai/ | Useful evaluation viewer | HHEM or RAGChecker [40] |
| OpenBMB RAGEval | P | Y | P | - | Generation/evaluation LLM dependencies | N verified | No turnkey dashboard established | Scoring backend plus custom UI [75] |
| RAGElo | P | - | - | - | LLM pairwise judgments | N verified | Library/results rather than evidence UI | Ragas for absolute criteria [71] |
| MIRAGE | P | - | Y: attribution | P | Needs access to generator internals; not an arbitrary closed API wrapper | Y: https://huggingface.co/spaces/gsarti/mirage | Useful attribution demonstration | Open-weight generator plus RAGChecker [54][65] |
| RAGTruth | P: detector test data | - | P: annotated spans | - | Dataset usable locally; training depends on chosen model | N verified | None established | Calibrate LettuceDetect/MiniCheck [59] |
| RAGBench | P | - | P: benchmark diagnostics | - | Dataset/model-dependent | N verified | None established | ARES or RAGChecker [63] |
| AlignScore | P: consistency | - | P | - | PyTorch; documented examples default to CUDA | N verified | None established | Ragas [72] |
| SelfCheckGPT | P: consistency, not grounding | - | P: sentence flags | - | CPU/GPU or API options, depending on method | N; local notebook | None established | Evidence-grounded checker such as HHEM [60] |
| RAGMark | P: quality/performance | - | P: stage bottlenecks | P: plots | CPU/GPU placement configurable; actual model dictates hardware | N verified | Benchmark plots, not paired evidence cards | Semantic scorer such as Ragas [64] |
| RAG-Safety-Bench | P: safety | - | P: controlled conditions | - | Model-dependent research setup | N verified | None established | Your oracle-context replay suite [55] |
| RAG Auditor | P | Y | Y, documented | P | Anthropic API documented | N verified | Close prototype candidate; inspect implementation | HHEM and stronger reference checks [69] |
| Adversarial harness | P: several proxy metrics | P | Y, documented | P | Groq API documented | N verified | Small interactive prototype | Licensed scorer library; resolve fork rights first [8] |

**Important distinction:** RAGTruth is a hallucination-annotation resource, **not** a generator of questions from newly uploaded documents. SelfCheckGPT's consistency signal is also not proof of grounding: repeated answers can agree while remaining unsupported.

### Case study: MIRAGE explains influence; RAGMark explains bottlenecks

MIRAGE uses model-internal saliency to connect generated tokens to source documents, including evaluation on multilingual question answering. This provides a different kind of explanation from asking another LLM to justify a score. Its limitation is architectural: access to model internals makes it unsuitable as a drop-in attribution layer for every closed model API. [54]

RAGMark instead examines pipeline quality and performance, including retrieval, reranking, compression, generation, and CPU/GPU placement. Its associated 2026 paper includes quality and performance measurements such as retrieval recall, latency, throughput, and energy. That can explain *where a pipeline slows down*, but it is not automatically an explanation of *which unsupported statement caused a wrong answer*. [64][53]

**Decision:** keep semantic failure attribution, document influence, and performance attribution as separate tabs or labels. They answer different questions.

### Papers with code to prioritize

| Research artifact | Established timing | Why it matters to AI-04 |
|---|---|---|
| OpenBMB RAGEval | ACL 2025 paper: https://aclanthology.org/2025.acl-long.418 ; arXiv 2408.01262 | Scenario-specific synthetic evaluation rather than generic trivia [52] |
| RAGMark | 2026 paper: https://arxiv.org/pdf/2609.05760 | Adds pipeline-stage performance diagnosis [53] |
| RAG-Safety-Bench | arXiv 2609.11758 | Controlled retrieval conditions useful for adversarial and oracle-context tests [55] |

These supplement, rather than invalidate, the older RAGChecker, ARES, MiniCheck, and RAGTruth codebases. A recent publication date alone is not a reason to replace a better-fitting component.

## 6. Chinese And Korean Projects: Useful Originals, Plus Explicit Gaps

The strongest regional additions in this inventory are **EvalScope, FlashRAG, UltraRAG, CRUD-RAG, and Korean-origin AutoRAG**, not an inflated count of mirrors. They range from general evaluation runners to RAG workflow builders and language-specific benchmarks. [37][74][68][38][21]

### Regional project metadata

| Project and URL | Plain-words description | Last push | License | Stars |
|---|---|---|---|---:|
| **EvalScope** - https://github.com/modelscope/evalscope | ModelScope evaluation runner with local/API execution and visualization | 2026-10-23 | Apache-2.0 | 3,583 [51][37] |
| **FlashRAG** - https://github.com/RUC-NLPIR/FlashRAG | RAG algorithms, datasets, benchmarking, and a local playground | 2026-10-12 | MIT | 3,593 [78][74] |
| **UltraRAG** - https://github.com/OpenBMB/UltraRAG | Workflow-oriented RAG framework with evaluation and a local UI | 2026-10-24 | Apache-2.0 | 5,731 [79][68] |
| **CRUD-RAG** - https://github.com/IAAR-Shanghai/CRUD_RAG | Chinese RAG benchmark with multiple answer/retrieval-related metrics | Not established; creation date is not an update date | Apache license stated; exact version not established | Not established [38] |
| **BytePioneer-AI RAGEval** - https://github.com/BytePioneer-AI/RAGEval | React/FastAPI evaluation-platform project; several engine/report features are described as planned | 2026-04-16 | MIT claimed in README; metadata license unclassified | 114 [49][41] |
| **Rag-Eval-Lab** - https://github.com/JellyZhang0101/Rag-Eval-Lab | Small Streamlit evaluation lab using retrieval and answer-similarity proxies | 2026-06-03 | README claims MIT; metadata did not identify a license | 1 [89][67] |
| **BAEM1N/RAG-Evaluation** - https://github.com/BAEM1N/RAG-Evaluation | Korean component-comparison benchmark for RAG configurations | 2026-06-10 | MIT | 3 [90] |

### Regional deliverable fit

| Project | D1 | D2 | D3 | D4 | Runtime | Live demo | Dashboard suitability | Combine with |
|---|:---:|:---:|:---:|:---:|---|---|---|---|
| EvalScope | P | - | P | P | Local models or online APIs; API evaluation documented without a GPU | N verified | React/Vite visualization; exact evidence-answer screen unconfirmed | RAG-specific scorer and test generator [37] |
| FlashRAG | P | - | P | P | vLLM and OpenAI-compatible generation paths | N hosted; local UI documented | Useful pipeline playground | RAGChecker [74] |
| UltraRAG | P | - | P | P | CPU and NVIDIA GPU Docker modes documented | N hosted; local UI on port 5050 | Useful workflow builder, not the requested dashboard out of the box | Ragas/DeepEval [68] |
| CRUD-RAG | P | - | - | - | Local/remote model paths; benchmark-specific setup | N verified | None established | FlashRAG plus a faithfulness detector [38] |
| BytePioneer RAGEval | P, partly planned | - | P, partly planned | P | React/FastAPI with LLM/RAG APIs | Y: published endpoint linked by repository; health not confirmed | Promising scaffold; do not equate roadmap with finished engine | Existing mature scorers [41] |
| Rag-Eval-Lab | P: proxy metrics | - | P | P | Local embeddings plus DeepSeek/OpenAI API paths | N; screenshot is not a live demo | Simple low-score inspection screen | HHEM for actual support checking [67] |
| BAEM1N/RAG-Evaluation | P | - | P: component comparison | - | Model-dependent; CPU-only deployment not established | N verified | Not established | RAGChecker and custom UI [90] |

**Decision:** use these projects for workflow diversity and language coverage, but do not label keyword overlap or answer similarity as full faithfulness evaluation.

### Case study: two projects named RAGEval are not the same system

OpenBMB RAGEval focuses on schema/scenario-driven generation of evaluation material and metrics including completeness, hallucination, and irrelevance. BytePioneer-AI RAGEval is a separate web-platform project, with React/FastAPI components and important capabilities still described as planned. Mixing their paper, interface screenshots, stars, or licenses would create a misleading competitor profile. [75][41]

The same caution applies to regional discovery. A Gitee or GitCode mirror can improve access without being a new evaluation engine. For this hackathon, count distinct implementations and reusable components, not every hosting location.

**Japanese, Korean dataset, and competition leads that remain incomplete:** JQaRA at https://github.com/hotchpotch/JQaRA and the Korean dataset at https://huggingface.co/datasets/allganize/RAG-Evaluation-Dataset-KO are additional leads, not fully catalogued fork recommendations here. Their complete update/license/runtime/demo records were not established in this inventory. No independently licensed Baidu-specific original, distinct Gitee/GitCode original, Kaggle evaluation engine, or named RAG-evaluation hackathon winner was sufficiently established to recommend as verified. This is an inventory gap, not a claim that none exist.

For reusable demonstrations, the stronger established leads are the **HHEM HF Space**, **MIRAGE HF Space**, **open-rag-eval viewer**, and the small **RAG Auditor** implementation. [1][65][40][69]

## 7. Real Incidents: Explain The Financial Stakes Without Inventing RAG Architectures

These cases establish the cost of unsupported output. They do **not** establish that every affected system used RAG, or that a particular evaluator would certainly have prevented the incident.

| Incident | What happened | Established financial consequence | AI-04 demonstration |
|---|---|---|---|
| **Moffatt v. Air Canada**, decision February 14, 2024 | Chatbot said a bereavement discount could be requested after travel, contrary to the actual policy | **CA$650.88 damages + CA$36.14 interest + CA$125 fees = CA$812.02** | Show the policy beside the unsupported "claim later" advice [57] |
| **Mata v. Avianca**, sanctions June 22, 2023 | Lawyers submitted fabricated cases and quotations and failed to verify them adequately | **$5,000 joint-and-several US federal-court penalty** | Flag legal claims with no supporting source passage [99] |
| **Deloitte Australia report**, refund reported October 20, 2025 | AI-assisted report contained a fabricated court quotation and nonexistent academic references | AP reported **more than A$97,000 refunded** on an approximately **A$440,000** contract | Compare every citation/quotation with the retrieved source text [97] |

The strongest narrative is not "AI is dangerous." It is **"a plausible sentence can be operationally expensive when nobody can inspect its evidence."**

### Case study: Air Canada's policy contradiction

The Air Canada chatbot told the claimant that a bereavement discount could be sought within 90 days after travel. The actual policy did not allow that post-travel application. The tribunal's award separated damages, interest, and fees; CA$812.02 is the total, not merely the damages figure. The decision does not disclose enough about the chatbot's architecture to label it a confirmed RAG failure. [57]

This makes an excellent non-expert demonstration. Upload a short policy, ask the same policy question, and show three outputs: correct and supported; wrong because the relevant clause was not retrieved; wrong despite the clause being visible. The financial story supplies the stakes, while your controlled replay supplies the stage diagnosis.

### Case study: fabricated citations survive fluent prose

In Mata v. Avianca, the problem was not just that a model generated nonexistent authorities. The court also addressed the lawyers' failure to verify the material and their conduct after the problem emerged. The penalty should therefore not be described as a fine imposed on a chatbot. [99]

The Deloitte report is a more recent companion example: reporting identified fabricated references and a false court quotation, and the later report established that more than A$97,000 had actually been refunded. Earlier coverage described a promised refund, so the later paid-refund reporting is the relevant outcome. Azure OpenAI use was disclosed, but that does not establish a RAG architecture. [97][98]

**Decision:** include citation existence and quotation support in the demo. A high semantic-similarity score is not enough to establish that an authority exists or says what the answer claims.

## 8. A Judge-Friendly Demo And Ten "What If" Answers

The following is a **proposed demo design**, not a claim that the listed projects already provide the complete screen. LettuceDetect's spans, RAGChecker's stage metrics, and the observability tools' traces provide complementary ingredients. [5][25][10]

### The single screen

```text
Question: Can I claim this discount after travel?

[Context relevance] [Evidence completeness] [Faithfulness] [Accuracy]
       GREEN                RED                 RED          RED

RETRIEVED EVIDENCE                    GENERATED ANSWER
Chunk 1, rank, source, version        Answer text
Chunk 2, rank, source, version        Unsupported phrases highlighted
Actual context sent to model         Claim-to-source links

DIAGNOSIS: Retrieval suspect / Generation suspect / Mixed / Unknown
WHY: One short explanation with cited evidence
NEXT: Fix retrieval | Replay with gold context | Compare new answer
```

Use **green** for passed checks and **red** for hallucinated or missing evidence, as requested. Add **amber** for unavailable references, evaluator disagreement, and uncertain diagnoses. An unmeasurable accuracy score should not become green merely because the support checker passed.

### Ten questions and how the demo should answer

| # | What a non-expert judge asks | What the demonstration shows |
|---:|---|---|
| 1 | **"What if the answer is not in any uploaded document?"** | An unanswerable test case. The correct behavior is an explicit abstention; the dashboard marks missing evidence and distinguishes it from a fabricated answer. |
| 2 | **"What if it finds the wrong paragraph?"** | Retrieved chunks appear beside the gold evidence. Low evidence completeness triggers "retrieval suspect"; oracle-context replay tests the same generator with the right passage. |
| 3 | **"What if the right paragraph is there and it still lies?"** | The correct passage remains visible while unsupported answer claims are highlighted. The diagnostic label changes to "generation suspect." |
| 4 | **"What if only one sentence is wrong?"** | Per-claim or span-level support flags the offending sentence rather than coloring the entire answer identically. |
| 5 | **"What if two documents disagree or one is outdated?"** | Source dates/versions are visible; the result is labeled conflict or source-quality failure, rather than automatically blaming the generator. |
| 6 | **"What if I paraphrase the question or use another language?"** | Run a paraphrase/language test group and compare scores. Show the evaluator's supported languages and mark unsupported language coverage rather than pretending equivalence. |
| 7 | **"What if a document says 'ignore the rules'?"** | Include an injected instruction in a retrieved chunk. Treat injection handling as a separate adversarial test, not as ordinary answer relevance. |
| 8 | **"Who checks whether your evaluator is wrong?"** | Display judge/model version, evidence spans, disagreement, and a human-reviewed calibration set. Allow a reviewer to override a mistaken label with a recorded explanation. |
| 9 | **"Can private documents stay offline?"** | Show the selected local-only mode and its limitations. HHEM can be the local support-checking candidate; question generation and reference grading also need local models if no data may leave the machine. |
| 10 | **"What happens with hundreds of questions or a slow laptop?"** | Display stage latency, model/API calls, caching, and estimated or measured cost separately. Run a small batch first; do not present a publisher's GPU benchmark as your laptop's speed. |

These questions make the demonstration understandable without hiding uncertainty. They also prevent the common mistake of presenting a single red/green score as a complete explanation.

### Minimum backend record

Persist the question, reference answer, reference evidence IDs, retrieved chunk IDs and ranks, actual generator context, generated answer, claim-level support, answer/reference comparison, reason code, evaluator version, timing, and cost. Keeping **retrieved text** and **actual model context** separately is important: otherwise context truncation can be misdiagnosed as hallucination despite supposedly "good retrieval."

**Decision:** prepare a small, deliberately varied evaluation set before optimizing the interface: supported answers, missing evidence, distractor retrieval, contradicted answers, mixed-quality answers, stale/conflicting sources, and injected instructions. Present these as controlled tests, not as a statistical guarantee of production reliability.

## 9. Synthesis: Which Combination Wins For This Hackathon?

The central trade-off is between **speed to a clear demonstration**, **depth of diagnosis**, **deployment cost**, and **freedom to redistribute**. The inventory contains tools for each dimension, but no inspected component should be assumed to satisfy the complete AI-04 contract without integration.

| Strategy and representative projects | Main mechanism | Scope | Principal trade-off | Best time horizon |
|---|---|---|---|---|
| **Metric-first:** Ragas, DeepEval, continuous-eval, OpenEvals | Configurable retrieval/answer checks | Fast scoring backend | Explanations and UI need assembly | Hackathon foundation |
| **Diagnostic-first:** RAGChecker, ARES, UpTrain | Claim decomposition, calibrated judging, failure patterns | Deeper evaluation | More dependencies, compute, or calibration | Hackathon differentiator, then validation |
| **Trace-first:** Langfuse, Phoenix, Opik, LangWatch, MLflow, Weave, TruLens, Evidently | Trace storage, comparisons, monitoring | Operational visibility | Trace visibility does not itself establish root cause; licenses differ | Persistent team workflow |
| **Detector-first:** HHEM, LettuceDetect, MiniCheck, Lynx, AlignScore | Context-claim support detection | Fast or fine-grained grounding checks | Not full answer truth or retrieval completeness; weight licenses vary | Local scoring and highlighting |
| **Test-data-first:** BenchmarkQED, OpenBMB RAGEval, Distilabel, RAGTruth, RAGBench, CRUD-RAG | Synthetic cases or labeled benchmarks | Repeatable evaluation | Generated data and fixed benchmarks may miss local failure modes | Before and after the demo |
| **Comparison/attribution:** RAGElo, MIRAGE, SelfCheckGPT, RAGMark, RAG-Safety-Bench | Relative ranking, influence, consistency, performance, controlled conditions | Specialized diagnosis | Their signals answer different questions and should not be blended blindly | Advanced extension |
| **Workflow/prototype-first:** AutoRAG, FlashRAG, UltraRAG, EvalScope, BytePioneer RAGEval, Rag-Eval-Lab, BAEM1N, RAG Auditor, adversarial harness | Existing pipelines, interfaces, and examples | Rapid implementation ideas | Version drift, proxy metrics, incomplete roadmaps, or unresolved licenses | Selective code reuse |

This comparison exposes three non-obvious tensions.

**First, the best UI and the best judge may come from different projects.** An observability dashboard can look complete while lacking a gold-reference accuracy check. A small detector can provide excellent span highlighting while saying nothing about missed evidence. Combining them is useful precisely because their mechanisms differ, not because their scores are interchangeable. [10][5][25]

**Second, local does not mean lightweight, and source-visible does not mean permissively reusable.** HHEM has an explicit publisher CPU claim; ARES documents much heavier requirements. Phoenix's license and Lynx's noncommercial weights introduce different legal constraints despite both being inspectable. [1][22][24][42]

**Third, relative improvement is not absolute reliability.** RAGElo can help choose between systems; SelfCheckGPT can reveal inconsistency; MIRAGE can expose influence. None of these alone establishes that the answer matches an authoritative, current reference. [71][60][54]

### Recommended build order

1. **Implement the evaluation record and dashboard first.** Make the evidence, answer, and missing-reference state visible.
2. **Choose Ragas or DeepEval, not both initially.** Add document-derived questions and the three requested score families.
3. **Add HHEM for a CPU-first support check, or LettuceDetect for span highlighting.** Measure on the actual machine and corpus.
4. **Implement RAGChecker-inspired reason codes and oracle-context replay.** Preserve mixed and unknown outcomes.
5. **Add one trace platform only if needed.** Langfuse is a reasonable permissive-core candidate; Phoenix is a source-available alternative requiring license awareness.
6. **Use small prototypes selectively.** Inspect RAG Auditor's flow and the adversarial harness's failure cases, but do not inherit their claims or unresolved licensing without review.

**Final recommendation:** pitch the product as **"a failure microscope for RAG"**, not another hallucination score. The winning moment is when a judge changes the retrieved evidence, watches the diagnosis change, and can read exactly why.

## References

1. *vectara/hallucination_evaluation_model · Hugging Face*. https://huggingface.co/vectara/hallucination_evaluation_model
2. *GitHub - patronus-ai/Lynx-hallucination-detection*. https://github.com/patronus-ai/Lynx-hallucination-detection
3. *Releases · promptfoo/promptfoo - GitHub*. https://github.com/promptfoo/promptfoo/releases
4. *EdinburghNLP/awesome-hallucination-detection*. https://github.com/EdinburghNLP/awesome-hallucination-detection
5. *GitHub - KRLabsOrg/LettuceDetect: Span-level grounding ...*. https://github.com/KRLabsOrg/LettuceDetect
6. *GitHub - AIAnytime/Hallucination-Guard: Hallucination ...*. https://github.com/AIAnytime/Hallucination-Guard
7. *promptfoo/LICENSE at main - GitHub*. https://github.com/promptfoo/promptfoo/blob/main/LICENSE
8. *GitHub - ShivanshSharma007s/Adversarial-RAG-evaluation-harness: Custom adversarial evaluation harness for a Retrieval-Augmented Generation (RAG) system with hallucination detection, confidence calibration, failure clustering, regression testing, and an interactive FastAPI dashboard. · GitHub*. https://github.com/ShivanshSharma007s/Adversarial-RAG-evaluation-harness
9. *GitHub - Bhavanasetty/AI-Hallucination-Detection-RAG: RAG ...*. https://github.com/Bhavanasetty/AI-Hallucination-Detection-RAG/tree/main
10. *langfuse/langfuse: Open source AI engineering platform: LLM evals ...*. https://github.com/langfuse/langfuse
11. *UpTrain is an open-source unified platform to evaluate and ...*. https://github.com/uptrain-ai/uptrain
12. *GitHub - promptfoo/promptfoo: Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line and CI/CD integration.  Used by OpenAI and Anthropic. · GitHub*. https://github.com/promptfoo/promptfoo
13. *Arize Ai*. https://api.github.com/repos/Arize-ai/phoenix
14. *api.github.com*. https://api.github.com/repos/vibrantlabsai/ragas
15. *Marker Inc Korea*. https://api.github.com/repos/Marker-Inc-Korea/AutoRAG
16. *Confident Ai*. https://api.github.com/repos/confident-ai/deepeval
17. *Giskard Oss*. https://api.github.com/repos/Giskard-AI/giskard-oss
18. *GitHub - truera/trulens: Evaluation and Tracking for LLM Experiments and AI Agents · GitHub*. https://github.com/truera/trulens
19. *GitHub - relari-ai/continuous-eval: Data-Driven Evaluation for LLM-Powered Applications · GitHub*. https://github.com/relari-ai/continuous-eval
20. *GitHub - vibrantlabsai/ragas: Supercharge Your LLM Application Evaluations 🚀 · GitHub*. https://github.com/vibrantlabsai/ragas
21. *GitHub - Marker-Inc-Korea/AutoRAG: Your Personal Librarian Agent. Ask anything on your computer, organize files, remember important info and files. · GitHub*. https://github.com/Marker-Inc-Korea/AutoRAG
22. *GitHub - stanford-futuredata/ARES: Automated Evaluation of RAG Systems · GitHub*. https://github.com/stanford-futuredata/ARES
23. *GitHub - confident-ai/deepeval: The LLM Evaluation Framework · GitHub*. https://github.com/confident-ai/deepeval
24. *GitHub - Arize-ai/phoenix: AI Observability & Evaluation · GitHub*. https://github.com/Arize-ai/phoenix
25. *GitHub - amazon-science/RAGChecker: RAGChecker: A Fine-grained Framework For Diagnosing RAG · GitHub*. https://github.com/amazon-science/RAGChecker
26. *GitHub - Giskard-AI/giskard-oss: 🐢 Open-Source Evaluation & Testing library for LLM Agents · GitHub*. https://github.com/Giskard-AI/giskard-oss
27. *api.github.com*. https://api.github.com/repos/langfuse/langfuse
28. *api.github.com*. https://api.github.com/repos/truera/trulens
29. *Amazon Science*. https://api.github.com/repos/amazon-science/RAGChecker
30. *Stanford Futuredata*. https://api.github.com/repos/stanford-futuredata/ARES
31. [GitHub - Liyan06/MiniCheck: MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents [EMNLP 2024] · GitHub](https://github.com/Liyan06/MiniCheck)
32. *lytang/MiniCheck-Flan-T5-Large · Hugging Face*. https://huggingface.co/lytang/MiniCheck-Flan-T5-Large
33. *api.github.com*. https://api.github.com/repos/promptfoo/promptfoo
34. *GitHub - langwatch/langevals: LangEvals aggregates various language model evaluators into a single platform, providing a standard interface for a multitude of scores and LLM guardrails, for you to protect and benchmark your LLM models and pipelines. · GitHub*. https://github.com/langwatch/langevals
35. *GitHub - microsoft/benchmark-qed: Automated benchmarking of Retrieval-Augmented Generation (RAG) systems · GitHub*. https://github.com/microsoft/benchmark-qed
36. *GitHub - hotchpotch/JQaRA: JQaRA: Japanese Question Answering with Retrieval Augmentation - 検索拡張(RAG)評価のための日本語Q&Aデータセット · GitHub*. https://github.com/hotchpotch/jqara
37. *GitHub - modelscope/evalscope: A streamlined and customizable framework for efficient large model (LLM, VLM, AIGC) evaluation and performance benchmarking. · GitHub*. https://github.com/modelscope/evalscope
38. *GitHub - IAAR-Shanghai/CRUD_RAG: CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models · GitHub*. https://github.com/IAAR-Shanghai/CRUD_RAG
39. *GitHub - comet-ml/opik: Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards. · GitHub*. https://github.com/comet-ml/opik
40. *GitHub - vectara/open-rag-eval: RAG evaluation without the need for "golden answers" · GitHub*. https://github.com/vectara/open-rag-eval
41. *GitHub - BytePioneer-AI/RAGEval: 灵鉴 RAG评测系统 | RAGEval  ✨ 开箱即用的RAG系统自动化评估工具 | One-stop RAG Evaluation Solution · GitHub*. https://github.com/BytePioneer-AI/RAGEval
42. *PatronusAI/Llama-3-Patronus-Lynx-8B-Instruct · Hugging Face*. https://huggingface.co/PatronusAI/Llama-3-Patronus-Lynx-8B-Instruct
43. *api.github.com*. https://api.github.com/repos/Liyan06/MiniCheck
44. *Lynx Hallucination Detection*. https://api.github.com/repos/patronus-ai/Lynx-hallucination-detection
45. *api.github.com*. https://api.github.com/repos/KRLabsOrg/LettuceDetect
46. *Continuous Eval*. https://api.github.com/repos/relari-ai/continuous-eval
47. *Open Rag Eval*. https://api.github.com/repos/vectara/open-rag-eval
48. *Benchmark Qed*. https://api.github.com/repos/microsoft/benchmark-qed
49. *Bytepioneer Ai*. https://api.github.com/repos/BytePioneer-AI/RAGEval
50. *Comet Ml*. https://api.github.com/repos/comet-ml/opik
51. *api.github.com*. https://api.github.com/repos/modelscope/evalscope
52. *RAGEval: Scenario Specific RAG Evaluation Dataset Generation Framework - ACL Anthology*. https://aclanthology.org/2025.acl-long.418
53. *RAGMark: A Comprehensive Framework for Benchmarking Retrieval-Augmented Generation Systems*. https://arxiv.org/pdf/2609.05760
54. *Model Internals-based Answer Attribution for Trustworthy Retrieval-Augmented Generation - ACL Anthology*. https://aclanthology.org/2024.emnlp-main.347
55. *RAG-Safety-Bench: Reliable Evaluation of Retrieval-Augmented LLM Safety*. https://arxiv.org/html/2609.11758v1
56. *GitHub - YHPeter/Awesome-RAG-Evaluation: The official repository for the paper: Evaluation of Retrieval-Augmented Generation: A Survey. · GitHub*. https://github.com/YHPeter/Awesome-RAG-Evaluation
57. *2024 BCCRT 149 (CanLII) | Moffatt v. Air Canada | CanLII*. https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html
58. *GitHub - mlflow/mlflow: The open source AI engineering platform for agents, LLMs, and ML models. MLflow enables teams of all sizes to debug, evaluate, monitor, and optimize production-quality AI applications while controlling costs and managing access to models and data. · GitHub*. https://github.com/mlflow/mlflow
59. *GitHub - ParticleMedia/RAGTruth: Github repository for "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models" · GitHub*. https://github.com/ParticleMedia/RAGTruth
60. *GitHub - potsawee/selfcheckgpt: SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models · GitHub*. https://github.com/potsawee/selfcheckgpt
61. *GitHub - evidentlyai/evidently: Evidently is ​​an open-source ML and LLM observability framework. Evaluate, test, and monitor any AI-powered system or data pipeline. From tabular data to Gen AI. 100+ metrics. · GitHub*. https://github.com/evidentlyai/evidently
62. *GitHub - langwatch/langwatch: Open-Source Agent Observability & Evals for AI Platform teams. Trace, test, route and govern every agent & coding assistant in the company. · GitHub*. https://github.com/langwatch/langwatch
63. *GitHub - rungalileo/ragbench · GitHub*. https://github.com/rungalileo/ragbench
64. *GitHub - zferic/RAGMark: RAG Benchmarking framework · GitHub*. https://github.com/zferic/RAGMark
65. *GitHub - Betswish/MIRAGE: Easy-to-use MIRAGE code for faithful answer attribution in RAG applications. Paper: https://aclanthology.org/2024.emnlp-main.347/ · GitHub*. https://github.com/Betswish/MIRAGE
66. *GitHub - langchain-ai/openevals: Readymade evaluators for your LLM apps · GitHub*. https://github.com/langchain-ai/openevals
67. *GitHub - JellyZhang0101/Rag-Eval-Lab: A Chinese RAG evaluation dashboard for comparing chunk size, top-k retrieval, answer quality, and latency. · GitHub*. https://github.com/JellyZhang0101/Rag-Eval-Lab
68. *GitHub - OpenBMB/UltraRAG: A Low-Code MCP Framework for Building Complex and Innovative RAG Pipelines · GitHub*. https://github.com/OpenBMB/UltraRAG
69. *GitHub - amitgambhir/rag-auditor: Open source RAG evaluation platform — automatically score faithfulness, relevancy, and hallucination risk · GitHub*. https://github.com/amitgambhir/rag-auditor
70. *GitHub - argilla-io/distilabel: Distilabel is a framework for synthetic data and AI feedback for engineers who need fast, reliable and scalable pipelines based on verified research papers. · GitHub*. https://github.com/argilla-io/distilabel
71. *GitHub - zetaalphavector/RAGElo: RAGElo is a set of tools that helps you selecting the best RAG-based LLM agents by using an Elo ranker · GitHub*. https://github.com/zetaalphavector/RAGElo
72. *GitHub - yuh-zha/AlignScore: ACL2023 - AlignScore, a metric for factual consistency evaluation. · GitHub*. https://github.com/yuh-zha/AlignScore
73. *GitHub - wandb/weave: Weave is a toolkit for developing AI-powered applications, built by Weights & Biases. · GitHub*. https://github.com/wandb/weave
74. *GitHub - RUC-NLPIR/FlashRAG: ⚡FlashRAG: A Python Toolkit for Efficient RAG Research (WWW2025 Resource) · GitHub*. https://github.com/RUC-NLPIR/FlashRAG
75. *GitHub - OpenBMB/RAGEval · GitHub*. https://github.com/OpenBMB/RAGEval
76. *Langchain Ai*. https://api.github.com/repos/langchain-ai/openevals
77. *api.github.com*. https://api.github.com/repos/wandb/weave
78. *Ruc Nlpir*. https://api.github.com/repos/RUC-NLPIR/FlashRAG
79. *api.github.com*. https://api.github.com/repos/OpenBMB/UltraRAG
80. *api.github.com*. https://api.github.com/repos/OpenBMB/RAGEval
81. *api.github.com*. https://api.github.com/repos/ParticleMedia/RAGTruth
82. *Yuh Zha*. https://api.github.com/repos/yuh-zha/AlignScore
83. *api.github.com*. https://api.github.com/repos/potsawee/selfcheckgpt
84. *Argilla Io*. https://api.github.com/repos/argilla-io/distilabel
85. *api.github.com*. https://api.github.com/repos/zetaalphavector/RAGElo
86. *api.github.com*. https://api.github.com/repos/rungalileo/ragbench
87. *Rag Auditor*. https://api.github.com/repos/amitgambhir/rag-auditor
88. *Adversarial Rag Evaluation Harness*. https://api.github.com/repos/ShivanshSharma007s/Adversarial-RAG-evaluation-harness
89. *Rag Eval Lab*. https://api.github.com/repos/JellyZhang0101/Rag-Eval-Lab
90. *Rag Evaluation*. https://api.github.com/repos/BAEM1N/RAG-Evaluation
91. *api.github.com*. https://api.github.com/repos/zferic/RAGMark
92. *Uptrain Ai*. https://api.github.com/repos/uptrain-ai/uptrain
93. *api.github.com*. https://api.github.com/repos/evidentlyai/evidently
94. *api.github.com*. https://api.github.com/repos/mlflow/mlflow
95. *api.github.com*. https://api.github.com/repos/Betswish/MIRAGE
96. *api.github.com*. https://api.github.com/repos/langwatch/langwatch
97. *Deloitte refunds over $60K for report with AI errors, Australian government says*. https://finance.yahoo.com/news/deloitte-refunds-over-60k-report-034715979.html
98. *Deloitte Australia to partially refund $290,000 report filled with suspected AI-generated errors | AP News*. https://apnews.com/article/australia-ai-errors-deloitte-ab54858680ffc4ae6555b31c8fb987f3
99. *UNITED STATES DISTRICT COURT SOUTHERN DISTRICT OF NEW YORK -----------------------------------------------------------x ROBERTO MATA, Plaintiff, 22-cv-1461 (PKC) -against- OPINION AND ORDER ON*. https://www.ctd.uscourts.gov/sites/default/files/Mata-v.-Avianca.pdf
