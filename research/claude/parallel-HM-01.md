<!-- run id: trun_3b693d434bb94e6db9c60a2a1e987fd3 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6db9c60a2a1e987fd3
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:12.524392Z
**Modified:** 2026-10-24T09:03:07.746518Z

## Output

# ProvenanceLab: Build Trustworthy Molecule Analysis From Open Source

## Executive Summary

- **Build The Missing Trust Layer**: RDKit supplies the chemistry engine; ChEMBL supplies distinct Checker, Standardizer and GetParent components. Neither is the complete student-facing HM-01 product. -> Build a thin workbench around these components rather than a new chemistry engine. [4][99]
- **Browser Chemistry Is Real, But Partial**: RDKit.js is the official JavaScript distribution, powered by the MinimalLib WebAssembly subset. -> Use it for responsive client operations; do not promise full Python API parity. [5]
- **Identity Is A Policy, Not One String**: RDKit exposes strict, stereo-insensitive and tautomer-insensitive registration-hash schemes. -> Show several explicit relationship badges instead of one ambiguous "same molecule" verdict. [35]
- **Standardisation Can Discard Information**: RDKit documents tautomer-processing settings that can remove double-bond or tetrahedral stereochemistry. -> Preserve the original structure and show every transformation. [38]
- **Freeze Data, Not Just URLs**: ChEMBL 37 provides downloadable structures, SQLite data and checksums; PubChem provides bulk and incremental downloads. -> Archive exact input files and provenance, with no live lookup during replay. [108][65]
- **A Lockfile Is One Layer**: conda-lock resolves environments separately for requested platforms. -> Add pinned binaries, runtime/platform metadata and replay tests; do not equate dependency pinning with demonstrated bit-for-bit cross-machine recomputation. [68]
- **Recent ML Reinforces The Problem**: The ChemBERTa-3 work reports run-to-run variance and publishes training configurations; its journal article appeared on **19 January 2026**. -> Keep learned predictions separate from calculated descriptors and imported experimental observations. [61][72]
- **The Best Demo Includes A Refusal**: The publisher marks the hexacyclinol synthesis article retracted on **14 November 2012**. -> Show a plausible molecule with a red evidence warning, proving that valid chemistry syntax does not validate a paper. [77]
- **Do Not Turn Hits Into Medicines**: A **2026** hackathon report describes **12** synthesised/tested compounds and **six** classified as binders in a primary assay, while explicitly warning against comparing workflows from those results. -> Present an evidence ladder, not a "we discovered a drug" claim. [74]

**Recommended build:** Ketcher standalone + RDKit.js + a pinned Python RDKit/ChEMBL-pipeline service + 3Dmol.js + immutable local data + a downloadable run manifest/RO-Crate. This is a proposed architecture, not an already-tested integration.

**Scope and metadata:** Research cut: **2026-10-24**. The inventory below is broad and actionable, not a defensible claim to enumerate every repository on the internet. "Last push" is the repository's observed push timestamp, not its latest release or proof of maintenance quality. Stars are the observed GitHub counts, not quality scores. "Yes, server-backed" means the interface is in a browser but computation needs a server. "Not confirmed" is deliberately not permission to redistribute. All "combine with" entries are recommendations, not verified integrations.


## 1. Reuse RDKit And ChEMBL; Make Identity Explicit

| Project | URL | Plain-words purpose | Last push | Licence | Stars | Browser? | Combine with (recommendation) |
|---|---|---|---|---|---:|---|---|
| RDKit [3] | https://github.com/rdkit/rdkit | Core molecule parsing, chemistry operations and descriptors | 2026-10-24 | BSD-3-Clause  | 3635 | No; native Python/C++ | Authoritative analysis service |
| RDKit.js / MinimalLib [6] | https://github.com/rdkit/rdkit-js | RDKit subset compiled to browser WebAssembly | 2026-09-19 | BSD-3-Clause [5] | 253 | Yes; native WASM | Ketcher + pinned RDKit service |
| MolVS [7] | https://github.com/mcs07/MolVS | Modular validation and structure standardisation | 2020-04-16 | MIT  | 189 | No; Python | RDKit; reference policy tests |
| ChEMBL Structure Pipeline [8] | https://github.com/chembl/ChEMBL_Structure_Pipeline | Checker, standardiser and salt/solvent parent extraction | 2025-11-24 | MIT  | 250 | No; Python | RDKit + frozen ChEMBL |
| datamol [9] | https://github.com/datamol-io/datamol | Convenience layer for everyday molecule processing | 2026-09-09 | Apache-2.0  | 556 | No; Python | RDKit service and notebooks |
| Open Babel [10] | https://github.com/openbabel/openbabel | Chemical-format conversion and chemistry toolkit | 2026-09-14 | GPL-2.0  | 1392 | No; native core | Optional import/export boundary |
| Indigo [110] | https://github.com/epam/Indigo | Cheminformatics engine used by Ketcher | 2026-10-23 | Apache-2.0  | 411 | Yes via WASM integration | Ketcher standalone; record engine differences |
| OpenChemLib JS [83] | https://github.com/cheminfo/openchemlib-js | JavaScript chemistry toolkit port | 2026-10-05 | BSD-3-Clause [87] | 93 | Yes; JavaScript | Alternative client engine, not silent fallback |
| Chemistry Development Kit [21] | https://github.com/cdk/cdk | Java chemistry and descriptor toolkit | 2026-10-24 | LGPL-2.1  | 610 | No; Java core | Independent comparison adapter |
| InChI [111] | https://github.com/IUPAC-InChI/InChI | Reference chemical identifier software | 2026-10-23 | MIT  | 118 | No verified browser package | Store as an additional identifier |
| SELFIES [112] | https://github.com/the-matter-lab/selfies | Alternative molecular string representation | 2025-05-17 | Apache-2.0  | 865 | No; Python package | Optional input/generation experiments |
| Mordred [20] | https://github.com/mordred-descriptor/mordred | Molecular descriptor calculator | 2024-02-07 | BSD-3-Clause  | 484 | No; Python | Optional descriptor plugin |
| medchem [19] | https://github.com/datamol-io/medchem | Medicinal-chemistry filters and checks | 2026-10-01 | Apache-2.0  | 79 | No; Python | Explainable, optional rule annotations |
| useful_rdkit_utils [113] | https://github.com/PatWalters/useful_rdkit_utils | Reusable practical RDKit utilities | 2026-10-15 | MIT  | 242 | No; Python | Descriptor and teaching helpers |
| ChEMBL Beaker (archived) [115] | https://github.com/chembl/chembl_beaker | Chemistry web-service implementation | 2024-04-09 | Not confirmed  | 50 | No; server service | Reference API patterns |
| ChEMBL chemistry_service (archived) [26] | https://github.com/chembl/chemistry_service | Older chemistry service code | 2023-03-23 | Not confirmed  | 1 | No; server service | Historical reference, not default base |

**Takeaway:** RDKit plus the ChEMBL pipeline is the most directly matched foundation. Alternative engines are useful adapters or cross-checks, but silently switching between them would weaken provenance.

### ChEMBL's three-stage design is the right case study

The ChEMBL pipeline separates checking, standardisation and parent extraction rather than treating them as one opaque cleanup operation. Its checker returns issue descriptions and a **0-9** severity penalty; that score is a pipeline-specific signal, not a universal probability of correctness. [99][1]

The associated paper reports that applying the pipeline corrected certain standardisation errors in previous ChEMBL releases and exposed other curation priorities. This is a concrete demonstration that a trusted database can improve its representations without the original molecule becoming "a different discovery." [99] For ProvenanceLab, preserve the source record and attach the new representation as a derived object with its own policy/version.

### Proposed validation contract

| Check | What the interface should say | What it must not do |
|---|---|---|
| Parsing and sanitisation | Invalid syntax or valence, with the failing atom/operation when available | Silently repair the input and report success |
| Potential stereochemistry | "Valid structure; stereochemistry under-specified" | Invent an enantiomer or call every unspecified centre invalid |
| Disconnected components | List fragments, charge and proposed parent relationship | Delete a counterion without recording it |
| Charge/protonation | Preserve original charge; offer a named comparison policy | Equate neutral and charged forms under every comparison |
| Tautomers | Show original, selected canonical form and enumeration/policy limits | Describe the canonical form as the experimentally dominant tautomer |
| Unsupported chemistry | State toolkit limitations and stop or require review | Claim that parser acceptance establishes chemical stability |

