<!-- run id: trun_3b693d434bb94e6d87726663222684a7 -->
<!-- processor: ultra -->
<!-- fetched: 2026-10-24 16:38 IST via mcp__parallel-task__getResultMarkdown, body below is verbatim -->

# Task Run Results

**Run ID:** trun_3b693d434bb94e6d87726663222684a7
**Status:** ✅ completed
**Processor:** ultra
**Created:** 2026-10-24T10:25:07.601090Z
**Modified:** 2026-10-24T10:32:06.588254Z

## Output

# Build an Evidence-First Campus Accessibility Demo Tonight

## Executive Summary

**Recommendation:** Build a small, evidence-backed routing application, not a live autonomous accessibility assessor. Precompute detections, manually resolve ambiguous sidewalk assignments, and keep reconstruction off the critical path. The browser should make three things obvious: **what was observed, where it probably belongs, and how it changes this user's route**.

- **Choose A Lightweight Core**: Use YOLO-World-S plus a second, separately run detector, with a small OSM-derived graph. The original YOLO-World reports **35.4 AP at 52 FPS on a V100**, not on a GTX 1650 and not on sidewalk accessibility -> benchmark your actual machine before promising live inference. [37]
- **Separate Objects From Accessibility Claims**: Grounding DINO supplies text-conditioned boxes; SAM 2 supplies prompted masks. Neither combination, by itself, establishes whether a wheelchair can pass -> add footpath context, passage-width review, and an explicit unknown state. [8][5]
- **Do Not Transfer Accuracy Across Tasks**: RampNet reports **0.9236 AP** for a specifically trained curb-ramp detector. That is useful evidence that specialized detection works, not a benchmark for your seven zero-shot Jaipur labels -> conduct a small, local error audit. [13]
- **Treat Centimetres As Estimates**: Depth Anything V2 has separate relative and metric models; Metric3D's reported KITTI errors are scene-depth metrics, not curb-height certification -> display estimated height only with calibration and uncertainty. [3][23][29]
- **Make Wrong-Side Assignment Visible**: In your assumed **5-15 m GPS-error** setting, nearest-edge snapping alone cannot reliably distinguish opposite sidewalks -> retain candidate edges and offer one-click human reassignment.
- **Use Personalized Constraints, Not One Accessibility Score**: AccessMap exposes slope, curb, stair, and other preferences; Project Sidewalk's AccessScore is an experimental aggregate sigmoid score -> use the former idea for routing and the latter for overview visualization. [12][34]
- **Keep Splats Optional**: Stock Splatfacto documents about **6 GB** for its default model and **12 GB** for its bigger model -> a **4 GB** machine is not a dependable stock-training target. Use another GPU or fall back to a photographic walkthrough. [28]
- **Animate Decisions, Not Just Lines**: deck.gl's TripsLayer already provides a timestamp-driven playhead and trail -> compare shortest and profile-aware routes while opening the actual evidence behind each detour. [2]

All thresholds, sample sizes, and time allocations proposed below are **implementation choices**, not measured performance claims. This is a demonstration of decision support, not a guarantee that a route is safe or accessible.

## 1. Detection: Two Models, Context, And Human Abstention

### Which pipeline to use tonight

| Pipeline | Best role | Important limitation | GTX 1650 / CPU decision |
|---|---|---|---|
| **YOLO-World-S / World-v2** | First-pass boxes for stairs, poles, motorcycles, curbs, ramps | An object label does not establish obstruction, traversable width, or ramp absence | Start here; batch size 1; cache text vocabulary; benchmark CUDA and CPU |
| **Grounding DINO-T + SAM 2.1 Tiny** | Strong alternative proposals followed by useful evidence masks | SAM is not an independent semantic detector; segmentation adds work and installation risk | Run sequentially, not simultaneously; use boxes if SAM installation fails |
| **OWLv2 Base** | A differently trained second detector for agreement/disagreement | Long relational descriptions and tiny distant features still require review | Straightforward Transformers fallback; run after unloading the first model |
| **Florence-2 Base** | Compact region captions, phrase grounding, alternate evidence extraction | Its prompt-driven tasks are not a guarantee of arbitrary barrier reasoning | Reasonable small-model experiment; not essential to the routing loop |
| **Qwen2.5-VL-3B** | Crop-plus-context verifier: visible passage, uncertainty, contradictory evidence | Generative answers can invent details; quantization and image tokens add complexity | Prefer remote inference or optional offline processing, not a required 4 GB resident model |

The official interfaces support these roles: Grounding DINO's `predict` returns boxes, scores and phrases; SAM 2 exposes `set_image`/`predict`; OWLv2 supports text-conditioned detection; Florence-2 Base is approximately **0.23B parameters** and supports detection, phrase grounding and captions. Qwen's **3B** variant supports visual localization and configurable image resolution. [8][5][15][27][20]

**My default:** YOLO-World-S plus OWLv2 Base for the easiest installation, or YOLO-World-S plus Grounding DINO-T if DINO already works. Treat these as *different detectors*, not statistically independent instruments. Shared training distributions and visual failure modes mean agreement can still be wrong.

### Explicit treatment of all seven requested labels

| Requested label | Detection proposal | Accessibility decision that must follow |
|---|---|---|
| Stairs | `stairs`, `staircase` | Associate with the traversed connector; determine whether an alternative ramp exists |
| Steps | `single step`, `stair step` | Inspect a close crop; distinguish a traversal lip from decorative edges/shadows |
| Kerb without ramp | Detect curb and crossing approach separately | **Do not equate no ramp detection with no ramp**; inspect the complete crossing interface |
| Curb ramp | `curb ramp`, `kerb ramp`, `sloped sidewalk entrance` | Confirm connection, landing, obstruction and usable width; ramp presence alone is insufficient |
| Broken pavement | `broken pavement`, `damaged sidewalk`, `uneven paving stones` | Verify surface condition and severity from evidence; retain unknown when detail is inadequate |
| Pole in footpath | `pole`, then footpath context | Use its ground-contact location and remaining passage, not bounding-box overlap alone |
| Parked motorbike on footpath | `motorcycle`, `motorbike`, then footpath context | Determine whether it obstructs passage; keep it time-dependent rather than permanent infrastructure |

This decomposition is the key design decision: **objects, spatial relationships, and missing infrastructure are different inference problems**.

