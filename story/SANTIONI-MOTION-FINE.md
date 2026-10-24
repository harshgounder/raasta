# SANTIONI MOTION, FINE (flip-book capture, 6 px per frame) v1, 2026-10-24

Reference study only. Local only, nothing of theirs ships: we copy grammar (how the camera, panels, text and sound behave), never art, code or sound. Our clean-room rule from `~/site-clones/santioni/` still applies.

Inputs read in full first: `story/STORY-v1.md` (2,327 B), `~/site-clones/santioni/research/m1/MOTION.md` (5,868 B), `~/site-clones/santioni/lab/tools/capture.mjs` (6,140 B), `~/site-clones/santioni/art/SOUND-BIBLE.md`, and the beat sheet in `story/STORY-CRAFT.md` part 3 (lines 170-243, written by another agent while this ran).

Evidence labels used below: **[frames]** = seen in the 6 px capture, **[flow]** = measured by optical flow on the frames, **[code]** = read in their shipped bundle `~/site-clones/santioni/original/site/app.1782836328290.js` or `assets/shaders/compiled.vs` (reference copy on disk), **[ours]** = our proposal, not something Santioni does.

---

## 0. What was captured, and how

| item | value |
|---|---|
| tool | `~/site-clones/santioni/lab/tools/capture-fine.mjs` (new, built from `capture.mjs`, which is unchanged): same Brave launch + WebGL age-gate pass, no 400-step cap, a frame on every step, waits until the shown scroll reaches the target, logs every sound start with its scroll y, blank-canvas guard, `MODE=hold` films a press by time |
| driver | `scratchpad/drive.sh`: one fresh browser per 3,000 px chunk, resumes from the last good frame if the canvas dies |
| step | 6 px per frame over the whole story (0 to 29,925 px). No 12/4 px split was needed: 0.3 to 0.6 s per frame |
| frames | **4,997 good frames**, 0 gaps over 13 px, 7 dead-canvas frames dropped (`run/walk.jsonl`) |
| viewport | 1440 x 900 (1 screen = 900 px) |
| videos | `run/video/all.mp4` (166.6 s at 30 fps, 1 frame = 6 px, so 1 s of video = 180 px of scroll) + 17 per-scene mp4s `run/video/NN-Scene.mp4` (each starts 450 px before its block) |
| contact sheets | labelled with scroll y: `run/sheets/NN-Scene-pK.jpg` (one tile per 36 to 60 px); `re media sheet` per scene: `run/re/sheet-NN-Scene.png` |
| cut detection | `re media scenes` at 0.3 and 0.15: `run/re/scenes-0.3.json`, `run/re/scenes-0.15.json` |
| flow | `run/pairs.jsonl` (per frame pair: layers peeled by RANSAC, speed, scale, drift, colour) and `run/summary.txt` (per 300 px window) |
| holds | `hold/hand/`, `hold/pour/`, `hold/antigravity/` (press at x 660, y 506 where the disc sits, film by time) |
| `re style motion` | `run/re/style-motion.txt`: finds only 6 CSS transitions, `ease`, no scroll timelines. Disagrees with the bundle on purpose: all real motion lives in WebGL and JS tweens (cubic-bezier eases such as `textBoxEase`, `speedUpEase`), which a CSS scan cannot see. The two engines disagree; the bundle is the truth here |

`scratchpad` = `/tmp/claude-1000/-home-liebert511/cc043658-cf6e-4a18-9856-e8de7ef64a10/scratchpad/santioni-fine/`

### Two capture traps found (logged in `~/hermes_logs/reasoning_failures.md`)
1. Puppeteer's default `captureBeyondViewport` made the WebGL canvas come back black after a few hundred shots. `captureBeyondViewport: false` fixed most of it.
2. Under memory pressure the canvas still died now and then (every other launch also failed the gate with exactly 185 bright px). Fix: chunks plus resume plus page reload between gate attempts. Real dark plates were kept (the Transition ink plate never goes below mean luminance 28).

---

## 1. The engine, in one paragraph (this is the whole trick) [code]

There is **one perspective camera for the whole story** (`Story.createCamera`: fov 35, z = 5). Every scene is a 3D diorama stacked down a single tall world column; each scene is given a height in screens (`sceneConfigs`). Scrolling does exactly one thing to the camera: `camera.group.position.y = lerpedScrollY * unitsPerPixelY`, a pure vertical **pedestal down** (crane down) at 1:1 for anything at z = 0. Nothing else is animated on the camera by scroll. So every "camera move" a viewer feels comes from:

- **depth**: a layer at depth z moves `r = 5 / (5 - z)` screen px per scroll px. z = 0 moves with the page (1.0), z = -5 moves at 0.5, z = -20 at 0.2 (looks almost pinned), z = +2.2 at 1.8 (rushes past). Captions sit at z = +0.45, so they move at **1.10** [code + flow agree: 1.1 is the most common speed in every caption window].
- **how each diorama is posed**: worm's-eye, top-down, over-the-shoulder and profile are all authored into the set, not made by moving the camera.
- **frames that pin or release** (a shader holds the panel border on screen, then lets go).
- **time tweens fired by scroll thresholds** (border close-in, caption entrance, inset entrance).