RDKit documents strict allowed-valence checking and distinguishes potential stereocentres with unspecified information. [31] More subtly, its documentation says a canonical tautomer is very likely **not** the most stable tautomer under given conditions: canonicalisation primarily serves repeatable representation. [38]

Keep four different questions separate: identical submitted material, same standardised structure, same parent, and equivalent under a declared tautomer/stereo policy. Use RDKit's registration-hash layers where appropriate, but retain a separate file hash for exact bytes. A chemistry-aware identity hash is not a substitute for an artefact checksum. [35]

**Decision:** Treat standardisation as an inspectable transformation graph, never an invisible prerequisite to displaying results.


## 2. Make Browser Chemistry Spectacular Without Faking Capability

| Project | URL | Plain-words purpose | Last push | Licence | Stars | Browser? | Combine with (recommendation) |
|---|---|---|---|---|---:|---|---|
| Ketcher [12] | https://github.com/epam/ketcher | Draw and edit chemical structures | 2026-10-23 | Apache-2.0  | 917 | Yes; standalone WASM or remote service | RDKit.js + explicit engine handoff |
| JSME [13] | https://github.com/jsme-editor/jsme-editor.github.io | Compact JavaScript molecule/reaction editor | 2025-03-09 | BSD-3-Clause [105] | 110 | Yes; JavaScript | RDKit.js validation |
| Kekule.js [11] | https://github.com/partridgejiang/Kekule.js | Edit, display and manipulate chemical objects | 2026-09-21 | MIT  | 280 | Yes; JavaScript | Optional Open Babel bundle |
| 3Dmol.js [14] | https://github.com/3dmol/3Dmol.js | Interactive WebGL molecule rendering | 2026-10-21 | BSD-3-Clause; bundled notices [78] | 1030 | Yes; WebGL | Ketcher + stored conformers |
| NGL [15] | https://github.com/nglviewer/ngl | Interactive molecular structure viewer | 2026-09-03 | MIT  | 734 | Yes; WebGL | Protein/ligand story panel |
| Mol* [16] | https://github.com/molstar/molstar | Rich macromolecular structure visualisation | 2026-10-23 | MIT  | 1035 | Yes; web viewer | Advanced protein context |
| mols2grid [17] | https://github.com/cbouy/mols2grid | Interactive grids for inspecting molecule collections | 2025-12-27 | Apache-2.0  | 259 | Yes; generated/browser UI | RDKit batch comparisons |
| Stmol [28] | https://github.com/napoles-uach/stmol | Molecule visuals inside Streamlit apps | 2026-09-07 | MIT [86] | 214 | Yes; Python server-backed | Fast prototype + analysis service |
| imolecule [56] | https://github.com/patrickfuller/imolecule | Molecular visualisation for notebooks/web pages | 2021-10-22 | MIT  | 85 | Yes; viewer component | Older educational visualisation reference |

**Takeaway:** Pick one editor and one primary viewer. For this problem, Ketcher + 3Dmol.js is a focused pairing; NGL or Mol* becomes more attractive when protein context is central.

### Ketcher demonstrates the offline-versus-service trade-off

Ketcher explicitly supports a remote Indigo REST provider and a standalone provider using Indigo WASM without a server dependency. Its documentation notes the standalone WASM size trade-off and offline capability. [98] That makes the standalone route a strong demo choice: judges can edit a structure while the network is disabled.

However, the editor's chemistry engine and the authoritative RDKit analysis engine are different components. Proposed design: save the editor export, validate it with the pinned analysis engine, and expose disagreements rather than choosing whichever answer looks nicer. The same principle applies to OpenChemLib JS, which is a JavaScript port with its own API, not a promise of RDKit-equivalent behaviour. [87]

### Open Babel JS: a verified bundle, not an invented canonical project

A browser Open Babel bundle is present in Kekule.js's `src/_extras/OpenBabel` directory, including JavaScript and a `.wasm` file. [84] This is a concrete browser integration lead; a separately maintained, canonical standalone repository named "Open Babel JS" was not established here.

| Component | URL | Purpose | Last update | Licence | Stars | Browser? | Combine with |
|---|---|---|---|---|---:|---|---|
| Open Babel JS/WASM bundle in Kekule.js | https://github.com/partridgejiang/Kekule.js/tree/master/src/_extras/OpenBabel | Browser access to bundled Open Babel functionality | Bundle rebuild date not confirmed; host repository last push 2026-09-21 | Host toolkit MIT; Open Babel core GPL-2.0; inspect bundled notices | Host repository 280; no independent count | Yes; bundled WASM | Optional format conversion, isolated from the default RDKit path [84][11][10] |
| RDKit MinimalLib source | https://github.com/rdkit/rdkit/tree/master/Code/MinimalLib | C++ layer underlying the browser build | Module-specific date not confirmed; RDKit last push 2026-10-24 | RDKit BSD-3-Clause | RDKit 3635; no independent count | Yes when compiled to WASM | Official RDKit.js distribution [102][3][4] |

These are modules/bundles inside larger projects, not additional independently maintained repositories. The permissive licence of a wrapper must not be assumed to relicense its dependencies.

For visual impact, 3Dmol.js is a verified WebGL-accelerated browser renderer under a BSD licence. [36] Proposed presentation: synchronised 2D/3D panels, atom-linked warnings, a fragment "explosion" view and a before/after transformation slider. Label generated conformers as generated, not experimentally observed; store their coordinates in the run bundle.

**Decision:** Use visuals to reveal uncertainty and transformation history. A rotating molecule is memorable; a rotating molecule that explains why two results differ is the product.


## 3. Freeze PubChem And ChEMBL Into Replayable Evidence

| Project | URL | Plain-words purpose | Last push | Licence | Stars | Browser? | Combine with (recommendation) |
|---|---|---|---|---|---:|---|---|
| DVC [40] | https://github.com/treeverse/dvc | Version datasets and pipeline artefacts alongside code | 2026-10-19 | Apache-2.0  | 15939 | No; CLI | Snapshot files + Git |
| DataLad [41] | https://github.com/datalad/datalad | Track datasets, files and their history | 2026-10-21 | MIT; third-party notices [79] | 669 | No; CLI | Alternative to DVC for data collections |
| AiiDA [42] | https://github.com/aiidateam/aiida-core | Track computational workflows and provenance | 2026-10-23 | MIT [66] | 601 | No; Python service | Later multi-step compute workflows |
| PROV Python [51] | https://github.com/trungdong/prov | Represent provenance relationships | 2026-09-18 | MIT  | 141 | No; Python | Run manifest to provenance graph |
| ro-crate-py [43] | https://github.com/ResearchObject/ro-crate-py | Package research objects and metadata | 2026-10-14 | Apache-2.0  | 89 | No; Python | Exportable run evidence bundle |
| conda-lock [44] | https://github.com/conda/conda-lock | Pin resolved Conda environments per platform | 2026-10-23 | MIT; bundled notices [80] | 564 | No; CLI | RDKit environment + container |
| uv [48] | https://github.com/astral-sh/uv | Python environment and dependency management | 2026-10-11 | Apache-2.0  | 90601 | No; CLI | Python service dependency lock |
| Nix [47] | https://github.com/NixOS/nix | Declarative software environments/builds | 2026-10-14 | LGPL-2.1  | 17870 | No; native tooling | Alternative environment strategy |
| repo2docker [45] | https://github.com/jupyterhub/repo2docker | Build runnable images from research repositories | 2026-10-05 | BSD-3-Clause  | 1739 | No; image builder | Teaching notebooks + pinned image |
| nbval [46] | https://github.com/computationalmodelling/nbval | Test notebook execution against expected outputs | 2025-09-17 | Not confirmed  | 452 | No; test runner | Golden notebook regression suite |
| JupyterLite [52] | https://github.com/jupyterlite/jupyterlite | Jupyter environment running in a web browser | 2026-10-22 | BSD-3-Clause  | 4912 | Yes; browser runtime | Small compatible teaching exercises |
| PubChemPy [24] | https://github.com/mcs07/PubChemPy | Python access to PubChem services | 2025-09-08 | MIT  | 517 | No; Python client | Snapshot ingestion only |
| ChEMBL webresource client [25] | https://github.com/chembl/chembl_webresource_client | Python access to ChEMBL services | 2026-03-24 | Apache-2.0 [73] | 453 | No; Python client | Snapshot ingestion only |

