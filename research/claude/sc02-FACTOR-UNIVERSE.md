# SC-02 FACTOR UNIVERSE (v1, 2026-10-24 ~16:30 IST, claude)

Scope (DECISIONS.md D1 + D2): accessible walking routes from street images for **all of India, any hour, season, weather, terrain**. Method: COPYPASTE-METHOD M1/M2 (the walking route as a convergence point, one lens per layer), M5 (D minus A, Part C), M11 (honest uncertainty, Part B). Format follows `~/sih-idea/05-FACTOR-SPACE-UNIVERSE.md` (14 layers).

Sources: Parallel web_search (model claude-opus-5-5), 29 search calls, run 2026-10-24 15:55 to 16:25 IST. Every S-number below is a URL whose excerpt was read in that window (excerpt-level read, not full-body; see red-team section). Rows tagged **HYPOTHESIS** have no source yet and are design guesses from claude, to be confirmed or killed.

## 0. Legend

**Profiles:** MW manual wheelchair, PW power wheelchair, WK walker, CR crutches, PR pram, BL blind (cane), LV low vision, EL elderly, PG pregnant, CH child, TI temporary injury, LG heavy luggage, ALL everyone.

**Cost effect:** `X` hard block (edge removed for that profile), `+3` heavy penalty, `+2` medium, `+1` light, `0` none, `?` unknown, which is never treated as safe (D2).

**Observed via:** IMG (image cue), SEG (segmentation), DEPTH (monocular / multi-view depth), OSM, DEM (elevation model), WX (weather API / IMD), CAL (clock + calendar), GOV (official data, court, audit), NEWS, USER (user report), IMU (phone motion sensor).

**Cost model sketch (claude design, HYPOTHESIS until built):**

```
edge_cost(e, profile, t) = length(e) * PROD_f  m_f(profile, value_f, conf_f(t))
  m_f = infinity        if factor f is a hard barrier for this profile and conf_f(t) >= tau
  conf_f(t) = conf_0 * 0.5 ^ (age / half_life_f)        (evidence decays, L3 half-lives)
  unknown segment  ->  m = profile_unknown_penalty (MW/PW/BL high, adult walker low), never 1.0
route = argmin over footway graph; if every route has an X for this profile -> say so, show the least-bad one with the barrier named
```

## Part A. The factor universe (348 factors, 14 layers)

### L1. Infrastructure geometry (34)

| ID | factor | unit / measure | observed via | cost effect by profile | source |
|---|---|---|---|---|---|
| 1.01 | Footpath exists at all on this side | bool per side | SEG sidewalk class, OSM sidewalk=*, USER | absent: ALL walk in carriageway; MW/PW/PR/BL/CH +3 | S82, S120 |
| 1.02 | Kerb / footpath height above road | mm (IRC and BMC max 150) | DEPTH at kerb edge | >150 with no ramp: MW X, EL/PG/WK +2, BL trip +1 | S1, S5 |
| 1.03 | Kerb ramp present at crossing | bool | IMG (Project Sidewalk CurbRamp / NoCurbRamp) | missing: MW/PW X at that crossing, PR/LG +2 | S109, S4 |
| 1.04 | Kerb ramp running gradient | ratio (HG 2021 1:12, IRC:103-2022 1:15) | DEPTH plane fit | steeper than 1:12: MW +3 or X, PW +1, WK +2 | S4, S1 |
| 1.05 | Kerb ramp flare gradient | ratio (max 1:10) | DEPTH | steep flares: WK/CR tip +2, BL trip +1 | S4 |
| 1.06 | Kerb ramp width | mm (HG >= 900, BMC >= 1200) | IMG + DEPTH scale | <700: MW/PW X; <900: MW +2 | S4, S5, S98 |
| 1.07 | Ramp bottom lip / gutter step | mm | DEPTH close view, USER | >10 mm: MW caster jam +3, PW +1 | S98 |
| 1.08 | Clear walking width | m (1.8 for two wheelchairs, 1.2 minimum) | SEG + DEPTH | <0.9: MW/PW X, PR +2, BL +1 | S5, S2, S4 |
| 1.09 | Running slope of footpath | % | DEM + IMG horizon tilt | >5%: MW +2, >8.3%: MW +3, EL/PG/WK +2 | S99, S129 |
| 1.10 | Cross slope | % (IRC 1:50 to 1:100) | DEPTH plane | >3%: MW must brake one rim +2; >2.5% "impossible for many" | S96, S98, S2 |
| 1.11 | Footpath height changes every few metres | count per 100 m, mm each | IMG + DEPTH | each step-down: MW X or detour, EL fall +2, BL +2 | S25 |
| 1.12 | Driveway ramps cutting across footpath | count per 100 m, slope 1:8 | IMG | cross-slope warp: MW +1, WK +1 | S3 |
| 1.13 | Footpath continuity across side street | bool (tabletop vs drop) | IMG + OSM junction | drop: MW needs two ramps or X | S3 |
| 1.14 | Abrupt end of footpath | bool | IMG + USER | dead end: MW/PW backtrack +3 or road +3 | S25, S28 |
| 1.15 | Joints, cracks, gaps across path | mm width | IMG close | wide gap: caster trap MW +2, cane catch BL +1 | S2 |
| 1.16 | Drain grating slot width and direction | mm, parallel / perpendicular | IMG | slots parallel to travel: MW/PR caster trap +3, BL cane +2 | S130 |
| 1.17 | Steps or stairs on route | count | IMG, OSM highway=steps | MW/PW X, PR +3, EL/WK/CR +2, LG +2 | S67, S131 |
| 1.18 | Step riser height | mm (150 standard) | DEPTH | >150: EL/PG +2 | S131 |
| 1.19 | Handrails on ramps and steps | bool | IMG | missing: EL/WK/CR/TI +2 | S130 |
| 1.20 | Ramp landings (every 5 m or 9 m of run) | bool | IMG + length | missing: MW fatigue +2 | S130 |
| 1.21 | Median refuge at wide crossing | m | IMG + OSM lanes | none on 4+ lanes: EL/WK/BL +2 | HYPOTHESIS |
| 1.22 | Crossing length | m, lanes | OSM lanes + IMG | long + short green: EL/WK/BL +2 | S66 |
| 1.23 | Foot over bridge as only crossing | type | OSM bridge=yes footway | no working lift: MW/PW X, PR +3 | S67, S68 |
| 1.24 | Subway with stairs only | bool | OSM tunnel + IMG | MW X; monsoon flooded ALL +3 | HYPOTHESIS |
| 1.25 | Bollard spacing at footpath entry | m (0.9 to 1.2) | IMG + DEPTH | <0.9: MW/PW X, PR +2 | S6, S26, S27 |
| 1.26 | Continuous guardrail with no openings | bool | IMG | forces long detour to crossing: ALL +1, MW +2 | S30 |
| 1.27 | Overhead clearance (signs, awnings, branches) | m (HYPOTHESIS >= 2.1) | IMG + DEPTH | low: BL head strike +3 (cane misses it) | HYPOTHESIS |
| 1.28 | Objects protruding into path | mm (BMC max 100) | IMG | BL +3 | S5 |
| 1.29 | Tactile paving present and laid correctly | bool + where it leads | IMG | wrong tactile leads BL into a pole (IRC Fig. 31): BL +3; MW 0 | S1, S30, S118 |
| 1.30 | Tree grate level with paving | mm (max 5 deviation) | IMG + DEPTH | open tree pit: BL/MW/WK +3 | S6 |
| 1.31 | Utility covers flush with surface | mm | IMG + DEPTH | raised: trip EL/BL +2; sunk: caster MW +2 | S6 |
| 1.32 | Turning space at corners | m (1.5 m circle) | IMG | none: MW cannot turn +2 | HYPOTHESIS |
| 1.33 | Footpath on one side only | sides | OSM + IMG | extra crossings: ALL +1, BL/EL +2 | S1 |
| 1.34 | Kerb edge colour contrast | contrast ratio | IMG | none: LV +2 | S4 |

### L2. Infrastructure state and decay (32)

| ID | factor | unit / measure | observed via | cost effect by profile | source |
|---|---|---|---|---|---|
| 2.01 | Potholes at or near crossing | count, depth cm | IMG + DEPTH | MW caster stop +3, BL fall +3; two-wheelers swerve into walkers | S9, S10 |
| 2.02 | Pothole depth | cm | DEPTH, shadow length | deep: MW forward pitch X (threshold HYPOTHESIS ~5 cm) | HYPOTHESIS |
| 2.03 | Broken or missing paver blocks | count per 10 m | IMG texture | MW vibration +2, WK tip +2, BL +2 | S118, S31 |
| 2.04 | Cracked concrete slabs | crack width mm | IMG | +1 most, MW +2 | HYPOTHESIS |
| 2.05 | Loose or rocking drain slab | bool | USER (often not visible), IMG gap | collapse: ALL +3 | S32, S28 |
| 2.06 | Missing drain slab (open box drain under footpath) | gap length m | IMG | fall into drain: ALL X at night, MW X | S31 |
| 2.07 | Wooden planks over drain gaps | bool | IMG | unstable: ALL +3, MW X | S31 |
| 2.08 | Open manhole (cover missing) | bool | IMG + USER | death risk: CH/BL X, ALL +3 | S11, S110 |
| 2.09 | Manhole protective grills installed | share of city | GOV (BMC: 71,426 of 73,437) | lowers fall-through risk under cover | S10 |
| 2.10 | Open borewell or pit near path | bool | USER, rare IMG | CH X | S12 |
| 2.11 | Open trench from utility work | length, depth | IMG | MW/PW/PR X, EL fall +3 | S25, S40, S41 |
| 2.12 | Dug-up footpath left unrestored | days since dug | IMG time series + USER | X until restored | S41, S38 |
| 2.13 | Soil, sand or debris heaps on footpath | length m | IMG | MW/PR X; wet soil slip EL +3 | S40, S39 |
| 2.14 | Half-finished footpath works | % complete | IMG + tender data | partial X | S127 |
| 2.15 | Incomplete bridge / FOB / flyover ramp | bool | IMG + NEWS | edge removed until open | HYPOTHESIS (user example) |
| 2.16 | New footpath crumbling within months | age vs condition | IMG over time | high decay rate, "new" does not mean safe | S33 |
| 2.17 | Surface material class | granite, paver, concrete, bitumen, mud | IMG texture | interlocking pavers and grass raise MW push force +1 to +2 | S100, S120 |
| 2.18 | Slipperiness when wet (polished granite, tiles) | class x rain | IMG material + WX | rain: EL/WK/CR/PG +3 | S5 |
| 2.19 | Surface roughness | vibration RMS | IMU (phone of user), IMG texture | MW spinal pain +2 | HYPOTHESIS |
| 2.20 | Faded zebra crossing | % paint left | IMG | crossing in name only: BL/EL +2 | S63, S69, S70 |
| 2.21 | Heat cracking and UV weathering | class | IMG | slow decay prior | HYPOTHESIS |
| 2.22 | Cheap materials (kerosene in place of emulsion) | not visible | NEWS | faster pothole return (shorter half-life) | S34 |
| 2.23 | Substandard paver blocks with fake receipts | not visible | NEWS | faster decay prior | S35 |
| 2.24 | Defect liability period still active | months | GOV tender | repair more likely, faster | S36 |
| 2.25 | Sewer leak washing soil out (cave-in) | bool | NEWS, USER, IMG sinkhole | ALL X | S45 |
| 2.26 | Bad design (footpath sends water into homes, blocks access) | bool | USER, NEWS | local +2 | S37 |
| 2.27 | Broken bollards lying on footpath | bool | IMG | trip BL/EL +2 | S25, S2 |
| 2.28 | Garbage dumped on footpath | volume | IMG | PR/MW X, BL +2 | S116, S25 |
| 2.29 | Collapsed kerb edge | bool | IMG | MW wheel drop +3 | HYPOTHESIS |
| 2.30 | Temporary patch with height mismatch | mm | DEPTH | trip +1 to +2 | S126 |
| 2.31 | Tree roots heaving slabs | mm | IMG | trip EL/BL +2 | HYPOTHESIS |
| 2.32 | Pothole recurrence on a segment | count per year | GOV complaints | prior for "pothole likely back" | S34 |

### L3. Obstacles, permanent vs temporary, with half-life (34)

Half-life = time after which half of observed instances of this obstacle type are gone from that spot. All half-life numbers are **claude estimates (HYPOTHESIS)** to be fitted from repeat photos; sources back the obstacle, not the number.

