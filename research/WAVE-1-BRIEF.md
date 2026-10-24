# WAVE 1 BRIEF: wide discovery (v1, 2026-10-24 ~14:30 IST, claude/lead)

Read FLEET-BRIEF.md (v3) first. This file is the work order for wave 1.

## User answers (2026-10-24 ~14:25, in force)

| topic | answer |
|---|---|
| deadline | **CORRECTED 14:50 (official site, verified by claude):** Round 1 EVALUATION runs 03:00-06:00 IST 25 Oct (PPT, prototype, presentation). Everything must be judgeable by **03:00**; target freeze 02:30. Additional problem statements release 18:15-20:15 today. Round 2 shortlist 06:30; Round 2 presentations 11:30-14:00; final 15:00-16:30 |
| rules | everything allowed. Copying or forking any project from GitHub, Gitee or anywhere is fine. Judges care about what they see, not novelty of code |
| statements | ONE statement only |
| team | just the user + the fleet |
| deliverables | live URL (website). If an app is needed it runs on the user's PC, and the website hosts it. YC-style startup pitch deck. Apple-style demo video only if everything else is done |
| judges | not deep tech experts. The project must look and sound mind-blowing to a common person and answer their "what if this happens?" questions |
| Parallel AI | spend freely, all products (search, extract, task, task groups, deep research, findall, chat, monitor). The user will buy more keys |
| scope | AI/ML first (it is an AI hackathon). Hardware: NO. Climate and Smart Cities: ignore unless you find a truly mind-blowing angle |

## Statements in scope

| priority | ids |
|---|---|
| P-A full depth | AI-01, AI-02, AI-03, AI-04, HM-01, HM-02, W3-01, W3-02 |
| P-B wow scan only (report only if mind-blowing, with reasons) | CL-01, CL-02, CL-03, CL-04, SC-01, SC-02 |
| out | HW-01 |

## The user's complaint about wave 0 (read it twice)

The first per-track lists (Vanna, RAGAS, GraphRAG, circomlib...) were called "so generic and small". The famous top-3 on GitHub is the starting point, not the result. Wave 1 must go far past it.

**Every source class below, every region, every language.** If a class gives nothing, write "searched X with queries Q, 0 relevant" so we can see it was covered.

### Code and model hosts (all of them)
GitHub (repos, topics, awesome-lists, code search, releases, gists), GitLab, Codeberg, Bitbucket, SourceForge, Gitee, GitCode (CSDN), Coding.net, OpenI (pcl), Gitea instances, Hugging Face (models, datasets, Spaces), ModelScope (Alibaba), Baidu AI Studio / PaddleHub, WiseModel, OpenXLab, Kaggle (notebooks, datasets, competition winners' write-ups), Papers With Code successors and code-linked arXiv, Replicate, Colab notebooks, Observable, CodeSandbox / StackBlitz / Glitch / Replit, Vercel and Netlify templates, npm / PyPI / crates packages, Docker Hub.

### Hackathon and competition winners
Devpost, DoraHacks, ETHGlobal showcase, Gitcoin, Encode, HackerEarth, Unstop, Devfolio, MLH, Kaggle, AIcrowd, DrivenData, Zindi (Africa), Tianchi (Alibaba), DataFountain, Signate (JP), Dacon (KR), AI City Challenge, ASVspoof challenge entries, BIRD leaderboard entries, TREC / CLEF tracks.

### Forums, social, blogs (global + regional)
Reddit (all relevant subs), Hacker News (Algolia search), X/Twitter, LinkedIn posts, YouTube demos, Discord/Telegram public channels, Medium, dev.to, Hashnode, Substack, Product Hunt, Indie Hackers.
China: Zhihu, CSDN, Juejin, Bilibili, V2EX, cnblogs, WeChat articles (via search), SegmentFault. Japan: Qiita, Zenn, note. Korea: velog, Tistory, Naver blogs. Russia: Habr. India: Analytics Vidhya, Indian dev Discords, IIT/NIT project pages. Europe, LatAm, Africa: local-language blogs where relevant.

### Papers and demos
arXiv (with code), Semantic Scholar, OpenReview, ACL Anthology, conference demo tracks (NeurIPS/ACL/EMNLP/Interspeech demos), university lab pages, live hosted demos.

## What each lead row must have

`research/<agent>/<PS-id>.md`, one table row per lead:

| field | meaning |
|---|---|
| name + URL | exact |
| host / region / language | where found |
| what it does, in plain words | 1-2 lines a non-tech person understands |
| wow for a common person | why a judge goes "whoa" (or "none") |
| what-if coverage | which judge questions it can answer live |
| licence, last commit, stars/downloads | numbers from the page, with fetched date |
| has weights / dataset / live demo | yes/no each |
| runs from a website? | in-browser / hosted backend / local only / unknown |
| combine-with | other leads it could merge with |
| status | VERIFIED (you opened it this session) or UNVERIFIED |

Plus at the top of each file: queries run, sources covered, sources that gave 0.

## Lanes

| lane | owner | what |
|---|---|---|
| L1 code/model/competition hosts | **dsh** (use your sub-fleet, unlimited) | every P-A statement across ALL code/model hosts and competition winner lists above, China/JP/KR hosts included. Clone or download the top candidates into `~/hypnexis-main/research/dsh/clones/` only when cheap (<500 MB each), note size |
| L2 forums/social/papers + regional | **hermes** (NO code; use your sub-fleet) | every P-A statement across forums, social, blogs (all regions above), papers, demo tracks. Surface leads that code-host search misses. Plus the P-B wow scan |
| L3 judge lens | **hermes** | for each P-A statement: the 5 "what if" questions a common person would ask, and which leads answer them. Plus Unstop page for this round: rules, judging, timeline (save raw to `research/hermes/unstop/`) |
| L4 ideation method | claude | copypaste.txt, solar (crazy and guerrilla ideas), SIH LUNAR-TIE ideation, merged into `method/IDEATION-METHOD.md`, then wave 2 |
| L5 check | claude now, codex after 16:28 | open and verify every lead that reaches a shortlist |

## Timing

| when (IST) | what |
|---|---|
| now to 15:30 | first pass, write files as you go (partial files are fine; never hold work in memory) |
| 15:30 | checkpoint: one bus message on `hyp` with counts per statement and file paths |
| 15:30 to 17:00 | deeper pass: second-order leads (forks of forks, Chinese mirrors, papers' code, competition write-ups) + combinations |
| 17:00 | wave 1 closes. claude merges, checks, ranks with reasons; the user picks with us ~17:30 |
| 17:30 to 05:00 | build (fork + customise + santioni-level website), deck, deploy, video if time |

## Quality rules

1. No verdicts without reasons. "Pick X" is useless; "X because a, b, c, here are the links" is the job.
2. Every number: URL + fetched time. Opened it = VERIFIED, otherwise UNVERIFIED.
3. Generic or shallow output gets sent back and redone. claude rechecks every file; codex will recheck after 16:28.
4. Do not stop at the first 10 results of a query. Use many queries, many languages, many synonyms.
5. No em dashes, no AI-tell words.
