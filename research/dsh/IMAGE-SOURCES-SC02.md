# Image-source universe for SC-02 (dsh, 16:50 IST)

Every kind of place that holds Indian street-level or street-adjacent imagery, with the GET route
tested today, the licence, and the honest result. A kind with no working route is marked BLOCKED
rather than left implied.

## Street-level imagery

| kind | instance and GET route | licence | tested 2026-10-24 |
|---|---|---|---|
| open street-level | Mapillary Graph API `https://graph.mapillary.com/images?bbox=W,S,E,N&access_token=TOKEN` | CC BY-SA | **BLOCKED without token**: HTTP 500 with no token. A free token unlocks it in minutes. |
| open street-level | KartaView `https://api.openstreetcam.org/2.0/photo/?lat=..&lng=..&radius=..` | CC BY-SA 4.0 | **EMPTY** response from this box, both 1.0 and 2.0 endpoints. Needs checking with a browser. |
| commercial | Google Street View Static `https://maps.googleapis.com/maps/api/streetview?location=..&key=..` | Google terms, no caching or redistribution | Needs key and money, and the policy forbids storing imagery. Avoid. |
| commercial India | Mappls (MapmyIndia) APIs | commercial | Needs key. Not tested. |
| free geotagged photos | Wikimedia Commons geosearch `https://commons.wikimedia.org/w/api.php?action=query&generator=geosearch&ggscoord=LAT%7CLON&ggsradius=250&ggsnamespace=6&prop=imageinfo&iiprop=url%7Cextmetadata` | per file, mostly CC BY-SA or public domain | **WORKS**. 12 hits at Hawa Mahal, all with URLs. |
| free geotagged photos | Flickr API `flickr.photos.search` with `license=1,2,4,5` | per file CC | Needs API key. Without key: error 100. |
| video frames | YouTube walking tours via `yt-dlp --flat-playlist` and frame extraction | standard YouTube licence is not reusable; only CC-BY or permission | **yt-dlp WORKS** (found a 21-minute Jaipur walking tour, id xy7BYZ4vGjw). Frames for internal analysis only unless the licence is clear. |
| citizen complaints | Swachhata app, BBMP Sahaaya, municipal grievance portals, news photos | public but terms vary; news photos are fair-use risk | Not tested tonight. Public complaints often include a photo and a location. |
| social | X and Reddit civic complaints | platform terms | X API is paid; Reddit API possible. Photos are not openly licensed. |

## Aerial, satellite, map geometry

| kind | instance and GET route | licence | tested |
|---|---|---|---|
| map geometry | OpenStreetMap API `https://api.openstreetmap.org/api/0.6/map?bbox=W,S,E,N` | ODbL | **WORKS**: 1.6 MB, 6,172 nodes, 1,206 ways around Hawa Mahal, including 67 footways and 6 stair ways. |
| satellite | Bhuvan (ISRO) `https://bhuvan.nrsc.gov.in` | public, check terms | Reachable, HTTP 302. No API test yet. |
| satellite | Copernicus Sentinel-2 via STAC | free, open | 10 m pixels, too coarse for a footpath, fine for context. |
| aerial | none available tonight | | |

## Working recommendation

1. Commons geosearch along the chosen route, licence recorded per file.
2. OSM API geometry for the graph, ODbL attribution.
3. User's own phone photos if they can take them, the cleanest licence and the most local evidence.
4. YouTube frames only with a clear licence, otherwise skip and say why.
5. Mapillary if somebody makes a free token in the next hour, because it is the only source with
   dense, modern Indian street coverage and heading metadata.