A minimal first detector uses the documented Ultralytics API. [32]

```python
import torch
from ultralytics import YOLOWorld

classes = [
    "stairs", "single step", "curb", "curb ramp",
    "broken pavement", "pole", "motorcycle"
]
device = 0 if torch.cuda.is_available() else "cpu"
model = YOLOWorld("yolov8s-worldv2.pt")
model.set_classes(classes)

# Deliberately permissive proposal threshold; not a safety confidence.
r = model.predict(
    "photo.jpg", imgsz=640, conf=0.12, iou=0.5,
    device=device, verbose=False
)[0]
proposals = [
    {"label": classes[int(cls)], "box_xyxy": box, "raw_score": score}
    for box, score, cls in zip(
        r.boxes.xyxy.cpu().tolist(),
        r.boxes.conf.cpu().tolist(),
        r.boxes.cls.cpu().tolist()
    )
]
```

For OWLv2, the documented high-level entry point is: [15]

```python
from transformers import pipeline
second_detector = pipeline(
    "zero-shot-object-detection",
    model="google/owlv2-base-patch16-ensemble",
    device=device if device != "cpu" else -1
)
second = second_detector("photo.jpg", candidate_labels=classes)
```

Normalize synonyms and coordinate conventions before matching. For DINO-to-SAM, convert DINO's returned boxes into the coordinate convention SAM expects; use the box as a prompt, then extract the contact region. Do not count the resulting mask as a second semantic vote.

### Accuracy, confidence, and the mandatory unsure state

**The useful published case study is RampNet.** It constructs more than **210,000** annotated panoramas from government curb-ramp locations and trains a modified ConvNeXt V2 detector. Its generated dataset reports **94.0% precision / 92.5% recall**, while the trained detector reports **0.9236 AP**. Those are different measurements, not interchangeable accuracy numbers. [13]

The contrast matters: this is supervised curb-ramp detection with a dedicated data pipeline, not evidence that a zero-shot prompt identifies every missing ramp, broken slab, or blocked passage in Jaipur. I did not find a directly comparable evaluation of these six model families on all seven requested labels under Jaipur-like conditions.

Use a transparent **agreement score**, explicitly not a probability. For example:

```python
# Design sketch: calibrated_score is optional and requires local labels.
# Raw detector scores from different models are NOT directly comparable.
match = same_semantic_class and box_iou >= 0.30
agreement_score = (
    0.5 * float(match)
    + 0.3 * footpath_context_score
    + 0.2 * independent_view_support
)
state = "candidate" if match and context_is_clear else "unsure"
# Only a reviewer action changes state to "verified".
```

Keep a single-model detection as `unsure`, rather than deleting it. Two models missing an obstacle is not evidence of clearance. Ask the VLM to return `visible`, `not_visible`, or `cannot_determine`, cite the relevant crop, and never infer dimensions from prose.

For a local audit, manually label a proposed **40-60 photos**, including negatives, shadows, tree roots, partial ramps and distant obstacles. Record per-class precision, recall, disagreement rate, and the fraction routed to review; hold some images out from prompt tuning. The decision-ready outcome is not a flattering global score, but knowing which classes need mandatory human review.

### Speed and memory: measure, do not transfer V100 FPS

The YOLO-World paper's **52 FPS / V100** result and SAM 2.1 Tiny's **91.2 FPS / A100** result are not GTX 1650 or CPU measurements. The cited official documentation does not establish end-to-end latency for your exact models, prompts, resolution and target hardware. [37][5]

Use this small benchmark around each already-loaded inference function:

```python
import time, numpy as np, torch

def bench(infer, n=10):
    infer()  # Warm-up; measure download/load separately.
    cuda = torch.cuda.is_available()
    if cuda:
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
    samples = []
    for _ in range(n):
        start = time.perf_counter()
        infer()
        if cuda:
            torch.cuda.synchronize()
        samples.append(time.perf_counter() - start)
    return {
        "p50_s": float(np.percentile(samples, 50)),
        "p95_s": float(np.percentile(samples, 95)),
        "peak_torch_GB": torch.cuda.max_memory_allocated()/1e9 if cuda else None
    }
```

Choose a product budget, for example **2 seconds per first-pass image on GPU or 10 seconds on CPU**, and switch to precomputation if exceeded. These are acceptance deadlines, **not predicted speeds**. Run models in separate processes to recover memory; PyTorch's peak allocation also excludes some system/display overhead.

A 3B model's language weights alone are roughly **6 GB at two bytes per parameter**, before vision activations and caches. Quantization may help but does not make a full Qwen pipeline a guaranteed 4 GB fit. Avoid copying BF16/FlashAttention examples blindly: the standard FlashAttention-2 CUDA path documents Ampere/Ada/Hopper support, with a separate Turing implementation and BF16 requiring newer supported architectures. [20][40]

**Decision:** Make asynchronous, cached inference the default. A smooth browser does not require real-time model inference.

## 2. Metric Depth: Estimate A Kerb, Do Not Certify It

| Model | Useful capability | Evidence and limitation | Tonight's choice |
|---|---|---|---|
| **Depth Anything V2 Metric Small** | Simple metric depth in metres | Separate indoor Hypersim and outdoor Virtual KITTI 2 checkpoints; Small is **24.8M parameters** | First experiment on the 4 GB machine |
| **Metric3D v2** | Metric depth plus surface normals, using camera information | Paper's ViT-Large reports KITTI **AbsRel 0.052**, delta1 **0.974**; these are not Small-model or curb-height results | Useful if calibrated intrinsics and its preprocessing already work |
| **UniDepth / UniDepthV2** | Metric depth, 3D points and camera estimation; V2 offers confidence output | Repository reports V2 KITTI delta1 **98.9** in its table; not a centimetre-height confidence guarantee | Good alternative, especially for points/camera output; benchmark memory first |

These figures come from different evaluation setups and should not be ranked as an apples-to-apples curb benchmark. [23][29][6]

The first trap is loading the normal relative-depth checkpoint and interpreting its colors as metres. The metric codebase returns an `HxW` array in metres and uses different maximum-depth settings: **20 m indoors, 80 m outdoors**. [3][23]

