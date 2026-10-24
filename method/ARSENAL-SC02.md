# ARSENAL-SC02: every arsenal piece that applies to SC-02, the exact command, who runs it

v1, 2026-10-24 ~16:45 IST, Claude Code subagent, read-only mining. Nothing installed, no heavy job run.
SC-02 = accessible walking routes from street images, all of India (brief: `research/WAVE-2-SC02-BRIEF.md`).
Sibling file: `method/ARSENAL.md` (fleet-wide tool map, search rails, key routing). This file is the SC-02 slice of the RE / style / media arsenal plus the researched tools in `~/re-universe`.

## 0. Sources read and how

| source | bytes | read | note |
|---|---|---|---|
| `research/WAVE-2-SC02-BRIEF.md` | 4,903 | full | |
| `~/.agents/capabilities/CAPABILITIES.md` | 28,700 | full | generated 2026-10-24 10:56 UTC (today, fresh) |
| `re manifest` (run 10:58 UTC) | 18,065 printed | full | 15 domains, 135 actions, 41 components, 18 plugin tools, 17 python helpers |
| `re playbook design / style / media / clone / model` | 798 / 997 / 613 / 914 / 803 | full | |
| re-universe `a1` / `m4` / `m3` / `m5` / `m2` / `m1` / `s2` | 43,356 / 68,992 / 86,813 / 53,930 / 81,426 / 83,772 / 69,349 | every line paged (Read tool, offsets) | |
| `~/re-arsenal/docs/RESUME.md` | 6,676 | full | |
| `~/site-clones/santioni/STATE-LEDGER.md` | 13,456 | full | |
| code checks | n/a | `bundle/lib/domains/{media,gen,style}.mjs`, `bundle/lib/py/media.py`, `bundle/index.js`, `santioni/tools/codex_img.sh` head, `~/.hermes/plugins/rea/{plugin,mcp}.json`, `~/.dsh/profiles/dsh-tui/package.json` | flags below come from the code, not from `--help` (which prints only the generic banner) |

Grades: VERIFIED = I saw it in code, config or a command today. UNVERIFIED = from a note, a README claim, or my inference.

## 1. Who can call what (the "agent" column below uses these letters)

| letter | agent | route to the arsenal | state |
|---|---|---|---|
| C | claude | Bash: `re <domain> <action> <target> [--flags]`; REA: `~/.agents/capabilities/bin/rea-claude <cmd> --token-limit N` (plain `rea` is not on PATH) | VERIFIED (manifest ran) |
| D | dsh | dsh-tui profile only: plugin tools `re_<domain>` with args `{action, target, second, options}` (options = the CLI flags, e.g. `{"fps":1}`), plus `mcp__rea__*` (207, REA 6.7.0) and dsh-ghidra | plugin rows VERIFIED in `package.json`; RESUME item 3 says the running TUI must be restarted to see them, so live availability is UNVERIFIED. dsh fleet/headless profiles do not have them |
| H | hermes | `rea` plugin = REA MCP via `npx rea-agents@6.4.0 mcp` (pinned 6.4.0, older than the 6.7.0 bundle); no `re_*` plugin, so `re` only through its terminal tool | VERIFIED (`~/.hermes/plugins/rea/mcp.json`) |
| X | codex | shell: `re ...` (UNVERIFIED from Codex); built-in image_gen through `~/site-clones/santioni/tools/codex_img.sh PROMPT.txt REF.png` (gpt-image-2 on the ChatGPT login) | codex_img.sh VERIFIED (header read) |

Rules that bind every row: two independent engines on any claim that matters (every playbook ends with it); clean-room (spec from evidence, no copied assets or brand); installs, model downloads, MCP registration and multi-minute CPU jobs need the user's GO (RESUME "shelved" list; `gen.cuda` is deferred, torch is 2.14.1+cpu).

## 2. Capability table by pipeline stage

