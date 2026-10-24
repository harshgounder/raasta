# RAASTA story sound plan v2 (2026-10-25)

Replaces the v1 synth sounds. Every file in this folder is a cut from a real recording (Freesound, found through the Openverse API, all licences re-checked on the live Freesound pages on 2026-10-25). No synthesis, no voice (subtitles only, per the user at 19:5x). The page code is not touched here: the story builder reads `MANIFEST.json`.

Rules carried over from `story/STORY-v2.md`, `~/site-clones/santioni/art/SOUND-BIBLE.md` and `story/SANTIONI-MOTION-FINE.md`:
- beds loop for the whole visit and only their gains move with scroll progress
- footsteps follow the walk: one paw sample per walk-cycle contact, round robin, never the same file twice in a row
- ONE loud hit on the whole page: `horn_hit`, beat 4, at the turn. Nothing else gets near it (measured in the preview: 1 s RMS -13 dB at the horn, next loudest -17 dB)
- nothing plays before the user's sound-on click

## Files and levels (measured on the shipped files)

| cue | stems | loop | file LUFS | true peak dBTP | default gain |
|---|---|---|---|---|---|
| indian_street_morning_bed | street_morning_bed | yes, 44.97 s, seam -26 dB (clean) | -22.0 | -6.2 | 0.8 |
| market_bed | market_bed | yes, 44.97 s, seam -10 dB | -22.0 | -2.1 | 0.45 |
| wind_high_bed | wind_high_bed | yes, 36.97 s, seam -13 dB | -22.0 | -7.3 | 0.85 in lifts |
| temple_bell | temple_bell_1, temple_bell_2 | no | -18 | -3.8 / -4.4 | 0.28 / 0.55 |
| cat_paws | cat_paw_1..6 (0.13 s each) | no | -23 to -26 (peak-limited) | <= -1.7 | 0.36 |
| cat_purr | cat_purr (9 s) | no | -18 | -2.0 | 0.22 |
| myna_call | myna_call_1, myna_call_2 | no | -18 | -8 | 0.3 |
| wingbeats | wingbeats_1, wingbeats_2 | no | -19 | -1.8 | 0.5 |
| scooter_passby | scooter_passby_1 (15 s), _2 (10 s) | no | -18 | -3.0 / -1.7 | 0.75 |
| horn_hit | horn_hit (2.6 s, two honks) | no | -14 | -3.1 | 1.0 |
| walker_taps | walker_tap_1..4 | no | -18 to -20 | -1.8 | 0.5 |
| young_steps | young_steps_quick (6 s) | no | -18 | -1.8 | 0.55 |
| cane_and_steps | cane_tap_1, cane_tap_2, cane_steps_old, kid_steps | no | -22 to -23 (taps, peak-limited), kid -19 | <= -1.8 | 0.45 |
| wheelchair_roll | wheelchair_roll (8.5 s) | no | -19 | -1.8 | 0.55 |
| phone_tap | phone_tap_1, _2 (click), _3 (soft thump) | no | -19 | -1.6 to -2.1 | 0.55 |
| ending_resolve | ending_resolve (24 s real tanpura drone, 6 s fade in, 8 s fade out) | no | -20 | -8.9 | 0.75 |

Very short clips (paws 0.13 s, cane taps 0.21 s) cannot reach -18 LUFS without clipping, so they sit at -22 to -26 with peaks at about -2 dBTP. That is by design: a paw should never be loud.

Loops: set `loopEnd = loopEndSeconds` from the manifest for both formats. The `.m4a` beds carry 2048 extra wrap-around samples so AAC priming cannot open a gap; the `.ogg` beds are exact. One-shot `.m4a` files start with 1024 samples (21 ms) of silence for the same reason (ffmpeg drops the first AAC frame on decode; checked: ogg and m4a line up at lag 0 after the fix).

## Per beat (progress = 0 at the beat's first scroll pixel, 1 at its last)

