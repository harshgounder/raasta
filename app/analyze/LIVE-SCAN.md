# LIVE SCAN, build notes (2026-10-24 23:48 IST to 2026-10-25, claude)

Goal: photograph anything (street, footpath, room, hallway) and see, within about 15 s, everything that
affects movement there, with the model flow visible stage by stage.

## What was built

| piece | file | what |
|---|---|---|
| stage runner | `raasta/scan.py` | the /analyze stages run one by one; each emits an event with its real output |
| VLM + reasoner | `raasta/vlm.py` | opencode-go only: `mimo-v2.6-flash` (vision describer) and `deepseek-v4.1-flash` (text reasoner) |
| body impact | `raasta/impact.py` | looks up `app/site/public/content/impact-matrix.json` or `app/route/hroute/impact.py` at request time; if neither exists: status `loading`, no numbers |
| server | `server.py` | `POST /scan` -> job id; `GET /scan/{id}/events` (SSE); `GET /scan/{id}` (full log); `GET /scan-info`; one worker thread = one job at a time. `POST /analyze` untouched (old copy: `archive/server.v1-before-scan.py`) |
| recorder | `tools/record_scan.py` | runs a scan against the server and saves the event log (used for the site's offline recordings) |
| probe | `tools/probe_opencode_vlm.py` | sends one image to a list of opencode-go models, logs status and latency to `logs/vlm-probe.json` |

Event order: `queued, start, intake, detector_a, detector_b, agreement, vlm_start, footpath_mask, depth,
measure, vlm, impact, reasoner_start, reasoner, placement, receipt, end` (or `error`).
The VLM call starts right after `agreement` in a thread, so it overlaps the GPU work (mask, depth, measure).

## opencode Go model tests (key read in code from ~/.config/opencode/opencode.json, never printed)

1. 23:50 IST, all 18 listed models, image request without session header: every one HTTP 400
   `MissingSessionID` ("Request is missing x-opencode-session"). Fix: send header `x-opencode-session`.
2. 23:52 IST, same 18 + 8 more with the header: every model HTTP 401
   `Upstream request failed: Invalid credential` (gemini-4-argon-contributor and minimax-m3.1-flash-free: 410 ModelDeprecated).
   `opencode run -m opencode-go/qwen3.8-flash` from the CLI fails the same way, so it is the key, not our request.
   Logs: `logs/vlm-probe-run1-all401.json`, `logs/vlm-probe-run2-more401.json`.
3. 00:02 IST (user order: ONLY mimo-v2.6-flash + deepseek-v4.1-flash): image request -> both 401 Invalid credential
   (`logs/vlm-probe-run3-user-pair.json`); text-only request -> both 401 too.
   So "does mimo-v2.6-flash accept images" is UNTESTED: the key is refused before the model is reached.

| model | role | image test | text test | latency |
|---|---|---|---|---|
| opencode-go/mimo-v2.6-flash | vision describer | 401 (key) | 401 (key) | 0.9-1.4 s to the 401 |
| opencode-go/deepseek-v4.1-flash | text reasoner | 401 (key) | 401 (key) | 0.9-1.3 s to the 401 |

Fix needed from the user: a working opencode Go key in `~/.config/opencode/opencode.json`
(provider `opencode-go`, options.apiKey) or `OPENCODE_GO_API_KEY` in the server's environment. The key is read on
every call and a 401 is re-tried after 60 s, so no restart is needed after fixing it.

Before the user order, NVIDIA NIM was tested as a fallback (archived in `archive/vlm.v1-nvidia-chain.py`):
nemotron-3.5-super-vl with thinking off answered the hallway in 3.3 s with good JSON; llama-3.2-11b-vision 2.1 s
on a short prompt but 14 to 40 s timeouts on the long one; gemma-4-31b and llama-3.2-90b timed out at 60 s.
Not used now (user order: opencode Go only).

## Body impact (item 2)

`impact-matrix.json` landed at 00:07-00:08 IST (schema raasta-impact-matrix-v1, 379 elements x 74 bodies x 5 contexts,
letters B/C/W/N). `raasta/impact.py` now reads it (re-read when the file changes, no restart):
- detector family -> matrix element: copied from `app/route/hroute/impact_adapter.py` LEGACY_TO_ELEMENT;
- VLM element id -> matrix element: `SCAN_TO_MATRIX` (claude mapping, judgement calls: e.g. `slippery` -> `polished_granite`,
  `moving_traffic` -> `fast_road_edge`). Indoor ids with no close matrix element (door, threshold, clutter, rug, wet floor,
  indoor ramp) are listed with "no matching element in the impact matrix", no verdict.
- context: night (intake light) -> `night_dark`, VLM weather rain/wet -> `monsoon_rain_evening`, else `day_clear`.
- B -> block, C -> slow, W -> warn, N -> none. 12 body leaves are table columns; each row also counts all 74.
The matrix's own note says its numbers are ASSUMPTIONS unless the element or body names a source; the page prints that note.
Archived generic version: `archive/impact.v1-generic.py`.

## Site (item 4)

- `app/site/src/pages/scan.js` (v1 archived at `app/site/archive/scan-v1/`), `app/site/src/pages/scan.css`. Landing page,
  story, /map and data.js untouched.
- Inputs: "take a photo" (`capture=environment`), upload, drag-drop anywhere, optional browser GPS (lat, lon, accuracy sent
  as gps_error_m). Files over 3 MB are downscaled to 2048 px in the browser (EXIF lost, so the file time is sent as captured_at).
- Flow diagram: 12 stage nodes, wires animate into the running stage, each node shows model name, time and a one-line real
  output; tapping a node shows its raw event payload (data inspector); event log with server timestamps.
- Photo overlays: A boxes solid, B boxes dashed, agreement lines with IoU, SegFormer mask PNG, depth PNG, vision verdict
  rings, final ACCEPT in red. Layer toggles.
- Final card: elements (grouped, icons), per-body table from the matrix, VLM range estimates, "what is not known"
  (every ABSTAIN, unmeasured heights, VLM / reasoner missing, receipt notes).
- Backend URL: `?api=` > saved on the page > `public/config.js` BACKEND_URL. CORS is `*` on the server.
- No backend or unreachable (4 s health check): plays a recording from `public/content/scan-examples/` with a red
  "RECORDING, NOT LIVE" banner. Re-record with `tools/record_examples.sh` (archives the old ones first).
- Note: the site shell's sound gate ("THE SAME STREET / enter") covers the page until clicked; that is existing shell
  behaviour, not this page.

## Timings (GTX 1650, models warm, VLM + reasoner failing fast on 401)

Recordings saved 00:14 IST (`app/site/public/content/scan-examples/`, 864 KB total):

| run | client total s | intake | det A | det B | mask | depth | measure | VLM | reasoner | counts | condition | impact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| street, cm_033 Cart on footpath (CC BY 4.0) | 10.56 | 0.60 | 3.40 | 3.94 | 1.31 | 0.93 | 0.12 | 0.08 | 0.00 | 1 ACCEPT, 10 ABSTAIN, 30 REJECT | day | day_clear, 4 rows |
| hallway, Hospital hallway in Lagos (CC0) | 6.61 | 0.13 | 2.03 | 3.60 | 0.10 | 0.62 | 0.02 | 0.05 | 0.00 | 2 ACCEPT, 0 ABSTAIN, 10 REJECT | day | day_clear, 2 rows |
| night, Bailey Road Patna (CC0) | 4.35 | 0.11 | 0.11 | 3.33 | 0.09 | 0.61 | 0.03 | 0.03 | 0.00 | 1 ACCEPT, 4 ABSTAIN, 36 REJECT | night | night_dark, 3 rows |

Other checks:
- Headless Brave end to end (`node tools/scan-shot.mjs IMAGE`, in app/site): live upload desktop 5.16 s, mobile 390 px
  5.15 s, recording replay OK, no page errors, no horizontal overflow. Shots: `app/site/shots/scan-live*.png`, `scan-rec.png`.
- Queue: two scans posted 0.3 s apart: second got `ahead: 1`, waited 4.98 s, finished at 11.26 s.
- Detector A/B times swing (A 0.1 to 4.9 s, B 3.3 to 5.7 s) between runs on the same warm server; cause not found tonight
  (UNVERIFIED guess: CPU contention from other processes during preprocessing).
- `POST /analyze` re-checked after the change: still returns raasta-receipt-v1 (street1.jpg, 11.7 s; its old NVIDIA judge
  timed out, unchanged behaviour).
- Budget: VLM call 12 s cap, reasoner 8 s cap. With a working key the expected total is detectors (~4-9 s) + the VLM
  part not hidden behind mask/depth + reasoner. NOT MEASURED: no working opencode Go key tonight.

## Known gaps (honest list)

1. opencode Go key refused (401) for every model: the vision describer and the text reasoner never ran. Indoor scenes
   therefore rely on the 14 street prompts only. In the hallway run, A and B agreed on "electric box" and "parked motorcycle
   on sidewalk" for a chair: two detectors agreeing on a wrong label is still possible, and the VLM (which could deny
   it) is not reachable. The VLM is wired to demote ABSTAIN on "deny" but never to touch ACCEPT.
2. mimo-v2.6-flash image support is untested (key). If it turns out text-only, set `SCAN_VISION_MODEL` to an image model
   only with the user's GO (user order: these two models only).
3. Element to matrix mapping for VLM ids is a claude judgement table, not reviewed.
4. Recordings contain no VLM output; re-record after the key works (`tools/record_examples.sh`).