| ID | obstacle | P / T | half-life (estimate) | observed via | cost effect | source |
|---|---|---|---|---|---|---|
| 3.01 | Electric pole in middle of footpath | P | 5+ years | IMG | BL collision +3; MW X if width < 0.9 m | S28 |
| 3.02 | Transformer / ring main unit on footpath | P | 5+ years | IMG | width loss; explosion risk ALL +1 | S29, S6 |
| 3.03 | Utility junction boxes on footpath | P | 3+ years | IMG | width loss MW +2 | S24 |
| 3.04 | Tree trunk inside footpath | P | decades | IMG | BL +2, MW width | S28 |
| 3.05 | Bus shelter or fixtures placed after paving | P | years | IMG | width | S1 |
| 3.06 | Telecom cabinets | P | years | IMG | width | HYPOTHESIS |
| 3.07 | Hoarding / signboard poles | P | 1 to 3 years | IMG | BL +2 | HYPOTHESIS |
| 3.08 | Shop platform (otla) built onto footpath | P (illegal) | until a drive, often years | IMG | MW X if steps | S20, S23 |
| 3.09 | Government-licensed booths (e.g. dairy booths) | semi | months | IMG | width | S20 |
| 3.10 | Cafe and restaurant seating spill | T | hours, daily cycle | IMG + CAL | evening +2 | S20, S25 |
| 3.11 | Vendor handcarts | T | hours, same spot daily | IMG + CAL | width, MW X at peak | S22, S88 |
| 3.12 | Fixed vendor kiosk | semi | weeks to months | IMG | width | S22 |
| 3.13 | Two-wheelers parked on footpath | T | minutes to hours, recurring | IMG | MW/PR X if full width | S117, S20 |
| 3.14 | Cars parked on footpath / kerb | T | hours | IMG | MW/PR X | S30 |
| 3.15 | Abandoned vehicles | semi | months | IMG repeat | X | S117 |
| 3.16 | Official vehicles (police, water board) parked | T | hours | IMG | X | S25, S117 |
| 3.17 | Construction pipes and material | T | weeks to months | IMG | X | S38, S39 |
| 3.18 | Construction debris | T | weeks | IMG | X | S127, S115 |
| 3.19 | Garbage heap | T | days, regrows | IMG | PR/MW X | S116 |
| 3.20 | Fallen tree or branch after storm | T | hours to days | IMG, USER, NEWS | X | S52, S124 |
| 3.21 | Dangling cables | semi | months | IMG | BL/CH +2, trip | S53 |
| 3.22 | Police or metro barricades | T / semi | days to years | IMG | X | S115 |
| 3.23 | Festival pandal on footpath or road | T | days to weeks, calendar-bound | IMG + CAL | X, crowd +3 | S61, S62 |
| 3.24 | Wedding tent / shamiana on road | T | 1 to 2 days | IMG + CAL | X | HYPOTHESIS |
| 3.25 | Rain puddle / waterlogging | T | hours to days after rain | IMG + WX | ? (hides what is under it) | S42 |
| 3.26 | Stray cattle resting | T | minutes to hours | IMG | +2 | S59 |
| 3.27 | Stray dog pack | T, recurring spot | weeks at a spot | IMG + USER | CH/EL +3, night +3 | S58 |
| 3.28 | People sleeping on footpath at night | T | night hours | IMG + CAL | route around; never publish as "obstacle" (dignity) | HYPOTHESIS |
| 3.29 | Queue outside shop, ATM, temple | T | hours | IMG + CAL | +1 | HYPOTHESIS |
| 3.30 | Loading / unloading vehicles | T | minutes | IMG | +2 | S22 |
| 3.31 | Shrine built on footpath | P | years to decades | IMG | width | HYPOTHESIS |
| 3.32 | Water hose, washing, tanker filling | T | minutes | IMG | slip +1 | HYPOTHESIS |
| 3.33 | Snow piles and slush | T | days | IMG + WX | MW X, EL +3 | S46 |
| 3.34 | Sand drift after dust storm | T | hours to days | IMG + WX | MW +2 | S47 |

### L4. Human behaviour (25)

| ID | factor | unit / measure | observed via | cost effect | source |
|---|---|---|---|---|---|
| 4.01 | Two-wheelers riding on footpaths | events per hour; Bengaluru police: 17,705 cases to Sept 2026 | IMG motion, GOV | collision BL/EL/CH +3 | S26 |
| 4.02 | Gig riders using footpath to skip jams | share of riders | IMG, NEWS | peak hours +2 | S26 |
| 4.03 | Parking on footpath | % length occupied | IMG | MW/PR X | S117, S20 |
| 4.04 | Vendors occupying footpath | m per 100 m | IMG + CAL | X at peak | S22, S15 |
| 4.05 | Hawkers return after clearance drives | days to relapse | IMG repeat, NEWS | clearance evidence decays fast | S114, S21 |
| 4.06 | Restaurants extending onto footpath | m | IMG | evening +2 | S25 |
| 4.07 | Government bodies themselves encroach | count | NEWS | permanent X, slow to clear | S23 |
| 4.08 | Wrong-side driving near crossings | events | IMG video, USER | BL/EL +2 | HYPOTHESIS |
| 4.09 | Drivers not yielding at zebra | yield rate | USER, video | EL/WK +2 | HYPOTHESIS |
| 4.10 | Signal jumping when signals are dead | events | NEWS | +2 crossing | S64 |
| 4.11 | People crossing railway tracks | deaths | GOV | track edges never routed | S71 |
| 4.12 | Festival crowds | people per m² | CAL + NEWS | crowd crush risk ALL +3 | S60, S123 |
| 4.13 | Processions and wedding baraats | duration | CAL + USER | X for hours | HYPOTHESIS |
| 4.14 | Protests, rallies, road blockades | duration | NEWS + USER | X | HYPOTHESIS |
| 4.15 | VVIP movement clearing or closing roads | hours | NEWS | temporary clear or temporary X | S16 |
| 4.16 | Encroachment removal drives | date | NEWS, GOV | short clear window | S132, S19 |
| 4.17 | Footpath used as shop display | m | IMG | width | S25 |
| 4.18 | Open urination / spitting spots | spot | USER | avoidance +1 | HYPOTHESIS |
| 4.19 | Passers-by who help lift a wheelchair over a kerb | crowd density | CAL + USER | can turn a MW X into +2 with helper | HYPOTHESIS |
| 4.20 | Staring, harassment of disabled people | reports | USER | +1 to +3 | HYPOTHESIS |
| 4.21 | Bollards removed by riders or shopkeepers | bool | IMG repeat | changes 1.25 | HYPOTHESIS |
| 4.22 | Owners building car ramps that create steps for walkers | count | IMG | MW +2 | HYPOTHESIS |
| 4.23 | Social media shaming triggers quick fixes | event | NEWS | sudden improvement, may be temporary | S126 |
| 4.24 | Citizen and lawyer groups pressuring agencies | event | NEWS | future clearance likely | S24 |
| 4.25 | Agencies' own vehicles on footpaths | count | IMG | X | S117 |

### L5. Time (19)

| ID | factor | unit / measure | observed via | cost effect | source |
|---|---|---|---|---|---|
| 5.01 | Hour of day (vendor and parking peaks) | hour | CAL | evening +2 at vendor streets | HYPOTHESIS |
| 5.02 | Weekday vs weekend | day | CAL | market streets weekend +2 | HYPOTHESIS |
| 5.03 | School opening and closing (vans, parents) | time window | CAL + OSM school | +2 near schools | HYPOTHESIS |
| 5.04 | Office rush hours | window | CAL | footpath riding peaks +2 | S26 |
| 5.05 | Night and known dark spots | hour | CAL + GOV dark-spot lists | EL/LV/women +2 to +3 | S56 |
| 5.06 | Festival calendar (Durga Puja, Ganesh, Diwali debris, Holi colour on surfaces) | date | CAL | pandals X, crowds +3 | S60, S61 |
| 5.07 | Election periods (rallies, posters, barricades) | date | CAL + NEWS | +2 | HYPOTHESIS |
| 5.08 | Monsoon timing differs by region (south-west Jun to Sep; north-east Oct to Dec in Tamil Nadu) | month | CAL + WX | waterlogging priors switch on | S133 |
| 5.09 | Post-monsoon repainting / repair season | month | CAL + NEWS | markings and potholes improve | S70 |
| 5.10 | Drain works season (open drains before and during rain) | month | NEWS | open drain prior up | S43 |
| 5.11 | Image age vs factor half-life | days | IMG metadata | stale evidence decays to ? | S93 |
| 5.12 | Time since last encroachment drive | days | NEWS | clear evidence decays | S21 |
| 5.13 | Signal timing by hour (vehicle-first AI signals) | seconds of green | USER, GOV | EL/WK +2 | S66 |
| 5.14 | Waste collection hours (bins out) | window | CAL | +1 | HYPOTHESIS |
| 5.15 | Weekly bazaar day | day | CAL + USER | X on that street | HYPOTHESIS |
| 5.16 | Dry-season construction peak | month | CAL | trenches +2 | HYPOTHESIS |
| 5.17 | Sunrise and sunset time (by latitude and date) | time | astronomy calc | switches day / night models | HYPOTHESIS |
| 5.18 | Prayer and darshan times (crowds) | window | CAL + USER | +2 | HYPOTHESIS |
| 5.19 | Tourist season in hill towns and old cities | month | CAL | crowds +2 | HYPOTHESIS |

### L6. Weather and season (23)

| ID | factor | unit / measure | observed via | cost effect | source |
|---|---|---|---|---|---|
| 6.01 | Rain intensity | mm per hour (Gurugram: 70 mm in 35 min) | WX | triggers waterlogging model | S45 |
| 6.02 | Waterlogging depth on segment | cm | IMG + DEM sinks + history | > few cm: MW/PW X, PR X, ALL ? for hidden hazards | S42, S44 |
| 6.03 | Open drain or manhole hidden under water | bool, unknowable from image | history + USER | never route through flooded segment with drain history: ALL X | S42, S44, S43 |
| 6.04 | Electrified water near poles and wires | bool | history + NEWS | ALL X near poles in standing water | S50, S51, S121 |
| 6.05 | Tree falls in storms (Bengaluru 1,222 uprooted May to Sept 2025) | count | WX + NEWS | tree-lined edges +2 in wind | S52 |
| 6.06 | Heatwave | degrees C, days | WX | EL/PG/MW +2 for long unshaded edges | S49 |
| 6.07 | Hot surfaces and metal handrims | surface degrees C | WX + material | MW hand burn +2 | HYPOTHESIS |
| 6.08 | Shade along route | % canopy | SEG vegetation | heat: shaded edges preferred | HYPOTHESIS |
| 6.09 | Fog visibility | m (Delhi 150 to 200 m) | WX | crossings +3, LV +3 | S48 |
| 6.10 | Dust storm visibility | near zero, 80 kmph winds | WX | ALL +3, avoid trees | S47, S119 |
| 6.11 | Smog / air quality | AQI | WX | EL/PG/asthma +2 for long routes | S48 |
| 6.12 | Snow on paths (hill towns) | cm | WX + IMG | MW X, EL +3 | S46 |
| 6.13 | Morning ice on shaded slopes | bool | WX temp | EL +3 | HYPOTHESIS |
| 6.14 | Landslides on hill walking routes | events | NEWS + GOV | X | S122, S111 |
| 6.15 | Cyclone warnings (coastal) | alert level | WX | X outdoors | HYPOTHESIS |
| 6.16 | High tide plus heavy rain (coastal cities) | tide m | WX + tide tables | waterlogging prior up | HYPOTHESIS (no source found in this round) |
| 6.17 | Mud and slush on kuccha paths | class | IMG + WX | MW X, PR +3 | HYPOTHESIS |
| 6.18 | Wind gusts (Delhi storms up to 128 kmph) | kmph | WX | falling objects +3 | S134 |
| 6.19 | Lightning | alert | WX | open routes +2 | S133 |
| 6.20 | Cold wave | degrees C | WX | EL +1 | HYPOTHESIS |
| 6.21 | Heat index (heat plus humidity) | index | WX | EL/PG +2 | HYPOTHESIS |
| 6.22 | Wet leaves and algae on slopes (Kerala, North East) | class | IMG + WX | slip +2 | HYPOTHESIS |
| 6.23 | Season-specific image look (monsoon green, winter haze) | domain | IMG | detector confidence drop | S104 |

### L7. Lighting and visibility (16)

| ID | factor | unit / measure | observed via | cost effect | source |
|---|---|---|---|---|---|
| 7.01 | Share of streetlights working | % (Bhopal: 5,361 of 20,618 off) | GOV dashboards | night edges +2 where low | S55 |
| 7.02 | Streetlight complaint volume | count (Ahmedabad: 4.33 lakh over 5 years) | GOV | prior for dark stretches | S54 |
| 7.03 | Known police "dark spots" | list | GOV | night +3 | S56 |
| 7.04 | Light pole spacing (about 3x fixture height) | m | IMG | gaps: night +1 | S1 |
| 7.05 | Pothole visible by day, invisible at night | bool | day image + night time | night: keep day evidence, raise penalty for BL/EL | HYPOTHESIS (user example) |
| 7.06 | Headlight glare | class | CAL + road type | LV +2 | HYPOTHESIS |
| 7.07 | Low sun glare on east-west streets | sun angle | astronomy + OSM bearing | LV +1 at dawn/dusk | HYPOTHESIS |
| 7.08 | Kerb and step edge contrast | contrast | IMG | LV +2 | S4 |
| 7.09 | Tree shadows hiding surface defects in photos | shadow % | IMG | detector ? | HYPOTHESIS |
| 7.10 | Power cuts | hours | GOV / USER | night +2 | HYPOTHESIS |
| 7.11 | Shop lights as the only light (dark after closing) | time | CAL | +2 after closing | HYPOTHESIS |
| 7.12 | FOB / subway lights not working | bool | NEWS, USER | +2 | S67 |
| 7.13 | Camera noise and blur at night | sharpness | IMG quality gate | detector confidence down | S104 |
| 7.14 | Reflective studs and markings | present | IMG | crossing visibility | S70 |
| 7.15 | Safetipin lighting score | 0 to 3 | DATA | night prior | S57 |
| 7.16 | Pedestrian visible to drivers | rating | DATA | crossing +2 | S57 |

