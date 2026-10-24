# Hypnexis: problem statements (new round)

Extracted from `Problem_Statements_hypn.pptx` (22 slides, all read). Text is verbatim from the slides except that em dashes were replaced with colons. Raw extract: `source/PS-raw-extract.txt`.


Problem Statements
6 tracks  ·  15 problem statements


## Track 01: AI & Machine Learning

- AI-01 Voice-Clone Detection for Phone Scams
- AI-02 Data-Analyst Agent on Messy Databases
- AI-03 Interactive Knowledge Base: Topic-Augmented Knowledge Graph Builder
- AI-04 RAG Evaluation Pipeline: Retriever and Generator Tested Apart

### AI-01  Voice-Clone Detection for Phone Scams
_Track 01 · AI & Machine Learning_


**Problem Statement**

Scammers can clone the voice of a relative or bank officer from just a few seconds of audio. Build a detector that decides whether a 2–10 second speech clip is genuine or synthetic, and keeps working on voice-cloning tools never seen during training.


**Explanation**

A detector trained on known generators may learn their specific traits and fail on new ones, so generalisation is the central challenge.

The ASVspoof 2019 evaluation set (mostly unseen attack systems) and the In-the-Wild dataset (real deepfakes of public figures) can both test generalisation. Pretrained self-supervised speech models are allowed.


**Key Challenges**

- Generalising to previously unseen voice generators
- Detecting synthetic speech from short clips with limited evidence
- Handling variations across languages and speakers
- Avoiding misleading shortcuts such as silence duration or loudness

### AI-02  Data-Analyst Agent on Messy Databases
_Track 01 · AI & Machine Learning_


**Problem Statement**

Business users ask plain-English questions such as “Which schools had falling enrolment last year?” Build an agent that explores a database, writes and executes SQL, checks its results, and returns the correct answer or acknowledges that it cannot answer.


**Explanation**

Real databases have cryptic column names, dirty values (“N/A”, mixed date formats), duplicated information and unstated business rules. A plausible but wrong answer is worse than none, so the agent must validate queries with row counts, value checks and similar methods.

The BIRD benchmark scores answers on execution results. Restriction: only open-weight models with 8 billion parameters or fewer.


**Key Challenges**

- Identifying the correct tables and columns
- Handling dirty values and external knowledge
- Checking results before answering
- Recognising questions the data cannot answer

### AI-03  Interactive Knowledge Base: Topic-Augmented Knowledge Graph Builder
_Track 01 · AI & Machine Learning_


**Problem Statement**

Vector search struggles with broad questions (“What are the main themes across these documents?”) and with chains of related facts. Build a system that ingests unstructured documents (PDFs, text), extracts entities, groups them into themes, maps their connections in a knowledge graph, and uses a query router to answer both thematic and specific factual questions.


**Explanation**

Deliverables: (1) ingestion pipeline extracting topics and triples; (2) embedded graph database (e.g. Neo4j) alongside a vector database (e.g. ChromaDB); (3) hybrid retrieval routing between topic communities and local graph relationships; (4) grounded answer generator; (5) split-screen Streamlit or React app.

Left: document uploader and chat box. Right: interactive, clickable node-link graph (pyvis, react-force-graph) that zooms to and highlights the topic cluster, documents and relationship paths behind each answer.


**Key Challenges**

- Accurately extracting entities and relationships from text
- Grouping entities into meaningful themes and communities
- Routing questions to thematic or local factual retrieval
- Showing the exact graph path supporting every answer

### AI-04  RAG Evaluation Pipeline: Retriever and Generator Tested Apart
_Track 01 · AI & Machine Learning_


**Problem Statement**

Build an automated pipeline that evaluates a Retrieval-Augmented Generation system by separating retrieval from answer generation. It must show whether a wrong response came from retrieving the wrong chunks or from the model hallucinating despite relevant context.


**Explanation**

Retriever and generator are evaluated independently, and the full system end to end. Deliverables: (1) scoring backend for context relevance, faithfulness and answer accuracy; (2) synthetic test-question generator from uploaded documents; (3) automated root-cause report for each failure; (4) clean single-screen dashboard.

Users upload documents or enter a query, inspect retrieved text beside the final answer, and view colour-coded scorecards: green for accurate, red for hallucinated or missing information.


**Key Challenges**

- Evaluating retriever and generator independently and end to end
- Generating realistic synthetic questions with known answers
- Distinguishing retrieval failures from hallucinations
- Presenting the diagnosis clearly on a single screen


## Track 02: Web3 & Blockchain

- W3-01 Zero-Knowledge Eligibility Credentials
- W3-02 Agent Wallet: Letting AI Agents Pay Safely

### W3-01  Zero-Knowledge Eligibility Credentials
_Track 02 · Web3 & Blockchain_


**Problem Statement**

Services often demand a full identity document to prove one fact, such as being over 18, living in a particular state, or having family income below a scholarship limit. Build a system where an issuer signs a credential and the holder proves a specific fact about it to a smart contract using zero-knowledge proofs, revealing nothing else.


