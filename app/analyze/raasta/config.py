"""Shared constants for /analyze: prompts, class families, thresholds, assumptions.

Every assumption that changes a number in a receipt lives here, so the receipt can quote it.
"""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # app/analyze
WEIGHTS = os.path.join(ROOT, "weights")
APP = os.path.dirname(ROOT)                      # app/
ROUTE_DIR = os.path.join(APP, "route")

# prompt -> class_family. Families are the barrier types of the routing service
# (app/route/hroute/config.py BARRIER_TYPES + clear type kerb_ramp_present), so a receipt
# detection can be handed to /barriers without renaming.
PROMPTS: dict[str, str] = {
    "stairs": "steps",
    "step": "steps",
    "curb without ramp": "missing_kerb_ramp",
    "curb ramp": "kerb_ramp_present",
    "broken pavement": "broken_footpath",
    "missing sidewalk": "missing_footpath",
    "pole on sidewalk": "pole_obstruction",
    "parked motorcycle on sidewalk": "parked_vehicle",
    "parked car on sidewalk": "parked_vehicle",
    # Indian extras
    "open drain": "open_drain",
    "pothole": "pothole",
    "street vendor cart": "vendor",
    "electric box": "pole_obstruction",
    "bollard": "pole_obstruction",
}
PROMPT_LIST = list(PROMPTS)

# Families that may be confused for each other by open-vocabulary detectors. Agreement across
# families in the same group still counts (IoU rule unchanged); the receipt then names both.
AGREE_GROUPS = [
    {"steps", "missing_kerb_ramp", "kerb_ramp_present"},   # level changes: a kerb is a step
    {"broken_footpath", "pothole", "open_drain"},          # surface defects
]

PS_CORE_FAMILIES = ["missing_kerb_ramp", "steps", "broken_footpath", "missing_footpath",
                    "pole_obstruction", "parked_vehicle"]
LEVEL_CHANGE = {"steps", "missing_kerb_ramp", "kerb_ramp_present"}


def same_family(a: str, b: str) -> bool:
    if a == b:
        return True
    return any(a in g and b in g for g in AGREE_GROUPS)


# detection thresholds (proposal level, deliberately loose; agreement does the filtering)
A_CONF = float(os.environ.get("ANALYZE_A_CONF", 0.08))
B_CONF = float(os.environ.get("ANALYZE_B_CONF", 0.10))
IOU_AGREE = 0.30
# single-model hits below these scores are REJECT (listed, not shown to people)
A_SINGLE_MIN = 0.25
B_SINGLE_MIN = 0.25
MAX_DETS_PER_MODEL = 40

# measurement assumptions
CAM_HEIGHT_M = (1.2, 1.7)            # hand-held / chest-to-eye height of a pedestrian camera
DEFAULT_HFOV_DEG = 65.0              # used when EXIF has no 35 mm focal length (phone main camera ~ 65-75)
HFOV_RANGE_DEG = (55.0, 80.0)        # spread used for the error of route 1 when FOV is assumed
KERB_PLAUSIBLE_CM = (3.0, 60.0)      # one riser or kerb; outside = route rejected
HEIGHT_ACCEPT_MAX_ERR_CM = 6.0
HEIGHT_ACCEPT_MAX_REL = 0.40

DEPTH_MODEL_ID = "depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf"
B_MODEL_ID = "google/owlv2-base-patch16-ensemble"
SEG_MODEL_ID = "malra/segformer-b0-finetuned-segments-sidewalk-4"
_LOCAL = {SEG_MODEL_ID: os.path.join(WEIGHTS, "segformer-sidewalk"),
          DEPTH_MODEL_ID: os.path.join(WEIGHTS, "da2-metric-outdoor-small"),
          B_MODEL_ID: os.path.join(WEIGHTS, "owlv2-base-patch16-ensemble")}


def resolve(repo_id: str) -> str:
    """Local folder (tools/pfetch.py) if complete, else the HF cache, else raise fast (no network
    download at request time: this network stalls HF downloads)."""
    loc = _LOCAL.get(repo_id)
    if loc and any(os.path.exists(os.path.join(loc, w)) for w in ("model.safetensors", "pytorch_model.bin")) and os.path.exists(os.path.join(loc, "preprocessor_config.json")):
        return loc
    try:
        from huggingface_hub import try_to_load_from_cache
        p = try_to_load_from_cache(repo_id, "model.safetensors")
        if isinstance(p, str) and os.path.exists(p):
            return repo_id
    except Exception:  # noqa: BLE001
        pass
    raise FileNotFoundError(f"weights for {repo_id} not downloaded yet (run tools/pfetch.py {repo_id} {loc})")