**Takeaway:** Use one data-versioning tool, one dependency-lock strategy and one portable provenance export. DVC, DataLad, AiiDA, Nix and RO-Crate solve overlapping but different problems; adopting all of them is not an MVP requirement.

### Frozen database access must replace live replay queries

| Source | Verified access | Update/release evidence | Licence and stars | Browser role | Proposed combination |
|---|---|---|---|---|---|
| ChEMBL release archive | https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/ ; `chembl_37_sqlite.tar.gz`, SDF and checksums | ChEMBL 37 directory exists; directory modification timestamps are not treated as release dates | Data CC BY-SA 3.0; GitHub stars not applicable | Downloads usable through browser; analysis needs a local engine | Frozen SQLite/SDF + file hashes + release notes [64][108][63] |
| PubChem bulk/monthly data | https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/ ; https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Monthly/ | Monthly index includes dated 2026 directories; `CURRENT-Full` is a moving location, not an immutable snapshot identifier | Check source-specific terms; stars not applicable | Browser download possible; ingestion/replay are local | Archive selected files and necessary annotations under a content-addressed manifest [109][62][65] |

For a hackathon, a documented, frozen teaching subset is preferable to pretending the entire databases were mirrored. Give the subset its actual acquisition date, source release/path, selection query, original records, checksums and exclusions; the research cut date does not prove a dataset was downloaded on that date.

PubChem distinguishes depositor-supplied Substance descriptions from the unique structures in Compound. Preserve that distinction when tracing a value back to its origin. [107] Also note that the standard Compound dump excludes annotations and 3D conformer models, so those need separate capture if the demo uses them. [65] ChEMBL's attribution guidance asks for both the resource URL and release version. [63]

### RO-Crate provides a better deliverable than a screenshot

The **2024** Workflow Run RO-Crate paper presents a model for recording execution provenance, including the workflow's inputs, outputs and execution context. [106] AiiDA similarly foregrounds computational workflows and provenance, while conda-lock resolves platform-specific environments. [66][68] These are useful building blocks, not evidence that ProvenanceLab already reproduces a computation across all machines.

Proposed run bundle: original input bytes; parsed structure; all derived structures and transformation parameters; snapshot identifiers and hashes; exact RDKit/WASM versions and binary hashes; code revision; platform lock and image digest; descriptor names, algorithms and units; conformer method/seed/thread settings; model/tokenizer revisions if used; warnings, exceptions, results and an HTML report. Export it as a RO-Crate and keep raw file checksums separate from chemistry-aware identity hashes.

### Missingness is part of the result schema

| Status | Example | Required behaviour |
|---|---|---|
| `not_computed` | A 3D descriptor was never requested or no conformer-generation step ran | Show the unperformed prerequisite; do not use zero |
| `not_available` | No matching experimental observation exists in the frozen subset | Name the snapshot and lookup; absence is not proof no measurement exists anywhere |
| `not_applicable` | A centre-specific stereochemical label is requested for a structure with no applicable centre | State the applicability rule |
| `error` | A requested calculation failed | Preserve the exception separately from all three absence states |
| `computed` / `observed` / `predicted` | A value exists | Store value, method/source, unit and provenance; distinguish the evidence class |

This is a proposed contract. A legitimate numerical zero remains zero; `null` requires a reason, and a prediction must never silently fill an unavailable experimental field.

For "exactly across machines," distinguish **archived replay** from **recomputation**. Archived replay returns stored artefact bytes; certified recomputation must pass golden tests in an explicitly supported reference runtime. Outside that envelope, report numerical tolerance comparisons or a reproducibility failure rather than promising universal bit identity.

**Decision:** Make "Download run" and "Replay offline" first-class product features, with a visible pass/fail result and a precise compatibility envelope.


## 4. Borrow Regional And Hugging Face Tools Selectively

| Project | URL | Plain-words purpose | Last push | Licence | Stars | Browser? | Combine with (recommendation) |
|---|---|---|---|---|---:|---|---|
| DeepChem [22] | https://github.com/deepchem/deepchem | Molecular ML datasets, models and examples | 2026-08-20 | MIT  | 7081 | No; Python core | Optional prediction adapter |
| Chemprop [23] | https://github.com/chemprop/chemprop | Graph neural networks for property prediction | 2026-10-21 | MIT [32] | 2511 | No; Python core | Separate predicted-property tier |
| molfeat [18] | https://github.com/datamol-io/molfeat | Common interface for molecular features | 2026-10-01 | Apache-2.0  | 235 | No; Python | Pinned feature/model plugins |
| Uni-Mol [53] | https://github.com/deepmodeling/Uni-Mol | 3D molecular representation-learning framework | 2025-05-29 | MIT  | 1167 | No verified browser runtime | Optional 3D ML experiment |
| TorchDrug [49] | https://github.com/DeepGraphLearning/torchdrug | Graph-based drug-discovery ML toolkit | 2024-08-12 | Apache-2.0  | 1588 | No; Python | Research extension, not MVP dependency |
| XenonPy [50] | https://github.com/yoshida-lab/XenonPy | Materials/chemical informatics ML utilities | 2024-07-15 | BSD-3-Clause  | 159 | No; Python | Materials-property extension |
| MoLFormer code [82] | https://github.com/IBM/molformer | SMILES language-model training and evaluation code | 2025-09-17 | Apache-2.0 [67] | 419 | No; PyTorch | Frozen embeddings + model manifest |
| ChemBERTa-3 [81] | https://github.com/deepforestsci/chemberta3 | Chemical foundation-model training/benchmark framework | 2026-07-23 | MIT [70] | 81 | No; Python | Reproducible ML benchmark template |
| MolPLA [91] | https://github.com/dmis-lab/MolPLA | Core/R-group molecular representation learning | 2024-03-13 | Not confirmed  | 6 | No; research code | Optional lead-optimisation lesson; licence unresolved |

**Takeaway:** These projects expand research and prediction capability, but none should replace deterministic validation. Keep the default HM-01 path usable without downloading model weights or requiring a GPU.

### Regional coverage: useful leads, with attribution limits

For Chinese-language/China-facing ecosystem discovery, **Uni-Mol, TorchDrug and Kekule.js** are useful leads; for Japan-facing discovery, **XenonPy, Mordred and iwatobipen's examples** are useful leads. These labels are discovery directions, not independently established nationality, localisation or institutional-origin claims from the repository metadata above. The concrete Japanese-language competition implementation appears in Section 5. [53][49][11][50][20][30][95]

The Korean affiliation is directly documented: MolPLA's repository identifies the Data Mining and Information Systems Lab at **Korea University, Seoul, South Korea**. Its method learns relationships between molecular cores and R-groups through masked graph contrastive learning and R-group retrieval. [85][69] It is a relevant lead-optimisation case study, but the code licence was not confirmed. The paper's CC BY licence does not resolve that code-licensing gap. [69]

### Model cards are evidence documents, not app specifications

| Model | URL | Plain-words purpose | Last update | Licence | Stars | Browser? | Combine with |
|---|---|---|---|---|---|---|---|
| MoLFormer-XL-both-10pct | https://huggingface.co/ibm-research/MoLFormer-XL-both-10pct | Turn SMILES into learned features; fine-tune a property model | Exact model revision date not confirmed | Apache-2.0 | Not applicable; HF likes are not GitHub stars | No packaged browser runtime verified | MoLFormer code + frozen weights/tokenizer + explicit prediction panel [60] |
| DeepChem ChemBERTa-77M-MLM | https://huggingface.co/DeepChem/ChemBERTa-77M-MLM | Masked-token molecular language model | Not confirmed | Not confirmed from reviewed page; no model card | Not applicable | No packaged browser runtime verified | Optional embedding experiment after licence/model documentation review [58] |
| ChemBERTa-zinc-base-v1 | https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1 | BERT-like masked modelling of SMILES strings | Not confirmed | Not confirmed from reviewed material | Not applicable | No packaged browser runtime verified | Educational language-model comparison; not an experimental-property source [59] |

The strongest documented initial choice here is MoLFormer for an optional embedding visualisation. Its card explicitly says it is **not intended for molecule generation**, has not been tested for molecules larger than approximately **200 atoms**, and may perform worse on invalid or noncanonical SMILES. [60] Its example uses `trust_remote_code=True`; pin and inspect that code rather than executing a moving revision. [60]

### ChemBERTa-3 is a reproducibility case study, not a magic predictor

