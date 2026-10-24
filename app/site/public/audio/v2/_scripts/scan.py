"""per-second rms profile of a file + best calm window of length W (lowest peak-to-median spread)."""
import sys, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import decode, SR, rms_env
p = sys.argv[1]; W = float(sys.argv[2]) if len(sys.argv) > 2 else 40
a = decode(p, af="highpass=f=60")
e = rms_env(a, 0.5)
peak = 20*np.log10(np.abs(a).max()+1e-9)
print(f"{p.split('/')[-1]} dur {len(a)/SR:.1f}s peak {peak:.1f} dBFS median {np.median(e):.1f}")
print(" ".join(f"{v:.0f}" for v in e[::2]))
w = int(W*2)
best = []
for s in range(0, max(1, len(e)-w), 2):
    seg = e[s:s+w]
    best.append((np.max(seg)-np.median(seg), s/2, np.median(seg)))
best.sort()
print("calmest windows (spread dB, start s, median):", [(round(b[0],1), b[1], round(b[2],1)) for b in best[:5]])
# stereo correlation
if a.shape[1] == 2:
    c = np.corrcoef(a[:,0], a[:,1])[0,1]; print(f"L/R corr {c:.2f}")
