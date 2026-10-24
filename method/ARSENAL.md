# ARSENAL: tool map for the 4-agent fleet (claude, codex, dsh, hermes)

v1, written 2026-10-24 14:17 IST by a Claude Code subagent, read-only inventory. No key values or secrets in this file: paths and env var NAMES only.

Grades: VERIFIED = I ran a command or read the config today. UNVERIFIED = taken from a note or inferred, not tested today.

## 0. Freshness and sources

| source | state today | note |
|---|---|---|
| `~/.agents/capabilities/CAPABILITIES.md` | generated 2026-10-21 15:50 UTC, about 3 days old, STALE | not rebuilt (instruction). Its line "alive 0 of 412 keys" is about the retired file, ignore it |
| `re manifest` | run 2026-10-24 08:34 UTC | 15 domains, 135 actions, 41 components, 18 plugin tools, 17 python helpers (VERIFIED) |
| `re state` | first try hit a 200 s timeout with no output; second run took about 10 minutes, exit 0, but printed only the header (`recheck 2026-10-24T08:38:18Z`, `root /home/liebert511/re-arsenal`) and no ledger rows | no PASS/FAIL evidence today. Last full run is the one in CAPABILITIES.md 1d (10-21): 35 PASS, 0 FAIL, 1 deferred (gen.cuda), Detect It Easy broken. Rerun `bash ~/re-arsenal/scripts/recheck.sh` in a terminal to see rows |
| `parallel-keys status` (proxy) | run today | total 13, usable 13, alive 1, unknown 12, dead 0, current index 0, sessions search 2 / task 2 (VERIFIED) |
| harness configs | `~/.hermes/config.yaml`, `~/.hermes/.env` (names only), `~/.dsh/profiles/*/cordis.patch.yml` + `package.json`, `~/.dsh/.env` (names only), `~/.codex/config.toml`, `~/.claude.json` (MCP names only) | read today |

## 1. Tool table

