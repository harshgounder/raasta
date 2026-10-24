# 04, routing and costs

hermes, 2026-10-25 03:00 IST. Scope: `app/route/hroute/costs.py` (260 lines) and `routing.py` (230 lines).
Formulas are copied from the code with line numbers. **ASSUMPTION** marks a value the code chooses rather than
derives.

## The cost of one segment

The module docstring states the model and the code implements exactly it (`costs.py:1-13`):

```
segment_cost(s) = travel_s + barrier_delay_s + uncertainty_s
travel_s        = length_m / profile.speed_mps                 costs.py:200
```

and the weight used by the search is that sum, or `None` when the segment is blocked (`costs.py:245-248`).

### Barrier delay, and why clusters are combined with a product

Each evidence record becomes a rule for a profile (`costs.py:80-128`), then a probability:

```
p_eff = p_present x p_attach                                     costs.py:137, 208
p_comb(cluster) = 1 - prod(1 - p_eff)                            costs.py:214
```

Clustering is by type and blocking-ness, chaining records closer than `dedupe_m` (default 5 m, **ASSUMPTION**)
so five separate reports about one broken kerb do not multiply into five costs (`costs.py:151-163`, 212-213).
Two records of different type in the same place still both apply.

If a blocking rule reaches `p_comb >= block_p`, the segment is removed for that profile
(`costs.py:225-229`); below the threshold it becomes a soft cost instead (`costs.py:230-237`,
`_decide()` at 141-148). A barrier can never make a segment cheaper, which is stated at `costs.py:9` and is the
reason the model is monotone.

### p_present, the part that ages

For a permanent barrier the probability is just the record's confidence (`costs.py:46-47`). For a temporary one:

```
age_h   = (leave_time - observed_at) in hours                    costs.py:54
decay   = 0.5 ** (age_h / half_life_h)                            costs.py:55
base    = max(decay, recurrence[type])                            costs.py:57
ratio   = hour_curve[leave_hour] / max(hour_curve[observed_hour], 0.1)   costs.py:61-64
p       = confidence * min(1, base * ratio)                       costs.py:65
```

Every factor in that block is an **ASSUMPTION**: the half-life per type lives in `temporal.default_half_life_h`,
the recurrence floor in `temporal.recurrence`, and the hour curves in `temporal.hour_curve`
(`costs.py:48-58`). The receipt prints them, which is how a reader sees that a vendor stall decays in hours and
a kerb does not decay at all.

### Uncertainty, the `-ln(1-p)` term

The docstring calls it out (`costs.py:6-7`) and the code is at `costs.py:166-194`:

```
uncovered = length - sum(clear_radius_m around each clear-type record)   costs.py:176-185
p_unseen  = 1 - (1 - p_per_100m) ** (uncovered / 100)                    costs.py:187
uncertainty_s = -ln(1 - min(p_unseen, 0.99)) * profile.unknown_penalty_s costs.py:194
```

Three details that matter for honesty.

1. Only **clear-type** evidence covers length, because "we saw a barrier here" says nothing about the next 40 m
   (`costs.py:173-174`, and the 25 m default radius at 176).
2. Some segment kinds are priced per segment rather than per 100 m (`costs.py:188-189`).
3. The uncertainty term is a **routing penalty in cost seconds, never travel time**. The route object says so in
   a field literally named `_uncertainty_cost_about` (`routing.py:122`), which exists because we once displayed
   it as minutes and the route looked four times slower than the model claimed.

## The search

- Shortest route: Dijkstra on `length_m` only (`routing.py:183`).
- Accessible route: Dijkstra where the edge weight is the whole segment cost, and edges whose weight is `None`
  (blocked) are dropped (`routing.py:161-164`, 197).
- If no accessible path exists, a second search uses `BIG + length` for blocked edges to find the
  **least-blocked** path, and the response names the blocking barriers instead of pretending a route exists
  (`routing.py:166-168`, 211-222). `BIG = 1e7` at `routing.py:14`.
- Multi-edge graphs pick the cheapest parallel edge (`routing.py:38-44`).

Complexity is Dijkstra with a binary heap, so `O(E log V)`; on the Jaipur graph (2,957 nodes, 4,537 segments)
the whole per-profile memoisation makes a two-route answer effectively instant, and the precomputed route files
are what the site serves.

## Tiers, the four words the site prints

`tier()` at `costs.py:32-40` assigns exactly one of four values per segment:

| tier | rule |
|---|---|
| `known_barrier` | any accepted evidence whose type is not a clear type (`costs.py:34-35`) |
| `known_clear` | accepted evidence, all clear types (`costs.py:36-37`) |
| `osm_tag` | only an OSM tag backs it (`costs.py:38-39`) |
| `unknown` | nothing (`costs.py:40`) |

Route output carries all four counts plus `unknown_share_pct` (`routing.py:76`, 123), and the human summary
prints them in that order (`routing.py:97-100`).

## Profiles

Profiles live in `assumptions.json` and are read through `cfg()`: each carries `speed_mps`,
`unknown_penalty_s`, and per-barrier rules with `block`, `cost_s`, optional `per_cm_s`,
`block_if_height_cm_gt`, `block_if_clear_width_cm_lt` (`costs.py:105-127`). Slope rules are separate and
compare against both standards:

```
MOHUA_PCT = 100/12 = 8.33 %    costs.py:23   MoHUA HG 2021 cl. 3.7.2, kerb ramp 1:12
IRC_PCT   = 100/15 = 6.67 %    costs.py:24   IRC:103-2022 sec 6.7 Fig. 48, kerb ramp 1:15
```

and `_slope_text()` prints both verdicts side by side (`costs.py:74-77`), which is the code-level version of
the "two codes disagree" explainer on the site.

Seven profiles exist; the demo prints whichever the user picks, and the precomputed files hold several leave
times per profile.

## What is weak here, in order

1. Every number above the travel term is an assumption with a name, and the impact matrix says so too. The
   honest claim is "the sign of the effect is defensible, the magnitude is not measured".
2. `block_p` is one global threshold, so a slightly-evidenced kerb and a strongly-evidenced one are treated the
   same once both clear it.
3. The hour curves are hand-made, and only apply when the observation has a clock time (`costs.py:60-64`).
   A photo without EXIF time gets no hour adjustment, which the receipt says in words.
4. The search is time-independent within a route: one leave time prices the whole path, so a two-hour walk
   across a market hour is not modelled.
