<!-- run id: trun_3b693d434bb94e6da71f0ac39267f122 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 14:52 IST (verbatim getResultMarkdown output below, unedited) -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6da71f0ac39267f122
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T08:52:12.047223Z
**Modified:** 2026-10-24T09:05:54.872408Z

## Output

# Building a Safer Indian Prescription Checker From Reusable Tools

## Executive Summary

- **Start With Indian Brand Resolution**: A-Z offers a nine-column Indian medicine catalogue, but only two composition fields. That is useful for lookup, not proof that every multi-ingredient product is fully represented -> preserve ingredient arrays and require confirmation when composition is incomplete. [21]
- **Fork A Prototype, Not Its Claims**: RxCheck is an MIT-licensed prescription-checking application with a documented mapping of **34 brands** -> it is a strong starting shell, but not a ready-made national medicine database or clinically validated safety engine. [38]
- **Do Not Build On A Retired Interaction API**: RxNav's official notice scheduled discontinuation of its drug-interaction features around **January 2, 2024** -> use RxNorm for terminology, and obtain interaction evidence separately. [14]
- **DDInter Is Promising, But Rights Remain A Gate**: DDInter 2.0 reports **302,516 interactions involving 2,290 approved drugs**, while its displayed last data update is **May 14, 2024** -> distinguish the newer publication/version from the age and reuse terms of its data. [6]
- **Public Does Not Mean Freely Mergeable**: Indian datasets carry materially different labels: CC BY-SA 4.0, MIT, Apache 2.0, CC BY-NC-SA 4.0, and unknown -> record both the uploader's licence and the upstream source before redistributing scraped commercial catalogues. [21][3][18][43][44]
- **Make The Indian Harm Concrete, Not Sensational**: A review published in 2025 includes **40 studies and 307,106 patients**, reporting a **median medication-error rate of 34.11%** -> describe this as a heterogeneous hospital-study finding, not a national probability for any prescription. [2]
- **Use Current Regulatory Examples**: CDSCO lists **156 prohibited FDCs dated August 2, 2024**, and **16 dated June 11, 2026** -> make formulation-specific regulatory checks a visible India-specific feature. [13]
- **Separate Duplication, Dose And Interaction**: A duplicated ingredient is not automatically an overdose; a normal-looking daily total is not automatically safe for a child or someone with renal impairment -> show separate findings, assumptions and unassessed checks.
- **Keep OCR Optional**: HM-02 starts with typed prescriptions. An available prescription OCR model is explicitly not clinically validated -> spend the first implementation effort on ingredient resolution, deterministic calculations and clear uncertainty, not handwriting spectacle. [47]

**Bottom line:** Build a transparent, source-linked decision-support demo: Indian brand catalogue -> confirmed ingredients and strengths -> deterministic duplicate/dose checks -> independently sourced interactions -> a small, ranked set of actionable alerts. Do not present it as an autonomous prescribing system.

**Scope and status.** This is a broad reusable-resource inventory, not a defensible claim to have found every repository on the internet. Dates below are source-reported; "created" is not "last updated," and relative labels such as "two months ago" are preserved rather than converted into invented dates. "Not established" means the requested detail was not publicly confirmed in the material reviewed. Coverage figures describe the source, not independently measured accuracy.

## 1. Indian Catalogues: Resolve Brands Before Checking Safety

The key local asset is a catalogue that can expand a brand into **all ingredients, amount, denominator, formulation and route**. Price, product descriptions and substitutes are secondary. A catalogue with many rows can still fail this task if strengths are embedded in prose or a third ingredient has nowhere to go.

### Downloadable Indian medicine datasets

In the tables, "backend" answers whether the resource can support your own website, rather than merely being viewable on someone else's website.

| Resource and URL | Plain-words use and coverage | Update reported | Licence and hackathon implications | Backend and combine-with |
|---|---|---|---|---|
| **A-Z Medicine Dataset of India** - `https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india` | Indian product lookup; **32.06 MB**, nine columns including name, manufacturer, pack, discontinuation flag and `short_composition1/2`. Original scrape source is not identified in the card. | Page says updated four years ago; price/availability described as **November 2022**. | **CC BY-SA 4.0** as uploaded. Attribute and assess share-alike obligations for redistributed adaptations; do not infer upstream permission. | Downloadable CSV for a local lookup service. Combine with ingredient normalization, a completeness check and reviewed dose rules. [21] |
| **250k Medicines Usage, Side Effects and Substitutes** - `https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes` | Card describes **over 248,000 drugs**; **89.41 MB**, **58 columns**, including composition, side effects, substitutes and interaction-related information. Treat these as catalogue fields, not a validated interaction engine. | Page says updated four years ago. | **CC BY-SA 4.0**. Same upstream-provenance caution. | Downloadable data; useful enrichment for the brand table, not an independent clinical corroboration source if it shares the same upstream catalogue. [20] |
| **1mg 117k Medicine Complete Data With Image Link** - `https://www.kaggle.com/datasets/abhay13072009/1mg-117k-medicine-complete-data-with-image-link` | Card says **117,000+** medicine/capsule/injection records scraped from **1mg**; NDJSON with composition, manufacturer, pack, uses, side effects and image links. Missing values are acknowledged. | Page says updated **two months ago**. | Uploader labels **MIT**. That does not establish a right to republish all 1mg text or images. | Downloadable NDJSON; strong candidate for a recent catalogue ingestion experiment. Combine with provenance, deduplication and strength parsing. [3] |
| **Indian Medicine Data** - `https://www.kaggle.com/datasets/mohneesh7/indian-medicine-data` | **354.16 MB**; eight fields including product, salt composition, manufacturer, description, side effects and drug interactions. Missing values remain as-is. Row count and original provenance are not established. | Page says updated three years ago. | **Apache 2.0** uploader label; confirm upstream rights separately. | Downloadable data; combine with a cleaner brand dictionary. Do not convert narrative interaction text directly into hard-stop rules. [18] |
| **MedOps medicine-dataset** - `https://github.com/The-MedOps/medicine-dataset` | Repository reports **253,973 products**, **14 JSON files**, about **96 MB** original data. Its schema also has only two short-composition fields. | Repository creation reported **June 12, 2026**; latest update not established. | A reusable licence was **not established**. Public GitHub access alone is insufficient. | JSON is convenient for a local service once permission is resolved; combine with schema validation and a complete ingredient model. [19] |
| **India Medicines and Drug Info Dataset** - `https://www.kaggle.com/datasets/apkaayush/india-medicines-and-drug-info-dataset` | Card claims roughly **300,000 rows**, **115.75 MB**, nine columns, collected from **Tata 1mg** in **2025**. Includes names, composition, manufacturer/category and price information. | Page says updated a year ago; collection year explicitly 2025. | **CC BY-NC-SA 4.0**. Noncommercial restriction matters for sponsored or commercial continuation; upstream rights remain a separate question. | Downloadable catalogue. Combine with a source/version manifest and data cleaning; freshness and cleanliness are not guaranteed by its size. [43] |
| **Medicines Dataset, ujjwalgupta23** - `https://www.kaggle.com/datasets/ujjwalgupta23/medicines-dataset` | Card claims **200,000+** products; `tata_1mg_Medicine_data.csv`, **57.22 MB**, seven columns including composition, manufacturer, quantity, price and image. | Page says updated a year ago. | Licence displayed as **Unknown**. Inspecting a candidate is different from permission to merge or redistribute it. | Downloadable CSV; alternative ingestion candidate after rights are clarified. [44] |

