"""list transient events in a file: start, length, peak dB, centroid. usage: events.py file [thresh_db_above_median] [min_gap_s]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from lib import decode, SR
p = sys.argv[1]; th = float(sys.argv[2]) if len(sys.argv) > 2 else 12; gap = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
a = decode(p, af="highpass=f=80").mean(axis=1)
hop = int(0.01 * SR)
k = len(a) // hop
e = 20 * np.log10(np.sqrt((a[: k * hop].reshape(k, hop) ** 2).mean(1)) + 1e-9)
med = np.median(e)
on = e > med + th
ev = []
i = 0
while i < k:
    if on[i]:
        j = i
        while j < k and (on[j] or (j + int(gap / 0.01) < k and on[j:j + int(gap / 0.01)].any())):
            j += 1
        ev.append((i, j)); i = j
    else:
        i += 1
print(f"{os.path.basename(p)} dur {len(a)/SR:.1f}s median {med:.1f} dB, {len(ev)} events")
for s, t in ev[:60]:
    seg = a[s * hop:t * hop]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) if len(seg) > 64 else np.zeros(2)
    f = np.fft.rfftfreq(len(seg), 1 / SR) if len(seg) > 64 else np.zeros(2)
    cen = (sp * f).sum() / (sp.sum() + 1e-9)
    print(f"  {s*0.01:7.2f}s len {(t-s)*0.01:5.2f}s peak {e[s:t].max():6.1f} cen {cen:6.0f}")
