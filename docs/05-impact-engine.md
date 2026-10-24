# 05, the impact engine

hermes, 2026-10-25 03:05 IST. Scope: `app/route/hroute/impact.py` (699 lines), the taxonomy under
`app/route/taxonomy/`, and the matrix under `app/site/public/content/impact-matrix.json`. Formulas carry line
references. **ASSUMPTION** marks a chosen number.

## What it is for

One question, asked 28,046 times per context: for this element (a broken kerb, a vendor, a crossing signal) and
this body (a manual wheelchair user, a blind cane user, an eighty-year-old), is the effect a **block**, a
**cost**, a **warning**, or **nothing**? The answer is a letter, not a score, because a judge can argue with a
score and cannot argue with "a 23 cm kerb is a block for this leaf".

## The taxonomy

| level | count | source |
|---|---|---|
| elements | 379 | `taxonomy/COUNTS.json:2` |
| categories | 12 | `COUNTS.json:3` (geometry 52, surface 42, fixed obstacles 33, temporary 60, crossings 27, light and time 37, weather 36, air and noise 28, crowd and safety 14, terrain 19, amenities 9, compound 22) |
| subcategories | 31 | `COUNTS.json:4` |
| elements with a named source | 52 | `COUNTS.json:19` |
| assumption-only elements | 327 | `COUNTS.json:20` |
| detectable from a photo | 132 yes, 161 partial, 86 no | `COUNTS.json:21-25` |
| bodies | 74 | `COUNTS.json:27` |
| bodies per scorer | visual 9, hearing 3, wheeled 9, ambulant 16, cognitive 9, systemic 10, situational 14, elderly 4 | `COUNTS.json:38-47` |
| interaction rules | 46, of which 26 create compounds and 21 have a named source | `COUNTS.json:56-59` |
| cells per context | 28,046 (379 x 74) | `COUNTS.json:62` |
| matrix size and build time | 1,285,243 bytes, 9.6 s | `COUNTS.json:112-113` |

The 86 photo-invisible elements are the honest core of this design: tactile paving wear, governance, noise, heat
and half the weather layer cannot be seen in a street photo, so they enter through OSM tags, weather feeds,
user reports or priors, and the taxonomoy records which.

## Attributes in, intensities out

Each element carries measurable attributes, and each body carries sensitivities. Both are turned into
normalised intensities in `intensities()` at `impact.py:207-226`:

```
vertical   = clamp(vertical_cm / 15)                       impact.py:213    15 cm = full intensity
width      = clamp((comfort - clear_width_cm) / comfort)   impact.py:210,214
             comfort = max(1.33 * min_width_cm_for_body, 120) cm
slope      = clamp(slope_pct / 8.33)                       impact.py:215    8.33 % = MoHUA 1:12
cross      = clamp(cross_slope_pct / 5)                    impact.py:216
noise      = clamp((noise_db - 60) / 40)                   impact.py:217
water      = clamp(water_cm / 20)                          impact.py:218
wait       = clamp(wait_s / 120)                           impact.py:219
visibility_needed, contrast_loss                          impact.py:220-221
plus 15 direct axes (roughness, slip, fall, overhead, glare, flicker, air, heat, cold,
crowd, vehicle, animal, electric, cognitive, effort)       impact.py:223-225
```

The width comfort rule is the only place a body's own limit enters the intensity, which is deliberate: a
90 cm gap is comfortable for one leaf and a hard block for another, and the same physical measurement must
produce different intensities without being re-measured.

## Seconds and risk, the two outputs

`core()` at `impact.py:235-256` computes both:

```
for each axis in SEC:   secs[axis]  = sensitivity[axis] * intensity[axis] * SEC[axis] * mult
for each axis in HAZ:   risks[axis] = clamp(sensitivity[axis] * intensity[axis] * HAZ[axis] * mult)
```

`SEC` and `HAZ` are the scale tables that turn a 0 to 1 intensity into seconds and into a 0 to 1 risk. Two
adjustments follow in the same function: a short ramp costs less time (`secs["slope"] *= min(1, run_m/20)`,
**ASSUMPTION** that 20 m is a full ramp, `impact.py:248`), and a detour is priced as its own time
(`impact.py:249-251`).

## The eight scoring functions

