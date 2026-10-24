# BUILD READINESS, hackathon night 2026-10-24 (deadline 06:00 IST 25 Oct)

read-only audit by Claude Code, 2026-10-24 ~14:30-14:45 IST. nothing installed, no logins, no config edits, no deploys.
only side effect: `tools/verify_state.sh` runs `git fetch` in the santioni repo (writes FETCH_HEAD) and rebuilds `lab/dist` via its "vite build" check.
grades: VERIFIED = command output or doc fetched this session; UNVERIFIED = estimate or memory.

## 0. one-screen verdict

```
static site ........ GitHub Pages via gh (ONLY authenticated deploy CLI) ............ [15/20]
                     needs a PUBLIC repo (Pages on private repos is a paid feature, UNVERIFIED)
ML demo ............ in-browser inference first (no backend to keep alive) ............ [14/20]
backend fallback ... user's PC + docker/uvicorn + tunnel ................................ [10/20]
                     BLOCKER: cloudflared and ngrok NOT installed (install needs GO)
deck ............... python-pptx 1.0.2 in ~/clause-engine/.venv + soffice for PDF ........ [17/20]
site kit ........... santioni kit 86/86 checks PASS today ................................ [17/20]
                     reskin = copy/VO/palette/beat content; 4-7 h estimate (UNVERIFIED)
```

## 1. santioni kit (~/site-clones/santioni)

### 1.1 verifier, run today (VERIFIED)

`bash tools/verify_state.sh` (full run, ~10 min) ended with:

```
PASS  vite build
PASS  test-agegate: 12/12 passed
PASS  test-hold: 11/11 passed
PASS  test-sound: 29/29 passed
PASS  test-resize: PASS no WebGL errors after resizes on the map and fog beats (0 errors, insets seen 3/3)
PASS  probe-story: 12/12 passed
PASS  test-carousel: 11/11 passed
PASS  test-tiers: 12/12 passed
PASS  inset-probe dpr 1 / dpr 2 / after a resize
PASS  swim-probe, test-longrun, retarget-probe
PASS  beats.mjs: 7/7 beats live (title fog night red crumble inks map)
PASS  art gate v2 on every beat + figure: PASS all hard checks
== 86 passed, 0 failed
```

files read in full: STATE-LEDGER.md 13,456 B, README.md 3,893 B, DESIGN.md 12,203 B, PLAN.md 6,180 B (35,732 B total, `wc -c`), plus lab/README.md 4,008 B, lab/package.json, story-script.json. last commit `6ac0a9c` (session 3 recheck, 2026-10-11). repo `harshgounder/santioni-look-kit`, PRIVATE.

### 1.2 how to run it (VERIFIED from lab/README.md + package.json)

```
cd ~/site-clones/santioni/lab
npm install            # node_modules already present
npm run dev            # http://localhost:5173/?scene=story
npm run build          # vite 8.3.4 -> lab/dist (static, 128 files, ~20 MB)
npm run shot -- --gpu nvidia --backend webgl   # headless Brave canvas check
```

build system: Vite 8.3.4, three 0.186.1, @dgreenheck/three-pinata 2.0.1 (MIT), tweakpane 4.0.5; dev deps puppeteer-core 25.13.0, @gltf-transform/cli. there is NO vite.config file, so `base` is `/` (matters for a GitHub Pages project path, see section 5).
query flags: `?scene=` (smoke, hatch, panel, story, crumble, inks), `backend=webgl|webgpu`, `panel`, `preset`, `dpr`, `t`, `gate=yesno|dob`, `tier=0-3|off`.

### 1.3 structure

