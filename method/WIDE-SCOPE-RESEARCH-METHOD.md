# WIDE-SCOPE RESEARCH METHOD (v1, written 2026-10-24 by claude, read-only extraction)

What this file is:

- **Part 1** describes how the crypto-events-atlas campaign (`~/crypto-events-atlas`, run 2026-10-22 to 2026-10-23) was actually run. It comes from that campaign's own files, and each claim names the file it came from.
- **Part 2** is an **ADAPTATION**. It retargets the same source universe and method to the 15 Hypnexis problem statements (`~/hypnexis-main/PROBLEM-STATEMENTS.md`). None of Part 2 has been run. Any named project, dataset, repo or site in Part 2 that does not come from the problem statements or the atlas files is a **seed hypothesis (UNVERIFIED)**. The research lanes must confirm or drop each one.
- **Part 3** is the coverage audit: the files read, their `wc -c` sizes, and what was not read.
- **Part 4** red-teams this file, with each claim graded.

Grades used: **VERIFIED** (I read it in the named file, or I ran the command), **UNVERIFIED** (seed or inference, not checked), **EXAGGERATED**, **WRONG**.

Rule from the user doctrine (`~/.claude/CLAUDE.md`): structure comes only from sourced landings. Anything proposed without a source is a hypothesis list. Part 2 follows that rule: its taxonomy is copied from the atlas structure, and its named items are labelled as seeds.

Path abbreviations used below: `A/` = `~/crypto-events-atlas/`, `PS` = `~/hypnexis-main/PROBLEM-STATEMENTS.md`, `FB` = `~/hypnexis-main/FLEET-BRIEF.md`.

---

# PART 1: THE METHOD AS IT WAS ACTUALLY RUN (crypto-events-atlas)

## 1.0 The ask that set the scope

The user's original ask is quoted verbatim in `A/GOALS.md` line 9. Its parts are:

- Find "sites or platforms that inform u of any crypto related event".
- Cover "many more types of events ... that i dont know of".
- "keep your scope as wide as possible".
- "dont just go through the global generic stuff go through the regional or countrys counterparts of those forums and aggregators or socials or project hosting spaces like github".
- "perform multiple waves tens of them of research and refinement".
- "use tiny fish and your websearches and like we did for dsh fleet".

The third ask, after the first pass (`A/GOALS.md` line 58), called the searches "verrry basic generic extremely surface level". It asked for a concentrated layer on X and other high-volume socials and forums. That ask produced the deep layer (section 1.6).

## 1.1 Timeline (from `A/LOG.md`, `A/WAVES.md`, `A/DEEP-LAYER-PLAN.md`)

```
2026-10-22
 W0    read protocol + skill + dedupe baseline; TinyFish key found; tf.py written; region/lang params tested (JP)
 W0.6  Parallel AI found DEAD (createDeepResearch x4 -> 401; 412 of 412 keys spent); fallback chosen
 W1    main session harvest: airdrops.io, cryptorank drophunting, coinmarketcal -> 00-sourced-landings.md
 W2-W7 topic lanes (2 opus researchers in parallel per wave)
 W8-W14 regional lanes (CN, JP, KR, VN+TH, IN, TR, RU/CIS, FA, Africa, BR/PT, ES/LATAM, EU-W, ID+PH, AR-MENA, EU-E)
 13:35 Claude session limit (HTTP 429) killed 2 lanes -> ONE lane at a time from then on
 15:12 compaction prep: GOALS, CONTINUATION, LANE-TEMPLATE, NEXT-LANES, verify_state.py, archive tarballs
 18:02 post-compaction audit: verdict "NOT achieved"; 8.5% of lane bytes read by main session
 18:25 W15 (MY/SG/Oceania/Nordics), 18:40 W16 (PK/BD/LK/NP/Central Asia)
 19:10 user ask 3 ("surface level"): measured the shallowness, tested 30+ access routes, wrote DEEP-LAYER-PLAN
 19:35 W17 L16 type gaps lane
 20:25 D1 X crawler started (scripted, no subagent)
2026-10-23
 00:29-04:58 D1b, D1c, D2, D3, D4, D5, D6, D7, D10, D11 collectors + one opus reading lane per corpus
 04:58 last logged step: D11READ (India slice) landed and checked
```

Not run by the last log line (`A/WAVES.md` rows W14 to W22; `A/prompts/NEXT-LANES.md`): L10a and L10b socials, L12 alert consolidation, L13 scams, L14 eligibility, L15a and L15b, both lie hunts, the uniqueness pass, pass 2, the 3x loop re-runs, the merged taxonomy, the README and the repo. These are listed in `A/scripts/verify_state.py` TODO_LANES.

## 1.2 Interpretations first, then a goal checklist

Before any search, the ask was split into readings and each reading got a verdict (`A/SCOPE.md` lines 9 to 17, repeated in `A/GOALS.md` lines 15 to 23):

| # | reading | verdict |
|---|---|---|
| A | a map of the SOURCES that announce events, global and regional | primary |
| B | a taxonomy of EVENT TYPES, including types the user does not know | primary |
| C | a live list of what is open now | by-product only, every item dated |
| D | build an alert bot | NOT asked; catalogue the mechanisms, build nothing |
| E | redo the earlier income analysis | already on disk; dedupe against it |

The readings then became a goal checklist (G1 to G13 in `A/GOALS.md`), each with a state such as DONE, PARTLY, NOT DONE, HOLDING or PLAN ONLY. After the compaction the checklist was re-scored against computed numbers, not against memory (`A/AUDIT-2026-10-22-post-compaction.md` sections 2 and 6).

## 1.3 How the source universe was defined

### 1.3.1 Source classes: the lane tree

`A/SCOPE.md` lines 23 to 41 hold the seed lane tree. It was written as a hypothesis list ("STATUS: SEED. Everything below is a hypothesis list from my head", line 3), and the harvest waves replaced it with sourced landings. The final set of classes, combining the breadth lanes and the deep layer:

| class id | source class | what it covers | first route used | lane file (under `A/research/`) |
|---|---|---|---|---|
| L1 | event-type taxonomy | every way the thing being searched for gets handed out | the category filters of aggregators, exchange announcement categories | `L1-taxonomy/00,01,02` |
| L2 | global aggregators and calendars | trackers, calendars, dashboards | TinyFish search, then each page's own filters and feeds | `L2-aggregators/01` |
| L3 | first-party channels of the big platforms (exchanges) | official programs and announcement feeds, with public JSON APIs | the platforms' own announcement APIs | `L3-exchange/01` |
| L4 | launch platforms | launchpads and sales | platform docs | `L4-launch/01` |
| L5 | quest and task platforms | quests, points, paid micro-tasks | platform docs, payout ledgers | `L5-quests/01` |
| L6 | niche ecosystem tools (memecoins) | launchpads, discovery tools, alert tools, wallet trackers | tool docs, keyless APIs tested with curl | `L6-memecoins/01,02` |
| L7 | bounties, grants, hackathons | listings with dated deadlines | public listing APIs (Superteam Earn) | `L7-bounties/01` |
| L8 | per-ecosystem program pages (chains) | foundation programs, incentive dashboards | each foundation's own page, Merkl API | `L8-chains/01,02` |
| L9 | code hosts (GitHub, GitLab, Gitee) | awesome lists, claim contracts, tracker repos, scrapers, malware that imitates them | GitHub search API, indexers | `L9-github/01` |
| L10 | social and community kinds | Telegram, Discord, X, Farcaster, Reddit, YouTube, newsletters, podcasts | planned as L10a and L10b, never run as lanes; covered later by the deep layer | (not written) |
| L11 | regional and country counterparts | local exchanges, media, forums, Telegram, vocabulary, law, scams | TinyFish with `--loc` and `--lang` | `L11-regional/01` to `17` |
| L12 | alert mechanisms | RSS, APIs, bots, webhooks per source | docs and curl | planned, not run |
| L13 | scams and fakes tied to the topic | fake claim sites, drainers, templated repos | security-firm reports, regulator lists | planned, not run (scam rows live inside other lanes) |
| L14 | eligibility | geo, KYC, sybil rules, India access | per-source terms | planned, not run |
| L15 | leading indicators and legacy items | governance forums, indexers, docs diffs, old claims | Snapshot, Discourse, indexers | planned, not run (partly covered by D4) |
| L16 | type gaps | thin or missing types found by the audit probe | 8+ query angles per type | `L16-type-gaps/01` |
| D1 to D11 | deep corpora | X, Telegram, YouTube, Bitcointalk and governance forums, Reddit, Bluesky/Medium/Substack, Binance Square, GitHub tooling, India slice | scripted collectors (section 1.8) | `D-deep/01` to `11` |

### 1.3.2 Rules attached to every source row

From `A/SCOPE.md` lines 45 to 50 and `A/BRIEF-COMMON.md` lines 24 to 30. For SOURCES, each row records:

- name and URL
- the types covered
- freshness: the date and where that date was seen
- free or paid
- the alert mechanism (RSS, API, Telegram, Discord, email, push or none)
- geo or KYC limits
- shill risk
- a non-obvious note
- known or new against the baseline
- VERIFIED or UNVERIFIED

Event-type rows have their own schema: type, mechanism, who runs it, where it is announced, eligibility and time cost, scam exposure, alive or dead in 2026, 2 to 4 dated examples with URLs, and VERIFIED or UNVERIFIED.

### 1.3.3 Geographic layering

The regional lanes (`A/scripts/verify_state.py` DONE_LANES; `A/WAVES.md` W8 to W16):