**Explanation**

The circuit, built with Circom, Noir or a similar framework, must verify the issuer's signature and the eligibility condition inside the proof. ZK-friendly signatures and hash functions can speed up proof generation.

An under-constrained signal is a common vulnerability: it can let someone forge a proof that still passes verification. Open-source circuit libraries may be used.


**Key Challenges**

- Ensuring every signal is fully constrained
- Verifying a signature inside the circuit
- Making proof generation fast enough for a browser

### W3-02  Agent Wallet: Letting AI Agents Pay Safely
_Track 02 · Web3 & Blockchain_


**Problem Statement**

AI agents increasingly buy things for users: API credits, tickets, groceries. Build an ERC-4337 account-abstraction smart-contract wallet that gives an AI agent a key able to spend only within an owner-defined policy.


**Explanation**

The agent's key might leak, or a malicious webpage might manipulate the agent. The wallet's policies must hold even if the agent misbehaves.

Policies must cover: allowed contracts and functions; per-transaction limits; daily limits; allowed recipients; permission expiry; and owner approval for transactions outside the policy. The agent can be any open model or a scripted bot.


**Key Challenges**

- Correctly validating signatures, nonces and chain IDs
- Expressing policies precisely
- Requiring owner approval for out-of-policy requests


## Track 03: Climate Tech

- CL-01 Satellite Forest-Loss Alerts
- CL-02 Scope 3 Emissions from Public Spending Records
- CL-03 Predicting Energy Consumption for a Building
- CL-04 MathWorks Challenge: Predicting Building Energy Consumption with MATLAB

### CL-01  Satellite Forest-Loss Alerts
_Track 03 · Climate Tech_


**Problem Statement**

Forest clearing for mining, roads and agriculture often goes unnoticed until it is too late. Using Sentinel-2 imagery, build a system that identifies where forest loss occurred in India between two dates, despite clouds and seasonal changes.


**Explanation**

Sentinel-2 offers 10 m imagery every few days, but monsoon clouds hide large areas, and leaf fall, harvesting and river changes can look like forest loss.

Public forest-loss maps are coarser (30 m) and may lag by a year, so they can serve only as imperfect training labels. Teams choose their own training regions and must test on a state not included in training.


**Key Challenges**

- Masking clouds and shadows
- Separating seasonal changes from actual forest loss
- Learning from coarse and noisy labels

### CL-02  Scope 3 Emissions from Public Spending Records
_Track 03 · Climate Tech_


**Problem Statement**

Organisations increasingly must report the emissions embedded in their purchases, often the largest part of their footprint. Using real, published spending records, map each line to an emission factor and estimate a department's purchasing carbon footprint while honestly representing uncertainty.


**Explanation**

Records contain short, inconsistent descriptions (“IT hardware”, “prof svcs”, “Facilities mgmt”) with supplier names and amounts. Each must be classified into a product or industry category, converted to the factor's currency and base year, and matched to an appropriate factor.

Teams must hand-label at least 2,000 spending lines, with two people agreeing on every label, to measure classification accuracy.


**Key Challenges**

- Classifying short, noisy descriptions into hundreds of categories
- Adjusting for currency differences and inflation
- Propagating uncertainty to the total emissions estimate

### CL-03  Predicting Energy Consumption for a Building
_Track 03 · Climate Tech_


**Problem Statement**

Build an AI model that predicts a building's energy consumption from its characteristics, local weather and other information. Use the predictions to identify buildings that consume or may be wasting the most energy and are strong candidates for retrofitting.


**Explanation**

Consumption depends on size, age, purpose, occupancy and weather. A model that memorises training buildings is not useful, so it must be tested on buildings it has never seen.

Start from the MathWorks challenge repository (MATLAB code, sample data, rubric) or public datasets such as Building Data Genome Project 2 and ASHRAE Great Energy Predictor III, plus public weather archives. Predictions should indicate reliability and explain the drivers.


**Key Challenges**

- Generalising to buildings not seen during training
- Combining building traits with weather and time-of-day effects
- Handling missing and noisy meter readings
- Explaining drivers of consumption and identifying likely waste

### CL-04  MathWorks Challenge: Predicting Building Energy Consumption with MATLAB
_Track 03 · Climate Tech_


**Problem Statement**

Buildings are major contributors to global energy use and carbon emissions. Develop a machine learning algorithm in MATLAB that predicts how much energy a building will consume from its characteristics, local weather data and other information, so that buildings using or wasting the most energy can be identified as retrofit candidates.


**Explanation**

Teams work with the MathWorks challenge repository: a sample training dataset and a starter MATLAB Live Script (Building Regression Models). Teams decide how to process the data, how to split it for training, test and validation, and which model types to train.

Submission: a 5-minute presentation (video, slides or write-up) and a link to code in a public repository. Judged on the MathWorks rubric: Solution Quality 70 (data mastery 20, use of machine learning 20, functionality 10, MATLAB proficiency 10, readability 10) and Presenting Quality 30 (creativity, quality, concept: 10 each).


