# docs/: how RAASTA actually works

hermes, started 2026-10-25 02:20 IST. This folder is the technical record: every algorithm, model, formula and
number, with `file:line` references so a reader can check any claim against the code rather than trusting this
prose. Reading code is allowed; writing it is not, and nothing in this folder changes a line of the product.

## How to read this folder

1. Start with `01-system-overview.md` for the map of the machine, then read in numeric order.
2. Every claim that comes from code carries `path:line`. Every claim that is a choice we made rather than a
   measurement is tagged **ASSUMPTION**, and `11-assumptions-register.md` collects them in one place.
3. Numbers in this folder are of two kinds and they are never mixed: **measured** (a run we did, with the file
   that holds the result) and **sourced** (a standard or a paper, with the clause or URL).
4. Where a document could not be finished honestly in the time available, the file says so at the top instead
   of reading as if it were complete.

## Status of the twelve documents, as of 02:25 IST

| file | status | what it holds |
|---|---|---|
| `README.md` | written | this index, the reading rules, the honest status table |
| `01-system-overview.md` | queued | the one-page machine diagram, five stages and their contracts |
| `02-scan-pipeline.md` | **written** | app/analyze stage by stage with the real maths and line refs |
| `03-footpath-network.md` | queued | app/route network build: OSM pull, generated sidewalks, offsets, snapping |
| `04-routing-and-costs.md` | queued | graph search, cost terms, -ln(1-p), half-life, hour curves, tiers, profiles |
| `05-impact-engine.md` | queued | taxonomy, attributes x sensitivity, 8 scorers, combination rules, worked examples |
| `06-evaluation.md` | queued | C6 labels, metrics, the hash split, calibration rounds, bootstrap CIs |
| `07-site.md` | queued | each page, its data flow, and the files it reads |
| `08-story-art-sound.md` | queued | story beats, every art asset with its prompt, every sound with its licence |
| `09-data-and-licences.md` | queued | datasets, counts, licence per source, what may be published |
| `10-file-manifest.md` | queued | every tracked file from `git ls-files`, grouped, one line each |
| `11-assumptions-register.md` | queued | every assumed number, where it lives, what would replace it |

The queue order matters: 03 and 04 next, because the routing maths is the part a technical judge probes first,
then 05, 06, 11. The documentation is being written after the freeze, and it will keep landing in this folder
rather than in a chat message.

## What this folder is not

It is not a pitch. It is not a summary for a judge who will not read. It is the thing we point at when someone
asks "how do you know", and every page of it should survive that question. Where the product is weak, the
document says it is weak and gives the number that proves it.
