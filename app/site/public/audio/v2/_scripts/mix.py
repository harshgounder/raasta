"""render preview-mix (about 62 s, beats 0-8 in order) from the shipped .ogg files. usage: mix.py <audio_v2_dir>"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from lib import decode, SR, normalise, encode, measure

D = sys.argv[1]
T = 62.0
N = int(T * SR)
mix = np.zeros((N, 2), np.float32)
cache = {}

def load(stem):
    if stem not in cache:
        cache[stem] = decode(os.path.join(D, stem + ".ogg"))
    return cache[stem]

def env(points):
    """piecewise-linear gain over the timeline, points = [(t, g), ...]"""
    t = np.arange(N) / SR
    xs, ys = zip(*points)
    return np.interp(t, xs, ys).astype(np.float32)[:, None]

def bed(stem, points, offset=0.0):
    a = load(stem)
    reps = int(np.ceil((N + offset * SR) / len(a))) + 1
    b = np.tile(a, (reps, 1))[int(offset * SR): int(offset * SR) + N]
    mix[:] += b * env(points)

def hit(stem, t, g):
    a = load(stem) * np.float32(g)
    s = int(t * SR)
    e = min(N, s + len(a))
    mix[s:e] += a[: e - s]

# beds (gain points: seconds, linear gain)
bed("wind_high_bed", [(0, 0), (2, .55), (6, .35), (8, .12), (16, .12), (17.5, .9), (20.5, .9), (22, .1), (41, .1), (42.5, .9), (45.5, .9), (47, .1), (54, .15), (57, .5), (62, 0)])
bed("street_morning_bed", [(0, 0), (3, .35), (6, .85), (16, .85), (17.5, .25), (20.5, .25), (22, .85), (35, .8), (41, .8), (42.5, .25), (45.5, .25), (47, .75), (54, .6), (58, .25), (62, 0)], offset=3.0)
bed("market_bed", [(0, 0), (26, 0), (28.5, .5), (35, .5), (37, .15), (41, .12), (47, .3), (54, .2), (57, 0), (62, 0)], offset=10.0)

# beat 0 (0-6): title, wind, distant bell, Billu wakes (purr), jumps down
hit("temple_bell_1", 1.6, .28)
hit("cat_purr", 2.6, .22)
hit("cat_paw_3", 5.4, .5); hit("cat_paw_6", 5.62, .42)
# beat 1 (6-16): the cat's street, paws follow the walk, traffic (scooter pass), myna
paws = [f"cat_paw_{i}" for i in (1, 2, 4, 5, 3, 6)]
t, k = 6.3, 0
while t < 15.6:
    hit(paws[k % 6], t, .36 + .06 * (k % 2)); t += .34; k += 1
hit("myna_call_1", 8.2, .35)
hit("scooter_passby_1", 9.0, .75)
# beat 2 (16-21): bird lift 1, wings, wind
hit("wingbeats_1", 16.1, .5)
hit("myna_call_2", 18.6, .3)
# beat 3 (21-27): young guy, quick easy steps, cat sits (no paws)
hit("young_steps_quick", 21.4, .55)
# beat 4 (27-35): old woman, walker taps, then THE one loud hit (horn) at the turn
for i, tt in enumerate([27.4, 29.0, 30.6]):
    hit(f"walker_tap_{i+1}", tt, .5)
hit("horn_hit", 31.9, 1.0)
hit("walker_tap_4", 33.6, .4)
# beat 5 (35-41): old man + kid, cane and steps, the RAASTA phone tap
hit("cane_steps_old", 35.2, .7)
hit("kid_steps", 35.8, .45)
hit("cane_tap_1", 37.6, .45)
hit("phone_tap_3", 39.0, .55); hit("phone_tap_1", 39.45, .5)
# beat 6 (41-47): bird lift 2, wings, first hint of the score
hit("wingbeats_2", 41.0, .5)
hit("ending_resolve", 43.0, .18)
# beat 7 (47-54): walk with RAASTA, paws + cane + kid, Zoya's wheelchair passes, birds
t, k = 47.2, 0
while t < 53.8:
    hit(paws[k % 6], t, .32); t += .36; k += 1
for i, tt in enumerate(np.arange(47.5, 53.8, 1.15)):
    hit("cane_tap_1" if i % 2 == 0 else "cane_tap_2", float(tt), .38)
hit("kid_steps", 47.8, .35)
hit("wheelchair_roll", 48.6, .55)
hit("myna_call_1", 51.6, .25)
# beat 8 (54-62): arrival, temple bell, score resolves
hit("temple_bell_2", 54.4, .55)
hit("ending_resolve", 53.6, .75)

i0, tp0 = measure(mix)
out, i1, tp1 = normalise(mix, -18.0, -1.0)
n = int(1.5 * SR)
out[-n:] *= np.linspace(1, 0, n)[:, None].astype(np.float32)
encode(out, D, "preview-mix")
print(json.dumps({"raw_lufs": round(i0, 1), "raw_tp": round(tp0, 1), "out_lufs": round(i1, 1), "out_tp": round(tp1, 1), "dur": T}))