**Key Challenges**

- Making informed choices to clean, process and split the data
- Justifying algorithm choices and iterating to show useful accuracy
- Delivering error-free, readable and well-organised MATLAB code
- Presenting the results creatively in a 5-minute submission


## Track 04: Health & MedTech

- HM-01 ProvenanceLab: Reproducible Molecule Analysis with Evidence Checks
- HM-02 Prescription Safety Checker for Indian Brand Medicines

### HM-01  ProvenanceLab: Reproducible Molecule Analysis with Evidence Checks
_Track 04 · Health & MedTech_


**Problem Statement**

How might we help biotechnology students analyse and compare molecules reproducibly while clearly identifying invalid inputs and missing evidence? Build a pipeline that validates molecular inputs precisely, computes and compares properties, never silently fills missing values, and can reproduce any previous run exactly.


**Explanation**

SMILES copied from papers may be broken (impossible valence), ambiguous (missing stereochemistry) or different forms of the same molecule (salts, charged forms, tautomers). Toolkit and library versions can give different property values, and spreadsheets may fill gaps silently.

Teams must download frozen PubChem and ChEMBL snapshots so analyses don't depend on live services, and build their own test set of broken and challenging inputs.


**Key Challenges**

- Classifying invalid inputs precisely, not just “invalid”
- Determining when two inputs are the same molecule
- Producing identical results across reruns and machines
- Distinguishing “not computed”, “not available” and “not applicable”

### HM-02  Prescription Safety Checker for Indian Brand Medicines
_Track 04 · Health & MedTech_


**Problem Statement**

Indian prescriptions use brand names, combination products and abbreviations that can hide drug interactions and dosage errors. Build a checker that reads a typed prescription, identifies each brand's active ingredients and strengths, and flags interactions, duplicate ingredients and potentially excessive doses.


**Explanation**

Different brands can share an ingredient, and combinations can hide duplication, such as two brands that both contain paracetamol. Frequencies use abbreviations like OD, BD, TDS and SOS. Safe doses depend on age, weight and kidney function.

Too many minor alerts cause alert fatigue, so users ignore important warnings. Teams must build their test set with help from a pharmacist or pharmacy student.


**Key Challenges**

- Resolving misspelled medicine brand names
- Identifying all ingredients in combination products
- Applying patient-specific dosage limits
- Reducing alert fatigue


## Track 05: Smart Cities

- SC-01 Multi-Camera Vehicle Re-Identification
- SC-02 Accessible Walking Routes from Street Imagery

### SC-01  Multi-Camera Vehicle Re-Identification
_Track 05 · Smart Cities_


**Problem Statement**

Cities plan roads and public transport using outdated surveys of where journeys begin and end. Using footage from multiple non-overlapping cameras, detect, track and re-identify vehicles across cameras to estimate traffic flows between them, without reading number plates.


**Explanation**

Number-plate recognition is prohibited, so vehicles must be matched by visual appearance. Indian traffic is dense and mixed (two-wheelers, autorickshaws, buses, cars), with heavy occlusion and many near-identical vehicles.

Cameras differ in viewing angle and lighting. Travel time between cameras helps decide which matches are plausible.


**Key Challenges**

- Tracking vehicles in dense, mixed traffic
- Handling appearance changes between cameras
- Distinguishing nearly identical vehicles

### SC-02  Accessible Walking Routes from Street Imagery
_Track 05 · Smart Cities_


**Problem Statement**

Navigation apps sometimes send wheelchair users onto footpaths with steps, broken surfaces and missing ramps. Build a system that detects accessibility barriers in street-level images, maps them to the correct footpath segments, and plans routes that avoid them.


**Explanation**

Barriers include missing kerb ramps, steps and stairs, broken or missing footpaths, poles obstructing movement, and parked vehicles blocking footpaths. Detections must be matched to the correct segment of the footpath network.

Project Sidewalk provides labelled examples from other countries, but Indian streets differ, so teams must label their own local images as well.


**Key Challenges**

- Detecting small barriers in varied street images
- Matching detections to the correct map segments
- Planning routes on footpath networks with barrier-related costs


## Track 06: Hardware

- HW-01 Open Innovation: Hardware

### HW-01  Open Innovation: Hardware
_Track 06 · Hardware_


**Problem Statement**

Choose a real problem of your own and solve it with a working hardware prototype. There is no fixed problem statement: teams define the problem, the users and the solution themselves, but the solution must be built around hardware.


**Explanation**

This is an open track for hardware only. Teams select their own sensors, microcontrollers, actuators and communication links, and build a physical prototype that can be demonstrated.

Software-only solutions are not eligible; software should support the hardware, not replace it.


**Key Challenges**

- Defining a real, well-scoped problem worth solving
- Building a working physical prototype
- Justifying hardware choices, including cost and power use
- Testing the prototype under realistic conditions
