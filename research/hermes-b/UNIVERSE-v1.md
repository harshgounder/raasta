# UNIVERSE v1: where a candidate project can exist, and how to reach it
Hypnexis 2026, hermes, 2026-10-24. Scope: every place a near-solution could already exist, global and regional, with an access route per platform and a query per problem statement. Nothing is "covered" until a query ran and the result, including zero results, is written in the ledger.

Rule that killed the last list: a platform with no query is not coverage. A query with no recorded result is not coverage. "Top GitHub repos" is not coverage.

## 0. Platforms and their access routes

Legend for route: API = documented programmatic endpoint; DUMP = bulk download; RSS = feed; SEARCH = only reachable through a search engine; BROWSER = needs a real browser session; LOGIN = account required, user's own account only.

### 1. Code forges, global
| platform | route | notes |
|---|---|---|
| github.com | API + code search + GraphQL | repo search, code search, topics, awesome lists, forks, issues |
| gitlab.com | API | public projects API, code search on paid tier only |
| bitbucket.org | API | weak search, use SEARCH |
| sourceforge.net | SEARCH + API | old but hosts real scientific code |
| codeberg.org (Forgejo) | API | EU, privacy projects |
| gitea.com + public Gitea instances | API per instance | instance list via gitea-instances |
| notabug.org, gitdab, git.disroot.org | BROWSER/API | small but real |
| radicle.xyz | CLI/seed nodes | p2p forge, rare gems |
| launchpad.net | API | Ubuntu-era scientific code |
| salsa.debian.org, framagit.org | API | research code upstreams |
| savannah.gnu.org, savannah.nongnu.org | SEARCH | GNU/non-GNU classics |
| softwareheritage.org | API + graph | archive of all of the above, by origin URL |
| azure devops public projects | API | enterprise code |
| archive: Google Code, CodePlex | Internet Archive | dead projects that still get forked |

### 2. Code forges, China (the ones a GitHub-only sweep misses)
| platform | route | notes |
|---|---|---|
| gitee.com | API + SEARCH | largest Chinese forge, mirrors of HF/GitHub projects |
| gitcode.com (CSDN) | SEARCH | active mirror host, many model repos |
| oschina.net / git.oschina.net | SEARCH | older Chinese OSS |
| coding.net | API | Tencent-adjacent |
| gitlab.cn (JiHu) | API | GitLab China |
| codearts (Huawei Cloud) | BROWSER | enterprise, some public |
| codeup (Alibaba Cloud) | BROWSER | enterprise, some public |
| PaddlePaddle/PaddleSpeech, ModelScope code | API | model repos with training code |
| CSDN, Juejin, Zhihu, V2EX, Bilibili | SEARCH | blog posts carry repo links that never reach GitHub |
| WeChat public accounts (mp.weixin.qq.com) | SEARCH | tutorials with code |

### 3. Code forges, other regions
| platform | region | route |
|---|---|---|
| gitflic.ru, gitverse.ru | Russia | API/SEARCH |
| habr.com | Russia | SEARCH, articles with repos |
| qiita.com, zenn.dev, note.com | Japan | SEARCH |
| naver.com blogs, velog.io, tistory.com, brunch.co.kr | Korea | SEARCH |
| 5ch.net, hatena.ne.jp | Japan | SEARCH |
| khoj.dev? no. skip | | |

### 4. Model, dataset and demo hosts
| platform | route | what it holds |
|---|---|---|
| huggingface.co | API | models, datasets, Spaces (working demos), discussions |
| modelscope.cn | API | Chinese models and datasets, many with weights not on HF |
| openi.pcl.ac.cn | API | Chinese open model hub |
| wisemodel.cn | SEARCH | Chinese model hub |
| replicate.com | API | hosted demos plus open weights links |
| civitai.com | API | image models, LoRAs, workflow metadata |
| kaggle.com | API | datasets, notebooks, competitions, public solutions |
| openml.org, uci.edu ml repo | API | classic datasets |
| zenodo.org, figshare, osf.io | API | research artifacts with code |
| paperswithcode.com | API | code+dataset links per benchmark |
| arxiv.org, openreview.net, semantic scholar, openalex | API | method sources |
| aihub, india datasets (see 9) | | |

### 5. Hackathon and project showcases (where near-identical projects already won)
Devpost, Unstop, Devfolio, HackerEarth, MLH, lablab.ai, Dev.to challenge tags, Gitcoin, ETHGlobal, DoraHacks, TAIKAI, AIcrowd, Zindi, DrivenData, Bitgrit, Kaggle competitions, Reskilll, TechGig, HackerRank contests, Hack Club, Major League Hacking archives, college fest archives (IITs, NITs, MUJ), GitHub topic `hackathon-project`.

### 6. Product and startup surfaces
Product Hunt, YC directory, Launch HN, IndieHackers, BetaList, Uneed, Peerlist, MicroLaunch, SaaSHub, AlternativeTo, G2, Capterra, Crunchbase, Tracxn, Wellfound, F6S, PitchBook (paywalled), company changelogs and pricing pages. The point is not the pitch, it is the screenshots, pricing and feature lists that show what users already expect.

### 7. Socials and communities, global
Reddit (per-sub, not sitewide), X, Hacker News (Algolia API), Lobsters, Mastodon/fediverse, Bluesky, Threads, LinkedIn, YouTube (demos), TikTok, Instagram, Twitch, Discord (public servers via disboard/top.gg), Slack communities, Telegram channels, Stack Exchange network (per-site API), Quora, Medium, Substack, Dev.to, Hashnode.

