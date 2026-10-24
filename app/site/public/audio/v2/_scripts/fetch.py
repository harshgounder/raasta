import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..")
cands = json.load(open(os.path.join(BASE, "cands.json")))
PICKS = [
 ("street", "street quiet morning alley", "kyles"),
 ("street", "India small street neighbourhood", "Martin.Sadoux"),
 ("street", "Indian Street traffic Ambience 2", "Athul_PR"),
 ("market", "Trivandrum Street Market", "Alcappuccino"),
 ("market", "crowd ext medium busy street downtown", "kyles"),
 ("market", "market ext covered on street close", "kyles"),
 ("wind", "Looping Gentle Wind Ambience", "dhallcomposer"),
 ("wind", "Wind blowing in an antenna", "felix.blume"),
 ("wind", "Wind.wav", "Cyril Laurier"),
 ("bell", "2HinduTemplesBells1", "LoopUdu"),
 ("bell", "2HinduTemplesBells2", "LoopUdu"),
 ("bell", "Shiva Bells", "grololo"),
 ("paws", "Cat Running Stairs", "PhilllChabbb"),
 ("paws", "Walking.wav", "Augdog"),
 ("paws", "Claws animal", "Nakhas"),
 ("cane", "paving_01a_barefeet_walk", "sturmankin"),
 ("purr", "Cat Purring (long/clear/loud)", "JamesBradford"),
 ("purr", "a big fat tom cat purrs", "PostProdDog"),
 ("myna", "Crowd of Myna birds", "edranil"),
 ("myna", "Birds of Bengal", "bratendu"),
 ("wings", "pigeons_fly away_ wing flaps", "csaszi"),
 ("wings", "Pigeons flying", "mcmikai"),
 ("wings", "birds taking off to fly", "Hope-Sounds"),
 ("scooter", "scooter pass by medium speed", "kyles"),
 ("scooter", "moped pass by.wav", "lartti"),
 ("scooter", "PassingMoped01", "Pingel"),
 ("horn", "auto horn honk real annoyed close", "kyles"),
 ("horn", "auto horn honk angry driver", "kyles"),
 ("walker", "Zimmer Walker Frame", "tuesdayblack"),
 ("cane", "Footsteps_Cane_hitting_Pavement", "Tdude9000"),
 ("cane", "Cane_Hitting_Pavement_2", "Tdude9000"),
 ("cane", "Cane_Hitting_Pavement_3", "Tdude9000"),
 ("cane", "walking on stone trail with white cane", "dpmart1970"),
 ("cane", "Steps of a Child in Grass", "JiggleSticks"),
 ("cane", "footsteps child parquet", "Yuval"),
 ("cane", "Walking footsteps on pavement.WAV", "thomasanthon"),
 ("cane", "Footsteps_Quick", "georgisound"),
 ("wheelchair", "SonicSnaps-IDES-FR-wheelchair", "thecityrings"),
 ("wheelchair", "Wheelchair.wav", "Shearwater256"),
 ("phone", "Screen tap", "EilasSFX"),
 ("phone", "Smart Phone Click", "AO-SoundPawz"),
 ("phone", "iPhone taps.aif", "figgy78"),
 ("resolve", "Tanpura 10", "sankalp"),
 ("resolve", "Singing Bowl, long without reverb", "hollandm"),
]
EXTRA = []  # rows found outside cands.json
reg = {}
for cue, t, c in PICKS:
    hit = None
    for k, rows in cands.items():
        for r in rows:
            if t.lower() in r["title"].lower() and c.lower() in r["creator"].lower():
                hit = r; break
        if hit: break
    if not hit:
        print("MISS", cue, t); continue
    sid = re.search(r"/sounds/(\d+)", hit["foreign_landing_url"] or "")
    sid = sid.group(1) if sid else hit["id"][:8]
    stem = f"{cue}_{sid}"
    dst = os.path.join(BASE, "dl", stem + "." + (hit["url"].rsplit(".", 1)[-1][:4]))
    if not os.path.exists(dst):
        subprocess.run(["curl", "-sSL", "-m", "90", "-A", "raasta-sound/1.0", "-o", dst, hit["url"]], check=False)
    reg[stem] = {"cue_group": cue, "file": dst, "title": hit["title"], "creator": hit["creator"], "license": hit["license"], "license_version": hit["license_version"], "landing": hit["foreign_landing_url"], "url": hit["url"], "source": hit["source"], "freesound_id": sid}
    print(stem, os.path.getsize(dst) if os.path.exists(dst) else "FAIL", hit["license"], hit["title"][:40])
json.dump(reg, open(os.path.join(BASE, "sources.json"), "w"), indent=1)
