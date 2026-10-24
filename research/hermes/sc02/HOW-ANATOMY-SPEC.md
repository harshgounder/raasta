# HOW-ANATOMY-SPEC: the internal data flow, for an anatomy-style /how page

hermes, 2026-10-25 00:50 IST, research and copy. Sources read in full for this file: `app/analyze/RESULTS.md`,
`app/analyze/RECEIPT-SCHEMA.md`, `app/analyze/CALIBRATION.md`, `app/analyze/LIVE-SCAN.md`,
`app/route/README.md`, `app/route/taxonomy/README.md`, `app/route/taxonomy/COUNTS.json`, `eval/C6-RESULTS.md`.
`app/reports/REPORT-BUILD.md` does not exist, so the report stage below rests on what the routing README and
the live site actually implement.

Every number below is measured on this machine or counted in those files. Nothing here is an estimate
unless it says ASSUMPTION.

## 1. The stages in order

| # | stage | input | output | real measured number | what goes wrong | what we do then |
|---|---|---|---|---|---|---|
| 1 | Photo in | camera, upload, drag-drop | JPEG + optional GPS, heading, captured_at | files over 3 MB are downscaled to 2048 px in the browser | downscaling strips EXIF, so the true capture time is lost | the browser sends file time as `captured_at` and the receipt marks the source as form, not exif |
| 2 | Intake, EXIF, condition | image bytes | rotated image, condition bin, sun position | 0.11 to 0.60 s; condition bins day/dusk/night, sharp/soft/blurry, clear/hazy | no EXIF, wrong rotation, night frame read as day | light and blur are classified from pixels, and a night frame downgrades every claim rather than failing |
| 3 | Detector A, YOLOE-11s-seg | image plus 14 text prompts | boxes, labels, A scores | 0.11 to 4.90 s across runs | prompt vocabulary misses a real object, or fires on a painted kerb | scores are kept, not conclusions; anything single-model goes to ABSTAIN above 0.25 |
| 4 | Detector B, OWLv2 | same image, same prompts | boxes, labels, B scores | 3.30 to 5.70 s | B over-fires on texture, which is why one class needed a calibrated single-detector rule | B alone only becomes ACCEPT in the one class that cleared the guard (pole, B >= 0.30) |
| 5 | Agreement | A and B boxes and labels | ACCEPT, ABSTAIN, REJECT per detection | IoU >= 0.3, same family group; a real run gave 1 ACCEPT, 10 ABSTAIN, 30 REJECT | both detectors agree on a wrong label, as happened once on an indoor hallway | agreement is necessary, not sufficient: the footpath-context stage and the VLM can still demote it |
| 6 | SegFormer footpath context | image | verdict footpath / carriageway / mixed / unknown, plus fractions | 0.09 to 1.31 s | a footpath object sits on the road, or the mask calls Indian paving "road" | an A+B agreement on the carriageway becomes ABSTAIN, which removed 428 false accepts |
| 7 | Measure | detections plus horizon, depth, shadow | height in cm with an error, or no height | 0.02 to 0.12 s; a height is printed only when 2 of 3 routes agree within 6 cm and 40 percent; 36 of 289 kerb and step detections reached that bar | a single view cannot separate height from tilt | the receipt says NO_ESTIMATE with the reason, and the route uses the unknown penalty instead of a fake number |
| 8 | VLM, mimo-v2.6-flash | image plus a short question | visible / not_visible / cannot_determine | 12 s cap; tonight 0.03 to 0.08 s to a 401, so it never actually ran | the key is refused, or the model is text-only | the stage is marked used=false with the reason, the page shows "vision check unavailable", and it can only demote an ABSTAIN, never promote anything |
| 9 | Reasoner, deepseek-v4.1-flash | structured context, no image | a short verdict and a reason | 8 s cap; same 401 tonight | a text model inventing geometry it cannot see | it is advisory and cannot change status either way |
| 10 | Placement probability | detection box, GPS, segment graph | placed with p >= 0.7, else ABSTAIN with the top 5 candidate segments | 0.7 threshold; the Jaipur dry run attached 0 of 130 photos, four inside the bbox scored 0.14 and 0.26 | the photo is outside the network, or the GPS is 60 m off | the record stays pending with candidates, and the site says so instead of dropping it |
| 11 | Element taxonomy | detection family, VLM ids | element ids in a 379-element tree | 379 elements, 12 categories, 31 subcategories; 131 mapped to a detector class; 132 detectable from a photo, 161 partial, 86 not | a detected object has no element, or two elements match one box | unmapped detections are listed as unclassified, and the 86 photo-invisible elements stay OSM or prior only |
| 12 | Body impact engine | element plus context | verdict per body: block, cost, warn, none | 74 bodies, 8 scoring functions, 28,046 cells per context, 5 contexts, matrix 1.28 MB, 9.6 s to compute all of it | the matrix is assumption-heavy: only 52 of 379 elements name a source | the page prints the matrix's own note, and the receipt marks which rows are sourced and which are assumed |
| 13 | Combination rules | element pairs | 22 compound elements | 46 rules, 26 of which create a compound, 21 with a named source | rain plus pothole plus night behaves differently from the sum of three costs | compounds carry their own verdicts, and the receipt names the rule that fired |
| 14 | Route cost | element verdicts, profile, hour, weather | seconds and blocks per segment | per-barrier costs by profile in `assumptions.json`; unknown share priced separately | the cost is an assumption stack | every cost is named in the receipt, and the profile row is printed with it |
| 15 | Route and confidence | graph, costs | route, minutes, tier counts, confidence inputs | the demo route reports 42 segments, 0 verified, 42 unknown, and an uncertainty cost in seconds that is not minutes | confidence gets read as accuracy | the page calls it evidence confidence and shows coverage and freshness separately |
| 16 | Receipt | everything above | `raasta-receipt-v1` JSON | id `rx-<sha256[:12]>` from image bytes, `img-<sha[:12]>`, timings per stage, thresholds, model ids | a receipt without its inputs is just a claim | the schema never renames fields, and every number carries the photo and the date |
| 17 | Report loop | receipt plus user confirmation | complaint draft with authority, reference, status trail | complaint generated within 24 h of human check in the current copy; 30-day escalation | the wrong authority gets it, or the ticket closes without a fix | jurisdiction is stored per segment, and a closed ticket never clears the barrier: only new evidence does |