Three more camera facts from the code:
- smoothing: the shown camera follows the scroll target with `Math.lerp(target, value, 0.08)` per frame on desktop (0.9 on mobile). MOTION.md measured the scroll object closing half the gap per frame; the **camera** is a second, slower layer on top: about 90% in 0.46 s and 99% in 0.92 s at 60 fps, if the lerp is per-frame (not verified on a real clock). **This corrects MOTION.md section 2.**
- **velocity tilt**: `camera.group.rotation.x = clamp(lerp(0.002 * scrollDelta, ...0.05), -0.2, 0.2)`: a fast flick tilts the whole world up to 0.2 rad (11.5 degrees) and it settles back. Not visible in a 6 px capture (delta too small); code only.
- **gaze**: `camera.moveXY = 0.5` on desktop, 0 on mobile: the camera drifts with the mouse. Our capture kept the mouse centred.
- **zoom**: the camera zooms exactly once in the story, and not on scroll: holding in AntiGravity tweens `camera.zoom` 1.0 to 1.1 over 6 s (`speedUpEase`, cubic-bezier 0.52, 0.02, 0.02, 1.00) and back on release.

**Measured over the whole run: scale change per 100 px stays between -0.03% and +0.08% in every window** [flow]. Santioni never dollies in or zooms with scroll. Wide to close always happens by changing panels.

---

## 2. Layout and the shot list (scroll y at 1440 x 900)

| # | scene | y range | screens | shot (what the frame is) | camera height / angle (authored) |
|---|---|---|---|---|---|
| 0 | Wander | 0-2250 | 2.5 | full-bleed title over night sky, closes to a framed wide shot of a tiny walking figure | high, wide, looking down a little |
| 1 | Profile | 2250-3375 | 1.25 | big side profile, chest up, inside a tall narrow frame that his head breaks out of | eye level, profile |
| 2 | Approach | 3375-5086 | 1.9 | from behind, over the shoulder, climbing steps toward a monolith; feet inset | low, behind the figure |
| 3 | Near | 5086-7577 | 2.77 | extreme wide: tiny figure at the base of a red disc on a huge slab | worm's-eye on the slab (trapezoid narrowing upward) |
| 4 | Hand | 7577-8927 | 1.5 | first-person-like close-up: his hand reaches in from the right edge over a red surface | close, over the hand |
| 5 | Target | 8927-10367 | 1.6 | figure silhouetted in a red disc seen through a round arch window | straight on, frame in frame |
| 6 | Transition | 10277-12017 | 1.93 | vertical ink streaks flood white to black, red nave rises | no figure |
| 7 | Cathedral | 11567-15167 | 4.0 | deep red nave, eyes inset crosses, figure enters from bottom as a back view, feet inset | crane from high nave down to his eye level |
| 8 | DrinkSelection | 15167-17417 | 2.5 | wide: figure at a pedestal with 3 bottles, then a close-up panel of the bottles slides over | eye level wide, then table level close |
| 9 | DrinkPour | 17417-21017 | 4.0 | first-person-like hand pours into a glass on a column capital, crane down the column to the figure drinking | close, then crane down to medium |
| 10 | AntiGravity | 21017-22793 | 1.97 | eyes close-up (brown to blue), then figure seen **from directly above**, floating in a white vortex | top-down |
| 11 | PillarCrumble | 22793-23918 | 1.25 | columns seen **from below**, tilted diagonals, cracking; inset of him looking up | worm's-eye |
| 12 | Colosseum | 23918-26843 | 3.25 | title plate reprise on red sky with floating rocks, then a colonnade; figure (now blue) walks in from bottom, back view | eye level behind |
| 13-16 | Taste, Collection, Products, Retail | 26843-30482 | 3.4 | flat product pages on red, moving at exactly 1.0 (no depth at all) | none |