**Takeaway:** These are alternative catalogue candidates, not seven independent clinical authorities. Prefer a source with explicit provenance, complete ingredient representation and usable rights over the largest advertised row count.

### Scrapers, Netmeds and official Indian lists

| Resource and URL | What is verified; coverage | Update | Licence/use | Backend and combine-with |
|---|---|---|---|---|
| **1mg drugs/medicine scraper** - `https://github.com/narender-rk10/1mg-drugs-medicine-scrapper` | Python scraping code and SQLite workflow; README describes 20+ fields including ingredients, strengths, forms and warnings. Its **100,000+** figure is an estimate, not an audited supplied-record count. | Latest update not established; three commits and no releases reported in the reviewed page. | **MIT code**; its own instructions call for respecting robots/terms. Code licensing does not license source-site content. | Can feed your own catalogue service. Combine with rate limits, provenance and a lawful ingestion plan. [40] |
| **Netmeds BeautifulSoup scraper, Supriyochow** - `https://github.com/Supriyochow/Web-Scraping-of-netmeds-website-using-BeautifulSoup` | Notebook/CSV project; README reports **27,440 records**. A complete normalized composition-and-strength schema was not established. | Created **April 5, 2021**; latest update not established. | Licence not established. | Local scraping/data-analysis starting point, not a verified safety catalogue. Pair with a composition audit before any merge. [51] |
| **Netmeds End-to-End Data Analysis, Sanjay00013** - `https://github.com/Sanjay00013/Netmeds_End_to_End_Data_Analysis_Project` | README describes **27,000+** products and fields including medicine name, manufacturer, prescription status, dosage and composition. Not evidence of a clinically normalized strength database. | Created **February 21, 2025**; latest update not established. | Licence not established. | Candidate scraping/analysis pipeline; compare field completeness with the 1mg candidates. [49] |
| **PMBI / Jan Aushadhi Product and MRP List** - `https://www.pmbi.co.in/ProductList.aspx` | Official product-list page with search and PDF-export instructions. The reviewed page did not establish a current row count, a resolved update date or a public API. | Displayed date was an unresolved template, not a usable date. | Public official reference; bulk open-data licence not established. | Website reference/export workflow, not a confirmed ready-made backend feed. Use for official generic-product checks and provenance, not all Indian brands. [12] |
| **CDSCO FDC portal and lists** - `https://cdsco.gov.in/opencms/opencms/en/Drugs/FDC` | Official regulatory approvals/prohibitions material; includes the **156-FDC 2024** and **16-FDC 2026** prohibition lists. It is not a complete brand-to-composition registry. | Individual list dates matter: **August 2, 2024** and **June 11, 2026**. | Official reference; a blanket reusable machine-readable-data licence was not established. | Website/PDF source. Convert relevant notifications into carefully reviewed, formulation-specific rules with source links. [13] |

**Takeaway:** Netmeds projects are real candidates, but their existence does not prove medically complete data or redistribution rights. PMBI and CDSCO add official provenance and regulatory context; neither replaces a national brand catalogue.

**PharmEasy gap:** A PharmEasy-named prescription-flow repository is verified below. A separately verified, openly licensed PharmEasy brand-composition dataset was **not established**. Do not relabel a 1mg CSV as PharmEasy data.

### Case study: A-Z's two composition columns create a hidden FDC risk

A-Z offers an accessible schema and a declared licence, which makes it appealing for a hackathon. However, its two composition columns cannot by themselves establish complete coverage for products containing more ingredients. The same structural limitation appears in the MedOps schema. [21][19]

**Proposed implementation outcome:** Import those fields into an ingredient array, but retain a `composition_complete` status. If the full product label or another reviewed record suggests additional ingredients, stop short of a green safety result. A small, complete catalogue for the demo is more defensible than a huge catalogue that silently drops an ingredient.

## 2. Interaction Resources: Distinguish Rules, Terminology And Signals

These resources solve different problems. A name-normalization API is not an interaction checker; an adverse-event association is not automatically a contraindication; a free website is not necessarily a downloadable open database.

| Resource and URL | Description and size/coverage | Last update/version evidence | Licence and hackathon use | Website/backend and combine-with |
|---|---|---|---|---|
| **DDInter 2.0** - `https://ddinter2.scbdd.com/` | Curated interaction resource with risk/mechanism/management material and food, disease and therapeutic-duplication features; **302,516 DDIs**, **2,290 approved drugs** reported. | Displayed data update **May 14, 2024**. | Redistribution licence not established. Open access is not equivalent to open data. | Working web interface; a public production API was not established. Combine with normalized ingredients and a licensed/local rule layer. [6] |
| **Original DDInter downloads** - `https://ddinter.scbdd.com/download/` | Downloadable CSV groups and risk/management/mechanism information. | Exact refresh date not established. | Bulk reuse terms require confirmation. | Local import is technically possible, but do not assume these files equal the complete newer 2.0 database. [10] |
| **DrugBank open-data releases** - `https://go.drugbank.com/releases/latest#open-data` | Open vocabulary/identifier and structure assets. Release page lists **5.1.22, June 27, 2026**, including **1.12 MB** vocabulary CSV and **5.16 MB** structure SDF; availability warnings appear on the page. | Explicit release date above. | Those open assets are **CC0**. They are **not** a free grant to the full DrugBank interaction database or commercial API. | Download assets if available; combine identifiers with separately licensed clinical rules. [11] |
| **DrugBank full datasets / services** - `https://go.drugbank.com/datasets` | Broader drug knowledge and interaction capabilities. Exact usable interaction coverage depends on the product/entitlement. | Current access and academic-download availability must be checked; the reviewed page describes paused academic downloads. | Broader datasets carry **CC BY-NC 4.0** terms in the reviewed material; API access is a separate product, not implied by the vocabulary licence. | Vendor website/dataset/service route. Resolve entitlement before designing the demo around live calls. [11] |
| **RxNorm / RxNav / RxTerms / RxClass** - `https://lhncbc.nlm.nih.gov/RxNav/` and `https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html` | Ingredient/product terminology, identifiers, classes and normalization; useful bridge after Indian brand expansion. Not a comprehensive Indian brand catalogue or a current DDI service. | RxNav describes monthly updates; reviewed release listing includes **June 1, 2026**. | Public APIs are available; distinguish API access from redistribution of underlying proprietary-source terminology. | REST services, RxMix and **RxNav-in-a-Box** self-hosting options. Pair with an Indian catalogue and separate interactions. [14] |
| **openFDA drug labels** - `https://open.fda.gov/apis/drug/label/` | API access to submitted structured product-label content, including narrative safety and dosing sections where present. US labels, not Indian brand coverage. | Described as a living dataset; no fixed inventory count used here. | Check `https://open.fda.gov/terms/`; do not interpret public access as clinical validation of your application. | Genuine API. Combine with a label-to-rule review process, not automatic extraction into hard stops. [33] |
| **TWOSIDES / OFFSIDES** - `https://tatonettilab.org/resources/tatonetti-stm.html` | TWOSIDES reports **868,221 significant associations**, **59,220 drug pairs**, **1,301 adverse events**. OFFSIDES reports **438,801 associations**, **1,332 drugs**, **10,097 events**. | Release freshness not established; these are research-resource figures. | Reuse licence not established in the reviewed page. | Downloadable research files. Use for hypothesis generation or explainable research enrichment, not automatic contraindications. [16] |
| **SIDER 4.1** - `http://sideeffects.embl.de/` | Drug-side-effect resource: **1,430 drugs**, **5,868 side effects**, **139,756 pairs**; frequency information for **39.9%** of pairs. Not a pairwise interaction engine. | **October 21, 2015** release; site warns it is unfunded/outdated. | **CC BY-SA 4.0** plus relevant MedDRA terms; educational/scientific use, not medical advice. | Downloadable data and website. Useful for an explanation layer, not current dose or DDI authority. [5] |
| **Hetionet v1** - `https://github.com/hetio/hetionet` | Integrative biomedical graph: **47,031 nodes**, **11 node types**, **2,250,197 relationships**, **24 relationship types**. Not a prescription safety rulebook. | Latest update not established. | Original integration content is **CC0**, but upstream licences apply; licence metadata varies by format. | JSON, Neo4j and TSV/matrix downloads. Combine with an exploratory knowledge graph; retain source-level licences. [9] |
| **DrugCentral** - `https://drugcentral.org/` | Additional drug-knowledge resource to inspect for terminology and evidence enrichment. A complete, India-ready DDI/dose engine was not established here. | Exact relevant update and usable subset size not established in this inventory. | Check licence at the required dataset/field level before incorporation. | Website/data-resource candidate; combine only after checking the required export or service and its terms. [54] [54] [54] [54] [54] [54] [54] [54] [54] [54] [54] |