DEPTH_MODEL = os.environ.get("ANALYZE_DEPTH_MODEL", DEPTH_MODEL_ID)
B_MODEL = os.environ.get("ANALYZE_B_MODEL", B_MODEL_ID)
SEG_MODEL = os.environ.get("ANALYZE_SEG_MODEL", SEG_MODEL_ID)
# segments.ai sidewalk label ids (model config id2label)
SEG_FOOTPATH = {2, 7, 5}        # flat-sidewalk, flat-curb, flat-parkingdriveway
SEG_ROAD = {1, 3, 4}            # flat-road, flat-crosswalk, flat-cyclinglane
ON_FOOTPATH_FAMILIES = {"parked_vehicle", "pole_obstruction", "vendor"}
A_WEIGHTS = os.path.join(WEIGHTS, "yoloe-11s-seg.pt")
A_TEXT_PE = os.path.join(WEIGHTS, "yoloe-11s-text-pe.pt")

# app/route/README.md: `uvicorn hroute.api:app --port 8020`, POST /barriers {city, records:[...]}
ROUTE_URL = os.environ.get("ROUTE_URL", "http://127.0.0.1:8020/barriers")

JUDGE_ENABLED = os.environ.get("ANALYZE_JUDGE", "1") != "0"
JUDGE_MAX_CALLS = int(os.environ.get("ANALYZE_JUDGE_MAX", 6))
# model ids checked live on 2026-10-24 (openrouter /models lists gemma-4-31b-it:free with image input;
# NVIDIA /v1/models lists meta/llama-3.2-90b-vision-instruct)
OPENROUTER_MODELS = os.environ.get("JUDGE_OPENROUTER_MODELS", "google/gemma-4-31b-it:free,qwen/qwen3.7-flash,google/gemma-3-4b-it").split(",")
NVIDIA_MODELS = os.environ.get("JUDGE_NVIDIA_MODELS", "meta/llama-3.2-11b-vision-instruct,google/gemma-4-31b-it").split(",")
JUDGE_TIMEOUT_S = float(os.environ.get("JUDGE_TIMEOUT_S", 6))    # one call
JUDGE_BUDGET_S = float(os.environ.get("JUDGE_BUDGET_S", 8))      # all judge calls for one image
# 2026-10-24 sanity test: llama-3.2-11b-vision said "visible" to stairs and an open drain on a shop
# roof crop, so a "visible" answer does not promote ABSTAIN -> ACCEPT unless this is set to 1.
JUDGE_CAN_ACCEPT = os.environ.get("JUDGE_CAN_ACCEPT", "0") == "1"
JUDGE_BREAKER_FAILS = int(os.environ.get("JUDGE_BREAKER_FAILS", 2))
JUDGE_COOLDOWN_S = float(os.environ.get("JUDGE_COOLDOWN_S", 600))

# Decision policy per C6 class (raasta/policy.py). Default = the v2 behaviour: two detectors must
# agree; an agreement on the carriageway is ABSTAIN. tools/calibrate.py overwrites calib/policy.json,
# which is loaded here when present (chosen on the C6 dev split only, see CALIBRATION.md).
POLICY: dict = {"_other": {"context_downgrade": True}}
# ANALYZE_POLICY: "calibrated" (guarded, default) | "naive" (calib/naive-v1, area classes accept single-B
# hits; test F1 for that class equals saying yes on every image) | "default" (two detectors only)
_POLICY_FILE = {"calibrated": os.path.join(ROOT, "calib", "policy.json"),
                "naive": os.path.join(ROOT, "calib", "naive-v1", "policy.json")}.get(
    os.environ.get("ANALYZE_POLICY", "calibrated"), "")
if _POLICY_FILE and os.path.exists(_POLICY_FILE):
    import json as _json
    with open(_POLICY_FILE) as _f:
        POLICY = _json.load(_f)["policy"]
