# L3, judge lens: the five "what if" questions per P-A statement

Written by hermes 2026-10-24 ~15:00 IST. Purpose: judges for this round are not deep tech experts, they
score innovation, problem understanding, technical feasibility, impact, scalability and presentation
quality (verbatim from the Unstop page, see `unstop/UNSTOP-FACTS.md`). Non-expert judges do not attack
architecture, they ask the questions a normal person asks. Each row names the leads from my L2 files that
answer the question live, so the demo script can be written straight off this.

Rule for using this file: a question with no mapped lead is a gap to either research in wave 2 or design
out of the pitch. Do not answer a what-if with a claim; answer it by showing the lead working.

## AI-01 Voice-Clone Detection for Phone Scams

Leads: `AI-01.md` (22). Main ones: ASVspoof 5, AASIST, AASIST3 (MTUCI), WaveFake, In-the-Wild,
DACON deepvoice contest, Velma (Modulate API), Resemble Detect, DeepFake-o-meter, TrueMedia OSS,
ElevenLabs classifier, OwlGuard.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "Can it catch a clone of MY voice, right now, from my phone?" | Resemble Detect demo, Velma API, ElevenLabs classifier, AASIST3 | record 10 seconds live on stage, run it, show a score |
| 2 | "Scammers change models every month, does yours still work?" | ASVspoof 5, In-the-Wild, WaveFake, DACON (telephone-channel audio) | hold out one generator family, show recall on it |
| 3 | "What happens when it says a real person is fake?" | DeepFake-o-meter (multi-detector), TrueMedia OSS, AASIST confidence intervals | show a second detector disagreeing, then a human-review queue |
| 4 | "Does it work on Hindi, or only English?" | DACON Korean set, In-the-Wild multi-language, ASVspoof5 multilingual tracks | play a Hindi clip, show the score |
| 5 | "Why not just block unknown numbers?" | OwlGuard anti-fraud flow, scam-call datasets in the file | one slide, compares blocking vs detection, uses their own missed-call story |

Weakest link: latency and false positives on compressed phone audio. Answer with a measured number, not
an adjective.

## AI-02 Data-Analyst Agent on Messy Databases

Leads: `AI-02.md` (25). Main ones: BIRD and mini-dev, XiYan-SQL (3B model plus MCP server), OmniSQL 7B,
Arctic-Text2SQL-R1 7B, CHESS, MAC-SQL, DIN-SQL, BIRD-CRITIC, Beaver benchmark, Spider 2.0, WrenAI,
Dataherald, Vanna, Natural-SQL-7B.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "Can I just ask a question in English and get the right number?" | XiYan-SQL, OmniSQL 7B, Arctic-Text2SQL-R1 7B | live question against a real messy warehouse, show SQL and answer |
| 2 | "My data has terrible column names, will it still work?" | Beaver benchmark (plain LLM 0 percent, RAG about 10, hints about 30), CHESS | show the before and after with column hints |
| 3 | "How do I know the answer is not made up?" | BIRD-CRITIC, CHESS execution checks, Beaver evaluation | run the SQL live and show the rows, not a sentence |
| 4 | "Does my data leave my laptop?" | XiYan 3B local, 8B cap in the statement, WrenAI self-host | point at the local endpoint, kill the network, ask again |
| 5 | "What if the question is ambiguous?" | BIRD-Interact, Dataherald clarify flow | ask a follow-up question instead of guessing |

Weakest link: the 8B cap. This is where the statement is scored (BIRD), so the leaderboard number must be
shown with the model name and the split, or the judges will assume it was cherry-picked.

## AI-03 Interactive Knowledge Base: Topic-Augmented Knowledge Graph Builder

Leads: `AI-03.md` (23). Main ones: Microsoft GraphRAG, LightRAG, KAG (Ant Group), Youtu-GraphRAG,
Neo4j LLM Graph Builder, Graphiti, cognee, DeepKE, AutoSchemaKG, iText2KG, GraphRAG Visualizer,
graphify, Kuzu.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "I drop 200 PDFs in, what do I see?" | GraphRAG Visualizer, graphify (folder to clickable graph.html), Neo4j LLM Graph Builder | drag a folder, graph appears, click a node |
| 2 | "Why is this edge here, who said that?" | iText2KG, Graphiti (temporal edges), KAG provenance | click edge, show the sentence it came from |
| 3 | "Is this just a chatbot with extra steps?" | LightRAG, Youtu-GraphRAG (lower token cost, higher accuracy claims) | same question to plain RAG and to the graph, side by side |
| 4 | "Does it get stale when documents change?" | Graphiti temporal model, cognee pipelines | update a document live, show the graph change |
| 5 | "Can I use it on my own laptop?" | Kuzu (embedded graph, WASM), graphify static html | open the exported graph with no server |

Weakest link: the word "topic-augmented" is the differentiator in the statement and only one lead
(ReTAG, code at bykimby/retag) matches that phrase. That is the intellectual hook for the pitch.

## AI-04 RAG Evaluation Pipeline: Retriever and Generator Tested Apart

Leads: `AI-04.md` (26). Main ones: RAGAS, DeepEval, TruLens, Arize Phoenix, Opik, Langfuse, promptfoo,
RAGChecker, ARES, MiniCheck, Vectara HHEM, RAGxplorer, AutoRAG (Korea), EvalScope (Alibaba), CRAG.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "My chatbot gives wrong answers. Which part is broken?" | RAGChecker (separate retriever and generator metrics), ARES | show the split diagnosis on a failing example |
| 2 | "How do I know your judge is not also an LLM making things up?" | MiniCheck, Vectara HHEM (120,014 downloads), RAGTruth | two independent judges agreeing, show disagreement rate |
| 3 | "Can I trust a score of 0.82?" | ARES confidence intervals, AutoRAG, CRAG | show variance across runs, not a single number |
| 4 | "Does it work in my language / my domain?" | EvalScope, RGB (Chinese), CRAG-MM | one non-English example |
| 5 | "Will this run without a GPU and without sending data out?" | promptfoo (local), DeepEval, MiniCheck Flan-T5 (small) | run on the laptop live |