### 8. Socials and communities, regional
Zhihu, Juejin, CSDN, V2EX, Weibo, Xiaohongshu, Douyin, Bilibili, Habr, VK, Odnoklassniki, Qiita, Zenn, Note, Naver Cafe, Kakao, Brunch, Velog, Tistory, 5ch, Hatena, Line OpenChat.

### 9. India-specific, because two of the live problem statements are India-shaped
data.gov.in, Bhuvan (ISRO), ISRO catalogues, CDSCO (drug approvals), NPPA (price control), ICMR, DGHS, ABDM/NDHM sandbox, Ayushman Bharat, UIDAI, DigiLocker, NPCI, ONDC, RBI, SEBI, TRAI, NDEM, MyGov, Startup India, GeM, Indian Kanoon (legal), eGazette, OpenCity, IndiaDataPortal, Census 2011, NFHS-5, PLFS.
Drug reference for HM-02: openFDA, RxNorm, DrugBank (licence), PubChem, ChEMBL, WHO ATC, CDSCO brand lists, Jan Aushadhi list, pharma company product pages, MedPlus/1mg/Netmeds/PharmEasy catalogues (respect robots, browser-only).

### 10. Search engines and code search engines (the actual discovery instruments)
GitHub code search, grep.app, Sourcegraph public search, searchcode.com, PublicWWW, Debian codesearch, Google dorks (site:specific), Bing, Brave, Yandex (RU/global), Baidu (CN), Naver (KR), Seznam (CZ), Ecosia, Mojeek, Marginalia, Common Crawl index, Tranco top sites, Internet Archive full-text, archive.today, Software Heritage.

### 11. Patents and standards (for "has someone already solved this properly")
Google Patents, USPTO, EPO, WIPO, CNIPA, Indian Patent Office, Lens.org, IETF RFCs, W3C, ISO, NIST, IEEE.

### 12. MCP/tool ecosystem (route to live data without keys)
MCP registries (modelcontextprotocol servers, smithery, mcp.so, glama), Parallel.ai, TinyFish, Browser Use, Firecrawl (dead here), Apify, SerpAPI, Exa, Tavily, Brave Search API, Oxylabs, Bright Data, ScraperAPI. Check licence and cost before assuming a route.

## 1. Query matrix per problem statement

Every PS gets the same shape: 4 query families x the platform tiers above.
- Q1 "existing implementation": repo/code queries per platform.
- Q2 "product exists": product/startup surfaces.
- Q3 "someone already failed": issues, Reddit/HN threads, post-mortems, "why X does not work".
- Q4 "data/weights exist": model and dataset hosts.

| PS | Q1 core terms | Q2 product terms | Q3 failure terms | Q4 artefacts |
|---|---|---|---|---|
| AI-01 | audio deepfake detection, anti-spoofing, AASIST, RawNet, XLS-R spoof, synthetic speech detection | voice scam detector, deepfake call blocker, voice biometric fraud | "unseen generator", cross-dataset EER, shortcut learning | ASVspoof 2019/2021, In-the-Wild, WaveFake, ASVspoof5, AASIST weights |
| AI-02 | text-to-SQL agent, BIRD benchmark, schema linking, SQL validation loop | AI data analyst, chat with database, BI copilot | BIRD failure analysis, dirty schema, hallucinated SQL | BIRD train/dev, Spider, Spider 2.0, open-weight <=8B SQL models |
| AI-03 | GraphRAG, LightRAG, entity extraction, community detection, hybrid retrieval | knowledge base chat, graph RAG product | GraphRAG cost, extraction drift, community quality | Neo4j, Chroma, pyvis, graph datasets |
| AI-04 | RAG evaluation, faithfulness, context relevance, synthetic Q generation | RAG observability, LLM eval platform | RAGAS limits, judge bias, eval gaming | RAGAS, TruLens, DeepEval, ARES, RGB benchmark |
| W3-01 | Circom, Noir, zk credential, signature in circuit, semaphore | ZK KYC, age proof, privacy passport | under-constrained circuit, forged proof CVE | circomlib, snarkjs, noir libs, zk-email |
| W3-02 | ERC-4337, account abstraction, session keys, policy wallet | agent payments, autonomous checkout | 4337 paymaster griefing, session key leaks | permissionless.js, Safe modules, Rhinestone, Alchemy AA |
| HM-01 | RDKit, molecule canonicalization, tautomer, PubChem snapshot | reproducible cheminformatics, ELN | silent imputation, toolkit version drift | PubChem, ChEMBL, RDKit, Open Babel |
| HM-02 | drug interaction check, brand to generic, BNF, RxNorm mapping | prescription safety app, med checker India | alert fatigue, brand ambiguity | openFDA, RxNorm, CDSCO, 1mg/PharmEasy catalogues |

## 2. Ledger contract

Every sweep appends one TSV row: `ps, platform, query, route, taken_at, hits, best_candidate_url, licence_seen, note`. Zero-hit rows are mandatory. A platform with no zero-hit row will be treated as unsearched.

## 3. Anti-generic checks before any verdict

1. Did the sweep touch at least one Chinese forge and one non-English community for the chosen PS?
2. Did it check hackathon archives for a project that already implements the statement?
3. Did it read the failure threads, not just the star counts?
4. Are weights/datasets actually downloadable, with a licence, today?
5. Is any claimed "novel" feature already shipped in a product found in tier 6?

## 4. Known dead ends on this box (do not spend time again)

- raw curl to Cloudflare-fronted sites: 403 / challenge page.
- r.jina.ai: same 403 shell.
- headless brave --dump-dom on Cloudflare: challenge page, no DOM.
- Firecrawl and web_search billing: dead on this pool.
- Unauthenticated GitHub REST search: rate limited; use `gh` CLI (authed as harshgounder) instead.