### L8. Regional and terrain (26)

| ID | factor | unit / measure | observed via | cost effect | source |
|---|---|---|---|---|---|
| 8.01 | Hill town gradients | % | DEM | MW +3 or X | S46 |
| 8.02 | Steps as main public paths (hill towns) | count | OSM steps, IMG | MW X | HYPOTHESIS |
| 8.03 | Landslide-prone pilgrim and walking routes | zone list | GOV + NEWS | seasonal X | S122 |
| 8.04 | Coastal corrosion of rebar and covers | class | IMG | decay faster | HYPOTHESIS |
| 8.05 | Desert towns sand drift | class | IMG + WX | MW +2 | S47 |
| 8.06 | Old walled cities: narrow lanes, mixed traffic, steps to havelis | lane width | OSM + IMG | MW +2, BL +2 | HYPOTHESIS |
| 8.07 | Villages: unpaved (kuccha) paths | surface | IMG | MW +3 dry, X wet | HYPOTHESIS |
| 8.08 | Highways through villages with no footpath | bool | OSM + IMG | ALL +3 | S82 |
| 8.09 | Rail level crossings (manned since unmanned BG crossings eliminated Jan 2019) | gate | OSM + GOV | gate wait; track flangeway gaps MW +2 | S72 |
| 8.10 | Station track trespass (Mumbai: 26,547 deaths Jan 2015 to May 2025) | deaths | GOV | track never a route edge | S71 |
| 8.11 | Station FOBs without lifts | bool | NEWS + USER | MW X between platforms | S73 |
| 8.12 | Metro construction corridors | km | NEWS + IMG | X or +3 for years | S115, S39 |
| 8.13 | New metro station access gaps | bool | NEWS | last 100 m X | S116 |
| 8.14 | Smart City redesigned streets | area | GOV | better geometry prior, audit says mixed | S78 |
| 8.15 | Cantonment and gated roads | access | OSM access=* | closed X | HYPOTHESIS |
| 8.16 | Pilgrimage routes | seasonal | CAL + NEWS | crowds + landslide | S122 |
| 8.17 | Riverfront ghat steps | count | OSM + IMG | MW X | HYPOTHESIS |
| 8.18 | North East and tribal hill tracks | surface | IMG | MW X | HYPOTHESIS |
| 8.19 | Seasonal flood plains (Assam, Bihar) | months | WX + GOV | X in flood | HYPOTHESIS |
| 8.20 | High altitude (Leh): thin air slows walkers | altitude m | DEM | EL/PG distance budget down | HYPOTHESIS |
| 8.21 | Kerala backwater and island paths | surface | IMG | ferry links | HYPOTHESIS |
| 8.22 | Industrial areas (trucks, open drains, no footpaths) | zone | OSM landuse | CH/ALL +3 | S11 |
| 8.23 | Peri-urban new layouts without footpaths yet | bool | IMG + OSM | +3 | S116 |
| 8.24 | State-level footpath availability (J&K 3%, Puducherry 5%, Bihar and Haryana 19 to 20%) | % roads | GOV (SC panel audit) | prior for "footpath exists" | S82 |
| 8.25 | City death hotspots (Delhi, Bengaluru 894, Jaipur 860 deaths in 2024) | deaths | GOV | crossing penalty prior | S8 |
| 8.26 | Language of signs and of our UI (22 scheduled languages) | language | USER setting | UI in user language | HYPOTHESIS |

### L9. Governance: standards, law, audits, corruption (29)

| ID | factor | unit / measure | observed via | cost effect / use in system | source |
|---|---|---|---|---|---|
| 9.01 | IRC:103-2022: footpath 150 mm, kerb ramp 1:15, flares 1:10, cross slope 1:50 to 1:100 | thresholds | GOV | rule floor (M9) for geometry checks | S1, S2 |
| 9.02 | MoHUA Harmonised Guidelines 2021: kerb ramp 1:12, width >= 900 mm, kerbs up to 200 mm | thresholds | GOV | rule floor | S4 |
| 9.03 | Standards disagree (1:15 vs 1:12) | conflict | GOV | use the stricter one for MW, show both to the user | S1, S4 |
| 9.04 | RPwD Act 2016 sections 40 to 46 (accessibility, 5-year retrofit) | law | GOV | legal hook for reports | S75 |
| 9.05 | Rajive Raturi v Union of India (8 Nov 2024): Rule 15 ultra vires, mandatory rules ordered | judgment | GOV | "the standard is now mandatory" | S74 |
| 9.06 | SC follow-up order 23 Feb 2026 in Rajive Raturi | order | GOV | status of mandatory rules | S135 |
| 9.07 | SC order 14 May 2025 (S. Rajaseekaran): footpaths under Art. 21, must be usable by PwD, encroachment removal mandatory | order | GOV | report export cites it | S14, S139 |
| 9.08 | SC June 2026: walking on demarcated footpaths a fundamental right | judgment | NEWS | same | S18 (case name UNVERIFIED) |
| 9.09 | SC 3 Aug 2026: Centre to demarcate walking space on every road, "with a rope or anything" | order | NEWS | cheap fix suggestion in reports | S17 |
| 9.10 | Bombay HC on hawkers (2024, 2025) and VVIP clearing | orders | NEWS | encroachment context | S15, S16, S114 |
| 9.11 | Karnataka HC: forged vendor licences, "right to footpaths must be protected" (Jul 2026) | order | NEWS | encroachment legitimacy is not visible in images | S19 |
| 9.12 | Bombay HC on bollards blocking wheelchairs (2023) | hearing | NEWS | bollard rule | S27 |
| 9.13 | Street Vendors Act 2014 vending zones | law | GOV | legal vendor zones are expected obstacles | HYPOTHESIS (no direct source fetched this round) |
| 9.14 | Accessible India Campaign deadlines missed and revised | dates | GOV | official "accessible" claims are weak evidence | S80, S136 |
| 9.15 | CAG Rajasthan RPwD audit (2023): ramps built, other facilities missing | audit | GOV | "has ramp" does not mean "accessible" | S76 |
| 9.16 | CAG 2025: retrofits without pre-audit or post-check | audit | NEWS (India Forum) | paper compliance vs usable access | S77 |
| 9.17 | CAG Smart City Mission audit (Report 11 of 2025, Karnataka) | audit | GOV | Smart City prior | S78 |
| 9.18 | CAG urban mobility audit (Lucknow) covering footpaths, zebra, FOBs, ramps | audit | NEWS | data source when tabled | S79 |
| 9.19 | CAG 2016 suburban rail: 59% of 33,445 deaths from trespass | audit | GOV | station area priors | S137 |
| 9.20 | Defect liability enforcement and blacklisting | penalties | GOV | repair-speed prior | S36 |
| 9.21 | Corruption in materials | qualitative | NEWS | decay prior | S34, S35 |
| 9.22 | Police FIRs blaming pothole victims, no compensation | pattern | NEWS | why official accident data undercounts | S13 |
| 9.23 | Officials suspended after manhole death (Mumbai Jul 2026) | event | NEWS | accountability signal | S110 |
| 9.24 | Smart City signals defunct (Thanjavur) | status | NEWS | "signal exists" is weak evidence | S65 |
| 9.25 | Agency fragmentation (JMC, JDA, JVVNL; GBA, BWSSB) | count of owners per segment | GOV | who to send a report to | S24, S25 |
| 9.26 | Unpaid contractor dues (Chennai over Rs 1,000 crore) stall works | Rs | NEWS | half-finished works last longer | S138 |
| 9.27 | Grievance dashboards (streetlights etc.) | complaints | GOV | live data feed | S54 |
| 9.28 | MoRTH vs NCRB pedestrian death counts differ (35,221 vs 27,586 in 2023) | count | GOV | any single official number is uncertain | S87 |
| 9.29 | Geospatial policy: street imagery must be collected by Indian entities | rule | GOV | limits imagery sources | S94 |

### L10. Users and bodies (26)

| ID | factor | unit / measure | observed via | cost effect / use | source |
|---|---|---|---|---|---|
| 10.01 | Manual wheelchair cross-slope limit (one-rim propulsion at ~3%) | % | profile | 1.10 thresholds | S96 |
| 10.02 | Step-climbing power chairs: median 20 cm step; ordinary power chairs far less | cm | profile | PW threshold per user device | S95 |
| 10.03 | Wheelchair width (95th pct power chair just over 700 mm) | mm | profile | 1.06, 1.08, 1.25 thresholds | S98 |
| 10.04 | Cross slope raises handrim load (1.8x at 6 degrees) | factor | profile | MW fatigue model | S97 |
| 10.05 | Grass and interlocking pavers raise push force | relative | profile | 2.17 multipliers | S100 |
| 10.06 | Walker users need level path, 1.2 m+ | m | profile | 1.08 | S4 |
| 10.07 | Crutch users need wider path (HG figure 2.6) | m | profile | 1.08 | S4 |
| 10.08 | Pram: small front wheels, kerbs | mm | profile | 1.02, 1.07 | HYPOTHESIS |
| 10.09 | Blind cane users miss sudden dips and overhead objects | class | profile | 1.27, 2.06 penalties | S28 |
| 10.10 | Low vision needs contrast and light | class | profile | L7 | S4 |
| 10.11 | Elderly share 11% (2024) to 21% (2050) | % | GOV | demand + fall-risk weights | S85, S84 |
| 10.12 | Pregnant walkers: falls, slope, heat | class | profile | L6 heat, 2.13 slip | S40 |
| 10.13 | Children: drains, dogs, traffic | class | profile | 2.06, 3.27 | S42, S125 |
| 10.14 | Temporary injury (cast, crutches for weeks) | duration | profile | like CR, temporary account | HYPOTHESIS |
| 10.15 | Heavy wheeled luggage (stations, bus stands) | kg | profile | steps +2 | HYPOTHESIS |
| 10.16 | Deaf walkers on shared roads cannot hear vehicles behind | class | profile | no-footpath edges +2 | HYPOTHESIS |
| 10.17 | Cognitive disability: complex junctions | class | profile | fewer turns preferred | HYPOTHESIS |
| 10.18 | Dog bite risk heavier for children and elderly | rate | GOV | 3.27 weight | S125, S143 |
| 10.19 | Endurance budget on long slopes | m, W | profile | max route length | S129 |
| 10.20 | Accessible toilets on route | count | OSM | long routes need them | HYPOTHESIS |
| 10.21 | Seats and rest points | per km | IMG + OSM | EL/PG prefer | HYPOTHESIS |
| 10.22 | Companion present (can lift over kerb) | bool | USER | MW X may become +2 | HYPOTHESIS |
| 10.23 | 2.68 crore disabled (Census 2011), 69% rural | count | GOV | rural matters, not only metros | S83 |
| 10.24 | People who stop going out (suppressed demand) | testimony | NEWS | users underreport barriers | S28 |
| 10.25 | Two-thirds of disabled respondents near transit cannot reach it safely (Chennai) | % | NGO study | last-mile focus | S81 |
| 10.26 | Hand-cranked tricycles and retrofitted scooters (common Indian mobility aids) | device | profile | width + kerb thresholds | HYPOTHESIS |

### L11. Data and sensing (24)

