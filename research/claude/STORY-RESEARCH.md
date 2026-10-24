# STORY RESEARCH v1 (claude, 2026-10-24 ~18:30 IST)

SC-02, accessible walking routes from street images, all of India. Lane from DECISIONS.md D5 (user story direction: multi-perspective, cat, small bird, old lady, ordinary guy, wheelchair user, follow one, emotional, more interactables).
Inputs read in full: research/BRAINSTORM-SYNTHESIS-v1.md (4,582 B), ARCHITECTURE-v1.md (4,910 B), research/hermes/JUDGE-LENS.md (11,543 B), DECISIONS.md D5 lines.
Search: Parallel web_search + web_fetch, 22 calls, session hypnexis-story-research. Every row below has a URL and a date (page date, or "n.d." when the page shows none).

Part 1 is research (sourced). Part 2 is a PROPOSAL (my design, not sourced; only the facts inside it are sourced).

---

## 0. TL;DR

```
ONE STREET IN JAIPUR, SIX HEIGHTS, ONE MAP

 600 cm  Gunjan (myna)   sees the network    -> routing + map
 158 cm  Kabir (phone)   sees nothing        -> the camera / upload
 140 cm  Kamla Devi      sees the clock      -> leave-time, rest stops, shade
 115 cm  Zoya            knows every kerb    -> the barrier profile
  95 cm  Pihu (pram)     sees exhaust pipes  -> curb-cut effect (helps everyone)
  22 cm  Billu (cat)     sees cliffs         -> the measuring stick (kerb in cm)
         Rekha Meena, JE has the budget      -> the complaint / receipt goes to her
```

- Follow **Billu the one-eyed street cat**, who rides on **Zoya's** lap. Billu is the camera, Zoya is the heart, Kabir is the judge's mirror.
- Each character holds one piece of the picture. The product is the thing that puts the pieces together, so every product feature walks in carried by the character who owns it. The demo never breaks the story because the demo IS the last act.
- Emotional turn: Kabir finally looks up and offers to lift Zoya over the kerb. She says **"Mujhe uthao mat. Raasta do."** ("Don't lift me. Give me a way.") Sound drops to Billu's purr. Kabir raises his phone, this time at the kerb.
- Line judges remember: **"Don't lift me. Give me a way."**

---

# PART 1: RESEARCH

## 1.1 What wins now (web, 2024-2026)

| # | piece | award + date (sourced) | what it does | technique to take | source |
|---|---|---|---|---|---|
| W1 | **Santioni Spirits, "The Notturno Experience"** (Active Theory, sound by plan8) | Awwwards SOTD 5 Oct 2026, Developer Award 7.66 | comic-book world, B/W ink plus one spot colour, narration boxes where a comic puts them, rough paper border | **hold-to-advance** instead of scroll: "a gesture that costs something", sound builds against the hold | https://www.awwwards.com/sites/santioni-spirits (n.d.); https://www.utsubo.com/blog/immersive-storytelling-websites-guide (page dated 2026-01-09 but cites May/June 2026 awards, so it was updated later) |
| W2 | **Ponpon Mania** (Justine Soulie + Patrick Heng, 2 people) | Awwwards SOTD 22 Oct 2025, SOTM Oct 2025 | interactive web comic about a sheep DJ | panel camera moves, mouse-reactive objects, Matter.js physics on 2D art, chapters as album tracks; proof that 3D is optional | https://www.awwwards.com/sites/ponpon-mania (n.d.); https://www.awwwards.com/ponpon-mania-a-comic-that-breathes-through-web-interaction.html (2025-11-26); https://www.webgpu.com/showcase/ponpon-mania-webgl-interactive-comic (2026-03-26) |
| W3 | **Messenger** (abeto) | listed as SOTY 2025 on the Awwwards SOTY page (listing excerpt is jumbled, see claims table) | tiny spherical planet, you deliver mail, calm but a little odd, lo-fi music | a world with no invisible walls; walk any direction and come back; calm pace as a feeling | https://www.awwwards.com/websites/sites_of_the_year (n.d.); https://www.commarts.com/webpicks/messenger (2025-12-09); https://www.awwwards.com/messenger.html (2026-01-15) |
| W4 | **Igloo Inc** (abeto) | Awwwards SOTY 2024 | immersive 3D | jury: "combines an immersive 3d experience with an easy to navigate, scroll interaction" | https://www.awwwards.com/annual-awards-2024/site-of-the-year (n.d.) |
| W5 | **IVRESS, Spin a Tale** (Utsubo, self-reported) | FWA of the Month May 2026, Awwwards SOTD 28 Jun 2026 (claimed by the maker) | 7 scenes, no voiceover, last scene loops to the first | continuous transitions (each scene becomes the next), loop structure | utsubo guide above |
| W6 | **Why Zero** (Sindhur Dutta) | (featured in Utsubo guide) | argument site built like a game | gated sections, hold to proceed, XP counter; "let the interaction model restate your thesis" | utsubo guide above |
| W7 | 2026 Awwwards mechanics sweep | 14 sites, read 2026-07-16 / 2026-08-29 | catalogue of mechanics | **per-chapter Web Audio scenes** are rare in winners and cheap to build: "high perceived-craft payoff"; Rive path-scroll; sticky stacked cards | https://github.com/coroboros/research/blob/main/articles/award-winning-websites-2025-2030/winners/awwwards-2026-winners.md (2026-07-30) |
| W8 | Cannes Lions 2026 Digital Craft Grand Prix: **"Project Genie"** (Google, Genie 3 world model in a consumer interface) | 23 Jun 2026 | world model you can walk in | juries are rewarding world models as craft right now; our "switch body" on a reconstructed street sits in this lane | https://www.canneslions.com/news/cannes-lions-international-festival-of-creativity-announces-winners-across-the-entertainment-and-craft-track-lions (2026-06-23) |
| W9 | Cannes Lions 2025: new **Inclusive Design** Lions; Grand Prix "Caption with Intention" (FCB Chicago, two Grands Prix) | 17 Jun 2025 | captions redesigned for deaf viewers | accessibility as a craft category, not a charity category | https://www.canneslions.com/news/cannes-lions-announces-2025-winners-across-entertainment-and-craft-tracks (2025-06-17); https://www.thedrum.com/opinion/cannes-lions-2025-did-accessibility-finally-hit-the-creative-mainstream (2025-07-01) |
| W10 | Webby 2026 has an **Accessible Technology** category ("above and beyond compliance") | 2026 | | our own site must pass its own test (captions, keyboard, reduced motion) | https://winners.webbyawards.com/winners/websites-and-mobile-sites (n.d.) |
| W11 | The Pudding | Online Journalism Awards entry 2025 | visual essays | "spoonful of sugar" method; goal "a visceral, emotional experience" | https://awards.journalists.org/entries/the-pudding-3 (2025-08-22) |

