"""Synthetic OSM-like graph so tests run offline and fast.

      4
      |  Cross Rd (tertiary)
  1---2---3===6---7      1-2-3 Main Rd (tertiary, drawn west->east)
      |                  3=6 highway=steps, 6-7 footway
      5
1 -> 2 is about 100 m.
"""
import os
import sys

import networkx as nx
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hroute.network import build_network  # noqa: E402

LAT0, LON0 = 26.9200, 75.8200
NODES = {1: (LON0, LAT0), 2: (LON0 + 0.001, LAT0), 3: (LON0 + 0.002, LAT0), 4: (LON0 + 0.001, LAT0 + 0.001),
         5: (LON0 + 0.001, LAT0 - 0.001), 6: (LON0 + 0.003, LAT0), 7: (LON0 + 0.004, LAT0)}
EDGES = [(1, 2, 100, "tertiary", "Main Rd"), (2, 3, 100, "tertiary", "Main Rd"),
         (4, 2, 200, "tertiary", "Cross Rd"), (2, 5, 200, "tertiary", "Cross Rd"),
         (3, 6, 300, "steps", ""), (6, 7, 400, "footway", "")]


def synthetic_graph():
    G = nx.MultiDiGraph(crs="epsg:4326")
    for n, (x, y) in NODES.items():
        G.add_node(n, x=x, y=y, street_count=2)
    for u, v, osmid, hw, name in EDGES:
        for a, b, rev in ((u, v, False), (v, u, True)):
            G.add_edge(a, b, osmid=osmid, highway=hw, name=name, oneway=False, reversed=rev, length=100.0)
    return G


@pytest.fixture()
def net():
    return build_network("synthetic", bbox=(LAT0 - 0.002, LON0 - 0.001, LAT0 + 0.002, LON0 + 0.005),
                         G=synthetic_graph())
