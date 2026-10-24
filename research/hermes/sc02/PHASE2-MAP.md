# PHASE2-MAP: SC-02 Phase 2, clause by clause

hermes, 2026-10-24 21:20 IST, research only. Source of the clauses: `Phase2_Problem_Statements.pptx`,
SC-02 slide. Source of "what we have": `app/route/README.md` (routing lane), `app/analyze/RESULTS.md`
(detection lane), `eval/C6-RESULTS.md` (our own labelled set). I read all three, and the numbers below are
theirs, not paraphrases.

The four Phase 2 clauses are:

1. Accept user photo reports and update barriers within a minute; expire temporary barriers.
2. Support 3 or more user profiles with different route costs.
3. Give each route a confidence score based on image age and coverage.
4. Report how many route segments have no recent imagery.

---

## Clause 1: photo report in, barrier updated, within a minute

**What a judge will check.** They will hand us a phone, photograph a real blocked ramp or a parked car on a
footpath, and watch the route change while they are standing there. Then they will ask what happens when the
blockage goes away, because a vendor is not a broken kerb.

**One-sentence demo.** "I photograph this blocked ramp, upload it, and by the time I have walked to the next
corner the route has turned amber with the barrier named and its date; the vendor barrier from yesterday is
already marked expired, because a stall is temporary and a kerb is not."

**What we already have.**
- `POST /analyze` takes a multipart image plus lat, lon, heading, captured_at, city and gps_error_m, and
  returns a receipt with per-detection status, class family, scores from two detectors, footpath context and
  measured height where two routes agree (`app/analyze/RESULTS.md`).
- Detection speed on this box is measured, not guessed: median 4.26 s per image warm, p90 5.78 s, across 313
  images with zero crashes.
- Barriers go to `POST /barriers` in the routing service, which attaches to a segment only at p >= 0.7 and
  otherwise returns ABSTAIN with its top five candidate segments (`app/route/README.md`).
- The record schema already carries `permanence` (permanent or temporary), `half_life_h`, `observed_at` and
  `photo`, and the cost model already decays a temporary barrier by half-life and hour-of-day.

**Honest gap.** The chain from upload to redrawn route has never been timed end to end; the 4.26 s is
detection only, attach and redraw are unmeasured. There is no expiry job: half-life currently discounts a
temporary barrier's cost, but nothing flips its status to expired or re-runs the route on a schedule. And the
Jaipur attach currently fails for the photos we have: dry-run attach gave 0 of 130 Jaipur records, because
the photos sit outside the walled-city bounding box and the four inside it scored p = 0.14 and 0.26 against
a 0.7 threshold. So the demo works only after the routing lane widens the network to the photo locations.

---

## Clause 2: three or more profiles, different costs

**What a judge will check.** The same start and end, three profiles, three visibly different routes or
times, and one sensible reason per difference. They will also try a profile they know: a blind user, an
elderly parent, a pram.

**One-sentence demo.** "Same start, same end: the wheelchair route is longer because it refuses the stairs
and the median, the blind route avoids the unmarked crossing, and the elderly route trades 80 metres for a
bench and a lit stretch."

**What we already have.**
- Precomputed files cover seven profiles across two leave times and multiple scenarios
  (`routes.json`), with per-barrier-type costs by profile in `hroute/assumptions.json`.
- The cost model distinguishes hard blocks from seconds, treats a median as blocked for wheelchairs and
  prams, and states the slope rule as the stricter 1:15 from IRC:103-2022 rather than the 1:12 in MoHUA
  2021, printing both in the explanation.
- A route result carries the counts a judge will ask for: segments, known barrier, known clear, OSM-tag only,
  unknown, distance, minutes, uncertainty cost.

**Honest gap.** Profile costs are assumptions, not measurements: no Indian hourly survey of vendors or
footpath parking exists in the model. The blind profile has no detector evidence behind it at all, because
tactile paving and unmarked crossings are not in the current detection classes, so its route differences come
from OSM tags and priors. An honest answer to "how do you know a blind user prefers this" is "we do not, we
encode the preference and say so".

---

## Clause 3: a confidence score per route, from image age and coverage

**What a judge will check.** That the number moves when evidence changes. They will ask what the number
means, and the wrong answer is "accuracy".

**One-sentence demo.** "This route reads 0.3 because 42 of its 44 segments have no photo, and when I clear
the oldest photo from the evidence the number drops further, because confidence here means evidence, not
correctness."

**What we already have.**
- Every segment is tiered as known barrier, known clear, OSM tag only, or unknown, and routes report
  `unknown_share_pct`, `oldest_evidence`, per-tier counts and `uncertainty_cost_s`.
- The uncertainty model is explicit: unseen probability per 100 m, converted to a cost, and only clear-type
  evidence covers length (25 m each side of a label).

**Honest gap.** There is no single 0 to 1 route confidence published yet; the ingredients exist in the route
JSON but nobody has fixed a formula, and a formula invented on stage would be a liability. It must be defined
as coverage times freshness, with the weights written down before the demo, and it must be labelled
"evidence confidence", never "accuracy", because our measured accuracy is low (see the Q&A below).

---

## Clause 4: how many route segments have no recent imagery

**What a judge will check.** A number on screen, and then the follow-up "recent means what". If the answer is
vague, they assume the number is decorative.

**One-sentence demo.** "Of this route's 42 segments, 42 have no photograph at all, so the whole route is
drawn grey and the page says so in a sentence, not a footnote."

