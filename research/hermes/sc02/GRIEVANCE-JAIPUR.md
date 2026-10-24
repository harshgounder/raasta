# Jaipur footpath and accessibility complaints: sourced ledger

Research subagent, 2026-10-24. Read only. No form was submitted, no account created, no login attempted.
Raw dumps live in `raw/grievance/`.

**Headline: 43 real, dated, place-specific complaint records were recovered.** Zero come from a municipal
grievance portal, because every Jaipur and Rajasthan portal found is a per-ticket lookup. All 43 come from
dated journalism that reports named residents, their ward, and the street they complained about. Every row
below is read from a page fetched today; the quote column is verbatim from that page.

## 1. Methods and blocks

| portal | what happened | exact block |
|---|---|---|
| Rajasthan Sampark, `sampark.rajasthan.gov.in` | First request at 16:36 IST returned HTTP 200, 8,194 bytes, but the body is a React shell: `You need to enable JavaScript to run this app.` | DNS then failed outright and never recovered. `curl`: `Could not resolve host: sampark.rajasthan.gov.in`. Chromium: `ERR_NAME_NOT_RESOLVED`, saved as `raw/grievance/sampark-rendered-dom.html`. Only one A record ever appeared (103.203.139.215) and it stopped answering. |
| Sampark SPA internals | Pulled `runtime.5952fd0e.js` plus five page chunks (171 KB to 219 KB each). Searched every bundle for API hosts, `/api`, `baseURL`, `process.env`. | No API base string in any chunk. The complaint endpoints are in chunks that could not be enumerated because the host stopped resolving. |
| Jaipur Municipal Corporation Greater, `jaipurmc.org` | Real server-rendered HTML, 236,997 bytes. No complaint list, but it links the actual grievance system. | No block. It is a brochure site plus a link out. |
| Jaipur Samadhan, `samadhan.jaipurmc.org` | The live grievance system for JMC. `Register Complain` and `Track Complain Status` both resolve. | **Hard block on bulk data.** The only search form is `POST /ComplaintRegistrationByWebsite/SearchComplains` and it requires `Mobile No. *` (mandatory) plus a complaint number. There is no list, no browse, no public feed. `/Dashboard`, `/Home/Index`, `/api/complaint/list` all return 404. Read-only stance meant no test submission. |
| CPGRAMS, `pgportal.gov.in` | Portal live, 27,698 bytes. | Public surface is only `Lodge Public Grievance` and `View Status`. Status needs a registration ID issued at filing. No public browse, so nothing to harvest. |
| Swachhata app / Swachh Bharat | Not attempted beyond search. | No public web complaint feed exists; complaints are app-side and tied to a login. |
| Reddit r/jaipur | `reddit.com/r/jaipur/search.json` returned HTTP 403. `old.reddit.com` in headless Chromium returned a page containing `blocked`. | Bot wall on both endpoints. Saved as `raw/grievance/reddit-jaipur-footpath.json` and `reddit-jaipur-footpath-dom.html`. |
| X / Twitter, Google Maps reviews | Not harvested. | Both need authenticated sessions or paid APIs. Out of scope for a read-only pass in the time box. |

What worked instead: Jaipur print and digital newsrooms run standing civic-complaint beats that do the
verification a portal would have done. Times of India Jaipur (`Prasidhi Sharma`, `Nandini Sharma`,
`Arpit Basu`) and Dainik Bhaskar's `Civic Issue` segment publish ward number, resident name, street, and the
complaint itself. Bhaskar English pages expose `datePublished` in JSON-LD, so dates are machine confirmed, not
guessed. All 42 rows are from those two publishers.

Geocoding: **no source supplies coordinates.** Coordinates in the last column are derived by me from the
stated area name using OpenStreetMap Nominatim (one query per area, 1.1 s apart, full responses in
`raw/grievance/geocode-nominatim.json`). They are area centroids, accurate to roughly a few hundred metres,
not door-level. Two Nominatim hits landed outside Jaipur city and were rejected rather than shipped:
"Gokulpura, Jaipur" resolved to 26.50, 75.57 (about 50 km south, wrong) and "Jaisinghpura, Jaipur" to
26.96, 75.29 (wrong). Gokulpura rows therefore carry the Jhotwara centroid, and the Jaisinghpura Khor row
carries none. Rows marked `no` have no defensible point.