```python
# Run from the repository's metric_depth directory, not its relative-depth tree.
import cv2, torch
from depth_anything_v2.dpt import DepthAnythingV2

model = DepthAnythingV2(
    encoder="vits", features=64,
    out_channels=[48, 96, 192, 384], max_depth=80
)
model.load_state_dict(torch.load(
    "checkpoints/depth_anything_v2_metric_vkitti_vits.pth",
    map_location="cpu"
))
model = model.to("cuda" if torch.cuda.is_available() else "cpu").eval()
with torch.inference_mode():
    depth_m = model.infer_image(cv2.imread("kerb.jpg"))
```

The model/checkpoint pattern and metre output follow the official metric implementation. [23]

**Metric3D is the instructive case study.** Its zero-shot evaluation uses supplied focal lengths and no scale alignment; the paper emphasizes the importance of camera intrinsics for metric estimation. That is materially different from applying a model to a resized, cropped phone image with guessed focal length. [29]

Its Hub entry point includes `metric3d_vit_small`, and inference can return depth and normals. However, the full resize, padding, canonical-camera and focal-length rescaling pipeline is part of the method; copying only the model-loading line is not enough. The published table cited above concerns larger variants. [9]

For height, reconstruct local 3D points and compare surfaces near the curb lip:

```python
# D is axial depth, K matches the oriented/resized image.
ray = np.linalg.inv(K) @ np.array([u, v, 1.0])
P_camera = D[v, u] * ray

# Fit a lower-surface plane n dot P + b = 0 with robust estimation.
# Normalize n; select upper-surface points near the same curb interface.
height_cm = 100 * abs(np.median(P_upper @ n + b))
```

This is a proposed geometric estimator, not a validated curb-measurement algorithm. Do **not** subtract two camera-range values and call the difference vertical height. Check whether your chosen output represents axial depth or radial range; use its documented point output where available. UniDepth exposes both camera-coordinate points and intrinsics. [6]

Reject or downgrade estimates when the curb is distant, masked by a vehicle, blurred, reflective, strongly sloped, or represented by too few pixels. Plane-fit residuals alone miss model scale bias. For the demonstration, photograph one known-size target or physically measure the featured curb, retain both values separately, and render uncalibrated estimates as **"height unknown"**, not a confident number.

**Decision:** Use depth for localization and visual explanation first. Use measured height, not monocular centimetres alone, for a hard wheelchair exclusion.

## 3. Geolocation: Project The Obstacle, Then Match Its Footpath

### Capture a pose sidecar, not just an image

Store the original image plus:

```text
image_id, observed_at, lat, lon, horizontal_accuracy_m,
heading_deg, heading_reference, pitch, roll,
image_width, image_height, exif_orientation,
camera_intrinsics, source, source_image_id, license
```

Treat missing values as missing. EXIF distinguishes `GPSImgDirectionRef` of **T = true north** and **M = magnetic north**; `GPSTrack` is a separate field and must not be substituted for camera direction. [24] A phone's travel direction or generic device heading is not automatically the optical-axis orientation needed by the projection. Use a capture flow that records camera-aligned orientation, or let the reviewer set a bearing.

For Mapillary, useful fields include `computed_geometry`, `computed_compass_angle`, `compass_angle`, `captured_at`, and thumbnail URLs. The computed values are the post-processing location and heading, not guaranteed surveyed ground truth. [11]

```bash
curl -G "https://graph.mapillary.com/IMAGE_ID" \
  --data-urlencode "access_token=$MAPILLARY_TOKEN" \
  --data-urlencode "fields=id,geometry,computed_geometry,compass_angle,computed_compass_angle,captured_at,thumb_2048_url"
```

Use a thumbnail for review and retain its source ID. Do not assume coverage exists around the selected campus. Mapillary imagery requires appropriate attribution under its CC-BY-SA terms. [41] For a panorama, first extract a perspective view and update its heading/intrinsics; do not apply a pinhole formula directly to the equirectangular image.

### Projection into world coordinates

Use the obstacle's **ground-contact pixel**, or the relevant curb interface, not its box center. In a pinhole camera:

\[
r = K^{-1}[u,v,1]^T,\quad P_c = z r,\quad P_w = C + R_{wc}P_c.
\]

Here `z` is axial depth. For radial range `d`, use `d * r / ||r||` instead. The following implementation assumes an already oriented image, a calibrated `K`, and a rotation mapping camera right/down/forward coordinates into east/north/up:

```python
import numpy as np
from pyproj import Geod
geod = Geod(ellps="WGS84")

def locate_pixel(lon, lat, u, v, depth_m, K, R_enu_cam, radial=False):
    ray = np.linalg.solve(K, np.array([u, v, 1.0]))
    p_cam = depth_m * (ray / np.linalg.norm(ray) if radial else ray)
    east, north, up = R_enu_cam @ p_cam
    bearing = np.degrees(np.arctan2(east, north))
    distance = np.hypot(east, north)
    out_lon, out_lat, _ = geod.fwd(lon, lat, bearing, distance)
    return out_lon, out_lat
```

The geometry above is an implementation derivation, not a claim that phone metadata provides an accurate full camera pose. Image rotation, stabilization crops, lens distortion, compass reference and camera pitch must be consistent with `K` and `R`.

### Candidate-edge matching, not unconditional nearest-edge snapping

For Jaipur, a metric working CRS such as **WGS84 / UTM zone 43N, EPSG:32643**, is appropriate for local graph geometry. Keep API/browser coordinates in WGS84 longitude/latitude. OSMnx provides graph projection; OpenSidewalks explicitly represents WGS84 coordinates as longitude/latitude. [16][39]

Proposed matching procedure:

1. Project the **estimated obstacle position**, not the camera GPS point.
2. Search multiple candidate pedestrian edges within a configurable uncertainty radius. A **30 m initial search radius** is a demo choice for the stated GPS-error scenario, not a guarantee.
3. Rank candidates using distance normalized by position uncertainty, camera-to-object visibility, path direction, correct road side, and crossing versus sidewalk context.
4. Save the top candidates and their scores. Require review when opposite-side candidates are similarly plausible.
5. Snap along the chosen edge to a measure `s`; attach a point obstacle or split a short affected interval, rather than penalizing an entire long street.

**Planned campus case:** a motorbike photographed from the roadway can project between two parallel sidewalk candidates. Nearest-camera snapping puts it on the photographer's side, not necessarily the motorbike's side. A side-by-side photo/map review resolves that ambiguity far more reliably than silently choosing the closest line.

