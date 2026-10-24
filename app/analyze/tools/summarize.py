"""Print a markdown table + aggregate numbers from one or more cli.py summary.json files.
  python3 tools/summarize.py out/run1/summary.json [...]
"""
import collections
import json
import os
import statistics
import sys

rows = []
for p in sys.argv[1:]:
    rows += json.load(open(p))

ok = [r for r in rows if r.get("ok")]
print(f"images: {len(rows)}, ok: {len(ok)}, failed: {len(rows) - len(ok)}\n")
tot = collections.Counter()
fam = collections.Counter()
hs = collections.Counter()
cond = collections.Counter()
for r in ok:
    tot.update(r["counts"])
    fam.update(r["accept"])
    hs.update(h.split(":")[-1] for h in r["height_status"])
    cond[r["condition"]] += 1
print("| status | count |\n|---|---|")
for k in ("ACCEPT", "ABSTAIN", "REJECT"):
    print(f"| {k} | {tot[k]} |")
print("\nACCEPT by class:", dict(fam.most_common()))
print("height status:", dict(hs))
print("condition bins:", dict(cond))
t = [r["timings"]["total_s"] for r in ok]
if t:
    for key in ("detect_A_s", "detect_B_s", "judge_s", "depth_s", "measure_s", "total_s"):
        v = [r["timings"].get(key) for r in ok if r["timings"].get(key) is not None]
        if v:
            print(f"{key}: median {statistics.median(v):.2f} s, p90 {sorted(v)[int(0.9 * (len(v) - 1))]:.2f} s, max {max(v):.2f} s (n={len(v)})")
print("\n| image | city | cond | ACC | ABS | REJ | accepted classes | heights | judge | total s |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    name = os.path.basename(r["image"])
    if not r.get("ok"):
        print(f"| {name} | | | | | | FAILED: {r['error'][:80]} | | | {r['seconds']} |")
        continue
    j = r["judge"]
    jt = f"{j.get('answered', '?')}/{j.get('calls', 0)} answered" if j.get("calls") else "no call"
    print(f"| {name} | {r.get('city') or ''} | {r['condition']} | {r['counts']['ACCEPT']} | {r['counts']['ABSTAIN']} | "
          f"{r['counts']['REJECT']} | {', '.join(r['accept'][:5])} | {'; '.join(r['heights']) or '-'} | {jt} | {r['timings']['total_s']} |")