ChemBERTa-3 publishes training code/configurations and tests infrastructure on cloud and on-premise systems. [61][72] Yet its authors also report notable variance under identical hyperparameters and warn that a better score under an easier split need not imply better generalisation to unseen chemical space. [61]

That tension is directly useful for the demo: the same molecule can have a deterministic descriptor, an imported observation under specified conditions and a learned prediction with model uncertainty. Proposed interface: three separate cards, each with its own provenance, rather than a single authoritative-looking "property" number.

**Decision:** Add one optional, pinned ML visualisation only after validation, missingness and replay work. Prediction scope, training overlap and applicability warnings belong beside the prediction.


## 5. Reuse Student Notebooks And Competition Workflows Carefully

| Project | URL | Plain-words purpose | Last push | Licence | Stars | Browser? | Combine with (recommendation) |
|---|---|---|---|---|---:|---|---|
| TeachOpenCADD [27] | https://github.com/volkamerlab/teachopencadd | Student-oriented drug-design notebooks | 2026-09-01 | CC-BY-4.0 [101] | 1085 | Yes; Jupyter server-backed | Teaching narrative + RDKit |
| Practical Cheminformatics Tutorials [29] | https://github.com/PatWalters/practical_cheminformatics_tutorials | Hands-on cheminformatics notebooks | 2026-08-22 | MIT  | 1335 | Yes; notebook frontend; backend needed | Import examples selectively |
| iwatobipen chemo_info [30] | https://github.com/iwatobipen/chemo_info | Cheminformatics scripts and experiments | 2025-04-18 | Not confirmed  | 32 | No native browser app; notebook use possible | Small examples; inspect each dependency |
| RDKit blog notebooks [114] | https://github.com/greglandrum/rdkit_blog | Worked RDKit examples and explanations | 2026-08-25 | Not confirmed  | 159 | Yes via notebook frontend; backend needed | Edge-case lessons and regression fixtures |
| Bioinformatics freeCodeCamp course [55] | https://github.com/dataprofessor/bioinformatics_freecodecamp | Educational bioinformatics/drug-discovery code | 2021-05-22 | Not confirmed  | 164 | Yes via notebooks; backend needed | Teaching inspiration; licence unresolved |
| DrugDisco [54] | https://github.com/NCBI-Hackathons/drugdisco | Hackathon-era automated drug-discovery pipeline | 2018-03-16 | MIT  | 30 | Yes; UI with backend | Historical workflow inspiration |
| Open Polymer Prediction solution [92] | https://github.com/chinchillaa/neurips-open-polymer-prediction-2025 | Japanese-language Kaggle polymer-property pipeline | 2025-07-18 | MIT stated in README [95] | 2 | No; Python pipeline | Offline evaluation and feature examples |
| YutaYokkaichi polymer solution [93] | https://github.com/YutaYokkaichi/NeurIPS---Open-Polymer-Prediction-2025 | Additional public competition solution repository | 2025-06-17 | Not confirmed  | 0 | No verified browser build | Comparison lead; licence unresolved |
| Open Babel documentation [116] | https://github.com/openbabel/documentation | Toolkit documentation sources | 2026-05-26 | Not confirmed  | 10 | Yes; rendered documentation, not chemistry runtime | Conversion-format help and attribution |

**Takeaway:** TeachOpenCADD offers the strongest student-oriented narrative base. Public competition code offers useful offline evaluation patterns, but public visibility and prize-winning status are separate questions.

### TeachOpenCADD is a better teaching base than a blank dashboard

TeachOpenCADD explicitly describes itself as a platform developed by students for students, with interactive notebooks using open-source packages including RDKit and molecular-visualisation tools. [101] That fits HM-01's audience better than making users learn a professional cheminformatics console before they understand salts, stereochemistry or missing data.

Proposed reuse: adapt one short lesson into a guided "Why do these two molecules disagree?" exercise, then make its input files and expected outputs part of the regression suite. Keep attribution and licence treatment distinct: the teaching repository is CC BY 4.0, while many underlying software dependencies use different licences. [101]

### Kaggle: verified competition, not verified winning code

The official **2025** Open Polymer Prediction competition concerns multi-task polymer-property prediction and provides data, baselines and evaluation pipelines. [94] The Japanese-language `chinchillaa` repository describes RDKit-descriptor ensembles and a string-feature/XGBoost baseline, with MIT terms stated in its README. [95]

Use it as a concrete example of offline data preparation and model comparison, not as a certified winner: its final ranking/prize status was not confirmed. The same caution applies to the second public solution repository. DrugDisco is a genuine NCBI-Hackathons repository with a drug-discovery workflow, but neither current production suitability nor a prize-winning claim is established by that provenance alone. [57]

### Hackathon outcomes and property-app inspiration

| Candidate | URL | What is actually established | Last update | Licence | Stars | Browser? | Combine with |
|---|---|---|---|---|---|---|---|
| Mol-Hunter | https://chemistry.illinois.edu/news/2024-05-23/illinois-chemistry-team-wins-computational-science-hackathon | University report identifies the molecular-discovery/synthesis agent and first place among 12 teams | Report 2024-05-23; code update not confirmed | Code licence not confirmed | Not confirmed | Not confirmed | Story/workflow inspiration; a forkable codebase was not established [96] |
| Tokyo-1 Drug Discovery Hackathon | Direct event-report URL not confirmed in the retained citation | Event report describes a 2025 drug-discovery hackathon and selection of awards/MVPs; specific reusable winning code not confirmed | Report 2025-10-03; code update not confirmed | Not confirmed | Not applicable | Not confirmed | Japan-focused discovery lead, not a verified software dependency [88] |
| TBXT hackathon data | https://github.com/bioArena/tbxt-hackathon-data | Public experimental-data link in a 2026 hackathon report | Report 2026-08-07; repository update not confirmed | Not confirmed | Not confirmed | Browser-readable repository; no app established | Evidence-ladder teaching case, after data-licence review [74] |
| ADMETlab 3.0 | https://admetlab3.scbdd.com/ | Public property-prediction web app, accessible without registration | Associated paper 2024; service update not confirmed | Software licence not confirmed; article CC BY-NC is not a software licence | Not confirmed | Yes; web service, not verified local/offline code | UI inspiration only unless source/licence and model provenance are established [90] |

A verified winner with unconfirmed source availability is a story lead, not a merge candidate. Conversely, a well-licensed non-winning repository can be the more practical hackathon dependency.

**Decision:** Reuse educational examples and evaluation mechanics; avoid importing an entire historical discovery pipeline or claiming a leaderboard result that the sources do not establish.


## 6. Turn Recent Papers And Real Failures Into Checks

| Source | Year/status | Concrete finding relevant to HM-01 | Product consequence |
|---|---|---|---|
| ChemBERTa-3 | 2025 preprint; journal article first published 2026-01-19 | Open training/configuration work, cross-environment tests and run variance | Pin splits, seeds, model revisions and configuration; do not promise identical stochastic training outcomes [61][72] |
| Recording provenance of workflow runs with RO-Crate | Published 2024-09-10 | Workflow Run RO-Crate records execution provenance using a portable research-object model | Export the actual run and artefacts, not just prose about reproducibility [106] |
| PubChem 2025 update | 2025 article | Distinguishes depositor Substance records and unique Compound structures; documents source-contributed article associations | Preserve source-level lineage; database presence is not an endorsement of a paper [107] |
| MolPLA | 2024 article | Core/R-group representation learning and retrieval | Useful advanced lesson; article openness does not establish code permissions [69] |
| ADMETlab 3.0 | 2024 article | Accessible molecular-property prediction service | Keep predictions visibly distinct from measurements and deterministic calculations [90] |
| Chemprop v2 paper | Version-specific paper; publication date not established in the excerpts used here | Describes reproducible study scripts/data splits and explicit split-file support | Save the split artefact and model version rather than only reporting a score [103] |
| ChEMBL structure-curation pipeline | 2020 foundational paper, retained despite preference for newer sources | Corrected prior standardisation errors | Dataset and standardisation versions both belong in provenance [99] |

The common thread is that reproducibility lives in versioned representations, execution artefacts and evaluation design. A recent publication date alone does not make a model, database record or web app suitable for an exact-replay workflow.

### Retraction case: hexacyclinol separates chemistry checks from evidence checks

