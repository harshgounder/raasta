# Wave 1 summary (dsh L1), 2026-10-24 15:20 IST

Source: Parallel TaskGroup pro `tgrp_85133678a4ff429386c65a9af82acad2`, 8/8 completed.
Raw: `wave1/raw.md`. Per statement: `wave1/<ID>.md`.

| id | fork candidates | weights | datasets | regional sources checked | note |
|---|---:|---:|---:|---:|---|
| AI-01 | 2 | 3 | 2 | 1 | AASIST (MIT, 308 stars), SSL_Anti-spoofing (184). CPU guard must be patched. |
| AI-02 | 3 | 3 | 2 | 1 | Vanna, DB-GPT, XiYanSQL-7B (BIRD dev 62.13% standalone). |
| AI-03 | 4 | 2 | 2 | 2 | LightRAG (39,144 stars, MIT, webui), Neo4j builder, RAGFlow, GraphRAG. |
| AI-04 | 4 | 2 | 2 | 2 | Ragas (16k), EvalScope, RAGChecker, Giskard. |
| W3-01 | 4 | 0 | 2 | 0 | StellarCred (30), galactica, noir-examples, Privado. |
| W3-02 | 3 | 1 | 2 | 1 | Kernel (ZeroDev), Smart Sessions (Rhinestone), Alchemy V2. |
| HM-01 | 3 | 0 | 2 | 0 | RDKit.js (browser WASM, 248), ChEMBL pipeline, datamol. |
| HM-02 | 4 | 1 | 2 | 1 | INDIAN_MEDICINE_MCP_SERVER, MedRecon, Tesseract.js, cql-execution. |

Honest gaps: candidates are 2 to 4 per statement, almost all GitHub, regional coverage 0 to 2 hosts
per statement. This is a starting point, not the wide sweep the user asked for. Wave 2 (4 statements,
pro, `tgrp_97b6f4364c21489887102bef073793c0`) demands 12 candidates, competition winners, regional
finds with exact queries, combos and judge what-ifs. Wave 3 fills any zero-hit host for the shortlist.

## Provisional ranking under the pre-registered rubric (before wave 2)

| id | fork | demo | legibility | novelty | evidence | risk | story | total /21 | reason |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| AI-03 | 3 | 2 | 3 | 2 | 2 | 2 | 3 | 17 | LightRAG is forkable today, the graph is the visual hero, no benchmark gate |
| AI-01 | 2 | 3 | 3 | 2 | 2 | 1 | 3 | 16 | most emotional demo, CPU patch and dataset licence are the risks |
| AI-02 | 3 | 2 | 3 | 2 | 3 | 1 | 2 | 16 | best evidence (BIRD), worst compute risk on a 7 GB CPU box |
| W3-02 | 2 | 2 | 3 | 3 | 1 | 1 | 3 | 15 | strongest story (an AI card that cannot overspend), chain setup risk |
| HM-02 | 2 | 2 | 3 | 2 | 1 | 0 | 2 | 12 | relatable, but a pharmacist-authored test set is a hard gate |
| AI-04 | 2 | 2 | 2 | 1 | 3 | 3 | 1 | 14 | safe to build, weakest wow |
| W3-01 | 2 | 1 | 2 | 3 | 1 | 1 | 2 | 12 | ZK is magic but browser proving is risky tonight |
| HM-01 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | RDKit.js in browser is neat, narrow audience |

Scores are provisional and will be re-scored after wave 2. The three to watch: AI-03, AI-01, AI-02.