Keep `semantic_confidence` and `location_confidence` separate. A clearly visible motorbike with uncertain edge assignment should remain a strong visual observation with an unresolved map location.

### Multi-photo triangulation

Associate the same **stationary** obstacle across views, then minimize perpendicular distance to its bearing rays. In a local metric coordinate frame:

```python
def triangulate_xy(camera_xy, unit_bearings, weights):
    A, b = np.zeros((2, 2)), np.zeros(2)
    for c, d, w in zip(camera_xy, unit_bearings, weights):
        P = np.eye(2) - np.outer(d, d)
        A += w * P
        b += w * P @ c
    if np.linalg.cond(A) > 1e4:  # Chosen rejection threshold.
        return None
    return np.linalg.solve(A, b)
```

Reject intersections behind cameras, nearly parallel rays, weak baselines, or inconsistent observations. Multiple photos do not remove a shared GPS bias. SfM can improve relative geometry, but georeferencing and metric scale still need anchors. A moving motorbike must not be triangulated as a stationary landmark.

**Decision:** The app should be able to say **"barrier seen; sidewalk assignment needs review."** "Correct segment" is an outcome to verify, not a property supplied automatically by GPS.

## 4. Graph Construction: Preserve Side, Crossings, And Unknown Infrastructure

### Start with OSMnx, but understand what `walk` means

OSMnx supports `network_type="walk"`; it retrieves a walking network, not a promise that both sidewalks have been separately mapped. Its default polygon import simplifies topology and retains only the largest weak component unless changed. Configure useful tags before downloading. [16]

```python
import osmnx as ox

ox.settings.useful_tags_way = list(set(ox.settings.useful_tags_way + [
    "foot", "access", "sidewalk", "sidewalk:left", "sidewalk:right",
    "wheelchair", "surface", "smoothness", "width", "incline",
    "lit", "tactile_paving", "crossing"
]))
ox.settings.useful_tags_node = list(set(ox.settings.useful_tags_node + [
    "barrier", "kerb", "kerb:height", "wheelchair", "tactile_paving"
]))
G = ox.graph_from_polygon(
    campus_polygon_wgs84, network_type="walk",
    simplify=False, retain_all=True
)
G = ox.project_graph(G, to_crs="EPSG:32643")
ox.save_graphml(G, "campus.graphml")
```

OSMnx documents tag retention through `useful_tags_node` and `useful_tags_way`. Its default access filter excludes `access=private`, which can matter on a campus. Import authorized private paths explicitly only when you have permission; do not silently override access restrictions. [16]

### Three sources of pedestrian geometry

| Source | How to use it | What not to imply |
|---|---|---|
| Explicit OSM footway/sidewalk/crossing | Preserve its geometry and topology; add evidence and review status | OSM presence alone does not establish current accessibility |
| Road centerline plus left/right offsets | Create **candidate** sidewalk geometry, with surveyed/configurable lateral offset | A parallel line is not proof that a sidewalk exists |
| Tile2Net aerial extraction | Produce additional candidate sidewalks/crosswalks from suitable orthophotos | Unvalidated segmentation is not a verified connected pedestrian network |

With Shapely, `line.offset_curve(+offset_m)` and `line.offset_curve(-offset_m)` can generate candidates in a metric CRS. Preserve the parent-road ID and side relative to its original direction. Resolve intersections, road bends, driveways, gates and crossings manually in the small demo area; geometric offsets do not solve topology.

**OpenSidewalks is the useful topology case study.** Its schema connects edges end-to-end, splits crossing/road geometry at shared nodes, and connects sidewalk centerlines to crossings through short footways. It represents curb interfaces where connected edges meet. A rendered line intersection without shared graph nodes is not a routable connection. [39]

Its incline is directional, and width/surface are edge attributes; an edge can be split where width changes. This is exactly why one undifferentiated road-centerline edge is too coarse for barrier-aware routing. [39]

**Tile2Net is the counterexample to an easy overnight shortcut.** It generates a topologically interconnected network from orthorectified imagery, but requires a CUDA GPU and suitable imagery. Its setup prefers zoom **19 or above**, not below **18**, and explicitly warns that a substantially different built environment from the US may need additional training. [22][25]

For tonight, hand-correct a small campus network before attempting Tile2Net. Render inferred edges as dashed and keep them `unknown`; they should not automatically become the wheelchair-friendly route.

### AccessMap, OpenSidewalks, and AccessScore are not the same thing

| System | What it contributes | How to use it here |
|---|---|---|
| **AccessMap** | User-configurable slope limits, curb/stair avoidance and other preferences | Model hard constraints and soft preferences separately |
| **OpenSidewalks** | Connectivity and feature schema | Structure the graph and directional accessibility attributes |
| **Project Sidewalk AccessScore** | Experimental aggregate score from observed features | Show neighborhood/street overview, not certified individual passability |

AccessMap's documented preferences include maximum uphill/downhill steepness and avoidance of raised curbs, stairs, noisy or crowded streets. The sources describe configurable routing behavior, not one universal numerical cost equation to copy. [12]

Project Sidewalk currently describes a street's score as:

\[
A_{street}=\operatorname{sigmoid}\left(\sum_i w_i\right).
\]

Weights depend on positive-feature quality, negative-feature severity and tags. Regional scores are street-length-weighted averages over audited streets, with coverage reported separately; the algorithm is experimental and weights may change. [34]

The non-obvious tension is that a high aggregate score can coexist with **one impassable crossing**. Averaging is useful for dashboards but cannot replace edge-level feasibility checks.

### A transparent personalized cost

Use your own clearly labeled demo function, inspired by personalized routing rather than presented as AccessMap's proprietary or exact implementation:

\[
C_p(e)=\begin{cases}
\infty & \text{if a confirmed constraint fails, or strict policy rejects unknowns}\\
\frac{L_e}{v_p}[1+P_{slope,p}+P_{surface,p}+P_{width,p}]
+P_{crossing,p}+\sum_b P_{b,p}+P_{unknown,p} & \text{otherwise}.
\end{cases}
\]

All terms must be nonnegative and in a consistent generalized-cost unit, such as seconds-equivalent. Evaluate slope separately in each direction. A confirmed impassable barrier remains impassable; do not dilute it by averaging confidence with unrelated good features.

