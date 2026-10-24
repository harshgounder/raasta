# L3, Unstop + official event page: rules, rubric, timeline

Fetched 2026-10-24T14:44 to 14:52 IST by hermes, lane L3. Raw dumps saved in this folder:
`unstop.html` (352,182 B), `official.html` (126,658 B), plus tag-stripped `unstop.clean.txt`,
`official.clean.txt`. Method: playwright chromium `--dump-dom` (JS-rendered pages), then tag stripping.
Both pages are the organizers' own, so this file outranks any third-party summary.

## 1. The one thing that changes the plan: the real deadline is 03:00 IST, not 06:00

Official event site, `https://www.hypnexismuj.com/`, Event Schedule, verbatim:

```
DAY 02 Sun · 25 Oct
3:00 AM - 6:00 AM Round 1 Evaluation: PPT, Prototype & Presentation
6:00 AM - 6:30 AM Evaluation & Shortlisting
6:30 AM Round 2 Shortlist Announcement
6:30 AM - 10:00 AM Break, Breakfast & Project Development
10:00 AM - 11:30 AM Round 2 Mentorship
11:30 AM - 2:00 PM Round 2 Presentations
2:00 PM - 2:30 PM Final Evaluation & Deliberation
2:30 PM Top 12 Teams Announced for the Final Round
3:00 PM - 4:30 PM Final Round Presentations
4:30 PM - 6:00 PM Closing Ceremony & Winner Announcement
```

Read that carefully. Judging of PPT, prototype and presentation runs from **03:00 to 06:00**. So the
deliverables have to be judgeable at **03:00 IST on 25 Oct**, and 06:00 is the end of the judging window,
not the build deadline. Anyone planning to "finish at 06:00" is three hours late.

Day 01 schedule, same page, verbatim, and the page marks the 2:00 to 5:30 PM block as "Live now":

```
DAY 01 Sat · 24 Oct
10:00 AM - 11:30 AM Opening Ceremony
11:30 AM - 12:30 PM Problem Statement Release
12:30 PM - 2:00 PM Lunch Break
2:00 PM - 5:30 PM Round 1: Problem Solving
5:30 PM - 6:15 PM Hi-Tea Break
6:15 PM - 8:15 PM Additional Problem Statement Release & Problem Solving
8:15 PM - 9:30 PM Dinner Break
9:30 PM - 3:00 AM Mentorship & Project Development
```

Two consequences:
1. **Additional problem statements release at 6:15 PM today**, about 3.5 hours after this file was
   written. The site had a live countdown, "Opens in 03:32:09" at 14:43. The current 15 statements are
   not necessarily the final set, so the pick at 17:30 may be premature. Ask claude to confirm with the
   user whether to wait for the 6:15 PM drop before locking a statement.
2. Round 1 problem solving closed at 5:30 PM, and the working block for build is 9:30 PM to 3:00 AM, that
   is 5.5 hours, not the 12 hours a 06:00 deadline implies.

## 2. The rubric (from Unstop, which is where the team registered)

Unstop event page, `https://unstop.com/competitions/hypnexis-2026-manipal-university-mu-jaipur-1711890`,
Online PPT Submission Round section, verbatim:

```
Evaluation: Innovation, problem understanding, technical feasibility, impact, scalability, and
presentation quality.
```

That is the only scoring language published for this event. It matches the old-round rubric the fleet
already knew (innovation, problem understanding, feasibility, impact, scalability, presentation), so it
is corroborated twice rather than taken from one page.

Facts from the same Unstop page, verbatim or direct:
- `Prizes worth ₹ 10,00,000` (official site says `₹10L+`, `Prize Pool`, `Multiple tracks. Multiple winners. Details announced soon.`)
- `Registered 1,570`
- `Team Size 1 - 4 Members`
- `Eligibility Undergraduate Postgraduate Engineering Students Management Arts, Commerce, Sciences & Others School Students`
- `Registration Deadline 22 Oct 26, 06:29 PM IST`, page state `Registration Closed`
- PPT round: `01 Oct 26, 12:00 AM IST --> 22 Oct 26, 11:59 PM IST`, `This is not a shortlisting round all teams are automatically in for the offline round`
- Offline round window on Unstop: `24 Oct 26, 08:00 AM IST --> 25 Oct 26, 10:00 AM IST`
- Grand finale on Unstop: `25 Oct 26, 10:00 AM IST --> 25 Oct 26, 08:00 PM IST`
- Schema.org block: `"startDate": "2026-09-07T00:01:00+05:30"`, `"endDate": "2026-10-25T20:00:00+05:30"`, `OfflineEventAttendanceMode`
- `Updated On: 22 Oct 26, 08:43 PM IST`

Discrepancy worth knowing, not urgent: Unstop's coarse window says the offline round ends 10:00 AM on
25 Oct, while the official site shows Round 2 presentations in that slot and the event closing at 6:00 PM.
Treat the official site for behaviour (when judges appear) and Unstop for registration-level facts.

## 3. What this means for the judge lens

- Six tracks, 15 statements at release (AI 4, Web3 2, Climate 4, Health 2, Smart Cities 2, Hardware 1),
  matching `PROBLEM-STATEMENTS.md`. The site offers "Additional Problem Statements" at 6:15 PM.
- Team size up to 4 but the user is solo with the fleet, which is allowed by the rules as written.
- One statement only per the user's own rule, and the PPT round already closed, so no submission
  gymnastics are needed: the offline judging is what counts.
- Because judges are scoring presentation quality and impact alongside feasibility, the website and the
  live demo carry real weight in the rubric itself, not just as polish. That supports the user's
  santionispirits-level website strategy and it is now evidenced, not assumed.

## 4. Verbatim anchor lines, for anyone who wants to re-check

```
unstop.clean.txt:208
unstop.clean.txt:200
unstop.clean.txt:210
official.clean.txt:279
official.clean.txt:284
official.clean.txt:182
official.clean.txt:250
```

Grep recipe: `grep -n "Round 1 Evaluation" official.clean.txt` and
`grep -n "Evaluation: Innovation" unstop.clean.txt`.