| body family | function | line | what it adds beyond the shared core |
|---|---|---|---|
| wheeled | `score_wheeled` | `impact.py:350` | hard geometry as block, kerb height, cross slope, surface roughness |
| ambulant | `score_ambulant` | `impact.py:374` | steps, camber, slip, fatigue and rest spacing |
| visual | `score_visual` | `impact.py:396` | contrast, tactile guidance, protrusions a cane misses, unseen-hazard model |
| hearing | `score_hearing` | `impact.py:460` | visual signals instead of audio cues, vehicle proximity |
| cognitive | `score_cognitive` | `impact.py:484` | decision load, crowd, predictability, signage |
| elderly | `score_elderly` | `impact.py:505` | crossing time, rest spacing, fall risk, heat and cold |
| systemic | `score_systemic` | `impact.py:527` | air quality, heat, exertion, infection and dust |
| situational | `score_situational` | `impact.py:555` | prams, loads, luggage, trolleys, casts |

The unseen-hazard model is worth its own line because it is the only piece of the visual scorer that is a model
rather than a table (`impact.py:229-232`):

```
unseen = clamp(visibility_needed * sensitivity.visibility * (0.25 + 0.75 * env) * 1.5)
env    = max(context visibility environment, contrast_loss)
```

That is the code version of "a step you cannot see is a fall", and it is why the night and monsoon contexts
change verdicts rather than merely adding a constant.

## Cross-cutting terms, and where the standards enter

`common_terms()` at `impact.py:259-293` encodes two needs every body shares:

```
startup = 2.5 s                                  impact.py:263  NCHRP 562, older pedestrians' start-up
need    = crossing_length / body_speed + startup  impact.py:264
if green_s and need > green_s:
    stranded_risk = clamp(0.6 * (need - green)/green * max(0.4, sensitivity.vehicle))   impact.py:268-269
    secs["crossing_time"] = need - green_s                                            impact.py:270
rest spacing:
if rest_gap_m > rest_spacing_m:
    secs["rest_spacing"] = min(300, (gap/rest - 1) * 30)                              impact.py:283-284
```

and relief, the one negative term, at `impact.py:287-292`: a bench or a shade tree returns up to 30 s times the
leaf's strongest effort, heat or cognitive sensitivity.

## Hard blocks, and the one place a helper changes a limit

`hard_geometry()` at `impact.py:296-309` produces block reasons rather than seconds:

```
narrow = clear_width_cm < limits.min_width_cm
block if vertical_cm > limits.max_vertical_cm and (spans_path or narrow)
helper: max_vertical_cm += 10 cm        impact.py:304-305  ASSUMPTION, a helper can tip a chair ~10 cm higher
```

That `+10` is the only place where a person's presence changes a physical threshold, and it is labelled as an
assumption in the code comment.

## Combination rules

`apply_interactions()` at `impact.py:173-201` runs 46 rules over element attributes and context before scoring.
26 of them create compounds, which is how the taxonomy's 22 compound elements are built, and 21 name a source
(`COUNTS.json:56-59`). The purpose is that two elements together are not the sum of their parts: a puddle plus
a pothole is a hidden depth, and rain plus a vendor plus night is a different street from any one of the three.

## Worked examples, computed from the formulas above

**1. A 23 cm kerb, manual wheelchair, no ramp.**
Element vertical_cm = 23, wheelchair leaf min_width_cm around 75 cm with hand_propelled set. Intensity
`vertical = 23/15 = 1.53 -> clamp 1.0`. The leaf's `max_vertical_cm` is below 23, so `hard_geometry` returns a
block, not a cost. Verdict: **B**, and the route removes the segment at `p >= block_p` (see 04).

**2. A 14 m crossing, 12 s green, elderly walker at 0.79 m/s.**
`need = 14/0.79 + 2.5 = 20.2 s`, stranded by 8.2 s, `short = 8.2/12 = 0.68`, so
`vehicle_stranded risk = 0.6 * 0.68 * max(0.4, sensitivity)`. With sensitivity 0.7 that is 0.29, a **W** with a
cost, which is the honest verdict: crossable, but not comfortably.

**3. A vendor cluster at 19:00 observed at 11:00.**
`p_present = conf * min(1, max(decay, recurrence) * hour_ratio)` from `costs.py:65`, where the hour ratio is
roughly the 19:00 curve value over the 11:00 value. For a market type with a 6 to 10 times evening peak the
cost rises by that factor even with no new photo, which is what makes the same street passable at noon and
blocked at seven.

## What is weak here, and the code says so itself

1. 327 of 379 elements are assumption-only, and the matrix note prints that on the page (`LIVE-SCAN.md:57`).
2. The intensities use single thresholds (15 cm, 8.33 percent, 5 percent camber, 60 dB) where real bodies have
   distributions.
3. The eight scorers overlap: an elderly wheelchair user takes the wheeled scorer plus parts of elderly, and
   nothing in the code composes two scorers for one person beyond the leaf's own sensitivity table.
4. Rest spacing and tactile coverage have no Indian source, so both are assumptions tagged A, exactly as
   `BODY-TAXONOMY.md` records.