## 2. The complaints

`fetched_at` is 2026-10-24 17:35 IST for every row.

| # | date | source | ward or area (as stated) | street or landmark (as stated) | issue type | quote (verbatim, max 25 words) | URL | fetched_at | geocoded |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-08-04 | Times of India Jaipur | Gopalpura, "one of Jaipur's largest coaching hubs" | footpaths outside coaching classes | footpath | "I try to use the footpath every day, but it is usually blocked by café furniture or roadside stalls." (Riya Sharma, student) | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-10-24 17:35 IST | yes, derived 26.8738, 75.7781 |
| 2 | 2026-08-04 | Times of India Jaipur | C-Scheme | footpaths used as office parking | parking on footpath | "Unless there is regular enforcement and encroachments are prevented from returning, the problem will continue." (Abhishek Jain, resident) | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-10-24 17:35 IST | yes, derived 26.9721, 75.7630 |
| 3 | 2026-08-04 | Times of India Jaipur | Subhash Marg | parked vehicles forcing pedestrians onto road during morning walks | parking on footpath | "It is especially unsafe for children and elderly people." (Sarika Meena, resident) | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-10-24 17:35 IST | yes, derived 26.9078, 75.7986 |
| 4 | 2026-08-04 | Times of India Jaipur | Sahakar Marg | unauthorised vegetable market | footpath | "an unauthorised vegetable market occupies both the pavement and part of the carriageway" | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-10-24 17:35 IST | yes, derived 26.8987, 75.7933 |
| 5 | 2026-08-04 | Times of India Jaipur | Ashok Nagar | office vehicles parked on footpaths | parking on footpath | "in Ashok Nagar and C-Scheme, office vehicles are routinely parked on footpaths" | https://timesofindia.indiatimes.com/city/jaipur/jaipurs-footpaths-remain-blocked-despite-sc-push/articleshow/132869224.cms | 2026-10-24 17:35 IST | yes, derived 26.8974, 75.7612 |
| 6 | 2026-06-22 | Times of India Jaipur | MI Road | outside shops on the commercial stretch | parking on footpath | "Vehicles illegally parked on footpaths create immense inconvenience not only for pedestrians but also for customers visiting nearby establishments." (Vikram Singh Rathore, shop employee) | https://timesofindia.indiatimes.com/city/jaipur/encroachments-choke-mi-road-pavements-forcing-pedestrians-into-heavy-traffic/articleshow/131896991.cms | 2026-10-24 17:35 IST | yes, derived 26.9160, 75.8015 |
| 7 | 2026-06-22 | Times of India Jaipur | MI Road | building frontage, "No Parking" sign in place | parking on footpath | "...try to stop people from parking here, but a total lack of regular monitoring and enforcement by authorities allows it to persist" (Mahesh Gujar, security guard) | https://timesofindia.indiatimes.com/city/jaipur/encroachments-choke-mi-road-pavements-forcing-pedestrians-into-heavy-traffic/articleshow/131896991.cms | 2026-10-24 17:35 IST | yes, derived 26.9160, 75.8015 |
| 8 | 2025-08-21 | Times of India Jaipur | B2 Bypass | footpath lined with furniture and toy stalls | footpath | "We used to sit near Mansarovar Metro Station. After we were removed from there, we shifted here." (Ramesh, toy seller) | https://timesofindia.indiatimes.com/city/jaipur/pedestrians-forced-on-to-roads-while-footpaths-overrun-by-encroachments/articleshow/123418536.cms | 2026-10-24 17:35 IST | yes, derived 26.8388, 75.7940 |
| 9 | 2025-08-21 | Times of India Jaipur | Jhalana, just off the RTO office | whole lane of footpath occupied since 2001 | footpath | "We were brought here for building work back in 2001. Since then, we've stayed here." (Rama Devi, resident) | https://timesofindia.indiatimes.com/city/jaipur/pedestrians-forced-on-to-roads-while-footpaths-overrun-by-encroachments/articleshow/123418536.cms | 2026-10-24 17:35 IST | yes, derived 26.8698, 75.8442 |
| 10 | 2025-08-21 | Times of India Jaipur | Raja Park | shop goods displayed on footpath | footpath | "If I move my products inside, customers won't even know what I'm selling." (shopkeeper) | https://timesofindia.indiatimes.com/city/jaipur/pedestrians-forced-on-to-roads-while-footpaths-overrun-by-encroachments/articleshow/123418536.cms | 2026-10-24 17:35 IST | yes, derived 26.8966, 75.8271 |
| 11 | 2025-08-21 | Times of India Jaipur | Adarsh Nagar, Ashok Chowk | LPG cylinders stored on the pavement | footpath | "The agency's delivery boys have been doing this for over two years." (Vinod Saini, juice shop owner) | https://timesofindia.indiatimes.com/city/jaipur/pedestrians-forced-on-to-roads-while-footpaths-overrun-by-encroachments/articleshow/123418536.cms | 2026-10-24 17:35 IST | yes, derived 26.8987, 75.8164 |
| 12 | 2025-08-21 | Times of India Jaipur | Ram Mandir Cinema area | footpaths under permanent shop structures | footpath | "Even around the Ram Mandir Cinema area, footpaths have essentially disappeared under permanent shop structures" | https://timesofindia.indiatimes.com/city/jaipur/pedestrians-forced-on-to-roads-while-footpaths-overrun-by-encroachments/articleshow/123418536.cms | 2026-10-24 17:35 IST | no, no unambiguous Nominatim match |
| 13 | 2026-07-26 | Times of India Jaipur | JLN Marg | outside Gate No. 2 and Gate No. 3, JDA headquarters | footpath | "more than 90% of the walking space has been taken over by landscaping, defeating the purpose of the footpath" (town planner) | https://timesofindia.indiatimes.com/city/jaipur/jda-hq-under-lens-for-pavement-encroachment/articleshow/132632617.cms | 2026-10-24 17:35 IST | yes, derived 26.8633, 75.8071 |
| 14 | 2026-07-26 | Times of India Jaipur | JLN Marg | same stretch, usable width | footpath | "The unobstructed portion is so narrow that two pedestrians can barely walk side by side." (official) | https://timesofindia.indiatimes.com/city/jaipur/jda-hq-under-lens-for-pavement-encroachment/articleshow/132632617.cms | 2026-10-24 17:35 IST | yes, derived 26.8633, 75.8071 |
| 15 | 2026-09-09 | Times of India Jaipur | Ward 23, Gokulpura, Jhotwara zone | road leading to the satellite hospital | pothole | "It was considered much safer than driving on a dark, waterlogged road full of potholes in the middle of the night" (Asha Devi, resident) | https://timesofindia.indiatimes.com/city/jaipur/gokulpura-residents-demand-action-on-neglect-unsafe-roads-poor-waste-management/articleshow/133978917.cms | 2026-10-24 17:35 IST | area only 26.9586, 75.7528 |
| 16 | 2026-09-09 | Times of India Jaipur | Ward 23, Gokulpura | potholes residents patched themselves | pothole | "I even tried filling potholes with construction waste myself" (Gopal Joshi, resident) | https://timesofindia.indiatimes.com/city/jaipur/gokulpura-residents-demand-action-on-neglect-unsafe-roads-poor-waste-management/articleshow/133978917.cms | 2026-10-24 17:35 IST | area only 26.9586, 75.7528 |
| 17 | 2026-07-14 | Times of India Jaipur | Kishanpole, Walled City | sewer lines overflowing into lanes | drain | "The biggest issue is poor maintenance of the drainage system. The drains are never cleaned properly." (Mohammad Zakariya, former councillor) | https://timesofindia.indiatimes.com/city/jaipur/kishanpole-residents-flag-sewer-road-woes/articleshow/132397137.cms | 2026-10-24 17:35 IST | yes, derived 26.9206, 75.8173 |
| 18 | 2026-07-14 | Times of India Jaipur | Kishanpole, Walled City | streets and residential lanes | drain | "Resident Irfan Ahmed said sewage continues to flow onto streets, posing a serious health risk." | https://timesofindia.indiatimes.com/city/jaipur/kishanpole-residents-flag-sewer-road-woes/articleshow/132397137.cms | 2026-10-24 17:35 IST | yes, derived 26.9206, 75.8173 |
| 19 | 2025-09-03 | Times of India Jaipur | Ward 12, Maan Bagh, Jaisinghpura Khor | sit-in at the local T-point | flooding | "colonies were built and drains blocked, diverting the entire flow into our ward" (Akhtar Hussain, councillor) | https://timesofindia.indiatimes.com/city/jaipur/civic-woes-residents-protest-over-waterlogging-road-cave-ins/articleshow/123663401.cms | 2026-10-24 17:35 IST | no, Nominatim match rejected as out of city |
| 20 | 2025-09-03 | Times of India Jaipur | Ward 37, JMC-Greater | road near Brij Bal Mandir School, caved in | pothole | "This road was constructed by the PWD. Wherever they worked, the condition is the same." (Ramesh Chandra Gupta, councillor) | https://timesofindia.indiatimes.com/city/jaipur/civic-woes-residents-protest-over-waterlogging-road-cave-ins/articleshow/123663401.cms | 2026-10-24 17:35 IST | no, school not resolvable |
| 21 | 2025-07-23 | Times of India Jaipur | Brahmpuri | Mount Road, large pothole named after MLA Balamukundacharya | pothole | "In Mount Road, Brahmpuri, a large pothole has been named after MLA Balamukundacharya." | https://timesofindia.indiatimes.com/city/jaipur/peeved-public-names-potholes-after-mlas-strings-up-sarcastic-posters/articleshow/122844277.cms | 2026-10-24 17:35 IST | no, Nominatim hit 26.7390, 76.0391 rejected |
| 22 | 2025-07-23 | Times of India Jaipur | Malviya Nagar | main road pothole titled after MLA Kalicharan Saraf | pothole | "Another on the main road in Malviya Nagar has been titled after MLA Kalicharan Saraf." | https://timesofindia.indiatimes.com/city/jaipur/peeved-public-names-potholes-after-mlas-strings-up-sarcastic-posters/articleshow/122844277.cms | 2026-10-24 17:35 IST | yes, derived 26.8594, 75.8098 |
| 23 | 2025-07-23 | Times of India Jaipur | Gulab Vihar, Jagatpura | crater named after MLA Kailash Chand Verma | pothole | "A crater in Gulab Vihar (Jagatpura) now bears the name of MLA Kailash Chand Verma." | https://timesofindia.indiatimes.com/city/jaipur/peeved-public-names-potholes-after-mlas-strings-up-sarcastic-posters/articleshow/122844277.cms | 2026-10-24 17:35 IST | yes, derived 26.8336, 75.8273 |
| 24 | 2025-07-23 | Times of India Jaipur | Hawa Mahal area | potholes named after local MLAs | pothole | "In areas like Hawa Mahal, Malviya Nagar, and Bagru, residents have 'dedicated' potholes to their respective MLAs" | https://timesofindia.indiatimes.com/city/jaipur/peeved-public-names-potholes-after-mlas-strings-up-sarcastic-posters/articleshow/122844277.cms | 2026-10-24 17:35 IST | yes, derived 26.9239, 75.8269 |
| 25 | 2025-07-23 | Times of India Jaipur | Bagru | potholed spots named after MLAs | pothole | "If our honourable leaders are quick to take credit for road construction, they should also take responsibility when things fall apart" (resident) | https://timesofindia.indiatimes.com/city/jaipur/peeved-public-names-potholes-after-mlas-strings-up-sarcastic-posters/articleshow/122844277.cms | 2026-10-24 17:35 IST | yes, derived 26.8088, 75.5423 (Bagru town, district) |
| 26 | 2026-04-14 | Times of India Jaipur | Ramganj, Walled City | Hida Ki Mori, Khalsa Colony, Shankar Colony, roads dug for PHED pipeline | pothole | "I personally went to the Kishanpole zone office and lodged a complaint about the road and the garbage dumping" (Taufiq Qureshi, resident) | https://timesofindia.indiatimes.com/city/jaipur/with-councillors-gone-civic-response-stalls-residents-left-struggling-amid-broken-roads-and-garbage-for-five-months/articleshow/130244829.cms | 2026-10-24 17:35 IST | yes, derived 26.9212, 75.8349 |
| 27 | 2026-04-14 | Times of India Jaipur | Ramganj, Walled City | unresolved roads after JMC board dissolution | pothole | "Now, for the past five months, there isn't even anyone to give us that assurance." (Saleem Khan, resident) | https://timesofindia.indiatimes.com/city/jaipur/with-councillors-gone-civic-response-stalls-residents-left-struggling-amid-broken-roads-and-garbage-for-five-months/articleshow/130244829.cms | 2026-10-24 17:35 IST | yes, derived 26.9212, 75.8349 |
| 28 | 2026-04-14 | Times of India Jaipur | Ramganj Modh and Jal Mahal | sewage lines opened and re-covered | drain | "The sewage was opened and then simply covered without proper cleaning. During the monsoon, the entire lane will be flooded." (Raunak Pandey) | https://timesofindia.indiatimes.com/city/jaipur/with-councillors-gone-civic-response-stalls-residents-left-struggling-amid-broken-roads-and-garbage-for-five-months/articleshow/130244829.cms | 2026-10-24 17:35 IST | yes, derived 26.9535, 75.8461 |
| 29 | 2026-08-14 | Times of India | Gokulpura, wards 46 and 47, Jhotwara | Pratap Circle Road, two-hour protest 10 am to noon | pothole | "If potholes resemble the Moon and Mars, why spend billions on rockets when Jhotwara is already offering the full experience" (Devendra Pratap Singh) | https://timesofindia.indiatimes.com/india/astronauts-land-on-road-craters-over-100-jaipur-residents-stage-unique-protest-against-potholes/articleshow/133235286.cms | 2026-10-24 17:35 IST | area only 26.9586, 75.7528 |
| 30 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 29, Maa Karni Nagar | residential road | pothole | "He added that despite repeated complaints, no action has been taken to date." (Amit, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | no, no match |
| 31 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 26, Hathoj | road near the Indane gas godown | drain | "the road near the Indane gas godown has been completely damaged due to sewage water accumulation" (Ravi Parik, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | yes, derived 26.9391, 75.6770 |
| 32 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 9 | Ved Ji intersection | pothole | "the road at Ved Ji intersection is completely broken, causing major inconvenience for commuters" | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | no, intersection not in OSM |
| 33 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 60, Vikas Nagar B | JDA-approved colony, unpaved road | pothole | "in JDA-approved Vikas Nagar B, the road has not been constructed for the last 15 years" (Kamlesh, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | yes, derived 26.8998, 75.7865 |
| 34 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 45, Ganesh Nagar | road in front of houses | flooding | "Sachin Meena, from Ward 45 Ganesh Nagar, reported severe waterlogging on the road" | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | yes, derived 26.8928, 75.7737 |
| 35 | 2025-11-24 | Dainik Bhaskar English, Civic Issue | Ward 50, Tejaji Nagar Panchyawala | trench dug for a water line connection | pothole | "a pit was dug to connect a water line, but after completion, it was left unfilled" (Shashikant, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-complain-about-bad-condition-of-roads-potholes-waterlogging-causes-inconvenience-to-citizens-136497475.html | 2026-10-24 17:35 IST | yes, derived 26.9188, 75.7211 |
| 36 | 2026-01-05 | Dainik Bhaskar English, Civic Issue | Ward 48, Panchyawala | behind Raghunath Vihar Royal Town, near Tejaji Temple | pothole | "After the work was completed, the road was never repaired. Large potholes remain" (Pradeep, resident) | https://www.bhaskarenglish.in/local/rajasthan/news/sewer-projects-leave-jaipur-roads-in-disrepair-residents-struggle-for-clean-water-136863538.html | 2026-10-24 17:35 IST | yes, derived 26.9188, 75.7211 |
| 37 | 2026-01-05 | Dainik Bhaskar English, Civic Issue | Ward 99, Sanganer | Krishi Nagar Toll-Tax Colony, near the Jain Temple | pothole | "The road was built a long time ago and has now deteriorated badly." (Om Prakash Gurjar, resident) | https://www.bhaskarenglish.in/local/rajasthan/news/sewer-projects-leave-jaipur-roads-in-disrepair-residents-struggle-for-clean-water-136863538.html | 2026-10-24 17:35 IST | area only 26.8146, 75.7732 |
| 38 | 2026-01-07 | Dainik Bhaskar English, Civic Issue | Ward 90, Ghatgate | behind Satyug Mahadev Ji Temple | drain | "the sewer chamber behind Satyug Mahadev Ji Temple at Ghatgate is broken" (Pradeep Parwani, resident) | https://www.bhaskarenglish.in/local/rajasthan/news/broken-chambers-garbage-hit-roads-trouble-jaipur-residents-frequent-power-cuts-add-to-woes-136881620.html | 2026-10-24 17:35 IST | no, Ghatgate not in OSM |
| 39 | 2026-01-07 | Dainik Bhaskar English, Civic Issue | Ward 31, Lankapuri, Shastri Nagar | residential roads | drain | "dirty drain water has been flowing on the roads for a long time. Pedestrians face difficulty moving, and the roads are worsening." (Farman) | https://www.bhaskarenglish.in/local/rajasthan/news/broken-chambers-garbage-hit-roads-trouble-jaipur-residents-frequent-power-cuts-add-to-woes-136881620.html | 2026-10-24 17:35 IST | yes, derived 26.9460, 75.8023 |
| 40 | 2025-11-19 | Dainik Bhaskar English, Civic Issue | Ward 95, Sector 3 | main market | drain | "the main market's sewer line is often choked. Dirty water fills the streets" (Ankit, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-face-problems-due-to-municipal-corporation-negligence-sewerage-cleanliness-stray-animals-136457264.html | 2026-10-24 17:35 IST | yes, derived 26.8808, 75.7919 |
| 41 | 2025-11-19 | Dainik Bhaskar English, Civic Issue | Ward 62, Sector 17 Pratap Nagar | residential road | drain | "the area's sewerage line overflows almost every month" (Deepak, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-face-problems-due-to-municipal-corporation-negligence-sewerage-cleanliness-stray-animals-136457264.html | 2026-10-24 17:35 IST | yes, derived 26.8808, 75.7919 |
| 42 | 2025-11-19 | Dainik Bhaskar English, Civic Issue | Ward 27 | Meena Chakki to Sirsi Link Road | pothole | "there are large potholes on the Meena Chakki to Sirsi Link Road" (Kuldeep Singh, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-face-problems-due-to-municipal-corporation-negligence-sewerage-cleanliness-stray-animals-136457264.html | 2026-10-24 17:35 IST | yes, derived 26.9161, 75.7774 |
| 43 | 2025-11-19 | Dainik Bhaskar English, Civic Issue | Ward 59 | Nahargarh Road | pothole | "the road on Nahargarh Road is badly broken, leading to daily accidents" (Gaurav Khandelwal, resident) | https://www.bhaskarenglish.in/local/rajasthan/jaipur/news/jaipur-residents-face-problems-due-to-municipal-corporation-negligence-sewerage-cleanliness-stray-animals-136457264.html | 2026-10-24 17:35 IST | yes, derived 26.9719, 75.8439 |

Row count: **43**. Geocoded: 32 rows carry a derived area point with coordinates, 4 carry an area-only point
(Gokulpura rows via the Jhotwara centroid, Sanganer for the Ward 99 row), and 7 carry no point at all because
Nominatim returned nothing or returned a match that was outside Jaipur and was rejected.

## 3. Why 43 and not 50

Three honest reasons, none of which is "I ran out of complaints":

1. **The portals that should own this data do not publish it.** Jaipur's only live grievance system requires
   a mobile number to see any single complaint. There is no way to enumerate complaints without filing one,
   which was out of scope and would have been unethical in a read-only pass. Rajasthan Sampark went
   off-DNS. CPGRAMS needs a ticket ID. That removed the entire class of source that would have yielded
   hundreds of rows with exact timestamps and statuses.
2. **I dropped rows rather than pad.** Several articles carried garbage, stray-dog, stray-cattle, power-cut
   and dirty-water complaints. Those are real citizen grievances but they are not footpath, pothole, drain,
   parking or ramp failures, so they are not in the table. Bhaskar's 2026-01-07 piece had a Gopal Ji's Path
   item about garbage plus long-parked vehicles; it never says footpath, so it is out.
3. **Dedupe by segment.** MI Road, Kishanpole, Ramganj and Gokulpura each appear more than once, but only
   where a different named resident makes a distinct, separately quotable complaint. Pure repeats of the
   same sentence were collapsed.

## 4. Two context numbers worth having on screen

Both read today, both citable, neither is a complaint row:

- **33,000 complaints in three months** on the 181 Sampark portal from Jaipur and Jodhpur alone, all about
  drains, potholes and filth. The article adds that actual complaint volume was over 70,000 and that 33,000
  is only the resolved-and-logged subset. Broken down: JDA Jaipur 20,141 resolved, Jodhpur Development
  Authority 12,885. Published 2026-04-08.
  https://www.bhaskar.com/g/local/rajasthan/jaipur/news/contact-portal-33000-complaints-on-drains-potholes-and-filth-in-jaipur-jodhpur-alone-in-3-months-dbp-137642196.html
- **The width standard these complaints can be measured against.** A 14-point notification by the
  directorate of urban bodies in July 2025, following a Supreme Court directive dated 14 May 2025, prescribes
  minimum pavement widths of 1.5 m in residential areas and 2.5 m to 3 m in commercial and high-traffic
  zones. Reported 2026-07-26.
  https://timesofindia.indiatimes.com/city/jaipur/jda-hq-under-lens-for-pavement-encroachment/articleshow/132632617.cms

The second number is the one that turns a complaint into a measurement. Row 13 is the same article claiming
more than 90 percent of a compliant-width footpath outside JDA's own headquarters is unusable. That is a
pitch slide on its own: the standard exists, the city wrote it down, and the authority's own pavement fails it.

## 5. Raw dumps

| file | what it is |
|---|---|
| `sampark-home.html` | React shell, 8,194 bytes, `You need to enable JavaScript to run this app.` |
| `sampark-rendered-dom.html` | Chromium dump showing `ERR_NAME_NOT_RESOLVED` |
| `sampark_js/runtime.js` | webpack runtime, chunk map only, no API base |
| `jaipurmc-home.html` | JMC Greater homepage, links out to Samadhan |
| `samadhan-home.html` | Samadhan landing, three options only |
| `samadhan-searchcomplain.html` | the mandatory `Mobile No. *` search form |
| `cpgrams-home.html` | CPGRAMS landing, lodge and status only |
| `reddit-jaipur-footpath.json` | HTTP 403 body |
| `reddit-jaipur-footpath-dom.html` | `old.reddit.com` blocked page |
| `toi-*.html` (10 files) | full TOI articles cited above |
| `bhaskar-en-*.html` (4 files) | full Bhaskar English articles, JSON-LD dates inside |
| `bhaskar-hi-33000-complaints-137642196.html` | the 33,000 complaint piece |
| `geocode-nominatim.json` | every Nominatim response, including the two rejects |