Total story 30,825 px = 34.3 screens (MOTION.md layout confirmed by this run's `layout.json`).

---

## 3. Scene by scene, like an editor

Speeds are screen px per 100 px of scroll, from `run/summary.txt` (dominant layers per 300 px window). "1.0" = moves with the page.

### 0. Wander (0-2250, 2.5 screens)
- **0-540, title plate.** Full bleed, dark sky with white cloud mass at the bottom. The title "NOTTURNO EXPERIENCE" is a 3D mesh at z = -1 that scrolls up and off by ~550 [frames]. Speeds: 1.0 (title, page) plus a 0 to 0.2 layer (sky, near pinned). Clouds and wind lines drift sideways on time, 160 to 170 px of horizontal drift per 100 px of scroll at our pace [flow], so the world is alive when the reader stops.
- **the frame closes in.** The panel border starts at the screen edges and pulls in to a padded panel (uPadX 0.18, uPadY 0.13 at 1600 px wide). Its progress is `max(time tween, eased scroll)`: "use scroll or time, whichever is larger" (shader comment) [code]. Seen at 335 to 551: side margins grow from 0 to the panel inset [frames].
- **the frame pins.** The Wander border is held on screen ("moves with scroll and then halts at the border of the next scene": `pos.y -= min(scroll, sceneHeight - screenHeight)`), so for ~1,350 px (about 550 to 1,450) the panel edges stay fixed while the world inside scrolls up behind them [code + frames: bottom border holds near y 780-870]. This is the only pinned frame in act one besides Hand.
- **figure rise.** The hooded figure enters from the panel's bottom edge at ~480 and grows into frame by rising, not by zoom (speed 0.7 to 0.8, he sits at z ~ -2) [flow + code: characterGroup z = -2].
- **insets.** Face close-up inset rises bottom-left at ~780, hands inset bottom-right at ~950, each animates in once with an 800 ms easeOutCubic edge transition when its world position passes mid-screen [code: FloatingFrame] and then rides at 1.1 [flow].
- **text.** Caption 1 at 929, caption 2 at 1169 (sound log). Each box grows from 25% width and slides from the left over 800 ms (`textBoxEase`), lines rise with a 200 ms stagger over 2 s [code: TextBox].
- **sound.** Footsteps (outside) every step of his walk cycle, keyframes 13 and 34 of the anim, volume ramps in at scene progress 0.33-0.5 and out at 0.7-1.0 [code]; wind bed rises over the first 1.5 world units and fades from 22 to 30 [code]; VO 1 and 2 at 929 and 1169 [log].
- **exit.** The pinned frame releases at ~1,450; the whole panel scrolls up while Profile's head appears **above** the next frame edge at ~1,850, i.e. before its own block starts at 2,250 [frames]. Overlap about 0.45 screen.

### 1. Profile (2250-3375, 1.25 screens)
- Shot scale jumps wide to close in one panel change: profile portrait, chest up, the head breaking out of a tall narrow frame (frame break) [frames].
- Motion: 1.0 to 1.1 (figure and captions), plus a 0.3 layer from 2,700: the moon, deep, rises slowly from the bottom right and crosses the next panel's top edge [flow + frames]. A deep object rising slower than the page reads as the camera tilting up toward something far away.
- Text: 2,033 and 2,789 (VO 4, 5).
- Exit (2,960-3,100): the Approach panel slides up **over** the bottom of the profile; the moon sits on top of the new panel's border, linking the two shots.

### 2. Approach (3375-5086, 1.9 screens)
- Back view on steps, figure in the left half, monolith with a small red disc ahead. Speeds drop to **0.4-0.7** across 3,500-4,400: the set is deep, so the scroll reads as a slow crane down past him while the steps in the foreground rise faster than the monolith [flow]. Wind lines and robe move on time.
- Feet inset (close-up, bare feet on the step) rises bottom right at ~4,040 and tweens in at 500 ms easeOutCubic with a 500 ms delay [code: animateIn tweens `stepsclose`].
- Text 3,737 (one caption), VO waits for idle.
- Footsteps fade in at progress 0.5-0.65 and out at 0.85-1.0 [code].
- Exit: Near's trapezoid slab appears below at ~4,630 while the feet inset is still on screen.

### 3. Near (5086-7577, 2.77 screens)
- Extreme wide. The slab with the red disc fills the screen as a trapezoid narrowing upward. Dominant speed **0.2** from 4,700 to 6,900: the slab is far back and almost pinned, while floor lines in front stream past and captions ride at 1.1 [flow]. Reads as a slow push toward the portal with no zoom at all.
- The disc is the first red in the film: red arrives as one object (MOTION.md section 4).
- Text 5,525/5,939 and 6,929 (VO 7 to 9).
- Exit (6,900-7,250): the slab panel scrolls off, the Hand panel's red edge rises into view under it.

### 4. Hand (7577-8927, 1.5 screens): the one sticky shot
- Full-width red panel, a hand reaching in from the right edge: the closest thing to a first-person shot in the site (the viewer's own hand position) [frames].
- **Sticky**: between the scene's top and `top + height - 1 screen` the hand group is pinned (`stickyGroup.position.y = limitTop - scrollTop`) [code]; measured speed **0.0** from 7,127 to 8,027 [flow]. 0.5 screen of pure pin.
- The red "water" texture is scrolled inside the pin in the opposite direction: a counter-scroll layer measured at **-2.0 to -2.9** [flow; code maps the scroll into the water shader's own uScroll]. So the frame is still while its surface flows.
- Interaction: disc "HOLD & MOVE" at about (660, 506). Hold made the hand reach forward into the surface and retract on release (`hold/hand/strip.jpg`).
- Exit: panel unpins and scrolls away at 1.0; Target's arch appears below at ~8,250.

### 5. Target (8927-10367, 1.6 screens)
- Round window (arch with four columns) framing a red disc and the figure's black silhouette with blowing hair. The arch frame moves at 1.0, the disc and figure inside at **0.4**: looking through a window into depth [flow]. The border's progress is the scene's scroll progress directly (scrubbed) [code].
- Text: "taking a deep breath, he steps in." at 8,861.
- Exit into Transition: from ~9,800 the arch scrolls off and the ink streaks rise.

### 6. Transition (10277-12017, 1.93 screens): the ink flood
- Vertical hatch streaks rise from the bottom and eat the frame white to black over **~1,100 px (9,850 to 10,950)**; the streak layer moves at **5.0-5.4x** the scroll [flow], because the line shader is drawn against a fixed camera matrix (`uFixed`) and scrolled by its own uniform [code]. A fast wipe that the reader controls.
- Black hold ~150 px (10,950-11,100, mean luminance down to 28).
- Red rises: the red nave's columns grow up out of the black from 11,000 to 11,500 at 0.3 (deep).
- Cut detector: one of only four hard cuts at threshold 0.3 sits here (10,400) [re media scenes].
- Scene config gives Transition marginTop -0.1 and Cathedral marginTop -0.5: the next scene starts **under** this one by half a screen [code].

### 7. Cathedral (11567-15167, 4 screens): the crane down to eye level
- 11,600-12,300: deep nave, columns at **0.3**, red ground; caption at 11,513 rides at 1.1.
- 12,400-13,500: the **eyes inset** (extreme close-up of his eyes in a wide letterbox panel) rises across the nave at 0.7: whose eyes, before what they see [frames].
- 13,550-14,100: he enters from the bottom edge as a **back view** and grows to fill the left third, his head lands at the altar's height: the long scroll down the nave ends at his eye level looking at the bottles [frames]. Small positive scale (+0.03 to +0.08% per 100 px) only here, from his walk, not the camera [flow].
- 14,075-14,700: feet inset (walking on the red floor) bottom centre; footsteps (inside) from ~10,640 to 15,185 [log; code ramps them in at progress 0.7-0.75].
- Exit (14,500-15,000): the red panel ends in a torn edge, the next wide shot (white ground, red wall, figure at pedestal) slides up under it.

### 8. DrinkSelection (15167-17417, 2.5 screens): wide, then the insert slides over
- Wide at eye level: the figure, a pedestal, three small bottles (blue, green, yellow). Speeds 0.5 to 0.8 [flow]. Blue appears for the first time, on the product, 0.1-2% of frame (MOTION.md).
- **Match on object**: from ~15,900 a second panel (the same three bottles, close, on a table, against black hatch) rises and covers the wide shot from below. Cut detector hit at 16,150-16,700 [re media scenes]. The bottles grow from ~30 px to ~200 px tall by panel change, never by zoom.
- Pick: "CHOOSE FLAVOR" disc. Click turns the chosen bottle with an 800 ms easeOutCubic tween, plays a carousel round robin [code]. Bottle hover sound fired at 16,283 because our idle mouse sat on a bottle [log].
- Exit: DrinkPour's red panel with a black surround rises below at ~16,850.

### 9. DrinkPour (17417-21017, 4 screens): hold, then crane down a column
- First-person-like hand from the left holding the bottle over a glass; "HOLD & POUR" disc on the glass.
- Hold [code + hold film]: disc shrinks to 0.1 over 400 ms and follows the pointer; `pourProgress` 0 to 1 over 3,000 ms linear while held, back over 1,000 ms on release; `pouring/start.ogg` at ~720 ms after press, `pouring/stop.ogg` ~600 ms after release (`hold/pour/hold.jsonl`).
- 18,000-19,500: the glass sits on a column capital; the scroll cranes **down the column** at **0.7** for ~1,500 px [flow]: a vertical travel that carries the eye from the object (glass) to the person (him, below) without a cut.
- 19,150-20,350: he is revealed beside the column drinking, with an inset of the same moment from another angle at right; the blue liquid colour climbs his robe from the hem, scrubbed by scroll (19,900-20,350) [frames].
- Exit: eyes close-up rises (20,300+); his brown eyes become blue at ~20,560: a match cut on the eyes, the colour swap is the cut [frames].

### 10. AntiGravity (21017-22793, 1.97 screens): top-down
- The only **top-down** shot: he floats in a white vortex seen from directly above, blue robe, "HOLD" disc [frames]. Cut detector hit at ~21,000 [re media scenes].
- Hold [code + film]: over 3 s the light beam speeds x8, wind x4, skin wind x3.5, **camera shake** ramps to amplitude 0.0035 world units at 10 Hz on x and y; over 6 s the figure rolls 0.045 pi and slides, and `camera.zoom` goes 1.0 to 1.1. Release reverses over 3/6 s; `antigravity/release.ogg` on release (`hold/antigravity/strip.jpg`).
- Exit: PillarCrumble's red panel rises below at ~22,200 while the vortex is still on screen.

### 11. PillarCrumble (22793-23918, 1.25 screens): worm's-eye
- Columns seen **from below**, tilted on diagonals, cracking; inset of his face looking up (profile, blue) bottom left from ~22,580: the inset is the "who is looking", the panel is "what he sees" [frames].
- Sound: `transitions/crack.ogg`, the loudest file on the site, fires when the scene's scroll progress passes 0.1 (logged at 22,079) [code + log]. It is the only scene with a transition stinger (`SCENE_TRANSITION_AUDIO = {pillarCrumbleScene: {in: "transition_crack"}}`).
- 23,450-23,900: the panel dissolves into red sky with rock fragments floating up (rocks at 0.5) [flow].
- Exit: the title plate returns on the red sky with rocks passing in front of it: a **chapter card** (23,780-24,850).

### 12. Colosseum (23918-26843, 3.25 screens)
- Title reprise at 0.5 (it drifts up at half speed: deep), colonnade arena at 0.4-0.5.
- 25,150-26,100: he enters from the bottom edge as a back view in the blue robe and grows into a large over-the-shoulder figure walking into the arena (the reveal: blue grows to ~12-14% of frame) [frames + flow colour].
- Exit (25,950-26,450): a torn black-and-white floor edge sweeps up at **1.7-1.8x** (a near foreground layer) and wipes to the red "INDULGE NOW ATONE LATER" page. Cut detector hit at 25,950-26,100.

### 13-16. Taste, Collection, Products, Retail
- Flat product UI at exactly **1.0**, no parallax layers at all [flow]. The camera stops being a camera. Jazz bed fades in on Taste's progress 0 to 1.25 [code].

---

## 4. Transition catalogue (how one shot becomes the next)

| type | where (px) | length | mechanics | evidence |
|---|---|---|---|---|
| **slide-over** (default) | every scene boundary | 0.25-0.5 screen overlap | the next panel rises from below and covers the current panel's lower edge; scene triggers overlap 0.25 screen, Transition and Cathedral use negative top margins (-0.1, -0.5 screen) | code + frames |
| **frame break** | Profile (head), Profile to Approach (moon), Colosseum (figure) | 300-600 | an object crosses the panel border and carries the eye into the next panel | frames |
| **pin and release** | Wander 550-1450, Hand 7650-8030 | 0.5-1.5 screens | border or group held on screen, then let go | code + flow 0.0 |
| **inset pre-announce** | Wander face/hands, Approach feet, Cathedral eyes and feet, DrinkPour angle, PillarCrumble face | inset rides 1.1 for 600-1,000 px | a small close-up panel rises inside the wide shot, tweening its edge in over 800 ms when it reaches mid-screen | code + frames |
| **insert on object (match)** | DrinkSelection bottles 15,900-16,700 | ~800 | close-up panel of the same object covers the wide | frames + cut 0.3 |
| **vertical travel (crane) object to person** | DrinkPour 18,000-19,500, Cathedral 11,600-14,100 | 1,500-2,500 | the scroll itself walks the eye down a column or nave to the character | flow 0.2-0.7 |
| **match cut on eyes** | DrinkPour to AntiGravity ~20,560 | instant | brown eyes become blue in the same framing | frames |
| **ink flood (night plate)** | Transition 9,850-11,500 | ~1,650 total (1,100 wipe, 150 black, 400 red rise) | streaks at 5x scroll, fixed-camera line shader | flow + code + cut 0.3 |
| **iris / window** | Target 8,500-9,900 | ~1,400 | round arch frame in front, deep disc behind at 0.4 | flow + frames |
| **crumble to chapter card** | PillarCrumble to Colosseum 23,450-24,850 | ~1,400 | panel breaks into floating rocks, title returns, stinger at progress 0.1 | frames + code |
| **tear wipe** | Colosseum to Taste 25,950-26,450 | ~500 | torn foreground edge sweeping at 1.7-1.8x | flow + cut 0.3 |

Cut density: at threshold 0.3 the whole 30,000 px has only **4 cut zones** (10,400, 16,150-16,700, 21,000, 25,950-26,100). Everything else is continuous. (The 0.2 s "cuts" in the raw detector output are a sampling artefact of the frame-per-step video, not shots.)

---

## 5. Text, sound and interaction timing

### Captions [code: TextBox, VOManager]
- A caption box is a 3D object at z +0.45 (rides at 1.1, a touch faster than the scene).
- It animates in when its centre passes about 60% of the screen height from the top: box scale x 0.25 to 1 and x -0.5 to 0 over 800 ms (`textBoxEase`), background alpha 333 ms linear, text lines rise over 2,000 ms easeOutQuart with a 200 ms stagger (150 ms if more than 4 lines), opacity 1,200 ms with 300 ms delay. A textbox blip (round robin of 6) plays.
- VO waits for the reader: plays only after scroll delta < 0.6 for 100 ms; leaving the panel fades it out. Karaoke highlight from 0.4 s before a word to 0.4 s after.
- Observed caption y (blip + VO): 929, 1,169, 1,745, 2,033, 2,789, 3,737, 5,525, 5,939, 6,215, 6,929, 8,861, 11,513, 14,663, 15,665, 22,187, 22,721. Average spacing in act one: **one caption every 400-700 px**, two captions per scene, placed on opposite sides (left, then right).

### Sound cues by scroll [log + code]

| y | cue |
|---|---|
| 0 (gate yes) | all drones, wind, jazz, interaction loops start at gain 0; drone 1 fades in over 1.2 s |
| 35-5,105 | outside footsteps follow the walk cycle (Wander, Approach) |
| approach / cathedral / antiGravity / taste progress | drone 1 to 2 to 3 to 4 to 5 crossfades ride scene progress (bounds 0-1, 0-1, -0.5-0.5, -0.25-0.5) |
| 10,640-15,185 | inside footsteps (Cathedral) |
| 16,283 / 16,517 | bottle hover, drinking one-shot |
| hold start / end | pouring start/stop, antigravity release, portal base/move loops follow hold |
| 22,079 | crack stinger (PillarCrumble progress > 0.1), the loudest hit on the site |
| Taste | jazz rises with progress |

### Interactions [code + hold films]
- Disc button shows (scale 0 to 1, 600 ms) only while it sits inside its scene's UI box and the box has at least a third of itself on screen; a press only starts a hold when the scroll is idle (|delta| < 1).
- During a hold the bundle sets `scroll.enabled = false` and re-enables 300 ms after release. **In our headless test a synthetic 300 px wheel during the hold still moved the page in all three scenes** (`hold/*/hold.jsonl`), so whether a real trackpad is blocked is UNVERIFIED; treat "scroll locks while holding" as the intent, not a measured fact.
- Hold beats get the most room: Cathedral and DrinkPour are 4 screens each, Hand 1.5 with a 0.5-screen pin, AntiGravity ~2.

---

## 6. Scale and viewpoint: the answers to the brief's questions

| question | answer |
|---|---|
| any eye-height or camera-height change? | **Yes, but authored per diorama, never by moving the camera's height mid-shot.** Heights seen: high wide (Wander), eye level profile (Profile), low behind (Approach), worm's-eye (Near slab, PillarCrumble), top-down (AntiGravity), table level (DrinkSelection close), and one long crane that ends at his eye level (Cathedral). The global camera only pans down. |
| any first-person shot? | **Two near-first-person shots**: Hand (his hand enters from the right edge, sticky) and DrinkPour (hand and bottle from the left). Plus shot/reverse pairs where an inset of his eyes or face says whose view the panel is (Cathedral eyes, PillarCrumble face). No true POV camera. |
| how wide becomes close | by **panel change plus inset**: a close-up inset rises inside the wide (pre-announce), then the next panel is the close-up. Scale order of act one: wide, close (insets), close-up profile, medium back, extreme wide, extreme close-up hand, frame-in-frame medium. Never a zoom (scale change per 100 px stays under 0.1%). |
| parallax layers | 0.0 (pinned), 0.2 (very far: Near slab, Cathedral deep columns), 0.3-0.5 (far sets, moon, colonnade, title reprise), 0.7-0.9 (characters and mid sets), 1.0 (panel plane, product UI), 1.1 (captions, insets), 1.7-1.8 (near foreground tear), 5x (fixed-camera ink streaks), -2 to -3 (counter-scrolling texture inside a pin) |
| camera per 100 px | always: 100 px pedestal down for the z = 0 plane. Felt moves: "slow push" = deep set at 0.2 plus foreground at 1.0+ (Near); "crane down a column" = mid set at 0.7 for 1,500 px (DrinkPour); "tilt up to the sky" = deep object at 0.3 rising (Profile moon); "hold" = 0.0 pin (Hand, Wander frame) |
| where time moves things | clouds, wind lines, robe, hair, walk cycles, line boil (8 fps stepped noise in the shaders), all running while the reader stops; 160+ px of sideways drift per 100 px of scroll in Wander at our slow pace |

---

## 7. Representative frames (scratchpad, 1440 x 900)

Prefix: `/tmp/claude-1000/-home-liebert511/cc043658-cf6e-4a18-9856-e8de7ef64a10/scratchpad/santioni-fine/run/f/`

| y | file | what it shows |
|---|---|---|
| 5 | `y-000056.jpg` | full-bleed title plate, night sky |
| 557 | `y-005572.jpg` | frame closed in, pinned, figure entering from the bottom edge |
| 1,097 | `y-010972.jpg` | wide with face and hands insets, first caption |
| 2,099 | `y-020992.jpg` | Profile close-up breaking its frame |
| 3,599 | `y-035992.jpg` | Approach back view, monolith, deep set at 0.4-0.6 |
| 4,049 | `y-040492.jpg` | feet inset rising inside the Approach panel |
| 5,297 | `y-052972.jpg` | Near extreme wide, slab almost pinned at 0.2 |
| 7,799 | `y-077992.jpg` | Hand, sticky, HOLD & MOVE disc |
| 9,197 | `y-091972.jpg` | Target window: arch at 1.0, disc at 0.4 |
| 10,552 | `y-105525.jpg` | ink flood half way |
| 11,398 | `y-113985.jpg` | red nave rising out of the black |
| 12,701 | `y-127012.jpg` | Cathedral eyes inset over the nave |
| 13,901 | `y-139012.jpg` | crane landed at his eye level, back view, altar ahead |
| 16,397 | `y-163972.jpg` | bottles close-up panel covering the wide |
| 18,401 | `y-184012.jpg` | glass on the capital, crane down the column begins |
| 19,697 | `y-196972.jpg` | he drinks, second-angle inset, blue climbing the robe |
| 21,497 | `y-214972.jpg` | top-down vortex |
| 22,901 | `y-229012.jpg` | worm's-eye columns with the face inset looking up |
| 23,849 | `y-238492.jpg` | chapter card: title reprise in the rock field |
| 25,697 | `y-256972.jpg` | Colosseum, blue figure walking in, back view |

Hold films: `.../santioni-fine/hold/hand/strip.jpg`, `.../hold/pour/strip.jpg`, `.../hold/antigravity/strip.jpg`.

---

## 8. Grammar for our switch-body story

Beats from `STORY-CRAFT.md` part 3 (B1 to B7) and cast heights from `STORY-v1.md`. Everything in this section is **[ours]**, derived from the measured grammar above.

### 8.1 The core rule: eye height lives in the set, the scroll always cranes down
Keep Santioni's engine exactly: one camera (fov 35, z 5), scroll = pedestal down, depth gives every felt move. A body is a **diorama posed at that body's eye height**, stacked in the column. We never animate the camera's height inside a panel except in one place (8.4), the same way Santioni saves its one long crane (Cathedral) for the turn into act two.

How each height reads in this grammar:

| body | eye height | diorama pose (camera inside the set) | depth spread (layer speeds) | frame device | inset ("who is looking") | time motion while idle | sound |
|---|---|---|---|---|---|---|---|
| Billu | 22 cm | worm's-eye: kerb face fills the lower half like a wall, legs and tyres rise on diagonals (PillarCrumble pose) | widest: ground lines in front at 1.6-1.8, kerb edge 1.0, street at 0.3, sky 0.1 | full bleed, no border (he is free) | his one eye (Cathedral eyes inset, letterbox) | whiskers and tail, paw idle | close paws, low rumble |
| Pihu | 95 cm | pram hood as a round window (Target arch), street seen through it | arch at 1.0, street at 0.4 | frame in frame | wheel stuck in a tile (Approach feet inset) | 10 Hz shake 0.0035 on the bump only (AntiGravity shake) | rattle, wheel clatter |
| Zoya | 115 cm | over the shoulder from behind her chair, the next kerb ahead (Approach / Cathedral back view) | chair and hands 0.9, kerb 0.6, street end 0.2 | framed panel | her hands on the rims (Hand: enters from frame edge) | push-rim tick on her push cycle (footstep keyframes) | rim ticks, her music |
| Kamla | 140 cm | medium from behind, walker in the foreground, temple tiny and far (Near slab: goal pinned at 0.2) | walker 1.0, path 0.5, temple 0.2 | framed panel | the next rest spot sign, or her feet | walker taps on a cycle | taps, far bell |
| Kabir | 158 cm | profile close-up with phone (Profile scene), street behind as thin, low-ink hatch | figure and phone 1.0, street 0.3 | tall narrow frame his head breaks out of | the phone screen | earbud beat | music up, street ducked |
| Gunjan | 600 cm | top-down plan of the same street (AntiGravity vortex pose) | flattest: everything 0.9-1.0, the street scrolls like a map | full bleed | wings or the myna's eye | wind lines on time | wingbeats, myna calls |

The measurable signature: **the lower the eye, the wider the spread of layer speeds** (Billu 0.1 to 1.8, Gunjan 0.9 to 1.0). That spread is our "body switch" in numbers, and a flow check like `fine_analyse.py` can verify it on our own build.

The kerb is our moon: the **same kerb appears in every body panel**, at a different screen size and angle, and crosses the panel border at each change (frame break), so the eye has one object to follow through all six heights.

### 8.2 Transition between bodies (one switch, about 1 screen)

```
 current body panel (1.0)                     next body panel
 ┌───────────────────────────┐
 │  street at this height     │  y0           inset of NEXT body's eye/face rises
 │                ┌────────┐  │               bottom corner at 1.1, tweens edge in
 │                │ face   │  │  y0+300       800 ms easeOutCubic at mid-screen
 │                └────────┘  │
 │   kerb crosses the border ▼│  y0+600       kerb breaks the frame edge
 └───────────────────────────┘
   ┌───────────────────────────┐ y0+700      next panel slides up OVER the bottom
   │ same kerb, new height     │              (overlap 0.25 screen = 225 px)
   │ caption box at 60% line   │ y0+900      caption 800 ms, VO after 100 ms idle
```

- order per switch: inset of the next body (pre-announce) at +300 px, kerb frame break at +600, slide-over at +700 with 225 px overlap, caption at about +900.
- sound: crossfade the body stems on the next scene's scroll progress, exactly like Santioni's drone crossfade (bounds 0 to 1 of the incoming panel). No stinger between bodies; save the one stinger for the turn.
- never zoom, never cut hard between bodies: Santioni has only 4 hard cuts in 34 screens, and the switch should feel like turning your head, not a jump.

### 8.3 How long each body holds

Santioni sizing: single-image beat 1.25 screens, walk or pick 2 to 2.5, hold interaction 4, one sticky shot 1.5 with a 0.5-screen pin.

| beat (STORY-CRAFT) | Santioni model | screens | px at 900 |
|---|---|---|---|
| B1 Billu's kerb (hold to open his eye, flick to jump) | Wander: full-bleed title, frame closes in and pins, then a hold | 2.5 + 1.0 for the hold = **3.5** | 3,150 |
| B2 same street, six heights (Pihu, Kamla, Kabir, Gunjan, Zoya; dial ends on Zoya) | five body panels as in 8.1, 1.25 each; Zoya gets 2 (she is the lead, and her chair must be in her first frame) | 4 x 1.25 + 2 = **7.0** | 6,300 |
| (dial version of B2) | DrinkSelection: wide shot, then a pick that swaps the panel | 2.5 | 2,250 |
| B3 at 5, the street closes (drag the sun) | a 4-screen interaction beat (DrinkPour); the drag pauses scroll like a hold | **4.0** | 3,600 |
| night plate between B3 and B4 | Transition ink flood, only one in the whole piece | **2.0** | 1,800 |
| B4 the turn ("Raasta do") | Hand: sticky close-up of Zoya's raised hand, 0.5-screen pin, scroll held for the line | **1.5** | 1,350 |
| chapter card | title reprise "RAASTA" on the new ground (PillarCrumble to Colosseum) | **1.25** | 1,125 |
| B5 the receipt (shutter, print) | DrinkPour hold: press to shoot, progress 0 to 1 over 3 s, paper prints | **4.0** | 3,600 |
| B6 Gunjan's map (pick a body, route draws) | AntiGravity top-down + DrinkSelection pick | **2.5** | 2,250 |
| B7 an ordinary morning + CTA | see 8.4, then the tear wipe to the CTA page | 4.0 + 1.25 = **5.25** | 4,725 |
| total | Santioni is 34.3 | **31.0** | 27,900 |

Captions: two per body panel at most, left then right, one every 400-700 px, as Santioni does.

### 8.4 The one camera-height move we allow: the ending crane (B7)
Santioni's Cathedral spends 4 screens craning down a deep nave until the camera sits at his eye level. Our mirror: B2 climbs the heights by **cuts** (the problem is fragmented, every body alone), and B7 descends them as **one continuous crane** from Gunjan's 600 cm to Billu's 22 cm over the same street, passing each body at its own height as each card lands: Zoya at the office (115), Kamla at the bell (140), Pihu asleep (95), Kabir looking down at a kerb (158, seen from above as we pass), Billu mid-jump on the B1 kerb (22). Built as one tall diorama: the street plan at the top (top-down) curving into street level at the bottom, so the pedestal-down scroll reads as the bird dropping to cat height. Depth spread should widen as we descend (0.9-1.0 at the top to 0.1-1.8 at the bottom), the measured signature from 8.1. End on a tear wipe (1.7x foreground edge) into the CTA page "Show us your street", which moves at a flat 1.0 like Santioni's product pages.

### 8.5 Checks we can run on our own build (same tools)
1. `capture-fine.mjs` at 6 px on our site, then `fine_analyse.py` + `fine_summary.py`: per body panel, report the layer-speed spread; Billu must be the widest, Gunjan the flattest.
2. Scale change per 100 px must stay under 0.1% everywhere except B7 if we ever add zoom there (we should not).
3. `re media scenes --threshold 0.3`: no more than about 4 hard cuts in the whole piece.
4. Caption y spacing 400-700 px; every VO only after 100 ms idle.

---

## 9. Red team of this file

| claim | grade | why |
|---|---|---|
| one camera, scroll only pedestals it down | VERIFIED | code (`camera.group.position.y = finalScrollY`) and flow (no scale change over 4,996 pairs) agree |
| captions ride at 1.1 | VERIFIED | code offsetZ 0.45 gives 1.099, flow's most common caption speed is 1.1 |
| Wander frame pins ~550-1,450 | VERIFIED (range approximate) | shader comment + border position in frames; exact start/end px not measured |
| Hand is sticky 0.5 screen | VERIFIED | code limit maths + flow 0.0 for 7,127-8,027 |
| camera lerp 0.08 per frame, 90% in 0.46 s | UNVERIFIED timing | the factor is in code; whether Hydra's lerp is frame-rate adjusted, and the real-clock curve, were not measured (would need frame-exact capture) |
| velocity tilt up to 0.2 rad | UNVERIFIED on screen | code only; a 6 px capture cannot show it |
| scroll locks while holding | UNVERIFIED, contradicted by our test | code sets it, our synthetic wheel still scrolled 300 px in all three holds |
| ink streaks at 5x | VERIFIED as measured | flow 5.0-5.4; the exact shader factor was not read |
| only 4 hard cuts | VERIFIED for this detector and threshold | a different threshold finds more; the claim is about 0.3 |
| sound cue y values | VERIFIED for our pacing | VO waits for idle, so a fast reader hears them later; chunk-start artefacts (y = 3,006, 6,006, ...) were removed |
| "lower eye = wider speed spread" | HYPOTHESIS [ours] | follows from the depth formula and Santioni's worm's-eye vs top-down shots, but it is a design rule for us, not something Santioni states |
| colour % for dark red | WRONG in the raw numbers | the red detector misses the dark maroon of Near/Hand (it reports 0% red there); section 4 of MOTION.md has the better colour numbers, use those |