**What we already have.**
- The counts are computed today: the Jaipur demo route reports segments 42, verified 0, osm-only 0,
  unknown 42, plus an oldest-evidence field. The network itself is 4,537 segments, of which 264 are
  OSM-observed and 4,273 are generated geometry.
- The receipt line already exists in prose form, which is what the site prints.

**Honest gap.** "Recent" is undefined. The product needs one number (I would use 24 months) written into the
code and the copy, plus a per-city coverage page so the answer is a page, not a console query. Until then the
honest phrasing is "no photograph at all", which is what the file supports.

---

## The four-clause summary, in one table

| clause | have | gap | risk to the demo |
|---|---|---|---|
| photo to barrier in a minute | 4.26 s median detection, attach API, permanence fields | end-to-end untimed, no expiry job, Jaipur attach 0 of 130 | HIGH, this is the clause a judge can physically test |
| 3 plus profiles | 7 profiles, per-type costs, hard blocks vs seconds | costs are assumptions, blind profile has no detector evidence | MEDIUM, visible but explainable |
| route confidence | tiers, unknown share, oldest evidence, uncertainty cost | no published formula, must not be called accuracy | MEDIUM, one slide of definition fixes it |
| segments without recent imagery | exact counts and the prose line | "recent" undefined, no coverage page | LOW, a definition and a page |

---

# Round 2 judge Q&A, 20 questions with short honest answers

1. **What is your detection accuracy?** Low and measured: micro F1 0.23 on our own 100-image Indian set,
   with pole obstruction at 0.48 and parked vehicles at 0.30. We print it on the site instead of quoting a
   benchmark from another country.
2. **Why is it so low?** Two reasons we can name: the footpath-context model was trained on Belgian
   sidewalks and calls most Indian ground "road", and kerb ramp versus no-ramp defeats open-vocabulary
   detectors. We abstain rather than guess, which is why 2,098 of 9,386 detections were abstentions.
3. **Are your labels trustworthy?** They are team labels made with AI assistance and they still need one
   human pass. The review queue is a file in the repo, and we say this before a judge finds it.
4. **Why are there zero verified barriers in Jaipur?** Because the photos we have fall outside the demo
   network's bounding box, and the four inside it attached below our 0.7 threshold. The route page says
   "42 of 42 unknown" rather than pretending.
5. **So what is real right now?** The routing, the cost model, the tier system, the receipts, the
   abstention policy, and 313 processed images. What is not real yet is Jaipur showing observed barriers.
6. **How do you measure a kerb height in centimetres?** Three routes: metric depth, vanishing point with an
   assumed 1.2 to 1.7 m camera height, and shadow altimetry. We print a height only when at least two agree
   within 6 cm and 40 percent, and 36 of 289 detections reached that bar.
7. **Is that height validated against a ruler?** No. There is no photo walk with ground truth yet, so every
   centimetre on the site is an estimate with an error bar, and we say so.
8. **Two models must agree, why does that help?** It converts most of our errors into abstentions instead of
   confident wrong answers: 428 agreements were demoted to abstain once the ground under the object read as
   carriageway. It costs recall and buys precision.
9. **What happens when they disagree?** One model alone becomes ABSTAIN if its score is at least 0.25, else
   REJECT, and the receipt records both scores so anyone can audit the call.
10. **Your judge model failed during the run, does that matter?** It failed on every provider for the batch,
    so we capped it at 8 s per image, added a circuit breaker, and made it unable to promote an abstention to
    an accept. It is support, not the decision.
11. **How do you expire a temporary barrier?** Half-life decay already discounts its cost by hour of day. The
    missing piece is a scheduled job that flips it to expired and recomputes routes, which is on the list.
12. **Can a user report override a photo?** Two channels meet in the same schema with a source field, and
    conflicting evidence becomes a disagreement the receipt shows rather than a silent overwrite. Expiry and
    recency decide which one leads.
13. **How accurate are the route costs?** They are assumptions with names attached, not measurements. We show
    the number, the assumption and the source in the same panel.
14. **What does confidence mean, if not accuracy?** Evidence: how much of the route has been seen, how
    recently, and how much of it is generated geometry. We will not call it accuracy.
15. **How much of your network is generated, not mapped?** In Jaipur, 4,273 of 4,537 segments. They are drawn
    differently and labelled generated, because they say where a footpath would be, not that one exists.
16. **Does it work outside the three demo cities?** The network builder runs for any place with OSM coverage,
    but barrier evidence needs photos, so elsewhere it is honest priors until imagery arrives.
17. **What about privacy, faces and number plates?** We never read plates, and the pipeline is about
    footpaths, not people. Photos come from licensed sources with attribution in the sidecar, and any
    deployment would need a blurring step before upload, which we have not built.
18. **Why not just use Google Maps wheelchair routing?** It exists abroad and covers almost nothing of urban
    India, and it does not show you the evidence behind a segment. Our pitch is the receipt, not the pin.
19. **What is the moat?** The evidence ledger: dated photographs, tiered certainty, and complaints tied to
    the same segment, which compounds with every upload and cannot be copied from a map provider's tiles.
20. **What would you do with one more week?** Wire the ramp versus no-ramp ONNX head, do a 50-kerb ruler walk
    to validate heights, get the human label pass done, and ship the expiry job so temporary barriers actually
    come and go. In that order, because the first two change what we are allowed to claim.