## 1.2 Interactive documentary and point of view

| # | piece | award / date | technique to take | source |
|---|---|---|---|---|
| D1 | **Bear 71** (NFB, Mendes + Allison, Jam3) | 2012 web, VR 2017; "multi-award-winning" (NFB) | told by the animal herself (narrated as the grizzly); the park is a **surveillance grid map** where you can also follow other tagged animals; humans seen through camera traps | https://opendoclab.mit.edu/bear-71 (2012-02-21); https://mediaspace.nfb.ca/epk/bear71vr (2017-02-08); https://niche-canada.org/2025/12/05/playing-inside-the-grid-bear-71-do-not-track-and-life-under-observation (2025-12-05) |
| D2 | **Notes on Blindness: Into Darkness** (Arte, Ex Nihilo, Archer's Mark) | Peabody 2022 (XR), Prix Europa 2016 Best Web Project, Kaleidoscope 2016 | built from **John Hull's own audio diaries**, binaural sound, 6 short chapters, 7 min each part | https://www.arte.tv/digitalproductions/en/notes-on-blindness (n.d.); https://voicesofvr.com/1068-notes-on-blindness-vr-experience-receives-a-legacy-peabody-award-for-interactive-storytelling (2022-03-24) |
| D3 | **Out My Window** (NFB Highrise, Kat Cizek) | 2010 | one of the first 360 web docs; 13 cities, people seen through their own windows | https://blog.nfb.ca/blog/2010/10/15/the-nfbs-highrise-project-unveils-its-new-interactive-web-documentary-out-my-window (2010-10-15) |
| D4 | **Life on Hold** (Al Jazeera) | 2015 | **10 characters**, one pane each, any order; each artwork decays with days since leaving Syria | http://i-docs.org/life-on-hold-al-jazeera-web-documentary-reflects-on-the-syrian-refugee-crisis/ (2015-05-06) |
| D5 | **Welcome to Pine Point** | 2 Webbys 2011 | memory scrapbook of a town that no longer exists | https://en.wikipedia.org/wiki/Welcome_to_Pine_Point (2011) |
| D6 | **despelote** (Cordero + Valbuena, Panic) | **BAFTA 2026 Game Beyond Entertainment**; IGF 2025 Excellence in Audio; IDFA DocLab competition | 2001 Quito "from the perspective of an eight-year-old", "viewing the world from hip height"; scanned photos of real streets; ambient sound **field-recorded on site** with friends and strangers; **positional audio**: voices get clearer as you get closer | https://www.bafta.org/awards/games/game-beyond-entertainment (n.d.); https://www.engadget.com/gaming/despelote-review-a-poignant-memoir-masquerading-as-a-soccer-game-124526276.html (2025-05-02); https://unity.com/blog/despelote-creator-narrative-game-design-goals (2025-06-11); https://festival.idfa.nl/en/section/9186c4fe-01f0-44b3-bdc0-7cd620e24b37/IDFA-DocLab-Competition-for-Digital-Storytelling (n.d.) |
| D7 | **Urban95** (Van Leer Foundation) | running since 2016; Udaipur joined 2019 as 3rd Indian city | asks planners: "If you could experience the city from an elevation of 95 cm, the height of a 3 year old, what would you do differently?" Udaipur norms include "protection against pollution at 95cm eye-level" | https://vanleerfoundation.org/ecm-article/urban95-creating-cities-for-the-youngest-people/ (2018-06-28); https://udaipurmc.org/uploads/1673006630-1001.pdf (2020-07-15); https://southasia.iclei.org/news/urban95-set-to-give-udaipur-a-child-friendly-makeover/ (n.d.) |

Why D7 matters: "design the city from one body's eye height" is already a funded planning method in Rajasthan. Our switch-body interactable is not a gimmick; it generalises an existing practice to every body.

## 1.3 Games (scale, non-human eyes, emotion)

| # | game | award (sourced) | technique to take | source |
|---|---|---|---|---|
| G1 | **Stray** (BlueTwelve, 2022) | The Game Awards 2022 Best Independent Game | camera "just one foot off the ground"; city as a jungle gym; makers: "the camera that is too close to the ground" made every system harder; the cat is "a very neutral character without taking sides" | https://www.radiotimes.com/technology/gaming/the-game-awards-uk (2022-12-09); https://www.ign.com/articles/stray-review (2022-07-18); https://www.destructoid.com/bluetwelve-interview-and-developing-the-world-of-stray/ (2024-01-26); https://journals.ed.ac.uk/ear/article/view/8958 (2024-02-29) |
| G2 | **Little Kitty, Big City** (Double Dagger, 2024) | Indie Game Awards 2024 Debut; BAFTA 2024 Family nominee | "From the cat's perspective, it's their world, and humans are living in it"; 100k units in 48 h | https://www.littlekittybigcity.com/ (n.d.); https://www.nintendolife.com/features/little-kitty-big-city-dev-talks-cat-vids-cosy-fatigue-finding-inspiration-in-dark-souls (2024-03-11); https://www.gamesindustry.biz/little-kitty-big-city-the-former-half-life-devs-cat-game-for-his-kids-that-became-an-overnight-success (2024-06-27) |
| G3 | **Florence** (Mountains, 2018) | (award not confirmed in this pass) | no dialogue; "the feeling or story has to come from the interactions, not from the images"; everyday actions turned into tiny games (brushing teeth = rub back and forth); colour arrives only at important moments | https://www.gamedeveloper.com/audio/designing-i-florence-i-to-convey-the-ineffable-feeling-of-being-in-love (2018-03-02); https://www.gamedeveloper.com/design/moments-from-florence (2021-08-16) |
| G4 | **Before Your Eyes** (GoodbyeWorld) | BAFTA 2022 Game Beyond Entertainment | webcam blink advances the story; a metronome warns that the next blink will cut; "the scene knows you're going to blink and cry" | https://www.bafta.org/media-centre/press-releases/bafta-games-awards-2022-winners-announced (2022-04-07); https://www.gamedeveloper.com/design/gone-before-you-blink-the-webcam-driven-gameplay-of-before-your-eyes (2021-12-14) |
| G5 | **Gris** (Nomada) | The Game Awards 2019 Games for Impact | wordless; world starts colourless, each chapter returns one colour; abilities return as she heals | https://thegameawards.com/rewind/year-2019 (n.d.); https://www.polygon.com/2018/12/15/18138073/gris-game-art-music-gameplay-nomada-studio (2018-12-15) |
| G6 | **That Dragon, Cancer** (Numinous) | The Game Awards 2016 Games for Impact | real home-video audio of the family; "the objective of the player is not to solve problems, but simply to be present"; it cannot be won | https://www.pcgamer.com/that-dragon-cancer-creator-delivers-poignant-speech-on-the-power-of-games/ (2016-12-02); https://docubase.mit.edu/project/that-dragon-cancer/ (n.d.); https://jamanetwork.com/journals/jama/fullarticle/2771583 (2020-10-13) |
| G7 | **Journey** (thatgamecompany) | DICE 2013 Game of the Year (8 of 11) | starts from the emotion, then designs; no HUD, no words; music prototyped first with the composer | https://gamesbeat.com/an-interview-with-jenova-chen-how-journeys-creator-went-bankrupt-and-won-game-of-the-year/ (2013-02-09); https://www.polygon.com/2013/2/7/3965342/journey-and-the-search-for-emotional-gaming (2013-02-07); music-first detail from a fan blog of the GDC 2013 talk: https://journey-archive.fandom.com/wiki/User_blog:JAlbor/GDC_2013:_Designing_Journey_with_Jenova_Chen (secondary) |

## 1.4 The disability-empathy trap (must read before designing)

| # | finding | source |
|---|---|---|
| E1 | Silverman, Gwinn, Van Boven (2015): after a **blindness simulation**, participants judged blind people **less capable** of work and independent living than controls; simulators forecast they would adapt slowly. "Experience simulation can sometimes harm rather than help." | https://journals.sagepub.com/doi/10.1177/1948550614559650 (2015-05-01); APA summary https://www.apa.org/education-career/k12/infusing-diversity/social-personality/research-summary-blindness-simulation-empathy (n.d.) |
| E2 | Simulations "present disability in narrow, negative terms, emphasizing impairment-related deficits and dependence rather than the social, economic" barriers | https://link.springer.com/rwe/10.1007/978-3-031-40858-8_11-1 (n.d.) |
| E3 | "The Promise of Empathy: Design, Disability, and Knowing the Other" (CHI paper): empathy activities can "diminish disabled perspectives"; call for direct work with disabled people | https://creativetech.mat.ucsb.edu/readings/promise_of_empathy.pdf (2019-02-19) |
| E4 | Notes on Blindness (D2) worked because it is **John Hull's own voice**, not a simulation of blindness | D2 sources |

Design rules that come out of E1 to E4 (these drive Part 2):
1. The viewer never "becomes disabled". The viewer changes **where the camera stands**, not what the body can do.
2. The barrier is the street, not the person (social model). Every hard moment is caused by a measured object: 31 cm, a cart, a bike on the ramp.
3. The wheelchair user is the **expert** in the story (she already has the map in her head), never the patient.
4. Her words in first person. If possible tonight, a real wheelchair user at MUJ reads or approves her lines and is credited. If not possible, say so on the credits page.
5. The effort meter cannot be won (G6 logic): the lesson is "effort was never the problem", not "try harder".

## 1.5 India facts the story stands on

| fact | number | source |
|---|---|---|
| persons with disabilities, Census 2011 | 2.68 crore (26.8 M), 2.21% | https://www.mospi.gov.in/sites/default/files/publication_reports/Disabled_persons_in_India_2016.pdf (2017-01-10) |
| disability in movement | 54,36,826 (20.3%), largest single type | https://a11y.enabled.in/disabled-population-in-india-as-per-census-2011-2016-updated/ (2017-08-28); https://unstats.un.org/unsd/demographic-social/meetings/2016/bangkok--disability-measurement-and-statistics/Session-6/India.pdf (2016-08-05) |
| elderly 60+ | 103 M (2011) to 319 M by 2050 (19.5%) | https://iipsindia.ac.in/sites/default/files/LASI_India_Executive_Summary.pdf (2021-02-15) |
| elderly share | 10.5% (2022) to 20.8% (2050) | https://india.unfpa.org/sites/default/files/pub-pdf/20230926_india_ageing_report_2023_web_version_.pdf (2023-09-26) |
| elderly with mobility limits | 58% of 60+ have difficulty stooping/kneeling/crouching; next is climbing stairs without rest | LASI executive summary above |
| footpath height rule | max **150 mm** above carriageway (IRC:103-2012 and IRC:103-2022; BMC Universal Footpath Policy 2023 says the same) | http://law.resource.org.s3.amazonaws.com/pub/in/bis/irc/irc.gov.in.103.2012.pdf (2019-10-23); https://law.resource.org/pub/in/bis/irc/irc.gov.in.078.2.2020.pdf (2025-10-09); https://portal.mcgm.gov.in/irj/go/km/docs/documents/MCGM%20Department%20List/Roads%20and%20Traffic/Docs/Universal%20Footpath%20Policy%2026.05.2023/Circular%20Universal%20footpath%20policy%2026.pdf (2023-07-25) |
| ramps | 1:12 slope (UTTIPEC 2010, Delhi) | https://timesofindia.indiatimes.com/city/delhi/delhis-footpaths-too-high-to-be-used-violate-all-norms/articleshow/16328787.cms (2012-09-09) |
| Supreme Court | right to walk on footpaths declared a **fundamental right**, asks Centre for a law | https://www.thehindu.com/news/national/supreme-court-declares-the-right-to-walk-carefree-on-footpaths-a-fundamental-right/article71121451.ece (2026-06-19); https://www.bbc.com/news/articles/ce3e4enkrqro (2026-08-06) |
| this month | Mumbai Agarbazar seniors ask BMC for a slope: "There is neither a slope nor supporting road to get to the footpath" | https://www.mid-day.com/mumbai/mumbai-news/article/mumbai-senior-citizens-seek-footpath-slope-at-agarbazar-for-easier-access-to-market-23653351 (2026-10-05) |
| court on bollards | Bombay HC took up a Shivaji Park wheelchair user's grievance on bollards at footpath entrances | https://timesofindia.indiatimes.com/city/mumbai/hc-to-bmc-list-steps-taken-for-disabled-access-to-footpaths/articleshow/106529014.cms (2024-01-04) |
| Bengaluru | "Footpaths are either broken or suddenly disappear" (a wheelchair user near Coffee Board Junction) | https://www.thehindu.com/news/cities/bangalore/broken-and-inaccessible-bengalurus-footpaths-fail-persons-with-disabilities/article71202931.ece (2026-07-10) |
| curb-cut effect | Berkeley 1970s kerb ramps for wheelchairs then helped prams, trolleys, bikes, suitcases | https://ssir.org/articles/entry/the_curb_cut_effect (2016-11-17) |

Eye heights (for the camera rig):

| body | eye height | source |
|---|---|---|
| seated wheelchair user (adult) | 1090 to 1295 mm (ADA Fig A3); woman avg 1155 mm, man 1220 mm; UN manual 1.16 to 1.33 m | https://archive.ada.gov/descript/reg3a/figA3ds.htm (2013-05-17); https://www.firstinarchitecture.co.uk/metric-data-03-average-dimensions-of-wheelchair-user/ (2019-08-13); https://www.un.org/esa/socdev/enable/designm/AD5-02.htm (n.d.) |
| standing adult | UN manual 1.40 to 1.75 m; US sample means F 151.6 cm, M 163.4 cm (Indian adults are shorter on average, so I use 158 cm for Kabir; that number is my estimate) | UN manual above; https://multisite.eos.ncsu.edu/www-ergocenter-ncsu-edu/wp-content/uploads/sites/18/2016/06/Anthropometric-Detailed-Data-Tables.pdf (2006-12-08) |
| 3-year-old | 95 cm | Urban95 (D7) |
| cat | about 20 to 25 cm (UNVERIFIED, no source fetched; hermes used 22 cm) | none |
| myna on a wire | about 6 m (UNVERIFIED estimate) | none |

## 1.6 Techniques extracted (what makes a non-expert feel something in under 3 minutes)

| # | technique | seen in | how we use it |
|---|---|---|---|
| T1 | **Hook in the first 3 seconds with sound** | Utsubo guide; Santioni | open on black with sound recorded at 22 cm: tyres huge, chappals slapping, a horn the size of a building |
| T2 | **A gesture that costs something** (hold, drag, press) instead of free scroll | Santioni hold-to-advance; Why Zero hold-to-proceed | hold to open Billu's eye; drag to push the wheelchair; drag the clock |
| T3 | **Interaction carries the feeling, not text** | Florence; Journey; Gris | the push meter that cannot be won says "effort is not the problem" with no sentence |
| T4 | **An unwinnable moment** | That Dragon, Cancer | the 31 cm kerb: no amount of dragging gets Zoya up it |
| T5 | **Real voice, real recordings** | Notes on Blindness; despelote; That Dragon, Cancer | field-record one real Jaipur or MUJ street at 6 heights tonight (phone on the ground, on a lap, on a walker, in a hand, on a terrace) |
| T6 | **Positional / proximity audio** | despelote | the temple bell is faint from Kamla's house and full at the end |
| T7 | **Colour returns at the resolution** | Gris; Florence | B/W woodcut world; red only marks barriers; the fixed ramp gets the first saffron sunlight wash |
| T8 | **Non-human narrator who is neutral** | Stray; Bear 71; Little Kitty | Billu does not judge anyone; the vendor and the bike rider are not villains |
| T9 | **Map as a character's view** | Bear 71 grid | Gunjan the myna sees the route network; the map is her eyes, not a dashboard |
| T10 | **Several people, one place** | Life on Hold; Out My Window | the same 20 m of street, re-seen by 6 bodies |
| T11 | **Body height as a design lens** | Urban95 (95 cm) | the switch-body dial; each height reveals a different fact |
| T12 | **Per-chapter audio stems** | Awwwards 2026 sweep (rare, cheap) | one Web Audio stem per body, crossfaded on switch |
| T13 | **Loop or return** | IVRESS | the last frame is the first street, now with a ramp |
| T14 | **Short** | Utsubo ("2-3 minutes, not 10"; 5 scenes max for a linear arc) | 5 acts, 10 beats, 180 s; each beat under 25 s |
| T15 | **The device that blocks you becomes the tool** | Before Your Eyes (your own blink is both the input and the threat) | Kabir's phone hid the street from him; at the turn the same phone measures it |

---

# PART 2: PROPOSAL (design, not sourced)

## 2.1 Theme in one sentence

Everyone on this street holds one piece of the picture and nobody holds all of it. Billu knows the ground, Gunjan knows the network, Zoya knows the barriers, Kamla knows the hours, Kabir has the camera, Rekha has the budget. The app is the moment the pieces meet.

```
          GUNJAN (network)
               |
 KABIR (camera) --- [ THE APP ] --- REKHA (budget, action)
               |          |
   BILLU (cm)  |   ZOYA (barrier knowledge)
               |
          KAMLA (time, rest, shade)      PIHU + ARJUN (curb-cut: it helps everyone)
```

## 2.2 The cast

| who | eye height | what they see | what they feel | product module they carry | sound |
|---|---|---|---|---|---|
| **Billu**, one-eyed street cat, ginger, lives at the chai stall, sleeps on Zoya's lap | 22 cm | kerbs are cliffs, drains are canyons, every crack is a road; he squints his one eye when unsure | curious, unbothered, loyal; does not know he is brave | **the measuring stick**: kerb heights in "Billus" then in cm; his squint = ABSTAIN | low-passed world, tyres hiss at ear level, close paws on stone, purr = safety motif |
| **Gunjan**, a common myna on the electricity wire | ~600 cm (perched), higher in flight | the whole lane network: where it bends, where it breaks, which line reaches the temple | amused, gossipy; she copies every sound she hears | **routing + map + coverage** (known / unknown) | wind, wide stereo, she mimics sounds from below (auto horn, pressure cooker, "golgappe!") |
| **Zoya**, 26, QA engineer at a Jaipur startup, manual wheelchair since childhood, sharp and funny | 115 cm | kerbs as walls, castor-catching cracks, a bike parked on the only ramp; she reads a street in one glance | not sad, tired of explaining; proud of her map | **the barrier profile**: she already has 14 kerbs memorised between home and office; the app makes her private map public | push-rim tick, castor rattle that changes with surface (rough tile = rattle, smooth = hum), her own voice |
| **Kamla Devi**, 68, retired Hindi teacher (32 years), walker since a hip fracture | 140 cm (stooped) | distance to the next place to sit, shade, the time the footpath disappears under carts | quietly ashamed she stopped going to the temple 3 years ago; does not complain | **leave-time + rest stops + shade** | rubber tips of the walker (thunk, thunk), breath, a temple bell far away, a shop radio |
| **Kabir**, 21, B.Tech at MUJ, earbuds in, phone in hand | 158 cm, but his eyes are on the screen | almost nothing: everything outside the phone is blurred; he steps up a 31 cm kerb without noticing | nothing, then guilt, then purpose | **the camera / upload**: his phone hid the street; now it measures it | lo-fi beat in earbuds, everything else ducked under it, notification pings; when he pulls the earbuds out, the street floods in |
| **Pihu**, 3, in a pram pushed by her father **Arjun** | 95 cm (Urban95) | exhaust pipes, the backs of knees, dogs at eye level | delight | **curb-cut effect**: the ramp built for Zoya is the ramp Arjun needs | pram wheels, her giggle |
| **Rekha Meena**, Junior Engineer, ward office | desk | 4,000 footpaths on paper and no photos of any of them | not lazy, blind in her own way: she has no data | **the receipt + one-tap Hindi complaint** lands on her desk | ceiling fan, file stamp |
| **Shankar bhaiya**, golgappa cart, arrives at 5 pm | 150 cm | his only patch of shade | he needs the space too | **blockage-by-hour** (labelled assumption) | his call, which Gunjan copies |

Naming notes: names are common across regions and religions, no caste-coded surnames except Meena for the JE (a common Rajasthan surname; swap if the team prefers no surname). "Chhotu" and similar nicknames avoided (child-labour connotation).

## 2.3 Who we follow (decision tree, confidence 0-20)

```
Who carries the camera through 3 minutes?
|
+-- Billu the cat, riding on Zoya's lap .............. 16/20  RECOMMENDED
|     + can stand at every height (ground, lap, walker basket, wire next to Gunjan)
|     + neutral narrator (Stray, Bear 71), never judges the vendor or the rider
|     + avoids the simulation trap (E1): we follow a cat, not "be disabled"
|     + is the measuring stick (hermes's idea 2) and the ABSTAIN face (squint)
|     + cat-perspective work has proven pull (Stray TGA 2022, Little Kitty 2024)
|     + iconic image: a cat riding a wheelchair through Jaipur
|     - risk: cute can outweigh the stakes -> Zoya's voice owns the turn
|
+-- Zoya .............................................. 12/20
|     + the person this is for, highest stakes
|     - following her through hardship for 3 min drifts toward pity
|     - needs a real voice to be honest (E4); not sure we get one tonight
|
+-- Kabir ............................................. 11/20
|     + mirror of the judges (able-bodied, never noticed)
|     - centres the able-bodied hero; "saviour" reading
|
+-- Kamla (dsh's version) ............................. 10/20
|     + temple quest is warm, Hindi line is strong
|     - slow pace, one profile only, less to interact with
|
+-- Gunjan the myna .................................... 7/20
      - too far from the ground; no kerb, no stakes
```

Merge used: Billu is the camera and narrator, Zoya is the human stake, Kabir is the turn, Gunjan is the map, Kamla is the clock. This is the "possible merge (claude)" row from BRAINSTORM-SYNTHESIS-v1 grown to 6 bodies.

## 2.4 Same street, six renders ("switch body" interactable)

One reconstructed 20 m stretch of a real lane (AnySplat / Spark splat if built in under 2 h, else 2.5D layered woodcut panels; always labelled "reconstructed"). Switching body moves the camera and changes four things: height, focus, overlay, sound.

| body | camera y | lens / focus | what lights up (overlay) | palette | audio stem |
|---|---|---|---|---|---|
| Billu | 0.22 m | wide (cat sees wide), slight fish-eye, ground fills half the frame | kerb face labelled "31 cm = 1.4 Billus"; drain gap; ink texture on every crack | B/W, kerb edge in red | ground stem (recorded with the phone on the road) |
| Pihu | 0.95 m | normal | exhaust pipes at face height, a scooter tail-pipe smoking right at her mouth | B/W, smoke grey | pram stem |
| Zoya | 1.15 m | normal, sharp | kerb becomes a wall; the only ramp, with a bike parked on it; surface roughness lines | B/W, barriers red | lap stem (phone on a lap, wheels audible) |
| Kamla | 1.40 m | slight tilt down (stooped) | rest-stop halos (benches, steps, shop ledges), shade polygons from the shadow clock, 5 pm cart zones | B/W, shade as cross-hatch | walker stem |
| Kabir | 1.58 m | deep blur except the phone (BokehPass), notification pings pull the camera to the screen | nothing; one caption: "Kabir walks this street every day. He has never seen this kerb." | B/W washed out | earbud stem (street ducked under a beat) |
| Gunjan | 6 m, then top-down | orthographic tilt into a map | the route network; shortest line vs Zoya's line; known / unknown coverage | B/W map, routes in red ink | wire stem + mimicry |

Fallback if the 3D is not ready by the 23:00 gate: art lane B4 draws the same scene as 6 panels from one master layout so geometry matches; camera "switch" becomes a vertical wipe between panels plus parallax layers. Same overlays, same sound.

## 2.5 Beat sheet (5 acts, 10 beats, 180 s)

| # | time | act | beat | interactable | sound | product piece shown |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:12 | I WAKE | Black. Street sound at 22 cm. Caption: "Billu is 22 cm tall." | **hold** to open Billu's one eye (Santioni hold-to-advance) | ground stem rises with the hold | none |
| 2 | 0:12-0:30 | I | Billu's street: the kerb is a cliff. He jumps it. Caption: "This kerb is 1.4 Billus. 31 cm. The rule says 15." | **drag Billu up** to jump; on release the cm number inks in | jump thump, chai stall clatter | measuring (Billus to cm) |
| 3 | 0:30-0:55 | II HEIGHTS | Same street, other bodies. Ends on Kabir: blur, pings. "He has never seen this kerb." | **switch-body dial** (6 heads); each turn re-renders the street | stem crossfade per body | the reconstruction itself |
| 4 | 0:55-1:15 | II | Zoya rolls in, Billu asleep on her lap. Her voice: "Ghar se office tak 14 kerb hain. Mujhe sab yaad hain. Kisi map pe ek bhi nahi hai." ("14 kerbs from home to office. I remember all of them. Not one is on any map.") Her hand-drawn mental map draws itself. | hover / tap her map to see each remembered kerb | push-rim tick, castor rattle | the barrier profile |
| 5 | 1:15-1:30 | II | She tries this kerb anyway because the long way is +18 min. | **push meter**: drag to push; meter fills; the wheel never rises. Caption at full: "Effort was never the problem. 31 cm is." | strain, then silence | (none: the unwinnable beat, T4) |
| 6 | 1:30-1:50 | III CLOCK | Kamla at her door. Temple bell, faint. "Teen saal ho gaye mandir gaye." ("3 years since I went to the temple.") Drag the day forward: shadows swing, Shankar's cart rolls in at 5, a delivery bike parks on the ramp, Kamla's footpath disappears. | **leave-time slider** (10:00 to 21:00) + **rain toggle** (puddle hides an open drain; walker tip slips) | Gunjan copies "golgappe!"; rain stem | leave-time blockage (labelled "likely blocked 17:00-21:00, based on X") |
| 7 | 1:50-2:10 | IV TURN | Kabir pulls out his earbuds. The street floods in. He sees Zoya at the kerb and reaches to lift the chair. Zoya: **"Mujhe uthao mat. Raasta do."** All sound drops to Billu's purr. Kabir raises his phone, at the kerb this time. | **tap the shutter** (or the viewer uploads their own street: "your turn") | earbud stem cuts, full street, then silence, then shutter | upload any photo (live /analyze) |
| 8 | 2:10-2:30 | IV | The photo inks into woodcut. Three measuring lines (shadow, geometry, depth) slide in and meet: **31 cm +- 3, 3 of 3 agree**. A paper receipt prints. If a live upload is unsure, Billu squints: "Not sure. Needs a human look." | **upload**, then flip the receipt to see each field's source | thermal-printer chatter | the receipt + ABSTAIN shown honestly |
| 9 | 2:30-2:48 | V MAP | Gunjan lifts off; the street becomes her map. Three lines: shortest (hits 3 barriers), Zoya's (+6 min, 0 kerbs), Kamla's (2 rest stops, shade, leave before 4:30). Other photos from other cities blink in; grey = unknown, said plainly. | **what-if buttons** (rain, leave at 6, pram, crutches, baraat on the road, bike on the ramp, night photo, no photo at all) | wind, the city as one chord | routes per body + coverage map |
| 10 | 2:48-3:00 | V | Kamla dictates the complaint in Hindi; the app drafts it; she corrects one matra (she taught Hindi for 32 years). It lands on Rekha's desk with the receipt. Final frame, labelled "simulated": the same first street, now with a ramp, first colour in the whole piece (saffron sun). Billu asleep on the ramp. Arjun pushes Pihu up it. Kamla walks past, bell loud. Zoya rolls by without stopping. | **one-tap complaint**; then "Photograph your street" opens the full demo | bell full and near, purr | Hindi complaint + the full demo |

Pacing check: 10 beats in 180 s, average 18 s. Two silences (beat 5 end, beat 7). One unwinnable beat (5). One turn (7). Colour only once (10). Loop back to beat 2's street (T13).

## 2.6 Interactables, full list

| interactable | beat | why it is not decoration |
|---|---|---|
| hold to open the eye | 1 | costs attention (T2), sets the sound |
| drag Billu to jump | 2 | turns "31 cm" into a body feeling (cliff) before it is a number |
| switch-body dial | 3 (and in the demo) | the core idea: same street, six cities |
| tap Zoya's mental map | 4 | shows her expertise, not her impairment |
| push meter (cannot be won) | 5 | says "the street is the problem" without a sentence |
| leave-time slider | 6 (and in the demo) | the real gap vs normal maps: time-of-day blockage |
| rain toggle | 6 | Indian street reality: a puddle hides a drain |
| earbuds out / shutter | 7 | the turn, done by the viewer's own hand |
| upload a photo | 8 | live proof on any street; honest ABSTAIN |
| flip the receipt | 8 | "is this real?" answered per field (dsh's receipt idea) |
| what-if buttons | 9 | the 5 judge questions (JUDGE-LENS style) answered by running a case |
| one-tap Hindi complaint | 10 | the street gets fixed, not only described |

## 2.7 How the demo sits inside the story

- The story IS the product walk-through: each module is introduced by the character who owns that piece (table in 2.2), so the judge has met every feature before the free demo opens.
- The upload is diegetic: Kabir's phone in beat 7, then "your turn" hands the same phone to the viewer.
- The receipt is a story object (a paper slip), not a dashboard card.
- The map is Gunjan's eyes, not a separate screen.
- After beat 10 the "workbench" opens: profile picker = the cast's faces (Zoya = manual wheelchair, Kamla = walker, Arjun + Pihu = pram, plus crutches and low vision as plain profiles), leave-time slider, upload, what-if wall, complaint. Same ink style, so no break.
- Every generated or reconstructed frame carries its label ("simulated", "reconstructed"); every inferred blockage says "based on X".

## 2.8 Sound plan (tonight, practical)

1. Field-record one real lane (MUJ gate road or a Jaipur lane) for 2 minutes at each height: phone on the road (22 cm), on a bag at 95 cm, on a lap at 115 cm, held at 140 cm, at 158 cm with earbuds playing, and from a terrace (Gunjan). This is the despelote / Notes on Blindness move (T5) and nobody else at the event will have it.
2. Web Audio: one stem per body, crossfade on switch (T12); starts on the first hold (browsers block sound before a user gesture).
3. Motifs: Billu's purr (safety), temple bell (Kamla's goal, positional), push-rim tick (Zoya's rhythm; every barrier drops a tick), lo-fi earbud beat (Kabir's bubble).
4. Captions for every sound and line, on by default. A site about access must be accessible (W9, W10).

## 2.9 Guardrails (from 1.4)

| risk | guard |
|---|---|
| pity / inspiration framing | Zoya is funny, expert, busy; she is never shown crying; the turn line is a demand, not a plea |
| disability simulation | the viewer moves the camera, never "becomes" disabled; the push meter is the street's cost, labelled as such |
| villains | vendor and rider are not blamed; the slider shows a time pattern |
| invented authenticity | if no wheelchair user voices or approves Zoya's lines tonight, the credits say "written by the team, not yet reviewed by a wheelchair user" |
| precision lies | Billu's squint = ABSTAIN; error bars always shown; 31 cm in the story is a placeholder until the 3 ruler-measured campus kerbs exist |
| the site itself | captions, keyboard path through every beat, reduced-motion version (panels instead of camera moves), contrast checked |

## 2.10 The line each judge remembers

**Primary:** "Mujhe uthao mat. Raasta do." / "Don't lift me. Give me a way."
**Backup (the thesis, 3 bodies):** "Billu can jump it. Kabir never saw it. Zoya can't cross it."
**Closing card:** "One street. Six heights. Now one map."

Name ideas for the site (hypotheses, user picks): **Raasta Do**, **Ek Gali** ("one lane"), **Billu's Map**.

---

## 3. Claims check (red team of this file)

| claim | grade | note |
|---|---|---|
| Santioni SOTD 5 Oct 2026, Active Theory + plan8, hold-to-advance | VERIFIED (Awwwards page + Utsubo guide) | hold mechanic from Utsubo text, not from playing the site myself |
| Ponpon Mania SOTD 22 Oct 2025, SOTM Oct 2025 | VERIFIED | |
| Messenger = SOTY 2025 | UNVERIFIED (listing excerpt mixes rows; the Messenger link sits next to a "SOTY 2025" tag) | open https://www.awwwards.com/annual-awards-2025/ to confirm before saying it on stage |
| Igloo Inc SOTY 2024 | VERIFIED | |
| IVRESS awards | UNVERIFIED (self-reported by its maker) | |
| Cannes 2026 Digital Craft GP Project Genie | VERIFIED (canneslions.com 2026-06-23) | |
| Cannes 2025 Inclusive Design + Caption with Intention 2 GPs | VERIFIED | |
| despelote BAFTA 2026 Game Beyond Entertainment, IGF 2025 Audio | VERIFIED (bafta.org category page; IGF/NYU/Shacknews) | |
| Before Your Eyes BAFTA 2022 | VERIFIED (BAFTA press release) | |
| Stray TGA 2022 Best Indie | VERIFIED | |
| Gris TGA 2019 Games for Impact; That Dragon, Cancer TGA 2016 Games for Impact | VERIFIED | |
| Journey DICE 2013 GOTY | VERIFIED (GamesBeat) | "music first" is from a fan blog: UNVERIFIED |
| Florence awards | UNVERIFIED (not searched to a primary source; left out of the table on purpose) | |
| Notes on Blindness Peabody 2022, Prix Europa 2016 | VERIFIED (Arte page, Voices of VR) | |
| Silverman 2015 result | VERIFIED (SAGE abstract) | |
| "Promise of Empathy" authors | not named in this file because the search result did not show them | |
| Census, LASI, UNFPA numbers | VERIFIED (primary PDFs) | |
| IRC 150 mm | VERIFIED (IRC:103-2012 and 2022 text) | |
| SC fundamental-right ruling 19 Jun 2026 | VERIFIED headline (The Hindu) + BBC | bench and case name not fetched |
| wheelchair eye 1090-1295 mm | VERIFIED (ADA) | |
| cat 22 cm, myna 6 m, Kabir 158 cm | UNVERIFIED estimates | fine for art; do not put on a slide as fact |
| "31 cm kerb" | PLACEHOLDER, not a measurement | replace with a real ruler-measured campus kerb |
| "+18 min", "+6 min", "14 kerbs" | INVENTED story numbers | replace with real /route output before the demo |

## 4. Reasoning log (why these choices)

- Why the cat leads: the user named the cat first and asked to follow "the cat n the bird or anyone"; E1 says do not make the viewer play disabled; a cat on a lap gives every height without simulation.
- Why 6 bodies, not 4: each extra body earns its place only if it carries a product module (2.2). The vendor and the JE carry modules too but get no camera height, to keep the dial at 6.
- Why the turn line is in Hindi: the judges are in India; one Hindi line with an English caption reads as real; it doubles as the product promise (raasta = route).
- Why Kabir is not the hero: he only takes the photo; Zoya names what is needed and Kamla files the complaint.
- What I could not do: play Santioni, Messenger or Ponpon live (no browser pass in this lane). Mechanics come from Awwwards pages, the Utsubo guide and the 2026 sweep.
- Mistake caught: first draft had Florence's BAFTA as fact; removed because no primary source was fetched.