| layer | where | what |
|---|---|---|
| story | `lab/src/scenes/story.js` (`const beats`) + `lab/src/story/story.js` | 7 beats on one native scroll, sized in screens: title 1.25, fog 2.5, night 1.25, red 2, crumble 2, inks 2.5, map 4 (hold beat). smoothing 0.5 per 60 fps frame |
| copy + VO | `lab/src/scenes/story-script.json` | ONE file: title "The mapmaker", captions = VO lines for fog, night, red, crumble, inks, map (map caption 2 after the hold) |
| look | `lab/src/look/` hatch.js (GLSL woodcut), hatch-tsl.js, panel.js (compositor, frame strokes, env plate, grain, refraction), panel.css, inktrail.js, crumble.js, glass.js, carousel.js, mapsheet.js, titlesheet.js, tiers.js | |
| interaction | `lab/src/interaction/hold.js`, `look/carousel.js`, `access/agegate.js` | hold 3 s fill / 1 s drain; carousel buttons/keys/swipe; age gate only with `?gate=` |
| character | `lab/public/chars/mapmaker-walk.min.glb` (439 KB) | MPFB CC0 body + CC0 monk robe + hood, Quaternius CC0 `Walk_Loop`, built by `art/character/build_mapmaker.py`, `dress.py`, `retarget.py` (Blender 5.2.2 LTS present) |
| audio | `lab/public/audio/manifest.json` (33 files: 7 loops, 18 one-shots, 8 VO) + `audio/audio.js`, `audio/storysound.js` | music stems audio-as-code 0.4.0 (MIT), SFX numpy (`tools/sound/build_sound.py`, `.venv`), VO Kokoro-82M voice af_heart speed 1.0 (`tools/sound/build_vo.py`, `.venv-vo`, torch 2.14.1+cpu) |
| font | `lab/public/fonts/Gloock-Regular.latin.woff2` (OFL) | painted in GL, real h1 on top |

### 1.4 reskin: files to change (from DESIGN.md section 4 + source tree)

| # | change | files |
|---|---|---|
| 1 | copy, title, VO lines | `lab/src/scenes/story-script.json`, then `.venv-vo/bin/python tools/sound/build_vo.py` (rebuilds changed lines only) |
| 2 | beats (order, screens, sound gains, insets) | `lab/src/scenes/story.js` |
| 3 | palette | hatch params `ink/mid/skin/paper` (look/hatch.js, presets in `lab/public/presets/`), `look/panel.css`, `art/ART-BIBLE.md` sec 3 |
| 4 | type | `look/panel.css`, `lab/public/fonts/` (OFL only) |
| 5 | beat content tied to the old topic | `look/mapsheet.js` (map drawing), `scenes/inks.js` + `look/carousel.js` items + `look/glass.js` (ink bottles), `look/crumble.js` `colonnade()` |
| 6 | demo hookup | most natural slot = the `inks` carousel (pick input) and `map` hold beat (run/result), or a DOM section after the story |
| 7 | character (optional) | `art/character/build_mapmaker.py`, `dress.py` -> re-export glb; keep the walk |
| 8 | sound beds (optional) | `tools/sound/build_sound.py` (+ its gate), keep -27..-21 LUFS per beat |
| 9 | drop the age gate | it only shows with `?gate=`; leave the flag off |

### 1.5 reference coverage (VERIFIED from STATE-LEDGER sec 3, 19 elements)

- done 7: frame, hatch, selective colour, insets, captions, crumble, carousel.
- partial 9: title (no ink splash), nav pill (no links/active state), cursor badge (no lag), hand (trail only, no arm), pick (no hover lift), hold (no pour stream), refraction (ground marks, not poster text), age gate (no split heading/tilt), sound toggle (text, not 4 bars).
- missing 3: loader, vortex, link underline swap.
- also open: kit packaging (tokens.css, package, recipe format, reskin guide), face detail, cloth motion, arm swing, real phone test, human listening test.

### 1.6 art pipeline

- code-made art: hatch shader, procedural map (mapsheet.js), engraved ground marks (gouge, wood grain, dry brush), code-built glass bottles, blue-noise grain (`tools/bluenoise.py`).
- Codex image_gen: `tools/codex_img.sh PROMPT.txt [REF.png]` (gpt-image-2 on ChatGPT login; codex-cli 0.164.0, `codex login status` -> "Logged in using ChatGPT"), then `tools/inkify.py` snaps to the inks, `lab/tools/measure.py` art gate v2 judges it.
- 3D: Blender 5.2.2 + MPFB, CC0 sources in `art/character/SOURCES.md`.

### 1.7 fastest reskin path (UNVERIFIED estimate)

