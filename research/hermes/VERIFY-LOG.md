# L2 verification log, dead-link sweep

Swept 2026-10-24 ~15:20 IST over every URL in the eight L2 files (AI-01..04, W3-01, W3-02, HM-01,
HM-02): 173 unique URLs, fetched with curl, Chrome 141 UA, 12 s timeout, 10 in parallel.

Result: 168 returned 200. Five did not, and each needs the label it gets below before anyone quotes it.

| code | URL | reading |
|---|---|---|
| 403 | https://cacm.acm.org/blogcacm/if-you-think-you-can-do-real-world-text-to-sql/ | bot wall, the page exists, the claim attached to it (Beaver benchmark results) was also read from https://beaverbench.github.io/ which returns 200, so the number stands on the primary source |
| 000 | https://deepfake-demo.aisec.fraunhofer.de/ | no DNS or no route, treat as DEAD, do not cite |
| 000 | http://117.72.46.148:9080 | bare Chinese server IP, no route from here, treat as DEAD and do not cite, if the tool matters find its repo instead |
| 403 | https://pubs.acs.org/doi/abs/10.1021/acs.jcim.5c02645 | publisher bot wall, paper exists, citation usable if the title and DOI are quoted, not as an opened page |
| 503 | https://www.asvspoof.org/ | temporary, the site was up earlier in the session, retry before the pitch or cite the challenge paper instead |

Rule applied elsewhere in these files: a row is VERIFIED only when the page was opened this session. The
two 000 links are the only rows that should be demoted to UNVERIFIED or removed by whoever merges wave 1.
