# WHATIF-WALL: the 15 questions a non-expert judge actually asks

hermes, 2026-10-24 20:05 IST, research and copy only. This is the copy for `/what-if`, in the voice of a
grandmother, an auto driver or a local corporator, not an engineer. Each row: the question, a two-line honest
answer, the product part that answers it, and one real image from `~/hypnexis-main/data/online/` with its
sidecar facts.

Verification note, stated once and it applies to every row: a vision read was attempted and is unavailable
on this host right now (the vision helper's remote closed the connection and the commandcode account is out
of credits). So image descriptions below rest on the dataset's own sidecar tags and the file title, which
were produced when the set was built, not on a fresh look at the pixels tonight. Anyone putting these on
the live page should eyeball the 15 images once, it takes a minute and removes the doubt. Paths are shown
relative to `~/hypnexis-main/data/online/`, licences are from the sidecar and travel with the image.

---

**1. "What if it is raining?"**
Water hides the surface, so we stop claiming and start warning: wet segments get a slip cost and any
measured kerb keeps its number but loses confidence.
Part: abstain plus route cost.
Image: `commons/cm_058_Water_puddles_in_road_by_raindrops_jpg.jpg` (Kolkata, CC0, Julyro, 2026-07-29, tags
day, waterlogged_footpath, after_rain).

**2. "What if the photo was taken at night?"**
At night we can still see the shape of the path but not the surface detail, so the segment is marked
low-confidence and never called safe.
Part: abstain.
Image: `commons/cm_107_Delhi_India_Rain_at_night_jpg.jpg` (Delhi, CC BY 4.0, Vyacheslav Argenberg,
2007-09-28, tags night, rain, wet, parked_vehicles).

**3. "What if a cow sits down on the footpath?"**
A cow is a temporary block: we price it for today, we do not repair the map for it, and the route offers a
way around instead of declaring the street broken.
Part: route cost.
Image: `commons/cm_006_Lascar_Hindu_Woman_touching_a_cow_believed_to_be_sacred_in_H.jpg` (Mumbai, CC BY
2.0, Jorge Lascar, 2007-04-27, tags day, animal_on_footpath, obstruction).

**4. "What if a shop puts its stall out at five in the evening?"**
The same footpath is fine at eleven in the morning and impassable at six, so the cost changes with the
clock, and the site shows the hour it is talking about.
Part: route cost, time-aware.
Image: `commons/cm_034_Vendor_on_footpath_in_India_jpg.jpg` (India, CC BY 4.0, Vendor on Robolow Universe,
2023, tags day, vendor_on_footpath, pole).

**5. "What if there is no footpath at all?"**
Then the map says so, and the route prices the road walk with the risk it carries instead of pretending a
path exists.
Part: map plus route cost.
Image: `commons/cm_200_Gultekdi_Road_2_jpg.jpg` (Pune, CC BY-SA 3.0, Miteshbhodia, 2012-10-02, tags day,
parked_bikes, no_footpath).

**6. "What if the footpath is broken and nobody fixed it?"**
We record the break with the date we saw it, and the receipt keeps showing the date, so a year-old break
looks a year old.
Part: scan plus receipt.
Image: `commons/cm_032_Damaged_footpath_in_India_jpg.jpg` (India, CC BY 4.0, Vendor on Robolow Universe,
2023, tags day, broken_footpath, bollards, tree_pit).

**7. "What if people park their bikes on it?"**
Parked bikes turn a footpath into a parking lot for hours at a time, so they are priced as a block, and the
complaint template names parking enforcement rather than construction.
Part: scan plus complaint.
Image: `commons/cm_201_Gultekdi_Road_6_jpg.jpg` (Pune, CC BY-SA 3.0, Miteshbhodia, 2012-10-02, tags day,
parked_bikes_on_footpath).

**8. "What if the whole street is flooded?"**
Flood water means no measurement is possible, so the segment goes to blocked-for-now with the rainfall that
caused it, and clears only on a later dry photo or a user report.
Part: abstain plus complaint.
Image: `commons/cm_098_Chennai_flood_water_logging_near_ofice_nandanam6_jpg.jpg` (Chennai, CC0,
Vijayingarsal, 2015-12-03, tags day, flooding, rain).

