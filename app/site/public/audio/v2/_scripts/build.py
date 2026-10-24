"""build every RAASTA v2 cue from the downloaded real recordings (sources.json), export ogg+m4a, write build-report.json.
spec per stem: src (sources.json key), start, dur, loop (L, X) or fades, target LUFS, af (ffmpeg filter on decode)."""
import json, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from lib import decode, normalise, fade, make_loop, seam_db, encode, measure, SR

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1]
SRC = json.load(open(os.path.join(BASE, "sources.json")))
os.makedirs(OUT, exist_ok=True)

BED, ONE, HIT = -22.0, -18.0, -14.0
HP = "highpass=f=70"
# cue -> list of variants (stem, src, start, dur, opts)
SPEC = {
 "indian_street_morning_bed": [("street_morning_bed", "street_451488", 67.0, 48.0, dict(loop=(45.0, 3.0), target=BED, af="highpass=f=60,lowpass=f=12000"))],
 "market_bed": [("market_bed", "market_451351", 97.0, 48.0, dict(loop=(45.0, 3.0), target=BED, af="highpass=f=60,lowpass=f=12000"))],
 "wind_high_bed": [("wind_high_bed", "wind_697217", 0.0, 41.0, dict(loop=(37.0, 4.0), target=BED, af="highpass=f=40"))],
 "temple_bell": [
   ("temple_bell_1", "bell_271626", 0.0, 7.5, dict(fin=0.005, fout=1.5, target=ONE, af=HP)),
   ("temple_bell_2", "bell_271627", 0.0, 8.9, dict(fin=0.005, fout=1.5, target=ONE, af=HP))],
 "cat_paws": [(f"cat_paw_{i+1}", "paws_569255", max(0, t - 0.012), 0.13, dict(fin=0.003, fout=0.07, target=-22.0, af="highpass=f=200,lowpass=f=5000"))
              for i, t in enumerate([0.35, 0.63, 1.16, 2.22, 7.81, 8.07])],
 "cat_purr": [("cat_purr", "purr_579898", 4.0, 9.0, dict(fin=1.0, fout=2.0, target=ONE, af="highpass=f=30"))],
 "myna_call": [
   ("myna_call_1", "myna_338173", 0.0, 2.8, dict(fin=0.02, fout=0.4, target=ONE, af="highpass=f=300")),
   ("myna_call_2", "myna_338173", 2.6, 2.9, dict(fin=0.05, fout=0.5, target=ONE, af="highpass=f=300"))],
 "wingbeats": [
   ("wingbeats_1", "wings_532180", 0.9, 2.4, dict(fin=0.01, fout=0.5, target=ONE, af=HP)),
   ("wingbeats_2", "wings_499570", 0.5, 3.6, dict(fin=0.01, fout=0.6, target=ONE, af=HP))],
 "scooter_passby": [
   ("scooter_passby_1", "scooter_450698", 2.0, 15.0, dict(fin=1.5, fout=3.0, target=ONE, af=HP)),
   ("scooter_passby_2", "scooter_523959", 1.5, 10.0, dict(fin=1.5, fout=2.5, target=ONE, af=HP))],
 "horn_hit": [("horn_hit", "horn_451318", 0.85, 2.6, dict(fin=0.005, fout=0.35, target=HIT, ceiling=-1.0, af=HP))],
 "walker_taps": [(f"walker_tap_{i+1}", "walker_540712", t - 0.05, 0.95, dict(fin=0.005, fout=0.25, target=ONE, af="highpass=f=120"))
                 for i, t in enumerate([1.06, 2.94, 5.23, 7.21])],
 "cane_and_steps": [
   ("cane_tap_1", "cane_138296", 0.0, 0.209, dict(fin=0.002, fout=0.04, target=ONE, af=HP)),
   ("cane_tap_2", "cane_138295", 0.0, 0.209, dict(fin=0.002, fout=0.04, target=ONE, af=HP)),
   ("cane_steps_old", "cane_138328", 0.0, 2.46, dict(fin=0.005, fout=0.2, target=ONE, af=HP)),
   ("kid_steps", "cane_634986", 0.0, 6.3, dict(fin=0.05, fout=0.5, target=ONE, af=HP)),
   ("young_steps_quick", "cane_368833", 0.0, 6.0, dict(fin=0.05, fout=0.6, target=ONE, af=HP))],
 "wheelchair_roll": [("wheelchair_roll", "wheelchair_174603", 2.5, 8.5, dict(fin=0.8, fout=1.5, target=ONE, af=HP))],
 "phone_tap": [
   ("phone_tap_1", "phone_444683", 1.22, 0.5, dict(fin=0.002, fout=0.15, target=ONE, af="highpass=f=200")),
   ("phone_tap_2", "phone_444683", 3.0, 0.5, dict(fin=0.002, fout=0.15, target=ONE, af="highpass=f=200")),
   ("phone_tap_3", "phone_536315", 0.38, 0.5, dict(fin=0.002, fout=0.15, target=ONE, af="highpass=f=120"))],
 "ending_resolve": [("ending_resolve", "resolve_153262", 10.0, 24.0, dict(fin=6.0, fout=8.0, target=ONE + -2, af="highpass=f=40"))],
}
OVR = json.load(open(os.path.join(BASE, "overrides.json"))) if os.path.exists(os.path.join(BASE, "overrides.json")) else {}
only = set(sys.argv[2:])
report = json.load(open(os.path.join(BASE, "build-report.json"))) if os.path.exists(os.path.join(BASE, "build-report.json")) else {}
for cue, variants in SPEC.items():
    for stem, src, start, dur, o in variants:
        if only and stem not in only and cue not in only:
            continue
        if stem in OVR:
            src, start, dur = OVR[stem].get("src", src), OVR[stem].get("start", start), OVR[stem].get("dur", dur)
        if src not in SRC:
            print("SKIP (no source)", stem, src); continue
        a = decode(SRC[src]["file"], start, dur, af=o.get("af"))
        if a.size == 0:
            print("EMPTY", stem); continue
        if "loop" in o:
            L, X = o["loop"]
            L = min(L, len(a) / SR - X - 0.01)
            L = (int(L * SR) // 1024) * 1024 / SR  # whole AAC frames, so the m4a decodes to the exact loop length
            a = make_loop(a, L, X)
        else:
            a = fade(a, o.get("fin", 0.01), o.get("fout", 0.05))
        a, lufs, tp = normalise(a, o["target"], o.get("ceiling", -1.5))
        if "loop" not in o:
            a = fade(a, 0.002, 0.01)  # guard against limiter edge clicks
        encode(a, OUT, stem, loop="loop" in o)
        seam = seam_db(a) if "loop" in o else None
        report[stem] = dict(cue=cue, src=src, start=start, dur=round(len(a) / SR, 3), loop="loop" in o, lufs=round(lufs, 2), true_peak=round(tp, 2), seam_db=None if seam is None else round(float(seam), 1), target=o["target"])
        print(f"{stem:24s} {len(a)/SR:6.2f}s LUFS {lufs:6.1f} TP {tp:5.1f} seam {seam if seam is None else round(seam,1)}")
json.dump(report, open(os.path.join(BASE, "build-report.json"), "w"), indent=1)