| ID | factor | unit / measure | observed via | effect on system | source |
|---|---|---|---|---|---|
| 11.01 | Street View India: 10 cities at launch (2022), later 3,000+ cities and towns | coverage | DATA | where imagery exists at all | S92, S140 |
| 11.02 | Imagery quality (low-grade cameras in early India capture) | resolution | IMG | small-barrier recall down | S93 |
| 11.03 | Imagery age per pano | date | metadata | staleness decay | S93 |
| 11.04 | Mapillary / KartaView density in India | images per km | DATA | fallback source | HYPOTHESIS (dsh lane S1a to measure) |
| 11.05 | User phone photos | count | USER | freshest evidence, noisiest | HYPOTHESIS |
| 11.06 | Project Sidewalk Chandigarh: 3,216 labels, 56 km, 59 contributors (Sept 2026) | labels | DATA | only Indian PS label set | S91 |
| 11.07 | Project Sidewalk global: ~1.68M labels across 59 cities | labels | DATA | pretraining pool | S91, S109 |
| 11.08 | Label types (CurbRamp, NoCurbRamp, Obstacle, SurfaceProblem, NoSidewalk...) | taxonomy | DATA | our taxonomy base | S109 |
| 11.09 | Cross-city transfer: curb ramp 84.7% precision, 82.7% recall (US/Mexico cities) | metric | paper | expect drop in India | S90 |
| 11.10 | IDD: 10,004 Indian road images, 34 classes | dataset | DATA | Indian segmentation | S103 |
| 11.11 | Phone GPS median error 5 to 8.5 m | m | IMU/GNSS | side-of-road ambiguity | S101 |
| 11.12 | Urban canyon NLOS errors tens to hundreds of m | m | GNSS | snap needs image cues | S102 |
| 11.13 | Road narrower than GPS error (old cities) | m | OSM width vs 11.11 | side unknown unless image says | S101 |
| 11.14 | Compass heading error | degrees | IMU | which footpath the camera sees | HYPOTHESIS |
| 11.15 | Motion blur | sharpness | IMG | quality gate | HYPOTHESIS |
| 11.16 | Occlusion by vehicles and people | % hidden | SEG | "cannot see the footpath" | HYPOTHESIS |
| 11.17 | Unknown camera height and pitch | m, deg | IMG | metric depth scale | HYPOTHESIS |
| 11.18 | EXIF stripped by messaging apps | bool | metadata | ask user for place and time | HYPOTHESIS |
| 11.19 | OSM footway and sidewalk tags missing in Indian cities | % roads | OSM | build footway graph from road graph | HYPOTHESIS (measure via Overpass) |
| 11.20 | DEM too coarse for kerbs (30 m cells) | m | DEM | slopes only at block scale | HYPOTHESIS |
| 11.21 | Grievance portals as evidence | records | GOV | fresh state | S54 |
| 11.22 | Conflicting official numbers | count | GOV | never quote one source as truth | S87 |
| 11.23 | Safetipin image audits (2.2 lakh images, Delhi 2023) | images | DATA | night lighting prior | S57 |
| 11.24 | Several images of the same spot | views | IMG | multi-view agreement = confidence (LUNAR-TIE move) | HYPOTHESIS |

### L12. AI failure modes (22)

| ID | factor | measure | observed via | effect on system | source |
|---|---|---|---|---|---|
| 12.01 | Domain shift from Western street data to Indian streets | accuracy drop | eval on IDD / own labels | do not trust PS-trained models raw | S103, S90 |
| 12.02 | Night images: Cityscapes-trained model 25.0 mIoU at night vs 45.7 fog, 50.0 rain | mIoU | eval | night outputs flagged low-confidence | S104 |
| 12.03 | Shortcut learning (e.g. "crowded = barrier", "Indian street = broken") | probe tests | eval | counterfactual test set | S105 |
| 12.04 | Adversarial patch or sticker fools detector | attack success | red-team | multi-view + two-family agreement | S106 |
| 12.05 | VLM object hallucination ("I see a ramp") | POPE-style rate | eval | VLM never sole judge | S107 |
| 12.06 | False safe (missed barrier) costs far more than false barrier | asymmetric loss | design | thresholds tuned for recall on barriers; conformal sets | S108 |
| 12.07 | False barrier: shadow read as pothole | FP rate | eval | depth check before X | HYPOTHESIS |
| 12.08 | Puddle reflections read as objects | FP rate | eval | wet-scene flag | HYPOTHESIS |
| 12.09 | Painted 3D zebra / street art illusions | FP | eval | depth disagreement flag | HYPOTHESIS |
| 12.10 | Tiny barriers (2 cm lip) below image resolution | recall | eval | mark ? not 0 | HYPOTHESIS |
| 12.11 | Monocular depth scale ambiguity | mm error | eval with tape measure | kerb height as range, not point | HYPOTHESIS |
| 12.12 | Annotator disagreement on what counts as a barrier | agreement | label audit | per-profile labels | S89 |
| 12.13 | Crowd label noise vs validated labels | metric | eval | validation weighting | S90 |
| 12.14 | Rare classes (open manhole, borewell) | count | data audit | synthetic + own photos | HYPOTHESIS |
| 12.15 | Old evidence used as current | age | ledger | half-life decay | HYPOTHESIS |
| 12.16 | Two detectors agree but share the same blind spot (same pretraining) | correlated error | eval | pick different families (detector + segmenter + depth) | HYPOTHESIS |
| 12.17 | Calibration drift across cities and seasons | ECE | eval | recalibrate per region | S108 |
| 12.18 | Open-vocabulary prompt sensitivity | variance | eval | prompt ensemble | HYPOTHESIS |
| 12.19 | Faces and number plates in images | privacy | IMG | blur before storage | HYPOTHESIS |
| 12.20 | Poisoned crowd reports (vendor reports spot "clear") | report trust | ledger | reputation + photo required | HYPOTHESIS |
| 12.21 | Users over-trust a green route | behaviour | UX test | always show confidence and age | HYPOTHESIS |
| 12.22 | Season shift (monsoon look vs dry look) | metric | eval | per-condition test sets | S104 |

### L13. Economics and incentives (18)

| ID | factor | unit | observed via | effect / use | source |
|---|---|---|---|---|---|
| 13.01 | Bengaluru fills ~30,000 potholes a year for ~Rs 30 crore (likely an underestimate) | Rs | NEWS | potholes recur, prior | S34 |
| 13.02 | Footpath tenders (Chennai Rs 280 crore) | Rs | NEWS | works = temporary X | S138 |
| 13.03 | Unpaid contractor dues stall works | Rs | NEWS | half-life of works up | S138 |
| 13.04 | Vendor livelihoods (PM SVANidhi target 1.15 crore vendors) | count | GOV | vendors are users too; route around, do not shame | S88 |
| 13.05 | Relaying cycles as recurring business (paver relays) | Rs per cycle | NEWS | new surface, same problems | S35, S141 |
| 13.06 | Accessible India retrofit funds (Rs 562 crore, 1,314 buildings) | Rs | NEWS | building access, not streets | S142 |
| 13.07 | Pothole victims' families not compensated | count | NEWS | official harm undercounted | S13 |
| 13.08 | Cost of a kerb ramp vs cost of a death | Rs | estimate | pitch number | HYPOTHESIS |
| 13.09 | Contractor penalties (Rs 6.67 crore case) | Rs | GOV | enforcement exists, rare | S36 |
| 13.10 | Parking scarcity drives footpath parking | spaces | HYPOTHESIS | parking prior near markets | HYPOTHESIS |
| 13.11 | Shopfront rent makes encroachment pay | Rs | HYPOTHESIS | commercial streets prior | HYPOTHESIS |
| 13.12 | Informal payments that let encroachment stay | qualitative | HYPOTHESIS | clearance relapse | HYPOTHESIS |
| 13.13 | Gig delivery time pressure | min | NEWS | footpath riding | S26 |
| 13.14 | Pre-election tender rush | count | NEWS | dug-up roads before polls | S138 |
| 13.15 | Cost of detours for wheelchair users (time, auto fares) | Rs, min | USER | route value metric | HYPOTHESIS |
| 13.16 | Lost access to transit (two-thirds cannot reach it) | % | NGO | value of last-mile fixes | S81 |
| 13.17 | Hoarding ad revenue keeps poles in footpaths | Rs | HYPOTHESIS | permanent obstacle prior | HYPOTHESIS |
| 13.18 | Our own API costs (Street View is paid per request) | Rs per 1,000 | DATA | cache, sample smartly | HYPOTHESIS (price check in dsh lane) |

### L14. Safety and crime (20)

| ID | factor | unit | observed via | cost effect | source |
|---|---|---|---|---|---|
| 14.01 | Dog bites: 37,17,336 cases and 54 suspected rabies deaths in 2024 | count | GOV | CH/EL +3 at known dog spots | S58 |
| 14.02 | Children: over 5 lakh dog bite victims under 15 in 2024 | count | GOV | CH +3 | S143 |
| 14.03 | Stray cattle deaths (MP: 437 in 8 months of 2026) | count | GOV/NEWS | +2 | S59 |
| 14.04 | Dark spots linked to sexual violence | spot | GOV/NEWS | night women +3 | S56 |
| 14.05 | Few people around ("eyes on the street") at night | rating | DATA | night +2 | S57 |
| 14.06 | Harassment of women walking | rating | DATA, USER | +2 | S57 |
| 14.07 | Chain snatching by riders | reports | NEWS, USER | +1 | HYPOTHESIS |
| 14.08 | Crowd crush (Kolkata Durga Puja Oct 2026, 19 dead, narrow approach) | deaths | NEWS | festival lanes X for MW, +3 ALL | S60 |
| 14.09 | Electrocution in waterlogged streets (Kolkata: 8 deaths in 24 h) | deaths | NEWS | X near poles in water | S50 |
| 14.10 | Over-speeding causes 68% of accidents | % | GOV | wide fast roads +2 at crossings | S7 |
| 14.11 | Pedestrian deaths 35,221 (2023), 20.6% of road deaths (2024) | count | GOV | headline number | S86, S8 |
| 14.12 | Pothole deaths 9,438 (2020 to 2024) | count | GOV | headline number | S9 |
| 14.13 | Railway trespass deaths | count | GOV | stations | S71 |
| 14.14 | Drowning in open drains during rain | events | NEWS | X | S43 |
| 14.15 | Tree branch falls on walkers | events | NEWS | windy days +2 | S124 |
| 14.16 | Footpath transformer explosion | events | NEWS | +1 near units | S29 |
| 14.17 | Robbery targeting elderly or disabled | reports | USER | +2 | HYPOTHESIS |
| 14.18 | Police presence / CCTV | bool | DATA | night -1 | HYPOTHESIS |
| 14.19 | Monkeys (temple and hill towns) | reports | USER | CH/EL +2 | HYPOTHESIS |
| 14.20 | Snakes on flooded rural paths | reports | USER | +2 | HYPOTHESIS |

## Part B. The WHAT-IF round (165 questions)

**Response codes:** DETECT (the image shows it, model finds it), ESTIMATE (a number with a range), UNKNOWN (marked unknown, which raises the cost and is never shown as safe), ASK (ask the user), REFUSE (the system declines and says why).

**Components (proposed architecture, claude design, not built yet):** C1 ingest + metadata, C2 image quality gate, C3 detector family A (open-vocabulary box detector), C4 detector family B (segmentation trained on Indian data), C5 agreement / fusion, C6 depth and geometry, C7 geo-matcher (GPS to footway segment, side of road), C8 evidence ledger (timestamps, half-life decay), C9 context engine (time, calendar, weather), C10 profile cost model, C11 router, C12 uncertainty layer (conformal, "needs a human look"), C13 human review / crowd queue, C14 UI and explanations, C15 world-model simulator.

