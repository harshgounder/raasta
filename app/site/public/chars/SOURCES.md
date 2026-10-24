# character sources (provenance)

| what | source | licence | how we use it |
|---|---|---|---|
| body | MPFB 2 (Blender extension, build 20260722) generated human | CC0 (MPFB generated humans) | `build_mapmaker.py` builds it; committed as `lab/public/chars/mapmaker(.min).glb` |
| walk clip `Walk_Loop` | Quaternius, Universal Animation Library, Standard 1.0 (files dated 2025-03), downloaded 2026-10-10 from https://store.godotengine.org/asset/quaternius/universal-animation-library/download/44/ | CC0 1.0 (License.txt inside the zip, kept as `sources/quaternius-ual-LICENSE.txt`; pack page https://quaternius.com/packs/universalanimationlibrary.html says CC0) | retargeted onto our rig (`retarget.py`, Rigify `DEF-*` -> our Mixamo names), only the baked result ships: `lab/public/chars/mapmaker-walk(.min).glb` |
| robe (default outfit since 2026-10-11) | MakeHuman community "Monk's robe" by Donitz (2022-12-28), http://www.makehumancommunity.org/clothes/monks_robe.html, files Monks_Robe.mhclo + .obj, downloaded 2026-10-11 | CC0 (page: "License: CC0 - Creative Commons Zero"; file header: "license: CC0") | fitted by MPFB (`HumanService.add_mhclo_asset`), hem flared below the knee (MM_FLARE 0.30), pleats softened (MM_ROBE_SMOOTH 8), re-weighted by dress.py `_skin` (skirt 65% to the hips), baked into the shipped glbs |
| hood (raised) | MakeHuman community "Monk's robe hood" by Donitz (2022-12-28), http://www.makehumancommunity.org/clothes/monks_robe_hood.html, Monks_Hood.mhclo + .obj | CC0 (file header: "license: CC0"; the sibling "hood down" page states CC0) | fitted by MPFB, re-weighted by `_skin`; no hat over a raised hood (MM_HOOD=off adds Monks_Hood_Off + the scripted hat) |
| (local test only) Xbot walk | three.js r186 examples (Mixamo-derived) | Mixamo terms: never redistributed | `mapmaker-walk.local*.glb`, git-ignored |

robe/hood sha256 (sources/monks_robe, git-ignored): Monks_Robe.mhclo `7f0cf2903c602bd817e8a3a38d4b6201313ab0c156702f9dcc3e440897b0a4c8`, Monks_Robe.obj `12ab7c180f724c1a50d3b2217d0d37ef03758ed387e22abb3933fe93269b90cc`, Monks_Hood.mhclo `5f32a69d26f68b9c5dd9076e9b6859c154291759726831def4bc5c7afc315aa7`, Monks_Hood.obj `989f2632ccce50d4cf99973167ecc10e6f33911a60e8e378d50d8b30d06306fc`, Monks_Hood_Off.mhclo `035a513374941e5675ad17138c51e4be52847c4a291c22436d2ba997279c9ca5`, Monks_Hood_Off.obj `d65fb26b6af91a26227796fdf7265efebacffb7883ac810272c9245549856336`. textures not used (the woodcut shader needs none).

build knobs (env, defaults = what ships): MM_OUTFIT robe|coat, MM_HOOD up|off|none, MM_HAT (0 with a raised hood), MM_FLARE 0.30, MM_HIPS_BLEND 0.65, MM_ROBE_SMOOTH 8, MM_AO_DIST 0.1 (m; Blender's default 10 m made the robe 67% coarse in the figure gate), MM_BAKE 1.

source file sha256: `1b7bf67866360665426bb99e4c71bd619f19b408453c24e30f0c3071601eee5c` (`sources/quaternius-ual-standard.glb`, git-ignored, re-download from the link above).

licence watch: quaternius.com published its own "Quaternius Asset License (QAL) v1.0" on 2026-08-28 (free, commercial, no credit, but no redistribution of the assets as a template or asset pack). it is not retroactive and the Universal Animation Library pages still state CC0 (checked 2026-10-10). we ship only the retargeted bake on our own character, never the library file.

newer build exists: the itch.io release is v3.0 (2026-06-16: root motion versions, 8-direction clips start on the left foot, new rig names). its free download needs the itch "no thanks" popup, which the headless script could not drive; the Godot store Standard 1.0 was used. switch when a v3 download is in hand (WALK_MAP may need new names).

rebuild:
```
cd art/character
WALK_MAP=rigify WALK_ACTION=Walk_Loop blender -b --factory-startup --python build_mapmaker.py -- ../../lab/public/chars/mapmaker-walk.glb sources/quaternius-ual-standard.glb
blender -b --factory-startup --python build_mapmaker.py -- ../../lab/public/chars/mapmaker.glb   # bare body, no walk
cd ../../lab; npx gltf-transform optimize public/chars/mapmaker-walk.glb public/chars/mapmaker-walk.min.glb --compress meshopt --texture-compress false --simplify false
```
