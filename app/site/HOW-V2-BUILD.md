# /how v2 build notes: the scan mill

claude, 2026-10-25, started 00:35 IST. Goal (user): "the how part of the site needs to show the full internal flow of
data, like the anatomy plugin". Built with the anatomy skill (`~/.claude/skills/anatomy`, MIT), closest example
opened first: `examples/dial-indicator` for the kit API and `examples/arcade-cabinet` for "a thing travels through a
mechanism and trips stages". `scripts/publish.mjs` was NOT run (it pushes to a public gallery).

v1 (7-box list + a flat PHOTO -> A/B -> =? diagram + eval table) archived to `app/site/archive/how-v1/`
(`index.html`, `how.js`, `how.png`). Nothing deleted.

## What the page is

1. **Fig 1, the scan mill** (Hero size): an isometric masala chakki on a bench, the metaphor hermes picked in
   `research/hermes/sc02/HOW-ANATOMY-SPEC.md`. Hover or tap any part: its stage card shows input, output, model, the
   measured number, what goes wrong, what we do, and how long it took in the selected recording.
2. **Run a photo through**: plays one of the three recorded scans (`public/content/scan-examples/*.json`) through the
   mill in the order the events really happened, with a live readout (recorded server clock, what that stage said,
   ACCEPT / ABSTAIN / REJECT counts). The red grain is the photo's evidence; grey bits fall into the ABSTAIN hatch,
   pale bits into the chaff bin (REJECT); the hatch door swings open whenever a stage abstains; the dial tries a
   height; the spoon (vision model) dips and comes back with a 401; the drawer of the element's category opens;
   74 pans sink by the real matrix verdict for that element; the ledger inks a line for the receipt; the wall clock
   hand reads recorded seconds (12 ticks = 12 s per turn). Stages 14, 15, 17 are not part of a scan, so they play
   after the scan, labelled "outside the scan, no timing".
3. **The 17 stages** as a plain card list (phones, judges who want to read), same cards as the figure.
4. **What we are bad at**: a dark ledger of 12 numbers we do not like, each with its source footnote.
5. **Sources**: footnote numbers on every number link to the file list (7 files).

## Stage to part map (all 17 + 3 extra parts)

| # | stage | mill part | in the recorded event log |
|---|---|---|---|
| 1 | photo in | hopper (+ feed duct) | queued, start |
| 2 | intake + condition | feed gate + face-up condition gauge (needle: day / dusk / night) | intake |
| 3 | detector A | upper stone (furrows turn while A runs) | detector_a |
| 4 | detector B | lower stone | detector_b |
| 5 | agreement | sieve on rubber mounts (shakes) | agreement |
| 6 | footpath context | gap wheel on the stone stand | footpath_mask |
| 7 | measure | dial gauge on a post | depth, measure |
| 8 | vision check | taster spoon on an arm | vlm_start, vlm |
| 9 | reasoner | bell on the spoon post | reasoner_start, reasoner |
| 10 | placement | alignment pin under the chute | placement |
| 11 | element taxonomy | cabinet of 12 drawers (one per category) | impact |
| 12 | body impact | 74 scale pans on 8 tiers, grouped by the 7 top body categories | impact |
| 13 | combination rules | gear pair on the cabinet side | impact |
| 14 | route cost | chute with a slope knob | (not in a scan) |
| 15 | route + confidence | delivery tray with a freshness tag | (not in a scan) |
| 16 | receipt | ledger book on the wall shelf + wall clock | receipt |
| 17 | report loop | letter tucked in the ledger | (not in a scan) |
| hatch | ABSTAIN | box with a hinged door, the one engraved label "ABSTAIN" | |
| reject | REJECT | chaff bin behind the sieve | |
| drive | one worker, one GPU | motor, flat belt, jack shaft into the stone stand | |

Anatomy rules applied: one camera (azimuth 58, elevation 30), solids only, four tones of ink #111 on paper #F3F3F3,
ONE lit accent in red #C82924 (the grain), one engraved label (ABSTAIN), no other words in the drawing (titles,
hint and readout live in the card corners), every line ends on something (checked, below).

## Files

| file | what |
|---|---|
| `app/site/how/index.html` | unchanged entry (loads `/src/pages/how.js`) |
| `app/site/how/tools/kit/` | vendored anatomy kit: `iso-kit.mjs`, `lathe.mjs`, `iso.css`, `LICENSE` (MIT) |
| `app/site/how/tools/extract-runs.mjs` | reads the 3 recordings + `impact-matrix.json` + `COUNTS.json`, writes `src/pages/how-runs.gen.js` |
| `app/site/how/tools/build-mill.mjs` | builds the figure with the kit, writes `src/pages/how-mill.gen.js` (SVG + projection + anchors) |
| `app/site/how/tools/preview.mjs` | static preview + 3x zoom of the figure (no Vite) for close-up checks |
| `app/site/how/tools/shot-how.mjs` | screenshots into `shots/how-v2/` + overflow + console checks (`--zoom` for close-ups) |
| `app/site/src/pages/how.js` | the page |
| `app/site/src/pages/how-live.js` | the live layer: moving parts, grain, bits, the replay timeline |
| `app/site/src/pages/how-data.js` | the 17 stage cards, the bad-numbers ledger, the source list |
| `app/site/src/pages/how-mill.css`, `how.css` | figure tokens (palette mapping), page layout |
| `app/site/src/pages/how-runs.gen.js`, `how-mill.gen.js` | generated, do not edit |