| # | what if ...? | honest response | component |
|---|---|---|---|
| 1 | the pothole is hidden under rainwater? | UNKNOWN: flooded segment with no recent dry photo becomes ? for all, X for MW/PW/PR; says "water hides what is under it" | C9, C8, C10 |
| 2 | the photo is 3 years old? | ESTIMATE: each finding decays by its half-life; old vendor = ?, old pole = still likely | C8 |
| 3 | a vendor sets up after the photo was taken? | ESTIMATE from time-of-day prior for that street; ASK the user to confirm on arrival | C9, C8, C13 |
| 4 | the only route has a step? | DETECT + ESTIMATE step height; shows the route with the step named, "needs a helper", never hides it | C6, C10, C14 |
| 5 | GPS puts the barrier on the wrong side of the road? | ESTIMATE side from image heading + footpath visible; if still ambiguous, mark both sides ? | C7 |
| 6 | two detectors disagree? | UNKNOWN: "needs a human look", queued for review, not marked safe | C5, C12, C13 |
| 7 | a judge uploads a photo from Leh in snow? | DETECT what it can (steps, poles), says snow covers the surface and kerb heights; surface = UNKNOWN; routes on OSM if Leh has data | C2, C4, C14 |
| 8 | the FOB lift is out of service today? | ASK / USER report flips the edge to X for MW; offers ground crossing or says none exists | C8, C11 |
| 9 | the photo is at night? | DETECT with night-flag; confidence lowered, near-threshold calls become UNKNOWN | C2, C12 |
| 10 | someone sticks a printed "ramp" sticker to fool the model? | DETECT disagreement between box detector, segmenter and depth (flat print has no slope); UNKNOWN + flag | C5, C6 |
| 11 | there is no street imagery at all for the village? | UNKNOWN for every segment; routes by OSM geometry only, asks for 3 phone photos at key junctions | C1, C11, C13 |
| 12 | OSM has no footpaths mapped? | ESTIMATE footway graph from road graph (both sides assumed), every edge starts as ? | C11 |
| 13 | the kerb ramp exists but a car is parked on it? | DETECT both; the ramp is blocked now, likely free later (car half-life hours) | C3, C8 |
| 14 | the ramp is steeper than 1:12 but meets IRC 1:15? | ESTIMATE slope; shows both standards, uses stricter for MW | C6, C10 |
| 15 | the depth model says kerb is 140 mm but true is 180 mm? | ESTIMATE as a range (e.g. 120 to 200); decision uses the range upper edge for MW | C6, C12 |
| 16 | a user reports a barrier that the photo does not show? | ACCEPT as recent evidence with lower weight; asks for a photo; decays faster without one | C8, C13 |
| 17 | the user is a power chair that climbs 10 cm? | profile override; 8 cm kerb becomes +1, not X | C10 |
| 18 | the user is blind and the route crosses a 6-lane road with no signal? | DETECT no signal; +3 or X for BL; suggests nearest signalled crossing | C10, C11 |
| 19 | the traffic signal exists but is dead? | UNKNOWN status from image alone; ASK / grievance data; dead-signal reports lower crossing score | C9, C8 |
| 20 | the zebra crossing is fully faded? | DETECT faded paint; treated as uncontrolled crossing | C3, C10 |
| 21 | the footpath is fine but 0.8 m wide? | DETECT + ESTIMATE width; MW/PW X, walker fine | C6, C10 |
| 22 | the footpath changes height 6 times in 100 m? | DETECT each step-down; MW prefers road edge only if traffic low, else X; says so | C6, C10 |
| 23 | bollards are 0.8 m apart? | ESTIMATE spacing; MW X at that entry | C6 |
| 24 | a festival pandal is put up next week? | CAL prior: festival dates raise cost on known pandal streets; ASK local users | C9 |
| 25 | there is a procession right now? | UNKNOWN until reported; live user reports flip edge to X for hours | C8, C13 |
| 26 | a protest blocks the road? | same as 25; never guesses politics, only "blocked" | C8 |
| 27 | waterlogging depth is 20 cm? | ESTIMATE from image (kerb partly submerged); X for MW/PR, ? for ALL over drains | C6, C9 |
| 28 | it is raining but the segment has never flooded before? | ESTIMATE from DEM sinks + history; lower risk than known flood spots, still flagged | C9 |
| 29 | a tree fell an hour ago? | UNKNOWN until reported; storm warning raises tree-lined edge cost | C9, C8 |
| 30 | live wires are lying in water? | REFUSE to route through any flooded segment next to poles during heavy rain; says why | C9, C10 |
| 31 | a manhole cover is missing at night? | DETECT only if a photo exists; else UNKNOWN; known missing-cover spots stay X until a "fixed" photo | C8 |
| 32 | the open manhole was fixed yesterday? | needs a new photo to clear; one "fixed" report lowers to +2, photo clears | C8, C13 |
| 33 | the borewell pit is in a field next to the path? | UNKNOWN from street images; user reports only; CH profile warned in rural areas | C13 |
| 34 | the trench is covered with a plank? | DETECT plank; +3 for walkers, X for MW | C3, C10 |
| 35 | the new footpath is half built? | DETECT construction; X now, re-check after expected completion | C3, C8 |
| 36 | the bridge on the map was never finished? | DETECT if images show it; else OSM says bridge but construction tag missing: ASK, mark ? | C7, C13 |
| 37 | the footpath ends suddenly? | DETECT end; router avoids dead ends for MW | C4, C11 |
| 38 | the image is blurred? | REFUSE that image ("too blurry to judge"), uses others | C2 |
| 39 | the camera points at the sky? | REFUSE image (no ground visible) | C2 |
| 40 | a bus blocks the whole footpath in the photo? | UNKNOWN for that stretch (occluded), not "clear" | C2, C12 |
| 41 | the photo is from WhatsApp with no EXIF? | ASK for place and time; can still detect, cannot place | C1 |
| 42 | the user's GPS is 30 m off in the old city? | ESTIMATE using image cues (shop signs, junction shape); else ASK to pin on map | C7 |
| 43 | the photo shows a barrier but not which segment? | ESTIMATE from heading + visible kerb line; low confidence = attached to both candidates as ? | C7 |
| 44 | the photo is a screenshot from Google Street View? | DETECT; uses pano date if visible, else ASK | C1 |
| 45 | the photo is AI-generated or edited? | ESTIMATE authenticity (metadata, artefact checks); suspicious = not used, flagged | C1, C12 |
| 46 | a vendor reports their spot as clear to avoid action? | weight by reputation and photo; conflict with other evidence = human review | C8, C13 |
| 47 | many users report the same barrier? | agreement raises confidence (multi-source = confidence) | C5, C8 |
| 48 | only one user reports and others walk past fine? | decays fast; asks the next user passing | C8, C13 |
| 49 | the model flags every crowded street as blocked? | shortcut test: counterfactual crowd-only images; if flagged, model is retrained or crowd ignored | C3, C12 |
| 50 | the VLM says "there is a ramp" but the segmenter sees none? | UNKNOWN; VLM alone never clears a barrier | C5 |
| 51 | the shadow of a pole looks like a pothole? | depth check (no depth change) lowers it to ? not X | C6 |
| 52 | a puddle reflects a pole? | wet-scene flag; reflected objects need depth support | C6, C2 |
| 53 | a 3D-painted zebra looks like a step? | depth says flat; no step | C6 |
| 54 | the kerb lip is 2 cm and too small to see? | UNKNOWN for MW at that ramp ("cannot see small lips"); ask MW users to confirm | C12, C13 |
| 55 | the step is 25 cm and the user has a carer? | profile + companion flag: +2 with "carer lift needed" | C10 |
| 56 | the user is pregnant and it is 45 C? | heat factor: shaded and shorter routes, rest points suggested | C9, C10 |
| 57 | the user is elderly and the route is 2 km uphill? | endurance budget: offers shorter or flatter route, or auto drop point | C10 |
| 58 | the user is a child walking to school? | prefers signalled crossings, avoids open drains and dog spots | C10 |
| 59 | the user has a broken leg for 6 weeks? | temporary profile with expiry | C10 |
| 60 | the user has a heavy suitcase at a station? | steps +2, lifts preferred; FOB with lift checked | C10 |
| 61 | the user is deaf? | no-footpath edges +2 (cannot hear traffic behind) | C10 |
| 62 | the user uses a hand-cranked tricycle? | wider width threshold, kerb limit like MW | C10 |
| 63 | dense fog at 7 am in Delhi? | WX: crossings +3, LV +3; says "fog: drivers cannot see you" | C9 |
| 64 | a dust storm is forecast in Rajasthan? | WX alert: suggests waiting; tree edges +3 | C9 |
| 65 | snow fell overnight in Shimla? | WX: slopes X for MW, +3 for EL; old dry-season photos kept for geometry only | C9, C8 |
| 66 | the route is on a landslide-prone hill road in monsoon? | GOV/NEWS zones: X in alert periods | C9 |
| 67 | high tide and heavy rain hit Mumbai at once? | ESTIMATE flood prior up on known low spots | C9 |
| 68 | a cyclone warning is issued? | REFUSE to suggest outdoor routes; shows shelter | C9 |
| 69 | it is Diwali night with crackers on the road? | CAL: +2 burns/noise, BL +3 (noise masks traffic) | C9 |
| 70 | Holi colours make surfaces slippery? | CAL: slip +2 | C9 |
| 71 | it is Durga Puja and the lane to a pandal is narrow? | CAL + NEWS: X for MW, crowd +3 for ALL | C9, C10 |
| 72 | streetlights on the stretch are reported off? | GOV/USER: night +2, LV +3 | C9, C8 |
| 73 | the pothole is visible by day but the user walks at night? | day evidence kept; night penalty for BL/EL raised; tells user "pothole here, hard to see at night" | C8, C14 |
| 74 | a police dark spot is on the route at 23:00? | night +3 for women and EL; alternative shown | C9, C10 |
| 75 | stray dogs gather near a dhaba at night? | USER reports: dog spot, CH/EL +3 at night | C8 |
| 76 | cattle block the lane? | DETECT; temporary, +2 | C3 |
| 77 | the route passes railway tracks? | REFUSE track crossing edges outside official crossings | C11 |
| 78 | the level crossing gate is closed for long periods? | ESTIMATE wait from timetable if available; else +1 | C9 |
| 79 | the station platform has no lift? | DETECT/USER: platform change X for MW; asks station staff option | C10 |
| 80 | metro construction moved the barricades last week? | images older than the move are stale; UNKNOWN; ASK | C8 |
| 81 | the metro station is new and OSM has no entrance? | ASK for entrance pin; marks access ? | C7, C13 |
| 82 | the old walled city lane is 2 m wide with mixed traffic? | ESTIMATE width; BL +2, MW +2, says "shared lane" | C10 |
| 83 | it is a kuccha path in a village after rain? | WX + IMG: MW X, PR +3 | C9, C10 |
| 84 | a highway runs through the village with no footpath? | DETECT absence; +3 ALL, CH warned | C4, C10 |
| 85 | it is a hill town with steps as the main road? | OSM steps + IMG: MW X, says no step-free route exists if so | C11 |
| 86 | the user is at 3,500 m altitude? | endurance budget reduced for EL/PG | C10 |
| 87 | there are two standards for the same ramp? | shows both (IRC 1:15, HG 1:12), uses stricter for MW | C10, C14 |
| 88 | a government booth sits on the footpath legally? | still a width obstacle; legality is not the walker's problem | C10 |
| 89 | the encroachment drive happened yesterday? | clear evidence decays with vendor half-life (days); not trusted for long | C8 |
| 90 | a court ordered the footpath cleared? | GOV note on the segment; does not change physical state until a photo | C8, C14 |
| 91 | the city claims a footpath is "accessible" in its records? | weak evidence (CAG audits found paper compliance); photo needed | C8 |
| 92 | a contractor resurfaced the road and raised it to kerb level? | DEPTH: kerb now 0 mm, ramp no longer needed; or drainage now floods footpath | C6 |
| 93 | the road was raised and now the footpath is lower than the road? | DETECT reversed step; flood prior up | C6 |
| 94 | a slab looks fine but rocks when stepped on? | UNKNOWN from images; USER/IMU reports only | C13 |
| 95 | the drain slab is missing and covered by leaves? | UNKNOWN; known slab gaps from history stay flagged | C8 |
| 96 | the footpath is polished granite and it is raining? | material + WX: slip +3 for EL/WK/CR/PG | C9, C10 |
| 97 | the surface is new but cheap (crumbles in months)? | decay prior for that agency/ward; re-check sooner | C8 |
| 98 | the photo is from the dry season and it is now monsoon? | geometry kept, surface and flood state = ? | C8, C9 |
| 99 | the user asks "is this route safe?" | never says "safe"; says "known barriers: none; unknown stretches: 3; oldest photo: 14 months" | C12, C14 |
| 100 | the system has 51% confidence? | below threshold = UNKNOWN, shown as grey, not green | C12 |
| 101 | conformal set contains both "ramp" and "no ramp"? | UNKNOWN, review queue | C12, C13 |
| 102 | the model was trained on Seattle images only? | REFUSE to ship that model raw; fine-tune on Indian labels, report Indian test score | C3, C12 |
| 103 | test images leak into training? | split by location (no same street in both); score reported on unseen city | C12 |
| 104 | annotators disagree whether a 10 cm step is a barrier? | per-profile labels: it is X for MW, 0 for walker | C10, C13 |
| 105 | a rare barrier (open manhole) has 5 training examples? | few-shot + own photos + synthetic; recall reported honestly with low count | C3, C12 |
| 106 | the detector misses a barrier that hurts someone? | false-safe incident log, model and threshold reviewed; route confidence shown always | C12 |
| 107 | the detector marks too many false barriers and routes become long? | shows why each X exists; user can dispute; disputed X goes to review | C13, C14 |
| 108 | a faces-and-plates image is uploaded? | blur before storage | C1 |
| 109 | someone uploads a photo of a private home? | REFUSE storage of non-street images | C1, C2 |
| 110 | someone uses the map to target vendors for eviction? | vendors shown only as "temporary width obstacle", no names, no shop IDs | C14 |
| 111 | a homeless person sleeps on the footpath? | treated as temporary width loss, never labelled publicly | C14 |
| 112 | a judge asks "what about Mumbai at 2 am in July"? | demo: switch time + weather, shows which edges go ? and why | C9, C14 |
| 113 | a judge uploads a random Indian street photo live? | DETECT + shows two-family agreement + confidence; unknowns named | C3 to C5, C14 |
| 114 | a judge uploads a non-street image (a cat)? | REFUSE: "no street found" | C2 |
| 115 | a judge uploads a foreign street photo? | DETECT works but warns "outside India, standards differ" | C1, C14 |
| 116 | there is no internet on the user's phone? | cached route + last known states; shows age | C14 |
| 117 | the Street View API quota runs out? | uses cached panos and user photos; marks fresh state ? | C1 |
| 118 | Street View imagery for the town is from 2022? | age shown, decay applied | C8 |
| 119 | several photos of the same spot disagree? | newest wins for temporary obstacles; majority for permanent; spread shown | C5, C8 |
| 120 | the same pole appears in 5 photos at slightly different GPS points? | clusters into one object (dedupe by position + appearance) | C7 |
| 121 | the GPS track jumps across a river? | map matching rejects impossible jumps | C7 |
| 122 | two footpaths run parallel (service road + main road)? | image heading + width pattern decides; else both ? | C7 |
| 123 | the footpath is inside a flyover pillar zone? | OSM layer + IMG; ? if unclear | C7 |
| 124 | the route needs crossing a median with railings? | DETECT railing; no gap = crossing removed | C3, C11 |
| 125 | the median gap is used by vehicles too? | +2 for crossing there | C10 |
| 126 | the crossing signal gives 8 seconds of green? | ESTIMATE crossing time by profile; if too short, +3 for EL/WK | C10 |
| 127 | the user wants the fastest route, not the most accessible? | user picks the trade-off; barriers still listed | C11, C14 |
| 128 | every route has at least one X for this user? | REFUSE to call any route accessible; shows least-bad route and the exact barrier | C11, C14 |
| 129 | the user is already on the route and hits a new barrier? | live report button, re-route from current point | C11, C13 |
| 130 | the user says "I can do 10 cm steps"? | personal threshold stored | C10 |
| 131 | the user cannot see the screen (blind)? | voice output, step-by-step with barrier warnings | C14 |
| 132 | the user speaks only Tamil / Hindi? | UI language switch | C14 |
| 133 | a world model renders "this street in monsoon"? | labelled as a simulation, never as evidence | C15, C14 |
| 134 | the simulated street shows a ramp that does not exist? | simulation output never feeds the ledger | C15, C8 |
| 135 | a 3D reconstruction gives a kerb height? | used as a third geometry estimate if multi-view; agreement with depth = confidence | C6, C15 |
| 136 | only one image exists, no multi-view? | single-view depth range, wider uncertainty | C6 |
| 137 | the image is taken from a moving bus? | blur + height unknown; ESTIMATE wider ranges | C2, C6 |
| 138 | a drone image is uploaded? | top view: good for width, poor for kerb height; used for width only | C1, C6 |
| 139 | satellite shows a footpath but trees cover it? | UNKNOWN for surface; width from gaps | C1 |
| 140 | a footpath is fine but leads to a closed gate? | OSM access + USER; X | C11 |
| 141 | the destination building itself has steps? | DETECT entrance steps; says "route ends at steps" | C3, C14 |
| 142 | public toilet on the way is locked? | USER report; toilet not counted | C8 |
| 143 | the user needs to rest every 200 m? | prefers routes with seats or shade | C10 |
| 144 | it is 46 C and the only shaded route is longer? | trade-off shown; EL/PG default to shade | C9, C10 |
| 145 | smog AQI is 450? | warns EL/PG; suggests shorter route or waiting | C9 |
| 146 | the dataset has no night photos of the user's city? | night outputs for that city marked low-confidence | C12 |
| 147 | the dataset over-represents Jaipur? | per-city scores reported; other cities flagged lower confidence | C12 |
| 148 | the city is not in OSM well (small town)? | OSM completeness score shown; unknown edges | C11 |
| 149 | the road was renamed or re-numbered? | position-based, names ignored | C7 |
| 150 | a new road opened after the map data? | ASK; user can add a segment for review | C13 |
| 151 | the system is wrong and someone falls? | incident path: apology, review, public log of the fix | C12, C13 |
| 152 | the city wants our data for repairs? | export list with photos, confidence and the law/standard it fails | C14 |
| 153 | the city disputes our findings? | each finding has photo, date, two-model agreement; disputes reviewed | C13 |
| 154 | a contractor is named in a report? | system reports places, not people | C14 |
| 155 | a journalist wants the worst 10 spots? | ranked by severity x usage, with dates and confidence | C14 |
| 156 | traffic police start fining footpath riders and the problem drops? | footpath-riding prior updated from fresh reports | C8, C9 |
| 157 | the photo shows a ramp blocked by a vendor's goods only in the evening? | time-tagged obstacle, evening only | C8, C9 |
| 158 | weekend market every Sunday blocks the street? | weekly pattern learned from repeat reports | C9 |
| 159 | the user is in a wheelchair and the only kerb ramp opens into a pothole? | DETECT both; ramp marked X if pothole at its foot | C3, C6 |
| 160 | tactile paving leads straight into a pole? | DETECT tactile + pole; BL +3, report to city | C3, C10 |
| 161 | the new footpath is too high (above 150 mm) to step onto from the road? | DEPTH: EL +2, MW X without ramp | C6 |
| 162 | a transformer sits in the footpath and the remaining width is 0.6 m? | DETECT + ESTIMATE; MW X | C6 |
| 163 | the photo shows rain but the weather API says dry? | trusts image for that moment, flags conflict | C5, C9 |
| 164 | the user marks a segment "fine" but is a walker, not a wheelchair user? | report counts only for that profile class | C8, C10 |
| 165 | the user asks the system to just say yes or no? | gives yes / no / not sure, with the one-line reason | C14 |