**Takeaway:** For a demo, curated interactions and terminology should be separate dependencies. TWOSIDES, SIDER and Hetionet are valuable research resources, but none should silently become the application's authoritative contraindication list.

### Case study: RxNav is useful precisely because its role is narrower

RxNav offers terminology APIs and a self-hosting route, while its official interaction-service notice says the interaction features were being discontinued. A team following an old tutorial could successfully normalize medicines and still have a broken interaction path. [14]

**Recommended decision:** Put a stable internal ingredient identifier between the Indian catalogue and every external resource. Use RxNorm where it helps with synonyms and terminology, then query a separately governed interaction layer. If that layer is unavailable, report **"interaction check unavailable"**, not "no interactions found."

## 3. Dose Safety: Build A Small Reviewed Rule Set, Not A Universal Calculator

No comprehensive, freely reusable, India-specific, computable adult/pediatric/renal dosing database was established in this inventory. That is a scope limit, not evidence that none exists. The workable hackathon approach is a small set of reviewed rules tied to explicit sources and patient contexts.

| Source and URL | What it can support | Update and coverage | Licence/use | Backend and combine-with |
|---|---|---|---|---|
| **DailyMed web services** - `https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm` | Retrieve US Structured Product Labels and associated information; useful for dose, contraindication and renal-warning evidence. | Changing label collection; record each selected label's own date/version. | Public service access does not establish one blanket licence for every embedded label asset. | REST integration/source retrieval. Combine with clinician-reviewed extraction into narrow rules. [23] [23] [23] [23] [23] [23] [23] [23] |
| **FDA acetaminophen guidance** - `https://www.fda.gov/drugs/safe-use-over-counter-pain-relievers-and-fever-reducers/acetaminophen` | Public-facing source for total acetaminophen exposure and duplicate-product warnings. | General guidance, not a complete age/weight/renal dosing table. | Official guidance reference; not a ready-made dosing dataset/API. | Website evidence for a reviewed paracetamol/acetaminophen rule; retain qualifications. [35] [35] [35] [35] [35] [35] [35] [35] |
| **ICMR Standard Treatment Workflows** - `https://www.icmr.gov.in/standard-treatment-workflows-stws` | Indian clinical workflows and specialty PDFs, useful for local clinical context and selected source-backed rules. | Listing page updated **August 19, 2026**; that is not the publication date of every linked guideline. | Open-data/code licence not established. Publicly accessible PDFs are not a computable dose engine. | Website/PDF reference; combine with manual rule authoring and clinical review. [46] |
| **ICMR Hypertension in Adults workflow** - `https://www.icmr.gov.in/icmrobject/uploads/STWs/1778941063_hypertensioninadults_final.pdf` | Example of a primary Indian workflow. Its advisory nature and patient-specific judgment matter. | Use the document's own version where stated; do not infer its date from the listing page. | Reference document; machine-readable reuse terms not established. | Readable PDF, not API. Pair selected recommendations with explicit eligibility and exceptions. [57] |

**Takeaway:** The difficult work is translating a source into a conditional rule without discarding its exceptions. A dose threshold without route, formulation, patient group and source version is not a dependable safety rule.

### A safe calculation contract for the demo

The following is a **proposed input contract**, not a claim that every handwritten abbreviation is unambiguous:

