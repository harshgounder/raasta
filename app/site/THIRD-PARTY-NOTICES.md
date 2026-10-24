# third-party notices (hypnexis SC-02 site; copied from the santioni kit and extended 2026-10-24)

everything the kit ships or bundles that we did not write, with its licence. provenance details for the character
are in `art/character/SOURCES.md`; tools that only produce files (Blender, MPFB, audio-as-code, Kokoro, Codex) are
listed there and in `art/SOUND-BIBLE.md`, they are not shipped.

| what | where it is used | licence | notice |
|---|---|---|---|
| three.js r186 (incl. the GLTFLoader addon) | bundled into every build | MIT | `Copyright © 2010-2026 three.js authors`, full text in `node_modules/three/LICENSE` |
| meshoptimizer decoder (shipped inside three's addons) | decodes `*.min.glb` | MIT | `Copyright (C) 2016-2026, by Arseny Kapoulkine`, header of `three/examples/jsm/libs/meshopt_decoder.module.js` |
| three-pinata 2.0.1 (Daniel Greenheck) | Voronoi fracture for the crumble (`lab/src/look/crumble.js`), bundled | MIT | full text in `node_modules/@dgreenheck/three-pinata/LICENSE` |
| "Hash without Sine" `hash12` (Dave Hoskins, https://www.shadertoy.com/view/4djSRW) | `lab/src/look/hatch.js`, `hatch-tsl.js`, `panel.js` | MIT | below |
| Gloock (display face) | `public/fonts/Gloock-Regular.latin.woff2` | SIL OFL 1.1 | `public/fonts/OFL-Gloock.txt` |
| M PLUS Rounded 1c (UI face) | `public/fonts/MPLUSRounded1c-*.woff2` | SIL OFL 1.1 | `public/fonts/OFL.txt` (Copyright 2016 The Rounded M+ Project Authors) |
| MPFB 2 generated body | `public/chars/mapmaker*.glb` | CC0 | none required |
| MakeHuman community "Monk's robe" + "Monk's robe hood" (Donitz) | fitted into `public/chars/mapmaker*.glb` | CC0 | none required (`art/character/SOURCES.md`) |
| MapLibre GL JS 6.15.0 (incl. its worker) | the map pages, bundled | BSD-3-Clause | full text in `node_modules/maplibre-gl/LICENSE.txt` |
| deck.gl 9.4.0 (@deck.gl/core, layers, geo-layers, extensions, mapbox) | routes, barriers, route animation, bundled | MIT | `node_modules/@deck.gl/core/LICENSE` |
| Baloo 2 (Devanagari 700, 800) | `public/fonts/Baloo2-Devanagari-*.woff2` (Hindi text) | SIL OFL 1.1 | `public/fonts/OFL-Baloo2.txt` |
| OpenStreetMap data (via the routing lane) | `app/site-data/*/network.geojson` | ODbL 1.0 | attribution on the map and /data |
| Project Sidewalk Chandigarh labels (via the routing lane) | barrier records | CC0 1.0 (per the routing lane's meta.json) | /data |
| Quaternius Universal Animation Library `Walk_Loop` (retargeted, baked) | `public/chars/mapmaker-walk*.glb` | CC0 1.0 | none required (`art/character/SOURCES.md`) |

our own (no third-party code): the blue-noise texture (`tools/bluenoise.py`, void-and-cluster), every shader other
than the hash above, the sound files (audio-as-code stems + numpy synthesis, Kokoro voice) and all art.

## MIT licence text for "Hash without Sine"

```
MIT License
Copyright (c) 2014 David Hoskins.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## Story sound v2 (`public/audio/v2/`, added 2026-10-25)

Real field and foley recordings from Freesound (found through the Openverse audio API), trimmed, faded, looped and loudness-normalised by us (`public/audio/v2/_scripts/`). These replace the synthesized v1 story sounds for the RAASTA story page; the line above about our own sound files covers v1 only. CC BY sounds need the credit line below wherever the credits are shown. Full per-file data: `public/audio/v2/MANIFEST.json`.

| sound (Freesound id) | author | licence | used as | link |
|---|---|---|---|---|
| "Cane_Hitting_Pavement_3.wav" (138295) | Tdude9000 | CC BY 3.0 | `cane_tap_2` | https://freesound.org/people/Tdude9000/sounds/138295 |
| "Cane_Hitting_Pavement_2.wav" (138296) | Tdude9000 | CC BY 3.0 | `cane_tap_1` | https://freesound.org/people/Tdude9000/sounds/138296 |
| "Footsteps_Cane_hitting_Pavement.wav" (138328) | Tdude9000 | CC BY 3.0 | `cane_steps_old` | https://freesound.org/people/Tdude9000/sounds/138328 |
| "Steps of a Child in Grass.wav" (634986) | JiggleSticks | CC BY 4.0 | `kid_steps` | https://freesound.org/people/JiggleSticks/sounds/634986 |
| "SonicSnaps-IDES-FR-wheelchair.wav" (174603) | thecityrings | CC BY 3.0 | `wheelchair_roll` | https://freesound.org/people/thecityrings/sounds/174603 |
| "2HinduTemplesBells1.wav" (271626) | LoopUdu | CC0 1.0 | `temple_bell_1` | https://freesound.org/people/LoopUdu/sounds/271626 |
| "2HinduTemplesBells2.wav" (271627) | LoopUdu | CC0 1.0 | `temple_bell_2` | https://freesound.org/people/LoopUdu/sounds/271627 |
| "Footsteps_Quick.wav" (368833) | georgisound | CC0 1.0 | `young_steps_quick` | https://freesound.org/people/georgisound/sounds/368833 |
| "auto horn honk real annoyed close India.flac" (451318) | kyles | CC0 1.0 | `horn_hit` | https://freesound.org/people/kyles/sounds/451318 |
| "crowd ext medium busy street downtown market movement steps throaty traffic motorcycles rickshaws horn honks India.flac" (451351) | kyles | CC0 1.0 | `market_bed` | https://freesound.org/people/kyles/sounds/451351 |
| "Crowd of Myna birds.mp3" (338173) | edranil | CC0 1.0 | `myna_call_1`, `myna_call_2` | https://freesound.org/people/edranil/sounds/338173 |
| "Claws animal (foley)" (569255) | Nakhas | CC0 1.0 | `cat_paw_1`, `cat_paw_2`, `cat_paw_3`, `cat_paw_4`, `cat_paw_5`, `cat_paw_6` | https://freesound.org/people/Nakhas/sounds/569255 |
| "Smart Phone Click" (444683) | AO-SoundPawz | CC0 1.0 | `phone_tap_1`, `phone_tap_2` | https://freesound.org/people/AO-SoundPawz/sounds/444683 |
| "Screen tap" (536315) | EilasSFX | CC0 1.0 | `phone_tap_3` | https://freesound.org/people/EilasSFX/sounds/536315 |
| "Cat Purring (long/clear/loud)" (579898) | JamesBradford | CC0 1.0 | `cat_purr` | https://freesound.org/people/JamesBradford/sounds/579898 |
| "Tanpura 10" (153262) | sankalp | CC0 1.0 | `ending_resolve` | https://freesound.org/people/sankalp/sounds/153262 |
| "scooter pass by medium speed echo off building.flac" (450698) | kyles | CC0 1.0 | `scooter_passby_1` | https://freesound.org/people/kyles/sounds/450698 |
| "moped pass by.wav" (523959) | lartti | CC0 1.0 | `scooter_passby_2` | https://freesound.org/people/lartti/sounds/523959 |
| "street quiet morning alley corner nearby throaty traffic motorcycles rickshaws pass boomy crows and rooster close by India.flac" (451488) | kyles | CC0 1.0 | `street_morning_bed` | https://freesound.org/people/kyles/sounds/451488 |
| "Zimmer Walker Frame on wooden floor" (540712) | tuesdayblack | CC0 1.0 | `walker_tap_1`, `walker_tap_2`, `walker_tap_3`, `walker_tap_4` | https://freesound.org/people/tuesdayblack/sounds/540712 |
| "Looping Gentle Wind Ambience on an Open Desert Plain.wav" (697217) | dhallcomposer | CC0 1.0 | `wind_high_bed` | https://freesound.org/people/dhallcomposer/sounds/697217 |
| "birds taking off to fly.mp3" (499570) | Hope-Sounds | CC0 1.0 | `wingbeats_2` | https://freesound.org/people/Hope-Sounds/sounds/499570 |
| "Pigeons flying" (532180) | mcmikai | CC0 1.0 | `wingbeats_1` | https://freesound.org/people/mcmikai/sounds/532180 |

Credit line (CC BY items): "Cane_Hitting_Pavement_3.wav" by Tdude9000 (https://freesound.org/people/Tdude9000/sounds/138295), CC BY 3.0, trimmed and levelled; "Cane_Hitting_Pavement_2.wav" by Tdude9000 (https://freesound.org/people/Tdude9000/sounds/138296), CC BY 3.0, trimmed and levelled; "Footsteps_Cane_hitting_Pavement.wav" by Tdude9000 (https://freesound.org/people/Tdude9000/sounds/138328), CC BY 3.0, trimmed and levelled; "Steps of a Child in Grass.wav" by JiggleSticks (https://freesound.org/people/JiggleSticks/sounds/634986), CC BY 4.0, trimmed and levelled; "SonicSnaps-IDES-FR-wheelchair.wav" by thecityrings (https://freesound.org/people/thecityrings/sounds/174603), CC BY 3.0, trimmed and levelled.