Wiley's original hexacyclinol synthesis article was first published on **11 April 2006** and is marked retracted on **14 November 2012**. [77] The source establishes the retraction; the report does not infer a detailed cause or treat statements inside the retracted article as validated chemical evidence.

Proposed demo: let the structure render successfully, then display the paper's retraction status beside the associated claim. The lesson is precise: a valence checker can evaluate a molecular representation but cannot establish whether a synthesis occurred or a paper's claim is reliable. Preserve the bibliographic record and warning rather than silently erasing the evidence trail.

### Repair case: ChEMBL shows why yesterday's answer can change

The ChEMBL pipeline paper reports corrections to errors in previous releases and identifies further curation priorities. [99] This is not a retraction or a claim of fraud; it is a documented data-curation improvement.

Proposed demo: compare two deliberately frozen source/policy configurations and show a structured difference: changed source record, changed parent selection or changed standardiser. The outcome should be "explained difference," not "the old researcher was wrong." This makes provenance useful even when everyone acted in good faith.

### Stereochemistry case: thalidomide resists the simplistic story

The reviewed thalidomide source states that the R and S enantiomers rapidly interconvert in body fluids and tissues, and explains why that complicates producing a stable nonteratogenic form. [75] Do not present the familiar but misleading demo slogan "one mirror image is safe, the other is dangerous" as the whole explanation.

Instead, show mirror-image structures, an unspecified-stereo warning and a note that biological interpretation needs evidence about interconversion and context. The visual is compelling precisely because the application refuses to infer clinical safety from a drawing.

### Discovery case: six binding signals are not six medicines

The **7 August 2026** TBXT hackathon report describes **12** compounds synthesised and tested, of which **six** were classified as binders to full-length TBXT in a primary surface-plasmon-resonance assay. [74] The same report explicitly cautions against interpreting its small, uneven set of results as a comparison of team workflows. [74]

Use this as an evidence ladder: generated idea -> valid structure -> computational score -> compound made -> primary binding result -> follow-up evidence. The later stages are not supplied merely by moving a molecule upward in a 3D animation. Label the hackathon report as reported evidence, not independent confirmation of therapeutic efficacy.

**Decision:** Ship an "evidence health" panel alongside the chemical-validity panel. One verified retraction case and several documented uncertainty/repair cases are stronger than a longer list of unsourced scandals.


## 7. Win Judges With An Explainable Offline Replay

The following is a **proposed demo**, not a report of executed tests or measured performance. 3Dmol.js supplies the verified browser-rendering foundation; ProvenanceLab must supply the interpretation, provenance and safeguards. [36]

### The central story: "same molecule" has several meanings

Start with two different SMILES spellings of ethanol, `CCO` and `OCC`. Proposed output: different input-byte hashes but a matching chemistry identity under the chosen policy. Then replace one entry with an acid/sodium-salt pair and reveal why a parent relationship is not the same thing as identical submitted material.

Next, show a structure with unspecified stereochemistry, followed by a fully specified variant. Rather than silently choosing a configuration, the application highlights the unresolved centre and lets the judge inspect the original and derived representations. RDKit's separate strict, stereo-insensitive and tautomer-insensitive hash layers make a good conceptual basis for these distinct badges. [35]

### Ten "what if" questions with proposed demo answers

| # | Non-expert judge question | Demo answer and visible behaviour |
|---:|---|---|
| 1 | "What if I type a molecule that cannot exist as drawn?" | Submit `C(C)(C)(C)(C)C` as a proposed over-valent-carbon fixture. Show a sanitisation failure, highlight the central atom, preserve the exact input and do not compute normal descriptors from a silently repaired substitute. RDKit documents higher-than-allowed-valence exceptions. [31] |
| 2 | "What if I write the same molecule differently?" | Compare `CCO` and `OCC`. Show original strings and file hashes separately from the expected matching chemical identity. State the toolkit/version and identity policy. This is a proposed regression fixture, not a computation executed in this report. |
| 3 | "What if I forget the left-handed/right-handed version?" | Use `CC(O)C(=O)O` as a proposed unspecified-stereo example. Say "valid but under-specified," highlight the potential centre, and avoid assigning an R/S label. RDKit distinguishes potential unspecified stereocentres. [31] |
| 4 | "What if one entry is a salt or has a different charge?" | Compare `CC(=O)O` with `CC(=O)[O-].[Na+]`. Keep the submitted forms separate; optionally show their relationship under a declared parent/charge policy. Display removed fragments and every transformation, not a single unqualified match badge. |
| 5 | "What if these are tautomers?" | Compare proposed acetone/enol fixtures `CC(=O)C` and `C=C(O)C`. Offer tautomer-policy matching while preserving the originals. Explain that canonicalisation does not identify the most stable form under experimental conditions. [38] |
| 6 | "What if a property is blank?" | Show three different badges: not computed, not available in this snapshot, and not applicable. A fourth error badge preserves a failed calculation. Never replace any of them with zero or an unlabelled model estimate. |
| 7 | "What if PubChem changes tomorrow or the Wi-Fi dies?" | Disable networking and replay from the archived subset. Show the database release/path, captured files and hashes; new live results belong to a new run. PubChem provides bulk download routes, but the application must create its own frozen replay boundary. [65] |
| 8 | "What if I run this on another laptop?" | Import the run bundle, verify hashes and execute the supported reference runtime. Show exact stored-output replay separately from recomputation parity; if parity fails, display the difference and environment instead of a green check. |
| 9 | "What if AI says it is a good drug?" | Display "model prediction, not established drug safety/efficacy." Show model revision, training/applicability limitations and any experimental evidence separately. MoLFormer's card itself limits its intended uses. [60] |
| 10 | "What if the paper is wrong or retracted?" | Keep the structure visible but flag the linked hexacyclinol article as retracted. Explain that chemical-validity and evidence-health checks answer different questions. [77] |

These proposed fixtures need automated tests against the exact pinned implementation before stage use. The strongest reveal is not a number: it is the application explaining why it will not supply one.

### Three visual moments worth implementing

| Moment | Proposed visual | Why it helps without exaggerating |
|---|---|---|
| Identity lens | Toggle strict, parent, stereo and tautomer relationships; animate changed atoms/fragments | Makes a hidden comparison policy visible |
| Evidence lens | Click any property to trace value -> method/source -> snapshot -> original record | Connects an attractive result to its evidence rather than its confidence styling |
| Replay lens | Network-off badge, bundle verification and before/after result diff | Demonstrates a reproducibility contract rather than merely claiming one |

Do not make the visual language stronger than the evidence: generated 3D coordinates are not a crystal structure, a docking pose is not a binding assay, and a checked checksum is not proof that the source claim is true. These are recommended product safeguards, not additional experimental findings.

**Decision:** Build a short, reliable story around one successful comparison, one ambiguity, one failure, one evidence warning and one offline replay. That is more defensible than a large dashboard of unexplained predictions.


## Synthesis

| Strategy | Mechanism | Scope | Main trade-off | Evidence/replay implication |
|---|---|---|---|---|
| RDKit + ChEMBL pipeline | Parse/check, standardise and derive parent structures | Core HM-01 chemistry | Powerful transformations can discard distinctions | Freeze policies and preserve original/derived structures [99][38] |
| RDKit.js + Ketcher standalone | WASM chemistry/editor operations near the user | Responsive/offline browser work | MinimalLib is a subset; editor and analysis engines may differ | Pin both builds and expose handoff/disagreement [104][98] |
| Open Babel / CDK / OpenChemLib / Indigo | Alternative chemistry or format engines | Interoperability and independent comparisons | More dependencies and potentially different semantics | Name the engine for every result; never silently fall back [10][21][87][110] |
| 3Dmol.js / NGL / Mol* | Browser molecular rendering | Communication and structural context | Visual plausibility can exceed evidentiary strength | Store coordinate origin and label generated versus observed structures [36][15][16] |
| DVC / DataLad + locks + RO-Crate | Version artefacts, constrain environments, package provenance | Data and run portability | No individual component establishes universal bit-identical recomputation | Test a declared reference runtime and export the complete run [40][41][68][106] |
| Chemprop / ChemBERTa / MoLFormer / Uni-Mol | Learned molecular representations and predictions | Optional research extension | Applicability, data-split dependence and stochastic variation | Separate predictions, pin revisions and preserve evaluation design [32][61][60][53] |
| Notebooks and competition solutions | Guided exercises and concrete evaluation code | Student learning and prototyping | Moving dependencies, uneven licences and unconfirmed prize claims | Reuse narrowly, add regression fixtures and keep attribution [101][95] |

