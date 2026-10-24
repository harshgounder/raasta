"""Footpath network builder for any Indian place.

Input: a bbox (south, west, north, east) or a place name.
Output: FootNetwork, a graph whose edges are footpath SEGMENTS, not road centrelines:

  source=osm        footways, paths, steps, pedestrian ways, service lanes, as mapped in OSM
  source=generated  sidewalk segments offset to both sides of a road where OSM has no
                    sidewalk geometry on that side (offset = road width estimate / 2 + 1 m)
  crossings         connect the two sides at intersections; crossing=generated unless an
                    OSM node at that junction carries crossing tags (crossing=osm:<type>)

Every segment: id, geometry, length_m, side (L/R relative to the parent road's drawing
direction, None if it has no parent), parent road, source, kind, evidence list.
Data: OpenStreetMap contributors, ODbL.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import math
import os
import pickle
from collections import defaultdict

import networkx as nx
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from shapely import STRtree
from shapely.geometry import LineString, MultiLineString, Point, mapping
from shapely.ops import substring

from .config import CACHE, cfg

ROAD_FILTER = ('["highway"]["area"!~"yes"]["access"!~"private"]'
               '["highway"!~"abandoned|bus_guideway|construction|motor|no|planned|platform|proposed|'
               'raceway|razed|rest_area|services|elevator|escalator|bus_stop"]["foot"!~"no"]["service"!~"private"]')
FOOT_FILTER = '["highway"~"footway|steps|path|pedestrian"]["access"!~"private"]'
SIDEWALK_FILTER = '["footway"~"sidewalk|crossing"]'

WAY_TAGS = ["sidewalk", "sidewalk:left", "sidewalk:right", "sidewalk:both", "footway", "surface",
            "smoothness", "incline", "wheelchair", "kerb", "ramp", "ramp:wheelchair", "crossing",
            "step_count", "foot", "lit", "tactile_paving", "handrail", "covered"]
NODE_TAGS = ["crossing", "kerb", "kerb:height", "barrier", "tactile_paving", "wheelchair",
             "crossing:markings", "crossing:signals"]

BAD_SURFACE = {"unpaved", "gravel", "ground", "dirt", "sand", "mud", "grass", "earth", "pebblestone",
               "fine_gravel", "rock", "unhewn_cobblestone"}
BAD_SMOOTH = {"bad", "very_bad", "horrible", "very_horrible", "impassable"}
HW_RANK = ["trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "road",
           "trunk_link", "primary_link", "secondary_link", "tertiary_link", "living_street", "service",
           "pedestrian", "footway", "path", "steps", "track", "cycleway", "bridleway", "corridor"]


def _first(v):
    if isinstance(v, (list, tuple)):
        return v[0] if v else None
    return v


def _hw(v):
    if isinstance(v, (list, tuple)):
        vs = [x for x in v if x]
        return min(vs, key=lambda x: HW_RANK.index(x) if x in HW_RANK else 99) if vs else None
    return v


def _num(v):
    v = _first(v)
    if v is None:
        return None
    try:
        s = str(v).strip().lower().replace("m", "").replace("%", "").split(";")[0].strip()
        return float(s)
    except ValueError:
        return None


def _oneway(d) -> bool:
    return _first(d.get("oneway")) in (True, "True", "yes", "true", "1")


def _longest(g):
    if g is None or g.is_empty:
        return None
    if isinstance(g, LineString):
        return g
    if isinstance(g, MultiLineString):
        return max(g.geoms, key=lambda x: x.length)
    parts = [x for x in getattr(g, "geoms", []) if isinstance(x, LineString)]
    return max(parts, key=lambda x: x.length) if parts else None


def _replace_ends(line: LineString, a, b) -> LineString:
    cs = list(line.coords)
    cs[0] = a
    cs[-1] = b
    if len(cs) == 2 and cs[0] == cs[1]:
        return LineString([a, (a[0] + 0.01, a[1])])
    return LineString(cs)


class FootNetwork:
    def __init__(self, city: str, crs, meta: dict | None = None):
        self.city = city
        self.crs = crs
        self.meta = meta or {}
        self.nodes: dict[int, tuple[float, float]] = {}
        self.segments: dict[str, dict] = {}
        self.roads: dict[str, dict] = {}
        self._gen = -1
        self._sid = 0
        self._graph = None
        self._tree = None
        self._ntree = None
        self._to_wgs = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
        self._to_proj = Transformer.from_crs("EPSG:4326", crs, always_xy=True)

    # ---------- construction helpers ----------
    def new_node(self, xy) -> int:
        nid = self._gen
        self._gen -= 1
        self.nodes[nid] = (float(xy[0]), float(xy[1]))
        return nid

    def add_segment(self, u, v, geom: LineString, *, kind, source, side=None, parent=None,
                    crossing=None, highway=None, osm=None, evidence=None, note=None) -> list[str]:
        """Add one segment, split into <= max_segment_m pieces. Returns the new ids."""
        if geom is None or geom.length <= 0.05:
            return []
        max_m = cfg()["network"]["max_segment_m"]
        n = max(1, math.ceil(geom.length / max_m))
        ids, prev = [], u
        for i in range(n):
            piece = geom if n == 1 else substring(geom, geom.length * i / n, geom.length * (i + 1) / n)
            nxt = v if i == n - 1 else self.new_node(piece.coords[-1])
            piece = _replace_ends(piece, self.nodes[prev], self.nodes[nxt])
            self._sid += 1
            sid = f"s{self._sid}"
            self.segments[sid] = {
                "id": sid, "u": prev, "v": nxt, "geom": piece, "length_m": round(piece.length, 2),
                "kind": kind, "source": source, "side": side, "parent_road": parent,
                "crossing": crossing, "highway": highway, "osm": osm or {},
                "evidence": [dict(e, id=f"{e.get('id', 'osm')}#{sid}") for e in (evidence or [])],
                "note": note,
            }
            ids.append(sid)
            prev = nxt
        self._graph = self._tree = None
        return ids

    # ---------- indexes ----------
    @property
    def graph(self) -> nx.MultiGraph:
        if self._graph is None:
            g = nx.MultiGraph()
            for nid, (x, y) in self.nodes.items():
                g.add_node(nid, x=x, y=y)
            for sid, s in self.segments.items():
                g.add_edge(s["u"], s["v"], key=sid)
            self._graph = g
        return self._graph

    def tree(self):
        if self._tree is None:
            ids = list(self.segments)
            self._tree = (STRtree([self.segments[i]["geom"] for i in ids]), ids)
        return self._tree

    def node_index(self, nodes=None):
        nodes = list(nodes if nodes is not None else self.nodes)
        return cKDTree(np.array([self.nodes[n] for n in nodes])), nodes

    def invalidate(self):
        self._graph = self._tree = self._ntree = None

    def to_xy(self, lat, lon):
        return self._to_proj.transform(lon, lat)

    def to_lonlat(self, x, y):
        return self._to_wgs.transform(x, y)

    def line_lonlat(self, geom) -> list[list[float]]:
        xs, ys = zip(*geom.coords)
        lons, lats = self._to_wgs.transform(list(xs), list(ys))
        return [[round(a, 6), round(b, 6)] for a, b in zip(lons, lats)]

    # ---------- io ----------
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = {k: v for k, v in self.__dict__.items() if not k.startswith("_") or k in ("_gen", "_sid")}
        with open(path, "wb") as f:
            pickle.dump(state, f)

    @classmethod
    def load(cls, path) -> "FootNetwork":
        with open(path, "rb") as f:
            state = pickle.load(f)
        net = cls(state["city"], state["crs"], state["meta"])
        net.__dict__.update(state)
        return net

    def stats(self) -> dict:
        by = defaultdict(int)
        length = defaultdict(float)
        for s in self.segments.values():
            by[f"{s['source']}:{s['kind']}"] += 1
            length[s["source"]] += s["length_m"]
        g = self.graph
        comps = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
        return {
            "nodes": len(self.nodes), "segments": len(self.segments),
            "by_source_kind": dict(sorted(by.items())),
            "length_km": {k: round(v / 1000, 2) for k, v in length.items()},
            "components": len(comps), "largest_component_nodes": comps[0] if comps else 0,
            "segments_with_evidence": sum(1 for s in self.segments.values() if s["evidence"]),
        }

    def to_geojson(self, tier_fn=None) -> dict:
        feats = []
        for s in self.segments.values():
            props = {k: s[k] for k in ("id", "kind", "source", "side", "crossing", "highway", "length_m", "note")}
            props["parent_road"] = s["parent_road"]
            props["evidence"] = [
                {k: e.get(k) for k in ("id", "type", "source", "status", "p_attach", "confidence",
                                       "observed_at", "permanence", "height_cm", "label")}
                for e in s["evidence"]]
            props["evidence_count"] = len(s["evidence"])
            if tier_fn:
                props["tier"] = tier_fn(s)
            if s["osm"]:
                props["osm"] = s["osm"]
            feats.append({"type": "Feature", "id": s["id"], "properties": props,
                          "geometry": {"type": "LineString", "coordinates": self.line_lonlat(s["geom"])}})
        return {"type": "FeatureCollection", "name": self.city, "meta": self.meta, "features": feats}


# ---------------------------------------------------------------- OSM download
def fetch_osm(city: str, bbox=None, place=None, refresh=False):
    """Raw OSM walk+road graph (osmnx MultiDiGraph), cached as a pickle under cache/raw/."""
    import osmnx as ox

    ox.settings.cache_folder = os.path.join(CACHE, "osmnx")
    ox.settings.use_cache = True
    ox.settings.requests_timeout = 300
    for t in WAY_TAGS:
        if t not in ox.settings.useful_tags_way:
            ox.settings.useful_tags_way = list(ox.settings.useful_tags_way) + [t]
    for t in NODE_TAGS:
        if t not in ox.settings.useful_tags_node:
            ox.settings.useful_tags_node = list(ox.settings.useful_tags_node) + [t]
    key = hashlib.sha1(repr((bbox, place)).encode()).hexdigest()[:10]
    raw = os.path.join(CACHE, "raw", f"{city}-{key}.pkl")
    if os.path.exists(raw) and not refresh:
        with open(raw, "rb") as f:
            return pickle.load(f)
    filters = [ox._overpass._get_network_filter("walk"), ROAD_FILTER, FOOT_FILTER, SIDEWALK_FILTER]
    if bbox is None:
        bbox = _place_bbox(place)
    s, w, n, e = bbox
    try:
        import requests

        requests.get(ox.settings.overpass_url.rstrip("/") + "/status", timeout=8).raise_for_status()
        G = ox.graph_from_bbox((w, s, e, n), custom_filter=filters, simplify=False, retain_all=True,
                               truncate_by_edge=True)
        how = "overpass"
    except Exception as exc:  # Overpass is often unreachable; the OSM editing API map call is the fallback
        print(f"[network] overpass failed ({type(exc).__name__}); falling back to OSM API 0.6 tiles")
        G = _graph_from_osm_api(city, bbox)
        how = "osm_api_0.6_map_tiles"
    G = ox.simplify_graph(G, node_attrs_include=["crossing", "kerb", "barrier"])
    G.graph["fetched_via"] = how
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    with open(raw, "wb") as f:
        pickle.dump(G, f)
    return G


def _place_bbox(place: str, half_km: float = 0.8):
    import osmnx as ox

    lat, lon = ox.geocode(place)
    dlat = half_km / 111.0
    dlon = half_km / (111.32 * math.cos(math.radians(lat)))
    return (lat - dlat, lon - dlon, lat + dlat, lon + dlon)


_EXCL_HW = {"abandoned", "bus_guideway", "construction", "motorway", "motorway_link", "no", "planned",
            "platform", "proposed", "raceway", "razed", "rest_area", "services", "elevator", "escalator",
            "bus_stop"}


def _keep_way(tags: dict) -> bool:
    hw = tags.get("highway")
    if not hw or hw in _EXCL_HW or tags.get("area") == "yes":
        return False
    if tags.get("access") == "private" or tags.get("foot") == "no" or tags.get("service") == "private":
        return False
    return True


def _fetch_tile(url, path):
    import requests

    if os.path.exists(path) and os.path.getsize(path) > 200:
        return path
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=180, headers={"User-Agent": "hypnexis-sc02-hackathon/0.1"})
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            if r.status_code == 400:
                return "split"
        except Exception:
            pass
    raise RuntimeError(f"OSM API tile failed: {url}")


def _graph_from_osm_api(city, bbox, tile_deg=0.005):
    """Download bbox from api.openstreetmap.org /map in tiles, keep highway ways, build with osmnx."""
    import xml.etree.ElementTree as ET
    from concurrent.futures import ThreadPoolExecutor

    import osmnx as ox

    s, w, n, e = bbox
    d = os.path.join(CACHE, "osmapi", city)
    os.makedirs(d, exist_ok=True)
    tiles = []
    lat = s
    while lat < n - 1e-9:
        lon = w
        while lon < e - 1e-9:
            tiles.append((round(lon, 6), round(lat, 6), round(min(lon + tile_deg, e), 6),
                          round(min(lat + tile_deg, n), 6)))
            lon += tile_deg
        lat += tile_deg

    def job(t):
        url = f"https://api.openstreetmap.org/api/0.6/map?bbox={t[0]},{t[1]},{t[2]},{t[3]}"
        return _fetch_tile(url, os.path.join(d, "_".join(map(str, t)) + ".osm"))

    with ThreadPoolExecutor(max_workers=3) as ex:
        paths = list(ex.map(job, tiles))
    if "split" in paths:
        raise RuntimeError("an OSM API tile had too many nodes; lower tile_deg")
    nodes, ways = {}, {}
    for p in paths:
        root = ET.parse(p).getroot()
        for nd in root.findall("node"):
            nodes[nd.get("id")] = nd
        for wy in root.findall("way"):
            tags = {t.get("k"): t.get("v") for t in wy.findall("tag")}
            if _keep_way(tags):
                ways[wy.get("id")] = wy
    need = {nd.get("ref") for wy in ways.values() for nd in wy.findall("nd")}
    out = ET.Element("osm", version="0.6", generator="hroute merge of api.openstreetmap.org map tiles")
    for nid in need:
        if nid in nodes:
            out.append(nodes[nid])
    for wy in ways.values():
        # drop refs to nodes we do not have (outside every tile)
        for nd in list(wy.findall("nd")):
            if nd.get("ref") not in nodes:
                wy.remove(nd)
        if len(wy.findall("nd")) >= 2:
            out.append(wy)
    merged = os.path.join(d, "merged.osm")
    ET.ElementTree(out).write(merged, encoding="utf-8", xml_declaration=True)
    G = ox.graph_from_xml(merged, simplify=False, retain_all=True)
    # the map call returns whole ways, which run far outside the bbox: cut back to the bbox
    G = ox.truncate.truncate_graph_bbox(G, (w, s, e, n), truncate_by_edge=True)
    return G


# ---------------------------------------------------------------- builder
def _side_tags(d, reversed_geom: bool) -> dict:
    """sidewalk tag value per side, relative to the edge's geometry direction."""
    val = {"L": None, "R": None}
    sw = _first(d.get("sidewalk"))
    if sw in ("both", "yes"):
        val = {"L": "yes", "R": "yes"}
    elif sw in ("no", "none"):
        val = {"L": "no", "R": "no"}
    elif sw == "left":
        val = {"L": "yes", "R": "no"}
    elif sw == "right":
        val = {"L": "no", "R": "yes"}
    elif sw == "separate":
        val = {"L": "separate", "R": "separate"}
    both = _first(d.get("sidewalk:both"))
    if both:
        val = {"L": both, "R": both}
    for side, key in (("L", "sidewalk:left"), ("R", "sidewalk:right")):
        if _first(d.get(key)):
            val[side] = _first(d.get(key))
    if reversed_geom:
        val = {"L": val["R"], "R": val["L"]}
    return val


