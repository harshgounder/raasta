# HM-02 evidence, and a correction about code and model runs

Written by hermes 2026-10-24 14:50 IST, at claude's request, after a "STOP BUILDING" notice.

## 1. Correction first, because it matters more than the evidence

I have written no code in this round, and I ran no model. Specifically:

- No resolver and no rule engine exist from me. Nothing of the kind is in my lane folder, and a find for
  `*.py`, `*.js`, `*.ts`, `*.sh`, `*.ipynb` and `*.onnx` under `~/hypnexis-main/research/hermes/` returns
  zero files (checked 2026-10-24T14:48:32).
- I did not run the AI-01 ONNX test mentioned in the lead's notice, so I have no model ids, no clip
  source and no result to hand over. Those are not mine to describe, and if they exist they came from
  another agent or another lane. Please attribute that result where it actually came from; I will not
  invent a provenance for it.
- Every file I wrote this round is research text: the eight statement files, `JUDGE-LENS.md`,
  `WOW-SCAN.md`, `VERIFY-LOG.md`, `unstop/UNSTOP-FACTS.md`, and this file. Nothing executable.
- The rule in FLEET-BRIEF section 3 is already how I have been operating all session: research, fact-check,
  critique, writing. Shell commands only for reading, fetching and measuring.

If the lead saw code attributed to hermes, the attribution is wrong. If it wants it dealt with, the paths
in the notice would need to be named so they can be identified, and I would still not edit them.

## 2. HM-02 evidence that I can stand behind

### 2.1 Indian Medicine Dataset, verified today by me

Repository: https://github.com/junioralive/Indian-Medicine-Dataset
Checked 2026-10-24T14:48 IST, via `gh api repos/junioralive/Indian-Medicine-Dataset`, which asks GitHub
directly rather than reading a cached page:

```
{"desc":"A curated dataset of Indian medicines, organized by brand. Essential for healthcare research
and pharmaceutical analysis.","full_name":"junioralive/Indian-Medicine-Dataset","license":"MIT",
"pushed":"2026-06-27T05:00:43Z","size_kb":24744,"stars":90}
```

README, fetched the same minute, verbatim:

```
`TOTAL MEDICINES` `253973`
```

and the field list, verbatim: `id`, `name`, `price(₹)`, `Is_discontinued`, `manufacturer_name`, `type`,
`pack_size_label`, `short_composition1`, `short_composition2`.

Data file: `DATA/indian_medicine_data.csv` (CSV and JSON both described in the README).
So: MIT licence, 253,973 rows, pushed 2026-06-27, 90 stars, 24.7 MB repo, brand to composition map with a
discontinued flag and rupee price.

One honesty note: the README's own example row is `Augmentin 625 Duo Tablet`, and the dataset's provenance
is a scrape of an Indian pharmacy site rather than a regulator export. For a pitch that means it is an
excellent starting map and it is not authoritative. Spot checks against CDSCO or NPPA are what make it
credible, and that is a build-time task, not a research one.

### 2.2 The other verified rows in `HM-02.md`

Three rows in that file carry VERIFIED status because the pages were opened this session. The dataset
above is one. The other two, with what they are for:

- Parchi, https://devpost.com/software/parchi-prescription-intelligence-for-indian-clinics. An Indian
  prescription checker that already names the data sources (ICMR AMRSN split by OPD, ward and ICU, CDSCO
  banned FDCs, NPPA, Jan Aushadhi) and frames a drug price in days of household income. This is the
  closest existing project to HM-02 and it is invisible to code search.
- DDInter 2.0, https://ddinter2.scbdd.com/. Open drug-drug interaction database, 302,516 interactions
  across 2,290 drugs with severity and mechanism, which is the interaction layer HM-02 would otherwise
  have to build.

Also verified in the same file, all opened this session: CDSCO, NPPA IPDMS 2.0, the Jan Aushadhi product
and MRP list, and two Kaggle India medicine datasets.

### 2.3 What is NOT yet verified for HM-02

- Whether the DDInter licence permits redistribution inside a product. The site states the database is
  open for research; commercial redistribution terms were not read.
- Whether an Indian brand name in the dataset resolves reliably to a generic, which is the hard part of
  the statement. No measurement has been done.
- The pharmacist dependency in the statement itself (test set needs a pharmacist or pharmacy student).
  That is a people question for the user, which the lead is already escalating.

## 3. Status

Standing by on L2 and L3 only. No code, no model runs, no deploy. If the lead wants deeper HM-02 evidence
(a licence read on DDInter, or a spot check of 20 dataset rows against a public source), that is research
and I will do it when asked.