```
keep character + walk + sound beds, change words/palette/content
 ├ story-script.json + VO rebuild ............ 1.0-1.5 h
 ├ palette + font in presets/panel.css ...... 0.5-1 h
 ├ inks/map beats -> topic objects + demo ... 2-3 h
 ├ exclude local-only files, build, deploy .. 0.5 h
 └ total ...................................... 4-6 h   (+2-4 h for a new character)
```

### 1.8 RISK found: dist ships local-only files

`lab/dist/` today contains `models/Xbot.glb`, `models/Soldier.glb` (three.js examples, Xbot is Mixamo-derived) and `chars/mapmaker-walk.local.glb`, `mapmaker-walk.local.min.glb` because Vite copies all of `public/`. git ignores them but a deploy of `dist/` would publish them. delete or move them out of the deploy copy (not done here, read-only).

## 2. deploy routes (VERIFIED presence/auth this session; limits from docs fetched today)

| route | CLI on PATH | logged in | free-tier facts for static site + small backend | source |
|---|---|---|---|---|
| GitHub Pages | `gh` 2.96.0 | YES, `harshgounder`, scopes gist, read:org, repo, workflow | site max 1 GB, soft 100 GB/month bandwidth, soft 10 builds/h (none with Actions), deploy timeout 10 min; static only. private-repo Pages needs a paid plan (UNVERIFIED) | docs.github.com Pages limits |
| Vercel | MISSING (no ~/.vercel, not in npx cache) | no | Hobby: functions 300 s max, 2 GB / 1 vCPU, CLI upload 100 MB | vercel.com/docs/limits, /plans/hobby |
| Netlify | MISSING | no | free = 300 credits/month, production deploy 15 credits each | agentdeals.dev, convika.com (secondary) |
| Cloudflare Pages/Workers (wrangler) | MISSING | no | Pages free: 500 builds/month, 25 MiB per file, 20,000 files; Workers free 10 ms CPU per request | developers.cloudflare.com |
| Firebase | MISSING | no | not checked, UNVERIFIED | |
| Surge | MISSING | no | not checked, UNVERIFIED | |
| Fly.io (fly/flyctl) | MISSING | no | not checked, UNVERIFIED | |
| Railway | MISSING | no | not checked, UNVERIFIED | |
| Render | no CLI | no | free web service 512 MB / 0.1 CPU, spins down after 15 min idle, ~1 min spin-up, 750 h/month | render.com/docs/free |
| Hugging Face | not on PATH; `~/re-arsenal/venv/bin/hf` (huggingface_hub 1.33.0) | NO (`hf auth whoami` -> "Error: Not logged in", no token file) | CPU Basic 2 vCPU / 16 GB free, BUT Gradio/Docker Spaces now need PRO to create; free accounts get up to 2 ZeroGPU Gradio Spaces; Static Spaces free | huggingface.co/docs/hub/spaces-overview |
| Modal | MISSING | no | UNVERIFIED | |
| ngrok | MISSING | no | UNVERIFIED | |
| cloudflared | MISSING | n/a | Quick Tunnel: no account, 200 in-flight requests then 429, no SSE, random hostname each start, no uptime guarantee | developers.cloudflare.com quick-tunnels |

no deploy-related env var names set (checked names only: vercel, netlify, cloudflare, hf, modal, ngrok, railway, fly, render, firebase -> none).

## 3. local toolchain (VERIFIED)