## Part C. D minus A gap list

D = what the ideal SC-02 system needs (from Part A and B). A = what the best existing work already gives. Class I = proxy possible tonight with another fork or a cheap trick. Class II = absorbed by other components. Class III = cannot be done tonight, say so on the site.

Feature claims about existing projects marked UNVERIFIED have not been checked against their code or docs in this round (dsh lane S1 owns that check).

| # | D (needed) | A (who covers it today) | gap | class | tonight's move |
|---|---|---|---|---|---|
| G1 | Indian barrier taxonomy (open drain, missing slab, otla, vendor cart, pandal, bollard spacing) | Project Sidewalk types (S109); Chandigarh adapted types (S89) | open drain / manhole / slab gaps not core PS types (UNVERIFIED for Chandigarh build) | I | add our labels on top of PS types |
| G2 | Indian training labels | PS Chandigarh 3,216 labels (S91); IDD segmentation (S103) | no barrier-level Indian labels at scale | I | label 150 to 300 own photos (MUJ + Jaipur) |
| G3 | Two-family detector agreement | open-vocab detectors + IDD-trained segmenters exist (dsh S1b to confirm) | nobody fuses them for barriers | I | box detector + segmenter + depth vote |
| G4 | Kerb / step height in mm | monocular metric depth models (UNVERIFIED accuracy at kerb scale) | no validated India kerb estimates | I | depth range + tape-measure check on 10 MUJ kerbs |
| G5 | Side-of-road and segment matching | PS geolocates labels via GSV (S89, S109) | phone photos with 5 to 8.5 m GPS error (S101) | I | heading + visible kerb line + nearest footway, else ? |
| G6 | Footway graph for any Indian town | OSM roads; footway tags sparse (HYPOTHESIS) | sidewalks rarely mapped | I | synthesize both-side footways from roads, all ? |
| G7 | Per-profile cost routing | wheelchair costing in Valhalla / OTP / AccessMap (UNVERIFIED) | profiles lack pram, blind, elderly, Indian factors | I | our multiplier table on OSMnx / pgRouting |
| G8 | Evidence ledger with half-life decay | none found | nobody models obstacle lifetimes | I | simple per-type half-life table (L3) |
| G9 | Time and calendar context (vendors, festivals, school) | none found for India | no data | I | rule priors from L5 + user reports |
| G10 | Weather context (rain, fog, heat) | weather APIs exist | not linked to walking cost | I | Open-Meteo / IMD flags into C9 |
| G11 | Hidden hazards under water | none | not detectable from pixels | III | say so: "flooded = unknown"; history only |
| G12 | Rocking slabs, loose covers | none | not visible | III | user / IMU reports only, later |
| G13 | Night robustness | ACDC shows big night drop (S104) | no Indian night barrier set | I/III | flag night outputs low-confidence tonight; real fix needs night labels (III) |
| G14 | Monsoon / snow robustness | ACDC rain/snow (S104) | not Indian | III | shown honestly as low confidence |
| G15 | Honest uncertainty (conformal, "needs a human look") | conformal methods (S108) | not used by sidewalk tools (UNVERIFIED) | I | calibrate on held-out labels, show sets |
| G16 | Crowd reports with trust | PS validations (S109) | no live on-street report loop in India | I | report button + simple reputation |
| G17 | Lighting and safety at night | Safetipin audits (S57) | not merged with accessibility | II | night penalty from lighting reports, cite Safetipin as method |
| G18 | Dog, cattle, crime spots | none integrated | data sparse | III | user reports only; say so |
| G19 | Legal and standards check per barrier | IRC / HG / court orders (S1, S4, S14, S74) | no tool maps a photo to the rule it breaks | I | lookup table from L9 in the export |
| G20 | City report export | none for India | not built | I | CSV + photos + rule cited |
| G21 | Imagery coverage everywhere | GSV India 3,000+ towns (S140), quality mixed (S93) | rural gaps, staleness | II/III | phone photos fill; rural coverage is III |
| G22 | World model "walk it first" / monsoon preview | generative models exist (dsh S1f) | no grounded, labelled-as-simulation walk-through | I | one demo scene, labelled "simulation" |
| G23 | 3D crossing reconstruction | multi-view methods exist (dsh S1f) | slow on GTX 1650 4 GB (to test) | III likely | precompute one scene offline |
| G24 | Voice output for blind users | phone TTS exists | not wired | I | browser speech API |
| G25 | Indian languages UI | i18n trivial | not done | I | Hindi + English tonight |
| G26 | Rural kuccha path model | none | no data | III | say so |
| G27 | Hill town steps-as-roads | OSM steps (partial) | gaps | II | OSM steps tag + ? |
| G28 | Shortcut / adversarial testing | methods known (S105, S106) | nobody tests sidewalk models for it | I | 20-image counterfactual test set |
| G29 | Privacy (faces, plates) | blur models exist | not wired | I | blur on upload |
| G30 | Vendor dignity (no shaming) | none | design choice | II | UI rule: "temporary obstacle", no names |

Counts: Class I 20 (G1 to G10, G15, G16, G19, G20, G22, G24, G25, G28, G29, plus the night flag half of G13); Class II 4 (G17, G27, G30, and the phone-photo half of G21); Class III 8 (G11, G12, G14, G18, G23, G26, plus the night-labels half of G13 and the rural half of G21). Split items are counted in both columns, so the total is above 30.

## Part D. Red-team of this document (claims graded)

