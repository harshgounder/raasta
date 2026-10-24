# Pre-registered selection rubric (dsh lane), 2026-10-24 14:40 IST

Written BEFORE wave 1 results are read, so the scores cannot be fitted to them. A statement or
fork candidate is scored on these seven axes, each 0 to 3, with the evidence that sets the score.
Total 21. Weights are deliberately flat; no axis can rescue a hard fail.

## Hard gates (any one fails the candidate outright)

1. Licence allows fork and public demo (MIT, Apache-2, BSD, AGPL acceptable for a private demo only
   if we never serve a modified binary; GPL/AGPL on a hosted site gets a legal note before build).
2. Repository alive: a commit or release inside the last 12 months, or an archived repo that still runs.
3. Runs on this box or in a browser: CPU-only is fine, a GPU-only model must have a hosted or quantised
   path, and anything needing paid infra beyond free credits fails.
4. Demo path in the browser: a route exists to a live URL without asking the judge to install anything.
5. No human-labelling dependency we cannot satisfy tonight (for example a pharmacist-authored test set).

## The seven axes

| axis | 0 | 1 | 2 | 3 | evidence required |
|---|---|---|---|---|---|
| Forkability | rewrite from scratch | fork plus heavy surgery | fork plus config and UI | fork, run, reskin in hours | repo, licence, last commit, install path |
| Demo-ability in browser | none | video only | server demo with setup | live in one click, CPU or hosted | live URL or a runbook that starts in under 5 minutes |
| Judge legibility | needs expertise | explainable with a slide | explainable in one sentence | a child understands and gasps | one-sentence pitch plus a 10-second visual |
| Novelty to a non-expert | familiar | seen in other demos | surprising | feels impossible until it happens | what the judge has plausibly never seen |
| Evidence quality | claims only | demo only | benchmark reported | benchmark reproduced by us | our own measured number, command logged |
| Risk of failure tonight | certain | likely | manageable | low | list of unknowns and a fallback |
| Story fit for the santioni site | none | loose | good | the motion literally is the product | beat-by-beat sketch of the 7 beats |

## Mind-boggling, defined for a non-expert judge

It must satisfy all three:
1. One sentence, no jargon, that a parent repeats to a friend.
2. A visible cause and effect the judge can trigger themselves in one click.
3. An answer to "what if X happens?" that is a second visible behaviour, not a promise.

Anything that needs the judge to trust a benchmark chart scores at most 2 on legibility.

## Scoring discipline

- Score every candidate before comparing across candidates; log the reason per axis.
- A score without a URL or a command is not a score.
- Two independent readers (me and one other agent) score the shortlist; disagreements above 3 points
  total go to claude with both reasons.
- The pre-registered shortlist size is 3. Widening after seeing results is allowed only with a written
  reason, and the widened list must be scored under the same rubric.
