# Wide-scope source map (dsh lane), 2026-10-24

Rule from the user: never generic, never training data. Global plus region plus country.
Every code host, model hub, dataset hub, competition platform, forum, social and paper index
that can plausibly hold a forkable project or a usable dataset. A source counts only after it
was actually queried in a wave and the query is logged.

## Baseline from the earlier campaign

`~/fleet-log/research/platform-hunt/PLATFORM-REGISTRY-MERGED.tsv`: 649 rows.
Region split: 409 global, 74 China, 33 Russia, 23 Japan, 17 Korea, 16 India, 7 France,
6 Germany, 6 Brazil, 5 each Turkey Spain Poland Iran, 3 Vietnam.
Category split is news/social/forum heavy (67 news, 34 social, 32 hackathons, 28 security,
28 Europe press, 26 forum, 24 China, 23 research, 23 ai-hub, 20 chat).
Gap: project discovery is thin. Gitee 2 rows, GitCode 1, ModelScope 1, OpenI 1, Tianchi 1,
DataFountain 1, AIcrowd 1, Zindi 1, Devpost 2, Devfolio 1, Unstop 1. That is the layer to grow.

## Layer 1: code and project hosts

| region | hosts |
|---|---|
| global | GitHub (repos, code search, topics, trending, discussions), GitLab, Bitbucket, SourceForge, Codeberg, Gitea public instances, sr.ht, GNU Savannah, Launchpad, Fossil, GitHub Gists, grep.app, Sourcegraph, searchcode |
| China | Gitee, GitCode (CSDN), Coding.net, AtomGit (OpenAtom), OSChina Git, JihuLab |
| Russia | Habr (articles plus code), GitFlic, GitVerse |
| Japan | Qiita, Zenn, Speaker Deck, GitHub JP orgs |
| Korea | Velog, Tistory tech blogs |
| India | Unstop, HackerEarth, Devfolio, SIH archives, college lab repos |

## Layer 2: model and weight hubs

Hugging Face (models, datasets, spaces), ModelScope (Alibaba), OpenI 启智, PaddleHub,
MindSpore Hub, Baidu AI Studio, Replicate, Ollama library, ONNX Model Zoo, TF Hub, PyTorch Hub,
NVIDIA NGC, Civitai (image weights), Shadertoy and Observable (visual demos), Spline and
Three.js examples (motion references).

## Layer 3: dataset and benchmark hubs

Hugging Face datasets, Kaggle (datasets and competitions), OpenML, UCI, Zenodo, Figshare,
AWS Open Data, Google Dataset Search, Papers with Code datasets, PhysioNet, OpenAlex, Crossref,
Semantic Scholar, OpenReview, arXiv (cs.CL, cs.CV, cs.SD, cs.LG, cs.AI), domain sets:
PubChem and ChEMBL (HM-01), BIRD and Spider (AI-02), ASVspoof and In-the-Wild (AI-01),
Sentinel-2 and Copernicus (CL), OSM and Project Sidewalk (SC).

## Layer 4: competitions and prior winners

Kaggle, AIcrowd, Zindi, Tianchi, DataFountain, DrivenData, Bitgrit, Signate, Nishika,
Devpost, Devfolio, Unstop, HackerEarth, MLH, XPRIZE, HeroX, InnoCentive.
Prior winners matter more than listings: the winning repo is a proven fork base.

## Layer 5: forums, socials, papers of record

Hacker News, Reddit (per-domain subreddits), Lobsters, Stack Exchange sites, dev.to, Hashnode,
Medium, X, LinkedIn, Bluesky, Mastodon, YouTube and Bilibili demos, V2EX, Zhihu, CSDN, Juejin,
SegmentFault, OSChina, Habr, Qiita, Zenn, Velog.

## How a wave is run (pre-registration, from the solar idea census)

1. Pre-register the exact queries and the source list before looking at results.
2. Every claim gets URL plus fetched_at plus VERIFIED or UNVERIFIED.
3. Every candidate project gets a falsifier: the one fact that would kill it (license,
   dead repo, no browser demo, model too big).
4. Nothing from training data. If a wave did not fetch it, it is not in the report.
5. A bank entry becomes a candidate only when a wave names it, with a reason and a falsifier.

## Wave status

- Wave 1 fired 2026-10-24 14:20 IST: Parallel TaskGroup `tgrp_85133678a4ff429386c65a9af82acad2`,
  8 statements (AI-01..04, W3-01, W3-02, HM-01, HM-02), pro processor, fields: fork candidates,
  datasets, models, mind-boggling demo angles, regional sources checked, missing pieces, risks,
  sources. Poll and log results here when it lands.
- Wave 2 (planned): competitions and prior winners only, per shortlisted statement.
- Wave 3 (planned): region sweep (China, Russia, Japan, Korea, India) for the shortlist.
