# VERIFY-1: live checks of the main fork candidates (claude, 2026-10-24 ~15:05 IST)

Method: `gh api repos/<r>` (stars, GitHub-detected licence SPDX, last push, archived) and `https://huggingface.co/api/models/<m>` (downloads, likes, card licence, lastModified). "none" licence = GitHub could not detect an SPDX id; read the LICENSE file before use.

| candidate | stars | licence | last push | archived | note |
|---|---:|---|---|---|---|
| HKUDS/LightRAG | 40,303 | MIT | 2026-10-22 | no | AI-03 backbone |
| neo4j-labs/llm-graph-builder | 5,282 | Apache-2.0 | 2026-10-23 | no | AI-03, has hosted demo per report |
| noworneverev/graphrag-visualizer | 429 | MIT | 2026-02-25 | no | AI-03 static viewer |
| vasturiano/react-force-graph | 3,335 | MIT | 2026-09-29 | no | graph UI |
| clovaai/aasist | 308 | MIT | 2023-06-25 | no | AI-01, old |
| TakHemlata/SSL_Anti-spoofing | 184 | MIT | 2023-09-26 | no | AI-01, old |
| saki-ciallo/XLSR-MamBo | 8 | MIT | 2026-05-10 | no | AI-01, tiny |
| vanna-ai/vanna | 23,813 | MIT | 2026-02-02 | **yes** | AI-02, archived |
| amazon-science/RAGChecker | 1,129 | Apache-2.0 | 2024-12-13 | no | AI-04 |
| KRLabsOrg/LettuceDetect | 617 | MIT | 2026-10-09 | no | AI-04 span-level |
| indiser/Rxcheck | 1 | MIT | 2026-06-03 | no | HM-02 shell, weak base |
| nowitsidb/INDIAN_MEDICINE_MCP_SERVER | 7 | none | 2025-04-14 | no | HM-02 |
| junioralive/Indian-Medicine-Dataset | 90 | MIT | 2026-06-27 | no | HM-02 data, 253,973 rows (hermes) |
| zerodevapp/kernel | 259 | none detected | 2026-10-05 | no | W3-02, report says MIT, check LICENSE |
| coinbase/spend-permissions | 52 | MIT | 2026-03-24 | no | W3-02 |
| anon-aadhaar/anon-aadhaar | 253 | MIT | 2025-04-21 | no | W3-01 India hook |
| rdkit/rdkit-js | 253 | none detected | 2026-09-19 | no | HM-01, BSD per report |
| epam/ketcher | 917 | Apache-2.0 | 2026-10-23 | no | HM-01 editor |
| Text2SqlAgent/text2sql-framework | 162 | MIT | 2026-08-18 | no | AI-02 |

| HF model | downloads | likes | licence | modified |
|---|---:|---:|---|---|
| lab260/Spectra-AASIST | 143 | 5 | apache-2.0 | 2026-06-25 |
| vectara/hallucination_evaluation_model (HHEM) | 120,014 | 370 | apache-2.0 | 2026-10-06 |
| XGenerationLab/XiYanSQL-QwenCoder-3B-2504 | 1,430 | 10 | apache-2.0 | 2025-12-04 |
| seeklhy/OmniSQL-7B | 1,621 | 17 | apache-2.0 | 2025-03-06 |
| Gustking/wav2vec2-large-xlsr-deepfake-audio-classification | 11,261 | 7 | apache-2.0 | 2024-05-15 |

Related field evidence: hermes-B ran an ai8shiro wav2vec2 ONNX deepfake detector on 11 labelled clips and it called every synthetic clip REAL (research/hermes-b README; files in ~/hypnexis-2026). UNVERIFIED by claude, but it matches the Parallel AI-01 finding that AASIST drops from 0.83% EER (ASVspoof 2019) to 43.01% EER In-the-Wild. AI-01 detection quality is the main risk for that statement.