Weakest link: this statement is the easiest to build and the hardest to make visually exciting. The wow
has to come from the diagnosis animation, which is the website's job, not the pipeline's.

## HM-01 ProvenanceLab: Reproducible Molecule Analysis

Leads: `HM-01.md` (15). Main ones: RDKit, Chemprop, DeepChem, Chemotion ELN, ChemOS, plus RetroCast and
Procrustes (the blind-metric finding).

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "Two labs got different answers from the same molecule. Who is right?" | RDKit version pinning, Chemprop, DeepChem | run the same input under two environments, show the divergence |
| 2 | "How do I know the result was not edited later?" | Chemotion ELN, hash-chained record proposal | show the audit trail and a tampered record failing |
| 3 | "Is the model itself trustworthy?" | RetroCast and Procrustes (standard retrosynthesis metric proven blind to chemical validity) | one slide: the metric everyone uses can pass an invalid molecule |
| 4 | "Can I redo this on my machine in one command?" | containerised pipeline leads, ChemOS | run the container live |
| 5 | "Does this matter outside a lab?" | Chemprop property prediction use cases | one sentence, concrete: a wrong solubility number costs a batch |

Weakest link: the chemistry audience is small and the judges are not chemists, so the demo must lead with
the audit story (same input, different answer, provable) and not with the chemistry.

## HM-02 Prescription Safety Checker for Indian Brand Medicines

Leads: `HM-02.md` (16). Main ones: Parchi (Devpost, names the exact Indian data sources), DDInter 2.0,
RxNorm style generic mapping, CDSCO, NPPA, Jan Aushadhi MRP list, prescription OCR, Indian Medicine Dataset.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "I have two strips at home. Is it safe to take both?" | DDInter 2.0 interactions, brand to generic mapping | photograph both strips, show the interaction |
| 2 | "My doctor wrote a brand I cannot afford. Is there a cheaper same-salt option?" | Jan Aushadhi MRP list, NPPA, Parchi's income framing | show price in days of household income |
| 3 | "Is this banned in India?" | CDSCO banned FDCs, Parchi | show the ban flag on a real combination |
| 4 | "The handwriting is unreadable, will it still read it?" | prescription OCR leads | test a messy handwritten prescription on stage |
| 5 | "Are you giving medical advice?" | no, it flags risks and sends you to a pharmacist | wording on screen, plus the pharmacist in the loop |

Weakest link: the statement itself says the test set needs a pharmacist or pharmacy student. That is a
person dependency, and the honest demo answer is a small validated set with the validation method shown,
not a claim of clinical accuracy.

## W3-01 Zero-Knowledge Eligibility Credentials

Leads: `W3-01.md` (17). Main ones: Semaphore, anon-aadhaar, zkPassport, OpenPassport, mopro, prove.email,
Mozilla Pact, Brave and EFF critiques.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "Do I have to upload my Aadhaar to prove my age?" | anon-aadhaar, zkPassport, OpenPassport | prove age with the document never leaving the phone |
| 2 | "Can someone reuse my proof?" | Semaphore nullifiers | same proof twice, second one rejected live |
| 3 | "What is actually hidden, and what leaks?" | Brave and EFF posts (both good), Mozilla Pact | one slide with the leak list, not a slogan |
| 4 | "Does it work on a normal phone, or do I need a laptop?" | mopro (mobile proving) | phone demo |
| 5 | "Why is this better than just checking my email?" | prove.email, eligibility framing | side-by-side of what the verifier learns |

Weakest link: a ZK demo is invisible by nature. The wow has to be the "watch what the verifier does NOT
learn" reveal, and the honest critique sources are what make it credible to a non-expert judge.

## W3-02 Agent Wallet: Letting AI Agents Pay Safely

Leads: `W3-02.md` (19). Main ones: Izanagi (ETHGlobal Tokyo, post-payment revoke via x402 escrow),
Proviso, Agent Payguard, Planbound, Safeliza, ERC-7715, Coinbase AgentKit, AP2.

| # | what-if a common person asks | which leads answer it | how the demo answers it |
|---|---|---|---|
| 1 | "What if the agent pays the wrong person?" | Izanagi (revoke after payment, funds claimed back) | show the money coming back on chain |
| 2 | "Can I cap what it can spend?" | ERC-7715 permissions, Planbound, Coinbase AgentKit | set a cap live, agent hits it, payment fails |
| 3 | "Does it need my seed phrase?" | session keys, smart account modules | show the key it uses is not the main key |
| 4 | "Who is allowed to change the rules?" | Planbound approved-plan enforcement | attempt a rule change, show it requires the human |
| 5 | "Is this real money or a toy chain?" | Base mainnet, x402 escrow | show the explorer link |

Weakest link: three of the four Tokyo projects build on the same pre-payment risk API, so "check before
paying" is crowded. The gap, and the pitch, is enforcement after the fact.

## P-B statements (wow scan only, per the brief)

CL-01, CL-02, CL-03, CL-04, SC-01, SC-02 are not in the L2 files. They get a separate scan file with a
verdict of "mind-blowing, here is why" or "ignore, here is why", and nothing else in them is built.