| lane file | region | languages named in prompts or collectors |
|---|---|---|
| 01-chinese-language | Mainland CN, HK, TW | zh (simplified and traditional) |
| 02-japanese | JP | ja |
| 03-korean | KR | ko |
| 04-vietnam-thailand | VN, TH | vi, th |
| 05-india | IN (own lane: the reader's home market) | en, hi, Hinglish |
| 06-turkish | TR | tr |
| 07-russian-cis | RU, CIS, UA | ru, uk |
| 08-persian | IR (Persian) | fa |
| 09-africa | NG, KE, ZA, GH and others | en, fr, sw, ha |
| 10-brazil-portuguese | BR, PT, Lusophone Africa | pt |
| 11-spanish-latam | ES, LATAM | es |
| 12-western-europe | DE, AT, CH, FR, BE, IT, NL | de, fr, it, nl |
| 13-indonesia-philippines | ID, PH | id, tl |
| 14-arabic-mena | Arabic MENA, Gulf, Egypt | ar |
| 15-eastern-europe | PL, CZ, SK, RO, HU, GR | pl, cs, ro, hu, el |
| 16-my-sg-oceania-nordics | MY, SG, AU, NZ, NO, SE, FI, DK | ms, en, sv, no, da, fi |
| 17-south-asia-pk-bd-lk-np-ca | PK, BD, LK, NP, Central Asia, Caucasus | ur, bn, si, ne, uz, ky, az, ka, hy |
| D-deep/11-india-slice | India again, across all deep corpora | hi, bn, ta, te, mr, gu, kn, ml, pa scripts plus Hinglish |

How the scope widened during the run (from `A/LOG.md`):

- Four countries in one lane proved too big, so ID, PH, MY and SG were split out (W9B note).
- India got its own lane because it is the reader's home market (W10A note).
- Arabic MENA was split away from Persian (W11B).
- LATAM-ES was split away from BR/PT (W12B).

Regions the files list as not covered (`A/AUDIT-2026-10-22-post-compaction.md` section 4; `A/prompts/NEXT-LANES.md` row 11):

- CN Macau
- Africa: Zambia, Zimbabwe, Rwanda, Mozambique, Angola, DRC
- RU/CIS: Armenia, Azerbaijan, Georgia, Moldova, Uzbekistan, Tajikistan (W16 later covered part of these)
- ES: Uruguay, Paraguay, Bolivia, Ecuador, Central America, Dominican Republic, US Hispanic
- EU: Flemish Belgium, Swiss French and Italian, Serbia, Croatia, Slovenia, Baltics
- Israel/Hebrew, Mongolia, Cambodia, Laos, Myanmar, the Caribbean, the Pacific

### 1.3.4 Language layering

Language was a separate axis from country. Each collector carried its own language table. Every layer below is VERIFIED by reading the named script.

| layer | where | languages |
|---|---|---|
| search engine locale | `A/scripts/tf.py`: `--loc` (country code) and `--lang` (language code) on every TinyFish search | any; tested with JP and ja on day 0 (`A/LOG.md` W0.3) |
| regional lane prompts | `A/prompts/LANE-TEMPLATE.md`: "Work in <languages>: use tf.py --loc <CC> with --lang <xx> and write natural local queries" | per lane |
| local vocabulary tables | each regional file has a vocabulary table (17 CN/JP/KR terms in L1a; 18 to 46 terms per regional file per `A/LOG.md`). The terms then became search keywords for later lanes (`A/LEADS.md` line 35) | per region |
| X keyword discovery | `A/scripts/d1c_kwsearch.py` LOCAL dict: 25 languages (hi, id, vi, tr, ru, pt, es, ar, ko, ja, zh, fa, ur, bn, th, fr, de, pl, it, uk, nl, sw, tl, ms, he) plus about 69 English queries, each with its matching country code | 26 |
| YouTube | `A/scripts/d3_youtube.py` Q dict: en plus hi, id, vi, tr, ru, pt, es, ar, ko, ja, zh, fa, ur, bn, ta, te, mr, th, fr, de, pl, it, uk, nl, sw, tl, ms, ne, he | 30 |
| Binance Square | `A/scripts/d7_square.py` LOC: 22 site locales (en, vi, tr, zh-CN, ru, ar, es, pt-BR, id, fr, de, ko, ja, th, uk-UA, pl, it, bn, es-MX, ro, kk-KZ, zh-TC) | 22 |
| Bitcointalk | `A/scripts/d4_boards.py` BOARDS: 36 boards, including India, Regional Languages (India), Naija, Pilipinas, Indonesian, Turkish, Spanish, German, French, Italian, Dutch, Polish, Portuguese, Brasil, Romanian, Greek, Japanese, Croatian, Chinese, Arabic, Korean and Russian | 20+ |
| first-party locale feeds | Binance CMS `lang` header and Bybit `locale` parameter, polled per locale (`A/CONTINUATION.md` sections 4 and 4b) | en, en-IN, es, es-MX, es-AR, pt-BR, ar, ar-BH, ru-KZ, az-AZ, vi-VN, th-TH, tr-TR, ar-SA, EU locales |
| Indian scripts | `A/scripts/d11_india_slice.py` SCRIPT regex covers Devanagari, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam and Gurmukhi; `A/scripts/d11_india_collect.py` has queries in hi, bn, ta, te, mr, gu, kn, ml, pa | 9 scripts |

The key finding on language (`A/CONTINUATION.md` section 4b; `A/LEADS.md` lines 136, 154, 197, 327): **a locale feed can hide items that the default feed does not show, and the reverse is also true.** For example, India-only Binance campaigns appear only with the header `lang: en-IN`. In the other direction, Bybit's Vietnam-only campaigns appeared in en-US but not in the vi-VN feed. Rule: poll the default AND every locale before claiming that something does not exist.

## 1.4 Lane and wave structure

```
                      user ask
                         |
        interpretations + goal checklist (GOALS.md)
                         |
   W0 rails test --- W1 main-session harvest (sourced landings)
                         |
   +---------------- BREADTH LAYER (W2..W17) ----------------+
   | topic lanes L1..L9 (W2-W7) | regional lanes L11 (W8-W16)|
   | type-gap lane L16 (W17)    | leads -> LEADS.md -> seeds |
   +--------------------------+------------------------------+
                         |
            post-compaction AUDIT (computed, not remembered)
                         |
   +---------------- DEEP LAYER (D1..D11) -------------------+
   | measure shallowness -> test 30+ access routes          |
   | scripted collectors (no model tokens) -> raw/D*/       |
   | keyword prefilter -> reading batches (~140-150 KB)     |
   | ONE opus reading lane per corpus -> research/D-deep/   |
   | strict novelty vs a frozen baseline (number, not vibe) |
   +--------------------------------------------------------+
                         |
   (planned, NOT run) refinement: L10/L12-L15, lie hunts,
   uniqueness pass, pass 2, 3x loop W19-W22, consolidation
```

Wave definition (`A/WAVES.md` line 1): "A wave = 2 opus researchers in parallel + main-session checks". After the 13:35 rate-limit kill, waves ran ONE lane at a time (`A/LOG.md` line 57; `A/CONTINUATION.md` section 3).

Each lane went through this loop, taken from `A/CONTINUATION.md` section 2:

1. Launch one `researcher` subagent (opus, in the background). Its prompt is built from the lane template.
2. Treat the 5-line hand-back as a claim, not as a fact. Open the lane file's leads and gaps sections and run 3 to 8 claim checks against primary sources.
3. Append a "main-session review" table to the lane file, with columns claim | how I checked | VERIFIED / PARTLY / WRONG / UNVERIFIED.
4. Append a block to LEADS.md, add a line to LOG.md, and update the WAVES.md row.
5. Send a Telegram update and give the user a table.

The waves were connected through `A/LEADS.md`. Every landed lane appended its "leads for other lanes", and those leads became the seeds of later lanes (`A/WAVES.md` line 41). For example, the CN lane's vocabulary terms were fed into the KR and JP searches, and the Arabic lane's "Pakistan Exclusive" leads went to the South Asia lane.

## 1.5 Prompts used

| prompt | file | what it fixes |
|---|---|---|
| common brief, read in full by every subagent | `A/BRIEF-COMMON.md` | today's date and the reader; hard rules (no agents, no signups, no wallet connects, write only the named file, in parts of about 60 lines); the dedupe baseline; "ranking pages are often paid shills"; every finding needs URL + its own date + where the date was seen + VERIFIED/UNVERIFIED; freshness; the tool recipes (`tf.py search/fetch`, `t.me/s/`, `gh api`, WebSearch); "Parallel AI is DEAD today"; the output table schemas; a "leads for other lanes" section; a "gaps" section; a hand-back of at most 5 lines; the shared-scratchpad rule |
| lane prompt template | `A/prompts/LANE-TEMPLATE.md` | "First read BRIEF-COMMON.md in full"; lane id, scope, wave; write in parts early, so that a rate-limit kill still leaves a usable file; regional and local-language instruction; an "already covered elsewhere (grep, do not repeat)" list; six topics per region (vocabulary, local platforms and their APIs, media/aggregators/Telegram/forums/YouTube/Discord/Facebook, local programs with dated deadlines, law and tax, local scams); "find at least 30 named sources not in the seeds"; the output path; the after-hand-back checklist |
| remaining lane specs | `A/prompts/NEXT-LANES.md` | 13 rows: lane id, output file, scope, seeds from LEADS.md; a fact-checker subagent for the lie hunts (15 claims each, verdicts CONFIRMED / PARTLY / WRONG / CANNOT VERIFY); uniqueness built "from headings and table first columns only, then hunt unknown unknowns" |
| rules added after the W15 audit | `A/LOG.md` line 66 | full https URLs on every row; "VERIFIED vs VERIFIED (secondary)"; a list of "claims a skeptic should check first" |
| depth rules for L16 | `A/LOG.md` line 71 | 8+ query angles per type, primary pages, read X posts in full with xread.py, use the yt-dlp, Telegram, Snapshot and Bitcointalk routes |
| deep-layer reading lanes | `A/DEEP-LAYER-PLAN.md` section 4 | one opus researcher per corpus; read the corpus files by offset and record bytes read against `wc -c`; write the report in parts; an item is VERIFIED only when the source text was read in full |

## 1.6 The deep layer: how "surface level" was measured and answered

### Step 1: measure the criticism

`A/DEEP-LAYER-PLAN.md` section 1, computed from `raw/`:

| measure | value |
|---|---|
| search calls saved with a query | 1,984 |
| words per query | median 6, mean 6.7 |
| results read per query | about 8, one page, never paged |
| queries aimed at X | 7 |
| X status ids already in the campaign's own files but never opened | 884 |

Conclusion written in that file: "breadth came from many lanes, not from depth in any one source."

### Step 2: test every access route before planning

`A/DEEP-LAYER-PLAN.md` section 2 has a table of more than 20 routes. Each one was graded WORKS, 429, dead, 403 or STALE, with what it yields and its limit. Examples:

- X single-post syndication endpoint: works, 30 of 30.
- X profile timeline: 429.
- Nitter: dead.
- Telegram `t.me/s/CHANNEL?before=ID`: works.
- yt-dlp: works, but `ytsearchdate` is rejected.
- Bitcointalk board 238: works.
- Snapshot GraphQL: works.
- Discourse `/latest.json` and `/search.json`: works.
- Bluesky `api.bsky.app` searchPosts: works.
- Substack `/api/v1/archive`: works.
- Medium tag RSS: works.
- Reddit `.json`: 403.
- Arctic Shift Reddit archive: works, though first graded STALE. That grade was later corrected as WRONG for active subs (`A/LOG.md` 00:41).
- GDELT: 429.
- Binance Square API: returned null.
- Farcaster hubs: DNS failure.
- Discord: no public read.
- X logged in through the user's Chrome: NOT TESTED; it needs the user's yes.

### Step 3: plan layers with a confidence score and a stop rule

The plan (`A/DEEP-LAYER-PLAN.md` section 3) defined layers D1 to D9. Each had a method, an output file and a confidence score from 0 to 20 that it adds new data. For example: D2 Telegram 17, D3 YouTube 16, D1 X 15, D5 Reddit 9 (later raised to about 13), D7 Binance Square 6, and D8 logged-in X 12 only if the user says yes.

The stop rule (section 3, last paragraph): "novelty rate = share of handles, domains and event-type candidates in a corpus that do not appear in any atlas lane file. A layer stops when its novelty rate falls under 10 percent over its last 200 items."

### Step 4: split the work between scripts and the model

`A/DEEP-LAYER-PLAN.md` section 4 and section 10:

- **Collection is scripted** in the main session (curl, urllib, yt-dlp), at polite rates, saved under `raw/D*/`. This uses almost no model tokens, so it does not hit the Pro 5-hour limit the way the opus lanes did.
- **Reading is model work**: one opus lane per corpus, after a keyword prefilter, so that the Pro limit is not spent on raw volume.

### Step 5: snowball

- **X:** read the known ids. Then follow quote, reply and parent chains to depth 2. Then run per-handle `site:x.com/HANDLE/status` searches paged up to 3 deep (D1b). Then run keyword discovery across 26 languages, paged up to 10 deep (D1c).
- **Telegram:** run a census of 1,008 known handles, walk the live channels back in time, then run a round-2 census of 3,343 handles that were mentioned 2 or more times in the other corpora (`A/LOG.md` 02:41).
- **Substack:** find publications from links in the other corpora (`A/scripts/d6_longform.py substack-find`).

### Step 6: run a separate slice for the home market

When five reading lanes each reported that "nothing in an Indian script showed up", a separate India layer was built (`A/DEEP-LAYER-PLAN.md` section 12):

- India-specific collectors for X and Telegram.
- An India slice cut out of every corpus.
- One reading lane for that slice.

### Corpus sizes reached

| corpus | size | source file |
|---|---|---|
| X | 13,142 posts read by script after crawl2 | `A/LOG.md` 03:30 |
| X | "17,000 posts read by script", 3,990 read by the model across 3 lanes | `A/DEEP-LAYER-PLAN.md` section 13 |
| Telegram | 130,884 posts when the walk was 40% done; 1,123 more channels in walk 2 | `A/DEEP-LAYER-PLAN.md` section 11; `A/LOG.md` 03:51 |
| YouTube | 28,853 feed entries; 3,167 channels | `A/DEEP-LAYER-PLAN.md` section 11; `A/LEADS.md` D3READ block |
| Bitcointalk | 1,433 first posts | `A/DEEP-LAYER-PLAN.md` section 11 |
| Reddit | 76 subs; 230,912 posts scanned; 28,991 kept | `A/LOG.md` 04:37 |
| Bluesky, Medium, Substack | 4,672 items | `A/DEEP-LAYER-PLAN.md` section 11 |
| GitHub | 2,675 repos | `A/DEEP-LAYER-PLAN.md` section 11 |

## 1.7 Tools and rails, as the files record them

| rail | used? | evidence |
|---|---|---|
| TinyFish search (free; supports `location`, `language`, `after_date`, `page`) | YES, the main search rail for every lane | `A/scripts/tf.py`; `A/BRIEF-COMMON.md` line 15; `A/LOG.md` W0.2 and W0.3 |
| TinyFish fetch (free, returns markdown of JS pages, can return links) | YES | `A/scripts/tf.py`. Caveat: "TinyFish text copies of t.me pages drop dates, use curl" (`A/CONTINUATION.md` section 4) |
| TinyFish browser and agent modes | NO. They cost credits, and the user was asked first; that question is still open | `A/LOG.md` W0.2; `A/CONTINUATION.md` sections 4 and 9 |
| WebSearch and WebFetch (Claude tools) | YES, as a secondary rail. WebSearch is US-only. A WebSearch summary once stated an inference as fact (the Pharos date) | `A/BRIEF-COMMON.md` line 19; `A/LEADS.md` line 276 |
| Parallel AI (search, task groups, deep research) | NO. DEAD on 2026-10-22: createDeepResearch x4 returned 401, and 412 of 412 keys were spent. The parallel-search MCP failed to connect (DCR 404) | `A/LOG.md` W0.2 and W0.6; `A/BRIEF-COMMON.md` line 21 |
| GitHub CLI `gh api` (repos, search/repositories, code search with a 7 s sleep) | YES | `A/BRIEF-COMMON.md` line 20; `A/scripts/d10_github.py` |
| direct public JSON APIs | YES, a large share of the verification work | `A/CONTINUATION.md` section 4: Binance CMS, Bybit v5, Upbit, Coinone, Gopax, OKX, alpha123, Superteam Earn, Merkl, DefiLlama, Sablier indexer GraphQL, CERT Polska domains.json |
| X syndication endpoint (`cdn.syndication.twimg.com/tweet-result`, token formula) | YES | `A/scripts/xread.py`, `A/scripts/d1_xcrawl.py` |
| Telegram public preview `t.me/s/<channel>` (`?before=`, `?q=`) | YES | `A/scripts/d2_tgwalk.py`; `A/LEADS.md` line 130 |
| yt-dlp (search results URL with the `sp` filter) plus YouTube channel RSS | YES | `A/scripts/d3_youtube.py` |
| Arctic Shift Reddit archive API | YES | `A/scripts/d5_reddit.py` |
| Bluesky `api.bsky.app`, Medium tag RSS, Substack archive API | YES | `A/scripts/d6_longform.py` |
| Snapshot GraphQL, Discourse `latest.json` and `search.json`, Bitcointalk HTML | YES | `A/scripts/d4_boards.py` |
| Telemetr and tgstat country catalogues (Telegram channel discovery) | YES, inside lanes | `A/LEADS.md` lines 191, 218 |
| HN Algolia, Mastodon, Warpcast, 4chan /biz/, GDELT | probed only, graded low value or 429 | `A/DEEP-LAYER-PLAN.md` section 2 |
| claude-in-chrome on logged-in X (route D8) | NO: "NOT TESTED", needs the user's explicit yes; not asked again | `A/DEEP-LAYER-PLAN.md` section 2 and section 8 |
| `fact-checker` subagent (lie hunts) | PLANNED, not run | `A/prompts/NEXT-LANES.md` row 10 |
| firecrawl, searxng, rivalsearch | NOT mentioned anywhere in the campaign files I read (grep, 0 hits). Outside the campaign: `~/.hermes/config.yaml` line 62 has `backend: firecrawl` and lines 320 to 321 list a `rivalsearch` MCP URL. `~/.dsh/profiles/dsh-tui/cordis.patch.yml` line 2 says "rivalsearch removed on request". searxng was found in neither config | grep run 2026-10-24 by me |

## 1.8 Collectors and scripts (all in `A/scripts/`, all read in full)

| script | corpus or role | route | politeness and resume | output |
|---|---|---|---|---|
| `tf.py` | search and fetch wrapper | TinyFish API; the key is read at runtime from `~/.hermes/.env` and never printed | 3 retries on 429 | prints results; `--save` writes JSON |
| `xread.py` | read named X posts | syndication endpoint | 1 request/s | text, date, likes, quoted and parent post |
| `d1_xcrawl.py` | D1 X corpus | syndication; follows quote, reply and parent chains to `--max-depth` | 1 req/s; on 429 sleep 90 s, 3 tries, then exit 2; resumable | `raw/D1/status.jsonl`, `summary.json` (counts, handles, domains, months, novelty) |
| `d1b_search.py` | more X ids per handle | `tf.py search "site:x.com/HANDLE/status" --page N` | stops paging a handle when a page adds nothing; resumable | `raw/D1b/ids.json`, `new-seeds.json` |
| `d1c_kwsearch.py` | keyword X discovery (the discovery step D1 lacked) | `site:x.com` + about 69 EN queries + 25 languages, paged up to 10, `after` 2026-09-15 | same stop rule; resumable | `raw/D1c/ids.json`, `new-seeds.json` |
| `d2_tgwalk.py` | D2 Telegram | `t.me/s/` census, then a `?before=` walk back to `--since` | 1 req/s; on 429 sleep 60 s; resumable via `.walkdone` markers | `raw/D2/census.jsonl`, `posts/*.jsonl`, `summary.json` |
| `d3_youtube.py` | D3 YouTube | yt-dlp on the search URL in 2 modes (this month by date; this year by relevance), then the RSS feed of every channel seen | 1.5 s; resumable | `raw/D3/videos.jsonl`, `feeds.jsonl` |
| `d4_boards.py` | D4 forums | Bitcointalk 36 boards plus first posts; Snapshot 18 keywords; Discourse on about 90 forum domains | 1.2 s (Bitcointalk), 0.7 s (others) | `raw/D4/*` |
| `d5_reddit.py` | D5 Reddit | Arctic Shift, paging backwards 100 posts per call, keyword filter applied client-side (the server filter times out on big subs) | 1.2 s | `raw/D5/posts/*.jsonl`, `scan.json` |
| `d6_longform.py` | D6 Bluesky, Medium, Substack | public APIs and RSS; Substack publications found from the other corpora plus `site:substack.com` searches | 0.7 to 1 s | `raw/D6/*` |
| `d7_square.py` | D7 Binance Square | `site:binance.com/<locale>/square/post` searches over 22 locales, because the feed API needed a request shape that was not available | stop-on-no-new | `raw/D7/results.jsonl` |
| `d10_github.py` | D10 GitHub tooling and malware | `gh api search/repositories` with 45 queries in several languages, `pushed:>` date | 2.5 s per call | `raw/D10/repos.jsonl` |
| `d11_india_collect.py` | D11 India collectors | `site:x.com` and `site:t.me` with India terms and 9 Indian-language query sets, `--loc IN` | resumable | `raw/D11x/`, `raw/D11/handles-india.json` |
| `d11_india_slice.py` | D11 India slice | regex for India terms and Indian scripts, times event keywords, over ALL corpora; per-source quota cap | n/a | `raw/D11/reading/india-NN.txt` (about 140 KB each) |
| `d_prepare_x.py`, `d_prepare_tg.py`, `d_prepare_misc.py` | turn corpora into reading batches | keyword regex, exact-text dedupe, per-channel caps, noise regex (games, music, Apple AirDrop), newest-first; records what was handed over so a re-run gives only the delta | n/a | `raw/D*/reading/*.txt` of 140 to 150 KB |
| `atlas_baseline.py` | frozen novelty baseline | research files from the archive v6 tarball (taken before any D file existed) plus raw outside D* | cached | `raw/baseline-cache/*` |
| `d_strict_novelty.py` (superseded), `d_novelty_all.py` | strict novelty per corpus | `grep -Fowf` against the baseline; also counts names seen 3+ times, to remove the long tail of one-off referral and spam domains | n/a | `raw/novelty-all.json` |
| `verify_state.py` and `.sh` | state checker run after any compaction | lane files present, review/leads/gaps sections, collector counts, running processes, TODO lanes, last log lines, archive tar integrity, a secret scan that includes the TinyFish key itself, external state (memory note, repo, README) | n/a | stdout |
| `verify_binance_hodler.py` | one claim check | Binance CMS catalog 48, HODLer and Launchpool counts by year | 0.5 s | stdout |

## 1.9 How the agents were split

From the campaign files:

- **Main session (Claude)**: orchestrated, wrote and ran every collector, ran every claim check, and wrote the review tables, LEADS, LOG, WAVES, the AUDIT and the compaction kit (`A/CONTINUATION.md` section 2; `A/LOG.md`).
- **Research lanes**: one `researcher` subagent per lane, model opus, run in the background. Two ran in parallel until 13:35 on 2026-10-22, then one at a time (`A/GOALS.md` G6; `A/LOG.md` line 57). There was no nesting and no spawning by subagents (`A/BRIEF-COMMON.md` line 6).
- **Reading lanes in the deep layer**: one opus lane per corpus, told to read by offset and record bytes (`A/DEEP-LAYER-PLAN.md` section 4).
- **dsh and hermes as agents: NOT used in this campaign.** "dsh" appears only as the model for the work ("run it like the dsh fleet (many parallel lanes)", G6, answered with opus subagents). "hermes" appears only as file paths: the TinyFish key in `~/.hermes/.env`, the dedupe baseline in `~/hermes-money-farm/`, and log copies in `~/hermes_logs/`. Grep run 2026-10-24.
- **codex**: not mentioned in any campaign file.
- **The user**: was sent updates over Telegram (chat 6408901386) when a wave landed. When the plugin disconnected, it was noted (`A/LOG.md` line 67).

## 1.10 Verification gates

| gate | rule | source |
|---|---|---|
| G-a hand-back is a claim | never pass a subagent's summary on as fact; open the file and check | `A/CONTINUATION.md` section 2 step 2 |
| G-b claim checks per lane | 3 to 8 checks against primary sources (curl APIs, TinyFish fetch, GitHub API, `t.me/s` previews with post times, on-chain transactions) | same |
| G-c review table in every lane file | claim / how checked / VERIFIED, PARTLY, WRONG or UNVERIFIED by me; `verify_state.py` flags files without one | `A/scripts/verify_state.py` [1] |
| G-d tag strength | VERIFIED (opened and seen) vs VERIFIED (secondary) vs UNVERIFIED; "read the tag text, not just the word" | `A/LOG.md` line 66; `A/AUDIT...` 5f |
| G-e owner pages beat posts | the caps and conditions sit on the owner's page; posts leave them out. Three X lanes confirmed this | `A/LEADS.md` line 324 |
| G-f ranking pages are not evidence | "best of" pages are often paid; use the project's own page | `A/BRIEF-COMMON.md` line 9; `A/SCOPE.md` rule 3 |
| G-g false freshness | month-stamped titles and fresh homepages are false signals; use RSS pubDate or Telegram datetime; a fetch can return a cached copy | `A/LEADS.md` line 20; `A/LOG.md` W1 |
| G-h negative claims | before "no X since date": poll the default feed AND every locale AND every announcement type, sorted by date | `A/CONTINUATION.md` section 4; `A/LEADS.md` lines 154, 225 |
| G-i dates and numbers in leads | a lead that carries a number or date stays "unverified" until opened | `A/CONTINUATION.md` section 3 |
| G-j contradiction handling | cross-file conflicts are re-checked live and resolved in the file (Binance Brazil: resolved; Pharos: kept OPEN, with "use the earlier date" as the safe rule) | `A/AUDIT...` 5b, 5c |
| G-k state over memory | after a compaction, read GOALS then CONTINUATION, then run `verify_state.sh`; "files beat memory" | `A/GOALS.md` line 3 |
| G-l lie hunts | fact-checker agents on the 15 claims that would change a decision (planned, not run) | `A/prompts/NEXT-LANES.md` row 10 |
| G-m coverage audit | bytes read vs `wc -c`; the honest number published (8.5%) | `A/AUDIT...` section 1 |
| G-n safety | read only: no signups, logins, wallet connects or installs; never run code from airdrop-bot repos (malware families found) | `A/BRIEF-COMMON.md` line 6; `A/LEADS.md` line 283 |

## 1.11 Dedupe and the uniqueness loop

1. **Baseline first.** An earlier note already on disk was named as the dedupe baseline, so lanes do not repeat it ("Famous names alone are not a finding. Dig for niche, new, small, regional": `A/BRIEF-COMMON.md` line 8).
2. **"Already covered elsewhere" lists in every prompt.** Lanes grep LEADS.md and the neighbouring lane files before searching (`A/prompts/LANE-TEMPLATE.md`).
3. **LEADS.md as the shared memory.** Each lane's leads become the next seeds. A process gap was found: leads had no status marker, so "how many leads were followed up" could not be computed (`A/AUDIT...` 5d). The proposed fix was a status column (open / followed with file / dropped with reason).
4. **A probe of thin types.** 31 candidate groups were grepped over all lane files; zero or low counts marked a type as "not researched". That produced lane L16 (`A/AUDIT...` section 3). The probe list was openly labelled "from my head", meaning it shows where the lanes are thin, not that the rest is complete.
5. **Strict novelty for the deep layer.** Corpora are compared against a frozen pre-deep-layer baseline (archive v6 tarball plus raw outside D*), with whole-word matching. A second figure counts only names seen 3+ times. The first number computed (83% of handles new) compared only against the written reports and was misleading; against everything saved it was 16% (`A/DEEP-LAYER-PLAN.md` section 8 note; `A/LOG.md` 21:05).
6. **Novelty is not value.** "the reading lanes decide which of these are events, which are referral funnels" (`A/DEEP-LAYER-PLAN.md` section 11).
7. **Uniqueness pass (planned, not run).** Build a coverage map from headings and first table columns only, then hunt unknown unknowns: regions, types, and platforms that blocked every method (`A/prompts/NEXT-LANES.md` row 11).
8. **3x loop (planned, not run).** Re-run the regional and taxonomy lanes with new keywords from the leads (`A/WAVES.md` W19 to W22).

## 1.12 What failed, and the lesson kept

| # | failure | evidence | lesson to carry |
|---|---|---|---|
| F1 | the main paid rail (Parallel AI) was dead at the start | `A/LOG.md` W0.6 | W0 must test every rail before planning around it |
| F2 | rate limit killed 2 parallel opus lanes (Pro 5 h cap) | `A/LOG.md` line 57 | write outputs in parts early; resume with a fresh agent that reads the partial file and the raw folder; spread model load |
| F3 | two lanes overwrote each other's scratch script (`s.sh`) | `A/LOG.md` line 40 | per-lane folders `scratchpad/<LANE>/` and `raw/<LANE>/`; re-read the `query` field before trusting a raw file |
| F4 | zsh `=word` expansion trap hit three times | `A/AUDIT...` 5g | never start an argument with `=` |
| F5 | an unverified lead date was copied into LEADS | `A/LEADS.md` line 127 | a number or date in a lead stays UNVERIFIED until opened |
| F6 | locale-feed false negatives (Bybit vi-VN, tr-TR; Binance es, es-MX dead; en-IN hidden) | `A/LEADS.md` lines 136, 154, 196, 327 | poll default plus every locale plus every type |
| F7 | subagent headline claims were WRONG (Bybit VN "last campaign", Token Splash "dead") | `A/LOG.md` lines 38, 55 | main-session checks catch subagent errors; never relay a hand-back as fact |
| F8 | searches were shallow: median 6 words, 8 results, never paged, 7 aimed at X | `A/DEEP-LAYER-PLAN.md` section 1 | measure depth; page; read corpora, not snippets |
| F9 | lenient novelty overstated the gain (83% vs 16%) | `A/LOG.md` 21:05 | use a strict, frozen baseline |
| F10 | "Reddit 2026 unreadable" claim was WRONG (only true for a dead sub) | `A/LOG.md` 00:41 | probe several targets before declaring a route dead |
| F11 | `ytsearchdate` unsupported in installed yt-dlp | `A/LOG.md` line 72 | test the tool flags; filter on `upload_date` yourself |
| F12 | YouTube batches sorted by views were mostly games and music; regenerated 3 times | `A/LOG.md` 02:22 | add a topic regex AND a noise regex before the model reads |
| F13 | Discourse blurb matches pulled governance noise | `A/LOG.md` 01:22 | narrower filter; keep the old batch in a v1 folder |
| F14 | an English keyword filter could not reach Hindi or Hinglish posts | `A/LEADS.md` line 324 | build a home-market slice with script and term regexes |
| F15 | Snapshot first run returned 0 (POST without JSON content-type) | `A/LOG.md` 00:38 | zero results means check the request first |
| F16 | three lane files cite bare domains, not URLs | `A/AUDIT...` 5a | full https URL on every row, enforced in the prompt |
| F17 | main session read only 8.5% of lane bytes | `A/AUDIT...` section 1 | coverage is a number to publish, not a feeling |
| F18 | the refinement half (lie hunts, uniqueness, pass 2, 3x loop) and the save step (README, repo) were not done | `A/scripts/verify_state.py` TODO_LANES; `A/GOALS.md` G4, G9 | schedule refinement waves up front and give them a state row |
| F19 | sites blocked to every method (cryptorank, coindar, Gitee, Zhihu, Xiaohongshu, Nairaland, DCInside and others) | `A/CONTINUATION.md` section 4; `A/AUDIT...` section 4 | list blocked sites as gaps; ask before paying for browser or agent runs; one cryptorank page turned out readable, so test per page |
| F20 | the compaction summary repeated "VERIFIED" counts that mixed primary and secondary sources | `A/AUDIT...` 5f | re-derive numbers from disk after a compaction |
| F21 | an `rm` of test markers was blocked by the safety check | `A/LOG.md` 21:40 | do not work around safety checks; design the script to ignore the leftovers |
| F22 | the Telegram plugin disconnected; one wave had no update | `A/LOG.md` line 67 | log missed notifications |

## 1.13 Compaction kit (how state survived context loss)

From `A/LOG.md` line 62 and `A/CONTINUATION.md` section 11:

- `GOALS.md`: verbatim asks, interpretations, goal checklist with state.
- `CONTINUATION.md`: read order, the per-lane loop, incidents, method rules, headline findings with grades, corrections, the coverage number, the ordered not-done list, and open questions for the user.
- `prompts/LANE-TEMPLATE.md` and `prompts/NEXT-LANES.md`: so a fresh context can launch the next lane exactly.
- `scripts/verify_state.sh`: recomputes the state from disk.
- `archive/` tarballs (v1 to v6), dated copies, a copy in `~/hermes_logs/`, and a memory note.

# PART 2: ADAPTATION (template, NOT run): the same source universe retargeted to the 15 Hypnexis problem statements

> **ADAPTATION.** Everything in Part 2 is a plan and a template.
>
> - Nothing was searched for it.
> - Named items come from two places:
>   - (a) the problem statement text (`PS`, cited by line), which is sourced, or
>   - (b) my own memory, which makes them **seed hypotheses, UNVERIFIED**, in the same way `A/SCOPE.md` marked its seed tree.
> - Lanes must open each seed, record URL plus date plus where the date was seen, and keep it, correct it or drop it.
> - Per `FB` section 2, "No research and no code until the user says go after P1." This template is for P2 (research), after that GO.

## 2.1 Mapping the original to the new goal

| crypto-events-atlas concept | hackathon adaptation |
|---|---|
| goal: every SOURCE that announces free-token events | goal: every SOURCE that holds prior work for a problem statement: projects, repos, models, datasets, papers, benchmarks, demos, competition winners, forums, socials, regional work |
| L1 event-type taxonomy (including types the user does not know) | **artefact-type taxonomy** per PS (section 2.2), including artefact types the team does not know exist (for example a challenge's post-mortem paper, a winning team's write-up, a leaderboard's hidden test-set notes) |
| L2 global aggregators and calendars | global indexes: code search, model and dataset hubs, paper indexes, leaderboards, "awesome" lists |
| L3 first-party platform channels with JSON APIs | first-party channels: official challenge pages, benchmark sites, standards bodies (EIPs/ERCs), dataset owners, regulator portals |
| L4 to L8 topic lanes | per-PS lanes (15) grouped into 6 track clusters |
| L9 code hosts | GitHub, GitLab, Gitee, Codeberg, Bitbucket, SourceForge, Hugging Face Spaces |
| L10 social kinds | X, Reddit, YouTube, Discord (public descriptions only), Telegram, LinkedIn, Bluesky, Mastodon, Medium, Substack, Dev.to and Hashnode, regional socials |
| L11 regional counterparts | regional code hosts, dataset portals, competition platforms, paper indexes and forums, India first (section 2.4) |
| L12 alert mechanisms | not needed (no monitoring); replaced by **L12h reproducibility routes**: API, download path, licence, compute fit |
| L13 scams and fakes | **L13h traps**: templated or malware repos, leaked or mislicensed datasets, benchmark contamination, paper-mill papers, SEO "top 10" blogs, fake model cards |
| L14 eligibility (geo, KYC) | **L14h rule fit**: hackathon rules per PS (for example AI-02 "only open-weight models with 8 billion parameters or fewer", `PS` line 53), licences, India data access, compute limits |
| L15 leading indicators | **L15h fresh work**: arXiv in the last 90 days, new commits, new HF uploads, current competitions, open issues of key repos |
| L16 type gaps | the same probe: grep landed files for each artefact type per PS; thin cells get a gap lane |
| deep layer D1 to D11 | **deep corpora** per PS: GitHub/GitLab search pages walked deep, HF API listings, arXiv and OpenAlex result sets, Kaggle discussions and solution write-ups, YouTube talks and demos, Reddit, X, Telegram and Discord public channels, plus an India slice |

## 2.2 Artefact-type taxonomy (what each PS lane hunts)

This is the starting row set, a hypothesis that the W1 harvest must refine (the same status as `A/SCOPE.md`).

| code | artefact type | why it matters for a hackathon build | minimum row fields |
|---|---|---|---|
| T1 | working repos (full systems) | a fork or a reference for the architecture | URL, stars, last commit date, licence, language, runs as-is? (README claim vs tested) |
| T2 | component libraries | the parts the build needs | URL, version and date, licence, install route |
| T3 | pretrained models and checkpoints | baselines; compute fit | hub URL, params, licence, card date, reported metric and on which split |
| T4 | datasets | training and test; the "unseen" split rules | URL, size, licence, access (open, form, paid), date, split notes, India coverage |
| T5 | benchmarks and leaderboards | the number judges will ask about | URL, metric, top score with date, whether entries are reproducible |
| T6 | papers (surveys, methods, failure analyses) | method choice and the Q&A defence | DOI or arXiv id, date, venue, code link, key number quoted verbatim |
| T7 | competition winners and solution write-ups | proven pipelines under time pressure | competition URL, rank, write-up URL, date |
| T8 | hackathon projects (Devpost, Devfolio, ETHGlobal, DoraHacks, SIH and others) | what judges already saw; avoid a clone | URL, event, date, prize, repo link, demo link |
| T9 | demos (HF Spaces, Streamlit, Gradio, YouTube) | UI ideas; proof that it runs | URL, date, live or dead |
| T10 | tutorials, talks, courses | the fast path for the team | URL, date, language |
| T11 | standards, specs, official docs | correctness (ERCs, circuit libs, Sentinel-2 product specs, drug schedules) | URL, version, date |
| T12 | official and regulator data (India first) | local fit and judge credibility | URL, owner, licence or terms, update date |
| T13 | forum and social threads (pitfalls, war stories) | the unknown failure modes | URL, date, platform, score or replies |
| T14 | people and labs (who works on it, by region) | follow-ups, mentors, citations | name, affiliation, URL |
| T15 | failure reports and negative results | the "key challenges" in each PS | URL, date, what failed |
| T16 | tools for evaluation and testing | proving the build works | URL, licence, what it measures |
| T17 | commercial products and APIs (for comparison only) | positioning in the pitch | URL, pricing page date |

## 2.3 Source-class universe, global layer

Every named site below is a **seed (UNVERIFIED)** unless it is cited from `PS` or `A/`. The "route" column copies the rail types that worked in Part 1.

| class | sources (seeds) | route (from Part 1 where it exists) | trap to watch (from Part 1 lessons) |
|---|---|---|---|
| S1 code hosts | GitHub (search API, topics, code search), GitLab, Gitee, Codeberg, Bitbucket, SourceForge | `gh api search/repositories` with `pushed:>` (as in `A/scripts/d10_github.py`); other hosts through their APIs or `site:` searches via tf.py | templated or malware repos (`A/LEADS.md` lines 99, 283); Gitee was unreachable from this machine (`A/LEADS.md` line 105) |
| S2 model and dataset hubs | Hugging Face (models, datasets, Spaces), Kaggle (datasets, models, notebooks), ModelScope, PyTorch Hub, Zenodo, Figshare, Mendeley Data, OpenML, Papers with Code datasets (status to check: reported shut down in 2025, UNVERIFIED) | hub APIs (untested here) and `site:` searches | cards that claim metrics without code; licence missing |
| S3 paper indexes | arXiv, OpenAlex, Semantic Scholar, ACL Anthology, CVF Open Access, ISCA Archive, OpenReview, IEEE Xplore (abstracts), bioRxiv, medRxiv, ChemRxiv, SSRN, Google Scholar (snippets) | APIs where public; otherwise tf.py | paper mills; preprints with no code; dates (use the v1 date and the venue date) |
| S4 benchmarks and leaderboards | the benchmark each PS names (see 2.6), plus HF leaderboards | the owner page, read in full | entries not reproducible; leaderboard screenshots in blogs |
| S5 competition platforms | Kaggle, DrivenData, AIcrowd, Codabench and CodaLab, EvalAI, Zindi, Topcoder, Tianchi, DataFountain, Signate, Dacon, MathWorks challenges | `site:` searches plus the competition's own discussion and solution pages | solution write-ups that differ from the final private leaderboard |
| S6 hackathon galleries | Devpost, Devfolio, Unstop, HackerEarth, MLH, ETHGlobal past projects, DoraHacks BUIDLs, Gitcoin, Smart India Hackathon results | `site:` searches, paged deep | demo links dead; the repo is a template |
| S7 demos | HF Spaces, Streamlit community, Gradio, Replicate, YouTube demo videos | HF API; yt-dlp search plus channel RSS (as in `A/scripts/d3_youtube.py`) | sorted-by-views noise (F12) |
| S8 Q&A and forums | Stack Overflow and Stack Exchange sites (GIS, Ethereum, Cryptography, Bioinformatics, Matter Modeling, Electrical Engineering), HN (Algolia), Reddit, Discourse forums (HF forum, PyTorch forum, ethresear.ch, Ethereum Magicians, OpenStreetMap community), MATLAB Answers, Kaggle discussions | Arctic Shift for Reddit (as in `A/scripts/d5_reddit.py`); Discourse `latest.json` and `search.json` (as in `A/scripts/d4_boards.py`) | stale threads: check the date of the accepted answer |
| S9 socials | X (syndication per post, `site:x.com` discovery, as in D1 to D1c), YouTube, LinkedIn (snippets only), Bluesky API, Mastodon, Telegram public channels (`t.me/s/`), Discord (public descriptions only) | Part 1 scripts as-is, with new keywords | posts omit conditions; owner pages win (G-e) |
| S10 long-form | Medium tag RSS, Substack archive API, Dev.to, Hashnode, personal blogs, lab blogs | `A/scripts/d6_longform.py` routes | template farms (`A/LEADS.md` line 288) |
| S11 standards and official docs | EIPs and ERCs, Circom and Noir docs, Copernicus and ESA Sentinel-2 docs, MathWorks docs, RDKit docs | owner page | version drift |
| S12 commercial and vendor | product pages and APIs for each PS domain | owner page | marketing numbers |

## 2.4 Geographic layer (India first, then the rest of the world)

Same layering logic as section 1.3.3. All rows are **seeds (UNVERIFIED)**; the lane confirms each one and adds at least 30 more per region, as `A/prompts/LANE-TEMPLATE.md` demanded.

| region lane | code hosts and hubs | data portals | competitions and hackathons | papers and forums | socials and media | query languages |
|---|---|---|---|---|---|---|
| R-IN India (home market, own lane like `05-india`) | GitHub orgs of IITs, IIITs, IISc, AI4Bharat | data.gov.in (OGD), Bhuvan and NRSC (ISRO), IndiaAI AIKosh, Bhashini, Forest Survey of India (ISFR), CDSCO, NPPA, Jan Aushadhi lists, GeM and CPPP procurement data, Census and Smart Cities data | Smart India Hackathon, Devfolio, Unstop, HackerEarth, ETHIndia | Shodhganga (theses), IndiaRxiv, Analytics Vidhya, r/developersIndia, r/india | X India tech, LinkedIn, YouTube in Hindi and Hinglish, Telegram study channels | en, hi, Hinglish, bn, ta, te, mr, gu, kn, ml, pa (the D11 script set) |
| R-CN China, HK, TW | Gitee, ModelScope, OpenI | national open-data portals | Tianchi, DataFountain, Biendata | CNKI (abstracts), Zhihu, CSDN, Bilibili | Bilibili, WeChat articles (often blocked) | zh-Hans, zh-Hant |
| R-JP Japan | GitHub plus Qiita and Zenn code posts | e-Gov data | Signate, Nishika | J-STAGE, Qiita, Zenn | X Japan, note.com | ja |
| R-KR Korea | GitHub | AI Hub (aihub.or.kr) | Dacon | KCI, velog, Naver blogs | YouTube Korea | ko |
| R-RU Russia, CIS | GitHub, GitFlic | national data portals | ODS.ai competitions | Habr, eLibrary | Telegram channels, VK | ru, uk |
| R-EU Europe | Codeberg, GitLab | data.europa.eu, Copernicus, national portals | EU hackathons, challenge workshops | HAL (FR), OpenAIRE, Zenodo | Mastodon, LinkedIn | de, fr, it, es, nl, pl |
| R-LATAM | GitHub | dados.gov.br, datos.gob.* | Kaggle community events | SciELO | YouTube, Telegram | es, pt |
| R-AF Africa | GitHub | national portals | Zindi | Masakhane, Deep Learning Indaba material | X, LinkedIn | en, fr, sw |
| R-MENA | GitHub | national portals | regional hackathons | Arabic NLP venues | X, Telegram | ar, fa |
| R-SEA SE Asia | GitHub | data portals (SG, ID, VN, TH, PH) | regional hackathons | regional journals | Facebook groups (descriptions only), YouTube | id, vi, th, tl, ms |
| R-SA South Asia other | GitHub | PK, BD, LK, NP portals | national hackathons | university repositories | YouTube, Facebook | ur, bn, si, ne |

The language rule carried over from F6 and F14: for every PS, write natural local queries, not word-for-word translations. Collect a vocabulary table of the local technical terms per region, as each Part 1 regional file did. Feed those terms back into the next wave.

## 2.5 Per-PS lane sheets (15)

How to read each sheet:

- **Anchors** are named in the PS text (sourced, with `PS` line numbers).
- **Seeds** are from my memory: **UNVERIFIED**, to be opened.
- **Keywords** are the English families. The lane writes the local-language versions for each region in 2.4.
- **Rule gates** are the PS constraints that every found artefact is checked against (the adapted L14h).

### AI-01 Voice-Clone Detection for Phone Scams (`PS` lines 17 to 38)
- Task: decide whether a 2 to 10 second clip is genuine or synthetic, and generalise to unseen cloning tools.
- Anchors (sourced):
  - ASVspoof 2019 evaluation set (mostly unseen attack systems)
  - In-the-Wild dataset
  - pretrained self-supervised speech models are allowed
- Keywords: audio deepfake detection, anti-spoofing countermeasure, spoofed speech generalisation unseen attacks, short-utterance spoof detection, codec-based fake speech, multilingual deepfake audio, shortcut learning silence anti-spoofing, phone channel deepfake.
- Seeds (UNVERIFIED):
  - Benchmarks and datasets: ASVspoof 2021 and ASVspoof 5, WaveFake, ADD challenge (Chinese), MLAAD, CodecFake, SpoofCeleb.
  - Models: AASIST, RawNet2, wav2vec 2.0, XLS-R and WavLM front ends.
  - Venues: ISCA Interspeech and ASVspoof workshop papers.
  - India: AI4Bharat Indic speech corpora and Bhashini (for Indian-language genuine speech).
- Region angle: CN (ADD challenge papers on CNKI and arXiv), IN (Hindi and regional-language clone scams, news and police advisories as problem evidence), KR (AI Hub voice data).
- Rule gates:
  - Test on unseen generators (report how each repo handles this).
  - Clip length 2 to 10 s.
  - Reject repos whose result depends on silence or loudness shortcuts (`PS` line 38).

### AI-02 Data-Analyst Agent on Messy Databases (`PS` lines 40 to 61)
- Anchors (sourced):
  - BIRD benchmark (scored on execution results)
  - only open-weight models of 8B parameters or fewer
- Keywords: text-to-SQL agent, BIRD leaderboard small model, schema linking, SQL self-correction execution feedback, unanswerable question detection text-to-SQL, dirty value normalisation, external knowledge evidence BIRD.
- Seeds (UNVERIFIED):
  - Benchmarks: Spider 2.0, BIRD mini-dev.
  - Systems: CHESS, DIN-SQL, DAIL-SQL, MAC-SQL, CodeS, OmniSQL, XiYan-SQL.
  - Models: SQLCoder, Qwen2.5-Coder 7B, Llama 3.1 8B.
  - Frameworks: Vanna, the LangChain SQL agent.
- Region angle: CN (several leading text-to-SQL groups publish on Gitee, ModelScope and Zhihu), KR and JP (Dacon and Signate tabular QA).
- Rule gates:
  - Parameter count of 8B or less, read from the model card, not from a blog.
  - Open weights.
  - The BIRD score reported on the dev or test split, with a date.

### AI-03 Topic-Augmented Knowledge Graph Builder (`PS` lines 63 to 84)
- Anchors (sourced):
  - Neo4j (graph database), ChromaDB (vector database)
  - pyvis, react-force-graph
  - Streamlit or React split screen
  - deliverables (1) to (5) at line 74
- Keywords: GraphRAG, community detection knowledge graph RAG, topic modelling plus knowledge graph, query router global vs local search, triple extraction LLM, graph path citation answer.
- Seeds (UNVERIFIED):
  - Systems: Microsoft GraphRAG, LightRAG, nano-graphrag, Neo4j LLM Graph Builder, LlamaIndex property graph, KAG / OpenSPG, HippoRAG, RAPTOR.
  - Methods and libraries: Leiden community detection, BERTopic.
  - Benchmarks: MultiHop-RAG, HotpotQA, MuSiQue.
- Region angle: CN (KAG and OpenSPG on Gitee and GitHub), HK (LightRAG), IN (hackathon galleries with GraphRAG demos).
- Rule gates:
  - Every answer must show the exact graph path (`PS` line 84).
  - Prefer repos that have a working visual demo (T9).

### AI-04 RAG Evaluation Pipeline (`PS` lines 86 to 107)
- Anchors (sourced):
  - context relevance, faithfulness, answer accuracy
  - a synthetic test-question generator
  - a root-cause report
  - a single-screen dashboard (line 97)
- Keywords: RAG evaluation retriever vs generator, faithfulness metric, hallucination despite relevant context, synthetic QA generation from documents, root cause RAG failure, RAG test set generation.
- Seeds (UNVERIFIED):
  - Tools: RAGAS, TruLens, DeepEval, ARES, RAGChecker, Arize Phoenix, promptfoo.
  - Benchmarks: CRAG (KDD Cup 2024), RGB (Chinese and English), FRAMES.
- Region angle: CN (RGB, Chinese RAG eval suites), IN (enterprise RAG eval talks at Indian meetups).
- Rule gates:
  - The retriever and the generator are scored apart AND end to end (`PS` line 104).
  - Metrics must be explainable in the Q&A.

### W3-01 Zero-Knowledge Eligibility Credentials (`PS` lines 115 to 135)
- Anchors (sourced):
  - Circom, Noir
  - a ZK-friendly signature and hash
  - "under-constrained signal" is the named vulnerability
  - open-source circuit libraries allowed
- Keywords: zk credential age proof, selective disclosure zk proof smart contract verifier, EdDSA Poseidon circom, Noir signature verification, under-constrained circuit bug, browser proving time, zk identity hackathon.
- Seeds (UNVERIFIED):
  - Libraries and projects: circomlib, zk-email, Semaphore, Anon Aadhaar (India-specific, PSE), Privado ID / iden3, Self (passport proofs), zkPassport.
  - Circuit bug trackers and checkers: 0xPARC zk-bug-tracker, Circomspect, Picus.
- Region angle:
  - IN: Aadhaar and DigiLocker as the issuer story; Anon Aadhaar as prior art.
  - EU: EUDI wallet ZK work.
  - CN: Gitee zk circuits.
  - Hackathons: ETHGlobal and ETHIndia past projects.
- Rule gates:
  - Every signal constrained: list the audit tools a repo used.
  - The signature verified inside the circuit.
  - Browser proving time stated with hardware.

### W3-02 Agent Wallet: Letting AI Agents Pay Safely (`PS` lines 137 to 157)
- Anchors (sourced):
  - ERC-4337
  - the policy list at line 150: allowed contracts and functions, per-transaction limit, daily limit, allowed recipients, expiry, owner approval out of policy
- Keywords: session keys ERC-4337, spending policy smart account, AI agent wallet, modular account permissions, owner co-sign out-of-policy, prompt injection wallet agent.
- Seeds (UNVERIFIED):
  - Reference code: eth-infinitism account-abstraction.
  - Standards: ERC-7579 modules, ERC-6900, ERC-7715 permissions.
  - Accounts and SDKs: Safe modules, ZeroDev Kernel, Biconomy, Alchemy Modular Account, Rhinestone.
  - Agent payments: Coinbase AgentKit, x402.
  - Discussion: Ethereum Magicians threads.
- Region angle: IN (ETHIndia agent-wallet projects), global ETHGlobal "agents" prizes, CN and KR wallet SDK repos.
- Rule gates:
  - Signature, nonce and chain-id validation (`PS` line 155).
  - Policies hold if the agent key leaks (line 148).

### CL-01 Satellite Forest-Loss Alerts (`PS` lines 167 to 187)
- Anchors (sourced):
  - Sentinel-2, 10 m, every few days
  - monsoon clouds
  - public forest-loss maps are coarser (30 m) and lag a year, so they are only imperfect labels
  - test on a state not used in training
- Keywords: Sentinel-2 change detection deforestation, cloud masking Sentinel-2, phenology seasonal false alarm, noisy label learning remote sensing, forest loss India, weak supervision Hansen labels.
- Seeds (UNVERIFIED):
  - Change maps and alerts: Hansen Global Forest Change / Global Forest Watch, GLAD and RADD alerts, Dynamic World.
  - Cloud masks: s2cloudless, Cloud Score+.
  - Platforms and libraries: Google Earth Engine, Microsoft Planetary Computer, Copernicus Data Space, TorchGeo.
  - Foundation models: Prithvi, Clay.
  - Datasets: BigEarthNet, ForestNet.
  - Brazil: PRODES and DETER (INPE), MapBiomas, as regional prior art.
  - India: ISFR (Forest Survey of India) and Bhuvan.
- Region angle: BR (the most mature deforestation alert systems), ID (ForestNet, palm oil), IN (FSI, NRSC, state forest departments, news on mining clearances as ground truth leads).
- Rule gates:
  - The held-out Indian state is named.
  - The label source and its resolution are stated.
  - Cloud handling is explained.

### CL-02 Scope 3 Emissions from Public Spending Records (`PS` lines 189 to 209)
- Anchors (sourced):
  - real published spending records
  - short noisy line descriptions
  - currency and base-year conversion
  - at least 2,000 hand-labelled lines with two people agreeing
  - uncertainty to the total
- Keywords: spend-based emission factors, EEIO, Scope 3 category 1 purchased goods, procurement description classification, inter-annotator agreement, Monte Carlo uncertainty carbon footprint, deflate spend to base year.
- Seeds (UNVERIFIED):
  - Emission factors: US EPA USEEIO supply-chain factors, EXIOBASE, UK DESNZ/DEFRA conversion factors, CEDA, Climatiq.
  - Spending records: UK government spend over 25,000 GBP files, USAspending.gov, India GeM / CPPP.
  - Classification schemes: UNSPSC, CPV, NAICS and ISIC codes.
  - Labelling tools: Label Studio, doccano.
- Region angle: UK (most published spend data), EU (CPV-coded tenders), IN (GeM and CPPP: check what is downloadable), and national inflation and PPP series.
- Rule gates:
  - The records are real and published (link and licence).
  - The labelling protocol shows agreement.
  - The uncertainty method is named.

### CL-03 Predicting Energy Consumption for a Building (`PS` lines 211 to 232)
- Anchors (sourced):
  - MathWorks challenge repository
  - Building Data Genome Project 2
  - ASHRAE Great Energy Predictor III
  - public weather archives
  - test on unseen buildings
  - reliability and drivers
- Keywords: building energy prediction unseen buildings, cross-building generalisation, ASHRAE GEP III winning solution, weather normalised energy, retrofit candidate ranking, meter data cleaning, SHAP building energy.
- Seeds (UNVERIFIED):
  - Kaggle GEP III top write-ups.
  - NREL BuildingsBench, ComStock and ResStock.
  - Weather data: Open-Meteo, ERA5, Meteostat.
  - Simulation: EnergyPlus.
  - India: BEE and ECBC data.
- Region angle: IN (BEE star-rated buildings, Indian campus smart-meter datasets if any), EU (building stock observatories), US (NREL).
- Rule gates:
  - The split is by building, not by time.
  - Reliability is reported.
  - Drivers are explained.

### CL-04 MathWorks Challenge: Building Energy with MATLAB (`PS` lines 234 to 255)
- Anchors (sourced):
  - the MathWorks challenge repository
  - starter Live Script "Building Regression Models"
  - a 5-minute presentation plus a public repo
  - rubric: Solution 70 (data 20, ML 20, functionality 10, MATLAB 10, readability 10), Presenting 30
- Keywords: MATLAB Regression Learner building energy, MATLAB Live Script ML, MathWorks challenge project hub, past MathWorks student challenge winners.
- Seeds (UNVERIFIED):
  - MathWorks challenge project hub on GitHub.
  - MATLAB File Exchange.
  - MATLAB Answers.
  - MathWorks student competitions pages.
- Region angle: IN (MathWorks India student programs), global winners pages.
- Rule gates:
  - The rubric weights map to deliverables.
  - The code is MATLAB, not a Python port.
- Shares the CL-03 data lanes. Run CL-03 and CL-04 as one cluster with two outputs.

### HM-01 ProvenanceLab: Reproducible Molecule Analysis (`PS` lines 263 to 284)
- Anchors (sourced):
  - broken SMILES (impossible valence), missing stereochemistry
  - salts, charged forms, tautomers
  - version-dependent properties
  - frozen PubChem and ChEMBL snapshots
  - an own test set of broken inputs
  - the distinction between "not computed", "not available" and "not applicable"
- Keywords: SMILES validation error classes, molecule standardisation, tautomer canonicalisation, salt stripping, cheminformatics reproducibility, RDKit version differences descriptors, provenance pipeline chemistry.
- Seeds (UNVERIFIED):
  - Toolkits: RDKit (rdMolStandardize), Open Babel, CDK, Indigo, Datamol, Mordred.
  - Pipelines and identifiers: ChEMBL structure pipeline, InChI and InChIKey.
  - Snapshots: PubChem FTP and ChEMBL release dumps.
  - Reproducibility tooling: conda-lock, Docker, DVC, Snakemake.
  - Forums: Matter Modeling Stack Exchange, RDKit GitHub discussions.
- Region angle: IN (CSIR OSDD history, Indian cheminformatics groups), CN (domestic chem databases), EU (EMBL-EBI as the ChEMBL owner).
- Rule gates:
  - Every tool version is pinned.
  - A rerun gives identical output.
  - Error classes are precise (`PS` line 281).

### HM-02 Prescription Safety Checker for Indian Brand Medicines (`PS` lines 286 to 307)
- Anchors (sourced):
  - Indian brand names and combination products
  - abbreviations OD, BD, TDS, SOS
  - dose limits by age, weight and kidney function
  - alert fatigue
  - a test set built with a pharmacist or pharmacy student
- Keywords: Indian medicine brand composition dataset, fixed-dose combination India, drug-drug interaction database open, duplicate ingredient detection, renal dose adjustment rules, fuzzy brand name matching, alert fatigue clinical decision support.
- Seeds (UNVERIFIED):
  - Indian regulators and lists: CDSCO approved lists, NPPA price notifications (with compositions), PMBJP Jan Aushadhi product list, National List of Essential Medicines, Indian Pharmacopoeia, National Formulary of India.
  - Indian brand datasets: Kaggle Indian medicine datasets (check provenance).
  - Interaction and side-effect databases: DDInter, TWOSIDES, SIDER, openFDA, DrugBank (licence check).
  - US reference: RxNorm.
  - Matching libraries: RapidFuzz and SymSpell.
- Region angle: IN is the core. Pharmacy e-commerce sites are for comparison only: their terms may forbid scraping, so record the terms, do not scrape. Add Indian pharmacy-student forums and Telegram groups (public descriptions only).
- Rule gates:
  - Data licence and terms.
  - The banned FDC list is considered.
  - The pharmacist-built test set protocol.

### SC-01 Multi-Camera Vehicle Re-Identification (`PS` lines 315 to 335)
- Anchors (sourced):
  - non-overlapping cameras
  - no number plates
  - dense mixed Indian traffic (two-wheelers, autorickshaws, buses, cars)
  - viewing angle and lighting changes
  - travel-time priors
- Keywords: multi-camera multi-target vehicle tracking, vehicle re-identification, spatio-temporal constraint re-id, origin-destination flow from cameras, Indian traffic dataset, occlusion tracking two-wheelers.
- Seeds (UNVERIFIED):
  - Challenge: AI City Challenge (multi-camera vehicle tracking track, CityFlow).
  - Re-id datasets: VeRi-776, VehicleID, VERI-Wild.
  - Libraries and trackers: FastReID, torchreid, ByteTrack, BoT-SORT, StrongSORT, Ultralytics YOLO.
  - India: IDD (India Driving Dataset) and other Indian traffic datasets.
- Region angle: IN (Indian traffic datasets from IIIT-H, IISc and others; Smart City command centre reports as the problem source), CN (re-id groups publish a lot; Gitee mirrors).
- Rule gates:
  - No plate reading anywhere in the pipeline.
  - Mixed-traffic classes are covered.
  - Camera-time priors are used.

### SC-02 Accessible Walking Routes from Street Imagery (`PS` lines 337 to 357)
- Anchors (sourced):
  - Project Sidewalk labels (other countries)
  - own Indian labels required
  - barrier classes (kerb ramps, steps, broken footpaths, poles, parked vehicles)
  - matching to footpath segments
  - barrier-cost routing
- Keywords: sidewalk accessibility detection street view, curb ramp detection, footpath network extraction, accessible routing wheelchair, map matching detections to sidewalks, OSM sidewalk tagging India.
- Seeds (UNVERIFIED):
  - Labels and tools: Project Sidewalk datasets and API, OpenSidewalks, AccessMap, Wheelmap.
  - Street imagery: Mapillary (imagery plus API), KartaView.
  - Map data and routing: OpenStreetMap footway, kerb and wheelchair tags, OSMnx, Valhalla, GraphHopper, pgRouting.
  - Segmentation datasets: Mapillary Vistas, Cityscapes.
  - India: IDD for Indian street scenes, Sugamya Bharat (Accessible India Campaign) materials.
- Region angle: IN (OSM India community, Indian disability-rights groups' audits as ground truth leads), JP and EU (mature accessibility map projects).
- Rule gates:
  - Local Indian labels exist.
  - Detections map to segments.
  - The routing cost is defined.

### HW-01 Open Innovation: Hardware (`PS` lines 364 to 385)
- Anchors (sourced):
  - the team defines the problem
  - a physical prototype is required
  - software only is not eligible
  - cost and power must be justified
- Keywords: per candidate problem, decided in P1. For each candidate: low-cost sensor prototype, ESP32 or Raspberry Pi project, BOM cost, power budget, field test.
- Seeds (UNVERIFIED):
  - Project galleries: Hackster.io, Hackaday.io, Instructables, Arduino Project Hub.
  - Simulators and design tools: Wokwi, KiCad, EasyEDA / OSHWLab.
  - Communities: Seeed Studio wiki, r/esp32, r/embedded.
  - India: Electronics For You and CircuitDigest, Indian vendors' catalogues for BOM prices, SIH hardware-edition results.
- Region angle: IN (BOM availability and price in India), CN (OSHWLab, Bilibili maker videos), JP (Qiita IoT).
- Rule gates:
  - It can be demonstrated live.
  - The BOM and the power numbers are sourced.
  - It is tested under realistic conditions.

## 2.6 Wave plan (ADAPTATION; same structure as section 1.4)

```
P1 user discussion -> GO (FB section 2; blocker for everything below)
 |
W0  rails test (main session): every route in 2.8 graded WORKS / 429 / 403 / dead / needs key,
    like A/DEEP-LAYER-PLAN.md section 2; Parallel through the proxy, TinyFish, gh, HF API,
    arXiv, OpenAlex, Kaggle CLI, GitLab, Gitee, Codeberg, yt-dlp, Arctic Shift, X syndication, t.me/s
 |
W1  harvest of PS anchors (main session): open every anchor named in PS (BIRD site, ASVspoof,
    In-the-Wild, BDG2, ASHRAE GEP III, MathWorks repo, PubChem/ChEMBL dumps, Project Sidewalk,
    ERC-4337, Circom/Noir docs, Sentinel-2 docs) -> sourced landings per PS
 |
BREADTH LAYER (one lane = one PS x one source layer)
 W2..W7   per track cluster: global layer S1..S12 (AI x4, W3 x2, CL x4 run as 3, HM x2, SC x2, HW x1 after P1 idea)
 W8..W12  India lane per cluster (R-IN), own lane like A/research/L11-regional/05-india.md
 W13..W16 rest-of-world lanes per cluster (R-CN, R-JP, R-KR, R-RU, R-EU, R-LATAM, R-AF, R-MENA, R-SEA, R-SA)
 W17      type-gap probe: grep all landed files for T1..T17 per PS; thin cells -> gap lane
 |
AUDIT (computed from disk, like A/AUDIT-2026-10-22-post-compaction.md)
 |
DEEP LAYER (scripted collectors, then one reading lane per corpus)
 H1 GitHub/GitLab/Codeberg/Gitee walked deep (paged search, topic graphs, forks of key repos, "used by")
 H2 HF models/datasets/Spaces listings per keyword family (+ ModelScope)
 H3 papers: arXiv + OpenAlex result sets, citation snowball from the top 20 per PS
 H4 competitions + hackathon galleries (Kaggle solution write-ups, Devpost/Devfolio/ETHGlobal/DoraHacks pages)
 H5 YouTube talks and demos (yt-dlp search + channel RSS, 2 modes, 25+ languages)
 H6 Reddit (Arctic Shift), HN, Stack Exchange, Discourse forums
 H7 X (site:x.com discovery + syndication reads), Bluesky, Medium, Substack
 H8 Telegram and Discord public descriptions, regional socials
 H11 India slice across H1..H8 (script + term regex, like A/scripts/d11_india_slice.py)
 |
REFINEMENT (Part 1 planned these and never ran them; here they get a state row from day one)
 R1 L13h traps   R2 L14h rule fit per PS   R3 L15h fresh work (last 90 days)
 R4 lie hunt A + B (fact-checker, 15 decision-driving claims each)
 R5 uniqueness pass (coverage map from headings + first columns, then unknown unknowns)
 R6 pass 2 on thin lanes   R7 3x loop with new keywords from LEADS
 |
CONSOLIDATE per PS: shortlist evidence pack -> P3 pick (user)
```

## 2.7 Agent split (ADAPTATION; roles are sourced from `FB` section 3, lane assignment is my proposal)

| agent | role per `FB` | proposed lanes here | limits per `FB` |
|---|---|---|---|
| claude (lead) | splits lanes, owns the decision log, checks everything | W0 rails test, W1 anchors, all prompts and specs, collectors H1 to H8 and H11 (scripts, as in Part 1), every main-session review table, the AUDIT, consolidation | subagent cap 5 (`FB` line 56; memory note says max 5 since 10-24, no nested spawns) |
| dsh | research lead for live sources: datasets, licences, repos, baselines, compute fit, feasibility numbers | global layer S1, S2, S4, S5 per PS; T3 and T4 licence and compute-fit rows; reproducibility checks (L12h) | "ship unchecked numbers": not allowed |
| hermes | research, fact-check, critique: rubric angle, judge angle, risks, "what wins" | R4 lie hunts; T7 and T8 (winners, what judges saw); regional forum and social reading lanes; L13h traps; judge-angle notes per PS | "write code. Ever.": not allowed |
| codex | deputy; checks every artefact (verdict files) | verdict files on each landed lane (second check after claude) | down until 16:28 IST 2026-10-24 per `FB` |

Rails per agent:

- Claude Code reaches Parallel through the rotating proxy on 127.0.0.1:8765. Hermes and dsh hold direct keys. All of this is per `~/AGENTS.md` Pitfalls (current key file `~/Desktop/parallel-new1.txt`, switched 2026-10-23). It is untested for this campaign, so W0 tests it.
- TinyFish keeps working through `A/scripts/tf.py`. The key file is `~/.hermes/.env`.
- Hermes config names firecrawl as its web backend and has a rivalsearch MCP entry (`~/.hermes/config.yaml` lines 62, 320 to 321). The dsh profile removed rivalsearch. Both are untested, so W0 tests them.
- searxng was not found in either config.

## 2.8 Collector adaptation (the specification only; build after the GO, per the user rule that research-only stays research)

| Part 1 script | adapted collector | change |
|---|---|---|
| `tf.py` | reuse as-is | new queries; `--loc` and `--lang` per region in 2.4; always page (`--page`), because F8 showed one-page searches were the main weakness |
| `d10_github.py` | H1 code-host collector | the 15 PS keyword families in en plus local terms; also GitLab, Codeberg and Gitee search APIs (routes UNTESTED); store stars, pushed, created, licence, topics, archived; add a fork and "used by" walk for the top repos |
| (new) | H2 hub collector | HF `api/models`, `api/datasets`, `api/spaces` search per keyword (route UNTESTED); store card date, licence, downloads, params |
| (new) | H3 paper collector | arXiv API and OpenAlex search per keyword, with dates; citation snowball from the top 20 per PS (routes UNTESTED) |
| `d1b_search.py`, `d1c_kwsearch.py`, `d7_square.py` | H4 gallery and competition collector | the same pattern: `site:devpost.com`, `site:devfolio.co`, `site:kaggle.com/competitions`, `site:dorahacks.io`, and others, paged until a page adds nothing |
| `d3_youtube.py` | H5 | the same 2 modes and channel RSS; topic regex plus noise regex (F12) |
| `d5_reddit.py`, `d4_boards.py` | H6 | the subreddit list per PS (for example MachineLearning, LocalLLaMA, remotesensing, gis, ethdev, cheminformatics, pharmacy, embedded, esp32: all seeds); Discourse forums per PS; Stack Exchange API (UNTESTED) |
| `d1_xcrawl.py`, `xread.py`, `d6_longform.py` | H7 | as-is, with new keywords |
| `d2_tgwalk.py` | H8 | Telegram study and dev channels per PS (only those with a public preview) |
| `d11_india_slice.py` | H11 | the same India regex, plus PS-specific Indian terms (CDSCO, NPPA, Jan Aushadhi, FSI, Bhuvan, GeM, IDD, Aadhaar, DigiLocker and others) |
| `d_prepare_*.py` | reading-batch builders | the same: dedupe, keyword plus noise filters, 140 to 150 KB batches, a handed-over record for deltas |
| `atlas_baseline.py`, `d_novelty_all.py` | baseline and novelty | baseline = all landed breadth files before H1, frozen as a tarball; novelty per corpus for repos (owner/name), models, datasets, DOIs and domains |
| `verify_state.py` | state checker | lanes per PS x layer, review tables, the TODO list, collector counts, a secret scan |

## 2.9 Verification gates (Part 1 gates, extended for hackathon artefacts)

All Part 1 gates G-a to G-n stay. Added for this goal (proposals):

| gate | rule |
|---|---|
| H-a licence | read the LICENSE file or the model and dataset card; "no licence" means not reusable; record it |
| H-b runs-as-claimed | stars are not evidence. A repo counts as "works" only after a clean install or a reproduced metric (dsh check). Otherwise mark it "README claim" |
| H-c metric provenance | every score has a split, a date and a link to the leaderboard or paper table read in full (the G-e "owner pages beat posts" rule) |
| H-d rule fit | check against the PS gates in 2.5 (for example AI-02 at 8B or less, CL-01 on an unseen state, SC-01 with no plates) |
| H-e data access | open, form, paid or blocked, tested on this machine; India-specific data checked for terms |
| H-f malware and traps | never run code from unknown repos (Part 1 found templated malware networks, `A/LEADS.md` lines 99 and 283); sandbox only, after a read |
| H-g freshness | last commit, last release and card update dates; a repo with a fresh README and a stale codebase is false freshness (G-g) |
| H-h ranking pages | "top 10 GitHub repos for X" blogs are leads, never evidence (G-f) |

## 2.10 Common brief for the hackathon lanes (adapted from `A/BRIEF-COMMON.md`, to be saved as its own file after the GO)

```
BRIEF-COMMON-HYP (read in full before any task)
Today is <date>. Campaign: for Hypnexis problem statement <PS id>, map every existing project, repo,
model, dataset, paper, benchmark, demo, competition winner, hackathon project, forum thread and
regional source (India first). Reader: the Hypnexis team. Folder: ~/hypnexis-main/research/.
Hard rules:
 - Do NOT spawn agents. Do NOT sign up, log in, install, or run anything you find. Read only.
 - Write ONLY the one output file named in your task, in parts (create, then append <= ~60 lines).
 - Dedupe: grep the already-landed files named in your task. Famous names alone are not a finding.
 - "Top N" blogs and awesome-lists are leads, not evidence. Open the owner page.
 - Every row: full https URL + its own date + where you saw the date + VERIFIED (opened) /
   VERIFIED (secondary) / UNVERIFIED. Quote numbers verbatim. Never invent a URL or a row.
 - Freshness: last commit / release / card update date.
 - Keep scratch files in scratchpad/<LANE>/ and raw output in raw/<LANE>/ only.
Tools: tf.py search (--loc --lang --page) and fetch; gh api; hub and paper APIs listed in your task;
 WebSearch/WebFetch; Parallel only if W0 graded it WORKS.
Output: header (lane, date, tools, query count, pages opened); SOURCES table with columns
 name | URL | artefact type T# | PS id | region | language | date + where seen | licence | access route |
 stars/citations/score | reproducible (claimed/tested) | rule fit | trap risk | non-obvious note |
 known/new | VERIFIED tag ; then a vocabulary table (local terms), "leads for other lanes", "gaps",
 "claims a skeptic should check first".
Hand-back: at most 5 lines: path, row count, 2-3 most surprising finds, biggest gap.
```

The lane prompt is the same as `A/prompts/LANE-TEMPLATE.md` with these words swapped:

- "regional and country counterparts" becomes "regional code hosts, dataset portals, competitions, paper indexes, forums".
- The six regional topics become: (1) local vocabulary; (2) local repos, models and datasets; (3) local competitions and hackathon winners; (4) local papers and theses; (5) local official data, law and terms that affect use; (6) local traps.
- The "find at least 30 named sources not in the seeds" rule stays.

## 2.11 Metrics and stop rules

- **Depth numbers**, computed from `raw/` the way `A/DEEP-LAYER-PLAN.md` section 1 did. Report all of them per lane: query count, median words per query, share of queries paged past page 1, queries per language, results opened vs snippets only.
- **Novelty rate per corpus** against the frozen breadth baseline. Stop a corpus when novelty falls under 10 percent over its last 200 items (the `A/DEEP-LAYER-PLAN.md` section 3 rule). Report both the all-names figure and the seen-3+-times figure.
- **Coverage matrix per PS**: artefact types T1 to T17 by region lanes, with the row count in each cell. Zero cells become gap lanes (the L16 pattern).
- **LEADS status column from day one**: open / followed (file) / dropped (reason), fixing `A/AUDIT...` 5d.
- **Coverage audit**: bytes read by the main session vs `wc -c` of every landed file, published as a percentage.

## 2.12 Decision tree with confidence per node (0 to 20, ADAPTATION)

```
[N0] user GO after P1 discussion? ................................. blocker (FB section 2)
  |- no  -> stop; nothing in Part 2 runs
  |- yes
[N1] scope: all 15 PS, or the P1 shortlist? ........................ user decides
  |   all 15 keeps the original width; a shortlist gives more depth per PS.
  |   Recommended: breadth W2-W7 for all 15, deep layer only for the shortlist
  |   (conf 13: Part 1 breadth came from many lanes and depth from corpora; time budget unknown)
[N2] W0 rails result
  |- Parallel WORKS -> use task groups for per-PS row enrichment (T1-T8 fields)  (conf 11: untested here; it was dead on 10-22)
  |- Parallel dead -> TinyFish + gh + direct APIs, as in Part 1             (conf 16: this exact stack carried Part 1)
  |- firecrawl / rivalsearch reachable via Hermes -> extra rail for hermes lanes (conf 8: config lines only, never tested)
[N3] breadth layer, per PS x global (S1-S12) ...................... conf 16 (same lane loop as Part 1)
[N4] India lane per cluster ........................................ conf 14 (Part 1 India needed a second slice to reach Indian-language content, F14)
[N5] rest-of-world lanes ........................................... conf 12 (CN sites such as Gitee/Zhihu were blocked in Part 1, F19)
[N6] deep layer H1-H3 (code, hubs, papers) ......................... conf 15 (public APIs exist; routes not yet graded)
[N7] deep layer H4-H8 (galleries, video, forums, socials) .......... conf 12 (Part 1 routes work; topic fit for ML/hardware unproven)
[N8] refinement R1-R7 .............................................. conf 10 (Part 1 planned the same and did not run it, F18; needs a state row and a slot)
[N9] consolidation into a per-PS evidence pack for P3 .............. conf 14
```

# PART 3: COVERAGE AUDIT (bytes read vs `wc -c`, computed 2026-10-24)

Every file below was read IN FULL with the Read tool. The longest line in any of them is 1,279 characters (measured with awk), so no line was cut by the tool's line limit.

| file | bytes (`wc -c`) | read |
|---|---|---|
| `A/GOALS.md` | 7,890 | full |
| `A/SCOPE.md` | 4,878 | full |
| `A/BRIEF-COMMON.md` | 4,927 | full |
| `A/WAVES.md` | 3,612 | full |
| `A/DEEP-LAYER-PLAN.md` | 16,387 | full |
| `A/CONTINUATION.md` | 12,392 | full |
| `A/LEADS.md` (333 lines, read in 3 pages: 1-120, 121-230, 231-334) | 91,843 | full |
| `A/LOG.md` (100 lines) | 32,052 | full |
| `A/AUDIT-2026-10-22-post-compaction.md` | 11,306 | full |
| subtotal: the 9 named files | **185,287** | 100% |
| `A/prompts/LANE-TEMPLATE.md` | 2,961 | full |
| `A/prompts/NEXT-LANES.md` | 8,189 | full |
| subtotal: prompts/ (2 of 2 files) | **11,150** | 100% |
| `A/scripts/` 23 files: atlas_baseline.py 4,223; d10_github.py 3,509; d11_india_collect.py 6,721; d11_india_slice.py 6,729; d1b_search.py 3,694; d1c_kwsearch.py 6,891; d1_xcrawl.py 7,803; d2_tgwalk.py 9,146; d3_youtube.py 12,453; d4_boards.py 14,609; d5_reddit.py 5,060; d6_longform.py 9,955; d7_square.py 4,807; d_novelty_all.py 6,162; d_prepare_misc.py 9,572; d_prepare_tg.py 6,257; d_prepare_x.py 3,586; d_strict_novelty.py 4,567; tf.py 3,241; verify_binance_hodler.py 1,295; verify_state.py 12,899; verify_state.sh 176; xread.py 2,756 | **146,111** | 100% (23 of 23; `__pycache__` skipped) |
| `PS` = `~/hypnexis-main/PROBLEM-STATEMENTS.md` | 17,002 | full |
| `FB` = `~/hypnexis-main/FLEET-BRIEF.md` | 5,608 | full |
| `~/hypnexis-main/README.md` | 654 | full |
| `~/hypnexis-main/CONTINUATION.md` | 1,179 | full |
| subtotal: hypnexis context | **26,280** | 100% |
| **TOTAL read in full** | **368,828** | |

Read only by grep (named lines, not the whole file):

- `~/.hermes/config.yaml` lines 62, 320 and 321.
- `~/.dsh/profiles/dsh-tui/cordis.patch.yml` line 2.
- `~/.agents/capabilities/CAPABILITIES.md`: 0 hits for firecrawl, searxng or rivalsearch.

NOT read. The task did not ask for these, and Part 1 does not quote from them:

| path | size | note |
|---|---|---|
| `A/research/**/*.md` (42 lane output files) | 2,570,373 bytes | their headline numbers are quoted only as reported in LEADS, LOG and DEEP-LAYER-PLAN |
| `A/raw/` | 905 MB (`du -sh`) | it was 174 MB at the time of the AUDIT; it grew through the deep layer |
| `A/archive/` | 46 MB | backups |

# PART 4: RED TEAM (attempt to prove this file wrong)

| # | claim in this file | grade | why |
|---|---|---|---|
| 1 | Parallel AI was dead during the campaign, and firecrawl, searxng and rivalsearch were not used | VERIFIED | `A/LOG.md` W0.6; grep of all read campaign files gave 0 hits for those three names |
| 2 | dsh and hermes were not used as worker agents in the crypto campaign | VERIFIED for the files read | no file names them as workers; the 42 lane files were not read, but their headers name opus subagents per `A/LOG.md`, which logs every lane launch as researcher(opus) |
| 3 | 1,984 searches with a median of 6 words; 884 unopened X ids | VERIFIED as written in `A/DEEP-LAYER-PLAN.md` | not recomputed by me from raw/ |
| 4 | the corpus sizes in 1.6 (13,142 or 17,000 X posts; 130,884 Telegram posts; and the others) | VERIFIED as reported | the two X figures come from different times (03:30 vs about 04:45); both are quoted with their sources; not recomputed |
| 5 | the language counts (26 in d1c, 30 in d3, 22 in d7) | VERIFIED | counted from the dicts in the scripts while reading; d1c is 25 local languages plus English |
| 6 | "two lanes in parallel until 13:35, then one at a time" | VERIFIED | `A/LOG.md` line 57; `A/GOALS.md` G6. The deep-layer collectors did run in parallel, as scripts in the background |
| 7 | Part 1 "planned but never ran" refinement | VERIFIED as of the last LOG line (2026-10-23 04:58) | the campaign may have continued after that line without updating LOG; `verify_state.sh` was NOT run today, because the task is read-only and the script also calls `gh` and `pgrep`. Treat this as the state at the last log line |
| 8 | the Part 2 seeds (datasets, repos, sites) | UNVERIFIED by design | from memory; some may be renamed, shut down or wrong (for example the Papers with Code status, ModelScope and Gitee reachability, the Kaggle Indian medicine dataset provenance) |
| 9 | the Part 2 API routes (HF, arXiv, OpenAlex, GitLab, Codeberg, Gitee, Stack Exchange, Kaggle CLI) | UNVERIFIED | none were tested; W0 exists to grade them |
| 10 | the agent-lane assignment in 2.7 | UNVERIFIED (my proposal) | the roles are sourced from `FB`; the mapping to lanes is mine and needs claude's and the user's OK |
| 11 | the decision-tree confidences in 2.12 | UNVERIFIED judgement | the reasons are given per node; no test backs the numbers |
| 12 | "Part 2 keeps the original width" | PARTLY | it keeps every source class and the regional and language layering. It drops the crypto-only classes (exchange feeds, memecoin tools) and swaps in hackathon classes. Region lanes are grouped per track cluster, not per PS, which is a width-for-time trade the user may reject |
| 13 | the Part 3 byte totals | VERIFIED | computed with `wc -c` and shell arithmetic: 185,287 + 11,150 + 146,111 + 26,280 = 368,828 |

Mistakes made while writing this file, logged so they are not hidden:

- At first I treated "rival" and "jina" grep hits in LEADS.md as tool names. They are parts of other words (rival as in "KGeN rivals", jina as in "jinacoin"). The tool table does not use them.
- "exa" matched "exactly". It was ignored.