| claim | grade | why |
|---|---|---|
| 348 factors (241 with a source, 107 HYPOTHESIS), 165 what-ifs | VERIFIED | counted by script after writing (log line at end). Caveat: for many rows the source proves the obstacle exists in India, not the threshold or cost number; those numbers are claude design values |
| Every S-number points to a fetched URL | VERIFIED at excerpt level | Parallel search excerpts read 2026-10-24; full bodies not read (byte coverage below the user's wc -c rule) |
| IRC:103-2022 kerb ramp 1:15 vs HG 2021 1:12 | VERIFIED | both quoted in excerpts S1 and S4; a real conflict, worth showing judges |
| SC June 2026 "right to walk is fundamental" | PARTLY | Indian Express explainer (S18) says so; case name seen only in a LiveLaw snippet, UNVERIFIED |
| Kolkata stampede 19 dead (Oct 2026) | VERIFIED (news) | The Hindu S60; still a breaking story, numbers may change |
| Half-life numbers in L3 | UNVERIFIED (HYPOTHESIS) | claude estimates; need repeat-photo data |
| Thresholds like "pothole > 5 cm stops a manual chair", "overhead 2.1 m" | UNVERIFIED (HYPOTHESIS) | not sourced; marked |
| Valhalla / OTP / AccessMap wheelchair features | UNVERIFIED | from memory, not checked this round |
| Mapillary and OSM sidewalk sparsity in India | UNVERIFIED | needs Overpass and Mapillary API counts (dsh) |
| Pothole deaths 9,438 (2020 to 2024) | VERIFIED (news quoting MoRTH Lok Sabha reply) | S9, S10 agree |
| Dog bites 37,17,336 (2024) | VERIFIED (news quoting Lok Sabha) | S58; an earlier answer said ~22 lakh for 2024 (S143), so two official figures disagree; use 37 lakh with that note |
| Component list C1 to C15 | DESIGN, not built | proposal only |
| Possible lie in my own work | checked | I first wanted to call IRC and HG "the same standard"; the excerpts show they differ. Fixed in 9.03 |

Known gaps in this doc: no Zhihu / Japanese / Korean sources (hermes lane S2f owns those); no direct Street Vendors Act source; no coastal tide-flood source; no hard number for vendor relapse time after drives; L13 economics thin on real Rs figures for kerb ramps.

## Source registry (fetched 2026-10-24, 15:55 to 16:25 IST, Parallel web_search excerpts)

| S | URL | what it supports |
|---|---|---|
| S1 | https://law.resource.org/pub/in/bis/irc/irc.gov.in.078.2.2020.pdf | IRC:103-2022: 150 mm footpath, ramp 1:15, flares 1:10, tactile laid wrong, light spacing |
| S2 | https://irc.nic.in/admnis/admin/showimg.aspx?ID=345 | IRC:103 draft: cross slope 1:50 to 1:100, 1.2 m clear width, surface breaks |
| S3 | https://irc.nic.in/admnis/admin/showimg.aspx?ID=237 | IRC draft 2020: footpath continuity, 1:8 property ramps |
| S4 | https://niua.in/intranet/sites/default/files/2262.pdf | MoHUA Harmonised Guidelines 2021: ramp 1:12, flares 1:10, width 900 mm, kerbs up to 200 mm, walkway widths by user group |
| S5 | https://portal.mcgm.gov.in/irj/go/km/docs/documents/MCGM%20Department%20List/Roads%20and%20Traffic/Docs/Universal%20Footpath%20Policy%2026.05.2023/Circular%20Universal%20footpath%20policy%2026.pdf | BMC Universal Footpath Policy 2023: 1.8 m, 150 mm, 100 mm protrusion, ramp 1.2 m |
| S6 | https://data.opencity.in/dataset/4f68a0bc-b0ec-44d7-a9d9-77d3980fb7e0/resource/06b6fe78-1b8e-4a6c-b3ce-a3df9f598fca/download/03.nammarastekaipidi_digital.pdf | Namma Raste Kaipidi: bollards 0.9 to 1.2 m, transformers at edge, tree grates 5 mm |
| S7 | https://morth.gov.in/backend/documents/uploaded/Road-Accident-in-India-2023-Publications.pdf | MoRTH RAI 2023 |
| S8 | https://morth.gov.in/backend/documents/uploaded/1781177676_V1gUW8tJWT.pdf | MoRTH RAI 2024: pedestrians 20.6%, city deaths |
| S9 | https://timesofindia.indiatimes.com/india/potholes-killed-9438-from-2020-to-2024-govt/articleshow/128279774.cms | 9,438 pothole deaths |
| S10 | https://indianexpress.com/article/business/pothole-related-road-fatalities-increase-by-53-per-cent-in-5-years-10529465 | +53%, BMC manhole grills |
| S11 | https://www.hindustantimes.com/cities/delhi-news/toddler-dies-after-falling-into-open-manhole-in-narela-101754763662823.html | toddler, open manhole, rain |
| S12 | https://ndrf.gov.in/sites/default/files/Borewell%20Rescue%20Precis.pdf | borewell cases |
| S13 | https://www.thenewsminute.com/karnataka/tnm-investigation-bbmp-and-cops-cover-13-pothole-deaths-bengaluru-170088 | pothole deaths covered up |
| S14 | https://api.sci.gov.in/supremecourt/2012/20376/20376_2012_3_42_61694_Order_14-May-2025.pdf | SC 14 May 2025 order |
| S15 | https://legal.economictimes.indiatimes.com/news/litigation/unauthorised-hawkers-cant-take-over-footpaths-public-roads-hc-suggests-pop-up-markets/109595594 | Bombay HC hawkers 2024 |
| S16 | https://www.business-standard.com/amp/india-news/streets-footpaths-cleared-for-pm-vvips-why-not-for-everyone-bombay-hc-124062400395_1.html | VVIP clearing |
| S17 | https://www.thehindu.com/news/national/centre-must-ensure-every-road-has-encroachment-free-space-for-walking-supreme-court/article71300211.ece | SC 3 Aug 2026 |
| S18 | https://indianexpress.com/article/explained/supreme-court-pedestrian-rights-footpath-judgment-explained-10749259 | SC June 2026 explainer |
| S19 | https://www.livelaw.in/high-court/karnataka-high-court/karnataka-high-court-stays-demolition-kr-market-shops-forged-licenses-right-to-footpaths-540579 | Karnataka HC, Safe Footpath campaign |
| S20 | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | Jaipur stalls, cafes, parking, dairy booths |
| S21 | https://timesofindia.indiatimes.com/city/jaipur/encroachments-choke-mi-road-pavements-forcing-pedestrians-into-heavy-traffic/articleshow/131896991.cms | MI Road Jaipur |
| S22 | https://timesofindia.indiatimes.com/city/jaipur/encroachments-make-jaipur-footpaths-unsafe/articleshow/131374323.cms | Tonk Road, handcarts, loading vehicles |
| S23 | https://timesofindia.indiatimes.com/city/jaipur/sc-orders-pavement-overhaul-but-civic-bodies-have-failed-jaipur-pedestrians-before/articleshow/131882922.cms | govt encroachments Jaipur |
| S24 | https://www.thestatesman.com/india/dimagi-naxal-group-lawyers-demand-removal-of-encroachments-from-footpaths-in-jaipur-1503633692.html | JVVNL junction boxes |
| S25 | https://www.thehindu.com/news/cities/bangalore/bengalurus-footpaths-belong-to-everyone-but-pedestrians/article71182538.ece | height changes, trenches, official vehicles |
| S26 | https://bangaloremirror.indiatimes.com/bangalore/cover-story/all-over-the-place/articleshow/134973794.cms | 17,705 footpath riding cases, bollard gaps |
| S27 | https://timesofindia.indiatimes.com/city/mumbai/footpath-bollards-a-mockery-of-wheelchair-bound-people/articleshow/104056186.cms | bollards vs wheelchairs, HC |
| S28 | https://www.thehindu.com/news/cities/bangalore/broken-and-inaccessible-bengalurus-footpaths-fail-persons-with-disabilities/article71202931.ece | poles, trees, dips a cane misses |
| S29 | https://timesofindia.indiatimes.com/city/bengaluru/video-bengaluru-footpath-transformer-explodes-outside-amazon-office-2-injured/articleshow/134758802.cms | transformer explosion |
| S30 | https://www.newindianexpress.com/cities/chennai/2025/Feb/03/encroachments-kerb-parking-make-footpaths-inaccessible-for-disabled-in-chennai | Chennai kerb parking, railings |
| S31 | https://www.thenewsminute.com/news/bengalurus-open-drains-civic-negligence-creates-a-daily-hazard-for-residents | missing slabs, planks, 10,072 broken footpaths |
| S32 | https://bangaloremirror.indiatimes.com/bangalore/civic/citizens-fall-through-cracks-of-poor-quality-drain-work/articleshow/97846913.cms | slab gave way |
| S33 | https://www.hindustantimes.com/cities/bengaluru-news/bengalurus-ejipura-footpaths-crumble-months-after-upgrade-101762056198562.html | crumbling new footpaths |
| S34 | https://www.thehindu.com/news/cities/bangalore/corruption-root-cause-of-low-quality-road-works-leading-to-potholes/article66045475.ece | kerosene, 30,000 potholes |
| S35 | https://www.hindustantimes.com/mumbai/paver-block-scam-can-blow-lid-off-bmc-s-policy/story-yWUE9AG63Ie52A2zdpxgwM.html | paver block scam |
| S36 | https://sansad.in/getFile/loksabhaquestions/annex/186/AU3054_CnAPuy.pdf?source=pqals | defect liability, penalties |
| S37 | https://www.onmanorama.com/news/kerala/2026/08/05/thrissur-corp-s-2-cr-scientific-footpath-directs-water-to-houses-blocks-shop-access-work-halted-over-protests.html | bad footpath design |
| S38 | https://timesofindia.indiatimes.com/city/dehradun/june-7-deadline-ends-dug-up-roads-continue-to-disrupt-daily-life-in-doon/articleshow/131608931.cms | debris after deadline |
| S39 | https://timesofindia.indiatimes.com/city/bengaluru/infra-hurdle-7-5km-of-pink-line-ready-bannerghatta-road-still-in-a-rut/articleshow/128270619.cms | pipes, debris, no footpath |
| S40 | https://www.newindianexpress.com/cities/bengaluru/2025/Sep/21/bengalurus-broken-roads-turn-daily-walks-into-a-nightmare-for-elderly-vulnerable | trenches, elderly, pregnant |
| S41 | https://www.mid-day.com/mumbai/mumbai-news/article/mumbai-residents-struggle-for-safe-access-as-santacruz-footpath-dug-up-23598737 | footpath dug, no work |
| S42 | https://www.newindianexpress.com/states/delhi/2026/Aug/07/open-drains-turn-deadly-in-rain-hit-delhi-as-man-goes-missing-three-children-narrowly-survive | children fell into drain hidden by water |
| S43 | https://timesofindia.indiatimes.com/city/hyderabad/man-swept-away-after-falling-into-open-drain-in-miyapur-search-still-on/articleshow/132721244.cms | 70-year-old swept away |
| S44 | https://timesofindia.indiatimes.com/city/mumbai/mumbai-monsoon-in-pictures-waterlogged-roads-uprooted-trees-flooded-streets/photostory/132136037.cms | waterlogging concealed open manhole |
| S45 | https://www.indiatoday.in/cities/gurugram/story/gurugram-rain-waterlogging-children-stranded-roads-cave-in-millennium-city-2980096-2026-08-26 | 70 mm in 35 min, cave-in |
| S46 | https://indianexpress.com/article/cities/chandigarh/shimla-snowfall-traffic-power-supply-imd-weather-10490004 | Shimla snow |
| S47 | https://www.hindustantimes.com/india-news/massive-dust-storm-engulfs-parts-of-rajasthan-disrupts-life-as-winds-hit-80-kmph-video-101780147638148.html | dust storm zero visibility |
| S48 | https://www.telegraphindia.com/india/dense-fog-severe-pollution-choke-delhi-low-visibility-disrupts-traffic-and-flights/cid/2138433 | fog 150 to 200 m |
| S49 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11790314/ | heatwave mortality, 10 cities |
| S50 | https://timesofindia.indiatimes.com/city/kolkata/8-die-on-waterlogged-city-streets-in-24-hours/articleshow/124075098.cms | 8 deaths, waterlogged streets |
| S51 | https://www.indiatoday.in/cities/delhi/story/uttam-nagar-boy-dies-of-electocution-after-grabbing-iron-pipe-in-flooded-delhi-lane-2988037-2026-09-06 | electrocution at pole |
| S52 | https://www.thehindu.com/news/national/karnataka/tree-fall-incidents-double-in-bengaluru-this-monsoon-three-killed/article70189581.ece | tree falls |
| S53 | https://www.dtnext.in/news/city/citizen-connect-dangling-cables-on-footpaths-in-anna-nagar-pose-risks-791052 | dangling cables |
| S54 | https://timesofindia.indiatimes.com/city/ahmedabad/dark-truth-ahmedabads-unlit-stretches-create-safety-concerns/articleshow/134749135.cms | streetlight complaints |
| S55 | https://timesofindia.indiatimes.com/city/bhopal/areas-of-darkness-inoperative-streetlights-overshadow-safety/articleshow/124562094.cms | 5,361 of 20,618 off |
| S56 | https://www.thehindu.com/news/cities/Delhi/aastha-kunj-gang-rape-area-was-already-a-delhi-police-dark-spot-but-lighting-gaps-remained/article71506949.ece | dark spot, 33% lights off |
| S57 | https://safetipin.com/wp-content/uploads/2024/05/safety-audits-in-delhi-2023.pdf | Safetipin Delhi 2023 |
| S58 | https://www.thehindu.com/news/national/over-37-lakh-dog-bite-cases-54-human-rabies-deaths-in-2024-govt-tells-lok-sabha/article69842885.ece | dog bites 2024 |
| S59 | https://timesofindia.indiatimes.com/city/bhopal/437-deaths-in-8-months-stray-cattle-turn-mp-roads-into-a-deadly-maze/articleshow/134419642.cms | cattle deaths MP |
| S60 | https://www.thehindu.com/news/cities/kolkata/kolkata-durga-puja-stampede-toll-rises-to-19-sitting-hc-judge-to-probe-incident/article71598984.ece | Durga Puja stampede |
| S61 | https://www.hindustantimes.com/cities/pune-news/ganesh-pandals-continue-to-block-roads-amid-pmc-inaction-despite-prior-warnings-101757620596074.html | pandals block roads |
| S62 | https://r3app.mcgm.gov.in/irj/go/km/docs/documents/HomePage%20Data/Quick%20Links/Ganeshotsav%20and%20other%20festivals/12.05.2017%20MDF-418-Gen.pdf | BMC pandal circular |
| S63 | https://www.newindianexpress.com/states/tamil-nadu/2025/Jul/05/safety-markings-vanish-from-many-tiruchy-roads | faded zebras |
| S64 | https://www.thehindu.com/news/cities/Tiruchirapalli/defunct-traffic-signals-cause-chaos-at-key-junctions-in-tiruchi/article70987156.ece | defunct signals |
| S65 | https://www.newindianexpress.com/states/tamil-nadu/2025/Aug/29/traffic-signals-on-the-blink-thanjavur-motorists-see-red | Smart City signals defunct |
| S66 | https://www.thehindu.com/news/national/karnataka/pedestrians-feel-sidelined-as-bengalurus-traffic-signal-system-prioritise-vehicles/article70225790.ece | short pedestrian greens |
| S67 | https://www.hindustantimes.com/cities/gurugram-news/ggms-foot-over-bridges-in-disrepair-pedestrians-forced-to-risk-roads-101741629910602.html | FOB escalators dead |
| S68 | https://telanganatoday.com/erragadda-foot-overbridge-unusable-as-lifts-and-escalators-remain-out-of-service | FOB lifts dead |
| S69 | https://timesofindia.indiatimes.com/city/jaipur/ngo-raises-alarms-over-road-safety-deficiencies-in-city-crossings/articleshow/132519124.cms | Jaipur crossings |
| S70 | https://www.mid-day.com/mumbai/mumbai-news/article/mumbai-fading-road-markings-put-city-commuters-at-risk-bmc-promises-post-monsoon-fix-23588710 | fading markings |
| S71 | https://www.hindustantimes.com/india-news/over-26-500-people-died-on-mumbai-railway-tracks-in-10-years-rti-data-reveals-101752780145113.html | 26,547 track deaths |
| S72 | https://sansad.in/getFile/annex/268/AU2359_YvrBqk.pdf?source=pqars | unmanned LCs eliminated |
| S73 | https://www.dtnext.in/news/chennai/revamp-works-stump-wheelchair-users-at-egmore-railway-station | Egmore station no lift |
| S74 | https://www.api.sci.gov.in/supremecourt/2005/9321/9321_2005_1_1503_56986_Judgement_08-Nov-2024.pdf | Rajive Raturi 2024 |
| S75 | https://ccpd.nic.in/harmonized-guidelines-for-standards-of-accessibility | RPwD sections 40 to 46 |
| S76 | https://saiindia.gov.in/webroot/uploads/download_audit_report/2023/PAG-(Au-I)-Raj-Rights-of-Persons_Report_Eng-1_OCR-064b7cfee846c19.93032773.pdf | CAG Rajasthan RPwD |
| S77 | https://www.theindiaforum.in/forum/indias-accessibility-promise-and-its-implementation-gap | CAG 2025 retrofit finding |
| S78 | https://cag.gov.in/en/audit-report/details/123892 | CAG Smart City (Karnataka) |
| S79 | https://timesofindia.indiatimes.com/city/lucknow/cags-urban-mobility-audit-to-assess-lmc-work/articleshow/133074856.cms | CAG urban mobility audit |
| S80 | https://sansad.in/getFile/loksabhaquestions/annex/178/AU3212.pdf?source=pqals | AIC deadlines revised |
| S81 | https://www.cag.org.in/database/launch-report-moving-without-barriers-documenting-mobility-barriers-encountered-people | Chennai: two-thirds cannot reach transit |
| S82 | https://timesofindia.indiatimes.com/india/at-1-5-lakh-pedestrians-made-up-20-of-road-deaths-in-5-years/articleshow/121241568.cms | SC panel audit footpath availability |
| S83 | https://www.mospi.gov.in/sites/default/files/publication_reports/Persons_Disabilities_31mar21.pdf | 2.68 crore disabled |
| S84 | https://india.unfpa.org/sites/default/files/pub-pdf/20230926_india_ageing_report_2023_web_version_.pdf | India Ageing Report 2023 |
| S85 | https://cdn.who.int/media/docs/default-source/searo/ageing-and-health/fact-sheets-2024/india---facts-and-figures---healthy-ageing.pdf | 11% to 21% elderly |
| S86 | https://opencity.in/road-crashes-in-2023-pedestrians-left-high-and-dry-as-fatalities-mount/ | 35,221 pedestrian deaths |
| S87 | https://www.news18.com/india/how-many-pedestrians-died-in-india-in-2023-roads-ministry-ncrb-data-at-odds-yet-again-ws-kl-9605482.html | MoRTH vs NCRB |
| S88 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2206995 | 1.15 crore vendors target |
| S89 | https://arxiv.org/abs/2602.09216v1 | Project Sidewalk Chandigarh adaptation |
| S90 | https://dl.acm.org/doi/fullHtml/10.1145/3517428.3550381 | cross-city training results |
| S91 | https://sidewalk-chandigarh.cs.washington.edu/leaderboard | Chandigarh label counts |
| S92 | https://blog.google/intl/en-in/products/explore-communicate/google-announces-local-partnerships-to-build-a-more-helpful-maps-experience-in-india | Street View India 2022 |
| S93 | https://virtualstreets.org/index.php/2025/06/20/india-steps-into-a-new-street-view-era | imagery quality and age |
| S94 | https://www.telegraphindia.com/my-kolkata/lifestyle/google-street-view-is-now-in-india/cid/1876870 | geospatial policy, local entities |
| S95 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5672886 | step-climbing wheelchairs |
| S96 | https://pubmed.ncbi.nlm.nih.gov/41945617 | cross slope 3% one-rim |
| S97 | https://pubmed.ncbi.nlm.nih.gov/17207679/ | handrim 1.8x at 6 degrees |
| S98 | https://assets.publishing.service.gov.uk/media/5a79554040f0b63d72fc4e31/inclusive-mobility.pdf | thresholds 10 mm, cross-fall 2.5%, chair width |
| S99 | https://trid.trb.org/View/921388 | perceived slope limits |
| S100 | https://sites.temple.edu/phire/files/2019/09/Conference_RESNA_LinJ_2011.pdf | surfaces and push force |
| S101 | https://www.cambridge.org/core/journals/journal-of-navigation/article/positional-accuracy-of-assisted-gps-data-from-highsensitivity-gpsenabled-mobile-phones/E1EE20CD1A301C537BEE8EC66766B0A9 | phone GPS 5 to 8.5 m |
| S102 | https://www.sciencedirect.com/science/article/pii/S0263224123013301 | urban canyon NLOS errors |
| S103 | https://idd.insaan.iiit.ac.in/media/publications/idd-650.pdf | IDD dataset |
| S104 | https://acdc.vision.ee.ethz.ch/other/ACDC_the_Adverse_Conditions_Dataset_with_Correspondences_for_semantic_driving_scene_understanding-Sakaridis+Dai+Van_Gool-ICCV_21.pdf | ACDC night/fog/rain/snow drop |
| S105 | https://arxiv.org/abs/2004.07780 | shortcut learning |
| S106 | https://arxiv.org/abs/1712.09665 | adversarial patch |
| S107 | https://arxiv.org/abs/2305.10355 | POPE VLM hallucination |
| S108 | https://arxiv.org/abs/2107.07511 | conformal prediction |
| S109 | https://projectsidewalk.org/api | PS label types, open data |
| S110 | https://www.hindustantimes.com/india-news/weather-today-live-updates-rain-delhi-ncr-monsoon-imd-alert-mumbai-rain-news-traffic-uttarakhand-himachal-karnataka-101782952377331.html | Mumbai manhole death, 4 officials suspended |
| S111 | https://www.nationalheraldindia.com/environment/landslides-now-a-year-round-threat-in-the-hills | Uttarakhand landslides |
| S114 | https://www.hindustantimes.com/cities/mumbai-news/hc-labels-mumbai-s-hawker-menace-a-disease-orders-bmc-to-clear-vikhroli-encroachments-101763579764320.html | Bombay HC 2025 hawkers |
| S115 | https://www.thehindu.com/news/cities/chennai/commute-along-battered-arcot-road-gets-exasperating-thanks-to-chennai-metro-rail-construction-work/article69448492.ece | metro construction |
| S116 | https://timesofindia.indiatimes.com/city/bengaluru/bengalurus-pink-line-metro-set-to-open-in-sept-but-access-will-be-a-challenge/articleshow/133659533.cms | missing footpaths, garbage, open drains at new metro |
| S117 | https://timesofindia.indiatimes.com/city/bengaluru/drive-against-abandoned-vehicles-begins-but-clarity-eludes-footpath-parking/articleshow/132317212.cms | abandoned and police vehicles on footpaths |
| S118 | https://bangaloremirror.indiatimes.com/bangalore/cover-story/great-barrier-grief/articleshow/114226077.cms | bollards, ramps, tactile |
| S119 | https://www.indiatoday.in/diu/story/rajasthan-dust-storm-western-disturbance-rain-north-india-2920468-2026-06-01 | Churu dust storm |
| S120 | https://www.cag.org.in/blogs/chennais-journey-become-pedestrian-friendly-space | IRC widths ignored, two-wheelers on footpaths |
| S121 | https://www.indiatoday.in/cities/mumbai/story/navi-mumbai-rains-exposed-wire-shocks-two-women-on-waterlogged-nerul-road-2938381-2026-07-01 | electrified water |
| S122 | https://www.thehindu.com/news/national/uttarakhand/one-dead-after-landslip-hits-kedarnath-walking-route-yatra-suspended-from-sonpryag-till-further-orders/article69698215.ece | Kedarnath walking route landslip |
| S123 | https://www.indiatoday.in/india/video/durga-puja-crowd-rush-near-central-avenue-sparks-safety-concerns-in-kolkata-ytvd-3019904-2026-10-17 | crowd rush in rain, narrow lane |
| S124 | https://www.freepressjournal.in/mumbai/mumbai-monsoon-tragedy-50-year-old-man-in-icu-after-branch-collapses-in-andheri-amid-rising-safety-concerns | branch fall on walker |
| S125 | https://www.business-standard.com/health/india-stray-dog-bite-cases-children-elderly-risk-125072900356_1.html | dog bites, children and elderly |
| S126 | https://www.indiatoday.in/trending-news/story/bengaluru-footpath-mess-gets-a-temporary-fix-after-canadian-vlogger-takedown-indiranagar-3009753-2026-10-05 | quick fix after viral video |
| S127 | https://www.thehindu.com/news/cities/bangalore/sanjaynagar-main-road-work-near-completion-footpath-woes-persist-for-bengaluru-residents/article71543531.ece | footpath works dragging |
| S129 | https://ebooks.iospress.nl/publication/40692 | wheelchair uphill slope physiology |
| S130 | http://tcpo.gov.in/sites/default/files/TCPO/schemes/Harmonisedguidelinesdreleasedon23rdMarch2016.pdf | HG 2016: ramp table, landings, grating width |
| S131 | https://niua.in/intranet/sites/default/files/2346.pdf | NIUA guide: riser 150 mm, 1.5 to 1.8 m footpath |
| S132 | https://timesofindia.indiatimes.com/city/jaipur/jmc-intensifies-encroachment-drive-across-the-city/articleshow/125773489.cms | JMC drive |
| S133 | https://www.dtnext.in/news/tamilnadu/monsoon-safety-advisory-for-public-eb-staff | NE monsoon advisory, lightning |
| S134 | https://www.hindustantimes.com/india-news/science-behind-delhi-pre-monsoon-dust-storms-in-summer-101781081349171.html | 128 kmph storm |
| S135 | https://api.sci.gov.in/supremecourt/2005/9321/9321_2005_7_813_68785_Order_23-Feb-2026.pdf | Rajive Raturi follow-up order |
| S136 | https://www.thehindu.com/news/national/targets-missed-accessible-india-campaigns-deadline-extended/article30300230.ece | AIC targets missed |
| S137 | https://prsindia.org/files/policy/policy_committee_reports/1472703813_CAG%20Summary-%20suburban%20train%20services.pdf | CAG suburban rail |
| S138 | https://www.thehindu.com/news/cities/chennai/tamil-nadu-assembly-elections-2026-1000-crore-unpaid-1200-new-tenders-chennai-corporations-pre-poll-rush-sparks-transparency-concerns/article70732483.ece | unpaid dues, footpath tender |
| S139 | https://www.thehindu.com/news/national/take-steps-to-ensure-proper-footpaths-supreme-court-tells-states/article69575980.ece | SC May 2025 news |
| S140 | https://www.business-standard.com/companies/news/google-maps-gets-powered-up-by-ai-expands-across-3-000-indian-cities-123121901102_1.html | 3,000 cities |
| S141 | https://indianexpress.com/article/cities/chandigarh/rs-10-crore-civic-push-in-chandigarh-paver-blocks-relaying-drainage-upgrade-sewer-strengthening-approved-10610659 | paver relaying spend |
| S142 | https://www.impriindia.com/insights/policy-update/accessible-india-campaign-sugamya-bharat-abhiyan-2015-an-analysis-of-progress-and-challenges/ | AIC Rs 562 crore |
| S143 | https://indianexpress.com/article/india/dog-bite-cases-reported-in-2024-children-victims-9817586/ | 5 lakh child victims; earlier ~22 lakh figure |

(S112, S113, S128 unused; numbers kept so references stay stable.)

## Picks for a non-expert judge

**10 factors:** (1) open drain hidden under monsoon water, 6.03; (2) pothole seen by day, invisible at night, 7.05; (3) footpath height changes every few metres, 1.11; (4) bollards meant to stop bikes also stop wheelchairs, 1.25; (5) electrified rainwater near poles, 6.04; (6) vendors and parking back within hours of a clearance drive, 4.05; (7) zebra crossing in name only plus dead signals, 2.20 / 9.24; (8) foot over bridge whose lift is broken, 1.23; (9) the government's own transformers and junction boxes on footpaths, 3.02 / 3.03; (10) two official standards giving different ramp slopes, 9.03.

**10 what-ifs:** #1 pothole under water, #2 photo 3 years old, #3 vendor after the photo, #4 only route has a step, #5 GPS wrong side, #6 detectors disagree, #7 Leh snow upload, #10 fake sticker, #73 day pothole at night, #99 "is it safe?" (it never says safe, only known / unknown / photo age).

## Log

- 2026-10-24 16:40 IST, python count over this file: 348 factor rows (L1 34, L2 32, L3 34, L4 25, L5 19, L6 23, L7 16, L8 26, L9 29, L10 26, L11 24, L12 22, L13 18, L14 20); 241 rows cite an S-source, 107 are HYPOTHESIS; 165 what-if rows; every cited S-number exists in the registry; 0 em dashes; banned-word grep clean.