The non-obvious tension is that **more normalisation can improve deduplication while reducing fidelity to the submitted material**. Similarly, more engines can improve interoperability while making exact comparisons harder, and more ML can improve spectacle while weakening a clear distinction between calculated, observed and predicted values. These are design trade-offs, not reasons to omit the tools.

A second tension concerns reproducibility itself: a chemically meaningful hash deliberately ignores selected representation differences, while a byte hash must detect them. Keep both. RDKit's chemistry-aware registration hashing and a portable workflow-provenance package address complementary layers rather than competing definitions of truth. [35][106]

**Recommended fork/merge order:** first build the thin UI and explicit result schema; integrate RDKit plus the ChEMBL pipeline; add Ketcher and 3Dmol.js; freeze a small PubChem/ChEMBL corpus; implement run export and offline replay; then add one teaching notebook and, only if time permits, one pinned prediction plugin. Treat MolVS and older hackathon repositories as reference material rather than automatic foundations.

The winning proposition is not "another molecule-property calculator." It is: **"We can show exactly what was submitted, what changed, where every value came from, why a value is missing, and whether another machine reproduced the declared run."** The inventory provides reusable components for that proposition; the trust contract is the part ProvenanceLab must build.


## References

### Project sources

The inventory URLs are the canonical project sources used for project metadata; repeated projects are listed once here. Browser capabilities and licence exceptions additionally use the project documentation/licence citations beside the relevant claims.

- 3dmol/3Dmol.js: https://github.com/3dmol/3Dmol.js. [14]
- aiidateam/aiida-core: https://github.com/aiidateam/aiida-core. [42]
- astral-sh/uv: https://github.com/astral-sh/uv. [48]
- cbouy/mols2grid: https://github.com/cbouy/mols2grid. [17]
- cdk/cdk: https://github.com/cdk/cdk. [21]
- chembl/chembl_beaker: https://github.com/chembl/chembl_beaker. [115]
- chembl/ChEMBL_Structure_Pipeline: https://github.com/chembl/ChEMBL_Structure_Pipeline. [8]
- chembl/chembl_webresource_client: https://github.com/chembl/chembl_webresource_client. [25]
- chembl/chemistry_service: https://github.com/chembl/chemistry_service. [26]
- cheminfo/openchemlib-js: https://github.com/cheminfo/openchemlib-js. [83]
- chemprop/chemprop: https://github.com/chemprop/chemprop. [23]
- chinchillaa/neurips-open-polymer-prediction-2025: https://github.com/chinchillaa/neurips-open-polymer-prediction-2025. [92]
- computationalmodelling/nbval: https://github.com/computationalmodelling/nbval. [46]
- conda/conda-lock: https://github.com/conda/conda-lock. [44]
- datalad/datalad: https://github.com/datalad/datalad. [41]
- datamol-io/datamol: https://github.com/datamol-io/datamol. [9]
- datamol-io/medchem: https://github.com/datamol-io/medchem. [19]
- datamol-io/molfeat: https://github.com/datamol-io/molfeat. [18]
- dataprofessor/bioinformatics_freecodecamp: https://github.com/dataprofessor/bioinformatics_freecodecamp. [55]
- deepchem/deepchem: https://github.com/deepchem/deepchem. [22]
- deepforestsci/chemberta3: https://github.com/deepforestsci/chemberta3. [81]
- DeepGraphLearning/torchdrug: https://github.com/DeepGraphLearning/torchdrug. [49]
- deepmodeling/Uni-Mol: https://github.com/deepmodeling/Uni-Mol. [53]
- dmis-lab/MolPLA: https://github.com/dmis-lab/MolPLA. [91]
- epam/Indigo: https://github.com/epam/Indigo. [110]
- epam/ketcher: https://github.com/epam/ketcher. [12]
- greglandrum/rdkit_blog: https://github.com/greglandrum/rdkit_blog. [114]
- IBM/molformer: https://github.com/IBM/molformer. [82]
- IUPAC-InChI/InChI: https://github.com/IUPAC-InChI/InChI. [111]
- iwatobipen/chemo_info: https://github.com/iwatobipen/chemo_info. [30]
- jsme-editor/jsme-editor.github.io: https://github.com/jsme-editor/jsme-editor.github.io. [13]
- jupyterhub/repo2docker: https://github.com/jupyterhub/repo2docker. [45]
- jupyterlite/jupyterlite: https://github.com/jupyterlite/jupyterlite. [52]
- mcs07/MolVS: https://github.com/mcs07/MolVS. [7]
- mcs07/PubChemPy: https://github.com/mcs07/PubChemPy. [24]
- molstar/molstar: https://github.com/molstar/molstar. [16]
- mordred-descriptor/mordred: https://github.com/mordred-descriptor/mordred. [20]
- napoles-uach/stmol: https://github.com/napoles-uach/stmol. [28]
- NCBI-Hackathons/drugdisco: https://github.com/NCBI-Hackathons/drugdisco. [54]
- nglviewer/ngl: https://github.com/nglviewer/ngl. [15]
- NixOS/nix: https://github.com/NixOS/nix. [47]
- openbabel/documentation: https://github.com/openbabel/documentation. [116]
- openbabel/openbabel: https://github.com/openbabel/openbabel. [10]
- partridgejiang/Kekule.js: https://github.com/partridgejiang/Kekule.js. [11]
- patrickfuller/imolecule: https://github.com/patrickfuller/imolecule. [56]
- PatWalters/practical_cheminformatics_tutorials: https://github.com/PatWalters/practical_cheminformatics_tutorials. [29]
- PatWalters/useful_rdkit_utils: https://github.com/PatWalters/useful_rdkit_utils. [113]
- rdkit/rdkit: https://github.com/rdkit/rdkit. [3]
- rdkit/rdkit-js: https://github.com/rdkit/rdkit-js. [6]
- ResearchObject/ro-crate-py: https://github.com/ResearchObject/ro-crate-py. [43]
- the-matter-lab/selfies: https://github.com/the-matter-lab/selfies. [112]
- treeverse/dvc: https://github.com/treeverse/dvc. [40]
- trungdong/prov: https://github.com/trungdong/prov. [51]
- volkamerlab/teachopencadd: https://github.com/volkamerlab/teachopencadd. [27]
- yoshida-lab/XenonPy: https://github.com/yoshida-lab/XenonPy. [50]
- YutaYokkaichi/NeurIPS---Open-Polymer-Prediction-2025: https://github.com/YutaYokkaichi/NeurIPS---Open-Polymer-Prediction-2025. [93]

### Chemistry, browser and licence documentation

- RDKit Book: https://www.rdkit.org/docs/RDKit_Book.html . [31]
- RDKit standardisation API: https://www.rdkit.org/docs/source/rdkit.Chem.MolStandardize.rdMolStandardize.html . [38]
- RDKit RegistrationHash: https://www.rdkit.org/docs/source/rdkit.Chem.RegistrationHash.html . [35]
- RDKit.js documentation/source and MinimalLib: https://www.rdkitjs.com/ ; https://github.com/rdkit/rdkit-js ; https://github.com/rdkit/rdkit/tree/master/Code/MinimalLib . [5][104][102]
- ChEMBL Structure Pipeline documentation: https://github.com/chembl/ChEMBL_Structure_Pipeline . [1]
- MolVS documentation: https://molvs.readthedocs.io/ . [37]
- Ketcher documentation: https://github.com/epam/ketcher . [98]
- JSME documentation and distribution licence: https://jsme-editor.github.io/ ; https://github.com/jsme-editor/jsme-editor.github.io . [34][105]
- 3Dmol.js documentation and licence: https://3dmol.org/ ; https://github.com/3dmol/3Dmol.js . [36][78]
- Kekule.js and its Open Babel bundle: https://github.com/partridgejiang/Kekule.js ; https://github.com/partridgejiang/Kekule.js/tree/master/src/_extras/OpenBabel . [39][84]
- OpenChemLib JS documentation: https://github.com/cheminfo/openchemlib-js . [87]
- Chemprop documentation/licence: https://github.com/chemprop/chemprop . [32]
- TeachOpenCADD documentation: https://github.com/volkamerlab/teachopencadd . [101]
- Stmol documentation: https://github.com/napoles-uach/stmol . [86]
- DataLad COPYING; conda-lock licence and documentation; AiiDA documentation; ChEMBL client licence. Respective project URLs above. [79][80][68][66][73]