def _road_offset(hw, d) -> tuple[float, str]:
    nc = cfg()["network"]
    width = _num(d.get("width"))
    how = "osm width"
    if not width:
        lanes = _num(d.get("lanes"))
        if lanes:
            width = lanes * nc["lane_width_m"]
            how = "osm lanes"
            if _first(d.get("oneway")) in (False, "False", "yes", True):
                width = max(width, 3.5)
    if not width:
        width = nc["road_width_m"].get(hw, 6)
        how = f"default for {hw}"
    off = min(nc["offset_max_m"], max(nc["offset_min_m"], width / 2 + nc["kerb_to_walk_centre_m"]))
    return off, f"road width {width:.1f} m ({how}), offset {off:.1f} m"


def _osm_evidence_for_way(hw, d) -> list[dict]:
    ev = []
    base = {"source": "osm_tag", "status": "ACCEPT", "permanence": "permanent", "observed_at": None,
            "p_attach": 1.0}
    if hw == "steps":
        if _first(d.get("ramp:wheelchair")) == "yes" or _first(d.get("ramp")) == "yes":
            ev.append({**base, "type": "kerb_ramp_present", "confidence": 0.7, "label": "OSM steps with ramp=yes"})
        else:
            ev.append({**base, "type": "steps", "confidence": 0.95, "label": "OSM highway=steps"
                       + (f", step_count={_first(d.get('step_count'))}" if d.get("step_count") else "")})
    surf = _first(d.get("surface"))
    if surf in BAD_SURFACE:
        ev.append({**base, "type": "broken_footpath", "confidence": 0.5, "label": f"OSM surface={surf}"})
    sm = _first(d.get("smoothness"))
    if sm in BAD_SMOOTH:
        ev.append({**base, "type": "broken_footpath", "confidence": 0.6, "label": f"OSM smoothness={sm}"})
    if _first(d.get("wheelchair")) == "no":
        ev.append({**base, "type": "osm_wheelchair_no", "confidence": 0.8, "label": "OSM wheelchair=no"})
    inc = _num(d.get("incline"))
    if inc is not None and abs(inc) > 0:
        ev.append({**base, "type": "steep_slope", "confidence": 0.6, "slope_pct": abs(inc),
                   "label": f"OSM incline={_first(d.get('incline'))}"})
    return ev