| beat | what happens | cue | in -> out (progress) | gain | notes |
|---|---|---|---|---|---|
| 0 title | dawn, Billu wakes, stretches, jumps down | wind_high_bed | 0 -> 1 | 0 -> 0.55 by 0.3, then down to 0.35 | first sound after the click, 1.2 s fade-in |
| | | indian_street_morning_bed | 0.3 -> 1 | 0 -> 0.35 | city waking up underneath |
| | | temple_bell_1 | one-shot at 0.25 | 0.28 | distant |
| | | cat_purr | one-shot at 0.4 (wake) | 0.22 | |
| | | cat_paws | 2 hits at the jump-down landing (about 0.9) | 0.5, 0.42 | |
| 1 the cat's street | 22 cm behind Billu, walking past the obstacles | indian_street_morning_bed | 0 -> 1 | 0.85 | |
| | | wind_high_bed | 0 -> 0.2 | 0.35 -> 0.12 | |
| | | cat_paws | each walk-cycle contact while the walk scrubs | 0.36 to 0.42, round robin | stop when the walk stops |
| | | myna_call_1 | one-shot at about 0.2 | 0.35 | Gunjan nearby |
| | | scooter_passby_1 | start when the speeding scooter enters, peak about 7 s in | 0.75 | brief says "one horn" here; kept OUT so beat 4 stays the only loud hit |
| 2 bird lift 1 | Gunjan rises, top view dungeon map | wingbeats_1 | one-shot at 0 | 0.5 | |
| | | wind_high_bed | 0 -> 0.3 rises, holds to 0.85, falls by 1 | 0.12 -> 0.9 -> 0.1 | |
| | | indian_street_morning_bed | ducks | 0.85 -> 0.25 -> back to 0.85 at 1 | the city drops away below |
| | | myna_call_2 | one-shot at about 0.5 | 0.3 | |
| 3 the young guy | Kabir steps over everything with ease, Billu sits | young_steps_quick | 0.1 -> 0.9 | 0.55 | no paws (cat sits); earbud music NOT made (no cue asked for it, see open items) |
| | | indian_street_morning_bed | 0 -> 1 | 0.85 | |
| 4 the old woman | Kamla: kerb, cart, then the scooter honks, she turns back | market_bed | 0 -> 0.2 fades in (the vendor cart) | 0 -> 0.5 | |
| | | walker_taps | one per walker placement, about every 1.6 s of her walk | 0.5, round robin | |
| | | horn_hit | ONE shot at the turn (about 0.6) | 1.0 | never retrigger on scroll back and forth: latch it per visit, or allow again only after the reader leaves beat 4 |
| | | walker_tap_4 | one more after the horn (she turns) | 0.4 | |
| 5 the old man and the kid | Dadaji, grandkid, "isse kuch nahi hoga", he opens RAASTA | cane_steps_old | at 0 | 0.7 | |
| | | kid_steps | at 0.1 | 0.45 | |
| | | cane_tap_1 | at about 0.4 | 0.45 | |
| | | phone_tap_3 then phone_tap_1 (+0.45 s) | when the red phone screen appears (about 0.65) | 0.55, 0.5 | the RAASTA moment |
| | | market_bed | 0 -> 0.3 fades | 0.5 -> 0.15 | |
| 6 bird lift 2 | top view, red route around every trap | wingbeats_2 | at 0 | 0.5 | |
| | | wind_high_bed | same shape as beat 2 | 0.1 -> 0.9 -> 0.1 | |
| | | indian_street_morning_bed | ducks | 0.8 -> 0.25 -> 0.75 | |
| | | ending_resolve | starts at about 0.3 | 0.18 | the first faint hint of the score |
| 7 the walk with RAASTA | Billu trots behind them, Zoya passes in her wheelchair | cat_paws | walk-cycle contacts | 0.32 | |
| | | cane_tap_1 / cane_tap_2 alternating | about every 1.15 s of their walk | 0.38 | |
| | | kid_steps | at 0.1 | 0.35 | |
| | | wheelchair_roll | when Zoya enters frame (about 0.2) | 0.55 | |
| | | myna_call_1 | about 0.6 | 0.25 | "birds" in the brief |
| | | market_bed | 0 -> 1 | 0.3 | quieter, the carts are not here yet |
| 8 arrival + tagline | temple / park, "Kuch nahi hua!", colour arrives, final crane up | ending_resolve | from 0 (6 s fade in built into the file) | 0.75 | real tanpura, the swell |
| | | temple_bell_2 | at about 0.1 | 0.55 | |
| | | wind_high_bed | rises with the crane up (0.5 -> 1) | 0.15 -> 0.5 | |
| | | indian_street_morning_bed, market_bed | fade out by 1 | 0.6 -> 0, 0.2 -> 0 | |
| 9 CTA | tear wipe | (none from this set) | | | v1 `tear` exists in `../` |

## Preview mix

`preview-mix.ogg` / `.m4a`: 62 s, beats 0 to 8 in order at these times: 0 title (0-6 s), 1 street (6-16), 2 lift (16-21), 3 Kabir (21-27), 4 Kamla + horn at 31.9 s (27-35), 5 Dadaji + phone at 39 s (35-41), 6 lift 2 (41-47), 7 walk + Zoya (47-54), 8 arrival (54-62). Mastered to -18 LUFS / -1.5 dBTP; the shipped .ogg measures -18.3 LUFS, -1.2 dBTP. Loudest seconds: 33 s (horn) -13.3 dB RMS, then 16 s (wings) -16.5. Exact timeline and gains: `_scripts/mix.py`.

## Rebuild

`_scripts/` (needs ffmpeg + numpy, run with `python3 -I`): `search.py` (Openverse queries -> cands.json), `fetch.py` (downloads the picks, writes sources.json), `build.py <outdir>` (cuts, loops, normalises, encodes), `mix.py <dir>` (preview), `manifest.py <dir>`, `scan.py` / `events.py` (analysis). Working copies and the downloaded sources live in the session scratchpad, not here.

## Open items

1. Nobody has listened yet. The cuts were chosen from loudness profiles, onset detection and spectrograms, not by ear. The user should play `preview-mix.ogg` first.
2. Cat paws are from an animal-claw foley recording (CC0), low-passed at 5 kHz; a real cat walking clip (Augdog, CC BY 4.0) was tried first and dropped because its noise floor turned to hiss at the needed gain.
3. The walker recording is a Zimmer frame on a wooden floor (indoor), not on a footpath.
4. The market bed source mentions horn honks and the street bed mentions rickshaws passing; the loop windows were picked as the calmest stretches (level spread under 4 to 9 dB) but a distant honk inside a bed is possible.
5. Earbud music for Kabir (beat 3 in STORY-v2) was not made: no CC0/CC-BY track was picked in the time box.
6. Sources are Freesound "hq" mp3 previews (128 kbps), not the original wav/flac, because there is no Freesound API key on disk (`apikeys.txt` has none). Re-cutting from originals later would raise quality a little.
