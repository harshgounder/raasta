# P-B wow scan, CL-01..04, SC-01, SC-02 (report only if mind-blowing)

Written by hermes 2026-10-24 ~15:10 IST, lane L2/L3 per WAVE-1-BRIEF: these six are "wow scan only, report
only if mind-blowing, with reasons". The user's own instruction is that climate and smart cities are
ignored unless there is a truly mind-blowing angle, and AI/ML comes first. So this file exists to be short
and to justify a no, not to build a case.

Method honesty: time-boxed scan, 6 statements, three live searches plus the PS text in
`PROBLEM-STATEMENTS.md`. Anything below marked UNVERIFIED was not opened this session and must not be
quoted in a pitch without a check.

## CL-01 Satellite Forest-Loss Alerts (Sentinel-2, test on an unseen Indian state)

Ecosystem is mature and free: Global Forest Watch integrated alerts, GLAD-S2 at 10 m, RADD radar alerts.
Sources opened: https://data.globalforestwatch.org/datasets/gfw::integrated-deforestation-alerts/about,
https://glad.umd.edu/dataset/glad-forest-alerts, https://www.globalnaturewatch.org/blog/data-and-tools/glad-s2-offers-high-resolution-deforestation-alerts/
(fetched 2026-10-24).

- Feasibility: high. Data and baselines exist, and the statement's "unseen Indian state" test is a clean,
  honest generalisation demo.
- Wow for a non-expert judge: moderate. A map with alerts blinking is decent, but the judge has likely
  seen GFW itself, and "we rebuilt Global Forest Watch" is the fastest way to lose an innovation score.
- Verdict: NOT mind-blowing on its own. Only worth it if the angle were something like catching a specific
  local land-grab in the user's own district within 6 days, and the build time does not allow that story
  work. Recommend ignore.

## CL-02 Scope 3 Emissions from Public Spending Records

- Feasibility: low for this fleet. The statement requires 2,000 hand-labelled lines with two independent
  labellers agreeing, which is a human-hours problem inside a 5.5 hour build window. No shortcut found in
  the scan.
- Wow: an emissions number attached to a government purchase order is a strong story for an auditor, weak
  for a common person.
- Verdict: ignore. The labelling requirement alone makes it infeasible tonight.

## CL-03 Predicting Energy Consumption for a Building

- Feasibility: high (standard tabular modelling on public datasets), but that is exactly why it is
  generic. A non-expert judge sees a chart of predicted versus actual.
- Wow: none without a story. Nothing in the scan changes that.
- Verdict: ignore, unless paired with CL-04 as a single energy narrative, which the user has already
  deprioritised.

## CL-04 MathWorks Challenge (Building Energy with MATLAB)

- Feasibility: gated on MATLAB tooling and a specific 5-minute presentation rubric, and licence terms were
  not checked in this scan (UNVERIFIED, and worth checking only if the user overrules and wants it).
- Wow: judged by MathWorks criteria, so it rewards a different skill set than the rest of the field.
- Verdict: ignore for this fleet. MATLAB is not our stack and the rubric is externally fixed.

## SC-01 Multi-Camera Vehicle Re-Identification (no number plates)

Sources checked: https://edge-ai-tech.eu/privacy-aware-vehicle-re-identification-at-the-edge-tracking-without-number-plates/
and https://www.aicitychallenge.org/2026-track4/ (fetched 2026-10-24; note track 4 this year is
text-based person re-ID, so the vehicle track number may differ, UNVERIFIED which track).

- Feasibility: low on this box. Re-ID across cameras needs GPU training; the local card is a GTX 1650 with
  4 GB and 7 GB system RAM. Pretrained models exist, but the statement's evaluation on unseen cameras is
  where they fail.
- Wow: high concept ("find the car without reading any plate"), and privacy framing is easy for a lay
  judge to grasp.
- Verdict: not for this fleet tonight. The demo would be a pretrained model on sample footage, which a
  sharp judge reads as a wrapper, and the hardware cannot train a fix.

## SC-02 Accessible Walking Routes from Street Imagery

Sources: Project Sidewalk (https://dl.acm.org/doi/fullHtml/10.1145/3290605.3300292, 2019 paper) and the UW
OpenSidewalks project (https://tcat.cs.washington.edu/opensidewalks/), both fetched 2026-10-24.

- Feasibility: medium to high for a demo. Project Sidewalk is an open web tool for labelling sidewalk
  accessibility from street imagery, and the university project publishes annotated data.
- Wow: genuinely humane and instantly legible to a common person ("can my mother in a wheelchair get from
  this bus stop to that clinic"). It is the one P-B statement with a real emotional hook.
- Blocker: street imagery coverage in India. Google Street View exists for a limited set of Indian cities
  (UNVERIFIED for the target city, must be checked before pitching), so an honest demo is limited to
  covered areas or to a curated image set.
- Verdict: the only one of the six that could qualify as mind-blowing, and it still loses to a strong AI/ML
  statement because the user put AI/ML first and because imagery coverage is the risk. Report only, do not
  build.

## Bottom line for the lead

None of the six justifies breaking the user's AI/ML-first instruction. If the 6:15 PM additional problem
statements contain an AI/ML statement, that is where the remaining research time belongs. SC-02 is the one
to keep in a back pocket: if a later statement turns out unbuildable, an accessibility-route demo is the
fallback with the best story per hour of work.
