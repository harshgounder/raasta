# derive the /map element impact fallback (block / slow / warn per barrier type per body) from the routing lane's
# assumptions file. run: python3 -I tools/make_impact_fallback.py   (from app/site). Read-only on app/route.
# the map prefers /content/impact-matrix.json when it exists; this file is only the fallback.
import json
from pathlib import Path

here = Path(__file__).resolve().parent.parent
src = here.parent / 'route' / 'hroute' / 'assumptions.json'
a = json.loads(src.read_text())['barriers']
out = {
    '_about': 'FALLBACK derived by app/site/tools/make_impact_fallback.py from app/route/hroute/assumptions.json '
              '(routing-lane ASSUMPTIONS, not measurements). block = hard block for that body; slow = adds 60 s or '
              'more, or blocks only under a measured condition; warn = adds under 60 s. Replaced at runtime by '
              '/content/impact-matrix.json when that file exists.',
    'types': {},
}
for t, v in a.items():
    if t.startswith('_') or not isinstance(v, dict):
        continue
    out['types'][t] = {}
    for p, r in v.items():
        if not isinstance(r, dict):
            continue
        cond = [k for k in r if k.startswith('block_if')]
        cost = r.get('cost_s') or 0
        if r.get('block') or r.get('unknown_height') == 'block':
            lvl = 'block'
        elif cond or cost >= 60:
            lvl = 'slow'
        elif cost > 0:
            lvl = 'warn'
        else:
            lvl = 'none'
        note = ', '.join(f"{k.replace('block_if_', 'blocks if ').replace('_', ' ')} {r[k]}" for k in cond)
        out['types'][t][p] = {'level': lvl, 'cost_s': r.get('cost_s'), 'note': note or None}
(here / 'src' / 'map2' / 'impact-fallback.json').write_text(json.dumps(out, indent=1))
print(len(out['types']), 'types')
