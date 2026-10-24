# ELEMENT x BODY impact engine (taxonomy + engine)

claude, 2026-10-25 ~00:25 IST. Replaces "7 generic profiles" with: 379 elements a walker meets, 74 body leaves
(hermes' 63 leaves from `research/hermes/sc02/BODY-TAXONOMY.md` plus 11 claude additions), 46 combination
rules, and one scoring function per body category. The old 7-profile model (`hroute/costs.py`,
`assumptions.json`) is untouched; the router reaches the new engine through a flag.

## Files

| file | what |
|---|---|
| `build_taxonomy.py` | the single source: archetypes, element rows, body rows, rules, sources. Edit here, then run it |
| `elements.json` | tree category > subcategory > element; every element has attributes on shared axes, temporal pattern, photo detectability, detector class, FACTOR-UNIVERSE refs, source |
| `bodies.json` | tree category > subcategory > leaf; per leaf: scorer, sensitivity vector (same axes), hard limits with sources, aid, speed, hermes needs with N/A flags |
| `interactions.json` | combination rules (when / effect / creates compound / reason / source) |
| `export_matrix.py` | writes `app/site/public/content/impact-matrix.json` and `COUNTS.json` |
| `COUNTS.json` | every count below, computed by script (not typed) |
| `../hroute/impact.py` | the engine: `impact(element, context, body_leaf)` |
| `../hroute/impact_adapter.py` | the flag for routing: `route_with_engine(..., engine="impact", body=...)` |
| `../tests/test_impact.py` | 42 tests (full suite: 74 pass, the 32 earlier route/api tests unchanged) |

Rebuild: `python3 -I taxonomy/build_taxonomy.py; .venv/bin/python taxonomy/export_matrix.py; .venv/bin/python -m pytest -q tests` (from `app/route`).

## Counts (from COUNTS.json, 2026-10-25 00:22 IST)

Elements: 379 in 12 categories and 31 subcategories.

| category | subcategories (elements) | total |
|---|---|---|
| geometry | kerbs 21, stairs_ramps 15, width_slope 16 | 52 |
| surface | holes 21, materials 21 | 42 |
| fixed_obstacles | utilities 11, furniture 14, overhead 8 | 33 |
| temporary_obstacles | parked 11, vendors 10, construction 16, events 13, people_animals 10 | 60 |
| traffic_crossings | crossings 16, moving_traffic 11 | 27 |
| light_time (time of day, sun angle, shadow, lighting, contrast) | time_of_day 11, sun_shadow 9, lighting 9, contrast_signage 8 | 37 |
| weather | rain_water 13, wind_storm 7, heat_cold 11, visibility_weather 5 | 36 |
| air_noise (things in the air, sound) | air 18, noise 10 | 28 |
| crowd_safety | crowd 7, social_safety 7 | 14 |
| terrain_transit | terrain 11, transit 8 | 19 |
| amenities (positive) | rest 9 | 9 |
| compound (created by combinations) | compound 22 | 22 |

Body subcategories (leaves): Mobility > Gait, balance, stature 10, Wheeled 9, Ambulatory aids 7; Sensory >
Vision 7, Hearing 3, Speech 1; Cognitive and neurological > Intellectual and learning 3, Neurological 2,
Sensory processing 1, Mental health 1; Chronic and systemic > Cardio-respiratory 2, Blood disorders 2, Fatigue
and pain 2, Metabolic and continence 2; Age and life stage > Older adults 4, Children and adolescents 2,
Pregnancy 1; Temporary and situational > Pushing wheels 4, Injury and recovery 3, Carrying 2, Accompanied 1,
Baseline 1; Environmental sensitivity > Body-state sensitivities 2, Sensory processing 1, Mental health 1.
(Subcategories for hermes' flat sections C to G are a claude grouping for the tree; scoring stays per leaf.)

Photo detectability: yes 132, partial 161, no 86. Elements mapped to a detector `class_family` / routing
type: 131. FACTOR-UNIVERSE coverage: of the 229 factors in layers L1 to L8 and L14 (the physical, temporal and
environmental layers), 212 are referenced by at least one element; the 17 not referenced are priors or
governance signals, not things a walker meets (2.21 to 2.24 material decay and liability, 4.05, 4.16, 4.23,
4.24 drives and pressure, 5.08, 5.09, 5.11, 5.12 timing priors, 7.02, 7.13 complaint volume and camera
noise, 8.14, 8.24, 8.25 area priors). Those belong in the evidence ledger, not in the element list.

Bodies: 74 leaves in 7 top categories and 25 subcategories. Top: Mobility 26, Sensory 11, Temporary and
situational 11, Chronic and systemic 8, Cognitive and neurological 7, Age and life stage 7, Environmental
sensitivity 4. Scorers: ambulant 16, situational 14, systemic 10, wheeled 9, visual 9, cognitive 9,
elderly 4, hearing 3. 63 leaves are hermes leaves (ids kept, e.g. `B1.1`); 11 are claude additions marked
with `*` in `hermes_id` (guide-dog user, albinism, active rigid chair, low-arm-function chair, step-climbing
power chair, hand-cranked tricycle, leprosy cured, acid-attack survivor, haemophilia, older adult with walker,
no-impairment baseline). Every RPwD Schedule sub-condition maps to at least one leaf (`rpwd` field).

Need flags across all leaves (`needs` list): A (assumption) 296, SOURCED 29, N7 (tactile, IRC:103) 14,
"-" 54 (tactile not needed).

Rules: 46; 26 create a compound element (22 distinct compounds); 21 rules name a source.

Matrix (379 x 74 = 28,046 cells per context, 5 contexts, computed in 7.6 s, 1.28 MB):

| context | block | cost | warn | none | elements with 3+ different verdicts across bodies |
|---|---|---|---|---|---|
| day_clear (11:00) | 3,901 | 7,941 | 3,137 | 13,067 | 239 |
| night_dark (21:00, no light) | 4,085 | 7,969 | 2,808 | 13,184 | 230 |
| monsoon_rain_evening (18:00) | 5,885 | 9,610 | 3,449 | 9,102 | 241 |
| heatwave_noon (13:00, 45 C) | 4,726 | 9,623 | 3,214 | 10,483 | 220 |
| winter_smog_morning (07:00, AQI 380) | 3,779 | 8,490 | 3,164 | 12,613 | 247 |

The last column is the point the user made: for about 240 of 379 elements, the same element gets three or
four different verdicts depending on the body.

## Same element, different bodies (engine output, not hand-written)

| element, context | mw_self | walking_frame | blind_cane | low_vision_moderate | deaf | autism_sensory | copd_asthma | older_80_frail | pram_stroller |
|---|---|---|---|---|---|---|---|---|---|
| pothole (11:00) | block 91s r0.19 | cost 59s r0.17 | warn 3s r0.46 | warn 1s r0.15 | none 4s r0.02 | none 4s r0.02 | none 4s r0.02 | cost 44s r0.34 | cost 61s r0.06 |
| pothole (21:00) | block 93s r0.34 | cost 61s r0.34 | warn 3s r0.46 | warn 4s r0.43 | none 5s r0.04 | none 5s r0.04 | none 5s r0.04 | block 47s r0.82 | cost 61s r0.09 |
| pothole (18:00, heavy rain) | block 134s r0.59 | block 83s r0.51 | block 59s r1.00 | block 54s r0.60 | warn 10s r0.07 | warn 10s r0.07 | warn 10s r0.07 | block 65s r0.99 | block 64s r0.17 |
| construction_dust (11:00) | none 2s | none 4s | none 4s | warn 9s | none 4s | cost 16s | cost 54s r0.24 | none 7s | cost 16s |
| vendor_handcart (19:00) | block 74s | block 44s | cost 50s | cost 43s | warn 10s | cost 93s | none 6s | block 43s | block 38s |
| loudspeaker_dj (20:00) | none 3s | none 3s | cost 51s | cost 24s | none 4s | block 76s | none 3s | none 3s | none 3s |
| signal_short_green (11:00) | cost 100s | cost 105s | cost 85s | cost 80s | cost 44s | cost 64s | cost 81s | cost 102s | cost 46s |

Darkness changes nothing for the cane user (sighted-only rules are skipped for bodies with no useful vision)
but raises the low-vision and frail-elderly risk; rain turns the pothole into "hole hidden under water" for
nearly everyone.

## How a weight is made (attributes x sensitivity)

```
element attrs (shared axes)          context {hour, light, weather, season, temp_c, aqi, festival, co_present}
   |                                       |
   +---- interaction rules (46) ------------+--> modified attrs (+ compound elements, scored too, worst wins)
   |
   v
presence p = confidence x hour_curve[hour] x season_factor          (only when hour / season given)
   |
   v
SCORER for the leaf's category (8 functions in impact.py) reads the leaf's own sensitivity vector + limits
   intensity_i  = attr_i normalised to 0..1   (vertical/15 cm, slope/8.33 %, cross/5 %, noise (dB-60)/40,
                  water/20 cm, wait/120 s, width = squeeze below max(1.33 x leaf min width, 120 cm))
   seconds      = SUM_i sens_i x intensity_i x SEC_i x scorer_multiplier_i  (+ detour m / leaf speed)
   risk         = 1 - PROD_i (1 - sens_i x intensity_i x HAZ_i x scorer_multiplier_i)
   hard limits  = leaf max kerb / slope / cross slope / water, min width, max AQI / heat / noise / flicker
   cross-cutting terms (hermes section 6): crossing time = length / leaf speed + 2.5 s start-up vs green;
                  rest spacing = rest_gap_m vs leaf rest_spacing_m; surface evenness = roughness axis
   |
   v
verdict = block  if a hard limit is broken or risk >= 0.6       (and p >= 0.5, else a soft 600 s cost)
          cost   if seconds >= 15, or risk >= 0.35 on something that covers the whole path
          warn   if risk >= 0.1 or seconds >= 8     (announce it; a point hazard can be stepped round)
          none   otherwise
router weight for non-block = seconds + risk x leaf risk_penalty_s (300 s default)
```

What differs per scorer (so the same obstruction weighs differently):

| scorer | leaves | what it does that the others do not |
|---|---|---|
| wheeled | 9 | geometry hard limits per chair; crowd eats clear width; small casters x1.3 roughness; hot metal x1.5 for hand-propelled; mud blocks; a helper adds 10 cm to a manual chair's kerb limit |
| ambulant | 16 | per-aid kerb limit (rollator 4 cm, crutches 10 cm, frame 15 cm); wet weather x1.5 slip; fall and crowd jostle weights |
| visual | 9 | cane finds ground objects (`cane_detectable` x `cane_skill`), misses overhead; low vision uses residual vision x light x fog; noise above 75 dB masks traffic; silent EVs; misleading tactile; no visual slowdown for point hazards (warn, not cost) |
| hearing | 3 | cannot hear vehicles from behind on road walks (x1.6); hearing-aid noise; cannot call for help |
| cognitive | 9 | wayfinding load x (1 + crowd); noise and flicker hard limits (autism 100 dB, photosensitive epilepsy flicker 0.7) |
| elderly | 4 | fall and slip x1.3 (fracture); wet x2 slip; ageing eyes; heat by temperature |
| systemic | 10 | air x AQI; heat x temperature; hard block at the leaf's air limit (CPCB severe band) or heat limit |
| situational | 14 | delegates by mode: pram/trolley/luggage use wheeled rules plus child exposure; crutches/cast use ambulant; child gets vehicle x1.5, dog x1.5, deep-drain block; pregnancy slip/fall/heat x1.3 to 1.4 |

## Sourced vs assumed (every number is labelled)

SOURCED (key in `SOURCES`, read level in brackets):

| number | source |
|---|---|
| kerb 15 cm standard; riser 150 mm | IRC:103-2012 cl 6.2.1 (verified, VERIFY-STANDARDS.md) |
| kerb ramp 1:15 = 6.67 % (wheelchair hard limit) | IRC:103-2022 cl 6.7 Fig 48 (verified) |
| ramp 1:12 = 8.33 % (active-user chair limit) | MoHUA HG 2021 cl 3.7.2 (verified) |
| ramp width 900 mm; walkway 1200 / 1800 mm | MoHUA HG 2021 cl 3.7.3, 3.5.1 (verified) |
| measured Indian kerbs 20 to 25 cm | GTKP 2017 audit (hermes, read) |
| step-climbing chair 20 cm | FACTOR-UNIVERSE S95 (excerpt) |
| cross slope about 3 % one-rim | S96 (excerpt) |
| 10 mm thresholds, chair width about 70 cm | UK Inclusive Mobility, S98 (excerpt) |
| AQI bands and health statements | CPCB NAQI (search excerpts of cpcb.nic.in, 2026-10-24) |
| heat wave 40 C plains, 45 C, severe 47 C | IMD FAQ on heat wave (search excerpt, 2026-10-24) |
| speeds: cane/crutch 0.80, walker 0.63, wheelchair 1.08 m/s; start-up 2.5 s | NCHRP 562 / TCRP 112 (search excerpt) |
| older adults 0.9 / 0.8 m/s; mobility-limited 0.77 m/s | Age and Ageing 2012 (PMID 22695790), 2025 (PMID 41354090) (abstracts) |
| leaf list, RPwD spine, N1 to N8 needs | RPwD Act 2016 Schedule; hermes BODY-TAXONOMY.md |
| obstacle existence in India | FACTOR-UNIVERSE S-numbers via `factor_refs` |

ASSUMPTION (claude unless marked hermes):
- all element attribute values except the rows with a named `attrs_source` (327 of 379 elements are
  assumption-only; 52 name a source, and even then the source backs the obstacle or threshold, not every axis);
- every sensitivity value (scorer base vectors + per-leaf edits, graded from hermes' qualitative columns);
- the verdict thresholds (block risk 0.6, cost 15 s, cost-risk 0.35, warn 0.1 / 8 s), SEC and HAZ scales,
  intensity normalisers, scorer multipliers, the 300 s risk penalty, the 600 s soft block;
- all hour curves except vendor and parked_vehicle, which are the existing assumptions.json curves (also
  ASSUMPTION there); all season profiles; all half-lives;
- every rest spacing (hermes A, quoted per leaf: "assumed, pram, rest spacing 100 m" is in the reason text);
- most hard limits beyond the IRC/HG/S95/CPCB ones (each limit has its own `limit_sources` entry).

## Router flag

```python
from hroute.impact_adapter import route_with_engine
route_with_engine(net, start, end, "mw_self", leave_time, engine="impact", context={"weather": "heavy_rain"})
route_with_engine(net, start, end, "manual_wheelchair", leave_time)           # engine="legacy": old path
```

Adapter rules (after a fresh-context review found over-blocking): labels of the same element within
`dedupe_m` form one cluster (p = max), clusters combine as 1 - prod(1 - p), and block vs soft cost is decided
on that combined p, exactly as `costs.segment_cost` does. A record only counts as co-present for another
(for interaction rules) when its own p >= block_p and both sit within 10 m on the segment (ASSUMPTION); a
record never pairs with itself. The leave time sets the hour, so night rules fire for night routing.

Legacy profile names also work with `engine="impact"` (mapped: manual_wheelchair -> mw_self, power_wheelchair
-> pw_standard, walker_elderly -> older_with_walker, pram -> pram_stroller, crutches -> crutches_bilateral,
low_vision -> low_vision_severe, default_walker -> no_impairment_adult). Evidence presence still comes from
the ledger (`costs.p_present` x `p_attach`); unknown-segment cost still uses the leaf's legacy profile.
The swap of `routing.segment_cost` is thread-local, so concurrent legacy API calls are unaffected (tested).
No endpoint was added (dsh owns Phase 2 endpoints): wire `engine`, `body`, `context` into `/route` there.

## Known limits (red team)

- 86 % of element rows (327 of 379) are assumption-only. The structure is sourced; the magnitudes are design values a
  user study should fit. The site must say so.
- Verdict thresholds were tuned against the brief's examples (pothole x 4 bodies, dust x 2); a different
  tuning would move borderline cells. The tests pin the examples, not the whole matrix.
- Rest spacing compares one element's `rest_gap_m`; the router does not yet sum distance between benches
  along a route.
- The blind leaf "rest every 30 m" is hermes' A value; hermes' cell reads "30 m guides", which may mean
  tactile guidance spacing, not rest. Flag to hermes.
- Compound elements replace the base result only when worse; seconds then take the max of both, so a
  compound never makes a segment cheaper.

## Change 2026-10-25 ~00:30 IST (claude, map review): cane contact with mid-path objects

Found from the site map: `blind_cane x electric_pole_midpath` scored N (none) in day_clear, because the visual
scorer skipped time terms for point obstacles and had no risk term for walking into one. Fix in
`hroute/impact.py` `score_visual`: a fixed object in the walking line (has `clear_width_cm`, `visibility_needed`
>= 0.3, not `spans_path`) adds a `collision` risk (0.4 x contact) and a `find_and_pass` time (12 s x contact), where
contact = miss x visibility_needed x the leaf's visibility sensitivity; guide-dog users get 0.4 of it. All
ASSUMPTIONS. Result: blind_cane x pole = warn (risk 0.22, +8 s); low_vision_moderate and the baseline adult stay
none; guide dog lower. Re-exported the matrix: 905 of 140,230 cells changed across the 5 contexts. Checked five
obvious cases at the same time (tests `test_white_cane_midpath_pole_is_not_none`, `test_obvious_cases_hold`):
blind x open drain = block, low vision severe x open manhole at night = block, deaf x reversing vehicles = warn,
manual wheelchair x steps = block, older adult with walker x 22 cm kerb = block. Full suite: 78 pass.

Per-body routes for the map: `precompute_bodies.py` (app/route) writes `app/site-data/<city>/routes-bodies/<trip>.json`
for every trip x 74 leaves x (08:00 clear, 08:00 rain, 19:00 clear, 19:00 rain, 19:00 no streetlight) via
`impact_adapter.route_with_engine(..., engine="impact")`; 3,700 routes in 74 s.