| Profile | Explicit hard-constraint policy | Soft preferences | Important unknowns |
|---|---|---|---|
| **Manual wheelchair** | Reject confirmed stairs/impassable lips or insufficient passage; user-configured limits | Uphill/downhill effort, roughness, detours | Width, cross-slope, landing and curb transitions |
| **Elderly walker** | User-selected stair, steepness and passage limits | Uneven pavement, long crossings, effort | Surface condition and support needs |
| **Pram** | Reject confirmed non-traversable steps or passage narrower than the configured pram | Roughness, slope, awkward crossings | Usable ramp/landing and actual clearance |
| **Low vision** | User-selected exclusions for hazardous crossings or obstructions | Poles, protrusions, confusing crossings, absent guidance | Tactile cues, signal information and obstacle detectability |

These are configuration starting points, not medical prescriptions or universal dimensional standards. A parked motorcycle is not automatically a complete block; the remaining traversable width matters.

**Decision:** Build a small, correct, side-specific graph. Missing information must influence the route instead of disappearing into a reassuring score.

## 5. Routing: A Small Backend Wins Tonight

| Option | Advantages | Main integration cost | Recommendation |
|---|---|---|---|
| **OSMnx + NetworkX backend** | Direct control over observations, profiles, hard exclusions and explanation | You own graph cleanup and API | **Best tonight** |
| **Client-side Dijkstra/A*** | Static hosting, instant local profile changes, offline potential | Export directed adjacency and preserve edge IDs; implement/test costs in JS | Good fallback for a small frozen graph |
| **Valhalla** | Mature pedestrian costing and useful accessibility-related options | Graph tiles, deployment, ingestion of new custom barrier semantics | Use later or if already deployed |
| **OSRM with foot profile** | Efficient routing with an explicitly prepared foot graph | Profile/preprocessing pipeline; arbitrary live barrier costs are not its simplest path | Not the fastest custom-barrier prototype |

Valhalla's pedestrian `type="wheelchair"` changes defaults including distance, walking speed and step penalty; `type="blind"` adds instructions. Those options are useful, but do not establish that your newly detected curb has been attached to its graph or that all wheelchair constraints are enforced. [14]

OSRM's route profile is determined by the Lua profile used when preparing data with `osrm-extract`; typical supplied profiles include car, bike and foot. Merely putting `/foot/` into a request to a car-prepared service does not rebuild its graph. [18]

### Preserve the actual multiedge in the result

OSMnx uses a multigraph; its conversion to a DiGraph selects parallel edges by a weight attribute. You must retain the selected original edge, not just a node sequence. [16]

```python
import math, networkx as nx

def route_for_profile(G, source, target, profile, as_of):
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))
    for u, v, k, edge in G.edges(keys=True, data=True):
        # Your function: excludes forbidden/strict-unknown edges,
        # evaluates only active observations at as_of, returns +inf if blocked.
        cost = edge_cost(edge, profile, as_of)
        if not math.isfinite(cost):
            continue
        if not H.has_edge(u, v) or cost < H[u][v]["cost"]:
            H.add_edge(u, v, cost=cost, original_edge=(u, v, k))
    try:
        nodes = nx.shortest_path(H, source, target, weight="cost")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"status": "no_verified_route", "edges": []}
    edges = [H[u][v]["original_edge"] for u, v in zip(nodes, nodes[1:])]
    return {"status": "route_found", "edges": edges}
```

NetworkX/OSMnx support weighted shortest paths, with Dijkstra documented for these operations. [16] For the UI's two routes, calculate a distance-only baseline and a profile-cost route from the **same graph snapshot**. Label the baseline "shortest", not "recommended".

Snap origins/destinations onto the correct side too, splitting edges if necessary. Do not add a straight nearest-node connector that crosses an uncrossable road or campus wall. If strict wheelchair routing finds no supported route, return that result rather than quietly re-enabling forbidden edges.

### Minimal API and evidence contract

```text
POST /observations       upload image + pose sidecar; return job_id
GET  /jobs/{id}          processing status and proposals
PATCH /observations/{id} reviewer label, contact pixel, edge and state
GET  /graph              directed nodes/edges + observation references
POST /route              origin, destination, profile, as_of, unknown_policy
```

Separate observation identity from graph identity:

```text
Observation:
  id, image_id, label, bbox_or_mask, ground_contact_pixel,
  detector_outputs[], agreement_score, semantic_state,
  estimated_lonlat, location_uncertainty, candidate_edges[], matched_edge_id,
  edge_measure_m, observed_at, reviewed_at, valid_until,
  height_cm_estimate, height_method, height_uncertainty, reviewer_notes

Edge:
  stable_id, from, to, geometry, length_m, parent_osm_id, side,
  infrastructure_source, verification_state,
  directional_grade, width_m, surface, crossings, observations[]
```

Expire transient observations with an explicitly chosen policy; keep structural observations subject to reinspection. Record field-level review dates rather than treating one timestamp as validation of all attributes, consistent with OSM's property-specific `check_date:*` convention. [44]

**Decision:** Use FastAPI plus saved GraphML/GeoJSON and static image assets. Keep inference outside the request-response route calculation. A frozen client graph is the emergency deployment fallback.

## 6. World-Model Visuals: One Crossing, Optional Reconstruction

### What can actually run on the available hardware?

| Approach | Real output | Resource evidence | Tonight's role |
|---|---|---|---|
| **gsplat + Splatfacto** | Trained Gaussian scene | Stock Splatfacto about **6 GB**, bigger about **12 GB** | Optional on a separate GPU |
| **VGGT** | Cameras, depths, point maps and tracks; COLMAP export | Repository describes rapid reconstruction, but no defensible GTX 1650 timing/memory figure here | Optional pose/point initializer, not a finished splat |
| **MASt3R** | Matches, 3D predictions and aligned reconstruction | Official example uses a 512-sized model and CUDA; no target-device runtime established | Alternative geometric reconstruction, not an automatic browser-ready splat |
| **Photo-sequence walkthrough** | Recorded photographic evidence | No reconstruction requirement | Most dependable local fallback |
| **Generated walkthrough video** | Synthetic visualization | Not a geometric measurement or observation | Decorative, clearly labeled; never routing evidence |

