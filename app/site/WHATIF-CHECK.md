# WHATIF-CHECK: the 15 photos on /what-if, checked by eye

claude, 2026-10-24. Source copy: `research/hermes/sc02/WHATIF-WALL.md` (hermes, 20:05 IST; hermes could not view the pixels).
I opened all 15 proposed images (contact sheets of the originals in `data/online/commons/`) and, for every swap, the replacement too.
Data: `app/site/public/content/whatif.json` field `wall` (the page counts "ends in: we do not know yet" from `ends_unknown`, so the ratio on the page is recomputed from the data, not typed).
Images on the site: `app/site/public/whatif/wNN_cm_XXX.jpg`, max 1280 px wide, JPEG q80, 4.65 MB for all 15 (lazy-loaded after the first 4).

## 1. Every row

| # | question (as printed) | hermes image | what the pixels show | verdict | image on the site | credit printed (author, licence, source) |
|---|---|---|---|---|---|---|
| 1 | What if it is raining? | cm_058 Water puddles | paved footpath by a lake railing, wide rain puddle on the tiles | MATCH | w01_cm_058.jpg | Julyro, CC0, Wikimedia Commons, Kolkata |
| 2 | What if the photo was taken at night? | cm_107 Delhi rain at night | wet street at night, scooters and a bicycle under shop lights | MATCH | w02_cm_107.jpg | Vyacheslav Argenberg, CC BY 4.0, Wikimedia Commons, Delhi |
| 3 | What if a cow is standing on the footpath? | cm_006 Lascar cow | a cow STANDING on a Mumbai footpath, women walking past | MATCH, question reworded: hermes wrote "sits down", the cow stands | w03_cm_006.jpg | Jorge Láscar from Australia, CC BY 2.0, Wikimedia Commons, Mumbai |
| 4 | What if a shop puts its stall out at five in the evening? | cm_034 Vendor on footpath | a hawker under an umbrella on an Ahmedabad footpath, BUT a stock-photo watermark is visible across the umbrella and his face | **SWAPPED** (watermark = the CC BY 4.0 claim is doubtful) | w04_cm_003.jpg: food-stall tables and stools set across a paved Kolkata footpath | Biswarup Ganguly, CC BY 3.0, Wikimedia Commons, Kolkata |
| 5 | What if there is no footpath at all? | cm_200 Gultekdi Road 2 | a narrow paved strip does exist in front of the shops (bikes parked on it), so "no footpath at all" is not what it shows | **SWAPPED** | w05_cm_181.jpg: Sanjauli junction, Shimla, people walking on the road between cars, no footpath anywhere | Biswarup Ganguly, CC BY 3.0, Wikimedia Commons, Shimla |
| 6 | What if the footpath is broken and nobody fixed it? | cm_032 Damaged footpath | broken pavers round a tree pit, bollards; fits, but it comes from the same Roboflow upload set as #4 (see section 2) | **SWAPPED** (provenance) | w06_cm_014.jpg: Bengaluru footpath with slabs pulled up and broken stone along the edge | Ryan from Toronto, Canada, CC BY 2.0, Wikimedia Commons, Bengaluru |
| 7 | What if people park their bikes on it? | cm_201 Gultekdi Road 6 | motorbikes and bicycles parked along the shop fronts, Pune | MATCH | w07_cm_201.jpg | Miteshbhodia, CC BY-SA 3.0, Wikimedia Commons, Pune |
| 8 | What if the whole street is flooded? | cm_098 Chennai flood | street under brown flood water, three men wading | MATCH | w08_cm_098.jpg | Vijayingarsal, CC0, Wikimedia Commons, Chennai |
| 9 | What if the road is steep or there are steps? | cm_180 Rivoli Road Shimla | concrete steps beside a steep path, people walking up | MATCH | w09_cm_180.jpg | Biswarup Ganguly, CC BY 3.0, Wikimedia Commons, Shimla |
| 10 | What if there is rubble or building material lying there? | cm_035 Rubble on footpath | a heap of construction rubble on a tiled footpath | MATCH, KEPT WITH A FLAG: same Roboflow upload set as #4; no watermark seen at full size; it is the only debris-on-footpath image in `data/online` | w10_cm_035.jpg | Vendor on Robolow Universe (spelling as on Commons), CC BY 4.0, Wikimedia Commons |
| 11 | What if carts are parked where the footpath should be? | cm_033 Cart on footpath | a single cart on a roadside dirt edge with no footpath, portrait crop; Roboflow set | **SWAPPED** (weak match + provenance); question reworded from "a cart is parked across the path" to match the new photo | w11_cm_199.jpg: hand carts standing at the shop fronts of a Pune road | Miteshbhodia, CC BY-SA 3.0, Wikimedia Commons, Pune |
| 12 | What if the path is too narrow to pass? | cm_022 Kodaikanal lake path | a young woman posing on a lakeside path that is not narrow; the person is the subject, not the width | **SWAPPED** | w12_cm_250.jpg: narrow Panaji lane with a thin footpath strip and parked scooters | Fredericknoronha, CC BY-SA 4.0, Wikimedia Commons, Panaji |
| 13 | What if the photo is years old? | cm_001 Salt Lake Sector V 2011 | Kolkata footpath, vendor under an umbrella, blue railing; capture date 2011-08-29 in the sidecar | MATCH | w13_cm_001.jpg | Biswarup Ganguly, CC BY 3.0, Wikimedia Commons, Kolkata |
| 14 | What if the whole market spills onto the road at night? | cm_156 Pune Laxmi Road | crowded night market street, parked motorbikes, neon signs (blurred) | MATCH | w14_cm_156.jpg | Amityadav8, Public domain, Wikimedia Commons, Pune |
| 15 | What if the kerb is high but there is a ramp just outside the photo? | cm_013 Noida footpath | long footpath with a high painted kerb, no ramp in view | MATCH | w15_cm_013.jpg | Rashid Jorvee, CC BY-SA 4.0, Wikimedia Commons, place not stated in the sidecar |