Total, measured client-side on three recordings: 10.56 s street, 6.61 s hallway, 4.35 s night. Queue test: a
second scan posted 0.3 s later waited 4.98 s and finished at 11.26 s, so the worker is serial by design.

The one number that must appear wherever accuracy is implied: micro F1 **0.23** on our own 100-image Indian
set, with 46 dev and 54 test after a hash split, and a shipped policy that only changes one class (pole,
B >= 0.30). The calibration file says plainly that the other per-class rules overfit and did not generalise.

## 2. Three machine metaphors

### Metaphor A, the sorting post office
Floor for intake, two clerks at two desks (A and B), a supervisor who compares their slips (agreement), a
pigeonhole wall for 379 element types, then 74 mailbags, one per body, and a dispatch clerk who chooses the
route. The letter gets a date stamp at every desk, which is exactly what a receipt is.

### Metaphor B, the railway signal box
Levers are thresholds, signals are verdicts, the timetable is the profile and the hour curves, the
interlocking is the combination rules (a lever cannot be pulled if another is set), and the train is the
route. Beautiful for showing that most things are gated rather than scored, weaker for showing measurement.

### Metaphor C, the masala chakki mill
A hopper takes the photo, two grinding stones are the two detectors, the sieve is the agreement step (fine
flour passes, coarse stays), graded trays are the element taxonomy, a brass scale weighs impact per body, and
a chute delivers the route. The mill also has a ledger nailed to the wall for receipts, and a jam hatch for
what cannot be ground.

## 3. The pick, and why

**Pick the chakki mill.** Three reasons, in order of weight.

1. The moving parts behave like our system. Two stones must turn together or nothing grinds, which is the
   two-detector rule made physical, and the sieve is not decoration but the thing that decides what becomes
   evidence. A sorting office has that too, but a mill also gives us *grading by size*, which is what a
   379-element taxonomy with block/cost/warn/none actually is.
2. It is Indian, everyday and warm, which matches the santionispirits woodcut language and the story's
   kitchen-and-street register. A signal box is British-railway cold, and the post office, while charming,
   is the most overused metaphor in explainer design.
3. It fails in the right places. A mill jams, and the honest page needs a jam hatch for ABSTAIN, plus a
   visible ledger for receipts. That gives the /how page a place to put the numbers that are uncomfortable:
   0.23 F1 on the scale's calibration card, 0 of 130 placed in Jaipur on the ledger, 86 elements that no
   camera can see sitting in an unground bin.

### Stage-to-part map for the drawing

| stage | mill part |
|---|---|
| photo in | hopper with a chute lip |
| intake and condition | the feed gate and the moisture gauge (light, blur, haze) |
| detector A | upper grinding stone, left-handed |
| detector B | lower grinding stone, right-handed |
| agreement | the sieve drum, with coarse returns falling back into the hopper |
| footpath context | the stone's gap setting, which decides what counts as grain and what is grit |
| measure | the brass dial on the stone axle, marked in centimetres with an error band |
| VLM and reasoner | the taster's small brass spoon, sampling the output and able to say "not flour" |
| placement | the alignment pin that seats the tray under the chute |
| element taxonomy | 379 graded trays in 12 racks |
| impact engine | 74 brass scales, one per body, each with 8 weights |
| combination rules | the gear train that couples two trays so they move together |
| route cost | the chute's slope, set per profile |
| route and confidence | the delivery tray with a freshness tag |
| receipt | the ledger nailed to the wall, one line per grind, dated and signed |
| report loop | the complaint letter tucked in the ledger with the ward's name on it |

Two drawing notes for whoever renders it: the readout panel should show live numbers pulled from the actual
receipts (10.56 s, 1 ACCEPT 10 ABSTAIN 30 REJECT, 379 elements, 74 bodies, 0.23 F1), and the jam hatch must be
visible and labelled ABSTAIN, because hiding the abstention box would make the whole page a lie.
