# STORY v2 build notes (landing page)

## 23:33 IST start
- plan: notes first, archive v1 story to archive/story-v1/, read STORY-v2.md + SANTIONI-MOTION-FINE.md + kit modules, then build a lean three.js scroll story in src/story/ (v2), placeholders for chars, audio wired by MANIFEST.json.
- state: art/out/v3 has 7 bg/map pngs; chars/ not yet there; public/audio/v2 empty.

## 23:36 archive + art
- archived src/story (v1), index.html, content/story.json to archive/story-v1/ (copies; v1 files in src/story will be replaced by v2 files, nothing deleted from archive).
- copied art/out/v3/*.png to public/art/v3/. chars/ empty, audio/v2 empty.
- engine decision: own lean three.js engine in src/story/ (one camera fov 35 z 5; each beat = pinned "shot" panel rendered with scissor; next panel slides up over current with the current drifting 0.25 screen; per-panel virtual camera pedestal + horizontal follow of the cat = real perspective parallax by depth). Kit's big panel compositor not reused (too much to learn by 01:30); kit pieces reused: shell nav. Captions/tags DOM (crisp Hindi). Reduced motion + no-WebGL = static comic strip fallback.

## 23:52 first code written
- src/story/main.js (engine + 10 panels), chars.js (placeholder silhouettes + auto swap from /art/v3/chars/<name>.png), sound.js (MANIFEST.json, recordings only, toggle), lines.js (ALL text, Devanagari from research/hermes/sc02/HINDI-CHECK.md, kid says Dadu), story.css. index.html title -> RAASTA.
- coordinator: user feedback: no wobble on backdrops (removing camera sway, gaze drift, shake, velocity tilt), elements must act (cart pushed + wheel, pothole ripple, scooter with motion lines, myna flaps, people walk), full images every beat.

## 23:53 first full capture done, beat 1 reworked
- npm build passed at 23:44. tools/story-frames.mjs (Vite + headless Brave, /?snap, jpg per step into shots/v2/<tag>/) + tools/story-sheet.py (contact sheet).
- shots/v2/desk/sheet-0-999999.jpg = whole story at 450 px steps (v1 of the engine): all 10 panels render, slide-overs work, flood plate works, CTA works.
- user feedback applied: camera has NO sway, gaze drift, shake or tilt now (backdrops move only by depth parallax with scroll). Elements act: beat 1 vendor pushes a cart in (wheel turns with distance), pothole ripple rings, scooter tears past with motion lines, myna flaps (2 drawings, squash once painted), cat walk cycle a/b on distance.
- maps now FILL the frame and the shot travels START (bottom) to END (top); beat 6 red route wipes up with it.
- temple crane stays inside the painting (plate sized for the rise), no fade seam.
- chars.js: painted files are cropped to alpha box (cat_walk_b had 15% bottom padding), painted cat faces LEFT (REAL_FACING), a walk pair only swaps to paint when both poses exist. cat_walk_b appeared then vanished from art/out/v3/chars (codex re-working?), watcher handles it.
- shots/v2/b1/sheet-0-999999.jpg = beat 1 at 300 px steps.

## 23:57 checkpoint (build passes, playable)
- full captures: shots/v2/desk/sheet-0-999999.jpg (1440x900, 450 px steps), shots/v2/mobile/sheet-0-999999.jpg (390x844, 422 px steps). Captions verified with text (shots/v2/cap/), phone screen renders red with the receipt.
- perf (tools/story-perf.mjs, headless Brave on the AMD iGPU, continuous wheel scroll): median frame 16.7 ms, p95 16.8 ms, 0 page errors.
- placeholders redrawn with real proportions (shoulders, neck, head 1/8), kid holds Dadu's hand, Kamla with dupatta + walker, vendor leaning into the cart.
- portrait phones: figures at 0.78 scale.
- still waiting: painted chars (art/out/v3/chars is empty again), audio/v2 MANIFEST.json (empty).

## 00:00 polish pass
- sound wiring verified with a FAKE manifest served by request interception (tools/story-sound-test.mjs; nothing written to audio/v2): toggle reads "sound on", loop gains follow beat visibility, the beat 4 horn one-shot fired exactly once.
- reduced motion: still comic verified on 390 px (tools/story-still.mjs, shots/v2/still-mobile.jpg), no GL canvas, 0 errors. Still-comic notes moved into lines.js (STILL_NOTES) so all text is in one file.
- flood plate now starts its streaks while sliding in (was a blank paper panel for one screen).
- beat 8: a small red phone rises in Dadu's hand when he shows Kamla the route.

## 00:0x flood + insets
- the ink flood is now an OVERLAY plate fixed to the screen (santioni's uFixed): see-through paper, ink streaks rise OVER the last street shot, black hold, marigold rises, then the temple slides up. Was: a paper panel sliding in blank. shots/v2/flood/.
- close-up insets cut from the approved art (CSS crop, no new art): beat 1 "pothole + open drain", beat 4 "kerb: 18 cm, no ramp". Ride at 1.10 with the 800 ms box ease.
- caught + fixed a syntax break (a comment ate a closing brace) before it shipped: always node --check main.js after a scripted edit.

## 00:03 map direction fix
- map shots were moving content DOWN as you scroll down (camera rose START to END): read as inverted. Now they pedestal down like every other shot (END/temple first, then down to START/home), and the beat 6 red route draws top-down in step with the pedestal so its head stays on screen. shots/v2/map6/.
- waiting on: painted chars (none yet), audio MANIFEST (none yet). Engine swaps both in live.

## 00:10 state
- full desktop recapture: shots/v2/desk/sheet-0-999999.jpg (63 frames, 0 errors). mobile check: shots/v2/mchk/.
- tag labels clamp to the screen (mobile clipped "vendor cart on footpath"); widths cached (no per-frame layout reads).
- Kamla 1.2 -> 1.45 tall in beat 4 (her stop + turn back read too small next to the giant legs in the kerb plate).
- a fresh-context reviewer is reading main.js/chars.js/sound.js for bugs.
- KNOWN ROUGH (honest): figures are code-drawn silhouettes until codex's cut-outs land; beat 7 "ways around" are tags over the walking group, not staged detours; Kabir's hops are small; title cat walks on rooftops (no scooter seat in the title art); no sound until MANIFEST.json exists.

## 00:15 sound landed + review fixes
- public/audio/v2/MANIFEST.json arrived (v2 shape: cues[].cue, beats[], beatGain, roundRobin, variants[].files). sound.js rewritten for it: beds ride per-beat gain x screen share; one-shots fired by STORY EVENTS in main.js (cat paw on each walk contact, scooter pass, the beat 4 horn as the scooter cuts Kamla off, walker taps every other step, Kabir's steps, cane + kid steps, wheelchair roll, phone taps 3 then 1 at +0.45 s, wingbeats on each bird lift, temple bells, tanpura resolve hint in beat 6 and swell into beat 8). AAC first, Ogg fallback (Safari).
- verified (tools/story-sound-test.mjs, real manifest): all 16 cues decode; one scroll through the story fires horn_hit exactly once, scooter once, phone_tap twice, paws 42; bed gains crossfade per beat (street 0.84 in beat 1, wind 0.88 over the maps, market 0.5 in beat 4).
- reviewer (fresh context) findings fixed: old parser did not match the manifest (moot, rewritten); char watcher started before layout (painted art popped in after 6 s) -> starts after layout; resize leaked swap hooks + no debounce -> resetCharSubs + 150 ms debounce + materials disposed; desktop height-only resize ignored -> threshold now phones only; remembered-on listener could re-enable sound after the user turned it off -> dropped on any toggle press; toggle before manifest resolved never loaded buffers -> load after manifest; screen readers got no story text (overlay hidden while off screen) -> overlay aria-hidden + a visually hidden ordered text version of every line.

## 00:15 real-time capture
- tools/story-video.mjs: wheel-scrolls the whole story with lerp ON (as a viewer would) and records it: shots/v2/scroll-desk.mp4 (1280x800 -> 960 wide, 7.6 MB; the raw 320 MB webm was moved to the scratchpad, not shipped). 1 fps tile check: captions box in with text, panels slide over, no blank frames.
- shots/v2/mobile/sheet-0-999999.jpg recaptured (390x844). beat 8 phone scaled down on portrait.
- still waiting for codex's character cut-outs; background watcher is on.

## 00:24 sound helper notes + first painted cat
- sound helper notes applied: beds loop on loopEndSeconds (loopStart 0, both formats); horn_hit latched once per visit (never on scroll back, none in beat 1); walker_tap_4 after the horn as she turns; beat 5 cane_steps_old 0.7, kid_steps 0.45, cane_tap_1 at 0.4; paws ride the walk pose swaps (cat walk frame index change), round robin.
- cat_walk_a.png landed in art/out/v3/chars (side view, faces LEFT, 1024 sq). Copied to public/art/v3/chars/. With only pose a painted, the walk uses pose a for both frames + bob (no painted/placeholder alternation). shots/v2/cat/ shows it in beats 0, 1, 5, 8.
- a background sync copies any new/updated file from art/out/v3/chars to public/art/v3/chars every 20 s until 01:20 (cp -u, adds/updates only).

## 00:40 painted cat + Dadu/kid in
- cat_walk_a + cat_walk_b (approved, pixel-aligned) are in; both poses now crop with the UNION alpha box so the swap never shifts or rescales. Beat 1 sheet with the painted cat walking through: shots/v2/b1/sheet-0-999999.jpg (1500-5400 px, 300 px steps).
- dadaji_kid.png landed (3/4 view, faces LEFT): REAL_FACING set, copied to public.
- story-frames.mjs now waits for 'load' (networkidle0 timed out once the char probes were running).

## 00:57 more figures
- kamla_walker (faces left) and guy_kabir (faces left, phone in hand) landed; REAL_FACING set for both; sync loop copies them to public.
- full desktop recapture with painted cat, Dadu+kid, Kamla: shots/v2/desk/sheet-0-999999.jpg, 0 errors.
- beat 8: the code-drawn red phone is hidden once the painted Dadu is in (it floated on his chest and read as a glitch).
- still to come: zoya_chair, myna_fly, logo_raasta.