def _crossing_tag(ndata) -> str | None:
    if not ndata:
        return None
    hw = ndata.get("highway")
    cr = ndata.get("crossing")
    if cr:
        return f"osm:{cr}"
    if hw == "crossing":
        return "osm:crossing"
    if hw == "traffic_signals":
        return "osm:traffic_signals"
    return None


def _kerb_evidence(ndata) -> list[dict]:
    kerb = (ndata or {}).get("kerb")
    if not kerb:
        return []
    base = {"source": "osm_tag", "status": "ACCEPT", "permanence": "permanent", "observed_at": None,
            "p_attach": 1.0}
    if kerb in ("lowered", "flush", "no"):
        return [{**base, "type": "kerb_ramp_present", "confidence": 0.7, "label": f"OSM kerb={kerb}"}]
    h = _num(ndata.get("kerb:height"))
    return [{**base, "type": "missing_kerb_ramp", "confidence": 0.7,
             "height_cm": h * 100 if h is not None and h < 1 else h, "label": f"OSM kerb={kerb}"}]


def _proj_cover(road: LineString, piece) -> float:
    """length of `piece` that runs along `road` (projection), so perpendicular pieces count ~0."""
    tot = 0.0
    for g in getattr(piece, "geoms", [piece]):
        if not isinstance(g, LineString) or g.length == 0:
            continue
        a = road.project(Point(g.coords[0]))
        b = road.project(Point(g.coords[-1]))
        tot += min(abs(b - a), g.length)
    return tot