| tool | result |
|---|---|
| node / npm / pnpm / bun | v22.23.1 / 10.9.8 / 12.3.4 / 1.3.14 |
| python3 / uv | 3.14.7 / uv 0.11.32 |
| docker | 29.8.2, daemon active, user in `docker` group |
| podman | MISSING |
| ffmpeg | n9.0.2 |
| browsers | Brave 154.1.96.61 (`/usr/bin/brave`); no chromium binary on PATH; Playwright browsers in `~/.cache/ms-playwright` (chromium-1228/1234/1243, headless shells, firefox) |
| playwright-core | `~/camofox-browser/node_modules/playwright-core`, `~/.hermes/hermes-agent/node_modules/playwright-core`, 3 copies under `~/.npm/_npx/` |
| GPU | GTX 1650 4096 MiB, driver 615.71.09, CUDA UMD 13.4 (+ AMD Vega iGPU per lab README) |
| torch | `~/r2-venv` 2.13.0+cu130, `cuda True` (only CUDA venv); `~/privacy-proxy/.venv` 2.13.0+cpu; `~/re-arsenal/venv` 2.14.1+cpu; santioni `.venv-vo` 2.14.1+cpu |
| ollama | client 0.40.0, server NOT running; models in `/var/lib/ollama`: qwen3:4b, bge-m3, mxbai-embed-large, nomic-embed-text (4.3 G) |
| llama.cpp | llama-server / llama-cli MISSING; one gguf: `~/.hermes/mnemosyne/models/MiniCPM5-1B-Q4_K_M.gguf` |
| Blender / Codex | Blender 5.2.2 LTS; codex-cli 0.164.0, ChatGPT login |
| RAM | 7.1 GiB total, 2.4 GiB available, swap 4.3 of 15 GiB used (tight) |
| disk | /home 220 G free of 477 G |
| CPU | 12 threads |

## 4. deck tooling (VERIFIED)

- python-pptx 1.0.2 in `~/clause-engine/.venv` (only venv found with it; not in system python or re-arsenal venv).
- builders: `~/clause-engine/build_deck.py` (python-pptx, palette block), `~/hypnexis-ppt-claude/build_deck.py`, `build_v2..v5.py` (v5 imports v4; usage line points at `/tmp/pptvenv`, which no longer exists, so run with the clause-engine venv). outputs v2-v5 .pptx + .pdf and VAKYA.pptx/pdf exist there as references.
- PDF export: `soffice` / `libreoffice` at /usr/bin. marp MISSING.
- skills: anthropic-skills:pptx (built in), design-taste, hackathon in `~/.claude/skills`; no dedicated pitch-deck skill. the Artifact Slides type is an option too (exports .pptx/PDF).

## 5. recommended default stack for tonight

```
                ┌────────────────────────────────────────┐
 judges ──────▶ │ GitHub Pages (public repo, gh authed)  │  santioni reskin, vite build, base set to /<repo>/
                │  + in-browser ML (transformers.js /    │  [14] no server to die at 03:00
                │    onnxruntime-web, WebGPU or WASM)    │
                └──────────────┬─────────────────────────┘
                               │ only if the model cannot run in the browser
                               ▼
                ┌────────────────────────────────────────┐
                │ user PC: docker or uv + FastAPI        │  GTX 1650 4 GB via ~/r2-venv (cu130)
                │ tunnel: cloudflared quick tunnel       │  [10] needs install GO; URL changes on restart
                └──────────────┬─────────────────────────┘
                               ▼ backup
                HF ZeroGPU Gradio Space (needs hf login GO) or Render free (login, 1 min cold start)
```

| risk | why | mitigation |
|---|---|---|
| tunnel tool missing | cloudflared and ngrok not installed | ask GO to install cloudflared early, or avoid a backend |
| quick tunnel URL changes | new hostname per start, no SSE | read the backend URL from a small config.json on Pages; no streaming over SSE (use plain POST or WebSocket) |
| GitHub Pages subpath | no vite.config, base `/` breaks at `/<repo>/` | add `base` in a vite config, or use a `<user>.github.io` repo |
| repo privacy rule | user default is private, Pages on private repos is paid (UNVERIFIED) | separate PUBLIC deploy repo with only the built site; kit repo stays private |
| local-only assets in dist | Xbot, Soldier, *.local*.glb get copied | strip before deploy (section 1.8) |
| laptop RAM | 2.4 GiB free with swap in use | close harnesses during judging; small model (<1 GB) |
| 4 GB VRAM | GTX 1650 | pick small models; CPU fallback |
| PC sleep / wifi during judging | lid-open wifi blip noted in memory (UNVERIFIED tonight) | keep lid open on power, static page shows a recorded demo clip when the API fails |
| HF Spaces rules changed | Gradio/Docker need PRO, only 2 ZeroGPU free | do not plan around HF CPU Spaces |
| WebGL on judge phones | kit never tested on a real phone | tiers.js steps quality down; test on the user's phone before submission |