Status: **inst** = installed and callable now; **kit** = already built inside `~/site-clones/santioni` (santioni-look-kit); **res** = researched in re-universe, not installed (needs GO); **host** = needs a hosted demo, API or rented GPU (the user's access-route rule: "no" on the laptop means pick a route, not drop).

### 2.1 Image intake (own photos, Mapillary/KartaView, YouTube walking-tour frames)

| capability | exact command | agent | status | why for SC-02 / caveat | source |
|---|---|---|---|---|---|
| download a walking-tour video | `yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" -o "walks/%(id)s.%(ext)s" URL` | C, D, H, X (shell) | inst (`~/.local/bin/yt-dlp`) | raw Indian street footage for test data. Rights: YouTube terms and creator copyright. Use own phone walks or CC-licensed clips for anything shown on stage; others for internal labelling only, and say so | ARSENAL.md row "Other CLIs"; which yt-dlp today |
| stream facts | `re media probe walks/X.mp4` | C, D (`re_media {action:"probe"}`) | inst | fps, resolution, rotation, and whether a GPS/telemetry data stream exists (GoPro-style tracks give free geotags; UNVERIFIED for any given clip) | manifest |
| shot cuts | `re media scenes walks/X.mp4` | C, D | inst | split a 40 min tour into shots; one frame per shot avoids near-duplicates | manifest |
| frames at a fixed rate | `re media frames walks/X.mp4 --fps 0.5 --out frames/X/` | C, D (`options:{fps:0.5}`) | inst | VERIFIED from code: the CLI passes only `--fps`; the `--count` in the description is not wired in `media.mjs` (the python helper supports count, start, duration). Output `frame_00001.png ...` | `bundle/lib/domains/media.mjs` line 37-46, `py/media.py` line 90 |
| contact sheet | `re media sheet walks/X.mp4 --out sheets/X.png` | C, D | inst | one image per video to triage which tours show kerbs, steps, poles, parked bikes | manifest |
| clip look stats | `re style video walks/X.mp4` | C, D | inst | per-frame brightness and palette drift: tag night, monsoon, glare frames for the robustness slice | manifest |
| better shot detection | PySceneDetect `scenedetect -i X.mp4 detect-content list-scenes`; OmniShotCut (install from git, not PyPI) | C, D | res | second engine against `re media scenes` (cross-check rule) | m2 section 3 + review correction |
| metric scale from video | Spirula Studio (SfM with metric scale from video metadata) | D | res | needed if kerb height is measured from a walk video | m4 section 2 |
| map imagery APIs | Mapillary v4, KartaView, Street View metadata | D | lane S1 owns it | read the documented APIs first; `re web har <capture.har>` + `re web openapi <capture.har>` only to map a viewer's calls for interop, within terms | manifest (web domain); brief lane S1 |

### 2.2 Barrier detection (kerb ramp missing, steps, broken path, poles, parked vehicles)

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| weight safety before load | `re ai pickle weights/model.pt` and `re data pickle weights/model.pt` (fickling) | C, D (`re_ai {action:"pickle"}`) | inst | every YOLO/SAM/.pt pulled from GitHub or HF is a pickle; check before `torch.load` | model playbook phase 2 |
| model container facts | `re ai models weights/` ; `re ai formats model.onnx` ; `re ai graph model.onnx --detail` | C, D | inst | input size, opset, op histogram before an onnxruntime-web export for the in-site demo | model playbook phase 1, 3 |
| lineage check | `re ai diff base.safetensors finetuned.safetensors` | C, D | inst | proves our India fine-tune differs from the base (judges ask) | model playbook |
| open-vocabulary detector + masks | SAM 3 (text prompts like "kerb ramp", "staircase", "pole"; presence head) | D, host | res (12,045 stars) | engine 1 of the "two detectors must agree" move | a1 section 1 |
| closed-set fast detector | YOLO26 (NMS-free, small-target label assignment, arXiv 2606.03748); RF-DETR; DETR-series (D-FINE, DEIM) | D | res | engine 2; small-target assignment is the brief's "small barriers" challenge | a1 section 1 |
| multi-frame agreement | roboflow/trackers (Apache-2.0); boxmot (AGPL) | D | res | track a pole across frames of one walk: several images of the same spot agreeing | a1 section 1 |
| masks for labelling | Sammie-Roto-2 (SAM2 + matting, GPL-3.0) | D | res | fast masks for our own Indian labels | m2 section 6 |
| "why flagged" heatmap | jacobgil/pytorch-grad-cam | D | res | explainability panel in the demo; pairs with "needs a human look" refusal | a1 section 8 |
| model inspection | TorchLens / Model Menagerie; Netron | C (read) | res | architecture figure for the deck | a1 section 8 |
| humans in the loop | Zalando RAG flywheel pattern (human-approved items feed the next retrieval) | design | n/a | label loop: low-confidence detections go to a reviewer queue, approved ones become training data | s2 section 3 |
| cheap scoring at scale | Naver: batch CLIP-style scorers in vLLM pooling runtime; Pinterest: send embeddings, not pixels | design | n/a | architecture slide: phones send embeddings or crops, server batches | s2 sections 1, 3 |

### 2.3 Depth and kerb or step height

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| CPU depth | localai-org/depth-anything.cpp (Depth Anything 2 and 3, ggml, CPU; exports PLY, GLB, COLMAP) | D | res (MIT, 1,132 stars) | the only depth route here that fits the laptop as stated; parity claims are the README's | a1 sections 1, 6 |
| second depth engine | Marigold V2 (diffusion depth); Depth Anything 3 (any-view depth + pose); Video-Depth-Anything | host | res | cross-check rule: two depth engines on every kerb height we quote | a1 section 1, 6; m2 (Go-with-the-Track row) |
| metric 3D from views | facebookresearch/map-anything (metric); VGGT-omega | host | res | relative depth alone cannot give centimetres; a metric model or a reference object (standard kerb stone, tile, bike wheel) is needed | a1 section 6 |
| material height map | `re style pbr frame.png --out pbr/` | C, D | inst | APPROXIMATE height, normal, roughness from one image. Good for WebGL textures of broken paving; NOT a measurement, never quote it as kerb height | manifest |

### 2.4 3D, Gaussian splats, world models of a crossing

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| splat trainers | LichtFeld Studio (compute 7.5+ incl. GTX 16-series, CUDA 12.8+); Brush (Rust/WebGPU); Spirula Studio (Vulkan, 10M Gaussians in 8 GB, author claim); OpenSplat (CPU mode, slow) | D | res | reconstruct one MUJ or Jaipur crossing from a 30 s phone orbit. None promises 4 GB VRAM | m4 section 2, find 5 |
| feed-forward splats | InfiniSplat v2; map-anything; Open-DiffusionGS | host | res | no per-scene training; fastest route tonight if a hosted GPU is available | a1 section 6; m4 section 1 |
| splat in the browser | Spark (THREE.js splat renderer, MIT, v2.4.0 2026-10-20); supersplat-viewer | C (site) | res | the santioni kit is three.js, so Spark drops into it | m4 section 2 |
| splat edit and convert | SuperSplat (browser editor); `splat-transform` CLI; SPZ (about 10x smaller than PLY, claim); KHR_gaussian_splatting (ratified glTF extension) | C, D | res | crop the crossing, compress for page weight, ship as GLB | m4 section 2, find 4 |
| GLB check | `re media glb crossing.glb` ; glTF-Validator ; glTF-Transform `inspect` / optimize; meshoptimizer | C, D | `re` inst, rest res | validate whatever 3D file goes into the site | manifest; m4 section 6 |
| single image to parallax "walk-through" | DepthFlow (image to 3D parallax video, AGPL) | D | res | cheapest "walk the route before you go" feel from one street photo | m4 section 4 |
| 3D props (pole, scooter, ramp, wheelchair) | TRELLIS.2 / Pixal3D (24 GB class, hosted); Procedura / img2threejs (code-3D by an LLM agent) | host, C | res | code-3D gives editable, light props for WebGL | m4 section 1 |
| auto-rig a GLB on CPU | skin-tokens.cpp (GGML, CPU or Vulkan) | D | res | rig a wheelchair-user or pram-parent character if we model one | m4 section 5, find 7 |
| "monsoon / night what-if" video | LTX-2.5 IC-LoRAs (Day-To-Night, Colorization; about 66 GiB, hosted); Go-with-the-Track (restyle keyframes, keep motion from tracks); Wan-Animate-2; MiniMax H3 (licence excludes EU, UK, South Korea, USA and restricts outputs outside its territory) | host | res | "predict how a spot looks in monsoon": restyle one real walk clip, keep the true geometry | m2 sections 1, find 4-6 |
| world-model recipes | OpenWorldLib; LongLive; minWM recipe (no repo found) | host | res | slide material, not a tonight build | a1 section 5 |
| 3D splat restyle | Stylos, GAST, ABC-GS (3DGS style transfer) | host | res | woodcut-style the crossing splat to match the site | m4 section 1 |

### 2.5 Map matching (detection to the right footpath segment)

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| inspect map files | `re data sqlite city.gpkg` (GeoPackage and MBTiles are SQLite); REA `inspect-sqlite-database` | C, D, H (REA) | inst | sanity-check an OSM or OpenSidewalks extract before routing | manifest (data domain); REA command list |
| inspect tile or PBF bytes | `re data protobuf tile.mvt` ; `re data fq tile.pbf ".[0]"` | C, D | inst | vector tiles and OSM PBF are protobuf; useful when a tile looks wrong | manifest |
| map matching itself | not in the arsenal or the notes | D (lane S1) | gap | see section 4 | n/a |

### 2.6 Routing with barrier costs

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| routing engines (OSMnx, Valhalla pedestrian, OpenTripPlanner wheelchair, pgRouting, AccessMap) | not in the arsenal or the notes | D (lane S1) | gap | see section 4 | brief lane S1 |
| system shape | Meta thin orchestrator (router does no domain work, specialists do); Uber deployment safety (shadow test, auto-rollback); Anthropic postmortem lesson (evals did not match user reports) | design | n/a | architecture slide and the "refuse when unsure" story | s2 sections 4, 6, 8 |

### 2.7 Site design: tokens, motion, fonts, sound from santionispirits.com

The look was already reverse engineered and rebuilt: `~/site-clones/santioni` (santioni-look-kit, private repo). STATE-LEDGER (2026-10-11): 7 story beats, woodcut hatch shader, 33 sounds, Kokoro VO, Gloock titles chosen by measurement, GPU quality tiers, 80/80 checks. Reskin it; do not re-clone from zero.

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| kit health first | `bash ~/site-clones/santioni/tools/verify_state.sh --quick` (full run about 10 min) | C | kit | believe only what checks out before forking | STATE-LEDGER rule |
| story engine | `lab/src/scenes/story.js` (`const beats`), captions + VO lines from one file `lab/src/scenes/story-script.json`; `node lab/tools/beats.mjs` | C | kit | swap the mapmaker story for an SC-02 story (a wheelchair user, a parent with a pram, a blind walker) | STATE-LEDGER section 1 |
| CSS tokens of the live page | `re style css https://santionispirits.com` | C, D | inst | delta check only: what the kit already took and what SC-02 recolours | design playbook phase 1 |
| runtime tokens with roles | `re style extract https://santionispirits.com --design-md` (dembrandt) | C, D | inst | DESIGN.md for the reskin; dembrandt `--tokens` drift gate exists upstream | manifest; m5 find 1 |
| motion fingerprint | `re style motion https://santionispirits.com` | C, D | inst | durations, easings, scroll timelines. m5 find 4: read timing from the runtime, never from a vision model; GSAP tweens are not in `getAnimations()` | manifest; m5 section 5 |
| tokens from a screenshot | `re style tokens shot.png` ; grade `re style image shot.png` | C, D | inst | when the live page blocks scripted fetch | design playbook |
| font identification | `re style fonts shot.png --top 6` | C, D | inst | kit chose Gloock (OFL) by measurement; Indian scripts need real font files (see 2.8 note) | manifest; STATE-LEDGER row "titles" |
| page evidence | REA `capture-web-screenshot`, `inspect-web-page`, `observe-web-session`, `inspect-web-network-capture`, `analyze-web-bundle`, `recover-javascript-sources` via `rea-claude <cmd> --token-limit 4000` | C, D (`mcp__rea__*`), H | inst | study shaders, scroll and audio loading of the reference; clean-room, no copied code or assets | CAPABILITIES 1e |
| recolour real frames into the look | `re style transfer ref.png frame.png --out graded.png --strength 0.8` ; `re style lut ref.png --from frame.png --out grade.cube` | C, D | inst | real Jaipur frames graded to the site palette | style playbook phases 2, 3 |
| woodcut / halftone from real photos | `re style print frame.png --mode woodcut` (also halftone, duotone, riso; `--cell 5`) | C, D | inst | story panels made from OUR street data, so the art itself is evidence | manifest; style playbook phase 4 |
| WebGL looks | dithering-shader (R3F), spite/sketch (hatch), canvas-ui / vfx-js, scroll-craft, oil-motion; tegaki (handwriting animation for captions) | C | res | add-ons to the kit if a beat needs them | m1 section 5c, m5 section 5, m1 section 6 |
| motion timing check of OUR page | motiscope on a screen recording (`ffmpeg` + stdlib python) | C | res | measures easing and beats from frames; states its own limits | m2 find 1 |
| sound bed and VO | kit: `tools/sound/build_sound.py` (audio-as-code, gate checks loop seams), `tools/sound/build_vo.py` (Kokoro-82M, voice af_heart, speed 1.0, -20.5 LUFS mono) | C | kit | new SC-02 lines through the same gates | STATE-LEDGER rows "sound", "voice" |
| loudness and timbre facts | `re media audio vo.wav` ; `re media spectrogram bed.ogg` | C, D | inst | keep every beat inside the kit's -27 to -21 LUFS bed band | media playbook; STATE-LEDGER bed mix row |
| SFX (wheelchair clatter, horn, monsoon rain, cane tap) | Stable Audio 3 Small-SFX (433M, CPU-capable, Stability Community Licence, gated); audio-studio-mcp | D | res, needs GO | m3 find 1; "trained on licensed and Creative Commons data" | m3 lane 5 |
| match our master to a reference | Matchering 2.0 (RMS, spectrum, peak, width; 4 GB RAM) ; pyloudnorm | C | res | one command against the kit's reference audio capture | m3 lane 6, find 9 |
| Hindi or regional narration | OmniVoice (600+ languages; its cloning part is record-only, use stock voices); Kokoro Hindi voices | D | res | mass appeal across India. Kokoro Hindi support is from my memory, UNVERIFIED | m3 lane 9 |
| voice in, voice out (blind users) | sherpa-onnx (on-device TTS, ASR, VAD); whisper.cpp | D | res | spoken route guidance in the demo | a1 section 3 |

### 2.8 Art generation (character, scenes, story panels)

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| ChatGPT app image route | `re gen chatgpt "<prompt>" --ref art/char-ref.png --out art/gen/ --timeout 420 --verify --intent "same character, woodcut hatch"` | C, D (`re_gen {action:"chatgpt"}`) | inst (ledger `gen.chatgpt` PASS on 10-21) | drives the logged-in desktop app over CDP port 9333; one app session, so run it serially (inference) | `domains/gen.mjs` line 17-41 |
| Codex image route | `sh ~/site-clones/santioni/tools/codex_img.sh art/p01.txt art/char-ref.png` | X | kit | gpt-image-2 on the ChatGPT login; a reference image keeps the character on-model (A1 lesson in the script) | codex_img.sh header |
| route check | `re gen routes` | C, D | inst | which routes are live right now | manifest |
| accept or retry | `re gen gate art/char-ref.png art/gen/x.png --intent "..." --max-distance 0.25` ; `re gen judge ref cand --json` | C, D | inst | local style distance plus a headless Claude verdict, both halves | `domains/gen.mjs` line 80, 136 |
| kit art gate | `python3 -I ~/site-clones/santioni/lab/tools/measure.py <img>` ; `python3 -I lab/tools/gate_selftest.py` ; `tools/inkify.py` | C | kit | hatch width, spacing, solid share; the gate the kit already trusts | STATE-LEDGER row "art gate" |
| local img2img (slow) | `re style generate ref.png "<scaffold + subject>" --strength 0.6 --steps 24` | C | inst, CPU only | about 1m40s at 384 px, 8 steps; several minutes at 512 px. Fallback only | RESUME item 1-2 |
| character consistency method | illo-skill (recurring mascot, woodcut and riso looks); style-consistency-ai; baituzhan (no real artist names in style anchors) | C | res | one recognisable hero across all beats | m1 section 4 |
| vectorise art for page weight | vtracer; inkvec; Vecline (render-back check) | C | res | crisp SVG panels at small size | m1 section 5a, find 8 |
| style metric caveat | csd-plus / MegaStyle encoder | C | res | CSD cosine fails as an absolute score (2605.09030); use it relatively, never as proof | m1 section 7, find 3 |
| provenance label | c2patool (sign and read Content Credentials) | C | res | mark generated panels as generated; honesty with judges | m1 section 8 |
| real text over art | real font files layered over images, never text painted by the model | C | method | m1 find 10: a current open model wrote Japanese product names right in 18 of 64 images; Devanagari and Tamil in generated images should be assumed worse (inference) | m1 find 10 |

### 2.9 Deck and demo video

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| slide deck | Artifact tool `action:"quickstart", intent:"slides"`, then the Slides type | C | inst (tool) | `re` has no deck action | Artifact tool description |
| figures | `re media sheet demo.mp4 --out deck/sheet.png` ; `re style image` on each figure | C, D | inst | one-image summaries of the dataset and the demo | manifest |
| demo video from code | HyperFrames (HTML/GSAP to MP4, Apache-2.0); Remotion | C | res | deterministic screen film if live demo fails | m2 section 5 |
| process skills | `hackathon` (locked decisions, mocks behind a flag, rehearsal, Q&A); `design-taste` (tokens first, 150 tells, audit at 375/768/1440, max 3 cycles); `brainstorm` | C | inst | | skill list |

### 2.10 Verification before the 02:30 freeze

| capability | exact command | agent | status | why / caveat | source |
|---|---|---|---|---|---|
| style distance vs reference | `re style compare ref.png ours.png` | C, D | inst | the acceptance test in design, style and clone playbooks | playbooks |
| anti-slop lint | `re style slop site/index.html --json --limit 12` (or the deployed URL) | C, D | inst (ledger `style.slop.gesso` PASS) | higher score is worse | manifest |
| headless audit | design-taste `scripts/audit.mjs` (contrast, overflow, focus, tap targets, reduced motion, console errors) | C | inst | a site about accessibility must itself pass these | m5 intro |
| screenshot diff | REA `capture-web-screenshot`, `compare-web-screenshots`, `compare-web-captures` | C, D, H | inst | deterministic diff owns "done" (m5 find 5: agents fake passes when they grade themselves) | CAPABILITIES 1e; m5 find 5 |
| kit tests | `bash ~/site-clones/santioni/tools/verify_state.sh` ; `node lab/tools/shot.mjs --dpr 2` ; `test-sound.mjs`, `test-tiers.mjs`, `probe-story.mjs` | C | kit | keep the 80 checks green after the reskin | STATE-LEDGER |
| arsenal truth | `re state` ; `re doctor` | C, D | inst | before claiming a tool works | RESUME |
| code and claims | `quality-gate` skill; `reviewer` agent; `fact-checker` agent | C | inst | every number on a slide gets a primary source | skill and agent lists |

## 3. The 15 highest-value uses tonight, in order

| # | use | command (first step) | agent | confidence 0-20 and why |
|---|---|---|---|---|
| 1 | Reskin santioni-look-kit for SC-02 instead of building a new site | `bash ~/site-clones/santioni/tools/verify_state.sh --quick`, then edit `story-script.json` + `story.js` beats | C | 17: kit exists with 80 checks; risk is the reskin time, not the tech |
| 2 | Build our own Indian test set from walking videos | `yt-dlp ...` then `re media scenes`, `re media frames --fps 0.5`, `re media sheet` | C, D | 16: all installed; rights note applies for anything shown |
| 3 | Weight safety and shape checks on every downloaded model | `re ai pickle <file.pt>`, `re ai models <dir>`, `re ai graph model.onnx` | D | 18: cheap, installed, prevents a pickle surprise |
| 4 | Character and scene art with a gate | `re gen chatgpt "<prompt>" --ref char-ref.png --verify`, `re gen gate`, kit `measure.py`; codex in parallel via `codex_img.sh` | C, X | 14: gen.chatgpt passed on 10-21; app session can hit usage limits (code checks for "usage limit") |
| 5 | Story panels from real Jaipur frames | `re style print frame.png --mode woodcut`, `re style transfer ref.png frame.png --out x.png` | C, D | 16: deterministic, installed, and the art doubles as evidence |
| 6 | Two-detector agreement (SAM 3 text prompts + YOLO26 or RF-DETR), trackers across frames | dsh lane S1 smoke tests | D | 11: not installed; 4 GB GPU, CPU torch; hosted route may be needed |
| 7 | Kerb height with two depth engines plus a reference object | depth-anything.cpp (CPU) and Marigold V2 or Depth Anything 3 (hosted) | D | 9: relative depth needs a scale; metric claims must be hedged |
| 8 | Delta check of the reference look | `re style css`, `re style extract --design-md`, `re style motion`, `re style fonts` on santionispirits.com | C | 15: installed; the kit already holds most of it |
| 9 | Sound for the new story | kit `build_vo.py` + `build_sound.py`, `re media audio` on each file; SFX via Stable Audio 3 Small (GO) | C, D | 13: kit pipeline proven; SFX model is gated and needs GO |
| 10 | Crossing in 3D on the page | phone orbit to LichtFeld/Brush/OpenSplat or a feed-forward model, then `splat-transform`, Spark in three.js, `re media glb` | D, C | 8: no trainer installed, 4 GB VRAM; fallback is DepthFlow parallax from one photo |
| 11 | "Why flagged" heatmaps and the refusal state | pytorch-grad-cam on the detector; low-confidence goes to a "needs a human look" queue | D | 10: depends on 6 |
| 12 | Monsoon or night what-if of one real clip | LTX-2.5 Day-To-Night IC-LoRA or Go-with-the-Track (hosted); label with c2patool | host | 6: big models, hosted only, licence checks |
| 13 | Map file sanity before routing | `re data sqlite city.gpkg`, `re data protobuf tile.mvt` | C, D | 12: installed; routing itself is a gap |
| 14 | Freeze gate | `re style compare`, `re style slop`, design-taste `audit.mjs`, REA `compare-web-screenshots`, kit `verify_state.sh` | C | 17: all installed; must run by 02:15 |
| 15 | Deck and backup film | Artifact Slides quickstart, `re media sheet` figures, HyperFrames screen film if live demo is shaky; `fact-checker` on every slide number | C | 13: Slides type depends on the account, check with quickstart |

```
tonight's flow (who: C claude, D dsh, X codex, H hermes)

 walks (yt-dlp)  ->  re media scenes/frames/sheet  ->  labels (Sammie-Roto, human queue)
      C/D                     C/D                              D
                                   |
                                   v
 re ai pickle/models  ->  SAM3 + YOLO26 agree?  --no-->  "needs a human look"
        D                      D        |yes
                                        v
                 depth x2 engines + reference object  ->  kerb height (hedged)
                                 D
                                        v
          map match + barrier-cost routing  (GAP: lane S1 tools, not in arsenal)
                                 D
                                        v
 santioni kit reskin  <-  re style print/transfer (real frames)  <-  re gen chatgpt + gate (C/X)
        C                         C/D
        |
        v
 re style compare + slop + audit.mjs + verify_state.sh  ->  freeze 02:30
```

## 4. Gaps the arsenal does not cover

| gap | effect on SC-02 | cheapest route (GO where it installs or talks to a service) |
|---|---|---|
| no detection, segmentation or labelling tool installed (no YOLO, SAM, CVAT, Label Studio) | the core AI stage is outside `re` | dsh lane S1 installs into a project venv; labelling UI not researched in any re-universe note |
| no depth model installed | kerb height has no local engine yet | depth-anything.cpp (CPU) is the researched fit |
| no GIS stack: map matching, OpenSidewalks schema, OSMnx, Valhalla, OpenTripPlanner, pgRouting, AccessMap | routing with barrier costs is not covered by the arsenal or the 7 notes at all | lane S1 sources only; `re data sqlite/protobuf` can only inspect files |
| no splat trainer or 3D generator installed; CUDA deferred (`gen.cuda`), torch CPU | 3D crossing needs a hosted GPU or a slow CPU path | OpenSplat CPU, hosted feed-forward models, or DepthFlow parallax as the fallback |
| no local video or world model | monsoon/night what-if is hosted only | LTX-2.5 / Go-with-the-Track on rented GPU; or a still-image restyle |
| `re media frames` CLI ignores `--count`, `--start`, `--duration` (helper supports them) | sample by rate only | use `--fps`; cut with ffmpeg first if a time range is needed |
| no wheelchair, pram or white-cane character asset; kit hero is a robed mapmaker (MPFB CC0 + Quaternius walk) | the emotional hook needs new characters | generated 2D panels via `re gen chatgpt` / codex; 3D needs a CC0 source (not researched) |
| no verified Indian-language TTS; generated images mis-write scripts | regional narration and signage risk | OmniVoice stock voices (res); real font files over art (Noto Devanagari not researched, hypothesis) |
| no screen-reader or full accessibility audit in `re` (only design-taste contrast, focus, tap targets) | a site about access must pass access tests | axe-core style checks (Trace and verdict use them, m5); manual keyboard and screen-reader pass |
| no deck action in `re`; no motion-fidelity score installed (designlang `fidelity` is research only); no GSAP timeline capture tool exists | deck and motion parity by hand | Artifact Slides; `re style motion` + motiscope on a recording |
| `re gen chatgpt` is one desktop app session | art generation is serial | split prompts between C (app) and X (codex image_gen) |
| hermes REA is pinned at 6.4.0; dsh `re_*` and `mcp__rea__*` need a dsh-tui restart (RESUME item 3) | tool lists may differ per agent | run `re_doctor`/`re_manifest` (dsh) or `rea doctor` before relying on a tool |
| Mapillary, Street View, YouTube terms | what may be shown or stored | lane S1 records terms per source; on stage, show own photos or permitted images |

## 5. Red team of this file

| claim | grade | why |
|---|---|---|
| `re media frames` passes only `--fps` | VERIFIED | `media.mjs` line 41-44 builds args `[file, dir, fps]` only |
| `re gen chatgpt` flags `--ref --out --timeout --verify/--judge --intent --max-distance`, port 9333 | VERIFIED | `gen.mjs` line 17-41 |
| dsh tool shape `{action, target, second, options}` | VERIFIED for the plugin code (`bundle/index.js` line 63-68); live availability in the running TUI UNVERIFIED | RESUME item 3 |
| hermes REA = rea-agents 6.4.0 over npx | VERIFIED | `mcp.json` |
| the brief's "GPT-Image-2.5" for codex art | likely WRONG for the codex route | STATE-LEDGER section 3: "Codex 0.162.1 still gives gpt-image-2 on a ChatGPT login; 2.5 needs an API key" (as of 2026-10-11; recheck at use time) |
| depth-anything.cpp is the only laptop-fit depth route | UNVERIFIED | README claims only; nothing run |
| SAM 3, YOLO26, splat trainers, Spark, DepthFlow, Stable Audio 3 rows | UNVERIFIED for this box | researched stats from 2026-10-21 notes; not installed, not run |
| Kokoro has Hindi voices | UNVERIFIED | from memory |
| "a site about accessibility must pass access tests" | reasoned, not sourced | judging rubric not read here |
| confidence numbers in section 3 | my estimates | reasons given per row; not measured |
| every listed `re` action exists | VERIFIED | `re manifest` output today |
