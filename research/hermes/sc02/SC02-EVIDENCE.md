# SC-02 evidence: compelled sources and trips-not-taken inputs

hermes, 2026-10-24 16:55 IST, research only. Two things claude asked for: the scar ledger's primary
sources (CAG, court orders, RTI, grievance portals) and the denominators for trips-not-taken (census
elderly and disabled by ward). Everything here is labelled OPENED (I read the page today) or UNOPENED (named
so it can be fetched, not quoted as evidence yet).

## 1. The strongest hook found tonight: footpaths are a fundamental right, per the Supreme Court

- OPENED: https://www.openglobalrights.org/who-gets-to-walk-disability-and-indias-cities/ , fetched
  2026-10-24. It reports that on **19 June 2026** the Supreme Court declared that walking on a safe,
  demarcated footpath is a fundamental right, and connects it to disability access.
- OPENED: https://www.disabilityrightsindia.com/2025/05/ , fetched 2026-10-24. A May 2025 order is quoted
  verbatim: `"Right to have unobstructed and disabled-friendly footpaths is guaranteed under Article 21,
  the Court unequivocally stated."`
- OPENED (secondary, headline level only): https://inclusionatwork.live/sc-disabled-friendly-footpaths-guidelines/
  reports an order requiring States and UTs to frame disabled-friendly footpath guidelines within two
  months, aligned with IRC norms.
- UNOPENED primary text: the judgment itself and the order dates. Do not quote a case number or a bench
  until the PDF is read. In the pitch, cite the date and the right, not a case citation.

Why this matters for the site: the pitch does not have to argue that accessibility is nice. The highest
court in the country already said the route is a right, and the product is the instrument that measures
whether the right is honoured on a specific 40 m of street.

## 2. CAG and audit machinery (machine-readable scars)

- OPENED (search result + dataset page): https://data.opencity.in/dataset/cag-audit-report-on-local-bodies
  aggregates CAG local-body audit reports, with PDFs, and is the cheapest machine-readable entry point.
- OPENED (portal): https://cag.gov.in/en/audit-report/details/124977 is a sample audit report detail page,
  which confirms the report-number scheme the scraper would follow.
- UNOPENED: the specific paragraph on footpaths or pedestrian facilities in a Rajasthan or Jaipur ULB
  report. This is the single highest-value fetch left: one CAG paragraph naming footpath deficiencies in
  the target city turns the scar ledger from concept to citation.
- Method: iterate report numbers on cag.gov.in, grep the PDFs for `footpath`, `pedestrian`, `accessibility`,
  `IRC 103`. Each hit stores report number, page, and the sentence.
- Also usable: https://saiindia.gov.in/webroot/uploads/download_audit_report/ is where the PDFs actually
  live (one Odisha report opened as a format sample).

## 3. Standards to measure against (numbers a judge can verify)

- OPENED: CPPR Pedestrian Audit Report 2008, https://www.cppr.in/wp-content/uploads/2012/10/Pedestrian-Audit-Report-2008.pdf
  lists audit criteria verbatim: footpaths should `Have even surface`, `Have continuity`, `Be at least 1.5 m
  wide`, which gives us a defensible width threshold alongside the 150 mm kerb standard.
- OPENED earlier: GTKP audit paper with measured Indian footpath heights of 200 to 250 mm,
  https://www.gtkp.com/document/irf-world-road-meeting-2017-paper-814/
- OPENED earlier: UNDP India Disability Accessibility Audit 2024 PDF, method plus manhole placement
  guidance, https://www.undp.org/sites/g/files/zskgke326/files/2024-11/dissability_accessibility_audit_report.pdf
- UNVERIFIED: the exact clause text of IRC:103. Cited by Indian studies but the standard itself was not
  opened. If the site prints "IRC:103", someone must read the clause first, or print "150 mm standard"
  without the code number.

## 4. Grievance portals (the complaint half of the scar ledger)

Named, all UNOPENED for this project. Each is a route to geocoded, dated, citizen-authored failures:

| channel | what it should give | note |
|---|---|---|
| State municipal grievance portals (e.g. Rajasthan Sampark, Jaipur Nagar Nigam Greater and Heritage portals) | complaint text, ward, date, status | status fields are the time-to-fix input |
| CPGRAMS (pgportal.gov.in) | central redressal, includes urban ministry | slower, but archived and citable |
| Swachhata app and municipal WhatsApp bots | pothole and footpath complaints with photos | often has images, which the pipeline can read directly |
| X and Reddit civic threads, Google Maps reviews of footpaths, bus stops and hospitals | unfiltered, sometimes with photos and dates | terms and rate limits apply, do not scrape hard |
| RTI replies | the "was it fixed" truth | the only channel that proves inaction in writing |

Method that keeps it honest: 50 geocoded complaints in one city, deduplicated by street segment, then
cross-checked against imagery. If imagery shows the barrier is still there while the portal says "closed",
that pair is the most powerful single artefact the project can show a judge.

## 5. Trips-not-taken: the denominators

Goal: a number of the form `people within 400 m of this failure who cannot use this route`, and a rupee
cost for the trips they do not make.

- UNOPENED: Census 2011 disability tables (India publishes disabled population by type of disability at
  district and sub-district level; ward-level is generally NOT published, which is the honest limitation).
  Route: censusindia.gov.in tables, C-series, disability by age and type.
- UNOPENED: elderly population by ward from the same census, plus municipal ward population projections
  where a city has published them.
- UNOPENED: transport accessibility literature for the avoidance rate. Without a cited rate, the estimate
  must be shown as a range with the assumption printed on screen, never as a single number.
- Formula to put in the deck, with the caveat visible:
  `trips avoided per day = catchment population x disability or age share x route dependence share x
  avoidance rate`, and the rupee cost as `trips x mean trip value`, where mean trip value is either a
  local auto fare (observable) or a minimum wage fraction (documented), never a made-up figure.
- The honest sentence for the pitch: "this is an estimate from census shares and a stated avoidance rate,
  here is the range, and here is the one trip we can prove happened before the footpath broke" (a
  before/after imagery pair, if we can find one).

## 6. What I would fetch next, in order, if the clock allowed

1. One CAG paragraph on footpaths in a Rajasthan ULB report (citation power, 40 minutes).
2. The 19 June 2026 Supreme Court judgment PDF, to get the exact holding and bench (citation power, 30 min).
3. 50 geocoded complaints from one Jaipur portal, deduplicated by segment (demo evidence, 60 min).
4. Census 2011 disability and elderly shares for Jaipur district, as the trips-not-taken denominator
   (30 min, and it forces the range presentation).

All research. None of it is code, and any one of the four materially hardens the pitch.