| tool | what it does | claude | codex | dsh | hermes | how to call | evidence path |
|---|---|---|---|---|---|---|---|
| Parallel search MCP (`web_search`, `web_fetch`) | ranked web results with excerpts, page fetch | YES (via proxy) | NO MCP | YES, dsh-tui profile only | NO (row `enabled: false`) | claude: `mcp__parallel-search__web_search`; dsh-tui: `parallel-search` MCP row | `~/.claude.json` user mcpServers; `~/.dsh/profiles/dsh-tui/cordis.patch.yml`; `~/.hermes/config.yaml` mcp_servers.parallel-search |
| Parallel task MCP (`createDeepResearch`, `createTaskGroup`, `getStatus`, `getResultMarkdown`) | async deep research reports, batch enrichment of a list | YES (via proxy) | NO MCP | YES, dsh-tui only | YES (`enabled: true`) | claude: `mcp__parallel-task__createDeepResearch` then poll `getStatus`, fetch `getResultMarkdown` | same three files |
| Parallel REST scripts | ultra8x deep research, task groups, FindAll, Monitor, rotation, watcher | via Bash | via shell | via bash | via terminal | `python3 ~/parallel-ai-stack/scripts/parallel-deep-research.py "q" --processor ultra8x --name X`; `watcher.py`; `taskgroup-enrich.py`; `findall.py`; `psearch.py` (174 entries in scripts/) | `~/parallel-ai-stack/README.md`, `~/parallel-ai-stack/scripts/` |
| parallel-cli 0.7.1 | search, extract, research, enrich, findall, monitor from a shell | on PATH, NOT authenticated | same | same | same | needs `PARALLEL_API_KEY` in env or `parallel-cli login`; `parallel-cli auth` said "Not authenticated" today (VERIFIED) | `~/.local/bin/parallel-cli`, `uv tool list` |
| TinyFish | free search + fetch, credit-gated browser sessions, `tinyfish_agent` web agent | NO | NO | NO native (note says dsh reached it through the Hermes key over HTTP) | YES: plugin 0.2.2 enabled, `web.search_backend: tinyfish`, `web.extract_backend: tinyfish`, toolset `tinyfish` on cli and every gateway platform | hermes: built-in web search/extract tools route to tinyfish; `tinyfish_agent` tool | `~/.hermes/config.yaml` web + plugins.enabled + platform_toolsets; `~/.hermes/plugins/tinyfish/plugin.yaml`; env name `TINYFISH_API_KEY` in `~/.hermes/.env`; `~/fleet-log/research/platform-hunt/dsh/TOOLCHAIN.md` |
| Firecrawl | scrape, crawl, search | NO | NO | NO | config says `web.backend: firecrawl`, `use_gateway: true`; no `FIRECRAWL_API_KEY` name in `~/.hermes/.env` today | hermes web backend (route through gateway, UNVERIFIED whether live) | `~/.hermes/config.yaml` web; `~/parallel-ai-stack/README.md` (08-03: Firecrawl backend 402) |
| SearXNG (local) | meta search, `site:` queries over indexed platforms | via curl | via curl | via curl | YES (`SEARXNG_INSTANCE_URL`) | `curl 'http://127.0.0.1:8888/search?q=QUERY&format=json'` (answered 200 in 7.6 s today, VERIFIED) | `~/.hermes/.env` names; `~/fleet-log/research/platform-hunt/dsh/TOOLCHAIN.md` |
| RivalSearch MCP | 13 tools: web, social, news, github, scientific search, map_website | NO | NO | NO (removed on request) | YES (mcp_servers.rivalsearch) | hermes MCP tools; endpoint answered 405 to a plain GET today (normal for MCP POST endpoint, liveness UNVERIFIED) | `~/.hermes/config.yaml`; `~/fleet-log/research/platform-hunt/hermes/TOOLCHAIN.md` |
| context7 MCP | library docs lookup | NO | NO | NO | YES | hermes MCP | `~/.hermes/config.yaml` mcp_servers.context7 |
| camofox-browser | anti-detect Firefox (Camoufox) REST server for Cloudflare-class walls | NO | NO | NO | YES (`CAMOFOX_URL` points at localhost:9377) | start: `cd ~/camofox-browser; npm start` then `curl -X POST http://localhost:9377/tabs ...`; server DOWN today (curl 000) | `~/camofox-browser/README.md`; `~/.hermes/.env` names |
| Hermes cloud browser | browser automation, provider browser-use via gateway | NO | NO | NO | YES | hermes browser tools | `~/.hermes/config.yaml` browser |
| Codex browser + computer use | in-app browser, desktop control, node REPL | NO | YES (plugins browser, unified-computer-use, MCP node_repl) | NO | NO | inside Codex | `~/.codex/config.toml` |
| Claude in Chrome / built-in browser | drive a real browser tab | skill available, extension state UNVERIFIED | NO | NO | NO | Skill `claude-in-chrome` | Claude Code skill list |
| Built-in web search/fetch | plain search and page fetch | YES (WebSearch, WebFetch) | UNVERIFIED (not set in config.toml) | YES (`dsh-tool-web`, `dsh-web-search-deepseek`, `dsh-web-fetch-http`) | YES (`web` toolset, routed to tinyfish) | native tool | `~/.dsh/profiles/node_modules/` package names; `~/.hermes/config.yaml` |
| X search | X/Twitter search toolset | NO | NO | NO | YES (`x_search` in cli toolset) | hermes cli | `~/.hermes/config.yaml` platform_toolsets.cli |
| REA 6.7.0 (Ghidra 12.1.4, jadx, apktool) | 155 CLI commands / 207 MCP tools: binary, web bundle, Electron, adb capture, firmware | YES via Bash: `~/.agents/capabilities/bin/rea-claude <cmd> --token-limit N` | shell can run the same wrapper (UNVERIFIED from Codex) | YES, dsh-tui: `mcp__rea__*` (207) | YES: plugin `rea` enabled (172 tools on 10-19, UNVERIFIED today) | plain `rea` is NOT on PATH; use the wrapper | `~/.agents/capabilities/CAPABILITIES.md` 1, 1e; `~/re-arsenal/docs/FINDINGS-2026-10-21.md`; `~/.hermes/plugins/rea/` |
| dsh-ghidra bridge | Ghidra with write-back, 219 tools (6 at rest) | NO (Ghidra only through rea / `re static decompile`) | NO | YES, dsh-tui | NO | dsh `ghidra_status` etc. | `~/.dsh/profiles/dsh-tui/package.json`; INSTALL-QUEUE G7 |
| re-arsenal `re` | 15 domains, 135 actions: static, dynamic, symbolic, malware, firmware, mobile, game, artifact, web, data, ai, blockchain, style, media, gen; 14 playbooks | YES via Bash | shell, same binary (UNVERIFIED from Codex) | YES: `re_*` plugin tools (18) in dsh-tui | shell only (no re plugin in Hermes config) | `re <domain> <action> <target> [--json]`; `re playbook <job>`; `re manifest`; `re state` | `~/.local/bin/re`, `~/re-arsenal/docs/RESUME.md`, manifest output |
| `re style` / `re web` (hackathon-useful slice) | live-site tokens (`css`, `extract`), motion, fonts, slop linter; JS deobf, sourcemap, HAR, endpoint extraction, OpenAPI from HAR | YES | shell | YES | shell | e.g. `re style css <url>`, `re style slop <url>`, `re web urls <bundle.js>`, `re web openapi <har>` | `re manifest` |
| GitHub CLI `gh` | repos, issues, PRs, code search, releases | YES (Bash) | shell | YES (bash, per skill) | YES (terminal) | `gh search repos ...`, `gh api ...`; logged in as harshgounder (keyring) (VERIFIED) | `gh auth status`; `~/.dsh/skills/github/SKILL.md` |
| GitHub MCP (read-only) | repos, issues, pull_requests, users toolsets | NO | NO | YES, dsh-tui (`api.githubcopilot.com/mcp/`, env names `MCP_GITHUB_TOKEN`, `GITHUB_TOKEN`) | NO | `mcp__github__*` in dsh | `~/.dsh/profiles/dsh-tui/cordis.patch.yml` |
| GitHits connector | search, grep, read, diff public repos, package changelogs and vulns | YES (claude.ai connector) | NO | NO | NO | `mcp__claude_ai_GitHits__search` etc. | this session's tool list |
| Hugging Face CLI | model and dataset hub access | `hf` NOT on PATH; present at `~/re-arsenal/venv/bin/hf` and `huggingface-cli` | same path | same path | same path | `~/re-arsenal/venv/bin/hf ...`; no HF token env name in `~/.hermes/.env` or `~/.dsh/.env` (anonymous only) | `ls ~/re-arsenal/venv/bin` |
| Other CLIs (uv tools) | yt-dlp, twitter-cli, bilibili-cli, kaggle, maigret, wafw00f, markdown-new, litellm | any shell | any shell | any shell | any shell (`markdown_new` is also a Hermes toolset) | e.g. `yt-dlp --write-auto-subs --skip-download URL` | `uv tool list` |
| Claude subagents and skills | researcher, fact-checker, reviewer agents; research-campaign, hackathon, brainstorm, design-taste skills | YES | NO | NO | NO | Agent tool, Skill tool | `~/.claude/agents`, `~/.claude/skills` |

