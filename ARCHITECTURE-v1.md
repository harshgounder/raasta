# ARCHITECTURE v1 (DRAFT, claude, 2026-10-24 ~16:50 IST): awaiting user GO

Working name: **(TBD with the story)**. SC-02 Accessible Walking Routes from Street Imagery, all of India.
Sources: research/BRAINSTORM-SYNTHESIS-v1.md, research/claude/sc02-*.md, method/*.md. Parallel SC-02 digest pending (fork/domain/tech) and may change parts.

## Product promise (one line)
Any street photo from anywhere in India becomes measured, honest accessibility evidence on the right stretch of footpath, and every person gets the route their body can actually take, at the hour they leave. It never says "safe": only "known barrier", "known clear (photo date)", or "unknown".

## System

```
BROWSER (static, santioni kit reskin: Vite + three.js)
  story scroll  ->  demo section
    map (MapLibre + deck.gl): MUJ campus + 2 more cities (precomputed)
    upload ANY photo -> /analyze (live)        evidence "receipt" cards
    profile: manual wheelchair | walker (Dadi/Kamla) | pram | crutches | low vision
    leave-time slider -> route changes          "pit wall": +minutes, kerbs climbed, rest stops
    uncertainty clouds + known/unknown coverage  same-kerb-different-sky slider (simulated, labelled)
    3D crossing (Spark splat, labelled reconstructed) if built in <2 h
    what-if wall (10 buttons, each runs a real case)     one-tap Hindi complaint draft
        |
        |  HTTPS (cloudflared tunnel to the user's PC; fallback = precomputed JSON baked into the site)
        v
BACKEND (FastAPI on the user's PC, GTX 1650 via ~/r2-venv torch 2.13 cu130 = CUDA OK)
  /analyze
    1 intake: EXIF time/GPS/heading, condition fingerprint (day/night/rain/fog/blur) -> zoo router bin
    2 detect A: open-vocab detector (YOLOE or Grounding DINO)      } agreement = confidence
      detect B: Florence-2 / OWLv2                                  } disagreement = ABSTAIN
      judge:    small VLM (Qwen-VL via OpenRouter/NVIDIA key, or local) with the Indian label set (Chandigarh paper)
    3 measure: kerb/step height from 3 routes: shadow altimetry (sun position) + vanishing-point/camera-height geometry
               + metric depth (MoGe-2 / Depth Anything V2) -> value +- error bar; spread too wide = ABSTAIN
    4 extra signals: shadow clock (time + heading check), wall stain line (flood depth), wet surface
    5 place: GPS + heading + side-of-road -> probability over footpath segments; < 0.7 = ABSTAIN
    6 record: ACCEPT/ABSTAIN/REJECT + tier stamp (observed today / earlier / inferred / unknown) + receipt
  /route
    OSMnx walk graph per city (precomputed), edge cost per profile from barriers (MoHUA 1:12 vs IRC 1:15, stricter for wheelchair)
    + blockage probability by hour (POI-based, labelled as assumption) + uncertainty cost -log(1-p)
    -> best route, shortest route, and "what you would hit on the shortest" list
  /complaint: Hindi draft with photo, GPS, segment, legal clause, jurisdiction
DATA
  own labelled Indian set: the user's MUJ photo walk (day + night pairs) + 3 ruler-measured kerbs (ground truth)
  YouTube walking-tour frames from several Indian cities (night, rain, markets) via yt-dlp + re media frames
  Project Sidewalk API labels (CC0, incl. Chandigarh), Mapillary where available
  OSM via OSMnx; Open Buildings heights for shade (if time)
```

## Lanes (build)
| lane | owner | output |
|---|---|---|
| B1 backend pipeline /analyze (detect, measure, place) | dsh (+ sub-fleet) | FastAPI service + smoke results |
| B2 routing /route + graph + costs + precompute | claude | service + JSON per city |
| B3 site: santioni reskin, story, demo UI, sound | claude (+ helpers) | the website |
| B4 art: character + scene panels (woodcut), deck visuals | codex (GPT-Image) + `re gen chatgpt` | PNGs with gates |
| B5 content: story text, numbers with sources, what-if answers, Hindi complaint templates, deck text | hermes (no code) | markdown |
| B6 checks: verdict per artifact | codex, claude reviews | verdicts/ |
| B7 data: YouTube frames set + labelling of the user's photos | claude helper | dataset + labels |

## Hour gates (fail = switch to the fallback, never debate)
| time | gate | fallback |
|---|---|---|
| 19:00 | /analyze returns a receipt for 3 real photos | detector A + VLM only |
| 21:00 | route on the MUJ graph avoids a real barrier | hand-placed barriers from labels |
| 23:00 | site story + demo wired on precomputed data | static scroll + video of the demo |
| 01:00 | live tunnel works from a phone on mobile data; deck draft | precomputed only |
| 02:30 | FREEZE: live URL, deck PDF, offline fallback tested | |

## Two never-cut beats (solar R7)
1. Upload any photo -> receipt with measured kerb height +- error, or an honest ABSTAIN.
2. Shortest route vs our route for a wheelchair, with the barriers it would hit.

## Open decisions for the user
story (Billu / Kamla / merge) and name; hosting GO (cloudflared + npx vercel); photo walk; hermes-B.
