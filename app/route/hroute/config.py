"""Load assumptions.json and expose shared constants."""
from __future__ import annotations

import json
import os
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # app/route
CACHE = os.path.join(ROOT, "cache")
SITE_DATA = os.path.abspath(os.path.join(ROOT, "..", "site-data"))
ASSUMPTIONS = os.path.join(HERE, "assumptions.json")

BARRIER_TYPES = [
    "missing_kerb_ramp", "steps", "broken_footpath", "missing_footpath", "pole_obstruction",
    "parked_vehicle", "pothole", "open_drain", "vendor", "waterlogging",
]
EXTRA_TYPES = ["steep_slope"]
PROFILES = [
    "manual_wheelchair", "power_wheelchair", "walker_elderly", "pram", "crutches",
    "low_vision", "default_walker",
]


@lru_cache(maxsize=1)
def cfg() -> dict:
    with open(ASSUMPTIONS) as f:
        return json.load(f)


def clear_types() -> set[str]:
    return set(cfg()["clear_types"])


def photo_sources() -> set[str]:
    return set(cfg()["source_tiers"]["photo"])


def evidence_sources() -> set[str]:
    """sources that count as ground evidence: our photos plus volunteer labels (Project Sidewalk)."""
    st = cfg()["source_tiers"]
    return set(st["photo"]) | set(st["volunteer_label"])


def source_class(src: str | None) -> str:
    for k, v in cfg()["source_tiers"].items():
        if not k.startswith("_") and src in v:
            return k
    return "other"