### Data, models, papers and cases

- ChEMBL releases and ChEMBL 37 files: https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/ ; https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/ . [64][108]
- ChEMBL licensing/attribution guidance: ChEMBL's published data-licensing guidance. [63]
- PubChem downloads: https://pubchem.ncbi.nlm.nih.gov/docs/downloads ; https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Monthly/ ; https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/ . [65][109][62]
- PubChem 2025 update, Nucleic Acids Research: https://doi.org/10.1093/nar/gkae1059 . [107]
- An open source chemical structure curation pipeline using RDKit, foundational 2020 paper. [99]
- Recording provenance of workflow runs with RO-Crate, 2024 paper. [106]
- ChemBERTa-3 preprint and 2026 Digital Discovery article; code: https://github.com/deepforestsci/chemberta3 . [61][72]
- Chemprop v2 paper, methods and reproducibility artefacts. [103]
- MolPLA paper and repository: https://github.com/dmis-lab/MolPLA . [69][85]
- HF model cards: https://huggingface.co/ibm-research/MoLFormer-XL-both-10pct ; https://huggingface.co/DeepChem/ChemBERTa-77M-MLM ; https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1 . [60][58][59]
- Open Polymer Challenge: https://open-polymer-challenge.github.io/ ; Kaggle competition: https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025 ; implementation: https://github.com/chinchillaa/neurips-open-polymer-prediction-2025 . [94][95]
- Illinois chemistry team's Mol-Hunter hackathon win: https://chemistry.illinois.edu/news/2024-05-23/illinois-chemistry-team-wins-computational-science-hackathon . [96]
- Tokyo-1 Drug Discovery Hackathon 2025 event report, published 2025-10-03. [88]
- Hits From A Hackathon, Rowan, 2026-08-07: https://www.rowansci.com/blog/hits-from-a-hackathon ; associated data: https://github.com/bioArena/tbxt-hackathon-data . [74]
- ADMETlab 3.0 paper and web service: https://admetlab3.scbdd.com/ . [90]
- Hexacyclinol original article with publisher retraction notice: https://onlinelibrary.wiley.com/doi/full/10.1002/anie.200504033 ; retraction notice: https://onlinelibrary.wiley.com/doi/10.1002/anie.201206869 . [77]
- Reviewed thalidomide stereochemistry/racemisation discussion. [75]

## References