**9. "What if the road is steep or there are steps?"**
Steps are a hard block for a wheelchair, not a slowdown, and a steep lane changes the cost for a walker or
an elderly person even when it is step-free.
Part: route cost.
Image: `commons/cm_180_Rivoli_Road_Shimla_2014_05_07_1174_JPG.jpg` (Shimla, CC BY 3.0, Biswarup Ganguly,
2014-05-07, tags day, hill, steps, slope).

**10. "What if there is rubble or building material lying there?"**
Rubble is read as a block on the path, photographed with its date, and the complaint says debris removal
rather than a new footpath.
Part: scan plus complaint.
Image: `commons/cm_035_Rubble_on_footpath_in_India_jpg.jpg` (India, CC BY 4.0, Vendor on Robolow Universe,
2023, tags day, debris_on_footpath).

**11. "What if a cart is parked across the path?"**
Same as a stall: it is a time-bound block, priced where it sits, and the route keeps moving around it.
Part: route cost.
Image: `commons/cm_033_Cart_on_footpath_in_India_jpg.jpg` (India, CC BY 4.0, Vendor on Robolow Universe,
2023, tags day, no_footpath, vendor).

**12. "What if the path is too narrow to pass?"**
Width is measured as a range, and below the chair width it blocks, between the two values it costs, so the
answer is never a plain yes.
Part: scan, with abstain when the edges are unclear.
Image: `commons/cm_022_Way_around_Kodaikanal_Lake_jpg.jpg` (India, CC0, Saral Shots, 2022-03-27, tags day,
footpath, railing, narrow).

**13. "What if the photo is years old?"**
Every segment carries the date it was seen, old segments are drawn as old, and nothing is called safe on the
strength of a photograph from another decade.
Part: receipt.
Image: `commons/cm_001_Sector_V_Salt_Lake_City_Kolkata_2011_08_29_4818_JPG.jpg` (Kolkata, CC BY 3.0,
Biswarup Ganguly, 2011-08-29, tags day, market, vendors_on_footpath, railing).

**14. "What if the whole market spills onto the road at night?"**
Then the evening route is different from the morning one, and the site says which hour the route was
computed for.
Part: route cost, time-aware.
Image: `commons/cm_156_Pune_Laxmi_Road_Shopping_Main_jpg.jpg` (Pune, public domain, Amityadav8,
2010-07-31, tags night, market, parked_bikes).

**15. "What if the kerb is high but there is a ramp just outside the photo?"**
This is the honest one: a kerb is visible here, a ramp is not, and not seen is not the same as not there, so
the answer is "unknown, go and check", not "no ramp".
Part: abstain.
Image: `commons/cm_013_Footpath_Noida_sector_126_jpg.jpg` (India, CC BY-SA 4.0, Rashid Jorvee, 2017-05-25,
tags day, footpath, kerb).

---

## How to render /what-if

- One card per question, image at 4:3 with the licence and author in small type under it, the question as
  the heading, the two lines as the body, and the part as a small chip (`scan`, `route cost`, `abstain`,
  `receipt`, `complaint`, `map`).
- The chip is the teaching moment: three of these fifteen end in `abstain`, which is the product's whole
  argument. Show that ratio somewhere on the page, "3 of 15 questions end in 'we do not know yet'", because
  a judge who sees a system admitting ignorance believes the other twelve answers more.
- Hindi copy: the site is bilingual and these lines need a native read before they go live. I can draft
  them, but someone who speaks Hindi daily should approve, and I would rather say that than ship a bad
  translation.

## Files

Images live under `~/hypnexis-main/data/online/commons/`. Sidecar facts are from
`~/hypnexis-main/data/online/MANIFEST.csv` (327 images with sidecars, 117 geotagged, 290 usable for
detection). All 15 files were confirmed present on disk at 20:02 IST with sizes between 75 KB and 929 KB.
