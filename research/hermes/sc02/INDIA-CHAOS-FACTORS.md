# SC-02: Indian chaos factors, with the what-if round

Lane S2/hermes, written 2026-10-24 16:48 IST. Research only. Companion: `MAX-INFO-PER-PIXEL.md`.
Purpose: the statement says all of India, any time, season and weather. Indian streets fail in ways that a
European accessibility model does not contain, so this file lists the failure modes, the "what if" a judge
or a wheelchair user would ask, and how the system should answer. Where I have a source I cite it; where I
do not, it says UNSOURCED so nobody quotes it as evidence.

Standard anchors used below: kerb height standard 150 mm, measured Indian footpaths in one audit at 200 to
250 mm (https://www.gtkp.com/document/irf-world-road-meeting-2017-paper-814/). Accessibility audit method
and manhole placement guidance from the UNDP India disability audit 2024
(https://www.undp.org/sites/g/files/zskgke326/files/2024-11/dissability_accessibility_audit_report.pdf).
Footpath width measurement precedent from the CPPR pedestrian audit 2008
(https://www.cppr.in/wp-content/uploads/2012/10/Pedestrian-Audit-Report-2008.pdf). All three fetched
2026-10-24.

## A. Footpath physical failures

| # | factor | what if X | system response |
|---|---|---|---|
| 1 | kerb too high, no ramp | "what if the kerb is 230 mm and no ramp exists" | flag as impassable, quote measured height against the 150 mm standard, route around |
| 2 | broken, missing or incomplete footpath | "what if there is no footpath for 40 m" | the segment becomes "road walking", which is a different and higher risk class, not a no-data hole |
| 3 | unfilled potholes and cave-ins | "what if the pothole is hidden by a puddle" | water plus depth cues, mark as inferred, flag as seasonal |
| 4 | open drains, unclosed manholes, borewell pits | "what if the manhole cover is missing at night" | hard no-go regardless of confidence, this is a safety class, not an accessibility class |
| 5 | broken or tilted paver blocks | "what if the surface is uneven but has no visible step" | surface roughness proxy from texture, low confidence, tagged |
| 6 | footpath used for parking (cars, two-wheelers) | "what if it is clear at 11am and blocked at 7pm" | time-conditional obstruction, this is the leave-time routing input |
| 7 | vendors occupying the path | "what if the market sets up at 6pm" | time-conditional, same mechanism, different detector |
| 8 | construction debris and dug-up trenches | "what if the Metro work moved since last month" | recency stamp on every capture, stale data visibly aged |
| 9 | flooding and waterlogging in monsoon | "what if this route is under 30 cm of water in July" | seasonal flag from stain lines and weather history, not guesswork |
| 10 | no shade, extreme surface heat | "what if the footpath is 55 C at 2pm" | heat exposure as a separate cost channel, matters for elderly users |
| 11 | encroachment by shop extensions | "what if the shop has swallowed half the footpath" | free width versus total width, report both |

## B. Behavioural and rule-breaking chaos

| # | factor | what if X | system response |
|---|---|---|---|
| 12 | two-wheelers riding on the footpath | "what if the safest path is also a bike lane" | risk channel, evidence from tyre marks and motion |
| 13 | people parking on the only ramp | "what if the ramp exists but is blocked 80 percent of the day" | effective accessibility, not nominal accessibility, and say which one is shown |
| 14 | dead traffic lights, no zebra enforcement | "what if the crossing is legal but nobody stops" | crossing risk from vehicle approach evidence, flag as dynamic |
| 15 | fake or faded zebra crossings | "what if the paint is gone but the crossing is still used" | worn-paint detection, mark as faded not absent |
| 16 | jaywalking norms, crowd flow | "what if everyone crosses here anyway" | the route should follow demonstrated desire lines, not only formal ones |
| 17 | stray dogs, cattle, monkeys | "what if a dog is on the ramp" | transient obstruction, not a route property, so it must not poison the score |
| 18 | festival and procession days | "what if the street is closed for a yatra" | calendar events as temporary route closures |

## C. Institutional and data chaos

| # | factor | what if X | system response |
|---|---|---|---|
| 19 | ward boundaries and municipal jurisdiction change | "what if this footpath belongs to a different authority" | jurisdiction tagging, otherwise the complaint goes to the wrong desk and dies |
| 20 | the same street appears in three datasets under three names | "what if Mapillary calls it one thing and OSM another" | street graph matching, with unresolved matches shown as unresolved |
| 21 | imagery is years old | "what if the photo is from 2019 and the road was rebuilt" | every reading carries a capture date, and stale segments are graded |
| 22 | no imagery at all for most of India | "what if there is no street view here" | the ladder: Mapillary, KartaView, phone video, YouTube walking tours, complaint photos, then explicit low confidence |
| 23 | photos are staged or selective | "what if the municipality only photographs the good stretch" | multi-source agreement, plus the shadow clock for time-of-day bias |
| 24 | complaint data is gamed or padded | "what if the grievance portal shows only closed tickets" | cross-check against physical evidence, weight tickets by fix verification |
| 25 | corruption and contractor capture | "what if the audit was written by the contractor" | compelled evidence (CAG, court orders, RTI) as the independent channel |

## D. Human and equity chaos

| # | factor | what if X | system response |
|---|---|---|---|
| 26 | wheelchair, walker, crutch, cane, prosthetic, blind cane, elderly without aids | "what if the user is a blind man with no wheelchair" | the profile changes what counts as a barrier, so it is a parameter, not a footnote |
| 27 | caregiver travelling with the person | "what if two people plus a chair need to pass" | width threshold changes |
| 28 | heat, fatigue, rest stops | "what if 400 m is too far without a bench" | bench and shade as route features, this is the F1 pit-stop metaphor done properly |
| 29 | cost of the trip, not just distance | "what if the accessible route is 900 m longer and costs a rickshaw fare" | time and money both priced |
| 30 | language and literacy | "what if the user reads only Hindi and cannot read the complaint form" | voice-first guidance and one-tap complaint with the RPwD clause pre-filled |
| 31 | women's safety at night on the same route | "what if the accessible route is unsafe after dark" | lighting and open-frontage as safety channels, separate from accessible channels |
| 32 | social stigma and nonconsumption | "what if the person simply does not leave home" | measure trips not taken as a first-class number, not a caveat |

## E. Factors with no data, and how to predict them

This is notice 7 part D. For each factor with no dataset, the honest move is a model with stated priors,
never a silent default:

| factor | prediction route | confidence |
|---|---|---|
| cross-slope | multi-view geometry, then a splat-based measurement | medium, improves with views |
| surface roughness | texture frequency plus a learned proxy, validated on 20 hand-scored patches | low to medium |
| effective accessibility by hour | time-of-day prior from vendor and parking patterns, plus captured timestamps | medium |
| trips not taken | census disability and ageing rates within a 400 m catchment, times an avoidance rate taken from transport accessibility literature | low, and must be presented as an estimate range |
| monsoon failure probability | stain and drainage evidence plus rainfall history for the pin code | medium |
| jurisdiction | municipal ward GIS layers, matched to the street segment | high where the layer exists |

## F. The what-if round that should appear on the site

Ten questions, in the order a judge asks them, each answered by a click rather than a claim:

1. What if the footpath is clear in the morning and blocked at 7pm? (time slider)
2. What if the kerb has no ramp at all? (route fails, alternate offered)
3. What if imagery is from 2019 and the road was rebuilt last year? (stale badge)
4. What if it is monsoon and the underpass floods? (season toggle)
5. What if the person cannot read Hindi? (voice mode)
6. What if the complaint was filed four times and never fixed? (scar ledger)
7. What if the fastest route is unsafe at night? (safety channel)
8. What if there is no street imagery here at all? (honest grey zone)
9. What if two detectors disagree? (abstain and ask for a human look)
10. What if the municipality disputes the measurement? (ruler, date, and the standard cited)

Every one of those has a physical or documentary answer behind it in these two files. That is the
difference between a demo that survives judges and one that only survives a screenshot.
