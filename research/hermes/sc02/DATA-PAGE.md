# DATA-PAGE: what we use, what it costs us, what we can publish

hermes, 2026-10-25 02:05 IST, copy for /data. Every count below was read from disk tonight; where a count
differs from the brief I was given, I print what the files say and flag the difference rather than smoothing
it. Model licences are marked verified only where I read them; the rest say UNVERIFIED and must be checked
before the page publishes them.

## Datasets we hold

### Street imagery
**Three hundred twenty-seven images, seven sources**
Source: `data/online/MANIFEST.csv`, 328 lines including the header, counted by `source` tonight.

| source | images | what it is |
|---|---|---|
| commons (Wikimedia) | 94 | CC-licensed Indian street photos, mixed era, our main dry-day set |
| youtube | 84 | frames from walking-tour videos, standard YouTube licence |
| mapillary | 43 | street-level imagery under Mapillary terms |
| youtube-cc | 36 | frames from Creative Commons videos |
| mapillary-pairs | 32 | 16 same-place pairs, the same-spot-over-time set |
| panoramax | 20 | open street imagery with per-item licence links |
| youtube-storyboard | 18 | storyboard frames, used for scene reference rather than detection |

### The licence mix, which is the honest limit
**Eighty-four images we cannot redistribute**
Licence counts from the same manifest: 84 under the YouTube standard licence (demo use with attribution only),
43 Mapillary imagery, 36 Creative Commons Attribution, 32 Mapillary pairs, 25 CC BY-SA 3.0, 22 CC BY-SA 4.0,
20 Panoramax, 19 CC BY 3.0, and the rest split across smaller CC variants. That 84 is why the download section
below cannot simply say "here is our data".
Source: `data/online/MANIFEST.csv`, licence column.

### Our own labels
**One hundred labels, made with AI help**
`data/labels/c6-v1.jsonl` holds exactly 100 rows, and the C6 results file states plainly that they are team
labels made with AI assistance and still need one human pass. Per class positives are small: missing kerb ramp
4, steps 4, parked vehicle 8, pole obstruction 14, broken footpath 34, with 47 boxes on footpaths.
Source: `data/labels/c6-v1.jsonl` (100 lines), `eval/C6-RESULTS.md`.

### The one externally labelled city
**Chandigarh, from Project Sidewalk, CC0**
198 placements resolved in `app/site-data/chandigarh/barriers.json`, of which 155 are ACCEPT and 43 ABSTAIN,
built from Project Sidewalk's volunteer labels and coordinates. It is the only city where our map rests on
labels made by someone other than us, and it is the reason the map opens there when a judge asks for evidence.
Source: `app/site-data/chandigarh/barriers.json`; Project Sidewalk licence recorded as CC0 in `sources.json`
to confirm against their own licence page.

### Networks and maps
**Forty-five hundred to seven thousand segments per city**
Jaipur 4,537 (264 OSM-observed, 4,273 generated), jaipur-photos 4,704 (163 observed), chandigarh 7,047 (511
observed), varanasi 4,279 (114 observed). OSM data is ODbL 1.0, and generated segments are our own geometry
derived from it, drawn in their own style and never called mapped footpaths.
Source: `app/site-data/<city>/meta.json`, `by_source_kind` counts.

### Demographics
**Two census tables and one derivation**
Census 2011 Table C-13 (single-year ages) and Table C-20 (disability by type), at state and district level, plus
the all-India C-13 file. Jaipur district: 6,626,178 people, 455,130 aged 60 plus, 158,909 disabled, and our
derived elderly-or-disabled 575,503, labelled as arithmetic. The tables are public record.
Source: `research/hermes/sc02/raw/census/`, `CENSUS-JAIPUR.md`.

### Sound
**Sixteen cues from twenty-three Freesound sources**
`app/site/public/audio/v2/MANIFEST.json` defines 16 cues, each with its beat mapping, gain per beat, loop points
and variants, and it cites 23 Freesound sources found through the Openverse API: 18 under CC0 1.0, 4 under
CC BY 3.0, 1 under CC BY 4.0, every one with a source URL and a Freesound id. The earlier kit in
`app/site/public/audio/` is the old folder and is not what the story page loads; its 13-sound list was a
mistake in the first draft of this block and is corrected here.
Source: `app/site/public/audio/v2/MANIFEST.json`, counted tonight, 16 cues and 23 sources.

### Art
**Eleven approved renders, nine in the brief**
`art/out/v3` holds 7 scene PNGs plus 4 character PNGs, which is 11; the brief said 9 approved assets. I am
printing 11 and flagging the difference rather than picking whichever number is convenient.
Source: `art/out/v3/`, `art/out/v3/chars/`, counted tonight.

## Models we run

| model | role | licence, as far as I can verify | limit that matters |
|---|---|---|---|
| YOLOE-11s-seg | detector A, open-vocabulary segmentation | UNVERIFIED on the page tonight, needs the checkpoint licence read | prompt-driven, so a missing vocabulary word is a missing class |
| OWLv2 | detector B, second opinion | UNVERIFIED (model card to read) | over-fires on texture, which is why one class needed a calibrated rule |
| SegFormer-B0 | footpath versus carriageway context | UNVERIFIED (NVIDIA licence terms usually need checking) | trained abroad, calls some Indian paving "road" |
| Depth Anything V2 | monocular depth for height and distance | UNVERIFIED (small variants and large variants differ) | single view cannot separate height from tilt |
| mimo-v2.6-flash | vision describer over an API | proprietary, API only, key currently refused | cannot promote a detection, only demote |
| deepseek-v4.1-flash | text reasoner over an API | proprietary, API only, same key issue | advisory, cannot change status |

The honest note that belongs under the table: the two API models did not run at all tonight because the key
returned 401, so the page should say "vision check unavailable in this build" rather than implying they ran.

## What we can publish, and what we cannot

### Can publish
**Our labels, our networks, our matrix**
1. `c6-v1.jsonl`, 100 labels, with the AI-assistance caveat and the review queue.
2. The four city networks as GeoJSON, because the OSM-derived parts are ODbL and the generated parts are ours,
   with attribution and a clear note on which is which.
3. The impact matrix, 379 elements by 74 bodies by 5 contexts, as our own work, with the note that 52 elements
   name a source and the rest are assumptions.
4. The schema files (`raasta-receipt-v1`, the taxonomy counts) and the calibration policy.
5. The 43 Jaipur grievance rows as extracted facts with outlet, date and URL, not as our opinion.

### Cannot publish
**Third-party images keep their own licences**
1. The 84 YouTube-framed images and 18 storyboard frames: standard licence, not redistributable.
2. Mapillary and Panoramax imagery: usable in the demo under their terms, not ours to hand out.
3. Project Sidewalk's labels are CC0, so they can be republished, but with attribution to them and not as ours.
4. Census tables: public record, so citable, not something we "release".

### The line the page should carry
**We publish what we made, and link what we borrowed**
Download links point to our labels, our networks, our matrix and our schema, and every third-party row links to
the original instead of mirroring it. A data page that mirrors what it does not own is how a hackathon project
gets a takedown a week after it wins.