1. *GitHub - chembl/ChEMBL_Structure_Pipeline: ChEMBL database structure pipelines · GitHub*. https://github.com/chembl/ChEMBL_Structure_Pipeline
2. *GitHub - mcs07/MolVS: Molecule Validation and Standardization · GitHub*. https://github.com/mcs07/MolVS
3. *api.github.com*. https://api.github.com/repos/rdkit/rdkit
4. *GitHub - rdkit/rdkit: The official sources for the RDKit library · GitHub*. https://github.com/rdkit/rdkit
5. *GitHub - rdkit/rdkit-js: A powerful cheminformatics and molecule rendering toolbelt for JavaScript, powered by RDKit . · GitHub*. https://github.com/rdkit/rdkit-js
6. *Rdkit Js*. https://api.github.com/repos/rdkit/rdkit-js
7. *api.github.com*. https://api.github.com/repos/mcs07/MolVS
8. *Chembl Structure Pipeline*. https://api.github.com/repos/chembl/ChEMBL_Structure_Pipeline
9. *Datamol Io*. https://api.github.com/repos/datamol-io/datamol
10. *api.github.com*. https://api.github.com/repos/openbabel/openbabel
11. *api.github.com*. https://api.github.com/repos/partridgejiang/Kekule.js
12. *api.github.com*. https://api.github.com/repos/epam/ketcher
13. *Jsme Editor.Github*. https://api.github.com/repos/jsme-editor/jsme-editor.github.io
14. *api.github.com*. https://api.github.com/repos/3dmol/3Dmol.js
15. *api.github.com*. https://api.github.com/repos/nglviewer/ngl
16. *api.github.com*. https://api.github.com/repos/molstar/molstar
17. *api.github.com*. https://api.github.com/repos/cbouy/mols2grid
18. *Datamol Io*. https://api.github.com/repos/datamol-io/molfeat
19. *Datamol Io*. https://api.github.com/repos/datamol-io/medchem
20. *Mordred Descriptor*. https://api.github.com/repos/mordred-descriptor/mordred
21. *api.github.com*. https://api.github.com/repos/cdk/cdk
22. *api.github.com*. https://api.github.com/repos/deepchem/deepchem
23. *api.github.com*. https://api.github.com/repos/chemprop/chemprop
24. *api.github.com*. https://api.github.com/repos/mcs07/PubChemPy
25. *Chembl Webresource Client*. https://api.github.com/repos/chembl/chembl_webresource_client
26. *Chemistry Service*. https://api.github.com/repos/chembl/chemistry_service
27. *api.github.com*. https://api.github.com/repos/volkamerlab/teachopencadd
28. *Napoles Uach*. https://api.github.com/repos/napoles-uach/stmol
29. *Practical Cheminformatics Tutorials*. https://api.github.com/repos/PatWalters/practical_cheminformatics_tutorials
30. *Chemo Info*. https://api.github.com/repos/iwatobipen/chemo_info
31. *The RDKit Book — The RDKit 2026.03.6 documentation*. https://www.rdkit.org/docs/RDKit_Book.html
32. *GitHub - chemprop/chemprop: Message Passing Neural Networks for Molecule Property Prediction · GitHub*. https://github.com/chemprop/chemprop
33. *GitHub - chembl/chembl_webresource_client: Official Python client for accessing ChEMBL API · GitHub*. https://github.com/chembl/chembl_webresource_client
34. *JSME Homepage - molecule structure input on the web*. https://jsme-editor.github.io/
35. *rdkit.Chem.RegistrationHash module — The RDKit 2026.03.5 documentation*. https://www.rdkit.org/docs/source/rdkit.Chem.RegistrationHash.html
36. *GitHub - 3dmol/3Dmol.js: WebGL accelerated JavaScript molecular graphics library · GitHub*. https://github.com/3dmol/3Dmol.js
37. *MolVS: Molecule Validation and Standardization — MolVS 0.1.1 documentation*. https://molvs.readthedocs.io/en/latest/
38. *rdkit.Chem.MolStandardize.rdMolStandardize module — The RDKit 2026.03.6 documentation*. https://www.rdkit.org/docs/source/rdkit.Chem.MolStandardize.rdMolStandardize.html
39. *GitHub - partridgejiang/Kekule.js: A Javascript cheminformatics toolkit. · GitHub*. https://github.com/partridgejiang/Kekule.js
40. *api.github.com*. https://api.github.com/repos/iterative/dvc
41. *api.github.com*. https://api.github.com/repos/datalad/datalad
42. *Aiida Core*. https://api.github.com/repos/aiidateam/aiida-core
43. *Ro Crate Py*. https://api.github.com/repos/ResearchObject/ro-crate-py
44. *Conda Lock*. https://api.github.com/repos/conda/conda-lock
45. *api.github.com*. https://api.github.com/repos/jupyterhub/repo2docker
46. *api.github.com*. https://api.github.com/repos/computationalmodelling/nbval
47. *api.github.com*. https://api.github.com/repos/NixOS/nix
48. *Astral Sh*. https://api.github.com/repos/astral-sh/uv
49. *api.github.com*. https://api.github.com/repos/DeepGraphLearning/torchdrug
50. *Yoshida Lab*. https://api.github.com/repos/yoshida-lab/XenonPy
51. *api.github.com*. https://api.github.com/repos/trungdong/prov
52. *api.github.com*. https://api.github.com/repos/jupyterlite/jupyterlite
53. *Uni Mol*. https://api.github.com/repos/deepmodeling/Uni-Mol
54. *Ncbi Hackathons*. https://api.github.com/repos/NCBI-Hackathons/drugdisco
55. *Bioinformatics Freecodecamp*. https://api.github.com/repos/dataprofessor/bioinformatics_freecodecamp
56. *api.github.com*. https://api.github.com/repos/patrickfuller/imolecule
57. *GitHub - NCBI-Hackathons/drugdisco: A high throughput automated drug discovery pipeline. · GitHub*. https://github.com/NCBI-Hackathons/drugdisco
58. *DeepChem/ChemBERTa-77M-MLM · Hugging Face*. https://huggingface.co/DeepChem/ChemBERTa-77M-MLM
59. *seyonec/ChemBERTa-zinc-base-v1 · Hugging Face*. https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1
60. *ibm-research/MoLFormer-XL-both-10pct · Hugging Face*. https://huggingface.co/ibm/MoLFormer-XL-both-10pct
61. *ChemBERTa-3: An Open Source Training Framework for Chemical Foundation Models*. https://chemrxiv.org/doi/pdf/10.26434/chemrxiv-2025-4glrl-v2
62. *Index of /pubchem/Compound/CURRENT-Full*. https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/
63. *ChEMBL licensing*. https://chembl.github.io/chembl-licensing
64. *Index of /pub/databases/chembl/ChEMBLdb/releases*. https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/
65. *Downloads - PubChem*. https://pubchem.ncbi.nlm.nih.gov/docs/downloads
66. *GitHub - aiidateam/aiida-core: The official repository for the AiiDA code · GitHub*. https://github.com/aiidateam/aiida-core
67. *GitHub - IBM/molformer: Repository for MolFormer · GitHub*. https://github.com/IBM/molformer
68. *GitHub - conda/conda-lock: Lightweight lockfile for conda environments · GitHub*. https://github.com/conda/conda-lock
69. *MolPLA: a molecular pretraining framework for learning cores, R-groups and their linker joints*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11211832/
70. *GitHub - deepforestsci/chemberta3: ChemBERTa-3 Repo · GitHub*. https://github.com/deepforestsci/chemberta3
71. *ChemRxiv: chemistry preprints*. https://chemrxiv.org/doi/10.26434/chemrxiv-2025-dzh5z
72. [
        
    ChemBERTa-3: an open source training framework for chemical foundation models - Digital Discovery (RSC Publishing)

    ](https://pubs.rsc.org/en/content/articlelanding/2026/dd/d5dd00348b)
73. *chembl_webresource_client/LICENSE at master · chembl/chembl_webresource_client · GitHub*. https://github.com/chembl/chembl_webresource_client/blob/master/LICENSE
74. *Hits From a Hackathon | Rowan*. https://www.rowansci.com/blog/hits-from-a-hackathon
75. [
            Thalidomide‐induced teratogenesis: History and mechanisms - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC4737249/)
76. *nbval/LICENSE at master · computationalmodelling/nbval · GitHub*. https://github.com/computationalmodelling/nbval/blob/master/LICENSE
77. *Total Syntheses of Hexacyclinol, 5‐<i>epi</i>‐Hexacyclinol, and Desoxohexacyclinol Unveil an Antimalarial Prodrug Motif<link href='#nss'></link> - La Clair - 2006 - Angewandte Chemie International Edition - Wiley Online Library*. https://onlinelibrary.wiley.com/doi/full/10.1002/anie.200504033
78. *3Dmol.js/LICENSE at master · 3dmol/3Dmol.js · GitHub*. https://github.com/3dmol/3Dmol.js/blob/master/LICENSE
79. *datalad/COPYING at master · datalad/datalad · GitHub*. https://github.com/datalad/datalad/blob/main/COPYING
80. *conda-lock/LICENSE at main · conda/conda-lock · GitHub*. https://github.com/conda/conda-lock/blob/main/LICENSE
81. *api.github.com*. https://api.github.com/repos/deepforestsci/chemberta3
82. *api.github.com*. https://api.github.com/repos/IBM/molformer
83. *Openchemlib Js*. https://api.github.com/repos/cheminfo/openchemlib-js
84. *Kekule.js/src/_extras/OpenBabel at master · partridgejiang/Kekule.js · GitHub*. https://github.com/partridgejiang/Kekule.js/tree/master/src/_extras/OpenBabel
85. *GitHub - dmis-lab/MolPLA*. https://github.com/dmis-lab/MolPLA
86. *GitHub - napoles-uach/stmol: This is the repository for the Stmol project, a Streamlit component that uses py3Dmol to render molecules. · GitHub*. https://github.com/napoles-uach/stmol
87. *GitHub - cheminfo/openchemlib-js: JavaScript port of OpenChemLib · GitHub*. https://github.com/cheminfo/openchemlib-js
88. *Tokyo-1 Drug Discovery Hackathon 2025 Event Report | 株式会社ゼウレカ*. https://xeureka.co.jp/en/1617
89. *GitHub - Dishant707/molio: ⚛️ atoma — Universal molecular file parser & analyzer. PDB, mmCIF, SDF, XYZ. CLI, Desktop GUI, Web WASM. 5-13x faster than Biopython/RDKit/OpenBabel. · GitHub*. https://github.com/Dishant707/molio
90. *ADMETlab 3.0: an updated comprehensive online ADMET prediction platform enhanced with broader coverage, improved performance, API functionality and decision support | Nucleic Acids Research | Oxford Academic*. https://academic.oup.com/nar/article/52/W1/W422/7640525
91. *Dmis Lab*. https://api.github.com/repos/dmis-lab/MolPLA
92. *Neurips Open Polymer Prediction 2025*. https://api.github.com/repos/chinchillaa/neurips-open-polymer-prediction-2025
93. *Neurips Open Polymer Prediction 2025*. https://api.github.com/repos/YutaYokkaichi/NeurIPS---Open-Polymer-Prediction-2025
94. *NeurIPS Competition Open Polymer Challenge: Leveraging Machine Learning for Polymer Informatics*. https://neurips.cc/virtual/2025/competition/127721
95. *GitHub - chinchillaa/neurips-open-polymer-prediction-2025: NeurIPS Open Polymer Prediction 2025 Kaggle Competition - Machine learning pipeline for predicting polymer properties from molecular structure data*. https://github.com/chinchillaa/neurips-open-polymer-prediction-2025
96. *Illinois chemistry team wins computational science hackathon | Department of Chemistry | Illinois*. https://chemistry.illinois.edu/news/2024-05-23/illinois-chemistry-team-wins-computational-science-hackathon
97. *GitHub - mordred-descriptor/mordred: a molecular descriptor calculator · GitHub*. https://github.com/mordred-descriptor/mordred
98. *GitHub - epam/ketcher: Web-based molecule sketcher · GitHub*. https://github.com/epam/ketcher
99. *An open source chemical structure curation pipeline using RDKit | Journal of Cheminformatics | Springer Nature Link*. https://link.springer.com/article/10.1186/s13321-020-00456-1
100. *Index of /pubchem/Compound*. https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/
101. *GitHub - volkamerlab/teachopencadd: TeachOpenCADD: a teaching platform for computer-aided drug design (CADD) using open source packages and data · GitHub*. https://github.com/volkamerlab/teachopencadd
102. *rdkit/Code/MinimalLib at master · rdkit/rdkit · GitHub*. https://github.com/rdkit/rdkit/tree/master/Code/MinimalLib
103. *Chemprop v2: An Efficient, Modular Machine Learning Package for Chemical Property Prediction — 14 September 2025*. https://chemrxiv.org/doi/pdf/10.26434/chemrxiv-2025-4p1nr
104. *RDKit.js Documentation | RDKit.js is a powerful cheminformatics and molecule rendering toolbelt for JavaScript. Official docs with examples for React, Vue, Angular, Svelte, Next.js, Node.js, and vanilla JS.*. https://www.rdkitjs.com/
105. *jsme-editor.github.io*. https://jsme-editor.github.io/dist/license.txt
106. *Recording provenance of workflow runs with RO-Crate | PLOS One*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210
107. *PubChem 2025 update | Nucleic Acids Research | Oxford Academic*. https://academic.oup.com/nar/article/53/D1/D1516/7903365
108. *Index of /pub/databases/chembl/ChEMBLdb/releases/chembl_37*. https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/
109. *Index of /pubchem/Compound/Monthly*. https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Monthly/
110. *api.github.com*. https://api.github.com/repos/epam/Indigo
111. *Iupac Inchi*. https://api.github.com/repos/IUPAC-InChI/InChI
112. *Aspuru Guzik Group*. https://api.github.com/repos/aspuru-guzik-group/selfies
113. *Useful Rdkit Utils*. https://api.github.com/repos/PatWalters/useful_rdkit_utils
114. *Rdkit Blog*. https://api.github.com/repos/greglandrum/rdkit_blog
115. *Chembl Beaker*. https://api.github.com/repos/chembl/chembl_beaker
116. *api.github.com*. https://api.github.com/repos/openbabel/documentation