def build_network(city: str, bbox=None, place=None, G=None, refresh=False) -> FootNetwork:
    import osmnx as ox

    nc = cfg()["network"]
    if G is None:
        G = fetch_osm(city, bbox=bbox, place=place, refresh=refresh)
    Gu = ox.convert.to_undirected(G)
    Gp = ox.project_graph(Gu)
    crs = Gp.graph["crs"]
    meta = {"city": city, "bbox_swne": list(bbox) if bbox else None, "place": place,
            "built_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "crs": str(crs), "osm": "OpenStreetMap contributors, ODbL",
            "fetched_via": G.graph.get("fetched_via", "cache"),
            "osmnx": ox.__version__}
    net = FootNetwork(city, crs, meta)
    gen_set, shared_set, ped_set = set(nc["generate_on"]), set(nc["shared_street"]), set(nc["pedestrian_ways"])

    roads, peds = [], []
    for u, v, k, d in Gp.edges(keys=True, data=True):
        hw = _hw(d.get("highway"))
        if hw is None:
            continue
        pu, pv = (Gp.nodes[u]["x"], Gp.nodes[u]["y"]), (Gp.nodes[v]["x"], Gp.nodes[v]["y"])
        geom = d.get("geometry") or LineString([pu, pv])
        rev = bool(_first(d.get("reversed")))
        if Point(geom.coords[0]).distance(Point(pu)) > Point(geom.coords[0]).distance(Point(pv)):
            geom = LineString(list(geom.coords)[::-1])
            rev = not rev
        # make sure the line touches its nodes exactly
        geom = _replace_ends(geom, pu, pv)
        rec = {"u": u, "v": v, "geom": geom, "hw": hw, "d": d, "rev": rev,
               "osmid": _first(d.get("osmid")), "name": _first(d.get("name")) or ""}
        if hw in gen_set and u != v:
            roads.append(rec)
        elif hw in gen_set or hw in shared_set or hw in ped_set:
            peds.append(rec)

    for i, r in enumerate(roads):
        r["rid"] = f"r{i}"
        net.roads[r["rid"]] = {"id": r["rid"], "osm_way": r["osmid"], "name": r["name"], "highway": r["hw"],
                               "geom": r["geom"], "oneway": bool(_first(r["d"].get("oneway")))}
    road_tree = STRtree([r["geom"] for r in roads]) if roads else None

    # OSM nodes used by kept edges
    for r in roads + peds:
        for n in (r["u"], r["v"]):
            net.nodes.setdefault(n, (Gp.nodes[n]["x"], Gp.nodes[n]["y"]))

    # ---- which sides need generated sidewalks
    # roundabouts: never generate the inner (island) side
    rb_parent = {}

    def rb_find(k):
        while rb_parent.get(k, k) != k:
            k = rb_parent[k]
        return k

    for r in roads:
        r["rb"] = None
        if _first(r["d"].get("junction")) in ("roundabout", "circular"):
            rb_parent[rb_find(r["u"])] = rb_find(r["v"])
    rb_pts = defaultdict(list)
    for r in roads:
        if _first(r["d"].get("junction")) in ("roundabout", "circular"):
            r["rb"] = rb_find(r["u"])
            rb_pts[r["rb"]] += list(r["geom"].coords)
    rb_centre = {k: Point(np.mean(v, axis=0)) for k, v in rb_pts.items()}

    # traffic islands: small faces of the road network whose every bounding road is one-way
    # (roundabout centres, channelised islands, medians). Sidewalks are not generated inside them.
    islands = []
    if roads:
        from shapely.ops import polygonize, unary_union

        faces = [f for f in polygonize(unary_union([r["geom"] for r in roads])) if f.area < 6000]
        for f in faces:
            ring = f.exterior.buffer(0.75)
            bounding = [roads[j] for j in road_tree.query(ring) if roads[j]["geom"].within(ring.buffer(0.5))
                        or roads[j]["geom"].intersection(ring).length > 0.8 * roads[j]["geom"].length]
            if bounding and all(_oneway(b["d"]) for b in bounding):
                islands.append(f)
    island_tree = STRtree(islands) if islands else None

    side_lines = [p["geom"] for p in peds if p["hw"] in ("footway", "path", "pedestrian")
                  and _first(p["d"].get("footway")) != "crossing"]
    side_tree = STRtree(side_lines) if side_lines else None
    for r in roads:
        off, off_note = _road_offset(r["hw"], r["d"])
        r["off"], r["off_note"] = off, off_note
        r["tags"] = _side_tags(r["d"], r["rev"])
        r["gen"] = {}
        L = r["geom"].length
        for side, sign in (("L", 1), ("R", -1)):
            poly = r["geom"].buffer(sign * (off + nc["osm_sidewalk_search_extra_m"]), single_sided=True)
            cover = 0.0
            if side_tree is not None:
                for j in side_tree.query(poly):
                    cover += _proj_cover(r["geom"], poly.intersection(side_lines[j]))
            if L > 0 and cover / L >= nc["osm_sidewalk_coverage_min"]:
                r["gen"][side] = ("osm_sidewalk", round(cover / L, 2))
                continue
            if island_tree is not None:
                probe = _longest(r["geom"].offset_curve(sign * off))
                if probe is not None:
                    mid = probe.interpolate(0.5, normalized=True)
                    if any(islands[j].contains(mid) for j in island_tree.query(mid)):
                        r["gen"][side] = ("traffic_island", None)
                        continue
            if r["rb"] is not None:
                c = rb_centre[r["rb"]]
                pt = _longest(r["geom"].offset_curve(sign * off))
                other = _longest(r["geom"].offset_curve(-sign * off))
                if pt is not None and other is not None and \
                        pt.interpolate(0.5, normalized=True).distance(c) < other.interpolate(0.5, normalized=True).distance(c):
                    r["gen"][side] = ("roundabout_island", None)
                    continue
            if _oneway(r["d"]):
                poly2 = r["geom"].buffer(sign * nc["dual_carriageway_search_m"], single_sided=True)
                twin = 0.0
                for j in road_tree.query(poly2):
                    o = roads[j]
                    if o is r or o["osmid"] == r["osmid"] or not _oneway(o["d"]) or o["rb"] is not None:
                        continue
                    twin += _proj_cover(r["geom"], poly2.intersection(o["geom"]))
                if L > 0 and twin / L >= 0.5:
                    r["gen"][side] = ("median", round(twin / L, 2))
                    continue
            r["gen"][side] = ("generate", None)

    # ---- incidences at each road node
    inc = defaultdict(list)  # node -> [(road, end)]
    for r in roads:
        inc[r["u"]].append((r, "start"))
        inc[r["v"]].append((r, "end"))

    def crossing_node(n):
        return _crossing_tag(Gp.nodes[n]) is not None

    def trims_at(n):
        return not (len(inc[n]) == 2 and not crossing_node(n))

    # ---- offset lines + endpoint keys
    lines = {}  # (rid, side) -> LineString
    for r in roads:
        L = r["geom"].length
        for side, sign in (("L", 1), ("R", -1)):
            if r["gen"][side][0] not in ("generate", "median", "traffic_island", "roundabout_island"):
                continue
            ln = _longest(r["geom"].offset_curve(sign * r["off"]))
            if ln is None or ln.length < 0.5:
                continue
            a = min(r["off"], 0.3 * ln.length) if trims_at(r["u"]) else 0.0
            b = min(r["off"], 0.3 * ln.length) if trims_at(r["v"]) else 0.0
            if a or b:
                ln = substring(ln, a, ln.length - b)
                if not isinstance(ln, LineString) or ln.length < 0.5:
                    continue
            lines[(r["rid"], side)] = ln

    def ep_key(r, side, end):
        return (r["rid"], side, end) if (r["rid"], side) in lines else None

    def ep_xy(key):
        ln = lines[(key[0], key[1])]
        return ln.coords[0] if key[2] == "start" else ln.coords[-1]

    def away(r, end):
        """(away_left_key, away_right_key, azimuth) walking away from the node at `end`."""
        g = r["geom"]
        if end == "start":
            p0, p1 = g.coords[0], g.interpolate(min(5.0, g.length * 0.5)).coords[0]
            return ep_key(r, "L", "start"), ep_key(r, "R", "start"), math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        p0, p1 = g.coords[-1], g.interpolate(max(g.length - 5.0, g.length * 0.5)).coords[0]
        return ep_key(r, "R", "end"), ep_key(r, "L", "end"), math.atan2(p1[1] - p0[1], p1[0] - p0[0])

    parent = {}

    def find(k):
        while parent.get(k, k) != k:
            k = parent[k]
        return k

    corners, crossings = [], []  # (keyA, keyB, node, kind)
    for n, lst in inc.items():
        aw = sorted((away(r, end) + (r,) for r, end in lst), key=lambda t: t[2])
        deg = len(aw)
        if deg == 1:
            a, b = aw[0][0], aw[0][1]
            if a and b:
                crossings.append((a, b, n, "dead_end"))
            continue
        for i in range(deg):
            a, b = aw[i][0], aw[(i + 1) % deg][1]
            if not (a and b):
                continue
            pa, pb = ep_xy(a), ep_xy(b)
            if (deg == 2 and not crossing_node(n)) or math.hypot(pa[0] - pb[0], pa[1] - pb[1]) < 1.0:
                parent[find(a)] = find(b)  # same physical corner point: share one node
            else:
                corners.append((a, b, n, "corner" if deg >= 3 else "join"))
        if deg >= 3 or crossing_node(n):
            for t in (aw if deg >= 3 else aw[:1]):
                if t[0] and t[1]:
                    crossings.append((t[0], t[1], n, "junction"))

    # ---- create endpoint nodes (merged groups share one node)
    groups = defaultdict(list)
    for (rid, side) in lines:
        for end in ("start", "end"):
            k = (rid, side, end)
            groups[find(k)].append(k)
    key_node = {}
    for root, ks in groups.items():
        pts = np.array([ep_xy(k) for k in ks])
        nid = net.new_node(pts.mean(axis=0))
        for k in ks:
            key_node[k] = nid
    endpoints_at = defaultdict(set)  # road node -> generated endpoint nodes there
    for n, lst in inc.items():
        for r, end in lst:
            for side in ("L", "R"):
                k = ep_key(r, side, end)
                if k:
                    endpoints_at[n].add(key_node[k])

    # ---- generated sidewalk segments
    for r in roads:
        par = {"id": r["rid"], "osm_way": r["osmid"], "name": r["name"], "highway": r["hw"]}
        for side in ("L", "R"):
            if (r["rid"], side) not in lines:
                continue
            ln = lines[(r["rid"], side)]
            u, v = key_node[(r["rid"], side, "start")], key_node[(r["rid"], side, "end")]
            ln = _replace_ends(ln, net.nodes[u], net.nodes[v])
            tag = r["tags"][side]
            ev = []
            if tag in ("no", "none"):
                ev.append({"source": "osm_tag", "status": "ACCEPT", "type": "missing_footpath", "confidence": 0.7,
                           "permanence": "permanent", "observed_at": None, "p_attach": 1.0,
                           "label": f"OSM sidewalk tag says no footpath on this side"})
            note = r["off_note"] + (f"; OSM sidewalk={tag}" if tag else "; no OSM sidewalk tag")
            why = r["gen"][side][0]
            kind = "sidewalk"
            if why != "generate":
                # median / island side: kept only so crossings connect; walking along it is costed
                kind = "median"
                # its high per-100 m uncertainty prior (assumptions.json unknown_prior.median) does the costing
                note = (f"{why.replace('_', ' ')} side, kept so crossings connect; no footpath assumed "
                        f"(ASSUMPTION); " + note)
                ev = []
            net.add_segment(u, v, ln, kind=kind, source="generated", side=side, parent=par,
                            highway=r["hw"], osm={"sidewalk": tag} if tag else None, evidence=ev, note=note)

    # ---- corners and crossings
    for a, b, n, kind in corners:
        na, nb = key_node[a], key_node[b]
        if na == nb:
            continue
        net.add_segment(na, nb, LineString([net.nodes[na], net.nodes[nb]]), kind="corner", source="generated",
                        note=f"{kind} at OSM node {n}")
    for a, b, n, kind in crossings:
        na, nb = key_node[a], key_node[b]
        if na == nb:
            continue
        r = next(rr for rr in roads if rr["rid"] == a[0])
        tag = _crossing_tag(Gp.nodes[n])
        net.add_segment(na, nb, LineString([net.nodes[na], net.nodes[nb]]), kind="crossing", source="generated",
                        crossing=tag or "generated", highway=r["hw"],
                        parent={"id": r["rid"], "osm_way": r["osmid"], "name": r["name"], "highway": r["hw"]},
                        osm={k: Gp.nodes[n].get(k) for k in NODE_TAGS + ["highway"] if Gp.nodes[n].get(k)},
                        evidence=_kerb_evidence(Gp.nodes[n]), note=f"{kind} crossing at OSM node {n}")

    # ---- OSM pedestrian ways and shared streets
    for p in peds:
        hw = p["hw"]
        kind = "steps" if hw == "steps" else ("shared_street" if hw in shared_set or hw in gen_set else "footway")
        if _first(p["d"].get("footway")) == "crossing":
            kind = "crossing"
        par, side = None, None
        if road_tree is not None:
            mid = p["geom"].interpolate(0.5, normalized=True)
            best = None
            for j in road_tree.query(mid.buffer(15.0)):
                dd = roads[j]["geom"].distance(mid)
                if dd <= 15.0 and (best is None or dd < best[0]):
                    best = (dd, roads[j])
            if best and kind != "crossing":
                rg = best[1]["geom"]
                t = rg.project(mid)
                q0, q1 = rg.interpolate(max(0, t - 1)), rg.interpolate(min(rg.length, t + 1))
                cross = (q1.x - q0.x) * (mid.y - q0.y) - (q1.y - q0.y) * (mid.x - q0.x)
                side = "L" if cross > 0 else "R"
            if best:
                r = best[1]
                par = {"id": r["rid"], "osm_way": r["osmid"], "name": r["name"], "highway": r["hw"]}
        osm = {k: _first(p["d"].get(k)) for k in WAY_TAGS if p["d"].get(k) is not None}
        osm["highway"] = hw
        osm["osm_way"] = p["osmid"]
        cr = None
        if kind == "crossing":
            cr = f"osm:{osm.get('crossing') or 'crossing'}"
        net.add_segment(p["u"], p["v"], p["geom"], kind=kind, source="osm", side=side, parent=par,
                        crossing=cr, highway=hw, osm=osm, evidence=_osm_evidence_for_way(hw, p["d"]),
                        note=p["name"] or None)

    # ---- links: OSM nodes of kept ways that sit on a road centreline -> nearby generated corners
    ped_nodes = {p["u"] for p in peds} | {p["v"] for p in peds}
    for n in ped_nodes:
        if n not in endpoints_at:
            continue
        tag = _crossing_tag(Gp.nodes[n])
        # the endpoint nearest to where each OSM way arrives is on the same side (plain link); reaching
        # any other endpoint means crossing the carriageway, so that segment is kind=crossing
        approach = []
        for p in peds:
            if p["u"] == n:
                approach.append(p["geom"].interpolate(min(3.0, p["geom"].length / 2)))
            elif p["v"] == n:
                approach.append(p["geom"].interpolate(max(0.0, p["geom"].length - 3.0)))
        eps = list(endpoints_at[n])
        same = {min(eps, key=lambda e: Point(net.nodes[e]).distance(a)) for a in approach} if approach else set(eps)
        for e in eps:
            k = "link" if e in same else "crossing"
            net.add_segment(n, e, LineString([net.nodes[n], net.nodes[e]]), kind=k, source="generated",
                            crossing=tag or "generated", evidence=_kerb_evidence(Gp.nodes[n]),
                            note=f"OSM way meets road at node {n}" + ("" if k == "link" else "; reaching this side crosses the road"))

    # drop road-centre nodes nothing uses
    used = {s["u"] for s in net.segments.values()} | {s["v"] for s in net.segments.values()}
    net.nodes = {k: v for k, v in net.nodes.items() if k in used}
    net.invalidate()

    _snap_dangling(net, nc["dangling_snap_m"])
    _stitch_islands(net, nc["island_stitch_m"])
    net.meta["stats"] = net.stats()
    return net


