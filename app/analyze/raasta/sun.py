"""Sun position. Engine 1: NOAA general solar position formula (no dependencies).
Engine 2: pvlib (if installed). The receipt carries both and their difference."""
from __future__ import annotations

import datetime as dt
import math


def noaa(lat: float, lon: float, t: dt.datetime) -> tuple[float, float]:
    """Return (elevation_deg, azimuth_deg clockwise from north). t must be tz-aware."""
    u = t.astimezone(dt.timezone.utc)
    doy = u.timetuple().tm_yday
    hour = u.hour + u.minute / 60 + u.second / 3600
    g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    tst = hour * 60 + eqt + 4 * lon            # true solar time, minutes (UTC based)
    ha = math.radians(tst / 4 - 180)
    la = math.radians(lat)
    cz = math.sin(la) * math.sin(decl) + math.cos(la) * math.cos(decl) * math.cos(ha)
    cz = max(-1.0, min(1.0, cz))
    zen = math.acos(cz)
    elev = 90 - math.degrees(zen)
    az = math.degrees(math.atan2(math.sin(ha), math.cos(ha) * math.sin(la) - math.tan(decl) * math.cos(la)))
    az = (az + 180) % 360
    return elev, az


def sun(lat: float, lon: float, t: dt.datetime) -> dict:
    e1, a1 = noaa(lat, lon, t)
    out = {"elevation_deg": round(e1, 2), "azimuth_deg": round(a1, 2), "engine": "NOAA formula"}
    try:
        import pandas as pd
        import pvlib
        sp = pvlib.solarposition.get_solarposition(pd.DatetimeIndex([t]), lat, lon)
        e2, a2 = float(sp["apparent_elevation"].iloc[0]), float(sp["azimuth"].iloc[0])
        out["check"] = {"engine": "pvlib", "elevation_deg": round(e2, 2), "azimuth_deg": round(a2, 2),
                        "diff_elev_deg": round(abs(e1 - e2), 2),
                        "diff_az_deg": round(abs((a1 - a2 + 180) % 360 - 180), 2)}
    except Exception as e:  # noqa: BLE001
        out["check"] = f"pvlib unavailable ({type(e).__name__})"
    return out
