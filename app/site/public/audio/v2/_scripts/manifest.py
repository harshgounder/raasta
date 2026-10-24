"""write MANIFEST.json for audio/v2 from sources.json + build-report.json. usage: manifest.py <audio_v2_dir>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import decode, SR
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = sys.argv[1]
SRC = json.load(open(os.path.join(BASE, "sources.json")))
REP = json.load(open(os.path.join(BASE, "build-report.json")))
LIC = {("cc0", "1.0"): ("CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
       ("by", "3.0"): ("CC BY 3.0", "https://creativecommons.org/licenses/by/3.0/"),
       ("by", "4.0"): ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/")}
# cue: (beats, bus, loop, default linear gain, per-beat gain notes, trigger)
CUES = {
 "indian_street_morning_bed": ([0, 1, 3, 4, 5, 7, 8], "ambience", True, 0.8, {"0": 0.35, "1": 0.85, "2": 0.25, "3": 0.85, "4": 0.8, "5": 0.8, "6": 0.25, "7": 0.75, "8": 0.6}, "loop for the whole story; ride gain by beat; duck to 0.25 during bird lifts"),
 "market_bed": ([4, 5, 7], "ambience", True, 0.45, {"4": 0.5, "5": 0.15, "7": 0.3, "8": 0.2}, "loop; fades in as the vendor cart enters (beat 4)"),
 "wind_high_bed": ([0, 2, 6, 8], "ambience", True, 0.85, {"0": 0.55, "1": 0.12, "2": 0.9, "6": 0.9, "8": 0.5}, "loop; rises with each bird lift (beats 2, 6) and the final crane up (8)"),
 "temple_bell": ([0, 8], "sfx", False, 0.45, {"0": 0.28, "8": 0.55}, "beat 0: distant, once near the start; beat 8: on arrival"),
 "cat_paws": ([0, 1, 7], "sfx", False, 0.36, {}, "round robin, never the same file twice in a row; one paw per walk-cycle contact of Billu (about every 0.34 s of walk); stop when the cat sits (beat 3)"),
 "cat_purr": ([0, 3], "sfx", False, 0.22, {}, "beat 0 when Billu wakes on the scooter seat; optional in beat 3 when he sits to watch"),
 "myna_call": ([1, 2, 7], "sfx", False, 0.3, {}, "Gunjan; once per beat, round robin"),
 "wingbeats": ([2, 6, 8], "sfx", False, 0.5, {}, "on each bird lift start (beat 2 variant 1, beat 6 variant 2, beat 8 crane up either)"),
 "scooter_passby": ([1], "sfx", False, 0.75, {}, "beat 1, the scooter speeding past close; variant 2 spare (beat 4 lead-in at 0.4 if wanted)"),
 "horn_hit": ([4], "sfx", False, 1.0, {}, "THE one loud hit of the whole page: beat 4 when the scooter honks at Kamla (the turn); never anywhere else"),
 "walker_taps": ([4], "sfx", False, 0.5, {}, "Kamla's walker frame, one tap per walker placement (about every 1.6 s of her walk), round robin"),
 "young_steps": ([3], "sfx", False, 0.55, {}, "Kabir's quick easy steps (one 6 s pass)"),
 "cane_and_steps": ([5, 7], "sfx", False, 0.45, {}, "Dadaji + the kid: cane_steps_old at beat 5 start; cane_tap_1/2 alternate about every 1.15 s of their walk in beat 7; kid_steps under it at 0.35-0.45"),
 "wheelchair_roll": ([7], "sfx", False, 0.55, {}, "Zoya's cameo passing on the same route (beat 7)"),
 "phone_tap": ([5], "ui", False, 0.55, {}, "the RAASTA moment: Dadaji opens the app (phone_tap_3 then phone_tap_1 about 0.45 s later)"),
 "ending_resolve": ([6, 8], "music", False, 0.75, {"6": 0.18, "8": 0.75}, "real tanpura drone (no synth); beat 6 a faint hint, beat 8 the swell as colour arrives"),
}
CUE_OF = {}
for stem, r in REP.items():
    c = r["cue"]
    if stem == "young_steps_quick":
        c = "young_steps"
    CUE_OF.setdefault(c, []).append(stem)
out = {"version": 2, "generated": "2026-10-25", "note": "real field recordings only (Freesound via the Openverse API), no synthesis. LUFS = integrated loudness of the shipped file (short clips padded to 1.2 s before measuring). gain = suggested linear playback gain; beatGain overrides it per beat.", "formats": ["ogg", "m4a"], "cues": []}
for cue, (beats, bus, loop, gain, bg, trig) in CUES.items():
    stems = CUE_OF.get(cue, [])
    srcs, seen = [], set()
    variants = []
    for s in stems:
        r = REP[s]; src = SRC[r["src"]]
        variants.append({"stem": s, "files": [s + ".ogg", s + ".m4a"], "seconds": r["dur"], "lufs": r["lufs"], "truePeak": r["true_peak"], "seamDb": r["seam_db"], "from": {"freesoundId": src["freesound_id"], "start": r["start"]}})
        if r["loop"]:
            n = len(decode(os.path.join(D, s + ".ogg")))
            variants[-1]["loopEndSeconds"] = n / SR
            variants[-1]["loopNote"] = "set AudioBufferSourceNode.loopEnd = loopEndSeconds (loopStart 0) for BOTH formats: the .m4a carries 2048 extra wrap-around samples so AAC priming never opens a gap"
        if r["src"] not in seen:
            seen.add(r["src"])
            name, url = LIC[(src["license"], src["license_version"])]
            srcs.append({"title": src["title"], "author": src["creator"], "licence": name, "licenceUrl": url, "sourceUrl": src["landing"], "fileUrl": src["url"], "freesoundId": src["freesound_id"], "foundVia": "Openverse API (api.openverse.org) index of Freesound"})
    out["cues"].append({"cue": cue, "beats": beats, "bus": bus, "loop": loop, "gain": gain, "beatGain": bg, "roundRobin": len(variants) > 1 and not loop, "trigger": trig, "variants": variants, "sources": srcs})
out["preview"] = {"files": ["preview-mix.ogg", "preview-mix.m4a"], "seconds": 62.0, "what": "beats 0-8 in order, compressed to 62 s, for judging; not used by the page"}
json.dump(out, open(os.path.join(D, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print(len(out["cues"]), "cues", sum(len(c["variants"]) for c in out["cues"]), "files")
for c in out["cues"]:
    print(c["cue"], [v["stem"] for v in c["variants"]], [s["licence"] for s in c["sources"]])
