# AUTHORITY CONTACTS, verified from official sites only

hermes, 2026-10-25 01:40 IST. Method: HTTPS GET with a real browser user agent, following redirects, from this
box. "Reachable" means I got a 200 tonight. "Unverified" means no official page confirmed the contact, and the
site must not print an address or a number from it.

| authority | official URL | status tonight | what I could confirm | what the site may print |
|---|---|---|---|---|
| JMC Greater and JMC Heritage (Jaipur Municipal Corporation) | https://jaipurmc.org/ | **200, reachable** | homepage publishes a "Citizen Helpline Centers" document link, and two Jaipur landline numbers appear on the homepage: 0141-2740140 and 0141-2747400, without a department label next to them | "Jaipur Municipal Corporation, jaipurmc.org, citizen helpline page" and the two numbers only with the caveat "published on the corporation homepage" |
| JMC Heritage separate domain | https://jaipurmcheritage.org/ | no response | nothing | do not print a separate Heritage domain; use jaipurmc.org |
| Jaipur Traffic Police | https://trafficpolicejaipur.gov.in/ | no response | nothing | do not print this domain |
| Rajasthan Police, Jaipur city | https://jaipurpolice.rajasthan.gov.in/ | **200, reachable** | the portal loads; no traffic-wing contact page found in the homepage links I could see | "Jaipur Police portal, jaipurpolice.rajasthan.gov.in" for parking enforcement, no phone |
| Rajasthan PWD | https://pwd.rajasthan.gov.in/ | **200, reachable** | the department portal loads; the contact page path was not found | "Rajasthan Public Works Department, pwd.rajasthan.gov.in" as the state road owner, no phone |
| Jaipur Metro Rail Corporation (JMRC) | http://jaipurmetrorail.in/ | **200 over http only**; https did not respond | official portal loads and publishes a Contact Details page at `/content/transportportal/en/metro/Aboutus/ContactDetails.html`; the numbers on it are loaded by script and I could not read them | "JMRC, jaipurmetrorail.in, Contact Details page" as the metro corridor owner, no phone |
| Jaipur Development Authority (JDA) | https://jda.rajasthan.gov.in/ | **200, reachable** | official portal loads with an About and Commissioner section; contact path not found | "JDA, jda.rajasthan.gov.in" for the JDA-maintained roads and the JLN Marg frontage named in the grievance ledger, no phone |
| Rajasthan municipal grievance route | https://rajmunicipal.com/public/feedback/ | appeared in search results with a toll free number 18005728545, **page not opened by me** | nothing first-hand | either open it and confirm the number, or print "Rajasthan municipal grievance route" with no number |
| State Commissioner for Persons with Disabilities, Rajasthan | not found tonight | nothing | nothing | do not name an office or an address; say "the state disability commissioner under the RPwD Act" and leave the contact to the escalation copy at runtime |

## What this changes in REPORT-FLOW.md

1. The only line that was already source-backed stands: the municipal corporation route via jaipurmc.org, now
   with the caveat that the two numbers are homepage numbers, not department numbers.
2. Traffic police and PWD and JDA can be named with their official domains, because the domains answered
   tonight. None of them can carry a phone number or a street address yet.
3. JMRC can be named with its official domain and its Contact Details page URL, with the note that https did
   not answer and the numbers are script-loaded.
4. The toll free number 18005728545 must be removed from anything the site prints until someone opens that
   page, because I only have it from a search snippet and this file's whole purpose is not to do that.
5. The disability commissioner line becomes structural only: named as an institution under the RPwD Act, no
   address, no number.

## The honest sentence for the report page

"The complaint goes to the office named on this card. Every contact on this site was checked against an
official website on 25 October 2026, and where we could not confirm a phone number, we did not print one."

That sentence is worth more than nine phone numbers, because a person who calls a wrong number once stops
using the product.