The distinction between **geometry initialization** and **Gaussian training** is essential. VGGT exports cameras and points that can feed a separate gsplat training pipeline; MASt3R supplies matching/reconstruction rather than a trained splat. [17][26]

**Splatfacto is the practical case study.** It uses gsplat, works better with SfM initialization such as COLMAP points, and trains on full images. Its documented default memory is already above this laptop's 4 GB. gsplat's reported savings of up to **4x memory** and up to **15% training time** versus the original implementation do not mean every scene fits on a GTX 1650. [28][7]

Therefore choose a **12-24 GB rental GPU as a planning allocation**, not a claim that this much is always necessary. Reserve one optional hour and use an early success/failure gate. There is no reliable source-backed total runtime for your exact 20-50-image capture, COLMAP alignment, model settings and hardware; the commands below must be tested, not sold as a fixed-minute guarantee.

### Capture and training recipe

Capture the proposed **20-50 overlapping photos** of one crossing from safe positions, with real lateral baseline, several viewing heights, sharp texture, and no zoom changes. Avoid relying on moving people/vehicles as reconstruction features. A stationary poorly parked bike may move between captures, so record its observation separately.

Nerfstudio requires camera poses, and its image processing uses COLMAP/FFmpeg; its capture guidance emphasizes overlapping, non-blurry images. [38]

```bash
# Requires a working CUDA/PyTorch/Nerfstudio environment and COLMAP.
ns-process-data images --data capture --output-dir scene

# 3000 iterations is a chosen draft budget, not a quality guarantee.
ns-train splatfacto --data scene --max-num-iterations 3000

ns-export gaussian-splat \
  --load-config outputs/.../config.yml \
  --output-dir exports/crossing
```

The processing, training and export command families are documented. [38][28] If alignment fails or the preview remains unusable at the allocated checkpoint, stop. Do not spend the remaining evening debugging CUDA extensions.

Do not assume local splat coordinates are georeferenced or metric. For tonight, open the scene in a separate modal tied to the crossing's evidence ID. Registering it accurately into the map is additional work and should not change routing geometry without validation.

### Browser viewers

| Viewer | Best use | Trade-off |
|---|---|---|
| **antimatter15/splat** | Fast proof that an exported scene can render | Minimal viewer; integrates less naturally with a rich scene |
| **Spark** | Gaussian scenes inside an existing Three.js experience | More integration, but clean mesh/annotation composition |
| **gsplat.js** | Self-contained JS scene/camera/loader approach | Its compact `.splat` representation drops SH coefficients, so color is not view-dependent |

antimatter15's viewer uses WebGL, CPU-worker sorting and progressive loading. Spark exposes `SparkRenderer` and `SplatMesh`; gsplat.js exposes scene/camera/renderer and async loading APIs. [36][35][33]

```js
import { SparkRenderer, SplatMesh } from "@sparkjsdev/spark";

// renderer, scene and camera are your existing THREE objects.
scene.add(new SparkRenderer({ renderer }));
const crossing = new SplatMesh({ url: "/assets/crossing.ply" });
scene.add(crossing);
renderer.setAnimationLoop(() => renderer.render(scene, camera));
```

If reconstruction fails, a smooth photo carousel, an actual captured walking clip, or a Three.js textured-photo sequence still gives a strong spatial narrative. If you generate a video, watermark it **"synthetic illustration - not surveyed geometry"** and keep original photos one click away.

**Decision:** A genuine small splat is a bonus. A generated scene must never become evidence for curb height, passage width, or route safety.

## 7. Browser Experience: Make The Detour Explain Itself

Use **MapLibre + deck.gl** for the map and keep Three.js/Spark in an optional evidence modal. Start with an overlaid deck canvas for predictable integration; use interleaving only when needed. `MapboxOverlay` supports both modes, while interleaving shares the basemap's WebGL2 context and is not supported with WebGL1 basemaps. [43]

### Visual grammar

| Element | Suggested rendering | Meaning |
|---|---|---|
| Shortest route | Thin, muted line | Distance baseline, not a safety recommendation |
| Profile-aware route | Bright solid line and animated traveler | Selected route under visible preferences |
| Confirmed barrier | Solid warning symbol | Reviewed observation |
| Unsure detection | Hollow amber symbol | Needs semantic or location review |
| Uncertainty | Translucent spatial halo | Location is approximate |
| Inferred sidewalk | Dashed line | Candidate infrastructure, not verified existence |
| Evidence card | Photo, crop/mask, age, source, edge and reason | Why this observation affects the route |

Do not rely on red/green alone. Provide keyboard-operable evidence controls, a textual route comparison, and a reduced-motion mode. The low-vision persona should be reflected in the interface, not only in route-cost coefficients.

TripsLayer takes a path plus one timestamp per vertex; `currentTime` is the playhead. Its timestamps use 32-bit floats, so use seconds relative to route start rather than Unix epoch time. [2]