## 2. Parallel AI keys: file ~/Desktop/parallel-new1.txt; per-harness assignment

File: `~/Desktop/parallel-new1.txt`, 13 non-empty lines today (it had 7 on the morning of 10-23; mtime 2026-10-23 14:08 IST). The old `~/Desktop/parallel spams` file is retired. Line numbers below are 1-based and were matched by comparing values in a script that printed only the line number. "Memory #" is the 0-based numbering the memory note and `~/AGENTS.md` use (#1 = line 2).

| harness | route | env var NAMES | key line (memory #) | graded |
|---|---|---|---|---|
| claude | rotating proxy `127.0.0.1:8765` (`/search/mcp`, `/task/mcp`), systemd user unit `parallel-mcp-proxy`, `PARALLEL_KEYS_FILE` drop-in | none in Claude config, proxy reads the file | all 13 lines, starts at index 0 (line 1) | VERIFIED (`parallel-keys status`, unit file) |
| hermes | direct to `search.parallel.ai` / `task-mcp.parallel.ai` | `MCP_PARALLEL_SEARCH_API_KEY`, `PARALLEL_API_KEY` | line 2 (#1) | VERIFIED |
| hermes | direct | `MCP_PARALLEL_TASK_API_KEY` | line 3 (#2) | VERIFIED |
| hermes | extra for scripts | `PARALLEL_API_KEY_7`, `PARALLEL_API_KEY_8` | lines 6, 7 (#5, #6) | VERIFIED |
| dsh | direct, dsh-tui profile only | `MCP_PARALLEL_SEARCH_KEY`, `PARALLEL_SEARCH_KEY` | line 4 (#3) | VERIFIED |
| dsh | direct, dsh-tui profile only | `MCP_PARALLEL_TASK_KEY`, `PARALLEL_TASK_KEY` | line 5 (#4) | VERIFIED |
| codex / Command Code shells | fish universal vars (`~/.config/fish/fish_variables`) | `MCP_PARALLEL_TASK_API_KEY` | line 7 (#6) | VERIFIED |
| codex / Command Code shells | fish universal | `MCP_PARALLEL_SEARCH_API_KEY` | matches NO line in the new file and none in the retired file | VERIFIED mismatch, memory says it should be #5 (line 6) |
| nobody direct | only the proxy | none | lines 8 to 13 | VERIFIED |

Notes:
- Overlap: the proxy rotates through every line, including lines 2 to 7 that Hermes, dsh and the fish shells use directly. Two rotation states draw on the same credit (same drift the memory note recorded on 09-30).
- Hermes has only `parallel-task` enabled; its `parallel-search` MCP row is `enabled: false`, so Hermes searches through TinyFish.
- dsh fleet profiles (`fleet-coord`, `fleet-resa`, `fleet-resb`, `fleet-verify`, `fleet-team`, `headless`) do not mount the Parallel MCP rows; only `dsh-tui` does.
- Running processes keep the env they started with; a key change needs a harness restart (`~/AGENTS.md` Pitfalls).
- User rule: never tell the user the keys are dead. If a call fails, run `~/parallel-mcp-proxy/.venv/bin/parallel-keys rotate` and report that call's exact error. (`parallel-keys` is not on PATH; use the venv path.)

## 3. Gaps (tools a harness lacks)

| harness | lacks | cheapest route (needs GO where it touches config) |
|---|---|---|
| claude | TinyFish, RivalSearch, context7, camofox, GitHub MCP, Ghidra write-back | SearXNG and camofox are reachable by curl from Bash once running; `gh` and GitHits cover GitHub; TinyFish only through Hermes or its HTTP API (config or key use needs GO) |
| codex | any Parallel MCP; parallel-cli unauthenticated; TinyFish; RivalSearch; REA/`re` not tested from Codex | shell scripts in `~/parallel-ai-stack/scripts` read the keys file directly; fix the stale fish `MCP_PARALLEL_SEARCH_API_KEY` (GO needed) |
| dsh (fleet/headless profiles) | Parallel MCP, GitHub MCP, REA, `re_*`, Ghidra (all live only in `dsh-tui`) | run research lanes in the `dsh-tui` profile, or add the rows to fleet profiles (GO needed) |
| dsh (all profiles) | TinyFish, RivalSearch (removed on request), camofox | SearXNG by curl; built-in web tool |
| hermes | Parallel search MCP (disabled), GitHub MCP, Ghidra bridge, `re_*` plugin tools; camofox server down; Firecrawl key name absent | `re` and `gh` from the terminal; start camofox with `npm start` in `~/camofox-browser` (GO) |
| all four | `hf` on PATH, any HF token; Detect It Easy (broken by design); CUDA generation (deferred by user) | `~/re-arsenal/venv/bin/hf` anonymous |

## 4. The two sessions that built this arsenal

| | Claude Code session | dsh session |
|---|---|---|
| id | `95bef0e9-86cd-4543-914e-0ab27bcd1164` | `cea8a779-7f58-48b4-b108-492e0abfb49f` |
| transcript | `~/.claude/projects/-home-liebert511/95bef0e9-86cd-4543-914e-0ab27bcd1164.jsonl` (15.2 MB, 7,519 hits for re-universe/registry terms) | `~/.dsh/sessions/--home-liebert511--/cea8a779-7f58-48b4-b108-492e0abfb49f/session.v4.jsonl.zstd` (3.0 MB compressed, 3,376 events, 4,408 hits for re-arsenal/re-universe/rea-bundle) |
| span | first event 2026-10-21 04:13 UTC, file last written 2026-10-22 19:01 IST | created 2026-10-21 09:54 IST, last event 2026-10-24 10:57 IST |
| opening ask | "is there a claude rea pluggin? ... reverse engineer anything and its other forks" | "is there a dsh rea pluggin? ... the most modern the most complete a toolkit" |
| what it made | research roster `~/re-universe` (private repo), capability registry `~/.agents/capabilities/` (CAPABILITIES.md, INSTALL-QUEUE.md, build_registry.py, bin/rea-claude), `re-playbook` skill, memory entries `re-universe-campaign.md`, `capabilities-registry.md` | installed toolkit `~/re-arsenal` (`re` CLI, dsh plugin `dsh-re-arsenal`), REA bundle `~/.dsh/plugins/rea-bundle`, `dsh-plugin-rea` and `dsh-ghidra` in the dsh-tui profile, CPU generation stack |
| key findings | 21 lanes: 10 REVIEWED + 7 REVIEWED_LEGACY_FORMAT, 4 NOT_STARTED (R4c, R4d, R4e, T), 30 notes (`STATE-LEDGER.md`). Do not register REA MCP in Claude Code (about 195k tokens of schema per REA tracker #4027, no gain on small tasks), use `rea-claude`. WebFetch digests get numbers and dates wrong, read raw with `tools/audit/ctx.py`. Agents die on API timeouts, so register in `inflight.json` and save early. Status must be computed from files (`verify_state.sh`), never typed | REA 6.7.0 = 207 MCP tools, Ghidra 12.1.4, dsh-ghidra 219 tools; 40 components ready, Detect It Easy broken on purpose (needs ICU 66); `re` grew to 15 domains / 135 actions; `re style` transfer, lut, print, pixel, slop built after reading Claude's M1/M5 notes; CUDA torch deferred by the user; incident: a `DSH_*` line in `~/.dsh/.env` broke dsh launch for about ten hours, never put `DSH_*` in a .env; COVERAGE-vs-CLAUDE: RE side covered well, design side partial |
| read first | `~/re-universe/COMPACTION-HANDOFF.md`, `STATE-LEDGER.md`, `RESUME.md`; `bash ~/re-universe/tools/check/verify_state.sh` | `~/re-arsenal/docs/RESUME.md`, `FINDINGS-2026-10-21.md`, `GAP-MATRIX.md`, `COVERAGE-vs-CLAUDE.md`; `re manifest`, `re state` |

Related sibling work on the web-research rails (not the two sessions above): `~/fleet-log/days/2026-10-16.md` (TinyFish wiring, SearXNG, RivalSearch, REA plugin in Hermes) and `~/fleet-log/research/platform-hunt/{dsh,hermes}/TOOLCHAIN.md` (the reach ladder: direct, SearXNG `site:`, r.jina.ai, MCP scrapers, platform libraries, hosted unlockers, archives).

## 5. Red team of this file

| claim | grade | why |
|---|---|---|
| only Hermes has TinyFish wired | VERIFIED | plugin and toolsets in Hermes config; no tinyfish in dsh configs (grep), Codex config, or Claude MCP list |
| Codex has no Parallel MCP | VERIFIED for config.toml; Codex may still reach Parallel from its shell | |
| Codex native web search | UNVERIFIED | not in config, `codex features list` printed nothing |
| Hermes REA = 172 tools | UNVERIFIED | 10-19 note, not re-counted today |
| SearXNG up | VERIFIED 14:1x IST today | may stop later |
| camofox down | VERIFIED (curl 000 on 9377) | Hermes points at it anyway |
| `re state` all PASS | UNVERIFIED today | run exited 0 but printed no ledger rows |
| fish search key mismatch | VERIFIED | value matched neither file; cause unknown |
