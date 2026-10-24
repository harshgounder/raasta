# barriers.input.json: what the routing lane reads

Path (stable): `app/site-data/<city>/barriers.input.json`, for example `app/site-data/jaipur/barriers.input.json`.
`python -m hroute.cli precompute <city>` (from `app/route`) attaches every record before routing. The same
objects can be POSTed live to `/barriers` as `{"city": "jaipur", "records": [ ... ]}`.

The file is a JSON list of records. One bad record is reported as REJECT in `barriers.json` and never
stops the run.

## Record

| field | required | type | meaning |
|---|---|---|---|
| `id` | yes (strongly) | string | stable id, e.g. `analyze-<photo-sha>-<n>`. Re-sending the same id replaces the old record |
| `type` | yes | string | one of `missing_kerb_ramp`, `steps`, `broken_footpath`, `missing_footpath`, `pole_obstruction`, `parked_vehicle`, `pothole`, `open_drain`, `vendor`, `waterlogging`; extension `steep_slope`; positive evidence `kerb_ramp_present`, `crossing_marked`, `clear` (photo shows the footpath fine: this is what lowers "unknown") |
| `lat`, `lon` | yes | number | WGS84 degrees |
| `position` | no | `camera` (default) or `barrier` | `camera`: lat/lon is the photo's GPS; `barrier`: lat/lon is already the barrier spot |
| `heading` | no | number | camera view direction, degrees clockwise from north (EXIF GPSImgDirection) |
| `side_hint` | no | `left` or `right` | which footpath of the road the barrier is on, as seen in the photo |
| `distance_m` | no | number | how far ahead of the camera the barrier is (camera mode) |
| `gps_error_m` | no (default 8) | number | GPS horizontal error (EXIF GPSHPositioningError if present) |
| `confidence` | no (default 0.8) | 0..1 | detector confidence that the barrier is real |
| `status` | no (default ACCEPT) | `ACCEPT` or `ABSTAIN` | detector decision. ABSTAIN records are kept as candidates only and never change routes |
| `observed_at` | yes for routing over time | ISO 8601 | photo time WITH time of day and offset, e.g. `2026-10-24T18:40:00+05:30`. A date only (`2026-10-24`) disables the hour-of-day curve |
| `permanence` | no | `permanent` or `temporary` | default: temporary for `parked_vehicle`, `vendor`, `waterlogging`; permanent otherwise |
| `half_life_h` | no | number | temporary only; default from assumptions.json (parked_vehicle 2, vendor 6, waterlogging 24) |
| `height_cm` | no | number | kerb or step height. Missing height on `missing_kerb_ramp` is treated as above 2 cm (blocks wheelchairs) |
| `clear_width_cm` | no | number | remaining clear width beside a pole, vendor or vehicle; below 90 blocks wheelchairs, below 70 blocks prams |
| `slope_pct` | no | number | ramp or path slope in percent (7.5 = 1:13) |
| `source` | no (default `photo`) | string | `photo`, `upload`, `video_frame`, `mapillary`, `manual_survey` count as evidence; `what_if` never does |
| `label`, `photo`, `ref` | no | string | free text, photo URL or path, licence or credit line. Shown in receipts |
| `segment_id` | no | string | only if the caller already knows the network segment (skips placement) |

## Example

```json
[
  {"id": "analyze-3f2a9c-0", "type": "missing_kerb_ramp", "lat": 26.92281, "lon": 75.82671,
   "position": "camera", "heading": 182, "side_hint": "left", "gps_error_m": 6,
   "confidence": 0.83, "status": "ACCEPT", "height_cm": 14, "observed_at": "2026-10-24T17:55:00+05:30",
   "source": "photo", "photo": "receipts/3f2a9c.jpg", "label": "kerb without ramp at Badi Chaupar"},
  {"id": "analyze-3f2a9c-1", "type": "vendor", "lat": 26.92281, "lon": 75.82671, "heading": 182,
   "side_hint": "right", "gps_error_m": 6, "confidence": 0.77, "clear_width_cm": 70,
   "observed_at": "2026-10-24T17:55:00+05:30", "source": "photo"}
]
```

## What comes back (barriers.json, one placement per record)

`status` ACCEPT (with `segment_id`, `p` >= 0.7), ABSTAIN (with the top 5 `candidates`, each
`{segment_id, p, distance_m, side, kind}`) or REJECT (with `reason`), plus the validated `record`.