```js
import { MapboxOverlay } from "@deck.gl/mapbox";
import { PathLayer, ScatterplotLayer } from "@deck.gl/layers";
import { TripsLayer } from "@deck.gl/geo-layers";

// routes: [{id, path: [[lon,lat],...], times: [0,...], color}]
// times are cumulative route travel times, with one entry per vertex.
const overlay = new MapboxOverlay({ interleaved: false, layers: [] });
map.addControl(overlay);
const start = performance.now();

function frame(now) {
  const t = (((now - start) / 1000) * playbackRate) % playbackDuration;
  overlay.setProps({ layers: [
    new PathLayer({
      id: "route-underlay", data: routes,
      getPath: d => d.path, getColor: d => d.color,
      getWidth: 4, widthUnits: "pixels"
    }),
    new TripsLayer({
      id: "route-motion", data: routes,
      getPath: d => d.path, getTimestamps: d => d.times,
      getColor: d => d.color, currentTime: t,
      trailLength: 8, widthMinPixels: 6,
      capRounded: true, jointRounded: true
    }),
    new ScatterplotLayer({
      id: "evidence", data: observations, pickable: true,
      getPosition: d => d.lonlat,
      getRadius: 5, radiusUnits: "pixels",
      getFillColor: d => d.state === "verified"
        ? [240, 90, 70] : [245, 180, 50],
      onClick: ({object}) => object && openEvidence(object.id)
    })
  ]});
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

The underlying overlay update and TripsLayer properties follow documented APIs; picking is enabled per layer with `pickable`. [43][2]

**Planned demonstration case:** select manual wheelchair, then animate both routes. When the baseline reaches a reviewed step or blocked crossing, pause its explanation and open the evidence card; continue the alternative route and show the detour reason. Present the barrier from your actual data, not a fabricated "success" metric.

Keep physical travel time separate from animation speed and from generalized accessibility cost. If an uncertain obstacle drives a conservative detour, say **"avoids an unverified crossing"**, not **"this crossing is inaccessible"**. Changing profile should update both the route and its explanation.

**Decision:** The strongest visual is a legible causal chain: photo -> reviewed observation -> affected edge -> changed route.

## Synthesis: What To Trust, What To Approximate

| Strategy | Mechanism | Scope and evidence | Trade-off / time horizon |
|---|---|---|---|
| Two-detector proposals | Different models propose matching visual objects | Photographic semantics; local evaluation needed | Fast to prototype; correlated errors remain |
| Metric monocular depth | Learned metric scene reconstruction | Range/geometry estimates, not certified curb height | Useful now for projection; calibration needed for measurement |
| Phone pose plus ray projection | Transform a pixel-derived 3D location into world coordinates | Limited by capture pose and depth quality | Immediate coarse localization; manual side review remains valuable |
| Multi-view reconstruction | Match observations across viewpoints and solve geometry | Relative geometric consistency | Better evidence but more association/registration work |
| OSM/OpenSidewalks graph | Encode connectivity and traversal attributes | Depends on completeness and field review | Essential core; topology errors outweigh visual polish |
| AccessMap-style personalization | Apply user constraints and preferences | A particular user's traversal needs | Good routing abstraction; no universal profile is sufficient |
| AccessScore | Aggregate weighted feature evidence through a sigmoid | Street/region overview, with audit coverage | Useful visualization; may conceal a single critical barrier |
| Gaussian evidence viewer | Reconstruct and render a local scene | Visual inspection, not automatic accessibility certification | High presentation value; optional under tonight's constraints |

The underlying source distinctions matter: OpenSidewalks specifies connectivity, AccessMap exposes configurable preferences, AccessScore aggregates observations, and Splatfacto reconstructs appearance from posed imagery. These are complementary components, not interchangeable solutions to accessibility. [39][12][34][28]

Three tensions determine the architecture. First, **semantic certainty and positional certainty can diverge**: an obvious pole may belong to either of two mapped paths. Second, **global quality and local feasibility diverge**: a street can score well while one crossing blocks a specific user. Third, **visual realism and evidential reliability diverge**: an attractive reconstruction or generated video does not validate centimetre geometry.

Keep separate confidence states for class, height, location, infrastructure existence and user passability. Preserve source image, processing activity and reviewer decisions, following the basic provenance idea of tracking the entities, activities and people that produced data. [45]

The best nine-hour deliverable is therefore a **small honest digital twin**: limited coverage, explicit unknowns, stable edge identities, configurable constraints, and persuasive original evidence. Expand geography and automate review only after that loop works.

## Nine-Hour Build Plan And Risk Fallbacks

This schedule assumes one builder, a small selected campus area, and some existing familiarity with Python and browser development. All durations are task budgets, not measured model runtimes. The stock Splatfacto memory requirement is the reason reconstruction remains optional rather than blocking the application. [28]

| Hour | Deliverable and work | Acceptance gate | Fallback if risky |
|---|---|---|---|
| **0-1** | Choose the exact campus polygon and demonstration crossing. Create Vite/React/MapLibre shell and Python environment. Download one detector and graph data; test image upload/sidecar. | Map loads; one real image and its source metadata are visible. | Use a frozen local graph and local photos if Overpass, Mapillary, tokens or network access fail. |
| **1-2** | Import OSM walking graph with needed tags. Inspect gates, separate sidewalk sides, and explicitly connect crossings. Hand-correct the short demonstration corridor. | Origin and destination connect through physically plausible topology. | Draw reviewed GeoJSON paths manually, clearly labeled as demo-authored/inferred. |
| **2-3** | Run YOLO-World and a small local photo audit. Save boxes and evidence crops. Measure actual inference latency/memory. | The essential photos have inspectable detections; errors are visible. | CPU batch inference, remote inference if permitted, or manually reviewed labels. Do not block the UI on inference. |
| **3-4** | Run second detector; normalize labels, compute agreement, implement `unsure` and review actions. | Disagreement produces a review item, not a silent deletion. | Keep single-model proposals flagged unsure; use a human as the second review channel, not a fake second detector. |
| **4-5** | Project contact points, rank candidate edges, build pin/edge reassignment. Test metric depth on the featured curb. | Reviewer can verify the correct path side and crossing interface. | Manual edge assignment; height remains unknown or separately physically measured. |
| **5-6** | Implement profile costs, hard exclusions, unknown policy, transient-observation validity, baseline/profile routes and no-route handling. | Changing a profile changes a relevant route or explains why it does not. | Frozen client-side graph plus Dijkstra; precomputed reviewed routes as a final presentation fallback. |
| **6-7** | Add competing-route animation, evidence cards, uncertainty styling and keyboard/text alternatives. | A viewer can explain the detour from the evidence without narration. | Static route lines, clickable photos and a clear textual comparison. |
| **7-8** | Optional separate-GPU reconstruction of one crossing; otherwise create a genuine photographic walkthrough. Integrate Spark only if a usable export already exists. | Usable scene/photo sequence appears within this hour's budget. | Stop reconstruction; use photos or captured video. Any generated video is explicitly synthetic and excluded from routing evidence. |
| **8-9** | Freeze versions and assets; test profile changes, no-route cases, stale motorbike observations, wrong-side snapping, missing GPS, mobile display and offline fallback. Record the demo. | Reproducible happy path plus honest failure behavior; no unsupported "safe route" claim. | Serve a fully static build with cached graph, evidence and clearly labeled precomputed route examples. |

**Final scope cut:** protect graph correctness, reviewable evidence, and profile-dependent routing. Drop automatic centimetre claims first, live inference second, and Gaussian reconstruction third. A beautiful map that clearly admits uncertainty is a much stronger demonstration than a photorealistic system that silently routes someone onto the wrong footpath.

## References

1. *Home - Spark*. https://sparkjs.dev/
2. *TripsLayer | deck.gl*. https://deck.gl/docs/api-reference/geo-layers/trips-layer
3. [GitHub - DepthAnything/Depth-Anything-V2: [NeurIPS 2024] Depth Anything V2. A More Capable Foundation Model for Monocular Depth Estimation · GitHub](https://github.com/DepthAnything/Depth-Anything-V2)
4. [GitHub - AILab-CVC/YOLO-World: [CVPR 2024] Real-Time Open-Vocabulary Object Detection · GitHub](https://github.com/AILab-CVC/YOLO-World)
5. *GitHub - facebookresearch/sam2: The repository provides code for running inference with the Meta Segment Anything Model 2 (SAM 2), links for downloading the trained model checkpoints, and example notebooks that show how to use the model. · GitHub*. https://github.com/facebookresearch/sam2
6. *GitHub - lpiccinelli-eth/UniDepth: Universal Monocular Metric Depth Estimation · GitHub*. https://github.com/lpiccinelli-eth/UniDepth
7. *GitHub - nerfstudio-project/gsplat: CUDA accelerated rasterization of gaussian splatting · GitHub*. https://github.com/nerfstudio-project/gsplat
8. [GitHub - IDEA-Research/GroundingDINO: [ECCV 2024] Official implementation of the paper "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection" · GitHub](https://github.com/IDEA-Research/GroundingDINO)
9. *GitHub - YvanYin/Metric3D: The repo for "Metric3D: Towards Zero-shot Metric 3D Prediction from A Single Image" and "Metric3Dv2: A Versatile Monocular Geometric Foundation Model..." · GitHub*. https://github.com/yvanyin/metric3d
10. *docs – The Taskar Center for Accessible Technology*. https://tcat.cs.washington.edu/tcat-documentation
11. *API Documentation*. https://www.mapillary.com/developer/api-documentation
12. *AccessMap – The Taskar Center for Accessible Technology*. https://tcat.cs.washington.edu/accessmap
13. *RampNet: A Two-Stage Pipeline for Bootstrapping Curb Ramp Detection in Streetscape Images from Open Government Metadata*. https://arxiv.org/abs/2508.09415
14. *API reference - Valhalla Docs*. https://valhalla.github.io/valhalla/api/turn-by-turn/api-reference/
15. *google/owlv2-base-patch16-ensemble · Hugging Face*. https://huggingface.co/google/owlv2-base-patch16-ensemble
16. *User Reference ¶*. https://osmnx.readthedocs.io/en/stable/user-reference.html
17. [GitHub - facebookresearch/vggt: [CVPR 2025 Best Paper Award] VGGT: Visual Geometry Grounded Transformer · GitHub](https://github.com/facebookresearch/vggt)
18. *OSRM API Documentation*. https://project-osrm.org/docs/v5.24.0/api/
19. *Mapillary API: FAQs*. https://www.mapillary.com/developer/api-documentation/faq
20. *Qwen/Qwen2.5-VL-3B-Instruct · Hugging Face*. https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct
21. *UniDepthV2: Universal Monocular Metric Depth Estimation Made Simpler*. https://arxiv.org/abs/2502.20110
22. *GitHub - VIDA-NYU/tile2net: Automated mapping of pedestrian networks from aerial imagery tiles · GitHub*. https://github.com/VIDA-NYU/tile2net
23. *Depth-Anything-V2/metric_depth at main · DepthAnything/Depth-Anything-V2 · GitHub*. https://github.com/DepthAnything/Depth-Anything-V2/tree/main/metric_depth
24. *GPS Tags*. https://exiftool.org/TagNames/GPS.html
25. *Vida Nyu*. https://raw.githubusercontent.com/VIDA-NYU/tile2net/main/BASICS.md
26. *GitHub - naver/mast3r: Grounding Image Matching in 3D with MASt3R · GitHub*. https://github.com/naver/mast3r
27. *microsoft/Florence-2-base · Hugging Face*. https://huggingface.co/microsoft/Florence-2-base
28. *Splatfacto - nerfstudio*. https://docs.nerf.studio/nerfology/methods/splat.html
29. *Metric3D v2: A Versatile Monocular Geometric Foundation Model for Zero-shot Metric Depth and Surface Normal Estimation*. https://arxiv.org/pdf/2404.15506v2
30. *YOLO-World: Real-Time Open-Vocabulary Object Detection - arXiv*. https://arxiv.org/html/2401.17270v2
31. *GitHub - ProjectSidewalk/SidewalkWebpage: Project Sidewalk web page · GitHub*. https://github.com/ProjectSidewalk/SidewalkWebpage
32. *YOLO-World Model | Ultralytics Docs*. https://docs.ultralytics.com/models/yolo-world/
33. *GitHub - huggingface/gsplat.js: JavaScript Gaussian Splatting library. · GitHub*. https://github.com/huggingface/gsplat.js
34. *API Docs — Project Sidewalk*. https://sidewalk-seattle.cs.washington.edu/api
35. *Getting Started - Spark*. https://sparkjs.dev/docs/
36. *GitHub - antimatter15/splat: WebGL 3D Gaussian Splat Viewer · GitHub*. https://github.com/antimatter15/splat
37. *YOLO-World: Real-Time Open-Vocabulary Object Detection V X*. https://arxiv.org/pdf/2401.17270
38. *Using custom data - nerfstudio*. https://docs.nerf.studio/quickstart/custom_dataset.html
39. *GitHub - OpenSidewalks/OpenSidewalks-Schema: Repository for the draft proposal of the OpenSidewalks schema · GitHub*. https://github.com/OpenSidewalks/OpenSidewalks-Schema
40. *GitHub - Dao-AILab/flash-attention: Fast and memory-efficient exact attention · GitHub*. https://github.com/Dao-AILab/flash-attention
41. *CC-BY-SA license for open data – Mapillary*. https://help.mapillary.com/hc/en-us/articles/115001770409-CC-BY-SA-license-for-open-data
42. *Overview - Spark*. https://sparkjs.dev/docs/overview/
43. *MapboxOverlay | deck.gl*. https://deck.gl/docs/api-reference/mapbox/mapbox-overlay
44. *Key:check_date - OpenStreetMap Wiki*. https://wiki.openstreetmap.org/wiki/Key:check_date
45. *PROV-Overview*. https://www.w3.org/TR/prov-overview