Rebuild after a recording or matrix changes:
```
cd app/site; node how/tools/extract-runs.mjs; node how/tools/build-mill.mjs; npm run build; node how/tools/shot-how.mjs
```

Not touched: landing page, `src/story/`, `/map` (`src/map2/`), `/scan`, `/report`, `/what-if`, `data.js`, `src/shell/`.

## Where every number comes from

Each card number has a footnote to its file. Checks I made while copying:

- Timings of the three recordings (intake 0.60 / 0.13 / 0.11 s, A 3.40 / 2.03 / 0.11, B 3.94 / 3.60 / 3.33, mask
  1.31 / 0.10 / 0.09, totals 10.56 / 6.61 / 4.35 s): LIVE-SCAN.md table, and they match the event logs.
- Street run: agreement gives 3 ACCEPT, 8 ABSTAIN, 30 REJECT (from the event log); after the footpath step the final
  receipt says 1 ACCEPT, 10 ABSTAIN, 30 REJECT (two A+B agreements moved to ABSTAIN because the ground reads as
  carriageway, and one B-only electric box became ACCEPT by the pole rule B >= 0.30). The spec quotes only the final.
- Pans: each pan is one body leaf in `impact-matrix.json` order; it sinks by the matrix letter for the run's ACCEPT
  element in the run's context (B 3.4, C 2.2, W 1.1, N 0 units). Street: electric_pole_midpath, day_clear,
  block 28, cost 1, warn 4, none 41 of 74 (from the recording's `all_bodies`).
- **Three different "seconds to compute the matrix"**: spec 9.6 s, taxonomy README 7.6 s, COUNTS.json 6.8 s. The page
  uses COUNTS.json (computed by script, newest). README's verdict table is also older than COUNTS.json (e.g. day_clear
  block 3,901 vs 3,915); the page uses COUNTS.json.
- **Two "F1 0.23"s**: C6-RESULTS.md headline = 98 of 100 images scored, micro P 0.31, R 0.18, F1 0.23; RESULTS.md =
  the 54-image test half, P 0.23, R 0.22, F1 0.23. The ledger line states both.
- Stage 15 (42 segments, 0 verified, 42 unknown) and stage 17 (24 h draft, 30-day escalation) come from the hermes
  spec only; the spec itself says REPORT-BUILD.md does not exist. Stage 17 says "neither is measured yet".
- The recordings contain no vision or reasoner output (401), so the spoon and bell never "answer" in any replay.

## Verification (what was actually run)

| check | result |
|---|---|
| `npm run build` (vite) | passes |
| `node how/tools/shot-how.mjs` (Brave headless, Vite dev) | desktop 1440 and mobile 390: 0 px horizontal overflow, no console errors, no page errors |
| anatomy `scripts/lines.mjs` on the static figure (`CHROME_PATH=/usr/bin/brave`) | `line ends: 0 of 556 ends on 89 lines float` |
| reduced motion | run jumps to one still end frame (`shots/how-v2/reduced-motion-end.png`) |
| 4x close-ups of the drive, stones, hopper | read by eye; fixed a belt drawn off its pulleys and a duct leg that stopped 5.6 units short of the duct |

Shots: `app/site/shots/how-v2/` (desktop-rest, desktop-full, hover, run-01..07, mobile-rest, mobile-full,
mobile-run, reduced-motion-end, z-* close-ups).

## Known gaps (honest)

1. The kit's geometry audit (`kit/audit.mjs`: recorder, settle, depth order) was NOT used: painter's order is
   hand-keyed by assembly depth, which works here because the assemblies stand apart on the bench and there are no
   pipes or cables crossing each other. A dense rebuild should move to the recorder.
2. The line check covers the static art; the live lines (stone furrows, needles, spokes) are drawn on faces between
   outlines but were not run through `lines.mjs` frame by frame.
3. Stage cards are English only (headings, lede and ledger intro have Hindi). 
4. The generated figure module is about 840 KB raw (most of it the 13 hatch-door and 7 x 12 drawer frames).
5. Short stages are stretched to about 1 s so they can be seen; the clock always shows the recorded time.
6. The grain only follows the first ACCEPT row's element; other ACCEPT rows (hallway has 2) are counted, not drawn.