Swaps: 5 (#4, #5, #6, #11, #12). Rewordings: 2 (#3, #11). Kept with a flag: 1 (#10).
Every replacement licence was read from its own sidecar JSON in `data/online/commons/`; all are Commons files with CC0, CC BY or CC BY-SA, or public domain.

## 2. The Roboflow set (why #4, #6, #11 went and #10 has a flag)

- Commons pages fetched 2026-10-24 (Parallel web_fetch): `File:Rubble_on_footpath_in_India.jpg` and `File:Vendor_on_footpath_in_India.jpg` were both uploaded 3 September 2026 by User:The Discoverer, Source `https://universe.roboflow.com/vendor/footpath-guide-2/browse`, Author "Vendor on Robolow Universe", licence CC BY 4.0.
- cm_034 (#4) carries a stock-photo watermark (seen at full size across the umbrella). A dataset that holds watermarked stock photos cannot pass on a clean CC BY 4.0 for its images, so the whole upload set is a provenance risk.
- Action for the team: replace #10 with a team photo of rubble on a footpath, or another Commons file with an own-work licence, before the repo goes public.

## 3. The ratio on the page: "3 of 15 questions end in: we do not know yet"

Recounted after the swaps (the swaps changed photos, not answers). Rule I used: the answer gives no value and no route verdict for that spot, only "not known".

| # | ends in "we do not know yet"? | why |
|---|---|---|
| 2 night | yes | shape only, low confidence, never called safe |
| 8 flood | yes | nothing can be measured, blocked until a later dry photo |
| 15 kerb, ramp out of frame | yes | "unknown, go and check" |
| 1 rain | no | the measured kerb keeps its number (lower confidence), wet segments get a cost |
| 12 narrow | no | width range gives block or cost; abstains only when edges are unclear |
| the other 10 | no | each gives a cost, a block, a date or a complaint |

Abstain appears as a part chip on 5 cards (#1, #2, #8, #12, #15); 3 of them end in not knowing. Both facts are visible on the page (chip vs red "ends in" line).

## 4. Hindi lines: ALL DRAFTS, need a native-speaker read by the team

WHATIF-WALL.md had no Hindi. I drafted Hindi for all 15 questions, all 15 answers, the 7 part chips, the page title, lede, ratio line and the "ends in" line, so the site's language switch does not fall back to English. Each wall item carries `"hi_status": "draft, needs a native Hindi read"` in whatif.json.

Lines to check first (most likely to read stiff):
- #1 answer: "हम दावा छोड़कर चेतावनी देते हैं" (we stop claiming and start warning)
- #12 answer: "किनारे साफ़ न दिखें तो हम कुछ नहीं कहते" (abstain)
- #15 answer: "न दिखना न होने जैसा नहीं है" (not seen is not the same as not there)
- chip "abstain" = "कुछ नहीं कहते"; chip "time-aware" = "समय के साथ"
- lede: "ऑटो वाले भैया या पार्षद"

## 5. Files

- `app/site/public/content/whatif.json` (new `wall` + `wall_note`; the old `items` for the map runner are untouched; v1 archived at `archive/site-story-v1/whatif-v1.json`)
- `app/site/public/whatif/` (15 images)
- `app/site/src/pages/whatif.js` (wall section on top, the existing map runner below it under "run a question on the map"; v1 archived at `archive/site-story-v1/whatif-js-v1.js`)
- `app/site/src/pages/page.css` (wi-* styles)
- `app/site/what-if/index.html` (meta description)
- `app/site/tools/shot.mjs` (what-if shot clicks the runner, then scrolls to top)
