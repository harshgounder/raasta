// runtime config, editable after the build (no rebuild): the /analyze backend (a cloudflared tunnel URL, for example).
// precedence: ?api=URL in the address bar > the URL saved on the scan page > this file > VITE_BACKEND_URL at build time.
// REPORTS_URL: the reports service (app/reports, port 8790). precedence: ?reports=URL > this file > http://<this host>:8790
// when the page runs on localhost or a LAN address. Empty on a public host = the page says the service is not set up.
window.HYP_CONFIG = { BACKEND_URL: 'https://configuration-timeline-down-endangered.trycloudflare.com', REPORTS_URL: 'https://plastics-dangerous-cottages-metallic.trycloudflare.com' }