def _snap_dangling(net: FootNetwork, max_m: float):
    g = net.graph
    tree, ids = net.node_index()
    added = 0
    for n in list(g.nodes):
        if g.degree(n) != 1:
            continue
        nbrs = set(g.neighbors(n))
        dists, idx = tree.query(net.nodes[n], k=6, distance_upper_bound=max_m)
        for d, i in zip(np.atleast_1d(dists), np.atleast_1d(idx)):
            if not np.isfinite(d) or i >= len(ids):
                continue
            m = ids[i]
            if m == n or m in nbrs:
                continue
            net.add_segment(n, m, LineString([net.nodes[n], net.nodes[m]]), kind="connector",
                            source="generated", note=f"dangling end snapped ({d:.1f} m)")
            added += 1
            break
    net.meta["dangling_snapped"] = added


def _stitch_islands(net: FootNetwork, max_m: float):
    g = net.graph
    comps = sorted(nx.connected_components(g), key=len, reverse=True)
    if len(comps) < 2:
        net.meta["islands_stitched"] = 0
        return
    main = set(comps[0])
    added = 0
    for comp in comps[1:]:
        if len(comp) < 2:
            continue
        mains = list(main)
        tree = cKDTree(np.array([net.nodes[m] for m in mains]))
        cn = list(comp)
        d, idx = tree.query(np.array([net.nodes[c] for c in cn]), k=1)
        j = int(np.argmin(d))
        if d[j] <= max_m:
            net.add_segment(cn[j], mains[int(idx[j])],
                            LineString([net.nodes[cn[j]], net.nodes[mains[int(idx[j])]]]), kind="connector",
                            source="generated", note=f"island stitched ({d[j]:.1f} m mapping gap)")
            main |= comp
            added += 1
    net.meta["islands_stitched"] = added
    net.invalidate()