| Input/check | Proposed behavior | Failure avoided |
|---|---|---|
| OD / BD / TDS | In the confirmed dosing-frequency field, interpret as once / twice / three times daily and show the expansion before checking. Ask for confirmation where context is ambiguous. | Treating ambiguous abbreviations as certain instructions. |
| SOS / as needed | Require maximum units per occasion and maximum administrations per 24 hours, or report that maximum daily exposure cannot be assessed. | Inventing a daily frequency. |
| Tablets/capsules | `ingredient amount per unit x units per dose x administrations per day`, summed across products. | Counting brands rather than active ingredients. |
| Liquids | Preserve both numerator and denominator, such as mg per 5 mL, then convert using the prescribed mL. | Treating mg/5 mL as mg/mL. |
| Children | Require age, weight with units, and the correct rule type: mg/kg/**dose** versus mg/kg/**day**. | A fivefold or schedule-dependent calculation error hidden by correct arithmetic. |
| Kidney function | Require the renal measure, value, units and the measure required by the specific rule; do not silently substitute eGFR for creatinine clearance. | Applying the wrong eligibility threshold. |
| Formulation/route | Keep immediate-release, modified-release and route distinct. | Treating all products with the same ingredient as interchangeable. |
| Missing context | Display **"not assessed: missing ..."** and the exact information needed. | A false green result from absent patient data. |

**Takeaway:** Separate parsing certainty from clinical certainty. Correct multiplication does not establish that the selected dose rule applies.

### Case study: duplicated paracetamol is not the same as overdose

**Synthetic demo, not a real-brand assertion:** Product A contains 650 mg paracetamol per tablet, one tablet BD. Product B contains 500 mg paracetamol per tablet, one tablet TDS. The calculated total is **650 x 2 + 500 x 3 = 2,800 mg/day**. The checker should flag duplicate exposure even though a single universal overdose conclusion cannot be made from that number alone.

FDA guidance states a maximum of **4,000 mg in 24 hours for adults and children 12 years and older**, and warns against using more than one acetaminophen-containing product at a time. Do not repurpose that figure as a recommended target or a universal safe limit for every patient; the cited page is not a renal-adjustment or full pediatric dosing database. [35] [35] [35] [35] [35] [35] [35] [35]

The demo's useful outcome is two separate messages: **"two products contain the same ingredient"** and **"dose assessment uses these patient assumptions."** Changing the patient's age, missing weight or renal context should change assessment status, not merely change the color of the same generic warning.

## 4. Forkable Apps: Reuse Workflow, Rebuild The Evidence Boundary

| Project and URL | What it does; coverage | Update evidence | Licence / hackathon use | Backend and combine-with |
|---|---|---|---|---|
| **RxCheck** - `https://github.com/indiser/Rxcheck` | Flask/Python/PostgreSQL prescription safety application; documented **34-brand** mapping, rule/catalogue files, external RxNorm/openFDA/LLM integrations. | Created **May 28, 2026**; latest commit date not established here. | **MIT code**. External services/data retain their own terms. | Strongest direct starting shell in this inventory. Replace/enlarge catalogue, audit rules and preserve stated limitations. [38] |
| **Indian Medicine MCP Server** - `https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER` | Indian medicine lookup, fuzzy/composition search and alternatives; README describes **15 endpoints**. Example responses are not an audited catalogue count. | Created **April 14, 2025**; latest update not established. | **MIT code**; inspect dataset provenance separately. | Locally runnable service/tool interface. Combine with a verified catalogue and deterministic safety engine. [37] |
| **Medicine Drug Advisor** - `https://github.com/sumankrsh/medicine-drug-advisor` | FastAPI/React/RAG application; README claims **45+ medicines** and **20+ mental-health conditions**, with query, drug and interaction endpoints. These are author-reported coverage claims. | Created **June 18, 2025**; three commits reported. | **MIT code**; source-data rights need separate review. Explicitly educational, not medical advice. | Local web/backend starting point for explanations; do not treat generated answers as clinical rules. [50] |
| **PharmEasy AI-assisted Prescription Flow** - `https://github.com/PKhetan0208/Pharmeasy-AI-assisted-Prescription-Flow` | Prescription-flow prototype with Node setup and Gemini API-key dependency. Not proof of official PharmEasy affiliation or a PharmEasy catalogue licence. | Created **June 4, 2026**; four commits reported. | Reusable licence not established. | App/backend code candidate; borrow workflow ideas only after permissions/dependencies are checked. [34] |
| **OpenEMR** - `https://github.com/openemr/openemr` | Broader open-source EHR platform, useful for medication-list and clinical-workflow integration rather than a small India-specific checker. | Use the selected release; a latest-release assertion is not made here. | GPL-family obligations require examination for the selected release and distribution model. | Self-hostable clinical application. Integrate a separate safety service rather than assuming it supplies Indian brand/dose coverage. [57] [57] [57] [57] [57] [57] [57] |
| **Vitatheca data** - `https://github.com/ziigzag/vitatheca-data` | Offline catalogue packaging with manifests/checksums and compressed SQLite. Repository describes roughly **820 MB** compressed full data and regional bundles around **280-290 MB**. Not established as an Indian catalogue. | Created **May 12, 2026**; latest update not established. | Compilation marked **CC0**, but upstream licences still apply. | Useful offline-distribution pattern; combine the packaging approach with your own permission-cleared catalogue. [52] |

**Takeaway:** RxCheck and the MCP server are practical accelerators, but code reuse does not import a trustworthy medical knowledge base. Keep the clinical rule engine testable without any LLM or network dependency.

### Additional niche repository leads

These candidates should remain visible rather than being silently excluded because their completeness or reuse permissions are unresolved.

| Project | URL | Candidate value | Update, licence and coverage status | Backend/use status | Combine-with |
|---|---|---|---|---|---|
| `gitzaan/Drug-Interaction-Checking-Website` | `https://github.com/gitzaan/Drug-Interaction-Checking-Website` | Additional interaction/safety prototype; inspect its rules and dependencies rather than assuming clinical completeness. | Latest commit, reusable data rights and validated coverage not established here. | Candidate web/app code; use only after checking the repository's actual licence and data sources. | Compare with RxCheck; do not inherit safety claims uncritically. [15] [15] [15] [15] [15] [15] [15] [15] [15] |
| `VidhyaES/drug-interaction-detector-nlp` | `https://github.com/VidhyaES/drug-interaction-detector-nlp` | Additional interaction/safety prototype; inspect its rules and dependencies rather than assuming clinical completeness. | Latest commit, reusable data rights and validated coverage not established here. | Candidate web/app code; use only after checking the repository's actual licence and data sources. | Compare with RxCheck; do not inherit safety claims uncritically. [8] [8] [8] [8] [8] [8] [8] [8] [8] [8] [8] |
| `thanmai-mathi/drug-safety-checker` | `https://github.com/thanmai-mathi/drug-safety-checker` | Additional interaction/safety prototype; inspect its rules and dependencies rather than assuming clinical completeness. | Latest commit, reusable data rights and validated coverage not established here. | Candidate web/app code; use only after checking the repository's actual licence and data sources. | Compare with RxCheck; do not inherit safety claims uncritically. [1] [1] [1] [1] [1] [1] [1] [1] [1] |

**Takeaway:** A repository's existence is verified separately from its safety claims. No clinical-validation or hackathon-winner status is inferred for these projects.

### Case study: RxCheck's 34-brand mapping is a useful boundary, not a defect to hide

RxCheck has the right architectural shape for HM-02: prescription input, local data/rules and external integrations. Its documented small brand mapping makes the coverage boundary visible, while its limitations acknowledge missed interactions and patient factors. [38]

**Recommended fork decision:** Retain the interface and separable services, replace the catalogue with permission-cleared records, and turn every demo case into a repeatable test. Do not reuse a README's "production" wording as evidence of measured clinical performance. A transparent 34-brand demo can be safer than an untested 250,000-row merge.

## 5. Fuzzy Matching, Small Models And OCR: Use Them To Extract, Not Prescribe

### Local matching and biomedical extraction

| Resource and URL | Coverage / plain-words role | Update evidence | Licence | Backend and combine-with |
|---|---|---|---|---|
| **RapidFuzz** - `https://github.com/rapidfuzz/RapidFuzz` | Python/C++ fuzzy string matching, including edit-distance and candidate-ranking tools. Coverage is your supplied catalogue. | Latest release not established here. | **MIT**. | Local library; good first choice for brand candidates. Combine spelling similarity with strength, dosage form and manufacturer checks. [27] |
| **SymSpell** - `https://github.com/wolfgarbe/SymSpell` | Dictionary-based spelling correction; useful for generating candidates, not proving two medicines are equivalent. | Latest release not established. | **MIT**. | Local library; combine a domain-specific dictionary with a confirmation step. [26] [26] [26] [26] [26] [26] [26] [26] [26] |
| **Med7** - `https://github.com/kormilitzin/med7` | Medication NER for **drug, strength, form, route, dosage, frequency and duration**; trained in an English clinical/MIMIC context. | Repository notes **November 2024** updates. | **Apache 2.0**. | Local spaCy models, including vector and transformer options. Combine extraction with Indian brand resolution; do not assume Indian abbreviations/generalization are solved. [22] |
| **d4data biomedical-ner-all** - `https://huggingface.co/d4data/biomedical-ner-all` | DistilBERT biomedical NER; card reports **107 entity types**, **66.4M parameters**, English MACCROBAT-based training. Not a dedicated Indian prescription parser. | Latest update not established. | **Apache 2.0**. | Transformers locally or supported hosted inference. Combine with prescription-specific field validation and an Indian dictionary. [31] |
| **GLiNER small v2.1** - `https://huggingface.co/urchade/gliner_small-v2.1` | **166M-parameter** arbitrary-label extraction model; useful for trying labels such as brand, strength and frequency without a generative answer. | Exact release/update date not established. | **Apache 2.0**. | Local inference; reviewed page lists no hosted inference provider. Combine with deterministic schema validation and domain tests. [28] |
| **scispaCy** - `https://github.com/allenai/scispacy` | Biomedical/scientific NLP pipelines. Model vocabulary sizes differ; these are not prescription-safety accuracy figures. | Latest relevant update not established. | **Apache 2.0 code**; check selected model/dependencies. | Local spaCy tooling. Useful for terminology/entity processing, not dose decisions. [24] |
| **Qwen3-0.6B** - `https://huggingface.co/Qwen/Qwen3-0.6B` | Small general-language-model candidate for constrained extraction or explanations. Not a biomedical safety authority. | Exact deployed revision should be pinned; no latest-date claim here. | Check the model card and selected revision's terms before redistribution. | Local-model candidate; require structured output, evidence retrieval and deterministic checking. Never let it invent missing brand compositions. [55] [55] [55] [55] [55] [55] [55] [55] [55] [55] |

**Takeaway:** Begin with a dictionary, RapidFuzz and a structured parser. Add a model only if it improves held-out extraction without increasing dangerous false matches.

### OCR engines, a prescription model and a dataset

| Resource and URL | Coverage / role | Update evidence | Licence | Backend and combine-with |
|---|---|---|---|---|
| **Tesseract** - `https://github.com/tesseract-ocr/tesseract` | General OCR engine/CLI, **100+ languages**; not a demonstrated solution for arbitrary prescription handwriting. | Version 5 began **November 30, 2021**; this is not a claim about the latest patch. | **Apache 2.0**. | Local CLI/library. Combine image preprocessing with mandatory text confirmation. [25] |
| **PaddleOCR** - `https://github.com/PaddlePaddle/PaddleOCR` | General document/OCR toolkit; prescription performance must be evaluated separately. | Pin a tested release; latest update not established here. | **Apache 2.0**. | Local toolkit/service option; combine with layout parsing and the same confirmed-text pipeline. [30] [30] [30] [30] [30] [30] [30] [30] |
| **EasyOCR** - `https://github.com/JaidedAI/EasyOCR` | General OCR library; useful baseline, not a clinical reader. | Latest update not established. | **Apache 2.0**. | Local Python integration; combine with preprocessing and correction UI. [32] [32] [32] [32] [32] [32] [32] [32] [32] [32] [32] |
| **Medical Prescription OCR, chinmays18** - `https://huggingface.co/chinmays18/medical-prescription-ocr` | English handwritten-prescription model; approximately **0.2B parameters**. Card reports **71% character** and **84% word** accuracy; these are author-reported metrics, not clinical validation. | Model update not established; linked dataset listing shows **July 3, 2025**. | Model marked **MIT**. Dataset permissions are separate. | Local CPU/CUDA example; no hosted inference provider listed. Useful experiment only after typed-input MVP. [47] |
| **Medical Prescription Dataset, chinmays18** - `https://huggingface.co/datasets/chinmays18/medical-prescription-dataset` | **1,000 rows**: **800 train / 100 validation / 100 test**, about **984 MB**, images and structured text. Schema includes patient/doctor/clinic and medication fields. | Exact dataset update should be pinned; linked listing above reports July 3, 2025. | Dataset licence **not established**. Model MIT does not license its training/test images. Check privacy, consent and de-identification before reuse. | Downloadable dataset candidate, not production API; combine with a permission and privacy review. [48][47] |

**Takeaway:** Open OCR software is readily available; permission-cleared, representative prescription evaluation data is a different problem. The dataset's patient-field schema is a reason to examine privacy, not proof that every record contains identifiable information.

### Case study: a near-match should produce a choice, not an invented medicine

**Proposed demo:** Enter a misspelled brand that has two close catalogue candidates. RapidFuzz ranks them, but the application also displays strength, form and manufacturer. If the difference remains ambiguous, the user must select a candidate; no ingredient is silently substituted.

The same boundary should apply to Med7 or an OCR model: extraction creates a proposed structured record, not a final medication order. Med7 acknowledges errors, and the prescription OCR card explicitly limits clinical claims. [22][47] The outcome to demonstrate is **safe abstention**, not an impressive-looking guess.

## 6. Indian Evidence, Products And Hackathon Precedents

### Statistics that make the problem real without overstating it

| Evidence | Verified figure or finding | What a judge should hear | Important limit |
|---|---|---|---|
| **Indian hospital medication-error systematic review**, published 2025 | **40 studies**, **307,106 patients**; median error rate **34.11%**. | "Across the hospital studies reviewed, medication errors were substantial and variable." | Not a national population prevalence or a prediction for this prescription. Study definitions/settings differ. [2] |
| **Stages of error in that review** | Prescribing **40%** across **30** studies; administration **31%** across **28**; transcription **22%** across **19**; dispensing **11%** across **21**. | "The prescribing stage is an important intervention point, but errors occur throughout the pathway." | Different study subsets/denominators; do not add these percentages or portray them as one partition. [2] |
| **Quality of the review's included studies** | **31 moderate**, **5 low**, **4 high** quality. | "The evidence is useful, but not uniformly strong." | Quality and heterogeneity constrain precise national extrapolation. [2] |
| **CDSCO prohibited FDC lists** | **156**, dated **August 2, 2024**; **16**, dated **June 11, 2026**. | "India-specific regulatory checks matter, and the lists change." | These are counts of listed FDC prohibitions, not patient injuries, unique active ingredients or a simple count of all banned brands. [13] |
| **FDC policy commentary** | Discusses inadequate evidence, avoidable adverse effects and antimicrobial-resistance concerns surrounding irrational combinations. | "A combination pill is convenient, but each ingredient still needs justification." | Commentary is not a new national harm estimate; the cited article is dated **September 24, 2024**, not 2025 merely because of its archive context. [4] |

**Takeaway:** Use the hospital review and the official notifications as two different kinds of evidence: one describes observed errors, the other establishes regulatory status. Neither proves your software prevents harm.

**Direct official FDC documents:**

- 2024 list: `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadNewsFiles/List%20of%20Prohibited%20FDC%20drugs_%20156%20FDCs_%20dated%2002.08.2024.pdf`
- 2026 list: `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadNewsFiles/List%20of%2016%20FDCs%20banned%20dated%2011.06.2026.pdf`
- 2026 Gazette notifications: `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadGazette_NotificationsFiles/2026.06.11%20S.O.%203068(E)%20to%20S.O.%203083(E)_%20Prohibition%20of%2016%20FDCs.pdf`

For the demo, match the exact ingredients, strengths/form and notification scope. Do not generalize a specific prohibited FDC into "these two ingredients can never be used together."

### India-facing products: useful inspiration, not open-source dependencies

| Product and URL | What is supported | Update / coverage | Licence and website/backend status | Combine-with / inspiration |
|---|---|---|---|---|
| **Eka Care / developer platform** - `https://www.eka.care/` and `https://developer.eka.care/introduction` | Official developer documentation for healthcare integration and authenticated access. | Current docs reviewed; relevant medicine-catalogue size and DDI coverage not established. | Commercial/vendor platform; no open-source grant inferred. Documented authentication uses client credentials/tokens. | Integration and consent/workflow inspiration. A drug-interaction API was **not verified** from the reviewed introduction. [45] |
| **HealthPlix** - `https://www.healthplix.com/` | Indian EMR product; useful clinician-workflow reference. | Relevant DDI/dose coverage and update date not established here. | Product website; no forkable source or public safety API licence established. | Learn prescription-entry and clinician-workflow patterns, not a claim of independently verified safety performance. [60] [60] [60] [60] [60] [60] [60] [60] |
| **ThePrescription** - `https://theprescription.in/` | Site markets an AI handwriting reader and claims medicine/salt and schedule interpretation. | Exact update, catalogue size and clinical accuracy not established. | Website product; public code, API and reusable licence not established. | Compare correction/confirmation UX. Treat the advertised capabilities as vendor claims. [56] |

**Takeaway:** These products show plausible workflows and integration needs. Their websites do not establish that their underlying medicine knowledge can be exported or merged into a hackathon app.

### Hackathon claims and discovery gaps

A verified adjacent precedent is **Peel**, covered by RIT as a HackMIT-winning low-cost medicine-testing device. It concerns physical medicine testing, not a reusable Indian prescription interaction engine. Its value is the clear demonstration of a concrete medication problem; it is not evidence that the present software problem has already been solved. [59] [59] [59] [59] [59] [59]

For the prescription-safety niche repositories above, a hackathon mention or a Devpost-style project page is not, by itself, a verified win. **No directly matching, licence-cleared prescription-safety winner is asserted here.** Likewise, no relevant, licence-cleared Gitee implementation was established; that is a discovery gap, not a claim that Gitee has none.

### Case study: regulatory currency and product polish solve different problems

CDSCO's 2026 FDC list supplies a concrete regulatory event. An India-facing EMR supplies a model for fitting alerts into prescribing workflow. Neither alone produces an ingredient-normalized, patient-specific checker. [13][45]

**Recommended demo decision:** Use one exact, source-linked regulatory example and a clinician-style review screen. Show the notification and the affected formulation, then offer confirmation/escalation rather than silently deleting a medicine. This makes the local relevance understandable without pretending the app is a regulator or prescriber.

## 7. A Demonstrable Architecture That Reduces Alert Fatigue

The following architecture and priorities are **recommendations**, not measured performance claims.

| Layer | Recommended implementation | Evidence and failure handling |
|---|---|---|
| **1. Input and consent** | Typed prescription, patient context, explicit demo/synthetic mode. Keep upload/OCR optional. | Avoid exposing identifiable prescriptions to external services by default. |
| **2. Structured parsing** | Extract brand, form, strength, units, route, frequency, duration and SOS maximum. Start deterministic; evaluate Med7/GLiNER if needed. | Retain original text and highlight unresolved fields. |
| **3. Brand resolution** | Exact normalized lookup -> fuzzy candidates -> human confirmation. | Never auto-accept solely on a similarity score; retain catalogue version and source. |
| **4. Ingredient expansion** | Store an array of canonical ingredients, amounts and denominators. Preserve salts, release form and route. | Incomplete composition prevents an all-clear result. |
| **5. Independent checks** | Duplicate ingredient; reviewed dose rules; licensed interactions; exact FDC notification rules. | Each check has its own assessed/unassessed state. |
| **6. Alert aggregation** | Group all warnings about the same underlying exposure; rank by seriousness, evidence and actionability. | Do not show an LLM paragraph as a new independent clinical finding. |
| **7. Explanation and audit** | Plain-language reason, arithmetic, source, uncertainty, next action and clinician override reason. | Store input/version/rule trace; distinguish "no finding" from "not checked." |

**Takeaway:** A clear evidence boundary is more valuable than a larger pile of alerts. Each layer should fail visibly and locally, rather than converting missing information into reassurance.

### Case study: one duplicate-exposure finding instead of four repetitive warnings

**Proposed scenario:** Two products contribute the same ingredient. A naive app might produce a brand-duplication warning, an ingredient warning, a dose warning and an AI-generated caution as four equal pop-ups. A better interface groups them into one exposure card showing both products, the summed amount, the applicable patient rule and any missing context.

This design addresses **alert fatigue**, a recognized clinical-decision-support problem described by AHRQ. It is a rationale for prioritization, not proof that the proposed interface reduces errors. [39] [39] [39] [39] [39] [39] [39] Measure the demo's alert count, false-positive burden, unresolved matches and whether users understand the required action before claiming improvement.

Use a three-part presentation: **requires immediate review**, **needs clarification**, and **information/monitoring**. Reserve blocking behavior for a narrow, clinically reviewed set of high-consequence situations; do not make every possible research association a hard stop.

### Ten questions a non-expert judge will ask

| # | "What if...?" | How the demo answers it |
|---|---|---|
| **1** | **Two different brands both contain paracetamol?** | Expand both into ingredients, group the duplicate and show the summed daily exposure. Explain separately whether a dose rule applies or remains unassessed. |
| **2** | **The doctor misspells a brand?** | Show ranked candidates with strength/form/manufacturer. An ambiguous case asks for confirmation; it never silently substitutes a medicine. |
| **3** | **One tablet contains three or more drugs?** | Display every ingredient in an array. A record with only two composition fields is not accepted as complete without support. |
| **4** | **The prescription says OD, BD, TDS or SOS?** | Show the interpreted schedule before calculation. SOS requires a maximum; otherwise show "maximum daily dose cannot be assessed." |
| **5** | **The patient is a child?** | Request age and weight with units. Show whether the selected rule is per dose or per day; missing data produces an unassessed result, not an adult default. |
| **6** | **The patient has kidney disease?** | Ask for the measure required by the selected rule and its units. Without an applicable, reviewed renal rule, state the limitation and request clinician review. |
| **7** | **It is a syrup, half tablet, injection or modified-release medicine?** | Show unit conversions and formulation/route explicitly. Do not equate mg/5 mL with mg/mL or substitute release forms automatically. |
| **8** | **The combination is prohibited in India?** | Match against the exact reviewed CDSCO notification, show the date/document and explain the formulation-specific finding. |
| **9** | **The doctor gets too many alerts?** | Present one grouped issue per underlying hazard, with severity, evidence and a concrete action. Keep secondary explanations expandable. |
| **10** | **The internet fails, the brand is unknown or the AI makes something up?** | Run catalogue/arithmetic locally where possible; show unavailable checks; refuse unsupported compositions. Explanations must point to stored records and rules, not invented citations. |

**Takeaway:** Each answer should be a visible interaction in the demo, including a failure/abstention case. An honest "cannot assess until weight is entered" is a stronger safety feature than a universal green checkmark.

## 8. Synthesis: The Best Merge Is A Layered System

| Strategy/resource class | Mechanism | Scope / evidence | Main trade-off | Refresh and implementation decision |
|---|---|---|---|---|
| **Indian scraped catalogues** | Resolve commercial names to product compositions. | Broad local product coverage; uploader counts and incomplete provenance. | Breadth versus rights, missing values and incomplete FDC representation. | Version and audit selected records; choose one primary catalogue rather than assuming overlapping mirrors corroborate one another. [21][3][43] |
| **RxNorm/RxNav** | Normalize terminology and identifiers. | Terminology services, not current DDI coverage. | Standardization without complete Indian brand coverage. | Use as a bridge after local brand resolution; never call its retired DDI path. [14] |
| **DDInter / licensed clinical datasets** | Curated pairwise interaction evidence. | Directly relevant interaction content. | Better clinical fit versus licensing/API uncertainty and refresh requirements. | Obtain permission or an appropriate product; pin the exact dataset/version. [6][11] |
| **Labels / ICMR / FDA** | Conditional clinical guidance. | Source-backed dose and patient-context evidence, not a ready-made universal rule engine. | Authority versus manual translation and exceptions. | Implement a narrow reviewed rule set, retaining source and eligibility. [46][57] |
| **TWOSIDES / SIDER / Hetionet** | Associations, side effects and graph relationships. | Useful research context; not equivalent to prescribing rules. | Discovery breadth versus actionability, age and upstream terms. | Keep out of hard-stop logic unless independently reviewed and justified. [16][5][9] |
| **NER / fuzzy matching / OCR** | Convert uncertain input into candidate structured records. | Extraction tools and author-reported model performance. | Convenience versus silent substitution or transcription errors. | Require confirmation and measure errors separately from rule-engine accuracy. [22][47] |

**Takeaway:** These layers differ in mechanism, coverage, evidentiary authority, licensing burden and refresh horizon. Combining them is useful only if those differences remain visible.

Three tensions determine the build. **First, catalogue size is not clinical completeness:** a massive CSV can omit a third ingredient. **Second, official terminology is not clinical advice:** RxNav can correctly identify a drug while providing no current interaction service. **Third, a persuasive AI explanation is not evidence:** it can improve readability only after the underlying record and rule exist.

**Recommended hackathon stack:** fork the MIT RxCheck shell or build a thin typed-input web app; use a permission-cleared, explicitly bounded Indian catalogue; add RapidFuzz with confirmation; implement deterministic duplicate exposure and a small reviewed dose-rule set; add interaction evidence only under usable terms; link exact CDSCO notifications; keep OCR and generative explanations optional. Evaluate unresolved matches, composition completeness, arithmetic, missed findings and alert burden separately.

The strongest claim to make is **"we make a prescription's ingredients, assumptions and safety checks visible."** Do not claim nationwide coverage, contamination-free data, regulatory approval or demonstrated prevention of medication harm without the corresponding evidence.

## References

1. *GitHub - thanmai-mathi/drug-safety-checker*. https://github.com/thanmai-mathi/drug-safety-checker
2. *Epidemiology of Medication Errors in Indian Hospital Settings*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12683552
3. *1mg 117k medicine complete data with image link - Kaggle*. https://www.kaggle.com/datasets/abhay13072009/1mg-117k-medicine-complete-data-with-image-link
4. *Navigating the Impact of India's Recent Ban on Fixed-Dose ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11970505
5. *SIDER Side Effect Resource*. http://sideeffects.embl.de/
6. *DDInter 2.0*. https://ddinter2.scbdd.com/
7. *RxNorm API - APIs*. https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html
8. *GitHub - VidhyaES/drug-interaction-detector-nlp: NLP-based real-time drug interaction checker using BioClinicalBERT NER, vector search & knowledge base queries. Built with safety warnings for hospital use cases.*. https://github.com/VidhyaES/drug-interaction-detector-nlp
9. *GitHub - hetio/hetionet: Hetionet: an integrative network of disease · GitHub*. https://github.com/hetio/hetionet
10. [
      
        DDinter
      
    ](https://ddinter.scbdd.com/download/)
11. *DrugBank Release Version 5.1.22*. https://go.drugbank.com/releases/latest#open-data
12. [
	Pharmaceuticals & Medical Devices Bureau of India
](https://www.pmbi.co.in/ProductList.aspx)
13. *FDC*. https://cdsco.gov.in/opencms/opencms/en/Drugs/FDC
14. *RxNav - LHNCBC*. https://lhncbc.nlm.nih.gov/RxNav/
15. *GitHub - gitzaan/Drug-Interaction-Checking-Website: Built a Next.js-based website that allows users to check potential drug interactions, integrating MongoDB and Python for efficient data management and interaction results.*. https://github.com/gitzaan/Drug-Interaction-Checking-Website
16. *Tatonetti Lab at Columbia University Medical Center*. https://tatonettilab.org/resources/tatonetti-stm.html
17. *drug-database · GitHub Topics · GitHub*. https://github.com/topics/drug-database
18. *Indian Medicine Data*. https://www.kaggle.com/datasets/mohneesh7/indian-medicine-data
19. *GitHub - The-MedOps/medicine-dataset · GitHub*. https://github.com/The-MedOps/medicine-dataset
20. *250k Medicines Usage, Side Effects and Substitutes*. https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes
21. *A-Z Medicine Dataset of India*. https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india/data
22. *GitHub - kormilitzin/med7 · GitHub*. https://github.com/kormilitzin/med7
23. *DailyMed - Web Services*. https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm
24. *GitHub - allenai/scispacy: A full spaCy pipeline and models for scientific/biomedical documents. · GitHub*. https://github.com/allenai/scispacy
25. *GitHub - tesseract-ocr/tesseract: Tesseract Open Source OCR Engine (main repository) · GitHub*. https://github.com/tesseract-ocr/tesseract
26. *GitHub - wolfgarbe/SymSpell: SymSpell: 1 million times faster spelling correction & fuzzy search through Symmetric Delete spelling correction algorithm · GitHub*. https://github.com/wolfgarbe/SymSpell
27. *GitHub - rapidfuzz/RapidFuzz: Rapid fuzzy string matching in Python using various string metrics · GitHub*. https://github.com/rapidfuzz/RapidFuzz
28. *urchade/gliner_small-v2.1 · Hugging Face*. https://huggingface.co/urchade/gliner_small-v2.1
29. *open.fda.gov*. https://open.fda.gov/terms/
30. *GitHub - PaddlePaddle/PaddleOCR: Turn any PDF or image document into structured data for your AI. A powerful, lightweight OCR toolkit that bridges the gap between images/PDFs and LLMs. Supports 100+ languages. · GitHub*. https://github.com/PaddlePaddle/PaddleOCR
31. *d4data/biomedical-ner-all · Hugging Face*. https://huggingface.co/d4data/biomedical-ner-all
32. *GitHub - JaidedAI/EasyOCR: Ready-to-use OCR with 80+ supported languages and all popular writing scripts including Latin, Chinese, Arabic, Devanagari, Cyrillic and etc. · GitHub*. https://github.com/JaidedAI/EasyOCR
33. *openFDA*. https://open.fda.gov/apis/drug/label/
34. *GitHub - PKhetan0208/Pharmeasy-AI-assisted-Prescription-Flow: An OCR-to-cart prescription parser and drug safety assistant that extracts medicine dosages, advises generic substitutes, and activates smart healthcare reminders · GitHub*. https://github.com/PKhetan0208/Pharmeasy-AI-assisted-Prescription-Flow
35. *Acetaminophen | FDA*. https://www.fda.gov/drugs/safe-use-over-counter-pain-relievers-and-fever-reducers/acetaminophen
36. *DDInter 2.0: an enhanced drug interaction resource with expanded data coverage, new interaction types, and improved user interface | Nucleic Acids Research | Oxford Academic*. https://academic.oup.com/nar/article/53/D1/D1356/7740584
37. *GitHub - nowitsidb/INDIAN_MEDICINE_MCP_SERVER: A comprehensive API server for medicine information lookup, alternative suggestions, and composition analysis. This server provides multiple endpoints for searching, filtering, and analyzing medicine data with advanced features like fuzzy matching and price comparison. · GitHub*. https://github.com/nowitsidb/INDIAN_MEDICINE_MCP_SERVER
38. *GitHub - indiser/Rxcheck: 💊 Clinical drug interaction checker with automated FDA data ingestion | PostgreSQL + openFDA ETL | Multi-provider LLM router | Prescription OCR | Indian generic alternatives | PMBJP pricing | Fault-tolerant checkpointing | Server-side security | Privacy-first | No signup required · GitHub*. https://github.com/indiser/Rxcheck
39. *Alert Fatigue | PSNet*. https://psnet.ahrq.gov/primer/alert-fatigue
40. *GitHub - narender-rk10/1mg-drugs-medicine-scrapper · GitHub*. https://github.com/narender-rk10/1mg-drugs-medicine-scrapper
41. *Indian Pharmaceutical Products*. https://www.kaggle.com/datasets/rishgeeky/indian-pharmaceutical-products
42. *Extensive A-Z Medicines Dataset of India*. https://www.kaggle.com/datasets/riturajsingh2004/extensive-a-z-medicines-dataset-of-india
43. *India Medicines and Drug Info Dataset*. https://www.kaggle.com/datasets/apkaayush/india-medicines-and-drug-info-dataset
44. *Medicines Dataset*. https://www.kaggle.com/datasets/ujjwalgupta23/medicines-dataset
45. *Overview*. https://developer.eka.care/introduction
46. *Standard Treatment Workflows (STWs) | Indian Council of Medical Research | Government of India*. https://www.icmr.gov.in/standard-treatment-workflows-stws
47. *chinmays18/medical-prescription-ocr · Hugging Face*. https://huggingface.co/chinmays18/medical-prescription-ocr
48. *chinmays18/medical-prescription-dataset · Datasets at Hugging Face*. https://huggingface.co/datasets/chinmays18/medical-prescription-dataset
49. *GitHub - Sanjay00013/Netmeds_End_to_End_Data_Analysis_Project: This project involves web scraping drug data from RxList and Netmeds, building a model to classify drugs, and analyzing trends. An Excel dashboard visualizes insights, while SQL queries extract patterns. Finally, EDA is performed, followed by a predictive model to estimate drug prices, integrating data science techniques for pharmaceutical analysis · GitHub*. https://github.com/Sanjay00013/Netmeds_End_to_End_Data_Analysis_Project
50. *GitHub - sumankrsh/medicine-drug-advisor: AI-powered medicine database and drug interaction checker with Indian medicines and mental health focus · GitHub*. https://github.com/sumankrsh/medicine-drug-advisor
51. *GitHub - Supriyochow/Web-Scraping-of-netmeds-website-using-BeautifulSoup · GitHub*. https://github.com/Supriyochow/Web-Scraping-of-netmeds-website-using-BeautifulSoup
52. *GitHub - ziigzag/vitatheca-data: Open data packs for Vitatheca — offline reference for foods and medications. Aggregated SQLite databases from USDA, EFSA, EMA, openFDA, WHO, DrugBank, RxNorm. · GitHub*. https://github.com/ziigzag/vitatheca-data
53. *GitHub - openemr/openemr: The most popular open source electronic health records and medical practice management solution. · GitHub*. https://github.com/openemr/openemr
54. *Drug Central*. https://drugcentral.org/
55. *Qwen/Qwen3-0.6B · Hugging Face*. https://huggingface.co/Qwen/Qwen3-0.6B
56. *AI Doctor Prescription Reader Online - Read Doctor Handwriting | Theprescription*. https://theprescription.in/
57. *HYPERTENSION IN ADULTS_Final*. https://www.icmr.gov.in/icmrobject/uploads/STWs/1778941063_hypertensioninadults_final.pdf
58. *Eka Care: AI-Native Health OS | EMR, EHR & ABDM Platform*. https://www.eka.care/
59. *RIT student wins HackMIT with low-cost medicine testing device | RIT*. https://www.rit.edu/news/rit-student-wins-hackmit-low-cost-medicine-testing-device
60. *Best EMR Software in India | HealthPlix - AI-Powered Digital Clinic*. https://www.healthplix.com/
61. *S. No. Drugs Name Notification No. & Date 1. Acetyl Salicylic acid + Ethoheptazine S.O. 3068(E) dated 11.06.2026 2. Aloe*. https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadNewsFiles/List%20of%2016%20FDCs%20banned%20dated%2011.06.2026.pdf
62. *S. No. Drugs Name Notification No. & Date 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12.*. https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadNewsFiles/List%20of%20Prohibited%20FDC%20drugs_%20156%20FDCs_%20dated%2002.08.2024.pdf
63. *का.आ. 3068(अ).—*. https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadGazette_NotificationsFiles/2026.06.11%20S.O.%203068(E)%20to%20S.O.%203083(E)_%20Prohibition%20of%2016%20FDCs.pdf
